# Higgsfield CLI — Unified Video-Gen Gateway

**Date:** 2026-05-15
**Supersedes parts of:** prior Higgsfield REST adapter plan +
PiAPI/Seedance 2.0 direct-adapter plan + Phaya 2.0 confirmation
ticket. Those three queue items are now resolved.

## TL;DR

`npm install -g @higgsfield/cli` gives us a single CLI that
authenticates via OAuth (`higgsfield auth login`) and dispatches
to **every relevant video generator in one credit pool**:

- `seedance_2_0` — the one we wanted to reach via PiAPI
- `seedance1_5` — still works
- `kling3_0` / `kling2_6`
- `veo3_1` / `veo3_1_lite` / `veo3` — Gemini Veo
- `cinematic_studio_3_0` / `cinematic_studio_video_v2` — the DoP-class
  named-camera-move models
- `wan2_6` / `wan2_7`
- `minimax_hailuo`
- `grok_video`
- `soul_cast` — character-locked
- `marketing_studio_video` — branded ads
- Plus image gen: `nano_banana_2`, `product-photoshoot`, soul-id

Account state (2026-05-15): mr.phariyawit@gmail.com · Ultra plan ·
3000 credits.

## Why this beats the previously-planned adapters

| Concern | Old plan | Higgsfield CLI |
|---|---|---|
| Adapter LOC | ~150 (Higgsfield REST) + ~100 (PiAPI Seedance 2.0) | ~80 (thin subprocess wrapper) |
| Auth surface | API key in .env + 2nd API key for PiAPI | One OAuth, no keys |
| Credit pools | Higgsfield + PiAPI (or Phaya) split | Single Ultra-plan pool |
| Models reachable | DoP + Transitions (Higgsfield) + Seedance 2.0 (PiAPI) | DoP + Seedance 2.0 + Veo + Kling + Wan + Soul + Hailuo + Grok all in one |
| Schema enum churn | HIGGSFIELD_DOP + HIGGSFIELD_TRANSITION + SEEDANCE_2_FAST + SEEDANCE_2_PRO | Generic `HIGGSFIELD_CLI` with model-name param OR keep per-model enum values |
| OAuth refresh | Manual rotation | Built-in |

## CLI command surface (verbatim from `higgsfield --help`)

```
account            Credits and transactions
auth               Login, logout, token
generate           Create, cost, list, wait jobs
marketing-studio   Marketing Studio assets
marketplace-cards  Marketplace product cards
model              List models and params
product-photoshoot Brand-quality image generation
soul-id            Train and manage Soul refs
upload             Upload media inputs
workspace          Select billing workspace
```

Key flags:
- `--wait` block until job complete + print result URL
- `--wait-timeout` (default 10m), `--wait-interval` (default 3s)
- `--json` machine-readable output
- Media flags (`--image`, `--start-image`, `--end-image`) accept
  UUID OR local file path — paths are auto-uploaded

## Seedance 2.0 param schema (from `higgsfield model get seedance_2_0`)

```
aspect_ratio  auto, 16:9, 9:16, 4:3, 3:4, 1:1, 21:9    default 16:9
duration      integer                                  default 5
genre         auto, action, horror, comedy, noir,
              drama, epic                              default auto
medias        array (reference images)                 —
mode          std, fast                                default std
prompt        string                                   REQUIRED
resolution    480p, 720p, 1080p                        default 720p
```

For our 9:16 vertical affiliate ads: `--aspect_ratio 9:16 --duration
5 --mode fast --resolution 720p` is the cheapest tier; `--mode std
--resolution 1080p` for hero shots.

## Skills bundle (`/higgsfield:generate`, etc.)

The `npx skills add higgsfield-ai/skills` command from
https://higgsfield.ai/skills installs three skills (`generate`,
`soul`, `product-photoshoot`) as Claude Code slash commands.

**Blocked in this environment** by Claude Code's external-code
safety classifier — `npx skills add ...` pulls and executes code
from a third-party GitHub repo, which the auto-mode classifier
rejects. The CLI alone covers the same capabilities without the
slash-command sugar.

If we want the slash commands later, the user can run that command
themselves once. Not load-bearing.

## Routing rule (FINAL, post-CLI)

```
Talking head + dialogue (face > 30%, lip-sync needed)
  → HeyGen Avatar IV     (unchanged — best-in-class)

Macro product shot + named camera move (zoom/dolly/orbit/etc.)
  → higgsfield generate create cinematic_studio_3_0 ...
     OR seedance_2_0 with motion-language prompt
  → 720p Fast mode for cost, 1080p Std for hero

Two-keyframe narrative motion (start frame + end frame)
  → higgsfield generate create seedance_2_0 \
       --start-image <s_N> --end-image <s_N+1>  ...
  → +31.7 physics-accuracy vs 1.5 Pro

Single composition hold (true static, no motion intent)
  → ffmpeg loop-still + edge-tts VO mux   (unchanged)

Image gen (scene stills, product photoshoots)
  → Gemini Nano Banana Pro (existing)  OR
  → higgsfield generate create nano_banana_2  OR
  → higgsfield product-photoshoot create ...  (branded mode)

Thai voice-over
  → edge-tts                              (unchanged)

Subtitle / closing-tag overlays
  → HyperFrames                           (unchanged)
```

## Integration plan for the Python orchestrator

Build a thin wrapper at `src/auto_affi/adapters/higgsfield_cli.py`
that subprocess-wraps `higgsfield generate create` with `--wait` +
`--json`. ~80 LOC.

Schema-wise: add ONE generator value `Generator.HIGGSFIELD_CLI` with
an optional `model: str` field on `AiShot` to pick which Higgsfield
model handles the shot. This is more flexible than enumerating
HIGGSFIELD_DOP / HIGGSFIELD_TRANSITION / SEEDANCE_2_FAST / etc. —
the model is just a string passed through to the CLI.

Pre-existing `Generator.SEEDANCE_2_FAST` / `SEEDANCE_2_PRO` enum
values + the `seedance2.py` PiAPI adapter stay in tree as a fallback
path for environments without Higgsfield access.

## Smoke-test status

Running now (background task bmuao51uf):
- Model: `seedance_2_0`
- Prompt: PD300X mic, slow 30-degree orbit revealing the maono wordmark
- Mode: fast · Resolution: 720p · Aspect: 9:16 · Duration: 5s
- Reference: `data/registry/items/28875679676/product-refs/pd300x-hero-clean.jpg`

Will validate:
1. CLI auto-upload of the local image
2. Wait flag actually blocks
3. JSON output shape (for the wrapper)
4. Mic identity preserved in the generated motion
5. Credit cost per clip at Fast/720p tier

## References

- CLI repo: https://github.com/higgsfield-ai/cli
- CLI docs: https://higgsfield.ai/cli
- Skills bundle: https://higgsfield.ai/skills
- MCP server: https://higgsfield.ai/mcp (still registered, redundant
  now that CLI is available)
- Previous routing learning:
  `.aegis/brain/learnings/2026-05-15-higgsfield-seedance2-stack-routing.md`
- Previous MCP-only learning:
  `.aegis/brain/learnings/2026-05-15-higgsfield-mcp-integration.md`
