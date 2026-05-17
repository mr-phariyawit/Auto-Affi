# Auto-Affi Pipeline — Current Workflow (v13, 2026-05-17)

This is the reference diagram for the production pipeline as it stands
after concept-2-v5 / final v13 shipped. The workflow is **Higgsfield-only
for all video generation**; HeyGen / PiAPI / Phaya legacy branches are
preserved in code as dormant fallbacks.

Source-of-truth artifacts:
- Orchestrator: [`scripts/produce-ai-storyboard.py`](../scripts/produce-ai-storyboard.py)
- Schema: [`src/auto_affi/schemas/ai_storyboard.py`](../src/auto_affi/schemas/ai_storyboard.py)
- Higgsfield adapter: [`src/auto_affi/adapters/higgsfield_cli.py`](../src/auto_affi/adapters/higgsfield_cli.py)
- Storyboard example: `data/registry/items/<item_id>/concept-N-vM/storyboard.json` (gitignored — per-product)
- Routing decision: [`.aegis/brain/learnings/2026-05-16-higgsfield-only-workflow-plan.md`](../.aegis/brain/learnings/2026-05-16-higgsfield-only-workflow-plan.md)

```mermaid
flowchart TD
    %% ========== INPUTS ==========
    subgraph INPUTS[" INPUTS "]
        SB["📜 concept-N-vM/storyboard.json<br/>AiStoryboard v2 schema<br/>(7 shot cards · consistency_seed)"]
        REFS["🖼️ Refs<br/>characters/&lt;persona&gt;-hero.jpg<br/>product-refs/&lt;sku&gt;-*.jpg"]
        MUSIC_BRIEF["🎵 music_prompt<br/>(or pre-staged music.mp3)"]
        ENV["🔑 .env<br/>GOOGLE_API_KEY · GCS_BUCKET<br/>HEYGEN_API_KEY (dormant)<br/>PHAYA_API_KEY (legacy)"]
        HFAUTH["🪪 Higgsfield OAuth<br/>(local CLI token,<br/>not in .env)"]
    end

    %% ========== ORCHESTRATOR ==========
    SB --> ORCH[/"⚙️ scripts/produce-ai-storyboard.py<br/>5-phase orchestrator"/]
    REFS --> ORCH
    ENV --> ORCH
    HFAUTH --> ORCH

    %% ========== PHASE 1: STILLS ==========
    ORCH --> P1
    subgraph P1["PHASE 1 · Stills (per shot)"]
        P1_GEMINI["Gemini Nano Banana Pro<br/>image_prompt + ref_lock + negatives<br/>→ sN_image.jpg"]
    end

    %% ========== PHASE 2: SHOT DISPATCH ==========
    P1 --> P2DEC{{"PHASE 2 · Per-shot<br/>dispatch by Generator"}}

    P2DEC -->|"higgsfield_cli<br/>(default video path)"| HF_CLI
    P2DEC -->|"hold<br/>(static B-roll + VO)"| HOLD
    P2DEC -->|"heygen_avatar_iv<br/>(dormant)"| HEYGEN
    P2DEC -->|"seedance_2_fast/pro<br/>(fallback)"| PIAPI
    P2DEC -->|"seedance_2kf<br/>(legacy)"| PHAYA_SD

    subgraph HF_CLI["higgsfield_cli branch"]
        HF_PREP["Resolve refs:<br/>--image (1-img) OR<br/>--start-image + --end-image (2-kf)"]
        HF_PREP --> HF_RUN["higgsfield generate create<br/>&lt;model&gt; --wait"]
        HF_RUN --> HF_MODEL{{"model = ?"}}
        HF_MODEL -->|product motion| HF_SD["seedance_2_0<br/>($0.75/5s Fast)"]
        HF_MODEL -->|named camera| HF_CS["cinematic_studio_3_0<br/>(DoP presets)"]
        HF_MODEL -->|silent wide| HF_VEO["veo3_1_lite<br/>(1080p T2V)"]
        HF_MODEL -->|narrative motion| HF_KLING["kling3_0<br/>(physics + audio)"]
        HF_SD --> HF_DL["Download URL<br/>→ sN_higgsfield_raw.mp4"]
        HF_CS --> HF_DL
        HF_VEO --> HF_DL
        HF_KLING --> HF_DL
    end

    subgraph HOLD["hold branch"]
        HOLD_TTS{{"audio_source<br/>= phaya_tts?"}}
        HOLD_TTS -->|yes| EDGE_TTS["edge-tts<br/>th-TH-NiwatNeural<br/>→ sN_vo.wav"]
        HOLD_TTS -->|silence/music| HOLD_NULL["anullsrc silent track"]
        EDGE_TTS --> HOLD_FF["ffmpeg loop-still + apad<br/>→ sN_clip.mp4"]
        HOLD_NULL --> HOLD_FF
    end

    subgraph HEYGEN["heygen branch (dormant)"]
        HG_TTS["edge-tts → wav"] --> HG_UPLOAD["Upload still + audio<br/>→ asset_ids"]
        HG_UPLOAD --> HG_RENDER["create_video_from_image<br/>(Avatar IV)"]
        HG_RENDER --> HG_DL["Download mp4"]
    end

    subgraph PIAPI["PiAPI fallback"]
        PIAPI_UP["GCS-sign start+end frames"] --> PIAPI_CALL["seedance-2 first_last_frames"]
    end

    subgraph PHAYA_SD["Phaya 1.5 legacy"]
        PHAYA_UP["GCS-sign frames"] --> PHAYA_CALL["create_seedance_video"]
    end

    %% ---- normalize ----
    HF_DL --> NORM["_normalize_mp4()<br/>h264 yuv420p + AAC 192k/44.1/2ch<br/>cap to shot.duration_s"]
    HOLD_FF --> NORM
    HG_DL --> NORM
    PIAPI_CALL --> NORM
    PHAYA_CALL --> NORM

    NORM --> CLIPS["📁 sN_clip.mp4<br/>(7 normalized clips)"]

    %% ========== PHASE 3-5 ==========
    CLIPS --> P3["PHASE 3 · Concat<br/>ffmpeg -f concat -c copy<br/>→ concat.mp4"]
    P3 --> P4{{"PHASE 4 · Music"}}
    P4 -->|"music.mp3 in workdir?"| P4_REUSE["📦 reuse"]
    P4 -->|"missing"| P4_GEN["Phaya text_to_music<br/>→ music.mp3"]
    MUSIC_BRIEF -.-> P4_GEN
    P4_REUSE --> MIX["_mix_music_under()<br/>-12dB under VO<br/>→ mixed.mp4"]
    P4_GEN --> MIX

    MIX --> P5["PHASE 5 · Subtitles<br/>HyperFrames render +<br/>ffmpeg overlay filter chain"]

    subgraph CAPS["caption templates"]
        TPL_LOWER["dialogue-subtitle<br/>(lower-third, Sarabun)"]
        TPL_UPPER["dialogue-subtitle-upper<br/>(upper-third, Mitr Bold)"]
    end
    P5 --> TPL_LOWER
    P5 --> TPL_UPPER
    TPL_LOWER --> FINAL
    TPL_UPPER --> FINAL

    %% ========== OUTPUT + VALIDATE ==========
    FINAL["🎬 out/...-final-vN.mp4<br/>(28s · 720×1280 · ~7 MB)"]
    FINAL --> VAL{{"Validation"}}
    VAL --> V_HOOK["validate-hook.py<br/>MOTION / AUDIO_ONSET /<br/>TEXT_OVERLAY 3-of-3"]
    VAL --> V_DIFF["compare-finals.py<br/>vs prior baseline"]
    VAL --> GCS_UP["GCS upload<br/>orders/&lt;order_no&gt;/runs/&lt;run_no&gt;/final.mp4"]

    %% ========== EXTERNAL SERVICES (legend) ==========
    subgraph EXT["External services"]
        EXT_HF["🟢 Higgsfield (OAuth · Ultra)<br/>video gen"]
        EXT_GEM["🟢 Gemini API<br/>stills"]
        EXT_EDGE["🟢 edge-tts (free)<br/>Thai VO"]
        EXT_GCS["🟢 GCS<br/>storage + signed URLs"]
        EXT_HG["⚪ HeyGen (dormant)"]
        EXT_PIAPI["⚪ PiAPI (fallback)"]
        EXT_PHAYA["⚪ Phaya (legacy music/TTS)"]
    end

    classDef active fill:#0a3,stroke:#0f0,color:#fff
    classDef dormant fill:#444,stroke:#888,color:#ccc
    classDef phase fill:#246,stroke:#48a,color:#fff
    class HF_CLI,HOLD active
    class HEYGEN,PIAPI,PHAYA_SD dormant
    class P1,P3,MIX,P5 phase
```

## Per-shot decision flow (the inner loop)

Every shot in the storyboard goes through Phase 2's router once. The
flow inside one shot:

```mermaid
flowchart LR
    SHOT["shot N<br/>(AiShot pydantic model)"] --> GEN{{"shot.generator"}}

    GEN -->|hold| H["hold + edge-tts VO<br/>(free, fast)"]
    GEN -->|higgsfield_cli| HF["higgsfield_cli<br/>(default video path)"]
    GEN -->|heygen_avatar_iv| HG["heygen_avatar_iv<br/>(dormant)"]
    GEN -->|seedance_2_*| PI["seedance_2_fast/pro<br/>(PiAPI fallback)"]
    GEN -->|seedance_2kf| PH["seedance_2kf<br/>(Phaya 1.5 legacy)"]

    HF --> HFM{{"shot.higgsfield_model"}}
    HFM -->|seedance_2_0| MOD1["product motion · $0.75/5s"]
    HFM -->|cinematic_studio_3_0| MOD2["DoP presets · ~$1.00/5s"]
    HFM -->|veo3_1_lite| MOD3["silent wide · 1080p"]
    HFM -->|kling3_0| MOD4["physics + audio"]

    H --> NORM[normalize → sN_clip.mp4]
    MOD1 --> NORM
    MOD2 --> NORM
    MOD3 --> NORM
    MOD4 --> NORM
    HG --> NORM
    PI --> NORM
    PH --> NORM

    classDef active fill:#0a3,stroke:#0f0,color:#fff
    classDef dormant fill:#444,stroke:#888,color:#ccc
    class HF,H,MOD1,MOD2,MOD3,MOD4 active
    class HG,PI,PH dormant
```

## Cost model (28s · 7-shot ad)

| Layer | Per ad | Source |
|---|---|---|
| Higgsfield Seedance 2.0 Fast (5 motion shots × ~$0.65) | ~$3.30 | Ultra plan: $129/3000 credits = $0.043/credit |
| Gemini Nano Banana Pro stills (7) | ~$0.30 | Per-image rate |
| edge-tts Thai VO | $0 | Microsoft free service |
| HyperFrames captions | $0 | Local Chrome render |
| GCS storage | <$0.01 | Negligible per run |
| **Total** | **~$3.60** | Validated against v13 actuals |

At 30 ads/month: ~$108 in Higgsfield credits + ~$9 in Gemini + $0 everything else = **~$117/month** all-in for video production. Compares to v12 at ~$103.50 (had HeyGen at $1.20/ad for 2 lip-sync shots) — the +$13.50/month is the cost of consolidating to one credit pool / one OAuth.

## What's deliberately NOT in this diagram

- **soul-id training** — not yet wired into the orchestrator. When adopted, becomes a one-time `higgsfield soul-id create` step that produces a `soul_id` ref to attach to character-bearing shots, replacing per-product hero portraits.
- **Marketing Studio / Product Photoshoot / Marketplace Cards workflows** — Higgsfield high-level abstractions documented in the proposal but not wired into the per-shot pipeline.
- **The registry / Sheets layer** — separate concern from this run-time view (see `src/auto_affi/registry/`).
- **Compliance gate** — manual review step that runs against the final mp4 before GCS canonical upload.
