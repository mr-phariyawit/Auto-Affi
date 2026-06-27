# Auto-Affi Crew — first workflow review (5-role spawn)

**Date:** 2026-06-27
**Crew:** Research / Marketing / Creative / Production / Audit Leads (spawned per `docs/team/auto-affi-crew.md`).
**Scope:** review the current production workflow + the just-built PGA gate before the first real run.
**Honesty:** findings are static-read reviews (agents did not execute the pipeline); the Audit/Production
exploits were grep-confirmed against source. Treat as reasoned, high-confidence, not runtime-proven.

---

## ⚠️ Headline: the PGA gate I shipped is BYPASSABLE — my "machine-enforced" claim was overstated

The Audit Lead (adversarial) found the gate does not actually bind the approval to what gets generated.
My prior PR/commit called it "machine-enforced"; the honest status is **"procedurally enforced for the
video stage, opt-in, and decoupled from the generated content."** Correcting this now.

### CRITICAL (Audit + Production cross-confirmed)
1. **Audit decoupled from generation** — `assert_may_generate` checks only booleans; it never re-hashes
   the actual prompt/images being sent vs the approved `prompt_hash`. Approve a clean manifest, then
   `generate_video(prompt="anything", images={two faces})` → passes. *(fixing this turn)*
2. **Gate is opt-in (`if run_dir is not None`)** — defaults OFF; any caller omitting `run_dir` (incl.
   live `dry_run=False`) generates ungated. A safety gate that defaults off is not a gate. *(fixing this turn)*
3. **Image stages 1–4 have NO gate** — only `generate_video` exists; cast/objects/storyboard/contact
   stills are never routed through the gate, yet gate 10 says EVERY image. *(follow-up: needs `generate_image`)*
4. **Credit check unwired + live cost hardcoded `$0.00`** — verify-before-spend is defined, not enforced;
   budget breaker is blind to real spend. *(follow-up)*

### HIGH
5. **`prompt_hash` omits face_reference_count + reference URIs** — false determinism; swap the face ref
   without changing the hash. *(fixing this turn)*
6. **`bypass` ignores `audit_pass`** — can override a known-failing hard-compliance audit (banned claims /
   restricted category). *(follow-up)*
7. **Per-shot audit only — no board-level consistency** (Creative) — soul_id is optional where it IS the
   consistency mechanism; nothing checks every shot shares the storyboard's seed/soul_id or that
   `visual_reference_lock` files exist; duration cap mismatch (schema 6s vs PGA 10s). *(follow-up)*
8. **CampaignBrief missing conversion levers** (Marketing) — no `framework` (PAS/BAB/UGC), no ≤1.0s
   hook-variant field, no disclosure/platform field; disclosure is advisory-only downstream. *(follow-up)*

### Honesty holes flagged
- `approved_by="human"` asserted, never verified; `approvals.json` is forgeable/unsigned (TOCTOU).
- A passing test (`test_generate_video_unguarded_without_run_dir`) blessed the escape hatch.
- Live `cost_usd=0.0` makes spend invisible to the cost watcher.

---

## Where the crew agreed the real bottleneck is
Research + Production + the prior gap analysis converge: **GAP-5 (outcome-zero) is the bottleneck, not more
code.** The economics gate is sound design on *unverified* assumptions. The single highest-leverage action
remains the **Week-1 5-video micro-pilot** on a real Shopee product (≥10% commission) to get ONE measured
conversion. The gate hardening below is cheap insurance so the pilot's real spend can't be wasted by the
exploits above.

## Disposition
- **This turn:** fix exploits #1, #2, #5 (fail-closed live gate + bind audit-hash to generation + hash
  covers face refs), TDD, update PR.
- **Follow-up tasks spawned:** image-stage gating (`generate_image` behind the gate), credit-check wiring +
  real cost accounting, bypass-respects-hard-compliance + tamper-evident approvals, board-level consistency
  audit, CampaignBrief framework/hook/disclosure fields.
