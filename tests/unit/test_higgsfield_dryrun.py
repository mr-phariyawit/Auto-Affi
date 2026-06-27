"""Tests for Higgsfield dry-run wrapper.

Verifies that dry_run=True (the default) returns a deterministic stub
and makes ZERO subprocess calls. The live subprocess path is tested with
mocks to keep the suite offline.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from auto_affi.adapters.higgsfield_cli import (
    HiggsfieldCli,
    HiggsfieldCliError,
    HiggsfieldVideo,
)
from auto_affi.workflows.budget import BudgetCircuitBreaker

# ---------------------------------------------------------------------------
# dry_run=True (default) — no subprocess, no network
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_dry_run_default_is_true() -> None:
    """HiggsfieldCli() with no args must default to dry_run=True."""
    # Should not raise even though 'higgsfield' binary is not on PATH
    cli = HiggsfieldCli()
    assert cli._dry_run is True


@pytest.mark.unit
def test_dry_run_returns_higgsfield_video() -> None:
    cli = HiggsfieldCli(dry_run=True)
    result = asyncio.run(
        cli.generate_video(model="seedance_2_0", prompt="test product orbit")
    )
    assert isinstance(result, HiggsfieldVideo)


@pytest.mark.unit
def test_dry_run_cost_is_zero() -> None:
    cli = HiggsfieldCli(dry_run=True)
    result = asyncio.run(
        cli.generate_video(model="seedance_2_0", prompt="test prompt")
    )
    assert result.cost_usd == 0.0


@pytest.mark.unit
def test_dry_run_video_url_is_empty() -> None:
    """Dry-run returns empty string for video_url (no real URL generated)."""
    cli = HiggsfieldCli(dry_run=True)
    result = asyncio.run(
        cli.generate_video(model="seedance_2_0", prompt="test")
    )
    assert result.video_url == ""


@pytest.mark.unit
def test_dry_run_local_path_is_placeholder() -> None:
    cli = HiggsfieldCli(dry_run=True)
    result = asyncio.run(
        cli.generate_video(model="seedance_2_0", prompt="test")
    )
    assert isinstance(result.local_path, Path)
    assert "dryrun" in result.local_path.name or "placeholder" in result.local_path.name


@pytest.mark.unit
def test_dry_run_makes_no_subprocess_call(monkeypatch: pytest.MonkeyPatch) -> None:
    """The critical constraint: dry_run MUST NOT call asyncio.create_subprocess_exec."""
    calls: list[object] = []

    async def fake_subprocess(*args: object, **kwargs: object) -> object:
        calls.append(args)
        raise AssertionError("subprocess was called in dry_run mode")

    import auto_affi.adapters.higgsfield_cli as _mod
    monkeypatch.setattr(_mod.asyncio, "create_subprocess_exec", fake_subprocess)

    cli = HiggsfieldCli(dry_run=True)
    result = asyncio.run(
        cli.generate_video(
            model="seedance_2_0",
            prompt="no subprocess please",
            aspect_ratio="9:16",
            duration=5,
        )
    )
    assert len(calls) == 0, f"subprocess was called {len(calls)} time(s)"
    assert isinstance(result, HiggsfieldVideo)


@pytest.mark.unit
def test_dry_run_account_credits_returns_zero() -> None:
    cli = HiggsfieldCli(dry_run=True)
    credits = asyncio.run(cli.account_credits())
    assert credits == 0.0


@pytest.mark.unit
def test_dry_run_does_not_import_shutil_which(monkeypatch: pytest.MonkeyPatch) -> None:
    """dry_run=True must not check PATH for the higgsfield binary."""
    checked: list[str] = []

    import shutil as _shutil

    original_which = _shutil.which

    def spy_which(name: str) -> str | None:
        checked.append(name)
        return original_which(name)

    monkeypatch.setattr("shutil.which", spy_which)

    # Importing the module may call which once during module-level code — that
    # is acceptable. We only care that HiggsfieldCli.__init__(dry_run=True)
    # does NOT call which("higgsfield").
    checked.clear()
    _ = HiggsfieldCli(dry_run=True)
    assert "higgsfield" not in checked, (
        f"dry_run=True should not check for higgsfield binary, but checked: {checked}"
    )


# ---------------------------------------------------------------------------
# dry_run=False with mocked subprocess (preserves live path shape)
# ---------------------------------------------------------------------------


def _fake_proc(stdout: str, returncode: int = 0) -> MagicMock:
    proc = MagicMock()
    proc.returncode = returncode
    proc.communicate = AsyncMock(return_value=(stdout.encode(), b""))
    return proc


def _approved_run(run_dir: Path) -> None:
    """Clear every PGA stage so a live generate_video() call passes the gate."""
    from auto_affi.pipeline.prompt_audit import STAGES, record_bypass

    for stage in STAGES:
        record_bypass(run_dir, stage, reason="test fixture: gate pre-cleared")


@pytest.mark.unit
def test_live_mode_raises_when_binary_missing() -> None:
    import auto_affi.adapters.higgsfield_cli as _mod
    with patch.object(_mod.shutil, "which", return_value=None), pytest.raises(HiggsfieldCliError, match="not found"):
        HiggsfieldCli(dry_run=False)


@pytest.mark.unit
def test_live_mode_parses_url_from_stdout(tmp_path: Path) -> None:
    stdout = (
        "Submitting job...\n"
        "Job queued: abc-123\n"
        "Polling...\n"
        "https://cdn.example.com/result.mp4\n"
    )
    captured: list[list[str]] = []

    async def fake_create(prog: str, *args: str, **kw: object) -> MagicMock:
        captured.append([prog, *args])
        return _fake_proc(stdout)

    import auto_affi.adapters.higgsfield_cli as _mod
    with (
        patch.object(_mod.shutil, "which", return_value="/usr/bin/hf"),
        patch.object(_mod.asyncio, "create_subprocess_exec", side_effect=fake_create),
        patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=99999.0)),
    ):
        _approved_run(tmp_path)
        cli = HiggsfieldCli(dry_run=False)
        result = asyncio.run(
            cli.generate_video(
                model="seedance_2_0",
                prompt="orbit",
                aspect_ratio="9:16",
                duration=5,
                mode="fast",
                run_dir=tmp_path,
                budget=BudgetCircuitBreaker(),
            )
        )

    assert result.video_url == "https://cdn.example.com/result.mp4"
    assert len(captured) == 1
    argv = captured[0]
    assert "--prompt" in argv and "orbit" in argv
    assert "--mode" in argv and "fast" in argv


@pytest.mark.unit
def test_live_mode_raises_on_nonzero_exit(tmp_path: Path) -> None:
    async def fake_create(prog: str, *args: str, **kw: object) -> MagicMock:
        return _fake_proc("ERROR: insufficient credits\n", returncode=1)

    import auto_affi.adapters.higgsfield_cli as _mod
    with (
        patch.object(_mod.shutil, "which", return_value="/x/hf"),
        patch.object(_mod.asyncio, "create_subprocess_exec", side_effect=fake_create),
        patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=99999.0)),
    ):
        _approved_run(tmp_path)
        cli = HiggsfieldCli(dry_run=False)
        with pytest.raises(HiggsfieldCliError, match="exit 1"):
            asyncio.run(
                cli.generate_video(
                    model="seedance_2_0", prompt="x", run_dir=tmp_path, budget=BudgetCircuitBreaker()
                )
            )


@pytest.mark.unit
def test_live_mode_raises_when_no_url_in_output(tmp_path: Path) -> None:
    async def fake_create(prog: str, *args: str, **kw: object) -> MagicMock:
        return _fake_proc("Job done.\n")

    import auto_affi.adapters.higgsfield_cli as _mod
    with (
        patch.object(_mod.shutil, "which", return_value="/x/hf"),
        patch.object(_mod.asyncio, "create_subprocess_exec", side_effect=fake_create),
        patch.object(HiggsfieldCli, "account_credits", AsyncMock(return_value=99999.0)),
    ):
        _approved_run(tmp_path)
        cli = HiggsfieldCli(dry_run=False)
        with pytest.raises(HiggsfieldCliError, match="could not parse video URL"):
            asyncio.run(
                cli.generate_video(
                    model="seedance_2_0", prompt="x", run_dir=tmp_path, budget=BudgetCircuitBreaker()
                )
            )


@pytest.mark.unit
def test_live_mode_requires_run_dir_fail_closed() -> None:
    """Fail-closed: a live (paid) call without run_dir is blocked, never silently
    ungated (Audit Lead GAP-2)."""
    import auto_affi.adapters.higgsfield_cli as _mod
    from auto_affi.pipeline.prompt_audit import GenerationBlocked
    with patch.object(_mod.shutil, "which", return_value="/x/hf"):
        cli = HiggsfieldCli(dry_run=False)
        with pytest.raises(GenerationBlocked, match="requires run_dir"):
            asyncio.run(cli.generate_video(model="seedance_2_0", prompt="x"))
