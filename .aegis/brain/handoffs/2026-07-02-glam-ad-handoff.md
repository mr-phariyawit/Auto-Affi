# HANDOFF — 2026-07-02 — Auto-Affi ad pipeline (GOLD STANDARD locked)

## STATE: ✅ working end-to-end. Approved glam ad shipped.
- Reference build: `runs/2026-06-30-umbrella-335/` → `master_glam.mp4` (1080×1920, 19s, cleanroom PASS, "ดีมาก").
  All-video: model rain HOOK → 3 presenter clips (cased/invert/hang) → model rain CTA + ฿335. STT-verified Thai VO.
- **THE recipe is codified: `docs/reference/gold-standard-ad-recipe.md`** — follow it verbatim for any new ad.
- Assets in the run: `02-cast/` (cast sheets: JIAP male presenter + female model + presenter/present stills),
  `03-charsheet/` (product lock), `05-shots/` (Veo clips), `06-edit/{slideshow,glam,hybrid}/` (HyperFrames projects).
- Deliverables copied to `~/Desktop/ผลงานร่ม-JIAP/` and the My Drive project folder.

## Proven capabilities (all verified live this session)
- Nano Banana char-sheets (product + Klaus-Karl cast) · Veo i2v (4s/$1.60) + referenceImages hero (8s/$3.20,
  needs locked sheet) · kie ElevenLabs v3 Thai VO (stability{0,.5,1}) + Gemini STT verify · kie Suno BGM ·
  HyperFrames local compose (Thai captions, Ken-Burns, footage bookends, ≥VO duration).
- Gate guards in code: `PROMPT_MODE_MISMATCH`, `VEO_PROVE_NEGATIVE` (336 tests green).

## NEXT (when a new product arrives)
1. Study real product photos → product char-sheet (3 clean views).
2. Pick cast persona → cast sheet (or reuse JIAP presenter / female model).
3. presenter+product stills per script beat → Veo (i2v presenter / referenceImages hero).
4. VO script matching the scenes → kie ElevenLabs → STT-verify each line → reword failures.
5. kie Suno BGM → HyperFrames compose (comp ≥ VO) → cleanroom + frame-check → Desktop/Drive.

## OPEN (external / human-only)
- Publish: Shopee affiliate link + Meta/TikTok token (not automatable). In human-queue.
- Gemini spend cap: watch ai.studio/spend (was hit 2026-06-30, cleared).

## Cost this session ~$30 Gemini/Veo + kie credits (mostly one-time discovery; a clean run now ~$9/ad).
