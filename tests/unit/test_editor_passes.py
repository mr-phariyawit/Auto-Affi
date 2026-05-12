"""Unit tests for editor standard passes framework (FR-VD-02)."""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_affi.pipeline.editor_passes import (
    AutoSubtitlePass,
    BrandOverlayPass,
    CTAEndcardPass,
    EditorPipelineResult,
    FillerCutPass,
    HookPunchInPass,
    SilenceTrimPass,
    create_default_passes,
    run_editor_pipeline,
)
from auto_affi.pipeline.editor_budget import EditorBudgetTracker
from auto_affi.schemas.storyboard import EditorPass, REQUIRED_EDITOR_PASSES


@pytest.fixture
def sample_video(tmp_path: Path) -> Path:
    """Create a minimal dummy video file for testing pass composition."""
    video = tmp_path / "input.mp4"
    video.write_text("[DUMMY VIDEO CONTENT]")
    return video


@pytest.fixture
def workdir(tmp_path: Path) -> Path:
    wd = tmp_path / "editor_work"
    wd.mkdir()
    return wd


# ------------------------------------------------------------------ #
# individual pass tests                                               #
# ------------------------------------------------------------------ #


@pytest.mark.unit
def test_filler_cut_copies_file(sample_video: Path, workdir: Path) -> None:
    p = FillerCutPass()
    assert p.name is EditorPass.FILLER_CUT
    result = p.apply(sample_video, workdir=workdir)
    assert result.exists()
    assert result.read_text() == sample_video.read_text()


@pytest.mark.unit
def test_auto_subtitle_copies_file(sample_video: Path, workdir: Path) -> None:
    p = AutoSubtitlePass()
    assert p.name is EditorPass.AUTO_SUBTITLE
    result = p.apply(sample_video, workdir=workdir)
    assert result.exists()


@pytest.mark.unit
def test_cta_endcard_copies_file(sample_video: Path, workdir: Path) -> None:
    p = CTAEndcardPass()
    assert p.name is EditorPass.CTA_ENDCARD
    result = p.apply(sample_video, workdir=workdir)
    assert result.exists()


@pytest.mark.unit
def test_hook_punch_in_fallback_copies(sample_video: Path, workdir: Path) -> None:
    """Without ffmpeg available, hook punch-in should gracefully fallback."""
    p = HookPunchInPass()
    assert p.name is EditorPass.HOOK_PUNCH_IN
    result = p.apply(sample_video, workdir=workdir)
    assert result.exists()


@pytest.mark.unit
def test_brand_overlay_fallback_copies(sample_video: Path, workdir: Path) -> None:
    """Without ffmpeg available, brand overlay should gracefully fallback."""
    p = BrandOverlayPass(watermark_text="TestBrand", handle="@test")
    assert p.name is EditorPass.BRAND_OVERLAY
    result = p.apply(sample_video, workdir=workdir)
    assert result.exists()


@pytest.mark.unit
def test_silence_trim_pass_name() -> None:
    p = SilenceTrimPass()
    assert p.name is EditorPass.SILENCE_TRIM
    assert p.estimated_cost == 0.0


# ------------------------------------------------------------------ #
# default pass registry                                               #
# ------------------------------------------------------------------ #


@pytest.mark.unit
def test_create_default_passes_has_all_required() -> None:
    passes = create_default_passes()
    assert len(passes) == 6
    names = [p.name for p in passes]
    for required in REQUIRED_EDITOR_PASSES:
        assert required in names


@pytest.mark.unit
def test_create_default_passes_in_canonical_order() -> None:
    passes = create_default_passes()
    names = [p.name for p in passes]
    expected = list(REQUIRED_EDITOR_PASSES)
    assert names == expected


# ------------------------------------------------------------------ #
# pipeline composition                                                #
# ------------------------------------------------------------------ #


@pytest.mark.unit
def test_run_pipeline_with_passthrough_passes(
    sample_video: Path, workdir: Path
) -> None:
    """Pipeline with copy-only passes (no ffmpeg needed)."""
    passes = [
        FillerCutPass(),
        AutoSubtitlePass(),
        CTAEndcardPass(),
    ]
    result = run_editor_pipeline(
        sample_video, workdir=workdir, passes=passes  # type: ignore[arg-type]
    )
    assert result.output_path.exists()
    assert len(result.passes_applied) == 3
    assert result.total_cost_usd == 0.0


@pytest.mark.unit
def test_run_pipeline_output_is_last_pass_output(
    sample_video: Path, workdir: Path
) -> None:
    passes = [FillerCutPass(), CTAEndcardPass()]
    result = run_editor_pipeline(
        sample_video, workdir=workdir, passes=passes  # type: ignore[arg-type]
    )
    # Output should be the CTA pass output (last in chain)
    assert "cta" in result.output_path.stem


@pytest.mark.unit
def test_run_pipeline_with_budget_tracker(
    sample_video: Path, workdir: Path
) -> None:
    budget = EditorBudgetTracker(budget_usd=0.40)
    passes = [FillerCutPass(), AutoSubtitlePass()]
    result = run_editor_pipeline(
        sample_video,
        workdir=workdir,
        passes=passes,  # type: ignore[arg-type]
        budget=budget,
    )
    status = budget.status()
    assert status.pass_count == 2
    assert status.spent_usd == 0.0  # All Phase 1 passes are free


@pytest.mark.unit
def test_run_pipeline_empty_passes(
    sample_video: Path, workdir: Path
) -> None:
    result = run_editor_pipeline(
        sample_video, workdir=workdir, passes=[]
    )
    assert result.output_path == sample_video
    assert result.passes_applied == []
    assert result.passes_skipped == []


@pytest.mark.unit
def test_pipeline_result_structure() -> None:
    result = EditorPipelineResult(
        output_path=Path("/tmp/out.mp4"),
        passes_applied=["silence_trim", "filler_cut"],
        passes_skipped=["hook_punch_in"],
        total_cost_usd=0.05,
    )
    assert len(result.passes_applied) == 2
    assert len(result.passes_skipped) == 1
    assert result.total_cost_usd == 0.05
