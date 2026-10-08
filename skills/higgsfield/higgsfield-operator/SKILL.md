---
name: higgsfield-operator
description: "Actually generate on Higgsfield (Seedance / Soul ID / Genjutsu) by driving the logged-in web UI through Claude in Chrome, behind the project's PGA gate and a per-run credit cap: lint the prompt, audit + human approval via gate_cli, read the live credit price from the Generate button, preflight, click once, log the spend, download and hand to QC. Use whenever someone wants a Higgsfield video or image generated, a take re-run, the live price of a Higgsfield job, or 'gen ใน Higgsfield', 'กด generate ให้หน่อย', 'เช็คราคาเครดิต' — and never click Generate without this skill's gate."
---

# Higgsfield Operator (UI route, gated)

Executes Higgsfield jobs in the user's logged-in Chrome. The coded pipeline stays Gemini/Veo/Kling (SPEC §8, ADR-009); this skill is the sanctioned out-of-pipeline route and it goes through the **same** PGA gate (`auto_affi.pipeline.prompt_audit`) via `src/auto_affi/ops/gate_cli.py`. Background: [references/routes.md](references/routes.md).

Credits are real money. The gate exists because un-audited prompts and wrong references burned credits before (memory: Pre-Generation Audit Gate). Never generate on your own initiative: every live generation needs the human's approval of *that* run in chat.

## The loop (one take)

`G` = `uv run python -m auto_affi.ops.gate_cli` (run from the repo root). Exit codes: 0 ok · 1 audit failed · 3 gate blocked · 4 budget blocked.

1. **Prompt.** Write it with `higgsfield-seedance-prompt` and get `lint_prompt.py` to 0 errors.
2. **Run dir + manifest.** `runs/<YYYY-MM-DD>-<slug>/` with `manifest.json` (template: [assets/manifest.example.json](assets/manifest.example.json)). Put the exact prompt text, the identity string (verbatim inside the prompt), `soul_id` = the Element tag, `reference_uris` = every Element/upload you will attach, `max_duration_s` = the model's recorded max, AVOID list as `negative_prompt`. Auto-Affi is 9:16 only — the audit rejects other aspects by design.
3. **Audit.** `G audit --run RUN --stage <stage> --manifest manifest.json` for each stage in order (cast_sheet → objects_sheet → storyboard → contact_sheet → video). Earlier stages that reuse already-locked assets are bypassed **only when the human says so**: `G bypass --run RUN --stage cast_sheet --reason "reuse locked JIAB Soul ID" --by human:<name>`.
4. **Ask for approval.** Show the human: prompt, lint line, audit result + `prompt_hash`, model/settings, expected credits, credit cap. Wait. Only after they approve in chat: `G approve --run RUN --stage video --by human:<name>`. If no cap exists, ask for one and record it on their word: `G budget --run RUN --max-credits N --by human:<name>`.
5. **Set the UI** to exactly the job (model, duration, aspect, resolution, Elements, prompt) — playbook: [references/ui-playbook.md](references/ui-playbook.md).
6. **Read the live price** with [scripts/read_price.js](scripts/read_price.js) (javascript tool). Check `model` and `settings_chips` match the job; if not, fix the UI and re-read.
7. **Preflight.** `G preflight --run RUN --stage video --manifest manifest.json --credits <price>` must exit 0. Exit 3 (prompt/reference changed since approval) → re-audit + re-approve. Exit 4 → ask the human to raise the cap or cut the job.
8. **Click Generate once**, then immediately `G spend --run RUN --credits <price> --commit --label "<shot> take<N>" --route ui --model <model> --ref "<card id/time>"`.
9. **Wait and collect** (polling tips in the playbook). On "Failed · Credits refunded": `G spend --run RUN --credits <price> --refund --label "<shot> take<N> refunded: <hover reason>"`. On success download into `RUN/media/` and review frames.
10. **Review** with `higgsfield-dailies-review` (measure → frames → rubric → `record_review.py` verdict in the same ledger); report produced vs verified honestly. `G status --run RUN` gives the stage/budget/ledger summary for the report.

A second take of the same approved prompt needs a new preflight (budget) but not a new approval; any prompt, reference or setting change does.

## Price checks without generating

To answer "how much would this cost?", do steps 5–6 only and report the reading with its time — prices change (the courses' figures are dated; 2026-10-08 live: Seedance 2.0 · 8s · 720p = 36 credits, list 48).

## Other routes

- **MCP** (`https://mcp.higgsfield.ai/mcp`, OAuth): use only if the server is connected in this session; same gate, read cost from the tool's response before calling generate.
- **REST API** (`~/.codex/skills/higgsfield-api-client`): not usable — project keys returned 401 on 2026-10-08 and ADR-009 retired Higgsfield from the coded pipeline. Do not wire it into `src/` without a new ADR.
