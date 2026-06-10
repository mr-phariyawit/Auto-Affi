"""Higgsfield CLI subprocess wrapper — dry-run by default (offline Phase 1).

In ``dry_run=True`` mode (the default), no subprocess to the ``higgsfield``
CLI is made and the binary is NOT required on PATH. A deterministic stub
result is returned with cost 0.0 and a local placeholder path.

The real subprocess path (``dry_run=False``) is preserved for Phase-2
when Higgsfield credentials are available. It routes through the locally-
installed ``higgsfield`` CLI (``npm install -g @higgsfield/cli``).

Why the CLI path over the REST adapter:
- One credit pool covers seedance_2_0 / cinematic_studio_3_0 / veo3_1
  / kling3_0 / wan2_x / minimax_hailuo / soul_cast / grok_video and
  the image gens (nano_banana_2, product-photoshoot).
- OAuth-only — no API key in ``.env``.
- The CLI auto-uploads local image paths passed via ``--image`` /
  ``--start-image`` / ``--end-image``.
"""

from __future__ import annotations

import asyncio
import dataclasses
import shutil
from pathlib import Path
from typing import Iterable


HIGGSFIELD_BIN = "higgsfield"

# Placeholder path returned by dry-run (guaranteed non-existent, clearly fake)
_DRY_RUN_PLACEHOLDER = Path("/tmp/higgsfield_dryrun_placeholder.mp4")


class HiggsfieldCliError(RuntimeError):
    """Raised on non-zero exit, missing CLI, or malformed output."""


@dataclasses.dataclass(frozen=True)
class HiggsfieldVideo:
    """Returned by ``generate_video`` — the public URL of the rendered
    MP4 plus the raw stdout for audit.

    In dry-run mode, ``video_url`` is an empty string and ``local_path``
    points to the placeholder. In live mode, ``video_url`` is a CloudFront
    URL.
    """

    video_url: str
    raw_stdout: str
    cost_usd: float = 0.0
    local_path: Path = _DRY_RUN_PLACEHOLDER


class HiggsfieldCli:
    """Thin async wrapper around the Higgsfield CLI.

    Args:
        dry_run: When True (default), returns a deterministic stub without
            touching the CLI binary or the network. Set to False only when
            Higgsfield credentials are available (Phase 2+).
        binary:  CLI binary name; only consulted when ``dry_run=False``.
    """

    def __init__(
        self,
        *,
        dry_run: bool = True,
        binary: str = HIGGSFIELD_BIN,
    ) -> None:
        self._dry_run = dry_run
        self._bin = binary

        if not dry_run:
            if shutil.which(binary) is None:
                raise HiggsfieldCliError(
                    f"`{binary}` not found on PATH. Install with "
                    f"`npm install -g @higgsfield/cli` and run "
                    f"`{binary} auth login`."
                )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _run(self, args: list[str]) -> tuple[str, str]:
        """Invoke the live CLI. Only called when dry_run=False."""
        proc = await asyncio.create_subprocess_exec(
            self._bin,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out_b, err_b = await proc.communicate()
        out = out_b.decode("utf-8", errors="replace")
        err = err_b.decode("utf-8", errors="replace")
        if proc.returncode != 0:
            raise HiggsfieldCliError(
                f"higgsfield {' '.join(args)} -> exit {proc.returncode}\n"
                f"STDOUT: {out[:500]}\nSTDERR: {err[:500]}"
            )
        return out, err

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

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

        In dry-run mode returns a deterministic stub immediately (no network,
        no subprocess, cost 0.0).

        Args:
            model:        Higgsfield job_set_type, e.g. ``seedance_2_0``.
            prompt:       Text prompt (required).
            aspect_ratio: ``9:16`` / ``16:9`` / ``1:1`` etc.
            duration:     Integer seconds (typically 5-10).
            mode:         Model-specific tier (``std`` / ``fast`` / ``pro``).
            resolution:   ``480p`` / ``720p`` / ``1080p``.
            images:       Dict of flag->path/uuid for reference images.
            wait_timeout: Passed to ``--wait-timeout`` (live mode only).
            wait_interval: Passed to ``--wait-interval`` (live mode only).
            extra_args:   Pass-through flags (live mode only).

        Returns:
            :class:`HiggsfieldVideo` with ``video_url`` set to the
            CloudFront URL (live) or empty string (dry-run).
        """
        if self._dry_run:
            stub_stdout = (
                f"[DRY-RUN] model={model} prompt={prompt[:40]!r} "
                f"aspect_ratio={aspect_ratio} duration={duration}s "
                f"mode={mode} resolution={resolution}"
            )
            return HiggsfieldVideo(
                video_url="",
                raw_stdout=stub_stdout,
                cost_usd=0.0,
                local_path=_DRY_RUN_PLACEHOLDER,
            )

        # --- live path (dry_run=False) ---
        args: list[str] = [
            "generate",
            "create",
            model,
            "--prompt",
            prompt,
            "--aspect_ratio",
            aspect_ratio,
            "--duration",
            str(duration),
            "--resolution",
            resolution,
            "--wait",
            "--wait-timeout",
            wait_timeout,
            "--wait-interval",
            wait_interval,
        ]
        if mode:
            args += ["--mode", mode]
        if images:
            for flag, value in images.items():
                args += [f"--{flag}", str(value)]
        args += list(extra_args)

        out, err = await self._run(args)

        video_url = ""
        for line in reversed(out.strip().splitlines()):
            line = line.strip()
            if line.startswith("http://") or line.startswith("https://"):
                video_url = line
                break
        if not video_url:
            raise HiggsfieldCliError(
                f"could not parse video URL from CLI output (exit 0).\n"
                f"STDOUT: {out[-400:]!r}\nSTDERR: {err[-400:]!r}"
            )
        return HiggsfieldVideo(
            video_url=video_url,
            raw_stdout=out,
            cost_usd=0.0,
            local_path=_DRY_RUN_PLACEHOLDER,
        )

    async def account_credits(self) -> float:
        """Best-effort parse of `higgsfield account status` -> credits.

        Dry-run: returns 0.0 (no CLI call).
        """
        if self._dry_run:
            return 0.0

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
