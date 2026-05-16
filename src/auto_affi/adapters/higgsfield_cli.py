"""Higgsfield CLI subprocess wrapper.

Routes generator calls through the locally-installed `higgsfield` CLI
(`npm install -g @higgsfield/cli`) instead of building a REST client.
The CLI handles auth (OAuth, no API key), credit accounting, async
job polling (`--wait`), and result-URL emission, so this wrapper is
deliberately thin (~80 LOC).

Why the CLI path over the REST adapter:
- One credit pool covers seedance_2_0 / cinematic_studio_3_0 / veo3_1
  / kling3_0 / wan2_x / minimax_hailuo / soul_cast / grok_video and
  the image gens (nano_banana_2, product-photoshoot).
- OAuth-only — no API key in `.env`.
- The CLI auto-uploads local image paths passed via `--image` /
  `--start-image` / `--end-image`, so we don't have to pre-stage GCS
  URLs the way we do for Phaya Seedance 1.5 Pro.

Usage:

    from auto_affi.adapters.higgsfield_cli import HiggsfieldCli, HiggsfieldCliError

    cli = HiggsfieldCli()
    job = await cli.generate_video(
        model="seedance_2_0",
        prompt="Slow 30-degree orbit around the maono PD300X mic ...",
        aspect_ratio="9:16",
        duration=5,
        mode="fast",
        resolution="720p",
        images={"image": Path("data/.../pd300x-hero-clean.jpg")},
    )
    # job.video_url is a public CloudFront URL we can curl down.

The wrapper does NOT impose a fixed model list — pass any string the
CLI accepts. See `higgsfield model list --video` for current options.
"""

from __future__ import annotations

import asyncio
import dataclasses
import json
import shutil
import subprocess
from pathlib import Path
from typing import Iterable


HIGGSFIELD_BIN = "higgsfield"


class HiggsfieldCliError(RuntimeError):
    """Raised on non-zero exit, missing CLI, or malformed output."""


@dataclasses.dataclass(frozen=True)
class HiggsfieldVideo:
    """Returned by ``generate_video`` — the public URL of the rendered
    MP4 plus the raw stdout for audit."""

    video_url: str
    raw_stdout: str


class HiggsfieldCli:
    """Thin async subprocess wrapper around the Higgsfield CLI.

    All public methods are coroutines so they can be awaited inside the
    existing orchestrator without blocking the event loop. Internally
    they shell out via ``asyncio.create_subprocess_exec``.
    """

    def __init__(self, *, binary: str = HIGGSFIELD_BIN) -> None:
        if shutil.which(binary) is None:
            raise HiggsfieldCliError(
                f"`{binary}` not found on PATH. Install with "
                f"`npm install -g @higgsfield/cli` and run "
                f"`{binary} auth login`."
            )
        self._bin = binary

    async def _run(self, args: list[str]) -> tuple[str, str]:
        """Invoke the CLI with the given args. Returns (stdout, stderr).
        Raises HiggsfieldCliError on non-zero exit."""
        proc = await asyncio.create_subprocess_exec(
            self._bin, *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out_b, err_b = await proc.communicate()
        out = out_b.decode("utf-8", errors="replace")
        err = err_b.decode("utf-8", errors="replace")
        if proc.returncode != 0:
            raise HiggsfieldCliError(
                f"higgsfield {' '.join(args)} → exit {proc.returncode}\n"
                f"STDOUT: {out[:500]}\nSTDERR: {err[:500]}"
            )
        return out, err

    async def generate_video(
        self,
        *,
        model: str,
        prompt: str,
        aspect_ratio: str = "9:16",
        duration: int = 5,
        mode: str | None = None,
        resolution: str = "720p",
        images: dict[str, Path | str] | None = None,
        wait_timeout: str = "10m",
        wait_interval: str = "4s",
        extra_args: Iterable[str] = (),
    ) -> HiggsfieldVideo:
        """Submit a video generation job and wait for completion.

        Args:
            model:        Higgsfield job_set_type, e.g. ``seedance_2_0``,
                ``cinematic_studio_3_0``, ``veo3_1``, ``kling3_0``.
            prompt:       Text prompt (required).
            aspect_ratio: ``9:16`` / ``16:9`` / ``1:1`` etc.
            duration:     Integer seconds (typically 5-10).
            mode:         Model-specific tier — for Seedance ``std`` or
                ``fast``; for Kling ``pro`` or ``std``. Some models
                ignore this field.
            resolution:   ``480p`` / ``720p`` / ``1080p``.
            images:       Dict of flag→path/uuid for reference images.
                Common keys: ``image`` (single ref), ``start-image``
                + ``end-image`` (two-keyframe). Local paths are
                auto-uploaded by the CLI; UUIDs are passed through.
            wait_timeout: Passed to ``--wait-timeout``.
            wait_interval: Passed to ``--wait-interval``.
            extra_args:   Pass-through flags the wrapper doesn't model
                explicitly (e.g. ``--genre noir`` for Seedance).

        Returns:
            HiggsfieldVideo with ``video_url`` set to the CloudFront URL
            the CLI emitted on its final stdout line.
        """
        args = ["generate", "create", model,
                "--prompt", prompt,
                "--aspect_ratio", aspect_ratio,
                "--duration", str(duration),
                "--resolution", resolution,
                "--wait", "--wait-timeout", wait_timeout,
                "--wait-interval", wait_interval]
        if mode:
            args += ["--mode", mode]
        if images:
            for flag, value in images.items():
                args += [f"--{flag}", str(value)]
        args += list(extra_args)

        out, err = await self._run(args)

        # The CLI prints progress + a final URL line. Take the last
        # non-empty line that looks like an http(s) URL.
        video_url = ""
        for line in reversed(out.strip().splitlines()):
            line = line.strip()
            if line.startswith("http://") or line.startswith("https://"):
                video_url = line
                break
        if not video_url:
            # CLI exited 0 but emitted no URL — the job may have been
            # rejected upstream (moderation, prompt-too-long, etc.) with
            # the actual reason on stderr. Surface both streams.
            raise HiggsfieldCliError(
                f"could not parse video URL from CLI output (exit 0).\n"
                f"STDOUT: {out[-400:]!r}\nSTDERR: {err[-400:]!r}"
            )
        return HiggsfieldVideo(video_url=video_url, raw_stdout=out)

    async def download(self, url: str, dest: Path) -> Path:
        """Curl the URL to disk. The CLI doesn't ship a built-in
        downloader, so we use httpx for consistency with the other
        adapters."""
        import httpx
        dest.parent.mkdir(parents=True, exist_ok=True)
        async with httpx.AsyncClient(timeout=httpx.Timeout(180.0)) as c:
            r = await c.get(url)
        if r.status_code >= 400:
            raise HiggsfieldCliError(
                f"download {url} → HTTP {r.status_code}"
            )
        dest.write_bytes(r.content)
        return dest

    async def account_credits(self) -> float:
        """Best-effort parse of `higgsfield account status` → credits.

        The CLI emits lines like:
            mr.phariyawit@gmail.com — ultra plan, 2982.5 credits
        We grep for `credits` and pull the float preceding it.
        """
        out, _ = await self._run(["account", "status"])
        for line in out.splitlines():
            line = line.strip().lower()
            if "credit" in line:
                tokens = line.replace(",", " ").split()
                for i, tok in enumerate(tokens):
                    if tok.startswith("credit"):
                        try:
                            return float(tokens[i - 1])
                        except (IndexError, ValueError):
                            continue
        raise HiggsfieldCliError(
            f"could not parse credit balance from `account status`:\n{out}"
        )
