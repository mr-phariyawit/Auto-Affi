#!/usr/bin/env python
"""Orchestrate an AiStoryboard v2 → finished video.

Phases:
  1. Resolve every shot's visual_reference_lock to local paths
  2. Render the scene still for each shot via Gemini Nano Banana Pro
     (with image_prompt + refs + negatives wired in)
  3. Dispatch each shot to its declared generator:
       hold             → ffmpeg loops the still for shot.duration_s
       seedance_2kf     → Phaya Seedance two-keyframe
       seedance_t2v     → Phaya Seedance text-to-video
       veo              → Gemini Veo 3.1 (not wired here yet — escalates)
  4. Normalize every shot to uniform AAC params + concat in order
  5. Generate music (Phaya text_to_music) + mix
  6. Render + composite per-shot subtitle overlays (HyperFrames)
  7. Save final to --output

Single-file orchestrator — keeps the v2 production path independent
of the legacy gen-video-seedance.py orchestrator (which is tied to
the v1 storyboard schema).

Usage:
    .venv/bin/python scripts/produce-ai-storyboard.py \\
        --item-id 28875679676 \\
        --storyboard-json data/registry/items/28875679676/concept-2-v2/storyboard.json \\
        --workdir out/maono-concept-2-workdir-v10 \\
        --output out/maono-concept-2-final-v10.mp4 \\
        --character-workdir out/maono-concept-2-workdir-v8/characters \\
        --product-refs-dir data/registry/items/28875679676/product-refs
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import timedelta
from pathlib import Path

import httpx
from pydantic import SecretStr

from auto_affi.adapters.gcs_storage import GcsStorage
from auto_affi.adapters.gemini_image import GEMINI_NANO_BANANA_PRO, GeminiImageClient
from auto_affi.adapters.higgsfield_cli import HiggsfieldCli, HiggsfieldCliError
from auto_affi.adapters.phaya import JobState, PhayaClient
from auto_affi.adapters.seedance2 import Seedance2Client
from auto_affi.pipeline.shot_renderers import (
    aac_flags, ffprobe_duration, resolve_refs, gemini_still,
    hold_to_mp4, normalize_mp4, pad_audio, thai_tts_wav,
    run_higgsfield_cli, run_seedance_2kf, run_seedance_2_2kf,
    concat_clips, mix_music_under, build_subtitle_overlays,
)
from auto_affi.post.hyperframes_renderer import (
    composite_overlays_with_ffmpeg, render_storyboard_overlays,
)
from auto_affi.schemas.ai_storyboard import (
    AiStoryboard, AudioSource, Generator,
)


async def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--item-id", type=int, required=True)
    p.add_argument("--storyboard-json", type=Path, required=True)
    p.add_argument("--workdir", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--character-workdir", type=Path, required=True)
    p.add_argument("--product-refs-dir", type=Path, required=True)
    p.add_argument("--skip-stills", action="store_true",
                   help="Don't re-generate stills if they already exist in workdir.")
    p.add_argument("--skip-shots", action="store_true",
                   help="Don't re-render shot clips if they already exist.")
    p.add_argument("--key-prefix", type=str, default="ai-storyboard/v2-concept-2",
                   help="GCS key prefix for Seedance keyframes.")
    p.add_argument("--tts-source", type=str, default="edge",
                   choices=["edge", "phaya"],
                   help="Thai TTS engine. 'edge' (default) = free Microsoft Edge "
                        "th-TH-NiwatNeural (natural male voice). 'phaya' = Phaya "
                        "Algenib (AI-obvious, hurts affiliate trust per 2026-05-15 "
                        "research).")
    p.add_argument("--tts-voice", type=str, default=None,
                   help="Override the default TTS voice (e.g. 'th-TH-PremwadeeNeural' "
                        "for the female Edge voice).")
    args = p.parse_args()

    # Env
    for k in ("PHAYA_API_KEY", "GOOGLE_API_KEY", "AUTO_AFFI__GCS_BUCKET"):
        if not os.environ.get(k, "").strip():
            print(f"ERROR: {k} missing"); return 1

    sb = AiStoryboard.model_validate_json(args.storyboard_json.read_text(encoding="utf-8"))
    args.workdir.mkdir(parents=True, exist_ok=True)
    print(f"📜 storyboard: {sb.concept_id} · {len(sb.shots)} shots · {sum(s.duration_s for s in sb.shots):.1f}s")

    gcs = GcsStorage(bucket_name=os.environ["AUTO_AFFI__GCS_BUCKET"])
    gemini = GeminiImageClient(
        api_key=SecretStr(os.environ["GOOGLE_API_KEY"]), model=GEMINI_NANO_BANANA_PRO,
    )
    phaya = PhayaClient(api_key=SecretStr(os.environ["PHAYA_API_KEY"]), timeout_s=60.0)
    # Seedance 2.0 client is constructed only when actually used so the
    # orchestrator still runs for storyboards that don't need it
    # (PIAPI_API_KEY remains optional until a SEEDANCE_2_* shot appears).
    seedance2: Seedance2Client | None = None
    if os.environ.get("PIAPI_API_KEY", "").strip():
        seedance2 = Seedance2Client(
            api_key=SecretStr(os.environ["PIAPI_API_KEY"]), timeout_s=120.0,
        )
    # Higgsfield CLI is constructed lazily — only when the storyboard
    # actually uses a higgsfield_cli shot AND the binary is present.
    higgsfield_cli: HiggsfieldCli | None = None
    needs_higgsfield = any(
        s.generator is Generator.HIGGSFIELD_CLI for s in sb.shots
    )
    if needs_higgsfield:
        try:
            higgsfield_cli = HiggsfieldCli()
        except HiggsfieldCliError as e:
            print(f"ERROR: storyboard uses higgsfield_cli but: {e}")
            return 1

    # PHASE 1 — Stills (Gemini per-shot)
    print("\n── PHASE 1 · Stills (Gemini Nano Banana Pro)")
    for shot in sb.shots:
        still = args.workdir / f"{shot.shot_id}_image.jpg"
        if args.skip_stills and still.exists():
            print(f"  📦 reusing {still.name}")
            continue
        refs = resolve_refs(
            shot.visual_reference_lock,
            workdir=args.workdir,
            characters_dir=args.character_workdir,
            product_refs_dir=args.product_refs_dir,
        )
        print(f"  {shot.shot_id}: refs=[{', '.join(p.name for p in refs)}] · prompt {len(shot.image_prompt)} chars")
        try:
            await gemini_still(client=gemini, shot=shot, dest=still, refs=refs)
            print(f"    ✅ {still.name} ({still.stat().st_size//1024} KB)")
        except Exception as e:
            print(f"    ❌ {e}")
            return 2

    # PHASE 2 — Per-shot clips
    print("\n── PHASE 2 · Shot rendering")
    shot_clips: dict[str, Path] = {}
    for shot in sb.shots:
        still = args.workdir / f"{shot.shot_id}_image.jpg"
        clip = args.workdir / f"{shot.shot_id}_clip.mp4"
        shot_clips[shot.shot_id] = clip
        if args.skip_shots and clip.exists():
            print(f"  📦 reusing {clip.name}")
            continue
        print(f"  {shot.shot_id} [{shot.generator.value}] {shot.duration_s}s · audio={shot.audio_source.value}")
        if shot.generator is Generator.HOLD:
            vo_wav: Path | None = None
            if shot.audio_source is AudioSource.PHAYA_TTS and shot.dialogue_th:
                vo_wav = args.workdir / f"{shot.shot_id}_vo.wav"
                if not vo_wav.exists():
                    print(f"   ↳ Thai TTS ({args.tts_source}): {shot.dialogue_th!r}")
                    await thai_tts_wav(
                        client=phaya, gcs=gcs, text=shot.dialogue_th, dest=vo_wav,
                        source=args.tts_source, voice=args.tts_voice,
                    )
                else:
                    print(f"   ↳ reusing {vo_wav.name}")
            hold_to_mp4(still, clip, shot.duration_s, voiceover_wav=vo_wav)
        elif shot.generator is Generator.SEEDANCE_2KF:
            await run_seedance_2kf(
                phaya=phaya, gcs=gcs, key_prefix=args.key_prefix,
                shot=shot, workdir=args.workdir, dest=clip,
            )
        elif shot.generator is Generator.HIGGSFIELD_CLI:
            if higgsfield_cli is None:  # pragma: no cover — guarded above
                print(f"    ❌ higgsfield_cli unavailable for {shot.shot_id}")
                return 5
            await run_higgsfield_cli(
                hf=higgsfield_cli, shot=shot, still=still,
                workdir=args.workdir, dest=clip,
            )
        elif shot.generator in (Generator.SEEDANCE_2_FAST, Generator.SEEDANCE_2_PRO):
            if seedance2 is None:
                print(f"    ❌ {shot.shot_id}: {shot.generator.value} requires "
                      f"PIAPI_API_KEY in .env — set it and re-run with --skip-shots "
                      f"to resume from cached upstream shots.")
                return 4
            variant = "fast" if shot.generator is Generator.SEEDANCE_2_FAST else "pro"
            await run_seedance_2_2kf(
                seedance2=seedance2, gcs=gcs, key_prefix=args.key_prefix,
                shot=shot, workdir=args.workdir, dest=clip, variant=variant,
            )
        else:
            print(f"    ⚠️  generator {shot.generator.value} not wired in this orchestrator")
            continue
        dur = ffprobe_duration(clip)
        print(f"    ✅ {clip.name} ({clip.stat().st_size // 1024} KB · {dur:.2f}s)")

    # PHASE 3 — Concat
    print("\n── PHASE 3 · Concat")
    ordered = [shot_clips[s.shot_id] for s in sb.shots if shot_clips[s.shot_id].exists()]
    concat_mp4 = args.workdir / "concat.mp4"
    concat_clips(ordered, args.workdir, concat_mp4)
    print(f"  ✅ {concat_mp4.name} ({concat_mp4.stat().st_size // 1024} KB · {ffprobe_duration(concat_mp4):.2f}s)")

    # PHASE 4 — Music
    print(f"\n── PHASE 4 · Music ({sb.music_duration_s}s)")
    music_local = args.workdir / "music.mp3"
    if not music_local.exists():
        submit = await phaya.create_music(prompt=sb.music_prompt, duration_s=int(sb.music_duration_s))
        if not submit.ok or submit.data is None:
            raise RuntimeError(f"music submit failed: {submit.error}")
        wait = await phaya._wait(
            poller=phaya.get_music_status, job_id=submit.data.job_id,
            interval=4.0, timeout=300.0,
        )
        if not (wait.ok and wait.data and wait.data.state is JobState.COMPLETED and wait.data.result_url):
            raise RuntimeError(f"music render failed: {wait.error if wait else 'unknown'}")
        m_url = wait.data.result_url
        if m_url.startswith(f"gs://{gcs.bucket_name}/"):
            k = m_url[len(f"gs://{gcs.bucket_name}/"):]
            m_url = await asyncio.to_thread(gcs.signed_url, k, ttl=timedelta(hours=1))
        async with httpx.AsyncClient(timeout=httpx.Timeout(180.0)) as c:
            r = await c.get(m_url); r.raise_for_status()
            music_local.write_bytes(r.content)
        print(f"  ✅ {music_local.name}")
    else:
        print(f"  📦 reusing {music_local.name}")
    mixed_mp4 = args.workdir / "mixed.mp4"
    mix_music_under(concat_mp4, music_local, mixed_mp4, gain_db=-12.0)

    # PHASE 5 — Subtitles via HyperFrames
    print("\n── PHASE 5 · Subtitle overlays")
    # Compute per-shot global offsets
    offsets: dict[str, float] = {}
    t = 0.0
    for s in sb.shots:
        offsets[s.shot_id] = t
        t += ffprobe_duration(shot_clips[s.shot_id])
    overlays = build_subtitle_overlays(sb, offsets)
    if overlays:
        ov_workdir = args.workdir / "overlays"
        ov_workdir.mkdir(parents=True, exist_ok=True)
        rendered = render_storyboard_overlays(
            overlays=overlays, projects_dir=Path("hyperframes"), output_dir=ov_workdir,
        )
        print(f"  ✅ rendered {len(rendered)} overlay(s)")
        composite_overlays_with_ffmpeg(base_video=mixed_mp4, overlays=rendered, output=args.output)
    else:
        mixed_mp4.replace(args.output)

    print(f"\n✅ {args.output} ({args.output.stat().st_size // 1024 // 1024} MB · {ffprobe_duration(args.output):.2f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
