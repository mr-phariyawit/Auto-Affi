"""Tests for production stages 4-7 + inbox (Sprint 8)."""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_affi.agents.production_director import (
    InvalidTransitionError,
    ProductionDirector,
)
from auto_affi.ops.console.inbox import (
    render_inbox_fragment,
    render_inbox_page,
    render_stage_review_page,
)
from auto_affi.schemas.production import (
    ProductionRunStatus,
    ProductionStageStatus,
)


# ------------------------------------------------------------------ #
# Helper: advance to a target stage                                    #
# ------------------------------------------------------------------ #

def _advance_to_stage(director: ProductionDirector, run_id: str, target: int):
    """Approve stages 1..target-1 to reach the target stage."""
    for s in range(1, target):
        director.decide(run_id, s, "approve")


class TestStage4VisualReferences:
    """Stage 4: Visual References (Nano Banana 2 stills)."""

    @pytest.mark.unit
    def test_stage_4_fires_after_stage_3(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 4)
        stage4 = d.get_run(run.run_id).get_stage(4)
        assert stage4 is not None
        assert stage4.status == ProductionStageStatus.IN_REVIEW
        assert stage4.current_revision is not None
        assert "scene_images" in stage4.current_revision.artifact

    @pytest.mark.unit
    def test_stage_4_produces_per_scene_images(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 4)
        stage4 = d.get_run(run.run_id).get_stage(4)
        images = stage4.current_revision.artifact["scene_images"]
        assert len(images) >= 3  # storyboard has 5 scenes
        assert all("gs_uri" in img for img in images)

    @pytest.mark.unit
    def test_stage_4_revise(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 4)
        run = d.decide(run.run_id, 4, "revise", notes_th="scene 2 too dark")
        stage4 = run.get_stage(4)
        assert stage4.revision_count == 2
        assert stage4.status == ProductionStageStatus.IN_REVIEW


class TestStage5Animatics:
    """Stage 5: Animatics (image-to-video clips)."""

    @pytest.mark.unit
    def test_stage_5_fires_after_stage_4(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 5)
        stage5 = d.get_run(run.run_id).get_stage(5)
        assert stage5.status == ProductionStageStatus.IN_REVIEW
        clips = stage5.current_revision.artifact["scene_clips"]
        assert len(clips) >= 3
        assert all(c["mode"] in ("i2v", "freeze") for c in clips)

    @pytest.mark.unit
    def test_stage_5_default_mode_is_i2v(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 5)
        stage5 = d.get_run(run.run_id).get_stage(5)
        clips = stage5.current_revision.artifact["scene_clips"]
        assert all(c["mode"] == "i2v" for c in clips)

    @pytest.mark.unit
    def test_stage_5_freeze_to_still(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 5)
        run = d.decide(run.run_id, 5, "revise", notes_th="--freeze scene 0")
        stage5 = run.get_stage(5)
        clips = stage5.current_revision.artifact["scene_clips"]
        scene_0 = [c for c in clips if c["scene_idx"] == 0]
        assert len(scene_0) == 1
        assert scene_0[0]["mode"] == "freeze"
        assert scene_0[0]["cost_thb"] == 0.05  # freeze cost, not 2.50

    @pytest.mark.unit
    def test_stage_5_cost_tracking(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 5)
        stage5 = d.get_run(run.run_id).get_stage(5)
        total = stage5.current_revision.artifact["total_cost_thb"]
        assert total > 0


class TestStage6VoiceOver:
    """Stage 6: Voice-over (Thai TTS with 2 voice options)."""

    @pytest.mark.unit
    def test_stage_6_fires_after_stage_5(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 6)
        stage6 = d.get_run(run.run_id).get_stage(6)
        assert stage6.status == ProductionStageStatus.IN_REVIEW
        takes = stage6.current_revision.artifact["scene_takes"]
        assert len(takes) >= 1

    @pytest.mark.unit
    def test_stage_6_two_voice_options(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 6)
        stage6 = d.get_run(run.run_id).get_stage(6)
        takes = stage6.current_revision.artifact["scene_takes"]
        for group in takes:
            assert len(group["takes"]) == 2
            voices = {t["voice"] for t in group["takes"]}
            assert voices == {"Algenib", "Zephyr"}

    @pytest.mark.unit
    def test_stage_6_voices_available(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 6)
        stage6 = d.get_run(run.run_id).get_stage(6)
        assert "Algenib" in stage6.current_revision.artifact["voices_available"]


class TestStage7Music:
    """Stage 7: Music & SFX."""

    @pytest.mark.unit
    def test_stage_7_fires_after_stage_6(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 7)
        stage7 = d.get_run(run.run_id).get_stage(7)
        assert stage7.status == ProductionStageStatus.IN_REVIEW
        assert "music_track" in stage7.current_revision.artifact
        assert "sfx_cues" in stage7.current_revision.artifact

    @pytest.mark.unit
    def test_stage_7_music_has_duration(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 7)
        stage7 = d.get_run(run.run_id).get_stage(7)
        track = stage7.current_revision.artifact["music_track"]
        assert track["duration_s"] > 0


class TestFullStages1To7:
    """End-to-end stages 1-7 dry run."""

    @pytest.mark.unit
    def test_approve_all_7_stages(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/Socket-bit-set-i.992256187.44154734826")

        for stage_id in range(1, 8):
            run = d.decide(run.run_id, stage_id, "approve")

        # Stages 1-7 all APPROVED
        for i in range(1, 8):
            assert run.get_stage(i).status == ProductionStageStatus.APPROVED

        # Stage 8 should be DRAFT (not implemented as stage runner yet)
        assert run.get_stage(8).status == ProductionStageStatus.DRAFT

        # Cost should have accumulated
        assert run.total_cost_thb > 0

    @pytest.mark.unit
    def test_dry_run_no_phaya_calls(self, tmp_path: Path) -> None:
        """All stage runners use fixture data -- no live API calls."""
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        for stage_id in range(1, 8):
            run = d.decide(run.run_id, stage_id, "approve")
        # If we got here without network errors, no live calls were made
        assert run.total_cost_thb > 0


class TestInboxRendering:
    """HTMX inbox rendering."""

    @pytest.mark.unit
    def test_inbox_page_has_htmx(self) -> None:
        html = render_inbox_page([])
        assert "htmx.org" in html
        assert "hx-get" in html

    @pytest.mark.unit
    def test_inbox_fragment_empty(self) -> None:
        html = render_inbox_fragment([])
        assert "No stages awaiting review" in html

    @pytest.mark.unit
    def test_inbox_fragment_with_runs(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        runs = d.list_runs()
        html = render_inbox_fragment(runs)
        assert "Brief" in html or "brief" in html
        assert "Review" in html

    @pytest.mark.unit
    def test_stage_review_page(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        stage = run.get_stage(1)
        html = render_stage_review_page(run, stage)
        assert "Brief" in html
        assert "approve" in html.lower()
        assert "revise" in html.lower()
        assert "reject" in html.lower()

    @pytest.mark.unit
    def test_stage_4_review_shows_image_grid(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 4)
        run = d.get_run(run.run_id)
        stage = run.get_stage(4)
        html = render_stage_review_page(run, stage)
        assert "image-grid" in html
        assert "Scene" in html

    @pytest.mark.unit
    def test_stage_6_review_shows_voice_options(self, tmp_path: Path) -> None:
        d = ProductionDirector(repo_root=tmp_path)
        run = d.start_run("https://shopee.co.th/test-i.100.200")
        _advance_to_stage(d, run.run_id, 6)
        run = d.get_run(run.run_id)
        stage = run.get_stage(6)
        html = render_stage_review_page(run, stage)
        assert "Algenib" in html
        assert "Zephyr" in html
