#!/bin/bash
# Render frames -> silent mp4 -> mux mix.wav -> checks. Run from the ep05-kaeng-khiao-wan folder with the pixel server on :${PORT:-8931}.
# SKIP_CAPTURE=1 reuses existing pixel/frames.
set -e
V=${1:-v1}
if [ -z "$SKIP_CAPTURE" ]; then
  rm -rf pixel/frames && mkdir -p pixel/frames
  (cd pixel && node capture.cjs frames > capture.log 2>&1)
fi
ffmpeg -y -v error -framerate 30 -i pixel/frames/f%05d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -movflags +faststart pixel/ep05-silent.mp4
ffmpeg -y -v error -i pixel/ep05-silent.mp4 -i audio/mix.wav -c:v copy -c:a aac -b:a 192k -movflags +faststart final/ep05-$V.mp4
ffprobe -v error -show_entries stream=codec_type,width,height,nb_frames,duration,r_frame_rate -of compact final/ep05-$V.mp4
ffmpeg -hide_banner -nostats -i final/ep05-$V.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
grep -c PAGEERROR pixel/capture.log || true
