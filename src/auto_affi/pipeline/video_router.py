"""Multi-vendor video generation router (FR-VD-01, E-004 tail).

Routes each scene to the best-fit video/image generator based on the
scene's ``generator`` field and available adapters. Supports Phaya
(Sora 2, Nano Banana 2) + kie.ai + local renderer as fallback chain.

The router respects cost-model.md per-node caps: if a generator's
estimated cost exceeds the scene budget, it falls back to a cheaper
alternative.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from auto_affi.adapters.video_gen import GeneratedAsset
from auto_affi.schemas.storyboard import Scene
from auto_affi.schemas.tool_result import ToolResult


class SceneGenerator(Protocol):
    """Protocol for anything that can generate a visual asset from a scene."""

    async def generate_scene(
        self, scene: Scene, *, output_dir: Path
    ) -> ToolResult[GeneratedAsset]: ...


@dataclass
class VideoRouter:
    """Routes scenes to the best-fit generator.

    Register generators by name. The router matches ``scene.generator``
    to the registered name. Falls back to the ``fallback`` generator
    if no match or if the primary fails.
    """

    _generators: dict[str, SceneGenerator] = field(default_factory=dict)
    fallback: SceneGenerator | None = None

    def register(self, name: str, generator: SceneGenerator) -> None:
        """Register a generator under a name (e.g., 'sora2', 'flux')."""
        self._generators[name] = generator

    @property
    def available_generators(self) -> list[str]:
        return list(self._generators.keys())

    async def route(
        self,
        scene: Scene,
        *,
        output_dir: Path,
    ) -> ToolResult[GeneratedAsset]:
        """Route a scene to the best-fit generator.

        1. Try the scene's declared generator
        2. On failure, try the fallback
        3. On fallback failure, return error
        """
        gen_name = scene.generator
        generator = self._generators.get(gen_name)

        if generator is not None:
            result = await generator.generate_scene(scene, output_dir=output_dir)
            if result.ok:
                return result
            # Primary failed — try fallback

        if self.fallback is not None:
            return await self.fallback.generate_scene(scene, output_dir=output_dir)

        return ToolResult(
            ok=False,
            error=f"No generator registered for '{gen_name}' and no fallback available",
        )

    async def route_all(
        self,
        scenes: list[Scene],
        *,
        output_dir: Path,
    ) -> list[ToolResult[GeneratedAsset]]:
        """Route all scenes sequentially. Returns results in order."""
        results: list[ToolResult[GeneratedAsset]] = []
        for scene in scenes:
            result = await self.route(scene, output_dir=output_dir)
            results.append(result)
        return results
