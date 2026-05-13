"""Ops Console data models (FR-OC-01, FR-OC-02).

Defines the read-models that the dashboard displays:
- CampaignSummary: today's campaigns + status
- KillSwitchState: current kill switch activations
- MetricsDashboard: aggregate metrics overview
- QueueItem: pending human review items
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class CampaignStatus(StrEnum):
    PENDING = "pending"
    IN_PRODUCTION = "in_production"
    PUBLISHED = "published"
    KILLED = "killed"
    FAILED = "failed"


class CampaignSummary(BaseModel):
    """One row in the campaigns table."""

    campaign_id: str
    product_name: str
    status: CampaignStatus
    video_count: int = 0
    total_views: int = 0
    total_gmv_thb: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class KillSwitchState(BaseModel):
    """Current kill switch state for dashboard display."""

    level: str  # product | campaign | platform | global
    scope_id: str
    activated_by: str
    reason: str
    activated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MetricsOverview(BaseModel):
    """Aggregate metrics for the dashboard header."""

    videos_today: int = 0
    videos_total: int = 0
    gmv_today_thb: float = 0.0
    gmv_total_thb: float = 0.0
    avg_ctr: float = 0.0
    cost_today_usd: float = 0.0
    pipeline_success_rate: float = 0.0


class QueueItemType(StrEnum):
    BRIEF_REVIEW = "brief_review"
    WIKI_PROMOTION = "wiki_promotion"
    SAFETY_ESCALATION = "safety_escalation"


class QueueItem(BaseModel):
    """A pending item for human review (FR-OC-02)."""

    item_id: str
    item_type: QueueItemType
    title: str
    description: str = ""
    priority: int = Field(ge=1, le=5, default=3)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class DashboardData(BaseModel):
    """Complete dashboard payload for the ops console."""

    metrics: MetricsOverview = Field(default_factory=MetricsOverview)
    campaigns: list[CampaignSummary] = Field(default_factory=list)
    kill_switches: list[KillSwitchState] = Field(default_factory=list)
    queue: list[QueueItem] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(UTC))
