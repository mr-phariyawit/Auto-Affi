"""Gated producer — drives real image/video generation THROUGH the PGA gate.

Closes Audit Lead GAP-B (reports/2026-06-27_crew-review-findings.md): the
spend-safety guard in :mod:`auto_affi.adapters.higgsfield_cli` was dead code —
``ops/produce_slice.py`` runs the offline ``dry_render`` and hardcodes every cost
to ``0.0``, so image-stage gating and verify-before-spend never executed in any
real run.

This producer calls :meth:`HiggsfieldCli.generate_image` (cast/objects/storyboard/
contact stills) and :meth:`HiggsfieldCli.generate_video` (video) for each PGA
stage, passing ``run_dir`` + the stage's :class:`ReferenceManifest` (so the
prompt-hash binding is exercised) + a shared :class:`BudgetCircuitBreaker`. The
adapter enforces the gate: a stage that is not human-approved (or explicitly
bypassed) raises ``GenerationBlocked`` before any spend.

``dry_run=True`` (the default ``HiggsfieldCli``) keeps this offline and free — the
gate still runs, but no credit/budget checks and zero cost. A ``dry_run=False``
producer performs verify-before-spend and records the real (estimated) cost.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from auto_affi.adapters.higgsfield_cli import (
    HiggsfieldCli,
    HiggsfieldImage,
    HiggsfieldVideo,
)
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
    model: str
    manifest: ReferenceManifest
    images: dict[str, Path | str] | None = None
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
    """Runs each :class:`StagePlan` through the gated Higgsfield adapter.

    Generation, gating and spend are all funnelled through the adapter chokepoint;
    this producer never touches ``approvals.json`` or records cost itself — it only
    requests generation, and the gate decides whether it may proceed.
    """

    cli: HiggsfieldCli
    run_dir: Path
    budget: BudgetCircuitBreaker

    async def produce_stage(self, plan: StagePlan) -> HiggsfieldImage | HiggsfieldVideo:
        if plan.kind is StageKind.IMAGE:
            return await self.cli.generate_image(
                model=plan.model,
                prompt=plan.manifest.prompt,
                stage=plan.stage,
                images=plan.images,
                run_dir=self.run_dir,
                manifest=plan.manifest,
                budget=self.budget,
            )
        return await self.cli.generate_video(
            model=plan.model,
            prompt=plan.manifest.prompt,
            duration=plan.duration,
            images=plan.images,
            run_dir=self.run_dir,
            manifest=plan.manifest,
            budget=self.budget,
            stage=plan.stage,
        )

    async def produce_all(
        self, plans: list[StagePlan]
    ) -> list[HiggsfieldImage | HiggsfieldVideo]:
        """Produce every stage in order. Stops at the first gate block (raises)."""
        results: list[HiggsfieldImage | HiggsfieldVideo] = []
        for plan in plans:
            results.append(await self.produce_stage(plan))
        return results
