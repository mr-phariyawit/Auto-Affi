# 05 — Hanky V12 Success Scenario Runbook (Last Known Good)

> **นี่คือ baseline ศักดิ์สิทธิ์ของบริษัท** — production path ที่พิสูจน์แล้วว่าได้ผล ทุก run ใหม่ต้องสร้าง `success_scenario_review.json` เทียบกับ runbook นี้ก่อน validate-generation ถ้า deviate ต้องมี `status: "approved"` ไม่งั้น generation ถูก block
>
> Source: [`docs/principles/2026-06-06-hanky-v12-success-scenario-runbook.md`](../docs/principles/2026-06-06-hanky-v12-success-scenario-runbook.md)
> Baseline file: `runs/2026-06-04-hanky-dry-towel-60s-seedance-marketing-test/outputs/hanky_house_microfiber_towel_60s_hyperframe_kie_elevenlabs_v12_brittney.mp4`

## 8 ขั้นตอนสู่ความสำเร็จ

### 1. Simple Product Story
หนึ่งปัญหา (rainy commute) · หนึ่ง product behavior · หนึ่ง proof loop (hands + fabric + droplets + pack-away) · หนึ่ง CTA — story ที่อ่านออกจาก contact sheet โดยไม่ต้องพึ่ง caption

### 1b. Deep Research ก่อน Prompt
หลัง Marketing เลือกสินค้า → search broadly: marketplace facts, similar listings, visual refs, user-review language, competitor visuals, seasonal context → แปลงเป็น prompt constraints ก่อนเขียน Nano Banana Pro/Seedance prompts


### 3. Dailies ตัดสินจาก Contact Sheet ไม่ใช่ Vibes
Numbered contact sheet + `dailies_qc.json` — audit bag/wardrobe/product/location/lighting ทีละ cell

### 4. Reject Attractive-But-Wrong
Scene 2 (wardrobe drift), Scene 5 (identity drift), Scene 11 (bag mismatch) ถูก regenerate ทั้งหมด — **ไม่มี "use with note" สำหรับ identity/product truth failures**

### 5. Post-Production Deterministic
Source video strip เป็น silent B-roll → HyperFrames จัดการ Thai captions — ห้ามมี model-generated Thai text ใน footage

### 6. Thai Voice Route Specific & Cached

### 7. Caption/Voice Sync Machine-Verified
`metrics/caption_voice_sync_v12_brittney.json` ต้อง `ok: true` — caption count = segment count, text exact match — ใช้ [`scripts/validate_caption_voice_sync.py`](09-scripts-reports.md)

### 8. Review-Ready ≠ Publish-Ready
Final MP4 reviewable แต่ publish blocked จนกว่า: affiliate URL + live price/SKU + rights + human approval

## success_scenario_review.json — 9 Required Fields

ทุก run ใหม่ต้อง check ครบ:

1. `deep_research_before_prompting`
2. `simple_story`
3. `kie_services_only_visual_video`
4. `contact_sheet_before_batch`
5. `numbered_dailies_anchor_audit`
6. `targeted_regeneration`
7. `kie_elevenlabs_v3_brittney_or_approved_voice`
8. `caption_voice_exact_match_before_final`
9. `publish_blocked_until_human_affiliate_price_rights`

## Gates ที่เพิ่มหลัง Rhodey Defect (2026-06-05)


## ทำไม V12 ถึงเป็น baseline — บทเรียน 12 versions

Hanky run วิ่งผ่าน V7→V12 (ดูเต็มใน [runs/2026-06-04-hanky-dry-towel-60s.md](runs/2026-06-04-hanky-dry-towel-60s.md)):

| Version | บทเรียน |
|---|---|
| V7 | Edge TTS fallback — เสียงไม่ผ่าน |
| V8 | JaiTTS local audition — ไม่ผ่าน |
| V9 | Bella stability 0.5 — **"too sleepy"** (user caught) |
| V10 | Bella stability 0.0 + script ใหม่ — ดีขึ้นแต่ยังไม่สุด |
| V11 | Voice audition 9 เสียงพร้อม labeled comparison video |
| **V12** | **Brittney + stability 0.0 — user selected → กลายเป็น company standard** |


---
[← Team Seats](04b-team-seats.md) | [HOME](HOME.md) | [Principles →](06-principles.md)
