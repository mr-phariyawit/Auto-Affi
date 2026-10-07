# Higgsfield Bible v2 (TH) — article + audio + visual

ฉบับ 2.0 • 7 ตุลาคม 2026 • จัดทำสำหรับ Auto-Affi • ต่อจาก Mega Bible v1 (5 ตุลาคม 2026)

## ขอบเขต หลักฐาน และวิธีอ่าน

คู่มือนี้สรุป 16 คอร์ส 171 บทของ Higgsfield Academy พร้อม Prompt Bank หมวดกล้อง 46 รายการ และหน้า overview ของคอร์ส 16 หน้า v1 เรียบเรียงจากข้อความบทความประกอบบทเรียนอย่างเดียว ส่วน v2 ใช้หลักฐานสามช่องทาง คือ article (ข้อความบทความและ prompt/cue ที่แนบ), audio (transcript ของเสียงในวิดีโอ) และ visual (เฟรมจากวิดีโอ รวมเฟรมความละเอียดสูงเมื่อจำเป็น)

**สถานะหลักฐาน (จาก `ledger.csv`):** ทั้งหมด 233 หน่วย = บทเรียน 171 + Prompt Bank 46 + Course Pages 16 ผ่านการตรวจโดย audit-lead วันที่ 2026-10-07 ทั้งหมด แบ่งเป็น **231 VERIFIED + 2 VERIFIED_GAP**

- ช่อง article ครบ 231 หน่วย ขาด 2 หน่วย คือ A15.L09 และ A15.L10 (สำเนาบทความถูกบล็อก) สองบทนี้เป็น VERIFIED_GAP และเนื้อหามาจาก transcript และเฟรมเท่านั้น
- ช่อง audio มีครบทุกบทเรียน 171 บท (Prompt Bank และ Course Pages ไม่มีเสียงให้ถอด)
- ช่อง visual มี 217 หน่วย คือบทเรียนทุกบทและ Prompt Bank ทุกรายการ (Course Pages ตรวจจากข้อมูลหน้าเว็บ ไม่ใช่วิดีโอ)

**รูปแบบการอ้างอิง** ทุกบรรทัดเนื้อหาในภาค A–F มีวงเล็บอ้างอิงอย่างน้อยหนึ่งอัน:

- `[A01.L03 t=01:22]` = เสียงพูดในวิดีโอ คอร์ส A01 บทที่ 3 ที่เวลานั้น (ช่วงเวลาเขียนเป็น `t=01:22-01:39`)
- `[A01.L03 frames t=01:03]` = สิ่งที่เห็นบนจอในเฟรมเวลานั้น
- `[A01.L03 article]` = บทความประกอบบทเรียน
- `[A01.L05 cue recreate-1b]` = prompt/cue ที่แนบมากับบท ตามชื่อ cue
- `[A15.L10 article-tail]` = ส่วนท้ายบทความที่เหลือรอดหลังช่องว่าง (ใช้เป็นหลักฐานบางส่วนเท่านั้น)
- `[PB.05]` = Prompt Bank รายการที่ 5 ส่วน `[CP.A13]` = หน้า overview ของคอร์ส A13

**ราคาและตัวเลข** ราคาเครดิต ชื่อโมเดล ความละเอียด ระยะเวลา และตัวเลขรายได้ทั้งหมดเป็นค่าที่บันทึกได้ ณ วันที่ถ่ายคอร์ส (as-recorded) ส่วนใหญ่อ่านจากปุ่มหรือแถบ settings บนจอ ไม่ใช่ราคาปัจจุบัน ต้องตรวจในผลิตภัณฑ์อีกครั้งก่อนใช้จริง ตัวเลขธุรกิจที่ผู้สอนหรือ Claude แสดงบนจอไม่มีแหล่งอ้างอิงอิสระ

**สิ่งที่เอกสารนี้ไม่ได้ทำ** ไม่ได้ทดลอง generate ตาม prompt ในคอร์ส ไม่ได้เปิดไฟล์ skill ที่คอร์สอ้าง (ส่วนใหญ่ไม่อยู่ในวัสดุคอร์ส) และไม่เพิ่มข้อเท็จจริงที่ไม่มีในบันทึกการศึกษา ข้อความที่เป็นการตีความจะติดป้าย "ข้อสังเกต" หรือ "อนุมาน" ไว้

**วิธีอ่าน**

- อยากรู้ว่าคอร์สเดียวสอนอะไร ให้อ่านภาค A (รายคอร์ส เรียงตาม A01–A16)
- อยากได้กฎที่ใช้ได้กับงานใหม่ ให้อ่านภาค B ซึ่งรวมเฉพาะกฎที่สอนตรงกันตั้งแต่สองคอร์สขึ้นไป
- อยากได้ prompt กล้องสำเร็จรูป ให้เปิดภาค C1 (Prompt Bank) และข้อมูลคอร์สจากหน้าเว็บอยู่ในภาค C2
- อยากรู้ว่าวิดีโอมีอะไรที่บทความไม่มี ให้อ่านภาค D
- ก่อนเชื่อ cue หรือตัวเลขใด ให้เช็กภาค E (จุดขัดแย้งและช่องว่างหลักฐาน)
- อยากรู้ว่า v2 ต่างจาก v1 ตรงไหน ให้ดูตารางภาค F

## สารบัญ

- ขอบเขต หลักฐาน และวิธีอ่าน
- ภาค A — รายคอร์ส
  - A01 Blockbuster 4K: The AI Filmmaking Pipeline
  - A02 Build an Ultra-Realistic Short Film in 4K
  - A03 Add AI VFX to Real Footage
  - A04 Make an AI Animated Short
  - A05 How to evaluate AI filmmaking demos
  - A06 The 3-Step Realistic AI Ad Workflow
  - A07 Build an AI Ad Agency with Claude + Higgsfield
  - A08 Seedance 4K: Cinematic Realism
  - A09 Build a Brand's Visuals with AI
  - A10 Make a Cinematic Ad End-to-End
  - A11 Automate a Faceless Niche Channel
  - A12 Build a Faceless Channel
  - A13 Mix AI with Real Footage
  - A14 Build 3D Games with MCP
  - A15 Direct a cinematic AI car commercial
  - A16 Direct AI fight scenes through controlled iteration
- ภาค B — กฎข้ามคอร์ส (B1 ลำดับงานและ asset … B13 MCP ต้นทุน และความรับผิดชอบ)
- ภาค C — Prompt Bank (PB) และ Course Pages (CP)
- ภาค D — เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- ภาค E — จุดที่คอร์สขัดแย้งกันเอง และช่องว่างหลักฐาน
- ภาค F — ตาราง diff v1 → v2
- บันทึกฉบับ

## ภาค A — รายคอร์ส

## A01 Blockbuster 4K: The AI Filmmaking Pipeline

### ภาพรวมและผลลัพธ์
- คอร์ส 10 บทของผู้สอน Adil ทำหนังสั้นแอ็กชันด้วย Seedance 2.0 ที่ 4K โดยให้ตัวเอกคนเดียวข้ามโลกโจรสลัด ทะเลทราย ป่า แล้วจบด้วยการเฉลยว่าน้องสาว (Cindy) เป็นคนกดปุ่มเขียวส่งเขาไป [A01.L01 t=00:30] [A01.L01 article]
- ผลลัพธ์ที่สัญญาไว้คือช็อตที่ดูเป็นภาพยนตร์ เล่าเรื่องจากฉากแรกถึงจุดหักมุม และไม่เผาเครดิตกับการสุ่ม generate [A01.L01 t=00:41] [A01.L01 article]
- Pipeline หลักคือ Script → Assets (characters, locations, props) → Scene generation [A01.L01 article]
- Claude skill เป็นตัวเขียน Seedance prompt ทั้งหมด ไม่เขียนด้วยมือ [A01.L01 t=00:51] [A01.L04 t=00:11]
- ไฟล์ทั้งหมด (script, prompts, asset sheets, skill) แจกในบล็อก higgsfield.ai/blog/case4k [A01.L01 article] [A01.L10 t=03:55]
- บทสรุปท้ายคอร์ส: ทำงานแบบคนทำหนัง คือบทก่อน แล้วใช้ prompt-building framework แปลงบทเป็นช็อต ห้ามโยน prompt บรรทัดเดียวแล้วหวัง [A01.L10 t=03:24]
- ผู้สอนบอกว่า workflow เดียวกันใช้กับโฆษณา หนังสั้น หรือไอเดียใดก็ได้ [A01.L10 t=04:00]

### Workflow ทีละขั้น
1. เขียน premise ประโยคเดียว (ตัวเอก + กับดัก + กฎที่วนซ้ำ) เช่น "a guy gets trapped in his little sister's AI generations. Every time he dies — he wakes up in a new world." [A01.L02 t=00:10]
2. ขอให้ Claude "expand my idea" แทน "write me a script" แล้วตอบคำถามของมัน: runtime 2 นาที, settings pirates/desert/jungle, plot twist = yes ได้บทแบบ BEAT ทีละช่วง [A01.L02 t=00:22] [A01.L02 t=00:27-00:35]
3. ตั้งโปรเจกต์ใน Higgsfield Cinema Studio → New Project แยกโฟลเดอร์ต่อฉากและโฟลเดอร์ย่อยต่อ asset และเก็บ asset สุดท้ายบน canvas [A01.L03 t=00:00-00:17] [A01.L03 t=01:52-02:02]
4. Hero character sheet: แนบ reference sheet ของตัวจริง (หน้าตรง + profile ซ้าย/ขวา) ให้ Claude เขียน prompt 3 views (full front, full back, close-up) พื้นเทา แล้วรันใน GPT Image 2.0 พร้อมแนบ reference [A01.L03 t=00:21-00:27] [A01.L03 t=00:31-00:45] [A01.L03 t=01:02]
5. แก้ภาพใน GPT Image 2.0 ให้ลบหน้าบนแผง full-body front เหลือหน้าเดียวต่อ sheet [A01.L03 t=01:22-01:47] [A01.L03 cue erase-extra-faces-for-consistency]
6. Location: ให้ Claude "enhance" คำขอสั้น ๆ (มุม 3/4 + แหล่งแสงชัด) แล้วรัน Soul Cinema หลาย batch (8 ภาพต่อ 1 credit) เลือกจากแสงและองค์ประกอบ [A01.L03 t=02:12-02:42] [A01.L03 t=03:01-03:31]
7. Props: พิมพ์ prompt split-screen ง่าย ๆ ลง Soul Cinema ตรง ๆ แล้วปรับแต่งด้วย edit prompt ที่ Claude เขียนใน GPT Image 2.0 (ระบุ hex สีเป๊ะ) [A01.L03 t=03:49] [A01.L03 t=04:12-04:41]
8. ตั้งชื่อทุก asset เป็น @tag แนะนำให้ Claude รู้จักด้วยชื่อนั้น และเพิ่มใน Higgsfield Elements ด้วยชื่อเดียวกันเป๊ะ (Character / Location / Prop) [A01.L03 t=05:10-05:26]
9. ติดตั้ง skill `higgsfield-seedance-prompt` ใน Claude: Customize → Skills → + → Upload a skill [A01.L04 t=00:15-00:25]
10. ต่อช็อต: เปิด skill ในแถบ Claude แนบทุก asset ที่ช็อตต้องใช้จาก canvas + script แล้วเล่า beat เป็นภาษาธรรมดาโดยวาง @tag หลังคำนามที่ต้องคงที่ [A01.L04 t=00:38-00:44] [A01.L04 cue upload-prompt-builder-skill]
11. วาง structured prompt ที่ได้ลง Seedance 2.0 ตั้ง 21:9, 4K, 15 s, 4 batches พร้อมแนบภาพ reference [A01.L05 t=00:02-00:05]
12. ดู batch เทียบกับเรื่อง จดข้อผิดเป็นข้อ ๆ ส่งกลับ Claude เป็น fix list ภาษาธรรมดา แล้วรันใหม่ด้วย settings เดิม [A01.L05 t=00:30-01:09]
13. เลือกช่วงดีจากหลาย batch มาประกอบ (ต้นจากคลิปหนึ่ง ที่เหลือจากอีกคลิป) แล้วลากเข้า PROJECT TIMELINE ทีละฉาก [A01.L05 t=03:05] [A01.L06 t=02:01-02:07] [A01.L05 frames t=01:30]
14. เชื่อมฉากด้วย action เข้า/ออกที่ตรงกัน (ตกจากป่า → ร่วงลงโซฟา, ฝุ่นทึบ → ทะเลทราย) [A01.L09 t=00:23-00:30] [A01.L07 t=01:03-01:26]

### กฎที่ใช้ซ้ำได้
- ห้าม one-shot บท ให้ Claude ขยายไอเดียและสัมภาษณ์เรา เพราะคำขอขี้เกียจครั้งเดียวได้บทกลาง ๆ ที่แย่ [A01.L02 t=00:18] [A01.L02 t=00:37-00:42]
- หนึ่งหน้าต่อ character sheet ถ้ามีหลายหน้า Seedance จะ drift identity ("by scene 5 our hero is a stranger") [A01.L03 t=01:22-01:39] [A01.L10 t=03:39]
- พื้นหลังเทาไม่รกเพิ่ม win rate และได้ generation ที่ใช้ได้มากขึ้น [A01.L03 t=00:45-00:54]
- Location ให้ขอมุม 3/4 เสมอ เพราะให้ depth เมื่อกล้องเคลื่อน และ win rate สูงกว่ามุมตรงแบน [A01.L03 t=02:42-02:52]
- Location ที่ดูถูกจะทำให้ทุกช็อตดูถูก และแก้ทีหลังด้วย prompt ไม่ได้ [A01.L03 t=02:02-02:12]
- แบ่งงาน: Soul Cinema = raw pass (prompt ง่าย หลาย take หลากหลาย); GPT Image 2.0 = edit และ clean sheet สุดท้าย [A01.L03 t=04:49-04:58]
- @tag ต้องตรงกันทั้งใน Claude และ Higgsfield Elements เพื่อให้ prompt จับคู่ reference อัตโนมัติ [A01.L03 t=05:10-05:26] [A01.L04 article]
- ใช้ crew reference sheet (@eduardo_crew) ไม่งั้นตัวประกอบดูเหมือนตัวสุ่ม [A01.L04 t=00:55] [A01.L04 article]
- ล็อกสภาพแวดล้อมด้วย location asset เฉพาะ เช่น @ocean_location ให้น้ำเหมือนกันทุก batch, @island_location ล็อกเกาะใน spyglass [A01.L05 article]
- Asset ซ้อน asset: ถ้า location ขาดจุดสำคัญ (oasis) ให้สร้างจุดนั้นเป็น location asset แยก [A01.L07 t=01:41-01:53] [A01.L10 t=03:39-03:43]
- ตัวละครต้องตอบสนองต่อโลก (ยิ้ม, ฟาดแผนที่ลง, เดินไปที่ประตู) การยืนจ้องเฉย ๆ ทำให้ช็อตตาย [A01.L05 t=01:15-01:27]
- take ที่ "ไม่แย่แต่น่าเบื่อ" ให้แก้ด้วย comedy ของตัวละคร (ท่าเดินแปลก ให้สัตว์พูด ประโยคซ้ำ) ไม่ใช่เพิ่ม spectacle [A01.L05 t=02:19-02:35]
- ถ้ามีภาพในหัวชัด ให้บอก Claude ตรง ๆ เป็นคำพูดธรรมดา [A01.L06 t=01:04-01:08]
- ถ้า cut หนึ่งทำลาย flow ให้สั่งลบ cut นั้นให้ cut ก่อนหน้าไหลเข้า cut ถัดไป [A01.L06 t=00:27-00:41]
- อัปโหลดภาพวาดแทนการอธิบาย geometry ด้วยคำ ("one drawing tells the model what 10 sentences can't") ประหยัด batch ที่พังและเครดิต [A01.L06 t=01:34-01:49]
- Loop หลัก: run → look → ขอแก้แบบเจาะจง → run อีก [A01.L06 t=02:11-02:16]
- เปิดฉากรบด้วยลูกปืนพลาดตกน้ำในเฟรมแรก อย่าให้โดนตัวเอกทันที [A01.L06 t=01:20-01:34]
- ความต่อเนื่องสภาพแวดล้อม: เรือที่โดนยิงต้องมีดาดฟ้าเปียกเลอะ ไม่ใช่แห้ง [A01.L06 t=02:43-02:54]
- เว้นที่ให้การไล่ล่า: ดันผู้ไล่ไปไกลด้านหลัง [A01.L07 t=02:32-02:45]
- ให้ตัวเอก "เกือบ" ถึงเป้าหมาย ("almost is what makes it hurt") [A01.L07 t=03:45-04:02]
- Multi-shot ล้มเหลวหนัก ให้ลดเหลือ one continuous shot ของโมเมนต์หลักอย่างเดียว [A01.L08 t=01:35-01:48]
- ใช้ multi-shot เมื่อ "the comedy is in the cut" [A01.L08 t=02:42]
- Asset ที่ออกมาเป็นการ์ตูน/พลาสติก ให้สลับเป็น asset ที่สมจริงกว่ากลางทาง และเตรียม variation ไว้ [A01.L08 t=02:54-03:20]
- เมื่อสภาพตัวละครเปลี่ยนกลางช็อต (เสื้อผ้าขาด) ให้สร้าง mid-story character sheet ของสภาพใหม่ แล้วสลับใช้ตั้งแต่เวลาที่เกิดเหตุ [A01.L08 t=04:27-04:46] [A01.L08 cue generate-mid-story-character-sheets]
- บทสนทนา: ให้ reverse-angle environment reference ของห้องเดียวกันทั้งสองฝั่ง และล็อกกล้องตามกฎ 180 องศาด้วย framing เดิมต่อผู้พูด [A01.L09 t=01:05-01:17] [A01.L09 t=02:31-02:50]
- กำกับอารมณ์ด้วยเจตนา ไม่ใช่ความดัง ("HELL NAHHH" = ไม่เชื่อแบบดูแคลน) [A01.L09 t=02:56] [A01.L09 cue enforce-the-180-rule]
- สั่งให้ effect จบครบ (dissolve ต้องหายหมดตัว) [A01.L09 t=02:24] [A01.L09 cue enforce-the-180-rule]

### โครงสร้าง Prompt
- ขอ character-sheet prompt จาก Claude: "Write a prompt for a character sheet of this guy, dressed as <role>. Three views: <view 1>, <view 2>, <close-up>. He is wearing <signature costume items>. <grime/weathering>. Use clean, light grey background." [A01.L03 cue 3-view-character-sheet]
- prompt GPT Image ที่ Claude ขยายแล้ว เรียงเป็น: sheet type + film-photo style → lighting (soft, diffused, no hotspots) → backdrop mid-grey ห้ามขาว → identity block (อายุ ผิว ผม หนวด ต่างหู ความไม่สมมาตร แผลเป็นระบุข้างและขนาด) → "keep exact same identity across views" → anatomy guard (แขนสองข้าง มือครบ) → grime/texture → costume → layout สามแผง → consistency recap → "never plastic CGI skin" → aspect [A01.L03 cue 3-view-character-sheet-recreate]
- ลบหน้าส่วนเกิน: "Erase the face from the <panel> on the <position> panel." [A01.L03 cue erase-extra-faces-for-consistency]
- คำขอ location: "Write a prompt for a <location>. <key furniture>, <single practical light>, <lighting mood>, 3/4 angle, <hero prop placement>, <secondary light source detail>." [A01.L03 cue establish-depth-with-3-4-angles]
- Location prompt ที่ขยายแล้ว: style/genre/period → set + props → พฤติกรรมไฟ practical → เวลา/อากาศ → shot type ("wide three-quarter interior establishing shot, eye-level, slow push-in") → lighting design → palette → mood → camera/lens (24mm, 2.39:1) → lens artefacts → DOF → grain → textures → atmosphere → film emulation [A01.L03 cue location-recreate]
- Prop turnaround ภาพเดียว: "Split-screen sheet, same <prop> twice: LEFT <angle + features>; RIGHT <angle + features>. <materials>, <environment>, <light>. Photoreal." [A01.L03 cue split-screen-ship-assets]
- Edit prompt: "Write a prompt to edit this reference image: <change 1>, <change 2>, and in the <panel> only — add <element>. The emblem color must be exactly hex `<hex>`." [A01.L03 cue customize-assets-in-gpt-image]
- เรียก skill ต่อช็อต: "/higgsfield-seedance-prompt write a prompt for scene <N>, part <M>. @<hero> is <action> in <location> @<location>. ... finds a <PROP> @<prop>. ... At that moment <event>, and <secondary> @<crew asset> says <dialogue gist>." วาง @tag ทันทีหลังคำนามที่ต้องคงที่ เรียง beat ตามลำดับ [A01.L04 cue upload-prompt-builder-skill]
- Fix notes แบบข้อ: "Fix the prompt: 1) <replace X with Y>, 2) <emotion beat>, 3) <dialogue line>, 4) <reaction on event>, 5) <lighting/time-of-day fix>, 6) <ending action>." [A01.L05 cue multi-shot-cabin-prompt]
- โครง Seedance prompt ที่ skill สร้าง: SCENE CONTEXT → ACTIVE REFERENCES → LOCATION MAP → FIRST FRAME / BLOCKING → FORMAT MODE → OPTICS → CAMERA → ACTION → PERFORMANCE → PHYSICS → LIGHTING → AUDIO → STYLE → POSITIVE LOCKS [A01.L05 cue recreate-1b]
- ใน ACTIVE REFERENCES แต่ละ @tag มีคำอธิบาย + "100% matches the reference; identity, face and wardrobe locked. Studio sheet background and layout NOT inherited"; location "control environment, materials and mood only; reference framing not inherited" [A01.L05 cue recreate-1b]
- ขอบเขตหน้าที่ reference: @main_ship_sheet "controls hull, deck, masts and rigging only", @ocean_location "controls water and sky atmosphere only", @button "appears ONLY inside the final zoomed spyglass view" [A01.L05 cue recreate-1-2a]
- FORMAT MODE แบบ Scene 1: "Sequence of cuts, no timecodes — cuts only at the specified points, the camera does not cut on its own" แล้วระบุ CUT n พร้อม shot size และ FOV เป็นองศา (เช่น 47° neutral, 29° portrait) [A01.L05 cue recreate-1b]
- FORMAT MODE แบบ Scene 2-4: "Timed multishot" ระบุช่วงเวลา เช่น "0.0s to 5.5s — LENS LOCK: 29° on the crest line ..." [A01.L07 cue recreate-2-1c]
- Locks ที่ตั้งชื่อเฉพาะ: HEADCOUNT LOCK ("exactly THREE riders on exactly THREE ostriches ... never two, never four"), STAGE LOCK, HANDS LOCK, FLIGHT LOCK, OPENING LOCK [A01.L07 cue recreate-2-1c] [A01.L06 cue recreate-1-4b] [A01.L07 cue recreate-2-1d]
- ล็อกข้างมือ/ตา ทิศจอ และสเกล: RIGHT hand, RIGHT eye; "SPYGLASS POV, MONOCULAR ... never the twin overlapping circles of binoculars"; เรือศัตรู "under 5% of the frame height" [A01.L05 cue recreate-1-2b]
- คำสั่งลบ cut: "Re-write the prompt. Remove cut <n> ... — cut <a> should flow straight into cut <b>, so nothing blends together." [A01.L06 frames t=00:35]
- แก้ด้วยภาพวาด: "<object> @<tag> must not <wrong behaviour> — <intended beat>: add <establishing event> right in the first frame. ... follow the green circle in the picture. ... And remove the first wide cut." [A01.L06 cue guide-layout-with-drawings]
- Stitch กับช็อตก่อน: "Write a prompt to stitch with the previous shot ... the generation starts with him landing on the deck ... transition to the next location. @location_desert + @main_character_desert. Camera handheld, at human eye level." [A01.L06 frames t=02:30]
- ลดความซับซ้อน: "Give me just one continuous POV shot. The eye opens slowly like shutters, and we see the spider." [A01.L08 t=01:42-01:48]
- Multishot request: "multishot, N cuts, <location @tag>. Cut 1: <action> + <line> + <camera move> + <what matters>. Cut 2: <shot size/angle> + <crowd action> + <end state> + <audio carry-over>." [A01.L08 article]
- Rewrite ที่ดี = สลับ asset → แก้ timing พร้อมเหตุผล → แก้กล้องต่อ cut พร้อมเหตุผล [A01.L08 frames t=03:25]
- Mid-story sheet fix: "Rewrite the prompt using the new @<state asset> immediately after <event>. Also, adjust the ending physics: <object> must stay <state> as <action>. <secondary actor> should not <wrong> — it <correct>." [A01.L08 cue generate-mid-story-character-sheets]
- Reverse-angle fix: "Re-write the prompt — use two extra locations, two reference images of the same room: @<room2> and @<room3>. Lock the exact size for the <prop> @<tag> and the <animal> @<tag> should sit on top of the <object>, not inside it." [A01.L09 cue use-reverse-angle-blueprints]
- 180-rule fix: "Re-write the prompt. Lock the camera. On <A> @<tag> lines, always show her from the same angle ... On <B> @<tag> lines, show him over <A>'s left shoulder — same framing every time. Fix <B>'s emotion on '<line>' ... <B> must disappear completely — the dissolve has to finish." [A01.L09 cue enforce-the-180-rule]
- OPTICS สลับ single/OTS ใน 15 s: "0.0-4.5s: 29° medium close single ... 4.5-7.0s: 47° over-shoulder medium ... 7.0-10.5s: 29° ... 10.5-15.0s: 47° ... No drift." [A01.L09 frames t=02:55]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Claude chat UI ตัวเลือกโมเดลอ่านได้ว่า "Fable 5" effort "High" ใช้เขียนบท prompt และ edit prompt [A01.L02 frames t=00:12] [A01.L04 frames t=00:40]
- GPT Image 2.0 (UI "GPT Image 2"): Auto / High / 2K / 4/4 = GENERATE 28 credits; แก้ลบหน้าที่ 1/4 = 7 credits [A01.L03 frames t=01:03] [A01.L03 frames t=01:43]
- Soul Cinema (imageModel=soul_cinematic): 8 ภาพต่อ 1 credit; settings 16:9 / 2K / 4/4; รัน split-screen props = 0.5 credits ที่ 4/4 [A01.L03 frames t=02:56] [A01.L03 frames t=03:55] [A01.L03 article]
- Seedance 2.0 / 21:9 / 4k / 15s / 4/4 / On / High = GENERATE 1,320 credits (ขีดฆ่า 1,560 เป็น discount) [A01.L05 frames t=00:05] [A01.L07 frames t=00:40]
- Seedance ที่ batch 2/4 = 660 credits (ขีดฆ่า 780) [A01.L07 frames t=01:20]
- Shot 1 ของฉากป่า: Seedance 2.0 / 21:9 / 4k / 8s / 1/4 / On / High = 176 credits (ขีดฆ่า 208); prompt ที่ Claude เขียนระบุ "OUTPUT SETTINGS: 21:9 aspect ratio, 8 seconds total" (8 s ไม่ใช่ 15 s) [A01.L08 frames t=01:22] [A01.L08 frames t=01:24]
- Aspect ratio dropdown ของ Seedance มี Auto, 16:9, 9:16, 4:3, 3:4, 1:1, 21:9 [A01.L05 frames t=00:05]
- Recreate URL ของ Seedance: `/generate/video/seedance_2_0?aspect_ratio=21:9&resolution=4k` [A01.L07 cue recreate-2-1c]
- Higgsfield Elements panel: แท็บ Uploads / Elements / Image Generations / Liked, ปุ่ม "New Element", หมวด Character / Location / Prop [A01.L03 frames t=05:20]
- PROJECT TIMELINE ของ Higgsfield ใช้รวมคลิปที่เลือก มีกลุ่มฉากแยกสี (Scene 1 ส้ม, 2 เบจ, 3 เขียว, 4 ชมพู) พร้อม audio track [A01.L05 frames t=01:30] [A01.L10 frames t=00:00]
- 4K ถูกยกเป็นเหตุผลให้ระเบิดคมและหนัก ไม่เบลอเป็น "slop" [A01.L06 t=01:55-02:01] [A01.L10 t=03:43-03:50]
- Asset tags ที่ใช้ในฉาก 1: @eduardo, @loc_cabin, @main_ship_sheet, @villain_ship_sheet, @spyglass_sheet, @parrot_sheet, @ship_cannon, @map_prop, @cannonball, @button, @eduardo_crew, @ocean_location, @island_location, @villain_captain, @helmsman_sheet [A01.L03 article]
- สีตราสัญลักษณ์แบรนด์ #D1FE17 [A01.L03 cue customize-assets-in-gpt-image]
- ปุ่ม button ล็อกขนาด "roughly 8 × 8 × 4 cm" [A01.L09 cue recreate-4-1a]

### คำเตือนและ failure modes
- สุ่ม generate เผาเครดิต [A01.L01 t=00:46]
- character sheet หลายหน้า → identity drift ข้ามฉาก [A01.L03 t=01:22-01:39]
- พื้นรกลด win rate; มุมตรงแบน win rate ต่ำกว่า 3/4 [A01.L03 t=00:50] [A01.L03 t=02:48]
- location พังที่เห็น: ไฟเกินทำให้แสงแปลกและบังพร็อพหลัก, เฟอร์นิเจอร์หลักไปอยู่มุม, แผนที่อยู่ผนังข้าง [A01.L03 t=03:01-03:19]
- ใบเรือปิดทำให้เรือดู "จอด" [A01.L03 t=04:18]
- ของบนโต๊ะเยอะเกินจะละลายรวมกัน [A01.L05 t=00:30]
- ความต่อเนื่องเวลาแตก: ข้างนอกประตูเป็นกลางคืนในเรื่องกลางวัน [A01.L05 t=00:45]
- spyglass POV อาจออกมาเป็นวงกล้องสองตา (binocular) prompt จึงห้ามไว้ [A01.L05 cue recreate-1-2b]
- จุดที่ลูกปืนชนเปลี่ยนทุก batch ถ้าอธิบายด้วยคำอย่างเดียว [A01.L06 t=01:14-01:20]
- batch ที่พังมีราคาเป็นเครดิต [A01.L06 t=01:49]
- เปิดฉากโดยไม่เว้นจังหวะให้หายใจ ทำให้ cut จากฉากก่อนดูผิด [A01.L07 t=01:03-01:26]
- ตัวเอกวิ่งผิดทาง; ผู้ไล่ชิดเกินจนไม่มีที่ไล่ [A01.L07 t=02:11] [A01.L07 t=02:38-02:45]
- นกกระจอกเทศต้องล็อกขาสองข้างและจำนวนตัวแบบ explicit [A01.L07 cue recreate-2-2a]
- ฉากป่าใช้ batch มากที่สุดในหนัง [A01.L08 t=00:18]
- POV multi-shot พัง: โมเดลวางแมงมุมไว้ในตาตัวละคร แทนที่กล้องจะเป็นตา [A01.L08 t=01:26-01:35]
- POV ซูมออกจากตาเหมือนเลนส์จริง และวางแมงมุมกลางเฟรมดูผิด [A01.L08 t=01:55-02:00]
- Mandrill ออกมาเป็นการ์ตูน (จมูกสีสด) [A01.L08 t=02:58-03:04]
- พูดบทยาวก่อนภัยมาถึง ดูเหมือนตัวเอกเลือกนอนเอง [A01.L08 t=03:25]
- มุมบนลงแบนซ่อนความวุ่นวาย [A01.L08 t=03:37-03:44]
- AI glitch คลาสสิก: เสื้อผ้าขาดแล้วกลับมาเย็บติดในวินาทีถัดไป [A01.L08 t=04:29-04:36]
- physics ตอนจบผิด: อุปกรณ์หลุดมือ, เสือตกตามลงไป [A01.L08 t=04:52-04:57]
- พื้นหลังมุมย้อนเปลี่ยนทุก generation ถ้าไม่มี reference ห้องสองฝั่ง [A01.L09 t=00:49]
- กล้องข้ามแกนเอง ซูมเอง ตัวละครหายไม่หมด Cindy ย้ายที่ทุก cut [A01.L09 t=02:18-02:27]
- แม้แก้แล้ว บาง batch ยัง drift ต้องรันอีก [A01.L09 t=03:05-03:11]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- Overlay บล็อกบอกบทบาทเครื่องมือ: GPT Image 2 = product sheets/edits/schematic maps; Soul Cinema และ Cinematic Locations = ภาพนิ่งสมจริง; Seedance 2.0 = ฉาก; ไฟล์ skill ชื่อ "higgsfield-seedance-shotlist-director.skill" [A01.L01 frames t=00:50]
- หน้าบทจริงเป็นบล็อก "BEAT N." มี camera language ในบท เช่น "SNAP ZOOM IN: on the island's shore ... lies a DEVICE WITH A BUTTON." [A01.L02 frames t=00:37]
- คำถามของ Claude ขึ้นเป็น bubble: "What runtime are you aiming for?" / "Which settings do you want?" / "Do you want any plot twists?" [A01.L02 t=00:25-00:30]
- การ์ด PRO TIP: "Keep only the close-up face on the character sheet." [A01.L03 frames t=01:25]
- เทียบ take ด้วย overlay แดง (ไฟเกิน, แผนที่ผิดที่, โต๊ะชิดมุม) และเขียว (ตะเกียง + แสงลอดไม้) [A01.L03 t=03:00-03:25]
- ราคาเครดิตบนปุ่ม GENERATE ของทุกโมเดล (28 / 7 / 0.5 / 1,320 / 660 / 176) อ่านได้เฉพาะจาก hires frames [A01.L03 frames t=01:03] [A01.L05 frames t=00:05] [A01.L08 frames t=01:24]
- รายการ skills อื่นที่ผู้สอนติดตั้ง (seedance-clean, seedance-shotlist-director, seedance-footage-vfx, character-sheet, cinematic-workflow-breakdown, seedance-director ฯลฯ) แต่บทความเอ่ยถึงแค่ skill เดียว [A01.L04 frames t=00:19]
- เมนู Add ของ Skills มี "Create with Claude" / "Write skill instructions" / "Upload a skill" [A01.L04 t=00:20]
- คลิปที่เลือกถูกขอบเขียวแล้วลากลง PROJECT TIMELINE [A01.L05 frames t=01:30]
- ข้อความลบ cut ที่พิมพ์จริงบนจอ และ cut ที่ถูกลบคือ POV แบบกล้องสองตาของเรือไกล [A01.L06 t=00:30] [A01.L06 frames t=00:35]
- ภาพวาด top-down ที่แนบเพื่อแก้จุดชน มีวงกลมสีเขียวเป็นตำแหน่งกระทบ [A01.L06 frames t=01:48]
- prompt ที่ Claude เขียนใหม่ในฉากป่ามีส่วน "WARDROBE STATE SWAP — HARD CONTINUITY RULE" (0.0-3.2 s ใช้ @main_character_jungle, 3.2 s เป็นต้นไปใช้ @main_character_jungle_torn) ซึ่งไม่อยู่ในบทความหรือ cue (การอ่านเป็นค่าประมาณ) [A01.L08 t=04:50-04:55]
- การ์ด PRO TIP: "USE BOTH SIDES OF THE LOCATION — CONSISTENT BACKGROUNDS IN EVERY ANGLE." [A01.L09 t=01:15]
- บันทึกการพูดบท: "Two months?! HELL NAHHH!" แบบเรียบ ขุ่นเคือง เสียงตก เป็นการปฏิเสธที่ไม่ใช่ตะโกน; มี HARD CUT ที่ 4.5 s และ 7.0 s [A01.L09 frames t=03:02]
- caption สามข้อท้ายคอร์ส: "ONE FACE PER CHARACTER SHEET", "SEPARATE LOCATION ASSETS FOR COMPLEX SCENES", "REVERSE ANGLES FOR CONSISTENCY" [A01.L10 t=03:40-03:45]
- หน้าตาตัวเอกต่างกันในแต่ละโลก (ผมสั้นในทะเลทราย ผมยาวในป่า) "หนึ่งตัวละคร" จึงถูกถือด้วยเรื่อง ไม่ใช่ทรงเดียวกันเป๊ะ (ข้อสังเกตของผู้จด) [A01.L01 t=02:00-04:00]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- cue recreate ของ character sheet เขียนว่า RED durag และมีทั้ง "21:9" และ "16:9" แต่ output บนจอและ sheet ที่ได้เป็นผ้าโพกหัว YELLOW [A01.L03 cue 3-view-character-sheet-recreate] [A01.L03 t=01:05-01:15]
- คำขอ part 5 บนจอแนบ asset ทะเลทรายเพื่อทำ transition ในกล้อง แต่ prompt สุดท้าย recreate-1-5c จบในฝุ่น "no transition, no new location" และไม่มี reference ทะเลทรายเลย [A01.L06 frames t=02:30] [A01.L06 cue recreate-1-5c]
- recreate-1-3b มี lock อ้าง "CUTS 3 and 5" ทั้งที่มีแค่ 3 cut; recreate-1-4b มี tag ผิดรูป "@[island_location]" [A01.L06 cue recreate-1-3b] [A01.L06 cue recreate-1-4b]
- คำขอพิมพ์ว่า "white macaques" แต่ cue recreate-3-2b บรรยาย "Japanese macaque — thick shaggy grey-brown fur, bare bright-red face" [A01.L08 frames t=03:25] [A01.L08 cue recreate-3-2b]
- recreate-3-3a มี WARDROBE STATE TIMELINE อยู่แล้ว แต่ไม่อ้าง @main_character_jungle_torn [A01.L08 cue recreate-3-3a]
- ฝั่งแกนกล้อง: recreate-4-1a/4-1b/2b ระบุ "TV-wall side" แต่ recreate-4-2a ระบุ "bookshelf-and-doorway side" [A01.L09 cue recreate-4-2a] [A01.L09 cue recreate-4-1b]
- recreate-1-2a และ 1-2b ใช้ recreateJobSetId เดียวกัน ไม่ชัดว่าลิงก์ 1-2b สร้างเวอร์ชัน comedy ได้จริง [A01.L05 cue recreate-1-2b]
- ไม่รู้ชื่อโมเดล Claude แน่ชัด: ตัวเลือกอ่านได้ "Fable 5 · High" จากเฟรมเท่านั้น ไม่มีในเสียงหรือบทความ [A01.L02 frames t=00:12]
- chip "On" (รูปลำโพง) และ "High" (รูปประกาย) ในแถบ Seedance ไม่เคยถูกตั้งชื่อบนจอ การตีว่าเป็น audio on เป็นการเดา [A01.L05 frames t=00:05]
- กฎภายใน ("director hacks") ของ skill ไม่ถูกแสดง เห็นแค่ output [A01.L04 t=00:25-00:30]
- Scene 1 ใช้ "Sequence of cuts, no timecodes" ส่วน Scene 2-4 ใช้ "Timed multishot" แต่คอร์สไม่อธิบายว่าเลือกอันไหนเมื่อไร [A01.L05 cue recreate-1b] [A01.L07 cue recreate-2-1c]
- ไม่มีตัวเลขรวม generation/เครดิตทั้งเรื่อง มีแค่มุก "two weeks and 400 generations later" [A01.L03 t=00:00-00:17]
- ชื่อโปรเจกต์บน breadcrumb สะกด "Blockbaster" ใน L05 แต่ "Blockbuster" ใน L07 (typo ใน UI) [A01.L05 frames t=00:05] [A01.L07 frames t=00:40]
- ตัวละครชื่อ "ADIL" ใน cue recreate-4-1a แต่ "main character" ใน cue หลังจากนั้น [A01.L09 cue recreate-4-1a]

### เทียบกับ v1
- เหมือนเดิม: ลำดับ script → assets → scenes → edit, พื้นเทา, มุม 3/4, ลบหน้าซ้ำ, ชื่อ tag เดียวกันใน Elements [A01.L03 t=05:10-05:26] [A01.L10 t=03:24-03:34]
- แก้: v1 ยกตัวอย่าง tag "@hero" แต่ในคอร์สจริงตัวเอกคือ @eduardo (และ @main_character_desert / @main_character_jungle / @main_character_room ในฉากหลัง) [A01.L03 article] [A01.L07 article]
- เพิ่ม: ชื่อ skill จริง `higgsfield-seedance-prompt` และวิธีติดตั้ง Customize → Skills → + → Upload a skill [A01.L04 t=00:15-00:25]
- เพิ่ม: settings Seedance ครบ (21:9, 4K, 15 s, 4 batches) และราคาเครดิตบนปุ่ม GENERATE ทุกโมเดล ณ วันที่บันทึก [A01.L05 frames t=00:05] [A01.L03 frames t=01:03]
- เพิ่ม: โครง prompt 14 ส่วนของ skill (SCENE CONTEXT ... POSITIVE LOCKS) และ named locks [A01.L05 cue recreate-1b]
- เพิ่ม: บทบาทแยกของ Soul Cinema (raw, 8 ภาพ/credit) กับ GPT Image 2.0 (edit/clean sheet) [A01.L03 t=04:49-04:58]
- เพิ่ม: การเขียนบทด้วย Claude แบบ "expand my idea" แทน "write me a script" [A01.L02 t=00:22]
- เพิ่ม: shot 1 ฉากป่าเป็น 8 s (ไม่ใช่ 15 s) [A01.L08 frames t=01:22]
- เพิ่ม: ส่วนขัดแย้งในตัวคอร์ส (durag สี, axis side, macaque สี, transition ที่หายไป) ซึ่ง v1 ไม่มี [A01.L03 cue 3-view-character-sheet-recreate] [A01.L09 cue recreate-4-2a]
- เหมือนเดิม: v1 สรุป A01.09 ว่าใช้ OTS + เส้น 180 องศา + ล็อกขนาดอุปกรณ์และตำแหน่งนกแก้ว ตรงกับคอร์ส [A01.L09 t=01:23-01:40] [A01.L09 t=02:31-02:50]

## A02 Build an Ultra-Realistic Short Film in 4K

### ภาพรวมและผลลัพธ์
- คอร์ส 19 บทของ Adil ("@ADILINTHEWILD") สร้างหนังดราม่าฟุตบอล "THE MISS" ยาวราว 2 นาที: นักฟุตบอล Santiago เล่าความรู้สึกผิดจากการยิงจุดโทษพลาดให้นักจิตวิทยาฟัง ย้อนไปวัยเด็ก แล้วจบที่เด็กแฟนบอลขอให้สอนลูกเล่น [A02.L01 frames t=00:30] [A02.L02 article] [A02.L02 frames t=00:00]
- หนังทั้งเรื่องทำใน Higgsfield โดยใช้ Claude Fable 5 เขียนบทและ Seedance 2.0 4K ทำทุกช็อต [A02.L01 t=00:33] [A02.L01 article]
- แนวคิดหลัก: อารมณ์มาจากสี มุมกล้อง และการเล่าเรื่อง ไม่ใช่แค่ไอเดีย จึงต้องคิดแบบผู้กำกับ ไม่ใช่แค่ "prompt AI film" [A02.L01 t=00:11] [A02.L01 article]
- เทคนิคที่ไม่มี emotional arc = "demo reel, not a film" [A02.L02 article]
- บทเรียนแรกให้ดูหนังจบหนึ่งรอบแบบผู้ชม จดว่าอะไรทำให้รู้สึก ซึ่งจะกลายเป็น shot list ที่จะเรียนเขียน [A02.L01 article] [A02.L01 t=00:50]
- เสาหลักการกำกับสี่ข้อตอนสรุป: camera movement ที่เขียนไว้ในบท, emotional beats ทีละขั้น, transitions ที่วางแผน, colour palette ต่อช็อต [A02.L19 t=02:18-02:24]
- ผู้สอนสรุปว่าความได้เปรียบคือมอง AI filmmaking "through the lens of psychology and directing" [A02.L19 t=02:36-02:44]

### Workflow ทีละขั้น
1. ดูหนังตัวอย่างจนจบโดยไม่ข้าม แล้วสังเกตการเปลี่ยน stakes สามช่วง (สารภาพในห้อง Dutch angle → ย้อนอดีตจุดโทษและตัวเองตอน 7 ขวบ → คำขอของเด็กตอนจบ) [A02.L02 article]
2. ให้ Claude Fable 5 เขียนบท: premise + อายุ/เบื้องหลังตัวเอก + beat ตอนจบ + "Keep each shot to 15 sec, and about 2 min total" เพราะ 1 ช็อต = 1 Seedance generation [A02.L03 cue script-request] [A02.L03 t=00:07]
3. ดันบทเข้าโครงสี่ส่วน setup / rising action / climax / resolution และระบุ genre (drama) [A02.L03 t=00:47-01:18] [A02.L03 t=01:23]
4. ใช้บทเป็นบัญชีงาน: slugline INT./EXT. = location ที่ต้องสร้าง, ตัวละคร = sheet, พร็อพ = ต้องเรียกออกมาก่อน generate; ผลที่ได้คือ "8 scenes, 1:52 total" [A02.L03 t=01:27] [A02.L04 frames t=00:20]
5. แต่ละฉาก เริ่มจากทำรายการ asset: characters, locations, props [A02.L09 t=00:02-00:16]
6. Character: ขอ prompt sheet 3 แผงพื้นเทาจาก Claude → Cinema Studio new project → วาง prompt → Soul Cinema → 16:9 → 2K → Generate หลายรอบแล้วเลือก [A02.L04 t=00:19-00:58] [A02.L04 t=00:58-01:06]
7. คัดด้วยแสง: นุ่มเกือบไม่มีเงา ไม่มีเงาแข็งบนหน้า ไม่มี glare บนผม มี catchlight ในตา [A02.L04 t=01:06-01:34]
8. ล็อกภาพที่เลือก → Create Element ตั้งชื่อ "Santiago" → Create เพื่อให้ Claude อ้างด้วยชื่อ และ Higgsfield ดึง element อัตโนมัติตอนวาง prompt [A02.L04 t=01:34-01:52]
9. Location: สลับเป็นโหมด Cinematic Locations ตั้ง mood ด้วยคำเรื่องโทนอุ่น/เย็น อากาศ เวลา และเขียน "3/4 angle" ทุกครั้ง แล้วเลือกเฟรมที่ depth สะอาดที่สุด [A02.L05 t=00:01] [A02.L05 t=00:05-00:19] [A02.L05 t=00:33-00:52]
10. ชุด/พร็อพ: ทำ prop sheet ใน Soul Cinema → แก้ระดับคำ (โลโก้ เลข 7 → 23) ด้วย GPT Image 2 แยกรอบ → รวมชุดกับ character sheet ด้วย GPT Image 2 ("Create a character in this uniform") [A02.L09 t=00:22-00:49] [A02.L09 t=00:49-01:25]
11. ติดตั้ง prompt-builder skill: Claude > Customize > Skills > + > อัปโหลด SKILL_prompt_workbench.md [A02.L06 t=00:19-00:30] [A02.L06 article]
12. ต่อฉาก: วางบทใน Claude + แนบ asset + อธิบายฉากทีละช็อต (ตำแหน่งกล้อง การเคลื่อน framing อารมณ์) พร้อม @tag [A02.L06 t=00:44-01:04] [A02.L06 article]
13. วาง output ลง Cinema Studio > Seedance 2.0 > 4K > duration 15 s > Generate (batch 4) โดย Elements แนบให้อัตโนมัติ [A02.L06 t=01:04-01:25] [A02.L08 article]
14. ทบทวน take ทีละ beat: 4/4 พัง = เขียน prompt ใหม่ ไม่ reroll; physics พัง = ทิ้ง; ชนะบางส่วน = เก็บเป็น backup หรือเฟรม [A02.L07 t=00:21-00:25] [A02.L10 t=01:07-01:43]
15. ถ้าอารมณ์แบน ให้ยกระดับกล้อง: แตกช็อตเพิ่ม, Dutch angle + ดันตัวละครชิดขอบ, wide establishing ก่อน, handheld, flare/หมอก, whip pan, speed ramp [A02.L08 t=00:00-00:27] [A02.L10 t=00:37-01:00] [A02.L12 t=00:16-00:30]
16. ประกอบฉากจากช็อตดีที่สุดของแต่ละ generation โดยรักษาเส้น 180° และใช้ match cut (เฟรมสุดท้ายของฉากก่อนเป็น reference ฉากถัดไป) [A02.L08 t=01:15-01:46] [A02.L10 t=00:07-00:22]
17. แก้การแสดงหรือเสียงแยก: generate shot ที่มีแต่ VO พร้อม delivery note แล้ว overlay เสียงบนภาพที่ล็อกแล้ว [A02.L16 t=00:00-00:08]
18. บทพูดแน่นให้แตกเป็น OTS สั้น ๆ พร้อม pause ที่เขียนไว้ และหลัง flashback เว้น 1-2 s [A02.L17 t=00:45-01:12]
19. beat ใหญ่เกิน 15 s ให้ Claude เขียนทั้งฉากแล้วแตกเป็น 8A/8B/8C เลือก take ตามการแสดง แล้ว stitch ทั้งเรื่อง [A02.L18 t=00:02-00:17] [A02.L19 article]

### กฎที่ใช้ซ้ำได้
- 1 ช็อต = 1 Seedance generation 15 s; จำกัดช็อตในบท ≤15 s เพื่อให้รู้จำนวนช็อตก่อนใช้เครดิต (~8 ช็อตสำหรับ 2 นาที) [A02.L03 t=00:07] [A02.L03 article]
- ตัวละครหรือพร็อพที่วนซ้ำทุกตัวต้องมี sheet พื้นเทา + LOCKS block บันทึกเป็น Element ถ้าข้าม sheet ทุก generation จะสร้างคนใหม่ [A02.L04 article] [A02.L09 t=01:57-02:12]
- เกณฑ์คัดหลักคือคุณภาพแสง ไม่ใช่ความเหมือน; sheet ที่มืดหรือ glare จะเป็นพิษกับทุกช็อตตามมา [A02.L04 article] [A02.L04 t=01:06-01:34]
- "CINEMATIC VIDEOS = HIGH-QUALITY IMAGES": วิดีโอดีได้แค่เท่า reference ข้างหลัง [A02.L04 t=01:17] [A02.L04 frames t=01:20]
- Location ต้องมี "3/4 angle" เพราะเห็นสองผนัง ให้ depth และระยะจริงระหว่างวัตถุ; มุมตรงทำให้ผนังแบนเป็นฉากหลัง [A02.L05 t=00:33-00:44]
- ตั้ง palette ใน prompt ทุกครั้งที่เปลี่ยน location หรือตัดไป flashback และให้ชื่อ grade จริง ไม่ใช้คำ mood คลุมเครือ [A02.L09 t=01:37-01:51] [A02.L09 article]
- อย่าให้โมเดลเดียวทั้งออกแบบและแก้ในรอบเดียว แยก generation กับ edit [A02.L09 article]
- ล็อก character sheet = ล็อกเสียง เพราะ Seedance สร้างเสียงเฉพาะตามหน้าตาตัวละคร [A02.L06 t=01:26-01:39]
- ถ้า 4/4 take พัง ปัญหาอยู่ที่ prompt ไม่ใช่ seed [A02.L07 t=00:21-00:25]
- ห้ามใช้ negative prompt กับ Seedance 2.0 เพราะอ่าน "not crying" เป็น "crying"; ให้บอกสภาพที่ต้องการ ("an anxious look") [A02.L07 t=00:33-00:48]
- แก้ครั้งเดียวมักไม่ล้างทุกปัญหา คาดว่า batch ถัดไปจะเจอ failure mode ใหม่ [A02.L07 article]
- "Basic isn't broken": เมื่ออารมณ์อ่านออกแล้ว หยุดจูนอารมณ์ ไปจูนกล้อง [A02.L07 t=01:07]
- การเคลื่อนไหวอย่างเดียวไม่พาอารมณ์ ให้แตกช็อตและใช้กล้องที่มีพลวัต [A02.L08 t=00:00-00:11]
- Dutch angle สร้างความตึงเครียด; ดันตัวละครชิดขอบเฟรมแทบไม่มี looking room ให้รู้สึกติดกับ [A02.L08 t=00:11-00:27]
- ขุดช็อตดีหนึ่งช็อตจากแต่ละ generation แล้วประกอบเหมือนตัด dailies [A02.L08 t=01:15-01:46] [A02.L08 article]
- รักษาเส้น 180° ใน prompt (นักจิตวิทยาจอซ้ายเสมอ นักฟุตบอลจอขวาเสมอ) เพื่อให้ eyeline ต่อกันข้าม cut [A02.L08 article]
- รันที่ 4K เพื่อให้แสง palette flare และหมอกปรากฏจริง ความละเอียดต่ำจะเกลี่ยหาย [A02.L10 t=00:22-00:30]
- Handheld หลีกเลี่ยงลุค "game engine" ของกล้องล็อกนิ่ง [A02.L10 article]
- take ที่ physics พังให้ทิ้งแล้ว reroll อย่าแก้ [A02.L10 article]
- ตัวละครที่ปรากฏครั้งเดียวมักเขียนด้วย text ได้โดยไม่ต้องมี sheet แต่ต้องจำกัดขอบเขต element ของตัวเอกไม่ให้หน้ารั่ว [A02.L11 t=00:21-00:30] [A02.L11 article]
- Seedance ไม่จำตำแหน่งจาก generation ก่อน ให้เปิดคลิปด้วย wide establishing สั้น ๆ แล้วทุกช็อตใน generation นั้นจะคงตำแหน่ง [A02.L12 t=00:04-00:30]
- ภาพใกล้ของอวัยวะให้เขียนแบบ anatomy reference (veins, tendons, knuckle creases, hangnail, uneven nails) ไม่งั้นออกมาเป็นพลาสติก [A02.L12 t=00:38-00:52]
- ประโยคที่พูดไม่จบ ("And I...") ดราม่าและจริงกว่า [A02.L12 t=00:56-01:08]
- ตัดช็อตที่ไม่เพิ่มอะไร แล้วยุบเนื้อหาเข้าช็อตข้างเคียง [A02.L12 t=01:08-01:13]
- เปลี่ยนจังหวะของ take ที่ล็อกแล้วด้วยประโยคเดียว ไม่ต้องเขียน prompt ใหม่ทั้งก้อน; ramp จาก take ที่ล็อกแล้วเท่านั้น [A02.L13 t=00:00-00:07] [A02.L13 article]
- เรียกชื่อเทคนิค ไม่ใช่ mood ("add a speed ramp during the kick" ไม่ใช่ "add more drama") [A02.L13 article]
- Whip pan ต้องระบุ duration และติดป้าย subject A/B/C และต้องเริ่ม-จบที่ shot size เดียวกัน [A02.L14 t=00:26-00:36] [A02.L14 t=01:05-01:13]
- ข้อความบนพร็อพ: ใส่คำเป๊ะใน prompt และค้างช็อตนานพอ (~2 s CU) [A02.L14 t=01:30-01:42]
- แก้ pacing/physics ก่อน แล้วค่อยใส่ performance note ไม่แก้สองอย่างในรอบเดียว [A02.L14 article]
- ทำให้อายุตัวละครด้วยการแนบ sheet ผู้ใหญ่ให้ Claude แปลงเป็นเด็ก แล้วเลือกคนที่เหมือนที่สุด [A02.L15 t=00:09-00:25]
- เปลี่ยนทุก reference ไปทิศเดียวกัน (อายุน้อยลง อุ่นขึ้น หยาบขึ้น) ถ้าแก่/อ่อนแค่ชิ้นเดียวจะดูเป็นคอสตูม [A02.L15 article]
- ภาพล็อกแล้วขาดแค่เสียง: generate shot แยกเพื่อเก็บบรรทัด แล้ว overlay เสียง อย่า reroll ทั้งช็อต [A02.L16 t=00:00-00:08] [A02.L16 article]
- ห้ามกระโดดเข้าบทพูดทันทีหลัง flashback ให้ pause 1-2 s [A02.L17 t=00:45-00:55]
- เลือกตามบรรทัด ไม่ใช่ตาม generation [A02.L17 t=01:17-01:44]
- ตัวละครใหม่กลางเรื่องยังต้องมี character sheet ก่อนทำวิดีโอ [A02.L18 t=01:03-01:13]
- เลือกระหว่าง take ที่สะอาดด้วยการแสดง ไม่ใช่ความเนียน [A02.L18 t=01:30-01:36]

### โครงสร้าง Prompt
- ขอบท: "Help me write a script for a short film about [protagonist + inciting failure] and now [present-day situation/location]. The hero is [age], [backstory duration], [lifelong dream]. At the end, after [main event], [closing encounter]. Keep each shot to [15 sec], and about [2 min] total." [A02.L03 cue script-request]
- Brief ขอ sheet: "write me a prompt for a character sheet on a plain gray background featuring a front view, back view, and a separate close-up headshot of a tired looking 25 year old Latino man with stubble in a casual outfit" [A02.L04 t=00:19-00:33]
- Character sheet prompt: layout line ("three panels side by side, plain gray studio backdrop, thin dark dividers") → panels (front / back / face CU) → identity block → outfit ทีละชิ้นพร้อม palette ซ้ำ → "Lighting: neutral soft even wrap-around, near-shadowless, 5600K, no color cast, readable skin texture, eye catchlights." → "LOCKS: one identical person in all three views ..." [A02.L04 cue character-sheet-prompt]
- Location prompt: "[mood] [style] [room type], shot from a 3/4 angle so two walls of the room are visible ... (not a flat head-on view)." + แหล่งแสง/หน้าต่าง + "Foreground center: [hero furniture, spacing in metres]" + "Behind: ... softly out of focus" + "shallow depth of field, soft bokeh, fine 35mm film grain. No people, no text." [A02.L05 cue office-location-prompt]
- Global Style header ของ skill: Style 8K IMAX photoreal / Cinematography "Lubezki × Deakins" / natural light, contre-jour / "Color: 60:30:10" / physical cine lens, 180° shutter / pore-level skin / Hollywood acting / Physics / rule of thirds / "No identity drift" / 24fps / "Audio: Environmental SFX only. No music. No subtitles." [A02.L06 cue scene-1-two-shot-prompt]
- Element roster: "@<element-id> — [one-line visual description]. 100% matches the reference." ต่อทุกตัวละครและ location [A02.L06 cue scene-1-two-shot-prompt]
- ACTION ต่อช็อต: "[SHOT n] (t0–t1s) — [beat name]" + Subject / First frame (ระยะเป็นเมตร ฝั่งจอ) + micro-beats ①②③ พร้อมบทพูด + Camera (lens mm, ระยะเคลื่อนเป็น cm, "no zoom") + "⚠️After 9s HARD CUT to SHOT 2 — no transition, no fade." [A02.L06 cue scene-1-two-shot-prompt]
- Reaction CU แบบ facial-anatomy timed beats: thousand-yard stare, masseter tightens, swallow, eyes gloss "no tear falls", inhale, blink [A02.L06 cue scene-1-two-shot-prompt]
- คำขอแก้แบบ positive: "Write this without using negative prompts: the character has a dry face with no tears, but his eyes show anxiety, his lips are slightly pursed, and his eyebrows are slightly furrowed. The psychologist's voice should sound gentle and caring." [A02.L07 frames t=00:27-00:33]
- 3-shot Dutch: "THREE SHOTS — static locked-off cameras, all canted Dutch angles, hard cuts at 6s and 10s. The 180° line stays fixed: A always screen-left, B always screen-right" + CAMERA "Dutch tilt ~45° with the LEFT/RIGHT side dipped", 24mm ≈84° FOV, "no fisheye" [A02.L08 cue scene-1-three-shot-prompt]
- Edit แบบเจาะจง: "Change the [element], and swap the [old value] to [new value]" [A02.L09 cue gpt-logo-swap]
- รวม asset: "Create a character in this [uniform]. Make him [grooming changes], looking [fresh]." พร้อมแนบสองภาพ [A02.L09 cue combine-kit-and-sheet]
- Prop sheet ของซ้ำ: SUBJECT (สเปกจริง ขนาด cm วัสดุ) / VIEW (45° three-quarter) / BACKGROUND (mid-grey ไม่มี props/text) / LIGHTING (WB 5600K) / COLOR (60:30:10 พร้อม %) / STYLE (8K product photo, NO 3D render) / CONSTRAINTS ("NOT oversized", "4:3 sheet") [A02.L09 cue ball-prop-sheet]
- Location reference ขอบเขต: "LOCATION REFERENCE ONLY (use for look, materials, scale and layout — not a keyframe, do not copy its composition)" [A02.L10 cue scene-2-match-cut-prompt]
- Override plate ว่าง: "CRITICAL: the stands are COMPLETELY FULL ... if the location reference plate shows the stands empty or sparse, IGNORE that and fully populate the stands" [A02.L10 cue flares-fog-handheld]
- Scope ตัวเอกเมื่อมีคนแปลกหน้า: "Used ONLY as the distant player ... his face and identity must NOT transfer" + "COMPLETELY DIFFERENT PERSON" [A02.L11 cue grandfather-prompt]
- FIRST FRAME / BLOCKING ใช้พิกัดจอ: "tight on X, face center, x50% y46%, head slightly bowed..." และระบุ stress ของบทพูด ("stress lands on 'missed'") [A02.L12 cue scene-3-close-up]
- 3-shot establish: "THREE SHOTS — wide establish, his nervous hands, then a 3/4 lips-rising-to-the-eyes confession from his shadow side. Hard cuts at 1.5s and 3.5s" [A02.L12 cue establish-and-hands]
- Single take สุดขั้ว: "ONE CONTINUOUS SHOT ... SUPER HANDHELD ... 3–6cm tremor, fast reactive whip-pans that lag then snap..." + LAYOUT "lock all positions" + beats 0-4 / 4-7 / 7-11 / 11-15 s + "REAL TIME ... NO slow-motion, NO speed-ramp" [A02.L13 cue speed-ramp-prompt]
- Speed ramp ต่อจาก take ล็อก: "Add slow-mo with a speed ramp during the kick" [A02.L13 t=01:06-01:13]
- Whip pan: "WHIP-PAN: A settled until ~0.3s before the move; then a fast motion-blur whip ~0.5s ... B settles in frame by ~1.4s" + camera "planted directly between the two ... pivoting on the spot" [A02.L14 cue whip-pan-prompt]
- ข้อความอ่านได้: "Remake shot [n] as a close-up where she writes in a notebook. I need her to write these exact phrases: "[line 1]", "[line 2]", "[line 3]". [camera angle]" [A02.L14 cue readable-text-fix]
- Sheet เด็ก: "CHARACTER SHEET — [NAME], AGE [n] (3 VIEWS, GRAY BACKDROP)" + identity + ชื่อ/เลขทาสีด้วยมือ ("clearly done by hand ... not printed") + LOCKS "No extra people, no other text, no props, no cropping" [A02.L15 cue young-santiago-sheet]
- Location ยุคเก่า: "Photoreal, 8K, cinematic. An empty [place] in a [region/class] [setting]: ... [warm golden-hour light, low sun, haze, long shadows, faded sun-bleached palette]. Empty, no people. No text other than incidental graffiti." [A02.L15 cue vintage-location]
- พร็อพเก่า: วัตถุ + ขนาด บนพื้นเทา + aging list (yellowed, scuffed, cracked seams, under-inflated, "kicked around for years") + ไฟ studio ด้านหน้าให้เห็นรอย [A02.L15 cue old-ball-prop]
- VO capture: "I need to generate a separate scene of [character] talking in [location]: '[exact line]'. With [pause pattern], [emotion], and [voice quality]." [A02.L16 cue voice-over-line]
- แตกบทพูด: "THREE SHOTS — a half-second wide to anchor the seating, then an over-the-shoulder eight. Static locked-off, eye-level, level and un-canted, hard cuts at 0.5s and 5s" และเขียน pause ลงใน beat ("'Eighteen years —' then a held pause '— and one second.'") [A02.L17 cue split-the-dialogue]
- Brief สั้นต่อช็อต: "[shot id] is up first. The idea here is that after [prior event], [character] is [action/location] when [inciting object event]. He [reaction action] and [looks around]." [A02.L18 cue scene-8-ask]
- 8B: "Composition: ASYMMETRIC framing in EVERY beat ... never centered" + token ชื่อ (FAN_KID, SANTIAGO "silhouetted torso/hands only, silent, no face") + "LOCATION — ... STYLE REFERENCE ONLY ... Model extends the world" + บทพูดมีการลังเล ("Uhh— you're... Santiago?") + "[AUDIO] NO MUSIC. SFX ONLY" [A02.L18 cue kid-fan-sheet]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Claude (claude.ai) ตัวเลือกอ่านได้ "Fable 5 High" ใช้เขียนบทและทุก prompt [A02.L03 frames t=00:38] [A02.L08 frames t=00:46]
- Soul Cinema (image): 16:9, 2K, บนจอแสดง "-0.25 CREDITS" ต่อ generation (ผู้สอนพูดว่า "less than half a credit") [A02.L04 t=00:50-01:02] [A02.L04 frames t=01:00]
- Cinematic Locations: แถบแสดง Image mode / "Cinematic Locations" / "4K" / "10/10" [A02.L05 frames t=00:31]
- GPT Image 2 สำหรับแก้โลโก้/เลขและรวมชุด: "GPT Image 2" | "16:9" | "High" | "4K" | "1/4" = GENERATE 12 credits [A02.L09 frames t=00:57] [A02.L09 frames t=01:16]
- GPT Image 2 สำหรับ ball prop sheet และ old ball: "16:9" | "High" | "4K" | "4/4" = 48 credits [A02.L09 frames t=02:09] [A02.L15 frames t=01:13]
- Seedance 2.0 แถบ Video mode: "16:9" | "4k" | "15s" | "3/4" | audio "On" | "High"; ปุ่ม GENERATE แสดงราคาขีดฆ่า (อ่านคล้าย "1,170") และ "990" [A02.L06 frames t=01:14]
- Seedance 2.0 ใช้ 4K, 15 s, batch 4 ทุกฉาก และสร้างเสียงตัวละครอัตโนมัติจาก sheet [A02.L06 article] [A02.L18 t=01:13-01:26]
- Higgsfield Cinema Studio (หน้า Explore แสดง "Cinema Studio 3.5"), Create Element มีช่อง name, description, Category "Auto" และ project tag [A02.L04 frames t=00:40] [A02.L04 frames t=01:35]
- Skill file: SKILL_prompt_workbench.md ("Prompt-builder skill") [A02.L06 article]
- Nano Banana Pro ถูกเอ่ยในบทความ L11 เท่านั้นว่าข้ามได้สำหรับตัวละครครั้งเดียว ไม่ได้ใช้บนจอ [A02.L11 article]
- ค่าที่ปรากฏใน cue: WB 4800K-5600K, haze ~10%, lens 24mm WS / 50mm / 85mm / 100mm CU, tremor 1-2 cm (handheld) ถึง 2-4 cm และ 3-6 cm (super handheld) [A02.L08 cue scene-1-three-shot-prompt] [A02.L10 cue flares-fog-handheld] [A02.L11 cue grandfather-prompt] [A02.L13 cue speed-ramp-prompt]
- 8B prompt ระบุ ARRI Alexa, WB 5500K, real time [A02.L18 cue kid-fan-sheet]
- Script resource: SCREEN_FINAL_SANTIAGO.pdf [A02.L03 article]

### คำเตือนและ failure modes
- ข้ามบทแล้วจะต้อง improvise asset ทีละฉาก [A02.L03 article]
- ส่วนใหญ่ใน batch ตกเพราะแสง ไม่ใช่ความเหมือน; ตัวอย่างที่ถูกคัดทิ้ง: หน้าซีกซ้ายมืดเกิน + glare แรงบนผม, หน้ามืดเกิน [A02.L04 article] [A02.L04 t=01:23-01:34]
- เก้าอี้ตัวที่สามโผล่มาเอง, ท่านั่ง "man spread", ไม่มีพลวัต มุมน่าเบื่อ การแสดงแย่ [A02.L07 t=00:01-00:20]
- batch ที่สอง: สัดส่วนเพี้ยน, location เปลี่ยน, วัตถุเกิน, ตัวละครชิดกันเกิน [A02.L07 t=00:51-01:01]
- Seedance ทำ composition ได้แต่ทิ้ง micro-action (ไม่เคาะเท้าตามสั่ง) [A02.L08 t=01:00-01:15]
- ไม่มี generation 15 s ไหนให้ครบ 3 ช็อตสะอาด [A02.L08 article]
- ทำผิดเส้น 180° แล้วตัวละครทั้งสองมองทิศเดียวกันบนจอ [A02.L08 article]
- ท่ากระโดดผู้รักษาประตูแปลกและช็อตตัดเร็ว; ผู้เล่นหายไปใน wide [A02.L10 t=01:07] [A02.L10 t=01:16]
- ถ้าไม่ scope element ตัวเอก โมเดลอาจยืมหน้าตัวเอกให้ตัวประกอบ; text-only extra "usually get away with" ไม่รับประกัน [A02.L11 article] [A02.L11 t=00:25]
- มือออกมาเรียบเป็นขี้ผึ้ง ("plasticky and too perfect") ถ้าไม่สะกด anatomy [A02.L12 t=00:38]
- ขอ speed ramp โดยไม่มีช็อตล็อกก่อน โมเดล "no beat to ramp around" [A02.L13 article]
- ไม่มี duration และป้าย subject ใน whip pan แล้ว Seedance จะ drift เวลาหรือหลงว่าใครอยู่บนจอ [A02.L14 article]
- ความต่อเนื่องอารมณ์แตก: ยิ้มทันทีหลังร้องไห้ [A02.L14 t=00:40]
- พูดก่อนกล้องหมุน บทพูดจึงซ้ำ [A02.L14 t=00:57-01:04]
- ลายมือในสมุดออกมาเป็นขีดเขี่ย ("AI slop") ดูเร็ว ๆ จะพลาด [A02.L14 t=01:30-01:37]
- แก่/อ่อนแค่ asset เดียว flashback จะดูเป็นคอสตูม [A02.L15 article]
- delivery แบน = ท่องบท [A02.L16 article]
- บทพูดเยอะใน take 15 s เดียวดูรีบ ผู้ชมไม่มีเวลาซึมซับ [A02.L17 t=00:21-00:28]
- 8A ตกเพราะ eye tracking ตาวอกแวก "all over the place" [A02.L18 t=00:30-00:40]
- โมเดลที่ต้องใช้ 3-4 batch เพื่อ take สะอาดหนึ่งอัน ยังไม่พร้อมสำหรับฉากแน่น [A02.L18 article]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- บทพูดเต็มของหนัง (บทความอ้างแค่บางส่วน) เช่น "Guilt." / "18 years and one second." / "Please, teach me your tricks." / "Haven't played in a long time." [A02.L02 t=00:31] [A02.L02 t=01:17] [A02.L02 t=02:00-02:04]
- Claude ตอบบทว่า "Here's the script — 'Santiago,' 8 scenes, 1:52 total" และอธิบายว่าฉาก 2 ตัดก่อนวิ่ง ส่วนการยิงพลาดเห็นแค่ในฉาก 4 [A02.L04 frames t=00:20]
- โน้ตของ Claude บนจอ: ถ้าภาพด้านหลังประดิษฐ์ทรงผมใหม่ ให้เพิ่ม "same curl pattern visible from behind" ใน LOCKS; ลายกราฟิกยุ่งให้เปลี่ยนเป็น "subtle marbled print" เพราะ "busy patterns are the most common consistency breaker in multi-panel sheets" [A02.L04 frames t=00:35]
- swatch พื้นเทาบนกราฟิกตัวอย่างอ่านได้ราว "#CDCDCD" (ตัวเลขไม่ชัดเล็กน้อย) [A02.L04 frames t=00:05]
- demo mood: ห้องของผู้สอนถูก render ใหม่ให้หน้าต่างมีหิมะ เพื่อแสดงว่าคำเรื่องอากาศเปลี่ยน mood [A02.L05 frames t=00:15]
- ชื่อหัวข้อในไฟล์ skill ที่เห็นบนจอคล้าย "ASSET TAGGING" และ "CONTEXT ISOLATION" (อ่านไม่ชัด) [A02.L06 frames t=00:00]
- แนบ asset เป็นภาพแล้ว map ด้วยลำดับ: "@Santiago is 1 photo, main character; @psychologist 2 photo, @office is the location (3 photo)" [A02.L06 frames t=00:55]
- การ์ด "PRO TIP: LOCK THE CHARACTER SHEET = LOCK THE VOICE" [A02.L06 frames t=01:35]
- คำขอแก้บนจอระบุ choreography ของสายตาละเอียด (มองพื้น → เงยขึ้นเมื่อถูกถาม → CU → เหลือบข้าง) ซึ่งบทความไม่มี [A02.L07 frames t=00:27-00:33]
- กราฟิก "SEEDANCE 2.0 / POSITIVE / ~~NEGATIVE~~" [A02.L07 frames t=00:35]
- ผู้สอนเอียงกล้อง talking-head ของตัวเองสาธิต Dutch angle; caption "SCENE 1/8 LOCKED" [A02.L08 frames t=00:15] [A02.L08 frames t=02:10]
- ราคาเครดิต GPT Image 2 (12 และ 48) อ่านได้จาก hires frames เท่านั้น [A02.L09 frames t=00:57] [A02.L09 frames t=02:09]
- ท้าย prompt สนามบนจอมีรายการ "NO people, NO crowd, NO match, NO daylight ... NO neon, NO real logos, NO readable text." [A02.L09 frames t=02:05]
- ภาษาในคำขอปู่แฟนบอลบนจอคือผ้าพันคอเขียน "SANTIAGO" และ "hope and anxiety" ต่างจาก cue ("hope and belief") [A02.L11 frames t=00:10]
- นักจิตวิทยา reaction shot เพื่อ pacing มีแต่ในเสียงพูด ไม่มี cue หรือบทความ [A02.L12 t=01:45-01:55]
- ผู้สอนพูดถึงหนัง AI ที่นำเสนอที่ Cannes [A02.L13 t=00:19]
- checklist ครึ่งคอร์ส: "✓ HOW TO BUILD THE ASSETS / ✓ THE FULL WORKFLOW / ✓ THE MAIN CAMERA MOVES" [A02.L13 frames t=01:35]
- คำขอแก้บริบทฉาก 5 บนจอเปลี่ยนดีไซน์ช็อตด้วย (CU มือนักจิตวิทยาเขียนสมุด แล้ว medium ตอนถาม แบ่งคำตอบรอบ micro-pause) บทความเอ่ยแค่ "shaky, red-eyed, no smile" [A02.L14 frames t=00:45]
- การ์ด "FIX #1 - ADD THE PAUSE / FIX #2 - SPLIT THE SCENE" [A02.L17 frames t=01:05]
- กราฟิก "SCENE 8 → 8A / 8B / 8C" [A02.L18 frames t=00:10]
- sheet เด็กแฟนบอลใส่เสื้อยืดกากี แต่ใน 8B ใส่ชุดฟุตบอล maroon/pink ซึ่งมาจาก prompt [A02.L18 t=01:05-01:30]
- overlay สรุป "1. CAMERA MOVES / 2. EMOTIONS / 3. TRANSITIONS" มีแค่สามข้อ แต่เสียงพูดมีข้อสี่คือ colour palette [A02.L19 t=02:20-02:24]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- Aspect ratio 16:9 vs 21:9: เสียงพูดและบทความบอกตั้ง Seedance 16:9 และ chip บนแถบอ่าน 16:9 แต่ทุก cue prompt และ recreate URL ระบุ 21:9 ไม่รู้ว่าหนังจริงใช้อันไหน [A02.L06 t=01:09-01:18] [A02.L06 frames t=01:14] [A02.L13 frames t=00:10]
- ใน cue ฉาก 1: hard cut "After 9s" ใน ACTION แต่ "one hard cut at 8s" ใน CONSTRAINTS [A02.L06 cue scene-1-two-shot-prompt]
- cue ฉาก 1 บอก Santiago ใส่ "dark-olive crew-neck t-shirt and black jeans" ขัดกับ sheet ที่ล็อก (camp shirt) [A02.L06 cue scene-1-two-shot-prompt]
- กฎห้าม negative ใช้กับ Seedance แต่คำขอของผู้สอนเองยังมี "dry face with no tears" และ cue ที่แก้แล้วยังมี "far from smooth or perfect" [A02.L07 frames t=00:27-00:33] [A02.L12 cue establish-and-hands]
- prompt ภาพนิ่งของ Claude (kit, ball, stadium) ใช้รายการ "NO ..." หนัก ขัดกับกฎ no-negatives (ซึ่งระบุไว้สำหรับ Seedance เท่านั้น) [A02.L09 frames t=02:05] [A02.L09 cue ball-prop-sheet]
- ball prop sheet: cue ระบุ 4:3 แต่ chip บนแถบอ่าน 16:9 [A02.L09 frames t=02:09]
- ชุดผู้รักษาประตู: cue L10 เขียน "green Brazil-style goalkeeper kit" แต่ sheet และ take เป็นสีเหลือง; cue L13 เพิ่ม "do NOT make it green" (น่าจะแก้ drift แต่เป็นการอนุมาน) [A02.L10 cue flares-fog-handheld] [A02.L13 cue speed-ramp-prompt]
- speed ramp: เสียงพูดบอก snap กลับ "the moment it hits the net" แต่บทความและ cue บอกผู้รักษาประตูเซฟได้ [A02.L13 t=00:55] [A02.L13 cue speed-ramp-prompt]
- ลูกบอลในฉาก 4 มีกราฟิกฟ้า/แดง ไม่ใช่ prop ขาว/graphite/แดงจาก L09 [A02.L13 frames t=00:25-00:35]
- ข้อความในสมุด: cue และบทความระบุ "Self-blame, unresolved" แต่เฟรมในหนังอ่านได้แค่ "Self-blame" [A02.L14 frames t=01:40] [A02.L02 frames t=00:45]
- บทความ L16 เรียกช็อต action ว่า "20-second shot" ขัดกับ 15 s ที่ใช้ทุกที่ [A02.L16 article]
- cue split-the-dialogue รวมเวลาได้ 10 s ไม่ใช่ 15 s [A02.L17 cue split-the-dialogue]
- ชื่อช็อตสุดท้าย: L18 เลือก take ที่สามของ 8B แล้วพูด "create scene 8C"; วิดีโอใน L19 ชื่อ "scene-8c-fan-kid-final-shot" แต่ asset hash ตรงกับ take 8B; ส่วนหน้ายิ้มของ Santiago ในหนังขัดกับ 8B ที่ห้ามโชว์หน้า จึงไม่ชัดว่ามี 8C แยกหรือไม่ [A02.L18 t=01:32-01:39] [A02.L19 article]
- cue "kid-fan-sheet" จริง ๆ บรรจุ video prompt ของ 8B ไม่ใช่ prompt ของ sheet [A02.L18 cue kid-fan-sheet]
- ไม่ทราบเครื่องมือตัดต่อ/stitch และ overlay เสียง เพราะไม่เคยแสดง [A02.L08 t=01:43-01:46] [A02.L16 t=00:46-00:51]
- ไม่ยืนยันว่า sheet เด็กและ location ใน L15 ใช้ Soul Cinema (chip ไม่อยู่ในเฟรม) [A02.L15 frames t=00:10]
- PromptBox ของคำขอ establish+hands ในบทความว่างเปล่า มีแค่ crop บนจอ [A02.L12 frames t=00:35]
- prompt ของ sheet เด็กแฟนบอล, 8A, 8C และวิดีโอฉาก 6 บอกว่า "in the description" แต่ไม่มีใน cues [A02.L18 t=01:08-01:13] [A02.L15 frames t=01:25]
- ไม่มีตัวเลขเครดิตรวมของหนัง [A02.L04 t=01:02]
- บทพูดฉากถนนตอนจบไม่ถูกถอดเสียงใน L19 รู้ได้จาก L02 และ cue L18 เท่านั้น [A02.L19 article] [A02.L02 t=01:53-02:04]

### เทียบกับ v1
- เหมือนเดิม: โครง setup / rising / climax / resolution, sheet พื้นเทาแสงนุ่ม, location มุม 3/4 เห็นสองผนัง, Dutch angle + เส้น 180° [A02.L03 t=00:47-01:18] [A02.L05 t=00:33-00:44] [A02.L08 t=00:11-00:27]
- เพิ่ม: กฎ "ห้าม negative prompt กับ Seedance" ซึ่ง v1 ไม่มี [A02.L07 t=00:33-00:48]
- เพิ่ม: กฎ 4/4 พัง = prompt ผิด ไม่ใช่ seed และ "Basic isn't broken" [A02.L07 t=00:21-00:25] [A02.L07 t=01:07]
- เพิ่ม: เหตุผลเรื่อง establishing shot คือ Seedance ไม่จำตำแหน่งข้าม generation [A02.L12 t=00:04-00:30]
- เพิ่ม: ตัวเลข whip pan (A นิ่งถึง -0.3 s, whip ~0.5 s, B นิ่งภายใน +1.4 s) และกฎ shot size เดียวกัน [A02.L14 cue whip-pan-prompt] [A02.L14 t=01:05-01:13]
- เพิ่ม: ราคาเครดิตที่เห็นบนจอ (Soul Cinema -0.25, GPT Image 2 12/48, Seedance 990 ขีดฆ่า ~1,170) ณ วันบันทึก [A02.L04 frames t=01:00] [A02.L09 frames t=02:09] [A02.L06 frames t=01:14]
- เพิ่ม: ชื่อไฟล์ skill SKILL_prompt_workbench.md และวิธีติดตั้ง [A02.L06 article]
- แก้: v1 A02.06 บอกว่าเสียงประจำตัว "ต้องฟังผลจริงทุกครั้ง" ซึ่งเป็นความเห็นของ v1; ในคอร์สผู้สอนแค่ยืนยันว่า lock sheet = lock voice ไม่ได้พูดเรื่องตรวจเสียง [A02.L06 t=01:26-01:39]
- แก้: v1 A02.09 เรียกสัดส่วนสีว่า "แนวทางออกแบบของตัวอย่าง" ในคอร์สจริงเขียน 60:30:10 พร้อม % บทบาทลงใน prompt โดยตรง [A02.L09 cue ball-prop-sheet]
- เพิ่ม: รายการความขัดแย้งในคอร์ส (16:9 vs 21:9, ชุดเขียว/เหลือง, ลูกเซฟ/เข้าประตู, 8B/8C) [A02.L06 frames t=01:14] [A02.L10 cue flares-fog-handheld] [A02.L13 t=00:55]
- เหมือนเดิม: แยก VO แล้วนำมาแทนเสียงใน edit, เว้นจังหวะหลัง flashback, แตกฉากสุดท้ายเป็นสามช็อต [A02.L16 t=00:00-00:08] [A02.L17 t=00:45-00:55] [A02.L18 t=00:02-00:17]

## A03 Add AI VFX to Real Footage

### ภาพรวมและผลลัพธ์
- คอร์ส 11 บท (ผู้สอนบนจอ @ADILINTHEWILD) สอนท่าเดียวที่ใช้ซ้ำทั้งคอร์ส: ใส่คลิปจริงที่ถ่ายเองเข้า Seedance 2.0 ใน Higgsfield + ประโยคเดียวบอกสิ่งที่จะเปลี่ยน ได้ช็อตเดิมที่การเคลื่อนไหว หน้า และกล้องยังคงอยู่ เปลี่ยนเฉพาะส่วนที่สั่ง [A03.L01 article] [A03.L01 t=01:16]
- เป็น video-to-video ล้วน ไม่มี keyframing, masking, tracking หรือ rotoscoping [A03.L01 article]
- แบ่งเป็นสามระดับ: Level 1 เปลี่ยนโลกรอบตัว, Level 2 เปลี่ยนองค์ประกอบเดียวในเฟรม, Level 3 handheld cinematic showcase [A03.L01 t=01:31-01:45] [A03.L01 article]
- ผู้สอนบอกว่าทำโดยไม่มีประสบการณ์ VFX: "I just shot it, prompted it, and that was it" [A03.L01 t=01:02-01:08]
- เครื่องมือเขียน prompt คือ Claude + Seedance prompting skill ฟรีจากคำอธิบายวิดีโอ [A03.L01 t=01:52] [A03.L11 t=00:34-00:40]
- กฎห้าข้อตอนสรุป: keep a real anchor, watch your edges, respect parallax, change one thing at a time, shoot for 4K [A03.L11 article]
- คำแนะนำสุดท้าย: ลองกับ footage ของตัวเองและเริ่มจากกรณีง่ายสุด คือเพิ่มวัตถุข้างหลังตัวเอง [A03.L11 article]

### Workflow ทีละขั้น
1. วางแผนก่อนถ่าย: ตัดสินใจว่าคลิปจะกลายเป็นอะไร แล้วถ่าย move จริง (เดิน ขับรถ monkey bars ลงบันได) โดยคิดถึงโลกนั้นไว้แล้ว [A03.L07 t=00:23-00:27] [A03.L08 t=00:00-00:06]
2. ถ่ายด้วยกล้องธรรมดาและให้มี anchor จริงหนึ่งอย่างในเฟรม (หน้า มือ dashboard) [A03.L01 article] [A03.L11 t=00:21-00:27]
3. ถ้าต้องการดีไซน์เฉพาะ ให้ออกแบบสัตว์/พร็อพเป็นภาพนิ่งก่อน (ในคอร์สใช้ GPT Image 2.0) [A03.L06 t=00:07-00:19]
4. ใน Claude แนบคลิป (และภาพ reference ถ้ามี) แล้วเปิด Seedance skill; Claude อ่านวิดีโอเป็นชุดเฟรม [A03.L02 t=00:21-00:34] [A03.L06 t=00:20-00:26]
5. พิมพ์คำขอประโยคเดียวแบบธรรมดา บอกเฉพาะสิ่งที่จะเปลี่ยน ผูกกับจังหวะการแสดง [A03.L02 t=00:35-00:42]
6. ถ้าต้องการหลายเวอร์ชัน ขอหลาย prompt ในคำขอเดียว keep-list เดิมจะถูกใช้ต่อ [A03.L03 t=00:16-00:21]
7. อ่าน prompt ที่ skill เขียน โดยเฉพาะ keep-list และ "honest flags" ท้าย prompt [A03.L02 t=00:49-00:59] [A03.L10 article]
8. ใน Higgsfield เปิด Seedance 2.0 ที่ 16:9, 4K แนบคลิปดิบ (อ้างด้วย `@source`) วาง prompt แล้วกด GENERATE ได้หลาย prompt ในคิวเดียว [A03.L03 t=00:33-00:37] [A03.L07 t=00:40-00:45]
9. ดูผลบนจอใหญ่ ตรวจหน้า (โดยเฉพาะ relight กลางคืน) แสง เงาสัมผัส และ parallax [A03.L01 t=00:37] [A03.L10 cue kraken]
10. ถ้า mood หลุด ให้เพิ่มภาพ environment เป็น mood-only reference แทนการเพิ่มคำ [A03.L10 cue kraken] [A03.L10 article]
11. ในการตัดต่อ ใช้ native 4K punch in เพื่อดึง 2-3 ช็อตจาก generation เดียว [A03.L01 article]

### กฎที่ใช้ซ้ำได้
- เก็บ anchor จริงหนึ่งอย่างไว้ในเฟรมเสมอ; เปลี่ยนทุกอย่างพร้อมกันสมองจะ "smell fake" [A03.L01 article] [A03.L11 article]
- Keep-list คือ anchor ที่เขียนลงกระดาษ: อะไรอยู่ในรายการถูกปกป้อง ที่เหลือเปลี่ยนได้ [A03.L02 article]
- ผูกการเปลี่ยนกับจังหวะการแสดง (ดีดนิ้วที่ ~2.2 s, บทพูด "transform myself", หันหัวที่ 2-3 s) ไม่ใช่ใส่ตอนสุ่ม [A03.L02 article] [A03.L05 cue hand-to-snake] [A03.L09 cue sauropods]
- ซ่อนการตัดไว้ใน light event: แดดย้อนบานเป็น flare ขาว พอจางโลกใหม่ก็มาแล้ว [A03.L02 cue desert-swap]
- คง key light ทิศและคุณภาพเดิมในโลกใหม่ ให้แสงบนตัวคนแทบไม่เปลี่ยน [A03.L02 cue desert-swap]
- กล้องเคลื่อนเร็ว โลกใหม่ต้องตามการเคลื่อนและ relight; ขยาย keep-list ให้ใหญ่ตามช็อต (subject, face, car, seatbelt, rig framing, camera position, driving motion) [A03.L03 t=00:07-00:30]
- โลกใหม่สืบทอดการเคลื่อนจริงจาก plate ทำให้ parallax ถูกเองโดยไม่ต้องอนิเมตด้วยมือ [A03.L03 article]
- ให้ Seedance ดึงแสงจากโลกที่สร้าง (neon บนรถ, ลาวาใต้คาง) แทนการ grade [A03.L03 t=00:37-00:50]
- แหล่งแสงที่เพิ่มต้องส่องตัวคน: ไฟต้องส่องหน้า เสื้อ และสีรถ ไม่งั้นดูเป็นสติกเกอร์ [A03.L04 article] [A03.L04 t=00:56-01:01]
- prompt ส่วนใหญ่ใช้ปกป้องการแสดง ส่วนน้อยบรรยายเอฟเฟกต์ ให้ลอกสัดส่วนนี้ [A03.L04 article]
- จำกัดเอฟเฟกต์ไม่ให้ทำลายองค์ประกอบ: "The hair burns but holds its shape and silhouette, never charring away" [A03.L04 cue head-on-fire]
- มือไม่มีที่ให้ผิด จึงจำกัดการเปลี่ยนให้เหลือองค์ประกอบเดียว [A03.L05 article]
- แยกซ้าย-ขวาให้ชัด: "his right hand — the one on the left side of frame from the viewer's perspective" [A03.L05 cue hand-to-snake]
- ใส่ anti-edit lock: "Do not re-frame, re-time, re-light or re-cut." [A03.L05 cue hand-to-snake]
- กำหนดความเร็ว transition เป็นคำ และ deadline ผูกกับท่าทาง ("by the moment he closes that hand into a fist, the hand is already a snake") [A03.L05 cue hand-to-snake]
- สิ่งที่เพิ่มต้องมีเจตจำนงของตัวเอง ไม่ mirror ร่างกาย ไม่งั้นดูเป็นกราฟิกแปะ [A03.L05 article] [A03.L05 t=00:34-00:38]
- ถ้ารู้ดีไซน์ที่ต้องการแน่ชัด ให้ "show, don't tell" ด้วยภาพ reference และ scope ว่าใช้แค่รูปลักษณ์ ไม่เอา background และแสง [A03.L06 t=00:07-00:19] [A03.L06 cue lizards-climbing]
- ขอ camera move ที่ไม่ได้ถ่ายจริงเพื่อ reveal (telephoto แน่นแล้ว zoom ออกกลับ framing เดิม) และกำหนด snap-back เป็น "a 100% match of the original framing" [A03.L06 t=00:26-00:37] [A03.L06 cue lizards-climbing]
- ใส่บทพูดตรงตัวใน prompt เพื่อยึด lip-sync [A03.L06 cue lizards-climbing]
- generation เดียวให้สองช็อต (telephoto เปิด + wide เดิม) [A03.L06 article]
- Handheld: transfer motion และกล้องแบบ 1:1 "Do not reinterpret or re-describe any of it" และระบุรายการที่อนุญาตให้เปลี่ยน [A03.L07 cue wing-walker]
- อ่านการเคลื่อนเดิมใหม่ในบริบทใหม่ แทนการประดิษฐ์ action ใหม่ [A03.L07 cue wing-walker] [A03.L10 cue kraken]
- ระบุพร็อพแน่นเพื่อลดความรก (harness "not heavily rigged", สีเดียวเป็น hex #d1fe17 "with no patterns or livery") [A03.L07 cue wing-walker]
- ขอ physics ที่ฉากต้องการแม้ต้นฉบับไม่มี (ลมพัดผมและสูท) ซึ่งผู้สอนยกว่าเป็นตัวขายช็อต [A03.L07 article] [A03.L07 t=00:52-01:00]
- Map วัตถุจริงหนึ่งต่อหนึ่งกับวัตถุโลกใหม่ (rig → iron rungs, พื้น → chasm, บันได → ดาดฟ้า, ราว → rigging) [A03.L08 cue jungle-temple] [A03.L10 cue kraken]
- ยิ่งการเคลื่อนจริงอยู่นิ่ง สภาพแวดล้อมยิ่งเปลี่ยนได้อิสระ [A03.L08 article]
- หน้าที่ของผู้ใช้คือชัดว่าต้องการอะไร skill เขียน prompt ยาวให้ [A03.L08 t=00:20-00:30]
- ซ่อนและให้สเกลสัตว์ด้วยบรรยากาศ: หมอก ลำต้น โผล่บางส่วน "never see a whole crisp creature", aerial perspective [A03.L09 cue sauropods] [A03.L09 article]
- น้ำหนักขายสัตว์ยักษ์: ช้า หนัก เคลื่อนน้อย ห้ามเร็ว ลอย ยาง หรือวนซ้ำ [A03.L09 article] [A03.L09 cue sauropods]
- สัตว์หลายตัวต้องเป็นสายพันธุ์และรูปหัวเดียวกันทุกตัว [A03.L09 cue sauropods]
- ป้องกันหน้าคนจากการถูก AI ทำให้เรียบ: "real human skin with pores, stubble ... never waxy, smoothed or warped" [A03.L09 cue sauropods]
- เปลี่ยนเสื้อผ้าให้ระบุว่าคลุมหมด ไม่ให้ตัวเดิมโผล่ ("so no striped shirt shows") [A03.L09 cue sauropods]
- โชว์สเกลด้วยการกั๊ก: ไม่เคยโชว์ตัว kraken เต็ม มีแต่หนวด บางเส้นอยู่ไกลเพื่อสเกล [A03.L10 cue kraken]
- ยิ่ง spectacle ใหญ่ ยิ่งพึ่ง anchor จริงหนึ่งอย่าง [A03.L10 article]
- Watch your edges: เอฟเฟกต์อยู่หลังขอบและมีเงาสัมผัสจริง ไม่แปะทับแบบสติกเกอร์ [A03.L11 article]

### โครงสร้าง Prompt
- รูปแบบคำขอที่ใช้ซ้ำ: "Seedance prompt for this clip — [describe your action + camera type]. Lock my action and the camera exactly. Turn it into [new world], me as [role]." [A03.L08 frames t=00:10]
- คำขอสวาปโลก: "swap the background to a desert at sunset right when he snaps his fingers." [A03.L02 frames t=00:40]
- คำขอหลายโลก: "Give me three prompts for this clip. Lock my action and the camera. Three environment swaps: neon city, lava field, above the clouds." [A03.L03 frames t=00:20]
- คำขอ Level 2: "Seedance prompt for this clip — set my whole head of curls on fire" [A03.L04 frames t=00:20]
- คำขอแบบเปิด: "turn my right hand into something unexpected right when I say the line, '...transform myself right in front of you'" [A03.L05 frames t=00:05]
- คำขอพร้อม reference: "Big lizards — @LIZARD — climbing up the side of a building. Keep my lip-sync exactly as is. Start tight on a telephoto shot of them climbing, then zoom out to my original framing as I start talking ..." [A03.L06 article]
- โครง prompt ของ skill (desert-swap): `@source:` คำบรรยายคลิปตรงตัว + เหตุการณ์มีเวลา → PRESERVE block → pre-trigger hold + sanitize ป้าย/จอ LED → "transform only the world around him" → "Photoreal. 16:9. 7s." + grade/แสง → NON-IP + "SFX and source dialogue only" → shot restatement → beat-by-beat transition → light matching + contact shadow → performance lock → recap + sound timeline [A03.L02 cue desert-swap]
- Inline keep-list: "Subject, face, car, seatbelt, rig framing, camera position and driving motion — preserve exactly." + "Replace background environment and time of day." + relight block (neon spill ข้าง, cool rim) + "Face and identity unchanged." [A03.L03 cue neon-city]
- Head as light source: "His whole head now reads as a light source" + spill บนฝากระโปรงและกระจก + "Everything else — ... — identical to the source" [A03.L04 cue head-on-fire]
- End state เด็ดขาด: "After this point no human hand remains at all ... stays that way to the end of the clip" [A03.L05 cue hand-to-snake]
- Realism register + negative list: "wildlife-documentary realism ... never CGI, rubbery, plastic or cartoonish, no glossy game-render look" [A03.L05 cue hand-to-snake]
- Light integration: lock แสงเดิม ทิศ ความนุ่ม contact shadow haze DOF lens grain "never pasted, never crisper or a different color temp" [A03.L05 cue hand-to-snake]
- Reference role line: `<<<[asset-uuid]>>>:` "Appearance, scale-texture and color reference only; ignore the photo's background and lighting, do not use it for the environment" [A03.L06 cue lizards-climbing]
- Timed shot plan: 0-1 s telephoto (~300mm look) → ที่ 1 s hard fast zoom-out → "a 100% match of the original framing" → take เดิมพร้อมบทพูดและ lip-sync [A03.L06 cue lizards-climbing]
- Wing-walker: preserve performance + กล้อง (start position + full movement) → "Change only the wardrobe, his placement, the aircraft, the environment, the grade and the audio" → "transfer it 1:1" → unified light → physics block → "No music, no vocals, no dialogue" [A03.L07 cue wing-walker]
- Anti-edit สี่คำกริยา: "Do not reinterpret, re-frame, re-time or re-angle any motion" + object remap list + "the same path and blocking as the source" [A03.L08 cue jungle-temple]
- Creature spec: จำนวน, สายพันธุ์เดียว, หัว คอ ปาก ตา ผิว สี ลำตัว ขา หาง + negative anatomy ("No plates, spikes or osteoderms") + analogy วัสดุ ("hide like a wet elephant or rhino") [A03.L09 cue sauropods]
- Timed beat: "at about 2 to 3 seconds, exactly as the man turns and looks back, one sauropod moves in closer" ด้วย "curious, menacing intent" [A03.L09 cue sauropods]
- Kraken: re-read แรงจูงใจ ("his anxious-then-panicked descent now reading as a reaction to the attack") + สเกลเทียบ (หนาเกินเสากระโดง, hundreds of feet) + crowd beat (หนวดจับลูกเรือลากตกเรือ) + "Two honest flags" ท้าย prompt [A03.L10 cue kraken]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Seedance 2.0 บน Higgsfield, video-to-video, 4K, 16:9; recreate link `/generate/video/seedance_2_0?aspect_ratio=16:9&resolution=4k` [A03.L02 cue desert-swap] [A03.L05 cue hand-to-snake]
- duration ใน prompt แต่ละบท: 7s (desert), 6s (neon, head fire), 12s (snake), 8s (lizards, wing-walker), 5s (temple), 11s (sauropods, kraken) [A03.L02 cue desert-swap] [A03.L03 cue neon-city] [A03.L05 cue hand-to-snake] [A03.L06 cue lizards-climbing] [A03.L08 cue jungle-temple] [A03.L09 cue sauropods] [A03.L10 cue kraken]
- แถบ generate ใน L07: "Seedance 2.0" | "16:9" | "4k" | "15s" | "1/4" | "High" | ไอคอนเสียง; GENERATE = 330 credits [A03.L07 frames t=00:47]
- Panel batch ใน L03: chip "Seedance 2.0", chip อ้าง source "@video_1", 3 prompt มีเลขกำกับ, ปุ่ม GENERATE เดียว (ไม่มี chip resolution/duration/credit) [A03.L03 frames t=00:34]
- Claude chat ใช้เขียน prompt; ตัวเลือกโมเดลอ่านได้ "Opus 4.8 High" ใน hires frames [A03.L02 frames t=00:37] [A03.L09 frames t=00:09] [A03.L10 frames t=00:02]
- Skill tag บนจออ่านได้ "/Seedance-footage-vfx" [A03.L02 frames t=00:37]
- คลิปที่แนบใน Claude แสดงเป็น "video.mp4" / "MP4" [A03.L02 frames t=00:37]
- GPT Image 2.0 ใช้ออกแบบภาพ reference สัตว์ [A03.L06 t=00:07-00:19]
- Syntax อ้าง asset: `@source:` (Higgsfield), `<<<video_1>>>:` และ `<<<asset-uuid>>>:` ใน prompt, `@LIZARD` ในคำขอ [A03.L06 cue lizards-climbing] [A03.L07 t=00:40-00:45]
- เวลาต่อ generation ราว "about two minutes" [A03.L04 t=00:45-00:51]
- Higgsfield create page: https://higgsfield.ai/create/video [A03.L11 article]

### คำเตือนและ failure modes
- ที่ 1080p รายละเอียดบิด ตัวอักษรบนจอเพี้ยน lip-sync drift เมื่อ crop [A03.L01 article] [A03.L03 article]
- จอเล็กซ่อนรายละเอียด ไม่ควรใช้ตัดสินคุณภาพ [A03.L01 t=00:41]
- Green screen + mask ทีละเฟรมดูแปะเสมอเพราะแสงไม่เคยตรง [A03.L02 article]
- ตัวอย่าง desert เป็นกล้องช้านิ่ง กล้องเร็วยากกว่า [A03.L02 t=01:32-01:37]
- prompt บังคับให้ป้าย จอ LED และแบรนด์ว่างหรือ generic (NON-IP) [A03.L02 cue desert-swap]
- ไฟที่ไม่ส่องหน้าดูเป็นสติกเกอร์ทุกครั้ง; รายละเอียดไฟ (ember, ขอบ) ถูกโยนทิ้งก่อนที่ความละเอียดต่ำ [A03.L04 article]
- ส่วนใหม่ที่ mirror มืออีกข้างดูเป็นกราฟิกแปะ; ไม่ match แสงกลางวันจะ "float" [A03.L05 article]
- เปลี่ยนมากกว่าหนึ่งอย่าง สมองอ่านว่า "the video glitched" [A03.L05 article] [A03.L11 article]
- background หรือแสงของภาพ reference อาจรั่วเข้าฉาก ต้องจำกัดไว้ที่รูปลักษณ์ [A03.L06 cue lizards-climbing]
- อธิบายดีไซน์เฉพาะด้วยคำ Seedance จะเดา [A03.L06 article]
- Handheld คือกรณียากสุด เอฟเฟกต์ต้องตาม angle/parallax/shake [A03.L07 t=00:00-00:23]
- prompt wing-walker ตัดเสียงทั้งหมดยกเว้น SFX ("No music, no vocals, no dialogue") จึงทิ้งเสียงพูดต้นฉบับ [A03.L07 cue wing-walker]
- สัตว์ photoreal "usually where AI falls apart" คือดูยาง ลอย CG [A03.L09 t=00:13-00:18]
- relight กลางคืนเสี่ยง face drift สูงกว่ากลางวัน ให้ตรวจหน้าใน take แรก [A03.L10 cue kraken] [A03.L10 article]
- ไม่มีภาพ reference mood พายุจะพึ่งแต่ prose และอาจหลุด [A03.L10 cue kraken]
- กลางคืนและอากาศหนักคือคำขอที่ยากที่สุด [A03.L10 article]
- ห้ามหนวดเล็ก ดูเป็นของเล่น บาง ยาง ลอย CG การ์ตูน หรือ game-engine [A03.L10 cue kraken]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- sizzle reel เปิดคอร์สมี inset คลิปจริงคู่กับผล และมีช็อตแขนกลแปลงร่างบนบันไดซึ่งไม่อยู่ในระดับที่บทความระบุ [A03.L01 t=00:35-00:40]
- lower-third ระดับสามขั้นสะกดผิด "TRANSFROM" บนจอ [A03.L01 t=01:35-01:40]
- กล่อง input ของ Claude จริง: thumbnail คลิป → skill tag บรรทัดแยก → คำขอประโยคเดียว → ตัวเลือกโมเดลมุมขวาล่าง [A03.L02 t=00:35-00:40]
- prompt เต็มบนจอถูก highlight สีเขียวที่ประโยค keep-list "Preserve his identity, face, mustache..." [A03.L02 t=00:50-00:55]
- gag เปลี่ยนพื้นหลังสตูดิโอผู้สอนเป็นป่าระหว่างพูด (ไม่มี prompt) [A03.L02 t=01:25]
- ผู้สอนบอก "I didn't grade any of it" ในช็อตขับรถสามโลก [A03.L03 t=00:44-00:46]
- panel Seedance แสดงสาม prompt เข้าคิวใต้ปุ่ม GENERATE เดียวจากคลิปเดียว [A03.L03 frames t=00:34]
- วงกลมสีเหลืองบนผลไฟชี้แสงส้มที่ตกบนเสื้อ (และบนรถ) เพื่อพิสูจน์ light interaction [A03.L04 t=00:56-01:01]
- คำขอ snake ในวิดีโอเป็นแบบปลายเปิด ("something unexpected") ไม่ได้ระบุงู [A03.L05 frames t=00:05]
- ภาพ reference กิ้งก่าบนจอเป็นตัวเล็กบนพื้นเทาอ่อน [A03.L06 t=00:10]
- แถบ Higgsfield พร้อม `@source` highlight เขียวและราคา 330 แสดงครั้งแรกใน L07 [A03.L07 frames t=00:47]
- คำขอ temple บนจอมีขั้นที่ผู้ใช้บรรยาย action และชนิดกล้องของตัวเองก่อนคำสั่ง lock ("grips shifting, body swaying, handheld") ซึ่งบทความไม่มี [A03.L08 frames t=00:10]
- รายละเอียดต้นทุนสตูดิโอที่พูด: "creature artists sculpturing every scale, trackers locking the CG to the camera move, and teams building entire environments from scratch" [A03.L11 t=00:00-00:21]
- montage สรุปยืนยันว่าคนใส่เสื้อกันฝนเหลืองปรากฏในผลช็อต sauropod [A03.L11 t=00:00-00:05]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- L05 เสียงพูดสื่อว่ามือกลายเป็นงู แต่ inset ผลใน hires เป็นแขนกลสีเงิน ไม่เห็นงูเลย ไม่รู้ว่า prompt ไหนสร้างเวอร์ชันแขนกล [A03.L05 frames t=00:30] [A03.L05 frames t=00:35]
- L06 ภาพ reference ดูเหมือนกิ้งก่าแบบ bearded dragon แต่ prompt เรียก "real large monitor lizard" (ข้อสังเกตของผู้จด) [A03.L06 t=00:10] [A03.L06 cue lizards-climbing]
- L07 chip duration อ่าน 15s แต่ cue ระบุ 8s คอร์สไม่อธิบาย [A03.L07 frames t=00:47] [A03.L07 cue wing-walker]
- L09 คลิปต้นฉบับเป็นเมือง (อาคารครีบตั้ง) แต่ cue และคำขอบอก "a man in a forest" และอนุญาตเปลี่ยนแค่เสื้อผ้ากับบรรยากาศ ขณะที่ผู้สอนพูด "the background swap looks incredibly real" [A03.L09 frames t=00:05] [A03.L09 t=00:19-00:24]
- L09 พูดว่าไดโนเสาร์สามตัว แต่ cue เขียน two to three [A03.L09 t=00:06-00:13] [A03.L09 cue sauropods]
- L10 flag ของ skill บอกว่า mood "rides entirely on the prose instead of the reference still" แปลว่ามีรอบก่อนที่ใช้ reference still แล้วถอดออก แต่ไม่ถูกแสดง [A03.L10 cue kraken]
- L03 PromptBox "volcanic dusk" และ "above the clouds" ว่างในไฟล์คอร์ส เห็นแค่บรรทัดแรกบนจอ [A03.L03 article] [A03.L03 frames t=00:35]
- L03/L04 ใช้ "SFX only" ทั้งที่ผู้สอนพูดในคลิป ไม่ชัดว่าเสียงพูดต้นฉบับคงอยู่หรือไม่ ขณะที่ cue อื่นเขียน "SFX and source dialogue only" ชัดเจน [A03.L03 cue neon-city] [A03.L02 cue desert-swap]
- เวอร์ชันโมเดล Claude: course wrap-up อ่านได้แค่ "Opus 4.x High" จาก sheet แต่ hires อ่าน "Opus 4.8 High"; ชื่อ skill อ่านจากเฟรมเท่านั้น [A03.L08 frames t=00:10] [A03.L02 frames t=00:37]
- ไม่มีการพูดหรือเขียนราคาเครดิตในบทความ ตัวเลขเดียวคือ 330 บนปุ่ม GENERATE ใน L07 [A03.L07 frames t=00:47]
- cue L07 มีตัว Cyrillic "с" ใน "Original сlip" (encoding artefact ในต้นฉบับ) [A03.L07 cue wing-walker]

### เทียบกับ v1
- เหมือนเดิม: ระบุ anchor ที่ต้องคง (หน้า มือ dashboard) และรายการเปลี่ยนเฉพาะส่วน [A03.L01 article] [A03.L02 article]
- เพิ่ม: workflow จริงคือ Claude อ่านคลิปเป็นเฟรม + Seedance skill เขียน keep-list ให้ ผู้ใช้พิมพ์แค่ประโยคเดียว [A03.L02 t=00:21-00:59]
- เพิ่ม: รูปแบบคำขอมาตรฐาน "Seedance prompt for this clip — ... Lock my action and the camera exactly. Turn it into ..." [A03.L08 frames t=00:10]
- เพิ่ม: settings (16:9, 4K, duration ต่อ prompt) และราคา 330 credits ณ วันบันทึก [A03.L07 frames t=00:47]
- เพิ่ม: syntax `@source` / `<<<video_1>>>` / `<<<uuid>>>` และการ scope ภาพ reference [A03.L06 cue lizards-climbing]
- แก้: v1 A03.02 บอกว่า "ภาพนิ่งที่ผู้ช่วยเห็นไม่แทนการดู motion ตลอดคลิป" แต่ในคอร์ส Claude อ่านวิดีโอเป็นชุดเฟรมและเขียน camera motion ลง keep-list เอง [A03.L02 t=00:21-00:34]
- แก้: v1 A03.10 บอกให้ "ใช้ภาพ mood ล็อกพายุ" เป็นขั้นปกติ แต่ในคอร์ส mood reference เป็น fallback เมื่อ take หลุด mood ตาม honest flag ของ skill [A03.L10 cue kraken]
- เพิ่ม: "honest flags" ท้าย prompt และ face-drift risk ในฉากกลางคืน [A03.L10 article]
- เพิ่ม: ความขัดแย้งในคอร์ส (snake vs แขนกล, urban vs forest, 15s vs 8s) [A03.L05 frames t=00:35] [A03.L09 frames t=00:05] [A03.L07 frames t=00:47]
- เหมือนเดิม: wing-walker ล็อกการเคลื่อน 1:1 และเพิ่มลม/slipstream; temple รักษาจุดจับและจังหวะเดิม [A03.L07 cue wing-walker] [A03.L08 cue jungle-temple]

## A04 Make an AI Animated Short

### ภาพรวมและผลลัพธ์
- คอร์ส 11 บท (ผู้สอนบนจอ "Adil" @ADILINTHEWILD; ผู้เขียนคอร์สในข้อมูลคือ Rus Syzdykov) ทำหนังสั้นแอนิเมชันเรื่องเดียว 8 ฉาก แต่ละฉากเป็นสไตล์แอนิเมชันต่างกันโดยสิ้นเชิง แต่ plot ต่อเนื่องกัน [A04.L02 t=00:03] [A04.L01 frames t=00:10]
- เครื่องมือคู่หลัก: Soul Cinema + Seedance 2.0 บน Higgsfield ซึ่งผู้สอนเรียกว่า "best combo right now" [A04.L02 t=00:17]
- บริบทเปิดตัว: Seedance 2.0 เปิดให้ทุกคนทั่วโลกบน Higgsfield ไม่ต้องรอคิว ไม่ต้องมี business account และมีโปร unlimited 7 วัน (ข้อมูล ณ วันบันทึก) [A04.L01 t=00:14] [A04.L01 t=00:20]
- ผู้สอนอ้างว่าแอนิเมชันตอนนี้ใช้แค่ "a couple hours and the right prompts" [A04.L01 t=00:05]
- เรื่อง: ตัวเอกตื่นสาย เลือกเส้นทาง "ULTRAFAST" บนนาฬิกา แล้ว teleport ผ่านโลกต่าง ๆ จนไปถึงร้านอาหารพบ Anna ที่สภาพพังพอกัน [A04.L03 article] [A04.L10 article]
- วงจรสรุปท้ายคอร์ส: Claude เขียน prompt, Seedance 2.0 ลงมือ, Soul Cinema + Nano Banana Pro ให้ชิ้นส่วนภาพ, วิดีโอก่อนหน้าป้อนเข้าทุกฉากใหม่ [A04.L11 t=01:55-02:08]
- ข้อสรุปหลักของบทความ: "A text description drifts over generations — a video reference doesn't." [A04.L11 article]

### Workflow ทีละขั้น
1. เขียนเรื่องต่อเนื่องเรื่องเดียว แบ่งเป็นฉากละ ≤15 s แต่ละฉากสไตล์ต่างกัน และจบทุกฉากด้วยอุปกรณ์เปลี่ยนฉากเดียวกัน (แฟลชขาวของการ teleport) เพื่อให้ฉากถัดไปเปิดจากจุดนั้น [A04.L02 t=00:03] [A04.L03 t=02:33] [A04.L04 t=01:09]
2. Keyframe ตัวเอกฉาก 1: Soul Cinema (16:9, 2k, เปิด enhancer) prompt บรรทัดเดียว รันหลาย batch แล้วเลือก [A04.L03 t=00:12] [A04.L03 t=00:30] [A04.L03 frames t=00:35]
3. ถ้า keyframe ใกล้แต่ผิด ให้แก้เฉพาะจุดด้วย Nano Banana Pro แทนการ reroll [A04.L03 t=00:45] [A04.L05 t=00:30-00:51]
4. ล็อกพร็อพที่วนซ้ำ: อัปโหลด keyframe ให้ Claude ขอ prompt prop sheet "for a watch that matches the exact style" แล้ว render ใน Nano Banana Pro [A04.L03 t=01:00] [A04.L03 cue scene1-prop-sheet]
5. ให้ Claude ทั้งสองภาพ (ตัวละคร + นาฬิกา) + plot ย่อหน้าเดียวพร้อมระยะเวลา ("Fifteen seconds") ให้ขยายเป็น Seedance prompt ทีละช็อตมี timestamp [A04.L03 t=01:35] [A04.L03 t=01:40-01:55]
6. Generate ใน Seedance 2.0 (21:9 หรือ 16:9, 1080p, 15 s) และ iterate "a couple iterations" [A04.L03 cue scene1-animated] [A04.L03 t=02:30]
7. ฉากใหม่: ทำ keyframe Soul Cinema ใหม่โดยเปลี่ยนแค่วลีสไตล์และวลีสภาพแวดล้อม [A04.L04 t=00:30-00:37]
8. ให้ Claude keyframe ใหม่ + prompt ของฉากแรก/ฉากก่อน + คำบรรยาย beat ธรรมดาพร้อม "15 seconds, ends on the teleport" [A04.L04 t=00:46-01:11] [A04.L05 frames t=00:55]
9. ป้อน Seedance สามอย่าง: prompt, keyframe เป็น style reference และ "most importantly" วิดีโอก่อนหน้า [A04.L04 t=01:12-01:21]
10. สไตล์ที่ไกลจากหน้าตาเดิมมาก (มังงะ) ให้สร้าง character sheet สไตล์นั้นก่อน จาก keyframe ห้องนอนเดิม + prop sheet นาฬิกา → Claude → Nano Banana Pro [A04.L07 t=00:13-00:35]
11. ฉากจบที่ต่อตรง: ข้าม keyframe ใช้ prop sheet + prompt ฉากแรก + คำบรรยายธรรมดา แล้วปล่อยให้ Seedance สร้างตัวละครที่ไม่ได้ระบุ (Anna) [A04.L10 t=00:08-00:19] [A04.L10 t=01:15-01:25]
12. ตัดต่อ 8 ฉากที่แต่ละฉากมาจาก generation เดียวเป็นหนัง (เครื่องมือตัดต่อไม่ถูกแสดง) [A04.L11 t=01:55-02:08]

### กฎที่ใช้ซ้ำได้
- สร้าง keyframe ตัวละครก่อน ทุกฉากต่อมาใช้ตัวเอกคนเดิม [A04.L03 t=00:00]
- ล็อกพร็อพที่ปรากฏทุกฉากด้วย prop sheet หลายมุม (พร้อมวัสดุและภายใน) ไม่งั้น Seedance คงความสม่ำเสมอไม่ได้ [A04.L03 t=01:20] [A04.L03 t=00:55]
- Soul Cinema ให้สไตล์, Nano Banana Pro แก้ตัวละคร: แก้ keyframe ไม่ใช่สร้างใหม่ [A04.L05 t=00:30-00:51] [A04.L03 t=00:45]
- เปิด enhancer ของ Soul Cinema กับ prompt ธรรมดาเพื่อให้มันประดิษฐ์สไตล์ที่เราไม่ได้ขอ [A04.L03 t=00:30]
- โลกใหม่ = เปลี่ยนสองวลี (สไตล์ + สภาพแวดล้อม) ใน prompt keyframe เดิม [A04.L04 t=00:30-00:37]
- prompt keyframe สั้นได้ เมื่อคำสไตล์แบกฉากไว้ ("Chibi gladiator toy in a low-poly arena" เจ็ดคำ) [A04.L05 t=00:14-00:25] [A04.L05 cue scene3-keyframe]
- สองคีย์เวิร์ดแรงพอจะแบกเฟรม ("stop motion" + "futuristic helicopter") แล้ว texture แสง background ตามมาเอง [A04.L06 t=00:27-00:37]
- keyframe ได้ใน batch แรกก็รับเลย ("sometimes you just get lucky") [A04.L08 t=00:25-00:33] [A04.L06 t=00:38]
- ใช้ "extra two minutes" สร้าง prompt ให้ดี: prompt พื้น ๆ ได้ผลพอใช้ prompt ที่สร้างดีได้ผลดีกว่ามาก [A04.L03 t=02:04]
- 1 ฉาก = 1 Seedance generation ≤15 s ที่มีหลายมุมและ camera move ข้างใน เพื่อให้ตัดต่อง่าย [A04.L03 t=02:33]
- "Consistency isn't a setting you toggle": มาจากการส่ง prompt และวิดีโอของช็อตก่อนต่อไปทุกครั้ง [A04.L04 article]
- ทำให้ Seedance prompt เป็นการต่อวิดีโอ ("Extend @video1. Continue exactly from the white flash of the last frame") ไม่ใช่ generation ใหม่ [A04.L05 cue scene3-animated]
- จบทุกฉากที่ teleport ให้ฉากถัดไปเปิดที่การมาถึงผ่าน portal [A04.L04 t=01:09] [A04.L04 cue scene2-animated]
- ถ้า style reference มีตัวละครที่ไม่ต้องการ ให้เขียนชัด: "style reference ONLY ... DO NOT use the character from image_2. Create a NEW original character ..." [A04.L06 cue scene4-animated] [A04.L08 cue scene6-animated]
- ผูกพร็อพกับตำแหน่งร่างกายและช่วงเวลา: "match this exact watch design on the hero's left wrist throughout all frames" [A04.L06 cue scene4-animated]
- ใช้กฎเวลาเดียวทั้งฉาก: ทุกอย่าง slow motion ยกเว้น teleport ไม่งั้นช็อตดูเป็นลูกเล่น [A04.L06 t=01:21] [A04.L06 article]
- ระบุไวยากรณ์ของ format (kanji SFX ใน 「」, reaction marks, เหงื่อ, speed lines, screentone) ไม่ใช่แค่สี [A04.L07 article] [A04.L07 cue scene5-animated]
- สไตล์ขาวดำเคร่งครัดใช้ negative แข็ง: "Black and white only — zero color", "zero 3D, zero CGI", "no color, no grey" [A04.L07 cue scene5-animated] [A04.L07 cue scene5-manga-sheet]
- ให้แต่ละฉากมีมุกทางกายภาพเฉพาะหนึ่งอย่างที่ผูกกับ physics ของโลกนั้น (มือ chibi กดปุ่มไม่โดน, นิ้วดินเหนียวจมทะลุข้อมือ) [A04.L05 article] [A04.L08 cue scene6-animated]
- เพิ่ม reaction beat ของตัวประกอบหลัง action (ปีศาจถือมือเปล่าแล้วทำปากยื่น) ให้โลกดูมีชีวิต [A04.L08 t=01:06-01:19] [A04.L08 article]
- ระบุว่าสไตล์ render องค์ประกอบอย่างไร ("fire is sculpted from orange-red clay ribbons, smoke is grey clay wisps") [A04.L08 cue scene6-animated]
- จำกัดสไตล์ไว้ที่องค์ประกอบเดียว: "cel-shaded flat coloring on hero only, cartoon physics and expressions on hero only" [A04.L09 cue scene7-animated]
- ความขัดกันของสไตล์คือมุก: "looks wrong on purpose" [A04.L09 t=00:59-01:06]
- จ่ายคืนรายละเอียดความต่อเนื่องจากฉากก่อน (รองเท้าหาย เสื้อขาด รอยไหม้) ใน brief ฉากจบ [A04.L10 t=00:20-00:30] [A04.L10 cue scene8-animated]
- ผูกพร็อพกับไทม์ไลน์ด้วยเงื่อนไขออก: "throughout all frames until he removes it" [A04.L10 cue scene8-animated]
- ใช้วิดีโอที่เสร็จแล้วเป็น continuity reference ไม่ใช่คำบรรยายตัวละคร [A04.L11 t=02:05] [A04.L11 article]

### โครงสร้าง Prompt
- Keyframe ฉาก 1: `<style word: Cartoon>, <style intensifier: highly stylized>, <subject + action + location>` บรรทัดเดียว [A04.L03 cue scene1-keyframe]
- Prop sheet: `Prop sheet of <object>` + orthographic views (front, side, back, top) + exploded view/internals + material breakdown + lighting + render style ตาม keyframe + clean neutral background + layout design sheet มี annotations/callouts + consistent proportions + grade [A04.L03 cue scene1-prop-sheet]
- Seedance ฉาก 1: header ผูก reference (`<<<image_1>>> is the character reference AND visual style reference — ...`, `<<<image_2>>>` คือนาฬิกาที่ข้อมือซ้าย) → keep-list ตัวละคร → style lock ซ้ำสองครั้ง → beats มี timecode (`Opening frame (0–4s)` / `Rushed preparation (4–10s)` / `Map selection + discovery (10–14s)` / `Teleportation (14–15s)`) พร้อมข้อความ UI ในเครื่องหมายคำพูดและภาษากล้อง → `Style:` ปิดท้ายด้วย `2.35:1 widescreen, 24fps` [A04.L03 cue scene1-animated]
- Brief ธรรมดาให้ Claude: "He wakes up, panics, sees a message from Anna, gets dressed, checks the watch, sees two route options plus a mystery third one — Ultra Fast — taps it, teleports. Fifteen seconds." [A04.L03 t=01:40-01:55]
- Keyframe ฉาก 2 ช่องที่สลับได้: `<STYLE PHRASE: 2D French graphic novel style>, <hero descriptor> <action>, <antagonist + action> <ENVIRONMENT PHRASE: in a futuristic environment>` [A04.L04 cue scene2-keyframe]
- Brief ต่อฉาก: "He jumps onto a horse, gets shot at, a bullet grazes him, he click the watch again and teleports away. 15 seconds, the shot ends on the teleport." [A04.L04 t=01:00-01:10]
- Edit ใน Nano Banana Pro: `Edit the main central character only:` + change list + `keep <character design, proportions, facial features>` + `preserve <lighting, environment, camera angle, DoF, surrounding characters> exactly` + `no changes to background or composition` + `seamless integration, consistent shadows and color grading` [A04.L05 cue scene3-edit]
- Extend prompt: `Extend @video1. Continue exactly from <last-frame state>.` + `@image1 is the character reference — <keep-list>, now transformed into <new style> matching @image2` + `@image2 is the visual style reference — ...` + beats มี timecode จบด้วย "Pure white frame. Smash cut to black." [A04.L05 cue scene3-animated]
- Style-only reference: `<<<image_2>>> is the visual style reference ONLY — <lighting, palette, environment, aesthetic>. DO NOT use the character from <<<image_2>>>. Create a NEW original character ...: <hero keep-list>` [A04.L06 cue scene4-animated]
- Brief เป็น comma list พร้อมเงื่อนไขจบ: "ROOFTOP, SLOW MOTION WORLD, HELICOPTER, ANDROID SHOOTS, BULLET IN EXTREME SLOW-MO, HE PANICS, FUMBLES THE WATCH, HITS IT WITH ONE CENTIMETER TO SPARE." [A04.L06 t=00:50-01:00]
- Character sheet สไตล์ใหม่: `CHARACTER SHEET — <STYLE>.` + `@Image1 = character reference. @Image2 = <prop> on left wrist. Same person across all frames.` + `STYLE:` (ยุค เส้น hatching screentone, "no color, no grey", อ้าง Akira/Ghost in the Shell) + `CHARACTER:` [A04.L07 cue scene5-manga-sheet]
- Manga Seedance prompt: block `@char:` + format line (`2D manga animation. 16:9. 15s. Black and white only — zero color. ... Free camera, handheld, dynamic cuts.`) + ย่อหน้าต่อ beat ไม่มี timestamp พร้อม shot size และ SFX ญี่ปุ่นใน 「」 + "Last frame:" [A04.L07 cue scene5-animated]
- Simile ช่วยกำกับท่าที: ปีศาจตรวจตัวเอก "like a chef inspecting a good cut of meat" [A04.L08 cue scene6-animated]
- Swap ตัวละครใน keyframe: `@image1 is the reference image to edit. In @image1, replace <target: location + current traits> with <source: character from @image2 + its traits>. Keep <wardrobe>. Do not change anything else — ... Only <face and hair> should change to match @image2.` [A04.L09 cue scene7-swap]
- ฉากจบ: `Extend <<<video_1>>>` + watch binding "until he removes it" + global mode line (`This final scene is live-action cinematic — ... photorealistic. No animation styles.`) + beats 0-3 / 3-7 / 7-11 / 11-15 s จบ "fade to warm white" [A04.L10 cue scene8-animated]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Soul Cinema ("Higgsfield Soul Cinema", soul_cinematic) สำหรับ keyframe: แถบ "Soul Cinema" | "16:9" | "2k" | ชิปไม้กายสิทธิ์ "On" | stepper "− 1/4 +" | "Color transfer" (New) + ช่อง "CHARACTER" + "GENERATE" [A04.L03 frames t=00:35] [A04.L06 frames t=00:20]
- ราคาบนจอ: "4 GENERATIONS = 0.5 CREDITS / 100 GENERATIONS = 12.5 CREDITS" [A04.L03 t=00:15]
- ใน L04 stepper อ่าน "− 4/4 +" [A04.L04 frames t=00:14]
- Nano Banana Pro (nano-banana-pro, 16:9) สำหรับแก้ตัวละคร swap, prop sheet และ manga character sheet [A04.L03 cue scene1-prop-sheet] [A04.L05 cue scene3-edit] [A04.L07 cue scene5-manga-sheet]
- Seedance 2.0 (seedance_2_0): 21:9 หรือ 16:9 ตาม cue URL, 1080p, 15 s, โหมด extend ด้วย @video1 / <<<video_1>>> และ image refs [A04.L03 cue scene1-animated] [A04.L04 cue scene2-animated] [A04.L06 cue scene4-animated]
- UI ของ Seedance แสดงช่อง "Input 1" / "Input 2": ใน L04 = keyframe ใหม่ + เฟรมวิดีโอฉาก 1 [A04.L04 frames t=01:15]
- ใน L08 เห็น input ครบสามช่อง: watch prop sheet + คลิปฉาก 1 + keyframe clay hell [A04.L08 t=00:50-01:00]
- Claude (นอก Higgsfield) เขียน prompt prop sheet, character sheet และ Seedance; มีการเอ่ยถึง "Claude skill" ในคำอธิบายวิดีโอแต่ไม่อยู่ในไฟล์คอร์ส [A04.L03 t=01:00] [A04.L03 t=02:01]
- เมนู Image ของ Higgsfield มีโมเดลอื่นที่ไม่ได้ใช้ เช่น Higgsfield Soul 2.0, Popcorn, Nano Banana 2, Seedream 5.0 lite, GPT Image 1.5, Grok Imagine, FLUX.2, Reve, Z-Image, Topaz และฟีเจอร์ Relight, Inpaint, Face Swap, Character Swap, Draw to Edit [A04.L03 frames t=00:32]
- Top nav ณ วันบันทึกมี "Cinema Studio 3.0" [A04.L03 frames t=00:32]

### คำเตือนและ failure modes
- ตัวละครดูผิดอย่าเริ่มใหม่ ให้แก้ใน Nano Banana Pro [A04.L03 t=00:45]
- "This is the part most people skip": prompt ที่สร้างไม่ดีจำกัดคุณภาพ [A04.L03 t=02:04]
- ไม่ส่ง prompt และวิดีโอก่อนหน้า ฉากจะเป็น "slideshow of unrelated clips" [A04.L04 article]
- prompt หนัก (graphic novel + เมืองอนาคต + ม้า + คาวบอย) "worth a couple of rerolls before it clicks" [A04.L04 article]
- ตัวกลางที่ generate มาไม่ตรงตัวเอก (ผมผิด ไม่มีสูท) ต้องแก้ด้วย edit [A04.L05 t=00:30]
- แอนิเมชันฉาก 4 "took a couple tries" ต่างจาก keyframe ที่ได้รอบแรก [A04.L06 t=01:17]
- style reference มีตัวละครของมันเอง ต้องตัดออกชัด ๆ [A04.L06 cue scene4-animated]
- สไตล์ที่ไกลจากตัวเดิม (มังงะ) ถ้าไปตรง Seedance โดยไม่มีตัวเอกในรูปนั้นก่อน มีนัยว่าจะไม่สำเร็จ [A04.L07 t=00:13]
- เปลี่ยนสไตล์แค่สี/เส้น ได้ลุคแต่ไม่ได้กลไกของ format [A04.L07 article]
- Soul Cinema ประดิษฐ์ตัวการ์ตูนที่ "didn't match our hero" [A04.L09 t=00:16]
- ผู้สอนเองไม่แน่ใจว่า Seedance จะทำ mixed-media ได้ [A04.L09 t=00:57]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- ภาพย่อแปดสไตล์ลอยข้างผู้สอน (ห้องนอน 3D อุ่น, สูทกับยาน, งานแต่งการ์ตูน, chibi ในอารีนา, มังงะขาวดำ, graphic novel ม้ากับคาวบอย, ร้านอาหาร, เวทีแดง) แต่ไม่ได้ map เลขฉาก [A04.L02 frames t=00:09]
- ผู้สอนพูดว่าทำหนังเรื่องนี้เพื่อฉลองการเปิดตัว Seedance ทั่วโลก บทความไม่ได้ผูกไว้ [A04.L02 t=00:00]
- ตัวเลขเครดิต 100 generations = 12.5 credits บนจอ บทความให้แค่ 0.5 [A04.L03 t=00:15]
- เส้นทาง UI จริง: เมนู Image → Higgsfield Soul Cinema → แถบ settings → GENERATE ได้ 4 ภาพ [A04.L03 t=00:30-00:40]
- ตัวอย่างก่อน/หลังการแก้ด้วย Nano Banana (ผู้ชายการ์ตูนกรีดร้องบนเตียงได้หน้าใหม่) [A04.L03 t=00:45-00:50]
- ผล prop sheet นาฬิกากลไกทองเหลืองสายหนังน้ำตาล มีมุมหน้า ข้าง หลัง exploded และคอลัมน์ callout [A04.L03 t=01:20-01:25]
- ผลฉาก 1 มีเสียงพูดของข้อความ UI ("I'll be in the cafe in 10 minutes" / "Would you like the long route or the short one?") และ panel บนจอสะกดผิด "short un?" [A04.L03 t=02:18] [A04.L03 frames t=02:26]
- prompt ที่วางจริงใน Seedance UI ฉาก 2 เป็นแบบไม่มี timestamp (subject → Environment: → Camera: → Style: → "No 3D rendering. No photorealism. No cel-shading gradients.") ต่างจาก cue [A04.L04 frames t=01:15]
- overlay "STYLE / CHARACTER / TELEPORT EFFECT" และ "PORTAL EFFECT / CHARACTER / STYLE" บอกสิ่งที่ส่งต่อ [A04.L04 t=00:55] [A04.L04 t=01:20]
- overlay คำสั่งแก้ "SWAP HAIR TO BLACK AND PUT HIM IN A BLACK SUIT" และภาพก่อน/หลัง (gladiator ผมบลอนด์ → chibi ผมดำสูทดำ อัศวินกับอารีนาไม่เปลี่ยน) [A04.L05 t=00:40-00:45]
- overlay "FIRST SCENE PROMPT → CLAUDE" ซ้ำในหลายฉาก [A04.L05 t=00:55] [A04.L06 t=00:45] [A04.L08 t=00:35]
- watch prop sheet ถูกใช้ซ้ำเป็น input ใน Seedance ฉากหลัง ๆ (บทความไม่ได้บอก) [A04.L05 t=01:20-01:30] [A04.L06 t=01:05-01:15]
- แกลเลอรีโปรเจกต์ Soul Cinema เดียวกันใช้ต่อทุกฉาก [A04.L06 t=00:15]
- keyframe ฉาก 4 แสงเย็นเทาฟ้า แต่ผลวิดีโอเป็น neon ชมพู/ฟ้าตาม prompt คือ Seedance relight ตามข้อความ (ข้อสังเกต) [A04.L06 t=00:30] [A04.L06 t=01:05-01:15]
- ฉากมังงะมีแค่ input เดียว (character sheet) ไม่เห็น input วิดีโอก่อนหน้า [A04.L07 t=01:00-01:10]
- Seedance เพิ่มรอยลิปสติกบนแก้มตัวเอกการ์ตูนเองโดยไม่มีใน prompt [A04.L09 t=00:40-00:50]
- prompt ที่วางบนจอใน L05/L07/L08/L09 มีย่อหน้า "Sound design (SFX only, no music): ..." ต่อท้ายซึ่งไม่มีใน cue (ผู้ตรวจพบจากเฟรมของตัวเอง) [A04.L08 t=00:50-01:00] [A04.L07 t=01:00-01:10]
- หนังเต็มมีเสียง รวมบทพูดภาษาญี่ปุ่นในช่วงมังงะ [A04.L11 t=01:02]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- วิดีโอ reference ต่อเนื่องคือฉากไหน: บทความบอก "previous scene" แต่ overlay บอก "FIRST SCENE PROMPT → CLAUDE", เสียงพูดว่า "the first video" และ thumbnail ใน Seedance UI ของ L05-L09 เป็นเฟรมฉาก 1 ยังไม่คลี่คลาย [A04.L05 frames t=00:55] [A04.L06 t=00:44] [A04.L04 article]
- prompt ที่วางใน Seedance UI ฉาก 2 (ไม่มี timestamp มี negative) ต่างจาก cue ที่มี timestamp ไม่รู้ว่าอันไหนสร้าง take ที่เห็น [A04.L04 frames t=01:15] [A04.L04 cue scene2-animated]
- prompt ฉาก 1 สั่ง "2D anime illustration, cel-shaded" แต่ผลเป็น paper-cutout 3D ตาม keyframe (อนุมานว่า image_1 ชนะข้อความ) [A04.L03 cue scene1-animated] [A04.L03 t=02:15-02:35]
- prompt ฉากจบสั่ง "photorealistic. No animation styles." และบทความบอกเป็น live action แต่ผลเป็น 3D stylized ตัวเอกและ Anna ยังผม paper-cutout [A04.L10 cue scene8-animated] [A04.L10 t=00:50-01:10]
- สีผมใน L05: พูดว่า "black" แต่ cue และบทความเขียน "natural brown" [A04.L05 t=00:37] [A04.L05 cue scene3-edit]
- L05 brief บอก "fourth try" แต่เสียงพูดว่า "fumbles the watch a couple times... on the last try" [A04.L05 t=01:08]
- keyframe (@image2) ไม่อยู่ใน input ที่เห็นของฉาก 3 [A04.L05 t=01:20-01:30]
- ฉากมังงะไม่ใช้ "Extend" แต่เปิดจาก "pure white void" ต่างจากฉากอื่น [A04.L07 cue scene5-animated]
- cue ฉาก 6 เขียน "Clay motion" แต่บนจอเป็น "Claymation" (ถอดเสียงผิด) [A04.L08 t=00:15-00:20] [A04.L08 cue scene6-keyframe]
- ฉากจบ brief เขียน "18:00" แต่พูดว่า "exactly 6 o'clock" [A04.L10 t=00:31]
- ผู้สอนเรียกทั้งฉากอารีนาและ 5 วินาทีของปีศาจว่าเป็น favorite (L08 บันทึกว่าใน L05 ก็เรียกอารีนาว่า favorite) [A04.L08 t=01:06-01:19]
- ไม่อธิบายความหมายของ stepper "1/4" vs "4/4" และชิป "On" (enhancer เป็นการอนุมาน) [A04.L03 frames t=00:35]
- ไม่ระบุว่าเสียงในคลิป (เสียง UI, ภาษาญี่ปุ่น) สร้างโดย Seedance เองหรือเพิ่มใน edit [A04.L03 frames t=02:26] [A04.L11 t=01:02]
- "Claude skill" และ "full prompts in the description" ถูกอ้างแต่ไม่อยู่ในไฟล์คอร์ส [A04.L03 t=01:15] [A04.L11 t=02:13]
- ไม่มีราคาเครดิต Seedance และจำนวนรอบ iterate ต่อฉาก นอกจาก "a couple tries" [A04.L06 t=01:17]
- ไม่รู้เครื่องมือตัดต่อรวมหนัง [A04.L11 t=01:55-02:08]

### เทียบกับ v1
- เหมือนเดิม: นาฬิกาและตัวละครเป็นแกนข้ามแปดสไตล์ และวงจร keyframe → targeted edit → scene prompt → previous-video continuation [A04.L02 t=00:03] [A04.L11 t=01:55-02:08]
- เพิ่ม: ราคา Soul Cinema 4 ภาพ = 0.5 credit (100 = 12.5) และ settings บนแถบ ณ วันบันทึก [A04.L03 t=00:15] [A04.L03 frames t=00:35]
- เพิ่ม: กฎ "เปลี่ยนสองวลี" (สไตล์ + สภาพแวดล้อม) ทำ keyframe โลกใหม่ [A04.L04 t=00:30-00:37]
- เพิ่ม: syntax "Extend @video1. Continue exactly from the white flash ..." และ "style reference ONLY — DO NOT use the character" [A04.L05 cue scene3-animated] [A04.L06 cue scene4-animated]
- เพิ่ม: การสร้าง prop sheet ผ่าน Claude → Nano Banana Pro และ character sheet มังงะ [A04.L03 cue scene1-prop-sheet] [A04.L07 cue scene5-manga-sheet]
- แก้: v1 A04.04 บอก "ส่ง prompt และวิดีโอก่อนหน้า" แต่หลักฐานในวิดีโอ (overlay + thumbnail) ชี้ว่าเป็นวิดีโอ/prompt ของฉากแรก ไม่ใช่ฉากก่อนหน้า (ยังไม่สรุป) [A04.L05 frames t=00:55] [A04.L06 t=00:44]
- แก้: v1 A04.03 เรียกฉาก 1 ว่า "Papercut" ซึ่งตรงกับผล แต่ prompt จริงสั่ง 2D anime cel-shaded; ลุค paper-cutout มาจาก keyframe [A04.L03 t=02:15-02:35]
- เพิ่ม: ฉากจบไม่ได้ออกมาเป็น photoreal ตามที่บทความอ้าง [A04.L10 t=00:50-01:10]
- เหมือนเดิม: v1 A04.06 เตือนว่า prior video ไม่ใช่หลักประกันว่าคนจะไม่ drift; คอร์สยืนยันว่าฉาก 4 ต้องลองหลายรอบ [A04.L06 t=01:17]
- เหมือนเดิม: v1 A04.10 บอกว่าอาจไม่ต้องสร้าง keyframe ทุกฉาก ตรงกับคอร์สที่ใช้แค่ prompt ฉากแรก + prop sheet [A04.L10 t=00:08-00:19]

## A05 How to evaluate AI filmmaking demos

### ภาพรวมและผลลัพธ์
- คอร์สนี้เป็นคอร์ส "รีวิว/ประเมิน" ไม่ใช่สอน generate: ใช้ showcase ของ Seedance 2.5 เป็นวัตถุที่ต้องตัดสินว่าพิสูจน์อะไรได้จริง ไม่ใช่ของให้ชื่นชม [A05.L01 article]
- วิดีโอเปรียบเทียบ Seedance 2.5 กับ Seedance 2.0 บน prompt เดียวกันใน 6 หมวด: camera movements, music videos, transformations, UGC, pure cinema, impossible worlds [A05.L01 t=00:27]
- ไม่มี Higgsfield UI, parameter หรือข้อความ prompt บนจอในบทใดเลย (0 cues) — prompt มีแค่ที่พูด paraphrase หรืออนุมานจาก dialogue ที่ generate ออกมา [A05.L01 article] [A05.L02 t=01:23]
- ผลลัพธ์ที่ได้: วิธีรีวิวแบบ "ดูทีละคำถาม" และรูปแบบโน้ต "I saw ___, so I would ___." ก่อนตัดสินคลิปใด ๆ [A05.L01 article]
- ข้อสรุปของคอร์ส: 2.5 ชนะทุกหมวดที่แสดง แต่มี "catch" คือทุกตัวอย่างของ 2.5 เป็น 720p ขณะที่ 2.0 เรนเดอร์ 4K [A05.L11 t=00:00] [A05.L11 t=00:15]
- ปลายทางคือ production decision record แบบ Capability / Constraint / Context / Verdict ที่อิงสิ่งที่สังเกตได้ [A05.L11 article]

### Workflow ทีละขั้น
1. ดูคลิปหนึ่งรอบโดยไม่หยุด แล้วค่อย replay โดยถือคำถามหลักฐานทีละข้อ [A05.L01 article]
2. เลือก pass ทีละอย่าง: camera trajectory, edit continuity, facial performance, body choreography, world coherence, delivery constraint [A05.L01 article]
3. Camera pass: บรรยายเส้นทางกล้องด้วยกริยาทางกายภาพ (push, rise, drop, orbit, whip, settle), ตาม subject detail 1 จุด + scene detail 1 จุด, หยุดทุก cut แล้วถามว่ามันหลบอะไร [A05.L02 article]
4. Continuity pass: ตาม feature ของนักแสดง 1 อย่างผ่านทุกฉาก/cut และทดสอบ lens effect ว่าบิดตามความลึกหรือเป็นแค่ filter ขอบเฟรม [A05.L03 article]
5. Face pass: ปิดเสียงก่อน ตรวจปาก+กราม คอ ตา/คิ้ว ว่า commit พร้อมกัน แล้วดู preparation-peak-release ขณะเคลื่อนไหว; ถ้าหน้าเล็กเกินให้บันทึก "inconclusive" [A05.L04 article]
6. Body pass: เลือกท่าที่ซ้ำ ตรวจ entry, contact, recovery และภาพสะท้อนบนพื้น ณ จังหวะเดียวกัน; replay ก่อน/หลัง cut ที่ตรงกับ contact หนึ่ง beat [A05.L05 article]
7. Transformation pass: list anchor ที่คงที่ก่อน แล้วตรวจ setup -> change -> consequence -> return และว่าผลกระทบ (rubble) ยังอยู่ [A05.L06 article]
8. UGC pass: เริ่มจาก contact frame (วางโทรศัพท์บนหิน) — การเคลื่อนของกล้องต้องสอดคล้องกับมือและพื้นผิว [A05.L07 article]
9. Geography pass: ทำ layer map ใกล้/กลาง/ไกล ใช้จอซ้อนเป็น checksum และตรวจ depth scaling เมื่อกล้องเคลื่อนเร็ว [A05.L08 article]
10. Drama pass: ทุก reverse shot ตรวจ eyeline, ทิศและจังหวะ flicker ของแสง practical, reaction ที่พัฒนา และฉากต้องไปถึง beat สุดท้าย [A05.L09 article]
11. Impossible-world pass: เริ่มจากคน แล้ว freeze เฟรมที่วุ่นที่สุดและถามคำถามเชิงพื้นที่ธรรมดา [A05.L10 article]
12. Delivery pass: ดูที่ขนาดจอและ crop ที่จะใช้จริง บันทึก Capability / Constraint / Context / Verdict แยกผล pass กับ fail และตรวจ spec ปัจจุบันใน product อีกครั้ง [A05.L11 article]
13. เขียนทุก finding เป็น "I saw ___, so I would ___." [A05.L01 article]

### กฎที่ใช้ซ้ำได้
- หนึ่ง replay = หนึ่งคำถามหลักฐาน ห้ามตัดสินกล้อง หน้า ร่างกาย แสง และความละเอียดในรอบเดียว [A05.L01 article]
- แทนคำคุณศัพท์ ("cinematic", "smooth", "bad") ด้วยหลักฐานที่หาเจอได้ เช่น "The orbit keeps one continuous camera path" [A05.L01 article]
- การตัดถี่ ๆ ตรงจังหวะยาก = โมเดลกำลังซ่อน motion ที่มัน animate ไม่ได้ [A05.L02 t=01:29] [A05.L05 t=01:20]
- cut ครั้งเดียวพิสูจน์ได้น้อย แต่ pattern การตัดที่ซ้ำ ๆ มีความหมาย [A05.L02 article]
- long take ไม่ได้ดีกว่าโดยอัตโนมัติ คำถามคือ move ถูก "แสดง" หรือแค่ "ถูกบอกเป็นนัย" ผ่าน edit [A05.L02 article]
- เลนส์จริงบิดตามความลึก (มือบิดก่อนหน้า) ส่วน filter โค้งแค่ขอบเฟรม [A05.L03 t=00:56] [A05.L03 t=01:49]
- เขียนโน้ตให้เพื่อนร่วมทีม verify หรือโต้แย้งได้ หนึ่ง claim ต่อหนึ่ง element [A05.L03 article]
- หลักฐานที่ขาด (หน้าเล็กเกิน) ห้ามแปลงเป็น verdict ให้ใช้ "inconclusive" [A05.L04 article]
- ผลกระทบต้องคงอยู่: เศษซากต้องยังอยู่หลังเหตุการณ์ ไม่มีอะไรถูก "ลบ" ระหว่างเฟรม [A05.L06 t=01:00] [A05.L06 t=01:40]
- ใน UGC กล้องคือโทรศัพท์ที่มีร่างกายถือ: สั่นก่อนวาง นิ่งหลังวาง pan แบบข้อมือ ไม่ใช่ crane [A05.L07 t=00:52] [A05.L07 t=01:00]
- จอซ้อนและภาพสะท้อนคือการเรนเดอร์ action ครั้งที่สอง ใช้เป็น consistency checksum [A05.L05 article] [A05.L08 article]
- อย่านับจำนวนวัตถุพื้นหลัง ให้ดูว่า layer ใกล้/กลาง/ไกลเปลี่ยน scale อย่างที่กล้องตัวเดียวทำได้ไหม [A05.L08 article]
- แสง practical (เทียน) ต้องรักษาทิศและจังหวะ flicker ข้ามทุกมุม [A05.L09 t=00:52]
- ตรวจ eyeline, แสง, reaction แยกกัน เพื่อระบุว่าปัญหาอยู่ที่ performance, screen direction, lighting หรือ edit timing [A05.L09 article]
- โลกซับซ้อนต้องมี anchor เรียบง่าย: คนหนึ่งคน วัตถุหนึ่งชิ้น การเคลื่อนหนึ่งทิศ แหล่งแสงหนึ่งแหล่ง [A05.L10 article]
- premise เหนือจริงไม่ได้ยกเว้น shot จากตรรกะพื้นที่พื้นฐาน; ปริมาณ detail หลอกตาได้ ความสม่ำเสมอคือบททดสอบ [A05.L10 article]
- ตัดสินที่ขนาดส่งมอบจริง: คลิปหนึ่งอาจผ่าน motion แต่ตก resolution — บันทึกทั้งสอง ไม่รวมเป็นคะแนนเดียว [A05.L11 article]

### โครงสร้าง Prompt
- คอร์สไม่แสดง prompt ตรงตัวเลย ทุกโครงด้านล่างคือ paraphrase จากคำพูดหรืออนุมานจาก output — ไม่ใช่ verbatim [A05.L01 article] [A05.L03 t=00:13]
- Music video (paraphrase): "a full 2000 rap video, platinum bold artist, wraparound shades, fisheye lens shoved in his face, dollar signs everywhere, and a different set every few seconds." [A05.L03 t=00:13]
  - โครงที่ใช้ซ้ำได้: [ยุค+ประเภทวิดีโอ] + [ลุคศิลปิน: ผม, accessory เด่น] + [การปฏิบัติต่อเลนส์/กล้อง] + [motif ฉาก] + [จังหวะตัด: เปลี่ยนฉากทุก N วินาที] [A05.L03 t=00:13]
  - ถอดเสียงน่าจะผิด: "2000" น่าจะเป็น "2000s", "bold" น่าจะเป็น "blond" [A05.L03 t=00:13]
- Transformation 1 (paraphrase): "a woman in glasses walks to a parking garage, a demon appears, she transforms, defeats the monster, and then transforms back." [A05.L06 t=00:06]
  - โครง: [ตัวละคร + identity anchor] + [สถานที่] + [ศัตรูปรากฏ] + [เปลี่ยนร่าง] + [ต่อสู้/ชนะ] + [กลับร่างเดิม] = beat sheet ครบในหนึ่ง prompt [A05.L06 t=00:06]
- Transformation 2: prompt มี dialogue script โดยแต่ละบรรทัดที่เอ่ยถึงร่างใหม่ (hero จากเกม, cop, robot) กระตุ้นการเปลี่ยนร่าง เช่น "Want me to be the hero from your favorite game? Or a cop?" [A05.L06 t=01:51]
  - โครง: [ตัวละคร 2 คน + ฉากคงที่] + [บทพูดเรียงลำดับ] + [บรรทัดที่เอ่ยชื่อร่าง = trigger การเปลี่ยนร่าง] [A05.L06 t=01:51]
- UGC (paraphrase): "A hiking creator on a mountain ridge reviewing her glasses." ในรูปแบบแนวตั้ง [A05.L07 t=00:05] [A05.L07 t=00:02]
  - โครง: [ประเภท creator] + [สถานที่] + [การรีวิวสินค้า] + [UGC แนวตั้ง/ถ่ายด้วยโทรศัพท์] + [beat ในบท: hook, features, outro] [A05.L07 t=00:05]
  - pattern บทที่ได้ยินใน output: location hook -> บริบทส่วนตัว -> claim สินค้า (fit) -> "you have to see this" reveal -> features (เบา, wrap กันลม) -> endorsement -> outro [A05.L07 t=00:15]
- Drama: prompt มี dialogue script ที่เขียนการไต่ระดับไว้ในบท: รายงาน -> ข้อเสนอ -> ค้าน -> ผู้นำระเบิด "Enough!" -> คำขาด พร้อม [ฉาก + แสง practical แหล่งเดียว] + [N ตัวละครรอบโต๊ะ] [A05.L09 t=00:02]
- Impossible world (paraphrase): "A gravity-broken city at golden hour. A schoolgirl has to pass a message to an old woman while the whole city is falling apart." [A05.L10 t=00:07]
  - โครง: [premise โลกเหนือจริง] + [แสงตามช่วงเวลา] + [ตัวเอกหนึ่งคน] + [ภารกิจเรื่องง่าย ๆ กับตัวละครที่สอง] + [ความโกลาหลเป็นฉากหลัง] — ตรงกับกฎ anchor "one person, one object, one movement, one light source" [A05.L10 t=00:07]
- Long-form: วางแผน music video 2 นาทีเป็น 4 generation x 30 s [A05.L05 t=01:39]
- UGC spot ทั้งชิ้น hook -> features -> outro ใส่ได้ใน 30 s generation เดียว [A05.L07 t=01:49]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Seedance 2.5: ยาวสุด 30 s ต่อ generation และทุกตัวอย่าง 2.5 ในคอร์สยาว 30 s [A05.L02 t=01:38]
- Seedance 2.5: ทุกตัวอย่างที่แสดงเป็น 720p [A05.L11 t=00:00]
- Seedance 2.0: ยาวสุด 15 s [A05.L02 t=01:41]
- Seedance 2.0: เรนเดอร์ 4K [A05.L11 t=00:15]
- ณ วันบันทึก Seedance 2.5 ขึ้นการ์ด "SEEDANCE 2.5 COMING SOON" (กำลังจะมาบน Higgsfield) [A05.L11 t=00:26]
- ทุกคลิปมี overlay มุมจอ "HIGGSFIELD" + ชื่อโมเดล [A05.L02 t=00:38]
- output มี native audio/dialogue พร้อม lip sync เป็นส่วนที่ถูกประเมิน [A05.L04 t=00:32] [A05.L06 t=01:51] [A05.L09 t=00:38]
- UGC test ใช้เฟรมแนวตั้ง 9:16 [A05.L07 t=00:02]
- ไม่มีการแสดง seed, aspect UI, references หรือ setting อื่นของ Higgsfield ในทุกบท [A05.L01 article] [A05.L11 article]

### คำเตือนและ failure modes
- showcase ถูกออกแบบมาให้ประทับใจตอนดูครั้งแรก งานของเราคือตัดสินว่ามันพิสูจน์อะไรจริง [A05.L01 article]
- 2.0 ตัด "มุมใหม่ทุกวินาที" เพื่อซ่อน motion ที่ทำไม่ได้ [A05.L02 t=01:29]
- 2.0 ใส่ camera move ไม่ครบใน 15 s และ "always struggled" กับ vertical effect [A05.L02 t=02:52] [A05.L02 t=02:58]
- fisheye ของ 2.0 เป็น "more of a filter than a lens" [A05.L03 t=01:49]
- "Screaming is where AI faces usually fall apart" — ทั้งหน้าต้อง commit [A05.L04 t=00:41]
- 2.0: lip sync เพี้ยนเมื่อกล้องเข้าใกล้ และเพลงฟังเหมือนอยู่ไกล [A05.L04 t=01:16] [A05.L04 t=01:23]
- 2.0: แขนขาทะลุกันตอนท่าเร็ว ท่าทาง reset เป็นท่าแปลกระหว่างฉาก [A05.L05 t=01:08]
- 2.0: shimmer makeup "turns to mush" เมื่อหันหน้า [A05.L05 t=01:30]
- 2.0: 15 s ทำให้ transformation รีบ, หนวด "soft and muddy", ปีศาจถูก "deleted" แทนที่จะถูกทำลาย [A05.L06 t=01:33] [A05.L06 t=01:40]
- 2.0 test 2: เปลี่ยนร่างแบบ hard cut, "teleports between forms", พื้นหลังกะพริบ [A05.L06 t=03:03]
- 2.0 UGC: 15 s ตัดส่วนสินค้าทิ้งทั้งหมด [A05.L07 t=01:27]
- seam เล็ก ๆ รวมกัน (หน้าแข็ง, ปากไม่ตรงเสียง, นิ้วบิดรอบสาย, geometry พังตอนวางโทรศัพท์) = "the difference between an ad and an AI ad" [A05.L07 t=01:30]
- 15 s บังคับให้ pull-back เร่ง: depth ถูกบีบ crew "flies past" รายละเอียดไกลพัง [A05.L08 t=01:20]
- 2.0 drama: 15 s หมดตรง peak ("Enough!") ฉากไม่มีตอนจบ, หน้า "hold one expression per line", แสง "plasticky and sloppy" [A05.L09 t=01:24] [A05.L09 t=01:32] [A05.L09 t=01:37]
- 2.0 impossible world: "almost everything that could break broke" (ไม่ได้แจกแจงในคำพูด) [A05.L10 t=01:23]
- 720p: หน้ากลายเป็น soft/smudgy บนทีวีหรือใน wide shot แม้บนมือถือแทบไม่เห็น [A05.L11 t=00:07]
- spec และความพร้อมของโมเดลเปลี่ยนได้ ต้องตรวจ interface ปัจจุบันก่อนสัญญา delivery format [A05.L11 article]
- "it looks better" ไม่ให้อะไรทีมนำไปทำต่อได้ [A05.L11 article]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- ข้อจำกัดความยาว 2.5 = 30 s เทียบ 2.0 = 15 s มีในวิดีโอ ไม่มีใน article และเป็นสาเหตุหลักของความล้มเหลวของ 2.0 ในหลายหมวด [A05.L02 t=01:38] [A05.L07 t=01:27] [A05.L09 t=01:24]
- "catch" ที่เปิดไว้ใน L01 คือ 720p ของ 2.5 vs 4K ของ 2.0 และ host ตัดสินว่า "might just be worth it" [A05.L01 t=00:20] [A05.L11 t=00:19]
- 720p ถูกเทียบว่าเป็น "the resolution YouTube called HD in 2010" [A05.L11 t=00:03]
- prompt ที่พูด paraphrase ของ hip-hop, transformation, UGC และ impossible world (article ไม่ระบุ) [A05.L03 t=00:13] [A05.L06 t=00:06] [A05.L07 t=00:05] [A05.L10 t=00:07]
- บท UGC ฉบับเต็มที่ได้ยินใน output เช่น "Okay, so we're at like 2,000 meters right now." ... "Okay, back to the trail." [A05.L07 t=00:15]
- dialogue script ฉบับเต็มของฉาก war council (article ไม่มีบทพูด) [A05.L09 t=00:02]
- test ที่สองของ transformation (dialogue + shape-shifting: hero, cop, cat, robot) ไม่มีใน article ทั้งหมด และ 2.5 สร้างเกิน prompt โดยรวม cat + robot เป็น "cyborg cat" [A05.L06 t=01:49] [A05.L06 t=02:38]
- fisheye tell เชิงรูปธรรม: เมื่อนักแสดงโน้มเข้าหากล้อง มือบิดก่อนหน้า [A05.L03 t=00:56]
- สัญญาณคุณภาพเพิ่ม: spotlight beam เห็นในอากาศ และ "Reflections used to be a dead giveaway. Now, they're kind of a flex." [A05.L05 t=00:41] [A05.L05 t=00:46]
- ตัวอย่างความล้มเหลวของ detail ผิว: shimmer makeup เละเมื่อหันหน้า (ไม่มีใน article) [A05.L05 t=01:30]
- การ์ดบนจอ "30 SEC X 4 = 2 MIN" สำหรับวางแผน music video 2 นาที [A05.L05 t=01:39]
- การ์ดบนจอ "HOOK — FEATURE — OUTRO" สำหรับ UGC spot 30 s [A05.L07 t=01:49]
- การตีความจอ monitor ในฉาก pull-back: โมเดล "keeping two copies of the same scene alive at once and syncing them" [A05.L08 t=00:50]
- UGC เป็น "home turf" ของ 2.0 อยู่แล้ว ช่องว่างจึงเล็กกว่า; "for anyone doing brand work, this category alone pays for the switch" [A05.L07 t=01:20] [A05.L07 t=01:46]
- สำหรับคนทำ short drama: "this category is your whole pipeline" ด้วย 30 s ในครั้งเดียว [A05.L09 t=01:40]
- ผล impossible world: "One prompt, one generation, 30 seconds, no editing, no comping, no fixing in post" [A05.L10 t=01:32]
- transformation "used to be the thing you cut around and fixed in post" ตอนนี้ "just one sentence in a prompt" [A05.L06 t=03:24]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- ชื่อ host ไม่ตรงกัน: วิดีโอแนะนำตัวว่า "Adil" แต่ metadata ของคอร์สเครดิต Ziya Rufat [A05.L01 t=00:10]
- L10: article บอกว่าส่งข้อความให้ "older woman" แต่ sheet แสดงชายชรากับสุนัขบนถนน และเฟรม handoff จริงไม่ถูกจับใน sheet [A05.L10 article]
- L05: มีเฟรม 2.0 สีขาวทั้งเฟรมราว ~65 s — ไม่ชัดว่าเป็น transition หรือ artifact [A05.L05 frames t=01:05]
- ไม่มี prompt verbatim เลย มีแค่ paraphrase และ dialogue ใน output — ไม่รู้ถ้อยคำ ความยาว หรือว่าระบุ shot list หรือไม่ [A05.L02 t=01:23] [A05.L05 t=00:50]
- สัญญาณ cat ใน transformation 2 ไม่ชัด: ถอดเสียงได้ "Furry," (น่าจะเป็น "Or furry,") และ hires frames t=02:00–02:06 ไม่มี caption บนจอ [A05.L06 t=02:02]
- ไม่ชัดว่า 720p ของ 2.5 เป็นข้อจำกัดถาวรหรือ setting ก่อน release; article เองให้ตรวจใน product ปัจจุบัน [A05.L11 article]
- ไม่ได้ระบุ aspect ratio/resolution ที่ใช้ใน test ที่ไม่ใช่ UGC [A05.L11 t=00:00]
- ชื่อตัวละครในฉาก drama ("Annas", "Yernat"/"Jönet") สะกดจากการเดาเสียง — ไม่ยืนยัน [A05.L09 t=00:02]
- การอนุมาน "Kixote" = Higgsfield มาจาก end card "HIGGSFIELD.AI" ไม่ใช่คำพูดที่ชัด [A05.L11 t=00:26]
- transcript ขาดหลายช่วงทำให้ประโยคไม่ครบ เช่น คำบรรยาย opening move ของฉาก 2 และประโยค "No other model on the market works ..." ที่ถูกตัด [A05.L02 t=02:27] [A05.L09 t=00:58]

### เทียบกับ v1
- เหมือนเดิม: แยกคำถามเป็นกล้อง edit ใบหน้า ร่างกาย โลก delivery และเขียนว่าเห็นอะไรจึงตัดสินอะไร [A05.L01 article]
- เพิ่ม: ระบุว่าทั้งคอร์สคือการเทียบ Seedance 2.5 vs 2.0 บน prompt เดียวกันใน 6 หมวด (v1 ไม่บอกโมเดลที่ถูกเทียบ) [A05.L01 t=00:27]
- เพิ่ม: ข้อจำกัด 30 s vs 15 s และ 720p vs 4K พร้อมว่าเป็นตัวเลข ณ วันบันทึก [A05.L02 t=01:38] [A05.L11 t=00:00]
- เพิ่ม: กฎ "ตัดถี่ตรงจุดยาก = ซ่อน motion" จากคำพูด host [A05.L02 t=01:29]
- เหมือนเดิม: fisheye จริงบิดตามความลึก vs ขอบโค้ง; v2 เพิ่ม tell "มือบิดก่อนหน้า" [A05.L03 t=00:56]
- เหมือนเดิม: ปิดเสียงอ่านปาก กราม ตา คอ และบันทึก inconclusive เมื่อหน้าเล็ก [A05.L04 article]
- แก้: v1 สรุป choreography เป็น "เข้าท่า สัมผัส ลงน้ำหนัก คืนสมดุล" (4 จังหวะ) แต่ article ใช้ 3 จังหวะ Entry / Contact / Recovery [A05.L05 article]
- เพิ่ม: โครง prompt ที่ paraphrase ได้ 4 ตัว + pattern บท UGC และบท drama [A05.L07 t=00:15] [A05.L09 t=00:02]
- เพิ่ม: Capability / Constraint / Context / Verdict สี่ช่องสำหรับ decision record (v1 พูดแค่ "รายงานหลายมิติ") [A05.L11 article]
- เพิ่ม: หลักฐานขัดแย้ง old woman vs ชายชรากับสุนัขใน L10 และชื่อ host ไม่ตรง [A05.L10 t=00:07] [A05.L01 t=00:10]

## A06 The 3-Step Realistic AI Ad Workflow

### ภาพรวมและผลลัพธ์
- คอร์สสร้างโฆษณาหูฟัง (over-ear สีครีม/ส้ม) ความยาวราว 50 s ที่ generate ด้วย AI ทั้งหมด แล้วถอดเป็นระบบ 3 ขั้น [A06.L01 t=01:22] [A06.L01 frames t=00:00]
- Step 1 = assets (product, characters, locations, props) ทำใน Soul Cinema และ GPT Image 2.0 [A06.L01 t=01:22]
- Step 2 = Claude skill ที่แปลงเรื่องเป็น prompts (แจกฟรีใน description) [A06.L01 t=01:13]
- Step 3 = generate ฉากใน Seedance 2.0 ภายใน Higgsfield AI [A06.L01 t=01:32]
- ลำดับตายตัว: assets ก่อน, prompts ที่สอง, generation ท้ายสุด — ข้ามขั้นแล้วหน้าเปลี่ยนทุกฉาก [A06.L01 article]
- concept ของโฆษณา: ทุกอย่างดังพร้อมกัน (เครื่องตัดหญ้า, จราจร, หัวหน้า) แตะหูฟังทีเดียวโลกเงียบ หนึ่ง beat ต่อฉาก [A06.L10 t=01:09]
- ผลลัพธ์สุดท้าย = "the best few seconds out of 100 tries" — การ iterate คือทักษะ และ workflow ใช้กับสินค้าใดก็ได้ [A06.L16 t=01:30] [A06.L16 t=01:37]

### Workflow ทีละขั้น
1. เขียนสคริปต์ก่อน: ไอเดียเดียวชัด ๆ หนึ่ง beat ต่อฉาก [A06.L10 t=01:03]
2. จัด project ใน Higgsfield เป็นโฟลเดอร์ต่อประเภท/สถานที่ก่อน generate อะไร (เช่น ASSETS, HERO, BOSS, KITCHEN, STADIUM, STREET, OFFICE, PROPS, SCENES) [A06.L02 t=00:13] [A06.L11 frames t=00:21]
3. Product sheet: อัปโหลดรูปสินค้า 1 รูปเข้า GPT Image 2.0 แล้วขอ front + 3/4 views [A06.L02 cue product-sheet-prompt]
4. Hero sheet: ให้ Claude เขียน prompt character sheet (face close-up + full body front/back บนพื้นเทา) แล้วรันใน Soul Cinema หลาย batch [A06.L03 cue character-sheet-prompt] [A06.L03 t=00:47]
5. เก็บ finalist อย่างน้อย 2 คนวางบน canvas เพื่อตัดสินด้วย motion test ไม่ใช่ภาพนิ่ง [A06.L03 t=00:59]
6. ตัวละครรอง: prompt บรรทัดเดียวใน AI Cast แล้วเลือกตาม "energy" [A06.L04 cue boss-prompt] [A06.L04 t=00:27]
7. Locations: prompt สั้นที่มุม 3/4, bright/clean/high-end commercial, หลาย batch; สถานที่ซับซ้อนให้ Claude ขยาย 3 keyword เป็น prompt ยาว [A06.L05 cue kitchen-location-prompt] [A06.L07 cue stadium-location-prompt]
8. Motion test ชุด hero x location ใน Seedance 2.0 ด้วย prompt ง่าย ๆ ที่คงที่ เปลี่ยนตัวแปรทีละตัว แล้วลากผู้ชนะขึ้นบนสุดของ canvas = locked [A06.L05 cue kitchen-test-prompt] [A06.L05 t=01:52]
9. แก้ location ที่ล็อกแล้วด้วย GPT Image 2.0 ให้รองรับ action ของฉาก ลงท้าย "Keep everything else the same." [A06.L05 cue kitchen-edit-prompt]
10. ลบหน้าออกจาก panel full-body ของทุก character sheet ให้เหลือหน้าเดียว [A06.L06 cue erase-face-prompt]
11. Wardrobe: ให้ Claude เขียน outfit prompt N ชุดจาก sheet, รันใน GPT Image 2.0, รวมส่วนที่ดีผ่าน Claude, แล้ว composite ชุดใหม่ใต้ภาพ Soul Cinema ต้นฉบับด้วย mask [A06.L08 cue outfit-ideas-prompt] [A06.L08 t=01:29]
12. Props: GPT Image 2.0 sheet สะอาดชิ้นละหนึ่ง ไม่ต้อง motion test [A06.L09 t=00:08]
13. Shotlist: โหลด skill "higgsfield-seedance-shotlist-director" เข้า Claude แล้วในแชตใหม่ให้ 3 อย่าง: script (PDF), ภาพ asset ที่ล็อกทุกชิ้น, ชื่อ @name ของแต่ละชิ้น [A06.L10 cue download-shotlist-skill] [A06.L10 t=01:00]
14. บันทึกทุก asset เป็น Higgsfield Element ด้วยชื่อเดียวกับใน Claude; วาง prompt แล้ว Element จะ attach อัตโนมัติ [A06.L11 t=00:21] [A06.L11 t=00:33]
15. รันแต่ละ prompt ใน Seedance 2.0, วินิจฉัยว่าผิดตรงไหน, ปัญหารวมแก้ที่ style prefix ครั้งเดียว ปัญหาเฉพาะช็อตแก้ที่ prompt ที่มีชื่อ [A06.L11 cue style-prefix-fix] [A06.L11 cue edit-prompt-1a]
16. ช่วงที่แย่ให้ดึงออกเป็น prompt ของตัวเอง และ prop ที่ drift ให้ล็อกเป็น Element ใหม่ [A06.L11 t=02:21] [A06.L11 cue moka-mug-request]
17. ต่อฉาก: ทำ sheet ชุด/สภาพเพิ่ม (แห้ง vs เปียก), override แสงของ prefix เฉพาะฉาก, match tap เปิดฉากกับ tap ปิดฉากก่อนหน้า, เพิ่ม coverage และช็อตที่สินค้าเป็นพระเอก [A06.L12 t=01:09] [A06.L12 t=02:15] [A06.L12 t=02:55] [A06.L12 t=03:52]
18. ปัญหาเชิงพื้นที่: สร้าง schematic map ใน GPT Image 2.0 แล้วให้ Claude เขียน prompt ใหม่รอบแผนที่; ยึดตัวเอกกับ landmark; ล็อก prop ทุก cut; ตั้งชื่อท่าเต้น; ใส่ music track เป็น audio input [A06.L13 cue street-schematic-prompt] [A06.L13 cue street-claude-rewrite-prompt] [A06.L13 t=04:05]
19. นำ map เดิมกลับมาใช้ในฉากถัดไป [A06.L15 cue scene5-boss-dance-prompt]
20. ตัดแต่ละฉากจาก keeper phase ของหลาย generation ตัดบน action แล้วเรียงฉากบน timeline [A06.L11 t=04:00] [A06.L11 t=05:21] [A06.L12 t=04:48]

### กฎที่ใช้ซ้ำได้
- ลำดับตายตัว assets -> shotlist -> scenes; ห้าม generate ฉากก่อนล็อก asset [A06.L01 article]
- ไม่มี shot list = Seedance ไม่มีอะไรมีโครงสร้างให้ animate [A06.L01 article]
- รูปสินค้ารูปเดียวไม่พอ ต้องให้โมเดลเห็นหลายมุม ไม่งั้นมันเดาและ hallucinate กลางฉาก [A06.L02 t=00:23]
- ไม่เขียน prompt sheet เอง: บอก Claude เป็นภาษาธรรมดาแล้วให้ Claude เขียนรายละเอียด [A06.L03 t=00:06]
- character sheet บนพื้นเทาเรียบ — host บอก win rate "way higher on gray" [A06.L03 t=00:38]
- เก็บ finalist ไม่ใช่ตัวเลือกเดียว และตัดสินด้วย motion test เพราะภาพนิ่งอาจพังเมื่อขยับ [A06.L03 t=00:59] [A06.L07 t=00:42]
- ใช้แรงตามบทบาท: hero ได้ความประณีต ตัวละครรองผ่านแบบเร็ว [A06.L04 t=00:00]
- ตัวร้ายต้องอ่านออกว่าเป็นปัญหาตั้งแต่แรกเห็น ทิ้งตัวเลือกที่ดูเป็นมิตรเกินไป [A06.L04 t=00:27]
- location ที่ดูปลอม/พลาสติก ไม่มี prompting ใดช่วยได้ [A06.L05 t=00:04]
- generate location ที่มุม 3/4 ไม่ใช่ head-on เพื่อให้มี depth ตอนกล้องขยับ — "way better win rate" [A06.L05 t=00:30]
- test ทีละตัวแปร (hero หรือ location) ไม่เปลี่ยนสองอย่างพร้อมกัน — "the part most people skip" [A06.L05 t=01:08]
- เลือก location ตามความต้องการของฉาก เช่น แสงสว่างที่ "feels like morning" สำหรับฉากเช้า [A06.L07 t=00:58]
- test ทุก location ก่อนเพื่อไม่เสียเครดิตกับฉากเต็มบน asset ผิด [A06.L07 t=01:21]
- หนึ่ง character sheet = หนึ่งใบหน้า; สองหน้าใน sheet ทำให้โมเดลไม่รู้จะจับหน้าไหนและ identity drift [A06.L06 t=00:13]
- ทดสอบด้วยชุดดำเรียบก่อน แต่งตัวจริงหลังล็อกตัวละครและสถานที่แล้ว [A06.L08 t=00:00]
- ทุกการ edit ลดคุณภาพ — GPT Image edit ทำผิว Soul Cinema นิ่มจนเป็น "AI slop"; แก้ด้วยการซ้อน layer + mask [A06.L08 t=01:06] [A06.L08 t=01:29]
- prop ไม่ต้อง motion test เพราะไม่ได้ "แสดง"; ทำมุมพอให้ครอบคลุมกล้องเท่านั้น [A06.L09 t=00:08] [A06.L09 article]
- อัปโหลด asset ให้ Claude อย่าบรรยายเป็นคำ — การบรรยายคือเหตุที่ prompt ออกมา generic [A06.L10 t=01:23]
- ใช้ชื่อ asset ใน Claude ตรงกับชื่อ Element ใน Higgsfield [A06.L10 article]
- style prefix ติดกับทุก prompt: แก้ครั้งเดียวเปลี่ยนทุกที่; ทุก prompt มีชื่อ (1a, 1b, 2a) เพื่อแก้เฉพาะตัว; ทำงานในเอกสารเดียว ไม่ใช่ 20 แชต [A06.L10 t=02:02] [A06.L10 t=02:15] [A06.L10 t=02:27]
- รันแต่ละ prompt ที่แก้แล้วหลายครั้ง และเก็บชิ้นจากคนละรอบมาประกอบ [A06.L11 t=02:14]
- ห้ามบรรยาย motion แบบย่อ ("he dances" ไม่มีความหมายกับ Seedance) — เขียนทีละท่าโดยไม่เปลี่ยนเรื่อง [A06.L11 t=04:36] [A06.L14 t=00:37]
- ถ้าตัวละครต้องเปลี่ยนกลางฉาก (แห้ง -> เปียก) ให้สร้าง reference ใบที่สอง อย่าสั่งด้วยคำ — "images are cheap, videos aren't" [A06.L12 t=01:09]
- บอก Claude ชัดว่า reference ไหนใช้กับ cut ไหน [A06.L12 t=01:56]
- style prefix คือค่า default; override เฉพาะฉากที่ต้องการลุคของตัวเอง [A06.L12 t=02:15]
- แก้ cut ไม่ใช่แค่ช็อต: เปิดแต่ละฉากด้วย tap ที่ตรงกับ tap สุดท้ายของฉากก่อน (มือเดียวกัน ท่าเดียวกัน) เพื่อ match cut [A06.L12 t=02:55] [A06.L14 t=00:53]
- ข้อความตรึงสถานที่ไม่ได้ ให้แผนที่ (schematic) แทน — "the number one hack to steal from this video" [A06.L13 t=00:35]
- ยึดตัวเอกกับตำแหน่งทางกายภาพ (ยืนใต้ต้นไม้ทางซ้าย) และล็อก prop ทุก cut อย่างชัดเจน [A06.L13 t=02:10] [A06.L13 t=03:01]
- เมื่อเวลามีผล ให้ใส่ music track จริงเป็น audio input และสั่งให้เต้นตาม beat [A06.L13 t=04:05]
- iterate prompt เดียวสามรอบ ดีกว่าเขียนสาม prompt แยก [A06.L13 t=04:55]
- "Two fixes, one edit": รวม match-cut opening กับ entrance ที่กำกับท่าไว้ในการแก้ครั้งเดียว [A06.L14 t=00:49]
- เมื่อไม่มีอะไรต้องแก้แล้ว brief ให้สั้น; มุกที่ขายตัวเองได้ใช้การกำกับท่าเต้นแบบทั่วไปได้ [A06.L15 t=00:13] [A06.L15 article]

### โครงสร้าง Prompt
- Product sheet (GPT Image 2): `Make a product sheet with [view list: front and 3/4 perspective] views of the [product] from @image_1.` [A06.L02 cue product-sheet-prompt]
- Meta-prompt ให้ Claude เขียน character sheet: `create a prompt for a character sheet of a [age/gender] with [face trait] — two panels, close-up and full body - front and back, on a grey background.` [A06.L03 cue character-sheet-prompt]
- โครงของ prompt ที่ Claude คืนมา (บนจอ อ่านได้บางส่วน): [sheet type + layout + style] / Left panel [หน้า + กฎ "entire head fully inside the frame ... nothing cropped" + ผิวจริง + สีหน้า + 85mm/แสง] / Right panel [front + back, ท่ายืน, สูงเต็มเฟรม, build เป็นเมตร (1.85m), "same streetwear outfit"] [A06.L03 frames t=00:15]
- ตัวละครรองใน AI Cast: `An [role] in his [age] with a [body trait], wearing a [wardrobe].` [A06.L04 cue boss-prompt]
- Location still: `[Room type], [camera angle 3/4], [light: bright clean daylight], [look: high-end commercial look].` [A06.L05 cue kitchen-location-prompt]
- Motion test: `the hero [@image ref] walks into the kitchen [@image ref], headphones [@image ref] on, dance a little` — คงที่ทุก test ทุกคำนามผูก @reference [A06.L05 cue kitchen-test-prompt]
- Location edit: รายการแก้เชิงพื้นที่เป็นข้อ `[clear X so Y]. On the [left/right] [surface] [add/remove] [object]. ... Keep everything else the same.` [A06.L05 cue kitchen-edit-prompt]
- ลบหน้าซ้ำ: `Erase the [element: face] from the [panel: full-body shot] on the [location: right panel].` [A06.L06 cue erase-face-prompt]
- Meta-prompt location ให้ Claude: `Give me a prompt for location. [Place]. [Angle: 3/4 view]. [Weather/time].` [A06.L07 cue stadium-location-prompt]
- prompt สนามที่ Claude คืนมา (บนจอ) จัดเป็น section: [shot type + place + time] / THE FOREGROUND & ROOF / THE TRACK / THE FIELD / THE BACKDROP / THE LIGHT & SKY / COLOR GRADE ("not a glossy ad look") / CAMERA & LENS (ARRI large-format, spherical prime) / "Photorealistic." [A06.L07 frames t=00:25]
- location ง่าย ๆ (บนจอ): "Pedestrian street, 3/4 view" และ "Warm color palette office, 3/4 view" = `[descriptor] [place], 3/4 view` [A06.L07 frames t=01:10]
- Location motion test: `he [@image char ref] [simple action] along the [location] in headphones` [A06.L07 cue stadium-test-prompt]
- Outfit ideas ให้ Claude: `Give me [N] [style] outfit ideas for this character. Write each as a prompt.` [A06.L08 cue outfit-ideas-prompt]
- รวมชุด: `Take the [garment] from the [Nth] look, make it [colour], and keep the [garment] from the [Mth]. Combine them into one prompt.` (แนบทั้งสองลุคเป็นภาพ) [A06.L08 cue outfit-combine-prompt]
- outfit prompt ที่ Claude เขียน (บนจอ): [Image 1 identity-preserve clause + traits] / [Look: รายการเสื้อผ้า เนื้อผ้า สี รองเท้า] / "No visible brand logos anywhere." / [Lighting] [A06.L08 frames t=00:25]
- ข้อความ input ให้ shotlist skill (บนจอ): `[/skill] The PDF is the script. add @name — [role/คำอธิบายบรรทัดเดียว]` ต่อ asset พร้อมแนบภาพ เช่น "@headphones — the product, cream with the orange ring" [A06.L10 frames t=01:35]
- Global Style Prefix (บนจอ) เป็นบรรทัดมี label: Style / Lighting / Color (60:30:10) / Camera (180° shutter) / Skin / Acting / Physics / Composition / Continuity ("No identity drift") / Technical (24fps) / Audio ("Diegetic dialogue and environmental SFX only. No music. No subtitles.") [A06.L10 frames t=02:00]
- โครง prompt ช็อตเต็ม (1A บนจอ): STYLE PREFIX / CHARACTERS (@tags + wardrobe) / SCENE (@location + blocking + props) / `CUT n — [shot size, lens mm, angle/move]: [action beat]` [A06.L10 frames t=01:45]
- บล็อก "Asset references — described to match the source images" บรรยายแต่ละ @asset ให้ตรงภาพต้นทางเพื่อพก identity ข้ามทุก cut [A06.L10 frames t=02:00]
- แก้ทั้ง shotlist: `change the style prefix for the whole shotlist — kill the [unwanted look], go [new look] lit from [direction], [adjectives]. apply to every prompt.` [A06.L11 cue style-prefix-fix]
- แก้เฉพาะช็อต: `edit prompt [id] — [new camera move], no [rejected move]. and cut [beat] down to a quick [N]-stage jump-cut tease — [stage 1], [stage 2], [stage 3].` [A06.L11 cue edit-prompt-1a]
- ให้ Claude เขียน prompt prop: `create the prompts for a [prop] and a [prop] that match the [location].` [A06.L11 cue moka-mug-request]
- Prop reference (GPT Image 2, 16:9): `The [prop] — [material], with [distinctive detail]. Clean studio light, neutral background, centered, product photography.` [A06.L11 cue mug-prompt]
- Prop reference แบบละเอียด: `The [prop] — [shape], [base finish/colour], [top finish/colour], [handle/knob], [small detail]. Studio product shot, soft directional light, neutral background, sharp focus.` [A06.L11 cue moka-pot-prompt]
- Montage prompt: `add intermediate prompt [id] — turn [beat] into a fast-cut montage. [shot 1 angle]. [shot 2 angle + trigger]. [shot 3]. [shot 4]. cut fast, [emotion]. lock @[element] and @[element] as exact references.` [A06.L11 t=03:28]
- เขียนใหม่พร้อมท่าเต้น: `rewrite prompt [id] — [beat]. [action chain]. add dance moves: [move list]. [tone]. end on [final action].` เช่น "two head nods, shoulders rolling one at a time, a knee-dip, a finger-snap, a quarter-spin at the door" [A06.L11 t=04:50]
- Outfit edit ให้ Claude: `give me a prompt to edit this character sheet so that he is wearing a [colour] [style] outfit, with these [attached prop].` [A06.L12 t=00:27]
- prompt sheet ที่ Claude คืนมา (บนจอ): triptych บนพื้นเทา + เส้นแบ่ง, Image 1 = face ref / Left: headshot รักษา traits / Middle: HEADLESS front full body + เสื้อผ้า / Right: HEADLESS back view — กฎหนึ่งหน้าถูกเขียนลงใน prompt [A06.L12 frames t=02:00]
- สภาพเปลี่ยน: `same character sheet, [state], [visible cue 1], [visible cue 2].` เช่น "same character sheet, post-run, sweaty chest, sweat stains on the shirt." [A06.L12 t=01:30]
- กำหนด reference ต่อ cut: "for 2a use the dry @s_hero for the warm-up and run cuts, switch to @s_hero_wet for the final decel-and-stop." [A06.L12 t=01:58]
- Override แสงเฉพาะฉาก: `for scene [n] only — override the prefix lighting. [light quality], [sun position], [sky], [shadows], [colour].` [A06.L12 t=02:38]
- โครง cut product-hero (บนจอ): `CUT n — [shot name], [take length], [FOV], [mount]: [rig behaviour] + [@product framing]` เช่น body-rig snorricam 29° FOV ล็อกที่ ear cup [A06.L12 frames t=04:05]
- Schematic: `Make a schematic. Mark the [landmark] and lock the [prop] to its [side] — [N] times a person's height, on the same line.` [A06.L13 cue street-schematic-prompt]
- เขียนฉากใหม่บนแผนที่: `Rewrite the [scene] prompt on the schematic. Lighting is [time], [sun position], [shadow], no [unwanted light]. Hero moves [direction] [action], [element] on his left and [element] on the right. Camera [behaviour]. [Background life] throughout.` [A06.L13 cue street-claude-rewrite-prompt]
- Pass 2: [ตำแหน่ง anchor + แสง] / `cut n: [shot size/angle], [action]` ทีละ cut / บรรทัดล็อก continuity ("lock the backpack on both shoulders in every single cut") [A06.L13 t=02:27]
- Pass 3: ต่อ cut ตั้งชื่อสไตล์เต้น + 2-3 ท่าเป็นรูปธรรม / "add the music track as an input - @audio_1 and have the hero dance in time with its beat" / คำสั่งกล้อง cut สุดท้าย [A06.L13 t=03:38]
- หัว prompt ผลลัพธ์ (บนจอ): STYLE PREFIX (override ของฉาก) / Audio ref (@music_track) / Location reference (@street_schematic + landmark + "@skydancer POSITION LOCKED") / Characters / cuts [A06.L13 frames t=04:35]
- Match-cut entrance: `edit [id] — open on [action] that matches the last cut of Scene [n] exactly, same pose, so it match-cuts clean. then [entrance], camera [behaviour]. he's [action] the whole way: [move 1], [move 2], ... landing on [final expression].` [A06.L14 t=00:53]
- Payoff: `For scene [n] - make [shot size], [angle] shot. The [character]—[prop on], [wardrobe state]—doing a [dance quality] right next to the [prop]. [Background reaction]. Lock him to the [side] of [prop] using the scene-[n] schematic.` [A06.L15 cue scene5-boss-dance-prompt]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Soul Cinema: hero sheet; 8 images = 1 credit [A06.L03 t=00:47]
- GPT Image 2.0 ("GPT Image 2"): product sheet, location edit, ลบหน้า, outfit, props, sheet นักกีฬา/เปียก, schematic — "best model right now for product editing" [A06.L02 t=00:37] [A06.L13 t=01:03]
- GPT Image 2 bar ใน product sheet: Auto, High, 2K, count 4/4, GENERATE แสดง 28 [A06.L02 frames t=00:44]
- GPT Image 2 bar สำหรับ edit/ลบหน้า/schematic: Auto, High, 2K, count 1/4, GENERATE แสดง 7 [A06.L05 frames t=02:17] [A06.L06 frames t=00:24] [A06.L13 frames t=01:05]
- AI Cast (แผง "CREATE YOUR SOUL CAST", ปุ่ม "Build Your Cast"): ที่ boss prompt count 2/10, GENERATE แสดง 0.25 [A06.L04 frames t=00:21]
- AI Cast มี genre presets (Action, Comedy, Drama, Thriller, Horror...) และแท็บ Details (Facial scar, Freckles, Tattoos, Eye patch) แต่ host ไม่ได้ใช้ พิมพ์บรรทัดเดียว [A06.L04 frames t=00:10]
- โหมด "Cinematic Locations": 2K, count 10/10, GENERATE 1.25 [A06.L05 frames t=00:23]
- Seedance 2.0 motion test (kitchen): 16:9, 1080p, 8s, count 1/4, High, audio On, GENERATE 176 (มีค่าขีดฆ่าจาง ๆ 208) [A06.L05 frames t=01:02]
- Seedance 2.0 location test (stadium): 16:9, 1080p, 10s, High, audio on, GENERATE 90 [A06.L07 frames t=00:53]
- Seedance 2.0 ฉากจริง: 16:9, 1080p, 15s, count 4/4, audio On [A06.L11 frames t=00:40]
- Seedance 2.0 ฉาก street: 15s, count 4/4, GENERATE แสดง 540 ข้างค่าขีดฆ่า 720 [A06.L13 frames t=04:39]
- Seedance 2.0 รับ audio input ได้ (music track เป็น @audio_1 / @music_track) [A06.L13 t=04:05]
- Claude (claude.ai chat, model picker แสดง "Opus 4.8") เขียน prompt ยาวทั้งหมด [A06.L03 frames t=00:08] [A06.L11 frames t=01:13]
- Claude skill: `higgsfield-seedance-shotlist-director.skill` เรียกในแชตเป็น /seedance-director-shotlist [A06.L10 cue download-shotlist-skill] [A06.L10 frames t=01:35]
- Shotlist output เป็นเอกสาร interactive (HTML) มี checkbox ต่อฉาก, ปุ่ม Copy ต่อ prompt, SFX notes ที่ไม่ถูก copy [A06.L10 frames t=02:00] [A06.L11 frames t=01:00]
- Higgsfield Elements: แท็บ Uploads / Elements / Image Generations / Video Generations / Liked, ปุ่ม "Create Element", dialog ตั้งชื่อ [A06.L11 frames t=00:21]
- photo editor ทั่วไปที่มี layer mask สำหรับ composite ชุด [A06.L08 t=01:37]
- ยอดรวมทั้งโฆษณาบนจอ: GENERATIONS 56, CREDITS ≥6,725 (ตัวนับยังวิ่งอยู่ตอนตัด ไม่เห็นค่าสุดท้าย) — ตัวเลข ณ วันบันทึก [A06.L16 frames t=01:04]

### คำเตือนและ failure modes
- asset ไม่ล็อก = หน้าต่างไปทุกฉาก [A06.L01 article]
- ป้อนภาพแบนภาพเดียว = โมเดลเดามุมที่ไม่เห็นและ hallucinate สินค้ากลางฉาก [A06.L02 t=00:26]
- ไฟล์กระจัดกระจายเสียเวลาครึ่งวันกลางการตัดต่อ [A06.L02 t=00:16]
- หน้าที่ดูดีในภาพนิ่งอาจพังทันทีที่ขยับ [A06.L03 t=01:00]
- พื้นหลังรกแย่งความสนใจจากตัวละครและลดผลที่ใช้ได้ [A06.L03 t=00:41]
- ครัวมืด: ทั้งช็อตจมเงาและหน้าหายไป [A06.L05 t=01:27]
- location ที่ generate อาจไม่รองรับ action (ไม่มีเตา ไม่มีประตู) ต้องแก้ก่อนไปต่อ [A06.L05 t=01:55]
- สองหน้าใน sheet: โมเดล drift ผสมหรือสลับรายละเอียดช็อตต่อช็อต — "pro tip, learned the hard way" [A06.L06 t=00:07] [A06.L06 t=00:13]
- location ที่สวยในภาพนิ่งอาจแพ้ video test เพราะแสงแบนเมื่อเคลื่อน [A06.L07 t=00:45]
- GPT Image edit ทำทุกอย่างนิ่มจนเป็นลุคพลาสติก "AI slop" [A06.L08 t=01:16]
- พิมพ์ prompt Seedance จากศูนย์และยัดเยียดเกินจะเผาเครดิต 20 generation ต่อมาไอเดียเละ [A06.L10 t=00:10]
- prop drift รูปทรง/สีระหว่าง take และใน close-up จะเห็นก่อนอย่างอื่น [A06.L11 t=02:36]
- กล้องนิ่งและ beat ที่ยัดแน่นทำให้ช็อตต้องทำมากเกินไป [A06.L11 t=00:53]
- note ของ Claude บนจอ: ช็อต detail สุดขั้ว (1b moka 12°, 2b ear-cup CU 18°) เสี่ยงที่สุด ให้ re-roll ก่อนถ้านิ่มหรือบิด [A06.L11 frames t=01:00]
- ไม่ล็อก outfit reference = take ที่ต่อกันมีกางเกง/รองเท้าต่างกันทุก generation [A06.L12 t=00:38]
- สั่งให้ใส่เหงื่อด้วยคำบน reference แห้ง = โมเดล improvise หน้าหยดน้ำ รายละเอียดผิด [A06.L12 t=01:20]
- tap ไม่ตรงกันระหว่างฉาก (คนละมือ ท่าเพี้ยน) ทำให้ cut พัง — "easy to miss" [A06.L12 t=03:03]
- ถ้าไม่ระบุแสงจะ drift ไปทางพระอาทิตย์ตก; ตัวเอกเดินคนละทิศทุก generation; sky dancer เปลี่ยนขนาด/ตำแหน่ง [A06.L13 t=00:15] [A06.L13 t=00:23] [A06.L13 t=00:28]
- brute-force ~20 generation เผาเครดิตและ geometry ยังหลวม [A06.L13 t=00:46]
- กระเป๋าโผล่บาง batch ไม่โผล่บาง batch ถ้าไม่ล็อกใน prompt [A06.L13 t=03:10]
- "He dances" = เต้นมั่ว/flailing [A06.L14 t=00:40]
- ตัวเอก "just kind of there" แทนการเดินเข้าฉาก = entrance อ่อน [A06.L14 t=00:28]
- ไม่มี render แรกที่เป็น render สุดท้าย [A06.L16 t=01:30]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- prompt ตัวเต็มที่ Claude เขียนแสดงบนจอเท่านั้น: character sheet (85mm, "nothing cropped", 1.85m), สนาม (ARRI large-format, "not a glossy ad look", 8-9 AM), outfit (identity block + "No visible brand logos anywhere") [A06.L03 frames t=00:15] [A06.L07 frames t=00:25] [A06.L08 frames t=00:25]
- Global Style Prefix ฉบับเต็ม, ข้อความตั้งชื่อ asset, บล็อก asset reference และโครง CUT พร้อม lens mm ต่อ cut แสดงบนจอเท่านั้น [A06.L10 frames t=02:00] [A06.L10 frames t=01:45]
- prompt ของ street และ office สั้นมาก ("Pedestrian street, 3/4 view"; "Warm color palette office, 3/4 view") — article ไม่ให้ [A06.L07 frames t=01:10]
- host วัดผลของพื้นเทาเป็น "win rate" ที่สูงกว่า [A06.L03 t=00:38]
- ชื่อ Element "@s_hero" และ "@s_hero_wet" (article ไม่ระบุชื่อ) [A06.L12 t=01:05] [A06.L12 t=01:40]
- prompt sheet นักกีฬาของ Claude ขอ figure front/back แบบ headless — กฎหนึ่งหน้าถูกฝังลงใน prompt generation [A06.L12 frames t=02:00]
- prompt ของ Claude ระบุว่า sky dancer "replacing the potted plant that previously stood there" — ใช้แผนที่สลับวัตถุในฉากเป็น prop [A06.L13 frames t=04:35]
- demo "trap": โฟลเดอร์ Seedance เต็มไปด้วยผลประทับ "SLOP" และ dialog "Delete generations from folder?" [A06.L10 frames t=00:20]
- script PDF ที่แสดงบนจอ: "Headphone Ad Script — ~60 sec · 16:9 · diegetic sound, no music" พร้อม SFX note ต่อฉาก [A06.L10 frames t=01:05]
- Claude เสนอ "Continuity choices you may want to confirm": ชุดชมพู/ยีนส์ทั้งวัน, เปลี่ยนเป็น @sneakers เฉพาะสนาม, ใส่ Converse ดำในถนน/ออฟฟิศเพื่อเลี่ยง identity drift [A06.L11 frames t=01:00]
- บรรทัดแสงของ prefix หลังแก้ (บนจอ): "Natural light only — soft, even morning daylight ... no contre-jour, no rim backlight" [A06.L11 frames t=02:00]
- demo เปรียบเทียบหน้าที่ถูก GPT edit ทำนิ่ม vs หน้า Soul Cinema ที่คม และ demo mask ว่าส่วนไหนมาจาก layer ไหน [A06.L08 frames t=01:10] [A06.L08 frames t=01:40]
- กราฟิกโครงโฟลเดอร์ต่อ location พร้อมตัวเลขที่ดูเหมือนจำนวนไฟล์: STADIUM (734), OFFICE (215), STREET (566), KITCHEN (444), PACKSHOT (333) [A06.L02 frames t=00:20]
- การ frame ต้นทุน: body-rig shot ปกติต้องใช้ rig, operator, วันถ่ายทำ และหลายพันดอลลาร์ [A06.L12 t=04:36]
- beat ที่เห็นเฉพาะใน final cut: ตัวเอกสวมหูฟังให้หัวหน้าในออฟฟิศ ซึ่งเป็นเหตุของฉาก 5 [A06.L16 frames t=00:45]
- บทพูดของหัวหน้า "Where the hell have you been? ... third time this week" และ "I'm on my way." ทางโทรศัพท์ [A06.L01 t=00:36] [A06.L01 t=00:33]
- host batch หลาย generation ของ prompt สุดท้าย ("same name and batch several") — ถ้อยคำไม่ชัด [A06.L13 t=04:41]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- เครดิตรวม: ตัวนับบนจอเป็น animation อ่านได้ "6 081" ที่ 01:02 และ "6 725" ที่ 01:04 — ใช้ ≥6,725 ไม่ใช่ 6,712 (ค่าที่อ่านกลาง animation) และไม่เห็นค่าสุดท้าย [A06.L16 frames t=01:04]
- บนจอบอก GENERATIONS 56 แต่คำพูดบอก "best few seconds out of 100 tries" — ไม่ชัดว่า "tries" นับ output รายชิ้นหรือ job [A06.L16 t=01:30]
- cue boss-prompt ลิงก์ recreate ไป nano-banana-pro แต่วิดีโอแสดงโหมด AI Cast — ไม่รู้ว่าโมเดลไหนสร้างหัวหน้าจริง [A06.L04 cue boss-prompt]
- cue location ลิงก์ recreate ใช้ soul_cinematic แต่ UI แสดง "Cinematic Locations" — โมเดลเดียวกันหรือ preset ไม่ชัด [A06.L05 cue kitchen-location-prompt]
- prompt ฉาก 5 บอกว่าตำแหน่ง @skydancer และ @boss "marked on this map" แต่ article บอกว่าใช้แผนที่เดิมไม่แก้ และวิดีโอไม่เห็นการทำแผนที่ใหม่ [A06.L15 frames t=00:40] [A06.L15 article]
- article เขียน "a finger stab" แต่คำพูดและ prompt ที่พิมพ์บอก "a finger snap" [A06.L14 t=01:07]
- Global Style Prefix บอก "No music" แต่ฉาก 3 ใส่ music track เป็น audio input และ prompt ฉาก 5 ยังมีบรรทัด "No music" — ไม่ชัดว่าฉากอื่นใน shotlist สุดท้ายเก็บบรรทัดนี้ไว้หรือไม่ [A06.L13 frames t=04:35] [A06.L15 frames t=00:40]
- note บอกว่าหัวหน้าที่เลือก "glasses-less" แต่ auditor เห็น candidate ที่โกรธหลายคนใส่แว่น และ @boss ใน L10 คือ "thin rimless glasses" — เป็นจุดไม่แน่นอนเล็กน้อย [A06.L04 frames t=00:35] [A06.L10 frames t=02:00]
- ความยาวโฆษณาไม่ตรงกัน: ราว 50 s (L01), ราว 55 s (L16), script เขียน ~60 sec [A06.L01 frames t=00:00] [A06.L10 frames t=01:05]
- ชื่อผู้สอน: transcript เรียกผู้สอนว่า "Adil" (auditor ยืนยันจากหน้า Claude "Evening, Adil") แต่ผู้เขียน article คือ David Matamoros [A06.L01 t=01:35] [A06.L03 frames t=00:08]
- เวอร์ชัน Claude ใน picker อ่านได้ "Opus 4.8" ในหลายบท แต่ใน L10/L14 ระบุไม่ได้ และไม่รู้ว่า skill ขึ้นกับเวอร์ชันหรือไม่ [A06.L10 t=00:23] [A06.L14 frames sheet_01 tile 12]
- เนื้อหาไฟล์ skill ไม่ได้ถูกเปิดในการศึกษา (มีแค่ลิงก์ดาวน์โหลด) [A06.L10 cue download-shotlist-skill]
- ค่า count/batch และต้นทุน GENERATE บางจุดอ่านไม่ชัดที่ความละเอียด contact sheet (เช่น Cinematic Locations count ~10, ฉาก 5 ราว ~330) [A06.L07 frames t=01:10] [A06.L15 frames t=00:40]

### เทียบกับ v1
- เหมือนเดิม: ลำดับ assets -> shotlist -> scenes และการล็อกก่อนสร้าง [A06.L01 article]
- เพิ่ม: เครื่องมือแต่ละขั้น (Soul Cinema, GPT Image 2.0, AI Cast, Cinematic Locations, Seedance 2.0, Claude skill) พร้อม settings บนจอ [A06.L01 t=01:22] [A06.L11 frames t=00:40]
- เพิ่ม: template prompt จาก cue ครบทุกตัว (product sheet, character sheet meta-prompt, location, motion test, edit, erase-face, outfit, style-prefix fix, schematic, rewrite) [A06.L02 cue product-sheet-prompt] [A06.L13 cue street-schematic-prompt]
- v1 ผิด: v1 บอก prop "ควรทดสอบตามความยาก" แต่คอร์สสอนชัดว่า props ไม่ต้อง motion test และไม่ต้องทดสอบหลาย candidate [A06.L09 t=00:08]
- แก้: v1 บอกให้ระวังมุมใหม่ของสินค้าว่าเป็นการเดา — คอร์สไม่ได้สอนข้อนี้ คอร์สสอนว่า sheet หลายมุมช่วยให้ Seedance "หยุดเดา" [A06.L02 t=00:51]
- เหมือนเดิม: ลบหน้าซ้ำจากภาพเต็มตัว; v2 เพิ่มว่ากฎนี้ถูกฝังลง prompt sheet ใหม่แบบ headless [A06.L06 cue erase-face-prompt] [A06.L12 frames t=02:00]
- เพิ่ม: เทคนิค composite layer + mask เพื่อเก็บหน้า Soul Cinema หลัง GPT edit (v1 พูดแค่ "คืนรายละเอียดส่วนบน") [A06.L08 t=01:29]
- เพิ่ม: กฎ "images are cheap, videos aren't" สำหรับสภาพแห้ง/เปียก และการผูก reference กับ cut [A06.L12 t=01:09] [A06.L12 t=01:56]
- เหมือนเดิม: แผนที่ล็อก hydrant + sky dancer สูง 2 เท่าคน + ใต้ต้นไม้ + กระเป๋า; v2 เพิ่ม audio input และการตั้งชื่อสไตล์เต้นต่อ cut [A06.L13 cue street-schematic-prompt] [A06.L13 t=03:38]
- เพิ่ม: ยอดรวม GENERATIONS 56 / CREDITS ≥6,725 (ตัวเลข ณ วันบันทึก) [A06.L16 frames t=01:04]
- เพิ่ม: Global Style Prefix ฉบับเต็มและโครง CUT ที่มีเลนส์ mm [A06.L10 frames t=02:00]

## A07 Build an AI Ad Agency with Claude + Higgsfield

### ภาพรวมและผลลัพธ์
- วิดีโอเล่าเป็น "24-hour challenge" สร้าง AI ad agency: Claude ทำ research ทั้งหมด, Higgsfield ทำทุกอย่างที่เหลือตั้งแต่โฆษณาถึงเว็บไซต์ [A07.L01 t=00:27]
- presenter (Adil) ปรึกษาผู้เชี่ยวชาญ 5 คน: Liam Ottley (offer), Brock (outreach), Nate Herk (back office/QC), Samin Yasar (website), Jack Roberts (launch) [A07.L02 t=00:21] [A07.L06 t=00:00] [A07.L07 t=00:05] [A07.L10 t=00:09] [A07.L11 t=00:07]
- article ทำหน้าที่เป็นชั้นแก้ไข: เพิ่มการ verify, compliance และ human approval ทับคำกล่าวอ้าง "I touch nothing" ของวิดีโอ [A07.L07 article] [A07.L09 article]
- niche ที่เลือกคือ roofing contractors; ข้อเสนอ "5 custom video ads in 24 hours, $500 instead of $5,000, pay after delivery" [A07.L01 t=01:26] [A07.L02 t=02:35]
- ผลลัพธ์ในวิดีโอ: portfolio 10 ตัว, cold email template, Claude Project + Gmail, subscription prompt, QC prompt และเว็บไซต์ที่ deploy แล้วพร้อม Lead Inbox [A07.L05 frames t=00:49] [A07.L10 frames sheet_03 tile 12]
- คอร์สจบก่อนการ validate: ไม่มีการส่ง email, ยอด reply หรือลูกค้าจ่ายเงินจริงให้เห็น — "the only thing this business doesn't have is clients" [A07.L10 t=03:00] [A07.L11 t=01:33]

### Workflow ทีละขั้น
1. เลือก niche ใน Claude ด้วย prompt B2B positioning: อุตสาหกรรมที่จ่ายโฆษณาแบบเดิมเยอะแต่ digital creative อ่อน [A07.L01 cue research-hidden-niches]
2. verify shortlist: ตัวเลข growth, โฆษณาจริงปัจจุบันของบริษัทใน niche, asset ที่มีวันที่และปัญหาที่เห็นชัด แล้วเขียน niche thesis ประโยคเดียว [A07.L01 article]
3. ทำ offer ด้วยสูตร 5 ข้อ (sell the result, hit the biggest problem, kill the risk, speed + entry price + bonus, CTA) รวมกับคำขอ research ราคาใน prompt เดียวของ Claude [A07.L02 t=01:30] [A07.L02 t=02:18]
4. ตรวจ offer ทีละบรรทัดเทียบสูตร และเลี่ยง guarantee/scarcity ปลอม [A07.L02 t=02:35] [A07.L02 article]
5. เพิ่ม Higgsfield เป็น custom MCP connector ใน Claude: Customize -> Connectors -> Add custom connector -> ชื่อ "Higgsfield" -> วาง endpoint -> Add -> Connect -> OAuth consent -> Allow [A07.L03 t=00:18] [A07.L03 frames t=00:31] [A07.L03 frames t=00:33]
6. พิสูจน์ round trip ด้วย test generation ทิ้งได้หนึ่งชิ้นที่คืน media เล่นได้ และบันทึก ID/URL [A07.L03 article]
7. สร้าง portfolio ด้วย prompt เดียวใน Claude: 5 สไตล์ต่างกัน + hook 3 วินาที + CTA; ตอบคำถาม setup ของ Claude; Claude เรียก Higgsfield `generate_video` [A07.L04 cue generate-roofing-ad-set] [A07.L04 frames t=00:28]
8. generate เกินแล้วคัด: ขออีก 5 ตัว และเลือกหนึ่งตัวต่อหนึ่ง creative role [A07.L04 t=01:07] [A07.L04 article]
9. ออกแบบ intake ย้อนจากโฆษณาที่เสร็จแล้ว: prompt "Operations Manager" พร้อม field บังคับ (Company Name, Location/City, Target Audience, Visual Style, Email) [A07.L05 frames t=00:50]
10. ทุก fact ที่จะปรากฏในโฆษณาให้หยุดถาม และบันทึก source + approver แยกกันต่อ fact [A07.L05 article]
11. เขียน cold outreach ใหม่แบบ prospect-first: subject = company + city, proof, CTA "reply INTERESTED" รับ sample ฟรี [A07.L06 t=00:42] [A07.L06 t=00:52] [A07.L06 t=01:01]
12. ก่อนอนุมัติ: เปิด proof link เอง, เติม placeholder ครบ, บันทึก jurisdiction/CAN-SPAM fields [A07.L06 article]
13. Back office: ย้าย ops prompt เข้า Claude Project, เชื่อม Gmail, เพิ่มกฎ "interested" -> intake questions -> verify -> client profile -> free sample [A07.L07 t=01:33] [A07.L07 t=01:53] [A07.L07 t=02:13]
14. ทดสอบด้วย reply ปลอม: ต้องได้ draft intake + profile provisional ที่ tag ที่มา และไม่มีข้อความหรือ generation ออกไปโดยไม่ได้อนุมัติ [A07.L07 article]
15. เปลี่ยนการส่งมอบเป็น subscription: prompt ทุกวันจันทร์ไล่ทุก client profile, 3 variations ต่อราย, เตรียม delivery email [A07.L08 cue monday-creative-refresh]
16. เพิ่ม QC gate ก่อนส่ง: เทียบแต่ละโฆษณากับ profile ที่อนุมัติ [A07.L09 t=00:10] [A07.L09 article]
17. สร้างเว็บขายด้วย prompt เดียวใน Claude + Higgsfield: 5 blocks + CTA เดียวกันหลังทุก block + ฟอร์ม -> admin "Lead Inbox" แล้วส่งฟอร์มทดสอบ [A07.L10 t=02:09] [A07.L10 t=02:50]
18. ตรวจหน้าเว็บที่ได้เทียบ brief และรัน funnel test ก่อนแชร์ลิงก์ [A07.L10 article]
19. Launch กับรายชื่อ 10-15 บริษัทที่มีหลักฐานสาธารณะปัจจุบันว่าวิดีโอโฆษณาอ่อน แทนการ blast 5,000 บริษัท [A07.L11 t=00:25] [A07.L11 article]
20. ทำ validation model หนึ่งเดือน (conservative/base/optimistic) และกฎ go/revise/stop ที่เขียนไว้ก่อน [A07.L12 article]

### กฎที่ใช้ซ้ำได้
- แยก output ของโมเดลออกจากหลักฐาน: รายการ niche, ตัวเลข growth และราคาตลาดจาก Claude ยัง unverified จนกว่าจะมีแหล่ง [A07.L01 article] [A07.L02 article]
- เลือก niche ที่ "มีงบโฆษณาอยู่แล้ว + มีช่องว่าง creative ที่เห็นได้" ไม่ใช่ niche ยอดนิยม (clothing, coffee shops) [A07.L01 t=00:46] [A07.L01 t=01:00]
- "Bad creative" ไม่พอเป็น finding ต้องระบุ asset ที่มีวันที่และปัญหาที่เห็น [A07.L01 article]
- ขายผลลัพธ์ทางธุรกิจ ไม่ใช่ deliverable — ผู้ซื้อไม่สนวิดีโอ สนผลลัพธ์ [A07.L02 t=00:55]
- ใช้ภาษา "designed to bring" แทน "will bring" [A07.L02 article]
- ตั้งราคาหลังรู้ต้นทุน และมีเหตุผลจริงสำหรับส่วนลด introductory [A07.L02 article]
- connector พิสูจน์แล้วเมื่อได้ผลที่เล่นได้/URL/ID กลับมาเท่านั้น; test ด้วยเนื้อหาทิ้งได้ก่อน [A07.L03 article]
- copy URL connector จากหน้าทางการปัจจุบัน ไม่ใช่ screenshot เก่า และอ่าน scope ของ OAuth ก่อนกด Allow [A07.L03 article] [A07.L03 frames t=00:33]
- portfolio ต้องสร้างตาม creative role ไม่ใช่ variation; role ซ้ำให้เก็บตัวที่ชัดกว่าแล้ว regenerate role ที่ขาด [A07.L04 article]
- ห้ามนำเสนอผู้พูด synthetic หรือความเสียหายที่แต่งขึ้นเป็น testimonial จริง — ติดป้าย fiction หรือลบตัวเลขเฉพาะ (แนว FTC) [A07.L04 article]
- ห้ามให้โมเดลเติมช่องว่างข้อเท็จจริงที่ปรากฏในโฆษณา (เบอร์โทร ราคา โปรโมชัน โลโก้) — หยุดและถาม [A07.L05 article]
- เว็บไซต์สาธารณะยืนยันชื่อ/ที่ตั้งได้ แต่ไม่ได้ให้สิทธิ์เผยแพร่ offer แทนลูกค้า [A07.L05 article]
- outreach ต้อง prospect-first: subject = company + city, ข้อสังเกตจริงหนึ่งข้อ, proof link หนึ่งลิงก์ที่ตรงช่องว่าง, CTA ตอบง่ายที่ใช้คัดกรองด้วย [A07.L06 article] [A07.L06 t=01:10]
- free sample คือ filter: ผู้รับต้องส่งข้อมูลธุรกิจ ใครส่งคือ lead จริง — "The CTA is the filter" [A07.L06 t=01:10]
- reply ขอ sample คือหลักฐานความสนใจ ไม่ใช่ยอดขาย [A07.L06 article]
- automation เอาการ copy/route ออก ไม่ได้เอาความรับผิดชอบออก: draft, ผล QC และ delivery ไปหาผู้อนุมัติที่มีชื่อ [A07.L07 article] [A07.L09 article]
- เก็บ creative memory ของ hook/angle ที่ใช้แล้วสำหรับงาน recurring [A07.L08 t=00:27]
- QC เทียบกับ profile ที่ลูกค้าอนุมัติเท่านั้น ไม่ใช่ผสมข้อเท็จจริงกับการเดาจากที่สาธารณะ [A07.L09 article]
- เว็บขายคือ "a conversation, not an art project" [A07.L10 t=00:41]
- ราคาต่ำที่ไม่อธิบายเหตุผลทำให้ผู้ซื้อกลัว [A07.L10 t=01:05]
- "A live URL is the beginning of the test, not the result." [A07.L10 article]
- เริ่มด้วย batch เล็กที่วัดผลได้ กำหนดสูตรทุกขั้นของ funnel ก่อนส่ง และ scale เมื่อ demand ที่สังเกตได้และ capacity การส่งมอบรองรับเท่านั้น [A07.L11 article] [A07.L12 article]
- เมื่อ revise ให้เปลี่ยนตัวแปรเดียวต่อการทดสอบ [A07.L12 article]

### โครงสร้าง Prompt
- หา niche: `Act as a <expert role>. Which <business category> spend big money on <legacy channel> but have the lowest <target-channel quality>?` — ตัวที่ใช้: "act as a B2B positioning expert. Which service niches spend big money on traditional ads but have the lowest digital ad quality?" [A07.L01 cue research-hidden-niches]
- เวอร์ชันอัปเกรดใน article เพิ่ม: `Rank the opportunities by <market growth, ability to pay, urgency, visible creative gap>. Cite the evidence behind each score.` [A07.L01 article]
- Offer (บนจอ, อ่านจาก crop อาจคลาดบางคำ): [research ราคาที่ agency เก็บ] + "using this formula (sell the end result, hit their biggest problem, remove all risk ..., add speed, an easy entry price, and a bonus ... strong call to action)" + [niche] + "Keep it short." [A07.L02 t=02:15]
- Offer (article): `Turn my service into a specific offer for [niche]. Sell the business result, name the biggest costly problem, lower the risk of the first step, add a believable delivery time and a first-step bonus, then end with one explicit call to action. Keep every promise measurable and do not invent proof, guarantees, or client results.` [A07.L02 article]
- Portfolio: `Make me video ads for a <niche> business — each in a completely different style: <style 1..5>. You already know our audience and our offer — use them. Every ad needs a strong hook in the first 3 seconds and a clear call to action at the end.` [A07.L04 cue generate-roofing-ad-set]
- article เพิ่ม: จำนวน "five", "clearly labeled fictional customer scenario" แทน testimonial และ guard `Do not fabricate a testimonial or imply that an actor or AI avatar is a real customer.` [A07.L04 article]
- prompt ที่ Claude เขียนให้ tool call (บนจอ): framing/realism style + lighting + "Casting anchor in every shot: <age, hair, wardrobe, location>" + action beats [A07.L04 frames t=00:35]
- Ops manager (บนจอ, กำลังพิมพ์): role "You are the Operations Manager of our AI Ad Agency" + Step 1 รับ raw brief -> Step 2 เช็ค 5 field + "If any details are missing, ask for them." -> Step 3 แปลงเป็น ad briefs -> Step 4 ส่ง Higgsfield generate [A07.L05 frames t=00:50]
- Cold email (บนจอ): "Rewrite my offer as a cold email to a roofer. Start with his business, not ours (company name, city, his ads). Add our 5 portfolio links as proof, keep the same deal, and end with one CTA — reply 'INTERESTED' to get a free banner ad for his business" [A07.L06 t=02:10]
- template ที่ Claude คืนมา: Subject "[Company Name] — your ads in [City]" + observation + รายการ 5 ลิงก์ + offer paragraph + "Reply INTERESTED — and I'll start with a free banner ad for your business." [A07.L06 frames t=02:20]
- Cold email (article): slot [company]/[city]/[jurisdiction] + กฎ subject + ข้อสังเกตจริง + proof หนึ่งลิงก์ + sample ฟรี + sender identity/ad disclosure/postal address/opt-out + "leave any field I have not verified blank for me to fill." [A07.L06 article]
- กฎ reply ใน Project (article): trigger = intent signal -> draft intake เพื่ออนุมัติ -> field สาธารณะเป็น provisional พร้อม source URL, observation date, unconfirmed -> ราคา/บริการ/โปรโมชัน/contact/claims/brand = client-supplied -> เตรียม sample เมื่อทุก field สำคัญยืนยันแล้ว [A07.L07 article]
- Weekly refresh: `It's <trigger day>. Go through every client profile and generate <N> fresh ad variations for each. Prepare a delivery email for every client.` [A07.L08 cue monday-creative-refresh]
- article เพิ่ม filter "active" และ `Avoid hooks and angles already used` [A07.L08 article]
- QC (บนจอ): "Run a QC check on every video before delivery: verify client details (Name, City, Services, Phone) and flag any legal or risky claims. If it passes, send it. If it fails, move it to 'Needs Review' with a reason." [A07.L09 t=00:15]
- QC (article): `Audit this final ad against the attached approved client profile. Return READY_FOR_HUMAN_REVIEW only if <field list> all match. For every failure, quote the exact frame or line, name the conflicting source field, and route it for correction. Never repair, approve, or send an ad silently. Every external delivery requires the named human approver.` [A07.L09 article]
- Website (บนจอ): expert-advice framing + "Build and launch a website ... using exactly this structure" + 5 blocks พร้อม copy ตรงตัว (Hero "answers in 5 seconds", Proof, process, Benefits, FAQ) + "After EVERY block — one button, same CTA as our email" [A07.L10 t=02:10]
- Website (article): `Build a responsive five-block sales page for [offer], aimed at [niche]. ...` + กฎ benefits ที่ verify แล้ว + CTA ซ้ำหลังทุก block + admin view ที่ protected + validate input [A07.L10 article]
- Launch (article): `Find 10 to 15 [niche] companies in [market] with a clear, current, publicly evidenced reason to test better video ads ... return the evidence URL, the observation date, the exact creative gap, and one truthful, evidence-specific opening line. Do not infer campaign performance without performance data. Exclude any company you cannot verify from a public source.` [A07.L11 article]
- Economics (article): `Build a one-month validation model for this service. Keep assumptions in a separate section from observed data. Track ... Run conservative, base, and optimistic cases. Present nothing as guaranteed.` [A07.L12 article]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Claude (web/desktop) model selector "Opus 5 · High" ในเกือบทุกบท; presenter เรียกว่า "almost on par with Fable 5" [A07.L01 t=01:12] [A07.L04 frames t=00:04]
- Higgsfield MCP: หน้า setup คือ `https://higgsfield.ai/mcp` แต่ endpoint ที่พิมพ์ในช่อง "Remote MCP server URL" คือ `https://mcp.higgsfield.ai/mcp` [A07.L03 article] [A07.L03 frames t=00:31]
- dialog "Add custom connector" (BETA): ช่องชื่อ, Remote MCP server URL, Advanced settings มี OAuth Client ID/Secret (optional) [A07.L03 frames t=00:31]
- OAuth consent ที่ `accounts.higgsfield.ai/oauth-consent` ขอ scope "Verify your identity" + "Your email address" [A07.L03 frames t=00:33]
- Claude เรียก tool Higgsfield `generate_video`; chip ต่อ call: "Seedance 2.0" · "9:16" · "15s" · "Audio" [A07.L04 frames t=00:36] [A07.L04 frames t=00:38]
- ข้อความ Claude: "Launching now: 5 jobs, Seedance 2.0, 9:16, 15s each." และ batch 2 "same specs (Seedance 2.0, 9:16, 15s)" [A07.L04 frames t=00:36] [A07.L05 frames t=00:49]
- banner ใน Claude UI: "Fable 5 uses your usage credits and draws down usage much faster than Opus 4.8." [A07.L04 frames t=00:38]
- Claude Projects: dialog "Create a project" มี Visibility (org "Higgsfield" / Private) [A07.L07 frames sheet_02 tile 10]
- Connectors ในบัญชี: เชื่อมแล้ว Google Drive, Higgsfield (CUSTOM), Ramp Data; ยังไม่เชื่อม Clay, Fireflies, Gmail, Google Calendar, HubSpot, Meta MCP (CUSTOM), Microsoft 365 [A07.L07 frames sheet_03 tile 1]
- เว็บที่ Higgsfield MCP สร้าง: Claude ถามว่าจะ "Publish to the Higgsfield community feed" หรือไม่ (เลือก "No — just deploy it live") และมี admin "LEAD INBOX" [A07.L10 frames sheet_03 tile 4] [A07.L10 frames sheet_03 tile 12]
- ไม่มี scheduler/cron ให้เห็น — การรันวันจันทร์คือ prompt ที่พิมพ์เอง [A07.L08 frames t=00:48]
- ราคาในวิดีโอ (ตัวอย่าง ไม่ใช่ราคาตลาดที่ validate): $500 one-off, ~$2,000/month subscription, ตารางตลาด HIGH QUALITY ADS $5000 / 1 VIDEO $1000 / WEBSITE $400 [A07.L08 article] [A07.L12 frames t=00:15]
- ตัวเลขตลาดที่ Claude ให้บนจอ: roofing "growing ~6% annually toward $46B+ by 2031" — ไม่มีแหล่ง [A07.L01 frames t=01:24]

### คำเตือนและ failure modes
- รายการ niche ของโมเดลไม่ใช่ research และตัวเลข ~6% บนจอไม่มีแหล่ง อย่าพูดซ้ำเป็นข้อเท็จจริง [A07.L01 article]
- ความนิยมในหมู่คนขาย/creator ไม่ใช่หลักฐานความต้องการของผู้ซื้อ [A07.L01 article]
- ห้ามสร้าง scarcity, testimonial, ผลลัพธ์ หรือ guarantee ปลอม [A07.L02 article]
- ไม่มี next action ชัด prospect จะไม่ทำอะไร — "the one everyone forgets" [A07.L02 t=01:49]
- connector ไม่ได้ทำให้ brief ถูกต้องหรือ output ผ่านอนุมัติ; MCP ภายนอกคือ trust boundary [A07.L03 article]
- "Not yet proven" = Claude เขียน prompt หรือบอกว่าเสร็จแต่ไม่คืน asset ที่ใช้ได้ [A07.L03 article]
- หน้า consent เตือน "Make sure that you trust Claude (claude.ai). You may be sharing sensitive data with this site or app." [A07.L03 frames t=00:33]
- Claude หา Higgsfield tools ไม่เจอในตอนแรก ("deferred in this chat, not missing") ก่อน generate [A07.L04 frames t=00:36]
- ผู้พูด synthetic ที่เล่าความเสียหาย $12,000 ไม่ใช่ testimonial; dramatization ยังทำให้เข้าใจผิดได้ถ้าผู้ชมคิดว่าเป็นประสบการณ์จริง (FTC) [A07.L04 article]
- โฆษณาที่ generate มีเบอร์โทร placeholder "XX-XX-XX-XX" เพราะไม่มีการให้เบอร์จริง [A07.L04 frames sheet_01 tile 11]
- รันโฆษณาเดิมนานเกินทำให้ attention/performance ตกและเสียเงิน [A07.L04 t=01:40]
- สั่ง "figure it out on its own" เมื่อข้อมูลขาดไม่ปลอดภัยสำหรับเบอร์ ราคา โปรโมชัน เงื่อนไข โลโก้ — คำตอบที่ดูสมเหตุสมผลก็ยังเป็นการแต่ง [A07.L05 article]
- Claude เตือนเองบนจอ: "a generic-but-false observation kills the email faster than no observation at all" [A07.L06 frames sheet_03 tile 7]
- กฎ email เชิงพาณิชย์ขึ้นกับ jurisdiction; US: CAN-SPAM (header/subject ถูกต้อง, ระบุว่าเป็นโฆษณา, ที่อยู่ไปรษณีย์, opt-out ที่ใช้ได้) [A07.L06 article]
- ถ้า field บังคับขาดห้ามส่ง; batch แรกต้องมีคนอนุมัติทุกข้อความ [A07.L06 article]
- demo ไม่ใช่ธุรกิจ: ที่ scale คนจะกลายเป็นคอขวดใน inbox; 50 clients x 5 videos = 250 videos/month [A07.L07 t=00:41] [A07.L07 t=01:12]
- ข้อมูลไม่ verify (เบอร์, การสะกดชื่อ) และคำสัญญาของ AI ที่อาจทำให้ลูกค้าถูกฟ้อง [A07.L07 t=01:02]
- schedule การ generate และ draft email ไม่ได้แปลว่าอนุมัติงาน [A07.L08 article]
- checker ที่แก้เงียบหรือส่งเองถือว่าสอบตก [A07.L09 article]
- หน้าเว็บที่ generate ผิด brief เอง: CTA กลายเป็น "GET A FREE ROOF CHECK" และ media synthetic ถูกติดป้าย "CUSTOMER TESTIMONIAL" [A07.L10 article]
- การส่งฟอร์มทดสอบหนึ่งครั้งพิสูจน์แค่ว่ามาถึงหนึ่งครั้ง ไม่ได้พิสูจน์ว่า admin route ถูกป้องกัน [A07.L10 article]
- Claude อาจคืน asset เก่าหรือเขียน claim แรงกว่าหลักฐาน; อย่าอนุมาน performance ของแคมเปญจากหน้าตา [A07.L11 article]
- "Are these numbers guaranteed? Of course not." — คณิตถูกแต่สมมติฐานยังไม่พิสูจน์ [A07.L12 t=00:56] [A07.L12 article]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- endpoint จริงของ connector `https://mcp.higgsfield.ai/mcp` ต่างจากหน้า setup `higgsfield.ai/mcp` [A07.L03 frames t=00:31]
- หน้า OAuth consent ตัวเต็ม (scope, Deny/Allow, redirect กลับ claude.ai) และ presenter บอก "our setup is done" โดยไม่มี test generation [A07.L03 frames t=00:33] [A07.L03 t=00:34]
- คำตอบ niche ของ Claude บนจอ: Roofing ("Average job is $10-30K ... ~6% annually toward $46B+ by 2031 ... 80%+ of demand is non-discretionary"), HVAC/plumbing, law firms ("$100-300+ per click"), med spas, home-services franchises, equipment dealers [A07.L01 frames t=01:24] [A07.L01 frames t=01:26]
- เหตุตัดสินใจเลือก roofing ที่ presenter พูดคือตัวเลข 6% YoY อย่างเดียว [A07.L01 t=01:26]
- offer ที่ Claude สร้างตัวเต็ม จบด้วย "Just reply "SPRINT" to this message" และ breakdown "Why it hits every part of the formula" [A07.L02 t=02:35] [A07.L02 frames t=02:20]
- จิตวิทยาของ Liam: "nobody's sitting at work dreaming of more hard work ... everybody's dreaming about the money" [A07.L02 t=01:17]
- Claude ถามคำถาม setup แบบมีตัวเลือก ("Do you have a logo or photos to use in the videos?" ข้อ 1 of 3) ก่อนเขียนสคริปต์ [A07.L04 frames t=00:28]
- batch summary ของ Claude: Funny "Dave" ที่ระบบแนะนำ night-vision preset แต่ Claude ปฏิเสธเพราะมีแค่ 3 วินาทีแรกเป็น night-vision [A07.L04 frames t=00:38]
- สคริปต์โฆษณาที่ได้ยิน: roof-cleaning, ceiling stain "paid 12 grand ... comment SPOT", real-estate "almost lost 18 grand ... 20 grand off ... comment SELL" [A07.L04 t=00:38] [A07.L04 t=00:54] [A07.L04 t=01:57]
- CTA แบบ comment-keyword ("comment SPOT", "comment SELL") ในโฆษณา [A07.L04 t=01:07] [A07.L04 t=02:12]
- note ของ Claude ใน batch 2: "10 ads total ... a full testing matrix ... run all 10 at low budget, find the 2-3 winning hooks, then come back for variations of just those winners" [A07.L05 frames t=00:49]
- ตัวเลข "20 spam messages a week" ของ roofer และ Brock เปลี่ยน CTA จาก "SPRINT" เป็น "reply INTERESTED" [A07.L06 t=00:32] [A07.L06 t=01:01]
- Nate: "using it at like 10%", "good demo ... a lot of holes" และการคำนวณ 250 videos/month [A07.L07 t=00:36] [A07.L07 t=01:12]
- diagram ขั้น verify: "INTERESTED" -> INTAKE QUESTIONS -> VERIFY -> COMPANY EXISTS ✓ / PHONE IS REAL ✓ -> CLIENT PROFILE SAVED [A07.L07 t=02:24]
- upgrade 4 "not about automation at all" — เป็นการเปลี่ยนโมเดลราคา; เหตุผล "your system is making these ads anyway" [A07.L08 t=00:00] [A07.L08 t=00:22]
- pipeline recap: LEADS IN -> VERIFIED -> FREE SAMPLE -> CLIENT -> FRESH ADS EVERY MONDAY -> QC CHECK & SHIP [A07.L09 t=00:39]
- Samin: ตัวอย่างเหตุผลราคาต่ำ "launch price just for our first 50 clients" [A07.L10 t=01:12]
- presenter อ้างว่า MCP หา domain ว่างเองและทุกองค์ประกอบ generate ด้วย Higgsfield (ไม่ได้ verify) [A07.L10 t=02:40]
- Jack คาดว่า batch 10-15 ที่เจาะจงจะตอบกลับ "half of them" (สมมติฐาน) [A07.L11 t=01:07]
- กราฟ "EVEN IN THE WORST CASE, 1 CLIENT A WEEK = $2,000 A MONTH" และกราฟิกรายได้ 5 clients $10,000 / 10 clients $20,000 ต่อเดือน [A07.L12 frames t=00:46] [A07.L12 t=00:34]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- L05: คำพูดบอกให้ Claude "figure it out on its own" เมื่อข้อมูลขาด แต่ prompt ที่พิมพ์บนจอเขียน "If any details are missing, ask for them" และเฟรมยังเห็นแค่ขณะพิมพ์ ไม่ชัดว่าส่งคำสั่งไหน [A07.L05 t=00:51] [A07.L05 frames t=00:51]
- L09: วิดีโอให้ "If it passes, send it" ขัดกับกฎ article ที่ checker ห้ามอนุมัติหรือส่งเอง [A07.L09 t=00:28] [A07.L09 article]
- L07: คำกล่าวอ้าง "I touch nothing" ขัดกับ approval gate ของ article [A07.L07 t=02:40] [A07.L07 article]
- L06: วิดีโอใส่ portfolio ทั้ง 5 ลิงก์ใน email แต่ article บอกให้ใช้ลิงก์เดียวที่ตรงช่องว่าง [A07.L06 t=01:40] [A07.L06 article]
- L06: Brock เสนอ "one free video" แต่ presenter เปลี่ยนเป็น "free banner ad" [A07.L06 t=01:01] [A07.L06 t=01:49]
- L10: prompt บอก CTA "free banner ad" แต่เว็บที่ deploy แสดง "GET A FREE ROOF CHECK" และ presenter ไม่ได้พูดถึง [A07.L10 frames sheet_03 tiles 8-11]
- L08: กฎติดตาม hook/angle มาจากคำพูดของ Nate แต่ไม่อยู่ใน prompt ที่ presenter พิมพ์ [A07.L08 t=00:27] [A07.L08 cue monday-creative-refresh]
- L12: กราฟ worst case ติดป้าย 1 client = $500/month แต่หัวกราฟและคำพูดคำนวณ $2,000/month จาก client $500 สี่รายต่อเดือน [A07.L12 t=00:46]
- L04: โฆษณาตัวที่ 3 พูด "18 grand" แล้ว "20 grand" แต่ presenter เรียกว่า "ready to sell" [A07.L04 t=01:57]
- L03: presenter พูดว่า "Settings" แต่จอแสดงหน้าต่าง "Customize" [A07.L03 t=00:18]
- L03 evidence history: note เดิมอ้างว่าไม่มีหน้า OAuth และรวม setup page กับ endpoint เป็นอันเดียว — ถูก audit FAIL สองรอบและแก้แล้ว [A07.L03 frames t=00:33] [A07.L03 frames t=00:31]
- ป้ายโมเดล Claude ไม่ตรงกัน: "Opus 5 · High" ในแอป แต่ browser view ใน L07 อ่านได้ "Opus 4.6 · High" ที่ความละเอียดต่ำ และ banner L04 พูดถึง "Opus 4.8" [A07.L07 frames sheet_02 tile 12] [A07.L04 frames t=00:38]
- L12: คำพูด "$400,000" คือถอดเสียงผิด บนจอเป็น WEBSITE $400 [A07.L12 t=00:15]
- ไม่แสดงว่า QC ตรวจเนื้อหาวิดีโอ (เฟรม/เสียง) อย่างไร [A07.L09 article]
- "exact prompts" ของ Nate สำหรับ upgrade 1-5 อ่านไม่ได้บนจอ ยกเว้น QC prompt บางส่วน [A07.L07 article] [A07.L09 t=00:15]
- ไม่แสดงการ host/deploy เว็บและจดโดเมนผ่าน Higgsfield MCP (ต้นทุน, ความเป็นเจ้าของ, auth ของ admin route) [A07.L10 t=02:20]
- custom Claude skill "built on Liam's formula" ไม่ถูกแสดง [A07.L04 t=00:26]
- คำว่า "supercomputer" ใน L04 ไม่ชัดและไม่ปรากฏบนจอ [A07.L04 t=01:26]
- วิดีโอ L11 ตัดกลางประโยค ("in under 24 hours,") ไม่มีการค้นรายชื่อหรือผลลัพธ์ [A07.L11 t=01:33]
- ไม่มีผล outreach ใด ๆ (15 emails, ยอด reply, ลูกค้าจ่ายเงิน) — คอร์สจบก่อน validate [A07.L12 t=00:58]

### เทียบกับ v1
- เหมือนเดิม: ตัวเลขตลาดที่ผู้สอนพูดไม่แทน research ของ niche จริง; v2 ระบุตัวเลขบนจอ (~6%, $46B+ by 2031) และว่าไม่มีแหล่ง [A07.L01 frames t=01:24] [A07.L01 article]
- เพิ่ม: สูตร offer 5 ข้อของ Liam Ottley และ offer ตัวเต็มที่ Claude เขียน [A07.L02 t=01:30] [A07.L02 t=02:35]
- แก้: v1 พูดถึง "ขอบเขต revision" ในบท offer แต่สูตรในคอร์สคือ result / problem / risk / speed+price+bonus / CTA [A07.L02 t=01:30]
- เพิ่ม: เส้นทาง UI ของ connector, endpoint `https://mcp.higgsfield.ai/mcp` และ OAuth scope [A07.L03 frames t=00:31] [A07.L03 frames t=00:33]
- เพิ่ม: settings ต่อ call ที่เห็น (Seedance 2.0, 9:16, 15s, Audio) [A07.L04 frames t=00:36]
- เหมือนเดิม: testimonial สมมติต้องติดป้าย และไม่ใส่ตัวเลขที่ไม่มีหลักฐาน [A07.L04 article]
- เหมือนเดิม: intake ย้อนจาก deliverable พร้อม source/approver ต่อ fact; v2 เพิ่มความขัดแย้ง "figure it out" vs "ask for them" [A07.L05 article] [A07.L05 frames t=00:51]
- เพิ่ม: 3 fixes ของ Brock และกลไก "The CTA is the filter" พร้อม CAN-SPAM fields [A07.L06 t=01:10] [A07.L06 article]
- เพิ่ม: upgrade 1-3 ของ Nate (Project, Gmail, กฎ interested) และการทดสอบด้วย reply ปลอม [A07.L07 t=01:33] [A07.L07 article]
- เพิ่ม: ห้าองค์ประกอบของ recurring promise (cadence, volume, creative memory, approval, learning signal) [A07.L08 article]
- เพิ่ม: token READY_FOR_HUMAN_REVIEW และการทดสอบ QC ด้วย profile ที่ตรงและที่ขัดแย้ง (Northstar Roofing) [A07.L09 article]
- เพิ่ม: การ drift ของ CTA บนเว็บที่ deploy และ funnel checklist ก่อนแชร์ [A07.L10 article]
- เหมือนเดิม: launch batch เล็กพร้อม denominator ที่กำหนดก่อน; v2 เพิ่มสูตรอัตราทั้ง 4 [A07.L11 article]
- เหมือนเดิม: กรณีต่ำ/กลาง/สูงและ go/revise/stop เปลี่ยนตัวแปรครั้งละหนึ่ง [A07.L12 article]

## A08 Seedance 4K: Cinematic Realism

### ภาพรวมและผลลัพธ์
- คอร์สเป็น showcase/test ของ Seedance 2.0 native 4K ข้ามหลาย genre โดย Adil (Adilet Abish, @ADILINTHEWILD) ไม่ใช่ tutorial UI ทีละขั้น [A08.L01 t=00:31] [A08.L01 article]
- ข้อค้นพบหลัก: native 4K ลด "slop" (morph หรือท่านิ่งค้าง) ที่ wide shot ซับซ้อนเคยมีที่ 720p/1080p [A08.L01 t=01:56] [A08.L01 article]
- ทดสอบ 8 บท: realism (มังกร/leviathan), crowd, VFX บน footage จริง, 2D/stylized, 3D CGI + 10-bit, โฆษณา/ข้อความ, game trailer + HUD, high-speed combat [A08.L01 article] [A08.L08 article]
- โหมดที่ใช้: text-to-video (epic/crowd), video-to-video (VFX บนคลิปมือถือ/laptop), image-to-video (game trailer, โฆษณาแบรนด์, HUD) [A08.L02 t=00:30] [A08.L03 t=00:16] [A08.L07 t=00:10]
- ตัดสินสุดท้าย: native 4K "worth it" และใช้ได้กับทุกสไตล์ (hyper-real, sci-fi, dark-fantasy RPG, anime) [A08.L08 article]
- presenter อ้างว่าใช้เงินทดสอบเกือบ $10,000 [A08.L01 t=00:35]

### Workflow ทีละขั้น
1. เล่าไอเดียช็อตให้ Claude ที่มี prompt-building skill แล้วให้มันเขียน Seedance prompt ที่ใช้ได้เลย ไม่ต้องเขียนเอง [A08.L01 t=00:36] [A08.L01 article]
2. เลือกโหมด: text-to-video สำหรับ epic/crowd [A08.L02 t=00:30]
3. video-to-video สำหรับ VFX: ถ่าย footage ธรรมดา ใส่เป็น video input แล้วเขียน prompt effect [A08.L03 t=00:16]
4. image-to-video จาก reference frame สำหรับ game trailer, โฆษณาแบรนด์ และช็อตที่มี HUD [A08.L06 cue cue-l6-skincare] [A08.L07 cue cue-l7-trailer]
5. ถ้าต้องใช้ reference ให้ generate ก่อน: Soul Cinema สำหรับตัวละคร/สถานที่/keyframe, GPT Image 2 สำหรับข้อความ/motion/storyboard [A08.L06 t=01:23]
6. เขียน prompt เป็น section มี label: style/look -> lighting/colour -> camera -> physics/material -> subjects ด้วย @handle หรือ @image_N -> location -> shots ตามเวลา หรือย่อหน้า "Single continuous shot 15s" -> constraints/forbidden -> audio (SFX only, ไม่มีเพลง) -> positive locks [A08.L01 cue cue-l1-kaiju] [A08.L07 cue cue-l7-trailer]
7. Generate บน Seedance 2.0 ที่ 4K (ลิงก์ Recreate ของคอร์สตั้ง 1080p เกือบทั้งหมด มีแค่ cue-l4-clown ที่เป็น 4k) [A08.L01 cue cue-l1-dragon] [A08.L04 cue cue-l4-clown]
8. Review ที่ native 4K บนจอใหญ่ที่สุด: หยุด ซูม ตรวจ texture, ช่องว่างในฝูงชน, ข้อความ/โลโก้, HUD pinning, น้ำหนัก และ depth [A08.L01 t=00:53] [A08.L02 t=00:00]
9. สำหรับ VFX ให้เทียบ generated กับ original เคียงกัน หารายละเอียดเล็กที่ถูกเปลี่ยน [A08.L03 t=01:18]
10. Export โดยตั้ง bitrate = High เพื่อเก็บสี 10-bit (ไม่มี banding) [A08.L05 t=00:57]

### กฎที่ใช้ซ้ำได้
- ใช้ native 4K กับ wide shot ที่วุ่น, ฝูงชน, กล้องเร็วที่มี depth มาก และข้อความบนจอ — เคสที่ 720p/1080p จะ morph, ค้าง, ละลายเป็น "pixel soup" หรือทำโลโก้เละ [A08.L01 t=01:56] [A08.L02 t=00:00] [A08.L06 t=00:30] [A08.L08 t=00:00]
- เลือก subject ที่จำลองยาก (น้ำกระเซ็น, ตา close-up, หมึกรัดวาฬ) เพื่อ stress โมเดล; ตัดสินเป็น layer (ผิว น้ำ พื้นหลัง) [A08.L01 t=03:08] [A08.L01 t=02:55]
- ตรวจความสมบูรณ์ของฝูงชนที่ "ช่องว่างระหว่างคน" (น้ำแข็งแตกระหว่างทหาร หิมะร่วง ไม่ warp) [A08.L02 t=00:00]
- prompt เป็น section ที่มี LOCKS ชัด: อะไรต้อง SAME ทุก cut และอะไร FORBIDDEN (design drift, warping, plastic CGI, IP, eye glow) [A08.L01 cue cue-l1-kaiju] [A08.L04 cue cue-l4-girl] [A08.L08 cue cue-l8-racing]
- VFX บน footage จริง: เขียน INPUT LOCK ระบุวัตถุใน plate, ห้าม re-grade/re-time/re-frame/smooth, และบอกว่าสิ่งที่เพิ่ม "ONLY" คือ effect + แสง เงา ปฏิกิริยาทางกายภาพ [A08.L03 cue cue-l3-screen]
- "INHERIT the source handheld orbit exactly" + parallax-lock กับระนาบจริง + occlusion ถูกต้อง = ดู "production-ready instead of pasted on" [A08.L03 cue cue-l3-screen] [A08.L03 article]
- คลิปต้นทางเดียว หลาย effect: เก็บคลิปและ template เดิม เปลี่ยนแค่ย่อหน้า effect; เริ่ม effect จาก feature ที่มีอยู่ (รอยสัก) แล้วโตทีละชิ้น; ปิดด้วย "the rest of him and the office unchanged. Face and identity unchanged." [A08.L03 t=00:26] [A08.L03 cue cue-l3-cyber]
- จอเป็น "physical membrane portal, NOT a flat decal" เพื่อให้สิ่งมีชีวิตมีปฏิสัมพันธ์ทางกายภาพ [A08.L03 cue cue-l3-screen]
- ให้โมเดลวาง staging เอง: "you don't even have to manually prompt every scene or camera movements" [A08.L04 t=01:38]
- 4K = AI slop น้อยลง, re-roll ที่เผาเครดิตน้อยลง, ตัดต่อน้อยลง [A08.L04 t=01:53]
- stress-test CGI ด้วยกล้องเร็ว + อนุภาคเยอะ และตรวจ banding ที่ควัน สีแดง และหมอก [A08.L05 t=00:20] [A08.L05 t=00:30]
- โฆษณาแบรนด์: รวมสินค้าทั้งหมดใน lineup reference ภาพเดียว ระบุ string โลโก้ตรงตัว ("Logos read exactly ...") และล็อกสีสินค้า ("Serum stays green, cream stays white") [A08.L06 cue cue-l6-skincare]
- ตัดสิน realism จาก texture ผิว (รูขุมขน grain ความไม่สมบูรณ์) — "perfect AI skin" ทำให้ตก uncanny valley [A08.L06 t=01:06]
- เลือก image model ตามงาน: Soul Cinema (ตัวละคร/สถานที่/keyframe, cinematic เป็น default), GPT Image 2 (ข้อความ/motion/storyboard) [A08.L06 t=01:23]
- Game/HUD: ใช้ reference frame เป็น "master visual + UI reference", ระบุ HUD ตามตำแหน่งจอพร้อม hex, "flat on screen, never in the 3D world", "numbers may tick, layout locked" และผูกการเปลี่ยน HUD กับ beat [A08.L07 cue cue-l7-trailer] [A08.L08 cue cue-l8-racing] [A08.L08 cue cue-l8-cathedral]
- default ไม่ใช้ slow motion; อนุญาต speed-ramp เฉพาะ beat ที่ตั้งชื่อ (jump-scare, impact, roar) [A08.L07 cue cue-l7-trailer] [A08.L08 cue cue-l8-racing]
- beat ที่ใช้ซ้ำได้: hook -> extreme slow-mo macro พร้อมอนุภาคค้าง -> snap กลับความเร็วปกติ [A08.L01 cue cue-l1-dragon] [A08.L04 cue cue-l4-fungal]
- ระบุ scale และ staging ของสิ่งมีชีวิตแล้วพูดซ้ำ ("~2.5 human-heights — a towering boss, NOT kaiju-giant"; "stay at the water surface ... never fly") [A08.L07 cue cue-l7-trailer] [A08.L01 cue cue-l1-kaiju]
- audio = SFX only พร้อมรายการ foley ไม่มีเพลง และระบุว่าเสียงเปลี่ยนอย่างไรช่วง slow motion [A08.L04 cue cue-l4-fungal] [A08.L03 cue cue-l3-screen]
- ช็อตเร็วที่มี depth ให้ตัดสินที่การจัดการ depth/พื้นที่ 3D ไม่ใช่แค่ motion 2D [A08.L08 t=00:12]
- reference แบบ style (ไม่ใช่ keyframe): "image1 is style reference not a keyframe ... animated and moving forward" [A08.L08 cue cue-l8-racing]

### โครงสร้าง Prompt
- Dragon oner (cue-l1-dragon): (1) tag line คุณภาพ/สไตล์ ("single continuous shot, one take no cuts, cinematic oner ... 35mm film quality ... steadicam fluidity") (2) ย่อหน้า subject + creature design + palette + hook + กฎ take (3) "Single continuous shot 15s:" beat ต่อเนื่อง (chase -> arc -> hook -> extreme slow motion + frozen particles -> snap back -> pull back wide) (4) footer "Total: <dur> / <n> shot / <aspect>" [A08.L01 cue cue-l1-dragon]
- Kaiju 6 cuts (cue-l1-kaiju): STYLE / LIGHTING / COLOR / CAMERA ("Never static") / MATERIAL / ACTING / PHYSICS (staging constraint) / CHARACTER DESIGN ("original, not based on any franchise") / CONTINUITY (SAME x ทุก cut) / TECHNICAL (24fps, slow motion beat เดียว) / AUDIO / SCENE CONTEXT / FORMAT MODE "Sequence of 6 cuts, no timecodes" / OPTICS (CUT n — shot size + lens°) / ACTION / POSITIVE LOCKS [A08.L01 cue cue-l1-kaiju]
- Epic crowd T2V (cue-l2-titan) ย่อหน้าเดียว: "<Shot size> shot of <giant> <action> as <crowd> <action> across <location>" -> "<camera> shakes hard with each <event>, snapping from <A> to <B> to <C>" -> FX สิ่งแวดล้อม -> palette/mood -> "<aspect>, <duration>" [A08.L02 cue cue-l2-titan]
- VFX portal (cue-l3-screen): Style ("Composition & grade INHERITED from <<<video_1>>>") -> INPUT LOCK (match 100%, รายการวัตถุ, "Do NOT re-grade, re-time, smooth, or re-frame", "ONLY additions are ...") -> SUBJECT ("mid-birth, half-in/half-out") -> ACTION SHOT 1/2/3 ตาม timecode -> CAMERA -> AUDIO (NO MUSIC) -> CONSTRAINTS (match source duration ~12s, portal not decal, NO slow-motion) [A08.L03 cue cue-l3-screen]
- VFX แปลงแขน (cue-l3-cyber/reptile/erase): `@video_1: <คำบรรยายคลิปต้นทาง>. Subject, face, pose, office, camera and motion reference — preserve exactly.` -> "Photoreal. 16:9. 10s. Filmic look — ... NON-IP — original <design> ... assembling part by part. SFX only." -> ย่อหน้าแปลงร่างทีละขั้นเริ่มจากรอยสัก -> "the rest of him and the office unchanged. Face and identity unchanged." -> รายการ SFX [A08.L03 cue cue-l3-cyber] [A08.L03 cue cue-l3-reptile] [A08.L03 cue cue-l3-erase]
- Painterly flight (cue-l4-girl): `<GENRE> — <LOGLINE> (CINEMATIC, <dur>)` / style paragraph / THE WORLD / THE COLOR / THE GIRL / THE CREATURE ("Same design in every frame, no drift") / KEY LOCKS / SHOTS (0–4 / 4–9 / 9–15s) / FORBIDDEN / `<dur>. <aspect>. <fps>. SFX only: <list>. No dialogue.` [A08.L04 cue cue-l4-girl]
- FPV jump-scare (cue-l4-fungal): Cinematography / Lighting / Color 60:30:10 / Camera (24mm, 180° shutter, speed-ramp 24->240fps) / Physics / SUBJECTS (@rider_pov, @alien_fly) / LOCATION / ACTION "ONE CONTINUOUS TAKE, NO cuts" พร้อม timecode และ fps ต่อช่วง / CONSTRAINTS / AUDIO (เสียงผูกกับ timecode) [A08.L04 cue cue-l4-fungal]
- Multi-shot cartoon มีบทพูด (cue-l5-jungle): tag line เริ่ม "montage, multi-shot ... Don't use one camera angle or single cut" -> ย่อหน้าฉาก/ตัวละคร -> `Shot N: <shot size + camera move>, <action>. <He says>: "<line>"` x6 -> "Total: 15s / 6 shots / 16:9" [A08.L05 cue cue-l5-jungle] [A08.L04 frames t=01:30]
- FPV CGI oner (cue-l4-clown): template เดียวกับ dragon — tag line ("cinematic FPV oner, 4K ultra-detailed ... fluid drone flight") -> ย่อหน้าฉากพร้อม slow-motion beat ที่วินาที 3 และ 7 -> "Single continuous shot 15s:" [A08.L04 cue cue-l4-clown] [A08.L05 frames t=00:21]
- Product commercial สั้น (cue-l5-product): `hypermotion, CGI commercial video of our products, about <dur>, <n> scenes / cuts with 3D CGI showing the product. @<ElementName>` [A08.L05 cue cue-l5-product]
- Timed multishot ad (cue-l6-skincare): Style (transition stylized ได้ครั้งเดียว: FILM BURN จาก Section 7 ไป 8, ที่เหลือ hard match-cut) -> SCENE CONTEXT -> ACTIVE REFERENCES (@image_1..3 = ตัวละคร, @image_4 = product lineup + "Logos read exactly <STRINGS>") -> FORMAT MODE -> `[Section k — a–b s]` x8 -> FILM BURN (13.0s, 10–14 frames) -> AUDIO ("No voiceover, no music, no on-screen text") -> POSITIVE LOCKS [A08.L06 cue cue-l6-skincare]
- Game trailer I2V (cue-l7-trailer): Style ("Match @image_1 as the master visual + UI reference 100% ... NOT live-action") / Lighting / Camera / Continuity / HUD LAYER (hex #d1ef17, element ต่อตำแหน่ง TOP-CENTER, TOP-RIGHT, RIGHT EDGE, BOTTOM-LEFT, BOTTOM-CENTER, BOTTOM-RIGHT, CENTER-LOWER, "STAYS PINNED") / SUBJECT @drifter / LOCATION "@image_1 as STYLE REFERENCE" / late beat @horned-mutant / SHOT 1–3 / CONSTRAINTS / "AUDIO — NO MUSIC, SFX ONLY" [A08.L07 cue cue-l7-trailer]
- Racing I2V (cue-l8-racing): Style ("NOT a film plate") / Cinematography / Lighting / Physics / Technical 60fps / REFERENCE ("image1 is the MASTER STYLE REFERENCE ... Match 100% ... the world extends forward") / SUBJECT / LOCATION / HUD (ค่า live พร้อมช่วง เช่น speed 320–360, "Flat on screen, never in the 3D world") / SHOT 1–3 / CONSTRAINTS ("No real brand logos", "No eye glow") / AUDIO [A08.L08 cue cue-l8-racing]
- Boss-fight oner (cue-l8-cathedral): template dragon + "third-person video-game camera with persistent in-game HUD" + ย่อหน้าฉากที่สะกด string และตำแหน่ง HUD + beat ที่สถานะ HUD เปลี่ยน (prompt หาย, boss bar เต็ม, stamina ลด, boss bar หมด) [A08.L08 cue cue-l8-cathedral]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Seedance 2.0 native 4K บน Higgsfield (`/generate/video/seedance_2_0`) ใช้ทั้ง T2V, V2V และ I2V; panel บนจอเขียน "Seedance 2.0 4K" [A08.L01 t=00:33] [A08.L01 frames t=01:19]
- frame ของ cue แสดงแค่ป้าย "Seedance 2.0 4K" ไม่มี chip resolution/duration/aspect/credit ให้เห็น [A08.L01 frames t=01:26] [A08.L07 frames t=00:07]
- ลิงก์ Recreate ของ cue ตั้ง 16:9, 1080p ยกเว้น cue-l4-clown ที่ resolution=4k [A08.L01 cue cue-l1-dragon] [A08.L04 cue cue-l4-clown]
- output 10-bit (มากกว่าพันล้านสี) เทียบ 8-bit (~16 ล้านสี) ลด banding; caption "8-BIT: 16M" [A08.L05 t=00:37] [A08.L05 frames t=00:40]
- Export setting: bitrate = High (ไม่เห็น UI ใน sheet) [A08.L05 t=00:57]
- Soul Cinema generate bar: Soul Cinema / 16:9 / 2k / count 4/4 / "Off" (ไอคอนไม้กายสิทธิ์) / ช่อง CHARACTER / GENERATE 1; presenter พูดว่า "eight batches just for one credit" [A08.L06 frames t=01:42] [A08.L06 t=01:35]
- GPT Image 2 สำหรับข้อความ/motion/storyboard [A08.L06 t=01:45]
- Claude + "professional prompt-building skill" (ลิงก์อยู่ใน description) [A08.L01 t=01:37]
- syntax reference ที่เห็น: `<<<video_1>>>`, `@video_1`, `@image_1..4`, `image1`, subject แบบ @ (`@drifter`, `@alien_fly`, `@rider_pov`, `@horned-mutant`) และ @-element `@Supercomputer-Heroine` [A08.L03 cue cue-l3-screen] [A08.L05 cue cue-l5-product] [A08.L07 cue cue-l7-trailer]
- ค่าตาม cue: dragon 15 s / 1 shot / 16:9; kaiju 24fps / 6 cuts; titan 10 s; VFX portal ~12 s; แขน 10 s; girl/fungal/clown 15 s; skincare 15 s 8 sections; trailer 15 s 3 shots; racing 60fps; cathedral 30fps [A08.L01 cue cue-l1-dragon] [A08.L02 cue cue-l2-titan] [A08.L03 cue cue-l3-screen] [A08.L08 cue cue-l8-cathedral]

### คำเตือนและ failure modes
- ที่ 720p/1080p wide shot ที่มีหลายส่วนเคลื่อนไหวจะ morph หรือนิ่งค้าง [A08.L01 t=02:03]
- ที่ 1080p ฝูงชนพื้นหลัง "melt into a blurry pixel soup" เมื่อกล้องขยับ; การสร้างฝูงชนเป็น "one of the hardest tasks" [A08.L02 t=00:00] [A08.L02 article]
- VFX บน footage จริงที่ 1080p "almost always changed small details and made the shot unusable" [A08.L03 t=01:31]
- guard ใน prompt VFX: re-grade/re-time/re-frame plate, จอแบบ decal แบน, slow motion, ลุค CG/เกม, สิ่งมีชีวิตออกมาทั้งตัว ("NO full exit"), ลอยไม่มี contact shadow [A08.L03 cue cue-l3-screen]
- "NON-IP — original cybernetic limb design" เพื่อเลี่ยงความเหมือนแฟรนไชส์ [A08.L03 cue cue-l3-cyber]
- FORBIDDEN list: design drift, geometry warp/ละลาย, plastic CGI gloss, desaturated grade, neon eyes, ข้อความ/โลโก้ที่อ่านได้, IP [A08.L04 cue cue-l4-girl]
- การเคลื่อนเยอะ + อนุภาคเยอะ "usually destroys AI videos"; export 8-bit มี "ugly bands" ในควัน/สีแดง [A08.L05 t=00:24] [A08.L05 t=00:50]
- ไม่ export ที่ High bitrate = เสียข้อดีของ 10-bit [A08.L05 article]
- AI video เดิมทำโลโก้/ฉลากเละในการตัดเร็ว ทำให้ใช้กับแคมเปญจริงไม่ได้ [A08.L06 article]
- AI UI มักเละหรือ drift; AI video ทั่วไปดู "floaty" เพราะโมเดล "don't understand weight" [A08.L07 article] [A08.L07 t=00:17]
- combat ความเร็วสูงและ effect ซับซ้อนคือ "the real challenge for any video model" [A08.L07 t=00:35]
- 1080p ไม่พอสำหรับ game cinematic [A08.L08 t=00:00]
- guard ในเกม: NO slow motion (ยกเว้น beat ที่ระบุ), HUD ต้องเป็น screen-space, no real brand logos, no eye glow, contact shadow บนเศษซาก [A08.L08 cue cue-l8-racing] [A08.L07 cue cue-l7-trailer]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- cue สลับกันระหว่าง L04 กับ L05: วิดีโอ L04 เล่นการ์ตูนสัตว์ประหลาดในวิหารป่า (prompt บนจอเป็น cue-l5-jungle แบบยาว) ส่วนวิดีโอ L05 เล่น clown golem (prompt บนจอเป็น cue-l4-clown แบบยาว) [A08.L04 frames t=01:30] [A08.L05 frames t=00:21]
- prompt บนจอหลายตัวเป็นเวอร์ชัน "ยาวกว่า" cue: trailer มี "[STYLE PREFIX]", Render look, Color 60:30:10, Surfaces, Acting, Physics, Composition ที่ cue ไม่มี; racing เพิ่ม "DO NOT use it as a frozen keyframe ... Introduce no new characters, props or palette." [A08.L07 frames t=00:07] [A08.L08 frames t=00:07]
- prompt clown บนจอเพิ่มถ้อยคำ "no trace of golden hour", "to read every surface", "never stopping, never pulling up or back" [A08.L05 frames t=00:21]
- บทพูดใน clip การ์ตูนถูก prompt ไว้ ("Okay — today's the day, I can feel it in my fur!") และโมเดล generate เสียงพูด [A08.L04 frames t=01:30] [A08.L04 t=01:14]
- effect ตัวที่ 5 "one last option" ใน L03 ไม่มีใน article/cue: มือเปิดยกขึ้นกลายเป็นเปลือกไหม้มีรอยแตกเรืองส้ม (ลุค molten) — ไม่ใช่ลูกไฟตามที่อ่านจาก sheet ครั้งแรก [A08.L03 frames t=01:25]
- คลิป laptop ต้นทางเป็นแนวตั้ง และ presenter เปลี่ยนเป็นแนวนอนสำหรับคลิปมือ ("let's do horizontal this time") [A08.L03 t=00:31]
- วิธีเทียบ "ORIGINAL" vs "GENERATED" เคียงกันและ stack ลูกศร original->generated ของแต่ละเวอร์ชัน [A08.L03 t=01:18]
- คนที่นั่งหลังกระจกใน plate ถูกเบลอเป็นกล่อง (privacy blur) — ไม่ชัดว่าใครใส่ [A08.L03 frames t=00:37]
- โฆษณาเปิด "DERMA.NEURAL" (ไม่มีใน article และไม่มี cue) [A08.L06 frames t=00:05]
- input 4 ภาพของ BEGIM บนจอ: นักพายเรือบนน้ำสีเทอร์ควอยซ์, ผู้หญิงบนบันไดแสงแดง, ผู้หญิงกลับหัวกับลูกโป่งหัวใจ, product lineup [A08.L06 frames t=00:40]
- ภาพ reference และผลลัพธ์ของ game trailer แสดงเคียงกัน (article ฝังแค่ reference) [A08.L07 frames t=00:10]
- HUD racing ในผลลัพธ์: ความเร็ว 318/356/297 km/h, timer, "1st", gear, BOOST bar [A08.L08 frames t=00:05]
- montage ปิดท้าย (kraken บนเรือบรรทุกเครื่องบิน, นักรบถือหอกกับมังกรเรืองเขียว) เพื่อแสดง "any visual style" [A08.L08 frames t=00:50]
- presenter: "I wish we had 4K when we were making our film" และเรียกผลว่า "true AI realism ... low-key scary" [A08.L01 t=02:09] [A08.L01 t=02:38]
- caption ขีดฆ่า "AI SLOP" / "BURNING CREDITS" [A08.L04 t=01:53]
- presenter สัญญาว่าบทหลังจะเปรียบเทียบ image model ที่ดีที่สุดกับ Seedance 4K (article ไม่พูด) [A08.L02 t=00:35]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- L04↔L05 cue สลับกัน: ในช่วง cue-l4-clown (89–104 s) panel บนจอแสดง prompt วิหารป่า และใน L05 ช่วง 20–27 s แสดง prompt clown golem; article ช่อง 3 ของ L04 (clown golem) ก็ไม่ตรงกับวิดีโอ L04 [A08.L04 frames t=01:30] [A08.L05 frames t=00:21] [A08.L04 article]
- cue-l5-product ("hypermotion CGI commercial ... @Supercomputer-Heroine") ไม่ปรากฏในวิดีโอ L05; อาจเป็นโฆษณา DERMA.NEURAL ใน L06 — ยังไม่ verify [A08.L05 cue cue-l5-product] [A08.L06 frames t=00:05]
- L08: HUD ในคลิป cathedral อ่านว่า "THE DROWNED CARDINAL" / "THE SUNKEN COVENANT" แต่ cue และ panel prompt บนจอเขียน "The Hollow Cardinal" / "The Exsanguinated Throne" — ไม่ชัดว่ามาจาก prompt เวอร์ชันอื่นหรือโมเดลเขียน HUD ใหม่ [A08.L08 frames t=00:25] [A08.L08 frames t=00:40]
- L02 aspect: คำพูดและ article บอก "ultra-wide 21:9" แต่ cue, ลิงก์ recreate และ panel บนจอจบด้วย "16:9, 10 seconds" [A08.L02 t=00:00] [A08.L02 frames t=00:07]
- คอร์สชูเรื่อง 4K แต่ลิงก์ Recreate เกือบทั้งหมดเป็น 1080p และไม่มีการแสดงว่าเลือก 4K ใน UI อย่างไร [A08.L01 cue cue-l1-kaiju] [A08.L01 frames t=02:46]
- L03 cue-l3-screen เขียน "16:9" แต่คลิป laptop ต้นทางเป็นแนวตั้ง [A08.L03 frames t=00:05]
- L03 effect ตัวที่ 5 ไม่มี prompt และไม่รู้ว่าใช้ prompt แยกหรือไม่ [A08.L03 frames t=01:25]
- L05: ไม่เห็นตำแหน่งปุ่ม bitrate=High — transcript จบที่ "high right here" และวิดีโอจบที่ 61.9 s [A08.L05 t=01:00]
- L06: "eight batches for one credit" ไม่ตรงกับ stepper 4/4 บนจอ และไม่รู้ว่า toggle "Off" คืออะไร [A08.L06 frames t=01:42]
- ชื่อ Claude prompt-building skill ถูกตัดใน transcript และลิงก์ "in the description" ไม่มีในวัสดุที่ศึกษา [A08.L01 t=01:37]
- ไม่มีการระบุต้นทุน/เครดิตของ generation 4K นอกจากคำอ้าง ~$10,000 ทั้งหมด [A08.L01 t=00:35]
- L05 ในช่วง cue-l5-jungle (0–15 s) วิดีโอแสดง host และช็อตควัน/เมฆ ไม่ใช่การ์ตูนป่า [A08.L05 frames t=00:07]

### เทียบกับ v1
- เหมือนเดิม: รายละเอียดคมไม่เท่ากับ physics ถูก ให้อ่านเป็น layer; v2 เพิ่มรายการ subject ที่จำลองยาก [A08.L01 t=02:55] [A08.L01 t=03:08]
- เพิ่ม: template prompt จาก cue ทั้ง 16 ตัว รวม INPUT LOCK, HUD LAYER และ POSITIVE LOCKS [A08.L03 cue cue-l3-screen] [A08.L07 cue cue-l7-trailer]
- เหมือนเดิม: ฝูงชนตรวจรายบุคคลและพื้นที่รวม; v2 เพิ่มจุดตรวจ "ช่องว่างระหว่างคน" และว่าเป็น T2V ล้วน [A08.L02 t=00:00] [A08.L02 t=00:30]
- เหมือนเดิม: VFX ต้องรับ parallax/occlusion ของ footage จริง; v2 เพิ่ม template แขนแบบสลับ effect และ effect ตัวที่ 5 [A08.L03 article] [A08.L03 frames t=01:25]
- v1 ผิด: v1 บอกว่า L04 มี "clown" แต่วิดีโอ L04 เล่นการ์ตูนสัตว์ประหลาดวิหารป่า — clown golem อยู่ในวิดีโอ L05 (cue สลับ) [A08.L04 frames t=01:30] [A08.L05 frames t=00:21]
- แก้: v1 บอกว่า bit depth/bitrate "ไม่รับประกันโดยชื่อโมเดล" — คอร์สอ้างว่า Seedance output 10-bit และสอนให้ตั้ง bitrate High ตอน export (ยังควรตรวจไฟล์จริง) [A08.L05 t=00:37] [A08.L05 t=00:57]
- เพิ่ม: เครื่องมือ reference ที่แนะนำ (Soul Cinema vs GPT Image 2) พร้อม generate bar ที่เห็น [A08.L06 t=01:23] [A08.L06 frames t=01:42]
- เหมือนเดิม: HUD ต้องอยู่ในพิกัดจอ; v2 เพิ่มวลี "flat on screen, never in the 3D world" และ "numbers may tick, layout locked" [A08.L08 cue cue-l8-racing] [A08.L07 cue cue-l7-trailer]
- เพิ่ม: ความขัดแย้ง HUD cathedral และ 21:9 vs 16:9 [A08.L08 frames t=00:25] [A08.L02 frames t=00:07]

## A09 Build a Brand's Visuals with AI

### ภาพรวมและผลลัพธ์
- คอร์ส 9 บทนี้สร้างแบรนด์เสื้อผ้าสมมติ "HIGGS" ตั้งแต่ศูนย์ โดยผู้สอน (Adil, @ADILINTHEWILD) แบ่ง stack เป็น 4 เครื่องมือ: Nano Banana Pro = brand assets, Soul = ออกแบบสินค้า, Claude = เขียน prompt, Marketing Studio = ประกอบเป็นโฆษณา [A09.L01 t=00:55–01:11] [A09.L01 article]
- byline ของบทความให้เครดิต Rus Syzdykov เป็นผู้เขียนคอร์ส ส่วนคนที่อยู่หน้ากล้องคือ Adil [A09.L01 t=00:50]
- ลำดับใหญ่ของคอร์สคือ BRAND → PRODUCT → ADS ซึ่งขึ้นเป็นกราฟิกตอนเปิด L02 [A09.L02 t=00:00]
- หลักฐานที่ผู้สอนยกมาคือร้าน OffCulture ที่ภาพสินค้าทั้งหมดทำด้วย Higgsfield Soul [A09.L01 t=01:15]
- ผู้สอนบอกว่าใช้ตัวอย่างเป็นแบรนด์เสื้อผ้า แต่ขั้นตอนเดียวกันใช้ได้กับทุก niche [A09.L01 t=01:31–01:45] [A09.L01 article]
- palette ของแบรนด์คือ accent #d1fe17 + #000000 + #ffffff ตามหน้า Notion [A09.L02 t=01:10] [A09.L02 cue c2a]
- ผลลัพธ์สุดท้าย: โลโก้และโลโก้หลายแบบ, สินค้า 5 ชิ้น (jersey, jacket, sneakers, pants, sunglasses), วิดีโอโฆษณาหลาย preset, ภาพ IG/เว็บ, packaging และวิดีโอ unboxing [A09.L09 t=01:56–02:01] [A09.L03 article]

### Workflow ทีละขั้น
1. ให้ Claude เขียน prompt โลโก้จาก brief บรรทัดเดียว (ชื่อแบรนด์ + hex + "flat vector, minimal") [A09.L02 cue c2a] [A09.L02 t=00:05–00:15]
2. รัน prompt โลโก้ใน Soul Cinema ทีละ batch 4 รูป ซึ่งทั้ง batch ใช้ครึ่งเครดิต [A09.L02 t=00:26–00:34] [A09.L02 frames t=00:35]
3. แก้จุดบกพร่องของโลโก้ที่เลือกด้วย edit ใน Nano Banana Pro โดยให้ Claude เขียน edit prompt แบบ "Recreate this logo exactly ... change only X" และลากโลโก้เดิมเข้าไปเป็น reference [A09.L02 cue c2c] [A09.L02 cue c2d] [A09.L02 t=00:40–01:00]
4. บันทึกโลโก้และ palette ลงหน้า Notion "Brand Design" ที่ใช้เป็น checklist [A09.L02 t=01:02–01:12] [A09.L02 article]
5. ทำโลโก้หลายแบบ (monogram / icon / horizontal lockup บนพื้นขาวและดำ) ใน NBP จาก prompt "mini-guide" ที่ Claude เขียน [A09.L02 cue c2e] [A09.L02 cue c2f] [A09.L02 t=01:50]
6. ทำ checklist "Product List" ใน Notion: T-shirt, pants, jacket, shoes, sunglasses, packaging [A09.L03 t=00:09–00:20] [A09.L03 article]
7. ทำสินค้าแต่ละชิ้นตาม pipeline เดียว: Claude ขยายไอเดียบรรทัดเดียวเป็น mockup prompt → Soul Cinema 16:9 ได้ 4 แบบ → เลือก 1 แบบ → NBP สลับโลโก้ [A09.L03 t=01:48–01:56] [A09.L03 article]
8. ขั้นสลับโลโก้ใส่ reference 2 รูป (image 1 = สินค้า, image 2 = โลโก้) แล้วแก้ต่อด้วยคำสั่งสั้นๆ เช่น "make the icon smaller" [A09.L03 t=00:50–01:10] [A09.L03 article]
9. สินค้าที่ต้องเห็นหลายมุม (sneakers) ให้ทำใน NBP โดยตรงเป็น 4-view reference sheet แบบ 2x2 บนพื้นขาว [A09.L03 cue c3e] [A09.L03 cue c3f] [A09.L03 t=01:59–02:19]
10. ลงสินค้าบนเว็บไซต์ของแบรนด์ (ทำแบบ vibe-coded) แล้วให้ Marketing Studio สร้าง product โดยสแกนจาก URL หรือกด "Create manually" [A09.L04 t=00:41–00:55] [A09.L04 article]
11. สร้าง avatar เอง: Upload → วางรูป (หน้า/หลัง) → ตั้งชื่อ → Create avatar หรือเลือก preset avatar ก็ได้ [A09.L04 t=00:56–01:15] [A09.L04 article]
12. สร้างวิดีโอโฆษณาใน Marketing Studio โดยเริ่มแบบ zero-prompt (ใส่ product + avatar แล้วกด Generate) [A09.L04 t=01:16–01:52] [A09.L04 article]
13. ถ้าต้องการคุมมากขึ้น ให้ติดตั้ง Claude skill สำหรับ Marketing Studio แนบรูป avatar + สินค้า ขอ "a prompt for a viral video" แล้วเอาไปวางใน preset ที่เลือก [A09.L04 t=02:01–02:40] [A09.L04 article]
14. เลือก preset ตามคอนเซปต์: Pro Virtual Try On / UGC Virtual Try On (L04), Hyper Motion (L05), Wild Card (L06), TV Spot (L07), Unboxing (L09) [A09.L06 t=00:38–00:45] [A09.L06 t=01:47–01:54] [A09.L07 t=00:36] [A09.L09 t=00:53–01:11]
15. ภาพนิ่ง IG ทำใน NBP อัตราส่วน 3:4 จาก prompt ของ Claude skill ใส่ reference ตัวละคร + prop sheet ของเสื้อผ้า + แว่น [A09.L08 t=00:12–00:42] [A09.L08 article]
16. ภาพสตูดิโอสำหรับเว็บทำใน NBP ด้วย prompt สั้น 4 ช่อง และ upload เสื้อผ้าแต่ละชิ้นเป็น reference แยกกัน [A09.L08 cue c8a] [A09.L08 t=01:02–01:22]
17. เอา ambassador ใส่ภาพสตูดิโอด้วย edit บรรทัดเดียวใน NBP ไม่ต้องถ่ายใหม่ [A09.L08 t=01:30–02:05] [A09.L08 article]
18. Packaging: แนบโลโก้ให้ Claude ขอ packaging concept (ตั้งชื่อคอลเลกชัน "Quantum Cosmos") → รันใน NBP โดยใช้โลโก้เป็น reference [A09.L09 t=00:11–00:37] [A09.L09 cue c9a]
19. Unboxing: preset Unboxing + product (pants) + avatar (Roko) + upload packaging เป็น "additional assets" + ไม่ใส่ prompt → Generate [A09.L09 t=00:53–01:11] [A09.L09 article]

### กฎที่ใช้ซ้ำได้
- อย่าเขียน prompt เอง ให้ Claude รับไอเดียบรรทัดเดียวพร้อม reference แล้วคัดลอกผลลัพธ์ที่มีโครงสร้างไปใช้ [A09.L02 t=00:05–00:15] [A09.L06 t=00:17–00:58]
- ใช้ thread Claude ยาวเส้นเดียวเพื่อให้ context ต่อเนื่อง (ในหน้าจอเห็น prompt ของบทก่อนอยู่ด้านบนเสมอ) [A09.L02 t=01:35] [A09.L06 t=00:20–00:25] [A09.L07 t=00:15–00:30]
- โลโก้ควรจำง่าย ไม่ต้องฉลาดหรือซับซ้อน ตัวอย่างอ้างอิงคือสามแถบของ Adidas, เครื่องหมายถูกของ Nike, ผลแอปเปิลของ Apple [A09.L02 t=00:16–00:26] [A09.L02 article]
- สร้างตัวเลือกราคาถูกก่อน (Soul Cinema 4 รูป ½ เครดิต) แล้วขัดเกลาตัวที่ชนะด้วย edit แทนการ regenerate [A09.L02 t=00:26–00:34] [A09.L03 t=00:50–01:02]
- edit ต้องมี keep-list ชัดเจน: "Recreate this exactly — same A, same B ... change only X" พร้อมค่าที่แม่นยำ เช่นเอียง 3–5° ตามเข็ม [A09.L02 cue c2d]
- เลือกสีแบรนด์ด้วยการ research ไม่ใช่รสนิยม เพราะสีสื่ออารมณ์และสัญญาณของหมวดสินค้า [A09.L02 t=01:13–01:27] [A09.L02 article]
- ใส่ brand hex ลงทุก brief ที่ให้ Claude เพื่อให้สีส่งต่อเข้าไปใน prompt [A09.L03 t=01:59–02:04] [A09.L03 cue c3e] [A09.L03 cue c3g]
- ตั้งชื่อ reference เป็นลำดับและอ้างตามบทบาท เช่น "Change the logo in image 1 with a logo from an image 2" [A09.L03 t=01:00] [A09.L08 frames t=00:40]
- เผื่อรอบสลับโลโก้ให้สินค้าทุกชิ้น เพราะ mockup prompt ของ Claude สร้างแบรนด์ placeholder ขึ้นมาเอง (AXIS, VALE, สัญลักษณ์ X ในวงกลม) [A09.L03 cue c3b] [A09.L03 cue c3d] [A09.L03 cue c3h]
- ให้แบรนด์มีสินค้า "hero" ที่ดังและจำได้ทันทีหนึ่งชิ้น (ของ HIGGS คือ jacket สีนีออน) [A09.L03 t=01:15–01:23] [A09.L03 article]
- ออกแบบชิ้นใหม่ให้เชื่อมชิ้นที่มีอยู่ เช่น กางเกงอยู่ระหว่าง jacket ที่ดังกับ jersey ที่เรียบ (ฐานดำ + เส้นข้างสีไลม์) [A09.L03 t=02:37–02:57] [A09.L03 article]
- แบบทดสอบการออกแบบ: ถ้าเป็นของที่เราจะใส่เอง ก็ควรขาย [A09.L03 t=02:23–02:28]
- เริ่ม preset ของ Marketing Studio แบบ zero-prompt ก่อน แล้วค่อยใส่ prompt เมื่อต้องการคุมความคิดสร้างสรรค์ [A09.L04 t=01:16–02:00] [A09.L05 t=00:05–00:41]
- อย่ารัน preset แบบ "blind" สำหรับงาน TV Spot ให้เล่าไอเดียตัวเองให้ Claude ก่อน [A09.L07 t=00:08–00:32] [A09.L07 article]
- batch ทั้ง catalogue: รัน preset หนึ่งรอบต่อสินค้าหนึ่งชิ้น เพื่อให้มีโฆษณาหลายตัวไว้ทดสอบ [A09.L05 t=00:46–00:56] [A09.L05 article]
- ถ้าจะทำ variant ให้คง character, product, preset ไว้ แล้วเปลี่ยนแค่ prompt [A09.L06 t=03:02–03:08] [A09.L06 article]
- ทำให้สีแบรนด์เป็นสีอิ่มตัวเพียงสีเดียว: โลกเป็น monochrome และสีนีออนมีเฉพาะบนเนื้อผ้า [A09.L04 cue c4a] [A09.L06 cue c6a] [A09.L07 cue c7a]
- ใช้ ambassador คนเดิมทั้ง feed, เว็บ และโฆษณา เพื่อให้ดูเป็น account เดียวกัน และ swap ตัวคนเข้าไปในภาพเดิมแทนการถ่ายใหม่ [A09.L08 t=00:42–00:48] [A09.L08 t=01:30–02:05]
- ตรวจความต่อเนื่องของโลโก้บนทุกพื้นผิวในผลลัพธ์ (พื้นรองเท้า หลัง jacket ด้านหน้า แว่น) [A09.L06 t=02:18–02:33] [A09.L06 article]
- ตั้งชื่อสินค้าบนเว็บให้ดี เพราะชื่อที่ scrape มาจะถูก avatar พูดในโฆษณา ("Velocity Pant") [A09.L09 t=01:35–01:38]
- เลือกเครื่องมือตาม output: ภาพนิ่งสำหรับ feed และเว็บทำใน NBP ไม่ใช่ Marketing Studio [A09.L08 t=00:29] [A09.L08 t=01:02]

### โครงสร้าง Prompt
- c2a (meta-prompt ให้ Claude): "Give me a prompt for a logo for a fashion brand called <NAME>. Accent color <#hex>. <Flat vector, minimal>." [A09.L02 cue c2a]
- c2b (โลโก้ใน Soul Cinema): บรรทัดหัว → composition แนวตั้ง icon บน/wordmark ล่าง → ส่วน ICON (อุปมาจากชื่อแบรนด์ + ตัวเลือก OR) → ส่วน WORDMARK (case/typeface 2–3 ตัวเลือก/สี) → Layout → Aesthetic → negatives ("No gradients. No shadows. No extra elements.") → การใช้งาน ("suitable for embroidery and labels") → แท็ก Style: [A09.L02 cue c2b]
- c2d (edit ใน NBP): "Recreate this logo exactly — same <mark>, same <background>, same composition and proportions — but change only <element>: <change 1>, <change 2 พร้อมองศา/ทิศ>. Keep the same <font>, <colour>, size and position." [A09.L02 cue c2d]
- c2f (variation sheet): "Use the provided logo to generate a clean visual mini-guide." → รายการ variation ที่มีเลขกำกับ → "Present each variation on: white background, black background" → จำนวน output → Style bullets [A09.L02 cue c2f]
- c3b / c3h (mockup เสื้อผ้า): บรรทัดหัว (flat lay, ghost mannequin, #FFFFFF, studio lighting) → หัวข้อ FABRIC & TEXTURE / SILHOUETTE / BASE COLOR / CONSTRUCTION / FRONT GRAPHIC หรือ LOGO / BACK / Colors / Technical พร้อม count lock เช่น "ONE single white stripe ... not three" [A09.L03 cue c3b] [A09.L03 cue c3h]
- c3d (jacket หน้า+หลัง): "Two views ... side by side" + framing lock ("nothing cropped ... collar to hem") + ระบุสิ่งที่ไม่มีอย่างชัดเจน ("No drawstrings, no cords") + placeholder logo + material + style (ghost mannequin, 8K, lookbook) [A09.L03 cue c3d]
- c3f (sneaker sheet ใน NBP): หัว "ONE original <product> in 4 views, 2x2 grid" → LOGO บรรยายด้วยรูปทรง (6-pointed organic star) ไม่ใช่ชื่อ → SHOE DESIGN แยกหัวข้อ → "4 VIEWS" (TOP LEFT ... BOTTOM RIGHT) → PRESENTATION ("All 4 same shoe same colorway", "NO text, NO callouts, NO labels") มุมคือ side, top, heel, sole [A09.L03 cue c3f]
- c4a (Pro Virtual Try-On transformation): CAMERA lock ขึ้นก่อน ("COMPLETELY STATIC throughout") → Location part 1/2 → beat ตามเวลา 0–3s / 4–7s / 8–10s / 11–15s แต่ละ beat ย้ำ "CAMERA STATIC" → ตั้งชื่อ transition ("LIQUID SCAN TRANSITION") ที่สลับฉากและชุดพร้อมกัน → grade ("neon yellow only as real material color on clothing") → "9:16 vertical" [A09.L04 cue c4a]
- c4b (UGC Try-On 5 คลิป): "# <BRAND> — 5 CLIPS" → LOCATION + CAMERA แบบ global ("Same angle all 5 clips, never moves") → negative lock ที่ย้ำทุกคลิป ("NO bag, NO backpack ...") → "## CLIP n — <dur> — <ITEM>" พร้อมสถานะที่ใส่ต่อจากคลิปก่อน ("already wearing ...") + การแต่งตัว 1 action; คลิปสุดท้ายมีบทพูด [A09.L04 cue c4b]
- c5a (logo animation ใน Hyper Motion): วลีสั้นเดียว "<logo> creating with <comet tail>" และใส่รูปโลโก้ในช่อง PRODUCT [A09.L05 cue c5a]
- c6a (skate try-on): ชุดเริ่มต้นของตัวละคร → action ต่อเนื่อง → กฎกล้องเข้มงวด ("strictly side-on ... never rotating. One continuous uncut shot") → กลไกที่ไอเท็มลอยรอแล้วสวมทันที → รายการ "Item n" ครบ 5 ชิ้น → ฉากจบ "Silence." → Sound (diegetic, "No music") → Style [A09.L06 cue c6a]
- c6b (ลอยในเมฆ, Wild Card): "# <TITLE> — ONE SHOT HANDHELD" → Style & Mood (practical VFX, handheld) → Dynamic Description ที่อ้าง "@image_1" พร้อมความไม่สมบูรณ์เพื่อความสมจริง → Static Description พร้อมขอบเขตท่าทาง ("no flips, no spins") → tag คุณภาพ/negative [A09.L06 cue c6b]
- c6c (วิ่งผ่าน portal, Wild Card): นิยาม transition อย่างแม่นยำ ("vertical floor-to-ceiling rectangular cuts ... hard straight-edged cut") → Location 1–6 ระบุเวลาและ props 3–5 อย่าง → ข้อจำกัด transition ("pixel-sharp, hard edge, no blending") → Sound ที่เปลี่ยนตามสถานที่ → Style [A09.L06 cue c6c]
- c7a (TV Spot): ฉาก → การจัดการฉากหลัง (long exposure) → subject + action → colour isolation lock ("Only the clothing fabric is colored, everything else is strictly black and white") → edit device พร้อมเวลา ("negative invert flashes ... 2-3 frames each") → tone → negatives ("No VFX. No box unpacking") [A09.L07 cue c7a]
- prompt social ของ skill (L08): ท่า → เลนส์/มุม → set ที่เห็นในภาพ → แสง → บทบาท reference ทีละรูป ("Character identity referenced from [image_1]. Outfit ... [image_2]. Glasses ... [image_3]") → aesthetic → tag กล้อง/ฟิล์ม [A09.L08 frames t=00:40]
- c8a (ภาพสตูดิโอเว็บ): "Professional studio picture, model wearing all of these clothes. Monochromatic background, side profile view." แล้วให้เสื้อผ้าเป็น reference แยกกัน [A09.L08 cue c8a] [A09.L08 t=01:15]
- swap ตัวตน: "Change the girl in [image 1] into a girl/guy in [image 2], keep the outfit" [A09.L08 t=01:50] [A09.L08 t=02:00]
- c9a (packaging): "Use the provided logo to design a premium packaging concept for a clothing collection called "<NAME>"." → Create: → Concept direction ("Feels like <A> mixed with <B>") → Design details → ส่วน "Bag:" / "Box:" (สี/hex, ข้อความในเครื่องหมายคำพูด, การวางโลโก้) → Presentation → Overall feel [A09.L09 cue c9a]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Claude: ตัวเลือก model บนจอเป็น "Sonnet 4.6" [A09.L02 frames t=00:10]
- Claude Skills panel มี personal skills คือ seedance-director ("Seedance 2.0 — Universal Director"), youtube-scriptwriter, youtube-scriptwriting, product-prompter, youtube-seo, youtube-idea-generator, skill-creator และไฟล์ที่ upload คือ "marketing-studio-director.skill" [A09.L04 t=02:10] [A09.L04 frames t=02:17]
- Soul Cinema: แถบเป็น "Soul Cinema · 16:9 · 2k · On · 4/4 · Color transfer (New)" มีช่อง CHARACTER และ "GENERATE ✦ 0.5" [A09.L02 frames t=00:35] [A09.L03 t=03:00]
- Nano Banana Pro สำหรับ batch 4 รูป: "16:9 · 4K · 4/4 · Unlimited (off)" กับ "GENERATE ✦ 16" [A09.L02 frames t=00:55] [A09.L03 frames t=02:17] [A09.L09 frames t=00:35]
- Nano Banana Pro สำหรับสลับโลโก้: "16:9 · 4K · 1/4" กับ "GENERATE ✦ 4" [A09.L03 frames t=01:00]
- Nano Banana Pro สำหรับภาพสตูดิโอ/swap: "16:9 · 2K · 1/4" กับ "GENERATE ✦ 2" [A09.L08 t=01:15] [A09.L08 frames t=02:04]
- Nano Banana Pro สำหรับ social batch: "3:4 · 4K · 4/4" กับ "GENERATE ✦ 16" [A09.L08 frames t=00:40]
- ภาพ packaging ที่ได้จาก NBP มีขนาด 5504x3072 [A09.L09 t=00:40]
- image model picker แสดง Auto (UNLIMITED), Higgsfield Soul 2.0, Higgsfield Soul Cinema (NEW), GPT Image 2 (NEW), Seedream 5.0 lite, Seedream 4.5, Nano Banana 2, Nano Banana Pro, Grok Imagine (เห็นบนจอ ไม่ได้ใช้ทุกตัว) [A09.L03 t=01:40]
- Marketing Studio มี preset UGC, Tutorial, Unboxing, Hyper Motion, Product Review, TV Spot, Wild Card, UGC Virtual Try On, Pro Virtual Try On [A09.L04 t=00:05]
- ค่า default ของแถบ Marketing Studio คือ 9:16 · 1080p · 15s แต่ TV Spot ตั้งเป็น 16:9 [A09.L04 frames t=00:02] [A09.L07 frames t=00:47]
- ตัวเลขเครดิตบนปุ่ม GENERATE ของ Marketing Studio 15s อ่านได้ "✦ 180 165" (180 ถูกขีด อ่านได้บางส่วน ดูเหมือนราคาลด) [A09.L04 frames t=00:02] [A09.L09 t=01:05]
- Hyper Motion 10s (run โลโก้) อ่านได้ "GENERATE ✦ 120 110" (อ่านได้บางส่วน) [A09.L05 frames t=02:05]
- การ์ดเปิด Marketing Studio มีแบรนด์ "Higgsfield Seedance 2.0 / MARKETING STUDIO" ซึ่งเป็นแค่ branding บนจอ บทเรียนไม่ได้พูดเรื่องนี้ [A09.L01 t=00:45]
- ราคา: UGC ของจริงราว $200–500 ส่วนใน Marketing Studio "less than five bucks" [A09.L04 t=00:34–00:40]
- Pro Virtual Try-On ใช้เวลาสร้างประมาณ 2 นาที ส่วน TV Spot "just a couple minutes" [A09.L04 t=03:12–03:17] [A09.L07 t=01:27]
- preset avatar ที่เห็น: Jayden, Stefan, Mei, Yuna, Adriana, Clara, Maria, Sofia, Valentina และบทหลังเห็น Jia, Lily, Tae เพิ่ม [A09.L04 frames t=01:15] [A09.L07 frames t=00:44]
- การสร้างภาพทั้งหมดทำใน Higgsfield Collab project ("NEW PROJECT IS READY. SHARE & CREATE TOGETHER") [A09.L02 t=00:25–00:30] [A09.L08 t=00:30]
- image viewer มี Overview / Upscale / Enhancer / Relight / Inpaint / Angles และปุ่ม Animate / Publish / Open in / Reference / Download [A09.L02 frames t=01:50] [A09.L03 t=02:20]

### คำเตือนและ failure modes
- wordmark ที่ AI สร้างอาจเล็กเกินหรือเพี้ยน: ผลหนึ่งจาก Soul Cinema สะกดเป็น "hioos" แทน "higgs" [A09.L02 t=00:50] [A09.L02 frames t=00:55]
- รอบแรกที่สลับโลโก้ icon ใหญ่เกินไป ต้องแก้อีกรอบด้วย "make the icon smaller" [A09.L03 t=01:03–01:08] [A09.L03 article]
- hex ใน prompt ที่ AI เขียนอาจพิมพ์ผิด: c3j เขียน #D1EF17 แทน #d1fe17 [A09.L03 cue c3j]
- prompt ที่ AI เขียนอาจกำหนดอัตราส่วนไม่ตรงกับ setting: prompt ของ skill เขียน "vertical 9:16 framing" แต่แถบตั้งเป็น 3:4 [A09.L08 frames t=00:40]
- c6a/c6c ขอ 2.39:1 Cinemascope ทั้งที่แถบตั้งเป็น 9:16 [A09.L06 cue c6a] [A09.L06 cue c6c]
- แว่นต้อง iterate prompt "a few iterations" กว่าจะได้กรอบไล่สีดำ→ไลม์ [A09.L03 t=03:32–03:38] [A09.L03 article]
- c4b ย้ำ "NO bag, NO backpack" ทุกคลิป ซึ่งบอกเป็นนัยว่าโมเดลชอบเติมกระเป๋าให้ avatar (อนุมานจาก prompt ผู้สอนไม่ได้พูด) [A09.L04 cue c4b]
- prompt TV Spot ที่วางจริงมี negatives "NO lightning, NO energy beams, NO particles ... ABSOLUTELY NO PACKSHOT. NEVER SHOW ISOLATED PRODUCTS" ซึ่งบอกเป็นนัยว่า preset มักเติม VFX และ pack shot (อนุมาน) [A09.L07 t=00:45] [A09.L07 frames t=00:47]
- c4a ย้ำ static camera และ "Glasses stay fully intact" ซึ่งบอกเป็นนัยถึงความเสี่ยงเรื่องกล้องขยับและแว่นเสียรูป (อนุมาน) [A09.L04 cue c4a]
- prompt ไอเดียกลางๆ ให้ผลกลางๆ: ใช้ preset เปล่าได้ แต่ "a little bit of effort" (skill) ให้ผลดีกว่า [A09.L04 t=01:54–02:00]
- avatar อาจเริ่มคลิปด้วยชุดเดิมของตัวเอง (Lulu เริ่มในชุดจาก Hellgrind) [A09.L04 t=03:58]
- Pro Virtual Try On ที่มีแว่นเป็นสินค้าชิ้นเดียว โมเดลสร้างเสื้อโค้ทดำที่ไม่ใช่ของ HIGGS ขึ้นมาเอง [A09.L04 t=04:30–04:52]
- บทความบอกว่า swap "keeps clothing, pose, and lighting untouched" แต่ตรวจที่ความละเอียดระดับ tile ไม่ได้ [A09.L08 article] [A09.L08 t=02:00]
- ป้ายร้านในฉากหลังออกมาเป็นตัวอักษรเพี้ยน (อ่านคล้าย "Thai Snont") [A09.L06 frames t=03:17]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- edit prompt จริงของ NBP ที่อ่านจากจอ: "Change the logo in image 1 with a logo from an image 2", "make the icon smaller", "on the left side of the jacket in image 1 add a logo from an image 2" และในช่อง prompt มี image chip แทรกอยู่ [A09.L03 t=01:00] [A09.L03 t=01:10] [A09.L03 t=01:45]
- ทุกการ generate ของภาพนิ่งเห็นแถบ setting และเครดิตชัด (Soul Cinema ✦0.5, NBP ✦2/4/16) ซึ่งบทความไม่ได้ระบุ [A09.L02 frames t=00:35] [A09.L03 frames t=01:00] [A09.L08 frames t=02:04]
- หน้าตา UI ของ Marketing Studio: "TURN ANY PRODUCT INTO A VIDEO AD", gallery "Generate across formats", sidebar "New project / Search / URL to Ad / Projects" [A09.L04 t=00:00]
- product ที่ scrape จากเว็บมีชื่อ "Field Polo", "Orbit Puffer", "Collider Shield", "HIGGS SS26 Technical S..." และต่อมามี "Velocity Pant", "Logo" [A09.L05 t=01:05] [A09.L09 t=01:00]
- audit ตรวจเฟรมแล้วพบว่าทั้ง tile "Orbit Puffer" และ "HIGGS SS26" เป็น jacket สีนีออนทั้งคู่ [A09.L05 frames t=01:10]
- ผล Hyper Motion run 1 ถ่ายเป็นภาพ macro เชิงอุตสาหกรรม (แขนกลประกอบ jersey, macro ปักลายดาว) แล้วจบที่ pack shot ในอุโมงค์สนาม ซึ่งบทความไม่ได้บรรยาย [A09.L05 t=00:10–00:40]
- prompt social ฉบับเต็มที่อ่านจาก hires (fisheye low-angle ระหว่าง C-stand, แสง teal-green, บทบาท image_1/2/3, "Shot on ARRI ALEXA 65") [A09.L08 frames t=00:40]
- mockup โปรไฟล์ IG "higgs" (30 Posts, ผู้ติดตามดูเหมือน "100k") เป็นแค่ภาพ mock ไม่ใช่ตัวเลขจริง [A09.L08 t=00:50]
- TV Spot ปิดด้วย end card โลโก้ HIGGS ซึ่งทั้งบทความและ prompt ไม่ได้พูดถึง [A09.L07 t=01:00]
- Claude skill ติดตั้งผ่าน Customize → Skills → + → Create skill → Upload a skill [A09.L04 t=02:01–02:20] [A09.L04 frames t=02:15]
- เสียงรีวิวที่ avatar พูดใน unboxing ใช้ชื่อสินค้าจากเว็บ ("the Velocity Pant ... this nylon is so crispy ... Higgs yellow lines") [A09.L09 t=01:13–01:28]
- ประกาศแจก merch: 3 ผู้ชนะ ให้คอมเมนต์คอนเซปต์แบรนด์ ประกาศภายในสองสัปดาห์ (ไม่มีในบทความ) [A09.L09 t=02:06–02:15] [A09.L01 t=01:45–01:51]
- ฉากเปิดของ L01 เป็น sizzle ของผลจาก Marketing Studio (กระโดดร่ม selfie, unboxing กล่องนีออน, try-on, review) เป็นตัวอย่างฟอร์แมตที่สอนทีหลัง [A09.L01 t=00:00–00:30]
- ผู้สอนขอให้ motion designer คอมเมนต์ว่าจะคิดค่าทำ logo animation เท่าไร [A09.L05 t=02:25–02:29]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- ที่มาของ Roko: บทความบอกว่า "pulled from Higgsfield's own preset avatars" แต่ transcript และหน้าจอเป็นการ upload ไฟล์ "from Hellgrind" แล้วตั้งชื่อ [A09.L06 t=00:45–00:52] [A09.L06 article]
- ชื่อซีรีส์ของ Lulu: บทความเขียน "How To Grind ... Kickstarter series" แต่ srt เขียน "Hell Grind"/"Hellgrind" [A09.L04 article] [A09.L04 t=03:58]
- L02: srt บอกว่าเลือก "the last one" แต่รูปที่วางกลับเข้า Claude ตรงกับ tile ที่สอง (ดาวสี่แฉก + "higgs" serif ที่กดหัวใจไว้) [A09.L02 frames t=00:55] [A09.L02 frames t=00:45]
- c3j สั่ง "floating on pure black backdrop" และ "No logos" แต่ภาพสุดท้ายอยู่บนพื้นขาวและมีโลโก้ (เลือก tile พื้นขาวแล้วสลับโลโก้ใน NBP) cue อาจไม่ใช่ prompt สุดท้าย [A09.L03 cue c3j] [A09.L03 frames t=03:40]
- prompt TV Spot ที่วางใน Marketing Studio ไม่ตรงกับ c7a (มี orbit 180° และ "ABSOLUTELY NO PACKSHOT" เพิ่ม) และส่วนหัวของ prompt ยังอ่านไม่ได้ ไม่รู้ว่าฉบับไหนสร้างผลที่เห็น [A09.L07 frames t=00:47] [A09.L07 cue c7a]
- c6b ใส่ tag "Stylized 3D animation" ขัดกับ framing แบบ photoreal ข้างหน้า [A09.L06 cue c6b]
- หลักฐานว่า Marketing Studio ใช้ Seedance 2.0 มีแค่ branding บนการ์ด L01 ส่วน Hyper Motion ไม่มีการพูดหรือแสดงชื่อโมเดล [A09.L01 t=00:45] [A09.L05 frames t=02:05]
- ตัวเลขเครดิต GENERATE ของ Marketing Studio อ่านได้บางส่วนเท่านั้น ("✦ 180 165") ต้นทุนที่พูดชัดมีแค่ "½ credit" กับ "UGC < $5" [A09.L04 frames t=00:02] [A09.L02 t=00:26–00:34]
- Pro Virtual Try-On ตัวที่สาม (แว่นอย่างเดียว) ไม่มี prompt บนจอและไม่มีใน cue [A09.L04 t=04:22–04:30]
- beat หิมะ/ไฟ/น้ำ/ของมีคมของ Hyper Motion run 2 มีแค่คำบรรยาย ไม่มีใน tile ใดเลย จึงยังไม่ได้ตรวจด้วยภาพ [A09.L05 t=01:29–01:40]
- ป้ายชื่อ "Malik" ใน avatar library ถูกตัดหาย ตรวจด้วย hires แล้วก็ยังยืนยันไม่ได้ [A09.L07 frames t=00:44]
- ไฟล์ Claude skill และ "prompts in the description" ไม่มีอยู่ในวัสดุคอร์ส [A09.L04 t=02:05] [A09.L08 t=00:55]
- "(9x9 Pro)" ในบทความ L08 เป็นข้อความเพี้ยน [A09.L08 article]
- L03 มุมของ sneaker: ผู้สอนพูดว่า "side, top, bottom, back" แต่ cue/บทความเขียน side, top, heel, sole (audit ให้ยึด cue c3f) [A09.L03 cue c3f] [A09.L03 t=02:19]

### เทียบกับ v1
- เพิ่ม: บทบาทของ Claude ในฐานะคนเขียน prompt ทุกขั้นและการใช้ thread เดียว ซึ่ง v1 ไม่พูดถึงเลย [A09.L02 t=00:05–00:15] [A09.L06 t=00:20–00:25]
- เพิ่ม: pipeline สินค้า Soul Cinema → NBP logo swap แบบ image 1/image 2 และปัญหาแบรนด์ placeholder (AXIS/VALE) [A09.L03 t=01:48–01:56] [A09.L03 cue c3b]
- เพิ่ม: ต้นทุนและ setting ที่เห็นบนจอ (Soul Cinema ✦0.5 ต่อ 4 รูป, NBP ✦16 ต่อ 4 รูป 4K, Marketing Studio 9:16/1080p/15s) [A09.L02 frames t=00:35] [A09.L02 frames t=00:55] [A09.L04 frames t=00:02]
- เพิ่ม: ขั้นสร้าง product จาก URL, upload avatar และทางเลือก zero-prompt [A09.L04 t=00:41–01:52]
- เพิ่ม: โครง prompt แบบ timecoded beats และ negative lock ที่ย้ำทุกคลิป (c4a/c4b/c6a/c6c) [A09.L04 cue c4a] [A09.L04 cue c4b]
- แก้: v1 A09.05 เขียนว่าภาพ stress test "ไม่ใช่หลักฐานความทนทานของสินค้าจริง" ข้อนี้เป็นคำเตือนที่ v1 เพิ่มเอง ในคอร์สผู้สอนนำเสนอว่าเป็น proof content ("I'm sending them this video") [A09.L05 t=01:44]
- แก้: v1 A09.04 ให้ "ตรวจ fit มือจับ และขนาดแว่น" แต่ในคอร์สสิ่งที่ตรวจคือโลโก้ต้องต่อเนื่องและแว่นต้องสะอาดเห็นโลโก้ด้านข้าง ส่วนเรื่องมือจับไม่ได้พูดถึง [A09.L04 t=03:00] [A09.L06 t=02:18–02:33]
- แก้: v1 A09.08 เขียนว่า "ภาพพื้นเรียบหลายมุม" แต่ในคอร์สภาพสตูดิโอเว็บเป็น side profile 1 รูปจาก prompt สั้น โดยใส่เสื้อผ้า 5 ชิ้นเป็น reference [A09.L08 cue c8a] [A09.L08 t=01:20]
- แก้: v1 A09.03 ไม่มี jersey/T-shirt ในรายการสินค้า แต่คอร์สมีครบ 5 ชิ้นและ packaging [A09.L03 t=00:09–00:20]
- เหมือนเดิม: ลำดับ โลโก้ → สินค้า → โฆษณา → packaging และการใช้ ambassador ต่อเนื่อง [A09.L02 t=00:00] [A09.L08 t=00:42–00:48]
- เหมือนเดิม: TV Spot ที่โลกเป็น monochrome แต่ชุดเป็นสี และใช้ flash ตอน cut [A09.L07 cue c7a]
- เหมือนเดิม: ส่ง packaging เป็น reference เข้า unboxing (คอร์สใช้ช่อง "additional assets") [A09.L09 t=00:53–01:11]

## A10 Make a Cinematic Ad End-to-End

### ภาพรวมและผลลัพธ์
- คอร์ส 10 บทนี้ผู้สอนคือ Adil (@ADILINTHEWILD) ทำโฆษณาฟุตบอลแบบ halftime ให้กระป๋องโซดา "TOP UP" ด้วยเว็บไซต์เดียวแทนงบสตูดิโอ [A10.L01 t=00:38] [A10.L01 article]
- pipeline มี 3 ขั้น: (1) assets ใน Soul Cinema และ GPT Image 2, (2) Claude skill/system prompt ที่เขียน shot prompt, (3) สร้างฉากด้วย Seedance 2.0 [A10.L01 t=00:41–00:50] [A10.L01 article]
- เรื่องในโฆษณา: ผู้ชายบนถนน NYC ที่ว่างเปล่าดื่มกระป๋องที่ลอยอยู่ กลายเป็นหุ่นฟุตบอล #7 ดวลกับหุ่นดำ #9 แพ้รอบแรก ล้มเพราะหมดพลัง ดื่มอีกครั้ง กลับมายิงประตู ทำท่าเก๊ก แล้วจบด้วย pack shot [A10.L01 t=01:00–02:40]
- twist ส่วนตัวของคอนเซปต์คือฟุตบอลผสมการ์ตูนหุ่นยนต์มีชีวิตแบบ Jetix เพราะโฆษณาฟุตบอลทั่วไปมีเยอะเกินแล้ว [A10.L01 t=02:45] [A10.L01 article]
- ชื่อแบรนด์ "TOP UP" อ่านได้จากกระป๋องและ pack shot เท่านั้น บทความไม่ได้บอก [A10.L01 t=01:10] [A10.L01 t=02:40]
- ข้อความสำคัญของคอร์ส: หนังที่เสร็จคือไม่กี่วินาทีที่ดีที่สุดจากราว 100 ครั้ง ดังนั้นทักษะจริงคือการ iterate [A10.L10 t=02:14–02:22] [A10.L10 article]
- ใช้ workflow เดิมได้แม้เปลี่ยนสินค้าหรือตัวละคร [A10.L10 t=02:23–02:29] [A10.L10 article]

### Workflow ทีละขั้น
1. เปิด project แยกใน Higgsfield Collab (ไม่ใช่หน้า Images) เพื่อให้ทุก model และ output ของโฆษณานี้อยู่ที่เดียวและแชร์ได้ [A10.L02 t=00:10] [A10.L02 article]
2. ทำ product sheet ของกระป๋อง (front/back/top) จากรูปสินค้ารูปเดียวด้วย GPT Image 2.0 เพื่อไม่ให้ video model เดาด้านที่มองไม่เห็นเอง [A10.L02 t=00:30–00:57] [A10.L02 cue cue-can-sheet]
3. สร้าง Soul character จากรูปตัวเอง 20 รูป: Character > upload 20 images ("the more you do here, the better") [A10.L02 t=01:09–01:20] [A10.L02 article]
4. ทำ character sheet ใน Soul Cinema โดยสั่งแค่ layout ไม่ระบุชุด แล้วรัน batch ใหญ่ราคาถูก (16:9, 2K, enhancer on, 40 รูป; 8 รูป = 1 credit) จากนั้นเลือกชุด [A10.L02 t=01:24–02:20] [A10.L02 article]
5. ทำ location still ใน Soul Cinema ด้วย anamorphic lens + shallow DoF + film grain ซึ่งรันไป 10 รอบ [A10.L02 t=02:50–03:17] [A10.L02 cue cue-location]
6. ทดสอบ character + location ด้วยกัน: ให้ Claude เขียน test shot สั้นๆ แล้วรัน Seedance 2.0 แบบ 5 s, 1 generation ถ้าผ่านก็ล็อกทั้งคู่ [A10.L02 t=03:30–04:34] [A10.L02 article]
7. ให้ Claude เขียน sheet prompt ที่มีโครงสร้างสำหรับหุ่น #7, หุ่นคู่แข่ง #9 (prompt เดียวกัน เปลี่ยนแค่ palette และเลข), บอล และประตู shield แล้วรัน batch ใน Soul Cinema และคัดเลือก [A10.L02 t=04:41–07:54] [A10.L02 article]
8. ติดตั้ง Claude skill (Customize > Skills > + > Upload a skill) แล้วเปิด chat ใหม่ [A10.L03 t=00:46–01:00] [A10.L03 article]
9. แนบ script PDF พร้อมบอกว่า "pdf file is the script" แนบ asset ที่ล็อกแล้วทั้งหมด และประกาศแต่ละชิ้นเป็น "@handle — description" [A10.L03 t=01:00–01:52] [A10.L03 article]
10. ลงทะเบียน asset ทุกชิ้นเป็น Element ใน Collab (+ > Elements > Create element) โดยตั้งชื่อตรงกับใน Claude ทุกตัวอักษร [A10.L04 t=00:06–00:36]
11. แต่ละฉาก: ส่ง brief สั้นภาษาธรรมดาให้ Claude → Claude คืน prompt เต็มที่มี style header ร่วม → วางใน Seedance 2.0 (16:9, 1080p, 15 s) รัน 4 batch [A10.L04 t=01:04–02:08] [A10.L04 article]
12. ดูผล แล้วบอกจุดเสียให้ Claude ในรูปแบบ director notes แทนการแก้ prompt เอง จากนั้นทดสอบ fix ด้วย 1 generation ก่อนรัน batch [A10.L04 t=04:21–05:02] [A10.L04 article]
13. ถ้าผลแบน ให้เปลี่ยนจากการเล่าเรื่องเป็นการกำกับทีละช็อตว่ากล้องเห็นอะไร พร้อมคำสั่งกล้องในทุกช็อต [A10.L05 t=01:19–02:08] [A10.L05 article]
14. ถ้าวัตถุเลื่อนที่ ให้ทำ location scheme: plate มุมสูงจาก GPT Image 2 → วาดจุดด้วยมือ → GPT Image 2 วางวัตถุและทำแผนที่มีป้าย → ประกาศให้ Claude และเพิ่มเป็น Element [A10.L06 t=02:57–04:45] [A10.L06 cue cue-location-scheme]
15. ตรวจโครงเรื่องระหว่างตัดต่อ (พระเอกต้องแพ้ก่อน) วางแผนฉากใหม่ และเก็บ footage ที่ดีแต่ไม่ตรงแผนไว้ใช้ [A10.L06 t=01:01–01:31] [A10.L06 article]
16. ฉากที่แน่นเกินให้แยกเป็นหลาย prompt [A10.L07 t=02:25–02:39] [A10.L07 article]
17. reuse: ต่อยอด prompt เดิม ใช้ take ที่ยังไม่ได้ใช้ และสร้างเฉพาะช็อตที่ขาดแล้วตัดเข้า footage เดิม [A10.L08 t=00:09–02:43] [A10.L07 t=06:35–06:57]
18. ปิดเรื่องด้วยมุก (ให้ Claude เสนอตัวเลือก) และ pack shot ที่มีสินค้าตก, ชื่อแบรนด์ประกอบตัว, tagline แล้วขัดเกลาด้วย note เรื่องกล้องและแสง [A10.L09 t=00:14–02:49] [A10.L09 article]
19. ตัดวินาทีที่ดีที่สุดจากทุก batch เข้าแต่ละฉาก แล้วต่อทุกฉากเป็นหนัง [A10.L04 t=02:48–02:52] [A10.L10 t=00:00]

### กฎที่ใช้ซ้ำได้
- สร้างและล็อกทุกองค์ประกอบที่ใช้ซ้ำ (character, location, props, product) เป็นภาพ reference ก่อนสร้างวิดีโอ [A10.L01 t=00:41] [A10.L10 t=01:55]
- location คือ "the most important image" เพราะวิดีโอดึง texture และแสงจาก still ที่ใส่เข้าไป location ที่ดูพลาสติกจึงทำให้ทุกช็อตเสีย [A10.L02 t=02:24–02:34] [A10.L02 article]
- ทดสอบ asset สำคัญร่วมกันด้วยต้นทุนต่ำ (5 s, 1 gen) ก่อนล็อก: "Key assets need to be tested before we lock them in" [A10.L02 t=03:35] [A10.L02 t=04:11–04:18]
- ขอให้ Claude คิดทางออกด้านกล้อง (dynamic movement, Dutch angle, low angle) แทนการกำหนดทุกการเคลื่อนไหวเอง [A10.L02 t=04:01]
- ทำหุ่นคู่แข่งจาก prompt ของหุ่นพระเอก โดยเปลี่ยนแค่ palette และเลข เพื่อให้อยู่โลกเดียวกัน [A10.L02 t=05:36–06:03] [A10.L02 article]
- คัด batch ด้วยเกณฑ์ที่ชัด: ตัดตัวที่ดูการ์ตูน ใหญ่เกิน แสงผิด (แสงสีฟ้า) มีหมวกที่ไม่จำเป็น หรืออ่านเลขไม่ออก [A10.L02 t=05:18–05:36] [A10.L02 t=06:16–06:34]
- props ต้องต่อเนื่องเหมือน character: ล็อกบอลและประตูเป็น asset แยก และออกแบบประตูให้เข้ากับโลก (shield ไฟฟ้า ไม่ใช่ตาข่าย) [A10.L02 t=06:44–07:48] [A10.L02 cue cue-goal]
- ตั้งชื่อ asset ให้ตรงกันใน Claude (@handle) และใน Higgsfield Elements เพื่อให้ prompt ที่วางแนบ reference เองอัตโนมัติ [A10.L04 t=00:39–00:43] [A10.L04 t=01:51–01:56]
- ใช้ style header ร่วมกันในทุก prompt และระบุ "No music, environmental SFX only" เสมอ แล้วค่อยใส่ score ตอนตัดต่อ [A10.L04 t=01:26–01:46] [A10.L04 article]
- ทำฉากแรกให้ดีที่สุด เพราะ "if the first thing you see feels off you stop watching" [A10.L04 t=01:00] [A10.L04 article]
- อย่าแก้ prompt ด้วยมือ ให้ดูผลแล้วส่ง director notes ภาษาธรรมดาที่ไล่ทุกจุดเสียให้ Claude [A10.L04 t=04:21–04:57] [A10.L07 t=01:09–01:33]
- ถ้าผลดีแล้ว ให้ดันต่ออีกขั้นด้วย note เจาะจง เช่น super macro ของชิ้นเกราะที่ล็อกเข้าที่ [A10.L04 t=05:18–05:41] [A10.L04 article]
- ให้ทุกช็อตมีคำสั่งกล้องของตัวเอง เพราะ low angle + handheld shake ให้ความรู้สึก "real sports ad" [A10.L05 t=02:15–02:33] [A10.L05 article]
- สร้างความตึงก่อนเปิดเผย: ขา/บอลของคู่แข่งก่อน → OTS จากพระเอก → ท่าเตรียมพร้อมของพระเอก [A10.L05 t=01:31–01:59] [A10.L05 article]
- เพิ่ม macro insert สั้นๆ ที่ไม่มีตัวละครเพื่อให้งานตัดต่อดูแพง ซึ่งเป็นช็อตที่สร้างง่ายที่สุด [A10.L05 t=03:16–03:43] [A10.L05 article]
- ยอมรับผลที่ได้บางส่วน: ใช้ส่วนที่ใช้ได้ แล้วทิ้งส่วนที่ไม่ได้ (เช่นการระเบิด) [A10.L05 t=04:40–04:44] [A10.L07 t=02:03–02:09]
- ฉาก action หลายตัวละครให้รันหลาย batch แล้วตัด phase จากหลาย generation มาต่อกัน ซึ่งดูเป็นธรรมชาติกว่า [A10.L06 t=00:30–00:49] [A10.L06 article]
- ถ้าโมเดลไม่มี anchor ของตำแหน่ง มันจะเดาตำแหน่งใหม่ทุกครั้ง การเพิ่มคำไม่ช่วย ให้ใช้ภาพแทน: "a map beats a paragraph" [A10.L06 t=02:40–02:52] [A10.L06 t=05:15–05:21]
- props ที่ใช้ครั้งเดียวไม่ต้องทำเป็น asset แค่เขียนบรรทัดเดียวใน prompt ก็พอ (นาฬิกาที่ขึ้น "TOP UP") [A10.L07 t=01:48–02:03] [A10.L07 article]
- แยกฉากที่แน่นเป็น generation ย่อย และเพิ่ม "air between the actions" ให้ beat การแสดง (หาก่อน แล้วค่อยยิ้ม) [A10.L07 t=02:31] [A10.L07 t=03:15–03:42]
- ให้ตัวละครเป็นคนทำ action เอง (เปิดกระป๋องเอง) เพื่อเลี่ยงเหตุการณ์ "magic" และ SFX ที่เกิดอัตโนมัติ [A10.L07 t=05:03–05:40] [A10.L07 article]
- ตรวจความต่อเนื่องกับช็อตข้างเคียง: ชิ้นเกราะต้องอยู่บนพื้นตั้งแต่ต้น และต้องลอยขึ้นจากพื้นถนน ไม่ใช่โผล่จากอากาศ [A10.L07 t=04:52–05:58] [A10.L07 article]
- ถ้าส่วนยากแก้ได้แล้ว ให้ต่อยอด prompt เดิม และถ้าไม่รู้ศัพท์เฉพาะ (stepovers, nutmegs, feints) ให้ถาม Claude [A10.L08 t=00:09–00:38] [A10.L08 article]
- ใช้ phase ที่ยังไม่ได้ใช้จาก batch ก่อน: "a trick that saves you credits" [A10.L08 t=01:02–01:13] [A10.L08 article]
- ตัดสิน generation จากเฉพาะช่วงที่ต้องการ ("these generations don't need to be perfect") [A10.L08 t=02:11–02:31] [A10.L08 article]
- ให้ Claude เสนอมุกหลายแบบแล้วเลือกจากเหตุผลว่าทำไมมันตลก และยังรัน batch สำรองแม้ผลแรกจะได้แล้ว [A10.L09 t=00:14–01:05] [A10.L09 article]
- pack shot คือ "the one that sells" และเป็นภาพสุดท้ายที่คนดูเห็น ให้แก้ด้วยการสั่งกล้องชัด และอ้างแสงจากฉากก่อนโดยระบุชื่อฉาก ("match it to scene one") [A10.L09 t=01:23–02:40] [A10.L09 article]

### โครงสร้าง Prompt
- prompt ของ skill มีโครง SUBJECT, LOCATION, LAYOUT/@scheme (ใส่ถ้ามี), ACTION ที่มี SHOT ตามเวลา, CAMERA, STYLE 60:30:10, CONSTRAINTS แต่ละ prompt ยาว ~15s และใช้เดี่ยวได้เพราะใส่ Style Prefix ไว้แล้ว (อ่านจากหน้า skill ได้บางส่วน) [A10.L01 frames t=00:35]
- Style prefix ของ skill: Style 8K photorealistic (no 3D render/game engine) / Lighting natural only, contre-jour / Color 60:30:10 / Camera 180° shutter / Skin pore-level / Acting micro-pauses / Physics "No floating props" / Continuity "No identity drift" / Technical 24fps / Audio "Environmental SFX only. No music. No subtitles." [A10.L01 frames t=00:35]
- กฎ LOCATION ของ skill: "@location is a STYLE REFERENCE ONLY, not a fixed keyframe ... Do not reproduce the reference 1:1." [A10.L01 frames t=00:35] [A10.L04 cue cue-scene-2]
- cue-can-sheet (GPT Image 2): "Make a product sheet with [front, back, top] for the product from @image_1" [A10.L02 cue cue-can-sheet] [A10.L02 t=00:38–00:46]
- cue-character-sheet (Soul Cinema): "[sheet type] — two panels. Left: [full body]. Right: [face close-up]." ไม่ระบุชุดและฉาก [A10.L02 cue cue-character-sheet] [A10.L02 t=01:32–01:39]
- cue-location: comma list "Modern New York City street, empty, sunny day, clear blue sky, cinematic, anamorphic lens, shallow depth of field, film grain" [A10.L02 cue cue-location] [A10.L02 t=03:15]
- cue-location-test (Seedance): แยก 2 บล็อก [VISUAL] (rig/ความสูงกล้อง, dutch 15°, subject <<<image_1>>> พร้อมรายการเสื้อผ้า, beats, เลนส์ 35mm) และ [AUDIO] ("NO MUSIC. SFX ONLY" + รายการเสียง diegetic) [A10.L02 cue cue-location-test]
- cue-robot-sheet: layout 2 view (FRONT/REAR, gray seamless) / scale 2.5x human / สัดส่วนสี white 60% red 30% cyan 10% / เลข 7 ที่อก / functional details / รายละเอียดแยกตาม view / three-point lighting / render style [A10.L02 cue cue-robot-sheet]
- prompt ของหุ่น #9 ที่ Claude เขียน (อ่านจาก hires) ใช้โครงเดียวกันและมีหัวข้อ "UNIT-9 // FOOTBALL EXOSUIT" [A10.L02 frames t=07:55]
- cue-goal: "Photoreal 8K product still:" + วัตถุ (ขนาด, energy field, rim, emitter base) + gray backdrop + "16:9, WB 6500K" + "No characters, no text" [A10.L02 cue cue-goal]
- element registry ใน Claude: invoke skill + "pdf file is the script" + "add" + หนึ่งบรรทัดต่อ asset แบบ "@kebab-case-handle — [who/what], [จุดเด่น]" เช่น "@goal-shield — Electric round shield, energy-field goal" [A10.L03 t=01:55] [A10.L03 t=01:18–01:52]
- cue-scene-1: [VISUAL] look header → @city-location → @adils-topup → rig + dutch องศา → "Beat one...five" → พฤติกรรมของ @topup → "Slow-motion ramping" ต่อ beat (100/60/70/40/100) → [AUDIO] "NO MUSIC. SFX ONLY" [A10.L04 cue cue-scene-1]
- cue-scene-2 (template มีป้าย): global header (Style ... Audio) → SUBJECT ("matches input 100%", start → end state) → MULTISHOT → PRACTICAL VFX (ชิ้นโลหะบิน ไม่ใช่ nano-particles) → LOCATION STYLE REFERENCE ONLY → ACTION SHOT 1–11 ตามเวลา 0:00–0:15 ทุกช็อตจบด้วย "Hard cut" → CAMERA → STYLE (WB 6500K, no glowing eyes) → CONSTRAINTS [A10.L04 cue cue-scene-2]
- director note รูปแบบ: แก้ motion + แก้กล้อง + "IMPORTANT:" แก้ทิศทาง + แก้หน้า เช่น "IMPORTANT: He runs forward, not backward. And fix the face natural smile, alive eyes, NO color change" [A10.L04 t=04:50]
- note แบบรักษา+เพิ่ม: "I like the result overall, but let's edit it again. I want super macro close-ups on the robot body pieces locking, the chest plate, the wrists, [helmet]" [A10.L04 t=05:35]
- cue-scene-3: SUBJECT ระบุความสูง (1.85m) และขนาดบอล → SHOT 1–5 ทางกายภาพละเอียด (km/h, cm, องศาข้อต่อ) → CAMERA global (shake 6–10cm, low angle, dutch ทุกช็อต) + FOV ต่อช็อต (18/35/47/35/63) → CONSTRAINTS (NO FADE, SHOT 2 = หุ่นตัวเดียวกับ SHOT 1, กล้องไม่นิ่ง) [A10.L05 cue cue-scene-3]
- brief แบบทีละช็อต: Shot A (subject + action) → "Then cut to" Shot B (POV/framing) → "Then cut to" Shot C → กฎกล้อง [A10.L05 t=02:00]
- brief ของ insert: จำนวน + subject แล้วไล่ "First / Second / Third" ให้แต่ละ beat มีหน้าที่เดียว [A10.L05 t=04:15] [A10.L05 cue cue-scene-4]
- cue-scene-5: กฎการครองบอลใส่ไว้ก่อน ("ball is always at the feet of whoever controls it ... only changes owner on a clean tackle") → SHOT 1–5 → CONSTRAINTS "Do NOT over-detail kick mechanics" [A10.L06 cue cue-scene-5]
- cue-location-plate: "High angle wide shot of the @location." และ cue-location-scheme: "Put the @goal shields into @image_1 where the circles are located and create a "LOCATION SCHEME WITH GOAL SHIELDS"" [A10.L06 cue cue-location-plate] [A10.L06 cue cue-location-scheme]
- การประกาศ scheme ให้ Claude: "@scheme - a location scheme for the goal shields. In every generation, the goals must appear exactly according to this @scheme. Also, use goal shields as a reference n[ot a keyframe]" [A10.L06 t=04:30]
- cue-scene-7 เพิ่ม style anchor ตามยุค ("mid-2000s practical robot suit commercials ... NOT a video game render"), บล็อก HEAVY HANDHELD และโมดูลฟิสิกส์ BALL (22cm, 7kg) / ROBOT PHYSICS (110kg, hydraulic delay) [A10.L07 cue cue-scene-7]
- note แก้ staging ใช้ตัวพิมพ์ใหญ่เน้นคำ: "face DOWN ... LEFT wrist ... searching for it FIRST, and THEN breaks into a smile ... stay in ONE spot" [A10.L07 t=03:50]
- note แก้หลายจุด: "A few fixes for scene 8 part 2." แล้วไล่ทีละข้อ เช่น "The can should NOT open on its own — he opens it himself with a clear action, no automatic hiss." [A10.L07 t=05:55]
- cue-scene-9 เป็น template กฎ: "Create one seamless 15-second cinematic action scene, not a storyboard, not panels, not a montage grid" + กฎดวล + timeline 0.0–15.0 sec แบ่งช่วง ~1.3 s แต่ละช่วงนำด้วยเทคนิคกล้อง (Snorricam feel, Split Diopter, Bullet Time accent ...) [A10.L08 cue cue-scene-9]
- cue-scene-10 เพิ่มบล็อก LAYOUT: "@scheme is an aerial top-down reference ... Use @scheme to place the @goal-shield goals correctly ... same positions and scale" [A10.L08 cue cue-scene-10]
- คำขอแบบต่อยอด: "Take <prompt เดิม> but this time before <beat>, add <action 1 อย่าง + detail 1 อย่าง>" [A10.L08 frames t=01:59]
- cue-scene-11: "MULTISHOT — comedic beat, played straight but funny" + CONSTRAINTS "Pure visual gag ... Played straight, timing sells the joke." [A10.L09 cue cue-scene-11]
- cue-scene-12 (pack shot): Beat 1–5 (ตกที่ 40 km/h → ฝัง 15 cm → ชิ้นโลหะประกอบตัวอักษร T-O-P-U-P จากซ้ายไปขวา → lightning 1 เส้น → tagline "POWER UP YOUR DAY") + CAMERA 47° + STYLE 6000K, กระป๋องผิวด้าน [A10.L09 cue cue-scene-12]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Seedance 2.0 ใช้กับวิดีโอทุกฉาก: 16:9, 1080p, 15 s และมี resolution ให้เลือก 480p / 720p / 1080p [A10.L04 t=01:56–02:08] [A10.L04 t=02:00]
- แถบ Seedance 2.0 ตอน 15s 1080p 2/4 แสดงราคา 360 ขีดฆ่า → 270 [A10.L02 frames t=04:13]
- แถบ Seedance 2.0 default (Auto, 1080p, 8s, 1/4) แสดง 96 ขีดฆ่า → 72 [A10.L04 frames t=00:07]
- Soul Cinema: 16:9, 2k, enhancer On, 4/4 ใช้ราว 0.5 credit [A10.L02 frames t=02:56] [A10.L02 t=03:15]
- Soul Cinema แบบ 1:1, 1.5k, enhancer Off, 1/4 ใช้ 0.125 [A10.L02 frames t=01:39]
- ในบท character sheet ผู้สอนพูดว่า 40 รูป และ 8 รูป = 1 credit ดังนั้น 40 รูป = 5 credits [A10.L02 t=01:42–02:00] [A10.L02 article]
- GPT Image 2 สำหรับ can sheet: 16:9, High, 2K, 1/4 ใช้ 7 [A10.L02 frames t=00:44]
- GPT Image 2 สำหรับ location plate: 16:9, High, 4K, 1/4 ใช้ 12 และ scheme แบบ 2K ใช้ 4 [A10.L06 frames t=03:03] [A10.L06 frames t=03:40]
- หน้า Character: dropdown model อ่านได้ "Soul 2.0", ring จำนวนรูป "20 /80" มีป้ายแดง "Bad" กับคำแนะนำ "Upload 20+ photos for best results", Quality "1440 px" "Perfect", ปุ่ม Create ใช้ 25 [A10.L02 frames t=01:15]
- Claude: skill chip "seedance-prompt-structure" อยู่ใน project "Higgsfield" และตัวเลือก model อ่านได้ "Fable 5 High" [A10.L03 frames t=01:02] [A10.L03 t=01:00]
- หน้า skill แสดง Added by "You", Last updated "Jun 8, 2026", Trigger "Slash command + auto" [A10.L01 frames t=00:35]
- dialog Upload skill ต้องการไฟล์ ".md file must contain skill name and description formatted in YAML" หรือ ".zip or .skill file must include a SKILL.md file" [A10.L03 frames t=00:57]
- Collab Elements panel มีแท็บ Uploads / Image Generations / Video Generations / Elements / Liked และ dialog New element มี "Element name (Required)", Category "Auto", Advanced settings [A10.L04 t=00:08–00:20]
- โปรแกรมตัดต่อที่ใช้ไม่ได้บอกชื่อ เห็นแค่ timeline ที่มีบล็อกสี [A10.L04 frames t=06:10] [A10.L05 t=02:50–02:55]
- หน้า home ของ Higgsfield ที่เห็นผ่านๆ มี tile Supercomputer, Nano Banana Pro, Seedance 2.0, Marketing Studio, Higgsfield Canvas, Cinema Studio 3.5, MCP & CLI [A10.L02 frames t=00:12] [A10.L02 t=00:10]
- WB ตามที่ระบุใน cue: ส่วนใหญ่ 6500K, ฉาก 8 part 1 ใช้ 5600K dawn, pack shot ใช้ 6000K [A10.L07 cue cue-scene-8-part-1] [A10.L09 cue cue-scene-12]

### คำเตือนและ failure modes
- ถ้าไม่มี product sheet หลายมุม video model จะเดาด้านกระป๋องที่มองไม่เห็นเอง [A10.L02 t=00:54] [A10.L02 article]
- การเปิด prompt enhancer ให้ความหลากหลายสูงแต่มีผลเสียปนมาด้วย (ดูการ์ตูน ใหญ่เกิน) [A10.L02 t=05:18–05:29]
- prompt ที่ใส่ข้อมูลเกินจำเป็นเปลืองเวลาและเครดิต และวงจรลอง-ไม่ชอบ-แก้-ลองใหม่โดยไม่มีโครงสร้างทำให้ไอเดียหลุด [A10.L03 t=00:15–00:40] [A10.L03 article]
- ถ้า generation ใส่เพลงมา จะชนกับ score ที่ใส่ตอนตัดต่อ จึงต้องใส่ "no music" ใน prompt [A10.L04 t=01:37] [A10.L04 article]
- ฉาก 2 รอบแรกเสียแบบ: รอยยิ้มเพี้ยน, ตัวละครวิ่งถอยหลัง, ตาว่างแล้วกลายเป็นสีฟ้า, transformation "not epic at all, he just stands there" [A10.L04 t=03:53–04:20] [A10.L04 article]
- prompt ที่เล่าแต่เรื่องได้ wide shot นิ่ง หุ่นแทบไม่ขยับ และไม่มีความตึงเลย ถึงสองรอบ และ note กว้างๆ ก็แก้ไม่ได้ [A10.L05 t=00:57–01:25] [A10.L05 article]
- ถ้าไม่มี anchor ของตำแหน่ง ประตูจะย้ายที่ระหว่าง generation หรือวาร์ปกลางช็อต และบางครั้งภาพ reference ขึ้นมาเป็น keyframe เต็มจอ [A10.L06 t=02:14–02:40] [A10.L06 article]
- ถ้าพระเอกชนะเร็วเกิน เรื่องก็จบ [A10.L06 t=01:03] [A10.L06 article]
- ฉาก 7 รอบแรก: ล้มแบบไม่มีน้ำหนัก และเกราะ "slices off" ในราว 1 วินาทีจนดูปลอม การแก้ฟิสิกส์คือส่วนที่ "the trickiest" [A10.L07 t=00:43–01:09] [A10.L07 article]
- ฉาก 8 part 1 รอบแรก: ปฏิกิริยาเร็วไป (เห็นกระป๋องแล้วยิ้มทันที) [A10.L07 t=03:15–03:21] [A10.L07 article]
- ฉาก 8 part 2 รอบแรก: ไม่มีเกราะแตกบนพื้น (ไม่ต่อเนื่องกับช็อตก่อน), กระป๋องเปิดเองพร้อมเสียงฟู่อัตโนมัติ, ไม่มี close-up ตอนแปลงร่าง, นิ่งเกินไป [A10.L07 t=04:49–05:19] [A10.L07 article]
- pack shot รอบแรก: นิ่งเกินไป, การประกอบชื่อไม่แรง, แสงแดดไม่เข้ากับทั้งเรื่อง [A10.L09 t=01:57–02:30] [A10.L09 article]
- อย่าคาดหวังว่าจะได้ในครั้งแรก "truth nobody tells you" คือหนังตัดมาจากความพยายามหลายครั้ง [A10.L10 t=02:14] [A10.L10 article]
- การสร้างฉากเปลืองเครดิต และคอร์สตั้งเป้าว่า "prompt without burning credits" [A10.L01 t=00:54]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- ชื่อจริงของ skill "seedance-prompt-structure" และเนื้อหาหน้า skill (description, style prefix, asset registry @hero/@rival/@prop/@location/@scheme, prompt skeleton) เห็นได้เฉพาะบนจอ [A10.L01 frames t=00:35] [A10.L03 t=01:00]
- ขั้นตอน UI ของ Elements (แท็บ, Create element, ช่องชื่อ, Category "Auto") มีแค่ในวิดีโอ บทความไม่ได้พูดถึง Elements เลย [A10.L04 t=00:06–00:36]
- demo auto-attach: วาง prompt ของ Claude ใน Seedance แล้ว thumbnail ของ reference เติมเองโดยไม่ต้อง upload และใน prompt เห็นเป็น element chip [A10.L04 t=01:51–01:56]
- caption บนจอ: "STYLE, LIGHTING, CAMERA, ACTING, PHYSICS" และ "PRO TIP: ADD 'NO MUSIC AND ONLY ENVIRONMENTAL SFX'" [A10.L04 t=01:30–01:40]
- ข้อความเต็มของ brief และ director note ทุกตัวบนจอ (ฉาก 3, 4, 6, 7, 8, 9, 10, 12) ซึ่งบทความสรุปไว้แค่ใจความ [A10.L05 t=02:00] [A10.L07 t=01:30] [A10.L09 t=02:50]
- แผนที่ location ที่สร้างขึ้นมีป้าย "LOCATION MAP", legend และพารามิเตอร์ (ถนนยาว 120 m กว้าง 24 m, portal ห่างกัน 120 m, ห่างอาคาร 15 m, portal ~3 m) [A10.L06 t=03:55–04:05]
- การ์ด "BEFORE / AFTER" ของการแก้ตำแหน่งประตูและการล้ม [A10.L06 t=05:00–05:05] [A10.L07 t=01:05]
- ตัวเลือกมุก 4 แบบของ Claude: "The Phantom Crowd", "The Confetti Misfire", "The Flex Malfunction", "The Held Pose" (เลือกอันสุดท้าย) [A10.L09 frames t=00:35]
- หน้าจอนาฬิกาขึ้น "TOP UP" บนจอ ส่วนบทความแค่ยกคำพูดมา [A10.L07 t=01:50]
- หนังโฆษณาฉบับเต็มเล่นในวิดีโอทั้ง L01 และ L10 ส่วนบทความบอกแค่ "watch the commercial" [A10.L01 t=01:00–02:40] [A10.L10 t=00:04–01:47]
- skill ให้ template ต่างกันในแต่ละฉาก: [VISUAL]/[AUDIO] ในฉาก 1, header มีป้าย + SHOT list ในฉาก 2–11, timeline เทคนิคแบบกฎในฉาก 9 โดยไม่มีคำอธิบาย [A10.L04 cue cue-scene-1] [A10.L04 cue cue-scene-2] [A10.L08 cue cue-scene-9]
- ลำดับแนบไฟล์ใน chat: script PDF, character sheet, location, can sheet, robot sheets (#7, #9) [A10.L03 t=01:15–01:55]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- บทความและ audio ของ L08 พูดว่า "slight tackle" แต่ cue เขียน "SLIDING TACKLE" และคำขอบนจออ่านได้ "add a slide tackle" แปลว่าบทความน่าจะรับคำที่ได้ยินผิดมา [A10.L08 cue cue-scene-10] [A10.L08 frames t=01:59]
- pack shot note ขอให้แสง "match it to the scene 1" (6500K) แต่ cue สุดท้ายตั้ง WB 6000K และฉาก 8 part 1 ใช้ 5600K dawn ซึ่งคอร์สไม่ได้อธิบาย [A10.L09 cue cue-scene-12] [A10.L07 cue cue-scene-8-part-1]
- หน้า Character: ผู้สอนพูดว่าตั้งชื่อ "Adil" แต่ช่องชื่อใน hires อ่านได้ "Digital Creator in Shadows" และ ring จำนวนรูปขึ้นป้าย "Bad" ทั้งที่ upload 20 รูป [A10.L02 frames t=01:15]
- ไม่ชัดว่าการสร้าง Soul character ใช้ "Soul 2.0" (ตามที่ dropdown อ่านได้) หรือ Soul Cinema [A10.L02 frames t=01:15]
- แถบ character sheet ใน hires ที่ 01:39 เป็น 1:1 / 1.5k / enhancer Off ก่อนที่ผู้สอนจะพูดถึง setting 16:9 / 2K / on / 40 รูป จึงไม่เห็นสถานะสุดท้ายบนจอ [A10.L02 frames t=01:39] [A10.L02 t=01:42–01:56]
- สถานะสุดท้ายของ test 5 s / 1 generation ไม่อยู่ใน hires (เห็นแค่ 15s 2/4 ก่อนเปลี่ยน) [A10.L02 frames t=04:13] [A10.L02 frames t=04:15]
- เครดิตต่อ generation ของ Seedance 15 s 1080p ไม่มีการพูด ที่อ่านได้มีแค่ตัวเลขบนปุ่มตอนก่อนเปลี่ยน setting [A10.L02 frames t=04:13]
- ไม่มีไฟล์ skill ในวัสดุคอร์ส จึงไม่รู้กฎเต็มของมันและเหตุผลที่ใช้ template ต่างกันในแต่ละฉาก [A10.L10 t=02:23–02:29] [A10.L04 cue cue-scene-2]
- ผลของประตูที่สร้างใน L02 ไม่มีบนจอ (วิดีโอตัดตอนกด Generate) และเพิ่งเห็นผลตอนเปิด L03 [A10.L02 frames t=07:55] [A10.L03 t=00:00]
- ไม่ได้แสดงโปรแกรมตัดต่อและวิธีใส่ score/เพลง [A10.L04 frames t=06:10] [A10.L10 t=00:00]
- "I'm out." (L07 07:13, L10 01:23) เป็น transcript ความเชื่อมั่นต่ำ ไม่ยืนยันว่าเป็นบทพูดจริงในโฆษณา [A10.L07 t=07:13] [A10.L10 t=01:23]
- "Oh, my God" 22 ครั้งใน L01 เป็น whisper hallucination บนเพลงโฆษณา (compression ratio 9.4) ไม่ใช่บทพูด [A10.L01 t=01:54]
- ไม่ชัดว่า cold open ของ L01 (สนามหญ้า, โซฟา) เป็นส่วนของโฆษณาหรือของ intro เพราะ L10 ไม่มีฉากนี้ [A10.L10 frames t=00:04] [A10.L01 t=00:00–00:10]
- จำนวน generation ทั้งหมดไม่ได้บอก มีแค่ "a hundred tries" (srt: "best 3 seconds of 100 tries") [A10.L10 t=02:14–02:22]
- ข้อความ brief ฉาก 1 และฉาก 9 ฉบับเต็มบนจอยังอ่านไม่ครบ เพราะเห็นแค่ตอนกำลังพิมพ์ [A10.L04 frames t=01:16] [A10.L08 frames t=00:42]

### เทียบกับ v1
- เพิ่ม: ชื่อ skill "seedance-prompt-structure", โครง prompt skeleton และ style prefix ฉบับที่อ่านได้จากจอ [A10.L01 frames t=00:35]
- เพิ่ม: การลงทะเบียน Elements โดยตั้งชื่อตรงกับ @handle ใน Claude เพื่อให้ auto-attach ทำงาน [A10.L04 t=00:06–00:43]
- เพิ่ม: ตัวเลข batch/เครดิตที่เห็น (40 รูป = 5 credits, Soul Cinema ✦0.5, GPT Image 2 ✦7/12/4, Seedance 15s 2/4 = 270) [A10.L02 t=01:42–02:00] [A10.L02 frames t=04:13] [A10.L06 frames t=03:03]
- เพิ่ม: สูตร location scheme ครบขั้นตอนพร้อม prompt จริงและการประกาศ @scheme [A10.L06 cue cue-location-scheme] [A10.L06 t=04:30]
- เพิ่ม: ข้อความ director note ฉบับเต็มและรูปแบบเน้นด้วยตัวพิมพ์ใหญ่ [A10.L07 t=03:50] [A10.L07 t=05:55]
- แก้: v1 A10.01 บอกให้ "แยก fantasy ออกจากคุณสมบัติจริง" ไม่มีอยู่ใน notes ของคอร์ส สิ่งที่คอร์สเน้นคือหา twist ส่วนตัวให้คอนเซปต์ [A10.L01 t=02:45]
- แก้: v1 A10.03 บอกให้ "ตรวจว่าผู้ช่วยไม่ได้ใส่ asset ที่ไม่มีจริง" ไม่มีใน notes สิ่งที่คอร์สสอนคือการประกาศ registry "@handle — description" ให้ครบทุก asset [A10.L03 t=01:18–01:52]
- แก้: v1 A10.10 พูดถึง "keeper ledger" ซึ่งคอร์สไม่ได้พูด pro tip ใน recap คือ maps, ใช้ asset ของตัวเองเป็น reference และรันหลาย batch [A10.L10 t=02:03–02:13]
- แก้: v1 A10.04 บอกว่า "มือจับกระป๋องและ macro ต้องมี contact" แต่ใน notes จุดเสียของฉาก 2 คือรอยยิ้ม, การวิ่งถอยหลัง, ตาเปลี่ยนสี, transformation ที่นิ่ง [A10.L04 t=03:53–04:20]
- เหมือนเดิม: ล็อก asset และทดสอบก่อนทำฉากเต็ม [A10.L02 t=03:30–04:34]
- เหมือนเดิม: style header ร่วม และแยก SFX ออกจาก score [A10.L04 t=01:26–01:46]
- เหมือนเดิม: map top-down ใช้ทำหน้าที่ geometry ไม่ใช่ keyframe (คอร์ส: "use goal shields as a reference not a keyframe") [A10.L06 t=04:16–04:33]
- เหมือนเดิม: reuse การเลี้ยงบอลที่ยังไม่ได้ใช้ และสร้าง tackle ใหม่เฉพาะส่วนที่ขาด [A10.L08 t=01:02–02:05]

## A11 Automate a Faceless Niche Channel

### ภาพรวมและผลลัพธ์
- ช่อง explainer แบบ faceless ยาว ~10 นาทีได้ยอดวิวเป็นล้านเพราะมีระบบที่ทำซ้ำได้ ระบบเดิมต้องใช้ทีมทำ script + voice + edit + thumbnail ราว "5 DAYS" ต่อตอน [A11.L01 t=00:00–00:15] [A11.L01 article]
- ผู้สอนคือ Adil (@ADILINTHEWILD) มี silver play button และผู้ติดตามเกือบ 300,000 คน ตั้งคำถามว่า prompt เดียวใน Claude chat เดียวจะรันระบบทั้งหมดได้ไหม [A11.L01 t=00:20] [A11.L01 article]
- สิ่งที่คอร์สสัญญา: วิดีโอ 10 นาทีจากประโยคเดียว, narration ด้วยเสียงตัวเองที่ clone, แปลภาษาที่สอง, thumbnail ในไม่กี่นาที, shorts 20 คลิปในคลิกเดียว [A11.L01 t=00:56–01:07] [A11.L01 article]
- ตัวอย่างหัวข้อตลอดคอร์สคือ "How the Great Pyramid was really built" ในสไตล์ภาพ miniature/diorama [A11.L04 frames t=00:00] [A11.L05 t=00:15–00:45]
- การแบ่งงาน: Claude = คิด (topic, script) ส่วน Higgsfield = ผลิต (video, thumbnails, shorts) และงานที่คนต้องทำเองเหลือแค่เลือก output กับ upload [A11.L11 article]
- ผู้สอนบอกว่า workflow นี้จะช่วยประหยัดเวลาเขาได้ "hundreds of hours" (ไม่มีในบทความ) [A11.L01 t=00:47–00:52]

### Workflow ทีละขั้น
1. Connect: copy ลิงก์ MCP จาก higgsfield.ai แล้วใน Claude ไปที่ Settings → Connectors → Add → ตั้งชื่อ → วางลิงก์ → Connect [A11.L02 t=00:00–00:11] [A11.L02 article]
2. ติดตั้ง skill ของผู้สอน "the exact same way" (ใน UI อยู่กลุ่ม Customize: Skills / Connectors / Plugins) ลิงก์อยู่ใน description [A11.L02 t=00:11–00:20] [A11.L02 t=00:05]
3. หาหัวข้อ: ถาม "What's actually working in explainer videos right now?" แล้ว skill จะศึกษา reference format → research เว็บสด → ให้คะแนน → เลือก 1 หัวข้อ [A11.L03 cue prompt-001] [A11.L03 t=00:30–00:40]
4. Script: skill โพสต์แผน (angle / hook / structure) ก่อน แล้วค่อยเขียน narration script ยาว 10 นาที ~1,450 คำ [A11.L04 frames t=00:03] [A11.L04 frames t=00:40]
5. ความยาว: ถาม "how long should the video be?" แล้ว skill แนะนำ 10 นาที [A11.L05 t=00:00–00:12] [A11.L05 frames t=00:04]
6. Generate: Higgsfield สร้างหนังทั้งเรื่อง (visuals, narration, edit) จาก prompt เดียว แล้วผลกลับมาเป็น card "Higgsfield AI" ใน chat ที่มีปุ่ม Download / Recreate [A11.L04 t=01:16–01:26] [A11.L06 frames t=00:10]
7. แปลภาษา: ส่ง "Translate the video into Spanish." แล้ววิดีโอทั้งเรื่องจะ re-render เป็นภาษานั้น [A11.L06 cue prompt-002] [A11.L06 article]
8. เสียง: higgsfield.ai → Audio → Voice Presets → Create a custom voice → อัดเสียงอ่าน sample script → upload (.mp3) → จะเป็น preset ไว้ใช้ต่อ [A11.L07 t=00:00–00:27] [A11.L07 article]
9. Package: ส่ง "Give me titles and thumbnails for this video" (บนจอพิมพ์ "Create 3 titles and 3 thumbnails...") แล้วเลือกผ่าน Q/A widget [A11.L08 cue prompt-003] [A11.L08 t=00:10] [A11.L08 frames t=00:40]
10. Shorts: ส่ง "Create shorts from this video with Shorts Studio." จะได้ shorts ~20 คลิป ตัดและใส่ caption แล้ว [A11.L09 cue prompt-004] [A11.L09 t=00:08–00:16]
11. เผยแพร่ shorts ชุดเดียวกันลง YouTube Shorts, Reels, TikTok วันละคลิป [A11.L09 t=00:57–01:20] [A11.L09 frames t=00:10]
12. วางแผน: ส่ง "Plan my first 30 days: eight long videos, topics ranked by search volume." จะได้แผนที่มีวันที่และติดตามสถานะ [A11.L10 cue prompt-005] [A11.L10 frames t=00:20]
13. ขยายงาน: ส่ง "Start videos two and three from the plan." แล้วทั้งสองรันขนานกัน: research → scripts → "the gate" [A11.L10 cue prompt-006] [A11.L10 frames t=00:33]
14. Operate: ลงวิดีโอยาว 2 ตัว/สัปดาห์ (Tue + Fri) + short ทุกวันในเวลาเดิม แล้วดู average view duration โดยใช้จุดที่คนดูหลุดเป็น note ของ script ถัดไป [A11.L10 t=00:41–01:06] [A11.L10 t=00:20]

### กฎที่ใช้ซ้ำได้
- รันทุกขั้นใน Claude chat เดียว ทุกคำสั่งจะอ้างถึง "this video" ได้เอง prompt จึงสั้นแค่บรรทัดเดียว [A11.L01 t=00:52–01:07] [A11.L06 cue prompt-002] [A11.L08 cue prompt-003]
- ให้ skill เลือกหัวข้อจาก research สดและการให้คะแนน แทนการ brainstorm เอง [A11.L03 t=00:00–00:40] [A11.L03 article]
- คาดหวังคำตอบสั้นและเด็ดขาด: "no long answers and no 20 options" [A11.L03 t=00:12–00:20] [A11.L03 article]
- เลือก niche ที่ RPM สูง ซึ่ง education อยู่บนสุด (กราฟิกเรียง EDUCATION > TRAVEL > ENTERTAINMENT) [A11.L03 t=00:20–00:29] [A11.L03 t=00:25]
- ตรวจหัวข้อกับหลักฐาน (หัวข้อคล้ายกันเคย "super viral") และใช้ vidIQ ประเมินเพดาน $1,000–$10,000/เดือนจาก AdSense อย่างเดียว บวก brand deals [A11.L03 t=00:40–00:56] [A11.L03 article]
- ทำ niche เดียว เพราะการผสม niche "resets it to zero" ในเรื่อง audience targeting [A11.L03 t=00:56–01:08] [A11.L03 article]
- มี 2 layer: prompt คุมภาพ ส่วน script คุมความหมาย ถ้าไม่มี script จริงจะได้ "beautiful nonsense" [A11.L04 t=00:03–00:11] [A11.L04 article]
- YouTube ไม่ได้ demonetize AI อัตโนมัติ แต่ flag spam/unoriginal ไม่ว่าจะเป็น AI หรือไม่ script ที่เขียนดีจึงเป็นสิ่งที่รักษาการสร้างรายได้ [A11.L04 t=00:16–00:29] [A11.L04 article]
- ใช้ model ที่เขียนเก่งที่สุดสำหรับ script และ prompt ซึ่งในการทดสอบของผู้สอนคือ Fable 5 (ไม่มีตัวเลข) [A11.L04 t=00:30–00:41] [A11.L04 article]
- โครง script สำหรับ retention: hook เปิดด้วย payoff ไม่ใช่ backstory, แต่ละ chapter ปูไปบทถัดไป, ใส่ open loop ราวทุกนาที [A11.L04 t=00:41–01:01] [A11.L04 article]
- ใช้มุมที่สดเพื่อความ original เช่นเปลี่ยน "mystery of the pyramids" เป็น "jobsite story" [A11.L04 frames t=00:03]
- ตั้งเป้า ~10 นาทีเพื่อ watch time แต่ "as long as it stays interesting" [A11.L05 t=00:03–00:12] [A11.L05 article]
- เปลี่ยนภาพทุกไม่กี่วินาทีเหมือนช่องใหญ่ และตัดสินผลที่ความ coherent (narrator เดียว style เดียว ไอเดียเดียว) ไม่ใช่ความสวยของคลิปเดี่ยว [A11.L05 t=00:32–01:03] [A11.L05 article]
- เปลี่ยนตัวแปรเดียวเมื่อ localize: ใช้หนังเดิมแล้วเปลี่ยนแค่ภาษา [A11.L06 t=00:00–00:26] [A11.L06 article]
- clone เสียงตัวเองเพื่อให้มีเสียงที่ไม่มีช่องไหนมี และเป็นสัญญาณว่ามาจากคนจริง ทำให้ถูก flag น้อยลง [A11.L07 t=00:27–00:39] [A11.L07 article]
- packaging กฎข้อ 1: focal point เดียวที่อ่านได้ในขนาดหน้าจอมือถือ [A11.L08 t=00:25–00:31] [A11.L08 article]
- packaging กฎข้อ 2: title เปิดคำถามที่ thumbnail ตั้งใจไม่ตอบ ช่องว่างนั้นคือสิ่งที่ทำให้คนคลิก [A11.L08 t=00:31–00:38] [A11.L08 article]
- shorts คือการค้นพบที่ไม่ต้องผูกมัด เพราะวิดีโอยาวบังคับให้คนตัดสินใจ "worth 10 minutes?" ซึ่งทำให้เสียคนดู [A11.L09 t=00:20–00:37] [A11.L09 article]
- สูตร watch hours: ชั่วโมงที่ต้องการ ÷ average view = ยอดวิวรวมทั้งช่อง (4,000 h ที่ 4 นาที ≈ 60,000 views) [A11.L09 t=00:39–00:56] [A11.L09 article]
- วางแผนทั้งเดือนตาม search volume, รันวิดีโอขนานกัน, ลงตามตารางที่ทำได้จริง และปิด loop ด้วย average view duration [A11.L10 t=00:02–01:06] [A11.L10 article]

### โครงสร้าง Prompt
- prompt-001 (หาหัวข้อ): คำถามเปิดคำถามเดียวที่ไม่มีช่องเติม "What's actually working in <format> right now?" โดย <format> = "explainer videos" [A11.L03 cue prompt-001]
- คำขอความยาว: "how long should the video be?" [A11.L05 t=00:00]
- prompt-002 (แปล): "Translate the video into <language>." มีช่องเดียวคือภาษา และอ้างถึงวิดีโอล่าสุดใน chat เอง [A11.L06 cue prompt-002]
- prompt-003 (packaging): "Give me titles and thumbnails for this video." และบนจอเป็นแบบระบุจำนวน "Create 3 titles and 3 thumbnails for th[is ...]" [A11.L08 cue prompt-003] [A11.L08 t=00:10]
- ข้อความเลือก packaging เป็น Q/A: "Q: Which title? A: No Wheels, No Cranes / Q: Which thumbnail? A: Thumbnail 1 (NO SLAVES?)" [A11.L08 t=00:40]
- prompt-004 (shorts): "Create shorts from this video with <tool>." โดย <tool> = Shorts Studio และบนจอพิมพ์ว่า "Create shorts from the video using Higgsfield Shorts Studio" [A11.L09 cue prompt-004] [A11.L09 frames t=00:07]
- prompt-005 (แผนเดือน): "Plan my first <N days>: <count> long videos, topics ranked by <metric>." [A11.L10 cue prompt-005]
- prompt-006 (รันแผน): "Start videos <i> and <j> from the plan." และ Claude บอกทางลัดเองว่า "Say "start video 2" and I'll run the full pipeline" [A11.L10 cue prompt-006] [A11.L10 frames t=00:23]
- แผนก่อนเขียน script ที่ skill แสดง: Research is in → **The angle.** → **The hook.** ("Payoff first, backstory later") → **The structure.** (ลำดับเหตุการณ์ของโปรเจกต์ก่อสร้าง "Each chapter hands off to the next question") → "Writing it now" [A11.L04 frames t=00:03]
- รูปแบบ script ที่ได้: หัว "10-minute narration script · ~1,450 words" → "Cold Open — A Mountain on a Deadline" → "Chapter 1 — The Customer" → "Chapter 2 — The Workers" ... [A11.L04 frames t=00:40]
- ตัวเริ่มต้นตาม outro: "one sentence about a topic you'd binge at 2am" ไม่มีข้อความตายตัวนอกจาก cue ของ L03–L10 [A11.L11 t=00:00–00:10]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Claude model: Fable 5 (ผู้สอนพูดเอง) และตัวเลือก model บนจออ่านได้ "Fable 5 High" ใน L03–L10 [A11.L04 t=00:30–00:35] [A11.L03 frames t=00:07] [A11.L10 frames t=00:07]
- ในหน้า home ของ Claude ใน L02 ตัวเลือก model อ่านได้ "Sonnet 5 Medium" [A11.L02 frames t=00:02]
- dialog "Add custom connector" (BETA): Name, "Remote MCP server URL", Advanced settings ที่มี OAuth Client ID/Secret (optional) ซึ่งปล่อยว่างไว้ [A11.L02 t=00:05] [A11.L02 frames t=00:08]
- หน้า Higgsfield มีหัวข้อ "HIGGSFIELD MCP FOR ANY AI" [A11.L02 frames t=00:01]
- card ผลลัพธ์ใน Claude: "Higgsfield AI" (tool "job_display"), chips Upscale / video / Audio, ปุ่ม Download, "Predict Virality" (Free), Recreate และ player แสดง "0:00 / 10:35" [A11.L06 frames t=00:10]
- คำตอบเรื่องความยาวของ Claude: ~1,450 คำที่ ~150 wpm ≈ 10:00 "which renders as 60 clips of 10 seconds each" และผ่านเกณฑ์ 8 นาทีที่ YouTube เปิด mid-roll [A11.L05 frames t=00:04]
- Shorts Studio: "Warm Glow" preset, vertical 9:16, ~180 credits "on the ledger" [A11.L09 frames t=00:10] [A11.L10 frames t=00:03]
- Audio → Voice Presets: panel "SELECT OR ADD A VOICE" มีปุ่ม Create custom voice และ preset TALLULAH, ROMAN, MABEL, STERLING, QUINN, LEO, GIA, JULIAN [A11.L07 frames t=00:17]
- แถบ audio generator: mode Voiceover / Change Voice / Translate, chips "Seed Audio 1.0", "24000 Hz", "1.0", "1.0", "0", "MP3" (ความหมายของ 1.0/0 ไม่มีป้าย) [A11.L07 frames t=00:15]
- dialog "Add Voice": Name + ไฟล์เสียง (ตัวอย่าง "Adil's_voice.mp3") + block "Sample script" [A11.L07 t=00:20] [A11.L07 frames t=00:18]
- หน้า home ของ Higgsfield แสดงผลิตภัณฑ์ "HIGGSFIELD EXPLAINER" ("Any topic to a captioned explainer video, up to 10 minutes") และ "HIGGSFIELD SHORTS STUDIO" [A11.L07 frames t=00:13]
- tile อื่นที่เห็นแต่ไม่ได้ใช้: SUPERCOMPUTER ("Powered by Fable 5.0"), Nano Banana Pro, Seedance 2.0, Nano Banana 2 Lite, MCP & CLI, Gemini Omni Flash, Cinema Studio 3.5, App Builder [A11.L07 frames t=00:13]
- Live web search ใน Claude: เห็นผลจาก youtube.com, pbs.org, openculture.com, outlierkit.com, nexlev.io ฯลฯ [A11.L03 frames t=00:30]
- vidIQ ใช้เป็นแหล่งประเมินรายได้ และ YouTube Studio ใช้ดู AVD (ตัวอย่างค่า 2:31) [A11.L03 t=00:45–00:51] [A11.L10 t=01:00]
- เกณฑ์สร้างรายได้: 1,000 subscribers + 4,000 watch hours [A11.L09 t=00:39–00:44] [A11.L09 article]

### คำเตือนและ failure modes
- การผสม niche จะรีเซ็ต targeting ของ algorithm เป็นศูนย์ [A11.L03 t=01:04–01:08] [A11.L03 article]
- ถ้าไม่มี script วิดีโอ AI จะกลายเป็น "beautiful nonsense" [A11.L04 t=00:05–00:11] [A11.L04 article]
- YouTube flag spam หรือ content ที่ไม่ original ไม่ว่าจะเป็น AI หรือไม่ [A11.L04 t=00:19–00:24] [A11.L04 article]
- model ที่เขียนอ่อนกว่าให้ script อ่อนกว่าและยอดวิวน้อยกว่า (จากการทดสอบของผู้สอน ไม่มีตัวเลข) [A11.L04 t=00:30–00:41] [A11.L04 article]
- วิดีโอยาวช่วยได้เฉพาะ "as long as it stays interesting" [A11.L05 t=00:08–00:12] [A11.L05 article]
- ความต่อเนื่องระหว่างคลิปคือปัญหาหลัก เพราะคลิป AI ส่วนใหญ่ "just don't look coherent together" [A11.L05 t=00:50–01:03] [A11.L05 article]
- ถ้าจะเปลี่ยนความยาว (6 หรือ 8 นาที) ต้อง re-grid script ก่อน render [A11.L05 frames t=00:04]
- กราฟิกบอกเป็นนัยว่าสิ่งที่ถูก flag คือ script แบบ template + narration AI ทั่วไป: "TEMPLATED → ORIGINAL SCRIPT / GENERIC AI NARRATION → YOUR OWN VOICE" [A11.L07 t=00:30] [A11.L07 t=00:33–00:39]
- วิดีโอที่ดีแต่ packaging ไม่ดีก็ "goes nowhere" และ thumbnail ที่อ่านไม่ออกบนมือถือจะไม่ work ใน feed [A11.L08 t=00:00–00:31] [A11.L08 article]
- วิดีโอยาวเสียคนดูที่ลังเลตรงจังหวะ "is this worth 10 minutes?" แม้ตัววิดีโอจะดี [A11.L09 t=00:25–00:31] [A11.L09 article]
- ข้อความบนจอ "the 119-second cut was the fix" บอกเป็นนัยว่า shorts รอบแรกล้มเหลวแล้ว skill ลองใหม่ ซึ่งผู้สอนไม่ได้พูดถึง [A11.L09 frames t=00:10]
- ตารางที่ไม่สม่ำเสมอไม่ฝึกทั้งคนดูและระบบแนะนำ [A11.L10 t=00:45–00:55] [A11.L10 article]
- Claude research table ระบุว่า YouTube เปลี่ยนชื่อกฎ reused-content เป็น "inauthentic content" เพื่อจัดการวิดีโอ template ที่ไม่มีความต่าง (ข้อความบนจอจาก Claude ไม่ใช่คำพูดผู้สอน) [A11.L03 frames t=00:15]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- ตารางคำตอบของ Claude: Niche | RPM/CPM | Why it works right now (Education $8–20, AI/tech $15–35; Travel $4–14; Beauty & fashion $4–12; Entertainment $2–8) [A11.L03 frames t=00:15]
- หัวข้อที่เลือกคือพีระมิด เห็นจากผล research และ thumbnail "THE PYRAMIDS" 1.8M/3.8M/3.6M views ซึ่งบทความไม่ได้บอกชื่อหัวข้อ [A11.L03 t=00:30–00:40] [A11.L04 frames t=00:00]
- การ์ด vidIQ: ช่องตัวอย่าง 5,748,481 views ประเมิน $1.6K/เดือน (4.49K subscribers, 57 videos) และอีกช่อง 63,481,387 views ประเมิน $6.3K [A11.L03 frames t=00:48] [A11.L03 t=00:45–00:50]
- กราฟิกทดลอง niche: "ONE NICHE → 154 → 348 SUBSCRIBERS / SWITCHING NICHES → 11 → 26" ไม่มีแหล่งที่มา [A11.L03 t=01:00–01:05]
- ข้อความแผนของ skill (angle "jobsite story", hook "six million tons, no wheels, no iron, no cranes") และข้อความ cold open เต็ม [A11.L04 frames t=00:03] [A11.L04 frames t=00:40]
- เหตุผล 10 นาทีของ skill: เกณฑ์ mid-roll 8 นาที, สัญญาณ "real documentary", และการคำนวณคำ/clip grid ซึ่งบทความบอกแค่ "watch time" [A11.L05 frames t=00:04]
- สไตล์ภาพของหนัง: miniature/diorama โทนอุ่นมีสปอตไลต์ (plinth ทราย, ตาชั่งชั่งขนมปังกับหิน, หุ่นไม้) [A11.L05 t=00:15–00:45]
- กราฟิก "INTERNET USERS BY PRIMARY LANGUAGE": English 25.9% (~1.19 billion) เทียบภาษาอื่น 74.1% ไม่มีแหล่งที่มา [A11.L06 frames t=00:20]
- thumbnail จริง 3 แบบ: "GENIUS METHOD", "NO SLAVES?", "6 MILLION TONS" ข้อความ 1–3 คำ contrast สูง และ mockup feed บนมือถือที่ใช้ทดสอบกฎข้อ 1 [A11.L08 t=00:15] [A11.L08 frames t=00:28]
- Claude ส่งลิงก์ MP4 ตรงก่อน แล้วรอบถัดมา "imported the final MP4 straight from its link (no re-upload needed)" [A11.L09 frames t=00:03] [A11.L10 frames t=00:03]
- แผน 8 หัวข้อจริง (Jul 08–Aug 04) เช่น Roman concrete, Bronze Age Collapse, "The pyramid that bends", Pompeii, Library of Alexandria แต่ละแถวมีเหตุผลและแหล่ง [A11.L10 frames t=00:20]
- script วิดีโอ 2/3 ที่รันขนาน: "each 60 blocks, 6 chapters, 7 open loops, every fact traced to its research file" [A11.L10 frames t=00:33]
- ท้าย L10 มีลิงก์ไปการทดลอง "sell AI videos to businesses" และ outro บอกว่าวิดีโอทั้งหมดอยู่ใน description ให้ไปตัดสินเอง [A11.L10 t=01:06–01:16] [A11.L11 t=00:10–00:14]
- ช่องตัวอย่างตอนเปิด: "Historic" (1.25M), "pern" (5.07M), "Furzgesagt" (25.3M ซึ่งสะกดล้อ Kurzgesagt) [A11.L01 frames t=00:02]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- จำนวนฉาก: บทความและคำพูดบอก "a hundred scenes" แต่คำตอบของ Claude บนจอบอก "60 clips of 10 seconds" ซึ่งอาจเป็นคนละหน่วย [A11.L05 t=01:00–01:03] [A11.L05 frames t=00:04]
- เส้นทาง setup: บทความเขียน "Settings" แต่ใน UI รายการที่กดอยู่ใต้ "Customize" [A11.L02 t=00:00] [A11.L02 article]
- Shorts: คำพูดใน outro บอกว่า "ask for your 20 shorts right in the same chat" แต่บทความเขียน "drop it straight into Shorts Studio" และ Claude เองเคยบอกว่า MP4 คือ "the file to drop into the Shorts Studio uploader" ก่อนจะ import จากลิงก์ [A11.L11 t=00:00–00:10] [A11.L11 article] [A11.L09 frames t=00:03]
- skill ไม่ได้บอกชื่อและที่อยู่ และลิงก์ MCP กับ skill อยู่แค่ "in the description" ไม่เคยแสดงให้อ่านได้ (ในคำพูดเรียกว่า "The explainer") [A11.L02 t=00:19–00:20] [A11.L06 t=00:20]
- ไม่ได้บอกชื่อ model ของ Higgsfield ที่ใช้ทำวิดีโอ 10 นาที, thumbnail และ narration [A11.L05 article] [A11.L08 t=00:10]
- ต้นทุนเครดิตของการ render เต็ม 10 นาทีไม่ปรากฏ เห็นแค่ shorts batch ~180 credits [A11.L09 frames t=00:10]
- ไม่ได้บอกว่าเวอร์ชันสเปนใช้เสียง clone หรือเสียง stock และ narration ในคลิปท้าย L07 ใช้เสียง clone หรือเปล่าก็เป็นแค่การอนุมานจากตำแหน่ง [A11.L06 frames t=00:10] [A11.L07 t=00:39–00:48]
- ไม่ได้บอกว่า "the gate" ใน pipeline ขนานตรวจอะไร [A11.L10 frames t=00:33]
- สาเหตุของ "the 119-second cut was the fix" ไม่มีคำอธิบาย [A11.L09 frames t=00:10]
- ไม่ชัดว่าผู้ใช้พิมพ์หัวข้อ "How the Great Pyramid was really built" เองหรือเป็นตัวเลือกที่ skill เสนอ [A11.L04 frames t=00:00]
- กฎ "one niche" กับการลงเวอร์ชันแปลภาษาในช่องเดียวกันไม่ได้อธิบายว่าเข้ากันอย่างไร [A11.L03 t=00:56–01:08] [A11.L06 article]
- ตัวเลขการทดลอง niche (154/348 กับ 11/26) และสถิติภาษา 25.9%/74.1% ไม่มีแหล่งอ้างอิง [A11.L03 t=01:00–01:05] [A11.L06 frames t=00:20]
- ชื่อ "Seed Audio 1.0" บนแถบ audio มีความเชื่อมั่นต่ำ และ sample script ย่อหน้าที่สองอ่านได้ไม่ครบ [A11.L07 frames t=00:15] [A11.L07 frames t=00:18]
- ตัวเลือก model ของ Claude ต่างกันระหว่างบท (L02 "Sonnet 5 Medium", L03–L10 "Fable 5 High") ซึ่งคอร์สไม่ได้อธิบาย [A11.L02 frames t=00:02] [A11.L03 frames t=00:07]

### เทียบกับ v1
- เพิ่ม: prompt จริงทั้ง 6 ตัว (prompt-001 ถึง prompt-006) และรูปแบบ Q/A ตอนเลือก packaging [A11.L03 cue prompt-001] [A11.L10 cue prompt-006] [A11.L08 t=00:40]
- เพิ่ม: ขั้นตอน connector ใน Claude (Add custom connector, Remote MCP server URL, OAuth optional) [A11.L02 t=00:05]
- เพิ่ม: เหตุผลเรื่องความยาว 10 นาที (เกณฑ์ mid-roll 8 นาที, 150 wpm, 60 × 10 s) [A11.L05 frames t=00:04]
- เพิ่ม: setting ของ Shorts Studio (Warm Glow, 9:16, ~180 credits) และคำแนะนำให้ลงวันละคลิป [A11.L09 frames t=00:10]
- เพิ่ม: สูตร watch hours (4,000 h ÷ 4 นาที ≈ 60k views) และ cadence Tue + Fri [A11.L09 t=00:39–00:56] [A11.L10 t=00:20]
- เพิ่ม: เส้นทาง voice clone ใน UI และชื่อ preset voices [A11.L07 t=00:00–00:27] [A11.L07 frames t=00:17]
- แก้: v1 A11.06 บอกว่าเสียงภาษาใหม่ยาวไม่เท่าเดิมจึงต้องจัดภาพและ subtitle ใหม่เอง แต่ในคอร์ส prompt บรรทัดเดียว "re-renders the whole video" เป็นภาษาใหม่โดยไม่ต้องตัดต่อเอง (ส่วนเรื่องคุณภาพคำแปลไม่ได้ตรวจ) [A11.L06 t=00:00–00:26] [A11.L06 article]
- แก้: v1 A11.09 บอกให้ "เลือกประเด็นที่จบในตัว ... ไม่ตัดตามระยะเวลาอย่างเดียว" แต่คอร์สไม่ได้สอนวิธีเลือก clip เพราะ Shorts Studio ตัดและใส่ caption ให้เองจากคำขอเดียว [A11.L09 t=00:08–00:16]
- แก้: v1 A11.03 บอกว่า RPM/รายได้ "ไม่เป็นค่าคาดการณ์ของช่องใหม่" ซึ่งเป็นคำเตือนของ v1 เอง คอร์สนำเสนอตัวเลข vidIQ $1k–$10k/เดือนว่าเป็นเพดาน [A11.L03 t=00:45–00:56]
- เหมือนเดิม: แยก narration ออกจากคำสั่งภาพ, hook มี payoff, แต่ละช่วงมีเหตุให้ดูต่อ [A11.L04 t=00:03–01:01]
- เหมือนเดิม: thumbnail ต้องมี focal point เดียวที่อ่านได้บนมือถือ และมี information gap [A11.L08 t=00:25–00:38]
- เหมือนเดิม: คนยังต้องเลือก output และ upload เอง [A11.L11 article]

## A12 Build a Faceless Channel

### ภาพรวมและผลลัพธ์
- คอร์ส 7 บทนี้เป็นการทดลองสร้างช่อง faceless แบบ Bright Side ด้วย AI ภายในราว "20 minutes" โดยใช้ Claude Fable 5 + Higgsfield MCP [A12.L01 t=00:11] [A12.L01 t=00:34–00:40] [A12.L01 article]
- ผู้สอนแนะนำตัวว่า "Adil" (@ADILINTHEWILD) ส่วน metadata ของคอร์สระบุผู้เขียนเป็น Rus Syzdykov [A12.L01 t=00:16]
- ช่องต้นแบบคือ Bright Side ซึ่ง vidIQ ประเมินรายได้ $39.5K/เดือน [A12.L01 t=01:04] [A12.L01 article]
- ข้อโต้แย้งหลัก: YouTube demonetize ช่องที่ไม่มีคุณค่า ไม่ใช่ช่องที่ใช้ AI; ยอดวิวไม่ขึ้นกับจำนวน subscriber; รูปแบบ "educational experiment" แบบ evergreen คุ้มที่จะยืม [A12.L01 t=01:13–01:54] [A12.L01 article]
- workflow ทำงานด้วย prompt หลักไม่กี่ตัวใน Claude Code: script → วิดีโอเต็ม → upload package → ขยายเป็นหลายวิดีโอ [A12.L03 cue cue-script-prompt] [A12.L04 cue cue-video-prompt] [A12.L05 cue cue-packaging-prompt] [A12.L05 cue cue-scale-prompt]
- ผลที่ได้: สารคดี Pompeii/Vesuvius 5 นาทีแบบ photoreal มีตัวละครเด็กฝึกงานร้านขนมปังคนเดิมในหลายช็อต ตามด้วยวิดีโอ Venice และ "ocean mysteries" [A12.L04 t=01:25–02:20] [A12.L05 t=02:05]
- ผล 3 วันหลัง upload: 7.3K views, watch time 213.7 ชั่วโมง, +27 subscribers (Jun 15–17, 2026) [A12.L07 t=00:05]

### Workflow ทีละขั้น
1. หาช่อง faceless ที่พิสูจน์แล้ว และตรวจรายได้ด้วย vidIQ "Quick channel stats" (Bright Side: 44.6M subs, 11K videos, ประเมิน $39.5K/เดือน) ยืม format ไม่ใช่วิดีโอ [A12.L01 t=01:04] [A12.L01 t=01:56–02:03]
2. เลือก niche ตาม RPM (finance, tech, education) ซึ่งคอร์สเลือก education เพราะดึงคนได้กว้างและ retention ดี [A12.L03 t=00:14–00:37] [A12.L03 article]
3. Setup ครั้งเดียว: ค้น "Higgsfield AI" → สมัคร → เปิด "MCP & CLI" → copy URL ของ connector [A12.L02 t=00:03–00:12] [A12.L02 article]
4. ใน Claude: Settings → Connectors → "Add Custom Connector" → ตั้งชื่อ "Higgsfield" → วาง URL → Connect [A12.L02 t=00:12–00:27] [A12.L02 article]
5. อนุมัติหน้า consent ของ accounts.higgsfield.ai ("Verify your identity; Your email address" → Allow) [A12.L02 t=00:25]
6. สลับไป Claude Code สำหรับงานที่เหลือทั้งหมด [A12.L02 t=00:27–00:36] [A12.L02 article]
7. Script: ใส่ prompt "analyze the channel, scenarios, hooks, and write me a script for a similar video <URL /videos>" แล้ว Claude จะ fetch ช่อง เลือกหัวข้อเอง (Pompeii) และเขียน shot list 9 acts เก็บเป็น pompeii/SHOTLIST.md [A12.L03 cue cue-script-prompt] [A12.L03 t=01:35]
8. วิดีโอ: ใส่ prompt "make a 5 minutes video like on the reference account using Seedance 2.0. 1080p. It's going on a faceless Youtube channel" [A12.L04 cue cue-video-prompt] [A12.L04 t=00:35–00:40]
9. Claude โหลด Higgsfield tools ตรวจ workspace, เครดิต และ spec จริงของ Seedance 2.0 ก่อนจ่าย แล้ว render ทีละ batch (C1–C12, C13–C24, C25–C35) โดยทำ VO และ music bed ขนานกันไป [A12.L04 t=00:40] [A12.L04 frames t=01:05]
10. ประกอบด้วย ffmpeg: concat คลิป → overlay VO + music ที่ duck เหลือ 10% → export 1080p เก็บลงโฟลเดอร์ project (audio/, clips/, out/, package/, SCRIPT.md, SHOTLIST.md, MANIFEST.md) [A12.L04 t=01:05] [A12.L04 t=01:15–01:20]
11. Package: ใส่ prompt "Put together a complete YouTube video package for me: prepare the thumbnails, title, and everything else needed to upload it" จะได้ thumbnail 3 แบบ, title, description, tags, chapters, captions.srt, checklist ใน UPLOAD_PACKAGE.md [A12.L05 cue cue-packaging-prompt] [A12.L05 frames t=00:33]
12. ขยาย: ใส่ prompt "Make me 2 more videos. Pick topics that would perform well on YouTube for the same channel" [A12.L05 cue cue-scale-prompt] [A12.L05 t=00:55–01:00]
13. Upload ใน YouTube Studio ระหว่างที่วิดีโออื่น render: Create → Upload → วาง title/description → ใส่ thumbnail 3 แบบใน A/B Testing → ทำตาม checklist → schedule [A12.L05 t=01:20–01:53] [A12.L05 article]
14. ทางเลือกสำหรับการเติบโต: ให้ MCP วิเคราะห์ Shorts ที่ viral ที่สุดใน niche แล้วสร้าง Short ใหม่ [A12.L06 t=00:50–01:05] [A12.L06 t=00:55]
15. รอ ~3 วัน แล้วดู YouTube Studio Analytics (views, watch time, subscribers) [A12.L07 t=00:00–00:13] [A12.L07 article]

### กฎที่ใช้ซ้ำได้
- ยืม format ของช่องที่พิสูจน์แล้ว ห้ามยืมวิดีโอ เพราะการใช้เนื้อหาซ้ำทำให้โดน reused-content strike [A12.L01 t=01:56–02:03] [A12.L01 article]
- ตรวจเงินของช่องต้นแบบก่อนสร้าง (views gained 7 days, est. monthly earnings) [A12.L01 t=01:04] [A12.L01 article]
- ตัดสิน niche จากว่าเนื้อหามีคุณค่าน่าดูหรือไม่ ไม่ใช่จากว่า AI ทำหรือเปล่า [A12.L01 t=01:13–01:28] [A12.L01 article]
- เลือก format ที่เรียบง่ายและทำซ้ำได้: เล่าเรื่องตรงไปตรงมา + ภาพ cinematic + รูปแบบง่าย [A12.L01 t=01:29] [A12.L01 article]
- ไม่ต้องรอ subscriber เพราะ algorithm ดันเนื้อหาดีไปหาคนที่ไม่ได้ติดตาม [A12.L01 t=01:40–01:47] [A12.L01 article]
- เลือก niche RPM สูง (finance/tech/education) และ education ยังรักษา retention ได้ดี [A12.L03 t=00:14–00:37] [A12.L03 article]
- ให้ script เป็น shot list ที่เครื่องอ่านได้ (acts, timecode, clip ID, VO ทีละคลิป) เพื่อให้ prompt ตามเพียงตัวเดียวขับการสร้างวิดีโอได้ [A12.L03 t=01:35] [A12.L04 cue cue-video-prompt]
- script ต้อง hook ตั้งแต่วินาทีแรก (Act 1 = Hook) [A12.L03 t=01:35] [A12.L03 article]
- เปลี่ยนภาพทุก 5–10 s ดังนั้นวิดีโอ 5 นาทีต้องมีอย่างน้อย 30 คลิป [A12.L04 t=00:00–00:14] [A12.L04 article]
- ความยาวคลิป: 5 s สำหรับ beat ที่กระแทก, 10 s สำหรับ beat ที่น่าทึ่ง/เปิดเผย และรวมกันต้องเท่ากับเวลาเป้าหมายพอดี (300 s) [A12.L04 t=00:25]
- ใส่บริบทปลายทาง ("going on a faceless YouTube channel") ใน prompt ให้โมเดล [A12.L04 t=00:35–00:40]
- ก่อนใช้เครดิต ให้ตรวจ workspace, ยอดเงิน, spec ของโมเดล และสำรวจโฟลเดอร์ project ว่ามีงานเดิมอยู่หรือไม่ [A12.L04 t=00:40] [A12.L05 t=01:00]
- เปลี่ยนถ้อยคำช็อตที่เกี่ยวกับความตายในประวัติศาสตร์เป็น "cinematic silhouette, dramatic ash, no visible injury" เพื่อเลี่ยง content filter [A12.L04 t=00:25] [A12.L05 t=00:10]
- ใช้ narration ต่อเนื่องเส้นเดียว แล้วปรับวิดีโอให้เข้ากับ VO และ duck เพลงลงเหลือ ~10% [A12.L04 t=01:05] [A12.L05 frames t=00:15]
- ขอ thumbnail 3 แบบที่ต่างกันชัดให้ YouTube A/B test (3–4 คำ, accent สีเหลืองจุดเดียว) [A12.L05 t=00:37–00:42] [A12.L05 t=00:50]
- title ไม่เกิน ~60 ตัวอักษรเพื่อให้แสดงครบ [A12.L05 t=01:35]
- ตั้ง "Altered/synthetic content" = YES (YouTube บังคับสำหรับภาพ AI), Category Education, "Not made for kids", upload captions.srt [A12.L05 t=00:50]
- แต่ละหัวข้อได้ research, script และ visual style ของตัวเอง ไม่ใช่ template เดียว [A12.L05 t=01:00–01:10] [A12.L05 article]
- กฎกันโดน demonetize 3 ข้อ: เสียง AI ต้องเข้ากับเรื่อง, script original มี insight จริง, ภาพตัดต่อและจังหวะดี [A12.L06 t=00:27–00:39] [A12.L06 article]
- อยู่ในรูปแบบ educational เพราะ "always perform" และยอดวิวเปิดทางไป paid collaborations/brand deals [A12.L07 t=00:13–00:37] [A12.L07 article]

### โครงสร้าง Prompt
- cue-script-prompt: "Analyze the [channel] (scenarios, hooks) and write me a script for a similar video: <reference channel /videos URL>" ช่องเติมคือเป้าวิเคราะห์ ผลที่ต้องการ และ URL /videos ของช่องต้นแบบ [A12.L03 cue cue-script-prompt]
- ข้อความที่พิมพ์จริงบนจอ: "analyze the channel,scenarios, hooks, and write me a script for a similar video https://www.youtube.com/@BRIGHTSIDEOFFICIAL/videos" [A12.L03 t=01:15–01:25]
- หัว shot list ที่ Claude เขียน: "Clip breakdown — Seedance 2.0 (silent) + one continuous Inworld TTS (Carter en) 16:9 1080p | TOTAL 5:00 (300s) | 35 clips | scenes 5/8/10s | VO verbatim per clip" [A12.L03 frames t=01:37]
- รูปแบบต่อคลิป: "C1 — 10s | <คำบรรยายภาพ>" ตามด้วยบรรทัด VO ในเครื่องหมายคำพูด [A12.L03 t=01:35]
- โครง 9 acts ("dawn → midnight → dawn → discovery"): Hook 0:00–0:28 C1–C3 → Calm & signs → Explosion → Burying → The decision → Night & the flow → The end → Discovery → Twist & outro 4:24–5:00 C32–C35 [A12.L04 frames t=00:29] [A12.L04 frames t=00:34]
- cue-video-prompt: "make a <length> video like on the reference account using <video model>. <resolution>. It's going on a <destination>." ซึ่งต้องมี shot list ของ L03 อยู่ใน conversation เดียวกัน [A12.L04 cue cue-video-prompt]
- prompt ต่อคลิปที่ Claude เขียนเอง: "Aerial drone view of a green vineyard-covered mountain looming over a sunlit ancient Roman city of Pompeii at dawn, terracotta rooftops, golden morning light, cinematic, epic" [A12.L04 frames t=00:45]
- prompt คลิปที่ Claude เขียนเอง: "Close-up of hands lighting a brick wood-fired oven inside an ancient Roman stone bakery, warm orange firelight, dawn, cinematic" [A12.L04 frames t=00:47]
- cue-packaging-prompt: "Put together a complete YouTube video package for me: prepare the <thumbnails, title> and everything else needed to upload it." [A12.L05 cue cue-packaging-prompt]
- cue-scale-prompt: "Make me <N> more videos. Pick topics that would perform well on <platform> for the same channel" [A12.L05 cue cue-scale-prompt]
- prompt เพลงที่ Claude เขียนเอง (Venice): "Melancholic cinematic orchestral score, beautiful but haunting, slow strings and soft piano, a sense of loss and wonder, gently building, no vocals, atmospheric" [A12.L05 frames t=01:58]
- prompt Shorts บนจอ: "Analyze the most viral Shorts in my niche to identify which mechanics work and what performs best, then create a YouTube Short for me." [A12.L06 t=00:55]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Claude desktop app แท็บ Code: model "Fable 5 (1M context)", effort "High", permission "Auto" [A12.L03 frames t=01:09] [A12.L04 t=00:41]
- URL ของ connector ที่แสดงบนหน้า Higgsfield คือ "https://mcp.higgsfield.ai/mcp" [A12.L02 frames t=00:13]
- หน้า "HIGGSFIELD MCP FOR ANY AI" มีแท็บ MCP / CLI / Skill และเลือก client ได้ Claude / Cursor / OpenClaw / Hermes พร้อม banner "If you are using Claude Code, Codex, OpenClaw, Hermes, it's better to use the CLI" [A12.L02 frames t=00:13]
- dialog "Add custom connector (BETA)": name, "Remote MCP server URL", OAuth Client ID/Secret (optional ปล่อยว่าง) [A12.L02 t=00:20]
- Higgsfield MCP tools ที่โหลดผ่าน ToolSearch: generate_video, generate_audio, select_workspace, show_plans_and_credits [A12.L04 frames t=00:42]
- generate_video ของ Seedance 2.0: 16:9 กับความยาว 10s/8s และมี chip "Audio" [A12.L04 frames t=00:45] [A12.L05 frames t=02:02]
- ความละเอียด 1080p (ยืนยัน 1920×1080 บนจอ) [A12.L04 t=00:27] [A12.L04 t=01:05]
- TTS: "Inworld TTS", เสียง "Carter (en)" เป็น narration เส้นเดียว [A12.L05 frames t=01:59] [A12.L04 t=00:25]
- เพลง: generate_audio "Sonilo Text to Music", 240s สำหรับ Venice ส่วน Pompeii เป็น music bed 300s [A12.L05 frames t=01:58] [A12.L04 t=01:05]
- workspace: "YT Team, 7.24M credits — cost ~2,500 total" [A12.L04 frames t=01:05]
- การสร้างซ้ำทั้งหมดใช้ประมาณ 3,000 credits ตามที่ Claude ยอมรับเอง [A12.L05 t=00:50]
- generation ที่โดน NSFW flag ขึ้น "Credits refunded" [A12.L05 t=02:00]
- spec thumbnail ในแผน: 1280×720 JPG [A12.L04 t=00:25] [A12.L05 frames t=00:35]
- ไฟล์ผลลัพธ์: out/"Pompeii Volcano.mp4" 174.6 MB และใน package มี Pompeii_FINAL_1080p.mp4 (4:59, 1920×1080, H.264/AAC, ~202 MB) [A12.L04 frames t=01:22] [A12.L05 frames t=01:36]
- ตัวเลข RPM ตัวอย่างบนจอ (ไม่ได้บอกว่าเป็นช่องของใคร): est. revenue $5,363.83, RPM $31.69, CPM $73.59 (11–17 Jun 2026) และ AVD 2:32 / 64.0% [A12.L03 t=00:15] [A12.L03 t=00:30]
- top nav ของ Higgsfield: Explore, Image, Video, Audio, Supercomputer, MCP & CLI, Collab, Plugins, Marketing Studio, Cinema Studio, AI Influencer, Can… [A12.L02 frames t=00:10]

### คำเตือนและ failure modes
- ช่อง AI โดน demonetize เฉพาะเมื่อไม่มีคุณค่า และ YouTube block คนที่ใช้ AI ทำ spam คุณภาพต่ำ [A12.L01 t=01:15–01:20] [A12.L06 t=00:21–00:25]
- คลิปสุ่มที่เอามาต่อกันโดยไม่ตัดต่อผิดกฎ [A12.L06 t=00:34–00:39] [A12.L06 article]
- ถ้าทำเอง ต้อง generate 30+ ครั้งและแก้คลิปที่เสีย ใช้เวลาราวครึ่งวันก่อนจะถึงขั้น voiceover [A12.L04 t=00:08–00:26] [A12.L04 article]
- Seedance 1080p "takes a few minutes each" และ pipeline มี 35 render Claude จึงทำทีละ batch [A12.L04 t=01:05]
- Higgsfield ขึ้น NSFW false flag กับคลิปประวัติศาสตร์ Pompeii (C27 buried city, C28 ruins, C31 casts) ซึ่ง Claude เดาว่าคำว่า "victims" ทำให้โดน แล้ว resubmit ด้วยคำที่ปลอดภัยกว่า [A12.L05 t=00:10]
- VO ออกมายาวกว่าวิดีโอที่วางแผน: "VO narration is 5:11 (311s) — about 17s longer" และ Claude ยืดวิดีโอราว ~5% ให้ตรง [A12.L05 frames t=00:15]
- งานที่จ่ายเงินซ้ำ: Claude สร้างคลิปทั้ง 35 ตัว + narration ใหม่ (~3,000 credits) ก่อนพบว่ารอบก่อนหน้าในวันเดียวกันประกอบวิดีโอและ package เสร็จแล้ว ("I should have checked the package/ folder first.") [A12.L05 t=00:50]
- Claude เรียก content filter ว่า "your square-waves gotcha" ซึ่งเป็นบทเรียนที่จำมาจาก project ก่อน [A12.L04 t=00:25]
- เห็นผลลัพธ์แค่ราว 1 นาที วิดีโอเต็มอยู่ "via the link in the description" จึงตรวจคุณภาพทั้งเรื่องจากบทนี้ไม่ได้ [A12.L04 t=02:26–02:32]
- "You can hit those numbers really fast" เป็นคำพูดส่วนตัวของผู้สอนโดยไม่มีข้อมูลประกอบ [A12.L06 t=00:09–00:14]
- dialog ของ Claude มีข้อความบนจอว่า "only use connectors from developers you trust" แต่ผู้สอนไม่ได้พูดถึง [A12.L02 t=00:20]
- ผล Google มีโฆษณาหน้าตาคล้ายกัน (OpenArt "Higgsfield Alternative", KlingAI) ควรเลือกลิงก์ทางการ (อนุมานจากหน้าจอ ผู้สอนไม่ได้พูด) [A12.L02 t=00:05]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- การ์ด vidIQ ของ Bright Side: 44.6M subscribers, 11K videos, views gained (7 days) +2,832,277, Est. monthly earnings $39.5K [A12.L01 t=01:05]
- หน้า policy ของ YouTube "What we check when we review your channel" ที่ขีดเส้นใต้ "original and 'authentic'" (อ่านจากภาพขยาย ถ้อยคำโดยประมาณ) [A12.L01 t=01:25]
- หน้า consent ของ accounts.higgsfield.ai (Verify your identity / Your email address, Deny / Allow) ซึ่งบทความไม่มี [A12.L02 t=00:25]
- คำตอบของ Claude บนจอบอกว่า shot list "already exists in your project from a prior session" แปลว่าในการถ่ายจริง script มาจาก session ก่อนบวกกับ memory recall [A12.L03 t=01:35]
- เหตุผลที่ Claude เลือก Pompeii: format "you are there" survival + อันตรายที่ซ่อนอยู่ + fact จริงตอนจบ, นับถอยหลังเพื่อ retention, setup ภาพน้อยจึงถูก, ปิดท้ายด้วย "3 million people still live there" [A12.L03 t=01:35]
- ก่อน generate Claude ถามว่าจะเริ่ม 35 คลิปเลยหรือจะปรับ shot list ก่อน และ prompt ของ L04 คือคำตอบของคำถามนั้น [A12.L04 t=00:25–00:40]
- รายงานความคืบหน้าบนจอ (script ล็อก, workspace confirmed, batch, ffmpeg, thumbnail + upload package) และตัวบอก "1 running task" [A12.L04 frames t=01:05]
- overlay "100X CHEAPER" / "100X FASTER" ระหว่างที่ผู้สอนพูดว่าถูกกว่าเร็วกว่า 100 เท่า โดยไม่มีตัวเลขต้นทุน [A12.L04 frames t=03:13] [A12.L04 frames t=03:15]
- แผน thumbnail ของ Claude: A "YOU HAVE 18 HOURS TO ESCAPE", B "WHY DID THEY STAY?", C "THE LAST DAY OF POMPEII" [A12.L05 frames t=00:53]
- รายการ title 5 ตัวใน UPLOAD_PACKAGE.md และ chapters (0:00 A Normal Morning in Pompeii ... 4:52 Vesuvius Is Still Watching) [A12.L05 t=01:35] [A12.L05 frames t=00:53]
- ใน YouTube Studio ใช้ title "What Your Last Day in Pompeii Would Actually Look Like" (title B ไม่ใช่ A ที่แนะนำ) [A12.L05 t=01:45]
- การ์ด YPP บนจอเพิ่มเงื่อนไขทางเลือก "10M valid public Shorts views" (90 วัน) ซึ่งทั้งบทความและเสียงพูดไม่มี [A12.L06 frames t=00:07]
- ตัวเลขใน Studio: Views 7.3K, Watch time 213.7 h, Subscribers +27; Realtime 27 subs / 6.9K views ใน 48 ชม.; กราฟแบนวันที่ 15 แล้วพุ่งวันที่ 16–17 [A12.L07 t=00:05]
- ฟุตเทจ Venice: สถิติแบบ Bright Side (118 islands, 14,000 poles under the Rialto, 23 cm lost in the 20th century) [A12.L05 t=02:10–03:05]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- คอร์สบอกว่า script มาจาก "one prompt" แต่บนจอ Claude เรียก memory และบอกว่า shot list มีอยู่แล้วจาก session ก่อน จึงไม่รู้ว่า prompt สองตัวจะได้ผลอย่างไรในบัญชีใหม่ที่ไม่มี memory [A12.L03 t=01:35] [A12.L04 t=02:48–02:56]
- ผู้สอนพูดว่า "I didn't write a single correction" แต่บนจอ Claude แก้เองทั้งการ resubmit คลิปที่โดน filter และการยืด VO [A12.L05 t=02:03] [A12.L05 t=00:10]
- ระยะเวลาไม่ตรงกัน: shot list 5:00, รายงานความคืบหน้า "4:52 runtime", VO 5:11, package แต่ละเวอร์ชันระบุ 5:11 (Pompeii_LastDay) และ 4:59 (Pompeii_FINAL) [A12.L04 t=01:05] [A12.L05 frames t=00:35] [A12.L05 frames t=01:36]
- อัตรายืดวิดีโอ: ตอนอ่านจากภาพความละเอียดต่ำได้ "~1%" ซึ่งผิด ฉบับแก้จาก hires คือ VO ยาวกว่า 17s และยืด ~5% [A12.L05 frames t=00:15]
- thumbnail ที่ upload จริงไม่ชัด: รายการของ Claude (18 HOURS / WHY DID THEY STAY / LAST DAY) ไม่ตรงกับภาพที่แสดง (YOUR LAST DAY / RUN OR DIE / FROZEN FOR 2000 YEARS) และ thumb_B.png ในโฟลเดอร์เป็น "RUN OR HIDE?" / "79 AD" [A12.L05 t=00:40] [A12.L05 frames t=00:33]
- เวลาที่อ้างไม่ตรงกันข้ามบท: "20 minutes" (L01), "10 minutes" สำหรับวิดีโอแรก (L04), "15 minutes" สำหรับสามวิดีโอ (L07) [A12.L01 t=00:11] [A12.L04 t=02:32] [A12.L07 t=00:58]
- คำอ้าง "100 times cheaper, faster" ไม่มีตัวเลขสนับสนุน ต้นทุนที่เห็นมีแค่ "~2,500 total" credits และ "~3,000 credits" ไม่มีตัวเลขเป็นเงิน [A12.L04 t=03:11–03:16] [A12.L04 frames t=01:05]
- คำอ้างว่าทำวิดีโอ 10/20/30 นาทีโดยตัวละครและ style คงเดิมได้ ไม่ได้สาธิตในคอร์ส [A12.L03 t=01:44–01:52]
- "under your 5-minute cap" และ "square-waves gotcha" ชี้ไปที่ memory ของ project ก่อนหน้าซึ่งคอร์สไม่ได้แสดง [A12.L03 t=01:35] [A12.L04 t=00:25]
- ผล 3 วันเป็น vanity metrics ไม่มีรายได้ ไม่แยกตามวิดีโอ และยังห่างเกณฑ์ YPP 1,000 subs / 4,000 h มาก [A12.L07 t=00:05] [A12.L06 t=00:02–00:09]
- ไม่ชัดว่ายอดวิวเป็น organic หรือได้แรงจาก audience เดิมของผู้สอน [A12.L07 t=00:05]
- ชื่อ model thumbnail ไม่ได้บอก และวิดีโอที่สอง "ocean mysteries" ไม่ได้แสดงเนื้อหา [A12.L05 t=00:25] [A12.L05 t=01:55]
- หน้า Higgsfield แนะนำให้ผู้ใช้ Claude Code ใช้ CLI แต่ผู้สอนใช้ connector ผ่าน UI ของ Claude แล้วค่อยสลับไป Claude Code [A12.L02 frames t=00:13] [A12.L02 t=00:27–00:36]

### เทียบกับ v1
- เพิ่ม: prompt จริงทั้ง 4 ตัว (script / video / package / scale) และ prompt Shorts บนจอ [A12.L03 cue cue-script-prompt] [A12.L04 cue cue-video-prompt] [A12.L05 cue cue-packaging-prompt] [A12.L05 cue cue-scale-prompt] [A12.L06 t=00:55]
- เพิ่ม: URL ของ connector "https://mcp.higgsfield.ai/mcp" และหน้า consent [A12.L02 frames t=00:13] [A12.L02 t=00:25]
- เพิ่ม: รูปแบบ shot list ที่เครื่องอ่านได้ (หัว Seedance 2.0 + Inworld TTS Carter, 35 clips, 5/8/10s) [A12.L03 frames t=01:37]
- เพิ่ม: กลไก pipeline (ตรวจเครดิตก่อน, batch, ffmpeg, duck 10%) และไฟล์ที่ได้ [A12.L04 frames t=01:05] [A12.L04 t=01:15–01:20]
- เพิ่ม: failure ที่เห็นจริง (NSFW false flag + refund, VO ยาวกว่า 17s/ยืด ~5%, จ่ายซ้ำ ~3,000 credits) [A12.L05 t=00:10] [A12.L05 frames t=00:15] [A12.L05 t=00:50]
- เพิ่ม: ตัวเลข 3 วันจริง (7.3K views, 213.7 h, +27 subs) [A12.L07 t=00:05]
- แก้: v1 A12.03 บอกให้คนทำ "fact-check ก่อนกลายเป็นเสียงเล่า" แต่คอร์สบอกว่า Claude fact-check และ research ส่วนที่ขาดเองโดยไม่ต้องสั่ง (คอร์สไม่ได้ตรวจความถูกต้องของ fact) [A12.L04 t=01:02–01:13] [A12.L04 article]
- แก้: v1 A12.02 พูดเรื่อง "แยกวิธี CLI กับ UI" แบบกว้างๆ แต่บนจอ Higgsfield แนะนำ CLI สำหรับผู้ใช้ Claude Code ขณะที่ผู้สอนใช้ custom connector [A12.L02 frames t=00:13] [A12.L02 t=00:12–00:27]
- แก้: v1 A12.04 บอกว่า "ไม่ยืนยันคุณภาพจากข้อความว่าสร้างเสร็จ" ซึ่งยังถูก แต่คอร์สมีหลักฐานว่าข้อความ "done" ของ Claude ซ่อนงานซ้ำและเวลาที่ไม่ตรงไว้ด้วย [A12.L05 t=00:50] [A12.L04 t=01:05]
- เหมือนเดิม: เรียน format จากช่องต้นแบบโดยไม่คัดลอกเนื้อหา [A12.L01 t=01:56–02:03]
- เหมือนเดิม: ตัวอย่าง Vesuvius แบ่ง 9 ช่วงตามเวลา ตั้งแต่สัญญาณก่อนระเบิดถึงการขุดค้น [A12.L04 frames t=00:29]
- เหมือนเดิม: ยอดวิวระยะสั้นยังไม่ใช่หลักฐานรายได้ และรายได้ของ Bright Side ไม่ใช่ผลของ workflow นี้ [A12.L07 t=00:20–00:26] [A12.L07 t=00:05]

## A13 Mix AI with Real Footage

### ภาพรวมและผลลัพธ์
- คอร์สนี้ไม่ใช่ text-to-video แต่เป็นการแก้ footage จริงที่ถ่ายไว้แล้ว บน timeline ของ Adobe Premiere Pro ผ่าน Higgsfield plugin โดยให้ AI เปลี่ยนแค่บางส่วนของภาพ จนคนดูแยกไม่ออกว่าส่วนไหนจริง [A13.L01 t=00:00] [A13.L01 t=00:25]
- บทเปิดเป็นเกม "real or AI?" แสดงประเภทงานแก้ที่จะสอน: ลบวัตถุ (เครื่องตัดหญ้าหายไประหว่าง t=00:05 กับ t=00:10), เปลี่ยนสี/รุ่นรถ, เปลี่ยน background ในซอยถังขยะ (ตึกอิฐ → รั้วต้นไม้) [A13.L01 frames t=00:05] [A13.L01 frames t=00:20]
- ผู้สอนคือ Adil (lower-third "@ADIL") และพูดในนามทีม Higgsfield ("our newest ... plugin for Premiere") [A13.L01 frames t=00:40] [A13.L10 t=00:14]
- ผลลัพธ์ของคอร์ส: ทำครบ 8 งานบน timeline เดียว คือ remove, add, wardrobe, background, transition, multi-angle, reframe, upscale [A13.L10 t=00:14] [A13.L10 article]

### Workflow ทีละขั้น
1. ถ่าย footage จริงตามปกติ แล้วค่อยแก้ด้วย AI ภายหลังบน timeline (ไม่แยกไป render pipeline อื่น) [A13.L01 t=00:25] [A13.L01 article]
2. ติดตั้ง plugin: เว็บ Higgsfield > Plugins > Download แล้วรัน installer (macOS .pkg "Install Higgsfield") [A13.L02 t=00:00] [A13.L02 frames t=00:07]
3. เปิด Premiere แล้วไปที่ Window > Extensions > Higgsfield Plugin เพื่อเปิด panel [A13.L02 t=00:10] [A13.L02 frames t=00:13]
4. Sign in: panel ขึ้น "Sign in with your Higgsfield account to authorize the plugin." + ปุ่ม "Continue in Browser" แล้วไปกด Allow ที่หน้า consent "Higgsfield Adobe plugin" ในเบราว์เซอร์ [A13.L02 frames t=00:16] [A13.L02 frames t=00:18]
5. ลบวัตถุ: Edit Video > เลือกคลิป > พิมพ์ "Remove the car" > Generate > วางผลลัพธ์ลง timeline แทนต้นฉบับ [A13.L03 t=00:00] [A13.L03 t=00:03] [A13.L03 t=00:08]
6. เพิ่มคน: Edit Video > กด "+" แนบ character sheet (file picker) > พิมพ์ "add an old man" > Generate [A13.L04 t=00:09] [A13.L04 frames t=00:07]
7. เปลี่ยนชุด: สลับไป Draw to Video (header "Draw to edit") > ทา mask บน frame > พิมพ์ "change the outfit to pajamas" > Generate > ตัดกลับไป take เดิมเมื่อต้องการชุดเดิม [A13.L05 t=00:03] [A13.L05 t=00:18]
8. เปลี่ยน environment: Edit Video > "change the background behind the person to a sunset view from the hill" > Generate [A13.L06 t=00:01] [A13.L06 frames t=00:10]
9. ทำ transition: แนบ Start frame และ End frame > พิมพ์ "Make a dynamic transition" > Generate > วางคั่นระหว่างสองช็อต [A13.L07 t=00:00] [A13.L07 t=00:07] [A13.L07 article]
10. เพิ่ม coverage: Edit Video > "create a multi-shot with two different camera angles" > สลับไปมุมใหม่หรือกลับมุมเดิม [A13.L08 t=00:08] [A13.L08 t=00:17]
11. ทำหลายสัดส่วน: Reframe > เลือกหลาย format (9x16, 4x3, 21x9) > Generate พร้อมกัน > เทียบแล้วเลือกอันเดียว [A13.L09 t=00:04] [A13.L09 t=00:10]
12. แก้ภาพคุณภาพต่ำ: เลือกคลิป > Upscale (ไม่ต้องมี prompt) [A13.L10 t=00:04]

### กฎที่ใช้ซ้ำได้
- เก็บ plate จริงไว้ ให้ AI เปลี่ยนเฉพาะชั้นเดียวต่อรอบ (วัตถุ / คน / ชุด / background / มุมกล้อง) [A13.L01 article] [A13.L04 article]
- กฎ "insert ไม่ใช่ rebuild": ตอนเพิ่มคน ให้ล็อก performance, framing, lighting ไว้ แล้วใส่แค่ element ใหม่ [A13.L04 article]
- เลือกเครื่องมือตามขอบเขตงาน: Edit Video = แก้ทั้งคลิปด้วยข้อความ, Draw to Video = แก้เฉพาะจุดด้วย mask, Start/End frame = transition, Reframe = สัดส่วนภาพ, Upscale = คุณภาพ [A13.L06 article] [A13.L07 t=00:00] [A13.L09 t=00:04] [A13.L10 t=00:04]
- แก้เฉพาะจุดให้ทาบริเวณที่จะเปลี่ยน แทนการอธิบายตำแหน่งเป็นคำพูด [A13.L05 t=00:03] [A13.L05 article]
- ถ้าจะใส่คนที่เจาะจง ให้แบก identity ด้วยภาพ reference (character sheet) แล้วให้ prompt สั้น [A13.L04 t=00:09] [A13.L04 article]
- prompt เปลี่ยน background ให้ระบุ "the background behind the person" + วิว + ช่วงเวลาของวัน [A13.L06 t=00:01] [A13.L06 article]
- transition: ให้ start/end frame กำหนดเนื้อหา และใน prompt บอกแค่ "สไตล์" ของ transition [A13.L07 t=00:07] [A13.L07 article]
- ขอหลาย variation ในคำขอเดียว (หลายมุมใน prompt เดียว, หลายสัดส่วนใน Reframe รอบเดียว) แล้วค่อยเลือก [A13.L08 t=00:08] [A13.L09 t=00:10]
- วางผลลัพธ์แต่ละอันซ้อนบน track บนเหนือต้นฉบับ เพื่อสลับกลับไปหา source ได้ตลอด [A13.L03 t=00:08] [A13.L06 frames t=00:05] [A13.L08 t=00:17]
- scope ภาพ reference ให้แคบ ("appearance/texture reference only; ignore its background and lighting") เพื่อไม่ให้รั่วไปที่ environment [A13.L04 cue cue-add-figure-behind]
- เลือก format จากการเทียบผลจริงของช็อตนั้น: ในตัวอย่าง 9x16 แคบไป จึงขยายจนเลือก 21x9 (เป็นการตัดสินของช็อตนี้ ไม่ใช่กฎตายตัว) [A13.L09 t=00:23] [A13.L09 article]

### โครงสร้าง Prompt
- prompt ที่พิมพ์จริงในคอร์สสั้นมาก: verb + object เช่น ช่องพิมพ์ "remove car" (ตัวเล็ก ไม่มี "the"; placeholder ว่าง = "Enter your idea") ไม่มี keep-list เพราะคาดว่า tool จะเก็บส่วนอื่นเอง [A13.L03 t=00:03] [A13.L03 frames t=00:07]
- เพิ่มคน: verb + element ใหม่ แล้วให้ภาพแนบแบก identity; บนจอพิมพ์ "[A]dd an old man to the right" พร้อม thumbnail ภาพแนบ [A13.L04 t=00:09] [A13.L04 frames t=00:12]
- เปลี่ยนชุด: mask + คำสั่งสั้น "Change outfit to pajamas" (ตามที่เห็นบนจอ) [A13.L05 frames t=00:10]
- background: "change the background behind the person to" + <วิว> + <ช่วงเวลา> [A13.L06 t=00:01] [A13.L06 frames t=00:10]
- transition: "Make a" + <คำคุณศัพท์สไตล์> + "transition" โดยเนื้อหามาจาก 2 frame ที่แนบ [A13.L07 t=00:07] [A13.L07 frames t=00:09]
- multi-angle: "create a multi-shot with" + <จำนวน> + "different camera angles" [A13.L08 t=00:08] [A13.L08 frames t=00:12]
- Reframe และ Upscale ไม่มี text prompt เลย ใช้แค่การเลือก option [A13.L09 t=00:04] [A13.L10 t=00:04]
- prompt แบบยาวใน cue ใช้โครงเดียวกัน: `@source:` บรรยายคลิปเดิม (subject, wardrobe, รถ, ตำแหน่ง rig, motion) + รายการ "preserve exactly" + "Replace background environment only." [A13.L01 cue cue-intro-volcanic-drive]
  - ต่อด้วย style line (Photoreal, 16:9, 6s, filmic grade) / keep-list ซ้ำ "replace only the world" / "Continuous shot from the same rig, same framing" + โลกใหม่ที่มี parallax / คำสั่ง match แสง / "Face and identity unchanged." / "SFX only:" [A13.L01 cue cue-intro-volcanic-drive]
- คำสั่ง match แสงใน cue ระบุชัดว่าแสงจากโลกใหม่ตกกระทบ subject อย่างไร เช่น "raking his face and the white paint to match the source's golden-hour key exactly" [A13.L01 cue cue-intro-cloud-sea-drive]
- โครงสำหรับเพิ่ม VFX บนช็อต locked-off: "Appearance, face, camera, motion and lighting reference — preserve exactly" + "fire added as VFX" + "Static locked-off ultra-wide, same framing and slight barrel distortion as the source" + VFX ทีละ beat + แสงที่เกิดจาก VFX + constraint ("holds its shape and silhouette, never charring away") + "Everything else ... identical to the source" [A13.L01 cue cue-intro-hair-on-fire]
- โครงสำหรับเพิ่มสิ่งของ/สัตว์ด้วย reference: `>>:` บรรยาย source + preserve list (identity, face, wardrobe, performance, exact lip-sync, framing, lens, handheld) + "Change only the background" / `>>:` บรรทัด reference "Appearance, scale-texture and color reference only; ignore the photo's background and lighting" [A13.L04 cue cue-add-figure-behind]
  - ต่อด้วย style line (Photoreal, 16:9, 8s, grade matched to source plate, NON-IP) / timeline ช็อตเดียวที่มี camera move 1 วินาทีก่อนจะ "100% match of the original framing" / กฎ integration (key direction และ colour temperature เดียวกัน, contact shadows, haze, DoF) / "Lock-down:" / "SFX and source dialogue only" [A13.L04 cue cue-add-figure-behind]
- cue เปลี่ยนชุดไม่ใช่ prompt เต็ม แต่ให้ keep-list ที่ใช้ซ้ำได้: "Face, identity, body stance, movement, timing, expression, camera position and framing all identical to the source — only the wardrobe changes" + "No on-screen text or watermark." [A13.L05 cue cue-wardrobe-swap]
- cue เปลี่ยนโลกตอนกลางคืนเพิ่มคำสั่ง relight ตามเวลาใหม่ ("magenta and cyan neon spill ... cool rim ... skin kept readable") และ keep-list "replace only the world and the lighting" [A13.L06 cue cue-background-world-swap]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Higgsfield plugin สำหรับ Adobe Premiere Pro; prompt bar แสดง model "Seedance 2.0", "16:9", "1080p", ปุ่ม Generate และ "+" [A13.L01 frames t=00:35]
- แถว settings ใน Edit Video: "+" | "Seedance 2.0" | "16:9" | "4s" | "108..." (chip ความละเอียดถูกตัด อ่านไม่ครบ น่าจะ 1080p แต่ไม่เห็นเต็ม) [A13.L03 frames t=00:02] [A13.L04 frames t=00:10]
- result card แสดง metadata "Seedance 2.0 · 16:9 · 4s · Audio" และขึ้น "Queued" ระหว่างรอ [A13.L06 frames t=00:12] [A13.L08 frames t=00:14]
- ปุ่มใต้ preview ใน Edit Video: "Draw to video", "Reframe", "Remove BG", "Upscale" [A13.L03 frames t=00:02]
- หน้า home ของ plugin มี 7 apps: Draw to video (new), Edit video, Reframe, Remove BG ("Clean video backgrounds"), Upscale, Image generation, Video generation [A13.L06 frames t=00:05] [A13.L06 t=00:20]
- Draw to edit: slider เลือก frame, สี mask 8 สี, ตัวเลือก "Brush" และ slider ขนาดแปรง; แถว mode อ่านว่า "Draw to Edit · 1080p" ไม่มีชื่อ model ใน panel นี้ แต่ result card ระบุ "Seedance 2.0 · 16:9 · 4s · Audio" [A13.L05 t=00:05] [A13.L05 frames t=00:10] [A13.L05 frames t=00:14]
- Reframe: chip 6 ตัว "9:16" | "16:9" | "4:3" | "3:4" | "21:9" | "1:1" และปุ่ม Generate สีเขียวกว้าง (ตัวเลขบนปุ่มถูก cursor บัง) [A13.L09 frames t=00:07]
- Upscale: เลือก "1k" | "4K"; เลือก 1k ปุ่มอ่าน "✦ 5 Generate", เลือก 4K อ่าน "✦ ...13 Generate" (ตัวเลขน่าจะเป็นเครดิต แต่ UI ไม่ได้บอก) [A13.L10 frames t=00:05] [A13.L10 frames t=00:07]
- settings ใน cue: Photoreal, 16:9, 6s หรือ 8s, audio "SFX only" / "SFX and source dialogue only" [A13.L01 cue cue-intro-volcanic-drive] [A13.L04 cue cue-add-figure-behind]
- การ sign in ผ่าน OAuth consent (accounts.higgsfield.ai) ขอสิทธิ์ email, verify identity, basic profile แล้ว redirect ไป localhost [A13.L02 frames t=00:18]
- เว็บ Higgsfield ที่เห็นมี tool cards: Supercomputer, Nano Banana Pro, Seedance 2.0, Marketing Studio, MCP & CLI ("Turn Claude into a creative engine"), Higgsfield Canvas, Cinema Studio 3.5 และ tile "Adobe Premiere Pro and After Effects are live" [A13.L02 frames t=00:02]

### คำเตือนและ failure modes
- คอร์สไม่ได้ระบุคำเตือนโดยตรง; ข้อสังเกตเดียวคือ 9x16 ของช็อตนี้แคบเกินไป ซึ่งเป็นการตัดสินเฉพาะเฟรม [A13.L09 t=00:23]
- prompt สั้นไม่ได้รับประกันว่ารายละเอียดที่พูดจะเข้าไปใน job: L08 พูดว่า "left side / lower angle" แต่ช่องพิมพ์มีแค่บรรทัดทั่วไป และ job ถูก queue ไปแล้ว [A13.L08 frames t=00:12] [A13.L08 frames t=00:14]
- mask ที่ทาแค่ลำตัวยังได้ชุดนอนครบทั้งเสื้อและกางเกง — ขอบเขตผลลัพธ์อาจกว้างกว่า mask [A13.L05 t=00:05] [A13.L05 t=00:15]
- ภาพ reference ที่ไม่ได้จำกัด scope อาจรั่วพื้นหลัง/แสงเข้ามา จึงต้องเขียน "ignore the photo's background and lighting" [A13.L04 cue cue-add-figure-behind]
- Upscale มี option ความละเอียดที่เปลี่ยนตัวเลขบนปุ่ม (5 vs ...13) — ตรวจก่อนกดถ้าตัวเลขนั้นคือเครดิต [A13.L10 frames t=00:05] [A13.L10 frames t=00:07]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- model ที่ใช้ใน plugin คือ Seedance 2.0 (16:9 / 1080p ใน prompt bar, 4s ใน result card) ซึ่ง article ไม่ได้ระบุ [A13.L01 frames t=00:35] [A13.L06 frames t=00:12]
- การเชื่อมบัญชีเป็นหน้า OAuth consent ในเบราว์เซอร์ (Allow/Deny) ไม่ได้กรอกรหัสใน panel [A13.L02 t=00:15]
- panel ถูก dock เป็นคอลัมน์ซ้าย ข้าง program monitor และ timeline มีแถบ "Last generations" และหมวด "Apps" [A13.L02 t=00:20]
- panel queue งานได้: card ที่กำลังทำแสดงใต้ผลก่อนหน้าขณะทำงานต่อ และ Reframe 3 format generate ขนานกันเป็น 3 card [A13.L07 t=00:10] [A13.L09 t=00:10]
- ผลเปลี่ยน background มีการ relight subject ให้เข้ากับ sunset (back light อุ่น, ดวงอาทิตย์ที่ขอบฟ้า) ไม่ใช่แค่เปลี่ยน plate [A13.L06 t=00:15]
- ผล transition เป็น camera move เร็ว motion blur ผ่านใบปาล์ม (สไตล์ whip/wipe) [A13.L07 t=00:15]
- ผล Reframe 4:3 มีหญ้าและท้องฟ้ามากกว่า source 16:9 แปลว่าขยาย frame (คล้าย outpaint) — เป็นการอนุมาน คอร์สไม่ได้พูด [A13.L09 t=00:25]
- start/end frame ถูกแนบผ่าน "+" ที่เปิด file picker (2 ไฟล์ .png 4,8 MB) [A13.L07 frames t=00:04] [A13.L07 frames t=00:07]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- ชื่อ "Quixel" ในชื่อบทและ article (และ "Kixel" ใน transcript L01/L10) ผิด — ต้องเป็น Higgsfield plugin; เสียงใน L02 และทุกหน้าจอ (เว็บ, installer, OAuth, panel) เขียน Higgsfield [A13.L02 t=00:00] [A13.L02 frames t=00:18] [A13.L01 t=00:54]
- article บอกว่า transition ทำใน "Video Generation" แต่ header ของ panel ในเฟรมอ่านว่า "Edit video" ขณะแนบ 2 frame [A13.L07 article] [A13.L07 frames t=00:07]
- สีรถที่สลับใน L01: article บอกแดง→ขาว, transcript บอกขาว→ดำ; tile ที่ t=00:15 เป็นรถซีดานสีขาว [A13.L01 t=00:00] [A13.L01 article] [A13.L01 frames t=00:15]
- cue ไม่ตรงกับวิดีโอ: cue ของ L01 (convertible/ภูเขาไฟ/ทะเลเมฆ/ผมติดไฟ), L04 (rooftop Almaty, Hotel Kazakhstan, ตะกวด, wing-walker พร้อม placeholder "prompt 1 wing walker") และ L06 (convertible กลางคืนเมือง neon) ไม่ปรากฏใน tile ที่สุ่มดู — ใช้ได้แค่โครงสร้าง [A13.L01 cue cue-intro-volcanic-drive] [A13.L04 cue cue-add-figure-behind] [A13.L06 cue cue-background-world-swap]
- article L04 เกริ่นว่า "Swapping the world around you is one thing" แต่ในลำดับวิดีโอ บทเปลี่ยน background (L06) มาทีหลัง [A13.L04 article]
- L01 บอกว่าทริกสุดท้ายคือทริกโปรด แต่บทสุดท้ายคือ Upscale — ไม่ได้ยืนยันว่าหมายถึงอันไหน [A13.L01 t=00:54] [A13.L10 t=00:04]
- ผลลัพธ์ที่ไม่อยู่ใน tile ที่สุ่ม: รถหายใน L03, ชายชราใน L04 (เห็นใน tile แรกของ L05 แทน), มุมใหม่ใน L08 และตัวเลือก 21x9 สุดท้ายใน L09 [A13.L03 t=00:08] [A13.L05 t=00:00] [A13.L08 t=00:17] [A13.L09 t=00:30]
- chip ความละเอียดถูกตัดเป็น "108..." ทุกบท จึงยืนยันค่าเต็มไม่ได้ [A13.L03 frames t=00:02]
- คอร์สไม่เคยพูดเรื่องเครดิตต่อการทำงาน ตัวเลขบนปุ่ม Upscale ไม่มี label [A13.L10 frames t=00:07]
- คุณภาพก่อน/หลัง Upscale ตัดสินไม่ได้ที่ความละเอียด contact sheet [A13.L10 t=00:10]

### เทียบกับ v1
- v1 ผิด: v1 ใช้ชื่อ Quixel ตามข้อความบท; ชื่อที่ถูกคือ Higgsfield plugin ตามเสียงและหน้าจอ [A13.L02 t=00:10] [A13.L02 frames t=00:13]
- เพิ่ม: model Seedance 2.0 และ settings (16:9, 4s, 1080p, Audio) ที่ v1 ไม่ได้ระบุ [A13.L01 frames t=00:35] [A13.L08 frames t=00:14]
- เพิ่ม: prompt ที่พิมพ์จริงทุกบท ("remove car", "Add an old man to the right", "Change outfit to pajamas" ฯลฯ) [A13.L03 frames t=00:07] [A13.L04 frames t=00:12] [A13.L05 frames t=00:10]
- เพิ่ม: โครง prompt ยาวจาก cue (`@source` + preserve list + relight + "Face and identity unchanged." + "SFX only") [A13.L01 cue cue-intro-volcanic-drive]
- เพิ่ม: ขั้นตอนติดตั้ง/OAuth และ UI ของ Draw to edit, Reframe, Upscale (1k/4K) [A13.L02 frames t=00:16] [A13.L05 t=00:05] [A13.L09 frames t=00:07] [A13.L10 frames t=00:05]
- แก้: v1 เขียนรายการตรวจ QC (เงาหลง, ขอบแขน, ใบหน้าคนเดิมเปลี่ยน ฯลฯ) ซึ่งไม่มีในบันทึกของคอร์ส; บันทึกบอกว่าคอร์ส "none stated" สำหรับคำเตือน [A13.L03 t=00:00] [A13.L05 t=00:03]
- เหมือนเดิม: การเทียบ 9:16 / 4:3 / 21:9 และการเลือก 21:9 เป็นการตัดสินของช็อตนี้ ไม่ใช่คำตอบทุกช่องทาง [A13.L09 t=00:23]
- เหมือนเดิม: start/end frame เป็นตัวกำหนดปลายทางของ transition [A13.L07 t=00:00]

## A14 Build 3D Games with MCP

### ภาพรวมและผลลัพธ์
- ผู้สอน Adil (@adilinthewild) อ้างว่าสร้างเกม multiplayer จริง 3 เกมในบ่ายเดียวโดยไม่เขียน code เลย publish แล้วตื่นมาเจอผู้เล่นเกือบ 4,000 คนและ 120 remixes (ตัวเลขที่ผู้สอนรายงานเอง) [A14.L01 t=00:00] [A14.L01 article]
- ปัญหาที่คอร์สแก้: เกมที่ Claude ทำเองมี logic ใช้ได้ แต่หน้าตาพื้นฐาน (ตัวละครเป็น capsule, กล่องสีเทา, texture เดียวทั้งโลก) [A14.L01 t=00:21] [A14.L01 article]
- ทางแก้คือแบ่งงาน: Claude Fable 5 เขียน game logic, Higgsfield MCP สร้าง skins/textures/environments และ host เกมให้ [A14.L01 t=00:37] [A14.L04 t=00:24]
- 3 เกมในคอร์ส: pirate game "BROADSIDE — PIRATE BOARDING", Blockfield (voxel team shooter), NeonSlice (หั่นผลไม้ด้วย webcam) [A14.L03 frames t=00:29] [A14.L05 t=00:19] [A14.L06 t=00:14]
- ปลายทางของคอร์ส: publish ขึ้น Higgsfield marketplace, วัดผล, ดูต้นทุนจริง ($68 สำหรับ 3 เกม) และได้ความเห็นจาก CEO ของ Smilegate [A14.L07 t=00:01] [A14.L09 t=00:00] [A14.L10 t=00:00]

### Workflow ทีละขั้น
1. วินิจฉัย baseline ก่อน: Claude อย่างเดียวได้ code ที่ทำงาน แต่ภาพเป็น capsule/กล่องเทา [A14.L01 t=00:21] [A14.L04 t=00:16]
2. Setup ขั้นที่ 1 (~30 วินาที): ใน Claude > Customize > Connectors เพิ่ม custom connector "Higgsfield" (dialog "Add custom connector BETA" มีช่อง "Remote MCP server URL") แล้ว sign in ผ่านหน้า OAuth กด Allow [A14.L02 t=00:04] [A14.L02 frames t=00:06] [A14.L02 frames t=00:08]
3. Setup ขั้นที่ 2: Customize > Skills > upload custom skill "game-studio" (Trigger: "Slash command + auto") [A14.L02 t=00:12] [A14.L02 frames t=00:15]
4. เปิด chat ใหม่ใน Claude (model chip "Fable 5 High", มี chip "Higgsfield" เหนือหัวข้อ) แล้วพิมพ์ประโยคเดียวอธิบายเกม [A14.L03 frames t=00:14] [A14.L03 t=00:11]
5. ตอบ interview แบบ multiple-choice ของ skill (มุมกล้อง/การควบคุม, look & setting, ขนาด match, ชุดอาวุธ, กติกาจบรอบ) หรือพิมพ์คำตอบเอง [A14.L05 t=00:39] [A14.L05 frames t=00:42]
6. อ่าน design brief ที่ skill เขียน แล้วอนุมัติ ("tell me whether to build it as is") [A14.L05 frames t=00:40] [A14.L05 frames t=00:42]
7. skill + MCP สร้าง assets และ deploy เกมไปที่ link *.higgsfield.gg โดย host และ sync ผู้เล่นให้อัตโนมัติ [A14.L05 t=01:00] [A14.L04 t=00:54]
8. เก็บ game_id ที่ได้กลับมา เพื่อให้การแก้ภายหลัง (rebalance, ปรับ map, rename) อัปเดต URL เดิม [A14.L05 frames t=01:02]
9. Play-test ด้วยการเปิดสอง tab หรือส่ง link ให้เพื่อน แล้วปรับค่าที่ skill แนะนำ (bazooka splash radius, sniper fire rate, respawn timer) [A14.L05 frames t=01:00]
10. ตอบ yes เมื่อ skill ถามว่าจะ publish ขึ้น Higgsfield marketplace ไหม [A14.L07 t=00:01]
11. วัดผล: plays, concurrent players, remixes [A14.L08 t=00:00] [A14.L08 t=00:22]
12. ขอให้ Claude ดึง credit breakdown ทั้งหมดรวม generation ที่ล้มเหลว [A14.L09 t=00:00]
13. ใช้ marketplace เป็น top of funnel ฟรี แล้วเอาเกมที่พิสูจน์แล้วไปยัง digital distribution platforms เพราะเราเป็นเจ้าของ code [A14.L09 t=00:12] [A14.L09 t=00:22]
14. หาความเห็นจากภายนอกแทนการประเมินตัวเอง [A14.L09 t=00:35] [A14.L10 t=00:00]

### กฎที่ใช้ซ้ำได้
- แบ่งบทบาท: "Fable writes the game and Higgsfield makes it look real" [A14.L04 t=00:24] [A14.L04 article]
- ทดสอบแบบ A/B: prompt เดียวกัน model เดียวกัน สลับแค่ MCP + skill แล้วเทียบภาพ [A14.L04 t=00:00] [A14.L04 article]
- ประโยคเดียวพอ ถ้ามี skill ขยายผ่าน interview เป็น "studio-grade brief"; brief คือ build prompt ตัวจริง ไม่ใช่ one-liner [A14.L05 t=00:49] [A14.L05 article]
- อนุมัติ design brief ก่อน build เพราะมันล็อก controls, สถิติอาวุธ, map และกติกา respawn [A14.L05 frames t=00:40]
- ให้อาวุธแต่ละชิ้นมี trade-off ชัด (sniper ยิงช้า + scope + ดาเมจสูง; bazooka จรวด + splash + ทำลาย block) [A14.L05 t=01:25] [A14.L05 article]
- ใช้ game_id ซ้ำเพื่ออัปเดตที่เดิม ถ้าไม่ใช้ การแก้จะสร้างเกมใหม่ที่ link ใหม่ [A14.L05 frames t=01:02]
- Deployed = เราส่ง link เอง; Published = คนแปลกหน้าค้นเจอ เล่น และ remix ได้ — ควร publish [A14.L07 t=00:06] [A14.L07 article]
- นับ generation ที่ล้มเหลวรวมในต้นทุนจริง [A14.L09 t=00:02] [A14.L09 article]
- ใช้ play เป็นสัญญาณฟรีว่าอะไรสนุก และนับ remix เป็นสัญญาณที่แรงกว่า play [A14.L07 t=00:28] [A14.L08 t=00:22]
- จังหวะแพลตฟอร์ม: publish ตอน marketplace ยังใหม่ ("the only game in town when the players show up"); ผู้สอนบอกว่าอีก 6 เดือนจะแออัด [A14.L07 t=00:36] [A14.L10 t=01:35]

### โครงสร้าง Prompt
- pirate prompt (ตาม cue/ที่พิมพ์): "Build a first-person pirate game where I sail a galleon, fire cannons at enemy ships, and board them for a sword fight on deck." [A14.L03 cue pirate-prompt]
- โครง slot: `Build a <perspective> <genre> game where I <traversal verb + vehicle>, <primary combat verb + target>, and <secondary interaction> for <secondary combat mode> on <location>.` [A14.L03 cue pirate-prompt]
- Blockfield prompt: "Build a block-world shooter with two teams against each other, where I can place and destroy blocks and fight the opposite team." [A14.L05 cue blockfield-prompt]
- โครง slot: `Build a <world style> <genre> with <team structure>, where I can <sandbox verbs> and <combat objective>.` [A14.L05 cue blockfield-prompt]
- ประโยคเปิด interview ของ skill: "Great pitch. ... Let me lock a few decisions before I write the design brief and build it. Tap your answers, or type your own." [A14.L05 frames t=00:35]
- คำตอบ interview ใน Blockfield: First-person / Bright voxel cartoon, desert theme / Big battle (up to ~22) / Full arsenal + a bazooka (6 slots) / Timed match, most kills wins [A14.L05 frames t=00:42]
- โครง design brief ที่ใช้ซ้ำได้: TITLE / ONE-LINE PITCH / GENRE (+ หมายเหตุเลี่ยง IP "no trademarked block-game names") / CONTROLS / WEAPONS AND TOOLS (เลขกำกับ แต่ละชิ้นมีสถิติ + trade-off) / กติกา sync / MAP (layout, bases, spawn, respawn UI) [A14.L05 frames t=00:40]
- ตัวอย่างใน brief: 6 slots = RIFLE (auto, 30-round mag), SHOTGUN (6 shells), SNIPER (scope RMB, one-shot headshot), BLOCKS (RMB วาง, wheel เปลี่ยนสี), PICKAXE (ขุด block), BAZOOKA (splash, ทำลาย block, reload ช้า); V = push-to-talk; map "Desert Temple" ฐาน Red/Blue [A14.L05 frames t=00:40]
- prompt bar ใน L01 (บนจอเท่านั้น ไม่ได้พูด): "Build me a first-person wall-running shooter with guns and monsters." [A14.L01 frames t=01:14]
- คำสั่งดึงต้นทุน: ผู้สอนเล่าว่า "asked Claude to pull the full credit breakdown" รวม failed generations — ไม่เห็นข้อความจริง [A14.L09 t=00:00]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Claude model chip "Fable 5 High" (Claude Fable 5, effort High) [A14.L03 frames t=00:14] [A14.L05 frames t=00:23]
- Higgsfield MCP เป็น custom connector ใน Claude; หน้า OAuth "Claude wants to access Higgsfield.AI on behalf of <account email>" ขอ "Verify your identity" และ "Your email address" [A14.L02 frames t=00:08]
- custom skill "game-studio": Added by: You, Trigger "Slash command + auto", Last updated Jun 16, 2026 (ผู้ audit อ่านได้ 16; ใน note อ่านไม่ชัดว่า 14) [A14.L02 frames t=00:15]
- คำอธิบาย skill (อ่านจาก crop ความละเอียดต่ำ ถ้อยคำไม่รับประกัน): เปลี่ยนไอเดียเกมบรรทัดเดียวเป็นเกม browser multiplayer ที่ deploy แล้ว โดยทำตัวเป็น game studio — interview → design brief → build → deploy → เสนอ publish; ห้ามใช้กับการแก้ code ทีละบรรทัด, app ที่ไม่ใช่เกม, หรือ voxel two-team shooter (ซึ่งมี skill เฉพาะ ดูเหมือนชื่อ "blockfield prompt expander") [A14.L02 frames t=00:15]
- ใน list skill มี "skill-creator" ด้วย แต่ไม่ได้ใช้ในคอร์ส [A14.L02 frames t=00:15]
- เกม host บน subdomain *.higgsfield.gg เช่น pirates.higgsfield.gg และ https://gallant-crane-167.higgsfield.gg/ [A14.L04 frames t=00:55] [A14.L05 frames t=01:02]
- หน้าเกมมี badge "HIGGSFIELD GAMES" และปุ่ม "Remix game" / "Copy link" [A14.L03 frames t=00:29]
- prompt bar mock ใน L01: "GPT Image 2", "16:9", "High", "2K", ตัวนับ "− 4/4 +", ปุ่ม "GENERATE" ราคา 28 credits [A14.L01 frames t=01:12]
- ต้นทุนรวม 3 เกม: TOTAL "$68.00" รวม failed generations; ใบเสร็จมี 2 บรรทัดที่ดูเหมือน Claude subscription + Higgsfield credits (ตัวเลขแยกอ่านไม่ชัด อาจ ~$20 + ~$48) [A14.L09 t=00:00] [A14.L09 frames t=00:05]
- ไม่มีการระบุ model generation ที่ใช้ทำ textures/skins/sound/animations, ไม่มี resolution หรือ seed [A14.L03 frames t=00:29]

### คำเตือนและ failure modes
- Claude อย่างเดียวได้แค่ tech demo: ไม่มี skins, textures หรือทะเลจริง เป็นรูปทรงเทา [A14.L04 t=00:16] [A14.L04 article]
- การเอาเกม vibe-coded ขึ้นออนไลน์แบบ multiplayer เป็นปัญหาแยก: วิธีเดิมต้องจ้าง back-end developer ~$50/ชั่วโมง (ตัวเลขนี้มีแค่ในเสียง), ทำ player-sync หลายสัปดาห์, เช่า server ทุกเดือน [A14.L04 t=00:34] [A14.L04 t=00:41]
- ใช้ chatbot ทั่วไป deploy ได้ แต่เราต้องเป็นคนกลางดูแล infrastructure เอง [A14.L05 t=01:05] [A14.L05 article]
- deploy ครั้งแรกเดา URL ของ zip ผิดได้ 403 แล้วแก้เป็น object URL ที่ถูก; publish ชนชื่อ จึงได้ชื่อใน marketplace "Blockfield: Desert Temple" ต่างจากชื่อในเกม "Blockfield - Multiplayer" [A14.L05 frames t=01:02]
- ไม่ใช้ game_id ซ้ำ = การแก้ทุกครั้งสร้างเกมแยกที่ link ใหม่ [A14.L05 frames t=01:02]
- ในเกมมี fallback "Microphone unavailable — you can hear others but not talk" (อ่านคร่าวๆ) [A14.L05 frames t=01:25]
- NeonSlice: tracking นิ้วหลุด = เสีย blade, โดนระเบิด = เสียหัวใจ; ส่วนยากคือให้ tracking, prediction, physics ทำงานด้วยกันโดยไม่พัง [A14.L06 t=00:32] [A14.L06 t=00:58]
- อคติของผู้สร้าง: "My opinion is not really worth much here" [A14.L09 t=00:35]
- ความเห็น CEO ใช้คำว่า "prototyping" — เป็นการรับรองระดับ prototype ไม่ใช่เกมเชิงพาณิชย์ที่เสร็จแล้ว (ตีความจาก subtitle) [A14.L10 frames t=00:55]
- ช่วงได้เปรียบมีเวลาจำกัด: กราฟ "OPPORTUNITY VS COMPETITION" จาก "Now" ถึง "6 months later" เป็นกราฟประกอบ ไม่มีแหล่งข้อมูล [A14.L07 frames t=00:45]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- ชื่อ skill "game-studio", trigger "Slash command + auto" และพฤติกรรม interview → brief → build → deploy → publish มีแค่บนจอ article บอกแค่ "a custom skill" [A14.L02 frames t=00:15]
- UI interview แบบ multiple-choice มีตัวเลือก "Something else" และปุ่ม Skip พร้อม 5 คู่คำถาม-คำตอบ [A14.L05 frames t=00:35] [A14.L05 frames t=00:42]
- เนื้อหา design brief เต็ม (controls, อาวุธ 6 ชิ้นพร้อมสถิติ, กติกา sync "Placing/mining is instant and synced to all players", map "Desert Temple", respawn "Respawning in X.Xs") [A14.L05 frames t=00:40]
- รายงาน deploy/publish: 403 retry, ชื่อชน, play link, game_id, ทดสอบสอง tab, ค่าที่ควรจูน [A14.L05 frames t=01:02]
- HUD เกมเรือ: "Enemy on the horizon! Close in and open fire.", "Q — harpoon launcher to board", "E — man the cannon", "Sails: 90% · Distance: 73 m" และเกมรันใน browser ที่ higgsfield.ai (cursor-lock overlay) [A14.L03 frames t=00:29] [A14.L03 frames t=00:25]
- หน้า onboarding "MAKE GAMES WITH HIGGSFIELD MCP IN CLAUDE": 1 Copy this URL → 2 Add the Higgsfield custom connector → 3 Make your first game ("Create game in Claude") [A14.L07 frames t=00:05]
- หน้า listing ใน marketplace: คำอธิบาย, จำนวน users/remixed, ปุ่ม Remix game / Play game, หน้าจอเกมฝังในหน้า และแถว "Explore Higgsfield Games" [A14.L08 frames t=00:00]
- ป้ายชื่อ CEO "HARRY (HG) NAM, CEO & PRESIDENT SMILEGATE" และ subtitle: เห็นเป็นวิธี prototype ไอเดียที่เร็วที่สุด, ช่วยการสื่อสารภายใน, "completeness ... much higher than expected" [A14.L10 frames t=00:20] [A14.L10 frames t=00:25]
- ขั้น funnel บนจอ: "STEP 1 PUBLISH YOUR GAMES", "STEP 2 TEST ON A REAL PLAYERS", "STEP 4 DISTRIBUTE GAMES", "STEP 5 EARN MONEY" [A14.L09 frames t=00:15] [A14.L09 frames t=00:25]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- ผู้สอนพูดว่า marketplace "almost empty" แต่ grid บนจอตอนบันทึกมีเกมของคนอื่นแล้ว ~17 เกม (BLOCKFIELD, ALIEN INTRUDERS, NEON DRIFT, ...) [A14.L07 t=00:19] [A14.L07 frames t=00:05]
- จำนวน remix: L01 พูด 120, L08 พูด 121 (ปัดเศษ) [A14.L01 t=00:00] [A14.L08 t=00:22]
- prompt เกมเรือที่พูดต่างจากที่พิมพ์: เสียงว่า "fire cannons, add enemy ships" แต่ cue/บนจอเป็น "fire cannons at enemy ships" [A14.L03 t=00:11] [A14.L03 cue pirate-prompt]
- transcript ส่วน CEO เป็นเสียงเกาหลีที่ whisper แปลเพี้ยน ("10 million dollars") ขณะที่ subtitle บนจอบอก "$1 billion in annual revenue" — ใช้ subtitle บนจอ [A14.L10 frames t=00:25]
- ชื่อ Smilegate อยู่แค่ใน article ของ L09 ไม่อยู่ในเสียงบทนั้น [A14.L09 article]
- ตัวเลข 4,000 ผู้เล่น / 121 remixes เป็นการรายงานเอง ตัวเลขบนหน้า listing ("~3,8xx users · ~12x remixed") อ่านไม่ชัด [A14.L08 frames t=00:00]
- ไม่เห็นไฟล์ skill จริง เห็นแค่คำอธิบายความละเอียดต่ำ; link "in the description" ไม่อยู่ในเอกสารคอร์ส [A14.L02 t=00:17] [A14.L02 frames t=00:15]
- ไม่เคยระบุว่า model generation ตัวไหนสร้าง textures/skins/sound [A14.L03 cue pirate-generated-assets]
- prompt ของ NeonSlice ไม่แสดง (มีแค่ตัวอย่าง "make a fruit-slicing game with my webcam" ในคำอธิบาย skill) และชื่อ "NeonSlice" ไม่ปรากฏบนจอ [A14.L06 t=00:14] [A14.L02 frames t=00:15]
- interview/brief ของเกมเรือไม่ถูกแสดง [A14.L03 t=00:11]
- การแบ่ง $68 และเครดิตต่อเกมไม่ชัด [A14.L09 frames t=00:05]
- STEP 3 ของ funnel ไม่อยู่ใน tile ที่สุ่ม และ "digital distribution platforms" ไม่เคยถูกระบุชื่อ; ไม่มีคำอธิบายเรื่องราคา rev share หรือ licensing ของ assets [A14.L09 frames t=00:15] [A14.L09 t=00:22]
- ภาพ studio play-test มีแค่ Blockfield ไม่เห็นเกมเรือหรือ NeonSlice [A14.L10 frames t=00:55]

### เทียบกับ v1
- เพิ่ม: path UI setup จริง (Customize > Connectors / Skills), ชื่อ skill "game-studio" และ trigger [A14.L02 frames t=00:06] [A14.L02 frames t=00:15]
- เพิ่ม: prompt ตัวเต็มของเกมเรือและ Blockfield พร้อมโครง slot [A14.L03 cue pirate-prompt] [A14.L05 cue blockfield-prompt]
- เพิ่ม: คำตอบ interview และโครง design brief ที่ใช้ซ้ำได้ [A14.L05 frames t=00:42] [A14.L05 frames t=00:40]
- เพิ่ม: model "Fable 5 High", host *.higgsfield.gg, การใช้ game_id ซ้ำ และ failure 403/ชื่อชน [A14.L03 frames t=00:14] [A14.L05 frames t=01:02]
- เพิ่ม: ตัวเลขผลลัพธ์ (~4,000 ผู้เล่น, สูงสุด 22 คนพร้อมกัน, 121 remixes) และต้นทุน $68 ซึ่ง v1 ไม่ได้ให้ตัวเลข [A14.L08 t=00:00] [A14.L09 t=00:00]
- เหมือนเดิม: deploy กับ publish เป็นคนละขั้น [A14.L07 t=00:06]
- เหมือนเดิม: ความเห็นสตูดิโอไม่ใช่ benchmark; ในวิดีโอ CEO เองพูดถึงการ "prototyping" [A14.L10 frames t=00:55]
- เหมือนเดิม: v1 เตือนว่าข้อกล่าวอ้างเรื่อง hosting/multiplayer ยังไม่ได้ทดสอบ — บันทึก v2 ก็มีแค่ภาพเพื่อนกด link pirates.higgsfield.gg ไม่มีการทดสอบอิสระ [A14.L04 frames t=00:55]
- แก้: v1 ไม่ได้บอกว่า CEO ชื่ออะไรหรือพูดอะไร; v2 ระบุตาม subtitle บนจอ [A14.L10 frames t=00:20]

## A15 Direct a cinematic AI car commercial

### ภาพรวมและผลลัพธ์
- คอร์สเปิดด้วยโฆษณารถสีแดงที่เสร็จแล้ว (~90 วินาที): ส่งกุญแจในโชว์รูม, ผู้หญิงหยุดรถกลางถนน, ผู้โดยสารรีบไปสนามบิน, เจ้าหน้าที่ด่านอ่านหนังสือพิมพ์, ส่งที่สนามบิน แล้วผู้สอน (Adil) อธิบายวิธีทำ [A15.L01 t=00:00] [A15.L01 frames t=01:10]
- Workflow มี 3 ขั้น: Assets, Setup, Generations และใช้ได้กับโฆษณาสินค้าใดก็ได้ (sneakers, perfume) โดยเปลี่ยน assets [A15.L01 t=01:43] [A15.L01 frames t=01:45]
- ผลลัพธ์ของคอร์ส: หนัง 5 ฉาก (โชว์รูม, ปั๊มน้ำมัน + ในรถ, driving montage, ด่านเก็บเงิน, สนามบิน) ที่ประกอบจากชิ้นส่วนของหลาย take โดยมี reference ที่ล็อกไว้ทุกตัว [A15.L03 t=01:39] [A15.L07 t=00:00] [A15.L11 t=01:05]
- ตั้งแต่ L04 เป็นต้นไป ผู้สอนเปลี่ยนวิธีสอนเป็นการโชว์เฉพาะสิ่งที่พังและวิธีแก้ ส่วน assets และ prompts อยู่ "in the description" [A15.L04 t=00:11]
- หลักใหญ่ที่ย้ำทั้งคอร์ส: continuity เป็นหน้าที่ของเรา model ไม่ได้ติดตามให้ [A15.L05 t=00:00] [A15.L05 article]

### Workflow ทีละขั้น
1. ดูโฆษณาอ้างอิงสองรอบ รอบสองนับเฉพาะสิ่งที่ต้องอยู่รอดข้ามช็อต (รถแดง, คนขับสองลุค, ผู้โดยสาร, พนักงานขาย, กุญแจ, สถานที่ที่กลับมา) [A15.L01 article]
2. ตั้ง project ใน Cinema Studio ("Car Commercial"): หนึ่ง folder ต่อฉาก, subfolder ตามประเภท asset, และ subfolder ใหม่ทุก iteration [A15.L01 t=01:57] [A15.L01 frames t=02:05]
3. สร้าง product reference บนพื้นเทากลาง แล้วบันทึกเป็น element ชื่อขึ้นต้นด้วย `@` (เช่น `car_sheet`) และบอกชื่อเดียวกันกับ Claude เพื่อให้ prompt ที่ Claude เขียนแนบ element อัตโนมัติเมื่อวางกลับใน Higgsfield [A15.L01 t=02:19] [A15.L01 t=02:31] [A15.L01 t=02:45]
4. ทำ character sheet 3 panel (หลังไม่มีหัว, หน้าไม่มีหัว, close-up ใบหน้า) ด้วย prompt ที่ Claude เขียน เลือกจากความแม่นของใบหน้า และ A/B model edit (Seedream 5.0 Pro vs Nano Banana Pro) [A15.L02 t=00:09] [A15.L02 t=00:47] [A15.L02 t=01:20]
5. ภาพที่ต้องการการแสดงเป็นธรรมชาติ: generate ใน Soul Cinema ก่อน แล้ว face-swap ใบหน้าที่อนุมัติในรอบ edit แยก [A15.L02 t=01:48] [A15.L02 article]
6. ทำ variant ของเรื่อง (ปลอมตัว) เป็น edit ของ sheet เดิม พร้อม prop ที่ออกแบบเผื่อ action ในอนาคต (หนวดปลอมแบบติด) [A15.L02 t=03:29] [A15.L02 article]
7. Cast ตัวละครรองตามบทบาท วนจนอ่านออกว่าใช่ และลบใบหน้าที่ขัดกันออกจาก sheet ด้วย image editor [A15.L02 t=05:06] [A15.L04 t=00:23]
8. แต่ละ location: prompt ขี้เกียจเพื่อหา vibe → Color Transfer ล็อก palette → prompt ละเอียดจาก Claude → มุม three-quarter → clean plate (ลบตัวหนังสือ, ของรก, รถไกลๆ) ทีละรอบแล้วทดสอบใน motion [A15.L03 t=00:05] [A15.L03 t=00:23] [A15.L04 t=01:14] [A15.L04 t=01:25]
9. โหลด Seedance prompt-generator skill ใน Claude แนบ assets ที่ล็อกแล้ว อธิบายฉากทีละ beat แล้ววาง output (REFERENCE DEFINITIONS / TECHNICAL BLOCK / PROMPT) ลงใน Seedance 2.0 [A15.L03 t=01:17] [A15.L03 frames t=01:35]
10. Generate เป็น batch แล้วเลือกระดับช็อต (ไม่ใช่ระดับ take) แล้ว stitch ฉากจากชิ้นส่วน [A15.L03 t=01:39] [A15.L06 t=00:31]
11. เช็ค geography ข้ามฉากบน timeline แล้วเติม bridge shot ใน location แยก เพื่อไม่เผยปลายทางเร็วเกิน [A15.L05 t=00:00] [A15.L05 t=00:21]
12. ดึง still ภายในรถ/ตำแหน่งจากวิดีโอ "statics" ต่อเนื่องอันเดียว แล้วบันทึกเฟรมเป็น element ตั้งชื่อตามหน้าที่ (position lock, steering-wheel lock) [A15.L05 t=01:44] [A15.L05 t=02:24]
13. แยก prompt ที่แน่นเกิน, ล็อก blocking ด้วยช็อตหน้าตรงเรียบๆ ก่อน, แก้การแสดงทีละตัวแปร, แก้ drift ด้วย reference ที่เจาะจงขึ้น [A15.L06 t=00:00] [A15.L07 t=01:57] [A15.L08 t=00:46] [A15.L08 t=01:21]
14. ท่าที่ยาก ให้วาด diagram หรือทำเครื่องหมายบนภาพ location และถ่ายกลางฉาก (บทสนทนา) ก่อน เพื่อให้กำหนดขอบทั้งสองข้าง [A15.L10 t=00:11] [A15.L10 t=01:22]
15. ประกอบหนัง แล้วแก้ปัญหา geography และช่องว่างของเรื่องที่เห็นเฉพาะตอนต่อกัน แล้ว audit ทั้งหนัง 5 รอบ (identity, vehicle, geography, blocking, story) [A15.L11 t=00:16] [A15.L11 article]

### กฎที่ใช้ซ้ำได้
- ทุกภาพที่กลับมาซ้ำต้องมี reference ที่อนุมัติหนึ่งอันและชื่อ `@` คงที่หนึ่งชื่อ ก่อนฉากใดจะใช้ [A15.L01 article]
- ทำตาราง dependency: แถวละหนึ่งภาพที่กลับมา มีชื่อ, reference และฉากที่ใช้; ประเภท = Product (รูปทรง, สี, badge, cabin), Character (หน้า, ชุด, variant), Prop (กุญแจ, ของปลอมตัว, หนังสือพิมพ์), Location (palette, geometry, clean plate) [A15.L01 article]
- ทำ product shot บนพื้นเทากลาง เพื่อวางเข้ากับพื้นหลังใดก็ได้ภายหลัง [A15.L01 t=02:19] [A15.L01 article]
- "Don't try to get everything out of one model": ให้แต่ละรอบ generate มีงานเดียว (Soul Cinema = การแสดง, edit = คืน identity) [A15.L02 t=01:48] [A15.L02 article]
- เมื่อ model เก่งคนละด้าน ให้เลือกตามลำดับความสำคัญ: Nano Banana Pro เก็บหน้าดีกว่า, Seedream เก็บผ้าดีกว่า → เลือก Nano Banana Pro [A15.L02 t=03:45]
- ถ้าหน้าใน close-up กับหน้าใน full-body ไม่ตรงกัน ให้ตัดหน้าออกจาก panel full-body ใน image editor แทนการ regenerate (ประหยัดเครดิต) [A15.L02 t=05:06] [A15.L02 t=05:22]
- ล็อก palette ด้วย Color Transfer จากภาพ vibe ที่อนุมัติ เพื่อให้ "the whole film looks like one film" [A15.L03 t=00:23] [A15.L03 article]
- ตัดสิน batch ระดับช็อต: เปลี่ยนคำถาม "ได้ไหม" เป็น "beat ไหนได้ เริ่มและจบตรงไหน" — คำตอบคือจุดตัด [A15.L03 t=01:39] [A15.L03 article]
- Cast ตามบทบาท ไม่ใช่แค่ความเสถียร: ปฏิเสธหน้าที่ใช้ได้แต่ดูเป็น villain หรือตัวประกอบ [A15.L04 t=00:23] [A15.L04 article]
- สร้าง location ที่มุม three-quarter ("really important for locations") [A15.L04 t=01:14] [A15.L10 t=00:00]
- "Clean your plate": ลบทุกอย่างที่ video model ทำพังได้ (ตัวหนังสือ, ของรก, รถ) ทีละรอบ edit และทดสอบใน motion [A15.L04 t=01:25] [A15.L04 t=01:46]
- จัดป้ายรายละเอียดพื้นหลัง safe / risky / unnecessary: เก็บ geometry ที่ช็อตต้องใช้, ทดสอบสิ่งที่ไม่แน่ใจ, ลบสิ่งที่ถ้าพังแล้วจะกวนสายตา [A15.L04 article]
- bridge การกระโดด geography ด้วยช็อตเดินทางที่แสดงระยะทาง ใน location แยกจากปลายทาง [A15.L05 t=00:14] [A15.L05 t=00:21]
- เฟรมจากวิดีโอเดียวกันเข้ากันเสมอ: ดึง still จากวิดีโอ statics อันเดียว แล้วตั้งชื่อตามหน้าที่ ไม่เก็บ screenshot ไร้ชื่อ [A15.L05 t=01:44] [A15.L05 t=02:24]
- ปิด prompt ยาวด้วย "If this is too much for one prompt, split it into two" ให้ Claude ตัดสินใจแบ่ง [A15.L06 t=00:00] [A15.L06 article]
- ใช้ประโยคทดสอบ: "I am keeping this because it supplies ___" [A15.L06 article]
- micro-acting แยกตัวละครออกจาก NPC: ใน mirror shot ให้สายตาลง, กระพริบช้าหนึ่งครั้ง, ตัดสินใจ, สายตากลับขึ้น ("that one second of doubt") [A15.L06 t=00:48] [A15.L06 article]
- เมื่อสถานะตัวละครเปลี่ยน (ถอดชุดปลอมตัวแล้ว) ให้เปลี่ยนไปใช้ reference hero ที่สะอาดตั้งแต่ช็อตนั้น [A15.L06 t=02:23] [A15.L06 article]
- "The tighter the frame, the less slop": ตัดไฟจราจรออกจากเฟรม, เลี่ยง wide FPV/aerial เหนือรถติด, ตัด overtake และรถหนาแน่น [A15.L07 t=00:49] [A15.L07 t=01:19]
- ล็อก blocking ก่อน: ช็อตแรกเป็นหน้าตรงเรียบๆ (คนขับหน้า, ผู้โดยสารหลัง, คาดเข็มขัดทั้งคู่) เพื่อไม่ให้ใครสลับที่นั่ง [A15.L07 t=01:57] [A15.L07 article]
- สร้าง sequence ใหม่รอบชิ้นที่รอดทุก take (รถพุ่งผ่าน กล้องสะเทือนจากลม) [A15.L07 t=03:19] [A15.L07 article]
- แก้การแสดงทีละตัวแปร: บอกสิ่งที่พลาดที่มองเห็นได้ + สถานะที่ต้องการ และคงทุกอย่างที่ทำงานแล้วไว้ [A15.L08 t=00:46] [A15.L08 article]
- แก้ drift ด้วย reference ที่เจาะจงขึ้น (screenshot พวงมาลัยจาก statics video เป็น `@car_wheel`) แทนการเปิด cabin ใหม่ [A15.L08 t=01:21] [A15.L08 article]
- การตัดประโยคให้สั้นลงเป็นการแก้การแสดงได้ ("Change what? No" → "Change? No") [A15.L08 t=01:57] [A15.L08 article]
- จำนวนช็อตต้องเขียนเป็นกฎแข็ง: "exactly 5 shots and 4 cuts, no extra inserts" [A15.L09 t=01:18]
- วัตถุที่ควบคุมไม่ได้ (หมวกปลิว) ให้ script เป็นการตกในจุดที่กำหนด [A15.L09 t=01:30]
- อนุมัติ blocking จาก beat ถัดไปย้อนกลับ: ทางเข้าที่ดีใช้ไม่ได้ถ้าทำให้ทางออกเป็นไปไม่ได้ [A15.L10 t=02:42]
- ตัดสิน clip เป็นลำดับ ไม่ใช่เดี่ยวๆ: "A generation can be visually successful and still fail the film" [A15.L11 t=00:16] [A15.L11 article]

### โครงสร้าง Prompt
- โครงหลักของ video prompt (จาก Seedance prompt-generator skill): `— REFERENCE DEFINITIONS —` บรรทัดละ `@element` + คำบรรยายสั้น + "character/vehicle/prop/location appearance only. Reference." → `— TECHNICAL BLOCK —` → `— PROMPT —` → SFX list [A15.L03 article] [A15.L03 frames t=01:35]
- TECHNICAL BLOCK ของฉากโชว์รูม: photoreal, 16:9, 12s, SFX only no music, 35mm Kodak 500T grain, light motif, NO CGI, NON-IP, "exactly seven shots and six cuts — no more, no fewer", จังหวะตัด, คุณภาพการแสดง, ภาษา/สำเนียง, micro-expression [A15.L03 article]
- PROMPT ระบุจำนวนช็อตซ้ำ แล้ว SHOT 1…SHOT N แต่ละช็อตมี framing, blocking (ซ้าย/ขวา), action, บทพูดในเครื่องหมายคำพูด, "Cut." — references นิยามครั้งเดียว ทุกช็อตอ้างแค่ tag [A15.L03 article]
- character sheet (driver): [3 panel บน canvas เดียว จากรูปที่แนบ ตีความเป็น <role>] + [replicate face 1:1 พร้อมรายการลักษณะที่ล็อก] + [การเปลี่ยนแปลงเดียวที่ชัด: clean-shaven] + [สีหน้า] + [ชุดพร้อม branding สมมุติ และ "no real brands/teams/sponsors"] + [LEFT rear headless / CENTER front headless / RIGHT face close-up] + [พื้นเทาเข้ม, softbox, contact shadow] + [photoreal 8K, NON-IP, 16:9] [A15.L02 article]
- คำขอ sheet ที่พิมพ์ให้ Claude: "Give me a prompt for an image where this character is a race car driver in his racing suit. Three panels on the right — a close-up of the face; in the center — full-body front view of the outfit; on the left — full-body rear view of the outfit, without the head. No copyright text on the clothing..." [A15.L02 frames t=00:30]
- face-swap: [Image 1 = base เก็บ composition/pose/props/แสง เปลี่ยนแค่หัว] + [Image 2 = identity source ใช้ close-up panel] + [keep-list 1:1] + [ปรับหน้าให้เข้ามุมกล้อง, การเอียงหัว, สีหน้า, แสง] + [match ทิศแสง, grade, grain, ความคม เพื่อรอยต่อคอ] + [คง aspect ratio เดิม] [A15.L02 article]
- prompt ภาพแชมป์ใน Soul Cinema (Claude เขียน) ใช้: identity 1:1 กับ close-up panel + ชุดเดิม + branding สมมุติ ("APEX GP", "VOLTRA", "KYRO FUEL") + framing + มุมกล้อง + action + อารมณ์ + background + lighting + "Photoreal, 8K ... 85mm lens ... NON-IP ... 3:4" [A15.L02 frames t=02:00] [A15.L02 frames t=02:02]
- ชุดปลอมตัว: [edit image_1 คง layout/ลำดับ panel/bg/แสง] + [หน้า 1:1] + [เปลี่ยนเฉพาะขนบนหน้า] + [ชุดใหม่ทุก panel ไม่มีแบรนด์] + [อุปกรณ์ใน face panel: แว่นสีอำพัน, หมวกน้ำตาล] + [NON-IP, no text, 16:9] [A15.L02 article]
- sheet ตัวละครรองจาก scratch ใน Soul Cinema: "3-view character sheet on neutral gray background — front full body, back full body, close-up ... no harsh shadows and no artificial studio light on the character at all." [A15.L02 frames t=04:30] [A15.L02 t=04:25]
- prompt location ละเอียด (ปั๊มน้ำมัน) ระบุมุมกล้อง (สูง ~4 เมตร), ช่วงเวลา, องค์ประกอบ, เลนส์ 35mm, deep focus และสัดส่วนสี "60% warm sun-bleached beige and asphalt grey, 30% teal sky and glass reflections, 10% red accents" [A15.L04 frames t=01:10]
- คำขอแบบภาษาธรรมดาให้ Claude: บอก beat, ท่าที่ต้องการ, ความรู้สึก, และ "10 seconds" แนบ 4 ภาพ (car sheet, girl sheet, plate, disguised hero) [A15.L04 frames t=02:05]
- reference definitions เพิ่ม guard ของ continuity: "he stays seated inside the car for the entire video, never exits" และ location "match this layout in every shot" [A15.L04 frames t=02:15]
- reference แบบ lock: `@car_wheel2` "use THIS exact steering wheel ... in every shot where the wheel is visible", `@image_1` "exact parked position and orientation lock ... the car sits precisely like this throughout the whole scene" [A15.L06 article]
- TECHNICAL BLOCK ของบทสนทนาเพิ่ม: "Accurate lip-sync on all dialogue", "All characters blink naturally", "Facial reactions perfectly synchronized with physical actions", "Precise eyelines" [A15.L06 article]
- อารมณ์ใน prompt ใช้การปรับด้วย negative ("NOT commanding, NOT dramatic") และระบุตำแหน่งกล้องต่อช็อต (มุมทแยงจากมุมผู้โดยสารหน้า, POV จากเบาะหลังเข้ากระจกมองหลัง "reflection holds ONLY @hero") [A15.L06 article]
- downtown drive: time-of-day override (2:00 PM, sun ~60°, 5500K, "absolutely no golden hour, no orange cast") + ระยะเวลาต่อ cut (แรก 3s ที่เหลือ ~4s) + clause กฎจราจรทั่วไป ("stays inside its own lanes ... never crossing the solid double line") + clause กระจกสะท้อนซ่อนคนขับ + CUT 1–4 แต่ละ cut มี camera move เดียว [A15.L07 article]
- การแสดง (ด่านเก็บเงิน): อารมณ์หลักแบบผสม ("intense engagement fused with sly irony"), ตำแหน่งที่อารมณ์อยู่บนหน้า ("living entirely in the eyes and brows"), รายการ negative ("absolutely no displeasure, no annoyance, no irritation, no sourness"), ระดับความเข้ม ("never tipping toward panic"), เหงื่อ "9/10" พร้อมสิ่งที่มองเห็น, และแบ่งบทพูดเป็นจังหวะ [A15.L08 article]
- คำขอ correction ให้ Claude: "Reduce the hero's smirk. Write the girl feeling anxiety from the speed, and have her deliver her line with suspicion and curiosity. And add t[he logo element...]" [A15.L08 frames t=00:55]
- คำขอ rewrite รวม fix ทั้งหมดในครั้งเดียว: ใช้ location ใหม่, เพิ่ม `@newspaper`, "Exactly 5 shots, no more, no fewer", สี่ช็อตแรกเร็ว ช็อตสุดท้ายยาวสุด [A15.L09 frames t=01:50]
- prop reference: "@newspaper: Classic daily broadsheet newspaper "THE DAILY OBSERVER" ... bold fictional headlines ... columns of unreadable body text — prop reference only" [A15.L09 frames t=01:55]
- diagram reference: "Motion diagram — the moving car (blue) ... movement and parking trajectory reference only, use ONLY the path of the moving car, ignore the parked cars drawn in the diagram, do not use for environment, style or vehicle design." [A15.L10 frames t=03:05]
- คำขอ 5A: "Write only the first shot of our scene - the drift-park from the @image1 diagram. And make sure none of the blue and red stripes from the [diagram show up]" [A15.L10 frames t=02:30]
- geography fix: ย่อหน้า "FIXED GEOGRAPHY FOR THE WHOLE SEQUENCE" ระบุประตู, ขอบถนน, ฝั่งถนน และทางเลือกที่ห้าม ("never through the left door, never through the front door") + ตำแหน่งกล้องเทียบกับรถ + eyeline เทียบกับเลนส์ [A15.L11 article]
- กล้องช็อตสุดท้าย: ยกขึ้นและเลื่อนซ้าย "only watching the car go, NOT following it" และให้น้ำหนักเวลา (สองช็อตแรกสั้น ช็อตสุดท้ายยาวสุด) [A15.L11 article]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Higgsfield Cinema Studio: New project, New folder ("Scene 1"), Elements panel (Uploads, Elements, Image Generations, Video Generations, Liked; "Create Element"); New Element dialog มีช่องชื่อ "car_sheet", "Add description", Category "Auto" [A15.L01 frames t=02:00] [A15.L01 frames t=02:35] [A15.L01 frames t=02:40]
- generation bar เริ่มต้น: "Seedance 2.0", "Auto", "1080p", duration (ดูเหมือน "8s"), count (ดูเหมือน "1/4"), "High", GENERATE (ราคาอ่านไม่ได้) [A15.L01 frames t=02:35]
- Seedream 5.0 Pro: ทำ driver sheet ("one of the best models for outfits especially when feeding in your own inputs"); รอบ edit เห็น 3:4, 2K, 4/4 [A15.L02 t=00:35] [A15.L02 frames t=02:25]
- Nano Banana Pro: ใช้ edit/face swap/disguise sheet; เห็น 3:4, chip คุณภาพ (ดูเหมือน 1K), toggle "Unlimited" [A15.L02 frames t=02:30] [A15.L02 t=03:45]
- Soul Cinema: "the most creative model on the site" แต่แนบ reference sheet ไม่ได้; bar = "Soul Cinema", "3:4" หรือ "16:9", "2k", "4/4", chip ไอคอนไม้กายสิทธิ์ "On" (ไม่มี label บอกหน้าที่), "Color transfer" (New), ช่อง "CHARACTER", GENERATE "10,000 free gens left" [A15.L02 t=01:48] [A15.L02 frames t=02:00] [A15.L04 frames t=01:03]
- Color Transfer อยู่ใน Image tab; dialog upload "Higgsfield files" มี "Upload from device" [A15.L03 t=00:23] [A15.L03 frames t=00:30]
- Claude (model chip อ่านว่า "Fable 5 High") + custom skill "Seedance prompt generator" (ไฟล์ .skill ให้ดาวน์โหลด) [A15.L03 t=01:17] [A15.L08 frames t=01:55]
- Seedance 2.0 ใช้กับวิดีโอทั้งหมด แนบ reference ได้ 4–7 ภาพ; @tags ไฮไลต์สีเขียวในช่อง prompt [A15.L03 frames t=01:35] [A15.L06 frames t=00:25]
- bar ของ Seedance ใน L09 (อ่านได้จาก hires): "Seedance 2.0", "Auto", "4k", "8s", "4/4", "High", chip ลำโพง "On", "Unlimited"; ปุ่ม GENERATE แสดง "832" ถูกขีดฆ่าและ "704" [A15.L09 frames t=00:32]
- ผู้สอนอ้างว่า "Cdance is currently the best image editor we have" เพราะทุกเฟรมของวิดีโอเดียวเข้ากัน [A15.L05 t=02:10]
- Seedream ใช้แก้ภาพ location (ลบสะพาน) สร้างมุมใหม่ `@airport12` [A15.L10 t=02:15]
- image editor ภายนอก (ไม่ระบุชื่อ) ใช้ลบหน้าและลบแถวบูธเกิน; diagram วาดด้วยมือ (ไม่ระบุเครื่องมือ) [A15.L02 t=05:17] [A15.L09 t=00:55] [A15.L10 t=00:16]
- settings ระดับ prompt ที่ใช้: 16:9 ทุกฉาก, 12s (โชว์รูม, บทสนทนาในรถ), 10s (ปั๊ม, ด่าน), 15s (driving bridge, downtown), 8s (ด่าน iteration 1), 13s (ปิดเรื่อง) [A15.L03 article] [A15.L05 frames t=00:50] [A15.L08 article] [A15.L09 frames t=00:32] [A15.L11 article]

### คำเตือนและ failure modes
- ไม่มีวินัย folder → หลังไม่กี่ร้อย generation จะหาอะไรไม่เจอ [A15.L01 t=02:08]
- reference edit ใน Seedream/Nano Banana Pro เก็บ identity ได้แต่ดู sloppy: หน้าเนียนเกิน, ท่าจัด, ฉากสะอาดเกินจริง [A15.L02 t=01:33] [A15.L02 article]
- ถ้าหนวดถูก generate เป็นหนวดจริง ช็อตลอกหนวดภายหลังจะไม่มีเหตุผล [A15.L02 t=03:36] [A15.L02 article]
- หน้าใน close-up กับ full-body ไม่ตรงกัน "will become an issue when we make the videos later" [A15.L02 t=05:06]
- batch แรกของฉากโชว์รูม "quite a few things still broke" — ต้องเตรียม stitch ไม่ใช่หวัง take เดียว [A15.L03 t=01:43]
- video model ทำพังกับตัวหนังสือที่ละลาย, ของรกพื้นหลัง, รถสุ่ม; รถไกลๆ กลายเป็นโคลนของรถแดง hero [A15.L04 t=01:32] [A15.L04 t=01:51]
- take ที่ได้ beat สำคัญอาจมีตอนจบเพี้ยน ต้องดูทั้ง take [A15.L04 t=02:23]
- การ "teleport" ระหว่าง location ทำให้คนดูสับสน; ใช้ plate ปลายทางเป็นช็อตเดินทางทำให้ montage พัง [A15.L05 t=00:04] [A15.L05 t=00:33]
- driving 4 take ใช้ได้ 1; aerial top-down เหนือรถติด "broke every single time" [A15.L05 t=00:53]
- ไฟจราจรผิดทุกครั้ง (แดงขณะรถวิ่ง หรือแดงเขียวพร้อมกัน) แก้ไม่ได้; FPV/aerial ทำให้รถข้ามเส้นทึบและลอยเลน [A15.L07 t=00:49] [A15.L07 t=01:00]
- highway FPV: drone ดิ่งตามแล้วรถ "loses its mind" และรถ 120 ดูเหมือน 60; match cut "Seedance has no idea what that is"; ตัวเลขบนหน้าปัดกลายเป็นโจ๊ก [A15.L07 t=02:57] [A15.L07 t=03:06] [A15.L07 t=03:15]
- ไม่มี logo reference model จะ "keeps inventing a new logo for the car"; แม้ล็อก logo แล้ว รูปทรงพวงมาลัยยังเปลี่ยนทุก generation [A15.L08 t=00:41] [A15.L08 t=01:12]
- การแก้เกิน (overcorrection) ลบคุณภาพที่ได้แล้ว (ลด smirk แล้วความสนุกหายหมด); การ rewrite กว้างๆ ทำให้ไม่รู้ว่าอะไรแก้ปัญหา [A15.L08 t=01:04] [A15.L08 article]
- iteration แรกของฉากด่าน "slop across the board": ตัวละคร teleport, แถวบูธเกินโผล่, หนังสือพิมพ์และมือเป็นโจ๊ก [A15.L09 t=00:34]
- model ไม่ทำตามจำนวนช็อต (ขอ 5 ได้ 6, 7) ถ้าไม่เขียนเป็นกฎแข็ง; วัตถุหลวม (หมวก) ปลิวแล้วหายถ้าไม่ script [A15.L09 t=01:18] [A15.L09 t=01:30]
- prompt เดียวทั้งฉากสนามบิน รถหยุดคนละที่ทุกครั้ง (ผิดเลน, ระยะผิด, ครั้งหนึ่งกลางถนน) [A15.L10 t=00:58]
- เส้นใน diagram อาจหลุดเข้าวิดีโอถ้าไม่ห้าม; จอดระหว่างรถสองคันบังคับให้ต้องถอยออก ทำให้ขับออกไม่สวย [A15.L10 t=02:29] [A15.L10 t=02:42]
- ช็อตปิดดูดีเดี่ยวๆ แต่บน timeline ผู้หญิงลงผิดประตูเข้าไปในรถวิ่ง และรถจอดผิดฝั่ง; ทางออกถูกต้องแต่เรื่องยังขาด (hero หายจากหนังตัวเอง) [A15.L11 t=00:19] [A15.L11 t=00:36]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- การวาง prompt ที่มีชื่อ element กลับใน Higgsfield ทำให้แนบ element อัตโนมัติ (article แค่บอกเป็นนัย) [A15.L01 t=02:45]
- prompt ที่พิมพ์ให้ Claude จริงทุกฉาก เช่น คำขอภาพแชมป์ "It should be a champion's photo, joyful, medium shot." [A15.L02 frames t=01:15] [A15.L02 t=01:04]
- prompt ภาพแชมป์ตัวเต็มที่ Claude เขียนและ settings ของ Soul Cinema [A15.L02 frames t=02:00]
- การเทียบ disguise 2 แถว Seedream 5.0 Pro กับ 2 แถว Nano Banana Pro และคำตัดสิน "kept the face better / kept the fabric better" [A15.L02 frames t=03:45]
- prompt location ปั๊มน้ำมันที่มีสัดส่วนสี 60/30/10 [A15.L04 frames t=01:10]
- ผลจาก "super basic prompt" รอบแรกเป็นรถ rally บนทางดิน ไม่ใช่ปั๊ม — ใช้แค่หา vibe [A15.L04 frames t=01:05]
- คำขอ driving bridge แบบ 3 ช็อต/2 cut 15s ("EXACTLY THREE SHOTS, ONLY TWO CUTS ... Car only — no driver visible") [A15.L05 frames t=00:45] [A15.L05 frames t=00:50]
- กราฟิก "PROJECT TIMELINE" ที่แสดงช่องว่างระหว่าง S1 กับ S2 และโตขึ้นตามฉาก [A15.L05 frames t=00:00] [A15.L06 frames t=02:50]
- คำขอ 6 มุม cabin รวม "a wheel-hub POV looking back at the driver" และคำขอ highway 4 ช็อตที่มี "our car at 120 ... traffic doing 60" [A15.L07 frames t=01:50] [A15.L07 frames t=02:45]
- caption "TIGHTER THE FRAME = LESS SLOPP" (ตัดกลางแอนิเมชัน) [A15.L07 frames t=01:23]
- บทพูด iteration 1 ของฉากด่าน ("Are you serious? Change what? No!" / "Me either.") มีเฉพาะในเสียง [A15.L08 t=00:22]
- ราคาบนปุ่ม GENERATE ของ Seedance 4k 8s 4/4: "832" ขีดฆ่า → "704" [A15.L09 frames t=00:32]
- element `@newspaper` "THE DAILY OBSERVER" พาดหัว "CITY PREPARES FOR SUMMER MARATHON" [A15.L09 frames t=01:15]
- diagram วาดมือ (เส้น cyan โค้งเข้าช่องว่างระหว่างสี่เหลี่ยมแดง) และ `@position` ที่ขีดแดงจุดจอด [A15.L10 frames t=00:15] [A15.L10 frames t=01:35]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- L09 และ L10 เป็น VERIFIED_GAP: สำเนา article ถูกบล็อก (chunk ถูก safety classifier บล็อก) จึงไม่มี article ของ L09 และหัว article ของ L10; เนื้อหาของสองบทนี้มาจาก transcript + frames เท่านั้น ห้ามไปดึง article [A15.L09 t=00:00] [A15.L10 t=00:00]
- ชื่อบท L09/L10 ไม่ได้ถูกบันทึกจาก course file; ผู้ audit ได้หัวข้อจาก browser ว่า L09 "Stabilize a comic set piece" และ L10 "Block the finale backward" (L10 ตรงกับ slug ในชื่อไฟล์ asset) [A15.L09 t=00:00] [A15.L10 t=00:00]
- สำหรับ L10 ยังมี "ท้าย article" หลัง GAP ใน course file (prompt block A "Lock the goodbye dialogue" 10s 4 ช็อต/3 cut และ block B "Clear the drift parking area" 4s ช็อตเดียว) ซึ่ง note ติด tag แยกและผู้ audit ตรวจว่าตรง; course wrap-up บอกว่า "intentionally not used" ขณะที่ note บอกว่าเพิ่มในรอบหลัง — ขัดกันเอง ไฟล์นี้จึงไม่ใช้ส่วนนั้นเป็นแหล่งหลัก (ให้ merge step ตัดสิน) [A15.L10 article-tail]
- prompt ทางการของ L08 ถูกตัดกลางประโยคโดย GAP marker (จบที่ "A soft breathy voice colo") จึงมีแค่ครึ่งแรก [A15.L08 article]
- L08: article บอกว่า prompt ทางการยังใช้บทพูดเก่า แต่ตัดต่อจริงใช้ "Change? No." [A15.L08 article] [A15.L08 t=01:57]
- L02: prompt ใน article บรรยายหนวดธรรมชาติ แต่เสียงขอหนวด "that looks like a fake stick-on" [A15.L02 article] [A15.L02 t=03:29]
- L02: เสียงขอภาพแชมป์ "medium shot" แต่ prompt ที่ Claude เขียนเป็น tight vertical close-up มุมต่ำ [A15.L02 t=01:15] [A15.L02 frames t=02:00]
- L02: ไม่บอกว่า face-swap รุ่นไหนชนะ (Seedream vs Nano Banana Pro) [A15.L02 frames t=02:35]
- L06: article ledger บอก "four different shots" แต่ทั้งฉากใช้ take มากกว่านั้น [A15.L06 t=00:31] [A15.L06 article]
- course wrap-up บอกว่าไม่มีราคาเครดิต แต่เฟรม L09 เห็นตัวเลข 832→704 บนปุ่ม GENERATE และ L02 เห็น "10,000 free gens left" — ไม่มีการพูดถึงต้นทุนรวม [A15.L09 frames t=00:32] [A15.L02 frames t=02:00]
- ค่า Seedance (resolution, duration, count) ส่วนใหญ่อ่านไม่ได้ที่ความละเอียด contact sheet ยกเว้นเฟรม L09 [A15.L03 frames t=01:35] [A15.L09 frames t=00:32]
- ไม่แน่ชัดว่า "Fable 5" เป็นชื่อ model Claude จริงหรืออ่าน chip ผิด [A15.L02 frames t=00:05]
- เนื้อหาของ skill "Seedance prompt generator" ไม่ปรากฏ เห็นแค่รูปแบบ output [A15.L03 t=01:17]
- ชื่อ "Mr. Magic" และประโยค "Just a deal doing his things" น่าจะเป็นการถอดเสียงผิด (ตรวจ hires แล้วยังไม่ชัด) [A15.L01 t=00:03] [A15.L09 t=02:03]
- คำขอ downtown 6 ช็อตแรกที่ล้มเหลวอ่านไม่ได้บนจอ [A15.L07 frames t=00:40]
- เฟรมพวงมาลัย close-up ที่พูดถึงใน L05 ไม่อยู่ใน tile ที่สุ่ม [A15.L05 t=02:24]

### เทียบกับ v1
- เพิ่ม: โครง video prompt 3 ส่วน REFERENCE DEFINITIONS / TECHNICAL BLOCK / PROMPT จาก Seedance prompt-generator skill [A15.L03 article]
- เพิ่ม: การใช้ชื่อ `@element` ร่วมกับ Claude และการแนบอัตโนมัติเมื่อวาง prompt [A15.L01 t=02:31]
- เพิ่ม: models ที่ใช้จริงต่องาน (Seedream 5.0 Pro, Nano Banana Pro, Soul Cinema, Seedance 2.0) และ settings ที่อ่านได้ [A15.L02 t=00:35] [A15.L09 frames t=00:32]
- เพิ่ม: เทคนิค statics video เพื่อดึง still ที่เข้ากัน และ reference แบบ lock (position, steering wheel) [A15.L05 t=01:44] [A15.L06 article]
- เพิ่ม: failure classes ของ driving (ไฟจราจร, FPV, overtake, match cut, หน้าปัด) และกฎ "tighter the frame" [A15.L07 t=00:49] [A15.L07 t=03:06]
- เพิ่ม: เนื้อหา L09/L10 จาก transcript + frames (fix 4 ข้อของฉากด่าน, diagram + `@position`, แบ่ง 5A/5B/5C) [A15.L09 t=00:55] [A15.L10 t=01:31]
- เพิ่ม: audit ทั้งหนัง 5 รอบ (identity, vehicle, geography, blocking, story) [A15.L11 article]
- แก้: ขั้นตอนตัวละครต้องแยก "การแสดง" (Soul Cinema) ออกจาก "identity" (face-swap edit) ไม่ใช่ทำใน model เดียว [A15.L02 t=01:48]
- เหมือนเดิม: ตาราง dependency ของ assets และโฟลเดอร์ต่อฉาก [A15.L01 article]
- เหมือนเดิม: bridge ช็อตเดินทางแทนการ teleport และ still ภายในจากวิดีโอคงที่ชุดเดียว [A15.L05 t=00:14] [A15.L05 t=01:44]
- เหมือนเดิม: เปลี่ยน reference ให้ตรงสถานะหลังถอดชุดปลอมตัว และพวงมาลัยต้องมี reference รูปทรงเฉพาะ [A15.L06 t=02:23] [A15.L08 t=01:21]
- เหมือนเดิม: ฉากด่านแก้ด้วย plate สะอาด, prop หนังสือพิมพ์ และ script จุดตกของหมวก — v2 ยืนยันจาก transcript + frames เท่านั้น [A15.L09 t=00:55] [A15.L09 t=01:30]
- เหมือนเดิม: ฉากจบวางกลางฉากก่อน และแก้จุดจอดที่มีรถขวางก่อนเลือกภาพสวย — v2 ยืนยันจาก transcript + frames [A15.L10 t=01:22] [A15.L10 t=02:42]
- แก้: v1 ไม่ได้บอกว่า L09/L10 ไม่มี article; v2 ระบุว่าเนื้อหาสองบทนี้มาจาก transcript + frames เท่านั้น [A15.L09 t=00:00] [A15.L10 t=00:00]

## A16 Direct AI fight scenes through controlled iteration

### ภาพรวมและผลลัพธ์
- ตัวอย่างหลักของคอร์สคือฉากต่อสู้กลางทุ่งหิมะในหมอก: hero Roko, monster หน้ากะโหลกสูง 4 เมตร, กองทัพ samurai และการแปลงร่างของ Roko เป็นอัศวินคริสตัล สร้างทีละช็อตเป็น "beats" [A16.L01 t=00:00] [A16.L01 t=02:31]
- คอร์สเปิดด้วยฉากที่เสร็จแล้ว แล้วอ่านย้อนกลับเป็นปัญหา continuity ก่อนสร้าง motion ใดๆ [A16.L01 article]
- วิดีโอเพิ่มชั้นการเขียน prompt ที่ article ไม่มี: Claude skill "higgsfield-cinematic-seedance-skill" ที่แปลงหน้า script + assets ที่ตั้งชื่อ เป็น prompt Seedance 4 ส่วน [A16.L01 t=01:29] [A16.L01 frames t=01:27]
- หลักการกลางของคอร์ส: แทนคำบอกความเข้ม ("huge", "dramatic") ด้วยพื้นที่และเวลาที่สังเกตได้ (เมตร, วินาที, เซนติเมตร, องศา) [A16.L03 t=02:44] [A16.L03 article]
- ผลลัพธ์: ช็อตที่ใช้จริงใน final cut แต่ละ beat และ playbook "find flaw → Claude fixes" [A16.L02 frames t=04:10] [A16.L05 t=02:15]

### Workflow ทีละขั้น
1. ดูฉากที่เสร็จแล้วหนึ่งรอบ ติดตามแค่ 3 อย่าง: ใครครองเฟรม, ภัยมาจากทางไหน, ช็อตถัดไปหันทางไหน [A16.L01 article]
2. ล็อก assets บน Higgsfield Canvas ก่อน motion: hero sheet + sheet สถานะเฉพาะฉาก (หมดแรง, เจ็บปวด), monster, crystal sword, กองทัพศัตรู, ร่างแปลง (@Roko_warrior) [A16.L01 t=02:12] [A16.L01 t=02:21] [A16.L01 frames t=02:17]
3. ทำ location เป็นภาพเดียวสองฝั่ง "FRONT VIEW" (ต้นไม้สีแดงเลือด) และ "BACK VIEW" ว่างเปล่า ภายในกำแพงหมอก [A16.L01 t=02:46] [A16.L01 frames t=02:44]
4. ติดตั้ง skill ใน Claude: Customize > Skills > "+" > upload (~30 วินาที) [A16.L01 t=01:42]
5. ให้ Claude หน้า script + ภาพ reference พร้อมชื่อ (เช่น "@Roko - the hero @Monster - the villian ...") แล้วบรรยายแต่ละ sequence สั้นๆ ตามที่นึกภาพ [A16.L01 t=01:53] [A16.L01 frames t=01:55]
6. Claude ขยายเป็น prompt มี @tag พร้อมสรุปรูปร่างสั้น, พิกัดเป็นเมตร, การเคลื่อนไหวเป็นวินาที, positive constraints + blocks style/sky/fog/physics/continuity/acting, camera block และ audio line ที่มีเวลา [A16.L01 t=01:29] [A16.L02 t=00:38]
7. ใน Cinema Studio เพิ่ม assets เป็น elements ก่อน แล้ววาง prompt (tags เข้าที่เอง) ตั้ง Seedance 2.0, 15s, batch 4, High แล้ว generate [A16.L02 t=01:20] [A16.L02 t=01:32]
8. ตรวจ batch: พังซ้ำ = ปัญหา brief/reference; พังครั้งเดียวหลัง movement ใช้ได้แล้ว = reroll [A16.L02 t=01:32] [A16.L04 t=01:23]
9. บอกสิ่งที่พังเป็นภาษาธรรมดาให้ Claude สร้าง prompt ใหม่ โดยเปลี่ยนเฉพาะระดับที่พัง (asset, action, camera, roll) [A16.L02 t=02:48] [A16.L02 t=04:01]
10. ช็อตใหญ่ แทนคำบอกความเข้มด้วยตัวเลข: ระยะมองเห็นในหมอก, ชั้นความลึก, ขั้น action 0.5 วินาที, ระยะ/ความสูงกล้องตอนเริ่ม-จบ, ระยะเวลาการแปลงร่าง, ช่องว่างใบมีดเป็น cm [A16.L03 t=00:57] [A16.L03 t=02:44] [A16.L04 t=00:40]
11. แทนคำปฏิเสธด้วยภาพเชิงบวก และแตก long take เป็น multi-shot ที่แต่ละช็อตมีเลนส์และหน้าที่ของตัวเอง [A16.L05 t=00:57] [A16.L05 t=01:11]
12. เมื่อ prompt ลงตัวแล้วให้รัน batch ใหญ่ แล้วตัดชิ้นที่ดีที่สุดจากหลาย generation มาประกอบ [A16.L03 t=01:59] [A16.L03 t=03:32] [A16.L05 t=02:10]

### กฎที่ใช้ซ้ำได้
- ทุกคนที่กลับมา, กองทัพ และแต่ละทิศกล้อง ต้องมี reference ที่อนุมัติหนึ่งอันก่อน motion [A16.L01 article]
- ให้ reference แต่ละอันมีหน้าที่ continuity เดียวที่ทดสอบได้ (หน้า/ชุด/ความเหนื่อย; scale/หัวกะโหลก/แขนใบมีด; ลุคกองทัพ; landmark หน้า + ทิศภัย; มุมย้อน; หมอก = ความลึกที่มีขอบ) [A16.L01 article]
- ทดสอบก่อนเริ่ม: "if the camera turned 180 degrees now, which approved reference describes the frame?" ถ้าไม่มี แปลว่า geography ยังไม่ล็อก [A16.L01 article]
- เก็บกองทัพเป็น reference เดียวตอน preflight; แยก class เมื่อ batch แสดง silhouette โคลนกันแล้วเท่านั้น [A16.L01 article] [A16.L02 t=02:12]
- Positive constraints ดีกว่าคำปฏิเสธ: "telling the model what not to do rarely works" — เปลี่ยนข้อห้ามเป็นคำสั่งที่มองเห็นได้ [A16.L02 t=03:19] [A16.L05 t=00:57]
- generate ทีละ 4 เสมอ เพื่อแยก glitch สุ่มออกจากปัญหาของ prompt [A16.L02 t=01:32] [A16.L02 article]
- ระบุสิ่งที่ทำงานแล้ว (identity, weather, direction) และเปลี่ยนเฉพาะตัวแปรที่พัง; อย่าให้รางวัลผลแย่ด้วยการเขียนใหม่ทั้งหมด [A16.L02 article] [A16.L04 article]
- ความเร็วกล้องต้องชัด: ไม่ใช่ "fast" แต่ "three times faster than a typical cinematic dolly pull" [A16.L02 t=01:04]
- กองทัพดูใหญ่จากการซ้อนชั้น (ทหารชัดคนเดียวหน้าสุด, ฝูงหนาแน่นตรงกลาง, เงาในหมอก) ไม่ใช่จำนวนตัวประกอบ; ทหาร ~40 คนที่อ่านชัดก็พอ [A16.L03 t=01:18] [A16.L03 article]
- ใช้หมอก (มองเห็น ~20 m) เป็น "the cheapest cleanup you'll ever do" ซ่อน glitch พื้นหลังในฉากใหญ่ [A16.L03 t=00:57]
- เขียน action ทีละวินาที (ขั้นละ 0.5 วินาที) เพื่อไม่ให้ model รีบหรือข้ามขั้น [A16.L03 t=01:34]
- จบ beat ใหญ่ด้วยการเปลี่ยนสถานะพร้อมกันแล้ว freeze ("free cliffhanger for the edit") [A16.L03 t=01:49]
- เขียน camera move เป็นเมตรและองศา ไม่ใช่คำคุณศัพท์ ("models prefer arithmetic over vague words") [A16.L03 t=02:44] [A16.L03 frames t=02:55]
- การแปลงร่างต้องเป็น snap ที่จับเวลา (~0.4 วินาที) และเปรียบเป็น "a weapon deploying, not a magic sequence" [A16.L03 t=02:59] [A16.L03 article]
- อ่าน action ใหญ่ผ่าน 5 ตัวควบคุม: start, path, state change, duration, end [A16.L03 article]
- match cut: เขียนว่าท่าตอนจบช็อต 1 "EXACTLY match" ตอนเริ่มช็อต 2; ความตึงเป็นเซนติเมตร; การปะทะเป็นมุม (vertical chop vs diagonal parry) + กฎวัสดุ "crystal always beats steel" [A16.L04 t=00:24] [A16.L04 t=00:40] [A16.L04 t=00:53]
- ระบุระดับของ defect (pose continuity, temporal continuity, material behavior, image quality) ก่อนตัดสินใจ rewrite หรือ reroll — "almost right" ไม่ใช่การวินิจฉัย [A16.L04 article]
- แตก fight เป็น hard cuts ที่เลนส์ต่างกัน (50mm orbit, 24mm low, 85mm close-up, 35mm wide) เพราะ long take ที่ลอยตามหลังดูเหมือนวิดีโอเกม [A16.L05 t=01:11] [A16.L05 t=01:24]
- ทดสอบ coverage: ปิดคำนาม action แล้วอ่านเฉพาะแผนกล้อง; ถ้าทุก setup ให้ข้อมูลเดียวกัน ก็ยังเป็นมุมเกมเดียวที่แค่ตัดแต่งหน้า [A16.L05 article]

### โครงสร้าง Prompt
- โครง skill 4 ส่วน: asset anchors (tags), พิกัดเป็นเมตร, การเคลื่อนไหวเป็นวินาที, กฎเข้มเพื่อกัน hallucination [A16.L01 t=01:29]
- ลำดับการเขียนตาม skill: "Separate: subject motion, camera motion, environmental motion, emotional acting, optics, lighting, audio."; สิ่งสำคัญด้าน space มาก่อน style, กล้องมาก่อน mood, เวลาบทพูดมาก่อนน้ำเสียง [A16.L01 frames t=01:35]
- ตัวอย่าง constraint ใน skill: ดี = "Exactly three named characters appear in the alley: @..., @... and @..." / อ่อน = "No extra people." [A16.L01 frames t=01:30]
- input ให้ Claude: `@<Tag> - <role>` ต่อ asset ที่แนบ [A16.L01 frames t=01:55]
- brief สั้นของ opening oner: `Scene <n>, sequence <n> — <shot role>. One continuous <camera type> take, <duration>, no cuts. <@A action at landmark>, <camera path> as <@B event>, pass <@C> on the way, and end <final composition>. <Positive staging constraint>.` [A16.L02 cue cue-opening-shot-brief]
- character block ที่ขยายแล้ว: `@roko [image1] — 20yo male, lean athletic build ... Character appearance only.`; `@crystal_sword ... Hilt fused directly to wielder's right crystal hand ... Element reference only.`; `@Monster ... In this shot the LEFT clawed hand is EMPTY` [A16.L02 frames t=00:40]
- environment blocks: `STYLE PREFIX:` (ทุ่งหิมะไม่ว่างเปล่า, texture แบบญี่ปุ่น, location "for STYLE/ELEMENT reference only — do NOT copy the close-up framing") + `Sky:` + `Fog:` + snow physics + `Physics:` + `Continuity:` + `Weather:` + `Acting: Hollywood` [A16.L02 frames t=00:50]
- geometry เป็นเมตร: "@roko stands 10 meters from the tree ... The 10-meter gap between them is the playing field." [A16.L02 frames t=01:05]
- camera block: `ONE CONTINUOUS TAKE, NO CUTS, NO EDITS.` FPV racing drone "GoPro-style action cam, ultra-wide ~14-18mm ... micro-vibrations from rotors", ถอยหลังเป็นเส้นตรง 15s, สูง ~50cm จากหิมะ (worm's-eye) [A16.L02 frames t=01:05]
- กฎพฤติกรรมฝูงชน: "Samurai movements are NEVER smooth. Every motion is JERKY..." และการโผล่ 2 ระลอกผูกกับตำแหน่งกล้อง (8-15 ตัวก่อน, หลายร้อยเมื่อ drone ผ่าน @roko) [A16.L02 frames t=01:22]
- audio line มีหน้าต่างเวลาและห้าม subtitle: `@Monster (Japanese, full-throated battle scream — heard during the first ~3-4 seconds of the take): "RAAAAAAA — IZAAAAA!!!" [... NO subtitle displayed.]` [A16.L02 frames t=01:22]
- โครงคำขอแก้ให้ Claude: `<observed defect>. Change <one variable> — <positive visible instruction>. And change <second variable> — instead of <old>, <new framing>.` [A16.L02 frames t=03:45]
- brief กองทัพ: `Next sequence — <relation> at full scale. One continuous take, <duration>. Open <framing> on <one subject + action>, <camera path 1> as <crowd event>, then <camera path 2> into <destination> — which stays <state>, <who is absent>. End with <synchronized action> at once, <visual trigger> — and hold the freeze.` [A16.L03 cue cue-army-scale-brief]
- depth block: "PHASE 1 — 0–4s ... FOREGROUND (sharp focus, the accent): ONE specific @samurais ... MIDDLE DISTANCE (~5-15m back): 8-15 other samurai ... FAR DISTANCE (~20-40m back): more samurai silhouettes ... fading toward the fog wall." [A16.L03 frames t=01:23]
- rise timeline: `<t0–t1>s: <หนึ่งขั้นของร่างกายที่มองเห็น>; Behind him: <สถานะฝูงชน>` ซ้ำทุก 0.5 วินาที [A16.L03 frames t=01:40]
- brief การแปลงร่าง: `Next shot — <name>. One <camera move> around <@subject>, no cuts. Start about <d1> m out and <h1> m up, then <path> while coming in closer — end at <d2> m and <h2> m high. Mid-arc <state change> — <speed limit> — and he becomes <@asset tag>. It should feel like <mechanical analogy>, not <cliche>. ...` [A16.L03 cue cue-transformation-brief]
- camera orbit ที่ขยายแล้ว: เริ่ม ~8 m สูง ~3 m → โค้ง ~180° เข้าใกล้ ~4 m ต่ำลง ~2 m, เลนส์ ~24-35mm, Roko อยู่กลางเฟรมตลอด [A16.L03 frames t=02:47]
- transformation block: "SINGLE SHARP SNAP ... (~0.4 seconds, faster than a normal blink) ... NOT a slow wave growing limb by limb ... NO particles, NO magical light burst" + พฤติกรรม samurai ระหว่างช็อต (ล้อมแต่ยังไม่บุกจน Monster พูด "Korose") [A16.L03 frames t=03:02]
- location block: "@Wasteland — ... Fog eats everything past ~15-25m into pure white-grey nothing ... One Japanese tree visible in deep background through fog as a ghostly silhouette" [A16.L03 frames t=01:03]
- brief match cut: `Write a prompt for next sequence. <Beat name>. Two shots, one frame-perfect match cut: <shot-1 framing + action> — freeze just before <contact> — then cut to <slow-motion camera move> around that frozen moment, and ramp back to real time as <material event>. Keep <background staging> with exact gaps.` [A16.L04 cue cue-match-cut-brief]
- timeline ช่องว่างใบมีด: "~5-8cm apart" → "9.0–11.0s ... ~2-3cm" → "11.0–13.0s ... ~1cm" → "13.0–13.5s: SPEED RAMP" → "13.5–14.0s: AT REAL-TIME SPEED ... RING." [A16.L04 frames t=00:40]
- กฎวัสดุในช็อต: "the odachi metal blade meets @crystal_sword and PARTIALLY SHATTERS (the crystal is harder than steel). Real metal sparks fly. @samurais2 jolted back from impact. NO videogame energy effects." [A16.L04 frames t=00:53]
- คำขอ rewrite ให้หลุดลุคเกม: `Re-write the fight. <@hero> <situation>, <enemy direction>, <action verbs — signature effect>. <Weight/feel adjectives>. Remove every '<negation phrase>' line and split it into <n> shots: <shot 1> — <shot 2> — <shot 3> — <shot 4>.` [A16.L05 cue cue-cinematic-coverage-brief]
- เปลี่ยนภาษาปฏิเสธเป็นคำถามเชิงบวก: Not a game → กล้องอยู่ไหนและช็อตนี้มีไว้ทำไม; No cheap effects → texture/แสง/เศษ/contact แบบไหน; Not weightless → อะไรงอ, หยุด, สะท้อนกลับ [A16.L05 article]

### Models และ settings (ตามที่เห็นในคอร์ส ณ วันที่บันทึก — ราคา/เครดิตอาจเปลี่ยน)
- Seedance 2.0 / "Higgsfield Seedance" สำหรับวิดีโอทั้งหมด; ผู้สอนบอกว่า render 4K และถือพื้นหลังได้ดีขึ้นมาก [A16.L01 frames t=01:30] [A16.L03 t=01:08]
- Cinema Studio (opening oner): "Seedance 2.0", "16:9", "1080p", "15s", "4/4", "High", audio "On", chip "Unlim..."; ปุ่ม Generate แสดง "720" ขีดฆ่าเป็น "540"; แนบ reference 5 ภาพ; project path ".../BEAT 1" [A16.L02 frames t=01:22] [A16.L02 t=01:20]
- Cinema Studio (fight เวอร์ชันลุคเกม): "Seedance 2.0", "Auto", "4K", "15s", "1/4", "High", audio "On"; Generate "390" ขีดฆ่าเป็น "330"; แนบ reference 6 ภาพ [A16.L05 frames t=00:10]
- Claude desktop + custom skill "higgsfield-cinematic-seedance-skill"; model selector อ่านว่า "Fable 5 High" [A16.L01 frames t=01:55] [A16.L02 frames t=03:43] [A16.L05 frames t=01:35]
- Higgsfield Canvas เป็นบอร์ดเก็บ reference ทั้งหมด [A16.L01 t=02:16]
- asset tags บนบอร์ด: @Roko, @monster, @crystal_sword, @samurais, @location_jungle3, @samurais2, @samurais3, @Roko_warrior [A16.L01 frames t=02:17]
- prompt match cut ระบุ "ACTION (2 SHOTs, frame-perfect match cut, 15s total)" และ hard cut "at exactly 5.0s"; บทนี้ไม่มี settings bar ให้เห็น [A16.L04 frames t=00:26]
- skill คำนวณตัวเลขความแม่น (cm/วินาที) ให้เอง ไม่ต้องคิดเอง [A16.L04 t=00:48]

### คำเตือนและ failure modes
- ทีมใช้เวลาหลายวันเขียนช็อตเดิมใหม่ "until the model stopped breaking" — skill มีไว้เพื่อเลี่ยงสิ่งนี้ [A16.L01 t=01:17]
- ไม่มีภาพมุมย้อน AI จะเดาสิ่งที่อยู่หลังตัวละคร และ batch จะ drift [A16.L01 t=02:53] [A16.L01 article]
- กฎใน skill: Seedance ไม่ทำตาม FOV เพราะ prompt ใส่ตัวเลข แต่อนุมาน FOV จากเนื้อหา; ถ้า FOV ขัดเนื้อหา ให้แก้การออกแบบช็อต [A16.L01 frames t=01:35]
- กฎใน skill: ไม่ต้องมี block NEGATIVE CONSTRAINTS แยก เว้นผู้ใช้ขอ — เปลี่ยนข้อห้ามสำคัญเป็น positive constraint ใน section ที่เกี่ยวข้อง [A16.L01 frames t=01:30]
- batch แรกของ opening oner ล้ม: การโผล่ดูเหมือน glitch, กองทัพเป็นโคลน, กล้องแบนทำให้ตัวละครเป็นจุดในหมอก [A16.L02 t=02:00] [A16.L02 article]
- "no held objects, no handle" ยังได้มือถือดาบ — negative prompting ผิดทาง; แขนนี้ "took way too many tries to get right" [A16.L02 t=03:10] [A16.L02 t=03:19]
- ฉากฝูงชนขนาดใหญ่ AI จะ glitch ที่พื้นหลัง; ไม่ล็อกเวลา model จะรีบหรือข้ามขั้น [A16.L03 t=01:02] [A16.L03 t=01:45]
- การแปลงร่างที่ปล่อยให้ช้า = "glowing anime power-up every single time" [A16.L03 t=03:10]
- ช็อตที่ร่างเป็น start point, path, timed change, end frame ไม่ได้ ก็วัดไม่พอจะวินิจฉัย [A16.L03 article]
- ถ้าไม่สะกด match cut ให้ชัด AI จะถือว่า cut เป็นฉากใหม่และทิ้ง pose [A16.L04 t=00:35]
- bullet time เป็นหนึ่งในช็อตที่ยากที่สุด (physics, สองร่างเคลื่อน, time dilation, กล้อง 180°) แต่ความซับซ้อนอย่างเดียวไม่ใช่เหตุผลที่จะ rewrite [A16.L04 t=01:06] [A16.L04 article]
- การแยก prompt พังออกจาก roll ไม่ดี "is how you save credits" [A16.L04 t=01:34]
- กับดักคำปฏิเสธ: เขียน "not a game, no CGI" ซ้ำเป็นสิบครั้งยังได้ลุคเกม เพราะ model ไม่สน "not" แต่เห็นคำว่า "game" ซ้ำ; "AI gives you what you ask for, not what you ban" [A16.L05 t=00:36] [A16.L05 t=01:00]
- กล้องต่อเนื่องที่ลอยตามหลัง hero อ่านเป็นเกมบุคคลที่สาม — "real movies don't shoot like that" [A16.L05 t=00:46]

### เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)
- workflow ของ Claude skill ทั้งหมด (ชื่อ skill, โครง 4 ส่วน, path ติดตั้ง, input = หน้า script + assets ที่ตั้งชื่อ) ไม่อยู่ใน article [A16.L01 t=01:17]
- กฎ reference ของ skill: ใช้เฉพาะ reference ที่ผู้ใช้ให้, ทุก @tag ต้องอยู่ใน ACTIVE REFERENCES, ห้าม tag เก่า/ไม่ใช้/ฉากก่อน/แต่งขึ้น; ใช้ OUTPUT SETTINGS เฉพาะเมื่อผู้ใช้ขอหรือ UI ไม่คุม [A16.L01 frames t=01:30] [A16.L01 frames t=01:40]
- settings ของ Cinema Studio และตัวเลขบนปุ่ม Generate (720→540, 390→330) [A16.L02 frames t=01:22] [A16.L05 frames t=00:10]
- prompt ที่ขยายแล้วบนจอ (character blocks, STYLE PREFIX, camera block FPV, กฎ samurai กระตุก, การโผล่ 2 ระลอก, เสียงร้องรบ) [A16.L02 frames t=00:40] [A16.L02 frames t=01:22]
- ตัวเลขที่ article ไม่ได้ให้: หมอกมองเห็น 20 m, ทหารชัด ~40 คน, ขั้นการลุก (มือ 0.5s, หมวก 1.5s, ยืน 3s), การแปลงร่าง 0.4s [A16.L03 t=01:00] [A16.L03 t=01:29] [A16.L03 t=01:36] [A16.L03 t=02:59]
- caption pro-tip: "Think like a director — Choose locations that naturally hide the AI slop.", "Crowd scale is about layering, not high numbers.", "Write camera moves in meters and degrees, not adjectives." [A16.L03 frames t=01:15] [A16.L03 frames t=01:30] [A16.L03 frames t=02:55]
- การเทียบต้นทุน: ฉากฝูงชนจริงต้องใช้ CGI crowd simulation หลายเดือนและ render หลายวัน ที่นี่ใช้ 5 นาทีกับ prompt เดียว (คำกล่าวของผู้สอน) [A16.L03 t=00:16]
- "Write tension in centimeters" และ skill คำนวณให้ — article ไม่พูดถึงเซนติเมตรเลย [A16.L04 t=00:40] [A16.L04 t=00:48]
- ข้อสังเกตยุค model: ช็อต bullet time ทำเมื่อหลายเดือนก่อน model รุ่นใหม่ควรได้เร็วกว่า [A16.L04 t=01:37]
- block แรกของ prompt เวอร์ชันลุคเกมเต็มไปด้วย "NOT ... NO ..." (เช่น "NOT a glowing fantasy material", "NO internal glow, NO pulsing light") — ตัวอย่างจริงของกับดักคำปฏิเสธ [A16.L05 frames t=00:10]
- caption "STEP 1 — Swap bans for direct descriptions." และรายการเลนส์ "50MM ORBIT. 24MM LOW ANGLE. 85MM CLOSE-UP. 35MM WIDE." [A16.L05 frames t=01:00] [A16.L05 frames t=01:25]

### จุดที่คอร์สขัดแย้งกันเอง / ช่องว่างของหลักฐาน
- การแก้แขนใน L02: transcript และ article บอก "raise the arm" แต่คำแก้ที่พิมพ์บนจอคือ "only the right arm, pointed straight at the camera, so the blade shortens into a small point. Never show it from the side" — ไม่รู้ว่าเวอร์ชันไหนให้ take สุดท้าย [A16.L02 t=03:33] [A16.L02 frames t=03:45]
- skill บอกให้เปลี่ยนข้อห้ามเป็น positive constraint แต่ camera block ที่ขยายแล้วยังมี "no sideways drift, no rotation, no tilt, no pan..." หลายข้อ [A16.L01 frames t=01:30] [A16.L02 frames t=01:05]
- ชื่อผู้สอน: metadata บอก Ziya Rufat (Creative Director, Higgsfield) แต่ Claude UI ทักว่า "Evening, Adil" [A16.L01 frames t=01:55]
- ชื่อ tag ไม่สม่ำเสมอ: cue ใช้ @roko_warrior แต่ prompt บนจอใช้ "@crystal_knight"; บอร์ดเขียน @samurais2/@samurais3 (เดิมเคยอ่านเป็น @samurai2/@samurai3) [A16.L03 cue cue-transformation-brief] [A16.L03 frames t=03:03] [A16.L01 frames t=02:17]
- ระยะหมอก: ผู้สอนพูด 20 m แต่ overlay ของ location block เขียน ~15-25m (สอดคล้องกัน แต่ไม่ใช่ค่าเดียว) [A16.L03 t=01:00] [A16.L03 frames t=01:03]
- ไม่มีบทไหนที่ title card เป็น Beat 4: L04 คือการฟันครั้งแรก และ title card "BEAT 5 — KILLING THE VIDEO-GAME LOOK" โผล่ท้าย L04 ซึ่งเป็นของ L05 [A16.L04 frames t=02:00]
- ค่าเลนส์ 50/24/85/35mm มีในเสียงและ caption แต่ไม่อยู่ใน cue text — น่าจะเข้ามาผ่านการขยายของ Claude (ยังไม่ยืนยัน) [A16.L05 t=01:24] [A16.L05 cue cue-cinematic-coverage-brief]
- ไฟล์ skill: วิดีโอบอก "grab it in the description below" แต่เนื้อหาคอร์สไม่มี link; เห็นกฎของ skill เพียงบางส่วนบนจอ [A16.L01 t=01:42]
- prompt ที่ขยายแล้วอ่านได้แค่บางส่วนบนจอ และ article บอกว่าไม่ได้ทำซ้ำไว้; prompt เต็มของ Beat 2–5 ไม่มี [A16.L02 article] [A16.L03 article]
- "I'm sorry" 5 ครั้งใน transcript L03 เป็น whisper hallucination ระหว่าง playback (compression_ratio 2.955) ไม่ใช่บทพูดของผู้สอน; บทพูดเดียวที่คาดในช็อตคือ Monster พูด "Korose" — ยังไม่ได้ฟังยืนยัน [A16.L03 t=03:40]
- ช็อต close-up 85mm จับดาบกลางอากาศไม่อยู่ใน tile ที่สุ่ม [A16.L05 frames t=01:45]
- ไม่มีการพูดถึงจำนวน iteration ที่ model รุ่นใหม่ต้องใช้ และ aspect/resolution/ต้นทุนของบางบทอ่านไม่ได้ [A16.L04 t=01:37] [A16.L04 frames t=00:26]

### เทียบกับ v1
- เพิ่ม: Claude skill "higgsfield-cinematic-seedance-skill" พร้อมกฎและวิธีติดตั้ง ซึ่ง v1 ไม่มี [A16.L01 t=01:42] [A16.L01 frames t=01:35]
- เพิ่ม: settings Seedance 2.0 จริง (15s, batch 4, High) และตัวเลขบนปุ่ม Generate [A16.L02 frames t=01:22] [A16.L05 frames t=00:10]
- เพิ่ม: ตัวเลขกำกับ (หมอก 20 m, ~40 ทหาร, ขั้น 0.5s, orbit 8→4 m / 3→2 m, snap 0.4s, ช่องว่างใบมีด 5-8 → 2-3 → 1 cm) [A16.L03 t=01:00] [A16.L03 frames t=02:47] [A16.L04 frames t=00:40]
- เพิ่ม: กฎวัสดุ "crystal always beats steel" และกฎ match cut "EXACTLY match" [A16.L04 t=00:24] [A16.L04 t=01:00]
- แก้: v1 สรุปว่าแก้แขนด้วยการ "กำกับท่ายกแขน" แต่คำแก้บนจอคือชี้แขนตรงเข้ากล้องให้ใบมีดสั้นเป็นจุด — เป็นข้อขัดแย้งที่ต้องระบุ [A16.L02 frames t=03:45]
- เหมือนเดิม: reference แต่ละอันมีหน้าที่เดียว และกฎ 180 องศาต้องมีภาพมุมที่อนุมัติรองรับ [A16.L01 article]
- เหมือนเดิม: ถ้า brief ทำงานแล้วแต่ take เดียวผิด ให้ reroll ก่อนเปลี่ยนสิ่งที่ล็อกไว้ [A16.L04 t=01:23]
- เหมือนเดิม: แทนกล้องลอยตามหลังด้วยช็อตที่มีหน้าที่ (orbit, low, close, wide) และข้อความในบทเป็นคำขอให้ Claude ขยาย ไม่ใช่ generation prompt ฉบับเต็ม [A16.L05 t=01:24] [A16.L05 cue cue-cinematic-coverage-brief]

## ภาค B — กฎข้ามคอร์ส

### B1 ลำดับงานและการล็อก asset ก่อนทำวิดีโอ
- ลำดับที่หลายคอร์สสอนตรงกันคือ บท → assets (ตัวละคร สถานที่ พร็อพ สินค้า) → shot list → ฉากวิดีโอ และห้าม generate ฉากก่อนล็อก asset [A01.L01 article] [A06.L01 article] [A10.L01 t=00:41] [A15.L01 article]
- ทุกองค์ประกอบที่กลับมาซ้ำต้องมี reference ที่อนุมัติแล้วหนึ่งอันก่อนเข้า motion ถ้าข้าม sheet ทุก generation จะสร้างคนใหม่ [A02.L04 article] [A02.L09 t=01:57-02:12] [A15.L01 article] [A16.L01 article]
- ทดสอบ asset สำคัญด้วยต้นทุนต่ำก่อนล็อก (motion test สั้น ๆ, ทดสอบ location ก่อนทำฉากเต็ม, ทดสอบ plate ที่ clean แล้วใน motion) เพื่อไม่เสียเครดิตกับฉากเต็มบน asset ผิด [A06.L03 t=00:59] [A06.L07 t=01:21] [A10.L02 t=03:35] [A15.L04 t=01:46]
- เมื่อสภาพตัวละครเปลี่ยนกลางเรื่อง (เสื้อขาด, ตัวเปียก, ถอดชุดปลอมตัว) ให้สร้าง reference ใบใหม่ของสภาพนั้นแล้วสลับใช้ตั้งแต่ช็อตที่เปลี่ยน แทนการสั่งด้วยคำ ("images are cheap, videos aren't") [A01.L08 t=04:27-04:46] [A06.L12 t=01:09] [A15.L06 t=02:23]
- ตัวละครใหม่กลางเรื่องยังต้องมี sheet แต่ตัวที่โผล่ครั้งเดียวและพร็อพที่ใช้ครั้งเดียวเขียนด้วยข้อความบรรทัดเดียวได้ [A02.L18 t=01:03-01:13] [A02.L11 t=00:21-00:30] [A10.L07 t=01:48–02:03]
- พร็อพที่ปรากฏซ้ำต้องล็อกด้วย prop sheet หลายมุม แต่ไม่ต้อง motion test เพราะพร็อพไม่ได้ "แสดง" [A04.L03 t=01:20] [A10.L02 t=06:44–07:48] [A06.L09 t=00:08]
- สินค้าต้องมีภาพหลายมุม รูปเดียวไม่พอเพราะโมเดลจะเดา; ทำบนพื้นเทากลางเพื่อวางกับพื้นหลังใดก็ได้ และโฆษณาหลายสินค้ารวมทั้งหมดใน lineup reference ภาพเดียว [A06.L02 t=00:23] [A15.L01 t=02:19] [A08.L06 cue cue-l6-skincare]
- จัดระเบียบงานเป็นโฟลเดอร์ต่อฉาก/ต่อ asset หรือเป็นตาราง dependency ที่บอกชื่อ reference และฉากที่ใช้ [A01.L03 t=00:00-00:17] [A06.L02 frames t=00:20] [A15.L01 article]

### B2 Character sheet และการคุม identity
- Character sheet บนพื้นเทาเรียบได้ win rate สูงกว่า [A01.L03 t=00:45-00:54] [A06.L03 t=00:38] [A02.L04 article]
- หนึ่ง sheet = หนึ่งใบหน้า ถ้ามีหน้าซ้ำบนแผง full-body ให้ลบออกใน image editor แทนการ regenerate เพราะสองหน้าทำให้ identity drift [A01.L03 t=01:22-01:39] [A01.L10 t=03:39] [A06.L06 t=00:13] [A15.L02 t=05:06]
- เกณฑ์คัด sheet คือคุณภาพแสงก่อนความเหมือน เพราะวิดีโอดึง texture และแสงจากภาพนิ่ง วิดีโอจึงดีได้แค่เท่า reference [A02.L04 article] [A02.L04 t=01:17] [A10.L02 t=02:24–02:34]
- แยกงาน generate กับงาน edit: Soul Cinema ทำ raw pass/สไตล์/การแสดง ส่วน GPT Image 2.0 หรือ Nano Banana Pro ทำ edit, clean sheet และคืน identity — "Don't try to get everything out of one model" [A01.L03 t=04:49-04:58] [A04.L05 t=00:30-00:51] [A15.L02 t=01:48] [A02.L09 article]
- เมื่อมีตัวเลือกที่ใกล้แล้ว ให้ edit ด้วย keep-list ("Recreate this exactly ... change only X") แทนการ regenerate [A09.L02 t=00:26–00:34] [A09.L02 cue c2d] [A04.L03 t=00:45] [A15.L02 t=05:22]
- ตรวจผิวและหน้าหลัง edit: A06 พบว่า GPT Image edit ทำผิว Soul Cinema นิ่มจนเป็น "AI slop" และแก้ด้วยการซ้อน layer + mask ส่วน A15 เลือก Nano Banana Pro เพราะเก็บหน้าได้ดีกว่า Seedream [A06.L08 t=01:06] [A06.L08 t=01:29] [A15.L02 t=03:45]
- Cast ตามบทบาท ไม่ใช่แค่ความเสถียร: ตัวร้ายต้องอ่านออกตั้งแต่แรกเห็น และปฏิเสธหน้าที่ใช้ได้แต่ดูผิดบท [A06.L04 t=00:27] [A15.L04 t=00:23]

### B3 Location, geography และ continuity ของพื้นที่
- Generate location ที่มุม 3/4 เสมอ เพราะเห็นสองผนัง มี depth เมื่อกล้องเคลื่อน และ win rate สูงกว่ามุมตรง [A01.L03 t=02:42-02:52] [A02.L05 t=00:33-00:44] [A06.L05 t=00:30] [A15.L04 t=01:14]
- Location ที่ดูถูกหรือพลาสติกทำให้ทุกช็อตเสีย และแก้ทีหลังด้วย prompt ไม่ได้ — A10 เรียก location ว่า "the most important image" [A01.L03 t=02:02-02:12] [A06.L05 t=00:04] [A10.L02 t=02:24–02:34]
- เมื่อ location ขาดจุดสำคัญหรือกล้องต้องหันกลับ ให้สร้าง location asset แยกหรือ reverse-angle reference; A16 ใช้คำถามทดสอบว่า "ถ้ากล้องหัน 180 องศาตอนนี้ reference ไหนอธิบายเฟรม" [A01.L07 t=01:41-01:53] [A01.L09 t=01:05-01:17] [A16.L01 article]
- ข้อความตรึงตำแหน่งไม่ได้ ให้ใช้ภาพ: แผนที่ schematic, ภาพวาด top-down หรือ diagram วาดมือ ("a map beats a paragraph") [A06.L13 t=00:35] [A10.L06 t=02:40–02:52] [A01.L06 t=01:34-01:49] [A15.L10 frames t=00:15]
- Seedance ไม่จำตำแหน่งข้าม generation: เปิดคลิปด้วย wide establishing สั้น ๆ, ล็อก blocking ด้วยช็อตแรกที่เรียบ หรือผูกตัวเอกกับตำแหน่งกายภาพ [A02.L12 t=00:04-00:30] [A15.L07 t=01:57] [A06.L13 t=02:10]
- รักษาเส้น 180 องศาด้วย framing เดิมต่อผู้พูด และกำหนดฝั่งจอของแต่ละตัวละครใน prompt [A01.L09 t=02:31-02:50] [A02.L08 article] [A16.L01 article]
- ซ่อนจุดที่ AI ทำพัง: clean plate ลบตัวหนังสือ/ของรก/รถ, ใช้หมอกเป็น "the cheapest cleanup", เลือกกรอบแคบ ("The tighter the frame, the less slop") และเลือก location ที่ซ่อน slop เอง [A15.L04 t=01:25] [A16.L03 t=00:57] [A15.L07 t=00:49] [A16.L03 frames t=01:15]
- เชื่อมฉากด้วย action ที่ต่อกัน (ตกจากป่า → ร่วงลงโซฟา, teleport → มาถึงผ่าน portal) หรือช็อตเดินทางที่แสดงระยะทาง แทนการกระโดดพื้นที่ [A01.L09 t=00:23-00:30] [A04.L04 t=01:09] [A15.L05 t=00:14]
- Match cut: เขียนให้ท่าตอนเปิดช็อตตรงกับท่าตอนจบช็อตก่อน (มือเดียวกัน ท่าเดียวกัน, "EXACTLY match") [A06.L12 t=02:55] [A06.L14 t=00:53] [A16.L04 t=00:24]
- ความต่อเนื่องของสภาพต้องคงอยู่: เรือโดนยิงดาดฟ้าต้องเปียก, ฉากจบจ่ายคืนรองเท้าหาย/เสื้อขาด, ชิ้นเกราะต้องอยู่บนพื้นตั้งแต่ต้น และเศษซากต้องไม่หายระหว่างเฟรม [A01.L06 t=02:43-02:54] [A04.L10 t=00:20-00:30] [A10.L07 t=04:52–05:58] [A05.L06 t=01:00]

### B4 ให้ Claude + skill เป็นคนเขียน prompt
- หลายคอร์สสอนตรงกันว่าไม่เขียน prompt เอง แต่บอกไอเดียเป็นภาษาธรรมดาให้ Claude กับ skill เขียน prompt ที่มีโครงสร้าง; หน้าที่ผู้ใช้คือชัดว่าต้องการอะไร [A01.L01 t=00:51] [A06.L03 t=00:06] [A09.L02 t=00:05–00:15] [A03.L08 t=00:20-00:30]
- ให้ Claude ขยายไอเดียและสัมภาษณ์เรา ("expand my idea" แทน "write me a script", interview → brief) และให้มันเสนอทางออกด้านกล้องหรือมุกหลายแบบ [A01.L02 t=00:22] [A14.L05 t=00:49] [A10.L02 t=04:01] [A10.L09 t=00:14–01:05]
- อัปโหลด asset ให้ Claude ดู อย่าบรรยายเป็นคำ เพราะการบรรยายทำให้ prompt ออกมา generic; เมื่อรู้ดีไซน์ชัดให้ "show, don't tell" ด้วยภาพ [A06.L10 t=01:23] [A01.L04 t=00:38-00:44] [A13.L04 t=00:09] [A03.L06 t=00:07-00:19]
- ตั้งชื่อ asset เป็น @tag ให้ตรงกันทั้งใน Claude และ Higgsfield Elements เพื่อให้ prompt ที่วางกลับแนบ reference อัตโนมัติ [A01.L03 t=05:10-05:26] [A06.L10 article] [A10.L04 t=00:39–00:43] [A15.L01 t=02:45]
- บอก Claude ชัดว่า reference ไหนเป็นอะไรและใช้กับ cut ไหน (อ้างด้วยลำดับภาพ เช่น "@Santiago is 1 photo", "image 1 / image 2") [A06.L12 t=01:56] [A09.L03 t=01:00] [A02.L06 frames t=00:55]
- รักษา context ไว้ในที่เดียว: thread Claude ยาวเส้นเดียว หรือเอกสาร shot list เดียว ไม่ใช่ 20 แชต [A09.L02 t=01:35] [A11.L01 t=00:52–01:07] [A06.L10 t=02:27]
- ใช้ style prefix/header ร่วมกันทุก prompt เพื่อแก้ครั้งเดียวเปลี่ยนทุกที่ แล้ว override เฉพาะฉากที่ต้องการลุคของตัวเอง [A06.L10 t=02:02] [A06.L12 t=02:15] [A10.L04 t=01:26–01:46] [A08.L07 frames t=00:07]
- อย่าแก้ prompt ด้วยมือ ให้ดูผลแล้วส่ง fix list หรือ director notes ภาษาธรรมดาที่ไล่ทุกจุดเสียกลับให้ Claude [A01.L05 t=00:30-01:09] [A10.L04 t=04:21–04:57] [A10.L07 t=01:09–01:33] [A15.L08 t=00:46]
- ถ้าไม่รู้ศัพท์เฉพาะให้ถาม Claude และถ้า prompt ยาวเกินให้ Claude ตัดสินใจแบ่งเอง ("If this is too much for one prompt, split it into two") [A10.L08 t=00:09–00:38] [A15.L06 t=00:00]

### B5 โครงสร้างและภาษาของ video prompt
- Prompt ที่ skill เขียนเป็น section ที่มีป้ายและ lock: A01 มี 14 ส่วนจบด้วย POSITIVE LOCKS, A08 แยก SAME กับ FORBIDDEN, A10 มี style prefix + asset registry + skeleton, A15 แบ่ง REFERENCE DEFINITIONS / TECHNICAL BLOCK / PROMPT, A16 บังคับ ACTIVE REFERENCES [A01.L05 cue recreate-1b] [A08.L01 cue cue-l1-kaiju] [A10.L01 frames t=00:35] [A15.L03 article] [A16.L01 frames t=01:30]
- บอกสถานะที่ต้องการแทนคำปฏิเสธ: A02 พบว่า Seedance 2.0 อ่าน "not crying" เป็น "crying" และ A16 สรุปว่า "telling the model what not to do rarely works" (ดูข้อยกเว้นในภาค E3) [A02.L07 t=00:33-00:48] [A16.L02 t=03:19] [A16.L05 t=00:57]
- เขียนตัวเลขแทนคำคุณศัพท์: ความเร็วกล้องเป็นอัตรา, การเคลื่อนเป็นเมตรและองศา, whip pan เป็นวินาที ("models prefer arithmetic over vague words") [A16.L02 t=01:04] [A16.L03 t=02:44] [A02.L14 t=00:26-00:36] [PB.36]
- เรียกชื่อเทคนิค ไม่ใช่ mood ("add a speed ramp during the kick" ไม่ใช่ "add more drama") และแทนคำคุณศัพท์อย่าง "cinematic" ด้วยสิ่งที่ตรวจได้ [A02.L13 article] [A05.L01 article]
- บรรยาย motion ทีละขั้น ไม่ย่อ ("he dances" ไม่มีความหมาย) และผูก deadline ของการเปลี่ยนกับท่าทางหรือวินาที [A06.L11 t=04:36] [A16.L03 t=01:34] [A03.L05 cue hand-to-snake]
- จำกัดขอบเขตภาพ reference ให้ชัดว่าใช้แค่สไตล์หรือรูปลักษณ์ ไม่เอาตัวละคร พื้นหลัง หรือแสงของภาพนั้น [A04.L06 cue scene4-animated] [A08.L08 cue cue-l8-racing] [A03.L06 cue lizards-climbing] [A13.L04 cue cue-add-figure-behind]
- ผูกพร็อพกับตำแหน่งร่างกาย ตำแหน่งในพื้นที่ และช่วงเวลา ("on the hero's left wrist throughout all frames until he removes it") [A04.L06 cue scene4-animated] [A04.L10 cue scene8-animated] [A06.L13 t=03:01]
- ข้อความที่ต้องอ่านได้ (ตัวหนังสือบนพร็อพ, โลโก้, HUD) ต้องใส่ string ตรงตัวใน prompt และค้างช็อตนานพอ [A02.L14 t=01:30-01:42] [A08.L06 cue cue-l6-skincare] [A08.L07 cue cue-l7-trailer]
- ใส่บทพูดตรงตัวใน prompt เพื่อยึด lip-sync — โมเดลจะ generate เสียงพูดตามนั้น [A03.L06 cue lizards-climbing] [A08.L04 frames t=01:30]
- ระบุสีเป็น hex เป๊ะ (พร็อพ, ชุด, สีแบรนด์) [A01.L03 t=04:12-04:41] [A03.L07 cue wing-walker] [A09.L03 t=01:59–02:04] [A08.L07 cue cue-l7-trailer]
- คุม palette ด้วยชื่อ grade จริงหรือสัดส่วนสี 60:30:10 ใน prompt หรือด้วย Color Transfer จากภาพ vibe ที่อนุมัติ [A02.L09 t=01:37-01:51] [A02.L09 cue ball-prop-sheet] [A15.L03 t=00:23] [A15.L04 frames t=01:10]
- เสียง: ใส่ "No music, environmental SFX only" แล้วค่อยใส่ score ตอนตัดต่อ ยกเว้นเมื่อจังหวะสำคัญ ให้ใส่ music track จริงเป็น audio input [A10.L04 t=01:26–01:46] [A08.L04 cue cue-l4-fungal] [A06.L10 frames t=01:05] [A06.L13 t=04:05]
- ใช้กฎเวลาเดียวทั้งฉาก: ไม่ใช้ slow motion โดย default และอนุญาตเฉพาะ beat ที่ตั้งชื่อ (หรือ slow motion ทั้งฉากยกเว้นจังหวะเดียว) [A08.L07 cue cue-l7-trailer] [A04.L06 t=01:21] [A08.L08 cue cue-l8-racing]
- คิดเป็น 1 generation ≤15 s ที่มีหลายมุมข้างใน และเขียนจำนวนช็อต/cut เป็นกฎแข็ง ("exactly 5 shots and 4 cuts, no extra inserts") [A02.L03 t=00:07] [A04.L03 t=02:33] [A15.L09 t=01:18]

### B6 VFX บน footage จริง
- เก็บ anchor จริงไว้หนึ่งอย่างและให้ AI เปลี่ยนเฉพาะชั้นเดียวต่อรอบ ยิ่ง spectacle ใหญ่ยิ่งต้องพึ่ง anchor; โลกซับซ้อนต้องมี anchor เรียบง่าย [A03.L01 article] [A03.L10 article] [A13.L01 article] [A05.L10 article]
- เขียน keep-list/INPUT LOCK ระบุสิ่งที่ต้องคง และห้าม re-frame, re-time, re-light, re-grade; ปิดด้วย "Face and identity unchanged." [A03.L02 article] [A03.L05 cue hand-to-snake] [A08.L03 cue cue-l3-screen] [A13.L01 cue cue-intro-volcanic-drive]
- ให้โลกใหม่สืบทอดการเคลื่อนกล้องจริงจาก plate (inherit handheld/orbit) เพื่อให้ parallax และ occlusion ถูกเอง [A03.L03 article] [A03.L07 cue wing-walker] [A08.L03 cue cue-l3-screen] [A08.L03 article]
- แสงจากสิ่งที่เพิ่มต้องตกบนตัวคนและวัตถุจริง (หน้า เสื้อ สีรถ) หรือให้ subject ถูก relight ตามโลกใหม่ ไม่งั้นดูเป็นสติกเกอร์ [A03.L04 article] [A03.L03 t=00:37-00:50] [A08.L03 cue cue-l3-screen] [A13.L06 t=00:15]
- ปกป้องผิวหน้าจริงจากการถูก AI ทำให้เรียบ ("real human skin with pores ... never waxy") [A03.L09 cue sauropods] [A08.L03 cue cue-l3-cyber] [A08.L06 t=01:06]
- คลิปต้นทางเดียวทำได้หลายเวอร์ชัน: เก็บคลิปและ template เดิม เปลี่ยนเฉพาะย่อหน้า effect หรือเข้าคิวหลาย prompt จากคลิปเดียว [A08.L03 t=00:26] [A03.L03 frames t=00:34]
- เอฟเฟกต์ต้องมีปฏิสัมพันธ์ทางกายภาพและอยู่หลังขอบจริง (จอเป็น "physical membrane portal, NOT a flat decal") [A03.L11 article] [A08.L03 cue cue-l3-screen] [A03.L04 article]
- ให้สเกลสัตว์ยักษ์ด้วยการกั๊กและบรรยากาศ แล้วระบุ scale ซ้ำ ("~2.5 human-heights ... NOT kaiju-giant") [A03.L09 cue sauropods] [A03.L10 cue kraken] [A08.L07 cue cue-l7-trailer]
- แก้เฉพาะจุดด้วยการทาบริเวณหรือภาพ แทนการอธิบายตำแหน่งเป็นคำ [A13.L05 t=00:03] [A01.L06 t=01:34-01:49] [A03.L06 t=00:07-00:19]

### B7 Iteration และการคัด take
- Generate ทีละ 4 เพื่อแยก glitch สุ่มออกจากปัญหาของ prompt; ถ้า 4/4 พัง ปัญหาอยู่ที่ prompt ไม่ใช่ seed [A16.L02 t=01:32] [A02.L07 t=00:21-00:25] [A01.L05 t=00:02-00:05]
- เปลี่ยนทีละตัวแปรและคงทุกอย่างที่ทำงานแล้ว — สอนตรงกันทั้งงานภาพ งานแปลภาษา และงานธุรกิจ [A06.L05 t=01:08] [A15.L08 t=00:46] [A16.L02 article] [A11.L06 t=00:00–00:26] [A07.L12 article]
- แก้ทีละเรื่อง: pacing/physics ก่อน แล้วค่อย performance และเมื่ออารมณ์อ่านออกแล้วให้หยุดจูนอารมณ์ไปจูนกล้อง ("Basic isn't broken") [A02.L14 article] [A02.L07 t=01:07] [A15.L08 t=00:46]
- ต่อยอด prompt เดิมแทนการเขียนใหม่ ("iterate one prompt three times") และเปลี่ยนจังหวะ take ที่ล็อกแล้วด้วยประโยคเดียว [A06.L13 t=04:55] [A10.L08 t=00:09–00:38] [A02.L13 t=00:00-00:07] [A16.L04 article]
- ขุดช่วงดีจากหลาย batch/generation แล้วประกอบเหมือนตัด dailies [A01.L05 t=03:05] [A02.L08 t=01:15-01:46] [A06.L11 t=02:14] [A10.L06 t=00:30–00:49]
- ตัดสินที่ระดับ beat ไม่ใช่ทั้งคลิป ("beat ไหนได้ เริ่มและจบตรงไหน"), ยอมรับผลบางส่วน และเก็บ phase ที่ยังไม่ได้ใช้ไว้ประหยัดเครดิต [A15.L03 t=01:39] [A10.L08 t=02:11–02:31] [A10.L08 t=01:02–01:13] [A10.L05 t=04:40–04:44] [A15.L07 t=03:19]
- Take ที่ physics พังให้ทิ้งแล้ว reroll; ถ้า brief ทำงานแต่ take เดียวผิดให้ reroll ก่อนเปลี่ยนสิ่งที่ล็อก [A02.L10 article] [A16.L04 t=01:23]
- เมื่อพังหนักให้ทำให้ง่ายลง: multi-shot → one continuous shot, แยกฉากแน่นเป็น generation ย่อย, ตัดช็อตที่ไม่เพิ่มอะไร [A01.L08 t=01:35-01:48] [A10.L07 t=02:31] [A02.L12 t=01:08-01:13]
- ระบุระดับของ defect ก่อนตัดสินใจ rewrite หรือ reroll และแยกตรวจ eyeline/แสง/reaction ให้รู้ว่าปัญหาอยู่ชั้นไหน — "almost right" ไม่ใช่การวินิจฉัย [A16.L04 article] [A05.L09 article]
- ตัดสินเป็นลำดับ ไม่ใช่คลิปเดี่ยว ("A generation can be visually successful and still fail the film"), เลือกตามบรรทัดและการแสดง และวัดความ coherent ของทั้งเรื่อง [A15.L11 t=00:16] [A02.L17 t=01:17-01:44] [A02.L18 t=01:30-01:36] [A11.L05 t=00:32–01:03]
- ผลดีแล้วก็ยังดันต่อด้วย note เจาะจง และรัน batch สำรองแม้ได้ผลแรกแล้ว [A10.L04 t=05:18–05:41] [A10.L09 t=00:14–01:05] [A06.L13 t=04:41]

### B8 กล้องและการตัด
- การเคลื่อนไหวอย่างเดียวไม่พาอารมณ์ ให้แตกช็อตและใช้กล้องที่มีพลวัต; fight ใช้ hard cut ที่เลนส์ต่างกันแทน long take ที่ลอยตามหลังซึ่งดูเป็นวิดีโอเกม [A02.L08 t=00:00-00:11] [A16.L05 t=01:11] [A16.L05 t=01:24]
- ภาษากล้องที่ขายความจริง: low angle + handheld shake ให้ "real sports ad", handheld เลี่ยงลุค game engine, Dutch angle สร้างความตึงเครียด [A10.L05 t=02:15–02:33] [A02.L10 article] [A02.L08 t=00:11-00:27]
- ใส่ macro insert สั้น ๆ ที่ไม่มีตัวละครให้งานตัดต่อดูแพง; beat ที่ใช้ซ้ำได้คือ hook → extreme slow-mo macro → snap กลับความเร็วปกติ [A10.L05 t=03:16–03:43] [A08.L01 cue cue-l1-dragon] [A08.L04 cue cue-l4-fungal]
- ปล่อยให้ Claude/โมเดลวาง staging และกล้องเองได้ ไม่ต้องสั่งทุกการเคลื่อน [A08.L04 t=01:38] [A10.L02 t=04:01]
- ทดสอบ coverage และความลึก: ช็อตเร็วที่มี depth ให้ตัดสินที่การจัดการพื้นที่ 3D และแต่ละ setup ต้องให้ข้อมูลต่างกัน [A08.L08 t=00:12] [A16.L05 article]

### B9 การแสดงและจังหวะเรื่อง
- ตัวละครต้องตอบสนองต่อโลก (micro-acting, "that one second of doubt", เว้น air ระหว่าง action) การยืนจ้องเฉย ๆ ทำให้ช็อตตาย [A01.L05 t=01:15-01:27] [A15.L06 t=00:48] [A10.L07 t=03:15–03:42]
- ให้ตัวละครเป็นคนทำ action เอง และสิ่งที่เพิ่มเข้ามาต้องมีเจตจำนงของตัวเอง ไม่เกิดแบบ "magic" [A10.L07 t=05:03–05:40] [A03.L05 article]
- ทำให้บทพูดสั้นลงหรือพูดไม่จบเพื่อแก้การแสดง ("Change what? No" → "Change? No", "And I...") [A15.L08 t=01:57] [A02.L12 t=00:56-01:08]
- กำกับอารมณ์ด้วยเจตนาและสถานะที่มองเห็นได้ ไม่ใช่ความดังหรือคำปฏิเสธ [A01.L09 t=02:56] [A02.L07 t=00:33-00:48] [A15.L08 t=00:46]
- Take ที่น่าเบื่อแก้ด้วยมุกของตัวละครหรือ reaction beat ของตัวประกอบ ไม่ใช่เพิ่ม spectacle [A01.L05 t=02:19-02:35] [A04.L08 t=01:06-01:19] [A10.L09 t=00:14–01:05]
- สร้างความตึงก่อนเปิดเผย และให้ตัวเอก "เกือบ" ถึงเป้าหมาย [A10.L05 t=01:31–01:59] [A01.L07 t=03:45-04:02]
- ฉากแรก/วินาทีแรกต้องดีที่สุด เพราะ "if the first thing you see feels off you stop watching" และ hook ต้องเปิดด้วย payoff [A10.L04 t=01:00] [A11.L04 t=00:41–01:01] [A12.L03 t=01:35]

### B10 ความละเอียดและการตัดสิน realism
- รันที่ 4K เมื่อแสง flare หมอก ฝูงชน wide ที่วุ่น และข้อความบนจอต้องปรากฏจริง ความละเอียดต่ำจะเกลี่ยหายหรือ morph [A02.L10 t=00:22-00:30] [A08.L01 t=01:56] [A08.L02 t=00:00] [A08.L04 t=01:53]
- ความละเอียดเป็น trade-off ที่ต้องบันทึกแยก: A05 ชั่ง Seedance 2.5 (30 s, 720p) กับ 2.0 (15 s, 4K) และให้ตัดสินที่ขนาดส่งมอบจริง [A05.L02 t=01:38] [A05.L11 article] [A05.L11 t=00:19] [A08.L01 t=01:56]
- ตัดสิน realism จาก texture ผิว (รูขุมขน ความไม่สมบูรณ์) และเขียนภาพใกล้แบบ anatomy reference ไม่งั้นออกมาเป็นพลาสติก [A08.L06 t=01:06] [A02.L12 t=00:38-00:52] [A03.L09 cue sauropods]
- ตัดสินเป็น layer และด้วยหลักฐานที่หาเจอได้ ไม่ใช่คำคุณศัพท์ (ผิว น้ำ พื้นหลัง; layer ใกล้/กลาง/ไกล) [A08.L01 t=03:08] [A05.L01 article] [A05.L08 article]

### B11 แบรนด์ โฆษณา และสินค้า
- ใส่ brand hex ลงทุก brief และล็อกสีสินค้าเป็นประโยค ("Serum stays green, cream stays white"); A09 ทำให้สีแบรนด์เป็นสีอิ่มตัวเดียวในโลก monochrome [A09.L03 t=01:59–02:04] [A09.L04 cue c4a] [A08.L06 cue cue-l6-skincare]
- ตรวจโลโก้ทุกพื้นผิวในผลลัพธ์ และระบุ string โลโก้ตรงตัว; เผื่อรอบสลับโลโก้เพราะ mockup prompt สร้างแบรนด์ placeholder เอง [A09.L06 t=02:18–02:33] [A09.L03 cue c3b] [A08.L06 cue cue-l6-skincare]
- Pack shot คือ "the one that sells" และแบรนด์ควรมีสินค้า hero ที่จำได้ทันที [A10.L09 t=01:23–02:40] [A09.L03 t=01:15–01:23]
- ทำ variant โดยคง character/product/preset แล้วเปลี่ยนแค่ prompt และทำหลายตัวไว้ทดสอบ (หนึ่ง preset ต่อสินค้า, ชุด 10 โฆษณาเป็น testing matrix) [A09.L06 t=03:02–03:08] [A09.L05 t=00:46–00:56] [A07.L05 frames t=00:49]
- ข้อเท็จจริงในโฆษณา (ราคา เบอร์โทร โปรโมชัน) ห้ามให้โมเดลเติม และเนื้อหา AI ต้องติดป้าย: testimonial สมมติต้องเป็น fiction, YouTube ตั้ง "Altered/synthetic content" = YES [A07.L05 article] [A07.L04 article] [A12.L05 t=00:50]

### B12 ช่อง faceless และเนื้อหายาว
- เลือก niche ที่ RPM สูง ซึ่งทั้งสองคอร์สให้ education อยู่บนสุด [A11.L03 t=00:20–00:29] [A12.L03 t=00:14–00:37]
- YouTube flag เนื้อหา spam/unoriginal ไม่ว่าจะเป็น AI หรือไม่ script ที่ original และมี insight จึงเป็นสิ่งที่รักษารายได้; ยืม format ได้แต่ห้ามยืมวิดีโอ [A11.L04 t=00:16–00:29] [A12.L06 t=00:27–00:39] [A12.L01 t=01:56–02:03]
- เปลี่ยนภาพทุกไม่กี่วินาที (A12: ทุก 5–10 s, วิดีโอ 5 นาทีต้องมีอย่างน้อย 30 คลิป) [A11.L05 t=00:32–01:03] [A12.L04 t=00:00–00:14]
- Script เป็นแผนที่เครื่องอ่านได้ (acts, timecode, clip ID, VO ต่อคลิป หรือ 60 blocks/6 chapters/open loops) เพื่อให้ prompt ตามเพียงตัวเดียวขับการสร้างวิดีโอ [A12.L03 t=01:35] [A12.L04 cue cue-video-prompt] [A11.L10 frames t=00:33]
- Thumbnail: focal point เดียวอ่านได้บนมือถือ ข้อความ 1–4 คำ และทำหลายแบบให้ทดสอบ [A11.L08 t=00:25–00:31] [A11.L08 t=00:15] [A12.L05 t=00:37–00:42]

### B13 MCP, ต้นทุน และความรับผิดชอบ
- Endpoint ของ Higgsfield connector คือ `https://mcp.higgsfield.ai/mcp` (ต่างจากหน้า setup) และการเชื่อมบัญชีเป็นหน้า OAuth consent Allow/Deny ในเบราว์เซอร์ [A07.L03 frames t=00:31] [A12.L02 frames t=00:13] [A12.L02 t=00:25] [A13.L02 t=00:15]
- Connector พิสูจน์แล้วเมื่อได้ผลกลับมาจริงเท่านั้น และก่อนใช้เครดิตให้ตรวจ workspace ยอดเงิน spec ของโมเดล และงานเดิมในโปรเจกต์ [A07.L03 article] [A12.L04 t=00:40] [A12.L05 t=01:00]
- นับ generation ที่ล้มเหลวและงานที่จ่ายซ้ำรวมในต้นทุนจริง [A14.L09 t=00:02] [A12.L05 t=00:50] [A10.L08 t=01:02–01:13]
- เริ่มด้วย batch เล็กที่วัดผลได้ และใช้สัญญาณจริง (play, remix, average view duration) ตัดสินก่อน scale [A07.L11 article] [A11.L10 t=00:02–01:06] [A14.L07 t=00:28]
- Automation เอาการ copy/route ออก ไม่ได้เอาความรับผิดชอบออก: A07 ส่ง draft และ QC ไปหาผู้อนุมัติที่มีชื่อ ส่วน A12 แสดงว่าข้อความ "done" ของ Claude ซ่อนการแก้เองและงานซ้ำไว้ [A07.L07 article] [A07.L09 article] [A12.L05 t=02:03] [A12.L05 t=00:10]

## ภาค C — Prompt Bank (PB) และ Course Pages (CP)

### C1 Prompt Bank — กล้อง 46 แบบ: ไวยากรณ์ร่วม
- ที่มา: 46 prompts ในแท็บ "Camera movements" ทุกรายการอยู่หมวด Camera; ผลตรวจภาพ MATCH 44 · MISMATCH 1 (PB.05) · UNCLEAR 1 (PB.32) และ audit ดึงเฟรมเองแล้ว PASS 46/46 [PB.05] [PB.32]
- ขอบเขตของการตรวจภาพ: ยืนยันได้แค่ชนิดและทิศทางของการเคลื่อน ไม่ได้วัดความเร็ว easing หรือตัวเลขเมตร/องศา/วินาที [PB.08] [PB.25]
- ข้อ 1 ประกาศ move เดียวพร้อม rig ก่อนเสมอ: "One continuous [move]" 11 prompts, ตระกูล zoom ใช้ "Locked tripod ... the entire move is optical", ที่เหลือบอก rig ตรง ๆ (ground rails, slider, jib, chest-mounted, shoulder-rig, motion-control) [PB.10] [PB.04] [PB.19]
- บางรายการเพิ่มคำเปรียบ เช่น "like an elevator window" หรือ "like a standing head-turn" [PB.26] [PB.02]
- ข้อ 2 ตัวเลขในช่องวงเล็บ 30 prompts เช่น ความสูง [1.5] m, รัศมี [2.5] m, FOV [18]/[84] องศา, หมุน [90] องศา, whip 0.4 s, snap 1.2 s [PB.10] [PB.15] [PB.29] [PB.36]
- ข้อ 3 ช่องเนื้อหาในวงเล็บ 37/46 เช่น [composition A], [the landing subject], [the lower anchor]; ไม่มีช่องใน PB.01, 16, 22, 23, 32, 33, 36, 37, 44 [PB.01] [PB.16] [PB.02]
- ข้อ 4 รายการ "no X, no Y" 41/46 ระบุ move ข้างเคียงที่โมเดลอาจสับสน: "no zoom" 26 prompts, zoom ห้าม dolly ("NOT a dolly out, NOT a pull-back"), orbit ห้าม "turntable effect"; ไม่มีรายการนี้ใน PB.14, 16, 21, 45, 46 [PB.38] [PB.15] [PB.14]
- ข้อ 5 ความเร็ว: "constant" 26 prompts, ease/decelerate/settle 19, "no speed ramps" 5 (PB.07, 08, 17, 18, 23) [PB.07] [PB.17] [PB.23]
- ข้อ 6 framing invariant หนึ่งอย่างที่ต้องคง (subject dead-center ขนาดคงที่, horizon level, lens axis ตรง); parallax ถูกเรียกใน 14 prompts — บังคับใน move กายภาพ ห้ามใน optical zoom [PB.10] [PB.04] [PB.38]
- ข้อ 7 เงื่อนไขเทียบเฟรมแรก/เฟรมสุดท้าย 8 prompts (PB.01, 10, 22, 25, 26, 35, 38, 44) [PB.01] [PB.22] [PB.35]
- ข้อ 8 end state แบบ hold/settle 22 prompts; ข้อยกเว้นคือ PB.23 จบกลางการเคลื่อน และ PB.32 ไม่หยุดเลย [PB.23] [PB.32]
- สองสำเนียง: 6 prompts ใช้หัวข้อ "Speed: ... Framing: ... End: ..." (PB.02, 06, 21, 43, 45, 46) และ PB.24 ใช้ "End:" อย่างเดียว ที่เหลือ 39 เป็นย่อหน้าเดียวเรียง move → ตัวเลข → ข้อห้าม → ความเร็ว → invariant → end [PB.02] [PB.24] [PB.46]
- โครงที่ประกอบจากข้อ 1–8 (เป็นโครงสังเคราะห์จากบันทึก ไม่ใช่ข้อความต้นฉบับ): [PB.10] [PB.36]

```
[ONE move + rig/physics] from [start slot] to [end slot] at [numeric params];
no [confusable move 1], no [confusable move 2], no zoom ...;
Speed: [constant / eased / ramp + duration];
Framing: [the invariant that must hold];
End: settle on [final composition] and hold.
```

- ไม่มี prompt ใดใน 46 รายการพูดถึงโฆษณา สินค้า หรือ affiliate; คอลัมน์ "ใช้เมื่อ" ในตารางด้านล่างอนุมานจากถ้อยคำของ prompt เท่านั้น [PB.01] [PB.42]
- เชื่อมกับคอร์ส: whip pan ใน PB ใช้ 0.4 s และ overshoot 2 องศา ส่วน A02 สอนให้ระบุ duration, ติดป้าย subject A/B และเริ่ม-จบที่ shot size เดียวกัน [PB.36] [PB.37] [A02.L14 t=00:26-00:36] [A02.L14 t=01:05-01:13]
- เชื่อมกับคอร์ส: PB ห้าม speed ramp ในหลายรายการ ตรงกับ A08 ที่ไม่ใช้ slow motion โดย default [PB.07] [PB.18] [A08.L07 cue cue-l7-trailer]
- เชื่อมกับคอร์ส: PB เขียนการเคลื่อนเป็นเมตรและองศาแบบเดียวกับที่ A16 สอน [PB.08] [PB.34] [A16.L03 t=02:44]

### C1.2 ดัชนี Prompt Bank 46 รายการ
| PB | ชื่อ | หมวด | การเคลื่อน (ย่อ) | ใช้เมื่อ (จากถ้อยคำ prompt) | ตรวจภาพ |
|---|---|---|---|---|---|
| [PB.01] | Static shot | Static | กล้องไม่ขยับเลย ทุกการเคลื่อนมาจากฉาก | การเคลื่อนทั้งหมดมาจากฉาก/สินค้า | MATCH |
| [PB.02] | Pan right | Pan & tilt | หมุนแนวนอนจากจุดเดียว ซ้ายไปขวา จนหมุนเจอ subject | reveal subject ที่รออยู่นอกขอบขวา | MATCH |
| [PB.03] | Tilt up | Pan & tilt | ตำแหน่งคงที่ หมุนขึ้นความเร็วคงที่จาก anchor ล่างถึง subject แล้ว hold | reveal ล่างขึ้นบน | MATCH |
| [PB.04] | Zoom in | Zoom & focus | กล้องล็อก zoom optical ช้า FOV ~84 → 29 หรือ 18 องศา ไม่มี parallax | tighten ช้าจาก wide สู่ detail | MATCH |
| [PB.05] | Dolly zoom | Zoom & focus | dolly เข้า 6 → 2.5 m พร้อม zoom ออก 18 → 84 องศา ให้หัวคงขนาด | subject คงที่ พื้นหลังยืด (ชวนเวียนหัว) | MISMATCH |
| [PB.06] | Rack focus | Zoom & focus | กล้องล็อก เปลี่ยนแค่โฟกัส ไกล → ใกล้ แล้ว follow focus | subject ยื่นวัตถุเข้าหาเลนส์ | MATCH |
| [PB.07] | Crane up | Aerial & crane | jib ขึ้น ~1.2 → 9 m พร้อม tilt ลงต่อเนื่อง | ยกจากคนสู่ภาพ location | MATCH |
| [PB.08] | Drone orbit | Aerial & crane | drone วนความเร็วคงที่ รัศมี 8 m สูง 4 m ราว 200 องศา | not stated | MATCH |
| [PB.09] | Aerial pullback | Aerial & crane | บินถอยและขึ้นตามแกน เร่งความเร็วถึง ~40 m ไกล 25 m สูง | ปิดเรื่องด้วยการถอยออก subject เล็กลงกลางจอ | MATCH |
| [PB.10] | Dolly in | Dolly & tracking | dolly เข้าบนราง ความเร็วคงที่ เลนส์สูง 1.5 m จบด้วย hold | ดันเข้าหา subject เดียวอย่างเด็ดขาด | MATCH |
| [PB.11] | Tracking | Dolly & tracking | เคลื่อนขนานด้านข้างเท่าความเร็ว subject มุม 90 องศา 3 ชั้น parallax | เดินทางด้านข้างผ่าน foreground | MATCH |
| [PB.12] | Push in | Dolly & tracking | ไหลเข้าช้า ~7 → 2 m สูง 1.5 m มีการแกว่งเล็กน้อย | เข้าใกล้แบบ "held breath" | MATCH |
| [PB.13] | Handheld | Specialty | shoulder rig สั่นจริง หายใจ horizon เอียง วนครึ่งวงแล้วเข้า close-up | not stated | MATCH |
| [PB.14] | POV | Specialty | กล้องเป็นตาคนสูง ~1.7 m เดินโยกตามก้าว มือโผล่เฉพาะตอนแตะของ | ช่วงบุคคลที่หนึ่งที่มือคนดูทำบางอย่าง | MATCH |
| [PB.15] | 360 orbit | Specialty | วงรอบ 360 องศา รัศมีล็อก 2.5 m subject กลางจอขนาดคงที่ กลับ framing แรก | not stated | MATCH |
| [PB.16] | Bullet time | Specialty | เวลาหยุด กล้องเคลื่อนโค้งรอบโมเมนต์ที่ค้างด้วยความเร็วปกติ | not stated | MATCH |
| [PB.17] | Crush zoom | Zoom & focus | hold ที่ 18 องศา แล้ว crash zoom ออก ~0.4 s ถึง 84 องศา แล้ว hold | crash ออกจากแน่นสู่กว้างเพื่อ reveal | MATCH |
| [PB.18] | Robot arm | Specialty | motion-control ผ่าน 4 ตำแหน่ง ช่วงละ ~1 s มี ease และ hold สั้น | subject เดียวหลายมุมใน take เดียว | MATCH |
| [PB.19] | Body-mounted camera: Snorricam | Specialty | rig ติดหน้าอกหันกลับหาตัวเอง หน้าล็อกกลางจอ โลกโยกด้านหลัง | not stated | MATCH |
| [PB.20] | Timelapse | Specialty | ถอยช้าคงที่ โลกเป็น time-lapse แต่ subject เคลื่อนเวลาจริง | not stated | MATCH |
| [PB.21] | Chase shot | Dolly & tracking | กวาดเข้าหาคนวิ่งแล้วตาม handheld สะเทือนทุกจังหวะกระแทก | not stated | MATCH |
| [PB.22] | Truck right | Dolly & tracking | เลื่อนขวาความเร็วคงที่ แกนเลนส์ตรงไม่ pan subject ไหลไปขอบซ้าย | not stated | MATCH |
| [PB.23] | Low tracking | Dolly & tracking | slow motion สุด (~1000 fps) กล้องต่ำกว่าเข่าเลื่อนข้าง จบกลางการเคลื่อน | not stated | MATCH |
| [PB.24] | Pan left | Pan & tilt | หมุนซ้าย ~90 องศา ให้ framing ปลายทางมาพร้อมเหตุการณ์ แล้ว hold | หมุนซ้ายไปลงที่ beat/เหตุการณ์ | MATCH |
| [PB.25] | Pedestal down | Pan & tilt | ทั้งกล้องลดลงตรง 2.2 → 0.8 m เลนส์ระนาบเดิม | not stated | MATCH |
| [PB.26] | Pedestal up | Pan & tilt | ทั้งกล้องยกขึ้นตรง 0.8 → 2.2 m เลนส์ระนาบเดิม | reveal ล่างขึ้นบนแบบ "elevator window" ไม่ tilt | MATCH |
| [PB.27] | Side tracking | Dolly & tracking | ข้อความเหมือน PB.11 ทุกไบต์ | not stated (ข้อความเดียวกับ PB.11) | MATCH |
| [PB.28] | Slider left | Dolly & tracking | slider ซ้ายสั้น ~40 cm ช้า แกนเลนส์ตรง parallax ชัด | parallax เบา ๆ บนฉากนิ่ง | MATCH |
| [PB.29] | Fast zoom in | Zoom & focus | hold 84 องศา แล้ว zoom แรง ~1.2 s ถึง 18 องศา แล้ว hold | punch-in จาก wide สู่ tight | MATCH |
| [PB.30] | Fast zoom out | Zoom & focus | hold 18 องศา แล้ว zoom ออก ~1.2 s ถึง 84 องศา แล้ว hold | เปิดกว้างเพื่อเผยผลลัพธ์ | MATCH |
| [PB.31] | Tilt down | Pan & tilt | tilt ลงช้า ~+35 → -10 องศา ผ่าน detail กลางทาง แล้ว hold | reveal บนลงล่างผ่าน detail | MATCH |
| [PB.32] | Push past | Dolly & tracking | เดินหน้าเลนเยื้อง ~0.6 m ผ่านไหล่ subject ต่อไปถึง reveal ไม่หยุด | ผ่านคนด้านหน้าไปหาสิ่งที่อยู่ไกลกว่า | UNCLEAR |
| [PB.33] | Follow shot | Dolly & tracking | ตามหลังไหล่ ~0.8 m ความเร็วเท่าการเดิน โฟกัสไปข้างหน้า | ตามหลังไปสู่สิ่งที่ subject เดินเข้าไปหา | MATCH |
| [PB.34] | Arc right | Dolly & tracking | arc ขวา ~60 องศา รัศมี 2.5 m subject กลางจอ subject ไม่ขยับ | not stated | MATCH |
| [PB.35] | Dolly out | Dolly & tracking | dolly ถอยบนราง ความเร็วคงที่ เลนส์ 1.6 m ไม่ tilt | ถอยปิดเรื่องระดับสายตา ไม่ยกสูง | MATCH |
| [PB.36] | Whip pan left | Pan & tilt | hold A → whip ซ้าย 0.4 s เบลอเต็ม → ลง B overshoot 2 องศา → hold | transition ในกล้องระหว่างสอง set-up นิ่ง | MATCH |
| [PB.37] | Whip pan right | Pan & tilt | hold A → whip ขวา 0.4 s → ลง B overshoot 2 องศา → hold | transition ในกล้องระหว่างสอง set-up นิ่ง | MATCH |
| [PB.38] | Slow zoom out | Zoom & focus | tripod ล็อก zoom optical ออกช้า 18 → 84 องศา ไม่ใช่ dolly ไม่มี parallax | เผยบริบทรอบ subject กลางจอ | MATCH |
| [PB.39] | Reverse tracking: Walk-and-talk | Dolly & tracking | กล้องถอยเท่าความเร็วเดิน ขนาดคงที่ FOV 47 องศา | presenter เดินเข้าหากล้องขนาดคงที่ | MATCH |
| [PB.40] | Arc left | Dolly & tracking | arc ซ้าย ~60 องศา รัศมี 2.5 m subject กลางจอ | not stated | MATCH |
| [PB.41] | Slider right | Dolly & tracking | slider ขวาสั้น ~40 cm ช้า แกนเลนส์ตรง | parallax เบา ๆ | MATCH |
| [PB.42] | Vehicle tracking | Dolly & tracking | เคลื่อนคู่รถเท่าความเร็ว รถคงขนาด ฉากไหลผ่านทุกชั้น | hero shot ของรถที่ล็อกในเฟรม | MATCH |
| [PB.43] | Drone push in | Aerial & crane | บินต่ำเร็วเข้าหาเป้า เอียงเลี้ยว ไต่ทางลาด แล้วเงยตาม subject ที่ลอยผ่าน | not stated | MATCH |
| [PB.44] | Truck left | Dolly & tracking | เลื่อนซ้ายความเร็วคงที่ แกนเลนส์ตรง subject ไหลไปขอบขวา | not stated | MATCH |
| [PB.45] | Helicopter shot | Aerial & crane | orbit ทวนเข็มจากไกลแบบ gimbal ข่าว แล้ว snap-zoom เข้า detail ใน take เดียว | not stated | MATCH |
| [PB.46] | Crane down | Aerial & crane | ลงตรงจากที่สูงหันหาเป้าตลอด tilt คลายจากก้มชันถึงระดับสายตา | จาก top-down ลงมาถึง subject ระดับสายตา | MATCH |

### C1.3 จำนวนต่อหมวดและข้อควรระวังของข้อมูล
- จำนวนต่อหมวด: Static 1 (PB.01); Pan & tilt 8 (PB.02, 03, 24, 25, 26, 31, 36, 37); Zoom & focus 7 (PB.04, 05, 06, 17, 29, 30, 38); Aerial & crane 6 (PB.07, 08, 09, 43, 45, 46); Dolly & tracking 17 (PB.10, 11, 12, 21, 22, 23, 27, 28, 32, 33, 34, 35, 39, 40, 41, 42, 44); Specialty 7 (PB.13, 14, 15, 16, 18, 19, 20) [PB.01] [PB.36] [PB.38] [PB.46] [PB.44] [PB.20]
- PB.05 Dolly zoom เป็น MISMATCH: prompt สั่ง "The subject's head size stays EXACTLY constant" แต่ในคลิปตัวอย่างหัวโตขึ้นต่อเนื่อง (บันทึกการศึกษาว่า ~2 เท่า, audit ว่า ~3–4 เท่า) — ใช้ข้อความ prompt ได้ แต่คลิปตัวอย่างไม่ใช่หลักฐานว่า prompt ได้ผล [PB.05]
- PB.32 Push past เป็น UNCLEAR: เห็นการเดินหน้าและ reveal แต่ subject ไม่ออกขอบซ้ายตามที่สั่ง และคลิปเปิดผ่านรูประตูซึ่ง prompt ไม่ได้บรรยาย [PB.32]
- PB.11 "Tracking" กับ PB.27 "Side tracking" มีข้อความ prompt เหมือนกันทุกไบต์ (md5 ตรงกัน) ต่างแค่ชื่อและคลิปตัวอย่าง [PB.11] [PB.27]
- PB.17 ชื่อ "Crush zoom" แต่ข้อความเขียน "crash zoom OUT" [PB.17]
- MATCH ที่เบี่ยงบางส่วน: PB.09 horizon ต่ำลงแทน "rises", PB.13 เฟรมท้ายดำจึงตรวจ hold ไม่ได้, PB.14 ตัวอย่างอยู่บนหลังม้า, PB.16 bullet time เป็นแค่ช่วง ~7.5–11.7 s ในคลิป 15 s [PB.09] [PB.13] [PB.14] [PB.16]
- MATCH ที่เบี่ยงบางส่วน (ต่อ): PB.22/PB.44 subject เดินไปกับกล้อง, PB.25 ลดลงทั้งชั้นไม่ใช่ 2.2 → 0.8 m, PB.33 ระยะ 0.8 m หลวมตอนท้าย, PB.34/PB.40 arc ใหญ่กว่า 60 องศาและรัศมีเปลี่ยน, PB.41 รถขับออกระหว่าง move [PB.22] [PB.44] [PB.25] [PB.33] [PB.34] [PB.40] [PB.41]

### C2 Course Pages — ข้อมูลหน้า overview ของ 16 คอร์ส
| CP | คอร์ส | หมวด | ระดับ | นาที (วิดีโอรวมจริง) | บท | ผู้เขียนใน route data | ผู้ดำเนินรายการ (จากบันทึกบทเรียน) |
|---|---|---|---|---|---|---|---|
| [CP.A01] | Blockbuster 4K: The AI Filmmaking Pipeline | movie-making | Intermediate | 40 (39.5) | 10 | Adilet Abish | Adil |
| [CP.A02] | Build an Ultra-Realistic Short Film in 4K | movie-making | Intermediate | 33 (33.6) | 19 | Adilet Abish | Adil |
| [CP.A03] | Add AI VFX to Real Footage | movie-making | Advanced | 12 (11.1) | 11 | Rus Syzdykov | @ADILINTHEWILD |
| [CP.A04] | Make an AI Animated Short | movie-making | Intermediate | 17 (16.6) | 11 | Rus Syzdykov | Adil |
| [CP.A05] | How to evaluate AI filmmaking demos | movie-making | Beginner | 20 (20.4) | 11 | Ziya Rufat | Adil |
| [CP.A06] | The 3-Step Realistic AI Ad Workflow | ugc-social-content | Intermediate | 36 (35.6) | 16 | David Matamoros | "Adil" (อาจถอดเสียงผิด) |
| [CP.A07] | Build an AI Ad Agency with Claude + Higgsfield | ugc-social-content | Beginner | 22 (22.3) | 12 | Rus Syzdykov | Adil + แขก 5 คน |
| [CP.A08] | Seedance 4K: Cinematic Realism | movie-making | Intermediate | 14 (13.9) | 8 | Adilet Abish | Adil |
| [CP.A09] | Build a Brand's Visuals with AI | ugc-social-content | Intermediate | 26 (25.6) | 9 | Rus Syzdykov | Adil |
| [CP.A10] | Make a Cinematic Ad End-to-End | ugc-social-content | Intermediate | 46 (46.1) | 10 | Mariam Barova | Adil |
| [CP.A11] | Automate a Faceless Niche Channel | automate-agents | Intermediate | 10 (10.4) | 11 | Rus Syzdykov | Adil |
| [CP.A12] | Build a Faceless Channel | ugc-social-content | Beginner | 14 (14.4) | 7 | Rus Syzdykov | Adil |
| [CP.A13] | Mix AI with Real Footage | ugc-social-content | Intermediate | 5 (4.6) | 10 | Mariam Barova | Adil |
| [CP.A14] | Build 3D Games with MCP | automate-agents | Beginner | 12 (12.0) | 10 | Mariam Barova | Adil |
| [CP.A15] | Direct a cinematic AI car commercial | ugc-social-content | Intermediate | 35 (35.1) | 11 | Adilet Abish | Adil |
| [CP.A16] | Direct AI fight scenes through controlled iteration | movie-making | Intermediate | 16 (15.7) | 5 | Ziya Rufat | ไม่ชัด (Claude ทักว่า "Adil") |

### C2.2 รูปแบบที่พบทุกหน้า
- รวม 16 คอร์ส 171 บท; ผลรวม duration_minutes บนหน้า 358 นาที และทุกคอร์สต่างจากวิดีโอรวมจริงไม่เกิน 1 นาที (ห่างมากสุดคือ A03 12 vs 11.1) [CP.A03] [CP.A10]
- ทุกหน้าแสดง byline เดียวกันว่า "Taught by the team / Higgsfield Creative" และไม่มีหน้าใดแสดงชื่อผู้เขียนใน route data บนหน้าจอ [CP.A01] [CP.A13]
- ผู้เขียนใน route data มี 5 คน: Rus Syzdykov 6 คอร์ส, Adilet Abish 4, Mariam Barova 3, Ziya Rufat 2, David Matamoros 1; bio ของ Matamoros และ Barova บอกว่าเป็นผู้เขียนบทความ GenAI [CP.A07] [CP.A01] [CP.A13] [CP.A05] [CP.A06]
- ผู้ดำเนินรายการบนกล้องคือ "Adil"/@ADILINTHEWILD ใน 14 จาก 16 คอร์ส ตรงกับชื่อผู้เขียนเฉพาะคอร์สของ Adilet Abish; ข้อสรุปว่าผู้เขียนใน route data คือคนเขียนบทความไม่ใช่คนในวิดีโอเป็นการอนุมานที่ยังไม่ยืนยัน [CP.A01] [CP.A10] [CP.A16]
- ช่องที่ว่างทุกหน้า: examples, metadata.languages/models/skills/tools, objectives[].description; has_examples, has_certificate และ certificate_unlocked เป็น false ทั้งหมด [CP.A02] [CP.A09]
- คำอธิบายคอร์สอยู่แค่ใน route data และ meta tag ไม่อยู่ในข้อความที่มองเห็น ส่วนรายการ "Skills you'll learn" เท่ากับชื่อ objective และ "N modules" เท่ากับจำนวนบท [CP.A13] [CP.A04]
- Reading minutes ไม่สัมพันธ์กับความยาววิดีโอ เช่น A10 อ่าน 32 นาทีต่อวิดีโอ 46 นาที, A15 อ่าน 22 ต่อ 35 [CP.A10] [CP.A15]
- preview_media เป็นวิดีโอบทที่ 1 เสมอ; featured_position มีเฉพาะ A01=0, A02=1, A03=2, A06=3; บททั้ง 10 ของ A01 ไม่มี video_poster ขณะที่คอร์สอื่นมีครบ [CP.A01] [CP.A02] [CP.A03] [CP.A06]
- หมวด: movie-making 7, ugc-social-content 7, automate-agents 2; ระดับ: Intermediate 11, Beginner 4, Advanced 1; เผยแพร่ 2026-07-18 ถึง 2026-08-09 และ updated_at เป็น 2026-10-07 จำนวน 12 คอร์ส 2026-08-10 จำนวน 4 คอร์ส [CP.A01] [CP.A15] [CP.A16]
- หน้าคอร์สบอกเครื่องมือน้อยมาก (metadata.models/tools ว่างทุกหน้า) แต่บทเรียนพึ่ง Claude + custom skill, Seedance 2.0, Soul Cinema, GPT Image 2, Nano Banana Pro, Higgsfield MCP และ Adobe Premiere Pro สำหรับ A13; A05, A09, A10, A15, A16 ไม่ระบุเครื่องมือเลยบนหน้า [CP.A05] [CP.A13] [CP.A15]

### C2.3 ข้อผิดพลาดของหน้าเทียบกับบทเรียน
- A13: ชื่อบทที่ 2 บนหน้าเขียนตรงตัวว่า "Setting Up the Quixel Plugin" แต่เครื่องมือจริงคือ Higgsfield plugin สำหรับ Premiere (ดูภาค E1) [CP.A13] [A13.L02 t=00:00]
- A13: หน้าไม่บอกว่าต้องใช้ Adobe Premiere Pro และไม่พูดถึงเครดิตต่อการทำงาน [CP.A13]
- A05: หน้าไม่บอกว่าบทเรียนตัดมาจากการเทียบ Seedance 2.5 กับ 2.0 [CP.A05] [A05.L01 t=00:27]
- A12: การเขียน script ด้วย "One Prompt" อาศัย memory จาก session ก่อน [CP.A12] [A12.L03 t=01:35]
- A07: หน้าพูดถึงการทดสอบ prospects แต่คอร์สไม่แสดงผลลัพธ์ใด ๆ [CP.A07] [A07.L12 t=00:58]
- A16: ไม่มีบทใดที่ title card เป็น Beat 4 และการ์ด "BEAT 5" โผล่ท้าย L04 [CP.A16] [A16.L04 frames t=02:00]

## ภาค D — เนื้อหาที่มีเฉพาะในวิดีโอ (v1 ไม่มี)

### D1 เส้นทาง UI และการตั้งค่าที่เห็นเฉพาะบนจอ
- ติดตั้ง skill ใน Claude: Customize → Skills → + → Upload a skill และเมนู Add มี "Create with Claude" / "Write skill instructions" / "Upload a skill"; A09 ผ่าน Create skill → Upload a skill [A01.L04 t=00:15-00:25] [A01.L04 t=00:20] [A09.L04 t=02:01–02:20]
- รายการ skill อื่นที่ผู้สอนติดตั้งไว้ (seedance-clean, seedance-shotlist-director, seedance-footage-vfx, character-sheet, cinematic-workflow-breakdown, seedance-director ฯลฯ) ขณะที่บทความเอ่ยถึงแค่ skill เดียว [A01.L04 frames t=00:19]
- ชื่อ skill ที่อ่านได้จากจอหรือวัสดุแต่ละคอร์ส: `higgsfield-seedance-prompt` (A01), SKILL_prompt_workbench.md (A02), seedance-prompt-structure (A10), game-studio (A14), "Seedance prompt generator" (A15), higgsfield-cinematic-seedance-skill (A16) [A01.L04 t=00:15-00:25] [A02.L06 article] [A10.L01 frames t=00:35] [A14.L02 frames t=00:15] [A15.L03 t=01:17] [A16.L01 t=01:42]
- ขั้นตอน Elements (แท็บ, Create element, ช่องชื่อ, Category "Auto") มีแค่ในวิดีโอ และเมื่อวาง prompt ของ Claude ลง Seedance thumbnail ของ reference เติมเองเป็น element chip [A10.L04 t=00:06–00:36] [A10.L04 t=01:51–01:56] [A15.L01 t=02:45]
- Connector: endpoint จริง `https://mcp.higgsfield.ai/mcp` ต่างจากหน้า setup `higgsfield.ai/mcp` และหน้า OAuth consent มี scope, Deny/Allow และ redirect กลับ claude.ai [A07.L03 frames t=00:31] [A07.L03 frames t=00:33] [A12.L02 t=00:25]
- หน้า Higgsfield แนะนำให้ผู้ใช้ Claude Code ใช้ CLI แต่ผู้สอนใช้ custom connector ผ่าน UI ของ Claude [A12.L02 frames t=00:13] [A12.L02 t=00:27–00:36]
- Plugin ใน Premiere: dock เป็นคอลัมน์ซ้ายมีแถบ "Last generations" และ "Apps", เข้าคิวงานได้, Reframe 3 format รันขนานเป็น 3 card และโมเดลที่ใช้คือ Seedance 2.0 (16:9 / 1080p, ผล 4s) [A13.L02 t=00:20] [A13.L07 t=00:10] [A13.L09 t=00:10] [A13.L01 frames t=00:35]
- กล่อง input ของ Claude จริง: thumbnail คลิป → skill tag บรรทัดแยก → คำขอประโยคเดียว → ตัวเลือกโมเดลมุมขวาล่าง [A03.L02 t=00:35-00:40]
- Panel Seedance เข้าคิวสาม prompt ใต้ปุ่ม GENERATE เดียวจากคลิปเดียว และ `@source` ถูก highlight เขียว [A03.L03 frames t=00:34] [A03.L07 frames t=00:47]
- แถบ Seedance ที่อ่านได้: A01 ตั้ง 21:9, 4K, 15 s, 4 batches; A07 9:16, 15s, Audio; A15 L09 "Seedance 2.0", "Auto", "4k", "8s", "4/4", "High", ลำโพง "On", "Unlimited" [A01.L05 t=00:02-00:05] [A07.L04 frames t=00:36] [A15.L09 frames t=00:32]
- เส้นทาง Soul Cinema: เมนู Image → Higgsfield Soul Cinema → แถบ settings → GENERATE ได้ 4 ภาพ และใช้แกลเลอรีโปรเจกต์เดียวต่อทุกฉาก [A04.L03 t=00:30-00:40] [A04.L06 t=00:15]
- UI ของ Marketing Studio: "TURN ANY PRODUCT INTO A VIDEO AD", gallery "Generate across formats", sidebar "New project / Search / URL to Ad / Projects" [A09.L04 t=00:00]
- หน้า onboarding เกม: "MAKE GAMES WITH HIGGSFIELD MCP IN CLAUDE" 3 ขั้น และ interview แบบ multiple-choice มี "Something else" กับปุ่ม Skip [A14.L07 frames t=00:05] [A14.L05 frames t=00:35]
- PROJECT TIMELINE: คลิปที่เลือกถูกขอบเขียวแล้วลากลง timeline และ A15 ใช้กราฟิก timeline แสดงช่องว่างระหว่างฉาก [A01.L05 frames t=01:30] [A15.L05 frames t=00:00]

### D2 ราคาและเครดิตที่อ่านได้จากจอ (as-recorded ณ วันถ่าย)
- A01: ตัวเลขบนปุ่ม GENERATE ของโมเดลต่าง ๆ 28 / 7 / 0.5 / 1,320 / 660 / 176 อ่านได้จาก hires frames เท่านั้น [A01.L03 frames t=01:03] [A01.L05 frames t=00:05] [A01.L08 frames t=01:24]
- A02: Soul Cinema -0.25, GPT Image 2 12 และ 48, Seedance 990 ขีดฆ่าเหลือราว 1,170 [A02.L04 frames t=01:00] [A02.L09 frames t=02:09] [A02.L06 frames t=01:14]
- A03: 330 บนปุ่ม GENERATE ใน L07 เป็นตัวเลขราคาเดียวของคอร์ส [A03.L07 frames t=00:47]
- A04: บนจอเขียน 100 generations = 12.5 credits ขณะที่บทความให้แค่ 0.5 [A04.L03 t=00:15]
- A06: ตัวนับท้ายคอร์ส GENERATIONS 56 และ CREDITS อย่างน้อย 6,725 (เป็น animation ไม่เห็นค่าสุดท้าย) [A06.L16 frames t=01:04]
- A09: Soul Cinema ✦0.5, Nano Banana Pro ✦2/4/16, Marketing Studio อ่านได้บางส่วน "✦ 180 165" [A09.L02 frames t=00:35] [A09.L03 frames t=01:00] [A09.L08 frames t=02:04] [A09.L04 frames t=00:02]
- A10: 40 รูป = 5 credits, Soul Cinema ✦0.5, GPT Image 2 ✦7/12/4, Seedance 15s 2/4 = 270 [A10.L02 t=01:42–02:00] [A10.L02 frames t=04:13] [A10.L06 frames t=03:03]
- A11–A12: shorts batch ราว ~180 credits; วิดีโอ faceless ~2,500 credits รวม และจ่ายซ้ำราว ~3,000 credits [A11.L09 frames t=00:10] [A12.L04 frames t=01:05] [A12.L05 t=00:50]
- A14: ต้นทุนเกมที่อ้างคือ $68 แต่การแบ่งต่อเกมไม่ชัด [A14.L09 t=00:00] [A14.L09 frames t=00:05]
- A15: Seedance 4k 8s 4/4 ปุ่ม GENERATE "832" ขีดฆ่าเหลือ "704" และ L02 เห็น "10,000 free gens left" [A15.L09 frames t=00:32] [A15.L02 frames t=02:00]
- A16: ตัวเลขบนปุ่ม Generate 720→540 และ 390→330 [A16.L02 frames t=01:22] [A16.L05 frames t=00:10]

### D3 Prompt และ brief ตัวเต็มที่มีเฉพาะบนจอ (ต่างจาก cue หรือบทความ)
- A01: บทเป็นบล็อก "BEAT N." ที่มี camera language ในบท และ prompt ฉากป่าที่ Claude เขียนใหม่มีส่วน "WARDROBE STATE SWAP — HARD CONTINUITY RULE" ซึ่งไม่อยู่ในบทความหรือ cue [A01.L02 frames t=00:37] [A01.L08 t=04:50-04:55]
- A02: คำขอแก้บนจอระบุ choreography ของสายตาละเอียด และ Claude แนะนำให้เปลี่ยนลายยุ่งเป็น "subtle marbled print" เพราะ "busy patterns are the most common consistency breaker" [A02.L07 frames t=00:27-00:33] [A02.L04 frames t=00:35]
- A03: คำขอ temple บนจอให้ผู้ใช้บรรยาย action และชนิดกล้องของตัวเองก่อนคำสั่ง lock และคำขอ snake เป็นแบบปลายเปิด ("something unexpected") [A03.L08 frames t=00:10] [A03.L05 frames t=00:05]
- A04: prompt ที่วางจริงใน Seedance ฉาก 2 ไม่มี timestamp (subject → Environment → Camera → Style → "No 3D rendering. No photorealism.") และ prompt ใน L05/L07/L08/L09 มีย่อหน้า "Sound design (SFX only, no music)" ต่อท้ายซึ่งไม่มีใน cue (พบจากเฟรมของผู้ตรวจ ดูภาค E2) [A04.L04 frames t=01:15] [A04.L08 t=00:50-01:00] [A04.L07 t=01:00-01:10]
- A06: prompt ตัวเต็มที่ Claude เขียน (character sheet 85mm "nothing cropped", สนาม ARRI "not a glossy ad look", outfit "No visible brand logos anywhere") และ Global Style Prefix ฉบับเต็มพร้อมโครง CUT ที่มีเลนส์ mm [A06.L03 frames t=00:15] [A06.L07 frames t=00:25] [A06.L08 frames t=00:25] [A06.L10 frames t=02:00]
- A06: prompt location สั้นมาก ("Pedestrian street, 3/4 view"; "Warm color palette office, 3/4 view") และบรรทัดแสงของ prefix หลังแก้ "Natural light only ... no contre-jour, no rim backlight" [A06.L07 frames t=01:10] [A06.L11 frames t=02:00]
- A08: prompt บนจอยาวกว่า cue: trailer มี "[STYLE PREFIX]", Render look, Color 60:30:10, Surfaces, Acting, Physics; racing เพิ่ม "DO NOT use it as a frozen keyframe" [A08.L07 frames t=00:07] [A08.L08 frames t=00:07] [A08.L05 frames t=00:21]
- A09: edit prompt จริงของ NBP ("Change the logo in image 1 with a logo from an image 2", "make the icon smaller") และ prompt social ตัวเต็มจาก hires [A09.L03 t=01:00] [A09.L03 t=01:10] [A09.L08 frames t=00:40]
- A10: ข้อความเต็มของ brief และ director note ทุกตัว (ฉาก 3, 4, 6, 7, 8, 9, 10, 12) และแผนที่ location ที่มีพารามิเตอร์ (ถนนยาว 120 m กว้าง 24 m) [A10.L05 t=02:00] [A10.L07 t=01:30] [A10.L09 t=02:50] [A10.L06 t=03:55–04:05]
- A11–A12: ข้อความแผนของ skill (angle "jobsite story"), เหตุผล 10 นาที (เกณฑ์ mid-roll 8 นาที) และรายงานความคืบหน้าของ Claude (script ล็อก, batch, ffmpeg, upload package) [A11.L04 frames t=00:03] [A11.L05 frames t=00:04] [A12.L04 frames t=01:05]
- A14: เนื้อหา design brief เต็ม (controls, อาวุธ 6 ชิ้นพร้อมสถิติ, กติกา sync, map "Desert Temple") และรายงาน deploy (403 retry, ชื่อชน, game_id) [A14.L05 frames t=00:40] [A14.L05 frames t=01:02]
- A15: คำขอที่พิมพ์ให้ Claude จริงทุกฉาก, คำขอ driving bridge "EXACTLY THREE SHOTS, ONLY TWO CUTS" และคำขอ cabin 6 มุมรวม wheel-hub POV [A15.L02 frames t=01:15] [A15.L05 frames t=00:45] [A15.L07 frames t=01:50]
- A16: กฎ reference ของ skill (ทุก @tag ต้องอยู่ใน ACTIVE REFERENCES, ห้าม tag เก่าหรือแต่งขึ้น, ใช้ OUTPUT SETTINGS เฉพาะเมื่อผู้ใช้ขอ) และ prompt ที่ขยายแล้ว (STYLE PREFIX, camera block FPV) [A16.L01 frames t=01:30] [A16.L01 frames t=01:40] [A16.L02 frames t=00:40]

### D4 Caption, overlay และการ์ด pro-tip บนจอ
- A01: "Keep only the close-up face on the character sheet.", "USE BOTH SIDES OF THE LOCATION — CONSISTENT BACKGROUNDS IN EVERY ANGLE." และสามข้อท้ายคอร์ส "ONE FACE PER CHARACTER SHEET" / "SEPARATE LOCATION ASSETS FOR COMPLEX SCENES" / "REVERSE ANGLES FOR CONSISTENCY" [A01.L03 frames t=01:25] [A01.L09 t=01:15] [A01.L10 t=03:40-03:45]
- A02: "PRO TIP: LOCK THE CHARACTER SHEET = LOCK THE VOICE", กราฟิก "SEEDANCE 2.0 / POSITIVE / ~~NEGATIVE~~", การ์ด "FIX #1 - ADD THE PAUSE / FIX #2 - SPLIT THE SCENE" [A02.L06 frames t=01:35] [A02.L07 frames t=00:35] [A02.L17 frames t=01:05]
- A02: overlay สรุปท้ายคอร์สมีสามข้อ (CAMERA MOVES / EMOTIONS / TRANSITIONS) แต่เสียงพูดมีข้อสี่คือ colour palette [A02.L19 t=02:20-02:24]
- A10: "STYLE, LIGHTING, CAMERA, ACTING, PHYSICS" และ "PRO TIP: ADD 'NO MUSIC AND ONLY ENVIRONMENTAL SFX'" [A10.L04 t=01:30–01:40]
- A16: "Think like a director — Choose locations that naturally hide the AI slop.", "Crowd scale is about layering, not high numbers.", "Write camera moves in meters and degrees, not adjectives.", "STEP 1 — Swap bans for direct descriptions." [A16.L03 frames t=01:15] [A16.L03 frames t=01:30] [A16.L03 frames t=02:55] [A16.L05 frames t=01:00]
- A15: "TIGHTER THE FRAME = LESS SLOPP" (ตัดกลางแอนิเมชัน); A08: caption ขีดฆ่า "AI SLOP" / "BURNING CREDITS" [A15.L07 frames t=01:23] [A08.L04 t=01:53]
- A04: overlay บอกสิ่งที่ส่งต่อ "STYLE / CHARACTER / TELEPORT EFFECT" และคำสั่งแก้ "SWAP HAIR TO BLACK AND PUT HIM IN A BLACK SUIT" [A04.L04 t=00:55] [A04.L05 t=00:40-00:45]
- A05: การ์ดวางแผน "30 SEC X 4 = 2 MIN" และ "HOOK — FEATURE — OUTRO" สำหรับ UGC 30 s [A05.L05 t=01:39] [A05.L07 t=01:49]
- การตรวจภาพด้วย overlay: A01 วงแดง/เขียวเทียบ take, A03 วงกลมเหลืองชี้แสงตกบนเสื้อ, A08 วาง ORIGINAL vs GENERATED เคียงกัน, A10 การ์ด BEFORE / AFTER [A01.L03 t=03:00-03:25] [A03.L04 t=00:56-01:01] [A08.L03 t=01:18] [A10.L06 t=05:00–05:05]
- Diagram ธุรกิจบนจอ: A07 ขั้น verify ("INTERESTED" → INTAKE → VERIFY → CLIENT PROFILE SAVED) และ pipeline recap; A14 funnel STEP 1–5 [A07.L07 t=02:24] [A07.L09 t=00:39] [A14.L09 frames t=00:15]

### D5 บทพูดและเสียงที่มีเฉพาะในวิดีโอ
- A02: บทพูดเต็มของหนัง เช่น "Guilt." / "18 years and one second." / "Please, teach me your tricks." [A02.L02 t=00:31] [A02.L02 t=01:17] [A02.L02 t=02:00-02:04]
- A01: บันทึกการพูดบท "Two months?! HELL NAHHH!" แบบเรียบ ขุ่นเคือง เสียงตก และ HARD CUT ที่ 4.5 s กับ 7.0 s [A01.L09 frames t=03:02]
- A04: ฉาก 1 มีเสียงพูดของข้อความ UI ("I'll be in the cafe in 10 minutes") และหนังเต็มมีบทพูดภาษาญี่ปุ่นในช่วงมังงะ [A04.L03 t=02:18] [A04.L11 t=01:02]
- A05: บท UGC เต็มที่ได้ยินใน output ("Okay, so we're at like 2,000 meters right now.") และ dialogue ฉาก war council [A05.L07 t=00:15] [A05.L09 t=00:02]
- A06: บทพูดของหัวหน้า "Where the hell have you been? ... third time this week" และ "I'm on my way." [A06.L01 t=00:36] [A06.L01 t=00:33]
- A07: สคริปต์โฆษณาที่ได้ยินพร้อม CTA แบบ comment-keyword ("comment SPOT", "comment SELL") [A07.L04 t=00:38] [A07.L04 t=01:07] [A07.L04 t=02:12]
- A08: บทพูดในคลิปการ์ตูนถูก prompt ไว้ ("Okay — today's the day, I can feel it in my fur!") และโมเดล generate เสียงพูด [A08.L04 frames t=01:30] [A08.L04 t=01:14]
- A09: avatar รีวิวใช้ชื่อสินค้าที่ scrape จากเว็บ ("the Velocity Pant ... this nylon is so crispy") [A09.L09 t=01:13–01:28]
- A15: บทพูด iteration 1 ของฉากด่าน ("Are you serious? Change what? No!") มีเฉพาะในเสียง [A15.L08 t=00:22]

### D6 พฤติกรรมของโมเดลที่เห็นในผลลัพธ์ (ข้อสังเกต)
- Seedance relight ตามข้อความ: keyframe ฉาก 4 แสงเย็นเทาฟ้า แต่วิดีโอออกมาเป็น neon ชมพู/ฟ้าตาม prompt [A04.L06 t=00:30] [A04.L06 t=01:05-01:15]
- Seedance เพิ่มสิ่งที่ไม่ได้สั่ง: รอยลิปสติกบนแก้มตัวเอก (A04) และ 2.5 รวม cat + robot เป็น "cyborg cat" (A05) [A04.L09 t=00:40-00:50] [A05.L06 t=02:38]
- ผลเปลี่ยน background relight subject ให้เข้ากับ sunset ไม่ใช่แค่เปลี่ยน plate; Reframe 4:3 มีหญ้าและฟ้ามากกว่า source (อนุมานว่าขยาย frame) [A13.L06 t=00:15] [A13.L09 t=00:25]
- ชุดในผลมาจาก prompt ไม่ใช่ sheet: เด็กแฟนบอลใส่เสื้อยืดกากีใน sheet แต่ใส่ชุดฟุตบอล maroon/pink ใน 8B [A02.L18 t=01:05-01:30]
- HUD ในคลิป cathedral อ่านเป็นชื่ออื่นจาก prompt ("THE DROWNED CARDINAL" แทน "The Hollow Cardinal") [A08.L08 frames t=00:25] [A08.L08 frames t=00:40]
- ความล้มเหลวของ detail: shimmer makeup เละเมื่อหันหน้า; ส่วนสัญญาณคุณภาพคือ spotlight beam ในอากาศและ "Reflections ... now they're kind of a flex" [A05.L05 t=01:30] [A05.L05 t=00:46]
- "หนึ่งตัวละคร" ของ A01 ถือด้วยเรื่อง ไม่ใช่ทรงผมเดียวกันเป๊ะ (ผมสั้นในทะเลทราย ผมยาวในป่า — ข้อสังเกตของผู้จด) [A01.L01 t=02:00-04:00]
- effect ตัวที่ 5 ใน A08 L03 เป็นมือกลายเป็นเปลือกไหม้มีรอยแตกเรืองส้ม ไม่มีใน article/cue [A08.L03 frames t=01:25]

### D7 ตัวเลขธุรกิจและแพลตฟอร์มบนจอ (ไม่มีแหล่งอิสระ)
- A11: ตาราง RPM/CPM ของ Claude (Education $8–20, AI/tech $15–35, Travel $4–14, Entertainment $2–8) และการ์ด vidIQ ($1.6K/เดือน ที่ 5.7M views) [A11.L03 frames t=00:15] [A11.L03 frames t=00:48]
- A11: กราฟิก "ONE NICHE → 154 → 348 SUBSCRIBERS / SWITCHING NICHES → 11 → 26" และสถิติภาษา English 25.9% ไม่มีแหล่งที่มา [A11.L03 t=01:00–01:05] [A11.L06 frames t=00:20]
- A12: การ์ด vidIQ ของ Bright Side (Est. monthly earnings $39.5K), การ์ด YPP เพิ่มเงื่อนไข "10M valid public Shorts views" และตัวเลข Studio 3 วัน (Views 7.3K, Watch time 213.7 h, Subscribers +27) [A12.L01 t=01:05] [A12.L06 frames t=00:07] [A12.L07 t=00:05]
- A07: คำตอบ niche ของ Claude (Roofing "~6% annually toward $46B+ by 2031") และกราฟ "1 CLIENT A WEEK = $2,000 A MONTH" [A07.L01 frames t=01:24] [A07.L12 frames t=00:46]
- A14: หน้า listing ใน marketplace (users/remixed) และป้ายชื่อ CEO Smilegate พร้อม subtitle เรื่องการ prototype [A14.L08 frames t=00:00] [A14.L10 frames t=00:20]
- คำกล่าวเทียบต้นทุนกับงานสตูดิโอ (creature artists/trackers, body-rig หลายพันดอลลาร์, CGI crowd หลายเดือน) เป็นคำพูดของผู้สอน ไม่มีตัวเลขยืนยัน [A03.L11 t=00:00-00:21] [A06.L12 t=04:36] [A16.L03 t=00:16]

## ภาค E — จุดที่คอร์สขัดแย้งกันเอง และช่องว่างหลักฐาน

### E1 จุดขัดแย้งหลักที่ต้องรู้ก่อนใช้ cue
- A08 L04↔L05 cue สลับกัน: วิดีโอ L04 เล่นการ์ตูนสัตว์ประหลาดในวิหารป่า (panel บนจอเป็น prompt ป่า) ส่วนวิดีโอ L05 เล่น clown golem (panel เป็น prompt clown) และ article ช่อง 3 ของ L04 ก็ไม่ตรงกับวิดีโอ — v1 ที่บอกว่า L04 มี clown จึงผิด ให้ยึดภาพบนจอเมื่ออ้าง cue สองตัวนี้ [A08.L04 frames t=01:30] [A08.L05 frames t=00:21] [A08.L04 article]
- A08 (ต่อ): cue-l5-product ไม่ปรากฏในวิดีโอ L05 (อาจเป็นโฆษณา DERMA.NEURAL ใน L06 — ยังไม่ verify) และช่วง cue-l5-jungle ของ L05 วิดีโอแสดง host กับช็อตควัน/เมฆ [A08.L05 cue cue-l5-product] [A08.L06 frames t=00:05] [A08.L05 frames t=00:07]
- A13 "Quixel" → Higgsfield plugin: ชื่อบทและ article เขียน "Quixel" (transcript ได้ "Kixel") แต่เสียงใน L02 และทุกหน้าจอ (เว็บ, installer, OAuth, panel) เขียน Higgsfield และหน้าคอร์สยังใช้ชื่อบท "Setting Up the Quixel Plugin" — v2 ใช้ชื่อ Higgsfield plugin [A13.L02 t=00:00] [A13.L02 frames t=00:18] [A13.L01 t=00:54] [CP.A13]
- A02 16:9 vs 21:9: เสียงพูดและบทความบอกตั้ง Seedance 16:9 และ chip บนแถบอ่าน 16:9 แต่ทุก cue prompt และ recreate URL ระบุ 21:9 จึงไม่รู้ว่าหนังจริงใช้อันไหน — ยังไม่คลี่คลาย [A02.L06 t=01:09-01:18] [A02.L06 frames t=01:14] [A02.L13 frames t=00:10]
- รูปแบบเดียวกันกลับด้านใน A08 L02 (คำพูดว่า "ultra-wide 21:9" แต่ cue และ panel จบด้วย "16:9, 10 seconds") และ cue sheet ของ A01 มีทั้ง "21:9" และ "16:9" — ต้องดู chip จริงก่อนกดทุกครั้ง [A08.L02 t=00:00] [A08.L02 frames t=00:07] [A01.L03 cue 3-view-character-sheet-recreate]
- A04 "FIRST SCENE" vs "previous scene": บทความบอกให้ส่ง prompt และวิดีโอของฉากก่อนหน้า แต่ overlay "FIRST SCENE PROMPT → CLAUDE" ซ้ำหลายฉาก เสียงพูดว่า "the first video" และ thumbnail ใน Seedance ของ L05–L09 เป็นเฟรมฉาก 1 — หลักฐานภาพเอียงไปทาง "ฉากแรก" แต่ยังไม่สรุป [A04.L04 article] [A04.L05 frames t=00:55] [A04.L06 t=00:44] [A04.L08 t=00:35]
- A04 (ต่อ): ฉากมังงะไม่ได้ใช้ "Extend" แต่เปิดจาก "pure white void" และมี input แค่ character sheet [A04.L07 cue scene5-animated] [A04.L07 t=01:00-01:10]
- PB.05 Dolly zoom: คลิปตัวอย่างไม่ตรงกับ prompt — prompt บังคับให้หัวคงขนาดแต่ในคลิปหัวโตขึ้นต่อเนื่อง คลิปจึงไม่ใช่หลักฐานว่า prompt นี้ได้ผล [PB.05]
- PB.11 == PB.27: ข้อความ prompt ของ "Tracking" กับ "Side tracking" เหมือนกันทุกไบต์ (md5 05b5be4f9a94221e1987e81b9a1fa3f3 ทั้งคู่) ต่างแค่ชื่อและคลิป; audit ระบุด้วยว่าคำสั่งตรวจใน summary ที่ hash ทั้งไฟล์ไม่ได้พิสูจน์ข้อนี้ ต้องเทียบรายแถว [PB.11] [PB.27]
- A15 L09/L10 เป็น VERIFIED_GAP: สำเนา article ถูกบล็อก จึงไม่มี article ของ L09 และหัว article ของ L10 เนื้อหาสองบทนี้มาจาก transcript + frames เท่านั้น และชื่อบทได้จาก browser ("Stabilize a comic set piece", "Block the finale backward") [A15.L09 t=00:00] [A15.L10 t=00:00]
- A15 L08 (ผลข้างเคียงของ GAP): prompt ทางการถูกตัดกลางประโยคโดย GAP marker ("A soft breathy voice colo") จึงมีแค่ครึ่งแรก และ article ยังใช้บทพูดเก่าขณะที่ตัดต่อจริงใช้ "Change? No." [A15.L08 article] [A15.L08 t=01:57]

### E2 Writer flags ที่ตัดสินแล้วใน v2
- A15 เรื่องเครดิต: wrap-up ของคอร์สบอกว่าไม่มีราคาเครดิตเลย แต่เฟรม L09 เห็นปุ่ม GENERATE "832" ขีดฆ่าเหลือ "704" (Seedance 2.0, 4k, 8s, 4/4) และ L02 เห็น "10,000 free gens left" — v2 ตัดสินให้ยึดเฟรม: มีตัวเลขบนปุ่ม แต่ไม่มีการพูดถึงราคาหรือต้นทุนรวม ข้อความ wrap-up จึงไม่ถูกตามตัวอักษร [A15.L09 frames t=00:32] [A15.L02 frames t=02:00]
- A15 L10 ส่วน article-tail: หลัง GAP ยังเหลือ prompt block A "Lock the goodbye dialogue" (10s, 4 ช็อต/3 cut) และ block B "Clear the drift parking area" (4s ช็อตเดียว) ผู้ audit ตรวจว่าตรง แต่ wrap-up บอกว่า "intentionally not used" ขณะที่ note บอกว่าเพิ่มในรอบหลัง — v2 ติดป้ายเป็นหลักฐานบางส่วน อ้างครั้งเดียว ไม่ใช้เป็นแหล่งหลัก [A15.L10 article-tail]
- เนื้อหาหลักของ A15 L10 ใน v2 จึงมาจาก transcript + frames: วางกลางฉากก่อน, แก้จุดจอดที่มีรถขวางก่อนเลือกภาพสวย และใช้ diagram วาดมือกับ `@position` [A15.L10 t=01:22] [A15.L10 t=02:42] [A15.L10 frames t=00:15]
- A04 บรรทัด "Sound design (SFX only, no music)": มาจากเฟรมที่ผู้ตรวจดึงเอง (audit/A04-details.md: prompt ที่วางบนจอใน L05/L07/L08/L09 มีย่อหน้านี้ต่อท้าย, ส่วน A04.L08 อ้างเฟรม t=55) ไม่ได้มาจาก cue หรือ transcript และผู้สอนไม่เคยพูดเรื่อง sound design — v2 ถือเป็นเนื้อหา prompt บนจอ ไม่ใช่สิ่งที่คอร์สสอน [A04.L08 t=00:50-01:00] [A04.L07 t=01:00-01:10] [A04.L08 frames t=00:55]

### E3 กฎที่คอร์สสอน vs สิ่งที่คอร์สทำเอง
- กฎห้าม negative: A02 สอนว่าห้ามใช้ negative กับ Seedance 2.0 แต่คำขอของผู้สอนเองยังมี "dry face with no tears" และ prompt ภาพนิ่งของ Claude มีรายการ "NO ..." หนัก (กฎระบุไว้สำหรับ Seedance เท่านั้น) [A02.L07 frames t=00:27-00:33] [A02.L09 frames t=02:05] [A02.L09 cue ball-prop-sheet]
- กฎห้าม negative (ต่อ): skill ของ A16 บอกให้เปลี่ยนข้อห้ามเป็น positive แต่ camera block ที่ขยายแล้วยังมี "no sideways drift, no rotation, no tilt" และ block แรกของเวอร์ชันลุคเกมเต็มไปด้วย "NOT ... NO ..." [A16.L01 frames t=01:30] [A16.L02 frames t=01:05] [A16.L05 frames t=00:10]
- กฎห้าม negative (ต่อ): คอร์สอื่นใช้ negative เป็นเครื่องมือตั้งใจ — A04 สไตล์ขาวดำใช้ "zero color", "zero 3D", A08 แยกหมวด FORBIDDEN และ Prompt Bank 41/46 มีรายการ "no X" ของ move ข้างเคียง; การอ่านของ v2: ข้อห้ามที่คอร์สเตือนคือการบรรยายสถานะ/อารมณ์ด้วยคำปฏิเสธ ไม่มีหลักฐานว่าคอร์สเลิกใช้ exclusion list ของกล้องหรือ style lock [A04.L07 cue scene5-animated] [A08.L01 cue cue-l1-kaiju] [PB.38]
- "No music": Global Style Prefix ของ A06 บอก "No music" แต่ฉาก 3 ใส่ music track เป็น audio input และ prompt ฉาก 5 ยังมีบรรทัด "No music" — ไม่ชัดว่าฉากอื่นใน shot list สุดท้ายเก็บบรรทัดนี้ไว้หรือไม่ [A06.L13 frames t=04:35] [A06.L15 frames t=00:40]
- 4K: A08 ชูเรื่อง 4K แต่ลิงก์ Recreate เกือบทั้งหมดเป็น 1080p และไม่เห็นวิธีเลือก 4K ใน UI; A05 แสดงว่า 2.5 ยังเป็น 720p และไม่ชัดว่าถาวรหรือเป็น setting ก่อน release [A08.L01 cue cue-l1-kaiju] [A08.L01 frames t=02:46] [A05.L11 article]
- ราคา Soul Cinema บันทึกไม่ตรงกัน: A01 "8 ภาพต่อ 1 credit", A04 4 ภาพ = 0.5 credit (100 = 12.5), A02 อ่านได้ -0.25 และ A08 "eight batches for one credit" ไม่ตรงกับ stepper 4/4 บนจอ [A01.L03 t=03:01-03:31] [A04.L03 t=00:15] [A02.L04 frames t=01:00] [A08.L06 frames t=01:42]
- Automation: A07 พูด "I touch nothing" และ "If it passes, send it" ขัดกับ approval gate ใน article; A12 พูดว่า "I didn't write a single correction" แต่บนจอ Claude แก้เองทั้งการ resubmit คลิปที่โดน filter และการยืด VO [A07.L07 t=02:40] [A07.L09 t=00:28] [A07.L09 article] [A12.L05 t=02:03] [A12.L05 t=00:10]
- "One prompt": A12 บอกว่า script มาจาก prompt เดียว แต่บนจอ Claude เรียก memory และบอกว่า shot list มีอยู่แล้วจาก session ก่อน จึงไม่รู้ผลในบัญชีใหม่ที่ไม่มี memory [A12.L03 t=01:35] [A12.L04 t=02:48–02:56]
- Cue ไม่ใช่ prompt สุดท้ายเสมอ: A01 cue เขียน RED durag แต่ผลเป็นผ้าโพกหัว YELLOW, A09 prompt TV Spot ที่วางจริงไม่ตรงกับ c7a และ cue ของ A13 L01/L04/L06 บรรยาย footage ที่ไม่ปรากฏใน tile ที่สุ่มดู (หน้าคอร์สชี้ว่าตรงกับ footage ของ A03) [A01.L03 cue 3-view-character-sheet-recreate] [A09.L07 frames t=00:47] [A13.L04 cue cue-add-figure-behind] [CP.A13]
- ภาพ reference ชนะข้อความ: A04 ฉาก 1 สั่ง "2D anime illustration, cel-shaded" แต่ผลเป็น paper-cutout ตาม keyframe และฉากจบสั่ง "photorealistic" แต่ผลเป็น 3D stylized (อนุมานว่า image_1 ชนะข้อความ) [A04.L03 cue scene1-animated] [A04.L10 cue scene8-animated] [A04.L10 t=00:50-01:10]
- กฎ "one niche" ของ A11 กับการลงเวอร์ชันแปลภาษาในช่องเดียวกันไม่ได้อธิบายว่าเข้ากันอย่างไร [A11.L03 t=00:56–01:08] [A11.L06 article]

### E4 ช่องว่างหลักฐานที่พบซ้ำหลายคอร์ส
- ไฟล์ skill ไม่อยู่ในวัสดุคอร์ส เห็นแค่ output หรือคำอธิบายบางส่วน จึงไม่รู้กฎเต็มของ skill [A01.L04 t=00:25-00:30] [A06.L10 cue download-shotlist-skill] [A10.L10 t=02:23–02:29] [A14.L02 t=00:17] [A16.L01 t=01:42]
- "prompts in the description" ถูกอ้างแต่ไม่มีในไฟล์คอร์ส [A02.L18 t=01:08-01:13] [A04.L11 t=02:13] [A09.L08 t=00:55] [A11.L02 t=00:19–00:20]
- ไม่มีตัวเลขเครดิตหรือจำนวน generation รวมของงานทั้งชิ้น มีแค่คำพูดอย่าง "400 generations" หรือ "100 tries" [A01.L03 t=00:00-00:17] [A02.L04 t=01:02] [A04.L06 t=01:17] [A10.L10 t=02:14–02:22] [A13.L10 frames t=00:07]
- ไม่แสดงโปรแกรมตัดต่อ การ stitch และการใส่ score [A02.L08 t=01:43-01:46] [A04.L11 t=01:55-02:08] [A10.L04 frames t=06:10]
- ป้ายโมเดล Claude ไม่ตรงกันข้ามคอร์สและภายในคอร์ส ("Fable 5 · High", "Opus 4.8 High", "Opus 5 · High", "Sonnet 5 Medium") และไม่แน่ว่า "Fable 5" อ่าน chip ถูกหรือไม่ [A01.L02 frames t=00:12] [A03.L08 frames t=00:10] [A07.L07 frames sheet_02 tile 12] [A11.L02 frames t=00:02] [A15.L02 frames t=00:05]
- Chip บนแถบ settings หลายตัวไม่เคยถูกตั้งชื่อ ("On" รูปลำโพง, "High", stepper 1/4 vs 4/4) การตีความจึงเป็นการเดา [A01.L05 frames t=00:05] [A04.L03 frames t=00:35] [A08.L06 frames t=01:42]
- ชื่อผู้ดำเนินรายการไม่ตรงกับผู้เขียนที่เครดิต (เช่น วิดีโอแนะนำตัว "Adil" แต่ metadata เครดิต Ziya Rufat) [A05.L01 t=00:10] [A16.L01 frames t=01:55] [CP.A05] [CP.A16]
- Transcript มี whisper hallucination ที่ห้ามอ้างเป็นบทพูด ("Oh, my God" 22 ครั้งบนเพลง, "I'm sorry" 5 ครั้ง, "10 million dollars" จากเสียงเกาหลี, "$400,000" ที่จริงคือ WEBSITE $400) [A10.L01 t=01:54] [A16.L03 t=03:40] [A14.L10 frames t=00:25] [A07.L12 t=00:15]
- ผลทางธุรกิจไม่ได้ validate: A07 ไม่มีผล outreach ใด ๆ, A12 ผล 3 วันเป็น vanity metrics, A14 ตัวเลขผู้เล่นเป็นการรายงานเอง, A11 ตัวเลขการทดลอง niche ไม่มีแหล่ง [A07.L12 t=00:58] [A12.L07 t=00:05] [A14.L08 frames t=00:00] [A11.L03 t=01:00–01:05]
- ผลบางช็อตไม่อยู่ใน tile ที่สุ่มดู จึงตรวจด้วยภาพไม่ได้ (รถหายใน A13 L03, พวงมาลัย close-up ใน A15 L05, ช็อต 85mm ใน A16 L05) [A13.L03 t=00:08] [A15.L05 t=02:24] [A16.L05 frames t=01:45]

### E5 ดัชนีความขัดแย้งย่อยรายคอร์ส
- A01: ฝั่งแกนกล้อง "TV-wall side" vs "bookshelf-and-doorway side", ลิงไม่ตรงสี ("white macaques" vs grey-brown), prompt สุดท้ายไม่มี transition ทะเลทรายที่คำขอแนบไว้ [A01.L09 cue recreate-4-2a] [A01.L08 cue recreate-3-2b] [A01.L06 cue recreate-1-5c]
- A02: hard cut "After 9s" vs "at 8s", ชุดผู้รักษาประตูเขียว vs เหลือง, speed ramp เข้าประตู vs เซฟ, ชื่อ 8B/8C ไม่ชัด [A02.L06 cue scene-1-two-shot-prompt] [A02.L10 cue flares-fog-handheld] [A02.L13 t=00:55] [A02.L18 t=01:32-01:39]
- A03: เสียงพูดว่ามือกลายเป็นงูแต่ผลเป็นแขนกลสีเงิน, คลิปต้นฉบับเป็นเมืองแต่ cue บอกป่า, duration chip 15s vs cue 8s [A03.L05 frames t=00:35] [A03.L09 frames t=00:05] [A03.L07 frames t=00:47]
- A05: article บอกส่งข้อความให้ "older woman" แต่ sheet แสดงชายชรากับสุนัข [A05.L10 article]
- A06: ตัวนับเครดิตเป็น animation (6 081 → 6 725) จึงใช้ ≥6,725, และ GENERATIONS 56 vs "100 tries" [A06.L16 frames t=01:04] [A06.L16 t=01:30]
- A07: วิดีโอใส่ portfolio 5 ลิงก์ใน email แต่ article บอกลิงก์เดียว และ CTA บนเว็บ deploy drift เป็น "GET A FREE ROOF CHECK" [A07.L06 t=01:40] [A07.L06 article] [A07.L10 frames sheet_03 tiles 8-11]
- A09: ที่มาของ Roko (preset avatar ใน article vs upload ไฟล์บนจอ) และ c3j สั่งพื้นดำ "No logos" แต่ภาพสุดท้ายพื้นขาวมีโลโก้ [A09.L06 t=00:45–00:52] [A09.L03 cue c3j]
- A10: "slight tackle" ใน article/audio vs "SLIDING TACKLE" ใน cue และ WB ของ pack shot 6000K vs "match it to the scene 1" (6500K) [A10.L08 cue cue-scene-10] [A10.L09 cue cue-scene-12]
- A11: "a hundred scenes" vs "60 clips of 10 seconds" และ Shorts ทำในแชตเดียวกัน vs Shorts Studio [A11.L05 t=01:00–01:03] [A11.L11 t=00:00–00:10] [A11.L11 article]
- A12: ระยะเวลาไม่ตรงกัน (shot list 5:00, รายงาน 4:52, VO 5:11, FINAL 4:59) และ thumbnail ที่ upload จริงไม่ตรงกับรายการของ Claude [A12.L04 t=01:05] [A12.L05 frames t=00:35] [A12.L05 t=00:40]
- A14: ผู้สอนบอก marketplace "almost empty" แต่ grid บนจอมีเกมของคนอื่นราว 17 เกม และ remix 120 vs 121 [A14.L07 t=00:19] [A14.L07 frames t=00:05] [A14.L08 t=00:22]
- A16: การแก้แขน "raise the arm" ในเสียง/บทความ vs ชี้แขนตรงเข้ากล้องบนจอ และชื่อ tag @roko_warrior vs @crystal_knight [A16.L02 t=03:33] [A16.L02 frames t=03:45] [A16.L03 cue cue-transformation-brief] [A16.L03 frames t=03:03]

## ภาค F — ตาราง diff v1 → v2

### F1 ตาราง diff
| หัวข้อ | v1 | v2 | ประเภท | ที่มา |
|---|---|---|---|---|
| ขอบเขตหลักฐานของบทเรียน A15 L09/L10 | ไม่ได้บอกว่าสองบทนี้ไม่มี article | ระบุว่าเป็น VERIFIED_GAP เนื้อหามาจาก transcript + frames เท่านั้น | แก้ | [A15.L09 t=00:00] [A15.L10 t=00:00] |
| Prompt Bank หมวดกล้อง | ไม่มี | 46 prompts พร้อมไวยากรณ์ร่วม ตารางดัชนี และผลตรวจภาพ MATCH 44 / MISMATCH 1 / UNCLEAR 1 | เพิ่ม | [PB.01] [PB.05] [PB.32] |
| ข้อมูลหน้า overview ของคอร์ส | มีแค่ดัชนีชื่อคอร์สและจำนวนบท | ระดับ หมวด นาทีเทียบวิดีโอจริง ผู้เขียนใน route data และข้อผิดพลาดของหน้า | เพิ่ม | [CP.A01] [CP.A13] |
| Negative prompt | C3: ไม่มีเหตุให้สรุปว่าห้าม negative ทั้งหมด | คอร์สสอนห้ามบรรยายสถานะด้วยคำปฏิเสธใน Seedance 2.0 แต่ยังใช้ exclusion list และ style lock (ดู E3) | แก้ | [A02.L07 t=00:33-00:48] [A16.L02 t=03:19] [A04.L07 cue scene5-animated] |
| A01 ชื่อ tag ตัวเอก | ยกตัวอย่าง "@hero" | ตัวเอกคือ @eduardo และ @main_character_desert / _jungle / _room | แก้ | [A01.L03 article] [A01.L07 article] |
| A01 skill | ไม่ระบุชื่อ | `higgsfield-seedance-prompt` ติดตั้งผ่าน Customize → Skills → + → Upload a skill | เพิ่ม | [A01.L04 t=00:15-00:25] |
| A01 settings และราคา | ไม่มี | 21:9, 4K, 15 s, 4 batches และตัวเลขบนปุ่ม GENERATE ณ วันบันทึก | เพิ่ม | [A01.L05 frames t=00:05] [A01.L03 frames t=01:03] |
| A01 โครง prompt | ไม่มี | โครง 14 ส่วนของ skill (SCENE CONTEXT ... POSITIVE LOCKS) และ named locks | เพิ่ม | [A01.L05 cue recreate-1b] |
| A01 บทบาทโมเดลภาพ | ไม่แยก | Soul Cinema = raw pass, GPT Image 2.0 = edit/clean sheet | เพิ่ม | [A01.L03 t=04:49-04:58] |
| A01 การเขียนบท | ไม่มี | ขอ "expand my idea" แทน "write me a script" | เพิ่ม | [A01.L02 t=00:22] |
| A01 ความยาวช็อตป่า | ไม่ระบุ | shot 1 ฉากป่าเป็น 8 s ไม่ใช่ 15 s | เพิ่ม | [A01.L08 frames t=01:22] |
| A01 ความขัดแย้งในคอร์ส | ไม่มี | durag สี, ฝั่งแกนกล้อง, สีลิง, transition ที่หายไป | เพิ่ม | [A01.L03 cue 3-view-character-sheet-recreate] [A01.L09 cue recreate-4-2a] |
| A02 negative prompt | ไม่มีกฎนี้ | ห้าม negative กับ Seedance 2.0 เพราะอ่าน "not crying" เป็น "crying" | เพิ่ม | [A02.L07 t=00:33-00:48] |
| A02 อ่าน take ที่พัง | ไม่มี | 4/4 พัง = prompt ผิดไม่ใช่ seed และ "Basic isn't broken" | เพิ่ม | [A02.L07 t=00:21-00:25] [A02.L07 t=01:07] |
| A02 establishing shot | ไม่มีเหตุผล | Seedance ไม่จำตำแหน่งข้าม generation | เพิ่ม | [A02.L12 t=00:04-00:30] |
| A02 whip pan | ไม่มีตัวเลข | A นิ่งถึง -0.3 s, whip ~0.5 s, B นิ่งภายใน +1.4 s และ shot size เดียวกัน | เพิ่ม | [A02.L14 cue whip-pan-prompt] [A02.L14 t=01:05-01:13] |
| A02 ราคา | ไม่มี | Soul Cinema -0.25, GPT Image 2 12/48, Seedance 990 ขีดฆ่า ~1,170 | เพิ่ม | [A02.L04 frames t=01:00] [A02.L09 frames t=02:09] [A02.L06 frames t=01:14] |
| A02 skill | ไม่มี | ไฟล์ SKILL_prompt_workbench.md และวิธีติดตั้ง | เพิ่ม | [A02.L06 article] |
| A02.06 เสียงประจำตัว | "ต้องฟังผลจริงทุกครั้ง" (ความเห็นของ v1) | คอร์สแค่ยืนยันว่า lock sheet = lock voice | แก้ | [A02.L06 t=01:26-01:39] |
| A02.09 สัดส่วนสี | "แนวทางออกแบบของตัวอย่าง" | เขียน 60:30:10 พร้อม % บทบาทลงใน prompt โดยตรง | แก้ | [A02.L09 cue ball-prop-sheet] |
| A02 ความขัดแย้งในคอร์ส | ไม่มี | 16:9 vs 21:9, ชุดเขียว/เหลือง, ลูกเซฟ/เข้าประตู, 8B/8C | เพิ่ม | [A02.L06 frames t=01:14] [A02.L10 cue flares-fog-handheld] [A02.L13 t=00:55] |
| A03 workflow | ไม่มี | Claude อ่านคลิปเป็นเฟรม + Seedance skill เขียน keep-list ผู้ใช้พิมพ์ประโยคเดียว | เพิ่ม | [A03.L02 t=00:21-00:59] |
| A03 รูปแบบคำขอ | ไม่มี | "Seedance prompt for this clip — ... Lock my action and the camera exactly. Turn it into ..." | เพิ่ม | [A03.L08 frames t=00:10] |
| A03 settings และราคา | ไม่มี | 16:9, 4K, duration ต่อ prompt และ 330 credits | เพิ่ม | [A03.L07 frames t=00:47] |
| A03 syntax | ไม่มี | `@source` / `<<<video_1>>>` / `<<<uuid>>>` และการ scope ภาพ reference | เพิ่ม | [A03.L06 cue lizards-climbing] |
| A03.02 การดู motion | "ภาพนิ่งที่ผู้ช่วยเห็นไม่แทนการดู motion" | Claude อ่านวิดีโอเป็นชุดเฟรมและเขียน camera motion ลง keep-list เอง | แก้ | [A03.L02 t=00:21-00:34] |
| A03.10 mood reference | ใช้ภาพ mood ล็อกพายุเป็นขั้นปกติ | mood reference เป็น fallback เมื่อ take หลุด mood ตาม honest flag | แก้ | [A03.L10 cue kraken] |
| A03 honest flags | ไม่มี | flag ท้าย prompt และความเสี่ยง face-drift ในฉากกลางคืน | เพิ่ม | [A03.L10 article] |
| A03 ความขัดแย้งในคอร์ส | ไม่มี | snake vs แขนกล, เมือง vs ป่า, 15s vs 8s | เพิ่ม | [A03.L05 frames t=00:35] [A03.L09 frames t=00:05] [A03.L07 frames t=00:47] |
| A04 ราคา Soul Cinema | ไม่มี | 4 ภาพ = 0.5 credit (100 = 12.5) และ settings บนแถบ | เพิ่ม | [A04.L03 t=00:15] [A04.L03 frames t=00:35] |
| A04 keyframe โลกใหม่ | ไม่มี | เปลี่ยนสองวลี (สไตล์ + สภาพแวดล้อม) | เพิ่ม | [A04.L04 t=00:30-00:37] |
| A04 syntax ต่อวิดีโอ | ไม่มี | "Extend @video1. Continue exactly from the white flash ..." และ "style reference ONLY — DO NOT use the character" | เพิ่ม | [A04.L05 cue scene3-animated] [A04.L06 cue scene4-animated] |
| A04 prop sheet | ไม่มี | สร้างผ่าน Claude → Nano Banana Pro และ character sheet มังงะ | เพิ่ม | [A04.L03 cue scene1-prop-sheet] [A04.L07 cue scene5-manga-sheet] |
| A04.04 วิดีโอต่อเนื่อง | "ส่ง prompt และวิดีโอก่อนหน้า" | หลักฐานภาพชี้ว่าเป็นของฉากแรก (ยังไม่สรุป) | แก้ | [A04.L05 frames t=00:55] [A04.L06 t=00:44] |
| A04.03 ฉาก 1 | เรียกว่า "Papercut" | ผลเป็น paper-cutout แต่ prompt จริงสั่ง 2D anime cel-shaded ลุคมาจาก keyframe | แก้ | [A04.L03 t=02:15-02:35] |
| A04 ฉากจบ | ไม่ระบุ | ไม่ได้ออกมาเป็น photoreal ตามที่บทความอ้าง | เพิ่ม | [A04.L10 t=00:50-01:10] |
| A05 สิ่งที่ถูกเทียบ | ไม่บอกโมเดล | ทั้งคอร์สเทียบ Seedance 2.5 vs 2.0 บน prompt เดียวกันใน 6 หมวด | เพิ่ม | [A05.L01 t=00:27] |
| A05 ข้อจำกัด | ไม่มี | 30 s vs 15 s และ 720p vs 4K (ตัวเลข ณ วันบันทึก) | เพิ่ม | [A05.L02 t=01:38] [A05.L11 t=00:00] |
| A05 การตัดถี่ | ไม่มี | ตัดถี่ตรงจุดยาก = ซ่อน motion | เพิ่ม | [A05.L02 t=01:29] |
| A05 choreography | 4 จังหวะ "เข้าท่า สัมผัส ลงน้ำหนัก คืนสมดุล" | 3 จังหวะ Entry / Contact / Recovery | แก้ | [A05.L05 article] |
| A05 decision record | "รายงานหลายมิติ" | Capability / Constraint / Context / Verdict | เพิ่ม | [A05.L11 article] |
| A05 ความขัดแย้งในคอร์ส | ไม่มี | old woman vs ชายชรากับสุนัข และชื่อ host ไม่ตรง | เพิ่ม | [A05.L10 t=00:07] [A05.L01 t=00:10] |
| A06 เครื่องมือ | ไม่ระบุ | Soul Cinema, GPT Image 2.0, AI Cast, Cinematic Locations, Seedance 2.0, Claude skill พร้อม settings | เพิ่ม | [A06.L01 t=01:22] [A06.L11 frames t=00:40] |
| A06 template | ไม่มี | template prompt จาก cue ครบทุกตัว | เพิ่ม | [A06.L02 cue product-sheet-prompt] [A06.L13 cue street-schematic-prompt] |
| A06 การทดสอบ prop | prop "ควรทดสอบตามความยาก" | props ไม่ต้อง motion test และไม่ต้องทดสอบหลาย candidate | v1 ผิด | [A06.L09 t=00:08] |
| A06 มุมสินค้า | ระวังมุมใหม่ว่าเป็นการเดา | sheet หลายมุมช่วยให้ Seedance "หยุดเดา" | แก้ | [A06.L02 t=00:51] |
| A06 คืนรายละเอียดหน้า | "คืนรายละเอียดส่วนบน" | composite layer + mask เก็บหน้า Soul Cinema หลัง GPT edit | เพิ่ม | [A06.L08 t=01:29] |
| A06 สภาพแห้ง/เปียก | ไม่มี | "images are cheap, videos aren't" และผูก reference กับ cut | เพิ่ม | [A06.L12 t=01:09] [A06.L12 t=01:56] |
| A06 ยอดรวม | ไม่มี | GENERATIONS 56 / CREDITS ≥6,725 | เพิ่ม | [A06.L16 frames t=01:04] |
| A06 style prefix | ไม่มี | Global Style Prefix ฉบับเต็มและโครง CUT ที่มีเลนส์ mm | เพิ่ม | [A06.L10 frames t=02:00] |
| A07 สูตร offer | พูดถึง "ขอบเขต revision" | result / problem / risk / speed+price+bonus / CTA | แก้ | [A07.L02 t=01:30] |
| A07 offer ตัวเต็ม | ไม่มี | สูตร 5 ข้อของ Liam Ottley และ offer ที่ Claude เขียน | เพิ่ม | [A07.L02 t=02:35] |
| A07 connector | ไม่มี | เส้นทาง UI, endpoint `https://mcp.higgsfield.ai/mcp` และ OAuth scope | เพิ่ม | [A07.L03 frames t=00:31] [A07.L03 frames t=00:33] |
| A07 settings ต่อ call | ไม่มี | Seedance 2.0, 9:16, 15s, Audio | เพิ่ม | [A07.L04 frames t=00:36] |
| A07 outreach | ไม่มี | 3 fixes ของ Brock, "The CTA is the filter" และ CAN-SPAM fields | เพิ่ม | [A07.L06 t=01:10] [A07.L06 article] |
| A07 automation | ไม่มี | upgrade 1-3 ของ Nate, recurring promise 5 องค์ประกอบ และ token READY_FOR_HUMAN_REVIEW | เพิ่ม | [A07.L07 t=01:33] [A07.L08 article] [A07.L09 article] |
| A07 เว็บที่ deploy | ไม่มี | CTA drift และ funnel checklist ก่อนแชร์ | เพิ่ม | [A07.L10 article] |
| A08 template | ไม่มี | template จาก cue 16 ตัว รวม INPUT LOCK, HUD LAYER และ POSITIVE LOCKS | เพิ่ม | [A08.L03 cue cue-l3-screen] [A08.L07 cue cue-l7-trailer] |
| A08 L04 | บอกว่า L04 มี "clown" | วิดีโอ L04 เป็นการ์ตูนวิหารป่า clown golem อยู่ใน L05 (cue สลับ) | v1 ผิด | [A08.L04 frames t=01:30] [A08.L05 frames t=00:21] |
| A08 bit depth/bitrate | "ไม่รับประกันโดยชื่อโมเดล" | คอร์สอ้างว่า output 10-bit และสอนตั้ง bitrate High ตอน export (ยังควรตรวจไฟล์จริง) | แก้ | [A08.L05 t=00:37] [A08.L05 t=00:57] |
| A08 โมเดลภาพ | ไม่มี | Soul Cinema vs GPT Image 2 ตามงาน พร้อม generate bar | เพิ่ม | [A08.L06 t=01:23] [A08.L06 frames t=01:42] |
| A08 HUD | ต้องอยู่ในพิกัดจอ | เพิ่มวลี "flat on screen, never in the 3D world" และ "numbers may tick, layout locked" | เพิ่ม | [A08.L08 cue cue-l8-racing] [A08.L07 cue cue-l7-trailer] |
| A09 บทบาท Claude | ไม่พูดถึงเลย | Claude เขียน prompt ทุกขั้นใน thread เดียว | เพิ่ม | [A09.L02 t=00:05–00:15] [A09.L06 t=00:20–00:25] |
| A09 สลับโลโก้ | ไม่มี | Soul Cinema → NBP logo swap แบบ image 1/image 2 และแบรนด์ placeholder | เพิ่ม | [A09.L03 t=01:48–01:56] [A09.L03 cue c3b] |
| A09 ต้นทุนและ setting | ไม่มี | Soul Cinema ✦0.5 ต่อ 4 รูป, NBP ✦16 ต่อ 4 รูป 4K, Marketing Studio 9:16/1080p/15s | เพิ่ม | [A09.L02 frames t=00:35] [A09.L02 frames t=00:55] [A09.L04 frames t=00:02] |
| A09 Marketing Studio | ไม่มี | product จาก URL, upload avatar, ทางเลือก zero-prompt และ timecoded beats | เพิ่ม | [A09.L04 t=00:41–01:52] [A09.L04 cue c4a] |
| A09.05 stress test | "ไม่ใช่หลักฐานความทนทานของสินค้าจริง" | เป็นคำเตือนที่ v1 เพิ่มเอง ผู้สอนนำเสนอเป็น proof content | แก้ | [A09.L05 t=01:44] |
| A09.04 สิ่งที่ตรวจ | "ตรวจ fit มือจับ และขนาดแว่น" | ตรวจโลโก้ต่อเนื่องและแว่นสะอาดเห็นโลโก้ด้านข้าง | แก้ | [A09.L04 t=03:00] [A09.L06 t=02:18–02:33] |
| A09.08 ภาพสตูดิโอเว็บ | "ภาพพื้นเรียบหลายมุม" | side profile 1 รูปจาก prompt สั้น ใส่เสื้อผ้า 5 ชิ้นเป็น reference | แก้ | [A09.L08 cue c8a] [A09.L08 t=01:20] |
| A09.03 รายการสินค้า | ไม่มี jersey/T-shirt | มีครบ 5 ชิ้นและ packaging | แก้ | [A09.L03 t=00:09–00:20] |
| A10 skill | ไม่มี | "seedance-prompt-structure", skeleton และ style prefix ที่อ่านได้จากจอ | เพิ่ม | [A10.L01 frames t=00:35] |
| A10 Elements | ไม่มี | ลงทะเบียน Elements ชื่อตรงกับ @handle เพื่อ auto-attach | เพิ่ม | [A10.L04 t=00:06–00:43] |
| A10 ตัวเลขเครดิต | ไม่มี | 40 รูป = 5 credits, Soul Cinema ✦0.5, GPT Image 2 ✦7/12/4, Seedance 15s 2/4 = 270 | เพิ่ม | [A10.L02 t=01:42–02:00] [A10.L02 frames t=04:13] [A10.L06 frames t=03:03] |
| A10 location scheme | ไม่มี | สูตรครบขั้นพร้อม prompt จริงและการประกาศ @scheme | เพิ่ม | [A10.L06 cue cue-location-scheme] [A10.L06 t=04:30] |
| A10 director note | ไม่มี | ข้อความเต็มและการเน้นด้วยตัวพิมพ์ใหญ่ | เพิ่ม | [A10.L07 t=03:50] [A10.L07 t=05:55] |
| A10.01 คอนเซปต์ | "แยก fantasy ออกจากคุณสมบัติจริง" | คอร์สเน้นหา twist ส่วนตัวให้คอนเซปต์ | แก้ | [A10.L01 t=02:45] |
| A10.03 asset | "ตรวจว่าผู้ช่วยไม่ได้ใส่ asset ที่ไม่มีจริง" | ประกาศ registry "@handle — description" ให้ครบทุก asset | แก้ | [A10.L03 t=01:18–01:52] |
| A10.10 recap | พูดถึง "keeper ledger" | pro tip คือ maps, ใช้ asset ของตัวเองเป็น reference และรันหลาย batch | แก้ | [A10.L10 t=02:03–02:13] |
| A10.04 จุดเสียฉาก 2 | "มือจับกระป๋องและ macro ต้องมี contact" | จุดเสียคือรอยยิ้ม การวิ่งถอยหลัง ตาเปลี่ยนสี transformation ที่นิ่ง | แก้ | [A10.L04 t=03:53–04:20] |
| A11 prompt | ไม่มี | prompt จริง 6 ตัว (prompt-001 ถึง 006) และ Q/A ตอนเลือก packaging | เพิ่ม | [A11.L03 cue prompt-001] [A11.L10 cue prompt-006] [A11.L08 t=00:40] |
| A11 connector | ไม่มี | Add custom connector, Remote MCP server URL, OAuth optional | เพิ่ม | [A11.L02 t=00:05] |
| A11 ความยาว 10 นาที | ไม่มีเหตุผล | เกณฑ์ mid-roll 8 นาที, 150 wpm, 60 × 10 s | เพิ่ม | [A11.L05 frames t=00:04] |
| A11 Shorts และ watch hours | ไม่มี | Shorts Studio (Warm Glow, 9:16, ~180 credits) และ 4,000 h ÷ 4 นาที ≈ 60k views | เพิ่ม | [A11.L09 frames t=00:10] [A11.L09 t=00:39–00:56] |
| A11 voice clone | ไม่มี | เส้นทาง UI และชื่อ preset voices | เพิ่ม | [A11.L07 t=00:00–00:27] [A11.L07 frames t=00:17] |
| A11.06 แปลภาษา | ต้องจัดภาพและ subtitle ใหม่เอง | prompt บรรทัดเดียว "re-renders the whole video" เป็นภาษาใหม่ (คุณภาพคำแปลไม่ได้ตรวจ) | แก้ | [A11.L06 t=00:00–00:26] [A11.L06 article] |
| A11.09 เลือก clip shorts | เลือกประเด็นที่จบในตัว | คอร์สไม่ได้สอน Shorts Studio ตัดและใส่ caption ให้เอง | แก้ | [A11.L09 t=00:08–00:16] |
| A11.03 RPM | "ไม่เป็นค่าคาดการณ์ของช่องใหม่" | เป็นคำเตือนของ v1 คอร์สนำเสนอ vidIQ $1k–$10k/เดือนเป็นเพดาน | แก้ | [A11.L03 t=00:45–00:56] |
| A12 prompt | ไม่มี | prompt จริง 4 ตัว (script / video / package / scale) และ prompt Shorts | เพิ่ม | [A12.L03 cue cue-script-prompt] [A12.L05 cue cue-scale-prompt] [A12.L06 t=00:55] |
| A12 connector | ไม่มี | URL "https://mcp.higgsfield.ai/mcp" และหน้า consent | เพิ่ม | [A12.L02 frames t=00:13] [A12.L02 t=00:25] |
| A12 shot list | ไม่มี | หัว Seedance 2.0 + Inworld TTS Carter, 35 clips, 5/8/10s | เพิ่ม | [A12.L03 frames t=01:37] |
| A12 pipeline และ failure | ไม่มี | ตรวจเครดิตก่อน, ffmpeg, duck 10%, NSFW false flag + refund, VO ยาวกว่า 17s ยืด ~5%, จ่ายซ้ำ ~3,000 credits | เพิ่ม | [A12.L04 frames t=01:05] [A12.L05 t=00:10] [A12.L05 frames t=00:15] [A12.L05 t=00:50] |
| A12 ผล 3 วัน | ไม่มีตัวเลข | 7.3K views, 213.7 h, +27 subs | เพิ่ม | [A12.L07 t=00:05] |
| A12.03 fact-check | ให้คน fact-check ก่อนเป็นเสียงเล่า | Claude fact-check และ research ส่วนที่ขาดเอง (คอร์สไม่ได้ตรวจความถูกต้อง) | แก้ | [A12.L04 t=01:02–01:13] [A12.L04 article] |
| A12.02 CLI vs UI | พูดแยกแบบกว้าง ๆ | Higgsfield แนะนำ CLI ให้ผู้ใช้ Claude Code แต่ผู้สอนใช้ custom connector | แก้ | [A12.L02 frames t=00:13] [A12.L02 t=00:12–00:27] |
| A12.04 ข้อความ "done" | ไม่ยืนยันคุณภาพจากข้อความว่าเสร็จ | ยังถูก และคอร์สมีหลักฐานว่า "done" ซ่อนงานซ้ำและเวลาที่ไม่ตรง | แก้ | [A12.L05 t=00:50] [A12.L04 t=01:05] |
| A13 ชื่อ plugin | ใช้ชื่อ Quixel ตามข้อความบท | Higgsfield plugin ตามเสียงและหน้าจอ | v1 ผิด | [A13.L02 t=00:10] [A13.L02 frames t=00:13] |
| A13 model และ settings | ไม่ระบุ | Seedance 2.0 (16:9, 4s, 1080p, Audio) | เพิ่ม | [A13.L01 frames t=00:35] [A13.L08 frames t=00:14] |
| A13 prompt | ไม่มี | prompt ที่พิมพ์จริงทุกบท ("remove car", "Add an old man to the right") และโครง prompt ยาวจาก cue | เพิ่ม | [A13.L03 frames t=00:07] [A13.L04 frames t=00:12] [A13.L01 cue cue-intro-volcanic-drive] |
| A13 UI | ไม่มี | ขั้นติดตั้ง/OAuth และ UI ของ Draw to edit, Reframe, Upscale (1k/4K) | เพิ่ม | [A13.L02 frames t=00:16] [A13.L09 frames t=00:07] [A13.L10 frames t=00:05] |
| A13 รายการ QC | เงาหลง ขอบแขน ใบหน้าเปลี่ยน ฯลฯ | ไม่มีในบันทึกของคอร์ส คอร์ส "none stated" สำหรับคำเตือน | แก้ | [A13.L03 t=00:00] [A13.L05 t=00:03] |
| A14 setup และ skill | ไม่มี | Customize > Connectors / Skills, skill "game-studio" และ trigger | เพิ่ม | [A14.L02 frames t=00:06] [A14.L02 frames t=00:15] |
| A14 prompt และ brief | ไม่มี | prompt เกมเรือและ Blockfield, คำตอบ interview และโครง design brief | เพิ่ม | [A14.L03 cue pirate-prompt] [A14.L05 cue blockfield-prompt] [A14.L05 frames t=00:40] |
| A14 host และ game_id | ไม่มี | "Fable 5 High", host *.higgsfield.gg, ใช้ game_id ซ้ำ, failure 403/ชื่อชน | เพิ่ม | [A14.L03 frames t=00:14] [A14.L05 frames t=01:02] |
| A14 ตัวเลขผล | ไม่ให้ตัวเลข | ~4,000 ผู้เล่น, สูงสุด 22 คนพร้อมกัน, 121 remixes, ต้นทุน $68 | เพิ่ม | [A14.L08 t=00:00] [A14.L09 t=00:00] |
| A14 CEO | ไม่บอกชื่อหรือคำพูด | ระบุตาม subtitle บนจอ | แก้ | [A14.L10 frames t=00:20] |
| A15 โครง video prompt | ไม่มี | REFERENCE DEFINITIONS / TECHNICAL BLOCK / PROMPT | เพิ่ม | [A15.L03 article] |
| A15 @element | ไม่มี | ใช้ชื่อ `@element` ร่วมกับ Claude และแนบอัตโนมัติเมื่อวาง prompt | เพิ่ม | [A15.L01 t=02:31] |
| A15 models | ไม่ระบุ | Seedream 5.0 Pro, Nano Banana Pro, Soul Cinema, Seedance 2.0 และ settings ที่อ่านได้ | เพิ่ม | [A15.L02 t=00:35] [A15.L09 frames t=00:32] |
| A15 statics และ lock reference | ไม่มี | statics video เพื่อดึง still ที่เข้ากัน และ reference แบบ lock (position, steering wheel) | เพิ่ม | [A15.L05 t=01:44] [A15.L06 article] |
| A15 driving failures | ไม่มี | ไฟจราจร, FPV, overtake, match cut, หน้าปัด และกฎ "tighter the frame" | เพิ่ม | [A15.L07 t=00:49] [A15.L07 t=03:06] |
| A15 L09/L10 เนื้อหา | ไม่มี | fix 4 ข้อของฉากด่าน, diagram + `@position`, แบ่ง 5A/5B/5C | เพิ่ม | [A15.L09 t=00:55] [A15.L10 t=01:31] |
| A15 audit ทั้งหนัง | ไม่มี | 5 รอบ (identity, vehicle, geography, blocking, story) | เพิ่ม | [A15.L11 article] |
| A15 ขั้นตัวละคร | ไม่แยก | แยก "การแสดง" (Soul Cinema) ออกจาก "identity" (face-swap edit) | แก้ | [A15.L02 t=01:48] |
| A16 skill | ไม่มี | "higgsfield-cinematic-seedance-skill" พร้อมกฎและวิธีติดตั้ง | เพิ่ม | [A16.L01 t=01:42] [A16.L01 frames t=01:35] |
| A16 settings | ไม่มี | Seedance 2.0 15s, batch 4, High และตัวเลขบนปุ่ม Generate | เพิ่ม | [A16.L02 frames t=01:22] [A16.L05 frames t=00:10] |
| A16 ตัวเลขกำกับ | ไม่มี | หมอก 20 m, ~40 ทหาร, ขั้น 0.5s, orbit 8→4 m / 3→2 m, snap 0.4s, ช่องว่างใบมีด 5-8 → 2-3 → 1 cm | เพิ่ม | [A16.L03 t=01:00] [A16.L03 frames t=02:47] [A16.L04 frames t=00:40] |
| A16 กฎวัสดุและ match cut | ไม่มี | "crystal always beats steel" และ "EXACTLY match" | เพิ่ม | [A16.L04 t=00:24] [A16.L04 t=01:00] |
| A16 การแก้แขน | "กำกับท่ายกแขน" | คำแก้บนจอคือชี้แขนตรงเข้ากล้องให้ใบมีดสั้นเป็นจุด (ขัดกับเสียง/บทความ) | แก้ | [A16.L02 frames t=03:45] |

## บันทึกฉบับ

2.0 — 7 ตุลาคม 2026. สร้างจากบันทึกการศึกษาราย course (A01–A16) ที่อ้างอิงครบทุกบรรทัด, บันทึก Prompt Bank 46 รายการ, บันทึก Course Pages 16 หน้า และรายงาน audit ของ PB, CP และ A04 ภาค A ประกอบแบบกลไกจากไฟล์ A01–A16 โดยไม่เขียนใหม่ ภาค B–F เขียนจากส่วน "กฎที่ใช้ซ้ำได้", "เนื้อหาที่มีเฉพาะในวิดีโอ", "จุดที่คอร์สขัดแย้ง" และ "เทียบกับ v1" ของแต่ละคอร์ส ภาค B รวมเฉพาะกฎที่สอนตั้งแต่สองคอร์สขึ้นไป กฎที่สอนคอร์สเดียวอยู่ในภาค A ของคอร์สนั้น

ตัวตรวจ `_tools/cite_check.py` ยืนยันว่าทุกบรรทัดเนื้อหาในภาค B–F มีการอ้างอิง แต่ไม่ได้ยืนยันว่าแต่ละอ้างอิงสนับสนุนข้อความ เอกสารนี้ไม่ได้ทดลอง generate ตาม prompt ใด ๆ ไม่ได้เปิดไฟล์ skill ที่คอร์สอ้าง และราคา/เครดิตทั้งหมดเป็นค่าที่บันทึกได้ ณ วันถ่ายคอร์ส

1.0 — 5 ตุลาคม 2026. Mega Bible ภาษาไทย เรียบเรียงจากข้อความบทความของ 16 คอร์ส 171 บท ไม่ได้ชมวิดีโอครบทุกบทและไม่ได้ทดสอบ generation
