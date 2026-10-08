#!/usr/bin/env python3
"""Extract the frames a reviewer must look at: contact sheets, both sides of every cut, first/last frame,
bursts around suspicious moments, and reference-vs-frame comparisons for identity/product checks.

Usage: review_frames.py VIDEO --out DIR [--report report.json] [--every 1.0] [--ref ref.jpg ...] [--burst 3.2 ...]
Writes DIR/manifest.json (image paths per group) and DIR/index.tsv (file → timestamp). Needs ffmpeg. Read-only on VIDEO.
Still frames cannot prove motion: list motion questions you could not answer as NOT_INSPECTABLE.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

THUMB_W = 360


def _ff(*args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *map(str, args)], check=True)


def _duration(video):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(video)],
                         check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def _frame(video, t, path, width=None):
    vf = [f'scale={width}:-2'] if width else []
    _ff('-ss', f'{max(t, 0):.3f}', '-i', video, '-frames:v', '1', *(['-vf', ','.join(vf)] if vf else []), '-q:v', '3', path)
    return path


def extract(video, out, report=None, every=1.0, refs=(), bursts=()):
    video, out = Path(video), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    dur = _duration(video)
    index, manifest = [], {'contact_sheets': [], 'cut_pairs': [], 'first_last': [], 'bursts': [], 'ref_compare': []}

    # Contact sheets: one tile every `every` s, 4 columns x 3 rows per sheet (row-major, see index.tsv).
    times = [round(i * every, 3) for i in range(int(dur / every) + 1) if i * every < dur]
    per_sheet = 12
    for s in range(0, len(times), per_sheet):
        chunk = times[s:s + per_sheet]
        sheet = out / f'sheet_{s // per_sheet + 1:02d}.jpg'
        _ff('-i', video, '-vf', f"fps=1/{every},trim=start={chunk[0]}:end={chunk[-1] + every / 2},setpts=PTS-STARTPTS,"
            f"scale={THUMB_W}:-2,tile=4x3:padding=4:color=white", '-frames:v', '1', '-q:v', '3', sheet)
        manifest['contact_sheets'].append(str(sheet))
        index += [(f'{sheet.name}#tile{k + 1}', t) for k, t in enumerate(chunk)]

    # First / last frame.
    for name, t in (('first', 0.0), ('last', max(dur - 0.05, 0))):
        p = _frame(video, t, out / f'{name}.jpg', 720)
        manifest['first_last'].append(str(p))
        index.append((p.name, t))

    # Cut pairs: just before | just after each detected cut (continuity, match cuts, identity across shots).
    for i, c in enumerate((report or {}).get('cuts', []), 1):
        a, b = _frame(video, c - 0.1, out / f'_a{i}.jpg', THUMB_W), _frame(video, c + 0.1, out / f'_b{i}.jpg', THUMB_W)
        pair = out / f'cutpair_{i:02d}_{c:.2f}s.jpg'
        _ff('-i', a, '-i', b, '-filter_complex', 'hstack=inputs=2', '-q:v', '3', pair)
        a.unlink(), b.unlink()
        manifest['cut_pairs'].append(str(pair))
        index.append((pair.name, c))

    # Bursts: 5 frames t-1 .. t+1 (0.5 s steps) for a suspicious moment (hands, contact, text, mouth).
    for t in bursts:
        ts = [round(t + k * 0.5, 3) for k in range(-2, 3) if 0 <= t + k * 0.5 < dur]
        parts = [_frame(video, x, out / f'_burst_{j}.jpg', THUMB_W) for j, x in enumerate(ts)]
        burst = out / f'burst_{t:.2f}s.jpg'
        _ff(*sum((['-i', p] for p in parts), []), '-filter_complex', f'hstack=inputs={len(parts)}', '-q:v', '3', burst)
        for p in parts:
            p.unlink()
        manifest['bursts'].append(str(burst))
        index += [(f'{burst.name}#{j + 1}', x) for j, x in enumerate(ts)]

    # Reference | frame at 4 evenly spaced moments, same height, for identity / product-truth comparison.
    for r, ref in enumerate(refs, 1):
        for k in range(4):
            t = round(dur * (k + 0.5) / 4, 2)
            f = _frame(video, t, out / '_rc.jpg')
            cmp = out / f'refcmp_{r}_{k + 1}_{t:.2f}s.jpg'
            _ff('-i', ref, '-i', f, '-filter_complex', '[0:v]scale=-2:640[a];[1:v]scale=-2:640[b];[a][b]hstack=inputs=2',
                '-q:v', '3', cmp)
            f.unlink()
            manifest['ref_compare'].append(str(cmp))
            index.append((cmp.name, t))

    (out / 'index.tsv').write_text('file\tt_seconds\n' + ''.join(f'{f}\t{t}\n' for f, t in index), encoding='utf-8')
    manifest.update(video=str(video), duration=dur, every=every)
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    return manifest


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--report', type=Path, help='probe_checks.py --out report (adds cut pairs)')
    ap.add_argument('--every', type=float, default=1.0)
    ap.add_argument('--ref', type=Path, action='append', default=[])
    ap.add_argument('--burst', type=float, action='append', default=[])
    a = ap.parse_args(argv)
    try:
        report = json.loads(a.report.read_text(encoding='utf-8')) if a.report else None
        m = extract(a.video, a.out, report, a.every, a.ref, a.burst)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
    for group in ('contact_sheets', 'cut_pairs', 'first_last', 'bursts', 'ref_compare'):
        print(f'{group}: {len(m[group])}')
    print(f'manifest: {a.out / "manifest.json"} — view every image before giving a verdict.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
