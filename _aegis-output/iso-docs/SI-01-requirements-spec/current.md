# SI.01 Requirements Specification -- Auto-Affi

> Adapted from `docs/si/srs.md` (ISO 29110 guideline-mode).
> This is the AEGIS BLOCK 0 canonical copy.

- **Project**: Auto-Affi
- **PM**: Nick Fury (aegis-team)
- **Compliance**: ISO/IEC 29110 Basic (guideline)
- **Source**: `docs/si/srs.md` + `SPEC.md`
- **Created**: 2026-05-13

---

## 1. Functional Requirements

### 1.1 Product Discovery (Scout)

| ID | Requirement | Priority | Acceptance |
|----|-------------|----------|------------|
| FR-SC-01 | Search products from Shopee Open API (GraphQL productOfferV2) by keyword + category + min commission | MUST | Returns >= 1 product with commission %, price, rating |
| FR-SC-02 | Score products with rubric (execution-playbook S5.2) | MUST | Output score 0-100 with reasoning string |
| FR-SC-03 | Filter restricted categories (medical, supplements, replica) automatically | MUST | Hard reject log entry, filtered from candidates |
| FR-SC-04 | Query LLM Wiki to avoid saturated/anti-pattern products before promote | MUST | Candidate list after saturation filter reduced >= 30% vs raw |

### 1.2 Strategy

| ID | Requirement | Priority | Acceptance |
|----|-------------|----------|------------|
| FR-ST-01 | Strategist creates CampaignBrief with required fields | MUST | JSON matches schema, all fields populated |
| FR-ST-02 | Strategist queries Wiki canonical rules before reasoning (RAG) | MUST | Retrieval log has >= 5 entries/call |
| FR-ST-03 | Prioritize mega-sale calendar (3.3, 6.6, 9.9, 10.10, 11.11, 12.12) if <= 14 days before sale | MUST | brief.priority_boost = true, budget x 2 |

### 1.3 Writers' Room

| ID | Requirement | Priority | Acceptance |
|----|-------------|----------|------------|
| FR-WR-01 | Phase 1: 1 Writer agent creates Storyboard JSON per schema (SPEC.md S6.2) | MUST | Schema-validated, <= 60s total duration |
| FR-WR-02 | Phase 2: Full Writers' Room (6 sub-agents) | MUST | Director final decision, Critic pre-promote review |
| FR-WR-03 | Storyboard: hook <= 2s + avg shot 1.5-2.5s + audio drop 40-60% | MUST | Schema field validation |
| FR-WR-04 | Script in Thai, no medical/whitening/guarantee claims | MUST | Critic + Typhoon verifier pass |

### 1.4 Video Production

| ID | Requirement | Priority | Acceptance |
|----|-------------|----------|------------|
| FR-VD-01 | 9:16 master video 1080x1920, 30fps, <= 60s, <= 100MB | MUST | ffprobe verify metadata |
| FR-VD-02 | Editor standard passes: silence_trim, filler_cut, auto_subtitle, hook_punch_in, brand_overlay, cta_endcard | MUST | All passes logged per video |
| FR-VD-03 | Hyperframe overlay for Thai text (not rendered by image/video model) | MUST | PaddleOCR Thai check >= 99% accuracy |
| FR-VD-04 | Editor budget cap $0.40/video; fallback FFmpeg recipe if exceeded | MUST | Cost log < cap or fallback triggered |
| FR-VD-05 | TTS: ElevenLabs (primary), Botnoi (regional), Azure (fallback) -- no OpenAI TTS | MUST | TTS provider log = whitelist only |

### 1.5 Publishing

| ID | Requirement | Priority | Acceptance |
|----|-------------|----------|------------|
| FR-PB-01 | Phase 1: publish to IG Reels via Meta Graph API | MUST | media_id returned, video on profile |
| FR-PB-02 | Phase 2: add FB Reels + YouTube Shorts | MUST | Per-platform PublishRecord persisted |
| FR-PB-03 | Every video has subId taxonomy [platform, account, video_id, campaign_id, variant] | MUST | Shopee deep link has subIds[0-4] complete |
| FR-PB-04 | Caption includes #Ad disclosure + AI label per TikTok 2025 rule | MUST | Text scan pass |
| FR-PB-05 | Posting time from Wiki "optimal time" per platform per niche | MUST | Scheduler reads from Wiki |

### 1.6 Analytics

| ID | Requirement | Priority | Acceptance |
|----|-------------|----------|------------|
| FR-AN-01 | Poll metrics at 1h/6h/24h/7d/30d per published video | MUST | Temporal schedule active, lag < 5 min |
| FR-AN-02 | Record views, likes, shares, saves, comments, avg_watch_pct, ctr, conversions, gmv_thb | MUST | metrics_timeseries complete |
| FR-AN-03 | Click-to-conversion attribution via subId join | MUST | Shopee conversionReport joined to video_id |

### 1.7 Feedback / Learning (LLM Wiki)

| ID | Requirement | Priority | Acceptance |
|----|-------------|----------|------------|
| FR-FB-01 | Feedback Curator nightly: label outcome, extract patterns | MUST | wiki_entries increase weekly |
| FR-FB-02 | Wiki tier system: Hypothesis -> Validated -> Canonical -> Deprecated | SHOULD | Tier field populated |
| FR-FB-03 | Bilateral sync: agents write to review queue only, Safety promotes to canonical | MUST | No direct canonical writes in audit log |
| FR-FB-04 | Offline replay weekly: compare new wiki vs canonical exemplar | MUST | Replay report summarizes divergence |

### 1.8 Safety

| ID | Requirement | Priority | Acceptance |
|----|-------------|----------|------------|
| FR-SF-01 | Pre-publish: claim-auditor + brand-list block + NSFW check | MUST | Pass before PublishRecord create |
| FR-SF-02 | Music license validation (licensed library only) | MUST | music_id in licensed list |
| FR-SF-03 | Disclosure: #Ad required per caption | MUST | Caption scan pass |
| FR-SF-04 | Kill switch: per-product/campaign/platform/global via ops console | MUST | API + Linear trigger works |
| FR-SF-05 | Auto-kill: 3 policy violations in 24h -> freeze pipeline | MUST | safety_event -> kill action |

### 1.9 Orchestration (Temporal)

| ID | Requirement | Priority | Acceptance |
|----|-------------|----------|------------|
| FR-OR-01 | Five workflows: Discovery/Campaign/Publish/Metrics/Learning | MUST | All registered, schedulable |
| FR-OR-02 | Idempotent activities with checkpoint | MUST | Duplicate run produces no data duplication |
| FR-OR-03 | Per-node token + step budget cap | MUST | Exceed triggers circuit-breaker |

### 1.10 Ops Console

| ID | Requirement | Priority | Acceptance |
|----|-------------|----------|------------|
| FR-OC-01 | Dashboard: candidate queue, campaign status, video preview, metrics, kill switches | MUST | Accessible via auth |
| FR-OC-02 | Manual approve/reject for low-confidence briefs | SHOULD | Button + audit log |

---

## 2. Non-Functional Requirements

| ID | Type | Requirement | Target |
|----|------|-------------|--------|
| NFR-PF-01 | Performance | Brief to published video latency P50/P95 | < 90 min / < 6 h |
| NFR-PF-02 | Performance | Metrics polling lag | < 5 min |
| NFR-PF-03 | Performance | Cache hit rate (prompt caching) | >= 70% after warmup |
| NFR-RL-01 | Reliability | Pipeline success rate (Phase 1) | >= 90% |
| NFR-RL-02 | Reliability | Pipeline success rate (Phase 3) | >= 95% |
| NFR-RL-03 | Reliability | RTO after region outage | < 2 h |
| NFR-RL-04 | Reliability | RPO | <= 24 h |
| NFR-CS-01 | Cost | Cost/video Phase 1 | <= $3.32 |
| NFR-CS-02 | Cost | Cost/video Phase 3 | <= $0.80 |
| NFR-CS-03 | Cost | Daily Opus spend cap | $50 |
| NFR-SC-01 | Scale | Videos/day Phase 1 | 5 |
| NFR-SC-02 | Scale | Videos/day Phase 3 | 75 |
| NFR-SC-03 | Scale | Concurrent campaigns | 50 (P1), 500 (P3) |
| NFR-SEC-01 | Security | Secrets in Vault/SOPS, no env-file commit | 100% |
| NFR-SEC-02 | Security | API key rotation cadence | 90 days |
| NFR-SEC-03 | Security | Agent external API via egress proxy allowlist | Enforced |
| NFR-PR-01 | Privacy | No PII from click events | Enforced |
| NFR-PR-02 | Privacy | Asset retention: hot 90d, cold archive | Enforced |
| NFR-PR-03 | Privacy | PDPC compliance | 100% |
| NFR-CP-01 | Compliance | OCPB disclosure #Ad on 100% video | 100% |
| NFR-CP-02 | Compliance | TikTok/IG/YT ToS compliance | 100% |
| NFR-CP-03 | Compliance | Direct Marketing License trigger | At THB 1.5M |
| NFR-OB-01 | Observability | OTel trace coverage on every agent+tool call | 100% |
| NFR-OB-02 | Observability | Langfuse retention | >= 30 days |
| NFR-OB-03 | Observability | Cost dashboard accuracy | +/- 5% vs invoice |
| NFR-MT-01 | Maintainability | Schema-validated handoff at every agent boundary | 100% |
| NFR-MT-02 | Maintainability | Test coverage on adapters + workflows | >= 70% |

---

## 3. Interface Requirements

### 3.1 External Interfaces

| ID | Interface | Notes |
|----|-----------|-------|
| IR-01 | Shopee Open API (GraphQL) | HMAC SHA256 sig, ~1 req/sec, subIds[0-4] |
| IR-02 | Anthropic Messages API | Opus 4.7 / Sonnet 4.6 / Haiku 4.5 + prompt caching + extended thinking |
| IR-03 | kie.ai gateway | Veo/Sora/Flux/Runway/Suno/MJ |
| IR-04 | ElevenLabs API | Multilingual v2, voice cloning |
| IR-05 | Botnoi Voice API | Regional Thai accents |
| IR-06 | Meta Graph API | FB+IG Content Publishing |
| IR-07 | YouTube Data API v3 | Shorts upload, OAuth refresh |
| IR-08 | TikTok Research API | Trend signals (pending approval) |
| IR-09 | phaya.io | Media transcoding |

### 3.2 Internal Interfaces

| ID | Interface | Notes |
|----|-----------|-------|
| IR-10 | Agent-Tool MCP | JSON {ok, data, cost_usd, latency_ms, trace_id} |
| IR-11 | Temporal Activities | Idempotent, schema-validated I/O |
| IR-12 | Wiki retrieval RAG | pgvector + Mem0 (Phase 2) |

---

## 4. Data Requirements

| ID | Requirement |
|----|-------------|
| DR-01 | Postgres schema per SPEC.md S6.1 -- all tables have created_at, updated_at |
| DR-02 | pgvector dims = 1536 (text-embedding-3-small) |
| DR-03 | ClickHouse for metrics_timeseries |
| DR-04 | S3 (R2) for assets + master video |

---

## Requirement Summary

| Category | Count | MUST | SHOULD |
|----------|-------|------|--------|
| Functional (FR-*) | 37 | 35 | 2 |
| Non-Functional (NFR-*) | 27 | 27 | 0 |
| Interface (IR-*) | 12 | 12 | 0 |
| Data (DR-*) | 4 | 4 | 0 |
| **Total** | **80** | **78** | **2** |
