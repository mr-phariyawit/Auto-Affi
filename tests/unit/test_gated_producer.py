"""Integration: the gated producer spends THROUGH the guard (GAP-B, on Gemini).

Proves a (mocked) live run drives image + video generation via the gate: each stage
calls assert_may_generate, and non-zero estimated cost reaches the budget breaker —
not 0.0. Provider is GeminiProvider; the live API methods are patched (no network).
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from auto_affi.adapters.gemini_provider import GeminiProvider
from auto_affi.adapters.gen_provider import GenAsset
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
_STAGES = [
    ("cast_sheet", StageKind.IMAGE),
    ("objects_sheet", StageKind.IMAGE),
    ("storyboard", StageKind.IMAGE),
    ("contact_sheet", StageKind.IMAGE),
    ("video", StageKind.VIDEO),
]


def _manifest(stage: str) -> ReferenceManifest:
    return ReferenceManifest(
        prompt=f"{_IDENTITY}. {stage} of a purple product, sunlit.",
        identity_string=_IDENTITY,
        cast_sheet_approved=True, objects_sheet_approved=True,
        declared_objects=["purple product"], scene_objects=["purple product"],
        face_reference_count=1,
        negative_prompt="different person, wrong face, extra limbs, watermark",
        aspect="9:16", resolution="720p", duration_s=4.0, soul_id="soul-x",
    )


def _plans() -> list[StagePlan]:
    return [
        StagePlan(stage=s, kind=k, manifest=_manifest(s), duration=4)
        for s, k in _STAGES
    ]


def _approve_all(run_dir: Path, plans: list[StagePlan]) -> None:
    for plan in plans:
        record_audit(run_dir, plan.stage, audit(plan.manifest))
        record_approval(run_dir, plan.stage, approved_by="operator:alice")


def _live_provider_patches(tmp_path: Path):
    """Patch the GeminiProvider live API methods so no network is hit."""
    async def fake_image(self, model, prompt, refs, aspect, run_dir, stage):
        return (run_dir or tmp_path) / f"{stage}.png"

    async def fake_video(self, model, prompt, duration, aspect, run_dir, stage):
        return (run_dir or tmp_path) / f"{stage}.mp4"

    return (
        patch.object(GeminiProvider, "_image_api", fake_image),
        patch.object(GeminiProvider, "_video_api", fake_video),
    )


@pytest.mark.unit
def test_live_run_spends_through_the_guard(tmp_path: Path) -> None:
    plans = _plans()
    _approve_all(tmp_path, plans)
    breaker = BudgetCircuitBreaker()

    import auto_affi.adapters.gen_provider as _gp
    real_amg = _gp.assert_may_generate
    gate_calls: list[str] = []

    def _spy(stage: str, run_dir: Path, *, manifest: object = None) -> None:
        gate_calls.append(stage)
        real_amg(stage, run_dir, manifest=manifest)  # type: ignore[arg-type]

    img, vid = _live_provider_patches(tmp_path)
    with img, vid, patch.object(_gp, "assert_may_generate", side_effect=_spy):
        provider = GeminiProvider(dry_run=False, api_key="test-key")
        producer = GatedProducer(provider=provider, run_dir=tmp_path, budget=breaker)
        results = asyncio.run(producer.produce_all(plans))

    assert gate_calls == ["cast_sheet", "objects_sheet", "storyboard", "contact_sheet", "video"]
    assert len(results) == 5
    assert all(isinstance(r, GenAsset) for r in results)
    assert all(r.cost_usd > 0.0 and r.cost_estimated for r in results)
    assert breaker.node_spent("image_gen") > 0.0
    assert breaker.node_spent("video_gen") > 0.0


@pytest.mark.unit
def test_producer_blocks_unapproved_stage(tmp_path: Path) -> None:
    plans = _plans()
    record_audit(tmp_path, "cast_sheet", audit(plans[0].manifest))
    record_approval(tmp_path, "cast_sheet", approved_by="op")  # only first approved
    img, vid = _live_provider_patches(tmp_path)
    with img, vid, patch.object(GeminiProvider, "_image_api", AsyncMock()):
        provider = GeminiProvider(dry_run=False, api_key="test-key")
        producer = GatedProducer(provider=provider, run_dir=tmp_path, budget=BudgetCircuitBreaker())
        with pytest.raises(GenerationBlocked):
            asyncio.run(producer.produce_all(plans))


@pytest.mark.unit
def test_dry_run_producer_is_offline_and_free_but_still_gated(tmp_path: Path) -> None:
    plans = _plans()
    _approve_all(tmp_path, plans)
    breaker = BudgetCircuitBreaker()
    provider = GeminiProvider(dry_run=True)
    producer = GatedProducer(provider=provider, run_dir=tmp_path, budget=breaker)
    results = asyncio.run(producer.produce_all(plans))
    assert len(results) == 5
    assert all(r.cost_usd == 0.0 for r in results)
    assert breaker.node_spent("video_gen") == 0.0


@pytest.mark.unit
def test_dry_run_producer_still_blocks_unapproved_stage(tmp_path: Path) -> None:
    plans = _plans()  # nothing approved
    provider = GeminiProvider(dry_run=True)
    producer = GatedProducer(provider=provider, run_dir=tmp_path, budget=BudgetCircuitBreaker())
    with pytest.raises(GenerationBlocked):
        asyncio.run(producer.produce_stage(plans[0]))


@pytest.mark.unit
def test_stageplan_rejects_kind_stage_mismatch() -> None:
    m = _manifest("video")
    with pytest.raises(ValueError, match="VIDEO kind"):
        StagePlan(stage="cast_sheet", kind=StageKind.VIDEO, manifest=m)
    with pytest.raises(ValueError, match="VIDEO kind"):
        StagePlan(stage="video", kind=StageKind.IMAGE, manifest=m)
