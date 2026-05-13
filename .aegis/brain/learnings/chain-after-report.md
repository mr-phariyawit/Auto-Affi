# Lesson: Apply Chain After Sub-Agent Reports -- Never Hold

> Confidence: HIGH (violation observed + corrected in session)
> Source: 2026-05-13 session arc, board correction

## Pattern

When a sub-agent completes and reports back, the orchestrator MUST
apply the command chain (next task from kanban, next sprint if done,
retro if sprint closed). Never end a response with "awaiting direction"
or "holding for your move."

This is Golden Rule #7 + command-chain.md in practice.

## Evidence

Early in session-3, the orchestrator paused after Sprint 3 planning
with an implicit "your call" stance. Board corrected: "Don't come
back to me for sprint-scope re-approval." After correction, Sprints
3+4 ran autonomously with zero pauses.

## Anti-pattern

- Ending with "Options: A/B/C -- what do you want?"
- Ending with "Sprint planned. Shall I proceed?"
- Ending with "Awaiting direction on next sprint"

All violate MBP and L3 autonomy contract.

## When to apply

- After EVERY sub-agent report
- After EVERY sprint close
- After EVERY task completion
- The only legal pause is an MBP escalation in the 4 allowed categories
