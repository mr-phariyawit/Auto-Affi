# Code Review — surviving code (2026-06-08)

> Post-reset, the only Auto-Affi **product** code on disk is under `scripts/`.
> `tools/` is AEGIS framework tooling (out of product scope). `src/auto_affi/` is
> deleted (rebuild pending, recoverable at `5602e53c`). Method: risk-pattern scan +
> structural read (not exhaustive line-by-line on the 1045-LOC scanner).

## scripts/validate_caption_voice_sync.py (102 LOC) — ✅ solid
Compares HyperFrames captions vs an approved voice-segment report; exit 0 ok / 1 mismatch.
Implements compliance **gate 6** (caption/VO sync, SPEC §10.5).
- **[nit]** `CAPTION_RE` parses HTML with regex; a nested `<div>` inside a caption could mis-close on the first `</div>`. Low risk (controlled template).
- Verdict: keep as-is.

## scripts/social_media_scanner.py (1045 LOC) — ✅ low-risk, reasonable
HTTP via **stdlib urllib only** (no `requests`/`subprocess`/`shell=True`/`eval`/`pickle`).
Secrets via `os.getenv` (YOUTUBE/GOOGLE/REDDIT/TIKTOK). `urlopen` has timeouts. Graceful
degradation when keys missing (returns explanatory `summary_th`). Writes named CSVs to `data/`.
- **[medium-nit]** No retry/backoff on `urlopen` — a transient failure aborts that source. (Matches handoff "fix retry" note.)
- **[nit]** `classify()` / `product_mapping()` / `signal_score()` are keyword heuristics — brittle to wording.
- **[ok]** `write_csv` opens `"w"` (overwrite); `append_unique` is read-modify-write — fine for a single-process script.
- No security issues; no critical bugs surfaced in structural review.

## scripts/verify_runs.py (207 LOC, new this session) — ✅ self-review
ffprobe via subprocess **list-args** (no shell), 60s timeout, `try/except` JSON parse.
- **[nit]** `declared_mp4s()` does a nested `os.walk` per referenced file (O(n·m)); fine at this scale.

## tools/ (55 shell/mjs) — not deep-reviewed
AEGIS framework tooling, out of Auto-Affi product scope. No high-risk patterns in spot checks.

## Summary
**0 critical · 0 security · 1 medium-nit (HTTP retry) · 4 nits.** Surviving code is healthy.
The real gap is **test coverage** — `tests/` was deleted; rebuild under Sprint-1 (AFFI-S1-*).
