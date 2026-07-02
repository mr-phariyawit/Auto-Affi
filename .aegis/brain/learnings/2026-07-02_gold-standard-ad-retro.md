# Retro — Auto-Affi ad pipeline breakthrough (session ending 2026-07-02)

## Outcome
Shipped an APPROVED ("ดีมาก") all-video Thai Shopee glam ad (umbrella-335 `master_glam.mp4`, 1080×1920 19s):
female model presenter, every scene a Veo clip, product+cast locked, STT-verified Thai VO, HyperFrames compose.
Codified the whole method as THE standard: `docs/reference/gold-standard-ad-recipe.md`.

## What went well
- **Locked char-sheets = the unlock.** A clean studio product sheet + a Klaus-Karl-style cast sheet, used as
  Veo `referenceImages`, gave dynamic motion AND faithful product — the thing that failed all session.
- **Objective verification beat "I can't hear/see it".** Gemini STT round-trip caught garbled Thai VO
  (คว่ำ→คร่อม, หยด→ยศ) with no ears needed. Frame-sampling caught choppy/anti-message video.
- **Workflows for the hard rethinks** (Veo-native redesign, tooling pivot, framework catalog) produced the
  decisive calls instead of thrashing.
- Cheap, reliable end state (~$9/ad) after the expensive discovery.

## What went wrong (and the fix now codified)
- **Mis-imagined the product** (separate sleeve vs integrated hard-case) → wasted the first run. FIX: study real
  photos first; char-sheet locks it.
- **i2v-only + FLF2V-prompt-on-i2v + raw-photo refs** → static/garbled/drifting clips, ~$12 wasted. FIX:
  referenceImages + locked sheet; guards `PROMPT_MODE_MISMATCH` / `VEO_PROVE_NEGATIVE`.
- **ElevenLabs Thai mispronunciation, whack-a-mole** → FIX: STT-verify + failure-word synonyms + stability{0,.5,1}.
- **VO not updated when scenes changed; video ended before VO; files "หาไม่เจอ"** → FIX: rewrite VO per scene,
  extend comp ≥ VO, deliver to Desktop + reveal in Finder.
- **MBP #7 blocks** (asked instead of acting) fired several times → keep executing, gate only paid/external.

## Keep doing
Follow `gold-standard-ad-recipe.md` exactly. Sheets → refs → animate → STT-verified VO → HyperFrames → verify → deliver.
