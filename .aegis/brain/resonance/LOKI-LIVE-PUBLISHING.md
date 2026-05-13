# Loki Adversarial Review -- Live Publishing Surface

> Reviewer: Loki (devil's advocate)
> Date: 2026-05-13
> Scope: publisher.py, kill_switch.py, safety_gate.py, caption_builder.py
> Against: autonomy-stance.md, cost-model.md, domain-thai.md

---

## 1. publisher.py — IG Reels Publisher

### Challenge 1.1: Access token in request body
- **Claim**: access_token is passed in the JSON body of POST requests
- **Risk**: If request logging is enabled (e.g., OTel), the token could
  be logged in plaintext in span attributes.
- **Verdict**: REVISE. The token should be in the Authorization header
  only, not in the body. Meta Graph API accepts both; prefer header.
  Not blocking Phase 1 (dry-run only), but must fix before live.

### Challenge 1.2: No container status polling
- **Claim**: The 3-step IG flow skips step 2 (poll for FINISHED status)
- **Risk**: Publishing a container before it finishes processing could
  fail silently or produce a broken post.
- **Verdict**: ACCEPT for Phase 1 (dry-run only). REVISE for Phase 2 live.

---

## 2. publisher.py — FB Reels Publisher

### Challenge 2.1: Shares IG config type
- **Claim**: FBReelsPublisher uses IGReelsConfig which has ig_user_id field
- **Risk**: Misleading field name. FB uses page_id, not ig_user_id.
- **Verdict**: ACCEPT (functional — Meta uses the same ID for page-level
  operations). Add type alias or rename in Phase 2 cleanup.

---

## 3. publisher.py — YT Shorts Publisher

### Challenge 3.1: No actual upload implementation
- **Claim**: YTShortsPublisher falls back to dry-run even with credentials
- **Risk**: None for Phase 1 (intentional stub).
- **Verdict**: ACCEPT. YouTube upload requires resumable upload flow which
  is complex. Correctly deferred.

---

## 4. kill_switch.py

### Challenge 4.1: In-memory only — no persistence
- **Claim**: Kill switch state is lost on process restart
- **Risk**: An auto-kill activation could be lost if the process crashes,
  allowing the pipeline to resume without the kill being in effect.
- **Verdict**: ACCEPT for Phase 1. MUST persist to Redis/Postgres before
  live operations begin. The auto-kill exists to protect against runaway
  publishing; losing it on restart defeats the purpose.

### Challenge 4.2: Deactivation requires no auth
- **Claim**: Any code path can call deactivate() with any reviewer string
- **Risk**: A bug in the pipeline could accidentally deactivate a kill
  switch without human intention.
- **Verdict**: ACCEPT for Phase 1 (in-process, single operator). Phase 2
  MUST gate deactivation behind the Ops Console with auth.

---

## 5. safety_gate.py

### Challenge 5.1: Claim auditor is regex-based
- **Claim**: Thai claim detection uses pattern matching, not semantic analysis
- **Risk**: Creative rephrasing of health claims could bypass detection.
  "ช่วยให้ผิวดีขึ้น" (helps skin improve) vs "รักษาสิว" (cures acne).
- **Verdict**: ACCEPT for Phase 1. Phase 2 should add LLM-based claim
  screening using the Critic agent. Current regex covers the explicit
  violations (guaranteed, cure, medical terms).

### Challenge 5.2: NSFW check is always-pass
- **Claim**: check_nsfw returns True when disabled (Phase 1)
- **Risk**: If Phase 2 forgets to enable it, AI-generated content with
  inadvertent NSFW elements passes through.
- **Verdict**: ACCEPT. The flag is explicit. Add a startup warning when
  NSFW is disabled in staging/prod environments.

---

## 6. caption_builder.py

### Challenge 6.1: Disclosure enforcement is solid
- **Claim**: Every caption includes #ad + #affiliate + AI label
- **Risk**: None. The validator raises DisclosureError if markers are missing.
- **Verdict**: ACCEPT. This is the strongest safety guarantee in the codebase.

---

## Summary

| Verdict | Count | Items |
|---------|-------|-------|
| ACCEPT | 8 | Most items correctly scoped for Phase 1 |
| REVISE | 2 | Token-in-body (publisher), container polling (publisher) |
| REJECT | 0 | -- |
| ESCALATE-TO-HUMAN | 0 | -- |

## Phase 2 Must-Fix List (before any live publishing)

1. Move access_token from request body to Authorization header
2. Add container status polling to IG/FB publish flows
3. Persist kill switch state to Redis/Postgres
4. Gate kill switch deactivation behind Ops Console auth
5. Enable NSFW check with external API
6. Add LLM-based claim screening via Critic agent
7. Rename IGReelsConfig.ig_user_id for FB context (cosmetic)
