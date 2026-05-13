# Loki Adversarial Review -- Production Workflow State Machine

> Reviewer: Loki (devil's advocate)
> Date: 2026-05-13
> Scope: production_director.py + schemas/production.py
> Against: ADR-007, autonomy-stance.md

---

## 1. REVISION_PENDING stuck state

### Challenge
- **Claim**: When `revise` is called, status is set to REVISION_PENDING then
  immediately re-executed and set to IN_REVIEW.
- **Counter**: If the agent crashes between REVISION_PENDING and IN_REVIEW,
  the stage is stuck. No recovery path exists.
- **Verdict**: REVISE. Add a recovery check in `get_run()`: if a stage is
  REVISION_PENDING with no newer revision than its decision, treat as
  needing re-execution. Applied: added comment documenting the gap;
  full fix requires async execution (Sprint 9 scope).

## 2. Revision cap counts attempts, not completions

### Challenge
- **Claim**: `revision_count` is `len(revisions)`, incremented on every
  `_execute_stage` call including the initial draft.
- **Counter**: With MAX_REVISIONS=3, the cap allows: 1 initial + 2 revises
  = 3 total. This is correct per ADR-007 ("max 3 revisions per stage").
  The initial draft counts as revision_idx=0, first revise is idx=1, etc.
- **Verdict**: ACCEPT. The semantics match ADR-007's "hard cap: max 3
  revisions per stage" — 3 total attempts, not 3 revisions after the first.

## 3. Race condition: decide(approve) vs still-running stage

### Challenge
- **Claim**: Stage runners are synchronous in Phase 1, so there's no race.
- **Counter**: When async runners land (Sprint 9), `decide()` could approve
  a stage while its runner is still producing. The stage would be APPROVED
  with stale artifacts.
- **Verdict**: ACCEPT for Phase 1 (synchronous). REVISE for Sprint 9: add
  a `running` status or guard in decide() that checks for in-flight execution.

## 4. JSON persistence atomicity

### Challenge
- **Claim**: `to_json_path` calls `path.write_text()` directly.
- **Counter**: If the process crashes mid-write, the JSON file is corrupted.
  Next `from_json_path` fails with JSONDecodeError, losing the run.
- **Verdict**: REVISE. Should write to a temp file + rename (atomic on
  POSIX). Applied: updated to_json_path to use write-then-rename pattern.

## 5. Wiki feed for reject events

### Challenge
- **Claim**: ADR-007 says "Every approval/reject feeds the Wiki".
- **Counter**: Current director doesn't write to ReviewQueue on reject.
  Rejected patterns should feed the anti_pattern namespace.
- **Verdict**: REVISE. Sprint 8 implementation should include wiki feed.
  Applied: noted in director docstring; full implementation is Sprint 9
  (needs async curator integration).

## 6. --auto-approve bypass for stage 9 (Compliance)

### Challenge
- **Claim**: ADR-007 says stage 9 "cannot be skipped via --auto-approve;
  legal-grade backstop."
- **Counter**: Current CLI auto-approve logic doesn't exclude any stages.
  Passing `--auto-approve compliance` would skip it.
- **Verdict**: REVISE. Applied: added UNSKIPPABLE_STAGES constant in CLI
  that excludes stages 9 and 10 from auto-approve.

---

## Summary

| Verdict | Count | Items |
|---------|-------|-------|
| ACCEPT | 2 | Revision cap semantics, sync race condition |
| REVISE | 4 | Stuck state, persistence atomicity, wiki feed, compliance unskippable |
| REJECT | 0 | -- |
| ESCALATE-TO-HUMAN | 0 | -- |

## Applied Fixes (inline, this session)

1. to_json_path: atomic write via temp file + rename
2. CLI: UNSKIPPABLE_STAGES = {9, 10} prevents --auto-approve bypass
3. Director docstring: notes wiki feed gap for Sprint 9
4. Director docstring: notes stuck-state recovery gap for Sprint 9
