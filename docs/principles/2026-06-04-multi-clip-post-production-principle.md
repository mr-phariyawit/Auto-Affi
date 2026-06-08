# Auto-Affi Multi-Clip Post-Production Principle

Date: 2026-06-04

Purpose: turn the HyperFrames study and current Auto-Affi production learnings into enforceable rules for editing commercials, reviews, and variants made from many short clips.

## Core Rule

> Generation creates shots. Post-production creates the finished commercial. Every clip must enter a deterministic edit timeline with known timing, silent visual sources, one intentional final audio bed, post-composited Thai text, reviewable boundaries, and a clean approval packet.

## Companion Principles

This principle is enforced together with:

- `docs/principles/2026-06-03-production-review-principle.md`
- `docs/principles/2026-06-04-model-routing-principle.md`
- `docs/principles/2026-06-04-rights-business-affairs-principle.md`
- `docs/principles/2026-06-04-learning-performance-principle.md`
- `docs/research/auto-affi-systematic-workflow-upgrade-blueprint-th-2026-06-04.md`

## Required Artifacts

Every multi-clip post-production run must include:

```text
clip_inventory.json
edit_decision_list.json
post_manifest.json
hyperframes_manifest.json or render_manifest.json
cleanroom_verification.json
review_frames_post/
final_review_mp4
```

For variant batches, also include:

```text
shared_clip_manifest.json
variant_clip_manifest.json
variant_assembly_manifest.json
```

## Operating Principles

1. **Post owns the timeline**
   - Do not treat provider output order as the edit.
   - Build an explicit edit decision list before final assembly.
   - Each clip must have role, source path, intended in/out, actual duration, product-truth notes, and approval status.

2. **Clip inventory before assembly**
   - Download every provider output into the run folder.
   - Record provider job id, local path, duration, resolution, fps, has-audio, source prompt, source rights status, and product identity risk.
   - Provider CDN URLs are not durable sources.

3. **Normalize first, edit second**
   - Before timeline work, normalize clips to the target frame geometry and fps.
   - Default master: 9:16, 1080x1920, 30fps unless the route decision says otherwise.
   - If a clip is off-duration, document whether it is trimmed, looped, slowed, replaced, or restricted to hook/cutdown use.

4. **Visual clips are silent by default**
   - Generated clip audio is draft-only unless explicitly approved.
   - Strip or mute source audio before final composition.
   - Final review MP4 must have exactly one intentional audio program: Thai VO, music/bed mix, or approved presenter audio.

5. **Scene-synced audio beats generic narration**
   - Voice lines are written against scene timing, not pasted over a finished concat.
   - Do not rescue crowded edits by speeding Thai VO.
   - If voice does not fit, rewrite the line, extend the master, or shorten the visual beat.

6. **HyperFrames is the deterministic compositor**
   - Use HyperFrames for Thai captions, CTA overlays, price cards, lower thirds, timed graphic elements, and final review composition when HTML/video timing is needed.
   - Each visible timed element should be represented by stable `data-start`, `data-duration`, and a patchable id or selector.
   - Prefer exact fps values such as `30`, `60`, or rational fps strings. Do not use ambiguous decimal fps.

7. **HTML timeline is source of truth**
   - The HyperFrames `index.html` or composition files are not throwaway render wrappers.
   - They are the editable source for timing, captions, overlays, media placement, and review changes.
   - Studio or agent edits must patch source files, not only mutate preview DOM.

8. **GSAP and motion must be seekable**
   - Animated timelines must be deterministic, paused by default, and registered in `window.__timelines`.
   - Avoid unseeded randomness, time-of-day logic, async timeline construction after render readiness, and infinite repeats that affect duration.
   - Rendering must produce the same frame when seeking to the same timestamp.

9. **Cuts must protect product truth**
   - A smooth edit fails if it changes what the Shopee product is.
   - Boundary frames must be reviewed for product identity drift, unreadable use case, wrong SKU/color/size, or accidental overclaim.
   - Keep product visible through proof moments, not only hook and CTA.

10. **Transitions serve comprehension**
    - Use hard cuts, match cuts, speed ramps, zoom punches, or graphic transitions only when they clarify the product story.
    - Do not hide weak generation with excessive motion, blur, or overlays.
    - Any transition that covers the product during proof or price/CTA moments is a review risk.

11. **Shared clips are rendered once**
    - In variant batches, separate hook-specific clips from shared body/CTA clips.
    - Render shared clips once, then reuse them across variants.
    - Variant differences should be traceable in `variant_assembly_manifest.json`.

12. **Captions and CTA are post-composited**
    - Do not rely on video models to draw Thai text.
    - Burn or overlay Thai text in post where spelling, line breaks, contrast, and timing can be inspected.
    - If a static title card or thumbnail intentionally uses model-generated text, the only approved model route is `nano_banana_2` / Nano Banana Pro, followed by OCR/spelling/claim review.
    - Captions must not cover product proof, price, hands/action, or CTA tap targets.

13. **Review boundaries, not only the final frame**
    - Extract review frames from hook, every major clip boundary, proof moment, price/CTA, and ending.
    - For multi-clip edits, also review one frame before and after important cuts.
    - If the cut creates product confusion, revise the EDL before regenerating more media.

14. **Cleanroom verification is mandatory**
    - Run ffprobe-style checks before approval.
    - Reject if final audio streams are zero or more than one, if source audio leaks, if duration is materially wrong, or if final fps/resolution differs from the declared master.
    - Render completion is not approval.

15. **Learning closes the edit**
    - Record which clips were reused, rejected, trimmed, or replaced.
    - Record edit failures such as product drift, caption collision, rushed VO, boundary jump, audio bleed, and provider duration mismatch.
    - Repeated successful edit structures should become reusable HyperFrames templates or registry blocks.

## Post-Production Gates

Reject or revise before human review when:

- `clip_inventory.json` is missing or has unknown durations;
- source clips still contain unapproved audio;
- the EDL is implicit or cannot be reconstructed;
- Thai text is drawn by a video model instead of post-composited, or Nano Banana Pro static text fails OCR/spelling/claim review;
- HyperFrames lint/validate fails when HyperFrames is used;
- GSAP or motion cannot be paused and seeked deterministically;
- review frames show product identity drift;
- captions cover the product during proof/price/CTA moments;
- final MP4 has more than one audio stream or no audio stream;
- variant batches regenerate shared body clips without a recorded reason.

## Recommended Timeline Shape

```text
0.0-1.5s   hook clip / attention movement / product visible
1.5-6.0s   problem or use-case proof
6.0-15.0s  product action and differentiator
15.0-24.0s price, size, color, realistic benefit
24.0-30.0s CTA and final product clarity
```

This shape is a default, not a law. The real law is: the final edit must make the product easier to understand, easier to trust, and easier to act on than any single generated clip.
