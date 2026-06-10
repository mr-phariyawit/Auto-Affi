"""Offline render pipeline using ffmpeg lavfi — zero paid/network calls.

Produces real mp4 files entirely from synthetic sources:
- render_shot: writes a silent 9:16 1080x1920 H.264 clip of the requested
  duration using the ``color`` lavfi source.
- assemble_master: concatenates shot clips and muxes in exactly one silent
  AAC audio track (anullsrc), producing a final 9:16 <=60s mp4 with
  exactly 1 video stream + 1 audio stream.

This satisfies the cleanroom contract: individual clips carry no audio;
the master has one silent audio track that real VO replaces in Phase 2.

Cost: 0.0 USD (no paid API calls).
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

# Canonical resolution for 9:16 short-form video
_WIDTH = 1080
_HEIGHT = 1920
_PIXEL_FORMAT = "yuv420p"
_VIDEO_CODEC = "libx264"
_AUDIO_CODEC = "aac"
_CRF = "28"
_PRESET = "ultrafast"


def _require_ffmpeg() -> str:
    """Return the path to ffmpeg, or raise RuntimeError if missing."""
    binary = shutil.which("ffmpeg")
    if binary is None:
        raise RuntimeError(
            "ffmpeg is not installed or not on PATH. "
            "Install ffmpeg (e.g. `brew install ffmpeg`) and retry."
        )
    return binary


def _require_ffprobe() -> str:
    """Return the path to ffprobe, or raise RuntimeError if missing."""
    binary = shutil.which("ffprobe")
    if binary is None:
        raise RuntimeError(
            "ffprobe is not installed or not on PATH. "
            "Install ffmpeg (which includes ffprobe) and retry."
        )
    return binary


def render_shot(shot: object, dest: Path) -> Path:
    """Render a single shot to a silent 9:16 1080x1920 H.264 mp4.

    Uses the ffmpeg ``color`` lavfi source to produce a solid-colour clip
    with no audio (``-an``). The colour cycles through a small palette based
    on the shot index in dest's stem so successive shots are visually distinct
    during debugging.

    Args:
        shot: An object with a ``duration_s: float`` attribute (AiShot or
              similar). Only ``shot.duration_s`` is read.
        dest: Destination path for the mp4 file. Parent dir must exist or
              will be created.

    Returns:
        ``dest`` (the written file path).

    Raises:
        RuntimeError: if ffmpeg is not installed.
        subprocess.CalledProcessError: if ffmpeg exits non-zero.
    """
    ffmpeg = _require_ffmpeg()
    duration_s: float = float(getattr(shot, "duration_s", 5.0))

    # Pick a colour from a small palette to distinguish shots visually
    _colours = ["0x1a1a2e", "0x16213e", "0x0f3460", "0x533483", "0xe94560"]
    stem_digit = sum(ord(c) for c in dest.stem) % len(_colours)
    colour = _colours[stem_digit]

    dest.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        ffmpeg,
        "-y",  # overwrite output without asking
        "-f", "lavfi",
        "-i", f"color=c={colour}:s={_WIDTH}x{_HEIGHT}:r=30:d={duration_s:.6f}",
        "-an",  # NO audio — cleanroom contract
        "-vcodec", _VIDEO_CODEC,
        "-crf", _CRF,
        "-preset", _PRESET,
        "-pix_fmt", _PIXEL_FORMAT,
        str(dest),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return dest


def assemble_master(clips: list[Path], dest: Path) -> Path:
    """Concatenate silent shot clips and mux in exactly one silent audio track.

    Steps:
    1. Writes a concat-list text file.
    2. Runs ffmpeg concat demuxer to join the video streams.
    3. Muxes in a single anullsrc AAC audio track so the final mp4 has
       exactly 1 video stream + 1 audio stream.

    The output is a 9:16 mp4 <=60s total duration.

    Args:
        clips: Ordered list of silent mp4 clips produced by :func:`render_shot`.
        dest:  Destination path for the master mp4.

    Returns:
        ``dest`` (the written file path).

    Raises:
        ValueError: if ``clips`` is empty.
        RuntimeError: if ffmpeg is not installed.
        subprocess.CalledProcessError: if ffmpeg exits non-zero.
    """
    if not clips:
        raise ValueError("assemble_master requires at least one clip")

    ffmpeg = _require_ffmpeg()
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Step 1: concat the silent video clips into an intermediate file
    with tempfile.TemporaryDirectory() as tmpdir:
        concat_list = Path(tmpdir) / "concat.txt"
        lines = [f"file '{clip.resolve()}'\n" for clip in clips]
        concat_list.write_text("".join(lines), encoding="utf-8")

        intermediate = Path(tmpdir) / "video_only.mp4"

        concat_cmd = [
            ffmpeg,
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",  # no re-encode; clips are already h264
            str(intermediate),
        ]
        subprocess.run(concat_cmd, check=True, capture_output=True)

        # Step 2: mux in exactly one silent audio track (anullsrc -> aac)
        # -shortest stops encoding when the video ends (anullsrc is infinite)
        mux_cmd = [
            ffmpeg,
            "-y",
            "-i", str(intermediate),       # video-only concat
            "-f", "lavfi",
            "-i", "anullsrc=r=44100:cl=stereo",  # silent audio source
            "-c:v", "copy",                # keep video as-is
            "-c:a", _AUDIO_CODEC,          # encode silent audio as aac
            "-b:a", "64k",
            "-shortest",                   # stop when video ends
            "-map", "0:v:0",               # exactly 1 video stream
            "-map", "1:a:0",               # exactly 1 audio stream
            str(dest),
        ]
        subprocess.run(mux_cmd, check=True, capture_output=True)

    return dest
