# Concept 2 Seedance Pipeline — Run 0011 Feedback

> Reviewed: 2026-05-14
> Verdict: ACCEPT (0 issues across 6 clips)

## What worked

1. **Two-keyframe Seedance between-scenes (`input_urls=[s_N, s_N+1]`)** — produces clean motion that converges to the end keyframe (avg `last→s[N+1]` = 0.04 vs threshold 0.10). Replaces single-image i2v's 784× weaker motion.
2. **No-trim rule** — keeping the full Seedance duration (4s / 8s enum) preserves end-frame convergence. Trimming from the end killed convergence on prior runs.
3. **Gemini Nano Banana Pro 2 with hero-portrait `image_input`** — identity lock across scenes 2/3/5 (father) and 4/6 (daughter). All 6 clips' start-keyframe match was ≤0.05.
4. **Apad on TTS audio** — when TTS is shorter than the clip, `apad` pads with silence so video duration wins (`-shortest` then caps to video). Preserves Seedance's end-keyframe convergence even on dialogue-shorter-than-clip cases.
5. **Uniform AAC params** (192k / 44100 / stereo) on every per-clip mux — required for downstream `-f concat -c copy` to stay clean. Without this, AAC profile mismatches cause `decode_pce: Input buffer exhausted` errors at clip boundaries.

## What broke + how to detect

- **Mismatched AAC params across clips → broken concat audio**. Detect: `ffmpeg -i final.mp4 -f null -` floods with AAC errors. Fix: pin every per-clip mux to `-c:a aac -b:a 192k -ar 44100 -ac 2`.
- **Truncated dialogue clips** (clips 2 & 3 cut from 8s → 3.5s). Detect: review unit flags duration drift. Fix: replace `-c:a aac -shortest` with `-filter_complex "[1:a]apad[a]" -shortest` — audio gets padded, video stays full length.
- **Music download crash on `gs://` URL**. Detect: pipeline raises `httpx.UnsupportedProtocol`. Fix: `_download` helper must sign-and-download when URL is `gs://<bucket>/...`.

## Doctrine to apply going forward

| Concern | Rule |
|---|---|
| Image generation | Gemini Nano Banana Pro 2 (`nano-banana-pro-preview`) ONLY. Phaya as fallback. |
| Character consistency | Generate a 360 set per character first (hero + 4 views), use hero as `image_input` for every scene gen they appear in. |
| Video generation | Phaya Seedance 1.5 Pro between-scenes (`input_urls=[start, end]`). Never single-image i2v for cinematic intent. |
| Trim | NEVER trim from end of Seedance output (kills convergence). Either no trim, or trim from start. |
| Audio uniformity | Every per-clip mux uses identical AAC params (192k/44100/stereo). |
| Dialogue+video sync | Always `apad` audio to video duration; `-shortest` then caps. |
| TTS | Phaya Algenib (Thai), `slow=true` for bedtime/intimate cadence. |
| Music | Phaya text-to-music classical guitar, -15dB under primary audio. |
| Compliance | Anatomy guard phrase appended to every Nano Banana prompt. Single-action prompts (no composition stacking). |
| Approval gates | research → 5 concepts → storyboard → script-refine → character 360 → scene stills → final video → review |

## Numbers worth remembering

- **8s Seedance clip @ 720p**: ฿12 per clip (no audio) · ฿24 per clip (with `generate_audio=true`)
- **Per-image Gemini Nano Banana Pro 2 w/ refs**: ~$0.04 = ฿1.40
- **Concept 2 end-to-end run cost (6 Seedance + 7 stills + 10 char-views + TTS + music)**: ~฿80
