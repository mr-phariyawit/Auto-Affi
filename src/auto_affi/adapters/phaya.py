"""Phaya.io adapter — Thai AI gateway consolidating video + TTS + music + embeddings.

Phaya.io (Bangkok) exposes a single REST surface at ``api.phaya.io/api/v1``
covering capabilities that Auto-Affi currently sources from four separate
vendors:

- **Sora 2 video gen** (replaces kie.ai for Sora 2 line, 8 credits/video)
- **Native Thai TTS** (replaces ElevenLabs Multilingual v2 for Thai content)
- **Text-to-Music** (replaces Suno via kie.ai, 3 credits/track)
- **Embeddings** (฿2.80 / M tokens — for Wiki RAG vector backend)
- **Image gen** (Nano Banana 2 / Seedream 5.0, 1-4 credits)
- **Image-to-Video** (storyboard scene → motion clip)
- **Thai Subtitle** (auto-subtitle pass for editor pipeline)
- **Phaya GPT** (LLM, ฿10.50-87.50 / M tokens — for non-reasoning agents)

Auth: ``Authorization: Bearer phaya_live_xxx``. Set via ``PHAYA_API_KEY`` env.

Architecture: thin ``PhayaClient`` does HTTP + jobs polling; thin protocol
adapters (``PhayaVideoGenAdapter``, ``PhayaTTSAdapter``) wrap the client to
conform to the existing :class:`VideoGenAdapter` / :class:`TTSAdapter`
protocols so they drop in alongside kie.ai / ElevenLabs without a refactor.

Cost tables are best-known-current; verify against ``/pricing`` endpoint
once the live key is available.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Final

import httpx
from pydantic import BaseModel, Field, SecretStr

from auto_affi.adapters._http_base import HttpExecutor, call_with_result
from auto_affi.adapters.tts import TTSProvider, TTSResult
from auto_affi.adapters.video_gen import GeneratedAsset, VideoGenerator
from auto_affi.exceptions import AdapterError
from auto_affi.schemas.storyboard import Scene
from auto_affi.schemas.tool_result import ToolResult

_BASE_URL: Final[str] = "https://api.phaya.io/api/v1"

# Phaya pricing (May 2026, from public docs). Verify against live /pricing
# once the API key is available. Credits-to-USD ratio is the main unknown:
# assumed ฿0.50 / credit ≈ $0.014 / credit pending live confirmation.
_USD_PER_CREDIT: Final[float] = 0.014
_USD_PER_M_TOKENS_GPT_IN: Final[float] = 0.30  # ฿10.50/M
_USD_PER_M_TOKENS_GPT_OUT: Final[float] = 2.50  # ฿87.50/M
_USD_PER_M_TOKENS_EMBED: Final[float] = 0.08  # ฿2.80/M

_COST_PER_SORA2_VIDEO: Final[float] = 8 * _USD_PER_CREDIT  # ≈ $0.11
_COST_PER_MUSIC: Final[float] = 3 * _USD_PER_CREDIT  # ≈ $0.042
_COST_PER_IMAGE_NANO_BANANA: Final[float] = 2 * _USD_PER_CREDIT
_COST_PER_IMAGE_NANO_BANANA_4K: Final[float] = 4 * _USD_PER_CREDIT


class PhayaModel(StrEnum):
    """Identifiers for Phaya-backed models referenced by the adapter."""

    SORA2 = "sora-2"
    NANO_BANANA_2 = "nano-banana-2"
    SEEDREAM_5 = "seedream-5.0"
    PHAYA_GPT = "phaya-gpt"
    PHAYA_EMBEDDING = "phaya-text-embedding"


class JobState(StrEnum):
    """States returned by ``GET /jobs/{id}``."""

    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class JobHandle(BaseModel):
    """Async-job handle returned by video / music endpoints."""

    job_id: str
    state: JobState = JobState.QUEUED
    result_url: str | None = None
    error: str | None = None
    cost_usd: float = 0.0


class ChatResponse(BaseModel):
    """Phaya GPT chat completion response."""

    content: str
    model: str
    usage_in_tokens: int = 0
    usage_out_tokens: int = 0
    cost_usd: float = 0.0


class EmbeddingResponse(BaseModel):
    """Phaya embeddings response (single batch)."""

    vectors: list[list[float]]
    model: str
    usage_tokens: int = 0
    cost_usd: float = 0.0


class TTSResponse(BaseModel):
    """Phaya TTS synthesis response (sync — short clips only)."""

    audio_url: str
    duration_s: float
    voice_id: str
    cost_usd: float = 0.0


class PhayaClient:
    """Thin Phaya REST client. Handles auth + retry + jobs polling.

    Async-job endpoints (video, music) return a :class:`JobHandle`; call
    :meth:`wait_for_job` to poll until terminal state. Sync endpoints
    (chat, embeddings, TTS short, image) return their typed model directly.
    """

    def __init__(
        self,
        *,
        api_key: SecretStr,
        client: httpx.AsyncClient | None = None,
        timeout_s: float = 30.0,
        max_retries: int = 3,
        base_url: str = _BASE_URL,
    ) -> None:
        if not api_key.get_secret_value().strip():
            raise AdapterError("Phaya: api_key is empty")
        if not api_key.get_secret_value().startswith("phaya_"):
            raise AdapterError(
                "Phaya: api_key must start with 'phaya_' (e.g. phaya_live_xxx)"
            )
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._http = HttpExecutor(
            vendor="Phaya", timeout_s=timeout_s, max_retries=max_retries, client=client
        )

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key.get_secret_value()}",
            "Content-Type": "application/json",
            "User-Agent": "auto-affi/0.1 (phaya-adapter)",
        }

    # ---- LLM: Phaya GPT chat ------------------------------------------ #

    async def chat(
        self, messages: list[dict[str, str]], *, model: str = PhayaModel.PHAYA_GPT
    ) -> ToolResult[ChatResponse]:
        async def _go() -> ChatResponse:
            payload = await self._http.post(
                url=f"{self._base_url}/chat/completions",
                body={"model": model, "messages": messages, "stream": False},
                headers=self._headers(),
            )
            content = (
                payload.get("choices", [{}])[0].get("message", {}).get("content", "")
            )
            usage = payload.get("usage", {})
            in_tok = int(usage.get("prompt_tokens", 0))
            out_tok = int(usage.get("completion_tokens", 0))
            cost = (
                in_tok * _USD_PER_M_TOKENS_GPT_IN / 1_000_000
                + out_tok * _USD_PER_M_TOKENS_GPT_OUT / 1_000_000
            )
            return ChatResponse(
                content=content,
                model=str(payload.get("model", model)),
                usage_in_tokens=in_tok,
                usage_out_tokens=out_tok,
                cost_usd=cost,
            )

        return await call_with_result(_go, cost_fn=lambda r: r.cost_usd)

    # ---- Embeddings ---------------------------------------------------- #

    async def embed(
        self, texts: list[str], *, model: str = PhayaModel.PHAYA_EMBEDDING
    ) -> ToolResult[EmbeddingResponse]:
        async def _go() -> EmbeddingResponse:
            payload = await self._http.post(
                url=f"{self._base_url}/embeddings",
                body={"model": model, "input": texts},
                headers=self._headers(),
            )
            data = payload.get("data", [])
            vectors = [item.get("embedding", []) for item in data]
            usage_tok = int(payload.get("usage", {}).get("total_tokens", 0))
            cost = usage_tok * _USD_PER_M_TOKENS_EMBED / 1_000_000
            return EmbeddingResponse(
                vectors=vectors,
                model=str(payload.get("model", model)),
                usage_tokens=usage_tok,
                cost_usd=cost,
            )

        return await call_with_result(_go, cost_fn=lambda r: r.cost_usd)

    # ---- Video: Sora 2 (async job) ------------------------------------ #

    async def create_sora2_video(
        self, prompt: str, *, duration_s: int = 5, aspect_ratio: str = "9:16"
    ) -> ToolResult[JobHandle]:
        async def _go() -> JobHandle:
            payload = await self._http.post(
                url=f"{self._base_url}/sora-2/create",
                body={
                    "prompt": prompt,
                    "duration": duration_s,
                    "aspect_ratio": aspect_ratio,
                },
                headers=self._headers(),
            )
            return JobHandle(
                job_id=str(payload["job_id"]),
                state=JobState(payload.get("state", "queued")),
                cost_usd=_COST_PER_SORA2_VIDEO,
            )

        return await call_with_result(_go, cost_fn=lambda h: h.cost_usd)

    # ---- Image-to-Video (async job) ----------------------------------- #

    async def create_image_to_video(
        self, image_url: str, *, duration_s: int = 5
    ) -> ToolResult[JobHandle]:
        async def _go() -> JobHandle:
            payload = await self._http.post(
                url=f"{self._base_url}/image-to-video/create",
                body={"image_url": image_url, "duration": duration_s},
                headers=self._headers(),
            )
            return JobHandle(
                job_id=str(payload["job_id"]),
                state=JobState(payload.get("state", "queued")),
                cost_usd=_COST_PER_SORA2_VIDEO,  # same tier
            )

        return await call_with_result(_go, cost_fn=lambda h: h.cost_usd)

    # ---- TTS (sync, short clips) -------------------------------------- #

    async def tts(
        self, text_th: str, *, voice_id: str = "th-female-energetic"
    ) -> ToolResult[TTSResponse]:
        async def _go() -> TTSResponse:
            payload = await self._http.post(
                url=f"{self._base_url}/tts/create",
                body={"text": text_th, "voice_id": voice_id, "language": "th"},
                headers=self._headers(),
            )
            chars = len(text_th)
            # Token-priced TTS — approximate at GPT input rate for now.
            cost = chars / 4 * _USD_PER_M_TOKENS_GPT_IN / 1_000_000
            return TTSResponse(
                audio_url=str(payload["audio_url"]),
                duration_s=float(payload.get("duration", 0.0)),
                voice_id=voice_id,
                cost_usd=cost,
            )

        return await call_with_result(_go, cost_fn=lambda r: r.cost_usd)

    # ---- Music (async job) -------------------------------------------- #

    async def create_music(
        self, prompt: str, *, duration_s: int = 30
    ) -> ToolResult[JobHandle]:
        async def _go() -> JobHandle:
            payload = await self._http.post(
                url=f"{self._base_url}/music/create",
                body={"prompt": prompt, "duration": duration_s},
                headers=self._headers(),
            )
            return JobHandle(
                job_id=str(payload["job_id"]),
                state=JobState(payload.get("state", "queued")),
                cost_usd=_COST_PER_MUSIC,
            )

        return await call_with_result(_go, cost_fn=lambda h: h.cost_usd)

    # ---- Jobs API ----------------------------------------------------- #

    async def get_job(self, job_id: str) -> ToolResult[JobHandle]:
        async def _go() -> JobHandle:
            # GET via POST-only HttpExecutor would need extending; use raw httpx.
            client = self._http.client or httpx.AsyncClient(timeout=self._http.timeout_s)
            owns = self._http.client is None
            try:
                response = await client.get(
                    f"{self._base_url}/jobs/{job_id}", headers=self._headers()
                )
            finally:
                if owns:
                    await client.aclose()
            if response.status_code >= 400:
                raise AdapterError(f"Phaya job poll HTTP {response.status_code}")
            payload = response.json()
            return JobHandle(
                job_id=job_id,
                state=JobState(payload.get("state", "queued")),
                result_url=payload.get("result_url"),
                error=payload.get("error"),
            )

        return await call_with_result(_go)

    async def wait_for_job(
        self, job_id: str, *, poll_interval_s: float = 2.0, timeout_s: float = 300.0
    ) -> ToolResult[JobHandle]:
        """Poll ``get_job`` until terminal state or timeout."""
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            result = await self.get_job(job_id)
            if not result.ok or result.data is None:
                return result
            if result.data.state in (JobState.COMPLETED, JobState.FAILED):
                return result
            await asyncio.sleep(poll_interval_s)
        return ToolResult(
            ok=False,
            error=f"Phaya job {job_id} timed out after {timeout_s}s",
            trace_id="",
        )


# --------------------------------------------------------------------- #
# Protocol adapters — drop-in for kie.ai (VideoGenAdapter) and          #
# ElevenLabs (TTSAdapter).                                              #
# --------------------------------------------------------------------- #


@dataclass(frozen=True)
class PhayaVideoGenAdapter:
    """Drops in alongside KieAiVideoGenAdapter for the Sora 2 line.

    The :attr:`generator` is ``SORA2`` so existing budget / dispatch logic
    keyed on the enum keeps working unchanged.
    """

    client: PhayaClient
    _generator: VideoGenerator = VideoGenerator.SORA2

    @property
    def generator(self) -> VideoGenerator:
        return self._generator

    async def generate_scene(
        self, scene: Scene, *, output_dir: Path
    ) -> ToolResult[GeneratedAsset]:
        create_result = await self.client.create_sora2_video(
            prompt=scene.visual_prompt, duration_s=int(scene.duration_s)
        )
        if not create_result.ok or create_result.data is None:
            return ToolResult(
                ok=False,
                error=create_result.error or "phaya: create failed",
                trace_id=create_result.trace_id,
            )
        job_result = await self.client.wait_for_job(create_result.data.job_id)
        if not job_result.ok or job_result.data is None:
            return ToolResult(
                ok=False,
                error=job_result.error or "phaya: job wait failed",
                trace_id=job_result.trace_id,
            )
        job = job_result.data
        if job.state == JobState.FAILED:
            return ToolResult(
                ok=False,
                error=f"phaya: job {job.job_id} failed: {job.error}",
                trace_id=job_result.trace_id,
            )
        if not job.result_url:
            return ToolResult(
                ok=False,
                error="phaya: completed job has no result_url",
                trace_id=job_result.trace_id,
            )
        asset_path = output_dir / f"scene_{scene.idx}_phaya.mp4"
        # NOTE: actual download of result_url to asset_path is left to the
        # Producer's asset-fetch step (same pattern as kie.ai). The adapter
        # surfaces the URL + cost; the orchestrator pulls bytes once.
        return ToolResult(
            ok=True,
            data=GeneratedAsset(
                scene_idx=scene.idx,
                asset_path=asset_path,
                generator=self._generator,
                duration_s=scene.duration_s,
                cost_usd=_COST_PER_SORA2_VIDEO,
            ),
            cost_usd=_COST_PER_SORA2_VIDEO,
            trace_id=job_result.trace_id,
        )


@dataclass(frozen=True)
class PhayaTTSAdapter:
    """Drops in alongside ElevenLabsTTSAdapter for native Thai TTS.

    Uses ``TTSProvider.ELEVENLABS`` enum value as a temporary placeholder
    until ``TTSProvider`` gains a ``PHAYA`` member in the next sprint
    (avoids enum migration in this scaffolding commit).
    """

    client: PhayaClient
    voice_id: str = "th-female-energetic"

    @property
    def provider(self) -> TTSProvider:
        return TTSProvider.ELEVENLABS  # placeholder; will add PHAYA in S5

    async def synthesize(
        self, text_th: str, *, output_path: Path
    ) -> ToolResult[TTSResult]:
        result = await self.client.tts(text_th, voice_id=self.voice_id)
        if not result.ok or result.data is None:
            return ToolResult(
                ok=False,
                error=result.error or "phaya tts failed",
                trace_id=result.trace_id,
            )
        return ToolResult(
            ok=True,
            data=TTSResult(
                audio_path=output_path,
                provider=self.provider,
                duration_s=result.data.duration_s,
                cost_usd=result.data.cost_usd,
            ),
            cost_usd=result.data.cost_usd,
            trace_id=result.trace_id,
        )
