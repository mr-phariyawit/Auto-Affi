"""TTS provider adapter with ElevenLabs primary + espeak-ng fallback.

Implements FR-VD-05: TTS whitelist enforcement.

Approved providers: ElevenLabs, Botnoi, Azure.
Explicitly BANNED: OpenAI TTS (per spec).

Phase 1:
  - ElevenLabs Multilingual v2 via REST API (primary)
  - espeak-ng local (fallback — already used by local_renderer)
  - Provider validation at construction time

Phase 2 additions:
  - Botnoi Voice API (regional Thai accents)
  - Azure Cognitive Services TTS
"""

from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Final, Protocol

import httpx
from pydantic import BaseModel, Field, SecretStr

from auto_affi.adapters._http_base import HttpExecutor, call_with_result
from auto_affi.exceptions import AdapterError
from auto_affi.schemas.tool_result import ToolResult


class TTSProvider(StrEnum):
    """Approved TTS providers."""

    ELEVENLABS = "elevenlabs"
    BOTNOI = "botnoi"
    AZURE = "azure"
    ESPEAK = "espeak"  # Local fallback only


# Hard-banned providers — raise at construction if selected.
_BANNED_PROVIDERS: Final[frozenset[str]] = frozenset({"openai", "openai_tts"})


@dataclass(frozen=True)
class TTSResult:
    """Result of a TTS synthesis call."""

    audio_path: Path
    provider: TTSProvider
    duration_s: float
    cost_usd: float


class TTSAdapter(Protocol):
    """Protocol for TTS adapters."""

    async def synthesize(
        self, text_th: str, *, output_path: Path
    ) -> ToolResult[TTSResult]: ...

    @property
    def provider(self) -> TTSProvider: ...


def validate_provider(provider: str) -> TTSProvider:
    """Validate a provider string against the whitelist.

    Raises :class:`AdapterError` for banned or unknown providers.
    """
    normalized = provider.lower().strip()
    if normalized in _BANNED_PROVIDERS:
        raise AdapterError(
            f"TTS provider '{provider}' is BANNED. "
            "Use ElevenLabs (primary), Botnoi, or Azure. See FR-VD-05."
        )
    try:
        return TTSProvider(normalized)
    except ValueError:
        raise AdapterError(
            f"Unknown TTS provider '{provider}'. "
            f"Approved: {', '.join(p.value for p in TTSProvider)}"
        )


# --------------------------------------------------------------------- #
# ElevenLabs adapter                                                    #
# --------------------------------------------------------------------- #

_ELEVENLABS_BASE = "https://api.elevenlabs.io"
_DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel — good for Thai
_DEFAULT_MODEL = "eleven_multilingual_v2"


class ElevenLabsConfig(BaseModel):
    """Configuration for ElevenLabs TTS."""

    api_key: SecretStr
    voice_id: str = Field(default=_DEFAULT_VOICE_ID, min_length=1)
    model_id: str = Field(default=_DEFAULT_MODEL, min_length=1)
    stability: float = Field(default=0.5, ge=0.0, le=1.0)
    similarity_boost: float = Field(default=0.75, ge=0.0, le=1.0)


class ElevenLabsTTS:
    """ElevenLabs Multilingual v2 adapter — primary TTS for Phase 1."""

    def __init__(
        self,
        config: ElevenLabsConfig,
        *,
        timeout_s: float = 30.0,
        max_retries: int = 3,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not config.api_key.get_secret_value():
            raise AdapterError("ElevenLabs api_key is required")
        self._config = config
        self._executor = HttpExecutor(
            vendor="ElevenLabs",
            timeout_s=timeout_s,
            max_retries=max_retries,
            client=client,
        )

    @property
    def provider(self) -> TTSProvider:
        return TTSProvider.ELEVENLABS

    async def synthesize(
        self, text_th: str, *, output_path: Path
    ) -> ToolResult[TTSResult]:
        """Synthesize Thai text to audio via ElevenLabs API."""
        url = f"{_ELEVENLABS_BASE}/v1/text-to-speech/{self._config.voice_id}"
        headers = {
            "xi-api-key": self._config.api_key.get_secret_value(),
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }
        body = {
            "text": text_th,
            "model_id": self._config.model_id,
            "voice_settings": {
                "stability": self._config.stability,
                "similarity_boost": self._config.similarity_boost,
            },
        }

        async def _do() -> TTSResult:
            # For ElevenLabs we need raw binary response, not JSON.
            # Use the executor's client directly for binary download.
            client = self._executor.client or httpx.AsyncClient(
                timeout=self._executor.timeout_s
            )
            owns_client = self._executor.client is None
            try:
                response = await client.post(url, json=body, headers=headers)
            finally:
                if owns_client:
                    await client.aclose()

            if response.status_code != 200:
                raise AdapterError(
                    f"ElevenLabs HTTP {response.status_code}: {response.text[:200]}"
                )

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(response.content)

            # Estimate duration from file size (MP3 ~128kbps)
            file_size = output_path.stat().st_size
            estimated_duration = file_size / (128_000 / 8)

            # Cost: ElevenLabs charges per character (~$0.30/1k chars for Creator plan)
            cost = len(text_th) * 0.0003

            return TTSResult(
                audio_path=output_path,
                provider=TTSProvider.ELEVENLABS,
                duration_s=estimated_duration,
                cost_usd=cost,
            )

        return await call_with_result(_do)


# --------------------------------------------------------------------- #
# espeak-ng fallback                                                    #
# --------------------------------------------------------------------- #


class EspeakTTS:
    """Local espeak-ng fallback — zero cost, low quality.

    Used for development and CI when no vendor credentials are available.
    Requires ``espeak-ng`` installed with Thai voice.
    """

    @property
    def provider(self) -> TTSProvider:
        return TTSProvider.ESPEAK

    async def synthesize(
        self, text_th: str, *, output_path: Path
    ) -> ToolResult[TTSResult]:
        """Synthesize Thai text via local espeak-ng."""

        async def _do() -> TTSResult:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            wav_path = output_path.with_suffix(".wav")

            try:
                subprocess.run(
                    [
                        "espeak-ng",
                        "-v", "th",
                        "-w", str(wav_path),
                        text_th,
                    ],
                    check=True,
                    capture_output=True,
                    timeout=30,
                )
            except FileNotFoundError:
                raise AdapterError(
                    "espeak-ng not found. Install via: brew install espeak-ng "
                    "or apt-get install espeak-ng"
                )
            except subprocess.CalledProcessError as err:
                raise AdapterError(f"espeak-ng failed: {err.stderr.decode()[:200]}")

            # Convert WAV to MP3 if ffmpeg available, otherwise keep WAV
            if output_path.suffix == ".mp3":
                try:
                    subprocess.run(
                        ["ffmpeg", "-y", "-i", str(wav_path), str(output_path)],
                        check=True,
                        capture_output=True,
                        timeout=30,
                    )
                    wav_path.unlink(missing_ok=True)
                except (FileNotFoundError, subprocess.CalledProcessError):
                    # No ffmpeg — just rename WAV
                    wav_path.rename(output_path)
            else:
                wav_path.rename(output_path)

            # Rough duration estimate: Thai speech ~4 chars/second
            estimated_duration = max(len(text_th) / 4.0, 1.0)

            return TTSResult(
                audio_path=output_path,
                provider=TTSProvider.ESPEAK,
                duration_s=estimated_duration,
                cost_usd=0.0,
            )

        return await call_with_result(_do)
