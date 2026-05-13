# Sprint 10 Plan -- Auto-Affi

- **Sprint**: sprint-10
- **Goal**: Ship all remaining Quick-Win (MANUAL mode) code — kill-switch human-approval gate, LLM-driven perfect storyboard (QW-8a), deploy script, monitoring lite. After this sprint, only vendor onboarding (human-queue items) blocks first live run.
- **Duration**: 5 days
- **Capacity**: 10 story points (reduced: polish sprint, not new features)
- **Phase**: MANUAL mode launch prep (ADR-008)
- **Predecessor**: Sprint 9 (10/10 pts, 100% delivered, ADR-007 COMPLETE)
- **Track**: Quick-Win / MANUAL mode (from roadmap-quick-win-vs-full.md)

## Sprint Backlog

| Task ID | Title | Epic | Points | Priority | QW Ref |
|---------|-------|------|--------|----------|--------|
| AFFI-T-054 | Kill-switch: wire requires_human_approval on Publisher | E-008 | 1 | P1 | QW-7 |
| AFFI-T-055 | Writers' Room: LLM-driven perfect storyboard (detailed per-scene prompts) | E-003 | 3 | P1 | QW-8a |
| AFFI-T-056 | Deploy: laptop cron script + posting-window scheduler | E-013 | 2 | P2 | QW-9 |
| AFFI-T-057 | Monitoring lite: JSONL metrics exporter + CSV/Sheet dashboard | E-010 | 2 | P2 | QW-10 |
| AFFI-T-058 | Stale kanban + roadmap refresh (sprints 7-9 history, sprint-10 board) | META | 1 | P3 | -- |
| AFFI-T-059 | ISO docs refresh: update PM.01 + SI.02 for sprints 7-9 closure | META | 1 | P3 | -- |

**Total**: 10 points across 6 tasks

## Success Criteria

- Kill-switch wired and tested: Publisher refuses to publish without human approval in MANUAL mode
- Storyboard output includes per-scene visual_prompt with lighting/framing/color/mood fields
- `scripts/deploy-cron.sh` exists and is documented in `docs/runbook-deploy.md`
- `auto_affi.ops.metrics_export` CLI writes daily JSONL summary
- Kanban current, roadmap updated with sprint 7-9 history
- All tests pass (target: 575+)

## Blocked Items (NOT in sprint -- awaiting human-queue resolution)

| QW Ref | Item | Blocker |
|--------|------|---------|
| QW-1 | Shopee Affiliate application | Human: vendor onboarding |
| QW-2 | Meta Business + IG token | Human: vendor onboarding |
| QW-3 | kie.ai credits | Human: vendor onboarding |
| QW-4 | ElevenLabs starter | Human: vendor onboarding |
| QW-5 | .env population | Human: after QW-1..4 |
| QW-6 | Seed Beauty SKUs | Human: curation |
| QW-11..13 | Live ops runs | Blocked on QW-1..6 |

## Notes

- ADR-008 established MANUAL vs AUTONOMOUS modes. Sprint 10 code ensures
  MANUAL mode is fully operational: every publish requires board approval,
  storyboards are viral-grade (not fixture quality), and monitoring is
  sufficient for the first 2 weeks of manual operation.
- After Sprint 10 + human-queue items resolved: first live run is possible.
- Phase 3 (AUTONOMOUS mode + harness-evolver) requires real data from
  MANUAL mode runs -- cannot be started until live ops prove the loop.
