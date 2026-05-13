"""Production Director — orchestrates the studio approval workflow (ADR-007).

Manages the state machine for production runs through stages 1-10.
Sprint 7 implements stages 1-3 (creative direction):
  1. Brief & Concept (Strategist)
  2. Script (Screenwriter)
  3. Storyboard (Cinematographer + Storyboard Artist)

Each stage follows: DRAFT -> IN_REVIEW -> APPROVED / REVISION_PENDING / REJECTED.
Board decisions are persisted and fed to the Wiki.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from auto_affi.schemas.production import (
    DEFAULT_SLA_HOURS,
    MAX_REVISIONS_PER_STAGE,
    Decision,
    ProductionRun,
    ProductionRunStatus,
    ProductionStageStatus,
    Revision,
    to_json_path,
)

# ------------------------------------------------------------------ #
# Shopee URL parser                                                    #
# ------------------------------------------------------------------ #

def parse_shopee_url(url: str) -> tuple[int, int]:
    """Extract (shop_id, item_id) from a Shopee URL.

    Patterns:
      https://shopee.co.th/...-i.<shop_id>.<item_id>
      https://shopee.co.th/product/<shop_id>/<item_id>
    """
    # Pattern 1: -i.<shop>.<item>
    m = re.search(r"-i\.(\d+)\.(\d+)", url)
    if m:
        return int(m.group(1)), int(m.group(2))
    # Pattern 2: /product/<shop>/<item>
    m = re.search(r"/product/(\d+)/(\d+)", url)
    if m:
        return int(m.group(1)), int(m.group(2))
    raise ValueError(f"Cannot parse Shopee URL: {url}")


# ------------------------------------------------------------------ #
# Stage runners (stages 1-3)                                          #
# ------------------------------------------------------------------ #

def _run_stage_1_brief_and_concept(
    run: ProductionRun,
    revision_notes: str | None = None,
) -> dict[str, Any]:
    """Stage 1: Strategist produces 3 angle options.

    Phase 1: deterministic template. Phase 2: LLM-driven.
    """
    base_angles = [
        {
            "option": "A",
            "angle_th": "ครบในชุดเดียว ใช้งานง่าย",
            "angle_en": "All-in-one set, easy to use",
            "hook_style": "curiosity_gap",
        },
        {
            "option": "B",
            "angle_th": "ของเดิมหลุดอีกแล้ว เสียเวลา...",
            "angle_en": "Old one stripped again, wasted time...",
            "hook_style": "frustration",
        },
        {
            "option": "C",
            "angle_th": "ช่างจริงเลือกใช้",
            "angle_en": "Real pros choose this",
            "hook_style": "social_proof",
        },
    ]

    return {
        "angles": base_angles,
        "persona": {
            "label": "Thai DIY enthusiasts 25-45",
            "pain_points": ["tools breaking", "incomplete sets", "wasted time"],
        },
        "kpis": {"target_ctr": 0.025, "target_gmv_thb": 500},
        "revision_notes": revision_notes,
    }


def _run_stage_2_script(
    run: ProductionRun,
    revision_notes: str | None = None,
) -> dict[str, Any]:
    """Stage 2: Screenwriter produces 5-scene script + 2 hook variants.

    Uses the approved angle from stage 1 as input.
    """
    # Get approved angle from stage 1
    stage1 = run.get_stage(1)
    chosen_angle = "ของเดิมหลุดอีกแล้ว เสียเวลา..."
    if stage1 and stage1.current_revision and stage1.current_revision.artifact:
        angles = stage1.current_revision.artifact.get("angles", [])
        if angles:
            chosen_angle = angles[0].get("angle_th", chosen_angle)

    scenes = [
        {
            "idx": 0,
            "purpose": "hook",
            "duration_s": 1.5,
            "dialogue_th": f"{chosen_angle}",
            "on_screen_text_th": "ลองดูสิ!",
        },
        {
            "idx": 1,
            "purpose": "agitate",
            "duration_s": 2.5,
            "dialogue_th": "ใช้ประแจเก่าๆ ขันไม่แน่น หัวเสียบ่อย",
            "on_screen_text_th": "",
        },
        {
            "idx": 2,
            "purpose": "demonstrate",
            "duration_s": 2.5,
            "dialogue_th": "ชุดนี้มีครบ 8-14มม. เหล็กแข็ง จับถนัดมือ",
            "on_screen_text_th": "เหล็ก CR-V แข็งแกร่ง",
        },
        {
            "idx": 3,
            "purpose": "social_proof",
            "duration_s": 2.0,
            "dialogue_th": "รีวิว 5 ดาว จากช่างจริง กว่าพันคน",
            "on_screen_text_th": "5 ดาว 1,000+ รีวิว",
        },
        {
            "idx": 4,
            "purpose": "cta",
            "duration_s": 2.0,
            "dialogue_th": "แตะลิงก์ใต้คลิป สั่งเลยตอนนี้!",
            "on_screen_text_th": "แตะลิงก์ใต้คลิป",
        },
    ]

    hook_variants = [
        {"variant": 1, "text_th": chosen_angle},
        {"variant": 2, "text_th": "อย่าเสียเวลากับของถูก เปลี่ยนมาใช้ชุดนี้"},
    ]

    return {
        "scenes": scenes,
        "hook_variants": hook_variants,
        "total_duration_s": sum(s["duration_s"] for s in scenes),
        "revision_notes": revision_notes,
    }


def _run_stage_3_storyboard(
    run: ProductionRun,
    revision_notes: str | None = None,
) -> dict[str, Any]:
    """Stage 3: Cinematographer + Storyboard Artist extend script to full storyboard.

    Adds visual_prompt, shot_type, movement, lighting per scene.
    """
    stage2 = run.get_stage(2)
    scenes_input = []
    if stage2 and stage2.current_revision and stage2.current_revision.artifact:
        scenes_input = stage2.current_revision.artifact.get("scenes", [])

    storyboard_scenes = []
    visual_templates = [
        {
            "shot_type": "extreme-closeup",
            "movement": "snap-zoom-in",
            "visual_prompt": (
                "Extreme closeup of socket wrench set chrome-vanadium steel, "
                "dark workshop background, dramatic side lighting casting "
                "sharp shadows, shallow depth of field, metal gleaming"
            ),
        },
        {
            "shot_type": "medium-shot",
            "movement": "slow-pan-right",
            "visual_prompt": (
                "Medium shot of Thai man's hands struggling with old rusty "
                "wrench on a bolt, fluorescent workshop lighting, frustrated "
                "expression visible, sweat drops, warm amber tone"
            ),
        },
        {
            "shot_type": "overhead-flat-lay",
            "movement": "static",
            "visual_prompt": (
                "Overhead flat lay of complete 8-14mm socket set organized in "
                "foam tray, clean white surface, each piece labeled, "
                "professional product photography lighting, crisp shadows"
            ),
        },
        {
            "shot_type": "medium-shot",
            "movement": "static",
            "visual_prompt": (
                "Screenshot mockup of 5-star Shopee reviews overlaid on dark "
                "gradient background, Thai review text visible, product image "
                "in corner, clean typography, trust indicators"
            ),
        },
        {
            "shot_type": "product-hero",
            "movement": "zoom-in-slow",
            "visual_prompt": (
                "Product hero shot of socket set in carrying case, "
                "Shopee logo badge in corner, price tag floating beside, "
                "clean dark background with dramatic rim lighting"
            ),
        },
    ]

    for i, scene_data in enumerate(scenes_input or visual_templates):
        vis = visual_templates[i] if i < len(visual_templates) else visual_templates[-1]
        storyboard_scenes.append({
            "idx": i,
            "purpose": scene_data.get("purpose", "demonstrate"),
            "duration_s": scene_data.get("duration_s", 2.0),
            "dialogue_th": scene_data.get("dialogue_th", ""),
            "on_screen_text_th": scene_data.get("on_screen_text_th", ""),
            "shot_type": vis["shot_type"],
            "movement": vis["movement"],
            "visual_prompt": vis["visual_prompt"],
            "generator": "sora2",
            "sfx": [],
            "transition_out": "cut" if i < len(scenes_input) - 1 else "fade-out",
        })

    return {
        "scenes": storyboard_scenes,
        "music_brief": {"genre": "industrial-ambient", "bpm_range": [85, 100]},
        "voice_profile": {"lang": "th", "gender": "m", "tone": "confident-direct"},
        "revision_notes": revision_notes,
    }


def _run_stage_4_visual_references(
    run: ProductionRun,
    revision_notes: str | None = None,
) -> dict[str, Any]:
    """Stage 4: Art Director produces Nano Banana 2 stills per scene.

    Phase 1 (dry-run): returns fixture URIs.
    Phase 2: calls PhayaClient.create_nano_banana_image().
    """
    stage3 = run.get_stage(3)
    scenes = []
    if stage3 and stage3.current_revision and stage3.current_revision.artifact:
        scenes = stage3.current_revision.artifact.get("scenes", [])

    scene_images = []
    for scene in scenes:
        idx = scene.get("idx", 0)
        scene_images.append({
            "scene_idx": idx,
            "gs_uri": f"gs://auto-affi-media-dev/production/{run.run_id}/stage4/scene_{idx}.jpg",
            "prompt": scene.get("visual_prompt", ""),
            "status": "generated",
        })

    return {
        "scene_images": scene_images,
        "total_cost_thb": len(scene_images) * 0.05,
        "revision_notes": revision_notes,
    }


def _run_stage_5_animatics(
    run: ProductionRun,
    revision_notes: str | None = None,
) -> dict[str, Any]:
    """Stage 5: Editor creates image-to-video clips per scene.

    Supports "freeze-to-still" mode per scene to save cost
    (฿0.05 Ken Burns vs ฿2.50 i2v).
    """
    stage4 = run.get_stage(4)
    scene_images = []
    if stage4 and stage4.current_revision and stage4.current_revision.artifact:
        scene_images = stage4.current_revision.artifact.get("scene_images", [])

    scene_clips = []
    for img in scene_images:
        idx = img.get("scene_idx", 0)
        # Default to i2v; freeze-to-still is triggered by revision notes
        mode = "i2v"
        if revision_notes and f"--freeze scene {idx}" in revision_notes:
            mode = "freeze"

        cost = 0.05 if mode == "freeze" else 2.50
        scene_clips.append({
            "scene_idx": idx,
            "gs_uri": f"gs://auto-affi-media-dev/production/{run.run_id}/stage5/scene_{idx}.mp4",
            "image_gs_uri": img.get("gs_uri", ""),
            "mode": mode,
            "duration_s": 5,
            "cost_thb": cost,
        })

    return {
        "scene_clips": scene_clips,
        "total_cost_thb": sum(c["cost_thb"] for c in scene_clips),
        "revision_notes": revision_notes,
    }


def _run_stage_6_voiceover(
    run: ProductionRun,
    revision_notes: str | None = None,
) -> dict[str, Any]:
    """Stage 6: Sound Designer produces Thai TTS per scene with 2 voice options.

    Board picks one voice for the whole run.
    """
    stage2 = run.get_stage(2)
    scenes = []
    if stage2 and stage2.current_revision and stage2.current_revision.artifact:
        scenes = stage2.current_revision.artifact.get("scenes", [])

    voices = ["Algenib", "Zephyr"]
    scene_takes = []
    for scene in scenes:
        idx = scene.get("idx", 0)
        dialogue = scene.get("dialogue_th", "")
        if not dialogue:
            continue
        takes = []
        for voice in voices:
            takes.append({
                "voice": voice,
                "gs_uri": f"gs://auto-affi-media-dev/production/{run.run_id}/stage6/scene_{idx}_{voice.lower()}.mp3",
                "text_th": dialogue,
            })
        scene_takes.append({
            "scene_idx": idx,
            "takes": takes,
        })

    return {
        "scene_takes": scene_takes,
        "voices_available": voices,
        "total_cost_thb": len(scene_takes) * len(voices) * 0.001,
        "revision_notes": revision_notes,
    }


def _run_stage_7_music(
    run: ProductionRun,
    revision_notes: str | None = None,
) -> dict[str, Any]:
    """Stage 7: Sound Designer produces music bed + SFX cue list."""
    stage3 = run.get_stage(3)
    music_brief = {}
    total_duration = 10.0
    if stage3 and stage3.current_revision and stage3.current_revision.artifact:
        music_brief = stage3.current_revision.artifact.get("music_brief", {})
        scenes = stage3.current_revision.artifact.get("scenes", [])
        total_duration = sum(s.get("duration_s", 2.0) for s in scenes)

    genre = music_brief.get("genre", "ambient")
    return {
        "music_track": {
            "gs_uri": f"gs://auto-affi-media-dev/production/{run.run_id}/stage7/music.mp3",
            "mood": genre,
            "duration_s": total_duration,
            "cost_thb": 0.05,
        },
        "sfx_cues": [
            {"scene_idx": 0, "sfx": "whoosh-01", "at_s": 0.0},
        ],
        "total_cost_thb": 0.05,
        "revision_notes": revision_notes,
    }


_STAGE_RUNNERS = {
    1: _run_stage_1_brief_and_concept,
    2: _run_stage_2_script,
    3: _run_stage_3_storyboard,
    4: _run_stage_4_visual_references,
    5: _run_stage_5_animatics,
    6: _run_stage_6_voiceover,
    7: _run_stage_7_music,
}


# ------------------------------------------------------------------ #
# Production Director                                                  #
# ------------------------------------------------------------------ #

class InvalidTransitionError(ValueError):
    """Raised when a state transition is invalid."""


@dataclass
class ProductionDirector:
    """Orchestrates the studio approval workflow.

    Manages state machine transitions, stage execution, and persistence.
    """

    repo_root: Path = field(default_factory=lambda: Path("."))
    _runs: dict[str, ProductionRun] = field(default_factory=dict, init=False)

    def start_run(self, shopee_url: str) -> ProductionRun:
        """Create a new production run and execute stage 1."""
        try:
            shop_id, item_id = parse_shopee_url(shopee_url)
        except ValueError:
            shop_id, item_id = 0, 0

        run = ProductionRun(
            shopee_url=shopee_url,
            shopee_item_id=item_id,
            shopee_shop_id=shop_id,
            status=ProductionRunStatus.IN_PROGRESS,
        )
        self._runs[run.run_id] = run

        # Execute stage 1
        self._execute_stage(run, 1)

        # Persist
        self._save(run)
        return run

    def decide(
        self,
        run_id: str,
        stage_idx: int,
        verdict: str,
        notes_th: str = "",
        decided_by: str = "board",
    ) -> ProductionRun:
        """Apply a board decision to a stage.

        Args:
            run_id: The production run ID.
            stage_idx: Stage number (1-10).
            verdict: "approve", "revise", or "reject".
            notes_th: Revision notes or rejection reason (Thai).
            decided_by: Who made the decision.

        Returns:
            Updated ProductionRun.

        Raises:
            InvalidTransitionError: If the stage is not in IN_REVIEW state.
        """
        run = self.get_run(run_id)
        if run is None:
            raise InvalidTransitionError(f"Run {run_id} not found")

        stage = run.get_stage(stage_idx)
        if stage is None:
            raise InvalidTransitionError(f"Stage {stage_idx} not found in run {run_id}")

        if stage.status != ProductionStageStatus.IN_REVIEW:
            raise InvalidTransitionError(
                f"Stage {stage_idx} is {stage.status.value}, not in_review"
            )

        decision = Decision(
            verdict=verdict,
            decided_by=decided_by,
            notes_th=notes_th or None,
        )

        # Apply decision to current revision
        if stage.current_revision:
            stage.revisions[-1] = stage.current_revision.model_copy(
                update={"decision": decision}
            )

        if verdict == "approve":
            stage.status = ProductionStageStatus.APPROVED
            # Fire next stage if not the last
            if stage_idx < 10:
                next_stage = run.get_stage(stage_idx + 1)
                if next_stage and next_stage.status == ProductionStageStatus.DRAFT:
                    self._execute_stage(run, stage_idx + 1)
            # Check if all stages approved
            if all(s.status == ProductionStageStatus.APPROVED for s in run.stages):
                run.status = ProductionRunStatus.APPROVED

        elif verdict == "revise":
            if stage.revision_count >= MAX_REVISIONS_PER_STAGE:
                raise InvalidTransitionError(
                    f"Stage {stage_idx} has reached max revisions ({MAX_REVISIONS_PER_STAGE})"
                )
            stage.status = ProductionStageStatus.REVISION_PENDING
            # Re-execute stage with revision notes
            self._execute_stage(run, stage_idx, revision_notes=notes_th)

        elif verdict == "reject":
            stage.status = ProductionStageStatus.REJECTED
            run.status = ProductionRunStatus.REJECTED

        else:
            raise InvalidTransitionError(f"Unknown verdict: {verdict}")

        self._save(run)
        return run

    def get_run(self, run_id: str) -> ProductionRun | None:
        """Get a production run by ID (from memory or disk)."""
        if run_id in self._runs:
            return self._runs[run_id]
        # Try loading from disk
        path = self._production_dir() / f"{run_id}.json"
        if path.exists():
            from auto_affi.schemas.production import from_json_path
            run = from_json_path(path)
            self._runs[run.run_id] = run
            return run
        return None

    def list_runs(
        self, status_filter: ProductionRunStatus | None = None
    ) -> list[ProductionRun]:
        """List all production runs, optionally filtered by status."""
        from auto_affi.schemas.production import list_runs as _list
        return _list(repo_root=self.repo_root, status_filter=status_filter)

    def _execute_stage(
        self,
        run: ProductionRun,
        stage_idx: int,
        *,
        revision_notes: str | None = None,
    ) -> None:
        """Execute a stage's agent and produce a deliverable."""
        stage = run.get_stage(stage_idx)
        if stage is None:
            return

        runner = _STAGE_RUNNERS.get(stage_idx)
        if runner is None:
            # Stages 4-10 not implemented in Sprint 7
            stage.status = ProductionStageStatus.DRAFT
            return

        artifact = runner(run, revision_notes)

        cost = artifact.get("total_cost_thb", 0.001) if isinstance(artifact, dict) else 0.001
        revision = Revision(
            revision_idx=stage.revision_count,
            cost_thb=cost,
            artifact=artifact,
        )
        stage.revisions.append(revision)
        stage.status = ProductionStageStatus.IN_REVIEW
        stage.sla_deadline = datetime.now(UTC) + timedelta(hours=DEFAULT_SLA_HOURS)

        run.total_cost_thb += revision.cost_thb

    def _save(self, run: ProductionRun) -> None:
        """Persist run to disk."""
        to_json_path(run, repo_root=self.repo_root)

    def _production_dir(self) -> Path:
        d = self.repo_root / ".aegis/brain/production"
        d.mkdir(parents=True, exist_ok=True)
        return d
