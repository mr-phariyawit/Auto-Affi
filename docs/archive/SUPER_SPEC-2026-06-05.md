# [ARCHIVED] Auto-Affi — Consolidated Super Spec (ISO 29110 Edition)

> **ARCHIVED 2026-06-08.** Superseded by [`SPEC.md`](../../SPEC.md) (single source of truth).
> Operational gates (§5 below) were folded into `SPEC.md` §10.5. Preserved verbatim for history.
> ⚠️ Stack notes below are STALE — names ElevenLabs/Chirp + TikTok-first; current stack is
> Higgsfield Seedance 2.0 + edge-tts + IG-first (see `SPEC.md` §19.3).

---

**Date:** 2026-06-05  

---

## 1. The Team (Auto-Affi Multi-Agent Studio)
The project is operated by a 24/7 subagent team supervised by a Human PM.

**Key Divisions:**
- **Command Center:** Global orchestration (ISO PM.1).
- **Intel Group:** News Desk, Social Radar, Culture Analyst.
- **Control Group:** Ethics, Compliance, Knowledge Librarian.

## 2. The Core Doctrine

## 3. Technical Stack
- **Post-Production:** FFmpeg + HyperFrames (Muxing Thai VO / Overlays).
- **Voice:** ElevenLabs Thai v3 / Chirp 3 HD.
- **Data:** Local CSV registry with subId attribution (5 levels).
- **Platforms:** TikTok (API), Shopee (API/App Packet).
- **Secrets:** Required production provider keys are provisioned in project `.env`; provider calls must load `.env` and must never print secret values.

## 4. ISO 29110 Traceability
All development artifacts live in `iso29110/`:
- **Planning:** `management/PM1_Project_Management_Plan/`
- **Requirements:** `implementation/SI2_Requirements_Specification/`
- **Design:** `implementation/SI3_Software_Design/`
- **Verification:** `implementation/SI7_Traceability_Matrix/` (Planned)

## 5. Compliance Gates (Non-Negotiable)
1. **Human-in-the-Loop:** No public post without human approval.
2. **Speed Guard:** Thai VO must be 1.0x - 1.15x speed.
3. **Disclosure:** `#โฆษณา #affiliate` mandatory in all captions.
4. **Cleanroom:** Exactly 1 video + 1 audio stream in final delivery.
5. **Env Secrets:** No provider call before `.env` is loaded and required secret variable names are present.
6. **Caption/VO Sync:** Final render is blocked unless captions match the approved voice segment report.
7. **Learning Closeout:** Every run records successes, failures, user-caught issues, and workflow rules changed.
8. **Seedance-Only Video:** Generated visual video uses `seedance_2_0` only; no visual-video fallback model.
10. **Human-Visible Storyboard:** No paid visual-video provider call before a 3x3 storyboard/contact sheet is shown and approval is recorded in `pre_generation_user_review.json`.

---
*Source: Documents/Auto-Affi/SUPER_SPEC.md (Updated 2026-06-05)*
