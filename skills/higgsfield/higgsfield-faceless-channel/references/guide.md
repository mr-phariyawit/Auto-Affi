# Focused guide

## Source lookup

Relevant Bible IDs: `A11 A12 B12 B13 D2 D7 E3 E4 E5`. Choose the needed IDs; do not load the entire list by default.

Use the shared helper at `../higgsfield-bible-director/scripts/bible_lookup.py` with repeated `--section ID`, or inspect `../higgsfield-bible-director/references/bible-snapshot.md`. These paths are relative to the skill root; resolve before calling. The helper is local and read-only. Shared contract: `../higgsfield-bible-director/references/operating-contract.md`.

## Operating notes

Verify current tools and plugin names before doing setup. The task of learning from a course is not authorization to install the course's integrations. Quoted prompts are as recorded; new prompts are authored synthesis, and reusable templates belong in the director's assets dir. Uploading, scheduling, subscribing to automation and voice cloning are separate user-authorized steps. Prices, credits, RPM and earnings below are as recorded in the course, never current fact; check current official platform policy when eligibility affects a release.

- Split the work: Claude thinks (topic, script), Higgsfield produces (video, thumbnails, shorts), the human still picks outputs and uploads; keep every step in one chat so one-line prompts can refer to "this video". [A11.L11 article] [A11.L01 t=00:52–01:07]
- Topic: let live research plus scoring pick it, not brainstorming; course prompt `What's actually working in <format> right now?` and expect short decisive answers ("no long answers and no 20 options"). [A11.L03 cue prompt-001] [A11.L03 t=00:00–00:40] [A11.L03 t=00:12–00:20]
- Niche: both courses rank education at the top by RPM; A11 says stay in one niche because mixing "resets it to zero" (course claim, unsourced). [A11.L03 t=00:20–00:29] [A12.L03 t=00:14–00:37] [A11.L03 t=00:56–01:08]
- Originality: borrow a proven format, never videos; YouTube flags spam/unoriginal content whether AI or not, so an original script with insight is what protects revenue. [A12.L01 t=01:56–02:03] [A11.L04 t=00:16–00:29] [A12.L06 t=00:27–00:39]
- Two layers: the prompt controls visuals, the script controls meaning; no real script gives "beautiful nonsense". Judge coherence (one narrator, one style, one idea), not single-clip beauty. [A11.L04 t=00:03–00:11] [A11.L05 t=00:32–01:03]
- Script: post a plan first (angle, hook, structure), open the hook with payoff not backstory, make each chapter hand off to the next question, add an open loop about every minute. [A11.L04 frames t=00:03] [A11.L04 t=00:41–01:01]
- Length math (as recorded): ~1,450 words at ~150 wpm is ~10:00, rendered as 60 clips of 10 s, past the 8-minute mid-roll threshold; re-grid the script before changing length. [A11.L05 frames t=00:04]
- Make the script a machine-readable shot list (acts, timecode, clip ID, VO per clip). Header seen: `Clip breakdown — <video model> (silent) + one continuous <TTS voice> 16:9 1080p | TOTAL 5:00 (300s) | 35 clips | scenes 5/8/10s | VO verbatim per clip`; per clip `C1 — 10s | <visual>` then the quoted VO line. [A12.L03 frames t=01:37] [A12.L03 t=01:35] [A12.L04 cue cue-video-prompt]
- Pacing: change the visual every 5–10 s (5 minutes needs at least 30 clips); 5 s for punchy beats, 10 s for reveals; clip lengths must sum exactly to the target (300 s). [A12.L04 t=00:00–00:14] [A12.L04 t=00:25]
- Course prompts: script `Analyze the [channel] (scenarios, hooks) and write me a script for a similar video: <reference channel /videos URL>`; video `make a <length> video like on the reference account using <video model>. <resolution>. It's going on a <destination>.` (needs the shot list in the same conversation). [A12.L03 cue cue-script-prompt] [A12.L04 cue cue-video-prompt]
- Before spending: check workspace, balance, model spec and existing project folders; A12's Claude re-rendered all 35 clips plus narration (~3,000 credits as recorded) before finding a finished package/ folder. Count failed and repaid generations in real cost. [A12.L04 t=00:40] [A12.L05 t=01:00] [A12.L05 t=00:50]
- Assembly seen: render in batches (C1–C12, C13–C24, C25–C35) with VO and music in parallel; ffmpeg concat, one continuous VO, music ducked to ~10%, 1080p export into audio/, clips/, out/, package/, SCRIPT.md, SHOTLIST.md, MANIFEST.md. [A12.L04 frames t=01:05] [A12.L04 t=01:15–01:20] [A12.L04 t=01:05]
- VO drift: narration came out 5:11, ~17 s longer than planned, and Claude stretched video ~5%; check VO duration against the clip grid before assembly. [A12.L05 frames t=00:15]
- Content filter: historical Pompeii shots got NSFW false flags (Claude guessed "victims"); rephrase as "cinematic silhouette, dramatic ash, no visible injury"; flagged generations showed "Credits refunded". [A12.L05 t=00:10] [A12.L04 t=00:25] [A12.L05 t=02:00]
- Localization: `Translate the video into <language>.` re-rendered the whole video, changing one variable; translation quality and which voice the Spanish version used were not shown, so review terminology, pronunciation and timing yourself. [A11.L06 cue prompt-002] [A11.L06 t=00:00–00:26] [A11.L06 frames t=00:10]
- Voice clone path seen: Audio → Voice Presets → Create custom voice → record the sample script → upload .mp3 → reusable preset; the course's reason (unique voice, human signal, fewer flags) is a claim. [A11.L07 t=00:00–00:27] [A11.L07 t=00:27–00:39]
- Packaging: one focal point readable at phone size, 1–4 words, title opens a question the thumbnail withholds; on-screen prompt `Create 3 titles and 3 thumbnails for this video`, choice made via Q/A widget. [A11.L08 t=00:25–00:31] [A11.L08 t=00:15] [A11.L08 t=00:31–00:38] [A11.L08 t=00:10]
- Upload package: `Put together a complete YouTube video package for me: prepare the <thumbnails, title> and everything else needed to upload it.` Seen: 3 distinct thumbnails for A/B (3–4 words, one yellow accent), 1280×720 JPG, title ≤ ~60 chars, Altered/synthetic content = YES, Not made for kids, captions.srt. [A12.L05 cue cue-packaging-prompt] [A12.L05 t=00:37–00:42] [A12.L04 t=00:25] [A12.L05 t=01:35] [A12.L05 t=00:50]
- Shorts: `Create shorts from this video with <tool>.` gave ~20 captioned 9:16 clips (Warm Glow, ~180 credits as recorded); on-screen "the 119-second cut was the fix" implies an unexplained retry. Viral-mechanics variant at [A12.L06 t=00:55]. [A11.L09 cue prompt-004] [A11.L09 frames t=00:10]
- Planning: `Plan my first <N days>: <count> long videos, topics ranked by <metric>.` then `Start videos <i> and <j> from the plan.`; course cadence 2 long/week plus a daily short, using AVD drop-off as the next script note. [A11.L10 cue prompt-005] [A11.L10 cue prompt-006] [A11.L10 t=00:41–01:06]
- Watch-hours math: hours ÷ average view = total views (4,000 h at 4 min ≈ 60,000); course threshold 1,000 subs + 4,000 h, while an A12 card adds "10M valid public Shorts views". [A11.L09 t=00:39–00:56] [A11.L09 t=00:39–00:44] [A12.L06 frames t=00:07]
- Economics on screen, unsourced: Claude's RPM table (Education $8–20, AI/tech $15–35), vidIQ cards ($1.6K/month at 5.7M views; Bright Side $39.5K est.), ~2,500 credits per 5-minute video. [A11.L03 frames t=00:15] [A11.L03 frames t=00:48] [A12.L01 t=01:05] [A12.L04 frames t=01:05]
- Automation removes routing, not responsibility: inspect the full output (listen, scene-to-script match, labels, export) because "done" hid self-fixes. Connector seen at `https://mcp.higgsfield.ai/mcp` via OAuth consent; "only use connectors from developers you trust". [A12.L05 t=02:03] [A12.L05 t=00:10] [A12.L02 frames t=00:13] [A12.L02 t=00:25] [A12.L02 t=00:20]

## Known contradictions

- E3: "I didn't write a single correction" vs on-screen Claude resubmitting filtered clips and stretching VO. [A12.L05 t=02:03] [A12.L05 t=00:10]
- E3: "one prompt" script, but Claude recalled memory and a shot list from a prior session; result in a fresh account is unknown. [A12.L03 t=01:35] [A12.L04 t=02:48–02:56]
- E3: A11's one-niche rule vs posting translated versions on the same channel is never reconciled. [A11.L03 t=00:56–01:08] [A11.L06 article]
- E4: MCP/skill links "in the description" are not in the course files; Claude model labels differ between lessons. [A11.L02 t=00:19–00:20] [A11.L02 frames t=00:02]
- E4: business results unvalidated: A12's 3-day stats are vanity metrics, A11's niche-test numbers have no source. [A12.L07 t=00:05] [A11.L03 t=01:00–01:05]
- E5: A11 "a hundred scenes" vs "60 clips of 10 seconds"; Shorts in the same chat vs Shorts Studio. [A11.L05 t=01:00–01:03] [A11.L11 t=00:00–00:10] [A11.L11 article]
- E5: A12 durations disagree (5:00 / 4:52 / 5:11 / 4:59) and uploaded thumbnails do not match Claude's list. [A12.L04 t=01:05] [A12.L05 frames t=00:35] [A12.L05 t=00:40]
