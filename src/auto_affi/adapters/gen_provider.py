"""Provider-agnostic generation interface + the shared spend gate.

ADR-009 retires Higgsfield in favour of Gemini. The PGA gate + verify-before-spend
chokepoint must NOT be duplicated or weakened per provider, so it lives here once
(`enforce_spend_gate`) and every provider routes through it. The producer depends on
the `GenProvider` Protocol, not on any concrete adapter.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

from auto_affi.pipeline.prompt_audit import (
    GenerationBlocked,
    ReferenceManifest,
    assert_may_generate,
)
from auto_affi.workflows.budget import BudgetCircuitBreaker, BudgetDecision


class ProviderSpendError(RuntimeError):
    """Raised when a live generation cannot proceed for spend reasons."""


@dataclass(frozen=True)
class GenAsset:
    """The result of a generation — image or video."""

    kind: str  # "image" | "video"
    url: str = ""  # remote URL (live) or "" (dry-run)
    local_path: Path | None = None
    cost_usd: float = 0.0
    cost_estimated: bool = False
    raw: str = ""  # provider stdout/op id, for audit


async def enforce_spend_gate(
    *,
    dry_run: bool,
    stage: str,
    run_dir: Path | None,
    manifest: ReferenceManifest | None,
    node: str,
    estimated_cost_usd: float,
    budget: BudgetCircuitBreaker | None,
) -> None:
    """The single chokepoint before ANY generation (any provider).

    1. Generation Lock (fail-closed): live calls require run_dir AND manifest; the
       PGA gate + hash binding is enforced via assert_may_generate.
    2. Verify-before-spend: for live calls the budget circuit-breaker is MANDATORY
       (daily + per-node USD caps). Gemini is billed per-use to a GCP project and
       exposes no pre-call balance API, so the budget breaker is the hard spend cap
       and is never skipped. (Higgsfield, the only provider with a balance API, was
       retired in ADR-009; the balance-check path was removed with it.)
    Dry-run performs only the gate (no budget check, no spend).
    """
    if not dry_run:
        if run_dir is None:
            raise GenerationBlocked(
                stage, "live generation requires run_dir — the PGA gate cannot be skipped"
            )
        if manifest is None:
            raise GenerationBlocked(
                stage, "live generation requires a manifest (hash binding cannot be skipped)"
            )
    if run_dir is not None:
        assert_may_generate(stage, run_dir, manifest=manifest)

    if dry_run:
        return

    # Budget circuit-breaker is MANDATORY on the live path — the hard spend cap.
    if budget is None:
        raise ProviderSpendError(
            f"live generation requires a BudgetCircuitBreaker for {node} "
            f"(verify-before-spend cannot be skipped)"
        )
    if budget.check_budget(node, estimated_cost_usd) is BudgetDecision.DENY:
        raise ProviderSpendError(
            f"budget breaker DENY for {node}: estimated ${estimated_cost_usd:.2f} "
            f"would exceed a cap"
        )


@runtime_checkable
class GenProvider(Protocol):
    """What the GatedProducer needs from any generation backend."""

    async def generate_image(
        self,
        *,
        stage: str,
        prompt: str,
        run_dir: Path | None = None,
        manifest: ReferenceManifest | None = None,
        budget: BudgetCircuitBreaker | None = None,
        reference_images: Iterable[Path | str] = (),
        model: str | None = None,
        aspect_ratio: str = "9:16",
        estimated_cost_usd: float | None = None,
    ) -> GenAsset: ...

    async def generate_video(
        self,
        *,
        stage: str,
        prompt: str,
        run_dir: Path | None = None,
        manifest: ReferenceManifest | None = None,
        budget: BudgetCircuitBreaker | None = None,
        reference_images: Iterable[Path | str] = (),
        model: str | None = None,
        duration: int = 8,
        aspect_ratio: str = "9:16",
        estimated_cost_usd: float | None = None,
    ) -> GenAsset: ...
