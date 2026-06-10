---
name: aegis-chronicle
description: "Project Chronicle — consolidate ALL activity from the first commit to now into a successes / failures / lessons ledger (project-WIDE, not session-scoped). Use for onboarding, post-mortems, pivot reviews, or 'what have we learned overall'."
profile: standard
triggers:
  en: ["chronicle", "consolidate all activities", "project history from zero", "lessons from the whole project", "successes and failures overall", "full retrospective from the start", "what have we learned so far", "post-mortem the whole project"]
  th: ["รวบรวม activities ทั้งหมด", "ประวัติโปรเจกต์ตั้งแต่เริ่ม", "บทเรียนทั้งโปรเจกต์", "ความสำเร็จและความผิดพลาดทั้งหมด", "สรุปทั้งโปรเจกต์ตั้งแต่ 0", "เรียนรู้อะไรบ้างตั้งแต่ต้น", "ทำ post-mortem ทั้งโปรเจกต์"]
reads:
  - .git (full history — git log --reverse from first commit)
  - .aegis/brain/learnings/
  - .aegis/brain/retrospectives/
  - .aegis/brain/handoffs/
  - .aegis/brain/logs/activity.log
  - runs/
  - docs/
  - "SPEC.md / SUPER_SPEC.md (As-Built / HONEST-STATUS sections)"
  - handoff.md
writes:
  - .aegis/brain/learnings/YYYY-MM-DD_project-chronicle.md
  - .aegis/brain/retrospectives/YYYY-MM/DD/project-chronicle.md
  - .aegis/brain/logs/activity.log (CHRONICLE entry)
wires: []
tests: []
supersedes: []
---

## Quick Reference
Project-WIDE chronicle — the long-arc counterpart to `/aegis-retro` (which is session-scoped).
Walks the **entire git history from the first commit**, plus uncommitted activity streams
(`runs/`, `docs/`, brain, task lists), and consolidates everything into ONE ledger of:
- 📅 **Timeline** — phases of work, in order
- ✅ **Successes** — what worked
- ❌ **Failures / mistakes** — what broke, what was wasted
- 📘 **Lessons** — generalizable, actionable takeaways
- 🔁 **Anti-patterns** — recurring traps to stop repeating

**Honesty contract (load-bearing):** every claim is tagged `[VERIFIED: <command>]` (a command/
evidence proved it) or `[REPORTED]` / `[PRODUCED]` (an artifact exists but was not proven).
Never present a reported count ("100% done", "N tests pass", "shipped") as verified.

**Main agent only** (Captain America / Opus). A subagent asked to run this should refuse and defer.

## When to use this vs `/aegis-retro`
| | `/aegis-retro` | `/aegis-chronicle` (this) |
|---|---|---|
| Scope | THIS session (since SESSION_START) | commit #1 → now (whole project) |
| Trigger | end of a working session | onboarding, post-mortem, pivot review, "what have we learned overall" |
| Output | session diary + friction + lessons | consolidated multi-phase ledger + anti-patterns + skill recommendations |
| Cadence | every session | every sprint-close, every pivot, or on demand |

## Full Instructions

### Step 1 — Gather the committed activity spine
- `git rev-list --count HEAD` → total commits.
- First + last: `git log --reverse --pretty=format:'%ad %h %s' --date=short | head -1` and `git log -1 ...`.
- Full chronological list: `git log --reverse --pretty=format:'%ad %h %s' --date=short`.
- **Group commits into PHASES** by theme/date cluster (e.g. "spec & research", "sprint 1–6", "creative pipeline", "hard-reset"). Name each phase.
- For files that were consolidated/deleted, recover originals: `git rev-list --all --objects | grep <file>` → `git cat-file -p <blob>`.

### Step 2 — Gather uncommitted / gitignored activity (do NOT skip)
- `runs/` — each folder is a real production attempt: read `README.md`, `approval_packet.json`, manifests, voice scripts. Capture what was produced and whether it was VERIFIED (e.g. cleanroom/ffprobe) vs just produced.
- `docs/research/`, `docs/principles/` — research + decisions made outside commits.
- `.aegis/brain/{learnings,retrospectives,handoffs}/`, the harness task list.
- 🔴 **Flag any significant work that lives OUTSIDE version control** — that absence is itself a finding (you cannot audit or recover what was never committed).

### Step 3 — Mine the honest-status sources
- SPEC / SUPER_SPEC "As-Built" / "HONEST STATUS" sections; `handoff.md` "Open Gates"; risk registers.
- Separate **claimed-done** from **actually-verified**. Reconcile spec-vs-reality drift.

### Step 4 — Classify into the ledger
For every activity tag ✅ / ❌ / 📘 / 🔁. Apply the honesty contract from Quick Reference.
- A "success" requires evidence it produced a VERIFIED outcome — not just that code was written.
- Money/clicks/users/posts = outcome KPIs; pt/tests/"% complete" = velocity metrics (vanity unless tied to an outcome).

### Step 5 — Write the consolidated chronicle
Write to `.aegis/brain/learnings/YYYY-MM-DD_project-chronicle.md` with frontmatter
(`date`, `category: chronicle`, `confidence`) and sections: **Timeline / Successes / Failures /
Lessons / Anti-patterns / Current state / Open gates**. Mirror a full copy to
`.aegis/brain/retrospectives/YYYY-MM/DD/project-chronicle.md`. Append to `activity.log`:
`[ts] CHRONICLE | commits=N | phases=N | successes=N | failures=N | lessons=N`.

### Step 6 — Recommend next skills (map lessons → preventive skills)
For each recurring failure, name the AEGIS skill that prevents recurrence, e.g.:
- outcome-zero / "100% but nothing shipped" → `aegis-coverage-screen` + `aegis-return-format` (verified-vs-produced) + a real outcome KPI in the roadmap.
- vendor/direction thrash → an ADR + `aegis-decisions` (decision-audit) before any stack swap.
- work outside VCS → commit run manifests; `aegis-handoff` at every pause.
Output a short "use these next" block.

### Step 7 — Show summary, then follow the command chain (MBP / Golden Rule #7)
Show a condensed box (phases, #✅, #❌, #📘, top anti-pattern, file path). Do NOT pause to ask
"what next?" — follow `.claude/references/command-chain.md`. Stop only for the 4 MBP escalation
categories (Identity / Irreversible scope / External access / Explicit approval gate).
