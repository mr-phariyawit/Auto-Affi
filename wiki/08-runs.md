# 08 — Production Runs

เอกสารหน้านี้สรุปข้อมูลโฟลเดอร์ `runs/` ซึ่งเก็บข้อมูลการผลิตวิดีโอแต่ละรอบ (Production Runs) ปัจจุบันมีทั้งหมด 11 runs ในระบบ

> **ทุก run มีหน้า detail พร้อม lessons learned ฉบับเต็ม** ในโฟลเดอร์ [`wiki/runs/`](runs/):
>
> | Run | Detail Page |
> |---|---|
> | GEESO Mini Umbrella | [runs/2026-06-03-geeso-mini-umbrella.md](runs/2026-06-03-geeso-mini-umbrella.md) |
> | Silicone Shoe Covers | [runs/2026-06-03-silicone-shoe-covers.md](runs/2026-06-03-silicone-shoe-covers.md) |
> | Hanky Dry Towel (brief) | [runs/2026-06-04-hanky-dry-towel.md](runs/2026-06-04-hanky-dry-towel.md) |
> | Hanky 60s ⭐ V12 baseline | [runs/2026-06-04-hanky-dry-towel-60s.md](runs/2026-06-04-hanky-dry-towel-60s.md) |
> | iFilm Pouch (simple test) | [runs/2026-06-04-ifilm-phone-pouch-simple-seedance-test.md](runs/2026-06-04-ifilm-phone-pouch-simple-seedance-test.md) |
> | iFilm Pouch (full, approved) | [runs/2026-06-04-ifilm-waterproof-phone-pouch.md](runs/2026-06-04-ifilm-waterproof-phone-pouch.md) |
> | Workflow OS Smoke Test | [runs/2026-06-04-workflow-os-smoke-test-shoe-covers.md](runs/2026-06-04-workflow-os-smoke-test-shoe-covers.md) |
> | Rhodey Rain Cover (defect) | [runs/2026-06-05-rhodey-backpack-rain-cover.md](runs/2026-06-05-rhodey-backpack-rain-cover.md) |
> | EUCERIN Premium Intake | [runs/2026-06-06-eveandboy-eucerin-premium-intake.md](runs/2026-06-06-eveandboy-eucerin-premium-intake.md) |
> | Yomihome Tape ⭐ V5.1 | [runs/2026-06-06-yomihome-screen-repair-tape.md](runs/2026-06-06-yomihome-screen-repair-tape.md) |
> | Umbrella Way (short film) | [runs/umbrella-way-20260604.md](runs/umbrella-way-20260604.md) |

## รายการ Runs ในปัจจุบัน

โฟลเดอร์รันในระบบเรียงตามลำดับเวลา:

### 1. `2026-06-03-geeso-mini-umbrella`
- **Product:** GEESO UPF50+ ร่มพกพาขนาดเล็ก 225g Mini Pocket Umbrella
- **Objective:** 15s Thai UGC-style ad clip (อิงจากสัญญาณพายุฤดูฝน)
- **Status:** `ready_for_human_review_v4_scene_sync` (รออนุมัติ; วางแผนจะทำ 30s v5 ต่อ)
- **Key Asset:** [geeso-mini-umbrella-review-v4-scene-sync.mp4](file:///Users/phariyawit.jiap/Documents/Auto-Affi/runs/2026-06-03-geeso-mini-umbrella/geeso-mini-umbrella-review-v4-scene-sync.mp4)

### 2. `2026-06-03-silicone-shoe-covers` (Sprint Handoff 2026-06-03)
- **Product:** ซิลิโคนหุ้มรองเท้า ถุงคลุมรองเท้ากันฝน waterproof shoe covers
- **Objective:** 30s commercial master, 9:16 Thai affiliate review
- **Status:** `ready_for_human_review` (รอ Human review และการใส่ Disclosure/Platform ก่อน Publish)

### 3. `2026-06-04-hanky-dry-towel` (Last-Known-Good / [Hanky V12](05-hanky-v12-runbook.md))
- **Product:** Hanky House ผ้าเช็ดตัวไมโครไฟเบอร์ แห้งไว พกพานง่าย
- **Objective:** "The Dry Escape" Hollywood-style ad, 15s transformation
- **Status:** เพิ่งผ่านการทำ Creative Brief ยังไม่เข้าสู่กระบวนการ Generation
- **Key Asset:** [creative_brief.md](file:///Users/phariyawit.jiap/Documents/Auto-Affi/runs/2026-06-04-hanky-dry-towel/creative_brief.md)

### 4. `2026-06-04-hanky-dry-towel-60s-seedance-marketing-test`
- **Product:** Hanky House ผ้าเช็ดตัวไมโครไฟเบอร์ แห้งไว พกพานง่าย
- **Objective:** 60s marketing test / 30s affiliate master test
- **Status:** `rough_cut_v7_hyperframe_voice_caption_ready_publish_blocked` (รออนุมัติ; ติด Publish Block ขาด Affiliate URL และ Live SKU check)
- **Key Asset:** [hanky_house_microfiber_towel_60s_hyperframe_voice_caption_v7.mp4](file:///Users/phariyawit.jiap/Documents/Auto-Affi/runs/2026-06-04-hanky-dry-towel-60s-seedance-marketing-test/outputs/hanky_house_microfiber_towel_60s_hyperframe_voice_caption_v7.mp4)

### 5. `2026-06-04-ifilm-phone-pouch-simple-seedance-test`
- **Product:** [Official] iFilm ซองกันน้ำโทรศัพท์มือถือ IPX8
- **Objective:** 30s review / simple seedance test
- **Status:** `ready_for_human_review` (ติด Blocked เนื่องจาก Product reference เห็นโลโก้/มือถือชัดเกินไปแล้วติดไปในคลิปเจน)
- **Key Asset:** [seedance_only_simple_phone_pouch_30s_silent.mp4](file:///Users/phariyawit.jiap/Documents/Auto-Affi/runs/2026-06-04-ifilm-phone-pouch-simple-seedance-test/outputs/seedance_only_simple_phone_pouch_30s_silent.mp4)

### 6. `2026-06-04-ifilm-waterproof-phone-pouch`
- **Product:** [Official] iFilm ซองกันน้ำโทรศัพท์มือถือ IPX8
- **Objective:** 30s commercial master / review
- **Status:** `approved_for_dispatch_prep_blocked_affiliate` (อนุมัติเตรียม Publish แต่ติด Blocked รอตั้งค่า Affiliate และเช็กราคาซ้ำ)
- **Key Asset:** [ifilm-phone-pouch-30s-review-edge-draft.mp4](file:///Users/phariyawit.jiap/Documents/Auto-Affi/runs/2026-06-04-ifilm-waterproof-phone-pouch/variants/v001-preproduction/ifilm-phone-pouch-30s-review-edge-draft.mp4)

### 7. `2026-06-04-workflow-os-smoke-test-shoe-covers`
- **Product:** ซิลิโคนหุ้มรองเท้า ถุงคลุมรองเท้ากันฝน waterproof shoe covers 
- **Objective:** Smoke test ตรวจสอบ Workflow OS (ไม่มีการเจนเพิ่มจาก External)
- **Status:** `ready_for_review_publish_blocked` (ยืนยันว่า Workflow OS ทำงานได้ถูกต้องในการบล็อก Publish)
- **Key Asset:** (Recycles asset จากรัน `2026-06-03-silicone-shoe-covers`)

### 8. `2026-06-05-rhodey-backpack-rain-cover-30s-production`
- **Product:** Rhodey Rain Cover Waterproof Backpack 30-40L
- **Objective:** 30s production (thai_affiliate_30s_master)
- **Status:** `blocked_env_missing` (Generation ถูกบล็อก / รอ Human Review; ปัจจุบันมีแค่ข้อมูล Previsualization)
- **Key Asset:** [storyboard_grid.json](file:///Users/phariyawit.jiap/Documents/Auto-Affi/runs/2026-06-05-rhodey-backpack-rain-cover-30s-production/storyboard_grid.json)

### 9. `2026-06-06-eveandboy-shopee-25362750043-30s-premium-intake`
- **Product:** EUCERIN - Spotless Brightening Skin Tone Perfecting Body Lotion
- **Objective:** Premium 30s Thai ad สำหรับ Shopee
- **Status:** `creative_v3_preflight_ready_pending_approval` (ถูกบล็อกรออนุมัติ Storyboard Contact Sheet จากผู้ใช้)
- **Key Asset:** [pre_generation_storyboard_contact_sheet_v3.png](file:///Users/phariyawit.jiap/Documents/Auto-Affi/runs/2026-06-06-eveandboy-shopee-25362750043-30s-premium-intake/review_frames/pre_generation_storyboard_contact_sheet_v3.png)

### 10. `2026-06-06-yomihome-screen-repair-tape-60s-production`
- **Product:** Yomihome Screen Repair Tape (yomihome เทปซ่อมมุ้งลวด)
- **Objective:** 60s production (thai_affiliate_60s_master) - เน้นความสวยงาม น่าตื่นเต้น น่าสนใจ
- **Status:** `pre_generation_review_ready` (ถูกบล็อกรออนุมัติภาพ V5.1 Seedance motion test จากผู้ใช้)
- **Key Asset:** [hollywood_v5_1_provider_approval_gate_board.png](file:///Users/phariyawit.jiap/Documents/Auto-Affi/runs/2026-06-06-yomihome-screen-repair-tape-60s-production/review_frames/hollywood_v5_1_provider_approval_gate_board.png)

### 11. `umbrella-way-20260604-161554`
- **Product:** "The Umbrella That Knows The Way" (Short film)
- **Objective:** ทำหนังสั้น 3 องก์ (3-minute) เกี่ยวกับร่มสีแดง
- **Status:** ผ่านการ QC ตัวเต็ม 3 นาทีแบบหยาบแล้ว กำลังเข้าสู่การทำ Hero pass (แก้ช็อตซูมที่ยังอ่อน) และใส่ Score/SFX
- **Key Asset:** [full_rough_3min_silent.mp4](file:///Users/phariyawit.jiap/Documents/Auto-Affi/runs/umbrella-way-20260604-161554/outputs/full_rough_3min_silent.mp4)

> **สถานะการ Publish ปัจจุบัน:** ทุก run ยังคงมีสถานะ publish-blocked เนื่องจากต้องรอใส่ affiliate URL และ subIds ซึ่งเป็น blocker ขั้นสุดท้ายของกระบวนการ publish ตาม Compliance Gate

## Workflow Evolution Timeline (06-03 → 06-06)

4 วันที่ระบบโตจาก production chaos → systematic creative factory — แต่ละ run สร้างกฎใหม่:

| วัน | Run | กฎ/ระบบที่เกิด |
|---|---|---|
| 06-04 | Umbrella Way | **Seedance 2.0-only lock** (mixed model = look variance) · previsualization gates (character sheet, storyboard grid, dailies QC) |
| 06-04 | iFilm ×2 | Full previz scaffold แรก · clean no-text reference rule (logo poisoning) · **Prompt Council gate** · `brain_activity` ≤16s · **run แรกที่ user approve** |
| 06-04 | Workflow OS Smoke | **"Review-ready ≠ publish-ready"** เป็น formal rule · packet separation พิสูจน์แล้ว |
| 06-05 | Rhodey (defect) | **Nano Banana Pro-only images** + **human-visible storyboard gate** + `pre_generation_user_review.json` (user จับ scripted schematic) |
| 06-06 | EUCERIN | Premium creative standard แรก · `company_creative_prompt_system_v1` · prompt lock bible/location map/camera atlas ใช้จริง |
| 06-06 | Yomihome V1→V5.1 | **Film world lock** (V4: passport/state machine/atlas) · **5-emotion strategy** (V5) · **autonomous team vote** + Continuity Architect veto |


## โครงสร้างทั่วไปของโฟลเดอร์ Run

แต่ละโฟลเดอร์ใน `runs/` จะเก็บ Artifacts สำคัญตามแต่ละด่านของ Workflow:
- `deep_product_research.json`, `research_synthesis.md`
- `success_scenario_review.json`
- `storyboard_grid.json`, `shot_cards.json`
- ไฟล์ Video/Audio จาก Seedance 2.0 และ ElevenLabs
- `dailies_qc.json`, `edit_decision_list.json`
- `approval_packet.json` (และข้อมูลการอนุมัติก่อน Publish)

---
[← Research](07-research.md) | [HOME](HOME.md) | [Scripts & Reports →](09-scripts-reports.md)
