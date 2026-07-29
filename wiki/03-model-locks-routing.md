# 03 — Model Locks & Provider Routing

> **Model locks เป็น compliance gate** (ดู [02-compliance-gates.md](02-compliance-gates.md) ข้อ 8–9) — ห้าม fallback เอง ถ้า model หลักใช้ไม่ได้ให้หยุดและรายงาน

## Production Locks (ปัจจุบัน)

| งาน | Lock | หมายเหตุ |
|---|---|---|
| **Text/story/script/reasoning** | Model text ที่กำหนดใน workflow ล่าสุดเท่านั้น | |
| **Stills / keyframes (image)** | **Nano Banana Pro** (`gemini-3-pro-image`) via `GEMINI_API_KEY` | `GeminiProvider` |
| **Video (image→video)** | **Kling 2.6** (`kling-2.6/image-to-video`) via kie.ai `KIE_API_KEY` | `KlingProvider` — **PRIMARY LOCK ตั้งแต่ 2026-07-24** |
| **Video (legacy / deliberate override)** | Veo 3.1 Fast (`veo-3.1-fast-generate-preview`) via `GEMINI_API_KEY` | เปิดด้วย `AUTO_AFFI_VIDEO_MODEL=veo` เท่านั้น — **ไม่ใช่ auto-fallback** |

### Video i2v lock — Kling 2.6 via kie.ai (2026-07-24)

- **สลับจาก Veo → Kling** หลังเทสต์จริง 3 ช็อต (hold / couple-hair / couple-CTA): Kling เท่าหรือดีกว่า Veo, ละเอียดกว่า (1076×1924 vs 720×1280), **ถูกกว่า 55–86%** (5s = 55 credits = $0.275 ≈ ฿9.3, VERIFIED via `creditsConsumed`). บน CTA, Kling ค้างคอมโพสิชัน (ของ+สบตา) ที่ Veo หลุด.
- **Adapter:** `src/auto_affi/adapters/kling_provider.py` (`KlingProvider`) — ผ่าน `enforce_spend_gate` เดิม (PGA + verify-before-spend), dry-run default, cost `_KLING_COST_PER_SECOND=0.055`. Stills ยังเป็น Nano Banana Pro; wiring คือ `RoutedGenProvider` + `build_default_provider()` ใน `routing_provider.py`.
- **Body:** `{model:"kling-2.6/image-to-video", input:{prompt:<motion-only>, image_urls:[PUBLIC_URL], sound:false, duration:"5"|"10"}}`. 9:16 = ป้อน still 9:16 (ไม่มี field aspect). `sound:false` → Thai VO mux แยก (no-lipsync). Seed ต้องเป็น **public URL** (host ผ่าน Postiz CDN — verified kie.ai ดึงได้).
- **Compliance — ห้าม auto-fallback:** ตามกติกาข้อบนสุดของไฟล์นี้ Kling fail → **หยุด+รายงาน** (default `video_fallback=None`). ถ้าจำเป็นต้องมี auto Kling→Veo สำหรับรัน unattended = opt-in ชัดเจนด้วย `build_default_provider(allow_veo_fallback=True)` เท่านั้น. Budget/gate DENY จะ propagate เสมอ (ไม่ "กู้" ด้วยการจ่ายแพงกว่า).

## Provider Endpoints & Auth

- **สถานะ: ยกเลิกการใช้งานทั้งหมด** ตามคำสั่งล่าสุด
- ~~Auth: `Authorization: Key {HF_API_KEY}:{HF_API_SECRET}` (env: `HF_KEY="key:secret"`)~~

- Create: `POST /api/v1/jobs/createTask` | Poll: `GET /api/v1/jobs/recordInfo?taskId=` | Credits: `GET /api/v1/chat/credit`
- Task states: `waiting`/`queuing`/`generating`/`success`/`fail`
- Rate limit: ≤20 requests/10s | 1 credit ≈ $0.005
- Transient 500: retry 3 ครั้ง + **cache segment ที่สำเร็จแล้ว** (กัน double-spend)


`aspect_ratio`: auto/16:9/9:16/4:3/3:4/1:1/21:9 · `duration`: int (default 5) · `genre`: auto/action/horror/comedy/noir/drama/epic · `mode`: std/fast · `resolution`: 480p/720p/1080p

**Prompt mode:** Nano Banana Pro = keyframe reference prompt (rich scene paragraph) / Seedance = motion prompt (physical motion เท่านั้น ห้าม re-invent visual identity) — ดู [Prompt Lock research](../docs/research/ai-video-prompt-lock-research-2026-06-06.md)


| Voice | ID | Note |
|---|---|---|
| **Brittney** — Social Media Youthful | `kPzsL2i3teMYv0FxEYQ6` | ⭐ Production default (V12 winner) |
| Eve — Energetic Happy | `BZgkqPqms7Kj9ulSkVzn` | Audition rank ต้น |
| Bella — Professional Bright Warm | `hpp4J3VqNfWAUOO0d1Us` | Baseline เดิม (V9 "too sleepy" ที่ stability 0.5) |
| Anika — Animated Friendly | `Sm1seazb4gs7RSlUVw7c` | |
| Hope — Bubbly Girly | `uYXf8XasLslADfZ2MB4u` | |
| Laura — Enthusiast Quirky | `FGY2WhTYpPnrIDTdsKH5` | |
| Lucy — Fresh Casual | `lcMyyd2HUfFzxdCaC4Ta` | |
| Adeline — Feminine Conversational | `5l5f8iK3YPeGga21rQIX` | |
| Emma — Adorable Upbeat | `pPdl9cQBQq4p6mRkZy2Z` | |
| Tiffany — Natural Welcoming | `6aDn1KB0hjpdcocrUkmq` | |


**VO text rules:** ห้าม raw spec/number (`UV50+`, `19 บาท`) — spell out เป็นภาษาไทย · audio tags (`[excited]`, `[friendly]`) ใช้ ≤1 tag/scene · `stability: 0.0` = expressive (เหมาะ Thai ads)

## Routing Ladder (อ้างอิง — แต่ production lock ยังคุม)

| Priority | Video | Image | หมายเหตุ |
|---|---|---|---|
| P2 (research only) | `veo3_1` | `flux_2` | |


## Post-Production Stack

| Tool | ใช้ทำ | กฎ |
|---|---|---|
| FFmpeg | Strip source audio, mux, assembly | ffmpeg local ไม่มี drawtext → ห้ามทำ Thai caption ด้วย ffmpeg |
| HyperFrames | Thai captions/CTA (HTML + GSAP + Sarabun font) | Deterministic, seekable, paused by default — แก้ปัญหา Pillow ไม่รองรับ Thai combining marks |
| `validate_caption_voice_sync.py` | Machine-check caption vs VO | Exit 1 = block final render |
| `brain_activity` | Virality score | รับ ≤16s — ใช้ hook sample; เป็น ranking signal ไม่ใช่ publish approval |

## Guardrails สรุป


---
[← Compliance Gates](02-compliance-gates.md) | [HOME](HOME.md) | [Data Registry →](04a-data-registry.md)
