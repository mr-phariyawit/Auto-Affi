# Learning Loop -- LLM Wiki & Self-Improvement

> Source: SPEC.md sections 5.1-5.4, 3.8, 11.2
> Last synced: 2026-05-13
> Purpose: The learning loop is the heart of the system -- it makes every
> agent smarter from experience. This file captures how it works so every
> agent knows how to read from and write to the shared brain.

## Why This Exists (SPEC 5)

> "The heart of the system -- makes every agent smarter from its own experience."

Without the learning loop, every pipeline run starts from zero context.
With it, the system accumulates knowledge: what hooks work, what products
convert, what patterns fail, what audiences respond to.

## Wiki Structure (SPEC 5.1)

Two layers:

### A. Vector Store (pgvector) -- Semantic Recall
- Table: `wiki_entries(id, namespace, content_md, embedding vector(1536), tags, tier, created_at, deprecated_at)`
- Namespaces:
  - `hook_pattern` -- what opening hooks work
  - `product_archetype` -- product types that convert well
  - `audience_persona` -- audience segments and their preferences
  - `failure_mode` -- things that consistently fail
  - `anti_pattern` -- patterns to actively avoid
  - `platform_norm` -- platform-specific conventions
  - `compliance_rule` -- regulatory requirements

### B. Knowledge Graph (Postgres relational) -- Causal/Structural
- Tables: `pattern_nodes` + `pattern_edges (cause -> effect, weight, evidence_count)`
- Purpose: answer "WHY does X work?" not just "X works"
- Phase: Not in Phase 1 (Phase 2+)

## Entry Tiers (SPEC 5.2) -- Anti-Wiki-Rot

| Tier | Criteria | How Agents Use It |
|------|----------|-------------------|
| **Hypothesis** | 1-2 evidence points | Injected as "tentative" hint -- agents may override |
| **Validated** | >= 5 evidence, p < 0.1 | Normal context -- agents should follow |
| **Canonical** | >= 20 evidence, replicated cross-niche | Hard rule -- agents MUST follow |
| **Deprecated** | Contradicted by >= 3 recent fails | Excluded from retrieval entirely |

## Feedback Loop Mechanics (SPEC 5.3)

1. **Outcome labeling**: Each video gets label after 7 days:
   `{breakout, hit, neutral, flop, banned}`
2. **Counterfactual extraction**: Feedback Curator asks: "What made this
   video flop when the brief is similar to other hits?"
3. **Pattern mining**: LLM + statistical test (chi-squared / lift) on
   feature columns
4. **Wiki write**: New entry + evidence IDs cited
5. **Context injection**: Next cycle, agents do retrieval-augmented
   prompting from wiki before reasoning

## Anti-Catastrophic-Forgetting (SPEC 5.4)

- **Exemplar set**: Canonical wins preserved permanently
- **Offline replay**: Periodically re-run Strategist on historical briefs,
  compare output with ground truth. Alert if divergence is high.
- This prevents the system from "forgetting" what works as new patterns accumulate.

## Agent Evaluation Harness (SPEC 11.2)

- **Offline replay**: Old briefs -> new agent -> compare with actual outcome
- **Golden set**: 100 hand-curated cases that must not regress
- **A/B traffic split**: 90% prod prompt / 10% candidate prompt
- **Auto-promote**: If candidate uplift > threshold (p < 0.05), auto-promote to prod

## How Agents Interact with the Wiki

- **Reading**: All agents do retrieval-augmented prompting from wiki before reasoning
- **Writing**: Only Feedback Curator writes new entries (batch, every 24h)
- **Promoting**: Safety agent or human promotes from review queue to canonical
- **Deprecating**: Feedback Curator marks stale patterns (contradicted by recent data)
- **Never**: Direct writes to canonical tier by any agent (bilateral wiki sync principle)
