# Higgsfield via MCP — Integration Path

**Date:** 2026-05-15
**Supersedes:** the "Higgsfield API key" External-access queue item.
The original plan (sign up Plus tier → API key → custom Python
adapter at `src/auto_affi/adapters/higgsfield.py`) is obsolete.
**Now:** Higgsfield is reached via its hosted MCP server, OAuth-based,
no API key to manage.

## Endpoint

```
https://mcp.higgsfield.ai
```

Transport: HTTP. Auth: OAuth via Higgsfield account (browser sign-in
on first use). No bearer tokens / API keys in `.env`.

## Registration

Already done at the project level:

```bash
claude mcp add --transport http higgsfield https://mcp.higgsfield.ai
```

This writes to `~/.claude.json` under the project entry for
`/Users/phariyawit.jiap/Documents/Auto-Affi`. The server appears in
`claude mcp list` and shows "Failed to connect" until OAuth is
completed.

## Activation (user-side, one-time)

1. In the Claude Code session, run `/mcp` slash command (or restart
   the session). The MCP UI surfaces unauthenticated servers and
   prompts a browser OAuth flow.
2. Sign in with Higgsfield account.
3. After OAuth completes, `claude mcp list` shows ✓ Connected and
   Higgsfield tools become available to Claude in conversation as
   `mcp__higgsfield__*` tool names.

## What MCP gives us vs the REST-adapter path

| Concern | REST adapter (was queued) | MCP (chosen) |
|---|---|---|
| Auth | Plus tier signup + API key in `.env` | OAuth account login, no `.env` |
| Code surface | ~150 LOC adapter + tests + schema enum | Zero adapter code — tools available to Claude directly |
| Per-call cost | Same Higgsfield credits ($0.05-0.30/clip) | Same |
| Conversational use | Manual `requests` calls or wrapper script | Direct tool invocation in any Claude session |
| Batch / scheduled use | First-class | Requires a Claude session running |
| Billing exposure | API key spend risk | OAuth session-scoped |

## Routing rule (updated)

The earlier routing decision (Higgsfield for macro product shots +
B-roll transitions) is unchanged in INTENT; only the EXECUTION
mechanism shifts:

- Macro product shot with named camera move (Crash Zoom / Dolly /
  Orbit / Bullet Time) → **call Higgsfield MCP tool** from this
  conversation rather than POST to `https://gateway.pixazo.ai/...`
- B-roll cinematic transition (17 effects) → same — MCP tool call
- Keep HeyGen Avatar IV for talking-head, edge-tts for Thai VO,
  HyperFrames for overlays, Gemini for stills

For storyboards that need Higgsfield-generated clips:
1. Author the AiStoryboard v2 JSON as usual
2. For shots with `generator: higgsfield_dop` (schema extension still
   pending), I call the MCP tool directly in this session, download
   the result clip, drop it into the workdir under the expected
   `{shot_id}_clip.mp4` name
3. Run `produce-ai-storyboard.py --skip-stills --skip-shots` to
   reuse the pre-staged Higgsfield clip + render captions + concat +
   music

This sidesteps the need to add a `HIGGSFIELD_DOP` enum + adapter
branch in the orchestrator (since the orchestrator never calls
Higgsfield programmatically — I do it through MCP in chat). The
orchestrator only needs to know "this shot's clip is already
pre-staged, skip it" — which `--skip-shots` already covers.

The schema extension for `HIGGSFIELD_DOP` / `HIGGSFIELD_TRANSITION`
Generator values is therefore **optional** — useful for declarative
storyboard authoring but not load-bearing for the MCP path.

## What stays in the human queue

- **PiAPI signup for Seedance 2.0** — still relevant. Seedance 2.0
  doesn't have an MCP server (only PiAPI / Atlas Cloud / fal.ai /
  Replicate REST APIs). The Seedance 2.0 adapter committed in
  `src/auto_affi/adapters/seedance2.py` remains the right path for
  that generator.

## Smoke-test plan (once OAuth completes)

In a fresh Claude Code session:

1. List available Higgsfield MCP tools (Claude will surface them as
   `mcp__higgsfield__*`)
2. Generate one test clip using DoP I2V with "crash-zoom-in" preset +
   the PD300X product reference at
   `data/registry/items/28875679676/product-refs/pd300x-hero-clean.jpg`
3. Download the result, sanity-check the motion (does it match the
   preset? Is the mic identity preserved?)
4. If quality acceptable, build concept-2-v4 storyboard with 3 shots
   pre-staged from Higgsfield (s0/s3/s5 macros) and the rest of the
   v3 flow

## References

- https://higgsfield.ai/mcp — official MCP setup page
- Routing decision: `.aegis/brain/learnings/2026-05-15-higgsfield-seedance2-stack-routing.md`
- Resolved queue item: `Higgsfield.ai API key (DoP + Transitions...)`
  in `.aegis/brain/human-queue.md`
