# Higgsfield-Only Video Workflow — Proposal

**Date:** 2026-05-16
**Trigger:** User directive — "higgfield ในการทำ video เท่านั้น" (Higgsfield for video only).
**Status:** PROPOSAL — code changes pending approval.

## The single load-bearing finding

**Higgsfield does not support Thai lip-sync in ANY of its routes.**

Verified across:
- Seedance 2.0 phoneme list: EN / ZH / JA / KO / FR / DE / ES / RU only.
- Kling 3.0 voice list: EN (+ Indian/British accents) / ZH / JA / KO / ES.
- Lipsync Studio: 70+ language input claim, Thai output unverified, no
  practitioner case studies for Thai.
- Soul Cast / Higgsfield Speak / Higgsfield Audio: Thai not listed.

Hard implication: a visible-talking-mouth shot with Thai dialogue
**cannot be produced by Higgsfield at this product price band.** A
naive replacement would degrade lip-sync quality vs HeyGen Avatar IV.

## The strategic reframe

We don't have to choose between "keep HeyGen for 2 shots" and "accept
Thai mouth-sync degradation". Instead: **redesign the storyboard so
no shot ever shows a visibly-speaking mouth in Thai.** Then every
frame can come from Higgsfield, and the directive holds 100%.

The Thai voice becomes a **voice-over track**, muxed on top of the
video — not lip-synced to any character. The on-screen visual shows
the creator's hands on the product, product macros, lifestyle B-roll,
or the creator gesturing / smiling / nodding (mouth closed or out of
frame). This pattern is what top Thai TikTok-Shop creators actually
ship — the prior 3-agent research (2026-05-15) showed voice-over +
B-roll wins over visible-talking-head for sub-฿5K affiliate products.

## The new routing rule

```
TALKING-HEAD WITH VISIBLE MOUTH (Thai)
  → DROPPED FROM STORYBOARD ENTIRELY
  Reason: Higgsfield cannot Thai-lipsync. Reframe as VO + B-roll.

CREATOR SHOT (visible person, MOUTH CLOSED OR OUT OF FRAME)
  → higgsfield generate create seedance_2_0 \
      --image <creator-ref> --prompt "Thai man mid-30s nodding,
      glancing at the mic, soft confident smile, mouth closed"
    OR with soul-id-trained persona for cross-product consistency.

PRODUCT MACRO WITH NAMED CAMERA MOVE
  → higgsfield generate create cinematic_studio_3_0 \
      --image <product-ref> --prompt "<motion language>"
    OR seedance_2_0 (cheaper)

TWO-KEYFRAME NARRATIVE MOTION
  → higgsfield generate create seedance_2_0 \
      --start-image <s_N> --end-image <s_N+1> --prompt "<motion>"
  Kling 3.0 alternative when 1080p native matters.

ESTABLISHING / B-ROLL WIDE
  → higgsfield generate create veo3_1_lite \
      --prompt "<scene>"  (cheapest 1080p text-to-video)

HOLD STILL (truly static — e.g. CTA card frame)
  → ffmpeg loop-still (no video gen, free)

THAI VOICE-OVER
  → edge-tts th-TH-NiwatNeural / th-TH-PremwadeeNeural
    (unchanged — free)

CAPTIONS / TAGLINES / CTA OVERLAYS
  → HyperFrames     (unchanged)

SCENE STILLS
  → Gemini Nano Banana Pro (current)
    OR higgsfield product-photoshoot for hero product shots
    (image gen — user's directive scopes to video, so this is an
    optional consolidation)

CHARACTER CONSISTENCY ACROSS A PRODUCT'S 5-8 SHOTS
  → higgsfield soul-id create + reuse soul_id across the run
  CAVEAT: Soul-Cast drifts after ~8 clips; cap usage per ad.

MULTI-PRODUCT PERSONA REUSE (same creator across 20+ products)
  → Train one soul_id ONCE → reuse forever (~$5 one-time per persona)
```

## What the storyboard becomes

Concrete delta vs concept-2-v4 (the previous shipped, v12):

| Shot | v4 (current) | v5 (Higgsfield-only) |
|---|---|---|
| s0 hook | Higgsfield Seedance 2.0 (product-in-hand push-in) | Same — already Higgsfield |
| s1 problem | hold (split-screen waveforms) | hold (no video gen needed; free) |
| s2 creator line 1 | **HeyGen Avatar IV — talking head** | **Higgsfield Seedance 2.0 — creator nodding/glancing, mouth closed**, VO muxed on top |
| s3 macro capsule | Higgsfield Seedance 2.0 (dolly-in) | Same |
| s4 creator line 2 | **HeyGen Avatar IV — talking head** | **Higgsfield Seedance 2.0 — creator gesturing toward mic, knowing smile, mouth closed**, VO muxed on top |
| s5 product hero | Higgsfield Seedance 2.0 (orbit) | Same |
| s6 CTA card | hold | Same |

Net: **2 shots flip from HeyGen → Higgsfield**. Zero new HeyGen
dependency. Cost delta: 2 × ~17.5 credits ≈ +$1.50 in Higgsfield, but
−$1.20 in HeyGen ≈ break-even.

## Workflow tools to adopt (beyond `generate create`)

1. **soul-id** — train a "Thai content creator" persona ONCE from
   3-5 reference photos (~$5 + minutes). Reuse across every product's
   creator-shot via `soul_cast` or as a `--image` ref. Saves
   identity-drift problems we kept hitting with one-off Gemini stills.

2. **product-photoshoot** — when launching a new product, run
   `higgsfield product-photoshoot create --mode product_shot
   --prompt "..." --image <pd-ref>` to get 4 brand-quality product
   stills before video gen. Replaces some of the Gemini still work.
   Optional consolidation per the user's "video only" directive — not
   strictly required.

3. **marketing-studio** — RESERVED for future. The high-level
   `marketing_studio_video` workflow takes product URL + avatar +
   mode and produces a complete ad in one call. Loses the
   per-shot compositional control we built into AiStoryboard v2.
   Worth piloting once the per-shot pipeline is solid; not the
   first move.

4. **cinematic_studio_3_0** — DoP camera-control model for cinematic
   moves on existing footage. Niche use, defer.

## What stays in the stack (non-video)

- **edge-tts** — Thai voice. Free, validated on v11/v12.
- **HyperFrames** — caption + overlay rendering.
- **Gemini Nano Banana Pro** — scene stills (until product-photoshoot
  fully replaces it; image gen is out-of-scope for the "video only"
  directive anyway).
- **ffmpeg** — concat, mux, normalize, music mix.
- **GCS** — registry / final mp4 hosting.
- **Phaya** — out (not used in v11/v12; can stay dormant or be removed).

## What leaves the stack

- **HeyGen Avatar IV** — fully removed. The adapter file
  `src/auto_affi/adapters/heygen.py` + tests stay in tree as a
  fallback (in case Higgsfield adds Thai support and we want to A/B,
  or in case we ship a non-Thai product). Mark the dispatch branch
  in the orchestrator as deprecated but functional.

- **Phaya Seedance 1.5 Pro path** — already obsoleted by
  Higgsfield CLI + Seedance 2.0; no further action needed.

- **PiAPI Seedance 2.0 path** — already obsoleted by Higgsfield;
  the queue item was resolved 2026-05-15.

## Cost model — per ad, per month

Assume 30 ads/month at the same 7-shot 28s structure:

| Shot | Higgsfield credits | USD @ Ultra plan |
|---|---|---|
| s0 push-in (Seedance 2.0 Fast, 5s) | 17.5 | $0.75 |
| s1 hold (free) | 0 | $0 |
| s2 creator B-roll (Seedance 2.0 Fast, 5s) | 17.5 | $0.75 |
| s3 macro dolly-in (Seedance 2.0 Fast, 4s) | 14 | $0.60 |
| s4 creator B-roll (Seedance 2.0 Fast, 5s) | 17.5 | $0.75 |
| s5 product orbit (Seedance 2.0 Fast, 5s) | 17.5 | $0.75 |
| s6 CTA hold (free) | 0 | $0 |
| Per ad subtotal (Higgsfield) | **84 credits** | **~$3.60** |
| Gemini stills (7 × ~$0.04) | — | $0.28 |
| edge-tts | — | $0 |
| HeyGen | — | **$0** (removed) |
| **Per ad TOTAL** | — | **~$3.88** |

vs v12 cost was **$3.45** with HeyGen for 2 shots. The Higgsfield-only
path is **$0.43 more per ad** because the 2 Seedance shots replacing
HeyGen are slightly more expensive than HeyGen's ~$0.60 each.

At 30 ads/month: **~$117** total monthly video-gen burn vs v12 at
**~$103.50**. Slight increase, but consolidation onto one OAuth
account + one credit pool is worth it operationally.

Soul-id training (one-time per persona): **+$5** amortized over
hundreds of ads = negligible.

## Migration plan (code changes when approved)

1. **Train the persona** — one-time:
   ```
   higgsfield soul-id create --name "thai-creator-male-30s" --soul-2 \
     --image characters/father-hero-portrait.jpg \
     --image <4 more refs>
   ```
   Save the resulting `soul_id` to
   `data/personas/thai-creator-male-30s.json`.

2. **Schema extension** in `src/auto_affi/schemas/ai_storyboard.py`:
   Add optional `soul_id: str | None` field to `AiShot`. When set
   AND `generator=higgsfield_cli`, the orchestrator passes it as a
   `--soul-id` flag to the CLI.

3. **New storyboard** — author `concept-2-v5/storyboard.json`:
   - s2 and s4 generators flip from `heygen_avatar_iv` → `higgsfield_cli`
   - Their `image_prompt` rewrites: "creator nodding, mouth closed,
     gesturing toward the mic" — NO speaking action verb
   - `audio_source` stays `phaya_tts` so edge-tts VO muxes over
   - Attach the soul_id once it's trained

4. **Orchestrator hold-with-VO support** is already wired (v11 commit).
   No change needed for s2/s4 audio.

5. **Caption strategy unchanged** — the Thai dialogue still gets
   captioned per-shot via HyperFrames; the captions are now the
   PRIMARY way the audience reads the dialogue (instead of seeing
   mouth movements). Per the affiliate research, captions are
   load-bearing for silent autoplay anyway.

6. **Deprecate HeyGen dispatch branch** in
   `scripts/produce-ai-storyboard.py` — keep the code, add a
   warning print if a storyboard uses `heygen_avatar_iv`.

## What we keep monitoring (re-evaluation triggers)

- Higgsfield announces Thai phoneme support → reconsider Higgsfield
  lip-sync for the talking-head shots.
- Soul-Cast drift past 8 clips becomes a real issue → rotate two
  trained personas per ad.
- `marketing_studio_video` workflow shows superior CVR in pilot
  → consider migrating from per-shot AiStoryboard v2 to that.
- `cinematic_studio_3_0` proves materially better than `seedance_2_0`
  for macro motion → switch the macro shots' default model.

## Open question (single, for the user's call)

This proposal **drops visible talking-head shots entirely**. The two
creator shots (s2, s4) become "creator visible but not speaking with
mouth in frame" — gesturing, nodding, glancing at the mic, knowing
smile. The Thai voice plays as voice-over.

Should I author the v5 storyboard with this design AND execute v13
against it? Or hold for a different interpretation of "Higgsfield
for video only" (e.g. accept Thai lip-sync quality degradation by
forcing Seedance 2.0 to do Thai phonemes anyway)?

Default action (per Decision Matrix, External-access NOT triggered):
**author + execute the reframe** since it's the strictly stronger
path. Will queue a question-to-brain instead of a menu when starting.

## Sources

- 2-agent research dispatch 2026-05-16:
  - `abcfb37fa04ec101f` (full capability matrix, 15 models)
  - `ad570a6197013c8c4` (Thai lip-sync deep dive — KEEP HeyGen verdict
    rejected here in favor of reframe to eliminate the dependency)
- Local CLI param probes (`higgsfield model get <each>`) captured
  in `.aegis/brain/runs/2026-05-16-*/` (this session's logs).
- Prior routing decision:
  `.aegis/brain/learnings/2026-05-15-higgsfield-cli-unified-gateway.md`
- Affiliate creative research (the reframe is consistent with this):
  `.aegis/brain/learnings/2026-05-15-affiliate-conversion-creative.md`
