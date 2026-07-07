# Learning — HyperFrames transitions (studied 2026-06-28)

HyperFrames = open-source HTML->deterministic video. `@hyperframes/shader-transitions` gives 14 GPU
shader transitions via `init({bgColor, accentColor, scenes:[ids], transitions:[{time,shader,duration,ease}]})`.
Omit `shader` -> CSS crossfade. Declarative HTML: data-start (id+offset = crossfade), data-duration,
data-track-index. 14 shaders: flash-through-white, chromatic-radial-split, glitch, light-leak,
cinematic-zoom, whip-pan, domain-warp-dissolve, ripple-waves, sdf-iris, thermal-distortion, swirl-vortex,
cross-warp-morph, gravitational-lens, ridged-burn. 13 collections (3d/blur/cover/destruction/dissolve/
distortion/grid/light/mechanical/other/push/radial/scale).

**Apply rule (affiliate shorts):** most cuts HARD (no shader; shader-on-every-cut = AI-slop); use a
shader only at 1-2 meaning moments — `whip-pan` hook->demo, `flash-through-white`/`chromatic-radial-split`
for the CTA hero reveal. Brand color -> accentColor. Lower-thirds/captions from catalog, not a shader.
HyperFrames render is LOCAL (free, no API spend) at the Edit/compose stage. Full ref:
docs/reference/hyperframes-transitions.md. See [[gemini-generation-playbook]].
