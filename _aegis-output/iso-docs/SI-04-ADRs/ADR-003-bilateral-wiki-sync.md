# ADR-003: Bilateral Wiki Sync (Review Queue + Safety Promotion)

- **Status**: Accepted
- **Date**: 2026-05-13
- **Deciders**: Nick Fury (Iron Man analysis, Loki review)
- **Source**: SPEC.md sections 5.1-5.3, 3.8, 3.9

## Context

The LLM Wiki is the shared brain. If any agent can write directly to
canonical entries, a single hallucinated pattern could corrupt the
knowledge base and degrade all future pipeline runs.

## Decision

**Two-path sync:**
1. **Write path**: Agents (specifically Feedback Curator, SPEC 3.8) write
   to a review queue only. Never directly to canonical wiki.
2. **Promote path**: Safety agent (SPEC 3.9) or human supervisor promotes
   entries from the review queue to canonical tier.

## Rationale

- **Knowledge integrity**: Prevents a single agent from poisoning shared knowledge
- **Audit trail**: Every canonical entry has a promotion record (who approved, when)
- **Tiered confidence**: Entries start as Hypothesis (1-2 evidence), only reach
  Canonical (20+ evidence) through accumulated validation
- **Human oversight**: Aligns with "human as supervisor" stance -- humans can
  intercept bad patterns before they become hard rules

## Entry Lifecycle

```
Feedback Curator writes WikiEntry (Hypothesis tier)
  -> Review Queue
  -> Safety Agent reviews (or human)
  -> IF approved: promote to Validated/Canonical
  -> IF rejected: mark as Deprecated with rationale
```

## Consequences

- (+) Wiki integrity preserved -- no single-agent poisoning
- (+) Audit trail for every canonical entry
- (+) Aligns with tiering system (Hypothesis -> Validated -> Canonical -> Deprecated)
- (-) 24h+ latency before new patterns become available (mitigated: Hypothesis tier
  still injected as "tentative" hints immediately)
- (-) Requires Safety agent or human to actively review queue (Phase 1: human only,
  since Safety agent is Phase 2)

## Phase 1 Implication

Safety agent is not live in Phase 1. Wiki promotion falls to human supervisor.
This means the review queue must be visible in the ops console dashboard.
Phase 1 human intervention rate target (30%) accounts for this manual review load.

## Cross-references

- Resonance: `architecture-principles.md` (Principle 3), `autonomy-stance.md`
- Resonance: `learning-loop.md` (full wiki mechanics)
