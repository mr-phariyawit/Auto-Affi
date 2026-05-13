#!/usr/bin/env python3
"""Perfect-storyboard demo: per-scene Phaya pipeline with image-first chaining.

Replaces direct Sora 2 T2V with the higher-control flow:
  1. Nano Banana 2 image gen (9:16, 1K) from a detailed Thai-Beauty prompt
  2. Phaya image-to-video animates the still (5 s default, silent)
  3. Phaya TTS (Algenib, th) renders the dialogue
  4. ffmpeg muxes video + audio into the scene clip
  5. GCS republish per ADR-006 (supabase URLs never persisted)
  6. ffmpeg concat → final 9:16 mp4

Detailed visual prompts are inline (PERFECT_PROMPTS) — far richer than
``Scene.visual_prompt`` from the static fixture. These represent the
"perfect storyboard" the Writers' Room is expected to LLM-generate in
Sprint 5; for now they're hand-crafted so the image pipeline is
provable end-to-end.

Cost estimate (May 2026 pricing):
  - Nano Banana 2 @ 1K = ~2 credits ≈ ฿0.05
  - Image-to-Video 5 s ≈ ~5-10 credits ≈ ฿0.10-0.25
  - TTS short clip ≈ free (token-priced)
  Per scene ≈ ฿0.30. Full 5-scene demo ≈ ฿1.50.

Usage:
  python scripts/demo-phaya-perfect.py --scenes 0
  python scripts/demo-phaya-perfect.py --scenes all
"""

from __future__ import annotations

import argparse
import asyncio
import os
import subprocess
import sys
import time
import uuid
from datetime import timedelta
from pathlib import Path

import httpx
from pydantic import SecretStr

from auto_affi.adapters.phaya import JobState, PhayaClient
from auto_affi.agents.writers_room import WritersRoom
from auto_affi.ops.run_once import (
    _niche_aware_brief,
    _resolve_product,
    brief_from_registry_entry,
    resolve_product_with_registry,
    storyboard_from_registry,
)
from auto_affi.pipeline.demo_storyboard import build_demo_storyboard
from auto_affi.registry import build_run_prefix, registry_from_env

try:
    from auto_affi.adapters.gcs_storage import GcsStorage
except ImportError:
    GcsStorage = None  # type: ignore[assignment]


# Hand-crafted "perfect" visual prompts for the demo Beauty storyboard.
# Each is rich on lighting / framing / color / mood — what a Writers' Room
# Director + Cinematographer + Storyboard Artist would produce.
PERFECT_PROMPTS: dict[int, str] = {
    0: (
        "Cinematic POV close-up of a young Thai woman's face seen through a "
        "bathroom mirror, soft afternoon window light from the right, peachy "
        "warm tones, shallow depth of field. Visible oily T-zone shine on "
        "forehead and nose, slightly concerned expression. Slight handheld "
        "camera shake. 9:16 vertical, Bangkok apartment aesthetic, no-filter "
        "dewy realistic skin texture. Beige bathrobe, minimal kawaii makeup. "
        "Cozy intimate vibe."
    ),
    1: (
        "Medium close-up of the same Thai woman by an office window, harsh "
        "Bangkok midday tropical sun grazing her forehead. Visible sebum "
        "shine reflecting light, frustrated expression. Office skyline "
        "blurred behind. 9:16 vertical, warm cinematic color grade, "
        "realistic skin texture with slight sweat sheen, golden-hour key "
        "light. Frustrated GRWM energy."
    ),
    2: (
        "Macro extreme closeup of feminine Thai hands gently applying clear "
        "gel serum from a frosted glass dropper onto inner forearm skin. "
        "Soft natural daylight from a large window, slow satisfying "
        "application motion. Peachy warm color palette, silk smooth fabric "
        "in background. 9:16 vertical, ASMR-aesthetic, Thai pampering "
        "routine vibe, slight motion blur on the dropper."
    ),
    3: (
        "Cinematic medium shot of the same Thai woman now confident, smooth "
        "matte forehead, natural minimal makeup, soft pink lipstick, faint "
        "smile toward camera. Soft side lighting, peachy warm tones, gentle "
        "bokeh of Bangkok dusk city lights behind. 9:16 vertical, "
        "transformation-after vibe, realistic dewy-matte skin, no-filter look."
    ),
    4: (
        "Closeup of a Thai woman's hand making an upward tap gesture toward "
        "the bottom of the frame, where a glowing pastel pink 'tap link in "
        "caption' overlay floats. Soft pastel-peach background, kawaii "
        "minimal aesthetic, glowing pink QR code in lower-right corner. "
        "9:16 vertical, viral TikTok endcard energy, dreamy soft light."
    ),
}

_TTS_PREFIX_STRIP = ("POV ", "POV: ", "[narrator] ", "Narrator: ")


def _tts_clean(text: str) -> str:
    """Strip TTS-unfriendly instruction-style prefixes (Gemini TTS rejects them)."""
    cleaned = text.strip()
    for prefix in _TTS_PREFIX_STRIP:
        if cleaned.lower().startswith(prefix.lower()):
            cleaned = cleaned[len(prefix):].lstrip(" :")
            break
    return cleaned


async def _download(url: str, dest: Path, *, gcs: "GcsStorage | None" = None) -> None:
    """Download by URL — supports gs:// (via GcsStorage) and https://.

    Phaya supabase URLs are gone from the adapter return path (ADR-006);
    callers should only see gs:// URIs from this client. The https://
    branch remains for legacy callers and signed-URL flows.
    """
    if url.startswith("gs://"):
        if gcs is None:
            raise RuntimeError("gs:// URI received but GcsStorage not provided")
        await asyncio.to_thread(gcs.download_to_file, url, dest)
        return
    async with httpx.AsyncClient(timeout=180.0, follow_redirects=True) as c:
        r = await c.get(url)
        r.raise_for_status()
        dest.write_bytes(r.content)


def _mux(video: Path, audio: Path | None, out: Path) -> None:
    """Mux video + audio. If audio is None, mux video with a silent track."""
    if audio is not None:
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(audio),
             "-c:v", "copy", "-c:a", "aac", "-shortest", str(out)],
            check=True,
        )
    else:
        # Add silent audio so concat across silent + voiced clips has consistent audio streams
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(video),
             "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
             "-c:v", "copy", "-c:a", "aac", "-shortest", str(out)],
            check=True,
        )


def _concat(clips: list[Path], workdir: Path, out: Path) -> None:
    listfile = workdir / "concat.txt"
    listfile.write_text("\n".join(f"file '{p.resolve()}'" for p in clips))
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(listfile), "-c", "copy", str(out)],
        check=True,
    )


async def _upload_cached_image(
    gcs: "GcsStorage | None",
    *,
    image_path: Path,
    idx: int,
    order_no: int | None,
    run_no: int | None,
) -> tuple[str, str]:
    """Upload a cached approved still to GCS, return (gs_uri, signed_https_url).

    The signed URL is what Phaya's i2v endpoint needs (it can't fetch gs://).
    """
    if gcs is None:
        raise RuntimeError(
            "--use-cached-images needs AUTO_AFFI__GCS_BUCKET configured so "
            "Phaya i2v can read the still via a signed URL"
        )
    key_prefix = build_run_prefix(order_no, run_no) if (order_no and run_no) else "demo-perfect/cached"
    key = f"{key_prefix}/stage4-visuals/scene_{idx}.jpg"
    asset = await asyncio.to_thread(
        gcs.upload_file,
        image_path,
        key=key,
        content_type="image/jpeg",
        cache_control="public, max-age=3600",
    )
    url = await asyncio.to_thread(gcs.signed_url, key, ttl=timedelta(hours=1))
    return asset.gs_uri, url


async def _process_scene_with_cached_image(
    client: PhayaClient,
    idx: int,
    scene: "Scene",
    workdir: Path,
    *,
    gcs: "GcsStorage | None",
    order_no: int | None,
    run_no: int | None,
) -> "tuple[Path, float, Path, Path, Path] | None":
    """Variant of _process_scene that reuses an approved still from workdir.

    Skips Nano Banana 2; uploads the local still to GCS, hands the signed
    URL to Phaya's i2v + TTS. Used when --use-cached-images is set.
    """
    has_dialogue = scene.dialogue is not None and scene.dialogue.text_th.strip()
    print(f"\n── scene {idx}: {scene.purpose} ({scene.duration_s}s) · cached image")
    image_path = workdir / f"s{idx}-image.jpg"
    if not image_path.exists():
        print(f"   ❌ no cached image at {image_path}")
        return None
    print(f"   1/3 uploading cached still + signing URL…")
    try:
        _, phaya_image_url = await _upload_cached_image(
            gcs, image_path=image_path, idx=idx, order_no=order_no, run_no=run_no
        )
    except Exception as e:
        print(f"   ❌ cached-image upload failed: {e}")
        return None

    duration_s = max(5, int(round(scene.duration_s)))
    if has_dialogue:
        tts_text = _tts_clean(scene.dialogue.text_th)
        print(f"   2/3 image-to-video ({duration_s}s) + tts in parallel…")
        i2v_submit, tts_submit = await asyncio.gather(
            client.create_image_to_video(image_url=phaya_image_url, duration_s=duration_s),
            client.create_tts(prompt=tts_text, voice="Algenib", language="th"),
        )
        if not i2v_submit.ok or i2v_submit.data is None:
            print(f"   ❌ i2v submit failed: {i2v_submit.error}"); return None
        if not tts_submit.ok or tts_submit.data is None:
            print(f"   ❌ tts submit failed: {tts_submit.error}"); return None
        i2v_wait, tts_wait = await asyncio.gather(
            client.wait_for_image_to_video(i2v_submit.data.job_id),
            client._wait(
                poller=client.get_tts_status,
                job_id=tts_submit.data.job_id,
                interval=3.0, timeout=240.0,
            ),
        )
        if not tts_wait.ok or tts_wait.data is None or tts_wait.data.state is not JobState.COMPLETED:
            print(f"   ❌ tts render failed"); return None
        if not tts_wait.data.result_url:
            print("   ❌ tts completed but no result_url"); return None
    else:
        print(f"   2/3 image-to-video ({duration_s}s), no tts (silent scene)…")
        i2v_submit = await client.create_image_to_video(
            image_url=phaya_image_url, duration_s=duration_s
        )
        if not i2v_submit.ok or i2v_submit.data is None:
            print(f"   ❌ i2v submit failed: {i2v_submit.error}"); return None
        i2v_wait = await client.wait_for_image_to_video(i2v_submit.data.job_id)
        tts_wait = None

    if not i2v_wait.ok or i2v_wait.data is None or i2v_wait.data.state is not JobState.COMPLETED:
        print(f"   ❌ i2v render failed")
        return None
    if not i2v_wait.data.result_url:
        print("   ❌ i2v completed but no result_url")
        return None

    print("   3/3 download + mux…")
    video_path = workdir / f"s{idx}-video.mp4"
    audio_path: Path | None = workdir / f"s{idx}-audio.wav" if has_dialogue else None
    downloads = [_download(i2v_wait.data.result_url, video_path, gcs=gcs)]
    if has_dialogue and tts_wait is not None and audio_path is not None:
        downloads.append(_download(tts_wait.data.result_url, audio_path, gcs=gcs))
    await asyncio.gather(*downloads)
    clip_path = workdir / f"s{idx}-clip.mp4"
    _mux(video_path, audio_path, clip_path)

    cost_thb = (
        (i2v_wait.data.cost_thb or 0.0)
        + ((tts_wait.data.cost_thb if (has_dialogue and tts_wait and tts_wait.data) else 0.0) or 0.0)
    )
    print(f"   ✅ scene done · cost ฿{cost_thb:.4f}")
    return clip_path, cost_thb, image_path, video_path, audio_path or video_path


async def _process_scene(
    client: PhayaClient,
    idx: int,
    scene,
    workdir: Path,
    *,
    use_scene_prompt: bool = False,
    gcs: "GcsStorage | None" = None,
) -> tuple[Path, float, Path, Path, Path] | None:
    """Per-scene perfect pipeline. Returns (clip, cost_thb, image, video, audio).

    When ``use_scene_prompt`` is True, trust ``scene.visual_prompt`` as-is
    (Writers' Room already produced niche-appropriate detail). Otherwise
    use the Beauty-tuned ``PERFECT_PROMPTS`` override.
    """
    if use_scene_prompt:
        detailed_prompt = scene.visual_prompt
    else:
        detailed_prompt = PERFECT_PROMPTS.get(idx, scene.visual_prompt)
    has_dialogue = scene.dialogue is not None and scene.dialogue.text_th.strip()
    print(f"\n── scene {idx}: {scene.purpose} ({scene.duration_s}s)")
    print(f"   prompt: {detailed_prompt[:100]}…")
    print(f"   dialogue: {scene.dialogue.text_th if has_dialogue else '<silent>'}")

    # 1. Image gen
    print("   1/3 image (nano-banana-2)…")
    img_submit = await client.create_nano_banana_image(
        prompt=detailed_prompt, aspect_ratio="9:16", resolution="1K"
    )
    if not img_submit.ok or img_submit.data is None:
        print(f"   ❌ image submit failed: {img_submit.error}")
        return None
    img_wait = await client.wait_for_nano_banana(img_submit.data.job_id)
    if not img_wait.ok or img_wait.data is None or img_wait.data.state is not JobState.COMPLETED:
        print(f"   ❌ image render failed: {img_wait.error or (img_wait.data.state if img_wait.data else '?')}")
        return None
    if not img_wait.data.result_url:
        print("   ❌ image completed but no URL")
        return None
    image_url = img_wait.data.result_url
    print(f"      canonical: {image_url[:80]}…")

    # 2. Image-to-video + TTS in parallel.
    # Phaya's /image-to-video/create requires http(s) URLs, not gs://. The
    # adapter republishes images to GCS for downstream ownership (ADR-006),
    # but for cross-Phaya-endpoint chaining we mint a short-lived signed
    # URL so Phaya can GET the image from our bucket.
    phaya_image_url = image_url
    if image_url.startswith("gs://") and gcs is not None:
        bucket_prefix = f"gs://{gcs.bucket_name}/"
        if image_url.startswith(bucket_prefix):
            key = image_url[len(bucket_prefix):]
            phaya_image_url = await asyncio.to_thread(
                gcs.signed_url, key, ttl=timedelta(hours=1)
            )
    duration_s = max(5, int(round(scene.duration_s)))
    if has_dialogue:
        tts_text = _tts_clean(scene.dialogue.text_th)
        print(f"   2/3 image-to-video ({duration_s}s) + tts in parallel…")
        i2v_submit, tts_submit = await asyncio.gather(
            client.create_image_to_video(image_url=phaya_image_url, duration_s=duration_s),
            client.create_tts(prompt=tts_text, voice="Algenib", language="th"),
        )
        if not i2v_submit.ok or i2v_submit.data is None:
            print(f"   ❌ i2v submit failed: {i2v_submit.error}")
            return None
        if not tts_submit.ok or tts_submit.data is None:
            print(f"   ❌ tts submit failed: {tts_submit.error}")
            return None
        i2v_wait, tts_wait = await asyncio.gather(
            client.wait_for_image_to_video(i2v_submit.data.job_id),
            client._wait(
                poller=client.get_tts_status,
                job_id=tts_submit.data.job_id,
                interval=3.0,
                timeout=240.0,
            ),
        )
        if not tts_wait.ok or tts_wait.data is None or tts_wait.data.state is not JobState.COMPLETED:
            print(f"   ❌ tts render failed")
            return None
        if not tts_wait.data.result_url:
            print("   ❌ tts completed but no result_url")
            return None
    else:
        print(f"   2/3 image-to-video ({duration_s}s), no tts (silent scene)…")
        i2v_submit = await client.create_image_to_video(
            image_url=phaya_image_url, duration_s=duration_s
        )
        if not i2v_submit.ok or i2v_submit.data is None:
            print(f"   ❌ i2v submit failed: {i2v_submit.error}")
            return None
        i2v_wait = await client.wait_for_image_to_video(i2v_submit.data.job_id)
        tts_wait = None

    if not i2v_wait.ok or i2v_wait.data is None or i2v_wait.data.state is not JobState.COMPLETED:
        print(f"   ❌ i2v render failed")
        return None
    if not i2v_wait.data.result_url:
        print("   ❌ i2v completed but no result_url")
        return None

    # 3. Download + mux
    print("   3/3 download + mux…")
    image_path = workdir / f"s{idx}-image.jpg"
    video_path = workdir / f"s{idx}-video.mp4"
    audio_path: Path | None = workdir / f"s{idx}-audio.wav" if has_dialogue else None
    downloads = [
        _download(image_url, image_path, gcs=gcs),
        _download(i2v_wait.data.result_url, video_path, gcs=gcs),
    ]
    if has_dialogue and tts_wait is not None and audio_path is not None:
        downloads.append(_download(tts_wait.data.result_url, audio_path, gcs=gcs))
    await asyncio.gather(*downloads)
    clip_path = workdir / f"s{idx}-clip.mp4"
    _mux(video_path, audio_path, clip_path)

    cost_thb = (
        (img_wait.data.cost_thb or 0.0)
        + (i2v_wait.data.cost_thb or 0.0)
        + ((tts_wait.data.cost_thb if (has_dialogue and tts_wait and tts_wait.data) else 0.0) or 0.0)
    )
    print(f"   ✅ scene done · cost ฿{cost_thb:.4f}")
    return clip_path, cost_thb, image_path, video_path, audio_path or video_path


def _parse_scenes(arg: str, total: int) -> list[int]:
    return list(range(total)) if arg == "all" else [int(x) for x in arg.split(",")]


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenes", default="0")
    parser.add_argument(
        "--output", type=Path, default=Path("out/demo-phaya-perfect.mp4")
    )
    parser.add_argument("--workdir", type=Path, default=Path("out/phaya-perfect-workdir"))
    parser.add_argument(
        "--shopee-url",
        type=str,
        default=None,
        help="Real Shopee URL — drives Writers' Room storyboard instead of the Beauty fixture",
    )
    parser.add_argument(
        "--music-prompt",
        type=str,
        default=None,
        help="Phaya text-to-music prompt; if set, music is generated and mixed under final concat",
    )
    parser.add_argument(
        "--music-duration",
        type=int,
        default=30,
        help="Duration in seconds for the music track (default 30)",
    )
    parser.add_argument(
        "--music-mix-db",
        type=float,
        default=-12.0,
        help="dB to attenuate the music track when mixing under voice (default -12dB)",
    )
    parser.add_argument(
        "--use-cached-images",
        action="store_true",
        help="Skip Nano Banana 2 generation; reuse workdir/s{idx}-image.jpg approved stills (uploaded via signed URL for Phaya i2v).",
    )
    args = parser.parse_args()

    key = os.environ.get("PHAYA_API_KEY")
    if not key:
        print("ERROR: PHAYA_API_KEY missing"); return 1

    # ---- Registry: source of truth for product brief + run numbering ---- #
    registry = registry_from_env()
    order_no: int | None = None
    run_no: int | None = None
    run_id = str(uuid.uuid4())[:12]
    if args.shopee_url:
        product, entry, niche_hints = resolve_product_with_registry(
            shopee_url=args.shopee_url, registry=registry
        )
        if entry is None:
            print(f"⚠️  product not in registry — falling back to niche-hint brief")
            brief = _niche_aware_brief(product, niche_hints)
        else:
            brief = brief_from_registry_entry(product, entry)
            order_no = entry.order_no
            print(f"📒 registry:  order_no={order_no:04d}  niche={entry.niche}/{entry.sub_niche}")
        if order_no is not None:
            run_entry = registry.start_run(
                order_no=order_no, run_id=run_id, publish_mode="dry_run"
            )
            run_no = run_entry.run_no
            print(f"🔢 run:       run_no={run_no:04d}  run_id={run_id}")
    gcs_key_prefix = (
        build_run_prefix(order_no, run_no) if (order_no and run_no) else "demo-perfect"
    )

    # GCS staging: per ADR-006, pass GcsStorage into the client so Phaya
    # supabase URLs auto-republish to gs:// before any caller sees them.
    gcs: GcsStorage | None = None
    bucket = os.environ.get("AUTO_AFFI__GCS_BUCKET")
    if GcsStorage is not None and bucket:
        try:
            gcs = GcsStorage(bucket_name=bucket)
            print(f"🪣 GCS: gs://{gcs.bucket_name}/{gcs_key_prefix}/")
        except Exception as e:
            print(f"⚠️  GCS init failed: {e}")
    client = PhayaClient(
        api_key=SecretStr(key),
        timeout_s=60.0,
        gcs=gcs,
        gcs_key_prefix=gcs_key_prefix,
    )

    use_scene_prompt = args.shopee_url is not None
    if args.shopee_url:
        # Storyboard precedence: (1) registry overrides → (2) LLM → (3) fallback
        overrides = (
            registry.get_storyboard_overrides(order_no) if order_no else []
        )
        if overrides and entry is not None:
            sb = storyboard_from_registry(
                entry=entry, overrides=overrides, brief=brief
            )
            print(f"🛒 product:   {product.name[:70]}…")
            print(f"📝 brief:     {brief.persona.label} · angle={brief.angle[:60]}…")
            print(f"🎬 storyboard: registry overrides ({len(overrides)} scenes, board-curated)")
        else:
            room = WritersRoom(llm_client=client)
            sb_result = await room.generate_storyboard(brief)
            if not sb_result.ok or sb_result.data is None:
                print(f"ERROR: Writers' Room failed: {sb_result.error}")
                if order_no and run_no:
                    registry.finalize_run(
                        run_no=run_no, order_no=order_no, status="FAILED",
                        error=f"writers_room: {sb_result.error}",
                    )
                return 4
            sb = sb_result.data
            print(f"🛒 product:   {product.name[:70]}…")
            print(f"📝 brief:     {brief.persona.label} · angle={brief.angle[:60]}…")
            print(f"🎬 storyboard: Writers' Room (LLM via Phaya GPT, fallback to template)")
    else:
        sb = build_demo_storyboard()
        print("🎬 demo storyboard fixture (Beauty) with PERFECT_PROMPTS override")
    indices = _parse_scenes(args.scenes, len(sb.scenes))
    args.workdir.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    bal0 = await client.get_credits()
    if not bal0.ok or bal0.data is None:
        print(f"ERROR: get_credits failed: {bal0.error}"); return 2
    print(f"📊 balance: ฿{bal0.data.balance_thb:.4f}")
    print(f"🎬 scenes: {indices} · {len(indices)}/{len(sb.scenes)}")

    # GCS was constructed above and passed to the PhayaClient — reuse it.

    clips: list[Path] = []
    total_cost_thb = 0.0
    run_date = time.strftime("%Y-%m-%d", time.gmtime())

    for idx in indices:
        if idx >= len(sb.scenes):
            continue
        if args.use_cached_images:
            result = await _process_scene_with_cached_image(
                client, idx, sb.scenes[idx], args.workdir,
                gcs=gcs, order_no=order_no, run_no=run_no,
            )
        else:
            result = await _process_scene(
                client, idx, sb.scenes[idx], args.workdir,
                use_scene_prompt=use_scene_prompt,
                gcs=gcs,
            )
        if result is None:
            print(f"⚠️  scene {idx} failed; continuing")
            continue
        clip, cost, _img, _vid, _aud = result
        clips.append(clip)
        total_cost_thb += cost
        # Raw assets are already on GCS — the adapter republishes them under
        # gs://<bucket>/phaya/{sora2,i2v,nano-banana,tts}/<job_id>.<ext>.
        # No per-scene re-upload needed in this script (ADR-006 boundary
        # is the adapter, not the script).

    if not clips:
        print("\n❌ no scenes succeeded"); return 3

    # Concat or single — write to intermediate path so we can optionally mux music
    intermediate = args.workdir / "concat.mp4"
    if len(clips) == 1:
        clips[0].replace(intermediate)
    else:
        _concat(clips, args.workdir, intermediate)

    # Optional music layer
    music_path: Path | None = None
    if args.music_prompt:
        print(f"\n🎵 generating music ({args.music_duration}s) via Phaya text-to-music…")
        music_submit = await client.create_music(
            prompt=args.music_prompt, duration_s=args.music_duration
        )
        if music_submit.ok and music_submit.data is not None:
            music_wait = await client._wait(
                poller=client.get_music_status,
                job_id=music_submit.data.job_id,
                interval=4.0,
                timeout=300.0,
            )
            if (
                music_wait.ok
                and music_wait.data is not None
                and music_wait.data.state is JobState.COMPLETED
                and music_wait.data.result_url
            ):
                music_path = args.workdir / "music.mp3"
                await _download(music_wait.data.result_url, music_path, gcs=gcs)
                print(f"   ✅ music ready ({music_path.stat().st_size//1024} KB)")
            else:
                print(f"   ⚠️  music render failed; continuing without music")
        else:
            print(f"   ⚠️  music submit failed: {music_submit.error}; continuing without music")

    if music_path is not None:
        # Mix concat audio + music at music-mix-db with -shortest to clip to video length
        print(f"🎚️  mixing music under voice @ {args.music_mix_db} dB…")
        gain_db = args.music_mix_db
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(intermediate),
             "-i", str(music_path),
             "-filter_complex",
             f"[1:a]volume={gain_db}dB[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0[aout]",
             "-map", "0:v", "-map", "[aout]",
             "-c:v", "copy", "-c:a", "aac", "-shortest",
             str(args.output)],
            check=True,
        )
    else:
        intermediate.replace(args.output)

    final_gs: str | None = None
    if gcs is not None:
        try:
            # Numbered registry path takes precedence over date-based legacy path
            final_key = (
                f"{gcs_key_prefix}/final.mp4"
                if order_no and run_no
                else f"demo-perfect/{run_date}/{args.output.name}"
            )
            asset = gcs.upload_file(
                args.output,
                key=final_key,
                content_type="video/mp4",
                cache_control="public, max-age=3600",
            )
            final_gs = asset.gs_uri
        except Exception as e:
            print(f"⚠️  final GCS upload failed: {e}")

    bal1 = await client.get_credits()
    spent = bal0.data.balance_thb - (bal1.data.balance_thb if bal1.data else 0.0)

    # Finalize registry run row — real spend from balance delta, not the
    # buggy per-scene reported sum.
    if order_no and run_no:
        registry.finalize_run(
            run_no=run_no,
            order_no=order_no,
            status="APPROVED" if clips else "FAILED",
            total_cost_thb=spent,
            gcs_prefix=gcs_key_prefix,
            final_mp4_gs_uri=final_gs or "",
            scene_count=len(clips),
            last_decision="dry-run-complete" if clips else "no-scenes-rendered",
        )

    print("\n" + "=" * 60)
    print(f"✅ local: {args.output} ({args.output.stat().st_size//1024} KB)")
    if final_gs:
        print(f"☁️  canonical: {final_gs}")
    if order_no and run_no:
        print(f"📒 registry:  order_no={order_no:04d}  run_no={run_no:04d}  → finalized")
    print(f"💰 reported sum: ฿{total_cost_thb:.4f}")
    print(f"💰 balance delta: ฿{spent:.4f}  (≈${spent*0.028:.4f})")
    print(f"📊 after: ฿{bal1.data.balance_thb if bal1.data else 0:.4f}")
    print(f"🎞️  scenes: {len(clips)}/{len(indices)}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
