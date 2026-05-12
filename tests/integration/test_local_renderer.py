"""Integration test: actually produce an mp4 with the local renderer.

Marked ``integration`` because it shells out to ffmpeg + espeak-ng. The
test skips automatically when those binaries are absent so unit-only CI
matrices stay green.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


@pytest.fixture(autouse=True)
def _require_binaries() -> None:
    for binary in ("ffmpeg", "ffprobe", "espeak-ng"):
        if shutil.which(binary) is None:
            pytest.skip(f"{binary} not available; install ffmpeg + espeak-ng")


def test_demo_storyboard_renders_to_valid_9x16_mp4(tmp_path: Path) -> None:
    from auto_affi.pipeline.demo_storyboard import build_demo_storyboard
    from auto_affi.pipeline.local_renderer import render_storyboard

    storyboard = build_demo_storyboard()
    output = tmp_path / "demo.mp4"
    workdir = tmp_path / "work"

    result = render_storyboard(
        storyboard,
        workdir=workdir,
        output_path=output,
        enable_tts=True,
    )

    assert result.mp4_path == output
    assert result.scene_count == len(storyboard.scenes)
    assert output.exists()
    assert output.stat().st_size > 50_000  # sanity floor

    ffprobe = shutil.which("ffprobe")
    assert ffprobe is not None
    probe = subprocess.run(  # noqa: S603
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate,codec_name",
            "-of",
            "default=noprint_wrappers=1",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    fields = dict(line.split("=", 1) for line in probe.stdout.strip().splitlines())
    assert fields["width"] == "1080"
    assert fields["height"] == "1920"
    assert fields["codec_name"] == "h264"
    assert fields["r_frame_rate"] == "30/1"
