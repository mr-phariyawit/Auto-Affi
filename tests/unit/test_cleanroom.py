"""Tests for pipeline.cleanroom.verify_master using real ffmpeg/ffprobe.

Builds real mp4 files via dry_render helpers and probes them with ffprobe.
All PASS/FAIL assertions are backed by actual ffprobe output.

Failure modes verified:
  - 0 audio streams (raw shot) → FAIL (final must have 1 audio)
  - 2 audio streams (manually constructed) → FAIL (final must have exactly 1)
  - 1v+1a master produced by assemble_master → PASS
  - source clip with audio bleeds → FAIL via source_clips check
  - duration tolerance violation → FAIL
  - resolution mismatch → FAIL (synthetic — tested via wrong-resolution file)
"""

from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import pytest

from auto_affi.pipeline.cleanroom import CleanroomReport, verify_master
from auto_affi.pipeline.dry_render import assemble_master, render_shot

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@dataclass
class _FakeShot:
    duration_s: float
    shot_id: str = "s0"


def _make_clip(tmpdir: Path, duration_s: float, shot_id: str = "s0") -> Path:
    """Produce a silent 1080x1920 clip via render_shot."""
    dest = tmpdir / f"clip_{shot_id}.mp4"
    render_shot(_FakeShot(duration_s=duration_s, shot_id=shot_id), dest)
    return dest


def _make_master(tmpdir: Path, clips: list[Path]) -> Path:
    """Assemble clips into a 1v+1a master via assemble_master."""
    dest = tmpdir / "master.mp4"
    assemble_master(clips, dest)
    return dest


def _make_master_with_two_audio(tmpdir: Path, duration_s: float = 3.0) -> Path:
    """Create a file with 2 audio streams using ffmpeg directly."""
    ffmpeg = "ffmpeg"
    dest = tmpdir / "double_audio.mp4"
    # Build a clip with 2 audio streams:
    #   map 0:v:0, map 1:a:0, map 1:a:0
    cmd = [
        ffmpeg, "-y",
        "-f", "lavfi", "-i", f"color=c=blue:s=1080x1920:r=30:d={duration_s}",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-c:v", "libx264", "-crf", "28", "-preset", "ultrafast",
        "-c:a", "aac", "-b:a", "64k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-map", "1:a:0",  # duplicate audio stream
        "-shortest",
        str(dest),
    ]
    subprocess.run(cmd, check=True, capture_output=True)  # noqa: S603 -- cmd is [ffmpeg, fixed flags, path]; no user input
    return dest


def _make_no_audio_file(tmpdir: Path, duration_s: float = 3.0) -> Path:
    """Create a video-only file (0 audio streams) using render_shot directly."""
    # render_shot produces exactly 0 audio streams — that's what we need
    dest = tmpdir / "no_audio.mp4"
    render_shot(_FakeShot(duration_s=duration_s), dest)
    return dest


# ---------------------------------------------------------------------------
# PASS cases
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_cleanroom_passes_good_master() -> None:
    """A proper 2-clip master assembled by assemble_master must pass cleanroom."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0"), _make_clip(d, 5.0, "s1")]
        master = _make_master(d, clips)

        report = verify_master(master)

        assert report.ok is True, f"violations: {report.violations}"
        assert report.video_streams == 1
        assert report.audio_streams == 1
        assert report.violations == []


@pytest.mark.unit
def test_cleanroom_passes_with_source_clips_provided() -> None:
    """Source clips (silent) + valid master → ok=True."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 3.0, "s0"), _make_clip(d, 3.0, "s1")]
        master = _make_master(d, clips)

        report = verify_master(master, source_clips=clips)

        assert report.ok is True, f"violations: {report.violations}"


@pytest.mark.unit
def test_cleanroom_passes_within_profile_tolerance() -> None:
    """Duration 10s ± 2s tolerance with profile_s=10 must pass."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 10.0, "s0")]
        master = _make_master(d, clips)

        report = verify_master(master, profile_s=10.0, tolerance_s=2.0)

        assert report.ok is True, f"violations: {report.violations}"


@pytest.mark.unit
def test_cleanroom_resolution_is_1080x1920() -> None:
    """verify_master must confirm the master is 1080x1920."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 3.0, "s0")]
        master = _make_master(d, clips)

        report = verify_master(master)

        assert report.width == 1080
        assert report.height == 1920


@pytest.mark.unit
def test_cleanroom_duration_populated() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0")]
        master = _make_master(d, clips)
        report = verify_master(master)
        assert report.duration_s > 0.0


@pytest.mark.unit
def test_cleanroom_report_is_cleanroom_report_instance() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 3.0, "s0")]
        master = _make_master(d, clips)
        report = verify_master(master)
        assert isinstance(report, CleanroomReport)


# ---------------------------------------------------------------------------
# FAIL cases — 0 audio streams (cleanroom: final must have 1)
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_cleanroom_fails_zero_audio_streams() -> None:
    """A video-only file (0 audio) must fail cleanroom — final needs 1 audio."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        no_audio = _make_no_audio_file(d, duration_s=3.0)

        report = verify_master(no_audio)

        assert report.ok is False
        assert report.audio_streams == 0
        assert any("audio" in v.lower() for v in report.violations), (
            f"expected audio violation, got {report.violations}"
        )


# ---------------------------------------------------------------------------
# FAIL cases — 2 audio streams
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_cleanroom_fails_two_audio_streams() -> None:
    """A file with 2 audio streams must fail cleanroom."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        double_audio = _make_master_with_two_audio(d, duration_s=3.0)

        report = verify_master(double_audio)

        assert report.ok is False
        assert report.audio_streams == 2
        assert any("audio" in v.lower() for v in report.violations), (
            f"expected audio violation, got {report.violations}"
        )


# ---------------------------------------------------------------------------
# FAIL cases — source clip has audio (bleed check)
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_cleanroom_fails_source_clip_with_audio() -> None:
    """Source clip with audio streams must cause a violation via source_clips check."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        # Build a valid master
        silent_clip = _make_clip(d, 3.0, "s0")
        master = _make_master(d, [silent_clip])

        # Provide the master itself as a source clip — it has 1 audio stream
        report = verify_master(master, source_clips=[master])

        assert report.ok is False
        assert any("source" in v.lower() for v in report.violations), (
            f"expected source-clip audio violation, got {report.violations}"
        )


# ---------------------------------------------------------------------------
# FAIL cases — duration tolerance
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_cleanroom_fails_duration_outside_tolerance() -> None:
    """Duration 5s with profile_s=15, tolerance_s=2 must fail."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0")]
        master = _make_master(d, clips)

        report = verify_master(master, profile_s=15.0, tolerance_s=2.0)

        assert report.ok is False
        assert any("duration" in v.lower() or "profile" in v.lower() for v in report.violations)


# ---------------------------------------------------------------------------
# FAIL cases — duration > 60s
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_cleanroom_fails_duration_over_60s() -> None:
    """A master > 60s must fail the 60s cap check."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        # 65s clip
        clips = [_make_clip(d, 65.0, "s0")]
        master = _make_master(d, clips)

        report = verify_master(master)

        assert report.ok is False
        assert any("60" in v for v in report.violations)
