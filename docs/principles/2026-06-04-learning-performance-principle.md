# Auto-Affi Learning and Performance Principle

Date: 2026-06-04

Purpose: make every run feed the next decision. A workflow is not complete until results, failures, costs, and creative learnings are captured.

## Core Rule

> A clip is not done when it renders. It is done when the system records what happened, why, what it cost, what passed, what failed, and what should change next.

## Required Artifacts

Every run must include:

```text
metrics/learning_log.md
metrics/performance_snapshot.json
metrics/model_scorecard.md
metrics/prompt_scorecard.md
metrics/prompt_council_failure_log.md
metrics/failure_taxonomy.json
```

Every run closeout must also record:

```text
successes_promoted
failures_found
user_caught_failures
workflow_rules_added
provider_failures
credit_waste_prevented_or_caused
next_run_blockers
```

When published or manually uploaded:

```text
publish/dispatch_log.jsonl
metrics/post_publish_results.jsonl
```

## Minimum Metrics

Before publish:

```text
route_used
provider_job_ids
cost_estimate
cost_actual
render_duration_sec
cleanroom_result
prompt_council_decision
brain_activity_score
approval_status
publish_blockers
failure_categories_seen
regeneration_decisions
physics_logic_failures
reality_mode
fantasy_rule_if_any
```

After publish:

```text
platform
account
post_url_or_id
affiliate_sub_ids
views
watch_time_or_retention
clicks
orders
commission
refunds_or_cancellations
comments_confusion
disclosure_issues
ROI
post_publish_actions
```

## Learning Decisions

| Result | Action |
| --- | --- |
| High approval, high CTR, low conversion | Improve product/offer fit |
| High virality, product drift | Keep pattern but tighten product identity gate |
| Low approval, strong product truth | Improve treatment/shot craft |
| Strong conversion, weak craft score | Build fast affiliate version, not premium film |
| Repeated route succeeds 3 times | Promote route into a custom skill/template |
| Repeated failure by route/model | Lower route priority or add constraint |
| Hook score below target | Revise 0-3s prompt and test a cutdown |
| Identity/color drift repeats twice in one run | Add anchor constraints and stop long-batch generation until dailies QC passes |
| User catches wardrobe, bag, product, location, or environment drift after QA passed | Add machine-check or independent audit seat before the next comparable generation |
| Caption/subtitle differs from voiceover | Add exact caption-vs-VO report comparison before final render |
| Provider transient failure occurs after partial success | Add retry with cached segment reuse; do not rerun completed paid segments |
| Voice sounds sleepy or off-brand | Run labeled voice audition before final voice lock |
| Generated product carries unintended logo/UI/text | Create clean no-text references or deterministic post assets before regenerating |
| Script artifact names collide across versions | Version segment folders, concat lists, reports, and output names |
| Non-Seedance video model appears cheaper or easier | Do not switch; rewrite/split the shot for Seedance 2.0 or escalate |
| Realistic storyboard fails physics/logic review | Fix storyboard blocking, object contact, water behavior, gravity, or cause/effect before generation |
| Fantasy storyboard fails physics/logic review | Add a written fantasy rule and Marketing reason, or downgrade to realistic |

## Hard Gates

- No run may be archived without `metrics/learning_log.md`.
- No run may be archived without the closeout fields listed above.
- Published runs must record dispatch path and subIds.
- Brain Activity or equivalent scoring must record scope. If a tool only accepts short videos, score a declared hook sample and say so.
- Do not treat virality score as approval; combine with product truth, craft QC, rights, and human approval.
- Any post-publish compliance issue must create a blocker in the next run's state.
- No multi-shot AI video run may close without recording identity drift, object/color drift, audio surprises, duration mismatch, storyboard gaps, naming collisions, and regenerate decisions when they occurred.
- No multi-shot AI video run may close without recording physics/logic failures, reality mode, and fantasy-rule gaps when they occurred.
- If a user-caught failure bypassed internal QA, the next comparable run must include a new automated check, stronger gate, or independent reviewer seat before generation or final render.

Detailed upgrade: `/Users/phariyawit.jiap/Documents/Auto-Affi/docs/principles/2026-06-05-main-workflow-learning-upgrade.md`.
