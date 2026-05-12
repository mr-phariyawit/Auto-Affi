# Prompt Engineering Standards — Auto-Affi

มาตรฐานเขียน / version / eval / deploy prompts ของทุก agent ในระบบ

- **PM**: Nick Fury
- **Linked**: `docs/llm-allocation.md`, `docs/si/test-plan.md` §4.3
- **Last updated**: 2026-05-12

---

## 1. หลักการ

1. **Prompt = code** — version, review, test, ship เหมือน code
2. **Schema-validated output** เสมอ (JSON via `response_format` หรือ tool-call)
3. **Cache aggressively** — system + tools + canonical wiki ผ่าน `cache_control`
4. **Few-shot from canonical wiki**, ไม่ใช่ hard-code ใน prompt
5. **No prompt without eval** — golden trace ก่อน promote

---

## 2. Prompt File Structure

```
src/auto_affi/agents/<agent_name>/
  prompts/
    system_v1.md          # current production
    system_v1.yaml        # metadata (model, thinking budget, tools)
    candidates/
      system_v2_draft.md  # candidate under eval
  tools/
    <tool_name>.py        # MCP tool implementation
  agent.py                # wires prompt + tools + model
  evals/
    golden_traces.jsonl   # 20+ test cases
    rubric.yaml           # scoring criteria
```

### 2.1 system_vN.md format
```markdown
---
agent: strategist
version: 1.0.0
model: claude-opus-4-7
extended_thinking_budget: 8000
cache_breakpoints: [system, tools, canonical_wiki]
last_updated: 2026-05-12
owner: ai-eng
linear_issue: AEG-145
---

# Role
You are the Strategist agent of Auto-Affi.

# Goal
...

# Hard rules (from canonical wiki)
1. ...
2. ...

# Process
1. ...

# Output schema
Match exactly: CampaignBrief (see schemas/campaign.py)
```

### 2.2 metadata yaml
```yaml
agent: strategist
version: 1.0.0
model: claude-opus-4-7
fallback_model: null         # null = no fallback for critical agents
extended_thinking:
  enabled: true
  budget_tokens: 8000
prompt_caching:
  breakpoints:
    - system_prompt
    - tool_definitions
    - canonical_wiki_retrieval
  ttl: 1h
tool_budget:
  max_calls_per_turn: 10
  hard_stop: 15
context_window:
  typical_input_tokens: 25000
  max_input_tokens: 40000
```

---

## 3. Versioning

### 3.1 Semantic version
- **Major** (X.0.0): breaking schema change in output
- **Minor** (1.X.0): behavior change (new rule, removed rule)
- **Patch** (1.0.X): wording tweak, same behavior

### 3.2 Lifecycle
1. **Candidate** — sits in `candidates/`, runs shadow eval
2. **Production** — promoted when eval gates pass (see §5)
3. **Archived** — old version moved to `archive/`, kept ≥ 6 months
4. **Deprecated** — flagged but still callable for 1 release

### 3.3 Promotion rules
- ⛔ ห้าม edit `system_vN.md` ของ production version โดยตรง
- ✅ Copy → `candidates/system_vN+1.md` → modify → eval → promote
- ✅ Promotion = PR with eval result attached + AI Eng approval + Nick Fury sign-off
- ⛔ Critical agents (Strategist, Director, Critic, Curator) ห้ามมี model fallback chain

---

## 4. Prompt Writing Discipline

### 4.1 Anthropic best practice
- Use XML-style tags สำหรับ section: `<role>`, `<goal>`, `<rules>`, `<process>`, `<output_format>`
- Constants / examples → จบ prompt (after cache breakpoint)
- Lists with explicit numbering for sequential reasoning
- Place schema definition before example output
- Long context → place primary instructions ที่ end

### 4.2 Cache breakpoints (max 4 ใช้ฉลาด)
Order (ที่เปลี่ยนน้อย → มาก):
1. **System prompt** (rarely change) — first breakpoint
2. **Tool definitions** (rarely change) — second
3. **Agent-specific KB / canonical wiki** (hourly change) — third
4. **Per-request wiki retrieval result** — NO cache (varies every call)

### 4.3 Extended thinking
- ใช้เฉพาะ 3 agent: Strategist (8k), Critic (6k), Curator (16k)
- Gate ถ้า task confidence > 0.85 หลัง initial pass → skip thinking
- ทุก thinking output → log to Langfuse for audit

### 4.4 Output discipline
- **Always JSON** for cross-boundary outputs
- Define output schema ทั้งใน prompt และใน pydantic
- Use Anthropic tool-use เพื่อบังคับ structure (ไม่ใช่ free-text JSON parsing)
- Stream OK, แต่ schema validation หลัง complete

### 4.5 Few-shot
- 2-5 examples max
- Examples ต้องสะท้อน production task จริง (ไม่ใช่ toy)
- Source examples จาก canonical wiki — ห้าม hard-code creative content
- Negative example (anti-pattern) ใส่ใน Critic / Safety prompt

### 4.6 Forbidden
- ❌ "Be creative" / "Think step by step" alone (vague)
- ❌ "Do not hallucinate" (doesn't work)
- ❌ Combine multiple tasks ใน 1 prompt (split into sub-agent)
- ❌ Prompt injection susceptible patterns — quote external content via XML wrapper
- ❌ PII / secret in prompt
- ❌ Hard-coded date (ใช้ template variable)

---

## 5. Evaluation Gates

### 5.1 ก่อน promote candidate → production

**Mandatory gates:**
- [ ] Golden trace set (≥ 20 case Phase 1, ≥ 100 Phase 3) runs pass
- [ ] No metric regress > 5% vs current production
- [ ] If uplift claimed → ≥ 5% uplift, p < 0.05, sample ≥ 200
- [ ] Manual review of 10 sample outputs by AI Eng
- [ ] Cost / latency within budget (per `llm-allocation.md`)
- [ ] Compliance check (no hallucinated rule, no forbidden topic)
- [ ] Nick Fury sign-off ใน PR

### 5.2 Shadow eval
- New candidate runs parallel กับ production บน 10% real traffic
- Compare outcome metrics 7 วันหลัง publish (ไม่ใช่ rubric เพียง)
- Promote เมื่อ outcome uplift ≥ 5%

### 5.3 Continuous regression
- ทุก PR ที่แตะ prompt directory → trigger eval run
- Block merge if regress
- Weekly canary: rerun golden traces เพื่อจับ model drift (Anthropic side)

---

## 6. Anti-Patterns (จาก research)

| Anti-pattern | ผลร้าย | กฎ |
|---|---|---|
| Mega-prompt (>10k token system) | Slow, expensive, hard to debug | Split into sub-agent |
| Hard-coded knowledge | Stale → wrong output | Move to wiki + RAG |
| No output schema | Parsing nightmare, silent error | Always schema-validated |
| Vibes-based eval | Drift undetected | Rubric + golden trace |
| Same prompt for multiple models | Quality variance | Per-model prompt variant |
| Direct edit of production prompt | No rollback, no eval | Candidate → eval → promote |
| Wiki write inside prompt instruction | Self-poisoning loop | Bilateral sync only |
| Catch-all "if you're unsure, do X" | Hides failure modes | Explicit decision tree |

---

## 7. Tool Definition Standards

ทุก MCP tool ต้องมี:
- **Name**: `<namespace>_<verb>_<noun>` (e.g., `shopee_search_products`)
- **Description**: ≤ 200 chars, ระบุ what + when to use
- **Input schema**: pydantic, all fields documented
- **Output schema**: `ToolResult` standard

ตัวอย่าง tool block:
```python
@tool(
    name="shopee_search_products",
    description="Search Shopee TH products by keyword. Returns up to 50 items with commission, price, rating. Use when scouting candidates.",
)
async def shopee_search_products(
    keyword: str,
    category: str | None = None,
    min_commission_pct: float = 3.0,
    limit: int = 50,
) -> ToolResult[list[ShopeeProduct]]:
    ...
```

---

## 8. Observability

### 8.1 Every prompt call must log
- `agent_name`, `prompt_version`, `model`, `input_tokens`, `output_tokens`, `cached_read_tokens`, `cached_write_tokens`, `cost_usd`, `latency_ms`, `trace_id`, `extended_thinking_used`
- Langfuse stores full trace
- Phoenix for creative output review
- Laminar for long workflow

### 8.2 Cost watcher
- Per-agent daily spend dashboard
- Alert if single call output > 50k tokens (possible infinite loop)
- Cache hit rate ≥ 70% SLO

---

## 9. Migration Playbook (New Anthropic Model)

ตัวอย่าง: Opus 4.8 ออก
1. **Shadow** — รัน new model ใน 5% Strategist traffic × 14 วัน
2. **Compare** — outcome uplift, cost delta, latency delta
3. **Decision**:
   - uplift > 5% + cost ≤ +20% → promote
   - uplift > 0 + cost ≥ +50% → ใช้ Critic/Curator only
   - uplift < 0 → keep old
4. **Rollout** — 5% → 25% → 100% over 7 วัน

---

## 10. Quick Reference

| Item | Rule |
|---|---|
| Edit production prompt | ⛔ — ใช้ candidate flow |
| Prompt cache | Always 3-4 breakpoints |
| Extended thinking | Strategist 8k / Critic 6k / Curator 16k only |
| Critical agent fallback model | ⛔ — retry only |
| Hard-code creative example | ⛔ — pull from wiki |
| Free-text JSON output | ⛔ — tool-use schema |
| Promote without eval | ⛔ — block merge |
| Comment in prompt | ✅ Markdown comments ok, ไม่ส่งไป API |
| Cost log | ✅ wajib (mandatory) |
| Linear link in PR | ✅ wajib |
