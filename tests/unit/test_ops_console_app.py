"""Tests for Ops Console app service (AFFI-T-045, T-046)."""

from __future__ import annotations

import pytest

from auto_affi.agents.kill_switch import KillLevel, KillSwitchRegistry
from auto_affi.ops.console.app import (
    DashboardService,
    get_dashboard_html,
    render_dashboard_fragment,
)
from auto_affi.ops.console.models import (
    CampaignStatus,
    CampaignSummary,
    DashboardData,
    MetricsOverview,
    QueueItem,
    QueueItemType,
)


class TestDashboardService:
    """DashboardService aggregation logic."""

    @pytest.mark.unit
    def test_empty_dashboard(self) -> None:
        svc = DashboardService()
        data = svc.get_dashboard()
        assert data.metrics.videos_today == 0
        assert data.campaigns == []
        assert data.kill_switches == []
        assert data.queue == []

    @pytest.mark.unit
    def test_add_campaign_updates_metrics(self) -> None:
        svc = DashboardService()
        svc.add_campaign(
            CampaignSummary(
                campaign_id="c1",
                product_name="Serum",
                status=CampaignStatus.PUBLISHED,
                video_count=2,
                total_views=5000,
                total_gmv_thb=1750.0,
            )
        )
        data = svc.get_dashboard()
        assert data.metrics.videos_today == 1
        assert data.metrics.gmv_today_thb == 1750.0

    @pytest.mark.unit
    def test_pipeline_success_rate(self) -> None:
        svc = DashboardService()
        svc.add_campaign(
            CampaignSummary(campaign_id="c1", product_name="A", status=CampaignStatus.PUBLISHED)
        )
        svc.add_campaign(
            CampaignSummary(campaign_id="c2", product_name="B", status=CampaignStatus.FAILED)
        )
        metrics = svc.get_metrics()
        assert metrics.pipeline_success_rate == pytest.approx(0.5)

    @pytest.mark.unit
    def test_kill_switch_activation(self) -> None:
        svc = DashboardService()
        assert svc.activate_kill_switch("platform", "ig", reason="test") is True
        switches = svc.get_kill_switches()
        assert len(switches) == 1
        assert switches[0].level == "platform"
        assert switches[0].scope_id == "ig"

    @pytest.mark.unit
    def test_kill_switch_deactivation(self) -> None:
        svc = DashboardService()
        svc.activate_kill_switch("global", "global", reason="test")
        assert svc.deactivate_kill_switch("global", "global") is True
        assert len(svc.get_kill_switches()) == 0

    @pytest.mark.unit
    def test_kill_switch_invalid_level(self) -> None:
        svc = DashboardService()
        assert svc.activate_kill_switch("invalid", "x") is False

    @pytest.mark.unit
    def test_deactivate_nonexistent(self) -> None:
        svc = DashboardService()
        assert svc.deactivate_kill_switch("global", "global") is False

    @pytest.mark.unit
    def test_add_queue_item(self) -> None:
        svc = DashboardService()
        svc.add_queue_item(
            QueueItem(
                item_id="q1",
                item_type=QueueItemType.BRIEF_REVIEW,
                title="Low-confidence brief",
                priority=2,
            )
        )
        queue = svc.get_queue()
        assert len(queue) == 1
        assert queue[0].item_id == "q1"

    @pytest.mark.unit
    def test_shared_kill_registry(self) -> None:
        """Service wraps an external KillSwitchRegistry."""
        reg = KillSwitchRegistry()
        reg.activate(KillLevel.PLATFORM, "ig", reason="external")
        svc = DashboardService(kill_registry=reg)
        switches = svc.get_kill_switches()
        assert len(switches) == 1


class TestHTMXRendering:
    """HTMX template rendering."""

    @pytest.mark.unit
    def test_dashboard_html_has_htmx(self) -> None:
        html = get_dashboard_html()
        assert "htmx.org" in html
        assert "hx-get" in html

    @pytest.mark.unit
    def test_fragment_rendering(self) -> None:
        data = DashboardData(
            metrics=MetricsOverview(videos_today=5, gmv_today_thb=3500.0),
            campaigns=[
                CampaignSummary(
                    campaign_id="c1",
                    product_name="Test Product",
                    status=CampaignStatus.PUBLISHED,
                    total_views=10000,
                ),
            ],
        )
        html = render_dashboard_fragment(data)
        assert "5" in html  # videos_today
        assert "3,500" in html  # GMV
        assert "Test Product" in html

    @pytest.mark.unit
    def test_fragment_with_kill_switches(self) -> None:
        from auto_affi.ops.console.models import KillSwitchState
        data = DashboardData(
            kill_switches=[
                KillSwitchState(
                    level="global",
                    scope_id="global",
                    activated_by="auto-kill",
                    reason="3 violations",
                ),
            ],
        )
        html = render_dashboard_fragment(data)
        assert "auto-kill" in html
        assert "3 violations" in html

    @pytest.mark.unit
    def test_fragment_empty_dashboard(self) -> None:
        data = DashboardData()
        html = render_dashboard_fragment(data)
        assert "Last updated" in html
