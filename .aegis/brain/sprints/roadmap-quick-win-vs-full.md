# Roadmap — Quick-Win Path vs Full Platform Path

> Two parallel tracks. Quick-win = first $1 of real GMV in 2-3 weeks.
> Full platform = SPEC.md Phase 1→3 over ~24 weeks.
> They DO NOT conflict — run both.

- **Created**: 2026-05-13
- **Owner**: mr.phariyawit@gmail.com
- **State at creation**: 108/131 pt code shipped (82 %), 0 real revenue, 0 deployed runtime

---

## Where we stand right now

| Asset | Status | Where |
|---|---|---|
| Scout (Shopee adapter + scoring + dedup) | ✅ coded | `src/auto_affi/adapters/shopee.py` + `agents/scout_scoring.py` |
| Strategy (CampaignBrief + Wiki RAG + mega-sale calendar) | ✅ coded | `agents/strategist.py` + `wiki/retriever.py` |
| Writers' Room (single Writer + storyboard schema) | ✅ coded (debate panel deferred) | `schemas/storyboard.py` |
| Video Production (kie.ai adapter + local fallback + editor passes + budget cap) | ✅ coded | `adapters/video_gen.py` + `pipeline/*` |
| Publishing (IG Reels + FB + YT stubs + scheduler + captions + subIds) | ✅ coded | `adapters/publisher.py` + `agents/posting_scheduler.py` |
| Analytics (5 poll schedules + outcome labels + click attribution) | ✅ coded | `agents/analytics_collector.py` + `schemas/metrics.py` |
| Wiki + Curator + Tier promotion + Replay | ✅ coded | `wiki/*` |
| Safety (claim audit + safety gate + kill switches + music license) | ✅ coded | `agents/safety_gate.py` + `agents/kill_switch.py` |
| Orchestration (workflow DAGs + in-process executor + budget circuit-breaker) | ✅ coded | `workflows/*` |
| Local mp4 demo (proven offline end-to-end) | ✅ working | `out/demo.mp4` |
| **Real API credentials** (Shopee, Meta, kie.ai, ElevenLabs, Anthropic) | ❌ MISSING | none |
| **Deployed runtime** (where it ticks 24/7) | ❌ MISSING | none |
| **First product picks** (real Shopee TH Beauty SKUs) | ❌ MISSING | none |
| **Monitoring/dashboard** | ❌ MISSING (Ops Console = Phase 2) | none |

---

## TRACK A — Quick-Win Path · "First $1 of real GMV"

**Goal**: prove the loop end-to-end with REAL money. 1 product. 1 video/day. 1 platform (IG Reels). Human approval gate on every post.

**Timeline**: 2-3 weeks elapsed. ~5 pt of code + heavy vendor-onboarding work.

**Success criteria**:
- ≥ 1 real post live on a real Shopee-tagged IG Reel
- ≥ 1 real click recorded with real subId attribution
- ≥ 1 real Shopee commission recorded (any amount, even ฿1)
- Kill switch validated by deliberately triggering once

### Quick-win work plan

| # | Item | Type | Owner | ETA | Blocks |
|---|---|---|---|---|---|
| QW-1 | Apply to Shopee Affiliate Program TH | vendor onboarding | human | 1-7 days | everything |
| QW-2 | Create Meta Business + IG Creator account + get long-lived Graph token (60d) | vendor onboarding | human | 1-2 days | publishing |
| QW-3 | Sign up kie.ai + buy credits ($20 floor for testing) | vendor onboarding | human | 30 min | premium video |
| QW-4 | Sign up ElevenLabs + buy starter ($5/mo) for Thai voice | vendor onboarding | human | 30 min | premium voice |
| QW-5 | Populate `.env` from `.env.example` with all keys | config | human + code | 30 min | runtime |
| QW-6 | Manual: pick 5-10 candidate Beauty products from Shopee TH (use the seed list) | curation | human | 1 hr | Scout seed |
| QW-7 | Code: wire `kill_switch` requires_human_approval=true on Publisher | 1 pt | spider-man | 2 hr | safety gate |
| QW-8 | Code: CLI wrapper `python -m auto_affi.ops.run_once --product <id>` (end-to-end manual ticker) | 2 pt | spider-man | 4 hr | repeatability |
| QW-9 | Deploy: pick the simplest viable runtime — your laptop's `cron` to run `run_once` once/day at the optimal Thai posting window | 1 pt + 1 day | thor | 1 day | 24/7 ops |
| QW-10 | Monitoring lite: a single Notion / Google Sheet dashboard pulling daily from `metrics_collector` JSONL output | 1 pt | spider-man | 3 hr | visibility |
| QW-11 | Run the first 3 posts MANUALLY-approved end-to-end | live ops | board + nick | 3 days | proof |
| QW-12 | Capture first real subId click (use a 2-tab self-test if needed before organic clicks arrive) | live ops | board | first day | attribution proof |
| QW-13 | Capture first real Shopee commission (any amount) | live ops | board + Shopee delay | 7-30 days | revenue proof |

**Code burden**: 5 pt (QW-7 + QW-8 + QW-9 + QW-10).
**Real work burden**: 80 % is vendor onboarding + ops, NOT code.

### Quick-win risk register

| Risk | Mitigation |
|---|---|
| Shopee Affiliate application rejected for new accounts | Apply early; fall back to Lazada Affiliate as alt (similar API surface) |
| Meta IG long-lived token expires every 60 days | Add token-refresh cron; document in `docs/runbook-tokens.md` |
| First videos blocked by IG community-standards (Thai beauty claims) | claim_auditor + safety_gate already enforce SPEC §10 — but EXPECT first 1-3 rejections; iterate |
| kie.ai cost overruns | `editor_budget.py` cap at $0.40/video already enforced; circuit-breaker at $5/day for QW phase |
| Zero clicks first week (cold start) | This IS the data — Curator records the flop, Wiki marks the pattern as Hypothesis→Deprecated, next cycle adjusts |

### What quick-win INTENTIONALLY skips
- Self-improvement loop ticking automatically (we'll review by hand for first 2 weeks)
- Multi-platform breadth (IG-only — FB + YT come Phase 2)
- Writers' Room debate panel (single Writer is fine for daily cadence)
- Ops Console (Notion sheet replaces it)
- Hyperframe overlay (basic 9:16 + caption + endcard is publish-quality enough)
- Multi-vendor video gen failover (kie.ai only; local fallback only if kie.ai is down)

---

## TRACK B — Full Platform Path · SPEC.md Phase 1 → 3

**Goal**: hit SPEC Phase 3 KPIs — 100+ videos/day, ≥4 % CTR, $50k+ GMV/month, ≤5 % human intervention.

**Timeline**: ~24 weeks elapsed (SPEC explicit Phase breakdown).

**Success criteria**: see `.aegis/brain/resonance/north-stars.md`.

### Full-platform work plan

| Phase | Weeks | Sprint count | Pts | Deliverable |
|---|---|---|---|---|
| Phase 1 tail | Week 1 | 1 sprint | ~28 | E-003 debate panel + E-004 Hyperframe/multi-vendor + Hook-drift cleanup + E2E integration test + deploy pipeline = code-complete |
| Phase 1 prove | Week 2-6 | runtime, not sprint | 0 code | Run live, validate Phase 1 exit gate: Beauty + 5 video/day + GMV ≥ $200/14d |
| Phase 2 | Week 7-14 | 4 sprints (~100 pt) | ~100 | E-010 Ops Console (8 pt actual) + multi-platform expansion (FB Reels prod, YT Shorts prod) + multi-niche (electronics, fashion) + Writers' Room full 6-agent debate + harness-evolver scaffolding |
| Phase 3 | Week 15-24 | 5 sprints (~150 pt) | ~150 | Self-improving autonomous: harness-evolver promoting prompt/temp/model variants from Wiki data, MoM CTR uplift ≥ 5 %, human intervention < 5 % |

### Sprint 5 (next session) preview — code-complete Phase 1
Per Nick Fury's session-3 handoff recommendation:

| Item | Pts | Notes |
|---|---|---|
| E-003 Writers' Room debate panel | 5 | Director / Screenwriter / Cinematographer / Sound Designer / Critic panel — debate-then-Director-decides per `agent-hierarchy.md` |
| E-004 Hyperframe overlay + multi-vendor video | 5 | Sora + Flux fallback chain alongside kie.ai Veo |
| Hook-drift cleanup | 2 | Restore 5 missing tools (`aegis-approval-gate`, `aegis-brain-graph`, `aegis-live-tail`, `aegis-activity-logger`, `aegis-resume`) — bundled as chore |
| E2E integration test | ~5 | One pytest that spins the InProcessExecutor through Discovery DAG + Campaign DAG end-to-end with VCR cassettes |
| Deploy pipeline | ~5 | `scripts/deploy.sh` + GHA workflow + secrets rotation runbook |
| **Total** | ~22 | Fits comfortably in 27 pt velocity |

After Sprint 5: Phase 1 = code-complete. Then we wait on real-world data (the quick-win track feeds this).

---

## The actual recommendation

**Run both tracks in parallel. They are NOT competing.**

Quick-win track:
- Unblocks revenue NOW (2-3 weeks)
- Validates SPEC assumptions with real data (not synthetic)
- Generates first real Wiki entries → real Curator patterns → smarter next-run
- Reveals which Phase 2/3 features are actually load-bearing vs. nice-to-have
- Critical insight: **you cannot tune a self-improving loop without real failure data**

Full platform track:
- Sprint 5 lands the Phase 1 code-complete cap (next session, 1 sprint)
- Phase 2 sprints can start in parallel with quick-win going live
- The quick-win's daily metrics feed Phase 2 prioritization decisions
- Phase 3 (harness-evolver) is unstartable without real data anyway

### Critical-path decision tree

```
                    ┌─────────────────────────────┐
                    │ Sprint 5 in next session    │
                    │ (Phase 1 code-complete)     │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │ Are vendor keys procured?   │
                    └──────┬───────────────┬──────┘
                          YES             NO
                           │               │
                           ▼               ▼
                ┌──────────────────┐  ┌──────────────────────┐
                │ Run quick-win    │  │ Block on QW-1..QW-5  │
                │ live ops weeks   │  │ Start Phase 2 anyway │
                │ 2-3+. Capture    │  │ Ops Console first    │
                │ real data.       │  │ (offline-codable)    │
                └────────┬─────────┘  └──────────┬───────────┘
                         │                       │
                         └───────────┬───────────┘
                                     ▼
                    ┌─────────────────────────────┐
                    │ Phase 2 sprints chained on  │
                    │ real data signals — Curator │
                    │ + harness-evolver Phase 3   │
                    └─────────────────────────────┘
```

### Three numbers to remember

| Number | Meaning |
|---|---|
| **5 pt** | Code burden remaining for quick-win (everything else is vendor + ops) |
| **22 pt** | Sprint 5 to code-complete Phase 1 fully |
| **2-3 weeks** | Elapsed time to first real GMV if vendor onboarding starts THIS week |

---

## What goes to human-queue from this doc

For the board to action (NOT Nick Fury — these are external/credentials):

- [ ] **[EXTERNAL]** Apply to Shopee Affiliate Program TH (QW-1) — start clock, can take a week
- [ ] **[EXTERNAL]** Create Meta Business + IG Creator account + get long-lived Graph token (QW-2)
- [ ] **[EXTERNAL]** Sign up kie.ai + buy initial credits (QW-3)
- [ ] **[EXTERNAL]** Sign up ElevenLabs starter (QW-4)
- [ ] **[EXTERNAL]** Manual seed: pick 5-10 candidate Beauty SKUs from Shopee TH (QW-6)
- [ ] **[IDENTITY]** Confirm whether quick-win runs on board's personal laptop (cron) or a hosted box — affects QW-9 deploy choice

Everything else is Nick Fury's domain — code, sprint plans, retros, instinct promotion, ADRs.
