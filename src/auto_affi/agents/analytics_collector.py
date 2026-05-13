"""Analytics Collector agent (FR-AN-01..03).

Polls platform metrics at configurable intervals, records full timeseries,
computes 7-day outcome labels, and performs click-to-conversion attribution
via the subId taxonomy.

Phase 1: dry-run transport with fixture data (no live API credentials).
Phase 2+: swap in real Meta Graph API + Shopee Affiliate API transports.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import ClassVar, Protocol

from auto_affi.schemas.metrics import (
    ConversionReport,
    MetricsSnapshot,
    OutcomeLabel,
    OutcomeThresholds,
    PollSchedule,
)
from auto_affi.schemas.tool_result import ToolResult

# ------------------------------------------------------------------ #
# Transport protocol                                                  #
# ------------------------------------------------------------------ #

class MetricsTransport(Protocol):
    """Pluggable transport for fetching platform metrics."""

    async def fetch_metrics(
        self,
        publish_record_id: str,
        schedule: PollSchedule,
    ) -> MetricsSnapshot: ...


class ConversionTransport(Protocol):
    """Pluggable transport for fetching Shopee conversion data."""

    async def fetch_conversions(
        self,
        video_id: str,
        publish_record_id: str,
    ) -> ConversionReport: ...


# ------------------------------------------------------------------ #
# Outcome labeling (FR-AN-02)                                        #
# ------------------------------------------------------------------ #

def label_outcome(
    snapshots: Sequence[MetricsSnapshot],
    *,
    thresholds: OutcomeThresholds | None = None,
) -> OutcomeLabel:
    """Classify a video's 7-day performance.

    Uses the latest snapshot in the sequence (assumed to be the most
    complete view of the video's lifetime metrics).  If the sequence is
    empty, returns FLOP as a safe default.

    Classification hierarchy (first match wins):
      1. ``banned`` — views == 0 AND the video was published >= 24h ago
         (platform likely removed it)
      2. ``breakout`` — views >= threshold AND ctr >= threshold
      3. ``hit`` — views >= threshold
      4. ``flop`` — views < threshold
      5. ``neutral`` — everything else
    """
    if not snapshots:
        return OutcomeLabel.FLOP

    t = thresholds or OutcomeThresholds()
    latest = max(snapshots, key=lambda s: s.ts)

    # Banned detection: zero views on a video that's been live long enough
    # to have at least the 24h poll.
    has_24h_poll = any(s.schedule == PollSchedule.HOUR_24 for s in snapshots)
    if latest.views == 0 and has_24h_poll:
        return OutcomeLabel.BANNED

    if latest.views >= t.breakout_views and latest.ctr >= t.breakout_ctr:
        return OutcomeLabel.BREAKOUT

    if latest.views >= t.hit_views:
        return OutcomeLabel.HIT

    if latest.views < t.flop_views:
        return OutcomeLabel.FLOP

    return OutcomeLabel.NEUTRAL


# ------------------------------------------------------------------ #
# Conversion attribution (FR-AN-03)                                   #
# ------------------------------------------------------------------ #

def attribute_conversions(
    sub_id_records: Sequence[dict[str, str]],
    conversion_reports: Sequence[dict[str, object]],
) -> list[ConversionReport]:
    """Join Shopee conversion data with video IDs via subId taxonomy.

    ``sub_id_records`` come from the link generator (AFFI-T-019) and
    contain at minimum ``video_id`` and ``sub_id`` keys.

    ``conversion_reports`` come from Shopee's conversionReport API and
    contain ``sub_id``, ``clicks``, ``conversions``, ``gmv_thb``.
    """
    # Build lookup: sub_id -> video_id
    sub_id_to_video: dict[str, str] = {}
    sub_id_to_publish: dict[str, str] = {}
    for rec in sub_id_records:
        sid = rec.get("sub_id", "")
        if sid:
            sub_id_to_video[sid] = rec.get("video_id", "")
            sub_id_to_publish[sid] = rec.get("publish_record_id", "")

    results: list[ConversionReport] = []
    for conv in conversion_reports:
        sid = str(conv.get("sub_id", ""))
        video_id = sub_id_to_video.get(sid)
        if not video_id:
            continue  # unmatched conversion — skip

        clicks = int(conv.get("clicks", 0))
        conversions = int(conv.get("conversions", 0))
        gmv = float(conv.get("gmv_thb", 0.0))
        rate = conversions / clicks if clicks > 0 else 0.0

        results.append(
            ConversionReport(
                video_id=video_id,
                publish_record_id=sub_id_to_publish.get(sid, ""),
                clicks=clicks,
                conversions=conversions,
                gmv_thb=gmv,
                conversion_rate=rate,
            )
        )

    return results


# ------------------------------------------------------------------ #
# Collector agent                                                     #
# ------------------------------------------------------------------ #

@dataclass
class AnalyticsCollector:
    """Collects platform metrics and computes outcomes.

    Instantiate with a :class:`MetricsTransport` (and optionally a
    :class:`ConversionTransport`).  Use the :class:`DryRunTransport`
    for development and CI.
    """

    transport: MetricsTransport
    conversion_transport: ConversionTransport | None = None
    thresholds: OutcomeThresholds = field(default_factory=OutcomeThresholds)
    _history: dict[str, list[MetricsSnapshot]] = field(
        default_factory=dict, init=False
    )

    async def collect(
        self,
        publish_record_id: str,
        schedule: PollSchedule,
    ) -> ToolResult[MetricsSnapshot]:
        """Poll metrics for a published video at the given schedule."""
        try:
            snapshot = await self.transport.fetch_metrics(
                publish_record_id, schedule
            )
        except Exception as err:
            return ToolResult(ok=False, error=str(err))

        self._history.setdefault(publish_record_id, []).append(snapshot)
        return ToolResult(ok=True, data=snapshot)

    def get_outcome(self, publish_record_id: str) -> OutcomeLabel:
        """Compute the current outcome label from collected history."""
        history = self._history.get(publish_record_id, [])
        return label_outcome(history, thresholds=self.thresholds)

    def get_history(self, publish_record_id: str) -> list[MetricsSnapshot]:
        """Return all collected snapshots for a publish record."""
        return list(self._history.get(publish_record_id, []))

    async def attribute(
        self,
        sub_id_records: Sequence[dict[str, str]],
        conversion_reports: Sequence[dict[str, object]],
    ) -> list[ConversionReport]:
        """Attribute conversions to videos via subId join."""
        return attribute_conversions(sub_id_records, conversion_reports)


# ------------------------------------------------------------------ #
# Dry-run transport (Phase 1 dev/CI)                                  #
# ------------------------------------------------------------------ #

class DryRunMetricsTransport:
    """Returns fixture metrics without hitting any external API."""

    def __init__(
        self,
        *,
        base_views: int = 1_000,
        base_ctr: float = 0.02,
    ) -> None:
        self._base_views = base_views
        self._base_ctr = base_ctr
        self._call_count = 0

    # Schedule multipliers — later polls accumulate more metrics
    _SCHEDULE_MULTIPLIERS: ClassVar[dict[PollSchedule, float]] = {
        PollSchedule.HOUR_1: 0.1,
        PollSchedule.HOUR_6: 0.3,
        PollSchedule.HOUR_24: 0.6,
        PollSchedule.DAY_7: 1.0,
        PollSchedule.DAY_30: 1.5,
    }

    async def fetch_metrics(
        self,
        publish_record_id: str,
        schedule: PollSchedule,
    ) -> MetricsSnapshot:
        self._call_count += 1
        mult = self._SCHEDULE_MULTIPLIERS.get(schedule, 1.0)
        views = int(self._base_views * mult)
        return MetricsSnapshot(
            publish_record_id=publish_record_id,
            schedule=schedule,
            views=views,
            likes=int(views * 0.05),
            comments=int(views * 0.01),
            shares=int(views * 0.008),
            saves=int(views * 0.02),
            avg_watch_pct=0.45,
            ctr=self._base_ctr,
            conversions=int(views * self._base_ctr * 0.1),
            gmv_thb=float(int(views * self._base_ctr * 0.1) * 350),
        )


class DryRunConversionTransport:
    """Returns fixture conversion data without Shopee API."""

    async def fetch_conversions(
        self,
        video_id: str,
        publish_record_id: str,
    ) -> ConversionReport:
        return ConversionReport(
            video_id=video_id,
            publish_record_id=publish_record_id,
            clicks=50,
            conversions=3,
            gmv_thb=1050.0,
            conversion_rate=0.06,
        )
