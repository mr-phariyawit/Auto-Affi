"""Tests for monitoring lite / JSONL metrics exporter (QW-10, AFFI-T-057)."""

from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from auto_affi.ops.metrics_export import (
    DailySummary,
    append_jsonl,
    summarize_snapshots,
)
from auto_affi.schemas.metrics import MetricsSnapshot, PollSchedule


# ------------------------------------------------------------------ #
# DailySummary tests                                                  #
# ------------------------------------------------------------------ #


class TestDailySummary:
    @pytest.mark.unit
    def test_to_json_roundtrip(self) -> None:
        summary = DailySummary(date="2026-05-13", videos_published=3, total_views=1200)
        raw = summary.to_json()
        data = json.loads(raw)
        assert data["date"] == "2026-05-13"
        assert data["videos_published"] == 3
        assert data["total_views"] == 1200

    @pytest.mark.unit
    def test_empty_summary(self) -> None:
        summary = DailySummary(date="2026-05-13")
        assert summary.videos_published == 0
        assert summary.total_views == 0
        assert summary.avg_ctr == 0.0


# ------------------------------------------------------------------ #
# summarize_snapshots tests                                           #
# ------------------------------------------------------------------ #


def _make_snapshot(
    *,
    pub_id: str = "pub-001",
    views: int = 100,
    likes: int = 10,
    ctr: float = 0.03,
    gmv: float = 50.0,
    ts: datetime | None = None,
) -> MetricsSnapshot:
    return MetricsSnapshot(
        publish_record_id=pub_id,
        schedule=PollSchedule.HOUR_24,
        ts=ts or datetime(2026, 5, 13, 12, 0, 0, tzinfo=UTC),
        views=views,
        likes=likes,
        ctr=ctr,
        gmv_thb=gmv,
    )


class TestSummarizeSnapshots:
    @pytest.mark.unit
    def test_empty_list(self) -> None:
        summary = summarize_snapshots([], date(2026, 5, 13))
        assert summary.videos_published == 0
        assert summary.snapshot_count == 0

    @pytest.mark.unit
    def test_single_snapshot(self) -> None:
        snapshots = [_make_snapshot(views=500, likes=50, ctr=0.04, gmv=100.0)]
        summary = summarize_snapshots(snapshots, date(2026, 5, 13))
        assert summary.videos_published == 1
        assert summary.total_views == 500
        assert summary.total_likes == 50
        assert summary.avg_ctr == 0.04
        assert summary.total_gmv_thb == 100.0
        assert summary.snapshot_count == 1

    @pytest.mark.unit
    def test_multiple_snapshots_same_pub(self) -> None:
        snapshots = [
            _make_snapshot(pub_id="pub-001", views=100, ctr=0.02),
            _make_snapshot(pub_id="pub-001", views=200, ctr=0.04),
        ]
        summary = summarize_snapshots(snapshots, date(2026, 5, 13))
        assert summary.videos_published == 1  # same pub_id
        assert summary.total_views == 300
        assert summary.avg_ctr == pytest.approx(0.03, rel=1e-3)

    @pytest.mark.unit
    def test_multiple_pubs(self) -> None:
        snapshots = [
            _make_snapshot(pub_id="pub-001", views=100),
            _make_snapshot(pub_id="pub-002", views=200),
            _make_snapshot(pub_id="pub-003", views=300),
        ]
        summary = summarize_snapshots(snapshots, date(2026, 5, 13))
        assert summary.videos_published == 3
        assert summary.total_views == 600

    @pytest.mark.unit
    def test_filters_by_date(self) -> None:
        snapshots = [
            _make_snapshot(
                pub_id="pub-001",
                views=100,
                ts=datetime(2026, 5, 13, 10, 0, 0, tzinfo=UTC),
            ),
            _make_snapshot(
                pub_id="pub-002",
                views=999,
                ts=datetime(2026, 5, 14, 10, 0, 0, tzinfo=UTC),  # different day
            ),
        ]
        summary = summarize_snapshots(snapshots, date(2026, 5, 13))
        assert summary.videos_published == 1
        assert summary.total_views == 100


# ------------------------------------------------------------------ #
# append_jsonl tests                                                  #
# ------------------------------------------------------------------ #


class TestAppendJsonl:
    @pytest.mark.unit
    def test_creates_file(self, tmp_path: Path) -> None:
        output = tmp_path / "metrics.jsonl"
        summary = DailySummary(date="2026-05-13", videos_published=1)
        append_jsonl(summary, output)
        assert output.exists()
        lines = output.read_text().strip().split("\n")
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["date"] == "2026-05-13"

    @pytest.mark.unit
    def test_appends_to_existing(self, tmp_path: Path) -> None:
        output = tmp_path / "metrics.jsonl"
        append_jsonl(DailySummary(date="2026-05-12"), output)
        append_jsonl(DailySummary(date="2026-05-13"), output)
        lines = output.read_text().strip().split("\n")
        assert len(lines) == 2

    @pytest.mark.unit
    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        output = tmp_path / "deep" / "nested" / "metrics.jsonl"
        append_jsonl(DailySummary(date="2026-05-13"), output)
        assert output.exists()
