"""Tests for production schemas (ADR-007 data model)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_affi.schemas.production import (
    STAGE_NAMES,
    Decision,
    ProductionRun,
    ProductionRunStatus,
    ProductionStage,
    ProductionStageStatus,
    Revision,
    from_json_path,
    to_json_path,
)


class TestProductionRun:
    """ProductionRun model."""

    @pytest.mark.unit
    def test_creates_10_stages(self) -> None:
        run = ProductionRun()
        assert len(run.stages) == 10
        assert run.stages[0].stage_id == 1
        assert run.stages[9].stage_id == 10

    @pytest.mark.unit
    def test_stage_names_match(self) -> None:
        run = ProductionRun()
        for stage in run.stages:
            assert stage.name == STAGE_NAMES[stage.stage_id]

    @pytest.mark.unit
    def test_default_status_is_draft(self) -> None:
        run = ProductionRun()
        assert run.status == ProductionRunStatus.DRAFT

    @pytest.mark.unit
    def test_current_stage_id(self) -> None:
        run = ProductionRun()
        assert run.current_stage_id == 1
        run.stages[0].status = ProductionStageStatus.APPROVED
        assert run.current_stage_id == 2

    @pytest.mark.unit
    def test_in_review_stages(self) -> None:
        run = ProductionRun()
        run.stages[0].status = ProductionStageStatus.IN_REVIEW
        run.stages[2].status = ProductionStageStatus.IN_REVIEW
        assert len(run.in_review_stages) == 2

    @pytest.mark.unit
    def test_get_stage(self) -> None:
        run = ProductionRun()
        assert run.get_stage(1) is not None
        assert run.get_stage(11) is None


class TestProductionStage:
    """ProductionStage model."""

    @pytest.mark.unit
    def test_current_revision_empty(self) -> None:
        stage = ProductionStage(stage_id=1, name="brief_and_concept")
        assert stage.current_revision is None

    @pytest.mark.unit
    def test_current_revision_populated(self) -> None:
        stage = ProductionStage(
            stage_id=1, name="brief_and_concept",
            revisions=[Revision(revision_idx=0)]
        )
        assert stage.current_revision is not None
        assert stage.current_revision.revision_idx == 0

    @pytest.mark.unit
    def test_revision_count(self) -> None:
        stage = ProductionStage(
            stage_id=1, name="brief_and_concept",
            revisions=[Revision(revision_idx=i) for i in range(3)]
        )
        assert stage.revision_count == 3


class TestDecision:
    """Decision model."""

    @pytest.mark.unit
    def test_approve(self) -> None:
        d = Decision(verdict="approve", decided_by="board")
        assert d.verdict == "approve"

    @pytest.mark.unit
    def test_revise_with_notes(self) -> None:
        d = Decision(
            verdict="revise",
            decided_by="board",
            notes_th="ขอ hook ที่ดราม่ากว่านี้",
        )
        assert d.notes_th is not None


class TestPersistence:
    """JSON round-trip persistence."""

    @pytest.mark.unit
    def test_round_trip(self, tmp_path: Path) -> None:
        run = ProductionRun(
            shopee_url="https://shopee.co.th/test-i.123.456",
            shopee_item_id=456,
            shopee_shop_id=123,
            status=ProductionRunStatus.IN_PROGRESS,
        )
        run.stages[0].status = ProductionStageStatus.IN_REVIEW
        run.stages[0].revisions.append(
            Revision(revision_idx=0, artifact={"angles": ["A", "B", "C"]})
        )

        path = to_json_path(run, repo_root=tmp_path)
        assert path.exists()

        loaded = from_json_path(path)
        assert loaded.run_id == run.run_id
        assert loaded.stages[0].status == ProductionStageStatus.IN_REVIEW
        assert loaded.stages[0].current_revision is not None
        assert loaded.stages[0].current_revision.artifact["angles"] == ["A", "B", "C"]

    @pytest.mark.unit
    def test_json_is_valid(self, tmp_path: Path) -> None:
        run = ProductionRun()
        path = to_json_path(run, repo_root=tmp_path)
        data = json.loads(path.read_text())
        assert data["run_id"] == run.run_id
        assert len(data["stages"]) == 10
