# Auto-Affi Production Crew — Team Charter

**Status:** Standing crew (human directive, 2026-06-27). Spawned to **ideate + review every
run, following the workflow gates — always.**
**Orchestrator:** Nick Fury (🧬) dispatches the crew; each role maps to a workflow stage/gate
in `docs/principles/2026-06-27-pre-generation-audit-and-approval-gate.md` and the production
workflow diagram. Crew complements (does not replace) the AEGIS personas.

---

## The 5 roles ↔ workflow gates

| Crew role | Owns (workflow) | Mandate | Gate / artifact | Backed by |
|---|---|---|---|---|
| 🔬 **Research Lead** | Pre-stage: product/market/trend intel + economics | Verified market + competitor + winning-pattern signals; only proven-success tactics (no guru claims); validate the Scout economics gate | Scout **economics gate**; trend signals | beast |
| 📣 **Marketing Lead** | Strategist brief | Angle, hook ≤1.0s, PAS/BAB/UGC, CTA, persona, platform fit, disclosure; conversion-first | `CampaignBrief` | iron-man / general |
| 🎨 **Creative Lead** | Cast sheet → Objects sheet → Storyboard → prompts/stills direction | Visual identity + consistency (soul-id), HSO×VCS rubric, prompt craft, Thai no-lipsync | PGA stages 1–4 artifacts | wasp / general |
| 🎬 **Production Lead** | Contact sheet → Video gen → Editor → compose | Asset generation + edit + compose to master; cost/credit discipline; verify-before-spend | PGA stage 5 + credit gate | spider-man / thor |
| 🛡️ **Audit Lead** | EVERY gate (cross-cutting) | Run the PGA checklist, block on fail; compliance gate; verify-before-spend; honesty (PRODUCED≠VERIFIED) | PGA audit at all stages + compliance | loki + black-panther + coulson |

---

## Standing operating rule ("ตาม workflow เสมอ")

For every production run, at each workflow gate:
1. **Ideate** — the owning role drafts/options the artifact (Research feeds → Marketing briefs →
   Creative builds sheets/storyboard → Production generates).
2. **Audit** — the **Audit Lead reviews EVERY artifact before it advances** (runs the PGA
   checklist; blocks on fail). No artifact passes a gate un-reviewed.
3. **Human gate** — per SPEC §10.5 g12, no generation without recorded human approval; only an
   explicit human `bypass <stage>` overrides.

Dispatch pattern: Nick Fury spawns the relevant role(s) per stage in parallel where independent;
the Audit Lead is spawned at **every** gate. Crew returns structured findings (not prose dumps);
the main thread synthesizes and presents to the human at the gate.

## Why
A single thread misses cross-discipline failure modes (the hula-hoop pitfalls were a creative
problem + an economics problem + an audit gap at once). A standing crew with an always-on Audit
Lead makes "ideate then independently review per workflow" the default, not the exception.

See [[feedback-pre-generation-audit-gate]] and `reports/2026-06-27_ai-affiliate-upgrade-plan.md`.
