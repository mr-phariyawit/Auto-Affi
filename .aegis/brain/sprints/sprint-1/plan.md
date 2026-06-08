# Sprint 1 — Rebuild the offline pipeline foundation

> Created: 2026-06-08 | Source: `SPEC.md` §3/§13/§17–20, `tasks/phase1-breakdown.md`
> Follows the consolidated-knowledge hard-reset (`82c7fe5c`).

## Sprint Goal
Rebuild `src/auto_affi/` to a **green offline vertical slice**: one fixture product →
compliance-passing 9:16 master, with **zero paid provider calls** and cost caps enforced —
while the 4 human gates (G1–G4) clear in parallel.

## Why offline-first (the §17.3 lesson)
The prior build hit *code-complete, outcome-zero* because it produced renders while the
4 external/identity gates stayed open and the video stack thrashed. Sprint 1 therefore
(a) locks the stack (§19.3), (b) builds only what runs without credentials, and
(c) routes the live-outcome work behind the human gates.

## Scope (27 pts engineering)
| ID | Title | Pts |
|----|-------|-----|
| AFFI-S1-01 | Restore build infra (pyproject/uv/pytest) | 3 |
| AFFI-S1-02 | Core schemas + tool-result contract | 3 |
| AFFI-S1-03 | Local JSONL/CSV registry + run model | 2 |
| AFFI-S1-04 | Shopee adapter (dry-run) + Scout scoring | 3 |
| AFFI-S1-05 | Strategist + Writer + Storyboard + HSO×VCS rubric lint | 5 |
| AFFI-S1-06 | Producer/Editor + pipeline + Higgsfield CLI (dry-run) + cost caps | 5 |
| AFFI-S1-07 | Compliance gate (cleanroom + speed-guard + caption/VO sync) | 3 |
| AFFI-S1-08 | Offline vertical slice on 1 fixture product | 3 |

## Parallel human track (NOT engineering points — `human-queue.md`)
- G1 Shopee Affiliate TH · G2 Meta/IG token · G3 Higgsfield credits · G4 runtime host

## Out of scope (Sprint 2+, gated)
- Live IG publish, real metrics poll, Wiki write-back (AFFI-E6) — needs G1/G2
- Full Writers' Room, multi-platform, Temporal, KG Wiki — Phase 2/3

## Definition of Done (Sprint 1, engineering — honest)
- [ ] `uv sync` + `pytest` run clean on a rebuilt `src/auto_affi/`
- [ ] Fixture product → `master.mp4` (9:16, ≤60s) passing all compliance gates, **dry-run, 0 paid calls**
- [ ] Cost caps (editor $0.40, daily budget×1.1) enforced in code with tests
- [ ] **Explicitly NOT** the Phase-1 live DoD — that needs the gates

## Method
TDD per rebuilt module (write failing test → implement → green). Reference prior code at
`5602e53c` but re-decide deliberately (esp. ADR-005 Temporal → keep in-process for Phase 1).
Black Panther review + War Machine QA + Loki challenge before any task → DONE.
