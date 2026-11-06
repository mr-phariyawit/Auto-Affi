#!/usr/bin/env bash
# Render wooden-mannequin pose drafts with headless Chrome (no playwright needed).
# Usage: tools/mannequin-pose/render.sh [OUT_DIR] [POSE_IDS...]   (default: all poses in poses.js)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$HERE/out}"; shift || true
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$OUT"
IDS=("$@"); if [ ${#IDS[@]} -eq 0 ]; then IDS=($(grep -oE '^  [A-Z][A-Za-z0-9_]*:' "$HERE/poses.js" | tr -d ' :')); fi
for id in "${IDS[@]}"; do
  "$CHROME" --headless=new --disable-gpu --use-angle=swiftshader --enable-unsafe-swiftshader \
    --allow-file-access-from-files --hide-scrollbars --window-size=900,1200 \
    --virtual-time-budget=6000 --screenshot="$OUT/$id-pose.png" \
    "file://$HERE/mannequin.html?pose=$id" >/dev/null 2>&1
  echo "rendered $OUT/$id-pose.png"
done
