# mannequin-pose — wooden-mannequin pose harness

Blocks pose / camera / key-light for a shot as a jointed wooden mannequin (the artist's sketch
dummy) plus a dreadnought guitar and simple props, rendered with headless Chrome + three.js.
The PNG is used as a **pose reference** alongside identity + wardrobe refs in GPT Image 2.5
Sunburst (Higgsfield image-edit), so the model gets body position, framing and light direction
without any likeness bias.

- `poses.js` — one entry per concept: camera, lights, guitar placement, props, joint angles (conventions documented at top of file).
- `mannequin.html` — the scene. Open directly in a browser with `?pose=B` to tweak live.
- `render.sh [OUT_DIR] [IDS...]` — renders 900x1200 PNGs via `Google Chrome --headless=new --screenshot` (no playwright/puppeteer needed; `--allow-file-access-from-files` lets the ES module load from disk).
- `sheet.html` — contact sheet; screenshot it the same way for a review board.

Verified 2026-11-06 on macOS with Chrome app + Node 22 + three@0.170.0: renders A/B/F/G in ~3 s each.

## Interactive poser (artifact)

`poser.html` is the same mannequin as an interactive page: orbit camera, click a joint → rotate it with
the gizmo rings or sliders, presets A/B/F/G, guitar front/back/none, stool/mic/wall props, key-light
and background controls, prompt → pose (Claude via the artifact `sample` capability, with an offline
keyword fallback), 3:4 PNG snapshot and pose JSON in the same schema as `poses.js` (paste it back into
`poses.js` and run `render.sh`).

Published 2026-11-06 as a private claude.ai artifact: https://claude.ai/artifact/9AhtJ19m85QVuuJU5L4V2k
(slug `4223ffc4-adee-4ddc-a759-6e673e560cbd`, capabilities `sample` + `downloads`). Republish after edits
with `publish_files` on this file as `index.html` plus `objlib.js`.

v2 (2026-11-06): scene objects. `objlib.js` is shared by the poser and `mannequin.html`: a library
(stool, chair, table, amp, speaker, mic, wall, box, sphere, cylinder, guitar, spot) plus `custom`
objects built from primitives (box/cylinder/sphere/cone/capsule/plane/torus). In the poser every
object and the figure itself can be selected from the Objects tab or by clicking, then moved /
rotated / scaled with the gizmo (W/E/R) or sliders, duplicated, deleted, recoloured; new objects come
from the library dropdown or from a prompt (Claude returns the full `objects` list, custom ones as
`parts`). Scene JSON now carries `objects`; legacy `guitar/props/wall` still load. Local test must go
through http (e.g. `python3 -m http.server 8765` in this folder): the app preview turns file:// pages
into data: URLs where the relative `objlib.js` import cannot resolve.

## v3 (2026-11-06): Claude Code ⇄ artifact channel + skill

The artifact declares `db` (+ `user`). `poser/inbox` = Claude → page (banner with โหลด; auto-loads on
a fresh page); `poser/outbox` = page → Claude ("ส่งฉาก + ภาพไป Claude" in Export: scene + jpeg data URL +
note). Claude Code writes/reads them with `mcp__claude-artifacts__db_write` / `db_get` (pass `ifVersion`
when the doc exists). `render-json.sh <scene.json>` renders any exported scene headless (`mannequin.html?json=`).
Skill: `skills/mannequin-poser/SKILL.md` (+ `references/scene-schema.md`). Example scene: `scenes/example-seated-amp.json`.

## v4 (2026-11-06): multiple figures

`mannequin-lib.js` (shared `buildMannequin` / `applyPoseTo` / `readBackJoint`) is used by both the harness and
the poser. Scene JSON has `figures: [{id,name,pose}]`; the legacy single `pose` still loads and is exported as
`figures[0].pose`. Poser: Pose tab has a character dropdown, + เพิ่มหุ่น / ลบ / ทำสำเนา; characters also appear
as blue buttons in the Objects tab for whole-body move/rotate. New library object `drumpad`. Preset "Duo · guitar +
drum pad" = `scenes/duo-guitar-drumpad.json`.

## v5 (2026-11-06): library

แท็บ คลัง: Save / Save-as / list / load / delete, stored in the artifact db collection `scenes` (thumb jpeg 180×240, title, scene, savedAt, source, note); localStorage fallback when `db` is null. Inbox pushes from Claude are auto-archived as `claude-<sentAt>`.
