"""Integration: the gated producer spends THROUGH the guard (Audit Lead GAP-B).

Proves that a (mocked) live run drives image + video generation via the gate:
each stage calls assert_may_generate, the credit check runs, and non-zero
estimated cost reaches the budget breaker — not the old hardcoded 0.0.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from auto_affi.adapters.higgsfield_cli import HiggsfieldCli, HiggsfieldImage, HiggsfieldVideo
from auto_affi.ops.produce import GatedProducer, StageKind, StagePlan
from auto_affi.pipeline.prompt_audit import (
    GenerationBlocked,
    ReferenceManifest,
    audit,
    record_approval,
    record_audit,
)
from auto_affi.workflows.budget import BudgetCircuitBreaker

_IDENTITY = "JIAP02, lean athletic Southeast Asian male"

_STAGE_MODELS = {
    "cast_sheet": ("nano_banana_2", StageKind.IMAGE),
    "objects_sheet": ("nano_banana_2", StageKind.IMAGE),
    "storyboard": ("nano_banana_2", StageKind.IMAGE),
    "contact_sheet": ("nano_banana_2", StageKind.IMAGE),
    "video": ("seedance_2_0", StageKind.VIDEO),
}


def _manifest(stage: str) -> ReferenceManifest:
    return ReferenceManifest(
        prompt=f"{_IDENTITY}. {stage} of a purple product, sunlit.",
        identity_string=_IDENTITY,
        cast_sheet_approved=True,
        objects_sheet_approved=True,
        declared_objects=["purple product"],
        scene_objects=["purple product"],
        face_reference_count=1,
        negative_prompt="different person, wrong face, extra limbs, watermark",
        aspect="9:16",
        resolution="720p",
        duration_s=8.0,
        soul_id="soul-jiap02",
    )


def _plans() -> list[StagePlan]:
    plans: list[StagePlan] = []
    for stage, (model, kind) in _STAGE_MODELS.items():
        plans.append(StagePlan(stage=stage, kind=kind, model=model, manifest=_manifest(stage)))
    return plans


def _approve_all(run_dir: Path, plans: list[StagePlan]) -> None:
    """Human-approve every stage (audit recorded + approved, both logged)."""
    for plan in plans:
        record_audit(run_dir, plan.stage, audit(plan.manifest))
        record_approval(run_dir, plan.stage, approved_by="operator:alice")


def _live_cli_patches(stdout: str = "https://cdn.example.com/asset\n"):
    async def fake_create(prog: str, *args: str, **kw: object) -> MagicMock:
        proc = MagicMock()
        proc.returncode = 0
        proc.communicate = AsyncMock(return_value=(stdout.encode(), b""))
        return proc

    import auto_affi.adapters.higgsfield_cli as _mod
    return (
        patch.object(_mod.shutil, "which", return_value="/x/hf"),
        patch.object(_mod.asyncio, "create_subprocess_exec", side_effect=fake_create),
    )


@pytest.mark.unit
def test_live_run_spends_through_the_guard(tmp_path: Path) -> None:
    plans = _plans()
    _approve_all(tmp_path, plans)
    breaker = BudgetCircuitBreaker()
    which, sub = _live_cli_patches()
    credits = AsyncMock(return_value=99999.0)
    with which, sub, patch.object(HiggsfieldCli, "account_credits", credits):
        cli = HiggsfieldCli(dry_run=False)
        producer = GatedProducer(cli=cli, run_dir=tmp_path, budget=breaker)
        results = asyncio.run(producer.produce_all(plans))

    assert len(results) == 5
    images = [r for r in results if isinstance(r, HiggsfieldImage)]
    videos = [r for r in results if isinstance(r, HiggsfieldVideo)]
    assert len(images) == 4 and len(videos) == 1
    # Real (estimated) cost reached the results AND the breaker — not 0.0.
    assert all(r.cost_usd > 0.0 and r.cost_estimated for r in results)
    assert breaker.node_spent("image_gen") > 0.0
    assert breaker.node_spent("video_gen") > 0.0
    # The credit check ran for every paid call (verify-before-spend).
    assert credits.await_count == 5


@pytest.mark.unit
def test_producer_blocks_unapproved_stage(tmp_path: Path) -> None:
    plans = _plans()
    # Approve only the first stage; the second is un-approved.
    record_audit(tmp_path, "cast_sheet", audit(plans[0].manifest))
    record_approval(tmp_path, "cast_sheet", approved_by="op")
    breaker = BudgetCircuitBreaker()
    which, sub = _live_cli_patches()
    with which, sub, patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=99999.0)):
        cli = HiggsfieldCli(dry_run=False)
        producer = GatedProducer(cli=cli, run_dir=tmp_path, budget=breaker)
        with pytest.raises(GenerationBlocked):
            asyncio.run(producer.produce_all(plans))


@pytest.mark.unit
def test_dry_run_producer_is_offline_and_free_but_still_gated(tmp_path: Path) -> None:
    plans = _plans()
    _approve_all(tmp_path, plans)
    breaker = BudgetCircuitBreaker()
    cli = HiggsfieldCli(dry_run=True)  # default offline
    producer = GatedProducer(cli=cli, run_dir=tmp_path, budget=breaker)
    results = asyncio.run(producer.produce_all(plans))
    assert len(results) == 5
    assert all(r.cost_usd == 0.0 for r in results)  # dry-run free
    assert breaker.node_spent("video_gen") == 0.0


@pytest.mark.unit
def test_dry_run_producer_still_blocks_unapproved_stage(tmp_path: Path) -> None:
    plans = _plans()  # nothing approved
    cli = HiggsfieldCli(dry_run=True)
    producer = GatedProducer(cli=cli, run_dir=tmp_path, budget=BudgetCircuitBreaker())
    with pytest.raises(GenerationBlocked):
        asyncio.run(producer.produce_stage(plans[0]))


@pytest.mark.unit
def test_stageplan_rejects_kind_stage_mismatch() -> None:
    m = _manifest("video")
    with pytest.raises(ValueError, match="VIDEO kind"):
        StagePlan(stage="cast_sheet", kind=StageKind.VIDEO, model="seedance_2_0", manifest=m)
    with pytest.raises(ValueError, match="VIDEO kind"):
        StagePlan(stage="video", kind=StageKind.IMAGE, model="nano_banana_2", manifest=m)
