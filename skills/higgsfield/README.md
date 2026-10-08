# Higgsfield Director + Bible Skills

สร้างสำหรับ Auto-Affi วันที่ 5 ตุลาคม 2026 และอัปเดต 7 ตุลาคม 2026 เป็น **Bible v2**: 16 คอร์ส / 171 บท + prompt bank 46 รายการ + หน้าคอร์ส 16 หน้า สรุปจาก article + audio transcript + frames และ audit แล้ว 233/233 (231 VERIFIED + 2 VERIFIED_GAP: A15.L09, A15.L10) ชุดนี้เป็นคำสั่งและเครื่องมือช่วยทำงานที่เรียกใช้ได้ ไม่ใช่การ fine-tune โมเดล และยังไม่ได้ทดสอบการสร้าง media จริงครบทุก workflow

## เริ่มใช้งาน

```text
ใช้ $higgsfield-bible-director
วางแผนโฆษณาสำหรับสินค้านี้ตาม Bible v2
เริ่มจากข้อเท็จจริงและ asset pack แล้วทำ shotlist กับ prompt
ใช้เฉพาะ skills ที่เกี่ยวข้อง และระบุข้อมูลที่ยังขาด
```

หรือใช้ agent ในโปรเจกต์นี้:

```text
ให้ agent higgsfield-director วาง workflow สำหรับงานนี้ตาม Bible
ส่ง brief, asset/state plan, shotlist, prompt และเกณฑ์ QC ที่จำเป็น
```

เมื่อเป็นคลิปสินค้าใหม่ที่เริ่มผลิตจริง ให้ใช้ทางเข้าเดิมร่วมด้วย:

```text
ใช้ $auto-affi-new-product-clip ร่วมกับ $higgsfield-bible-director
ทำคลิปสินค้านี้ตาม workflow เดิมและหลักใน Bible
เตรียมงานให้ตรวจได้ก่อนถึงขั้นจ่ายเครดิตตาม gate ที่ยังค้าง
```

ไม่ต้องพิมพ์ชื่อทุกตัวพร้อมกัน (ตอนนี้มี 12 skills รวม `higgsfield-seedance-prompt` ที่เขียนและ lint prompt Seedance ด้วย `scripts/lint_prompt.py` และ `higgsfield-operator` ที่กด generate จริงผ่าน UI หลังผ่าน PGA gate + credit cap ด้วย `uv run python -m auto_affi.ops.gate_cli` และ `higgsfield-dailies-review` ที่ตรวจคลิปที่ได้ด้วย ffmpeg + frames + rubric) ตัว router เลือกตาม deliverable และโหลดข้อมูลเฉพาะส่วน Skills ตั้งให้เลือกโดยอัตโนมัติได้ตามคำอธิบายด้วย หากรายการ skills ในแชทเดิมยังไม่ปรากฏ ให้เปิดแชทใหม่เพื่อให้ค้นพบไฟล์ที่เพิ่งเพิ่ม

## Agent และการติดตั้ง

- Codex project agent: `.codex/agents/higgsfield-director.toml`
- Claude project adapter: `.claude/agents/higgsfield-director.md` สำหรับบทบาทเดียวกันใน framework เดิม
- Skills ต้นฉบับ: `skills/higgsfield/<skill-name>/`
- Installed aliases: `~/.codex/skills/<skill-name>` ชี้มาที่ต้นฉบับใน repository นี้

ไฟล์ agent ใช้ name, description และ developer_instructions ตาม [เอกสาร Custom agents ของ Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents) ไม่มี model override หรือการเปลี่ยน permissions/global config การใช้ aliases ทำให้แก้ไฟล์เดียวแล้วใช้งานได้ตรงกัน หากย้ายหรือลบ repository ต้องปรับ links ให้ตรงที่ใหม่

## Skills ที่สร้าง

| Skill | เรียกเมื่อ | ผลงานหลัก |
|---|---|---|
| `$higgsfield-bible-director` | ต้องเลือก/รวม workflow จาก Bible | route, brief, handoff, หลักฐานการจบงาน |
| `$higgsfield-asset-continuity` | คน/สินค้า/ฉาก/สถานะต้องคงเดิม | reference pack, register, map, state table |
| `$higgsfield-cinematic-direction` | หนัง โฆษณา animation รถ หรือต่อสู้ | beat, coverage, prompt, keeper/revision |
| `$higgsfield-vfx-footage` | ใช้ footage จริงเป็นฐาน | keep-list, trigger, edit และ integration QC |
| `$higgsfield-brand-visuals` | ภาพแบรนด์หลายรูปแบบ | identity master, variants, packaging/try-on checks |
| `$higgsfield-faceless-channel` | explainer/channel/localization/shorts | evidence, script, scene plan, packaging |
| `$higgsfield-game-production` | เกมที่เล่นได้ | GDD, mechanics/input tests, media และ publish readiness |
| `$higgsfield-production-qc` | demo/dailies/export หรือแก้งานผิด | report by timecode, blocker, keeper, targeted fix |
| `$higgsfield-agency-operations` | รับงานโฆษณา/บริการ/ต้นทุน | offer, intake, approval ownership, QC และ economics |

## ความถูกต้องและประสิทธิภาพที่ออกแบบไว้

Reference แต่ละชิ้นมีหน้าที่ ชื่อ version และข้อไม่แน่ใจ; ภาพมุมใหม่ของสินค้าไม่ถูกนับเป็นหลักฐานรายละเอียดที่ต้นฉบับไม่เห็น คน พร็อพ เสื้อผ้า และสถานที่มีสถานะก่อน/หลังที่รับกันข้าม cut เมื่อผลผิดซ้ำจะวินิจฉัย brief/reference ก่อนสุ่มใหม่ เก็บ keeper และสร้างเฉพาะ beat ที่ขาด

โหลด Bible ตาม ID เฉพาะที่ต้องใช้ มี snapshot เดียวและ SHA-256 เพื่อรู้ฉบับต้นทาง ไม่โหลดทั้งเล่ม (171 บท + prompt bank + หน้าคอร์ส) ทุกครั้ง ใช้ agent ตัวเดียวเป็นค่าเริ่มต้นและไม่เปลี่ยนงานเล็กให้เป็น pipeline ใหญ่โดยอัตโนมัติ

กฎ Auto-Affi เดิมยังเป็นเจ้าของ model/voice/research/storyboard/preflight เมื่อใช้ production route นั้น ชุด Bible ไม่สร้าง approval เอง ไม่อนุญาตเครดิต และไม่แทนคำสั่ง `validate-generation` ที่มีอยู่แล้ว

รายงานแยก DRAFTED, STRUCTURALLY_CHECKED, MEDIA_INSPECTED และ EXECUTED เพื่อไม่ให้ artifact ที่เพิ่งเขียนถูกกล่าวว่าทดสอบสร้างวิดีโอแล้ว ข้อมูลราคา โมเดล กติกา รายได้ และ plugin จากคอร์สต้องตรวจปัจจุบันเมื่อมีผลต่อการทำงาน

## ตัวช่วยที่ใช้ได้ทันที

จากโฟลเดอร์ `higgsfield-bible-director`:

```bash
python3 scripts/bible_lookup.py --list
python3 scripts/bible_lookup.py --section A16.04 --section C1
python3 scripts/bible_lookup.py --search "มือ" --limit 5 --json

python3 scripts/production_packet.py init --run-dir /absolute/new-run --mode cinematic
python3 scripts/production_packet.py check --run-dir /absolute/run --stage plan --write-report
python3 scripts/production_packet.py check --run-dir /absolute/run --stage delivery --write-report
```

`init` ไม่เขียนทับ run เดิม; `check` จับ IDs ซ้ำ references/ไฟล์ที่ขาด claim ที่ใช้แต่ยังไม่ verified งบรวมค่าใช้ไปกับรอบถัดไป และ attempt cap ส่วน delivery ตรวจไฟล์/รายงาน/สถานะ review ที่บันทึกไว้

**ข้อจำกัดของ checker:** ตรวจเอกสารกับการมีไฟล์เท่านั้น ไม่ fetch แหล่ง claim ไม่เปิดดูภาพ ไม่เล่นวิดีโอ ไม่ฟังเสียง และไม่เช็คสิทธิของ media ดังนั้น structural pass ยังต้องตรวจเนื้อหาจริง และไม่ใช่สิทธิเริ่ม provider call

## ผลตรวจที่ทำแล้ว

- `quick_validate.py` ผ่านทั้ง 9 skills; UI YAML และ installed links ตรวจแล้ว
- Agent TOML parse ผ่าน และมี fields ที่เอกสารกำหนด
- Helper tests ผ่าน 11 tests ด้วย synthetic fixtures ใน temporary directories ไม่มีการใช้เงินจริง/เครดิต
- Source lookup ครอบคลุม 171 lesson IDs; ตรวจว่าอ่าน lesson เดี่ยวแล้วไม่ติด lesson ถัดไป
- ตรวจ path ของ references, skill routing และการครอบคลุมทั้ง 16 คอร์ส

ยังไม่ได้ทดสอบ spawn profile นี้ใน runtime ของแอปหรือสร้างงานด้วย provider จริง การตรวจ `codex --version` พบว่า CLI ที่ `/opt/homebrew/bin/codex` เรียก binary ที่ไม่มีในเครื่อง จึงไม่อ้างว่า agent runtime smoke test ผ่าน และไม่ได้แก้ CLI ซึ่งอยู่นอกงานนี้ ตัว skills และ helper scripts ถูกติดตั้งและตรวจได้แยกจากปัญหา CLI

รายละเอียด: `validation-report.json` และ `tests/test_helpers.py`
