# Higgsfield web UI playbook (Claude in Chrome)

Proven tricks from live runs (memory `higgsfield-ui-automation`, 2026-10-07/08). Re-verify anything that looks different — the UI changes.

## Pages
- Video create: `https://higgsfield.ai/ai/video?model=seedance_2_0` (the marketing page `/ai-video` has a "Create Video Now" button that lands here). Tabs: Create Video · Edit Video · Motion Control.
- Left panel: preset card, Elements/attachments, Prompt box, Model row, chips `8s` · `Auto` · `720p`, then **Generate ✦ <list> <price>**.
- The prompt box keeps the LAST session's prompt — clear it and paste the approved prompt; verify with JS `innerText` length.

## Live price
- Run `scripts/read_price.js`. The current price is the last number in the Generate button (`Generate 48 36` → 36; 48 is struck through).
- 2026-10-08: Seedance 2.0 · 8s · Auto · 720p = 36 credits (list 48).
- 2026-10-07 (30 s, Ultra discount): Seedance 2.5 480p 90 / 720p 210 / 1080p 360; Genjutsu 29.5 s ref 480p 87 / 720p 203 / 1080p 319.

## References and Soul ID
- Soul ID in video only via Seedance (Create Video) → "@ Elements" → My Elements → the Element (e.g. @JIAP). Genjutsu / Motion Control / Lite have no Soul slot.
- Real @-mentions: type "@" alone, wait 2 s, keyboard Down×N + Return. Typed "@Image1" stays plain text; mouse clicks on the menu are unreliable.
- Bulk uploads: open the picker, `find` the `input type=file`, `file_upload` paths (≤10 MB per call → PNG→JPG q93). Uploads are not auto-attached; select them (newest first). Verify the count of "Remove media" buttons.
- Video uploads need a VISIBLE tab: `osascript -e 'tell application "Google Chrome" to activate'`, confirm `document.visibilityState=='visible'`, then upload; confirm the trim dialog.

## Prompts
- Long prompts: type as one line; CDP type may time out (~30 s) but the text lands — verify length with JS.
- Create Video rejects edit-style prompts ("copy @Video 1 exactly, replace only…") → Failed · Credits refunded; the reason shows only on hover of the failed card → use the Edit Video tab.

## Waiting and reviewing
- Poll `document.body.innerText.includes('Generating')` in short calls; a long in-page await loop times out CDP (~45 s).
- Review without downloading: clone the result `<video>` src into a body-level fixed `<video id=__rv>`, seek `currentTime`, zoom/screenshot, then remove it.
- Failed cards: hover to read the reason, then record the refund in the ledger.
