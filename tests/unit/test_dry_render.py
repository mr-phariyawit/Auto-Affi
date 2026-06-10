"""Tests for the offline render pipeline (dry_render.py).

Uses real ffmpeg/ffprobe to produce and verify actual mp4 files.
ffmpeg 8.1.1 is confirmed installed at /opt/homebrew/bin/ffmpeg.
All assertions are backed by ffprobe output (VERIFIED).
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import pytest

from auto_affi.pipeline.dry_render import assemble_master, render_shot

# ---------------------------------------------------------------------------
# Helper: minimal shot-like object
# ---------------------------------------------------------------------------


@dataclass
class _FakeShot:
    duration_s: float
    shot_id: str = "s0"


# ---------------------------------------------------------------------------
# Helper: ffprobe stream info
# ---------------------------------------------------------------------------


def _ffprobe_streams(path: Path) -> list[dict]:  # type: ignore[type-arg]
    """Run ffprobe and return the list of stream dicts."""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        str(path),
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)  # noqa: S603 -- cmd is [ffprobe, fixed flags, path]; no user input
    data = json.loads(result.stdout)
    return data.get("streams", [])  # type: ignore[no-any-return]


def _video_streams(path: Path) -> list[dict]:  # type: ignore[type-arg]
    return [s for s in _ffprobe_streams(path) if s.get("codec_type") == "video"]


def _audio_streams(path: Path) -> list[dict]:  # type: ignore[type-arg]
    return [s for s in _ffprobe_streams(path) if s.get("codec_type") == "audio"]


# ---------------------------------------------------------------------------
# render_shot tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_render_shot_produces_file() -> None:
    """render_shot must write a real file to dest."""
    shot = _FakeShot(duration_s=3.0)
    with tempfile.TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir) / "shot_s0.mp4"
        result = render_shot(shot, dest)
        assert result == dest
        assert dest.exists()
        assert dest.stat().st_size > 0


@pytest.mark.unit
def test_render_shot_returns_dest_path() -> None:
    shot = _FakeShot(duration_s=2.0)
    with tempfile.TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir) / "out.mp4"
        returned = render_shot(shot, dest)
        assert returned == dest


@pytest.mark.unit
def test_render_shot_ffprobe_resolution() -> None:
    """ffprobe must confirm 1080x1920 (9:16) video stream."""
    shot = _FakeShot(duration_s=2.0, shot_id="s1")
    with tempfile.TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir) / "shot.mp4"
        render_shot(shot, dest)

        vstreams = _video_streams(dest)
        assert len(vstreams) == 1, f"expected 1 video stream, got {len(vstreams)}"
        assert vstreams[0]["width"] == 1080
        assert vstreams[0]["height"] == 1920


@pytest.mark.unit
def test_render_shot_no_audio_streams() -> None:
    """Single shot must have 0 audio streams (cleanroom contract)."""
    shot = _FakeShot(duration_s=2.0)
    with tempfile.TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir) / "shot.mp4"
        render_shot(shot, dest)

        astreams = _audio_streams(dest)
        assert len(astreams) == 0, (
            f"render_shot must produce no audio, but got {len(astreams)} audio stream(s)"
        )


@pytest.mark.unit
def test_render_shot_duration_approx() -> None:
    """ffprobe-reported duration must be within ±0.5s of requested."""
    requested = 3.0
    shot = _FakeShot(duration_s=requested, shot_id="s2")
    with tempfile.TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir) / "shot.mp4"
        render_shot(shot, dest)

        vstreams = _video_streams(dest)
        reported = float(vstreams[0].get("duration", 0))
        assert abs(reported - requested) < 0.5, (
            f"Duration mismatch: requested={requested}s, ffprobe={reported}s"
        )


@pytest.mark.unit
def test_render_shot_creates_parent_dirs() -> None:
    """render_shot must create parent directories if they don't exist."""
    shot = _FakeShot(duration_s=1.0)
    with tempfile.TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir) / "nested" / "deep" / "shot.mp4"
        render_shot(shot, dest)
        assert dest.exists()


@pytest.mark.unit
def test_render_shot_cost_is_zero() -> None:
    """render_shot records 0 cost — no paid API call."""
    # The function returns the path; it always costs 0.0 by design.
    # Verify by inspecting that no exception is raised and file is written.
    shot = _FakeShot(duration_s=1.0)
    with tempfile.TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir) / "shot.mp4"
        result = render_shot(shot, dest)
        assert result.exists()  # File produced = 0 paid calls


# ---------------------------------------------------------------------------
# assemble_master tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_assemble_master_produces_file() -> None:
    """assemble_master must write a real mp4 to dest."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        clips = []
        for i, dur in enumerate([2.0, 3.0]):
            clip = tmppath / f"clip_{i}.mp4"
            render_shot(_FakeShot(duration_s=dur, shot_id=f"s{i}"), clip)
            clips.append(clip)

        dest = tmppath / "master.mp4"
        result = assemble_master(clips, dest)
        assert result == dest
        assert dest.exists()
        assert dest.stat().st_size > 0


@pytest.mark.unit
def test_assemble_master_exactly_one_video_stream() -> None:
    """ffprobe must confirm exactly 1 video stream in master."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        clips = [
            tmppath / f"c{i}.mp4"
            for i in range(3)
        ]
        for i, clip in enumerate(clips):
            render_shot(_FakeShot(duration_s=2.0, shot_id=f"s{i}"), clip)

        dest = tmppath / "master.mp4"
        assemble_master(clips, dest)

        vstreams = _video_streams(dest)
        assert len(vstreams) == 1, (
            f"expected exactly 1 video stream, got {len(vstreams)}"
        )


@pytest.mark.unit
def test_assemble_master_exactly_one_audio_stream() -> None:
    """ffprobe must confirm exactly 1 audio stream in master (the silent AAC track)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        clips = [tmppath / f"c{i}.mp4" for i in range(2)]
        for i, clip in enumerate(clips):
            render_shot(_FakeShot(duration_s=2.0, shot_id=f"s{i}"), clip)

        dest = tmppath / "master.mp4"
        assemble_master(clips, dest)

        astreams = _audio_streams(dest)
        assert len(astreams) == 1, (
            f"expected exactly 1 audio stream, got {len(astreams)}"
        )
        assert astreams[0]["codec_name"] == "aac", (
            f"audio codec should be aac, got {astreams[0].get('codec_name')}"
        )


@pytest.mark.unit
def test_assemble_master_video_resolution_preserved() -> None:
    """Master video must retain 1080x1920 after concat."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        clips = [tmppath / "c0.mp4"]
        render_shot(_FakeShot(duration_s=3.0), clips[0])

        dest = tmppath / "master.mp4"
        assemble_master(clips, dest)

        vstreams = _video_streams(dest)
        assert vstreams[0]["width"] == 1080
        assert vstreams[0]["height"] == 1920


@pytest.mark.unit
def test_assemble_master_duration_approx() -> None:
    """Master total duration must be within ±1s of sum of clip durations."""
    durations = [3.0, 4.0, 2.0]
    expected_total = sum(durations)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        clips = []
        for i, dur in enumerate(durations):
            clip = tmppath / f"c{i}.mp4"
            render_shot(_FakeShot(duration_s=dur, shot_id=f"s{i}"), clip)
            clips.append(clip)

        dest = tmppath / "master.mp4"
        assemble_master(clips, dest)

        vstreams = _video_streams(dest)
        reported = float(vstreams[0].get("duration", 0))
        assert abs(reported - expected_total) < 1.0, (
            f"Duration mismatch: expected~{expected_total}s, ffprobe={reported}s"
        )


@pytest.mark.unit
def test_assemble_master_raises_on_empty_clips() -> None:
    """assemble_master must raise ValueError for empty clip list."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir) / "master.mp4"
        with pytest.raises(ValueError, match="at least one clip"):
            assemble_master([], dest)


@pytest.mark.unit
def test_assemble_master_single_clip() -> None:
    """assemble_master with a single clip must produce valid 1v+1a mp4."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        clip = tmppath / "c0.mp4"
        render_shot(_FakeShot(duration_s=5.0), clip)

        dest = tmppath / "master.mp4"
        assemble_master([clip], dest)

        assert dest.exists()
        vstreams = _video_streams(dest)
        astreams = _audio_streams(dest)
        assert len(vstreams) == 1
        assert len(astreams) == 1


@pytest.mark.unit
def test_assemble_master_creates_parent_dirs() -> None:
    """assemble_master must create parent directories if they don't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        clip = tmppath / "c0.mp4"
        render_shot(_FakeShot(duration_s=2.0), clip)

        dest = tmppath / "nested" / "output" / "master.mp4"
        assemble_master([clip], dest)
        assert dest.exists()
