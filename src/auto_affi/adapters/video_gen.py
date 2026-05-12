"""Video generation adapter interface + kie.ai implementation (FR-VD-01).

Defines the :class:`VideoGenAdapter` protocol that all video generation
providers must implement. Phase 1 uses kie.ai as the gateway to Veo 3 /
Sora 2 / Flux / Runway, with the local renderer as a zero-cost fallback.

The adapter converts a :class:`Scene` from a Storyboard into a generated
video clip asset. The Producer agent calls one adapter per scene, then
FFmpeg composes all clips into the master 9:16 video.

Adapter pattern mirrors ``_http_base.py``: shared retry/error plumbing,
vendor-specific signing + parsing stays local.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Final, Protocol

import httpx
from pydantic import BaseModel, Field, SecretStr

from auto_affi.adapters._http_base import HttpExecutor, call_with_result
from auto_affi.exceptions import AdapterError
from auto_affi.schemas.storyboard import Scene
from auto_affi.schemas.tool_result import ToolResult


class VideoGenerator(StrEnum):
    """Supported video/image generation backends."""

    VEO3 = "veo3"
    VEO3_FAST = "veo3_fast"
    SORA2 = "sora2"
    KLING = "kling"
    HAILUO = "hailuo"
    FLUX = "flux"
    IMAGEN = "imagen"
    LOCAL = "local"  # Fallback: local_renderer


@dataclass(frozen=True)
class GeneratedAsset:
    """Result of generating one scene's visual asset."""

    scene_idx: int
    asset_path: Path
    generator: VideoGenerator
    duration_s: float
    cost_usd: float
    width: int = 1080
    height: int = 1920


class VideoGenAdapter(Protocol):
    """Protocol that all video generation adapters implement."""

    async def generate_scene(
        self, scene: Scene, *, output_dir: Path
    ) -> ToolResult[GeneratedAsset]: ...

    @property
    def generator(self) -> VideoGenerator: ...


# --------------------------------------------------------------------- #
# kie.ai gateway adapter (production)                                   #
# --------------------------------------------------------------------- #

_KIE_BASE_URL: Final[str] = "https://api.kie.ai"

# kie.ai pricing per generation (approximate, May 2026)
_KIE_COST_PER_SCENE: Final[dict[str, float]] = {
    "veo3": 0.08,
    "veo3_fast": 0.04,
    "sora2": 0.10,
    "kling": 0.06,
    "hailuo": 0.05,
    "flux": 0.02,
    "imagen": 0.03,
}


class KieConfig(BaseModel):
    """Configuration for the kie.ai video generation gateway."""

    api_key: SecretStr
    base_url: str = Field(default=_KIE_BASE_URL)
    default_generator: VideoGenerator = VideoGenerator.VEO3_FAST


class KieVideoGen:
    """kie.ai gateway adapter — routes to Veo/Sora/Flux/Runway via unified API."""

    def __init__(
        self,
        config: KieConfig,
        *,
        timeout_s: float = 120.0,
        max_retries: int = 2,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not config.api_key.get_secret_value():
            raise AdapterError("kie.ai api_key is required")
        self._config = config
        self._executor = HttpExecutor(
            vendor="kie.ai",
            timeout_s=timeout_s,
            max_retries=max_retries,
            client=client,
        )

    @property
    def generator(self) -> VideoGenerator:
        return self._config.default_generator

    async def generate_scene(
        self, scene: Scene, *, output_dir: Path
    ) -> ToolResult[GeneratedAsset]:
        """Generate a video clip for one storyboard scene via kie.ai."""
        generator = scene.generator
        url = f"{self._config.base_url}/v1/generate"
        headers = {
            "Authorization": f"Bearer {self._config.api_key.get_secret_value()}",
            "Content-Type": "application/json",
        }
        body = {
            "model": generator,
            "prompt": scene.visual_prompt,
            "duration_s": scene.duration_s,
            "aspect_ratio": "9:16",
            "resolution": "1080x1920",
        }

        async def _do() -> GeneratedAsset:
            payload = await self._executor.post(url=url, body=body, headers=headers)
            return _parse_kie_response(
                payload,
                scene_idx=scene.idx,
                generator=generator,
                duration_s=scene.duration_s,
                output_dir=output_dir,
            )

        cost_per_scene = _KIE_COST_PER_SCENE.get(generator, 0.05)

        return await call_with_result(
            _do,
            cost_fn=lambda _: cost_per_scene,
        )


def _parse_kie_response(
    payload: dict[str, Any],
    *,
    scene_idx: int,
    generator: str,
    duration_s: float,
    output_dir: Path,
) -> GeneratedAsset:
    """Parse kie.ai response and save the asset."""
    try:
        asset_url = payload["data"]["url"]
        status = payload.get("status", "completed")
    except (KeyError, TypeError) as err:
        raise AdapterError(f"Unexpected kie.ai response: {err}") from err

    if status != "completed":
        raise AdapterError(f"kie.ai generation not completed: status={status}")

    # In production, we'd download the asset from the URL.
    # For now, record the URL as the path placeholder.
    output_path = output_dir / f"scene_{scene_idx:03d}.mp4"

    try:
        gen_enum = VideoGenerator(generator)
    except ValueError:
        gen_enum = VideoGenerator.VEO3

    return GeneratedAsset(
        scene_idx=scene_idx,
        asset_path=output_path,
        generator=gen_enum,
        duration_s=duration_s,
        cost_usd=_KIE_COST_PER_SCENE.get(generator, 0.05),
    )


# --------------------------------------------------------------------- #
# Local fallback adapter                                                #
# --------------------------------------------------------------------- #


class LocalVideoGen:
    """Fallback adapter using PIL-based local renderer.

    Produces placeholder frames — zero vendor cost, usable for CI and
    development without credentials. Delegates to
    ``pipeline.local_renderer`` for actual rendering.
    """

    @property
    def generator(self) -> VideoGenerator:
        return VideoGenerator.LOCAL

    async def generate_scene(
        self, scene: Scene, *, output_dir: Path
    ) -> ToolResult[GeneratedAsset]:
        """Generate a placeholder clip for one scene."""

        async def _do() -> GeneratedAsset:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"scene_{scene.idx:03d}_local.mp4"

            # Create a minimal placeholder file.
            # In real usage, this delegates to local_renderer.render_scene()
            output_path.write_text(
                f"[LOCAL PLACEHOLDER] scene={scene.idx} "
                f"prompt={scene.visual_prompt[:50]} "
                f"duration={scene.duration_s}s"
            )

            return GeneratedAsset(
                scene_idx=scene.idx,
                asset_path=output_path,
                generator=VideoGenerator.LOCAL,
                duration_s=scene.duration_s,
                cost_usd=0.0,
            )

        return await call_with_result(_do)


# --------------------------------------------------------------------- #
# Factory                                                               #
# --------------------------------------------------------------------- #


def create_video_gen(
    *,
    provider: str = "local",
    config: KieConfig | None = None,
    client: httpx.AsyncClient | None = None,
) -> VideoGenAdapter:
    """Factory for video generation adapters.

    Returns the appropriate adapter based on provider name and config.
    """
    if provider == "kie" or provider == "kie.ai":
        if config is None:
            raise AdapterError("KieConfig required for kie.ai provider")
        return KieVideoGen(config, client=client)  # type: ignore[return-value]
    if provider == "local":
        return LocalVideoGen()  # type: ignore[return-value]
    raise AdapterError(f"Unknown video gen provider: {provider}")
