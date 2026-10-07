# Focused guide

## Source lookup

Relevant Bible IDs: `A01 A02 A04 A06 A10 A15 A16 B5 B6 B7 D6 D8`. Choose the needed IDs; do not load the entire list by default.

Use the shared helper at `../higgsfield-bible-director/scripts/bible_lookup.py` with repeated `--section ID`, or inspect `../higgsfield-bible-director/references/bible-snapshot.md`. These paths are relative to the skill root; resolve before calling. The helper is local and read-only. Shared contract: `../higgsfield-bible-director/references/operating-contract.md`.

## Operating notes

Read the mode you need: A02 drama/performance; A04 animation; A06 realistic product commercial; A10 action ad; A15 vehicle blocking; A16 fight. A01 is the common assets-to-scenes film pipeline.

Prompt structure: PURPOSE; REFERENCE ROLES; START STATE; visible ACTION sequence; CAMERA path/framing/time; LIGHT/material; AUDIO; END STATE; ACCEPTANCE. Avoid naming a technique without its start/end and narrative job.

Drama: performance onset/peak/release, pauses, eyelines and reverse angles. Create VO separately if image is already a keeper and audio is the issue. Animated worlds: maintain prop identity and actual style grammar such as screentone or clay response.

Vehicles: seat positions, interior angle references, landmarks, wheel geometry, lane/curb and door exit. Validate the ending backward when it determines blocking. Fights: numeric scale and path, contact, recovery, material consequences, and staged foreground/mid/background.

The A16 short instructions shown in the source are requests for a prompt builder, not downloaded expanded generation prompts. All new prompts are authored synthesis and should be labeled accordingly. Settings or voices in the examples are not guaranteed current capabilities.

Deliver only the requested scope. A small prompt revision should list the preserved locks and change, not re-create script/assets.
