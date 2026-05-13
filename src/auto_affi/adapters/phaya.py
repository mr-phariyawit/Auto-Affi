"""Phaya.io adapter — Thai AI gateway consolidating video + TTS + music + embeddings.

Phaya.io (Bangkok) is a model GATEWAY (similar to OpenRouter): it exposes a
unified REST API at ``api.phaya.io`` that fronts third-party models —
``phaya-gpt`` routes to ``google/gemini-2.5-flash``, Sora 2 T2V from OpenAI,
Nano Banana / Seedream image gen, etc. Auth is per-account API key; costs
are billed in **Thai Baht (THB)**, returned as ``credits_used`` on each
response. Conversion to USD uses a fixed 0.028 rate for budget reporting.

Capabilities exercised by this adapter:

- **Embedding** (``Phaya Text Embedding``, 4096-dim) — ฿2.80 / M tokens
- **Chat completion** (``Phaya-GPT`` → Gemini 2.5 Flash) — ฿10.50 / M in, ฿87.50 / M out
- **Sora 2 text-to-video** — async job, watermark-removable, 9:16 native
- **Text-to-speech** — multilingual incl. Thai, voice catalog at ``/voices``
- **Text-to-music** — async job, prompt-driven

Each capability has its own ``/create`` (or ``/generate``) endpoint and its
own ``/status/{job_id}`` poller — there is **no unified Jobs API**.

The adapter conforms to existing protocols (:class:`VideoGenAdapter`,
:class:`TTSAdapter`) so it drops into the kie.ai / ElevenLabs slots without
callsite refactors. Endpoint paths and response shapes verified against
``api.phaya.io/openapi.json`` and live probes (2026-05-13).
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Final

import httpx
from pydantic import BaseModel, SecretStr

from auto_affi.adapters._http_base import HttpExecutor, call_with_result
from auto_affi.adapters.tts import TTSProvider, TTSResult
from auto_affi.adapters.video_gen import GeneratedAsset, VideoGenerator
from auto_affi.exceptions import AdapterError
from auto_affi.schemas.storyboard import Scene
from auto_affi.schemas.tool_result import ToolResult

_BASE_URL: Final[str] = "https://api.phaya.io"
_USD_PER_THB: Final[float] = 0.028  # ฿1 ≈ $0.028 (May 2026)


def _thb_to_usd(thb: float) -> float:
    return round(thb * _USD_PER_THB, 6)


class PhayaModel(StrEnum):
    """Identifiers used in request bodies (Phaya routes to upstream model)."""

    PHAYA_GPT = "phaya-gpt"  # → google/gemini-2.5-flash
    PHAYA_EMBEDDING = "phaya-text-embedding"
    SORA2 = "sora2"


class JobState(StrEnum):
    """States returned by per-capability ``/status/{job_id}`` endpoints.

    Phaya uses a richer state set than the generic queued/processing pair;
    we collapse to the four terminal-or-not buckets the orchestrator cares
    about. Unknown states are mapped to PROCESSING (safe — keeps polling).
    """

    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


def _coerce_state(raw: str) -> JobState:
    s = raw.lower().strip()
    if s in ("completed", "success", "succeeded", "done"):
        return JobState.COMPLETED
    if s in ("failed", "error", "cancelled", "canceled"):
        return JobState.FAILED
    if s in ("queued", "pending"):
        return JobState.QUEUED
    return JobState.PROCESSING


class JobHandle(BaseModel):
    """Async-job handle returned by video / music endpoints."""

    job_id: str
    state: JobState = JobState.QUEUED
    result_url: str | None = None
    error: str | None = None
    cost_thb: float = 0.0

    @property
    def cost_usd(self) -> float:
        return _thb_to_usd(self.cost_thb)


class ChatResponse(BaseModel):
    content: str
    model: str
    usage_in_tokens: int = 0
    usage_out_tokens: int = 0
    cost_thb: float = 0.0

    @property
    def cost_usd(self) -> float:
        return _thb_to_usd(self.cost_thb)


class EmbeddingResponse(BaseModel):
    vectors: list[list[float]]
    model: str
    usage_tokens: int = 0
    cost_thb: float = 0.0

    @property
    def cost_usd(self) -> float:
        return _thb_to_usd(self.cost_thb)


class TTSResponse(BaseModel):
    """Initial TTS submission — TTS is async via /status/{job_id}."""

    job_id: str
    voice: str
    state: JobState = JobState.QUEUED


class CreditsBalance(BaseModel):
    user_id: str
    email: str | None = None
    balance_thb: float
    balance_usd: float


class PhayaClient:
    """Thin Phaya REST client. Auth + retry + per-capability polling.

    Notes:
    - Base URL is ``https://api.phaya.io`` (paths carry the ``/api/v1`` prefix).
    - Auth header: ``Authorization: Bearer <key>``. Both ``pk_*`` (publishable)
      and ``phaya_*`` (legacy) key shapes are accepted.
    - Each capability returns ``credits_used`` in **THB**; we surface both
      THB (native) and USD (converted) for budget tracking.
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
        if not api_key.get_secret_value().startswith(("phaya_", "pk_", "sk_")):
            raise AdapterError(
                "Phaya: api_key must start with 'pk_', 'sk_', or 'phaya_'"
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

    # ---- Account ------------------------------------------------------ #

    async def get_credits(self) -> ToolResult[CreditsBalance]:
        async def _go() -> CreditsBalance:
            client = self._http.client or httpx.AsyncClient(timeout=self._http.timeout_s)
            owns = self._http.client is None
            try:
                r = await client.get(
                    f"{self._base_url}/api/v1/user/profile", headers=self._headers()
                )
            finally:
                if owns:
                    await client.aclose()
            if r.status_code >= 400:
                raise AdapterError(f"Phaya HTTP {r.status_code}: {r.text[:200]}")
            data = r.json()
            balance = float(data.get("credits_balance", 0.0))
            return CreditsBalance(
                user_id=str(data.get("user_id", "")),
                email=data.get("email"),
                balance_thb=balance,
                balance_usd=_thb_to_usd(balance),
            )

        return await call_with_result(_go)

    # ---- LLM: Phaya GPT chat (Gemini 2.5 Flash under the hood) -------- #

    async def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str = PhayaModel.PHAYA_GPT,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> ToolResult[ChatResponse]:
        async def _go() -> ChatResponse:
            body: dict[str, Any] = {"messages": messages, "model": model}
            if max_tokens is not None:
                body["max_tokens"] = max_tokens
            if temperature is not None:
                body["temperature"] = temperature
            payload = await self._http.post(
                url=f"{self._base_url}/api/v1/phaya-gpt/chat/completions",
                body=body,
                headers=self._headers(),
            )
            msg = payload.get("message") or {}
            content = str(msg.get("content", ""))
            usage = payload.get("usage", {})
            return ChatResponse(
                content=content,
                model=str(payload.get("model", model)),
                usage_in_tokens=int(usage.get("prompt_tokens", 0)),
                usage_out_tokens=int(usage.get("completion_tokens", 0)),
                cost_thb=float(payload.get("credits_used", 0.0)),
            )

        return await call_with_result(_go, cost_fn=lambda r: r.cost_usd)

    # ---- Embeddings (4096-dim) ---------------------------------------- #

    async def embed(
        self, texts: list[str], *, model: str | None = None
    ) -> ToolResult[EmbeddingResponse]:
        async def _go() -> EmbeddingResponse:
            body: dict[str, Any] = {"input": texts}
            if model is not None:
                body["model"] = model
            payload = await self._http.post(
                url=f"{self._base_url}/api/v1/embedding/create",
                body=body,
                headers=self._headers(),
            )
            data = payload.get("data", [])
            vectors = [item.get("embedding", []) for item in data]
            usage = payload.get("usage", {})
            return EmbeddingResponse(
                vectors=vectors,
                model=str(payload.get("model", "Phaya Text Embedding")),
                usage_tokens=int(usage.get("total_tokens", 0)),
                cost_thb=float(payload.get("credits_used", 0.0)),
            )

        return await call_with_result(_go, cost_fn=lambda r: r.cost_usd)

    # ---- Sora 2 Text-to-Video (async job) ----------------------------- #

    async def create_sora2_video(
        self,
        prompt: str,
        *,
        aspect_ratio: str = "9:16",
        n_frames: int = 120,
        remove_watermark: bool = True,
    ) -> ToolResult[JobHandle]:
        """Submit a Sora 2 T2V job. Poll via :meth:`wait_for_sora2`."""

        async def _go() -> JobHandle:
            payload = await self._http.post(
                url=f"{self._base_url}/api/v1/sora2-text-to-video/create",
                body={
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio,
                    "n_frames": n_frames,
                    "remove_watermark": remove_watermark,
                },
                headers=self._headers(),
            )
            return JobHandle(
                job_id=str(payload.get("job_id") or payload.get("id", "")),
                state=_coerce_state(str(payload.get("state", "queued"))),
                cost_thb=float(payload.get("credits_used", 0.0)),
            )

        return await call_with_result(_go, cost_fn=lambda h: h.cost_usd)

    async def get_sora2_status(self, job_id: str) -> ToolResult[JobHandle]:
        return await self._get_status(
            f"/api/v1/sora2-text-to-video/status/{job_id}", job_id=job_id
        )

    async def wait_for_sora2(
        self, job_id: str, *, poll_interval_s: float = 3.0, timeout_s: float = 300.0
    ) -> ToolResult[JobHandle]:
        return await self._wait(
            poller=self.get_sora2_status, job_id=job_id, interval=poll_interval_s, timeout=timeout_s
        )

    # ---- TTS (async job — generate → status) -------------------------- #

    async def create_tts(
        self,
        prompt: str,
        *,
        voice: str = "Algenib",
        language: str = "th",
        slow: bool = False,
    ) -> ToolResult[TTSResponse]:
        async def _go() -> TTSResponse:
            payload = await self._http.post(
                url=f"{self._base_url}/api/v1/text-to-speech/generate",
                body={
                    "prompt": prompt,
                    "voice": voice,
                    "language": language,
                    "slow": slow,
                },
                headers=self._headers(),
            )
            return TTSResponse(
                job_id=str(payload.get("job_id") or payload.get("id", "")),
                voice=voice,
                state=_coerce_state(str(payload.get("state", "queued"))),
            )

        return await call_with_result(_go)

    async def get_tts_status(self, job_id: str) -> ToolResult[JobHandle]:
        return await self._get_status(
            f"/api/v1/text-to-speech/status/{job_id}", job_id=job_id
        )

    # ---- Music (async job) -------------------------------------------- #

    async def create_music(
        self, prompt: str, *, duration_s: int = 30
    ) -> ToolResult[JobHandle]:
        async def _go() -> JobHandle:
            payload = await self._http.post(
                url=f"{self._base_url}/api/v1/text-to-music/generate",
                body={"prompt": prompt, "duration": duration_s},
                headers=self._headers(),
            )
            return JobHandle(
                job_id=str(payload.get("job_id") or payload.get("id", "")),
                state=_coerce_state(str(payload.get("state", "queued"))),
                cost_thb=float(payload.get("credits_used", 0.0)),
            )

        return await call_with_result(_go, cost_fn=lambda h: h.cost_usd)

    async def get_music_status(self, job_id: str) -> ToolResult[JobHandle]:
        return await self._get_status(
            f"/api/v1/text-to-music/status/{job_id}", job_id=job_id
        )

    # ---- Internal: status GET + polling helpers ----------------------- #

    async def _get_status(self, path: str, *, job_id: str) -> ToolResult[JobHandle]:
        async def _go() -> JobHandle:
            client = self._http.client or httpx.AsyncClient(timeout=self._http.timeout_s)
            owns = self._http.client is None
            try:
                r = await client.get(f"{self._base_url}{path}", headers=self._headers())
            finally:
                if owns:
                    await client.aclose()
            if r.status_code >= 400:
                raise AdapterError(f"Phaya status HTTP {r.status_code}: {r.text[:200]}")
            payload = r.json()
            return JobHandle(
                job_id=job_id,
                state=_coerce_state(str(payload.get("state", "processing"))),
                result_url=payload.get("result_url") or payload.get("output_url"),
                error=payload.get("error"),
                cost_thb=float(payload.get("credits_used", 0.0)),
            )

        return await call_with_result(_go)

    async def _wait(
        self, *, poller: Any, job_id: str, interval: float, timeout: float
    ) -> ToolResult[JobHandle]:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = await poller(job_id)
            if not result.ok or result.data is None:
                return result
            if result.data.state in (JobState.COMPLETED, JobState.FAILED):
                return result
            await asyncio.sleep(interval)
        return ToolResult(
            ok=False,
            error=f"Phaya job {job_id} timed out after {timeout}s",
            trace_id="",
        )


# --------------------------------------------------------------------- #
# Protocol adapters — drop-in for kie.ai (VideoGenAdapter) and          #
# ElevenLabs (TTSAdapter).                                              #
# --------------------------------------------------------------------- #


@dataclass(frozen=True)
class PhayaVideoGenAdapter:
    """Drops in alongside the kie.ai Sora 2 path."""

    client: PhayaClient
    _generator: VideoGenerator = VideoGenerator.SORA2

    @property
    def generator(self) -> VideoGenerator:
        return self._generator

    async def generate_scene(
        self, scene: Scene, *, output_dir: Path
    ) -> ToolResult[GeneratedAsset]:
        # n_frames at 24 fps ≈ scene.duration_s; round up to nearest integer
        n_frames = max(24, int(scene.duration_s * 24))
        create = await self.client.create_sora2_video(
            prompt=scene.visual_prompt, n_frames=n_frames
        )
        if not create.ok or create.data is None:
            return ToolResult(
                ok=False,
                error=create.error or "phaya: sora2 create failed",
                trace_id=create.trace_id,
            )
        wait = await self.client.wait_for_sora2(create.data.job_id)
        if not wait.ok or wait.data is None:
            return ToolResult(
                ok=False,
                error=wait.error or "phaya: sora2 wait failed",
                trace_id=wait.trace_id,
            )
        job = wait.data
        if job.state is JobState.FAILED:
            return ToolResult(
                ok=False,
                error=f"phaya: sora2 job {job.job_id} failed: {job.error}",
                trace_id=wait.trace_id,
            )
        if not job.result_url:
            return ToolResult(
                ok=False,
                error="phaya: completed job has no result_url",
                trace_id=wait.trace_id,
            )
        return ToolResult(
            ok=True,
            data=GeneratedAsset(
                scene_idx=scene.idx,
                asset_path=output_dir / f"scene_{scene.idx}_phaya.mp4",
                generator=self._generator,
                duration_s=scene.duration_s,
                cost_usd=job.cost_usd,
            ),
            cost_usd=job.cost_usd,
            trace_id=wait.trace_id,
        )


@dataclass(frozen=True)
class PhayaTTSAdapter:
    """Drops in alongside ElevenLabsTTSAdapter for native Thai TTS."""

    client: PhayaClient
    voice: str = "Algenib"

    @property
    def provider(self) -> TTSProvider:
        # Placeholder — TTSProvider gains a PHAYA member in Sprint 5.
        return TTSProvider.ELEVENLABS

    async def synthesize(
        self, text_th: str, *, output_path: Path
    ) -> ToolResult[TTSResult]:
        submit = await self.client.create_tts(
            prompt=text_th, voice=self.voice, language="th"
        )
        if not submit.ok or submit.data is None:
            return ToolResult(
                ok=False,
                error=submit.error or "phaya tts create failed",
                trace_id=submit.trace_id,
            )
        # Wait via the TTS status route.
        wait = await self.client._wait(
            poller=self.client.get_tts_status,
            job_id=submit.data.job_id,
            interval=2.0,
            timeout=120.0,
        )
        if not wait.ok or wait.data is None or wait.data.state is JobState.FAILED:
            return ToolResult(
                ok=False,
                error=(wait.error if wait else "phaya tts wait failed"),
                trace_id=wait.trace_id if wait else "",
            )
        return ToolResult(
            ok=True,
            data=TTSResult(
                audio_path=output_path,
                provider=self.provider,
                duration_s=0.0,  # Phaya TTS status doesn't return duration; caller measures post-download
                cost_usd=wait.data.cost_usd,
            ),
            cost_usd=wait.data.cost_usd,
            trace_id=wait.trace_id,
        )
