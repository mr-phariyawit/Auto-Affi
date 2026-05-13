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

try:
    from auto_affi.adapters.gcs_storage import GcsStorage
except ImportError:  # google-cloud-storage not installed in some envs
    GcsStorage = None  # type: ignore[assignment, misc]

_BASE_URL: Final[str] = "https://api.phaya.io"
_USD_PER_THB: Final[float] = 0.028  # ฿1 ≈ $0.028 (May 2026)

# Domains we MUST never expose downstream per ADR-006. Phaya stages results
# on Supabase; we strip these URLs at adapter return time.
_TRANSIENT_HOSTS: Final[tuple[str, ...]] = ("supabase.co",)


def _is_transient_url(url: str | None) -> bool:
    return bool(url) and any(h in url for h in _TRANSIENT_HOSTS)


def _redact(url: str | None) -> str:
    """Mask a transient (supabase) URL for log-safe display.

    Returns ``"<phaya-transient:abcd…wxyz>"`` instead of the raw URL so
    ADR-006 'never logged' is upheld even if a caller accidentally prints
    the adapter's internal state.
    """
    if not url:
        return "<none>"
    if not _is_transient_url(url):
        return url  # gs:// URIs and our own CDN URLs are safe to log
    # Last 4 chars of path give enough uniqueness to correlate in logs
    # without leaking the public-bucket path.
    suffix = url.rstrip("/").split("/")[-1][:8]
    return f"<phaya-transient:{suffix}>"


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
        gcs: "GcsStorage | None" = None,
        gcs_key_prefix: str = "phaya",
    ) -> None:
        """Construct a Phaya REST client.

        When ``gcs`` is provided, completed-job result URLs are
        auto-republished to GCS per ADR-006 — callers receive ``gs://``
        URIs and the transient Supabase URLs never leave this client.
        When ``gcs`` is ``None``, the legacy passthrough behavior is
        preserved (callers get the supabase URL — use only for testing).
        """
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
        self._gcs = gcs
        self._gcs_key_prefix = gcs_key_prefix.strip("/")

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
                cost_thb=float(payload.get("credits_used") or 0.0),
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
                cost_thb=float(payload.get("credits_used") or 0.0),
            )

        return await call_with_result(_go, cost_fn=lambda r: r.cost_usd)

    # ---- Sora 2 Text-to-Video (async job) ----------------------------- #

    async def create_sora2_video(
        self,
        prompt: str,
        *,
        aspect_ratio: str = "portrait",
        n_frames: str = "15",
        remove_watermark: bool = True,
    ) -> ToolResult[JobHandle]:
        """Submit a Sora 2 T2V job. Poll via :meth:`wait_for_sora2`.

        Phaya constraints (from openapi.json, May 2026):
        - ``aspect_ratio``: ``"landscape"`` (16:9) or ``"portrait"`` (9:16). Default ``portrait`` for Auto-Affi's Reels format.
        - ``n_frames``: literal string ``"10"`` or ``"15"`` (only 2 valid values).
          Clips are short by design — stitch multiple for longer scenes.
        - ``prompt``: 1-2000 chars.
        """
        if aspect_ratio not in ("landscape", "portrait"):
            raise AdapterError(
                f"Phaya Sora 2: aspect_ratio must be 'landscape' or 'portrait', got {aspect_ratio!r}"
            )
        if n_frames not in ("10", "15"):
            raise AdapterError(
                f"Phaya Sora 2: n_frames must be '10' or '15', got {n_frames!r}"
            )

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
                cost_thb=float(payload.get("credits_used") or 0.0),
            )

        return await call_with_result(_go, cost_fn=lambda h: h.cost_usd)

    async def get_sora2_status(self, job_id: str) -> ToolResult[JobHandle]:
        return await self._get_status(
            f"/api/v1/sora2-text-to-video/status/{job_id}",
            job_id=job_id,
            kind="sora2",
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
            f"/api/v1/text-to-speech/status/{job_id}",
            job_id=job_id,
            kind="tts",
        )

    # ---- Image generation: Nano Banana 2 (async job) ------------------ #

    async def create_nano_banana_image(
        self,
        prompt: str,
        *,
        aspect_ratio: str = "9:16",
        resolution: str = "1K",
        output_format: str = "jpg",
        image_input: list[str] | None = None,
    ) -> ToolResult[JobHandle]:
        """Submit a Nano Banana 2 image generation job.

        Aspect ratios (verified from openapi): 1:1, 1:4, 1:8, 2:3, 3:2,
        3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9, auto.
        Resolutions: 1K, 2K, 4K. Defaults pick 9:16 + 1K for Reels-grade
        reference images (~2 credits ≈ ฿0.03).
        """
        if aspect_ratio not in {
            "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3",
            "4:5", "5:4", "8:1", "9:16", "16:9", "21:9", "auto",
        }:
            raise AdapterError(
                f"Phaya nano-banana: aspect_ratio {aspect_ratio!r} not in supported enum"
            )
        if resolution not in ("1K", "2K", "4K"):
            raise AdapterError(
                f"Phaya nano-banana: resolution must be 1K/2K/4K, got {resolution!r}"
            )

        async def _go() -> JobHandle:
            body: dict[str, Any] = {
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "resolution": resolution,
                "output_format": output_format,
            }
            if image_input:
                body["image_input"] = image_input
            payload = await self._http.post(
                url=f"{self._base_url}/api/v1/nano-banana/create",
                body=body,
                headers=self._headers(),
            )
            return JobHandle(
                job_id=str(payload.get("job_id") or payload.get("id", "")),
                state=_coerce_state(str(payload.get("status") or payload.get("state", "queued"))),
                cost_thb=float(payload.get("credits_used") or 0.0),
            )

        return await call_with_result(_go, cost_fn=lambda h: h.cost_usd)

    async def get_nano_banana_status(self, job_id: str) -> ToolResult[JobHandle]:
        return await self._get_status(
            f"/api/v1/nano-banana/status/{job_id}",
            job_id=job_id,
            kind="nano-banana",
        )

    async def wait_for_nano_banana(
        self, job_id: str, *, poll_interval_s: float = 3.0, timeout_s: float = 180.0
    ) -> ToolResult[JobHandle]:
        return await self._wait(
            poller=self.get_nano_banana_status,
            job_id=job_id,
            interval=poll_interval_s,
            timeout=timeout_s,
        )

    # ---- Image-to-Video (async job) ----------------------------------- #

    async def create_image_to_video(
        self,
        image_url: str,
        *,
        duration_s: int = 5,
        image_format: str = "auto",
        music_url: str | None = None,
    ) -> ToolResult[JobHandle]:
        """Submit an image-to-video job. Animates a still image.

        Duration in whole seconds (default 5). Music optional; if omitted,
        the i2v output is silent and we layer Phaya TTS on top later.
        """
        if image_format not in ("auto", "jpeg", "png", "gif", "webp"):
            raise AdapterError(
                f"Phaya i2v: image_format {image_format!r} not in supported enum"
            )

        async def _go() -> JobHandle:
            body: dict[str, Any] = {
                "image_url": image_url,
                "duration": duration_s,
                "image_format": image_format,
            }
            if music_url:
                body["music_url"] = music_url
            payload = await self._http.post(
                url=f"{self._base_url}/api/v1/image-to-video/create",
                body=body,
                headers=self._headers(),
            )
            return JobHandle(
                job_id=str(payload.get("job_id") or payload.get("id", "")),
                state=_coerce_state(str(payload.get("status") or payload.get("state", "queued"))),
                cost_thb=float(payload.get("credits_used") or 0.0),
            )

        return await call_with_result(_go, cost_fn=lambda h: h.cost_usd)

    async def get_image_to_video_status(self, job_id: str) -> ToolResult[JobHandle]:
        return await self._get_status(
            f"/api/v1/image-to-video/status/{job_id}",
            job_id=job_id,
            kind="i2v",
        )

    async def wait_for_image_to_video(
        self, job_id: str, *, poll_interval_s: float = 5.0, timeout_s: float = 420.0
    ) -> ToolResult[JobHandle]:
        return await self._wait(
            poller=self.get_image_to_video_status,
            job_id=job_id,
            interval=poll_interval_s,
            timeout=timeout_s,
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
                cost_thb=float(payload.get("credits_used") or 0.0),
            )

        return await call_with_result(_go, cost_fn=lambda h: h.cost_usd)

    async def get_music_status(self, job_id: str) -> ToolResult[JobHandle]:
        return await self._get_status(
            f"/api/v1/text-to-music/status/{job_id}",
            job_id=job_id,
            kind="music",
        )

    # ---- Internal: status GET + polling helpers ----------------------- #

    async def _republish_to_gcs(
        self, supabase_url: str, *, job_id: str, kind: str
    ) -> str:
        """Download a transient Supabase URL → upload to GCS → return gs:// URI.

        ADR-006 enforcement boundary. The supabase URL is held only as a
        transient local variable inside this method; the caller never sees it.
        """
        if self._gcs is None:
            raise AdapterError("Phaya: GCS not configured but republish requested")
        # Pick a content-type + extension based on the kind tag.
        ext_ct = {
            "sora2": ("mp4", "video/mp4"),
            "i2v": ("mp4", "video/mp4"),
            "tts": ("wav", "audio/wav"),
            "nano-banana": ("jpg", "image/jpeg"),
            "music": ("mp3", "audio/mpeg"),
        }
        ext, content_type = ext_ct.get(kind, ("bin", "application/octet-stream"))
        # Download bytes (transient — never returned). Reuse the injected
        # test transport when present so MockTransport-based tests can stub
        # the download. In production we open a fresh follow-redirects client.
        if self._http.client is not None:
            r = await self._http.client.get(supabase_url)
            r.raise_for_status()
            data = r.content
        else:
            async with httpx.AsyncClient(timeout=180.0, follow_redirects=True) as c:
                r = await c.get(supabase_url)
                r.raise_for_status()
                data = r.content
        key = f"{self._gcs_key_prefix}/{kind}/{job_id}.{ext}"
        # GCS SDK is sync — run in default thread executor
        stored = await asyncio.to_thread(
            self._gcs.upload_bytes, data, key=key, content_type=content_type
        )
        return stored.gs_uri

    async def _get_status(
        self, path: str, *, job_id: str, kind: str | None = None
    ) -> ToolResult[JobHandle]:
        """Per-capability status poller. Phaya field names vary by endpoint:
        - Sora 2 T2V uses ``status`` + ``video_url``
        - TTS uses ``status`` + ``audio_url``
        - Some others use ``state`` + ``result_url`` / ``output_url``
        We accept all four URL field names and both status keys.

        When ``self._gcs`` is set AND the job is COMPLETED with a transient
        URL, the URL is downloaded + republished to GCS atomically; the
        returned ``result_url`` is the ``gs://`` URI. Supabase URLs never
        leave this method (ADR-006).
        """

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
            raw_state = (
                payload.get("status")
                or payload.get("state")
                or "processing"
            )
            raw_url = (
                payload.get("video_url")
                or payload.get("audio_url")
                or payload.get("image_url")
                or payload.get("result_url")
                or payload.get("output_url")
            )
            state = _coerce_state(str(raw_state))
            # Republish per ADR-006 if completed + GCS configured + URL is transient
            final_url = raw_url
            if (
                state is JobState.COMPLETED
                and self._gcs is not None
                and _is_transient_url(raw_url)
                and kind is not None
            ):
                final_url = await self._republish_to_gcs(
                    raw_url, job_id=job_id, kind=kind
                )
            return JobHandle(
                job_id=job_id,
                state=state,
                result_url=final_url,
                error=payload.get("error") or payload.get("message"),
                cost_thb=float(payload.get("credits_used") or 0.0),
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
        # Phaya Sora 2 only accepts n_frames="10" or "15". Pick "15" (longer).
        # Multi-clip stitching for scenes > clip length is the Producer's job.
        create = await self.client.create_sora2_video(
            prompt=scene.visual_prompt, n_frames="15", aspect_ratio="portrait"
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
