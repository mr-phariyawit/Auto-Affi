# Auto-Affi — System Upgrade Plan (from successful-operator research)

**Date:** 2026-06-27
**Method:** 41-agent workflow (`wf_943d2d7b-2ae`) — 20 web-research agents (distinct angles) →
20 adversarial verify agents (guru/course-seller filter) → 1 synthesis. 142 tactics survived
verification out of the raw pool.
**Companion docs:** `reports/2026-06-27_gap-analysis-vs-hula-hoop-pipeline.md`,
`.aegis/brain/learnings/2026-06-27_hula-hoop-seedance-pipeline-study.md`

> **Honesty note (global PRODUCED≠VERIFIED rule):** `[VERIFIED]` below means "a subagent
> cited a named, success-evidenced source" — NOT that we independently audited the revenue
> figures. Treat case-study numbers (Tarte $105.88M, Divi $4.7M, Jenn Leach $52K, etc.) as
> *sourced claims to validate*, not as our measured facts. The only number WE have measured
> for Auto-Affi remains: ZERO live posts. Everything here is a hypothesis backlog, not proof.

---

## 1. What winners do differently (8 recurring high-signal patterns)

1. **Pre-spend seller/commission vetting** `[VERIFIED: Jenn Leach $52K case]` — pick affiliate
   commission **≥8–10% BEFORE** producing the video. Same traffic at $1–12 commission vs $50+
   commission = ~10× revenue gap. This is a *gate*, not an optimization.
2. **Micro-creator volume beats mega** `[VERIFIED: Hamster Garage; TikTok data]` — 10K–100K
   followers out-engage mega-creators (30.1% vs 7%). Tarte's $105.88M ran 6,600 creators ×
   23K videos, 88% via the affiliate channel.
3. **Niche-first, single hero SKU** `[VERIFIED: Divi $4.7M, Loop €126.5M]` — depth in one
   community beats broadcast. Sub-5K THB Shopee TH impulse band is the sweet spot.
4. **Commission-tier reality** `[VERIFIED: Shopee TH data]` — beauty 15–20%, electronics 5–10%.
   **<8% commission on sub-5K products is unviable at $3/video.** Test breakeven before scaling.
5. **Content velocity** `[VERIFIED: Hamster Garage 3.2× GMV]` — ≥5–7 posts/week is the
   precondition for viral outliers; problem-solution format drove SwingUp +543%.
6. **Problem-solution > cinematic** `[VERIFIED: Wisesight Q1 2026, 3:1 lift]` — price-comparison
   + before/after beats brand-film HSO. One TikTok Shop supplement: 2.1% → 9.7% CVR in 3 months.
   (Confirms our own SPEC §19.2 v10 correction.)
7. **Price-band conversion law** `[VERIFIED: TikTok Shop data]` — <$30 products convert 5%+;
   >$80 convert <1%. Shopee TH beauty is ~70% sub-$10. Stay low.
8. **Multi-layer ROAS tracking** `[VERIFIED: Tarte]` — Layer1 volume/GMV, Layer2 CTR/speed,
   Layer3 profit with a ≥3:1 ROAS kill-signal. Track **per-video + per-creator**, never just
   aggregate (the "Jenn Leach trap" = good traffic, wrong product, $0).

---

## 2. Priority upgrade table (10 changes)

| # | Upgrade | Why / source | Maps to | Effort | Expected impact |
|---|---|---|---|---|---|
| 1 | **Pre-spend Shopee seller/commission vetting gate** | Jenn Leach failure; winners run 15%+ | GAP-2, §3.1 Scout | 8h | Kills 10–20% of $0-revenue videos before spend |
| 2 | **Commission ≥8–10% hard filter in Scout scoring** | breakeven: $3 ÷ views×CVR×comm needs ≥8% | GAP-2, §3.1 | 6h | <5%-commission queue: 100% → <20% |
| 3 | **Lock ONE niche for 90 days** | Divi/Loop/Tarte: depth > breadth | §1.3 | 4h | 2–3× faster learning per niche |
| 4 | **Systematize 5-variant 3-second hook A/B** | 84.3% viral-hook rule; our §19.1 already wants <1.0s | §19.1 | 12h | Baseline 40–60% 3s retention, test on 50+ |
| 5 | **Default creative = problem→demo→CTA (PAS/BAB)** | Wisesight 3:1; CVR 2.1%→9.7% | §19.2 | 16h | 30–50% CTR lift over 3 weeks |
| 6 | **Daily A/B + auto-pause rollover loop** | Meta Andromeda fatigue (17-day, 30% decay); pause <0.8% CTR | §18 ADR-008 | 20h | ~3 weeks to a winner per niche |
| 7 | **1 render → 4 platform-specific variants** | InfluenceFlow 2.5–4× reach multiplier | §3.6 Publisher | 16h | +50% reach, no extra CPV |
| 8 | **(Phase-2) Micro-creator recruitment network** | Hamster Garage/Tarte | Phase-2 | — | Path to $50K+ GMV/mo |
| 9 | **(Phase-2) Shopee Live integration** | 10% vs 5–7% commission; 5–12% vs 3–5% CVR | Phase-2 | — | 2–3× conversion |
| 10 | **Close GAP-1: visual QC gate before paid gen** | winners QA before spend | GAP-1 | 6h | Brand + compliance; prevents 2–5% policy hits |

---

## 3. Contradictions with current SPEC (decide deliberately)

| Our SPEC choice | What winners do | Reconciliation |
|---|---|---|
| Higgsfield-only (gate 8) | mix generators + platform-native tools | Keep Higgsfield primary; add Shopee/TikTok native image-to-video as a **tier-2 variant source** (also softens GAP-4 failover) |
| edge-tts free Thai VO | casual peer-authority Thai (not formal) | A/B edge-tts vs ElevenLabs on 5–10 videos; upgrade only if completion <40% |
| $3/video target | one source cites $60/video at scale (but 5-channel network) | $3 is correct **iff commission ≥8%**; if <5%, cut to ~$1.50 or shift niche |
| Outcome-zero posture | Divi proved in 2 weeks; Blissim 700 samples → 1K videos | **CRITICAL: clear §20 identity/external gates, ship a 5-video micro-pilot in Week 2 BEFORE any 50+ production push** |

---

## 4. Do NOT copy (failed verification or wrong fit)

- **Live commerce as Phase-1 primary** — needs a live operator; out of scope.
- **"Google Cloud Thai TTS"** — surfaced but **does not exist as described**; use ElevenLabs/Murf if upgrading from edge-tts.
- **$1.8M "Kayla" / "$500–5K/mo guaranteed"** — unverified guru-grade claims; rejected.
- **Pure AI talking-avatar content** — YouTube demonetizes it; our B-roll + VO (no-lipsync) approach is the correct lane, not a limitation.
- **500–2000 creator networks now** — Tarte is brand-partnership-driven; a solo bot must NOT attempt recruitment before ~$1K/mo revenue.

---

## 5. Single highest-leverage next action

**Week 1 — run a real 5-video micro-pilot on Shopee TH with ≥10% commission:**

1. Pick 2–3 sellers: rating >4.5★, 10–15% commission, sub-3K THB (beauty/wellness/gadget).
2. Generate 5 videos (Higgsfield + edge-tts + problem→demo→CTA).
3. Publish real Shopee affiliate links (a test FB/IG account, <1K audience is fine).
4. Measure 7 days: views, clicks, conversions, commission earned.
5. **Success gate:** ≥1 conversion ⇒ ≥~$1.50 revenue = 50% payback proof.
6. **Blocker rule:** if NO seller ≥10% commission exists in the niche → STOP, pivot niche;
   do NOT proceed at <8% margin.

This single real data point validates or kills the entire Phase-1 economics. It also finally
attacks **GAP-5 (outcome-zero)** — which all 20 research angles agree is the real bottleneck,
not the pipeline. Do not scale past 5 videos until the pilot shows a >0.5% conversion signal.

---

## 6. How this binds to prior analysis

- Confirms our hula-hoop study's **verify-before-spend** thesis — winners gate on *commission*
  (GAP-2 economic check) the same way the hula-hoop team learned to gate on *identity/credits*.
- Reframes priority: GAP-5 (ship one real post) > everything. The upgrades in §2 are how you
  *industrialize after* the pilot proves economics, not before.
