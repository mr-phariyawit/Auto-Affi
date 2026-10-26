# External techniques (not from the Bible)

Source: KEMLIFE free prompt pack "Prompt จัดโครงสร้าง Prompt วิดีโอ AI" (Notion, read 2026-10-27; full study in `docs/reference/kemlife-seedance-story-ad-study-2026-10-27.md` at the repo root).
It is a 2-minute story ad: 3 Nano Banana Pro character sheets → 4 × 30 s Seedance 2.5 clips (9:16, 480p, audio on).

Status: **written into a prompt pack, not tested by us.** That is why every rule here is `warn` and has an X id or an `[EXT.*]` cite, kept apart from the Bible-audited R rules. Promote a rule to the Bible only after a generation shows it works (log it in `higgsfield-recipe-ledger`).

| Cite | Technique | Linter |
|---|---|---|
| [EXT.KEMLIFE.STYLE-LOCK] | A film made from several clips repeats one STYLE block word-for-word in every clip (camera, lens, focal length, aperture, grade, grain, handheld, aspect, "NO TEXT ON SCREEN"). Clips cut together like one film. | R22 now also checks `STYLE:` |
| [EXT.KEMLIFE.NEGATIVE-REF] | When a person who is not a reference appears (another child, a customer), say so and name the look-alike reference: "a different child, NOT @image3". Otherwise the model pastes the reference face onto the extra. | X01 |
| [EXT.KEMLIFE.WARDROBE-SWITCH] | Change of outfit inside one clip is tied to a time: "from 0:22 onward wearing outfit B from his sheet". Outfit B must be on the same character sheet. | X02 |
| [EXT.KEMLIFE.DIALOGUE-DELIVERY] | Every spoken line carries its delivery before the quote: `X says (furious, voice cracking): "…"`. | X03 |
| [EXT.KEMLIFE.PRODUCT-LOCK] | The product gets its own PRODUCT block: @tag, a one-line description, "Keep cover design exact." Seed it early (half-hidden), reveal it late. | X04 |

## Clip skeleton (S5 in skeletons.md)

`FORMAT` (length / cut count / genre + emotional arc / language) → `STYLE` (locked) → `SUBJECT n` (one-line look + @tag, repeated in every clip) → `ENVIRONMENT` → `PRODUCT` (only in clips that show it) → `AUDIO` → `TIMELINE` (3–5 s beats, shot size + action + dialogue).

## Auto-Affi notes

- They write the dialogue in Korean, so no Thai mouth movement is needed. Our rule (Thai = VO over B-roll, no visible Thai lip-sync) still applies. X03 also covers VO lines.
- 480p is their choice for 30 s clips. `model-limits.md` records only 720p for 2.5, so the linter warns (M01) on 480p until we see it in the UI.
