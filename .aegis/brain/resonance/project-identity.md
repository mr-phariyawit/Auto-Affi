# Project Identity -- Auto-Affi

## Core

- **Name**: Auto-Affi
- **Purpose**: Autonomous AI marketing platform that scouts Shopee products, creates Thai-native 9:16 vertical videos, publishes to social platforms with affiliate links, collects metrics, and self-improves through an LLM Wiki feedback loop.
- **One-line**: "AI Marketing Company operating 24/7 -- product discovery to video to revenue to learning"
- **Owner**: mr.phariyawit@gmail.com
- **Created**: 2026-05-13
- **Framework**: AEGIS v12.0
- **Agents**: 10 Marvel characters (v9 consolidation)
- **Profile**: full

## Domain

- **Market**: Thailand -- Shopee affiliate marketing
- **Content format**: Premium 9:16 vertical video (IG Reels, FB Reels, YouTube Shorts)
- **Language**: Thai-native (no transliteration, native Thai UX)
- **Niche (Phase 1)**: Beauty products
- **Revenue model**: Shopee affiliate commission via subId-tagged deep links

## North-Star KPIs

| KPI | Phase 1 Target | Phase 3 Target |
|-----|---------------|---------------|
| Videos produced / day | 5 | 100+ |
| Cost / video | <= $3.32 | <= $0.80 |
| Avg CTR on affiliate link | >= 1.5% | >= 4% |
| Affiliate GMV / month | $1k | $50k+ |
| Human intervention rate | <= 30% | <= 5% |

## Tech Stack

- **Language**: Python 3.12+
- **AI**: Claude (Opus 4.7 reasoning, Sonnet 4.6 throughput, Haiku 4.5 fast)
- **Video**: kie.ai (Veo/Sora/Flux/Suno), FFmpeg, Hyperframe
- **TTS**: ElevenLabs (primary), Botnoi (regional Thai), Azure (fallback)
- **Orchestration**: Temporal Workflows
- **Data**: Postgres + pgvector + ClickHouse + S3/R2
- **Observability**: Langfuse + OpenTelemetry + Phoenix
- **CI**: GitHub Actions

## Architecture Principles

1. **Agent hierarchy, not peer mesh** -- strict handoff chain, no agent-to-agent side channels
2. **Schema-validated boundaries** -- every agent handoff is Pydantic-validated
3. **Bilateral wiki sync** -- agents write to review queue only, Safety promotes to canonical
4. **Cost-aware** -- per-node budget caps, circuit-breakers, fallback recipes
5. **Thai-first** -- all scripts, captions, and content in native Thai

## Phase Structure

- **Phase 0** (now): PM setup, repo skeleton, docs, AEGIS bootstrap
- **Phase 1** (Week 1-6): Single closed loop -- Beauty niche, 5 video/day, GMV >= $200/14d
- **Phase 2** (Week 7-14): Multi-platform + portfolio, Writers' Room full team
- **Phase 3** (Week 15-24): Self-improving autonomous, harness-evolver, MoM CTR uplift >= 5%
