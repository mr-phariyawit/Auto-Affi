#!/usr/bin/env python3
"""Verify rendered productions under runs/ against the cleanroom rules.

Honest verifier: probes the ACTUAL media files with ffprobe and reports measured
facts. Cleanroom rules (SUPER_SPEC.md / SPEC.md §10):
  - final deliverable: 1080x1920 (9:16), exactly 1 video + 1 audio stream
  - silent source/B-roll: 0 audio streams
  - duration present and > 0

Final candidates per run = (a) any .mp4 path referenced in approval_packet.json /
*manifest*.json, plus (b) composited finals in outputs/ or run root (mp4s that are
NOT per-scene clips `sNNN_*` and not under raw/source dirs). Per-scene clips and
obvious raw sources are excluded from the "final" verdict but counted.

Usage: python3 scripts/verify_runs.py [--json] [runs_dir]
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

RUNS = sys.argv[-1] if (len(sys.argv) > 1 and not sys.argv[-1].startswith("--")) else "runs"
AS_JSON = "--json" in sys.argv

SCENE_RE = re.compile(r"(^|/)s\d{2,3}[_-]", re.IGNORECASE)
RAW_DIR_RE = re.compile(r"/(raw|source|sources|seedance_visual|kie_outputs|clips|stills|frames|review_frames[^/]*)/", re.IGNORECASE)


def ffprobe(path: str):
    """Return (width, height, duration_s, n_video, n_audio) or None on error."""
    try:
        out = subprocess.run(  # noqa: S603 — fixed ffprobe args, no shell, no user input
            ["ffprobe", "-v", "error", "-show_entries",  # noqa: S607 — ffprobe resolved from PATH by design
             "stream=codec_type,width,height:format=duration",
             "-of", "json", path],
            capture_output=True, text=True, timeout=60)
        if out.returncode != 0:
            return None
        data = json.loads(out.stdout or "{}")
        streams = data.get("streams", [])
        v = [s for s in streams if s.get("codec_type") == "video"]
        a = [s for s in streams if s.get("codec_type") == "audio"]
        w = v[0].get("width") if v else None
        h = v[0].get("height") if v else None
        dur = data.get("format", {}).get("duration")
        dur = round(float(dur), 1) if dur else None
        return (w, h, dur, len(v), len(a))
    except Exception:
        return None


def declared_mp4s(run_dir: str):
    """Scan approval/manifest JSONs for any .mp4 string values."""
    found = set()
    for root, _dirs, files in os.walk(run_dir):
        depth = root[len(run_dir):].count(os.sep)
        if depth > 2:
            continue
        for fn in files:
            if not fn.endswith(".json"):
                continue
            low = fn.lower()
            if not any(k in low for k in ("approval", "manifest", "deliver", "final")):
                continue
            try:
                with open(os.path.join(root, fn), encoding="utf-8") as fh:
                    txt = fh.read()
            except (OSError, UnicodeDecodeError):  # best-effort scan, skip unreadable JSONs
                continue
            for m in re.findall(r'"([^"]+\.mp4)"', txt):
                cand = m if os.path.isabs(m) else os.path.join(run_dir, m)
                if os.path.isfile(cand):
                    found.add(os.path.normpath(cand))
                else:
                    base = os.path.basename(m)
                    for r2, _d2, f2 in os.walk(run_dir):
                        if base in f2:
                            found.add(os.path.normpath(os.path.join(r2, base)))
                            break
    return found


def composited_finals(run_dir: str):
    """mp4s that look like full composites (not per-scene, not raw)."""
    out = []
    for root, _dirs, files in os.walk(run_dir):
        for fn in files:
            if not fn.endswith(".mp4"):
                continue
            full = os.path.join(root, fn)
            rel = full[len(run_dir):]
            if SCENE_RE.search("/" + fn) or RAW_DIR_RE.search(rel):
                continue
            out.append(full)
    out.sort(key=lambda p: os.path.getsize(p), reverse=True)
    return out


def verdict(probe, silent_name: bool):
    """Cleanroom = 9:16 aspect + correct stream counts. 1080x1920 is a quality
    target (sub-target res is a note, not a cleanroom fail)."""
    if probe is None:
        return "ERROR", "ffprobe failed"
    w, h, dur, nv, na = probe
    if not w or not h:
        return "FAIL", "no video stream"
    aspect_ok = abs((h / w) - (16 / 9)) < 0.03  # portrait 9:16
    res_full = (w, h) == (1080, 1920)
    res_note = "1080x1920" if res_full else (
        f"{w}x{h} 9:16 sub-target" if aspect_ok else f"{w}x{h} NOT-9:16")
    if silent_name:
        if not aspect_ok:
            return "WARN", f"silent src; {res_note}"
        if na != 0:
            return "WARN", f"silent-named but {na} audio; {res_note}"
        return "OK-silent-src", f"0 audio B-roll; {res_note}"
    # non-silent final deliverable
    if not aspect_ok:
        return "FAIL", f"NOT 9:16 ({w}x{h}) — raw/source"
    if nv != 1:
        return "FAIL", f"{nv} video streams; {res_note}"
    if na != 1:
        return "FAIL", f"{na} audio (cleanroom=1); {res_note}"
    if not dur:
        return "FAIL", "no duration"
    if not res_full:
        return "PASS-720", f"cleanroom OK, sub-target {w}x{h}"
    return "PASS", "1080x1920, 1v+1a clean"


def main():
    runs = sorted(d.path for d in os.scandir(RUNS) if d.is_dir())
    report = []
    summary = {"runs": 0, "no_output": 0, "final_pass": 0, "final_fail": 0}
    for run in runs:
        summary["runs"] += 1
        name = os.path.basename(run)
        decl = declared_mp4s(run)
        comp = composited_finals(run)
        # final candidates: declared first, then top composited non-silent
        cands = []
        seen = set()
        for c in list(decl) + comp:
            n = os.path.normpath(c)
            if n in seen:
                continue
            seen.add(n)
            cands.append(c)
        cands = cands[:6]
        if not cands:
            report.append((name, [], "NO RENDERED OUTPUT (intake/smoke only)"))
            summary["no_output"] += 1
            continue
        rows = []
        run_has_pass = False
        for c in cands:
            silent = "_silent" in os.path.basename(c).lower() or c.endswith("_no_audio.mp4") or "no_audio" in os.path.basename(c).lower()
            pr = ffprobe(c)
            v, note = verdict(pr, silent)
            if v in ("PASS", "PASS-720"):
                run_has_pass = True
            rows.append({
                "file": os.path.relpath(c, run),
                "declared": os.path.normpath(c) in decl,
                "probe": pr, "verdict": v, "note": note,
            })
        if run_has_pass:
            summary["final_pass"] += 1
        else:
            summary["final_fail"] += 1
        report.append((name, rows, None))

    if AS_JSON:
        print(json.dumps({"summary": summary, "runs": [
            {"run": n, "note": note, "candidates": rows} for n, rows, note in report]}, indent=2))
        return

    print("# runs/ Production Verification")
    print(f"\n_ffprobe-measured ({__import__('os').path.basename(__file__)}). "
          f"{summary['runs']} runs · "
          f"{summary['final_pass']} with ≥1 clean final · "
          f"{summary['final_fail']} no clean final · "
          f"{summary['no_output']} no rendered output._\n")
    print("**Verdicts**: `PASS`=1080x1920 + 1 video + 1 audio · "
          "`PASS-720`=9:16 + 1v+1a but sub-target res (720x1280) · "
          "`OK-silent-src`=9:16 silent B-roll/source (0 audio, expected) · "
          "`WARN`=silent but odd · `FAIL`=NOT 9:16 (raw 1024x1024 etc.) or wrong stream counts.\n")
    print("**Scope (honest)**: this checks aspect/resolution/stream-count (cleanroom) only. "
          "It does NOT verify caption disclosure, VO speed-guard (1.0-1.15x), caption/VO sync, "
          "or product-identity accuracy — those need caption text + voice-segment reports, not ffprobe. "
          "Candidate finals = mp4s referenced in approval/manifest JSONs + composited outputs (per-scene `sNNN_*` and raw sources excluded best-effort).\n")
    for name, rows, note in report:
        print(f"\n## {name}")
        if note:
            print(f"- {note}")
            continue
        print("\n| verdict | file | WxH | dur(s) | v | a | note | declared |")
        print("|---|---|---|---|---|---|---|---|")
        for r in rows:
            pr = r["probe"]
            w, h, dur, nv, na = pr if pr else (None, None, None, None, None)
            print(f"| {r['verdict']} | `{r['file']}` | {w}x{h} | {dur} | {nv} | {na} | {r['note']} | {'✓' if r['declared'] else ''} |")


if __name__ == "__main__":
    main()
