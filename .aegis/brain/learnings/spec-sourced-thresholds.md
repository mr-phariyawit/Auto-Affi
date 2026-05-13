# Lesson: SPEC-Sourced Thresholds Reduce Escalations to Near-Zero

> Confidence: HIGH (validated across 4 sprints, 0 escalations)
> Source: 2026-05-13 session arc

## Pattern

Every configurable threshold in the codebase should trace to a SPEC
section or resonance file. When the SPEC provides a number, use it
verbatim. When the SPEC provides a range, use the conservative bound.
Never invent numbers that could trigger MBP escalation.

## Evidence

Sprint 4 thresholds, all SPEC-sourced:
- Kill switch auto-kill: 3 violations/24h (SPEC 10.4)
- Editor budget cap: $0.40 (SPEC 3.5.1)
- Daily budget cap: $50 (NFR-CS-03)
- Per-video target: $2.87 (SPEC Appendix C)
- Alert multiplier: 1.5x (SPEC 11.3)
- Wiki tiers: 5/20/3 evidence counts (SPEC 5.2)
- Mega-sale window: 14 days (SPEC via FR-ST-03)

Result: 0 judgment-call escalations, 0 human-queue items.

## Anti-pattern

Inventing threshold values ("let's set the cap at $0.50") creates
a judgment-call that should be logged, may need Captain America
fallback, and can be second-guessed in retro. SPEC numbers are
pre-approved by definition.

## When to apply

- Always, for any configurable value in production code
- Especially for cost, safety, and compliance thresholds
