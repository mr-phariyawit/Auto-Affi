# Architecture Principles

> Source: SPEC.md sections 2, 3, 4, 7, Appendix B
> Last synced: 2026-05-13
> Purpose: Architectural invariants that constrain every design decision.
> Cross-references to ADRs where formal decisions are recorded.

## The 5 Core Principles

### 1. Agent Hierarchy, Not Peer Mesh
Strict handoff chain. No agent-to-agent side channels. The Director in
Writers Room has final decision authority. The Orchestrator (Temporal)
sequences all activities. This prevents deadlocks, makes tracing
deterministic, and ensures every decision has one accountable agent.

See: ADR-001 (Agent Hierarchy vs Peer Mesh)

### 2. Schema-Validated Boundaries (Pydantic at Every Handoff)
Every inter-agent handoff uses a Pydantic model. No free-form dicts.
Key schemas from SPEC:
- `ProductCandidate` (Scout -> Strategist)
- `TrendSignal` (Trend Analyst -> Strategist)
- `CampaignBrief` (Strategist -> Writers Room)
- `Storyboard` (Writers Room -> Producer)
- `MasterVideo` (Producer -> Publisher)
- `PublishRecord` (Publisher -> Analytics)
- `WikiEntry` (Feedback Curator -> LLM Wiki)

Agent tool responses also follow a strict contract (SPEC 8.2):
`{ "ok": true, "data": {...}, "cost_usd": 0.012, "latency_ms": 840, "trace_id": "..." }`

See: ADR-002 (Schema Validation Strategy)

### 3. Bilateral Wiki Sync
The LLM Wiki is the shared brain. Two rules:
- **Write path**: Agents write to a review queue only (never direct to canonical)
- **Promote path**: Safety agent (or human supervisor) promotes from review queue to canonical wiki
This prevents poisoning the shared knowledge base with hallucinated patterns.

See: ADR-003 (Bilateral Wiki Sync)

### 4. Cost-Aware Execution
Every activity has a budget. Specifics from SPEC:
- Per-video total target: <= $2.87 (Phase 1, Appendix C)
- Editor agent token cost gate: $0.40/video max -- fallback to deterministic FFmpeg if exceeded
- Daily budget controller: auto-stop generation when daily cost > budget * 1.1
- Per-scene cost caps through Producer agent
- Tool response includes `cost_usd` for tracking

See: ADR-004 (Cost Control Architecture)

### 5. Thai-First Content
All scripts, captions, and content in native Thai. No transliteration.
Filler words to detect/remove: ["eee", "eum", "a", "aa"] (Thai phonetic).
Disclosure requirements: `#advertising` / `#affiliate` per NBTC / Shopee ToS.
Thai mega-sale calendar awareness (11.11, 12.12, Songkran, etc.) for timing.

## Additional Architectural Constraints

### Temporal as Orchestrator (SPEC 2, 4, 7)
- All workflows are Temporal Workflows -- durable, replayable, retry-safe
- Every activity is idempotent + checkpointed
- Custom multi-agent orchestration on top of Claude tool-use + Temporal
- Rationale (SPEC 7): "durable, replayable; don't depend on frameworks that may die fast"

### Multi-Vendor Abstraction (SPEC 7)
- Video gen: abstracted behind `VideoGenAdapter` (Veo 3, Runway Gen-3, Kling)
- Image gen: adapter pattern (Flux 1.1 Pro, Imagen 3, SDXL)
- TTS: ElevenLabs primary, Azure fallback
- This allows cost/quality tradeoff per scene and vendor failover

### Observability First (SPEC 11)
- OpenTelemetry trace covers: workflow -> activity -> agent call -> tool call
- Span attributes: agent.name, model, input/output tokens, cost_usd, cache_hit
- LLM eval harness: offline replay + golden set (100 cases) + A/B traffic split

## Subsystem Map (SPEC 2.1)

```
1. Orchestrator      -- Temporal Workflows (schedule, retries, DAG, timers)
2. Agent Crew        -- Claude-based agents, each with role/tools/memory
3. Asset Pipeline    -- image gen + video gen + TTS + lipsync + composition
4. Data Plane        -- Postgres (OLTP) + pgvector (semantic) + S3 (assets) + ClickHouse (analytics)
5. Publishing Plane  -- Meta Graph API, IG Content Publishing API, YouTube Data API v3
6. Learning Loop     -- Feedback Curator -> LLM Wiki -> context injection in next run
7. Shared Context Bus -- Postgres + Redis (session, rate limit, lightweight queues)
8. Ops Console       -- Next.js 15 + shadcn/ui (internal supervisor dashboard)
```
