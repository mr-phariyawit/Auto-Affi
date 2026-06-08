# Hanky V12 Success Scenario Runbook

Date: 2026-06-06

Baseline final:
`runs/2026-06-04-hanky-dry-towel-60s-seedance-marketing-test/outputs/hanky_house_microfiber_towel_60s_hyperframe_kie_elevenlabs_v12_brittney.mp4`

Purpose: make the last known good production path explicit, so future runs do not improvise around proven gates.

## What Made V12 Work

1. Simple product story
   - One buyer problem: rainy commute.
   - One product behavior: compact microfiber towel helps handle small wet moments.
   - One proof loop: hands, fabric, droplets, pack-away.
   - One CTA: check latest details and price.

1b. Deep product and market research before prompting
   - Search broadly after one product is selected.
   - Collect marketplace facts, similar listings, visual references, user-review language, competitor visuals, use-case contexts, and seasonal/news context.
   - Convert research into image/video prompt constraints before writing Nano Banana Pro or Seedance prompts.

2. Seedance 2.0 only for visual video
   - No visual-video model switching.
   - Regeneration stayed inside Seedance 2.0.
   - Risky shots were repaired by tighter shot contracts, not by fallback models.

3. Dailies were judged by contact sheet, not vibes
   - `outputs/review_frames/hanky_60s_contact_sheet_v5.png` existed.
   - `dailies_qc.json` recorded numbered cell checks.
   - Bag, wardrobe, product, location, and lighting anchors were audited per visible cell.

4. Bad attractive clips were rejected
   - Scene 2 wardrobe drift was rejected and regenerated.
   - Scene 5 identity drift was rejected and regenerated.
   - Scene 11 bag mismatch was rejected and regenerated through r3.

5. Post-production was deterministic
   - Source video was stripped to silent visual B-roll.
   - HyperFrames handled Thai captions and layout.
   - No model-generated Thai captions were used in the visual footage.

6. Thai voice route was specific and cached
   - Voice: Brittney, `kPzsL2i3teMYv0FxEYQ6`.
   - `language_code: "th"`, `stability: 0.0`.
   - Successful voice segments were cached; completed segments were not force-regenerated.

7. Caption/voice sync was machine-verified
   - `metrics/caption_voice_sync_v12_brittney.json` had `ok: true`.
   - Caption count equaled voice segment count.
   - Caption text matched voice segment text exactly.

8. Review-ready stayed separate from publish-ready
   - Final MP4 could be reviewed.
   - Publish remained blocked for affiliate URL, live price/SKU, rights, and human approval.

## Mandatory Future-Gate Checklist

Every new run must create `success_scenario_review.json` before `validate-generation`.

Required fields:

```json
{
  "baseline_success_run_id": "2026-06-04-hanky-dry-towel-60s-seedance-marketing-test",
  "baseline_final_mp4": "runs/2026-06-04-hanky-dry-towel-60s-seedance-marketing-test/outputs/hanky_house_microfiber_towel_60s_hyperframe_kie_elevenlabs_v12_brittney.mp4",
  "success_steps_checked": {
    "deep_research_before_prompting": true,
    "simple_story": true,
    "seedance_only_visual_video": true,
    "contact_sheet_before_batch_or_motion_test": true,
    "numbered_dailies_anchor_audit": true,
    "targeted_regeneration_not_batch_force": true,
    "kie_elevenlabs_v3_brittney_or_approved_voice": true,
    "caption_voice_exact_match_before_final": true,
    "publish_blocked_until_human_affiliate_price_rights": true
  },
  "deviations_from_success_scenario": [],
  "decision": "pass_with_publish_block"
}
```

If any deviation exists, it must have `status: "approved"` or generation stays blocked.

## Added After Rain-Cover Defect

- Any generated image reference, clean product image, keyframe, storyboard imagery, or image-bearing contact sheet must be Nano Banana Pro (`nano_banana_2`) only.
- Scripted schematic images are not allowed as production references.
- A human-visible pre-generation storyboard/contact sheet must be shown and approved before paid Seedance generation.
- After Marketing selects one product, create `deep_product_research.json`, `visual_reference_board.json`, and `research_synthesis.md` before creative brief, image prompts, video prompts, or storyboard approval.
