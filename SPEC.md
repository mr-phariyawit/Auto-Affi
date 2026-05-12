# Auto-Affi — AI Marketing Platform Specification

> ระบบ AI agent crew ที่ทำงาน 24/7 เพื่อค้น product จาก Shopee มาทำ affiliate, วิเคราะห์ viral trends, สร้าง storyboard + premium 9:16 video, publish ไป FB / IG / YouTube Shorts, เก็บ metrics, แล้ว self-learn ผ่าน LLM Wiki

- **Version**: 0.1.0 (draft)
- **Status**: Specification — pre-implementation
- **Owner**: TBD
- **Last updated**: 2026-05-12

---

## 1. Vision & Goals

### 1.1 Vision
สร้าง "AI Marketing Company" ที่ทำงาน autonomous 24/7 — ตั้งแต่หา product, คิด strategy, เขียนบท, สร้างวิดีโอ premium ระดับ Hollywood แนวตั้ง 9:16, publish ลง social, วัดผล, แล้วเรียนรู้จากความสำเร็จ/ล้มเหลวของตัวเองเพื่อปรับปรุงรอบถัดไป — โดยมนุษย์เป็นเพียง supervisor

### 1.2 Goals (เชิงปริมาณ)
| KPI | Target Phase 1 | Target Phase 3 |
|---|---|---|
| Videos produced / day | 5 | 100+ |
| Cost / video (full pipeline) | ≤ $3 | ≤ $0.80 |
| Avg CTR on affiliate link | ≥ 1.5% | ≥ 4% |
| Affiliate GMV / month | $1k | $50k+ |
| Human intervention rate | ≤ 30% | ≤ 5% |
| Strategy improvement / month (CTR uplift) | — | ≥ 5% MoM |

### 1.3 Non-Goals
- ไม่ใช่ creator marketplace (ไม่มีมนุษย์ creator ใน loop)
- ไม่ทำ paid ads ในเฟสแรก (organic-only)
- ไม่ทำ multi-tenant SaaS ใน Phase 1

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Orchestrator (Temporal)                   │
│   schedule · retries · DAG · long-running workflows · timers    │
└──────┬──────────┬──────────┬──────────┬──────────┬──────────────┘
       │          │          │          │          │
   ┌───▼──┐  ┌───▼───┐  ┌───▼───┐  ┌───▼────┐ ┌───▼──────┐
   │Scout │  │Trend  │  │Strat- │  │Writers │ │Publisher │
   │Agent │  │Analyst│  │egist  │  │Room    │ │Agent     │
   └───┬──┘  └───┬───┘  └───┬───┘  └───┬────┘ └───┬──────┘
       │         │          │          │          │
       └────┬────┴────┬─────┴────┬─────┴────┬─────┘
            │         │          │          │
        ┌───▼─────────▼──────────▼──────────▼────┐
        │   Shared Context Bus (Postgres + Redis)│
        └───┬─────────────────────────────────┬──┘
            │                                 │
   ┌────────▼─────────┐               ┌───────▼──────────┐
   │   LLM Wiki       │◄──────────────│ Feedback Curator │
   │ (pgvector + KG)  │   patterns    │   Agent          │
   └──────────────────┘               └───────▲──────────┘
                                              │
                                       ┌──────┴───────┐
                                       │ Analytics    │
                                       │ Collector    │
                                       └──────▲───────┘
                                              │
                              ┌───────────────┴──────────────┐
                              │  Meta / IG / YouTube APIs    │
                              │  + Shopee Affiliate API      │
                              └──────────────────────────────┘
```

### 2.1 Subsystems
1. **Agent Crew** — Claude-based agents แต่ละตัวมี role / tools / memory ของตัวเอง
2. **Orchestrator** — Temporal Workflows คุม pipeline แบบ durable, retry-safe, long-running
3. **Asset Pipeline** — image gen + video gen + TTS + lipsync + composition
4. **Data Plane** — Postgres (OLTP) + pgvector (semantic) + S3 (assets) + ClickHouse (analytics)
5. **Publishing Plane** — Meta Graph API, IG Content Publishing API, YouTube Data API v3
6. **Learning Loop** — Feedback Curator → LLM Wiki → context injection ใน next-run

---

## 3. Agent Crew (Hollywood-grade)

แต่ละ agent = Claude (Opus 4.7 สำหรับ reasoning-heavy / Sonnet 4.6 สำหรับ throughput) ที่มี system prompt + tool set + memory namespace ของตัวเอง

### 3.1 Product Scout Agent
- **Role**: ค้น product จาก Shopee ที่มี viral potential + commission ดี
- **Inputs**: trending keywords จาก Trend Analyst, ประวัติ win/fail จาก LLM Wiki
- **Tools**:
  - `shopee.search_products(keyword, category, min_commission)`
  - `shopee.get_product_details(item_id)`
  - `shopee.get_affiliate_link(item_id)`
  - `wiki.query_similar_products(embedding)`
- **Outputs**: `ProductCandidate` (10–50 ต่อรอบ) พร้อม score
- **Scoring rubric**: price band, commission %, rating, sales velocity, review sentiment, novelty vs. saturated wiki

### 3.2 Trend Analyst Agent
- **Role**: ขุด viral signal จาก TikTok / Reels / Shorts / Threads
- **Tools**:
  - `tiktok.search_trending(region=TH)`
  - `youtube.shorts_trending()`
  - `meta.reels_insights()` (limited)
  - `web.scrape(url)` (rate-limited, ToS-compliant)
- **Outputs**: `TrendSignal { hook_pattern, audio_id, hashtags, format, lifecycle_phase }`
- **Cadence**: ทุก 6 ชม.

### 3.3 Strategist Agent
- **Role**: matchmaker — เอา product ↔ trend ↔ audience persona มาประกบเป็น campaign brief
- **Outputs**: `CampaignBrief { product_id, target_persona, angle, hook, cta, success_hypothesis, expected_ctr }`
- **Critical**: ต้อง query LLM Wiki หา *anti-patterns* ก่อนยืนยัน

### 3.4 Writers' Room (Multi-agent panel)
จำลอง Hollywood writers room — รันแบบ debate แล้วให้ Director ตัดสินใจ

| Sub-agent | Role |
|---|---|
| **Director** | กำหนด tone, pacing, emotional arc — final decision authority |
| **Screenwriter** | เขียนบทพูด / dialogue / VO script (ภาษาไทย-native), ≤ 60 วินาที |
| **Cinematographer** | ออกแบบ shot list, framing 9:16, lighting, b-roll cues |
| **Storyboard Artist** | สร้าง storyboard JSON + reference image prompts ต่อ scene |
| **Sound Designer** | เลือก music bed (royalty-free / licensed), SFX, voice characteristics |
| **Critic** | red-team — หาจุดอ่อน, brand-risk, claim compliance, repetitive patterns |

**Output**: `Storyboard` schema (ดู §6.2)

### 3.5 Producer Agent (Asset Pipeline Orchestrator)
- ตัดสินใจว่าแต่ละ scene จะใช้ generator ตัวไหน (Veo 3 / Runway Gen-3 / Kling / stock + Ken Burns)
- เลือก voice (ElevenLabs / Azure / OpenAI TTS), apply lipsync (Sync.so / Wav2Lip) ถ้าจำเป็น
- Compose ผ่าน FFmpeg pipeline → master 9:16 1080×1920, 30fps, ≤ 60s, ≤ 100MB

### 3.6 Publisher Agent
- เลือก optimal posting time per platform (จาก Wiki)
- สร้าง caption / hashtags / first-comment per platform
- ผูก affiliate link ผ่าน link-shortener ของระบบเอง (เพื่อ track cross-platform)
- Schedule + post + บันทึก `PublishRecord`

### 3.7 Analytics Collector Agent
- Poll metrics ทุก 1h / 6h / 24h / 7d / 30d
- รวบ views, likes, shares, saves, comments, watch-time, click-through, conversions, GMV
- เก็บใน ClickHouse + Postgres `metrics_timeseries`

### 3.8 Feedback Curator Agent
- รัน batch ทุก 24 ชม.
- เปรียบเทียบ win (top 20%) vs. fail (bottom 20%) cohort
- Extract structured patterns → write เป็น `WikiEntry` ใหม่ + update embeddings
- Mark stale patterns เป็น deprecated

### 3.9 Supervisor / Safety Agent (always-on)
- Pre-publish guardrails: copyrighted music, misleading claims, prohibited categories (medical, financial advice), brand safety
- Hard-block + escalate ให้ human reviewer ถ้าผ่าน threshold

---

## 4. End-to-End Pipeline (Temporal Workflow)

```
DiscoveryWorkflow         (cron: 4x/day)
  └─ TrendAnalystActivity
  └─ ScoutActivity
  └─ persist ProductCandidates + TrendSignals

CampaignWorkflow          (per accepted candidate)
  └─ StrategistActivity → CampaignBrief
  └─ WritersRoomActivity (parallel sub-agents → debate → consolidate)
       └─ Storyboard
  └─ SafetyPreCheckActivity (block / pass)
  └─ ProducerActivity
       ├─ for scene in storyboard:
       │   ├─ generate visual (Veo/Runway/Kling)
       │   ├─ generate audio (TTS)
       │   └─ generate b-roll
       └─ compose (FFmpeg) → MasterVideo
  └─ SafetyPostCheckActivity (watermark, claim audit)
  └─ PublishWorkflow (fan-out per platform)
       ├─ FB Reel
       ├─ IG Reel
       └─ YT Short
  └─ schedule MetricsWorkflow (1h, 6h, 24h, 7d, 30d signals)

LearningWorkflow          (cron: nightly)
  └─ AnalyticsRollupActivity
  └─ FeedbackCuratorActivity → WikiEntries
  └─ EmbeddingsRefreshActivity
  └─ StrategyEvalActivity (offline replay vs. new wiki)
```

**Durability guarantees**: ทุก activity idempotent + checkpoint ที่ Temporal — ถ้า video gen timeout 30 นาที, workflow resume ได้

---

## 5. Self-Learning Loop (LLM Wiki)

หัวใจของระบบ — ทำให้ทุก agent "ฉลาดขึ้น" จากประสบการณ์ของตัวเอง

### 5.1 Wiki Structure
สอง layer:

**A. Vector store (pgvector)** — semantic recall
- `wiki_entries(id, namespace, content_md, embedding vector(1536), tags, tier, created_at, deprecated_at)`
- namespaces: `hook_pattern`, `product_archetype`, `audience_persona`, `failure_mode`, `anti_pattern`, `platform_norm`, `compliance_rule`

**B. Knowledge Graph (Postgres relational)** — causal / structural
- `pattern_nodes` + `pattern_edges (cause → effect, weight, evidence_count)`
- ใช้สำหรับ "ทำไม X ถึง work" ไม่ใช่แค่ "X work"

### 5.2 Entry Tiers (กัน wiki rot)
| Tier | Criteria | Use |
|---|---|---|
| **Hypothesis** | 1–2 evidence | injected as "tentative" hint |
| **Validated** | ≥ 5 evidence, p < 0.1 | normal context |
| **Canonical** | ≥ 20 evidence, replicated cross-niche | hard rule |
| **Deprecated** | contradicted by ≥ 3 recent fails | excluded จาก retrieval |

### 5.3 Feedback Loop Mechanics
1. **Outcome labeling** — แต่ละ video ได้ outcome `{breakout, hit, neutral, flop, banned}` หลัง 7 วัน
2. **Counterfactual extraction** — Feedback Curator query: "อะไรที่ทำให้ video นี้ flop ทั้งที่ brief คล้าย hit อื่น?"
3. **Pattern mining** — ใช้ LLM + statistical test (chi-sq / lift) บน feature columns
4. **Wiki write** — entry ใหม่ + อ้าง evidence ids
5. **Context injection** — รอบถัดไป agent ทำ retrieval-augmented prompting จาก wiki ก่อน reasoning

### 5.4 Anti-Catastrophic-Forgetting
- เก็บ "exemplar set" ของ canonical wins ตลอดไป
- Periodic offline replay: รัน strategist บน historical brief แล้วเทียบ output กับ ground truth — alert ถ้า divergence สูง

---

## 6. Data Model (Postgres core tables)

### 6.1 Core Schema
```sql
products              (id, shopee_item_id, title, price, commission_pct, category,
                       rating, sold_count, seller_id, raw_payload jsonb, scouted_at)

product_candidates    (id, product_id, scout_score, scout_reasoning, status, created_at)

trend_signals         (id, source, payload jsonb, hook_pattern, audio_ref,
                       lifecycle_phase, observed_at)

campaign_briefs       (id, product_id, persona, angle, hook, cta, hypothesis,
                       expected_ctr, status, created_by_agent, created_at)

storyboards           (id, brief_id, version, scenes jsonb, total_duration_s,
                       music_brief, voice_profile, safety_status)

assets                (id, storyboard_id, scene_idx, kind, generator, s3_uri,
                       cost_usd, generated_at)

videos                (id, storyboard_id, master_s3_uri, duration_s, size_bytes,
                       safety_status, ready_at)

publish_records       (id, video_id, platform, platform_post_id, posted_at,
                       caption, hashtags, affiliate_link_id)

affiliate_links       (id, product_id, short_code, target_url, created_at)

click_events          (id, link_id, platform, ts, geo, ua_hash)

metrics_timeseries    (id, publish_record_id, ts, views, likes, comments,
                       shares, saves, avg_watch_pct, ctr, conversions, gmv_thb)

outcomes              (id, publish_record_id, label, score, evaluated_at)
```

### 6.2 Storyboard JSON Schema
```jsonc
{
  "version": 1,
  "brief_id": "uuid",
  "total_duration_s": 42,
  "aspect": "9:16",
  "voice_profile": { "lang": "th", "gender": "f", "tone": "energetic-confidant", "tts_engine": "elevenlabs", "voice_id": "..." },
  "music_brief": { "genre": "lofi-hype", "bpm_range": [90, 110], "license": "epidemic-sound" },
  "scenes": [
    {
      "idx": 0,
      "duration_s": 3,
      "purpose": "hook",
      "shot": { "type": "extreme-closeup", "movement": "snap-zoom-in" },
      "visual_prompt": "...",
      "generator": "veo3",
      "dialogue": { "speaker": "narrator", "text_th": "...", "emphasis_words": [...] },
      "on_screen_text": { "th": "...", "style": "bold-pop", "position": "center-upper" },
      "sfx": ["whoosh-01"],
      "transition_out": "match-cut"
    }
  ],
  "cta_scene_idx": 5,
  "affiliate_link_placement": "pinned_comment + on_screen_qr"
}
```

---

## 7. Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| **Agent runtime** | Claude API (Opus 4.7 + Sonnet 4.6) via Anthropic SDK Python | Best reasoning / tool-use; prompt caching ลด cost |
| **Multi-agent orchestration** | Custom on top of Claude tool-use + Temporal | Durable, replayable; ไม่พึ่ง framework ที่อาจตายเร็ว |
| **Workflow engine** | Temporal | Long-running, retries, schedules, signals |
| **Backend API** | FastAPI (Python 3.12) | Async, type-safe, ecosystem ดี |
| **OLTP DB** | Postgres 16 | + pgvector + JSONB |
| **Cache / queue lite** | Redis 7 | Rate limit, session, lightweight queues |
| **Analytics DB** | ClickHouse | metrics_timeseries scale |
| **Object storage** | S3-compatible (R2 / MinIO dev) | Assets + master videos |
| **Video gen** | Veo 3 (Google), Runway Gen-3, Kling — abstracted behind `VideoGenAdapter` | Multi-vendor fallback |
| **Image gen** | Flux 1.1 Pro, Imagen 3, SDXL — adapter pattern | Cost/quality tradeoff per scene |
| **TTS** | ElevenLabs Multilingual v2 (primary), Azure TTS (fallback) | Native Thai support |
| **Lipsync** | Sync.so / Wav2Lip (when narrator on-camera) | Optional |
| **Composition** | FFmpeg + Remotion (programmatic React→video) | Subtitle burn-in, brand overlay |
| **Social publishing** | Meta Graph API (FB+IG), YouTube Data API v3; n8n สำหรับ glue ที่ไม่ใช่ core | Official APIs first |
| **Shopee** | Shopee Affiliate Open API + Shopee Open Platform | Official endpoints + retry adapter |
| **Frontend (ops console)** | Next.js 15 + shadcn/ui | Internal supervisor dashboard |
| **Auth** | Clerk หรือ self-hosted Authentik | ทีม internal |
| **Observability** | OpenTelemetry → Grafana Cloud (Tempo+Loki+Prom) | Trace agent calls end-to-end |
| **LLM eval** | Custom harness + Inspect-AI | Offline replay & regression |
| **IaC** | Pulumi (TypeScript) | Multi-cloud-friendly |
| **CI/CD** | GitHub Actions + Argo CD (k8s) | Standard |

---

## 8. APIs & Interfaces

### 8.1 Internal HTTP (FastAPI)
```
POST /campaigns                    create brief manually / approve auto
GET  /campaigns/{id}
POST /campaigns/{id}/approve
POST /campaigns/{id}/reject

GET  /products/candidates?status=pending
POST /products/candidates/{id}/promote

GET  /videos/{id}
GET  /videos/{id}/preview

POST /wiki/entries                 (Curator service-to-service)
GET  /wiki/search?q=...&namespace=...
POST /wiki/entries/{id}/deprecate

GET  /metrics/campaigns/{id}
GET  /metrics/dashboard
```

### 8.2 Agent Tool Contract
ทุก agent tool คืน JSON ตาม schema นี้:
```json
{ "ok": true, "data": {...}, "cost_usd": 0.012, "latency_ms": 840, "trace_id": "..." }
```
ทำให้ Feedback Curator ติดตาม cost / latency ระดับ tool ได้

### 8.3 External Integrations
| Integration | Auth | Key Endpoints | Rate Limits Plan |
|---|---|---|---|
| Shopee Affiliate | Partner ID + signature | `/product/list`, `/shortlink` | 100 req/min — token bucket |
| Meta Graph | Long-lived page token | `/me/video_reels`, `/me/feed` | App-level budget watcher |
| YouTube | OAuth refresh token | `videos.insert`, `videos.list` | Quota: 10k units/day |
| TikTok Research | Approved app | `research/video/query/` | Pending approval — fallback to public scrape |
| Veo / Runway | API key | their respective gen endpoints | Concurrent job cap |

---

## 9. Non-Stop Operation

### 9.1 Always-On Strategy
- Temporal Schedules: `DiscoveryWorkflow` ทุก 6h, `LearningWorkflow` ทุก 24h, `MetricsPoll` ทุก 1h
- **Backpressure**: ถ้า GPU budget เหลือต่ำ → ลด throughput; ถ้า platform API rate limit → queue
- **Budget controller**: หยุด generation อัตโนมัติเมื่อ daily cost > budget * 1.1 + alert ทีม
- **Hot-standby**: 2 worker pools (primary/secondary) คนละ region

### 9.2 Operational SLOs
| SLO | Target |
|---|---|
| Discovery cycle freshness | < 6h |
| Brief → published video | P50 < 90 min, P95 < 6h |
| Metrics polling lag | < 5 min |
| Wiki update lag (after outcome) | < 24h |
| Pipeline success rate | ≥ 95% |

---

## 10. Safety, Compliance, Guardrails

### 10.1 Pre-publish Checks (Supervisor Agent)
- Music license validation (ID match against licensed library)
- Claim auditor: หา health / financial / "guaranteed" claims → block
- Brand-list block: cigarettes, weapons, supplements ที่ไม่ตรง regulation
- Image safety: NSFW classifier on every generated frame sample
- Disclosure: บังคับ `#โฆษณา` / `#affiliate` ตาม กสทช. / Shopee ToS

### 10.2 Platform Compliance
- FB/IG: Branded content disclosure, no engagement bait
- YouTube: YPP-friendly captions, no copyrighted audio without license
- Shopee: ห้าม misrepresent commission, ห้ามใช้ keyword ห้าม

### 10.3 Data Privacy
- ไม่เก็บ PII จาก click_events (เก็บแค่ ua_hash + geo level region)
- Asset retention: 90 วันใน hot storage, archive ที่ Glacier-class

### 10.4 Kill Switches
- Per-product, per-campaign, per-platform, และ global stop ผ่าน ops console
- Auto-kill เมื่อ platform return policy violation 3 ครั้งใน 24h

---

## 11. Observability & Eval

### 11.1 Tracing
- OpenTelemetry trace ครอบ workflow → activity → agent call → tool call
- Span attributes: agent.name, model, input_tokens, output_tokens, cost_usd, cache_hit

### 11.2 Agent Evaluation Harness
- **Offline replay**: เอา brief เก่าๆ ใส่ agent ใหม่ — เทียบกับ outcome จริง
- **Golden set**: 100 hand-curated cases ที่ต้องไม่ regress
- **A/B traffic split**: 90% prod prompt / 10% candidate prompt; auto-promote ถ้า uplift > threshold p < 0.05

### 11.3 Cost Watcher
- Per-video cost breakdown dashboard: scout LLM, strat LLM, writers LLM, image, video, TTS, compose, publish
- Alert ถ้า cost/video > target * 1.5

---

## 12. Security

- Secrets ใน Vault / SOPS; ไม่มี secret ใน env file สาธารณะ
- IAM: agent service account แยกต่อ role
- Network: agents → external APIs ผ่าน egress proxy เดียวที่ allowlist
- Audit log: ทุก write ลง wiki + ทุก publish + ทุก kill-switch action

---

## 13. Phased Roadmap

### Phase 1 — MVP "Single-loop closed" (Week 1–6)
- Scout (Shopee) + Strategist + 1 Writer agent (no Writers Room debate)
- Storyboard JSON v1
- Video gen: Veo 3 only
- TTS: ElevenLabs only
- Publish: IG Reel only
- Metrics polling + simple wiki (vector store, no KG)
- **Exit criteria**: 1 video ครบ loop, auto-publish, auto-collect metric, auto-write wiki entry

### Phase 2 — "Hollywood + Multi-platform" (Week 7–14)
- Full Writers Room (5 sub-agents + critic)
- Multi-vendor video gen with adapter
- Add FB Reels + YT Shorts publishing
- Trend Analyst agent live
- Wiki tiering system + KG layer
- Safety agent online

### Phase 3 — "Self-improving autonomous" (Week 15–24)
- Offline replay + automatic prompt promotion
- Counterfactual feedback mining
- Cost-aware planner (auto-choose generator per scene)
- Anti-forgetting exemplar set
- Multi-account, multi-niche scaling

---

## 14. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Platform API ban / policy change | High | High | Multi-platform, official APIs, fast disclosure, kill switches |
| Video gen vendor outage | Medium | Med | Multi-vendor adapter + auto-failover |
| Hallucinated claims in script | Medium | High | Critic agent + claim auditor + canonical wiki rules |
| Wiki rot / pattern overfitting | High | Med | Tiering + deprecation + offline replay |
| Cost runaway | Medium | High | Budget controller + per-scene cost caps |
| Copyright strike (music/clip) | Medium | High | Licensed library only, fingerprint check pre-publish |
| Shopee affiliate ToS change | Medium | Med | Adapter layer, monthly ToS review |
| Catastrophic forgetting | Medium | High | Exemplar replay + canonical-tier hard rules |

---

## 15. Open Questions
1. ใช้ Veo 3 (กระชับสุด) หรือ Sora-2 (คุณภาพดีกว่าแต่ latency สูง) เป็น primary?
2. จะลงทุน fine-tune Thai TTS เอง หรือยึด ElevenLabs ตลอด?
3. Phase 1 จะรองรับ niche เดียว (เช่น beauty) หรือเปิดกว้าง?
4. Human-in-the-loop threshold: pre-publish review ที่ confidence ต่ำกว่าเท่าไร?
5. Wiki entry จะอนุญาตให้ agent "เขียนทับ" entry เก่าได้เลย หรือต้อง propose + approve?

---

## 16. Glossary
- **Brief**: campaign specification ที่ Strategist ออก ก่อนเข้า Writers Room
- **Storyboard**: scene-by-scene plan ที่ Writers Room consolidate
- **Master video**: final composited mp4 พร้อม publish
- **Wiki entry**: structured lesson learned ที่ Feedback Curator เขียนกลับ
- **Outcome**: 7-day post-publish label (breakout/hit/neutral/flop/banned)

---

## Appendix A — Example Agent System Prompt (Strategist, excerpt)
```
You are the Strategist agent of Auto-Affi.
Goal: produce a CampaignBrief that maximizes affiliate GMV.
Hard rules (from canonical wiki):
  - Hook within 1.5s or ≥30% drop-off
  - Single CTA, no more than 2 product features
Process:
  1. Retrieve top-k wiki entries from namespaces:
     hook_pattern, audience_persona, anti_pattern
  2. Generate 3 candidate angles. Self-critique each.
  3. Pick the angle with highest expected_ctr × confidence.
  4. Output strict JSON matching CampaignBrief schema.
Forbidden: medical claims, "guaranteed" language, comparative claims
without source.
```

## Appendix B — Cost Model (Phase 1 per video, target)
| Item | Est. cost USD |
|---|---|
| Scout + Strategist LLM | 0.05 |
| Writer LLM | 0.10 |
| 8 scenes × image | 0.25 |
| Video gen (Veo) | 1.80 |
| TTS (60s) | 0.18 |
| Compose + storage | 0.05 |
| Publish API | ~0 |
| Metrics + wiki write | 0.07 |
| **Total target** | **≤ 2.50** |
