# Sprint 1 Plan -- Auto-Affi

- **Sprint**: sprint-1
- **Goal**: Build the foundation pipeline -- Scout Agent (search + score + filter) + Strategist skeleton + Storyboard schema + Safety gate. These form the first three stages of the end-to-end pipeline.
- **Duration**: 5 days (2026-05-13 to 2026-05-18)
- **Capacity**: 26 story points
- **Phase**: Phase 1 -- Single Closed Loop

---

## Sprint Backlog

| Task ID | Title | Epic | Points | Assignee | Status |
|---------|-------|------|--------|----------|--------|
| AFFI-T-001 | Shopee GraphQL adapter -- productOfferV2 search | E-001 | 5 | spider-man | TODO |
| AFFI-T-002 | Scout scoring rubric implementation | E-001 | 3 | spider-man | TODO |
| AFFI-T-003 | Restricted category filter | E-001 | 2 | spider-man | TODO |
| AFFI-T-005 | CampaignBrief schema + Strategist skeleton | E-002 | 3 | spider-man | TODO |
| AFFI-T-008 | Storyboard JSON schema + single Writer agent | E-003 | 5 | spider-man | TODO |
| AFFI-T-011 | Claim auditor -- Thai script safety | E-003 | 3 | spider-man | TODO |
| AFFI-T-029 | Pre-publish safety gate | E-008 | 5 | spider-man | TODO |

**Total**: 26 points across 7 tasks

---

## Sprint Rationale

Sprint 1 targets the left side of the pipeline: Discovery -> Strategy -> Writers -> Safety. This creates the complete data flow from "find a product" to "have a validated storyboard ready for video production." Video production (AFFI-E-004) and publishing (AFFI-E-005) are Sprint 2 scope.

The existing codebase already has partial implementations for:
- shopee.py adapter (needs completion)
- scout_scoring.py (needs rubric finalization)
- campaign_brief.py schema (needs field completion)
- storyboard.py schema (needs validation rules)
- claim_auditor.py (needs Thai-specific patterns)

Sprint 1 completes and hardens these into production-ready modules with tests.

---

## Definition of Done (per task)

1. Implementation passes lint (ruff)
2. Unit tests pass (pytest -m unit) on Python 3.12+
3. Black Panther code review APPROVED
4. SI.02 traceability updated
5. No P0/P1 issues open

---

## Risks

- Python 3.12+ not available on current system (tests need explicit env setup)
- Shopee API access may require real credentials for integration tests (unit tests use VCR)
