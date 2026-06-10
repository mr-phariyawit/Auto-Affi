# Auto-Affi Rights and Business Affairs Principle

Date: 2026-06-04

Purpose: convert rights, claims, affiliate, disclosure, and platform research into hard workflow rules.

## Core Rule

> Review-ready is never publish-ready. Public posting requires rights, claims, affiliate tracking, disclosure, and platform path to pass.

## Required Artifacts

Every run must include:

```text
product_truth.json
claim_ledger.json
rights_tracker.json
ai_usage_log.json
publish/tiktok_publish_packet.json
publish/shopee_affiliate_link_request.json
```

Premium/client work also requires:

```text
brand_brief.json
business_affairs_review.json
release_tracker.json
```

## Hard Gates

- No unsupported claim in script, caption, visual implication, price text, or CTA.
- No fake certifications, fake badges, fake Thai legal text, fake platform UI, or fake seller claims.
- No third-party video/music/voice/likeness/font/source footage without documented rights.
- No voice clone, face swap, digital replica, or Soul ID use without explicit consent and scope.
- No affiliate URL generation except through approved Shopee Affiliate API/dashboard or user-controlled official path.
- No scraping private Shopee pages or using automation to bypass platform controls.
- No public publish without caption/platform commercial-content disclosure and AI label where required.
- No public publish when product price/SKU/status is stale or unchecked.

## Rights Tracker Minimum Fields

```text
asset_id
asset_type
owner
source_url_or_path
license_or_release
territory
term
media
ai_training_allowed
voice_or_likeness_scope
expiry
publish_status
notes
```

## Claim Ledger Minimum Fields

```text
claim_id
claim_text_th
claim_type
where_used
evidence_url_or_asset
risk_level
approval_status
forbidden_adjacent_claims
legal_notes
```

## Publish Packet Must Prove

- exact final MP4 path;
- product URL and affiliate URL/subIds;
- caption and hashtags;
- disclosure settings;
- AI label requirement;
- current price/SKU recheck;
- approval owner and timestamp;
- platform/account/path;
- post-publish monitor plan.

## Stop Conditions

Use `black` severity and involve counsel or user confirmation when:

- regulated product/category;
- paid client production with contracts;
- talent likeness, voice clone, minors, or releases;
- union/agency/talent-packaging issue;
- unclear source footage or music rights;
- platform ToS uncertainty that affects account risk.
