# Higgsfield + Seedance 2.0 — Stack Routing Decision

**Date:** 2026-05-15
**Trigger:** User asked to study https://higgsfield.ai/ and https://www.byteplus.com/en/activity/seedance2-0
**Decision authority:** Nick Fury after 2-agent parallel research.

## TL;DR

- **Higgsfield**: ADOPT for macro product shots (DoP preset library) + B-roll transitions (17-effect tool). SKIP its Kling Avatar talking-head (HeyGen is better path). DEFER its Speak audio (Thai unverified).
- **Seedance 2.0**: ADOPT for two-keyframe shots, contingent on Phaya gateway support. +31.7 physics-accuracy points, Fast tier @ 720p is 35% cheaper than current 1.5 Pro. If Phaya is behind, build direct Atlas Cloud / PiAPI adapter.

## The routing rule (updated)

```
Talking head + dialogue (face occupies > 30%, lip-sync needed)
  → HeyGen Avatar IV     (unchanged — best-in-class for Thai lip-sync via edge-tts upload)

Product macro WITH named cinematic camera move (zoom / dolly / orbit / push-in)
  → Higgsfield DoP I2V-01 lite + preset (e.g. "crash-zoom-in", "dolly-in-slow", "orbit-360")
  → max 5s/clip · ~$0.05-0.15/clip at Plus tier
  → REPLACES hold-stills whose visual would benefit from cinematic energy

B-roll transition between two stills (cinematic effect — blur-zoom, dissolve, etc.)
  → Higgsfield Transitions (17 named effects, two-image input)
  → ~$0.04/clip
  → REPLACES manual ffmpeg xfade for cinematic-feel transitions

Two distinct compositions, narrative motion between (CHARACTER motion or scene change)
  → Seedance 2.0 Pro first_last_frames (UPGRADE from 1.5 Pro)
  → Fast @ 720p ($0.16/s) for cost-sensitive · Pro @ 1080p ($0.247/s) for hero shots
  → +31.7 physics accuracy vs 1.5 Pro

Single composition true hold (no motion intent at all)
  → ffmpeg loop-still + edge-tts VO mux     (unchanged)

Wide cinematic establishing shot (rare for affiliate, occasionally needed)
  → Veo 3.1 via Higgsfield (premium tier, $0.14-0.30/clip)

Thai voice-over (any source — hold or HeyGen upload)
  → edge-tts th-TH-NiwatNeural / Premwadee     (unchanged)

Subtitle / closing-tag overlays
  → HyperFrames                              (unchanged)

Hero scene stills
  → Gemini Nano Banana Pro                   (unchanged)
```

## Why this routing wins

The previous v11 used 5 `hold` shots out of 7 — static stills with edge-tts VO over the top. Research from the 3 affiliate-conversion agents (2026-05-15) showed that **static B-roll hurts CVR**: TikTok Shop creators with > 100 units/day always have motion-on-product. Higgsfield's DoP preset library is the cheapest way to add cinematic motion to product macros without re-doing the whole scene as a Seedance two-keyframe call (which is overkill for a product zoom).

So the new routing:
- Keeps the AI-storyboard schema's `hold` generator (true holds still exist — text overlays, title cards)
- Adds `higgsfield_dop` for macro-with-camera-move
- Adds `higgsfield_transition` for cinematic B-roll bridges
- Upgrades `seedance_2kf` → `seedance_2_2kf` (Fast/Pro variant) for the narrative-motion case

This is a SCHEMA EXTENSION, not a breaking change. Old `hold` shots still work; the orchestrator now has more options for new storyboards.

## Higgsfield — adopt details

**Use cases:**
- Concept-2-v3 s0 (product in hand) → could become Higgsfield DoP "slow-push-in" or "crash-zoom-out" macro at 3s — adds motion vs current static hold
- Concept-2-v3 s3 (PD300X capsule + cables) → "dolly-in on USB-C port" reveal at 4s
- Concept-2-v3 s5/s6 (product hero + price) → "orbit-30-degrees" around the mic

**Skip use cases:**
- s2 / s4 (talking head) → HeyGen wins; don't replace
- s1 (split-screen problem) → keep manual composition (Higgsfield can't do split-screen natively)
- Captions → HyperFrames stays

**Concrete costs (Plus tier $49/mo, 1000 credits):**
- DoP I2V lite, 5s clip = ~8 credits = ~$0.39/clip
- DoP I2V preview = ~12 credits = ~$0.59/clip
- Transitions tool = ~5 credits = ~$0.25/clip
- Veo 3.1 (via Higgsfield) = ~20 credits = ~$0.98/clip
- For a 7-shot ad with 3 Higgsfield motion shots: ~$1.20 total

**Risk flags:**
- Thai language for Speak audio NOT verified — keep edge-tts
- DoP trained on human-actor footage, macros may need prompt-engineering for product-centric shots
- Defaults to cinematic-warm color grade — fights the flat UGC look we want
- Rate limits not publicly documented

## Seedance 2.0 — adopt details

**What's new vs 1.5 Pro:**
- +31.7 physics-accuracy points (Megaton benchmark: 73.0 vs 53.0)
- Diffusion-transformer architecture tracks frame relationships → consistent characters across shots
- Native audio + lip-sync in 8 languages (NOT Thai — gap)
- `first_last_frames` task type confirmed for two-keyframe (our use case)
- Multi-modal input: up to 12 images/videos/audio per request

**Pricing (third-party gateways, no Phaya yet):**
- Atlas Cloud: $0.022/s (Fast 480p) · $0.16/s (Fast 720p) · $0.247/s (Pro 1080p)
- PiAPI: $0.08/s (seedance-2-fast) · $0.10/s (seedance-2)
- For our typical 4s transition: Fast 720p = $0.64 · Pro 1080p = $0.99

**Phaya status:** Unknown. Need to probe. If Phaya doesn't support 2.0 yet, the fallback is a direct Atlas Cloud / PiAPI adapter (`src/auto_affi/adapters/seedance_direct.py`, ~100 LOC mirroring HeyGen adapter pattern).

**Risk flags:**
- Aggressive content moderation post-Hollywood pressure blocks realistic human face refs. We pass Thai father portraits as refs — could trigger. Workaround: pass stylized refs (anime / illustration) which they accept.
- No Thai lip-sync (uses English fallback — useless for us)
- Aggressive prompt-structure expectations: 60-100 words, one action verb per shot

## Action plan (when API keys + Phaya support arrive)

1. **Higgsfield API key** → queued to human-queue.md as External access
2. **Probe Phaya for Seedance 2.0** → write a quick `tools/probe-phaya-seedance-2.py` that calls `create_seedance_video()` with a `model_version="2.0"` hint and inspects the error response
3. **Build adapters** when keys arrive:
   - `src/auto_affi/adapters/higgsfield.py` (~150 LOC, mirrors HeyGen async client pattern)
   - Either extend `phaya.py` with `create_seedance_2_video()` OR build `seedance_direct.py` for Atlas Cloud
4. **Schema extension** in `ai_storyboard.py`:
   - Add `Generator.HIGGSFIELD_DOP`, `Generator.HIGGSFIELD_TRANSITION`, `Generator.SEEDANCE_2_FAST`, `Generator.SEEDANCE_2_PRO`
   - Add optional `camera_preset: str | None` field for Higgsfield routing
5. **Orchestrator** in `produce-ai-storyboard.py`:
   - New `_run_higgsfield_dop()` and `_run_higgsfield_transition()` helpers
   - New `_run_seedance_2_2kf()` helper (Fast/Pro variant)
6. **Concept-2-v4 storyboard** (when ready) tests the new routing with 3 Higgsfield motion shots replacing the static holds — A/B against v11

## Sources

**Higgsfield (Agent 1, task a03c793fea1ac5c19):**
- Higgsfield.ai official site, camera-controls page, pricing page, cloud API
- Official Python + Node SDK on GitHub
- Practitioner comparisons (similarlabs.com, aivorapulse, aifunnelinsider)
- Apidog.com for API integration writeup

**Seedance 2.0 (Agent 2, task ac48cb7b4b4ed5208):**
- BytePlus ModelArk official docs
- Megaton Monitor 1.5 vs 2.0 benchmark
- Runware / Cutout.pro / WaveSpeed Seedance 2.0 guides
- Atlas Cloud + PiAPI pricing
- NerdBot honest review (Apr 2026)

Full memos in agent task outputs.
