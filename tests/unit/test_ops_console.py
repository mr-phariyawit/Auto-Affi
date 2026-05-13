"""Tests for Ops Console data models (AFFI-T-044)."""

from __future__ import annotations

import pytest

from auto_affi.ops.console.models import (
    CampaignStatus,
    CampaignSummary,
    DashboardData,
    KillSwitchState,
    MetricsOverview,
    QueueItem,
    QueueItemType,
)


class TestOpsConsoleModels:
    """Ops Console model validation."""

    @pytest.mark.unit
    def test_campaign_summary(self) -> None:
        summary = CampaignSummary(
            campaign_id="camp-001",
            product_name="Vitamin C Serum",
            status=CampaignStatus.PUBLISHED,
            video_count=3,
            total_views=15000,
        )
        assert summary.status == CampaignStatus.PUBLISHED

    @pytest.mark.unit
    def test_kill_switch_state(self) -> None:
        state = KillSwitchState(
            level="global",
            scope_id="global",
            activated_by="auto-kill",
            reason="3 violations in 24h",
        )
        assert state.level == "global"

    @pytest.mark.unit
    def test_metrics_overview_defaults(self) -> None:
        metrics = MetricsOverview()
        assert metrics.videos_today == 0
        assert metrics.avg_ctr == 0.0

    @pytest.mark.unit
    def test_queue_item(self) -> None:
        item = QueueItem(
            item_id="q-001",
            item_type=QueueItemType.BRIEF_REVIEW,
            title="Low-confidence brief needs approval",
            priority=2,
        )
        assert item.priority == 2

    @pytest.mark.unit
    def test_queue_item_rejects_invalid_priority(self) -> None:
        with pytest.raises(ValueError):
            QueueItem(
                item_id="q-bad",
                item_type=QueueItemType.SAFETY_ESCALATION,
                title="test",
                priority=0,
            )

    @pytest.mark.unit
    def test_dashboard_data_empty(self) -> None:
        dashboard = DashboardData()
        assert dashboard.metrics.videos_today == 0
        assert dashboard.campaigns == []
        assert dashboard.kill_switches == []
        assert dashboard.queue == []

    @pytest.mark.unit
    def test_dashboard_data_populated(self) -> None:
        dashboard = DashboardData(
            metrics=MetricsOverview(videos_today=5, gmv_today_thb=3500.0),
            campaigns=[
                CampaignSummary(
                    campaign_id="c1",
                    product_name="Product A",
                    status=CampaignStatus.PUBLISHED,
                ),
            ],
            kill_switches=[
                KillSwitchState(
                    level="platform",
                    scope_id="ig",
                    activated_by="human",
                    reason="IG account suspended",
                ),
            ],
        )
        assert len(dashboard.campaigns) == 1
        assert len(dashboard.kill_switches) == 1
