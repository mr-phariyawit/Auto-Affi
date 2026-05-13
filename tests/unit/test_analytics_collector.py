"""Tests for the Analytics Collector agent (AFFI-T-022/023/024)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from auto_affi.agents.analytics_collector import (
    AnalyticsCollector,
    DryRunConversionTransport,
    DryRunMetricsTransport,
    attribute_conversions,
    label_outcome,
)
from auto_affi.schemas.metrics import (
    ConversionReport,
    MetricsSnapshot,
    OutcomeLabel,
    OutcomeThresholds,
    PollSchedule,
)


# ------------------------------------------------------------------ #
# MetricsSnapshot schema tests (T-022)                                #
# ------------------------------------------------------------------ #


class TestMetricsSnapshot:
    """MetricsSnapshot schema validation."""

    @pytest.mark.unit
    def test_valid_snapshot(self) -> None:
        snap = MetricsSnapshot(
            publish_record_id="pub-001",
            schedule=PollSchedule.HOUR_1,
            views=100,
            likes=5,
            ctr=0.02,
        )
        assert snap.views == 100
        assert snap.schedule == PollSchedule.HOUR_1

    @pytest.mark.unit
    def test_defaults_to_zero(self) -> None:
        snap = MetricsSnapshot(
            publish_record_id="pub-002",
            schedule=PollSchedule.DAY_7,
        )
        assert snap.views == 0
        assert snap.ctr == 0.0
        assert snap.gmv_thb == 0.0

    @pytest.mark.unit
    def test_rejects_negative_views(self) -> None:
        with pytest.raises(ValueError):
            MetricsSnapshot(
                publish_record_id="pub-003",
                schedule=PollSchedule.HOUR_1,
                views=-1,
            )

    @pytest.mark.unit
    def test_rejects_ctr_above_one(self) -> None:
        with pytest.raises(ValueError):
            MetricsSnapshot(
                publish_record_id="pub-004",
                schedule=PollSchedule.HOUR_1,
                ctr=1.5,
            )

    @pytest.mark.unit
    def test_all_poll_schedules_valid(self) -> None:
        for sched in PollSchedule:
            snap = MetricsSnapshot(
                publish_record_id="pub-005",
                schedule=sched,
            )
            assert snap.schedule == sched


# ------------------------------------------------------------------ #
# OutcomeThresholds tests (T-023)                                     #
# ------------------------------------------------------------------ #


class TestOutcomeThresholds:
    """OutcomeThresholds validation."""

    @pytest.mark.unit
    def test_defaults_valid(self) -> None:
        t = OutcomeThresholds()
        assert t.breakout_views > t.hit_views > t.flop_views

    @pytest.mark.unit
    def test_rejects_inverted_thresholds(self) -> None:
        with pytest.raises(ValueError, match="hit_views must be < breakout_views"):
            OutcomeThresholds(breakout_views=100, hit_views=200)

    @pytest.mark.unit
    def test_rejects_flop_above_hit(self) -> None:
        with pytest.raises(ValueError, match="flop_views must be < hit_views"):
            OutcomeThresholds(
                breakout_views=50000,
                hit_views=1000,
                flop_views=2000,
            )


# ------------------------------------------------------------------ #
# Outcome labeling tests (T-023)                                      #
# ------------------------------------------------------------------ #


class TestOutcomeLabeling:
    """label_outcome() classification logic."""

    @pytest.mark.unit
    def test_empty_snapshots_returns_flop(self) -> None:
        assert label_outcome([]) is OutcomeLabel.FLOP

    @pytest.mark.unit
    def test_breakout(self) -> None:
        snap = MetricsSnapshot(
            publish_record_id="p1",
            schedule=PollSchedule.DAY_7,
            views=60_000,
            ctr=0.08,
        )
        assert label_outcome([snap]) is OutcomeLabel.BREAKOUT

    @pytest.mark.unit
    def test_hit(self) -> None:
        snap = MetricsSnapshot(
            publish_record_id="p1",
            schedule=PollSchedule.DAY_7,
            views=15_000,
            ctr=0.01,  # below breakout_ctr
        )
        assert label_outcome([snap]) is OutcomeLabel.HIT

    @pytest.mark.unit
    def test_flop(self) -> None:
        snap = MetricsSnapshot(
            publish_record_id="p1",
            schedule=PollSchedule.DAY_7,
            views=200,
            ctr=0.01,
        )
        assert label_outcome([snap]) is OutcomeLabel.FLOP

    @pytest.mark.unit
    def test_neutral(self) -> None:
        snap = MetricsSnapshot(
            publish_record_id="p1",
            schedule=PollSchedule.DAY_7,
            views=3_000,
            ctr=0.01,
        )
        assert label_outcome([snap]) is OutcomeLabel.NEUTRAL

    @pytest.mark.unit
    def test_banned_zero_views_with_24h_poll(self) -> None:
        snapshots = [
            MetricsSnapshot(
                publish_record_id="p1",
                schedule=PollSchedule.HOUR_1,
                views=0,
            ),
            MetricsSnapshot(
                publish_record_id="p1",
                schedule=PollSchedule.HOUR_24,
                views=0,
            ),
        ]
        assert label_outcome(snapshots) is OutcomeLabel.BANNED

    @pytest.mark.unit
    def test_zero_views_without_24h_not_banned(self) -> None:
        """Zero views at 1h poll is too early to call banned."""
        snap = MetricsSnapshot(
            publish_record_id="p1",
            schedule=PollSchedule.HOUR_1,
            views=0,
        )
        assert label_outcome([snap]) is OutcomeLabel.FLOP

    @pytest.mark.unit
    def test_uses_latest_snapshot(self) -> None:
        """label_outcome should use the most recent snapshot by timestamp."""
        old = MetricsSnapshot(
            publish_record_id="p1",
            schedule=PollSchedule.HOUR_1,
            views=100,
            ctr=0.01,
            ts=datetime(2026, 5, 1, tzinfo=UTC),
        )
        new = MetricsSnapshot(
            publish_record_id="p1",
            schedule=PollSchedule.DAY_7,
            views=60_000,
            ctr=0.08,
            ts=datetime(2026, 5, 8, tzinfo=UTC),
        )
        assert label_outcome([old, new]) is OutcomeLabel.BREAKOUT

    @pytest.mark.unit
    def test_custom_thresholds(self) -> None:
        t = OutcomeThresholds(
            breakout_views=1000,
            hit_views=500,
            flop_views=100,
            breakout_ctr=0.03,
        )
        snap = MetricsSnapshot(
            publish_record_id="p1",
            schedule=PollSchedule.DAY_7,
            views=1200,
            ctr=0.04,
        )
        assert label_outcome([snap], thresholds=t) is OutcomeLabel.BREAKOUT


# ------------------------------------------------------------------ #
# Conversion attribution tests (T-024)                                #
# ------------------------------------------------------------------ #


class TestConversionAttribution:
    """attribute_conversions() join logic."""

    @pytest.mark.unit
    def test_basic_join(self) -> None:
        sub_ids = [
            {"sub_id": "s1", "video_id": "v1", "publish_record_id": "p1"},
            {"sub_id": "s2", "video_id": "v2", "publish_record_id": "p2"},
        ]
        conversions = [
            {"sub_id": "s1", "clicks": 100, "conversions": 5, "gmv_thb": 1750.0},
            {"sub_id": "s2", "clicks": 50, "conversions": 2, "gmv_thb": 700.0},
        ]
        results = attribute_conversions(sub_ids, conversions)
        assert len(results) == 2
        assert results[0].video_id == "v1"
        assert results[0].clicks == 100
        assert results[0].conversion_rate == pytest.approx(0.05)

    @pytest.mark.unit
    def test_unmatched_conversions_skipped(self) -> None:
        sub_ids = [
            {"sub_id": "s1", "video_id": "v1", "publish_record_id": "p1"},
        ]
        conversions = [
            {"sub_id": "s99", "clicks": 10, "conversions": 1, "gmv_thb": 350.0},
        ]
        results = attribute_conversions(sub_ids, conversions)
        assert len(results) == 0

    @pytest.mark.unit
    def test_zero_clicks_rate_zero(self) -> None:
        sub_ids = [
            {"sub_id": "s1", "video_id": "v1", "publish_record_id": "p1"},
        ]
        conversions = [
            {"sub_id": "s1", "clicks": 0, "conversions": 0, "gmv_thb": 0.0},
        ]
        results = attribute_conversions(sub_ids, conversions)
        assert len(results) == 1
        assert results[0].conversion_rate == 0.0

    @pytest.mark.unit
    def test_empty_inputs(self) -> None:
        assert attribute_conversions([], []) == []


# ------------------------------------------------------------------ #
# ConversionReport schema tests (T-024)                               #
# ------------------------------------------------------------------ #


class TestConversionReport:
    """ConversionReport schema validation."""

    @pytest.mark.unit
    def test_auto_compute_rate(self) -> None:
        report = ConversionReport(
            video_id="v1",
            publish_record_id="p1",
            clicks=100,
            conversions=5,
            gmv_thb=1750.0,
        )
        assert report.conversion_rate == pytest.approx(0.05)

    @pytest.mark.unit
    def test_explicit_rate_preserved(self) -> None:
        report = ConversionReport(
            video_id="v1",
            publish_record_id="p1",
            clicks=100,
            conversions=5,
            gmv_thb=1750.0,
            conversion_rate=0.10,
        )
        assert report.conversion_rate == pytest.approx(0.10)


# ------------------------------------------------------------------ #
# AnalyticsCollector integration tests (T-022/023)                    #
# ------------------------------------------------------------------ #


class TestAnalyticsCollector:
    """AnalyticsCollector with DryRunTransport."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_collect_returns_snapshot(self) -> None:
        collector = AnalyticsCollector(transport=DryRunMetricsTransport())
        result = await collector.collect("pub-001", PollSchedule.HOUR_1)
        assert result.ok
        assert result.data is not None
        assert result.data.publish_record_id == "pub-001"
        assert result.data.views > 0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_collect_accumulates_history(self) -> None:
        collector = AnalyticsCollector(transport=DryRunMetricsTransport())
        await collector.collect("pub-001", PollSchedule.HOUR_1)
        await collector.collect("pub-001", PollSchedule.DAY_7)
        history = collector.get_history("pub-001")
        assert len(history) == 2

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_outcome_after_collection(self) -> None:
        transport = DryRunMetricsTransport(base_views=60_000, base_ctr=0.08)
        collector = AnalyticsCollector(transport=transport)
        await collector.collect("pub-001", PollSchedule.DAY_7)
        outcome = collector.get_outcome("pub-001")
        assert outcome is OutcomeLabel.BREAKOUT

    @pytest.mark.unit
    def test_outcome_no_history_returns_flop(self) -> None:
        collector = AnalyticsCollector(transport=DryRunMetricsTransport())
        assert collector.get_outcome("nonexistent") is OutcomeLabel.FLOP

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_schedule_multipliers(self) -> None:
        """Later schedules should return higher view counts."""
        transport = DryRunMetricsTransport(base_views=10_000)
        collector = AnalyticsCollector(transport=transport)
        r1 = await collector.collect("pub-001", PollSchedule.HOUR_1)
        r7 = await collector.collect("pub-001", PollSchedule.DAY_7)
        assert r1.data is not None and r7.data is not None
        assert r7.data.views > r1.data.views

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_attribution_integration(self) -> None:
        collector = AnalyticsCollector(transport=DryRunMetricsTransport())
        sub_ids = [
            {"sub_id": "s1", "video_id": "v1", "publish_record_id": "p1"},
        ]
        conversions = [
            {"sub_id": "s1", "clicks": 80, "conversions": 4, "gmv_thb": 1400.0},
        ]
        results = await collector.attribute(sub_ids, conversions)
        assert len(results) == 1
        assert results[0].video_id == "v1"
