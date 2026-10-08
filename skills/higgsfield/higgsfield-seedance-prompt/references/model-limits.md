# Model limits as recorded in the courses (not current API docs)

Re-check the live Higgsfield UI before spending credits: menus and prices change after recording.

| Model | Max duration | Durations seen | Resolution | Aspect ratios | Batch | Inputs |
|---|---|---|---|---|---|---|
| Seedance 2.0 | 15 s [A05.L02 t=01:41] | 5 s [A10.L02 t=03:30–04:34]; 8 s [A06.L05 frames t=01:02]; 10 s [A06.L07 frames t=00:53]; 15 s [A01.L05 frames t=00:05] | 480p / 720p / 1080p menu [A10.L04 t=01:56–02:08]; 4K [A01.L05 frames t=00:05] [A05.L11 t=00:15] [A16.L05 frames t=00:10] | Auto, 16:9, 9:16, 4:3, 3:4, 1:1, 21:9 [A01.L05 frames t=00:05]; 9:16 15 s via MCP generate_video [A07.L04 frames t=00:36] | 1/4–4/4 [A01.L05 frames t=00:05] [A10.L02 frames t=04:13] | images [A15.L03 frames t=01:35]; audio input [A06.L13 t=04:05]; T2V/V2V/I2V [A08.L01 t=00:33]; @video1 extend [A04.L03 cue scene1-animated] |
| Seedance 2.5 | 30 s [A05.L02 t=01:38] | all examples 30 s | 720p in every example; unclear if permanent [A05.L11 t=00:00] [A05.L11 article] | 9:16 UGC example [A05.L07 t=00:02] | not shown | "COMING SOON" at recording [A05.L11 t=00:26] |
| Marketing Studio (Seedance 2.0) | 15 s default | — | 1080p default | 9:16 default; TV Spot 16:9 [A09.L04 frames t=00:02] [A09.L07 frames t=00:47] | — | — |

Conflicts:
- A08 promotes 4K, but most of its Recreate links are 1080p [A08.L01 cue cue-l1-kaiju] [A08.L01 frames t=02:46].
- A16 instructor says 4K [A16.L03 t=01:08]; one bar reads 1080p [A16.L02 frames t=01:22], the fight bar 4K [A16.L05 frames t=00:10].
- A10's menu lists only 480p/720p/1080p [A10.L04 t=01:56–02:08].
- A course prompt itself runs to 16.0 s on a 15 s model (A01 recreate-2-1d, found by the linter) — course cues can break their own limits.
