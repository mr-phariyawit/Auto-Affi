# Cost Model -- Per-Node Budgets, Circuit-Breakers, Fallback Recipes

> Source: SPEC.md sections 3.5.1, 9.1, 11.3, Appendix C
> Last synced: 2026-05-13
> Purpose: Every agent must respect cost constraints. This file defines
> the exact budget caps, circuit-breaker triggers, and fallback paths.

## Phase 1 Per-Video Cost Breakdown (SPEC Appendix C)

| Item | Est. Cost USD |
|------|--------------|
| Scout + Strategist LLM | $0.05 |
| Writer LLM | $0.10 |
| Editor agent (token, capped) | $0.30 |
| 8 scenes x image gen | $0.25 |
| Video gen (Veo) | $1.80 |
| TTS (60s) | $0.18 |
| ASR (Whisper, self-hosted) | $0.02 |
| Hyperframe overlays render | $0.05 |
| Compose + storage | $0.05 |
| Publish API | ~$0 |
| Metrics + wiki write | $0.07 |
| **Total target** | **<= $2.87** |

Note: SPEC 1.2 says "<= $3/video" for Phase 1, "<= $0.80/video" for Phase 3.
The $2.87 breakdown in Appendix C gives $0.13 headroom under the $3 target.

## Circuit-Breakers

### Editor Agent Token Cap (SPEC 3.5.1)
- **Trigger**: Claude token cost > $0.40 per video at editor stage
- **Action**: Stop AI editing. Fall back to deterministic FFmpeg recipe.
- **Rationale**: Editor is the most token-hungry stage. Capping it prevents cost blowout.

### Daily Budget Controller (SPEC 9.1)
- **Trigger**: daily cost > budget * 1.1
- **Action**: Auto-stop generation. Alert team.
- **Human escalation**: Human must approve budget increase or accept halt.

### Cost Alert (SPEC 11.3)
- **Trigger**: cost/video > target * 1.5 (i.e., > $4.31 in Phase 1)
- **Action**: Dashboard alert. Does not auto-stop but flags for review.

### Platform API Rate Limit (SPEC 9.1)
- **Trigger**: API rate limit hit
- **Action**: Queue requests. Reduce throughput. Do not retry aggressively.

### GPU Budget (SPEC 9.1)
- **Trigger**: GPU budget running low
- **Action**: Reduce throughput (fewer videos/day, not lower quality)

## Fallback Recipes

| When | Instead of | Use |
|------|-----------|-----|
| Editor token cap exceeded | AI-driven editing | Deterministic FFmpeg recipe (cut/concat/overlay) |
| Veo 3 outage | Veo 3 video gen | Runway Gen-3 or Kling (Phase 2+; Phase 1 = queue) |
| ElevenLabs outage | ElevenLabs TTS | Azure TTS fallback |
| Image gen over budget | Flux/Imagen per scene | Stock footage + Ken Burns effect |
| Daily budget exceeded | Continue generation | Halt and alert |

## Phase 3 Cost Target

$0.80/video requires:
- Cost-aware planner that auto-chooses cheapest-adequate generator per scene
- Prompt caching reducing LLM costs by ~60%
- Self-hosted Whisper (already planned) keeping ASR near-zero
- Volume discounts on video gen APIs
- More efficient prompts from learning loop refinement

## Per-Tool Cost Tracking (SPEC 8.2)

Every agent tool response includes `cost_usd` and `latency_ms`.
The Feedback Curator uses this to track cost/quality correlation at the tool level.
This enables data-driven decisions about which tools to use per scene.
