# Auto-Affi Variant-Testing Pipeline — Design

**Date:** 2026-05-18
**Status:** SPEC — pending user review before plan generation
**Supersedes:** the v13 single-ad-per-concept workflow at
`docs/workflow-pipeline-v13.md`
**Origin:** brainstorming-skill session 2026-05-17/18 with Approach B
selected ("Variant Testing")

## 1. Goal

Build the cheapest possible per-concept video pipeline that
**measurably** increases purchase conversions for Thai TikTok-Shop /
Shopee-Live affiliate ads. The system's primary success metric is
**CVR (conversion rate)** — the proportion of viewers who reach the
affiliate link and complete a purchase — not views, likes, shares,
brand impressions, or production volume.

The previous pipeline (v1-v13) optimized for "ads that look like they
convert" without measuring whether they actually do. This rewrite
closes the loop: ship N variants per concept → measure → learn → reuse
winning patterns on the next product.

## 2. Hard constraints (user-stated, non-negotiable)

1. **No HeyGen.** The adapter, tests, dispatch branch, env check, and
   enum value are deleted. Higgsfield's lip-sync gap for Thai is
   sidestepped by the existing "mouth-closed VO+caption" reframe from
   the v13 storyboard.
2. **Higgsfield-only for video generation.** All video shots route
   through `higgsfield generate create <model>` via the CLI wrapper
   already in tree (`src/auto_affi/adapters/higgsfield_cli.py`).
3. **Gemini API direct where it's cheaper.** Currently this is stills
   only (Imagen 4 Fast at $0.02 vs Higgsfield's nano_banana_2 at
   $0.09). For video, empirical CLI cost probes show Higgsfield Ultra
   is cost-competitive with Gemini direct, so Higgsfield wins on
   single-pane-of-glass.
4. **Conserve Higgsfield credits.** Default video model flips from
   `seedance_2_0 Fast 720p` (17.5 cr / 5s = $0.75) to
   **`kling3_0` std** (10 cr / 5s = $0.43, 57% cheaper AND native
   1080p AND has audio). Shared shots across variants render exactly
   once.

## 3. Non-goals (deliberately out of scope)

- Multi-language ads (Thai-only for now).
- Auto-posting to TikTok / Shopee — human posts each variant with the
  affiliate-link wired in.
- Live-commerce flow / Shopee Live integration.
- Persona-locked single-creator-account strategy (Approach C — may
  fold in later if data justifies it).
- Real-time A/B optimization / auto-rotation.
- CTA / body variant testing (deferred — MVP is hook-variants only).

## 4. The unit of work — concept and variants

- A **concept** = one product (SKU) × one creative angle. Example:
  `28875679676 × shure-vs-maono` means "Maono PD300X / price-drama
  vs Shure".
- A **variant** = one storyboard for that concept where the **opening
  hook (first 1-2 shots) differs**; body + CTA shots are SHARED across
  variants of the same concept.
- N = **3 variants** per concept by default. (2 = too noisy a winner
  signal; 5 = costs more than the learning is worth at MVP volume.)

### Why hook-only variants for MVP

- The hook is the highest-leverage point in the storyboard — 70% of
  algorithmic distribution decisions happen in the first 3 seconds
  (TTSVibes 2025 research, captured in
  `.aegis/brain/learnings/2026-05-15-affiliate-conversion-creative.md`).
- Hook-variants share 5 of 7 shots → 60% cost savings vs naive "3
  separate ads".
- A single experimental dimension (hook) gives the cleanest causal
  signal. Multi-dimensional variants (hook × CTA × body) explode the
  sample-size requirement.

CTA-variant and body-variant testing are FUTURE extensions, gated on
hook-variant testing actually working.

## 5. Directory layout

```
data/registry/items/<sku>/concepts/<concept_id>/
├── base.json                  body + CTA shots (s2-s6) shared across variants
├── hooks/
│   ├── a.json                 variant A — hook shots (s0+s1)
│   ├── b.json                 variant B — hook shots
│   └── c.json                 variant C — hook shots
├── links.json                 variant_id → Shopee sub_id mapping
└── results.jsonl              per-variant Shopee dashboard pulls (append-only)

data/patterns/
└── winning-hooks.jsonl        cross-concept learning log (append-only)

out/<sku>-<concept>/
├── shared/                    rendered once, reused across all variants
│   ├── s2_clip.mp4
│   ├── s3_clip.mp4
│   ├── s4_clip.mp4
│   ├── s5_clip.mp4
│   └── s6_clip.mp4
├── variant-a/
│   ├── s0_clip.mp4, s1_clip.mp4    hook-specific
│   └── final.mp4                    assembled
├── variant-b/
└── variant-c/
```

`data/registry/` and `out/` are gitignored — git tracks the framework,
not per-product artifacts.

## 6. Schema additions

`src/auto_affi/schemas/ai_storyboard.py`:

```python
class ConceptVariantSet(BaseModel):
    """A concept with N hook variants sharing a body+CTA base."""
    concept_id: str
    item_id: int
    base: AiStoryboard            # contains shots s2..s6 (body + CTA)
    variants: dict[str, list[AiShot]]  # {"a": [s0, s1], "b": [...], "c": [...]}
    # validators: every variant must have same number of shots as the base
    # expects, total duration of base + variant must hit target_total_duration
```

Existing `AiStoryboard` stays for the single-ad path
(`produce-ai-storyboard.py` keeps working). The variant orchestrator
operates on `ConceptVariantSet`.

## 7. Components

### 7a. `scripts/produce-variant-set.py` (NEW)

The new orchestrator. Phases:

1. **Load + validate** `ConceptVariantSet` from `base.json` +
   `hooks/*.json`.
2. **Stills phase** — Gemini Imagen / Nano Banana Pro for every shot
   in every variant. Stills are cheap (~$0.02 ea), so generate fresh
   per variant rather than try to share.
3. **Shared-shot render phase** — render shots `s2..s6` of the base
   ONCE via Higgsfield Kling 3.0 std. Cache under `out/<sku>-<concept>/shared/`.
4. **Variant-shot render phase** — for each variant, render only the
   hook shots `s0..s1` via Higgsfield. Cache under
   `out/<sku>-<concept>/variant-<x>/`.
5. **Variant-specific CTA bake** — the s6 closing-tag overlay is
   re-rendered per variant with that variant's affiliate-link text
   (via HyperFrames — cheap, deterministic, local).
6. **Per-variant assembly** — for each variant, concat
   `variant-<x>/s0,s1 + shared/s2..s5 + variant-<x>/s6` → music mix
   → caption overlay → `out/<sku>-<concept>/variant-<x>/final.mp4`.
7. **Persist `links.json`** — variant_id → sub_id (per-concept Shopee
   affiliate parameter).

### 7b. `scripts/pull-shopee-results.py` (NEW)

- Inputs: concept directory.
- Reads `links.json`.
- Pulls Shopee Affiliate dashboard data per sub_id (API if available;
  manual CSV import fallback — Shopee Affiliate TH API is intermittent).
- For each variant: views, clicks, orders, revenue, CVR.
- Appends to `results.jsonl`.
- Cadence: run 72h after first post (Thai TikTok-Shop typical
  attention window).

### 7c. `scripts/compare-variant-results.py` (NEW)

- Inputs: concept directory.
- Reads `results.jsonl` (latest pull).
- Declares winner by highest CVR with minimum sample-size threshold
  (default: 200 clicks per variant). Below threshold → "no winner
  declared; need more data".
- Appends winner to `data/patterns/winning-hooks.jsonl` with hook-type
  metadata.

### 7d. Pattern library — `data/patterns/winning-hooks.jsonl`

Append-only learning log:

```json
{"ts":"2026-05-18","concept":"shure-vs-maono","winner":"b","hook_type":"price_comparison_text","hook_summary":"Side-by-side price text overlay","cvr":0.012,"sample_size":4280}
```

Author of next concept browses this file → seeds their 3 hook variants
with proven hook_types + 1 experimental. Compounds knowledge over
time.

## 8. Cost model (per concept = 3 variants)

| Component | Shared? | Per concept |
|---|---|---|
| Stills × 7 × 3 variants (Gemini Imagen 4 Fast batch) | per-variant | ~$0.42 |
| Body+CTA shots × 5 via Kling 3.0 std @ 5s | YES | 50 cr ≈ $2.15 |
| Hook shots × 2 × 3 variants via Kling 3.0 std @ 5s | per-variant | 60 cr ≈ $2.58 |
| edge-tts Thai VO | per-variant | $0 |
| HyperFrames caption overlays | per-variant | $0 |
| **Total per 3-variant concept** | | **~$5.15** |

Compared to v13 cost of $3.60 for 1 ad, this produces 3 testable
variants for $5.15 — a 1.43x cost multiplier for 3x the data.

Compared to naive "3 separate v13 ads" at $10.80, this is **52%
cheaper** for the same 3-variant output.

## 9. HeyGen removal (cleanup task, done as part of this work)

Delete:
- `src/auto_affi/adapters/heygen.py`
- `scripts/heygen-lipsync-clips.py`
- `tests/unit/test_heygen_adapter.py`
- `Generator.HEYGEN_AVATAR_IV` enum value
- The `heygen_avatar_iv` dispatch branch in
  `scripts/produce-ai-storyboard.py`
- The `HEYGEN_API_KEY` env-check stanza

Keep:
- Archived v9 final mp4 in `archive/` (gitignored anyway).
- Git history of the adapter (recoverable via `git log --diff-filter=D`).

## 10. Migration sequence

1. Remove HeyGen (cleanup).
2. Add `ConceptVariantSet` schema + tests.
3. Add `produce-variant-set.py` orchestrator + tests.
4. Build a real concept-3-v1 against PD300X to validate the
   end-to-end variant flow (no Shopee posting yet — just produce 3
   mp4s and confirm shared-shot reuse worked).
5. Add `pull-shopee-results.py` + `compare-variant-results.py` once
   the user has tried posting variants and has at least one
   results.jsonl with real data.
6. Update `docs/workflow-pipeline-v13.md` → `docs/workflow-pipeline-v14.md`
   reflecting the variant flow.

## 11. Error handling

- If 1 variant fails mid-render (e.g. Higgsfield transient empty-output
  bug), ship the other 2. Partial concepts still produce learnings.
- If Shopee dashboard pull fails, retry with exponential backoff,
  then defer.
- If affiliate-link generation fails (Shopee Affiliate API down),
  abort the variant set — can't measure without unique sub_ids.
- All errors logged to `data/registry/items/<sku>/concepts/<concept>/errors.log`.

## 12. Testing

- Unit tests for `ConceptVariantSet` schema validation (per-variant
  shot count = base's hook-slot count, total duration matches).
- Mocked Higgsfield CLI test for `produce-variant-set.py` — verify
  shared shots are dispatched exactly once across 3 variants.
- Mocked Shopee dashboard test for `pull-shopee-results.py`.
- Live integration test = run against PD300X concept-3-v1, confirm
  3 mp4s + `links.json` produced for ~$5.

## 13. Open questions (to resolve before invoking writing-plans)

None — all design questions resolved during brainstorming. User
selected Approach B, default-model swap to Kling 3.0 std, and
HeyGen-removal scope autonomously per the recommended path.

## 14. References

- Brainstorming session: this conversation, 2026-05-17/18
- Previous workflow: `docs/workflow-pipeline-v13.md`
- Cost data (empirical CLI probes): captured in this conversation
  2026-05-17
- Affiliate-conversion research:
  `.aegis/brain/learnings/2026-05-15-affiliate-conversion-creative.md`
- Higgsfield-only routing decision:
  `.aegis/brain/learnings/2026-05-16-higgsfield-only-workflow-plan.md`
- Higgsfield CLI gateway:
  `.aegis/brain/learnings/2026-05-15-higgsfield-cli-unified-gateway.md`
