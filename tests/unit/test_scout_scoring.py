"""Unit tests for the Scout scoring rubric."""

from __future__ import annotations

import pytest

from auto_affi.agents.scout_scoring import (
    RESTRICTED_CATEGORIES,
    RejectReason,
    ScoutInput,
    score,
)


def _strong_beauty() -> ScoutInput:
    """A high-scoring beauty product baseline used across several tests."""
    return ScoutInput(
        category="beauty_skincare",
        commission_rate=0.08,
        aov_thb=350.0,
        shop_rating=4.8,
        review_count=10_000,
        sales_velocity_7d=120,
        tiktok_mention_growth_7d=0.5,
        saturation_count_7d=1,
        shop_catalog_size=500,
    )


@pytest.mark.unit
def test_strong_beauty_candidate_scores_high() -> None:
    result = score(_strong_beauty())
    assert result.rejected is False
    # Commission EV caps at THB 200, so a typical-AOV beauty product cannot
    # max the score; 0.25 is the empirical floor for a "strong" candidate.
    assert result.score > 0.25
    assert set(result.breakdown.keys()) == {
        "commission_ev",
        "cr_signal",
        "trend_momentum",
        "saturation",
        "return_penalty",
        "cookie_utilisation",
        "raw_weighted_sum",
    }


@pytest.mark.unit
@pytest.mark.parametrize("category", sorted(RESTRICTED_CATEGORIES))
def test_restricted_categories_rejected(category: str) -> None:
    candidate = ScoutInput(
        category=category,
        commission_rate=0.10,
        aov_thb=500.0,
        shop_rating=4.9,
        review_count=5_000,
    )
    result = score(candidate)
    assert result.rejected is True
    assert result.reject_reason is RejectReason.RESTRICTED_CATEGORY


@pytest.mark.unit
def test_low_shop_rating_rejected() -> None:
    candidate = ScoutInput(
        category="beauty_skincare",
        commission_rate=0.10,
        aov_thb=500.0,
        shop_rating=4.4,
        review_count=1_000,
    )
    result = score(candidate)
    assert result.rejected is True
    assert result.reject_reason is RejectReason.LOW_SHOP_RATING


@pytest.mark.unit
def test_low_commission_and_low_aov_rejected() -> None:
    candidate = ScoutInput(
        category="home",
        commission_rate=0.02,
        aov_thb=150.0,
        shop_rating=4.8,
        review_count=200,
    )
    result = score(candidate)
    assert result.rejected is True
    assert result.reject_reason is RejectReason.LOW_COMMISSION_AND_AOV


@pytest.mark.unit
def test_low_commission_high_aov_passes_filter() -> None:
    # Cheap commission but premium AOV still produces real money per click.
    candidate = ScoutInput(
        category="beauty_skincare",
        commission_rate=0.025,
        aov_thb=2_500.0,
        shop_rating=4.7,
        review_count=800,
    )
    result = score(candidate)
    assert result.rejected is False


@pytest.mark.unit
def test_saturation_drops_score() -> None:
    base = score(_strong_beauty()).score
    saturated = _strong_beauty()
    candidate = ScoutInput(
        category=saturated.category,
        commission_rate=saturated.commission_rate,
        aov_thb=saturated.aov_thb,
        shop_rating=saturated.shop_rating,
        review_count=saturated.review_count,
        sales_velocity_7d=saturated.sales_velocity_7d,
        tiktok_mention_growth_7d=saturated.tiktok_mention_growth_7d,
        saturation_count_7d=10,
        shop_catalog_size=saturated.shop_catalog_size,
    )
    assert score(candidate).score < base


@pytest.mark.unit
def test_fashion_return_penalty_lower_than_beauty() -> None:
    fashion = ScoutInput(
        category="fashion",
        commission_rate=0.10,
        aov_thb=400.0,
        shop_rating=4.8,
        review_count=5_000,
        sales_velocity_7d=80,
    )
    beauty = ScoutInput(
        category="beauty_skincare",
        commission_rate=0.10,
        aov_thb=400.0,
        shop_rating=4.8,
        review_count=5_000,
        sales_velocity_7d=80,
    )
    assert score(fashion).score < score(beauty).score


@pytest.mark.unit
def test_score_clamped_to_unit_interval() -> None:
    # Push every positive lever to its cap; even then score must be <= 1.0.
    candidate = ScoutInput(
        category="beauty_skincare",
        commission_rate=1.0,
        aov_thb=1_000.0,
        shop_rating=5.0,
        review_count=1_000_000,
        sales_velocity_7d=10_000,
        tiktok_mention_growth_7d=10.0,
        saturation_count_7d=0,
        shop_catalog_size=100_000,
    )
    result = score(candidate)
    assert 0.0 <= result.score <= 1.0


@pytest.mark.unit
def test_unknown_category_uses_default_prior() -> None:
    # Category we don't know yet should still pass filters when rating &
    # commission are healthy, and produce a non-zero score.
    candidate = ScoutInput(
        category="emerging_niche_xyz",
        commission_rate=0.06,
        aov_thb=400.0,
        shop_rating=4.7,
        review_count=500,
        sales_velocity_7d=50,
    )
    result = score(candidate)
    assert result.rejected is False
    assert result.score > 0.0
