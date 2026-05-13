#!/usr/bin/env python3
"""Build a storyboard approval sheet for a concept run.

Generates any missing scene images via Phaya Nano Banana 2 (using existing
ones if already in the workdir), then composes a single PNG storyboard
sheet with one row per frame: thumbnail + frame metadata (timestamp,
duration, purpose, dialogue, on-screen text, AI image prompt snippet).

Usage:
    .venv/bin/python scripts/build-storyboard-sheet.py \\
        --item-id 28875679676 \\
        --workdir out/maono-concept-2-workdir \\
        --output  out/maono-concept-2-storyboard-sheet.png

The sheet is the human-review gate before the expensive i2v phase fires.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pydantic import SecretStr

# Make `src/auto_affi/...` importable when running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from auto_affi.adapters.phaya import JobState, PhayaClient
from auto_affi.registry import LocalJsonlRegistry


# Layout constants — tuned for A2-portrait readability
THUMB_W = 540          # scene thumbnail width (preserves 9:16)
THUMB_H = 960          # scene thumbnail height
ROW_GAP_PX = 32        # vertical gap between rows
COL_GAP_PX = 40        # horizontal gap between thumb and text
TEXT_W = 800           # text column width
MARGIN_PX = 60
HEADER_H = 220
BG_COLOR = (250, 248, 244)   # off-white paper
TEXT_COLOR = (32, 32, 36)
SUBTLE_COLOR = (120, 120, 130)
ACCENT_COLOR = (180, 100, 50)


def _load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    # Thai-capable fonts come first so Thai glyphs render (not tofu boxes).
    # Ayuthaya = clean body text (both Thai + Latin)
    # Krungthep = heavier weight for headings (both Thai + Latin)
    candidates_bold = [
        "/System/Library/Fonts/Supplemental/Krungthep.ttf",
        "/System/Library/Fonts/Supplemental/Silom.ttf",
        "/System/Library/Fonts/Supplemental/Ayuthaya.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    candidates_regular = [
        "/System/Library/Fonts/Supplemental/Ayuthaya.ttf",
        "/System/Library/Fonts/Supplemental/Sathu.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for c in (candidates_bold if bold else candidates_regular):
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


async def _ensure_image(
    client: PhayaClient, *, idx: int, prompt: str, workdir: Path
) -> Path:
    """Generate (or reuse) scene image at workdir/s{idx}-image.jpg."""
    target = workdir / f"s{idx}-image.jpg"
    if target.exists() and target.stat().st_size > 10_000:
        print(f"  scene {idx}: cached ({target.stat().st_size//1024} KB)")
        return target
    print(f"  scene {idx}: generating (nano-banana-2, 9:16, 1K)…")
    submit = await client.create_nano_banana_image(
        prompt=prompt, aspect_ratio="9:16", resolution="1K"
    )
    if not submit.ok or submit.data is None:
        raise RuntimeError(f"scene {idx} submit failed: {submit.error}")
    wait = await client.wait_for_nano_banana(submit.data.job_id)
    if not wait.ok or wait.data is None or wait.data.state is not JobState.COMPLETED:
        raise RuntimeError(f"scene {idx} render failed: {wait.error}")
    if not wait.data.result_url:
        raise RuntimeError(f"scene {idx} completed but no URL")
    # Download to local workdir
    import httpx
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as h:
        r = await h.get(wait.data.result_url)
        r.raise_for_status()
        target.write_bytes(r.content)
    print(f"  scene {idx}: written ({target.stat().st_size//1024} KB)")
    return target


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Naive word-wrap; works for English + Thai (Thai has no spaces, fall back to per-character chunking)."""
    if not text:
        return []
    if " " in text:
        words = text.split(" ")
        lines: list[str] = []
        current = ""
        for w in words:
            trial = f"{current} {w}".strip()
            if font.getbbox(trial)[2] <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines
    # No spaces — chunk by char-count that fits max_width
    out: list[str] = []
    buf = ""
    for ch in text:
        if font.getbbox(buf + ch)[2] <= max_width:
            buf += ch
        else:
            if buf:
                out.append(buf)
            buf = ch
    if buf:
        out.append(buf)
    return out


def _draw_text_block(
    draw: ImageDraw.ImageDraw,
    *,
    x: int,
    y: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
    line_height: int,
    color: tuple[int, int, int],
) -> int:
    """Draw wrapped text; return final y after the block."""
    for line in _wrap_text(text, font, max_width):
        draw.text((x, y), line, fill=color, font=font)
        y += line_height
    return y


def build_sheet(
    *,
    frames: list[dict],
    workdir: Path,
    output: Path,
    title: str,
    subtitle: str,
) -> None:
    n = len(frames)
    body_h = n * (THUMB_H + ROW_GAP_PX) - ROW_GAP_PX
    sheet_w = MARGIN_PX * 2 + THUMB_W + COL_GAP_PX + TEXT_W
    sheet_h = MARGIN_PX * 2 + HEADER_H + body_h

    sheet = Image.new("RGB", (sheet_w, sheet_h), BG_COLOR)
    draw = ImageDraw.Draw(sheet)

    f_title = _load_font(60, bold=True)
    f_subtitle = _load_font(28)
    f_frame_label = _load_font(36, bold=True)
    f_meta = _load_font(24)
    f_dialogue = _load_font(28)
    f_prompt = _load_font(20)
    f_caption = _load_font(20)

    # Header
    draw.text((MARGIN_PX, MARGIN_PX), title, fill=TEXT_COLOR, font=f_title)
    draw.text((MARGIN_PX, MARGIN_PX + 80), subtitle, fill=SUBTLE_COLOR, font=f_subtitle)
    draw.line(
        [(MARGIN_PX, MARGIN_PX + HEADER_H - 8),
         (sheet_w - MARGIN_PX, MARGIN_PX + HEADER_H - 8)],
        fill=ACCENT_COLOR, width=3,
    )

    # Rows
    y = MARGIN_PX + HEADER_H
    for f in frames:
        idx = f["idx"]
        img_path = workdir / f"s{idx}-image.jpg"
        thumb = Image.open(img_path).convert("RGB")
        thumb = thumb.resize((THUMB_W, THUMB_H), Image.LANCZOS)
        sheet.paste(thumb, (MARGIN_PX, y))
        # Thin border on the thumbnail
        draw.rectangle(
            [(MARGIN_PX, y), (MARGIN_PX + THUMB_W, y + THUMB_H)],
            outline=(40, 40, 50), width=2,
        )
        # Frame number badge
        draw.rectangle(
            [(MARGIN_PX + 16, y + 16), (MARGIN_PX + 16 + 84, y + 16 + 56)],
            fill=ACCENT_COLOR,
        )
        draw.text(
            (MARGIN_PX + 24, y + 16),
            f"#{idx+1}",
            fill=(255, 255, 255), font=f_frame_label,
        )

        # Text column
        tx = MARGIN_PX + THUMB_W + COL_GAP_PX
        ty = y + 4

        t_start, t_end = f["timestamp_s"]
        purpose = f.get("purpose", "")
        meta_line = f"FRAME {idx+1}  ·  {t_start:.1f}–{t_end:.1f}s  ·  {f.get('duration_s', t_end - t_start):.1f}s  ·  {purpose.upper()}"
        draw.text((tx, ty), meta_line, fill=ACCENT_COLOR, font=f_frame_label)
        ty += 50

        ty = _draw_text_block(
            draw, x=tx, y=ty,
            text=f"Shot: {f.get('shot_size', '')} · {f.get('camera_movement', '')}",
            font=f_meta, max_width=TEXT_W, line_height=32, color=SUBTLE_COLOR,
        )
        ty += 12

        ty = _draw_text_block(
            draw, x=tx, y=ty,
            text=f"Scene: {f.get('scene_location', '')}",
            font=f_meta, max_width=TEXT_W, line_height=32, color=SUBTLE_COLOR,
        )
        ty += 12

        ty = _draw_text_block(
            draw, x=tx, y=ty,
            text=f"Emotion: {f.get('emotional_intention', '')}",
            font=f_meta, max_width=TEXT_W, line_height=32, color=SUBTLE_COLOR,
        )
        ty += 18

        if f.get("dialogue_th"):
            draw.text((tx, ty), "Dialogue (Thai):", fill=TEXT_COLOR, font=f_frame_label)
            ty += 44
            ty = _draw_text_block(
                draw, x=tx, y=ty,
                text=f["dialogue_th"],
                font=f_dialogue, max_width=TEXT_W, line_height=36, color=TEXT_COLOR,
            )
            ty += 18
        if f.get("on_screen_text_th"):
            draw.text((tx, ty), "On-screen text:", fill=TEXT_COLOR, font=f_frame_label)
            ty += 44
            ty = _draw_text_block(
                draw, x=tx, y=ty,
                text=f["on_screen_text_th"],
                font=f_dialogue, max_width=TEXT_W, line_height=36, color=ACCENT_COLOR,
            )
            ty += 18

        if f.get("ai_image_prompt"):
            draw.text((tx, ty), "AI image prompt:", fill=TEXT_COLOR, font=f_frame_label)
            ty += 44
            # Trim to ~600 chars for sheet readability — full prompt is in the JSON file
            snippet = f["ai_image_prompt"]
            if len(snippet) > 600:
                snippet = snippet[:600] + "…"
            ty = _draw_text_block(
                draw, x=tx, y=ty,
                text=snippet,
                font=f_prompt, max_width=TEXT_W, line_height=28, color=SUBTLE_COLOR,
            )

        y += THUMB_H + ROW_GAP_PX

    sheet.save(output, "PNG", optimize=True)
    print(f"\n✅ sheet written: {output} ({output.stat().st_size//1024} KB · {sheet_w}×{sheet_h})")


async def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--item-id", type=int, required=True)
    p.add_argument("--workdir", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument(
        "--storyboard-json",
        type=Path,
        default=None,
        help="Path to concept-2-storyboard.json (defaults to data/registry/items/<item>/concept-2-storyboard.json)",
    )
    args = p.parse_args()

    if args.storyboard_json is None:
        args.storyboard_json = (
            Path("data/registry/items") / str(args.item_id) / "concept-2-storyboard.json"
        )

    storyboard = json.loads(args.storyboard_json.read_text(encoding="utf-8"))
    frames = storyboard["frames"]
    print(f"loaded {len(frames)} frames from {args.storyboard_json}")

    # Sync the prompts against the registry storyboard rows so we use whatever
    # the demo pipeline would use (which may have been trimmed if the schema
    # cap differs). For now we use the JSON file's prompts directly.

    args.workdir.mkdir(parents=True, exist_ok=True)

    key = os.environ.get("PHAYA_API_KEY", "").strip()
    if not key:
        print("ERROR: PHAYA_API_KEY missing"); return 1
    client = PhayaClient(api_key=SecretStr(key), timeout_s=60.0)
    bal0 = await client.get_credits()
    print(f"balance before: ฿{bal0.data.balance_thb:.4f}")

    print(f"\nGenerating/reusing images for {len(frames)} frames…")
    for f in frames:
        await _ensure_image(
            client, idx=f["idx"], prompt=f["ai_image_prompt"], workdir=args.workdir
        )

    bal1 = await client.get_credits()
    spent = bal0.data.balance_thb - bal1.data.balance_thb
    print(f"\nbalance after: ฿{bal1.data.balance_thb:.4f} (spent ฿{spent:.4f})")

    build_sheet(
        frames=frames,
        workdir=args.workdir,
        output=args.output,
        title=f"Storyboard · {storyboard.get('concept_title_en', '')}",
        subtitle=(
            f"{storyboard.get('concept_title_th', '')}  ·  "
            f"item {args.item_id}  ·  order 0001  ·  "
            f"{storyboard.get('length_s', '?')}s · {storyboard.get('platform', '?')} · {storyboard.get('aspect_ratio', '?')}"
        ),
    )
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
