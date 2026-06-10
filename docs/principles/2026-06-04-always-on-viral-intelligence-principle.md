# Auto-Affi Always-On Viral Intelligence Principle

Date: 2026-06-04

## Core Principle

> The intelligence team may watch news and social media all the time, but production starts only after Marketing selects a product or product angle into a collection, Research validates it, and the idea passes ethics, claim, and policy gates.

The goal is not to exploit every viral event. The goal is to find fast social demand windows, let Marketing curate product opportunities, and let Research prove which opportunities are useful, low-risk, and production-ready.

Detailed 24/7 subagent operating blueprint:

- `docs/research/auto-affi-24-7-subagent-team-blueprint-th-2026-06-04.md`

## Operating Model

Maintain two separate data layers:

- `data/viral_signal_intelligence.csv`: raw and semi-processed news/social signals.
- `data/marketing_collection.csv`: Marketing-selected product ideas, angles, and collection priorities for Research to validate.
- `data/product_intelligence_candidates.csv`: product candidates that passed mapping, claim, ethics, and policy checks.

For the 24/7 sidecar, also maintain:

- `data/source_registry.csv`
- `data/signal_observations.csv`
- `data/signal_clusters.csv`
- `data/subagent_ops_queue.csv`
- `data/human_review_inbox.csv`
- `data/product_need_map.csv`
- `data/claim_ledger_index.csv`
- `data/run_registry.csv`
- `data/post_publish_results.csv`

A viral signal is not a product candidate until it passes human-readable review gates.

A marketing collection row is not a product candidate. It is a request for Research to validate product truth, price/SKU, claims, risk, evidence, and Shopee availability.

Repeated viral sightings are useful. Do not treat every repeat as trash. Avoid exact duplicate raw rows, but preserve repeat observations, refreshed cluster velocity, repeated source/platform evidence, and Marketing notes because repeated attention can be a product-opportunity signal.

Ownership:

- Marketing owns selection, buyer angle, hook hypothesis, priority, and collection status.
- Research owns source validation, product truth, Shopee evidence, claim limits, and candidate readiness.
- Safety/Compliance can block either Marketing collection rows or Research candidates.

Use `fail-closed`: if source, rights, claim, likeness, disclosure, or sensitive-event information is missing, route to amber/red review instead of auto-generating content.

## Always-On Teams

1. **News Desk**
   - Watches Thai news, official weather/government updates, entertainment news, consumer issues, commuting, lifestyle, tech, and seasonal events.
   - Records source URL, timestamp, summary, and confidence.

2. **Social Radar**
   - Watches TikTok, Facebook, Instagram, YouTube Shorts, X, Pantip, Google Search/Trends, and creator chatter where available.
   - Records topic velocity, repeated keywords, public sentiment, and observed engagement.

3. **Entertainment and Lifestyle Desk**
   - Tracks celebrity, beauty, sleep, fitness, dating, parenting, fashion, travel, and everyday-life trends.
   - Converts celebrity attention into general audience needs without using the celebrity as endorsement.

4. **Marketing Collection Desk**
   - Reviews trend clusters, direct product ideas, seasonal calendars, and performance learnings.
   - Selects product ideas into `data/marketing_collection.csv`.
   - Writes the buyer archetype, marketing angle, hook hypothesis, priority, and expected content format.
   - Cannot approve product claims or bypass Research.

5. **Ethics and Brand Safety Desk**
   - Screens for violence, death, illness, minors, personal humiliation, doxxing, unverified allegations, political sensitivity, and active legal cases.
   - Can mark a signal as `red_no_product_mapping`.

6. **Product Research Desk**
   - Takes Marketing collection rows and researches product truth, Shopee evidence, price/SKU, claim boundaries, and affiliate feasibility.
   - Writes validated rows into `data/product_intelligence_candidates.csv`.
   - Rejects or sends back weak ideas instead of forcing a product candidate.

7. **Product Mapping Desk**
   - Maps safe signals and Marketing collection ideas to product needs, Shopee search queries, and low-risk candidate categories.
   - Does not approve medical, performance, or safety claims.

8. **Claims and Compliance Desk**
   - Checks product category risk, platform restrictions, FDA/health-ad claim risk, disclosure, AI label, and affiliate rules.
   - Health, vitamin, supplement, bruise, medicine, and cosmetic-adjacent products require stricter gates.

9. **Performance Desk**
   - Tracks hook potential, trend age, demand window, urgency score, expected conversion path, and post-publish learning.

## Source Priority

1. Official or primary sources for factual signals:
   - TMD, PRD, official agencies, verified announcements, original platform posts when accessible.
2. Thai news and trusted media:
   - Used for timing, public interest, and social framing.
3. Social platforms:
   - Used for virality, sentiment, memes, comment themes, and consumer pain signals.
4. Search and ecommerce:
   - Google, Shopee search/listings, product pages, image refs, price/SKU availability.

Use foreign sources only as context unless the target audience is international.

## Signal Color Rules

`green`: safe lifestyle/weather/commute/household/beauty/fashion/tech signals with low personal harm.

`amber`: celebrity/lifestyle drama, relationship topics, health-adjacent topics, financial stress, conflict without physical harm, or any signal involving a public figure.

`red`: death, active violence, injury, domestic abuse, minors, self-harm, serious illness, public humiliation, doxxing, unverified accusations, active criminal/legal cases, or content where a real person is visibly suffering.

Red signals cannot become product prompts. They may become broad social learning only after de-identification and human approval.

## Product Mapping Rules

- Map from the audience need, not from a person's pain.
- Do not use the real person's name, image, quote, likeness, scandal, injury, or private details in an ad.
- Do not imply a product treats, cures, prevents, or fixes health conditions unless the claim is legally supported and approved for the category.
- Do not turn violence or abuse into a shopping hook.
- Prefer low-risk everyday products: commute, rain, storage, cleaning, sleep comfort, beauty routine, organization, phone accessories, home safety, creator tools.
- Health-adjacent products require evidence, label review, platform policy review, and human approval.

## Example Mapping

Celebrity looks tired after a late event:

- Unsafe framing: "Use this because this celebrity has dark circles."
- Safer signal: many viewers discuss late nights, tired eyes, and next-day routines.
- Candidate categories: cooling eye mask, concealer, gentle eye cream, sleep mask.
- Claim limits: no medical claim, no guaranteed dark-circle reduction, no celebrity endorsement.

Domestic dispute or violence news:

- Unsafe framing: sell bruise-reduction cream from a person's injury.
- Safer handling: mark `red_no_product_mapping`.
- Possible later broad topic only with human approval: personal safety, emergency preparedness, first-aid awareness, support resources.
- Hard rule: do not monetize a victim's injury or imply treatment claims from a news incident.

## Mandatory Fields

Every captured signal should include:

```text
signal_id
captured_at
platform
source_type
source_url
topic
summary_th
people_involved_type
harm_level
verification_status
virality_evidence
engagement_snapshot
trend_age_hours
demand_window
audience_need
candidate_product_category
candidate_query
ethics_color
policy_risk
claim_risk
human_review_required
product_mapping_status
notes_th
```

## External Policy Notes Checked On 2026-06-04

- TikTok's branded content support page says creators promoting a brand, product, or service should use content disclosure settings and follow TikTok policies and applicable laws: https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/promoting-a-brand-product-or-service
- TikTok says realistic AI-generated images, audio, or video should be labeled so viewers understand the content context: https://newsroom.tiktok.com/en-us/new-labels-for-disclosing-ai-generated-content
- TikTok branded content policy includes affiliate commission as branded content and restricts or prohibits sensitive product categories in branded content: https://www.tiktok.com/legal/page/global/bc-policy/ja
- Thai FDA supplement-ad guidance warns against advertising supplements as necessary or claiming disease prevention/treatment effects: https://exfood.fda.moph.go.th/law/data/announ_fda/054supplement309.pdf

Policies change. Recheck platform and regulator pages before publishing health-adjacent, celebrity-adjacent, or sensitive-topic content.

## Human Gate

Human review is mandatory when:

- ethics color is `amber` or `red`;
- a real person, public figure, victim, child, or private individual is involved;
- the product category is health, supplement, cosmetic treatment, medicine, safety, finance, legal, or adult;
- the content uses AI-generated realistic people, voices, or scenes;
- the angle could look like it profits from harm, scandal, illness, or humiliation.

No team can self-approve an amber/red signal.
