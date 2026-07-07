# HANDOFF — 2026-06-30 — Auto-Affi umbrella production (fresh restart)

## 🔴 ONE BLOCKER (external — resume hinges on this)
**Gemini project exceeded its MONTHLY SPEND CAP** → `RESOURCE_EXHAUSTED 429` on every image+Veo call.
Human must raise/reset it at **https://ai.studio/spend** before any Gemini generation resumes.
VO (ElevenLabs/kie.ai), BGM (kie Suno), and HyperFrames render are on OTHER providers/local → NOT blocked.

## WHERE WE ARE
- User said "ทุบ video เก่าทิ้ง เริ่มใหม่ทั้งหมด" after the old umbrella result was judged bad
  (choppy, unclear Thai VO, confusing story, not Veo3-native).
- **Root cause found (big):** I had the PRODUCT MECHANISM WRONG the whole time. Real product (from photos):
  crook-handle umbrella, black-out / YELLOW-in, with an **integrated black ribbed HARD-CASE tube** that seals
  the closed wet canopy (reverse/retract). Benefits: **ล็อกน้ำฝนไว้ใน · แขวนได้ทุกที่**. The old work animated a
  non-existent "insert into separate sleeve + zip" → looked fake. NOW anchored to the real product.

## DONE THIS SESSION
- Old run ARCHIVED (recoverable): `runs/_archive/2026-06-28-uv-auto-umbrella-335-v1-archived` (178M).
- Fresh run: `runs/2026-06-30-umbrella-335/` with raw product photos + `BRIEF.md` (corrected) + `STORYBOARD.md` (new, Veo3-native).
- **v2 production stack verified + codified** (see memory `project-auto-affi-v2-stack`):
  Veo 3.1-fast i2v (payload: bytesBase64Encoded/int-dur/no-generateAudio/follow_redirects; CANNOT do
  FLF2V/absence/precise-action) · post=HyperFrames CLI v0.7.18 (doctor PASS, local, free; Noto Sans Thai
  @font-face; Thai word-sync NOT viable) · VO=ElevenLabs v3 via kie.ai ([excited/friendly]+stability;
  recordInfo poll; UA download) · BGM=kie Suno (/api/v1/generate, needs callBackUrl placeholder).
- **Gate guards shipped (336 tests):** `PROMPT_MODE_MISMATCH` (FLF2V words on i2v) + `VEO_PROVE_NEGATIVE`
  (no-drip language) + `pre-generation-checklist.md`. produce-affiliate-video skill wired to v2.
- Refs: docs/reference/{short-form-format-v2, storytelling-frameworks, hyperframes-*, kie-elevenlabs-vo, pre-generation-checklist}.md

## NEXT (when spend cap is cleared) — new run, NEW storyboard
1. Gen 4 STATE keyframes from real product refs (~$0.24): kf1_wet · kf2_cased · kf3_hang · kf4_cta (see STORYBOARD.md).
2. SHOW keyframes → get approval (storyboard gate).
3. Fire 4 Veo i2v clips ($6.4) — single-action Veo-safe prompts, NO prove-the-negative, product-anchored, ONE setting.
4. Insert the no-drip PROOF as a STILL (not Veo). VO via kie ElevenLabs (stability 0.5, [friendly]). BGM via kie Suno.
5. Compose in HyperFrames (skeleton: docs/templates/hyperframes-short-skeleton.html) → render 1080×1920 → compliance.

## COST SO FAR (honest)
Old umbrella run ~$25.6 Gemini (~$14.4 wasted, mostly the FLF2V-prompt-on-i2v $9.6 bug) + ~7 kie credits.
Hit the Gemini monthly cap. With the v2 stack + guards a clean run should be ~$8-10.

## HUMAN-QUEUE (open)
1. Gemini spend cap (ai.studio/spend) — blocks all generation.
2. Publish (Shopee link + Meta/TikTok token) — external.
3. Confirm umbrella close-mechanism if my photo-read is wrong (FYI; storyboard uses STATES so it's robust).
