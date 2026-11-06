#!/usr/bin/env bash
# Render one scene JSON (poser export) to PNG with headless Chrome.
# Usage: tools/mannequin-pose/render-json.sh <scene.json> [out.png]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
IN="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
OUT="${2:-${IN%.json}.png}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --use-angle=swiftshader --enable-unsafe-swiftshader \
  --allow-file-access-from-files --hide-scrollbars --window-size=900,1200 \
  --virtual-time-budget=6000 --screenshot="$OUT" \
  "file://$HERE/mannequin.html?json=file://$IN" >/dev/null 2>&1
echo "$OUT"
