# ADR-007 — Studio-grade approval workflow (Shopee URL → finished clip with human gates)

- **Status**: Proposed (awaiting board approval before Sprint 7)
- **Date**: 2026-05-13
- **Proposed by**: claude-orchestrator on board directive ("ขอละเอียด แบบ professional studio")
- **Replaces**: the current single-shot `run_once.py` autopilot flow

## Context — why the current pipeline is not studio-grade

Today the loop is fire-and-forget:

```
Shopee URL → Strategist → Writers' Room → Storyboard → Phaya pipeline
                        → Editor → Safety Gate → Publish → Analytics
```

One CLI call, ~3 min elapsed, one `out/*.mp4`. Functional, but:

| Problem (today) | Studio reality |
|---|---|
| One shot at angle / hook | Strategy presents 3 options; client picks |
| Storyboard is whatever Writers' Room emits | Cinematographer pitches the shot list; client signs off scene by scene |
| Image gen runs immediately on scene prompts | Art Director presents key-art references first |
| TTS uses whatever voice was passed | Sound Designer presents 2-3 voice castings; client picks |
| Final cut is whatever ffmpeg muxes | Director sits with the editor for the final pass |
| Compliance happens post-render | Legal / claim audit runs at multiple checkpoints |
| No paper trail of what was approved | Every decision is a signed deliverable |

For an ad agency the gates are **the product**: clients pay for the right to see + revise each milestone, not just the final mp4. Skipping the gates means we ship the first thing that compiled, which is fine for synthetic demos but a quality+brand+legal risk in live ops.

## Decision

Replace `run_once.py` with a **gated production flow** (`auto_affi.ops.produce`) that mirrors a real commercial production studio. **10 distinct stages**, each with:

- A named owner (existing agent persona maps cleanly)
- An input schema + output schema (Pydantic-validated)
- A human approval gate (default ON; can be `--auto`-skipped per-stage)
- Revision support (every reject loops the stage with diff vs prior)
- Decision persistence (feeds Wiki + Ops Console + audit log)
- Cost / latency budget shown BEFORE the stage executes

The board reviews the deliverable, picks `APPROVE` / `REVISE <notes>` / `REJECT`, and the flow advances or loops. State persists across CLI invocations so the board can review on their own schedule (mobile, browser, anywhere).

## The 10 stages

```
       ┌────────────────────────────────────────────────────────────┐
       │ ProductionRun  status=DRAFT … APPROVED  · trace_id  · cost │
       └────────────────────────────────────────────────────────────┘
                                  │
   ─── Pre-production (creative) ───────────────────────────────────
   1.  📋 Brief & Concept           Strategist          ฿0.001  · 30s
       Output: 3 angle options + persona + KPIs
       Gate:   board picks 1 angle
                                  │
   2.  ✍️ Script                    Screenwriter        ฿0.005  · 60s
       Output: 5-scene script (hook / agitate / demo / proof / cta)
               + 2 alternates for hook line
       Gate:   board picks hook variant + approves full script
                                  │
   3.  🎬 Storyboard                Cinematographer +   ฿0.005  · 60s
                                    Storyboard Artist
       Output: per-scene shot list (camera / lighting / lens /
               motion / on-screen text / SFX cues)
       Gate:   per-scene approve OR scene-level revise
                                  │
   ─── Production (assets) ─────────────────────────────────────────
   4.  🖼️ Visual References         Art Director        ฿0.05/scn · 60s/scn
       Output: Nano Banana 2 still per scene, 9:16 1K
       Gate:   per-scene approve / regenerate
                                  │
   5.  🎞️ Animatics (motion)        Editor              ฿2.50/scn · 90s/scn
       Output: image-to-video clip per scene (silent)
       Gate:   per-scene approve / regenerate / freeze-to-still
                                  │
   6.  🗣️ Voice-over                Sound Designer      ฿0.001/scn · 15s/scn
       Output: Thai TTS per scene with 2 voice options (Algenib +
               Zephyr) + slow/normal pacing
       Gate:   board picks voice once for the run + approves all VO
                                  │
   7.  🎵 Music & SFX               Sound Designer      ฿0.05    · 30s
       Output: text-to-music bed matching mood + SFX cue list
       Gate:   board approves audio bed
                                  │
   ─── Post-production ─────────────────────────────────────────────
   8.  ✂️ Final Cut                 Editor + Director   ฿0.00    · 30s
       Output: muxed mp4 with all 6 editor passes
               (silence trim, filler cut, auto-subtitle, hook
                punch-in, brand overlay, cta endcard)
       Gate:   board approves final cut
                                  │
   9.  🛡️ Compliance                Safety + Legal      ฿0.001   · 10s
       Output: claim audit + brand-blocklist + NSFW + music license
               + Phase 1 non-goals check
       Gate:   automated PASS or human override if borderline
                                  │
  10.  📤 Publish                   Publisher + Board    ฿0.00   · 10s
       Output: IG Reels post (FB/YT in Phase 2) + subId tracking
       Gate:   board final go/no-go (only "live" stage)
                                  │
       ┌────────────────────────────────────────────────────────────┐
       │ Analytics + Curator start polling — feeds Wiki for         │
       │ next-run Strategist priors                                 │
       └────────────────────────────────────────────────────────────┘

Total studio cost per produced clip: ~฿15  (~$0.42)
Total studio elapsed (with human at every gate, generous SLAs):
    1 business day for first-pass; 2-3 hours for experienced approver
```

Mapping to existing AEGIS agent personas — none of these stages need new agents, only new state + UI:

| Stage | Owner persona (existing) |
|---|---|
| 1 Brief & Concept | Strategist (`agents/strategist.py`) |
| 2 Script | Writers' Room → Screenwriter role (`agents/writers_room.py`) |
| 3 Storyboard | Writers' Room → Cinematographer + Storyboard Artist roles |
| 4 Visual References | Art Director (new lightweight role inside Writers' Room) |
| 5 Animatics | Editor (new — but pipeline calls already exist via `adapters/phaya.py`) |
| 6 Voice-over | Sound Designer + `adapters/tts.py` |
| 7 Music & SFX | Sound Designer + Phaya text-to-music |
| 8 Final Cut | Editor + Director (existing editor_passes.py) |
| 9 Compliance | Safety Gate + Claim Auditor + Music License (all exist) |
| 10 Publish | Publisher (existing dry-run + IG/FB/YT prod paths) |

## State machine per stage

```
              ┌─────────┐
              │  DRAFT  │  ← stage agent starts work
              └────┬────┘
                   │ produced
                   ▼
              ┌─────────────┐
              │ IN_REVIEW   │  ← board sees the deliverable
              └─┬─────┬───┬─┘
       approve │ revise│   │ reject
               ▼     ▼   ▼
       ┌─────────┐ ┌─────────────────┐ ┌──────────┐
       │APPROVED │ │ REVISION_PENDING│ │ REJECTED │
       └─────────┘ └────────┬────────┘ └──────────┘
        next stage  loops back to DRAFT     run halts
                    (with revision notes
                     appended to brief)
```

- **DRAFT** — agent is producing the deliverable
- **IN_REVIEW** — deliverable is ready; awaiting board's call (visible in Ops Console + queued at `.aegis/brain/human-queue.md`)
- **APPROVED** — locked in; next stage starts
- **REVISION_PENDING** — board asked for changes; agent re-runs with the revision notes injected into context. Previous artifacts preserved for diff
- **REJECTED** — entire run halts; logged for the Wiki anti-pattern set

A run is COMPLETED only when stage 10 is APPROVED. Until then it's resumable from disk.

## Data model — minimal additions

```python
# src/auto_affi/schemas/production.py

class ProductionRunStatus(StrEnum):
    DRAFT       = "draft"
    IN_PROGRESS = "in_progress"
    APPROVED    = "approved"     # all 10 stages green
    REJECTED    = "rejected"     # any stage REJECT
    EXPIRED     = "expired"      # any stage past SLA (default 24 h)

class ProductionStageStatus(StrEnum):
    DRAFT             = "draft"
    IN_REVIEW         = "in_review"
    APPROVED          = "approved"
    REVISION_PENDING  = "revision_pending"
    REJECTED          = "rejected"

class Decision(BaseModel):
    decided_at: datetime
    verdict: Literal["approve", "revise", "reject"]
    decided_by: str                 # email of board reviewer
    notes_th: str | None = None     # revision notes / reject reason

class Revision(BaseModel):
    revision_idx: int               # 0 = first draft, 1 = first revise, …
    produced_at: datetime
    cost_thb: float
    artifact_gs_uris: list[str]     # all GCS objects produced this revision
    decision: Decision | None       # None while still IN_REVIEW

class ProductionStage(BaseModel):
    stage_id: int                   # 1-10
    name: str                       # "brief_and_concept", "script", …
    status: ProductionStageStatus
    revisions: list[Revision]       # ordered; last is the current
    sla_deadline: datetime

class ProductionRun(BaseModel):
    run_id: str                     # uuid4
    shopee_url: str
    shopee_item_id: int
    shopee_shop_id: int
    started_at: datetime
    status: ProductionRunStatus
    stages: list[ProductionStage]   # 10 entries, ordered
    total_cost_thb: float
    final_mp4_gs_uri: str | None = None
    published_post_id: str | None = None
```

Persistence: one JSON-per-run at `.aegis/brain/production/<run_id>.json`, indexed in `MEMORY.md`. (Postgres later when Phase 2 needs concurrent runs.)

## CLI surface

```bash
# Kick off a new run — first stage executes, awaits board approval
python -m auto_affi.ops.produce start \
    --shopee-url "https://shopee.co.th/...i.<shop>.<item>"
→ Creates ProductionRun, runs stage 1 (Brief & Concept), prints summary,
  queues IN_REVIEW notification in human-queue.md, exits 0.

# Show what's awaiting board review
python -m auto_affi.ops.produce status
→ Lists all runs with IN_REVIEW stages, deliverables, SLA timers.

# Approve a stage and advance
python -m auto_affi.ops.produce approve <run_id> --stage <n>
→ Marks stage APPROVED, kicks off stage n+1, exits.

# Request revision (loops the stage with notes)
python -m auto_affi.ops.produce revise <run_id> --stage <n> \
    --notes "ขอ hook ที่ดราม่ากว่านี้ ใช้คำว่า 'เสียดาย' แทน 'หลุด'"
→ Stage status → REVISION_PENDING, agent re-runs with notes, exits.

# Reject and halt run
python -m auto_affi.ops.produce reject <run_id> --stage <n> \
    --reason "ตลาดไม่เหมาะ"
→ Run status → REJECTED, logged to Wiki anti-patterns.

# Power flag: skip board gate for a specific stage
python -m auto_affi.ops.produce start --shopee-url ... \
    --auto-approve script,storyboard
→ Stages 2 + 3 auto-approve on draft; all others still gated.

# Resume the latest IN_REVIEW run interactively
python -m auto_affi.ops.produce next
→ Prints next gate, opens Ops Console URL, waits for input.
```

## Ops Console additions (E-010 polish)

New routes on top of the existing FastAPI app:

| Method | Path | Returns |
|---|---|---|
| GET | `/api/production/runs` | All runs, filtered by status |
| GET | `/api/production/runs/{run_id}` | Full ProductionRun |
| GET | `/api/production/runs/{run_id}/stages/{n}` | Stage detail incl. all revisions + decision |
| GET | `/api/production/runs/{run_id}/stages/{n}/preview` | Renders the deliverable inline (script text / storyboard JSON / image grid / mp4 player) |
| POST | `/api/production/runs/{run_id}/stages/{n}/decide` | `{verdict, notes_th}` — apply decision, advance/loop |
| GET | `/inbox` | HTMX dashboard — list of IN_REVIEW stages awaiting board |

Inbox UI sketch (Jinja2 + HTMX, no React build step):

```
┌─ AEGIS Studio / Inbox ──────────────────────────────────────────┐
│  📋 3 stages awaiting your review                                │
│                                                                  │
│  Run  Stage             Product              SLA           Actions │
│  ──── ───────────────── ───────────────────  ─────────────  ─────  │
│  r-01 Script            Socket bit set       3h left        👁 review │
│  r-02 Storyboard scene2 Vitamin C serum      18h left       👁 review │
│  r-03 Voice-over        Hair growth oil      OVERDUE 2h     👁 review │
│                                                                  │
│  Recent decisions (last 5):                                      │
│  ✅ r-01 Brief approved by mr.phariyawit@aeternix.tech 14:32     │
│  ↻  r-02 Hook revised — "ขอดราม่าน้อยกว่านี้" 13:50              │
└──────────────────────────────────────────────────────────────────┘
```

Each "review" link opens a single-page stage view: the deliverable + an Approve / Revise / Reject row. Mobile-responsive (~500 LOC of Jinja2 + HTMX, no JS framework).

## Implementation plan — 3 sprints

| Sprint | Stages covered | Pts | New code | UI |
|---|---|---|---|---|
| **Sprint 7** | 1 Brief · 2 Script · 3 Storyboard | ~16 pt | `agents/production_director.py` + `schemas/production.py` + CLI + 3 routes | Stage-review pages for the 3 creative stages |
| **Sprint 8** | 4 Visual Refs · 5 Animatics · 6 VO · 7 Music | ~14 pt | Asset-stage glue + image grid view + mp4 player + voice cast picker | Inbox dashboard |
| **Sprint 9** | 8 Final Cut · 9 Compliance · 10 Publish + first end-to-end live run | ~10 pt | Final-cut review + compliance dashboard + publish gate | Compliance audit panel |

Total ≈ **40 pt** over 3 sprints at our 27-pt cadence → ~6 weeks calendar with the board doing real reviews on each gate.

## Walk-through with the Hardware product (concrete example)

Item: `8-14มม. SOCKET HEAD bolt set` (Shopee i.992256187.44154734826)

```
Day 1, 10:00  python -m auto_affi.ops.produce start --shopee-url …
              → Stage 1 runs (Phaya GPT, 30s, ฿0.001)
              → Strategist emits 3 angle options:
                  A. "ครบในชุดเดียว ใช้กับสว่านได้เลย" (completeness)
                  B. "ประแจหลุดอีกแล้ว เสียเวลา…" (frustration)
                  C. "ช่างจริงเลือกใช้" (social proof)
              → IN_REVIEW, queued in human-queue.md
              → Slack/email notification to board (Sprint 8)

Day 1, 14:30  Board reviews inbox, picks angle B (frustration)
              → POST /api/production/runs/r-1/stages/1/decide
                {verdict: "approve", chosen_option: "B"}
              → Stage 2 (Script) auto-fires
              → Writers' Room generates the 5-scene script + 2 hook variants
              → IN_REVIEW

Day 1, 16:00  Board reviews script
              → Hook variant 1: "ประแจหลุดอีกแล้ว เสียเวลา..." ✅
              → Variant 2 nope
              → Approve
              → Stage 3 (Storyboard) fires
              → IN_REVIEW

Day 2, 09:00  Board reviews storyboard
              → Scene 2 visual prompt is too generic, revise:
                "ขอเห็น 150mm extension bar ชัดในเฟรม"
              → Stage 3 re-runs with notes; new draft in 60s
              → Board approves second draft
              → Stage 4 fires (5 Nano Banana stills, ~5 min)
              → IN_REVIEW

Day 2, 11:00  Board reviews image grid — approves all 5 stills
              → Stage 5 fires (5 i2v clips, ~10 min, ฿13)
              → IN_REVIEW

Day 2, 13:00  Board reviews animatics
              → Scene 0 motion is weak, regenerate
              → New scene 0 in 90s
              → Approve all 5
              → Stage 6 (VO) fires with both voice options
              → IN_REVIEW

Day 2, 15:00  Board picks Algenib voice
              → Stage 7 (Music) fires
              → IN_REVIEW

Day 2, 16:00  Board approves music bed
              → Stage 8 (Final Cut) fires — 30s
              → IN_REVIEW with full mp4 preview

Day 2, 17:00  Board approves final cut
              → Stage 9 (Compliance) runs automated checks → PASS
              → Stage 10 (Publish) waits for go/no-go
              → IN_REVIEW with publish preview

Day 3, 10:00  Board approves publish
              → Posted to IG Reels (Sprint 9 live path)
              → Analytics + Curator start polling
              → ProductionRun status → APPROVED, run closed
              → Total cost: ฿15.23 · Total elapsed: 48 h (~6 h active board time)
```

Compare to today's flow: same mp4 produced in 3 minutes, but with zero board control and zero paper trail.

## Why this is worth the 40-pt investment

| Without gates (today) | With gates (this ADR) |
|---|---|
| Bad creative ships | Bad creative gets revised before render |
| ~฿13/video wasted on rejected outputs | Stage-level revise costs only the stage |
| No learning signal beyond raw CTR | Every approval/reject feeds the Wiki — Strategist gets smarter per run |
| One model of board's taste (none) | Board's taste becomes part of resonance |
| Compliance is a "did we get sued?" lottery | Compliance runs at every gate; one bad scene gets caught before mux |
| Brand risk on unsupervised live ops | Board signs off on the actual final cut |
| Can't run multiple SKUs in parallel | Each run has independent state; board reviews on schedule |

## Auto-approval ramps (future, after data exists)

Once the Wiki has ≥ 50 production runs:

- **Wiki-driven auto-approve**: when a stage's draft matches a Canonical-tier pattern with ≥ 90 % approval rate, auto-approve. Board sees a summary, not a gate. Reduces active board time from ~6 h/run to ~30 min/run by Phase 3.
- **Confidence thresholding**: only stages 1-3 (creative direction) need board attention by Phase 3; production stages 4-7 auto-pass when Wiki confirms pattern fit. Compliance + publish never auto.

## Non-goals (explicit)

- ❌ Replacing the board entirely (per `non-goals.md` resonance — Auto-Affi is supervisor-supervised, not autonomous-everything)
- ❌ Multi-tenant / multi-client workflows (Phase 2)
- ❌ Native mobile app (Phase 3 — Ops Console mobile-responsive is enough)
- ❌ Real-time collaborative review (only one board for Phase 1)
- ❌ Slack / Line / email integrations (Sprint 9+; queue surfaces in Ops Console first)

## Risks & mitigations

| Risk | Mitigation |
|---|---|
| Board becomes the bottleneck → throughput drops | `--auto-approve` flag per-stage; Wiki auto-approve ramp; SLA expiry auto-rejects stale runs |
| Revision loops thrash credits (esp. Stage 5 i2v at ฿2.50/scene) | Hard cap: max 3 revisions per stage. Stage 5 also offers freeze-to-still fallback (฿0.05 instead of ฿2.50) |
| State machine bugs strand runs | Idempotent stage execution + manual `resume <run_id>` recovery |
| Board approves something non-compliant | Stage 9 is automated and cannot be skipped via `--auto-approve`; legal-grade backstop |
| Revisions break asset lineage | Every Revision records `parent_revision_idx` + GCS keeps all artifacts for 90 days |

## Open questions for the board

These three need a board call before Sprint 7 plan locks. **None of them are blockers — defaults are listed.** If silence by Sprint 7 plan time, defaults apply.

1. **Default SLA per stage** — 24 h, or shorter (12 h to keep velocity up, 48 h to let board breathe). Default: **24 h**.
2. **Approver count** — single approver (board only) or multi (board + assistant)? Default: **single, board only, Phase 1**.
3. **Notification channel** — email-only / human-queue-only / both? Default: **human-queue.md + future Slack hook**.

## Related

- [[north-stars]] — KPI table; this workflow targets the "human intervention rate ≤ 30 % Phase 1" goal explicitly
- [[autonomy-stance]] — "human as supervisor only" stance; this is HOW that supervision is structured operationally
- [[agent-hierarchy]] — Director-decides pattern within Writers' Room; gates are the inter-agent handoff equivalent at studio level
- [[cost-model]] — every stage line-itemed against the budget
- ADR-001 (Agent hierarchy vs peer mesh) — stages enforce the strict hierarchy in practice
- ADR-003 (Bilateral wiki sync) — board decisions ARE the bilateral signal that promotes Wiki entries to Canonical
- ADR-006 (GCS staging) — all stage artifacts live as `gs://` URIs, signed for board review

---

**Status**: Proposed. Awaiting board approval to lock Sprint 7 backlog around this ADR. Default Sprint 7 scope (16 pt) covers Stages 1-3 + CLI + 3 Ops Console routes.
