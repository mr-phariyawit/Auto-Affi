# HyperFrames Compose Cookbook — assembling a full Thai ad

**Last reviewed:** 2026-07-06 · **HF version:** v0.7.37 · **Scope:** the operational "how to lay out a complete 9:16 Thai Shopee ad" reference — track layout, scene chaining, custom clips HF has no block for (CTA / price card / disclosure / endcard), caption anti-leak, shader-transition editorial policy, and beat detection.

**Provenance:** Consolidated 2026-07-06 from three retired reference docs (`hyperframes-capability-map.md`, `hyperframes-caption-compose.md`, `hyperframes-transitions.md`) — only the still-accurate, unique content survived a coverage-diff against the two source-verified docs below (stale v0.7.18 claims dropped). Complements, does not duplicate:
- [hyperframes-components.md](hyperframes-components.md) — *what* the 25 caption/effect components are + 5 Thai-safety rules
- [hyperframes-packages-guides.md](hyperframes-packages-guides.md) — the CLI, render/validation gates, packages verdict
- [gold-standard-ad-recipe.md](gold-standard-ad-recipe.md) — the locked end-to-end pipeline

> **Always:** vendor GSAP locally (`hf/vendor/gsap.min.js`, never a CDN — CSP-blocked + non-hermetic), feed the pythainlp `{text,start,end}` array for any word-karaoke, and drive only **visual** props with GSAP — never `video.play()`/`.pause()`/`currentTime` (the producer owns playback + VO-over-BGM ducking).

---

## 1. Track-index layout

Clips on the **same** `data-track-index` **cannot overlap** — give overlapping layers different indices. A full ad:

| Track | Layer |
|:--:|---|
| `0` | Veo scenes (chained, relative timing) |
| `-1` | VO audio — but prefer the producer's auto VO+ducked-BGM mix over a hand-placed clip |
| `3` | Animated Thai captions (word-karaoke) |
| `4` | Lower-third: brand + price + CTA bar |
| `5` | Persistent `#โฆษณา` disclosure (full duration) |
| `6` | Full-screen CTA endcard |

---

## 2. Scene chaining + declarative crossfade (no shader needed)

`data-start` accepts a plain number of seconds **or a clip id** — relative timing gives a free CSS crossfade:

- `data-start="intro"` → start when `intro` ends (hard butt-join)
- `data-start="intro - 0.5"` → 0.5s **overlap = crossfade** (the two clips must be on **different tracks**)
- `data-start="intro + 2"` → 2s gap
- other timing attrs: `data-duration`, `data-media-start`, `data-volume`

```html
<video id="scene-1" class="clip" data-start="0"             data-duration="4"
       data-track-index="0" muted playsinline src="./clips/veo-01.mp4"
       style="width:100%;height:100%;object-fit:cover;"></video>
<video id="scene-2" class="clip" data-start="scene-1 - 0.3" data-duration="4"
       data-track-index="0" muted playsinline src="./clips/veo-02.mp4"
       style="width:100%;height:100%;object-fit:cover;"></video>
<!-- scene-3: data-start="scene-2 - 0.3", scene-4: data-start="scene-3 - 0.3" -->
```
*(For a real overlap-crossfade rather than a butt-join, put alternating scenes on tracks 0 and 1 so they can overlap.)*

---

## 3. Custom clips — CTA / price card / disclosure / endcard

> HyperFrames has **no** named `cta-*` / `endcard-*` / `sticker` / `badge` block (probe 404 — confirmed non-existent). Build these as **custom `<div class="clip">` clips**. (For lower-third *chrome* you can use the catalog `lt-*` blocks — see components §8 — but the price/CTA/endcard content is hand-authored.) Worked example: JIAP DEALS · ฿335 · กดตะกร้าส้ม · #โฆษณา.

### Lower-third: brand + price + CTA bar (track 4)

```html
<div id="lower-third" class="clip" data-start="2" data-duration="11" data-track-index="4"
     style="position:absolute;bottom:60px;left:0;right:0;height:120px;background:rgba(0,0,0,0.8);
            display:flex;align-items:center;justify-content:space-between;padding:0 30px;">
  <div class="thai-cap" style="font-size:48px;font-weight:900;">JIAP DEALS</div>
  <div id="price-tag" class="thai-cap" style="font-size:56px;color:#ff6b35;font-weight:900;">฿335</div>
  <div id="cta-btn" class="thai-cap" style="background:#ff8c42;padding:12px 28px;border-radius:8px;font-size:32px;">กดตะกร้าส้ม</div>
</div>
```
```js
// entrance + life of the lower-third (visual props only — never touch media playback)
tl.from('#lower-third', { y:200, opacity:0, duration:0.5 }, 2);                    // slide up
tl.to('#price-tag',     { scale:1.12, duration:0.3, yoyo:true, repeat:1 }, 2.4);   // price pop
tl.to('#cta-btn',       { boxShadow:'0 0 30px rgba(255,140,66,0.9)',
                          duration:0.6, yoyo:true, repeat:-1 }, 2.6);              // CTA pulse
```

### Persistent #โฆษณา disclosure (track 5, full duration)

```html
<div id="disclosure" class="clip thai-cap" data-start="0" data-duration="15" data-track-index="5"
     style="position:absolute;bottom:24px;right:20px;font-size:28px;color:#ddd;">#โฆษณา</div>
```

### Full-screen CTA endcard (track 6)

```html
<div id="endcard" class="clip" data-start="13" data-duration="2" data-track-index="6"
     style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
            background:rgba(0,0,0,0.72);">
  <div class="thai-cap" style="text-align:center;">
    <div style="font-size:64px;font-weight:900;margin-bottom:24px;">กดตะกร้าส้ม</div>
    <div style="font-size:40px;color:#ffd54a;">฿335 · JIAP DEALS</div>
    <div style="font-size:28px;color:#bbb;margin-top:18px;">#โฆษณา</div>
  </div>
</div>
```
```js
tl.from('#endcard', { opacity:0, scale:0.96, duration:0.4 }, 13);
```

**Legal note (not a HyperFrames guarantee):** keep `#โฆษณา` **persistent (full duration, track 5) AND repeated on the endcard**. HF only guarantees it *renders* — a human must confirm placement/duration against current Thai ad-disclosure rules.

---

## 4. Caption hard-kill (anti-leak)

After every caption's exit fade, also `visibility:hidden` it so it can't bleed onto the next caption:

```js
tl.from('#cap1', {opacity:0, y:50, duration:0.3}, 1);
tl.to('#cap1',   {opacity:0, duration:0.3}, 3.6);
tl.set('#cap1',  {opacity:0, visibility:'hidden'}, 3.9);   // hard kill so it can't leak onto cap2
```

---

## 5. Shader transitions — 14 effects + editorial policy

> Add a shader transition as a **block**: `npx hyperframes add <name>`, then wire declaratively with `data-composition-src` (components §8). Use **≤2 per video**, short `duration` (**0.3–0.6s** — the catalog ships each as a 4s showcase, far too long), and retarget the 1920×1080 showcase to 1080×1920.

| shader | effect | best moment in an affiliate short |
|---|---|---|
| `flash-through-white` | white-flash crossfade | **PRODUCT REVEAL / hero** (climax, 0.5–1s) — top pick for the CTA reveal |
| `chromatic-radial-split` | RGB chromatic-aberration radial split | climactic hero/price reveal, pulls focus to center |
| `glitch` | digital glitch artifacts | hook / disruption; **tech/digital products** |
| `light-leak` | cinematic light sweep | reveal or CTA; premium polish |
| `cinematic-zoom` | dramatic zoom blur | showcase→CTA pivot, feature change |
| `whip-pan` | fast camera whip-pan | energetic cut between demo beats / problem→solution |
| `domain-warp-dissolve` | fractal-noise organic dissolve | lifestyle → product close-up; soft midpoint |
| `ripple-waves` | concentric ripple distortion | product reveal; outward motion draws focus |
| `sdf-iris` | SDF circular iris open/close | reveal; geometric focus to center |
| `thermal-distortion` | heat-haze shimmer | premium polish → high-impact shot |
| `swirl-vortex` | swirling vortex distortion | transformative claim / pivotal moment |
| `cross-warp-morph` | morph-blend between two images | **before/after**, product-angle change |
| `gravitational-lens` | spacetime-bend warp | premium / upgrade / before-after |
| `ridged-burn` | ridged-turbulence burn | dramatic reveal / special offer |

**Editorial policy for sub-30s shorts:**
- **Keep most cuts HARD (no shader).** 3+ cuts in the first 3s lifts completion; a shader on *every* cut reads as AI-slop. Spend a shader on only **1–2 meaning moments**.
- **Hook → first demo:** `whip-pan` (~0.4s) — energy, problem→solution.
- **Within a continuous demo** (insert → lift → hang): **hard cuts** for continuity — no shader.
- **Final → CTA hero / price reveal:** `flash-through-white` or `chromatic-radial-split` (~0.5s) — the one hero beat.
- Carry price/CTA emphasis with **lower-thirds (`lt-*`)** + **caption effects (`caption-*`)**, not with a shader.

---

## 6. Beat detection — `hyperframes beats`

**`npx hyperframes beats [DIR] --json`** — detects beats in the project's music track (headless) and writes `beats/<audio>.json`. `[VERIFIED LIVE: beats --help, v0.7.37]`

- Snap caption/transition `data-start`s to the emitted beat times so cuts land on the BGM — the cheap "feels professional" multiplier in a 15s vertical ad.
- Only the standalone `beats` command exists — there is **no** `render --beats` flag at v0.7.37.
- Optional / not in the current locked recipe; add only for a music-synced edit.

---

## Related
- [hyperframes-components.md](hyperframes-components.md) · [hyperframes-packages-guides.md](hyperframes-packages-guides.md) · [gold-standard-ad-recipe.md](gold-standard-ad-recipe.md)
- Memory: `project-hyperframes-compose`, `reference-hyperframes-components`, `reference-hyperframes-packages-guides`
