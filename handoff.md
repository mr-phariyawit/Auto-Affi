# Auto-Affi Sprint Handoff

Closed: 2026-06-03
Timezone: Asia/Bangkok
Sprint focus: prove one-product-to-one-production-review-video workflow for Auto-Affi.

## Sprint Result

This sprint is closed with a working production-review pipeline:


Latest review artifact:

```text
```

Status:

- Product: silicone waterproof shoe covers / Thai Home Center / observed price starts at 19 THB.
- Product timing signal: Thai rainy-season/weather signal.
- Output status: ready for human review.
- Public publish status: blocked until human approval, affiliate link/subIds, and platform/caption disclosure gate.
- Final on-media disclosure: removed from video and spoken voice by user request.
- Caption/platform disclosure: still required before public posting.

## Final Files

Core final:

```text
runs/2026-06-03-silicone-shoe-covers/production_kie_v2_no_disclosure_manifest.json
runs/2026-06-03-silicone-shoe-covers/approval_packet.json
runs/2026-06-03-silicone-shoe-covers/review_frames_production_v2_no_disclosure/
```

Source media:

```text
runs/2026-06-03-silicone-shoe-covers/kie_outputs/seedance_visual/d8e6938c1c67c7fac85cf885080ac2b2_1.mp4
runs/2026-06-03-silicone-shoe-covers/audio/voice_th_30s_kie_elevenlabs_bella_no_disclosure.wav
```

Production scripts:

```text
runs/2026-06-03-silicone-shoe-covers/scripts/kie_generate_scene_voice_30s.py
runs/2026-06-03-silicone-shoe-covers/scripts/build_30s_kie_production_clip.py
runs/2026-06-03-silicone-shoe-covers/scripts/build_30s_kie_production_clip_v2_no_disclosure.py
runs/2026-06-03-silicone-shoe-covers/scripts/build_30s_local_clip.py
```

## Verification

Latest v2 checks:

```text
duration: 29.91s
resolution: 1080x1920
visual-only source audio streams: 0
final audio streams: 1
final video streams: 1
voice speed factor: 1.0x for every scene
speed guard errors: none
```

Visual review:

- Top on-video `โฆษณา / Affiliate` label was removed.
- Spoken `โฆษณา affiliate` line was removed.
- Final CTA voice is `ดูราคาในลิงก์นะคะ`.
- Final CTA caption is `ดูราคาในลิงก์`.

Remaining human-review risk:


## New Principle Created

The sprint produced a new workflow principle:

```text
docs/principles/2026-06-03-production-review-principle.md
```

The principle was also added to:

```text
SUPER_SPEC.md
/Users/phariyawit.jiap/.codex/skills/auto-affi-one-shot-workflow/SKILL.md
/Users/phariyawit.jiap/.codex/skills/thai-voiceover-hyperframes/SKILL.md
```

Principle summary:

> One timely product becomes one production-review clip that feels like a natural Thai commercial, uses generated visuals only as silent B-roll, uses separate scene-synced Thai voice, passes cleanroom audio verification, and stays blocked from public publish until human approval and platform/caption disclosure gates are satisfied.

Non-negotiable production rules learned:

- Use Thai-news-first product intelligence.
- Default to 30s commercial master for Thai affiliate review clips.
- Generated video audio is draft-only; final source video must be visual-only.
- Thai VO must be separate, scene-synced, and natural.
- Do not solve timing by speeding up Thai voice.
- Preferred voice speed factor is 1.0x; warning above 1.08x; reject above 1.15x.
- Final MP4 must have exactly one intended audio stream.
- Thai captions are composited in post, not drawn by the video model.
- On-media disclosure may be removed for a review variant, but public publish still needs platform/caption disclosure.
- A beautiful clip fails if product identity drifts from the real Shopee item.

## Model/API Notes


- Credit check worked. Current main workflow now assumes production provider keys are provisioned in `.env` and loaded before provider calls.
- `bytedance/seedance-2-fast` generated the source visual.
- `elevenlabs/text-to-dialogue-v3` generated Thai scene voice.
- Bella voice id used: `hpp4J3VqNfWAUOO0d1Us`.


- Seedance visual task consumed 495 credits for one 15s source video.
- ElevenLabs VO was low-cost by comparison.
- Last successful credit check before v2 replacement voice showed 38.5 credits; v2 replacement voice consumed 0.28 credits.
- Clipboard is no longer the normal production key path. Load `.env` before paid provider calls and never print secret values.


- Python helper upload hit `HTTP 403: error code: 1010` against the upload CDN.
- Direct `curl --location https://kieai.redpandaai.co/api/file-stream-upload ...` worked.
- Next sprint should fix the helper's multipart upload behavior or use curl for uploads.

## Re-Render Commands

Re-render final v2 from existing downloaded assets:

```bash
cd /Users/phariyawit.jiap/Documents/Auto-Affi
python3 runs/2026-06-03-silicone-shoe-covers/scripts/build_30s_kie_production_clip_v2_no_disclosure.py
```

Re-render v1 with on-video disclosure:

```bash
cd /Users/phariyawit.jiap/Documents/Auto-Affi
python3 runs/2026-06-03-silicone-shoe-covers/scripts/build_30s_kie_production_clip.py
```


```bash
cd /Users/phariyawit.jiap/Documents/Auto-Affi
set -a
source .env
set +a
python3 runs/2026-06-03-silicone-shoe-covers/scripts/kie_generate_scene_voice_30s.py --force
```

## Open Gates

Do not public-publish yet. These are still required:

1. Human review/approval of product accuracy and final creative.
2. Valid Shopee affiliate shortlink and five subIds.
3. Caption/platform commercial-content disclosure before public publish.
4. TikTok API/OAuth/audit path, or manual upload path.
5. Shopee Video official path, or human app upload packet.
7. Product identity review because the generated shoe-cover visual can read as a boot.

## Recommended Next Sprint

1. Make product identity more controllable:
   - try first-frame plus last-frame video control, or Wan/Kling image-to-video;
   - avoid outputs that visually turn shoe covers into boots;
   - keep real product images in the edit as anchor frames.
2. Add an automated cleanroom verifier command:
   - final must have exactly one audio stream;
   - source visual must have zero audio streams;
   - speed guard must be empty.
3. Add a publish packet builder:
   - MP4;
   - caption;
   - Shopee URL/affiliate URL/subIds;
   - platform disclosure settings;
   - product attachment metadata.
4. Run the next product from the same principle:
   - Thai news/weather scout;
   - CSV record;
   - product normalizer;
   - v2-style cleanroom render.

## Repo/Workspace Caution

The Auto-Affi worktree was already in a heavily cleaned/consolidated state with many tracked files marked deleted and the current useful state reduced mostly to:

```text
SUPER_SPEC.md
data/
docs/
runs/
scripts/
handoff.md
```

Do not run destructive git recovery commands unless explicitly requested. The current sprint artifacts live in the files listed above.
