# AI Video Prompt Lock Research V5.1 Addendum

Date: 2026-06-06

Purpose: upgrade Auto-Affi from good-looking isolated shot prompts to a repeatable commercial production system where the same character, location, product state, and camera grammar survive across dozens or hundreds of scenes.

## What Changes

V5.1 treats each generated shot as an output of a locked world model, not as a standalone prompt. The company must maintain four layers before any provider call:

1. World lock: campaign title, product truth, realism mode, room geography, time/light states.
2. Identity lock: character passport, hand anchors, wardrobe, emotional range, and forbidden drift.
3. Map lock: location zones, camera access points, prop coordinates, wet/dry rules, and product-use zones.
4. Shot lock: camera slot, one physical action, start state, end state, motion language, and QC acceptance.

For a 100-scene workflow, the local scene prompt should not re-describe the world from scratch. It should import the locked IDs, describe only the scene-specific action, and record why any token changes.

## Source Lessons Applied

- Google image-generation guidance favors narrative scene descriptions over disconnected keyword lists, with camera angle, lens, lighting, and details for realistic photography. This supports using Nano Banana Pro keyframes as full scene descriptions, not keyword piles.
- Google also frames commercial/product images as explicit product photography prompts and sequential storytelling as consistency-driven panels. This supports using keyframes/storyboard references before motion.
- Runway's video prompt guidance is useful even when Seedance is the required video model: once an input image exists, the prompt should mainly describe motion rather than restating every visual detail. It also recommends direct physical actions over abstract concepts and one scene per short clip.
- Google video prompt guidance lists camera angles, movement, lens, and rack focus vocabulary. This supports a camera atlas instead of ad hoc camera phrasing.
- Sora's storyboard workflow reinforces timestamped cards and pacing between cards. This supports the V5.1 timeline/card structure before paid motion generation.

## Production Rule

Use two prompt modes:

- Nano Banana Pro keyframe/reference prompt: rich scene paragraph with character, map zone, camera, light, product state, and visual composition.
- Seedance 2.0 motion prompt: direct, physical motion and camera behavior. If a keyframe reference exists, do not re-invent the visual identity; let the reference image carry identity and use the text for motion.

## Lock Formula

Every scene must compile into this structure:

```text
SCENE_ID:
  continuity_token
  imported_world_lock
  imported_character_lock
  imported_location_zone
  imported_camera_slot
  product_state_start
  product_state_end
  one_scene_action
  motion_prompt
  negative_registry
  qc_acceptance
```

The Prompt Continuity Architect can block provider generation when any scene lacks a continuity token, map zone, camera slot, product state, or visible QC acceptance.

## Sources

- Google Gemini API image-generation prompt guide: https://ai.google.dev/gemini-api/docs/image-generation
- Google Vertex AI video-generation prompt guide: https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide
- Runway Gen-4 video prompting guide: https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide
- OpenAI Sora storyboard help: https://help.openai.com/en/articles/9957612-generating-videos-on-sora
- StoryDiffusion consistency research: https://arxiv.org/abs/2405.01434
