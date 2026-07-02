"""Metrics schemas for the Analytics Collector agent (FR-AN-01..03).

:class:`MetricsSnapshot` captures a single point-in-time measurement of a
published video's performance.  :class:`OutcomeLabel` classifies a video's
7-day performance for the Feedback Curator.

:class:`ConversionReport` joins Shopee click/conversion data back to the
video that generated the traffic, using the subId taxonomy (AFFI-T-019).
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

# ------------------------------------------------------------------ #
# Poll schedule                                                       #
# ------------------------------------------------------------------ #

class PollSchedule(StrEnum):
    """When to poll metrics after publish."""

    HOUR_1 = "1h"
    HOUR_6 = "6h"
    HOUR_24 = "24h"
    DAY_7 = "7d"
    DAY_30 = "30d"


# ------------------------------------------------------------------ #
# Outcome labeling (FR-AN-02)                                        #
# ------------------------------------------------------------------ #

class OutcomeLabel(StrEnum):
    """7-day outcome classification for Feedback Curator (SPEC 5.3)."""

    BREAKOUT = "breakout"
    HIT = "hit"
    NEUTRAL = "neutral"
    FLOP = "flop"
    BANNED = "banned"


class OutcomeThresholds(BaseModel):
    """Configurable thresholds for outcome classification.

    Defaults are calibrated for Phase 1 Thai Beauty niche on IG Reels.
    """

    breakout_views: int = Field(default=50_000, ge=0)
    hit_views: int = Field(default=10_000, ge=0)
    flop_views: int = Field(default=500, ge=0)
    breakout_ctr: float = Field(default=0.06, ge=0.0, le=1.0)
    hit_ctr: float = Field(default=0.02, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def _thresholds_ordered(self) -> OutcomeThresholds:
        if self.hit_views >= self.breakout_views:
            raise ValueError("hit_views must be < breakout_views")
        if self.flop_views >= self.hit_views:
            raise ValueError("flop_views must be < hit_views")
        return self


# ------------------------------------------------------------------ #
# Metrics snapshot (FR-AN-01 / FR-AN-02)                              #
# ------------------------------------------------------------------ #

class MetricsSnapshot(BaseModel):
    """Point-in-time metrics for a published video.

    Maps directly to ``metrics_timeseries`` columns in SPEC 6.1.
    """

    publish_record_id: str = Field(min_length=1)
    schedule: PollSchedule
    ts: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Engagement metrics
    views: int = Field(ge=0, default=0)
    likes: int = Field(ge=0, default=0)
    comments: int = Field(ge=0, default=0)
    shares: int = Field(ge=0, default=0)
    saves: int = Field(ge=0, default=0)

    # Watch metrics
    avg_watch_pct: float = Field(ge=0.0, le=1.0, default=0.0)

    # Conversion metrics
    ctr: float = Field(ge=0.0, le=1.0, default=0.0)
    conversions: int = Field(ge=0, default=0)
    gmv_thb: float = Field(ge=0.0, default=0.0)


# ------------------------------------------------------------------ #
# Conversion attribution (FR-AN-03)                                   #
# ------------------------------------------------------------------ #

class ConversionReport(BaseModel):
    """Per-video conversion attribution via subId join.

    Joins Shopee ``conversionReport`` data with the video's publish
    record using the subId taxonomy from AFFI-T-019.
    """

    video_id: str = Field(min_length=1)
    publish_record_id: str = Field(min_length=1)
    clicks: int = Field(ge=0, default=0)
    conversions: int = Field(ge=0, default=0)
    gmv_thb: float = Field(ge=0.0, default=0.0)
    conversion_rate: float = Field(ge=0.0, le=1.0, default=0.0)
    attributed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def _compute_rate(self) -> ConversionReport:
        if self.clicks > 0 and self.conversion_rate == 0.0:
            self.conversion_rate = self.conversions / self.clicks
        return self
