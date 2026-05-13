# Sprint 4 Plan -- Auto-Affi

- **Sprint**: sprint-4
- **Goal**: Close every Phase 1 epic tail -- kill switches, auto-kill, workflow chains, budget circuit-breaker, multi-platform publisher stubs, wiki promotion path, offline replay, and mega-sale calendar. After this sprint, all Phase 1 subsystems are wired end-to-end.
- **Duration**: 5 days (2026-05-13 to 2026-05-18)
- **Capacity**: 27 story points
- **Phase**: Phase 1 -- Single Closed Loop
- **Predecessor**: Sprint 3 (27/27 pts, 100% delivered)

---

## Sprint Backlog

| Task ID | Title | Epic | Points | Assignee | Priority |
|---------|-------|------|--------|----------|----------|
| AFFI-T-031 | Kill switch registry (product/campaign/platform/global) | E-008 | 3 | spider-man | P1 |
| AFFI-T-032 | Auto-kill trigger (3 violations in 24h -> freeze) | E-008 | 3 | spider-man | P1 |
| AFFI-T-035 | Metrics + Learning workflow chains | E-009 | 5 | spider-man | P1 |
| AFFI-T-036 | Budget circuit-breaker for workflows | E-009 | 3 | spider-man | P1 |
| AFFI-T-033 | NSFW safety check placeholder with contract | E-008 | 2 | spider-man | P2 |
| AFFI-T-018 | Posting schedule from Wiki optimal-time | E-005 | 2 | spider-man | P2 |
| AFFI-T-021 | FB Reels + YT Shorts publisher stubs | E-005 | 2 | spider-man | P2 |
| AFFI-T-027 | Wiki promotion path (Safety -> canonical store) | E-007 | 3 | spider-man | P2 |
| AFFI-T-028 | Offline replay for wiki validation | E-007 | 2 | spider-man | P3 |
| AFFI-T-007 | Mega-sale calendar boost in Strategist | E-002 | 2 | spider-man | P3 |

**Total**: 27 points across 10 tasks

---

## Sprint Rationale

Sprint 4 closes every remaining Phase 1 epic tail:

1. **Safety tail (E-008, 8pt)**: Kill switches + auto-kill + NSFW contract.
2. **Orchestration tail (E-009, 8pt)**: Metrics+Learning workflow chains + budget circuit-breaker.
3. **Publishing tail (E-005, 4pt)**: Posting schedule from Wiki + FB/YT stubs.
4. **Wiki tail (E-007, 5pt)**: Promotion path + offline replay.
5. **Strategy tail (E-002, 2pt)**: Mega-sale calendar boost.

---

## Definition of Done (per task)

1. Implementation passes lint via `.venv/bin/python -m ruff check`
2. Unit tests pass via `.venv/bin/python -m pytest -m unit`
3. Black Panther code review APPROVED
4. No P0/P1 issues open
