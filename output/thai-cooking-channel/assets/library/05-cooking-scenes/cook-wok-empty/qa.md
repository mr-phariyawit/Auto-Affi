# QA — cook-wok-empty (candidate r1)

**Verdict: qa-fail**

The wok content is right (empty, clean, seasoned, top-down, unlit burner) but it is
rendered as a photograph of a carbon-steel wok — photoreal worn-steel texture and
metallic sheen — which breaks the universal STYLE ("no photographic rendering, no
glossy highlights"). It is the third strong photographic outlier (with chillies and
mortar) and would clash as a background under ink-and-gouache food layers. Secondary:
the handle is cropped at the right edge.

## Acceptance criteria

| # | Criterion | Result | What I saw [VERIFIED: looked at image + edge pixel scan + crops] |
|---|---|---|---|
| 1 | One wok, centred, from directly above, filling most of frame | met | Top-down wok fills the frame |
| 2 | Interior empty, clean, dry — no food/oil/liquid | met | Bare dry interior |
| 3 | Dark matte seasoned carbon steel (not stainless/non-stick) | partial | Reads as seasoned carbon steel, but via a photoreal metal texture rather than matte gouache |
| 4 | Burner faint and secondary, no flames | met | Dark grate beneath, secondary, unlit |
| 5 | Calm, uncluttered, layerable | met | Clean open circle |
| 6 | No text/numbers/labels | met | None found |

## Universal rules

- No text / no hands / plain cream ground: pass.
- Subject framing: pan body has margin on left/top/bottom (edge scan: 0 dark px on those
  edges), BUT the handle runs off and is cut at the right edge (104 dark px at x=W-1).
  Left rim margin is tight (~30 px). Flagged per the cut-off-handle rule.
- Style: FAIL — photographic seasoned-steel rendering with metallic sheen, inconsistent
  with the ink-and-gouache set.

## Defects

1. Photographic rendering + metallic sheen (universal STYLE violation).
2. Handle cropped at the right frame edge.

## Fix (exact prompt change)

Replace the final sentence of paragraph 1 —
"The focus is the clean open circle of the seasoned wok interior, even, uncluttered and
calm, rendered in a few flat tonal steps."
with:
"Render the whole wok and burner as a flat ink-and-gouache plate: a brown-black ink
outline filled with opaque matte colour in only two or three flat tonal steps. The
seasoned steel must be matte and simplified with NO photographic metal texture, no
metallic sheen and no specular highlight. Keep the entire wok, including the full length
of its handle, inside the frame with a band of empty cream paper on all four sides."

Regenerate and re-QA for photographic drift and for the handle being fully in-frame.


## Round 2

**Verdict: qa-pass** [VERIFIED: looked at r2.png full image + full-res crop of the interior]

Both round-1 defects are fixed. The metallic sheen is gone: the interior is now a dark,
matte, mottled seasoned-steel surface in flat tonal steps with no specular highlight and
no photographic metal reflection [VERIFIED: interior crop — matte stipple, no sheen]. The handle is now
fully inside the frame with a cream margin [VERIFIED: edge pixel scan = 0 dark px on all four edges,
including the right/bottom where the handle loop sits].

Acceptance criteria [VERIFIED: looked at image]:
1. One wok, centred, top-down, filling most of the frame. Met.
2. Interior empty, clean, dry — no food/oil/liquid. Met.
3. Dark matte seasoned carbon steel (not stainless/non-stick) — Met (now matte, was "partial" in r1).
4. Burner grate faint and secondary, no flames. Met.
5. Calm, uncluttered, layerable as a background. Met.
6. No text/numbers/labels. Met.

Style: the mottled interior is the heaviest-textured surface in the set and reads a touch
busier than the flat plant plates, but it is matte, ink-outlined and gloss-free, so it is
consistent-enough with the house style and usable as a background layer. Acceptable.

No prompt change required. (If a cleaner background is later wanted, simplify the interior
mottle to fewer flat tonal steps — optional, not a blocker.)
