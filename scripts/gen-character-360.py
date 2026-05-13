#!/usr/bin/env python3
"""Character-360 generator — identity-lock reference views per character.

For each character in the roster JSON:
  1. Generate the HERO portrait (no image_input — fresh)
  2. Generate every other view with image_input=[hero_canonical_url]
     so face/hair/build/costume stay consistent across angles
  3. Save all views locally + upload to GCS
  4. Build a printable character-360 sheet (one row per character,
     5 views per row + identity description)

The hero portrait's GCS signed URL becomes the canonical reference
passed to ALL subsequent scene-still re-generations (and is what locks
character identity across scenes).

Usage:
    .venv/bin/python scripts/gen-character-360.py \\
        --item-id 28875679676 \\
        --roster data/registry/items/28875679676/concept-2-character-roster.json \\
        --workdir out/maono-concept-2-workdir/characters \\
        --sheet out/maono-concept-2-character-360-sheet.png
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import timedelta
from pathlib import Path
from typing import Any

import httpx
from PIL import Image, ImageDraw, ImageFont
from pydantic import SecretStr

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from auto_affi.adapters.gcs_storage import GcsStorage
from auto_affi.adapters.gemini_image import (
    GEMINI_NANO_BANANA_PRO,
    GeminiImageClient,
    write_image_to_path,
)
from auto_affi.adapters.phaya import JobState, PhayaClient


# -----------------------------------------------------------------------
# Font helpers (Thai-capable per the storyboard-sheet conventions)
# -----------------------------------------------------------------------
def _load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates_bold = [
        "/System/Library/Fonts/Supplemental/Krungthep.ttf",
        "/System/Library/Fonts/Supplemental/Ayuthaya.ttf",
    ]
    candidates_regular = [
        "/System/Library/Fonts/Supplemental/Ayuthaya.ttf",
        "/System/Library/Fonts/Supplemental/Sathu.ttf",
    ]
    for c in (candidates_bold if bold else candidates_regular):
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


# -----------------------------------------------------------------------
# View generator
# -----------------------------------------------------------------------
async def _download(url: str, dest: Path) -> None:
    async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as c:
        r = await c.get(url)
        r.raise_for_status()
        dest.write_bytes(r.content)


async def _generate_view_phaya(
    *,
    client: PhayaClient,
    gcs: GcsStorage,
    bucket: str,
    char_id: str,
    view_id: str,
    prompt: str,
    image_input_urls: list[str] | None,
    workdir: Path,
) -> tuple[Path, str]:
    """Generate one character view via Phaya Nano Banana 2."""
    print(f"    view {view_id}: {'with ref' if image_input_urls else 'fresh (no ref)'} · engine=phaya")
    submit = await client.create_nano_banana_image(
        prompt=prompt, aspect_ratio="9:16", resolution="1K",
        image_input=image_input_urls,
    )
    if not submit.ok or submit.data is None:
        raise RuntimeError(f"submit failed: {submit.error}")
    wait = await client.wait_for_nano_banana(submit.data.job_id)
    if not wait.ok or wait.data is None or wait.data.state is not JobState.COMPLETED:
        raise RuntimeError(f"render failed: {wait.error}")
    if not wait.data.result_url:
        raise RuntimeError("completed but no URL")
    canonical = wait.data.result_url

    local = workdir / f"{char_id}-{view_id}.jpg"
    if canonical.startswith(f"gs://{bucket}/"):
        key = canonical[len(f"gs://{bucket}/"):]
        signed = await asyncio.to_thread(gcs.signed_url, key, ttl=timedelta(hours=1))
        await _download(signed, local)
    elif canonical.startswith("http"):
        await _download(canonical, local)
        ckey = f"characters/{char_id}/{view_id}.jpg"
        await asyncio.to_thread(
            gcs.upload_file, local, key=ckey, content_type="image/jpeg",
            cache_control="public, max-age=3600",
        )
        signed = await asyncio.to_thread(gcs.signed_url, ckey, ttl=timedelta(hours=1))
    else:
        raise RuntimeError(f"unrecognised URL scheme: {canonical[:60]}")
    return local, signed


async def _generate_view_gemini(
    *,
    client: GeminiImageClient,
    gcs: GcsStorage,
    item_id: int,
    char_id: str,
    view_id: str,
    prompt: str,
    reference_image_paths: list[Path] | None,
    workdir: Path,
) -> tuple[Path, str]:
    """Generate one character view via Gemini Nano Banana Pro 2.

    Gemini accepts reference images as inline base64 (read from local paths).
    No GCS upload needed for references — Gemini consumes them in-request.
    """
    print(f"    view {view_id}: {'with ref' if reference_image_paths else 'fresh (no ref)'} · engine=gemini")
    r = await client.create_image(
        prompt=prompt, aspect_ratio="9:16",
        reference_images=reference_image_paths,
    )
    if not r.ok or r.data is None:
        raise RuntimeError(f"gemini: {r.error}")
    local = workdir / f"{char_id}-{view_id}.jpg"
    # Gemini returns PNG by default; we keep .jpg ext for backward compat with downstream sheet builder
    write_image_to_path(r.data, local)
    # Upload to bucket for signed URL (so Phaya Seedance downstream can fetch it later)
    ckey = f"items/{item_id}/characters/{char_id}-{view_id}.jpg"
    await asyncio.to_thread(
        gcs.upload_file, local, key=ckey, content_type=r.data.mime_type,
        cache_control="public, max-age=3600",
    )
    signed = await asyncio.to_thread(gcs.signed_url, ckey, ttl=timedelta(hours=1))
    return local, signed


# -----------------------------------------------------------------------
# Sheet builder
# -----------------------------------------------------------------------
THUMB_W = 360
THUMB_H = 640
COL_GAP = 24
ROW_GAP = 60
MARGIN = 60
HEADER_H = 220
TEXT_COL_W = 540
BG_COLOR = (250, 248, 244)
TEXT_COLOR = (32, 32, 36)
SUBTLE_COLOR = (120, 120, 130)
ACCENT_COLOR = (180, 100, 50)


def build_character_sheet(
    *,
    roster: dict[str, Any],
    workdir: Path,
    output: Path,
) -> None:
    chars = roster["characters"]
    max_views = max(len(c["views"]) for c in chars)
    row_block_w = (THUMB_W + COL_GAP) * max_views + TEXT_COL_W
    sheet_w = MARGIN * 2 + row_block_w
    row_h = THUMB_H + ROW_GAP
    sheet_h = MARGIN * 2 + HEADER_H + row_h * len(chars)
    sheet = Image.new("RGB", (sheet_w, sheet_h), BG_COLOR)
    draw = ImageDraw.Draw(sheet)

    f_title = _load_font(56, bold=True)
    f_subtitle = _load_font(24)
    f_char_label = _load_font(34, bold=True)
    f_view = _load_font(18, bold=True)
    f_desc = _load_font(20)

    # Header
    draw.text(
        (MARGIN, MARGIN),
        f"Character 360 · {roster.get('concept_id', '')}",
        fill=TEXT_COLOR, font=f_title,
    )
    draw.text(
        (MARGIN, MARGIN + 70),
        "Identity-locked reference views — approved hero portrait drives all scene-stills",
        fill=SUBTLE_COLOR, font=f_subtitle,
    )
    draw.line(
        [(MARGIN, MARGIN + HEADER_H - 8), (sheet_w - MARGIN, MARGIN + HEADER_H - 8)],
        fill=ACCENT_COLOR, width=3,
    )

    y = MARGIN + HEADER_H
    for char in chars:
        # Place views
        x = MARGIN
        for view in char["views"]:
            view_id = view["view_id"]
            jpg = workdir / f"{char['char_id']}-{view_id}.jpg"
            if jpg.exists():
                thumb = Image.open(jpg).convert("RGB")
                thumb = thumb.resize((THUMB_W, THUMB_H), Image.LANCZOS)
                sheet.paste(thumb, (x, y))
                # Hero badge for canonical
                if view.get("is_canonical_reference"):
                    draw.rectangle(
                        [(x + 12, y + 12), (x + 12 + 110, y + 12 + 44)],
                        fill=ACCENT_COLOR,
                    )
                    draw.text(
                        (x + 22, y + 18),
                        "HERO",
                        fill=(255, 255, 255), font=f_view,
                    )
                # View id label below
                draw.text(
                    (x + 4, y + THUMB_H + 8),
                    view_id,
                    fill=TEXT_COLOR, font=f_view,
                )
            draw.rectangle(
                [(x, y), (x + THUMB_W, y + THUMB_H)],
                outline=(40, 40, 50), width=2,
            )
            x += THUMB_W + COL_GAP

        # Character text column
        tx = MARGIN + (THUMB_W + COL_GAP) * len(char["views"]) + 12
        draw.text(
            (tx, y),
            f"{char['display_name_th']}  ·  {char['display_name_en']}",
            fill=ACCENT_COLOR, font=f_char_label,
        )
        ty = y + 50
        # Wrap description text
        desc = char["identity_description"]
        # Naïve wrap to TEXT_COL_W
        words = desc.split(" ")
        line = ""
        line_height = 28
        for w in words:
            trial = (line + " " + w).strip()
            if f_desc.getbbox(trial)[2] <= TEXT_COL_W:
                line = trial
            else:
                draw.text((tx, ty), line, fill=TEXT_COLOR, font=f_desc)
                ty += line_height
                line = w
        if line:
            draw.text((tx, ty), line, fill=TEXT_COLOR, font=f_desc)
            ty += line_height

        ty += 20
        scenes = ", ".join(str(s) for s in char.get("appears_in_scenes", []))
        draw.text(
            (tx, ty),
            f"Appears in scenes: {scenes}",
            fill=SUBTLE_COLOR, font=f_desc,
        )

        y += row_h

    sheet.save(output, "PNG", optimize=True)
    print(f"\n✅ sheet written: {output} ({output.stat().st_size//1024} KB · {sheet_w}×{sheet_h})")


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
async def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--item-id", type=int, required=True)
    p.add_argument("--roster", type=Path, required=True)
    p.add_argument("--workdir", type=Path, required=True)
    p.add_argument("--sheet", type=Path, required=True)
    p.add_argument(
        "--engine", choices=["gemini", "phaya"], default="gemini",
        help="Image-gen engine. Default 'gemini' (Nano Banana Pro 2 via Gemini API "
             "as the user mandated). 'phaya' falls back to Phaya gateway.",
    )
    args = p.parse_args()

    bucket = os.environ.get("AUTO_AFFI__GCS_BUCKET", "").strip()
    if not bucket:
        print("ERROR: AUTO_AFFI__GCS_BUCKET required"); return 1
    gcs = GcsStorage(bucket_name=bucket)

    roster = json.loads(args.roster.read_text(encoding="utf-8"))
    args.workdir.mkdir(parents=True, exist_ok=True)
    args.sheet.parent.mkdir(parents=True, exist_ok=True)

    # Engine setup
    phaya_client: PhayaClient | None = None
    gemini_client: GeminiImageClient | None = None
    if args.engine == "phaya":
        key = os.environ.get("PHAYA_API_KEY", "").strip()
        if not key:
            print("ERROR: PHAYA_API_KEY missing"); return 1
        phaya_client = PhayaClient(
            api_key=SecretStr(key), timeout_s=60.0, gcs=gcs,
            gcs_key_prefix=f"items/{args.item_id}/characters",
        )
        bal0 = await phaya_client.get_credits()
        print(f"📊 phaya balance: ฿{bal0.data.balance_thb:.4f}")
    else:
        gkey = os.environ.get("GOOGLE_API_KEY", "").strip()
        if not gkey:
            print("ERROR: GOOGLE_API_KEY missing (needed for --engine gemini)"); return 1
        gemini_client = GeminiImageClient(
            api_key=SecretStr(gkey), model=GEMINI_NANO_BANANA_PRO,
        )
        print(f"📊 engine: Gemini {GEMINI_NANO_BANANA_PRO}")
    print(f"📋 roster: {len(roster['characters'])} characters")

    # Generate per character
    canonical_refs: dict[str, str] = {}
    for char in roster["characters"]:
        cid = char["char_id"]
        print(f"\n── character: {cid} ({char['display_name_en']})")
        hero_signed_url: str | None = None
        hero_local_path: Path | None = None
        for view in char["views"]:
            view_id = view["view_id"]
            target_jpg = args.workdir / f"{cid}-{view_id}.jpg"
            if target_jpg.exists() and target_jpg.stat().st_size > 10_000:
                print(f"    view {view_id}: cached ({target_jpg.stat().st_size//1024} KB)")
                if view.get("is_canonical_reference"):
                    key_in_bucket = f"items/{args.item_id}/characters/{cid}-{view_id}.jpg"
                    await asyncio.to_thread(
                        gcs.upload_file, target_jpg, key=key_in_bucket,
                        content_type="image/jpeg", cache_control="public, max-age=3600",
                    )
                    hero_signed_url = await asyncio.to_thread(
                        gcs.signed_url, key_in_bucket, ttl=timedelta(hours=1)
                    )
                    hero_local_path = target_jpg
                continue

            try:
                if args.engine == "phaya":
                    assert phaya_client is not None
                    ref_urls = [hero_signed_url] if (hero_signed_url and not view.get("is_canonical_reference")) else None
                    _, signed = await _generate_view_phaya(
                        client=phaya_client, gcs=gcs, bucket=bucket,
                        char_id=cid, view_id=view_id,
                        prompt=view["prompt"], image_input_urls=ref_urls,
                        workdir=args.workdir,
                    )
                else:
                    assert gemini_client is not None
                    ref_paths = [hero_local_path] if (hero_local_path and not view.get("is_canonical_reference")) else None
                    local_path, signed = await _generate_view_gemini(
                        client=gemini_client, gcs=gcs, item_id=args.item_id,
                        char_id=cid, view_id=view_id,
                        prompt=view["prompt"], reference_image_paths=ref_paths,
                        workdir=args.workdir,
                    )
                    if view.get("is_canonical_reference"):
                        hero_local_path = local_path
            except Exception as e:
                print(f"    ❌ view {view_id} failed: {e}")
                continue
            if view.get("is_canonical_reference"):
                hero_signed_url = signed
        if hero_signed_url:
            canonical_refs[cid] = hero_signed_url

    if args.engine == "phaya":
        assert phaya_client is not None
        bal1 = await phaya_client.get_credits()
        spent = bal0.data.balance_thb - bal1.data.balance_thb
        print(f"\n📊 phaya balance: ฿{bal1.data.balance_thb:.4f}  (spent ฿{spent:.4f})")

    # Build the sheet
    build_character_sheet(roster=roster, workdir=args.workdir, output=args.sheet)

    # Persist canonical references for the next stage
    refs_out = args.workdir / "canonical-refs.json"
    refs_out.write_text(
        json.dumps({"item_id": args.item_id, "canonical_refs": canonical_refs}, indent=2),
        encoding="utf-8",
    )
    print(f"✅ refs persisted: {refs_out}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
