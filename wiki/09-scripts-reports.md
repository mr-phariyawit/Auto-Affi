# 09 — Scripts, Tools & Reports

## Scripts ([`scripts/`](../scripts/))

### `social_media_scanner.py` — Trend Scanner (Intel engine)
Scan viral signals จาก Google Trends RSS (default), YouTube Data API + Reddit API (optional), manual CSV imports — TikTok ยัง access-gated (บันทึกเป็น blocked task) · classify ethics green/amber/red · map product category · เขียน 7 intel CSVs ([data registry](04a-data-registry.md)) + optional daily report

```bash
python3 scripts/social_media_scanner.py --geo TH --geo US --limit 20 --write-marketing --report
```
Env (optional): `YOUTUBE_API_KEY`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`

### `validate_caption_voice_sync.py` — Caption/VO Sync Gate (Compliance Gate #6)
เทียบ caption ใน HyperFrames `index.html` กับ voice report JSON — text mismatch หรือ count mismatch = exit 1 = **block final render**

```bash
python3 scripts/validate_caption_voice_sync.py \
  --html variants/v001/index.html \
  --voice-report jobs/voice_report.json \
  --output-json variants/v001/caption_sync_validation.json
```


```bash
python3 scripts/kie_market_catalog.py --out-json docs/research/kie_market_models_2026-06-03.json \
  --out-csv docs/research/kie_market_models_2026-06-03.csv --max-workers 16
```

อ่าน key+secret จาก macOS clipboard (`pbpaste`) → validate format → เขียน `.env` atomic (chmod 600, preserve `KIE_API_KEY` เดิม) → ได้ `HF_API_KEY`, `HF_API_ID`, `HF_API_SECRET`, `HF_KEY`

```bash
```
⚠️ บทเรียน: clipboard เคยมี URL แทน key → ตรวจ format ก่อนเสมอ (Compliance Gate #5)

## Reports ([`reports/`](../reports/))

| Report | สรุป |
|---|---|
| `ad_hoc_scout_2026-06-04.md` | Scout 5 ไอเดียสินค้าจากสัญญาณฝน/Pride/เปิดเทอม — seeded เข้า marketing_collection, ห้าม generate จนกว่า Research validate |
| `daily_digest_2026-06-05.md` | Digest รอบแรก: 24 signals (16 green / 7 amber / 1 red), 8 clusters, 9 open human reviews, top 3 candidates — blocker: ยังไม่มี affiliate sub-IDs |
| `social_scan_2026-06-05.md` | Output จาก scanner: 20 items TH+US, new signals = 0 (ซ้ำทั้งหมด), amber ครอง TH top (politics/gold/court), green = weather/sports |

## Per-Run Scripts

แต่ละ run folder มี `scripts/` ของตัวเอง (เช่น `kie_generate_scene_voice_30s.py`, `build_30s_kie_production_clip.py`) — เป็น run-specific ไม่ใช่ shared tooling ดูตัวอย่างใน [runs/2026-06-03-silicone-shoe-covers.md](runs/2026-06-03-silicone-shoe-covers.md)

---
[← Runs](08-runs.md) | [HOME](HOME.md) | [Ops Guide →](10-ops-guide.md)
