# Focused guide

## Source lookup

Relevant Bible IDs: `A01.03 A06.02 A06.03 A06.04 A06.05 A06.06 A06.07 A06.08 A06.09 A06.12 A15.05 B1 B2 B3 B4 D3 D6 E1 E3 E4 E5`. Choose the needed IDs; do not load the entire list by default.

Use the shared helper at `../higgsfield-bible-director/scripts/bible_lookup.py` with repeated `--section ID`, or inspect `../higgsfield-bible-director/references/bible-snapshot.md`. These paths are relative to the skill root; resolve before calling. The helper is local and read-only. Shared contract: `../higgsfield-bible-director/references/operating-contract.md`.

## Operating notes

Verify current tools and plugin names before doing setup. The task of learning from a course is not authorization to install the course's integrations. New prompts below are authored synthesis from course templates; reusable templates (`asset-register.csv`, shotlist, take/QC) live in the director's assets directory. If only a sheet is requested, deliver the sheet plus its role and uncertainties; do not force a whole campaign.

- Order is script -> assets (characters, locations, props, products) -> shot list -> video; never generate scenes before assets are locked. [A01.L01 article] [A06.L01 article]
- Start with a dependency register (ID | role | source | version | observed facts | uncertainty | used shots), organised as folders per scene/asset or a table naming each reference and the scenes that use it. [A01.L03 t=00:00-00:17] [A06.L02 frames t=00:20]
- Every recurring element needs one approved reference before motion; one-off extras and single-use props can be a one-line text description. [A15.L01 article] [A02.L18 t=01:03-01:13]
- Spend by role: the hero gets careful sheets, secondary characters a quick one-line pass picked on "energy"; a villain must read as the problem at first sight. [A06.L04 t=00:00] [A06.L04 t=00:27] Secondary cast template: `An [role] in his [age] with a [body trait], wearing a [wardrobe].` [A06.L04 cue boss-prompt]
- Character sheets go on a plain grey background (host reports a higher "win rate"); busy backgrounds steal attention and cut usable results. [A06.L03 t=00:38] [A06.L03 t=00:41]
- Meta-prompt for Claude: `create a prompt for a character sheet of a [age/gender] with [face trait] — two panels, close-up and full body - front and back, on a grey background.` [A06.L03 cue character-sheet-prompt] With a real person, attach front + left/right profile refs and ask for three views (full front, full back, close-up) on clean light grey. [A01.L03 cue 3-view-character-sheet]
- One sheet = one face: erase the duplicate face (`Erase the [element: face] from the [panel: full-body shot] on the [location: right panel].`), or ask for HEADLESS front/back bodies up front. [A06.L06 cue erase-face-prompt] [A06.L12 frames t=02:00]
- Split the work: Soul Cinema for raw passes/many takes, GPT Image 2.0 for edits and the clean final sheet; Nano Banana Pro was chosen in A15 for holding the face. [A01.L03 t=04:49-04:58] [A15.L02 t=03:45] When a candidate is close, edit with a keep-list ("change only X") instead of regenerating. [A09.L02 t=00:26–00:34] [A04.L03 t=00:45]
- Every edit costs quality: GPT Image edits softened Soul Cinema skin into "AI slop"; fix by compositing the new layer under the original with a mask. [A06.L08 t=01:06] [A06.L08 t=01:29]
- Keep at least two finalists and decide with a motion test, not a still; faces that look good still can break the moment they move. [A06.L03 t=00:59] [A06.L03 t=01:00]
- Motion tests use one fixed simple prompt with every noun bound to an @reference and change one variable at a time (hero OR location): `the hero [@image ref] walks into the kitchen [@image ref], headphones [@image ref] on, dance a little` [A06.L05 cue kitchen-test-prompt] [A06.L05 t=01:08]
- Products need multiple angles on neutral grey; a single flat photo makes the model guess and hallucinate mid-scene: `Make a product sheet with [view list: front and 3/4 perspective] views of the [product] from @image_1.` [A06.L02 t=00:26] [A06.L02 cue product-sheet-prompt]
- Props get one clean multi-angle sheet each, covering only camera-needed angles, with no motion test because props do not "act". [A06.L09 t=00:08] [A06.L09 article] Prop turnaround in one image: `Split-screen sheet, same <prop> twice: LEFT <angle + features>; RIGHT <angle + features>. <materials>, <environment>, <light>. Photoreal.`; brand colours as exact hex in the edit prompt. [A01.L03 cue split-screen-ship-assets] [A01.L03 cue customize-assets-in-gpt-image]
- Locations at 3/4, never head-on; a cheap or plastic location ruins every shot and no prompting fixes it later. [A06.L05 t=00:30] [A06.L05 t=00:04] Location template: `[Room type], [camera angle 3/4], [light: bright clean daylight], [look: high-end commercial look].`; on-screen simple form was "Pedestrian street, 3/4 view". [A06.L05 cue kitchen-location-prompt] [A06.L07 frames t=01:10]
- Test each location in video first: a beautiful still can lose because light goes flat in motion, and dark rooms swallow faces. [A06.L07 t=00:45] [A06.L05 t=01:27] Edit a locked location so it supports the scene action (stove, door), ending with "Keep everything else the same." [A06.L05 t=01:55] [A06.L05 cue kitchen-edit-prompt]
- Build a reverse-angle or separate location asset when the camera turns; ask which reference explains the frame after a 180-degree turn. [A01.L07 t=01:41-01:53] [A16.L01 article]
- Pin geography with images (schematic map, top-down drawing), not paragraphs; Seedance does not remember positions across generations. [A06.L13 t=00:35] [A02.L12 t=00:04-00:30]
- Wardrobe: test in plain black first, dress only after character and location lock; an unlocked outfit reference gives different trousers/shoes every take. [A06.L08 t=00:00] [A06.L12 t=00:38]
- State changes (dry -> wet, torn shirt) get a new reference, not words ("images are cheap, videos aren't"): `same character sheet, [state], [visible cue 1], [visible cue 2].` [A06.L12 t=01:09] [A06.L12 t=01:30] Record state transitions (beat | before | change | after | receiving shot) and bind refs per cut, e.g. dry @s_hero for the run, @s_hero_wet from the final stop. [A06.L12 t=01:58] [A06.L12 t=01:20]
- Continuity is our job, not the model's; bridge geography jumps with a travel shot in a separate location instead of "teleporting". [A15.L05 t=00:00] [A15.L05 t=00:21] Keep state continuity: wet decks after hits, lost shoes/torn shirts paid off at the end, debris must not vanish between frames. [A01.L06 t=02:43-02:54] [A05.L06 t=01:00]
- Pull matching stills from one continuous "statics" video and save each frame as an element named by function (position lock, steering-wheel lock). [A15.L05 t=01:44] [A15.L05 t=02:24]
- Name every asset as an @tag identical in Claude and Higgsfield Elements (Character / Location / Prop) so pasted prompts attach references. [A01.L03 t=05:10-05:26] [A01.L03 frames t=05:20] Upload assets for Claude to see instead of describing them, and state which reference serves which cut. [A06.L10 t=01:23] [A06.L12 t=01:56]
- Video-only: the full Claude-written sheet prompt (85mm, "nothing cropped", 1.85m) and outfit prompt (identity block + "No visible brand logos anywhere") appear only on screen. [A06.L03 frames t=00:15] [A06.L08 frames t=00:25] PRO TIP card "Keep only the close-up face on the character sheet."; failure takes were marked with red/green overlays (over-lighting, misplaced map). [A01.L03 frames t=01:25] [A01.L03 t=03:00-03:25]
- Credits as recorded in the course only: GPT Image 2 at 4/4 showed 28, a 1/4 edit 7; Soul Cinema was recorded as 8 images per 1 credit. [A01.L03 frames t=01:03] [A01.L03 frames t=01:43] [A06.L03 t=00:47]

## Known contradictions

- Cue text is not always the final prompt: the A01 sheet cue says RED durag and mixes "21:9"/"16:9", but the on-screen sheet is YELLOW; check the real chip before generating. [A01.L03 cue 3-view-character-sheet-recreate] [A01.L03 t=01:05-01:15]
- Reference images beat text: A04 asked for cel-shaded anime but got paper-cutout following the keyframe. [A04.L03 cue scene1-animated] [A04.L10 t=00:50-01:10]
- Outfits in results can follow the prompt rather than the sheet (khaki T-shirt on sheet, maroon/pink kit in 8B). [A02.L18 t=01:05-01:30]
- Soul Cinema pricing was recorded inconsistently across courses (8 per credit vs 4 = 0.5 credit). [A01.L03 t=03:01-03:31] [A04.L03 t=00:15]
- A06 boss: cue links nano-banana-pro but video shows AI Cast; notes say "glasses-less" while @boss later has thin rimless glasses. [A06.L04 cue boss-prompt] [A06.L10 frames t=02:00] A06 location cue links soul_cinematic but the UI shows "Cinematic Locations"; same model or preset is unclear. [A06.L05 cue kitchen-location-prompt]
- Evidence gaps: skill files are absent from course materials, and some shots (A15 steering-wheel close-up) are not in sampled tiles. [A06.L10 cue download-shotlist-skill] [A15.L05 t=02:24]
