# Visual review rubric (what the scripts cannot measure)

Status per item: PASS · ISSUE · NA · NOT_INSPECTABLE. Missing evidence (face too small, moment not in any frame) is NOT_INSPECTABLE, never a pass [A05.L04 article]. Rules come from Bible v2 via `higgsfield-production-qc/references/guide.md`; V5 is an Auto-Affi project rule.

| ID | Check | Look at | Fail looks like | Source |
|---|---|---|---|---|
| V1 | Identity matches the locked sheet / Element in every shot and across cuts (face, hair, build, wardrobe) | ref_compare, cut_pairs | face drift, wardrobe taken from the prompt instead of the sheet | [A04.L06 t=00:30] [A02.L18 t=01:05-01:30] |
| V2 | Product truth: shape, colour, logo and every rendered string equal the approved copy | bursts on product moments, last frame | smudged label, wrong word ("DROWNED" for "Hollow") | [A08.L08 frames t=00:25] [A08.L08 frames t=00:40] |
| V3 | Hands and anatomy | bursts on hand actions, set-downs | twisting fingers, geometry breaking on set-down, extra limbs | [A05.L07 t=01:30] [A05.L04 t=00:41] |
| V4 | No unrequested details or text | contact sheets | added marks, merged objects, stray captions/watermarks | [A04.L09 t=00:40-00:50] [A05.L06 t=02:38] |
| V5 | Thai no-lipsync: no visibly speaking Thai mouth; Thai lines are VO | bursts inside VO windows | mouth flapping to Thai audio | project rule (creative-lead) |
| V6 | Physics and contact persist | bursts, consecutive tiles | debris vanishing between frames, lens warp only on edges | [A05.L06 t=01:40] [A05.L03 t=00:56] |
| V7 | Continuity across cuts: match-cut pose, screen sides, light | cut_pairs | pose reset, character switches screen side | [A16.L04 t=00:24] [A01.L09 t=02:31-02:50] |
| V8 | Each prompt beat happens in its time window | contact sheets + T07 offsets | beat missing, order swapped, cut far from the planned second | [A15.L03 t=01:39] |
| V9 | Rapid cuts are not hiding motion the model could not animate | cut_pairs + count | a cut exactly at every hard moment | [A05.L02 t=01:29] |
| V10 | Legible at delivery size (faces, text, crowds) | full frames at real size | soft/smudgy faces at 720p, morphing text | [A05.L11 t=00:07] [A02.L10 t=00:22-00:30] |

Motion quality (speed, weight, camera smoothness) cannot be proven from stills: mark it NOT_INSPECTABLE unless bursts settle it, and say a human must watch at normal speed.

## Issue note format [A05.L03 article]
`take / timecode / observation / expectation / severity (blocker|major|minor) / hypothesis / one fix / retest`

## Verdict
- **KEEP** — no ISSUE in T01–T07 or V1–V10 that touches the deliverable; record keeper range(s) per beat [A15.L03 t=01:39].
- **REROLL** — one-off defect after the brief clearly works; same prompt, new take [A16.L04 t=01:23].
- **FIX-BRIEF** — the same failure repeats across takes (4/4 fail = prompt, not seed) or the defect is caused by the prompt/reference; change ONE variable [A16.L02 t=01:32].
- **REJECT** — physics-broken or off-brief beyond repair; stop and report [A02.L10 article].
