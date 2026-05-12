# Software Requirements Specification — Auto-Affi

- **Project**: Auto-Affi
- **PM**: Nick Fury (aegis-team)
- **Compliance**: ISO 29110 Basic guideline
- **Linked**: `SPEC.md` (full design), `docs/pm/sow.md` (scope)
- **Last updated**: 2026-05-12

> Requirement IDs ใช้สำหรับ traceability matrix ภายหลัง (`docs/si/traceability-matrix.md` — Tier 2)

---

## 1. Functional Requirements

### 1.1 Product Discovery (Scout)
| ID | Requirement | Priority | Acceptance |
|---|---|---|---|
| FR-SC-01 | ระบบต้องค้นหา product จาก Shopee Open API (GraphQL `productOfferV2`) ตาม keyword + category + min commission | MUST | คืน ≥ 1 product พร้อม commission %, price, rating |
| FR-SC-02 | ระบบต้อง score product ด้วย rubric ใน `execution-playbook.md` §5.2 | MUST | output score 0-100 พร้อม reasoning string |
| FR-SC-03 | ระบบต้อง filter restricted categories (medical, supplements, replica) ออกอัตโนมัติ | MUST | hard reject log entry, ไม่ปรากฏใน candidates |
| FR-SC-04 | ระบบต้อง query LLM Wiki เพื่อหลีกเลี่ยง saturated / anti-pattern product ก่อน promote | MUST | candidate list หลังกรอง saturation ลด ≥ 30% เทียบ raw |

### 1.2 Strategy
| ID | Requirement | Priority | Acceptance |
|---|---|---|---|
| FR-ST-01 | Strategist ต้องสร้าง CampaignBrief พร้อม fields: product_id, persona, angle, hook, cta, hypothesis, expected_ctr | MUST | JSON ตรง schema, fields ครบ |
| FR-ST-02 | Strategist ต้อง query Wiki canonical rules ก่อน reasoning (RAG) | MUST | retrieval log มี ≥ 5 entries / call |
| FR-ST-03 | ระบบต้อง prioritize mega-sale calendar (3.3, 6.6, 9.9, 10.10, 11.11, 12.12) ถ้า ≤ 14 วันก่อน sale | MUST | brief.priority_boost = true, budget × 2 |

### 1.3 Writers' Room
| ID | Requirement | Priority | Acceptance |
|---|---|---|---|
| FR-WR-01 | Phase 1: 1 Writer agent สร้าง Storyboard JSON ตาม schema ใน `SPEC.md` §6.2 | MUST | schema-validated, ≤ 60s total duration |
| FR-WR-02 | Phase 2: Writers' Room ครบ 6 sub-agents (Director, Screenwriter, Cinematographer, Storyboard Artist, Sound Designer, Critic) | MUST | Director สรุป final decision, Critic ตรวจก่อน promote |
| FR-WR-03 | Storyboard ต้องระบุ hook ≤ 2 วินาที + avg shot 1.5-2.5s + audio drop position 40-60% | MUST | ตรวจ schema field by field |
| FR-WR-04 | Script ต้องเป็นภาษาไทย, no medical/whitening/guarantee claims | MUST | Critic + Typhoon verifier pass |

### 1.4 Video Production (Editor + Producer)
| ID | Requirement | Priority | Acceptance |
|---|---|---|---|
| FR-VD-01 | ระบบต้องสร้าง 9:16 master video 1080×1920, 30fps, ≤ 60s, ≤ 100MB | MUST | ffprobe verify metadata |
| FR-VD-02 | Editor ต้องรัน standard passes: silence_trim, filler_cut (เออ/อืม/อะ/อ่า), auto_subtitle, hook_punch_in, brand_overlay, cta_endcard | MUST | passes ครบใน log ของแต่ละ video |
| FR-VD-03 | Hyperframe overlay สำหรับ Thai text (no Thai text rendered by image/video model) | MUST | PaddleOCR Thai check ≥ 99% accuracy บนตัวอักษรใน video |
| FR-VD-04 | Editor budget cap $0.40 / video; fallback FFmpeg recipe ถ้า exceed | MUST | cost log < cap, ไม่ก็ trigger fallback |
| FR-VD-05 | TTS = ElevenLabs Multilingual v2 (primary), Botnoi (regional), Azure (fallback) — ห้าม OpenAI TTS | MUST | TTS provider log = whitelist only |

### 1.5 Publishing
| ID | Requirement | Priority | Acceptance |
|---|---|---|---|
| FR-PB-01 | Phase 1: publish ไป IG Reels ผ่าน Meta Graph API | MUST | media id returned, video appears on profile |
| FR-PB-02 | Phase 2: เพิ่ม FB Reels + YouTube Shorts | MUST | per-platform PublishRecord persisted |
| FR-PB-03 | ทุก video ต้องผูก subId taxonomy: `[platform, account_handle, video_id, campaign_id, variant]` | MUST | Shopee deep link มี subIds[0-4] ครบ |
| FR-PB-04 | Caption ต้องมี `#โฆษณา` + AI label ตาม TikTok 2025 rule | MUST | text scan pass |
| FR-PB-05 | Posting time เลือกตาม Wiki "optimal time" per platform per niche | MUST | scheduler reads from Wiki |

### 1.6 Analytics
| ID | Requirement | Priority | Acceptance |
|---|---|---|---|
| FR-AN-01 | Poll metrics ทุก 1h / 6h / 24h / 7d / 30d ต่อ published video | MUST | Temporal schedule active, lag < 5 min |
| FR-AN-02 | บันทึก views, likes, shares, saves, comments, avg_watch_pct, ctr, conversions, gmv_thb | MUST | metrics_timeseries รวมครบ |
| FR-AN-03 | Click→Conversion attribution ผ่าน subId join | MUST | Shopee conversionReport joined to video_id |

### 1.7 Feedback / Learning (LLM Wiki)
| ID | Requirement | Priority | Acceptance |
|---|---|---|---|
| FR-FB-01 | Feedback Curator รัน nightly: label outcome (breakout/hit/neutral/flop/banned), extract patterns | MUST | wiki_entries เพิ่มขึ้น weekly |
| FR-FB-02 | Wiki ใช้ tier system: Hypothesis → Validated → Canonical → Deprecated (Phase 2+) | SHOULD | tier field populated |
| FR-FB-03 | Bilateral sync: agent เขียนเข้า review queue เท่านั้น, Safety promote → canonical | MUST | direct canonical write ไม่มีใน audit log |
| FR-FB-04 | Offline replay weekly: เปรียบเทียบ wiki ใหม่ vs canonical exemplar | MUST | replay report สรุป divergence |

### 1.8 Safety
| ID | Requirement | Priority | Acceptance |
|---|---|---|---|
| FR-SF-01 | Pre-publish: claim-auditor (no medical/financial/guarantee claim), brand-list block, image safety NSFW check | MUST | pass before PublishRecord create |
| FR-SF-02 | Music license validation (licensed library only) | MUST | music_id ∈ licensed list |
| FR-SF-03 | Disclosure: บังคับ `#โฆษณา` หรือ `ได้รับค่าตอบแทน` ต่อ caption | MUST | caption scan pass |
| FR-SF-04 | Kill switch: per-product / per-campaign / per-platform / global ผ่าน ops console | MUST | API endpoint + Linear issue trigger ทำงาน |
| FR-SF-05 | Auto-kill: 3 platform policy violation ใน 24h → freeze pipeline | MUST | safety_event log → kill action |

### 1.9 Orchestration (Temporal)
| ID | Requirement | Priority | Acceptance |
|---|---|---|---|
| FR-OR-01 | Workflows: DiscoveryWorkflow / CampaignWorkflow / PublishWorkflow / MetricsWorkflow / LearningWorkflow | MUST | all workflows registered, schedulable |
| FR-OR-02 | Idempotent activities; retry safe with checkpoint | MUST | duplicate run ไม่ทำให้ data ซ้ำ |
| FR-OR-03 | Per-node token + step budget cap | MUST | exceed → trigger circuit-breaker |

### 1.10 Ops Console
| ID | Requirement | Priority | Acceptance |
|---|---|---|---|
| FR-OC-01 | Internal dashboard แสดง: candidate queue, campaign status, video preview, metrics, kill switches | MUST | accessible via auth |
| FR-OC-02 | Manual approve/reject ของ brief หลัง low-confidence | SHOULD | button + audit log |

---

## 2. Non-Functional Requirements

| ID | Type | Requirement | Target |
|---|---|---|---|
| NFR-PF-01 | Performance | Brief → published video latency P50 / P95 | < 90 min / < 6 h |
| NFR-PF-02 | Performance | Metrics polling lag | < 5 min |
| NFR-PF-03 | Performance | Cache hit rate (prompt caching) | ≥ 70% หลัง warmup |
| NFR-RL-01 | Reliability | Pipeline success rate (Phase 1) | ≥ 90% |
| NFR-RL-02 | Reliability | Pipeline success rate (Phase 3) | ≥ 95% |
| NFR-RL-03 | Reliability | RTO (recovery time) after region outage | < 2 h |
| NFR-RL-04 | Reliability | RPO (data loss) | ≤ 24 h |
| NFR-CS-01 | Cost | Cost / video (Phase 1) | ≤ $3.32 |
| NFR-CS-02 | Cost | Cost / video (Phase 3 target) | ≤ $0.80 |
| NFR-CS-03 | Cost | Daily Opus spend cap | $50 |
| NFR-SC-01 | Scale | Videos / day (Phase 1) | 5 |
| NFR-SC-02 | Scale | Videos / day (Phase 3) | 75 |
| NFR-SC-03 | Scale | Concurrent campaigns | 50 (Phase 1), 500 (Phase 3) |
| NFR-SEC-01 | Security | Secrets ใน Vault / SOPS, no env-file commit | 100% compliance |
| NFR-SEC-02 | Security | API key rotation cadence | 90 วัน |
| NFR-SEC-03 | Security | All agent → external API ผ่าน egress proxy allowlist | enforced |
| NFR-PR-01 | Privacy | ไม่เก็บ PII จาก click event (เก็บแค่ ua_hash + geo region) | enforced |
| NFR-PR-02 | Privacy | Asset retention hot 90d, archive cold | enforced |
| NFR-PR-03 | Privacy | PDPC compliance (no email/phone collected via affiliate funnel) | 100% |
| NFR-CP-01 | Compliance | OCPB disclosure `#โฆษณา` on 100% video | 100% |
| NFR-CP-02 | Compliance | TikTok/IG/YT ToS — no visual product alteration, no fake urgency, no recycled watermark | 100% |
| NFR-CP-03 | Compliance | Direct Marketing License — register if revenue ≥ THB 1.5M (proactive) | trigger |
| NFR-OB-01 | Observability | OpenTelemetry trace coverage on every agent call + tool call | 100% |
| NFR-OB-02 | Observability | Langfuse retention | ≥ 30 วัน |
| NFR-OB-03 | Observability | Cost dashboard accuracy | ± 5% vs invoice |
| NFR-MT-01 | Maintainability | Schema-validated handoff every agent boundary | 100% |
| NFR-MT-02 | Maintainability | Test coverage on adapters + workflows | ≥ 70% |

---

## 3. Interface Requirements

### 3.1 External
| ID | Interface | Notes |
|---|---|---|
| IR-01 | Shopee Open API (GraphQL) | HMAC SHA256 sig, ~1 req/sec rate, subIds[0-4] |
| IR-02 | Anthropic Messages API | Opus 4.7 / Sonnet 4.6 / Haiku 4.5 with prompt caching + extended thinking |
| IR-03 | kie.ai gateway | Primary route สำหรับ Veo/Sora/Flux/Runway/Suno/MJ |
| IR-04 | ElevenLabs API | Multilingual v2, voice cloning |
| IR-05 | Botnoi Voice API | Regional Thai accents |
| IR-06 | Meta Graph API | FB+IG Content Publishing API |
| IR-07 | YouTube Data API v3 | Shorts upload, OAuth refresh |
| IR-08 | TikTok Research API | Trend signals (pending app approval) |
| IR-09 | phaya.io | Media transcoding (PDPA-sensitive route) |

### 3.2 Internal
| ID | Interface | Notes |
|---|---|---|
| IR-10 | Agent ↔ Tool MCP | JSON `{ok, data, cost_usd, latency_ms, trace_id}` standard |
| IR-11 | Temporal Activities | All idempotent, schema-validated input/output |
| IR-12 | Wiki retrieval RAG | pgvector + Mem0 (Phase 2) |

---

## 4. Data Requirements
| ID | Requirement |
|---|---|
| DR-01 | Postgres schema ตาม `SPEC.md` §6.1 — ทุก table มี `created_at`, `updated_at` |
| DR-02 | pgvector dims = 1536 (text-embedding-3-small) หรือ Claude embeddings เมื่อพร้อม |
| DR-03 | ClickHouse สำหรับ metrics_timeseries (high-volume time-series) |
| DR-04 | S3 (R2) สำหรับ asset + master video |
| DR-05 | Backup: daily Postgres + S3 snapshot, 30-day retention |

---

## 5. Constraints
| ID | Constraint |
|---|---|
| C-01 | Compliance mode = guideline (ไม่ audit-ready) |
| C-02 | Project tracking ทำใน Linear (aegis-team workspace) |
| C-03 | ห้าม commit secret ลง git |
| C-04 | ห้ามใช้ Helicone (maintenance mode) |
| C-05 | ห้าม peer-to-peer agent call (strict hierarchy only) |
| C-06 | ห้าม direct wiki write จาก agent (bilateral sync only) |
| C-07 | Thai content only (Phase 1-3) |
| C-08 | ใช้ commercial models ผ่าน kie.ai (no custom training Phase 1-3) |

---

## 6. Glossary
ดู `SPEC.md` §16

---

## 7. Verification Method
ทุก requirement = 1 line entry ใน traceability matrix (`docs/si/traceability-matrix.md` Tier 2) → mapped กับ design + test case + verification record
