"""Unit tests for the video-review unit.

Validates pure-Pillow pixel-diff + static-detection logic without needing
real Phaya outputs. Synthetic clips are generated on the fly via PIL +
ffmpeg from static and moving image sequences.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

from auto_affi.qa.video_review import (
    MOTION_STATIC_THRESHOLD,
    analyze_motion,
    analyze_scene,
    render_report_md,
    review_video_run,
)


def _make_solid_image(path: Path, size: tuple[int, int], color: tuple[int, int, int]) -> None:
    img = Image.new("RGB", size, color)
    img.save(path, "JPEG", quality=85)


def _make_clip_from_frames(frames: list[Path], out: Path, fps: int = 25) -> None:
    """Build a clip from a sequence of input frames at given fps."""
    # ffmpeg concat-glob is fiddly; use image2 demuxer with %d naming
    workdir = out.parent / f"_clip_build_{out.stem}"
    workdir.mkdir(parents=True, exist_ok=True)
    for i, f in enumerate(frames):
        link = workdir / f"frame_{i:04d}.jpg"
        link.write_bytes(f.read_bytes())
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
         "-i", str(workdir / "frame_%04d.jpg"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
        check=True,
    )


@pytest.fixture
def static_clip(tmp_path):
    """A 2-second clip of a single solid-grey frame replicated."""
    frames = []
    for i in range(50):  # 50 frames @ 25fps = 2s
        f = tmp_path / f"static_{i:04d}.jpg"
        _make_solid_image(f, (128, 256), (96, 96, 96))
        frames.append(f)
    out = tmp_path / "static.mp4"
    _make_clip_from_frames(frames, out)
    return out


@pytest.fixture
def moving_clip(tmp_path):
    """A 2-second clip that transitions from black to white — clearly moving."""
    frames = []
    for i in range(50):
        f = tmp_path / f"moving_{i:04d}.jpg"
        v = int(255 * i / 49)
        _make_solid_image(f, (128, 256), (v, v, v))
        frames.append(f)
    out = tmp_path / "moving.mp4"
    _make_clip_from_frames(frames, out)
    return out


def test_analyze_motion_static(static_clip, tmp_path):
    score = analyze_motion(static_clip, workdir=tmp_path / "qa")
    assert score.is_static is True
    assert score.mean_abs_diff < MOTION_STATIC_THRESHOLD
    assert 1.5 < score.duration_s < 2.5


def test_analyze_motion_moving(moving_clip, tmp_path):
    score = analyze_motion(moving_clip, workdir=tmp_path / "qa")
    assert score.is_static is False
    assert score.mean_abs_diff > MOTION_STATIC_THRESHOLD
    assert 1.5 < score.duration_s < 2.5


def test_analyze_scene_flags_motion_intent_missed(static_clip, tmp_path):
    sb_frame = {
        "idx": 0,
        "duration_s": 2.0,
        "camera_movement": "slow-dolly-in",
    }
    review = analyze_scene(
        scene_idx=0, clip_path=static_clip,
        storyboard_frame=sb_frame, workdir=tmp_path / "qa",
    )
    assert "MOTION_INTENT_MISSED" in review.issues
    assert review.motion.is_static is True
    assert "Seedance" in review.recommendation or "motion strength" in review.recommendation


def test_analyze_scene_passes_when_intent_is_static(static_clip, tmp_path):
    sb_frame = {
        "idx": 1,
        "duration_s": 2.0,
        "camera_movement": "static",
    }
    review = analyze_scene(
        scene_idx=1, clip_path=static_clip,
        storyboard_frame=sb_frame, workdir=tmp_path / "qa",
    )
    assert "MOTION_INTENT_MISSED" not in review.issues


def test_analyze_scene_flags_duration_drift(moving_clip, tmp_path):
    # moving_clip is ~2s; declare expected 5s → 3s drift
    sb_frame = {
        "idx": 2,
        "duration_s": 5.0,
        "camera_movement": "static",
    }
    review = analyze_scene(
        scene_idx=2, clip_path=moving_clip,
        storyboard_frame=sb_frame, workdir=tmp_path / "qa",
    )
    assert "DURATION_MISMATCH" in review.issues


def test_review_video_run_rolls_up_overall(tmp_path, static_clip):
    # Stage a workdir with two clips both named s0-clip.mp4, s1-clip.mp4
    workdir = tmp_path / "run-workdir"
    workdir.mkdir()
    (workdir / "s0-clip.mp4").write_bytes(static_clip.read_bytes())
    (workdir / "s1-clip.mp4").write_bytes(static_clip.read_bytes())

    # Storyboard JSON: both scenes ask for non-static motion
    sb = {
        "frames": [
            {"idx": 0, "duration_s": 2.0, "camera_movement": "slow-dolly-in"},
            {"idx": 1, "duration_s": 2.0, "camera_movement": "push-in"},
        ]
    }
    sb_path = workdir / "storyboard.json"
    import json
    sb_path.write_text(json.dumps(sb), encoding="utf-8")

    report = review_video_run(
        storyboard_json_path=sb_path, workdir=workdir, run_no=42,
    )
    assert len(report.reviews) == 2
    assert report.overall_static_ratio == 1.0
    assert "Seedance" in report.overall_recommendation
    md = render_report_md(report)
    assert "STATIC" in md
    assert "MOTION_INTENT_MISSED" in md


def test_render_report_md_handles_empty(tmp_path):
    from auto_affi.qa.video_review import VideoReviewReport
    rep = VideoReviewReport(
        run_id="", item_id=0, order_no=0, run_no=0,
        reviews=[], overall_static_ratio=0.0,
        overall_recommendation="No clips found; nothing to review.",
    )
    md = render_report_md(rep)
    assert "No clips found" in md
