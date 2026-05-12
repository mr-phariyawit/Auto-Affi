# ADR-002: Schema Validation Strategy (Pydantic at Every Handoff)

- **Status**: Accepted
- **Date**: 2026-05-13
- **Deciders**: Nick Fury (Iron Man analysis, Loki review)
- **Source**: SPEC.md sections 6.1, 6.2, 8.2

## Context

Agent outputs range from product candidates to storyboard JSON to
publish records. Without validation, one agent's malformed output
silently corrupts the next agent's input, creating hard-to-debug
failures deep in the pipeline.

## Decision

**Every inter-agent handoff is Pydantic-validated. No free-form dicts cross boundaries.**

Key schema objects:
- `ProductCandidate` (Scout -> Strategist)
- `TrendSignal` (Trend Analyst -> Strategist)
- `CampaignBrief` (Strategist -> Writers Room)
- `Storyboard` (Writers Room -> Producer) -- complex JSON, SPEC 6.2
- `MasterVideo` (Producer -> Publisher)
- `PublishRecord` (Publisher -> Analytics)
- `WikiEntry` (Feedback Curator -> LLM Wiki)

Agent tool responses follow a universal contract (SPEC 8.2):
```json
{ "ok": true, "data": {...}, "cost_usd": 0.012, "latency_ms": 840, "trace_id": "..." }
```

## Rationale

- **Fail-fast**: Malformed output is caught at the boundary, not 3 stages later
- **Cost tracking**: `cost_usd` in every tool response enables per-video cost breakdown
- **Self-documenting**: Pydantic models serve as living documentation of the contract
- **LLM-friendly**: JSON schema can be injected into agent prompts as output format spec

## Consequences

- (+) Reliable pipeline -- invalid data never silently passes
- (+) Cost/latency tracking at tool level for free
- (+) Schema serves as documentation and test fixture generator
- (-) Schema evolution requires migration (mitigated by version field in Storyboard)
- (-) Slight overhead per handoff (negligible vs LLM call cost)

## Cross-references

- Resonance: `architecture-principles.md` (Principle 2)
- SPEC: section 6.2 (Storyboard JSON Schema), section 8.2 (Agent Tool Contract)
