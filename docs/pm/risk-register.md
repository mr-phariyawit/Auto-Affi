# Risk Register — Auto-Affi

> Formal register ตาม ISO 29110 guideline. **Live updates อยู่ใน Linear** (label `risk`) — ไฟล์นี้ track ระดับ baseline + canonical mitigation

- **Owner**: Nick Fury
- **Review cadence**: weekly ใน status report
- **Scoring**: Probability 1-5 × Impact 1-5 = Exposure (1-25)
- **Last updated**: 2026-05-12

---

## Scoring Legend
| Score | Probability | Impact |
|---|---|---|
| 1 | Rare (<5%) | Negligible (<1d delay) |
| 2 | Unlikely (5-25%) | Minor (1-3d delay or <$200 loss) |
| 3 | Possible (25-50%) | Moderate (3-7d delay or $200-1k loss) |
| 4 | Likely (50-75%) | Major (1-2wk delay or $1k-10k loss) |
| 5 | Almost certain (>75%) | Critical (>2wk delay or >$10k loss / project failure) |

**Exposure thresholds**: 1-6 low / 7-12 medium / 13-25 high — high = weekly review + owner assigned

---

## Active Risk Register

| ID | Category | Risk | P | I | Exp | Owner | Mitigation | Contingency | Status | Review |
|---|---|---|---|---|---|---|---|---|---|---|
| R-01 | Platform | Shopee Affiliate API ban / key revoke | 2 | 5 | 10 | Nick Fury | ToS-compliant only, multiple app_id rotation, signature debugging, monitor API changelog weekly | Pause publishing, manual link until reinstated, escalate via partner channel | Open | weekly |
| R-02 | Platform | TikTok / IG / YT account suspension (multi-account hygiene) | 4 | 4 | 16 | Ops | Burner portfolio (10/niche), content fingerprint diversity, 2FA + hardware key, IP allowlist, manual warm-up | Spawn replacement burner immediately, re-distribute content load | Open | weekly |
| R-03 | Compliance | OCPB / PDPC violation (misleading claim, missing disclosure, PII collection) | 3 | 5 | 15 | Safety | Critic Opus + Typhoon verifier pre-publish, hard-block list (medical/whitening/financial), #โฆษณา auto-tag, no PII collection via landing proxy | Pull video, file appeal if needed, legal consult (PDPC fines up to 5M THB) | Open | weekly |
| R-04 | Cost | LLM / video gen cost runaway | 3 | 4 | 12 | Tech Lead | Budget controller hard cap, per-scene cost predictor, kie.ai gateway (-51% cost), throttle ที่ 80% / kill ที่ 110% | Auto-kill workflows, manual review, downgrade Opus→Sonnet temp | Open | weekly |
| R-05 | Quality | Wiki rot / pattern overfit / catastrophic forgetting | 3 | 4 | 12 | AI Eng | Tiered wiki (Hypothesis→Validated→Canonical→Deprecated), bilateral-sync (review queue not direct write), offline replay weekly, canonical exemplar lock | Roll back to last canonical snapshot, manual curation sprint | Open | monthly |
| R-06 | Vendor | Veo / Sora / Runway outage or breaking API change | 3 | 3 | 9 | Tech Lead | Multi-vendor adapter via kie.ai + direct fallback, Open-Sora 2.0 standby (Phase 3) | Switch primary in adapter config, alert in 5 min | Open | monthly |
| R-07 | Quality | Hallucinated claim in Thai script | 3 | 4 | 12 | AI Eng | Critic Opus + Typhoon 2 verifier + claim-auditor MCP + Safety hard gates | Block publish, write to anti-pattern wiki | Open | weekly |
| R-08 | Tech | Temporal / Postgres data loss | 2 | 5 | 10 | Tech Lead | Daily snapshot, 30-day retention, weekly restore drill, cross-region replica | Restore from latest snapshot, accept ≤ 24h data loss | Open | monthly |
| R-09 | Tech | Tool-call compounding failure (3-15%/call × 9 agents) | 4 | 3 | 12 | AI Eng | Idempotent tools, retry with backoff, circuit-breaker in Temporal, tool budget per agent | Manual workflow restart, debug trace in Langfuse | Open | weekly |
| R-10 | Process | Bag-of-agents topology drift (peer-to-peer agent calls) | 2 | 5 | 10 | Tech Lead | Architecture decision lock — strict hierarchy, schema-validated handoffs only, code review enforces | Refactor sprint immediately if detected | Open | per-PR |
| R-11 | People | Key person dependency (single AI Eng / Video Eng) | 3 | 4 | 12 | Nick Fury | Pair on critical paths, doc-as-code, runbook for every subsystem | Pause non-critical work, redistribute, hire contract | Open | monthly |
| R-12 | Vendor | kie.ai service quality / pricing change | 2 | 3 | 6 | Tech Lead | Adapter pattern (kie.ai = primary, direct vendor = fallback), monthly pricing review | Switch to direct vendor in adapter | Open | monthly |
| R-13 | Vendor | ElevenLabs / Botnoi outage or Thai voice quality drop | 2 | 3 | 6 | Video Eng | ElevenLabs primary, Botnoi + Azure secondary, voice clone backup library | Switch TTS provider in pipeline config | Open | quarterly |
| R-14 | Quality | TikTok algo change ทำให้ KPI ตก | 3 | 4 | 12 | AI Eng | Weekly algo signal monitor (official changelog + creator forum + variance test), adaptive wiki rules | Re-run Strategist with new constraints, suspend campaigns until validated | Open | weekly |
| R-15 | Compliance | Direct Marketing License threshold (THB 1.8M revenue/year) crossed without registration | 2 | 4 | 8 | Nick Fury | Monitor revenue monthly, register at THB 1.5M proactively | File registration, accept temporary pause | Open | monthly |
| R-16 | Tech | Prompt injection via Shopee / social scraping content | 2 | 4 | 8 | AI Eng | Untrusted content tag, sandboxed tool perms, output filter | Detect → quarantine → patch system prompt | Open | monthly |
| R-17 | Process | Wiki self-poisoning (agent writes wrong pattern, others learn it) | 3 | 5 | 15 | AI Eng | Bilateral sync mandatory, Safety promote only, offline replay vs canonical | Roll back wiki to last known good, audit all entries since | Open | weekly |
| R-18 | Cost | Burner account creation cost / phone number supply | 3 | 2 | 6 | Ops | Bulk SIM contract, virtual number fallback (where ToS allows) | Pause new account spawn, prioritize existing | Open | monthly |
| R-19 | Quality | AI-generated content label / detection penalty | 3 | 3 | 9 | AI Eng | Always label per TikTok 2025 rule, monitor reach metrics for AI-flagged content | A/B test labeled vs unlabeled (where allowed), adjust style | Open | monthly |
| R-20 | Schedule | Phase 1 exit criteria miss (GMV < $200 / 14d) | 3 | 3 | 9 | Nick Fury | Beauty niche focus, mega-sale alignment, manual review of top 10 video creative | Extend Phase 1 by 2 wk, re-baseline | Open | per-phase |

---

## Risk Heat Map

```
            P1    P2    P3    P4    P5
I5         |     R-01 |R-03 |R-17 |
           |     R-08 |     |     |
           |     R-10 |     |     |
I4         |     R-15 |R-04 |R-02 |
           |     R-16 |R-05 |     |
           |          |R-07 |     |
           |          |R-09 |     |
           |          |R-11 |     |
           |          |R-14 |     |
I3         |          |R-06 |R-18 |
           |     R-12 |R-19 |     |
           |     R-13 |R-20 |     |
I2         |          |     |     |
I1         |          |     |     |
```

**HIGH (Exp ≥ 13)**: R-02 (16), R-03 (15), R-17 (15) — รายงานทุกสัปดาห์
**MEDIUM (Exp 7-12)**: R-01, R-04, R-05, R-07, R-08, R-09, R-10, R-11, R-14, R-15, R-16, R-19, R-20
**LOW (Exp ≤ 6)**: R-06, R-12, R-13, R-18

---

## Linear Integration
- Risk register sync ขึ้น Linear ภายใต้ label `risk` + custom field `exposure`
- ทุก risk = 1 Linear issue (mirror ของ register นี้)
- Weekly status report list HIGH risks ที่เปลี่ยนสถานะ
- Closed risk → archive ใน Linear, mark `Status: Closed` ใน register นี้พร้อม resolution note
