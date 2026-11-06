# Scene JSON schema (poser ⇄ harness)

Same format for `poses.js` entries, `render-json.sh`, the artifact inbox/outbox and the Export tab. All keys optional except what you change; degrees for angles, metres for positions. Figure faces **+Z** (toward the camera at +Z); **+X is the figure's LEFT** (viewer's right); Y up; floor y = 0. Colours are decimal RGB numbers (0xffc27a → 16761466).

```json
{
 "title": "short name", "notes": "framing + key light side",
 "bg": 2763306, "floor": 3815994,
 "cam": {"pos": [x,y,z], "target": [x,y,z], "fov": 38},
 "light": {"keyPos": [x,y,z], "color": 16773856, "intensity": 2.2, "ambient": 0.35,
           "rimPos": [x,y,z], "rimColor": 10469631, "rimIntensity": 1.0},
 "figures": [ {"id":"fig-1","name":"มือกีตาร์","pose":{...}}, {"id":"fig-2","name":"มือกลอง","pose":{...}} ],  // one or more characters; legacy single "pose" still accepted
 "objects": [ {"id":"guitar","name":"กีตาร์","kind":"guitar","pos":[x,y,z],"rot":[x,y,z],"scale":1}, ... ],
 "pose": {   // = figures[0].pose (kept for single-figure consumers)
   "rootPos": [0,0.98,0], "bodyYaw": 0,
   "spineLean": 0, "spineTwist": 0, "spineTilt": 0, "chestLean": 0, "chestTwist": 0,
   "headPitch": 0, "headYaw": 0, "headTilt": 0,
   "armL": {"fwd":0,"out":8,"twist":0,"bend":5,"foreTwist":0}, "armR": {...},
   "legL": {"fwd":0,"out":3,"twist":0,"bend":0,"foot":0},   "legR": {...}
 }
}
```

## Pose semantics
- `rootPos` hip: standing y 0.98, seated on the 0.64 stool y 0.72. `bodyYaw` + turns the figure's left side toward camera.
- `spineLean` + forward. `headPitch` + looks down; `headYaw` + turns to the figure's left; `headTilt` ear-to-shoulder.
- Arms: `fwd` raise forward (90 horizontal, 170 overhead), `out` abduct sideways, `twist` rotate upper arm, `bend` elbow 0–150, `foreTwist` forearm.
- Legs: `fwd` thigh forward (85 seated), `out`, `twist`, `bend` knee (90 seated), `foot` toe up (+) / down (−).
- Walking: legL fwd 22 bend 8 foot 8 · legR fwd −14 bend 28 foot −20 · arms swing opposite (armR fwd −18, armL fwd 18).
- Playing guitar in front: fretting armL out 50–60 fwd 25–35 bend 70; strumming armR fwd 28–34 out 8–12 bend 48–55 twist 55.
- Guitar slung on back: armL fwd 38 bend 105 out 6 (hand on the strap).
- Singing at a mic: headPitch −6…−10, spineLean 5; mic stand at `[figX, 0, figZ+0.45]`.
- Drum pad player, SEATED on a stool (rootPos y 0.72, legs fwd≈80 bend≈86): spineLean 8, headPitch 16, armL fwd 58 out 16 bend 92, armR fwd 84 out 12 bend 62 (one stick raised); stool at `[figX,0,figZ-0.02]`, pad at `[figX+0.05,0,figZ+0.47]` scale `[1,0.86,1]`, rotated to face them. Standing variant: pad scale 1, spineLean 10, headPitch 18.
- Two characters: x ≈ −0.45 and x ≈ 0.8 (second slightly behind, z −0.3), camera two-shot `pos [0.25,1.35,4.7] target [0.15,1.0,0] fov 42`. Objects that belong to a figure are positioned relative to that figure's rootPos.
- Example: `tools/mannequin-pose/scenes/duo-guitar-drumpad.json`.

## Objects
`{"id","name","kind","pos","rot","scale","color"?,"parts"?}` — `scale` number or `[x,y,z]`; `color` tints every part.
Library kinds (origin at the base on the floor, facing +Z): `stool` (seat 0.64) · `chair` (seat 0.45) · `table` (top 0.74, 1.0×0.6) · `amp` (0.6×0.5×0.3) · `speaker` (0.4×0.7×0.35) · `mic` (1.58 tall, capsule at ~1.64) · `drumpad` (electronic pad on a tripod stand, pad at 0.93 tilted, two sticks) · `wall` (10×4 plane; put at z ≈ −0.9) · `box` (0.5) · `sphere` (r 0.25) · `cylinder` · `guitar` · `spot`.
- `guitar`: body centre is the origin, neck points +X before rot. Held in front `pos [0.02,0.95,0.26] rot [-10,0,22]`; on lap seated `pos [-0.02,0.86,0.36] rot [-8,-10,32]`; slung on back `pos [0.14,1.08,-0.26] rot [0,180,55]`.
- `spot`: `{"kind":"spot","pos":[0.5,4.2,2],"target":[0,1.2,0],"intensity":60}` (a light, not a mesh).
- `custom`: `"parts":[{"shape":"box|cylinder|sphere|cone|capsule|plane|torus","size":[...],"pos":[x,y,z],"rot":[x,y,z],"color":n,"roughness":0.8,"metalness":0}]` with sizes box `[w,h,d]`, cylinder `[rTop,rBottom,h]`, sphere `[r]`, cone `[r,h]`, capsule `[r,len]`, plane `[w,h]`, torus `[r,tube]`. Local `pos` is relative to the object's origin; keep the object's base at local y = 0 so `pos.y = 0` puts it on the floor (or `0.74` on a table top).

## Camera and light presets
- Full body: `cam.pos [0.4,1.2,4.2] target [0,0.95,0] fov 36` · 3/4 body: `[0.35,1.15,2.7] / [0,0.95,0.1] / 38` · close-up chest: `[0.3,1.6,2.0] / [0,1.45,0.1] / 34` · low angle: cam y ≈ 0.8–1.0 · profile: `[3.2,1.2,0.3] / [0,1.0,0]`.
- Key light: camera-left = negative x; softbox `[-2.5,2.6,2.4]` warm 16773856; sunset `[-4,1.4,3]` colour 16761466; top spot `[0.3,4,1.2]`. High-key: bg 14277081 floor 13619151 ambient 0.95. Stage: bg 394758 floor 855309 ambient 0.08–0.1 + a `spot` object.

## Presets to start from
`tools/mannequin-pose/poses.js`: `A` street walk (guitar on back, brick wall), `B` studio stool, `F` live stage (mic + spot), `G` close-up high-key. The poser's Presets chips are the same scenes.
