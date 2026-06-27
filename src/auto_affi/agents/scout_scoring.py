"""Product Scout scoring rubric.

Pure function ranking a Shopee product offer for affiliate suitability,
per ``docs/execution-playbook.md`` §5.2. The LLM-driven part of the Scout
agent (reasoning over wiki anti-patterns, novelty checks) lives in the
agent module; this file is the deterministic, testable core.

Formula (all sub-scores clamped to 0..1 before weighting):

    score = 0.30 * commission_ev
          + 0.25 * cr_signal
          + 0.15 * trend_momentum
          - 0.15 * saturation
          - 0.10 * return_rate_penalty
          + 0.05 * cookie_utilisation

Hard filters (any one fails → REJECT):
    - category in RESTRICTED_CATEGORIES
    - shop rating < 4.5
    - commission_rate < 3% AND aov_thb < 300
    - unviable economics: breakeven_views > MAX_BREAKEVEN_VIEWS

The economics filter (2026-06-27) operationalises the #1 finding of the
successful-operator research: vet *money earned per conversion* (commission-EV
in THB), not the commission *rate*, BEFORE any paid pipeline run. A blunt
"reject < 8% commission" rule was deliberately NOT adopted — it contradicts the
existing principle that a low rate on a high-AOV product still earns real money
per conversion (see ``test_low_rate_high_aov_survives_economics_gate``). Instead
we reject products that cannot recoup production cost within a plausible view
ceiling. See ``reports/2026-06-27_ai-affiliate-upgrade-plan.md`` §2 #1/#2.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel, Field

# Categories that the Safety / Critic agents would reject downstream anyway.
# Filtering them at scout time saves an entire pipeline run.
RESTRICTED_CATEGORIES: frozenset[str] = frozenset(
    {
        "supplements",
        "medical_device",
        "pharmaceuticals",
        "weight_loss",
        "whitening",
        "replica",
        "tobacco",
        "alcohol",
        "weapons",
        "financial_services",
    }
)

# Historical conversion rate priors per Shopee category, sourced from the
# Shopee-TH research note in docs/execution-playbook.md §5.5.
# Values are midpoints of observed ranges.
CR_CATEGORY_PRIOR: dict[str, float] = {
    "beauty_skincare": 0.0225,  # 1.5-3%
    "mom_baby": 0.015,  # 1-2%
    "gadgets_accessories": 0.0115,  # 0.8-1.5%
    "fashion": 0.009,  # 0.6-1.2%
    "home": 0.006,  # 0.4-0.8%
    "food_beverage": 0.008,
}

DEFAULT_CR_PRIOR: float = 0.005  # Unknown categories get the floor.

# Economics gate (2026-06-27 research finding #1). ~$3/video SPEC §1.2 target at
# ~35 THB/USD. A product whose commission-EV cannot recoup this within a
# modest-success view ceiling is unviable and must not reach paid production.
PRODUCTION_COST_THB: float = 105.0
# A product needing more than this many views just to recoup one video's cost is
# too thin for an organic small-audience operation. Tunable per-pilot via score().
# Every currently-passing candidate breaks even well under 1k views; the three
# live Shopee fixtures recoup within ~200-770 views.
MAX_BREAKEVEN_VIEWS: float = 10_000.0
# Shopee caps per-order commission near THB 200; shared by EV and breakeven.
_COMMISSION_CAP_THB: float = 200.0

# Return-rate penalty by category — fashion and electronics are the worst
# offenders. Values represent the typical fraction of orders returned and
# directly suppress the score.
RETURN_RATE_PENALTY: dict[str, float] = {
    "fashion": 0.12,
    "gadgets_accessories": 0.06,
    "home": 0.04,
}


class RejectReason(StrEnum):
    """Why a candidate was hard-filtered."""

    RESTRICTED_CATEGORY = "restricted_category"
    LOW_SHOP_RATING = "low_shop_rating"
    LOW_COMMISSION_AND_AOV = "low_commission_and_aov"
    UNVIABLE_ECONOMICS = "unviable_economics"


@dataclass(frozen=True)
class ScoutInput:
    """Everything the scoring rubric needs about one product candidate."""

    category: str
    commission_rate: float
    aov_thb: float
    shop_rating: float
    review_count: int
    sales_velocity_7d: int = 0
    tiktok_mention_growth_7d: float = 0.0
    saturation_count_7d: int = 0
    shop_catalog_size: int = 0


class ScoutScore(BaseModel):
    """Result of scoring a candidate."""

    rejected: bool
    reject_reason: RejectReason | None = None
    score: float = Field(ge=0.0, le=1.0, default=0.0)
    breakdown: dict[str, float] = Field(default_factory=dict)


def _clamp(value: float, *, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def _commission_ev(commission_rate: float, aov_thb: float) -> float:
    """Expected commission in THB, normalised to 0..1 against a 200 THB cap.

    Shopee caps per-order commission near THB 200 across most categories.
    Scaling against that ceiling keeps the sub-score in the [0, 1] band.
    """
    raw_thb = min(commission_rate * aov_thb, _COMMISSION_CAP_THB)
    return _clamp(raw_thb / _COMMISSION_CAP_THB)


def _breakeven_views(*, commission_rate: float, aov_thb: float, category: str, production_cost_thb: float) -> float:
    """Views needed for one video's commission-EV to recoup production cost.

    breakeven_views = production_cost / (commission_per_conversion x CR_prior).
    Returns ``inf`` when the product can never earn (zero EV or zero CR), which
    the economics gate treats as unviable.
    """
    commission_per_conversion = min(commission_rate * aov_thb, _COMMISSION_CAP_THB)
    cr_prior = CR_CATEGORY_PRIOR.get(category, DEFAULT_CR_PRIOR)
    earnings_per_view = commission_per_conversion * cr_prior
    if earnings_per_view <= 0.0:
        return math.inf
    return production_cost_thb / earnings_per_view


def _cr_signal(*, category: str, shop_rating: float, review_count: int) -> float:
    """Conversion-rate signal blending category prior, trust, and log(reviews)."""
    prior = CR_CATEGORY_PRIOR.get(category, DEFAULT_CR_PRIOR)
    # Map shop_rating 4.0-5.0 to 0..1; below 4.0 is essentially zero.
    rating_factor = _clamp((shop_rating - 4.0) / 1.0)
    # log10(reviews) maxes out at ~4 (10k reviews); normalise by 4.
    review_factor = _clamp(math.log10(max(review_count, 1)) / 4.0)
    # 3% CR is "excellent"; normalise the prior the same way as commission_ev.
    prior_factor = _clamp(prior / 0.03)
    return prior_factor * rating_factor * review_factor


def _trend_momentum(*, sales_velocity_7d: int, tiktok_mention_growth_7d: float) -> float:
    """Combine sales delta and TikTok mention growth.

    sales_velocity_7d is interpreted as units sold in the past 7 days;
    100+ units = full credit. tiktok_mention_growth_7d is a fraction (0.5 = +50%).
    """
    sales_factor = _clamp(sales_velocity_7d / 100.0)
    mention_factor = _clamp(tiktok_mention_growth_7d / 1.0)
    return (sales_factor + mention_factor) / 2.0


def _saturation(saturation_count_7d: int) -> float:
    """Heavier penalty as more affiliate listings push the same SKU.

    10+ competing listings in the past 7 days saturate the lane completely.
    """
    return _clamp(saturation_count_7d / 10.0)


def _return_rate_penalty(category: str) -> float:
    """Per-category typical return rate, capped at 1.0."""
    return _clamp(RETURN_RATE_PENALTY.get(category, 0.0) / 0.20)


def _cookie_utilisation(shop_catalog_size: int) -> float:
    """Bigger catalog raises the chance the 7-day cookie captures a cross-sell."""
    return _clamp(shop_catalog_size / 1000.0)


def score(
    candidate: ScoutInput,
    *,
    production_cost_thb: float = PRODUCTION_COST_THB,
    max_breakeven_views: float = MAX_BREAKEVEN_VIEWS,
) -> ScoutScore:
    """Score a candidate, applying hard filters before weighted sum.

    ``production_cost_thb`` / ``max_breakeven_views`` tune the economics gate so
    a niche pilot can tighten the bar (lower ceiling = stricter).
    """
    # --- hard filters --------------------------------------------------- #
    if candidate.category in RESTRICTED_CATEGORIES:
        return ScoutScore(rejected=True, reject_reason=RejectReason.RESTRICTED_CATEGORY)
    if candidate.shop_rating < 4.5:
        return ScoutScore(rejected=True, reject_reason=RejectReason.LOW_SHOP_RATING)
    if candidate.commission_rate < 0.03 and candidate.aov_thb < 300:
        return ScoutScore(rejected=True, reject_reason=RejectReason.LOW_COMMISSION_AND_AOV)

    breakeven_views = _breakeven_views(
        commission_rate=candidate.commission_rate,
        aov_thb=candidate.aov_thb,
        category=candidate.category,
        production_cost_thb=production_cost_thb,
    )
    if breakeven_views > max_breakeven_views:
        return ScoutScore(rejected=True, reject_reason=RejectReason.UNVIABLE_ECONOMICS)

    # --- weighted sub-scores ------------------------------------------- #
    commission_ev = _commission_ev(candidate.commission_rate, candidate.aov_thb)
    cr_signal = _cr_signal(
        category=candidate.category,
        shop_rating=candidate.shop_rating,
        review_count=candidate.review_count,
    )
    trend_momentum = _trend_momentum(
        sales_velocity_7d=candidate.sales_velocity_7d,
        tiktok_mention_growth_7d=candidate.tiktok_mention_growth_7d,
    )
    saturation = _saturation(candidate.saturation_count_7d)
    return_penalty = _return_rate_penalty(candidate.category)
    cookie_util = _cookie_utilisation(candidate.shop_catalog_size)

    raw = (
        0.30 * commission_ev
        + 0.25 * cr_signal
        + 0.15 * trend_momentum
        - 0.15 * saturation
        - 0.10 * return_penalty
        + 0.05 * cookie_util
    )
    final = _clamp(raw)

    return ScoutScore(
        rejected=False,
        score=final,
        breakdown={
            "commission_ev": commission_ev,
            "cr_signal": cr_signal,
            "trend_momentum": trend_momentum,
            "saturation": saturation,
            "return_penalty": return_penalty,
            "cookie_utilisation": cookie_util,
            "raw_weighted_sum": raw,
            "breakeven_views": breakeven_views,
        },
    )
