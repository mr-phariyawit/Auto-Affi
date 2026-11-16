# 3D-rendered-as-pixel-art: games, technique, and tools for short pixel-style cooking animation

Research date: 2026-11-16. Evidence tags used on every finding:

- **[P]** = verified from primary source, page opened in this session (developer's own article, vendor page, engine docs)
- **[S]** = secondary (press write-up, search-result summary of a page I did not open, third-party tutorial, forum post)
- **[U]** = unverified / from the researcher's memory, no page opened. These are kept out of "Cited Findings" and listed under "Gaps" so the writer does not present them as fact.

Note on method: about 30 search/fetch calls were made. Several target pages were not reachable or not opened (t3ssel8r's videos, Madalaski's tutorial, aarthificial's devlogs, Unity/Blender manual pages, PixelLab and Retro Diffusion official pricing pages, HD-2D developer talks). Those items are flagged as gaps, not filled in.

---

## 1. Which games render 3D as pixel art, or mix sprites with 3D? (with cooking highlighted)

### Takeaway
Only three titles on the candidate list have a developer statement, opened in this session, that describes the 3D/pixel split: Dead Cells (3D models pre-rendered to low-res sprites), Eastward (hand-drawn pixel assets rebuilt in a 3D scene with hand-painted bump maps), and Dave the Diver (developer says it blends 2D pixels and 3D art, but does not say which element is which). Everything else on the list could not be confirmed from a primary source in this session and is listed under Gaps as unverified.

### Cited Findings

**Dead Cells — Motion Twin, article dated 2018-01-25 (engine not stated in the article)**
- [P] Models are built in 3DS Max and exported as FBX; a "little homebrew program, developed for this very specific task" renders the mesh "in a very small size and without antialiasing" to obtain the pixel look — [Game Developer, Thomas Vasseur, "Art Design Deep Dive: Using a 3D pipeline for 2D animation in Dead Cells"](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- [P] Each animation frame is exported as a PNG together with its normal map, so the volume can be shaded in-game with "a basic toon shader" — [same article](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- [P] Animation approach: set key poses first with as few frames as possible; interpolation frames are added "before or after the key frames", never between them, so attacks are essentially pose-to-pose with VFX supplying the motion — [same article](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- [P] Stated benefit: old 3D assets are reused for new monsters, saving "hundred of hours of work"; retakes are done by moving keyframes rather than redrawing — [same article](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- [S] A Steam developer reply reportedly says most animations are 3D pre-rendered with a pixel-art shader while some simpler ones are hand-made (search-result summary; thread not opened) — [Steam discussion](https://steamcommunity.com/app/588650/discussions/0/2741975115060630076)
- [S] 80.lv republished the same pipeline as a case study (not opened) — [80.lv](https://80.lv/articles/case-study-dead-cells-character-art-pipeline)
- What is 3D / what is sprite: characters and monsters are authored in 3D but **shipped as 2D sprite frames + normal maps**. It is a pre-render pipeline, not a real-time 3D-to-pixel renderer. Cooking: none.

**Eastward — Pixpil, article dated 2021-10-11, in-house engine**
- [P] Base art is drawn in Aseprite by the artist; each asset is split into layers by structure (e.g. rooftop separated from wall) — [Game Developer, "Eastward's creators share insights on making pixel art adventures"](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
- [P] The 2D assets are then rebuilt in a 3D environment, so the game is a 3D game seen from a 2D perspective; bump maps are hand-painted one asset at a time so they light correctly — [same article](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
- [P] Pixpil uses its own engine (the article spells it "Maoi"); shader textures and lighting convey weather and time of day — [same article](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
- [S] Red Bull describes the engine as a Pixpil homebrew engine fused with the open-source MOAI framework (search summary, page not opened) — [Red Bull](https://www.redbull.com/my-en/eastward-interview)
- What is 3D / what is sprite: **hand-drawn pixel sprites placed in a 3D scene and lit with hand-painted bump maps**. No 3D character models are described. The opened article does not mention cooking.

**Dave the Diver — Mintrocket (Nexon), Unity + URP**
- [P] Unity's case study says the game "blends 2D pixels and 3D art"; lead game designer Chanhee Woo: "It was very appealing to us to have both the arcade-like action of 2D with the spatial impression of 3D." — [Unity case study](https://unity.com/case-study/dave-diver)
- [P] The team used URP (a platform-specific Render Pipeline Asset per platform), Shader Graph so artists could author shaders, and Cinemachine for cameras. Unity version is not stated — [Unity case study](https://unity.com/case-study/dave-diver)
- [P] The case study **does not state which elements are sprites and which are 3D** — [Unity case study](https://unity.com/case-study/dave-diver); same gap in the press summary — [Game World Observer, 2023-12-04](https://gameworldobserver.com/2023/12/04/dave-the-diver-unity-2d-3d-graphics-optimization-mintrocket)
- [S] An interviewer describes it as 2D pixel-art elements combined with low-poly 3D models with smoother textures (search summary, page not opened) — [Software Engineering Daily, 2024-04-09](https://softwareengineeringdaily.com/2024/04/09/developing-dave-the-diver-with-jaeho-hwang-and-minsuk-cha)
- Appears to be: pixel-art characters over 3D-modelled environments/creatures. This is a hybrid, not 3D characters rendered as pixels.

**A Short Hike — Adam Robinson-Yu (adamgryu), Unity**
- [S] The pixel effect is described as rendering the world to a very small render texture and having a second camera display it enlarged with point filtering, a trick learned from a Unity plug-in called GB Camera (third-party summary of the GDC talk; talk itself not opened) — [80.lv GDC postmortem summary](https://80.lv/articles/gdc-a-short-hike-postmortem); talk listing — [GDC Vault, "Crafting A Tiny Open World: 'A Short Hike' Postmortem"](https://gdcvault.com/play/1026613/Independent-Games-Summit-Crafting-A)
- [S] A forum comment says the game uses ordinary 3D models with reduced-palette textures, renders to a texture, then applies a colour-grading post-process — [itch.io forum post](https://itch.io/post/2065934)
- What is 3D / what is sprite: appears to be **fully 3D with a low-resolution render target** (real-time pixelation). No cooking.

**t3ssel8r (unreleased work) and followers**
- [S] t3ssel8r published a video on animating for 3D pixel-art games; 80.lv quotes: "Animating convincingly in this style is a little different from typical 3D game animations" (article dated 2021-06-29; game and engine not named in it) — [80.lv](https://80.lv/articles/tips-on-convincing-animations-for-3d-pixel-art-games)
- [S] A 2026 arXiv paper cites t3ssel8r's "3D pixel art rendering in Unity" video as the reference for snapping to the screen grid (search summary; paper not opened) — [arXiv 2603.14587, "Texel Splatting: Perspective-Stable 3D Pixel Art"](https://arxiv.org/abs/2603.14587)
- [P] David Holland's Godot project names t3ssel8r's Unity work as its main inspiration — [David Holland, "3D Pixel Art Rendering", 2024-09-24, updated 2025-05-26](https://davidholland.netlify.app/articles/3d-pixel-art-rendering)

**Cooking / restaurant games found by search**
- [S] Chef RPG is described as a 2D pixel-art restaurant game (so no 3D-to-pixel renderer) — [Chef RPG BackerKit updates](https://chef-rpg.backerkit.com/hosted_preorders/project_updates)
- [S] Pixel Plate is a 2D restaurant game made in Unity — [itch.io](https://bearswithcares.itch.io/pixel-plate)
- [S] Restaurantario is a low-poly 3D restaurant game, not pixel-styled — [itch.io](https://seasaltedtoaster.itch.io/restaurantario)
- [S] A custom Unity render pipeline by "Red Giraffe" that turns 3D scenes into pixel art was covered by 80.lv; the search result does not say it is a cooking game — [80.lv](https://80.lv/articles/custom-unity-render-pipeline-transforms-3d-scenes-into-pixel-art)

### Inferences
- The candidate list falls into four distinct technical families, and only the first two are true "3D rendered as pixels": (a) **offline pre-render to sprites** (Dead Cells), (b) **real-time low-res render target** (A Short Hike, t3ssel8r, David Holland), (c) **pixel sprites placed in a 3D lit scene** (Eastward, HD-2D family, Dave the Diver), (d) **2D pixel art with dynamic lighting** only. A short non-interactive video maps most directly onto (a), because frames are rendered offline anyway.
- Dead Cells is the strongest precedent for a solo video creator: one person produced all models and animation, and the pipeline's stated purpose was to avoid redrawing frames on every retake.

### Gaps
The following were on the brief's check-list but **no developer source was opened**; treat every line as **[U] from memory, not verified**:
- Octopath Traveler (Square Enix / Acquire, 2018, Unreal Engine 4), Triangle Strategy (2022), Star Ocean: The Second Story R (2023): "HD-2D" = pixel-art character sprites in 3D environments with depth of field and lighting. One search for a developer talk returned nothing usable; only a [4Gamer article](https://www.4gamer.net/games/210/G021013/20241105005/) surfaced and it was not opened.
- Sea of Stars (Sabotage Studio, 2023, Unity): hand-drawn pixel art with a custom dynamic-lighting system; has campfire cooking. The only hit was a Spanish forum article ([foro3d](https://foro3d.com/2026/julio/sea-of-stars-pixel-art-de-16-bits-con-iluminacion-dinamica-en-unity.html)), not opened, with no implementation detail.
- Eastward's cooking minigame, and Dave the Diver's sushi-restaurant loop: widely known gameplay features, but not stated in the two developer articles opened.
- Cuisineer (BattleBrew Productions, 2023): appears to be a 3D/cel-shaded isometric game, not pixel art. Not checked.
- Mina the Hollower (Yacht Club Games): hand-drawn Game Boy Color-style pixel art. Not checked.
- Loddlenaut (Moon Lagoon, 2023): low-poly 3D with a low-resolution retro look. Not checked.
- The Last Night (Odd Tales): pixel sprites in 3D scenes with heavy post-processing; unreleased. Not checked.
- Songs of Conquest (Lavapotion, Unity): pixel sprites on 3D terrain. Not checked.
- Unsighted (Studio Pixel Punk): pixel art with lighting. Not checked.
- Lunacid (KIRA): low-res PS1-style 3D, not pixel-art sprites. Not checked.
- Shadows of Doubt (ColePowered Games, Unity): voxel-style 3D. Not checked.
- Lucas Pope (Return of the Obra Dinn 1-bit dithering stabilisation; Mars After Midnight): relevant to dithering stability under motion. His devlog was not opened.
- Guilty Gear Xrd (Arc System Works, GDC 2015 talk): 3D made to look 2D by stepped/limited animation and hand-edited normals. Relevant principle only; talk not opened.
- Tiny Glade: excluded as instructed (not pixel art).
- Engine of Dead Cells is not stated in the opened article.

---

## 2. Is there a cooking-focused game with fully 3D characters rendered as pixel art?

### Takeaway
None was found. Stated plainly: in this session's searches, no cooking or restaurant game was identified in which fully 3D characters are rendered through a 3D-to-pixel renderer. The closest matches are hybrids or non-cooking games.

### Cited Findings
- [S] The dedicated search for a cooking game with a 3D-to-pixel renderer returned only: 2D pixel restaurant games ([Chef RPG](https://chef-rpg.backerkit.com/hosted_preorders/project_updates), [Pixel Plate](https://bearswithcares.itch.io/pixel-plate)), a low-poly non-pixel restaurant game ([Restaurantario](https://seasaltedtoaster.itch.io/restaurantario)), and a generic 3D-to-pixel Unity pipeline not tied to cooking ([80.lv](https://80.lv/articles/custom-unity-render-pipeline-transforms-3d-scenes-into-pixel-art)).
- [P] Closest by technique (no cooking): Dead Cells — 3D characters pre-rendered to pixel sprites — [Game Developer](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- [P] Closest by subject (food-themed, hybrid 2D pixel + 3D, split not specified by the developer): Dave the Diver — [Unity case study](https://unity.com/case-study/dave-diver)
- [P] Closest by subject with pixel sprites in a 3D-lit scene: Eastward — [Game Developer](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
- [S] A separate, non-pixel precedent for appetising stylised 3D food: a developer's custom "soup shader" for anime-style ramen (search hit, not opened) — [Automaton](https://automaton-media.com/en/?p=13942)

### Inferences
- "Not found" here means not found in roughly four targeted searches, not proven absent. Small itch.io/Steam titles could exist. The gap itself suggests the look is uncommon for cooking content, which is a differentiation opportunity for a video channel rather than evidence the look does not work.

### Gaps
- No exhaustive Steam tag search ("Cooking" + "Pixel Graphics" + "3D") was run.
- Several itch.io comments praising "pixel rendering of the 3D environment" surfaced without game titles attached; not followed up.

---

## 3. How the look is achieved (pipeline elements)

### Takeaway
Two developer-authored descriptions were opened and they agree on the core recipe: render the 3D scene small with no anti-aliasing, shade it with toon/stepped lighting, and add one-pixel outlines from depth and normals; for a moving camera, snap the camera to a texel-sized grid and shift the output back by the snap error. Blender Studio's own test confirms the same elements and documents where Blender's compositor fights the look.

### Cited Findings

**Low-resolution render with no anti-aliasing**
- [P] Dead Cells renders the mesh "in a very small size and without antialiasing" — [Game Developer](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- [S] A Short Hike: tiny render texture enlarged with point (nearest-neighbour) filtering — [80.lv summary](https://80.lv/articles/gdc-a-short-hike-postmortem)
- [P] David Holland's Godot demo mentions 640x360 as a working resolution (stated in the god-ray section; the main render resolution is not given explicitly) — [David Holland](https://davidholland.netlify.app/articles/3d-pixel-art-rendering)

**Toon / stepped lighting**
- [P] Dead Cells exports a normal map per frame and shades it with "a basic toon shader" — [Game Developer](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- [P] David Holland: "It's toon lighting!"; directional-light attenuation is smoothed to reduce shadow flicker, and normal noise is used against shadow popping — [David Holland](https://davidholland.netlify.app/articles/3d-pixel-art-rendering)
- [P] Blender Studio test: a Color Ramp set to constant interpolation produces stepped value changes, combined with a screen-space Bayer (ordered dither) filter, via a modified version of Lucas Roedel's free Pixel Art shader add-on — [Blender Studio, Rik Schutte, "Exploring 3D Pixel Art in Blender 4.2", 2024-06-06](https://studio.blender.org/blog/3d-pixel-art-in-blender)

**Outlines from depth and normals**
- [P] David Holland: edge detection samples screen depth and normals; the kernel is only the up/down/left/right texels so the line stays one pixel thick; depth drives silhouette outlines and normals drive inner edge highlights; "Convex edges are isolated by taking the cross product of neighbouring texels, and grading it against a number of arbitrary heuristics." — [David Holland](https://davidholland.netlify.app/articles/3d-pixel-art-rendering)
- [S] A ready-made Godot implementation exists: Leo Peltola's "3D Pixel art outline & highlight Shader" (not opened; licence not checked) — [godotshaders.com](https://godotshaders.com/shader/3d-pixel-art-outline-highlight-post-processing-shader/)

**Camera: orthographic projection and texel snapping (pixel "creep"/"swimming")**
- [P] David Holland: the camera is snapped to a view-aligned, texel-sized grid to remove pixel creep, then the rendered output is shifted back in screen space by the snap error to restore smooth motion — [David Holland](https://davidholland.netlify.app/articles/3d-pixel-art-rendering)
- [S] Snapping works under orthographic projection because every pixel shifts by the same amount, so one snap corrects all of them; perspective projection breaks this (search summary of the paper) — [arXiv 2603.14587](https://arxiv.org/abs/2603.14587)
- [S] Camera snapping keeps pixels stable but can leave a slight stutter — [Otavio Peixoto, 3D Pixel Art portfolio page](https://otaviopeixoto1.github.io/portfolio/3DPixelArt)
- [S] ProPixelizer's docs call "creep" the best-known 3D pixel-art artefact and advise checking the orthographic projection with a test cube — [ProPixelizer docs](https://propixelizer.github.io/docs/tips_and_tricks/artefacts)
- [S] A Reddit thread notes that if objects and camera are not snapped to pixels, outlines become visually noisy when objects move — [r/godot thread](https://redlib.cypherpunktools.com/r/godot/comments/1k6nzj7/does_anyone_have_any_good_tutorials_on_this_kind)
- [P] Blender Studio hit the same problem: viewport pixels and the Grease Pencil pixelate effect did not align when the camera moved, so "the camera had to stay static for consistent results"; pixels were seen jumping to match the grid — [Blender Studio](https://studio.blender.org/blog/3d-pixel-art-in-blender)

**Limited frame count / pose-to-pose animation**
- [P] Dead Cells: as few keyframes as possible, interpolation only before or after keys, never between — [Game Developer](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- [S] t3ssel8r: animating in this style "is a little different from typical 3D game animations" (topics listed: references, animation passes, importing/previewing, tweaking) — [80.lv, 2021-06-29](https://80.lv/articles/tips-on-convincing-animations-for-3d-pixel-art-games)

**Dithering and palette**
- [P] Blender Studio: screen-space Bayer filter combined with constant-interpolation Color Ramp — [Blender Studio](https://studio.blender.org/blog/3d-pixel-art-in-blender)
- [P] PixelOver lists dithering and indexation (palette reduction) as layer filters — [PixelOver Steam page](https://store.steampowered.com/app/1762550)
- [S] A Short Hike reportedly uses reduced-palette textures plus a colour-grading post-process rather than hard per-pixel quantisation — [itch.io forum post](https://itch.io/post/2065934)

### Inferences
- For a video with a **locked-off camera**, the hardest real-time problem (camera snapping, sub-pixel error compensation) disappears. Blender Studio's own note that the camera "had to stay static" is a constraint for games but is the normal case for a top-down or three-quarter cooking shot. Recommending static or hard-cut cameras over pans avoids most "pixel swimming".
- Moving **objects** still creep even with a static camera: a pan, hand, or ingredient that moves less than one texel per frame will shimmer along its edges and outlines. The sources imply two mitigations: move things in whole-texel steps, and hold poses (pose-to-pose, low frame count) so sub-texel in-betweens are never shown.
- Per-frame normal maps (Dead Cells) show that lighting can be decided after the pixel render. For video this is optional; baking toon lighting into the low-res render is simpler.

### Gaps
- t3ssel8r's original videos (the commonly cited primary source for camera snapping and the overall look) were **not opened**; only citations to them were seen. [U]
- Madalaski's Unity tutorial and aarthificial's "Astortion" devlogs were **not searched or opened**. David Holland's article references "aarthifical" as an influence, but no detail was extracted. [U]
- Unity manual pages (URP renderer features, Pixel Perfect Camera, Recorder) were not opened. [U]
- No source was opened that gives a specific frame-hold number ("on twos/threes" at 24 fps = 12/8 unique frames per second). The principle is supported by Dead Cells' pose-to-pose description; the exact numbers are convention, not a cited finding. [U]
- No opened source discusses temporal stability of dithering under motion (Lucas Pope's Obra Dinn devlog is the known reference; not opened). [U]

---

## 4. Tools a solo creator can use to make pixel-styled video without shipping a game

### Takeaway
Three routes are documented well enough to act on: Blender 4.2+ (free; EEVEE pixel size + AA off + stepped Color Ramp + Bayer dither, with a known compositor anti-aliasing caveat), Godot 4 (free; pixel/outline shaders plus Movie Maker mode for frame-perfect offline export to PNG sequence), and PixelOver (about USD 19.99, Early Access v0.19.3; imports 3D models, applies dithering/indexation, exports images/GIF/spritesheets). AI pixel tools exist but sources consistently report inconsistent pixel grids and flicker; official pricing and licence pages for them were not verified.

### Cited Findings

**Blender (free, open source)**
- [P] Blender 4.2 test by Blender Studio: EEVEE Next with viewport pixel size 4x (Performance settings), anti-aliasing disabled in viewport preferences, Grease Pencil "Pixelate" effect at pixel size 40 to match, brush radius 0.02 so one unit maps to one pixel — [Blender Studio, 2024-06-06](https://studio.blender.org/blog/3d-pixel-art-in-blender)
- [P] Caveat: the compositor's Pixelate filter "includes anti-aliasing, which softens edges"; the author says developers planned an option to disable it. The effect in that test only works in EEVEE Rendered viewport mode — [Blender Studio](https://studio.blender.org/blog/3d-pixel-art-in-blender)
- [P] Shading used a modified version of Lucas Roedel's free Pixel Art shader add-on (Bayer filter + constant Color Ramp) — [Blender Studio](https://studio.blender.org/blog/3d-pixel-art-in-blender)
- [S] BNPR guide recommends low output resolution, render samples = 1 for crisp aliased pixels, and bloom disabled — [BNPR "Pixel Art Basics"](https://bnpr.gitbook.io/bnpr/pixel-art/pixel-art-basics)
- [S] Common compositor recipe: scale render down (e.g. to 1/5), Pixelate node, scale back up — [GameFromScratch, "Easy Sprite Art In Blender Tutorial"](https://gamefromscratch.com/easy-sprite-art-in-blender-tutorial/)
- [S] Add-ons that surfaced (pages not opened, price/licence not verified): Lospec Blender Toolkit, described as a free collection for low-spec art — [Lospec](https://lospec.com/blender-toolkit); "Pixel Kit – One-Click Pixel Art Renderer", paid — [Superhive Market](https://superhivemarket.com/products/pixel-kit---one-click-pixel-art-renderer); "Pixel – A Cheat Code For Pixel Art" — [Superhive Market](https://superhivemarket.com/products/alttab-pixel/ratings)
- [S] Isometric sprite-from-3D tutorial in Blender — [J.S. Abbott, ArtStation](https://jsabbott.artstation.com/blog/YQaAw/tutorial-creating-2d-pixel-art-style-isometric-sprites-from-a-3d-model-in-blender)

**Godot 4 (free, open source)**
- [P] Movie Maker mode records non-real-time ("offline rendering") video and audio with perfect frame pacing regardless of hardware — [Godot docs, "Creating movies"](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html)
- [P] Output formats: OGV (Theora/Vorbis, lossy, editor builds only, no transparency), AVI (MJPEG, 4 GB limit, no transparency), PNG sequence + WAV (lossless, supports transparency, intended for FFmpeg) — [Godot docs](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html)
- [P] Frame rate is a project setting (override with `--fixed-fps`); resolution follows the window size, or the viewport size when stretch mode is `viewport`; enable from command line with `--write-movie`; `--resolution` is clamped to the display resolution — [Godot docs](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html)
- [P] David Holland's full 3D pixel-art look (toon lighting, depth/normal outlines, camera snap) was built on a custom build based on Godot 4.3; he notes some limitations apply to the official build — [David Holland](https://davidholland.netlify.app/articles/3d-pixel-art-rendering)
- [S] Godot has built-in integer scaling since 4.3 — [GDQuest, "Setting up pixel art graphics in Godot 4"](https://www.gdquest.com/library/pixel_art_setup_godot4/)

**Unity**
- [P] Dave the Diver's team used URP + Shader Graph for a 2D-pixel/3D blend, showing artists without programming skills can author the shaders — [Unity case study](https://unity.com/case-study/dave-diver)
- [S] ProPixelizer is a Unity pixelisation package with documentation on artefacts (price/licence not checked) — [ProPixelizer docs](https://propixelizer.github.io/docs/tips_and_tricks/artefacts)
- [S] A written Unity URP pixelated-style tutorial exists (not opened) — [kyriota, "Unity Pixelated Art Style In URP", 2022-08-02](https://kyriota.github.io/2022/08/02/UnityPixelatedArtStyleInURP/)

**PixelOver (Deakcor)**
- [P] Current version 0.19.3; minimum price USD 19.99 on itch.io; demo can save projects but cannot export — [PixelOver itch.io page](https://deakcor.itch.io/pixelover)
- [P] Steam: Early Access since 2021-10-13, price shown as THB 400; imports images, GIFs and 3D models; layer workflow with indexation, dithering, pixel-perfect lines, colour cycling; keyframe animation, bone rigging, inverse kinematics, mesh deformation; exports images, GIFs or spritesheets (no video export listed); Windows, macOS 10.12+, Linux; requires Vulkan 1.2 — [PixelOver Steam page](https://store.steampowered.com/app/1762550)
- [P] No commercial-use licence statement appears on either store page; Steam references a third-party EULA whose text is not shown — [Steam](https://store.steampowered.com/app/1762550); [itch.io](https://deakcor.itch.io/pixelover)
- [S] 3D support history: static OBJ/VOX in v0.8 — [devlog](https://deakcor.itch.io/pixelover/devlog/317241/pixelover-08-static-3d); rigged GLTF/GLB in v0.9 — [devlog](https://deakcor.itch.io/pixelover/devlog/351366/pixelover-09-animated-3d); later FBX/DAE (search summary, devlogs not opened)
- [S] The tool is itself built on Godot — [GameFromScratch](https://gamefromscratch.com/pixelover-godot-powered-pixel-art-power-tool/)
- [P] A user report on the itch page mentions 12.8 GB memory use on macOS with an 896x1344 image — [PixelOver itch.io page](https://deakcor.itch.io/pixelover)

**AI options (2026) and their weaknesses**
- [P] Vendor explanation of the core defect: image models produce "pictures _of_ pixels"; they render around 1024x1024 so each painted "pixel" is a block of about 16x16 real pixels, and the block size can change between generations. Example given: a 158x158 sprite's new pose came back with blocks twice as wide, i.e. 80x80 when snapped, "a quarter of the detail the character started with" — [SpriteCook blog, 2026-08-26](https://www.spritecook.ai/blog/why-ai-cant-match-pixel-art-resolution) (vendor source; it sells a competing tool)
- [P] Recommended fix from the same source: detect the block grid and downscale so each block becomes one real pixel; uneven upscales or off-grid exports make the model guess — [SpriteCook blog](https://www.spritecook.ai/blog/why-ai-cant-match-pixel-art-resolution)
- [S] Community reports on video models (WAN 2.1 thread): pixels do not keep a consistent size, pixels move diagonally, and characters "look 2D but move as if in 3D" — [r/StableDiffusion thread](https://reddit.birdcat.cafe/r/StableDiffusion/comments/1kt6okc/how_to_do_flickerless_pixelart_animations)
- [S] Flicker cause per a video-model vendor: the model generates latents that a decoder turns into pixels, giving periodic flicker/warble if the latents are not smooth — [LTX blog](https://ltx.io/blog/temporal-consistency-in-ai-video)
- [S] Retro Diffusion pricing, third-party figures only: Aseprite extension one-time USD 20 (Lite) / USD 65 (full), runs locally — [Cinevva comparison guide](https://app.cinevva.com/guides/ai-pixel-art-generators); about USD 0.03 per image for RD Fast — [macmyths](https://macmyths.com/apps/retro-diffusion/)
- [S] PixelLab pricing, third-party figure only: USD 12/month, about 40 trial generations; described as strongest for skeleton animation and 4/8-direction rotation — [Cinevva comparison guide](https://app.cinevva.com/guides/ai-pixel-art-generators)

### Inferences
- PixelOver's documented outputs are images, GIFs and spritesheets, with no video export listed. For a 1080x1920 short it would be a sprite/element generator feeding a compositor (the project already uses HyperFrames), not the final renderer.
- Godot Movie Maker's PNG-sequence output combined with `viewport` stretch mode is the cleanest documented way to get an exact low-res frame (e.g. 180x320) per rendered frame with no capture drift; upscaling by an integer factor can then be done in FFmpeg with nearest-neighbour. The FFmpeg step is standard practice but was not cited from a source here.
- Blender is workable for static-camera shots but its compositor Pixelate node anti-aliases; the safer Blender route implied by the sources is to render at the true low resolution with AA/filtering off and upscale externally, rather than pixelate a high-res render.
- AI image-to-video in "pixel style" is the weakest fit for the brief: every source that discusses it reports grid inconsistency, and the fix (grid detect + downscale) is per-image, not temporally stable. A deterministic 3D render gives a genuinely fixed grid.

### Gaps
- Official Retro Diffusion and PixelLab pricing, plan limits and commercial-licence terms were **not verified**: `https://www.pixellab.ai/pricing` returned HTTP 404 and no official Retro Diffusion page was opened. Figures above are third-party and may be stale.
- Licence and price of the Blender add-ons (Lucas Roedel's Pixel Art shader, Lospec Toolkit, Pixel Kit, "Pixel") were not verified.
- PixelOver's commercial-use terms are not published on the pages opened; supported 3D formats are confirmed only via devlog titles/search summaries.
- Aseprite (current version, price, licence) and Pixel Composer were **not researched**. From memory only [U]: Aseprite is a paid pixel editor (about USD 19.99, source-available under its own EULA); Pixel Composer is a node-based pixel-art VFX compositor by MakhamDev sold on Steam/itch. Verify before citing.
- Unity Recorder and URP pixelation renderer-feature documentation were not opened. [U]
- Blender "Filter Size" pixel-filter setting and Workbench engine behaviour were not confirmed from the Blender manual. [U]
- No source was found testing 2026 image-to-video models (Veo, Kling, Seedance, Hailuo) specifically on pixel-grid stability.

---

## 5. Making food readable and appetising at low resolution

### Takeaway
The one pixel-art food tutorial opened (Raymond Schlitter / Slynyrd) says: keep food sprites around 32x32 px (48x48 for a hero dish), sample colours from real photos but keep the palette small and shared across items, and use outlines so food pops instead of looking like a downscaled photo. Specific guidance on highlights, saturation and steam was not found in pixel-art-specific sources.

### Cited Findings
- [P] Food sprites were drawn "roughly within 32x32px"; the finished ramen tutorial sprite is "roughly 48x48px" — [Slynyrd Pixelblog 30 – Food, Raymond Schlitter, 2020-09-30](https://www.slynyrd.com/blog/2020/9/30/pixelblog-30-food)
- [P] Colours were "sampled colors directly from the photos"; the artist "maintained limited colors and tried to reuse many of the same colors across all items" — [Slynyrd](https://www.slynyrd.com/blog/2020/9/30/pixelblog-30-food)
- [P] Outlines keep the food cartoony and make sprites "pop off the screen"; without outlines and with too many colours, sprites risk looking like "down scaled photos" — [Slynyrd](https://www.slynyrd.com/blog/2020/9/30/pixelblog-30-food)
- [P] Choose foods that are "easily recognizable"; "Capturing just the right colors and forms not only stimulates the eyes, it incites hunger."; self-test: "If you're not getting hungry your illustration must not be effective." The style borrows the vibrant realism of Japanese anime food illustration — [Slynyrd](https://www.slynyrd.com/blog/2020/9/30/pixelblog-30-food)
- [S] General ramp advice: a colour ramp is a brightness-ordered set of colours and a good one also shifts hue across the ramp rather than only lightening/darkening one hue (search summary) — [OpenGameArt, "Some insights about pixel art color ramps"](https://lpc.opengameart.org/node/20643)
- [S] General readability advice: cut unnecessary detail; small or low-colour pieces cannot hold fine detail (search summary) — [Pixel Grimoire, "How to start making pixel art #4"](https://medium.com/pixel-grimoire/how-to-start-making-pixel-art-4-f57f51dcfa02)
- [S] From illustration (not pixel-specific): glossy, wet-looking highlights read as appetising; keep one edge of a highlight crisp and soften the other — [Clip Studio Tips, "How to Paint Appetizing Food"](https://tips.clip-studio.com/en-us/articles/3732)

### Inferences
- The Slynyrd warning about "down scaled photos" applies directly to 3D-to-pixel food: a textured, smoothly lit 3D dish rendered small will look like a downscaled photo. The remedy the sources point to is the same as section 3: few flat colours per material (stepped ramp), a dark outline, and hand-chosen palette shared across ingredients.
- A 32–48 px food sprite inside a 180x320 frame occupies about 18–27% of frame width, which is small for a food-first short. On a 270x480 grid the same dish can be drawn at roughly 64–96 px. This suggests either the larger grid for food close-ups or separately authored larger "hero dish" sprites for insert shots. This is the researcher's arithmetic, not a sourced recommendation.
- Hue-shifted ramps (warm highlights, cooler shadows) are the general pixel-art answer to making food look fresh rather than muddy, but no opened source states this specifically for food.

### Gaps
- No pixel-art-specific source was found on **steam/smoke animation**, **specular highlight placement on food**, **saturation levels**, or **food-to-character size ratio**. The Slynyrd page shows ramen and restaurant GIFs but gives no animation advice in the text.
- The ramp and highlight items above come from search summaries or from general illustration tutorials; they should be tested rather than treated as pixel-art consensus.

---

## 6. Recommendation scaffold for a 9:16 short at 1080x1920

### Takeaway
Sources support choosing a base resolution that divides the output exactly and scaling by a whole number with nearest-neighbour; 180x320 (x6) and 270x480 (x4) both satisfy this for 1080x1920. No opened source addresses pixel fonts versus high-res text overlays or a recommended frame rate for pixel video, so those points are researcher inference and are labelled as such.

### Cited Findings
- [S] The base height must divide the target height evenly; 320x180 scales to 1080p at x6 and 640x360 at x3 (search summary) — [GDQuest, "Setting up pixel art graphics in Godot 4"](https://www.gdquest.com/library/pixel_art_setup_godot4/); [Ziva pixel-perfect resolution calculator](https://ziva.sh/tools/pixel-perfect-resolution-calculator)
- [S] 384x216 and 480x270 fill 1080p and 4K exactly but leave bars at 1440p (search summary) — [Ziva calculator](https://ziva.sh/tools/pixel-perfect-resolution-calculator)
- [S] Integer scaling as a general principle for sharp pixels — [tanalin.com, "Integer scaling"](https://tanalin.com/en/articles/integer-scaling/)
- [P] Offline, fixed-frame-rate rendering with exact viewport-size frames is available in Godot (`viewport` stretch mode sets the recorded resolution; FPS is a project setting) — [Godot docs](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html)
- [P] Working resolution used in a credible 3D pixel-art demo: 640x360 mentioned — [David Holland](https://davidholland.netlify.app/articles/3d-pixel-art-rendering)
- [P] Sprite scale reference: food 32x32, hero dish 48x48 — [Slynyrd](https://www.slynyrd.com/blog/2020/9/30/pixelblog-30-food)
- [P] Animation: fewest possible key poses, no in-betweens between keys — [Game Developer, Dead Cells](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- [P] Static camera gives consistent pixel alignment; a moving camera causes grid mismatch and jumping pixels unless snapped — [Blender Studio](https://studio.blender.org/blog/3d-pixel-art-in-blender); [David Holland](https://davidholland.netlify.app/articles/3d-pixel-art-rendering)

### Inferences
Arithmetic for 1080x1920 portrait (researcher's calculation, exact):

| Internal grid | Scale | Texel size on screen | Note |
|---|---|---|---|
| 135x240 | x8 | 8 px | very chunky; 32 px food = 24% of width |
| 180x320 | x6 | 6 px | portrait equivalent of 320x180; classic 16-bit feel |
| 216x384 | x5 | 5 px | |
| 270x480 | x4 | 4 px | portrait equivalent of 480x270; room for 64–96 px hero food |
| 360x640 | x3 | 3 px | portrait equivalent of 640x360 (David Holland's working size); pixels start to read as "HD" on phones |

- All five divide 1080x1920 exactly, so any of them upscales with nearest-neighbour and no blur. Choosing a non-divisor grid (e.g. 200x356) forces fractional scaling and uneven pixel widths, which is the same defect the AI sources describe.
- Base resolution choice follows from the subject: 180x320 suits character-plus-kitchen wide shots; 270x480 suits food close-ups where the dish needs more than 48 px.
- Frame rate (inference, not sourced): encode the video container at a platform-normal 30 fps but update the pixel animation less often (e.g. hold each pose for 2–3 frames, about 10–15 unique poses per second), matching Dead Cells' pose-to-pose approach. Render the low-res frames at the lower rate and duplicate, rather than rendering 30 unique sub-texel frames.
- Text (inference, not sourced): two consistent options exist — (a) a pixel font drawn on the internal grid so text shares the texel size, or (b) crisp high-resolution captions deliberately placed as a separate overlay layer. Mixing texel sizes inside the "pixel" layer (often called "mixels") is what to avoid. Thai script has stacked vowels and tone marks that need more vertical pixels than Latin; at a 6 px texel a legible Thai pixel font would be large on screen, so a high-res overlay for Thai captions is the lower-risk choice. This needs a render test; no source was found.
- Camera (supported by section 3): prefer locked-off shots and hard cuts; if a move is required, move in whole-texel steps.

### Gaps
- No source was found on "mixels" or on pixel font versus high-res overlay for video; the search returned nothing on that term.
- No source was found recommending a specific frame rate for pixel-art video on short-form platforms.
- No source was found on how TikTok/Reels/Shorts re-encoding (chroma subsampling, bitrate) affects hard pixel edges at x4 versus x6 scale. This should be tested with an actual upload.
- No source on Thai pixel-font legibility at these grid sizes.
- Nothing in this section has been render-tested; it is a scaffold from sources plus arithmetic, not a verified recipe.
