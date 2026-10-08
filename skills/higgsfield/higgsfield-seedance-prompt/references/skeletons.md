# Seedance prompt skeletons taught in the courses

Pick ONE skeleton per job. Citations point into Bible v2 (`../higgsfield-bible-director/references/bible-snapshot.md`).
Read the cited section with `bible_lookup.py --section A01.05` (lesson) when you need the original wording.

| Skeleton | Use when | Source |
|---|---|---|
| S1 Structured cinematic | multi-cut story shots with locked assets (film, ad scene) | A01 L05 skill output |
| S2 Standalone 15 s ad | every prompt must work alone, shared style prefix, timed SHOT list | A10 `seedance-prompt-structure` |
| S3 Shotlist CUT n — lens | ad/product sequence written as a shot list with a Global Style Prefix | A06 |
| S4 Continuous take / action | one-take, fights, scale, transformation; coordinates in metres, motion in seconds | A16 skill |

## S1 — Structured cinematic (14 sections, in this order) [A01.L05 cue recreate-1b]

```
SCENE CONTEXT: <story beat this shot serves>
ACTIVE REFERENCES:
@tag — <what it controls> only; <what is NOT inherited>.
LOCATION MAP: <who/what is where; screen sides>
FIRST FRAME / BLOCKING: <exact opening composition>
FORMAT MODE: Sequence of cuts, no timecodes   |   Timed multishot
OPTICS: CUT n — <shot size>, <FOV°>            (or per-segment LENS LOCK: 29°)
CAMERA: <rig + one move, numbers>
ACTION: <beats in order>
PERFORMANCE: <visible/audible acting signals>
PHYSICS: <weight, contact, materials>
LIGHTING: <sources + direction>
AUDIO: <SFX / dialogue / "No music">
STYLE: <grade, texture>
POSITIVE LOCKS: Exactly N named characters … ; named locks (HEADCOUNT / HANDS / STAGE LOCK)
```
- Timed form: `0.0s to 5.5s — LENS LOCK: 29° …` [A01.L07 cue recreate-2-1c]
- Named locks: [A01.L07 cue recreate-2-1c] [A01.L06 cue recreate-1-4b] [A01.L07 cue recreate-2-1d]
- A08 Kaiju prompt uses the same family (STYLE … TECHNICAL / AUDIO / SCENE CONTEXT / FORMAT MODE / OPTICS / ACTION / POSITIVE LOCKS) [A08.L01 cue cue-l1-kaiju]

## S2 — Standalone 15 s ad (A10) [A10.L01 frames t=00:35] [A10.L04 cue cue-scene-2]

```
<STYLE PREFIX — identical in every prompt of the project>
Style: … / Lighting: … / Color: 60:30:10 … / Camera: 180° shutter … / Skin: … / Acting: … /
Physics: … / Continuity: … / Technical: 24fps / Audio: Environmental SFX only. No music. No subtitles.

SUBJECT: @tag matches input 100%; start state → end state.
LOCATION: @location is a STYLE REFERENCE ONLY, not a fixed keyframe.
MULTISHOT / ACTION:
SHOT 1 (0:00–0:03): … Hard cut.
SHOT 2 (0:03–0:07): … Hard cut.
CAMERA: …
STYLE: 60:30:10 …
CONSTRAINTS: …
```
- Skill chip name `seedance-prompt-structure` [A10.L03 frames t=01:02]
- Two-block variant `[VISUAL] … [AUDIO] "NO MUSIC. SFX ONLY"` [A10.L02 cue cue-location-test]

## S3 — Shotlist with Global Style Prefix (A06) [A06.L10 frames t=02:00] [A06.L10 frames t=01:45]

```
STYLE PREFIX: Style / Lighting / Color (60:30:10) / Camera (180° shutter) / Skin / Acting / Physics /
Composition / Continuity ("No identity drift") / Technical (24fps) /
Audio ("Diegetic dialogue and environmental SFX only. No music. No subtitles.")
CHARACTERS: @tag — wardrobe …
SCENE: @location + blocking + props
CUT 1 — <shot size>, <lens mm>, <angle/move>: <action beat>
CUT 2 — …
```
- Scene override with audio input and locked schematic [A06.L13 frames t=04:35]
- Product cut: `CUT n — [shot name], [take length], [FOV], [mount]: [rig behaviour] + [@product framing]` [A06.L12 frames t=04:05]

## S4 — Continuous take / action (A16) [A16.L01 t=01:29] [A16.L01 frames t=01:35]

Four parts: asset anchors (tags), coordinates in metres, motion in seconds, hard anti-hallucination rules.
Order: subject motion → camera motion → environment → acting → optics → lighting → audio.
```
ACTIVE REFERENCES:
@hero [image1] — Character appearance only.
@prop [image2] — Element reference only.
STYLE PREFIX: Sky: … Fog: … Physics: … Continuity: … Weather: … Acting: …
CAMERA: ONE CONTINUOUS TAKE, NO CUTS, NO EDITS. <start/end distance + height in metres>
ACTION (2 SHOTs, frame-perfect match cut, 15s total):
SHOT 1 (0.0–5.0s): … end pose …
SHOT 2 (5.0–15.0s): start pose EXACTLY matches the end of SHOT 1 …
```
- Blocks: [A16.L02 frames t=00:40] [A16.L02 frames t=00:50] [A16.L02 frames t=01:05] [A16.L04 frames t=00:26]
- ACTIVE REFERENCES required; OUTPUT SETTINGS only when asked or the UI cannot set it [A16.L01 frames t=01:30] [A16.L01 frames t=01:40]

## Related — A15 car commercial [A15.L03 article] [A15.L03 frames t=01:35]
`— REFERENCE DEFINITIONS — → — TECHNICAL BLOCK — → — PROMPT — → SFX list`; references defined once, shots use tags only.
Do not copy the A15 L08 official prompt as a template: it is truncated by an evidence gap [A15.L08 article].
