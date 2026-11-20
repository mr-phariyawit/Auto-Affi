#!/bin/bash
# EP05 VO: one take per line, then STT. Run from Auto-Affi root.
D=output/thai-cooking-channel/ep05-kaeng-khiao-wan/audio/vo-en-v1
while IFS=$'\t' read -r id vo sen sth; do
  [ -f "$D/line_$id.wav" ] && continue
  python3 tools/gemini-tts.py --model gemini-2.5-pro-preview-tts --voice Sulafat --text "Say at a brisk, lively pace, like a warm confident cooking-show narrator: $vo" --out "$D/line_$id.wav" > "$D/line_$id.log" 2>&1
  python3 tools/gemini-stt.py "$D/line_$id.wav" > "$D/line_$id.stt.txt" 2>&1
  echo "$id done"
done < "$D/lines.tsv"
