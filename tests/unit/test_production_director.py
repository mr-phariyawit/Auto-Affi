"""Tests for ProductionDirector (ADR-007 state machine)."""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_affi.agents.production_director import (
    InvalidTransitionError,
    ProductionDirector,
    parse_shopee_url,
)
from auto_affi.schemas.production import (
    MAX_REVISIONS_PER_STAGE,
    ProductionRunStatus,
    ProductionStageStatus,
)


class TestParseShopeeUrl:
    """Shopee URL parser."""

    @pytest.mark.unit
    def test_standard_url(self) -> None:
        shop_id, item_id = parse_shopee_url(
            "https://shopee.co.th/Socket-bit-set-i.992256187.44154734826"
        )
        assert shop_id == 992256187
        assert item_id == 44154734826

    @pytest.mark.unit
    def test_product_url(self) -> None:
        shop_id, item_id = parse_shopee_url(
            "https://shopee.co.th/product/123/456"
        )
        assert shop_id == 123
        assert item_id == 456

    @pytest.mark.unit
    def test_invalid_url(self) -> None:
        with pytest.raises(ValueError, match="Cannot parse"):
            parse_shopee_url("https://example.com/not-shopee")


class TestProductionDirector:
    """Production Director state machine."""

    @pytest.mark.unit
    def test_start_run(self, tmp_path: Path) -> None:
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run(
            "https://shopee.co.th/test-i.100.200"
        )
        assert run.status == ProductionRunStatus.IN_PROGRESS
        assert run.shopee_item_id == 200
        assert run.stages[0].status == ProductionStageStatus.IN_REVIEW
        assert run.stages[0].revision_count == 1

    @pytest.mark.unit
    def test_approve_advances_to_next_stage(self, tmp_path: Path) -> None:
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")
        run_id = run.run_id

        # Approve stage 1 -> stage 2 fires
        run = director.decide(run_id, 1, "approve")
        assert run.stages[0].status == ProductionStageStatus.APPROVED
        assert run.stages[1].status == ProductionStageStatus.IN_REVIEW

    @pytest.mark.unit
    def test_revise_loops_stage(self, tmp_path: Path) -> None:
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")
        run_id = run.run_id

        # Revise stage 1
        run = director.decide(run_id, 1, "revise", notes_th="ขอเปลี่ยน angle")
        assert run.stages[0].status == ProductionStageStatus.IN_REVIEW  # re-fired
        assert run.stages[0].revision_count == 2

    @pytest.mark.unit
    def test_reject_halts_run(self, tmp_path: Path) -> None:
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")
        run_id = run.run_id

        run = director.decide(run_id, 1, "reject", notes_th="ตลาดไม่เหมาะ")
        assert run.stages[0].status == ProductionStageStatus.REJECTED
        assert run.status == ProductionRunStatus.REJECTED

    @pytest.mark.unit
    def test_revision_cap_enforced(self, tmp_path: Path) -> None:
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")
        run_id = run.run_id

        # Exhaust revision cap
        for i in range(MAX_REVISIONS_PER_STAGE - 1):
            run = director.decide(run_id, 1, "revise", notes_th=f"rev {i}")

        # Next revise should fail
        with pytest.raises(InvalidTransitionError, match="max revisions"):
            director.decide(run_id, 1, "revise", notes_th="too many")

    @pytest.mark.unit
    def test_invalid_verdict(self, tmp_path: Path) -> None:
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")
        # Pydantic Literal["approve","revise","reject"] catches invalid verdict
        with pytest.raises((InvalidTransitionError, Exception)):
            director.decide(run.run_id, 1, "maybe")

    @pytest.mark.unit
    def test_decide_on_non_review_stage(self, tmp_path: Path) -> None:
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")
        # Stage 2 is DRAFT, not IN_REVIEW
        with pytest.raises(InvalidTransitionError, match="not in_review"):
            director.decide(run.run_id, 2, "approve")

    @pytest.mark.unit
    def test_run_not_found(self, tmp_path: Path) -> None:
        director = ProductionDirector(repo_root=tmp_path)
        with pytest.raises(InvalidTransitionError, match="not found"):
            director.decide("nonexistent", 1, "approve")

    @pytest.mark.unit
    def test_full_stages_1_to_3(self, tmp_path: Path) -> None:
        """Walk through stages 1-3 sequentially."""
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")
        rid = run.run_id

        # Stage 1: approve
        run = director.decide(rid, 1, "approve")
        assert run.stages[0].status == ProductionStageStatus.APPROVED
        assert run.stages[1].status == ProductionStageStatus.IN_REVIEW

        # Stage 2: revise once, then approve
        run = director.decide(rid, 2, "revise", notes_th="ขอ hook ดราม่ากว่านี้")
        assert run.stages[1].revision_count == 2
        run = director.decide(rid, 2, "approve")
        assert run.stages[1].status == ProductionStageStatus.APPROVED
        assert run.stages[2].status == ProductionStageStatus.IN_REVIEW

        # Stage 3: approve
        run = director.decide(rid, 3, "approve")
        assert run.stages[2].status == ProductionStageStatus.APPROVED
        # Stage 4 should remain DRAFT (not implemented in Sprint 7)
        assert run.stages[3].status == ProductionStageStatus.DRAFT

    @pytest.mark.unit
    def test_persistence_across_get(self, tmp_path: Path) -> None:
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")

        # Clear in-memory cache to force disk read
        director._runs.clear()

        loaded = director.get_run(run.run_id)
        assert loaded is not None
        assert loaded.run_id == run.run_id
        assert loaded.stages[0].status == ProductionStageStatus.IN_REVIEW

    @pytest.mark.unit
    def test_list_runs(self, tmp_path: Path) -> None:
        director = ProductionDirector(repo_root=tmp_path)
        director.start_run("https://shopee.co.th/test-i.100.200")
        director.start_run("https://shopee.co.th/test-i.100.300")
        runs = director.list_runs()
        assert len(runs) == 2

    @pytest.mark.unit
    def test_stage_artifact_has_data(self, tmp_path: Path) -> None:
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")
        stage1 = run.get_stage(1)
        assert stage1 is not None
        assert stage1.current_revision is not None
        assert "angles" in stage1.current_revision.artifact


class TestProductionRoutes:
    """Production route handler tests."""

    @pytest.mark.unit
    def test_list_runs_empty(self, tmp_path: Path) -> None:
        from auto_affi.ops.console.production_routes import ProductionRouteHandler
        handler = ProductionRouteHandler(
            director=ProductionDirector(repo_root=tmp_path)
        )
        result = handler.list_runs()
        assert result["count"] == 0

    @pytest.mark.unit
    def test_get_run(self, tmp_path: Path) -> None:
        from auto_affi.ops.console.production_routes import ProductionRouteHandler
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")
        handler = ProductionRouteHandler(director=director)
        result = handler.get_run(run.run_id)
        assert "run_id" in result
        assert result["run_id"] == run.run_id

    @pytest.mark.unit
    def test_decide_approve(self, tmp_path: Path) -> None:
        from auto_affi.ops.console.production_routes import ProductionRouteHandler
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")
        handler = ProductionRouteHandler(director=director)
        result = handler.decide(run.run_id, 1, "approve")
        assert result["ok"] is True
        assert result["verdict"] == "approve"
        assert result["stage_status"] == "approved"

    @pytest.mark.unit
    def test_decide_invalid_verdict(self, tmp_path: Path) -> None:
        from auto_affi.ops.console.production_routes import ProductionRouteHandler
        director = ProductionDirector(repo_root=tmp_path)
        run = director.start_run("https://shopee.co.th/test-i.100.200")
        handler = ProductionRouteHandler(director=director)
        result = handler.decide(run.run_id, 1, "invalid")
        assert "error" in result
