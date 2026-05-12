# North-Star KPIs & Phase Gates

> Source: SPEC.md sections 1.2, 13
> Last synced: 2026-05-13
> Purpose: Every agent must know what "winning" looks like. This file is the
> quantitative definition of success at each phase.

## KPI Table (verbatim from SPEC 1.2)

| KPI | Phase 1 Target | Phase 3 Target |
|-----|---------------|----------------|
| Videos produced / day | 5 | 100+ |
| Cost / video (full pipeline) | <= $3.00 | <= $0.80 |
| Avg CTR on affiliate link | >= 1.5% | >= 4% |
| Affiliate GMV / month | $1k | $50k+ |
| Human intervention rate | <= 30% | <= 5% |
| Strategy improvement / month (CTR uplift) | -- | >= 5% MoM |

Note: The last row (MoM CTR uplift >= 5%) is a Phase 3 KPI only. It measures
self-improvement velocity -- whether the learning loop is actually making the
system smarter over time.

Sustainability caveat (Loki review): The 5% MoM target applies at Phase 3 start.
CTR improvement has diminishing returns -- going from 1.5% to 4% over 6 months
is ~17% MoM, but sustaining 5% MoM after reaching 4% hits a ceiling (~6-8% for
top organic performers in Thai Beauty). Expect this KPI to taper naturally. It is
a velocity signal, not a perpetual mandate.

## Phase Exit Gates (hard gates -- do not advance without meeting these)

### Phase 1 Exit (Week 6)
- Beauty niche only (single niche)
- 5 video/day sustained for 3+ consecutive days
- GMV >= $200 over any rolling 14-day window
- At least 1 full loop complete: scout -> strategy -> write -> produce -> publish -> collect metrics -> wiki write
- Exit criteria quote (SPEC 13, Phase 1): "1 video krop loop, auto-publish, auto-collect metric, auto-write wiki entry"

### Phase 2 Exit (Week 14)
- Full Writers Room (5 sub-agents + critic) operational
- Multi-vendor video gen adapter live (Veo + at least 1 fallback)
- Publishing to FB Reels + IG Reels + YT Shorts
- Wiki tiering system + knowledge graph layer operational
- Safety agent online and blocking pre-publish violations

### Phase 3 Success State (Week 24)
- 100+ videos/day
- Cost <= $0.80/video
- CTR >= 4%
- GMV >= $50k/month
- MoM CTR uplift >= 5% (learning loop proving itself)
- Human intervention <= 5%
- Multi-account, multi-niche scaling active
- Offline replay + automatic prompt promotion running

## Operational SLOs (SPEC 9.2)

| SLO | Target |
|-----|--------|
| Discovery cycle freshness | < 6h |
| Brief -> published video | P50 < 90 min, P95 < 6h |
| Metrics polling lag | < 5 min |
| Wiki update lag (after outcome) | < 24h |
| Pipeline success rate | >= 95% |

## How agents use this file

- **Strategist / Scout**: optimize for CTR and GMV targets
- **Producer / Editor**: optimize for cost/video target
- **Feedback Curator**: measure MoM CTR uplift as primary success metric
- **Nick Fury (AEGIS)**: use phase gates to determine when to advance scope
- **All agents**: human intervention rate is a team metric -- minimize escalations
