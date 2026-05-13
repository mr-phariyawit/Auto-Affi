# PM.01 Project Plan -- Auto-Affi

> Adapted from `docs/pm/project-plan.md` (ISO 29110 guideline-mode).
> This is the AEGIS BLOCK 0 canonical copy. Source of truth for live updates: Linear.

- **Project**: Auto-Affi -- Autonomous AI Marketing Platform (Shopee Affiliate, TH)
- **Project Manager**: Nick Fury (aegis-team)
- **Compliance**: ISO/IEC 29110 Basic (guideline-mode, not audit-ready)
- **Created**: 2026-05-13
- **Baseline from**: `docs/pm/project-plan.md` (2026-05-12)

---

## 1. Project Identity

- **Name**: Auto-Affi
- **One-line purpose**: AI agent crew that autonomously scouts Shopee products, creates Thai-native 9:16 videos, publishes to social platforms with affiliate links, collects metrics, and self-improves through an LLM Wiki feedback loop.
- **Vision**: Build an "AI Marketing Company" operating 24/7 -- from product discovery to video production to publishing to self-learning -- with humans as supervisors only.
- **North-star KPIs**: Videos/day, cost/video, CTR on affiliate link, monthly GMV, human intervention rate.

## 2. Scope

- **Functional scope**: See SI-01 (Requirements Specification) -- 50+ requirements across 10 subsystems.
- **Out-of-scope**: See `docs/pm/sow.md` Exclusions.
- **Subsystems**: Agent Crew (9 agents), Temporal Orchestrator, Asset Pipeline, Data Plane, Publishing Plane, Learning Loop (LLM Wiki).

## 3. Schedule (High-Level Baseline)

| Phase | Window | Exit Criteria | Status |
|-------|--------|---------------|--------|
| **Phase 0** -- PM setup | Week 0 | Linear board ready, Tier 1 docs merged, repo skeleton | COMPLETE |
| **Phase 1** -- Single closed loop | Week 1-6 | Beauty niche x 5 video/day x loop complete x GMV >= $200/14d | COMPLETE (Sprint 1-6, 163pt) |
| **Phase 1.5** -- ADR-007 Studio Workflow | Week 6-8 | 10-stage production pipeline operational | COMPLETE (Sprint 7-9, 40pt) |
| **Phase 1.6** -- MANUAL mode launch prep | Week 8-9 | Kill-switch, LLM storyboard, cron, monitoring | IN PROGRESS (Sprint 10, 10pt) |
| **Phase 2** -- Multi-platform + portfolio | Week 10-17 | FB+IG+YT live, Writers' Room debate panel | PLANNED |
| **Phase 3** -- Self-improving autonomous | Week 18-27 | Harness-evolver online, MoM CTR uplift >= 5% | PLANNED |

### Sprint History (updated 2026-05-13)

| Sprint | Points | Tests | Key Deliverables |
|--------|--------|-------|-----------------|
| 1 | 26 | 121 | Scout + Strategy |
| 2 | 28 | 214 | Writers' Room + Video Production |
| 3 | 27 | 322 | Publishing + Analytics |
| 4 | 27 | 377 | Wiki/Feedback + Safety + Orchestration |
| 5 | 27 | 451 | Phase 1 close-out + Phase 2 foundation |
| 6 | 28 | 481 | Ops Console + Multi-platform + Deploy |
| 7 | 16 | 509 | ADR-007 stages 1-3 (creative direction) |
| 8 | 14 | 543 | ADR-007 stages 4-7 (asset production) |
| 9 | 10 | 557 | ADR-007 stages 8-10 (post-prod + publish) |
| 10 | 10 | 605+ | MANUAL mode: kill-switch, LLM storyboard, cron, monitoring |

## 4. Roles & Responsibilities

| Role | Owner | Scope |
|------|-------|-------|
| Project Manager | Nick Fury | Plan, Linear, escalation, status |
| Tech Lead | TBD | Architecture decisions, code review |
| AI / Prompt Eng | TBD | Agent prompts, eval, wiki curation |
| Video Pipeline Eng | TBD | Editor + Hyperframe + ffmpeg + ASR |
| Ops / Safety | TBD | Publishing accounts, compliance, kill switches |

## 5. Budget Frame (Phase 1)

| Item | Monthly Allocation |
|------|--------------------|
| LLM (Claude) | $500 |
| kie.ai (Veo/Sora/Flux/Suno) | $400 |
| ElevenLabs TTS | $99 |
| Infra (Postgres + Redis + Temporal + S3) | $200 |
| Self-host GPU (Whisper / Typhoon) | $300 |
| Tooling (Langfuse + Linear + Sentry) | $150 |
| Contingency (10%) | $165 |
| **Phase 1 monthly total** | **$1,800** |

Hard cap: throttle at 80%, kill at 110%.

## 6. Risk Management

- Register: `docs/pm/risk-register.md` (20 risks, R-01 through R-20)
- Top risks (exposure >= 15): R-02 (account suspension, 16), R-03 (OCPB/PDPC violation, 15), R-17 (wiki self-poisoning, 15)
- Review cadence: weekly

## 7. Quality Plan

- Test plan: `docs/si/test-plan.md` (4-layer: unit, integration, agent eval, e2e)
- Coding standards: `docs/si/coding-standards.md`
- Prompt standards: `docs/si/prompt-standards.md`
- Coverage target: >= 70% on adapters + workflows

## 8. Communication

- Linear = single source of truth for task/bug/CR
- GitHub = code + spec docs + PR review
- Standup = daily async in Linear; weekly sync 30 min

## 9. Version Control

- Branch model: trunk-based (`main` protected, `claude/<slug>` for AI branches)
- Commit format: Conventional Commits
- PR rules: >= 1 review required, squash merge default

## 10. Backup / Continuity

- GitHub remote = primary code
- Postgres / S3: daily snapshot, 30-day retention
- Wiki vector store: weekly dump to S3
