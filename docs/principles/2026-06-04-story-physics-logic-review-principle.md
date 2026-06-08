# Auto-Affi Story Physics and Logic Review Principle

Date: 2026-06-04

Purpose: add a dedicated pre-generation review team that checks whether storyboards obey the intended reality mode, physical behavior, cause/effect logic, and marketing intent before Seedance video generation.

## Research Basis

- Storyboard and shot-list practice separates visual flow, framing, movement, lenses, and lighting before production so teams can align before shooting or rendering.
- Animation fundamentals such as staging, timing, spacing, anticipation, arcs, follow-through, and overlapping action are used to make motion readable and physically believable.
- Current AI storyboard research also emphasizes continuity planning across characters, backgrounds, locations, and shot transitions before video generation.

Reference links:

- StudioBinder storyboard/shot-list tutorials: https://www.studiobinder.com/tutorials/visualize/
- SIGGRAPH animation principles summary: https://education.siggraph.org/static/HyperGraph/animation/character_animation/principles/prin_trad_anim.htm
- University of Washington animation principles lecture notes: https://courses.cs.washington.edu/courses/cse557/17au/assets/lectures/animation-principles-4pp.pdf
- CANVAS continuity-aware storyboard research: https://arxiv.org/abs/2604.13452

## Core Rule

> The storyboard must define the laws of its world before a video model renders motion.

A normal commercial must obey normal physics. A fantasy commercial may break physics only when Marketing explicitly asks for fantasy and the storyboard defines the fantasy rule.

## Required Artifact

Every multi-shot AI video run must include:

```text
story_physics_review.json
location_environment_design.json
```

The provider call is blocked unless this review is `pass_for_generation` or `pass_with_publish_block`.

## Reality Mode

Marketing must declare one mode:

```text
realistic
stylized
fantasy
surreal
```

### `realistic`

Use for normal product reviews, affiliate clips, practical demos, and believable commercials.

Rules:

- Gravity, weight, balance, friction, water behavior, hand motion, and object scale must feel normal.
- Product use must be physically plausible.
- The designed location must support the action: reachable surfaces, plausible walking paths, realistic wet/dry zones, and believable light/weather conditions.
- Camera movement must be possible or at least visually motivated.
- No floating, teleporting, instant transformations, impossible water behavior, or unsupported product effects.

### `stylized`

Use for expressive edits, heightened product beauty, exaggerated camera motion, or playful timing.

Rules:

- Physics may be polished or compressed, but cause/effect still needs to read.
- Exaggeration must improve clarity, not hide product drift.

### `fantasy`

Use only when Marketing explicitly wants magic, surreal product behavior, or impossible movement.

Rules:

- The fantasy rule must be written down.
- The rule must stay consistent across shots.
- The fantasy must serve the hook, brand memory, or story payoff.
- The storyboard must separate intentional fantasy from accidental model failure.

### `surreal`

Use for concept films or art-led campaign ideas.

Rules:

- Logic can be dreamlike, but visual continuity and viewer comprehension still matter.
- Product truth, claims, rights, and disclosure gates still apply for commercial work.

## Review Team

Add this council seat before generation:

```text
Story Physics and Logic Review
```

Owns:

- reality mode and marketing intent alignment;
- gravity, weight, balance, friction, water, and object scale;
- cause/effect between shots;
- action continuity and screen direction;
- camera motivation and spatial logic;
- location/environment realism, wetness state, lighting motivation, and transition plausibility;
- product-use plausibility;
- fantasy-rule consistency when fantasy is requested.

## Required Review Fields

```text
run_id
variant_id
reality_mode
marketing_intent
fantasy_rule
storyboard_grid_path
shot_cards_path
location_environment_design_path
review_scope
physics_checks
logic_checks
marketing_override
required_revisions
decision
reviewer
reviewed_at
```

## Physics Checks

For each storyboard cell or shot:

```text
gravity
weight
balance
friction_or_contact
water_or_fluid_behavior
object_scale
hand_or_body_mechanics
camera_physicality
continuity_of_motion
```

## Logic Checks

For each storyboard cell or shot:

```text
cause_and_effect
before_after_state
screen_direction
spatial_relationship
location_environment_plausibility
product_role_logic
claim_implication
transition_logic
viewer_comprehension
```

## Marketing Override

Marketing can approve physics-breaking ideas only by writing:

```text
marketing_override: true
reality_mode: fantasy
fantasy_rule: ...
business_reason: ...
non_negotiable_limits: ...
```

Examples:

- Allowed fantasy: "The red umbrella floats because the campaign concept is a magical guide; it always moves like a gentle compass and never teleports."
- Not allowed by default: "A normal waterproof phone pouch levitates, makes rain stop, or guarantees the phone cannot break."

## Decision Values

```text
pass_for_generation
pass_with_publish_block
revise
block
```

## Hard Gates

- No normal product demo can break normal gravity without Marketing's declared fantasy mode.
- No fantasy shot can proceed without a written fantasy rule.
- No impossible product function can imply a commercial claim unless the claim ledger supports it.
- No shot may ask Seedance to solve unclear blocking, object contact, or cause/effect.
- No long-batch generation when storyboard logic is `revise` or `block`.

## Fast Checklist

For normal affiliate/product stories:

```text
Does the object fall, hang, bend, splash, slide, and stop like it has weight?
Does the actor's hand/body action make sense?
Does water behave like water?
Does the location make the action possible?
Do wet/dry states, light, surfaces, and transitions match the approved environment design?
Does the product solve only the allowed problem?
Does each shot follow logically from the prior shot?
Can the viewer understand the scene without captions?
```

For fantasy stories:

```text
What law is being broken?
Why is it broken?
Is the broken law consistent?
Does it serve Marketing's hook?
Does it avoid false product claims?
```
