"""Cleanroom verification gate — ffprobe-backed stream analysis.

Verifies that a final master mp4 satisfies the production-review principle:

  - exactly 1 video stream
  - exactly 1 audio stream  (final has VO muxed in)
  - each source clip has 0 audio streams (raw/visual B-roll is silent)
  - duration within ``tolerance_s`` of ``profile_s`` (if given) and ≤ 60s
  - resolution is 1080x1920 (9:16)

See docs/principles/2026-06-03-production-review-principle.md §Cleanroom
Verification Gate for the full policy.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, cast

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Report model
# ---------------------------------------------------------------------------


class CleanroomReport(BaseModel):
    """Result of :func:`verify_master`."""

    ok: bool
    video_streams: int
    audio_streams: int
    duration_s: float
    width: int = 0
    height: int = 0
    violations: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _require_ffprobe() -> str:
    binary = shutil.which("ffprobe")
    if binary is None:
        raise RuntimeError(
            "ffprobe is not installed or not on PATH. "
            "Install ffmpeg (which includes ffprobe) and retry."
        )
    return binary


def _probe_streams(path: Path) -> list[dict[str, Any]]:
    """Run ffprobe on *path* and return the list of stream dicts."""
    ffprobe = _require_ffprobe()
    cmd = [
        ffprobe,
        "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        str(path),
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)  # noqa: S603 -- cmd is [ffprobe, fixed flags, path]; no user input
    data: dict[str, Any] = json.loads(result.stdout)
    return cast(list[dict[str, Any]], data.get("streams", []))


def _count_streams(streams: list[dict[str, Any]], codec_type: str) -> int:
    return sum(1 for s in streams if s.get("codec_type") == codec_type)


def _get_duration(streams: list[dict[str, Any]]) -> float:
    """Best-effort duration from the first video or audio stream."""
    for s in streams:
        raw = s.get("duration")
        if raw is not None:
            try:
                return float(raw)
            except (TypeError, ValueError):
                pass
    return 0.0


def _get_dimensions(streams: list[dict[str, Any]]) -> tuple[int, int]:
    """Return (width, height) from the first video stream, or (0, 0)."""
    for s in streams:
        if s.get("codec_type") == "video":
            w = s.get("width", 0)
            h = s.get("height", 0)
            return int(w), int(h)
    return 0, 0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def verify_master(
    master_path: Path,
    *,
    source_clips: list[Path] | None = None,
    profile_s: float | None = None,
    tolerance_s: float = 2.0,
) -> CleanroomReport:
    """Verify *master_path* satisfies the cleanroom contract.

    Parameters
    ----------
    master_path
        Path to the final assembled mp4.
    source_clips
        If provided, each clip is probed and must have 0 audio streams.
    profile_s
        Expected total duration in seconds. If given, master duration must
        be within ``± tolerance_s``.
    tolerance_s
        Allowed duration deviation from ``profile_s``. Default 2.0s.

    Returns
    -------
    CleanroomReport
        ``ok=True`` only when all invariants hold.
    """
    violations: list[str] = []

    # Probe the master
    master_streams = _probe_streams(master_path)
    n_video = _count_streams(master_streams, "video")
    n_audio = _count_streams(master_streams, "audio")
    duration = _get_duration(master_streams)
    width, height = _get_dimensions(master_streams)

    # --- stream count checks ---
    if n_video != 1:
        violations.append(
            f"final must have exactly 1 video stream; found {n_video}"
        )
    if n_audio != 1:
        violations.append(
            f"final must have exactly 1 audio stream; found {n_audio}"
        )

    # --- resolution check ---
    if n_video >= 1 and (width != 1080 or height != 1920):
        violations.append(
            f"resolution must be 1080x1920 (9:16); found {width}x{height}"
        )

    # --- duration checks ---
    if duration > 60.0:
        violations.append(
            f"duration {duration:.2f}s exceeds 60s cap"
        )
    if profile_s is not None and abs(duration - profile_s) > tolerance_s:
        violations.append(
            f"duration {duration:.2f}s deviates from profile "
            f"{profile_s:.2f}s by more than {tolerance_s:.2f}s"
        )

    # --- source clip audio checks ---
    if source_clips:
        for clip_path in source_clips:
            clip_streams = _probe_streams(clip_path)
            clip_audio = _count_streams(clip_streams, "audio")
            if clip_audio != 0:
                violations.append(
                    f"source clip {clip_path.name} must have 0 audio streams; "
                    f"found {clip_audio}"
                )

    return CleanroomReport(
        ok=len(violations) == 0,
        video_streams=n_video,
        audio_streams=n_audio,
        duration_s=duration,
        width=width,
        height=height,
        violations=violations,
    )
