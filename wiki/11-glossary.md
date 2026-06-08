# 11 — Glossary

| Term | ความหมายใน Auto-Affi |
|---|---|
| **Hanky V12** | Last-known-good production baseline จาก run hanky-dry-towel-60s — ทุก run ใหม่ต้องเทียบกับ runbook นี้ ([05](05-hanky-v12-runbook.md)) |
| **Success Scenario Review** | `success_scenario_review.json` — 9-field check เทียบ Hanky V12 ก่อน generation |
| **Cleanroom** | Final video ต้องมี exactly 1 video + 1 audio stream — กัน source audio รั่ว (Gate #4) |
| **Silent B-roll** | Source video ที่ strip audio ออกแล้ว — default ของทุก generated clip |
| **Contact Sheet** | ภาพ grid (3x3) รวมทุก shot — ใช้ตัดสิน dailies ทีละ cell ไม่ใช่จาก vibes |
| **Dailies QC** | การ audit generated clips ทีละ numbered cell: bag/wardrobe/product/location/lighting |
| **Attractive-but-wrong** | Clip สวยแต่ผิด product truth/continuity → ต้อง reject เสมอ ไม่มี "use with note" |
| **Prompt Council** | Gate ที่ ≥3 independent seats ต้อง vote pass ก่อน provider call — drafter ห้าม self-approve |
| **Prompt Density** | คะแนนความละเอียด prompt — ขั้นต่ำ affiliate 85 / premium 90 / regulated 95 |
| **Continuity Token** | Token บังคับทุก scene: `WORLD= \| CHAR= \| WARD= \| LOC= \| CAM= \| TIME= \| PROP= \| PRODUCT=` — drift โดยไม่อธิบาย = blocked |
| **Character Passport** | Locked character identity (age/hair/wardrobe/hands/expression range) ใช้ข้ามทุก scene |
| **Location Map** | World map ของ run: zones, camera access, wet/dry, surfaces, lighting |
| **Camera Atlas** | Named camera families ที่ register ก่อน production (10–18 families) |
| **Product State Machine** | สถานะ product ต่อ scene (เช่น folded → unfolded → packed) กัน prop drift |
| **Reality Mode** | ประกาศโลกของ story: realistic / stylized / fantasy / surreal — fantasy ต้องมี written rule |
| **Brand Remove Test** | ถ้าเอาสินค้าออกแล้ว plot ยังเดินได้ = story fail (สินค้าต้อง structurally necessary) |
| **Memory Frame** | ภาพเดียวที่คนดูจำได้หลังดูจบ — ทุก ad ต้องมี (Emotion Standard) |
| **5 Emotion Pillars** | ตื่นตา/ตื่นเต้น/น่าสนใจ/สนุก/กินใจ — ทุก pillar ≥4.0, avg ≥4.3 |
| **Ethics Color** | green = ไปได้ / amber = human review / red = ห้าม product mapping (death/violence/minors) |
| **Review-ready ≠ Publish-ready** | มี final MP4 ดูได้ ≠ โพสต์ได้ — publish ต้องผ่าน affiliate/rights/disclosure/human approval |
| **Speed Guard** | Thai VO speed: warn >1.08x, hard reject >1.15x — ห้ามเร่งเสียงแก้ script ยาว |
| **HyperFrames** | Deterministic HTML/GSAP compositor สำหรับ Thai captions (Sarabun font) — แก้ปัญหา Thai combining marks |
| **EDL** | Edit Decision List — Post owns timeline, ต้องมีก่อน assembly |
| **subId Attribution** | Affiliate tracking 5 levels: platform/account/product/campaign/variant |
| **Workflow OS** | Packet architecture: `state.json` (blockers) / `verification.json` (machine proof) / `approval_packet.json` (human) / `publish_packet.json` (publish gates) |
| **Run** | 1 production = 1 โฟลเดอร์ใน `runs/` + 1 แถวใน `run_registry.csv` |
| **User-caught failure** | ความผิดพลาดที่ user จับได้ (ไม่ใช่ machine) — ต้อง promote เป็น machine-check ก่อน run ถัดไป |
| **Last Known Good** | หลักการ: ทำตาม path ที่พิสูจน์แล้วสำเร็จล่าสุด deviate ได้เฉพาะมี approved reason |
| **Fail-closed** | ถ้า gate/ข้อมูลไม่ครบ = หยุด ไม่ใช่เดาแล้วไปต่อ |

---
[← Ops Guide](10-ops-guide.md) | [HOME](HOME.md)
