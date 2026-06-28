# Human Queue · คิวรอ Human

> Items that ONLY a human can act on. Bilingual EN / TH.
> Surfaced at `/aegis-start`, `/aegis-status`, `/aegis-handoff`, session end.
> Append via `tools/aegis-queue-human.sh`. Resolve via `tools/aegis-queue-resolve.sh`.
>
> The 4 MBP categories that reach here:
> 1. **Identity** — who are we / what is this
> 2. **Irreversible scope** — destructive / unrecoverable action
> 3. **External access** — needs credentials / accounts / approvals the board owns
> 4. **Explicit approval gate** — hard checkpoint required by SPEC or governance

---

## Pending

> Phase-1 critical path = these 4 gates (`SPEC.md` §20). Live outcome is impossible
> until they clear. Engineering (Sprint 1) proceeds offline in parallel.

<!-- PENDING_START -->

### [2026-06-08] EXTERNAL — G1 · Shopee Affiliate Program TH / สมัคร Shopee Affiliate TH

- **EN**: Apply now — 1–7 day approval. **Blocks ALL live publishing + the real subId click** that defines Phase-1 done. Fallback: Lazada Affiliate. After approval, curate 5–10 candidate SKUs to seed Scout (฿300–1500, ≥4★, ≥10% commission).
- **TH**: สมัครเลย รออนุมัติ 1–7 วัน บล็อกการ publish live ทั้งหมด + subId click จริง (เงื่อนไข Phase-1 done). สำรอง: Lazada Affiliate
- **Category**: External access
- **Blocks**: all-live-publish, real-subId-click, AFFI-E6
- **Raised**: 2026-06-08T12:50:00Z
- **Resolved**: _(pending)_

### [2026-06-08] EXTERNAL — G2 · Meta Business + IG Creator + 60-day Graph token / สร้าง Meta Business + IG Creator + Graph token 60 วัน

- **EN**: Need IG Creator account (not personal) + Meta Business app + long-lived (60-day) Graph token. Blocks IG Reel publishing (FR-07). Token-refresh runbook is a Phase-2 follow-up.
- **TH**: ต้องมี IG Creator (ไม่ใช่ส่วนตัว) + Meta Business app + token 60 วัน บล็อกการโพสต์ IG Reel
- **Category**: External access
- **Blocks**: IG-publishing (FR-07)
- **Raised**: 2026-06-08T12:50:00Z
- **Resolved**: _(pending)_

### [2026-06-08] EXTERNAL — G3 · Higgsfield account + credits / สมัคร Higgsfield + เติม credits

- **EN**: Locked visual-video stack is Higgsfield Seedance 2.0 (`SPEC.md` §19.3). Need account + credits (~$3.60–3.88/ad video-gen, ~$117/mo at 30 ads; soul-id ~$5/persona). This **supersedes** all prior video-vendor gates (kie.ai / Phaya / PiAPI / HeyGen) — do NOT re-evaluate vendors.
- **TH**: stack วิดีโอที่ล็อกแล้วคือ Higgsfield Seedance 2.0 ต้องสมัคร + เติม credit (~$117/เดือน ที่ 30 คลิป) แทน vendor วิดีโอเดิมทั้งหมด ห้ามเปลี่ยนเจ้าอีก
- **Category**: External access
- **Blocks**: visual-video-gen (FR-04)
- **Raised**: 2026-06-08T12:50:00Z
- **Resolved**: _(pending)_

### [2026-06-08] IDENTITY — G4 · Runtime host for 24/7 operation / เลือก runtime host สำหรับรัน 24/7

- **EN**: Personal laptop `cron` (weeks 1–2) vs hosted box / Temporal Cloud free tier / small VPS. Affects deploy script + reliability SLO. Default: laptop cron first, migrate later. (ADR-005 Temporal was accepted-but-never-built; re-decide deliberately.)
- **TH**: laptop cron (สัปดาห์ 1–2) หรือ VPS/Temporal Cloud — กระทบ deploy + reliability SLO เริ่มที่ laptop ก่อนได้
- **Category**: Identity
- **Blocks**: deploy, 24/7-operation
- **Raised**: 2026-06-08T12:50:00Z
- **Resolved**: _(pending)_
<!-- PENDING_END -->

## Resolved

<!-- RESOLVED_START -->

### [2026-06-09] EXPLICIT — Place pyproject.toml (agents guard-blocked from quality configs) / วาง pyproject.toml (guard กัน agent เขียน config คุณภาพ)

- **EN**: AFFI-S1-01 build infra is authored but the config-protection guard blocks agents from writing pyproject.toml by design. It is a FRESH file with STRONG gates (mypy strict, full ruff, strict-markers) — strengthening, not weakening. Unblock with one command: cp _aegis-output/specs/AFFI-S1-01-build-config-proposed.txt pyproject.toml  — then the agent runs uv sync + pytest and continues Sprint-1 autonomously (source .py modules are NOT guarded).
- **TH**: AFFI-S1-01 เขียน build infra แล้ว แต่ guard กันไม่ให้ agent เขียน pyproject.toml (ตั้งใจ) ไฟล์สร้างใหม่ gate เข้ม ไม่ได้ลดมาตรฐาน ปลดบล็อกคำสั่งเดียว: cp _aegis-output/specs/AFFI-S1-01-build-config-proposed.txt pyproject.toml แล้ว agent รัน uv sync + pytest ต่อเองได้เลย
- **Category**: Explicit approval gate
- **Raised by**: claude
- **Blocks**: AFFI-S1-01 then all of Sprint-1 (every task needs the test runner)
- **Raised**: 2026-06-09T13:26:52Z
- **Resolved**: 2026-06-10T14:42:47Z — Satisfied by reality at handoff 2026-06-10: pyproject.toml is committed (d93ff46d 'feat(s1-01): build infra'), uv.lock present, and the test runner works — VERIFIED ruff 'All checks passed' + pytest '264 passed, 86% cov'. The Sprint-1 blocker (no test runner) is gone; all of S1-01..S1-08 landed on top.
### [2026-06-08] IRREVERSIBLE — Resolve mid-hard-reset working tree (finalize vs restore)

- **EN**: Human chose **Path A (finalize the reset)**. Executed: committed as `82c7fe5c` (504 files; src/ + tests/ + old brain wiped from tree). Working tree clean; prior implementation fully recoverable at `5602e53c`; `.venv/` + `runs/` added to `.gitignore`; `SPEC.md` + `.env.example` preserved on disk. Not pushed (commit-only per request).
- **TH**: เลือก Path A (ยืนยัน reset) commit แล้วเป็น `82c7fe5c` กู้คืนโค้ดเดิมได้จาก `5602e53c` working tree สะอาด ยังไม่ push
- **Category**: Irreversible scope
- **Raised**: 2026-06-08T12:21:04Z
- **Resolved**: 2026-06-08T12:50:00Z — committed 82c7fe5c

### [2026-06-08] SUPERSEDED — Pre-reset vendor/credit gates folded into §19.3 stack lock

- **EN**: The following pre-reset pending gates are superseded by the 2026-06-08 hard-reset + `SPEC.md` §19.3 (Higgsfield-only + edge-tts + Gemini stills): kie.ai signup, ElevenLabs starter (→ edge-tts free), Phaya top-ups, HeyGen Avatar IV key, PiAPI key, Beauty-SKU pre-curation (now folded into G1), and "add google-cloud-storage to pyproject.toml" (pyproject deleted; handled by Sprint-1 task AFFI-S1-01). GCS bucket + Gemini key + Phaya key were already provisioned (see entries below). Net live-credit need now = G1 Shopee + G2 Meta/IG + G3 Higgsfield + G4 host.
- **TH**: gate vendor/credit ก่อน reset ถูกแทนด้วย §19.3 (Higgsfield + edge-tts + Gemini) — kie.ai/ElevenLabs/Phaya/HeyGen/PiAPI/Beauty-SKU/gcs-in-pyproject ไม่ต้องทำแล้ว เหลือ G1–G4
- **Category**: External access
- **Resolved**: 2026-06-08T12:50:00Z — superseded by hard-reset + stack lock

### [2026-05-15] EXTERNAL — Confirm Phaya Seedance 2.0 support OR build direct adapter

- **EN**: Phaya's REST does not expose model-listing. Resolved via Higgsfield CLI route (Phaya 1.5 Pro stays usable for legacy storyboards).
- **Category**: External access
- **Resolved**: 2026-05-15T15:31:36Z — routed through Higgsfield instead.

### [2026-05-15] EXTERNAL — PiAPI account + key for Seedance 2.0

- **EN**: Replaced by Higgsfield CLI (credit pool via OAuth). PiAPI adapter kept as fallback only (now removed in hard-reset).
- **Category**: External access
- **Resolved**: 2026-05-15T15:31:36Z — superseded by Higgsfield CLI.

### [2026-05-15] EXTERNAL — Higgsfield.ai API key (DoP + Transitions)

- **EN**: Replaced by Higgsfield MCP server (OAuth, no API key). Registered via `claude mcp add`.
- **Category**: External access
- **Resolved**: 2026-05-15T15:21:15Z — Higgsfield MCP (OAuth).

### [2026-05-13] EXTERNAL — Enable Gemini API pay-as-you-go OR add prepay credits

- **EN**: Board provided fresh API key from a billed project. Smoke-tested nano-banana-pro-preview HTTP 200. Key in `.env`.
- **Category**: External access
- **Resolved**: 2026-05-13T21:29:41Z — fresh billed key in .env.

### [2026-05-13] EXTERNAL — Top up Google AI Studio / Gemini API credits

- **EN**: Superseded by the more specific pay-as-you-go diagnosis above.
- **Category**: External access
- **Resolved**: 2026-05-13T21:19:11Z — superseded.

### [2026-05-13] EXTERNAL — Top up Phaya.io credits (~฿300+)

- **EN**: Board topped up ฿17.49 → ฿161.49 (+฿144). (Phaya now legacy per §19.3.)
- **Category**: External access
- **Resolved**: 2026-05-13T20:14:14Z — topped up.

### [2026-05-13] EXTERNAL — Create GCP project + GCS bucket gs://auto-affi-media-dev + service account

- **EN**: Provisioned: bucket gs://auto-affi-media-dev (asia-southeast1), service account auto-affi-media@atn-tools.iam.gserviceaccount.com (roles/storage.objectAdmin scoped to bucket), key at ~/.config/auto-affi/sa.json (chmod 600), .env updated. Live smoke test passed (upload+download+delete). Per ADR-006 — still valid for the rebuild.
- **Category**: External access
- **Resolved**: 2026-05-13T10:00:22Z — provisioned + smoke-tested.

### [2026-05-13] EXTERNAL — Provide PHAYA_API_KEY

- **EN**: Key delivered, written to .env (0600), live probes confirmed. (Phaya now legacy per §19.3.)
- **Category**: External access
- **Resolved**: 2026-05-13T09:35:51Z — key in .env.
<!-- RESOLVED_END -->

### [2026-06-28] EXTERNAL — UV umbrella run · product image + Higgsfield credits

- **EN**: Run `runs/2026-06-28-uv-auto-umbrella-335` reached the gated visual stages. Need (1) the **product image** of the umbrella (Shopee link given, no image file) — required for the objects_sheet + contact frames; (2) **Higgsfield credits** (§20 G3) for any paid generation; (3) confirm **commission %** + **shop rating ★** for the economics record. Workflow ran Step 0–2 + cast_sheet PGA audit (passed, awaiting approval).
- **TH**: รัน UV umbrella ถึง stage ที่ต้องเจนภาพแล้ว ต้องการ (1) รูปสินค้าจริง (ให้แต่ลิงก์ ยังไม่มีไฟล์รูป) สำหรับ objects/contact, (2) Higgsfield credits สำหรับเจน paid, (3) ยืนยัน commission % + rating ★
- **Category**: External access
- **Blocks**: objects_sheet, contact_sheet, video (paid stages)
- **Raised**: 2026-06-28
- **Resolved**: _(pending)_

### [2026-06-28] EXTERNAL — Veo 3 video access (provider pivot ADR-009)

- **EN**: Pivot to Gemini-only confirmed. Stills via Nano Banana Pro are AVAILABLE (MCP, verified). **Veo 3 video has NO key/endpoint in `.env`** (no Veo MCP tool; no GEMINI/Veo key) → the video stage cannot run. Provision a Veo 3 access path (Google/Gemini API key with Veo access, or a Veo-capable endpoint). Until then: image stages run on Nano Banana Pro; video stays blocked. Higgsfield (HF_API_ID/HF_API_SECRET) is retired per ADR-009.
- **TH**: เปลี่ยนเป็น Gemini-only แล้ว รูปผ่าน Nano Banana Pro ใช้ได้จริง แต่ **Veo 3 ยังไม่มี key/endpoint ใน `.env`** → stage วิดีโอรันไม่ได้ ต้องขอ access Veo 3 (Google/Gemini API key ที่เปิด Veo) ก่อน
- **Category**: External access
- **Blocks**: video stage (all runs), incl. runs/2026-06-28-uv-auto-umbrella-335
- **Raised**: 2026-06-28
- **Resolved**: 2026-06-28 — GEMINI_API_KEY added to .env; verified HTTP 200 with Veo 2/3/3.1 + image model access.
