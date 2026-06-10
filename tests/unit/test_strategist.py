"""Tests for src/auto_affi/agents/strategist.py.

All tests are deterministic offline — no network, no LLM, no Anthropic.
"""

from __future__ import annotations

import re
from datetime import date

import pytest

from auto_affi.adapters.shopee import ShopeeProduct, get_fixture_products
from auto_affi.agents.strategist import build_brief, is_mega_sale_window
from auto_affi.schemas.campaign_brief import BriefStatus, CampaignBrief

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def umbrella_product() -> ShopeeProduct:
    """Rainy-season umbrella — triggers rainy-season-must-have template."""
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
    """Skincare / beauty product — triggers beauty-result-reveal template."""
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
def gadget_product() -> ShopeeProduct:
    """Waterproof gadget pouch — triggers everyday-hero-gadget template."""
    return ShopeeProduct(
        item_id=10000002,
        shop_id=500002,
        name="ซองใส่โทรศัพท์กันน้ำ กระเป๋าคาดเอว 2-in-1",
        price_min=89.0,
        price_max=149.0,
        commission_rate=0.08,
        rating_star=4.7,
        sales=1850,
    )


# ---------------------------------------------------------------------------
# Schema validity
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_brief_is_campaign_brief_instance(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert isinstance(brief, CampaignBrief)


@pytest.mark.unit
def test_brief_schema_valid_all_fixtures() -> None:
    """Every fixture product must produce a schema-valid brief without raising."""
    for product in get_fixture_products():
        brief = build_brief(product)
        assert isinstance(brief, CampaignBrief)


@pytest.mark.unit
def test_expected_ctr_within_bounds(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert 0.0 <= brief.expected_ctr <= 0.15


@pytest.mark.unit
def test_confidence_within_bounds(sunscreen_product: ShopeeProduct) -> None:
    brief = build_brief(sunscreen_product)
    assert 0.0 <= brief.confidence <= 1.0


@pytest.mark.unit
def test_hook_template_slug_matches_pattern(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert re.match(r"^[a-z0-9_-]+$", brief.hook_template_slug), (
        f"hook_template_slug {brief.hook_template_slug!r} does not match ^[a-z0-9_-]+$"
    )


@pytest.mark.unit
def test_persona_age_range_pattern(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert re.match(r"^\d{1,2}-\d{1,2}$", brief.persona.age_range), (
        f"age_range {brief.persona.age_range!r} does not match pattern"
    )


@pytest.mark.unit
def test_persona_pain_points_at_least_one(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert len(brief.persona.pain_points) >= 1
    assert len(brief.persona.pain_points) <= 5


@pytest.mark.unit
def test_cta_text_non_empty(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert len(brief.cta.text_th) >= 1
    assert len(brief.cta.text_th) <= 80


@pytest.mark.unit
def test_angle_length(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert 1 <= len(brief.angle) <= 200


@pytest.mark.unit
def test_hypothesis_length(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert 1 <= len(brief.hypothesis) <= 300


@pytest.mark.unit
def test_status_is_proposed_by_default(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert brief.status == BriefStatus.PROPOSED


@pytest.mark.unit
def test_product_id_and_shop_id_propagated(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert brief.product_id == umbrella_product.item_id
    assert brief.shop_id == umbrella_product.shop_id


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_build_brief_is_deterministic(umbrella_product: ShopeeProduct) -> None:
    """Same product must yield same slug/angle/ctr on repeated calls."""
    b1 = build_brief(umbrella_product)
    b2 = build_brief(umbrella_product)
    assert b1.hook_template_slug == b2.hook_template_slug
    assert b1.angle == b2.angle
    assert b1.expected_ctr == b2.expected_ctr
    assert b1.confidence == b2.confidence


@pytest.mark.unit
def test_different_products_may_differ(
    umbrella_product: ShopeeProduct,
    sunscreen_product: ShopeeProduct,
) -> None:
    """Umbrella and sunscreen have different keyword profiles → different slugs."""
    b_umbrella = build_brief(umbrella_product)
    b_sunscreen = build_brief(sunscreen_product)
    # They may share templates by coincidence, but slug should differ here
    assert b_umbrella.hook_template_slug != b_sunscreen.hook_template_slug


# ---------------------------------------------------------------------------
# Template routing
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_umbrella_uses_rainy_season_template(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert brief.hook_template_slug == "rainy-season-must-have"


@pytest.mark.unit
def test_sunscreen_uses_beauty_template(sunscreen_product: ShopeeProduct) -> None:
    brief = build_brief(sunscreen_product)
    assert brief.hook_template_slug == "beauty-result-reveal"


@pytest.mark.unit
def test_gadget_uses_everyday_hero_template(gadget_product: ShopeeProduct) -> None:
    brief = build_brief(gadget_product)
    assert brief.hook_template_slug == "everyday-hero-gadget"


# ---------------------------------------------------------------------------
# Mega-sale window
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_priority_boost_on_1111(umbrella_product: ShopeeProduct) -> None:
    """Date 7 days before 11.11 → priority_boost=True."""
    brief = build_brief(umbrella_product, today=date(2026, 11, 4))
    assert brief.priority_boost is True


@pytest.mark.unit
def test_no_priority_boost_outside_window(umbrella_product: ShopeeProduct) -> None:
    """Date far from any mega sale → priority_boost=False."""
    brief = build_brief(umbrella_product, today=date(2026, 3, 20))
    assert brief.priority_boost is False


@pytest.mark.unit
def test_is_mega_sale_window_day_of() -> None:
    """Exactly on a mega-sale date → True."""
    assert is_mega_sale_window(today=date(2026, 11, 11)) is True


@pytest.mark.unit
def test_is_mega_sale_window_14_days_before() -> None:
    """14 days before → still within window."""
    assert is_mega_sale_window(today=date(2026, 10, 28)) is True


@pytest.mark.unit
def test_is_mega_sale_window_15_days_before() -> None:
    """15 days before → outside window."""
    assert is_mega_sale_window(today=date(2026, 10, 27)) is False


# ---------------------------------------------------------------------------
# Scout score integration
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_scout_score_high_bumps_ctr(umbrella_product: ShopeeProduct) -> None:
    brief_low = build_brief(umbrella_product, scout_score=0.1)
    brief_high = build_brief(umbrella_product, scout_score=0.9)
    # High scout score should yield equal or higher CTR
    assert brief_high.expected_ctr >= brief_low.expected_ctr


@pytest.mark.unit
def test_scout_score_high_still_within_bounds(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product, scout_score=1.0)
    assert brief.expected_ctr <= 0.15


@pytest.mark.unit
def test_wiki_evidence_slugs_contains_template_slug(umbrella_product: ShopeeProduct) -> None:
    brief = build_brief(umbrella_product)
    assert brief.hook_template_slug in brief.wiki_evidence_slugs
