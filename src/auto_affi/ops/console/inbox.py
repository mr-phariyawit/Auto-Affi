"""HTMX inbox dashboard for production workflow review (ADR-007).

Renders:
- Inbox page: list of IN_REVIEW stages across all runs
- Stage review page: deliverable preview + approve/revise/reject buttons
- Mobile-responsive, dark theme, no React build step
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from auto_affi.schemas.production import (
    ProductionRun,
    ProductionStage,
    ProductionStageStatus,
)


def render_inbox_page(runs: list[ProductionRun]) -> str:
    """Render the full inbox HTML page."""
    return f"""\
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auto-Affi Studio Inbox</title>
<script src="https://unpkg.com/htmx.org@2.0.4"></script>
<style>
{_CSS}
</style>
</head>
<body>
<h1>Auto-Affi Studio / Inbox</h1>
<div id="inbox" hx-get="/api/inbox/fragment" hx-trigger="load, every 10s"
     hx-swap="innerHTML">
  {_render_inbox_fragment(runs)}
</div>
</body>
</html>
"""


def render_inbox_fragment(runs: list[ProductionRun]) -> str:
    """Render just the inbox content (for HTMX polling)."""
    return _render_inbox_fragment(runs)


def render_stage_review_page(
    run: ProductionRun,
    stage: ProductionStage,
) -> str:
    """Render the stage review page with deliverable + decision buttons."""
    artifact = {}
    if stage.current_revision:
        artifact = stage.current_revision.artifact or {}

    return f"""\
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Review: {stage.display_name} | {run.run_id}</title>
<script src="https://unpkg.com/htmx.org@2.0.4"></script>
<style>
{_CSS}
</style>
</head>
<body>
<a href="/inbox" class="back-link">Back to Inbox</a>
<h1>Stage {stage.stage_id}: {stage.display_name}</h1>
<div class="meta">
  Run: {run.run_id} | Revision: {stage.revision_count} |
  Status: <span class="badge badge-{stage.status.value}">{stage.status.value}</span>
</div>

<div class="card">
  <h2>Deliverable</h2>
  {_render_artifact(stage.stage_id, artifact)}
</div>

{_render_decision_form(run.run_id, stage) if stage.status == ProductionStageStatus.IN_REVIEW else '<p class="meta">Stage already decided.</p>'}

{_render_revision_history(stage)}
</body>
</html>
"""


# ------------------------------------------------------------------ #
# Internal renderers                                                   #
# ------------------------------------------------------------------ #

def _render_inbox_fragment(runs: list[ProductionRun]) -> str:
    in_review: list[tuple[ProductionRun, ProductionStage]] = []
    for run in runs:
        for stage in run.in_review_stages:
            in_review.append((run, stage))

    if not in_review:
        return '<p class="empty">No stages awaiting review.</p>'

    html = f'<p class="count">{len(in_review)} stage(s) awaiting your review</p>'
    html += '<table><tr><th>Run</th><th>Stage</th><th>Product</th><th>Rev</th><th>SLA</th><th></th></tr>'

    for run, stage in in_review:
        sla_str = _sla_badge(stage)
        product = run.shopee_url.split("/")[-1][:30] if run.shopee_url else f"item-{run.shopee_item_id}"
        html += (
            f'<tr>'
            f'<td>{run.run_id[:8]}</td>'
            f'<td>{stage.display_name}</td>'
            f'<td>{product}</td>'
            f'<td>{stage.revision_count}</td>'
            f'<td>{sla_str}</td>'
            f'<td><a href="/production/runs/{run.run_id}/stages/{stage.stage_id}/review" '
            f'class="btn btn-sm">Review</a></td>'
            f'</tr>'
        )
    html += '</table>'
    return html


def _sla_badge(stage: ProductionStage) -> str:
    now = datetime.now(UTC)
    delta = stage.sla_deadline - now
    hours = delta.total_seconds() / 3600
    if hours < 0:
        return f'<span class="badge badge-red">OVERDUE {abs(hours):.0f}h</span>'
    if hours < 3:
        return f'<span class="badge badge-amber">{hours:.0f}h left</span>'
    return f'<span class="badge badge-green">{hours:.0f}h left</span>'


def _render_artifact(stage_id: int, artifact: dict[str, Any]) -> str:
    """Render stage-specific deliverable preview."""
    if not artifact:
        return '<p class="empty">No deliverable yet.</p>'

    if stage_id <= 3:
        # Script / storyboard / brief: pretty-print JSON
        return f'<pre class="artifact-json">{json.dumps(artifact, indent=2, ensure_ascii=False)}</pre>'

    if stage_id == 4:
        # Image grid
        images = artifact.get("scene_images", [])
        html = '<div class="image-grid">'
        for img in images:
            uri = img.get("gs_uri", "")
            html += f'<div class="image-card"><div class="placeholder">Scene {img.get("scene_idx", "?")}</div><p class="uri">{uri}</p></div>'
        html += '</div>'
        return html

    if stage_id == 5:
        # Video clips
        clips = artifact.get("scene_clips", [])
        html = '<div class="clip-grid">'
        for clip in clips:
            mode = clip.get("mode", "i2v")
            cost = clip.get("cost_thb", 0)
            html += (
                f'<div class="clip-card">'
                f'<div class="placeholder">Scene {clip.get("scene_idx", "?")}</div>'
                f'<p>Mode: {mode} | Cost: {cost:.2f} THB</p>'
                f'</div>'
            )
        html += '</div>'
        return html

    if stage_id == 6:
        # Voice takes
        takes = artifact.get("scene_takes", [])
        html = '<div class="takes-list">'
        for take_group in takes:
            html += f'<h3>Scene {take_group.get("scene_idx", "?")}</h3>'
            for take in take_group.get("takes", []):
                html += f'<p>Voice: {take.get("voice", "?")} | <code>{take.get("gs_uri", "")}</code></p>'
        html += '</div>'
        return html

    if stage_id == 7:
        # Music
        track = artifact.get("music_track", {})
        return (
            f'<div class="music-card">'
            f'<p>Mood: {track.get("mood", "?")}</p>'
            f'<p>Duration: {track.get("duration_s", 0):.0f}s</p>'
            f'<p>Cost: {track.get("cost_thb", 0):.2f} THB</p>'
            f'<p><code>{track.get("gs_uri", "")}</code></p>'
            f'</div>'
        )

    return f'<pre class="artifact-json">{json.dumps(artifact, indent=2, ensure_ascii=False)}</pre>'


def _render_decision_form(run_id: str, stage: ProductionStage) -> str:
    return f"""\
<div class="card decision-form">
  <h2>Decision</h2>
  <form hx-post="/api/production/runs/{run_id}/stages/{stage.stage_id}/decide"
        hx-target="#result" hx-swap="innerHTML">
    <div class="form-row">
      <label>Verdict:</label>
      <select name="verdict">
        <option value="approve">Approve</option>
        <option value="revise">Revise</option>
        <option value="reject">Reject</option>
      </select>
    </div>
    <div class="form-row">
      <label>Notes (Thai):</label>
      <textarea name="notes_th" rows="3" placeholder="revision notes / reject reason"></textarea>
    </div>
    <button type="submit" class="btn">Submit Decision</button>
  </form>
  <div id="result"></div>
</div>
"""


def _render_revision_history(stage: ProductionStage) -> str:
    if not stage.revisions:
        return ""
    html = '<div class="card"><h2>Revision History</h2>'
    for rev in stage.revisions:
        verdict = rev.decision.verdict if rev.decision else "pending"
        html += (
            f'<div class="revision">'
            f'<span class="badge badge-{verdict}">Rev {rev.revision_idx}: {verdict}</span>'
            f' | Cost: {rev.cost_thb:.3f} THB'
            f' | {rev.produced_at.strftime("%H:%M %b %d")}'
        )
        if rev.decision and rev.decision.notes_th:
            html += f' | Notes: {rev.decision.notes_th}'
        html += '</div>'
    html += '</div>'
    return html


# ------------------------------------------------------------------ #
# CSS                                                                  #
# ------------------------------------------------------------------ #

_CSS = """\
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, sans-serif;
       background: #0f1117; color: #e4e4e7; padding: 1.5rem; max-width: 900px; margin: 0 auto; }
h1 { font-size: 1.4rem; margin-bottom: 1rem; color: #a78bfa; }
h2 { font-size: 1rem; color: #71717a; margin-bottom: 0.75rem; text-transform: uppercase;
     letter-spacing: 0.05em; }
h3 { font-size: 0.9rem; color: #a1a1aa; margin: 0.5rem 0; }
.back-link { color: #818cf8; text-decoration: none; font-size: 0.85rem; }
.meta { color: #71717a; font-size: 0.85rem; margin-bottom: 1rem; }
.count { color: #a78bfa; font-size: 0.9rem; margin-bottom: 0.75rem; }
.empty { color: #52525b; font-style: italic; }
.card { background: #1e1e2e; border-radius: 12px; padding: 1.25rem;
        border: 1px solid #2e2e3e; margin-bottom: 1rem; }
table { width: 100%; border-collapse: collapse; }
th, td { text-align: left; padding: 0.5rem; border-bottom: 1px solid #2e2e3e; font-size: 0.85rem; }
th { color: #71717a; text-transform: uppercase; font-size: 0.75rem; }
.badge { padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.75rem; display: inline-block; }
.badge-green, .badge-approve, .badge-approved { background: #065f46; color: #6ee7b7; }
.badge-amber, .badge-revise, .badge-revision_pending { background: #78350f; color: #fde68a; }
.badge-red, .badge-reject, .badge-rejected { background: #7f1d1d; color: #fca5a5; }
.badge-in_review, .badge-pending { background: #1e3a5f; color: #93c5fd; }
.btn { background: #4f46e5; color: white; border: none; padding: 0.5rem 1rem;
       border-radius: 6px; cursor: pointer; font-size: 0.85rem; text-decoration: none; }
.btn:hover { background: #4338ca; }
.btn-sm { padding: 0.25rem 0.5rem; font-size: 0.75rem; }
.artifact-json { background: #111827; padding: 1rem; border-radius: 8px;
                 font-size: 0.8rem; overflow-x: auto; white-space: pre-wrap;
                 max-height: 400px; overflow-y: auto; color: #d1d5db; }
.image-grid, .clip-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 0.75rem; }
.image-card, .clip-card { background: #111827; border-radius: 8px; padding: 0.75rem; text-align: center; }
.placeholder { background: #1e293b; height: 100px; border-radius: 4px; display: flex;
               align-items: center; justify-content: center; color: #64748b; font-size: 0.8rem;
               margin-bottom: 0.5rem; }
.uri { font-size: 0.65rem; color: #4b5563; word-break: break-all; }
.form-row { margin-bottom: 0.75rem; }
.form-row label { display: block; color: #a1a1aa; font-size: 0.85rem; margin-bottom: 0.25rem; }
.form-row select, .form-row textarea { width: 100%; background: #111827; border: 1px solid #2e2e3e;
    color: #e4e4e7; padding: 0.5rem; border-radius: 6px; font-size: 0.85rem; }
.revision { padding: 0.5rem 0; border-bottom: 1px solid #1e1e2e; font-size: 0.85rem; }
.decision-form { margin-top: 1rem; }
@media (max-width: 600px) {
  body { padding: 1rem; }
  .image-grid, .clip-grid { grid-template-columns: repeat(2, 1fr); }
}
"""
