# ADR-004: Cost Control Architecture (Per-Node Budgets + Circuit-Breakers)

- **Status**: Accepted
- **Date**: 2026-05-13
- **Deciders**: Nick Fury (Iron Man analysis, Loki review)
- **Source**: SPEC.md sections 3.5.1, 9.1, 11.3, Appendix C

## Context

At Phase 3 scale (100+ videos/day at $0.80/video), the system processes
$80+/day in generation costs. Without granular cost control, a single
runaway agent or generator failure could burn through the daily budget
in minutes.

## Decision

**Three-layer cost control:**

### Layer 1: Per-Node Budget Caps
Every pipeline stage has a cost cap (SPEC Appendix C):
- Scout + Strategist LLM: $0.05
- Writer LLM: $0.10
- Editor agent: $0.30 (hard cap $0.40 -- SPEC 3.5.1)
- Image gen (8 scenes): $0.25
- Video gen (Veo): $1.80
- TTS (60s): $0.18
- ASR: $0.02
- Hyperframe: $0.05
- Compose + storage: $0.05
- Metrics + wiki: $0.07

### Layer 2: Circuit-Breakers
- Editor agent: stop AI editing at $0.40, fall back to FFmpeg
- Daily budget: auto-stop at budget * 1.1
- Cost alert: flag at target * 1.5

### Layer 3: Cost Tracking
- Every tool response includes `cost_usd` (SPEC 8.2)
- Per-video cost breakdown dashboard (SPEC 11.3)
- Feedback Curator correlates cost with outcome quality

## Rationale

- **Predictable economics**: Total per-video cost is bounded and measurable
- **Graceful degradation**: Circuit-breakers fall back to cheaper alternatives
  (FFmpeg, stock footage) rather than halting entirely
- **Data-driven optimization**: Per-tool cost tracking enables the Phase 3
  cost-aware planner to choose cheapest-adequate generator per scene

## Consequences

- (+) No runaway costs -- bounded per-video and per-day
- (+) Fallback recipes maintain throughput at lower quality
- (+) Cost data feeds learning loop for optimization
- (-) Fallback to FFmpeg reduces quality (acceptable for cost protection)
- (-) Auto-stop at daily budget requires human to re-enable (by design)

## Cross-references

- Resonance: `cost-model.md` (detailed breakdown), `architecture-principles.md` (Principle 4)
