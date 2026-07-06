# HyperFrames Components — Reference for Auto-Affi Thai Shopee Ads

**Last reviewed:** 2026-07-06 · **HF version:** v0.7.37 · **Scope:** all **25 components** (`type=component`) in the HeyGen registry, studied from their **real installed source** (~6,500 lines), oriented to 9:16 Thai Shopee affiliate ads.

**Provenance / honesty:** Component list is `[VERIFIED]` via `npx hyperframes catalog --type component --json` (25) and `--type block --json` (109). Each component's mechanism, controls, Thai-safety, and gotchas were extracted by reading the installed HTML in `compositions/components/` — not from the docs pages (the public `/catalog/components/*.md` pages contain **no code**, only an "install it and read the file" pointer). Thai-safety verdicts are source-derived judgments, not render-tested per component; the karaoke pattern itself is render-verified in `runs/2026-07-04-clear-men-couple-v9/hf`.

> **components** = paste-in pieces that layer *onto* your composition (captions, text-effects, overlays). **blocks** = standalone sub-compositions with their own `data-width/height/duration` (transitions, lower-thirds, VFX, maps) — see §8. The URL `hyperframes.heygen.com/catalog/components/` = the 25 here.

---

## 1. The 5 universal rules — do these to ANY caption before shipping Thai

Every caption component was authored for **English landscape demos**. The mechanism is almost always fine; the *packaging* is not. Before any HF caption enters an Auto-Affi ad:

1. **Swap the font — MANDATORY.** Every caption ships a Latin-only display face (Anton, Montserrat 800/900, Poppins, Gabarito, Playfair Display). **None have Thai glyphs → Thai renders as tofu boxes.** Replace `font-family` (and any canvas `fitFontSize` font string) with a Thai face: `'Noto Sans Thai'`/`'IBM Plex Sans Thai'` for body, `'Kanit'`/`'Anuphan'` 900 for display. Verify `line-height` (Anton uses `1` — clips upper tone marks; bump to ~1.25 + small top pad).
2. **Retarget 1920×1080 → 1080×1920.** All are hardcoded landscape in 3–4 places (`data-width/height`, `viewport` meta, `html/body` CSS, and `fitFontSize` `maxWidth` ~1620–1760). Change all, and drop `maxWidth` to ~980 for 9:16.
3. **Feed the pythainlp word array — never their tokenizer.** Every caption consumes a pre-tokenized `WORDS`/`TRANSCRIPT` array of `{text,start,end}`. **Our pipeline already produces this** (pythainlp `newmm` + STT-aligned seconds — see [gold-standard-ad-recipe](gold-standard-ad-recipe.md)). Do **not** rely on their internal `.split(" ")`/`join(" ")` — Thai has no inter-word spaces, so a space-join inserts wrong gaps and space-split fails. Set the flex `gap` to `0` for Thai.
4. **Vendor GSAP + fonts for offline render.** All load `gsap` from `cdn.jsdelivr.net` and fonts from Google Fonts. For a hermetic render, vendor them locally (proven pattern: `hf/vendor/gsap.min.js`, `<script src="vendor/gsap.min.js">` — see the CLEAR ad). CDN refs are also CSP-blocked inside a claude.ai Artifact.
5. **Patch Latin-only helper regexes.** Keyword/emoji/accent logic in several captions cleans words with `.replace(/[^a-z]/g,"")` → **every Thai word becomes empty** → no emoji, no accent color, no keyword highlight. Rewrite `clean` to keep Thai (strip only whitespace/punct) and key your maps on Thai words.

**Key finding on Thai-safety:** *No component breaks Thai by animating the REAL text per-character* — all 25 set each unit via `.textContent` on a whole span/word, so combining marks stay attached. The `thaiSafe: caution` verdicts below are for the **secondary** reasons above (Latin regexes, a Latin-locked scramble gimmick, font). The genuinely weak ones are weak on *fit* (decoration, not conversion), not on glyph safety.

---

## 2. All 25, ranked by Thai-ad fit

| Fit | Component | Cat | Grain | Thai | Where in the ad |
|:--:|---|---|---|:--:|---|
| **4** | `caption-highlight` | caption | word | safe | benefit bullets, CTA — red pill sweep (very Shopee) |
| **4** | `caption-clip-wipe` | caption | word | safe | hook + benefits — gold keyword flash |
| **4** | `caption-kinetic-slam` | caption | word | safe | **hook** — one giant word slams in |
| **4** | `caption-gradient-fill` | caption | word | safe | hook + benefits — rainbow karaoke sweep |
| **4** | `caption-emoji-pop` | caption | word | caution¹ | benefit bullets — 1-3 word chunks + emoji |
| **4** | `caption-blend-difference` | caption | block | safe | auto-legibility over any b-roll |
| **4** | `shimmer-sweep` | text-fx | frame | safe | **price reveal / CTA / brand** glint |
| **4** | `vignette` | overlay | frame | safe | b-roll polish, focus + legibility |
| 3 | `caption-neon-glow` | caption | word | safe | hook/benefits — cyan+pink keyword glow |
| 3 | `caption-parallax-layers` | caption | word | safe | hook — giant red word *behind* subject |
| 3 | `caption-neon-accent` | caption | block | caution¹ | benefit bullets — 4-word phrase pop |
| 3 | `caption-particle-burst` | caption | word | caution¹ | price/keyword — gold word + confetti |
| 3 | `caption-weight-shift` | caption | line | caution¹ | running subtitle track (2-line) |
| 3 | `caption-pill-karaoke` | caption | word | caution¹ | UGC read-along subtitle (our current style) |
| 3 | `caption-editorial-emphasis` | caption | word | caution¹ | hook — one word explodes serif-italic |
| 3 | `caption-glitch-rgb` | caption | word | caution¹ | hook — techy RGB glitch snap |
| 3 | `caption-texture` | caption | word | caution¹ | hook — lava/texture-filled word slam |
| 3 | `morph-text` | text-fx | block | safe | title card — line→line liquid morph (ลดหนัก→ส่งฟรี→กดเลย) |
| 3 | `grain-overlay` | overlay | frame | safe | b-roll polish — film grain |
| 3 | `grid-pixelate-wipe` | transition | block | safe | one scene→scene pixel wipe |
| 3 | `parallax-zoom` / `-unzoom` | transition | block | safe | grid→hero collapse (needs a card grid) |
| 2 | `matrix-decode` | caption | word | caution² | novelty only — scramble is Latin-locked |
| 2 | `motion-blur` | text-fx | block | safe | moving cards/logos only (keep captions sharp) |
| 2 | `texture-mask-text` | text-fx | block | safe | one carved-stone/metal brand word (static) |

¹ caution = Latin-only helper (font/regex) needs patching, mechanism is glyph-safe · ² the decode animation itself is Latin — real text is safe but the gimmick shows Latin gibberish

---

## 3. Tier 1 — USE THESE (fit 4)

### Captions (word-karaoke, the workhorses)

**`caption-highlight`** — red rounded "pill" sweeps behind each word as spoken (`scaleX` wipe, `transform-origin:0% 50%`). The most *Shopee-native* look. Controls: `WORDS[]`, `RAW_GROUPS[]` (line chunking), `.hl-word-bg` gradient (`#ff1745→#df1238` — recolor to brand), `fitFontSize` base 80. → **benefit bullets + CTA.**

**`caption-clip-wipe`** — each word reveals via `clip-path: inset()` left-to-right; `KEYWORDS` set flashes gold `#FFD700`; spoken words dim to 40%. Controls: `WORDS[]`, `KEYWORDS` (indices → gold), `RAW_GROUPS[]`. Gold flash = ready-made emphasis for **product name / price / CTA verb**. → **hook + benefits.**

**`caption-kinetic-slam`** — ONE giant word center-screen, 4 rotating entrances (`wi % 4`: drop / slide-L / slide-R / scale-pop). Scroll-stopper. Controls: `WORDS[]`, `KEYWORDS` (gold), `entranceMode`, `fitFontSize` base 220. Add a scrim (`.kt-overlay` is transparent) so white doesn't wash on bright footage. → **hook** (best) + CTA punch word.

**`caption-gradient-fill`** — rainbow "Siri" gradient sweeps across each word's glyphs (`background-position` on `background-size:350%`, clipped to text). Premium-tech look. Recolor `SIRI_GRAD` to Shopee orange/red for on-brand; the white "unspoken tail" can be low-contrast — add a shadow. → **hook + benefits.**

**`caption-emoji-pop`** — 1-3 word chunks pop as a block with an auto-emoji floating above + accent colors + heavy `-webkit-text-stroke:3px #000`. High-energy TikTok look. **Requires rule 5 patch** (`[^a-z]` regex nukes Thai emoji/accent lookup). → **benefit bullets.**

**`caption-blend-difference`** — pure CSS `mix-blend-mode:difference` on the caption container → text auto-inverts per-pixel against any footage (white-on-dark, black-on-light). Needs `isolation:isolate` on the root. Zero JS, stateless — **pair with a motion caption** for punch. Best as the **legibility guarantee** over unpredictable Veo b-roll; weaker for price/CTA where a locked brand color beats auto-inversion.

### Polish (no text risk, high value)

**`shimmer-sweep`** — diagonal light band slides across any `.shimmer-sweep-target` (animates `--shimmer-pos`, `mix-blend-mode:overlay`). Wrap `฿199`, a `ซื้อเลย` button, or the brand lockup. Bump `--shimmer-color` alpha over dark footage. → **price reveal / CTA / brand stamp.**

**`vignette`** — radial edge-darken (`--vignette-size` 45%, `--vignette-color` `rgba(0,0,0,0.7)`). Focuses the center, lifts perceived production value, improves caption legibility. Use `ellipse` for 9:16; dial alpha to ~0.5 for product-forward shots. Sits `z-index:90` (under grain). → **b-roll polish, whole ad.**

---

## 4. Tier 2 — USE WITH CARE (fit 3)

- **`caption-neon-glow`** — dim phrase, cyan glow sweeps per word, pink `#FF0099` on keywords. Solid karaoke alt; neon may be off-brand for gentle products.
- **`caption-parallax-layers`** — giant red 3D emphasis word sits *behind* the video subject as the VO says it (needs subject matting). Striking hook device.
- **`caption-neon-accent`** — 4-word phrase groups, scale+fade pop + gentle wiggle, accent-color keywords. Needs rule 5 patch.
- **`caption-particle-burst`** — word pop + gold keyword + radial confetti burst. Great for punching price/keyword; patch Latin keyword logic.
- **`caption-weight-shift`** — 2-line chunks; BOLD weight shifts top→bottom line on beat. Good *running subtitle* track for dense VO.
- **`caption-pill-karaoke`** — grey pill, words light up in karaoke, auto-chunked 4-word/2-line. Clean UGC read-along. **This is closest to our current hand-rolled karaoke** — the official block also needs 9:16 retarget; our custom one already works.
- **`caption-editorial-emphasis`** — 2-3 word magazine blocks; periodically one word explodes into giant Playfair italic. Great for a single-word hook (`ของแท้`, `ลดแรง`).
- **`caption-glitch-rgb`** — RGB chromatic-aberration snap per word, resolves to clean white. Techy energy; real text is Thai-safe.
- **`caption-texture`** — words filled with a scrolling image texture (lava default). Mood-specific — bold hooks, not gentle products. Needs a texture PNG.
- **`morph-text`** — full lines dissolve one into the next via gooey liquid-metal morph (SVG threshold). **Thai-safe.** Perfect for a title-card sequence `ลดหนัก → ส่งฟรี → กดเลย`.
- **`grain-overlay`** — animated film grain (`z-index:100`, hides compression banding on flat AI footage). Pure polish.
- **`grid-pixelate-wipe` / `parallax-zoom` / `parallax-unzoom`** — scene transitions. Pixel-wipe = one snappy hard cut. Parallax zoom/unzoom need a real **card grid** (variants/colorways), so niche for a single-product ad.

---

## 5. Tier 3 — AVOID / niche (fit ≤2)

- **`matrix-decode`** — the "decode" scramble frames use Latin gibberish; on Thai the effect degrades to a plain snap. Novelty only.
- **`motion-blur`** — velocity-driven directional blur on *moving elements*. **Never on captions/price** (must stay razor-sharp). Use only on moving product cards/logos during entrances.
- **`texture-mask-text`** — static carved-material fill (66 presets) for ONE hero/brand word. No motion, no sync — decoration, not a caption engine.

---

## 6. Recommended caption kit — ad beat → component

| Beat | Component | Why |
|---|---|---|
| **HOOK** (0–1.5s) | `caption-kinetic-slam` **or** `caption-clip-wipe` | one-word slam / gold-flash keyword = scroll-stopper |
| **BENEFIT bullets** | `caption-highlight` (red pill) | Shopee-native, paces eye through spoken selling points |
| **PRICE reveal** | solid `caption-highlight` word + `shimmer-sweep` glint | high-contrast number + premium shine |
| **CTA** | `caption-highlight` / `caption-clip-wipe` gold verb | tight VO-synced call-to-action |
| **BRAND stamp** | `shimmer-sweep` on lockup | premium cue, zero glyph risk |
| **Legibility net** | `caption-blend-difference` on the caption container | auto-inverts over any b-roll luminance |
| **Whole-clip polish** | `vignette` (+ optional `grain-overlay`) | focus center, lift production value |
| **Scene cut** | `grid-pixelate-wipe` | one energetic hard cut (problem→product) |

**Keep the hand-rolled word-karaoke as the workhorse** — it's render-verified, Thai-correct (pythainlp), offline, and 9:16-native. The blocks above are *upgrades to layer in*, not replacements. All Tier-1/2 captions read the **same** `{text,start,end}` word array we already generate, so switching styles is a font+layout+recolor job, not a data job.

---

## 7. Specific upgrades for the CLEAR ad

One change, highest ROI first:
1. **Add `shimmer-sweep` to the ฿199 price + CTA button** on the endcard — one glint pass when the price lands. Cheap, premium, zero Thai risk.
2. **Add `vignette`** (`ellipse`, alpha ~0.5) over all 5 shots — focuses on Jiab/product, improves caption legibility, lifts the flat Veo look.
3. **Swap the hook caption (shot 1) to `caption-kinetic-slam`** for the opening line — one-word slam is a stronger scroll-stopper than the current running band. Feed the same pythainlp word array; swap font to Kanit 900 Thai; retarget 9:16.
4. **Optional:** `caption-clip-wipe` gold-flash on the brand word "CLEAR" and the price number where they're spoken.

---

## 8. Blocks (109) — quick reference + how to add

Blocks are standalone sub-compositions (own `data-width/height/duration`). Add via `data-composition-src`. Relevant families for Auto-Affi:

- **Shader transitions (14):** `cinematic-zoom` (what we use), `whip-pan`, `swirl-vortex`, `light-leak`, `glitch`, `ripple-waves`, `sdf-iris`, `flash-through-white`… — **use ≤2 per video.**
- **Transition galleries (13):** `transitions-scale/-dissolve/-cover/-push/-radial/-blur/-3d/-light/-grid/-mechanical/…` — reference sets, pick a CSS transition.
- **Lower-thirds (12):** `lt-soft-pill`, `lt-clean-bar`, `lt-dark-card`, `lt-bold-block`, `lt-accent-underline`, `yt-lower-third`… — for a presenter name/handle strip.
- **Social overlays (7):** `tiktok-follow`, `instagram-follow`, `yt-lower-third`, `x-post`, `reddit-post`, `spotify-card`, `macos-notification` — stamp a follow-card as a beat closer.
- **Maps/data-viz (8), code (24+9), liquid-glass (7), VFX (6), showcases (6)** — mostly out-of-scope for product ads.

**Add commands:**
```bash
npx hyperframes catalog --type component --json      # list all 25 components
npx hyperframes catalog --type block --json          # list all 109 blocks
npx hyperframes add <name> --no-clipboard            # install one (component → compositions/components/, block → sub-composition)
npx hyperframes add captions                         # install all caption-tagged at once (15)
```

**Wiring contract (both):** component = paste HTML into the composition; it self-registers a **paused** GSAP timeline at `window.__timelines["<id>"]` which the renderer **seeks per frame** (never `.play()`). Block = `<div data-composition-src="compositions/<block>.html" data-start data-duration data-width data-height>`. See `~/.claude/skills/hyperframes-registry/references/wiring-{components,blocks}.md`.

---

## Related
- [gold-standard-ad-recipe.md](gold-standard-ad-recipe.md) — the locked pipeline (this doc = the caption/compose layer, step 6)
- Memory: `project-hyperframes-compose` — compose format, Thai-karaoke unlock (pythainlp), offline-100% vendoring, headless-Chrome render engine
- Worked example: `runs/2026-07-04-clear-men-couple-v9/hf/` (`master_karaoke.mp4`, `index.html`, `vendor/gsap.min.js`)
