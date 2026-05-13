#!/usr/bin/env python3
"""Two-keyframe video generation via Phaya Seedance 1.5 Pro — between-scenes.

Per-clip workflow:
    clip N = approved still N as START + approved still N+1 as END
    7 stills → 6 clips. Each clip morphs from one approved scene
    composition to the next via Seedance's first-last-frame
    interpolation. No within-scene end-frame generation needed.

1. Read approved start (workdir/s{N}-image.jpg) and end (s{N+1}-image.jpg)
2. Upload both to GCS, sign URLs
3. Call Phaya Seedance with input_urls=[start_url, end_url], 9:16,
   duration from storyboard
4. Download clip, trim to target duration, mux with TTS if dialogue

After all clips done: concat + music mix + register run + upload final.

Usage:
    .venv/bin/python scripts/gen-video-seedance.py \\
        --item-id 28875679676 \\
        --storyboard-json data/registry/items/28875679676/concept-2-storyboard.json \\
        --workdir out/maono-concept-2-workdir \\
        --output  out/maono-concept-2-seedance.mp4 \\
        --music-prompt "<music prompt>" \\
        --clips 0                               # smoke test 1 clip first

Smoke-test pattern: --clips 0 (single clip = s0→s1) ~฿4-8. Then --clips all.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
import uuid
from datetime import timedelta
from pathlib import Path

import httpx
from pydantic import SecretStr

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from auto_affi.adapters.phaya import JobState, PhayaClient
from auto_affi.registry import build_run_prefix, registry_from_env

try:
    from auto_affi.adapters.gcs_storage import GcsStorage
except ImportError:
    GcsStorage = None  # type: ignore[assignment]


# Map storyboard camera_movement field → minimal Seedance motion prompt.
# Per Kling/Higgsfield best practice: minimal motion verbs; let the model infer.
def _seedance_motion_prompt(camera_movement: str | None, duration_s: float) -> str:
    if not camera_movement:
        return ""
    m = camera_movement.lower()
    if "static" in m and "rack-focus" not in m and "rack focus" not in m:
        return "static shot, locked-off camera"
    if "rack-focus" in m or "rack focus" in m:
        return "rack focus pull from foreground to background"
    if "dolly-in" in m or "dolly in" in m or "push-in" in m or "push in" in m:
        return "slow dolly in"
    if "pull-back" in m or "pull back" in m or "pull-out" in m:
        return "slow pull back"
    if "tilt up" in m:
        return "slow tilt up"
    if "tilt down" in m:
        return "slow tilt down"
    if "pan" in m:
        return "slow pan"
    if "handheld" in m or "tremor" in m:
        return "subtle handheld motion"
    if "match-cut" in m or "match cut" in m:
        return "subtle push in"
    return camera_movement


# Map storyboard duration_s → Seedance enum duration string ("4", "8", "12").
def _seedance_duration(target_s: float) -> str:
    # Pick the smallest valid duration that is >= target so we can trim
    if target_s <= 4.0:
        return "4"
    if target_s <= 8.0:
        return "8"
    return "12"


def _end_state_prompt(
    *,
    motion_label: str,
    visual_prompt: str,
) -> str:
    """Build an end-frame prompt from the camera_movement intent.

    The Nano Banana 2 call uses ``image_input=[start_url]`` for consistency,
    so we only specify the COMPOSITIONAL DIFFERENCE — the rest carries
    over from the start frame via image conditioning.
    """
    m = motion_label.lower()
    # Anti-anatomy guard preserved
    anatomy_guard = (
        " Anatomically correct human anatomy: exactly two hands visible if "
        "hands are in frame, five fingers per hand, no extra limbs, no extra "
        "body parts, no duplicate features."
    )
    base = (
        "Same scene, same character, same lighting and color palette as the "
        "reference image. Maintain character identity, outfit, and pose family. "
    )
    if "static" in m and "rack-focus" not in m:
        return base + "Minimal change — slightly different micro-expression or breath." + anatomy_guard
    if "rack-focus" in m or "rack focus" in m:
        return base + "Same composition but focus has shifted: previously out-of-focus subject is now sharp, previously sharp subject is now out of focus." + anatomy_guard
    if "dolly-in" in m or "dolly in" in m or "push-in" in m or "push in" in m:
        return base + "Camera has dollied closer to the subject; subject now fills more of the frame, fewer surrounding details visible." + anatomy_guard
    if "pull-back" in m or "pull back" in m or "pull-out" in m:
        return base + "Camera has pulled back to a wider shot; subject is smaller, more surrounding context visible." + anatomy_guard
    if "tilt up" in m:
        return base + "Camera has tilted up; framing is now higher in the scene." + anatomy_guard
    if "tilt down" in m:
        return base + "Camera has tilted down; framing is now lower in the scene." + anatomy_guard
    if "pan" in m:
        return base + "Camera has panned to reveal a slightly different part of the scene." + anatomy_guard
    return base + f"End state of the motion: {motion_label}." + anatomy_guard


async def _upload_to_gcs(
    gcs: "GcsStorage", *, local_path: Path, key: str, content_type: str
) -> tuple[str, str]:
    """Upload file, return (gs_uri, 1-hour signed URL for Phaya consumption)."""
    asset = await asyncio.to_thread(
        gcs.upload_file, local_path, key=key, content_type=content_type,
        cache_control="public, max-age=3600",
    )
    url = await asyncio.to_thread(gcs.signed_url, key, ttl=timedelta(hours=1))
    return asset.gs_uri, url


async def _download(url: str, dest: Path) -> None:
    async with httpx.AsyncClient(timeout=180.0, follow_redirects=True) as c:
        r = await c.get(url)
        r.raise_for_status()
        dest.write_bytes(r.content)


def _trim_clip(src: Path, dst: Path, *, duration_s: float) -> None:
    """Trim a clip to duration_s seconds via ffmpeg copy codec (fast, no re-encode)."""
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
         "-t", f"{duration_s:.3f}", "-c", "copy", str(dst)],
        check=True,
    )


# Uniform AAC params for every per-clip mux. CRITICAL for ``-f concat -c copy``
# downstream — if individual clips have mismatched profile / sample-rate /
# channel-count, the demuxer concat produces a broken AAC bytestream at clip
# boundaries and ``ffmpeg -i ... -f null -`` rejects it with a flood of
# "decode_pce: Input buffer exhausted" / "channel element X.X is not allocated"
# errors. Pin everything to: AAC LC · 192k bps · 44100 Hz · stereo.
_AAC_BITRATE = "192k"
_AAC_SAMPLE_RATE = "44100"
_AAC_CHANNELS = "2"


def _aac_flags() -> list[str]:
    return [
        "-c:a", "aac",
        "-b:a", _AAC_BITRATE,
        "-ar", _AAC_SAMPLE_RATE,
        "-ac", _AAC_CHANNELS,
    ]


def _mux_with_audio(video: Path, audio: Path | None, out: Path) -> None:
    """Mux a video with an audio track using uniform AAC params.

    When ``audio`` is None: synthesises a silent stereo track via
    ``anullsrc`` for the full video duration.

    When ``audio`` is shorter than the video, the audio is padded with
    silence via the ``apad`` filter so the END of the video keyframe is
    preserved (the prior ``-shortest`` cut the VIDEO to TTS length when
    TTS was shorter, which killed Seedance's convergence to s[N+1]).
    """
    if audio is None:
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(video),
             "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
             "-map", "0:v", "-map", "1:a",
             "-c:v", "copy", *_aac_flags(), "-shortest", str(out)],
            check=True,
        )
    else:
        # Pad audio with silence (apad) so it's always ≥ video duration.
        # Then -shortest caps the final to video duration → video wins.
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(video), "-i", str(audio),
             "-filter_complex", "[1:a]apad[a]",
             "-map", "0:v", "-map", "[a]",
             "-c:v", "copy", *_aac_flags(), "-shortest", str(out)],
            check=True,
        )


def _concat(clips: list[Path], workdir: Path, out: Path) -> None:
    listfile = workdir / "concat-seedance.txt"
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
         f"[1:a]volume={gain_db}dB[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0[aout]",
         "-map", "0:v", "-map", "[aout]",
         "-c:v", "copy", *_aac_flags(), "-shortest", str(out)],
        check=True,
    )


def _parse_scenes(arg: str, total: int) -> list[int]:
    if arg == "all":
        return list(range(total))
    return [int(x.strip()) for x in arg.split(",") if x.strip()]


async def process_clip(
    *,
    client: PhayaClient,
    gcs: "GcsStorage",
    clip_idx: int,
    start_scene_idx: int,
    end_scene_idx: int,
    target_duration_s: float,
    motion_label: str,
    dialogue_th: str,
    workdir: Path,
    order_no: int,
    run_no: int,
    resolution: str,
    rich_prompt: str | None = None,
    rich_duration_str: str | None = None,
    generate_audio: bool = False,
) -> dict | None:
    """Generate one Seedance clip between approved stills s[start]→s[end].

    No end-frame regeneration — uses the already-approved stills as the
    two keyframes. Seedance interpolates the motion between them.
    """
    print(f"\n── clip {clip_idx}: s{start_scene_idx} → s{end_scene_idx} "
          f"({target_duration_s}s) · camera={motion_label or '—'}")

    start_local = workdir / f"s{start_scene_idx}-image.jpg"
    end_local = workdir / f"s{end_scene_idx}-image.jpg"
    if not start_local.exists():
        print(f"   ❌ start frame missing at {start_local}")
        return None
    if not end_local.exists():
        print(f"   ❌ end frame missing at {end_local}")
        return None

    key_prefix = build_run_prefix(order_no, run_no)

    # 1. Upload both keyframes → signed URLs Phaya can fetch
    print(f"   1/3 uploading start + end keyframes…")
    start_key = f"{key_prefix}/stage4-visuals/clip_{clip_idx}_start_s{start_scene_idx}.jpg"
    end_key = f"{key_prefix}/stage4-visuals/clip_{clip_idx}_end_s{end_scene_idx}.jpg"
    start_gs, start_signed = await _upload_to_gcs(
        gcs, local_path=start_local, key=start_key, content_type="image/jpeg",
    )
    end_gs, end_signed = await _upload_to_gcs(
        gcs, local_path=end_local, key=end_key, content_type="image/jpeg",
    )

    # 2. Seedance two-keyframe i2v
    if rich_prompt is not None and rich_duration_str is not None:
        seedance_duration = rich_duration_str
        final_prompt = rich_prompt
        print(f"   2/3 Seedance i2v ({seedance_duration}s requested → trim to {target_duration_s:.1f}s) · "
              f"rich prompt ({len(final_prompt)} chars) · audio={generate_audio}")
    else:
        seedance_duration = _seedance_duration(target_duration_s)
        final_prompt = _seedance_motion_prompt(motion_label, target_duration_s) or "smooth cinematic transition"
        print(f"   2/3 Seedance i2v ({seedance_duration}s requested → trim to {target_duration_s:.1f}s) · "
              f"prompt: {final_prompt!r} · audio={generate_audio}")
    submit = await client.create_seedance_video(
        prompt=final_prompt,
        input_urls=[start_signed, end_signed],
        aspect_ratio="9:16",
        resolution=resolution,
        duration=seedance_duration,
        fixed_lens=False,
        generate_audio=generate_audio,
    )
    if not submit.ok or submit.data is None:
        print(f"   ❌ Seedance submit failed: {submit.error}")
        return None
    wait = await client.wait_for_seedance(submit.data.job_id)
    if not wait.ok or wait.data is None or wait.data.state is not JobState.COMPLETED:
        print(f"   ❌ Seedance render failed: {wait.error or (wait.data.state if wait.data else '?')}")
        return None
    if not wait.data.result_url:
        print("   ❌ Seedance completed but no result_url")
        return None

    # 3. Download. KEYFRAME INTEGRITY RULE: do NOT trim. Seedance converges
    # to the end keyframe over the FULL declared duration ("4" / "8" / "12");
    # trimming the tail cuts the convergence and the clip ends mid-motion
    # instead of on the intended s[N+1] composition. We keep the full
    # output; total runtime is variable but each clip ends on its end_image.
    raw_clip = workdir / f"clip{clip_idx}-seedance-raw.mp4"
    if wait.data.result_url.startswith(f"gs://{gcs.bucket_name}/"):
        raw_key = wait.data.result_url[len(f"gs://{gcs.bucket_name}/"):]
        signed = await asyncio.to_thread(gcs.signed_url, raw_key, ttl=timedelta(hours=1))
        await _download(signed, raw_clip)
    else:
        await _download(wait.data.result_url, raw_clip)
    trimmed_clip = raw_clip  # alias for downstream — no trim performed

    final_clip = workdir / f"clip{clip_idx}-seedance-final.mp4"
    audio_path: Path | None = None  # populated only on the no-Seedance-audio path
    if generate_audio:
        # Seedance produced the audio; re-encode audio to AAC with the
        # uniform params (192k/44100/stereo) so this clip's audio matches
        # silent / TTS clips byte-for-byte at concat time.
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(trimmed_clip),
             "-c:v", "copy", *_aac_flags(), str(final_clip)],
            check=True,
        )
    else:
        # No Seedance audio — fall back to TTS for dialogue clips, silence otherwise
        if dialogue_th.strip():
            print(f"   3/3 TTS: {dialogue_th!r}")
            tts_submit = await client.create_tts(
                prompt=dialogue_th, voice="Algenib", language="th"
            )
            if tts_submit.ok and tts_submit.data is not None:
                tts_wait = await client._wait(
                    poller=client.get_tts_status,
                    job_id=tts_submit.data.job_id,
                    interval=3.0, timeout=240.0,
                )
                if (tts_wait.ok and tts_wait.data and tts_wait.data.state is JobState.COMPLETED
                        and tts_wait.data.result_url):
                    audio_path = workdir / f"clip{clip_idx}-seedance-audio.wav"
                    url = tts_wait.data.result_url
                    if url.startswith(f"gs://{gcs.bucket_name}/"):
                        a_key = url[len(f"gs://{gcs.bucket_name}/"):]
                        a_signed = await asyncio.to_thread(gcs.signed_url, a_key, ttl=timedelta(hours=1))
                        await _download(a_signed, audio_path)
                    else:
                        await _download(url, audio_path)
        _mux_with_audio(trimmed_clip, audio_path, final_clip)

    cost_thb = (wait.data.cost_thb or 0.0)
    print(f"   ✅ clip done · {final_clip.name} · scene cost ฿{cost_thb:.4f}")
    return {
        "clip_path": final_clip,
        "cost_thb": cost_thb,
        "start_gs": start_gs,
        "end_gs": end_gs,
        "raw_clip": raw_clip,
        "trimmed_clip": trimmed_clip,
        "audio_path": audio_path,
    }


async def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--item-id", type=int, required=True)
    p.add_argument("--storyboard-json", type=Path, required=True)
    p.add_argument("--workdir", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--clips", type=str, default="all",
                   help="'all' or comma-separated CLIP indices (e.g. '0' for smoke test). "
                        "Clip N uses s[N] as start, s[N+1] as end. 7 stills → 6 clips (0..5).")
    p.add_argument("--resolution", type=str, default="720p",
                   choices=["480p", "720p", "1080p"])
    p.add_argument("--music-prompt", type=str, default=None)
    p.add_argument("--music-duration", type=int, default=30)
    p.add_argument("--music-mix-db", type=float, default=-12.0)
    p.add_argument(
        "--clip-prompts-json",
        type=Path,
        default=None,
        help="Path to detailed per-clip prompts JSON. If set, overrides "
             "the camera_movement-based simple motion prompts and enables "
             "generate_audio=true (Seedance produces foley/dialogue audio).",
    )
    p.add_argument(
        "--generate-audio",
        action="store_true",
        help="Enable Seedance's diegetic audio generation per clip.",
    )
    args = p.parse_args()

    key = os.environ.get("PHAYA_API_KEY", "").strip()
    if not key:
        print("ERROR: PHAYA_API_KEY missing"); return 1
    bucket = os.environ.get("AUTO_AFFI__GCS_BUCKET", "").strip()
    if not bucket or GcsStorage is None:
        print("ERROR: GCS bucket required for two-keyframe mode (Phaya needs signed URLs)")
        return 1

    sb = json.loads(args.storyboard_json.read_text(encoding="utf-8"))
    frames = sb["frames"]
    n_stills = len(frames)
    n_clips = n_stills - 1  # between-scenes: clip N = (s[N], s[N+1])

    # Optional rich-prompt config — overrides camera_movement-based simple prompts
    rich_prompts: dict[int, dict] = {}
    if args.clip_prompts_json is not None:
        rich = json.loads(args.clip_prompts_json.read_text(encoding="utf-8"))
        for entry in rich.get("clips", []):
            rich_prompts[int(entry["clip_idx"])] = entry
        print(f"📝 rich prompts: loaded {len(rich_prompts)} from {args.clip_prompts_json}")

    # Build the clip plan: target durations + camera labels + dialogue.
    # Each clip = the transition INTO the end-scene, so duration + dialogue
    # come from the end-scene's storyboard entry. Camera label comes from
    # the end-scene's camera_movement (which describes the motion arriving
    # at that scene).
    clip_plan: list[dict] = []
    for clip_i in range(n_clips):
        end_scene = frames[clip_i + 1]
        clip_plan.append({
            "clip_idx": clip_i,
            "start_scene_idx": clip_i,
            "end_scene_idx": clip_i + 1,
            "target_duration_s": float(end_scene.get("duration_s", 5.0)),
            "motion_label": end_scene.get("camera_movement", "") or "",
            "dialogue_th": (end_scene.get("dialogue_th") or "").strip(),
        })

    indices = _parse_scenes(args.clips, n_clips)
    args.workdir.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Registry start_run
    registry = registry_from_env()
    entry = registry.find_product_by_item_id(args.item_id)
    if entry is None:
        print(f"ERROR: product not in registry: item_id={args.item_id}")
        return 1
    run_id = str(uuid.uuid4())[:12]
    run_entry = registry.start_run(
        order_no=entry.order_no, run_id=run_id, publish_mode="dry_run",
    )
    order_no, run_no = entry.order_no, run_entry.run_no
    print(f"📒 registry:  order_no={order_no:04d}  run_no={run_no:04d}  run_id={run_id}")
    print(f"🎬 engine:    Phaya Seedance 1.5 Pro (two-keyframe, between-scenes)")
    print(f"🎬 stills:    {n_stills}  ·  clips total: {n_clips}  ·  selected: {indices}")
    print(f"🎬 resolution:{args.resolution}")
    print(f"🎬 plan:")
    for cp in clip_plan:
        print(f"      clip {cp['clip_idx']}: s{cp['start_scene_idx']} → s{cp['end_scene_idx']}  "
              f"({cp['target_duration_s']}s) · {cp['motion_label'] or '—'} · "
              f"dialogue={cp['dialogue_th'] or '<silent>'}")

    gcs = GcsStorage(bucket_name=bucket)
    print(f"🪣 GCS:       gs://{gcs.bucket_name}/{build_run_prefix(order_no, run_no)}/")
    client = PhayaClient(
        api_key=SecretStr(key),
        timeout_s=60.0,
        gcs=gcs,
        gcs_key_prefix=build_run_prefix(order_no, run_no),
    )

    bal0 = await client.get_credits()
    print(f"📊 balance:   ฿{bal0.data.balance_thb:.4f}")

    # Process each clip
    results: dict[int, dict] = {}
    for idx in indices:
        if idx >= n_clips:
            continue
        cp = clip_plan[idx]
        rich = rich_prompts.get(idx)
        rich_prompt = rich.get("prompt") if rich else None
        rich_duration_str = rich.get("seedance_duration_str") if rich else None
        target_dur = float(rich.get("target_duration_s", cp["target_duration_s"])) if rich else cp["target_duration_s"]
        result = await process_clip(
            client=client, gcs=gcs,
            clip_idx=cp["clip_idx"],
            start_scene_idx=cp["start_scene_idx"],
            end_scene_idx=cp["end_scene_idx"],
            target_duration_s=target_dur,
            motion_label=cp["motion_label"],
            dialogue_th=cp["dialogue_th"],
            workdir=args.workdir,
            order_no=order_no, run_no=run_no,
            resolution=args.resolution,
            rich_prompt=rich_prompt,
            rich_duration_str=rich_duration_str,
            generate_audio=args.generate_audio,
        )
        if result is not None:
            results[idx] = result

    # Pick up cached clips from prior runs in the same workdir so subset
    # runs (--clips 1,2,3,4,5) can still concat against an existing clip 0.
    for ci in range(n_clips):
        cached = args.workdir / f"clip{ci}-seedance-final.mp4"
        if ci not in results and cached.exists():
            print(f"  📦 reusing cached {cached.name} for clip {ci}")
            results[ci] = {"clip_path": cached, "cost_thb": 0.0,
                           "raw_clip": cached, "trimmed_clip": cached,
                           "start_gs": "", "end_gs": "", "audio_path": None}

    if not results:
        print("\n❌ no scenes succeeded")
        registry.finalize_run(
            run_no=run_no, order_no=order_no, status="FAILED",
            last_decision="no-scenes-rendered",
        )
        return 3

    # If smoke-test (single scene), don't concat — output is the single trimmed clip with audio
    intermediate = args.workdir / "concat-seedance.mp4"
    if len(results) == 1:
        only = next(iter(results.values()))
        only["clip_path"].replace(intermediate)
    else:
        clips_in_order = [results[i]["clip_path"] for i in sorted(results.keys())]
        _concat(clips_in_order, args.workdir, intermediate)

    # Optional music
    music_path: Path | None = None
    if args.music_prompt:
        print(f"\n🎵 generating music ({args.music_duration}s)…")
        music_submit = await client.create_music(
            prompt=args.music_prompt, duration_s=args.music_duration
        )
        if music_submit.ok and music_submit.data is not None:
            music_wait = await client._wait(
                poller=client.get_music_status,
                job_id=music_submit.data.job_id,
                interval=4.0, timeout=300.0,
            )
            if (music_wait.ok and music_wait.data and music_wait.data.state is JobState.COMPLETED
                    and music_wait.data.result_url):
                music_path = args.workdir / "music-seedance.mp3"
                await _download(music_wait.data.result_url, music_path)
                print(f"   ✅ music ready")
            else:
                print(f"   ⚠️  music render failed")

    if music_path is not None:
        print(f"🎚️  mixing music under voice @ {args.music_mix_db} dB…")
        _mix_music_under(intermediate, music_path, args.output, gain_db=args.music_mix_db)
    else:
        intermediate.replace(args.output)

    # Upload final to GCS
    final_gs = ""
    try:
        asset = gcs.upload_file(
            args.output,
            key=f"{build_run_prefix(order_no, run_no)}/final.mp4",
            content_type="video/mp4",
            cache_control="public, max-age=3600",
        )
        final_gs = asset.gs_uri
    except Exception as e:
        print(f"⚠️  final GCS upload failed: {e}")

    bal1 = await client.get_credits()
    spent = bal0.data.balance_thb - (bal1.data.balance_thb if bal1.data else 0.0)

    registry.finalize_run(
        run_no=run_no, order_no=order_no,
        status="APPROVED" if results else "FAILED",
        total_cost_thb=spent,
        gcs_prefix=build_run_prefix(order_no, run_no),
        final_mp4_gs_uri=final_gs,
        scene_count=len(results),
        last_decision="seedance-two-keyframe-complete" if results else "no-scenes-rendered",
    )

    print("\n" + "=" * 60)
    print(f"✅ local: {args.output} ({args.output.stat().st_size//1024} KB)")
    if final_gs:
        print(f"☁️  canonical: {final_gs}")
    print(f"📒 registry:  order_no={order_no:04d}  run_no={run_no:04d}  → finalized")
    print(f"💰 balance delta: ฿{spent:.4f}")
    print(f"📊 after: ฿{bal1.data.balance_thb if bal1.data else 0:.4f}")
    print(f"🎞️  scenes: {len(results)}/{len(indices)}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
