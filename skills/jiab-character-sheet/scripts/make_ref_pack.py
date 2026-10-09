#!/usr/bin/env python3
"""Export approved JIAB images as a model-ready ref pack and write sheet.json.

Usage:
  make_ref_pack.py --version v11 [--out cast-library/jiab/v11] [--state DEFAULT]
                   [--approved-by "operator 2026-10-07"] [--motion-test PASS|FAIL|NOT_RUN]
                   [--affects shot1,shot2] "VIEW=path" "VIEW=path" ...

VIEW is one of: front, 34L, 34R, profileL, profileR, fullbody, hairtop.
Each image is copied (never edited) to CHAR_JIAB_<version>[_<state>]_<VIEW>.<ext>.
The pack is what goes to a video/image model; the review board is not.
"""
import argparse
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image

VIEWS = {"front", "34L", "34R", "profileL", "profileR", "fullbody", "hairtop"}
MIN_SHORT_SIDE = 300  # Higgsfield rejects smaller references
LOCK_MIN_SHORT_SIDE = 1024  # a locked pack must survive 1080p video refs without upscaling
MAX_PACK = 5          # every 2026 tool takes 1-5 character refs


def lock_status(refs, motion_test, approved_by):
    """Decide whether this pack may be called LOCKED.

    refs:        list of dicts with keys view, original (bool), short_side (int)
    motion_test: "PASS" | "FAIL" | "NOT_RUN"
    approved_by: operator approval text, or "" if none yet

    Return "LOCKED" or "PENDING: <reason>". Only a LOCKED pack may be
    fed to video generation.
    """
    # Rule decided 2026-10-09 (operator delegated: "ไป research แล้วมาตอบแทนผม"), from
    # docs/reference/character-sheet-professional-ai-film.md stage B (3-5 hero refs:
    # front, 3/4, side, full body) and stage E / §7 (5 s motion test before "locked").
    views = {r["view"] for r in refs}
    reasons = []
    if not approved_by.strip():
        reasons.append("no operator approval")
    if not 3 <= len(refs) <= 5:
        reasons.append(f"{len(refs)} refs (need 3-5)")
    if "front" not in views or not views & {"34L", "34R"} or not views & {"profileL", "profileR"}:
        reasons.append("needs front + a three-quarter + a profile")
    if any(not r["original"] for r in refs):
        reasons.append("screencrop in pack (download originals)")
    if any(r["short_side"] < LOCK_MIN_SHORT_SIDE for r in refs):
        reasons.append(f"ref under {LOCK_MIN_SHORT_SIDE}px short side")
    if motion_test != "PASS":
        reasons.append(f"motion test {motion_test}")
    return "LOCKED" if not reasons else "PENDING: " + "; ".join(reasons)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", required=True)
    ap.add_argument("--out")
    ap.add_argument("--state", default="")
    ap.add_argument("--approved-by", default="")
    ap.add_argument("--motion-test", default="NOT_RUN", choices=["PASS", "FAIL", "NOT_RUN"])
    ap.add_argument("--affects", default="")
    ap.add_argument("panels", nargs="+")
    a = ap.parse_args()

    if len(a.panels) > MAX_PACK:
        ap.error(f"{len(a.panels)} refs; a ref pack holds at most {MAX_PACK}")
    out = Path(a.out or f"cast-library/jiab/{a.version}")
    out.mkdir(parents=True, exist_ok=True)
    tag = f"CHAR_JIAB_{a.version}" + (f"_{a.state.upper()}" if a.state else "")

    refs = []
    for p in a.panels:
        view, _, src = p.partition("=")
        if view not in VIEWS or not src:
            ap.error(f"bad panel {p!r}; use VIEW=path with VIEW in {sorted(VIEWS)}")
        src = Path(src)
        w, h = Image.open(src).size
        if min(w, h) < MIN_SHORT_SIDE:
            ap.error(f"{src} short side {min(w, h)} px < {MIN_SHORT_SIDE}; upscale before packing")
        original = "SCREENCROP" not in src.name.upper()
        dst = out / f"{tag}_{view}{src.suffix.lower()}"
        shutil.copy2(src, dst)
        refs.append({"view": view, "file": str(dst), "source": str(src), "size": f"{w}x{h}",
                     "short_side": min(w, h), "original": original, "sha256": sha256(dst)})
        if not original:
            print(f"WARN {view}: screencrop, not the downloaded original")

    sheet = {
        "asset": tag,
        "element_tag": "@jiab",
        "version": a.version,
        "state": a.state or "DEFAULT",
        "created_local": datetime.now().isoformat(timespec="seconds"),
        "refs": refs,
        "approved_by": a.approved_by,
        "motion_test": a.motion_test,
        "affects_shots": [s for s in a.affects.split(",") if s],
        "status": lock_status(refs, a.motion_test, a.approved_by),
    }
    path = out / f"{tag}.sheet.json"
    path.write_text(json.dumps(sheet, ensure_ascii=False, indent=2))
    print(f"{path} refs={len(refs)} status={sheet['status']}")


if __name__ == "__main__":
    main()
