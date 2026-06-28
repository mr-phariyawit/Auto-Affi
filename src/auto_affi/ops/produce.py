"""Gated producer — drives real image/video generation THROUGH the PGA gate.

Closes Audit Lead GAP-B and ADR-009: the spend-safety guard is no longer dead code,
and the producer depends on the provider-agnostic `GenProvider` Protocol (Gemini today),
not a concrete adapter. For each PGA stage it calls the provider's generate_image
(cast/objects/storyboard/contact stills) or generate_video, passing run_dir + the stage
`ReferenceManifest` (so the prompt-hash binding is exercised) + a shared
`BudgetCircuitBreaker`. The provider enforces the gate at the shared chokepoint: a stage
that is not human-approved (or explicitly bypassed) raises before any spend.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from auto_affi.adapters.gen_provider import GenAsset, GenProvider
from auto_affi.pipeline.prompt_audit import STAGES, ReferenceManifest
from auto_affi.workflows.budget import BudgetCircuitBreaker


class StageKind(StrEnum):
    """Whether a PGA stage produces a still image or a video clip."""

    IMAGE = "image"
    VIDEO = "video"


@dataclass(frozen=True)
class StagePlan:
    """One stage's generation request. ``manifest`` is audited + hash-bound at the gate."""

    stage: str
    kind: StageKind
    manifest: ReferenceManifest
    model: str | None = None
    reference_images: tuple[Path | str, ...] = ()
    duration: int = 8

    def __post_init__(self) -> None:
        if self.stage not in STAGES:
            raise ValueError(f"unknown stage: {self.stage!r}")
        if self.kind is StageKind.VIDEO and self.stage != "video":
            raise ValueError("VIDEO kind is only valid for the 'video' stage")
        if self.kind is StageKind.IMAGE and self.stage == "video":
            raise ValueError("the 'video' stage must use VIDEO kind")


@dataclass
class GatedProducer:
    """Runs each :class:`StagePlan` through a gated :class:`GenProvider`.

    Generation, gating and spend all funnel through the provider's shared chokepoint;
    this producer never touches ``approvals.json`` or records cost itself — it only
    requests generation, and the gate decides whether it may proceed.
    """

    provider: GenProvider
    run_dir: Path
    budget: BudgetCircuitBreaker = field(default_factory=BudgetCircuitBreaker)

    async def produce_stage(self, plan: StagePlan) -> GenAsset:
        if plan.kind is StageKind.IMAGE:
            return await self.provider.generate_image(
                stage=plan.stage,
                prompt=plan.manifest.prompt,
                run_dir=self.run_dir,
                manifest=plan.manifest,
                budget=self.budget,
                reference_images=plan.reference_images,
                model=plan.model,
            )
        return await self.provider.generate_video(
            stage=plan.stage,
            prompt=plan.manifest.prompt,
            run_dir=self.run_dir,
            manifest=plan.manifest,
            budget=self.budget,
            reference_images=plan.reference_images,
            model=plan.model,
            duration=plan.duration,
        )

    async def produce_all(self, plans: Iterable[StagePlan]) -> list[GenAsset]:
        """Produce every stage in order. Stops at the first gate block (raises)."""
        results: list[GenAsset] = []
        for plan in plans:
            results.append(await self.produce_stage(plan))
        return results
