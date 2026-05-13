# SI.02 Traceability Matrix -- Auto-Affi

> Maps SI.01 requirements to implementation artifacts + test coverage.
> Updated: 2026-05-13 (Sprint 10 in progress, Sprint 1-9 complete).

- **Project**: Auto-Affi
- **Created**: 2026-05-13
- **Last updated**: 2026-05-13 (Sprint 10, session 9)
- **Status**: Phase 1+2 complete, MANUAL mode prep in progress

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
| FR-SC-01 | Shopee product search | E-001 | T-001 | adapters/shopee.py, adapters/shopee_public.py | test_shopee_adapter.py, test_shopee_public.py | VERIFIED |
| FR-SC-02 | Product scoring rubric | E-001 | T-002 | agents/scout_scoring.py | test_scout_scoring.py | VERIFIED |
| FR-SC-03 | Restricted category filter | E-001 | T-003 | agents/scout_scoring.py | test_scout_scoring.py | VERIFIED |
| FR-SC-04 | Wiki saturation query | E-001 | T-004 | wiki/saturation.py | test_saturation.py | VERIFIED |
| FR-ST-01 | CampaignBrief creation | E-002 | T-005 | schemas/campaign_brief.py | test_campaign_brief.py | VERIFIED |
| FR-ST-02 | Wiki RAG before reasoning | E-002 | T-006 | wiki/retriever.py | test_wiki_retriever.py | VERIFIED |
| FR-ST-03 | Mega-sale calendar boost | E-002 | T-007 | agents/strategist.py | test_strategist.py | VERIFIED |
| FR-WR-01 | Storyboard JSON creation | E-003 | T-008, T-037 | schemas/storyboard.py, agents/writers_room.py | test_storyboard.py, test_writers_room.py | VERIFIED |
| FR-WR-02 | Writers' Room debate panel | E-003 | T-038 | agents/writers_room.py | test_writers_room.py | VERIFIED |
| FR-WR-03 | Hook/shot/audio timing rules | E-003 | T-010 | schemas/storyboard.py (validators) | test_storyboard.py | VERIFIED |
| FR-WR-04 | Thai script + claim safety | E-003 | T-011 | agents/claim_auditor.py | test_claim_auditor.py | VERIFIED |
| FR-VD-01 | Master video specs | E-004 | T-012 | pipeline/local_renderer.py | test_local_renderer.py | VERIFIED |
| FR-VD-02 | Editor standard passes | E-004 | T-013 | pipeline/editor_passes.py | test_editor_passes.py | VERIFIED |
| FR-VD-03 | Hyperframe Thai overlay | E-004 | T-014 | pipeline/hyperframe.py | test_hyperframe.py | VERIFIED |
| FR-VD-04 | Editor budget cap + fallback | E-004 | T-015 | pipeline/editor_budget.py | test_editor_budget.py | VERIFIED |
| FR-VD-05 | TTS provider whitelist | E-004 | T-016 | adapters/tts.py | test_tts.py | VERIFIED |
| FR-PB-01 | IG Reels publish | E-005 | T-017 | adapters/publisher.py | test_publisher_adapter.py | VERIFIED |
| FR-PB-02 | FB Reels + YT Shorts | E-005 | T-018, T-048, T-049 | adapters/publisher.py | test_publisher_multiplatform.py | VERIFIED |
| FR-PB-03 | subId taxonomy on links | E-005 | T-019 | adapters/shopee_subids.py | test_shopee_subids.py | VERIFIED |
| FR-PB-04 | Ad disclosure in caption | E-005 | T-020 | agents/caption_builder.py | test_caption_builder.py | VERIFIED |
| FR-PB-05 | Wiki-driven posting time | E-005 | T-021 | agents/posting_scheduler.py | test_posting_scheduler.py | VERIFIED |
| FR-AN-01 | Metrics polling schedule | E-006 | T-022 | agents/analytics_collector.py | test_analytics_collector.py | VERIFIED |
| FR-AN-02 | Full metrics recording | E-006 | T-023 | schemas/metrics.py | test_metrics.py | VERIFIED |
| FR-AN-03 | Click-conversion attribution | E-006 | T-024 | schemas/metrics.py (ConversionReport) | test_conversion.py | VERIFIED |
| FR-FB-01 | Feedback Curator nightly | E-007 | T-025 | wiki/review_queue.py | test_wiki_review.py | VERIFIED |
| FR-FB-02 | Wiki tier system | E-007 | T-026 | wiki/tier_promoter.py, wiki/entry.py | test_tier_promoter.py | VERIFIED |
| FR-FB-03 | Bilateral sync | E-007 | T-027 | wiki/store.py | test_wiki_store.py | VERIFIED |
| FR-FB-04 | Offline replay | E-007 | T-028 | wiki/replay.py | test_replay.py | VERIFIED |
| FR-SF-01 | Pre-publish safety gates | E-008 | T-029 | agents/safety_gate.py | test_safety_gate.py | VERIFIED |
| FR-SF-02 | Music license check | E-008 | T-030 | agents/music_license.py | test_music_license.py | VERIFIED |
| FR-SF-03 | Ad disclosure enforcement | E-008 | T-031 | agents/caption_builder.py | test_caption_builder.py | VERIFIED |
| FR-SF-04 | Kill switch (multi-level) | E-008 | T-032, T-054 | agents/kill_switch.py, adapters/publisher.py | test_kill_switch.py, test_publisher_approval_gate.py | VERIFIED |
| FR-SF-05 | Auto-kill on 3 violations | E-008 | T-033 | agents/kill_switch.py | test_kill_switch.py | VERIFIED |
| FR-OR-01 | Five Temporal workflows | E-009 | T-034 | workflows/definitions.py | test_workflows.py | VERIFIED |
| FR-OR-02 | Idempotent activities | E-009 | T-035 | workflows/handlers.py | test_workflow_handlers.py | VERIFIED |
| FR-OR-03 | Budget cap circuit-breaker | E-009 | T-036 | workflows/budget.py | test_budget.py | VERIFIED |
| FR-OC-01 | Ops dashboard | E-010 | T-044, T-045, T-046 | ops/console/app.py, ops/console/server.py | test_ops_console.py | VERIFIED |
| FR-OC-02 | Manual approve/reject | E-010 | T-038 | ops/produce.py, agents/production_director.py | test_production_director.py | VERIFIED |

### Sprint 10 additions (MANUAL mode prep)

| REQ ID | Description | Epic | Task(s) | Source File(s) | Test(s) | Status |
|--------|-------------|------|---------|----------------|---------|--------|
| FR-QW-07 | Human approval gate on Publisher | E-008 | T-054 | adapters/publisher.py (HumanApprovalGatePublisher) | test_publisher_approval_gate.py | VERIFIED |
| FR-QW-08a | LLM-driven perfect storyboard | E-003 | T-055 | agents/writers_room.py (LLM path) | test_writers_room_llm.py | VERIFIED |
| FR-QW-09 | Deploy cron scheduler | E-013 | T-056 | scripts/deploy-cron.sh | (manual verification) | IMPLEMENTED |
| FR-QW-10 | Monitoring lite JSONL exporter | E-010 | T-057 | ops/metrics_export.py | test_metrics_export.py | VERIFIED |

## Non-Functional Requirements

| REQ ID | Description | Task(s) | Verification Method | Status |
|--------|-------------|---------|---------------------|--------|
| NFR-PF-01 | Video latency P50 < 90min | -- | Temporal metrics | NOT_STARTED (needs live ops) |
| NFR-PF-02 | Metrics lag < 5 min | T-022 | Polling schedule test | VERIFIED (dry-run) |
| NFR-PF-03 | Prompt cache >= 70% | -- | Langfuse dashboard | NOT_STARTED (needs live ops) |
| NFR-RL-01 | Pipeline success >= 90% P1 | -- | Success rate monitor | NOT_STARTED (needs live ops) |
| NFR-CS-01 | Cost/video <= $3.32 P1 | T-015 | EditorBudgetTracker | VERIFIED (unit test) |
| NFR-SC-01 | 5 videos/day P1 | -- | Daily count monitor | NOT_STARTED (needs live ops) |
| NFR-SEC-01 | Secrets in Vault/SOPS | T-052 | dev-setup.sh checks | IMPLEMENTED |
| NFR-OB-01 | OTel 100% coverage | -- | Trace analysis | NOT_STARTED |
| NFR-MT-02 | Test coverage >= 70% | -- | pytest-cov report | VERIFIED (80% coverage) |

---

## Coverage Summary

| Category | Total | NOT_STARTED | IN_PROGRESS | IMPLEMENTED | VERIFIED |
|----------|-------|-------------|-------------|-------------|----------|
| FR-* | 42 | 0 | 0 | 1 | 41 |
| NFR-* | 9 | 4 | 0 | 1 | 4 |
| **Total** | **51** | **4** | **0** | **2** | **45** |

> 41/42 functional requirements VERIFIED with passing tests (605 unit tests, 80% coverage).
> 4 NFR items require live production data (blocked on vendor credential onboarding).
> Sprint 10 added 4 new QW-track requirements, 3 already VERIFIED.
