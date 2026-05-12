# Project Plan — Auto-Affi

> Lightweight plan ตาม ISO/IEC 29110 Basic (guideline-mode). **Live tracking ทั้งหมดอยู่ใน Linear** ภายใต้ aegis-team — ไฟล์นี้ track แค่ baseline + decision frame

- **Project Manager**: Nick Fury (aegis-team)
- **Compliance mode**: Guideline only (not audit-ready)
- **Tracking tool**: Linear (aegis-team workspace)
- **Last updated**: 2026-05-12

---

## 1. Project Identity
- **Name**: Auto-Affi
- **Goal**: Autonomous AI marketing platform — Shopee affiliate (TH) end-to-end
- **Vision**: ดู `SPEC.md` §1
- **300% target**: ดู `docs/execution-playbook.md` §7

## 2. Scope Reference
- Functional / non-functional scope → `docs/si/srs.md`
- Out-of-scope items → `docs/pm/sow.md` §Exclusions

## 3. Schedule (high-level baseline)

| Phase | Window | Exit Criteria |
|---|---|---|
| **Phase 0** — PM setup | Week 0 (now) | Linear board ready, Tier 1 docs merged, repo skeleton |
| **Phase 1** — Single closed loop | Week 1-6 | Beauty niche × 5 video/วัน × loop ครบ × GMV ≥ $200/14d |
| **Phase 2** — Multi-platform + portfolio | Week 7-14 | FB+IG+YT, 10 burner accounts, Writers' Room ครบ |
| **Phase 3** — Self-improving autonomous | Week 15-24 | Harness-evolver online, MoM CTR uplift ≥ 5% |

**Linear**: milestone ละ 1 cycle, story-level breakdown ภายใน

## 4. Roles & Responsibilities
ดูฉบับเต็มใน `docs/pm/stakeholder-register.md`

| Role | Person | Scope |
|---|---|---|
| Project Manager | Nick Fury | Plan, Linear, escalation, status |
| Tech Lead | TBD | Architecture decisions, code review |
| AI / Prompt Eng | TBD | Agent prompts, eval, wiki curation |
| Video Pipeline Eng | TBD | Editor + Hyperframe + ffmpeg + ASR |
| Ops / Safety | TBD | Publishing accounts, compliance, kill switches |

## 5. Budget Frame (Phase 1)
| Item | Allocation |
|---|---|
| LLM (Claude) | $500 / month |
| kie.ai (Veo/Sora/Flux/Suno) | $400 / month |
| ElevenLabs TTS | $99 / month (Creator) |
| Infra (Postgres + Redis + Temporal + S3) | $200 / month |
| Self-host GPU (Whisper / Typhoon) | $300 / month |
| Tooling (Langfuse + Linear seats + Sentry) | $150 / month |
| Contingency (10%) | $165 |
| **Phase 1 monthly total** | **≈ $1,800** |

Hard cap: throttle ที่ 80%, kill ที่ 110% (ตาม `docs/llm-allocation.md` §10)

## 6. Communication Plan
- **Linear** = single source of truth สำหรับ task / bug / CR
- **GitHub** = code + spec docs + PR review
- **Standup** = daily async ใน Linear update; weekly sync 30 min
- **Status report** = weekly markdown ใน `docs/pm/status-reports/` (Tier 2 — เริ่มสัปดาห์ 1)
- **Escalation** = ping Nick Fury direct → decision ใน 24 ชม.

## 7. Version Control Plan
- **Branch model**: trunk-based
  - `main` = protected, deploy-ready
  - `claude/<feature-slug>` = AI/co-dev branches
  - `feat/<slug>` = human branches
- **Commit format**: Conventional Commits (`docs:`, `feat:`, `fix:`, `chore:`)
- **PR rules**: review required (≥1), squash merge default
- **Tagging**: `v0.X.Y` semver, tag on Phase exit
- **รายละเอียดเพิ่ม** → `docs/si/scm-plan.md` (Tier 2)

## 8. Risk Management
- Register → `docs/pm/risk-register.md`
- Review cadence: weekly ใน status report
- Top risks ที่ทำให้ project fail (จาก register): platform ban, cost runaway, wiki rot

## 9. Quality Plan
- Test plan → `docs/si/test-plan.md`
- Coding standards → `docs/si/coding-standards.md`
- Prompt standards → `docs/si/prompt-standards.md`
- Eval harness: Langfuse + OpenLLMetry + Phoenix (ดู `execution-playbook.md` §6)

## 10. Backup / Continuity
- GitHub remote = primary
- Linear cloud-hosted = primary  
- Postgres / S3: daily snapshot, 30-day retention
- Wiki vector store: weekly dump → S3

## 11. Closure
- Phase exit review = 30-min retro + closure record ใน `docs/pm/closure-reports/`
- Lessons learned → feed กลับ Wiki canonical + adjust Project Plan
