#!/usr/bin/env python3
"""Validate HyperFrames captions against an approved segmented voice report."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


CAPTION_RE = re.compile(r'id=["\']cap-(\d+)["\'][^>]*>(.*?)</div>', re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")


def normalize_text(value: str) -> str:
    without_tags = TAG_RE.sub("", value)
    unescaped = html.unescape(without_tags)
    return re.sub(r"\s+", " ", unescaped).strip()


def load_captions(index_html: Path) -> list[dict[str, Any]]:
    body = index_html.read_text(encoding="utf-8")
    captions = []
    for match in CAPTION_RE.finditer(body):
        captions.append({"id": int(match.group(1)), "text": normalize_text(match.group(2))})
    captions.sort(key=lambda row: row["id"])
    return captions


def load_voice_segments(report_path: Path) -> list[dict[str, Any]]:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    segments = report.get("segments")
    if not isinstance(segments, list):
        raise ValueError(f"{report_path} does not contain a list at key 'segments'")
    out = []
    for index, segment in enumerate(segments, start=1):
        text = segment.get("text") if isinstance(segment, dict) else None
        if not isinstance(text, str):
            raise ValueError(f"segment {index} in {report_path} has no string 'text'")
        out.append({"id": index, "text": normalize_text(text)})
    return out


def validate(index_html: Path, voice_report: Path) -> dict[str, Any]:
    captions = load_captions(index_html)
    voice_segments = load_voice_segments(voice_report)
    mismatches = []
    max_len = max(len(captions), len(voice_segments))
    for idx in range(max_len):
        caption = captions[idx] if idx < len(captions) else None
        voice = voice_segments[idx] if idx < len(voice_segments) else None
        if caption is None or voice is None:
            mismatches.append(
                {
                    "index": idx + 1,
                    "caption": caption["text"] if caption else None,
                    "voice": voice["text"] if voice else None,
                    "reason": "count_mismatch",
                }
            )
            continue
        if caption["text"] != voice["text"]:
            mismatches.append(
                {
                    "index": idx + 1,
                    "caption": caption["text"],
                    "voice": voice["text"],
                    "reason": "text_mismatch",
                }
            )
    return {
        "ok": not mismatches and len(captions) == len(voice_segments),
        "caption_count": len(captions),
        "voice_segment_count": len(voice_segments),
        "mismatches": mismatches,
        "index_html": str(index_html),
        "voice_report": str(voice_report),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", required=True, type=Path, help="HyperFrames index.html")
    parser.add_argument("--voice-report", required=True, type=Path, help="Voice generation report JSON")
    parser.add_argument("--output-json", type=Path, help="Optional path for the validation report")
    args = parser.parse_args()

    result = validate(args.html, args.voice_report)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
