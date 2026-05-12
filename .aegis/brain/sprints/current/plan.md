# Sprint 2 Plan -- Auto-Affi

- **Sprint**: sprint-2
- **Goal**: Build the video production pipeline and publishing foundation -- from Storyboard to rendered video to IG Reels publish with trackable affiliate links. This completes the "single closed loop" through the production+publish stages.
- **Duration**: 5 days (2026-05-13 to 2026-05-18)
- **Capacity**: 28 story points
- **Phase**: Phase 1 -- Single Closed Loop
- **Predecessor**: Sprint 1 (26/26 pts, 100% delivered)

---

## Sprint Backlog

| Task ID | Title | Epic | Points | Assignee | Priority |
|---------|-------|------|--------|----------|----------|
| AFFI-T-004 | Wiki saturation query for Scout dedup | E-001 | 3 | spider-man | P3 |
| AFFI-T-012 | Video gen adapter interface + Veo 3 impl | E-004 | 5 | spider-man | P1 |
| AFFI-T-013 | Editor agent standard passes framework | E-004 | 5 | spider-man | P1 |
| AFFI-T-015 | Editor budget cap + FFmpeg fallback | E-004 | 3 | spider-man | P2 |
| AFFI-T-016 | TTS provider adapter (ElevenLabs + fallback) | E-004 | 3 | spider-man | P2 |
| AFFI-T-017 | IG Reels publisher adapter (Meta Graph API) | E-005 | 5 | spider-man | P1 |
| AFFI-T-019 | SubId taxonomy injection into deep links | E-005 | 2 | spider-man | P2 |
| AFFI-T-020 | Caption builder with ad disclosure | E-005 | 2 | spider-man | P2 |

**Total**: 28 points across 8 tasks

---

## Sprint Rationale

Sprint 2 targets the middle-to-right pipeline: Video Production + Publishing.
After Sprint 1 (Scout -> Strategy -> Writers -> Safety), the missing link for
Phase 1 exit is: Storyboard -> Video -> Publish -> (Analytics + Wiki in Sprint 3).

Priority order follows pipeline dependency:
1. Video gen adapter (T-012) + Editor passes (T-013) = produce a video from storyboard
2. TTS adapter (T-016) + Budget cap (T-015) = voice + cost control
3. IG publisher (T-017) + SubId injection (T-019) + Caption (T-020) = publish with tracking
4. Wiki saturation (T-004) = remaining Scout task from Sprint 1

---

## Definition of Done (per task)

1. Implementation passes lint via `.venv/bin/python -m ruff check`
2. Unit tests pass via `.venv/bin/python -m pytest -m unit`
3. Black Panther code review APPROVED
4. SI.02 traceability updated
5. No P0/P1 issues open

---

## Risks

- Video gen adapter (T-012) depends on kie.ai API which requires credentials -- fallback to local_renderer for dev
- IG publisher (T-017) requires Meta Graph API access + long-lived page token -- implement with mock transport, integration test deferred
- Editor passes (T-013) require ffmpeg on the system -- CI may need ffmpeg installed
