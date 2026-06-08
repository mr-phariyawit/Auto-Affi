# 06 — Principles & Company Standards Index

> 17 เอกสารใน [`docs/principles/`](../docs/principles/) — แต่ละฉบับเกิดจาก incident จริงใน production แล้วถูก encode เป็นกฎ เรียงตามวันที่ = เห็นวิวัฒนาการของบริษัท
>
> **ลำดับชั้น:** `company-*` prefix = Company Standard (บังคับทั้งบริษัท) > Runbook (canonical path) > Principle (กฎเฉพาะด้าน) > Review (architecture reference)

## 2026-06-03 — จุดเริ่มต้น

### [Production Review Principle](../docs/principles/2026-06-03-production-review-principle.md)
**Trigger:** Shoe-cover clip สวยแต่ product ดูเหมือน rain boot — "beautiful clip ≠ accurate clip"
**กฎหลัก:** Marketing → Research validation ก่อน run folder เสมอ · video source = silent B-roll · voice speed ≤1.08x warn / >1.15x reject · 30s master default · cleanroom 1+1 streams · Thai text ห้าม generate ใน video model · ทุก run ต้องมี learning log

## 2026-06-04 — วันที่ระบบเกิด (8 ฉบับ)

### [Always-On Viral Intelligence](../docs/principles/2026-06-04-always-on-viral-intelligence-principle.md)
"ดู signal ตลอดเวลา ≠ ผลิตทุก signal" — 3 data layers (signal → collection → candidates) · สี green/amber/**red ห้าม map เด็ดขาด** (death/violence/minors) · 9 always-on desks

### [AI Video Previsualization](../docs/principles/2026-06-04-ai-video-previsualization-principle.md)
**Trigger:** Umbrella Way 181s rough cut — character drift, umbrella เพี้ยนเป็น pink, model switching variance
**กฎหลัก:** Skill-first/storyboard-first/model-second · 15 required artifacts ก่อน multi-shot · Seedance 2.0 lock · dailies QC ทีละ cell

### [Learning & Performance](../docs/principles/2026-06-04-learning-performance-principle.md)
Render เสร็จ ≠ workflow เสร็จ — 6 metrics artifacts ก่อน archive · closeout fields บังคับ (user_caught_failures, credit_waste) · route สำเร็จ 3 ครั้ง → promote เป็น template · **ห้าม archive run ที่ไม่มี learning_log**

### [Main Flow Mermaid Review](../docs/principles/2026-06-04-main-flow-mermaid-review.md)
Architecture diagram หลัก — upgrade หลัง Hanky พบ wardrobe failure: เพิ่ม location/env gate, story audit gate, `.env`-first, human-visible pre-generation gate, 14-step pre-generation chain

### [Model Routing](../docs/principles/2026-06-04-model-routing-principle.md)

### [Multi-Clip Post-Production](../docs/principles/2026-06-04-multi-clip-post-production-principle.md)
Post owns timeline — explicit EDL ก่อน assembly · silent B-roll default · HyperFrames = deterministic compositor (GSAP seekable/paused) · static title card ผ่าน Nano Banana Pro + OCR review

### [Prompt Council Gate](../docs/principles/2026-06-04-prompt-council-gate.md)
**Trigger:** prompts เป็น "vibe paragraphs" + drafter self-approve
**กฎหลัก:** Prompt = production contract · ≥3 independent seats vote pass · density ≥85/90/95 · decisions: pass/pass_with_publish_block/revise/block

### [Rights & Business Affairs](../docs/principles/2026-06-04-rights-business-affairs-principle.md)
"Review-ready ≠ publish-ready" · required: product_truth, claim_ledger, rights_tracker, ai_usage_log, publish packets · ห้าม fake certification · ห้าม voice clone/face swap ไม่มี consent · ห้าม publish ไม่มี AI label · stop ระดับ black: regulated/talent likeness/union

### [Story Physics & Logic Review](../docs/principles/2026-06-04-story-physics-logic-review-principle.md)
**Trigger:** generate แล้ว physics พัง (น้ำพุ่งผิดทาง, product ลอย)
**กฎหลัก:** Storyboard ต้องประกาศ "laws of its world" · reality mode: realistic/stylized/fantasy/surreal · fantasy ต้องมี written rule + Marketing sign-off ห้ามใช้ซ่อน physics bug · `story_physics_review.json` ก่อน provider call

### [Talent & Partner](../docs/principles/2026-06-04-talent-partner-principle.md)
8 lean core roles · "Own the brief, strategy, taste, rights, approval, learning loop. Partner for craft." · ห้าม present AI เป็นการ replace craft เมื่อ partner มีส่วนจริง

## 2026-06-05 — Retrospective ครั้งใหญ่

### [Main Workflow Learning Upgrade](../docs/principles/2026-06-05-main-workflow-learning-upgrade.md)
**กฎใหม่สำคัญสุด:** **Last Known Good Scenario** — ทุก run ต้องมี `success_scenario_review.json` เทียบ [Hanky V12](05-hanky-v12-runbook.md) · human-visible 3x3 contact sheet ก่อน spend · deep research artifacts บังคับ · caption/VO exact match gate · Nano Banana Pro เท่านั้น

## 2026-06-06 — ยกระดับเป็น Company Standards (4 ฉบับ + Runbook)

### [Company Ad Emotion Standard](../docs/principles/2026-06-06-company-ad-emotion-standard.md) 🏢
Objective: **"สร้างโฆษณาที่ดูตื่นตา ตื่นเต้น น่าสนใจ สนุก และกินใจเท่านั้น"**
5 emotion pillars: ตื่นตา (Wonder) / ตื่นเต้น (Thrill) / น่าสนใจ (Curiosity) / สนุก (Fun) / กินใจ (Heart) — ทุก pillar ≥4.0, average ≥4.3 · ต้องมี memory frame + share/save trigger · hard fail: instructional-only, fake fear/disease

### [Company AI Video Continuity Prompt Standard](../docs/principles/2026-06-06-company-ai-video-continuity-prompt-standard.md) 🏢
สำหรับ campaign >3 scenes: 7 required assets (creative_council, character_passports, location_map, camera_atlas, prop_product_state_machine, scene_prompt_contracts, continuity_qc_matrix) · prompt contract 8 locked blocks · **Continuity Token บังคับทุก scene** (`WORLD= | CHAR= | WARD= | LOC= | CAM= | TIME= | PROP= | PRODUCT=`) · camera atlas ≥10 families

### [Company Autonomous Creative Decision System](../docs/principles/2026-06-06-company-autonomous-creative-decision-system.md) 🏢
ทีม vote เองได้: creative route, keep/kill/regenerate, caption/VO direction · **ห้าม bypass:** credit acknowledgement, model locks, claims, affiliate/rights/publish approval · 8 vote seats + structured output

### [Company Scene-Scale Prompt Lock Standard](../docs/principles/2026-06-06-company-scene-scale-prompt-lock-standard.md) 🏢
ตอบโจทย์ scale 10/50/100 scenes: locked production bible ทุก scene · 8 prompt layers (global→character→location→camera→product→action→motion→QC) · unexplained token drift = blocked · camera atlas 18 families · veto seats kill "beautiful but wrong"

### [Hanky V12 Success Scenario Runbook](../docs/principles/2026-06-06-hanky-v12-success-scenario-runbook.md) ⭐
Canonical last-known-good — สรุปเต็มใน [05-hanky-v12-runbook.md](05-hanky-v12-runbook.md)

## Synthesis

4 วัน (06-03 → 06-06) คือ progression จาก **production chaos → systematic creative factory**: shoe-cover สอน "beautiful ≠ accurate" → umbrella เปิดปัญหา multi-shot continuity → Hanky 12 versions กลั่นเป็น V12 runbook → 06-06 บริษัท encode ทุกบทเรียนเป็น 4 Company Standards ที่ทีม autonomous ทำงานได้โดยไม่รอ founder ทุก micro-decision แต่ hard safety gates ยังครบ

---
[← Hanky V12](05-hanky-v12-runbook.md) | [HOME](HOME.md) | [Research →](07-research.md)
