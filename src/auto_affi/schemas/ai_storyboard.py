"""AI-gen-ready storyboard schema (v2 — replaces schemas/storyboard.py for
new productions).

Derived from the 2026-05-15 research on AI-gen video storyboarding +
HeyGen Avatar IV workflow. See:
``.aegis/brain/learnings/2026-05-15-ai-gen-storyboard-methodology.md``

Key invariants this schema enforces that the v1 schema didn't:

1. **Generator routing is a first-class field.** Every shot declares which
   model owns it (higgsfield_cli / seedance_2kf / seedance_t2v / veo /
   hold). The orchestrator dispatches based on this, not on prose.

2. **Duration buckets** match the AI consistency floor (3-6s per shot).
   A shot that wants > 6s is split into sub-shots with the same
   consistency_seed.

3. **Visual reference locks** are explicit (file paths) — not implied by
   prose. Every shot lists which character / product / lighting refs
   are attached to the gen call.

4. **A consistency_seed is mandatory** and is the SAME across all shots
   in a storyboard — prevents character / lighting / palette drift
   between shots.

5. **Negatives** are a structured list — anti-prompts that get appended
   to the generator call. Includes anti-patterns we've learned (no
   over-the-shoulder, no mesh-head condenser if SKU is broadcast mic).

6. **Audio source is declared** — phaya_tts / seedance_diegetic /
   music_only / silence. HeyGen Avatar IV requires phaya_tts.

7. **Keyframes block** is only present when generator = seedance_2kf,
   and names the start + end refs explicitly.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class Generator(StrEnum):
    """Which model owns rendering of this shot."""

    HIGGSFIELD_CLI = "higgsfield_cli"  # routes through `higgsfield generate create <model>`
    SEEDANCE_2KF = "seedance_2kf"  # two-keyframe i2v — Seedance 1.5 Pro via Phaya
    SEEDANCE_2_FAST = "seedance_2_fast"  # Seedance 2.0 Fast via PiAPI ($0.08/s) — fallback path
    SEEDANCE_2_PRO = "seedance_2_pro"  # Seedance 2.0 full quality via PiAPI ($0.10/s) — fallback path
    SEEDANCE_T2V = "seedance_t2v"  # text-to-video (no start frame)
    VEO = "veo"  # Gemini Veo 3.1 (premium)
    HOLD = "hold"  # static image held for the shot duration


class NarrativeRole(StrEnum):
    """HSO×VCS Method narrative function of the shot."""

    HOOK = "hook"  # 0-3s — pattern interrupt
    STORY = "story"  # 3-30s — emotional / informational beats
    OFFER = "offer"  # 30s+ — product reveal + price + CTA
    BRIDGE = "bridge"  # silent transition / breath


class AudioSource(StrEnum):
    PHAYA_TTS = "phaya_tts"  # external Thai TTS, MUST route through HeyGen
    SEEDANCE_DIEGETIC = "seedance_diegetic"  # in-clip Seedance audio
    MUSIC_ONLY = "music_only"  # music bed, no dialogue
    SILENCE = "silence"  # silent + room tone only


class SubtitlePlacement(StrEnum):
    LOWER_THIRD = "lower_third"
    UPPER_THIRD = "upper_third"
    CENTER = "center"


class Keyframes(BaseModel):
    """Start + end reference for Seedance two-keyframe i2v."""

    start_ref: str  # path relative to workdir, e.g. "s0_image.jpg"
    end_ref: str
    motion_label: str = Field(min_length=1, max_length=200)


class Subtitle(BaseModel):
    text_th: str = Field(min_length=1, max_length=300)
    placement: SubtitlePlacement = SubtitlePlacement.LOWER_THIRD
    # Caption appears for the full shot duration unless overridden
    start_offset_s: float = 0.0
    duration_s: float | None = None


class AiShot(BaseModel):
    """One shot in an AI-gen storyboard — fully specified for batch
    submission. No prose interpretation required at gen time."""

    shot_id: str = Field(min_length=1)
    narrative_role: NarrativeRole
    duration_s: float = Field(gt=0.5, le=6.0)  # AI consistency floor
    generator: Generator
    image_prompt: str = Field(min_length=20, max_length=2000)
    visual_reference_lock: list[str] = Field(default_factory=list)
    negatives: list[str] = Field(default_factory=list)
    consistency_seed: int
    audio_source: AudioSource
    dialogue_th: str | None = None
    subtitle: Subtitle | None = None
    keyframes: Keyframes | None = None
    # Optional generator-specific knobs
    motion_prompt: str | None = None  # HeyGen Avatar IV body/head motion
    expressiveness: Literal["low", "medium", "high"] | None = None  # HeyGen
    aspect_ratio: Literal["9:16", "16:9"] = "9:16"
    # Higgsfield CLI knobs — only meaningful when generator=HIGGSFIELD_CLI
    higgsfield_model: str | None = None  # e.g. "seedance_2_0", "cinematic_studio_3_0", "veo3_1"
    higgsfield_mode: str | None = None  # e.g. "fast" / "std" for Seedance, "pro" / "std" for Kling
    higgsfield_resolution: Literal["480p", "720p", "1080p"] | None = None

    @field_validator("shot_id")
    @classmethod
    def _shot_id_format(cls, v: str) -> str:
        # s0, s1, ..., s99 — keeps filenames sortable
        if not v.startswith("s") or not v[1:].isdigit():
            raise ValueError(f"shot_id must match s<int>, got {v!r}")
        return v

    @model_validator(mode="after")
    def _enforce_generator_invariants(self) -> "AiShot":
        # Two-keyframe Seedance must declare keyframes (1.5 Pro AND 2.0)
        if self.generator in (
            Generator.SEEDANCE_2KF,
            Generator.SEEDANCE_2_FAST,
            Generator.SEEDANCE_2_PRO,
        ) and self.keyframes is None:
            raise ValueError(
                f"shot {self.shot_id}: {self.generator.value} requires keyframes block"
            )

        # Higgsfield CLI shots must name which underlying model to dispatch
        if self.generator is Generator.HIGGSFIELD_CLI:
            if not self.higgsfield_model:
                raise ValueError(
                    f"shot {self.shot_id}: higgsfield_cli requires "
                    f"higgsfield_model (e.g. 'seedance_2_0', "
                    f"'cinematic_studio_3_0', 'veo3_1')"
                )

        # phaya_tts requires dialogue_th
        if self.audio_source is AudioSource.PHAYA_TTS and not self.dialogue_th:
            raise ValueError(
                f"shot {self.shot_id}: audio_source=phaya_tts requires dialogue_th"
            )

        return self


class AiStoryboard(BaseModel):
    """A full AI-gen storyboard — ordered list of shots + production meta."""

    version: Literal["2"] = "2"
    concept_id: str
    title_en: str
    title_th: str
    item_id: int
    consistency_seed: int = Field(
        description="Seed propagated to every shot. Locks character + "
                    "lighting + palette across the whole storyboard."
    )
    palette_grade: str = Field(
        default="desaturated 0.65 + warm-amber accent",
        description="LUT / grade target applied to the final concat. "
                    "Defends against AI-slop plastic look.",
    )
    target_total_duration_s: float = Field(gt=5.0, le=60.0)
    aspect_ratio: Literal["9:16", "16:9"] = "9:16"
    music_prompt: str = Field(min_length=20)
    music_duration_s: float = Field(gt=0.0, le=60.0)
    shots: list[AiShot] = Field(min_length=1)

    @model_validator(mode="after")
    def _propagate_and_validate(self) -> "AiStoryboard":
        # Force every shot to share the storyboard's consistency_seed —
        # the schema's load-bearing invariant against character drift.
        for shot in self.shots:
            if shot.consistency_seed != self.consistency_seed:
                raise ValueError(
                    f"shot {shot.shot_id} has consistency_seed="
                    f"{shot.consistency_seed} but storyboard requires "
                    f"{self.consistency_seed}. Every shot must share the seed."
                )

        # shot_ids must be unique
        ids = [s.shot_id for s in self.shots]
        if len(set(ids)) != len(ids):
            raise ValueError(f"duplicate shot_ids in storyboard: {ids}")

        # Total duration must be within ±2s of target
        total = sum(s.duration_s for s in self.shots)
        if abs(total - self.target_total_duration_s) > 2.0:
            raise ValueError(
                f"shots sum to {total:.2f}s but target is "
                f"{self.target_total_duration_s:.2f}s (±2s tolerance)"
            )
        return self

    def shots_by_generator(self) -> dict[Generator, list[AiShot]]:
        """Group shots by generator — used by the orchestrator to dispatch
        per-engine batches in parallel."""
        out: dict[Generator, list[AiShot]] = {}
        for s in self.shots:
            out.setdefault(s.generator, []).append(s)
        return out
