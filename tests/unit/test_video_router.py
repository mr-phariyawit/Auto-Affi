"""Tests for the multi-vendor video router (AFFI-T-040)."""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_affi.adapters.video_gen import GeneratedAsset, VideoGenerator
from auto_affi.pipeline.video_router import VideoRouter
from auto_affi.schemas.storyboard import Scene, ScenePurpose
from auto_affi.schemas.tool_result import ToolResult


# ------------------------------------------------------------------ #
# Mock generator                                                       #
# ------------------------------------------------------------------ #

class MockGenerator:
    def __init__(self, name: str, *, fail: bool = False) -> None:
        self._name = name
        self._fail = fail
        self.call_count = 0

    async def generate_scene(
        self, scene: Scene, *, output_dir: Path
    ) -> ToolResult[GeneratedAsset]:
        self.call_count += 1
        if self._fail:
            return ToolResult(ok=False, error=f"{self._name} failed")
        return ToolResult(
            ok=True,
            data=GeneratedAsset(
                scene_idx=scene.idx,
                asset_path=output_dir / f"scene_{scene.idx}_{self._name}.mp4",
                generator=VideoGenerator.SORA2,
                duration_s=scene.duration_s,
                cost_usd=0.50,
            ),
        )


def _make_scene(idx: int = 0, generator: str = "sora2") -> Scene:
    return Scene(
        idx=idx,
        duration_s=2.0,
        purpose=ScenePurpose.DEMONSTRATE,
        shot_type="medium-shot",
        visual_prompt="test scene prompt for video generation",
        generator=generator,
    )


# ------------------------------------------------------------------ #
# Tests                                                                #
# ------------------------------------------------------------------ #


class TestVideoRouter:
    """Multi-vendor video generation routing."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_route_to_registered_generator(self) -> None:
        router = VideoRouter()
        mock = MockGenerator("sora2")
        router.register("sora2", mock)
        result = await router.route(_make_scene(), output_dir=Path("/tmp"))
        assert result.ok
        assert mock.call_count == 1

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_fallback_on_unregistered_generator(self) -> None:
        router = VideoRouter()
        fallback = MockGenerator("fallback")
        router.fallback = fallback
        # Use "kling" which is a valid Literal but not registered in the router
        result = await router.route(
            _make_scene(generator="kling"), output_dir=Path("/tmp")
        )
        assert result.ok
        assert fallback.call_count == 1

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_fallback_on_primary_failure(self) -> None:
        router = VideoRouter()
        primary = MockGenerator("sora2", fail=True)
        fallback = MockGenerator("fallback")
        router.register("sora2", primary)
        router.fallback = fallback
        result = await router.route(_make_scene(), output_dir=Path("/tmp"))
        assert result.ok
        assert primary.call_count == 1
        assert fallback.call_count == 1

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_no_generator_no_fallback_error(self) -> None:
        router = VideoRouter()
        # sora2 is valid but not registered, and no fallback
        result = await router.route(_make_scene(generator="hailuo"), output_dir=Path("/tmp"))
        assert not result.ok
        assert "No generator" in (result.error or "")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_route_all_sequential(self) -> None:
        router = VideoRouter()
        mock = MockGenerator("sora2")
        router.register("sora2", mock)
        scenes = [_make_scene(i) for i in range(3)]
        results = await router.route_all(scenes, output_dir=Path("/tmp"))
        assert len(results) == 3
        assert all(r.ok for r in results)
        assert mock.call_count == 3

    @pytest.mark.unit
    def test_available_generators(self) -> None:
        router = VideoRouter()
        router.register("sora2", MockGenerator("sora2"))
        router.register("flux", MockGenerator("flux"))
        assert set(router.available_generators) == {"sora2", "flux"}
