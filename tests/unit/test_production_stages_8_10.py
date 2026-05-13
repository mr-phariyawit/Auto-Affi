"""Tests for production stages 8-10 (Sprint 9 — close ADR-007)."""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_affi.agents.production_director import (
    InvalidTransitionError,
    ProductionDirector,
)
from auto_affi.schemas.production import (
    ProductionRunStatus,
    ProductionStageStatus,
)


# ------------------------------------------------------------------ #
# Helper                                                               #
# ------------------------------------------------------------------ #

def _advance_to_stage(d: ProductionDirector, run_id: str, target: int):
    for s in range(1, target):
        d.decide(run_id, s, "approve")


# ------------------------------------------------------------------ #
# Stage 8 — Final Cut                                                  #
# ------------------------------------------------------------------ #

class TestStage8FinalCut:

    @pytest.mark.unit
    def test_stage_8_fires_after_stage_7(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 8)
        stage8 = d.get_run(run.run_id).get_stage(8)
        assert stage8.status == ProductionStageStatus.IN_REVIEW
        art = stage8.current_revision.artifact
        assert "final_mp4_gs_uri" in art
        assert "editor_passes_applied" in art
        assert len(art["editor_passes_applied"]) == 6

    @pytest.mark.unit
    def test_stage_8_editor_pass_revision(self, tmp_path: Path) -> None:
        """Revise stage 8 to remove a specific editor pass."""
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 8)
        run = d.decide(run.run_id, 8, "revise", notes_th="remove auto_subtitle")
        stage8 = run.get_stage(8)
        passes = stage8.current_revision.artifact["editor_passes_applied"]
        assert "auto_subtitle" not in passes
        assert len(passes) == 5

    @pytest.mark.unit
    def test_stage_8_cost_is_zero(self, tmp_path: Path) -> None:
        """FFmpeg editor passes have no API cost."""
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 8)
        stage8 = d.get_run(run.run_id).get_stage(8)
        assert stage8.current_revision.artifact["total_cost_thb"] == 0.0


# ------------------------------------------------------------------ #
# Stage 9 — Compliance                                                 #
# ------------------------------------------------------------------ #

class TestStage9Compliance:

    @pytest.mark.unit
    def test_stage_9_fires_after_stage_8(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 9)
        stage9 = d.get_run(run.run_id).get_stage(9)
        assert stage9.status == ProductionStageStatus.IN_REVIEW
        art = stage9.current_revision.artifact
        assert "passed" in art
        assert "findings" in art
        assert "checks_run" in art

    @pytest.mark.unit
    def test_stage_9_passes_clean_content(self, tmp_path: Path) -> None:
        """Default fixture content has no compliance violations."""
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 9)
        stage9 = d.get_run(run.run_id).get_stage(9)
        art = stage9.current_revision.artifact
        assert art["passed"] is True
        assert len(art["findings"]) == 0

    @pytest.mark.unit
    def test_stage_9_is_unskippable(self, tmp_path: Path) -> None:
        """Stage 9 cannot be in --auto-approve list."""
        from auto_affi.ops.produce import UNSKIPPABLE_STAGES
        assert 9 in UNSKIPPABLE_STAGES

    @pytest.mark.unit
    def test_stage_9_auto_advances_on_pass(self, tmp_path: Path) -> None:
        """Compliance pass + approve should fire stage 10."""
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 9)
        run = d.decide(run.run_id, 9, "approve")
        stage10 = run.get_stage(10)
        assert stage10.status == ProductionStageStatus.IN_REVIEW


# ------------------------------------------------------------------ #
# Stage 10 — Publish                                                   #
# ------------------------------------------------------------------ #

class TestStage10Publish:

    @pytest.mark.unit
    def test_stage_10_fires_after_stage_9(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 10)
        stage10 = d.get_run(run.run_id).get_stage(10)
        assert stage10.status == ProductionStageStatus.IN_REVIEW
        art = stage10.current_revision.artifact
        assert "caption" in art
        assert "affiliate_link" in art
        assert "subids" in art
        assert "#โฆษณา" in art["caption"]

    @pytest.mark.unit
    def test_stage_10_is_unskippable(self, tmp_path: Path) -> None:
        from auto_affi.ops.produce import UNSKIPPABLE_STAGES
        assert 10 in UNSKIPPABLE_STAGES

    @pytest.mark.unit
    def test_stage_10_dry_run_mode(self, tmp_path: Path) -> None:
        """Without credentials, publish mode is dry_run."""
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 10)
        stage10 = d.get_run(run.run_id).get_stage(10)
        assert stage10.current_revision.artifact["publish_mode"] == "dry_run"


# ------------------------------------------------------------------ #
# Full 10-stage end-to-end                                             #
# ------------------------------------------------------------------ #

class TestFullEndToEnd:

    @pytest.mark.unit
    def test_all_10_stages_approved(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run(
            "https://shopee.co.th/Socket-bit-set-i.992256187.44154734826"
        )

        for stage_id in range(1, 11):
            run = d.decide(run.run_id, stage_id, "approve")

        assert run.status == ProductionRunStatus.APPROVED
        assert all(
            s.status == ProductionStageStatus.APPROVED for s in run.stages
        )
        assert run.total_cost_thb > 0

    @pytest.mark.unit
    def test_end_to_end_json_has_all_keys(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")

        for stage_id in range(1, 11):
            run = d.decide(run.run_id, stage_id, "approve")

        # Verify JSON round-trip
        from auto_affi.schemas.production import from_json_path
        path = tmp_path / f".aegis/brain/production/{run.run_id}.json"
        loaded = from_json_path(path)
        assert loaded.status == ProductionRunStatus.APPROVED
        assert len(loaded.stages) == 10

    @pytest.mark.unit
    def test_end_to_end_with_revisions(self, tmp_path: Path) -> None:
        """Full run with revisions at stages 2 and 5."""
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")

        # Stage 1: approve
        run = d.decide(run.run_id, 1, "approve")

        # Stage 2: revise, then approve
        run = d.decide(run.run_id, 2, "revise", notes_th="ขอ hook ดราม่า")
        run = d.decide(run.run_id, 2, "approve")

        # Stages 3-4: approve
        run = d.decide(run.run_id, 3, "approve")
        run = d.decide(run.run_id, 4, "approve")

        # Stage 5: freeze scene 0, then approve
        run = d.decide(run.run_id, 5, "revise", notes_th="--freeze scene 0")
        run = d.decide(run.run_id, 5, "approve")

        # Stages 6-10: approve
        for s in range(6, 11):
            run = d.decide(run.run_id, s, "approve")

        assert run.status == ProductionRunStatus.APPROVED
        assert run.get_stage(2).revision_count == 2  # initial + 1 revise
        assert run.get_stage(5).revision_count == 2  # initial + 1 revise

    @pytest.mark.unit
    def test_reject_at_stage_9_halts(self, tmp_path: Path) -> None:
        """Compliance rejection halts the entire run."""
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 9)
        run = d.decide(run.run_id, 9, "reject", notes_th="health claims found")
        assert run.status == ProductionRunStatus.REJECTED
        assert run.get_stage(9).status == ProductionStageStatus.REJECTED
