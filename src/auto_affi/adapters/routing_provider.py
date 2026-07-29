"""Provider routing — stills on Nano Banana Pro, i2v on Kling (the model lock).

"Switch to Kling" (2026-07-24, verified 55-86% cheaper at equal-or-better quality): video
generation goes to Kling via kie.ai, still images stay on Nano Banana Pro (Gemini).

**Model-lock compliance gate** (wiki/03-model-locks-routing.md): a locked model must NOT
silently fall back — "ห้าม fallback เอง ถ้า model หลักใช้ไม่ได้ให้หยุดและรายงาน". So the DEFAULT wiring has
NO auto-fallback: a genuine Kling failure (:class:`KlingGenerationError`) propagates and the
run halts + reports. :class:`RoutedGenProvider` still SUPPORTS a ``video_fallback`` (used only
on a real generation failure, never on a deliberate spend/gate DENY) for callers who
explicitly opt in to automatic Kling->Veo recovery for unattended runs — but the factory
leaves it off unless asked. To run the legacy Veo-only path deliberately, set
``AUTO_AFFI_VIDEO_MODEL=veo``.

Everything stays behind the provider-agnostic :class:`GenProvider` Protocol, so the
:class:`GatedProducer` is unchanged — it just receives a :class:`RoutedGenProvider`.
"""

from __future__ import annotations

import os
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from auto_affi.adapters.gemini_provider import GeminiProvider
from auto_affi.adapters.gen_provider import GenAsset, GenProvider
from auto_affi.adapters.kling_provider import (
    KlingGenerationError,
    KlingProvider,
    UploadImage,
    postiz_upload_image,
)
from auto_affi.pipeline.prompt_audit import ReferenceManifest
from auto_affi.workflows.budget import BudgetCircuitBreaker


@dataclass
class RoutedGenProvider:
    """A `GenProvider` that routes stills -> ``image_provider`` and video -> ``video_provider``.

    ``video_fallback`` (if set) is used ONLY when the primary video provider raises
    :class:`KlingGenerationError` — a real generation failure. Spend/gate stops propagate.
    """

    image_provider: GenProvider
    video_provider: GenProvider
    video_fallback: GenProvider | None = None

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
    ) -> GenAsset:
        return await self.image_provider.generate_image(
            stage=stage, prompt=prompt, run_dir=run_dir, manifest=manifest, budget=budget,
            reference_images=reference_images, model=model, aspect_ratio=aspect_ratio,
            estimated_cost_usd=estimated_cost_usd,
        )

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
        duration: int = 5,
        aspect_ratio: str = "9:16",
        estimated_cost_usd: float | None = None,
    ) -> GenAsset:
        try:
            return await self.video_provider.generate_video(
                stage=stage, prompt=prompt, run_dir=run_dir, manifest=manifest, budget=budget,
                reference_images=reference_images, model=model, duration=duration,
                aspect_ratio=aspect_ratio, estimated_cost_usd=estimated_cost_usd,
            )
        except KlingGenerationError:
            if self.video_fallback is None:
                raise
            # Fallback model has its own default model id — don't force Kling's onto Veo.
            return await self.video_fallback.generate_video(
                stage=stage, prompt=prompt, run_dir=run_dir, manifest=manifest, budget=budget,
                reference_images=reference_images, model=None, duration=duration,
                aspect_ratio=aspect_ratio, estimated_cost_usd=estimated_cost_usd,
            )


def build_default_provider(
    *, dry_run: bool = True, upload_image: UploadImage | None = None, allow_veo_fallback: bool = False
) -> GenProvider:
    """Wire the standard stack: Nano Banana Pro stills + Kling i2v video (the model lock).

    Per the model-lock compliance gate there is NO auto-fallback by default — a Kling
    failure halts + reports. ``AUTO_AFFI_VIDEO_MODEL=veo`` forces the legacy Veo-only path
    (a single GeminiProvider). ``allow_veo_fallback=True`` is an EXPLICIT override that wires
    automatic Kling->Veo recovery on a genuine generation failure (for unattended runs) —
    use it knowingly; it steps outside the no-self-fallback policy.
    """
    gemini = GeminiProvider(dry_run=dry_run)
    if os.environ.get("AUTO_AFFI_VIDEO_MODEL", "kling").lower() == "veo":
        return gemini
    kling = KlingProvider(dry_run=dry_run, upload_image=upload_image or postiz_upload_image)
    fallback = gemini if allow_veo_fallback else None
    return RoutedGenProvider(image_provider=gemini, video_provider=kling, video_fallback=fallback)
