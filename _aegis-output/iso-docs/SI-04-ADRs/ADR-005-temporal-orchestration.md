# ADR-005: Temporal as Orchestration Engine

- **Status**: Accepted
- **Date**: 2026-05-13
- **Deciders**: Nick Fury (Iron Man analysis, Loki review)
- **Source**: SPEC.md sections 2, 4, 7

## Context

The Auto-Affi pipeline involves long-running workflows (video generation
can take 30+ minutes), multiple retry scenarios (API failures, rate limits),
scheduled cadences (discovery every 6h, learning every 24h), and complex
DAG dependencies. We need an orchestration engine that handles all of these
durably.

## Options Considered

1. **Temporal Workflows** -- durable, replayable, retry-safe, long-running
2. **Celery + Redis** -- simple task queue, no native workflow state
3. **Airflow** -- DAG scheduler, poor fit for event-driven agent work
4. **Custom async** -- full control, high maintenance burden

## Decision

**Temporal Workflows** with custom multi-agent orchestration on top of
Claude tool-use.

SPEC 7 rationale (verbatim): "Durable, replayable; don't depend on
frameworks that may die fast."

## Key Workflows (SPEC 4)

```
DiscoveryWorkflow     (cron: 4x/day)
CampaignWorkflow      (per accepted candidate -- main pipeline)
LearningWorkflow      (cron: nightly)
MetricsPollWorkflow   (scheduled: 1h/6h/24h/7d/30d)
```

## Durability Guarantees (SPEC 4)

- Every activity is idempotent + checkpointed at Temporal
- If video gen times out at 30 minutes, workflow resumes from checkpoint
- Retry policies configurable per activity type
- Scheduled workflows via Temporal Schedules (not external cron)

## Consequences

- (+) Durable execution -- no lost work on crashes
- (+) Built-in retry, timeout, and schedule management
- (+) Replayable -- can debug any workflow execution after the fact
- (+) Temporal UI provides free observability for workflow state
- (-) Operational complexity of running Temporal cluster
- (-) Learning curve for Temporal SDK patterns
- (-) Vendor lock-in to Temporal (mitigated: open source, self-hostable)

## Cross-references

- Resonance: `architecture-principles.md` (Temporal as Orchestrator section)
- Resonance: `agent-hierarchy.md` (pipeline order matches workflow activities)
