# Domain: Thai Market, Beauty Niche, 9:16 Format

> Source: SPEC.md sections 1.1, 3.1-3.6, 10.1-10.2, 13
> Last synced: 2026-05-13
> Purpose: Thai-specific conventions, regulatory requirements, platform
> norms, and cultural awareness that every content-producing agent needs.

## Market: Thailand -- Shopee Affiliate

- **Platform**: Shopee (primary e-commerce)
- **Revenue**: Affiliate commission via subId-tagged deep links
- **Link tracking**: System-owned link-shortener for cross-platform attribution
- **API**: Shopee Affiliate Open API + Shopee Open Platform
- **Rate limits**: 100 req/min with token bucket

## Niche: Beauty Products (Phase 1)

- Phase 1 is Beauty-only. Single niche focus for learning loop quality.
- Multi-niche scaling deferred to Phase 3.
- Beauty niche implications:
  - Visual-heavy content (product close-ups, before/after, texture shots)
  - Regulated claims: no medical claims, no "guaranteed" results
  - High commission rates in beauty category on Shopee TH
  - Seasonal peaks: mega-sales (11.11, 12.12), Songkran, New Year

## Content Format: 9:16 Vertical Video

- **Aspect**: 9:16 (portrait/vertical)
- **Resolution**: 1080x1920
- **Frame rate**: 30fps
- **Duration**: <= 60 seconds
- **File size**: <= 100MB
- **Codec**: H.264
- **Platforms**: IG Reels (Phase 1), FB Reels + YT Shorts (Phase 2+)

## Thai Language Requirements

- **All content in native Thai** -- no transliteration, no English-primary
- **Thai filler words to auto-remove**: ["eee/เออ", "eum/อืม", "a/อะ", "aa/อ่า"]
- **Voice profile**: Thai female, energetic-confidant tone (default from SPEC 6.2)
- **TTS engines with Thai support**: ElevenLabs Multilingual v2 (primary), Azure TTS (fallback)
- **ASR**: Whisper-large-v3 with Thai+English code-switch support (WhisperX for word-level timestamps)
- **Subtitles**: Auto-burned, Thai text, style from reference clip

## Regulatory / Compliance (Thailand)

### NBTC (กสทช.) Requirements
- Mandatory disclosure: `#โฆษณา` (advertising) and/or `#affiliate`
- Must appear in caption/first-comment on every published post

### Shopee ToS
- No misrepresentation of commission
- No prohibited keyword usage
- Monthly ToS review (tracked as operational cadence)

### Platform-Specific Rules
- **FB/IG**: Branded content disclosure, no engagement bait
- **YouTube**: YPP-friendly captions, no copyrighted audio without license

### Content Safety
- Prohibited categories: cigarettes, weapons, unregulated supplements
- Medical/financial claims: hard-blocked by Claim Auditor
- NSFW: classifier on every generated frame sample
- Music: licensed library only + fingerprint check pre-publish

## Mega-Sale Calendar Awareness

Thai e-commerce has predictable traffic spikes. Content strategy should
align with these events for maximum affiliate conversion:

- **Monthly doubles**: 1.1, 2.2, 3.3, ... 12.12 (Shopee mega-sales)
- **Valentine's Day** (Feb 14): beauty gift surge (lipstick, skincare sets, fragrance)
- **Songkran** (mid-April): beauty/skincare surge (sunscreen, waterproof makeup)
- **Mid-Year Sale** (June/July): Shopee's major mid-year event
- **Mother's Day TH** (Aug 12): major beauty gifting occasion in Thailand
- **11.11**: Biggest single-day sale in SEA e-commerce
- **12.12**: Year-end mega-sale
- **New Year / Christmas**: gifting season (beauty sets, gift boxes)
- **PayDay patterns** (25th-end of month): general spending surge, align product pushes

The Strategist and Scout agents should increase discovery cadence and
adjust product selection 5-7 days before major sale events.
