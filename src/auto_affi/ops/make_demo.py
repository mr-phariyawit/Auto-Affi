"""CLI: produce a 9:16 demo mp4 with no vendor credentials.

Usage::

    uv run python -m auto_affi.ops.make_demo --output out/demo.mp4

The output is a real, playable mp4 rendered locally via PIL + espeak-ng +
ffmpeg. Image and TTS quality are placeholder-grade; the artefact exists
so the rest of the system (schemas, validators, publishing flow,
analytics) can be exercised end-to-end before Veo / ElevenLabs / Shopee
credentials are issued.
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from auto_affi.pipeline.demo_storyboard import build_demo_storyboard
from auto_affi.pipeline.local_renderer import RenderResult, render_storyboard


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a demo 9:16 mp4 locally")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("out/demo.mp4"),
        help="output mp4 path (default: out/demo.mp4)",
    )
    parser.add_argument(
        "--no-tts",
        action="store_true",
        help="skip espeak-ng narration (use silent audio)",
    )
    args = parser.parse_args(argv)

    storyboard = build_demo_storyboard()
    with tempfile.TemporaryDirectory(prefix="auto-affi-demo-") as tmp:
        result: RenderResult = render_storyboard(
            storyboard,
            workdir=Path(tmp),
            output_path=args.output,
            enable_tts=not args.no_tts,
        )

    print(
        f"OK: rendered {result.scene_count} scenes, {result.duration_s:.1f}s -> {result.mp4_path}"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover -- CLI entrypoint
    raise SystemExit(main())
