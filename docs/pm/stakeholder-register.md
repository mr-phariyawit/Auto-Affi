# Stakeholder Register & RACI — Auto-Affi

- **Owner**: Nick Fury
- **Last updated**: 2026-05-12

---

## 1. Stakeholders

| Stakeholder | Role | Interest | Authority | Contact |
|---|---|---|---|---|
| **Nick Fury** | Project Manager (aegis-team) | Delivery, risk, schedule, budget | Full PM authority + scope/budget changes ≤ 10% | Linear @nick.fury |
| **Sponsor** | TBD | Business outcome, ROI, GMV target | Approve material change, kill switch | TBD |
| **Tech Lead** | aegis-team engineer | Architecture, code quality | Tech stack decisions, deploy approval | TBD |
| **AI / Prompt Engineer** | aegis-team | Agent prompts, eval, wiki | Prompt promotion, wiki tier changes | TBD |
| **Video Pipeline Engineer** | aegis-team | Editor + Hyperframe + ffmpeg + ASR + TTS | Video pipeline architecture | TBD |
| **Ops / Safety Engineer** | aegis-team | Publishing accounts, compliance, kill switches | Hold/release published content | TBD |
| **End User** (internal) | aegis-team supervisor on duty | Ops console, daily monitoring | Manual override of pipeline | TBD |
| **Anthropic** | LLM provider | API stability | API access conditions, rate limits | support |
| **Shopee Affiliate** | Commission payer | Compliance, payout | Affiliate ToS, key revoke | partner portal |
| **kie.ai** | Gateway provider | Service health | Per-request access, pricing | support |
| **ElevenLabs / Botnoi** | TTS vendors | Voice generation | API access | support |
| **OCPB (สคบ.)** | Thai regulator | Consumer protection | Fines, enforcement | public hotline |
| **PDPC** | Thai data regulator | PDPA compliance | Fines (up to 5M THB) | pdpc.or.th |

---

## 2. RACI Matrix

**Legend**: R = Responsible (doer) · A = Accountable (sign-off owner) · C = Consulted · I = Informed

| Deliverable / Decision | PM (Fury) | Sponsor | Tech Lead | AI Eng | Video Eng | Ops/Safety |
|---|---|---|---|---|---|---|
| Project Plan & SOW | **A** R | C | C | I | I | I |
| Budget approval | **A** | R | C | I | I | I |
| Scope change > 10% | R | **A** | C | C | C | I |
| Architecture decisions | I | I | **A** R | C | C | C |
| Tech stack changes | I | I | **A** R | C | C | I |
| Agent prompt v1 + eval setup | I | I | C | **A** R | I | C |
| Prompt promotion to prod | I | I | C | **A** R | I | C |
| Wiki tier change / canonical lock | I | I | C | **A** R | I | C |
| Wiki entry promotion (bilateral sync) | I | I | I | R | I | **A** |
| Video pipeline architecture | I | I | C | C | **A** R | I |
| Video gen vendor switch (kie.ai vs direct) | I | I | C | I | **A** R | I |
| Publishing account management | I | I | I | I | I | **A** R |
| Pre-publish safety gate | I | I | I | C | I | **A** R |
| Kill switch trigger | I | I | C | C | C | **A** R |
| Phase exit go/no-go | R | **A** | C | C | C | C |
| Risk register review | **A** R | I | C | C | C | C |
| Change request approval | **A** | C (if material) | C | I | I | I |
| Sprint planning (Linear cycle) | **A** R | I | C | C | C | C |
| Code review approval (per PR) | I | I | **A** R | C | C | I |
| Daily Linear standup | R | I | R | R | R | R |
| Weekly status report | **A** R | I | C | C | C | C |
| Incident response (P0/P1) | **A** | I | R | R | R | R |
| External vendor escalation | **A** R | C (if material) | C | C | C | C |
| Compliance violation response | C | I | C | C | C | **A** R |
| PDPC / OCPB inquiry | **A** R | I | I | C | I | C |

---

## 3. Communication Matrix

| Audience | Channel | Frequency | Content | Owner |
|---|---|---|---|---|
| All team | Linear async | Daily | Yesterday/today/blocker | each |
| All team | Sync meeting | Weekly (30 min) | Demo + plan next sprint | Nick Fury |
| Sponsor | Status report | Weekly markdown | KPI + risks + decisions | Nick Fury |
| Sponsor | Steering review | Monthly | Strategy + budget | Nick Fury |
| Sponsor | Phase exit review | Per phase | Outcome + retrospective | Nick Fury |
| External vendor (kie.ai, ElevenLabs) | Email / portal | On-need | Support tickets | Tech Lead |
| Regulators | Formal letter | Reactive only | When inquiry received | Nick Fury + counsel |

---

## 4. Engagement Strategy

| Stakeholder | Engagement Level | Strategy |
|---|---|---|
| Sponsor | Keep satisfied | Monthly steering + weekly status |
| Tech / AI / Video / Ops Eng | Manage closely | Daily Linear + weekly sync |
| Anthropic / Shopee / kie.ai | Keep informed | Monitor changelog + portal alerts |
| OCPB / PDPC | Monitor + comply | Quarterly compliance audit, react fast on inquiry |
| Internal supervisor | Keep informed | Ops console + weekly walkthrough |
