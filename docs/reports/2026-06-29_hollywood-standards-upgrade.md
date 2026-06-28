I now have the ground truth. The PGA gate is real and strong, but critically it has **no `prompt_mode` field and no i2v/FLF2V mismatch check** — the exact bug all 5 teams flagged. The Scene schema has free-text `shot_type`/`movement`/`visual_prompt` with no mode lock, no product-state, no hero-proof contract. This makes my recommendations precise. Let me produce the consolidated plan.

# Auto-Affi Hollywood-Standard Upgrade Plan — Nick Fury Consolidation

*Synthesized from 5 teams (Research/Production-QA · Marketing · Creative · Production · Audit). Grounded against the live code: `src/auto_affi/schemas/storyboard.py` (Scene/Storyboard) and `src/auto_affi/pipeline/prompt_audit.py` (PGA gate). The PGA gate is strong on identity/compliance/determinism but has **zero prompt-mode awareness** — the precise hole behind the i2v garble and the no-drip anti-message.*

---

## 1. TOP 10 Studio-Grade Standards Auto-Affi Must Adopt

1. **i2v Prompt Discipline** — i2v prompts lead with `[Motion]+[Camera]+[Action]`, never re-describe the static image; FLF2V/still prompts are a different field and must never be reused on i2v calls. `[Production, Audit, Marketing]`
2. **Prompt-Mode ↔ Generator Lock** — every scene declares `prompt_mode` (image_to_video / first_last_frame / video_gen) and the audit blocks any mode that doesn't match its generator. `[Production, Marketing, Creative]`
3. **Product State Machine + Hero-Proof Visual Contract** — every product scene names the exact use-state and what the camera MUST show (water flowing AWAY from a no-drip sleeve), so the claim cannot render as its opposite. `[Production, Marketing, Audit]`
4. **Storyboard + Shot List Duality** — a visual storyboard is insufficient alone; each panel needs a text shot-list entry (movement type, lens, lighting, mode). `[Research-QA, Creative]`
5. **Save-the-Cat / PAS Beat-to-Second Mapping** — 24s = Hook(0–2s)/Agitate(2–8s)/Demo(8–18s)/CTA(18–24s), each beat tagged with its emotional pillar. `[Marketing, Creative]`
6. **Shot-Grammar Lexicon** — named shot sizes (ECU/CU/MS/WS/EWS), angles, and movement families replace ad-hoc prose like "camera moves." `[Creative, Production]`
7. **Continuity Tokens + 180° / Continuity Bible** — `WORLD|CHAR|WARD|LOC|CAM|TIME|PROP|PRODUCT` tokens on every prompt; eyeline/screen-direction locked across multi-scene runs. `[Production, Creative]`
8. **Emotion Pillar Gate (≥4.0 each / ≥4.3 avg)** — Wonder/Thrill/Curiosity/Fun/Heart scored per scene before generation (the 2026-06-06 standard, currently unenforced). `[Marketing, Creative]`
9. **Post-Generation Verification Audit** — systematic motion-physics + message-coherence + consistency spot-check + `ffprobe` deliverable QC + safe-zone check before assembly. `[Research-QA, Audit, Creative]`
10. **Pre-Production Research / Reference Board** — benchmark hook + hero angle against 5–10 Thai TikTok Shop winners before any storyboard. `[Research-QA, Marketing]`

---

## 2. GAP Table (gap · severity · which recent failure it maps to)

| # | Gap | Severity | Maps to recent failure |
|---|-----|----------|------------------------|
| G1 | No `prompt_mode` field anywhere; PGA `ReferenceManifest` has no mode field and `audit()` never checks mode-vs-generator | **High** | **i2v garble** — FLF2V prompts reused on i2v → junk motion (thumbnail looked fine) |
| G2 | No product state machine / hero-proof contract; `Scene.visual_prompt` is free text, no claim-vs-visual assertion | **High** | **No-drip rendered as water pouring OUT** (anti-message) |
| G3 | Scene schema has no shot-grammar, lighting, blocking, or coverage fields (`shot_type`/`movement` are free strings) | **High** | Inconsistent/ad-hoc shots; vague "camera moves"; weak motion |
| G4 | Emotion Pillar standard (2026-06-06) exists but is **not** a gate; no per-scene pillar field | **High** | Emotionally flat clips pass; "looks bad" stays subjective |
| G5 | Storyboard HTML review gate is advisory, not code-blocking (`Storyboard.approve()` has no DRAFT→APPROVED state machine) | **High** | **Ton run skipped storyboard review**, jumped straight to Veo |
| G6 | No beat-to-second / PAS mapping; `ScenePurpose` enum exists but no timing or emotional-job binding | **High** | Incoherent pacing; agitation too weak to convert |
| G7 | No continuity tokens / 180° / continuity bible for ≥3-scene runs | Med | Character/product/location drift across shots |
| G8 | No post-gen verification: no motion-physics check, no `ffprobe` QC, no safe-zone QC, no brand-visual-conflict scan | Med | Garbled motion + anti-message caught only by eyeball, late |
| G9 | No pre-production research / reference board; no Thai TikTok Shop format codification | Med | Hooks/hero angles not benchmarked to Thai winners |
| G10 | No audio mastering (LUFS/true-peak), color-grade, or product-image input spec | Low | Inconsistent loudness/look; poor i2v input images |

---

## 3. Prioritized Upgrade Backlog (ordered by impact/effort)

| Rank | Action | Exact file / skill / checklist to edit | Expected impact |
|------|--------|----------------------------------------|-----------------|
| **1** | Add `prompt_mode: Literal["image_to_video","first_last_frame","video_gen"]` to `Scene`; add `prompt_mode` + i2v-language detector to `ReferenceManifest`; new `AuditCode.PROMPT_MODE_MISMATCH` that fails when mode≠generator OR i2v prompt contains FLF2V language ("between frames","last frame","interpolate","transition to") | `src/auto_affi/schemas/storyboard.py` (Scene); `src/auto_affi/pipeline/prompt_audit.py` (`ReferenceManifest`, `AuditCode`, `audit()`, `prompt_hash()`) | **Kills the #1 failure (i2v garble) at the gate.** Highest impact, low effort — extends an existing enforced audit. |
| **2** | Add `product_state` + `hero_proof_contract` (what camera MUST show / MUST NOT show) to `Scene`; PGA fails a `product`-kind manifest in HOOK/DEMONSTRATE without a proof contract; flag anti-message keywords | `src/auto_affi/schemas/storyboard.py` (Scene); `src/auto_affi/pipeline/prompt_audit.py` (new `AuditCode.HERO_PROOF_MISSING` / `PRODUCT_ANTI_MESSAGE`) | **Prevents no-drip→water-pouring class.** Makes the claim machine-checkable pre-gen. Low effort. |
| **3** | Hard-block storyboard approval: extend PGA's existing `STAGES`/`assert_may_generate` so `storyboard` stage requires the storyboard.html-equivalent approval before `contact_sheet`/`video`; document the gate as MANDATORY | `skills/produce-affiliate-video.md` (Step 4.5 → hard gate); `src/auto_affi/pipeline/prompt_audit.py` (already has stage ordering — wire storyboard sign-off into it) | **Makes "skip storyboard, jump to Veo" impossible.** Reuses the existing append-only approval machinery — low effort, high $ protection. |
| **4** | Add beat fields to `Scene`: `beat_name`, `beat_start_s`, `beat_end_s`, `emotion_pillar`; Storyboard validator warns if Agitate>6s or beats non-contiguous | `src/auto_affi/schemas/storyboard.py` (Scene + new `model_validator`) | Locks PAS pacing + emotional job per scene. Medium effort, structural fix for weak-hook/weak-agitation. |
| **5** | Emotion Pillar gate: per-scene 5-pillar scores; block storyboard approval if any pillar <4.0 or avg <4.3 | new `src/auto_affi/pipeline/emotion_gate.py` + `skills/produce-affiliate-video.md` Step 3.5 | Enforces the already-written 2026-06-06 standard. Medium effort. |
| **6** | Shot-Grammar Lexicon skill + replace free-text `shot_type`/`movement` with enums (ECU/CU/MS/WS/EWS; pan/tilt/push/dolly/track/crane) + `lighting` (key ratio, temp) field | new `skills/shot-grammar-lexicon.md`; `src/auto_affi/schemas/storyboard.py` (Scene) | Consistent visual language; kills vague "camera moves" → stronger motion. Medium effort. |
| **7** | Continuity tokens on every prompt + linter; mandatory continuity bible (character/location/camera/prop) for ≥3-scene runs; bind into `prompt_hash` | new `skills/continuity-token-schema.md` + `tools/continuity-token-linter.py`; `prompt_audit.py` | Stops cross-shot drift. Medium effort. |
| **8** | Post-gen audit suite: `tools/ffprobe-qc.sh` (1 audio stream, 1080×1920, 30fps, duration±50ms), `tools/safe-zone-qc` (TikTok 900×1492 / IG 996×1400), motion-physics + brand-visual-conflict spot-check | new `tools/` + `skills/produce-affiliate-video.md` post-gen gate | Catches garble/anti-message/overlap before publish. Medium effort. |
| **9** | Pre-production research + reference/mood board templates; Thai TikTok Shop format standard (problem/result in first 3s, product-in-motion, hook rotation) | `docs/PRE_PRODUCTION_RESEARCH_PHASE.md`, `docs/THAI_TIKTOK_SHOP_FORMAT_STANDARD.md`, `docs/REFERENCE_BOARD_TEMPLATE.md` | Anchors hooks to proven Thai winners. Higher effort, slower payoff. |
| **10** | Audio mastering spec (TikTok/IG true-peak ≤−1dB, VO −14dBFS, music −18dBFS), color-grade spec, product-still input spec (≥1080p, sRGB, focus) | `docs/audio-mastering-spec.md`, `docs/color-mastering-spec.md`, `docs/PRODUCT_VISUAL_STANDARDS.md` | Polish/consistency. Lowest impact now. |

---

## 4. TOP 5 Do-NOW Changes (before the next paid generation)

These five are the minimum to not repeat the i2v-garble, anti-message, and skipped-review failures. **The first three are code/gate changes in already-enforced files — do them before any paid Veo call.**

1. **Add `prompt_mode` + i2v-language guard to the PGA.** Edit `Scene` (`prompt_mode`) and `ReferenceManifest`+`audit()` in `prompt_audit.py` with `AuditCode.PROMPT_MODE_MISMATCH`. Block if generator is i2v but the prompt re-describes the static image or carries FLF2V words ("between/last frame","interpolate","transition to"). *Directly closes the garble bug at the gate that already runs.*

2. **Require a hero-proof + product-state contract for every product scene.** Add `product_state` + `hero_proof_contract` to `Scene`; PGA fails a product HOOK/DEMONSTRATE scene without one. *Stops "no-drip → water pouring out."*

3. **Make storyboard approval a hard block.** Wire the storyboard-HTML sign-off into the existing `STAGES`/`assert_may_generate` ordering so `video` cannot run until `storyboard` is human-approved. *Makes the Ton-run skip impossible — zero paid frames without sign-off.*

4. **Adopt the i2v Prompt Craft rule + Beat/Emotion tagging in the workflow doc.** Update `skills/produce-affiliate-video.md`: separate i2v vs FLF2V prompt fields, require beat-to-second map (Hook/Agitate/Demo/CTA) and a 5-pillar emotion tag per scene before generation. *Fixes weak motion + weak hook at authoring time.*

5. **Ship the Pre-Generation Audit Checklist** (one page, signed by producer+creative lead before any paid gen):
   - [ ] **Prompt mode matches generator** (i2v prompt is motion-forward, NOT re-describing the image; no FLF2V language reused)
   - [ ] **Hero claim cannot be misread** — proof contract names what camera MUST show; anti-message ruled out (no-drip ≠ water out)
   - [ ] **Motion is specified** — named camera move (dolly/pan/push), one move per shot, not "camera moves"
   - [ ] **Beat-to-second + emotion** — Hook≤2s, Agitate present, CTA in last beat; each scene tags its pillar (≥4.0)
   - [ ] **Continuity tokens present** (`WORLD|CHAR|WARD|LOC|CAM|TIME|PROP|PRODUCT`) + seed/soul-id locked
   - [ ] **Storyboard.html human-approved** (hard gate) before any paid call

---

**You are here:** Research consolidated → upgrade plan delivered. Next action in the chain is to land **Do-NOW items 1–3** (the three PGA/schema code edits in `storyboard.py` + `prompt_audit.py`) as the first commit before the next paid generation — they are the load-bearing fixes and reuse machinery that is already enforced.

**Verification status:** This plan is `[PRODUCED: unverified]` analysis grounded in two files I read directly (`storyboard.py`, `prompt_audit.py`) — those confirm the i2v/mode gap and the free-text Scene fields are real. The team findings themselves were not re-verified; treat the source teams' "gaps" as their claims, not independently re-confirmed by me. No code was changed in this task.