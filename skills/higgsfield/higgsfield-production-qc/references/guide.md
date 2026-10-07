# Focused guide

## Source lookup

Relevant Bible IDs: `A05 A08 B7 B10 C1.3 C2.3 D6 E1 E2 E3 E4 E5`. Choose the needed IDs; do not load the entire list by default.

Use the shared helper at `../higgsfield-bible-director/scripts/bible_lookup.py` with repeated `--section ID`, or inspect `../higgsfield-bible-director/references/bible-snapshot.md`. These paths are relative to the skill root; resolve before calling. The helper is local and read-only. Shared contract: `../higgsfield-bible-director/references/operating-contract.md`.

## Operating notes

Verify current tools and plugin names before doing setup. The task of learning from a course is not authorization to install the course's integrations. Rubrics, scales and new prompts here are authored synthesis, not vendor benchmarks; reusable templates live in the director's assets dir. Blockers (wrong SKU, unsupported claim, wrong label/mechanism/CTA, unplayable file) are never averaged away; delivery QC opens the actual exported file, and structural packet checks cannot stand in for missing visual or audio evidence.
- Review a showcase for what it proves, not for how it impresses: one replay = one evidence question, replace adjectives with findable evidence, note as `I saw ___, so I would ___.` [A05.L01 article]
- Mark each check PASS / ISSUE / NA / NOT_INSPECTABLE; missing evidence (face too small) is "inconclusive", never a verdict, and a positive JSON field stays declared-only until reviewed. [A05.L04 article]
- Issue notes must let a teammate verify or dispute them: one claim per element, `artifact+version / timecode / observation / expectation / severity / hypothesis / one fix / retest`. [A05.L03 article]
- Decision record = `Capability / Constraint / Context / Verdict`; judge at real delivery size and record motion and resolution separately, never one score; "it looks better" gives the team nothing. [A05.L11 article]
- Rapid cuts at hard moments = the model hiding motion it cannot animate; one cut proves little, a repeated pattern matters; ask whether a move is shown or only implied by the edit. [A05.L02 t=01:29] [A05.L02 article]
- Tells: real lens distortion follows depth (hands warp first) while a filter only bends edges; debris must persist, nothing "deleted" between frames; UGC phone shakes before set-down and pans from the wrist. [A05.L03 t=00:56] [A05.L06 t=01:40] [A05.L07 t=00:52]
- Use screens and reflections as a consistency checksum, check near/mid/far layer scale instead of counting objects, and check eyeline, light and reaction separately to locate the failing layer. [A05.L08 article] [A05.L09 article]
- Face/ad failure modes: screaming is where AI faces break; a stack of small seams (stiff face, lip-sync drift, fingers twisting, geometry breaking on set-down) is "the difference between an ad and an AI ad". [A05.L04 t=00:41] [A05.L07 t=01:30]
- Video-only: A05 compares Seedance 2.5 vs 2.0 on one prompt across 6 categories; as recorded in the course 2.5 = 30 s at 720p and 2.0 = 15 s at 4K, and the 15 s cap caused most 2.0 failures. [A05.L01 t=00:27] [A05.L02 t=01:38] [A05.L11 t=00:15] [A05.L07 t=01:27]
- 720p faces go soft/smudgy on a TV or in a wide shot even if a phone hides it; specs change, so check the current interface before promising a delivery format. [A05.L11 t=00:07] [A05.L11 article]
- Require 4K (as taught) when flares, fog, crowds, busy wides or on-screen text must read; lower resolution smears or morphs them, and crowds are checked in the gaps between people. [A02.L10 t=00:22-00:30] [A08.L01 t=01:56] [A08.L02 t=00:00]
- Judge realism by layer (skin, water, background) with hard subjects, and by skin texture (pores, grain, imperfection); "perfect AI skin" reads uncanny. [A08.L01 t=03:08] [A08.L06 t=01:06]
- VFX on real plates: at 1080p the model "almost always changed small details", so review ORIGINAL vs GENERATED side by side; fast depth shots are judged on 3D space, not 2D motion. [A08.L03 t=01:31] [A08.L03 t=01:18] [A08.L08 t=00:12]
- Export: stress CGI with fast camera + particles and inspect banding in smoke, reds and fog; 10-bit only pays off when exported at High bitrate. [A08.L05 t=00:30] [A08.L05 t=00:57] [A08.L05 article]
- Read every rendered string against approved copy: a HUD came out "THE DROWNED CARDINAL" instead of "The Hollow Cardinal". [A08.L08 frames t=00:25] [A08.L08 frames t=00:40]
- Observed model behavior: it adds unrequested details (lipstick mark, a merged "cyborg cat"), relights to the text over the keyframe, and takes wardrobe from the prompt not the sheet, so check outputs against the locked sheet. [A04.L09 t=00:40-00:50] [A05.L06 t=02:38] [A04.L06 t=00:30] [A02.L18 t=01:05-01:30]
- Take triage: generate 4; if 4/4 fail the prompt is wrong, not the seed; change one variable at a time and keep what works. [A16.L02 t=01:32] [A01.L05 t=00:02-00:05] [A06.L05 t=01:08]
- Name the defect level before rewrite vs reroll ("almost right" is not a diagnosis); discard physics-broken takes, and reroll before touching locks when the brief works. [A16.L04 article] [A02.L10 article] [A16.L04 t=01:23]
- On repeated heavy failure simplify: multi-shot to one continuous shot, split dense scenes, cut shots that add nothing. [A01.L08 t=01:35-01:48] [A10.L07 t=02:31] [A02.L12 t=01:08-01:13]
- Keepers are selected per beat (take ID, in/out, purpose), mined across batches like dailies, and judged in sequence: a visually successful generation can still fail the film. [A15.L03 t=01:39] [A01.L05 t=03:05] [A15.L11 t=00:16]
- Prompt Bank data caveat: sample clips are not proof a prompt works; PB.05 mismatches its clip, PB.11 and PB.27 are byte-identical, PB.17 is titled "Crush" but says "crash zoom OUT"; course pages also omit requirements (A13 Premiere Pro and credits, A05 being a 2.5 vs 2.0 comparison). [PB.05] [PB.11] [PB.27] [PB.17] [CP.A13] [CP.A05]
- Cost review = total spend incl. failed takes / approved deliverables, currencies never mixed; the courses give no whole-piece credit totals, only remarks like "400 generations". [A01.L03 t=00:00-00:17] [A02.L04 t=01:02]

## Known contradictions

- E1: aspect ratio differs between speech, chips and cue/Recreate (A02 16:9 vs 21:9; A08 L02 the reverse), so check the real chip before generating or delivering. [A02.L06 t=01:09-01:18] [A08.L02 t=00:00] [A08.L02 frames t=00:07]
- E1: A08 L04/L05 cues are swapped versus the videos; trust the on-screen panel when citing them. [A08.L04 frames t=01:30] [A08.L05 frames t=00:21]
- E2: A15 wrap-up claims no credit prices, but frames show a GENERATE button 832 struck to 704 as recorded in the course; v2 follows the frames. [A15.L09 frames t=00:32] [A15.L02 frames t=02:00]
- E3: A08 headlines 4K yet most Recreate links are 1080p with no visible 4K selector, and A05's 2.5 at 720p may be pre-release only. [A08.L01 cue cue-l1-kaiju] [A08.L01 frames t=02:46] [A05.L11 article]
- E3: cues are not always the final prompt and a reference image can beat the text (RED durag rendered YELLOW; cel-shaded request rendered paper-cutout). [A01.L03 cue 3-view-character-sheet-recreate] [A04.L03 cue scene1-animated] [A04.L10 t=00:50-01:10]
- E3: "I touch nothing" / "If it passes, send it" conflicts with the article's approval gate; QC stays a gate. [A07.L07 t=02:40] [A07.L09 t=00:28] [A07.L09 article]
- E4: some results never appear in sampled tiles (NOT_INSPECTABLE), and editing, stitching and scoring are never shown. [A13.L03 t=00:08] [A15.L05 t=02:24] [A02.L08 t=01:43-01:46]
- E4: transcripts contain whisper hallucinations that must not be quoted as dialogue, and business results are unvalidated. [A10.L01 t=01:54] [A16.L03 t=03:40] [A07.L12 t=00:58] [A12.L07 t=00:05]
- E5: A05 article says "older woman" but the sheet shows an old man with a dog; A06 credit counter is an animation (use >=6,725 as recorded) and 56 generations vs "100 tries". [A05.L10 article] [A06.L16 frames t=01:04] [A06.L16 t=01:30]
