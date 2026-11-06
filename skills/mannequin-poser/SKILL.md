---
name: mannequin-poser
description: "Use when the operator wants a pose / blocking / pose-reference for a shot: จัดท่า, ท่าหุ่น, หุ่นไม้, mannequin, poser, pose ref, blocking, draft ท่า, ส่งท่าไป artifact, เปิดใน poser, or when a Claude-side scene (pose + objects + camera + key light) must be shown in the Mannequin Poser artifact for the operator to review or edit, or read back from it after they edited. Converts a text brief into scene JSON, renders a check PNG headless, pushes the scene to the artifact inbox, and reads the operator's edits from the outbox. Not for generating the final photo (that is the GPT Image / OpenRouter route) and not for JIAB identity sheets."
---

# Mannequin Poser — scene from text, shown in the artifact

Artifact: **Mannequin Poser — หุ่นไม้ 3D จัดท่า** · url `https://claude.ai/artifact/9AhtJ19m85QVuuJU5L4V2k` · slug `4223ffc4-adee-4ddc-a759-6e673e560cbd`.
Source: `tools/mannequin-pose/` (`poser.html`, `objlib.js`, `mannequin.html`, `poses.js`, `render.sh`, `render-json.sh`). Operator guide: `tools/mannequin-pose/USAGE-TH.md`.

Channels on the artifact's db (capability `db` is declared):
- `poser/inbox`  — Claude → page. The page shows a banner "Claude ส่งฉากมา: <title>" with a โหลด button (auto-loads on a fresh page).
- `scenes/<id>` — the page's library (แท็บ คลัง): every scene the operator saved (`source:"user"`) and every inbox push auto-archived (`source:"claude"`, id `claude-<sentAt>`). Each doc: `title, scene, thumb (jpeg data URL 180×240), savedAt, source, note`. Browse with `db_list`/`db_query` on collection `scenes`; load one with `db_get scenes/<id>`. To re-show an old job, read it here and push its `scene` to `poser/inbox` again.
- `poser/outbox` — page → Claude. The operator presses "ส่งฉาก + ภาพไป Claude" in the Export tab; the doc holds `scene`, `image` (jpeg data URL or null), `sentAt`, `note`.

## Procedure

1. **Build the scene JSON** from the brief using [references/scene-schema.md](references/scene-schema.md). Start from the nearest preset in `tools/mannequin-pose/poses.js` (A street / B stool / F stage / G close-up) and change only what the brief implies. Objects outside the library are `kind:"custom"` with `parts` (primitives). Give the scene a `title` (short, Thai ok) and `notes` (one line: framing + key light side).
2. **Save and render it** so you see it before the operator does:
   ```bash
   tools/mannequin-pose/render-json.sh tools/mannequin-pose/scenes/<slug>.json
   ```
   Read the PNG, check: figure inside the 3:4 frame, hands near the guitar neck/strings if playing, feet on the floor (standing hip y 0.98, seated 0.72), objects not intersecting the figure, key light on the intended side. Fix and re-render until it reads. Display the PNG inline ([[feedback_always_show_images]]).
3. **Push to the artifact** with `mcp__claude-artifacts__db_write`:
   ```json
   {"slug":"4223ffc4-adee-4ddc-a759-6e673e560cbd","ops":[{"op":"set","path":"poser/inbox","ifVersion":<version from db_get if the doc exists>,
     "data":{"scene":<scene json>,"title":"<title>","note":"<what to check>","sentAt":"<ISO time>"}}]}
   ```
   `db_get poser/inbox` first: if it exists you must pass its `version` as `ifVersion`. Then tell the operator in one line: open the artifact, the banner loads the scene (or press โหลด), edit if needed, then press "ส่งฉาก + ภาพไป Claude".
4. **Read back** when the operator says they sent it (or when asked "เอาท่าที่ผมจัดมาใช้"): `db_get poser/outbox` → save `scene` to `tools/mannequin-pose/scenes/<slug>-operator.json`, decode `image` (if present) to a jpg next to it, render the JSON with `render-json.sh` for the clean 900×1200 pose PNG, and display it. That PNG is the pose reference for the gen step (IMAGE 3 after face-front and face-side; see [[reference_openrouter_gpt_image_sunburst]]).
5. **Persist**: keep every scene JSON under `tools/mannequin-pose/scenes/`; if the operator approves a pose for a recurring shot, also add it to `poses.js` so `render.sh` and the preset list can use it.

## Honesty
- A pushed scene is `[PRODUCED]` until the operator confirms it appeared; the inbox banner cannot be verified from Claude Code. Say so.
- Never claim a pose "matches the brief" without having looked at the rendered PNG.
- Rendering is free; the gen step costs money — this skill ends before any spend.

## Gotchas
- Headless render needs the Chrome app; `render-json.sh` passes `--allow-file-access-from-files` so the JSON loads from disk. No playwright is installed.
- The artifact page cannot be tested from `file://` in the app preview (relative `objlib.js` import fails in a data: URL); serve with `python3 -m http.server` for local checks.
- `db_write` refuses without `ifVersion` on an existing doc — always `db_get` first.
- Document body limit is 256 KiB: an outbox `image` may be null when the jpeg was too big; render the scene JSON instead.
