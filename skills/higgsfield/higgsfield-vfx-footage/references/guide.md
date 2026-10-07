# Focused guide

## Source lookup

Relevant Bible IDs: `A03 A13 A08.03 B6 B8 B10 D1 D3 D6 E1 E3 E4 E5`. Choose the needed IDs; do not load the entire list by default.

Use the shared helper at `../higgsfield-bible-director/scripts/bible_lookup.py` with repeated `--section ID`, or inspect `../higgsfield-bible-director/references/bible-snapshot.md`. These paths are relative to the skill root; resolve before calling. The helper is local and read-only. Shared contract: `../higgsfield-bible-director/references/operating-contract.md`.

## Operating notes

Verify current tools and plugin names before doing setup. The task of learning from a course is not authorization to install the course's integrations. New prompts written from these notes are authored synthesis, not course quotes; keep reusable templates in the director's assets dir. Write exact keep/change constraints and the permitted output purpose for every job.

- Core method (A03): pure video-to-video from a real clip, no keyframing, masking, tracking or rotoscoping [A03.L01 article]; levels are world swap, one-element change, handheld showcase [A03.L01 t=01:31-01:45]. Five closing rules: keep a real anchor, watch your edges, respect parallax, change one thing at a time, shoot for 4K [A03.L11 article].
- Plan before shooting: decide what the clip becomes, then film the real move with that world in mind [A03.L07 t=00:23-00:27] [A03.L08 t=00:00-00:06].
- Request template: `Seedance prompt for this clip — [describe your action + camera type]. Lock my action and the camera exactly. Turn it into [new world], me as [role].` [A03.L08 frames t=00:10]
- Multi-version request: `Give me three prompts for this clip. Lock my action and the camera. Three environment swaps: ...`; the keep-list carries over [A03.L03 frames t=00:20] [A03.L03 t=00:16-00:21].
- Long-prompt skeleton: `@source:` literal clip description + timed events -> PRESERVE block -> "transform only the world" -> `Photoreal. 16:9. <N>s.` -> relight block -> `Face and identity unchanged.` -> audio line [A13.L01 cue cue-intro-volcanic-drive] [A03.L03 cue neon-city].
- Keep-list = written anchor; grow it with the shot (subject, face, car, seatbelt, rig framing, camera position, driving motion) [A03.L02 article] [A03.L03 t=00:07-00:30]. Most of the prompt protects the performance; only a small part describes the effect [A03.L04 article].
- Anti-edit lock: `Do not re-frame, re-time, re-light or re-cut.` [A03.L05 cue hand-to-snake]; motion variant `Do not reinterpret, re-frame, re-time or re-angle any motion` [A03.L08 cue jungle-temple].
- Tie the change to a performance beat (snap ~2.2 s, a spoken line, head turn at 2-3 s), never a random moment [A03.L02 article] [A03.L05 cue hand-to-snake]. Hide the swap inside a light event (sun flare blooms white, new world on fade) and keep the original key direction [A03.L02 cue desert-swap].
- Inherit the plate camera (`INHERIT the source handheld orbit exactly`) so parallax and occlusion come free [A08.L03 cue cue-l3-screen] [A03.L03 article].
- Added light must hit the real subject (face, shirt, car paint) or it reads as a sticker [A03.L04 article] [A03.L04 t=00:56-01:01]. Effects sit behind real edges with contact shadows; a screen is "physical membrane portal, NOT a flat decal" [A03.L11 article] [A08.L03 cue cue-l3-screen].
- Constrain destructive effects: "holds its shape and silhouette, never charring away" [A03.L04 cue head-on-fire]; disambiguate left/right from the viewer's side [A03.L05 cue hand-to-snake].
- Reference role line: `Appearance, scale-texture and color reference only; ignore the photo's background and lighting` [A03.L06 cue lizards-climbing] [A13.L04 cue cue-add-figure-behind].
- Map real objects 1:1 to new-world objects (rig -> iron rungs, stairs -> deck, rail -> rigging) [A03.L08 cue jungle-temple] [A03.L10 cue kraken].
- Giant creatures: hide and scale with haze/partial reveals, slow heavy motion, same species every instance [A03.L09 cue sauropods] [A03.L09 article]. Protect real skin: "real human skin with pores, stubble ... never waxy" [A03.L09 cue sauropods] [A08.L06 t=01:06].
- Settings as recorded in the course: Seedance 2.0, video-to-video, 4K, 16:9 [A03.L02 cue desert-swap]; generate bar showed 330 credits [A03.L07 frames t=00:47]; about two minutes per generation [A03.L04 t=00:45-00:51].
- Failure modes: 1080p distorts details, on-screen text, lip-sync on crop [A03.L01 article] [A08.L03 t=01:31]; night relight raises face-drift risk, check the face first [A03.L10 article].
- Judge on a big screen; small screens hide detail [A03.L01 t=00:41]; compare ORIGINAL vs GENERATED side by side for small changed details [A08.L03 t=01:18].
- Premiere plugin (A13) setup path: Higgsfield web > Plugins > Download, then Window > Extensions > Higgsfield Plugin [A13.L02 t=00:00] [A13.L02 t=00:10]; sign-in is a browser OAuth consent (user-performed) [A13.L02 t=00:15].
- Pick the tool by scope: Edit Video (whole clip by text), Draw to Video (mask), Start/End frame (transition), Reframe, Upscale [A13.L06 article] [A13.L07 t=00:00]. Stack each result on a track above the source so you can always cut back [A13.L03 t=00:08] [A13.L08 t=00:17].
- Typed plugin prompts are short verb + object ("remove car", "Add an old man to the right", "Change outfit to pajamas") [A13.L03 frames t=00:07] [A13.L04 frames t=00:12] [A13.L05 frames t=00:10].
- Insert, not rebuild: lock performance, framing, lighting; carry a specific person's identity with an attached character sheet [A13.L04 article] [A13.L04 t=00:09].
- Background: `change the background behind the person to <view> <time of day>`; the result also relit the subject [A13.L06 t=00:01] [A13.L06 t=00:15].
- Plugin UI as recorded: Seedance 2.0, 16:9, 1080p, 4s results, jobs queue [A13.L01 frames t=00:35] [A13.L07 t=00:10]; Upscale 1k/4K buttons read 5 vs ...13, unlabeled [A13.L10 frames t=00:05] [A13.L10 frames t=00:07].
- Mask scope can be exceeded (torso mask produced full pajamas) [A13.L05 t=00:15]; short prompts may drop spoken detail [A13.L08 frames t=00:12]. Reframe output choice is per-shot (9x16 too tight here, 21x9 chosen), not a universal rule [A13.L09 t=00:23]; 4:3 appeared to extend the frame [A13.L09 t=00:25].

## Known contradictions

- The A13 titles say "Quixel", but the audio and every screen say Higgsfield plugin; use Higgsfield [A13.L02 t=00:00] [A13.L02 frames t=00:18] [A13.L01 t=00:54] [CP.A13].
- A13 cues for L01/L04/L06 describe footage not seen in sampled tiles (it matches A03 footage), so a cue is not always the final prompt [A13.L04 cue cue-add-figure-behind] [CP.A13].
- A03: the narration says hand to snake but the result shows a silver mech arm; the source clip is urban but the cue says forest; the duration chip reads 15s vs 8s in the cue [A03.L05 frames t=00:35] [A03.L09 frames t=00:05] [A03.L07 frames t=00:47].
- A13 article puts transitions in "Video Generation", but the panel header reads "Edit video" [A13.L07 article] [A13.L07 frames t=00:07]. A08 L03 cue says 16:9 but the laptop source clip is vertical [A08.L03 frames t=00:05].
- A03 L03/L04 use "SFX only" while the presenter speaks; other cues say "SFX and source dialogue only" [A03.L03 cue neon-city] [A03.L02 cue desert-swap].
- Evidence gaps: no per-job credit totals (unlabeled Upscale number); some results are absent from sampled tiles (car removal) [A13.L10 frames t=00:07] [A13.L03 t=00:08].
