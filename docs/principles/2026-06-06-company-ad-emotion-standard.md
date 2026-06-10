# Company Ad Emotion Standard

Date: 2026-06-06

Company objective:

**บริษัทต้องสร้างโฆษณาที่ดูตื่นตา ตื่นเต้น น่าสนใจ สนุก และกินใจเท่านั้น**

This is a creative gate, not a slogan. A commercial that is merely clear, useful, technically consistent, or claim-safe is not enough.

## The Five Required Emotions

Every ad must pass all five:

1. **ตื่นตา / Wonder**
   - The first visual world must feel worth looking at.
   - There must be at least one memorable frame that could work as a thumbnail.

2. **ตื่นเต้น / Thrill**
   - The ad must create a tiny question, tension, countdown, chase, reveal, or transformation.
   - The viewer should feel a reason to keep watching.

3. **น่าสนใจ / Curiosity**
   - The viewer must understand why this product/action matters, but not feel they are watching a plain tutorial.
   - A hook should open a loop and the product should close it.

4. **สนุก / Fun**
   - There must be a playful beat, surprise, satisfying action, witty line, or social share/save reason.
   - If the ad feels like homework, it fails.

5. **กินใจ / Heart**
   - The ad must connect the product to a human feeling: relief, care, pride, calm, hope, trust, or belonging.
   - It must avoid fake sentiment. The feeling must come from a real product change.

## Scoring Rule

Each pillar scores 1-5.

- 5 = unmistakable and memorable.
- 4 = clearly present.
- 3 = present but weak.
- 2 = barely present.
- 1 = absent.

Company pass:

- Minimum 4 in every pillar.
- Average score at least 4.3.
- At least one scene must be a "memory frame."
- At least one beat must be "share/save worthy."
- Product truth and claim safety must pass.

## Hard Fail Conditions

Fail the ad if:

- it is merely instructional;
- it is pretty but emotionally flat;
- it has no memorable frame;
- it has no fun or surprise;
- it uses fake fear, disease, danger, or overclaiming;
- it could be replaced by a product listing demo with no emotional loss;
- the product is not necessary to the ending.

## Prompt Requirement

Every scene contract must include:

```text
emotion_pillar:
  wonder:
  thrill:
  curiosity:
  fun:
  heart:

memory_frame:
share_or_save_trigger:
product_truth_reason:
```

If the scene cannot name its emotional job, it is not allowed into generation.

## Research Support

- TikTok's creative guidance emphasizes TikTok-first vertical creative, hooks, product benefits, and clear CTA as performance foundations.
- WARC/DAIVID emotion research finds strongest creative-effectiveness campaigns tend to evoke multiple intense positive emotions, including warmth, relief, hope, trust, calmness, and entrancement.
- Video ad affect research points to visual context and attention as core drivers of emotional response, so the company must design frames and context, not just scripts.
