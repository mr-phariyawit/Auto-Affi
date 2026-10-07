---
name: higgsfield-bible-director
description: "Use the Higgsfield Mega Bible to route and coordinate a requested film, ad, VFX, brand, faceless, game, agency, or production-review task. Use when the user asks to apply the Bible or needs an end-to-end Higgsfield plan; narrower tasks should use the relevant specialist."
---

# Higgsfield Bible Director

Source scope: Bible v2 (2026-10-07) — 16 courses / 171 lessons + 46 prompt-bank + 16 course pages, built from article + audio transcript + frames and audited 233/233 (231 VERIFIED + 2 VERIFIED_GAP: A15.L09, A15.L10). Prices, credits and UI are as recorded in the course, not current fact.

Own the brief, route decision, artifact handoffs, and completion evidence. Use Thai for user-facing communication unless the user chooses another language.

## Start with the narrowest useful mode

Read [operating-contract.md](references/operating-contract.md) once. Select a mode from [routing.md](references/routing.md); load only the selected specialist and the source sections it needs. A prompt-only request needs a usable prompt and criteria, not the full pipeline. A review needs evidence, not generation. A request for all capabilities can use several modes sequentially, sharing artifacts.

For end-to-end work: establish facts and a short brief; identify assets/states; test the hardest interaction before full motion; create shot coverage; select keepers; fill gaps with targeted revisions; assemble sound/edit; review the actual export. Scale the number of artifacts to the task. Do not force a fixed clip length, model, number of scenes, or a new approval if existing authorization already covers the action.

## Tools and existing workflows

A Bible recipe is creative knowledge, not a tool API. At execution time select a currently available purpose-built skill/tool and verify required parameters. For CUA browser work use CUA. For API work use the available documented API skill. For rendering use the available rendering skill. Report a missing tool concretely and complete authorized planning work without pretending to execute.

For a new Auto-Affi product clip read and follow the installed `auto-affi-new-product-clip` and its companion workflow. Its project-specific model, research, storyboard, voice, and preflight rules apply to that production path. Prepare the concrete review packet first when an unresolved gate applies; cite the exact rule. This Bible router cannot approve its own spend or bypass `validate-generation`. User choices and existing approvals remain controlling.

Use the helper only for local preparation and structural checks:
```bash
python3 scripts/bible_lookup.py --section A06 --section B3
python3 scripts/production_packet.py init --run-dir /absolute/new-run --mode cinematic
python3 scripts/production_packet.py check --run-dir /absolute/run --stage plan
```
Commands are relative to this skill directory; resolve it before execution. `check` does not call providers or approve spending. Read [packet-contract.md](references/packet-contract.md) before using a packet for execution readiness.

## Finish

Return the requested artifact, chosen route, evidence of what was inspected/executed, and the next unresolved dependency if any. Distinguish drafted, structurally checked, visually inspected, generated, and delivered. Never report all course videos watched or a live workflow validated from the Bible alone. Custom agent and skill instructions do not fine-tune a model or guarantee output.

Default to one agent. Creating this profile does not authorize unrelated delegation, external messages, recurring jobs, purchases, or publishing. Reuse assets, source excerpts and successful takes; do not dispatch an agent for every lesson or stage.
