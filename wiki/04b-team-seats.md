# 04b — Team Seats & Decision Authority

> Auto-Affi ทำงานเป็น multi-agent studio — แต่ละ seat มี contract ชัดเจน ที่มา: [`README.md`](../README.md) + [Talent & Partner Principle](../docs/principles/2026-06-04-talent-partner-principle.md) + [Autonomous Creative Decision System](../docs/principles/2026-06-06-company-autonomous-creative-decision-system.md)

## Production Seats (14 ตำแหน่ง)

| Seat | รับผิดชอบ |
|---|---|
| **Marketing** | เลือกสินค้า 1 ตัว, buyer angle, hook, CTA, reality mode |
| **Product Research / Claims** | Product truth, price/SKU, claim ledger, block unsupported claims |
| **Visual Research** | Google/web/image research, reference metadata, visual hazards, prompt implications |
| **Location / Environment Design** | World map, wet/dry zones, surfaces, lighting, product-use zones, realistic transitions |
| **Shooting Production** | Shot contract, one action per shot, camera, movement, continuity anchors |
| **Story Audit** | Narrative logic, product necessity, buyer memory image, no caption-dependent story |
| **Continuity / Storyboard Audit** | Wardrobe, prop, bag, product, location, environment, screen direction |
| **Story Physics / Logic** | Gravity, scale, weight, water, contact/friction, cause/effect, fantasy rules |
| **Prompt Council** | Independent pass/revise/block ก่อน provider call — **ห้าม self-approve** |
| **Provider Ops** | `.env` readiness, route decision, model locks, local download, cost estimate |
| **Dailies QC** | Numbered contact sheet audit, targeted regeneration, **reject attractive-but-wrong** |
| **Compliance / Publish** | Rights, disclosure, affiliate URL, price/SKU recheck, human publish approval |
| **Learning** | Scorecards, failure taxonomy, promote user-caught issues เป็น workflow rules |

## Intel Desks (always-on, 9 desks)

News Desk · Social Radar · Entertainment · Marketing Collection · Ethics · Product Research · Product Mapping · Claims/Compliance · Performance — ดู [Always-On Viral Intelligence Principle](../docs/principles/2026-06-04-always-on-viral-intelligence-principle.md)

## Prompt Council Gate

- ต้องมี **≥3 independent seats vote "pass"** — drafter ห้ามโหวตให้ตัวเอง
- Mandatory seats สำหรับ multi-shot: Marketing, Product Research/Claims, Shooting Production, Location/Environment, Story Audit, Continuity Audit, Story Physics/Logic, Post/Rights/Compliance
- Decision values: `pass_for_generation` / `pass_with_publish_block` / `revise` / `block`
- Density score ขั้นต่ำ: affiliate 85 / premium 90 / regulated 95

## Autonomous Vote (8 seats — ตั้งแต่ Yomihome run)

User delegate การตัดสินใจ creative ให้ทีม vote เองได้ (หลัง storyboard route visible):

ECD · Film Director · DOP · Production Designer · **Prompt Continuity Architect** (มี veto "hold provider spend") · Product Truth/Claims · Performance Marketing · Thai Copy/VO Lead

Output ต้อง structured: `keep | kill | regenerate | hold` + emotion_scores + critical_locks + next_action

**Veto seats** ที่ kill shot "beautiful but wrong" ได้: Prompt Continuity Architect, Location Map Supervisor, Camera Grammar Lead, Product Truth/Claims

## Lean Core Roles (องค์กรจริง 8 ตำแหน่ง)

EP/Founder · Creative Strategy · AI Film Director · Producer · Cinematography/Prompt Director · Post Supervisor · Business Affairs · Growth/Analytics — **"Own the brief, strategy, taste, rights, approval, and learning loop. Partner for specialized craft."**

Review rituals: Prompt council (ทุก generation) / Dailies (ทุก generation) / Postmortem (per run) / Partner review (monthly)

---
[← Data Registry](04a-data-registry.md) | [HOME](HOME.md) | [Hanky V12 Runbook →](05-hanky-v12-runbook.md)
