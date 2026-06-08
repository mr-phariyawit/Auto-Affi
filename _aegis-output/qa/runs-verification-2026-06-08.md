# runs/ Production Verification

_ffprobe-measured (verify_runs.py). 14 runs · 7 with ≥1 clean final · 3 no clean final · 4 no rendered output._

**Verdicts**: `PASS`=1080x1920 + 1 video + 1 audio · `PASS-720`=9:16 + 1v+1a but sub-target res (720x1280) · `OK-silent-src`=9:16 silent B-roll/source (0 audio, expected) · `WARN`=silent but odd · `FAIL`=NOT 9:16 (raw 1024x1024 etc.) or wrong stream counts.

**Scope (honest)**: this checks aspect/resolution/stream-count (cleanroom) only. It does NOT verify caption disclosure, VO speed-guard (1.0–1.15x), caption/VO sync, or product-identity accuracy — those need caption text + voice-segment reports, not ffprobe. Candidate finals = mp4s referenced in approval/manifest JSONs + composited outputs (per-scene `sNNN_*` and raw sources excluded best-effort).


## 2026-06-03-geeso-mini-umbrella

| verdict | file | WxH | dur(s) | v | a | note | declared |
|---|---|---|---|---|---|---|---|
| FAIL | `hyperframes/th-voice-v2/my-video/hf_20260603_103050_visual_only.mp4` | 720x1280 | 15.0 | 1 | 0 | 0 audio (cleanroom=1); 720x1280 9:16 sub-target | ✓ |
| FAIL | `hyperframes/th-voice-v2/my-video/hf_20260603_103050_visual_only.mp4` | 720x1280 | 15.0 | 1 | 0 | 0 audio (cleanroom=1); 720x1280 9:16 sub-target | ✓ |
| PASS | `geeso-mini-umbrella-review-v2-th-voice.mp4` | 1080x1920 | 15.1 | 1 | 1 | 1080x1920, 1v+1a clean | ✓ |
| PASS | `geeso-mini-umbrella-review-v4-scene-sync.mp4` | 1080x1920 | 15.0 | 1 | 1 | 1080x1920, 1v+1a clean | ✓ |
| PASS-720 | `hyperframes/th-voice-v2/my-video/hf_20260603_103050_fac3ae4b-f79c-447f-8a55-232f41cdf312.mp4` | 720x1280 | 15.1 | 1 | 1 | cleanroom OK, sub-target 720x1280 | ✓ |
| PASS | `geeso-mini-umbrella-review-v4-scene-sync.mp4` | 1080x1920 | 15.0 | 1 | 1 | 1080x1920, 1v+1a clean | ✓ |

## 2026-06-03-silicone-shoe-covers

| verdict | file | WxH | dur(s) | v | a | note | declared |
|---|---|---|---|---|---|---|---|
| FAIL | `shoe-covers-30s-visual-only.mp4` | 1080x1920 | 30.0 | 1 | 0 | 0 audio (cleanroom=1); 1080x1920 | ✓ |
| FAIL | `kie_outputs/seedance_visual/d8e6938c1c67c7fac85cf885080ac2b2_1.mp4` | 720x1280 | 15.0 | 1 | 0 | 0 audio (cleanroom=1); 720x1280 9:16 sub-target | ✓ |
| PASS | `shoe-covers-30s-workflow-draft.mp4` | 1080x1920 | 29.9 | 1 | 1 | 1080x1920, 1v+1a clean | ✓ |
| PASS | `shoe-covers-30s-workflow-draft.mp4` | 1080x1920 | 29.9 | 1 | 1 | 1080x1920, 1v+1a clean |  |
| FAIL | `shoe-covers-30s-visual-only.mp4` | 1080x1920 | 30.0 | 1 | 0 | 0 audio (cleanroom=1); 1080x1920 |  |

## 2026-06-04-hanky-dry-towel
- NO RENDERED OUTPUT (intake/smoke only)

## 2026-06-04-hanky-dry-towel-60s-seedance-marketing-test

| verdict | file | WxH | dur(s) | v | a | note | declared |
|---|---|---|---|---|---|---|---|
| PASS-720 | `audio/kie_elevenlabs_v11_youth_audition/labeled_video_segments/09_bella.mp4` | 720x1280 | 7.1 | 1 | 1 | cleanroom OK, sub-target 720x1280 | ✓ |
| PASS-720 | `audio/kie_elevenlabs_v11_youth_audition/labeled_video_segments/08_emma.mp4` | 720x1280 | 8.0 | 1 | 1 | cleanroom OK, sub-target 720x1280 | ✓ |
| PASS-720 | `audio/kie_elevenlabs_v11_youth_audition/labeled_video_segments/04_hope.mp4` | 720x1280 | 7.4 | 1 | 1 | cleanroom OK, sub-target 720x1280 | ✓ |
| PASS-720 | `audio/kie_elevenlabs_v11_youth_audition/labeled_video_segments/05_laura.mp4` | 720x1280 | 7.1 | 1 | 1 | cleanroom OK, sub-target 720x1280 | ✓ |
| PASS-720 | `audio/kie_elevenlabs_v11_youth_audition/labeled_video_segments/07_adeline.mp4` | 720x1280 | 8.6 | 1 | 1 | cleanroom OK, sub-target 720x1280 | ✓ |
| PASS-720 | `audio/kie_elevenlabs_v11_youth_audition/labeled_video_segments/06_lucy.mp4` | 720x1280 | 7.1 | 1 | 1 | cleanroom OK, sub-target 720x1280 | ✓ |

## 2026-06-04-ifilm-phone-pouch-simple-seedance-test

| verdict | file | WxH | dur(s) | v | a | note | declared |
|---|---|---|---|---|---|---|---|
| OK-silent-src | `outputs/seedance_only_simple_phone_pouch_30s_silent.mp4` | 720x1280 | 30.2 | 1 | 0 | 0 audio B-roll; 720x1280 9:16 sub-target | ✓ |

## 2026-06-04-ifilm-waterproof-phone-pouch

| verdict | file | WxH | dur(s) | v | a | note | declared |
|---|---|---|---|---|---|---|---|
| FAIL | `variants/v001-preproduction/visual_only_15s.mp4` | 720x1280 | 15.0 | 1 | 0 | 0 audio (cleanroom=1); 720x1280 9:16 sub-target | ✓ |
| PASS | `variants/v001-preproduction/ifilm-phone-pouch-30s-review-edge-draft.mp4` | 1080x1920 | 29.9 | 1 | 1 | 1080x1920, 1v+1a clean | ✓ |
| FAIL | `variants/v001-preproduction/visual_only_loop_30s.mp4` | 720x1280 | 30.1 | 1 | 0 | 0 audio (cleanroom=1); 720x1280 9:16 sub-target | ✓ |
| PASS | `variants/v001-preproduction/ifilm-phone-pouch-30s-review-edge-draft.mp4` | 1080x1920 | 29.9 | 1 | 1 | 1080x1920, 1v+1a clean |  |
| PASS | `variants/v001-preproduction/ifilm-phone-pouch-15s-hook-sample-edge-draft.mp4` | 1080x1920 | 15.1 | 1 | 1 | 1080x1920, 1v+1a clean |  |
| FAIL | `variants/v001-preproduction/visual_only_loop_30s.mp4` | 720x1280 | 30.1 | 1 | 0 | 0 audio (cleanroom=1); 720x1280 9:16 sub-target |  |

## 2026-06-04-workflow-os-smoke-test-shoe-covers
- NO RENDERED OUTPUT (intake/smoke only)

## 2026-06-05-rhodey-backpack-rain-cover-30s-production
- NO RENDERED OUTPUT (intake/smoke only)

## 2026-06-06-eveandboy-shopee-25362750043-30s-premium-intake

| verdict | file | WxH | dur(s) | v | a | note | declared |
|---|---|---|---|---|---|---|---|
| PASS-720 | `outputs/eucerin_v3_master_storyboard.mp4` | 720x1280 | 30.2 | 1 | 1 | cleanroom OK, sub-target 720x1280 |  |
| OK-silent-src | `outputs/master_video_no_audio.mp4` | 720x1280 | 30.1 | 1 | 0 | 0 audio B-roll; 720x1280 9:16 sub-target |  |
| FAIL | `outputs/task_a.mp4` | 720x1280 | 15.0 | 1 | 0 | 0 audio (cleanroom=1); 720x1280 9:16 sub-target |  |
| FAIL | `outputs/task_b.mp4` | 720x1280 | 15.0 | 1 | 0 | 0 audio (cleanroom=1); 720x1280 9:16 sub-target |  |
| OK-silent-src | `outputs/eucerin_v2_local_animatic_30s_silent.mp4` | 720x1280 | 30.0 | 1 | 0 | 0 audio B-roll; 720x1280 9:16 sub-target |  |
| OK-silent-src | `outputs/eucerin_v3_local_animatic_30s_silent.mp4` | 720x1280 | 30.0 | 1 | 0 | 0 audio B-roll; 720x1280 9:16 sub-target |  |

## 2026-06-06-yomihome-screen-repair-tape-60s-production

| verdict | file | WxH | dur(s) | v | a | note | declared |
|---|---|---|---|---|---|---|---|
| PASS-720 | `outputs/hollywood_v3_caption_voice_preview_v0_1.mp4` | 720x1280 | 26.8 | 1 | 1 | cleanroom OK, sub-target 720x1280 | ✓ |
| FAIL | `outputs/hollywood_v3_caption_preview_v0_1.mp4` | 720x1280 | 26.8 | 1 | 0 | 0 audio (cleanroom=1); 720x1280 9:16 sub-target |  |
| OK-silent-src | `outputs/hollywood_v3_proof_edit_silent_v0.mp4` | 720x1280 | 26.8 | 1 | 0 | 0 audio B-roll; 720x1280 9:16 sub-target |  |
| PASS-720 | `outputs/v3_001_night_tiny_hole_thriller_r2_source.mp4` | 720x1280 | 5.1 | 1 | 1 | cleanroom OK, sub-target 720x1280 |  |
| OK-silent-src | `outputs/v3_001_night_tiny_hole_thriller_r2_silent.mp4` | 720x1280 | 5.0 | 1 | 0 | 0 audio B-roll; 720x1280 9:16 sub-target |  |
| PASS-720 | `outputs/v3_006_cinematic_press_release_r2_source.mp4` | 720x1280 | 5.1 | 1 | 1 | cleanroom OK, sub-target 720x1280 |  |

## 2026-06-08-anua-heartleaf-toner-60s-premium-intake
- NO RENDERED OUTPUT (intake/smoke only)

## 2026-06-08-yonex-aerus-z2-60s

| verdict | file | WxH | dur(s) | v | a | note | declared |
|---|---|---|---|---|---|---|---|
| FAIL | `veo_clip_s02.mp4` | 1024x1024 | 3.0 | 1 | 0 | NOT 9:16 (1024x1024) — raw/source |  |
| FAIL | `veo_clip_s01.mp4` | 1024x1024 | 3.0 | 1 | 0 | NOT 9:16 (1024x1024) — raw/source |  |
| FAIL | `veo_clip_s04.mp4` | 1024x1024 | 3.0 | 1 | 0 | NOT 9:16 (1024x1024) — raw/source |  |
| FAIL | `veo_clip_s03.mp4` | 1024x1024 | 3.0 | 1 | 0 | NOT 9:16 (1024x1024) — raw/source |  |

## 2026-06-08-yonex-aerus-z2-v2-new-flow

| verdict | file | WxH | dur(s) | v | a | note | declared |
|---|---|---|---|---|---|---|---|
| FAIL | `video_only.mp4` | 1024x1024 | 15.0 | 1 | 0 | NOT 9:16 (1024x1024) — raw/source |  |
| FAIL | `clip_s03.mp4` | 1024x1024 | 4.0 | 1 | 0 | NOT 9:16 (1024x1024) — raw/source |  |
| FAIL | `clip_s04.mp4` | 1024x1024 | 4.0 | 1 | 0 | NOT 9:16 (1024x1024) — raw/source |  |
| FAIL | `clip_s01.mp4` | 1024x1024 | 4.0 | 1 | 0 | NOT 9:16 (1024x1024) — raw/source |  |
| FAIL | `clip_s02.mp4` | 1024x1024 | 3.0 | 1 | 0 | NOT 9:16 (1024x1024) — raw/source |  |

## umbrella-way-20260604-161554

| verdict | file | WxH | dur(s) | v | a | note | declared |
|---|---|---|---|---|---|---|---|
| OK-silent-src | `outputs/full_rough_3min_silent.mp4` | 720x1280 | 181.1 | 1 | 0 | 0 audio B-roll; 720x1280 9:16 sub-target |  |
| OK-silent-src | `outputs/rough_act12_reel_silent.mp4` | 720x1280 | 70.4 | 1 | 0 | 0 audio B-roll; 720x1280 9:16 sub-target |  |
| PASS-720 | `outputs/mt02_puddle_memory_transition.mp4` | 720x1280 | 5.1 | 1 | 1 | cleanroom OK, sub-target 720x1280 |  |
| OK-silent-src | `outputs/mt02_puddle_memory_transition_silent.mp4` | 720x1280 | 5.0 | 1 | 0 | 0 audio B-roll; 720x1280 9:16 sub-target |  |
| OK-silent-src | `outputs/proof_reel_10s_silent.mp4` | 720x1280 | 10.1 | 1 | 0 | 0 audio B-roll; 720x1280 9:16 sub-target |  |
| PASS-720 | `outputs/mt01_umbrella_waits_skywalk.mp4` | 720x1280 | 5.1 | 1 | 1 | cleanroom OK, sub-target 720x1280 |  |
