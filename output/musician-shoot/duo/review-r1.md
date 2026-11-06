# Duo band poster — round 1 review (2026-11-06)

File: `duo-r1.png` 1152×1536 [VERIFIED: PIL]. Route: OpenRouter `openai/gpt-image-2.5-sunburst`, quality high, 6 input_references (Jiab front, Jiab side, drummer front, operator mannequin snapshot, Jiab keeper H, Crafter product photo). Cost: expected ≈ $0.12; the script's cost lookup returned HTTP 400 and `/credits` still shows 10.797 right after the call (endpoint lags) → **[PRODUCED: cost unverified]**.

| Check | Verdict (my visual read vs refs; operator's judgment is final) |
|---|---|
| Singer likeness (Jiab) | PLAUSIBLE — same man as the keeper set: eyes, nose, lips, stubble, fringe |
| Drummer likeness (new ref) | PLAUSIBLE — middle-parted wavy dark hair, straight brows, ear stud, goatee; face a touch leaner than the selfie; mustache lighter than ref |
| Pose vs mannequin | PASS — singer at mic mid-note strumming, left hand on neck; drummer seated, leaning in, right stick raised, left stick on the pad; amp behind |
| Camera | PARTIAL — two-shot from slightly left and above as blocked, but closer/tighter than the operator snapshot (feet of singer at frame edge) |
| Light | PASS — warm key from camera-left high with falloff on the right side of faces, red-amber rim from behind right on the drummer, overhead spot beam in haze, floor shadows cast toward camera-right, black background |
| Wardrobe / guitar | PASS — suede blouson, white tee, light jeans, wheat boots; sunburst dreadnought with tortoise pickguard, plain headstock; drummer black tee + dark jeans + black sneakers |
| Text / logos | PASS — none |

Round-2 levers if wanted: widen (fov 42 → "wider two-shot, full body with floor room") and darken the drummer's key side for more poster contrast; heavier mustache on the drummer ("thin mustache clearly visible").

# Round 2 (2026-11-06) — camera fix

File: `duo-r2.png` 1152×1536. Refs reordered: IMAGE 1 = operator mannequin snapshot, IMAGE 2 = Jiab face-front, IMAGE 3 = drummer face-front (keeper + guitar photo dropped; wardrobe/guitar by text). Prompt gained a numeric COMPOSITION block (camera 1.7 m high, left, 15° down, 42° fov; singer fills frame height, drummer ≈60 % of his height; mic base bottom-centre; floor = lower 40 %; shadows to lower-left). Cost [VERIFIED from API response]: $0.086 (prompt $0.037 + output $0.049).

| Check | Verdict |
|---|---|
| Camera vs mannequin | PASS — high-left, looking down and across; singer large in the left foreground with boots and floor around them; drummer smaller right-back, head at the singer's chest; mic base bottom-centre; floor fills the lower part. Shadows fall toward lower-right (prompt asked lower-left) — the model kept its own key-light geometry. |
| Singer likeness | PLAUSIBLE — unchanged from round 1 despite the face moving to IMAGE 2 |
| Drummer likeness | PLAUSIBLE — mustache now visible, hair/brows/ear stud match |
| Wardrobe / guitar / pad | PASS — plain headstock, tortoise pickguard, pad on tripod, amp behind |
| Light | PASS — warm key left, red rim right, overhead beam in haze |

Lesson: for camera/composition, put the mannequin FIRST and spell the camera out in numbers; identity still held with faces at IMAGE 2–3 and only 3 refs.

# Round 3 (2026-11-06) — drummer face up

File: `duo-r3.png` 1152×1536. Same recipe as round 2 (mannequin IMAGE 1 = new operator snapshot with the drummer's head lifted, Jiab face IMAGE 2, drummer face IMAGE 3) + prompt: head lifted, face toward camera, lit by the key, relaxed open-mouth grin, not looking at the pad. Cost [VERIFIED from API response]: $0.087.

| Check | Verdict |
|---|---|
| Drummer face | PASS — head up, full face to camera, lit; mustache + goatee + middle-part hair + ear stud all readable; grin as prompted |
| Drummer likeness | PLAUSIBLE — closest of the three rounds; cheeks slightly fuller than the selfie |
| Camera vs mannequin | PASS — same high-left framing as round 2; singer large left, drummer right-back, mic base bottom-centre, floor visible |
| Singer | unchanged, PLAUSIBLE; mouth open on a note |
| Light | PASS — warm key left, red rim right, overhead beam; shadows again fall lower-right |
