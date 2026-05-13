"""Tests for the Wiki tier promotion logic (AFFI-T-026)."""

from __future__ import annotations

import pytest

from auto_affi.wiki.entry import WikiEntry, WikiNamespace, WikiTier
from auto_affi.wiki.tier_promoter import TierPromoter, TierThresholds


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def _make_entry(
    slug: str = "test-entry",
    tier: WikiTier = WikiTier.HYPOTHESIS,
    evidence_count: int = 1,
) -> WikiEntry:
    return WikiEntry(
        slug=slug,
        namespace=WikiNamespace.HOOK_PATTERN,
        tier=tier,
        title="Test entry",
        summary="Test summary for tier promotion tests",
        evidence_ids=[f"ev-{i}" for i in range(evidence_count)],
    )


# ------------------------------------------------------------------ #
# Tier promotion tests                                                #
# ------------------------------------------------------------------ #


class TestTierPromoter:
    """TierPromoter.evaluate() and add_evidence()."""

    @pytest.mark.unit
    def test_hypothesis_stays_below_threshold(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(evidence_count=3)
        result = promoter.evaluate(entry)
        assert result.tier is WikiTier.HYPOTHESIS

    @pytest.mark.unit
    def test_hypothesis_to_validated(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(evidence_count=5)
        result = promoter.evaluate(entry)
        assert result.tier is WikiTier.VALIDATED

    @pytest.mark.unit
    def test_hypothesis_to_canonical_directly(self) -> None:
        """If evidence >= 20 and starting at Hypothesis, jump to Canonical."""
        promoter = TierPromoter()
        entry = _make_entry(evidence_count=20)
        result = promoter.evaluate(entry)
        assert result.tier is WikiTier.CANONICAL

    @pytest.mark.unit
    def test_validated_to_canonical(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(tier=WikiTier.VALIDATED, evidence_count=20)
        result = promoter.evaluate(entry)
        assert result.tier is WikiTier.CANONICAL

    @pytest.mark.unit
    def test_canonical_stays_canonical(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(tier=WikiTier.CANONICAL, evidence_count=25)
        result = promoter.evaluate(entry)
        assert result.tier is WikiTier.CANONICAL

    @pytest.mark.unit
    def test_deprecated_stays_deprecated(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(tier=WikiTier.DEPRECATED, evidence_count=30)
        result = promoter.evaluate(entry)
        assert result.tier is WikiTier.DEPRECATED

    @pytest.mark.unit
    def test_deprecation_overrides_promotion(self) -> None:
        """Contradictions cause deprecation even on high-evidence entries."""
        promoter = TierPromoter()
        entry = _make_entry(tier=WikiTier.VALIDATED, evidence_count=25)
        result = promoter.evaluate(entry, contradiction_count=3)
        assert result.tier is WikiTier.DEPRECATED
        assert result.deprecated_at is not None

    @pytest.mark.unit
    def test_deprecation_threshold_below(self) -> None:
        """2 contradictions is below the threshold (3)."""
        promoter = TierPromoter()
        entry = _make_entry(tier=WikiTier.VALIDATED, evidence_count=10)
        result = promoter.evaluate(entry, contradiction_count=2)
        assert result.tier is WikiTier.VALIDATED

    @pytest.mark.unit
    def test_even_canonical_can_be_deprecated(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(tier=WikiTier.CANONICAL, evidence_count=30)
        result = promoter.evaluate(entry, contradiction_count=5)
        assert result.tier is WikiTier.DEPRECATED

    @pytest.mark.unit
    def test_custom_thresholds(self) -> None:
        promoter = TierPromoter(
            thresholds=TierThresholds(
                validated_evidence=3,
                canonical_evidence=10,
                deprecation_contradictions=2,
            )
        )
        entry = _make_entry(evidence_count=3)
        result = promoter.evaluate(entry)
        assert result.tier is WikiTier.VALIDATED


# ------------------------------------------------------------------ #
# add_evidence tests                                                   #
# ------------------------------------------------------------------ #


class TestAddEvidence:
    """TierPromoter.add_evidence() merging and re-evaluation."""

    @pytest.mark.unit
    def test_add_evidence_promotes(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(evidence_count=3)
        result = promoter.add_evidence(entry, [f"new-{i}" for i in range(3)])
        # 3 existing + 3 new = 6 >= 5 threshold -> Validated
        assert result.tier is WikiTier.VALIDATED
        assert len(result.evidence_ids) == 6

    @pytest.mark.unit
    def test_add_evidence_deduplicates(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(evidence_count=3)
        # Add duplicates of existing evidence
        result = promoter.add_evidence(entry, ["ev-0", "ev-1", "new-0"])
        assert len(result.evidence_ids) == 4  # 3 original + 1 new

    @pytest.mark.unit
    def test_add_evidence_with_contradictions(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(evidence_count=10)
        result = promoter.add_evidence(
            entry, ["new-0"], contradiction_count=3
        )
        assert result.tier is WikiTier.DEPRECATED


# ------------------------------------------------------------------ #
# can_promote tests                                                    #
# ------------------------------------------------------------------ #


class TestCanPromote:
    """TierPromoter.can_promote() predicate."""

    @pytest.mark.unit
    def test_can_promote_true(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(evidence_count=5)
        assert promoter.can_promote(entry) is True

    @pytest.mark.unit
    def test_can_promote_false(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(evidence_count=2)
        assert promoter.can_promote(entry) is False

    @pytest.mark.unit
    def test_can_promote_deprecation(self) -> None:
        promoter = TierPromoter()
        entry = _make_entry(evidence_count=5)
        assert promoter.can_promote(entry, contradiction_count=3) is True
        # It "can promote" in the sense that the tier WOULD change (to Deprecated)
