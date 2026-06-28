"""GeminiProvider — PGA gate + verify-before-spend on the Gemini path (ADR-009).

Live API methods (_image_api/_video_api) are patched so no network is touched.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import patch

import pytest

from auto_affi.adapters.gemini_provider import GeminiProvider
from auto_affi.adapters.gen_provider import GenAsset, ProviderSpendError
from auto_affi.pipeline.prompt_audit import (
    STAGES,
    GenerationBlocked,
    ReferenceManifest,
    audit,
    record_approval,
    record_audit,
    record_bypass,
)
from auto_affi.workflows.budget import BudgetCircuitBreaker

_IDENTITY = "JIAP02 lean athletic Southeast Asian male"


def _m(prompt: str = f"{_IDENTITY}, product orbit") -> ReferenceManifest:
    return ReferenceManifest(
        prompt=prompt, identity_string="JIAP02",
        cast_sheet_approved=True, objects_sheet_approved=True,
        declared_objects=["product"], scene_objects=["product"],
        face_reference_count=1, negative_prompt="different person, extra limbs",
        aspect="9:16", resolution="720p", duration_s=4.0, soul_id="soul-x",
    )


def _clear(run_dir: Path, stage: str, manifest: ReferenceManifest) -> None:
    for prior in STAGES[: STAGES.index(stage)]:
        record_bypass(run_dir, prior, reason="prior")
    record_audit(run_dir, stage, audit(manifest))
    record_approval(run_dir, stage, approved_by="op")


def _patch_apis(tmp_path: Path):
    async def fake_image(self, model, prompt, refs, aspect, run_dir, stage):
        return (run_dir or tmp_path) / f"{stage}.png"

    async def fake_video(self, model, prompt, duration, aspect, run_dir, stage):
        return (run_dir or tmp_path) / f"{stage}.mp4"

    return (
        patch.object(GeminiProvider, "_image_api", fake_image),
        patch.object(GeminiProvider, "_video_api", fake_video),
    )


# --------------------------- dry-run (offline/free) ---------------------- #


@pytest.mark.unit
def test_dry_run_image_is_free_stub_after_gate(tmp_path: Path) -> None:
    m = _m()
    _clear(tmp_path, "cast_sheet", m)
    p = GeminiProvider(dry_run=True)
    a = asyncio.run(p.generate_image(stage="cast_sheet", prompt=m.prompt, run_dir=tmp_path, manifest=m))
    assert isinstance(a, GenAsset) and a.kind == "image" and a.cost_usd == 0.0


@pytest.mark.unit
def test_dry_run_does_not_require_key() -> None:
    GeminiProvider(dry_run=True)  # no key needed offline


@pytest.mark.unit
def test_live_provider_requires_key() -> None:
    with pytest.raises(ProviderSpendError, match="GEMINI_API_KEY"):
        GeminiProvider(dry_run=False, api_key=None)


# --------------------------- gate enforcement ---------------------------- #


@pytest.mark.unit
def test_image_blocked_without_approval(tmp_path: Path) -> None:
    p = GeminiProvider(dry_run=True)
    with pytest.raises(GenerationBlocked):
        asyncio.run(p.generate_image(stage="cast_sheet", prompt="x", run_dir=tmp_path, manifest=_m()))


@pytest.mark.unit
def test_live_requires_run_dir(tmp_path: Path) -> None:
    img, vid = _patch_apis(tmp_path)
    with img, vid:
        p = GeminiProvider(dry_run=False, api_key="k")
        with pytest.raises(GenerationBlocked, match="requires run_dir"):
            asyncio.run(p.generate_image(stage="cast_sheet", prompt="x", manifest=_m(),
                                         budget=BudgetCircuitBreaker()))


@pytest.mark.unit
def test_live_requires_manifest(tmp_path: Path) -> None:
    m = _m()
    _clear(tmp_path, "cast_sheet", m)
    img, vid = _patch_apis(tmp_path)
    with img, vid:
        p = GeminiProvider(dry_run=False, api_key="k")
        with pytest.raises(GenerationBlocked, match="requires a manifest"):
            asyncio.run(p.generate_image(stage="cast_sheet", prompt="x", run_dir=tmp_path,
                                         budget=BudgetCircuitBreaker()))


@pytest.mark.unit
def test_live_requires_budget(tmp_path: Path) -> None:
    m = _m()
    _clear(tmp_path, "cast_sheet", m)
    img, vid = _patch_apis(tmp_path)
    with img, vid:
        p = GeminiProvider(dry_run=False, api_key="k")
        with pytest.raises(ProviderSpendError, match="requires a BudgetCircuitBreaker"):
            asyncio.run(p.generate_image(stage="cast_sheet", prompt=m.prompt, run_dir=tmp_path, manifest=m))


@pytest.mark.unit
def test_live_blocked_on_manifest_hash_mismatch(tmp_path: Path) -> None:
    approved = _m("JIAP02, scene A")
    _clear(tmp_path, "cast_sheet", approved)
    img, vid = _patch_apis(tmp_path)
    with img, vid:
        p = GeminiProvider(dry_run=False, api_key="k")
        tampered = _m("JIAP02, scene B")
        with pytest.raises(GenerationBlocked, match="hash mismatch"):
            asyncio.run(p.generate_image(stage="cast_sheet", prompt="x", run_dir=tmp_path,
                                         manifest=tampered, budget=BudgetCircuitBreaker()))


# --------------------------- verify-before-spend ------------------------- #


@pytest.mark.unit
def test_live_image_records_real_cost_and_spends(tmp_path: Path) -> None:
    m = _m()
    _clear(tmp_path, "cast_sheet", m)
    breaker = BudgetCircuitBreaker()
    img, vid = _patch_apis(tmp_path)
    with img, vid:
        p = GeminiProvider(dry_run=False, api_key="k")
        a = asyncio.run(p.generate_image(stage="cast_sheet", prompt=m.prompt, run_dir=tmp_path,
                                         manifest=m, budget=breaker))
    assert a.cost_usd > 0.0 and a.cost_estimated
    assert breaker.node_spent("image_gen") > 0.0


@pytest.mark.unit
def test_live_video_short_clip_proceeds(tmp_path: Path) -> None:
    m = _m()
    _clear(tmp_path, "video", m)
    breaker = BudgetCircuitBreaker()
    img, vid = _patch_apis(tmp_path)
    with img, vid:
        p = GeminiProvider(dry_run=False, api_key="k")
        a = asyncio.run(p.generate_video(stage="video", prompt=m.prompt, duration=4, run_dir=tmp_path,
                                         manifest=m, budget=breaker))
    assert a.kind == "video" and a.cost_usd > 0.0
    assert breaker.node_spent("video_gen") > 0.0


@pytest.mark.unit
def test_live_long_veo_clip_denied_over_budget(tmp_path: Path) -> None:
    # Veo 3 is pricey: 8s ~ $3.20 exceeds the $1.80 video_gen node cap -> DENY.
    m = _m()
    _clear(tmp_path, "video", m)
    img, vid = _patch_apis(tmp_path)
    with img, vid:
        p = GeminiProvider(dry_run=False, api_key="k")
        with pytest.raises(ProviderSpendError, match="budget breaker DENY"):
            asyncio.run(p.generate_video(stage="video", prompt=m.prompt, duration=8, run_dir=tmp_path,
                                         manifest=m, budget=BudgetCircuitBreaker()))
