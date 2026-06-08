# Auto-Affi AI Video Previsualization Principle

Date: 2026-06-04


## Core Rule

> Do not ask a video model to invent the film. Build the film language first, then let the model render controlled shots.

The upgraded workflow is **skill-first, storyboard-first, model-second**.

Weak workflow:

```text
idea -> prompt -> clip -> hope continuity works
```

Upgraded workflow:

```text
idea -> treatment -> location/environment design -> character/continuity bible
-> storyboard grid -> shot contracts -> story audit -> model routing -> keyframe/motion test
-> dailies QC -> batch generation -> edit/QC -> learning
```

## What We Learned From The Umbrella Rough

The `umbrella-way-20260604-161554` run produced a usable 181s rough cut, but exposed production weaknesses:

- Character identity was acceptable for rough, but not locked enough for final close-ups.
- The red umbrella drifted toward pink/magenta in some finale shots.
- Switching models was useful for exploration, but increased look and motion-language variance; future video runs now lock to Seedance 2.0 only.
- Some models returned audio even when the creative intent was silent source video.
- A shot id ending in `_silent` collided with the post-production naming convention.
- Shot prompts were good, but the workflow needed a stronger previsual layer: character sheet, 3x3 board, continuity bible, and explicit regenerate criteria.

These are workflow mistakes, not only prompt mistakes.

## Required Artifacts

Every AI-video run that has more than one generated shot must include:

```text
character_sheet.json
continuity_bible.json
location_environment_design.json
continuity_audit.json
storyboard_grid.json
shot_cards.json
story_audit.json
story_physics_review.json
route_decision.json
prompt_council_review.json
clip_inventory.json
edit_decision_list.json
dailies_qc.json
regeneration_plan.json
metrics/failure_taxonomy.json
```

Commercial/product runs still require product truth, claim ledger, rights tracker, approval packet, and learning artifacts.

## Character Sheet Gate

Before video generation, lock the important visual anchors.

Character sheet fields:

```text
character_id
role
age_range
face_anchor
hair_anchor
wardrobe_anchor
body_language
approved_reference_assets
forbidden_variations
continuity_priority
closeup_model_policy
```

For non-human anchors, use the same structure:

```text
object_id
object_role
shape_anchor
color_anchor
surface_anchor
scale_anchor
approved_reference_assets
forbidden_variations
continuity_priority
```

Rule:

- If a close-up depends on identity, use a reference-driven route or regenerate until the anchor passes.
- If the anchor is an object motif, specify exact color drift blockers such as `deep vivid plain red, not pink, not magenta`.

## Location And Environment Design Gate

Before storyboard approval, design the realistic world where the character will move.

Required fields:

```text
world_id
reality_mode
geography_or_city_logic
weather_and_time
primary_locations
transition_map
floor_wall_ceiling_materials
lighting_sources
wetness_or_weather_state
crowd_and_traffic_density
camera_access_points
product_use_zones
forbidden_environment_jumps
```

Rules:

- A realistic commercial needs a plausible route before the character acts, for example `rainy sidewalk -> covered walkway -> cafe table -> office lobby`.
- Location changes must have a visible or logically implied transition. A character cannot jump from street rain to a luxury lobby, beach, bedroom, or unrelated cafe without the storyboard explaining how.
- Environment physics must match the scene: rain-wet exterior surfaces, indoor dry floors, consistent light direction, believable reflections, reachable bag/table/hand positions, and normal crowd/traffic behavior.
- Product proof must happen in locations where the use is plausible. A commuter can dab a towel at a sheltered walkway or cafe table; a wet macro proof should not suddenly appear in a studio lab unless the ad declares a controlled insert.
- Every generated shot prompt should include the approved location anchor or intentionally hide the background.

## Continuity And Location Audit Gate

Storyboard approval is not complete until a continuity auditor checks adjacent shots against the locked character, object, wardrobe, product, and location/environment anchors.

For every adjacent pair of shots, record:

```text
from_shot_id
to_shot_id
character_anchor
wardrobe_anchor
bag_or_prop_anchor
location_anchor
environment_anchor
lighting_weather_anchor
allowed_change
forbidden_jump
decision
```

Rules:

- A normal realistic product story may not introduce a new raincoat, jacket, uniform, bag, hairstyle, product color, or product scale between adjacent shots unless the storyboard explicitly shows the change happening.
- A normal realistic product story may not introduce a new city, room type, weather state, floor/wall material, lighting direction, crowd condition, or impossible location transition unless the storyboard explicitly designs that move.
- If scene 1 establishes a white shirt, scene 2 may not suddenly show green sleeves, a raincoat, or outerwear unless Marketing and Storyboard declare a costume-change beat.
- Hands-only and object close-ups still need wardrobe anchors: cuff color, sleeve type, hand wetness, bag color, and product color must match the previous beat or be intentionally hidden.
- Hands-only and macro inserts still need environment anchors: table material, bag position, wetness state, lighting, and background blur must match the approved location or be written as controlled inserts.
- Dailies QC must compare contact-sheet frames against this audit. A shot with an unexplained wardrobe/object/location/environment jump is `reject` or `regenerate`, never `use_with_note`.

## Storyboard Grid Gate

Use 3x3 story grids for continuity control.

For a 30s commercial:

```text
one 3x3 grid = 9 beats
```

For a 3-minute film:

```text
multiple 3x3 pages = act/sequence boards
```

Every storyboard cell must include:

```text
cell_id
time_range
story_function
CAM
MOVE
MOOD_STYLE
anchor_assets
must_keep
must_avoid
location_anchor
environment_anchor
lighting_weather_anchor
realistic_transition_from_previous
realistic_transition_to_next
model_hint
reality_mode
physics_or_fantasy_rule
```

Gate:

- No long batch generation until the current 3x3 page has passed review.
- If adjacent cells do not cut together on paper, do not expect video models to fix it.
- No storyboard proceeds to prompt council until `story_audit.json` and `story_physics_review.json` pass.

## Story Audit Gate

Before any generated video call, audit the storyboard as a story, not as a prompt list.

Create:

```text
story_audit.json
```

Required fields:

```text
run_id
variant_id
status
reviewer
storyboard_grid_path
shot_cards_path
location_environment_design_path
continuity_audit_path
story_physics_review_path
review_scope
buyer_archetype
human_tension
product_role
beat_order
story_checks
required_revisions
decision
reviewed_at
```

Story checks:

```text
buyer_archetype_alignment
human_tension_visible
product_role_is_structural
problem_to_resolution_order
one_story_function_per_beat
no_missing_or_redundant_beats
location_environment_supports_story
viewer_comprehension_without_captions
claim_implication_safety
marketing_memory_image
cta_readiness
```

Rules:

- A product ad must still work as a small story: problem, product reveal/use, proof, resolution, and memory image.
- The product must change the outcome. If the product can be removed and the viewer still understands the same story, revise.
- Every storyboard cell should own one story function and one visible action. Do not ask one shot to be hook, demo, proof, transition, and CTA at the same time.
- The approved location/environment design must make the story possible before the character acts.
- The storyboard should be understandable with captions off. Captions can sharpen conversion, but they cannot carry missing story logic.
- If Marketing intentionally wants fantasy, Story Audit must confirm the fantasy rule helps the offer instead of hiding a physics or claim problem.

Gate:

- No model routing, prompt council pass, or provider call until `story_audit.json.decision` is `pass_for_generation` or `pass_with_publish_block`.
- If Story Audit returns `revise` or `block`, revise the storyboard before writing final prompts.

## Shot Contract Upgrade

Shot prompts must be generated from shot contracts, not vibe paragraphs.

Each shot must include:

```text
shot_id
storyboard_cell_id
duration_sec
emotional_function
camera
subject_action
object_action
continuity_anchors
location_environment_anchors
negative_constraints
start_image
end_image
model
model_reason
production_pass
qc_acceptance_criteria
regenerate_triggers
story_physics_notes
```

For generated video, every shot contract must use:

```text
model: seedance_2_0
model_reason: locked_seedance_2_0_only_policy
```

`production_pass` values:

```text
exploration
rough
continuity_lock
hero_final
insert_texture
post_only
```

## Model Routing Upgrade

Generated video is Seedance 2.0 only.

Exploration rule:

- Explore different shot contracts, prompts, start images, duration splits, motion language, and edit order.
- Do not explore different video models.
- Every generated video shot still records a model reason, but it must be `locked_seedance_2_0_only_policy`.

Final rule:

- Keep the same Seedance 2.0 route for character shots, inserts, objects, weather, reflections, and hero/finale beats.
- If Seedance 2.0 struggles, simplify the shot, split the action, improve reference frames, or regenerate; do not fallback to another video model.
- Non-video utilities may still be used for voice, post, reframe, cutout, upscale, scoring, and captions.

Recommended routing:

| Shot Need | Preferred Policy |
| --- | --- |
| Character/emotional continuity | `seedance_2_0`, reference-driven |
| Key hero reveal | `seedance_2_0`, stricter anchors |
| Object insert | `seedance_2_0`, simplified action |
| Rain/reflection/texture | `seedance_2_0`, split into clean visual beats |
| Product proof | `seedance_2_0` only after approved keyframe/product truth |
| Final polish | regenerate fewer Seedance 2.0 shots with stricter anchors |

## Dailies QC Gate

After each generation batch, create:

```text
clip_inventory.json
dailies_qc.json
contact_sheet.png
regeneration_plan.json
```

QC dimensions:

```text
identity_pass
object_anchor_pass
bag_prop_silhouette_pass
strap_handle_geometry_pass
carry_position_pass
color_pass
story_function_pass
camera_motion_pass
audio_policy_pass
duration_pass
cutability_pass
rights_claim_pass
physics_logic_pass
```

Decision values:

```text
use
use_with_trim
use_as_texture
regenerate
reject
```

Gate:

- A rough cut may include amber clips for story testing.
- A final cut may not include red clips for identity, product truth, rights, audio bleed, or disclosure.
- Contact-sheet review must be numbered cell by numbered cell. A global "bag looks okay" pass is invalid when any visible bag/prop changes silhouette, strap, handle, size, color, or carry position between adjacent cells.
- If an established structured commuter bag becomes a tote, handbag, backpack, or unrelated shoulder bag, the shot is `regenerate` or `reject`, never `use`.

## Naming Rules

Shot IDs must not end with reserved processing suffixes:

```text
_silent
_raw
_final
_proxy
_approved
```

Use:

```text
s024_mother_smile
```

Do not use:

```text
s024_mother_smiles_silent
```

Post-production owns suffixes such as `_silent.mp4`.

## Failure Taxonomy

Every repeated issue must be logged in `metrics/failure_taxonomy.json`.

Required categories:

```text
identity_drift
wardrobe_continuity_jump
location_environment_jump
object_color_drift
object_shape_drift
product_truth_drift
model_audio_surprise
duration_mismatch
prompt_under_specified
storyboard_gap
story_logic_gap
product_role_gap
bag_prop_continuity_jump
model_switch_look_drift
caption_or_text_generation
naming_collision
edit_boundary_jump
rights_or_claim_block
```

Learning rule:

- If a failure repeats twice in one run, add a constraint or routing rule before generating more.
- If a route succeeds three times for the same shot type, promote it into the model scorecard.

## Hard Gates

- No multi-shot batch without `storyboard_grid.json`.
- No multi-shot batch without `story_audit.json`.
- No multi-shot batch without `story_physics_review.json`.
- No character close-up without character/object anchors.
- No storyboard/prompt council pass without `location_environment_design.json`.
- No storyboard/prompt council pass without Story Audit confirming buyer tension, product necessity, beat order, viewer comprehension, and marketing memory image.
- No storyboard/prompt council pass without adjacent-shot wardrobe/object/location/environment continuity audit.
- No final pass without `model_lock_policy: seedance_2_0_only_all_video_shots`.
- No realistic storyboard may break gravity, water behavior, body mechanics, object scale, or cause/effect without a declared Marketing fantasy mode.
- No fantasy storyboard may proceed without a written fantasy rule.
- No provider output used as source of truth until downloaded locally.
- No generated clip audio in final composition unless explicitly approved.
- No full-batch generation after a failed dailies QC without a regeneration plan.
- No final visual pass without numbered contact-sheet anchor audit for bag, prop, product, wardrobe, location, and environment anchors.
- No closeout without failure taxonomy and learning notes.
