# HyperFrames Packages & Guides — Reference for Auto-Affi

**Last reviewed:** 2026-07-06 · **HF version:** v0.7.37 · **Scope:** all **13 packages + 26 guides** (39 docs pages, ~9,500 lines) from `hyperframes.heygen.com/{packages,guides}/*`, studied from their **real markdown** via a 40-agent workflow, scored against the Auto-Affi Thai Shopee offline-render pipeline.

**Provenance / honesty:** Page list `[VERIFIED]` from `llms.txt`. Content and every command/flag/limit below is **doc-sourced** (agents read the official `.md`), not personally re-run per claim — treat exact flags as "what the docs state," verify before relying in code. The pipeline mapping (§4) was cross-checked against [gold-standard-ad-recipe.md](gold-standard-ad-recipe.md). Companion doc: [hyperframes-components.md](hyperframes-components.md) (the 25 caption/effect components).

> **Our pipeline:** Gemini/Veo footage → HyperFrames composes the master **offline** (chrome-headless-shell via the **CLI**, vendored GSAP/no-CDN, pythainlp Thai word-karaoke from an STT `{text,start,end}` array, producer auto-mixes Thai VO + ducked BGM) → MP4. We drive HF through the **CLI only**; we do not import the JS packages.

---

## 1. Page inventory — relevance to Auto-Affi (0–5)

| Rel | Page | Type | One-line takeaway |
|:--:|---|---|---|
| **5** | `packages/cli` | pkg | THE interface we use — `render/add/catalog/transcribe/inspect/lint/doctor` + all flags |
| **5** | `guides/rendering` | guide | `--docker` (deterministic), `--batch`, formats, `--strict-variables` |
| **4** | `guides/authentication` | guide | **silent** local TTS/BGM fallback when no key → preflight `auth status --json` |
| **4** | `guides/common-mistakes` | guide | the exact bugs that silently break a master (see §3) |
| **4** | `guides/gsap-animation` | guide | timeline length = last tween; never animate `<video>` |
| **4** | `packages/lint` | pkg | structural pre-render gate as a Node lib (`lintProject`) |
| **4** | `guides/remove-background` | guide | optional JIAP matting over a product plate |
| **4** | `guides/troubleshooting` | guide | font-reflow → caption drift; lint before render |
| 3 | `guides/performance` | guide | source images decode to `w×h×4` RGBA — downsize first |
| 3 | `guides/pipeline` | guide | official 7-step; `narration.txt` separation |
| 3 | `packages/producer` | pkg | engine under `render`; `ProgressCallback` if we go programmatic |
| 3 | `guides/prompting` | guide | 7 determinism rules (no `Math.random()`/`Date.now()`) |
| 3 | `guides/video-components` | guide | `hyperframes add` the catalog (captions/blocks) |
| 2 | `packages/core` · `engine` · `sdk` · `shader-transitions` | pkg | don't import (see §5); engine loses audio auto-mix |
| 2 | `guides/hyperframes-vs-remotion` · `skills` · `video-editor-cheatsheet` · `website-to-video` · `feedback` | guide | BeginFrame determinism; skills to install; snapshot gate |
| 1 | `guides/4k-rendering` · `antigravity` · `claude-design` · `copilot-cli` · `deploy` · `html-in-canvas` · `keyframes` · `open-design` · `timeline-editing` | guide | interactive/GUI/scale — out of scope (§5) |
| 1 | `packages/parsers` · `player` · `studio` · `studio-server` | pkg | GUI/embed/transitive — don't install |
| 0 | `packages/aws-lambda` · `gcp-cloud-run` · `guides/figma` · `guides/hdr` | both | cloud fan-out / Figma / HDR — irrelevant |

---

## 2. ADOPT NOW — concrete changes (ordered by impact)

**A. Add `npx hyperframes inspect` as a pre-render gate.** `[cli, troubleshooting]` — `inspect` (formerly `layout`) headlessly seeks the timeline and reports `text_box_overflow` / `content_overlap` / `text_occluded` — exactly the Thai-caption failure mode (Thai runs longer than English → wraps → overflows 9:16). Run at your beats:
```bash
npx hyperframes inspect --at <hook>,<feature>,<cta> --json    # --tolerance 2px, --samples 9
```
False positives: escape with `data-layout-allow-overflow` / `data-layout-ignore`. Cheaper than finding overflow after a full render.

**B. Add `npx hyperframes lint` as a hard fail-fast before every render.** `[lint, common-mistakes]` — catches the silent master-breakers: a timed caption missing `class="clip"` (renders it for the *whole* video, ignoring `{start,end}`), an **unmuted `<video>`** (headless autoplay fails → clip silently drops; producer needs videos muted to auto-mix anyway), missing `data-width/height`, `data-start` → nonexistent clip id, deprecated `data-layer/data-end`. Wire into the Python orchestrator; a structural error stops the run before render spend.

**C. `npx hyperframes auth status --json` preflight.** `[authentication]` — HF TTS/music **silently falls back to local Kokoro/MusicGen when no key is set (no error).** We supply pre-rendered VO/BGM so it rarely fires, but assert `configured`/`offline_engines` so any run that *would* fall back fails loud. Also set `HYPERFRAMES_NO_TELEMETRY=1` in the subprocess env.

**D. `--docker` for the final Thai-font master.** `[rendering, troubleshooting]` — local mode "may vary across platforms due to font and Chrome version differences." For Thai this is critical: a font/Chrome diff causes **text reflow → word-karaoke `{start,end}` mis-aligns.** `--docker` pins Chrome+fonts+FFmpeg (deterministic BeginFrame path). Use for masters; local for iteration. (`--docker` disables `--gpu` — acceptable trade.)

**E. `--strict-variables` + `--batch rows.json` for per-product variants.** `[rendering, cli]`
```bash
npx hyperframes render --batch rows.json --output "renders/{name}.mp4" --strict-variables
```
Writes `manifest.json` (per-row status/time/errors); continues past failures unless `--batch-fail-fast`. **Caveat (§3 #6): total render *length* is NOT variable-drivable — only clip durations/media trims. Length variants need separate HTML.**

**F. Source-image guardrail — free memory/perf.** `[performance]` — Chrome decodes every image to raw RGBA (`w×h×4` bytes) regardless of file size (a 7000×5000 JPEG = 140 MB decoded). Downsize Gemini stills / PNG overlays to ≤2× the 1080×1920 canvas before feeding HF: `mogrify -path resized -resize 3840x3840\> *.jpg` — zero visual loss.

**G. Import STT transcript instead of re-running whisper (optional).** `[cli]` — `npx hyperframes transcribe` normalizes whisper.cpp / OpenAI-Whisper JSON / SRT / VTT into the same `[{text,start,end}]` array + auto-patches caption HTML. Pass **`--preserve-cues`** (one cue per entry — for single-word/CJK captions with no internal spaces = **exactly our pythainlp Thai word cues**). Only if it saves duplicate alignment work.

**H. Get timeout/memory units right.** `[cli]` — `--browser-timeout` is in **SECONDS** but its env fallback `PRODUCER_PAGE_NAVIGATION_TIMEOUT_MS` is **MILLISECONDS** (1000× footgun). `--low-memory-mode` auto-engages ≤8 GB from **host** `os.totalmem()` (not cgroup) — in a container set `PRODUCER_LOW_MEMORY_MODE` explicitly.

---

## 3. PITFALLS to encode (mistake → fix)

| # | Mistake | Fix |
|:--:|---|---|
| 1 ✅ | **Video cut off early** — composition duration = the GSAP timeline's last tween, NOT the video's `data-duration`. A Veo clip longer than your last caption tween silently truncates. | End the paused timeline with `tl.set({}, {}, TOTAL_VO_SECONDS)` (zero-dur pad). Verify with `npx hyperframes compositions`. |
| 2 ✅ | **Caption renders whole video**, ignoring `{start,end}` — timed element missing `class="clip"`. | Every karaoke word / overlay: `class="clip"` + `data-start` + `data-duration` + `data-track-index`. Lint catches it. |
| 3 | **Animating a `<video>` breaks frame rendering** — animating `width/height/top/left/visibility` on a `<video>` makes Chrome stop updating its frames. | Wrap the video in a non-timed `<div>`, animate the wrapper, video fills `100%`. (This is *why* our recipe says "never animate a `<video>`.") |
| 4 | **Scripts controlling media desync the mix** — `video.play()`/`.pause()`/`audio.currentTime` in composition JS fights the producer (which owns playback + VO-over-BGM ducking via `data-start/data-media-start/data-volume`). | GSAP for visual props only (opacity/x/y/scale/color). Never touch media playback in scripts. |
| 5 | **`Math.random()` / `Date.now()` break determinism** — different frames per render, invisible until frames disagree. | Seeded PRNG (mulberry32) only. Never emit `Math.random()`/`Date.now()` in compositions. |
| 6 | **Total render length is NOT variable-drivable** — root `data-duration` read once at compile; later `--variables`/`setAttribute` ignored (clip durations & media trims *are* re-read). | Different ad lengths = separate HTML variant. |
| 7 | **Thai font missing → reflow → caption timing drifts.** | Vendor Noto Sans Thai via `@font-face` (recipe does this) **AND** `--docker` for the master. |
| 8 | **Silent capture-mode fallback** — an inline `<iframe>` or raw `requestAnimationFrame` loop (outside a Frame Adapter) drops HF from deterministic BeginFrame to real-time Screenshot mode (wall-clock racing). | Keep caption/overlay HTML free of inline iframes / stray rAF. Watch the render diagnostic for a fallback notice. |
| 9 | **Stacked `backdrop-filter: blur()` blows the frame budget** (glass overlays, large radii). | ≤2–3 blur layers per region; for static blur, pre-render to PNG and overlay as `<img>`. |
| 10 | **`doctor --json` exits 0 even when unhealthy** — health is in the payload. | Gate on `jq -e '.ok'`, not exit status. |
| 11 | **`feedback --file-issue` / `publish` upload the project publicly** — would leak unreleased client Shopee assets. | Never run them on a client ad project. |

---

## 4. HF's 7-step pipeline vs our gold-standard

Official: **capture → design → strategy → storyboard+script → voiceover+timing → build → validate** `[pipeline]`.

| HF step | Our equivalent | Verdict |
|---|---|---|
| 1. Capture (scrape a website) | **Generate footage** (Nano Banana Pro sheets → Veo i2v) | ✅ Fully replaced — we're generative-first, no website |
| 2. Design (`DESIGN.md`, brand tokens) | Cast + product char-sheets (identity locks) | ✅ Our locks are stronger for a recurring protagonist |
| 3. Strategy | Implicit in the beat plan | ✅ Fine at our scale |
| 4. Storyboard + script | Per-beat shots + Thai script | ✅ Aligned |
| 5. Voiceover + timing → `transcript.json` `[{text,start,end}]` | ElevenLabs VO → STT → our karaoke array | ✅ **Exact data-contract match** — HF's `transcript.json` *is* our STT array |
| 6. Build (one HTML/beat, `window.__timelines`) | HF compose (paused timeline, `class="clip"`) | ✅ Aligned |
| 7. Validate (`lint`→`inspect`→`snapshot`→`render`) | Cleanroom PASS + eyeball | ⚠️ **Biggest gap — adopt §2 A+B+D** |

**Net:** steps 4–6 already congruent; step 5's contract is a perfect match. The one real gap is **Step 7 rigor** — we eyeball where HF gives free structural gates. Keep our **adversarial Asset-QC gate** (anatomy/grooming/identity/label before Veo) — HF has no equivalent (it doesn't do generative footage). Optionally adopt HF's **`narration.txt`** discipline: keep exact-spoken-text (with Thai pronunciation substitutions like คว่ำ→พลิกกลับ baked in) separate from the script, so re-running VO with a new voice doesn't require redoing substitutions.

---

## 5. Packages — import any programmatically? **Verdict: stay on the CLI.**

Nearly every package page opens by telling single-machine users to use the CLI/producer. Import nothing today.

| Package | Import? | Reason |
|---|---|---|
| `@hyperframes/lint` | **Maybe — the only candidate** | `lintProject('./dir')` returns structured findings (`code/message/fixHint/selector`) vs scraping stdout. Adopt only if stdout-parsing gets brittle. Caveat: `shouldBlockRender`'s first two booleans are undocumented — with `false,false` only errors block (unmuted-video/missing-clip may pass as warnings). |
| `@hyperframes/producer` | No, unless you want structured progress | Engine under `render`; config maps 1:1 to CLI flags. Only reason: a `ProgressCallback` (queued→rendering→encoding→complete). Not worth it for one-shot renders. |
| `@hyperframes/engine` | **No** | Page warns "most users should NOT use the engine directly." Dropping to it **loses the producer's audio auto-mix** (our VO+ducked-BGM) + caption injection. |
| `@hyperframes/sdk` | No now | An *editing* engine, not a renderer. Its Embedded Override Mode (`openComposition(templateHtml,{overrides})`) fits a future reusable-JIAP-template, but adds no render/caption/audio capability. Revisit if we templatize. |
| `@hyperframes/core` · `parsers` | No | Foundation types/parsers; linter already reachable via `npx hyperframes lint`. Installing `parsers` separately risks version drift vs the CLI's bundled copy. |
| `@hyperframes/player` | No | 3 KB browser playback widget — irrelevant to headless MP4. Only for an internal preview dashboard. |

**Bottom line:** CLI is the supported layer for single-machine offline render. If stdout parsing ever bites, `@hyperframes/lint` is the one clean, low-risk upgrade.

---

## 6. Out of scope (ignore + why)

- **`aws-lambda` / `gcp-cloud-run`** — distributed cloud fan-out (S3/Step Functions, GCS/Workflows) for splitting huge renders; we render one short clip locally. If we ever need batch throughput, run N independent local CLI renders instead.
- **4K rendering** — supersampling to 3840×2160 = 4× time/cost for a 1080×1920 ad; `<video>`/`<canvas>` don't even benefit (locked to source res).
- **HDR** — only engages on BT.2020 PQ/HLG sources; Veo/Gemini is SDR bt709 → never fires. Don't pass `--hdr`.
- **Website-to-video / capture** — scrapes a URL for assets; we generate footage.
- **Figma import** — needs `FIGMA_TOKEN` + a Figma source we don't have.
- **Studio / studio-server / timeline-editing / keyframes / claude-design / open-design / antigravity / copilot-cli** — interactive human-in-browser authoring; we're headless + Python-driven. (Useful mental model: preview stutter ≠ bad render — render is seek-driven per-frame.)
- **Deploy templates (Vercel/Cloudflare)** — hosted `/api/render` behind a preview UI; we render offline.
- **Shader-transitions / html-in-canvas** — WebGL/3D polish; revisit only for a specific effect (≤2 shader transitions/video).
- **`remove-background`** — *usable later*: one offline command to matte JIAP over a separate product plate (human-only model — **cannot** cut the product itself). Optional pre-process, not in the current recipe.

---

## Related
- [gold-standard-ad-recipe.md](gold-standard-ad-recipe.md) — §4 maps onto its steps; §2's lint/inspect/docker/auth gates are the concrete additions to its "Compose" + "Non-negotiables"
- [hyperframes-components.md](hyperframes-components.md) — the 25 caption/effect components + 5 Thai-safety rules
- Memory: `project-hyperframes-compose`, `reference-hyperframes-components`
