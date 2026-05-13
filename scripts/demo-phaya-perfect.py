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
from datetime import timedelta
from pathlib import Path

import httpx
from pydantic import SecretStr

from auto_affi.adapters.phaya import JobState, PhayaClient
from auto_affi.agents.writers_room import WritersRoom
from auto_affi.ops.run_once import _niche_aware_brief, _resolve_product
from auto_affi.pipeline.demo_storyboard import build_demo_storyboard

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


def _mux(video: Path, audio: Path, out: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(audio),
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
    print(f"\n── scene {idx}: {scene.purpose} ({scene.duration_s}s)")
    print(f"   prompt: {detailed_prompt[:100]}…")
    print(f"   dialogue: {scene.dialogue.text_th}")

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
    if not i2v_wait.ok or i2v_wait.data is None or i2v_wait.data.state is not JobState.COMPLETED:
        print(f"   ❌ i2v render failed")
        return None
    if not tts_wait.ok or tts_wait.data is None or tts_wait.data.state is not JobState.COMPLETED:
        print(f"   ❌ tts render failed")
        return None
    if not i2v_wait.data.result_url or not tts_wait.data.result_url:
        print("   ❌ completed but no result_url")
        return None

    # 3. Download + mux
    print("   3/3 download + mux…")
    image_path = workdir / f"s{idx}-image.jpg"
    video_path = workdir / f"s{idx}-video.mp4"
    audio_path = workdir / f"s{idx}-audio.wav"
    await asyncio.gather(
        _download(image_url, image_path, gcs=gcs),
        _download(i2v_wait.data.result_url, video_path, gcs=gcs),
        _download(tts_wait.data.result_url, audio_path, gcs=gcs),
    )
    clip_path = workdir / f"s{idx}-clip.mp4"
    _mux(video_path, audio_path, clip_path)

    cost_thb = (
        (img_wait.data.cost_thb or 0.0)
        + (i2v_wait.data.cost_thb or 0.0)
        + (tts_wait.data.cost_thb or 0.0)
    )
    print(f"   ✅ scene done · cost ฿{cost_thb:.4f}")
    return clip_path, cost_thb, image_path, video_path, audio_path


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
    args = parser.parse_args()

    key = os.environ.get("PHAYA_API_KEY")
    if not key:
        print("ERROR: PHAYA_API_KEY missing"); return 1

    use_scene_prompt = args.shopee_url is not None
    if args.shopee_url:
        product, niche_hints = _resolve_product(
            product_id=None, shopee_url=args.shopee_url, fixture_path=None
        )
        brief = _niche_aware_brief(product, niche_hints)
        room = WritersRoom()
        sb_result = await room.generate_storyboard(brief)
        if not sb_result.ok or sb_result.data is None:
            print(f"ERROR: Writers' Room failed: {sb_result.error}")
            return 4
        sb = sb_result.data
        print(f"🛒 product:   {product.name[:70]}…")
        print(f"📋 niche:     {(niche_hints or {}).get('niche', '?')}/{(niche_hints or {}).get('sub_niche', '?')}")
        print(f"📝 brief:     {brief.persona.label} · angle={brief.angle[:60]}…")
        print(f"🎬 storyboard from Writers' Room (using scene.visual_prompt as-is)")
    else:
        sb = build_demo_storyboard()
        print("🎬 demo storyboard fixture (Beauty) with PERFECT_PROMPTS override")
    indices = _parse_scenes(args.scenes, len(sb.scenes))
    args.workdir.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # GCS staging: per ADR-006, pass GcsStorage into the client so Phaya
    # supabase URLs auto-republish to gs:// before any caller sees them.
    gcs: GcsStorage | None = None
    bucket = os.environ.get("AUTO_AFFI__GCS_BUCKET")
    if GcsStorage is not None and bucket:
        try:
            gcs = GcsStorage(bucket_name=bucket)
            print(f"🪣 GCS: gs://{gcs.bucket_name}/  (adapter auto-republishes)")
        except Exception as e:
            print(f"⚠️  GCS init failed: {e}")
    client = PhayaClient(api_key=SecretStr(key), timeout_s=60.0, gcs=gcs)
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

    if len(clips) == 1:
        clips[0].replace(args.output)
    else:
        _concat(clips, args.workdir, args.output)

    final_gs: str | None = None
    if gcs is not None:
        try:
            asset = gcs.upload_file(
                args.output,
                key=f"demo-perfect/{run_date}/{args.output.name}",
                content_type="video/mp4",
                cache_control="public, max-age=3600",
            )
            final_gs = asset.gs_uri
        except Exception as e:
            print(f"⚠️  final GCS upload failed: {e}")

    bal1 = await client.get_credits()
    spent = bal0.data.balance_thb - (bal1.data.balance_thb if bal1.data else 0.0)

    print("\n" + "=" * 60)
    print(f"✅ local: {args.output} ({args.output.stat().st_size//1024} KB)")
    if final_gs:
        print(f"☁️  canonical: {final_gs}")
    print(f"💰 reported sum: ฿{total_cost_thb:.4f}")
    print(f"💰 balance delta: ฿{spent:.4f}  (≈${spent*0.028:.4f})")
    print(f"📊 after: ฿{bal1.data.balance_thb if bal1.data else 0:.4f}")
    print(f"🎞️  scenes: {len(clips)}/{len(indices)}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
