"""Tests for the Feedback Curator agent (AFFI-T-025)."""

from __future__ import annotations

import pytest

from auto_affi.agents.feedback_curator import (
    ExtractedPattern,
    FeedbackCurator,
    OutcomeRecord,
    extract_patterns,
    split_cohorts,
)
from auto_affi.schemas.metrics import OutcomeLabel
from auto_affi.wiki.entry import WikiNamespace, WikiTier
from auto_affi.wiki.review_queue import ReviewQueue


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def _make_record(
    video_id: str,
    outcome: OutcomeLabel,
    views: int = 1000,
    ctr: float = 0.02,
    hook: str = "",
    category: str = "",
    hour: int = 12,
) -> OutcomeRecord:
    return OutcomeRecord(
        video_id=video_id,
        publish_record_id=f"pub-{video_id}",
        outcome=outcome,
        views=views,
        ctr=ctr,
        hook_template_slug=hook,
        product_category=category,
        posted_hour=hour,
    )


# ------------------------------------------------------------------ #
# Cohort splitting tests                                              #
# ------------------------------------------------------------------ #


class TestSplitCohorts:
    """split_cohorts() logic."""

    @pytest.mark.unit
    def test_basic_split(self) -> None:
        records = [
            _make_record("v1", OutcomeLabel.BREAKOUT, views=50000),
            _make_record("v2", OutcomeLabel.HIT, views=15000),
            _make_record("v3", OutcomeLabel.NEUTRAL, views=3000),
            _make_record("v4", OutcomeLabel.FLOP, views=200),
            _make_record("v5", OutcomeLabel.BANNED, views=0),
        ]
        wins, fails = split_cohorts(records)
        assert len(wins) >= 1
        assert len(fails) >= 1
        assert all(
            r.outcome in (OutcomeLabel.BREAKOUT, OutcomeLabel.HIT) for r in wins
        )
        assert all(
            r.outcome in (OutcomeLabel.FLOP, OutcomeLabel.BANNED) for r in fails
        )

    @pytest.mark.unit
    def test_no_wins(self) -> None:
        records = [
            _make_record("v1", OutcomeLabel.FLOP, views=100),
            _make_record("v2", OutcomeLabel.NEUTRAL, views=2000),
        ]
        wins, fails = split_cohorts(records)
        assert wins == []
        assert len(fails) >= 1

    @pytest.mark.unit
    def test_no_fails(self) -> None:
        records = [
            _make_record("v1", OutcomeLabel.BREAKOUT, views=50000),
            _make_record("v2", OutcomeLabel.NEUTRAL, views=3000),
        ]
        wins, fails = split_cohorts(records)
        assert len(wins) >= 1
        assert fails == []

    @pytest.mark.unit
    def test_wins_sorted_descending(self) -> None:
        records = [
            _make_record("v1", OutcomeLabel.HIT, views=10000),
            _make_record("v2", OutcomeLabel.BREAKOUT, views=80000),
            _make_record("v3", OutcomeLabel.BREAKOUT, views=60000),
        ]
        wins, _ = split_cohorts(records)
        assert wins[0].video_id == "v2"


# ------------------------------------------------------------------ #
# Pattern extraction tests                                            #
# ------------------------------------------------------------------ #


class TestPatternExtraction:
    """extract_patterns() logic."""

    @pytest.mark.unit
    def test_hook_pattern_detection(self) -> None:
        wins = [
            _make_record("v1", OutcomeLabel.BREAKOUT, hook="curiosity_gap"),
            _make_record("v2", OutcomeLabel.HIT, hook="curiosity_gap"),
            _make_record("v3", OutcomeLabel.HIT, hook="before_after"),
        ]
        fails = [
            _make_record("v4", OutcomeLabel.FLOP, hook="talking_head"),
            _make_record("v5", OutcomeLabel.FLOP, hook="talking_head"),
        ]
        patterns = extract_patterns(wins, fails)
        hook_patterns = [p for p in patterns if p.namespace == WikiNamespace.HOOK_PATTERN]
        anti_patterns = [p for p in patterns if p.namespace == WikiNamespace.ANTI_PATTERN]
        assert len(hook_patterns) >= 1
        assert any("curiosity_gap" in p.slug for p in hook_patterns)
        assert len(anti_patterns) >= 1
        assert any("talking_head" in p.slug for p in anti_patterns)

    @pytest.mark.unit
    def test_no_patterns_from_insufficient_data(self) -> None:
        wins = [_make_record("v1", OutcomeLabel.HIT, hook="x")]
        fails = [_make_record("v2", OutcomeLabel.FLOP, hook="y")]
        patterns = extract_patterns(wins, fails)
        # Need count >= 2 for a pattern to emerge
        hook_wins = [p for p in patterns if "hook-win" in p.slug]
        assert len(hook_wins) == 0

    @pytest.mark.unit
    def test_empty_cohorts(self) -> None:
        assert extract_patterns([], []) == []

    @pytest.mark.unit
    def test_posting_time_pattern(self) -> None:
        wins = [
            _make_record("v1", OutcomeLabel.HIT, hour=18),
            _make_record("v2", OutcomeLabel.BREAKOUT, hour=18),
            _make_record("v3", OutcomeLabel.HIT, hour=20),
        ]
        fails = [
            _make_record("v4", OutcomeLabel.FLOP, hour=6),
            _make_record("v5", OutcomeLabel.FLOP, hour=6),
        ]
        patterns = extract_patterns(wins, fails)
        time_patterns = [p for p in patterns if p.namespace == WikiNamespace.PLATFORM_NORM]
        assert len(time_patterns) >= 1


# ------------------------------------------------------------------ #
# ReviewQueue isolation tests (bilateral sync)                         #
# ------------------------------------------------------------------ #


class TestReviewQueueIsolation:
    """Review queue enforces bilateral wiki sync."""

    @pytest.mark.unit
    def test_submit_forces_hypothesis_tier(self) -> None:
        queue = ReviewQueue()
        from auto_affi.wiki.entry import WikiEntry

        entry = WikiEntry(
            slug="test-entry",
            namespace=WikiNamespace.HOOK_PATTERN,
            tier=WikiTier.CANONICAL,  # try to sneak in canonical
            title="Test",
            summary="Test summary",
        )
        item = queue.submit(entry)
        # Bilateral sync: forced to Hypothesis regardless of input
        assert item.entry.tier is WikiTier.HYPOTHESIS

    @pytest.mark.unit
    def test_approve_sets_tier(self) -> None:
        queue = ReviewQueue()
        from auto_affi.wiki.entry import WikiEntry

        entry = WikiEntry(
            slug="test-entry",
            namespace=WikiNamespace.HOOK_PATTERN,
            tier=WikiTier.HYPOTHESIS,
            title="Test",
            summary="Test summary",
        )
        queue.submit(entry)
        approved = queue.approve("test-entry", target_tier=WikiTier.VALIDATED)
        assert approved is not None
        assert approved.entry.tier is WikiTier.VALIDATED
        assert approved.status == "approved"

    @pytest.mark.unit
    def test_reject_with_reason(self) -> None:
        queue = ReviewQueue()
        from auto_affi.wiki.entry import WikiEntry

        entry = WikiEntry(
            slug="bad-pattern",
            namespace=WikiNamespace.ANTI_PATTERN,
            tier=WikiTier.HYPOTHESIS,
            title="Bad pattern",
            summary="This is wrong",
        )
        queue.submit(entry)
        rejected = queue.reject("bad-pattern", reason="Insufficient evidence")
        assert rejected is not None
        assert rejected.status == "rejected"
        assert rejected.rejection_reason == "Insufficient evidence"

    @pytest.mark.unit
    def test_approve_nonexistent_returns_none(self) -> None:
        queue = ReviewQueue()
        assert queue.approve("nonexistent") is None

    @pytest.mark.unit
    def test_pending_filters_correctly(self) -> None:
        queue = ReviewQueue()
        from auto_affi.wiki.entry import WikiEntry

        for i in range(3):
            entry = WikiEntry(
                slug=f"entry-{i}",
                namespace=WikiNamespace.HOOK_PATTERN,
                tier=WikiTier.HYPOTHESIS,
                title=f"Entry {i}",
                summary=f"Summary {i}",
            )
            queue.submit(entry)
        queue.approve("entry-0")
        queue.reject("entry-1", reason="bad")
        assert len(queue.pending()) == 1
        assert queue.pending()[0].entry.slug == "entry-2"


# ------------------------------------------------------------------ #
# FeedbackCurator integration tests                                    #
# ------------------------------------------------------------------ #


class TestFeedbackCurator:
    """FeedbackCurator end-to-end."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_curate_produces_entries(self) -> None:
        curator = FeedbackCurator()
        # Need enough records so that 20% cohorts have >= 2 members
        # 10 records * 20% = 2 per cohort minimum
        outcomes = [
            _make_record("v1", OutcomeLabel.BREAKOUT, views=50000, hook="curiosity_gap"),
            _make_record("v2", OutcomeLabel.HIT, views=15000, hook="curiosity_gap"),
            _make_record("v3", OutcomeLabel.HIT, views=12000, hook="curiosity_gap"),
            _make_record("v4", OutcomeLabel.HIT, views=11000, hook="before_after"),
            _make_record("v5", OutcomeLabel.NEUTRAL, views=3000),
            _make_record("v6", OutcomeLabel.NEUTRAL, views=2500),
            _make_record("v7", OutcomeLabel.FLOP, views=200, hook="talking_head"),
            _make_record("v8", OutcomeLabel.FLOP, views=150, hook="talking_head"),
            _make_record("v9", OutcomeLabel.FLOP, views=100, hook="talking_head"),
            _make_record("v10", OutcomeLabel.BANNED, views=0, hook="talking_head"),
        ]
        result = await curator.curate(outcomes)
        assert result.ok
        assert result.data is not None
        assert len(result.data) >= 1
        # All entries should be Hypothesis tier
        assert all(e.tier is WikiTier.HYPOTHESIS for e in result.data)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_curate_submits_to_queue(self) -> None:
        queue = ReviewQueue()
        curator = FeedbackCurator(review_queue=queue)
        # Need enough records for 20% cohorts to have >= 2 members with same hook
        outcomes = [
            _make_record("v1", OutcomeLabel.BREAKOUT, hook="test_hook"),
            _make_record("v2", OutcomeLabel.HIT, hook="test_hook"),
            _make_record("v3", OutcomeLabel.HIT, hook="test_hook"),
            _make_record("v4", OutcomeLabel.NEUTRAL),
            _make_record("v5", OutcomeLabel.NEUTRAL),
            _make_record("v6", OutcomeLabel.FLOP, hook="bad_hook"),
            _make_record("v7", OutcomeLabel.FLOP, hook="bad_hook"),
            _make_record("v8", OutcomeLabel.FLOP, hook="bad_hook"),
        ]
        await curator.curate(outcomes)
        assert len(queue.pending()) >= 1

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_curate_too_few_outcomes(self) -> None:
        curator = FeedbackCurator()
        result = await curator.curate([
            _make_record("v1", OutcomeLabel.HIT),
        ])
        assert result.ok
        assert result.data == []

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_curate_cost_is_zero_phase1(self) -> None:
        """Phase 1 curator uses no LLM calls — pure statistical."""
        curator = FeedbackCurator()
        outcomes = [
            _make_record("v1", OutcomeLabel.BREAKOUT, hook="a"),
            _make_record("v2", OutcomeLabel.HIT, hook="a"),
            _make_record("v3", OutcomeLabel.FLOP, hook="b"),
            _make_record("v4", OutcomeLabel.FLOP, hook="b"),
        ]
        result = await curator.curate(outcomes)
        assert result.cost_usd == 0.0
