# Execution routes — why UI, and what it must respect (2026-10-08)

| Route | Status 2026-10-08 | Evidence |
|---|---|---|
| UI via Claude in Chrome | **Default.** Logged in, create page reachable, live price readable without clicking | read `Generate 48 36` on Seedance 2.0 · 8s · 720p |
| MCP `https://mcp.higgsfield.ai/mcp` | Not connected: config URL lacks `/mcp` (ENDPOINT_NOT_FOUND). User fixes via `/mcp` + OAuth | session MCP notice; course A07 L03 shows `/mcp` |
| REST `platform.higgsfield.ai` | Unusable: project `HF_API_ID/SECRET` → 401 Invalid credentials (free status probe); docs list no Seedance 2.0 / Soul ID Elements | `higgsfield_api.py status <dummy>` → 401 |

## Decision (human, 2026-10-08: "go UI")
- SPEC §8 / ADR-009 keeps the coded pipeline Gemini/Veo (+ Kling via kie.ai). Higgsfield stays out of `src/` providers.
- Higgsfield generation is allowed only through this operator, behind the same PGA gate (`prompt_audit`) via `gate_cli`, with a per-run credit cap (`credits.json`, fail-closed) and a spend ledger (`ledger.jsonl`). Addendum: `docs/principles/2026-10-08-higgsfield-ui-operator-addendum.md`.

## Known gate limits (from the code)
- `approvals.json` is advisory; the event log `audit_events.jsonl` is authoritative, but appending a forged approve event still passes (no signing) — `prompt_audit.py` notes this. The operator must never write approve/bypass events without the human's words in chat.
- `ALLOWED_ASPECT = "9:16"` — other aspects fail the audit by design.
