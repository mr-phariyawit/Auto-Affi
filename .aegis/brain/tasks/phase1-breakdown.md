# Auto-Affi — Phase 1 Work Breakdown

> Generated 2026-06-08 from `SPEC.md` §3/§13/§17–20 after the consolidated-knowledge
> hard-reset (`82c7fe5c`). Phase-1 goal = **single real loop closed** →
> ONE real video live + ONE real subId click (verified, `SPEC.md` §20).
>
> Engineering is REBUILD (prior `src/auto_affi/` recoverable at `5602e53c` — use as reference, do not blind-restore).
> **Live outcome is gated on the 4 human gates (AFFI-GATE-*), not code.**

## Epics

| Epic | Title | SPEC § | Notes |
|------|-------|--------|-------|
| AFFI-E1 | Foundation & contracts | ADR-002, §8.2 | schemas, settings, tool-result, registry |
| AFFI-E2 | Adapters (locked stack) | §19.3, ADR-006 | Shopee, Higgsfield CLI, edge-tts, Gemini stills, GCS |
| AFFI-E3 | Agent crew (Phase-1 subset) | §3.1–3.4 | Scout, Strategist, 1 Writer |
| AFFI-E4 | Pipeline + Producer/Editor + cost | §3.5, ADR-004/007 | in-process 10-stage gated flow |
| AFFI-E5 | Compliance & QA gates | §10, SUPER_SPEC | disclosure, cleanroom, speed-guard, caption/VO sync |
| AFFI-E6 | Publish + metrics + Wiki loop | §3.6–3.8, §5 | IG Reel, metrics poll, Wiki write (gated G1/G2) |
| AFFI-GATE | Human critical path | §20 | the 4 gates — only the human clears these |

## Human gates (critical path — `human-queue.md`)

| ID | Gate | Category | Blocks |
|----|------|----------|--------|
| AFFI-GATE-G1 | Shopee Affiliate Program TH (apply) | External | all live publish + real subId |
| AFFI-GATE-G2 | Meta Business + IG Creator + 60-day token | External | IG publishing |
| AFFI-GATE-G3 | Higgsfield account + credits | External | visual video gen |
| AFFI-GATE-G4 | Runtime host decision | Identity | deploy + reliability SLO |

## Sprint 1 tasks (offline-buildable — zero paid calls)

| ID | Title | Epic | Pts | Acceptance |
|----|-------|------|-----|-----------|
| AFFI-S1-01 | Restore build infra (pyproject.toml, uv.lock, pytest cfg) | E1 | 3 | `uv sync` + `pytest` run; re-decided deps documented |
| AFFI-S1-02 | Core schemas + tool-result contract (pydantic) | E1 | 3 | schemas validate; `{ok,data,cost_usd,latency_ms,trace_id}` enforced; tests green |
| AFFI-S1-03 | Local JSONL/CSV registry + run model | E1 | 2 | run roundtrip persists/loads; uses surviving `data/*.csv`; tests green |
| AFFI-S1-04 | Shopee adapter (dry-run) + Scout scoring | E2/E3 | 3 | keyword→scored candidate; no network in tests; tests green |
| AFFI-S1-05 | Strategist + Writer + Storyboard schema + HSO×VCS rubric lint | E3 | 5 | brief+storyboard validate; rubric lint (hook ≤1.0s, shots 3–5s, 100% captions) |
| AFFI-S1-06 | Producer/Editor + in-process pipeline + Higgsfield CLI adapter (dry-run) + cost caps | E4 | 5 | pipeline runs dry; editor $0.40 cap + daily budget×1.1 stop enforced; tests green |
| AFFI-S1-07 | Compliance gate: cleanroom + speed-guard + caption/VO sync | E5 | 3 | non-compliant render hard-blocked w/ reason; wires surviving `validate_caption_voice_sync.py` |
| AFFI-S1-08 | Offline vertical slice on 1 fixture product → compliant 9:16 master | E1–E5 | 3 | fixture → master.mp4 9:16 ≤60s, passes compliance, 0 paid calls |

**Sprint 1 engineering total: 27 pts.** Live-loop tasks (publish/metrics/Wiki, AFFI-E6)
are deferred to Sprint 2 because they are gated on G1/G2 — building them now would
re-create the "code without outcome" trap (`SPEC.md` §17.3).

## Definition of Done
- **Sprint 1 (engineering)**: `src/` skeleton green; fixture product → compliance-passing master in dry-run; cost caps enforced. *This is NOT Phase-1 done.*
- **Phase 1 (product)**: ONE real video live on IG + ONE real subId click recorded — **verified**. Requires G1+G2+G3 (+G4 for 24/7).
