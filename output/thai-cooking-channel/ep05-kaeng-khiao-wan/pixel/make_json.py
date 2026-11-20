#!/usr/bin/env python3
"""
Crop/resize EP05 final.png assets into real.json (720x392 JPEG) and
inset_real.json (264x264 JPEG) for use with the pixel template.

Crossfade pairs (mortar, pot) use the same contain_blur fit so they align.

Run from any directory: python3 make_json.py
"""
import os, json, base64, io
from PIL import Image

HERE   = os.path.dirname(os.path.abspath(__file__))
LIB    = os.path.join(HERE, '..', '..', 'assets', 'library')
RW, RH = 720, 392   # real.json target size
IW, IH = 264, 264   # inset_real.json target size
JQUAL  = 90

def load(rel):
    return Image.open(os.path.join(LIB, rel, 'final.png')).convert('RGB')

def crop_landscape(img, w=RW, h=RH, top_offset=None):
    """Resize so width fits w, then crop height to h.
    top_offset: row in the RESIZED image to start the crop (default: centre).
    """
    sw, sh = img.size
    scale  = w / sw
    new_h  = round(sh * scale)
    img    = img.resize((w, new_h), Image.LANCZOS)
    if top_offset is None:
        top = (new_h - h) // 2       # centre crop
    else:
        top = max(0, min(top_offset, new_h - h))
    return img.crop((0, top, w, top + h))

def contain_blur(img, w=RW, h=RH):
    """Whole image fitted to the box height, centred, over a darkened blurred cover-fill of itself."""
    from PIL import ImageFilter, ImageEnhance
    sw, sh = img.size
    bg = img.resize((w, round(sh * w / sw)), Image.LANCZOS)
    t = (bg.size[1] - h) // 2
    bg = bg.crop((0, t, w, t + h)).filter(ImageFilter.GaussianBlur(18))
    bg = ImageEnhance.Brightness(bg).enhance(0.55)
    fg = img.resize((round(sw * h / sh), h), Image.LANCZOS)
    bg.paste(fg, ((w - fg.size[0]) // 2, 0))
    return bg

def crop_square(img, side=IW):
    """Centre-crop to square, then resize."""
    sw, sh = img.size
    s = min(sw, sh)
    x0, y0 = (sw - s) // 2, (sh - s) // 2
    img = img.crop((x0, y0, x0 + s, y0 + s))
    return img.resize((side, side), Image.LANCZOS)

def to_b64(img, quality=JQUAL):
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=quality, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

# ── real.json ──────────────────────────────────────────────────────────────
# key → (pillar/folder, top_offset_on_resized_image)
# top_offset=None → centre crop (default)
# pt-history: radio is at resized rows ~31-350; offset=50 shows grille+knobs+bowl top
real_map = {
    'kw-dish':      ('06-dishes/kw-dish-green-curry-chicken',          None),
    'kw-chillies':  ('03-thai-spices/kw-spice-fresh-green-chillies',   None),
    'kw-seeds':     ('03-thai-spices/kw-spice-toasting-seeds',         None),
    'kw-herbs':     ('02-thai-vegetables/kw-veg-paste-herbs',          None),
    'kw-mortar-chillies': ('05-cooking-scenes/kw-cook-mortar-chillies', None),
    'kw-mortar-paste':    ('05-cooking-scenes/kw-cook-mortar-paste',    None),
    'kw-store':     ('01-seasonings/kw-sea-storebought-paste',         None),
    'kw-pot-oil':   ('05-cooking-scenes/kw-cook-pot-paste-oil',        None),
    'kw-pot-chicken': ('05-cooking-scenes/kw-cook-pot-chicken-eggplant', None),
    'kw-pot-basil': ('05-cooking-scenes/kw-cook-pot-basil-finish',     None),
    'kw-eggplant':  ('02-thai-vegetables/kw-veg-thai-eggplant-bamboo', None),
}

real_out = {}
for key, (rel, top_off) in real_map.items():
    img = load(rel)
    cropped = contain_blur(img)   # v2 (owner 2026-11-18): show the whole photo, not a tight crop
    real_out[key] = to_b64(cropped)
    print(f'real  {key:20s} {cropped.size}  top_offset={top_off}')

out_path = os.path.join(HERE, 'real.json')
with open(out_path, 'w') as f:
    json.dump(real_out, f)
print(f'wrote {out_path}  ({os.path.getsize(out_path)//1024} kB)')

# ── inset_real.json ────────────────────────────────────────────────────────
inset_map = {
    'target':    '06-dishes/kw-dish-green-curry-chicken',
    'chillies':  '03-thai-spices/kw-spice-fresh-green-chillies',
    'chillies2': '03-thai-spices/kw-spice-fresh-green-chillies',
    'spices':    '03-thai-spices/kw-spice-toasting-seeds',
    'herbs':     '02-thai-vegetables/kw-veg-paste-herbs',
    'pound':     '05-cooking-scenes/kw-cook-mortar-chillies',
    'gapi':      '05-cooking-scenes/kw-cook-mortar-paste',
    'store':     '01-seasonings/kw-sea-storebought-paste',
    'fry':       '05-cooking-scenes/kw-cook-pot-paste-oil',
    'chicken':   '05-cooking-scenes/kw-cook-pot-chicken-eggplant',
    'eggplant':  '02-thai-vegetables/kw-veg-thai-eggplant-bamboo',
    'basil':     '05-cooking-scenes/kw-cook-pot-basil-finish',
}

inset_out = {}
for key, rel in inset_map.items():
    img = load(rel)
    cropped = crop_square(img)
    inset_out[key] = to_b64(cropped)
    print(f'inset {key:20s} {cropped.size}')

out_path = os.path.join(HERE, 'inset_real.json')
with open(out_path, 'w') as f:
    json.dump(inset_out, f)
print(f'wrote {out_path}  ({os.path.getsize(out_path)//1024} kB)')
