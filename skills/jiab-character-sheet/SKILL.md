---
name: jiab-character-sheet
description: "Use when building, extending or locking the JIAB (Jiab / JIAP host) character sheet or reference pack on Higgsfield GPT Image 2.5 Sunburst: retouching a real photo of Jiab into the approved idealized JIAB look, continuing the R-series (R23, R24…), making a new angle (front, three-quarter, profile, full body) from an approved hero, adding an outfit or state sheet, building the review board or ref pack for video, or deciding whether the sheet is locked. Triggers also on รีทัช, แต่งรูป, ทำให้หล่อ, ลบริ้วรอย, ใต้ตาคล้ำ, character sheet, ชีท, ref pack, ทำมุมใหม่, ชุดที่ 2. Not for Soul-ID training sets or for generating the video itself."
---

# JIAB character sheet

One pipeline from a real photo of Jiab to a locked, model-ready JIAB reference pack. Retouching is stage 1 of it, not a separate job. The standard behind every stage is [docs/reference/character-sheet-professional-ai-film.md](../../docs/reference/character-sheet-professional-ai-film.md); this skill is the executable version of it for JIAB.

The look is fixed: read [references/style-spec.md](references/style-spec.md) once per session. The operator's veto zone is **under the eyes**: any line, bag or darkness is an instant fail.

## Where are we? Start at the first stage that is not done

| Stage | Output | Done when | Current state (update this row when it changes) |
|---|---|---|---|
| 1 Hero front | front retouch, passes 1–3 | operator approves | **v12 hero approved 2026-10-08** ("ผ่าน ทำ v12 เลย"): AI Influencer gen4 → GPT Image hair-fix → under-eye edit, built from the R15 black-blazer board `cast-library/jiab/identity-ref/JIAB-CHARACTER-REFERENCE-board-R15.png`. R14 BANNED + archived (memory `feedback_identity_ref_sheet_not_r14`) |
| 2 Angles from hero | 34L, profileR, fullbody | operator approves each | **v12 angles approved 2026-10-08**: R30 34L + R31 profileR (from v12 front hero + model-study style targets), each followed by a pass-3 under-eye fix (100% QC flagged creases). fullbody = right half of the hero image |
| 3 Ref pack + review board | `cast-library/jiab/v<N>/` | originals downloaded, pack + board + sheet.json written | **v12 complete 2026-10-08**: front, 34L, profileR, fullbody (all originals) + sheet.json (status PENDING: lock rule TODO) + `v12/review/JIAB-v12-board.jpg`. Note: front/fullbody white bg, 34L/profileR light-grey |
| 4 States | one pack per outfit/state | operator approves | not started |
| 5 Motion test | one 5 s clip per state | face, hair, outfit stable | **v12 DEFAULT PASS 2026-10-09** (operator "approve"): Kling 2.6 i2v 5 s from 34L, 55 kie cr, `runs/2026-10-09-jiab-v12-motion-test/`. Under-eye bunches at a full toothy smile; prompt "small smile" was ignored, so ask for "closed-lip smile" next time |
| 6 Lock | `status: LOCKED` in sheet.json | `lock_status()` says LOCKED | **v12 DEFAULT LOCKED 2026-10-09**. Rule (make_ref_pack.py, from the professional-sheet guide stage B/E §7): operator approval + 3-5 refs + front, a three-quarter and a profile + all originals + every short side ≥1024 px + motion test PASS |

Every stage that generates spends credits, so every generation goes through the **gate** below.

## Stage 1 — hero front (retouch recipe)

All passes: **GPT Image 2.5 Sunburst**, image-edit, 3:4, High, 2K, count 1. UI price was 2.75 credits per image; re-read the Generate button each run. Prompts are verbatim in [references/prompts.md](references/prompts.md).

1. **Pass 1, style transfer.** IMAGE 1 = real photo (eyes toward the lens), IMAGE 2 = style target of the same angle. Sets light, hair, face shape, expression, outfit.
2. **Pass 2, beautify** (ref = pass-1 result). Wrinkles zero, dewy glow, rosy lips, eyes a touch more open.
3. **Pass 3, under-eye only** (ref = pass-2 result). Always run it on a stage-1 hero. (Stage 2 angles get it only when QC fails.)
4. **Optional pass 4**, one system only, with the "Keep EVERYTHING … change ONLY" frame.

One system per pass, because a single long prompt saturates (R7 → R8). Face width and age are set by pass 1 and by the identity photo; a late pass cannot change face geometry (R19). If the face is too wide or old, redo pass 1.

Inputs: webcam frames by angle in `output/character-reference/jiab-soul-id/real-capture-take2-frames/upload-ready/`, real refs in `cast-library/jiap/identity/real-refs/`, style targets `output/character-reference/jiab-soul-id/model-study/EXAMPLE-target-{front,34,profile}-oct2.png`, other style-bible files in `cast-library/jiab/style-bible-2026-10-06/README.md`. Upscale anything under 300 px on the short side ×3 with PIL first.

## Stage 2 — every other angle comes from the approved hero

Use the prompt "Angle from an approved hero" (three-quarter and profile variants in prompts.md). The two references are the **approved hero** (identity) and a **style image of the target angle** (angle, pose, framing, light only). Never start a new angle from a webcam frame: R16–R20 (four passes) kept the real face width and the look-away gaze, while R21 and R22 each passed in one generation from R14.

Default views are front, 34L, profileR and fullbody (four refs, leaving one slot under the five-ref limit). Add 34R, profileL or hairtop only when a campaign shotlist needs them. Identity ref for every angle is the stage-1 front hero (R14). For fullbody, use a taller aspect if the UI offers one (UNTESTED), and check identity on a face crop. Run pass 2 or 3 on an angle only when its QC fails.

## Stage 3 — ref pack and review board are two different things

| | Ref pack (for models) | Review board (for the operator) |
|---|---|---|
| Content | 1–5 single images, one face each, no text, light-grey background | the same images in a labelled grid |
| Source | downloaded **originals** (needs the operator's `โหลด`) | originals or screencrops |
| Made by | `scripts/make_ref_pack.py` | `scripts/compare_board.py --cols 3` |
| Goes to | Kling / Veo / Seedance / Nano Banana Pro refs | the operator's eyes only, never a model |

```bash
python3 skills/jiab-character-sheet/scripts/make_ref_pack.py --version v11 \
  --approved-by "operator 2026-10-07: ผ่าน R14/R21/R22" \
  "front=PATH_R14" "34L=PATH_R21" "profileR=PATH_R22"
python3 skills/jiab-character-sheet/scripts/compare_board.py \
  cast-library/jiab/v11/review/JIAB-v11-board.jpg --cols 3 --height 900 \
  "FRONT R14=..." "3/4 L R21=..." "PROFILE R R22=..."
```

Layout: `cast-library/jiab/v<N>/CHAR_JIAB_v<N>[_<STATE>]_<view>.<ext>` plus `CHAR_JIAB_v<N>[_<STATE>].sheet.json` and `review/`. The v11 pack (R14 hero) was archived on 2026-10-08; the next pack is **v12**, built from the black-blazer character-reference board. States are added into the same `v<N>` folder. Replacing an already approved image means a new `v<N+1>` folder and the affected shots in `--affects`. Element tags: `@jiab` for the default outfit, `@jiab_<state>` (for example `@jiab_outfit2`) for each state, so the video prompt names which outfit to use.

## Stage 4 — states and outfits are edits of approved images

One pack per state (`--state OUTFIT2`, `--state STAGE`). Make each by image-edit of the **already approved** image of the same angle, using the "Outfit / state edit" prompt (IMAGE 1 = approved angle, IMAGE 2 = style-bible outfit image). Outfit edits tend to soften or change the face, so re-run identity and under-eye QC; if the face drifted, repair it with a pass-3 style "change ONLY" edit instead of regenerating.

## Stage 5 — motion test before lock

One 5-second clip per state in the tool the campaign will use (Kling 2.6 i2v via kie.ai is the project default; Seedance takes Soul ID through @Elements), with the ref pack as references. Check that the face does not stretch, the hair keeps its shape and the outfit does not change. Fail → back to stage 2 or 4. Record the result with `--motion-test PASS|FAIL`.

## Gate before every generation

Show the operator the reference thumbnails with their roles, the full prompt, settings and cost, then wait for `เจน` / `go`. Skip the wait only when the operator approved the whole batch in advance, and write that in the run log.

## Running on Higgsfield

Use Claude in Chrome ("cic"); steps and traps are in [references/higgsfield-ui.md](references/higgsfield-ui.md). The two that cause most failures: reference order follows **selection order** in the picker, so zoom on the thumbnails and match the IMAGE roles in the prompt; and long prompts time out while typing but still land, so verify the text before Generate.

## QC after every generation

Show the image inline, then build a strip against its inputs:

```bash
python3 skills/jiab-character-sheet/scripts/compare_board.py OUT.jpg "HERO=..." "STYLE=..." "R23=..."
python3 skills/jiab-character-sheet/scripts/compare_board.py OUT-eyes.jpg --crop 0.22,0.27,0.78,0.40 "R14=..." "R23=..."
```

Log each item PASS / FAIL / NOT_INSPECTABLE:
1. Under-eye: zero lines, bags, darkness (veto item).
2. Wrinkles gone, skin still reads as real.
3. Dewy glow yes, oily hotspots no.
4. Eyes fully open with catchlights; brows thick and dark.
5. Hair medium-long voluminous waves swept up.
6. High-key light grey, soft, no vignette, no hard rim.
7. Identity vs the approved hero (and the real photo for stage 1): nose, lips, mustache, goatee, moles.
8. Over-retouch: glowing eye whites, edge halos, perfect symmetry.
9. Angle: matches the target view (profile = true 90°, ear visible; three-quarter ≈ 30°, eyes to camera).

A viewer screencrop is not the original: 100%-zoom checks are NOT_INSPECTABLE until the original is downloaded.

## Logging and reporting

Runs are numbered after the highest in `output/character-reference/jiab-soul-id/retouch-refs/`; list the folder first (it was R22 on 2026-10-07). Save screencrops there as `CHAR_JIAB_v<N>_<view>_R<N>_<pass>_SCREENCROP.png` and downloaded originals without the suffix. Write `run-R<N>-<view>-<pass>.json` there too: run, date_local, trigger (the operator's words), model, settings, cost_ui, refs with verified order, full prompt, result (size, created time, screencrop/board paths, original_downloaded), qc, operator_verdict (`pending` until the operator says otherwise). Save the full prompt every time; R11/R12 texts were lost.

Everything is PRODUCED until the operator gives a verdict. End each turn with the stage table position, e.g. "stage 2: fullbody produced, waiting for verdict".

## Boundaries

- Soul-ID training sets come only from the original style-bible images, never from retouched or generated images (operator ruling 2026-10-06).
- A review board, or anything with text on it, is never a model reference.
- On a rejection, write the operator's exact words, change one variable next run, and add durable lessons to `docs/reference/pro-retouch-and-grooming-for-studio-portraits.md` §12.
