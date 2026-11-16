# 2D pixel-art games where a character visibly cooks or prepares food

Research date: 2026-11-16. Researcher notes for the report writer.

**Evidence tags used on every line**

- `[P]` verified from primary: I opened the page/API myself (Steam store page HTML, Steam `appdetails` JSON, itch.io page, the article itself).
- `[S]` secondary: taken from a search-result summary or a third-party article describing something else; page not opened or fact not on the page I opened.
- `[V]` visual: I looked at the image myself. For Steam titles this means **the first six store screenshots only, as 400x225 thumbnails** (very low resolution). I saw **no video or animation for any game**. Anything about motion, frame counts or cooking animation is therefore never `[V]`.
- `[M]` from memory / unverified: not checked in this session. Treat as a lead, not a fact.

**How the Steam numbers were obtained (applies to every "Steam" line):** Steam `api/appdetails` JSON (developer, publisher, release date, PC platforms, Metacritic score field) and the English store page HTML (`store.steampowered.com/app/<id>/?l=english&cc=us`), both fetched 2026-11-16. Review figures are the line "X% of the N user reviews for this game are positive" **as shown on the English-language store page**. For big titles this is clearly the English-language subset, not the all-language total (e.g. Stardew Valley shows 397,380). Console/mobile platforms are **not** in that data; where given they are `[M]`.

---

## 1. Which games qualify?

### Takeaway
Roughly a dozen released titles are genuinely pixel art with cooking as the core loop or a showcase sequence; the strongest style references are Dave the Diver (sushi bar + cooking cutscenes), Chef RPG, Pixel Cafe, Galaxy Burger, Touhou Mystia's Izakaya, Magical Delicacy and Eastward. Several commonly cited "pixel cooking" games are **not pixel art** on inspection (Lemon Cake, Cuisineer, Venba, Battle Chef Brigade, PlateUp!, Coral Island, Cook Serve Delicious) and no commercially released pixel-art game centred on Thai food was found.

### Cited Findings

**A. Qualify: pixel art + cooking is core or prominent**

- Dave the Diver — Steam tags lead with "Pixel Graphics"; cooking/sushi restaurant is half of the loop. `[P]` — [Steam](https://store.steampowered.com/app/1868140/)
- Chef RPG — Steam tags "Pixel Graphics, Cooking"; Early Access. `[P]` — [Steam](https://store.steampowered.com/app/1796790/)
- Pixel Cafe — tags "Pixel Graphics, Time Management, Cooking". `[P]` — [Steam](https://store.steampowered.com/app/2409360/)
- Galaxy Burger — tags "Cooking, Simulation, Cozy, 2D" (note: **no** "Pixel Graphics" tag in the top 12, but screenshots are clearly pixel art `[V]`); a press roundup calls it "a light pixel art touch" `[S]`. — [Steam](https://store.steampowered.com/app/2749770/); [Bonus Action roundup](https://bonus-action.com/guides/steam-cooking-fest-2026-best-game-deals-recommendations/)
- Touhou Mystia's Izakaya — tags "Pixel Graphics, Time Management, Cooking"; developer's store text says "As a pixel art game, we spent a lot of time on the visual presentation" `[S, quoted from search summary of the Steam page]`. — [Steam](https://store.steampowered.com/app/1584090/)
- Magical Delicacy — tags "Cooking, Platformer, Pixel Graphics". `[P]` — [Steam](https://store.steampowered.com/app/2231190/)
- Eastward — tags "Pixel Graphics"; cooking is a central stat-boost mechanic per the designers `[S]`. — [Steam](https://store.steampowered.com/app/977880/); [Game Developer, Road to the IGF](https://www.gamedeveloper.com/disciplines/road-to-the-igf-pixpil-s-i-eastward-i-)
- Bear's Restaurant — tags "Story Rich, Pixel Graphics"; narrative game set in a restaurant (cooking is story framing more than mechanic). `[P]` — [Steam](https://store.steampowered.com/app/1687550/)
- Kairosoft restaurant sims — Cafeteria Nipponica (tags "Cooking, Pixel Graphics"), The Ramen Sensei ("Pixel Graphics, Cooking"), Cafe Master Story ("Pixel Graphics, Cooking"). `[P]` — [Cafeteria Nipponica](https://store.steampowered.com/app/1952170/); [The Ramen Sensei](https://store.steampowered.com/app/1918540/); [Cafe Master Story](https://store.steampowered.com/app/2427100/)
- Kitchen Crisis — tags "Isometric, Pixel Graphics, Cooking" (tower-defence/automation kitchen). `[P]` — [Steam](https://store.steampowered.com/app/2118250/)
- Dungeon Munchies — tags "Pixel Graphics, Side Scroller" (hunt monsters, cook them for buffs `[M]`). `[P for tags]` — [Steam](https://store.steampowered.com/app/799640/)
- Culinary Wizard — tags "Cooking, Pixel Graphics, Free to Play"; tiny (34 reviews). `[P]` — [Steam](https://store.steampowered.com/app/3477590/)
- Coffee Talk and VA-11 Hall-A — both tagged "Pixel Graphics"; drink-mixing rather than cooking, included as close-up "preparation screen" references. `[P]` — [Coffee Talk](https://store.steampowered.com/app/914800/); [VA-11 Hall-A](https://store.steampowered.com/app/447530/)

**B. Pixel art, cooking is a secondary system (farm/life sims)**

- Stardew Valley, Fields of Mistria, Sun Haven, Roots of Pacha, Travellers Rest (Early Access), Little Witch in the Woods, Spirittea, Core Keeper, Potion Permit — all carry the "Pixel Graphics" tag. `[P]` — [Stardew](https://store.steampowered.com/app/413150/); [Fields of Mistria](https://store.steampowered.com/app/2142790/); [Sun Haven](https://store.steampowered.com/app/1432860/); [Roots of Pacha](https://store.steampowered.com/app/1245560/); [Travellers Rest](https://store.steampowered.com/app/1139980/); [Little Witch in the Woods](https://store.steampowered.com/app/1594940/); [Spirittea](https://store.steampowered.com/app/1931010/); [Core Keeper](https://store.steampowered.com/app/1621690/); [Potion Permit](https://store.steampowered.com/app/1337760/)

**C. Checked and excluded as "not pixel art" (still useful as non-pixel references)**

- Lemon Cake — no "Pixel Graphics" tag `[P]`; screenshots show smooth, rendered/painted 3D-looking bakery, not pixel art `[V]`. — [Steam](https://store.steampowered.com/app/1338330/)
- Cuisineer — no "Pixel Graphics" tag `[P]`; screenshots show painted/cel-shaded 2D art with large illustrated dish splash screens `[V]`; reviewers call it "cel-shaded" / "cutesy anime" `[S]`. (One aggregator lists it as pixel art; that is wrong on the visual evidence.) — [Steam](https://store.steampowered.com/app/1963570/); [Niche Gamer review](https://nichegamer.com/reviews/cuisineer-review)
- Venba — tags "Cooking, Narrative, Stylized"; no pixel tag `[P]`. Stylised flat 2D art by art director Sam Elkana, influences cited as Samurai Jack / Dexter's Laboratory `[S]`. Culturally specific (Tamil / South Indian) cooking-narrative reference. — [Steam](https://store.steampowered.com/app/1491670/); [PlayStation Blog](https://blog.playstation.com/2023/06/12/the-story-of-venbas-culinary-and-cultural-roots-from-creative-director-abhi/)
- Battle Chef Brigade Deluxe — tags include "Hand-drawn"; no pixel tag `[P]`. — [Steam](https://store.steampowered.com/app/452570/)
- PlateUp!, Coral Island, Cook Serve Delicious!, Overcooked! 2, Good Pizza Great Pizza, Mineko's Night Market ("Hand-drawn"), Omelet You Cook, Rolling Hills, Snacko — none has "Pixel Graphics" in the top tags `[P]`. PlateUp!/Coral Island/Overcooked are 3D `[M]`. — [PlateUp!](https://store.steampowered.com/app/1599600/); [Coral Island](https://store.steampowered.com/app/1158160/); [Cook, Serve, Delicious!](https://store.steampowered.com/app/247020/); [Overcooked! 2](https://store.steampowered.com/app/728880/)
- Moonlighter — pixel art ("Pixel Graphics" tag) but tags are shop-keeping/roguelite with no cooking tag `[P]`; it is a shop game, not a cooking game `[M]`. Exclude. — [Steam](https://store.steampowered.com/app/606150/)
- Potion Craft / Potionomics — not checked this session; not cooking. Excluded per brief.

**D. Thai / South-East Asian food**

- No released commercial pixel-art game centred on Thai cooking was found on Steam (Steam store search for "Thai food", "Pad Thai", "Nasi Lemak" returned no app). `[P — negative search result]` — [Steam search API](https://store.steampowered.com/api/storesearch/?cc=us&l=en&term=Pad%20Thai)
- "dish ruchhh" (itch.io, dev "deewa_") — Northern Thai restaurant sim; page tags it Pixel Art; Godot; HTML5; name-your-price; **status "Canceled"**; dishes named: Lom Pla Som, Khao Soi Gai, Ong Poo Na, Aeb Pla Nin, Kai Pam. No description of mechanics or camera on the page. `[P]` — [itch.io](https://dewakuneiei.itch.io/dish-ruchhh)
- The same developer published a devlog titled "Art Assets" for that game (not opened). `[S]` — [itch.io devlog](https://dewakuneiei.itch.io/dish-ruchhh/devlog/818147/art-assets)
- "Thai Street Food Story" (itch.io, dev "Beam", art & programming) — Godot, HTML5, status Released, 1 rating (5.0), "No generative AI was used"; URL slug is `khao-soi`. Page does **not** state the art style or describe cooking. `[P]` — [itch.io](https://beamcsrd.itch.io/khao-soi)
- "Cooking With Spirits" (game-jam entry on Thai ghost folklore, commenters praised pixel-art monsters) and "aroy dee" (RAWG listing) surfaced in search only. `[S, unopened]` — [itch.io thread](https://itch.io/post/8752380/view-in-topic); [RAWG](https://rawg.io/games/aroy-dee)
- Cuisineer (non-pixel) shows South-East/East Asian dishes as full-screen illustrations: I saw "ICE KACANG" and "CHASHU RAMEN" title-banner splash art in its store screenshots. `[V]` — [Steam](https://store.steampowered.com/app/1963570/)
- Dave the Diver's later jungle content ("Bancho Grill"): the team reportedly flew in recipe books from Indonesia and studied "cooking methods using coconut milk, palm sugar, and banana leaves"; the lead designer took a cooking class. `[P for the article, which itself quotes an earlier Inven interview]` — [Inven Global, "The Food of Dave the Diver", 21 Jun 2026](https://www.invenglobal.com/business_industry/articles/22989/the-food-of-dave-the-diver)
- Food Cart Simulator (street-food, "inspired by diverse cultures" `[S]`) is 3D, realistic, unreleased ("To be announced") `[P]` — not a pixel reference. — [Steam](https://store.steampowered.com/app/3647140/)

**E. Unreleased / Early Access flags (as of 2026-11-16)**

- Chef RPG: Early Access since 12 Sep 2024. `[P]` — [Steam](https://store.steampowered.com/app/1796790/)
- Travellers Rest: Early Access since 28 Jul 2020. `[P]` — [Steam](https://store.steampowered.com/app/1139980/)
- Witchbrook (Chucklefish, pixel): listed for 28 Jan 2027, unreleased. `[P]` — [Steam](https://store.steampowered.com/app/1846700/)
- Nainai's Recipe and Soup Pot: "Coming soon"; both 3D/first-person by tags, not pixel. `[P]` — [Nainai's Recipe](https://store.steampowered.com/app/1730460/); [Soup Pot](https://store.steampowered.com/app/1387810/)
- Fields of Mistria: `appdetails` returns release date "Aug 5, 2026" and my Early-Access check did not fire, which suggests a 1.0 release on that date. `[P for the raw field; interpretation is mine]` — [Steam](https://store.steampowered.com/app/2142790/)

### Inferences
- The "pixel cooking game" space splits into three visual formats an animator can borrow from: (1) fixed close-up station screens with large food sprites (Galaxy Burger, Pixel Cafe, Coffee Talk/VA-11 Hall-A); (2) side-on diorama + bespoke cutscenes (Dave the Diver, Mystia's Izakaya); (3) top-down RPG worlds where food is mostly menu icons (Chef RPG, Stardew-likes, Kairosoft).
- A Thai-cooking pixel series would be entering a nearly empty niche; the nearest culturally specific precedents are non-pixel (Venba, Cuisineer) or tiny/cancelled itch.io projects.

### Gaps
- itch.io tag browse ("pixel-art" + "cooking") was not systematically crawled; only search-surfaced titles are listed. More small Thai/SEA jam games probably exist.
- Mobile-only pixel titles (e.g. Hungry Hearts Diner, other Kairosoft mobile releases) were not verified; "Hungry Hearts" returned nothing on Steam. `[M]` that Hungry Hearts Diner (GAGEX, mobile) is pixel art.
- BurgerTime (Data East, 1982 arcade) is the canonical retro pixel food game — `[M]`, not checked; see [Wikipedia](https://en.wikipedia.org/wiki/BurgerTime) (unopened). Cooking Mama is not pixel art `[M]`.
- DEADLINE DINNER (Steam 4922230, released 31 Oct 2026, 9 reviews) surfaced as "cozy pixel-art restaurant sim" in a search summary `[S]`, but its Steam tags do not include Pixel Graphics `[P]`; art style unverified. — [Steam](https://store.steampowered.com/app/4922230/)

---

## 2. Per-game facts (developer, release, how cooking is shown, view, food art, reception)

### Takeaway
Release/credit/review data below is primary (Steam, 2026-11-16); visual notes are from six low-res store thumbnails per game; **no developer source gave sprite resolution or cooking-animation frame counts for any cooking game** — those fields are gaps across the board.

### Cited Findings

Format: **Game** — dev / pub / Steam release / PC platforms `[P]`; reception `[P]`; then cooking presentation and visuals with their own tags.

- **Dave the Diver** — MINTROCKET / MINTROCKET / 28 Jun 2023 / Windows, Mac. 96% positive of 51,635 (English view); Metacritic field 90. `[P]` — [Steam](https://store.steampowered.com/app/1868140/)
  - Engine: Unity (Unity published a case study; art director named as Kiyeop Chung). `[S]` — [Unity case study](https://unity.com/resources/dave-diver)
  - Mixed 2D/3D: team started with flat 2D pixel underwater scenes, found them unappealing, added 3D background objects ("It felt much deeper and looked unique"), later 3D sea creatures ("making 2D Dave fight 3D sharks" was the hardest task). `[P]` — [Game Developer, Joel Couture, 24 Aug 2023](https://gamedeveloper.com/design/dave-the-diver)
  - Seen in screenshots: underwater scenes are chunky 3D/voxel-like terrain with a small pixel diver; the sushi bar is a **side-on cross-section** with customers seated along a counter, hanging lanterns, warm reds against dark background, HUD on top. `[V]`
  - Cooking presentation: pixel-art cutscenes play when a dish is made/upgraded/researched; reviewers describe chef Bancho sharpening his knife under a cherry-blossom tree and slicing a falling petal, seasoning "salt bae-style". `[S]` — [GamesRadar](https://gamesradar.com/dave-the-diver-players-cant-get-over-how-extra-its-cutscenes-are) (page body failed to load for me; details come from search summary); [RPGFan review](https://rpgfan.com/review/dave-the-diver)
  - Dish design rule: keep each fish's iconic feature in the sushi rather than generic red/white slices (angler-fish sushi keeps the lantern). `[P]` — [Game Developer](https://gamedeveloper.com/design/dave-the-diver)
  - Consoles (Switch, PS4/PS5 `[M]`; Xbox release reported Nov 2025 `[S]`). — [Xbox Wire](https://news.xbox.com/en-us/2025/11/20/dave-the-diver-xbox-partner-preview/)

- **Chef RPG** — World 2 Studio / World 2 Studio / Early Access 12 Sep 2024 / Windows, Mac. 89% of 2,061. `[P]` — [Steam](https://store.steampowered.com/app/1796790/)
  - Vancouver-based team; project lead Noah ("Pixel Architect") has posted dev videos on YouTube since 2020; art described as Studio Ghibli-inspired; launched via Kickstarter by an architectural designer. `[S]` — [Game Developer press release](https://gamedeveloper.com/press-release/chef-rpg-an-open-world-pixel-art-game-project-started-by-an-architectural-designer-is-live-on-kickstarter); [Gematsu](https://www.gematsu.com/2021/11/pixel-art-chef-rpg-announced-for-switch-pc)
  - Seen in screenshots: top-down 3/4 view of town and restaurant floor; detailed painterly pixel environments (snow, timber buildings); large pixel character portraits in dialogue; a recipe/cooking UI with **one larger plated-dish illustration** above a grid of **small ingredient icons**. `[V]`
  - Switch version announced 2021 `[S]`; current console status not checked. — [Gematsu](https://www.gematsu.com/games/chef-rpg)

- **Pixel Cafe** — Baltoro Games / Baltoro Games / 30 Nov 2023 / Windows. 91% of 858. `[P]` — [Steam](https://store.steampowered.com/app/2409360/)
  - Critic scores ranged 5/10–8/10 on OpenCritic; praised for "great retro pixel aesthetic" and lo-fi soundtrack; compared to Cook, Serve, Delicious; weak script noted. `[S]` — [OpenCritic](https://opencritic.com/game/15916/pixel-cafe); [GameGrin](https://www.gamegrin.com/reviews/pixel-cafe-review)
  - Seen in screenshots: **fixed front-on counter screen** — customers stand behind the counter with order panels above their heads; food and drink items (cups, pastries, meat patties, jars) are laid out as medium-sized sprites on the counter in the foreground; city skyline backdrop in muted pink/teal dusk palette; story scenes use large-pixel half-body portraits. `[V]`
  - Consoles (Switch/PS/Xbox) per review titles. `[S]` — [Gaming.net review](https://www.gaming.net/reviews/pixel-cafe-review-ps5-ps4-nintendo-switch-xbox-one-xbox-series-x-s-pc)

- **Galaxy Burger** — Galactic Workshop / Galactic Workshop / 23 Aug 2024 / Windows, Mac. 96% of 1,379. `[P]` — [Steam](https://store.steampowered.com/app/2749770/)
  - Seen in screenshots: **close-up top-down griddle/assembly station** filling the screen; ingredient bins along the top; **large, clean-outlined food sprites** (patties, bacon, fried egg, onion rings, buns) that are the main subject, not icons; separate fryer-station screen with baskets; customers shown front-on at the counter one at a time; recipe book spread with a stacked-burger illustration and ingredient list; flat warm yellow/orange palette, minimal lighting. `[V]`
  - Recipe assembly, stations switched via tabs ("Stove / Customers / Fryer / Drinks" visible in screenshot UI). `[V]`

- **Touhou Mystia's Izakaya** — 二色幽紫蝶 (Dichromatic Purpilion), Re零同人社 / same (Phoenixx also listed by aggregators `[S]`) / 1 Oct 2021 / Windows, Mac. 98% of 3,627 (English view); an aggregator snapshot gives ~29,694 all-language, Overwhelmingly Positive `[S]`. `[P]` — [Steam](https://store.steampowered.com/app/1584090/); [wasdland snapshot](https://www.wasdland.com/game/touhou-mystias-izakaya-1584090)
  - Gather ingredients by day, run the izakaya by night; cooking includes "micro rhythm games" for bonuses. `[S]` — [Steam](https://store.steampowered.com/app/1584090/)
  - Seen in screenshots: side-on izakaya stall under a sunset sky with paper lanterns; **high-detail, high-colour-count "illustration-grade" pixel art** for key scenes (a street stall with the cook at the counter, sparrows, lanterns); chibi character sprites; a loading card showing a chibi cook at a grill with the caption "Girl's Cooking...". `[V]`

- **Magical Delicacy** — Skaule (Steven Kaule, solo, Hamburg `[S]`) / Whitethorn Games / 16 Jul 2024 / Windows. 77% of 245; Metacritic field 82. `[P]` — [Steam](https://store.steampowered.com/app/2231190/); [Gamecity Hamburg](https://gamecity-hamburg.de/news/3-questions-to-skaule-on-the-release-of-magical-delicacy/)
  - Seen in screenshots: **side-on platformer** with detailed pixel buildings, silhouetted foreground foliage, night scenes with small warm light sources; cooking handled through list-style UI panels (ingredient list, recipe with small icons) over a kitchen interior. `[V]`

- **Eastward** — Pixpil / Chucklefish, XD / 16 Sep 2021 / Windows, Mac. 85% of 3,667; Metacritic field 82. `[P]` — [Steam](https://store.steampowered.com/app/977880/)
  - Custom engine; base assets drawn in Aseprite; see section 4. `[P]` — [Game Developer, 11 Oct 2021](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
  - Cooking was added "to give players more atmosphere of living in that world" and gives stat boosts. `[S]` — [EarlyGame interview](https://earlygame.com/gaming/eastwards-interview-producer-tommy-zhou)
  - Seen in screenshots: top-down 3/4 view, extremely dense hand-drawn pixel environments, dynamic warm/cool lighting with glow and light pools. No cooking screen among the six thumbnails I viewed. `[V]`

- **Bear's Restaurant** — Odencat / Odencat / 6 Oct 2021 / Windows, Mac, Linux. 94% of 655. `[P]` — [Steam](https://store.steampowered.com/app/1687550/)
  - Seen in screenshots: low-resolution RPG-Maker-like top-down pixel art, small sprites, a bear chef behind a counter; one side-on shot of a night-time street food stall lit by a street-lamp cone with a red lantern. `[V]`

- **Cafeteria Nipponica** — Kairosoft / Kairosoft / Steam 3 Jul 2022 / Windows. 86% of 182. `[P]` — [Steam](https://store.steampowered.com/app/1952170/)
  - Switch 18 Apr 2019, PS4 1 Oct 2020. `[S]` — [Deku Deals](https://www.dekudeals.com/items/cafeteria-nipponica?platform=all)
  - Seen in screenshots: **isometric** restaurant floor, tiny chibi staff/customers with speech bubbles ("Yum!"); dishes appear only as **small menu icons** in lists ("Crab Fried Rice", "Curry n' Rice", "Hayashi Rice", "Udon") and in a "Develop Dish" dialog combining ingredients. `[V]`
- **The Ramen Sensei** — Kairosoft / 4 Sep 2022 (Steam) / Windows. 69% of 193. Build a bowl by choosing noodle, soup, toppings. `[P]`/`[S]` — [Steam](https://store.steampowered.com/app/1918540/)
- **Cafe Master Story** — Kairosoft / 15 Oct 2023 / Windows. 96% of 393. `[P]` — [Steam](https://store.steampowered.com/app/2427100/)

- **Kitchen Crisis** — Team Samoyed / 2 Apr 2024 / Windows, Mac, Linux. 74% of 310. Isometric kitchen on a floating platform, UI-heavy recipe tables with small dish icons. `[P]`, `[V]` — [Steam](https://store.steampowered.com/app/2118250/)
- **Dungeon Munchies** — maJAJa / 27 Jul 2022 / Windows, Mac. 94% of 917. `[P]` — [Steam](https://store.steampowered.com/app/799640/)
- **Coffee Talk** — Toge Productions / 29 Jan 2020 / Windows, Mac. 94% of 4,768; Metacritic field 76. `[P]` — [Steam](https://store.steampowered.com/app/914800/)
- **VA-11 Hall-A** — Sukeban Games / Ysbryd, PLAYISM / 21 Jun 2016 / Windows, Linux. 96% of 12,111; Metacritic field 77. `[P]` — [Steam](https://store.steampowered.com/app/447530/)

Secondary-cooking farm/life sims (data only; cooking presentation not verified this session):

- **Stardew Valley** — ConcernedApe / 26 Feb 2016 / Windows, Mac, Linux. 98% of 397,380 (English view); Metacritic field 89. `[P]` — [Steam](https://store.steampowered.com/app/413150/). Community modders state inventory/item sprites are generally 16x16, NPC overworld sprites 16x32, portraits 64x64. `[S]` — [Stardew forums](https://forums.stardewvalley.net/threads/sprite-sizes-character-sheets-pixel-art.5597/latest)
- **Fields of Mistria** — NPC Studio / date field 5 Aug 2026 / Windows, Linux. 97% of 26,395. Seen: saturated pastel top-down pixel art, large anime portraits. `[P]`, `[V]` — [Steam](https://store.steampowered.com/app/2142790/)
- **Sun Haven** — Pixel Sprout Studios / 10 Mar 2023 / Windows, Mac. 83% of 13,424. `[P]` — [Steam](https://store.steampowered.com/app/1432860/)
- **Roots of Pacha** — Soda Den / 25 Apr 2023 / Windows, Mac, Linux. 94% of 2,525. `[P]` — [Steam](https://store.steampowered.com/app/1245560/)
- **Travellers Rest** — Isolated Games / Isolated Games, IndieArk / Early Access 28 Jul 2020 / Windows. 88% of 8,478. `[P]` — [Steam](https://store.steampowered.com/app/1139980/)
- **Little Witch in the Woods** — SUNNY SIDE UP / date field 14 Sep 2025 / Windows, Mac. 90% of 4,859. `[P]` — [Steam](https://store.steampowered.com/app/1594940/)

Non-pixel references (data only):

- **Cuisineer** — BattleBrew Productions / Marvelous Europe, XSEED / 9 Nov 2023 / Windows. 76% of 1,832; Metacritic field 79. `[P]` — [Steam](https://store.steampowered.com/app/1963570/)
- **Venba** — Visai Games / 31 Jul 2023 / Windows, Mac. 95% of 1,922. Built in Unity `[S]`. — [Steam](https://store.steampowered.com/app/1491670/)
- **Battle Chef Brigade Deluxe** — Trinket Studios / 20 Nov 2017 / Windows, Mac. 94% of 1,638; Metacritic field 80. `[P]` — [Steam](https://store.steampowered.com/app/452570/)
- **Lemon Cake** — Cozy Bee Games / 18 Feb 2021 / Windows. 86% of 1,697. `[P]` — [Steam](https://store.steampowered.com/app/1338330/)
- **PlateUp!** — It's happening / Yogscast Games / 4 Aug 2022. 96% of 12,712. `[P]` — [Steam](https://store.steampowered.com/app/1599600/)
- **Cook, Serve, Delicious!** — Vertigo Gaming / 8 Oct 2013. 95% of 2,963. `[P]` — [Steam](https://store.steampowered.com/app/247020/)

### Inferences
- Food is drawn at three scales across the catalogue: icon-sized (roughly inventory-tile scale) in Kairosoft, Stardew-likes and Chef RPG's ingredient grids; medium "prop" sprites on a counter in Pixel Cafe; and large hero sprites that fill the play area in Galaxy Burger. Only the last two formats put the food itself on camera in a way that maps to a recipe video.
- The games that put food large on screen all switch away from the world camera to a dedicated flat screen (top-down griddle, front-on counter, recipe book spread). None of the six-thumbnail sets showed a large pixel dish inside a top-down world view.
- Lighting splits into flat/unlit warm palettes for station screens (Galaxy Burger, Kairosoft) versus dynamic glow lighting for world views (Eastward, Dave the Diver bar, Magical Delicacy night scenes).

### Gaps
- **Sprite resolution / pixel density**: no developer-documented figure found for any of the cooking-focused games. Only community-sourced 16x16 figures for Stardew Valley.
- **Dedicated cooking animations and frame counts** (chopping, stirring, wok toss): not documented by any developer source I found, and I viewed no footage, so I cannot confirm their existence per game. From memory only `[M]`: Dave the Diver has many bespoke Bancho cutscenes; Eastward shows John cooking in a short animated sequence tied to a slot-machine minigame; Stardew Valley cooking is menu-only with no cooking animation; Travellers Rest / Fields of Mistria show the character working at kitchen stations. All need footage review.
- Console/mobile platform lists and engines are mostly `[M]` or `[S]`: Stardew Valley (custom C#/XNA→MonoGame `[M]`), Eastward on Switch `[P via Game Developer]`, Pixel Cafe consoles `[S]`.
- Steam review totals in all languages were not retrievable (the `appreviews` JSON endpoint redirected); figures are the English store-page view.
- Travellers Rest, Dungeon Munchies and Little Witch in the Woods: only one thumbnail each loaded into my contact sheet, so no useful visual notes.

---

## 3. Which are most praised for food art or cooking animation, and why?

### Takeaway
Dave the Diver is the clear standout for cooking *animation* (its over-the-top pixel cutscenes of chef Bancho are singled out by reviewers and players); for food *illustration* the most-praised title is Cuisineer, which is not pixel art. Praise clusters around three things: comedic exaggeration, variety (not repeating the same clip), and food designs that keep an ingredient's recognisable feature.

### Cited Findings
- Dave the Diver: reviewers call the pixel cutscenes "a true highlight" and "brilliantly animated and bursting with charm"; cutscenes fire on making/upgrading a meal and "you're not seeing the same animation over and over". `[S]` — [RPGamer review](https://www.rpgamer.com/review/dave-the-diver-review/); [Push Square review](https://pushsquare.com/reviews/ps5/dave-the-diver)
- GamesRadar ran a piece specifically on players being unable to "get over how extra its cutscenes are"; a syndicated summary describes the chef sharpening his knife and then slicing a single falling petal. `[S — headline verified [P], body not loaded]` — [GamesRadar](https://gamesradar.com/dave-the-diver-players-cant-get-over-how-extra-its-cutscenes-are)
- A year-end editors' roundup said the cutscenes are so good one editor "would pay for a cutscene DLC pack". `[S]` — [Yahoo/“Best Design 2023: Dave the Diver”](https://malaysia.news.yahoo.com/best-design-2023-dave-diver-140047676.html)
- Director Jaeho Hwang on why the sushi works: instead of the realistic red or white slice, keep the fish's signature part (angler-fish lantern) — he credits this as a reason players enjoy the sushi. `[P]` — [Game Developer](https://gamedeveloper.com/design/dave-the-diver)
- Hwang on the loop: taking caught fish "straight into sushi"; inspiration was a Jeju Island restaurant whose owner dives in the morning and cooks the catch at night. `[P]` — [Inven Global](https://www.invenglobal.com/business_industry/articles/22989/the-food-of-dave-the-diver)
- Cuisineer (non-pixel): reviews say you get "an amazing splash image of every new recipe you learn" with fine ingredient detail, and that the food illustrations are "extremely tantalizing". `[S]`; I confirmed the full-screen dish splash format (ribbon title + large bowl illustration with radial glow) in store screenshots `[V]`. — [Niche Gamer review](https://nichegamer.com/reviews/cuisineer-review); [Steam](https://store.steampowered.com/app/1963570/)
- Pixel Cafe: praise is for the overall retro pixel look and lo-fi music, not specifically for food animation. `[S]` — [GameGrin](https://www.gamegrin.com/reviews/pixel-cafe-review)
- Magical Delicacy: publisher and reviewers praise detailed pixel art "bringing colorful characters, environments, and food to life", with parallax depth. `[S]` — [Whitethorn Games](https://whitethorngames.com/magicaldelicacy)
- Venba (non-pixel): team recreated the dishes in real life to work out the aesthetics and how to stylise ingredient animation; creative director Abhi says the process is to make cooking "abstracted, simplified, and stylised" and to keep only the most enjoyable steps (for biryani: cooking and mixing; grinding spices and marinating were moved out of interactive play). `[S]` for the real-cooking reference, `[P]` for the Abhi quotes. — [Thumbsticks, 9 Apr 2024](https://www.thumbsticks.com/the-making-of-venba-recipe-for-success/); [Shacknews interview](https://shacknews.com/article/135211/venba-video-interview?amphtml=1)

### Inferences
- What reviewers reward is *staging*, not simulation: a short, punchy, character-led "reveal" clip per dish (Dave the Diver) or a hero illustration per dish (Cuisineer). Both are directly transferable to a short-form recipe video: a per-dish signature flourish plus a final hero plate.
- Venba's rule of cutting tedious steps and keeping the tactile ones is the clearest stated editorial principle for adapting a real cuisine and applies regardless of art style.
- "Keep the recognisable feature of the ingredient" (Hwang) is a readable-at-small-size principle that suits Thai ingredients with strong silhouettes (bird's-eye chillies, kaffir lime leaves, holy basil), though that application is my inference, not sourced.

### Gaps
- No review I opened analyses frame-by-frame cooking animation in any pixel game; the praise is qualitative.
- No evidence found of awards specifically for food art in a pixel-art game.
- Reception of cooking visuals in Chef RPG, Galaxy Burger and Mystia's Izakaya specifically (as opposed to overall Steam rating) was not found.

---

## 4. Developer write-ups, talks and interviews on how the pixel food/cooking art was made

### Takeaway
I found **no** developer source that documents the production of pixel food sprites or cooking animations in a commercial game (tools, frame counts, palette limits). The usable primary material is adjacent: Eastward's Aseprite-to-lit-3D pipeline, Dave the Diver's 2D/3D reasoning and dish-design rule, Magical Delicacy's pixel-first iteration, Venba's (non-pixel) reference-cooking approach, and one very practical non-game tutorial (Slynyrd's Pixelblog 30 on food).

### Cited Findings
- Eastward pipeline: base assets drawn in Aseprite by lead artist Hong Moran; each asset split into layers by natural structure (roof vs wall); layers rebuilt in a 3D environment and hand-painted into bump maps one by one so lighting works; custom in-house engine; lighting/shader system handles weather, time of day, fog layers and sun beams; "we handcrafted every single detail". Interviewee: Tommo Zhou, lead programmer/co-founder. `[P]` — [Game Developer, Bryant Francis, 11 Oct 2021](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
- Eastward scale: around 70,000 hand-drawn animation frames at the time of an earlier article (lead designer Feng Ye) — whole game, not cooking. `[S]` — [Game Developer, Road to the IGF](https://www.gamedeveloper.com/disciplines/road-to-the-igf-pixpil-s-i-eastward-i-)
- Dave the Diver: 2D pixel underwater looked flat, so 3D backgrounds and later 3D creatures were added; art director and lead designer got diving certifications for reference. `[P]`/`[S]` — [Game Developer](https://gamedeveloper.com/design/dave-the-diver); [Xbox Wire](https://news.xbox.com/en-us/2025/11/20/dave-the-diver-xbox-partner-preview/)
- Dave the Diver: Unity case study quotes art director Kiyeop Chung on artists using Shader Graph. `[S]` — [Unity](https://unity.com/resources/dave-diver)
- Dave the Diver food research for the jungle/"Bancho Grill" content: Indonesian recipe books, coconut milk/palm sugar/banana-leaf methods, a cooking class. No art-pipeline detail. `[P]` — [Inven Global](https://www.invenglobal.com/business_industry/articles/22989/the-food-of-dave-the-diver)
- Magical Delicacy (solo dev Steven Kaule): "I usually start directly with pixel art and iterate a lot on designs"; spent "multiple months just doing pixel art" to find the style before anything playable; established "an initial color palette" early; works only digitally with very few sketches; cooking "came naturally from the cozy witch setting… Starting with potions, I expanded that to all kinds of food." Nothing on food sprites, animation, engine or resolution. `[P]` — [Gamer Social Club interview, 18 Jun 2024](https://gamersocialclub.ca/2024/06/18/magical-delicacy-developer-interview)
- Chef RPG: project lead posts development videos on the "Pixel Architect" YouTube channel (since 2020); BackerKit updates link to devlogs (critic and party systems). No cooking-animation devlog was identified. `[S]` — [BackerKit updates](https://chef-rpg.backerkit.com/hosted_preorders/project_updates?page=2); [80.lv](https://80.lv/articles/this-cute-pixel-art-game-about-restaurant-management-boasts-some-updates)
- Venba GDC 2024 talks exist: "Good Enough Is Better Than Good: A Postmortem of Venba" (Abhi Swami) and "Venba: An Intimate Journey Through Sound". Neither is a food-art talk; not viewed. `[S]` — [GDC Vault postmortem](https://gdcvault.com/play/1034474/Independent-Games-Summit-Good-Enough); [GDC Vault sound talk](https://gdcvault.com/play/1034461/Independent-Games-Summit-Venba-An)
- Cuisineer: BattleBrew describe their look as "Yaba-kawa" (yabai-kawaii), from asking "what if we made [Diablo], but super cute?"; a Japanese Automaton email interview reportedly covers recipe inspiration (not opened). `[S]` — [VideoGamesGood BitSummit Q&A](https://www.videogamesgood.com/post/bitsummit-10-developer-q-a-cuisineer-dishes-up-dungeon-crawling-and-restaurant-sim-action); [Automaton JP](https://automaton-media.com/articles/interviewsjp/20231109-271400/)
- Practical pixel-food craft (non-game tutorial, Raymond Schlitter / Slynyrd, Pixelblog 30 "Food", 30 Sep 2020): food sprites "roughly within 32x32px"; a ramen tutorial sprite "roughly 48x48px"; "I used photo references and sampled colors directly from the photos"; "I maintained limited colors and tried to reuse many of the same colors across all items"; outlines keep sprites "relatively cartoony and pop off the screen"; too many colours and no outlines would look like "down scaled photos". No frame counts given for the animated ramen/restaurant GIFs. `[P]` — [Slynyrd Pixelblog 30](https://slynyrd.com/blog/2020/9/30/pixelblog-30-food)

### Inferences
- Because no studio has published its cooking-animation pipeline, the animator should treat the games as *visual* references (study footage) and take *process* guidance from the Slynyrd tutorial: 32–48 px food sprites, photo-sampled colours, a shared limited palette across all dishes, and outlines.
- Eastward's method (flat Aseprite pixel art + hand-painted normal/bump data + engine lighting) explains why its look is hard to reproduce in a pure frame-by-frame video workflow; Galaxy Burger / Pixel Cafe style flat-lit station screens are far cheaper to emulate.
- The absence of documentation is itself a finding: claims online about specific frame counts or palette sizes for these games' cooking animations should be treated as unsourced.

### Gaps
- No GDC Vault talk on pixel food art or cooking animation was found; GDC Vault itself was not searched directly (only via web search).
- Mintrocket's cutscene animator(s), tools and frame counts: not found in any source.
- The Chef RPG "Pixel Architect" YouTube devlogs and the dish ruchhh "Art Assets" itch devlog were not opened; they are the most likely places for actual pixel-food process detail.
- An unsourced blog "Eastward Visual Design Analysis" surfaced in search; flagged as speculative and not used. — [halabaojia](https://halabaojia.pages.dev/collection/20251231-eastward-pixel-art-visual-masterpiece)
- Whether any of these studios used Aseprite for food specifically is undocumented except Eastward's general statement.

---

## 5. Relevant pixel-art cooking content outside games

### Takeaway
There is no single famous "pixel recipe animation" creator I could verify; the most useful non-game references are Slynyrd's food tutorial and commercial animated food sprite packs, which show standard conventions (32–64 px dishes, GIF + sprite-sheet delivery, steam loops).

### Cited Findings
- Slynyrd (Raymond Schlitter) Pixelblog 30 — food sprite set, animated ramen and a restaurant scene, with the technique notes quoted in section 4. `[P]` — [Slynyrd](https://slynyrd.com/blog/2020/9/30/pixelblog-30-food)
- CaioMarcelPixel "Animated Food Pack 64x64" — 100+ animated dishes, delivered as .aseprite, GIF and PNG sprite sheets. `[S]` — [itch.io](https://caiomarcelpixel.itch.io/animated-food-pack-64x64)
- Dangoya "Pixel food pack" — animated frames of food being progressively eaten. `[S]` — [itch.io](https://dangoya.itch.io/pixel-food-pack-animated-frames-of-eaten-food)
- "timmyskitchen" — a pixel-art cooking animation in which ingredients are mixed with transitions and sound, then the dish is served and eaten (pizza key visual). `[S]` — [post mirror](https://art.cleberg.net/post/timmyskitchen/Pizza-keyvisual-for-my-cooking-animation-940257039)
- PixelJoint piece by "mixiekins": animated pixel food based on real menu items for event GIF adverts. `[S]` — [PixelJoint](https://pixeljoint.com/pixelart/113333.htm)
- Pixxiland "2D pixel art cook character animations" asset pack (cook character animation set). `[S]` — [itch.io](https://pixxilandartstudio.itch.io/2d-pixel-art-cook-character-animations)
- Non-pixel adjacent: Kitchen Ghosts (Daria Khoroshavina) food cinemagraphs. `[S]` — [Moss and Fog](https://mossandfog.com/delicious-moments-brought-to-life-with-cinemagraphs/)

### Inferences
- Asset-pack conventions (64x64 animated dishes, "being eaten" frame sequences, cook character animation sets) indicate the practical working sizes hobbyist and indie artists use for food; these are larger than in-game inventory icons and close to what reads on a phone screen after integer upscaling.

### Gaps
- Could not verify well-known social-media pixel food animators (Instagram/TikTok/Bluesky were not searched; search engine results were dominated by asset stores and AI-image sites).
- None of the listed packs/pages were opened except Slynyrd, so frame counts and exact contents are unverified.
- No pixel-art Thai recipe animation outside games was found.
