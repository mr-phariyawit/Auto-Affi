#!/usr/bin/env python
"""Compare two final mp4s to catch silent regressions.

Motivation: the v5 final lost SFX because the script composited overlays
on the WRONG base (final-v3-clean.mp4, pre-SFX). The diff was invisible
to the eye — only the spectrum revealed missing audio energy in the
SFX band. This tool surfaces that kind of regression in one command.

Compares:
  * Duration (warn if delta > 0.5s)
  * Total audio RMS (warn if drop > 6 dB → likely missing audio layer)
  * Per-second audio RMS profile (visualize where the loss happened)
  * Video frame count (warn if delta > 1 frame)

Usage:
    .venv/bin/python scripts/compare-finals.py \\
        --baseline out/maono-concept-2-final-v4.mp4 \\
        --candidate out/maono-concept-2-final-v6.mp4
"""

from __future__ import annotations

import argparse
import math
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MediaProfile:
    path: Path
    duration_s: float
    frame_count: int
    audio_rms_db: float
    rms_per_second: list[float]


def _ffprobe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def _ffprobe_frame_count(path: Path) -> int:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-count_frames", "-show_entries", "stream=nb_read_frames",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return int(r.stdout.strip())


def _audio_rms_total_db(path: Path) -> float:
    """Mean volume across the whole file (dBFS, negative = quieter)."""
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path),
         "-af", "volumedetect", "-vn", "-sn", "-dn",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    # ffmpeg writes volumedetect stats to stderr
    for line in r.stderr.splitlines():
        if "mean_volume:" in line:
            try:
                return float(line.split("mean_volume:")[1].strip().split()[0])
            except (IndexError, ValueError):
                pass
    return float("-inf")


def _audio_rms_per_second(path: Path, duration_s: float) -> list[float]:
    """Coarse per-second RMS profile via ffmpeg astats."""
    n_buckets = max(1, math.ceil(duration_s))
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path),
         "-af", "asetnsamples=44100,astats=metadata=1:reset=1,"
                "ametadata=print:key=lavfi.astats.Overall.RMS_level",
         "-vn", "-sn", "-dn", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    values: list[float] = []
    for line in r.stderr.splitlines():
        if "Overall.RMS_level=" in line:
            try:
                values.append(float(line.split("=")[-1]))
            except ValueError:
                pass
    if not values:
        return [float("-inf")] * n_buckets
    # Bucket values into per-second slots
    per_sec = max(1, len(values) // n_buckets)
    bucketed = [values[i:i + per_sec] for i in range(0, len(values), per_sec)]
    return [sum(b) / len(b) for b in bucketed if b]


def profile(path: Path) -> MediaProfile:
    duration_s = _ffprobe_duration(path)
    return MediaProfile(
        path=path,
        duration_s=duration_s,
        frame_count=_ffprobe_frame_count(path),
        audio_rms_db=_audio_rms_total_db(path),
        rms_per_second=_audio_rms_per_second(path, duration_s),
    )


def _ascii_bar(value: float, *, vmin: float = -60.0, vmax: float = 0.0, width: int = 30) -> str:
    if not math.isfinite(value):
        return " " * width + "  -inf"
    clamped = max(vmin, min(vmax, value))
    fill = int(round((clamped - vmin) / (vmax - vmin) * width))
    return "█" * fill + "·" * (width - fill) + f"  {value:6.1f} dB"


def compare(a: MediaProfile, b: MediaProfile) -> int:
    """Return 0 if no regression, 1 if warnings, 2 if hard regression."""
    print(f"\n📐 {a.path.name}  vs  {b.path.name}")
    print(f"{'─' * 60}")
    print(f"  duration:   {a.duration_s:7.3f}s  →  {b.duration_s:7.3f}s   (Δ {b.duration_s - a.duration_s:+.3f}s)")
    print(f"  frames:     {a.frame_count:7d}   →  {b.frame_count:7d}    (Δ {b.frame_count - a.frame_count:+d})")
    print(f"  audio RMS:  {a.audio_rms_db:7.2f}dB→ {b.audio_rms_db:7.2f}dB  (Δ {b.audio_rms_db - a.audio_rms_db:+.2f} dB)")

    exit_code = 0
    if abs(b.duration_s - a.duration_s) > 0.5:
        print(f"  ⚠️  duration delta > 0.5s")
        exit_code = max(exit_code, 1)
    if abs(b.frame_count - a.frame_count) > 1:
        print(f"  ⚠️  frame-count delta > 1")
        exit_code = max(exit_code, 1)
    rms_drop = a.audio_rms_db - b.audio_rms_db
    if rms_drop > 6.0:
        print(f"  ❌ audio RMS dropped {rms_drop:.1f} dB — likely missing audio layer (SFX? music? VO?)")
        exit_code = max(exit_code, 2)
    elif rms_drop > 3.0:
        print(f"  ⚠️  audio RMS dropped {rms_drop:.1f} dB — investigate")
        exit_code = max(exit_code, 1)

    # Per-second RMS profile side-by-side — spot where the loss occurred
    print(f"\n  per-second audio RMS (left=baseline, right=candidate):")
    n = max(len(a.rms_per_second), len(b.rms_per_second))
    for i in range(n):
        av = a.rms_per_second[i] if i < len(a.rms_per_second) else float("-inf")
        bv = b.rms_per_second[i] if i < len(b.rms_per_second) else float("-inf")
        diff = bv - av if math.isfinite(av) and math.isfinite(bv) else float("nan")
        flag = "  ⚠️" if math.isfinite(diff) and diff < -6.0 else ""
        print(f"    t={i:2d}s  {_ascii_bar(av, width=20)}   {_ascii_bar(bv, width=20)}{flag}")

    if exit_code == 0:
        print(f"\n✅ no regression — final v{b.path.stem} matches baseline shape")
    elif exit_code == 1:
        print(f"\n⚠️  warnings present — review the spec deltas above")
    else:
        print(f"\n❌ HARD REGRESSION — do not ship this final without explanation")
    return exit_code


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--baseline", type=Path, required=True,
                   help="The known-good final mp4 to compare against.")
    p.add_argument("--candidate", type=Path, required=True,
                   help="The new final mp4 under review.")
    args = p.parse_args()

    for path in (args.baseline, args.candidate):
        if not path.exists():
            print(f"ERROR: {path} not found", file=sys.stderr)
            return 3

    a = profile(args.baseline)
    b = profile(args.candidate)
    return compare(a, b)


if __name__ == "__main__":
    sys.exit(main())
