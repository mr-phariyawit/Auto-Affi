# QA — cook-mortar-chilli-garlic (candidate r1)

**Verdict: qa-fail**

Every content criterion is met and the subject is fully in-frame, but the image is
rendered as a near-photograph: photoreal granite speckle on the mortar and pestle and
glossy wet highlights on the chilli and juice. That breaks the universal STYLE
("no photographic rendering, no glossy highlights"). Together with veg-thai-chillies it
is the strongest photographic outlier in the set, so it cannot ship against an
ink-and-gouache plate library.

## Acceptance criteria

| # | Criterion | Result | What I saw [VERIFIED: looked at image + pestle-top crop] |
|---|---|---|---|
| 1 | Single stone mortar + pestle, centred, on empty paper | met | One granite mortar and pestle, centred |
| 2 | Contents coarsely broken/chunky, not smooth paste | met | Chunky broken chilli, split garlic cloves, loose seeds, free juice — clearly coarse |
| 3 | Red and green chilli + pale garlic + loose seeds | met | All present and legible |
| 4 | Pestle present (leaning in mortar) | met | Pestle leans into the bowl |
| 5 | Minimal/no steam, no flames | met | No steam, no flame |
| 6 | No hands/text/numbers/labels | met | None found |

## Universal rules

- No text / no hands / plain cream ground: pass.
- Subject fully inside frame: pass — pestle top has clear margin above (crop confirms),
  mortar body clears all four edges.
- Style: FAIL — photoreal granite and glossy wet contents; reads as a photograph, not a
  flat ink-and-gouache plate. Cross-set outlier.

## Defects

1. Photographic rendering of granite (universal STYLE violation).
2. Glossy wet highlights on chilli pieces and juice (no-glossy-highlights violation).

## Fix (exact prompt change)

Replace the last sentence of paragraph 1 —
"The granite is matte with a gritty, hand-carved surface."
with:
"Render the whole mortar, pestle and contents as a flat ink-and-gouache botanical plate:
fine brown-black ink outlines filled with opaque matte colour in only two or three flat
tonal steps. The granite must be suggested with a few flat speckle marks, NOT a
photographic stone texture; the chilli, garlic and juice must be matte with absolutely no
glossy wet highlights, no specular shine and no photographic rendering anywhere."

Regenerate and re-QA for photographic drift before accepting.


## Round 2

**Verdict: qa-fail** [VERIFIED: looked at r2.png full image + full-res crops of the pestle/rim and the contents]

The dominant round-1 defect is NOT fixed. The granite is still rendered as a dense,
continuous, photoreal granite speckle covering the whole bowl and pestle — not the
"few flat speckle marks" the prompt asks for [VERIFIED: pestle/rim crop shows full-field realistic
stone grain]. At thumbnail it looks painterly; at full size it reads as a photograph of granite.
Secondary: the chilli pieces and the free juice in the bowl carry wet/glossy specular
highlights [VERIFIED: contents crop — glistening red chilli and shiny juice], a no-glossy-highlights violation.

Acceptance criteria [VERIFIED: looked at image]:
1. Single stone mortar + pestle, centred, on empty paper. Met.
2. Contents coarsely broken/chunky, not a smooth paste — Met (big split garlic cloves, broken chilli, loose seeds).
3. Red + green chilli + pale garlic + loose seeds. Met.
4. Pestle present, leaning into the bowl. Met.
5. Minimal/no steam, no flames. Met.
6. No hands/text/numbers/labels. Met.
- Framing: no subject pixel on any border [VERIFIED: edge pixel scan = 0 dark px on all four edges]; fully in frame.

Style: FAIL — photoreal dense granite + wet specular contents. Still a cross-set outlier
against the matte ink-and-gouache plant plates (veg-three-basils); does not match the house style.

## Fix (exact prompt change)

Replace in paragraph 2 —
"The granite is suggested with a few flat speckle marks, and the chilli, garlic and juice are matte."
with:
"Render the granite as a single flat mid-grey fill carrying only a SPARSE scatter of
individual grey and black flecks — a sparse hand-painted suggestion of stone, with large
areas of plain flat grey between the flecks; NOT a dense, continuous or photographic
granite texture. The chilli pieces, garlic and juice are completely dead-matte with no
wet sheen, no glistening droplets and no white specular highlights anywhere."

Regenerate and re-QA at full size for both the dense-granite texture and wet-contents gloss before accepting.
