# 10 — Ops Guide: วิธีสั่งงาน Production

> สรุปจาก [`README.md`](../README.md) — copy prompt เหล่านี้ไปใช้ได้ตรง ๆ

## หลักการสั้นที่สุด

ทุกคลิปสินค้าใหม่เริ่มด้วย:

```text
ใช้ $auto-affi-new-product-clip
```

Skill นี้คือ front door → บังคับเข้า `$auto-affi-one-shot-workflow` — **อย่าสั่งแค่ `Go`/`Next` ถ้ายังไม่ approve storyboard/contact sheet**

## Prompt Templates

### 1. เริ่มคลิปใหม่ — ให้ Marketing เลือกสินค้า

```text
ใช้ $auto-affi-new-product-clip
เริ่ม production คลิปสินค้าใหม่ 60 วินาที
ให้ทีม marketing เลือกสินค้าใหม่ 1 ตัว
หลังเลือกสินค้าแล้ว ให้ search Google/web/image เพื่อเก็บข้อมูลและรูปอ้างอิงให้มากพอ
สรุป research เพื่อใช้สร้าง prompt image และ video
ใช้ Nano Banana Pro สำหรับภาพ/reference/keyframe/storyboard เท่านั้น
ใช้ Seedance 2.0 สำหรับ video เท่านั้น
ทำ storyboard/contact sheet ให้ดูก่อน ห้ามยิง provider จนกว่าฉัน approve
```

### 2. เริ่มจาก Shopee/affiliate URL

```text
ใช้ $auto-affi-new-product-clip
ทำคลิปสินค้าใหม่ 60 วินาทีจาก URL นี้: <url>
ต้อง research Google/web/image ก่อน prompt
ตรวจ product truth, claim ledger, rights, และ visual references
ใช้ Nano Banana Pro สำหรับภาพ/reference/keyframe/storyboard เท่านั้น
ใช้ Seedance 2.0 สำหรับ video เท่านั้น
โชว์ storyboard/contact sheet ให้ฉัน approve ก่อนจ่ายเครดิต
```

### 3. Approve หลังเห็น storyboard

```text
Approve storyboard/contact sheet นี้
เริ่ม Seedance 2.0 motion test 3 ช็อตสำคัญเท่านั้น
หลังเสร็จให้ทำ numbered contact sheet/dailies QC
ถ้ามี continuity, physics, product, prop, location หรือ caption/voice issue ให้ reject และ regenerate เฉพาะช็อตที่พัง
```

> Pattern สำคัญ: **motion test 3 ช็อตก่อน** ไม่ใช่ full batch — ประหยัดเครดิตถ้า direction พัง

### 4. Resume งานค้าง

```text
ใช้ $auto-affi-new-product-clip
resume run <run-id>
ตรวจว่า deep_product_research, visual_reference_board, research_synthesis,
success_scenario_review และ pre_generation_user_review ผ่านครบหรือยัง
ถ้ายังไม่ครบ ห้ามยิง provider
```

## Environment & Keys

- Key ทุกตัวอยู่ใน `.env` — **ห้าม paste secret ลง README/prompt/log/artifact**
- Key หาย/โหลดไม่ได้ = **หยุด workflow และรายงานว่า key ตัวไหนขาด** โดยไม่ยิง provider
- Expected vars: `HF_API_KEY`, `HF_API_ID`, `HF_API_SECRET`, `HF_KEY`, `KIE_API_KEY`

## Checklist ก่อน Approve Spend (สำหรับ Human PM)

1. เห็น 3x3 storyboard/contact sheet จริง (ไม่ใช่คำอธิบาย)
2. ภาพทั้งหมดเป็น Nano Banana Pro (ไม่มี scripted schematic)
3. `success_scenario_review.json` ครบ 9 fields
4. Prompt Council ผ่าน (ไม่ใช่ drafter approve ตัวเอง)
5. รู้ค่าใช้จ่าย credit โดยประมาณก่อนกด approve
6. Motion test 3 ช็อตก่อน full batch

## Checklist ก่อน Publish (ยังไม่มี run ไหนผ่านครบ)

1. Human approval บันทึกแล้ว
2. Affiliate URL + subIds (5 levels) ใส่แล้ว ← **blocker ปัจจุบันของทุก run**
3. Live price/SKU recheck
4. Caption มี `#โฆษณา #affiliate` + AI label
5. Rights tracker ครบ, cleanroom audit ผ่าน

---
[← Scripts](09-scripts-reports.md) | [HOME](HOME.md) | [Glossary →](11-glossary.md)
