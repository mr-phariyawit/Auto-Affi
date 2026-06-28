# HyperFrames Transitions — complete reference (for Auto-Affi)

> Studied 2026-06-28 from https://hyperframes.heygen.com — index (`/llms.txt`), `packages/shader-transitions`,
> all 14 individual shader pages, 13 transition-collection pages, `concepts/data-attributes`.
> HyperFrames = open-source **HTML→deterministic frame-by-frame video** (GSAP/Lottie/CSS, seekable).
> Auto-Affi uses it at the **Edit/compose stage** to composite the Veo clips as "scenes" with GPU
> shader transitions between them, plus catalog lower-thirds + caption effects.

## How transitions work (the API)

`@hyperframes/shader-transitions` — GPU (WebGL) transitions: captures each scene as a texture and
composites through fragment shaders driven by a **GSAP timeline**.

```js
import { init } from "@hyperframes/shader-transitions";
const timeline = init({
  bgColor: "#0a0a0a",
  accentColor: "#FFC400",                  // brand accent
  scenes: ["scene-1", "scene-2", "scene-3"],   // DOM element ids (our Veo clips)
  transitions: [
    { time: 4, shader: "whip-pan",            duration: 0.5 },
    { time: 16, shader: "flash-through-white", duration: 0.5 },
  ],
});
```
- `transitions[]` items: `{ time (s, absolute timeline pos), shader?, duration?, ease? (GSAP) }`.
- **Omit `shader`** → CSS-fallback (plain crossfade) at that point.
- No WebGL → graceful fallback to normal playback. `SHADER_NAMES` export = the valid 14 for validation.

### Declarative HTML timing (alternative / for layout)
`data-start` (seconds OR a clip id), `data-duration`, `data-track-index` (layer), `data-media-start`,
`data-volume`. **Relative timing = built-in crossfade:** `data-start="intro"` = start when intro ends;
`data-start="intro - 0.5"` = 0.5s **overlap/crossfade** (overlapping clips need different tracks);
`data-start="intro + 2"` = 2s gap.

## The 14 built-in shader transitions

| shader name | effect | best moment in an affiliate short |
|---|---|---|
| `flash-through-white` | white-flash crossfade | **PRODUCT REVEAL / hero** (climax, 0.5–1s) — top pick for the CTA reveal |
| `chromatic-radial-split` | RGB chromatic-aberration radial split | climactic hero/price reveal, pulls focus to center |
| `glitch` | digital glitch artifacts | hook / intentional disruption; **tech/digital products** |
| `light-leak` | cinematic light sweep | reveal or CTA; premium polish |
| `cinematic-zoom` | dramatic zoom blur (motion through space) | showcase→CTA pivot, feature change |
| `whip-pan` | fast camera whip-pan | energetic cut between demo beats / problem→solution |
| `domain-warp-dissolve` | fractal-noise organic dissolve | lifestyle → product close-up; soft midpoint |
| `ripple-waves` | concentric ripple distortion | product reveal; outward motion draws focus |
| `sdf-iris` | SDF circular iris open/close | reveal; geometric focus to center |
| `thermal-distortion` | heat-haze shimmer | premium polish → high-impact shot |
| `swirl-vortex` | swirling vortex distortion | transformative claim / pivotal moment |
| `cross-warp-morph` | morph-blend between two images | **before/after**, product-angle change |
| `gravitational-lens` | spacetime-bend warp | premium / upgrade / before-after |
| `ridged-burn` | ridged-turbulence burn | dramatic reveal / special offer |

> All ship as 4s showcase blocks at 1920×1080, installable via `npx hyperframes add <name>`, but as
> *transitions* the `duration` is set in the `transitions[]` config (use **0.3–0.6s** for short ads).

## The 13 transition collections (category showcases)

`transitions-3d` (perspective flip/rotate) · `-blur` · `-cover` · `-destruction` · `-dissolve` (fade) ·
`-distortion` (warp) · `-grid` · `-light` · `-mechanical` · `-other` · `-push` (slide) · `-radial`
(wipe/reveal) · `-scale` (zoom). Each is a 11–24s demo reel; install via `npx hyperframes add transitions-<cat>`.

## Recommended transition map for sub-30s affiliate shorts (Auto-Affi)

- **Keep most cuts HARD (no shader)** — research says 3+ cuts in first 3s lifts completion; shader on
  every cut = AI-slop. Use a shader only at 1–2 *meaning* moments.
- **Hook → first demo:** `whip-pan` (0.4s) — energy, problem→solution.
- **Within a continuous demo** (insert→lift→hang): **hard cuts** for continuity (no shader).
- **Final → CTA hero/price reveal:** `flash-through-white` or `chromatic-radial-split` (0.5s) — the one
  hero beat.
- Brand accent color into `accentColor`; pair with catalog **lower-thirds** (`lt-*`) + **caption** effects
  (`caption-*`) for price/CTA, NOT a shader.

## Where this fits Auto-Affi
Edit/compose stage (Step 5): Veo clips become `scenes`; the editor builds a HyperFrames HTML composition
with `init({scenes, transitions})`, burns Thai captions (caption-* blocks) + lower-third price card +
CTA endcard, renders deterministically → master. Cost: HyperFrames is local render (free, no API spend).

## Sources
hyperframes.heygen.com: `/packages/shader-transitions`, `/concepts/data-attributes`, the 14
`/catalog/blocks/<shader>` pages, the 13 `/catalog/blocks/transitions-*` pages, `/llms.txt`.
