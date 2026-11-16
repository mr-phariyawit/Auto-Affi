# QA — cook-wok-basil-in (candidate r1)

**Verdict: qa-fail**

Food content is right — coarse browned pork with pounded red+green chilli and crushed
garlic, lightly sauced, a loose handful of fresh un-wilted bright-green toothed basil
dropped on top, no long beans / onion / baby corn / fried egg, only a thin steam wisp.
But the whole scene is rendered as a photograph (photoreal seasoned-steel wok, wooden
handle with metallic rivets, glistening specular food), breaking the universal STYLE
("no photographic rendering, no glossy highlights"). As the hero in-pan shot of an
ink-and-gouache library it must match the plate style, so it fails.

## Acceptance criteria

| # | Criterion | Result | What I saw [VERIFIED: looked at image + basil crop] |
|---|---|---|---|
| 1 | Top-down/45°, wok filling most of frame | met | High three-quarter wok, fills frame |
| 2 | Basil fresh, flat, bright green, not wilted/stirred-in | met | Crisp bright-green leaves sitting on top, un-wilted |
| 3 | Leaves recognisably holy basil (toothed) | met (borderline) | Toothed, pointed, purple-stemmed basil with flower spikes — reads as holy basil, though teeth are deeper than the "sparse shallow" of the A1 sprig |
| 4 | Meat coarse, browned, pounded chilli/garlic, lightly sauced | met | Coarse browned mince, red+green chilli, pale crushed garlic, glistening dark sauce, not a gravy |
| 5 | No long beans/onion/baby corn, no fried egg, no flames, minimal steam | met | None of the forbidden veg; no egg; no flame; thin steam wisp only |
| 6 | No hands/text/numbers/labels | met | None found |

## Universal rules

- No text / no hands / plain cream ground: pass.
- Framing: pan body in-frame with margin; wooden handle cut at the right edge (intended
  partial per prompt, but flagged for a composited layer).
- Style: FAIL — photographic rendering + glossy specular food; the strongest hero-shot
  outlier against the ink-and-gouache set.

## Defects

1. Photographic rendering + glossy highlights (universal STYLE violation).
2. Handle cropped at right edge (minor; shared with cook-wok-empty).

## Fix (exact prompt change)

Replace the final clause of paragraph 1 —
"...the whole scene rendered in a few flat tonal steps."
with:
"...the whole scene rendered as a flat ink-and-gouache plate: brown-black ink outlines
filled with opaque matte colour in only two or three flat tonal steps, with NO
photographic metal or food texture, no glossy or wet specular highlights and no 3D
sheen anywhere. Keep the whole wok including the full handle inside the frame with a
band of empty cream paper on all sides."

Regenerate and re-QA for photographic drift. When re-rendering, keep the basil clearly
holy basil (broadly elliptical with sparse shallow teeth, lightly hairy), not a
deeply saw-toothed or smooth sweet-basil leaf.


## Round 2

**Verdict: qa-fail** [VERIFIED: looked at r2.png full image + full-res crops of the basil and the meat]

The style and framing defects are fixed, but the round-1 leaf-shape note was not
addressed. The food is now matte: coarse browned mince, chilli and garlic rendered in flat
gouache with no wet specular [VERIFIED: meat crop — matte crumb, no gloss]; the photoreal steel and
glossy food of r1 are gone. Framing fixed — the whole wok incl. the full wooden handle is
inside the frame with margin [VERIFIED: edge pixel scan = 0 dark px on all four edges].

BUT the basil leaves still fail the holy-basil spec. They are narrow, lance-elliptical
leaves with a fine, prominent saw-tooth margin (roughly 10-12 sharp teeth per side)
[VERIFIED: basil crop], not the "broadly elliptical, sparse shallow teeth" called for — the same
too-deep-teeth problem flagged in round 1, and narrower than the library's own holy-basil
plate (veg-three-basils, leftmost). Purple stems and matte un-wilted surface read correctly,
but the leaf outline drifts toward a sharply serrated / sweet-basil-mint silhouette.

Acceptance criteria [VERIFIED: looked at image]:
1. High three-quarter, wok fills frame. Met.
2. Basil fresh, flat, bright green, un-wilted, sitting on top. Met.
3. Recognisably holy basil — NOT MET: leaf too narrow with too-deep sharp teeth vs the broadly-elliptical sparse-shallow-tooth spec.
4. Meat coarse, browned, pounded chilli/garlic, lightly sauced, not swimming. Met.
5. No long beans/onion/baby corn, no fried egg, no flames, minimal steam — Met (green pieces are short chilli segments, pale pieces are garlic cloves; one thin steam wisp).
6. No hands/text/numbers/labels. Met.

Style: now matte and consistent with the plant plates; the ONLY remaining failure is leaf morphology.

## Fix (exact prompt change)

Replace in paragraph 2 —
"The holy basil leaves are broadly elliptical with sparse shallow teeth and a softly hairy matte surface."
with:
"The holy basil leaves must be BROADLY elliptical — width roughly half the length, not
narrow or lance-shaped — with each margin carrying only a FEW (about four to six per side)
shallow, soft, rounded teeth, NOT a fine saw-edge and NOT many sharp serrations; surface
softly hairy and dead-matte. Do not draw narrow, deeply saw-toothed, mint-like or glossy
sweet-basil leaves."

Regenerate and re-QA the leaf outline at full size before accepting; the rest of the image is ready.
