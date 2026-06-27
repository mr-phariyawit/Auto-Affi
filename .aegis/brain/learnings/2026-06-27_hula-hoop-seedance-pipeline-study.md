# Learnings — Hula Hoop ฿239 Seedance Pipeline (external project study)

**Date:** 2026-06-27
**Source:** `wPWBPsAQ.tgz` — external affiliate-video pipeline (`/opt/data/products/hula-hoop-239/`)
**Why studied:** Near-identical domain to Auto-Affi (Shopee affiliate video ads via AI image-to-video).
Goal: harvest their verified successes and (cost-bearing) failures into our brain.

---

## What the project is

Pipeline: **Character (JIAP02) → Storyboard → Starting Frames → AI Image-to-Video → Edit → Final.**
4 shots × 8s = ~32s, 9:16, Shopee product (weighted hula hoop ฿239). Providers tried: Veo 3.1 (blocked),
Seedance 2.0 Mini via kie.ai (shipped). Character = AI male presenter that must stay consistent across shots.

This is the SAME shape as Auto-Affi (Scout → Strategist → Writer → Storyboard → Producer/Editor → Compliance).

---

## Successes worth copying [VERIFIED: read from their SEEDANCE_SYSTEM_SPEC.md §7,§8]

1. **Single source-of-truth spec** with pipeline-ordered folders (`00-source`→`03-veo-output`). State is legible at a glance. — We already do this (SPEC + runs/).
2. **Identity lock as one canonical string** injected into every prompt (`JIAP02_IDENTITY`), NOT multiple competing reference images.
3. **Human approval gates only at cost/irreversible points** — after storyboard, after clip QC, before final export. Matches our MBP (only 4 categories reach human).
4. **Pre-flight vision check before paid API** — `vision_analyze(frame, ref)` must confirm "same person" BEFORE burning credits.
5. **Concrete pitfall→fix table** as a standing artifact (not vague warnings).

---

## Failures that cost real money [VERIFIED: their §8 pitfall log, dated 26Jun26]

| # | Failure | Root cause | Cost paid |
|:-:|:--|:--|:--|
| 1 | `reference_image_2` → wrong face | Frame had a different face + identity ref as 2nd image → model saw 2 faces → matched neither | Whole batch credits wasted |
| 2 | Veo 3.1 RAI audio filter blocked indoor prompts | `generate_audio` needs Enterprise tier; Developer API silently blocks | Forced mid-project provider swap → Seedance |
| 3 | Starting frame had a foam roller in shot | Model focused on the wrong object, not the product | Re-gen frame |
| 4 | Gemini returned the reference sheet, not a new image | Prompt didn't explicitly say "create a NEW image" | Wasted gen round |
| 5 | Credits ran out mid-batch → partial loss | No balance check before firing 4 shots | Partial batch loss |
| 6 | Duplicate `gen_seedance_shots.py` (legacy "do NOT use") left in tree | Old script never deleted, only commented | Risk of running wrong script |

**Common root cause:** paid + non-deterministic AI gen with *implicit* constraints (filters, ref-image count,
in-frame objects) → every retry = real money → **verify before spend, always.**

---

## Transferable rules for Auto-Affi (actionable)

1. **VERIFY-BEFORE-SPEND gate (bind to global "PRODUCED ≠ VERIFIED" rule):** before ANY paid AI call (image/video/VO),
   run a pre-flight check (asset identity, in-frame correctness, prompt sanity) AND assert provider credit balance.
   Tag the call `[VERIFIED]` only after the *output* is checked, never after mere submission.
2. **One canonical identity/brand string, injected everywhere.** Never stack multiple competing reference images for the same identity.
3. **Provider = swappable adapter from day 1.** They got blocked by Veo's hidden filter and had to swap. Our adapter pattern (Higgsfield/Seedance/Gemini) must never hard-assume one provider's constraints.
4. **Pre-flight asset hygiene:** the input frame must contain ONLY the intended product/subject — stray props hijack the model's focus.
5. **Explicit "generate NEW image" instruction** when a model can echo its reference input.
6. **Delete legacy scripts, don't comment them "do not use".** A "do NOT use" note does not stop a wrong run.
7. **Every product run ships a pitfall→fix table** as a standing artifact.

Related: [[verify-before-spend-gate]], project compliance/cost-cap work (AFFI-S1-06/07).
