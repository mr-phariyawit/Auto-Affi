"""The Higgsfield adapter must refuse to generate without a cleared PGA gate."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from auto_affi.adapters.higgsfield_cli import HiggsfieldCli
from auto_affi.pipeline.prompt_audit import (
    GenerationBlocked,
    ReferenceManifest,
    audit,
    record_approval,
    record_audit,
    record_bypass,
)

_IDENTITY = "JIAP02, lean athletic Southeast Asian male"


def _manifest() -> ReferenceManifest:
    return ReferenceManifest(
        prompt=f"{_IDENTITY}. Product orbit shot.",
        identity_string=_IDENTITY,
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


def _clear_all_but_video(run_dir: Path) -> None:
    """Approve every stage that precedes 'video' so ordering is satisfied."""
    for stage in ("cast_sheet", "objects_sheet", "storyboard", "contact_sheet"):
        record_audit(run_dir, stage, audit(_manifest()))
        record_approval(run_dir, stage)


@pytest.mark.unit
def test_generate_video_blocked_when_run_dir_has_no_approval(tmp_path: Path) -> None:
    cli = HiggsfieldCli(dry_run=True)
    with pytest.raises(GenerationBlocked):
        asyncio.run(
            cli.generate_video(model="seedance_2_0", prompt="x", run_dir=tmp_path)
        )


@pytest.mark.unit
def test_generate_video_allowed_after_full_approval(tmp_path: Path) -> None:
    _clear_all_but_video(tmp_path)
    record_audit(tmp_path, "video", audit(_manifest()))
    record_approval(tmp_path, "video")

    cli = HiggsfieldCli(dry_run=True)
    result = asyncio.run(
        cli.generate_video(model="seedance_2_0", prompt="x", run_dir=tmp_path)
    )
    assert result.cost_usd == 0.0  # dry-run stub returned, gate passed


@pytest.mark.unit
def test_generate_video_respects_explicit_bypass(tmp_path: Path) -> None:
    for stage in ("cast_sheet", "objects_sheet", "storyboard", "contact_sheet", "video"):
        record_bypass(tmp_path, stage, reason="operator override")
    cli = HiggsfieldCli(dry_run=True)
    # Should not raise — every stage explicitly bypassed.
    asyncio.run(cli.generate_video(model="seedance_2_0", prompt="x", run_dir=tmp_path))


@pytest.mark.unit
def test_generate_video_unguarded_without_run_dir(tmp_path: Path) -> None:
    # Backward-compat: omitting run_dir keeps the legacy dry-run behaviour.
    cli = HiggsfieldCli(dry_run=True)
    result = asyncio.run(cli.generate_video(model="seedance_2_0", prompt="x"))
    assert result.cost_usd == 0.0
