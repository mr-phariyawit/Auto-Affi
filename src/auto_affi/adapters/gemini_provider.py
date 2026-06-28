"""Gemini generation provider — Nano Banana Pro stills + Veo 3 video (ADR-009).

Routes every call through the shared `enforce_spend_gate` (PGA gate + verify-before-
spend), so the gate is never duplicated or weakened. Live calls hit the Gemini API
(image: gemini-3-pro-image; video: Veo 3) via httpx; unit tests patch `_image_api` /
`_video_api` so no network is touched. ``dry_run=True`` (default) returns deterministic
stubs at cost 0.0 — keeps the offline slice green.

Gemini is billed per-use to a GCP project and exposes no pre-call credit balance, so the
spend gate relies on the mandatory budget circuit-breaker (+ project-level billing caps),
never a fabricated balance check.
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx

from auto_affi.adapters.gen_provider import (
    GenAsset,
    ProviderSpendError,
    enforce_spend_gate,
)
from auto_affi.pipeline.prompt_audit import ReferenceManifest
from auto_affi.workflows.budget import BudgetCircuitBreaker

_DEFAULT_IMAGE_MODEL = "gemini-3-pro-image"
# Veo 3.1-fast: required for first->last keyframe interpolation (`lastFrame`) and
# `referenceImages`. Veo 3.0-fast does text/first-frame only (verified 2026-06-28
# against ai.google.dev/gemini-api/docs/video). FLF2V storyboards need 3.1-fast.
_DEFAULT_VIDEO_MODEL = "veo-3.1-fast-generate-001"
_GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta"
_DRY_PLACEHOLDER = Path("/tmp/gemini_dryrun_placeholder")  # noqa: S108

# --- Cost model (ESTIMATES — Gemini/Veo pricing, documented, caller-overridable) ---
# Nano Banana Pro stills are cheap; Veo 3 is the cost driver. Veo 3 fast ~ $0.40/s,
# so an 8s clip (~$3.20) EXCEEDS the $1.80 video_gen node cap — the breaker will DENY,
# which is correct. Keep Veo clips short (<=4s -> ~$1.60) to stay under the cap, or
# raise the cap deliberately. This is a real cost consequence of ADR-009.
_IMAGE_COST_USD: float = 0.06
_VEO_COST_PER_SECOND: float = 0.40


@dataclass
class GeminiProvider:
    """`GenProvider` backed by the Gemini API (Nano Banana Pro + Veo 3)."""

    dry_run: bool = True
    api_key: str | None = None
    image_model: str = _DEFAULT_IMAGE_MODEL
    video_model: str = _DEFAULT_VIDEO_MODEL
    timeout_s: float = field(default=120.0)
    poll_interval_s: float = field(default=10.0)

    def __post_init__(self) -> None:
        if not self.dry_run and not self._key():
            raise ProviderSpendError("live GeminiProvider requires GEMINI_API_KEY in env or api_key")

    def _key(self) -> str:
        return self.api_key or os.environ.get("GEMINI_API_KEY", "")

    # ------------------------------------------------------------------ #
    # Public API (GenProvider Protocol)
    # ------------------------------------------------------------------ #

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
        est = _IMAGE_COST_USD if estimated_cost_usd is None else estimated_cost_usd
        await enforce_spend_gate(
            dry_run=self.dry_run, stage=stage, run_dir=run_dir, manifest=manifest,
            node="image_gen", estimated_cost_usd=est, budget=budget,
        )
        if self.dry_run:
            return GenAsset(kind="image", url="", local_path=_DRY_PLACEHOLDER, cost_usd=0.0,
                            raw=f"[DRY-RUN] image {model or self.image_model} stage={stage}")
        path = await self._image_api(model or self.image_model, prompt,
                                     [str(r) for r in reference_images], aspect_ratio, run_dir, stage)
        if budget is not None:
            budget.record_spend("image_gen", est)
        return GenAsset(kind="image", local_path=path, cost_usd=est, cost_estimated=True)

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
        first_frame: Path | str | None = None,
        last_frame: Path | str | None = None,
    ) -> GenAsset:
        est = _VEO_COST_PER_SECOND * duration if estimated_cost_usd is None else estimated_cost_usd
        await enforce_spend_gate(
            dry_run=self.dry_run, stage=stage, run_dir=run_dir, manifest=manifest,
            node="video_gen", estimated_cost_usd=est, budget=budget,
        )
        if self.dry_run:
            mode = "flf2v" if last_frame else ("i2v" if first_frame else "t2v")
            return GenAsset(kind="video", url="", local_path=_DRY_PLACEHOLDER, cost_usd=0.0,
                            raw=f"[DRY-RUN] video {model or self.video_model} stage={stage} {duration}s {mode}")
        path = await self._video_api(model or self.video_model, prompt, duration, aspect_ratio,
                                     run_dir, stage, first_frame, last_frame)
        if budget is not None:
            budget.record_spend("video_gen", est)
        return GenAsset(kind="video", local_path=path, cost_usd=est, cost_estimated=True)

    # ------------------------------------------------------------------ #
    # Live API (patched in unit tests — never hits the network there)
    # ------------------------------------------------------------------ #

    async def _image_api(
        self, model: str, prompt: str, refs: list[str], aspect_ratio: str,
        run_dir: Path | None, stage: str,
    ) -> Path:
        """Live Nano Banana Pro call -> saved PNG. Not exercised in CI (mocked)."""
        parts: list[dict[str, object]] = [{"text": prompt}]
        for ref in refs:
            raw = await asyncio.to_thread(Path(ref).read_bytes)
            data = base64.b64encode(raw).decode()
            parts.append({"inline_data": {"mime_type": "image/png", "data": data}})
        body = {"contents": [{"parts": parts}],
                "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect_ratio}}}
        url = f"{_GEMINI_BASE}/models/{model}:generateContent?key={self._key()}"
        async with httpx.AsyncClient(timeout=self.timeout_s) as client:
            resp = await client.post(url, json=body)
            resp.raise_for_status()
            payload = resp.json()
        b64 = _first_inline_image(payload)
        out = (run_dir or Path(".")) / f"{stage}.png"
        await asyncio.to_thread(out.write_bytes, base64.b64decode(b64))
        return out

    async def _video_api(
        self, model: str, prompt: str, duration: int, aspect_ratio: str,
        run_dir: Path | None, stage: str,
        first_frame: Path | str | None = None, last_frame: Path | str | None = None,
    ) -> Path:
        """Live Veo call (long-running op) -> saved mp4. Not exercised in CI (mocked).

        Supports text-to-video, image-to-video (``first_frame`` -> ``instances[].image``)
        and FLF2V interpolation (``last_frame`` -> ``instances[].lastFrame``; Veo 3.1+ only).
        Thai-no-lipsync: no native Veo audio is requested; Thai VO is muxed separately.
        """
        first_b64 = (await _read_b64(first_frame)) if first_frame else None
        last_b64 = (await _read_b64(last_frame)) if last_frame else None
        body = build_video_body(prompt, duration, aspect_ratio, first_b64, last_b64)
        key = self._key()
        async with httpx.AsyncClient(timeout=self.timeout_s) as client:
            start = await client.post(
                f"{_GEMINI_BASE}/models/{model}:predictLongRunning?key={key}", json=body)
            start.raise_for_status()
            op_name = start.json()["name"]
            while True:
                poll = await client.get(f"{_GEMINI_BASE}/{op_name}?key={key}")
                poll.raise_for_status()
                op = poll.json()
                if op.get("done"):
                    break
                await asyncio.sleep(self.poll_interval_s)
            uri = _veo_video_uri(op)
            dl = await client.get(uri if "key=" in uri else f"{uri}&key={key}")
            dl.raise_for_status()
            out = (run_dir or Path(".")) / f"{stage}.mp4"
            await asyncio.to_thread(out.write_bytes, dl.content)
            return out


def build_video_body(
    prompt: str, duration: int, aspect_ratio: str,
    first_b64: str | None = None, last_b64: str | None = None,
) -> dict[str, Any]:
    """Pure builder for the Veo predictLongRunning request (verified field names).

    - text-to-video: prompt only -> ``personGeneration: allow_all``.
    - image-to-video: + ``image`` (first frame) -> ``personGeneration: allow_adult``.
    - FLF2V: + ``lastFrame`` (Veo 3.1+) -> interpolates motion between the two keyframes.
    ``durationSeconds`` is a STRING per the API; ``generateAudio`` is always False
    (Thai VO is muxed at the edit stage, never baked native).
    """
    instance: dict[str, Any] = {"prompt": prompt}
    if first_b64 is not None:
        instance["image"] = {"inlineData": {"mimeType": "image/png", "data": first_b64}}
    if last_b64 is not None:
        instance["lastFrame"] = {"inlineData": {"mimeType": "image/png", "data": last_b64}}
    params: dict[str, Any] = {
        "aspectRatio": aspect_ratio,
        "durationSeconds": str(duration),
        "generateAudio": False,
        "personGeneration": "allow_adult" if first_b64 is not None else "allow_all",
    }
    return {"instances": [instance], "parameters": params}


async def _read_b64(p: Path | str) -> str:
    raw = await asyncio.to_thread(Path(p).read_bytes)
    return base64.b64encode(raw).decode()


def _first_inline_image(payload: Any) -> str:
    for cand in payload.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inline_data") or part.get("inlineData")
            if inline and inline.get("data"):
                return str(inline["data"])
    raise ProviderSpendError(f"no image in Gemini response: {json.dumps(payload)[:300]}")


def _veo_video_uri(op: Any) -> str:
    resp = op.get("response", {})
    # Veo nests samples under generateVideoResponse (verified); older shape is flat.
    gvr = resp.get("generateVideoResponse") or resp.get("generate_video_response") or {}
    samples = (gvr.get("generatedSamples") or gvr.get("generated_samples")
               or resp.get("generatedSamples") or resp.get("generated_samples") or [])
    if samples:
        video = samples[0].get("video", {})
        uri = video.get("uri") or video.get("url")
        if uri:
            return str(uri)
    raise ProviderSpendError(f"no video uri in Veo response: {json.dumps(op)[:300]}")
