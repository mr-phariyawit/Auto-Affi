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
**Image-to-video (first frame) — VERIFIED LIVE on `veo-3.1-fast-generate-preview`, 2026-06-28, produced a real 4s/720×1280/h264 clip:**
```json
{ "instances": [{ "prompt": "<shot, 9:16, cinematic motion>",
    "image": { "bytesBase64Encoded": "<first frame b64>", "mimeType": "image/png" } }],
  "parameters": { "aspectRatio":"9:16", "durationSeconds":4 } }
```
Then **poll** `GET .../{operation.name}` until `{"done":true}`, **download**
`response.generateVideoResponse.generatedSamples[0].video.uri` **with `follow_redirects=True`** (the download URI
302-redirects to a files blob). Mirrors `gemini_provider.py::_video_api` + `build_video_body`.

**Hard-won facts — the published docs (ai.google.dev/gemini-api/docs/video) were WRONG on 4 counts; these are verified by live 200s:**
- Image bytes go in **`image.bytesBase64Encoded` + `mimeType`**, NOT `inlineData` (which is a generateContent shape → Veo 400s `inlineData isn't supported`).
- **`durationSeconds` must be a NUMBER (int)**, not a string (string → 400 `needs to be a number`).
- **`generateAudio` is rejected by this model** — omit it (400 `generateAudio isn't supported`). Veo emits native audio; STRIP it and mux the Thai VO in edit.
- The download is a **302 redirect** → the httpx client MUST `follow_redirects=True` or you get a confusing `302 Unknown Error` AFTER the (billable) op already completed.
- **FLF2V (`lastFrame`) + `referenceImages` are NOT available on the Gemini API** for this model — sending `lastFrame` → 400 `use case is currently not supported` (those are Vertex-AI Veo features). On the Gemini API, motion comes from the **first frame + the prompt only**; the storyboard's LAST keyframe is intent-documentation, not an API input.
- `personGeneration` is NOT required (omit); the bare i2v payload above is the minimal working request.

⚠️ **Billing trap:** a 400 at the predict step is free (no op). But once predict returns 200 an op is created and **billed even if the download later fails** — so the `follow_redirects` bug cost one wasted ~$1.60 clip before it was caught. Always fix the download path before firing at scale.

🚨 **PROMPT-MODE MUST MATCH GEN-MODE (cost a wasted $9.60 batch).** An i2v call has ONLY a first frame —
do NOT feed it an FLF2V prompt. Prompts authored for first→last interpolation begin "Animate the
transition between the first and last frame… It opens on…". Sent to i2v (no `lastFrame`), Veo is told to
interpolate toward a frame that does not exist → it improvises **garbage motion in every clip**. The first
frame still conditions the scene (so it *looks* right in a thumbnail) but the MOTION is junk.
- **i2v prompt =** one continuous action + camera move described FROM the start frame, no "between frames",
  no "last frame", no "transition". e.g. "Ton holds the wet umbrella as it drips to the floor; slow
  downward camera tilt." Keep a separate `i2v_prompt` field; never reuse the FLF2V `veo_cinematic_prompt`.
- Always **sample mid+end frames of the FIRST test clip and actually look** before firing the batch —
  a coherent thumbnail of frame-0 does NOT prove the motion is right.

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

## Thai VO QA — ElevenLabs-only (verified method 2026-07-02)
kie ElevenLabs v3 is English-trained → mispronounces some Thai words unpredictably. Since the operator
often can't audition by ear, VERIFY every generated line objectively:
1. **STT round-trip:** send the generated mp3 to Gemini (`gemini-2.5-flash` generateContent, inline_data
   `audio/mpeg`, prompt "Transcribe this Thai speech exactly") → compare transcription to the intended text.
   Mismatch = mispronounced → reword and regen.
2. **Known ElevenLabs-Thai failure words** (reword to a synonym): คว่ำ→พลิกกลับ · หยด→ไม่ไหลออก ·
   trailing ได้ often heard as ดี → end the line on a different word. Prefer common mid-tone words; avoid
   ไม้ตรี / rare clusters.
3. **stability ∈ {0, 0.5, 1.0} ONLY** (kie rejects other values with HTTP 500). Use 1.0 for max clarity.
4. **No truncation:** set the HyperFrames audio clip `data-duration` >= the actual mp3 duration.
