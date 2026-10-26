# Study: KEMLIFE "Prompt จัดโครงสร้าง Prompt วิดีโอ AI" (Notion, read 2026-10-27)

Source: https://app.notion.com/p/cryptodog/Prompt-Prompt-AI-3e90157f27d78178a837d21c5f9184e4
Owner: เข้ม KEMLIFE — course "AI Video Mastery" (aivideomastery.store). The page is a free lead-magnet for the course.
Status: READ in full (34 text blocks + 2 images). Nothing generated or tested by us. Claims about model behaviour below are THEIR claims, unverified.

## What the page contains

A complete 2-minute K-drama "story ad" (family money fight → daughter breaks piggy bank → mother finds a book → family recovers → CTA for the book), built in two stages:

| Stage | Model / settings (as written on the page) | Output |
|---|---|---|
| 1. Character sheets | Nano Banana Pro · text2image · 16:9 · 2K | 3 sheets: father (32, delivery rider, 2 outfits), mother (30), daughter (6, with props) |
| 2. Video | Seedance 2.5 · element2video · 9:16 · 480p · 30 s · audio ON | 4 clips A–D × 30 s = 2:00, stitched |

Refs are attached in a FIXED order to every clip: @image1 father, @image2 mother, @image3 daughter, @image4 product (book cover).

Images on the page: course banner ("AI Video Mastery ทักษะทำเงินปี 2026") and a Facebook Page Insights screenshot showing $777.36 approximate earnings / 393,907 interactions for Jun 4–Jul 1 (social proof — not verifiable, earnings are down 6% on the screenshot itself).

## Character-sheet recipe (stage 1)

Every sheet uses the same frame:
- "Professional character reference sheet", photorealistic, clean light-grey studio background, soft even light.
- Identity line: name, nationality, age, role, build, hair, face mood, one skin/texture detail.
- Wardrobe spelled out garment by garment, with colours and construction details (collar, zipper, panels, cuffs, pockets). Brand safety: "NO logos, NO text, NO brand marks".
- Layout: full-body front / side / back on the left, a row of **4 labeled close-up expressions** on the right. The 4 expressions are the emotional beats the script needs (e.g. tired → angry → crying → proud smile). So the sheet doubles as an emotion reference.
- Second outfit (for the ending) as an extra full-body view on the same sheet.
- Props the character holds in the story are on the sheet (piggy bank, crayon drawing).
- Small name label at the top.

Compare to our standard (`project_character_sheet_pro_standard`): we say ref pack = single images with NO text, review board separate. They put labels + 4 expressions on one board and use it directly as the video ref. Their approach is cheaper (1 image per character); ours avoids text leaking into the video. Untested which wins in Seedance 2.5.

## Video prompt skeleton (stage 2) — same 7 blocks in every clip

1. **FORMAT** — duration / cut count (7–8 cuts per 30 s) / genre + emotional arc of THIS clip ("tense to heartbreaking", "climax to reconciliation") / dialogue language / "NO MUSIC".
2. **STYLE** — copied word-for-word into all 4 clips: camera body, lens series, focal length, aperture, saturation, dominant tone, grain, handheld with "camera movement intensity follows emotional intensity", aspect, "NO TEXT ON SCREEN".
3. **SUBJECTS** — each subject re-described in one compact line + its @image tag, in every clip, even though the ref is attached.
4. **ENVIRONMENT** — location(s) + time of day + light sources + weather; can contain 2–3 locations per clip.
5. **PRODUCT** (only in the clip that sells) — product @tag + short description + "Keep cover design exact."
6. **AUDIO** — list of diegetic sounds per location; no music track.
7. **TIMELINE** — 3–5 s timecoded beats; each = shot size + camera + action; dialogue as `X says (emotion, delivery note): "line"`.

## Techniques worth stealing

- **Locked STYLE block across clips** = series consistency. A 2-minute film is built from 30 s clips that look like one film because the STYLE text never changes.
- **Negative reference disambiguation**: when a new extra (another child) appears, the prompt says only one ref is in this clip and the extra is "a different child, NOT @image3". Prevents the model from pasting the daughter's face onto the extra.
- **Timestamped wardrobe switch** inside one clip ("from 0:22 onward wearing outfit B from his sheet") — relies on outfit B being on the same sheet.
- **Plant → payoff for the product**: the book is hidden under the bills in clip A (edge visible), and only revealed in clip D. Product placement that feels like story, not an ad.
- **Emotion arc per clip in FORMAT** tells the model the pacing; camera shake scales with emotion.
- **Dialogue in Korean** — sidesteps the Thai lip-sync weakness (our constraint: no Thai lip-sync). Thai would go into subtitles/VO in post.
- **NO MUSIC + NO TEXT** in generation; music, subs, CTA text added in the edit.
- **Low res (480p) for 30 s clips** — likely a credit-cost choice. Our `model-limits.md` lists Seedance 2.5 = 30 s, 720p in examples; 480p not confirmed by us.

## Gaps vs our `higgsfield-seedance-prompt` skill

Already covered: timed segments, shot/cut counts, AUDIO block with "No music", @tag vs attached Elements.
Not covered (candidate additions):
1. Multi-clip series mode — lint that the STYLE block is byte-identical across clips of one film.
2. Negative-ref rule — when a new person appears, require "NOT @imageN" for look-alike refs.
3. Mid-clip wardrobe switch with a timestamp, tied to an outfit on the sheet.
4. Emotion-parenthetical dialogue format.
5. PRODUCT block with "keep design exact".

## Marketing read (for สายตำ)

The format is a **story ad**: 1:30 of drama, product appears as the solution, CTA in the last 4 s spoken by the lead holding the product. For a Shopee affiliate this maps to: problem-drama with JIAB → product plant early → reveal as the fix → JIAB holds product + CTA. Length (2:00) is long for TikTok shop ads; a 30 s version (one clip A–D compressed) is the realistic test.
The page itself is a funnel: free prompt → course with "lifetime price before switching to yearly" scarcity. The earnings screenshot is marketing, not evidence of what the course teaches.
