"""Unit tests for the wiki saturation checker (FR-SC-04)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from auto_affi.wiki.saturation import SaturationChecker, SaturationResult


@pytest.fixture
def checker() -> SaturationChecker:
    return SaturationChecker(
        product_threshold=3,
        category_threshold=5,
        window_days=7,
    )


@pytest.mark.unit
def test_fresh_product_is_not_saturated(checker: SaturationChecker) -> None:
    result = checker.check(product_id=100, category="beauty_skincare")
    assert result.is_saturated is False
    assert result.product_count_7d == 0
    assert result.category_count_7d == 0
    assert result.reason is None


@pytest.mark.unit
def test_product_saturated_after_threshold(checker: SaturationChecker) -> None:
    for _ in range(3):
        checker.record_promotion(product_id=100, category="beauty_skincare")

    result = checker.check(product_id=100, category="beauty_skincare")
    assert result.is_saturated is True
    assert result.product_count_7d == 3
    assert "Product promoted 3x" in (result.reason or "")


@pytest.mark.unit
def test_category_saturated_after_threshold(checker: SaturationChecker) -> None:
    # 5 different products in the same category
    for i in range(5):
        checker.record_promotion(product_id=200 + i, category="gadgets_accessories")

    result = checker.check(product_id=999, category="gadgets_accessories")
    assert result.is_saturated is True
    assert result.category_count_7d == 5
    assert "gadgets_accessories" in (result.reason or "")


@pytest.mark.unit
def test_different_category_not_affected(checker: SaturationChecker) -> None:
    for _ in range(4):
        checker.record_promotion(product_id=300, category="beauty_skincare")

    result = checker.check(product_id=400, category="home")
    assert result.is_saturated is False
    assert result.category_count_7d == 0


@pytest.mark.unit
def test_old_records_outside_window(checker: SaturationChecker) -> None:
    old_time = datetime.now(UTC) - timedelta(days=8)
    checker._records.append(
        __import__("auto_affi.wiki.saturation", fromlist=["PromotionRecord"]).PromotionRecord(
            product_id=500, category="beauty_skincare", promoted_at=old_time
        )
    )

    result = checker.check(product_id=500, category="beauty_skincare")
    assert result.is_saturated is False
    assert result.product_count_7d == 0


@pytest.mark.unit
def test_filter_candidates_splits_correctly(checker: SaturationChecker) -> None:
    # Saturate product 100
    for _ in range(3):
        checker.record_promotion(product_id=100, category="beauty_skincare")

    candidates = [(100, "beauty_skincare"), (200, "beauty_skincare"), (300, "home")]
    accepted, saturated = checker.filter_candidates(candidates)

    assert len(accepted) == 2
    assert len(saturated) == 1
    assert saturated[0].product_id == 100


@pytest.mark.unit
def test_filter_candidates_empty_list() -> None:
    checker = SaturationChecker()
    accepted, saturated = checker.filter_candidates([])
    assert accepted == []
    assert saturated == []


@pytest.mark.unit
def test_prune_old_removes_expired(checker: SaturationChecker) -> None:
    from auto_affi.wiki.saturation import PromotionRecord

    old_time = datetime.now(UTC) - timedelta(days=10)
    recent_time = datetime.now(UTC) - timedelta(days=1)

    checker._records = [
        PromotionRecord(product_id=1, category="a", promoted_at=old_time),
        PromotionRecord(product_id=2, category="b", promoted_at=old_time),
        PromotionRecord(product_id=3, category="c", promoted_at=recent_time),
    ]

    removed = checker.prune_old()
    assert removed == 2
    assert len(checker._records) == 1
    assert checker._records[0].product_id == 3


@pytest.mark.unit
def test_below_threshold_not_saturated(checker: SaturationChecker) -> None:
    # 2 promotions (below threshold of 3)
    checker.record_promotion(product_id=100, category="beauty_skincare")
    checker.record_promotion(product_id=100, category="beauty_skincare")

    result = checker.check(product_id=100, category="beauty_skincare")
    assert result.is_saturated is False
    assert result.product_count_7d == 2


@pytest.mark.unit
def test_category_saturation_counts_all_products_in_category(
    checker: SaturationChecker,
) -> None:
    # 4 different products + our candidate = 5 total in category
    for i in range(4):
        checker.record_promotion(product_id=600 + i, category="fashion")
    checker.record_promotion(product_id=700, category="fashion")

    result = checker.check(product_id=999, category="fashion")
    assert result.is_saturated is True
    assert result.category_count_7d == 5
