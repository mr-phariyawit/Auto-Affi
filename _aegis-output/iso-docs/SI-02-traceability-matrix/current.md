# SI.02 Traceability Matrix -- Auto-Affi

> Maps SI.01 requirements to implementation artifacts + test coverage.
> Updated as tasks complete. Phase 0 baseline: requirements mapped, impl/test TBD.

- **Project**: Auto-Affi
- **Created**: 2026-05-13
- **Status**: Initialized (requirement IDs seeded, impl/test columns pending)

---

## Legend

| Column | Meaning |
|--------|---------|
| REQ ID | Requirement ID from SI.01 |
| Description | Short description |
| Epic | AEGIS Epic ID |
| Task(s) | AEGIS Task IDs that implement this requirement |
| Source File(s) | Implementation files |
| Test(s) | Test files that verify this requirement |
| Status | NOT_STARTED / IN_PROGRESS / IMPLEMENTED / VERIFIED |

---

## Functional Requirements

| REQ ID | Description | Epic | Task(s) | Source File(s) | Test(s) | Status |
|--------|-------------|------|---------|----------------|---------|--------|
| FR-SC-01 | Shopee product search | AFFI-E-001 | AFFI-T-001 | src/auto_affi/adapters/shopee.py | tests/unit/test_shopee_adapter.py | IN_PROGRESS |
| FR-SC-02 | Product scoring rubric | AFFI-E-001 | AFFI-T-002 | src/auto_affi/agents/scout_scoring.py | tests/unit/test_scout_scoring.py | IN_PROGRESS |
| FR-SC-03 | Restricted category filter | AFFI-E-001 | AFFI-T-003 | -- | -- | NOT_STARTED |
| FR-SC-04 | Wiki saturation query | AFFI-E-001 | AFFI-T-004 | -- | -- | NOT_STARTED |
| FR-ST-01 | CampaignBrief creation | AFFI-E-002 | AFFI-T-005 | src/auto_affi/schemas/campaign_brief.py | tests/unit/test_campaign_brief.py | IN_PROGRESS |
| FR-ST-02 | Wiki RAG before reasoning | AFFI-E-002 | AFFI-T-006 | -- | -- | NOT_STARTED |
| FR-ST-03 | Mega-sale calendar boost | AFFI-E-002 | AFFI-T-007 | -- | -- | NOT_STARTED |
| FR-WR-01 | Storyboard JSON creation | AFFI-E-003 | AFFI-T-008 | src/auto_affi/schemas/storyboard.py | tests/unit/test_storyboard.py | IN_PROGRESS |
| FR-WR-02 | Writers' Room 6 sub-agents | AFFI-E-003 | AFFI-T-009 | -- | -- | NOT_STARTED |
| FR-WR-03 | Hook/shot/audio timing rules | AFFI-E-003 | AFFI-T-010 | -- | -- | NOT_STARTED |
| FR-WR-04 | Thai script + claim safety | AFFI-E-003 | AFFI-T-011 | src/auto_affi/agents/claim_auditor.py | tests/unit/test_claim_auditor.py | IN_PROGRESS |
| FR-VD-01 | Master video specs | AFFI-E-004 | AFFI-T-012 | src/auto_affi/pipeline/local_renderer.py | tests/integration/test_local_renderer.py | IN_PROGRESS |
| FR-VD-02 | Editor standard passes | AFFI-E-004 | AFFI-T-013 | -- | -- | NOT_STARTED |
| FR-VD-03 | Hyperframe Thai overlay | AFFI-E-004 | AFFI-T-014 | -- | -- | NOT_STARTED |
| FR-VD-04 | Editor budget cap + fallback | AFFI-E-004 | AFFI-T-015 | -- | -- | NOT_STARTED |
| FR-VD-05 | TTS provider whitelist | AFFI-E-004 | AFFI-T-016 | -- | -- | NOT_STARTED |
| FR-PB-01 | IG Reels publish | AFFI-E-005 | AFFI-T-017 | -- | -- | NOT_STARTED |
| FR-PB-02 | FB Reels + YT Shorts | AFFI-E-005 | AFFI-T-018 | -- | -- | NOT_STARTED |
| FR-PB-03 | subId taxonomy on links | AFFI-E-005 | AFFI-T-019 | src/auto_affi/adapters/shopee_subids.py | tests/unit/test_shopee_subids.py | IN_PROGRESS |
| FR-PB-04 | Ad disclosure in caption | AFFI-E-005 | AFFI-T-020 | -- | -- | NOT_STARTED |
| FR-PB-05 | Wiki-driven posting time | AFFI-E-005 | AFFI-T-021 | -- | -- | NOT_STARTED |
| FR-AN-01 | Metrics polling schedule | AFFI-E-006 | AFFI-T-022 | -- | -- | NOT_STARTED |
| FR-AN-02 | Full metrics recording | AFFI-E-006 | AFFI-T-023 | -- | -- | NOT_STARTED |
| FR-AN-03 | Click-conversion attribution | AFFI-E-006 | AFFI-T-024 | -- | -- | NOT_STARTED |
| FR-FB-01 | Feedback Curator nightly | AFFI-E-007 | AFFI-T-025 | -- | -- | NOT_STARTED |
| FR-FB-02 | Wiki tier system | AFFI-E-007 | AFFI-T-026 | src/auto_affi/wiki/entry.py | -- | IN_PROGRESS |
| FR-FB-03 | Bilateral sync | AFFI-E-007 | AFFI-T-027 | -- | -- | NOT_STARTED |
| FR-FB-04 | Offline replay | AFFI-E-007 | AFFI-T-028 | -- | -- | NOT_STARTED |
| FR-SF-01 | Pre-publish safety gates | AFFI-E-008 | AFFI-T-029 | src/auto_affi/agents/claim_auditor.py | tests/unit/test_claim_auditor.py | IN_PROGRESS |
| FR-SF-02 | Music license check | AFFI-E-008 | AFFI-T-030 | -- | -- | NOT_STARTED |
| FR-SF-03 | Ad disclosure enforcement | AFFI-E-008 | AFFI-T-031 | -- | -- | NOT_STARTED |
| FR-SF-04 | Kill switch (multi-level) | AFFI-E-008 | AFFI-T-032 | -- | -- | NOT_STARTED |
| FR-SF-05 | Auto-kill on 3 violations | AFFI-E-008 | AFFI-T-033 | -- | -- | NOT_STARTED |
| FR-OR-01 | Five Temporal workflows | AFFI-E-009 | AFFI-T-034 | -- | -- | NOT_STARTED |
| FR-OR-02 | Idempotent activities | AFFI-E-009 | AFFI-T-035 | -- | -- | NOT_STARTED |
| FR-OR-03 | Budget cap circuit-breaker | AFFI-E-009 | AFFI-T-036 | -- | -- | NOT_STARTED |
| FR-OC-01 | Ops dashboard | AFFI-E-010 | AFFI-T-037 | -- | -- | NOT_STARTED |
| FR-OC-02 | Manual approve/reject | AFFI-E-010 | AFFI-T-038 | -- | -- | NOT_STARTED |

## Non-Functional Requirements

| REQ ID | Description | Task(s) | Verification Method | Status |
|--------|-------------|---------|---------------------|--------|
| NFR-PF-01 | Video latency P50 < 90min | -- | Temporal metrics | NOT_STARTED |
| NFR-PF-02 | Metrics lag < 5 min | -- | Polling schedule test | NOT_STARTED |
| NFR-PF-03 | Prompt cache >= 70% | -- | Langfuse dashboard | NOT_STARTED |
| NFR-RL-01 | Pipeline success >= 90% P1 | -- | Success rate monitor | NOT_STARTED |
| NFR-CS-01 | Cost/video <= $3.32 P1 | -- | Cost dashboard | NOT_STARTED |
| NFR-SC-01 | 5 videos/day P1 | -- | Daily count monitor | NOT_STARTED |
| NFR-SEC-01 | Secrets in Vault/SOPS | -- | CI scan | NOT_STARTED |
| NFR-OB-01 | OTel 100% coverage | -- | Trace analysis | NOT_STARTED |
| NFR-MT-02 | Test coverage >= 70% | -- | pytest-cov report | NOT_STARTED |

---

## Coverage Summary

| Category | Total | NOT_STARTED | IN_PROGRESS | IMPLEMENTED | VERIFIED |
|----------|-------|-------------|-------------|-------------|----------|
| FR-* | 38 | 26 | 12 | 0 | 0 |
| NFR-* | 27 | 27 | 0 | 0 | 0 |
| **Total** | **65** | **53** | **12** | **0** | **0** |

> 12 requirements show IN_PROGRESS because partial source files already exist in `src/auto_affi/`.
> Full VERIFIED status requires passing tests on Python 3.12+ environment.
