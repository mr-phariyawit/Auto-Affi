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
import re
import shutil
from collections.abc import Iterable
from pathlib import Path

from auto_affi.pipeline.prompt_audit import (
    GenerationBlocked,
    ReferenceManifest,
    assert_may_generate,
)
from auto_affi.workflows.budget import BudgetCircuitBreaker, BudgetDecision

HIGGSFIELD_BIN = "higgsfield"

# Placeholder path returned by dry-run (guaranteed non-existent, clearly fake)
_DRY_RUN_PLACEHOLDER = Path("/tmp/higgsfield_dryrun_placeholder.mp4")  # noqa: S108

# --- Cost model (ESTIMATES — Higgsfield credit pricing is not exposed by the CLI) ---
# Sourced from the Seedance reference (~20.5 credits/s) and the hula-hoop study
# (656 credits ≈ $3.28 ⇒ ~$0.005/credit). Treat as estimates; callers may override
# via estimated_credits / estimated_cost_usd. Used for verify-before-spend only.
_VIDEO_CREDITS_PER_SECOND: float = 20.5
# ~$0.03/still, matching SPEC Appendix C ("8 scenes x image = 0.25"); keeps a
# multi-still run under the $0.25 image_gen node cap.
_IMAGE_CREDITS_DEFAULT: float = 6.0
_USD_PER_CREDIT: float = 0.005
_CREDIT_SAFETY_MARGIN: float = 1.2


class HiggsfieldCliError(RuntimeError):
    """Raised on non-zero exit, missing CLI, or malformed output."""


# Numbers bound to the word "credit" on either side (grouped digits allowed).
_CREDIT_AFTER = re.compile(r"credits?\s*[:=]?\s*([\d][\d,]*(?:\.\d+)?)", re.IGNORECASE)
_CREDIT_BEFORE = re.compile(r"([\d][\d,]*(?:\.\d+)?)\s*credits?\b", re.IGNORECASE)
_BALANCE_HINTS = ("remaining", "available", "balance")


def _parse_credit_balance(out: str) -> float:
    """Fail-closed parse of `higgsfield account status` output -> balance.

    Only accepts a number directly adjacent to the word "credit"; never wraps to
    an unrelated token. Prefers a line that names remaining/available/balance;
    otherwise returns the CONSERVATIVE (minimum) candidate so the balance is never
    overstated. Raises when nothing can be confidently parsed (never guesses high).
    """
    preferred: list[float] = []
    candidates: list[float] = []
    for raw in out.splitlines():
        line = raw.strip()
        if "credit" not in line.lower():
            continue
        nums = [
            float(m.group(1).replace(",", ""))
            for pattern in (_CREDIT_AFTER, _CREDIT_BEFORE)
            for m in pattern.finditer(line)
        ]
        if not nums:
            continue
        candidates.extend(nums)
        if any(hint in line.lower() for hint in _BALANCE_HINTS):
            preferred.extend(nums)
    pool = preferred or candidates
    if not pool:
        raise HiggsfieldCliError(
            f"could not confidently parse a credit balance (fail-closed):\n{out}"
        )
    return min(pool)


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
    cost_estimated: bool = False


@dataclasses.dataclass(frozen=True)
class HiggsfieldImage:
    """Returned by ``generate_image`` — the public URL of the rendered still.

    Dry-run: ``image_url`` empty, ``local_path`` the placeholder, cost 0.0.
    Live: ``image_url`` is the CDN URL, ``cost_usd`` is the ESTIMATED spend
    (``cost_estimated=True``) since the CLI does not report per-job cost.
    """

    image_url: str
    raw_stdout: str
    cost_usd: float = 0.0
    local_path: Path = _DRY_RUN_PLACEHOLDER
    cost_estimated: bool = False


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

        if not dry_run and shutil.which(binary) is None:
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

    async def _pre_spend_guard(
        self,
        *,
        node: str,
        stage: str,
        run_dir: Path | None,
        manifest: ReferenceManifest | None,
        estimated_credits: float,
        estimated_cost_usd: float,
        budget: BudgetCircuitBreaker | None,
        credit_margin: float,
    ) -> None:
        """Single chokepoint before ANY generation (video or image).

        1. Generation Lock (fail-closed): live calls require run_dir; the PGA gate
           + hash binding is enforced via assert_may_generate.
        2. Verify-before-spend (SPEC §10.5 gate 13): for live calls, assert the
           provider credit balance covers the job, and consult the budget breaker.
        Dry-run performs only the gate (no balance/budget checks, no spend).
        """
        if not self._dry_run and run_dir is None:
            raise GenerationBlocked(
                stage, "live generation requires run_dir — the PGA gate cannot be skipped"
            )
        if run_dir is not None:
            assert_may_generate(stage, run_dir, manifest=manifest)

        if self._dry_run:
            return

        # verify-before-spend: provider credit balance must cover the job.
        balance = await self.account_credits()
        required = estimated_credits * credit_margin
        if balance < required:
            raise HiggsfieldCliError(
                f"insufficient Higgsfield credits for {node}: balance {balance:.1f} < "
                f"required {required:.1f} ({estimated_credits:.1f} x {credit_margin} margin)"
            )

        # budget circuit breaker is MANDATORY on the live path (Audit Lead GAP-C) —
        # a cap that defaults off is not a cap.
        if budget is None:
            raise HiggsfieldCliError(
                f"live generation requires a BudgetCircuitBreaker for {node} "
                f"(verify-before-spend cannot be skipped)"
            )
        decision = budget.check_budget(node, estimated_cost_usd)
        if decision is BudgetDecision.DENY:
            raise HiggsfieldCliError(
                f"budget breaker DENY for {node}: estimated ${estimated_cost_usd:.2f} "
                f"would exceed a cap"
            )

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
        run_dir: Path | None = None,
        stage: str = "video",
        manifest: ReferenceManifest | None = None,
        budget: BudgetCircuitBreaker | None = None,
        estimated_credits: float | None = None,
        estimated_cost_usd: float | None = None,
        credit_margin: float = _CREDIT_SAFETY_MARGIN,
    ) -> HiggsfieldVideo:
        """Submit a video generation job and wait for completion.

        In dry-run mode returns a deterministic stub immediately (no network,
        no subprocess, cost 0.0).

        Pre-Generation Audit gate (SPEC §10.5 g10-12): when ``run_dir`` is
        provided, the Pre-Generation Audit + approval gate is enforced for
        ``stage`` BEFORE anything is generated — no approval, no generation.
        The live producer path always passes ``run_dir``; legacy dry-run callers
        that omit it are unaffected.

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
        est_credits = (
            estimated_credits
            if estimated_credits is not None
            else _VIDEO_CREDITS_PER_SECOND * duration
        )
        est_usd = estimated_cost_usd if estimated_cost_usd is not None else est_credits * _USD_PER_CREDIT
        await self._pre_spend_guard(
            node="video_gen",
            stage=stage,
            run_dir=run_dir,
            manifest=manifest,
            estimated_credits=est_credits,
            estimated_cost_usd=est_usd,
            budget=budget,
            credit_margin=credit_margin,
        )

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
        # The job ran (exit 0) → credits were spent. Record BEFORE parsing the URL
        # so a parse failure cannot make real spend invisible (Audit Lead GAP-E).
        if budget is not None:
            budget.record_spend("video_gen", est_usd)

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
            cost_usd=est_usd,
            local_path=_DRY_RUN_PLACEHOLDER,
            cost_estimated=True,
        )

    async def generate_image(
        self,
        *,
        model: str,
        prompt: str,
        stage: str,
        aspect_ratio: str = "9:16",
        images: dict[str, Path | str] | None = None,
        run_dir: Path | None = None,
        manifest: ReferenceManifest | None = None,
        budget: BudgetCircuitBreaker | None = None,
        estimated_credits: float | None = None,
        estimated_cost_usd: float | None = None,
        credit_margin: float = _CREDIT_SAFETY_MARGIN,
        extra_args: Iterable[str] = (),
    ) -> HiggsfieldImage:
        """Submit an image generation job (cast/objects/storyboard/contact stills).

        Routed through the SAME PGA gate + verify-before-spend chokepoint as
        ``generate_video`` (SPEC §10.5 gate 10 requires EVERY image to pass). ``stage``
        MUST be the image stage being generated (e.g. ``cast_sheet``). Fail-closed:
        a live call requires ``run_dir``.
        """
        est_credits = estimated_credits if estimated_credits is not None else _IMAGE_CREDITS_DEFAULT
        est_usd = estimated_cost_usd if estimated_cost_usd is not None else est_credits * _USD_PER_CREDIT
        await self._pre_spend_guard(
            node="image_gen",
            stage=stage,
            run_dir=run_dir,
            manifest=manifest,
            estimated_credits=est_credits,
            estimated_cost_usd=est_usd,
            budget=budget,
            credit_margin=credit_margin,
        )

        if self._dry_run:
            stub_stdout = f"[DRY-RUN] image model={model} stage={stage} prompt={prompt[:40]!r}"
            return HiggsfieldImage(
                image_url="",
                raw_stdout=stub_stdout,
                cost_usd=0.0,
                local_path=_DRY_RUN_PLACEHOLDER,
            )

        # --- live path (dry_run=False) ---
        args: list[str] = [
            "generate",
            "image",
            model,
            "--prompt",
            prompt,
            "--aspect_ratio",
            aspect_ratio,
            "--wait",
        ]
        if images:
            for flag, value in images.items():
                args += [f"--{flag}", str(value)]
        args += list(extra_args)

        out, err = await self._run(args)
        # Record spend before URL parse (Audit Lead GAP-E).
        if budget is not None:
            budget.record_spend("image_gen", est_usd)

        image_url = ""
        for line in reversed(out.strip().splitlines()):
            line = line.strip()
            if line.startswith("http://") or line.startswith("https://"):
                image_url = line
                break
        if not image_url:
            raise HiggsfieldCliError(
                f"could not parse image URL from CLI output (exit 0).\n"
                f"STDOUT: {out[-400:]!r}\nSTDERR: {err[-400:]!r}"
            )
        return HiggsfieldImage(
            image_url=image_url,
            raw_stdout=out,
            cost_usd=est_usd,
            local_path=_DRY_RUN_PLACEHOLDER,
            cost_estimated=True,
        )

    async def account_credits(self) -> float:
        """Parse `higgsfield account status` -> available credit balance.

        Dry-run: returns 0.0 (no CLI call).

        FAIL-CLOSED (Audit Lead GAP-A): the previous parser did ``tokens[i-1]``
        which wrapped to the last token when a line started with "credit",
        reading a fabricated/overstated balance. This implementation:
        - only accepts a number directly bound to the word "credit" (either side),
        - handles grouped digits (``1,234``),
        - biases to the CONSERVATIVE (minimum) candidate so balance is never
          overstated, and prefers a line naming remaining/available/balance,
        - raises when nothing can be confidently parsed (never guesses high).
        The real CLI output format is still unverified — capture it and add a
        format test before trusting a live balance.
        """
        if self._dry_run:
            return 0.0

        out, _ = await self._run(["account", "status"])
        return _parse_credit_balance(out)
