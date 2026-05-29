# AI-Generated Short-Form Video Storyboarding: Methodology & Schema (2026)

## Executive Summary

Traditional storyboards optimized for human crews miss critical AI-generation fields. Current practitioners (studios running 50+ AI video projects/month) use a **three-layer workflow**: (1) reference frame locks via image generation, (2) shot-card specifications with routing metadata, (3) JSON API payloads for orchestration. The "shot card" is a JSON structure that bundles visual specification, generator routing, audio source, and timing—not a human-readable visual board.

**Key finding**: The storyboard's primary job in AI workflows is *eliminating ambiguity at generation time*, not communicating intent to crews. This inverts traditional storyboarding.

---

## 1. AI-Gen Storyboard Fields (vs. Traditional)

### Traditional Storyboard Columns
- Shot description
- Dialogue/voiceover
- Sound design notes
- Camera movement
- Duration

### AI-Gen Storyboard ADDS / REPLACES WITH

| Field | Purpose | Example |
|-------|---------|---------|
| **Image Prompt** | Directs image model for reference frame | "Medium shot, warm 3-point lighting, subject facing camera-left at 45°, office background, daylight, shallow depth-of-field" |
| **Visual Reference Lock** | Character/object consistency across shots | `ref_image_id: "char_main_001"`, `lighting_match: "shot_02"` |
| **Generator Routing** | Which tool for THIS shot + WHY | `{"tool": "seedance_2_fast", "reason": "avatar_talking_head", "reference_inputs": 1, "max_duration_sec": 6}` |
| **Keyframe Spec** (for motion shots) | Start frame + end frame + motion vector | `{"keyframe_start": "char_profile_walking_left", "keyframe_end": "char_profile_walking_right", "motion_type": "lateral_tracking"}` |
| **Duration Floor/Ceiling** | AI consistency constraint (generators work in 3-6s buckets) | `{"min_sec": 3, "target_sec": 4.5, "max_sec": 6}` |
| **Audio Source** | In-video TTS+lip-sync vs. external audio vs. silent | `{"type": "seedance_native_tts", "language": "th", "voice_id": "phaya_algenib_warm"}` or `{"type": "external_wav", "path": "audio/vo_shot_03.wav"}` |
| **Caption Placement** | Where subtitles sit (top/bottom/center) + font metadata | `{"position": "bottom", "safe_margin_px": 24, "font_scale": 1.0, "background": "semi-transparent"}` |
| **Negatives** | Explicitly exclude artifacts/concepts | `["motion_blur", "depth_error", "face_distortion", "occlusion_glitch"]` |
| **Consistency Seed** | Ensures frame-to-frame coherence | `12847` (fixed across related shots) |

**Why these matter**: A traditional "over-the-shoulder shot" fails in AI because:
- No depth spec → AI struggles with occlusion/layering
- No camera movement constraint → AI may interpolate invalid motion
- No reference lock → character appears inconsistent shot-to-shot
- No audio routing → unclear if TTS or external audio

---

## 2. The Shot Card JSON Schema

```json
{
  "shot_id": "03_talking_head",
  "scene_num": 3,
  "duration_target_sec": 4.5,
  
  "visual_spec": {
    "image_prompt": "Medium close-up of woman, 45° camera-left, seated at desk, warm office lighting (3200K key, soft fill), shallow DoF, green wall background, confident expression looking at camera",
    "reference_lock": {
      "character_id": "protagonist_001",
      "character_ref_image": "assets/char_main_setup_frame.jpg",
      "lighting_match_to_shot": "02_medium",
      "environment_continuity": "office_steady"
    },
    "camera": {
      "shot_type": "medium_close_up",
      "angle_degrees": 45,
      "movement": "none",
      "lens_equivalent_mm": 50,
      "focus": "face"
    },
    "negatives": ["motion_blur", "facial_jitter", "occlusion_artifact"],
    "consistency_seed": 8847
  },
  
  "audio_spec": {
    "type": "seedance_native_tts",
    "language": "th",
    "voice_id": "phaya_algenib_warm",
    "script_text": "เราไปสร้างสิ่งที่ยอดเยี่ยม",
    "speech_rate": 1.0,
    "emotion_tone": "confident"
  },
  
  "video_generation": {
    "tool": "heygen_seedance_2_fast",
    "reason": "talking_head_avatar_with_native_tts",
    "reference_inputs_count": 1,
    "reference_input_0": "image_prompt_frame",
    "max_duration_sec": 6,
    "api_params": {
      "quality": "standard",
      "fps": 24
    }
  },
  
  "composition": {
    "frame_layout": {
      "foreground": "character_seated",
      "midground": "desk_elements",
      "background": "office_wall"
    },
    "safe_zone_margin_percent": 10,
    "aspect_ratio": "9:16"
  },
  
  "subtitles": {
    "enabled": true,
    "text": "เราไปสร้างสิ่งที่ยอดเยี่ยม",
    "position": "bottom",
    "margin_safe_px": 24,
    "font_size_scale": 1.0,
    "background_style": "semi_transparent_black"
  },
  
  "notes": "Part of brand intro sequence. Maintain eye contact with camera. No hand gestures in this shot.",
  "variant_for_platform": "tiktok_9_16"
}
```

**Delivery format**: One JSON per shot, or a JSONL file with one shot object per line for batch API submission.

---

## 3. Decision Rules: When to Route to Which Tool

### Decision Tree

```
Shot = talking head (single person, mouth visible)?
├─ YES → HeyGen Avatar IV (photo + TTS)
│        (Cost: cheap, motion limited to micro-expressions)
│        Max duration: 4-6 sec per generation
│
└─ NO → Is shot primarily action/transition (2+ positions)?
   ├─ YES → Seedance 2.0 (2 keyframes + motion)
   │        (Cost: medium, motion quality high)
   │        Max duration: 8-10 sec
   │        Use when: walk, turn, hand motion, camera move
   │
   └─ NO → Is shot establishing B-roll / no characters?
      ├─ YES → Veo 3.1 or Kling 3.0 (text-to-video)
      │        (Cost: high, quality leader)
      │        Use: landscapes, product reveals, complex scenes
      │        Max duration: 8-12 sec
      │
      └─ NO → Is shot simple motion (camera pan, zoom)?
         └─ Seedance Fast tier (minimal reference)
```

### Scoring Heuristic (Production Teams Use)

| Criterion | Points | Tool Impact |
|-----------|--------|------------|
| Character talking head visible | +5 | → Avatar IV |
| Multiple distinct keyframes needed | +4 | → Seedance |
| Establishing/hero shot | +3 | → Veo 3.1 / Kling 3.0 |
| Heavy occlusion/depth required | +3 | → Veo 3.1 (better occlusion) |
| Simple motion, no character detail | +2 | → Seedance Fast |
| TTS lip-sync mandatory | +5 | → Avatar IV or Seedance native audio |
| Duration > 8 sec | -2 | (splits into multiple shots or Premium tier) |
| Budget critical | +3 | → Seedance Fast |
| Quality/creative hero | -2 | (upgrade to premium tier) |

---

## 4. Anti-Patterns: What Traditional Storyboards Get Wrong for AI

### Pattern 1: Overspecified Depth
**Bad**: "Over-the-shoulder shot of CEO overlooking skyline"
- AI occlusion struggles: shoulder shape → warping, topology breaks
**Better**: "Medium shot, CEO centered. Blurred building backdrop (shallow DoF)."
- AI excels at single depth layer with blur; avoids occlusion zone

### Pattern 2: Match Cuts Across Generators
**Bad**: "Cut on motion: character walks left off-frame, enters next scene from right"
- Different generators produce incompatible motion curves
**Better**: "Shot ends with character exiting frame. Next shot: static wide establishing."
- Breaks dependency; each generator independent

### Pattern 3: Whip Pans & Fast Motion
**Bad**: "Fast whip pan across room"
- AI motion artifacts spike with angular velocity > 20°/sec
**Better**: "Smooth dolly-in, 0.3x speed multiplier"
- Constrain motion vectors; let AI interpolate smoothly

### Pattern 4: Complex Multi-Object Occlusion
**Bad**: "Wide shot: 3 people interacting, camera weaving between them"
- Topology errors multiply; faces warp on proximity
**Better**: "Three separate medium shots: close-up A, close-up B, two-shot AB (frontal)"
- Route each composition to cleaner generator path

### Pattern 5: No Lighting Continuity Spec
**Bad**: "Scene transitions from day to night"
- Color shift causes character/object jitter between shots
**Better**: Explicit lighting seed + color temperature in each shot: "Match 3200K tungsten from shot 02"

### Pattern 6: Vague Emotional State
**Bad**: "Character looks surprised"
- Different seeds produce different face shapes; no guarantee of consistency
**Better**: "Reference: char_main_surprised_001.jpg (specific frame lock)"

---

## 5. The Workflow Deliverable: Storyboard → Engineering Handoff

### Step 1: Human-Readable Reference Storyboard (for approval)
A Google Doc or Figma board with:
- Scene number, duration, dialogue
- Static reference frame (image model output, locked)
- Prose camera/audio description
- Shot routing decision (e.g., "Seedance 2.0 — keyframe motion")

**Used for**: Creative review, client sign-off, script sync

### Step 2: JSON Shot Card Batch File
One JSONL file per scene (line-delimited JSON), containing the schema from **Section 2** above.

**Used for**: API submission, orchestration, consistency tracking

### Example delivery:
```
scene_03_shotcards.jsonl

{"shot_id":"03_01_talking_head","scene_num":3,"duration_target_sec":4.5,"visual_spec":{...},"audio_spec":{...},...}
{"shot_id":"03_02_action_walk","scene_num":3,"duration_target_sec":6,"visual_spec":{...},...}
{"shot_id":"03_03_wide_establishing","scene_num":3,"duration_target_sec":5,"visual_spec":{...},...}
```

### Step 3: Orchestration Manifest
A control JSON that sequences shots, handles frame carryforward, and routes batches:

```json
{
  "project_id": "campaign_Q2_2026",
  "scenes": [
    {
      "scene_id": "03",
      "shots": [
        {"shot_ref": "03_01_talking_head", "output_path": "renders/03_01.mp4"},
        {"shot_ref": "03_02_action_walk", "output_path": "renders/03_02.mp4"},
        {"shot_ref": "03_03_wide_establishing", "output_path": "renders/03_03.mp4"}
      ],
      "stitch_order": ["03_01", "03_02", "03_03"],
      "consistency_seed_carry": 8847
    }
  ],
  "post_render": {
    "overlay_captions": true,
    "add_music": "track_id_007",
    "output_formats": ["mp4_9_16_tiktok", "mp4_9_16_reels"]
  }
}
```

---

## 6. Practitioner Workflow Summary

**Current teams shipping 50+ videos/month use this cadence:**

1. **Script → Human storyboard** (2-4 hours): Scene breakdown, dialogue timing, shot list
2. **Reference frame generation** (1 hour): Fast image model (Nano Banana, FLUX) per shot—cheap, quick
3. **Shot card JSON assembly** (2-3 hours): Engineering team fills template with routing decisions, tool selection, audio specs
4. **Batch video generation** (2-4 hours, parallel): All shots submitted via orchestration manifest to respective APIs
5. **Render assembly + post** (1-2 hours): Stitching, caption overlays, platform export
6. **QA / consistency check** (1-2 hours): Frame-to-frame continuity, audio sync, artifact detection

**Total time**: 8-16 hours for 5 shots (~30-60 sec video)  
**Cost per finished 10-sec clip**: ~$1.50 (vs. $5 if using one premium generator for all shots)

---

## 7. Key Insights from 2026 Practitioners

1. **Storyboard is a spec document, not a communication tool.** Its job is eliminating ambiguity, not impressing creatives.

2. **Reference frames lock composition.** Once the static frame is generated and approved, the video model treats it as a constraint—not a suggestion.

3. **Audio routing is load-bearing.** Seedance native TTS is fast but less controllable; external TTS + Avatar IV is slower but gives fine-grained control. Decision must be made at storyboard time.

4. **Duration targets must respect generator ceilings.** Seedance caps at 15 sec; Veo at 12 sec. Shots > 8 sec should split or upgrade to premium tier.

5. **Multi-shot sequences need consistency seeds.** A fixed seed value carried across shots prevents character/lighting drift.

6. **Occlusion is the enemy.** Avoid layered depth. Simpler compositions reduce re-generation cost by 60-70%.

---

## Sources & Tools

**Practitioners:**
- [2026 AI Video Production Playbook (Medium)](https://medium.com/@paoloperrone/the-2026-ai-video-production-playbook-bc683d5b85da)
- [JSON Prompting Deep Dive (Medium)](https://medium.com/@ai.in.motion.blog/video-generation-with-json-prompting-my-deep-dive-into-structured-creativity-e89b4b82c1b8)
- [Creative AI Studio Google Docs Template (Medium)](https://creativeaistudio.medium.com/how-to-create-an-ai-storyboard-for-your-next-ai-video-using-google-docs-genius-prompts-74078b5f03f0)

**Platforms & Schemas:**
- [Video Notation Schema (GitHub)](https://github.com/context-notation/video-notation-schema) — structured JSON for cinematic control
- [Novi AI (Multi-scene editor)](https://www.noviai.ai/)
- [LTX Studio (Short-form workflow)](https://ltx.studio/blog/short-form-video)
- [HeyGen Community Guide (Seedance prompting)](https://community.heygen.com/public/resources/seedance-avatar-shots-prompting-guide-get-the-best-results-in-heygen)

**API & Orchestration:**
- [JSON2Video (REST API for video spec)](https://json2video.com/)
- [Atlas Cloud State of AI Video APIs (2026)](https://www.atlascloud.ai/blog/case-studies/the-state-of-ai-video-apis-in-2026-from-text-to-video-to-cinematic-directing)

