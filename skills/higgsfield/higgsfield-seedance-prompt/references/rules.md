# Prompt rules (Bible v2)

`scripts/lint_prompt.py` checks the rows marked **lint**. The rest need your judgement while writing.
All citations exist verbatim in Bible v2. Prices, menus and limits are as recorded in the courses, not current.

## Checked by the linter

| ID | Rule | Sev | Citation |
|---|---|---|---|
| M00–M02 | Model, resolution and aspect must be in the recorded limits table (see model-limits.md) | error/warn | [A05.L02 t=01:41] [A01.L05 frames t=00:05] |
| R00 | References in use need an ACTIVE REFERENCES / REFERENCE DEFINITIONS / CHARACTERS block | error | [A16.L01 frames t=01:30] [A15.L03 article] |
| R01 | Every @tag: declared, attached to the job under the identical Element name, and used; no stale or invented tags | error/warn | [A16.L01 frames t=01:30] [A16.L01 frames t=01:40] [A01.L03 t=05:10-05:26] [A10.L04 t=00:06–00:36] |
| R03 | Each reference states its scope ("appearance only", "controls water and sky only", "NOT inherited") | warn | [A01.L05 cue recreate-1b] [A01.L05 cue recreate-1-2a] [A15.L03 article] [A15.L10 frames t=03:05] |
| R06 | Describe states/emotions positively ("dry eyes, steady breath", not "not crying"); camera/style exclusion lists are fine | warn | [A02.L07 t=00:33-00:48] [A16.L02 t=03:19] [A16.L05 t=00:57] [PB.38] |
| R08 | Duration ≤ recorded model max (2.0 = 15 s, 2.5 = 30 s) | error | [A05.L02 t=01:41] [A05.L02 t=01:38] [A04.L03 t=02:33] |
| R09 | Timed segments start at 0, are contiguous, end at the job duration | error/warn | [A16.L04 frames t=00:26] [A01.L09 frames t=02:55] [A10.L04 cue cue-scene-2] |
| R10 | "Exactly N shots and N-1 cuts" must match the SHOT/CUT blocks | error | [A15.L03 article] [A15.L09 t=01:18] [A15.L05 frames t=00:45] |
| R11 | "no timecodes" format mode contains no timecodes | warn | [A01.L05 cue recreate-1b] [A01.L07 cue recreate-2-1c] |
| R12 | Each CUT line: shot size + lens mm or FOV° | warn | [A06.L10 frames t=01:45] [A01.L05 cue recreate-1b] [A10.L05 cue cue-scene-3] |
| R14 | Numbers, not speed words ("3x faster", metres, degrees, seconds) | warn | [A16.L02 t=01:04] [A16.L03 t=02:44] [A02.L14 t=00:26-00:36] [PB.36] |
| R18 | Match cut: end pose of shot N EXACTLY matches the start of shot N+1 | error | [A16.L04 t=00:24] [A16.L04 t=00:35] [A06.L14 t=00:53] |
| R19 | Dialogue verbatim in quotes tied to a speaker tag; AUDIO says "No subtitles" | warn | [A03.L06 cue lizards-climbing] [A08.L04 frames t=01:30] [A16.L02 frames t=01:22] |
| R20 | Dialogue scenes add lip-sync / eyeline lines | warn | [A15.L06 article] |
| R21 | AUDIO block present; default "No music, environmental SFX only" unless a music track is attached | warn | [A10.L04 t=01:26–01:46] [A06.L13 t=04:05] [A08.L04 cue cue-l4-fungal] |
| R22 | One shared style prefix across a project's prompts; per-scene changes labelled "override" | warn | [A06.L10 t=02:02] [A06.L12 t=02:15] [A06.L12 t=02:38] [A10.L01 frames t=00:35] |
| R24 | Exact colours as valid hex (AI-written hex gets mistyped: #D1EF17 for #d1fe17) | warn | [A01.L03 t=04:12-04:41] [A09.L03 t=01:59–02:04] [A09.L03 cue c3j] |
| R27 | "Exactly N named characters…" instead of "No extra people" | warn | [A16.L01 frames t=01:30] [A01.L07 cue recreate-2-1c] |
| R30 | Aspect/duration written in the prompt must equal the job settings; OUTPUT SETTINGS only when asked | error | [A16.L01 frames t=01:40] [A09.L08 frames t=00:40] [A09.L06 cue c6a] |

## Judgement rules (apply while writing)

| Rule | Citation |
|---|---|
| Define each reference once; shots use the tag only | [A15.L03 article] |
| A location reference is a style reference, not a keyframe ("Do not reproduce the reference 1:1") | [A10.L01 frames t=00:35] [A10.L04 cue cue-scene-2] |
| Don't repeat a banned concept word — the model gives what you name | [A16.L05 t=00:36] [A16.L05 t=01:00] |
| One camera move per cut, rig named first | [A15.L07 article] [PB.10] [PB.04] [PB.19] |
| Name the technique ("speed ramp during the kick"), not mood words ("more drama") | [A02.L13 article] [A05.L01 article] |
| Whip pan: duration, subjects labelled A/B, same shot size at start and end | [A02.L14 t=00:26-00:36] [A02.L14 t=01:05-01:13] |
| Big action in 0.5 s steps: start, path, state change, duration, end | [A16.L03 t=01:34] [A16.L03 article] [A06.L11 t=04:36] |
| Readable text/logo/HUD as exact strings, held ~2 s in close-up | [A02.L14 t=01:30-01:42] [A08.L06 cue cue-l6-skincare] |
| Palette as a 60:30:10 split or a named grade | [A02.L09 t=01:37-01:51] [A10.L01 frames t=00:35] |
| No slow motion by default; only in named beats | [A08.L07 cue cue-l7-trailer] [A04.L06 t=01:21] |
| Fix each character's screen side (180° rule) | [A01.L09 t=02:31-02:50] [A02.L08 article] [A16.L01 article] |
| Fix prompts: keep-list + change one variable ("change only X; keep everything else the same") | [A09.L02 t=00:26–00:34] [A06.L05 cue kitchen-edit-prompt] [A16.L02 article] [A15.L08 t=00:46] |
| No recorded length limit; if too much for one prompt, split into two generations | [A15.L06 t=00:00] [A10.L08 t=00:09–00:38] |

## Course contradictions to keep in mind (Bible ภาค E)

- Negatives: A02 bans them, yet A02/A16/A15 use negation; the Bible reads the warning as "don't describe states by negation", exclusion lists are fine [A02.L07 frames t=00:27-00:33] [A16.L02 frames t=01:05] [A16.L05 frames t=00:10] [PB.38]
- 16:9 vs 21:9: A02 voice/bar 16:9 but cues 21:9; A08 L02 the reverse — set aspect in the UI and keep the prompt consistent [A02.L06 t=01:09-01:18] [A08.L02 t=00:00]
- OUTPUT SETTINGS inside the prompt in A01 vs "only when asked" in A16 [A01.L08 frames t=01:24] [A16.L01 frames t=01:40]
- Reference image style beats text style ("photorealistic" came out 3D stylized) — fix the reference, not only the words [A04.L10 t=00:50-01:10]
- Cue text is not always the final prompt used on screen [A09.L07 frames t=00:47]
- "Let the model stage the camera" vs "write moves in metres/degrees" — choose per shot [A08.L04 t=01:38] [A16.L03 t=02:44]
