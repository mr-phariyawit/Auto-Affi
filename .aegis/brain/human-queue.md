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
<!-- PENDING_END -->

## Resolved

<!-- RESOLVED_START -->

### [2026-05-13] EXTERNAL — Provide PHAYA_API_KEY (phaya_live_xxx) / ส่ง PHAYA_API_KEY (phaya_live_xxx) ให้ระบบ

- **EN**: Phaya.io = Thai AI gateway (Bangkok). Sora 2 video, Thai TTS, Music, Embeddings, Image gen, Thai Subtitle — one vendor consolidates kie.ai + ElevenLabs + Flux + Suno (Phase 1 video stack). Adapter skeleton + tests landing this commit; only needs the live key to flip from dry-run to production. Set in .env as PHAYA_API_KEY. Never log, never commit.
- **TH**: Phaya.io = AI gateway สัญชาติไทย (กรุงเทพ). Sora 2 + เสียงไทย + Music + Embeddings + Thai Subtitle รวมในเจ้าเดียว แทน kie.ai + ElevenLabs ได้. ใส่ใน .env เป็น PHAYA_API_KEY.
- **Category**: External access
- **Raised by**: claude-orchestrator
- **Blocks**: phaya-live-integration
- **Raised**: 2026-05-13T09:21:10Z
- **Resolved**: 2026-05-13T09:35:51Z — Key delivered via clipboard, written to .env (0600). Live probes confirmed: auth OK (email=mr.phariyawit@gmail.com, balance=฿150), embed OK (4096-dim, ฿0.000028/call), chat OK in raw probe (Thai response). Adapter rewritten with correct paths from openapi.json. 12 unit tests pass.
<!-- RESOLVED_END -->
