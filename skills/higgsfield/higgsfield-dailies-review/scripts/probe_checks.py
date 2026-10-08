#!/usr/bin/env python3
"""Measurable checks on a generated clip: duration, aspect, resolution, audio, black gaps, freezes, cuts vs prompt.

Usage: probe_checks.py VIDEO [--job job.json] [--prompt prompt.txt] [--out report.json]
Statuses: PASS · ISSUE (blocks KEEP) · WARN (look at it) · NA (nothing to compare against).
Exit 1 when any ISSUE. Needs ffmpeg/ffprobe; local and read-only.
These checks cannot judge identity, product truth, hands or acting — review_frames.py prepares frames for that.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

RES_SHORT_SIDE = {'480p': 480, '720p': 720, '1080p': 1080, '1k': 1080, '2k': 1440, '4k': 2160}
RANGE_RE = re.compile(r'^\s*(?:SHOT|CUT)\s+\d+\s*\(?\s*(\d+(?:\.\d+)?)\s*s?\s*(?:–|—|-|to)\s*(\d+(?:\.\d+)?)\s*s', re.I | re.M)
BLOCK_RE = re.compile(r'^\s*(?:SHOT|CUT)\s+\d+\s*(?:\(|:|—|–|-)', re.I | re.M)
ONER_RE = re.compile(r'one continuous (?:take|shot)|no cuts|single take|unbroken shot', re.I)


def ffprobe(video):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                          'format=duration:stream=codec_type,width,height,r_frame_rate', '-of', 'json', str(video)],
                         check=True, capture_output=True, text=True).stdout
    data = json.loads(out)
    v = next(s for s in data['streams'] if s['codec_type'] == 'video')
    num, den = (int(x) for x in v['r_frame_rate'].split('/'))
    return {'duration': float(data['format']['duration']), 'width': v['width'], 'height': v['height'],
            'fps': round(num / den, 3) if den else None,
            'audio': any(s['codec_type'] == 'audio' for s in data['streams'])}


def detect(video, has_audio):
    """One decode pass: blackdetect + freezedetect + scdet (+ silencedetect when audio exists)."""
    cmd = ['ffmpeg', '-hide_banner', '-nostats', '-i', str(video),
           '-vf', 'blackdetect=d=0.2:pix_th=0.10,freezedetect=n=0.003:d=1.0,scdet=threshold=10']
    cmd += ['-af', 'silencedetect=n=-50dB:d=0.5'] if has_audio else ['-an']
    cmd += ['-f', 'null', '-']
    log = subprocess.run(cmd, capture_output=True, text=True).stderr
    black = [(float(a), float(b)) for a, b in re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', log)]
    fs = [float(x) for x in re.findall(r'freeze_start: ([\d.]+)', log)]
    fe = [float(x) for x in re.findall(r'freeze_end: ([\d.]+)', log)]
    freeze = list(zip(fs, fe + [None] * (len(fs) - len(fe))))
    cuts = [float(t) for _, t in re.findall(r'lavfi\.scd\.score: ([\d.]+), lavfi\.scd\.time: ([\d.]+)', log)]
    ss = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
    se = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    silence = list(zip(ss, se + [None] * (len(ss) - len(se))))
    return black, freeze, cuts, silence


def merge_cuts(cuts, black, tol=0.25):
    """A black gap is one transition: drop cuts at its start/end, keep one at the gap start."""
    kept = []
    for t in sorted(cuts):
        if any(a - tol <= t <= b + tol for a, b in black):
            continue
        if not kept or t - kept[-1] > tol:
            kept.append(t)
    gaps = [a for a, b in black if a > tol]
    return sorted(kept + gaps)


def expected_cuts(prompt):
    """(count, times) of cuts the prompt asks for; (None, []) when the prompt does not say."""
    if not prompt.strip():
        return None, []
    if ONER_RE.search(prompt):
        return 0, []
    spans = [(float(a), float(b)) for a, b in RANGE_RE.findall(prompt)]
    if spans:
        return len(spans) - 1, sorted(b for _, b in spans)[:-1]
    blocks = len(BLOCK_RE.findall(prompt))
    return (blocks - 1, []) if blocks else (None, [])


def run_checks(video, job=None, prompt=''):
    job = job or {}
    p = ffprobe(video)
    black, freeze, raw_cuts, silence = detect(video, p['audio'])
    cuts = merge_cuts(raw_cuts, black)
    checks = []

    def add(cid, title, st, detail):
        checks.append({'id': cid, 'title': title, 'status': st, 'detail': detail})

    d = job.get('duration_s')
    if d is None:
        add('T01', 'duration', 'NA', f"{p['duration']:.2f}s (no job duration)")
    else:
        ok = abs(p['duration'] - d) <= max(0.3, 0.02 * d)
        add('T01', 'duration', 'PASS' if ok else 'ISSUE', f"{p['duration']:.2f}s vs job {d}s")

    aspect = str(job.get('aspect', '')).lower()
    if not re.fullmatch(r'\d+:\d+', aspect):
        add('T02', 'aspect', 'NA', f"{p['width']}x{p['height']} (job aspect {aspect or 'unset'})")
    else:
        a, b = (int(x) for x in aspect.split(':'))
        ok = abs(p['width'] / p['height'] - a / b) <= 0.01 * (a / b)
        add('T02', 'aspect', 'PASS' if ok else 'ISSUE', f"{p['width']}x{p['height']} vs job {aspect}")

    res = str(job.get('resolution', '')).lower()
    if res not in RES_SHORT_SIDE:
        add('T03', 'resolution', 'NA', f"short side {min(p['width'], p['height'])}px")
    else:
        short = min(p['width'], p['height'])
        add('T03', 'resolution', 'PASS' if short >= RES_SHORT_SIDE[res] * 0.98 else 'ISSUE',
            f"short side {short}px vs job {res} ({RES_SHORT_SIDE[res]}px)")

    want_audio = job.get('audio_expected')
    if want_audio is None:
        add('T04', 'audio', 'NA', 'audio stream present' if p['audio'] else 'no audio stream')
    elif want_audio and not p['audio']:
        add('T04', 'audio', 'ISSUE', 'job expects audio but the file has no audio stream')
    elif want_audio and any(a <= 0.1 and (b is None or b >= p['duration'] - 0.1) for a, b in silence):
        add('T04', 'audio', 'ISSUE', 'audio stream is silent for the whole clip')
    else:
        add('T04', 'audio', 'PASS' if want_audio else ('WARN' if p['audio'] else 'PASS'),
            'audio present' if p['audio'] else 'no audio (as expected)')

    inner = [(a, b) for a, b in black if a > 0.1 and b < p['duration'] - 0.1]
    edge = [x for x in black if x not in inner]
    st = 'ISSUE' if inner else ('WARN' if edge else 'PASS')
    add('T05', 'black frames', st, '; '.join(f'{a:.2f}-{b:.2f}s' for a, b in black) or 'none')

    add('T06', 'frozen frames ≥1 s (a hold can be intended)', 'WARN' if freeze else 'PASS',
        '; '.join(f"{a:.2f}-{'end' if b is None else round(b, 2)}s" for a, b in freeze) or 'none')

    n_exp, t_exp = expected_cuts(prompt)
    if n_exp is None:
        add('T07', 'cuts vs prompt', 'NA', f'{len(cuts)} cuts at {[round(c, 2) for c in cuts]}; prompt gives no count')
    elif n_exp != len(cuts):
        add('T07', 'cuts vs prompt', 'ISSUE', f'{len(cuts)} cuts at {[round(c, 2) for c in cuts]}, prompt asks {n_exp}')
    else:
        off = [round(abs(a - b), 2) for a, b in zip(cuts, t_exp)] if t_exp else []
        st = 'WARN' if any(o > 0.5 for o in off) else 'PASS'
        add('T07', 'cuts vs prompt', st, f'{len(cuts)} cuts at {[round(c, 2) for c in cuts]}'
            + (f'; offsets vs prompt {off}' if off else ''))

    issues = sum(c['status'] == 'ISSUE' for c in checks)
    warns = sum(c['status'] == 'WARN' for c in checks)
    return {'video': str(video), 'probe': p, 'checks': checks, 'cuts': cuts, 'black': black,
            'freeze': freeze, 'silence': silence, 'summary': {'issues': issues, 'warnings': warns},
            'note': 'Measurable checks only; identity, product truth, hands, text and acting need the frame review.'}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video', type=Path)
    ap.add_argument('--job', type=Path)
    ap.add_argument('--prompt', type=Path)
    ap.add_argument('--out', type=Path)
    a = ap.parse_args(argv)
    try:
        job = json.loads(a.job.read_text(encoding='utf-8')) if a.job else {}
        prompt = a.prompt.read_text(encoding='utf-8') if a.prompt else ''
        report = run_checks(a.video, job, prompt)
    except (OSError, ValueError, subprocess.CalledProcessError, StopIteration) as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if a.out:
        a.out.write_text(text, encoding='utf-8')
    for c in report['checks']:
        print(f"{c['status']:5} {c['id']} {c['title']}: {c['detail']}")
    print(f"{report['summary']['issues']} issues, {report['summary']['warnings']} warnings. "
          'Measurable checks only — run review_frames.py and inspect identity/product/hands/text next.')
    return 1 if report['summary']['issues'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
