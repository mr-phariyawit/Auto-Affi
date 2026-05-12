# Statement of Work — Auto-Affi

- **Project**: Auto-Affi (AI Marketing Platform, Shopee affiliate TH)
- **Sponsor**: TBD
- **Project Manager**: Nick Fury (aegis-team)
- **Compliance**: ISO 29110 Basic (guideline mode)
- **Last updated**: 2026-05-12

---

## 1. Background
ตลาดไทยขาด TH-localized full-stack AI affiliate tool ที่รวม Shopee Open API + Thai script gen + multi-account publishing + subId attribution กลับ creative variant — ดูรายละเอียดที่ `docs/execution-playbook.md` §1

## 2. Objectives
1. ลด human-hour ในการผลิต affiliate video ลง ≥ 90% เทียบ baseline manual
2. Achieve Phase 1 GMV ≥ $200 / 14 วัน ใน beauty niche (baseline 100%) → stretch $5k/เดือน (300%)
3. Build self-learning loop ที่ MoM CTR uplift ≥ 5% หลัง Phase 3
4. Operate ภายใต้ Thai regulation (OCPB, PDPC, NBTC) + platform ToS (Shopee, TikTok, IG, YT)

## 3. Scope — In Scope
### 3.1 System Components (Phase 1 minimum)
- Shopee Open API adapter (product search, deep link, conversion report)
- AI agent crew: Scout, Strategist, 1 Writer, Producer, Editor, Publisher, Analytics, Feedback Curator, Safety
- Temporal workflow orchestration
- Postgres + pgvector + Redis + S3 data plane
- 9:16 video pipeline (Veo 3 Fast via kie.ai + ElevenLabs TTS + Hyperframe + FFmpeg)
- IG Reels publishing + subId tagging
- LLM Wiki (vector layer, Phase 1)
- Ops console (internal supervisor dashboard)

### 3.2 Phase 2 Additions
- Writers' Room ครบ (Director, Screenwriter, Cinematographer, Storyboard Artist, Sound Designer, Critic)
- FB Reels + YouTube Shorts publishing
- Multi-account portfolio (10 accounts / niche)
- LLM Wiki tier system + Mem0 + Graphiti KG
- Bilateral-sync wiki review queue

### 3.3 Phase 3 Additions
- Auto prompt evolution (harness-evolver)
- Cost-aware planner
- Multi-niche expansion (Mom&Baby, gadgets, food)
- Optional: live commerce AI host

## 4. Out of Scope (Exclusions)
- ❌ Paid ads (Phase 1-3 organic only)
- ❌ Multi-tenant SaaS — internal use only
- ❌ Non-Thai markets (Phase 3+ optional)
- ❌ Lazada / TikTok Shop direct integration (Phase 3 stretch)
- ❌ Live commerce streaming (Phase 3.5 optional)
- ❌ Real-time human chat / customer service
- ❌ B2B sales / lead generation
- ❌ Financial / medical / regulated niches (compliance hard-block)
- ❌ Non-Thai TTS (Phase 1-3)
- ❌ Custom video model training (use commercial models via kie.ai)

## 5. Deliverables

| # | Deliverable | Phase | Acceptance Owner |
|---|---|---|---|
| D1 | Repository skeleton + CI/CD | Phase 0 | Tech Lead |
| D2 | ISO 29110 Tier 1 docs (this batch) | Phase 0 | Nick Fury |
| D3 | Linear board configured (cycles, labels, automations) | Phase 0 | Nick Fury |
| D4 | Shopee API adapter (functional + tested) | Phase 1 | Tech Lead |
| D5 | Temporal workflow + DB schema deployed | Phase 1 | Tech Lead |
| D6 | Agent v1 (Scout + Strategist + Writer) with eval harness | Phase 1 | AI Eng |
| D7 | Video pipeline producing 1 master mp4 from prompt | Phase 1 | Video Eng |
| D8 | IG Reels publish + subId attribution working end-to-end | Phase 1 | Tech Lead |
| D9 | Analytics polling + Wiki write loop operational | Phase 1 | AI Eng |
| D10 | Phase 1 closure report + lessons learned | Phase 1 | Nick Fury |
| D11 | Writers' Room + multi-platform live | Phase 2 | AI Eng |
| D12 | 10-account portfolio operating with rotation | Phase 2 | Ops |
| D13 | Bilateral-sync Wiki + KG layer live | Phase 2 | AI Eng |
| D14 | Harness-evolver running + Phase 3 KPI dashboard | Phase 3 | Tech Lead |

## 6. Acceptance Criteria
แต่ละ deliverable ต้องผ่านเงื่อนไข:
1. **Functional**: ตรงตาม requirement ใน `docs/si/srs.md`
2. **Quality gate**: pass test plan ใน `docs/si/test-plan.md`
3. **Compliance**: pass safety check (OCPB rules + platform ToS)
4. **Sign-off**: Nick Fury record acceptance ใน `docs/pm/acceptance-records/` หรือ Linear issue close

## 7. Assumptions
- Anthropic Claude API + Shopee Affiliate Open API + kie.ai available throughout project
- Team มีสิทธิ์ใช้ aegis-team Linear workspace
- มี Thai-speaking team member ≥ 1 คนสำหรับ Critic / Quality Gate review
- มี GPU H100 × 2 หรือ A10 × 2 สำหรับ self-host (Typhoon, Whisper)
- มี budget ≥ $1,800/mo ตาม `project-plan.md` §5

## 8. Constraints
- Compliance ระดับ guideline (ไม่ audit-ready) — เร่ง velocity ได้
- ห้าม commit secret / API key ลง git
- ห้ามใช้ Helicone (maintenance mode — ตาม `execution-playbook.md` §4)
- ห้ามทำ visual product alteration (TikTok policy)
- ห้ามใช้ generic OpenAI TTS สำหรับ Thai
- ห้าม direct wiki write จาก agent (bilateral sync only)

## 9. Schedule Frame
ดูรายละเอียดที่ `docs/pm/project-plan.md` §3 — Phase 0 → 3 across ~24 สัปดาห์

## 10. Change Management
- Change request submit เป็น Linear issue label `cr`
- Nick Fury review ภายใน 24 ชม.
- Material change (เปลี่ยน scope/budget/schedule > 10%) → escalate sponsor

## 11. Termination Clauses
- หาก Phase 1 GMV < $50 / 14 วัน → review go/no-go ของ Phase 2
- หาก budget overrun > 30% และ trend ไม่ดีขึ้น 2 สัปดาห์ติด → kill switch

## 12. Sign-off
| Role | Name | Date |
|---|---|---|
| Project Manager | Nick Fury | _________ |
| Sponsor | TBD | _________ |
| Tech Lead | TBD | _________ |
