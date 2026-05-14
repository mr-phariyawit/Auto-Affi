"""Tests for the HyperFrames renderer wiring — render path is mocked so
no actual ``npx`` / Chrome invocation runs in CI."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from auto_affi.post.hyperframes_renderer import (
    HyperframesRendererError,
    OverlayRender,
    composite_overlays_with_ffmpeg,
    render_storyboard_overlays,
)
from auto_affi.schemas.storyboard import HyperframeOverlay


def _mk_template(projects_dir: Path, name: str) -> Path:
    """Create a stub HyperFrames project dir with a minimal index.html."""
    p = projects_dir / name
    p.mkdir(parents=True)
    (p / "index.html").write_text(
        '<div id="stage" data-composition-id="x" data-width="720" data-height="1280" data-duration="2"></div>',
        encoding="utf-8",
    )
    return p


def test_render_storyboard_overlays_skips_missing_template(tmp_path):
    overlays = [
        HyperframeOverlay(scene_idx=0, template="not-a-real-template", props={}),
    ]
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()
    output_dir = tmp_path / "out"
    # Force shutil.which to return a path so the npx-availability check passes
    with patch("auto_affi.post.hyperframes_renderer.shutil.which", return_value="/usr/bin/npx"):
        results = render_storyboard_overlays(
            overlays=overlays, projects_dir=projects_dir, output_dir=output_dir,
        )
    assert results == []
    # Manifest is written even on empty result
    assert (output_dir / "overlays-manifest.json").exists()


def test_render_storyboard_overlays_runs_renderer_for_each_valid_template(tmp_path):
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()
    _mk_template(projects_dir, "closing-tag")
    output_dir = tmp_path / "out"

    overlays = [
        HyperframeOverlay(
            scene_idx=4, template="closing-tag",
            props={"start_s": 40.0, "duration_s": 4.5, "text": "ระยะทางไม่ลบเสียงพ่อ"},
        ),
    ]

    captured_cmds: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        captured_cmds.append(cmd)
        # Simulate creating the output file so downstream sidecar logic works
        # Find the --output flag and touch the path
        if "--output" in cmd:
            i = cmd.index("--output")
            Path(cmd[i + 1]).parent.mkdir(parents=True, exist_ok=True)
            Path(cmd[i + 1]).write_bytes(b"\x00" * 10)
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    with patch("auto_affi.post.hyperframes_renderer.shutil.which", return_value="/usr/bin/npx"), \
         patch("auto_affi.post.hyperframes_renderer.subprocess.run", side_effect=fake_run):
        results = render_storyboard_overlays(
            overlays=overlays, projects_dir=projects_dir, output_dir=output_dir,
        )

    assert len(results) == 1
    r = results[0]
    assert r.template == "closing-tag"
    assert r.scene_idx == 4
    assert r.start_s == 40.0
    assert r.duration_s == 4.5
    assert r.mov_path.name == "overlay-4-closing-tag.mov"

    # Verify variables were passed as JSON
    cmd = captured_cmds[0]
    assert "--variables" in cmd
    vars_json = cmd[cmd.index("--variables") + 1]
    parsed = json.loads(vars_json)
    assert parsed["text"] == "ระยะทางไม่ลบเสียงพ่อ"
    assert parsed["start_s"] == 40.0
    assert parsed["duration_s"] == 4.5


def test_render_storyboard_overlays_persists_manifest(tmp_path):
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()
    _mk_template(projects_dir, "snap-title")
    output_dir = tmp_path / "out"

    overlays = [
        HyperframeOverlay(scene_idx=0, template="snap-title",
                           props={"start_s": 0.2, "duration_s": 1.5, "text_th": "หยุดเสียเวลา"}),
    ]

    def fake_run(cmd, **kwargs):
        if "--output" in cmd:
            i = cmd.index("--output")
            Path(cmd[i + 1]).parent.mkdir(parents=True, exist_ok=True)
            Path(cmd[i + 1]).write_bytes(b"\x00" * 10)
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    with patch("auto_affi.post.hyperframes_renderer.shutil.which", return_value="/usr/bin/npx"), \
         patch("auto_affi.post.hyperframes_renderer.subprocess.run", side_effect=fake_run):
        render_storyboard_overlays(
            overlays=overlays, projects_dir=projects_dir, output_dir=output_dir,
        )

    manifest_path = output_dir / "overlays-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert len(manifest) == 1
    assert manifest[0]["template"] == "snap-title"
    assert manifest[0]["props"]["text_th"] == "หยุดเสียเวลา"


def test_render_storyboard_overlays_no_npx():
    """If npx is missing, raise — the integration is unusable without Node."""
    with patch("auto_affi.post.hyperframes_renderer.shutil.which", return_value=None):
        with pytest.raises(HyperframesRendererError):
            render_storyboard_overlays(
                overlays=[], projects_dir=Path("."), output_dir=Path("."),
            )


def test_composite_overlays_with_ffmpeg_passthrough_when_empty(tmp_path):
    """Empty overlay list = byte-copy pass-through (no filter graph)."""
    base = tmp_path / "base.mp4"
    base.write_bytes(b"\x00" * 100)
    out = tmp_path / "out.mp4"

    captured_cmd: list[str] = []

    def fake_run(cmd, **kwargs):
        captured_cmd.extend(cmd)
        out.write_bytes(b"copied")
        return subprocess.CompletedProcess(cmd, 0)

    with patch("auto_affi.post.hyperframes_renderer.subprocess.run", side_effect=fake_run):
        result = composite_overlays_with_ffmpeg(base_video=base, overlays=[], output=out)

    assert result == out
    assert "-c" in captured_cmd and "copy" in captured_cmd
    # NO filter_complex when empty
    assert "-filter_complex" not in captured_cmd


def test_composite_overlays_with_ffmpeg_builds_filter_chain(tmp_path):
    """Multiple overlays → chained overlay filters with -itsoffset per input."""
    base = tmp_path / "base.mp4"
    base.write_bytes(b"\x00" * 100)
    mov1 = tmp_path / "ov1.mov"; mov1.write_bytes(b"\x00")
    mov2 = tmp_path / "ov2.mov"; mov2.write_bytes(b"\x00")

    overlays = [
        OverlayRender(template="a", scene_idx=0, mov_path=mov1, start_s=2.0, duration_s=1.0),
        OverlayRender(template="b", scene_idx=4, mov_path=mov2, start_s=10.0, duration_s=3.0),
    ]
    out = tmp_path / "out.mp4"

    captured_cmd: list[str] = []

    def fake_run(cmd, **kwargs):
        captured_cmd.extend(cmd)
        out.write_bytes(b"composited")
        return subprocess.CompletedProcess(cmd, 0)

    with patch("auto_affi.post.hyperframes_renderer.subprocess.run", side_effect=fake_run):
        composite_overlays_with_ffmpeg(base_video=base, overlays=overlays, output=out)

    # Verify -itsoffset appears for each overlay with its start_s
    assert "-itsoffset" in captured_cmd
    assert "2.000" in captured_cmd
    assert "10.000" in captured_cmd
    # Filter chain mentions both overlays' enable windows
    fc_idx = captured_cmd.index("-filter_complex") + 1
    fc = captured_cmd[fc_idx]
    assert "between(t,2.000,3.000)" in fc
    assert "between(t,10.000,13.000)" in fc
