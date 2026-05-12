# Thai-Focused GenAI Stack — Auto-Affi

แผนเลือก model สำหรับ **script (text) / image / video / voice / ASR** ที่ดีที่สุดในตลาด ณ ตอนนี้ — **เน้นภาษาไทยเท่านั้น**

- **Last updated**: 2026-05-12
- **Principle**: ใช้ model ที่ดีที่สุดในโลก *แต่* prompt และ post-process ให้เหมาะกับภาษาไทย — ไม่จำเป็นต้องใช้ "Thai model" ทุกชั้นถ้า frontier model ทำได้ดีกว่า

---

## 1. Script / บทพูด / Caption (Text Generation)

### 1.1 ตัวเลือกอันดับ 1 — Claude Opus 4.7 + Sonnet 4.6
- **Strength**: Thai นาตู่ดีเยี่ยม รวมถึง register (ทางการ / กันเอง / Gen-Z / สลัง), cultural reference, idiom, รุ้สึก tone ได้ดีกว่า GPT/Gemini
- **Use**: Strategist, Director, Critic, Curator → Opus 4.7 / Screenwriter → Sonnet 4.6
- **Prompt language**: ผสมไทย-อังกฤษได้ — system prompt อังกฤษ + brand voice guide ไทย + Few-shot ไทย

### 1.2 ตัวเลือกเสริม — Typhoon 2 (SCB 10X / OpenTyphoon)
- Thai-native fine-tune (Llama 3.1 70B base) — **เก่งสุดสำหรับ Thai-only**
- **Use เป็น verifier / second opinion**: ใช้ Typhoon review script ที่ Claude เขียน เพื่อจับสำนวนที่ "ไม่เป็นไทย", awkward translation, Gen-Z slang validation
- self-host บน vLLM (H100 × 2) หรือ OpenTyphoon API

### 1.3 อย่าใช้
- ❌ GPT-4o-mini / Haiku 4.5 สำหรับ script — Thai creative tone อ่อนกว่า
- ❌ Open-source 7B models เปล่าๆ — Thai code-switching เพี้ยน

### 1.4 ขั้นตอน (Screenwriter)
```
Draft 1: Sonnet 4.6 (creative, Thai-native voice)
Polish:  Sonnet 4.6 (tone-tighten + hook punch)
Verify:  Typhoon 2 (Thai naturalness score)
Approve: Director (Opus 4.7)
```

### 1.5 Hook ภาษาไทย — ข้อสำคัญ
- ใช้คำกริยา-รุนแรงต้นประโยค ("หยุดเลย!", "ใครจะคิด...")
- หลีกเลี่ยงสำนวนแปล (literal translation จากอังกฤษ)
- ห้ามใช้คำเชยยุค 2010 ("เด็ดสะระตี่", "เริ่ดไปอีก") — ให้ Typhoon validate
- ใส่เสียงสะดุดหู (onomatopoeia ไทย: ปั้ง, แวบ, แชะ, ฟิ้ว)

---

## 2. Image Generation

### 2.1 ปัญหาหลักของไทย: **ตัวอักษรไทยในรูป**
**Image model ทุกตัวในโลก** ยัง render Thai script ไม่ดี (พยัญชนะ-สระ-วรรณยุกต์ซ้อนกันผิด, สระลอย, อักขระสลับ)

**กฎเหล็ก**: ❌ **ห้ามให้ image model วาดข้อความไทย** — ทุก Thai text จะถูก composite ผ่าน Hyperframe / Remotion ใน post

### 2.2 ตัวเลือกอันดับ 1 — Flux 1.1 Pro Ultra (Black Forest Labs)
- Photorealism + prompt adherence ดีที่สุด ณ ตอนนี้
- 4MP output, รองรับ 9:16 native
- **Use**: hero shot, product close-up, character portrait

### 2.3 ตัวเลือกอันดับ 2 — Midjourney v7
- Aesthetic / stylized ที่สุด — เหมาะ scene "moody" / luxury / dramatic
- API ไม่เปิด → ใช้ผ่าน proxy (Useapi.net) หรือ workaround
- **Use**: lifestyle scene, mood board, emotional cuts

### 2.4 ตัวเลือกอันดับ 3 — Google Imagen 4
- Prompt understanding แม่นมาก, ภาพคน + composition ดี
- **Use**: realistic Thai people / Thai street scene (ภาพไทยๆ Imagen 4 เข้าใจวัฒนธรรมดีกว่า Midjourney)

### 2.5 ตัวเลือกพิเศษสำหรับ Thai aesthetic
- **Recraft v3** — สำหรับ designed/graphic style (poster, infographic)
- **Ideogram 3** — ถ้าจำเป็นต้องมีตัวอักษร *อังกฤษ* ในภาพ (Thai ยังพัง)

### 2.6 Workflow ในระบบ
```
Cinematographer agent (Sonnet 4.6) → English visual prompt
   └─ adapter พิจารณา style:
        - photoreal product → Flux 1.1 Pro Ultra
        - lifestyle/mood     → Midjourney v7
        - Thai people/scene  → Imagen 4
        - graphic/poster     → Recraft v3
   └─ Generate (พื้นภาพไม่มี text)
   └─ Hyperframe overlay (Thai text + lower-third + animation)
```

### 2.7 Cost reference (per 9:16 image)
| Model | USD/image | คุณภาพ Thai context |
|---|---|---|
| Flux 1.1 Pro Ultra | $0.06 | ดี (ถ้า prompt ระบุ) |
| Midjourney v7 | ~$0.10 | ดี (Asian face พอใช้) |
| Imagen 4 | $0.04 | ดีมาก (Thai street/face) |
| Recraft v3 | $0.04 | ดี (graphic) |

---

## 3. Video Generation

### 3.1 ปัญหาหลักของไทย: **ภาษา prompt + Thai text in video**
- Video model ทุกตัวเข้าใจ prompt อังกฤษดีกว่าไทยมาก → **prompt ทุกครั้งเป็นอังกฤษ**
- Native audio ของ Veo 3 / Sora 2 ภาษาไทย **ยังเพี้ยน** (โทนเสียง / accent / lip-sync ไทยพัง)
- **กฎ**: video gen สร้างภาพล้วน → TTS ไทยแยก → mux ใน post

### 3.2 ตัวเลือกอันดับ 1 — Veo 3.1 (Google)
- คุณภาพ / motion realism / prompt adherence ดีที่สุด ณ ต้น 2026
- 1080p, สูงสุด 8 วินาที/clip, รองรับ 9:16
- มี image-to-video (สำคัญ — เริ่มจาก Flux image)
- **Use**: scene หลักทุก scene ที่ต้องการ realism

### 3.3 ตัวเลือกอันดับ 2 — Sora 2 (OpenAI)
- Physics simulation + camera motion เนียนกว่า Veo บางกรณี
- Latency สูงกว่า, cost สูงกว่า
- **Use**: hero scene / fallback เมื่อ Veo prompt fail

### 3.4 ตัวเลือกอันดับ 3 — Kling 2.1 (Kuaishou)
- Asian face / Asian body motion เนียนสุดในสาย (เพราะ train data Asian เยอะ)
- **Use เฉพาะ**: scene ที่มี Thai/Asian people เป็น subject

### 3.5 ตัวเลือกเสริม — Runway Gen-4 / Hailuo / Pika 2.0
- Fallback adapter เมื่อ rate-limit
- Hailuo MiniMax เร็ว + ถูก เหมาะ b-roll

### 3.6 Adapter Strategy
```
Producer agent decides per scene:
  - "Thai person closeup, emotion"   → Kling 2.1
  - "Product spinning hero"          → Veo 3.1
  - "Cinematic establishing shot"    → Sora 2 (premium) / Veo 3.1
  - "Quick b-roll / texture"         → Hailuo (cost)
  - "Stylized motion graphic"        → Hyperframe (HTML→video)
```

### 3.7 Cost reference (per 5-8s clip)
| Model | USD/clip | ใช้กรณี |
|---|---|---|
| Veo 3.1 | ~$0.75 | primary |
| Sora 2 | ~$1.20 | premium hero |
| Kling 2.1 | ~$0.30 | Asian subject |
| Runway Gen-4 | ~$0.60 | fallback |
| Hailuo | ~$0.10 | b-roll |
| Hyperframe (self-host) | ~$0.02 | motion graphic |

---

## 4. Thai TTS (Voiceover)

**สำคัญสุด** — เสียงพูดไทยเพราะ/ไม่เพี้ยน = ผ่านหรือไม่ผ่านวิดีโอ

### 4.1 ตัวเลือกอันดับ 1 — ElevenLabs Multilingual v2 + Turbo v2.5
- Thai voice library ขยายมาก ปี 2025-26
- รองรับ voice cloning (จับเสียงคนไทยจริงได้ 1 นาที sample → clone)
- Emotion / pacing control ดี
- **Cost**: ~$0.18/นาที (Creator plan)
- **Use**: หลัก — narrator + character

### 4.2 ตัวเลือกอันดับ 2 — Botnoi Voice (ไทย)
- **Thai-native** — accent / สำเนียงไทยเป็นธรรมชาติที่สุดในตลาด
- เลือกได้หลายตัวละคร / ภูมิภาค (อีสาน, เหนือ, ใต้ ใช้ในการเจาะ persona)
- Latency ดี, cost ต่ำ
- **Use**: narrator สำหรับ niche ที่ต้องการ "เสียงไทยแท้" / persona regional

### 4.3 ตัวเลือกเสริม
- **Microsoft Azure Neural TTS Thai** (Premwadee, Niwat) — solid, enterprise SLA
- **Google Cloud TTS Thai** — ใช้เป็น fallback
- **NECTEC Vaja** — รัฐบาลไทย, ฟรี, แต่ robotic — ไม่แนะนำ production

### 4.4 ห้ามใช้
- ❌ OpenAI TTS — Thai accent เพี้ยน (อ่านเหมือนฝรั่งพูดไทย)
- ❌ Chatterbox / Bark — ภาษาไทยพัง

### 4.5 Workflow
```
Screenwriter → script TH + emotion tags + emphasis marks
Sound Designer → ElevenLabs voice_id + style settings
TTS adapter:
  primary:    ElevenLabs (default)
  premium:    ElevenLabs cloned voice (สำหรับ brand)
  Thai-native niche: Botnoi Voice
  fallback:   Azure TTS
```

### 4.6 Voice Cloning Strategy (Phase 2+)
- จ้าง voice actor ไทยมือดี 5 คน → record 30 นาที each → clone ผ่าน ElevenLabs Professional Voice Cloning
- Wiki track ว่า voice ไหนได้ CTR สูงสุดต่อ niche
- ใช้ voice เดียวกันใน campaign ครอบครัวเดียวกัน → brand recall

---

## 5. Thai ASR (สำหรับ Editor — filler cut, subtitle)

### 5.1 ตัวเลือกอันดับ 1 — Whisper-large-v3 (self-hosted)
- Thai accuracy WER ~ 15% บน clean audio
- word-level timestamp ผ่าน WhisperX
- self-host บน A10 GPU 1 ใบ
- **Use**: ทุก raw clip → transcript + timestamp

### 5.2 ตัวเลือกอันดับ 2 — Gowajee / Thonburian Whisper
- Whisper fine-tuned บน Thai dataset (Pathumma / Common Voice TH)
- WER ดีกว่า base ~ 3-5 percentage points สำหรับ Thai
- **Use**: เมื่อ niche ที่ต้องการ accuracy สูง (legal/medical-adjacent — แต่ระบบเราหลีกเลี่ยงอยู่แล้ว)

### 5.3 ตัวเลือกเสริม — Azure Speech-to-Text Thai
- Cloud, สูง SLA, จ่ายเป็นรายนาที
- **Use**: fallback ตอน self-host ล่ม

---

## 6. Lipsync (เฉพาะกรณี on-camera narrator)

### 6.1 ตัวเลือกอันดับ 1 — Sync.so (Sync Labs)
- ดีที่สุด ณ ตอนนี้สำหรับ Thai mouth shape (ภาษาไทยมี syllable structure ต่างจากอังกฤษ → ปากต่าง)
- Cost: ~$0.12/วินาที

### 6.2 ตัวเลือกอันดับ 2 — Hedra (character.ai)
- เร็ว, full-character generation จาก audio + portrait
- **Use**: AI presenter virtual

### 6.3 ตัวเลือกอันดับ 3 — LatentSync (open source, self-host)
- ใช้ฟรี, คุณภาพรองลงมา
- **Use**: เมื่อ budget ต่ำ

---

## 7. Music / Sound Design

### 7.1 ตัวเลือกอันดับ 1 — Suno v4.5 / Udio v1.5
- Generate music ตามอารมณ์ พร้อม license commercial use
- ภาษาไทย (มี Thai vocal): Suno ทำได้ดีกว่า
- **Use**: background music ที่ unique ไม่ชน claim ลิขสิทธิ์

### 7.2 ทางเลือก Licensed
- **Epidemic Sound** / **Artlist** — license library, copyright-safe ทุก platform
- **Use**: หลัก สำหรับ commercial — กัน copyright strike

### 7.3 SFX
- **ElevenLabs Sound Effects v2** — prompt → SFX, ภาษาอังกฤษ
- **Freesound.org** — Creative Commons

---

## 8. Translation / Localization (เผื่อขยาย market)

แม้ scope หลักไทยเท่านั้น แต่ Phase 3 อาจขยายเป็น SEA — เก็บ stack ไว้
- **Claude Opus 4.7** — translation ที่ดีที่สุดสำหรับไทย → ภาษาอื่น (รักษา nuance)
- **DeepL** — fallback สำหรับ language pair ที่ Claude อ่อน (vi/id)
- **NLLB-200** — บนเครื่อง, ฟรี, สำหรับ rough draft

---

## 9. Quality Gate ภาษาไทย (Critical)

ทุก video output ต้องผ่าน 4 check ก่อน publish:

| Check | Tool | Pass criteria |
|---|---|---|
| **Script natural-Thai score** | Typhoon 2 verifier prompt | ≥ 8/10 |
| **Pronunciation review** | Whisper round-trip — TTS → ASR → diff vs. original | WER ≤ 3% |
| **Thai text rendering ในรูป** | OCR (PaddleOCR Thai) ทุก scene | ตัวอักษรไทยตรง ≥ 99% |
| **Cultural appropriateness** | Critic agent (Opus) | no red flag |

ถ้า fail check ใด → Editor re-run จุดนั้น (ไม่ใช่ทั้ง pipeline)

---

## 10. สรุปตาราง "ใช้อะไร" สำหรับงานไทย

| งาน | Primary | Backup | หมายเหตุ |
|---|---|---|---|
| Script / dialogue / caption | Claude Opus 4.7 + Sonnet 4.6 | Typhoon 2 verifier | Sonnet pol → Typhoon validate |
| Image (พื้น) | Flux 1.1 Pro Ultra | Imagen 4 / Midjourney v7 | ห้าม render Thai text |
| Image (Thai people) | Imagen 4 | Midjourney v7 | |
| Video (general) | Veo 3.1 | Sora 2 / Runway Gen-4 | prompt EN, audio off |
| Video (Asian face) | Kling 2.1 | Veo 3.1 | |
| Video (b-roll cheap) | Hailuo | Pika 2.0 | |
| Motion graphic / title | Hyperframe (HTML render) | Remotion | self-host |
| TTS Thai narrator | ElevenLabs Multilingual v2 | Botnoi Voice / Azure TTS | Phase 2: cloned voices |
| TTS Thai niche/regional | Botnoi Voice | ElevenLabs | อีสาน/เหนือ/ใต้ |
| ASR Thai | Whisper-large-v3 (self) | Gowajee / Azure | word timestamps |
| Lipsync | Sync.so | Hedra / LatentSync | เฉพาะ on-camera |
| Music | Suno v4.5 + Epidemic Sound | Udio | license-safe |
| SFX | ElevenLabs SFX v2 | Freesound | |

---

## 11. Cost Update (Per Video, Thai-optimized)

| Item | USD |
|---|---|
| Scout + Strategist + Writers' Room (LLM) | 1.20 |
| Editor agent (LLM) | 0.13 |
| Typhoon verifier (self-host) | 0.01 |
| 4× Flux/Imagen image | 0.20 |
| 5× Veo 3.1 clip | 3.75 |
| 1× Kling clip (subject) | 0.30 |
| ElevenLabs TTS (60s) | 0.18 |
| Whisper ASR (self) | 0.02 |
| Suno music | 0.10 |
| Hyperframe overlay render | 0.05 |
| Compose + storage | 0.05 |
| Publish + analytics | ~0.05 |
| **Total** | **≈ $6.04/video** |

> Phase 1 target $2.87 อ้างอิงตอนใช้ Veo เป็นหลัก scene เดียว — production จริง 6 scene พร้อม premium quality อยู่ที่ ~$6 → คุ้มเพราะ CTR คาดหวัง 2-4%

### 11.1 ลด cost ได้ที่ไหน
- ใช้ Hailuo แทน Veo สำหรับ b-roll → ลด ~$2/video
- Suno → Epidemic Sound license (flat fee) → ลด per-call
- Phase 3 self-host video gen (เช่น Open-Sora 2.0 เมื่อพร้อม) → ลด 60%

---

## 12. Open Questions (Thai-specific)
1. **Typhoon 2 vs Typhoon 3** (ถ้าออก) — เมื่อใดควรอัพ?
2. **Voice cloning legal** — clone เสียงคนไทยต้อง consent form แบบไหน, GDPR/PDPA?
3. **คำหยาบ / มุกล่อแหลม** — บรรทัดแดงอยู่ที่ไหน? Critic (Opus) ตัดสิน หรือมี static rule?
4. **ภาษาภูมิภาค** (อีสาน, เหนือ, ใต้) — Phase 1 ใช้กลางอย่างเดียว หรือทดลอง?
5. **Lipsync vs no-lipsync** — เริ่มจาก voice-over-only (no face) ลด complexity ดีกว่าไหม?
