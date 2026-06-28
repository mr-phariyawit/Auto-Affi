---
name: gemini-generation-playbook
description: "How Auto-Affi actually generates with Gemini (Nano Banana Pro images + Veo 3 video) — verified REST payloads, the MCP sandbox gotcha, cost reality, reference-image consistency, and the SHOW-the-draft-before-approve rule. Trigger whenever generating/regenerating a still or clip, debugging a Gemini/Veo call, choosing image vs video params, or wiring the GeminiProvider. Also: 'เจนรูป', 'เจนวิดีโอ Veo', 'prompt ที่ส่ง gemini', 'nano banana payload'."
profile: standard
triggers:
  en: ["generate image gemini", "nano banana pro", "veo 3 video", "gemini api payload", "regenerate draft", "reference image consistency"]
  th: ["เจนรูป gemini", "นาโนบานาน่า", "เจนวิดีโอ veo", "payload gemini", "รีเจนภาพ"]
reads: ["src/auto_affi/adapters/gemini_provider.py", "docs/templates/pipeline-step-templates.md"]
writes: ["runs/<run>/"]
wires: ["gemini_provider", "gen_provider", "produce"]
tests: []
supersedes: []
---

## Quick Reference

> **"Show the pixels, not the prompt. Verified payload beats documented payload."**

Auto-Affi generates via **three channels** (ADR-009 Gemini-only). Use them in this order.

## Hard rules (learned from real runs)

1. **SHOW the generated draft before asking for approval.** A human cannot approve a stage from a
   prompt string — generate the cheap draft (~$0.06), display it, THEN gate. Don't loop on prose.
2. **Reference-image consistency replaces soul-id.** Pass the approved `cast_sheet.png` + `objects_sheet.png`
   (and the real product photos) as `reference_images` on EVERY downstream call — that is the character/
   product lock.
3. **Veo clips ≤ 4s.** Veo 3 fast ≈ $0.40/s → an 8s clip ($3.20) exceeds the $1.80 video_gen cap and the
   budget breaker DENIES it (correct). Keep clips ≤ 4s (~$1.60).
4. **Thai no-lipsync = `generateAudio: false`.** Veo native audio is never requested; Thai VO is muxed
   over B-roll separately; no shot shows a visibly-speaking Thai mouth.
5. **Tag verification honestly.** The image payload is `[VERIFIED]` (objects_sheet generated). The Veo
   payload is `[PRODUCED: not yet verified live]` until the first real clip returns.

## Channel 1 — Nano Banana Pro via MCP (`mcp__Nano_Banana_Pro__generate_image`)
```json
{ "prompt": "...", "reference_images": ["/abs/ref1.jpg", "... up to 14"],
  "aspect_ratio": "9:16", "size": "1K|2K|4K", "model": "gemini-3-pro-image", "out_path": "/abs/out.png" }
```
**GOTCHA (verified):** the MCP server is sandboxed — it CANNOT read `reference_images` outside its own
output dir (EPERM), and Google-Drive CloudStorage on-demand files fail too. Text-only generation works;
reference-conditioned generation does NOT. → For any run needing the real product refs, use Channel 2.

## Channel 2 — Image via REST (default for Auto-Affi) `[VERIFIED]`
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key=$GEMINI_API_KEY
```
```json
{ "contents": [{ "parts": [
    { "text": "<prompt>" },
    { "inline_data": { "mime_type": "image/jpeg", "data": "<base64 of ref>" } }
] }],
  "generationConfig": { "responseModalities": ["IMAGE"], "imageConfig": { "aspectRatio": "9:16" } } }
```
**Response:** `candidates[0].content.parts[*].inline_data.data` (base64 PNG) → write bytes.
We read local refs ourselves (full FS access), base64-inline them — bypasses the MCP sandbox entirely.
Mirrors `gemini_provider.py::_image_api`.

## Channel 3 — Video via REST (Veo, long-running) `[PRODUCED: not yet verified live]`
```
POST .../models/<MODEL>:predictLongRunning?key=$GEMINI_API_KEY
```
**Text / first-frame only (Veo 3.0 fast):**
```json
{ "instances": [{ "prompt": "<shot 9:16>",
    "image": { "inlineData": { "mimeType":"image/png", "data":"<first frame b64>" } } }],
  "parameters": { "aspectRatio":"9:16", "durationSeconds":"4", "generateAudio":false, "personGeneration":"allow_adult" } }
```
**FLF2V — first→last keyframe interpolation (Veo 3.1 / 3.1-fast ONLY) `[VERIFIED structure 2026-06-28]`:**
```json
{ "instances": [{ "prompt":"Animate the transition between the first and last frame. ...",
    "image":     { "inlineData": { "mimeType":"image/png", "data":"<FIRST b64>" } },
    "lastFrame": { "inlineData": { "mimeType":"image/png", "data":"<LAST b64>" } } }],
  "parameters": { "aspectRatio":"9:16", "durationSeconds":"4", "generateAudio":false, "personGeneration":"allow_adult" } }
```
Then **poll** `GET .../{operation.name}` until `{"done":true}`, **download**
`response.generateVideoResponse.generatedSamples[0].video.uri`. Mirrors `gemini_provider.py::_video_api`.

**Hard-won facts (verified against ai.google.dev/gemini-api/docs/video):**
- `lastFrame` + `referenceImages` exist ONLY on **veo-3.1 / veo-3.1-fast** — `veo-3.0-fast` does text/first-frame only.
  Doing FLF2V requires switching the video model to 3.1-fast.
- `referenceImages` (pass character/product as assets, ≤3) **forces `durationSeconds:"8"`** (≈$3.20) → exceeds the
  $1.80 breaker → DENIED. So carry consistency in the FIRST/LAST keyframes instead (they already lock identity), not referenceImages.
- `personGeneration:"allow_adult"` is required for image-to-video / interpolation (vs `allow_all` for text-to-video).

## Production note (gate integrity)
Cheap **preview** drafts (to enable the human review gate) may be generated via Channel 2 directly and
labelled `[PRODUCED: est cost]`. The **production** run records spend + enforces the PGA gate through
`ops/produce.GatedProducer` + `GeminiProvider`. Real spend is always logged (never reported as $0).

## Cost model (estimates)
| asset | model | est cost |
|---|---|---|
| still | gemini-3-pro-image | ~$0.06 |
| clip (4s) | veo-3.0-fast | ~$1.60 |
| clip (8s) | veo-3.0-fast | ~$3.20 → DENIED ($1.80 cap) |


## Reference-image technical rules (VERIFIED on the umbrella run)
For character + product consistency across frames (gemini-3-pro-image / Nano Banana Pro):
1. **Images FIRST, then text** (reference-then-describe). Putting text first degrades ref usage.
2. **Order: character refs → product refs → style refs.** Max 14 total (5 char, 6 object, 3 style).
3. **Label each ref in the prompt:** "REFERENCE 1 is the CHARACTER (same face/hair/wardrobe)...
   REFERENCE 2-3 are the PRODUCT (same item)". Say "the SAME person" / "the SAME product".
4. Give the character ref MULTIPLE angles (a 4-view turnaround sheet) — locks the face hard.
5. parts order in REST: `[charImg, prodImg1, prodImg2, {text}]`. Verified: held face + outfit +
   product (even the ID-card photo) across all 6 BTS shots.

## Integration
- **From** `produce-affiliate-video` Step 4 (the gated stages call this).
- **Uses** `gemini_provider` / `gen_provider` (the verified payloads live there).
- Keys in `.env` (`GEMINI_API_KEY`); never echo the value; rotate if pasted in chat.
