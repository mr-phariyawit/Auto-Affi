#!/usr/bin/env python
"""Replace selected video clips with HeyGen Avatar IV lip-synced versions.

For each dialogue-bearing scene, this script:
  1. Generates a verified Thai TTS audio via Phaya (Algenib voice).
  2. Pads the audio with silence to match the original clip duration so
     the resulting HeyGen video drops into the timeline cleanly.
  3. Uploads the corresponding scene still + padded audio to HeyGen.
  4. Kicks off Avatar IV (type=image) lip-sync, polls to completion.
  5. Downloads the result + normalizes audio params (AAC 192k/44100/stereo)
     so concat with sibling Seedance clips is gapless.
  6. Writes the result to ``<workdir>/clip{N}-heygen-lipsync.mp4`` and
     copies it over the canonical ``clip{N}-seedance-final.mp4`` so the
     pipeline's downstream concat picks it up.

Why this exists: Seedance --generate-audio produces speech-LIKE audio but
words aren't verified — the model can hallucinate plausible-sounding
gibberish that the audience hears as "Thai-ish". HeyGen Avatar IV gives
deterministic lip-sync (0.02s error floor per practitioner research)
driven by an audio file we control end-to-end (Phaya TTS = verified Thai
pronunciation of the exact lullaby lyrics).

Usage:
    .venv/bin/python scripts/heygen-lipsync-clips.py \\
        --item-id 28875679676 \\
        --storyboard-json data/registry/items/28875679676/concept-2-storyboard.json \\
        --workdir out/maono-concept-2-workdir-v8 \\
        --clip-scene-map "2:3,3:4" \\
        --aspect-ratio 9:16 \\
        --resolution 720p
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
from auto_affi.adapters.heygen import HeyGenClient, HeyGenError
from auto_affi.adapters.phaya import PhayaClient, JobState


def _ffprobe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def _aac_flags() -> list[str]:
    """Uniform AAC encode flags so HeyGen outputs concat cleanly with
    sibling Seedance clips (192k / 44.1kHz / stereo, matches the rest
    of the pipeline)."""
    return ["-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2"]


def _pad_audio_to_duration(src: Path, dest: Path, target_duration_s: float) -> None:
    """Pad the TTS WAV with trailing silence so its duration matches the
    target clip duration. HeyGen produces a video whose duration matches
    the audio — padding ensures the resulting clip fills the timeline
    slot exactly."""
    src_dur = _ffprobe_duration(src)
    if src_dur >= target_duration_s - 0.01:
        # Already long enough — just copy
        dest.write_bytes(src.read_bytes())
        return
    pad_s = target_duration_s - src_dur
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
         "-af", f"apad=pad_dur={pad_s:.3f}",
         "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "1",
         str(dest)],
        check=True,
    )


def _normalize_lipsync_output(src: Path, dest: Path) -> None:
    """Re-encode HeyGen output to the pipeline's canonical params so concat
    against Seedance clips is gapless (same video codec/pix_fmt + AAC
    audio params)."""
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p",
         *_aac_flags(),
         str(dest)],
        check=True,
    )


async def _phaya_tts_wav(
    *, client: PhayaClient, gcs: GcsStorage, text: str, dest: Path,
) -> Path:
    """Generate Phaya TTS audio (Algenib voice, Thai) → local WAV."""
    submit = await client.create_tts(prompt=text, voice="Algenib", language="th")
    if not submit.ok or submit.data is None:
        raise RuntimeError(f"Phaya TTS submit failed: {submit.error}")
    wait = await client._wait(
        poller=client.get_tts_status,
        job_id=submit.data.job_id,
        interval=3.0, timeout=240.0,
    )
    if not (wait.ok and wait.data and wait.data.state is JobState.COMPLETED
            and wait.data.result_url):
        raise RuntimeError(f"Phaya TTS render failed: {wait.error if wait else 'unknown'}")
    url = wait.data.result_url
    # httpx can't fetch gs://, so sign the URL if needed
    if url.startswith(f"gs://{gcs.bucket_name}/"):
        key = url[len(f"gs://{gcs.bucket_name}/"):]
        url = await asyncio.to_thread(gcs.signed_url, key, ttl=timedelta(hours=1))
    dest.parent.mkdir(parents=True, exist_ok=True)
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as c:
        r = await c.get(url)
        r.raise_for_status()
        dest.write_bytes(r.content)
    return dest


def _parse_clip_scene_map(s: str) -> list[tuple[int, int, int]]:
    """Parse ``clip:dialogue_scene[:image_scene]`` triples.

    Examples:
      ``"2:3,3:4"``       → [(2, 3, 3), (3, 4, 4)]  (image defaults to dialogue scene)
      ``"2:3,3:4:3"``     → [(2, 3, 3), (3, 4, 3)]  (clip 3 uses s3's still even though dialogue is on s4 — useful when the speaker visual lives on a different scene than the dialogue, e.g. father's voice-over playing while daughter is asleep)
    """
    out: list[tuple[int, int, int]] = []
    for entry in s.split(","):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split(":")
        if len(parts) == 2:
            ci, dsi = int(parts[0]), int(parts[1])
            isi = dsi
        elif len(parts) == 3:
            ci, dsi, isi = int(parts[0]), int(parts[1]), int(parts[2])
        else:
            raise ValueError(f"bad map entry {entry!r}; want clip:dialogue_scene[:image_scene]")
        out.append((ci, dsi, isi))
    return out


async def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--item-id", type=int, required=True)
    p.add_argument("--storyboard-json", type=Path, required=True)
    p.add_argument("--workdir", type=Path, required=True)
    p.add_argument(
        "--clip-scene-map", type=str, required=True,
        help="Comma-separated <clip_idx>:<dialogue_scene_idx> pairs "
             "(e.g. '2:3,3:4'). The dialogue text is read from "
             "storyboard.frames[scene_idx].dialogue_th.",
    )
    p.add_argument("--aspect-ratio", type=str, default="9:16",
                   choices=["9:16", "16:9"])
    p.add_argument("--resolution", type=str, default="720p",
                   choices=["720p", "1080p", "4k"])
    p.add_argument(
        "--motion-prompt", type=str, default="subtle natural reading expression",
        help="Optional HeyGen motion prompt (body/head motion guidance).",
    )
    p.add_argument(
        "--expressiveness", type=str, default="medium",
        choices=["low", "medium", "high"],
    )
    p.add_argument(
        "--no-replace-canonical", action="store_true",
        help="Skip overwriting clip{N}-seedance-final.mp4 with the HeyGen "
             "output. Useful for A/B comparison runs.",
    )
    args = p.parse_args()

    # Env
    heygen_key = os.environ.get("HEYGEN_API_KEY", "").strip()
    if not heygen_key:
        print("ERROR: HEYGEN_API_KEY missing"); return 1
    phaya_key = os.environ.get("PHAYA_API_KEY", "").strip()
    if not phaya_key:
        print("ERROR: PHAYA_API_KEY missing"); return 1
    bucket = os.environ.get("AUTO_AFFI__GCS_BUCKET", "").strip()
    if not bucket:
        print("ERROR: AUTO_AFFI__GCS_BUCKET missing"); return 1

    sb = json.loads(args.storyboard_json.read_text(encoding="utf-8"))
    frames = sb["frames"]
    pairs = _parse_clip_scene_map(args.clip_scene_map)
    if not pairs:
        print("ERROR: --clip-scene-map produced no pairs"); return 1

    gcs = GcsStorage(bucket_name=bucket)
    phaya = PhayaClient(api_key=SecretStr(phaya_key), timeout_s=60.0)
    heygen = HeyGenClient(api_key=SecretStr(heygen_key), timeout_s=120.0)

    print(f"🧬 HeyGen Avatar IV lip-sync pass")
    print(f"   workdir:        {args.workdir}")
    print(f"   storyboard:     {args.storyboard_json}")
    print(f"   clip:scene map: {pairs}")
    print(f"   aspect/res:     {args.aspect_ratio}/{args.resolution}\n")

    summary: list[dict] = []

    for clip_idx, dialogue_scene_idx, image_scene_idx in pairs:
        if max(dialogue_scene_idx, image_scene_idx) >= len(frames):
            print(f"❌ scene out of range (only {len(frames)} frames)")
            continue
        dialogue = (frames[dialogue_scene_idx].get("dialogue_th") or "").strip()
        if not dialogue:
            print(f"⚠️  scene {dialogue_scene_idx} has no dialogue_th — skipping clip {clip_idx}")
            continue
        canonical_clip = args.workdir / f"clip{clip_idx}-seedance-final.mp4"
        scene_still = args.workdir / f"s{image_scene_idx}-image.jpg"
        if not scene_still.exists():
            print(f"❌ scene still missing: {scene_still}"); continue
        if not canonical_clip.exists():
            print(f"❌ canonical clip missing: {canonical_clip}"); continue

        target_duration = _ffprobe_duration(canonical_clip)
        print(f"\n── clip {clip_idx} ↔ dialogue=s{dialogue_scene_idx} image=s{image_scene_idx}")
        print(f"   target duration: {target_duration:.2f}s")
        print(f"   dialogue:        {dialogue!r}")

        # 1. Phaya TTS
        tts_wav = args.workdir / f"clip{clip_idx}-heygen-tts.wav"
        print(f"   1/5 Phaya TTS (Algenib · th) → {tts_wav.name}")
        await _phaya_tts_wav(client=phaya, gcs=gcs, text=dialogue, dest=tts_wav)
        tts_dur = _ffprobe_duration(tts_wav)
        print(f"       tts duration: {tts_dur:.2f}s")

        # 2. Pad to clip duration
        padded_wav = args.workdir / f"clip{clip_idx}-heygen-tts-padded.wav"
        print(f"   2/5 padding TTS to {target_duration:.2f}s")
        _pad_audio_to_duration(tts_wav, padded_wav, target_duration)

        # 3. Upload still + audio to HeyGen
        print(f"   3/5 uploading scene still + padded TTS to HeyGen")
        try:
            img_asset = await heygen.upload_asset(scene_still)
            aud_asset = await heygen.upload_asset(padded_wav)
        except HeyGenError as e:
            print(f"       ❌ upload failed: {e}"); continue
        print(f"       image_asset_id: {img_asset.asset_id}")
        print(f"       audio_asset_id: {aud_asset.asset_id}")

        # 4. Create video + poll
        print(f"   4/5 HeyGen Avatar IV (type=image) generating…")
        try:
            job = await heygen.create_video_from_image(
                image_asset_id=img_asset.asset_id,
                audio_asset_id=aud_asset.asset_id,
                aspect_ratio=args.aspect_ratio,
                resolution=args.resolution,
                motion_prompt=args.motion_prompt,
                expressiveness=args.expressiveness,
            )
            print(f"       video_id: {job.video_id} · status={job.status}")
            completed = await heygen.wait_for_video(
                job.video_id, interval_s=4.0, timeout_s=600.0,
            )
        except HeyGenError as e:
            print(f"       ❌ heygen render failed: {e}"); continue

        # 5. Download + normalize
        raw_path = args.workdir / f"clip{clip_idx}-heygen-raw.mp4"
        final_path = args.workdir / f"clip{clip_idx}-heygen-lipsync.mp4"
        print(f"   5/5 downloading + normalizing → {final_path.name}")
        await heygen.download_video(completed.video_url, raw_path)
        _normalize_lipsync_output(raw_path, final_path)
        final_dur = _ffprobe_duration(final_path)
        size_kb = final_path.stat().st_size // 1024
        print(f"       ✅ {final_path.name} ({size_kb}KB · {final_dur:.2f}s)")

        # 6. Replace canonical (so downstream concat picks up the lip-sync)
        if not args.no_replace_canonical:
            backup = args.workdir / f"clip{clip_idx}-seedance-final.pre-heygen.mp4"
            if not backup.exists():
                canonical_clip.rename(backup)
                print(f"       📦 backed up Seedance original → {backup.name}")
            else:
                canonical_clip.unlink()
            final_path.replace(canonical_clip)
            # Re-export under the heygen-lipsync name too so it survives audit
            subprocess.run(["cp", str(canonical_clip), str(final_path)], check=True)
            print(f"       🔁 promoted to canonical clip{clip_idx}-seedance-final.mp4")

        summary.append({
            "clip_idx": clip_idx,
            "dialogue_scene_idx": dialogue_scene_idx,
            "image_scene_idx": image_scene_idx,
            "dialogue": dialogue,
            "tts_duration_s": tts_dur,
            "final_duration_s": final_dur,
            "heygen_video_id": completed.video_id,
            "image_asset_id": img_asset.asset_id,
            "audio_asset_id": aud_asset.asset_id,
        })

    # Persist a manifest for downstream tooling / audit
    if summary:
        manifest = args.workdir / "heygen-lipsync-manifest.json"
        manifest.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\n📒 manifest: {manifest}")
    print(f"\n✅ HeyGen lip-sync pass complete · {len(summary)} clip(s) replaced")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
