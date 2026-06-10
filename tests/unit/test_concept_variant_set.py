"""Tests for ConceptVariantSet -- one concept x N hook variants on
shared body+CTA base."""

from __future__ import annotations

import pytest

from auto_affi.schemas.ai_storyboard import (
    AiShot,
    AiStoryboard,
    AudioSource,
    ConceptVariantSet,
    Generator,
    NarrativeRole,
)


def _hook_shot(shot_id: str = "s0", dur: float = 1.0) -> AiShot:
    return AiShot(
        shot_id=shot_id,
        narrative_role=NarrativeRole.HOOK,
        duration_s=dur,
        generator=Generator.HOLD,
        image_prompt="a" * 30,
        consistency_seed=51728,
        audio_source=AudioSource.SILENCE,
    )


def _body_shot(shot_id: str, dur: float = 6.0) -> AiShot:
    return AiShot(
        shot_id=shot_id,
        narrative_role=NarrativeRole.STORY,
        duration_s=dur,
        generator=Generator.HOLD,
        image_prompt="a" * 30,
        consistency_seed=51728,
        audio_source=AudioSource.MUSIC_ONLY,
    )


def _base_with_body_and_cta(target_total: float) -> AiStoryboard:
    # 2s reserved for 2-shot hooks (each 1s) so we stay within AiStoryboard's
    # ±2s tolerance check on (sum(base.shots) vs target_total_duration_s).
    body_dur = target_total - 2.0
    # Split body into 3 shots so each respects AiShot's duration_s <= 6.0 cap
    per_shot = body_dur / 3
    return AiStoryboard(
        concept_id="test-concept",
        title_en="t", title_th="t",
        item_id=1,
        consistency_seed=51728,
        target_total_duration_s=target_total,
        music_prompt="a" * 30,
        music_duration_s=target_total,
        shots=[
            _body_shot("s2", dur=per_shot),
            _body_shot("s3", dur=per_shot),
            _body_shot("s4", dur=per_shot),
        ],
    )


def test_concept_variant_set_valid_shape():
    """Happy path: base + 3 hook variants each contributing 6s of hook."""
    base = _base_with_body_and_cta(target_total=20.0)
    variants = {
        "a": [_hook_shot("s0"), _hook_shot("s1")],
        "b": [_hook_shot("s0"), _hook_shot("s1")],
        "c": [_hook_shot("s0"), _hook_shot("s1")],
    }
    vs = ConceptVariantSet(
        concept_id="shure-vs-maono",
        item_id=1,
        base=base,
        variants=variants,
    )
    assert vs.concept_id == "shure-vs-maono"
    assert list(vs.variants.keys()) == ["a", "b", "c"]


def test_concept_variant_set_rejects_empty_variants():
    base = _base_with_body_and_cta(target_total=20.0)
    with pytest.raises(ValueError, match="at least one"):
        ConceptVariantSet(
            concept_id="x", item_id=1, base=base, variants={},
        )


def test_concept_variant_set_rejects_mismatched_hook_shot_count():
    """All variants must have the same number of hook shots."""
    base = _base_with_body_and_cta(target_total=20.0)
    variants = {
        "a": [_hook_shot("s0"), _hook_shot("s1")],
        "b": [_hook_shot("s0")],  # only 1 hook shot — mismatch
    }
    with pytest.raises(ValueError, match="same number of hook shots"):
        ConceptVariantSet(
            concept_id="x", item_id=1, base=base, variants=variants,
        )


def test_concept_variant_set_rejects_variant_seed_mismatch():
    """Variant hook shots must share base.consistency_seed."""
    base = _base_with_body_and_cta(target_total=20.0)
    bad_hook = AiShot(
        shot_id="s0",
        narrative_role=NarrativeRole.HOOK,
        duration_s=3.0,
        generator=Generator.HOLD,
        image_prompt="a" * 30,
        consistency_seed=99999,  # different seed
        audio_source=AudioSource.SILENCE,
    )
    variants = {
        "a": [bad_hook, _hook_shot("s1")],
    }
    with pytest.raises(ValueError, match="consistency_seed"):
        ConceptVariantSet(
            concept_id="x", item_id=1, base=base, variants=variants,
        )


def test_concept_variant_set_total_duration_check():
    """base.target_total_duration must equal hook-duration + body-duration."""
    base = _base_with_body_and_cta(target_total=20.0)
    # Hooks here add 2s (2 x 1s), body adds 18s, total 20 ✓
    ok = ConceptVariantSet(
        concept_id="x", item_id=1, base=base,
        variants={"a": [_hook_shot("s0"), _hook_shot("s1")]},
    )
    assert ok is not None
    # Now overshoot: 3 x 1s hooks = 3s, body 18s, total 21 vs target 20 → fail
    with pytest.raises(ValueError, match="total duration"):
        ConceptVariantSet(
            concept_id="x", item_id=1, base=base,
            variants={"a": [_hook_shot("s0"), _hook_shot("s1"), _hook_shot("s9")]},
        )


def test_concept_variant_set_variant_id_format():
    """Variant IDs should be lowercase single letters a-z for filename safety."""
    base = _base_with_body_and_cta(target_total=20.0)
    with pytest.raises(ValueError, match="variant id"):
        ConceptVariantSet(
            concept_id="x", item_id=1, base=base,
            variants={"VARIANT-1": [_hook_shot("s0"), _hook_shot("s1")]},
        )
