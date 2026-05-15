"""Tests for the Higgsfield CLI subprocess wrapper. The CLI binary is
mocked end-to-end via asyncio.create_subprocess_exec patching, so the
tests run with no Higgsfield account / network / spend."""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock

import pytest

from auto_affi.adapters.higgsfield_cli import (
    HiggsfieldCli,
    HiggsfieldCliError,
    HiggsfieldVideo,
)


def _fake_subprocess(stdout: str, returncode: int = 0):
    """Build an AsyncMock that mimics asyncio.subprocess.Process.communicate()."""
    proc = MagicMock()
    proc.returncode = returncode
    proc.communicate = AsyncMock(return_value=(stdout.encode(), b""))
    return proc


def test_init_raises_when_cli_missing():
    with patch("auto_affi.adapters.higgsfield_cli.shutil.which", return_value=None):
        with pytest.raises(HiggsfieldCliError, match="not found"):
            HiggsfieldCli()


def test_generate_video_parses_url_from_last_line():
    stdout = (
        "Submitting job...\n"
        "Job queued: abc-def-123\n"
        "Polling...\n"
        "https://cdn.example.com/result.mp4\n"
    )
    captured_args: dict[str, list[str]] = {}

    async def fake_create(prog, *args, **kwargs):
        captured_args["argv"] = [prog, *args]
        return _fake_subprocess(stdout)

    with patch("auto_affi.adapters.higgsfield_cli.shutil.which", return_value="/usr/local/bin/higgsfield"), \
         patch("asyncio.create_subprocess_exec", side_effect=fake_create):
        cli = HiggsfieldCli()
        result = asyncio.run(cli.generate_video(
            model="seedance_2_0",
            prompt="cinematic product orbit",
            aspect_ratio="9:16",
            duration=5,
            mode="fast",
            resolution="720p",
            images={"image": Path("/tmp/x.jpg")},
        ))

    assert isinstance(result, HiggsfieldVideo)
    assert result.video_url == "https://cdn.example.com/result.mp4"
    argv = captured_args["argv"]
    assert argv[0] == "higgsfield"
    assert argv[1:4] == ["generate", "create", "seedance_2_0"]
    assert "--prompt" in argv and "cinematic product orbit" in argv
    assert "--aspect_ratio" in argv and "9:16" in argv
    assert "--duration" in argv and "5" in argv
    assert "--mode" in argv and "fast" in argv
    assert "--resolution" in argv and "720p" in argv
    assert "--wait" in argv
    assert "--image" in argv and "/tmp/x.jpg" in argv


def test_generate_video_supports_two_keyframe_flags():
    stdout = "https://cdn.example.com/two-kf.mp4\n"
    captured: dict[str, list[str]] = {}

    async def fake_create(prog, *args, **kwargs):
        captured["argv"] = [prog, *args]
        return _fake_subprocess(stdout)

    with patch("auto_affi.adapters.higgsfield_cli.shutil.which", return_value="/x/higgsfield"), \
         patch("asyncio.create_subprocess_exec", side_effect=fake_create):
        cli = HiggsfieldCli()
        result = asyncio.run(cli.generate_video(
            model="seedance_2_0",
            prompt="transition between s2 and s3",
            duration=5,
            images={
                "start-image": Path("/tmp/s2.jpg"),
                "end-image": Path("/tmp/s3.jpg"),
            },
        ))
    assert result.video_url.endswith("/two-kf.mp4")
    argv = captured["argv"]
    assert "--start-image" in argv and "/tmp/s2.jpg" in argv
    assert "--end-image" in argv and "/tmp/s3.jpg" in argv


def test_generate_video_raises_on_nonzero_exit():
    async def fake_create(prog, *args, **kwargs):
        return _fake_subprocess("ERROR: insufficient credits\n", returncode=1)

    with patch("auto_affi.adapters.higgsfield_cli.shutil.which", return_value="/x/higgsfield"), \
         patch("asyncio.create_subprocess_exec", side_effect=fake_create):
        cli = HiggsfieldCli()
        with pytest.raises(HiggsfieldCliError, match="exit 1"):
            asyncio.run(cli.generate_video(model="seedance_2_0", prompt="x"))


def test_generate_video_raises_when_no_url_in_output():
    async def fake_create(prog, *args, **kwargs):
        # CLI exited 0 but emitted no URL (weird edge case)
        return _fake_subprocess("Job queued.\nWaiting...\nDone.\n")

    with patch("auto_affi.adapters.higgsfield_cli.shutil.which", return_value="/x/higgsfield"), \
         patch("asyncio.create_subprocess_exec", side_effect=fake_create):
        cli = HiggsfieldCli()
        with pytest.raises(HiggsfieldCliError, match="could not parse video URL"):
            asyncio.run(cli.generate_video(model="seedance_2_0", prompt="x"))


def test_account_credits_parses_balance():
    stdout = "mr.x@example.com — ultra plan, 2982.5 credits\n"

    async def fake_create(prog, *args, **kwargs):
        return _fake_subprocess(stdout)

    with patch("auto_affi.adapters.higgsfield_cli.shutil.which", return_value="/x/higgsfield"), \
         patch("asyncio.create_subprocess_exec", side_effect=fake_create):
        cli = HiggsfieldCli()
        credits = asyncio.run(cli.account_credits())
    assert credits == pytest.approx(2982.5)


def test_schema_higgsfield_cli_requires_model_name():
    """AiShot validator: HIGGSFIELD_CLI must declare which underlying
    Higgsfield model to dispatch (seedance_2_0, cinematic_studio_3_0, ...)."""
    from auto_affi.schemas.ai_storyboard import (
        AiShot, AudioSource, Generator, NarrativeRole,
    )

    # Missing higgsfield_model → ValueError
    with pytest.raises(ValueError, match="higgsfield_model"):
        AiShot(
            shot_id="s0",
            narrative_role=NarrativeRole.OFFER,
            duration_s=5.0,
            generator=Generator.HIGGSFIELD_CLI,
            image_prompt="a" * 30,
            consistency_seed=1,
            audio_source=AudioSource.MUSIC_ONLY,
        )

    # With higgsfield_model → accepted
    shot = AiShot(
        shot_id="s0",
        narrative_role=NarrativeRole.OFFER,
        duration_s=5.0,
        generator=Generator.HIGGSFIELD_CLI,
        image_prompt="a" * 30,
        consistency_seed=1,
        audio_source=AudioSource.MUSIC_ONLY,
        higgsfield_model="seedance_2_0",
        higgsfield_mode="fast",
        higgsfield_resolution="720p",
    )
    assert shot.higgsfield_model == "seedance_2_0"
    assert shot.higgsfield_mode == "fast"
    assert shot.higgsfield_resolution == "720p"
