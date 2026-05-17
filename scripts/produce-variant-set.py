#!/usr/bin/env python
"""Variant-set orchestrator — renders N hook variants of one concept,
sharing body+CTA shots across all variants.

Spec: docs/superpowers/specs/2026-05-18-auto-affi-variant-testing-design.md

Reads a ConceptVariantSet from disk:
    data/registry/items/<sku>/concepts/<concept_id>/
    ├── base.json       AiStoryboard (body + CTA shots, no hooks)
    └── hooks/{a,b,c}.json    list[AiShot] per variant

Phases:
  1. Stills — Gemini per-shot-per-variant
  2. Shared-shot render — Higgsfield once for body+CTA
  3. Variant-hook render — Higgsfield per variant
  4. Per-variant CTA bake — HyperFrames overlay with variant-specific sub_id
  5. Per-variant assembly — concat shared+variant clips, mix music, captions
  6. Persist links.json
"""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import json
import os
import sys
from pathlib import Path

from pydantic import SecretStr

from auto_affi.adapters.gcs_storage import GcsStorage
from auto_affi.adapters.gemini_image import (
    GEMINI_NANO_BANANA_PRO, GeminiImageClient,
)
from auto_affi.adapters.higgsfield_cli import HiggsfieldCli
from auto_affi.pipeline.shot_renderers import (
    build_subtitle_overlays, concat_clips, gemini_still, hold_to_mp4,
    mix_music_under, run_higgsfield_cli, thai_tts_wav,
)
from auto_affi.post.hyperframes_renderer import (
    composite_overlays_with_ffmpeg, render_storyboard_overlays,
)
from auto_affi.schemas.ai_storyboard import (
    AiShot, AiStoryboard, AudioSource, ConceptVariantSet, Generator,
    NarrativeRole,
)


# ---------------------------------------------------------------------------
# Pure-logic helpers — no I/O, fully unit-testable
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class RenderPlan:
    """Output of build_render_plan — describes what the orchestrator
    will render and where each artifact will land. Pure data, no I/O."""

    concept_dir_name: str
    shared_shot_ids: list[str]
    variant_hook_shots: dict[str, list[str]]   # variant_id -> shot_ids
    variant_outputs: dict[str, Path]           # variant_id -> final.mp4 path
    shared_out_dir: Path

    @property
    def shared_shot_count(self) -> int:
        return len(self.shared_shot_ids)

    @property
    def variant_hook_render_count(self) -> int:
        return sum(len(s) for s in self.variant_hook_shots.values())

    @property
    def total_renders(self) -> int:
        return self.shared_shot_count + self.variant_hook_render_count


def _concept_dir_name(vs: ConceptVariantSet) -> str:
    """Standard directory name: <item_id>-<concept_id>."""
    return f"{vs.item_id}-{vs.concept_id}"


def build_render_plan(
    vs: ConceptVariantSet, *, out_root: Path = Path("out"),
) -> RenderPlan:
    """Pure function — given a ConceptVariantSet, return the render plan.

    Shared shots = base.shots (the body+CTA list).
    Variant hook shots = variants[v].
    Output paths follow the convention in the spec section 5.
    """
    cd = _concept_dir_name(vs)
    concept_dir = out_root / cd
    shared_out = concept_dir / "shared"
    variant_outputs: dict[str, Path] = {
        vid: concept_dir / f"variant-{vid}" / "final.mp4"
        for vid in vs.variants
    }
    return RenderPlan(
        concept_dir_name=cd,
        shared_shot_ids=[s.shot_id for s in vs.base.shots],
        variant_hook_shots={
            vid: [s.shot_id for s in shots]
            for vid, shots in vs.variants.items()
        },
        variant_outputs=variant_outputs,
        shared_out_dir=shared_out,
    )


def build_links_map(vs: ConceptVariantSet) -> dict[str, str]:
    """Pure function — variant_id -> Shopee sub_id of the form
    <item_id>-<concept_id>-<variant_id>. Persisted to links.json."""
    return {
        vid: f"{vs.item_id}-{vs.concept_id}-{vid}"
        for vid in vs.variants
    }


# ---------------------------------------------------------------------------
# I/O orchestration (Phase 2 of plan — wired in Task 9)
# ---------------------------------------------------------------------------


def load_variant_set(concept_dir: Path) -> ConceptVariantSet:
    """Read base.json + hooks/*.json from a concept directory."""
    base_path = concept_dir / "base.json"
    if not base_path.exists():
        raise FileNotFoundError(f"base.json missing in {concept_dir}")
    base = AiStoryboard.model_validate_json(base_path.read_text(encoding="utf-8"))

    hooks_dir = concept_dir / "hooks"
    if not hooks_dir.is_dir():
        raise FileNotFoundError(f"hooks/ missing in {concept_dir}")
    variants: dict[str, list[AiShot]] = {}
    for hook_file in sorted(hooks_dir.glob("*.json")):
        vid = hook_file.stem
        data = json.loads(hook_file.read_text(encoding="utf-8"))
        variants[vid] = [AiShot.model_validate(d) for d in data]

    return ConceptVariantSet(
        concept_id=concept_dir.name,
        item_id=base.item_id,
        base=base,
        variants=variants,
    )


# ---------------------------------------------------------------------------
# Render orchestration (Phase 3 — wired against shared shot_renderers)
# ---------------------------------------------------------------------------


async def orchestrate_renders(
    vs: ConceptVariantSet, plan: RenderPlan,
    *, characters_dir: Path, product_refs_dir: Path,
    music_path: Path | None,
    tts_source: str = "edge", tts_voice: str | None = None,
) -> None:
    """Execute all render phases. Shared shots render once (under
    plan.shared_out_dir); variant shots render under
    plan.variant_outputs[vid].parent."""

    # Construct clients (lazy where possible)
    for k in ("GOOGLE_API_KEY", "AUTO_AFFI__GCS_BUCKET"):
        if not os.environ.get(k, "").strip():
            raise RuntimeError(f"missing env: {k}")
    GcsStorage(bucket_name=os.environ["AUTO_AFFI__GCS_BUCKET"])
    gemini = GeminiImageClient(
        api_key=SecretStr(os.environ["GOOGLE_API_KEY"]),
        model=GEMINI_NANO_BANANA_PRO,
    )
    higgsfield: HiggsfieldCli | None = None
    needs_hf = any(
        s.generator is Generator.HIGGSFIELD_CLI
        for shots in [vs.base.shots] + list(vs.variants.values())
        for s in shots
    )
    if needs_hf:
        higgsfield = HiggsfieldCli()

    plan.shared_out_dir.mkdir(parents=True, exist_ok=True)
    for vid in vs.variants:
        plan.variant_outputs[vid].parent.mkdir(parents=True, exist_ok=True)

    # PHASE 1 — Stills (shared + per-variant)
    print("── PHASE 1 · stills")
    for shot in vs.base.shots:
        still = plan.shared_out_dir / f"{shot.shot_id}_image.jpg"
        if still.exists():
            print(f"  📦 reusing shared {still.name}")
            continue
        refs: list[Path] = []  # callers supply via resolve_refs if needed
        await gemini_still(client=gemini, shot=shot, dest=still, refs=refs)
        print(f"  ✅ shared {still.name}")
    for vid, shots in vs.variants.items():
        for shot in shots:
            still = plan.variant_outputs[vid].parent / f"{shot.shot_id}_image.jpg"
            if still.exists():
                print(f"  📦 reusing variant-{vid} {still.name}")
                continue
            await gemini_still(client=gemini, shot=shot, dest=still, refs=[])
            print(f"  ✅ variant-{vid} {still.name}")

    # PHASE 2 — Shared shot clips (render ONCE)
    print("\n── PHASE 2 · shared shots (render once)")
    for shot in vs.base.shots:
        still = plan.shared_out_dir / f"{shot.shot_id}_image.jpg"
        clip = plan.shared_out_dir / f"{shot.shot_id}_clip.mp4"
        if clip.exists():
            print(f"  📦 reusing {clip.name}")
            continue
        await _render_one_shot(
            shot=shot, still=still, dest=clip,
            higgsfield=higgsfield, workdir=plan.shared_out_dir,
            tts_source=tts_source, tts_voice=tts_voice,
        )

    # PHASE 3 — Per-variant hook shots
    print("\n── PHASE 3 · per-variant hook shots")
    for vid, shots in vs.variants.items():
        var_dir = plan.variant_outputs[vid].parent
        for shot in shots:
            still = var_dir / f"{shot.shot_id}_image.jpg"
            clip = var_dir / f"{shot.shot_id}_clip.mp4"
            if clip.exists():
                print(f"  📦 reusing variant-{vid} {clip.name}")
                continue
            await _render_one_shot(
                shot=shot, still=still, dest=clip,
                higgsfield=higgsfield, workdir=var_dir,
                tts_source=tts_source, tts_voice=tts_voice,
            )

    # PHASE 4 — Per-variant assembly
    print("\n── PHASE 4 · per-variant assembly")
    for vid, shots in vs.variants.items():
        var_dir = plan.variant_outputs[vid].parent
        # Variant hook clips
        var_clip_paths = [var_dir / f"{s.shot_id}_clip.mp4" for s in shots]
        # Shared body+CTA clips
        shared_clip_paths = [
            plan.shared_out_dir / f"{s.shot_id}_clip.mp4"
            for s in vs.base.shots
        ]
        all_clips = var_clip_paths + shared_clip_paths
        concat_mp4 = var_dir / "concat.mp4"
        concat_clips(all_clips, var_dir, concat_mp4)

        # Music mix (use the music_path if supplied, else skip)
        mixed = var_dir / "mixed.mp4"
        if music_path and music_path.exists():
            mix_music_under(concat_mp4, music_path, mixed, gain_db=-12.0)
        else:
            mixed = concat_mp4

        # Captions (per-shot subtitles from the variant's shot list +
        # the base's shot list — same logic as produce-ai-storyboard)
        # Compute offsets across the full timeline:
        merged_shots = shots + list(vs.base.shots)
        offsets: dict[str, float] = {}
        t = 0.0
        for s in merged_shots:
            offsets[s.shot_id] = t
            # use actual clip duration from disk if available; spec says
            # variant + base durations sum to base.target_total_duration_s
            t += s.duration_s
        # Build a synthetic AiStoryboard for overlay rendering
        synthetic = AiStoryboard(
            concept_id=f"{vs.concept_id}-{vid}",
            title_en=vs.base.title_en, title_th=vs.base.title_th,
            item_id=vs.item_id, consistency_seed=vs.base.consistency_seed,
            target_total_duration_s=vs.base.target_total_duration_s,
            music_prompt=vs.base.music_prompt,
            music_duration_s=vs.base.music_duration_s,
            shots=merged_shots,
        )
        overlays = build_subtitle_overlays(synthetic, offsets)
        if overlays:
            ov_workdir = var_dir / "overlays"
            ov_workdir.mkdir(parents=True, exist_ok=True)
            rendered = render_storyboard_overlays(
                overlays=overlays, projects_dir=Path("hyperframes"),
                output_dir=ov_workdir,
            )
            composite_overlays_with_ffmpeg(
                base_video=mixed, overlays=rendered,
                output=plan.variant_outputs[vid],
            )
        else:
            mixed.replace(plan.variant_outputs[vid])
        print(f"  ✅ variant-{vid}: {plan.variant_outputs[vid]}")


async def _render_one_shot(
    *, shot: AiShot, still: Path, dest: Path,
    higgsfield: HiggsfieldCli | None, workdir: Path,
    tts_source: str, tts_voice: str | None,
) -> None:
    """Single-shot dispatch shared by Phase 2 + Phase 3."""
    print(f"  {shot.shot_id} [{shot.generator.value}] {shot.duration_s}s")
    if shot.generator is Generator.HOLD:
        vo_wav: Path | None = None
        if shot.audio_source is AudioSource.PHAYA_TTS and shot.dialogue_th:
            vo_wav = workdir / f"{shot.shot_id}_vo.wav"
            if not vo_wav.exists():
                await thai_tts_wav(
                    client=None, gcs=None, text=shot.dialogue_th, dest=vo_wav,
                    source=tts_source, voice=tts_voice,
                )
        hold_to_mp4(still, dest, shot.duration_s, voiceover_wav=vo_wav)
    elif shot.generator is Generator.HIGGSFIELD_CLI:
        if higgsfield is None:
            raise RuntimeError(f"{shot.shot_id}: higgsfield_cli requires the CLI")
        await run_higgsfield_cli(
            hf=higgsfield, shot=shot, still=still, workdir=workdir, dest=dest,
        )
    else:
        raise RuntimeError(
            f"{shot.shot_id}: generator {shot.generator.value} not supported "
            f"in variant orchestrator (use HOLD or HIGGSFIELD_CLI)"
        )


async def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--concept-dir", type=Path, required=True,
                   help="Path to data/registry/items/<sku>/concepts/<concept_id>/")
    p.add_argument("--out-root", type=Path, default=Path("out"))
    p.add_argument("--character-workdir", type=Path, default=None,
                   help="Directory holding characters/* reference images "
                        "(currently unused — variant orchestrator's stills "
                        "skip resolve_refs; provide once visual_reference_lock "
                        "wiring lands).")
    p.add_argument("--product-refs-dir", type=Path, default=None,
                   help="Directory holding product-refs/* (same caveat as "
                        "--character-workdir).")
    p.add_argument("--music-path", type=Path, default=None,
                   help="Pre-generated music track to mix under every variant "
                        "(reuse across variants — variant testing should hold "
                        "music constant). If omitted, variants ship without a "
                        "music bed.")
    p.add_argument("--tts-source", type=str, default="edge",
                   choices=["edge", "phaya"],
                   help="Thai TTS engine. 'edge' (default) = free Microsoft "
                        "Edge th-TH-NiwatNeural (natural male voice).")
    p.add_argument("--tts-voice", type=str, default=None,
                   help="Override the default TTS voice.")
    p.add_argument("--plan-only", action="store_true",
                   help="Print the render plan + write links.json, then exit "
                        "without rendering anything.")
    args = p.parse_args()

    vs = load_variant_set(args.concept_dir)
    plan = build_render_plan(vs, out_root=args.out_root)
    links = build_links_map(vs)

    print(f"📜 concept: {vs.concept_id} (item {vs.item_id})")
    print(f"   shared shots: {plan.shared_shot_ids}")
    print(f"   variants: {plan.variant_hook_shots}")
    print(f"   total renders: {plan.total_renders} "
          f"(vs naive {plan.shared_shot_count * len(vs.variants) + plan.variant_hook_render_count})")
    print(f"   outputs: {[str(p) for p in plan.variant_outputs.values()]}")

    # links.json persistence
    (args.concept_dir / "links.json").write_text(
        json.dumps(links, indent=2), encoding="utf-8",
    )
    print(f"   wrote {args.concept_dir / 'links.json'}")

    if args.plan_only:
        print("\n(--plan-only) skipping render orchestration.")
        return 0

    await orchestrate_renders(
        vs, plan,
        characters_dir=args.character_workdir or Path("."),
        product_refs_dir=args.product_refs_dir or Path("."),
        music_path=args.music_path,
        tts_source=args.tts_source, tts_voice=args.tts_voice,
    )
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
