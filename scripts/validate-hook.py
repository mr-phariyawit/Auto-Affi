#!/usr/bin/env python
"""Validate the first 1 second of a video against pattern-interrupt criteria.

Implements the HSO×VCS Method's "Hook in ≤1s" principle. Per TTSVibes 2025
data, 71% of viewers decide stay/leave in the first 3 seconds; videos that
maintain ≥70% intro retention get 2.2× more views. A "pattern-interrupt"
hook is what unlocks that retention floor.

Three measurable criteria a hook can satisfy (ANY ONE = pass):

  1. MOTION  — pixel-diff between t=0 and t=1.0s > threshold
     (something visually changes between first and last frame of the hook
     window). Catches motion-based hooks: zoom-in, push, reveal.

  2. AUDIO ONSET — RMS energy at t≈0 is substantively different
     (≥ 6 dB delta either direction) from steady-state. Catches sound-
     design-driven hooks: silence-then-bang, music drop, voice entry.

  3. TEXT OVERLAY — bright pixel density in lower or upper-third bands
     differs from frame interior, signaling on-screen text. Catches
     caption-driven hooks: "หยุดเลื่อน!" at frame 0.

Reports each check independently with concrete metrics, then returns a
single verdict: PASS (any criterion satisfied) / WARN (close but no
criterion clean) / FAIL (no signal at all).

Usage:
    .venv/bin/python scripts/validate-hook.py \\
        --video out/maono-concept-2-final-v7.mp4
"""

from __future__ import annotations

import argparse
import math
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


HOOK_WINDOW_S = 1.0
MOTION_THRESHOLD = 0.04         # mean pixel-diff (0-1 normalized)
AUDIO_DELTA_DB_THRESHOLD = 6.0  # dB
TEXT_BAND_BRIGHTNESS_DELTA = 18.0  # 0-255 luminance scale


@dataclass(frozen=True)
class HookCheck:
    name: str
    metric_label: str
    metric_value: float
    threshold: float
    passed: bool
    detail: str


def _extract_frame(video: Path, t_s: float, out: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t_s:.3f}",
         "-i", str(video), "-frames:v", "1", str(out)],
        check=True,
    )


def _ffprobe_duration(video: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def check_motion(video: Path, tmpdir: Path) -> HookCheck:
    """Pixel-diff between t=0 and t=HOOK_WINDOW_S (normalized 0-1)."""
    f0 = tmpdir / "hook_t0.png"
    f1 = tmpdir / "hook_t1.png"
    _extract_frame(video, 0.0, f0)
    _extract_frame(video, HOOK_WINDOW_S - 0.05, f1)
    im0 = Image.open(f0).convert("L").resize((128, 128))
    im1 = Image.open(f1).convert("L").resize((128, 128))
    b0 = im0.tobytes()
    b1 = im1.tobytes()
    delta = sum(abs(a - b) for a, b in zip(b0, b1)) / (len(b0) * 255)
    return HookCheck(
        name="MOTION",
        metric_label="mean pixel-diff (t=0 vs t=1s)",
        metric_value=delta,
        threshold=MOTION_THRESHOLD,
        passed=delta > MOTION_THRESHOLD,
        detail=f"motion ratio: {delta:.4f} (need > {MOTION_THRESHOLD})",
    )


def _audio_rms_window(video: Path, start_s: float, duration_s: float) -> float:
    """Mean volume (dBFS) within a window via ffmpeg volumedetect."""
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-ss", f"{start_s:.3f}",
         "-t", f"{duration_s:.3f}", "-i", str(video),
         "-af", "volumedetect", "-vn", "-sn", "-dn", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    for line in r.stderr.splitlines():
        if "mean_volume:" in line:
            try:
                return float(line.split("mean_volume:")[1].strip().split()[0])
            except (IndexError, ValueError):
                pass
    return float("-inf")


def check_audio_onset(video: Path) -> HookCheck:
    """Compare audio RMS at hook vs steady-state — looking for either
    silence-then-bang OR loud-then-quiet (any sharp delta = signal)."""
    hook_rms = _audio_rms_window(video, 0.0, HOOK_WINDOW_S)
    # Steady-state sample: 2s window starting at 4s (well past hook)
    steady_rms = _audio_rms_window(video, 4.0, 2.0)
    if not (math.isfinite(hook_rms) and math.isfinite(steady_rms)):
        return HookCheck(
            name="AUDIO_ONSET",
            metric_label="hook vs steady-state RMS",
            metric_value=float("nan"),
            threshold=AUDIO_DELTA_DB_THRESHOLD,
            passed=False,
            detail=f"could not measure (hook={hook_rms} steady={steady_rms})",
        )
    delta = abs(hook_rms - steady_rms)
    return HookCheck(
        name="AUDIO_ONSET",
        metric_label="|hook RMS − steady RMS|",
        metric_value=delta,
        threshold=AUDIO_DELTA_DB_THRESHOLD,
        passed=delta > AUDIO_DELTA_DB_THRESHOLD,
        detail=f"hook={hook_rms:.1f} dB · steady={steady_rms:.1f} dB · Δ={delta:.1f} dB "
               f"(need > {AUDIO_DELTA_DB_THRESHOLD} dB)",
    )


def check_text_overlay(video: Path, tmpdir: Path) -> HookCheck:
    """Detect bright-on-dark caption boxes in the upper or lower third
    of the hook frame (a proxy for on-screen text)."""
    f0 = tmpdir / "hook_t0.png"  # may already exist from check_motion
    if not f0.exists():
        _extract_frame(video, 0.0, f0)
    im = Image.open(f0).convert("L")
    w, h = im.size
    third = h // 3
    upper = im.crop((0, 0, w, third))
    middle = im.crop((0, third, w, 2 * third))
    lower = im.crop((0, 2 * third, w, h))

    def mean(img):
        b = img.tobytes()
        return sum(b) / len(b) if b else 0

    u, m, l = mean(upper), mean(middle), mean(lower)
    # Look for either band brighter than middle (light text on dark vid)
    # OR substantially darker (dark text box on bright vid).
    upper_delta = abs(u - m)
    lower_delta = abs(l - m)
    max_delta = max(upper_delta, lower_delta)
    detail_band = "upper" if upper_delta >= lower_delta else "lower"
    return HookCheck(
        name="TEXT_OVERLAY",
        metric_label=f"|{detail_band}-third − middle| luminance",
        metric_value=max_delta,
        threshold=TEXT_BAND_BRIGHTNESS_DELTA,
        passed=max_delta > TEXT_BAND_BRIGHTNESS_DELTA,
        detail=f"upper={u:.1f} mid={m:.1f} lower={l:.1f} · max Δ={max_delta:.1f} "
               f"(need > {TEXT_BAND_BRIGHTNESS_DELTA})",
    )


def validate(video: Path) -> int:
    duration = _ffprobe_duration(video)
    if duration < HOOK_WINDOW_S:
        print(f"❌ video too short ({duration:.2f}s < {HOOK_WINDOW_S}s)")
        return 2

    tmpdir = video.parent / f".hook-validate-{video.stem}"
    tmpdir.mkdir(parents=True, exist_ok=True)

    checks = [
        check_motion(video, tmpdir),
        check_audio_onset(video),
        check_text_overlay(video, tmpdir),
    ]

    print(f"\n🎯 Hook validation: {video.name}")
    print(f"   Total duration: {duration:.2f}s · Hook window: 0.0-{HOOK_WINDOW_S}s\n")
    print(f"   {'CHECK':<14} {'STATUS':<8} {'DETAIL'}")
    print(f"   {'─' * 14} {'─' * 8} {'─' * 60}")
    for c in checks:
        symbol = "✅" if c.passed else "❌"
        print(f"   {c.name:<14} {symbol:<8} {c.detail}")

    n_passed = sum(1 for c in checks if c.passed)
    print()
    if n_passed >= 1:
        print(f"✅ PASS — hook satisfies {n_passed}/3 criteria. "
              f"Algorithmic distribution likely.")
        return 0
    # Soft-pass: any check within 50% of threshold = WARN
    softs = sum(
        1 for c in checks
        if not c.passed and math.isfinite(c.metric_value) and
        c.metric_value > c.threshold * 0.5
    )
    if softs > 0:
        print(f"⚠️  WARN — {softs}/3 criteria within 50% of threshold but no clean pass.")
        print(f"    Recommend: add a stronger pattern interrupt at t=0 "
              f"(motion / SFX / on-screen text).")
        return 1
    print(f"❌ FAIL — no pattern-interrupt signal detected in hook window.")
    print(f"    First 1s likely loses 30%+ of viewers per TTSVibes 2025 data.")
    print(f"    Recommend: rebuild hook with one of:")
    print(f"      • snap zoom / whip pan / hard cut at t=0")
    print(f"      • sub-bass hit or sudden silence at t=0")
    print(f"      • caption flash at t=0 (e.g. 'หยุดเลื่อน!')")
    return 2


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--video", type=Path, required=True)
    args = p.parse_args()
    if not args.video.exists():
        print(f"ERROR: {args.video} not found", file=sys.stderr)
        return 3
    return validate(args.video)


if __name__ == "__main__":
    sys.exit(main())
