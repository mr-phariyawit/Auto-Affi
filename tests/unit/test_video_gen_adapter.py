"""Unit tests for the video generation adapter interface."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import SecretStr

from auto_affi.adapters.video_gen import (
    GeneratedAsset,
    KieConfig,
    KieVideoGen,
    LocalVideoGen,
    VideoGenerator,
    create_video_gen,
)
from auto_affi.exceptions import AdapterError
from auto_affi.schemas.storyboard import Scene, ScenePurpose


def _sample_scene(idx: int = 0) -> Scene:
    return Scene(
        idx=idx,
        duration_s=2.0,
        purpose=ScenePurpose.DEMONSTRATE,
        shot_type="medium-closeup",
        visual_prompt="apply serum on forearm in soft daylight",
        generator="veo3_fast",
    )


@pytest.mark.unit
def test_video_generator_enum_values() -> None:
    assert VideoGenerator.VEO3 == "veo3"
    assert VideoGenerator.LOCAL == "local"
    assert VideoGenerator.FLUX == "flux"


@pytest.mark.unit
def test_kie_config_defaults() -> None:
    config = KieConfig(api_key=SecretStr("test"))
    assert "kie.ai" in config.base_url
    assert config.default_generator == VideoGenerator.VEO3_FAST


@pytest.mark.unit
def test_kie_requires_api_key() -> None:
    config = KieConfig(api_key=SecretStr(""))
    with pytest.raises(AdapterError, match="api_key is required"):
        KieVideoGen(config)


@pytest.mark.unit
def test_kie_provider_property() -> None:
    config = KieConfig(api_key=SecretStr("test"))
    adapter = KieVideoGen(config)
    assert adapter.generator == VideoGenerator.VEO3_FAST


@pytest.mark.unit
async def test_local_video_gen_produces_placeholder(tmp_path: Path) -> None:
    adapter = LocalVideoGen()
    scene = _sample_scene()
    result = await adapter.generate_scene(scene, output_dir=tmp_path)

    assert result.ok is True
    assert result.data is not None
    assert result.data.generator == VideoGenerator.LOCAL
    assert result.data.cost_usd == 0.0
    assert result.data.duration_s == scene.duration_s
    assert result.data.asset_path.exists()


@pytest.mark.unit
async def test_local_video_gen_multiple_scenes(tmp_path: Path) -> None:
    adapter = LocalVideoGen()
    results = []
    for i in range(3):
        r = await adapter.generate_scene(_sample_scene(idx=i), output_dir=tmp_path)
        results.append(r)

    assert all(r.ok for r in results)
    assert len(set(r.data.asset_path for r in results if r.data)) == 3


@pytest.mark.unit
def test_local_generator_property() -> None:
    adapter = LocalVideoGen()
    assert adapter.generator == VideoGenerator.LOCAL


@pytest.mark.unit
def test_create_video_gen_local() -> None:
    adapter = create_video_gen(provider="local")
    assert adapter.generator == VideoGenerator.LOCAL


@pytest.mark.unit
def test_create_video_gen_kie_requires_config() -> None:
    with pytest.raises(AdapterError, match="KieConfig required"):
        create_video_gen(provider="kie")


@pytest.mark.unit
def test_create_video_gen_kie_with_config() -> None:
    config = KieConfig(api_key=SecretStr("test"))
    adapter = create_video_gen(provider="kie", config=config)
    assert adapter.generator == VideoGenerator.VEO3_FAST


@pytest.mark.unit
def test_create_video_gen_unknown() -> None:
    with pytest.raises(AdapterError, match="Unknown video gen provider"):
        create_video_gen(provider="nonexistent")


@pytest.mark.unit
def test_generated_asset_defaults() -> None:
    asset = GeneratedAsset(
        scene_idx=0,
        asset_path=Path("/tmp/test.mp4"),
        generator=VideoGenerator.VEO3,
        duration_s=3.0,
        cost_usd=0.08,
    )
    assert asset.width == 1080
    assert asset.height == 1920
