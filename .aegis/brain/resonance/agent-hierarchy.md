# Agent Hierarchy -- Hollywood Writers' Room Pattern

> Source: SPEC.md sections 3.1-3.9, 4, Appendix A
> Last synced: 2026-05-13
> Purpose: Define the agent crew, their roles, handoff chain, and the
> debate-then-Director-decides pattern that governs creative decisions.

## The Pattern: Hollywood Writers' Room (SPEC 3.4)

The Writers Room is modeled after a Hollywood production. Multiple
specialized agents debate, then the Director makes the final call.
This is NOT consensus -- it is structured disagreement followed by
authority.

## Agent Crew (Production Pipeline Order)

### 1. Product Scout Agent (SPEC 3.1)
- **Role**: Find Shopee products with viral potential + good commission
- **Inputs**: trending keywords from Trend Analyst, win/fail history from Wiki
- **Output**: `ProductCandidate` (10-50 per cycle) with score
- **Scoring rubric**: price band, commission %, rating, sales velocity, review sentiment, novelty vs saturated wiki

### 2. Trend Analyst Agent (SPEC 3.2)
- **Role**: Mine viral signals from TikTok / Reels / Shorts / Threads
- **Output**: `TrendSignal { hook_pattern, audio_id, hashtags, format, lifecycle_phase }`
- **Cadence**: every 6 hours
- **Phase**: Not in Phase 1 (Phase 2+)

### 3. Strategist Agent (SPEC 3.3)
- **Role**: Matchmaker -- product x trend x audience persona -> campaign brief
- **Output**: `CampaignBrief { product_id, target_persona, angle, hook, cta, success_hypothesis, expected_ctr }`
- **Critical rule**: MUST query LLM Wiki for anti-patterns before confirming
- **Hard rules** (from Appendix A): Hook within 1.5s, single CTA, max 2 product features
- **Forbidden**: medical claims, "guaranteed" language, comparative claims without source

### 4. Writers' Room (SPEC 3.4) -- Multi-Agent Panel

| Sub-agent | Role | Authority |
|-----------|------|-----------|
| **Director** | Tone, pacing, emotional arc | FINAL DECISION (debate ends here) |
| **Screenwriter** | Dialogue / VO script (Thai-native), <= 60 seconds | Creative lead |
| **Cinematographer** | Shot list, framing 9:16, lighting, b-roll cues | Visual lead |
| **Storyboard Artist** | Storyboard JSON + reference image prompts per scene | Technical creative |
| **Sound Designer** | Music bed (royalty-free), SFX, voice characteristics | Audio lead |
| **Critic** | Red-team: weaknesses, brand-risk, claim compliance, repetitive patterns | Adversarial |

**Decision protocol**: Agents debate. Critic challenges. Director decides.
No voting. No consensus. Director is accountable for the final Storyboard.

**Output**: `Storyboard` schema (SPEC 6.2)

### 5. Producer Agent (SPEC 3.5) + Editor Sub-agent (SPEC 3.5.1)
- **Role**: Asset Pipeline Orchestrator
- **Decisions**: which generator per scene (Veo 3 / Runway / Kling / stock)
- **Voice selection**: ElevenLabs / Azure / OpenAI TTS
- **Composition**: FFmpeg + Hyperframe + Remotion -> master 9:16 1080x1920, 30fps, <= 60s, <= 100MB
- **Editor sub-agent**: AI video editor with MCP-style tools
  - Standard passes: silence trim, filler cut, auto-subtitle, hook punch-in, brand overlay, CTA endcard
  - Cost gate: $0.40/video max at editor stage, fallback to deterministic FFmpeg

### 6. Publisher Agent (SPEC 3.6)
- **Role**: Optimal posting time, caption/hashtags per platform, affiliate link via system link-shortener
- **Output**: `PublishRecord`

### 7. Analytics Collector Agent (SPEC 3.7)
- **Role**: Poll metrics at 1h/6h/24h/7d/30d intervals
- **Metrics**: views, likes, shares, saves, comments, watch-time, CTR, conversions, GMV
- **Storage**: ClickHouse + Postgres `metrics_timeseries`

### 8. Feedback Curator Agent (SPEC 3.8)
- **Role**: Batch every 24h, compare win (top 20%) vs fail (bottom 20%)
- **Output**: `WikiEntry` -- structured patterns + updated embeddings
- **Marks stale patterns as deprecated** (anti-wiki-rot)

### 9. Supervisor / Safety Agent (SPEC 3.9)
- **Role**: Pre-publish guardrails -- always-on
- **Checks**: copyrighted music, misleading claims, prohibited categories, brand safety
- **Authority**: Hard-block + escalate to human if threshold exceeded
- **Phase**: Not in Phase 1 (Phase 2+)

## Handoff Chain (Pipeline Order)

```
Scout -> Strategist -> Writers Room -> Producer/Editor -> Safety -> Publisher -> Analytics -> Feedback Curator -> Wiki -> (next cycle)
```

Every arrow is a Pydantic-validated handoff. No free-form data crossing boundaries.

## Model Assignment (SPEC 3)

- **Opus 4.7**: reasoning-heavy agents (Strategist, Director, Critic, Feedback Curator)
- **Sonnet 4.6**: throughput agents (Scout, Screenwriter, Cinematographer, Publisher)
- **Haiku 4.5**: fast/simple tasks (tool routing, metric formatting)
