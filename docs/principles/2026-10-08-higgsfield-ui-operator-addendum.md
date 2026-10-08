# Addendum to ADR-009 — Higgsfield via the gated UI operator (2026-10-08)

**Status:** accepted (human decision in chat, 2026-10-08: "go UI").
**Amends:** SPEC §8 "Gemini-Only Visual (ADR-009)". Does not reverse it.

## Context
ADR-009 (2026-06-28) retired Higgsfield/Seedance from the coded pipeline in favour of Gemini (Nano Banana Pro + Veo). Since then the operator has kept using Higgsfield's web UI for Soul ID characters and the approved Genjutsu dance recipe, without any gate around those clicks. The Higgsfield REST keys in `.env` now return 401, the REST docs do not cover Seedance 2.0 / Soul ID Elements, and the Higgsfield MCP is not connected.

## Decision
1. The coded pipeline (`src/auto_affi/adapters/*_provider.py`) stays as ADR-009 says. No Higgsfield provider is added to `src/`.
2. Higgsfield generation is allowed only through the `higgsfield-operator` skill (UI via Claude in Chrome; MCP when connected).
3. Every such generation passes the same PGA gate as the coded pipeline: `src/auto_affi/ops/gate_cli.py` calls `prompt_audit.audit / record_audit / record_approval / record_bypass / assert_may_generate` unchanged. Approval and bypass are recorded only on the human's explicit word.
4. Verify-before-spend for the UI route is a per-run credit cap (`runs/<run>/credits.json`, fail-closed when absent) checked against the live price read from the Generate button immediately before the click; every committed spend and refund is appended to `runs/<run>/ledger.jsonl`.

## Consequences
- One gate for all routes; the event log stays the source of truth.
- Credit caps are in Higgsfield credits, not USD — they do not feed the USD `BudgetCircuitBreaker`.
- Known limit inherited from `prompt_audit`: event-log approvals are tamper-evident against JSON edits but not cryptographically signed.
- Re-introducing a coded Higgsfield provider requires a new ADR that supersedes ADR-009.
