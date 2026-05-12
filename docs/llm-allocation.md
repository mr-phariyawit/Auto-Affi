# LLM Allocation Plan — Auto-Affi Crew

แผนการเลือก / ใช้ LLM ต่อ agent + เทคนิคประหยัด token + fallback strategy

- **Model family**: Claude 4.x — Opus 4.7 / Sonnet 4.6 / Haiku 4.5
- **API**: Anthropic Messages API + prompt caching + extended thinking + tool use
- **Last updated**: 2026-05-12

---

## 1. หลักการเลือก Model

| มิติ | Opus 4.7 | Sonnet 4.6 | Haiku 4.5 |
|---|---|---|---|
| Reasoning depth | สูงสุด | ดี | พอใช้ |
| Creative writing TH | สูงสุด | ดี | จำกัด |
| Cost (relative) | 1.0x | 0.2x | 0.04x |
| Latency | ช้าสุด | กลาง | เร็วสุด |
| **ใช้เมื่อ** | งานคิดยาก / ตัดสินใจสำคัญ / pattern mining | งานปกติส่วนใหญ่ / tool use / structured output | งาน high-volume / format / classify / parse |

**กฎทอง**:
1. **Default = Sonnet 4.6** — ถ้าไม่มีเหตุผลชัดเจน
2. **Upgrade เป็น Opus** เฉพาะ critical reasoning + critic + curator
3. **Downgrade เป็น Haiku** เฉพาะงาน format / parse / classify ที่ schema ชัด
4. ใช้ **Extended Thinking** ในงาน Opus เท่านั้น (ที่ pattern mining / strategy)
5. ใช้ **Prompt Caching** ทุกที่ที่ system prompt + wiki context > 1024 tokens

---

## 2. Per-Agent Model Map

| Agent | Model | Extended Thinking | Cache Strategy | เหตุผล |
|---|---|---|---|---|
| **Product Scout** | Sonnet 4.6 | — | cache: system + scoring rubric + wiki anti-patterns | High volume (50+ products/รอบ × 4 รอบ/วัน), schema ชัด |
| **Trend Analyst** | Sonnet 4.6 | — | cache: system + historical signal patterns | Parse raw social signals → structured |
| **Strategist** | **Opus 4.7** | ใช้ (budget 8k tokens) | cache: system + wiki canonical rules | Matchmaking ที่ต้องคิดลึก ผูกกับ outcome ทั้งหมด |
| **Writers' Room — Director** | **Opus 4.7** | ใช้ (budget 4k) | cache: writer style guide + recent canonical wins | Final decision authority, รวมความเห็น sub-agent |
| **Writers' Room — Screenwriter** | Sonnet 4.6 | — | cache: brand voice + Thai script examples | Creative writing TH, ทำ throughput สำคัญ |
| **Writers' Room — Cinematographer** | Sonnet 4.6 | — | cache: shot vocabulary + 9:16 framing rules | Structured visual plan |
| **Writers' Room — Storyboard Artist** | Sonnet 4.6 | — | cache: storyboard JSON schema | Structured output |
| **Writers' Room — Sound Designer** | Haiku 4.5 | — | cache: music library taxonomy | Pick from finite set |
| **Writers' Room — Critic (Red Team)** | **Opus 4.7** | ใช้ (budget 6k) | cache: anti-pattern wiki + failure modes | ต้องหา flaw subtle ที่คนอื่นมองไม่เห็น |
| **Producer** | Sonnet 4.6 | — | cache: generator capability matrix | Routing / scheduling |
| **Editor sub-agent** | Sonnet 4.6 | — | cache: tool catalog + standard passes | Tool-use heavy (FFmpeg/Hyperframe/ASR), token-capped $0.40/วีดีโอ |
| **Publisher** | Haiku 4.5 | — | cache: platform-specific caption templates | Format caption + hashtags + API call |
| **Analytics Collector** | Haiku 4.5 | — | — | ดึง JSON, push to DB; reasoning น้อย |
| **Feedback Curator** | **Opus 4.7** | ใช้ (budget 16k) | cache: wiki schema + statistical rubric | Pattern mining จาก outcome — งานยากสุดในระบบ |
| **Supervisor / Safety** | Sonnet 4.6 (primary) + Opus (escalation) | escalation: ใช้ | cache: compliance rules + brand blocklist | ส่วนใหญ่ตรวจตาม rule → Sonnet พอ; edge case ส่ง Opus |
| **Ops Console / chat with user** | Sonnet 4.6 | — | cache: tool descriptions | Internal dashboard chat |

### 2.1 หมายเหตุการเลือก
- **Strategist + Curator + Critic = Opus** เพราะนี่คือ "ขุมพลัง learning" ของระบบ — quality ที่นี่ × 10000 รอบ = ROI สูงสุด
- **Screenwriter ไม่ใช่ Opus** — บทไทย Sonnet 4.6 ทำได้ดีพอ และต้องวิ่งหลายร้อยครั้ง
- **Sound Designer = Haiku** — เลือกจาก finite music library ไม่ต้องคิด
- **Publisher + Analytics = Haiku** — format + push, ไม่มี reasoning

---

## 3. Prompt Caching Strategy

Claude prompt caching ลด cost ของ cached tokens ลง ~90% และลด latency ลง ~80% — ระบบนี้พึ่ง cache เป็นหัวใจ

### 3.1 Cache Layout (ทุก agent)
```
[cache_control: system prompt          ]   ← rarely changes, TTL 1h
[cache_control: tool definitions       ]   ← rarely changes, TTL 1h
[cache_control: agent-specific kb      ]   ← rule book / wiki canonical, TTL 1h
[                wiki retrieval result ]   ← per-request RAG, no cache
[                user/task content     ]   ← varies, no cache
```

### 3.2 ตัวอย่าง Cache Win
**Strategist agent** ต่อ campaign:
- System + tools + canonical wiki = ~12k tokens (cached)
- Per-call new content = ~2k tokens (uncached)
- **Cost without cache** (Opus): 14k × $15/M = $0.21
- **Cost with cache**: 12k × $1.5/M (read) + 2k × $15/M = $0.048 → **ประหยัด 77%**

### 3.3 Cache TTL Discipline
- ใช้ **5 minute cache** สำหรับ wiki retrieval results (Curator update บ่อย)
- ใช้ **1 hour cache** สำหรับ system prompt + tool schema
- **Cache breakpoint discipline**: ใส่ `cache_control` ที่ขอบเขตที่ change rate แตกต่างชัด เท่านั้น (ไม่ใส่เกิน 4 จุด)

---

## 4. Extended Thinking Usage

ใช้เฉพาะ Opus + 3 agent ที่งานคิดลึกจริง:

| Agent | Thinking budget | Why |
|---|---|---|
| Strategist | 8k tokens | Cross-reference wiki + reason about persona × angle × hook |
| Critic | 6k tokens | ลำดับ flaw / brand risk / compliance gap |
| Feedback Curator | 16k tokens | Statistical reasoning + counterfactual mining |

**Gate**: ถ้า task confidence > 0.85 หลัง initial pass → skip extended thinking ในรอบนั้น

---

## 5. Tool Use Discipline

### 5.1 Tool result shape (มาตรฐานทั้งระบบ)
```json
{ "ok": true, "data": {...}, "cost_usd": 0.012, "latency_ms": 840, "trace_id": "..." }
```
Curator track ได้ว่า tool ไหนกินเงิน / ช้า / fail บ่อย → ปรับ Wiki

### 5.2 Tool budget per agent (max tool calls / turn)
| Agent | Max tools / turn | Hard stop |
|---|---|---|
| Scout | 20 | 30 |
| Strategist | 10 | 15 |
| Writers' Room sub-agents | 5 each | 8 |
| Editor | 50 (FFmpeg ops) | 80 |
| Publisher | 6 | 10 |
| Curator | 30 (DB queries) | 50 |

### 5.3 Parallel tool use
- เปิด `disable_parallel_tool_use: false` (default) ทุก agent
- Producer + Editor ใช้ประโยชน์มาก (ดึง asset หลายตัวพร้อมกัน)

---

## 6. Context Window Strategy

Opus 4.7 / Sonnet 4.6 มี 1M context — ใช้แบบฉลาด ไม่ใช่ใส่ทุกอย่าง

| Agent | Typical input | Strategy |
|---|---|---|
| Scout | ~15k | system + rubric + wiki top-20 anti-pattern |
| Strategist | ~25k | system + canonical wiki + top-10 persona + brief context |
| Writers' Room | ~40k (shared) | brief + storyboard schema + 5 reference scripts |
| Editor | ~30k | tool catalog + storyboard + ASR transcript + style reference metadata |
| Curator | ~150k | 7-day outcomes batch + wiki + statistical eval results |

**Rule**: ถ้า context > 200k โดยไม่ใช่ Curator → มีอะไรผิดแล้ว ต้อง summarize / chunk

---

## 7. Fallback Chain

```
Opus 4.7 (primary)
   └─ on rate-limit / 5xx → Sonnet 4.6 (same prompt, mark trace "degraded")
        └─ on rate-limit → queue + exponential backoff
             └─ if backlog > 30min → alert + kill campaign workflow

Sonnet 4.6 (primary)
   └─ on rate-limit → Haiku 4.5 (only if task allows — flag in agent metadata)
        └─ else queue + backoff
```

**Critical**: Strategist + Curator + Critic — **ห้าม fallback ไป Sonnet/Haiku** ใน production output (mark degraded + retry only)

---

## 8. Cost Model — Per Video Breakdown

ราคา reference (USD/M tokens, ประมาณการ 2026):
- Opus 4.7: input $15 / output $75
- Sonnet 4.6: input $3 / output $15
- Haiku 4.5: input $0.80 / output $4

| Agent | Calls / video | Avg in (cached %) | Avg out | Model | Cost USD |
|---|---|---|---|---|---|
| Scout (amortized per accepted product) | 1 | 14k (85%) | 2k | Sonnet | 0.04 |
| Trend Analyst (amortized) | 0.2 | 10k (80%) | 1k | Sonnet | 0.01 |
| Strategist | 1 | 14k (85%) + 8k thinking | 3k | Opus | 0.40 |
| Director | 1 | 18k (80%) + 4k thinking | 2k | Opus | 0.35 |
| Screenwriter | 1 | 12k (85%) | 4k | Sonnet | 0.07 |
| Cinematographer | 1 | 10k (85%) | 3k | Sonnet | 0.05 |
| Storyboard Artist | 1 | 8k (85%) | 5k | Sonnet | 0.08 |
| Sound Designer | 1 | 4k (90%) | 0.5k | Haiku | 0.001 |
| Critic | 1 | 16k (80%) + 6k thinking | 2k | Opus | 0.35 |
| Producer | 1 | 8k (85%) | 1k | Sonnet | 0.02 |
| Editor agent | 1 | 25k (70%) | 6k | Sonnet | 0.13 |
| Publisher (3 platforms) | 3 | 3k (90%) | 0.5k | Haiku | 0.003 |
| Analytics (over 30 days) | 10 | 2k | 0.3k | Haiku | 0.02 |
| Curator (amortized 1/100 videos) | 0.01 | 150k (50%) + 16k thinking | 8k | Opus | 0.03 |
| **Total LLM** | | | | | **≈ $1.57** |

หมายเหตุ: Editor agent cost ($0.13) อยู่ใน budget cap $0.40 → มี headroom 3x สำหรับ tool-call retry

---

## 9. Eval & Promotion Loop

ทุก agent มี "candidate prompt" ที่แข่งกับ "production prompt"

| Step | Detail |
|---|---|
| 1. Shadow run | candidate prompt รัน parallel กับ production ใน 10% traffic |
| 2. Score | เทียบ outcome 7 วันหลัง publish (sample size ≥ 200) |
| 3. Promote | ถ้า uplift > 5% และ p < 0.05 → promote candidate → production |
| 4. Archive | เก็บ prompt version ใน git พร้อม eval result |

**Special: Curator** เพราะ output ไม่มี "outcome" ตรงๆ → eval ด้วย:
- Wiki entry coverage on canonical patterns (recall benchmark)
- Statistical validity ของ patterns ที่เขียน (held-out replay)

---

## 10. Operational Safeguards

| Safeguard | Mechanism |
|---|---|
| Daily Opus spend cap | $50/day Phase 1 → throttle ที่ 80% → kill ที่ 110% |
| Per-campaign LLM cap | $3.00/video hard limit ที่ Producer enforce |
| Token outlier alert | ถ้า single agent call > 50k output → alert (อาจ infinite loop) |
| Prompt drift detection | weekly diff ของ system prompt + alert ถ้า diverge > threshold |
| Cache hit rate SLO | ต้อง ≥ 70% หลัง warmup; ถ้าต่ำ → investigate |
| Model deprecation watch | subscribe Anthropic changelog; eval ใหม่ ทุกครั้งที่ minor version ออก |

---

## 11. Migration Plan (เมื่อ model ใหม่ออก)

ตัวอย่าง: Opus 4.8 ออก
1. **Shadow** — รัน Opus 4.8 ใน 5% traffic ของ Strategist เป็นเวลา 14 วัน
2. **Compare** — outcome uplift, cost delta, latency delta
3. **Decision matrix**:
   - uplift > 5% และ cost ≤ +20% → promote
   - uplift > 0 และ cost ≥ +50% → ใช้เฉพาะ Critic + Curator
   - uplift < 0 → keep old
4. **Rollout** — gradual 5% → 25% → 100% over 7 วัน

---

## 12. Open Questions
1. ใช้ batch API (50% off, 24h SLA) สำหรับ Curator ดีไหม — น่าจะคุ้ม
2. Strategist ที่ใช้ Opus + extended thinking — ลอง self-consistency (3 samples → vote) ดีกว่าไหม?
3. Editor agent fallback ไป deterministic FFmpeg recipe — เกณฑ์ trigger ที่ชัดคืออะไร (cost cap / quality eval)?
4. Publisher captions ลอง fine-tuned small model (เช่น GPT-4o-mini หรือ Haiku) เทียบ
5. คิด on-prem inference (vLLM + Llama-3 405B) สำหรับ Editor ASR/tool agent ที่กิน token เยอะที่สุด?
