# Pipeline Step Templates — layout · prompt · result (PRE-RUN REVIEW)

> **Status: DRAFT — must be human-approved before the first real run (SPEC §10.5 gate 11,
> Reference-Sheet Lock).** These are the canonical, reusable templates each PGA stage fills in.
> Authoring them up front is what makes "ผลลัพธ์เดิมเสมอ" (deterministic) possible: same approved
> inputs ⇒ same prompt hash ⇒ same locked output. The `cast_sheet` + `objects_sheet` outputs become
> the single visual reference every downstream stage binds to.

## Shared locks (injected into EVERY prompt)

```
IDENTITY  = "JIAP02, a fit lean athletic Southeast Asian male, late 20s, V-line jaw,
             short dark quiff hair with slight widow's peak, light stubble on chin and
             jawline, dark brown eyes, medium tan skin tone, confident relaxed smile"
NEG       = "deformed face, different person, wrong face, blurry face, extra limbs,
             multiple people, bad anatomy, text, watermark"
SOUL_ID   = "soul-jiap02"     SEED = <one locked int for the whole run>
ASPECT    = "9:16"
```
Rule: exactly ONE face reference per gen; NEVER a second conflicting face ref (hula-hoop pitfall #2).
The input frame must contain ONLY the intended subject/product — no stray props (pitfall #8).

---

## STEP 1 — Cast / Character Sheet  (stage `cast_sheet`, image)

**Layout:** 5–6 panel turnaround on a neutral studio bg (front · 3/4 · side · full-body · wardrobe A · wardrobe B).

**Prompt template:**
```
{IDENTITY}. Character reference turnaround sheet: front, three-quarter, side, and
full-body views; wardrobe A ({wardrobe_a}) and wardrobe B ({wardrobe_b}); neutral
grey studio background, even lighting, consistent face across all panels. {NEG}
```
**Result template:** `cast_sheet.png` → registers `identity_string` (verbatim string above) + `soul_id`.
This is locked reference #1; its `prompt_hash` is bound at approval.

---

## STEP 2 — Objects / Props Sheet  (stage `objects_sheet`, image)

**Layout:** hero SKU only — front + in-hand — white bg; a written list "ONLY these objects".

**Prompt template:**
```
Studio product shot of {sku_name} ONLY — a {color} {material} {category}; two views
(front and held in hand); clean white seamless background; no other objects in frame,
no people. {NEG}, stray props, extra products
```
**Result template:** `objects_sheet.png` → registers `declared_objects = [{sku_name}]`.
Locked reference #2. Downstream `scene_objects ⊆ declared_objects` (the PGA stray-object check).

---

## STEP 3 — Storyboard  (stage `storyboard`, image grid)

**Layout:** 3×3 grid, 9:16 cells; hook ≤1.0s; 3–6s/shot; seed + palette panel.

**Prompt template (per shot `image_prompt`):**
```
{IDENTITY}. {scene_and_action}. {shot_type} ({shot_movement}), 9:16, {palette_grade}.
Ad style: {framework e.g. problem->demo->CTA}. {NEG}
```
**Result template:** `AiStoryboard` JSON (`schemas/ai_storyboard.py`) — `shots[]` with
`image_prompt`, `consistency_seed` (= SEED, shared by every shot), `palette_grade`,
`visual_reference_lock` (paths to cast/objects sheets), `negatives`, `narrative_role`,
`duration_s ≤ 6.0`. Hook shot first; HSO×VCS rubric must pass.

---

## STEP 4 — Contact Sheet / Starting Frames  (stage `contact_sheet`, image)

**Layout:** one starting frame per shot, 9:16, with a vision-check caption "same person? ✓".

**Prompt template (per shot `fNN`):**
```
{IDENTITY} starting frame for shot {shot_id}: {scene}. Single face reference, soul-id
{SOUL_ID}, seed {SEED}, 9:16. ONLY {sku_name} present in the frame. {NEG}
```
**Pre-flight (verify-before-spend):** vision-compare each frame vs the cast sheet → "same person"
must be confirmed BEFORE the paid video call.
**Result template:** `fNN.png` per shot + `pre_generation_user_review.json` recording the 3×3 review +
the human approval (SPEC §10.5 gate 9).

---

## STEP 5 — Video  (stage `video`, PAID — Higgsfield Seedance)

**Layout:** 9:16 clip per shot → concat to master.

**Prompt template (per shot):**
```
{IDENTITY}. {action}. Ad style: {framework}. Thai dialogue is VOICE-OVER over B-roll —
the mouth is NOT visibly speaking Thai (no lip-sync). 9:16, {palette_grade}. {NEG}
```
**Result template:** `shotNN.mp4` (720p, ≤8s) → concat + edit (captions, hook punch-in, brand
overlay, CTA endcard) → **master**: cleanroom (exactly 1 video + 1 audio stream), 9:16, ≤60s,
Thai VO 1.0–1.15×, disclosure `#โฆษณา/#affiliate`.

---

## Per-step PGA review panel (what the human sees before approving)

```
STAGE: <stage>                         prompt_hash: <sha256[:8]>
PGA checklist:  A identity-verbatim ✓ · A cast+objects approved ✓ · B single-subject/no-stray ✓
                B 1-face-ref ✓ · B negative-present ✓ · B 9:16 ✓ · B seed/soul-id ✓ · B Thai-no-lipsync ✓
                C no-banned-claims ✓ · C economics-passed ✓
[ approve / go ]   [ bypass <stage> ]      ← no input = NO generation
```

## Honest status
- **Result schemas exist** for storyboard (`AiStoryboard`) and brief (`CampaignBrief`).
- **Prompt templates, layouts, and image-sheet result templates above are NEWLY AUTHORED here** —
  they did not exist as canonical artifacts before. They require human approval before a real run.
- Per-product values (`{sku_name}`, `{wardrobe_*}`, `{scene}`, `{framework}`) are filled from the
  CampaignBrief + product data at run time, then audited + approved per stage.
