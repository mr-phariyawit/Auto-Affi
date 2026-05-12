# Loki Adversarial Review -- Resonance Enrichment

> Reviewer: Loki (devil's advocate)
> Date: 2026-05-13
> Scope: All 8 new/updated resonance files + 5 ADRs
> Method: Each claim tested against SPEC, internal consistency, and external reality

---

## 1. north-stars.md

### Challenge 1.1: GMV $50k/mo at Phase 3 -- realistic?
- **Claim**: Phase 3 GMV target is $50k+/month
- **Counter-evidence**: At 100 videos/day, $50k/mo requires ~$17/video in GMV.
  At 4% CTR and average Shopee Beauty order ~$10-15, commission ~5-8%, that is
  $0.50-1.20 per click that converts. Need ~42k-100k converting clicks/month.
  At 4% CTR on views, need ~1M-2.5M views/month across 3000 videos. Achievable
  but aggressive for Thai Beauty niche on organic-only.
- **Verdict**: ACCEPT. Aggressive but within the range of successful Shopee
  affiliate accounts in TH. The learning loop is designed to improve CTR over time.
  Risk is appropriately flagged in SPEC section 14.

### Challenge 1.2: MoM CTR uplift >= 5% -- sustainable?
- **Claim**: Phase 3 KPI requires >= 5% month-over-month CTR improvement
- **Counter-evidence**: CTR improvement has diminishing returns. Going from
  1.5% to 4% over 6 months is ~17% MoM. But sustaining 5% MoM after reaching
  4% means hitting 4.2%, 4.41%, 4.63%... which hits a ceiling.
- **Verdict**: REVISE. The resonance file should note this is a Phase 3 *start*
  target, not a perpetual requirement. Recommend adding: "Expected to taper as
  CTR approaches platform ceiling (~6-8% for top performers)."

### Challenge 1.3: Cost/video $3 vs $2.87 discrepancy
- **Claim**: SPEC 1.2 says "<= $3", Appendix C totals $2.87
- **Counter-evidence**: Not a conflict -- $2.87 is the itemized estimate,
  $3.00 is the target with headroom.
- **Verdict**: ACCEPT. Correctly captured in cost-model.md as "$0.13 headroom."

---

## 2. non-goals.md

### Challenge 2.1: "Creator marketplace" as permanent non-goal
- **Claim**: "No human creator in loop" is permanent
- **Counter-evidence**: SPEC 1.3 says "ไม่ใช่ creator marketplace" without
  specifying permanence. However, SPEC 1.1 vision says "AI Marketing Company"
  and "humans as supervisors only." The entire architecture assumes AI-only content.
- **Verdict**: ACCEPT. The vision is structurally incompatible with human creators.

### Challenge 2.2: Phase-gated non-goals correctly categorized?
- **Claim**: Multi-niche is Phase 2, multi-tenant is Phase 3
- **Counter-evidence**: SPEC 13 Phase 3 says "multi-account, multi-niche scaling."
  SPEC 1.3 says "no multi-tenant SaaS in Phase 1" (implies Phase 2 or later).
- **Verdict**: ACCEPT. Categories are correct per SPEC.

---

## 3. architecture-principles.md

### Challenge 3.1: Subsystem map complete?
- **Claim**: 6 subsystems listed (Orchestrator, Agent Crew, Asset Pipeline,
  Data Plane, Publishing Plane, Learning Loop)
- **Counter-evidence**: SPEC also mentions "Shared Context Bus" (Postgres + Redis)
  in the architecture diagram, and "Ops Console" (Next.js, SPEC 7). These are
  arguably subsystems.
- **Verdict**: REVISE. Add "7. Shared Context Bus (Postgres + Redis)" and
  "8. Ops Console (Next.js + shadcn/ui)" to the subsystem map. These are
  infrastructure and UI respectively, but they are distinct subsystems in the
  architecture diagram.

---

## 4. agent-hierarchy.md

### Challenge 4.1: Director authority vs Critic power
- **Claim**: Director has "FINAL DECISION authority" after debate
- **Counter-evidence**: What if Critic identifies a genuine compliance violation?
  Does Director override?
- **Verdict**: ACCEPT. Director decides creative/strategic questions. Compliance
  violations are handled by Safety agent (hard-block), not by Director discretion.
  The hierarchy is correct: Director decides creative, Safety overrides on compliance.

### Challenge 4.2: Phase 1 simplification not highlighted enough
- **Claim**: Writers Room has 6 sub-agents
- **Counter-evidence**: SPEC 13 Phase 1 says "1 Writer agent, no debate."
  The resonance file lists the full team but notes Phase 2+ for some agents.
- **Verdict**: ACCEPT. Phase gating is correctly noted.

---

## 5. autonomy-stance.md

### Challenge 5.1: "Human as supervisor" vs Meta/YouTube ToS
- **Claim**: Fully autonomous publishing
- **Counter-evidence**: Meta ToS requires a "real person" behind branded content.
  YouTube automated content policies could flag AI-generated content. Thailand's
  upcoming AI content regulations may require disclosure.
- **Verdict**: ACCEPT with NOTE. The system includes mandatory disclosure
  (#advertising/#affiliate per NBTC). Platform ToS compliance is handled by
  Safety agent checks. The "human as supervisor" means a human IS accountable --
  they just don't create content manually. This satisfies most ToS "real person"
  requirements. Flag for periodic ToS review (already in domain-thai.md).

---

## 6. cost-model.md

### Challenge 6.1: Veo 3 at $1.80/video -- stable pricing?
- **Claim**: Video gen (Veo) costs $1.80
- **Counter-evidence**: Veo 3 is relatively new. Pricing may change. At 100
  videos/day, that is $180/day on video gen alone.
- **Verdict**: ACCEPT. The multi-vendor adapter (Phase 2) mitigates vendor
  pricing risk. The fallback recipe system handles outages. The cost model
  is appropriately Phase 1 scoped.

---

## 7. domain-thai.md

### Challenge 7.1: Mega-sale calendar -- complete?
- **Claim**: Lists monthly doubles, Songkran, Mid-Year, 11.11, 12.12, New Year
- **Counter-evidence**: Missing: Valentine's Day (beauty gift surge), Mother's Day
  (August in Thailand, major beauty gift), Lazada birthday sales (competitor but
  affects market), PayDay sales (end of month).
- **Verdict**: REVISE. Add Valentine's Day (Feb 14), Mother's Day TH (Aug 12),
  and note PayDay patterns. These are significant for Beauty niche.

---

## 8. learning-loop.md

### Challenge 8.1: 7-day outcome labeling -- too slow?
- **Claim**: Each video gets outcome label after 7 days
- **Counter-evidence**: Viral content peaks at 24-48h on Reels/Shorts. Waiting
  7 days means the learning loop misses the peak signal.
- **Verdict**: ACCEPT. The 7-day label captures full-funnel outcome (including
  conversions/GMV which lag). Early signals (views at 1h/6h/24h) are already
  collected by Analytics Collector. The 7-day label is for definitive classification.

---

## 9. ADRs (001-005)

### All 5 ADRs reviewed
- ADR-001 (Hierarchy): ACCEPT -- well-reasoned, consequences balanced
- ADR-002 (Schema): ACCEPT -- Pydantic is the right choice for Python
- ADR-003 (Wiki Sync): ACCEPT -- Phase 1 human-review gap correctly noted
- ADR-004 (Cost Control): ACCEPT -- three-layer model is comprehensive
- ADR-005 (Temporal): ACCEPT -- alternatives adequately dismissed

---

## Summary

| Verdict | Count | Items |
|---------|-------|-------|
| ACCEPT | 13 | Most claims validated against SPEC |
| REVISE | 3 | MoM CTR sustainability note, subsystem map gaps, mega-sale calendar gaps |
| REJECT | 0 | -- |
| ESCALATE-TO-HUMAN | 0 | -- |

## REVISE Actions Required

1. **north-stars.md**: Add note that MoM CTR uplift 5% is a Phase 3 start target,
   expected to taper as CTR approaches platform ceiling
2. **architecture-principles.md**: Add Shared Context Bus and Ops Console to subsystem map
3. **domain-thai.md**: Add Valentine's Day, Mother's Day TH, PayDay patterns to mega-sale calendar
