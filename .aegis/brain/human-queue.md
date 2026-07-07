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

### [2026-07-02] EXTERNAL — CLEAR Men bottle photo file (product char-sheet) / ไฟล์รูปขวด CLEAR Men

- **EN**: Drop the real CLEAR Men Scalp Pro bottle photo (.jpg/.png) into `runs/2026-07-02-clear-men-scalp-pro/00-source/product/`. Shopee blocks automated fetch (JS-rendered, empty); pasted-in-chat images are not disk files. Blocks ONLY product char-sheet generation — the rest of the Lock Sheet proceeds.
- **TH**: วางไฟล์รูปขวด CLEAR Men Scalp Pro จริงลงใน `runs/2026-07-02-clear-men-scalp-pro/00-source/product/` — Shopee ดึงอัตโนมัติไม่ได้ รูปในแชตไม่ใช่ไฟล์ บล็อกเฉพาะการเจน product char-sheet
- **Category**: External access
- **Blocks**: clear-product-charsheet-gen
- **Raised**: 2026-07-02T00:00:00Z
- **Resolved**: _(pending)_
### [2026-07-07] EXTERNAL — Postiz channel OAuth grants + API key + affiliate links (auto-publish 4 ads)

- **EN**: To auto-publish the 4 finished ads via Postiz, the operator must — in the live browser — grant Postiz OAuth for **Facebook Page**, **Instagram (FB Business)**, and **TikTok** (I cannot grant OAuth / authenticate). Then copy the **Postiz API key** (Settings → Public API) so `~/Desktop/Auto-Affi-ads/postiz_publish.sh` can run. Videos verified posting-ready (1080×1920, <40MB, Postiz CDN-hosts on upload). Still missing **real Shopee affiliate links** for CLEAR (×2) + umbrella — only Gatsby link known (`s.shopee.co.th/5LA6RtWT9O`); the other 3 captions have link placeholders.
- **TH**: จะโพสต์ 4 ตัวอัตโนมัติผ่าน Postiz ต้อง (ในเบราว์เซอร์) กดอนุญาต OAuth ให้ Postiz สำหรับ Facebook Page / Instagram / TikTok (ผมกดยืนยันตัวตนแทนไม่ได้) แล้วก๊อป API key จาก Settings → Public API เพื่อรันสคริปต์. ยังขาด affiliate link จริงของ CLEAR (×2) + ร่ม — มีแต่ Gatsby.
- **Category**: External access
- **Blocks**: auto-publish (postiz_publish.sh), 3-of-4 captions (missing affiliate links)
- **Raised**: 2026-07-07T00:00:00Z
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

### [2026-06-28] APPROVAL-GATE — UV umbrella run · 2 sheets awaiting approval

- **EN**: `runs/2026-06-28-uv-auto-umbrella-335` — cast_sheet (hash 09ea56fd) + objects_sheet (hash fe5d847d) PGA-audited PASS, awaiting human approval before Nano Banana Pro generation. Reply `approve cast_sheet` / `approve objects_sheet` (or `go`). Color locked black/yellow. Also confirm commission % + shop rating ★ (rating <4.5 = scout reject; currently assumed 4.8).
- **TH**: 2 sheet audit ผ่านแล้ว รอ approve ก่อนเจน · ยืนยัน commission% + rating ด้วย
- **Category**: Explicit-approval-gate + External access
- **Blocks**: objects_sheet/cast_sheet generation, storyboard, contact, video
- **Raised**: 2026-06-28
- **Resolved**: _(pending)_

## [2026-06-29] Publish umbrella-335 master_v2.mp4 (EXTERNAL — blocks publish only)
- **EN:** master_v2.mp4 is produced + compliant (cleanroom PASS, 15s 1080×1920). To PUBLISH needs: (1) real Shopee affiliate link for the ฿335 umbrella, (2) Meta/TikTok upload token (SPEC §20 G2). I cannot drive external publishing.
- **TH:** วิดีโอเสร็จ+ผ่าน compliance แล้ว เผยแพร่ต้องการ: (1) ลิงก์ affiliate Shopee จริง (2) token อัปโหลด Meta/TikTok — มนุษย์ทำ

## [2026-06-30] Umbrella mechanism — ASSUMED (correct if wrong, FYI only — work continues)
- **EN:** From product photos I read the umbrella as: crook-handle, black-out/yellow-in, with an integrated black hard-case tube that seals the closed wet canopy (reverse/retract). Shots show STATES (open-wet / cased / hanging / dry) so the exact close-motion doesn't matter. If the real mechanism differs, tell me and I'll adjust before the paid Veo step.
- **TH:** อ่านจากรูป: ด้ามโค้ง นอกดำในเหลือง เคสแข็งหุ้มตอนหุบ (ล็อกน้ำ). ถ้ากลไกจริงต่างจากนี้ บอกได้ก่อนยิง Veo.

## [2026-06-30] 🔴 Gemini monthly SPEND CAP exceeded (blocks ALL image+Veo generation)
- **EN:** Raise/reset the project spend cap at https://ai.studio/spend — until then no keyframes or Veo clips can generate. (VO/BGM via kie.ai + HyperFrames render are unaffected.)
- **TH:** ขยาย spend cap ที่ ai.studio/spend ก่อน ไม่งั้นเจนรูป/วิดีโอ Gemini ไม่ได้เลย

## [2026-07-03] Add real side-profile photos of Jiab to the cast ref set (External access — enhances, non-blocking)
- **EN:** Drop real photos of Jiab (2 side-profiles pasted in chat + any other angles) into `cast-library/jiap/identity/real-refs/` (HEIC/JPG/PNG). Pasted images don't persist as files, so I can't wire them as Gemini references. Once present I'll add them to the permanent identity anchor set for the tightest nose/identity lock on every future gen. Work continues meanwhile using `real-face-hq.png` (front) as the anchor.
- **TH:** วางรูปจริงของเจี๊ยบ (2 profile ที่ paste + มุมอื่น) ลง `cast-library/jiap/identity/real-refs/` — paste ในแชตไม่กลายเป็นไฟล์ เลย feed เป็น ref ไม่ได้ พอมีไฟล์ผมเพิ่มเข้า anchor ถาวร ล็อกจมูกแน่นสุด · ระหว่างนี้ทำงานต่อด้วย real-face-hq (หน้าตรง)
- **Category**: External access
- **Blocks**: nothing — optional identity-lock enhancement
- **Raised**: 2026-07-03
- **Resolved**: _(pending)_

## [2026-07-03] JIAP cast — "match ref" scope: face vs whole-look (Identity — decide/continue)
- **EN:** Operator sent white-shirt/quiff-hair reference photos of Jiab and asked to make front+3/4 "match this ref". Decision taken (keeping "หน้าเหมือน" as north star): KEPT the current front/3-4 because fresh regens drifted the face toward a K-idol (verified via montage) — the current panels already match the real Jiab face = same person as the ref. Remaining difference vs the ref is STYLING only: cast uses v4 fringe hair + orange tee (locked), ref shows a swept-up quiff + white shirt. If operator wants the whole cast restyled to the ref look (quiff + shirt), that's a 9-panel restyle — awaiting explicit go. Side profile already re-matched to the clean side ref (jiab_ref).
- **TH:** ถ้าอยากให้ทั้ง cast เป็นลุค ref (ผม quiff + เชิ้ตขาว) = restyle 9 พาเนล รอ "go" · ตอนนี้เก็บ front/3-4 เดิม (เหมือนจริงสุด, regen ใหม่ drift)
- **Category**: Identity / Explicit-approval-gate
- **Blocks**: nothing (v7 cast is complete + consistent as-is)
- **Raised**: 2026-07-03
- **Resolved**: _(pending)_

## [2026-07-04] JIAP cast — need the white-shirt/quiff REF photos as FILES (External access, unblocks exact match)
- **EN:** Repeated "ยังไม่เหมือน" traced to: (1) I over-idealized the v7 face (sharp jaw / lean cheeks per an earlier request) so it diverged from the fuller/natural real face; (2) the correct hairstyle is a swept-UP QUIFF (not the v4 down-fringe). Reverted to a natural fuller face + quiff — best interim = `identity/jiab_face_natural_quiff.png`. To lock the EXACT target I need the operator's 2 white-shirt/quiff reference images AS FILES (chat pastes don't persist to the macOS clipboard, so I can't grab them). Action: drag those 2 photos into `cast-library/jiap/identity/real-refs/` (folder opened). Then I rebuild the full cast (front/3-4/side/expressions) to match them exactly — no more gen-guessing. Decision: holding gen spend until files arrive; natural_a is the standing interim.
- **TH:** วาง 2 รูป ref (เชิ้ตขาว+quiff) ลง `identity/real-refs/` แล้วผมทำ cast ให้ตรงเป๊ะ · ระหว่างนี้ใช้ natural_a เป็นตัวตั้ง หยุดเผา gen เดา
- **Category**: External access / Identity
- **Blocks**: exact cast-face match (interim natural_a usable)
- **Raised**: 2026-07-04
- **Resolved**: _(pending)_
