---
name: higgsfield-seedance-prompt
description: "Write and lint Seedance (Higgsfield) video prompts the way the Higgsfield Academy courses do: pick the taught skeleton, fill it from a shot brief with @tag references, then run a deterministic linter that checks tags vs attached Elements, model duration/resolution limits, timecodes, shot/cut counts, match cuts, audio, hex colours and prompt-vs-job settings. Use whenever someone asks for a Seedance / Higgsfield video prompt, a shot prompt from a storyboard or shotlist, a prompt review or fix before spending credits, or 'เขียน prompt Seedance', 'ตรวจ prompt ก่อน gen', even if they don't say 'lint'."
---

# Seedance Prompt Compiler + Linter

Turns a shot brief into a course-structured Seedance prompt and proves it is structurally consistent before anyone spends credits. Rules come from the audited Bible v2; every rule carries the course citation that taught it.

## 1. Pin the job first

Write `job.json` beside the prompt (example: [assets/job.example.json](assets/job.example.json)). The prompt is checked against it, so get it from the brief or the live UI, never by guessing:
`model` (seedance-2.0 / seedance-2.5), `duration_s`, `aspect`, `resolution`, `references` (the exact Higgsfield Element names, e.g. `@jiab`), `audio_reference` (true if a music/voice track is attached).

Limits are as recorded in the courses — see [references/model-limits.md](references/model-limits.md). If the brief asks for something outside them (20 s on 2.0, 1080p on 2.5), say so instead of writing around it.

## 2. Pick one skeleton

Read [references/skeletons.md](references/skeletons.md) and choose by deliverable:
S1 structured cinematic (multi-cut story shot) · S2 standalone 15 s ad with shared style prefix · S3 shotlist `CUT n — lens` with Global Style Prefix · S4 continuous take / action in metres and seconds.
Several prompts in one project share one STYLE PREFIX; label a deliberate per-scene change `STYLE PREFIX (override)`.

## 3. Write the prompt

Apply [references/rules.md](references/rules.md). The ones that most often break generations:
- Declare every reference once in ACTIVE REFERENCES with its scope ("appearance only", "NOT inherited"); use the identical tag everywhere. A tag the job doesn't attach is a hallucination magnet.
- Refer to people by their @tag, not he/she. Briefs rarely state gender, and a pronoun that contradicts the reference image invites identity drift.
- Describe states positively. Seedance can read "not crying" as "crying"; exclusion lists in CAMERA/STYLE blocks are fine.
- Numbers over adjectives: metres, degrees, seconds, "3x faster". Each CUT gets shot size + lens mm or FOV°.
- Timed segments start at 0, touch each other and end exactly at `duration_s`. "Exactly N shots and N-1 cuts" must match the blocks you wrote.
- Match cuts say the end pose EXACTLY matches the next start, otherwise the model treats the cut as a new scene.
- AUDIO block always. Default "No music. Environmental SFX only. No subtitles." unless a track is attached.
- **Auto-Affi Thai ads:** no visibly speaking Thai mouth — dialogue is VO over B-roll (creative-lead rule, project constraint not from the courses). Write VO lines for the audio pipeline, not on-camera quotes.

## 4. Lint, fix, repeat

```bash
python3 <skill>/scripts/lint_prompt.py shot01.txt [shot02.txt ...] --job job.json
```
Fix every ERROR. For each WARN either fix it or state why it is intentional (e.g. the shot really needs a negated physical constraint). Re-run until 0 errors. Several files at once also checks style-prefix drift (R22).

## 5. Report honestly

Return: the prompt(s), the job settings, the lint result line (`PASS (0 errors, N warnings)`) with any accepted warnings explained, and open questions (missing references, unknown Element names). A lint PASS is structural only — it is not a generated or reviewed video. Live prices, menus and model availability must be read from the current UI before spending; the course figures are dated. Hand generation to the execution adapter in `../higgsfield-bible-director/references/routing.md` and review results with `higgsfield-production-qc`.
