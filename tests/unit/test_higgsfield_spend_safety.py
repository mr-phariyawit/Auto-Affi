"""Verify-before-spend + image-stage gating for the Higgsfield adapter.

Closes Audit Lead gaps #3 (image stages ungated) and #4 (credit check unwired,
live cost hardcoded $0.00). See reports/2026-06-27_crew-review-findings.md.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from auto_affi.adapters.higgsfield_cli import (
    HiggsfieldCli,
    HiggsfieldCliError,
    HiggsfieldImage,
    _parse_credit_balance,
)
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


def _fake_proc(stdout: str, returncode: int = 0) -> MagicMock:
    proc = MagicMock()
    proc.returncode = returncode
    proc.communicate = AsyncMock(return_value=(stdout.encode(), b""))
    return proc


def _cleared(run_dir: Path) -> None:
    for stage in STAGES:
        record_bypass(run_dir, stage, reason="test fixture: gate pre-cleared")


def _m() -> ReferenceManifest:
    """A clean, audit-passing manifest for live calls (manifest is now mandatory)."""
    return ReferenceManifest(
        prompt="JIAP02 product orbit, sunlit",
        identity_string="JIAP02",
        cast_sheet_approved=True,
        objects_sheet_approved=True,
        declared_objects=["product"],
        scene_objects=["product"],
        face_reference_count=1,
        negative_prompt="different person, extra limbs, watermark",
        aspect="9:16",
        resolution="720p",
        duration_s=8.0,
        soul_id="soul-x",
    )


def _clear_for(run_dir: Path, stage: str, manifest: ReferenceManifest) -> None:
    """Bypass prior stages and audit+approve the target bound to ``manifest``'s hash."""
    idx = STAGES.index(stage)
    for prior in STAGES[:idx]:
        record_bypass(run_dir, prior, reason="prior")
    record_audit(run_dir, stage, audit(manifest))
    record_approval(run_dir, stage, approved_by="op")


def _live_subprocess(stdout: str = "https://cdn.example.com/out.mp4\n"):
    async def fake_create(prog: str, *args: str, **kw: object) -> MagicMock:
        return _fake_proc(stdout)

    import auto_affi.adapters.higgsfield_cli as _mod
    return (
        patch.object(_mod.shutil, "which", return_value="/x/hf"),
        patch.object(_mod.asyncio, "create_subprocess_exec", side_effect=fake_create),
    )


# --------------------------- credit gate --------------------------------- #


@pytest.mark.unit
def test_live_video_blocked_on_insufficient_credits(tmp_path: Path) -> None:
    m = _m()
    _clear_for(tmp_path, "video", m)
    which, sub = _live_subprocess()
    with which, sub, patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=10.0)):
        cli = HiggsfieldCli(dry_run=False)
        with pytest.raises(HiggsfieldCliError, match="insufficient Higgsfield credits"):
            asyncio.run(
                cli.generate_video(
                    model="seedance_2_0",
                    prompt=m.prompt,
                    duration=8,
                    run_dir=tmp_path,
                    manifest=m,
                    budget=BudgetCircuitBreaker(),
                )
            )  # 8s ~= 164 credits required, only 10 available


@pytest.mark.unit
def test_live_video_proceeds_when_credits_sufficient(tmp_path: Path) -> None:
    m = _m()
    _clear_for(tmp_path, "video", m)
    which, sub = _live_subprocess()
    breaker = BudgetCircuitBreaker()
    with which, sub, patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=9999.0)):
        cli = HiggsfieldCli(dry_run=False)
        result = asyncio.run(
            cli.generate_video(
                model="seedance_2_0",
                prompt=m.prompt,
                duration=8,
                run_dir=tmp_path,
                manifest=m,
                budget=breaker,
            )
        )
    assert result.video_url == "https://cdn.example.com/out.mp4"
    # real cost recorded, not the old hardcoded 0.0
    assert result.cost_usd > 0.0
    assert result.cost_estimated is True
    assert breaker.node_spent("video_gen") > 0.0  # spend reached the breaker


@pytest.mark.unit
def test_live_requires_budget_fail_closed(tmp_path: Path) -> None:
    """The budget breaker is mandatory on the live path (Audit Lead GAP-C)."""
    m = _m()
    _clear_for(tmp_path, "video", m)
    which, sub = _live_subprocess()
    with which, sub, patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=9999.0)):
        cli = HiggsfieldCli(dry_run=False)
        with pytest.raises(HiggsfieldCliError, match="requires a BudgetCircuitBreaker"):
            asyncio.run(
                cli.generate_video(
                    model="seedance_2_0", prompt=m.prompt, duration=8, run_dir=tmp_path, manifest=m
                )
            )


# --------------------------- budget breaker ------------------------------ #


@pytest.mark.unit
def test_live_video_blocked_when_over_budget(tmp_path: Path) -> None:
    m = _m()
    _clear_for(tmp_path, "video", m)
    breaker = BudgetCircuitBreaker()
    # Drive daily spend to the cap so the next job is DENY.
    breaker.record_spend("video_gen", breaker.daily_cap * 1.1)
    which, sub = _live_subprocess()
    with which, sub, patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=9999.0)):
        cli = HiggsfieldCli(dry_run=False)
        with pytest.raises(HiggsfieldCliError, match="budget breaker DENY"):
            asyncio.run(
                cli.generate_video(
                    model="seedance_2_0",
                    prompt=m.prompt,
                    duration=8,
                    run_dir=tmp_path,
                    manifest=m,
                    budget=breaker,
                )
            )


# --------------------------- image-stage gate ---------------------------- #


@pytest.mark.unit
def test_live_image_blocked_when_over_budget(tmp_path: Path) -> None:
    """Mirror of the video over-budget test for the image_gen node (Audit follow-up)."""
    m = _m()
    _clear_for(tmp_path, "cast_sheet", m)
    breaker = BudgetCircuitBreaker()
    breaker.record_spend("image_gen", breaker.node_caps["image_gen"])  # at the node cap
    which, sub = _live_subprocess("https://cdn.example.com/still.png\n")
    with which, sub, patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=9999.0)):
        cli = HiggsfieldCli(dry_run=False)
        with pytest.raises(HiggsfieldCliError, match="budget breaker DENY"):
            asyncio.run(
                cli.generate_image(
                    model="nano_banana_2",
                    prompt=m.prompt,
                    stage="cast_sheet",
                    run_dir=tmp_path,
                    manifest=m,
                    budget=breaker,
                )
            )


@pytest.mark.unit
def test_live_requires_manifest_fail_closed(tmp_path: Path) -> None:
    """A live (paid) call without a manifest is blocked — the approval-to-content
    hash binding cannot be skipped (Audit Lead GAP-E)."""
    m = _m()
    _clear_for(tmp_path, "video", m)
    which, sub = _live_subprocess()
    with which, sub, patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=9999.0)):
        cli = HiggsfieldCli(dry_run=False)
        with pytest.raises(GenerationBlocked, match="requires a manifest"):
            asyncio.run(
                cli.generate_video(
                    model="seedance_2_0",
                    prompt=m.prompt,
                    duration=8,
                    run_dir=tmp_path,
                    budget=BudgetCircuitBreaker(),
                )
            )


@pytest.mark.unit
def test_generate_image_blocked_without_approval(tmp_path: Path) -> None:
    cli = HiggsfieldCli(dry_run=True)
    with pytest.raises(GenerationBlocked):
        asyncio.run(
            cli.generate_image(
                model="nano_banana_2", prompt="cast sheet", stage="cast_sheet", run_dir=tmp_path
            )
        )


@pytest.mark.unit
def test_generate_image_live_requires_run_dir_fail_closed() -> None:
    import auto_affi.adapters.higgsfield_cli as _mod
    with patch.object(_mod.shutil, "which", return_value="/x/hf"):
        cli = HiggsfieldCli(dry_run=False)
        with pytest.raises(GenerationBlocked, match="requires run_dir"):
            asyncio.run(
                cli.generate_image(model="nano_banana_2", prompt="x", stage="cast_sheet")
            )


@pytest.mark.unit
def test_generate_image_dry_run_returns_stub_after_gate(tmp_path: Path) -> None:
    _cleared(tmp_path)
    cli = HiggsfieldCli(dry_run=True)
    result = asyncio.run(
        cli.generate_image(
            model="nano_banana_2", prompt="cast sheet", stage="cast_sheet", run_dir=tmp_path
        )
    )
    assert isinstance(result, HiggsfieldImage)
    assert result.cost_usd == 0.0
    assert result.image_url == ""


# --------------------- credit parser: fail-closed (GAP-A) ---------------- #


@pytest.mark.unit
def test_parse_credit_balance_handles_grouped_digits() -> None:
    assert _parse_credit_balance("Credits: 1,234") == 1234.0
    assert _parse_credit_balance("5000 credits available") == 5000.0


@pytest.mark.unit
def test_parse_credit_balance_is_conservative_not_wraparound() -> None:
    # Old parser wrapped tokens[i-1] -> read the wrong (overstated) number.
    # New parser picks the number bound to 'credit', biased to the minimum,
    # so "12 used of 5000" never overstates available balance.
    assert _parse_credit_balance("Credits 12 used of 5000") == 12.0


@pytest.mark.unit
def test_parse_credit_balance_fails_closed_on_unparseable() -> None:
    with pytest.raises(HiggsfieldCliError, match="fail-closed"):
        _parse_credit_balance("Account: active\nPlan: pro\n")


# --------------------- hash-binding on the generate path (GAP-D) --------- #


def _manifest(prompt: str) -> ReferenceManifest:
    return ReferenceManifest(
        prompt=prompt,
        identity_string="JIAP02",
        cast_sheet_approved=True,
        objects_sheet_approved=True,
        declared_objects=["product"],
        scene_objects=["product"],
        face_reference_count=1,
        negative_prompt="different person, extra limbs",
        aspect="9:16",
        resolution="720p",
        duration_s=8.0,
        soul_id="soul-x",
    )


@pytest.mark.unit
def test_generate_blocked_when_manifest_differs_from_approval(tmp_path: Path) -> None:
    # Approve the video stage for manifest A (priors bypassed for ordering).
    for stage in ("cast_sheet", "objects_sheet", "storyboard", "contact_sheet"):
        record_bypass(tmp_path, stage, reason="fixture")
    approved = _manifest("JIAP02 holding the product, sunlit")
    record_audit(tmp_path, "video", audit(approved))
    record_approval(tmp_path, "video")

    cli = HiggsfieldCli(dry_run=True)
    tampered = _manifest("JIAP02 in a totally different scene")
    with pytest.raises(GenerationBlocked, match="hash mismatch"):
        asyncio.run(
            cli.generate_video(
                model="seedance_2_0", prompt="x", run_dir=tmp_path, manifest=tampered
            )
        )
