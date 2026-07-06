# HyperFrames — Complete Guide (Auto-Affi)

**Last reviewed:** 2026-07-06 · **HF version:** v0.7.37 (live on this machine) · **Audience:** the Auto-Affi operator producing 9:16 Thai Shopee affiliate videos.

This is the single detailed entry point. It gives the **architecture + composition model + full catalog + compose cookbook + CLI/validation + worked example** in one place. The three focused reference docs go deeper on their slice:
- [hyperframes-components.md](hyperframes-components.md) — the 25 caption/effect components (exhaustive)
- [hyperframes-compose-cookbook.md](hyperframes-compose-cookbook.md) — assembling a full ad (track layout, custom clips, transitions)
- [hyperframes-packages-guides.md](hyperframes-packages-guides.md) — the 13 packages + 26 guides + validation gates

> Everything below is `[VERIFIED]` against the live CLI + installed source unless marked otherwise. Where a claim is doc-sourced (not personally re-run), it says so.

---

## 1. What HyperFrames is

**HyperFrames renders video from HTML.** A composition is an HTML file whose DOM declares timing with `data-*` attributes and whose animation is a **paused, seekable** GSAP timeline. The renderer plays no video in real time — it **seeks the timeline frame-by-frame**, screenshots each frame in a headless browser, and encodes the frames with FFmpeg.

For Auto-Affi it replaces the old hand-rolled ffmpeg-concat compose step: we author one HTML composition (Veo clips + Thai karaoke captions + CTA + overlays) and HF produces the polished master, deterministically and offline.

**Why it fits us:** deterministic (same input → same frames), offline (no cloud), renders Thai correctly, and its **producer auto-mixes audio** (Thai VO + ducked BGM) so we avoid the `amix duration=first` bug that once cut audio to scene 1.

---

## 2. Architecture — how a render actually happens

```
composition HTML (paused GSAP timeline)
        │
        ▼
 chrome-headless-shell  ×N workers     ← seek timeline to frame t, screenshot  (puppeteer, BeginFrame API)
        │  900 PNG frames (30s @ 30fps)
        ▼
 producer: FFmpeg encode  +  auto-mix all <audio> (VO + ducked BGM), mute videos
        │
        ▼
   master.mp4  (h264 + aac)
```

- **Render engine = headless Chrome.** `hyperframes doctor` lists `✓ Chrome` as a required dep; the binary is `chrome-headless-shell` under `~/.cache/puppeteer/…`, driven by **puppeteer-core** + `@puppeteer/browsers`. It is NOT the visible Google Chrome nor the `Control_Chrome` MCP — it's an invisible per-render process that spawns and tears down. `[VERIFIED: doctor + render logs — "Capturing frame N/900 (4 workers)"]`
- **Deterministic seek (BeginFrame).** On Linux + chrome-headless-shell the engine uses Chrome's BeginFrame API to advance virtual time exactly per frame — no wall-clock racing. An inline `<iframe>` or a stray `requestAnimationFrame` loop drops it to real-time Screenshot mode (non-deterministic) — avoid both. `[doc-sourced: engine, hyperframes-vs-remotion]`
- **producer** = the pipeline under `npx hyperframes render`: frame capture + encode + **audio auto-mix** + caption injection + optional `--docker` deterministic mode.
- **CLI** = the agent-facing wrapper over producer/engine. We drive HF **through the CLI only** (see §9).

---

## 3. The composition model — the `data-*` contract

A composition is one HTML file. The runtime reads these attributes:

**Root:**
```html
<div id="root" data-composition-id="main" data-start="0" data-duration="30"
     data-width="1080" data-height="1920"> … </div>
```
`data-duration` is the master length — **but see the #1 pitfall (§10): the real length is the last GSAP tween, not this.**

**Clips (video / caption / overlay) — anything timed carries `class="clip"`:**
```html
<video class="clip" data-start="0" data-duration="6" data-track-index="0" muted playsinline …>
<div   class="clip" data-start="6" data-duration="6" data-track-index="1"> caption </div>
```
- `class="clip"` is mandatory on any timed element — **without it the element shows for the whole video**, ignoring `data-start/duration`.
- `<video>` must be `muted` (headless autoplay fails otherwise → the clip silently drops; the producer also needs videos muted to own the audio mix).
- **Tracks:** clips on the **same `data-track-index` cannot overlap** — give overlapping layers different indices (see the track map in the cookbook).
- **Relative timing:** `data-start` accepts a number **or a clip id** — `data-start="scene-1 - 0.3"` = 0.3 s overlap (free crossfade, needs different tracks).

**Audio:**
```html
<audio src="vo1.wav" data-start="0.3"  data-track-index="2" data-volume="1.0"></audio>
<audio src="bgm.mp3" data-start="0" data-duration="30" data-track-index="3" data-volume="0.15"></audio>
```
The producer auto-mixes every `<audio>` and ducks under voice — no manual amix.

**Animation:** one paused GSAP timeline, registered for the renderer to seek:
```html
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });
  // …visual tweens only (opacity/x/y/scale/color)…
  window.__timelines['main'] = tl;   // renderer seeks THIS per frame — never .play()
</script>
```
**Rule:** GSAP drives **visual props only**. Never `video.play()/.pause()/.currentTime` in composition JS — the producer owns playback + ducking.

---

## 4. Offline-100% + deterministic Thai rendering

- **Vendor GSAP.** Default compositions load GSAP from a CDN (`cdn.jsdelivr.net`). For a hermetic render, vendor it: `curl -fsSL https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js -o hf/vendor/gsap.min.js` then `<script src="vendor/gsap.min.js">`. **Proof of offline:** grep the final `index.html` for `https?://` → must be **0**. `[VERIFIED: re-rendered, frame byte-identical to CDN version]`
- **Thai fonts = system.** Use `font-family:'Noto Sans Thai','Thonburi',sans-serif` — no `@font-face`, no external font. Complex stacking (สระ+วรรณยุกต์: ขึ้น/หลุด/ใต้) renders correctly. `[VERIFIED: pixel-checked]`
- **`--docker` for the final master.** Local render "may vary across platforms due to font/Chrome version differences." For Thai this matters: a reflow shifts word-karaoke `{start,end}` timing. `--docker` pins Chrome+fonts+FFmpeg (deterministic). Use it for masters; local for iteration. `[doc-sourced: rendering, troubleshooting]`

---

## 5. Thai word-karaoke — the unlock

Word-level karaoke synced to a Thai VO is the core caption style. The trap: **Whisper is useless for Thai** — Thai has no inter-word spaces, so `hyperframes transcribe --model small --language th` returns `wordCount=1` AND wrong text (ลด→รถ).

**The working pipeline** `[VERIFIED: rendered, highlight advances แฟน@1.6s → หลุด@14s → บาท@26.5s]`:
1. We already KNOW the exact VO script → don't transcribe it.
2. `pythainlp` 5.3.4 `word_tokenize(text, engine="newmm")` splits each Thai line into real words (เมื่อก่อน|แฟน|ไม่ค่อย|มั่นใจ…).
3. `ffprobe` each VO wav's duration; distribute word timings across `[shot_start+0.35 … +dur]` weighted by `len(word)`; emit the flat `[{id,text,start,end}]` array HF captions consume.
4. Render each word as `<span id="wN">`; GSAP `tl.to('#wN',{color:'#ffd24a',scale:1.16},word.start)` then settle to white at `word.end`.

This same `{text,start,end}` array feeds **every** HF caption component — switching caption styles is a font+layout job, not a data job.

### The 5 universal rules for ANY HF caption on Thai
Every caption ships English-landscape. Before shipping Thai:
1. **Swap the font** — all ship Latin-only faces (Anton/Montserrat/Poppins/Gabarito/Playfair), no Thai glyphs → tofu. Use Noto Sans Thai / Kanit 900.
2. **Retarget 1920×1080 → 1080×1920** (data-width/height + viewport + CSS + `fitFontSize` maxWidth).
3. **Feed the pythainlp word array** — never their `.split(" ")`; set flex `gap:0`.
4. **Vendor GSAP + fonts** for offline.
5. **Patch Latin-only regexes** — `.replace(/[^a-z]/g,"")` nukes Thai keyword/emoji/accent lookups.

**Key finding:** no component breaks Thai by animating the *real text* per-character — all use whole-word `.textContent` spans, so combining marks stay attached. "caution" verdicts are about font/regex, not glyph safety.

---

## 6. Component catalog (25) — ranked for Thai Shopee ads

Full detail in [hyperframes-components.md](hyperframes-components.md). Summary by fit (0–5):

**Tier 1 — USE (fit 4):**
| Component | Cat | Where in the ad |
|---|---|---|
| `caption-highlight` | caption | benefit bullets, CTA — red pill sweep (most Shopee-native) |
| `caption-clip-wipe` | caption | hook + benefits — gold keyword flash |
| `caption-kinetic-slam` | caption | **hook** — one giant word slams in |
| `caption-gradient-fill` | caption | hook + benefits — rainbow karaoke sweep |
| `caption-emoji-pop` | caption | benefit bullets — 1-3 word chunks + emoji (patch Thai regex) |
| `caption-blend-difference` | caption | auto-legibility over any b-roll |
| `shimmer-sweep` | text-fx | **price/CTA/brand** glint |
| `vignette` | overlay | b-roll polish, focus + legibility |

**Tier 2 — with care (fit 3):** `caption-neon-glow`, `caption-parallax-layers`, `caption-neon-accent`, `caption-particle-burst`, `caption-weight-shift`, `caption-pill-karaoke`, `caption-editorial-emphasis`, `caption-glitch-rgb`, `caption-texture`, `morph-text`, `grain-overlay`, `grid-pixelate-wipe`, `parallax-zoom`, `parallax-unzoom`.

**Tier 3 — niche/avoid (fit ≤2):** `matrix-decode` (Latin-locked scramble), `motion-blur` (moving elements only, never captions), `texture-mask-text` (static).

---

## 7. Blocks (109) — categories

Blocks are standalone sub-compositions (own `data-width/height/duration`), added via `data-composition-src`. Relevant families:
- **Shader transitions (14):** `cinematic-zoom`, `whip-pan`, `flash-through-white`, `chromatic-radial-split`, `glitch`, `light-leak`, `swirl-vortex`, `ripple-waves`, `sdf-iris`, `thermal-distortion`, `cross-warp-morph`, `gravitational-lens`, `ridged-burn`, `domain-warp-dissolve` — **≤2 per video**, 0.3–0.6 s each.
- **Transition galleries (13):** `transitions-scale/-dissolve/-cover/-push/-radial/-blur/-3d/-light/-grid/-mechanical/…` — CSS transition reference sets.
- **Lower-thirds (12):** `lt-soft-pill`, `lt-clean-bar`, `lt-dark-card`, `lt-bold-block`, `lt-accent-underline`, `yt-lower-third`, …
- **Social overlays (7):** `tiktok-follow`, `instagram-follow`, `x-post`, `reddit-post`, `spotify-card`, `macos-notification`, `yt-lower-third`.
- **Maps/data-viz (8), code (24+9), liquid-glass (7), VFX (6), showcases (6)** — mostly out-of-scope for product ads.

Full shader table + editorial policy in the [cookbook §5](hyperframes-compose-cookbook.md).

---

## 8. Compose cookbook — assembling a full ad

Full detail in [hyperframes-compose-cookbook.md](hyperframes-compose-cookbook.md). The essentials:

- **Track map:** `0` scenes · `3` captions · `4` lower-third/price/CTA · `5` persistent `#โฆษณา` · `6` endcard. Same-track clips can't overlap.
- **HF has NO cta/endcard/sticker/badge block** — build CTA, price card, disclosure, endcard as custom `<div class="clip">` clips (worked markup in the cookbook).
- **Caption anti-leak:** after a caption's exit fade, `tl.set('#capN',{opacity:0,visibility:'hidden'})` so it can't bleed onto the next.
- **Transitions:** keep most cuts HARD; spend a shader on only 1–2 meaning moments (hook→demo `whip-pan`; final→CTA `flash-through-white`).
- **Beats:** `npx hyperframes beats --json` → snap caption/transition `data-start`s to the BGM.
- **#โฆษณา disclosure:** persistent full-duration + repeated on the endcard; human-verify against Thai ad-disclosure rules (HF only guarantees it renders).

---

## 9. CLI + validation gates

We drive HF through the CLI. The commands we use: `render`, `add`, `catalog`, `transcribe`, `beats`, `doctor`.

**ADOPT these validation gates** (our biggest gap — we currently eyeball):
| Gate | Catches |
|---|---|
| `hyperframes lint` (before every render) | caption missing `class="clip"` (shows whole video), **unmuted `<video>`** (silent drop), missing `data-width/height` |
| `hyperframes inspect --at <beats> --json` | Thai text overflow / occlusion / overlap in 9:16 |
| `hyperframes render --docker` (final master) | font/Chrome drift → karaoke timing mis-align |
| `hyperframes auth status --json` (preflight) | silent local TTS/BGM fallback when no key |

Also: downsize source images to ≤2× canvas (Chrome decodes to `w×h×4` RGBA regardless of file size).

---

## 10. Pitfalls to avoid (mistake → fix)

1. **Video cut off early** — length = last GSAP tween, not `data-duration`. Fix: `tl.set({},{},TOTAL_VO_SECONDS)` pad. ✅ we do this.
2. **Caption for whole video** — missing `class="clip"`. Fix: always add it (+ `data-start/duration/track-index`).
3. **Animating a `<video>`** stops Chrome updating frames. Fix: wrap in a div, animate the wrapper.
4. **Scripts controlling media** desync the mix. Fix: GSAP visual props only.
5. **`Math.random()` / `Date.now()`** break determinism. Fix: seeded PRNG.
6. **Render length NOT variable-drivable** — `data-duration` read once. Fix: separate HTML per length.
7. **Thai font missing → reflow → timing drift.** Fix: vendor Noto Sans Thai + `--docker`.
8. **Inline iframe / stray rAF** drops determinism. Fix: keep overlay HTML clean.
9. **`doctor --json` exits 0 even when unhealthy.** Fix: gate on `jq -e '.ok'`.
10. **`feedback --file-issue` / `publish` upload publicly.** Never run on a client ad.

---

## 11. Packages — stay on the CLI

Verdict: import nothing. `@hyperframes/lint` is the only candidate (structured findings vs stdout scraping) if parsing gets brittle. `@hyperframes/engine` **loses the producer's audio auto-mix**. `producer/core/parsers/player/sdk/studio` — no. **Out of scope:** `aws-lambda`/`gcp-cloud-run` (cloud fan-out), 4K/HDR, website-to-video, Figma, Studio GUI. Detail in [packages-guides](hyperframes-packages-guides.md).

---

## 12. Worked example — the CLEAR Men couple ad

`runs/2026-07-04-clear-men-couple-v9/hf/` — the reference implementation. Builder committed at [docs/reference/examples/hf-clear-men-karaoke-build.py](examples/hf-clear-men-karaoke-build.py) (run outputs are gitignored; the master is regenerable).

30 s, 1080×1920, offline-100%:
- 5 Veo i2v clips (4 s → stretched 6 s), per-clip cinematic-zoom
- Thai word-karaoke (44 words via pythainlp), highlight advances with the VO
- **vignette** (ellipse, α .5) over all shots — captions kept above it via z-index
- **shimmer-sweep** glint across the orange price card at the endcard (whole-card sweep — a white glint over white-on-orange text is invisible; sweep the coloured container instead)
- animated Shopee CTA endcard + persistent #โฆษณา
- producer audio auto-mix (Thai VO + ducked BGM) — verified non-silent in all 5 shots

Fits [gold-standard-ad-recipe.md](gold-standard-ad-recipe.md) step 6 (compose).

---

## Related
- Reference docs: [components](hyperframes-components.md) · [compose-cookbook](hyperframes-compose-cookbook.md) · [packages-guides](hyperframes-packages-guides.md) · [gold-standard-ad-recipe](gold-standard-ad-recipe.md)
- Official docs: `hyperframes.heygen.com/llms.txt` (index) · `/packages/*` · `/guides/*` · `/catalog/components|blocks/*`
- Memory: `project-hyperframes-compose`, `reference-hyperframes-components`, `reference-hyperframes-packages-guides`
