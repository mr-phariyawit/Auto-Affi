# Sprint 1 — Kanban

> Updated: 2026-06-08 19:40 | Goal: green offline pipeline vertical slice (0 paid calls)
> Gate-aware: live-outcome tasks are BLOCKED on human gates G1–G4 (see human-queue.md).

## BLOCKED — human gates (critical path, not engineering)

| ID | Gate | Category | Owner |
|----|------|----------|-------|
| G1 | Shopee Affiliate Program TH (apply) | External | @human |
| G2 | Meta Business + IG Creator + 60-day token | External | @human |
| G3 | Higgsfield account + credits | External | @human |
| G4 | Runtime host decision | Identity | @human |

## TODO (8 tasks, 27 pts)

| ID | Title | Pts | Assignee | Priority |
|----|-------|-----|----------|----------|
| AFFI-S1-01 | Restore build infra (pyproject/uv/pytest) | 3 | @spider-man | high |
| AFFI-S1-02 | Core schemas + tool-result contract | 3 | @spider-man | high |
| AFFI-S1-03 | Local JSONL/CSV registry + run model | 2 | @spider-man | high |
| AFFI-S1-04 | Shopee adapter (dry-run) + Scout scoring | 3 | @spider-man | med |
| AFFI-S1-05 | Strategist + Writer + Storyboard + rubric lint | 5 | @spider-man | med |
| AFFI-S1-06 | Producer/Editor + pipeline + Higgsfield CLI (dry-run) + cost caps | 5 | @spider-man | med |
| AFFI-S1-07 | Compliance gate (cleanroom + speed-guard + caption/VO sync) | 3 | @spider-man | high |
| AFFI-S1-08 | Offline vertical slice on 1 fixture product | 3 | @spider-man | med |

## IN_PROGRESS (0)

| ID | Title | Pts | Assignee | Priority |
|----|-------|-----|----------|----------|

## DONE (0)

| ID | Title | Pts | Assignee | Priority |
|----|-------|-----|----------|----------|

## REVIEW (0)

| ID | Title | Pts | Assignee | Gate |
|----|-------|-----|----------|------|

---
_Dependency order: S1-01 → S1-02 → (S1-03, S1-04) → S1-05 → S1-06 → S1-07 → S1-08._
_BLOCK 0 cleared: PM-01, SI-01, SI-02, breakdown, kanban all present (2026-06-08)._
