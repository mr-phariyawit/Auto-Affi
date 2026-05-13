"""Tests for wiki canonical store + promotion pipeline (AFFI-T-027)."""

from __future__ import annotations

import pytest

from auto_affi.wiki.entry import WikiEntry, WikiNamespace, WikiTier
from auto_affi.wiki.review_queue import ReviewQueue
from auto_affi.wiki.store import WikiStore, promote_from_queue
from auto_affi.wiki.tier_promoter import TierPromoter


def _make_entry(slug: str, evidence_count: int = 1) -> WikiEntry:
    return WikiEntry(
        slug=slug,
        namespace=WikiNamespace.HOOK_PATTERN,
        tier=WikiTier.HYPOTHESIS,
        title=f"Entry {slug}",
        summary=f"Summary for {slug}",
        evidence_ids=[f"ev-{i}" for i in range(evidence_count)],
    )


class TestWikiStore:
    """WikiStore basic operations."""

    @pytest.mark.unit
    def test_empty_store(self) -> None:
        store = WikiStore()
        assert store.entry_count == 0
        assert store.get("nope") is None

    @pytest.mark.unit
    def test_get_by_namespace(self) -> None:
        store = WikiStore()
        entry = _make_entry("e1")
        store._put(
            entry,
            action="promoted",
            from_tier=WikiTier.HYPOTHESIS,
            reviewer="test",
        )
        results = store.get_by_namespace(WikiNamespace.HOOK_PATTERN)
        assert len(results) == 1
        assert results[0].slug == "e1"

    @pytest.mark.unit
    def test_get_active_excludes_deprecated(self) -> None:
        store = WikiStore()
        active = _make_entry("active")
        deprecated = _make_entry("deprecated").model_copy(
            update={"tier": WikiTier.DEPRECATED}
        )
        store._put(
            active,
            action="promoted",
            from_tier=WikiTier.HYPOTHESIS,
            reviewer="test",
        )
        store._put(
            deprecated,
            action="promoted",
            from_tier=WikiTier.HYPOTHESIS,
            reviewer="test",
        )
        assert len(store.get_active()) == 1

    @pytest.mark.unit
    def test_audit_log(self) -> None:
        store = WikiStore()
        store._put(
            _make_entry("e1"),
            action="promoted",
            from_tier=WikiTier.HYPOTHESIS,
            reviewer="human",
            reason="looks good",
        )
        assert len(store.audit_log) == 1
        assert store.audit_log[0].reviewer == "human"


class TestPromoteFromQueue:
    """Full promote pipeline: queue -> promoter -> store."""

    @pytest.mark.unit
    def test_promote_pipeline(self) -> None:
        queue = ReviewQueue()
        store = WikiStore()
        promoter = TierPromoter()

        # Submit entries with enough evidence for promotion
        queue.submit(_make_entry("e1", evidence_count=6))
        queue.submit(_make_entry("e2", evidence_count=2))

        promoted = promote_from_queue(queue, store, promoter)
        assert promoted == 2
        assert store.entry_count == 2

        # e1 should be Validated (6 evidence >= 5 threshold)
        e1 = store.get("e1")
        assert e1 is not None
        assert e1.tier is WikiTier.VALIDATED

        # e2 stays Hypothesis (2 evidence < 5 threshold)
        e2 = store.get("e2")
        assert e2 is not None
        assert e2.tier is WikiTier.HYPOTHESIS

    @pytest.mark.unit
    def test_promote_empty_queue(self) -> None:
        queue = ReviewQueue()
        store = WikiStore()
        promoter = TierPromoter()
        promoted = promote_from_queue(queue, store, promoter)
        assert promoted == 0

    @pytest.mark.unit
    def test_promote_audits_logged(self) -> None:
        queue = ReviewQueue()
        store = WikiStore()
        promoter = TierPromoter()
        queue.submit(_make_entry("e1", evidence_count=6))
        promote_from_queue(queue, store, promoter, reviewer="safety")
        assert len(store.audit_log) == 1
        assert store.audit_log[0].reviewer == "safety"
        assert store.audit_log[0].action == "promoted"

    @pytest.mark.unit
    def test_queue_cleared_after_promote(self) -> None:
        queue = ReviewQueue()
        store = WikiStore()
        promoter = TierPromoter()
        queue.submit(_make_entry("e1"))
        promote_from_queue(queue, store, promoter)
        assert len(queue.pending()) == 0
        assert len(queue.approved()) == 1
