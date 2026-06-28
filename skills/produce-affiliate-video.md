---
name: produce-affiliate-video
description: "End-to-end Auto-Affi production workflow from a NEW product. Trigger when the human supplies a product (image + name/price/commission/category/link) and wants an affiliate video, or says 'new product', 'produce a video for this', 'start production', 'รับสินค้าใหม่', 'ทำวิดีโอ affiliate', 'เริ่มผลิต'. Drives intake → economics gate → brief → the 5 PGA-gated stages (cast/objects/storyboard/contact/video) → edit → compliance → publish. Every paid generation is gated: audit + human approval + verify-before-spend. Over-trigger rather than under-trigger whenever a product is handed over for a video."
profile: standard
triggers:
  en: ["new product", "produce affiliate video", "make a video for this product", "start production", "product intake", "affiliate video"]
  th: ["สินค้าใหม่", "รับสินค้าใหม่", "ทำวิดีโอ affiliate", "เริ่มผลิต", "ผลิตวิดีโอ", "ทำคลิปสินค้า"]
reads: ["docs/templates/pipeline-step-templates.md", "docs/team/auto-affi-crew.md", "docs/principles/2026-06-27-pre-generation-audit-and-approval-gate.md", "SPEC.md"]
writes: ["runs/<run-id>/"]
wires: ["scout_scoring", "prompt_audit", "produce", "compliance_gate"]
tests: []
supersedes: []
---

## Quick Reference

> **"No paid pixel before audit + approval + balance. Same approved input, same output."**

Full production from a new product to a compliant 9:16 master. Five PGA-gated stages, each:
**fill template → PGA audit → show review panel → human approves (or bypasses) → generate.**
The Audit Lead reviews every artifact before it advances. No generation without approval.

- **Run dir:** `runs/<YYYY-MM-DD>-<product-slug>/`
- **Gates (binding):** SPEC §10.5 g1–13 — PGA audit, reference-sheet lock, generation lock, verify-before-spend.
- **Templates:** `docs/templates/pipeline-step-templates.md` (must be human-approved first run).
- **Crew:** `docs/team/auto-affi-crew.md` (Research / Marketing / Creative / Production / Audit).
- **Code:** `scout_scoring` (economics gate) · `prompt_audit` (gate) · `ops/produce.GatedProducer` (spend) · `compliance_gate`.

## When to Use vs When Not to Use

| Use this skill when | Don't use when |
|---|---|
| Human hands over a product for an affiliate video | Just analysing/spec work → other skills |
| "Start production", new product data arrives | Editing an existing master only → editor flow |
| Re-running a product after a brief change | Pure research/strategy with no production intent |

## Process

### Step 0 — Intake (input contract)
Collect, in one message, then create the run dir:
**Required:** product image(s) · name (TH) · price ฿ · **commission %** · category (beauty/gadget/home/mom_baby/fashion/food) · affiliate link.
**Helpful:** shop rating ★ + sales · 2–4 selling points (TH) · persona · do/don't-say constraints.
🔒 Never paste API keys in chat — keys live in `.env` (gate 5). Record intake to `runs/<run>/PROD.md`.

### Step 1 — Scout economics gate (FREE, verify-before-spend)
Run `scout_scoring.score(ScoutInput(...))`. If `rejected` (restricted category / low rating /
`UNVIABLE_ECONOMICS` = breakeven_views over ceiling) → **STOP, report the reason**, suggest a niche
pivot. Only a viable product proceeds. (This is the #1 successful-operator rule: vet economics first.)

### Step 2 — Strategist brief
Produce a `CampaignBrief`: angle + hook ≤1.0s + **problem→demo→CTA (PAS/BAB/UGC)** + single CTA +
persona + disclosure plan. Conversion-first for sub-5000 THB; peer-authority Thai VO, not narrated poetry.

### Step 3 — Dispatch the crew (parallel where independent)
Research feeds verified signals → Marketing owns the brief → Creative builds the sheets/storyboard →
Production generates → **Audit Lead reviews EVERY artifact at EVERY gate**. Crew returns structured
findings; the main thread synthesises and presents to the human at each gate.

### Step 4 — The 5 PGA-gated stages (in order)
**REFERENCE-SHEET BATCH FIRST (gate 11):** generate ALL reference/character sheets — every
`cast_sheet` (character/hero, incl. a product as the "character" for product-demos) + `objects_sheet`
— SHOW them together and get them approved as a SET **before** the `storyboard` stage. Never start a
storyboard on an un-approved reference sheet. (Like the AetherFlow `*-charsheet.jpg` that precedes every
storyboard.) Only after the sheet set is approved do storyboard → contact → video proceed.

For each stage `cast_sheet → objects_sheet → storyboard → contact_sheet → video`:
1. **Fill the template** (`docs/templates/pipeline-step-templates.md`) with this product's values; inject
   `{IDENTITY}` verbatim, `{NEG}`, one face ref, `REF_IMAGES` (cast+objects sheets) + `{SEED}`, 9:16, Thai-no-lipsync.
2. **PGA audit** — `prompt_audit.audit(manifest)` → record to `runs/<run>/approvals.json` (+ event log).
   Any fail → **block, report the failing item, do NOT generate.** Hard-compliance (banned/restricted/
   economics) can never be cleared, not even by bypass.
3. **Show the review panel** (stage · prompt_hash · checklist ✓/✗) and **WAIT**.
4. **Human approves** (`go`/`approve`) → generate via `GatedProducer` (GeminiProvider enforces the gate +
   mandatory budget breaker; Gemini has no pre-call balance API). Or **`bypass <stage>`** (logged; live bypass needs a preceding audit).
   No input → never generate speculatively.
5. **Pre-video pre-flight (stage 5):** vision-compare each contact frame vs the cast sheet ("same
   person?") BEFORE the paid Veo call; the mandatory budget breaker is the hard spend cap.

### Step 4.5 — STORYBOARD review page (MANDATORY before any paid Veo)
NEVER jump from frames straight to Veo. Assemble a self-contained `runs/<run>/storyboard.html` shot
TABLE — columns: No · เวลา/timecode · First frame (the generated starting frame, embedded) · เนื้อหา·motion ·
Prompt → Veo · เสียง/VO (Thai) · กล้อง/camera · Transition — plus the full VO, total duration, and the next
Veo cost. Present it for explicit human approval; only after `approve storyboard` do paid Veo clips run.
(Format: a per-shot table like the AetherFlow storyboards.)

### Step 5 — Edit → Compliance → Master
Concat shots → editor (captions, hook punch-in, brand overlay, CTA endcard) → `run_compliance`:
cleanroom (1 video + 1 audio), 9:16, Thai VO 1.0–1.15×, disclosure `#โฆษณา/#affiliate`, caption/VO sync.
Block the render if any gate fails. Output `runs/<run>/master.mp4`.

### Step 6 — Publish (gated)
Publishing needs SPEC §20 external blockers cleared (Meta token G2, etc.) + a recorded human approval.
If blocked, stop here and surface the blocker to the human-queue — the master is produced, not published.

### Step 7 — Learning closeout
Record successes, failures, user-caught issues, any rule changed, and per-stage cost to
`runs/<run>/` + brain learnings. Tag every claim `[VERIFIED: cmd]` or `[PRODUCED: unverified]`.

## Output Format
```
runs/<YYYY-MM-DD>-<slug>/
├── PROD.md                       # intake (image refs + data)
├── scout.json                    # economics-gate result
├── brief.json                    # CampaignBrief
├── approvals.json                # per-stage PGA state (gate source of truth = audit_events.jsonl)
├── audit_events.jsonl            # append-only approve/bypass/audit log
├── 01-cast_sheet.png  02-objects_sheet.png  03-storyboard.json
├── 04-contact/ fNN.png  pre_generation_user_review.json
├── 05-shots/ shotNN.mp4
├── master.mp4                    # compliant 9:16 master
└── closeout.md                   # successes/failures/cost, [VERIFIED|PRODUCED] tagged
```

## Integration with Personas / Crew
| Crew role | Owns in this workflow |
|---|---|
| 🔬 Research Lead | Step 1 economics signals; only proven-success tactics |
| 📣 Marketing Lead | Step 2 CampaignBrief (angle/hook/CTA/disclosure) |
| 🎨 Creative Lead | Step 4 cast/objects sheets, storyboard, prompts |
| 🎬 Production Lead | Step 4–5 generation, edit, compose; cost discipline |
| 🛡️ Audit Lead | **every** gate: PGA checklist, verify-before-spend, PRODUCED≠VERIFIED |

## Integration with Other Skills
- **From** `super-spec` / product intake → this skill drives production.
- **Uses** `aegis-approval-gate` (human gates), `compliance_gate` code, the templates + crew docs.
- **To** `aegis-retro` / brain learnings → Step 7 closeout feeds the self-learning loop.

## Hard rules (non-negotiable)
1. No image/video generation without a passing PGA audit AND a recorded human approval (or explicit bypass).
2. Verify-before-spend: economics gate (Step 1) + mandatory budget breaker (every paid Gemini/Veo call).
3. One canonical identity string + Nano Banana Pro reference images (cast+objects sheets) + one seed per run; exactly one face ref; only the intended
   product in frame (hula-hoop pitfalls #1/#2/#8).
4. Honesty: never report PRODUCED work as VERIFIED. The only Auto-Affi number measured is live outcome.
