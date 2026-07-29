"""Kling generation provider — image-to-video via kie.ai (the cheap i2v path).

Verified 2026-07-24: Kling 2.6 i2v on kie.ai produced 1076x1924 5s clips at 55 credits
($0.275 ~= THB 9.3) each — 55-86% cheaper than Veo 3.1 Fast at equal-or-better quality on
our Shopee-ad shots (hold / couple-hair / couple-CTA); on the CTA it HELD the product +
eye-contact composition where Veo drifted. Kling here is VIDEO-ONLY (i2v); stills stay on
Nano Banana Pro (see :class:`GeminiProvider`). Wire the two via :class:`RoutedGenProvider`.

Same kie.ai host/auth/poll as the ElevenLabs VO path (docs/reference/kie-elevenlabs-vo.md):
  create  POST https://api.kie.ai/api/v1/jobs/createTask     (Bearer KIE_API_KEY)
  poll    GET  https://api.kie.ai/api/v1/jobs/recordInfo?taskId=<id>
  result  data.resultJson -> resultUrls[0] (.mp4; the download needs a browser User-Agent)

Every call routes through the shared ``enforce_spend_gate`` (PGA gate + verify-before-spend),
identical to GeminiProvider — the gate is never duplicated or weakened. ``dry_run=True``
(default) returns deterministic stubs at cost 0.0 so the offline slice stays green; the live
``_video_api`` is patched out in unit tests.

Kling 2.6 i2v needs a PUBLIC image URL for the seed frame (no base64/local path — kie.ai
rejects both). A local reference frame is hosted via the injectable ``upload_image`` callable
(default: Postiz CDN, verified fetchable by kie.ai 2026-07-24). An http(s) reference is used
as-is. No native audio is requested (``sound: false``) — Thai VO is muxed at the edit stage,
so the Thai-no-lipsync rule is preserved exactly as on the Veo path.
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
from collections.abc import Awaitable, Callable, Iterable
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

_KIE_BASE = "https://api.kie.ai"
_DEFAULT_VIDEO_MODEL = "kling-2.6/image-to-video"
_DRY_PLACEHOLDER = Path("/tmp/kling_dryrun_placeholder")  # noqa: S108
_BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120 Safari/537.36"
)

# --- Cost model (VERIFIED 2026-07-24: 55 credits = $0.275 for a 5s Kling 2.6 i2v clip) ---
# kie.ai bills credits (1 credit = $0.005). 5s = 55cr = $0.275; 10s ~= $0.55. Both sit well
# under the $1.80 video_gen node cap — that head-room vs Veo's $0.40/s IS the cost win.
_KLING_COST_PER_SECOND: float = 0.055

UploadImage = Callable[[Path], Awaitable[str]]


class KlingGenerationError(RuntimeError):
    """Kling generation itself failed (task fail / timeout / no result / network).

    Distinct from :class:`ProviderSpendError`, which is a DELIBERATE gate or budget stop.
    :class:`RoutedGenProvider` falls back to Veo on this error but never on a spend stop —
    a budget DENY must never be "recovered" by spending more on the pricier model.
    """


def build_kling_body(model: str, prompt: str, image_url: str, duration: str) -> dict[str, Any]:
    """Pure builder for the kie.ai Kling ``createTask`` request (VERIFIED 2026-07-24).

    Kling 2.6 i2v is deliberately minimal: 9:16 output comes from feeding a 9:16 SOURCE
    image (there is no ``aspectRatio`` field), ``duration`` is the STRING ``"5"`` or
    ``"10"``, and ``sound: false`` keeps it silent (Thai VO is muxed separately).
    """
    return {
        "model": model,
        "input": {"prompt": prompt, "image_urls": [image_url], "sound": False, "duration": duration},
    }


def _kling_duration(seconds: int) -> str:
    """Map a requested duration to Kling's allowed set ``{"5","10"}`` (5s is the minimum)."""
    return "10" if seconds >= 8 else "5"


def _kling_video_url(data: dict[str, Any]) -> str:
    """Extract the output mp4 URL from a ``recordInfo`` ``data`` block.

    ``resultJson`` is itself a JSON-encoded STRING holding ``{"resultUrls": ["...mp4"]}``.
    """
    rj = data.get("resultJson")
    if rj:
        try:
            urls = json.loads(rj).get("resultUrls") or []
        except (json.JSONDecodeError, TypeError, AttributeError):
            urls = []
        if urls:
            return str(urls[0])
    raise KlingGenerationError(f"no video url in kling record: {json.dumps(data)[:300]}")


async def postiz_upload_image(path: Path) -> str:
    """Host a local image on the Postiz CDN and return its public URL (the VERIFIED default).

    kie.ai i2v requires a public image URL; the Postiz uploader returns a CDN URL that kie.ai
    fetches successfully (verified 2026-07-24). Requires ``postiz auth:login`` done once. The
    CLI prints a header line before the JSON, so we slice from the first ``{``/``[``.
    """
    def _run() -> str:
        postiz = str(Path("~/.hermes/node/bin/postiz").expanduser())
        out = subprocess.run(  # noqa: S603 - trusted local CLI, fixed args
            [postiz, "upload", str(path)], capture_output=True, text=True, timeout=120
        ).stdout
        candidates = [i for i in (out.find("{"), out.find("[")) if i != -1]
        if not candidates:
            raise KlingGenerationError(f"postiz upload gave no JSON: {out[:200]}")
        payload = json.loads(out[min(candidates):])
        rec = payload[0] if isinstance(payload, list) else payload
        url = rec.get("path")
        if not url:
            raise KlingGenerationError(f"postiz upload has no path: {out[:200]}")
        return str(url)

    return await asyncio.to_thread(_run)


@dataclass
class KlingProvider:
    """`GenProvider` (video only) backed by kie.ai Kling i2v.

    Still-image requests raise — route them to an image provider (Nano Banana Pro) via
    :class:`RoutedGenProvider`. Mirrors :class:`GeminiProvider`'s dry-run + spend-gate shape.
    """

    dry_run: bool = True
    api_key: str | None = None
    video_model: str = _DEFAULT_VIDEO_MODEL
    upload_image: UploadImage | None = None
    timeout_s: float = field(default=300.0)
    poll_interval_s: float = field(default=8.0)
    max_poll_s: float = field(default=540.0)

    def __post_init__(self) -> None:
        if not self.dry_run and not self._key():
            raise ProviderSpendError("live KlingProvider requires KIE_API_KEY in env or api_key")

    def _key(self) -> str:
        return self.api_key or os.environ.get("KIE_API_KEY") or os.environ.get("AUTO_AFFI__KIE_API_KEY", "")

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
        raise ProviderSpendError(
            "KlingProvider is video-only (i2v); route still images to an image provider "
            "(Nano Banana Pro / GeminiProvider) — see RoutedGenProvider."
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
        kdur = _kling_duration(duration)
        est = _KLING_COST_PER_SECOND * int(kdur) if estimated_cost_usd is None else estimated_cost_usd
        await enforce_spend_gate(
            dry_run=self.dry_run, stage=stage, run_dir=run_dir, manifest=manifest,
            node="video_gen", estimated_cost_usd=est, budget=budget,
        )
        if self.dry_run:
            return GenAsset(kind="video", url="", local_path=_DRY_PLACEHOLDER, cost_usd=0.0,
                            raw=f"[DRY-RUN] kling {model or self.video_model} stage={stage} {kdur}s i2v")
        refs = [str(r) for r in reference_images]
        if not refs:
            raise ProviderSpendError("Kling i2v requires a seed image in reference_images (got none)")
        path = await self._video_api(model or self.video_model, prompt, kdur, run_dir, stage, refs[0])
        if budget is not None:
            budget.record_spend("video_gen", est)
        return GenAsset(kind="video", local_path=path, cost_usd=est, cost_estimated=True)

    # ------------------------------------------------------------------ #
    # Live API (patched in unit tests — never hits the network there)
    # ------------------------------------------------------------------ #

    async def _to_url(self, seed: str) -> str:
        """Resolve a seed reference to a public URL kie.ai can fetch."""
        if seed.startswith(("http://", "https://")):
            return seed
        if self.upload_image is None:
            raise ProviderSpendError(
                "Kling seed is a local path but no upload_image was provided; pass a public "
                "URL in reference_images or wire an uploader (e.g. postiz_upload_image)"
            )
        return await self.upload_image(Path(seed))

    async def _video_api(
        self, model: str, prompt: str, kdur: str, run_dir: Path | None, stage: str, seed: str,
    ) -> Path:
        """Live kie.ai Kling call (create -> poll -> download). Not exercised in CI (mocked)."""
        image_url = await self._to_url(seed)
        body = build_kling_body(model, prompt, image_url, kdur)
        headers = {"Authorization": f"Bearer {self._key()}", "Content-Type": "application/json"}
        async with httpx.AsyncClient(timeout=self.timeout_s, follow_redirects=True) as client:
            cr = await client.post(f"{_KIE_BASE}/api/v1/jobs/createTask", json=body, headers=headers)
            cr.raise_for_status()
            tid = (cr.json().get("data") or {}).get("taskId")
            if not tid:
                raise KlingGenerationError(f"kling createTask returned no taskId: {cr.text[:300]}")
            waited = 0.0
            while True:
                await asyncio.sleep(self.poll_interval_s)
                waited += self.poll_interval_s
                rec = await client.get(
                    f"{_KIE_BASE}/api/v1/jobs/recordInfo", params={"taskId": tid}, headers=headers)
                rec.raise_for_status()
                data = rec.json().get("data") or {}
                state = data.get("state")
                if state == "success":
                    break
                if state in ("fail", "failed"):
                    raise KlingGenerationError(f"kling task {tid} failed: {json.dumps(data)[:300]}")
                if waited >= self.max_poll_s:
                    raise KlingGenerationError(f"kling task {tid} timed out after {waited:.0f}s (state={state})")
            url = _kling_video_url(data)
            dl = await client.get(url, headers={"User-Agent": _BROWSER_UA, "Referer": "https://kie.ai/"})
            dl.raise_for_status()
            out = (run_dir or Path(".")) / f"{stage}.mp4"
            await asyncio.to_thread(out.write_bytes, dl.content)
            return out
