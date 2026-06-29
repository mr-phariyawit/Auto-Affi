---
title: HyperFrames Capability Map (Auto-Affi post-production)
created: 2026-06-29
verified: |
  CLI VERIFIED LIVE on this machine (hyperframes v0.7.18):
  - `hyperframes doctor` PASS — M5, ffmpeg 8.1.1, Chrome headless-shell, Docker running, whisper-cpp present.
  - Kokoro TTS + MusicGen = optional, NOT installed (pip install kokoro-onnx / transformers torch).
  - `hyperframes catalog --json` = 132 items (authoritative list: docs/reference/hyperframes-catalog.json).
  Verified blocks for Auto-Affi: 15 caption-* (caption-highlight[tiktok], caption-pill-karaoke,
  caption-kinetic-slam, caption-emoji-pop, caption-neon-glow...), 10 lower-third (lt-soft-pill,
  lt-dark-card, lower-third-bild, news-ticker...), social (tiktok-follow...), 16 shader transitions +
  showcases, text-fx (morph-text, shimmer-sweep). NO dedicated cta/endcard/sticker block -> build custom.
status: research-level for per-block markup; CLI + catalog VERIFIED; no render run yet.
---

Note on the `probed:true` flags: that tag came from the upstream research, not from my own execution. I have NOT run any install or render command in this session, nor confirmed Thai font rendering. I'll mark anything I could verify from the feature corpus as `[PROBED]` (described consistently across the dataset) and anything I'm inferring or that has no evidence as `[UNVERIFIED]`.

Here is the capability map.

---

# Auto-Affi HyperFrames Capability Map

> Source: 80 researched HyperFrames features. **Honesty note:** every command below is transcribed from the research corpus, not executed in this session. `[PROBED]` = the feature/behavior is described consistently in the source data. `[UNVERIFIED]` = inferred, gap-filled, or has no execution evidence (especially Thai-rendering and timing claims). No render, install, or Thai-font test was actually run here.

---

## 1. Capability Map (by category)

### Transitions
| Block | What (one line) | Auto-Affi use |
|---|---|---|
| `@hyperframes/shader-transitions` | 14 WebGL cinematic transitions (domain-warp, whip-pan, sdf-iris, cinematic-zoom, chromatic-split, glitch, light-leak, flash-through-white, cross-warp-morph, etc.) `[PROBED]` | Scene-to-scene cuts between Veo clips: cinematic-zoom on product reveal, flash-through-white on price drop, light-leak for premium feel. ~400ms each. |
| `transitions-3d` | Perspective flip / rotate between clips `[PROBED]` | Rotate product 180° front→back between angle shots. |
| `transitions-blur` | Blur-in / blur-out scene blend `[PROBED]` | Soft, non-jarring move from wide shot to close-up detail. |
| `transitions-cover` | Directional cover/uncover slide reveals `[PROBED]` | Slide in "ส่งฟรี" / "ลดราคา" overlays over the product. |
| `transitions-destruction` | Shatter / fragmentation scene change `[PROBED]` | Price "breaks apart" to reveal discount; high-impact tease→reveal. |
| `transitions-dissolve` | Opacity cross-fade `[PROBED]` | Default soft cut between product and lifestyle footage. |
| `transitions-distortion` | Mesh warp / ripple morph `[PROBED]` | High-energy montage between product angles. |
| `transitions-grid` | Clip splits into animating grid tiles `[PROBED]` | Show 4-6 variants/angles at once, then resolve to next scene. |
| `transitions-light` | Lens flare / bloom / light-ray transition `[PROBED]` | Premium reveal for luxury/high-ticket items. |
| `transitions-mechanical` | Shutter / iris aperture transition `[PROBED]` | Precision/engineering signal for gadgets, appliances. |
| `transitions-push` | Directional push/slide `[PROBED]` | Product→testimonial, or push-down into price CTA. |
| `transitions-radial` | Circular/radial wipe from center/edge `[PROBED]` | Spotlight reveal of logo or price (UGC look). |
| `transitions-scale` | Zoom-in/out, scale morph `[PROBED]` | Scale thumbnail→fullscreen for product reveal. |
| `transitions-other` | Misc wipes/reveals collection `[PROBED]` | Hide jump-cuts when stitching 9:16 segments. |

### Captions
| Block | What | Auto-Affi use |
|---|---|---|
| `cli transcribe` (Whisper) | Audio/video → word-level timestamps; VTT/SRT/JSON; `--preserve-cues` `[PROBED]` | Veo Thai VO → SRT for burnt-in captions. **Thai accuracy [UNVERIFIED]** — corpus only shows `.en` models in examples (see Gaps). |
| `cli transcribe` (format convert) | VTT↔SRT↔JSON conversion `[PROBED]` | Re-encode existing caption files to WebVTT for burn-in. |
| Thai font support (`--font-dir`, `@font-face`) | Embed Prompt/Sarabun/Noto Sans Thai; burn into MP4 `[PROBED-claim]` / **render-correctness [UNVERIFIED]** | Baked Thai captions, no sidecar SRT needed. Kerning claim unverified. |

### Lower-thirds + Titles
> **Gap:** No dedicated "lower-third" or "title" block appears in the 80 features. Lower-thirds must be **composed manually** as HTML/CSS divs animated by GSAP via `@hyperframes/core` / `sdk.setText` / `setStyle` / `setTiming`. `[UNVERIFIED]` — no purpose-built block exists.

| Mechanism | What | Auto-Affi use |
|---|---|---|
| `sdk.setText` / `setStyle` / `setTiming` | Programmatic text/CSS/keyframe editing on any div `[PROBED]` | Build a lower-third div (product name + price), animate slide-in via setTiming. |
| `core` GSAP adapter (26+ easings) | Drives caption/title animation `[PROBED]` | Hand-authored title cards and lower-thirds. |
| `transitions-cover` | Slide-in overlay (closest pre-built lower-third proxy) `[PROBED]` | "ส่งฟรี" banner sliding over footage. |

### CTA + Endcard + Stickers
> **Gap:** No dedicated CTA / endcard / sticker block in the corpus. These are **composed manually** (HTML div + GSAP), using transition blocks for entrance. `[UNVERIFIED]` — no purpose-built block.

| Mechanism | What | Auto-Affi use |
|---|---|---|
| `sdk.setText` + `transitions-push`/`-scale` | Hand-built CTA card animated in `[PROBED for parts]` / endcard-block **[UNVERIFIED]** | Final 2-3s "กดลิงก์ใต้คลิป" CTA + price + Shopee logo. |
| `vfx-iphone-device` | 3D iPhone/MacBook mockup, live HTML on screen, turntable `[PROBED]` (needs Chrome flag `#canvas-draw-element`) | Endcard showing app UI on a spinning phone. |
| `code-*` reveal blocks | Sticker-like animated text/logo entrances `[PROBED]` | `code-particle-assemble` to assemble "Auto-Affi" logo as an intro sticker. |

### Audio
| Block | What | Auto-Affi use |
|---|---|---|
| `producer` audio mixing | Multi-track mix (VO + music + SFX), per-clip volume/pan, auto re-mux `[PROBED]` | VO 100% + brand music 40% fade-in + beat SFX, single MP4 out. |
| `cli tts` (Kokoro-82M, local) | Local TTS, voice presets, speed; claims Thai `[PROBED-claim]` / **Thai quality [UNVERIFIED]** | Generate Thai CTA/product-name callouts locally (no API latency). |
| `cli beats` / `render --beats` | Music beat detection `[PROBED]` | Snap captions/transitions to beat marks. |
| `engine muxVideoWithAudio` | Combine video+audio tracks via ffmpeg `[PROBED]` | Mux final VO+music+SFX into the export. |

### Effects + Motion
| Block | What | Auto-Affi use |
|---|---|---|
| `vfx-iphone-device` | Real GLTF iPhone 15 Pro Max / MacBook, live canvas screen, 360° `[PROBED]` (Chrome flag req.) | Demo app/software UI without filming hardware. |
| `code-3d-extrude` | Syntax code on lit 3D beveled slab `[PROBED]` | Tech-product intro (API/SDK snippet). |
| `code-shader-dissolve` / `code-particle-assemble` | GPU shader/particle code reveal `[PROBED]` | Dramatic climax/intro effect. |
| `core` GSAP adapter | 26+ easings, keyframe engine `[PROBED]` | All custom motion (captions, stickers, CTAs). |

### Text (animated typography / code)
> The corpus is **heavily code-snippet-weighted**: ~30 of 80 features are VS Code / macOS Terminal recreations and code-animation blocks. High value for dev-tool/SaaS shorts, low value for typical Shopee physical-product shorts.

| Block | What | Auto-Affi use |
|---|---|---|
| `code-typing` | Frame-accurate token typing w/ caret `[PROBED]` | Reveal commands/curl synced to VO. |
| `code-morph` (Shiki Magic Move) | Animate code "before→after" `[PROBED]` | "manual → one-liner" benefit framing. |
| `code-highlight` / `code-scroll` / `code-diff` | Spotlight line / scroll file / red-green diff `[PROBED]` | Feature-release reveals. |
| `code-snippet-apple-terminal-*` (13 themes: basic, clear-dark/light, grass, homebrew, man-page, novel, ocean, pro, red-sands, silver-aerogel, solid-colors) | macOS Terminal recreations, per-char typing, 12s `[PROBED]` | `brew install` / `curl api…` setup demos; theme = brand mood. |
| `code-snippet-dark-2026 / dark-modern / dark-plus / light-* / monokai / solarized-light / visual-studio-* / high-contrast*` (~14 VS Code themes) | Full VS Code workbench, typing, 3D tilt, 11s `[PROBED]` | Dev-tool/SaaS product demos. |
| `code-snippet-flight` | Code blocks FLIP-assemble `[PROBED]` | Tech-stack reveal. |

### Data / Charts
> **Gap:** No chart, graph, or data-viz block exists in the 80 features. `--variables` JSON is data-*injection* (text/price swaps), not visualization. `[UNVERIFIED]` — no chart capability found.

| Mechanism | What | Auto-Affi use |
|---|---|---|
| Data-driven templates (`--variables` / `lambda render-batch users.jsonl`) | Placeholder substitution at render time `[PROBED]` | 1 template → 100 personalized shorts (ASIN, price, review count). |
| `sdk.setVariableValue` | Programmatic data-binding `[PROBED]` | Bind product fields before render. |

### Engine + Timeline
| Block | What | Auto-Affi use |
|---|---|---|
| `@hyperframes/core` | HTML↔composition parse/generate, validate, GSAP adapter, runtime IIFE `[PROBED]` | Parse Veo+captions into objects, generate GSAP keyframes. |
| `@hyperframes/parsers` | Dep-free HTML/GSAP(AST)/manifest parsing, `ensureHfIds`, spring-ease `[PROBED]` | Inject captions/CTAs into clip tracks; stable diffs. |
| `@hyperframes/engine` | Seekable `BeginFrame` capture, media frame extraction, browser mgmt, encoding (`detectGpuEncoder`, `applyFaststart`, `muxVideoWithAudio`), `window.__hf.seek` `[PROBED]` | Deterministic frame-by-frame render; GPU encode; faststart MP4. |
| `@hyperframes/sdk` | `openComposition`, set Text/Style/Timing/Variable, find/serialize, patch events, undo/redo, FS/headless/iframe adapters `[PROBED]` | Programmatic build/edit of the whole short. |
| `@hyperframes/lint` | Detect unmuted video, missing clip class, deprecated attrs, bad `data-start`; `shouldBlockRender()` `[PROBED]` | Pre-render gate (unmuted Veo audio = blocker). |
| `@hyperframes/studio` + `studio-server` | Browser NLE: timeline, scrub, element picker, hot reload `[PROBED]` (React 18-19, Zustand peer deps) | Visual editing of clip/caption/CTA positions. |
| `@hyperframes/cli` | init/add/catalog/preview/lint/inspect/snapshot/publish/render/benchmark/beats/doctor `[PROBED]` | Whole local workflow. |
| `@hyperframes/player` | 3KB `<hyperframes-player>` web component `[PROBED]` | Embed autoplay+loop+muted short on product pages. |

### Export / Render
| Block | What | Auto-Affi use |
|---|---|---|
| `cli render` / `producer` | HTML→MP4/WebM/MOV/PNG-seq; fps 24/30/60; draft/standard/high; workers 1-8; GPU; Docker deterministic `[PROBED]` | Local 1080×1920 30fps MP4; `--workers 4`. |
| `producer` HTTP server | `POST /render`, SSE `/render/stream`, `/lint`, `/outputs/:token` `[PROBED]` | Render API + live progress to a backend. |
| HDR (`producer` / `engine`) | BT.2020/PQ/HLG detect, 10-bit H.265, HDR10 metadata `[PROBED]` | Future premium HDR campaigns. |
| `cli cloud render` (HeyGen) | Cloud render, 1080p/4k, async `--callback-url`, `--no-wait` `[PROBED]` | No-local-GPU rendering. |
| `@hyperframes/aws-lambda` | Step Functions chunked parallel render, S3 assembly `[PROBED]`; "~4min→~45s" timing **[UNVERIFIED]** | 100-variant batches; claimed speedup unproven. |
| `@hyperframes/gcp-cloud-run` | Cloud Workflows plan→render→assemble, GCS, scale-to-zero `[PROBED]` | Cost/region arbitrage; Thailand CDN delivery. |
| `cli remove-background` | Subject extract → transparent WebM `[PROBED]` | Cut product out before compositing. |
| `cli capture` | Screenshot website → JSON `[PROBED]` | Capture Shopee storefront for swaps. |

---

## 2. Top 15 features for 15s Thai Shopee shorts (ranked)

Ranked by value to a short-form, vertical, Thai, fast-turnaround, batch-personalized workflow.

1. **`cli render` / `producer` (local 1080×1920 MP4, GPU, workers)** `[PROBED]` — the core deliverable. Nothing ships without it.
2. **`@hyperframes/sdk` (programmatic compose: setText/setTiming/setVariable)** `[PROBED]` — lets Auto-Affi *generate* shorts in code, not hand-edit. This is what makes it an automation platform.
3. **Data-driven templates + `lambda render-batch users.jsonl`** `[PROBED]` — 1 template → N personalized shorts (ASIN/price/reviews). Core scaling lever.
4. **`@hyperframes/shader-transitions` (14 cinematic)** `[PROBED]` — biggest production-polish-per-effort; cinematic-zoom/flash-through-white/light-leak fit price-reveal beats.
5. **`producer` audio mixing (VO + music + SFX)** `[PROBED]` — one-pass VO+music balance, no separate DAW step.
6. **Thai font support (burnt-in captions)** `[PROBED-claim, render [UNVERIFIED]]` — captions are mandatory for muted-autoplay Thai feeds; **must be Thai-render-tested before trusting.**
7. **`@hyperframes/lint` / `shouldBlockRender`** `[PROBED]` — catches unmuted Veo audio (auto-fail) before wasting a render. Cheap insurance at batch scale.
8. **`cli tts` Kokoro Thai (local)** `[PROBED-claim, Thai quality [UNVERIFIED]]` — local Thai VO with no API latency; **audition Thai output first.**
9. **`cli transcribe` → SRT** `[PROBED, Thai accuracy [UNVERIFIED]]` — auto-captions from Veo VO; verify Thai model support.
10. **`cli beats` (beat-sync)** `[PROBED]` — snap caption/transition timing to music; the "feels professional" multiplier in 15s.
11. **`@hyperframes/engine` deterministic capture (`window.__hf.seek`)** `[PROBED]` — reproducible renders = safe batch automation.
12. **`@hyperframes/player` (3KB embed)** `[PROBED]` — autoplay+loop+muted short directly on Shopee product pages.
13. **`cli preview` + `inspect`/`snapshot`** `[PROBED]` — review beat-sync points before committing GPU time.
14. **`transitions-scale` / `transitions-radial`** `[PROBED]` — cheap, mobile-readable product-reveal and spotlight moves for 9:16.
15. **`cli remove-background`** `[PROBED]` — clean product cutouts for compositing over lifestyle/branded backgrounds.

*Deliberately excluded from top 15:* the ~30 code-snippet/terminal/VS-Code blocks — high quality but a poor fit for typical physical-product Shopee shorts (relevant only when the *product itself* is a dev tool/SaaS).

---

## 3. Complete COMPOSE recipe (Veo mp4 → final 1080×1920 MP4, local)

> All commands transcribed from the corpus. **[UNVERIFIED]** end-to-end — this exact pipeline was not executed in this session. Treat as a starting script to test, not a proven runbook. Where the corpus lacks a real block (lower-thirds, CTA endcard) the step is hand-authored HTML/GSAP.

```bash
# --- 0. Install ---
npm install -g hyperframes            # or use: npx hyperframes <cmd>
npx hyperframes doctor --json         # check Chrome, fonts, deps  [PROBED]

# --- 1. Scaffold a vertical project ---
npx hyperframes init umbrella-short --example blank --video scene1.mp4
# Set composition dims to 1080x1920 (vertical) in the generated HTML  [PROBED]

# --- 2. Add transitions between Veo scenes ---
npx hyperframes add shader-transitions     # 14 WebGL cuts  [PROBED]
npx hyperframes add transitions-scale      # product reveal
npx hyperframes add transitions-radial     # price spotlight

# --- 3. Captions: Veo Thai VO -> SRT (verify Thai model!) ---
npx hyperframes transcribe vo.wav --language th --to srt --output captions.srt
#   ^ Thai accuracy [UNVERIFIED] — confirm a Thai Whisper model is available

# --- 4. (Optional) Thai TTS for CTA callout (local Kokoro) ---
npx hyperframes tts 'กดลิงก์ใต้คลิปเลย' --lang th --speed 0.95 --output cta.wav
#   ^ Thai quality [UNVERIFIED] — audition before use

# --- 5. Beat detection for timing ---
npx hyperframes beats ./audio     # snap captions/transitions to beats  [PROBED]

# --- 6. Lower-thirds + CTA endcard: HAND-AUTHORED (no block exists) ---
#   Add <div class="lower-third">{{product}} · {{price}}</div> animated via GSAP,
#   and a final <div class="cta">…</div>. Use SDK or edit HTML directly.

# --- 7. Lint before render (catch unmuted Veo audio) ---
npx hyperframes lint --json       # shouldBlockRender gate  [PROBED]

# --- 8. Preview / snapshot beat-sync points ---
npx hyperframes preview --port 4567
npx hyperframes snapshot --at 2.9,7.4,12.5 --frames 10   # review keyframes

# --- 9. Render final vertical MP4 (audio auto-mixed + muxed) ---
npx hyperframes render \
  --output umbrella-short.mp4 \
  --format mp4 --fps 30 --quality high \
  --workers 4 --gpu \
  --variables '{"product":"ร่มกันยูวี","price":"199"}'
#   producer auto-extracts/mixes <video>+<audio> and applies faststart  [PROBED]
```

SDK-driven alternative for batch automation (instead of steps 6-9):

```js
import { openComposition } from '@hyperframes/sdk';
import { createRenderJob, executeRenderJob } from '@hyperframes/producer';

const comp = openComposition(html);
comp.setText('caption', 'ร่มกันยูวี กันได้ 99%');
comp.setText('price', '฿199');
comp.setTiming('clip-2', { start: 5, duration: 5 });
await comp.flush();

const job = createRenderJob({ fps: 30, quality: 'high', format: 'mp4', workers: 4, useGpu: true });
const result = await executeRenderJob(job, comp.serialize());   // [PROBED API shapes, run [UNVERIFIED]]
```

---

## 4. Ready-to-adapt skeleton: umbrella 15s short

> Composition shell (1080×1920, 15s). Timing is a **suggested beat layout, [UNVERIFIED]**. Lower-third and CTA are hand-authored divs because no block exists. `data-start`/`data-duration` follow the corpus's documented attribute convention `[PROBED]`.

```html
<!-- umbrella-short.html  | 1080x1920 | 15s -->
<div class="composition" data-width="1080" data-height="1920" data-duration="15">

  <!-- TRACK 0: Veo scenes -->
  <video class="clip" src="veo_hook.mp4"     data-start="0"  data-duration="4"  muted></video>
  <video class="clip" src="veo_rain.mp4"     data-start="4"  data-duration="4"  muted></video>
  <video class="clip" src="veo_lifestyle.mp4" data-start="8" data-duration="4.5" muted></video>

  <!-- TRACK 1: transitions at cut points -->
  <div data-composition-id="shader-transitions"
       data-composition-src="compositions/shader-transitions.html"
       data-start="0" data-duration="15" data-track-index="1"
       data-width="1080" data-height="1920"></div>
  <!-- config: cinematic-zoom @4s, flash-through-white @8s, light-leak @12s -->

  <!-- TRACK 2: Thai captions (burnt-in, Prompt font) -->
  <style>
    @font-face { font-family:'Prompt'; src:url('Prompt-Bold.ttf'); }
    .caption{ font-family:'Prompt'; font-weight:700; font-size:56px; color:#fff;
              text-shadow:0 2px 8px rgba(0,0,0,.6); position:absolute; bottom:340px; }
    .lower-third{ font-family:'Prompt'; position:absolute; bottom:200px; left:48px;
                  background:rgba(0,0,0,.55); padding:16px 28px; border-radius:14px; color:#fff; }
    .cta{ font-family:'Prompt'; font-weight:700; position:absolute; inset:0;
          display:flex; flex-direction:column; align-items:center; justify-content:center;
          background:#ee4d2d; color:#fff; opacity:0; } /* Shopee orange */
  </style>
  <div class="caption" id="cap1">ฝนตกไม่ต้องเปียก ☔</div>

  <!-- TRACK 3: lower-third (hand-authored) -->
  <div class="lower-third" id="lt"><b>{{product}}</b><br>กันยูวี 99% · พับเก็บง่าย</div>

  <!-- TRACK 4: CTA endcard 12s–15s (hand-authored) -->
  <div class="cta" id="endcard">
    <div style="font-size:72px">{{price}}.-</div>
    <div style="font-size:44px">กดลิงก์ใต้คลิป 🛒</div>
  </div>

  <!-- AUDIO -->
  <audio src="vo.wav"    data-volume="1.0" data-start="0"></audio>
  <audio src="music.mp3" data-volume="0.4" data-start="0"></audio>
  <audio src="cta.wav"   data-volume="1.0" data-start="12"></audio>

  <!-- TIMELINE: GSAP drives caption/lower-third/CTA + window.__hf.seek bridge -->
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    const tl = gsap.timeline({ paused:true });
    tl.from('#cap1',     { opacity:0, y:40, duration:.4 }, 0.3)
      .from('#lt',       { opacity:0, x:-60, duration:.5 }, 4.2)
      .to('#endcard',    { opacity:1, duration:.4 }, 12.0);
    window.__hf = { seek(t){ tl.time(t); } };   // engine calls this per frame  [PROBED API]
  </script>
</div>
```

Render: `npx hyperframes render --output umbrella-short.mp4 --format mp4 --fps 30 --quality high --workers 4 --gpu --variables '{"product":"ร่มกันยูวี Auto","price":"199"}'`

---

## 5. Honest gaps / UNVERIFIED / Thai concerns

**Hard capability gaps (no block exists in the 80 features):**
- **Lower-thirds / titles** — no dedicated block. Must hand-author HTML+GSAP. `[UNVERIFIED — gap]`
- **CTA / endcard / stickers** — no dedicated block. Hand-authored; `transitions-cover`/`-push` only provide the entrance animation. `[UNVERIFIED — gap]`
- **Data/charts** — **zero** charting/graph/data-viz blocks. `--variables` is text substitution, not visualization. If a short needs an animated bar/price-graph, it must be built from scratch. `[UNVERIFIED — gap]`

**Thai-support concerns (highest risk — none render-tested here):**
- **Whisper Thai transcription** `[UNVERIFIED]` — every transcribe model example in the corpus is English (`tiny.en`/`medium.en`). Thai support is claimed via `--language` but no Thai example or accuracy evidence exists. **Test before relying on auto-captions.**
- **Kokoro Thai TTS** `[UNVERIFIED]` — "Thai/EN" is asserted; Kokoro-82M Thai voice quality and naturalness are not demonstrated in the data. Audition required.
- **Thai font rendering / kerning** `[UNVERIFIED]` — `--font-dir` + `@font-face` Prompt/Sarabun is claimed, and "GSAP animates Thai kerning correctly" is asserted but unproven. Thai has complex glyph stacking (vowels/tone marks above/below); headless-Chrome render must be **snapshot-inspected at the pixel level** before trusting burnt-in captions.

**Performance / claim caveats:**
- Lambda "~4min→~45s" and the "16 parallel workers" speedup are **[UNVERIFIED]** marketing-style numbers, not benchmarks in the data.
- `vfx-iphone-device` requires a **non-default Chrome flag** (`#canvas-draw-element`); may not render in standard headless render. `[PROBED requirement, render [UNVERIFIED]]`
- `studio` needs React 18-19 + Zustand peer deps — integration cost, not a drop-in. `[PROBED]`
- Code-snippet blocks default to **1920×1080**; using them in 1080×1920 requires overriding `data-width`/`data-height` (some docs note this, some don't). `[PROBED with caveat]`

**Corpus bias:** ~30 of 80 features are code/terminal/IDE recreations — excellent for dev-tool/SaaS promos but largely irrelevant to physical-product Shopee shorts. The genuinely Shopee-relevant surface is roughly the engine/render/transitions/audio/caption core (~25 features), not the full 80.

**Meta-honesty:** the upstream `probed:true` flags are the researcher's, not mine. I executed nothing in this session. The single biggest unproven risk for Auto-Affi is **Thai text correctness across transcribe → TTS → burnt-in font render** — that chain needs a real render + pixel-level Thai snapshot inspection before any production batch.

---

**You are here:** Capability map delivered (10 categories, top-15 ranking, compose recipe, umbrella skeleton, gaps). Next concrete action to de-risk: run `npx hyperframes doctor` + a single Thai-caption test render and `snapshot --at` to pixel-verify Thai glyph stacking before building the batch pipeline.