"""Unit tests for Storyboard schema and validators."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from auto_affi.schemas.storyboard import (
    REQUIRED_EDITOR_PASSES,
    Dialogue,
    EditorPass,
    HyperframeOverlay,
    MusicBrief,
    OnScreenText,
    Scene,
    ScenePurpose,
    Storyboard,
    VoiceProfile,
)


def _voice() -> VoiceProfile:
    return VoiceProfile(
        lang="th",
        gender="f",
        tone="energetic-confidant",
        tts_engine="elevenlabs",
        voice_id="voice-th-001",
    )


def _music() -> MusicBrief:
    return MusicBrief(genre="lofi-hype", bpm_range=(90, 110), license="suno")


def _hook() -> Scene:
    return Scene(
        idx=0,
        duration_s=1.5,
        purpose=ScenePurpose.HOOK,
        shot_type="extreme-closeup",
        movement="snap-zoom-in",
        visual_prompt="close-up of glowing skin texture",
        generator="veo3_fast",
        dialogue=Dialogue(speaker="narrator", text_th="POV: คนผิวมัน"),
        on_screen_text=OnScreenText(th="POV", style="bold-pop", position="center-upper"),
    )


def _body_scene(idx: int) -> Scene:
    return Scene(
        idx=idx,
        duration_s=2.0,
        purpose=ScenePurpose.DEMONSTRATE,
        shot_type="medium",
        visual_prompt="product applied to forearm, soft daylight",
        generator="veo3_fast",
    )


def _cta_scene(idx: int) -> Scene:
    return Scene(
        idx=idx,
        duration_s=2.0,
        purpose=ScenePurpose.CTA,
        shot_type="medium",
        visual_prompt="hand pointing to caption area",
        generator="veo3_fast",
    )


def _valid_storyboard() -> Storyboard:
    scenes = [_hook(), _body_scene(1), _body_scene(2), _cta_scene(3)]
    return Storyboard(
        brief_id="brief-001",
        voice_profile=_voice(),
        music_brief=_music(),
        scenes=scenes,
        cta_scene_idx=3,
        affiliate_link_placement="pinned_comment + on_screen_qr",
    )


@pytest.mark.unit
def test_valid_storyboard_round_trips() -> None:
    board = _valid_storyboard()
    assert board.total_duration_s == pytest.approx(7.5)
    assert board.editor_passes == list(REQUIRED_EDITOR_PASSES)


@pytest.mark.unit
def test_hook_must_be_first_scene_purpose() -> None:
    scenes = [_body_scene(0), _body_scene(1), _cta_scene(2)]
    with pytest.raises(ValidationError):
        Storyboard(
            brief_id="b",
            voice_profile=_voice(),
            music_brief=_music(),
            scenes=scenes,
            cta_scene_idx=2,
            affiliate_link_placement="pinned_comment",
        )


@pytest.mark.unit
def test_hook_duration_capped_at_two_seconds() -> None:
    too_long_hook = Scene(
        idx=0,
        duration_s=2.5,
        purpose=ScenePurpose.HOOK,
        shot_type="extreme-closeup",
        visual_prompt="x",
        generator="veo3_fast",
    )
    scenes = [too_long_hook, _body_scene(1), _cta_scene(2)]
    with pytest.raises(ValidationError):
        Storyboard(
            brief_id="b",
            voice_profile=_voice(),
            music_brief=_music(),
            scenes=scenes,
            cta_scene_idx=2,
            affiliate_link_placement="pinned_comment",
        )


@pytest.mark.unit
def test_scene_indices_must_be_contiguous() -> None:
    skipped = Scene(
        idx=5,
        duration_s=2.0,
        purpose=ScenePurpose.DEMONSTRATE,
        shot_type="medium",
        visual_prompt="x",
        generator="veo3_fast",
    )
    scenes = [_hook(), skipped, _cta_scene(2)]
    with pytest.raises(ValidationError):
        Storyboard(
            brief_id="b",
            voice_profile=_voice(),
            music_brief=_music(),
            scenes=scenes,
            cta_scene_idx=2,
            affiliate_link_placement="pinned_comment",
        )


@pytest.mark.unit
def test_total_duration_cap() -> None:
    long_scene = Scene(
        idx=1,
        duration_s=15.0,
        purpose=ScenePurpose.DEMONSTRATE,
        shot_type="wide",
        visual_prompt="long demo",
        generator="veo3",
    )
    scenes = [
        _hook(),
        long_scene,
        long_scene.model_copy(update={"idx": 2}),
        long_scene.model_copy(update={"idx": 3}),
        long_scene.model_copy(update={"idx": 4}),
        _cta_scene(5),
    ]
    with pytest.raises(ValidationError):
        Storyboard(
            brief_id="b",
            voice_profile=_voice(),
            music_brief=_music(),
            scenes=scenes,
            cta_scene_idx=5,
            affiliate_link_placement="pinned_comment",
        )


@pytest.mark.unit
def test_avg_shot_band_enforced() -> None:
    tiny_scenes = [
        _hook(),
        Scene(
            idx=1,
            duration_s=0.5,
            purpose=ScenePurpose.DEMONSTRATE,
            shot_type="m",
            visual_prompt="x",
            generator="veo3_fast",
        ),
        Scene(
            idx=2,
            duration_s=0.5,
            purpose=ScenePurpose.DEMONSTRATE,
            shot_type="m",
            visual_prompt="x",
            generator="veo3_fast",
        ),
        _cta_scene(3).model_copy(update={"duration_s": 0.5}),
    ]
    with pytest.raises(ValidationError):
        Storyboard(
            brief_id="b",
            voice_profile=_voice(),
            music_brief=_music(),
            scenes=tiny_scenes,
            cta_scene_idx=3,
            affiliate_link_placement="pinned_comment",
        )


@pytest.mark.unit
def test_cta_index_must_point_to_cta_scene() -> None:
    scenes = [_hook(), _body_scene(1), _body_scene(2), _cta_scene(3)]
    with pytest.raises(ValidationError):
        Storyboard(
            brief_id="b",
            voice_profile=_voice(),
            music_brief=_music(),
            scenes=scenes,
            cta_scene_idx=1,
            affiliate_link_placement="pinned_comment",
        )


@pytest.mark.unit
def test_missing_required_editor_pass_rejected() -> None:
    base = _valid_storyboard()
    bad_passes = [p for p in REQUIRED_EDITOR_PASSES if p is not EditorPass.AUTO_SUBTITLE]
    with pytest.raises(ValidationError):
        Storyboard(
            brief_id=base.brief_id,
            voice_profile=base.voice_profile,
            music_brief=base.music_brief,
            scenes=base.scenes,
            cta_scene_idx=base.cta_scene_idx,
            affiliate_link_placement=base.affiliate_link_placement,
            editor_passes=bad_passes,
        )


@pytest.mark.unit
def test_hyperframe_overlay_index_must_exist() -> None:
    base = _valid_storyboard()
    with pytest.raises(ValidationError):
        Storyboard(
            brief_id=base.brief_id,
            voice_profile=base.voice_profile,
            music_brief=base.music_brief,
            scenes=base.scenes,
            cta_scene_idx=base.cta_scene_idx,
            affiliate_link_placement=base.affiliate_link_placement,
            hyperframe_overlays=[HyperframeOverlay(scene_idx=99, template="x", props={})],
        )


@pytest.mark.unit
def test_music_bpm_must_be_ordered() -> None:
    with pytest.raises(ValidationError):
        MusicBrief(genre="x", bpm_range=(120, 90), license="suno")
