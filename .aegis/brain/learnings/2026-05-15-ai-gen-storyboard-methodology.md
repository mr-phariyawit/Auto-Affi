# AI-Gen Storyboard Methodology + HeyGen Avatar IV Workflow

**Date:** 2026-05-15
**Trigger:** User rejected concept-2 v9. Root cause: original storyboard was authored before we understood HeyGen Avatar IV's actual input constraints or the proper way to STRUCTURE a storyboard for AI generation (vs. for human production crew).
**Decision authority:** Nick Fury, after 2-agent parallel research dispatch.

## The core insight

> Traditional storyboards optimize for human crew coordination. AI-gen
> storyboards must optimize for unambiguous generator specification.
> The storyboard's job flips: "communicate intent to a DP" → "eliminate
> ambiguity for a model".

## Shot-card schema (one JSON per shot)

Every shot in an AI-gen storyboard is a fully-specified deliverable
that engineering can submit to a batch generator without further
interpretation. Required fields:

```jsonc
{
  "shot_id": "s0",
  "duration_s": 4.5,                    // 3-6s — matches AI consistency floor
  "narrative_role": "hook|story|offer", // HSO×VCS function
  "generator": "heygen_avatar_iv|seedance_2kf|seedance_t2v|veo|hold",
  "image_prompt": "...",                // strict, AI-friendly composition
  "visual_reference_lock": [             // attach refs to lock identity
    "characters/father-hero.jpg",
    "product-refs/pd300x-side-clean.jpg"
  ],
  "negatives": [                         // anti-prompts (occlusion etc.)
    "no over-the-shoulder framing",
    "no whip-pan", "no mesh-head microphone"
  ],
  "consistency_seed": 73194,             // FIXED across all shots — prevents drift
  "audio_source": "phaya_tts|seedance_diegetic|music_only|silence",
  "dialogue_th": "...",                  // only if audio_source = phaya_tts
  "subtitle": {                          // per-shot caption overlay
    "text_th": "...", "placement": "lower_third"
  },
  "keyframes": {                         // only if generator = seedance_2kf
    "start_ref": "s0_image.jpg",
    "end_ref":   "s1_image.jpg",
    "motion_label": "slow push-in 50mm"
  }
}
```

## Decision tree — which generator owns this shot

```
Talking head with visible mouth?
├─ YES → HeyGen Avatar IV (chest-up photo + Phaya TTS audio)
│        Limits: 3-6s clean, single speaker, head turn < 30°
│
└─ NO  → Two distinct positions / requires motion between keyframes?
   ├─ YES → Seedance 1.5 Pro two-keyframe (start + end ref attached)
   │
   └─ NO  → Single composition / establishing / B-roll?
      └─ YES → Seedance text-to-video OR hold-still
               (use hold-still when stillness IS the aesthetic)
```

## Scoring heuristic (when in doubt)

Per shot, sum:

- character_visibility ×5 (face occupies > 30% of frame)
- keyframes_needed ×4 (motion between two distinct compositions)
- occlusion_complexity ×3 (foreground objects across subject)
- tts_mandatory ×5 (dialogue with visible mouth)
- duration > 8s ×(-2) (penalize beyond AI consistency floor)
- budget_critical ×3

Highest-scoring branch wins.

## HeyGen Avatar IV — official input constraints

**Photo (the input still that Avatar IV animates):**

- Min 1080p, 9:16 native (matching final aspect)
- CHEST-UP framing — face occupies "substantial portion" of frame
- FRONT-FACING — pure profile / head-turn > 30° fails
- Single person only — multi-person photos produce artifacts
- Mouth slightly open in source still — helps the lip-sync model
- Clean background, soft indirect lighting (no harsh shadows / backlights)
- No foreground occlusion (hand near face, hair across mouth, etc.)
- No anime / heavily stylized characters

**Audio:**

- Single speaker per render — overlapping audio degrades sync
- Clean / noise-free (the single biggest quality factor per HeyGen)
- External TTS (Phaya for Thai) preferred over HeyGen's built-in TTS
- Pad with TRUE silence (not noise) to extend duration

**Per-render limits:**

- Max 180s per single Avatar IV job
- Max 5000 script chars per scene (we hit ~50-100 in practice)
- Split multi-scene ads into 30-60s chunks per render

**Failure modes (avoid at storyboard time):**

- Head turns > 30° during the shot
- Hand or object near mouth in source photo
- Multiple faces in source photo
- Dramatic backlight or strong rim light
- Stylized / anime characters
- Photo too wide (face occupies < 20% of frame)

## Anti-patterns to KILL at storyboard time

| Pattern | Why AI fails | Replacement |
|---|---|---|
| Over-the-shoulder framing | Occlusion + depth-layering confusion | Centered medium shot with shallow DoF |
| Match cut on motion | Generators don't reliably match velocity | Break the cut — use beat hold + transition |
| Whip pan | Angular velocity > 20°/sec causes blur artifacts | Smooth dolly-in / dolly-out instead |
| 3+ persons + camera weaving | Topology errors explode | Split into separate medium shots |
| Vague emotion ("looks sad") | Model interprets loosely | Reference frame lock |
| Day → night without color-temp match | No continuity spec | Explicit color_temp_k field per shot |
| Hand/page near speaker's face | HeyGen lip-sync confused | Move object out of frame; isolate face |
| Mic in foreground of talking-head shot | Foreground occlusion + face occupation | Mic in soft focus background OR separate shot |

## Three-layer delivery model

1. **Layer 1 — Human-readable storyboard** (markdown or sheet image)
   For creative + brand approval; doesn't go to engineering.

2. **Layer 2 — Shot-card JSONL** (one shot per line)
   What engineering submits to the batch generator.

3. **Layer 3 — Orchestration manifest** (single JSON)
   Sequencing, consistency_seed carryforward, post-processing rules,
   output mux spec.

## Practitioner production numbers (50+ videos/month teams)

- 8-16h for a 30-60s video (5 shots) end-to-end
- ~$1.50 / 10s finished clip (vs. ~$5 with single premium generator)
- Reference frame generation: 1h
- Shot-card assembly: 2-3h (engineering)
- Batch video gen: 2-4h (parallel)
- QA + post: 2-4h

## What this means for concept-2 (and Auto-Affi going forward)

Concept-2 v1-v9 violated multiple rules:
- Scene 3 "over-the-shoulder past the microphone" → AI occlusion failure
- Father reading from page with hands in frame → mouth-occlusion risk
- 8s shot durations → past AI consistency floor (need 3-6s)
- No consistency_seed → character drift between shots
- Mic in foreground of dialogue shots → HeyGen Avatar IV confused
- Match-cut entry on scene 4 → generator incompatibility

The fix is NOT another patch on the same storyboard. It's a full
storyboard re-author against this methodology, with the shot-card
schema codified in `src/auto_affi/schemas/ai_storyboard.py` and the
generator-router enforcing the decision tree.

## Sources

**HeyGen workflow (Agent 1):**
- [HeyGen Avatar IV Complete Guide](https://help.heygen.com/en/articles/11269603-heygen-avatar-iv-complete-guide)
- [How to Create an Avatar Using Avatar IV Photo-to-Video](https://help.heygen.com/en/articles/12623520-how-to-create-an-avatar-using-the-avatar-iv-photo-to-video)
- [Avatar IV API announcement](https://www.heygen.com/blog/announcing-the-avatar-iv-api)
- [Product Placement w/ Avatar IV + Veo 3.1](https://help.heygen.com/en/articles/12704854-product-placement-with-avatar-iv-veo-3-1)
- [Avatar/Voice Shooting Tips](https://community.heygen.com/public/resources/avatar-and-voice-shooting-tips-and-tricks)

**Storyboard methodology (Agent 2):**
- [2026 AI Video Production Playbook (Medium)](https://medium.com/@paoloperrone/the-2026-ai-video-production-playbook-bc683d5b85da)
- [JSON Prompting Deep Dive](https://medium.com/@ai.in.motion.blog/video-generation-with-json-prompting-my-deep-dive-into-structured-creativity-e89b4b82c1b8)
- [Video Notation Schema (GitHub)](https://github.com/context-notation/video-notation-schema)
- [Seedance Avatar Shots Prompting Guide](https://community.heygen.com/public/resources/seedance-avatar-shots-prompting-guide-get-the-best-results-in-heygen)
- [Atlas Cloud — State of AI Video APIs 2026](https://www.atlascloud.ai/blog/case-studies/the-state-of-ai-video-apis-in-2026-from-text-to-video-to-cinematic-directing)

Full agent memos archived at:
`_aegis-output/research/ai-storyboard-methodology-2026.md`
(Agent 2 output) and prior task IDs a0ba21e38f7bd594a + a51dcc787cd7e54c7.
