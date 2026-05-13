# Sprint 3 Plan -- Auto-Affi

- **Sprint**: sprint-3
- **Goal**: Close the feedback loop -- Analytics collecting metrics, Feedback Curator extracting patterns into the Wiki, Orchestration wiring the DAGs, plus Strategy Wiki RAG and Safety music license to complete tails.
- **Duration**: 5 days (2026-05-13 to 2026-05-18)
- **Capacity**: 27 story points
- **Phase**: Phase 1 -- Single Closed Loop
- **Predecessor**: Sprint 2 (28/28 pts, 100% delivered)

---

## Sprint Backlog

| Task ID | Title | Epic | Points | Assignee | Priority |
|---------|-------|------|--------|----------|----------|
| AFFI-T-022 | Metrics schema + Analytics collector skeleton | E-006 | 3 | spider-man | P1 |
| AFFI-T-023 | Full metrics recording + outcome labeling | E-006 | 3 | spider-man | P1 |
| AFFI-T-024 | Click-to-conversion attribution (subId join) | E-006 | 2 | spider-man | P2 |
| AFFI-T-025 | Feedback Curator skeleton + pattern extraction | E-007 | 5 | spider-man | P1 |
| AFFI-T-026 | Wiki tier promotion + deprecation logic | E-007 | 3 | spider-man | P2 |
| AFFI-T-034 | Workflow definitions: Discovery + Campaign DAGs | E-009 | 5 | spider-man | P1 |
| AFFI-T-006 | Strategy Wiki RAG integration | E-002 | 3 | spider-man | P2 |
| AFFI-T-030 | Music license validation gate | E-008 | 3 | spider-man | P3 |

**Total**: 27 points across 8 tasks

---

## Sprint Rationale

Sprint 3 closes the feedback loop that makes Auto-Affi self-improving:

1. **Analytics (E-006, 8pt)**: Without metrics collection, the learning loop has zero signal. This is the highest-leverage work remaining. Metrics schema, collector, outcome labeling, and conversion attribution complete E-006 entirely.

2. **Feedback/Wiki (E-007 first 2 tasks, 8pt)**: Turns raw metrics into structured wiki patterns. The Feedback Curator compares win/fail cohorts, extracts patterns, and writes to the review queue. Wiki tier promotion implements the Hypothesis->Validated->Canonical->Deprecated lifecycle from SPEC 5.2.

3. **Orchestration foundation (E-009, 5pt)**: Defines the Discovery and Campaign workflow DAGs with typed activity steps. Phase 1 uses in-process executor (no Temporal server required). This wires the full pipeline into a runnable DAG rather than manual `make_demo` invocation.

4. **Tails (6pt)**: Strategy Wiki RAG (T-006) connects the wiki to the Strategist. Music license validation (T-030) completes another Safety gate. Both are small, high-value completions of existing epic scope.

Priority order follows data dependency:
1. T-022 (metrics schema) -> T-023 (outcome labeling) -> T-024 (attribution)
2. T-025 (curator, depends on outcome labels) -> T-026 (tier promotion)
3. T-034 (workflows, depends on all upstream agents existing)
4. T-006 + T-030 (independent tails, parallelizable)

---

## Definition of Done (per task)

1. Implementation passes lint via `.venv/bin/python -m ruff check`
2. Unit tests pass via `.venv/bin/python -m pytest -m unit`
3. Black Panther code review APPROVED
4. SI.02 traceability updated
5. No P0/P1 issues open

---

## Risks

- T-024 (attribution) assumes Shopee conversionReport schema from docs -- may need adjustment when real API is available (MBP External-access blocker: API keys needed for live data)
- T-025 (curator) pattern extraction quality depends on having enough outcome data -- Phase 1 will start with fixture data
- T-034 (workflows) is foundational but deliberately simple (in-process executor) -- full Temporal integration deferred to Sprint 4
