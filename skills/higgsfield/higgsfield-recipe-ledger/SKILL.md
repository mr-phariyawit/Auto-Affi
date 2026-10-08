---
name: higgsfield-recipe-ledger
description: "Learn from our own Higgsfield runs: report credits per take and per KEEP from run ledgers, promote a KEEP take into a reusable recipe (prompt + job + manifest + cost + evidence), and record failures with their cause and next lever so they are not repeated. Use before writing a new Higgsfield/Seedance/Genjutsu prompt (check what already worked or failed), after a take is reviewed, when someone asks 'สูตรไหนเคยได้ผล', 'เสียเครดิตไปเท่าไหร่ต่อคลิปที่ใช้ได้', 'อันนี้เคยพังไหม', or wants a winning setup reused."
---

# Recipe Ledger (what worked, what it cost, what failed and why)

Store: `recipes/higgsfield/` (one folder per recipe + `failures.jsonl` + generated `INDEX.md`). Script: `scripts/recipes.py` (`R` below = `python3 <skill>/scripts/recipes.py`). Inputs are the run ledgers that `gate_cli` (spend/refund) and `higgsfield-dailies-review` (review) write into `runs/<run>/ledger.jsonl`; a take's spend and review join by an identical `--label` ("shot01 take2").

## Before writing a prompt
Read `recipes/higgsfield/INDEX.md`. Reuse a recipe for the same model/use (change only what the brief requires, e.g. swap the reference video), and check the failure table for the planned model + shot type — if a failure matches, start from its next lever instead of repeating what was tried. Say which recipe or failure you used.

## After a take is reviewed
- **KEEP** → `R promote --name <model-use-v1> --run RUN --label "<label>" --prompt RUN/<prompt> --job RUN/job.json --manifest RUN/manifest.json --tags a,b`. Refused unless the ledger holds a KEEP review for that label, so a recipe always has evidence.
- **FIX-BRIEF / REJECT / refund** whose cause you understand → `R fail --name <short-slug> --model M --symptom "..." --cause "..." --tried "..." --next-lever "..." --evidence "RUN label"`. No cause, no entry: "X failed" alone teaches nothing.
- Recipes approved outside a ledger (older runs) are imported only with human evidence: `--evidence "human:<who> <words> <date>"`.

## Cost questions
`R report` (all `runs/*/ledger.jsonl`) or `R report RUN ...` → per run and per model: spent, refunded, net, takes, KEEPs, **credits per KEEP**, plus every non-KEEP review and refund as a failure candidate. Credits are Higgsfield credits as charged at the time; never mix them with USD budgets.

## Rules
- A recipe is evidence of one success, not a guarantee: re-lint, re-audit and re-approve when reused (the gate binds the exact prompt hash).
- Name versions (`-v2`) instead of overwriting; promote refuses an existing name.
- `INDEX.md` is generated (`R index`); do not edit it by hand.
