"""Tests for scripts/produce-variant-set.py — variant orchestrator.

End-to-end behavior is mocked (Higgsfield CLI, Gemini, edge-tts,
HyperFrames, ffmpeg) — these tests verify the orchestration LOGIC:
shared shots render once, variant shots render per variant, final
assembly produces N mp4s with correct file paths."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "produce-variant-set.py"


def _load_script_module():
    spec = importlib.util.spec_from_file_location("produce_variant_set", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["produce_variant_set"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def script_mod():
    return _load_script_module()


def test_render_plan_dedupes_shared_shots(script_mod):
    """Given a ConceptVariantSet with 2 hook shots + 5 base shots × 3
    variants, the render plan must dispatch the 5 base shots ONCE and
    the 2 hook shots × 3 variants = 6 hook renders, not 21.

    Fixture math (body sum must be within ±2s of target; body+hooks must
    equal target ±0.01s):
      body  = 5 shots × 5.0s = 25.0s
      hooks = 2 shots × 1.0s =  2.0s
      target = 27.0s
        |25 - 27| = 2 ≤ 2 ✓ (AiStoryboard)
        25 + 2   = 27       ✓ (ConceptVariantSet)
    """
    from auto_affi.schemas.ai_storyboard import (
        AiShot, AiStoryboard, AudioSource, ConceptVariantSet,
        Generator, NarrativeRole,
    )

    def _shot(sid, role=NarrativeRole.STORY, dur=5.0, gen=Generator.HOLD):
        return AiShot(
            shot_id=sid, narrative_role=role, duration_s=dur,
            generator=gen, image_prompt="a" * 30,
            consistency_seed=42, audio_source=AudioSource.MUSIC_ONLY,
        )

    base = AiStoryboard(
        concept_id="t", title_en="t", title_th="t", item_id=1,
        consistency_seed=42, target_total_duration_s=27.0,
        music_prompt="a" * 30, music_duration_s=27.0,
        shots=[_shot("s2", dur=5.0), _shot("s3", dur=5.0),
               _shot("s4", dur=5.0), _shot("s5", dur=5.0), _shot("s6", dur=5.0)],
    )
    variants = {
        "a": [_shot("s0", role=NarrativeRole.HOOK, dur=1.0),
              _shot("s1", role=NarrativeRole.HOOK, dur=1.0)],
        "b": [_shot("s0", role=NarrativeRole.HOOK, dur=1.0),
              _shot("s1", role=NarrativeRole.HOOK, dur=1.0)],
        "c": [_shot("s0", role=NarrativeRole.HOOK, dur=1.0),
              _shot("s1", role=NarrativeRole.HOOK, dur=1.0)],
    }
    vs = ConceptVariantSet(
        concept_id="t", item_id=1, base=base, variants=variants,
    )

    plan = script_mod.build_render_plan(vs)
    # 5 shared shots (rendered once) + 2 hook shots × 3 variants = 11 total
    assert plan.shared_shot_count == 5
    assert plan.variant_hook_render_count == 6
    assert plan.total_renders == 11


def test_build_render_plan_emits_correct_output_paths(script_mod, tmp_path):
    """Plan should emit one mp4 path per variant under
    out/<sku>-<concept>/variant-<id>/final.mp4.

    Fixture math:
      body  = 2 shots × 6.0s = 12.0s
      hooks = 2 shots × 1.0s =  2.0s
      target = 14.0s
        |12 - 14| = 2 ≤ 2 ✓ (AiStoryboard)
        12 + 2   = 14       ✓ (ConceptVariantSet)
    """
    from auto_affi.schemas.ai_storyboard import (
        AiShot, AiStoryboard, AudioSource, ConceptVariantSet,
        Generator, NarrativeRole,
    )

    def _shot(sid, role=NarrativeRole.STORY, dur=6.0):
        return AiShot(
            shot_id=sid, narrative_role=role, duration_s=dur,
            generator=Generator.HOLD, image_prompt="a" * 30,
            consistency_seed=42, audio_source=AudioSource.MUSIC_ONLY,
        )

    base = AiStoryboard(
        concept_id="shure-vs-maono", title_en="t", title_th="t",
        item_id=28875679676, consistency_seed=42,
        target_total_duration_s=14.0, music_prompt="a" * 30,
        music_duration_s=14.0,
        shots=[_shot("s2", dur=6.0), _shot("s3", dur=6.0)],
    )
    variants = {
        "a": [_shot("s0", role=NarrativeRole.HOOK, dur=1.0),
              _shot("s1", role=NarrativeRole.HOOK, dur=1.0)],
        "b": [_shot("s0", role=NarrativeRole.HOOK, dur=1.0),
              _shot("s1", role=NarrativeRole.HOOK, dur=1.0)],
    }
    vs = ConceptVariantSet(
        concept_id="shure-vs-maono", item_id=28875679676,
        base=base, variants=variants,
    )

    plan = script_mod.build_render_plan(vs, out_root=tmp_path)
    expected_a = tmp_path / "28875679676-shure-vs-maono" / "variant-a" / "final.mp4"
    expected_b = tmp_path / "28875679676-shure-vs-maono" / "variant-b" / "final.mp4"
    assert plan.variant_outputs == {"a": expected_a, "b": expected_b}


def test_build_links_json_assigns_unique_sub_ids(script_mod, tmp_path):
    """links.json maps variant_id → sub_id of shape
    <item_id>-<concept>-<variant_id>.

    Fixture math (2 body shots needed — 1 body shot cannot satisfy both
    validators within the duration_s cap of 6.0s):
      body  = 2 shots × 4.0s = 8.0s
      hooks = 2 shots × 1.0s = 2.0s
      target = 10.0s
        |8 - 10| = 2 ≤ 2 ✓ (AiStoryboard)
        8 + 2   = 10      ✓ (ConceptVariantSet)
    """
    from auto_affi.schemas.ai_storyboard import (
        AiShot, AiStoryboard, AudioSource, ConceptVariantSet,
        Generator, NarrativeRole,
    )

    def _shot(sid, role=NarrativeRole.STORY, dur=4.0):
        return AiShot(
            shot_id=sid, narrative_role=role, duration_s=dur,
            generator=Generator.HOLD, image_prompt="a" * 30,
            consistency_seed=42, audio_source=AudioSource.MUSIC_ONLY,
        )

    base = AiStoryboard(
        concept_id="shure-vs-maono", title_en="t", title_th="t",
        item_id=28875679676, consistency_seed=42,
        target_total_duration_s=10.0, music_prompt="a" * 30,
        music_duration_s=10.0,
        shots=[_shot("s2", dur=4.0), _shot("s3", dur=4.0)],
    )
    variants = {
        "a": [_shot("s0", role=NarrativeRole.HOOK, dur=1.0),
              _shot("s1", role=NarrativeRole.HOOK, dur=1.0)],
        "b": [_shot("s0", role=NarrativeRole.HOOK, dur=1.0),
              _shot("s1", role=NarrativeRole.HOOK, dur=1.0)],
    }
    vs = ConceptVariantSet(
        concept_id="shure-vs-maono", item_id=28875679676,
        base=base, variants=variants,
    )
    links = script_mod.build_links_map(vs)
    assert links == {
        "a": "28875679676-shure-vs-maono-a",
        "b": "28875679676-shure-vs-maono-b",
    }
