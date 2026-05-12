# Kanban Board -- Sprint 1

- **Sprint**: sprint-1
- **Updated**: 2026-05-13T10:15Z
- **WIP Limit**: 3

---

## TODO

(empty -- all tasks moved to IN_REVIEW or DONE)

## IN_PROGRESS

(empty)

## IN_REVIEW

| Task | Title | Points | Assignee | Notes |
|------|-------|--------|----------|-------|
| AFFI-T-005 | CampaignBrief schema + Strategist skeleton | 3 | spider-man | Strategist agent class created, needs Python 3.12+ to verify tests |
| AFFI-T-029 | Pre-publish safety gate | 5 | spider-man | 3-check composed pipeline created, needs Python 3.12+ to verify tests |

## QA

(empty)

## DONE

| Task | Title | Points | Assignee | Notes |
|------|-------|--------|----------|-------|
| AFFI-T-001 | Shopee GraphQL adapter -- productOfferV2 search | 5 | spider-man | Full impl + 6 unit tests exist. HMAC signing, retry, rate-limit, GraphQL error handling. |
| AFFI-T-002 | Scout scoring rubric implementation | 3 | spider-man | 6-dimension weighted rubric + 9 unit tests. Hard filters + breakdown. |
| AFFI-T-003 | Restricted category filter | 2 | spider-man | Integrated in scout_scoring.py. 10 restricted categories. Parametrized tests. |
| AFFI-T-008 | Storyboard JSON schema + single Writer agent | 5 | spider-man | Full Pydantic model with 7 validators. Tests exist. |
| AFFI-T-011 | Claim auditor -- Thai script safety | 3 | spider-man | 10 regex patterns, 4 categories, severity levels. 7 unit tests. |

---

## Burndown

| Day | TODO | WIP | Review | Done | Points Done |
|-----|------|-----|--------|------|-------------|
| D1 (May 13) | 7 | 0 | 0 | 0 | 0/26 |
| D1 (May 13 update) | 0 | 0 | 2 | 5 | 18/26 |

---

## Notes
- 5 tasks moved to DONE based on existing codebase review -- full implementations with tests already exist
- 2 tasks in IN_REVIEW: new code written this session (strategist.py, safety_gate.py) with tests -- pending Python 3.12+ verification
- Sprint 1 velocity: 18 points done (pending verification), 8 points in review
- Blocked: Python 3.12+ not available on system -- tests cannot execute to verify new code
