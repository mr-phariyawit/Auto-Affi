# Running a retouch pass on Higgsfield with Claude in Chrome

Learned on 2026-10-06/07 across R1–R15 and the Soul-ID work. Everything here was observed in the live UI.

## Steps

1. Open `https://higgsfield.ai/ai/image?model=gpt-image-2-5-sunburst`. Check that the model reads GPT Image 2.5 Sunburst, then set aspect 3:4, quality High, 2K and count 1.
2. **Attach references.** Open the image picker, `find` the `input type=file`, then upload with `file_upload` and a list of paths. Keep each call under 10 MB; convert PNG to JPG at quality 93 if needed. Uploads are not attached automatically, so select them in the Uploads tab, newest first.
   - For pass 2 and 3 the reference is the previous result. Select it from the Generations tab instead of uploading.
3. **Check the reference order.** Zoom on the attached thumbnails. IMAGE 1 is the first thumbnail shown, and that follows the selection order. If it doesn't match the prompt, fix the prompt text or remove and re-add the references in the right order. Remove buttons work only when found with `find` and clicked by ref; clicking by coordinate is unreliable.
4. **Enter the prompt** as one line. Typing a long prompt may time out after about 30 s, but the text still arrives. Verify the full text with `get_page_text` or by reading the editor's innerText, then compare its length with the source.
5. Read the price on the Generate button and show the audit (see SKILL.md "Gate"). Click Generate only after the go.
6. **Find the result.** The newest tile is at the top left of the gallery. Open it to read its size and created time, then capture a screencrop and a face zoom with `save_to_disk`.

## Known traps

- Switching model or navigating away clears the attached references on the image page. Attach them last, just before typing.
- The Uploads grid re-sorts after every upload, so re-read tile positions instead of reusing old coordinates.
- `.click()` from JavaScript is ignored on Download. A real click by ref works, but downloading originals needs the operator's permission. Chrome may also block multiple automatic downloads; the operator allows higgsfield.ai in site settings.
- If Claude in Chrome disconnects, `list_connected_browsers` comes back empty. Ask the operator to open the Claude side panel in Chrome. Meanwhile, a page can be read by opening its URL in Chrome from the shell and taking a read-only screenshot with computer use.

## Learned on the first live skill run (R16–R18, 2026-10-07)

- **Uploading into the reference slot replaces what you selected.** The second upload through the slot's file input took the place of the identity photo already selected, so the order became style → identity. Upload every file first, then select them in the grid in IMAGE order. Otherwise, use the swapped-role prompt and zoom on the thumbnails to confirm.
- **Pass 2 and 3 inputs:** open the result in the viewer and click **Reference** in the side panel. The result is added after the existing references. Remove the older ones with the remove buttons found by `find` (hover the thumbnail first if they are not listed).
- **Aspect menu:** one click on "3:4" can leave the menu open and set a neighbouring value (it once set 8:9). Typing while the menu is open goes nowhere. After choosing, zoom on the bar, confirm it reads 3:4, then click into the prompt box before typing.
- Each Sunburst image took about 60 s. "Generating" disappears from the page text when it is done, and the new result is the top-left tile.

## Downloading originals (2026-10-07, after the operator's `โหลด`)

- Go to `https://higgsfield.ai/asset/all` (newest first, grouped Today / Yesterday / dates). Open a tile, confirm the prompt start, size and Created time in the side panel against the run log, then `find` "Download button in viewer side panel" and click it by ref. One file per click; no Chrome block was hit for three files.
- The file lands in `~/Downloads` as `hf_<UTC yyyymmdd_hhmmss>_<asset-id>.png`. The asset id is also in the viewer URL (`/asset/all/<asset-id>`), so match by id, not by time. The timestamp is UTC (R14 at 11:11 PM local = `161115`).
- The viewer's image URL is a signed `images.higgs.ai/?…` link; reading it from JS is blocked, so use the Download button.

## Learned on v12 angles (R30/R31, 2026-10-08)

- **Two empty slots, one file each, kept the order.** With the old references removed, the bar showed two empty slots, each with its own `input type=file`. Uploading the hero into slot 1 and then the style image into slot 2 gave IMAGE 1 = hero and IMAGE 2 = style. This differs from R16, where the upload went into an already-filled slot and replaced its image.
- **Picker selection order = IMAGE order.** It held again for R30: picking style first, then hero, gave IMAGE 1 = style. The Uploads grid re-sorts after each upload and greys the hovered tile, so zoom on the attached thumbnails before typing.
- **The ✕ on an attached thumbnail is not in the accessibility tree.** Find it with JS (24×24 buttons on the thumbnail's top-right corner), then click those coordinates.
- **Hash check of the typed prompt:** compute SHA-256 of the editor's innerText in page JS and compare it with the hash of `prompt.txt`, returning only a boolean. Returning the hex digest is blocked by the tool as "Base64 data".
