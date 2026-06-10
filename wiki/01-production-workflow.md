# 01 — Production Workflow

> Workflow มี 2 ระดับ: **Quick-start prompt** (สั่งงานถูกทางใน 1 ข้อความ) และ **Full production orchestration** (audit ว่างานเดินครบจริง) — งาน production จริงต้องยึด full flow เสมอ

**Front door:** ทุกงานคลิปสินค้าใหม่เริ่มด้วย `$auto-affi-new-product-clip` → `$auto-affi-one-shot-workflow` (ดู prompt templates ใน [10-ops-guide.md](10-ops-guide.md))

## Full Production Flow

Flow หลักจาก [`README.md`](../README.md) — ทุก node คือ gate ที่ต้องผ่านตามลำดับ:

### Phase 1: Signal → Product (Intel)

```
Viral/News/Social Signals
  → Ethics & Product-Mapping Gate (red → Human Review Inbox)
  → Marketing Collection → Marketing เลือกสินค้า 1 ตัวเท่านั้น
  → Deep Google/Product/Market Research
  → deep_product_research.json + visual_reference_board.json + research_synthesis.md
  → Research Dense Enough? → Product Truth Pass?
  → Product Candidate CSV → Run Folder + Creative Brief
```

### Phase 2: Pre-Production (ห้ามข้าม — 14 gates ก่อน spend)

```
Last-Known-Good Success Scenario Review (Hanky V12 runbook — ดู 05-hanky-v12-runbook.md)
  → Product Truth + Claim Ledger + Rights Tracker + AI Usage Log
  → Commercial Safety Pass?
  → Creative Strategy + Treatment + Look Bible + Thai VO Script
  → Location/Environment Design → Realistic World Pass?
  → Character Sheet + Continuity Bible
  → Storyboard Grid + Shot Cards
  → Story Audit Pass? → Continuity Audit Pass? → Story Physics & Logic Pass?
  → Env/Secrets Preflight (.env keys present — ไม่ print ค่า)
  → Route Decision → Model Lock Check (Seedance 2.0 / Nano Banana Pro เท่านั้น)
  → Nano Banana Pro Image/Keyframe Gate
  → Prompt Council (independent vote — ห้าม self-approve)
  → Human-Visible Storyboard/Contact Sheet → user approve การ spend credit
  → Generation Preflight Validator (generation_allowed: true)
```

### Phase 3: Generation → Post

```
Seedance 2.0 Visual Generation
  → Download Source Media ทันที (CDN retention สั้น)
  → Strip Source Audio (silent B-roll เสมอ)
  → Dailies QC + Numbered Contact Sheet (ตัดสินทีละ cell ไม่ใช่จาก vibes)
  → reject/regenerate เฉพาะช็อตที่พัง → Edit Decision List
  → HyperFrames Post (Thai caption + Sarabun font)
  → Caption/Voice Exact-Match Gate (machine-verified)
  → Final Render → Audio Cleanroom Audit (1 video + 1 audio stream)
```

### Phase 4: Approval → Publish → Learning

```
Virality Predictor + Performance Snapshot
  → Approval Packet
  → Human Approval + Publish Gates? (affiliate URL, live price/SKU, rights, disclosure)
  → pass: Publish Dispatch | block: Publish Blocked (review-ready ≠ publish-ready)
  → Learning Log + Scorecards + Failure Taxonomy
  → Run Retrospective (successes / failures / user-caught issues)
  → New Workflow Rule Needed? → Upgrade Gates/Templates/Skills/Scripts
  → Archive Run With Evidence
```

> Mermaid diagram ฉบับเต็ม (ทุก decision branch) อยู่ใน [`README.md`](../README.md) section "Full Production Flow" และ [`docs/principles/2026-06-04-main-flow-mermaid-review.md`](../docs/principles/2026-06-04-main-flow-mermaid-review.md)

## กฎเหล็กที่ห้ามลืม

1. **อย่าสั่งแค่ `Go`/`Next`** ถ้ายังไม่เห็นและ approve storyboard/contact sheet — workflow ต้องหยุดก่อน spend เครดิตทุกครั้ง
2. **ห้าม fallback model เอง** — Seedance 2.0 ใช้ไม่ได้ = หยุดและรายงาน ไม่ใช่เปลี่ยน model
3. **Key หาย = หยุด** — ห้ามยิง provider ถ้า `.env` ไม่ครบ รายงานว่า key ตัวไหนขาด
4. **Review-ready ≠ publish-ready** — final MP4 ดูได้ แต่ publish ต้องผ่าน affiliate URL + live price/SKU + rights + human approval
5. **ทุก run จบด้วย learning** — ห้าม archive run ที่ไม่มี learning log

## Required Artifacts ต่อ run (สำคัญ)

| Stage | Artifact |
|---|---|
| Research | `deep_product_research.json`, `visual_reference_board.json`, `research_synthesis.md` |
| Baseline | `success_scenario_review.json` (9 fields ตาม Hanky V12) |
| Truth/Rights | `product_truth`, `claim_ledger.json`, `rights_tracker`, `ai_usage_log.json` |
| Previz | `character_sheet.json`, `continuity_bible.json`, `storyboard_grid`, `shot_cards`, `story_audit`, `story_physics_review.json`, `continuity_audit.json` |
| Routing | `route_decision.json` |
| Council | `prompt_council_review` (decision: pass) |
| Approval | `pre_generation_user_review.json` (explicit approve + credit acknowledgement) |
| QC | `dailies_qc.json`, numbered contact sheet, `edit_decision_list.json` |
| Post | caption/voice sync report (`ok: true`), cleanroom verification |
| Closeout | `approval_packet.json`, learning log, failure taxonomy, retrospective |

---
[← Overview](00-overview.md) | [HOME](HOME.md) | [Compliance Gates →](02-compliance-gates.md)
