"""Monitoring lite — JSONL metrics exporter (QW-10).

Reads MetricsSnapshot history from the analytics collector and writes
daily summary lines to a JSONL file for lightweight dashboard consumption.

Usage:
    .venv/bin/python -m auto_affi.ops.metrics_export \
        --output out/metrics.jsonl \
        --date 2026-05-13

Each line is a self-contained JSON object:
    {"date": "2026-05-13", "videos_published": 3, "total_views": 1200, ...}

This is the Phase 1 monitoring story — replaces a full Ops Console
dashboard with a simple file that Google Sheets or Notion can ingest.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path

from auto_affi.schemas.metrics import MetricsSnapshot


@dataclass(frozen=True, slots=True)
class DailySummary:
    """Single-day aggregate of video performance metrics."""

    date: str
    videos_published: int = 0
    total_views: int = 0
    total_likes: int = 0
    total_comments: int = 0
    total_shares: int = 0
    total_saves: int = 0
    avg_ctr: float = 0.0
    total_conversions: int = 0
    total_gmv_thb: float = 0.0
    avg_watch_pct: float = 0.0
    snapshot_count: int = 0

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


def summarize_snapshots(
    snapshots: list[MetricsSnapshot],
    target_date: date,
) -> DailySummary:
    """Aggregate a list of MetricsSnapshot into a DailySummary for one day.

    Filters snapshots to those whose ``ts`` falls on ``target_date``.
    """
    day_snapshots = [
        s for s in snapshots
        if s.ts.date() == target_date
    ]

    if not day_snapshots:
        return DailySummary(date=target_date.isoformat())

    unique_pubs = set(s.publish_record_id for s in day_snapshots)
    total_views = sum(s.views for s in day_snapshots)
    total_likes = sum(s.likes for s in day_snapshots)
    total_comments = sum(s.comments for s in day_snapshots)
    total_shares = sum(s.shares for s in day_snapshots)
    total_saves = sum(s.saves for s in day_snapshots)
    total_conversions = sum(s.conversions for s in day_snapshots)
    total_gmv = sum(s.gmv_thb for s in day_snapshots)

    ctrs = [s.ctr for s in day_snapshots if s.ctr > 0]
    avg_ctr = sum(ctrs) / len(ctrs) if ctrs else 0.0

    watch_pcts = [s.avg_watch_pct for s in day_snapshots if s.avg_watch_pct > 0]
    avg_watch = sum(watch_pcts) / len(watch_pcts) if watch_pcts else 0.0

    return DailySummary(
        date=target_date.isoformat(),
        videos_published=len(unique_pubs),
        total_views=total_views,
        total_likes=total_likes,
        total_comments=total_comments,
        total_shares=total_shares,
        total_saves=total_saves,
        avg_ctr=round(avg_ctr, 6),
        total_conversions=total_conversions,
        total_gmv_thb=round(total_gmv, 2),
        avg_watch_pct=round(avg_watch, 4),
        snapshot_count=len(day_snapshots),
    )


def append_jsonl(summary: DailySummary, output_path: Path) -> None:
    """Append a DailySummary as one JSONL line to the output file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as f:
        f.write(summary.to_json() + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="auto_affi.ops.metrics_export",
        description="Export daily metrics summary to JSONL",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("out/metrics.jsonl"),
        help="Output JSONL file path (default: out/metrics.jsonl)",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Target date (YYYY-MM-DD). Default: today.",
    )
    args = parser.parse_args()

    target = (
        date.fromisoformat(args.date) if args.date
        else datetime.now(UTC).date()
    )

    # Phase 1: no live data source — generate empty summary for the day.
    # When live ops start, this will read from analytics_collector history.
    summary = DailySummary(date=target.isoformat())
    append_jsonl(summary, args.output)
    print(f"Exported: {summary.to_json()}")
    print(f"Written to: {args.output}")


if __name__ == "__main__":
    main()
