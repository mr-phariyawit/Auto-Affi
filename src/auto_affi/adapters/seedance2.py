"""Seedance 2.0 async client via PiAPI gateway.

Direct alternative to Phaya's `create_seedance_video` (which still
targets Seedance 1.5 Pro). PiAPI exposes ByteDance Seedance 2.0 with
the `first_last_frames` task type for two-keyframe i2v — the same
shape we used with 1.5 Pro, but with +31.7 physics-accuracy points
(Megaton benchmark 73.0 vs 53.0) and Fast tier at $0.08/s ~35%
cheaper than 1.5 Pro at equivalent resolution.

Why this lives outside `phaya.py`:
- Phaya gateway hasn't (as of 2026-05-15) exposed a Seedance 2.0
  endpoint. Building direct keeps us unblocked.
- The PiAPI surface is generic REST (POST submit, GET poll, MP4 URL
  in result) — same async pattern as `src/auto_affi/adapters/heygen.py`,
  no new dependencies, ~100 LOC.

Endpoints (PiAPI v1):
  POST {base}/api/v1/task         — submit
  GET  {base}/api/v1/task/{id}    — poll status + result

Auth:
  X-API-Key: <PIAPI_API_KEY>

Routing for our pipeline:
- Generator.SEEDANCE_2_FAST — seedance-2-fast model, default tier
- Generator.SEEDANCE_2_PRO  — seedance-2 model (full quality)

Reference:
- https://piapi.ai/seedance-2-0
- .aegis/brain/learnings/2026-05-15-higgsfield-seedance2-stack-routing.md
"""

from __future__ import annotations

import asyncio
import dataclasses
import time
from pathlib import Path
from typing import Literal

import httpx
from pydantic import SecretStr


PIAPI_API_BASE = "https://api.piapi.ai"


class Seedance2Error(RuntimeError):
    """Raised on non-2xx responses or terminal failure states from PiAPI."""


@dataclasses.dataclass(frozen=True)
class Seedance2Job:
    task_id: str
    status: str  # "Pending" | "Processing" | "Completed" | "Failed"


@dataclasses.dataclass(frozen=True)
class Seedance2Result:
    task_id: str
    video_url: str
    duration_s: float | None


class Seedance2Client:
    """Thin async client around PiAPI's Seedance 2.0 endpoints."""

    def __init__(
        self,
        *,
        api_key: SecretStr,
        timeout_s: float = 120.0,
        base_url: str = PIAPI_API_BASE,
    ) -> None:
        self._api_key = api_key
        self._timeout = httpx.Timeout(timeout_s)
        self._base_url = base_url.rstrip("/")

    def _headers(self) -> dict[str, str]:
        return {
            "X-API-Key": self._api_key.get_secret_value(),
            "Content-Type": "application/json",
        }

    async def create_first_last_frames(
        self,
        *,
        first_frame_url: str,
        last_frame_url: str,
        prompt: str,
        model: Literal["seedance-2-fast", "seedance-2"] = "seedance-2-fast",
        duration_s: int = 4,
        resolution: Literal["480p", "720p", "1080p"] = "720p",
        aspect_ratio: Literal["9:16", "16:9", "1:1"] = "9:16",
    ) -> Seedance2Job:
        """Submit a two-keyframe Seedance 2.0 generation job.

        Args:
            first_frame_url: publicly-accessible URL for the start frame
                (typically a GCS signed URL).
            last_frame_url:  publicly-accessible URL for the end frame.
            prompt:          motion description (60-100 words, one action
                verb per shot per Seedance 2.0 prompt guide).
            model:           seedance-2-fast ($0.08/s) or seedance-2
                ($0.10/s, full quality).
            duration_s:      4-12s typical (Seedance 2.0 supports up to
                15s but 4-8s is the sweet spot for affiliate transitions).
            resolution:      480p (cheapest) / 720p (recommended) / 1080p.
            aspect_ratio:    9:16 vertical for our use case.
        """
        body = {
            "model": model,
            "task_type": "first_last_frames",
            "input": {
                "first_frame_url": first_frame_url,
                "last_frame_url": last_frame_url,
                "prompt": prompt,
                "duration": str(duration_s),
                "aspect_ratio": aspect_ratio,
                "resolution": resolution,
            },
        }
        async with httpx.AsyncClient(timeout=self._timeout) as c:
            r = await c.post(
                f"{self._base_url}/api/v1/task",
                headers=self._headers(), json=body,
            )
        if r.status_code >= 400:
            raise Seedance2Error(
                f"create_first_last_frames → HTTP {r.status_code}: {r.text[:500]}"
            )
        data = r.json().get("data") or r.json()
        return Seedance2Job(
            task_id=data["task_id"],
            status=data.get("status", "Pending"),
        )

    async def get_task(self, task_id: str) -> dict:
        async with httpx.AsyncClient(timeout=self._timeout) as c:
            r = await c.get(
                f"{self._base_url}/api/v1/task/{task_id}",
                headers=self._headers(),
            )
        if r.status_code >= 400:
            raise Seedance2Error(
                f"get_task({task_id}) → HTTP {r.status_code}: {r.text[:400]}"
            )
        return r.json().get("data") or r.json()

    async def wait_for_task(
        self,
        task_id: str,
        *,
        interval_s: float = 4.0,
        timeout_s: float = 600.0,
    ) -> Seedance2Result:
        """Poll until status terminal. Returns the video URL.

        PiAPI's terminal states (observed): "Completed", "Failed",
        "Success". We accept both case variants.
        """
        deadline = time.monotonic() + timeout_s
        last_status = "unknown"
        while time.monotonic() < deadline:
            data = await self.get_task(task_id)
            status = (data.get("status") or "unknown").lower()
            if status != last_status:
                print(f"  ⏳ seedance2 {task_id}: {status}")
                last_status = status
            if status in ("completed", "succeeded", "success"):
                output = data.get("output") or {}
                video_url = (
                    output.get("video_url")
                    or output.get("url")
                    or data.get("video_url")
                )
                if not video_url:
                    raise Seedance2Error(
                        f"completed but no video_url in response: {data}"
                    )
                return Seedance2Result(
                    task_id=task_id,
                    video_url=video_url,
                    duration_s=output.get("duration"),
                )
            if status in ("failed", "error"):
                err = data.get("error") or output.get("error")
                raise Seedance2Error(f"seedance2 task failed: {err or data}")
            await asyncio.sleep(interval_s)
        raise Seedance2Error(
            f"seedance2 polling timed out after {timeout_s}s (last={last_status})"
        )

    async def download_video(self, url: str, dest: Path) -> Path:
        """Stream the rendered mp4 to disk."""
        async with httpx.AsyncClient(timeout=self._timeout) as c:
            r = await c.get(url)
        if r.status_code >= 400:
            raise Seedance2Error(f"download_video {url} → HTTP {r.status_code}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(r.content)
        return dest
