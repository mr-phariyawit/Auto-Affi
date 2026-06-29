---
title: Auto-Affi Short-Form Format v2 (the default for Thai Shopee shorts)
created: 2026-06-29
origin: /grill-me design session 2026-06-29 (human-directed, Veo-strength + TikTok-native)
supersedes: the 24s/6-clip PAS-narrative + ffmpeg-PNG approach used on run umbrella-335 v1
---

# Auto-Affi Short-Form Format v2

> Designed to what Veo3 is actually good at + TikTok ears+eyes theory. Complex narrative is OUT —
> Veo3 shows *moments/states*, it cannot *tell a story* or *prove a precise action*.

## 1. Duration & structure  `[grill Q1]`
- **15s default**, 3 beats: **HOOK (≤2s) → DEMO → CTA**.
- PAS 24–30s narrative reserved ONLY for products with a genuinely complex pain to agitate.
- 15s clips: ~3–4 Veo shots of ≤4s, each must earn its place.

## 2. What Veo3 is good at (the hard constraint)  `[verified run umbrella-335]`
- ✅ i2v from a strong first frame (character/product consistency); continuous/ambient motion; premium look from the keyframe; ≤4s in budget.
- ❌ precise END-action (no FLF2V on Gemini API), depicting ABSENCE (no-drip → renders water), multi-action in 4s, text.
- **Rule:** ask Veo to SHOW a state/vibe, never to PROVE. Proof = a still cut-in + a caption, not Veo motion.
- Gate enforced: `AuditCode.PROMPT_MODE_MISMATCH` blocks FLF2V language on an i2v prompt.

## 3. Hook (TikTok ears+eyes, <2s)  `[grill Q2]`
Three redundant layers, SAME core message, lands muted OR sound-on:
1. **FRAME (eyes):** Veo first-frame = the scroll-stopper — a single arresting STATE (relatable pain / curiosity gap), + one simple Veo motion (push-in / drip / reaction). NOT a product beauty shot.
2. **TEXT (eyes, muted):** bold Thai caption, top/center.
3. **VO (ears):** one punchy excited line.

## 4. Demo beat  `[grill Q3]`
Veo action shot (its strength: insert/seal/hang) **+ a 0.5–1s still cut-in for proof (dry paper/floor — 100% controllable) + caption**. Never ask Veo to animate the "no-drip" proof.

## 5. Post-production = HyperFrames ONLY (local, free, deterministic)  `[grill Q4; CLI verified v0.7.18]`
- **Captions:** `caption-highlight` (tagged *tiktok*) word-synced via `hyperframes transcribe` (VO → word timestamps) = karaoke ears+eyes. (alts: pill-karaoke, kinetic-slam, emoji-pop.)
- **Price:** `lt-dark-card` lower-third — "JIAP DEALS · ฿335".
- **CTA endcard:** custom div + `transitions-scale`/`-push` entrance (no CTA block exists) — "กดตะกร้าส้มใต้คลิป".
- **Disclosure:** persistent `#โฆษณา` div.
- **Rhythm:** `hyperframes beats` → snap cuts/captions to the BGM beat.
- **Transitions:** shader (whip-pan / flash-through-white / cinematic-zoom), 1–2 *meaning* moments only.
- **Thai text:** embed `Noto Sans Thai` via `@font-face`; `snapshot`-verify tone marks; render `--docker` for determinism.
- Compose model: GSAP `timeline({paused})` registered to `window.__timelines[id]`; `clip` class + `data-start/-duration/-track-index`; overlapping overlays on different tracks; never animate `<video>` dims; muted playsinline + separate `<audio>` track.
- Replaces the ad-hoc ffmpeg-PNG overlay (ffmpeg here has no drawtext).

## 6. VO = ElevenLabs v3 via kie.ai ONLY  `[grill Q5; verified live]`
- `model: elevenlabs/text-to-dialogue-v3`, `language_code: th`, **style ตื่นเต้น/เสียงดัง = `[excited]` tag + `stability: 0`**.
- Endpoints: createTask → `recordInfo?taskId=` poll → UA-download. See `kie-elevenlabs-vo.md`.
- Voice: pick from 68 presets, **human-approved by ear**.
- **Audio mix:** HyperFrames `producer` — VO 100% / BGM ~30% ducked / SFX accents; single muxed track.

## 7. Narrative framework  `[storytelling-frameworks.md — 15 to choose from]`
Default spine **PAS** (+ 4Ps proof beat + UGC-voiced hook). Pick per product at the CampaignBrief / Creative Treatment step.

## Open items
- VO voice + excitement level: pending human ear-check on the test line.
- Kokoro/MusicGen optional local fallbacks NOT installed (we use kie.ai VO + supplied/Generated BGM).
- Premium considerations: BGM source (royalty-free vs MusicGen), SFX library — to wire at build.
