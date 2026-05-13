# Retrospective -- 2026-05-13 Session Arc

> Scope: Physical session covering Sprints 1+2 (prior context) + resonance enrichment + Sprints 3+4 (this context)
> Date: 2026-05-13
> Duration: 3 context windows (session-1: S1+S2, session-2: DX+brain, session-3: resonance+S3+S4)
> Branch: claude/ai-marketing-platform-JFcLs

---

## The Arc

| Metric | Session Start | Session End | Delta |
|--------|--------------|-------------|-------|
| Points done | 0 | 108 | +108 |
| Roadmap % | 0% | 82% | +82pp |
| Epics complete | 0/10 | 7/10 | +7 |
| Tasks done | 0/45 | 33/45 | +33 |
| Tests | 0 | 377 | +377 |
| Coverage | 0% | 85% | +85pp |
| Resonance files | 1 | 10 | +9 |
| ADRs | 0 | 5 | +5 |
| Commits | 0 | 8 | +8 |

Sprint velocity held dead steady: 26, 28, 27, 27 (avg 27 pt/sprint).

Epics completed: E-001 Scout, E-002 Strategy, E-005 Publishing, E-006 Analytics,
E-007 Feedback/Wiki, E-008 Safety, E-009 Orchestration.

Phase 1 "single closed loop" is architecturally complete: every subsystem
from product discovery through video publishing through metrics collection
through wiki learning has a tested implementation.

---

## What Worked

### 1. Path A (adapt existing docs) over Path B (re-spec)

The project already had rich docs in `docs/pm/`, `docs/si/`, and `SPEC.md`.
Rather than regenerating from scratch via `/super-spec`, Sprint 1 adapted
these into BLOCK 0 artifacts (PM.01, SI.01, SI.02). This saved roughly
one full sprint of spec work.

**Lesson**: When the project has existing documentation, adapt it rather
than discarding it. The sunk cost is real and recoverable.

### 2. Resonance enrichment BEFORE implementation sprints

The session-3 resonance enrichment (9 files, 5 ADRs from SPEC.md) was
done BEFORE Sprints 3+4. This meant every implementation decision had
pre-loaded context: cost-model.md provided exact budget caps for the
circuit-breaker, domain-thai.md provided the mega-sale calendar for the
Strategist, learning-loop.md provided tier semantics for the promoter.

Zero re-debates on thresholds or design choices across 18 tasks.

**Lesson**: Enrich resonance BEFORE the implementation sprint that depends
on it. The 30-minute investment pays back across every subsequent task.

### 3. SPEC-sourced numbers everywhere

Every configurable threshold in the codebase traces to a SPEC.md section:
- Kill switch auto-kill: 3 violations/24h (SPEC 10.4)
- Editor budget cap: $0.40 (SPEC 3.5.1)
- Daily budget cap: $50 (NFR-CS-03)
- Per-video target: $2.87 (SPEC Appendix C)
- Wiki tiers: 5/20/3 evidence counts (SPEC 5.2)

Result: 0 human escalations across 4 sprints. No judgment calls on
numbers that could have triggered MBP category 1 (Identity) questions.

**Lesson**: SPEC-sourced thresholds reduce judgment-call escalations to
near-zero. Bake the numbers into resonance, not into ad-hoc decisions.

### 4. Loki adversarial pass on safety-critical designs

Loki's resonance review caught 3 revisions before commit:
- MoM CTR 5% sustainability caveat (taper expectation)
- Subsystem map gaps (+Shared Context Bus, +Ops Console)
- Mega-sale calendar gaps (+Valentine's, +Mother's Day TH, +PayDay)

All constructive; all applied before any implementation consumed them.

### 5. Consistent adapter pattern

The `_http_base.py` + `ToolResult[T]` + `Protocol` pattern established
in Sprint 1 made every subsequent adapter (TTS, video gen, publisher,
analytics transport) a drop-in. Tests followed the same shape. This
compounded across 4 sprints.

---

## What Didn't Work / Friction

### 1. Session 1 venv misdiagnosis

System Python (3.9) was used instead of `.venv/bin/python` (3.13),
causing PEP 695 syntax errors. Cost ~one orchestration cycle to diagnose.
Fixed permanently via instinct promotion + CLAUDE.md Rule #8.

### 2. Hook drift never resolved

5 tools referenced in `.claude/settings.json` hooks still don't exist:
`aegis-approval-gate/check.mjs`, `aegis-brain-graph/hook.sh`,
`aegis-brain-graph/staleness.mjs`, `aegis-live-tail/emit.mjs`,
`aegis-activity-logger/log.mjs`, `aegis-resume/session-start.mjs`.
These fire silent errors on every tool call. Routed around all session,
never fixed. Annoyance noise, not a blocker, but technical debt.

### 3. Orchestrator "holding for direction" pattern

Early in the session, the orchestrator paused with "awaiting direction"
instead of applying the command chain. Board corrected, memory pinned.
No recurrence after the correction.

### 4. Test iteration on cohort splitting

`split_cohorts()` in FeedbackCurator needed 2 iterations because the
20% cohort calculation returned only 1 member for small datasets,
making pattern extraction impossible (needs count >= 2). The minimum
was bumped from `max(1,...)` to `max(2,...)`. Minor friction but a
reminder to think about edge cases in statistical functions.

---

## Velocity & Projection

| Sprint | Points | Tasks | New Tests |
|--------|--------|-------|-----------|
| sprint-1 | 26 | 7 | 121 |
| sprint-2 | 28 | 8 | 93 |
| sprint-3 | 27 | 8 | 108 |
| sprint-4 | 27 | 10 | 55 |
| **Total** | **108** | **33** | **377** |

Average: 27 pt/sprint. Consistent enough to project Sprint 5 at 23 pt
(the exact remaining Phase 2 scope). Phase 2 could complete in a single
sprint given steady velocity.

---

## Lessons Promoted

See `.aegis/brain/learnings/`:
1. `resonance-before-implementation.md`
2. `spec-sourced-thresholds.md`
3. `chain-after-report.md`
