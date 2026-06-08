# 02 — Compliance Gates (Non-Negotiable)

> 10 gates จาก [`SUPER_SPEC.md`](../SUPER_SPEC.md) — ทุกข้อเป็น hard block ไม่มีข้อยกเว้น แต่ละ gate เกิดจาก incident จริง (ดูที่มาใน [08-runs.md](08-runs.md))

| # | Gate | กฎ | เกิดจาก incident |
|---|---|---|---|
| 1 | **Human-in-the-Loop** | ห้าม public post โดยไม่มี human approval | หลักการก่อตั้ง |
| 2 | **Speed Guard** | Thai VO speed 1.0x–1.15x (warning >1.08x, hard reject >1.15x) | GEESO umbrella: Edge TTS เร่งถึง 1.523x จน user จับได้ |
| 3 | **Disclosure** | `#โฆษณา #affiliate` บังคับในทุก caption | Shoe covers: user ขอลบ on-media disclosure → ต้องชดเชยที่ caption/platform layer |
| 6 | **Caption/VO Sync** | Final render ถูก block จนกว่า caption ตรงกับ approved voice segment report (machine-check) | Hanky V12: render แรกใช้ caption ของ V10 โดยไม่มีใครเห็น |
| 7 | **Learning Closeout** | ทุก run บันทึก successes, failures, user-caught issues, workflow rules changed | runs แรก ๆ ไม่ capture learning ที่ใช้ต่อได้ |
| 8 | **Seedance-Only Video** | Generated visual video = `seedance_2_0` เท่านั้น ห้าม fallback | Umbrella Way: mixed models (Kling/Wan) ทำให้ look variance สูงใน finale |
| 9 | **Nano Banana Pro-Only Images** | Product reference, keyframe, storyboard imagery, static text image, contact sheet = `nano_banana_2` เท่านั้น; scripted schematic ถูก block | Rhodey rain cover: AI สร้าง schematic placeholder เป็น production reference โดยไม่ขออนุญาต → production หยุดทันที |
| 10 | **Human-Visible Storyboard** | ห้ามยิง paid video provider ก่อนแสดง 3x3 storyboard/contact sheet และบันทึก approve ใน `pre_generation_user_review.json` | Rhodey defect เดียวกัน — gate เคย machine-visible แต่ human-invisible |

## Review-Ready vs Publish-Ready

หลักการจาก [Rights & Business Affairs Principle](../docs/principles/2026-06-04-rights-business-affairs-principle.md) + Workflow OS smoke test:

| Packet | บอกอะไร |
|---|---|
| `state.json` | Operational blockers ปัจจุบัน |
| `verification.json` | Cleanroom/stream proof (machine) |
| `approval_packet.json` | Human-facing review packet |
| `publish_packet.json` | Blocked จนกว่า publish-only gates ผ่านครบ |

**Publish gates เพิ่มเติมจาก review:** affiliate URL + subIds, live price/SKU recheck, rights tracker ครบ, platform disclosure, AI label, human publish approval

## Ethics Gate (Intel layer)

Signal ทุกตัวถูกจัดสี ก่อนเข้า product mapping:

- **Green** — ไปต่อได้
- **Amber** — ต้อง human review, ห้าม self-approve
- **Red** — ห้าม product mapping เด็ดขาด (death/violence/injury/minors/self-harm) — map จาก audience need ไม่ใช่จาก personal pain ของบุคคลจริง

## Stop Conditions ระดับ Black (Rights/BA)

Regulated product, talent likeness, voice clone โดยไม่มี consent, union issues → หยุดทันที ไม่มี workaround

## Autonomous Team vs Human Authority

จาก [Company Autonomous Creative Decision System](../docs/principles/2026-06-06-company-autonomous-creative-decision-system.md):

| ทีมตัดสินใจเองได้ | ทีมห้าม bypass (human เท่านั้น) |
|---|---|
| Creative route, ลำดับ proof-test | Provider credit acknowledgement |
| Keep/kill/regenerate dailies | Model locks |
| Caption/VO direction | Product-truth / claim gates |
| Cut readiness for review | Affiliate URL, price/SKU/stock recheck |
| | Rights, disclosure, AI label, final publish approval |

---
[← Production Workflow](01-production-workflow.md) | [HOME](HOME.md) | [Model Locks & Routing →](03-model-locks-routing.md)
