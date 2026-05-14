#!/usr/bin/env python
"""Generate timed HyperFrames dialogue subtitles from a storyboard.

Implements the HSO×VCS Method's "captions on 100% of dialogue" principle
(NCAM +40% retention / Facebook +12% watch-time / dual-coding theory).

The pipeline:
1. Read storyboard JSON; find scenes with non-empty dialogue_th.
2. Probe the workdir for actual clip mp4 durations (NOT the storyboard's
   planned durations — Seedance/Veo produce slightly different lengths).
3. Compute the absolute timeline position of each dialogue-bearing scene.
4. Render one MOV per dialogue beat via the dialogue-subtitle HyperFrames
   template, with text + duration injected as --variables.
5. Composite all caption MOVs onto the base video.

Dialogue carrier: gen-video-seedance.py maps clip i = transition into
scene i+1, so clip i carries scene i+1's dialogue. Captions appear over
the clip whose end scene contains the dialogue.

Usage:
    .venv/bin/python scripts/gen-dialogue-captions.py \\
        --storyboard-json data/registry/items/28875679676/concept-2-storyboard.json \\
        --workdir out/maono-concept-2 \\
        --base-video out/maono-concept-2-final-v6.mp4 \\
        --output out/maono-concept-2-final-v7.mp4
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from auto_affi.post.hyperframes_renderer import (
    OverlayRender,
    composite_overlays_with_ffmpeg,
    render_storyboard_overlays,
)
from auto_affi.schemas.storyboard import HyperframeOverlay


def _ffprobe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def _scene_to_clip(scene_idx: int) -> int:
    """Map a scene index to the clip that carries its dialogue.

    Per gen-video-seedance.py the clip plan is:
        clip i = transition (s[i], s[i+1])  →  end_scene = frames[i+1]
                                              dialogue_th = end_scene.dialogue_th
    So scene N's dialogue is played during clip (N-1).
    Scene 0 has no preceding clip → returns -1 if dialogue lives there
    (caller should special-case scene 0 by overlaying at t=0 of clip 0).
    """
    return scene_idx - 1


def build_caption_overlays(
    *, storyboard: dict, workdir: Path,
) -> list[HyperframeOverlay]:
    """Compute HyperframeOverlay list with precise timeline positioning.

    Returns one overlay per dialogue-bearing scene, with `start_s` and
    `duration_s` resolved from actual clip durations in workdir.
    """
    frames = storyboard["frames"]
    n_clips = len(frames) - 1

    # Probe actual clip durations from workdir
    clip_durations: list[float] = []
    cumulative = 0.0
    clip_offsets: list[float] = []  # offset of clip i in final timeline
    for ci in range(n_clips):
        clip_path = workdir / f"clip{ci}-seedance-final.mp4"
        if not clip_path.exists():
            print(f"  ⚠️  missing {clip_path.name} — using storyboard target {frames[ci+1].get('duration_s', 5.0)}s")
            d = float(frames[ci + 1].get("duration_s", 5.0))
        else:
            d = _ffprobe_duration(clip_path)
        clip_durations.append(d)
        clip_offsets.append(cumulative)
        cumulative += d

    print(f"  📐 clip durations: {[f'{d:.2f}s' for d in clip_durations]}")
    print(f"  📐 cumulative offsets: {[f'{o:.2f}s' for o in clip_offsets]}")
    print(f"  📐 total timeline: {cumulative:.2f}s")

    overlays: list[HyperframeOverlay] = []
    for scene_idx, frame in enumerate(frames):
        dialogue = (frame.get("dialogue_th") or "").strip()
        if not dialogue:
            continue
        clip_idx = _scene_to_clip(scene_idx)
        if clip_idx < 0:
            # Scene 0 dialogue — overlay at t=0 of clip 0 (rare)
            start = 0.0
            duration = clip_durations[0] if clip_durations else 3.0
        else:
            if clip_idx >= len(clip_durations):
                print(f"  ⚠️  scene {scene_idx} dialogue but no clip {clip_idx} — skipping")
                continue
            start = clip_offsets[clip_idx]
            duration = clip_durations[clip_idx]

        print(f"  📝 scene {scene_idx} → clip {clip_idx} @ {start:.2f}s × {duration:.2f}s : {dialogue!r}")
        overlays.append(HyperframeOverlay(
            scene_idx=scene_idx,
            template="dialogue-subtitle",
            props={
                "text_th": dialogue,
                "start_s": start,
                "duration_s": duration,
            },
        ))
    return overlays


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--storyboard-json", type=Path, required=True)
    p.add_argument("--workdir", type=Path, required=True,
                   help="Directory containing clip{N}-seedance-final.mp4 files.")
    p.add_argument("--base-video", type=Path, required=True,
                   help="The final mp4 to composite captions onto.")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--hyperframes-projects-dir", type=Path,
                   default=Path("hyperframes"))
    p.add_argument("--overlays-workdir", type=Path, default=None,
                   help="Where to write rendered caption MOVs "
                        "(default: <workdir>/dialogue-captions).")
    args = p.parse_args()

    import json
    storyboard = json.loads(args.storyboard_json.read_text(encoding="utf-8"))
    overlays_workdir = args.overlays_workdir or (args.workdir / "dialogue-captions")
    overlays_workdir.mkdir(parents=True, exist_ok=True)

    print(f"📜 storyboard: {args.storyboard_json}")
    print(f"🎞️  base:       {args.base_video} ({_ffprobe_duration(args.base_video):.2f}s)")

    overlays = build_caption_overlays(storyboard=storyboard, workdir=args.workdir)
    if not overlays:
        print(f"⚠️  no dialogue scenes found — copying base to output as-is")
        subprocess.run(["cp", str(args.base_video), str(args.output)], check=True)
        return 0

    print(f"\n🎨 rendering {len(overlays)} caption overlay(s)…")
    rendered = render_storyboard_overlays(
        overlays=overlays,
        projects_dir=args.hyperframes_projects_dir,
        output_dir=overlays_workdir,
    )
    if not rendered:
        print(f"❌ no overlays rendered — bailing")
        return 2

    print(f"\n🎬 compositing {len(rendered)} overlay(s) onto {args.base_video.name}…")
    composite_overlays_with_ffmpeg(
        base_video=args.base_video, overlays=rendered, output=args.output,
    )
    out_dur = _ffprobe_duration(args.output)
    size_mb = args.output.stat().st_size / 1024 / 1024
    print(f"\n✅ {args.output} ({size_mb:.1f} MB, {out_dur:.2f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
