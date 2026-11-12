# Football kick — JIAB (2026-11-12)

Pose ref: `tools/mannequin-pose/scenes/kick-ball.json` → `pose-kick-ball.png` (caption bar cropped off).

| Round | Model | Refs (in order) | Cost [VERIFIED: usage.cost in API response] | Result (visual review) |
|---|---|---|---|---|
| r1 `kick-r1.png` | openai/gpt-image-2.5-sunburst, high, 3:4 | mannequin, face-front, face-side | $0.083 | Pose, camera side/height, ball position, kit, light all follow the mannequin + brief. Face only partly him: hair, stubble, cheek moles carried over, but slimmer jaw and smaller nose (idealized). |
| r2 `kick-r2.png` | google/gemini-nano-banana-2.1, 2K, face-only EDIT of r1 | kick-r1, face-side, face-front | $0.059 | Layout held pixel-close (pose, kit, ball, grass unchanged). Face now wider jaw, fuller cheeks, broader nose, heavier lids, stubble — clearly closer to the refs. Keeper. |

Open points: head is tilted down so the eyes are half hidden — likeness is judged on jaw/nose/cheeks/hair only. No metric was run; this is eyeball comparison against `refs/face-front.jpg` and `refs/face-side.jpg` (`kick-face-check.jpg`: r1 / r2 / side ref / front ref).
Recipe that worked: Sunburst for composition from the mannequin, then a Nano Banana 2.1 edit pass that changes the face only.
