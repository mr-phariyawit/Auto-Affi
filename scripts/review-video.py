#!/usr/bin/env python3
"""Review a video-production run — feedback-loop entry point.

Compares per-scene clips (ffmpeg-extracted first/last frames) against the
storyboard intent and emits a markdown + JSON review report.

Usage:
    .venv/bin/python scripts/review-video.py \\
        --item-id 28875679676 \\
        --workdir out/maono-concept-2-workdir \\
        --storyboard-json data/registry/items/28875679676/concept-2-storyboard.json \\
        --output-md out/maono-concept-2-review.md \\
        --output-json out/maono-concept-2-review.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Make `src/auto_affi/...` importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from auto_affi.qa.video_review import render_report_md, review_video_run


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--item-id", type=int, required=True)
    p.add_argument("--order-no", type=int, default=1)
    p.add_argument("--run-no", type=int, default=0)
    p.add_argument("--run-id", type=str, default="")
    p.add_argument("--workdir", type=Path, required=True)
    p.add_argument("--storyboard-json", type=Path, required=True)
    p.add_argument("--output-md", type=Path, required=True)
    p.add_argument("--output-json", type=Path, default=None)
    args = p.parse_args()

    print(f"reviewing run #{args.run_no:04d} (item {args.item_id})…")
    report = review_video_run(
        storyboard_json_path=args.storyboard_json,
        workdir=args.workdir,
        run_id=args.run_id,
        item_id=args.item_id,
        order_no=args.order_no,
        run_no=args.run_no,
    )
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_report_md(report), encoding="utf-8")
    print(f"✅ review written: {args.output_md}")

    if args.output_json is not None:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ json written:   {args.output_json}")

    print()
    print(f"scenes reviewed: {len(report.reviews)}")
    print(f"static ratio:    {report.overall_static_ratio*100:.0f}%")
    print(f"overall:         {report.overall_recommendation}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
