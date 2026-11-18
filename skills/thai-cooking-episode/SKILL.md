---
name: thai-cooking-episode
description: "Use when producing or publishing an episode of the สายตำ Thai-cooking channel (EP02 onward): picking the dish, researching authentic taste and the four pillars, writing the sourced VO script, generating illustrations with GPT Image 2.5 Sunburst, recording the Gemini Sulafat VO, music/SFX, building the animatic or the pixel-kitchen render, adding EN+TH subtitles, rendering the MP4, making Shopee affiliate links, and posting per platform (TikTok / Facebook / Instagram / YouTube). Triggers also on ตอนที่ 2, ตอนต่อไป, ทำเมนูใหม่, ช่องอาหารไทย, ผัดกะเพรา, ต้มยำ, คลิปทำอาหาร, ซับไตเติล, โพสต์คลิปอาหาร. Not for the JIAB character sheet or product-review ads."
---

# Thai-cooking episode

One pipeline from a dish name to a verified post on every platform. EP01 (ผัดกะเพรา) built it; read [docs/thai-cooking-channel/ep01-retro.md](../../docs/thai-cooking-channel/ep01-retro.md) once per session for what went wrong and why.

Hard rules live in [docs/thai-cooking-channel/rules.md](../../docs/thai-cooking-channel/rules.md). The step-by-step walk-through with exact commands is [docs/thai-cooking-channel/workshop-ep02.md](../../docs/thai-cooking-channel/workshop-ep02.md). Before reporting any stage as done, run its row in [docs/thai-cooking-channel/soul-checklist.md](../../docs/thai-cooking-channel/soul-checklist.md).

## Where are we? Start at the first stage that is not done

| # | Stage | Output (per episode folder `output/thai-cooking-channel/ep<NN>-<slug>/`) | Done when | Spends? |
|---|---|---|---|---|
| 0 | Open decisions | answers recorded in the episode's `README.md` | dish, art style (pixel-hybrid or ink-gouache), channel name status are written down | no |
| 1 | Research | `reports/<dish> รสดั้งเดิมและสี่เสา.md` + table "ใช้ได้ / ห้ามใช้" | every claim has a source the agent opened | no |
| 2 | VO script | `script/vo-script-v1.md` (EN lines + TH subtitle lines + source per line) | owner approves the script | no |
| 3 | Illustrations | `assets/library/...` + `manifest.json` | QA pass per asset, spend under the cap | **yes** (OpenRouter) |
| 4 | VO | `audio/vo-en-v1/*.wav` + `.json` | STT of every line matches the script | **yes** (Gemini, small) |
| 5 | Music + SFX | `audio/music/`, `audio/sfx/` | owner listened, or accepted the EP01 recipe | **yes** (kie.ai credits) |
| 6 | Picture | animatic (HyperFrames) or pixel render | timed from the VO; all text in the safe area | no |
| 7 | Subtitles | EN main line + smaller TH line, burned in | every subtitle matches the VO line and fits the safe area | no |
| 8 | Final MP4 | `final/ep<NN>-v<N>.mp4` | soul-checklist row 8 passes (frames, loudness, STT, watermark) | no |
| 9 | Affiliate links | `affiliate-links.md` | each `s.shopee.co.th` link redirects to the right item ID | no |
| 10 | Post | one post per platform, per the platform table in rules.md | owner approved the caption; live post opened and checked | public — owner approves |

Every generation step goes through the project's pre-generation audit: show the prompt and the spend cap, get the owner's go, then generate (memory `feedback_pre_generation_audit_gate`).

## Tools that already work (verified in EP01)

| Job | Tool | Notes |
|---|---|---|
| Illustration | `tools/thai-assets-gen.py --ids a,b` | reads `assets/manifest.json`, never overwrites, stops at the cap. Sunburst drifts photoreal on metal/stone/cooked food: add the "flat ink-and-gouache plate, two or three flat tonal steps, no specular highlights" paragraph |
| Photoreal stage images | `tools/openrouter-imagegen.py --ref <empty-wok.png>` | passing the previous stage as IMAGE 1 holds framing so stages crossfade |
| VO | `tools/gemini-tts.py --model gemini-2.5-pro-preview-tts --voice Sulafat --text "Say at a brisk, lively pace, like a warm confident cooking-show narrator: <line>"` | multi-sentence style text is read aloud — keep the one-line directive form |
| STT check | `tools/gemini-stt.py` | re-transcribe once before regenerating a line |
| Music | kie.ai Suno V6, `POST /api/v1/jobs/createTask` model `ai-music-api/generate` | 12 credits for 2 variations; request saved in EP01 `audio/music/request.json` |
| SFX | ffmpeg synthesis (EP01 `audio/sfx/synth/`) | kie ElevenLabs SFX returned 500s; owner accepted synth SFX |
| Animatic | HyperFrames (`npx --yes hyperframes`), template = EP01 `animatic-v2/index.html` | safe area: text in y 288–1248, x 120–888 (x 120–780 below y 840) |
| Pixel render | EP01 `demo/pixel-style-demo/` → `python3 build.py`; serve with `python3 -m http.server 8931`; `pixel-v1/capture.cjs <outDir>` | render mode `?render=1`, `window.__seek(seconds)`; set `SEG` from the VO segment starts |
| Encode | `ffmpeg -framerate 30 -i f%05d.png -i mix.wav -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart` | target about -14 LUFS, true peak ≤ -1 dBTP |
| Affiliate links | in-app browser, logged in to the affiliate Shopee account → `affiliate.shopee.co.th/offer/product_offer` → search → item page → "เอา ลิงก์" | read the short link from the dialog's textarea; verify with `curl -s -o /dev/null -w '%{redirect_url}'` |
| Posting | Postiz: `npx --yes postiz upload <mp4>` then MCP `integrationSchedulePostTool` (TikTok: `DIRECT_POST`) | status: `npx --yes postiz posts:list \| tail -n +2` |

## Subtitles (new from EP02)

English is the main line; Thai sits under it, smaller (about 60–65% of the English size). One subtitle per VO line, on screen for the whole line. Both lines must stay inside the safe area and must not cover the step card or the chef. Thai text is the TH column of the script, not a machine translation made at render time. This overrides the EP01 "no Thai characters on screen" rule for subtitles only; other on-screen labels stay English.

## Platform split (summary — rules.md is the source)

- **TikTok**: no Shopee links, no "Shopee" / "link in bio" calls to buy, in caption or in the video. Render a TikTok cut whose end card has no Shopee box. Turn on the content disclosure only if the post earns commission (TikTok Shop). Caption edits are possible only in the first 7 days, once a day; commercial-content posts only in the app.
- **Facebook / Instagram / YouTube**: Shopee product links + hub link in the caption/description, with the #โฆษณา #ad affiliate line, and each platform's paid-partnership / paid-promotion setting where its rules require it.
