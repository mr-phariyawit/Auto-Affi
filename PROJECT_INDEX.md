# Auto-Affi — Project Index

> Current map of the repo after the **2026-06-08 consolidated-knowledge hard-reset** (commit `82c7fe5c`).
> Hand-maintained — the prior auto-generated AEGIS index was stale (pointed to a deleted brain graph
> and missing docs). **Single source of truth = [`SPEC.md`](SPEC.md).**

## Start here
| Doc | What |
|-----|------|
| [SPEC.md](SPEC.md) | ★ Canonical spec — vision, 9-agent architecture, pipeline, data model, roadmap; §10.5 operational gates; §17 honest as-built; §18 ADRs; §19 creative method; §20 gates |
| [README.md](README.md) | Production usage guide (Thai) — how to drive a new product clip |
| [wiki/HOME.md](wiki/HOME.md) | Knowledge base (12 sections: workflow, compliance, model locks, Hanky-V12 runbook, principles, research) |
| [CLAUDE.md](CLAUDE.md) | AEGIS agent rules + golden rules |

## Planning (Phase 1 rebuild)
- [`_aegis-output/iso-docs/`](_aegis-output/iso-docs/) — PM-01 plan · SI-01 requirements · SI-02 traceability
- [`.aegis/brain/tasks/phase1-breakdown.md`](.aegis/brain/tasks/phase1-breakdown.md) — epics + Sprint-1 tasks
- [`.aegis/brain/sprints/current/`](.aegis/brain/sprints/current/) — Sprint 1 plan + kanban
- [`.aegis/brain/human-queue.md`](.aegis/brain/human-queue.md) — the **4 live gates** (critical path)

## Knowledge
- [`wiki/`](wiki/) — 00 overview … 11 glossary
- [`docs/principles/`](docs/principles/) (17) · [`docs/research/`](docs/research/) (9) · `docs/decisions/`
- [`docs/archive/`](docs/archive/) — superseded docs (e.g. `SUPER_SPEC-2026-06-05.md`)

## Code
- `src/auto_affi/` — **DELETED** in hard-reset; REBUILD pending (recoverable at `5602e53c`; layout in SI-02)
- [`scripts/`](scripts/) — `verify_runs.py` (cleanroom verifier), `social_media_scanner.py`, `validate_caption_voice_sync.py`
- [`tools/`](tools/) — AEGIS framework tooling (shell/mjs)

## Outputs & data
- [`runs/`](runs/) — 14 production runs · verified: [`_aegis-output/qa/runs-verification-2026-06-08.md`](_aegis-output/qa/runs-verification-2026-06-08.md)
- [`_aegis-output/`](_aegis-output/) — agent outputs (`qa/`, `reviews/`, `iso-docs/`)
- [`data/`](data/) — CSV registries (run_registry, product_intelligence_candidates, signal_*)
- `reports/` — daily scan digests

## Key facts (SPEC §17/§20 — read before planning)
- **Status: outcome-zero** — 0 live posts, 0 real clicks, 0 measured KPI.
- **Critical path = 4 human gates** (Shopee Affiliate TH · Meta/IG token · Higgsfield credits · runtime host), **not code**.
- **Definition of done = ONE real live video + ONE real subId click — verified, not produced.**
