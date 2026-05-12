# Non-Goals -- What We Explicitly Will NOT Build

> Source: SPEC.md section 1.3, plus inferred from sections 13 and 15
> Last synced: 2026-05-13
> Purpose: Prevent scope creep. Every agent must know the boundaries.
> Non-goals are not permanent rejections -- they have sunset dates.

## Phase 1 Non-Goals (expire at Phase 2 start, Week 7)

| Non-Goal | Rationale | Sunset |
|----------|-----------|--------|
| Creator marketplace (human creators in loop) | SPEC 1.3: "no human creator in loop" -- system is fully AI | Never (permanent) |
| Paid ads / ad spend | SPEC 1.3: "organic-only in Phase 1" | Phase 2 or later |
| Multi-tenant SaaS | SPEC 1.3: "no multi-tenant SaaS in Phase 1" | Phase 3 or later |
| Multi-niche (beyond Beauty) | SPEC 13 Phase 1: "beauty niche only" | Phase 2 (portfolio expansion) |
| Multi-platform publishing | SPEC 13 Phase 1: "IG Reel only" | Phase 2 (add FB Reels + YT Shorts) |
| Full Writers Room debate | SPEC 13 Phase 1: "1 Writer agent, no debate" | Phase 2 (5 sub-agents + critic) |
| Knowledge Graph layer | SPEC 13 Phase 1: "simple wiki, vector store, no KG" | Phase 2 |
| Multi-vendor video gen | SPEC 13 Phase 1: "Veo 3 only" | Phase 2 (adapter pattern) |
| Safety agent | SPEC 13 Phase 1: not listed in MVP scope | Phase 2 |
| Trend Analyst agent | SPEC 13 Phase 1: not listed in MVP scope | Phase 2 |

## Permanent Non-Goals (no sunset)

| Non-Goal | Rationale |
|----------|-----------|
| Human creator marketplace | The system IS the creator. No human content production in the loop ever. |
| Manual content creation workflows | The entire pipeline is autonomous. Manual creation tools are out of scope. |

## How to read this file

- If a non-goal has a "Sunset" date, it becomes a GOAL at that phase
- Agents must NOT build toward sunset items prematurely
- If an agent's task touches a non-goal, STOP and check:
  1. Is the non-goal permanent? -> Hard reject
  2. Is it phase-gated and we are in that phase? -> Proceed
  3. Is it phase-gated and we are NOT in that phase? -> Reject with explanation

## Loki Review Notes

The non-goals are internally consistent. The "multi-tenant SaaS" item is
correctly phase-gated (not permanent) because the SPEC implies multi-account
scaling in Phase 3. "Creator marketplace" is correctly permanent because the
SPEC vision (1.1) is an AI-only system where "humans are supervisors only."
