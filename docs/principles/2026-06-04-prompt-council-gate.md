# Auto-Affi Prompt Council Gate

Date: 2026-06-04


## Core Rule

> Every prompt must pass a multi-team council before generation. The team or agent that drafts a prompt cannot self-approve it. If the prompt is not dense enough, the council returns `revise` or `block`, never `pass`.

## Required Council Seats

Each prompt review must include at least these independent seats:

| Seat | Owns |
| --- | --- |
| Marketing Council | buyer archetype, hook, positioning, conversion action, offer clarity |
| Product Research and Claims Council | product truth, evidence, price/SKU, identity anchors, prohibited claims |
| Shooting Production Council | shot contract, actor action, blocking, camera, lighting, continuity |
| Location and Environment Design Council | realistic world design, location map, wet/dry state, lighting/weather, transition plausibility, product-use zones |
| Story Audit Council | narrative logic, buyer tension, product necessity, beat order, viewer comprehension, and marketing memory image |
| Continuity and Storyboard Audit Council | adjacent-shot identity, wardrobe, prop, bag, product, location/environment, and screen-direction continuity |
| Story Physics and Logic Council | reality mode, gravity, weight, water, object scale, cause/effect, fantasy-rule consistency |
| Post, Rights, and Compliance Council | cleanroom audio, captions, Thai text, rights, disclosure, AI label, publish blocks |

Optional seats for premium/client work:

- Cinematography/Lighting Council
- Editor/Sound Council
- Growth/Analytics Council
- Legal/Business Affairs Council
- Client/Brand Council

## Non-Self-Approval

Rules:

- `draft_owner` may propose or revise the prompt, but cannot vote `pass`.
- At least three independent council seats must vote `pass` before generation.
- Product Research and Post/Compliance are mandatory pass seats for any commercial prompt.
- Location and Environment Design is a mandatory pass seat for any realistic multi-shot AI video prompt.
- Story Audit is a mandatory pass seat for any multi-shot AI video prompt.
- Continuity and Storyboard Audit is a mandatory pass seat for any multi-shot AI video prompt.
- Story Physics and Logic is a mandatory pass seat for any multi-shot AI video prompt.
- Any `block` vote from Product Research, Compliance, or Rights blocks generation.
- Any `block` vote from Story Physics and Logic blocks generation until the storyboard or marketing reality mode is revised.
- Any unresolved dissent must be recorded in `dissent_log`.
- Automation may mark `prompt_review_ready`, but only the council can mark `generation_ready`.

## Prompt Density Minimum

Every prompt gets a `density_score` from 0 to 100.

Minimums:

- 85 for affiliate/social review clips.
- 90 for premium brand commercials.
- 95 for client/paid production or regulated categories.

Density is not length. Density means the prompt contains the right constraints:

- human truth and buyer pressure;
- first 0-3s hook;
- product role in story;
- shot-by-shot or scene-by-scene action;
- product identity anchors and "must not become" list;
- allowed claim IDs and blocked visual implications;
- approved location/environment design and realistic transition map;
- approved story audit: buyer tension, product necessity, beat order, viewer comprehension without captions, and final memory image;
- camera, lighting, blocking, continuity, safe caption zones;
- declared reality mode and story-physics logic: normal physics for realistic work, written fantasy rule for fantasy work;
- voice-over visual policy: no visible speaking mouth unless the project deliberately uses a talking-head/lip-sync route;
- no generated Thai text inside Seedance/video frames; intentional generated static text-image assets must route to `nano_banana_2` / Nano Banana Pro and pass OCR/spelling/claim review;
- source audio disabled or cleanroom fallback;
- expected outputs and fallback route.

## Decision Values

```text
pass_for_generation
pass_with_publish_block
revise
block
```

Use `pass_with_publish_block` only when the prompt is safe to generate but publish still needs affiliate URL, price/SKU recheck, disclosure, AI label, or human/client approval.

## Mandatory Review Fields

```text
run_id
variant_id
prompt_pack_id
stage
draft_owner
provider
model
params
research_refs
product_truth_refs
claim_ledger_refs
rights_tracker_refs
buyer_archetype_th
human_truth_th
positioning_sentence
0_3s_hook
product_role_in_story
identity_anchors
must_not_become
shot_contract
negative_prompt
claim_map
blocked_claim_scan
caption_safe_zones
vo_visual_policy
thai_text_policy
audio_policy
disclosure_plan
fallback_rule
location_environment_design_path
story_audit_path
continuity_audit_path
story_physics_review_path
density_score
council_votes
dissent_log
required_revisions
final_decision
```

## Pass/Fail Rules

Pass only if:

- the product changes the story outcome;
- the first 0-3s has visible human tension or a thumb-stop image;
- product turn appears early enough for the format;
- every claim maps to the claim ledger;
- product identity anchors are explicit;
- prompt states what the product must not become;
- the storyboard has passed Story Audit and can be understood before captions are added;
- each shot has one clear actor action and a motivated camera move;
- location/environment design makes the character action possible before the character acts;
- adjacent shots preserve declared wardrobe, prop, product, bag, location, environment, lighting, and weather anchors unless a visible change beat is written;
- the storyboard has passed story physics and logic review;
- realistic stories obey normal gravity, object weight, water behavior, body mechanics, and cause/effect;
- fantasy stories include a written fantasy rule and Marketing rationale;
- lighting keeps product surfaces readable;
- voice-over concepts use B-roll, hands, product action, over-shoulder, profile, or closed-mouth reactions rather than a character visibly moving their mouth as if speaking;
- Thai captions/price/CTA on the final video timeline are planned for deterministic post-composition; model-generated static text images are allowed only through Nano Banana Pro and review gates;
- source audio is disabled or there is a documented strip-and-replace fallback;
- publish blockers are recorded separately from generation readiness.

Revise or block if:

- the prompt is only a mood/vibe paragraph;
- product can be removed and the story still works;
- prompt asks Seedance/video models for fake labels, fake badges, fake Thai text, or unsupported claims;
- prompt implies deep water, guaranteed safety, medical/safety guarantees, or "works with every phone";
- voice-over prompt asks for visible lip movement, talking-to-camera, or mouth-as-if-speaking without an explicit talking-head/lip-sync route, consent, and sync QA;
- multiple scenes/actions compete in one shot;
- the story can still work after removing the product, the problem/reveal/proof/resolution order is unclear, or the storyboard needs captions to explain basic cause/effect;
- normal product demos break gravity, water, object scale, or product-use logic without an approved fantasy mode;
- fantasy motion is inconsistent or creates unsupported product claims;
- density score is below threshold;
- the drafting team is also trying to approve its own prompt.

## Required Artifact

Every run must include:

```text
prompt_council_review.json
story_audit.json
story_physics_review.json
```

Recommended prompt pack naming:

```text
prompt_packs/visual.v002.council-reviewed.prompt-pack.jsonl
prompt_packs/voice.v002.council-reviewed.prompt-pack.jsonl
```

The generation job may not start unless `story_audit.decision`, `story_physics_review.decision`, and `prompt_council_review.final_decision` are all `pass_for_generation` or `pass_with_publish_block`.
