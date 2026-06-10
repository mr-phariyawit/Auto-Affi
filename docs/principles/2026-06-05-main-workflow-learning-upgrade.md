# Auto-Affi Main Workflow Learning Upgrade

Date: 2026-06-05

Purpose: convert real production wins and user-caught failures into enforceable workflow rules.

## What Succeeded

1. **Simple product stories beat complex narrative experiments.**
   - iFilm phone pouch and Hanky microfiber towel were easier to audit than the earlier umbrella story.
   - Default affiliate ad structure should be one buyer problem, one product behavior, one proof loop, one CTA.

2. **Seedance 2.0 can produce useful product B-roll when each shot has one action.**
   - The strongest shots were hands, product inserts, water/proof texture, bag/table/lobby actions, and simple movement.
   - 3x3 storyboard grids are enough for most 30s product commercials.

3. **Generated video should remain silent visual B-roll.**
   - Source audio stripping and HyperFrames cleanroom composition produced reliable finals.
   - Final audio should be one intentional VO/music bed only.

4. **Deterministic post wins for Thai text and captions.**
   - HTML/HyperFrames captions with embedded Thai font worked better than model-generated Thai text.
   - Caption overlays must be safe-area checked in review frames.

   - The selected youth/social voice is Brittney, voice id `kPzsL2i3teMYv0FxEYQ6`, unless a later audition beats it.

6. **Audition videos help humans choose voice faster.**
   - A labeled voice comparison video made the Brittney selection easier.
   - Local `ffmpeg` lacks `drawtext`, so title cards should be rendered as images when labels are needed.

7. **Cache and retry save credits.**
   - Successful voice segments must be cached and reused; do not rerun all segments after one failure.

8. **`.env`-first secret handling reduces work stoppage.**
   - Production keys are now treated as provisioned in `.env`.
   - Provider calls load `.env`; logs record only variable names and present/missing status.

## What Failed

1. **Continuity audit missed wardrobe and bag drift.**
   - Scene 2 unexpectedly changed a white shirt into a raincoat-like sleeve.
   - Contact-sheet image 11 changed the established bag into a different bag.

2. **Location/environment logic needed to be explicit before generation.**
   - The model should not invent transitions between rain, covered walkway, lobby, cafe, and product-use zones.
   - Wet/dry states, light sources, surfaces, and movement path must be designed before shot cards.

3. **Storyboard audit was too weak before the user pushed it.**
   - Story logic, product necessity, and buyer memory image must be checked before prompts.
   - A storyboard that only works because captions explain it is not ready for generation.

4. **Caption copy drifted from the voiceover.**
   - The first V12 Brittney render reused older V10 caption copy.
   - This is a final-render blocker, not a cosmetic note.

5. **Voice routing initially used invalid external voice IDs.**

6. **Voice tone was under-directed at first.**
   - Early voices were too sleepy.
   - Voice direction must include target age/energy, commercial role, and stability/emotion settings before generation.

7. **Product references can poison generated shots.**
   - Phone pouch product refs carried readable logo/UI into generated footage.
   - Use clean no-text references, blank screens, or deterministic post for text.

8. **Scripts initially risked duplicate spend and artifact collision.**
   - `force=True` and shared concat-list names can waste credits or overwrite prior version artifacts.
   - Every production version needs versioned segment folders, concat lists, reports, and outputs.

9. **Publish readiness was easy to overstate.**
   - Review-ready clips still had price/SKU, affiliate URL, rights, disclosure, and human approval blockers.
   - Main workflow must keep review-ready separate from publish-ready.

10. **Provider/key assumptions created avoidable stalls.**
    - Clipboard key workflows were brittle.
    - Provider helpers must support the actual `.env` variable names used by the project.

11. **A scripted schematic image slipped into production previsualization.**
    - A rough locally generated rain-cover reference was shown and was not acceptable quality.
    - Production image references, cleanup references, keyframes, storyboard imagery, and visual contact sheets must use Nano Banana Pro (`nano_banana_2`) or approved real source assets only.

12. **The storyboard gate was machine-visible but not human-visible.**
    - `storyboard_grid.json` existed, but the user did not see a 3x3 storyboard/contact sheet before paid Seedance generation started.
    - JSON contract pass is not enough; the reviewer must see and approve the storyboard/contact sheet and spend before provider calls.

13. **The latest run failed to inherit the last known good scenario.**
    - The rain-cover run restarted from generic artifacts and improvised a reference image path instead of first checking the V12 runbook.
    - Future runs must create `success_scenario_review.json` before visual generation and list every approved deviation from the V12 baseline.

## New Workflow Rules

### Story and Visual

- For standard affiliate products, Marketing should choose the simplest story that proves the product.
- Use one 3x3 storyboard board for 30s commercials unless the product truly needs more.
- Every shot card must have one visible action, one product/prop anchor, one location state, one physics expectation, and one regenerate trigger.
- Before generation, pass `location_environment_design.json`, `story_audit.json`, `continuity_audit.json`, and `story_physics_review.json`.
- Dailies QC must inspect numbered contact-sheet cells, not only the compiled video.

### Product References

- Clean product refs before video generation when readable logo/UI/package text is not intended.
- Phone/product screens should be blank unless the screen content is approved and rights-safe.
- Reject attractive shots if product silhouette, bag, prop, wardrobe, or location anchor changes.
- Generated product references, clean keyframes, storyboard imagery, and any image-bearing contact sheets must use Nano Banana Pro (`nano_banana_2`) only.
- Scripted schematic images, hand-drawn placeholders, rough vector drawings, or non-Nano Banana image generations are blocked as production references.

### Human-Visible Pre-Generation Review

- Before paid Seedance generation, render a reviewable 3x3 storyboard/contact sheet from the shot cards.
- Show the reviewer the contact sheet, shot-card summary, model lock, image-reference source, and estimated credit spend.
- Record approval/revise/block in `pre_generation_user_review.json`.
- Do not treat `storyboard_grid.json` alone as approval to spend credits.

### Last Known Good Scenario

- The current baseline is `hanky_house_microfiber_towel_60s_hyperframe_kie_elevenlabs_v12_brittney.mp4`.
- Before a new paid visual call, create `success_scenario_review.json`.
- Unapproved deviations from the baseline block generation.

### Deep Research Before Prompting

- After Marketing chooses one product, search broadly before writing image or video prompts.
- Required artifacts: `deep_product_research.json`, `visual_reference_board.json`, and `research_synthesis.md`.
- Research must include product facts, similar listings, visual references, user-review language, competitor/use-case visuals, seasonal/news context, risks/contradictions, and prompt implications.
- Visual references are research metadata only unless rights are approved or they are regenerated with Nano Banana Pro.
- `research_synthesis.md` must convert findings into image prompt constraints, Seedance video prompt constraints, location/environment design, physics/hand mechanics, and negative prompts.

### Voice

- Use scene-synced short VO segments.
- Default commercial-youth voice: Brittney `kPzsL2i3teMYv0FxEYQ6`, `stability: 0.0`, `language_code: "th"`, unless a new audition beats it.
- Generate labeled audition comparisons before locking a new voice family.
- Cache successful segments and retry transient provider failures; do not regenerate completed segments by default.

### Captions and Post

- Thai captions/CTA are deterministic post assets, not model-generated video text.
- Before final render, extract HyperFrames caption text and compare it exactly against the approved VO segment report.
- Final render is blocked when `caption_count != voice_segment_count` or any caption text differs from VO text.
- Review frames must sample beginning, middle, CTA/end, and any price/disclosure areas.

### Secrets and Provider Calls

- Load `.env` before route decisions and provider calls.
- Record only variable names and readiness, never secret values.
- Clipboard is not part of the normal production route.
- Provider helpers must support the actual project env aliases.

### Review vs Publish

- A clip can be review-ready while publish-blocked.
- Publish requires human approval, live price/SKU recheck, affiliate URL/subIds, disclosure path, rights status, and verified upload/dispatch path.

## Mandatory Retrospective Fields

Every run closeout must add these to `metrics/learning_log.md` and/or the run report:

```text
successes_promoted
failures_found
user_caught_failures
workflow_rules_added
provider_failures
credit_waste_prevented_or_caused
next_run_blockers
```

## Promotion Rule

- If a fix succeeds once, record it as a candidate rule.
- If it prevents a repeated failure or saves credits, promote it into the main workflow.
- If the user catches a failure after internal audit passed, add a machine-check or independent review seat before the next comparable generation.
