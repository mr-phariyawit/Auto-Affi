# Task routing

Select by requested deliverable, not every keyword. One specialist is usually enough; add continuity or QC when the task genuinely requires it. Shared artifacts stay in the same run and retain IDs/version.

| Task | Skill | Load source IDs on demand |
|---|---|---|
| End-to-end or mixed workflow | higgsfield-bible-director | B1, B2, B8, E2 |
| References / identity / product shape / states | higgsfield-asset-continuity | A01.03, A06.02–09, B3, B4 |
| Film / ad / dialogue / action | higgsfield-cinematic-direction | A01, A02, A10, B5–B7 |
| Animated style continuity | higgsfield-cinematic-direction | A04, D6 |
| Car / road / doors / dialogue selection | higgsfield-cinematic-direction | A15, B4, B5 |
| Fight / scale / transformation / impact | higgsfield-cinematic-direction | A16, C1 |
| Existing footage edit / VFX / crop / upscale | higgsfield-vfx-footage | A03, A13, D7 |
| Logo / product family / packaging / campaign | higgsfield-brand-visuals | A09, B3 |
| Channel / explainer / localization / shorts | higgsfield-faceless-channel | A11, A12, D9, D10 |
| Playable game / GDD / input / publish plan | higgsfield-game-production | A14, B9 |
| Demo evidence / dailies / export / failure diagnosis | higgsfield-production-qc | A05, A08, C1–C7, D11 |
| Service / offer / client / portfolio / economics | higgsfield-agency-operations | A07, C7 |
| Auto-Affi new product production | existing auto-affi-new-product-clip + appropriate Bible specialist | A06, E1–E8 |

The helper accepts exact IDs, not ranges. For A06.02–09 select the needed individual IDs or the A06 course. `--list` shows all IDs. Avoid loading an entire course if one small lesson answers the request.

Execution adapter rules:
- User asks CUA: use CUA for browser interactions and read the current browser documentation.
- API/SDK: read the current installed Higgsfield API client or provider integration skill; do not translate marketing course menus into guessed endpoints.
- Existing media-edit/faceless/UGC production skill: use its actual supported workflow; the Bible specialist supplies creative criteria.
- Existing HyperFrames/rendering/voice skill: load it only when the requested output requires that implementation.
- Tool missing: return a concrete draft/plan and name the unavailable execution step; never report it as generated.

No default model override, background scheduler or automatic agent fan-out is part of this package.
