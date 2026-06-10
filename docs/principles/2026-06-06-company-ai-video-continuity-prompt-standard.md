# Company AI Video Continuity Prompt Standard

Date: 2026-06-06

This standard exists because ordinary shot prompts are not enough for commercial-grade AI video. A company that wants repeatable film quality must build the world first, then generate scenes from that world.

## Non-Negotiable

For any campaign with more than three generated scenes, production must create these assets before provider generation:

1. `creative_council.json`
2. `character_passports.json`
3. `location_map.json`
4. `camera_atlas.json`
5. `prop_product_state_machine.json`
6. `scene_prompt_contracts.json`
7. `continuity_qc_matrix.json`

## Prompt Contract Shape

Each scene prompt must be composed from fixed blocks:

```text
GLOBAL_LOCK:
  world_id, film_title, creative_platform, realism mode, aspect ratio, product truth

CHARACTER_LOCK:
  character_id, age range, face/hair/body/wardrobe/hand anchors, forbidden drift

LOCATION_LOCK:
  location_id, map coordinates, light source, wall/window/table relation, wet/dry state

CAMERA_LOCK:
  camera_slot_id, lens feel, framing, movement, focus behavior, allowed cut purpose

SCENE_ACTION:
  one action only, start state, motion, end state

PRODUCT_LOCK:
  product shape/material/state, exact use behavior, forbidden claims

NEGATIVE_LOCK:
  no text, no logo hallucination, no location jump, no new character, no magical repair

QC_ACCEPTANCE:
  visible pass/fail criteria
```

## Continuity Token

Every scene gets a compact token:

```text
WORLD=W01 | CHAR=C01 | WARD=W01A | LOC=L01-Z03 | CAM=CAM-MACRO-INSIDE-01 | TIME=NIGHT-RAIN | PROP=P03-CUT | PRODUCT=PATCH-UNAPPLIED
```

If any token changes, the prompt must explain why.

## Camera Atlas Requirement

The camera atlas must include every recurring camera family:

- macro insert
- extreme macro product texture
- table top-down
- over-shoulder
- eye-line POV
- locked wide room release
- match-cut before/after
- side profile hand action
- low hero product frame
- reflection or glass layer frame

Each camera family defines allowed location slots, lens feel, motion, emotional use, and forbidden uses.

## Location Map Requirement

The location map must describe the environment as a small set, not an abstract apartment:

- floorplan zones
- object coordinates
- camera access points
- lighting direction
- outside weather
- wet/dry rules
- where the product can be used
- where props can be stored
- forbidden jumps

## Creative Council Expansion

For premium commercial work, the creative council must include:

- Executive Creative Director
- Film Director
- Director of Photography
- Production Designer
- Prompt Continuity Architect
- Character Continuity Lead
- Location Map Supervisor
- Camera Grammar Lead
- Product Truth / Claims
- Editor
- Performance Marketing
- Thai Copy / VO Lead

The prompt continuity architect can block provider generation.

## Provider Policy

For Auto-Affi current policy:

- Visual video: Seedance 2.0 only.
- Generated reference/keyframe/storyboard imagery: Nano Banana Pro only.
- No public publish without affiliate URL, live price/SKU, rights/disclosure, AI label, and human approval.
