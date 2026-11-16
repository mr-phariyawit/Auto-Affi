# Toolchain options for a code-generated maths/physics simulation short (TikTok 1080x1920, "How many clacks?")

Research date: 2026-11-13. Version/date facts marked **[API]** come from the public GitHub REST API (`api.github.com/repos/<repo>` and `/releases/latest`) queried on 2026-11-13. Anything labelled **unverified** was not confirmed from a primary source in this session. Nothing here was test-rendered: every technique note is PRODUCED advice, not VERIFIED on this machine.

## 1. Tool comparison (Manim CE vs ManimGL, Remotion, Motion Canvas, HyperFrames, Canvas/p5 + headless capture, Python + ffmpeg, Processing, Godot/Unity)

### Takeaway
Every candidate can output 1080x1920; the real differentiators are (a) whether the renderer is seek-based/deterministic by design, (b) audio handling, (c) licence, and (d) how much new tooling the creator must learn. HyperFrames (Apache-2.0, very actively released, already in the creator's stack) and Manim CE (MIT, the tool the original 3Blue1Brown clacks animation lineage comes from) are the two strongest fits; Motion Canvas and ManimGL show stale release cadences.

### Cited Findings

Maintenance / licence snapshot (all [API], 2026-11-13):

| Tool | Latest release | Last push | Licence (GitHub SPDX) | Stars |
|---|---|---|---|---|
| Manim Community (ManimCommunity/manim) | v0.22.1, 2026-10-27 | 2026-11-12 | MIT | 42.5k |
| ManimGL (3b1b/manim) | v1.7.2, 2024-12-13 | 2026-09-09 | MIT | 96.5k |
| Remotion (remotion-dev/remotion) | v4.0.543, 2026-11-11 | 2026-11-12 | custom (NOASSERTION) | 72.8k |
| Motion Canvas (motion-canvas/motion-canvas) | v3.17.2, 2024-12-14 | 2026-07-02 | MIT | 19.8k |
| HyperFrames (heygen-com/hyperframes) | v0.9.41, 2026-11-13 | 2026-11-13 | Apache-2.0 | 83.6k |
| p5.js (processing/p5.js) | v2.4.0, 2026-11-12 | 2026-11-11 | LGPL-2.1 | 24.3k |
| Processing 4 (processing/processing4) | 4.5.7 (build 1435), 2026-09-24 | 2026-10-25 | custom (NOASSERTION) | 0.5k |
| Godot (godotengine/godot) | 4.7.2-stable, 2026-08-18 | 2026-11-12 | MIT | 120k |
| CCapture.js (spite/ccapture.js) | v2.0.0, 2026-07-27 | 2026-10-13 | MIT | 3.8k |
| pygame (pygame/pygame) | 2.6.1, 2024-09-29 | 2025-11-01 | (none detected) | 9.0k |
| pygame-ce (pygame-community/pygame-ce) | 2.5.8, 2026-08-09 | 2026-11-10 | (none detected) | 1.7k |
| Mediabunny (Vanilagy/mediabunny, WebCodecs muxing) | v1.65.2, 2026-11-04 | 2026-11-12 | MPL-2.0 | 7.5k |

Sources for the table: [ManimCommunity/manim](https://api.github.com/repos/ManimCommunity/manim), [3b1b/manim](https://api.github.com/repos/3b1b/manim), [remotion-dev/remotion](https://api.github.com/repos/remotion-dev/remotion), [motion-canvas/motion-canvas](https://api.github.com/repos/motion-canvas/motion-canvas), [heygen-com/hyperframes](https://api.github.com/repos/heygen-com/hyperframes), [processing/p5.js](https://api.github.com/repos/processing/p5.js), [processing/processing4](https://api.github.com/repos/processing/processing4), [godotengine/godot](https://api.github.com/repos/godotengine/godot), [spite/ccapture.js](https://api.github.com/repos/spite/ccapture.js), [pygame/pygame](https://api.github.com/repos/pygame/pygame), [pygame-community/pygame-ce](https://api.github.com/repos/pygame-community/pygame-ce), [Vanilagy/mediabunny](https://api.github.com/repos/Vanilagy/mediabunny).

Manim (CE and GL)
- Manim CE releases in 2026: v0.19.2 (Jan 17), v0.20.0 (Feb 20), v0.20.1 (Feb 27), v0.21.0 (Aug 10) — [Manim CE changelog](https://docs.manim.community/en/stable/changelog/0.21.0-changelog.html); the GitHub API shows v0.22.1 on 2026-10-27 — [GitHub API](https://api.github.com/repos/ManimCommunity/manim/releases/latest).
- ManimGL's last tagged release is v1.7.2 (2024-12-13) although the repo was pushed to on 2026-09-09, i.e. development continues on the branch without releases — [GitHub API](https://api.github.com/repos/3b1b/manim/releases/latest); a secondary article notes users sometimes install from the repo head to get newer behaviour — [remio.ai](https://www.remio.ai/post/3b1b-manim-is-trending-again-but-the-real-story-is-its-split-ecosystem).
- Manim CE `Scene.add_sound(sound_file, time_offset=0, gain=None)` attaches an audio file at the current scene time; scene/mobject updaters receive `dt`, documented as defaulting "(mostly) to 1/frames_per_second" — [Manim CE Scene reference](https://docs.manim.community/en/stable/reference/manim.scene.scene.Scene.html).
- The original 3Blue1Brown clacks scene is Manim code: collisions are precomputed in `get_clack_data()`, and sounds are added in `add_clack_sounds()` with `collision_sound: "clack.wav"`, `min_time_between_sounds: 0.004`, `gain=-20` — [3b1b/videos _2019/clacks/question.py](https://raw.githubusercontent.com/3b1b/videos/master/_2019/clacks/question.py).

Remotion
- Free licence: "For individuals and companies of up to 3 people", all features, unlimited commercial use. Company licence otherwise: "Remotion for Creators" $25 per seat per month; "Remotion for Automators" $0.01 per render with a $100 monthly minimum; Enterprise from $500 per month — [Remotion licence & pricing](https://www.remotion.dev/docs/license/pricing).
- The licence is source-available, not OSI open source (GitHub reports no SPDX match) — [GitHub API](https://api.github.com/repos/remotion-dev/remotion); HyperFrames' own comparison calls it a "Source-available Remotion License" — [heygen-com/hyperframes README](https://github.com/heygen-com/hyperframes).
- Determinism model: Remotion renders several browser tabs in parallel that do not share state; animations must be "driven purely by `useCurrentFrame()`", must show the same visual for the same frame, and "should not rely on frames being rendered in order"; randomness only through its seeded `random()` — [Remotion flickering docs](https://www.remotion.dev/docs/flickering).

Motion Canvas
- A TypeScript library that "uses generators to program animations" plus a real-time preview editor; positioned for informative vector animations synchronised with voice-overs — [Motion Canvas docs](https://motioncanvas.io/docs/).
- Last tagged release v3.17.2 on 2024-12-14; last push 2026-07-02 — [GitHub API](https://api.github.com/repos/motion-canvas/motion-canvas/releases/latest). A Hacker News commenter called it abandoned while another called it merely "stable"; neither is an official statement — [HN thread mirror](https://hn.nuxt.dev/item/47155375).
- Revideo is a fork created because Motion Canvas maintainers treated video-pipeline features as out of scope — [Revideo docs](https://docs.re.video/). The `redotvideo/revideo` GitHub API path returned "Moved Permanently" on 2026-11-13 (repo renamed/moved; new location not followed) — [GitHub API](https://api.github.com/repos/redotvideo/revideo).

HyperFrames
- Apache-2.0 with "no per-render fees or commercial-use thresholds"; renderer "seeks each frame in headless Chrome and encodes the result with FFmpeg, so the same input produces the same video"; adapters for GSAP, CSS, Lottie, Three.js, Anime.js, WAAPI, or a custom runtime; audio declared with `<audio>` plus `data-start`, `data-duration`, `data-track-index`, `data-volume` and mixed by the producer package — [heygen-com/hyperframes README](https://github.com/heygen-com/hyperframes).
- Composition rules: a paused timeline registered on `window.__timelines` under the root id, no wall-clock time, no unseeded randomness; violations make output "break quietly". Examples set `data-fps="30"`, `data-width`, `data-height`. HeyGen itself concedes Remotion is older, has more templates/production history, a more mature Lambda renderer, and a model that is "simpler to reason about" — [HyperFrames vs Remotion guide](https://hyperframes.heygen.com/guides/hyperframes-vs-remotion).
- Frame-adapter contract (experimental v0 API, signatures may change): `{ id, init?, getDurationFrames(), seekFrame(frame), destroy? }`; the renderer requests frames in any order, so adapters must support forward/backward/random seeks, return identical state for the same frame, avoid wall-clock timers and unseeded randomness, and finish async work before capture. `createGSAPFrameAdapter({id, fps, timeline})` is the built-in helper — [HyperFrames frame adapters](https://hyperframes.heygen.com/concepts/frame-adapters).
- The producer's audio mix reportedly targets -14 LUFS (third-party summary of HeyGen material, not re-checked against source) — [HeyGen html-to-video write-up](https://www.heygen.com/research/html-to-video).

Canvas / p5.js + capture
- MDN's canvas optimisation guide recommends pre-rendering repeated drawing to an offscreen canvas and says to avoid `shadowBlur` where possible — [MDN Optimizing canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas).
- CCapture.js is still alive (v2.0.0, 2026-07-27) — [GitHub API](https://api.github.com/repos/spite/ccapture.js/releases/latest); Mediabunny is an actively released WebCodecs-era media library (v1.65.2, 2026-11-04) — [GitHub API](https://api.github.com/repos/Vanilagy/mediabunny/releases/latest).

Python + ffmpeg (pygame etc.)
- Upstream pygame has had no release since 2.6.1 (2024-09-29); the pygame-ce fork is the maintained line (2.5.8, 2026-08-09) — [pygame API](https://api.github.com/repos/pygame/pygame/releases/latest), [pygame-ce API](https://api.github.com/repos/pygame-community/pygame-ce/releases/latest).

### Inferences
Qualitative matrix. Rows not backed by a citation above are from general tool knowledge and are **unverified in this session**.

| Tool | 9:16 | Determinism | Render speed | Text / LaTeX | Glow / bloom | Audio | Learning curve for this creator |
|---|---|---|---|---|---|---|---|
| Manim CE | Yes (set pixel width/height + frame size in config; unverified this session) | Strong: fixed dt per frame, offline renderer | Slow-to-medium (Cairo CPU); fine for 28 s | Best: native LaTeX (`MathTex`) | Weak: no built-in bloom; fake with stacked wide low-opacity strokes, or post-process in ffmpeg | `add_sound` per event (proven by 3b1b clacks code) | Medium-high: new scene/mobject model, LaTeX install |
| ManimGL | Yes | Strong | Faster (OpenGL), interactive | LaTeX | Better (shaders possible) | Same `add_sound` lineage | High: sparse docs, no release since Dec 2024 |
| Remotion | Yes (composition width/height) | Strong by contract (pure function of frame; parallel tabs) | Good (multi-tab concurrency) | Web fonts; KaTeX/MathJax via React | Full browser stack (canvas, SVG, CSS, WebGL) | First-class `<Audio>` with frame offsets | Medium: React + bundler; overlaps HyperFrames' role |
| Motion Canvas | Yes | Good (generator timeline, seekable in editor) | Medium | Has LaTeX component | Canvas filters/shadows | Single audio track oriented; per-event SFX is awkward (unverified) | Medium; stale releases |
| HyperFrames | Yes (`data-width=1080 data-height=1920`) | Strong if rules followed; silent failure if not | Medium (headless Chrome screenshot per frame) | Web fonts; KaTeX possible; Thai fonts already solved in this project | Full browser stack | Declarative `<audio>` tracks mixed by producer | Lowest: already in use |
| Canvas/p5 + puppeteer/CCapture/WebCodecs | Yes | Only if you write the frame-stepping harness yourself | Medium | Canvas text; no LaTeX without extra lib | `shadowBlur`, `filter`, additive blend | None built in: mux with ffmpeg | Low-medium, but you rebuild what HyperFrames already gives |
| Python (pygame-ce / cairo / skia / matplotlib) + ffmpeg pipe | Yes | Strong if you step frames manually and pipe raw frames | Fast (skia) to slow (matplotlib) | Weak-to-OK; matplotlib has mathtext | Manual: blur a glow layer with numpy/OpenCV/skia image filters and add | None built in: build WAV with numpy, mux with ffmpeg | Low for Python users; all layout/typography by hand |
| Processing (Java) | Yes | `saveFrame` loop is frame-stepped | Fast | Basic | `blendMode(ADD)` + blur filter | Separate | Medium; new language/runtime, no advantage here |
| Godot / Unity | Yes | Godot has a fixed-fps "movie maker" write mode (unverified this session) | Real-time fast | UI text, no LaTeX | Best: real HDR bloom/glow | Engine audio, recorded with movie mode | High; overkill for a 2D block puzzle |

- The seek-based web renderers (Remotion, HyperFrames) and the offline Python renderers (Manim) both satisfy "frame-accurate, not wall-clock"; the risk class is the same in both web tools: any code path that reads real time or runs its own `requestAnimationFrame` loop silently breaks determinism.
- For a solo creator, Remotion is free (individual / ≤3 people), so licence cost is not the blocker; the blocker is that it duplicates a renderer the creator already operates and adds a React/bundler layer.
- ManimGL and Motion Canvas are poor choices for a new production pipeline in late 2026 on release-cadence grounds alone (both last tagged December 2024).

### Gaps
- No benchmark of actual render time per tool for this scene was run or found; "render speed" cells are qualitative.
- Manim CE vertical configuration, Godot movie-maker mode, Motion Canvas audio limits and Processing behaviour were not re-verified from primary docs in this session.
- Unity was not researched separately (licence/terms as of late 2026 not checked).
- Revideo's current repo location and maintenance status were not resolved.
- The team's local notes pin HyperFrames v0.7.37; upstream is now v0.9.41. Changes between those versions were not reviewed.

## 2. Driving a custom simulation frame-by-frame in a seek-based renderer

### Takeaway
The correct pattern is exactly what 3Blue1Brown's own clacks code does: compute the full collision event list once (analytically), then make every frame a pure function `state(t)` that looks up the surrounding events and interpolates; never integrate physics step-by-step inside the render loop. The same event list then drives the counter, the flashes, and the audio track.

### Cited Findings
- 3b1b's `SlidingBlocks.get_clack_data()` precomputes a finite list of `(location, time)` collision events using `theta = np.arctan(np.sqrt(self.mass_ratio))` and `for k in range(1, int(PI / theta) + 1)`; per-frame position is derived from a linearly advancing phase-space point reflected by geometry, and the counter is `n_clacks = int(ps_point_angle / theta)` — not a physics integration — [3b1b/videos clacks/question.py](https://raw.githubusercontent.com/3b1b/videos/master/_2019/clacks/question.py).
- The collision count has the digits of pi when the mass ratio is a power of 100: ratio 100 gives 31 collisions, 10,000 gives 314 — [3Blue1Brown clacks solution](https://3blue1brown.com/lessons/clacks-solution); [IMA "Computing Pi Inefficiently"](https://ima.org.uk/13142/urban-maths-computing-pi-inefficiently/).
- Remotion: treat a component as a function from frame number to image; same frame must give the same visual; frames may render out of order across parallel tabs — [Remotion flickering docs](https://www.remotion.dev/docs/flickering).
- HyperFrames: the renderer pauses the animation and seeks it to an exact time before each capture; a frame adapter's `seekFrame(n)` must support random-order seeks and be idempotent — [HyperFrames vs Remotion](https://hyperframes.heygen.com/guides/hyperframes-vs-remotion); [frame adapters](https://hyperframes.heygen.com/concepts/frame-adapters).
- Motion Canvas programs animations with generator functions — [Motion Canvas docs](https://motioncanvas.io/docs/).
- This project's own HyperFrames study notes record that a raw `requestAnimationFrame` loop outside a frame adapter drops HyperFrames from deterministic capture to a real-time screenshot mode, and that `Math.random()`/`Date.now()` must be replaced by a seeded PRNG — local file `/Users/phariyawit.jiap/Documents/Auto-Affi/docs/reference/hyperframes-packages-guides.md` (lines 72 and 75), which summarises the [HyperFrames guides](https://hyperframes.heygen.com/guides/hyperframes-vs-remotion).

### Inferences
- Recommended architecture (tool-agnostic), unverified by execution:
  1. `events = simulate(m1, m2, v0, x1, x2)` — event-driven, exact: between collisions both blocks move at constant velocity, so the next collision time is solved in closed form (block-block or block-wall), velocities are updated with the elastic-collision formulas, and the loop ends when no further collision can occur. Output: array of `{t, x1, x2, v1, v2, kind}`. For ratio 100 this is 31 events; for 10,000 it is 314.
  2. `state(t)`: binary-search the last event with `event.t <= t`, then `x = event.x + event.v * (t - event.t)`. `count(t)` = index of that event + 1. This is random-access, idempotent and order-independent, which is exactly the Remotion / HyperFrames contract.
  3. Time remapping ("slow motion" caption): keep physics in simulation time and define a monotonic `simTime = warp(videoTime)`; map event times through the inverse warp to get video-time timestamps for audio and flashes. Do not slow the simulation by changing dt.
  4. Emit `events.json` once from a Node or Python script; the composition and the audio builder both read it, so picture and sound cannot drift.
- HyperFrames wiring (inferred, needs a smoke test): one paused GSAP timeline registered at `window.__timelines[id]` containing a single linear proxy tween, e.g. `tl.to(clock, { t: DURATION, duration: DURATION, ease: "none", onUpdate: () => draw(clock.t) })`, where `draw(t)` repaints a `<canvas>` (or sets SVG/DOM attributes) from `state(t)`. GSAP fires `onUpdate` on seek, so this stays inside the supported GSAP adapter and avoids the experimental custom frame-adapter API. DOM text (title, "clacks: N", captions, watermark) can be set in the same callback.
- Remotion equivalent: `const t = useCurrentFrame() / fps; const s = state(t);` and draw in a `useEffect`/canvas ref or as SVG. Motion Canvas equivalent: a single `yield* time(0, DURATION, DURATION, linear)` signal with nodes computed from it, rather than chaining tweens per collision.
- Why not step physics per frame: at high mass ratios many collisions fall inside one 1/30 s frame, so fixed-dt integration miscounts collisions (tunnelling) and makes the final count wrong — fatal for a video whose punchline is the count.

### Gaps
- The exact `onUpdate`-on-seek behaviour under HyperFrames v0.9.x was not tested; the official frame-adapter page gives no canvas guidance and no documented registration API for custom adapters.
- Not verified whether `<canvas>` 2D content is captured identically in HyperFrames' deterministic mode and its fallback screenshot mode.
- Which mass ratio @mathmango1 used (and therefore the true event count in the reference clip) was not measured in this research task.

## 3. Achieving the neon glow look (and its cost in headless Chrome)

### Takeaway
The cheap, robust neon recipe is "bright thin core + one or two wider blurred copies composited additively on a near-black background"; prefer pre-rendered or low-resolution glow layers over per-frame `shadowBlur` or stacked CSS blur filters, because blur cost scales with radius × area × frames in a screenshot-per-frame renderer.

### Cited Findings
- MDN: pre-render repeated drawing to an offscreen canvas and "avoid the shadowBlur property whenever possible" — [MDN Optimizing canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas).
- web.dev: offscreen canvases should fit the sprite tightly, otherwise the copy cost cancels the gain — [web.dev canvas performance](https://web.dev/articles/canvas-performance/).
- A real-world change replaced `shadowBlur` glow with multiple fills of the same shape at increasing inflation and decreasing `globalAlpha`, reporting a visually close result — [feedBack PR #729](https://github.com/got-feedBack/feedBack/pull/729).
- A community answer suggests drawing the glow on a much smaller canvas and scaling it up with smoothing as a faster blur than filters — [html5gamedevs thread](https://www.html5gamedevs.com/topic/11450-most-performant-way-to-draw-a-blurred-polygon).
- `shadowBlur` performance differs widely by engine (far slower in Firefox than Blink per a Mozilla bug) — [Mozilla bug 1190398](https://bugzilla.mozilla.org/show_bug.cgi?id=1190398).
- This project's HyperFrames notes: stacked `backdrop-filter: blur()` layers blow the frame budget; keep to 2–3 blur layers per region and pre-render static blur to PNG — local file `/Users/phariyawit.jiap/Documents/Auto-Affi/docs/reference/hyperframes-packages-guides.md` (line 76), summarising the [HyperFrames guides](https://hyperframes.heygen.com/guides/hyperframes-vs-remotion).

### Inferences
(All from general web-graphics knowledge; unverified by rendering in this session.)
- Option ranking for this clip (few shapes, 1080x1920, ~840 frames at 30 fps):
  1. **Canvas 2D, two-pass stroke**: draw each stroke twice — a wide pass with `shadowColor` = stroke colour and `shadowBlur` ≈ 20–40 px, then a thin near-white core. With under ~10 glowing primitives per frame, `shadowBlur` in Blink is affordable for an offline render even though MDN discourages it for real-time. Set `globalCompositeOperation = "lighter"` for glow passes so overlapping cyan/pink/orange add toward white like real light.
  2. **Sprite the static glow**: the orange floor/wall line and the block outlines never change shape, so render each once (with glow) to a tight offscreen canvas or PNG and `drawImage` it at the block's x each frame. This makes per-frame cost near zero and is the MDN-recommended pattern.
  3. **CSS on DOM/SVG elements**: `filter: drop-shadow(0 0 6px c) drop-shadow(0 0 18px c)` (two stacked radii give the tight-plus-wide halo) or `text-shadow` for the coloured counter digits. Good for text; each filtered element becomes its own compositing layer, so keep the count small and avoid animating the blur radius.
  4. **SVG `feGaussianBlur` + `feMerge`**: equivalent look, resolution-independent; set the filter region (`x/y/width/height`) generously or the glow is clipped to the bounding box — the most common pitfall. Thin horizontal/vertical lines have a zero-height bounding box, so use `filterUnits="userSpaceOnUse"`.
  5. **True bloom post-process** (render scene to a texture, threshold, multi-scale blur, add back; e.g. three.js `UnrealBloomPass`): best quality and the only option that makes everything bright glow uniformly, but adds WebGL to the capture path (headless GPU/SwiftShader differences, colour-space and antialiasing surprises). Not needed for flat 2D line art.
  6. **ffmpeg-side bloom**: render clean frames, then `split → gblur → blend=all_mode=screen` (or `addition`) in one filtergraph. Zero browser cost and tool-agnostic; downside is that it also blooms white text unless text is composited after.
- Pitfalls specific to headless Chrome capture: (a) glow on pure `#000` shows 8-bit banding in wide halos after H.264 — use a dark navy background (as the reference clip does) and/or add faint noise; (b) 4:2:0 chroma subsampling softens saturated cyan/pink thin lines, so keep the core stroke at least 4–6 px at 1080 wide and near-white in the centre; (c) `device-scale-factor` > 1 multiplies blur cost by its square; (d) software-GL fallback makes filter-heavy pages much slower than on the developer's interactive Chrome; (e) blur/filter output can differ slightly between Chrome versions and platforms, which matters only if frames are rendered on mixed machines.
- The gradient-coloured lines in the circle diagram: assign each chord a hue from its collision index (`hsl(index / N * span)`) and draw with additive blending so dense regions brighten.

### Gaps
- No source was found that benchmarks `shadowBlur` vs CSS `drop-shadow` vs SVG filters specifically under headless Chrome screenshot capture.
- No primary source confirming additive (`"lighter"`) compositing as the recommended neon technique was found; it is standard practice but cited here only as inference.
- The reference clip's exact glow radii/colours were not measured in this task.

## 4. Generating and syncing collision sound effects programmatically

### Takeaway
Build the whole SFX track offline as one WAV from the same event list (sample-accurate placement in numpy, or `OfflineAudioContext`), thin events with a minimum inter-sound gap exactly as 3Blue1Brown does (0.004 s), then mux/mix it as a single audio track; do not hand hundreds of individual clips to ffmpeg `adelay`/`amix` or to the compositor.

### Cited Findings
- 3b1b's implementation: iterate precomputed clack times, skip any event closer than `min_time_between_sounds = 0.004` s to the last accepted one, and call `add_sound("clack.wav", time_offset=..., gain=-20)`; slow-motion scenes swap in `slow_clack.wav`; visual flashes are thinned separately with `min_time_between_flashes: 1/30` — [3b1b/videos clacks/question.py](https://raw.githubusercontent.com/3b1b/videos/master/_2019/clacks/question.py).
- Manim CE exposes the same per-event API: `add_sound(sound_file, time_offset=0, gain=None)` — [Manim CE Scene reference](https://docs.manim.community/en/stable/reference/manim.scene.scene.Scene.html).
- ffmpeg `amix` has a `normalize` option that defaults to on and rescales inputs by active input count; `normalize=0` disables it. A Trac ticket shows `amix=inputs=79:normalize=0` in real use. Older source capped inputs at 32; newer source allows up to INT16_MAX — [ffmpeg amix docs (7.1)](https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Audio/amix.html); [FFmpeg Trac #8033](https://ffmpeg.org/pipermail/ffmpeg-trac/2021-May/058498.html); [af_amix.c source](https://ffmpeg.org/doxygen/trunk/af__amix_8c_source.html).
- HyperFrames audio is declarative (`<audio data-start data-duration data-track-index data-volume>`), mixed by the producer, and scripts that control media playback desync the mix — [heygen-com/hyperframes README](https://github.com/heygen-com/hyperframes); local notes `/Users/phariyawit.jiap/Documents/Auto-Affi/docs/reference/hyperframes-packages-guides.md` (line 71).
- The pygame-based "bouncing ball" tutorials play sounds live through the mixer (one sample raises `pygame.mixer.set_num_channels(500)`), i.e. real-time playback rather than an offline-built track — [Pythonic Bounce: add sound](https://pythonic-bounce.beehiiv.com/p/pythonic-bounce-how-to-add-sound-and-run-the-simulation).
- TikTok publishes no official loudness target; vendor sources mostly cite about -14 LUFS integrated with -1 dBTP ceiling, one cites -16 LUFS — [Fora Soft LUFS targets 2026](https://www.forasoft.com/learn/audio-for-video/articles-audio/lufs-targets-per-platform-2026); [loudfix TikTok](https://loudfix.pages.dev/normalize-audio-tiktok); [-16 LUFS claim](https://d1lex0gkhzvix9.cloudfront.net/tiktok-instagram-reels-loudness).

### Inferences
(Recipe is PRODUCED, not VERIFIED — nothing was rendered.)
- Recommended recipe (Python, already in the stack):
  1. Load one short clack sample (or synthesise: 2–5 ms noise burst through a band-pass around 2–4 kHz with a ~40–80 ms exponential decay; a woodblock-like sine at ~1.2 kHz with fast decay also works) at 48 kHz mono float.
  2. `track = np.zeros(int(sr * duration))`; for each event in video time: `i = round(t * sr); track[i:i+len(clack)] += gain * clack`. Placement is sample-accurate (1/48000 s), far finer than a 1/30 s frame.
  3. **Rate limit**: drop events closer than ~4 ms to the previously accepted one (3b1b's constant). 4 ms = 250 clacks/s, which already fuses into a buzz/zip; that is the desired "merging" effect.
  4. **Density handling**: scale per-clack gain by local density (e.g. `gain = 1/sqrt(1 + clacks_in_last_50ms)`) so the burst does not clip, and optionally shorten the decay tail when the gap is small.
  5. **Pitch rising** (if wanted for drama; note 3b1b used a fixed sample): resample each clack by a factor tied to collision index or inverse gap (`rate = 2 ** (k * semitone / 12)`), precomputing a handful of pitch variants rather than resampling per event. With a fixed sample, perceived pitch still rises naturally as the repetition rate enters the audible range.
  6. Slow-motion sections: use event times after the time warp, and optionally a lower/longer clack variant, mirroring `slow_clack.wav`.
  7. Soft-limit (`np.tanh` or a peak limiter), write WAV with `soundfile`, then loudness-normalise with ffmpeg two-pass `loudnorm=I=-14:TP=-1:LRA=11` (measure pass, then apply with measured values) and mux: `-c:v copy -c:a aac -b:a 192k -ar 48000`.
- Alternatives: `OfflineAudioContext` (schedule one `AudioBufferSourceNode.start(t)` per event with `playbackRate` for pitch, render to a buffer, encode WAV) keeps everything in JS/Node-adjacent tooling and is equally sample-accurate; `sox`/pydub work but offer nothing over numpy here; ffmpeg `adelay`+`amix` is workable for a few dozen events (ratio 100 → 31 clacks) if `normalize=0` is set, but a 300+ input filtergraph is slow to build, fragile on the command line, and gives no density control.
- In HyperFrames, attach the finished WAV as a single `<audio data-start="0">` track (or mux afterwards with ffmpeg) instead of 31–314 `<audio>` elements; if the producer applies its own loudness target, normalise only once (either let the producer do it, or mux outside the producer) to avoid double processing.
- Sync check that should be run before publishing: compare event times against audio onsets (e.g. detect peaks in the rendered WAV and diff against `events.json`) and step through frames at 3–4 collisions to confirm the counter increments on the same frame as the contact. A loudness-only short clip with sparse transients reads low on integrated LUFS, so also check true peak rather than relying on LUFS alone.

### Gaps
- No primary TikTok source for a loudness target exists; -14 LUFS is an industry convention, unverified.
- Whether HyperFrames v0.9.x normalises the final mix to -14 LUFS automatically was only seen in a secondary summary; not confirmed in the official docs fetched.
- How @mathmango1 produced the clack audio (sample vs synthesis, pitch behaviour) was not analysed here.
- No source found on ffmpeg performance with hundreds of `adelay` branches.

## 5. TikTok export specs as of 2026

### Takeaway
Export 1080x1920, H.264 + AAC in MP4, 30 fps (60 only if motion genuinely benefits), roughly 8–12 Mbps for line-art on dark backgrounds; keep titles, counter and captions inside the centre region and out of the top ~10%, bottom ~20–25% and right ~12–15% of the frame. Only the ad-spec minimums are officially published; safe-zone pixel numbers come from third parties and conflict.

### Cited Findings
- Official TikTok Ads spec (in-feed, non-Spark): vertical 9:16 recommended, resolution at least 540x960; file types .mp4/.mov/.mpeg/.3gp/.avi; duration up to 10 minutes; file size ≤ 500 MB; bitrate ≥ 516 kbps. Safe zone depends on orientation, caption length and add-on formats, and TikTok provides downloadable safe-zone files rather than pixel numbers on the page — [TikTok Ads Help: auction in-feed ads](https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads).
- Third-party guides agree on 1080x1920, 9:16, MP4/MOV with H.264 and AAC; 30 fps most commonly recommended, 23–60 fps accepted — [Sked Social size guide](https://skedsocial.com/blog/tiktok-video-size-guide); [postfa.st TikTok specs](https://postfa.st/sizes/tiktok/video).
- Bitrate recommendations vary: 4–6 Mbps, ~5 Mbps for 1080p, 4–8 Mbps, and 8–10 Mbps for 60 fps — [cococonvert](https://cococonvert.com/blog/video-for-tiktok-format); [convertintomp4 2026 specs](https://convertintomp4.com/da/blog/social-media-video-specs-2026).
- Safe-zone figures conflict between sources: top ~150 px / bottom ~480 px; top ~220 px / bottom ~480 px; and top 120–200 px, bottom 250–370 px, right 120–164 px, left 50–60 px — [socialrails](https://socialrails.com/sizes/tiktok/video); [screensnap guide](https://www.screensnap.pro/blog/tiktok-video-size-guide); [posteverywhere](https://posteverywhere.ai/blog/tiktok-aspect-ratio).

### Inferences
- A conservative layout box that satisfies all three third-party safe-zone sets on a 1080x1920 canvas: keep essential text within x ≈ 60–910 px and y ≈ 220–1440 px. The title should sit below y ≈ 220; the "clacks: N" counter and small captions should stay above y ≈ 1440; nothing important in the right ~170 px column (like/comment/share rail). Decorative elements (floor line, glow, faint watermark) can bleed outside.
- 30 fps is the pragmatic default: it halves render time and file size, matches the most common recommendation, and the collision burst is conveyed mostly by audio and the counter anyway. 60 fps is defensible for fast sliding motion but TikTok re-encodes uploads regardless (re-encode behaviour unverified).
- Because TikTok transcodes, upload a higher-quality master than the delivery target: e.g. `libx264 -crf 14–16 -preset slow -pix_fmt yuv420p -profile:v high -movflags +faststart`, BT.709 tagged, AAC 192 kbps 48 kHz. Thin neon lines on dark gradients are where low bitrates band and smear first.
- Length: the reference is 28 s; a puzzle-question short benefits from a loopable ending. No authoritative 2026 source on "recommended length" for organic posts was found, so treat any specific number as opinion.

### Gaps
- No official TikTok page for organic-upload recommended resolution/bitrate/fps or organic safe zones was retrieved; the official numbers above are ad minimums.
- TikTok's downloadable safe-zone template was not downloaded or measured.
- No primary source for TikTok's 2026 recommended video length for organic reach.
- TikTok's server-side re-encode ladder (and whether 60 fps is preserved) is unverified.

## 6. What creators of this genre actually use, and whether they generate code with AI

### Takeaway
Evidence is thin and mostly indirect: the dominant documented stack for "bouncing ball / satisfying simulation" shorts is Python + pygame (screen-captured or frame-exported), with tutorials explicitly prompting ChatGPT for the code; the maths-explainer lineage (3Blue1Brown's clacks) is Manim. No disclosure of @mathmango1's own stack was found.

### Cited Findings
- A newsletter aimed at this genre walks readers through asking ChatGPT for a pygame bouncing-ball simulation, customising it and posting captures to TikTok/Shorts/Reels — [Pythonic Bounce: create with ChatGPT](https://pythonic-bounce.beehiiv.com/p/create-own-bouncing-ball-code-with-chatgpt-code); companion issues cover adding sound with pygame + numpy — [Pythonic Bounce: sound](https://pythonic-bounce.beehiiv.com/p/pythonic-bounce-how-to-add-sound-and-run-the-simulation).
- An itch.io seller markets a bouncing-ball project as used on many large YouTube/TikTok channels, indicating templated/commercialised code in the genre — [Jimmylol on itch.io](https://jimmylol.itch.io).
- Open-source "ball in ring chaos" projects for this style are Python + pygame — [QuantumZain/chaotic-system](https://github.com/QuantumZain/chaotic-system).
- The canonical colliding-blocks animation is 3Blue1Brown's, written in Manim, with source published — [3b1b/videos clacks/question.py](https://raw.githubusercontent.com/3b1b/videos/master/_2019/clacks/question.py); [3Blue1Brown clacks solution](https://3blue1brown.com/lessons/clacks-solution).
- HyperFrames is explicitly positioned for AI-agent-authored video (plain HTML handoff to agents, agent skills) — [heygen-com/hyperframes README](https://github.com/heygen-com/hyperframes); [HyperFrames vs Remotion](https://hyperframes.heygen.com/guides/hyperframes-vs-remotion).

### Inferences
- The reference clip's look (rounded neon blocks, glow, crisp web-style sans-serif, CSS-like gradients) is consistent with either a browser canvas/SVG render or a Python renderer with a glow pass; it cannot be attributed to a specific tool from appearance alone.
- Given the tutorial ecosystem and the simplicity of the scenes, AI-assisted code generation is very likely common in the genre, but this is an inference from tutorials, not from creator disclosures.
- pygame-style real-time capture is the least deterministic route (wall-clock loop, live mixer audio); the creator's existing seek-based pipeline is a technical step up from what the genre's tutorials describe.

### Gaps
- No Reddit, Hacker News or YouTube thread was found in which a simulation-shorts creator states their stack; searches returned tutorials and code-generator pages only.
- No statement from @mathmango1 about tools or AI use was found (profile/bio/comments were not inspected in this task).
- No quantitative data on how prevalent AI-generated code is among these channels.

## 7. Recommendation for this creator (existing HyperFrames + ffmpeg + Python/Node stack)

### Takeaway
Stay on HyperFrames: one 1080x1920, 30 fps composition whose single paused GSAP timeline drives a pure `draw(t)` over a precomputed collision event list, with DOM/CSS for all text, canvas (or SVG) for blocks and the circle diagram, and one numpy-built clack WAV muxed with ffmpeg. Use Manim CE only if LaTeX-heavy explanation scenes become the core of the channel. Main risk: HyperFrames' determinism rules fail silently, and driving a canvas via GSAP `onUpdate` is an inferred pattern that has not been tested on this machine.

### Cited Findings
- HyperFrames is Apache-2.0 with no per-render or commercial thresholds, seek-based, and released as recently as 2026-11-13 (v0.9.41) — [heygen-com/hyperframes README](https://github.com/heygen-com/hyperframes); [GitHub API](https://api.github.com/repos/heygen-com/hyperframes/releases/latest).
- Its rules (paused timeline on `window.__timelines`, no wall clock, no unseeded randomness) "break quietly" when violated, and its custom frame-adapter API is experimental v0 — [HyperFrames vs Remotion](https://hyperframes.heygen.com/guides/hyperframes-vs-remotion); [frame adapters](https://hyperframes.heygen.com/concepts/frame-adapters).
- The proven reference design for this exact puzzle (precomputed events, per-frame geometric lookup, sounds thinned at 0.004 s) is public and portable — [3b1b/videos clacks/question.py](https://raw.githubusercontent.com/3b1b/videos/master/_2019/clacks/question.py).
- Remotion would be free for a solo creator but is a second renderer with a React/bundler layer — [Remotion pricing](https://www.remotion.dev/docs/license/pricing).
- Manim CE is MIT and actively released (v0.22.1, 2026-10-27) — [GitHub API](https://api.github.com/repos/ManimCommunity/manim/releases/latest).

### Inferences
- Reasons for HyperFrames: zero new tooling or licence exposure; Thai-capable typography, lint/inspect gates and ffmpeg post already exist in this project; the browser gives every glow technique (canvas shadow, CSS drop-shadow, SVG filters, additive blending); the simulation is tiny (31 or 314 events) so the "pure function of time" pattern is trivial; and the same `events.json` feeds the Python audio builder.
- Suggested build order: (1) `simulate` script → `events.json` plus a unit check that the count equals 31 / 314 for ratios 100 / 10,000; (2) `state(t)` + `draw(t)` in a plain HTML page scrubbed by a slider; (3) wrap in the HyperFrames timeline; (4) numpy clack track → WAV → loudnorm; (5) render, mux, then verify by frame-stepping around several collisions and diffing two renders for identical frames.
- Runner-up: Manim CE, if future videos need equations and proof-style scenes; cost is a new mental model, LaTeX toolchain, and weaker glow (needs an ffmpeg bloom pass). Not recommended: ManimGL and Motion Canvas (no tagged release since December 2024), pygame-style real-time capture (non-deterministic), Godot/Unity (overkill).
- Main risk and mitigation: silent determinism failure (a stray `requestAnimationFrame`, `Date.now()`, or unseeded random drops capture to wall-clock mode or produces mismatched frames). Mitigate with a 2-second smoke render first, a double-render frame hash comparison, and a counter-vs-audio onset check before the full render. Secondary risks: the local project notes target HyperFrames v0.7.37 while upstream is v0.9.41 (pin the version used, or re-read the changelog before upgrading); heavy blur filters slowing headless capture (pre-render static glow sprites); TikTok re-encode banding on dark gradients (navy background, high-bitrate master).

### Gaps
- None of the recommended pipeline was executed; feasibility of the GSAP-proxy-tween canvas pattern in HyperFrames is unverified until a smoke render is done.
- No measured render time for a 28 s 1080x1920 canvas composition in HyperFrames on this machine.
- HyperFrames changes between v0.7.37 and v0.9.41 were not reviewed.
