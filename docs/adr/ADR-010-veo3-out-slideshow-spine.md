# ADR-010 — Veo3 out of ad spine → Ken Burns slideshow

I have everything I need. The research is grounded and the current stack is verified. Here's the decision.

---

# Auto-Affi Ad Spine — PIVOT DECISION

## 1. Verdict on Veo3

**MAKE OPTIONAL — b-roll accent only, never the spine.** Retire Veo3 from the ad backbone. All four research streams converge: Veo3 produces isolated 4s photoreal "moments" with no continuity, no lipsync, no product mechanism, cannot animate an absence (the umbrella-335 "no-drip" bug proved this), and costs $1.60/4s (~฿38+/15s). It has **zero conversion signal** in the Thai affiliate market where proof and authenticity drive impulse buys. Keep it in the toolbox for the occasional 3-5s cinematic accent — but a run should never *require* it.

## 2. Recommended Primary Format — KINETIC PRODUCT-PHOTO SLIDESHOW (Ken Burns + Thai VO + HyperFrames)

**The spine: Nano Banana stills → Ken Burns zoom/pan in HyperFrames → ElevenLabs v3 Thai VO + Suno BGM + Thai captions → 9:16 MP4.**

**Why it converts (Thai Shopee/TikTok Shop):**
- "Simple slideshows outperform high-production ads by **+30% ROAS**" — proof beats polish in the Thai impulse market.
- Real product stills = **trust signal**; AI-isolated Veo moments read as fake (Thai consumers: 86% prefer authentic/honest).
- Voiceover-led = **+12-18% conversion vs text-only**; captions mandatory (30% audience loss if audio-only).
- Ken Burns motion = scroll-stop on a motion-sensitive feed; matches the proven 15s Hook(≤3s)→Demo→CTA (PAS) formula.
- **The proof moment is a REAL still** (dry canopy sealed in the case), not an AI gamble — this is exactly the "no-drip" problem that killed the old umbrella run.

**Why it's executable NOW:** every tool is already verified live on this Mac (umbrella-335, 2026-06-29/30). Nano Banana stills ✓, kie.ai ElevenLabs v3 Thai VO ✓, kie Suno BGM ✓, HyperFrames v0.7.18 CLI (doctor PASS, deterministic FREE render) ✓. **Zero new integration, zero Veo dependency, ~฿20-50/spot.** Swap stills = new variation → 5-10 A/B variants in a batch.

## 3. Ranked Fallback Ladder

| Rank | Path | When to use | Cost (18s video) |
|------|------|-------------|------------------|
| **Spine (default)** | Ken Burns slideshow (Nano Banana + HyperFrames) | Every product | **~฿20-50** (VO+BGM only; render free) |
| **2nd — AI avatar presenter** | **Kling Avatar 2.0** on kie.ai (image+audio→talking presenter, Thai, 1080p, real continuity/lipsync) | Products that need a spokesperson (supplements, gadgets w/ claims) | ~฿1.7-2.2 avatar + VO/BGM ≈ **<฿40** |
| **3rd — motion b-roll** | **Seedance 2.0 Fast** on kie.ai ($0.022/s, best logo/text fidelity) | 5s motion accent inside the slideshow spine | ~฿0.66-0.88/5s |
| Reserve | InfiniteTalk (avatar, needs clip-stitching) / Veo3 (cinematic accent only) | Only if 2nd/3rd fail | ฿2.7-3.6 / ฿38+ |

Note: avatar-presenter (2nd) is the strongest *upgrade* path if slideshow ROAS plateaus — it adds a human face without a $150-300 creator hire, all on kie.ai you already have.

## 4. Keep / Drop from Current Stack

**KEEP (all verified, all core):**
- **Nano Banana Pro** — product stills. The whole spine feeds off these. KEEP.
- **kie.ai ElevenLabs v3 Thai VO** — `[excited]`/`[friendly]`+`stability`+`language_code:th`. KEEP (human directive; proven parity with human VO).
- **kie Suno BGM** — trending/instrumental. KEEP.
- **HyperFrames v0.7.18** — the deterministic free compositor (Ken Burns, captions, lower-thirds, CTA, transitions). This becomes the *primary render engine*, not just post. KEEP + promote.

**DROP / MAKE OPTIONAL:**
- **Veo3** — remove from the spine. Keep the two gate guards (`PROMPT_MODE_MISMATCH`, `VEO_PROVE_NEGATIVE`) as a safety net for the rare accent use. Optional, not required.

**Practical note:** the current Gemini spend-cap blocker (ai.studio/spend, from the 2026-06-30 handoff) still gates *Nano Banana* stills. VO/BGM/render are on other providers and are unblocked — but you can't ship the slideshow until Nano Banana stills can generate. This is the one live external blocker.

## 5. Concrete 15-18s Umbrella Skeleton (GEESO 335 — crook-handle, black-out/yellow-in, integrated hard-case tube)

PAS spine, 5 stills, Ken Burns paths. Product = real photos (mechanism corrected in handoff: seals wet canopy in an integrated ribbed case → **ล็อกน้ำฝนไว้ใน · แขวนได้ทุกที่**).

| Beat | Time | Still (Ken Burns) | Thai caption / VO |
|------|------|-------------------|-------------------|
| **HOOK** | 0-3s | Rainy street / wet bag, fast push-in | คatpion: "ฝนตก กระเป๋าเปียกทุกที?" · VO `[excited]`: "ร่มพับที่ล็อกน้ำไว้ในตัว!" |
| **DEMO 1** | 3-8s | Umbrella open in rain, yellow interior, slow pan | "กันฝน UPF50+ เบา 125g" |
| **DEMO 2** | 8-12s | Wet canopy retracting into the ribbed hard-case tube, push-in on mechanism | "พับเก็บ = ล็อกน้ำฝนไว้ในเคส" |
| **PROOF (still)** | 12-14s | Sealed case held over a dry bag/dry hand — **real still, not motion** | "ไม่หยดเลย แขวนได้ทุกที่" |
| **CTA** | 14-18s | Product hero + price card, scale-in entrance, Shopee orange #EE4D2D | "JIAP DEALS · ฿335 · กดตะกร้าสีส้ม" |

Audio: VO 100% / Suno BGM ~30% ducked. Captions phrase-level (Thai whisper word-sync is NOT viable — verified). Font: Noto Sans Thai @font-face (lint-enforced). Whip-pan Hook→Demo, flash-to-white → CTA; hard cuts elsewhere.

**Est. cost this spot:** Nano Banana 5 stills ~฿8-15 + kie VO ~฿5-15 + Suno BGM ~฿5-10 + HyperFrames render FREE = **~฿20-45**. (vs old Veo umbrella run $25.6 with $14.4 wasted.)

## 6. New Tool to Get Access To

**Kling Avatar 2.0 via kie.ai** — already on the kie.ai platform you're authenticated to, so this is **enabling a model, not a new subscription**. ~$0.0562/sec Standard (~฿1.7-2.2 per 18s video). This is your fallback #2 (presenter format) and the single highest-leverage upgrade if the slideshow needs a human face. **Do not buy Creatify/JoggAI/HeyGen** ($36-49/mo) — Kling Avatar on your existing kie.ai account covers the avatar use case at a fraction of the cost and with native Thai + API automation.

**Everything else in the recommended spine you already own.** No new spend required to ship the slideshow format.

---

**Bottom line:** Veo3 out of the spine → **Ken Burns slideshow** in, on tools already verified working, at ~฿20-45/spot with +30% ROAS backing. Avatar (Kling on kie.ai) is the one upgrade to unlock as fallback #2. First action gated only by the Gemini spend cap for Nano Banana stills.

Files referenced: `/Users/phariyawit.jiap/Documents/Auto-Affi/runs/2026-06-30-umbrella-335/` (BRIEF.md, STORYBOARD.md), `docs/reference/short-form-format-v2.md`, `docs/reference/hyperframes-*.md`, `docs/reference/kie-elevenlabs-vo.md`, `docs/templates/hyperframes-short-skeleton.html`, `.aegis/brain/handoffs/2026-06-30-umbrella-handoff.md`.
---

## ADDENDUM (2026-07-02) — Veo IS viable with the RIGHT method: LOCKED CHAR-SHEET + referenceImages

User insight ("สร้างตัวละครแล้ว lock ด้วย") resolved the whole Veo problem. Two method errors, both fixed:

1. **Use `referenceImages`, NOT image-to-video (i2v).** i2v locks the exact first frame → Veo can only gently
   nudge a static frame (why every clip looked stiff). `referenceImages` (Veo 3.1/3.1-fast, "asset" type, up to 3,
   **forces durationSeconds=8 ≈ $3.20**) lets Veo generate FRESH cinematic motion (orbit/rotate/rack-focus).
2. **Feed a LOCKED product CHAR-SHEET, not raw source photos.** Raw Shopee photos (text overlays, mixed
   states/variants) made Veo drift to a generic umbrella (lost the hard-case mechanism). A clean, consistent
   3-view studio char-sheet (Nano Banana: open · cased · hero, neutral bg, no text, same variant) LOCKS the
   identity → Veo keeps the exact product (ribbed hard-case tube + yellow + crook handle) AND moves dynamically.

**Verified live 2026-07-02** (runs/2026-06-30-umbrella-335/05-shots/reftest/): raw-refs = big motion but wrong
product; locked-char-sheet refs = faithful product + premium rain-rotation. Char-sheet fidelity slightly calms
motion (Veo stays near refs) — acceptable tradeoff for a hero shot.

### Revised pipeline (hybrid, one lock feeds everything)
1. **Always build a LOCKED CHAR-SHEET first** (Nano Banana, clean studio, 3 consistent views) — the master identity lock.
2. **Veo `referenceImages` (8s, ~$3.20)** off the char-sheet → 1 premium HERO/hook shot (dynamic + faithful). NOT i2v.
3. **Char-sheet stills → HyperFrames Ken-Burns slideshow** for the exact demo/proof/CTA beats (cheap, pixel-exact).
4. kie ElevenLabs VO + Suno BGM + HyperFrames compose → master.

New gate rule to add: if `prompt_mode == "referenceImages"` require a char-sheet ref set (not raw photos) + duration==8.
i2v remains allowed but flagged "static-motion; prefer referenceImages for hero shots."
