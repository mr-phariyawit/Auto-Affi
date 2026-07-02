# HANDOFF — 2026-07-02 (late) — Auto-Affi: codebase hardening + Lock Sheet standard

## STATE: ✅ green. 6 commits this session on `feat/pga-stage-kind` (UNPUSHED, no PR yet).
- Tests **340 passed**, ruff clean, mypy clean (38 files). Working tree clean outside `.aegis/brain`.
- Prior state (glam ad shipped, GOLD-STANDARD locked) unchanged — see `2026-07-02-glam-ad-handoff.md`.

## What shipped this session (all VERIFIED)
1. **[SECURITY] PGA gate GAP-1 hash-laundering closed** (`159164d1`). `assert_may_generate` bound the
   generated manifest to the forgeable `approvals.json` hash; `record_approval`/`record_bypass` laundered
   it into the append-only log. Fix: new `_audit_hash_in_log()` — the binding hash now comes ONLY from the
   audit event in `audit_events.jsonl`, never the JSON. +2 forge tests (proven failing before the fix).
2. **Disclosure regex + dead code** (`d9237951`). `has_disclosure()` matched bare `"ad"` as a substring
   (“made”, “gadget”, “ready” all passed) → word-bounded it. Removed the dead `balance_fn` branch from the
   spend gate (dead post-ADR-009). +tests.
3. **Coverage** (`51662a5a`): StagePlan unknown-stage guard → `produce.py` 100%.
4. **11 safe refactors** (`4bcc557d`) via a find→adversarial-verify workflow — dead code, DRY
   (`_fftools.require_binary`, `_read_jsonl`, `_shot_dialogue`, `_name_bucket`), simplifications,
   shared test fixtures → `tests/unit/conftest.py`. Net −91 LOC, all behaviour-preserving.
5. **[NEW STANDARD] Unified LOCK SHEET** (`27e3678d` + `13a30f6e`). Single-page production bible that
   replaces the 3 separate artifacts (cast_sheet + objects_sheet + storyboard). Modelled on the NOVA sheet
   + AetherFlow storyboard columns, wired to our real pipeline, + 3 Auto-Affi-only panels (Economics/Scout,
   PGA Gate Status, Compliance & Cost).
   - Template: `docs/templates/lock-sheet-template.html` · Standard: `docs/reference/lock-sheet-layout.md`
   - Wireframe preview + **fully-populated example** (real umbrella-335 assets): `docs/reference/lock-sheet-*.png`
   - Working filled file: `runs/2026-06-30-umbrella-335/lock-sheet.html` (run dir git-ignored).
   - Skill `produce-affiliate-video.md` Step 4.5 now assembles the Lock Sheet as the review artifact.

## READY FOR A NEW PRODUCT — intake contract (produce-affiliate-video Step 0)
Hand over in ONE message, then a run dir `runs/<YYYY-MM-DD>-<slug>/` is created:
- **Required:** product image(s) · name (TH) · price ฿ · **commission %** · category
  (beauty/gadget/home/mom_baby/fashion/food) · affiliate link.
- **Helpful:** shop rating ★ + sales · 2–4 selling points (TH) · persona · do/don’t-say constraints.
- 🔒 **Never paste API keys in chat** — `GEMINI_API_KEY` + `KIE_API_KEY` already in `.env` (git-ignored). Rotate the ones pasted earlier.

Then the flow is: Scout economics gate → brief → CREATIVE_TREATMENT → **LOCK SHEET** (cast+product refs →
approve as a SET) → storyboard on the sheet → approve → Veo (i2v 4s / refImg 8s) → kie ElevenLabs VO
(STT-verify each line) → kie Suno BGM → HyperFrames compose (comp ≥ VO) → cleanroom → master → Desktop/Drive.
Follow `docs/reference/gold-standard-ad-recipe.md` verbatim; use the Lock Sheet as the gate review page.
Cast can be reused: JIAP presenter “Ton” + female rain model (`02-cast/cast_sheet_*.png`).

## OPEN (external / human-only — in `.aegis/brain/human-queue.md`)
- **G1 Shopee affiliate link** — blocks live publishing + real subId click. (pending)
- **G2 Meta/IG Creator + 60-day Graph token** — blocks IG Reel publishing. (pending)
- ⚠️ **G3 (Higgsfield) is STALE** — ADR-009 retired Higgsfield; the stack is Gemini/Veo + kie.ai. This
  queue item should be marked superseded (do NOT sign up for Higgsfield).
- Gemini spend cap: watch ai.studio/spend (hit once 2026-06-30, cleared).

## RECOMMENDED FIRST ACTION next session
- If a new product is provided → run `produce-affiliate-video` from Step 0 (Lock Sheet is now the review artifact).
- Else → `git push` + open a PR for the 6 `feat/pga-stage-kind` commits (not yet done); and mark G3 superseded.
