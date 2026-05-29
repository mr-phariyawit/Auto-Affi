"""Gemini Veo 3.1 video adapter — keyframe video with native lip-synced dialogue.

Veo 3.1 (and Veo 3.1 Fast / Lite) are Google's premium video models with:
- First-and-last frame keyframe support (image-conditioned at both ends)
- Native multilingual dialogue with automatic lip-sync
- High-fidelity video output (up to 1080p)

API contract: ``predictLongRunning`` — submit, get an operation name, poll
``operations/<name>`` until done, fetch the resulting video bytes. Different
from Gemini's regular ``generateContent`` (synchronous).

The dialogue trick (per Veo docs): include the line you want the character
to say INSIDE QUOTES in the prompt. Veo handles language detection,
accent, and lip-sync automatically. Example:

    prompt = (
        "A Thai father reads a bedtime story to his daughter from a printed "
        "page in his hotel room. He says \"จันทร์เจ้าขา ขอข้าวขอแกง\" in a "
        "soft, tender, bedtime cadence."
    )
"""

from __future__ import annotations

import asyncio
import base64
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import httpx
from pydantic import BaseModel, SecretStr

from auto_affi.schemas.tool_result import ToolResult


VEO_3_1 = "veo-3.1-generate-preview"
VEO_3_1_FAST = "veo-3.1-fast-generate-preview"
VEO_3_1_LITE = "veo-3.1-lite-generate-preview"
VEO_3_0 = "veo-3.0-generate-001"
VEO_3_0_FAST = "veo-3.0-fast-generate-001"

_SUPPORTED_ASPECTS = frozenset({"16:9", "9:16"})  # Veo's currently supported set


class VeoVideoResult(BaseModel):
    """Result of a Veo video-generation call."""

    video_bytes: bytes
    mime_type: str = "video/mp4"
    model: str
    operation_name: str
    poll_attempts: int = 0


@dataclass(frozen=True)
class GeminiVeoClient:
    """Veo 3.x async client. Submits and polls predictLongRunning operations.

    Construct once per session; one call ``create_video()`` does the full
    submit + poll + fetch round-trip.
    """

    api_key: SecretStr
    base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    timeout_s: float = 600.0
    poll_interval_s: float = 5.0
    model: str = VEO_3_1
    injected_client: httpx.AsyncClient | None = None

    def _submit_url(self, model: str) -> str:
        return f"{self.base_url}/models/{model}:predictLongRunning?key={self.api_key.get_secret_value()}"

    def _poll_url(self, op_name: str) -> str:
        return f"{self.base_url}/{op_name}?key={self.api_key.get_secret_value()}"

    def _encode_image(self, image: Path) -> dict[str, Any]:
        data = image.read_bytes()
        ext = image.suffix.lower().lstrip(".")
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                "png": "image/png", "webp": "image/webp"}.get(ext, "image/jpeg")
        return {"mimeType": mime, "bytesBase64Encoded": base64.b64encode(data).decode("ascii")}

    async def create_video(
        self,
        prompt: str,
        *,
        first_frame: Path | None = None,
        last_frame: Path | None = None,
        aspect_ratio: str = "9:16",
        duration_seconds: int = 8,
        person_generation: Literal["allow_all", "allow_adult", "dont_allow"] = "allow_all",
        model: str | None = None,
    ) -> ToolResult[VeoVideoResult]:
        """Generate a video. Returns full mp4 bytes inline.

        For two-keyframe mode pass BOTH ``first_frame`` and ``last_frame``
        as local paths; Veo encodes them inline as base64 and interpolates
        the motion between them.

        For dialogue: include the spoken line INSIDE QUOTES in the prompt
        (any language; Veo handles accent + lip-sync automatically).
        """
        if aspect_ratio not in _SUPPORTED_ASPECTS:
            return ToolResult(
                ok=False,
                error=f"Veo: aspect_ratio {aspect_ratio!r} not in {sorted(_SUPPORTED_ASPECTS)}",
                trace_id="",
            )

        used_model = model or self.model
        instance: dict[str, Any] = {"prompt": prompt}
        if first_frame is not None:
            instance["image"] = self._encode_image(first_frame)
        if last_frame is not None:
            instance["lastFrame"] = self._encode_image(last_frame)

        body: dict[str, Any] = {
            "instances": [instance],
            "parameters": {
                "aspectRatio": aspect_ratio,
                "durationSeconds": int(duration_seconds),
                "personGeneration": person_generation,
            },
        }

        # --- Submit ---
        try:
            if self.injected_client is not None:
                r = await self.injected_client.post(self._submit_url(used_model), json=body)
            else:
                async with httpx.AsyncClient(timeout=self.timeout_s) as c:
                    r = await c.post(self._submit_url(used_model), json=body)
        except httpx.HTTPError as e:
            return ToolResult(ok=False, error=f"Veo submit HTTP error: {e}", trace_id="")
        if r.status_code >= 400:
            return ToolResult(
                ok=False,
                error=f"Veo submit HTTP {r.status_code}: {r.text[:400]}",
                trace_id="",
            )
        op_name = r.json().get("name", "")
        if not op_name:
            return ToolResult(ok=False, error=f"Veo submit: no operation name in response: {r.text[:200]}", trace_id="")

        # --- Poll ---
        deadline = time.monotonic() + self.timeout_s
        attempts = 0
        while time.monotonic() < deadline:
            attempts += 1
            try:
                if self.injected_client is not None:
                    pr = await self.injected_client.get(self._poll_url(op_name))
                else:
                    async with httpx.AsyncClient(timeout=60.0) as c:
                        pr = await c.get(self._poll_url(op_name))
            except httpx.HTTPError as e:
                return ToolResult(ok=False, error=f"Veo poll HTTP error: {e}", trace_id="")
            if pr.status_code >= 400:
                return ToolResult(
                    ok=False,
                    error=f"Veo poll HTTP {pr.status_code}: {pr.text[:400]}",
                    trace_id="",
                )
            payload = pr.json()
            if payload.get("done"):
                # Extract video bytes from the response
                resp = payload.get("response", {})
                err = payload.get("error", {})
                if err:
                    return ToolResult(ok=False, error=f"Veo op error: {err}", trace_id="")
                # Veo response shape: generateVideoResponse.generatedSamples[0].video.{uri | bytesBase64Encoded}
                samples = (
                    resp.get("generateVideoResponse", {}).get("generatedSamples", [])
                    or resp.get("predictions", [])
                    or resp.get("generatedSamples", [])
                )
                if not samples:
                    return ToolResult(
                        ok=False,
                        error=f"Veo op done but no samples: {payload}"[:400],
                        trace_id="",
                    )
                video_obj = samples[0].get("video") or samples[0]
                video_bytes: bytes | None = None
                if isinstance(video_obj, dict):
                    if "bytesBase64Encoded" in video_obj:
                        video_bytes = base64.b64decode(video_obj["bytesBase64Encoded"])
                    elif "uri" in video_obj:
                        # Files API URI — needs ?alt=media + auth. The API key
                        # goes via header (x-goog-api-key) to avoid httpx's
                        # query-string re-encoding clobbering alt=media when
                        # the URL also contains an action separator (':download').
                        uri = video_obj["uri"]
                        sep = "&" if "?" in uri else "?"
                        if "alt=media" not in uri:
                            uri = f"{uri}{sep}alt=media"
                        headers = {"x-goog-api-key": self.api_key.get_secret_value()}
                        async with httpx.AsyncClient(timeout=300.0, follow_redirects=True) as c:
                            vr = await c.get(uri, headers=headers)
                            if vr.status_code >= 400:
                                return ToolResult(
                                    ok=False,
                                    error=f"Veo video URI fetch HTTP {vr.status_code} from {uri[:160]}: {vr.text[:200]}",
                                    trace_id="",
                                )
                            video_bytes = vr.content
                if video_bytes is None:
                    return ToolResult(
                        ok=False,
                        error=f"Veo op done but no video bytes/uri: {samples[0]}"[:400],
                        trace_id="",
                    )
                return ToolResult(
                    ok=True,
                    data=VeoVideoResult(
                        video_bytes=video_bytes,
                        model=used_model,
                        operation_name=op_name,
                        poll_attempts=attempts,
                    ),
                    trace_id="",
                )
            await asyncio.sleep(self.poll_interval_s)

        return ToolResult(
            ok=False,
            error=f"Veo poll timed out after {self.timeout_s}s and {attempts} attempts",
            trace_id="",
        )


def write_video_to_path(result: VeoVideoResult, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(result.video_bytes)
    return dest
