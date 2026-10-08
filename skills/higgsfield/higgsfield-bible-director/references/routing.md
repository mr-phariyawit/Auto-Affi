# Task routing

Select by requested deliverable, not every keyword. One specialist is usually enough; add continuity or QC when the task genuinely requires it. Shared artifacts stay in the same run and retain IDs/version.

| Task | Skill | Load source IDs on demand |
|---|---|---|
| End-to-end or mixed workflow | higgsfield-bible-director | B1, B4, B13, E1, E4 |
| References / identity / product shape / states | higgsfield-asset-continuity | A01.03, A06.02, A06.03, A06.05, A06.06, A06.08, B1, B2, B3, D3 |
| Reuse what worked / cost per kept take / known failures | higgsfield-recipe-ledger | B7, B13 |
| Review a generated take (measure + frames + rubric, KEEP/REROLL/FIX-BRIEF) | higgsfield-dailies-review | B7, A05, A16.02 |
| Actually generate on Higgsfield / live credit price (UI via Claude in Chrome, gated) | higgsfield-operator (+ gate_cli) | B13, A07 |
| Seedance video prompt writing / prompt review before spend | higgsfield-seedance-prompt (+ its lint_prompt.py) | B5, A01.05, A10, A16 |
| Film / ad / dialogue / action | higgsfield-cinematic-direction | A01, A02, A10, B5, B7, B8, B9, C1.2 |
| Animated style continuity | higgsfield-cinematic-direction | A04, D6, E1 |
| Car / road / doors / dialogue selection | higgsfield-cinematic-direction | A15, B3, B5, E2 |
| Fight / scale / transformation / impact | higgsfield-cinematic-direction | A16, B5, B7, C1.2 |
| Existing footage edit / VFX / crop / upscale | higgsfield-vfx-footage | A03, A13, B6, D1 |
| Logo / product family / packaging / campaign | higgsfield-brand-visuals | A09, B11, D4 |
| Channel / explainer / localization / shorts | higgsfield-faceless-channel | A11, A12, B12, D5 |
| Playable game / GDD / input / publish plan | higgsfield-game-production | A14, B13 |
| Demo evidence / dailies / export / failure diagnosis | higgsfield-production-qc | A05, A08, B7, B10, C1.3, C2.3, D6, E3, E4 |
| Service / offer / client / portfolio / economics | higgsfield-agency-operations | A07, B11, B13, D2, D7 |
| Auto-Affi new product production | existing auto-affi-new-product-clip + appropriate Bible specialist | A06, B11, D2, E1, E5 |

The helper accepts exact Bible v2 IDs, not ranges (v1 B–E IDs are invalid). For A06 lessons select the needed individual IDs (A06.02 … A06.09) or the A06 course. `--list` shows all IDs. Avoid loading an entire course if one small lesson answers the request.

Execution adapter rules:
- Higgsfield generation: use `higgsfield-operator` (UI route behind the PGA gate + credit cap); never click Generate outside it.
- User asks CUA: use CUA for browser interactions and read the current browser documentation.
- API/SDK: read the current installed Higgsfield API client or provider integration skill; do not translate marketing course menus into guessed endpoints.
- Existing media-edit/faceless/UGC production skill: use its actual supported workflow; the Bible specialist supplies creative criteria.
- Existing HyperFrames/rendering/voice skill: load it only when the requested output requires that implementation.
- Tool missing: return a concrete draft/plan and name the unavailable execution step; never report it as generated.

No default model override, background scheduler or automatic agent fan-out is part of this package.
