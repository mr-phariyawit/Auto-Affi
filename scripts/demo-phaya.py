#!/usr/bin/env python3
"""Generate a Phaya-powered demo from the seed storyboard.

Mirrors ``auto_affi.ops.make_demo`` but routes per-scene generation through
``PhayaVideoGenAdapter`` (Sora 2 T2V) + ``PhayaTTSAdapter`` instead of the
local PIL+espeak fallback. Output: ``out/demo-phaya.mp4``.

Strategy: generate scene 0 first (cost-discover), report real cost, then
continue with the remaining scenes if --all is passed AND budget permits.
Default --scenes=1 keeps cost bounded at first run.

Usage:
  python scripts/demo-phaya.py                 # scene 0 only (~฿25)
  python scripts/demo-phaya.py --scenes all    # all 5 scenes (~฿125)
  python scripts/demo-phaya.py --scenes 0,1,4  # specific scenes
"""

from __future__ import annotations

import argparse
import asyncio
import os
import subprocess
import sys
import time
from pathlib import Path

import httpx
from pydantic import SecretStr

from auto_affi.adapters.phaya import JobState, PhayaClient
from auto_affi.pipeline.demo_storyboard import build_demo_storyboard

try:
    from auto_affi.adapters.gcs_storage import GcsStorage, StoredAsset
except ImportError:  # google-cloud-storage not installed in some envs
    GcsStorage = None  # type: ignore[assignment]
    StoredAsset = None  # type: ignore[assignment]


async def _download(url: str, dest: Path) -> None:
    async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as c:
        r = await c.get(url)
        r.raise_for_status()
        dest.write_bytes(r.content)


def _parse_scene_arg(arg: str, total: int) -> list[int]:
    if arg == "all":
        return list(range(total))
    return [int(x) for x in arg.split(",")]


_TTS_PREFIX_STRIP = ("POV ", "POV: ", "POV:", "[narrator] ", "Narrator: ")


def _tts_clean(text: str) -> str:
    """Strip TTS-unfriendly instruction-style prefixes.

    Gemini TTS (under Phaya) interprets prefixes like ``POV ...`` as a
    *generation instruction* rather than a transcript to recite, and fails
    with "Model tried to generate text". Strip the common offenders before
    submission so the storyboard's source text stays human-readable.
    """
    cleaned = text.strip()
    for prefix in _TTS_PREFIX_STRIP:
        if cleaned.lower().startswith(prefix.lower()):
            cleaned = cleaned[len(prefix):].lstrip(" :")
            break
    return cleaned


def _mux(video: Path, audio: Path, out: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            str(out),
        ],
        check=True,
    )


def _concat(clips: list[Path], workdir: Path, out: Path) -> None:
    listfile = workdir / "concat.txt"
    listfile.write_text("\n".join(f"file '{p.resolve()}'" for p in clips))
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(listfile),
            "-c",
            "copy",
            str(out),
        ],
        check=True,
    )


async def _process_scene(
    client: PhayaClient, scene_idx: int, scene, workdir: Path
) -> tuple[Path, float] | None:
    """Submit video + tts, wait, download, mux. Returns (clip_path, cost_thb)."""
    print(f"\n── scene {scene_idx}: {scene.purpose} ({scene.duration_s}s)")
    print(f"   visual:   {scene.visual_prompt[:80]}")
    print(f"   dialogue: {scene.dialogue.text_th}")

    # Phaya Sora 2 only accepts n_frames="10" or "15" (string enum). "15" = max.
    # Sanitize TTS text — Gemini TTS rejects instruction-style prefixes.
    tts_text = _tts_clean(scene.dialogue.text_th)
    video_submit, tts_submit = await asyncio.gather(
        client.create_sora2_video(
            prompt=scene.visual_prompt, n_frames="15", aspect_ratio="portrait"
        ),
        client.create_tts(prompt=tts_text, voice="Algenib", language="th"),
    )
    if not video_submit.ok or video_submit.data is None:
        print(f"   ❌ video submit failed: {video_submit.error}")
        return None
    if not tts_submit.ok or tts_submit.data is None:
        print(f"   ❌ tts submit failed: {tts_submit.error}")
        return None
    print(f"   jobs: video={video_submit.data.job_id[:24]}… tts={tts_submit.data.job_id[:24]}…")

    t0 = time.time()
    video_done, tts_done = await asyncio.gather(
        client.wait_for_sora2(video_submit.data.job_id, poll_interval_s=5.0, timeout_s=420.0),
        client._wait(
            poller=client.get_tts_status,
            job_id=tts_submit.data.job_id,
            interval=3.0,
            timeout=240.0,
        ),
    )
    elapsed = time.time() - t0

    if not video_done.ok or video_done.data is None or video_done.data.state is not JobState.COMPLETED:
        msg = video_done.error or (video_done.data.state if video_done.data else "?")
        print(f"   ❌ video render failed: {msg}")
        return None
    if not tts_done.ok or tts_done.data is None or tts_done.data.state is not JobState.COMPLETED:
        msg = tts_done.error or (tts_done.data.state if tts_done.data else "?")
        print(f"   ❌ tts render failed: {msg}")
        return None
    if not video_done.data.result_url or not tts_done.data.result_url:
        print("   ❌ completed job has no result_url")
        return None

    print(f"   ✅ rendered in {elapsed:.0f}s")

    video_path = workdir / f"s{scene_idx}-video.mp4"
    audio_path = workdir / f"s{scene_idx}-audio.mp3"
    await asyncio.gather(
        _download(video_done.data.result_url, video_path),
        _download(tts_done.data.result_url, audio_path),
    )
    print(f"   ⤓ video {video_path.stat().st_size//1024} KB  audio {audio_path.stat().st_size//1024} KB")

    clip_path = workdir / f"s{scene_idx}-clip.mp4"
    _mux(video_path, audio_path, clip_path)
    cost_thb = (video_done.data.cost_thb or 0.0) + (tts_done.data.cost_thb or 0.0)
    return clip_path, cost_thb, video_path, audio_path


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenes", default="0", help="'all', comma-list, or single idx")
    parser.add_argument(
        "--output", type=Path, default=Path("out/demo-phaya.mp4"), help="final mp4 path"
    )
    parser.add_argument(
        "--workdir", type=Path, default=None, help="intermediate assets dir"
    )
    args = parser.parse_args()

    key = os.environ.get("PHAYA_API_KEY")
    if not key:
        print("ERROR: PHAYA_API_KEY missing in env")
        return 1

    sb = build_demo_storyboard()
    indices = _parse_scene_arg(args.scenes, len(sb.scenes))
    workdir = args.workdir or Path("out/phaya-workdir")
    workdir.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    client = PhayaClient(api_key=SecretStr(key))
    bal0 = await client.get_credits()
    if not bal0.ok or bal0.data is None:
        print(f"ERROR: get_credits failed: {bal0.error}")
        return 2
    print(f"📊 balance before: ฿{bal0.data.balance_thb:.4f} (≈${bal0.data.balance_usd:.4f})")
    print(f"🎬 scenes: {indices} · {len(indices)} of {len(sb.scenes)} · workdir={workdir}")

    # GCS staging per ADR-006 — initialize lazily, fall back if not configured
    gcs: GcsStorage | None = None
    bucket_name = os.environ.get("AUTO_AFFI__GCS_BUCKET")
    if GcsStorage is not None and bucket_name:
        try:
            gcs = GcsStorage(bucket_name=bucket_name)
            print(f"🪣 GCS: gs://{gcs.bucket_name}/ (per ADR-006)")
        except Exception as e:
            print(f"⚠️  GCS init failed ({e}); falling back to local-only")
    else:
        print("ℹ️  GCS not configured; local-only output (supabase URLs transient)")

    clips: list[Path] = []
    total_cost_thb = 0.0
    gcs_uris: list[str] = []
    run_date = time.strftime("%Y-%m-%d", time.gmtime())

    for idx in indices:
        if idx >= len(sb.scenes):
            print(f"   skip: scene {idx} out of range")
            continue
        result = await _process_scene(client, idx, sb.scenes[idx], workdir)
        if result is None:
            print(f"⚠️  scene {idx} failed; continuing with remaining scenes")
            continue
        clip, cost, video_path, audio_path = result
        clips.append(clip)
        total_cost_thb += cost

        # Republish raw assets to GCS per ADR-006 (supabase URLs never persisted)
        if gcs is not None:
            try:
                video_asset = gcs.upload_file(
                    video_path,
                    key=f"sora2/{run_date}/scene{idx}.mp4",
                    content_type="video/mp4",
                )
                audio_asset = gcs.upload_file(
                    audio_path,
                    key=f"tts/{run_date}/scene{idx}.wav",
                    content_type="audio/wav",
                )
                print(f"   ☁️  {video_asset.gs_uri}")
                print(f"   ☁️  {audio_asset.gs_uri}")
                gcs_uris.extend([video_asset.gs_uri, audio_asset.gs_uri])
            except Exception as e:
                print(f"   ⚠️  GCS republish failed: {e}")

    if not clips:
        print("\n❌ no scenes succeeded")
        return 3

    if len(clips) == 1:
        clips[0].replace(args.output)
        out_path = args.output
    else:
        _concat(clips, workdir, args.output)
        out_path = args.output

    # Republish the final muxed mp4 too
    final_gs_uri: str | None = None
    if gcs is not None:
        try:
            final_asset = gcs.upload_file(
                out_path,
                key=f"demo/{run_date}/{out_path.name}",
                content_type="video/mp4",
                cache_control="public, max-age=3600",
            )
            final_gs_uri = final_asset.gs_uri
            gcs_uris.append(final_gs_uri)
        except Exception as e:
            print(f"   ⚠️  final GCS republish failed: {e}")

    bal1 = await client.get_credits()
    spent = bal0.data.balance_thb - (bal1.data.balance_thb if bal1.data else 0.0)

    print("\n" + "=" * 60)
    print(f"✅ local output: {out_path} ({out_path.stat().st_size//1024} KB)")
    if final_gs_uri:
        print(f"☁️  GCS canonical: {final_gs_uri}")
    print(f"💰 reported cost_thb sum: ฿{total_cost_thb:.4f}")
    print(f"💰 balance delta:          ฿{spent:.4f}  (≈${spent*0.028:.4f})")
    print(f"📊 balance after:          ฿{bal1.data.balance_thb if bal1.data else 0:.4f}")
    print(f"🎞️  scenes rendered:       {len(clips)} / {len(indices)} requested")
    print(f"🪣 GCS objects:            {len(gcs_uris)}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
