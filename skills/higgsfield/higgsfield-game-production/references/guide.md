# Focused guide

## Source lookup

Relevant Bible IDs: `A14 B9 C7`. Choose the needed IDs; do not load the entire list by default.

Use the shared helper at `../higgsfield-bible-director/scripts/bible_lookup.py` with repeated `--section ID`, or inspect `../higgsfield-bible-director/references/bible-snapshot.md`. These paths are relative to the skill root; resolve before calling. The helper is local and read-only. Shared contract: `../higgsfield-bible-director/references/operating-contract.md`.

## Operating notes

GDD output: player/audience, core loop, controls/input, states, win/loss, mechanics differences, levels, art/audio direction and tests. Build mechanics with placeholders before spending on nonessential art.

For sail/cannon/boarding, test aim/contact/damage and state transitions. For a shooter, distinguish each weapon's observable behavior and destruction. For hand tracking, test velocity/collision plus lost tracking and restart. Actual webcam access is an execution step, not granted by source text.

Deliverable stages: design proposed; code built; local game played; deployed URL verified; marketplace published. Do not collapse them into DONE. Media generation is not evidence the game logic works.

Metrics: total players, concurrent players, remix and return rate need explicit windows/denominators. Record all failed takes and integration labor. Hosting/ownership promises and course cost totals are not current terms. Game trailer-only tasks route to cinematic direction.
