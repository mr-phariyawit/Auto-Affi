"""Tests for src/auto_affi/agents/writers_room.py.

All tests are deterministic offline — no network, no LLM, no Anthropic.
"""

from __future__ import annotations

import pytest

from auto_affi.adapters.shopee import ShopeeProduct, get_fixture_products
from auto_affi.agents.strategist import build_brief
from auto_affi.agents.writers_room import build_storyboard, _derive_seed
from auto_affi.schemas.storyboard import (
    EditorPass,
    REQUIRED_EDITOR_PASSES,
    ScenePurpose,
    Storyboard,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def umbrella_product() -> ShopeeProduct:
    return ShopeeProduct(
        item_id=10000001,
        shop_id=500001,
        name="ร่มกันฝน UV พับได้ 3 ตอน กันแดด กันฝน",
        price_min=129.0,
        price_max=199.0,
        commission_rate=0.07,
        rating_star=4.8,
        sales=3200,
    )


@pytest.fixture()
def sunscreen_product() -> ShopeeProduct:
    return ShopeeProduct(
        item_id=10000003,
        shop_id=500003,
        name="ครีมกันแดด SPF50+ PA++++ ไม่มัน บางเบา",
        price_min=185.0,
        price_max=285.0,
        commission_rate=0.09,
        rating_star=4.9,
        sales=8100,
    )


@pytest.fixture()
def umbrella_brief(umbrella_product: ShopeeProduct):  # type: ignore[no-untyped-def]
    return build_brief(umbrella_product)


@pytest.fixture()
def umbrella_storyboard(umbrella_brief, umbrella_product: ShopeeProduct) -> Storyboard:  # type: ignore[no-untyped-def]
    return build_storyboard(umbrella_brief, umbrella_product)


# ---------------------------------------------------------------------------
# Schema validity
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_storyboard_is_storyboard_instance(
    umbrella_brief, umbrella_product: ShopeeProduct  # type: ignore[no-untyped-def]
) -> None:
    sb = build_storyboard(umbrella_brief, umbrella_product)
    assert isinstance(sb, Storyboard)


@pytest.mark.unit
def test_storyboard_schema_valid_all_fixtures() -> None:
    """Every fixture product must produce a schema-valid storyboard."""
    for product in get_fixture_products():
        brief = build_brief(product)
        sb = build_storyboard(brief, product)
        assert isinstance(sb, Storyboard)


@pytest.mark.unit
def test_brief_id_propagated(umbrella_brief, umbrella_storyboard: Storyboard) -> None:  # type: ignore[no-untyped-def]
    assert umbrella_storyboard.brief_id == umbrella_brief.brief_id


# ---------------------------------------------------------------------------
# Hook constraints
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_hook_is_first_scene(umbrella_storyboard: Storyboard) -> None:
    assert umbrella_storyboard.scenes[0].purpose == ScenePurpose.HOOK


@pytest.mark.unit
def test_hook_duration_leq_2s(umbrella_storyboard: Storyboard) -> None:
    hook = umbrella_storyboard.scenes[0]
    assert hook.duration_s <= 2.0, f"hook duration {hook.duration_s}s > 2.0s"


@pytest.mark.unit
def test_hook_duration_geq_1s(umbrella_storyboard: Storyboard) -> None:
    hook = umbrella_storyboard.scenes[0]
    assert hook.duration_s >= 1.0, f"hook duration {hook.duration_s}s < 1.0s"


# ---------------------------------------------------------------------------
# CTA constraints
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_last_scene_is_cta(umbrella_storyboard: Storyboard) -> None:
    assert umbrella_storyboard.scenes[-1].purpose == ScenePurpose.CTA


@pytest.mark.unit
def test_cta_scene_idx_valid(umbrella_storyboard: Storyboard) -> None:
    sb = umbrella_storyboard
    assert sb.cta_scene_idx == len(sb.scenes) - 1
    assert sb.scenes[sb.cta_scene_idx].purpose == ScenePurpose.CTA


# ---------------------------------------------------------------------------
# Duration constraints
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_total_duration_within_60s(umbrella_storyboard: Storyboard) -> None:
    total = umbrella_storyboard.total_duration_s
    assert total <= 60.0, f"total duration {total}s > 60s"


@pytest.mark.unit
def test_total_duration_positive(umbrella_storyboard: Storyboard) -> None:
    assert umbrella_storyboard.total_duration_s > 0.0


@pytest.mark.unit
def test_avg_body_shot_in_band(umbrella_storyboard: Storyboard) -> None:
    """Body shots (non-hook) average must be 1.0–5.0s per Storyboard validator."""
    body = umbrella_storyboard.scenes[1:]
    avg = sum(s.duration_s for s in body) / len(body)
    assert 1.0 <= avg <= 5.0, f"avg body shot {avg:.2f}s outside [1.0, 5.0]"


@pytest.mark.unit
def test_each_scene_duration_positive(umbrella_storyboard: Storyboard) -> None:
    for scene in umbrella_storyboard.scenes:
        assert scene.duration_s > 0.0, f"scene[{scene.idx}] has duration_s <= 0"


@pytest.mark.unit
def test_each_scene_duration_leq_15s(umbrella_storyboard: Storyboard) -> None:
    """Schema enforces duration_s <= 15; our templates use <= 6."""
    for scene in umbrella_storyboard.scenes:
        assert scene.duration_s <= 15.0


# ---------------------------------------------------------------------------
# Scene index contiguity
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_scene_indices_contiguous(umbrella_storyboard: Storyboard) -> None:
    for expected, scene in enumerate(umbrella_storyboard.scenes):
        assert scene.idx == expected, (
            f"scene at position {expected} has idx={scene.idx}"
        )


# ---------------------------------------------------------------------------
# Dialogue / captions
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_all_scenes_have_dialogue_or_on_screen_text(umbrella_storyboard: Storyboard) -> None:
    for scene in umbrella_storyboard.scenes:
        has_dialogue = scene.dialogue is not None
        has_caption = scene.on_screen_text is not None
        assert has_dialogue or has_caption, (
            f"scene[{scene.idx}] ({scene.purpose.value}) has neither dialogue nor on_screen_text"
        )


@pytest.mark.unit
def test_dialogue_text_non_empty(umbrella_storyboard: Storyboard) -> None:
    for scene in umbrella_storyboard.scenes:
        if scene.dialogue is not None:
            assert len(scene.dialogue.text_th) >= 1


# ---------------------------------------------------------------------------
# Voice and music profile
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_voice_profile_lang_th(umbrella_storyboard: Storyboard) -> None:
    assert umbrella_storyboard.voice_profile.lang == "th"


@pytest.mark.unit
def test_music_brief_bpm_ordered(umbrella_storyboard: Storyboard) -> None:
    lo, hi = umbrella_storyboard.music_brief.bpm_range
    assert lo <= hi


# ---------------------------------------------------------------------------
# Editor passes
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_all_required_editor_passes_present(umbrella_storyboard: Storyboard) -> None:
    present = set(umbrella_storyboard.editor_passes)
    for required_pass in REQUIRED_EDITOR_PASSES:
        assert required_pass in present, f"Missing editor pass: {required_pass}"


@pytest.mark.unit
def test_editor_passes_are_editor_pass_enum(umbrella_storyboard: Storyboard) -> None:
    for ep in umbrella_storyboard.editor_passes:
        assert isinstance(ep, EditorPass)


# ---------------------------------------------------------------------------
# Affiliate link
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_affiliate_link_placement_non_empty(umbrella_storyboard: Storyboard) -> None:
    assert len(umbrella_storyboard.affiliate_link_placement.strip()) >= 1


@pytest.mark.unit
def test_affiliate_link_contains_pinned_comment(umbrella_storyboard: Storyboard) -> None:
    assert "pinned_comment" in umbrella_storyboard.affiliate_link_placement


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_build_storyboard_is_deterministic(
    umbrella_brief, umbrella_product: ShopeeProduct  # type: ignore[no-untyped-def]
) -> None:
    sb1 = build_storyboard(umbrella_brief, umbrella_product)
    sb2 = build_storyboard(umbrella_brief, umbrella_product)
    # Same number of scenes, same durations, same purposes
    assert len(sb1.scenes) == len(sb2.scenes)
    for s1, s2 in zip(sb1.scenes, sb2.scenes):
        assert s1.duration_s == s2.duration_s
        assert s1.purpose == s2.purpose


# ---------------------------------------------------------------------------
# Seed derivation
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_derive_seed_is_positive_int(
    umbrella_brief, umbrella_product: ShopeeProduct  # type: ignore[no-untyped-def]
) -> None:
    seed = _derive_seed(umbrella_brief, umbrella_product)
    assert isinstance(seed, int)
    assert seed >= 0


@pytest.mark.unit
def test_derive_seed_is_deterministic(
    umbrella_brief, umbrella_product: ShopeeProduct  # type: ignore[no-untyped-def]
) -> None:
    s1 = _derive_seed(umbrella_brief, umbrella_product)
    s2 = _derive_seed(umbrella_brief, umbrella_product)
    assert s1 == s2


@pytest.mark.unit
def test_different_products_different_seeds(
    umbrella_brief, umbrella_product: ShopeeProduct, sunscreen_product: ShopeeProduct  # type: ignore[no-untyped-def]
) -> None:
    sunscreen_brief = build_brief(sunscreen_product)
    s1 = _derive_seed(umbrella_brief, umbrella_product)
    s2 = _derive_seed(sunscreen_brief, sunscreen_product)
    assert s1 != s2
