---
title: GOLD-STANDARD Auto-Affi Ad Recipe (locked 2026-07-02)
status: THE standard — follow this for every new product/ad. Proven on the umbrella-335 GLAM ad.
supersedes: the i2v-first / Veo-spine approaches (ADR-009/010 early)
---

# GOLD-STANDARD Ad Recipe

> One product-consistent, cast-consistent, all-video Thai Shopee ad — cheap, reliable, no lottery.
> Reference build: `runs/2026-06-30-umbrella-335/` → `master_glam.mp4` (approved "ดีมาก" 2026-07-02).

## The pipeline (in order — never skip the sheets)

### 1. LOCK the identities first (Nano Banana Pro stills, ~$0.06 each)
- **Product char-sheet** (`03-charsheet/`): 3 clean studio views of the EXACT product (open / cased / hero),
  neutral bg, NO text, one variant. Generated from the real product photos. This is the product lock.
- **Cast char-sheet** (`02-cast/cast_sheet_*.png`): a Klaus-Karl-style design sheet of the presenter —
  4 body views + 5 expressions + fabric/logo/palette tiles, branded (JIAP DEALS). This is the human lock.
  Personas proven: 👨 male UGC presenter · 👩 female glamour model (elegant/editorial, platform-safe — NOT explicit).
- ⚠️ **Study the REAL product photos before writing anything** — we wasted a whole run on a mis-imagined
  mechanism. The umbrella = crook handle + integrated ribbed HARD-CASE tube (locks water in), NOT a separate sleeve.

### 2. Presenter/product shots = cast-sheet + product-sheet as REFERENCES (Nano Banana, ~$0.06 each)
Pass REFERENCE 1 = cast sheet, REFERENCE 2-3 = product sheet, and label them ("the SAME person / SAME product").
One still per script beat: presenter demonstrating each feature (holds case, inverts it, hangs it). Character +
product both stay locked.

### 3. Animate = Veo, the RIGHT way (this was the breakthrough)
- **i2v (first frame)** for subtle presenter/beauty motion — `bytesBase64Encoded` image, `durationSeconds:4` (int),
  NO `generateAudio`, `follow_redirects=True`, model `veo-3.1-fast-generate-preview`. ~$1.60/4s. Good for
  "person presents / walks in rain" (gentle motion). Locks the exact composition.
- **referenceImages (Veo 3.1)** for a dynamic HERO orbit — pass the LOCKED char-sheet (NOT raw photos → they drift),
  `referenceType:"asset"`, forces `durationSeconds:8` (~$3.20). Motion + faithful product.
- ❌ Veo can NOT do FLF2V / precise end-action / prove-a-negative on the Gemini API. Never ask it to show "no drip".

### 4. VO = kie.ai ElevenLabs v3 ONLY (operator directive) — but VERIFY it
- Model `elevenlabs/text-to-dialogue-v3`, `stability` ∈ {0, 0.5, 1.0} ONLY (kie 500s otherwise), `language_code:"th"`.
- **ElevenLabs mispronounces Thai** → after EVERY line, STT round-trip: transcribe the mp3 with Gemini
  (`gemini-2.5-flash`, inline `audio/mpeg`) and compare to intended text. Mismatch → reword + regen.
- Known failure words → synonyms: คว่ำ→พลิกกลับ · หยด→ไม่ไหลออก · trailing ได้→ends as ดี (end the line differently).
- **VO must match the CURRENT scenes** (rewrite the script when the visuals change — don't reuse an old script).

### 5. BGM = kie Suno (`/api/v1/generate`, instrumental, needs a `callBackUrl` placeholder), ducked ~0.17.

### 6. Compose = HyperFrames (local, free, deterministic)
- `data-composition-id/width/height`, every clip `class="clip"` + `data-start/duration/track-index`,
  GSAP `paused` timeline registered to `window.__timelines['<id>']`. Videos `muted playsinline`; captions =
  Noto Sans Thai `@font-face`; Ken-Burns on stills only (never animate a `<video>`).
- **Composition duration MUST cover the last VO** — if video ends before speech, extend the last scene/comp.
- Prefer real footage over held stills for hook AND cta (bookend with motion). Hold a clip's LAST frame (not
  a jump-back still) if a video is shorter than its window.
- Render `--quality standard --fps 30`, native 1080×1920 (no upscale). Verify: cleanroom PASS + sample frames.

## Cost (a clean run at this standard)
char-sheets ~$0.2 + presenter stills ~$0.3 + Veo (1 hero 8s + 3 presenter 4s) ~$8 + kie VO/BGM ~$0.5 = **~$9/ad**.
(vs the $25 lottery of the first umbrella run.)

## Delivery
Copy masters to `~/Desktop/ผลงานร่ม-JIAP/` AND the My Drive project folder + `open` in Finder
(My Drive→cloud sync lags; Desktop is instant).

## Non-negotiables (the anti-waste gates)
1. Real-product study → char-sheets → refs → animate. Never animate before the sheets exist.
2. Veo prompt-mode matches gen-mode (i2v prompt ≠ referenceImages prompt ≠ FLF2V). Guard: `PROMPT_MODE_MISMATCH`.
3. Never ask Veo to prove a negative. Guard: `VEO_PROVE_NEGATIVE`. Proof = still + caption.
4. STT-verify every Thai VO line. Rewrite VO when scenes change.
5. Video ≥ VO length. Cleanroom + frame-check before delivery.
