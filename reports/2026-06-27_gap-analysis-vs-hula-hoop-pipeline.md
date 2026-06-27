# Gap Analysis — Auto-Affi vs. external Hula-Hoop Seedance Pipeline

**Date:** 2026-06-27
**Analyst:** AEGIS team (study request)
**Baseline studied:** `wPWBPsAQ.tgz` — external single-product affiliate-video pipeline (hula-hoop ฿239, Shopee TH).
**Subject:** Auto-Affi (this repo) at branch `claude/ai-marketing-platform-JFcLs`.
**Companion artifact:** `.aegis/brain/learnings/2026-06-27_hula-hoop-seedance-pipeline-study.md`

> Method: every "Auto-Affi reality" claim below is grounded in the actual SPEC.md §17–20
> and in `grep` over `src/`. Claims are tagged `[VERIFIED]` (read from code/spec) or
> `[INFERRED]` (reasoned, not directly proven). Per the global PRODUCED≠VERIFIED rule.

---

## 0. TL;DR (decision-first)

Auto-Affi is the **systematized, hardened** version of the hula-hoop pipeline — same shape
(Scout→Strategist→Writer→Storyboard→Producer/Editor→Compliance→Publish), but with real
schemas, cost caps, compliance gates, a cleanroom verifier, hard-reset discipline, and a
stronger character-lock (`soul-id`) than the hula-hoop's "single frame + identity string".

**But the two projects share the SAME headline failure** — lots PRODUCED, **ZERO live
outcome VERIFIED** — and Auto-Affi has it *worse on one axis*: the hula-hoop project at
least fired real paid generations and learned real pitfalls; Auto-Affi built the gates but
**never fired one real paid run end-to-end to a live platform** (SPEC §17.1, §17.3).

The gaps that matter are **3 tactical** (un-enforced pre-spend gates the hula-hoop project
paid cash to learn) + **1 strategic** (over-built gates, under-ran reality).

---

## 1. Where Auto-Affi already WINS (hula-hoop lessons already solved)

| Hula-hoop pitfall | Auto-Affi state | Evidence |
|:--|:--|:--|
| Legacy script left in tree ("do NOT use") | Hard-reset discipline; HeyGen fully removed; SPEC consolidated to one file | `[VERIFIED]` SPEC §17.2, tasks #28–32 |
| Single identity string fragile across shots | Higgsfield `soul-id` trained persona (~$5 once), capped per ad to avoid drift | `[VERIFIED]` SPEC §19.3 |
| Vague "be careful" warnings | Hard per-run compliance gates + post-hoc verifier | `[VERIFIED]` SPEC §10.5, `scripts/verify_runs.py`, `pipeline/compliance_gate.py` |
| No cost ceiling | 3-layer cost control: per-node caps + circuit breaker + per-tool tracking | `[VERIFIED]` ADR-004, `pipeline/editor_budget.py` ($0.40 hard cap) |
| Ad-hoc provider payloads | Adapter pattern behind a typed boundary | `[VERIFIED]` `adapters/higgsfield_cli.py` |
| No human review of frames | Mandatory 3×3 storyboard contact-sheet approval before paid call (gate 9) | `[VERIFIED]` SPEC §10.5 gate 9, `pre_generation_user_review.json` |

**Verdict:** Auto-Affi has out-engineered the hula-hoop project on structure. The architecture
is not the problem.

---

## 2. TACTICAL GAPS — hula-hoop pitfall-fixes NOT yet enforced in Auto-Affi

These are concrete fixes the hula-hoop team paid real credits to discover, that Auto-Affi
has **not** wired as automated pre-spend gates.

### GAP-1 — No pre-flight VISUAL identity verification before paid video-gen 🔴
- **Hula-hoop pitfall #1/#2:** starting frame face ≠ character → Seedance output wrong → whole
  batch of credits wasted. Their fix: `vision_analyze(frame, ref)` must confirm "same person"
  *before* the paid call.
- **Auto-Affi reality:** the only pre-flight is a *text* claim auditor
  (`claim_auditor.py:209` "Publisher pre-flight check"). There is **no visual check** that the
  keyframe/still actually matches the `soul-id` persona before firing Higgsfield. `[VERIFIED: grep found zero vision/identity/face-match guard in src/]`
- **Risk transferred:** soul-id reduces drift but does not eliminate a bad input keyframe
  (e.g. a Gemini still that rendered an off-model face). One bad still → paid video-gen on a
  wrong face → ~$3.6/ad burned, same failure class.
- **Fix:** add an automated `identity_preflight` gate: vision-compare the chosen still vs. the
  persona reference; block the Higgsfield call on mismatch.

### GAP-2 — Provider credit-balance check exists but is NEVER enforced 🔴
- **Hula-hoop pitfall #5:** credits ran out mid-batch → partial loss.
- **Auto-Affi reality:** `higgsfield_cli.account_credits()` EXISTS
  (`adapters/higgsfield_cli.py:200`) but **is called nowhere** —
  `[VERIFIED: grep "account_credits" across src/scripts/tools shows definition only, zero call-sites]`.
  Auto-Affi's cost controls are all *our-side accounting* (editor budget, daily budget×1.1);
  none assert the *provider* pool can cover the batch before firing.
- **Risk transferred:** identical to hula-hoop #5 — a multi-shot ad batch can die halfway,
  losing the credits already spent on completed shots.
- **Fix:** wire `account_credits()` as a hard pre-batch gate in `ops/produce_slice.py`:
  estimate batch cost → assert provider balance ≥ cost × safety-margin → else block + queue.

### GAP-3 — No "generate a NEW image" guard on Gemini stills 🟡
- **Hula-hoop pitfall #4/#6:** Gemini returned the reference sheet instead of a new image;
  OpenRouter returned `content: null` with the image hidden in `images[0]`.
- **Auto-Affi reality:** uses "Gemini Nano Banana Pro" for stills (SPEC §19.3) — same provider,
  same failure surface. No guard found that asserts the returned still is a *new* render and
  not an echoed reference. `[INFERRED: no still-validation code surfaced in grep]`
- **Fix:** validate still output (dimensions/hash differ from reference; non-null image field)
  before it enters the pipeline.

### GAP-4 — "Multi-vendor fallback" is spec-only; one real video adapter exists 🟡
- **Hula-hoop pitfall #2:** Veo's hidden RAI audio filter blocked them mid-project → forced
  swap to Seedance. Lesson: never hard-assume one provider's constraints.
- **Auto-Affi reality:** SPEC §7 promises Veo/Runway/Kling behind `VideoGenAdapter`, but only
  `higgsfield_cli.py` is implemented, and gate 8 ("Seedance-Only Visual") + §19.3 deliberately
  **lock to Higgsfield/Seedance**. `[VERIFIED: adapters/ contains only higgsfield + shopee]`
  This is a *reasoned* lock (Thai-lipsync constraint), not thrash — but it means a Higgsfield
  outage or policy change has **no failover**, the exact scenario that bit the hula-hoop team.
- **Fix (deliberate, not urgent):** keep the lock, but document a tested fallback runbook
  (veo3_1_lite is already referenced for establishing shots) so a Higgsfield outage degrades
  gracefully instead of halting.

---

## 3. STRATEGIC GAP — over-built gates, under-ran reality 🔴🔴

This is the most important finding and it is **mutual**, but Auto-Affi is further from the
finish line on the one axis that counts.

- **Hula-hoop project:** thin process, but it **actually ran** — uploaded frames, fired paid
  Seedance batches, produced real `.mp4`s, and harvested 8 concrete pitfalls *because real
  money hit a real API*. Its lessons are battle-tested.
- **Auto-Affi:** SPEC §17.1 (measured) — **614 unit tests pass, ZERO live posts, ZERO clicks,
  ZERO commission, ZERO §1.2 KPI.** §17.3 names the headline failure: roadmap said "100%
  complete" while truth was "code-complete, outcome-zero", after ~5 days of vendor thrash that
  re-rendered the same demo instead of shipping one real post.

**The gap is not more code.** It is the 4 un-cleared external/identity blockers (SPEC §20):
1. `[EXTERNAL]` Shopee Affiliate TH approval (1–7 days) — blocks everything.
2. `[EXTERNAL]` Meta Business + IG Creator + 60-day Graph token.
3. `[EXTERNAL]` Higgsfield account + credits.
4. `[IDENTITY]` Runtime host decision (laptop cron vs VPS vs Temporal Cloud).

The hula-hoop project's existence is the proof: a *worse-engineered* pipeline that **fired one
real paid run** learned more about production reality than Auto-Affi's 614 green tests did.

---

## 4. Gap summary table

| ID | Gap | Severity | Type | Hula-hoop origin | Fix owner |
|:--|:--|:-:|:--|:--|:--|
| GAP-1 | No pre-spend visual identity check | 🔴 High | Code | Pitfall #1/#2 | dev (1 gate) |
| GAP-2 | Provider credit-balance check not wired | 🔴 High | Code | Pitfall #5 | dev (wire existing method) |
| GAP-3 | No "new image" guard on Gemini stills | 🟡 Med | Code | Pitfall #4/#6 | dev (validator) |
| GAP-4 | Single real video adapter; no failover runbook | 🟡 Med | Process | Pitfall #2 | architect |
| GAP-5 | **Outcome-zero: never fired a real live run** | 🔴🔴 Critical | External/Human | shared headline failure | **human (4 blockers, §20)** |

---

## 5. Recommended action order

1. **Wire the two verify-before-spend gates now** (GAP-1, GAP-2) — they are pure code, small,
   and directly bind to the global PRODUCED≠VERIFIED rule. Effectively free insurance before
   any real credits are ever spent.
2. **Add the Gemini still validator** (GAP-3) — cheap, prevents a known echo failure.
3. **Clear the §20 external blockers** (GAP-5) — this is the real critical path. Belongs to the
   human (Identity/External categories → already tracked in SPEC §20 / human-queue). Nothing in
   §1–4 ships outcome until this is done.
4. **Document the Higgsfield-outage fallback runbook** (GAP-4) — deliberate, low urgency.

**Definition of done (unchanged from SPEC §20):** ONE real video live on a real platform with
ONE real subId click recorded — *verified, not produced.*
