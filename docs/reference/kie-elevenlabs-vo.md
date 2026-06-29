---
title: VO via ElevenLabs v3 (kie.ai) — VERIFIED recipe
created: 2026-06-29
status: end-to-end VERIFIED LIVE (taskId fef12dcf..., state=success, real 4.75s mp3 downloaded)
key: KIE_API_KEY in .env (never echo the value)
---

# Auto-Affi VO — ElevenLabs v3 via kie.ai (the ONLY VO engine, per human directive)

Style directive: **ตื่นเต้น / เสียงดัง (excited, loud)** → `[excited]` audio tag + `stability: 0` (most expressive).

## Endpoints (VERIFIED — the published doc was WRONG on the poll path)
- **Create:** `POST https://api.kie.ai/api/v1/jobs/createTask`  (Bearer KIE_API_KEY)
- **Poll:**   `GET  https://api.kie.ai/api/v1/jobs/recordInfo?taskId=<id>`  ← NOT `getTaskDetail` (404)
- **Download:** the `resultJson` URL (`https://tempfile.aiquickdraw.com/voice/<id>.mp3`) **requires a browser
  `User-Agent` header** or it 403s. Use `curl -L -A "Mozilla/5.0 ..."`.

## Create body
```json
{
  "model": "elevenlabs/text-to-dialogue-v3",
  "input": {
    "dialogue": [
      { "text": "[excited] ร่มเปียกเนี่ย ศัตรูหมายเลขหนึ่งของคนขึ้นรถเลย บอกเลย!", "voice": "EkK5I93UQWFDigLMpZcX" }
    ],
    "stability": 0,            // 0 | 0.5 | 1.0  — 0 = most expressive/excited
    "language_code": "th"      // Thai supported (54+ langs)
  }
}
```
- `dialogue[]` can hold multiple lines/voices (it is text-to-DIALOGUE) → one entry per VO beat.
- Audio tags (`[excited]`, `[shouting]`, `[laughs]`) are ElevenLabs-v3 native (kie.ai doc doesn't list them but the model honours them). Combine with `stability:0` for the loud/hyped read.
- Voices: 68+ presets (James `EkK5I93UQWFDigLMpZcX`, Arabella `Z3R5wn05IrDiVCyEkUrK`, Bella `hpp4J3VqNfWAUOO0d1Us`, ...). **Pick a voice the human approves by ear** — English-trained voices speak Thai with possible accent.

## Response
- `createTask` → `{ code:200, data:{ taskId, recordId } }`
- `recordInfo` → `data.state` in {waiting, generating, success, failed}; on success `data.resultJson` holds the mp3 URL; `data.creditsConsumed` = real spend.

## Cost / gate
Each VO line bills kie.ai credits (creditsConsumed in recordInfo). Route through the spend gate like any
paid generation; verify-before-spend (one short line) before batching all VO beats.
