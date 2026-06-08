# Auto-Affi Model Routing Principle

Date: 2026-06-04


## Core Rule

> Skill chooses the workflow. Model renders the media. Human QA approves the truth.


## June 2026 Credit Burn-Down Policy



## Env-First Provider Access

Production provider keys are already provisioned in the project `.env`.

- Load `.env` before creating `route_decision.json` and before every provider call.
- Verify only required variable-name presence, such as `HF_KEY`, `HF_API_KEY` or project alias `HF_API_ID`, `HF_API_SECRET`, `KIE_API_KEY`, `OPENAI_API_KEY`, `OPENROUTE_API_KEY`, `GOOGLE_API_KEY`, or `YOUTUBE_API_KEY` when the route uses them.
- Do not print, paste, commit, or write secret values into run artifacts.
- Clipboard keys are not part of the normal production route and are allowed only for an explicit one-off manual override.
- If an env var is missing, block that provider route and record only the missing variable name.

## Seedance 2.0 Only Video Policy

For AI video scenes and clips, the workflow is now locked to:

```text
seedance_2_0
```

Rules:

- Use `seedance_2_0` for every generated video shot, scene, insert, transition, memory beat, product B-roll, and hero/finale moment.
- Do not use Kling, Wan, Veo, Cinema Studio, Marketing Studio Video, Minimax, or any other video model for scene generation.
- Do not switch models between scenes for cost, texture, weather, insert, or hero-shot reasons.
- If `seedance_2_0` is unavailable, blocked, or fails quality after constrained retries, stop visual video generation and escalate; do not silently fallback to another video model.
- Non-video tools such as post-production, reframe, cutout, upscale after visual lock, scoring, captions, and voice may still be routed through their approved utilities when they do not generate new scene video.

## Nano Banana Pro Static Text/Image Lock

For the next production rounds, any model-generated static image that intentionally contains text, typography, title-card copy, thumbnail copy, package-label mockup, or layout text is locked to:

```text
nano_banana_2
```

Customer-facing name:

```text
Nano Banana Pro
```

Rules:

- Use `nano_banana_2` only for approved static text/image generation, not video scene generation.
- Do not use GPT Image, Seedream, Flux, Marketing Studio Image, or any other image model for intentional generated text/typography while this lock is active.
- Thai captions, price, disclosure, and CTA that appear on the final video timeline should still be post-composited in HyperFrames or another deterministic editor whenever possible.
- If a Nano Banana Pro text image is used, run OCR/spelling/claim review before it can enter a final asset.
- If Nano Banana Pro cannot render readable/compliant text after constrained retries, switch to deterministic post-composition or stop; do not silently fallback to another image-text model.

## Required Artifact

Every run must include:

```text
route_decision.json
```

Required fields:

```text
run_id
variant_id
profile
primary_route
secondary_route
selected_model_or_tool
route_reason
input_assets
prompt_council_review_path
expected_outputs
failure_triggers
fallback_ladder
provider_job_ids
durable_local_outputs
cost_estimate
decision_owner
decision_status
env_ready
required_env_vars
missing_env_vars
```

For multi-shot AI video, also record:

```text
production_pass
model_lock_policy
shot_model_routing
final_pass_primary_model
identity_sensitive_shots
insert_texture_shots
```

## Routing Ladder

| --- | --- | --- |
| Product UGC/review video | `seedance_2_0` only | no visual-video fallback |
| Cinematic B-roll | `seedance_2_0` only | no visual-video fallback |
| Premium hero moment | `seedance_2_0` only | no visual-video fallback |
| Static text image / title card / thumbnail text | `nano_banana_2` only | deterministic post-composition or stop |
| Product/keyframe still without intentional text | `nano_banana_2`, `gpt_image_2`, `cinematic_studio_2_5` | Imagen, Seedream, Flux |
| Product cleanup | `image_background_remover`, `nano_banana_2` | Recraft, Seedream edit |
| Listing pack | `marketplace-cards`, product photoshoot | still/edit fallback |
| Reframe | `reframe` | manual/ffmpeg fallback |
| Video cutout | `sam_3_video` | fallback only if needed |
| Final scoring | `brain_activity` | manual review if too long/unsupported |

## Model Switching Policy

Video model switching is disabled.

Every generated video shot must record:

```text
model: seedance_2_0
model_reason: locked_seedance_2_0_only_policy
model_lock_policy: seedance_2_0_only_all_video_shots
```

If a shot seems better suited to another video model, rewrite the shot for Seedance 2.0 or split the beat into smaller Seedance 2.0 clips. Do not route the shot to another video model.

Static text/image model switching is also disabled while the Nano Banana Pro lock is active. Every intentional generated text-image asset must record:

```text
model: nano_banana_2
model_reason: locked_nano_banana_pro_static_text_image_policy
static_text_image_model_lock_policy: nano_banana_pro_only_for_model_generated_text_images
```

## Hard Gates

- No generation without `prompt_council_review.json` pass or pass-with-publish-block.
- No provider call before `.env` is loaded and required env var names are present.
- Download every provider output immediately into the run folder.
- Provider CDN URLs are never the final source of truth.
- `topaz_video` is after visual lock, not a rescue for weak direction.
- `brain_activity` is a ranking signal, not approval.
- If a model returns source audio unexpectedly, strip it before final composition and record the incident.
- If a model route changes an identity anchor, product anchor, or recurring motif color, mark the shot `regenerate` or `use_as_texture`; do not promote it to final.
- If provider output duration differs from the request, document it and either regenerate, split into shot clips, or label it as a hook/cutdown sample.
- If `seedance_2_0` is unavailable, blocked, or repeatedly fails, stop and escalate instead of falling back to a different visual video model.
- If an intentional generated text-image asset does not use `nano_banana_2`, block it before generation or reject it in QC.
- If a Nano Banana Pro text image has OCR/spelling/claim errors, regenerate with `nano_banana_2`, rebuild it deterministically in post, or stop.

## Fallback Triggers

Fallback is allowed only when one of these is true:

- Product identity drift persists after one constrained retry.
- Model output violates duration, audio, or controllability requirements.
- Credit/time budget requires an approved lower-cost utility route.

For visual video, these fallback triggers mean "stop or retry Seedance 2.0 with a revised shot contract"; they do not permit another video model.

## Stop Conditions

Block further generation when:

- the prompt council decision is `revise` or `block`;
- product truth or claim ledger is missing;
- rights tracker is red/black for required source assets;
- the route would require scraping private pages or bypassing platform controls.
