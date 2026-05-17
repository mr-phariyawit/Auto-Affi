"""Shared render helpers used by both produce-ai-storyboard.py and
produce-variant-set.py. Extracted 2026-05-18 during the variant-testing
implementation."""

from __future__ import annotations

import asyncio
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

import httpx

from auto_affi.adapters.gcs_storage import GcsStorage
from auto_affi.adapters.gemini_image import GeminiImageClient, write_image_to_path
from auto_affi.adapters.higgsfield_cli import HiggsfieldCli, HiggsfieldCliError
from auto_affi.adapters.phaya import JobState, PhayaClient
from auto_affi.adapters.seedance2 import Seedance2Client, Seedance2Error
from auto_affi.schemas.ai_storyboard import (
    AiShot, AiStoryboard, SubtitlePlacement,
)
from auto_affi.schemas.storyboard import HyperframeOverlay


__all__ = [
    "aac_flags",
    "ffprobe_duration",
    "resolve_refs",
    "gemini_still",
    "hold_to_mp4",
    "normalize_mp4",
    "pad_audio",
    "thai_tts_wav",
    "run_higgsfield_cli",
    "run_seedance_2kf",
    "run_seedance_2_2kf",
    "concat_clips",
    "mix_music_under",
    "build_subtitle_overlays",
]


def aac_flags() -> list[str]:
    return ["-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2"]


def ffprobe_duration(p: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(p)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def resolve_refs(
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


async def gemini_still(
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


def hold_to_mp4(
    still: Path, dest: Path, duration_s: float,
    *, fps: int = 24, voiceover_wav: Path | None = None,
) -> None:
    """Loop a still into an mp4 of the requested duration.

    If ``voiceover_wav`` is provided, that WAV becomes the audio track —
    padded with silence (apad) up to ``duration_s`` so the clip's video
    length always wins. Otherwise the audio is anullsrc silence.
    """
    if voiceover_wav is not None and voiceover_wav.exists():
        audio_input = ["-i", str(voiceover_wav)]
        # Pad VO to clip duration so video length governs concat
        audio_filter = ["-af", f"apad=whole_dur={duration_s:.3f}"]
    else:
        audio_input = ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
        audio_filter = []

    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-loop", "1", "-i", str(still),
         *audio_input,
         "-t", f"{duration_s:.3f}", "-r", str(fps),
         *audio_filter,
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p",
         *aac_flags(), "-shortest",
         str(dest)],
        check=True,
    )


def normalize_mp4(src: Path, dest: Path, *, target_duration_s: float | None = None) -> None:
    """Re-encode to canonical params so concat is gapless. Optionally
    pad / trim to a target duration."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src)]
    af = ["apad"] if target_duration_s else []
    if af:
        cmd += ["-af", ",".join(af)]
    cmd += [
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        *aac_flags(),
    ]
    if target_duration_s is not None:
        cmd += ["-t", f"{target_duration_s:.3f}"]
    cmd += [str(dest)]
    subprocess.run(cmd, check=True)


def pad_audio(src: Path, dest: Path, target_s: float) -> None:
    cur = ffprobe_duration(src)
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
        state = wait.data.state.value if (wait.ok and wait.data) else "?"
        detail = wait.data.detail if (wait.ok and wait.data and hasattr(wait.data, "detail")) else None
        raise RuntimeError(
            f"phaya TTS render failed · state={state} · "
            f"wait.error={wait.error!r} · detail={detail!r} · "
            f"job_id={submit.data.job_id}"
        )
    url = wait.data.result_url
    if url.startswith(f"gs://{gcs.bucket_name}/"):
        key = url[len(f"gs://{gcs.bucket_name}/"):]
        url = await asyncio.to_thread(gcs.signed_url, key, ttl=timedelta(hours=1))
    dest.parent.mkdir(parents=True, exist_ok=True)
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as c:
        r = await c.get(url); r.raise_for_status()
        dest.write_bytes(r.content)
    return dest


async def _edge_tts_wav(*, text: str, dest: Path, voice: str = "th-TH-NiwatNeural") -> Path:
    """Free Microsoft Edge TTS — Thai male voice (Niwat) by default.

    Used as the primary Thai TTS path. Phaya Algenib is a fallback only
    when explicitly forced — research (2026-05-15) showed Phaya Algenib
    reads as AI-obvious to Thai audiences at >฿1,500 product price bands,
    hurting affiliate trust. Edge TTS Niwat is closer to a natural Thai
    male voice. Writes mp3, transcodes to wav at the canonical rate so
    downstream apad / pad-to-duration flows behave identically.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    mp3 = dest.with_suffix(".mp3")
    # subprocess (sync) is fine — edge-tts is fast (~1s for ≤30 char text)
    subprocess.run(
        [sys.executable, "-m", "edge_tts",
         "--voice", voice, "--text", text,
         "--write-media", str(mp3)],
        check=True, capture_output=True, text=True,
    )
    # mp3 → wav 44.1kHz mono so apad downstream is byte-clean
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3),
         "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "1", str(dest)],
        check=True,
    )
    return dest


async def thai_tts_wav(
    *, client: PhayaClient | None, gcs: GcsStorage | None, text: str, dest: Path,
    source: str = "edge", voice: str | None = None,
) -> Path:
    """Route Thai TTS through the configured source. ``edge`` is free and
    sounds more natural for >฿1,500 affiliate price bands.

    ``client`` and ``gcs`` are required only for the ``phaya`` source;
    pass ``None`` when using ``edge`` (the default)."""
    if source == "edge":
        return await _edge_tts_wav(
            text=text, dest=dest,
            voice=voice or "th-TH-NiwatNeural",
        )
    if source == "phaya":
        if client is None or gcs is None:
            raise RuntimeError(
                "phaya TTS source requires a PhayaClient + GcsStorage "
                "(got client=None or gcs=None)"
            )
        return await _phaya_tts_wav(client=client, gcs=gcs, text=text, dest=dest)
    raise ValueError(f"unknown tts source: {source!r}")


async def run_seedance_2kf(
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
    normalize_mp4(raw, dest, target_duration_s=shot.duration_s)


async def run_higgsfield_cli(
    *, hf: HiggsfieldCli, shot: AiShot, still: Path, workdir: Path, dest: Path,
) -> None:
    """Dispatch a shot through the Higgsfield CLI (`higgsfield generate
    create <model> ...`). The model is taken from ``shot.higgsfield_model``;
    optional ``higgsfield_mode`` and ``higgsfield_resolution`` override the
    defaults (Fast / 720p — cheapest tier).

    For two-keyframe shots (``shot.keyframes`` set), the start_ref and
    end_ref local stills are passed as ``--start-image`` and
    ``--end-image``; the CLI auto-uploads them.

    For single-image shots (no keyframes), the per-shot scene still is
    passed as ``--image``.

    The CLI emits a CloudFront URL on its final stdout line — we curl
    it down + normalize to canonical AAC so concat is clean.
    """
    model = shot.higgsfield_model or ""
    mode = shot.higgsfield_mode
    resolution = shot.higgsfield_resolution or "720p"

    print(f"   ↳ Higgsfield CLI · model={model} · mode={mode or 'default'} · {resolution}")

    if shot.keyframes is not None:
        start_local = workdir / shot.keyframes.start_ref
        end_local = workdir / shot.keyframes.end_ref
        for p in (start_local, end_local):
            if not p.exists():
                raise RuntimeError(f"{shot.shot_id}: keyframe missing: {p}")
        images = {
            "start-image": str(start_local.resolve()),
            "end-image": str(end_local.resolve()),
        }
        prompt = shot.keyframes.motion_label
    else:
        images = {"image": str(still.resolve())}
        prompt = shot.image_prompt

    duration_int = max(4, min(15, round(shot.duration_s)))

    try:
        result = await hf.generate_video(
            model=model, prompt=prompt,
            aspect_ratio=shot.aspect_ratio,
            duration=duration_int,
            mode=mode, resolution=resolution,
            images=images,
        )
    except HiggsfieldCliError as e:
        raise RuntimeError(f"{shot.shot_id}: higgsfield_cli failed: {e}") from e

    raw = workdir / f"{shot.shot_id}_higgsfield_raw.mp4"
    await hf.download(result.video_url, raw)
    normalize_mp4(raw, dest, target_duration_s=shot.duration_s)


async def run_seedance_2_2kf(
    *, seedance2: Seedance2Client, gcs: GcsStorage, key_prefix: str,
    shot: AiShot, workdir: Path, dest: Path, variant: str,
) -> None:
    """Seedance 2.0 two-keyframe via PiAPI direct.

    Mirror of run_seedance_2kf but routes through PiAPI's
    `first_last_frames` task type — +31.7 physics-accuracy vs 1.5 Pro
    per Megaton benchmark. Fast tier (~$0.08/s) for cost-sensitive,
    Pro tier (~$0.10/s) for hero shots.
    """
    if shot.keyframes is None:
        raise RuntimeError(f"{shot.shot_id}: {variant} requires keyframes block")
    start_local = workdir / shot.keyframes.start_ref
    end_local = workdir / shot.keyframes.end_ref
    for p in (start_local, end_local):
        if not p.exists():
            raise RuntimeError(f"{shot.shot_id}: keyframe missing: {p}")

    print(f"   ↳ Seedance 2.0 ({variant}) · motion={shot.keyframes.motion_label!r}")
    start_key = f"{key_prefix}/{shot.shot_id}_start.jpg"
    end_key = f"{key_prefix}/{shot.shot_id}_end.jpg"

    def _upload(local: Path, key: str) -> str:
        gcs.upload_file(local, key=key, content_type="image/jpeg",
                        cache_control="public, max-age=3600")
        return gcs.signed_url(key, ttl=timedelta(hours=1))

    start_url = await asyncio.to_thread(_upload, start_local, start_key)
    end_url = await asyncio.to_thread(_upload, end_local, end_key)

    model = "seedance-2-fast" if variant == "fast" else "seedance-2"
    # PiAPI accepts integer-seconds for `duration`; cap to shot duration
    duration_int = max(4, min(12, round(shot.duration_s)))

    try:
        job = await seedance2.create_first_last_frames(
            first_frame_url=start_url, last_frame_url=end_url,
            prompt=shot.keyframes.motion_label,
            model=model, duration_s=duration_int,
            resolution="720p", aspect_ratio=shot.aspect_ratio,
        )
        completed = await seedance2.wait_for_task(
            job.task_id, interval_s=4.0, timeout_s=600.0,
        )
    except Seedance2Error as e:
        raise RuntimeError(f"{shot.shot_id}: seedance2 failed: {e}") from e

    raw = workdir / f"{shot.shot_id}_seedance2_raw.mp4"
    await seedance2.download_video(completed.video_url, raw)
    normalize_mp4(raw, dest, target_duration_s=shot.duration_s)


def concat_clips(clips: list[Path], workdir: Path, out: Path) -> None:
    listfile = workdir / "concat.txt"
    listfile.write_text("\n".join(f"file '{p.resolve()}'" for p in clips))
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(listfile), "-c", "copy", str(out)],
        check=True,
    )


def mix_music_under(video: Path, music: Path, out: Path, *, gain_db: float = -12.0) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-i", str(video), "-i", str(music),
         "-filter_complex",
         f"[1:a]volume={gain_db}dB[m];[0:a][m]amix=inputs=2:duration=longest:dropout_transition=0[mix]",
         "-map", "0:v", "-map", "[mix]",
         "-c:v", "copy", *aac_flags(), "-shortest", str(out)],
        check=True,
    )


def build_subtitle_overlays(sb: AiStoryboard, shot_offsets: dict[str, float]) -> list[HyperframeOverlay]:
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
