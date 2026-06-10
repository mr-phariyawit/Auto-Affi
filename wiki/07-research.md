# 07 — Research Docs Index

> 16 ไฟล์ใน [`docs/research/`](../docs/research/) — แบ่งเป็น 4 กลุ่ม: Prompt Engineering, Provider/API, Strategy, Org Design

## Prompt Engineering & Continuity

### [AI Video Prompt Lock Research](../docs/research/ai-video-prompt-lock-research-2026-06-06.md) (2026-06-06)
ระบบ prompt รักษา identity/location/product/camera ข้ามฉาก — lock 5 layers: character passport, location map, camera atlas, continuity tokens, reference images · "Prompt Continuity Bible" ก่อนทุก multi-scene run · Nano Banana Pro = keyframe reference prompt / Seedance = motion prompt เท่านั้น

### [Prompt Lock V5.1 Addendum](../docs/research/ai-video-prompt-lock-research-2026-06-06-v5-1-addendum.md) (2026-06-06)
จาก isolated shot prompts → **"locked world model"** สำหรับ 100+ scenes — 4 lock layers (World/Identity/Map/Shot) · scene prompt import locked IDs แล้วอธิบายเฉพาะ action ใหม่ · Prompt Continuity Architect block provider call ถ้า token ขาด → ฐานของ [Scene-Scale Standard](06-principles.md)

## Provider / API Reference



"Skill chooses the workflow. Model renders the media." — 7-layer selection stack · 1 lead skill + ≤3 support · repeat 3 ครั้ง → สร้าง custom skill · Tier 1: Product Analyzer, Seedance Director, Storyboard Cheatcode, UGC Ad Production ฯลฯ


**167 models** + machine-readable [`kie_market_models_2026-06-03.json`](../docs/research/kie_market_models_2026-06-03.json)/[`.csv`](../docs/research/kie_market_models_2026-06-03.csv) (generate โดย [`scripts/kie_market_catalog.py`](09-scripts-reports.md)) · 1 credit ≈ $0.005 · media 14 วัน · rate ≤20 req/10s

### [ElevenLabs v3 Options Playbook](../docs/research/elevenlabs-v3-options-playbook-th-2026-06-05.md) (2026-06-05)

## Strategy / Vision

### [Hollywood-Grade Marketing Film Studio Playbook](../docs/research/hollywood-grade-marketing-film-studio-playbook-th-2026-06-04.md) (TH) / [EN](../docs/research/hollywood-grade-marketing-film-studio-playbook-2026-06-04.md) (2026-06-04)
Founder playbook 4-layer model (Agency+Production+Studio+IP) · 20 principles (Human Truth first, Brand structurally necessary, Director Treatment = creative contract, **Brand Remove Test**) · 12-phase pipeline · budget bands spec $20k–150k → Hollywood $500k–5M+ · SAG-AFTRA 2025 AI consent rules · ACES pipeline

### [Hollywood Studio Research Swarm Synthesis](../docs/research/hollywood-studio-research-swarm-synthesis-2026-06-04.md) (2026-06-04)
12-lane research → 3-stage growth: **affiliate/performance studio → premium brand film → owned IP** · moat = commercial intelligence + taste + craft network · Thailand: 491 foreign productions ปี 2024, cash rebate สูงสุด 30% · connected document system (Project ID ผูก brief→deliverable)

### [Benchmark Talent & Company Target Map](../docs/research/benchmark-talent-company-target-map-2026-06-04.md) (2026-06-04)
Recruiting radar — near-term: Thai/SEA partners (Phenomena Bangkok, Greenlight Films, Yggdrazil, Kantana Post) ก่อน apex names · first advisor = commercially experienced craft leader ไม่ใช่คนดังสุด

Screenwriting + camera grammar + lighting recipes — lock 5 อย่างก่อน generate (story intent, product role, visual grammar, lighting motivation, production control) · **Brand Remove Test ต้อง fail** ถ้า plot เดินได้โดยไม่มีสินค้า · one camera move per shot · Thai captions composite ใน post เท่านั้น + spec ละเอียดของ `seedance_2_0`/`marketing_studio_video`/`cinematic_studio_3_0`

## Org Design / Workflow OS

### [24/7 Subagent Team Blueprint](../docs/research/auto-affi-24-7-subagent-team-blueprint-th-2026-06-04.md) (2026-06-04)
ทีม 16 subagents — queue lifecycle 13 ขั้น · fail-closed safety sidecar · trend score formula · ฐานของ [data registry](04a-data-registry.md) 12 CSVs

### [Systematic Workflow Upgrade Blueprint](../docs/research/auto-affi-systematic-workflow-upgrade-blueprint-th-2026-06-04.md) (2026-06-04)
จาก one-shot generator → **15-stage workflow OS** · profiles: `thai_affiliate_30s_master` (default), `15s_cutdown`, `premium_brand_commercial`, `product_broll_pack`, `static_marketplace_pack` · 10 QA gates (G0–G10) · run folder structure (variants/, publish/, metrics/) · subId taxonomy 5 levels

---
[← Principles](06-principles.md) | [HOME](HOME.md) | [Runs →](08-runs.md)
