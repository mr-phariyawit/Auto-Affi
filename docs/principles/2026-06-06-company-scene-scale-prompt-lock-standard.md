# Company Scene-Scale Prompt Lock Standard

Date: 2026-06-06

This standard answers one production question: if the company creates 10, 50, or 100 generated scenes, how do we keep the same character, same room, same product truth, and same camera authorship?

## Standard

No generated video scene is provider-ready unless it imports a locked production bible:

- Character passport
- Location map
- Product state machine
- Camera atlas
- Negative continuity registry
- Scene contract
- Dailies QC contract

## Prompt Layers

1. Global lock: aspect ratio, model locks, realism mode, claim policy, campaign tone.
2. Character lock: stable physical anchors, wardrobe, hand details, expression range, forbidden drift.
3. Location lock: zone ID, map relationship, light state, wet/dry state, allowed product behavior.
4. Camera lock: shot family, lens feel, focus behavior, movement, emotional purpose, forbidden use.
5. Product lock: state before action, state after action, material, scale, truth boundary.
6. Scene action: one visible action only.
7. Motion lock: subject motion, camera motion, scene motion, style descriptor.
8. QC lock: what a reviewer must see to keep the generated clip.

## Continuity Token

Every provider draft must include one compact token:

```text
WORLD=W01 | CHAR=C01_HAND_ONLY | WARD=WARD_C01_HOME_MINIMAL | LOC=L01-Z01 | CAM=CAM05_HERO_PRESS_MACRO | TIME=MORNING_CLOUDY | PRODUCT=P06_PATCH_PRESSED
```

If the token changes, the scene contract must explain why. Unexplained token drift blocks generation.

## Camera Coverage

The camera atlas must register all recurring camera families before production:

- Establishing wide
- Locked master
- Macro insert
- Extreme macro
- Top-down product ritual
- Side-profile hand action
- Over-shoulder
- Point of view
- Eye-line rack focus
- Match cut
- Static proof frame
- Slow push-in
- Dolly or truck move
- Pan or tilt
- Handheld search
- Product beauty frame
- Reflection or glass-layer frame
- Final room release

Unused camera slots can remain inactive, but unregistered camera language should not appear in a provider prompt.

## Team Authority

The Creative Strike Team has taste authority, but the Prompt Continuity Architect, Location Map Supervisor, Camera Grammar Lead, and Product Truth / Claims seat have hard veto power. A beautiful shot that changes the room, actor, repair truth, or product behavior is killed.

## Provider Rule

For the current Auto-Affi policy:

- Generated image, reference, keyframe, and storyboard assets: Nano Banana Pro only.
- Visual video: Seedance 2.0 only.
- No paid provider call unless the relevant gate records approval and credit-spend acknowledgement.
