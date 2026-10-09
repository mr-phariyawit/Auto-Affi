#!/usr/bin/env python3
"""Build a labelled board for JIAB QC strips and character-sheet review boards.

Usage:
  compare_board.py OUT.jpg "LABEL=path" "LABEL=path" ... [--crop x0,y0,x1,y1] [--height 900] [--cols N]

--crop takes fractions of each image (0-1), e.g. 0.25,0.28,0.75,0.48 for a
front-portrait eye band, so the same region is compared across runs.
All panels are scaled to the same height; labels sit above each panel.
--cols wraps panels into rows of N (e.g. --cols 3 for a 2x3 review board).
Labels are drawn on the board only, never on the images, so a review board
must not be used as a model reference.
"""
import sys
from PIL import Image, ImageDraw, ImageFont


def parse(argv):
    out, panels, crop, height, cols = None, [], None, 900, 0
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--crop":
            crop = [float(v) for v in argv[i + 1].split(",")]
            i += 2
            continue
        if a == "--height":
            height = int(argv[i + 1])
            i += 2
            continue
        if a == "--cols":
            cols = int(argv[i + 1])
            i += 2
            continue
        if out is None:
            out = a
        else:
            label, _, path = a.rpartition("=")
            if not path:
                sys.exit(f"panel must be LABEL=path, got: {a}")
            panels.append((label, path))
        i += 1
    if not out or not panels:
        sys.exit(__doc__)
    return out, panels, crop, height, cols or len(panels)


def font(size):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc",
              "/Library/Fonts/Arial.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()


def main():
    out, panels, crop, height, cols = parse(sys.argv[1:])
    label_h, gap = 44, 12
    f = font(26)
    tiles = []
    for label, path in panels:
        im = Image.open(path).convert("RGB")
        if crop:
            w, h = im.size
            im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
        w, h = im.size
        im = im.resize((max(1, round(w * height / h)), height), Image.LANCZOS)
        tiles.append((label, im))
    rows = [tiles[i:i + cols] for i in range(0, len(tiles), cols)]
    row_h = height + label_h + gap
    total_w = max(sum(t.size[0] for _, t in r) + gap * (len(r) + 1) for r in rows)
    board = Image.new("RGB", (total_w, row_h * len(rows) + gap), "white")
    d = ImageDraw.Draw(board)
    for ri, row in enumerate(rows):
        x, y = gap, ri * row_h
        for label, im in row:
            d.text((x + 4, y + gap // 2 + 6), label, fill="black", font=f)
            board.paste(im, (x, y + label_h + gap))
            x += im.size[0] + gap
    board.save(out, quality=90)
    print(f"{out} {board.size[0]}x{board.size[1]} panels={len(tiles)}")


if __name__ == "__main__":
    main()
