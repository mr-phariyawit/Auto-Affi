# Image-model benchmark snapshot — 2026-11-06 (boards dated Nov 2, 2026)

Source pages fetched by a research subagent (all [PROBED ✓] unless noted): arena.ai text-to-image, image-edit (single), image-edit/multi-image-edit, company/leaderboard-changelog; artificialanalysis.ai text-to-image + editing boards; OpenRouter `/api/v1/images/models` (62 models) + endpoint pricing.

## arena.ai — Multi-Image Edit (the board that matches our 2-face + pose-ref job)
| # | Model | Score |
|---|---|---|
| 1 | GPT-Image-2.5 Sunburst | 1522 |
| 2 | GPT-Image-2.5 Flare | 1476 |
| 3 | GPT-Image-2 | 1454 |
| 4 | GPT-Image-2.6 Flare (prelim) | 1439 |
| 5 | Gemini Nano Banana 2.1 | 1431 |
| 6 | Krea 3 Ultra | 1426 |
| 7 | Seedream 5.0 Pro | 1412 |
| 8 | Muse Image (Meta) | 1399 |
Nano Banana Pro #10–11 (1365/1363).

## arena.ai — Single Image Edit: Sunburst 1517, Flare 1482, GPT-Image-2.6 Sunburst 1476, MAI-Image-2.7-Preview 1469 (no public API), GPT-Image-2.6 Flare 1462, GPT-Image-2 1460, Grok Imagine 2.0 1438, NB 2.1 1427. Seedream 5.0 Pro #14, NB Pro #16, FLUX.2 max #37.
## arena.ai — Text-to-Image: Sunburst 1427, GPT-Image-2.6 Sunburst 1409, Flare 1399, 2.6 Flare 1384, GPT-Image-2 1382, MAI-Image-2.6 1331, NB 2.1 1325, Grok 2.0 1317.
## Artificial Analysis — Editing: Sunburst 1199, MAI-2.7-Preview 1195, Flare 1182, Krea 3 Ultra / NB 2.1 1152, Seedream 5.0 Pro 1129, FLUX 3 1120, NB Pro 1109.

Change since 2026-10-06 snapshot: Sunburst/Flare still #1/#2 everywhere; new entrants GPT-Image-2.6 (Nov 4, scores BELOW 2.5), MAI-Image-2.7-Preview (Oct 27), Nano Banana 2.1 (Oct 6, 14 refs / 4 characters), Krea 3 Ultra (Oct 15), FLUX 3 Image (Oct). Seedream 5.0 Pro pushed to #14 single / #7 multi.

## OpenRouter `/api/v1/images` availability (dedicated image models; NOT in `/api/v1/models`)
| Model | Max refs | Price |
|---|---|---|
| openai/gpt-image-2.5-sunburst / -flare, gpt-image-2.6-*, gpt-image-2 | 16 | $8/M img-in, $5/M txt, $30/M img-out tokens (≈ $0.09–0.12/image at quality high) |
| google/gemini-nano-banana-2.1 | 14 | $30/M img-out tokens |
| google/gemini-3-pro-image (NB Pro) | 14 | $2/M in, $120/M out |
| bytedance-seed/seedream-5-0-pro | 14 | $0.045/img ($0.09 hi-res) |
| krea/k3-edit | 8 | $0.03/img ($0.06 2K) |
| black-forest-labs/flux-3-image | 10 | $0.041–0.07/img |
Not on OpenRouter: MAI-Image-2.7, Kling, Midjourney.

## Verdict
Keep **gpt-image-2.5-sunburst** for identity-preserving multi-ref work. Cheap A/B candidate: **nano-banana-2.1**. No board measures face-identity fidelity directly — our own two-face test is the real check.

## Addendum 2026-11-07 — own A/B on the low-angle duo shot
Same prompt + 3 refs through OpenRouter `/api/v1/images`. Sunburst $0.086 / 1152×1536; Nano Banana 2.1 $0.061 / 1792×2400 (`resolution: "2K"`). Sunburst followed the mannequin camera and the lighting brief; NB 2.1 drifted toward eye level and flat light but rendered both faces at least as close to the refs. Details: `output/musician-shoot/duo/review-r1.md` (round 4 A/B).
