#!/usr/bin/env python
"""Orchestrate an AiStoryboard v2 → finished video.

Phases:
  1. Resolve every shot's visual_reference_lock to local paths
  2. Render the scene still for each shot via Gemini Nano Banana Pro
     (with image_prompt + refs + negatives wired in)
  3. Dispatch each shot to its declared generator:
       hold             → ffmpeg loops the still for shot.duration_s
       heygen_avatar_iv → Phaya TTS → HeyGen Avatar IV → download
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
import json
import os
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

import httpx
from pydantic import SecretStr

from auto_affi.adapters.gcs_storage import GcsStorage
from auto_affi.adapters.gemini_image import GEMINI_NANO_BANANA_PRO, GeminiImageClient, write_image_to_path
from auto_affi.adapters.heygen import HeyGenClient, HeyGenError
from auto_affi.adapters.phaya import PhayaClient, JobState
from auto_affi.post.hyperframes_renderer import (
    OverlayRender, composite_overlays_with_ffmpeg, render_storyboard_overlays,
)
from auto_affi.schemas.ai_storyboard import (
    AiStoryboard, AiShot, AudioSource, Generator, SubtitlePlacement,
)
from auto_affi.schemas.storyboard import HyperframeOverlay


def _aac_flags() -> list[str]:
    return ["-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2"]


def _ffprobe_duration(p: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(p)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def _resolve_refs(
    refs: list[str], *, workdir: Path, characters_dir: Path, product_refs_dir: Path,
) -> list[Path]:
    """Resolve string refs from the storyboard to absolute paths."""
    out: list[Path] = []
    for r in refs:
        if r.startswith("characters/"):
            p = characters_dir / r.removeprefix("characters/")
        elif r.startswith("product-refs/"):
            p = product_refs_dir / r.removeprefix("product-refs/")
        else:
            # sN_image.jpg lives in workdir
            p = workdir / r
        if not p.exists():
            raise FileNotFoundError(f"ref not found: {r} → {p}")
        out.append(p)
    return out


async def _gemini_still(
    *, client: GeminiImageClient, shot: AiShot, dest: Path, refs: list[Path],
) -> None:
    """Generate the shot's reference still via Gemini Nano Banana Pro.
    Negatives are appended to the image_prompt with explicit phrasing."""
    neg = " ".join(f"DO NOT: {n}." for n in shot.negatives)
    prompt = f"{shot.image_prompt}\n\nStrict negatives — {neg}"
    r = await client.create_image(
        prompt=prompt,
        aspect_ratio=shot.aspect_ratio,
        reference_images=refs if refs else None,
    )
    if not r.ok or r.data is None:
        raise RuntimeError(f"gemini still failed for {shot.shot_id}: {r.error[:300]}")
    write_image_to_path(r.data, dest)


def _hold_to_mp4(still: Path, dest: Path, duration_s: float, *, fps: int = 24) -> None:
    """Loop a still into an mp4 of the requested duration with silent audio."""
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-loop", "1", "-i", str(still),
         "-f", "lavfi", "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100",
         "-t", f"{duration_s:.3f}", "-r", str(fps),
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p",
         *_aac_flags(), "-shortest",
         str(dest)],
        check=True,
    )


def _normalize_mp4(src: Path, dest: Path, *, target_duration_s: float | None = None) -> None:
    """Re-encode to canonical params so concat is gapless. Optionally
    pad / trim to a target duration."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src)]
    af = ["apad"] if target_duration_s else []
    if af:
        cmd += ["-af", ",".join(af)]
    cmd += [
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        *_aac_flags(),
    ]
    if target_duration_s is not None:
        cmd += ["-t", f"{target_duration_s:.3f}"]
    cmd += [str(dest)]
    subprocess.run(cmd, check=True)


def _pad_audio(src: Path, dest: Path, target_s: float) -> None:
    cur = _ffprobe_duration(src)
    if cur >= target_s - 0.01:
        dest.write_bytes(src.read_bytes())
        return
    pad = target_s - cur
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
         "-af", f"apad=pad_dur={pad:.3f}",
         "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "1", str(dest)],
        check=True,
    )


async def _phaya_tts_wav(*, client: PhayaClient, gcs: GcsStorage, text: str, dest: Path) -> Path:
    submit = await client.create_tts(prompt=text, voice="Algenib", language="th")
    if not submit.ok or submit.data is None:
        raise RuntimeError(f"phaya TTS submit failed: {submit.error}")
    wait = await client._wait(
        poller=client.get_tts_status, job_id=submit.data.job_id,
        interval=3.0, timeout=240.0,
    )
    if not (wait.ok and wait.data and wait.data.state is JobState.COMPLETED and wait.data.result_url):
        raise RuntimeError(f"phaya TTS render failed: {wait.error if wait else 'unknown'}")
    url = wait.data.result_url
    if url.startswith(f"gs://{gcs.bucket_name}/"):
        key = url[len(f"gs://{gcs.bucket_name}/"):]
        url = await asyncio.to_thread(gcs.signed_url, key, ttl=timedelta(hours=1))
    dest.parent.mkdir(parents=True, exist_ok=True)
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as c:
        r = await c.get(url); r.raise_for_status()
        dest.write_bytes(r.content)
    return dest


async def _run_heygen_avatar_iv(
    *, heygen: HeyGenClient, phaya: PhayaClient, gcs: GcsStorage,
    shot: AiShot, still: Path, dest: Path, workdir: Path,
) -> None:
    """Phaya TTS → HeyGen Avatar IV → save."""
    if not shot.dialogue_th:
        raise RuntimeError(f"{shot.shot_id}: heygen requires dialogue_th")

    tts_wav = workdir / f"{shot.shot_id}_tts.wav"
    print(f"   ↳ Phaya TTS: {shot.dialogue_th!r}")
    await _phaya_tts_wav(client=phaya, gcs=gcs, text=shot.dialogue_th, dest=tts_wav)
    padded = workdir / f"{shot.shot_id}_tts_padded.wav"
    _pad_audio(tts_wav, padded, shot.duration_s)
    print(f"   ↳ uploading still + audio to HeyGen")
    img = await heygen.upload_asset(still)
    aud = await heygen.upload_asset(padded)
    print(f"   ↳ HeyGen Avatar IV: render")
    job = await heygen.create_video_from_image(
        image_asset_id=img.asset_id,
        audio_asset_id=aud.asset_id,
        aspect_ratio=shot.aspect_ratio,
        resolution="720p",
        motion_prompt=shot.motion_prompt or "subtle natural reading expression, no head turn",
        expressiveness=shot.expressiveness or "medium",
    )
    completed = await heygen.wait_for_video(job.video_id, interval_s=4.0, timeout_s=600.0)
    raw = workdir / f"{shot.shot_id}_heygen_raw.mp4"
    await heygen.download_video(completed.video_url, raw)
    # Normalize to canonical AAC params + cap to declared duration
    _normalize_mp4(raw, dest, target_duration_s=shot.duration_s)


async def _run_seedance_2kf(
    *, phaya: PhayaClient, gcs: GcsStorage, key_prefix: str,
    shot: AiShot, workdir: Path, dest: Path,
) -> None:
    """Two-keyframe Seedance i2v: requires shot.keyframes.start_ref + end_ref
    to exist as local stills in the workdir."""
    if shot.keyframes is None:
        raise RuntimeError(f"{shot.shot_id}: seedance_2kf requires keyframes block")
    start_local = workdir / shot.keyframes.start_ref
    end_local = workdir / shot.keyframes.end_ref
    for p in (start_local, end_local):
        if not p.exists():
            raise RuntimeError(f"{shot.shot_id}: keyframe missing: {p}")

    print(f"   ↳ Seedance 2kf · motion={shot.keyframes.motion_label!r}")
    start_key = f"{key_prefix}/{shot.shot_id}_start.jpg"
    end_key = f"{key_prefix}/{shot.shot_id}_end.jpg"

    def _upload(local: Path, key: str) -> tuple[str, str]:
        asset = gcs.upload_file(local, key=key, content_type="image/jpeg",
                                cache_control="public, max-age=3600")
        url = gcs.signed_url(key, ttl=timedelta(hours=1))
        return asset.gs_uri, url

    _, start_signed = await asyncio.to_thread(_upload, start_local, start_key)
    _, end_signed = await asyncio.to_thread(_upload, end_local, end_key)
    # Pick Seedance duration from {4, 8, 12} — cap to the shot's declared duration
    seedance_dur = "4" if shot.duration_s <= 5.0 else "8" if shot.duration_s <= 10.0 else "12"
    submit = await phaya.create_seedance_video(
        shot.keyframes.motion_label,
        input_urls=[start_signed, end_signed],
        aspect_ratio=shot.aspect_ratio,
        resolution="720p",
        duration=seedance_dur,
        generate_audio=False,
        fixed_lens=False,
    )
    if not submit.ok or submit.data is None:
        raise RuntimeError(f"{shot.shot_id}: seedance submit failed: {submit.error}")
    wait = await phaya._wait(
        poller=phaya.get_seedance_status, job_id=submit.data.job_id,
        interval=4.0, timeout=480.0,
    )
    if not (wait.ok and wait.data and wait.data.state is JobState.COMPLETED and wait.data.result_url):
        raise RuntimeError(f"{shot.shot_id}: seedance failed: {wait.error if wait else 'unknown'}")
    url = wait.data.result_url
    if url.startswith(f"gs://{gcs.bucket_name}/"):
        k = url[len(f"gs://{gcs.bucket_name}/"):]
        url = await asyncio.to_thread(gcs.signed_url, k, ttl=timedelta(hours=1))
    raw = workdir / f"{shot.shot_id}_seedance_raw.mp4"
    async with httpx.AsyncClient(timeout=httpx.Timeout(180.0)) as c:
        r = await c.get(url); r.raise_for_status()
        raw.write_bytes(r.content)
    _normalize_mp4(raw, dest, target_duration_s=shot.duration_s)


def _concat(clips: list[Path], workdir: Path, out: Path) -> None:
    listfile = workdir / "concat.txt"
    listfile.write_text("\n".join(f"file '{p.resolve()}'" for p in clips))
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(listfile), "-c", "copy", str(out)],
        check=True,
    )


def _mix_music_under(video: Path, music: Path, out: Path, *, gain_db: float = -12.0) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-i", str(video), "-i", str(music),
         "-filter_complex",
         f"[1:a]volume={gain_db}dB[m];[0:a][m]amix=inputs=2:duration=longest:dropout_transition=0[mix]",
         "-map", "0:v", "-map", "[mix]",
         "-c:v", "copy", *_aac_flags(), "-shortest", str(out)],
        check=True,
    )


def _build_subtitle_overlays(sb: AiStoryboard, shot_offsets: dict[str, float]) -> list[HyperframeOverlay]:
    """Map each shot's subtitle to a HyperframeOverlay on the global timeline."""
    overlays: list[HyperframeOverlay] = []
    for i, shot in enumerate(sb.shots):
        if shot.subtitle is None:
            continue
        sub = shot.subtitle
        global_start = shot_offsets[shot.shot_id] + sub.start_offset_s
        dur = sub.duration_s if sub.duration_s is not None else shot.duration_s
        template = "dialogue-subtitle-upper" if sub.placement is SubtitlePlacement.UPPER_THIRD else "dialogue-subtitle"
        overlays.append(HyperframeOverlay(
            scene_idx=i, template=template,
            props={
                "text_th": sub.text_th,
                "start_s": global_start,
                "duration_s": dur,
            },
        ))
    return overlays


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
    args = p.parse_args()

    # Env
    for k in ("PHAYA_API_KEY", "HEYGEN_API_KEY", "GOOGLE_API_KEY", "AUTO_AFFI__GCS_BUCKET"):
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
    heygen = HeyGenClient(api_key=SecretStr(os.environ["HEYGEN_API_KEY"]), timeout_s=120.0)

    # PHASE 1 — Stills (Gemini per-shot)
    print("\n── PHASE 1 · Stills (Gemini Nano Banana Pro)")
    for shot in sb.shots:
        still = args.workdir / f"{shot.shot_id}_image.jpg"
        if args.skip_stills and still.exists():
            print(f"  📦 reusing {still.name}")
            continue
        refs = _resolve_refs(
            shot.visual_reference_lock,
            workdir=args.workdir,
            characters_dir=args.character_workdir,
            product_refs_dir=args.product_refs_dir,
        )
        print(f"  {shot.shot_id}: refs=[{', '.join(p.name for p in refs)}] · prompt {len(shot.image_prompt)} chars")
        try:
            await _gemini_still(client=gemini, shot=shot, dest=still, refs=refs)
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
        print(f"  {shot.shot_id} [{shot.generator.value}] {shot.duration_s}s")
        if shot.generator is Generator.HOLD:
            _hold_to_mp4(still, clip, shot.duration_s)
        elif shot.generator is Generator.HEYGEN_AVATAR_IV:
            await _run_heygen_avatar_iv(
                heygen=heygen, phaya=phaya, gcs=gcs,
                shot=shot, still=still, dest=clip, workdir=args.workdir,
            )
        elif shot.generator is Generator.SEEDANCE_2KF:
            await _run_seedance_2kf(
                phaya=phaya, gcs=gcs, key_prefix=args.key_prefix,
                shot=shot, workdir=args.workdir, dest=clip,
            )
        else:
            print(f"    ⚠️  generator {shot.generator.value} not wired in this orchestrator")
            continue
        dur = _ffprobe_duration(clip)
        print(f"    ✅ {clip.name} ({clip.stat().st_size // 1024} KB · {dur:.2f}s)")

    # PHASE 3 — Concat
    print("\n── PHASE 3 · Concat")
    ordered = [shot_clips[s.shot_id] for s in sb.shots if shot_clips[s.shot_id].exists()]
    concat_mp4 = args.workdir / "concat.mp4"
    _concat(ordered, args.workdir, concat_mp4)
    print(f"  ✅ {concat_mp4.name} ({concat_mp4.stat().st_size // 1024} KB · {_ffprobe_duration(concat_mp4):.2f}s)")

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
    _mix_music_under(concat_mp4, music_local, mixed_mp4, gain_db=-12.0)

    # PHASE 5 — Subtitles via HyperFrames
    print("\n── PHASE 5 · Subtitle overlays")
    # Compute per-shot global offsets
    offsets: dict[str, float] = {}
    t = 0.0
    for s in sb.shots:
        offsets[s.shot_id] = t
        t += _ffprobe_duration(shot_clips[s.shot_id])
    overlays = _build_subtitle_overlays(sb, offsets)
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

    print(f"\n✅ {args.output} ({args.output.stat().st_size // 1024 // 1024} MB · {_ffprobe_duration(args.output):.2f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
