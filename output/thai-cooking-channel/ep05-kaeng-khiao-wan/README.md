# EP05 — แกงเขียวหวาน (Kaeng Khiao Wan)

ความคืบหน้าของตอนนี้ อัปเดตทุกครั้งที่จบขั้น (กันงานหายเมื่อ /clear)
เริ่มจากแม่แบบ EP04 (`ep04-khao-pad/pixel/` template, `make_json.py`, `capture.cjs`, `check.cjs`, `final/build-final.sh`, `audio/mix.sh`)

## ขั้น 0 — คำตอบเจ้าของช่อง

| เรื่อง | คำตอบ | วันที่ | ที่มา |
|---|---|---|---|
| เมนู | แกงเขียวหวาน = EP05 | 20 พ.ย. 2026 | `research/top20-thai-dishes-survey-2026-11-18.md` §4 + คำสั่งงาน "ไม่ต้องถามเรื่องเมนูอีก" |
| เสาหลัก | เครื่องเทศ (พริกแกงเขียวหวาน) | 20 พ.ย. 2026 | คำสั่งงาน |
| แนวภาพ | พิกเซลผสมภาพจริง แบบ EP01–EP04 | 18 พ.ย. 2026 | ตัดสินแล้ว |
| เสียง / ซับ | EN VO Gemini Sulafat + ซับ EN หลัก TH เล็ก · การ์ดท้าย ≤ 3 วินาที | 18 พ.ย. 2026 | ตัดสินแล้ว |
| TikTok | หยุดชั่วคราว ไม่ทำเวอร์ชัน TikTok | 18 พ.ย. 2026 | rules.md §4 |
| Instagram | Reel ธรรมดา · "#โฆษณา #ad" บรรทัดแรก | 18 พ.ย. 2026 | rules.md §6 ข้อ 5 |
| Facebook | ผ่าน Postiz ไม่มีป้าย Paid partnership | 20 พ.ย. 2026 | เจ้าของช่อง: "Approve, FB via Postiz" (อนุมัติคลิป + แคปชันด้วย) |
| เพดานเงินสร้างภาพ | USD 2 (manifest cap 4.6955) | 20 พ.ย. 2026 | เจ้าของช่อง: "Approve, cap USD 2" |

## สถานะรายขั้น

| ขั้น | สถานะ | หลักฐาน |
|---|---|---|
| 0 ตัดสินใจ | ครบ ยกเว้นเพดานเงินและวิธีโพสต์ FB | ตารางด้านบน |
| 1 ค้นคว้า | **ตรวจแล้ว**: ทุกแถวที่บทใช้มีคำพูดจริงจาก 4 หน้าที่ session หลักเปิดเอง (HTK 2 หน้าผ่านเบราว์เซอร์, Wikipedia + NatGeo ผ่าน WebFetch) · thaifoodmaster ติด paywall ไม่ใช้ | `reports/แกงเขียวหวาน รสดั้งเดิมและสี่เสา.md` |
| 2 บท | v1 อนุมัติแล้ว ("Approve, cap USD 2") → เจ้าของช่องสั่งให้พากย์ละเอียดกว่าซับ → **v2 อนุมัติแล้ว** (เจ้าของช่อง 20 พ.ย. 2026: "Approve v2") 13 เทค ราว 2:20–2:40 | `script/vo-script-v2.md` |
| 3 ภาพ | **ตรวจแล้ว** 11 ภาพผ่าน QA รอบแรก (ดูทุกภาพเอง) ใช้ไป USD 0.581 (เพดานรอบนี้ 2) · ครก 2 ใบ + หม้อ 3 ใบ กรอบตรงกัน · เจ้าของช่องสั่ง "Go, generate" 20 พ.ย. 2026 · tools/thai-assets-gen.py ล้มตอนเขียน manifest เพราะรายการใหม่ไม่มี `cost_usd` (ภาพสร้างสำเร็จ) → เติมฟิลด์แล้วคำนวณยอดจาก candidates/*.json | `reference/ep05-images-r1.jpg`, `qa.md` ต่อภาพ, `pga-images.md` |
| 4 เสียงพากย์ | **ตรวจแล้ว**: 13 เทค STT ตรงบท 13/13 (ต่างแค่สะกด UK/US) รวม 145.1 วินาที · ผมฟังเองไม่ได้ | `audio/vo-en-v1/stt-check.md` |
| 5 เสียงผสม | **ตรวจแล้ว**: -14.0 LUFS, true peak -2.2 dBTP (ไฟล์ MP4) · ดนตรี Suno ของ EP01 วน 3.7 รอบ + เสียงประกอบสังเคราะห์ของ EP01 | `audio/mix.sh`, `audio/timing.json`, `final/check/loudness.txt` |
| 6–7 ภาพเคลื่อนไหว + ซับ | **ตรวจแล้ว**: ซับตรงคอลัมน์ SUB ของบท v2 13/13 EN+TH (โปรแกรมเทียบทีละตัวอักษร) · กล่องซับ x 120–888, y 628–837 ทุกช่วง ไม่ทับอะไร · TH = 65% ของ EN · การ์ดท้าย 2.77 วินาที ("In Thailand?" + "No Thai eggplant?") · session หลักดูเฟรมกลางทุกช่วงเอง | `pixel/check/subtitle-diff.txt`, `pixel/check/subtitle-box.txt`, `final/check/sheet.jpg` |
| 8 MP4 | **ตรวจแล้ว**: 1080x1920, 30 fps, 4684 เฟรม, 156.14 วินาที, -14.0 LUFS, peak -2.2 dBTP, ลายน้ำ @saitum528 (session หลักซูมดูเอง) · STT ไฟล์เต็ม: ครบ 13 บรรทัด แต่ที่รอยต่อ 12a→12b STT ได้ "If in Thailand" / "Ingredient links" เมื่อถอดพร้อมท้าย 12a ส่วนตัด 12b เดี่ยวจาก MP4 ถอดได้ "In Thailand, affiliate links are in the caption." 4/4 รอบ — **ยังไม่มีใครฟังด้วยหู** รอเจ้าของช่องฟังช่วง 2:30–2:36 | `final/ep05-v1.mp4`, `final/check/` |
| 9 ลิงก์ affiliate | **ตรวจแล้ว**: 6 ลิงก์ redirect 301 ไปรหัสสินค้าตรง + collshp 200 | `affiliate-links.md` |

## บทเรียนตอนนี้

- WebFetch เปิด hot-thai-kitchen.com ได้ HTTP 402 → เปิดด้วยเบราว์เซอร์ในแอปแล้วดึงประโยคด้วย JS แทน
- รายการใหม่ใน manifest ต้องมี `"cost_usd": 0.0` ไม่งั้น `thai-assets-gen.py` ล้มหลังสร้างภาพเสร็จ (เสียเงินแล้วแต่ไม่บันทึก)
- curl ตรวจลิงก์ Shopee ติดกันเร็วได้รหัส 000 → เว้น 1 วินาที
- เจ้าของช่อง 20 พ.ย.: เสียงพากย์ละเอียดกว่าซับ (บท v2) — ตรวจซับเทียบคอลัมน์ SUB ไม่ใช่ VO

| 10 โพสต์ | **โพสต์แล้วและเปิดตรวจครบ 3 แพลตฟอร์ม** (ตารางด้านล่าง) · เจ้าของช่องอนุมัติ 20 พ.ย. 2026: "Approve, FB via Postiz" | `post/` |

## โพสต์ (20 พ.ย. 2026, Postiz เวลา 11:07 UTC)

| แพลตฟอร์ม | สถานะ | ตรวจแล้ว | ยังขาด |
|---|---|---|---|
| YouTube | **Public** https://www.youtube.com/watch?v=KXISNq_-iMQ (Postiz cmwovibpy00tlob07p6e18f2g) | Studio หลังรีโหลด: paid promotion = Yes, AI = Yes, not made for kids, Public · ไม่ล็อกอิน (curl): isPrivate false, 156 วินาที, **"Includes paid promotion"** ในหน้า watch, คำอธิบายมี #โฆษณา + ลิงก์ Shopee 6 + collshp, playability OK | ป้าย AI ตรวจจากภายนอกไม่ได้ (ยืนยันจาก Studio) · คลิปยาว 2:36 YouTube อาจไม่จัดเป็น Shorts (ยังไม่ได้ตรวจ) |
| Facebook | **Live** https://www.facebook.com/reel/4122670307875301 (Postiz cmwoviksv00tqob07n4nr5guf) | เล่นได้ 156.3 วินาที, แคปชันครบถึง #thaicooking, ลิงก์ Shopee 6 + collshp กดได้ 7 ตัว, #โฆษณา #ad บรรทัดแรก, **"AI content"** บนหัวโพสต์ในไทม์ไลน์เพจ (สลับเป็นเพจ → Edit post → คลิกสวิตช์จริง → Save รอ Saving หาย) · สลับกลับโปรไฟล์ส่วนตัวแล้ว | ไม่มีป้าย Paid partnership ตามที่เจ้าของช่องเลือก |
| Instagram | **Live** https://www.instagram.com/p/Df9guqClWl_/ (Postiz cmwovi2oe00q1tl07tk2eabas) Reel ธรรมดา | เล่นได้ 156.1 วินาที, ป้าย "AI content", #โฆษณา #ad บรรทัดแรก, แคปชันครบถึง #thaicooking (1,750 ตัวอักษร ใต้เพดาน 2,200), ลิงก์ Shopee 6 + collshp, บรรทัดลิงก์ในไบโอ, ช่องคอมเมนต์เปิด | Paid partnership (บัญชียังไม่ผ่านเกณฑ์) |

- YouTube Studio ในเบราว์เซอร์ในแอปเปิดช่อง AetherFlow Studio ไว้ → หน้า edit ขึ้น "Oops" → สลับช่องเป็น สายตํา Shop ผ่านเมนู avatar → Switch account ก่อน
- เบราว์เซอร์ในแอปถูกซ่อน: หน้า youtube.com แสดงว่างเปล่า แต่ studio.youtube.com และ facebook/instagram ใช้ JS อ่านค่าได้
- แคปชัน Instagram จำกัด 2,200 ตัวอักษร (Thai ก็นับเป็นตัว) — ตัดขั้นตอนเต็มออก ใส่ "เล่าไว้ในคลิป"
