# Execution Playbook — Auto-Affi 300%

แผนปฏิบัติการที่ผ่านการ research จริงจาก case study production multi-agent, viral video mechanics, และ Shopee affiliate ไทย — ออกแบบให้ **ทะลุเป้า KPI 3x** ไม่ใช่แค่แตะ

- **Last updated**: 2026-05-12
- **Synthesis sources**: Cognition/Devin, LangGraph prod, Anthropic eval, MAST taxonomy, Mem0 2026, TikTok algo 2026, Shopee Open API, OCPB enforcement

---

## 1. ทำไมถึงจะชนะ — Strategic Wedge

### 1.1 The Gap (จาก research)
- ตลาดไทยยัง **ไม่มี TH-localized AI Product Scout** ที่รวม Shopee Open API scoring + Thai script gen + multi-account TikTok/IG/YT + subId attribution กลับมาที่ creative variant
- Top human operators ทำ **THB 300K–1M+/เดือน** ด้วยมือ (portfolio 10-30 burner accounts × 8-12 videos/วัน × live commerce 2-6 ชม.)
- เครื่องมือคู่แข่ง: **Zaapi** = inbox-only, **Ecomobi** = aggregator ไม่มี AI, **Axiom** = generic RPA, **Tapfiliate/Scaleo/Lindy** = global ไม่ localize ไทย

### 1.2 จุด Leverage (สิ่งที่ทำให้ 300%)
| Lever | ผลคูณ | กลไก |
|---|---|---|
| **7-day indirect-order attribution** (Shopee 2026) | ~2x effective commission | คลิกเดียวเก็บทุก purchase 7 วัน → ไม่ต้องเจาะ SKU ตรง |
| **kie.ai gateway** | ลด cost 51% | Sora 2 $0.015/s vs $0.10 = scale ได้ 2x ใน budget เดิม |
| **Mega-sale alignment** (3.3, 6.6, 9.9, 11.11, 12.12) | +14-17% CTR | schedule push ตรง spike + เตรียม content ล่วงหน้า 14 วัน |
| **Multi-account portfolio** | 10-30x reach | 1 video × 30 accounts ≠ 30 video × 1 account (algo เพิ่ม first-seed test) |
| **AI-generated KOS persona** (ไม่ใช่ influencer voice) | 3-5x conversion | ตาม Impact.com: 9/10 top TH creators by revenue = KOS |
| **Bilateral-sync Wiki** | -90% poison loop | agent เขียนเข้า review folder → Safety promote → ไม่ปนเปื้อนเอง |

**สรุป**: ถ้า Phase 1 baseline = $1k GMV/เดือน → 300% = $3k → ทำได้ด้วย 6 lever รวมกัน

---

## 2. Build Sequence — Phase 1-3 (refined)

### Phase 1 (Week 1-6) — "Single closed loop ที่ขายได้จริง"
**Exit criteria**: 1 niche (beauty/skincare) × 5 video/วัน × loop ครบ ตั้งแต่ scout → publish → metric → wiki write ครบ 14 วัน → GMV ≥ $200

ลำดับ build (critical path):
1. **Shopee Open API adapter** (GraphQL, HMAC, subIds[0-4] taxonomy ล็อก) — 1 สัปดาห์
2. **Temporal workflow + Postgres+pgvector schema** — 1 สัปดาห์
3. **Scout + Strategist + 1 Writer (no Writers' Room yet)** with golden trace eval — 1.5 สัปดาห์
4. **Editor agent ผ่าน MCP** (video-use + Hyperframe + Whisper) บน kie.ai Veo 3 Fast — 1 สัปดาห์
5. **Publisher IG Reels only** (เดี่ยวก่อน) + subId tag — 0.5 สัปดาห์
6. **Analytics polling + simple Wiki (vector only)** — 1 สัปดาห์

### Phase 2 (Week 7-14) — "Hollywood + Multi-platform + portfolio"
- Writers' Room ครบ 6 sub-agents + Critic
- เปิด FB Reels + YT Shorts
- Portfolio 10 burner accounts ต่อ niche, ใช้ 1 video × 10 accounts pattern
- Wiki ขึ้น tier system (Hypothesis → Validated → Canonical) + Mem0/Graphiti integration
- Safety agent online + bilateral-sync Wiki

### Phase 3 (Week 15-24) — "Self-improving autonomous"
- Harness-evolver plugin (auto prompt evolution ผ่าน LangSmith/Langfuse eval)
- Cost-aware planner per scene
- Multi-niche expansion (Mom&Baby, gadgets, food)
- Live commerce AI host (Phase 3.5 stretch)

---

## 3. Skill / Agent Allocation ใน Build Process

**ระหว่างพัฒนา** Auto-Affi เอง — ใช้ Claude Code skill + subagent อย่างฉลาด

| Build task | Tool / Skill | เหตุผล |
|---|---|---|
| ออกแบบ architecture / phase planning | **Plan agent** | trade-off analysis ของ Temporal vs LangGraph ต้อง explicit |
| Code review ทุก PR | **review skill** | catch typing / schema bug ก่อน merge |
| Security review ก่อน deploy | **security-review skill** | secret leak, prompt injection surface, PII flow |
| Setup CI/test runner | **session-start-hook skill** | ให้ test ทำงานใน web session ได้ |
| Claude API integration | **claude-api skill** | prompt caching strategy + thinking budget — มันรู้ pattern best practice |
| Initialize CLAUDE.md | **init skill** | onboard subagent ใหม่ + standard ของ codebase |
| Reduce permission noise | **fewer-permission-prompts skill** | speed-up dev loop |
| Repetitive monitoring | **loop skill** | poll training run / PR status |
| Refactor / cleanup | **simplify skill** | ทุก 2 สัปดาห์รัน 1 รอบ |
| Broad codebase exploration | **Explore agent** | "where is X defined" ตอน onboard |
| Background research (มากกว่า 3 query) | **general-purpose agent** | parallel research แบบที่เพิ่งทำเอกสารนี้ |

### 3.1 Build-time Subagent Pattern (สำคัญ)
ทุก subsystem มี dedicated subagent ที่:
- มี **SKILL.md ของตัวเอง** (role, trigger condition, tool allowlist)
- **Isolated context window** — ไม่ pollute main agent
- มี **acceptance rubric** ที่ Editor-as-judge ตรวจอัตโนมัติ
- ผ่าน **schema-validated handoff** เท่านั้น

ตัวอย่าง: เวลา build Editor agent → spawn subagent ที่มี skill `video-pipeline` กับ tool ที่อนุญาตเฉพาะ FFmpeg + Hyperframe + Whisper (ไม่ให้แตะ DB / Shopee API)

---

## 4. Anti-Patterns — เลี่ยงเด็ดขาด (จาก MAST + real prod failures)

| Anti-pattern | ผลร้าย | กฎของเรา |
|---|---|---|
| **Bag-of-Agents** (agent คุยกันมั่ว) | 17x error compound | Hierarchy เข้มงวด: Supervisor → Writers' Room ภายใน → Producer ขึ้น ห้าม Editor↔Publisher คุย |
| **Specification ambiguity** | "be a creative strategist" | ทุก agent มี Pydantic input/output schema + explicit acceptance criteria |
| **Context collapse** (2%/step retention loss) | 60% สูญที่ step 5 | Re-ground ทุก hop, ไม่ใช่แค่ append; ใช้ Mem0 retrieval ไม่ใช่ context dump |
| **Tool-call compounding** (3-15% fail/call × 9 agents) | catastrophic | Retry idempotent + circuit-breaker ใน Temporal + tool budget per agent |
| **Unbudgeted token loops** | infinite re-planning | Hard cap step + token ต่อ workflow node |
| **Helicone** (maintenance mode มี.ค. 2026) | dead-end stack | ใช้ Langfuse + OpenLLMetry แทน |
| **CrewAI flat role topology** | 3x token overhead, debug หิน | ใช้ LangGraph deterministic graph หรือ Temporal เท่านั้น |
| **Direct wiki write จาก agent** | self-poisoning | Bilateral sync: agent → review folder → Safety promote → canonical |
| **Generic AI TTS voice** | TikTok skip + ban risk | ElevenLabs Thai-cloned + label AI per TikTok 2025 rule |
| **Fake countdown / fake stock** | OCPB violation, ban | Critic Opus block ก่อน publish |
| **Health/whitening claims ไม่มี evidence** | OCPB fine + 1.8M revenue threshold license | Compliance hard filter ที่ Strategist + Critic |
| **Visual product alteration** (color/size AI) | TikTok throttle | Image gen ห้ามแก้ product image — ใช้รูปจริงจาก Shopee |
| **Watermark cross-platform recycle** | algo deprioritize ทั้ง IG + TikTok | Render แยกต่อ platform จาก master master ไม่ใช่ re-upload |
| **Hook > 2 วินาที** | scroll-away | Critic บังคับ hook ≤ 2s |
| **>1 CTA ใน 5 วินาทีแรก** | completion tank | Director rule — CTA เดียวเท่านั้นใน scene 0-1 |

---

## 5. Canonical Wiki Rules (seed Day 1)

ใส่เป็น Tier=Canonical ตั้งแต่เริ่ม — ไม่ต้องรอ learn ใหม่

### 5.1 Content rules
- **Hook < 2s** เลือกจาก 6 templates: POV / Contrarian / Numbers&Scarcity / PAS / Before-After / Open-Loop
- **Average shot 1.5-2.5s**; reset attention ทุก 1-2s (cut/zoom/caption pop/SFX)
- **Audio drop ที่ 40-60% timestamp** (reveal/demo moment)
- **Target completion ≥ 70%** (TikTok 2026 viral threshold)
- **1 share-trigger + 1 save-trigger ต่อ video** (อัลกอ 2026 ให้ DM-share สูงสุดของ IG)
- **Thai-language captions เสมอ** + `#โฆษณา` + AI-content label
- **CTA เดียว** ใน first 5s, optional restate ที่ end-card
- **KOS persona ไม่ใช่ influencer voice** — เน้น "ใช้แล้วชอบจริง" tone

### 5.2 Product Scout scoring rubric (encode ทันที)
```
Score = 0.30 × Commission_EV
      + 0.25 × CR_category_prior × shop_rating × log(review_count)
      + 0.15 × Trend_momentum (7d sales delta + TikTok mention growth)
      - 0.15 × Saturation (count affiliate listings same SKU 7d)
      - 0.10 × Return_rate_penalty (fashion/electronics)
      + 0.05 × Cookie_utilisation (shop catalog breadth)

Hard filters:
  - Restricted categories (medical claims, unapproved supplements, replica brands) → REJECT
  - Shop rating < 4.5 → REJECT
  - Commission < 3% AND AOV < THB 300 → REJECT
```

### 5.3 SubId taxonomy (ล็อกทันที — Shopee เก็บ 5 slots)
```
subId[0] = platform           (tk | ig | yt | fb)
subId[1] = account_handle     (@accountname or hash)
subId[2] = video_id           (campaign-stamped)
subId[3] = campaign_id        (campaign UUID short)
subId[4] = variant            (A/B/C — creative variant)
```
ทุก published video ผูก subId เต็มเซต → Analytics รวมเข้า BigQuery → join กับ TikTok/IG/YT analytics ผ่าน `video_id`

### 5.4 Mega-sale calendar (เตรียม content ล่วงหน้า 14 วัน)
| Date | Push level | Content prep deadline |
|---|---|---|
| 3.3 | High | T-14 |
| 6.6 | High | T-14 |
| 9.9 | **Peak** | T-21 |
| 10.10 | High | T-14 |
| 11.11 | **Peak** | T-21 |
| 12.12 | Peak | T-21 |

Strategist agent ต้อง query calendar ทุกครั้ง → ถ้า ≤ 14 วันก่อน mega-sale → priority boost + budget bump 2x

### 5.5 Niche priority (Phase 1-2)
1. **Beauty / Skincare** — CR 1.5-3%, AOV 250-450, top KOS share — start here
2. **Mom & Baby** — CR 1-2%, high LTV + repeat — Phase 2
3. **Gadgets / Accessories** — CR 0.8-1.5%, impulse — Phase 2
4. **Fashion** — CR 0.6-1.2% แต่ return rate 12% drag — Phase 3 cautious
5. **Food & Beverage** — Phase 3+

---

## 6. Observability & Eval Stack (production-grade)

### 6.1 Stack ที่ใช้
- **OpenLLMetry (Traceloop)** — OTel instrumentation vendor-neutral
- **Langfuse self-hosted (MIT license)** — prompt versioning, eval, trace storage
- **Arize Phoenix** — notebook-grade eval ของ Writers' Room creative output
- **Laminar (Apache 2.0)** — long-running Temporal workflow transcript debugging
- ❌ **ห้ามใช้ Helicone** — maintenance mode มี.ค. 2026

### 6.2 Golden Trace Set (ต้องสร้าง Day 1)
- 100 hand-curated case จาก Shopee top performers จริง
- ทุก prompt change รัน eval set → block PR ถ้า regress
- Promote prompt candidate เมื่อ uplift ≥ 5%, p < 0.05, sample ≥ 200

### 6.3 Evaluator-Optimizer Pattern
- **Editor agent = LLM-as-judge** ที่มี rubric ชัด (ไม่ใช่ vibes)
- Rubric: hook_strength, shot_pacing, completion_pred, share_trigger_count, save_trigger_count, compliance_flags, KOS_voice_score
- Critic agent ใช้ rubric เดียวกันใน red-team mode

### 6.4 Memory Architecture (refined)
- **Core memory** (always-in-context): brand voice, KOS persona, hard rules
- **Archival vector** (Qdrant or pgvector): creative history embeddings
- **Procedural memory** (Mem0): "what worked for hooks in beauty vertical"
- **Temporal KG** (Graphiti): campaign → outcome → pattern causal edges
- **Bilateral sync**: agent write → review queue → Safety promote → canonical

---

## 7. KPI Scoreboard (300% target)

| KPI | Phase 1 baseline | 100% goal | **300% goal** |
|---|---|---|---|
| Videos / day | 5 | 25 | **75** |
| Cost / video | $3.32 (kie.ai) | $1.80 | **$0.80** (self-host + adapter) |
| Avg CTR | 0.84% | 1.5% | **4%+** |
| Avg CR | 0.6% | 1.2% | **2.5%+** |
| Affiliate GMV / month | $200 | $1k | **$5k+** |
| Completion rate | 60% | 70% | **78%+** (TikTok benchmark) |
| Wiki canonical entries | 30 | 150 | **500+** |
| Human intervention rate | 50% | 25% | **<5%** |
| MoM CTR uplift | flat | 3% | **8%+** |

### 7.1 Leading Indicators (วัดรายวัน)
- Hook retention (1.5s hold rate)
- Share count per 1k views
- Save count per 1k views
- subId-tagged conversion / video
- Wiki entry write rate
- Cost/video drift vs target

---

## 8. Operational Discipline

### 8.1 Daily Rhythm (ทีมตอนเริ่ม)
- 07:00 — Analytics rollup ของเมื่อวาน → Wiki write batch
- 08:00 — Standup human supervisor review safety escalations
- 09:00-23:00 — Continuous pipeline (Temporal schedule)
- 23:00 — Cost reconciliation + budget watcher report

### 8.2 Weekly Rhythm
- จันทร์: prompt version eval review
- พุธ: portfolio rebalance (kill burner accounts ที่ throttle, spawn ใหม่)
- ศุกร์: niche performance review + Strategist priority refresh

### 8.3 Burner Account Hygiene
- 30 บัญชี TikTok ต่อ niche, แบ่ง 3 cohort: new (10) / warm-up (10) / scaled (10)
- Rotation: ถ้าบัญชี throttled (views drop 70%+ × 5 video ติด) → retire, spawn ใหม่
- Content fingerprint สลับต่อบัญชี (different voice, different overlay style) — เลี่ยง algo detection
- ⚠️ **Legal**: ตรวจ ToS ของ TikTok/Meta เรื่อง multi-account ก่อน scale; Phase 1 ลองตัว 3-5 account ก่อน

### 8.4 PDPC Compliance (Aug 2025 enforcement)
- ห้ามเก็บ email/phone จาก click ผ่าน landing page proxy
- Click attribution ใช้ subId เท่านั้น (Shopee จัดการ user PII ตัวมันเอง)
- DPO + privacy notice ถ้า revenue ≥ THB 1.8M/ปี (Direct Marketing License threshold)

---

## 9. Risk-Mitigation ที่เกิน Standard

| Risk | Standard mitigation | **เพิ่มเป็น 300%** |
|---|---|---|
| Platform ban | Multi-platform | + Burner portfolio + content fingerprint diversity + alt domain redirect proxy |
| Video gen vendor outage | Multi-vendor adapter | + kie.ai gateway + direct vendor + self-host Open-Sora 2.0 standby (Phase 3) |
| Wiki rot | Tier system | + Bilateral sync + nightly offline replay + canonical exemplar replay |
| Cost runaway | Budget cap | + Per-scene cost predictor (estimate ก่อน gen) + auto-throttle ที่ 80% daily budget |
| Hallucinated claim | Critic agent | + Typhoon 2 verifier + claim-auditor MCP + PDPC-compliance gate ที่ Safety |
| Algo change | Wiki update | + Weekly algo signal monitor (3 source: official changelog + creator forum + own variance test) |
| Catastrophic forgetting | Exemplar replay | + Procedural memory separation (Mem0) + canonical tier hard-rule lock |
| Account compromise | 2FA | + Hardware key + IP-allowlist + session anomaly detection |

---

## 10. Decision Log (open questions + bet)

| Question | Default bet | Trigger to revisit |
|---|---|---|
| Veo 3 vs Sora 2 primary? | **Veo 3 Fast ผ่าน kie.ai** ($0.30/clip) | quality eval flag drop > 10% |
| Single niche vs multi Phase 1? | **Beauty only** (highest CR) | GMV plateau ที่ $500/mo |
| Human pre-publish threshold? | **confidence < 0.7** ส่ง human | false-positive rate > 30% |
| Wiki overwrite vs propose? | **Bilateral sync** (research strongly supports) | review queue backlog > 7 days |
| LangGraph vs Temporal? | **Temporal** (durable, long-running, ดีกว่า workflow > 1h) | dev velocity drop > 30% |
| TS vs Python stack? | **Python** (Anthropic SDK + Temporal + Whisper ecosystem ดีสุด) | ทีมไม่มี Python expert |
| Self-host video gen? | **Phase 3** เมื่อ Open-Sora 2.0 พร้อม | kie.ai cost drift > $5k/mo |

---

## 11. Quick-Win Hit List (สัปดาห์แรก)

ทำ 5 อย่างนี้ก่อน — leverage สูงสุด:

1. **subId taxonomy ล็อก** + Shopee API adapter — ทำ attribution ทำงานก่อนทุกอย่าง (วันที่ 1-3)
2. **Beauty Top-50 product seed list** จาก Shopee Open API → คะแนนเข้า Postgres (วันที่ 3-5)
3. **Hook library 6 templates × 3 ภาษาไทย examples** seed เข้า Wiki canonical (วันที่ 5-7)
4. **1 video manual end-to-end** — ไม่ผ่าน agent, ทำมือ → publish → วัด baseline CTR/CR ของเราเอง (วันที่ 7-10)
5. **Langfuse + golden trace 20 case** — eval harness ทำงานก่อน build agent (วันที่ 10-14)

ถ้า 5 อย่างนี้ครบใน 2 สัปดาห์ → confidence ระบบจะ ship 300% สูงมาก

---

## Sources (research synthesized)

### Multi-agent prod
- [Cognition Devin 2025](https://cognition.ai/blog/devin-annual-performance-review-2025)
- [MAST taxonomy](https://arxiv.org/pdf/2503.13657)
- [Bag-of-Agents 17x error](https://towardsdatascience.com/why-your-multi-agent-system-is-failing-escaping-the-17x-error-trap-of-the-bag-of-agents/)
- [LangGraph vs CrewAI](https://redwerk.com/blog/langgraph-vs-crewai/)
- [Anthropic eval guide](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Mem0 State of Memory 2026](https://mem0.ai/blog/state-of-ai-agent-memory-2026)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Harness engineering](https://github.com/ai-boost/awesome-harness-engineering)

### Viral video
- [TikTok algo 2026 (Buffer)](https://buffer.com/resources/tiktok-algorithm/)
- [TikTok algo 2026 (Go-Viral)](https://www.go-viral.app/blog/tiktok-algorithm-2026/)
- [IG algo 2026 (Later)](https://later.com/blog/how-instagram-algorithm-works/)
- [Marketing Agent TikTok 2026](https://marketingagent.blog/2025/11/03/tiktok-marketing-strategy-for-2026-the-complete-guide-to-dominating-the-worlds-fastest-growing-platform/)
- [Impact.com influencer trends](https://impact.com/influencer/influencer-marketing-ecommerce-trends/)
- [TikTok AI rules](https://www.affiversemedia.com/tiktoks-ai-crackdown-new-community-guidelines-signal-tougher-times-for-performance-marketers/)
- [OCPB enforcement](https://www.nationthailand.com/news/general/40056899)

### Shopee TH
- [Shopee commission 2026 (Alibaba)](https://www.alibaba.com/product-insights/shopee-commission-rate-analysis-2026-latest-insights.html)
- [Shopee affiliate community guidelines](https://help.shopee.com.my/10/article/140075-[ENG]-Shopee-Affiliates-Social-Media-Community-Guidelines)
- [Affiliate API community (shopee-aff)](https://github.com/bcat95/shopee-aff)
- [Direct Marketing License TH](https://www.transatlanticlaw.com/content/thailand-tightens-oversight-on-direct-sales-and-direct-marketing/)
- [PDPC fines 2025](https://cookieinformation.com/blog/what-is-the-thailand-pdpa/)
- [WE Interactive affiliate TH 2026](https://we-interactive.com/affiliate-marketing-thailand-the-2026-strategic-guide-to-high-performance-partnerships/)
