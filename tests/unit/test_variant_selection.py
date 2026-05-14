"""Tests for the parallel-variant selection logic in gen-video-seedance.py.

The script is not importable as a package module (it's a CLI under
scripts/), so we import via a runtime sys.path shim. This is purposely
narrow: we only test ``_score_variant`` and ``process_clip_with_variants``
behavior. The underlying ``process_clip`` is mocked end-to-end — no Phaya
credits burned, no network calls."""

from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "gen-video-seedance.py"


def _load_script_module():
    """Load scripts/gen-video-seedance.py as a runtime module."""
    spec = importlib.util.spec_from_file_location("gen_video_seedance", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_video_seedance"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def script_mod():
    return _load_script_module()


def test_score_variant_returns_zero_on_exception(script_mod, tmp_path):
    """If analyze_motion raises, _score_variant degrades gracefully to 0."""
    bogus = tmp_path / "does-not-exist.mp4"
    assert script_mod._score_variant(bogus) == 0.0


def test_score_variant_combines_motion_and_duration(script_mod, tmp_path):
    """Score = motion_score × duration_term (capped at 1.0 for ≥3s clips)."""
    fake_clip = tmp_path / "x.mp4"
    fake_clip.write_bytes(b"\x00")

    class FakeMotion:
        motion_score = 0.5
        duration_s = 4.0  # → duration_term capped to 1.0

    with patch("auto_affi.qa.video_review.analyze_motion", return_value=FakeMotion()):
        score = script_mod._score_variant(fake_clip)
    assert score == pytest.approx(0.5)


def test_score_variant_penalizes_short_clips(script_mod, tmp_path):
    """Sub-3s clips get a proportional duration penalty (avoid 1-frame wins)."""
    fake_clip = tmp_path / "tiny.mp4"
    fake_clip.write_bytes(b"\x00")

    class TinyMotion:
        motion_score = 0.5
        duration_s = 1.5  # → duration_term = 0.5

    with patch("auto_affi.qa.video_review.analyze_motion", return_value=TinyMotion()):
        score = script_mod._score_variant(fake_clip)
    assert score == pytest.approx(0.25)


def test_process_clip_with_variants_passthrough_n1(script_mod, tmp_path):
    """n_variants=1 → direct passthrough, no parallelism, no scoring."""
    canonical = tmp_path / "clip0-seedance-final.mp4"
    canonical.write_bytes(b"\x00" * 100)

    sentinel_result = {"clip_path": canonical, "cost_thb": 1.0}

    async def fake_process_clip(**kwargs):
        return sentinel_result

    with patch.object(script_mod, "process_clip", side_effect=fake_process_clip):
        result = asyncio.run(script_mod.process_clip_with_variants(
            n_variants=1,
            client=None, gcs=None, clip_idx=0,
            start_scene_idx=0, end_scene_idx=1, target_duration_s=4.0,
            motion_label="", dialogue_th="", workdir=tmp_path,
            order_no=1, run_no=1, resolution="720p",
        ))
    assert result is sentinel_result


def test_process_clip_with_variants_runs_n_jobs_and_picks_highest_score(script_mod, tmp_path):
    """n_variants=3 → run 3 jobs in parallel, score, copy winner to canonical."""
    workdir = tmp_path
    canonical = workdir / "clip0-seedance-final.mp4"

    call_count = {"n": 0}

    async def fake_process_clip(**kwargs):
        # Each call writes the canonical clip file; process_clip_with_variants
        # then renames it to a variant-specific path.
        i = call_count["n"]
        call_count["n"] += 1
        canonical.write_bytes(f"variant-{i}-content".encode())
        return {
            "clip_path": canonical, "cost_thb": 1.0,
            "start_gs": "", "end_gs": "", "raw_clip": canonical,
            "trimmed_clip": canonical, "audio_path": None,
        }

    # Score in reverse: variant 0 lowest, variant 2 highest
    scores_by_filename = {
        "clip0-seedance-variant-0.mp4": 0.10,
        "clip0-seedance-variant-1.mp4": 0.30,
        "clip0-seedance-variant-2.mp4": 0.50,
    }

    def fake_score(path: Path) -> float:
        return scores_by_filename.get(path.name, 0.0)

    with patch.object(script_mod, "process_clip", side_effect=fake_process_clip), \
         patch.object(script_mod, "_score_variant", side_effect=fake_score):
        result = asyncio.run(script_mod.process_clip_with_variants(
            n_variants=3,
            client=None, gcs=None, clip_idx=0,
            start_scene_idx=0, end_scene_idx=1, target_duration_s=4.0,
            motion_label="", dialogue_th="", workdir=workdir,
            order_no=1, run_no=1, resolution="720p",
        ))

    assert call_count["n"] == 3
    assert result is not None
    assert result["clip_path"] == canonical
    assert result["selected_variant"] == 2
    assert result["n_variants"] == 3
    # All 3 variant files preserved for audit
    for i in range(3):
        assert (workdir / f"clip0-seedance-variant-{i}.mp4").exists()
    # Canonical = winner's contents
    assert canonical.read_bytes() == b"variant-2-content"


def test_process_clip_with_variants_handles_all_failed(script_mod, tmp_path):
    """If every variant returns None, the wrapper returns None too."""
    async def all_fail(**kwargs):
        return None

    with patch.object(script_mod, "process_clip", side_effect=all_fail):
        result = asyncio.run(script_mod.process_clip_with_variants(
            n_variants=3,
            client=None, gcs=None, clip_idx=0,
            start_scene_idx=0, end_scene_idx=1, target_duration_s=4.0,
            motion_label="", dialogue_th="", workdir=tmp_path,
            order_no=1, run_no=1, resolution="720p",
        ))
    assert result is None
