# Auto-Affi Daily Digest - 2026-06-05

This is the first digest run in this workspace. The current cycle is dominated by rainy-season commuter needs, with the safest commercial path concentrated in utility products that already have live Shopee price floors.

## Snapshot
- `source_registry.csv`: 4 sources, with Shopee, TMD, YouTube, and TikTok coverage split across official/public and manual-review access.
- `viral_signal_intelligence.csv`: 24 signals total, with 16 green, 7 amber, and 1 red.
- `signal_clusters.csv`: 8 clusters total, with 3 marketing-ready, 4 needing human review, and 1 blocked.
- `product_need_map.csv`: 8 mapped needs total, with 3 query-ready, 4 needing human review, and 1 red no-mapping case.
- `marketing_collection.csv`: 8 selected items total, with 7 selected for research and 1 blocked.
- `product_intelligence_candidates.csv`: 9 candidate rows, including 3 clearly ready-for-normalizer or candidate items that are safe to keep in the active shortlist.
- `subagent_ops_queue.csv`: 19 tasks total, with 6 completed, 11 captured, 1 queued, and 1 blocked.
- `human_review_inbox.csv`: 9 open reviews, all still undecided.
- `claim_ledger_index.csv`: 8 claims indexed, with 6 approved and 2 still review-required.
- `run_registry.csv`: empty.
- `post_publish_results.csv`: empty.

## Top Safe Marketing Opportunities
- Backpack rain cover: green and marketing-ready, backed by fresh TMD rain coverage plus live Shopee price-floor checks.
- Phone waterproof pouch: green and marketing-ready, with today’s low-price floor and a simple splash/rain protection demo path.
- Back-to-school rain kit: green and marketing-ready, with strong open-term timing and a clean utility angle for parents.
- Hanky House microfiber towel: ready for normalization, with a strong commuter-drying story, but it is secondary to the three rain-protection items above.

## Amber And Red Items Awaiting Human Review
- `example-celebrity-late-night-tired-eyes`: amber. Keep as a generalized need only if a human explicitly approves the product and claim framing.
- `tmd-southwest-coast-heavy-rain-20260604`: amber. Travel-prep only; do not fearmonger.
- `review-dry-bag-flood-signal-20260604`: amber. Travel-prep only; do not use flood imagery.
- `review-mosquito-home-claim-20260604`: amber. Home-comfort only; no disease or prevention claims.
- `review-pride-event-comfort-20260604`: amber. Respectful festival-comfort only; no likeness or identity gimmick.
- `review-pride-month-festivals-20260604`: amber. Same restraint as above.
- `review-thaipbs-pride-bangkok-20260604`: amber. Same restraint as above.
- `example-domestic-violence-injury`: red. Do not map to a product; archive as social learning only.

## Research Blockers
- `task-review-eye-comfort-20260604` is still queued and needs a human decision before any normalization.
- `product_intelligence_candidates.csv` has a few partially malformed rows with shifted or blank fields, so downstream automation should not rely on them without re-normalization.
- No run history or post-publish feedback exists yet in `run_registry.csv` or `post_publish_results.csv`, so there is no learning loop from live publish performance.
- No affiliate shortlinks or sub-IDs are recorded yet for the active shortlist, so even safe candidates are still pre-publish only.

## Source And Access Issues
- `tiktok_research_api` is disabled in `source_registry.csv`; TikTok work must stay on manual review and must not become continuous scraping.
- `shopee_product_page` is allowed with caution, but price, SKU, and stock must be rechecked before publish.
- YouTube and TMD sources are official/public, but the report should still treat their timestamps as freshness-sensitive.

## Stale Price Or SKU Checks
- Recheck the older `2026-06-03` umbrella and shoe-cover candidates before reusing them; they are still useful signals, but their price/SKU state should be treated as stale relative to today’s fresh crawler pass.
- Revalidate the `2026-06-04` travel dry bag candidate before reuse if it stays in the working set.
- Fresh live price-floor checks are already present for backpack rain cover, phone waterproof pouch, and the back-to-school rain kit, so those three are the least stale commercial options.

## Candidate Shortlist
- `rain-commute-bag-cover-20260604`: strongest safe candidate and best fit for immediate production work.
- `phone-waterproof-pouch-20260604`: strong second candidate with low-friction demo value and fresh price-floor evidence.
- `school-rain-kit-20260604`: strong third candidate with clear seasonal timing and a simple parent-friendly utility story.
- `hanky-dry-towel-20260604`: viable secondary candidate if the team wants a non-rain-protection fallback.
- `rain-travel-dry-bag-20260604`: keep only as an amber fallback until a human confirms the travel-prep framing.

## Recommended Human Decisions
- Reject the red violence mapping and keep it archived.
- Approve travel-prep framing only for the dry bag and south-west coast weather signals.
- Approve respectful event-comfort framing only for the Pride-related rows.
- Approve the limited home-comfort claim for the mosquito-screen repair row.
- Make an explicit product-and-claim decision on the eye-comfort example before normalization.
- Prioritize the three green rain-season utility products for the next production pass.
