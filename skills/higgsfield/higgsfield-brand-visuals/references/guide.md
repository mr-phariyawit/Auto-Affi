# Focused guide

## Source lookup

Relevant Bible IDs: `A09 A09.02 A09.03 A09.04 A09.05 A09.06 A09.07 A09.08 A09.09 A06.02 B11 E3 E4 E5`. Choose the needed IDs; do not load the entire list by default.

Use the shared helper at `../higgsfield-bible-director/scripts/bible_lookup.py` with repeated `--section ID`, or inspect `../higgsfield-bible-director/references/bible-snapshot.md`. These paths are relative to the skill root; resolve before calling. The helper is local and read-only. Shared contract: `../higgsfield-bible-director/references/operating-contract.md`.

## Operating notes

Verify current tools and plugin names before doing setup. The task of learning from a course is not authorization to install the course's integrations. Prompts written from these notes are authored synthesis, not course prompts; reusable templates live in the director's assets dir. Inventing a brand = label outputs as proposals; selling an existing SKU = preserve confirmed geometry and exact label/artwork, never borrow details from generated variations. Apply Auto-Affi entry rules before any new paid production. Prices/credits below are as recorded in the course, not current fact.

- Order is BRAND -> PRODUCT -> ADS; keep a checklist page holding the approved logo and palette (course palette: accent #d1fe17 + #000000 + #ffffff). [A09.L02 t=00:00] [A09.L02 t=01:10] [A09.L02 cue c2a]
- Let Claude write every prompt from a one-line idea plus references, inside one long thread so context carries forward. [A09.L02 t=00:05–00:15] [A09.L06 t=00:17–00:58] [A09.L02 t=01:35]
- Logo meta-prompt: `Give me a prompt for a logo for a fashion brand called <NAME>. Accent color <#hex>. <Flat vector, minimal>.`; keep the mark simple and memorable, not clever. [A09.L02 cue c2a] [A09.L02 t=00:16–00:26]
- Generate cheap options first (Soul Cinema, 4 images at half a credit as recorded in the course), then polish the winner by edit instead of regenerating. [A09.L02 t=00:26–00:34] [A09.L03 t=00:50–01:02]
- Edit with an explicit keep-list: `Recreate this logo exactly — same <mark>, same <background>, same composition and proportions — but change only <element>: <change + angle/direction>. Keep the same <font>, <colour>, size and position.` [A09.L02 cue c2d]
- Variation sheet: `Use the provided logo to generate a clean visual mini-guide.` + numbered variants (monogram / icon / horizontal lockup) + `Present each variation on: white background, black background`. [A09.L02 cue c2f] [A09.L02 cue c2e]
- Failure mode: AI wordmarks come out tiny or misspelled (one Soul Cinema tile read "hioos" for "higgs"); AI-written hex can be mistyped (#D1EF17 for #d1fe17) - diff hex against the master. [A09.L02 t=00:50] [A09.L03 cue c3j]
- Put the brand hex in every brief and lock product colours in a sentence; keep the brand colour the one saturated hue in a monochrome world. [A09.L03 t=01:59–02:04] [A08.L06 cue cue-l6-skincare] [A09.L04 cue c4a]
- Product pipeline: Claude mockup prompt -> Soul Cinema 16:9 x4 -> pick one -> NBP logo swap with `Change the logo in image 1 with a logo from an image 2`, then short fixes like `make the icon smaller`. [A09.L03 t=01:48–01:56] [A09.L03 t=01:00] [A09.L03 t=01:03–01:08]
- Budget a logo-swap pass for every item: Claude mockup prompts invent placeholder brands (AXIS, VALE, X-in-circle). [A09.L03 cue c3b] [A09.L03 cue c3d] [A09.L03 cue c3h]
- Apparel mockup structure: header (flat lay, ghost mannequin, #FFFFFF, studio light) -> FABRIC / SILHOUETTE / BASE COLOR / CONSTRUCTION / LOGO / BACK sections; state absences explicitly ("No drawstrings, no cords") and lock framing ("nothing cropped"). [A09.L03 cue c3b] [A09.L03 cue c3d]
- Multi-angle products: `ONE original <product> in 4 views, 2x2 grid` on white, describing the logo by shape, not name. [A09.L03 cue c3f] [A09.L03 t=01:59–02:19]
- A single flat product photo is not enough - the model guesses unseen angles and hallucinates mid-scene; build a sheet: `Make a product sheet with <views> views of the <product> from @image_1.` (GPT Image 2 bar as recorded: Auto, High, 2K, 4/4, 28). [A06.L02 t=00:23] [A06.L02 cue product-sheet-prompt] [A06.L02 frames t=00:44]
- Give the brand one instantly recognizable hero product and design new pieces to bridge existing ones. [A09.L03 t=01:15–01:23] [A09.L03 t=02:37–02:57]
- Marketing Studio: create the product from the site URL or "Create manually", start presets zero-prompt, add a Claude-written prompt only for more control; product names scraped from the site are spoken by the avatar, so name them well. [A09.L04 t=00:41–00:55] [A09.L04 t=01:16–02:00] [A09.L09 t=01:35–01:38]
- Variants: keep character, product and preset fixed and change only the prompt; run one preset per product for a test set. [A09.L06 t=03:02–03:08] [A09.L05 t=00:46–00:56]
- QC every output for logo continuity on every surface (sole, jacket back, front, glasses), and watch for invented garments (a non-brand black coat appeared in a glasses-only try-on). [A09.L06 t=02:18–02:33] [A09.L04 t=04:30–04:52]
- Video-only failure signals: prompts repeat "NO bag, NO backpack" per clip and static-camera locks; avatars may start in their own outfit; background signage renders as garbled text. [A09.L04 cue c4b] [A09.L04 t=03:58] [A09.L06 frames t=03:17]
- Feed and web stills belong in NBP, not Marketing Studio; web studio shot: `Professional studio picture, model wearing all of these clothes. Monochromatic background, side profile view.` with each garment as a separate reference. [A09.L08 t=00:29] [A09.L08 cue c8a]
- Keep one ambassador across feed, web and ads; swap them in by edit (`Change the girl in [image 1] into a girl/guy in [image 2], keep the outfit`) instead of reshooting. [A09.L08 t=00:42–00:48] [A09.L08 t=01:50]
- AI prompts can contradict the settings bar (prompt says 9:16 while bar is 3:4; cues ask 2.39:1 on a 9:16 bar) - the bar wins; check it. [A09.L08 frames t=00:40] [A09.L06 cue c6a]
- Packaging: `Use the provided logo to design a premium packaging concept for a clothing collection called "<NAME>".` + concept direction + Bag/Box sections; feed the result to Unboxing as "additional assets". [A09.L09 cue c9a] [A09.L09 t=00:53–01:11]
- Ad facts (price, phone, promotion) must never be model-filled, and AI content must be labelled. [A07.L05 article] [A12.L05 t=00:50]

## Known contradictions

- A09 cue c3j asks for a black backdrop and "No logos", but the final image is on white with a logo - cues are not always the final prompt (also true of the pasted TV Spot prompt vs c7a). [A09.L03 cue c3j] [A09.L07 frames t=00:47]
- Roko's origin: the article says preset avatar, the screen shows an uploaded file. [A09.L06 t=00:45–00:52]
- Stress-test ads: v1 warned they are not durability evidence; the course itself presents them as proof content - treat as depiction, not substantiation. [A09.L05 t=01:44]
- Marketing Studio credit readouts are only partly legible ("180 165"); the only clearly stated costs are "half credit" and "UGC under $5", as recorded in the course. [A09.L04 frames t=00:02] [A09.L02 t=00:26–00:34]
- The Claude skill file and "prompts in the description" are not in the course materials. [A09.L04 t=02:05] [A09.L08 t=00:55]
- Negatives: A09 still prompts use heavy "No ..." lists; the no-negative rule was taught for Seedance only. [A02.L09 cue ball-prop-sheet] [PB.38]
- Sneaker views: spoken "side, top, bottom, back" vs cue side/top/heel/sole (audit follows cue c3f). [A09.L03 cue c3f] [A09.L03 t=02:19]
