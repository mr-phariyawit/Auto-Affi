---
name: higgsfield-dailies-review
description: "Review generated video takes like dailies with real evidence: measure duration/aspect/resolution/audio/black gaps/freezes/cuts-vs-prompt with ffmpeg, extract contact sheets, cut pairs, bursts and reference-vs-frame comparisons, inspect them against a cited rubric (identity, product label truth, hands, stray text, Thai no-lipsync, continuity), then record KEEP / REROLL / FIX-BRIEF / REJECT with keeper ranges in the run ledger. Use whenever a Higgsfield/Seedance/Veo/Kling clip comes back, someone asks 'ตรวจคลิปนี้', 'QC วิดีโอ', 'take ไหนใช้ได้', 'ควร reroll ไหม', or before a clip goes into an edit or gets posted."
---

# Dailies Review (evidence-based QC for generated video)

A generated clip is PRODUCED, not verified, until someone has measured it and looked at it. This skill makes both steps cheap and leaves evidence a teammate can re-check. Rules: [references/rubric.md](references/rubric.md) (cited from Bible v2 via `higgsfield-production-qc`).

## 1. Measure

```bash
python3 <skill>/scripts/probe_checks.py take.mp4 --job job.json --prompt prompt.txt --out RUN/review/take1.report.json
```
`job.json` is the same file the prompt was linted against (add `"audio_expected": true` when the clip should carry audio). Checks: T01 duration · T02 aspect · T03 resolution · T04 audio · T05 black gaps · T06 freezes ≥1 s · T07 cuts vs the prompt's SHOT/CUT plan (or "one continuous take"). Exit 1 = at least one ISSUE.

## 2. Extract what must be seen

```bash
python3 <skill>/scripts/review_frames.py take.mp4 --out RUN/review/take1 --report RUN/review/take1.report.json \
  --ref <locked face/product reference> [--ref ...] [--burst <t of a hand action / label / VO line> ...]
```
Gives contact sheets (1 tile/s, `index.tsv` maps tile → second), a before|after image for every detected cut, first/last frame, 5-frame bursts and reference|frame pairs. Choose the references from the run's approved sheets (single face image + product packshot), not a multi-panel board.

## 3. Look — every image

Open each file listed in `manifest.json` with the Read tool and fill V1–V10 from the rubric. Show the user the images that carry a finding (memory rule: always display the actual image). Be specific: timecode, what you see, what was expected. Anything no frame shows → NOT_INSPECTABLE; motion quality needs a human watching at normal speed.

## 4. Decide and record

Verdict per take: KEEP / REROLL / FIX-BRIEF / REJECT (definitions in the rubric; 4/4 failing takes means the prompt is wrong, not the seed). Then:
```bash
python3 <skill>/scripts/record_review.py --run RUN --label "shot01 take1" --verdict REROLL \
  --issues "V2 label smudged 5.0-6.0s; V3 thumb merges 3.2s" --keep "0.0-4.8s" --report RUN/review/take1.report.json
```
Then feed the recipe ledger: KEEP → `recipes.py promote`; a failure whose cause you understand → `recipes.py fail` (skill `higgsfield-recipe-ledger`). The entry lands in `RUN/ledger.jsonl` next to the spend lines from `gate_cli`, so cost per kept take can be computed later. REROLL needs a new preflight (budget) but not a new approval; FIX-BRIEF changes the prompt, so it goes back through `higgsfield-seedance-prompt` lint and the gate's re-audit + human approval.

## 5. Report

`T01–T07` table, `V1–V10` table with image paths, verdict + keeper ranges, NOT_INSPECTABLE list, and the one variable to change if FIX-BRIEF. Never upgrade "the script passed" to "the clip is good": T-checks say nothing about faces, labels or acting.
