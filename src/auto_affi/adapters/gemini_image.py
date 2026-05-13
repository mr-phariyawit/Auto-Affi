"""Gemini image-generation adapter — Nano Banana Pro 2 (gemini-3-pro-image-preview).

Drops in alongside ``PhayaClient.create_nano_banana_image`` so the team can
route image generation through Google directly (instead of Phaya gateway)
once Gemini credits are funded.

API endpoint: ``POST /v1beta/models/{model}:generateContent?key=<KEY>``.

Request body shape:
    {
        "contents": [{
            "parts": [
                {"text": "<prompt>"},
                // optional reference images for identity-conditioning:
                {"inline_data": {"mime_type": "image/jpeg", "data": "<base64>"}},
                ...
            ]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "9:16"}
        }
    }

Response has ``candidates[0].content.parts[].inline_data`` carrying the
generated image as base64. Multiple parts may include text commentary;
we filter to image parts only.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import httpx
from pydantic import BaseModel, SecretStr

from auto_affi.exceptions import AdapterError
from auto_affi.schemas.tool_result import ToolResult


# Gemini image model aliases — pinned to the model the user requested.
# `nano-banana-pro-preview` and `gemini-3-pro-image-preview` resolve to the
# same upstream model (Gemini 3 Pro Image Preview); we prefer the named
# alias because "Nano Banana Pro 2" is the human-facing name.
GEMINI_NANO_BANANA_PRO = "nano-banana-pro-preview"
GEMINI_FLASH_3_1_IMAGE = "gemini-3.1-flash-image-preview"
GEMINI_FLASH_2_5_IMAGE = "gemini-2.5-flash-image"

# Aspect ratios Gemini accepts on imageConfig.aspectRatio
_SUPPORTED_ASPECTS = frozenset({"1:1", "9:16", "16:9", "3:4", "4:3", "2:3", "3:2"})


class GeminiImageResult(BaseModel):
    """Result of a Gemini image-generation call."""

    image_bytes: bytes
    mime_type: str = "image/png"
    model: str
    text_commentary: str = ""  # Gemini sometimes includes a short text part
    usage_input_tokens: int = 0
    usage_output_tokens: int = 0

    @property
    def usage_total_tokens(self) -> int:
        return self.usage_input_tokens + self.usage_output_tokens


@dataclass(frozen=True)
class GeminiImageClient:
    """Thin Gemini image-gen client. Synchronous httpx; image-gen is fast
    enough (~3-10s typically) that we don't need polling — the response
    comes back inline.

    For testing, inject an ``httpx.AsyncClient`` (with a ``MockTransport``)
    via ``injected_client``; production uses a fresh client per call.
    """

    api_key: SecretStr
    base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    timeout_s: float = 120.0
    model: str = GEMINI_NANO_BANANA_PRO
    injected_client: httpx.AsyncClient | None = None

    def _url(self, model: str) -> str:
        return f"{self.base_url}/models/{model}:generateContent?key={self.api_key.get_secret_value()}"

    def _encode_reference(self, image: Path | bytes) -> dict[str, Any]:
        """Encode a local file or raw bytes into Gemini's inline_data form."""
        if isinstance(image, Path):
            data = image.read_bytes()
            # Guess mime by extension
            ext = image.suffix.lower().lstrip(".")
            mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                    "png": "image/png", "webp": "image/webp"}.get(ext, "image/jpeg")
        else:
            data = image
            mime = "image/jpeg"  # caller responsibility to ensure
        return {"inline_data": {"mime_type": mime, "data": base64.b64encode(data).decode("ascii")}}

    async def create_image(
        self,
        prompt: str,
        *,
        aspect_ratio: str = "9:16",
        reference_images: list[Path] | None = None,
        model: str | None = None,
    ) -> ToolResult[GeminiImageResult]:
        """Generate an image (optionally conditioned on reference images).

        ``reference_images`` are passed as inline image parts AFTER the
        text prompt — the model uses them for identity / style / composition
        conditioning. Same role as Phaya Nano Banana 2's ``image_input``.
        """
        if aspect_ratio not in _SUPPORTED_ASPECTS:
            return ToolResult(
                ok=False,
                error=f"Gemini: aspect_ratio {aspect_ratio!r} not in {sorted(_SUPPORTED_ASPECTS)}",
                trace_id="",
            )

        used_model = model or self.model
        parts: list[dict[str, Any]] = [{"text": prompt}]
        for ref in (reference_images or []):
            parts.append(self._encode_reference(ref))

        body = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {"aspectRatio": aspect_ratio},
            },
        }

        try:
            if self.injected_client is not None:
                r = await self.injected_client.post(self._url(used_model), json=body)
            else:
                async with httpx.AsyncClient(timeout=self.timeout_s) as c:
                    r = await c.post(self._url(used_model), json=body)
        except httpx.HTTPError as e:
            return ToolResult(ok=False, error=f"Gemini HTTP error: {e}", trace_id="")

        if r.status_code >= 400:
            return ToolResult(
                ok=False,
                error=f"Gemini HTTP {r.status_code}: {r.text[:400]}",
                trace_id="",
            )

        payload = r.json()
        candidates = payload.get("candidates") or []
        if not candidates:
            return ToolResult(ok=False, error="Gemini: no candidates", trace_id="")

        image_bytes: bytes | None = None
        image_mime = "image/png"
        text_commentary = ""
        for part in candidates[0].get("content", {}).get("parts", []):
            if "inline_data" in part:
                data_b64 = part["inline_data"].get("data", "")
                if data_b64:
                    image_bytes = base64.b64decode(data_b64)
                    image_mime = part["inline_data"].get("mime_type", "image/png")
            elif "inlineData" in part:  # SDK-style key
                data_b64 = part["inlineData"].get("data", "")
                if data_b64:
                    image_bytes = base64.b64decode(data_b64)
                    image_mime = part["inlineData"].get("mimeType", "image/png")
            elif "text" in part:
                text_commentary += part["text"]

        if image_bytes is None:
            return ToolResult(
                ok=False,
                error=f"Gemini: no image part in response (got: {payload}[:400])",
                trace_id="",
            )

        usage = payload.get("usageMetadata", {})
        return ToolResult(
            ok=True,
            data=GeminiImageResult(
                image_bytes=image_bytes,
                mime_type=image_mime,
                model=used_model,
                text_commentary=text_commentary.strip(),
                usage_input_tokens=int(usage.get("promptTokenCount", 0)),
                usage_output_tokens=int(usage.get("candidatesTokenCount", 0)),
            ),
            trace_id="",
        )


def write_image_to_path(result: GeminiImageResult, dest: Path) -> Path:
    """Write a GeminiImageResult to disk; returns the path."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(result.image_bytes)
    return dest
