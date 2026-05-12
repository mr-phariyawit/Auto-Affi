# ISO/IEC 29110 Gap Analysis — Auto-Affi

Audit เอกสารปัจจุบันเทียบ **ISO/IEC 29110 Basic Profile** (Very Small Entity — VSE) เพื่อหา gap ก่อน entry สู่ production engineering

- **Standard**: ISO/IEC TR 29110-5-1-2:2011 (Basic VSE Profile Management & Engineering Guide)
- **Target Profile**: **Basic** (เหมาะกับทีม ≤ 25 คน, project เดี่ยว)
- **Last updated**: 2026-05-12

---

## 1. ISO 29110 Basic Profile — 2 Processes

1. **Project Management (PM)** — 4 activities: PM Planning, PM Execution, PM Assessment & Control, PM Closure
2. **Software Implementation (SI)** — 6 activities: SI Initiation, Requirements Analysis, Architectural & Detailed Design, Construction, Integration & Tests, Product Delivery

แต่ละ activity ต้องมี **Work Products** ที่ระบุไว้ในมาตรฐาน

---

## 2. Inventory ปัจจุบัน — สิ่งที่เรามี

| ไฟล์ | ครอบคลุม | คล้าย Work Product ของ 29110 |
|---|---|---|
| `SPEC.md` | architecture, agent crew, data model, tech stack, phased roadmap, risks, cost, glossary, sample prompts | Software Requirements (บางส่วน) + Software Design (บางส่วน) |
| `docs/llm-allocation.md` | per-agent model + caching + thinking budgets + eval/promotion | Software Design (Detailed) |
| `docs/thai-genai-stack.md` | gen-AI stack TH + kie.ai/phaya.io adapter + Thai quality gates | Software Design (Detailed) + partial Configuration |
| `docs/execution-playbook.md` | strategic wedge, build sequence, anti-patterns, KPI 300%, risk-mitigation, decision log | Project Plan (บางส่วน) + Risk List (บางส่วน) + Acceptance Criteria (บางส่วน) |

**ครอบคลุมประมาณ 40%** ของ work products ที่ 29110 Basic ต้องการ — แต่กระจัดกระจาย ไม่แยกเอกสารชัด

---

## 3. Gap Analysis — Project Management Process

| Work Product (ISO 29110) | สถานะ | ไฟล์ที่ partial | Gap |
|---|---|---|---|
| **Project Plan** | 🟡 Partial | `execution-playbook.md` มี phase + sequence | ยังขาด: schedule รายสัปดาห์, resource/role assignment, budget breakdown, communication plan, version control plan |
| **Statement of Work (SOW)** | 🔴 Missing | — | ต้องมี: scope agreement, deliverables list, acceptance criteria ระดับ contract, assumptions, exclusions |
| **Project Repository Structure** | 🟡 Partial | git repo มี | ขาด: convention doc (branch naming, commit format, folder structure spec) |
| **Risk Register** | 🟡 Partial | `SPEC.md` §14 + `execution-playbook.md` §9 มี risk แต่เป็นตาราง descriptive | ต้องมี: formal register พร้อม Risk ID, owner, probability, impact, exposure score, mitigation, contingency, review date, status |
| **Progress Status Record** | 🔴 Missing | — | ต้องมี: template + cadence (weekly status report format) |
| **Change Request (CR) Log + Procedure** | 🔴 Missing | — | ต้องมี: CR template, approval workflow, traceability ID |
| **Meeting Records / Minutes** | 🔴 Missing | — | ต้องมี: template + storage location |
| **Acceptance Record** | 🔴 Missing | — | ต้องมี: per-milestone sign-off record |
| **Correction Register** | 🔴 Missing | — | ต้องมี: track defects + action items + verification |
| **Verification Results (PM)** | 🔴 Missing | — | review records ของ Project Plan ฯลฯ |
| **Validation Results (PM)** | 🔴 Missing | — | stakeholder validation ของ delivered output |
| **Project Repository Backup** | 🔴 Missing | — | backup procedure + cadence + location |
| **Stakeholder Register / RACI** | 🔴 Missing | — | who is responsible/accountable/consulted/informed ในแต่ละ deliverable |
| **Closure Report** (end of phase) | 🔴 Missing | — | template สำหรับ end-of-phase retrospective + lessons learned |

**Gap PM = 11 missing + 3 partial = ใหญ่**

---

## 4. Gap Analysis — Software Implementation Process

| Work Product (ISO 29110) | สถานะ | ไฟล์ที่ partial | Gap |
|---|---|---|---|
| **Software Requirements Specification (SRS)** | 🟡 Partial | `SPEC.md` §1-2 มี vision, functional outline | ต้องแยกเอกสาร: functional + non-functional requirements (พร้อม ID), use cases, user stories, interface requirements, ratification record |
| **Software Design Description (SDD) — Architecture** | 🟢 Good | `SPEC.md` §2-3 + diagram | OK; แต่ควรเพิ่ม: deployment view, component-connector view, decision rationale |
| **Software Design Description (SDD) — Detailed Design** | 🟡 Partial | `SPEC.md` §6 (data model) + `llm-allocation.md` + `thai-genai-stack.md` | ขาด: interface contract (API spec ละเอียด), per-component algorithms, error handling design, security design ระดับ component |
| **Traceability Record / Matrix** | 🔴 Missing | — | ต้องมี: Requirement ↔ Design ↔ Code ↔ Test mapping |
| **Test Plan** | 🔴 Missing | — | ต้องมี: test strategy, test environments, entry/exit criteria, test data approach |
| **Test Cases & Test Procedures** | 🔴 Missing | — | ต้องมี: per-feature test cases (incl. agent eval, Thai quality gate, end-to-end loop), procedure steps |
| **Test Report** | 🔴 Missing | — | template + actual results storage |
| **Software Configuration** (baselines + version control plan) | 🟡 Partial | git ใช้อยู่ | ขาด: formal SCM plan, baseline definition, release tagging convention |
| **Software User Documentation** | 🔴 Missing | — | ops console user manual, supervisor playbook |
| **Software Operation Guide / Maintenance Documentation** | 🔴 Missing | — | runbook, troubleshooting, on-call procedures, deployment guide |
| **Software Components** (source) | 🔴 Not started | — | (จะมีเมื่อเริ่มเขียนโค้ด) |
| **Coding Standards / Style Guide** | 🔴 Missing | — | Python style (Black/Ruff config), prompt versioning standard, schema convention |
| **Peer Review Records (Code/Design)** | 🔴 Missing | — | review checklist + storage |
| **Verification Results (SI)** | 🔴 Missing | — | per-task review evidence |
| **Validation Results (SI)** | 🔴 Missing | — | stakeholder demo / sign-off |
| **Software Configuration Items (SCI) list** | 🔴 Missing | — | what gets versioned: code, prompts, schemas, configs, wiki snapshots |
| **Product Operation Guide** | 🔴 Missing | — | end-user (internal ops team) instructions |

**Gap SI = 13 missing + 3 partial = ใหญ่มาก**

---

## 5. สรุป Gap (รวม)

| Category | 🟢 Good | 🟡 Partial | 🔴 Missing |
|---|---|---|---|
| Project Management (14 items) | 0 | 3 | 11 |
| Software Implementation (16 items) | 1 | 3 | 12 |
| **รวม 30 items** | **1** | **6** | **23** |

**Coverage**: ~ **23% ระดับ ISO 29110 Basic** (เอกสารปัจจุบันคุณภาพดีแต่กระจัดกระจาย + ขาด PM artifacts ที่เป็น discipline)

---

## 6. Priority Order — เติมอะไรก่อน

แบ่งเป็น 3 tier ตาม **return on effort**

### Tier 1 — ต้องทำก่อนเริ่มเขียนโค้ด (Phase 1 prep, 1 สัปดาห์)
1. **Project Plan (formal)** — schedule รายสัปดาห์, role/RACI, budget breakdown, communication plan, version control plan
2. **Statement of Work (SOW)** — scope + deliverables + acceptance criteria + assumptions/exclusions
3. **Risk Register (formal)** — แยกออกจาก SPEC, มี ID/owner/prob/impact/mitigation/review-date
4. **Software Requirements Specification (SRS)** — แยกจาก SPEC, มี Req-ID เพื่อทำ traceability ภายหลัง
5. **Test Plan + Test Strategy** — incl. agent eval harness, Thai quality gates, golden trace approach
6. **Coding & Prompt Standards** — Black/Ruff, prompt versioning, schema convention, secret handling

### Tier 2 — ทำขณะ Phase 1 implementation (2-3 สัปดาห์)
7. **Software Design Description (SDD)** — รวมจาก SPEC + llm-allocation + thai-genai-stack มาเป็นเอกสารเดียวที่ครบ architecture + detailed design + decision rationale
8. **Traceability Matrix** — Requirement ↔ Design ↔ Code ↔ Test
9. **Test Cases & Test Procedures**
10. **SCM Plan** — branch model, release tag convention, baseline definition, SCI list
11. **Change Request log + procedure**
12. **Progress Status Record template** + weekly cadence
13. **Operation/Runbook** (เริ่ม draft ตั้งแต่ Phase 1 deploy)

### Tier 3 — ก่อน Phase 1 close (sign-off readiness)
14. **Test Report**
15. **Verification Results** (peer review records)
16. **Validation Results** (stakeholder sign-off)
17. **Acceptance Record**
18. **Correction Register**
19. **Closure Report** (Phase 1 retrospective + lessons learned)
20. **User Documentation** (supervisor / ops manual)
21. **Maintenance Documentation**
22. **Stakeholder Register / RACI** (ถ้ายังไม่เสร็จ)
23. **Repository Backup Procedure**

---

## 7. Proposed Repo Structure (after gap fill)

```
auto-affi/
├── README.md
├── SPEC.md                                 (kept, reference)
├── docs/
│   ├── pm/
│   │   ├── project-plan.md                 (Tier 1)
│   │   ├── statement-of-work.md            (Tier 1)
│   │   ├── risk-register.md                (Tier 1)
│   │   ├── stakeholder-register.md         (Tier 3)
│   │   ├── change-requests/
│   │   │   ├── CR-template.md
│   │   │   └── log.md
│   │   ├── status-reports/
│   │   │   └── 2026-W19.md                 (weekly)
│   │   ├── meeting-minutes/
│   │   ├── acceptance-records/
│   │   ├── correction-register.md
│   │   └── closure-reports/
│   ├── si/
│   │   ├── srs.md                          (Tier 1)
│   │   ├── sdd.md                          (Tier 2)
│   │   ├── traceability-matrix.md          (Tier 2)
│   │   ├── test-plan.md                    (Tier 1)
│   │   ├── test-cases/
│   │   ├── test-reports/
│   │   ├── scm-plan.md                     (Tier 2)
│   │   ├── coding-standards.md             (Tier 1)
│   │   ├── prompt-standards.md             (Tier 1)
│   │   ├── operation-guide.md              (Tier 2-3)
│   │   ├── maintenance-docs.md             (Tier 3)
│   │   ├── user-documentation.md           (Tier 3)
│   │   └── peer-reviews/
│   ├── llm-allocation.md                   (kept — feeds SDD)
│   ├── thai-genai-stack.md                 (kept — feeds SDD)
│   ├── execution-playbook.md               (kept — feeds Project Plan + Risk Register)
│   └── iso29110-gap-analysis.md            (this file)
```

---

## 8. คำแนะนำ — Pragmatic vs Pure Compliance

ISO 29110 Basic เหมาะมากสำหรับ VSE — **ไม่ต้องทำทุก artifact แบบ formal** ถ้าเหตุผลไม่คุ้ม

**ทำแบบเต็ม (formal sign-off)**:
- Project Plan, SOW, Risk Register, SRS, Test Plan, SCM Plan, Coding Standards
- เหตุผล: ทำครั้งเดียว มี discipline ทั้ง project

**ทำแบบ lightweight** (อาจเป็น git issue / weekly markdown):
- Status Reports, Meeting Minutes, CR log, Correction Register
- เหตุผล: ทุกคนรู้ context อยู่แล้ว เอา discipline ไม่ต้องเอา ceremony

**ทำเฉพาะตอนใกล้ milestone**:
- Acceptance Record, Verification Results, Validation Results, Closure Report

**ทำตอน Phase 2+**:
- User Documentation, Maintenance Docs, Stakeholder RACI (เพิ่มเมื่อทีมโตขึ้น)

---

## 9. Open Questions
1. ต้องการ formal compliance ISO 29110 (audit-ready) หรือใช้เป็น guideline?
2. ถ้า audit-ready → ต้องเตรียม Verification & Validation Records ทุกชิ้น (effort สูง)
3. ใช้ tool อะไร track CR / Status / Risk? — GitHub Issues + Projects เพียงพอหรือต้อง Jira/Linear?
4. ใครเป็น Project Manager? (ISO 29110 ต้องระบุชัด)
5. Phase 1 จะตั้ง baseline date เมื่อไร? (ต้องล็อกสำหรับ progress tracking)
