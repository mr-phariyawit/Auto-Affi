I have everything I need. The compose recipe will reference the existing transitions doc's `init({scenes, transitions})` API exactly. Returning the consolidated playbook as Markdown.

---

# Auto-Affi HyperFrames — Caption & Compose Playbook

> Consolidates 4 probe runs (all `hyperframes.heygen.com/llms.txt` + package docs `[PROBED]`) into a concrete, ready-to-run recipe for the JIAP DEALS umbrella 15s short (9:16, ฿335, กดตะกร้าส้ม, #โฆษณา). Pairs with the in-repo transition reference `docs/reference/hyperframes-transitions.md`.
>
> **Tag legend:** `[PROBED]` = verified against probed HyperFrames docs. `[UNVERIFIED]` = pattern-level inference / not confirmed on a probed page → treat as needs-a-test-render.

---

## 0. The non-negotiable rules (memorize these — they break renders silently)

`[PROBED]`
1. Root element MUST have `data-composition-id`, `data-width`, `data-height`. (Some docs also show `data-composition-duration` / `data-composition-variables` on root — both forms appear; `data-composition-id/width/height` is the consistent minimum.)
2. Every timed element MUST have `class="clip"` + `data-start` + `data-duration` + `data-track-index`.
3. Clips on the **same** `data-track-index` **cannot overlap** — give overlapping captions/lower-thirds **different track indices**.
4. GSAP timeline MUST be `gsap.timeline({ paused: true })` and registered as `window.__timelines['<composition-id>'] = tl`. The framework drives it — never call `.play()`, `.pause()`, `video.play()`, or set `currentTime`.
5. **Composition length = last GSAP tween endpoint**, NOT the video length. Pad with `tl.set({}, {}, 15)` to force a 15s timeline.
6. **Never animate `<video>` width/height/dimensions directly** — it halts frame capture. Wrap the video in a `<div>` and animate the wrapper (`scale`, `x`, `y`).
7. Videos must be `muted playsinline`. Audio is a separate `<audio class="clip">` track — the framework auto-extracts + muxes via FFmpeg.
8. Determinism: **no** `Math.random()`, `Date.now()`, `requestAnimationFrame`, or unseeded randomness. Same input → identical MP4.

---

## 1. Caption blocks + Thai text/font

### 1a. Available caption / text-animation blocks `[PROBED]`
16 verified (names converge across all 3 deep probes): `pill-karaoke` (word-by-word highlight), `kinetic-slam`, `neon-glow`, `neon-accent`, `highlight`, `gradient-fill`, `glitch-rgb`, `emoji-pop`, `matrix-decode`, `parallax-layers`, `particle-burst`, `clip-wipe`, `editorial-emphasis`, `texture`, `weight-shift`, `blend-difference`.

Install any block: `npx hyperframes add <block-name>` → emits an installable snippet you embed as a sub-composition (`data-composition-src="compositions/<block>.html"`). `[PROBED]`

> ⚠️ `[UNVERIFIED]` Individual per-block doc pages (e.g. `/catalog/blocks/pill-karaoke.md`) returned **404** in probes. Block **names** are confirmed (from `/llms.txt`); their exact installed markup/params are **not** doc-confirmed. Treat installed-block internals as needing a snapshot test (§3, step 6).

### 1b. Thai text + font `[PROBED]`
- HyperFrames renders all text via **Chrome headless (Harfbuzz)** → proper Thai grapheme shaping. **No `ffmpeg drawtext` Thai workaround needed.**
- Standard CSS `font-family` / `@font-face` works; **no documented limitation on Thai/Unicode.**
- **Recommended:** embed a Thai-capable font via `@font-face` (don't rely on system fallback — OS-dependent). `Noto Sans Thai` (covers U+0E00–U+0E7F) is the safe default; `Thonburi` is a macOS system fallback.
- For cross-platform identical output, render with `--docker` (bundles consistent Chrome + fonts). `[PROBED]`

```html
<style>
@font-face {
  font-family: 'Noto Sans Thai';
  src: url('./fonts/NotoSansThai-Bold.ttf') format('truetype');
  font-weight: 700;
}
.thai-cap {
  font-family: 'Noto Sans Thai', 'Thonburi', sans-serif;
  font-weight: 800; color: #fff;
  text-shadow: 0 2px 8px #000;   /* legibility over busy Veo footage */
}
</style>
```

### 1c. Animated Thai caption block (drop-in) `[PROBED]` structure / `[UNVERIFIED]` exact look
```html
<div id="cap1" class="clip thai-cap"
     data-start="1" data-duration="2.5" data-track-index="3"
     style="position:absolute; bottom:520px; left:30px; right:30px;
            font-size:48px; text-align:center; line-height:1.4;">
  ร่มเปียก = ศัตรูหน้าฝน 🌧️
</div>

<script>
const tl = gsap.timeline({ paused: true });
// entrance
tl.from('#cap1', { opacity:0, y:50, duration:0.3 }, 1);
// HARD KILL at exit — prevents caption leaking onto the next one
tl.to('#cap1', { opacity:0, duration:0.3 }, 3.2);
tl.set('#cap1', { opacity:0, visibility:'hidden' }, 3.5);
window.__timelines['auto-affi-umbrella'] = tl;
</script>
```

### 1d. Word-level karaoke sync to VO `[PROBED]`
- `npx hyperframes transcribe <audio.mp3>` → word-level timestamps (VTT). Feed those times into either the `pill-karaoke` block (`data-start-word="<sec>"` per `<span>`) or hand-rolled GSAP tweens per word ID.
- `npx hyperframes tts "<thai text>"` → on-device Kokoro TTS (no API key) if you need a generated VO.

```js
// Hand-rolled karaoke from transcribe output
const words = [
  {id:'#w0', s:1.0, e:1.5}, {id:'#w1', s:1.6, e:2.1}, {id:'#w2', s:2.2, e:3.0}
];
words.forEach(w => {
  tl.to(w.id, { opacity:1, color:'#FF6B00', duration:0.15 }, w.s);
  tl.to(w.id, { opacity:0.5, color:'#fff', duration:0.15 }, w.e);
});
```

---

## 2. Lower-third / price / CTA / endcard blocks (JIAP DEALS · ฿335 · กดตะกร้าส้ม · #โฆษณา)

### 2a. Catalog lower-third `[PROBED]`
`npx hyperframes add lower-third` → 12 styles: `BILD`, `accent-underline`, `bold-block`, `clean-bar`, `color-block`, `dark-card`, `kicker-name`, `mask-reveal`, `side-rule`, `soft-pill`, `stack-bars`, `youtube-lower-third`. Plus social overlays: `instagram-follow`, `tiktok-follow`, `spotify-card`, `x-post-card`, `reddit-post`.

> ⚠️ `[UNVERIFIED]` There is **no named `cta-*` or `endcard-*` block** — probes returned 404 for those naming patterns. Build CTA + endcard as **custom clips** (below). This is the safe, doc-grounded approach.

### 2b. Combined lower-third price card + CTA (custom, drop-in) `[PROBED]` structure
```html
<!-- track-index 4: lower-third price+brand+CTA bar (own track so it can overlap captions on track 3) -->
<div id="lower-third" class="clip"
     data-start="2" data-duration="13" data-track-index="4"
     style="position:absolute; bottom:60px; left:0; right:0; height:120px;
            background:rgba(0,0,0,0.8); display:flex; align-items:center;
            justify-content:space-between; padding:0 30px;">
  <div style="font-size:48px; color:#fff; font-weight:900;
              font-family:'Noto Sans Thai';">JIAP DEALS</div>
  <div id="price-tag" style="font-size:56px; color:#ff6b35; font-weight:900;
              font-family:'Noto Sans Thai';">฿335</div>
  <div id="cta-btn" style="background:#ff8c42; padding:12px 28px; border-radius:8px;
              color:#fff; font-size:32px; font-weight:900;
              font-family:'Noto Sans Thai';">กดตะกร้าส้ม</div>
</div>

<!-- track-index 5: #โฆษณา disclosure (legal — keep it on screen, readable) -->
<div id="disclosure" class="clip thai-cap"
     data-start="0" data-duration="15" data-track-index="5"
     style="position:absolute; bottom:24px; right:20px; font-size:28px; color:#ddd;">
  #โฆษณา
</div>
```

```js
// entrance + life of the lower-third
tl.from('#lower-third', { y:200, opacity:0, duration:0.5 }, 2);      // slide up
tl.to('#price-tag', { scale:1.12, duration:0.3, yoyo:true, repeat:1 }, 2.4); // price pop
tl.to('#cta-btn',  { boxShadow:'0 0 30px rgba(255,140,66,0.9)',
                     duration:0.6, yoyo:true, repeat:-1 }, 2.6);     // CTA pulse
```

### 2c. CTA endcard (full-screen, custom) `[PROBED]` structure
```html
<div id="endcard" class="clip"
     data-start="13" data-duration="2" data-track-index="6"
     style="position:absolute; inset:0; display:flex; align-items:center;
            justify-content:center; background:rgba(0,0,0,0.72);">
  <div style="text-align:center; font-family:'Noto Sans Thai'; color:#fff;">
    <div style="font-size:64px; font-weight:900; margin-bottom:24px;">กดตะกร้าส้ม</div>
    <div style="font-size:40px; color:#ffd54a; font-weight:800;">฿335 · JIAP DEALS</div>
    <div style="font-size:28px; color:#bbb; margin-top:18px;">#โฆษณา</div>
  </div>
</div>
```
```js
tl.from('#endcard', { opacity:0, scale:0.96, duration:0.4 }, 13);
```

**Disclosure note (legal, not a HyperFrames claim):** `#โฆษณา` is kept persistent (full 15s, track 5) **and** repeated on the endcard. Verify placement/duration against current Thai ad-disclosure norms — this playbook only guarantees it *renders*.

---

## 3. The exact compose recipe (4 Veo MP4s → shaders → captions/lower-thirds → 1080×1920 MP4, local)

### Step 0 — Install `[PROBED]`
```bash
node -v          # need Node.js 22+
ffmpeg -version  # required (doctor auto-installs via Homebrew on first run)
npm install -g hyperframes        # or use: npx hyperframes <cmd>
npx hyperframes init jiap-umbrella-15s --example blank
cd jiap-umbrella-15s
npx hyperframes doctor            # checks Node + FFmpeg + Chrome
# optional caption blocks:
npx hyperframes add pill-karaoke
npx hyperframes add lower-third
# put the 4 Veo files in the project, e.g. ./clips/veo-01..04.mp4
# put NotoSansThai-Bold.ttf in ./fonts/
```

### Step 1 — Load the 4 Veo MP4s as scenes `[PROBED]`
Each Veo clip is a `<video class="clip" muted playsinline>` on **track 0**, chained with **relative timing** (built-in crossfade via overlap):
```html
<video id="scene-1" class="clip" data-start="0"            data-duration="4"
       data-track-index="0" muted playsinline src="./clips/veo-01.mp4"
       style="width:100%; height:100%; object-fit:cover;"></video>
<video id="scene-2" class="clip" data-start="scene-1 - 0.3" data-duration="4"
       data-track-index="0" muted playsinline src="./clips/veo-02.mp4"
       style="width:100%; height:100%; object-fit:cover;"></video>
<!-- scene-3, scene-4 same pattern -->
```
> Overlapping clips need **different tracks** if you want a true visual crossfade. For shader transitions (Step 2), the `init()` call drives the cut instead — keep them on track 0 and let the shader handle the boundary. `[PROBED]`

### Step 2 — Add shader transitions (from the in-repo doc) `[PROBED]`
Per `docs/reference/hyperframes-transitions.md`: keep most cuts HARD; use a shader only at 1–2 meaning moments. 14 valid shaders (`flash-through-white`, `whip-pan`, `chromatic-radial-split`, `light-leak`, `cinematic-zoom`, `domain-warp-dissolve`, `ripple-waves`, `sdf-iris`, `thermal-distortion`, `swirl-vortex`, `cross-warp-morph`, `gravitational-lens`, `ridged-burn`, `glitch`).
```js
import { init as initShaderTransitions } from '@hyperframes/shader-transitions';
initShaderTransitions({
  bgColor: '#0a0a0a',
  accentColor: '#FF8C42',                               // JIAP orange
  scenes: ['scene-1','scene-2','scene-3','scene-4'],
  transitions: [
    { time: 3.7,  shader: 'whip-pan',            duration: 0.4 }, // hook → demo
    // scene-2→3 = HARD CUT (omit) for demo continuity
    { time: 11.5, shader: 'flash-through-white', duration: 0.5 }, // demo → CTA hero reveal
  ],
});
```

### Step 3 — Layer captions + lower-thirds synced to VO `[PROBED]`
Add the §1c caption clips (track 3), §2b lower-third+CTA (track 4), disclosure (track 5), endcard (track 6), plus the VO audio track:
```html
<audio id="vo" class="clip" data-start="0" data-duration="15"
       data-track-index="-1" data-volume="0.85" src="./audio/vo-thai.wav"></audio>
```
Sync captions to VO via `npx hyperframes transcribe ./audio/vo-thai.wav` → use returned word times in the GSAP tweens (§1d). `[PROBED]`

### Step 4 — QA gates, then render to 1080×1920 MP4 `[PROBED]`
```bash
npx hyperframes lint index.html        # structural HTML errors
npx hyperframes validate index.html    # WCAG contrast (caption legibility)
# eyeball Thai shaping + price/CTA alignment at key beats:
npx hyperframes snapshot index.html --time 1.5  --output qa_cap.png
npx hyperframes snapshot index.html --time 11.6 --output qa_cta.png

# RENDER — 1080x1920, set in HTML root (data-width=1080 data-height=1920)
npx hyperframes render index.html \
  --output master_1080x1920.mp4 \
  --fps 30 --quality standard --format mp4 --docker

# verify the artifact
ffprobe -v error -show_entries stream=width,height -show_entries format=duration \
  -of default=noprint_wrappers=1 master_1080x1920.mp4
```
- `--quality`: `draft` (iterate) → `standard` (visually lossless 1080p, recommended) → `high`. `[PROBED]`
- `--docker` = deterministic fonts/Chrome across machines (recommended for Thai). `[PROBED]`
- For supersampled portrait you may use `--resolution portrait-4k` (2160×3840) then downscale — `[UNVERIFIED]` resolution-flag token names (`portrait-4k`) appear in only one probe; the **reliable** path is `data-width=1080 data-height=1920` in HTML root.

---

## 4. Ready-to-adapt skeleton — umbrella 15s short

Save as `index.html`. Self-contained except `./fonts/NotoSansThai-Bold.ttf`, `./clips/veo-0X.mp4`, `./audio/vo-thai.wav`. **Structure is `[PROBED]`; exact visual styling is design-tunable.**

```html
<!doctype html>
<meta charset="utf-8" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<style>
  body { margin:0; }
  @font-face { font-family:'Noto Sans Thai';
               src:url('./fonts/NotoSansThai-Bold.ttf') format('truetype'); font-weight:700; }
  .thai-cap { font-family:'Noto Sans Thai','Thonburi',sans-serif; font-weight:800;
              color:#fff; text-shadow:0 2px 8px #000; }
  [data-composition-id] { background:#000; overflow:hidden; }
</style>

<div id="root" data-composition-id="auto-affi-umbrella"
     data-width="1080" data-height="1920">

  <!-- 4 Veo scenes (track 0) -->
  <video id="scene-1" class="clip" data-start="0"            data-duration="4"
         data-track-index="0" muted playsinline src="./clips/veo-01.mp4"
         style="width:100%;height:100%;object-fit:cover;"></video>
  <video id="scene-2" class="clip" data-start="scene-1 - 0.3" data-duration="4"
         data-track-index="0" muted playsinline src="./clips/veo-02.mp4"
         style="width:100%;height:100%;object-fit:cover;"></video>
  <video id="scene-3" class="clip" data-start="scene-2 - 0.3" data-duration="4"
         data-track-index="0" muted playsinline src="./clips/veo-03.mp4"
         style="width:100%;height:100%;object-fit:cover;"></video>
  <video id="scene-4" class="clip" data-start="scene-3 - 0.3" data-duration="4"
         data-track-index="0" muted playsinline src="./clips/veo-04.mp4"
         style="width:100%;height:100%;object-fit:cover;"></video>

  <!-- VO (auto-muxed) -->
  <audio id="vo" class="clip" data-start="0" data-duration="15"
         data-track-index="-1" data-volume="0.85" src="./audio/vo-thai.wav"></audio>

  <!-- Animated Thai captions (track 3) -->
  <div id="cap1" class="clip thai-cap" data-start="1" data-duration="3" data-track-index="3"
       style="position:absolute;bottom:540px;left:30px;right:30px;font-size:48px;text-align:center;">
    ร่มเปียก = ศัตรูหน้าฝน 🌧️</div>
  <div id="cap2" class="clip thai-cap" data-start="4.5" data-duration="3.5" data-track-index="3"
       style="position:absolute;bottom:540px;left:30px;right:30px;font-size:48px;text-align:center;">
    ร่มกันพายุ + ปลอกกันน้ำ</div>

  <!-- Lower-third: brand + price + CTA (track 4) -->
  <div id="lower-third" class="clip" data-start="2" data-duration="11" data-track-index="4"
       style="position:absolute;bottom:60px;left:0;right:0;height:120px;background:rgba(0,0,0,0.8);
              display:flex;align-items:center;justify-content:space-between;padding:0 30px;">
    <div class="thai-cap" style="font-size:48px;font-weight:900;">JIAP DEALS</div>
    <div id="price-tag" class="thai-cap" style="font-size:56px;color:#ff6b35;font-weight:900;">฿335</div>
    <div id="cta-btn" class="thai-cap" style="background:#ff8c42;padding:12px 28px;border-radius:8px;font-size:32px;">กดตะกร้าส้ม</div>
  </div>

  <!-- Persistent disclosure (track 5) -->
  <div id="disclosure" class="clip thai-cap" data-start="0" data-duration="15" data-track-index="5"
       style="position:absolute;bottom:24px;right:20px;font-size:28px;color:#ddd;">#โฆษณา</div>

  <!-- Endcard (track 6) -->
  <div id="endcard" class="clip" data-start="13" data-duration="2" data-track-index="6"
       style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
              background:rgba(0,0,0,0.72);">
    <div class="thai-cap" style="text-align:center;">
      <div style="font-size:64px;font-weight:900;margin-bottom:24px;">กดตะกร้าส้ม</div>
      <div style="font-size:40px;color:#ffd54a;">฿335 · JIAP DEALS</div>
      <div style="font-size:28px;color:#bbb;margin-top:18px;">#โฆษณา</div>
    </div>
  </div>
</div>

<script type="module">
  import { init as initShaderTransitions } from '@hyperframes/shader-transitions';
  initShaderTransitions({
    bgColor:'#0a0a0a', accentColor:'#FF8C42',
    scenes:['scene-1','scene-2','scene-3','scene-4'],
    transitions:[
      { time:3.7,  shader:'whip-pan',            duration:0.4 },
      { time:11.5, shader:'flash-through-white', duration:0.5 },
    ],
  });
</script>
<script>
  const tl = gsap.timeline({ paused:true });

  // captions: entrance + hard-kill (no leak)
  tl.from('#cap1', {opacity:0,y:50,duration:0.3}, 1);
  tl.to('#cap1',   {opacity:0,duration:0.3}, 3.6);
  tl.set('#cap1',  {opacity:0,visibility:'hidden'}, 3.9);
  tl.from('#cap2', {opacity:0,y:50,duration:0.3}, 4.5);
  tl.to('#cap2',   {opacity:0,duration:0.3}, 7.6);
  tl.set('#cap2',  {opacity:0,visibility:'hidden'}, 7.9);

  // lower-third + price + CTA
  tl.from('#lower-third', {y:200,opacity:0,duration:0.5}, 2);
  tl.to('#price-tag',     {scale:1.12,duration:0.3,yoyo:true,repeat:1}, 2.4);
  tl.to('#cta-btn',       {boxShadow:'0 0 30px rgba(255,140,66,0.9)',duration:0.6,yoyo:true,repeat:-1}, 2.6);

  // endcard
  tl.from('#endcard', {opacity:0,scale:0.96,duration:0.4}, 13);

  // FORCE 15s composition length
  tl.set({}, {}, 15);

  window.__timelines['auto-affi-umbrella'] = tl;
</script>
```
> ⚠️ The shader-transitions `import` is an ES module (`@hyperframes/shader-transitions`). In a HyperFrames project init this resolves through the project's bundler/preview server. `[UNVERIFIED]` exact module-resolution in a bare `index.html` — run `npx hyperframes preview` (localhost:3002 hot-reload) to confirm it loads before rendering.

---

## 5. Honest gaps & fallbacks

| # | Gap | Status | Fallback |
|---|-----|--------|----------|
| G1 | Per-block doc pages (`pill-karaoke`, `kinetic-slam`, `neon-glow`, lower-third styles) | `[UNVERIFIED]` — **404** on probe. Only block *names* confirmed via `/llms.txt`. | Install the block, then `npx hyperframes snapshot` at its active time to see real output. Don't assume markup. |
| G2 | `cta-*` / `endcard-*` / `sticker` / `badge` named blocks | **Do not exist** `[PROBED 404]`. | Build CTA + endcard as custom clips (§2b/2c) — already done in skeleton. |
| G3 | Thai complex-script shaping (tone marks above/below, sara-am) | `[PROBED]` browser/Harfbuzz handles it; **no HyperFrames-native Thai shaping doc**. | (a) Embed `Noto Sans Thai` via `@font-face`, don't trust system fallback. (b) Render `--docker` for identical glyphs cross-machine. (c) **Snapshot-verify** stacked tone marks (`ปิ้`, `น้ำ`) before final render. If a specific block mangles Thai, fall back to a plain `<div class="clip">` caption — those are confirmed to shape Thai correctly. |
| G4 | `--resolution portrait-4k` token | `[UNVERIFIED]` — appears in 1 probe only. | Reliable path: set `data-width=1080 data-height=1920` in root + `--fps 30 --quality standard`. |
| G5 | `data-composition-duration` on root vs `tl.set({},{},15)` | Both forms appear `[PROBED]`, not reconciled. | Use **both** (root attr + `tl.set`) as belt-and-suspenders; the `tl.set` is the doc-consistent one. |
| G6 | `@hyperframes/shader-transitions` import in a bare HTML file | `[UNVERIFIED]` module resolution outside the project bundler. | Run `npx hyperframes preview` first; if the import fails, fall back to **declarative crossfade** (overlap clips on different tracks, no shader) — that's pure HTML, always works. |
| G7 | `#โฆษณา` legal placement/duration | Out of scope of probes (ad-law, not HyperFrames). | Kept persistent + on endcard; **human must confirm** against current Thai disclosure rules. |
| G8 | Render time / machine cost | `[PROBED]` ~5–8 min per 30s at `standard` on a mid-spec Mac; `high` >20 min. | Iterate at `--quality draft`; only render `standard`/`high` for the master. HyperFrames render is **local + free** (no API spend). |

**Verified vs produced:** Everything above is `[PROBED]` at the **documentation** level — the install/render commands, data-attributes, GSAP model, Thai-font approach, and 14-shader API are confirmed against probed HyperFrames docs. **Nothing here has been run** — no actual `npx hyperframes render` was executed and no MP4 was produced in this session. First action before trusting the skeleton: `npx hyperframes doctor` → `npx hyperframes preview` → `npx hyperframes snapshot` on the Thai captions (G3) → then `render`.

**Relevant repo files:** `/Users/phariyawit.jiap/Documents/Auto-Affi/docs/reference/hyperframes-transitions.md` (transition map this playbook reuses), `/Users/phariyawit.jiap/Documents/Auto-Affi/.aegis/brain/learnings/2026-06-28_hyperframes-transitions.md`.