# Test Plan — Auto-Affi

- **PM**: Nick Fury
- **Linked**: `docs/si/srs.md`, `docs/execution-playbook.md` §6
- **Last updated**: 2026-05-12

---

## 1. Test Strategy

ระบบเป็น agentic + integrated pipeline — ใช้ 4 layer:

| Layer | Goal | Tools |
|---|---|---|
| **Unit** | Function/adapter correctness | pytest, ruff, mypy |
| **Integration** | Agent ↔ Tool, adapter ↔ vendor API | pytest-asyncio, VCR cassettes for vendor APIs |
| **Agent Eval** | Prompt quality, golden trace regression | Langfuse + Phoenix + offline replay |
| **End-to-End** | Full pipeline brief → publish → metric → wiki | Temporal test workflows + sandbox accounts |

**Critical**: agent quality ≠ code correctness — separate eval gates เป็นมาตรฐาน

---

## 2. Test Environments

| Env | Purpose | Data | Vendor APIs |
|---|---|---|---|
| **dev (local)** | unit + integration | seed data, mocked vendors | VCR cassettes |
| **staging** | end-to-end, real APIs, no publish | anonymized, 10% prod | Real (kie.ai sandbox) + sandbox social accounts |
| **prod** | live operation | live | Real |

**Sandbox social accounts**: 2× burner accounts ต่อ platform เพื่อ test publishing โดยไม่กระทบ prod portfolio

---

## 3. Entry / Exit Criteria

### 3.1 Entry to Phase 1 implementation
- [ ] Test environments provisioned (dev + staging)
- [ ] Golden trace set ≥ 20 cases ใน Langfuse
- [ ] CI pipeline runs unit + lint บนทุก PR

### 3.2 Exit per Phase
- [ ] All MUST requirements ผ่าน test
- [ ] Code coverage ≥ 70% บน adapters + workflows
- [ ] Agent eval regression test pass (no uplift ≥ -5%)
- [ ] Zero P0/P1 bugs open
- [ ] Compliance gate pass (10 sample videos ผ่าน safety + Thai quality gates)

---

## 4. Test Categories

### 4.1 Unit Tests
ครอบคลุม:
- Shopee API adapter (request signing, response parsing, retry, rate limit)
- subId taxonomy encoder / decoder
- Wiki retrieval ranking
- Scout scoring rubric arithmetic
- FFmpeg command builder
- Hyperframe template renderer
- Cost predictor (per-scene budget estimator)

**Standard**: pytest, fixtures ใน `tests/fixtures/`, deterministic seed

### 4.2 Integration Tests
ครอบคลุม:
- Agent → Anthropic API (with prompt caching verification)
- Agent → kie.ai (Veo / Sora / Flux endpoints) — VCR cassette
- Agent → ElevenLabs TTS (Thai voice)
- Temporal workflow handoff (schema-validated input/output)
- Postgres write-read round trip
- pgvector embedding store/retrieve
- Meta Graph API publish (sandbox account)

**Standard**: pytest-asyncio, VCR.py สำหรับ vendor APIs ที่จ่ายเงิน, cleanup fixture สำหรับ DB

### 4.3 Agent Evaluation (สำคัญ)

#### 4.3.1 Golden Trace Set
- 100 hand-curated cases (Phase 1 เริ่ม 20)
- Coverage: 5 niches × 4 product archetypes × 5 brief styles
- Each case: input + expected output rubric scores

#### 4.3.2 Per-Agent Eval
| Agent | Metric | Threshold | Tool |
|---|---|---|---|
| Scout | Top-10 product overlap vs human curator | ≥ 70% recall | Langfuse |
| Strategist | Brief rubric score (vs human-rated) | ≥ 8/10 avg | Phoenix |
| Writer | Thai naturalness (Typhoon verifier) | ≥ 8/10 | Typhoon API |
| Critic | Anti-pattern detection recall on planted issues | ≥ 90% | Langfuse |
| Editor | Output spec compliance (pacing, hook, subtitle accuracy) | 100% schema pass | pytest + ffprobe |
| Curator | New canonical wiki entry validity (held-out replay) | ≥ 80% | offline replay |

#### 4.3.3 Regression Gate
- ทุก prompt change รัน golden trace set
- Block PR ถ้า any metric regress > 5%
- Promote prompt candidate เมื่อ uplift ≥ 5% และ p < 0.05 บน ≥ 200 sample

### 4.4 Thai Quality Gates (per-video, pre-publish)
ตาม `docs/thai-genai-stack.md` §10:
1. Typhoon 2 script naturalness ≥ 8/10
2. Whisper round-trip WER ≤ 3%
3. PaddleOCR Thai text rendering ≥ 99% accuracy
4. Critic Opus cultural appropriateness pass

ทุก video fail check ใด → Editor re-run จุดนั้น (ไม่ rerun ทั้ง pipeline)

### 4.5 End-to-End Pipeline Tests
Sandbox scenario:
- **E2E-01**: 1 product → brief → storyboard → 5 scenes generated → composed → published to sandbox IG → metric polled
- **E2E-02**: Fail-injection: Veo 3 timeout → adapter fallback to direct Veo
- **E2E-03**: Fail-injection: Critic block → Editor regenerate scene
- **E2E-04**: Mega-sale calendar 14 วันก่อน → priority_boost = true
- **E2E-05**: Kill switch trigger → all in-flight publishing paused within 5 min
- **E2E-06**: Bilateral sync — agent attempts direct canonical write → blocked, lands in review queue

### 4.6 Safety / Compliance Tests
- **SF-01**: medical claim ใน script → Critic block
- **SF-02**: copyrighted music ID match → block
- **SF-03**: missing `#โฆษณา` → publisher block
- **SF-04**: 3 violation ใน 24h → auto-kill
- **SF-05**: PII leak attempt (email/phone in caption) → block

### 4.7 Performance Tests
- **PF-01**: 50 concurrent campaigns ใน staging → workflow latency P95 ≤ 6h
- **PF-02**: Cache hit rate measurement หลัง 24h warmup → ≥ 70%
- **PF-03**: Cost / video tracking accuracy vs invoice ± 5%

### 4.8 Security Tests
- **SEC-01**: Secret scanning (gitleaks) บน PR
- **SEC-02**: Egress allowlist enforcement test (block unknown domain)
- **SEC-03**: Prompt injection canary in Shopee scraped content → quarantined
- **SEC-04**: API key rotation procedure runbook test

---

## 5. CI/CD Integration

### 5.1 PR Pipeline (every PR)
```
1. ruff + black + mypy (lint)
2. pytest unit (parallel)
3. pytest integration (with VCR replay)
4. gitleaks secret scan
5. agent eval regression (golden trace, 20 cases Phase 1)
6. PR review (≥ 1 human approval)
```

### 5.2 Main Pipeline (post-merge to main)
```
1. Full integration test (live sandbox vendors)
2. E2E pipeline smoke (E2E-01)
3. Deploy to staging
4. Post-deploy health check (Temporal worker healthy, DB migrations applied)
```

### 5.3 Pre-Prod Promotion (weekly cadence)
```
1. Full E2E regression (E2E-01 → E2E-06)
2. Compliance gate (10 random video sample)
3. Cost drift check vs target
4. Manual approval (Nick Fury or Tech Lead)
5. Deploy to prod
```

---

## 6. Test Data Strategy
- Seed data ใน `tests/fixtures/` — covers Phase 1 niches
- Production data ห้าม leak — staging ใช้ anonymized 10% sample
- Sandbox social accounts: 2/platform, never reused เป็น prod burner
- Golden trace set version-controlled ใน `tests/golden_traces/`

---

## 7. Defect Management
- All bugs → Linear issue with severity:
  - **P0** (production down / data loss) — 4h SLA
  - **P1** (key feature blocked) — 24h SLA
  - **P2** (workaround exists) — 1 week
  - **P3** (cosmetic / nice-to-have) — backlog
- Correction Register: `docs/pm/correction-register.md` (Tier 2)
- Trend review weekly ใน status report

---

## 8. Test Tools
| Tool | Use |
|---|---|
| pytest, pytest-asyncio | unit + integration |
| VCR.py | vendor API cassettes |
| ruff | lint |
| black | format |
| mypy | type check |
| gitleaks | secret scan |
| Langfuse | agent trace + eval storage |
| Arize Phoenix | creative output eval |
| Laminar | long-running workflow trace |
| Typhoon 2 (self-host) | Thai naturalness verifier |
| Whisper-large-v3 | TTS round-trip verifier |
| PaddleOCR Thai | text rendering verifier |
| ffprobe | video metadata check |
| Temporal test util | workflow scenarios |

---

## 9. Test Schedule
- **Pre-Phase 1**: golden trace set 20 cases + CI pipeline operational
- **Phase 1 weekly**: regression run + 5 E2E run + compliance gate run
- **Per-PR**: unit + integration + golden trace + lint
- **Phase exit**: full E2E + compliance + cost + perf review → exit gate

---

## 10. Roles
| Role | Responsibility |
|---|---|
| Tech Lead | CI pipeline, integration tests |
| AI Eng | Golden trace, agent eval setup |
| Video Eng | Pipeline + Thai quality gate tests |
| Ops/Safety | Safety + compliance test cases |
| Nick Fury | Phase exit gate approval |
