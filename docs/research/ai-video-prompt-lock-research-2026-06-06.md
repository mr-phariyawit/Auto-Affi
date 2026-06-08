# AI Video Prompt Lock Research

Date: 2026-06-06

Purpose: build a company-grade prompt system for high-scene-count AI video where character identity, location geography, product truth, and camera language survive across many scenes.

## Primary Lessons

1. Prompting must be treated as a production contract, not a creative paragraph.
   - Every scene needs a global identity block, location block, camera block, action block, product truth block, and negative block.
   - The local scene prompt should never re-invent the world.

2. Character consistency needs a character passport.
   - Stable identity fields: age range, body scale, hair, face shape, skin tone, wardrobe, accessories, hand details, movement habit, emotional range.
   - Variable fields: expression, micro-action, hand position, gaze, distance from camera.
   - Forbidden drift: new wardrobe, new face age, new hair, extra people, talking-mouth when using VO.

3. Location consistency needs a map, not just a room description.
   - Define room topology, wall/window orientation, table/drawer/window relationships, light sources, prop positions, wet/dry zones, and camera access points.
   - Each scene references location slots by ID instead of writing a fresh room description.

4. Camera consistency needs a camera grammar.
   - Use named camera positions and shot types: macro insert, over-shoulder, locked wide, table top-down, side profile, match-cut, low hero, reflection shot.
   - Define allowed lenses/movement per act so the film has visual authorship.

5. Long-scene workflows need continuity tokens.
   - A token combines `world_id`, `character_id`, `wardrobe_id`, `location_id`, `camera_slot_id`, `time_state`, `prop_state`, and `product_state`.
   - Prompts should include those tokens in every scene so a reviewer can machine-check drift.

6. Reference systems beat prose alone.
   - Where provider supports it, use approved reference images/keyframes for character, room, product, and hero shot.
   - For this Auto-Affi workflow, any generated image/reference/keyframe must remain Nano Banana Pro only, and any visual video remains Seedance 2.0 only.

## Company Rule

The company should create a reusable `Prompt Continuity Bible` before every multi-scene AI video run:

- `character_passports`
- `location_map`
- `prop_product_state_machine`
- `camera_atlas`
- `scene_contracts`
- `negative_prompt_registry`
- `continuity_token_schema`
- `qa_acceptance_matrix`

No scene prompt is allowed to go to provider unless it imports these locks.

## Sources

- Runway official Gen-4 prompting and reference workflow guidance: https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide
- Google Vertex AI Veo/video prompt guide on prompt components and camera language: https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide
- OpenAI Sora help center on storyboard-style video generation workflows: https://help.openai.com/en/articles/9957612-generating-videos-on-sora
- StoryDiffusion research on long-range consistency via consistent attention: https://arxiv.org/abs/2405.01434
