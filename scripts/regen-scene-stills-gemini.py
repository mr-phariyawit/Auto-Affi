#!/usr/bin/env python3
"""Regenerate scene stills via Gemini Nano Banana Pro 2 with hero refs.

Reads the storyboard JSON for per-scene prompts, the character roster
JSON for which characters appear in which scene, and the pre-generated
character-360 hero portraits (local paths) as reference images.

For each scene:
  - Identify which character heroes belong (per roster's appears_in_scenes)
  - Build reference_images list with their hero portrait local paths
  - Call Gemini Nano Banana Pro 2 with the scene's rich AI prompt + refs
  - Save the still locally + upload to GCS under the run prefix

Scenes 0 and 1 have no characters; they're copied as-is from a base
workdir (no spend) unless --regen-all is set.

Usage:
    .venv/bin/python scripts/regen-scene-stills-gemini.py \\
        --item-id 28875679676 \\
        --storyboard-json data/registry/items/28875679676/concept-2-storyboard.json \\
        --roster data/registry/items/28875679676/concept-2-character-roster.json \\
        --character-workdir out/maono-concept-2-workdir/characters-gemini \\
        --base-workdir out/maono-concept-2-workdir/scene-stills-v2 \\
        --output-workdir out/maono-concept-2-workdir/scene-stills-v3 \\
        --sheet out/maono-concept-2-storyboard-sheet-v3.png
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

from pydantic import SecretStr

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from auto_affi.adapters.gcs_storage import GcsStorage
from auto_affi.adapters.gemini_image import (
    GEMINI_NANO_BANANA_PRO,
    GeminiImageClient,
    write_image_to_path,
)


def _scene_characters_map(roster: dict[str, Any]) -> dict[int, list[str]]:
    """Build {scene_idx: [char_id, ...]} from the roster's appears_in_scenes lists."""
    out: dict[int, list[str]] = {}
    for char in roster["characters"]:
        cid = char["char_id"]
        for s in char.get("appears_in_scenes", []):
            out.setdefault(int(s), []).append(cid)
    return out


_PRODUCT_ANCHOR_PROMPT_PREFIX = (
    "PRODUCT IDENTITY LOCK — The microphone visible in this frame MUST be "
    "the MAONO PD300X (a broadcast-style dynamic podcast mic, NOT a "
    "studio condenser): chunky black shock-mount cage half-encircling the "
    "body, side-address foam capsule (speak INTO the grey foam end "
    "horizontally — not vertical / not into the top), solid cylindrical "
    "matte-black metal body, 'maono' wordmark in flat lowercase white "
    "letters visible on the side, top-mounted gain knob with small green "
    "LED indicators and a control button. The attached product reference "
    "images show the exact product appearance — match them. Explicitly DO "
    "NOT depict a mesh-head condenser, a thin spring shock mount, or a "
    "vertically-addressed mic. "
)


async def _regenerate_scene(
    *,
    client: GeminiImageClient,
    gcs: GcsStorage,
    item_id: int,
    scene_idx: int,
    prompt: str,
    char_ids: list[str],
    character_workdir: Path,
    output_workdir: Path,
    product_refs: list[Path] | None = None,
    inject_product_anchor: bool = False,
) -> tuple[Path, str] | None:
    """Regen one scene still; return (local_path, gcs_signed_url) or None on failure."""
    refs: list[Path] = []
    for cid in char_ids:
        hero = character_workdir / f"{cid}-hero-portrait.jpg"
        if not hero.exists():
            print(f"    ❌ hero portrait missing for {cid}: {hero}")
            return None
        refs.append(hero)
    if product_refs:
        refs.extend(product_refs)

    if inject_product_anchor:
        prompt = _PRODUCT_ANCHOR_PROMPT_PREFIX + prompt

    char_label = "+".join(char_ids) if char_ids else "no-char"
    prod_label = f"+prod×{len(product_refs)}" if product_refs else ""
    print(f"  scene {scene_idx}: refs=[{char_label}{prod_label}] · prompt {len(prompt)} chars")

    r = await client.create_image(
        prompt=prompt,
        aspect_ratio="9:16",
        reference_images=refs if refs else None,
    )
    if not r.ok or r.data is None:
        print(f"    ❌ gemini: {r.error[:200]}")
        return None
    local = output_workdir / f"s{scene_idx}-image.jpg"
    write_image_to_path(r.data, local)

    # Upload to bucket so downstream (Seedance) has a stable signed URL
    key = f"items/{item_id}/scene-stills-v3/s{scene_idx}-image.jpg"
    await asyncio.to_thread(
        gcs.upload_file, local, key=key, content_type=r.data.mime_type,
        cache_control="public, max-age=3600",
    )
    signed = await asyncio.to_thread(gcs.signed_url, key, ttl=timedelta(hours=1))
    print(f"    ✅ {local.name} ({local.stat().st_size//1024} KB)")
    return local, signed


async def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--item-id", type=int, required=True)
    p.add_argument("--storyboard-json", type=Path, required=True)
    p.add_argument("--roster", type=Path, required=True)
    p.add_argument(
        "--character-workdir", type=Path, required=True,
        help="Where character hero portraits live (e.g. characters-gemini/)",
    )
    p.add_argument(
        "--base-workdir", type=Path, required=True,
        help="Where character-less scene stills (s0, s1) live for copy",
    )
    p.add_argument(
        "--output-workdir", type=Path, required=True,
        help="Where new scene stills will be written (v3 / Gemini-locked)",
    )
    p.add_argument("--sheet", type=Path, default=None)
    p.add_argument(
        "--regen-all", action="store_true",
        help="Also re-generate scenes 0 and 1 (which have no characters). "
             "Default: copy from --base-workdir.",
    )
    p.add_argument(
        "--product-ref", type=Path, action="append", default=[],
        help="Path to a product reference image. Pass multiple times to "
             "supply multiple angles. When set, these are appended to the "
             "image_input list AFTER character heroes, and a product-anchor "
             "block is prepended to the prompt for scenes flagged with "
             "--product-scenes.",
    )
    p.add_argument(
        "--product-scenes", type=str, default="",
        help="Comma-separated scene indices that depict the product "
             "(e.g. '2,3'). Only these scenes receive product refs + "
             "anchor prompt. If empty AND --product-ref is set, ALL "
             "regenerated scenes receive product refs.",
    )
    args = p.parse_args()

    bucket = os.environ.get("AUTO_AFFI__GCS_BUCKET", "").strip()
    if not bucket:
        print("ERROR: AUTO_AFFI__GCS_BUCKET required"); return 1
    gkey = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not gkey:
        print("ERROR: GOOGLE_API_KEY required"); return 1

    gcs = GcsStorage(bucket_name=bucket)
    client = GeminiImageClient(api_key=SecretStr(gkey), model=GEMINI_NANO_BANANA_PRO)
    print(f"📊 engine: Gemini {GEMINI_NANO_BANANA_PRO}")

    sb = json.loads(args.storyboard_json.read_text(encoding="utf-8"))
    roster = json.loads(args.roster.read_text(encoding="utf-8"))
    scene_chars = _scene_characters_map(roster)
    frames = sb["frames"]

    args.output_workdir.mkdir(parents=True, exist_ok=True)

    # Parse --product-scenes once
    product_scenes: set[int] = set()
    if args.product_scenes.strip():
        product_scenes = {int(x.strip()) for x in args.product_scenes.split(",") if x.strip()}
    elif args.product_ref:
        # If product refs given without explicit scenes → apply to every regen scene
        product_scenes = set(range(len(frames)))

    # Verify all product refs exist before burning any credits
    for prp in args.product_ref:
        if not prp.exists():
            print(f"ERROR: product ref not found: {prp}"); return 1
    if args.product_ref:
        print(f"📷 product refs: {len(args.product_ref)} ({[str(p.name) for p in args.product_ref]})")
        print(f"📷 product scenes: {sorted(product_scenes) if product_scenes else 'none'}")

    # Scenes without characters — copy from base unless --regen-all
    for scene_idx, frame in enumerate(frames):
        chars = scene_chars.get(scene_idx, [])
        if not chars and not args.regen_all:
            src = args.base_workdir / f"s{scene_idx}-image.jpg"
            dst = args.output_workdir / f"s{scene_idx}-image.jpg"
            if src.exists():
                dst.write_bytes(src.read_bytes())
                print(f"  scene {scene_idx}: copied from base (no characters)")
            else:
                print(f"  scene {scene_idx}: no characters AND no base copy — skipping")
            continue

        use_product = scene_idx in product_scenes
        result = await _regenerate_scene(
            client=client, gcs=gcs, item_id=args.item_id,
            scene_idx=scene_idx,
            prompt=frame["ai_image_prompt"],
            char_ids=chars,
            character_workdir=args.character_workdir,
            output_workdir=args.output_workdir,
            product_refs=args.product_ref if use_product else None,
            inject_product_anchor=use_product,
        )
        if result is None:
            print(f"  scene {scene_idx}: FAILED")
            continue

    # Optional sheet rebuild
    if args.sheet is not None:
        from subprocess import run
        print()
        run([
            ".venv/bin/python", "scripts/build-storyboard-sheet.py",
            "--item-id", str(args.item_id),
            "--workdir", str(args.output_workdir),
            "--output", str(args.sheet),
        ], check=False)

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
