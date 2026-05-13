"""Ops Console FastAPI application (FR-OC-01, FR-OC-02).

Minimal supervisor dashboard API. Serves:
- GET /api/dashboard — full DashboardData payload
- GET /api/dashboard/metrics — MetricsOverview only
- GET /api/dashboard/kill-switches — active kill switches
- GET /api/dashboard/queue — pending human review items
- POST /api/dashboard/kill-switches/{level}/{scope_id}/activate
- POST /api/dashboard/kill-switches/{level}/{scope_id}/deactivate
- GET / — HTMX dashboard page

Auth: single-header API key for Phase 1. Phase 2 hardens to OIDC.
"""

from __future__ import annotations

from auto_affi.agents.kill_switch import KillLevel, KillSwitchRegistry
from auto_affi.ops.console.models import (
    CampaignStatus,
    CampaignSummary,
    DashboardData,
    KillSwitchState,
    MetricsOverview,
    QueueItem,
)

# ------------------------------------------------------------------ #
# Dashboard service (in-memory state, no DB in Phase 1)                #
# ------------------------------------------------------------------ #


class DashboardService:
    """Aggregates dashboard data from in-memory registries.

    Phase 1: returns fixture/demo data.
    Phase 2: reads from Postgres + Redis.
    """

    def __init__(
        self,
        *,
        kill_registry: KillSwitchRegistry | None = None,
    ) -> None:
        self._kill_registry = kill_registry or KillSwitchRegistry()
        self._campaigns: list[CampaignSummary] = []
        self._queue: list[QueueItem] = []

    def get_dashboard(self) -> DashboardData:
        """Return the full dashboard payload."""
        return DashboardData(
            metrics=self._get_metrics(),
            campaigns=self._campaigns,
            kill_switches=self._get_kill_switches(),
            queue=self._queue,
        )

    def get_metrics(self) -> MetricsOverview:
        return self._get_metrics()

    def get_kill_switches(self) -> list[KillSwitchState]:
        return self._get_kill_switches()

    def get_queue(self) -> list[QueueItem]:
        return list(self._queue)

    def activate_kill_switch(
        self,
        level: str,
        scope_id: str,
        *,
        activated_by: str = "human",
        reason: str = "",
    ) -> bool:
        """Activate a kill switch. Returns True if successful."""
        try:
            kill_level = KillLevel[level.upper()]
        except KeyError:
            return False
        self._kill_registry.activate(
            kill_level, scope_id,
            activated_by=activated_by,
            reason=reason,
        )
        return True

    def deactivate_kill_switch(
        self,
        level: str,
        scope_id: str,
        *,
        deactivated_by: str = "human",
        reason: str = "",
    ) -> bool:
        """Deactivate a kill switch. Returns True if found and deactivated."""
        try:
            kill_level = KillLevel[level.upper()]
        except KeyError:
            return False
        result = self._kill_registry.deactivate(
            kill_level, scope_id,
            deactivated_by=deactivated_by,
            reason=reason,
        )
        return result is not None

    def add_campaign(self, campaign: CampaignSummary) -> None:
        self._campaigns.append(campaign)

    def add_queue_item(self, item: QueueItem) -> None:
        self._queue.append(item)

    def _get_metrics(self) -> MetricsOverview:
        """Compute metrics from campaign data."""
        published = [
            c for c in self._campaigns
            if c.status == CampaignStatus.PUBLISHED
        ]
        return MetricsOverview(
            videos_today=len(published),
            videos_total=len(self._campaigns),
            gmv_today_thb=sum(c.total_gmv_thb for c in published),
            gmv_total_thb=sum(c.total_gmv_thb for c in self._campaigns),
            pipeline_success_rate=(
                len(published) / len(self._campaigns)
                if self._campaigns else 0.0
            ),
        )

    def _get_kill_switches(self) -> list[KillSwitchState]:
        return [
            KillSwitchState(
                level=r.level.name.lower(),
                scope_id=r.scope_id,
                activated_by=r.activated_by,
                reason=r.reason,
                activated_at=r.ts,
            )
            for r in self._kill_registry.active_switches()
        ]


# ------------------------------------------------------------------ #
# HTMX template rendering                                             #
# ------------------------------------------------------------------ #

_DASHBOARD_HTML = """\
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auto-Affi Ops Console</title>
<script src="https://unpkg.com/htmx.org@2.0.4"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, sans-serif;
       background: #0f1117; color: #e4e4e7; padding: 2rem; }
h1 { font-size: 1.5rem; margin-bottom: 1.5rem; color: #a78bfa; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem; margin-bottom: 2rem; }
.card { background: #1e1e2e; border-radius: 12px; padding: 1.25rem;
        border: 1px solid #2e2e3e; }
.card h2 { font-size: 0.85rem; color: #71717a; text-transform: uppercase;
           letter-spacing: 0.05em; margin-bottom: 0.5rem; }
.card .value { font-size: 2rem; font-weight: 700; }
.card .value.green { color: #4ade80; }
.card .value.amber { color: #fbbf24; }
.card .value.red { color: #f87171; }
table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
th, td { text-align: left; padding: 0.5rem 0.75rem; border-bottom: 1px solid #2e2e3e; }
th { color: #71717a; font-size: 0.8rem; text-transform: uppercase; }
.status { padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.75rem; }
.status.published { background: #065f46; color: #6ee7b7; }
.status.killed { background: #7f1d1d; color: #fca5a5; }
.status.pending { background: #78350f; color: #fde68a; }
.refresh-note { color: #52525b; font-size: 0.75rem; margin-top: 2rem; }
</style>
</head>
<body>
<h1>Auto-Affi Ops Console</h1>
<div id="dashboard" hx-get="/api/dashboard/fragment" hx-trigger="load, every 10s"
     hx-swap="innerHTML">
  Loading dashboard...
</div>
<p class="refresh-note">Auto-refreshes every 10 seconds via HTMX</p>
</body>
</html>
"""


def render_dashboard_fragment(data: DashboardData) -> str:
    """Render the HTMX fragment for the dashboard content area."""
    m = data.metrics

    # KPI cards
    html = '<div class="grid">'
    html += _card("Videos Today", str(m.videos_today), "green" if m.videos_today > 0 else "amber")
    html += _card("Videos Total", str(m.videos_total), "green")
    html += _card("GMV Today", f"{m.gmv_today_thb:,.0f} THB", "green" if m.gmv_today_thb > 0 else "amber")
    html += _card("GMV Total", f"{m.gmv_total_thb:,.0f} THB", "green")
    html += _card("Pipeline Rate", f"{m.pipeline_success_rate:.0%}", "green" if m.pipeline_success_rate >= 0.9 else "red")
    html += _card("Kill Switches", str(len(data.kill_switches)), "red" if data.kill_switches else "green")
    html += '</div>'

    # Kill switches
    if data.kill_switches:
        html += '<div class="card"><h2>Active Kill Switches</h2><table>'
        html += '<tr><th>Level</th><th>Scope</th><th>By</th><th>Reason</th></tr>'
        for ks in data.kill_switches:
            html += f'<tr><td>{ks.level}</td><td>{ks.scope_id}</td><td>{ks.activated_by}</td><td>{ks.reason}</td></tr>'
        html += '</table></div>'

    # Campaigns
    if data.campaigns:
        html += '<div class="card"><h2>Today\'s Campaigns</h2><table>'
        html += '<tr><th>Product</th><th>Status</th><th>Videos</th><th>Views</th><th>GMV</th></tr>'
        for c in data.campaigns[:10]:
            status_class = c.status.value
            html += (
                f'<tr><td>{c.product_name}</td>'
                f'<td><span class="status {status_class}">{c.status.value}</span></td>'
                f'<td>{c.video_count}</td><td>{c.total_views:,}</td>'
                f'<td>{c.total_gmv_thb:,.0f}</td></tr>'
            )
        html += '</table></div>'

    # Queue
    if data.queue:
        html += '<div class="card"><h2>Pending Review</h2><table>'
        html += '<tr><th>Type</th><th>Title</th><th>Priority</th></tr>'
        for q in data.queue:
            html += f'<tr><td>{q.item_type.value}</td><td>{q.title}</td><td>P{q.priority}</td></tr>'
        html += '</table></div>'

    html += f'<p class="refresh-note">Last updated: {data.last_updated.strftime("%H:%M:%S UTC")}</p>'
    return html


def _card(title: str, value: str, color: str = "green") -> str:
    return f'<div class="card"><h2>{title}</h2><div class="value {color}">{value}</div></div>'


def get_dashboard_html() -> str:
    """Return the full dashboard HTML page."""
    return _DASHBOARD_HTML
