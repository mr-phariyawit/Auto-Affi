---
date: 2026-06-09
category: chronicle
confidence: high
scope: project-wide (commit #1 → now)
generated_by: aegis-chronicle
honesty: every claim tagged [VERIFIED] / [REPORTED] / [PRODUCED]
---
# Auto-Affi — Project Chronicle (0 → now)

Span: **2026-05-12 → 2026-06-09** · **95 commits** `[VERIFIED: git rev-list --count HEAD = 95]`
First: `7df70843 docs: add end-to-end SPEC` · Last: `25f724b3 chore: cleanup goal` (06-08) + this session (06-09).
Note: a large stream of real work (the 2026-06-03 production runs, 06-04 Hollywood research, KIE work)
lives in `runs/`, `docs/research/`, `data/` — **outside discrete git commits** (gitignored / folded into
the hard-reset). Activities below therefore merge the committed spine with the uncommitted streams.

## 📅 Timeline — phases of work

| Phase | Dates | What happened |
|---|---|---|
| **A. Spec & research blitz** | 05-12 | End-to-end SPEC, AI-video-editor stack, LLM allocation, Thai-GenAI stack, kie.ai gateway, 300% execution playbook, ISO-29110 gap + Tier-1 docs, repo skeleton + CI, Shopee adapter + subId, Scout scoring, wiki hook library, CampaignBrief/Storyboard schemas, claim auditor, Anthropic adapter, local renderer, demo.mp4 — **all in one day** |
| **B. AEGIS + Sprints 1–6** | 05-13 | AEGIS v12 bootstrap; sprints 1–6 in a single day — strategist, safety gate, video pipeline, publishing, analytics, wiki curator, orchestration, phaya.io gateway, GCS staging (ADR-006), Writers' Room, run_once, Ops Console, deploy, multi-platform/niche. Reported **"roadmap 100%, 13/13 epics, 481 tests, 163pt"** `[REPORTED in commit 4861ed0c/48647de5 — not re-verified]` |
| **C. Studio approval flow (ADR-007/008)** | 05-13 | 10-stage gated MANUAL/AUTONOMOUS flow (sprints 7–9), `ProductionDirector`, dual-mode design |
| **D. Real creative pipeline + vendor thrash** | 05-14 → 05-18 | concept-2 Gemini+Seedance, HyperFrames, captions/hook-validator/parallel-variants, product-identity lock, **HeyGen Avatar IV added (05-15) then REMOVED (05-18)**, AiStoryboard v2, edge-tts, affiliate-conversion creative learning, Higgsfield-CLI unified gateway, variant-testing pipeline v14 |
| **E. Framework upkeep + hard-reset** | 05-23 → 06-08 | AEGIS v15.0→v15.1.0; consolidate knowledge + full code snapshot (05-29); complete hard-reset to consolidated baseline (06-08); regenerate gate-centric Phase-1 spec/breakdown/sprint; **GOAL cleanup loop** (verify runs, merge SUPER_SPEC→SPEC, tidy venv, code-review) |
| **(off-VCS) Production runs + Hollywood pivot** | 06-03 → 06-05 | 2 real review clips (silicone shoe-covers, geeso umbrella); KIE Seedance + ElevenLabs v3 Thai VO; 06-04 research pivot toward a "Hollywood cinematic studio"; 8 new product-intelligence CSV rows |
| **F. This session** | 06-09 | Full-recursive read of every doc + as-built code; AEGIS reinstall (doctor GREEN); built `aegis-chronicle` skill + this ledger |

## ✅ Successes (what worked)
1. **Foundation velocity** — a complete spec + repo skeleton + a code-level Phase-1 closed loop stood up in ~2 days. `[VERIFIED: git history, 50+ commits 05-12/05-13]`
2. **Hard-won creative method** — HSO×VCS rubric, the affiliate-conversion correction (UGC testimonial > brand film; price-comparison beats cinematic 3:1), Thai-VO-separate-from-visual, cleanroom audio (0 source / exactly 1 final stream), and the speed-guard (warn 1.08× / reject 1.15×). Distilled from rejected versions **v1–v13**. `[VERIFIED: docs + runs encode it]`
3. **Real architecture** — Pydantic contract layer with pre-spend validators, `ProductionDirector` 10-stage state machine + atomic persistence, variant orchestrator with shared-shot dedup (11 renders not 21), cost circuit-breakers (editor $0.40, daily $50), bilateral-sync wiki. `[VERIFIED: read at git HEAD — 87 files / ~15k LOC]`
4. **A real honesty reckoning was written down** — SPEC §17 "code-complete, outcome-zero" + the four open blockers. Rare and valuable self-honesty. `[VERIFIED: §17–20]`
5. **Two production clips actually rendered + locally verified** — shoe-covers 30s, all 11 voice segments at 1.0× via KIE ElevenLabs v3, cleanroom PASS. `[VERIFIED: approval_packet.json audio_cleanroom + ffprobe in run]`
6. **ISO-29110 governance scaffolding** — SRS, test-plan, coding/prompt standards, 8 ADRs, 20-risk register. `[VERIFIED: docs present]`
7. **AEGIS framework adopted + reinstalled clean this session** — `aegis-doctor` GREEN. `[VERIFIED: tools/aegis-doctor.sh exit 0]`

## ❌ Failures / mistakes (the expensive part)
1. **Velocity theater** — "roadmap 100% / 13 epics / 481 tests / 163pt" was reported on a single day (05-13) while the real outcome was **zero**. This is the headline failure (SPEC §17.3). `[VERIFIED by absence + §17.3]`
2. **Outcome-zero** — across the whole project: **0 live posts, 0 real clicks, 0 Shopee commission**; the Phase-1 exit criterion (1 video → publish → metric) never ran against a real platform. `[VERIFIED by absence: no real PublishRecord]`
3. **Vendor / direction thrash** — kie.ai → Phaya → PiAPI → HeyGen → Higgsfield (+ KIE re-added as fallback). **HeyGen was added and removed within 3 days** (05-15 → 05-18). ~5 days re-rendering the same demo instead of shipping one real post. `[VERIFIED: git history]`
4. **External blockers never cleared** — Shopee Affiliate approval, Meta/IG token, Higgsfield credits, runtime host. Four human/identity gates, **none of them code** — yet the team kept writing code. `[VERIFIED: §20]`
5. **Three divergent execution paths** — run-local scripts (newest, KIE), `scripts/produce-variant-set.py` (Higgsfield), and `ops/produce.py` `ProductionDirector` (stages 4–8 emit **fixture** `gs://` URIs, publish is `dry_run`). The clips that shipped used the run-local path, not the "studio" engine. `[VERIFIED: read at HEAD]`
6. **Scope drift** — 4 direction eras culminating in a 06-04 "Hollywood $5M studio" pivot while Phase-1 (1 post + 1 click) was still unclosed. `[VERIFIED: docs/research 06-04]`
7. **Work outside version control** — the 2 production runs, Hollywood research, and product CSVs were not committed as discrete history; the 362 KB `SUPER_SPEC.md` was consolidated to a 2 KB stub by the GOAL loop and survives only as git blob `d54717af` (recoverable, but it was nearly lost to disk). `[VERIFIED: git cat-file -s d54717af = 362359]`
8. **Doc-era drift never reconciled** — kie-era docs (Veo/Sora/14-agent crew) vs Higgsfield-era docs coexist; a research synthesis even asserted THB/rebate figures that its own source playbooks do not contain. `[VERIFIED: full-read cross-check]`
9. **Unverified test counts** — "481 tests" (05-13) / "614 pass" (§17, 05-29) vs 277 test functions found at HEAD; never re-run this session. `[REPORTED, NOT VERIFIED]`

## 📘 Lessons (generalizable, actionable)
1. **"Done" = VERIFIED outcome, not produced artifact.** Code-complete ≠ done. (This project is the origin story of that rule.)
2. **Ship ONE real unit before optimizing the stack.** Pick one vendor, get one real post + one real click, *then* tune. A swap that re-renders the same demo is motion, not progress.
3. **Surface coverage/blocker gaps on Day 1.** External/identity gates (approvals, credits, tokens, host) belong on the board before any code sprint — not discovered after "100%."
4. **Keep the real execution path singular.** Don't let a governance/fixture flow and the actual render scripts diverge; the demo should run through the same engine that ships.
5. **Commit the artifacts that matter** (run manifests, approval packets, research) — you can't audit or learn from what was never in VCS.
6. **Velocity metrics are vanity** (pt / tests / "% complete") unless each is tied to a real outcome KPI (post live, click recorded, commission paid).
7. **Decisions before swaps** — log an ADR + decision-audit entry before changing vendor/direction; thrash is cheaper to prevent than to unwind.

## 🔁 Anti-patterns to stop repeating
- 🔁 "**100% complete**" declared from velocity, not outcome.
- 🔁 **Vendor-of-the-week** swaps that reset the demo instead of advancing it.
- 🔁 **Building around an unopened gate** (writing publish code with no platform approval).
- 🔁 **Bigger-vision pivot** while the smallest real loop is still unclosed.

## Current state (as of 2026-06-09)
- Codebase preserved at git HEAD (87 src files); working tree is the consolidated baseline (`SPEC.md` 38 KB + `SUPER_SPEC.md` 2 KB stub; 362 KB original = blob `d54717af`).
- AEGIS v15.1.0 installed, `aegis-doctor` GREEN; hooks load on next session restart.
- Pending gate-centric sprint **AFFI-S1-01…08** (offline vertical slice → 1 compliant master) is queued.

## Open gates (still the real critical path — human-only, none are code)
1. Shopee Affiliate TH approval · 2. Meta/IG token · 3. Higgsfield credits · 4. runtime host.
**Phase-1 done = ONE real video live + ONE real subId click — verified, not produced.**

## Recommended next skills → see the response that generated this file (Step 6).
- [HyperFrames transitions](2026-06-28_hyperframes-transitions.md) — 14 shaders + apply rule
