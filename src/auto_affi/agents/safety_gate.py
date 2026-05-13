"""Pre-publish safety gate — composed pipeline (FR-SF-01).

Three checks run in sequence before any video can be published:

  1. **Claim audit** — Thai compliance (claim_auditor.audit)
  2. **Brand blocklist** — known brands that prohibit affiliate content
  3. **NSFW check** — image/video safety (placeholder for Phase 1)

All three must PASS before a :class:`PublishRecord` may be created.
If any check fails, the gate returns a structured :class:`SafetyVerdict`
with all violations so the agent can re-draft or escalate.

The gate is intentionally over-eager: false positives cost a re-draft
(~$0.05 LLM call); false negatives cost an account ban (~$500 lost
revenue + 2-week recovery).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel, Field

from auto_affi.agents.claim_auditor import audit


class SafetyCheckName(StrEnum):
    """Names of individual safety checks in the pipeline."""

    CLAIM_AUDIT = "claim_audit"
    BRAND_BLOCKLIST = "brand_blocklist"
    NSFW_CHECK = "nsfw_check"


class CheckResult(BaseModel):
    """Result of a single safety check."""

    check: SafetyCheckName
    passed: bool
    violations: list[str] = Field(default_factory=list)


class SafetyVerdict(BaseModel):
    """Aggregated result of the full safety gate."""

    passed: bool
    checks: list[CheckResult]
    block_reason: str | None = None

    @property
    def failed_checks(self) -> list[CheckResult]:
        return [c for c in self.checks if not c.passed]


# Default brand blocklist — brands known to prohibit or restrict affiliate
# content. Configurable per deployment via settings.
DEFAULT_BRAND_BLOCKLIST: frozenset[str] = frozenset(
    {
        # Luxury brands that DMCA affiliate content
        "chanel",
        "hermes",
        "louis vuitton",
        "gucci",
        "dior",
        "prada",
        # Brands with exclusive affiliate programmes (our accounts are not approved)
        "apple",
        "samsung official",
        # Brands with Thai advertising restrictions
        "est cola",  # requires Thai FDA pre-approval for health claims
    }
)


@dataclass(frozen=True)
class SafetyGateConfig:
    """Runtime configuration for the safety gate."""

    brand_blocklist: frozenset[str] = DEFAULT_BRAND_BLOCKLIST
    claim_min_severity: int = 2
    nsfw_enabled: bool = False  # Phase 1: placeholder, no external API yet


def check_claims(text_th: str, *, min_severity: int = 2) -> CheckResult:
    """Run the claim auditor on Thai text.

    Returns a :class:`CheckResult` with violation details.
    """
    violations = audit(text_th)
    blocking = [v for v in violations if v.severity >= min_severity]

    if not blocking:
        return CheckResult(check=SafetyCheckName.CLAIM_AUDIT, passed=True)

    return CheckResult(
        check=SafetyCheckName.CLAIM_AUDIT,
        passed=False,
        violations=[
            f"[{v.category}/{v.pattern_name}] severity={v.severity}: "
            f"'{v.matched_text}' at {v.span}"
            for v in blocking
        ],
    )


def check_brand_blocklist(
    text: str,
    *,
    product_name: str = "",
    blocklist: frozenset[str] = DEFAULT_BRAND_BLOCKLIST,
) -> CheckResult:
    """Check if the content mentions a blocked brand.

    Searches both the script text and the product name (case-insensitive).
    """
    combined = f"{text} {product_name}".lower()
    found: list[str] = []
    for brand in blocklist:
        if brand.lower() in combined:
            found.append(brand)

    if not found:
        return CheckResult(check=SafetyCheckName.BRAND_BLOCKLIST, passed=True)

    return CheckResult(
        check=SafetyCheckName.BRAND_BLOCKLIST,
        passed=False,
        violations=[f"Blocked brand mentioned: {b}" for b in sorted(found)],
    )


def check_nsfw(*, enabled: bool = False) -> CheckResult:
    """NSFW image/video safety check (placeholder for Phase 1).

    In Phase 1 this always passes. Phase 2 will integrate an external
    safety API (e.g., Azure Content Safety or Amazon Rekognition).
    """
    if not enabled:
        # Placeholder: always pass when disabled.
        return CheckResult(
            check=SafetyCheckName.NSFW_CHECK,
            passed=True,
            violations=["NSFW check disabled (Phase 1 placeholder)"],
        )

    # Phase 2: call external API here.
    return CheckResult(check=SafetyCheckName.NSFW_CHECK, passed=True)


def safety_gate(
    *,
    script_text_th: str,
    product_name: str = "",
    config: SafetyGateConfig | None = None,
) -> SafetyVerdict:
    """Run the full pre-publish safety pipeline.

    Parameters
    ----------
    script_text_th
        The Thai-language script / caption to audit.
    product_name
        The product name (for brand blocklist matching).
    config
        Optional runtime config. Defaults to :class:`SafetyGateConfig`.

    Returns
    -------
    SafetyVerdict
        Aggregated result. ``passed=True`` only if all checks pass.
    """
    cfg = config or SafetyGateConfig()

    checks: list[CheckResult] = [
        check_claims(script_text_th, min_severity=cfg.claim_min_severity),
        check_brand_blocklist(
            script_text_th,
            product_name=product_name,
            blocklist=cfg.brand_blocklist,
        ),
        check_nsfw(enabled=cfg.nsfw_enabled),
    ]

    all_passed = all(c.passed for c in checks)
    block_reason: str | None = None

    if not all_passed:
        failed = [c for c in checks if not c.passed]
        reasons = [f"{c.check}: {'; '.join(c.violations)}" for c in failed]
        block_reason = " | ".join(reasons)

    return SafetyVerdict(
        passed=all_passed,
        checks=checks,
        block_reason=block_reason,
    )
