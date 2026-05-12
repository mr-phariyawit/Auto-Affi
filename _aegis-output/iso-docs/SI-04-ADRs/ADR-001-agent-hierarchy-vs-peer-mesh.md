# ADR-001: Agent Hierarchy vs Peer Mesh

- **Status**: Accepted
- **Date**: 2026-05-13
- **Deciders**: Nick Fury (Iron Man analysis, Loki review)
- **Source**: SPEC.md sections 2, 3.4, 4

## Context

The Auto-Affi agent crew needs a communication topology. Two options:
1. **Peer mesh**: Any agent can call any other agent directly
2. **Strict hierarchy**: Agents follow a handoff chain with clear authority

## Decision

**Strict hierarchy with Director authority in Writers Room.**

The Orchestrator (Temporal) sequences all activities. Within the Writers Room,
the Director has final decision authority after debate. No agent-to-agent
side channels exist outside the defined handoff chain.

## Rationale

- **Traceability**: Every decision has one accountable agent. OpenTelemetry traces
  are linear (workflow -> activity -> agent -> tool), not a graph.
- **Deadlock prevention**: Peer mesh with cyclic dependencies causes hangs.
  Hierarchy is DAG-structured.
- **Cost control**: Side channels create untracked LLM calls. Hierarchy ensures
  every call goes through the pipeline and is budgeted.
- **Debuggability**: When a video flops, the postmortem follows the chain.
  Which agent made which decision is unambiguous.

## Consequences

- (+) Clear accountability per stage
- (+) OpenTelemetry tracing is straightforward
- (+) Cost tracking at tool/agent level is reliable
- (-) Less creative serendipity than peer mesh (mitigated by Writers Room debate)
- (-) Single point of failure at Director level (mitigated by Critic red-teaming)

## Cross-references

- Resonance: `agent-hierarchy.md`, `architecture-principles.md` (Principle 1)
