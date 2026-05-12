"""Thai-language compliance claim auditor.

Deterministic first filter used by the Safety and Critic agents before any
storyboard or caption ships. Catches the four highest-risk claim families
that OCPB and platform ToS regularly fine or throttle in 2025-26:

  - medical / health (รักษา / แก้ + condition)
  - whitening / pigmentation
  - financial guarantees (รับประกัน / การันตี + return / income)
  - generic guarantees ("100%" / "ได้ผลแน่นอน")

The audit is intentionally over-eager: any hit short-circuits the
pipeline and forces a re-draft. The downstream Critic Opus may still
catch subtler violations, but anything caught here saves the LLM round
trip entirely. See docs/pm/risk-register.md R-03 and
docs/execution-playbook.md section 10 for the policy justification.
"""

from __future__ import annotations

import re
from enum import StrEnum

from pydantic import BaseModel, Field


class ClaimCategory(StrEnum):
    """Top-level risk category for an audit hit."""

    MEDICAL = "medical"
    WHITENING = "whitening"
    FINANCIAL = "financial"
    GUARANTEE = "guarantee"


class ClaimViolation(BaseModel):
    """One matched phrase the auditor wants the agent to remove."""

    category: ClaimCategory
    pattern_name: str
    matched_text: str = Field(min_length=1)
    span: tuple[int, int]
    severity: int = Field(ge=1, le=3, description="1=advise, 2=block, 3=hard-block")


class _Pattern:
    __slots__ = ("category", "name", "regex", "severity")

    def __init__(
        self,
        category: ClaimCategory,
        name: str,
        regex: re.Pattern[str],
        severity: int,
    ) -> None:
        self.category = category
        self.name = name
        self.regex = regex
        self.severity = severity


def _compile(pattern: str) -> re.Pattern[str]:
    # Thai script is matched directly; we don't apply IGNORECASE because Thai
    # has no case, and any English markers we include are already lowercase.
    return re.compile(pattern, flags=re.UNICODE)


# Medical / health -------------------------------------------------------- #
# Phrasing the Thai FDA and OCPB call out most often: anything that promises
# to treat, cure, or eliminate a named condition; "100% safe" with a body
# part; or before/after frames with medical wording.
_MEDICAL_CONDITIONS = (
    "สิว",
    "ฝ้า",
    "กระ",
    "มะเร็ง",
    "เบาหวาน",
    "ความดัน",
    "ผมร่วง",
    "โรค",
)
_MEDICAL_VERBS = ("รักษา", "หาย", "บรรเทา", "กำจัด", "แก้", "ลด")

_PATTERNS: tuple[_Pattern, ...] = (
    _Pattern(
        ClaimCategory.MEDICAL,
        "treat_named_condition",
        _compile(
            r"(?:" + "|".join(_MEDICAL_VERBS) + r")\s*(?:" + "|".join(_MEDICAL_CONDITIONS) + r")"
        ),
        severity=3,
    ),
    _Pattern(
        ClaimCategory.MEDICAL,
        "cured_completely",
        _compile(r"หาย(?:ขาด|สนิท|ทันที|ภายใน\s*\d+)"),
        severity=3,
    ),
    # Whitening / pigmentation ------------------------------------------- #
    _Pattern(
        ClaimCategory.WHITENING,
        "skin_lightening",
        _compile(r"(?:ผิว|หน้า)\s*(?:ขาว|กระจ่าง)(?:ขึ้น|ใส|ออร่า|วิ้ง|ฉ่ำ)?"),
        severity=3,
    ),
    _Pattern(
        ClaimCategory.WHITENING,
        "english_whitening",
        _compile(r"\b(?:whitening|brighten(?:ing)?|skin\s*white)\b"),
        severity=2,
    ),
    # Financial guarantees ----------------------------------------------- #
    _Pattern(
        ClaimCategory.FINANCIAL,
        "guaranteed_return",
        _compile(r"(?:รับประกัน|การันตี)\s*(?:ผลตอบแทน|กำไร|รายได้|คืนเงิน)"),
        severity=3,
    ),
    _Pattern(
        ClaimCategory.FINANCIAL,
        "income_promise",
        _compile(r"รวย(?:เร็ว|ภายใน|ใน\s*\d+)"),
        severity=3,
    ),
    _Pattern(
        ClaimCategory.FINANCIAL,
        "passive_income_lure",
        _compile(r"รายได้\s*(?:เสริม|พิเศษ)\s*\d+"),
        severity=2,
    ),
    # Generic guarantee --------------------------------------------------- #
    _Pattern(
        ClaimCategory.GUARANTEE,
        "absolute_percent",
        _compile(r"(?:100|๑๐๐)\s*%"),
        severity=2,
    ),
    _Pattern(
        ClaimCategory.GUARANTEE,
        "guaranteed_result",
        _compile(r"ได้ผล\s*(?:แน่นอน|ทันที|100%|ทุกคน)"),
        severity=3,
    ),
    _Pattern(
        ClaimCategory.GUARANTEE,
        "money_back_promise",
        _compile(r"คืนเงิน(?:เต็มจำนวน|100%|ทุกบาท)"),
        severity=2,
    ),
)


def audit(text_th: str) -> list[ClaimViolation]:
    """Return every claim violation found in ``text_th``.

    Returns an empty list when the text is compliant. Order matches reading
    order so the Critic agent can render a deterministic re-draft prompt.
    """
    violations: list[ClaimViolation] = []
    for pattern in _PATTERNS:
        for match in pattern.regex.finditer(text_th):
            violations.append(
                ClaimViolation(
                    category=pattern.category,
                    pattern_name=pattern.name,
                    matched_text=match.group(0),
                    span=(match.start(), match.end()),
                    severity=pattern.severity,
                )
            )
    violations.sort(key=lambda v: v.span[0])
    return violations


def is_blocked(text_th: str, *, min_severity: int = 2) -> bool:
    """Convenience guard used by the Publisher pre-flight check."""
    return any(v.severity >= min_severity for v in audit(text_th))
