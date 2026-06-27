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
)
from auto_affi.pipeline.prompt_audit import STAGES, GenerationBlocked, record_bypass
from auto_affi.workflows.budget import BudgetCircuitBreaker


def _fake_proc(stdout: str, returncode: int = 0) -> MagicMock:
    proc = MagicMock()
    proc.returncode = returncode
    proc.communicate = AsyncMock(return_value=(stdout.encode(), b""))
    return proc


def _cleared(run_dir: Path) -> None:
    for stage in STAGES:
        record_bypass(run_dir, stage, reason="test fixture: gate pre-cleared")


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
    _cleared(tmp_path)
    which, sub = _live_subprocess()
    with which, sub, patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=10.0)):
        cli = HiggsfieldCli(dry_run=False)
        with pytest.raises(HiggsfieldCliError, match="insufficient Higgsfield credits"):
            asyncio.run(
                cli.generate_video(
                    model="seedance_2_0", prompt="x", duration=8, run_dir=tmp_path
                )
            )  # 8s ~= 164 credits required, only 10 available


@pytest.mark.unit
def test_live_video_proceeds_when_credits_sufficient(tmp_path: Path) -> None:
    _cleared(tmp_path)
    which, sub = _live_subprocess()
    with which, sub, patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=9999.0)):
        cli = HiggsfieldCli(dry_run=False)
        result = asyncio.run(
            cli.generate_video(model="seedance_2_0", prompt="x", duration=8, run_dir=tmp_path)
        )
    assert result.video_url == "https://cdn.example.com/out.mp4"
    # real cost recorded, not the old hardcoded 0.0
    assert result.cost_usd > 0.0
    assert result.cost_estimated is True


# --------------------------- budget breaker ------------------------------ #


@pytest.mark.unit
def test_live_video_blocked_when_over_budget(tmp_path: Path) -> None:
    _cleared(tmp_path)
    breaker = BudgetCircuitBreaker()
    # Drive daily spend to the cap so the next job is DENY.
    breaker.record_spend("video_gen", breaker.daily_cap * 1.1)
    which, sub = _live_subprocess()
    with which, sub, patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=9999.0)):
        cli = HiggsfieldCli(dry_run=False)
        with pytest.raises(HiggsfieldCliError, match="budget breaker DENY"):
            asyncio.run(
                cli.generate_video(
                    model="seedance_2_0", prompt="x", duration=8, run_dir=tmp_path, budget=breaker
                )
            )


# --------------------------- image-stage gate ---------------------------- #


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
