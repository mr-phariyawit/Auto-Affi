---
name: aegis-thai-tldr
description: "Translate any agent output / report / handoff / human-queue into a Thai DECISION-FIRST TLDR — read once and instantly know what YOU must decide or do. Use at the end of long/technical responses, on /aegis-status, or when the human says สรุป / ต้องทำอะไร / ขอ TLDR / อ่านไม่ไหว."
profile: minimal
triggers:
  en: ["thai tldr", "tldr in thai", "what do i decide", "what do i need to do", "summarize in thai", "decision tldr"]
  th: ["สรุปไทย", "แปลไทย", "ขอ tldr", "tldr", "สรุปสั้น", "สรุปให้หน่อย", "ต้องตัดสินใจอะไร", "ต้องทำอะไร", "อ่านทีเดียวเข้าใจ", "อ่านไม่ไหว"]
reads:
  - "(content to distill — the current/last agent output, or .aegis/brain/human-queue.md)"
writes: []
wires: []
tests: []
supersedes: []
---

## Quick Reference
แปลผลลัพธ์ของ agent (ที่มักยาว / เทคนิค / ปนอังกฤษ) → **TLDR ภาษาไทยที่เอา "การตัดสินใจ" ขึ้นก่อน**
อ่านครั้งเดียวรู้ทันทีว่า *คุณ (มนุษย์)* ต้องตัดสินใจหรือลงมืออะไร — ไม่ต้องไล่อ่านทั้งรายงาน

แกน: **decision-first · ≤5 บรรทัด/เรื่อง · ไทยล้วน** (ยกเว้น command / path / flag / ชื่อไฟล์ → คงไว้ ห้ามแปล)

## Output template (ใช้ตายตัวทุกครั้ง)
```
━━ TLDR (ไทย) ━━
🎯 ต้องทำ:   <สิ่งที่มนุษย์ต้องทำ/ตัดสินใจ — 1 บรรทัด ประโยคคำสั่ง — หรือ "ไม่มี ✅">
⏱️ ด่วน:     <ทำเลย / รอได้ / กำลังบล็อกอะไรอยู่>
📌 เพราะ:    <เหตุผล 1 บรรทัด ภาษาคนทั่วไป>
🔢 ทางเลือก:  1) …  2) …          ← ใส่เฉพาะเมื่อเป็น "ตัวเลือกจริง"; ไม่มีให้ลบบรรทัดนี้
👉 คำสั่ง:    <command / path ที่ก๊อปวางได้เลย ถ้ามี>
```

## Rules (สิ่งที่ทำให้ TLDR ดีจริง)
1. **เอา action/decision ขึ้นก่อนเสมอ** — ห้ามเล่า background นำ
2. **ถ้าไม่มีอะไรต้องตัดสินใจ → บอกตรง ๆ**: "ไม่ต้องทำอะไร — แค่รับทราบ (FYI)" เพื่อไม่ให้เสียเวลาค้นหา
3. **แยกประเภทให้ชัด**: 「ตัดสินใจ」(เลือก A/B) · 「ลงมือ」(รัน 1 command) · 「FYI」(ไม่ต้องทำ)
4. **คง command / path / ชื่อไฟล์ / flag เป็นอังกฤษ** — แปลคำอธิบาย ไม่แปลโค้ด
5. **≤5 บรรทัดต่อเรื่อง** — หลายเรื่องให้ list เป็นข้อ เรื่องละ 1–2 บรรทัด เรียงตามความด่วน
6. **ซื่อสัตย์**: blocked = บอก blocked; ยังไม่ verified = อย่าเขียนว่าเสร็จ (กฎ verified-vs-produced)
7. **ผูกกับ 4 หมวด MBP**: ถ้าเรื่องนั้นไม่เข้า Identity / Irreversible / External / Approval-gate → มนุษย์ "ไม่น่าต้องตัดสินใจ" (agent ควรทำเอง) → จัดเป็น FYI

## When to use
- ปิดท้ายรายงานยาว ๆ ของ agent (แนบ TLDR ท้ายสุด)
- เมื่อมนุษย์พิมพ์: "สรุป", "ต้องทำอะไร", "ขอ TLDR", "อ่านไม่ไหว"
- ย่อ `.aegis/brain/human-queue.md` ทั้งคิว → เหลือ "ตอนนี้ต้องทำอะไรบ้าง"
- ต่อท้าย `/aegis-status` และ `/aegis-handoff`

## Worked example
รายงานยาว → "...config-protection guard blocked pyproject.toml ... queued ... cp _aegis-output/specs/AFFI-S1-01-build-config-proposed.txt pyproject.toml ..."
```
━━ TLDR (ไทย) ━━
🎯 ต้องทำ:   วางไฟล์ build config (agent โดน guard บล็อก เขียนเองไม่ได้)
⏱️ ด่วน:     ทำเลย — บล็อก Sprint-1 ทั้งหมด (ทุก task รอ test runner)
📌 เพราะ:    AEGIS กัน agent แตะ quality config; ไฟล์นี้สร้างใหม่ + เข้มขึ้น วางได้ปลอดภัย
👉 คำสั่ง:    cp _aegis-output/specs/AFFI-S1-01-build-config-proposed.txt pyproject.toml
```

## Continuation (MBP / Golden Rule #7)
ออก TLDR แล้ว **ทำงานต่อตาม command-chain ทันที — ห้ามจบด้วยคำถาม/เมนู** เว้นแต่ติด 1 ใน 4 หมวด MBP
(ซึ่ง TLDR จะ surface บรรทัด 🎯 ให้เห็นชัดอยู่แล้ว) อยากให้ TLDR ออกอัตโนมัติทุก response →
ต้อง wire เข้า on-stop hook (เป็น config = ต้องให้มนุษย์ตั้ง ไม่ใช่ agent)
