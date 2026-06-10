# Company Autonomous Creative Decision System

Date: 2026-06-06

Company objective:

**บริษัทต้องสร้างโฆษณาที่ดูตื่นตา ตื่นเต้น น่าสนใจ สนุก และกินใจเท่านั้น**

This system lets the internal creative/production team decide faster after a storyboard route is visible, while preserving provider-spend and publish safety.

## Authority Split

The team may decide:

- which creative route is strongest;
- which shots to proof-test first;
- whether generated dailies are kept, killed, or regenerated;
- which caption/VO direction is most emotionally effective;
- whether a cut is ready for human review.

The team may not bypass:

- provider credit acknowledgement gates;
- model locks;
- product-truth and claim gates;
- affiliate URL / live price / SKU / stock recheck;
- rights, disclosure, AI label, and final publish approval.

## Required Vote Seats

Every keep/kill/regenerate decision must include these seats:

1. Executive Creative Director
2. Film Director
3. Director of Photography
4. Production Designer
5. Prompt Continuity Architect
6. Product Truth / Claims
7. Performance Marketing
8. Thai Copy / VO Lead

## Pass Rule

An ad or shot can advance only when:

- each emotion pillar scores at least 4.0;
- the average emotion score is at least 4.3;
- memory frame is present;
- share/save trigger is present;
- product truth passes;
- character/location/camera continuity passes;
- no hard-fail condition appears.

## Hard Fail

Kill or regenerate if any of these happen:

- pretty but emotionally flat;
- no fun or surprise;
- no human relief/care/trust;
- product could be removed without changing the ending;
- patch becomes invisible, magical, fake, or unsupported;
- room, character, product, or camera geography drifts;
- fake price, fake logo, fake package, disease/fear claim, or publish claim appears.

## Decision Output

Every decision writes:

```text
decision:
  keep | kill | regenerate | hold
reason:
  one sentence
emotion_scores:
  wonder:
  thrill:
  curiosity:
  fun:
  heart:
critical_locks:
  product_truth:
  continuity:
  claim_safety:
next_action:
  exact shot/edit/prompt change
```

## Production Principle

Do not protect weak work because it is already generated. Protect the company standard.

