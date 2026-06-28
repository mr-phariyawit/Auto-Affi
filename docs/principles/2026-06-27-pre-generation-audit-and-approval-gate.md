# Pre-Generation Audit (PGA) + Approval Gate — BINDING

**Status:** Binding for every production run (human directive, 2026-06-27).
**Enforces:** SPEC §10.5 gates 10 (PGA), 11 (Reference-Sheet Lock), 12 (Generation Lock).
**Driver:** Human directive — "audit ต้องเช็คมาตรฐาน prompt ก่อนเจนรูป/วิดีโอเสมอ; ต้องผลลัพธ์เดิมเสมอ
(character/cast/objects sheet, storyboard); human ไม่ approve ห้ามเจน จนกว่ามนุษย์สั่ง bypass."
Backed by the hula-hoop study pitfalls (#1 wrong face, #2 conflicting ref, #8 stray prop) and
the verify-before-spend rule.

---

## The three laws

1. **AUDIT ALWAYS** — no image or video is generated (free OR paid, draft OR final) until its
   prompt + references pass the PGA checklist below. No exception.
2. **DETERMINISTIC / SAME RESULT** — character/cast sheet + objects/props sheet + storyboard are
   the single locked references. Same approved inputs ⇒ same locked prompt (hashed into the run
   manifest). Reference sheets are the consistency anchor; soul-id/seed are locked.
3. **NO GEN WITHOUT APPROVAL** — every gated stage waits for an explicit recorded human approval.
   No approval → WAIT (never generate speculatively). Only a human `bypass <stage>` overrides,
   logged, for that one stage only.

---

## Stage order (each stage is gated)

```
1. Cast / Character Sheet      → PGA → ⛔ approve →  (locked identity reference)
2. Objects / Props Sheet       → PGA → ⛔ approve →  (locked props reference)
3. Storyboard (layout)         → PGA → ⛔ approve →  (locked scene plan)
4. Contact sheet / stills      → PGA → ⛔ approve →  (per-shot starting frames)
5. Video generation (paid)     → PGA + credit check → ⛔ approve → generate
```
A later stage may NOT start until the earlier stage is approved (or explicitly bypassed). Changing
an earlier approved artifact invalidates every downstream approval — re-audit + re-approve.

---

## PGA checklist (run before EVERY generation call)

### A. Reference lock
- [ ] Cast/character sheet exists, is human-approved, and is the single canonical identity reference.
- [ ] Objects/props sheet exists, is human-approved; every required product/prop is listed and ONLY those.
- [ ] The prompt injects the canonical identity string **verbatim** (no paraphrase drift).

### B. Prompt standard
- [ ] Single intended subject; NO stray/unintended objects in the scene (hula-hoop pitfall #8).
- [ ] Exactly ONE face reference (approved starting frame / soul-id). Never a second conflicting
      face reference (`reference_image_2`) — root cause of a wasted-credit batch (pitfall #2).
- [ ] Negative prompt present (deformed face, wrong/different person, extra limbs, multiple people,
      text, watermark, bad anatomy).
- [ ] Aspect 9:16, resolution, and duration are within spec for the target stage.
- [ ] Deterministic anchor set: soul-id / seed locked so cross-shot output is reproducible.
- [ ] Thai no-lipsync respected (§19.3): no visibly-speaking Thai mouth; dialogue is VO over B-roll.

### C. Compliance
- [ ] No banned claims (medical / financial / "guaranteed"); disclosure plan present.
- [ ] Category not in RESTRICTED_CATEGORIES; product passed the Scout economics gate.

### D. Determinism / "same result"
- [ ] Prompt + all reference URIs + seed/soul-id recorded to `runs/<run>/manifest.json` BEFORE gen.
- [ ] Prompt hash computed; identical approved inputs reproduce the identical hash.
- [ ] If ANY input changed since approval → approval is void → re-audit + re-approve.

**Result:** every checkbox must be ✅. Any ✗ → `audit_pass=false` → generation BLOCKED, reported to
human with the failing item. Never "fix silently and proceed".

---

## Approval state — `runs/<run>/approvals.json`

```jsonc
{
  "cast_sheet":     { "audited": true, "audit_pass": true, "approved": true,  "approved_by": "human", "approved_at": "ISO8601", "bypassed": false, "bypass_reason": null, "prompt_hash": "..." },
  "objects_sheet":  { "audited": true, "audit_pass": true, "approved": false, "approved_by": null,     "approved_at": null,       "bypassed": false, "bypass_reason": null, "prompt_hash": "..." },
  "storyboard":     { "audited": false, ... },
  "contact_sheet":  { "audited": false, ... },
  "video":          { "audited": false, ... }
}
```
- A stage generates ONLY if `audit_pass == true AND (approved == true OR bypassed == true)`.
- `bypass` is set ONLY by an explicit human command (`bypass <stage> [reason]`) and is logged to
  `.aegis/brain/logs/activity.log`.

---

## Integrity model (honest threat model)

The gate reads the **append-only `audit_events.jsonl` as its source of truth**, not the mutable
`approvals.json` (which is treated as advisory/forgeable). This applies to the **target stage AND
every prior stage** in the ordering chain — a forged `approvals.json` cannot launder an upstream
stage or leak a banned upstream artifact downstream. Properties (2026-06-28, Audit Lead gap #6 +
H2/H5, hardened across four adversarial BLOCK rounds):

1. **Hard-compliance is sticky and un-launderable.** When an audit records `banned_claims`,
   `category_restricted`, or `economics_not_passed`, a `hard_block` latch is written to the log.
   It cannot be cleared by `approve`, by `bypass`, OR by a clean **same-hash re-audit** (the
   compliance flags are not in the prompt hash, so re-auditing the same artifact "clean" does
   NOT lift the latch). The latch only resets when the prompt hash changes — a genuinely
   different artifact, which records a fresh audit event. `assert_may_generate` reads the
   latest audit event from the log, so editing `approvals.json` cannot launder it.

2. **Approvals AND bypasses are tamper-EVIDENT against JSON edits and stale-event replay.** A
   clearance is honoured only if its event (`approve` bound to the exact `prompt_hash`, or
   `bypass`) **post-dates the latest audit event** for that stage in the append-only log. This
   rejects (a) the JSON-only forge (`approved=true`/`bypassed=true` with no event) and (b)
   reverting `approvals.json` to a previously-cleared state to replay an old event (a newer
   audit event now sits after it). A `bypass` is additionally bound to one artifact: when a
   manifest is supplied, its hash must equal the hash recorded at bypass time — a bypass trusts
   ONE hand-made artifact, not any content.

   **Honest limits (still NOT cryptographic):** a local actor who can write the run directory
   can still *append a forged `approve`/`audit` event* to the log — append-only does not stop
   appends. And `approved_by` / `approval_token` are self-asserted, not verified identities.
   True integrity requires signed events or an external approval channel that issues verifiable
   tokens. Claim "tamper-evident against JSON edits and stale replay", NOT "human-verified" or
   "tamper-proof".

## Live-path bypass requires a preceding audit (intentional, fails closed)

On the LIVE (paid) path the adapter requires a manifest, and the gate binds it to the
hash recorded for the stage. A `bypass <stage>` records the hash from the stage's prior
audit — so to bypass a stage AND generate live, an audit of that exact artifact must run
first (it seeds the bound hash). A pure no-audit bypass leaves the bound hash empty and can
never satisfy a live call's hash check — it **fails closed** (over-blocks, never over-spends).
This is intentional: a live bypass still binds to ONE specific artifact, not "any content".
Dry-run bypass is unaffected (no manifest required there).

## Agent operating procedure (until a code gate lands)

The pipeline is partly agent-driven, so the agent IS the enforcement point:
1. Author the stage artifact (sheet / storyboard / prompt).
2. Run the PGA checklist out loud; write the result + prompt_hash to `approvals.json`.
3. If audit fails → stop, report the failing item, do NOT generate.
4. If audit passes → present the artifact + exact prompt to the human and WAIT.
5. Generate only after the human approves (or explicitly bypasses that stage).
6. Follow-up engineering task: codify PGA as `pipeline/prompt_audit.py` + `approvals.json` writer so
   the gate is machine-enforced, not just procedural.
