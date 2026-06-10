# Auto-Affi Production Review Principle

Date: 2026-06-03

This principle captures the workflow proven by the silicone shoe-cover production run:

- product intelligence from Thai weather/news;
- cleanroom video composition with exactly one final audio stream;
- review variant with no spoken or on-video affiliate disclosure by user request;
- approval packet retaining the compliance gate before public posting.

## Core Principle

> One timely product becomes one production-review clip that feels like a natural Thai commercial, uses generated visuals only as silent B-roll, uses separate scene-synced Thai voice, passes cleanroom audio verification, and stays blocked from public publish until human approval and platform/caption disclosure gates are satisfied.

## Companion Principles

This production principle is enforced together with:

- `docs/principles/2026-06-04-always-on-viral-intelligence-principle.md`
- `docs/research/auto-affi-24-7-subagent-team-blueprint-th-2026-06-04.md`
- `docs/principles/2026-06-04-prompt-council-gate.md`
- `docs/principles/2026-06-04-model-routing-principle.md`
- `docs/principles/2026-06-04-rights-business-affairs-principle.md`
- `docs/principles/2026-06-04-talent-partner-principle.md`
- `docs/principles/2026-06-04-multi-clip-post-production-principle.md`
- `docs/principles/2026-06-04-learning-performance-principle.md`
- `docs/principles/2026-06-05-main-workflow-learning-upgrade.md`

## Environment and Secret Handling

All API keys required for the current production workflow are provisioned in the project `.env`.

- Verify only that required variable names are present; do not print, paste, commit, or copy secret values into reports.
- Normal production runs must not depend on clipboard keys. Clipboard is only for an explicit one-off manual override.
- If a required key is missing, block that provider route and record only the missing variable name in the run artifacts.

## Production Path

1. **Marketing-first product collection**
   - Start from Marketing-selected product ideas in `data/marketing_collection.csv`.
   - Marketing can select from Thai weather/news/events, social clusters, seasonal calendars, performance learning, brand requests, or manual human ideas.
   - Use foreign sources only as secondary context unless the target market is international.
   - For always-on scouting, first record raw news/social signals in `data/viral_signal_intelligence.csv`.
   - Marketing collection rows describe buyer angle, product idea, hook hypothesis, and priority; they are not approved product candidates.
   - Research validates Marketing collection rows before moving them into `data/product_intelligence_candidates.csv`.
   - Record only validated products in `data/product_intelligence_candidates.csv`.

2. **Research validates before product candidacy**
   - Research owns product truth, Shopee URL, price/SKU, image evidence, shop/brand, allowed claims, prohibited claims, and policy risk.
   - Research can reject, block, or send a Marketing collection row back for reframing.
   - A run folder cannot be created from a collection row unless Research validation passes or a human records a justified review override.

2.5. **Keep affiliate stories simple unless Marketing proves complexity is needed**
   - Default to one buyer problem, one product behavior, one proof loop, and one CTA.
   - A 30s product commercial usually uses one 3x3 storyboard board.
   - Complex stories require explicit Marketing reason, extra story audit, and clearer location/environment map.

3. **Viral intelligence must not exploit harm**
   - Green signals can move to product mapping after evidence check.
   - Amber signals need human review before product mapping.
   - Red signals such as violence, injury, death, minors, self-harm, serious illness, active criminal/legal cases, or visible victim suffering cannot become product prompts.
   - Map from broad audience needs, not from a real person's pain, scandal, injury, or humiliation.

3. **One product, one run folder**
   - Create `runs/YYYY-MM-DD-product-slug/`.
   - Keep product assets, payloads, source media, voice segments, final MP4, review frames, manifest, and approval packet in that folder.

4. **Visual source is silent**
   - Generate product video with source audio disabled when the model supports it, for example `generate_audio: false`.
   - If source audio exists, strip it before composition.
   - Treat the generated video as visual B-roll only.

5. **Voice is separate and scene-synced**
   - Write a timed scene table before generating voice.
   - Generate short Thai voice segments per visual beat.
   - For voice-over concepts, do not make the on-screen character visibly move their mouth as if speaking.
   - Prefer hands, product action, over-shoulder, profile, walking, listening, closed-mouth reaction, and B-roll.
   - Use visible mouth/lip-sync only when the route is explicitly a talking-head or presenter route with consent and sync QA.
     - model: `elevenlabs/text-to-dialogue-v3`;
     - `language_code: "th"`;
     - one short dialogue item per scene;
     - default current youth/commercial voice: Brittney, `kPzsL2i3teMYv0FxEYQ6`, `stability: 0.0`;
   - Before changing voice family, create a labeled audition comparison for human selection.
   - Cache successful voice segments and retry transient provider failures instead of regenerating completed paid segments.

6. **Natural speech beats speed**
   - Do not fix crowded scripts by speeding up voice.
   - Preferred segment speed factor: `1.0x`.
   - Warning threshold: above `1.08x`.
   - Hard reject threshold: above `1.15x`.
   - If a line does not fit, rewrite the line or use a 30s master.

7. **30s commercial master is the default**
   - Use 30 seconds when the product needs proof, price, size/color, use case, CTA, and Thai voice that sounds human.
   - Use 15 seconds only for hook tests or very simple products.

8. **Prompt council before generation**
   - Treat prompts as production contracts, not vibe paragraphs.
   - Every visual/voice/caption prompt must pass multi-team review before generation.
   - Required seats: Marketing, Product Research/Claims, Shooting Production, and Post/Rights/Compliance.
   - The prompt drafter cannot self-approve the prompt.
   - If density is below threshold, return `revise` or `block`; do not self-approve.
   - See `docs/principles/2026-06-04-prompt-council-gate.md`.

9. **Route decision before provider calls**
   - Load `.env` and record provider env readiness by variable name only.
   - Record primary route, secondary route, fallback ladder, route reason, cost estimate, and local download plan.

10. **Rights and business affairs are not optional**
   - Maintain product truth, claim ledger, rights tracker, AI usage log, affiliate link request, and publish packet.
   - Public posting remains blocked without affiliate URL/subIds, price/SKU recheck, disclosure, AI label, and rights status.

11. **Talent and partner plan scales the craft**
   - For premium or repeated production, record who owns strategy, prompt direction, post, compliance, growth, and external craft partner needs.
   - Partner for specialized craft when rights, quality, legal, or production complexity exceeds the lean core.

12. **Learning closes the loop**
   - Every run must have learning log, performance snapshot, model scorecard, prompt scorecard, and prompt council failure log.
   - A rendered clip is not workflow-complete until costs, scores, gates, failures, and next decisions are recorded.

13. **Thai text is controlled**
   - Do not ask video models to draw Thai text.
   - Add Thai captions/CTA overlays during composition whenever text appears on the final video timeline.
   - Before final render, machine-check caption text against the approved VO segment report. Block final render if caption count or text differs.
   - If the production explicitly needs a model-generated static text image, title card, or thumbnail mockup, route it only to `nano_banana_2` / Nano Banana Pro and run OCR/spelling/claim review before final use.
   - Review frames at the beginning, middle, price/CTA area, and ending.

13.5. **Product references must not leak unintended text or UI**
   - Use clean no-text product references when readable logos, phone UI, packaging text, or claims should not appear.
   - Reject generated footage that carries unapproved reference text into the video.

14. **On-media disclosure is configurable, but publish disclosure is mandatory**
   - Review variants may omit spoken or visible words like `โฆษณา` or `affiliate` when the human requests a cleaner commercial feel.
   - The approval packet must record that on-media disclosure was removed by request.
   - Public posting must compensate with platform commercial-content disclosure and/or caption disclosure before dispatch.

15. **Approval packet is the control plane**
   - The packet must point to the latest final MP4.
   - The packet must keep:
     - product URL and source signal;
     - model/job ids;
     - source visual path;
     - voiceover path;
     - final MP4 path;
     - review frames path;
     - cleanroom verification;
     - risks and publish gates;
     - human approval status.

16. **No public publish before explicit approval**
    - A review-ready clip is not a publish-ready clip.
    - Publish requires human approval, compliant caption/disclosure settings, valid affiliate link/subIds, and verified platform path.

17. **Retrospective upgrades are mandatory**
    - Every run closeout records successes promoted, failures found, user-caught failures, workflow rules added, provider failures, credit waste prevented or caused, and next-run blockers.
    - If the user catches a failure after internal QA passed, the next comparable run must include a stronger gate, machine-check, or independent reviewer seat.

## Cleanroom Verification Gate

Every production-review MP4 must pass:

```text
raw generated video audio streams = 0, or stripped before final
visual-only source audio streams = 0
final audio streams = 1
final video streams = 1
duration ~= selected profile, usually 30s
voice speed guard errors = []
```

Reject the output if:

- final has more than one audio stream;
- final has zero audio streams;
- source audio bleeds into the final mix;
- voice is rushed or robotic;
- voice-over visuals show character mouth movement that implies unsynced speech, unless an explicit talking-head/lip-sync route was approved;
- viral signal is red or exploitative and was mapped directly into a product prompt;
- run folder was created from `marketing_collection.csv` before Research validation passed or a human review override was recorded;
- Thai text is model-drawn in video frames, or static model text fails OCR/spelling/claim review;
- captions cover the product at critical moments;
- visual product identity drifts too far from the real Shopee product.
- generation started before `prompt_council_review.json` passed independent multi-team review.
- generation started before `route_decision.json` exists.
- archive is attempted before the learning artifacts are created.

## Production Naming

Recommended output names:

```text
production_kie_manifest.json
production_kie_v2_no_disclosure_manifest.json
review_frames_production/
review_frames_production_v2_no_disclosure/
```

## Learned Risk From Shoe-Cover Run


> A beautiful clip still fails review if the generated product use materially changes what the Shopee item is.

When product identity is fragile, prefer:

- real Shopee product image anchors;
- first-frame or image-to-video control;
- closer captions that avoid overclaiming;
- human review before creating affiliate publish assets.
