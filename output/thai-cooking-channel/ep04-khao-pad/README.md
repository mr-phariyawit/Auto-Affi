# EP04 — ข้าวผัด (Khao Pad)

ความคืบหน้าของตอนนี้ อัปเดตทุกครั้งที่จบขั้น (กันงานหายเมื่อ /clear)
เริ่มจากแม่แบบ EP03 (`ep03-tom-yum-kung/pixel/` template, `make_json.py`, `capture.cjs`, `check.cjs`, `final/build-final.sh`, `audio/mix.sh`)

## ขั้น 0 — คำตอบเจ้าของช่อง

| เรื่อง | คำตอบ | วันที่ | ที่มา |
|---|---|---|---|
| เมนู | ข้าวผัด = EP04 ตามลำดับตอนที่เสนอในผลสำรวจ | 19 พ.ย. 2026 | `research/top20-thai-dishes-survey-2026-11-18.md` §4 + คำสั่งงาน "ไม่ต้องถามเรื่องเมนูอีก" |
| แนวภาพ | พิกเซลผสมภาพจริง แบบ EP01–EP03 | 18 พ.ย. 2026 | ตัดสินแล้ว ไม่ถามซ้ำ |
| เสียง / ซับ | EN VO Gemini Sulafat + ซับ EN หลัก TH เล็ก · การ์ดท้าย ≤ 3 วินาที | 18 พ.ย. 2026 | ตัดสินแล้ว |
| TikTok | หยุดชั่วคราว ไม่ทำเวอร์ชัน TikTok | 18 พ.ย. 2026 | rules.md §4 |
| Instagram | Reel ธรรมดา (trial reel ใช้ไม่ได้) · "#โฆษณา #ad" บรรทัดแรก | 18 พ.ย. 2026 | rules.md §6 ข้อ 5 |
| Facebook | ผ่าน Postiz ไม่มีป้าย Paid partnership | 19 พ.ย. 2026 | เจ้าของช่อง: "Approve, FB via Postiz" |
| เพดานเงินสร้างภาพ | USD 2 | 19 พ.ย. 2026 | เจ้าของช่อง: "Approve, cap USD 2" |

## สถานะรายขั้น

| ขั้น | สถานะ | หลักฐาน |
|---|---|---|
| 0 ตัดสินใจ | ครบ | ตารางด้านบน |
| 1 ค้นคว้า | ผลิตแล้ว ตรวจแล้วเฉพาะแถว (ข): agent เปิด 13 หน้า (7 ล้ม) แต่หลายแถวคำพูดไม่รองรับข้อความ → session หลักเปิด HTK (เบราว์เซอร์), EatingThaiFood, Hungry in Thailand (WebFetch) เอง ได้ 11 แถว (ข) ที่บทใช้ | `reports/ข้าวผัด รสดั้งเดิมและสี่เสา.md` §(ข) |
| 2 บท | **อนุมัติแล้ว** v1 (เจ้าของช่อง 19 พ.ย. 2026: "Approve, cap USD 2") (8 บรรทัด, ข้าวผัดปู + ทางเลือกกุ้ง หมู ไก่) | `script/vo-script-v1.md` |
| 3 ภาพ | **ตรวจแล้ว** 10 ภาพผ่าน QA รอบแรก (ดูทุกภาพเอง) ใช้ไป USD 0.543 (เพดานรอบนี้ 2) · กระทะ 4 ใบ (กระเทียม → ไข่ → ข้าว → ปู) กรอบตรงกัน · เจ้าของช่องสั่ง "Go, generate" 19 พ.ย. 2026 | `reference/ep04-images-r1.jpg`, `qa.md` ต่อภาพ, `pga-images.md` |
| 4 เสียงพากย์ | **ตรวจแล้ว**: 8 บรรทัด STT ตรงบท · บรรทัด 8 ถ่ายใหม่เป็นสองประโยคแยก (08a + เงียบ 0.45 วินาที + 08b) เพราะเทคเดียวพูด "prik nam pla" ต่อ "In Thailand" จน STT ของไฟล์ผสมรวมเป็นวลีเดียว (ใช้เงินเพิ่มราว 1 เซนต์) · ผมฟังเองไม่ได้ | `audio/vo-en-v1/stt-check.md` |
| 5 เสียงผสม | **ตรวจแล้ว**: -14.5 LUFS, true peak -1.7 dBTP (ไฟล์ MP4) · ดนตรี Suno ของ EP01 + เสียงประกอบสังเคราะห์ของ EP01 (plate, sizzle, pour, pepper, leaves) · loudnorm TP -2.5 เพราะ AAC ดันพีคขึ้น ~0.6 dB (รอบแรกได้ -0.8) | `audio/mix.sh`, `audio/timing.json` |
| 6–7 ภาพเคลื่อนไหว + ซับ | **ตรวจแล้ว**: ซับตรงบท 8/8 EN+TH (โปรแกรมเทียบทีละตัวอักษร) · กล่องซับ x 120–888, y 628–837 ทุกช่วง · บรรทัด 8 ตัดบรรทัดเอง (k 0.73) · กระทะพิกเซลกลับเป็นกระทะของ EP02 · มาตรรส Salty/Sweet/Sour/Spicy ไม่มีขีดเป้า · การ์ดท้าย 2.8 วินาที ("In Thailand?" + "No crab?") | `pixel/check/subtitle-diff.txt`, `pixel/check/subtitle-box.txt`, `pixel/check/sheet.jpg` |
| 8 MP4 | **ตรวจแล้ว**: 1080x1920, 30 fps, 1344 เฟรม, 44.8 วินาที, -14.5 LUFS, peak -1.7 dBTP, ลายน้ำ @saitum528 อ่านชัด, การ์ดท้ายเริ่ม 42.01 วินาที · STT ไฟล์สุดท้ายได้ทุกคำตรงบท แต่สองรอบยังใส่จุดหลัง "in Thailand" แทนหลัง "prik nam pla" (เสียงจริงเป็นสองเทคมีช่องว่าง 0.45 วินาที ซับแยกถูก) — **ยังไม่ได้ฟังด้วยหู** รอเจ้าของช่องฟัง 8 วินาทีท้าย | `final/ep04-v1.mp4`, `final/check/sheet.jpg`, `final/check/final-stt*.txt`, `final/check/wm-zoom.png` |
| 9 ลิงก์ affiliate | **ตรวจแล้ว**: 5 ลิงก์ redirect 301 ไปรหัสสินค้าตรง + ลิงก์รวมร้านตอบ 200 | `affiliate-links.md` |
| 10 โพสต์ | **โพสต์แล้วและเปิดตรวจครบ 3 แพลตฟอร์ม** (ตารางโพสต์ด้านล่าง) · เจ้าของช่องอนุมัติ 19 พ.ย. 2026: "Approve, FB via Postiz" | `captions-draft.md` |## บันทึกสำหรับขั้นโพสต์ (จาก session หลัก 19 พ.ย. 2026)

- YouTube: ทุกครั้งที่กด Save ใน Studio ให้รีโหลดหน้าแล้วอ่านค่า paid promotion และ AI use ซ้ำ (EP03 ค่า paid promotion หายเพราะกล่อง "Verify it's you" ขัดตอน Save) · หลังโพสต์เปิดหน้า watch แบบไม่ล็อกอิน ดูป้าย "Includes paid promotion" (ป้าย AI ตรวจจากภายนอกไม่ได้)

## โพสต์ (19 พ.ย. 2026, Postiz เวลา 12:40 UTC)

| แพลตฟอร์ม | สถานะ | ตรวจแล้ว | ยังขาด |
|---|---|---|---|
| YouTube | **Public** https://youtube.com/shorts/HyNn4qDOWdM (Postiz cmwnjdnyr060sqh07nwaqeti6) | Studio หลังรีโหลด: paid promotion = Yes, AI = Yes, not made for kids, Public (รอบแรกกด Public ไม่ติด ต้องคลิกวงกลมซ้ำ) · ไม่ล็อกอิน: oEmbed 200, isPrivate false, 45 วินาที, **"Includes paid promotion"** อยู่ในหน้า watch, คำอธิบายมี #โฆษณา + ลิงก์ 5 + collshp | ป้าย AI ตรวจจากภายนอกไม่ได้ (ยืนยันจาก Studio เท่านั้น) |
| Instagram | **Live** https://www.instagram.com/p/Df7GlJSCgH-/ (Postiz cmwnjdmht05uknz07oy2x7eo0) Reel ธรรมดา | เล่นได้ 44.8 วินาที, ป้าย "AI content", #โฆษณา #ad บรรทัดแรก, แคปชันครบถึง #thaicooking, ลิงก์ Shopee 5 + collshp, บรรทัดลิงก์ในไบโอ, ช่อง "Add a comment…" เปิด | Paid partnership (บัญชียังไม่ผ่านเกณฑ์) |
| Facebook | **Live** https://www.facebook.com/reel/1591642129671038 (Postiz cmwnjdp8g060tqh077qfjt2jw) | เล่นได้ 44.8 วินาที, แคปชันครบถึง #thaicooking, ลิงก์กดได้ 6 ตัว, #โฆษณา #ad บรรทัดแรก, **"AI content"** ขึ้นบนหัวโพสต์ในไทม์ไลน์เพจ (สลับเป็นเพจ → Edit post → Add AI label → Save รอจน "Saving" หาย) · สลับกลับเป็นโปรไฟล์ส่วนตัวแล้ว ("Comment as" โปรไฟล์ส่วนตัว) | ไม่มีป้าย Paid partnership ตามที่เจ้าของช่องเลือก · **ข้อสังเกต (ยังไม่ทดสอบ):** หน้า Edit reel มีปุ่ม "Tag business partner" ซึ่งอาจแปลว่าใส่ป้ายพาร์ทเนอร์ทีหลังได้ ขัดกับ rules.md §7 ข้อ 1 |

## บทเรียนตอนนี้

- AAC ดัน true peak ขึ้น ~0.6–0.9 dB หลัง loudnorm → ตั้ง TP -2.5 ใน mix.sh (รอบแรก -1.5 ได้ -0.8 เกินกติกา)
- เทคเสียงเดียวที่มีสองประโยค ("…prik nam pla. In Thailand, …") อาจพูดต่อกันจนฟังเป็นวลีเดียว แทรกเงียบไม่พอ → ถ่ายแยกสองเทคตั้งแต่ร่างบท
- FB Add AI label: คลิกสวิตช์ด้วย JS เปลี่ยนแค่หน้าตา ไม่บันทึก ต้องคลิกเมาส์จริงแล้วรอ "Saving" จบ · YouTube Studio: เลือก Public ครั้งแรกไม่ติด ต้องรีโหลดอ่านค่าทุกครั้ง
