# Focused guide

## Source lookup

Relevant Bible IDs: `A14 A14.02 A14.03 A14.04 A14.05 A14.06 A14.07 A14.08 A14.09 A14.10 B13 D1 D2 D3 D4 D7 E4 E5`. Choose the needed IDs; do not load the entire list by default.

Use the shared helper at `../higgsfield-bible-director/scripts/bible_lookup.py` with repeated `--section ID`, or inspect `../higgsfield-bible-director/references/bible-snapshot.md`. These paths are relative to the skill root; resolve before calling. The helper is local and read-only. Shared contract: `../higgsfield-bible-director/references/operating-contract.md`.

## Operating notes

Verify current tools and plugin names before doing setup. The task of learning from a course is not authorization to install the course's integrations. Connecting an account, deploying, or publishing publicly is a separate user-authorized step. New prompts and briefs are authored synthesis, not course quotes; reusable templates live in the director's assets dir. Game trailer-only tasks route to cinematic direction.

- Split roles: Claude writes game logic; Higgsfield MCP supplies skins/textures/environments and hosting. Claude alone yields a working tech demo of capsules and grey boxes, so diagnose that baseline first. [A14.L04 t=00:24] [A14.L04 t=00:16]
- Fair comparison: same prompt, same model, toggle only MCP + skill, then compare visuals. [A14.L04 t=00:00]
- Setup as recorded: Claude > Customize > Connectors > "Add custom connector" with a "Remote MCP server URL", then OAuth Allow; then Customize > Skills > upload custom skill "game-studio" (Trigger "Slash command + auto"). [A14.L02 t=00:04] [A14.L02 frames t=00:08] [A14.L02 frames t=00:15]
- The working connector endpoint was `https://mcp.higgsfield.ai/mcp`, not the setup page URL; a connector counts as proven only once real results return. [A07.L03 frames t=00:31] [A07.L03 article]
- Model chip seen in the course: "Fable 5 High"; the generation model for textures/skins/sound, resolution and seed were never named. [A14.L03 frames t=00:14] [A14.L03 frames t=00:29]
- One-line pitch templates: `Build a <perspective> <genre> game where I <traversal verb + vehicle>, <primary combat verb + target>, and <secondary interaction> for <secondary combat mode> on <location>.` and `Build a <world style> <genre> with <team structure>, where I can <sandbox verbs> and <combat objective>.` [A14.L03 cue pirate-prompt] [A14.L05 cue blockfield-prompt]
- The one-liner only seeds an interview; the expanded "studio-grade brief" is the real build prompt. Interview axes: camera/controls, look & setting, match size, weapon set, round-end rule (multiple choice, plus "Something else" and Skip). [A14.L05 t=00:49] [A14.L05 t=00:39] [A14.L05 frames t=00:35]
- GDD/brief skeleton: `TITLE / ONE-LINE PITCH / GENRE (avoid trademarked names) / CONTROLS / WEAPONS AND TOOLS (numbered, stats + trade-off each) / SYNC RULES / MAP (layout, bases, spawn, respawn UI)`. Approve it before build, since it locks controls, weapon stats, map and respawn. [A14.L05 frames t=00:40]
- Give each weapon an observable trade-off (sniper: slow fire, scope, high damage; bazooka: rocket, splash, destroys blocks). [A14.L05 t=01:25]
- Input/HUD evidence from the pirate game: Q harpoon to board, E man the cannon, sails % and distance readout; test aim, contact, damage and boarding state transitions. [A14.L03 frames t=00:29]
- Webcam hand-tracking: lost finger tracking costs the blade, bombs cost hearts; the hard part is tracking + prediction + physics together, so test lost-tracking and restart. Actual camera access is an execution step. [A14.L06 t=00:32] [A14.L06 t=00:58]
- Plan a mic fallback for voice chat ("Microphone unavailable", listen-only). [A14.L05 frames t=01:25]
- Deploy lands on a *.higgsfield.gg link; keep the returned game_id and reuse it, or every edit spawns a new game at a new URL. [A14.L05 t=01:00] [A14.L05 frames t=01:02]
- Recorded deploy failure modes: first zip URL guess returned 403 then retried with the right object URL; a publish name collision changed the marketplace title. [A14.L05 frames t=01:02]
- Playtest with two tabs or a friend's link, then tune skill-suggested values (splash radius, fire rate, respawn timer). [A14.L05 frames t=01:00]
- Keep stages separate: design proposed, built, local play, deployed (you share the link), published (strangers find, play, remix). Media output is not evidence game logic works. [A14.L07 t=00:06]
- Signals: plays are a free fun signal, remixes a stronger one; start small and use real signals before scaling. Give players/concurrent/remix figures explicit windows and denominators. [A14.L07 t=00:28] [A14.L08 t=00:22]
- Cost as recorded in the course: $68 total for 3 games including failed generations, per-game split unclear; always count failed and repeated generations. [A14.L09 t=00:00] [A14.L09 frames t=00:05] [A14.L09 t=00:02]
- Publish plan as shown on screen: funnel STEP 1 publish, STEP 2 real-player test, STEP 4 distribute, STEP 5 earn (STEP 3 unseen); target platforms, pricing, rev share and asset licensing were never stated. [A14.L09 frames t=00:15] [A14.L09 t=00:22]
- Seek outside review instead of self-assessment; the studio CEO framed it as "prototyping", a prototype-level endorsement, not a shipped-game benchmark. [A14.L09 t=00:35] [A14.L10 frames t=00:55]

## Known contradictions

- Instructor says the marketplace is "almost empty", yet ~17 other games show on screen; remix count 120 vs 121. [A14.L07 t=00:19] [A14.L07 frames t=00:05] [A14.L08 t=00:22]
- Spoken pirate prompt ("add enemy ships") differs from the typed cue ("at enemy ships"); use the typed one. [A14.L03 t=00:11] [A14.L03 cue pirate-prompt]
- CEO transcript "10 million dollars" is a whisper mistranslation of Korean; on-screen subtitle says "$1 billion in annual revenue". [A14.L10 frames t=00:25]
- Player counts (~4,000 / 121 remixes) are self-reported; listing numbers are illegible. [A14.L08 frames t=00:00]
- The skill file itself is not in the course materials; only a low-res description was visible, so full skill rules are unknown. [A14.L02 t=00:17] [A14.L02 frames t=00:15]
- Hosting/multiplayer claims were never independently tested; pirate and NeonSlice interview/brief and prompt were not shown. [A14.L04 frames t=00:55] [A14.L03 t=00:11] [A14.L06 t=00:14]
