# QA — veg-thai-chillies (candidate r1)

**Verdict: qa-fail**

Botanically the scatter is right, but the fruits are rendered with bright glossy
specular highlights and a semi-photographic / 3D-render finish. That breaks
acceptance criterion 5 ("matte, no glossy highlight") AND the universal STYLE
("no glossy highlights, no photographic rendering"). This is the strongest style
outlier in the set, so it fails despite being on the needs-reference list.

## Acceptance criteria

| # | Criterion | Result | What I saw [VERIFIED: looked at image] |
|---|---|---|---|
| 1 | Read as small slim bird's-eye, not spur/bell | met | All fruits slender, finely pointed, a few cm — correct type |
| 2 | Green and red present, roughly equal number | met | ~5 green and ~5 red, alternating |
| 3 | At least one split showing seeds + membrane | met | Two split lengthways, pale membrane + cluster of flat seeds, intact calyx |
| 4 | Separated, none touching, countable | met | Clear cream paper between every fruit |
| 5 | Surfaces matte, no glossy highlight | NOT MET | Strong white specular highlights and shiny skin on nearly every fruit — reads as 3D/photographic, not matte gouache |
| 6 | No text/numbers/labels | met | Edges and corners clean |

## Botanical / sourced details

- Short green stalk + star-shaped calyx: present and correct on whole and cut fruit.
- Cut fruit shows pale placental membrane and plausible cluster of flat seeds: correct.
- Type reads as bird's-eye (ขี้หนู/จินดา): correct.

## Universal rules

- No text / no hands / plain cream ground: pass.
- All fruits fully inside frame with margin: pass.
- Style: FAIL — glossy, semi-photographic finish; inconsistent with the ink-and-gouache
  matte plate used by the rest of the set. This is a cross-set outlier.

## Defects

1. Glossy specular highlights on fruit skin (criterion 5 + STYLE violation).
2. Overall render reads photographic/3D rather than flat gouache.

## Fix (exact prompt change)

Replace the final sentence of paragraph 1 —
"Each fruit has a smooth, firm, gently curved body, the surface shown in a few flat
tonal steps so the rounded form reads without any shine."
with:
"Each fruit has a smooth, firm, gently curved body rendered in completely matte,
dead-flat gouache using only two or three tonal steps; the rounded form must read from
the tonal steps alone, with absolutely NO white specular highlights, no glossy sheen,
no wet look and no photographic reflection anywhere on the skin, stalk or calyx."

Regenerate after the change; re-QA for gloss before accepting. Still needs an owner
reference photo to confirm cultivar shape once the render is matte.


## Round 2

**Verdict: qa-pass** [VERIFIED: looked at r2.png full image + full-res crop of the red/green cluster]

The round-1 gloss defect is fixed. At full size every fruit is rendered in flat
ink-and-gouache: brown-black outlines, opaque matte colour in two to three tonal steps,
visible paper tooth, and only soft tonal shading on the rounded bodies. No white
specular highlights, no wet sheen, no 3D/photographic skin anywhere [VERIFIED: red-fruit crop].

Acceptance criteria re-check [VERIFIED: looked at image]:
1. Type — all fruits slim, finely pointed, a few cm: bird's-eye. Met.
2. Green/red roughly equal (~5/5), alternating. Met.
3. Two fruits split lengthways showing pale membrane + cluster of flat seeds, intact green calyx. Met.
4. Separated, none touching, countable on cream paper. Met.
5. Matte, no glossy highlight — NOW MET (was the round-1 fail).
6. No text/numbers/labels. Met.
- Calyces intact (short green stalk + star calyx) on whole and cut fruit; seeds plausible. Met.
- Framing: no subject pixel on any border [VERIFIED: edge pixel scan top/bot/left/right = 0 dark px]; clear cream margin all sides.

Stylistic consistency: now consistent with the plant plates (e.g. veg-three-basils/r1) —
same matte ink+gouache botanical-plate treatment. No longer a photographic outlier.

No prompt change required.
