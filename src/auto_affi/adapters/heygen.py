"""HeyGen Avatar IV async client — verified lip-sync from photo + audio.

Avatar IV ("av4") takes ONE photo of a person + ONE audio file and produces
a lip-synced video where the mouth, head, and facial dynamics follow the
audio. Sync-error floor is ~0.02s per practitioner benchmarks — substantially
tighter than what Seedance's --generate-audio produces.

Flow:

  1. ``upload_asset(image_path)``         → returns image_asset_id
  2. ``upload_asset(audio_path)``         → returns audio_asset_id
  3. ``create_video(image_asset_id, audio_asset_id, aspect_ratio, resolution)``
                                          → returns video_id
  4. ``wait_for_video(video_id)``         → polls until status="completed",
                                            returns video_url
  5. ``download_video(url, dest_path)``   → writes local mp4

References:
- https://developers.heygen.com/docs/upload-assets   (v3 assets endpoint)
- https://developers.heygen.com/reference/create-video.md  (v3 video create)
- https://www.heygen.com/blog/announcing-the-avatar-iv-api  (overview)
"""

from __future__ import annotations

import asyncio
import dataclasses
import time
from pathlib import Path
from typing import Literal

import httpx
from pydantic import SecretStr


HEYGEN_API_BASE = "https://api.heygen.com"


class HeyGenError(RuntimeError):
    """Raised on non-2xx responses from the HeyGen API."""


@dataclasses.dataclass(frozen=True)
class UploadedAsset:
    asset_id: str
    url: str
    mime_type: str
    size_bytes: int


@dataclasses.dataclass(frozen=True)
class VideoJob:
    video_id: str
    status: str  # "waiting" | "processing" | "completed" | "failed"
    output_format: str


@dataclasses.dataclass(frozen=True)
class CompletedVideo:
    video_id: str
    video_url: str
    duration_s: float | None
    thumbnail_url: str | None


class HeyGenClient:
    """Thin async client around HeyGen's v3 REST API."""

    def __init__(
        self,
        *,
        api_key: SecretStr,
        timeout_s: float = 120.0,
        base_url: str = HEYGEN_API_BASE,
    ) -> None:
        self._api_key = api_key
        self._timeout = httpx.Timeout(timeout_s)
        self._base_url = base_url.rstrip("/")

    def _headers(self, content_type: str | None = None) -> dict[str, str]:
        h = {"X-Api-Key": self._api_key.get_secret_value()}
        if content_type:
            h["Content-Type"] = content_type
        return h

    async def upload_asset(self, file_path: Path) -> UploadedAsset:
        """POST /v3/assets — multipart upload returning an asset_id usable
        in subsequent video-create calls.

        MIME type is auto-detected from file bytes — no need to set it.
        """
        if not file_path.exists():
            raise HeyGenError(f"asset file not found: {file_path}")
        async with httpx.AsyncClient(timeout=self._timeout) as c:
            with file_path.open("rb") as fh:
                files = {"file": (file_path.name, fh)}
                r = await c.post(
                    f"{self._base_url}/v3/assets",
                    headers=self._headers(),
                    files=files,
                )
        if r.status_code >= 400:
            raise HeyGenError(
                f"upload_asset {file_path.name} → HTTP {r.status_code}: {r.text[:400]}"
            )
        data = r.json().get("data") or r.json()
        return UploadedAsset(
            asset_id=data["asset_id"],
            url=data.get("url", ""),
            mime_type=data.get("mime_type", ""),
            size_bytes=int(data.get("size_bytes", 0)),
        )

    async def create_video_from_image(
        self,
        *,
        image_asset_id: str,
        audio_asset_id: str | None = None,
        audio_url: str | None = None,
        aspect_ratio: Literal["16:9", "9:16"] = "9:16",
        resolution: Literal["720p", "1080p", "4k"] = "1080p",
        motion_prompt: str | None = None,
        expressiveness: Literal["low", "medium", "high"] | None = None,
    ) -> VideoJob:
        """POST /v3/videos with ``type="image"`` — talking-photo with the
        provided audio driving the lip-sync. Exactly one of
        ``audio_asset_id`` / ``audio_url`` must be set."""
        if (audio_asset_id is None) == (audio_url is None):
            raise HeyGenError(
                "create_video_from_image requires exactly one of "
                "audio_asset_id or audio_url"
            )
        # HeyGen v3 nests the image source in a typed object — `image` is
        # NOT a top-level asset_id string. Audio still uses the flat
        # audio_asset_id / audio_url fields per their convention.
        body: dict[str, object] = {
            "type": "image",
            "image": {"type": "asset_id", "asset_id": image_asset_id},
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        }
        if audio_asset_id is not None:
            body["audio_asset_id"] = audio_asset_id
        else:
            body["audio_url"] = audio_url
        if motion_prompt:
            body["motion_prompt"] = motion_prompt
        if expressiveness:
            body["expressiveness"] = expressiveness

        async with httpx.AsyncClient(timeout=self._timeout) as c:
            r = await c.post(
                f"{self._base_url}/v3/videos",
                headers=self._headers("application/json"),
                json=body,
            )
        if r.status_code >= 400:
            raise HeyGenError(
                f"create_video → HTTP {r.status_code}: {r.text[:600]}"
            )
        data = r.json().get("data") or r.json()
        return VideoJob(
            video_id=data["video_id"],
            status=data.get("status", "waiting"),
            output_format=data.get("output_format", "mp4"),
        )

    async def get_video_status(self, video_id: str) -> dict:
        """GET /v3/videos/{video_id} — returns the raw v3 status payload."""
        async with httpx.AsyncClient(timeout=self._timeout) as c:
            r = await c.get(
                f"{self._base_url}/v3/videos/{video_id}",
                headers=self._headers(),
            )
        if r.status_code >= 400:
            raise HeyGenError(
                f"get_video_status({video_id}) → HTTP {r.status_code}: {r.text[:400]}"
            )
        return r.json().get("data") or r.json()

    async def wait_for_video(
        self,
        video_id: str,
        *,
        interval_s: float = 4.0,
        timeout_s: float = 600.0,
    ) -> CompletedVideo:
        """Poll ``get_video_status`` until ``status="completed"`` or
        ``status="failed"`` / timeout."""
        deadline = time.monotonic() + timeout_s
        last_status = "unknown"
        while time.monotonic() < deadline:
            data = await self.get_video_status(video_id)
            status = data.get("status", "unknown").lower()
            if status != last_status:
                print(f"  ⏳ heygen {video_id}: {status}")
                last_status = status
            if status in ("completed", "succeeded", "success"):
                video_url = (
                    data.get("video_url")
                    or data.get("video_url_caption")
                    or (data.get("output", {}) or {}).get("url")
                )
                if not video_url:
                    raise HeyGenError(
                        f"completed but no video_url in response: {data}"
                    )
                return CompletedVideo(
                    video_id=video_id,
                    video_url=video_url,
                    duration_s=data.get("duration"),
                    thumbnail_url=data.get("thumbnail_url"),
                )
            if status in ("failed", "error"):
                raise HeyGenError(
                    f"heygen render failed: {data.get('error') or data}"
                )
            await asyncio.sleep(interval_s)
        raise HeyGenError(
            f"heygen polling timed out after {timeout_s}s (last status={last_status})"
        )

    async def download_video(self, url: str, dest: Path) -> Path:
        """Stream the rendered mp4 to disk."""
        async with httpx.AsyncClient(timeout=self._timeout) as c:
            r = await c.get(url)
        if r.status_code >= 400:
            raise HeyGenError(
                f"download_video {url} → HTTP {r.status_code}"
            )
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(r.content)
        return dest
