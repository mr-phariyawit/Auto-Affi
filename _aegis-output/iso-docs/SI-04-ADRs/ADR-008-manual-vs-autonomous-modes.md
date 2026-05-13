# ADR-008 — Dual operational modes: MANUAL vs FULLY AUTONOMOUS

- **Status**: Proposed (awaiting board approval before Sprint 10)
- **Date**: 2026-05-13
- **Proposed by**: claude-orchestrator on board directive: *"สร้างแผน implement update mode quickwin ให้เป็นชื่อว่า manual ซึ่ง workflow ต้องใช้ human approve เท่านั้น และ อีก mode คือ fully autonomous (full tech stacked)"*
- **Renames**: the "quick-win path" naming from `sprints/roadmap-quick-win-vs-full.md` → **MANUAL** mode
- **Extends**: ADR-007 (studio workflow) — gates remain identical; mode controls whether the board or the system pulls the trigger at each gate

## Context

ADR-007 shipped the studio workflow with every gate gated on board approval. That is the right default for the first ~50-100 videos: the board's taste becomes Wiki Canonical patterns, content liability stays low, and we don't ship visual garbage at scale.

But the Phase 3 north-star (`north-stars.md`) is 100+ videos/day with ≤ 5 % human intervention. At that cadence the board cannot personally pick every angle, voice, or freeze-vs-i2v. The system must decide on its own — using the resonance, Wiki patterns, kill switches, and cost-model already in place.

We need TWO named modes — clearly toggled, clearly safe, clearly visible — that share the same 10-stage workflow but differ in **who pulls the trigger**.

## Decision

Two operational modes. Each `ProductionRun` is created in exactly one of them. Mode is set at `produce start` time and immutable for the lifetime of the run.

```
┌───────────────────────────────────────────────────────────────────┐
│  MODE = MANUAL                                                    │
│  ─────────────                                                    │
│  Every gate awaits board approve/revise/reject via CLI or         │
│  Ops Console. Wiki is read for context (priors shown to the       │
│  board) but never auto-decides. SLA: 24 h per stage.              │
│                                                                   │
│  Default mode for all new runs. Use for:                          │
│   • First N=50 videos per niche (Wiki calibration)                │
│   • Brand-sensitive launches                                      │
│   • Regulated content (medical claims, financial)                 │
│   • Any time a Loki review queues an instinct-revision            │
└───────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────┐
│  MODE = AUTONOMOUS  (full tech stacked)                           │
│  ──────────────────                                               │
│  Every gate auto-decides via AutonomousDecider, which queries     │
│  Wiki for the matching pattern + confidence score + kill-switch   │
│  state. Approves if confidence ≥ threshold; escalates to the      │
│  board queue otherwise. Compliance + Publish retain hard checks   │
│  (UNSKIPPABLE per ADR-007 Sprint 8 Loki) but their AUTO path is   │
│  fully wired. SLA: minutes per stage.                             │
│                                                                   │
│  Available only when the board has explicitly opted in (global    │
│  flag + per-niche flag + per-day cost cap). Use for:              │
│   • Scaled production after Wiki has ≥ 50 Canonical patterns      │
│   • Phase 2/3 KPI runs (100+ videos/day)                          │
│   • A/B variant production at the same campaign                   │
└───────────────────────────────────────────────────────────────────┘
```

The mode toggle is the **entire feature**. No other code change between manual and autonomous — both run the same 10-stage state machine, with the same UNSKIPPABLE list, with the same persistence + audit log. Only the *decider* changes.

## Mode toggle — where the bit lives

| Layer | Mode location | Default |
|---|---|---|
| **Per-run** (CLI / API) | `--mode manual\|autonomous` flag on `produce start` | `manual` |
| **Per-niche** (resonance) | `niche_config[<niche>].autonomous_allowed: bool` | `false` |
| **Global** (env) | `AUTO_AFFI__AUTONOMOUS_ENABLED=true\|false` | `false` |
| **Per-day** (state) | `daily_autonomous_budget_thb` ledger in `.aegis/brain/state/` | `100` |

Autonomous mode requires **all four** to allow. Missing any → run falls back to manual + queues a board notification. This is the kill-switch's spiritual sibling at the mode level.

## AutonomousDecider — the new agent

The single addition to the codebase. Lives at `src/auto_affi/agents/autonomous_decider.py`. Per-stage, it:

1. **Reads the deliverable** the stage agent produced (same JSON as a human would see in `/inbox`)
2. **Queries Wiki** via `wiki/retriever.py` for the closest Canonical-tier patterns matching the brief's niche + persona + hook style + (for assets) visual prompt class
3. **Computes a confidence score** (0.0-1.0) from:
   - Wiki match strength (cosine similarity of embeddings via Phaya embeddings, 4096-dim)
   - Historical board approval rate for matched patterns
   - Safety-gate result (claim_auditor, brand blocklist, NSFW)
   - Cost-model fit (does the deliverable's projected cost fit the run budget?)
   - Niche/non-goals alignment
4. **Decides**:
   - `confidence ≥ 0.85` → APPROVE (logged to activity.log + Wiki review-queue as "auto-approve")
   - `0.60 ≤ confidence < 0.85` → APPROVE WITH WATCH (auto-approves but flags for board post-hoc review within 24 h)
   - `0.40 ≤ confidence < 0.60` → ESCALATE (creates a human-queue item; stage becomes IN_REVIEW; SLA 4 h)
   - `confidence < 0.40` → REJECT (run halts as anti-pattern; logged to Wiki)

The 4 thresholds are tunable per niche + per stage. Defaults in `resonance/autonomous-thresholds.md` (new file). Loki review of the thresholds is mandatory before Sprint 11 ships.

Confidence math (sketch):

```
score = 0.40 * wiki_similarity                # 0-1 cosine sim
      + 0.25 * historical_approval_rate       # board approval rate of matched patterns
      + 0.15 * safety_gate_signal             # 1.0 PASS · 0.3 SOFT-FAIL · 0.0 HARD-FAIL
      + 0.10 * cost_fit_signal                # 1.0 within budget · 0.5 50-100% · 0.0 over
      + 0.10 * niche_alignment_signal         # match against niche_config + non-goals

Hard floors (drop score to 0 regardless):
  - Any kill switch active for this niche / global → 0.0
  - claim_auditor severity == "HIGH"             → 0.0
  - daily_autonomous_budget exhausted             → 0.0
  - Match is Hypothesis-tier only (no Canonical match) → 0.0
```

## Stage-by-stage autonomous behavior

The bit changes per stage. Below = what AutonomousDecider does when the stage lands `IN_REVIEW`:

| Stage | AUTONOMOUS behavior |
|---|---|
| **1 Brief & Concept** | Wiki RAG returns top-3 angles for niche+persona. AutonomousDecider picks the highest-historical-CTR angle. If no Canonical match exists for this niche × persona pair → ESCALATE. |
| **2 Script** | Auto-pick first hook variant. If `claim_auditor` flags HIGH severity on either variant → REJECT. Otherwise APPROVE. |
| **3 Storyboard** | Per-scene: check `visual_prompt` against Canonical exemplars in the niche's Wiki tier. If any scene scores below threshold → ESCALATE on that scene only. |
| **4 Visual References** | Per-scene: auto-approve if Nano Banana 2 returns no error AND the image embedding (via Phaya embed) has cosine-sim ≥ 0.65 with the scene's `visual_prompt` Canonical exemplar. Otherwise REVISE up to 3× before ESCALATING. |
| **5 Animatics** | Cost-protected: if scene's projected i2v cost would push run over the per-run cap → use freeze-to-still automatically. Otherwise auto-approve once the i2v completes successfully. ESCALATE if Phaya rejects 2× in a row. |
| **6 Voice-over** | Auto-pick voice from `resonance/voice-preference.md` per niche (e.g. Algenib for Beauty, Zephyr for Hardware). |
| **7 Music & SFX** | Auto-pick mood from `niche_config[<niche>].music_default`. |
| **8 Final Cut** | Pure ffmpeg, no decision needed — runs the 6 editor passes deterministically. APPROVE auto unless ffmpeg fails. |
| **9 Compliance** | **NEVER auto-skipped** (ADR-007 mandate). The automated checks (claim+brand+NSFW+music-license) just run; PASS → advance, HARD-FAIL → REJECT run, SOFT-FAIL → ESCALATE to human queue for override decision. |
| **10 Publish** | **REQUIRES three explicit YES conditions** before auto-firing: (a) global `AUTO_AFFI__AUTONOMOUS_ENABLED=true`, (b) `niche_config[<niche>].autonomous_publish=true`, (c) `daily_autonomous_publishes < daily_cap`. Otherwise ESCALATE — human pulls the publish trigger. |

## Safety mechanisms

Layered, defense-in-depth (each layer can halt autonomous mode independently):

| Layer | Trigger | Action |
|---|---|---|
| Per-stage confidence floor | confidence < 0.40 | REJECT, log anti-pattern |
| Per-run cost cap | run cost > ฿20 | halt + ESCALATE remaining stages |
| Daily budget cap | autonomous spend > daily_autonomous_budget_thb | mode degrades to MANUAL for the rest of the day |
| Kill switch (existing) | any of 4 levels (CONTENT/CAMPAIGN/NICHE/GLOBAL) active | halt all autonomous runs in scope |
| Compliance hard-fail | claim_auditor HIGH or banned brand | REJECT |
| Anomaly detector | 3 consecutive low-confidence stages in a single run | halt run + ESCALATE entire run for board post-mortem |
| Wiki regression watch | autonomous-approved videos with sub-1% CTR over 7 days | auto-degrade niche to MANUAL until board re-enables |

All layers feed `activity.log` with structured entries. Loki adversarial pass on the safety matrix is **mandatory** before any autonomous run touches a live publish.

## Migration path — MANUAL today → AUTONOMOUS tomorrow

This is the gradient, not a switch. Niches earn autonomous mode by accumulating Wiki signal.

```
Week 0-2     All runs MANUAL. Board reviews every gate. Wiki accumulates first
             Canonical patterns. Autonomous globally disabled.

Week 3-4     `AUTO_AFFI__AUTONOMOUS_ENABLED=true` (global). Per-niche still off.
             AutonomousDecider runs in SHADOW MODE — computes what it WOULD have
             decided alongside the human's call. Board sees the deltas in
             /inbox/shadow_decisions/. Builds trust + tunes thresholds.

Week 5-6     First niche (Beauty, the most-data-rich) flips to per-niche autonomous
             for stages 1-7. Stage 8 (Final Cut) auto. Stage 9 hard-checked.
             Stage 10 STILL manual approval. Board only intervenes on
             ESCALATE-tier confidence scores.

Week 7-10    Stage 10 autonomous-publish enabled per niche, gated by 7-day rolling
             CTR floor (≥ 1.5% for Beauty). Board sees only ESCALATEs + a daily
             summary. Phase 1 KPI "human intervention ≤ 30%" testable here.

Week 11+     Additional niches (Electronics, Fashion) graduate from MANUAL as
             their Wiki Canonical counts cross threshold. Phase 3 KPI "human
             intervention ≤ 5%" testable here.
```

The board can pull the brake at any point: flip the global flag off, autonomous halts gracefully (running stages complete, new ones revert to MANUAL).

## Data model changes

Minimal — one StrEnum + 2 fields on `ProductionRun`:

```python
# src/auto_affi/schemas/production.py

class ProductionMode(StrEnum):
    MANUAL = "manual"           # ADR-007 default — board approves every gate
    AUTONOMOUS = "autonomous"   # ADR-008 — AutonomousDecider approves


class ProductionRun(BaseModel):
    # ... existing fields ...
    mode: ProductionMode = ProductionMode.MANUAL
    autonomous_confidence_log: list[ConfidenceEntry] = []  # per-stage decision trace


class ConfidenceEntry(BaseModel):
    stage_id: int
    revision_idx: int
    confidence: float                    # 0.0 - 1.0
    decision: Literal["auto_approve", "watch_approve", "escalate", "reject"]
    wiki_match_id: str | None            # which Canonical pattern matched
    safety_signal: float
    cost_fit_signal: float
    decided_at: datetime
```

`Decision.decided_by` already exists — autonomous decisions use `"autonomous_decider"` instead of a board email.

## CLI surface

```bash
# Manual run (default; same as today):
.venv/bin/python -m auto_affi.ops.produce start --shopee-url URL

# Explicitly manual (for clarity in scripts):
.venv/bin/python -m auto_affi.ops.produce start --shopee-url URL --mode manual

# Autonomous run (requires all 4 toggle layers to allow):
.venv/bin/python -m auto_affi.ops.produce start --shopee-url URL --mode autonomous
# → If any toggle layer denies, prints why + falls back to manual + queues board notification

# Inspect autonomous decisions for a run:
.venv/bin/python -m auto_affi.ops.produce trace <run_id> --confidence
# → Per-stage: stage_id, confidence, decision, wiki_match, reason

# Force a niche back to manual (board override):
.venv/bin/python -m auto_affi.ops.produce mode set --niche Beauty --mode manual
```

Ops Console additions:
- `/inbox/shadow_decisions/` — shadow-mode deltas during Week 3-4
- `/autonomous/status` — global flag, per-niche flags, daily budget remaining, recent ESCALATEs
- `/autonomous/decisions/{run_id}` — per-stage confidence trace for any autonomous run

## Implementation phases — 2 sprints

| Sprint | Focus | Pts |
|---|---|---|
| **Sprint 10** | Mode scaffolding, AutonomousDecider skeleton with shadow mode, ProductionRun.mode field, CLI `--mode` flag, ops-console autonomous status page, Loki review of decider logic | ~14 pt |
| **Sprint 11** | Wiki-driven decision logic (stages 1-7 auto paths), Canonical-tier requirement enforcement, per-run + per-day cost caps, ESCALATE → human-queue integration, anomaly detector, autonomous-publish path with the 3 explicit yes-conditions, first autonomous shadow run on the Hardware product | ~14 pt |

After Sprint 11 closes:
- Manual mode is the named default and unchanged from ADR-007.
- Autonomous mode is wired but `AUTO_AFFI__AUTONOMOUS_ENABLED=false` by default — opt-in only.
- Shadow-mode lets the board see what AutonomousDecider would have done before trusting it for real decisions.

## Open questions for the board

Defaults below — if no answer by Sprint 10 plan time, defaults apply:

1. **First niche to graduate** — Beauty (most data) or Hardware (most recent end-to-end test)? Default: **Beauty**.
2. **Confidence threshold tuning** — start at 0.85 / 0.60 / 0.40 (auto / watch / escalate / reject) or more conservative 0.90 / 0.70 / 0.50? Default: **conservative 0.90 / 0.70 / 0.50** for the first month, relax to 0.85 / 0.60 / 0.40 once 100+ autonomous runs land without incident.
3. **Daily autonomous budget** — ฿100/day, ฿250/day, ฿500/day? Default: **฿100/day** for first month (≈ 7 videos/day at our cost model), then expand as KPIs verify.

## Risks + mitigations

| Risk | Mitigation |
|---|---|
| Autonomous ships brand-damaging content | Compliance stage 9 NEVER skips; layered safety matrix above; kill switches across 4 levels; daily-budget mode-degrade |
| Wiki contains bad patterns from early-day mistakes | Canonical tier requires ≥ 5 board approvals; promotion is auditable; Curator anti-pattern feed REJECTs known-bad |
| Confidence threshold drifts (overconfident model) | Quarterly Loki audit of threshold-vs-real-CTR correlation; auto-degrade per-niche on 7-day CTR floor breach |
| Shadow-mode disagreement is ignored | `/inbox/shadow_decisions/` shows every divergence in red; weekly digest emails to board (Sprint 11+) |
| One niche's autonomous patterns leak into another | Wiki matching is niche-scoped via niche_config; cross-niche matches require explicit board approval to promote |
| Cost runaway from broken AutonomousDecider | Per-run hard cap (฿20); daily hard cap (฿100); circuit breaker on 3 consecutive cost-cap hits → niche degrades to MANUAL |
| Autonomous decides at 03:00 with no board awake | activity.log + ESCALATEs queue + morning digest; nothing posts live without 7-day CTR floor green |

## Non-goals

- ❌ Removing MANUAL mode (it's the default and always remains as the fallback)
- ❌ Removing the 10-stage gates (autonomous mode goes THROUGH them faster, not around them)
- ❌ Cross-account autonomous mode (Phase 2)
- ❌ Reinforcement-learning re-training (Phase 3 harness-evolver per `north-stars.md`)
- ❌ Real-time autonomous decisions (this is async batch; "fast" means seconds, not millis)

## Related

- ADR-007 (Studio approval workflow) — gates are unchanged; mode controls who pulls each trigger
- `[[autonomy-stance]]` — "human as supervisor only" — autonomous mode IS this stance materialized
- `[[north-stars]]` — Phase 3 KPI "human intervention ≤ 5%" is unreachable in pure MANUAL; this ADR is the path
- `[[learning-loop]]` — Wiki tier semantics drive AutonomousDecider's confidence
- `[[cost-model]]` — per-run + per-day budgets are the safety net
- `sprints/roadmap-quick-win-vs-full.md` — RENAMES "quick-win" to MANUAL; this ADR is implementation for the autonomous half

---

**Status**: Proposed. Defaults locked unless board overrides by Sprint 10 plan time. Sprint 10 + 11 (~28 pt total) implements the design; subsequent niche-graduation work is operational, not engineering.
