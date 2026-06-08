# ElevenLabs v3 Options Playbook for Thai Auto-Affi VO

Date: 2026-06-05


## Executive Takeaway


1. `stability`
2. `language_code`
3. `dialogue[].text`
4. `dialogue[].voice`
5. multi-line / multi-voice dialogue structure
6. `callBackUrl` for async production orchestration

The biggest creative lever is not a hidden API field. It is prompt-text engineering inside `dialogue[].text`: audio tags, punctuation, emphasis, shorter scene lines, and better voice selection.



```json
{
  "model": "elevenlabs/text-to-dialogue-v3",
  "input": {
    "dialogue": [
      {
        "text": "ฝนมาไวอีกแล้ว! ไม่ต้องให้วันสะดุดค่ะ",
        "voice": "hpp4J3VqNfWAUOO0d1Us"
      }
    ],
    "stability": 0.0,
    "language_code": "th"
  }
}
```

### `stability`

Meaning: how stable/consistent the voice is versus how expressive/random the result can be.

Observed and recommended:

- `0.0`: most expressive; best candidate for brighter ads; slightly more variable.
- `0.5`: balanced; v9 was technically clean but emotionally sleepy.
- `1.0`: likely too monotone for short-form ads, but useful for calm explainers or legal/medical tone.

For Thai affiliate ads, start with `0.0` or `0.5`. Reject if it hallucinates weird non-speech, mispronounces Thai, or overacts.

### `language_code`

Use `th` for Thai. Use `auto` only for mixed-language lines where English brand names become worse under `th`.

For production, write Thai numbers and product claims in spoken Thai text manually instead of relying on text normalization:

- Prefer: `ยูวีห้าสิบพลัส`, `สิบเก้าบาท`
- Avoid raw: `UV50+`, `19 บาท`, `IPX8`

### `dialogue[].text`

This is the real creative control surface. Eleven v3 responds to:

- audio tags: `[excited]`, `[happy]`, `[curious]`, `[whispers]`, `[laughs]`, `[sighs]`
- punctuation: `!`, `?`, `...`
- capitalization/emphasis in English terms
- line structure and breathing room

ElevenLabs docs explicitly say Eleven v3 does not support SSML break tags. Use audio tags, punctuation, ellipses, and text structure instead.

Thai commercial examples worth testing:

```text
[excited] ฝนมาไวอีกแล้ว! ไม่ต้องให้วันสะดุดค่ะ
```

```text
[bright] มือเปียก กระเป๋าเปียก... แต่เราจัดการได้ทันที
```

```text
[friendly] ผ้าไมโครไฟเบอร์ผืนเล็กนี่แหละ พกง่ายมาก
```

Keep tags sparse. One tag per scene is usually enough. Too many tags can make the voice theatrical or unstable.

### `dialogue[].voice`


```text
hpp4J3VqNfWAUOO0d1Us
```

Working label in our runs:

```text
bella_professional_bright_warm
```

For future tests, find 3-5 Thai-friendly voices and score them on:

- Thai pronunciation
- ad energy
- trustworthiness
- age/persona fit
- stability under `[excited]`
- consistency across 12 scene segments

### Multi-Speaker / Multi-Voice


This enables:

- creator + friend Q&A
- customer objection + narrator answer
- before/after comedic contrast

For strict scene sync, Auto-Affi should still generate one 5s scene voice task at a time. Multi-speaker in a single long request may sound more conversational but is harder to align to video beats.


Native endpoint:

```text
POST /v1/text-to-dialogue
```

Native body/query controls include:

- `inputs[]`: text + `voice_id`
- `model_id`: default `eleven_v3`
- `language_code`
- `settings.stability`
- `pronunciation_dictionary_locators`: up to 3 dictionaries
- `seed`: best-effort deterministic generation
- `apply_text_normalization`: `auto`, `on`, `off`
- `output_format`: mp3/opus/pcm/wav variants

Native timestamp endpoint:

```text
POST /v1/text-to-dialogue/with-timestamps
```


## Recommended v11 Experiment Matrix

Run short A/B tests before a full 60s render:

| Variant | Stability | Text style | Goal |
| --- | ---: | --- | --- |
| A | 0.0 | v10 copy + `[excited]` first 3 scenes | More ad energy |
| B | 0.0 | v10 copy + `[friendly]`/`[bright]` sparse tags | Warm but not shouty |
| C | 0.5 | v10 copy + tags | Check if tags alone can beat sleepy tone |
| D | 0.0 | Q&A two-speaker micro dialogue | More TikTok-native feel |
| E | 0.0 | New voice ID, same v10 copy | Test whether voice choice beats prompt tweaking |

Suggested first test payload:

```json
{
  "model": "elevenlabs/text-to-dialogue-v3",
  "input": {
    "dialogue": [
      {
        "text": "[excited] ฝนมาไวอีกแล้ว! ไม่ต้องให้วันสะดุดค่ะ",
        "voice": "hpp4J3VqNfWAUOO0d1Us"
      }
    ],
    "stability": 0.0,
    "language_code": "th"
  }
}
```

## Youthful / Cheerful Voice Shortlist



```text
https://static.aiquickdraw.com/elevenlabs/voice/<voice_id>.mp3
```


Recommended audition order for a younger, brighter Thai commercial tone:

| Rank | Voice | Voice ID | Why test | Risk |
| ---: | --- | --- | --- | --- |
| 3 | Anika - Animated, Friendly and Engaging | `Sm1seazb4gs7RSlUVw7c` | Friendly and engaging; likely brighter than Bella. | Could be too animated. |
| 4 | Hope - Bubbly, Gossipy and Girly | `uYXf8XasLslADfZ2MB4u` | Directly bubbly/girly. | Could become too gossip/cartoon for product trust. |
| 5 | Laura - Enthusiast, Quirky Attitude | `FGY2WhTYpPnrIDTdsKH5` | Enthusiastic and quirky. | May overact or accent Thai poorly. |
| 6 | Lucy - Fresh and Casual | `lcMyyd2HUfFzxdCaC4Ta` | Fresh/casual fallback from older Auto-Affi plan. | May not be energetic enough. |
| 7 | Adeline - Feminine and Conversational | `5l5f8iK3YPeGga21rQIX` | Natural conversational female fallback. | May be pleasant but less youthful. |
| 9 | Bella - Professional, Bright, Warm | `hpp4J3VqNfWAUOO0d1Us` | Known working baseline from v9/v10. | Previously judged sleepy without aggressive copy/stability tuning. |

### Rejected External Voice IDs


| Voice | Voice ID |
| --- | --- |
| Anna - Thailand Female | `brM9iIbwDREZaWL8luun` |
| Bridgit - Bright Friendly Youthful | `KR1TkIhkSykEjI4B0DtH` |
| Emme | `QI7MqdLSOT7Xq48Th0oc` |
| Lana - Upbeat Friendly | `0zj1iWvloMkAXydIFsJR` |
| Rhea - Cheerful Friendly | `TXb68m09B5U6BTh8UMd5` |
| Candy - Young and Sweet | `Nggzl2QAXh3OijoXD116` |
| Maisie - Friendly Casual | `QtY3JBOUKEB5xzrRfOKc` |

### External Voice Index Candidates

Recommended audition order:

| Rank | Voice | Voice ID | Why test | Risk |
| ---: | --- | --- | --- | --- |
| 1 | Anna - Thailand Female | `brM9iIbwDREZaWL8luun` | Authentic Thai female accent; best chance for natural Thai pronunciation. | May be less teen/bright than Gen Z ad voices. |
| 2 | Bridgit - Bright Friendly Youthful | `KR1TkIhkSykEjI4B0DtH` | Explicitly described as bright, friendly, youthful Gen Z for commercials. | English-origin voice may accent Thai. |
| 3 | Emme | `QI7MqdLSOT7Xq48Th0oc` | Bright youthful American female, friendly upbeat energy. | Thai pronunciation unknown. |
| 4 | Lana - Upbeat Friendly | `0zj1iWvloMkAXydIFsJR` | Young, lively, bright, expressive tone. | Thai pronunciation unknown. |
| 5 | Rhea - Cheerful and Friendly | `TXb68m09B5U6BTh8UMd5` | Cheerful, energetic companion voice. | Could become too character-like. |
| 6 | Candy - Young and Sweet | `Nggzl2QAXh3OijoXD116` | Youthful, cute, bubbly, excited, happy. | High risk of sounding cartoonish/too young for commerce. |
| 7 | Maisie - Friendly Casual | `QtY3JBOUKEB5xzrRfOKc` | Bright girl-next-door commercial tone. | Alto voice may read older than desired. |
| 8 | Jessica - British warm | `jP5jSWhfXz3nfQENMtf4` | Warm female voice; worth testing if Thai pronunciation is acceptable. | Not clearly teen/Gen Z from listing. |

Legacy candidates from earlier Auto-Affi notes:

- Eve: `BZgkqPqms7Kj9ulSkVzn`
- Lucy: `lcMyyd2HUfFzxdCaC4Ta`

These should be treated as fallback candidates only until retested, because current public voice indexes may use different Lucy/Eve IDs than our older notes.

### Audition Script

Use the same 2-line Thai test for every candidate:

```text
[excited] ฝนมาไวอีกแล้ว! ไม่ต้องให้วันสะดุดค่ะ
[friendly] ผ้าไมโครไฟเบอร์ผืนเล็กนี่แหละ พกง่ายมาก
```

Scoring rubric:

- Thai pronunciation: 0-5
- Youthful energy: 0-5
- Cheerfulness without cartoon effect: 0-5
- Commercial trust: 0-5
- Consistency across two short lines: 0-5

Reject immediately if:

- Thai sounds foreign enough to distract.
- Tone sounds like a child rather than a young adult.
- Tags cause laughter, weird breath, or non-speech artifacts.
- The same voice changes persona between the two lines.

## Production Guardrails

- Generate one short line per visual scene unless testing multi-speaker.
- Reject any segment requiring speed factor above `1.08x`; rewrite the line instead.
- Keep final source video audio-free; add only the intended VO track in HyperFrames.
- Save task IDs, credit before/after, segment durations, stability, voice ID, and payload preview.

## Sources

- ElevenLabs Text to Dialogue API: https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert
- ElevenLabs Text to Dialogue with timestamps API: https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert-with-timestamps
- ElevenLabs prompting and Eleven v3 best practices: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
