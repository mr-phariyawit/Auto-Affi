"""Storyboard — Writers' Room consolidated output.

Mirrors the JSON schema in SPEC.md §6.2 line-for-line so the Editor agent
can hand it straight to the asset pipeline. Hard rules from the canonical
wiki are encoded as validators here, not just in prompts, because schema
violations are caught at handoff time before any GPU spend happens.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class Aspect(StrEnum):
    """Output aspect ratio. Phase 1 is 9:16 only."""

    VERTICAL_9_16 = "9:16"


class VoiceProfile(BaseModel):
    """TTS settings consumed by the Producer."""

    lang: Literal["th"]
    gender: Literal["m", "f", "neutral"]
    tone: str = Field(min_length=1, max_length=80)
    tts_engine: Literal["elevenlabs", "botnoi", "azure"]
    voice_id: str = Field(min_length=1)


class MusicBrief(BaseModel):
    """Music selection criteria for the Sound Designer."""

    genre: str = Field(min_length=1, max_length=40)
    bpm_range: tuple[int, int]
    license: Literal["epidemic-sound", "artlist", "suno", "self-cleared"]

    @model_validator(mode="after")
    def _bpm_ordered(self) -> MusicBrief:
        low, high = self.bpm_range
        if low <= 0 or high <= 0:
            raise ValueError("BPM values must be positive")
        if low > high:
            raise ValueError("BPM range must be ordered low..high")
        return self


class ScenePurpose(StrEnum):
    """High-level role of each scene in the funnel."""

    HOOK = "hook"
    DEMONSTRATE = "demonstrate"
    AGITATE = "agitate"
    RESOLVE = "resolve"
    SOCIAL_PROOF = "social_proof"
    CTA = "cta"


class Dialogue(BaseModel):
    """Spoken line for the scene."""

    speaker: Literal["narrator", "character"]
    text_th: str = Field(min_length=1, max_length=300)
    emphasis_words: list[str] = Field(default_factory=list)


class OnScreenText(BaseModel):
    """Burned-in Thai text -- never rendered by the image/video model."""

    th: str = Field(min_length=1, max_length=120)
    style: str = Field(min_length=1, max_length=40)
    position: str = Field(min_length=1, max_length=40)


GeneratorName = Literal["veo3", "veo3_fast", "sora2", "kling", "hailuo", "flux", "imagen"]


class Scene(BaseModel):
    """One shot in the storyboard."""

    idx: int = Field(ge=0)
    duration_s: float = Field(gt=0, le=15)
    purpose: ScenePurpose
    shot_type: str = Field(min_length=1, max_length=60)
    movement: str = Field(default="static", max_length=60)
    visual_prompt: str = Field(min_length=1, max_length=2000)
    generator: GeneratorName
    dialogue: Dialogue | None = None
    on_screen_text: OnScreenText | None = None
    sfx: list[str] = Field(default_factory=list)
    transition_out: str = Field(default="cut")


class HyperframeOverlay(BaseModel):
    """HTML/Hyperframe overlay layered on top of a scene."""

    scene_idx: int = Field(ge=0)
    template: str = Field(min_length=1)
    props: dict[str, object] = Field(default_factory=dict)


class EditorPass(StrEnum):
    """Standard post-production passes the Editor must run."""

    SILENCE_TRIM = "silence_trim"
    FILLER_CUT = "filler_cut"
    AUTO_SUBTITLE = "auto_subtitle"
    HOOK_PUNCH_IN = "hook_punch_in"
    BRAND_OVERLAY = "brand_overlay"
    CTA_ENDCARD = "cta_endcard"


# Editor passes are mandatory in this order -- see playbook section 3.5.1.
REQUIRED_EDITOR_PASSES: tuple[EditorPass, ...] = (
    EditorPass.SILENCE_TRIM,
    EditorPass.FILLER_CUT,
    EditorPass.AUTO_SUBTITLE,
    EditorPass.HOOK_PUNCH_IN,
    EditorPass.BRAND_OVERLAY,
    EditorPass.CTA_ENDCARD,
)

_MAX_TOTAL_DURATION_S = 60.0
_MAX_HOOK_DURATION_S = 2.0
_AVG_SHOT_MIN_S = 1.0
# 2026-05-14: raised from 3.0 → 5.0 to accommodate cinematic narrative pacing
# (4-6s holds for emotional beats, per John Lewis / Apple "Misunderstood" /
# Cannes-Lions short-film grammar). Sketch-style 1-3s cuts still fit comfortably.
_AVG_SHOT_MAX_S = 5.0


class Storyboard(BaseModel):
    """Writers' Room final output."""

    storyboard_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    version: int = Field(default=1, ge=1)
    brief_id: str
    aspect: Aspect = Aspect.VERTICAL_9_16
    voice_profile: VoiceProfile
    music_brief: MusicBrief
    scenes: list[Scene] = Field(min_length=2)
    cta_scene_idx: int = Field(ge=0)
    affiliate_link_placement: str = Field(min_length=1)
    reference_clip_uri: str | None = None
    editor_passes: list[EditorPass] = Field(default_factory=lambda: list(REQUIRED_EDITOR_PASSES))
    hyperframe_overlays: list[HyperframeOverlay] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # ------------------------------------------------------------------ #
    # validators                                                         #
    # ------------------------------------------------------------------ #

    @model_validator(mode="after")
    def _scene_indices_contiguous(self) -> Storyboard:
        for expected, scene in enumerate(self.scenes):
            if scene.idx != expected:
                raise ValueError(
                    f"scene.idx must be contiguous from 0; got {scene.idx} at position {expected}"
                )
        return self

    @model_validator(mode="after")
    def _total_duration_within_cap(self) -> Storyboard:
        total = sum(scene.duration_s for scene in self.scenes)
        if total > _MAX_TOTAL_DURATION_S:
            raise ValueError(f"total duration {total:.1f}s exceeds 60s cap (publisher rejects)")
        return self

    @model_validator(mode="after")
    def _first_scene_is_hook_within_limit(self) -> Storyboard:
        first = self.scenes[0]
        if first.purpose is not ScenePurpose.HOOK:
            raise ValueError("scenes[0].purpose must be HOOK")
        if first.duration_s > _MAX_HOOK_DURATION_S:
            raise ValueError(
                f"hook duration {first.duration_s:.1f}s exceeds {_MAX_HOOK_DURATION_S}s cap"
            )
        return self

    @model_validator(mode="after")
    def _avg_shot_in_band(self) -> Storyboard:
        # Hook is short by design -- exclude it from the average.
        body = self.scenes[1:]
        if not body:
            return self
        avg = sum(scene.duration_s for scene in body) / len(body)
        if not _AVG_SHOT_MIN_S <= avg <= _AVG_SHOT_MAX_S:
            raise ValueError(
                f"avg shot {avg:.2f}s outside {_AVG_SHOT_MIN_S}-{_AVG_SHOT_MAX_S}s band"
            )
        return self

    @model_validator(mode="after")
    def _cta_scene_index_valid(self) -> Storyboard:
        if self.cta_scene_idx >= len(self.scenes):
            raise ValueError("cta_scene_idx out of range")
        if self.scenes[self.cta_scene_idx].purpose is not ScenePurpose.CTA:
            raise ValueError("cta_scene_idx must point to a CTA scene")
        return self

    @model_validator(mode="after")
    def _required_editor_passes_present(self) -> Storyboard:
        missing = [p for p in REQUIRED_EDITOR_PASSES if p not in self.editor_passes]
        if missing:
            raise ValueError(f"missing required editor passes: {missing}")
        return self

    @model_validator(mode="after")
    def _hyperframe_indices_in_range(self) -> Storyboard:
        n = len(self.scenes)
        for overlay in self.hyperframe_overlays:
            if overlay.scene_idx >= n:
                raise ValueError(f"hyperframe overlay scene_idx {overlay.scene_idx} out of range")
        return self

    @field_validator("affiliate_link_placement")
    @classmethod
    def _affiliate_link_must_be_disclosed(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("affiliate_link_placement is required")
        return value

    # ------------------------------------------------------------------ #
    # convenience                                                        #
    # ------------------------------------------------------------------ #

    @property
    def total_duration_s(self) -> float:
        return sum(scene.duration_s for scene in self.scenes)
