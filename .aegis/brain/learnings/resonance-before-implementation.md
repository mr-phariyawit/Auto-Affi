# Lesson: Enrich Resonance BEFORE Implementation Sprints

> Confidence: HIGH (validated across Sprint 3+4, 18 tasks, 0 re-debates)
> Source: 2026-05-13 session arc

## Pattern

When a sprint depends on domain knowledge, cost constraints, or
architectural principles: distill them into resonance files BEFORE
the sprint begins. The 30-minute investment eliminates mid-sprint
debates and judgment-call escalations.

## Evidence

Session 3 enriched resonance with 9 files from SPEC.md (cost-model,
autonomy-stance, learning-loop, domain-thai, etc.) before Sprints 3+4.

Result:
- BudgetCircuitBreaker thresholds came directly from cost-model.md
- Mega-sale calendar dates came from domain-thai.md
- Wiki tier thresholds came from learning-loop.md
- Kill switch design came from autonomy-stance.md
- Zero human escalations across 18 tasks

## Anti-pattern

Starting implementation before resonance is enriched forces agents to
re-read SPEC.md per-task, make ad-hoc threshold decisions, and risk
inconsistent values across modules.

## When to apply

- Before any sprint that introduces a new domain area
- Before any sprint that touches cost/budget/threshold logic
- Before any sprint that implements safety-critical features
