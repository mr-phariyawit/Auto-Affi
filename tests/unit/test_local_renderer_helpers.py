"""Unit tests for pure helpers in the local renderer (no ffmpeg/espeak)."""

from __future__ import annotations

import pytest

from auto_affi.pipeline.demo_storyboard import build_demo_storyboard
from auto_affi.schemas.storyboard import REQUIRED_EDITOR_PASSES


@pytest.mark.unit
def test_build_demo_storyboard_is_a_valid_storyboard() -> None:
    board = build_demo_storyboard()
    assert len(board.scenes) == 5
    assert board.scenes[0].purpose.value == "hook"
    assert board.scenes[-1].purpose.value == "cta"
    assert board.cta_scene_idx == 4
    assert board.editor_passes == list(REQUIRED_EDITOR_PASSES)
    assert all(scene.dialogue is not None for scene in board.scenes)


@pytest.mark.unit
def test_build_demo_storyboard_duration_under_cap() -> None:
    board = build_demo_storyboard()
    assert 5 <= board.total_duration_s <= 60
