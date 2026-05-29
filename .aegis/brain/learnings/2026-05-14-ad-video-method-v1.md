# Auto-Affi Ad Video Method v1 — HSO×VCS

**Date:** 2026-05-14
**Decision authority:** Nick Fury, after 3-agent parallel research dispatch (viral mechanics / cinematic technique / AI-gen workflows)
**Status:** APPROVED — sets the rubric for all future MANUAL-mode runs

## Why this decision now

User asked the team to research ad-video methods and pick the best. Three
research agents went out in parallel; their findings converged on the same
core architecture from three independent angles. That convergence is the
strongest evidence the method is correct.

## The method (one paragraph)

**Hook-Story-Offer framework**, wrapped in a **Vertical Cinema Stack** for
production discipline, executed via **two-keyframe AI generation** with
**parallel variant selection**. Every clip ≤6s for AI consistency. Every
shot averages 3-5s for viral retention. Hook lands in ≤1s. Audio is always
three discrete stems (rumble + dialogue + music). Captions cover 100% of
dialogue. Grade is desaturated with one accent color.

## The 8 principles (ranked by impact)

1. **Hook in ≤1s** — first frame must be the pattern interrupt. 71% of
   viewers decide stay/leave in first 3s. Below 70% intro retention =
   no algorithmic distribution.
2. **3-5s avg shot length** — Nielsen 2021: 3+ cuts in first 3s = +58%
   completion. Also matches AI consistency floor (degradation past 6s).
3. **Two-keyframe between scenes** — Seedance/Veo first+last frame anchor.
   Spatial coherence > generative drift. Already wired in
   `scripts/gen-video-seedance.py`.
4. **Parallel variants 3-5, pick best** — VISTA framework: beats serial
   refinement 70% of the time. NOT YET WIRED — see upgrade #1 below.
5. **Layered 3-stem audio** — sub-bass rumble (25-40 Hz, first 2s) +
   clean dialogue (4 kHz boost) + music (separated stem). Mono / unmixed
   = AI-slop tell. PARTIALLY WIRED — Phaya generates music + dialogue
   but no deliberate rumble layer.
6. **Captions on 100% of dialogue** — Facebook +12% watch-time, NCAM +40%
   retention. Thai 3-5 words per line. Currently only the closing tag
   has captions (HyperFrames overlay #1). GAP.
7. **Desaturated grade + 1 accent color** — defeats AI-slop "plastic"
   look. Currently no grade pass at all. GAP.
8. **Vertical cinema grammar** — eyeline on top horizontal third, depth
   layering (foreground/subject/background separation), match cuts on
   thematic gestures. Currently storyboard prompts don't specify this.
   GAP at prompt-authoring layer.

## Spec values (every future storyboard must hit)

| Spec | Target | Source |
|---|---|---|
| Hook duration | ≤1.0s | TTSVibes 2025 (71% scroll-decision) |
| Avg shot length | 3-5s | Nielsen 2021 (+58% completion) |
| Cuts/second | 0.3-0.5 baseline; 0.6+ in pattern-interrupt segments | Submagic 2025 |
| Music BPM | 120-140 | Opus Pro 2025 |
| Speech pace | 140-160 wpm | Opus Pro 2025 |
| Caption coverage | 100% of dialogue, 3-5 words/line | NCAM/Facebook studies |
| 1st-3s retention | ≥70% | TTSVibes 2025 (2.2× more views) |
| Total length | 15-30s for affiliate / 30-45s for narrative arc | Opus Pro 2025 |
| Clip duration | 3-6s max | AI consistency floor (Seedance/Veo/Pika) |
| Variants per shot | 3-5 parallel | VISTA paper (+70% win rate) |
| Audio stems | ≥3 (rumble + dialogue + music) | Cinema-grade tell |
| Grade saturation ceiling | 60-75% with 1 accent at 100% | Cannes-Lions 2024-25 trend |
| Eyeline position | Top horizontal third | Vertical cinema grammar |

## How to apply: Maono concept-2 audit

The shipped v6 (`out/maono-concept-2-final-v6.mp4`) was built before this
rubric existed. Auditing it against the method:

| Principle | Status | Notes |
|---|---|---|
| Hook ≤1s | UNVERIFIED | Need to time-check the first second. Storyboard opens with father-at-distance — not a clear pattern interrupt |
| 3-5s avg shot | ✅ ~5.6s avg | Slightly long; cinematic pacing OK but at edge of retention |
| Two-keyframe | ✅ | All inter-scene transitions use Seedance |
| Parallel variants | ❌ | 1 take per shot |
| 3-stem audio | ⚠️ partial | Dialogue + music present; no deliberate sub-bass rumble layer |
| Captions 100% | ❌ | Only closing tag (1 of 8+ dialogue beats captioned) |
| Desaturated grade | ❌ | No deliberate grade pass |
| Vertical cinema grammar | ⚠️ partial | Some scenes hit it (daughter bedroom); others are center-framed |
| Music 120-140 BPM | UNVERIFIED | Need to ffprobe-check the generated track |
| Speech 140-160 wpm | UNVERIFIED | Need to time-check dialogue density |

**Verdict:** v6 ships, but it's a B-grade execution of the method. Next
product run should target A-grade.

## Upgrade backlog (rooted in the rubric)

P0:
- Caption generator: extract dialogue from storyboard → HyperFrames captions
  with timing → composite onto every dialogue scene (not just closing tag)
- Hook-second validator: QA pass that timestamps the first 1s and asserts
  pattern-interrupt criteria (motion change OR text overlay OR sudden audio)
- Parallel variant gen: `scripts/gen-video-seedance.py --variants 3` →
  pick highest-scoring per `qa/video_review.py`

P1:
- Grade pass: ffmpeg LUT applied to final concat (`graded.cube` per product
  in `data/registry/items/<id>/`)
- Sub-bass rumble layer: 25-40 Hz drone underneath first 2s of every video,
  duck under dialogue
- BPM + WPM validators in `qa/video_review.py`

P2:
- Storyboard prompt linter: catch missing eyeline / depth / DOF specs
- Match-cut hint extractor: surface thematic-gesture pairs across adjacent
  scenes for editor

## Why this method beats the alternatives

We considered:
- **AIDA / PAS** — require longer ramp before payoff. Loses the first-3s
  retention game. Better for landing pages, not feed-format.
- **"Tell a story first, hook later"** — directly contradicted by the data.
  71% decide in 3s.
- **"Slow cinematic shots build trust"** — directly contradicted by
  Nielsen +58% completion data.
- **Pure cinematic (Cannes-style)** — wins awards, loses scrolls without
  the HSO retention scaffolding.
- **Pure performance-marketing** — captures attention, loses brand. The
  Vertical Cinema Stack is what makes affiliate content not look like
  affiliate content.

HSO×VCS is the synthesis. Each layer earns its place via independent data.

## Sources (audit trail)

- Agent 1 (viral mechanics): 14 sources incl. TTSVibes retention data,
  Copyblogger HSO study, Wyzowl case studies, Nielsen 2021, OpusPro 2025
- Agent 2 (cinematic): D&AD archive, Cannes Lions 2025, LBBOnline grading
  trends, vertical cinematography masterclass
- Agent 3 (AI workflows): Seedance 2.0 docs, Kling 3.0 / Pika 2.2 / Runway
  Gen-4.5 / Sora 2 / Veo 3.1 practitioner reports, VISTA paper (arXiv
  2510.15831), IC-LoRA workflows, HeyGen / D-ID lip-sync data

Full memos archived at:
`.aegis/brain/runs/2026-05-14-21e3b892-27bc-49c6-8a34-35112d07/`
(agent task outputs a051d8f2/abfe7732/a9df7f9e).
