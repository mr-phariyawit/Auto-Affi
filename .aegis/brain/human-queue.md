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

<!-- PENDING_START -->

### [2026-05-13] EXTERNAL — Apply to Shopee Affiliate Program TH / สมัคร Shopee Affiliate TH

- **EN**: Quick-win QW-1. Start the application clock now — can take 1-7 days for approval. Blocks all live publishing.
- **TH**: Quick-win QW-1 — เริ่มสมัครก่อน รออนุมัติ 1-7 วัน บล็อก publishing live ทั้งหมด
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: quick-win-track
- **Raised**: 2026-05-13T09:16:52Z
- **Resolved**: _(pending)_

### [2026-05-13] IDENTITY — Confirm runtime host for quick-win cron / ยืนยัน runtime สำหรับ cron quick-win

- **EN**: Quick-win QW-9. Personal laptop cron vs hosted box. Affects deploy script + reliability SLO. Default: laptop cron weeks 1-2, then migrate to Temporal Cloud free tier or small VPS.
- **TH**: Quick-win QW-9 — laptop cron vs hosted box; สัปดาห์แรก laptop ก็พอ
- **Category**: Identity
- **Raised by**: claude-orchestrator
- **Blocks**: deploy-step
- **Raised**: 2026-05-13T09:16:52Z
- **Resolved**: _(pending)_

### [2026-05-13] EXTERNAL — Create Meta Business + IG Creator + long-lived Graph token / สร้าง Meta Business + IG Creator + Graph token 60d

- **EN**: Quick-win QW-2. Need IG Creator (not personal) + Meta Business app + 60-day token. Token-refresh runbook deferred to Sprint 5.
- **TH**: Quick-win QW-2 — IG Creator + Meta Business + token 60d
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: IG-publishing
- **Raised**: 2026-05-13T09:17:08Z
- **Resolved**: _(pending)_

### [2026-05-13] EXTERNAL — Sign up kie.ai + initial credits (~$20) / สมัคร kie.ai เติม credit เริ่มต้น (~$20)

- **EN**: Quick-win QW-3. Required for premium video (Veo/Sora/Flux). Local fallback is publish-quality espeak-ng + PIL only — not viral-grade.
- **TH**: Quick-win QW-3 — kie.ai สำหรับวิดีโอ premium
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: publish-grade-video
- **Raised**: 2026-05-13T09:17:08Z
- **Resolved**: _(pending)_

### [2026-05-13] EXTERNAL — Sign up ElevenLabs starter (~$5/mo) for Thai TTS / สมัคร ElevenLabs starter (~$5/เดือน) สำหรับเสียงไทย

- **EN**: Quick-win QW-4. Required for native Thai TTS. Azure + Botnoi documented as Phase 2 fallbacks.
- **TH**: Quick-win QW-4 — ElevenLabs สำหรับ TTS ไทย
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: voiced-video
- **Raised**: 2026-05-13T09:17:08Z
- **Resolved**: _(pending)_

### [2026-05-13] EXTERNAL — Pick 5-10 Beauty SKUs from Shopee TH / เลือก Beauty SKU 5-10 ชิ้นจาก Shopee TH

- **EN**: Quick-win QW-6. After Shopee Affiliate approved, curate 5-10 candidate Beauty SKUs to seed Scout. Criteria: ฿300-1500, ≥4★, ≥10% commission, recent sales velocity.
- **TH**: Quick-win QW-6 — หลังได้ Shopee Affiliate แล้ว เลือก Beauty SKU 5-10 ชิ้น
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: first-cycle
- **Raised**: 2026-05-13T09:17:08Z
- **Resolved**: _(pending)_

### [2026-05-13] EXTERNAL — Top up Phaya.io credits (recommend ฿1,000+) / เติม credit Phaya.io (แนะนำ ฿1,000+)

- **EN**: Initial 150 THB (~$4.20) covers probes + ~1,300 Sora 2 videos at ฿0.10/job test scale, but real Phase 1 daily ops (5 videos/day premium Sora 2) burn ~฿125/day. Top up to ฿1,000+ for first 8-day live test cycle. Console: https://phaya.io/dashboard or wherever Phaya hosts billing.
- **TH**: ตอนนี้มี ฿150 (~$4.20) เติม ฿1,000+ พอใช้ Phase 1 ราว 8 วัน — Sora 2 + TTS + embed รวมๆ ราว ฿125/วัน
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: phase-1-live-test
- **Raised**: 2026-05-13T09:35:51Z
- **Resolved**: _(pending)_

### [2026-05-13] IDENTITY — Add google-cloud-storage>=3.0.0 to pyproject.toml [adapters] group / เพิ่ม google-cloud-storage>=3.0.0 ใน pyproject.toml [adapters]

- **EN**: AEGIS config-protection hook blocks agent edits to pyproject.toml (governance). One-line addition under [project.optional-dependencies] adapters: 'google-cloud-storage>=3.0.0', then 'uv lock' to refresh uv.lock. Package already installed in .venv via uv pip install; this just makes it reproducible. Locked tests pass.
- **TH**: Hook กัน agent แก้ pyproject.toml — เพิ่ม google-cloud-storage>=3.0.0 ใน [adapters] แล้วรัน uv lock
- **Category**: Identity
- **Raised by**: claude-orchestrator
- **Blocks**: reproducible-install
- **Raised**: 2026-05-13T10:00:22Z
- **Resolved**: _(pending)_

### [2026-05-15] EXTERNAL — Phaya top-up needed for concept-2 reset Step 4 / ต้องเติม Phaya credits สำหรับ concept-2 reset Step 4

- **EN**: Balance ฿29.18; need ~฿45-75 for --variants 3 × 6 clips (HSO×VCS Method P0 #3). Without top-up: fall back to --variants 1 (~฿15-25, fits budget). Steps 0-3 complete; new stills + sheet show PD300X identity locked correctly. After top-up resume with: scripts/gen-video-seedance.py --item-id 28875679676 --storyboard-json data/registry/items/28875679676/concept-2-storyboard.json --workdir out/maono-concept-2-workdir-v8 --output out/maono-concept-2-final-v8.mp4 --variants 3 ...
- **TH**: Balance ฿29.18; ต้องเพิ่ม ~฿45-75 สำหรับ --variants 3 × 6 clips (HSO×VCS Method P0 #3). ถ้าไม่เติม: ใช้ --variants 1 (~฿15-25 พอ). Steps 0-3 เสร็จแล้ว — stills + sheet ใหม่ มี PD300X ถูกต้อง
- **Category**: External access
- **Raised by**: nick-fury
- **Blocks**: Step 4: scripts/gen-video-seedance.py --variants 3
- **Raised**: 2026-05-15T06:17:06Z
- **Resolved**: _(pending)_

### [2026-05-15] EXTERNAL — HeyGen Avatar IV API key for verified Thai lip-sync / HeyGen Avatar IV API key สำหรับ lip-sync ภาษาไทย

- **EN**: Seedance --generate-audio produces speech-LIKE audio but words aren't verified (could be plausible-sounding gibberish). HeyGen Avatar IV gives deterministic lip-sync (0.02s sync error per practitioner research). Need: HEYGEN_API_KEY in .env + new adapter src/auto_affi/adapters/heygen.py. Cost: ~$0.12/sec, ~฿65 for concept-2's 16s of dialogue. Flow: Phaya TTS (verified Thai) → HeyGen Avatar IV (lip-sync to s2/s3 stills) → replace clip 2/3 video tracks.
- **TH**: Seedance --generate-audio ออกเสียงคล้าย Thai แต่ verify คำพูดไม่ได้ HeyGen Avatar IV จะ lip-sync แม่นๆ (sync error 0.02s) ต้องการ HEYGEN_API_KEY + สร้าง adapter ใหม่ ค่าใช้จ่าย ~฿65 สำหรับ dialogue 16s ของ concept-2
- **Category**: External access
- **Raised by**: nick-fury
- **Blocks**: Replace Seedance --generate-audio dialogue with HeyGen Avatar IV lip-sync on clips 2+3
- **Raised**: 2026-05-15T08:14:10Z
- **Resolved**: _(pending)_

### [2026-06-08] IRREVERSIBLE — Resolve mid-hard-reset working tree: finalize wipe OR restore from HEAD / ตัดสินสถานะ hard-reset ค้าง: commit การลบทั้งหมด หรือ restore กลับจาก HEAD

- **EN**: doctor 2026-06-08 found the working tree mid-hard-reset. HEAD (5602e53c) = 'snapshot before hard-reset'; tree has 380 unstaged DELETIONS wiping src/ (87), tests/ (67), .aegis brain (108), pyproject.toml + uv.lock + tools/docs/scripts/skills. 0 staged, 50 untracked, 19 modified. Verification (tests+lint) CANNOT run — infra deleted. Fully recoverable from HEAD. Two irreversible paths: (A) finalize the reset = git add -A && commit && push; (B) abort = git restore . to bring code/tests/brain back, then re-run /aegis-verify. Human must pick intent; AEGIS will not auto-commit a source/brain wipe nor auto-restore over an intentional reset. Also queued: stray venv (17,408 .py) inside runs/2026-06-04-hanky-dry-towel.../ should be gitignored+removed either way.
- **TH**: doctor 2026-06-08 พบ working tree ค้างกลางการ hard-reset. HEAD คือ snapshot ก่อน reset; tree มีการลบ 380 ไฟล์ที่ยังไม่ stage (src/ tests/ .aegis brain pyproject.toml uv.lock). รัน test/lint ไม่ได้เพราะ infra ถูกลบ แต่กู้คืนจาก HEAD ได้ครบ. เลือก: (A) ยืนยัน reset = commit+push การลบ; (B) ยกเลิก = git restore . แล้วรัน /aegis-verify ใหม่. ต้องให้ human ตัดสินเจตนา. หมายเหตุ: มี venv หลง 17,408 ไฟล์ใน runs/hanky-dry-towel ควร gitignore+ลบ.
- **Category**: Irreversible scope
- **Raised by**: claude-orchestrator
- **Blocks**: /aegis-verify (tests+lint), any build/deploy until tree resolved
- **Raised**: 2026-06-08T12:21:04Z
- **Resolved**: _(pending)_
<!-- PENDING_END -->

## Resolved

<!-- RESOLVED_START -->

### [2026-05-15] EXTERNAL — Confirm Phaya Seedance 2.0 support OR build direct adapter / Confirm Phaya รองรับ Seedance 2.0 หรือสร้าง direct adapter

- **EN**: Phaya's REST does not expose model-listing endpoint (probed /models and /seedance-video/info → 404). Current create_seedance_video() targets 1.5 Pro only. Two paths to choose between: (a) ask Phaya support if they have a 2.0 endpoint / parameter — if yes, 30 LOC delta to adapter; (b) build src/auto_affi/adapters/seedance_direct.py against Atlas Cloud ($0.16/s Fast 720p) or PiAPI ($0.08/s seedance-2-fast) — ~100 LOC mirroring HeyGen adapter pattern, +1 day work. +31.7 physics accuracy + 35% cheaper Fast tier justifies switch. Routing rule fully documented in .aegis/brain/learnings/2026-05-15-higgsfield-seedance2-stack-routing.md
- **TH**: Phaya ไม่มี endpoint ดู model list — ต้องถาม Phaya support หรือสร้าง direct adapter ไป Atlas Cloud / PiAPI (~1 วัน) Seedance 2.0 +31.7 physics accuracy + ถูกกว่า 35% Fast tier
- **Category**: External access
- **Raised by**: nick-fury
- **Blocks**: Upgrade Seedance 1.5 Pro → 2.0 in concept-2 and future products
- **Raised**: 2026-05-15T11:03:39Z
- **Resolved**: 2026-05-15T15:31:36Z — Resolved via Higgsfield CLI — Phaya doesn't need to support 2.0, we route through Higgsfield instead. Phaya's create_seedance_video (1.5 Pro) stays usable for legacy storyboards.
### [2026-05-15] EXTERNAL — PiAPI account + key for Seedance 2.0 / PiAPI account + key สำหรับ Seedance 2.0

- **EN**: Cheapest direct-API route to Seedance 2.0 first_last_frames task (no Phaya wait). Sign up: https://piapi.ai/seedance-2-0 — generate API key — set PIAPI_API_KEY=... in .env. seedance-2-fast = ~$0.08/s ($0.32 per 4s clip). REST shape mirrors HeyGen (POST submit + GET poll), adapter is purely additive. Adapter + schema enum + orchestrator branch will be committed in advance so the only thing that changes when the key arrives is the .env entry.
- **TH**: เส้นทาง direct-API ที่ถูกที่สุดไป Seedance 2.0 — สมัครที่ https://piapi.ai/seedance-2-0 paste key เป็น PIAPI_API_KEY ใน .env ค่าใช้จ่ายประมาณ $0.32 ต่อคลิป 4 วินาที
- **Category**: External access
- **Raised by**: nick-fury
- **Blocks**: Wire SEEDANCE_2_FAST / SEEDANCE_2_PRO generators into production runs
- **Raised**: 2026-05-15T11:29:06Z
- **Resolved**: 2026-05-15T15:31:36Z — Replaced by Higgsfield CLI — 'higgsfield generate create seedance_2_0' routes through Higgsfield's credit pool (Ultra plan 3000 credits, OAuth). PiAPI adapter (src/auto_affi/adapters/seedance2.py) stays in tree as a fallback path but is no longer the primary.
### [2026-05-15] EXTERNAL — Higgsfield.ai API key (DoP + Transitions for product motion shots) / Higgsfield.ai API key (DoP + Transitions สำหรับ product motion shots)

- **EN**: Research approved Higgsfield DoP for macro product shots with 50+ named camera presets (Crash Zoom, Dolly In, Orbit 360, Bullet Time) + Transitions tool (17 effects). Replaces 3 static hold shots in concept-2-v3 (s0/s3/s5) with cinematic motion at ~$0.30 total. Plus tier $49/mo gives 1000 credits = ~50 motion clips. Public REST API + official Python SDK. Sign up: https://higgsfield.ai/pricing — generate API key in dashboard — paste to HEYGEN_API_KEY-style env var HIGGSFIELD_API_KEY. After arrival, adapter is ~150 LOC + schema enum extension + orchestrator branch (1 day work). Full routing rule in .aegis/brain/learnings/2026-05-15-higgsfield-seedance2-stack-routing.md
- **TH**: Research อนุมัติ Higgsfield DoP สำหรับ macro product shots + 50+ camera presets. Plus tier $49/เดือน = 1000 credits. ต้องสมัครที่ https://higgsfield.ai/pricing แล้ว paste API key เข้า HIGGSFIELD_API_KEY ใน .env
- **Category**: External access
- **Raised by**: nick-fury
- **Blocks**: Higgsfield DoP + Transitions adapter + schema extension
- **Raised**: 2026-05-15T11:02:58Z
- **Resolved**: 2026-05-15T15:21:15Z — Replaced by Higgsfield MCP server (https://mcp.higgsfield.ai) — OAuth-based, no API key needed. Registered in Claude Code via 'claude mcp add'. User completes OAuth via /mcp slash command. REST adapter path obsolete for our use case.
### [2026-05-13] EXTERNAL — Enable Gemini API pay-as-you-go OR add prepay credits (project-level) / เปิด pay-as-you-go ของ Gemini API หรือ เติม prepay credit

- **EN**: Gemini API key (AIzaSy…OYLg) authenticates fine — model list works (33 models). But EVERY generateContent call returns HTTP 429 'prepayment credits depleted' (tested text Flash + image Flash + image Pro). Diagnosis: project linked to this key has billing enabled but is in PREPAY mode with zero balance. Two unblock paths: (A) at https://ai.studio/projects toggle the project to Pay-as-you-go mode (recommended — no manual top-ups), or (B) add prepay credit balance at the same page. Either path unblocks ALL image-gen via Gemini Nano Banana Pro 2.
- **TH**: Gemini API key auth ok แต่ทุก call ได้ HTTP 429 prepay หมด. ที่ https://ai.studio/projects เลือก project ของ key นี้ → toggle เป็น Pay-as-you-go หรือเติม prepay credit. ปลดล็อก image-gen ทั้งหมด
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: concept-2-rerun-via-gemini-nano-banana-pro · all-image-generation
- **Raised**: 2026-05-13T21:19:11Z
- **Resolved**: 2026-05-13T21:29:41Z — Board provided fresh API key from a billed project (clipboard). Smoke-tested nano-banana-pro-preview: HTTP 200, image returned. Old key replaced in .env.
### [2026-05-13] EXTERNAL — Top up Google AI Studio / Gemini API credits / เติม credit Google AI Studio (Gemini API)

- **EN**: Gemini API key authenticated (33 models accessible) but prepayment credits are depleted — all calls return HTTP 429 'prepayment credits depleted'. Top up at https://ai.studio/projects. ~$5-10 covers many thousands of vision-QA calls at Gemini 2.5 Flash pricing (~$0.0001/image).
- **TH**: Gemini API key ใช้งานได้ (33 models) แต่ credit หมด — call ทุกครั้งได้ HTTP 429. เติมที่ https://ai.studio/projects. ~$5-10 พอใช้ vision QA หลายพันครั้ง (~$0.0001/รูป).
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: vision-qa-character-consistency · vision-qa-anatomy-check
- **Raised**: 2026-05-13T21:03:40Z
- **Resolved**: 2026-05-13T21:19:11Z — Superseded by more specific diagnosis — see new queue entry
### [2026-05-13] EXTERNAL — Top up Phaya.io credits (~฿300+ recommended) / เติม credit Phaya เพิ่ม (~฿300+)

- **EN**: Phaya balance ฿17.49 — insufficient to complete Concept 2 via Seedance. Each 8s 720p+audio clip costs ฿24; 5 remaining clips need ~฿120. Top up to ฿300+ for completion plus 1-2 iteration rounds. Cost reality only became visible after the HTTP 402 error today (Phaya's credits_used field reports 0 — balance delta is the truth).
- **TH**: Phaya balance เหลือ ฿17.49 — ไม่พอเสร็จ Concept 2 ด้วย Seedance. คลิป 8 วิ 720p+เสียง ราคา ฿24/คลิป × 5 คลิป = ~฿120. แนะนำเติม ฿300+ เพื่อให้พอจบ + iterate 1-2 รอบ.
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: concept-2-seedance-completion
- **Raised**: 2026-05-13T20:11:34Z
- **Resolved**: 2026-05-13T20:14:14Z — Top-up confirmed by board. Balance ฿17.49 → ฿161.49 (+฿144). Resuming Concept 2 Seedance run #11.
### [2026-05-13] EXTERNAL — Create GCP project + GCS bucket gs://auto-affi-media-dev + service account / สร้าง GCP project + bucket gs://auto-affi-media-dev + service account

- **EN**: Per ADR-006. Steps: 1) Pick/create GCP project. 2) Create bucket 'auto-affi-media-dev' (region: asia-southeast1 = Singapore, lowest latency from Phaya TH origin). 3) Service account 'auto-affi-media' with roles/storage.objectAdmin scoped to that bucket only. 4) Download JSON key, place at ~/.config/auto-affi/sa.json (chmod 600), set GOOGLE_APPLICATION_CREDENTIALS in .env. 5) Reply with project ID + bucket name confirmed.
- **TH**: ตาม ADR-006 — สร้าง GCP project, bucket asia-southeast1, service account จำกัด roles/storage.objectAdmin บน bucket นี้เท่านั้น แล้วใส่ key ลง .env
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: production-asset-pipeline + ADR-006
- **Raised**: 2026-05-13T09:51:07Z
- **Resolved**: 2026-05-13T10:00:22Z — Provisioned by claude-orchestrator via gcloud CLI on the aeternix account: bucket gs://auto-affi-media-dev in asia-southeast1 created, service account auto-affi-media@atn-tools.iam.gserviceaccount.com with roles/storage.objectAdmin scoped to the bucket only, key at ~/.config/auto-affi/sa.json (chmod 600), .env updated with AUTO_AFFI__GCS_BUCKET + GOOGLE_APPLICATION_CREDENTIALS. Live smoke test passed (upload + download + delete). Demo asset uploaded to gs://auto-affi-media-dev/demo/2026-05-13/demo-phaya-scene0.mp4.
### [2026-05-13] EXTERNAL — Provide PHAYA_API_KEY (phaya_live_xxx) / ส่ง PHAYA_API_KEY (phaya_live_xxx) ให้ระบบ

- **EN**: Phaya.io = Thai AI gateway (Bangkok). Sora 2 video, Thai TTS, Music, Embeddings, Image gen, Thai Subtitle — one vendor consolidates kie.ai + ElevenLabs + Flux + Suno (Phase 1 video stack). Adapter skeleton + tests landing this commit; only needs the live key to flip from dry-run to production. Set in .env as PHAYA_API_KEY. Never log, never commit.
- **TH**: Phaya.io = AI gateway สัญชาติไทย (กรุงเทพ). Sora 2 + เสียงไทย + Music + Embeddings + Thai Subtitle รวมในเจ้าเดียว แทน kie.ai + ElevenLabs ได้. ใส่ใน .env เป็น PHAYA_API_KEY.
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: phaya-live-integration
- **Raised**: 2026-05-13T09:21:10Z
- **Resolved**: 2026-05-13T09:35:51Z — Key delivered via clipboard, written to .env (0600). Live probes confirmed: auth OK (email=mr.phariyawit@gmail.com, balance=฿150), embed OK (4096-dim, ฿0.000028/call), chat OK in raw probe (Thai response). Adapter rewritten with correct paths from openapi.json. 12 unit tests pass.
<!-- RESOLVED_END -->
