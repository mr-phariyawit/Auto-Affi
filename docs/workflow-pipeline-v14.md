# Auto-Affi Pipeline — Current Workflow (v14, 2026-05-18)

This is the reference diagram for the production pipeline after the
**variant-testing** flow shipped (plan
[`docs/superpowers/plans/2026-05-18-variant-testing-pipeline.md`](superpowers/plans/2026-05-18-variant-testing-pipeline.md),
spec
[`docs/superpowers/specs/2026-05-18-auto-affi-variant-testing-design.md`](superpowers/specs/2026-05-18-auto-affi-variant-testing-design.md)).

The unit of work is no longer a single ad — it is **one concept × N
hook variants**, sharing a common body+CTA backbone. HeyGen has been
removed entirely (commit `373bfac`); Higgsfield-CLI + HOLD are the only
two video generators in the per-shot decision flow.

> v13 ([`docs/workflow-pipeline-v13.md`](workflow-pipeline-v13.md)) is
> **superseded for new productions** but kept as the historical
> reference for the single-ad path (`scripts/produce-ai-storyboard.py`).
> That script is still wired and still works — use it when you need
> exactly one ad and not a 3-way test.

Source-of-truth artifacts:
- Orchestrator: [`scripts/produce-variant-set.py`](../scripts/produce-variant-set.py)
- Schema: [`src/auto_affi/schemas/ai_storyboard.py`](../src/auto_affi/schemas/ai_storyboard.py) (`ConceptVariantSet`)
- Shot renderers: [`src/auto_affi/pipeline/shot_renderers.py`](../src/auto_affi/pipeline/shot_renderers.py)
- Higgsfield adapter: [`src/auto_affi/adapters/higgsfield_cli.py`](../src/auto_affi/adapters/higgsfield_cli.py)
- Live concept example: `data/registry/items/<sku>/concepts/<concept_id>/{base.json,hooks/*.json,links.json,results.jsonl}` (gitignored — per-product)
- Pattern library: `data/patterns/winning-hooks.jsonl` (gitignored, append-only)

## Directory layout (concept × variants)

```
data/registry/items/<sku>/concepts/<concept_id>/
├── base.json                  body + CTA shots (s2..s6) shared across variants
├── hooks/
│   ├── a.json                 variant A — hook shots (s0+s1)
│   ├── b.json                 variant B — hook shots
│   └── c.json                 variant C — hook shots
├── links.json                 variant_id → Shopee sub_id mapping (written by orchestrator)
└── results.jsonl              per-variant Shopee dashboard pulls (append-only, deferred)

data/patterns/
└── winning-hooks.jsonl        cross-concept learning log (append-only, deferred)

out/<sku>-<concept>/
├── shared/                    rendered ONCE, reused across all variants
│   ├── s2_clip.mp4 … s6_clip.mp4
│   └── music.mp3              optionally pre-staged
├── variant-a/
│   ├── s0_clip.mp4, s1_clip.mp4    hook-specific
│   └── final.mp4                    assembled per-variant
├── variant-b/
└── variant-c/
```

`data/registry/` and `out/` are gitignored — git tracks the framework,
not per-product artifacts.

## 5-phase orchestrator (`produce-variant-set.py`)

```mermaid
flowchart TD
    %% ========== INPUTS ==========
    subgraph INPUTS[" INPUTS "]
        BASE["📜 base.json<br/>AiStoryboard (s2..s6: body + CTA)"]
        HOOKS["📜 hooks/{a,b,c}.json<br/>per-variant hook shots (s0+s1)"]
        REFS["🖼️ Refs<br/>characters/&lt;persona&gt;-hero.jpg<br/>product-refs/&lt;sku&gt;-*.jpg"]
        MUSIC_PRE["🎵 music.mp3 (pre-staged in shared/)<br/>or --music-path arg"]
        ENV["🔑 .env<br/>GOOGLE_API_KEY · AUTO_AFFI__GCS_BUCKET"]
        HFAUTH["🪪 Higgsfield OAuth<br/>(local CLI token)"]
    end

    %% ========== ORCHESTRATOR ==========
    BASE --> LOAD[/"load_variant_set()<br/>+ ConceptVariantSet validators<br/>(duration-parity, same-N-shots)"/]
    HOOKS --> LOAD
    LOAD --> PLAN[/"build_render_plan()<br/>shared_out_dir + variant_outputs"/]
    PLAN --> ORCH[/"⚙️ orchestrate_renders()<br/>4 render phases + persist links"/]
    REFS --> ORCH
    MUSIC_PRE --> ORCH
    ENV --> ORCH
    HFAUTH --> ORCH

    %% ========== PHASE 1: STILLS ==========
    ORCH --> P1
    subgraph P1["PHASE 1 · Stills (shared + per-variant)"]
        P1_BASE["Gemini Nano Banana Pro<br/>shared base shots<br/>→ shared/sN_image.jpg"]
        P1_VAR["Gemini Nano Banana Pro<br/>per-variant hook shots<br/>→ variant-X/sN_image.jpg"]
    end

    %% ========== PHASE 2: SHARED CLIPS (RENDER ONCE) ==========
    P1 --> P2
    subgraph P2["PHASE 2 · Shared shot clips (render ONCE)"]
        P2_LOOP["for shot in vs.base.shots:<br/>if exists → 📦 reuse<br/>else → _render_one_shot()"]
        P2_LOOP --> P2_OUT["📁 shared/s2..s6_clip.mp4<br/>(5 clips, body + CTA)"]
    end

    %% ========== PHASE 3: VARIANT CLIPS ==========
    P2 --> P3
    subgraph P3["PHASE 3 · Per-variant hook shots"]
        P3_LOOP["for vid, shots in vs.variants.items():<br/>for shot in shots:<br/>_render_one_shot()"]
        P3_LOOP --> P3_OUT["📁 variant-{a,b,c}/s0,s1_clip.mp4<br/>(2 clips × N variants)"]
    end

    %% ========== PHASE 4: ASSEMBLY ==========
    P3 --> P4
    subgraph P4["PHASE 4 · Per-variant assembly"]
        P4_CONCAT["concat_clips()<br/>[s0,s1 (variant)] + [s2..s6 (shared)]<br/>→ variant-X/concat.mp4"]
        P4_CONCAT --> P4_MIX["mix_music_under()<br/>music @ -12dB under VO<br/>→ variant-X/mixed.mp4"]
        P4_MIX --> P4_CAP["HyperFrames captions<br/>(dialogue-subtitle / -upper)<br/>→ variant-X/final.mp4"]
    end

    %% ========== PHASE 5: PERSIST LINKS ==========
    P4 --> P5
    subgraph P5["PHASE 5 · Persist links.json"]
        P5_LINKS["build_links_map()<br/>{variant_id → sub_id}<br/>→ concepts/&lt;id&gt;/links.json"]
    end

    P5 --> OUT["🎬 N × out/&lt;sku&gt;-&lt;concept&gt;/variant-X/final.mp4"]

    %% ========== DEFERRED MEASUREMENT (DASHED) ==========
    OUT -.->|"operator posts to TikTok Shop<br/>with per-variant sub_id"| SHOPEE["Shopee Affiliate dashboard<br/>72h attention window"]
    SHOPEE -.->|"manual CSV export<br/>(API intermittent)"| PULL[("scripts/pull-shopee-results.py<br/>⚠️ deferred — T12 stub")]
    PULL -.-> RESULTS["📝 concepts/&lt;id&gt;/results.jsonl<br/>(views/clicks/orders/CVR per variant)"]
    RESULTS -.-> COMPARE[("scripts/compare-variant-results.py<br/>⚠️ deferred — T13/T14")]
    COMPARE -.->|"winner by CVR<br/>(min 200 clicks)"| WINNERS["🏆 data/patterns/winning-hooks.jsonl<br/>cross-concept learning library"]
    WINNERS -.->|"author of next concept<br/>browses winning hook_types"| BASE

    %% ========== EXTERNAL SERVICES ==========
    subgraph EXT["External services"]
        EXT_HF["🟢 Higgsfield (OAuth · Ultra)<br/>video gen"]
        EXT_GEM["🟢 Gemini API<br/>stills"]
        EXT_EDGE["🟢 edge-tts (free)<br/>Thai VO"]
        EXT_GCS["🟢 GCS<br/>storage + signed URLs"]
        EXT_SHOPEE["🟡 Shopee Affiliate TH<br/>(CSV export · deferred)"]
    end

    classDef active fill:#0a3,stroke:#0f0,color:#fff
    classDef phase fill:#246,stroke:#48a,color:#fff
    classDef deferred fill:#553,stroke:#aa6,color:#fff,stroke-dasharray: 5 5
    class P1,P2,P3,P4,P5 phase
    class PULL,COMPARE,WINNERS,RESULTS,SHOPEE deferred
```

## Per-shot decision flow (the inner loop, simplified)

Every shot (base or variant) goes through the same per-shot router as
v13 — but the surface area is reduced. HeyGen / PiAPI / Phaya branches
are gone. Only **`higgsfield_cli`** and **`hold`** remain:

```mermaid
flowchart LR
    SHOT["shot N<br/>(AiShot pydantic model)"] --> GEN{{"shot.generator"}}

    GEN -->|hold| H["hold + edge-tts VO<br/>(free, fast)"]
    GEN -->|higgsfield_cli| HF["higgsfield_cli<br/>(only video gen)"]

    HF --> HFM{{"shot.higgsfield_model"}}
    HFM -->|seedance_2_0| MOD1["product motion<br/>~$0.65/5s @ 720p Fast<br/>(T11 live default)"]
    HFM -->|kling3_0 std| MOD2["physics + audio<br/>10 cr ≈ $0.43/5s<br/>(spec default — 57% cheaper)"]
    HFM -->|cinematic_studio_3_0| MOD3["DoP presets<br/>~$1.00/5s"]
    HFM -->|veo3_1_lite| MOD4["silent wide · 1080p"]

    H --> NORM[normalize → sN_clip.mp4]
    MOD1 --> NORM
    MOD2 --> NORM
    MOD3 --> NORM
    MOD4 --> NORM

    classDef active fill:#0a3,stroke:#0f0,color:#fff
    classDef removed fill:#400,stroke:#800,color:#888,stroke-dasharray: 3 3
    class HF,H,MOD1,MOD2,MOD3,MOD4 active
```

The model is chosen per-shot via the `higgsfield_model` field in the
storyboard JSON. The plan recommends `kling3_0` std as the new default
(57% cheaper than `seedance_2_0` Fast), but the live T11 run
(shure-vs-maono) used `seedance_2_0 @ 720p` per the concept author's
storyboard. **Both are supported** — `higgsfield_model` picks.

## Cost model (per concept = 3 variants)

Per spec section 8 + T11 actuals:

| Component | Shared? | Per concept |
|---|---|---|
| Stills × 7 × 3 variants (Gemini Nano Banana Pro) | per-variant | ~$0.42 |
| Body+CTA shots × 5 via Higgsfield @ 5s (shared) | YES | ~$2–3 |
| Hook shots × 2 × 3 variants via Higgsfield @ 5s | per-variant | ~$2.5–4 |
| edge-tts Thai VO | per-variant | $0 |
| HyperFrames caption overlays | per-variant | $0 |
| GCS storage | shared | <$0.01 |
| **Spec estimate (kling3_0 std)** | | **~$5.15** |
| **T11 actual (seedance_2_0 720p)** | | **~$6.00** |

T11 live validation (PD300X / shure-vs-maono, commit between `94ca148`
and now) produced 3 mp4s end-to-end for **~$6** total — vs naive "3
separate v13 ads" at $10.80 → **~44% savings** for the same 3-variant
output. The naive comparison is the more honest one because the 3
ads-vs-1 ad is a different unit; variant-testing replaces "ship one ad
and pray" with "ship three and measure".

Cost-per-variant works out to **~$2.00** — vs $3.60 for a v13 single
ad. The first variant is more expensive (it pays for the shared body
+ CTA renders), and each additional variant adds ~$0.86 marginal
(hook clips + assembly). The math favours 3-variant batches.

## Pattern-library learning loop (deferred)

Once the operator posts variants to TikTok / Shopee and accumulates
~72h of dashboard data:

```
results.jsonl  ──►  compare-variant-results.py  ──►  winning-hooks.jsonl
   ▲                                                      │
   │                                                      ▼
pull-shopee-results.py                          (author seeds next concept's
   ▲                                             hooks with proven hook_types
   │                                             + 1 experimental)
Shopee Affiliate dashboard (CSV or API)
```

`winning-hooks.jsonl` rows look like:
```json
{"ts":"2026-05-18","concept":"shure-vs-maono","winner":"b","hook_type":"price_comparison_text","hook_summary":"Side-by-side price text overlay","cvr":0.012,"sample_size":4280}
```

Author of next concept browses this file → seeds their 3 hook variants
with proven hook_types + 1 experimental. Knowledge compounds across
concepts instead of being lost to memory.

**Status: wiring deferred per spec section 10 step 5.** Neither
`pull-shopee-results.py` nor `compare-variant-results.py` exist yet —
the user directive is "no speculative measurement code before we know
the real Shopee API shape". T12/T13/T14 in the plan will wire these
once real `results.jsonl` data exists.

## What's deliberately NOT in this diagram

- **HeyGen / Avatar IV** — removed entirely in commit `373bfac` (Phase 1).
  The adapter, tests, lipsync driver script, `HEYGEN_AVATAR_IV` enum
  value, and dispatch branch are all gone. Recoverable via
  `git log --diff-filter=D` if ever needed.
- **PiAPI Seedance / Phaya 1.5 legacy branches** — still in the code
  for the v13 single-ad path but **not invoked by `produce-variant-set.py`**.
  The variant orchestrator only dispatches `higgsfield_cli` and `hold`
  (per spec — those are the only two generators needed for variant testing).
- **soul-id training** — not yet wired into either orchestrator.
- **Marketing Studio / Product Photoshoot / Marketplace Cards** —
  Higgsfield higher-level abstractions, not wired into the per-shot
  pipeline.
- **Registry / Sheets layer** — separate concern from this run-time view.
- **Compliance gate** — manual review step against each variant's
  final mp4 before TikTok-Shop upload.
- **Phase 5 measurement scripts** — see "Pattern-library learning loop"
  above. Deliberately deferred until real Shopee data exists.

## When to use v13 vs v14

| Situation | Pipeline |
|---|---|
| Shipping a single ad (no A/B/C test) | v13 — `scripts/produce-ai-storyboard.py` |
| Shipping a concept with 3 hook variants for testing | **v14 — `scripts/produce-variant-set.py`** |
| Backfilling old `storyboard.json` files | v13 (schema-compatible) |
| New product / new concept (default) | **v14** (variant-testing is the new default) |

v13 is **superseded** for new productions but is not deprecated — it
remains the right tool for one-off renders and is still tested. The
schema (`AiStoryboard`) is shared — `ConceptVariantSet` wraps it.
