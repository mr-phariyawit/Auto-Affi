---
title: Pre-Generation Checklist (run BEFORE any paid Veo/image/VO call)
created: 2026-06-30
origin: Hollywood-standards do-now #5; hardens the lessons from run umbrella-335 (~$14.4 wasted)
enforced_by: prompt_audit gate (codes below) + this manual gate
---

# Pre-Generation Checklist

> One page. Every box must be ✓ before a paid generation. The first three are now GATE-ENFORCED
> (the audit fails the manifest); the rest are producer judgment.

## Gate-enforced (AuditCode → blocks before spend)
- [ ] **Prompt mode matches generator.** i2v prompt is motion-forward, ONE start frame, NO FLF2V words
      ("between the first and last frame", "last frame", "interpolate"). → `PROMPT_MODE_MISMATCH`
- [ ] **No "prove the negative".** i2v prompt does NOT ask Veo to show an ABSENCE ("no drip", "stays dry",
      "ไม่หยด"). Veo renders the opposite (water pouring). Proof = still cut-in + caption. → `VEO_PROVE_NEGATIVE`
- [ ] **Reference lock + identity.** cast/objects sheets approved; identity string verbatim in prompt;
      exactly one face ref (character); 9:16; seed/soul-id locked. → existing PGA codes.

## Producer judgment (not yet code-gated)
- [ ] **Model + duration in budget.** Veo `veo-3.1-fast-generate-preview`, `durationSeconds:4` (int),
      no `generateAudio`; ≤$1.80/clip. (8s/referenceImages → over cap → DENY.)
- [ ] **Verify-before-spend.** Confirm the exact model ID exists (`catalog`/list-models) before a paid call;
      test ONE clip and LOOK at mid+end frames (motion, anti-message) before firing the batch.
- [ ] **Download path proven.** httpx `follow_redirects=True` (Veo URL 302s; the op already billed).
- [ ] **Hero is Veo-feasible.** Veo SHOWS a state/vibe; it does NOT prove a precise action. The money beat's
      proof lives in a still + caption, not Veo motion.
- [ ] **Format = v2** (`short-form-format-v2.md`): 15s, HOOK≤2s→DEMO→CTA, hook lands muted+sound-on.
- [ ] **VO via ElevenLabs v3 / kie.ai** ([excited]+stability0, th); BGM via kie Suno (ducked); compose in HyperFrames.
- [ ] **Post = HyperFrames** (Noto Sans Thai @font-face; `snapshot`-verify Thai; render local/free; upscale to 1080×1920).

## Wasted-spend ledger (why this exists — run umbrella-335)
$9.6 FLF2V-prompt-on-i2v · $1.6 redirect bug · $1.6 no-drip→water · $1.6 superseded clip = **~$14.4 of $24 video wasted.**
The first two boxes above would have prevented $11.2 of it. Run the checklist.
