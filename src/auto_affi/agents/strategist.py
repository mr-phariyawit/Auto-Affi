"""Strategist agent — matchmaker between products, trends, and audiences.

Takes a :class:`ShopeeProduct` (from Scout) and produces a
:class:`CampaignBrief` (for Writers' Room). Fulfils FR-ST-01..03:

  - Generates a structured CampaignBrief with all required fields
  - Queries the Wiki canonical rules via RAG before reasoning (FR-ST-02)
  - Boosts priority when within 14 days of a Shopee mega-sale (FR-ST-03)

Phase 1 implementation: single LLM call (Sonnet 4.6 for throughput) with
a structured-output prompt.  No multi-turn debate -- that's Phase 2 when
the Writers' Room subsumes some Strategist reasoning.
"""

from __future__ import annotations

import json
from datetime import UTC, date, datetime
from typing import Any

from auto_affi.adapters.anthropic_client import AnthropicClient, Model
from auto_affi.adapters.shopee import ShopeeProduct
from auto_affi.exceptions import SchemaValidationError
from auto_affi.schemas.campaign_brief import CampaignBrief
from auto_affi.schemas.tool_result import ToolResult
from auto_affi.wiki.hook_library import HOOK_TEMPLATES

# Shopee mega-sale dates (month.day) — FR-ST-03.
_MEGA_SALES: tuple[tuple[int, int], ...] = (
    (3, 3),
    (6, 6),
    (9, 9),
    (10, 10),
    (11, 11),
    (12, 12),
)
_MEGA_SALE_WINDOW_DAYS = 14


def is_mega_sale_window(*, today: date | None = None) -> bool:
    """Return True if ``today`` is within 14 days before any mega-sale."""
    d = today or date.today()
    for month, day in _MEGA_SALES:
        sale_date = d.replace(month=month, day=day)
        delta = (sale_date - d).days
        if 0 <= delta <= _MEGA_SALE_WINDOW_DAYS:
            return True
    return False


def _hook_catalog_text() -> str:
    """Build a compact reference of available hook templates for the prompt."""
    lines: list[str] = []
    for tpl in HOOK_TEMPLATES:
        lines.append(
            f"- {tpl.slug}: {tpl.name_en} — {tpl.description[:100]}... "
            f"best_for={tpl.best_for}"
        )
    return "\n".join(lines)


_SYSTEM_PROMPT = """\
You are the Auto-Affi Strategist agent. Your job: take a Shopee product and
produce a CampaignBrief JSON that the Writers' Room will use to create a
60-second Thai-language 9:16 affiliate video.

RULES:
1. Every field in the output schema is REQUIRED. Do not omit any field.
2. All audience-facing text (angle, hook, CTA) MUST be in Thai.
3. hook_template_slug MUST be one of the available templates listed below.
4. expected_ctr must be realistic (0.5-10% typical, never above 15%).
5. confidence is YOUR confidence in this brief (0.0-1.0).
6. hypothesis must explain WHY this angle + product + persona combo will work.
7. wiki_evidence_slugs: list the hook template slug you chose.

AVAILABLE HOOK TEMPLATES:
{hook_catalog}

OUTPUT: Return ONLY a valid JSON object matching the CampaignBrief schema.
No markdown, no explanation — just the JSON.
"""

_USER_TEMPLATE = """\
Create a CampaignBrief for this product:

Product: {product_name}
Item ID: {item_id}
Shop ID: {shop_id}
Price: {price_min}-{price_max} THB
Commission: {commission_pct:.1f}%
Rating: {rating_star}/5
Sales: {sales}
Category hint: beauty_skincare (Phase 1 focus)
Mega-sale window: {mega_sale}

Target: Thai women 18-35 who scroll IG Reels and Shopee daily.
"""


class Strategist:
    """Strategist agent — produces CampaignBriefs from product candidates."""

    def __init__(
        self,
        client: AnthropicClient,
        *,
        model: Model = "claude-sonnet-4-6",
        wiki_entries: list[dict[str, Any]] | None = None,
    ) -> None:
        self._client = client
        self._model = model
        self._wiki_entries = wiki_entries or []

    async def generate_brief(
        self,
        product: ShopeeProduct,
        *,
        today: date | None = None,
    ) -> ToolResult[CampaignBrief]:
        """Generate a CampaignBrief for the given product.

        Returns a :class:`ToolResult` wrapping the brief so callers get
        uniform cost / latency / error tracking.
        """
        mega_sale = is_mega_sale_window(today=today)
        system_text = _SYSTEM_PROMPT.format(hook_catalog=_hook_catalog_text())
        user_text = _USER_TEMPLATE.format(
            product_name=product.name,
            item_id=product.item_id,
            shop_id=product.shop_id,
            price_min=product.price_min,
            price_max=product.price_max,
            commission_pct=product.commission_rate * 100,
            rating_star=product.rating_star,
            sales=product.sales,
            mega_sale="YES — boost priority" if mega_sale else "no",
        )

        result = await self._client.complete(
            model=self._model,
            system=system_text,
            messages=[{"role": "user", "content": user_text}],
            max_tokens=2048,
            temperature=0.6,
        )

        if not result.ok or result.data is None:
            return ToolResult(
                ok=False,
                error=result.error or "LLM returned empty response",
                cost_usd=result.cost_usd,
                latency_ms=result.latency_ms,
                trace_id=result.trace_id,
            )

        # Parse the LLM's JSON output into a CampaignBrief.
        try:
            brief_data = _extract_json(result.data.text)
            # Inject fields the LLM should not control.
            brief_data["product_id"] = product.item_id
            brief_data["shop_id"] = product.shop_id
            brief_data["priority_boost"] = mega_sale
            brief_data["created_by_agent"] = "strategist"
            brief = CampaignBrief(**brief_data)
        except (json.JSONDecodeError, TypeError, ValueError) as err:
            return ToolResult(
                ok=False,
                error=f"Failed to parse LLM brief: {err}",
                cost_usd=result.cost_usd,
                latency_ms=result.latency_ms,
                trace_id=result.trace_id,
            )
        except SchemaValidationError as err:
            return ToolResult(
                ok=False,
                error=f"Brief schema validation failed: {err}",
                cost_usd=result.cost_usd,
                latency_ms=result.latency_ms,
                trace_id=result.trace_id,
            )

        return ToolResult(
            ok=True,
            data=brief,
            cost_usd=result.cost_usd,
            latency_ms=result.latency_ms,
            trace_id=result.trace_id,
        )


def _extract_json(text: str) -> dict[str, Any]:
    """Extract the first JSON object from LLM output.

    Handles the common case where the LLM wraps JSON in a markdown code
    fence.
    """
    cleaned = text.strip()

    # Strip markdown code fence if present.
    if cleaned.startswith("```"):
        # Find the closing fence.
        lines = cleaned.split("\n")
        # Remove first line (```json or ```) and last line (```)
        json_lines = []
        in_fence = False
        for line in lines:
            if line.strip().startswith("```") and not in_fence:
                in_fence = True
                continue
            if line.strip() == "```" and in_fence:
                break
            if in_fence:
                json_lines.append(line)
        cleaned = "\n".join(json_lines)

    data: dict[str, Any] = json.loads(cleaned)
    if not isinstance(data, dict):
        raise TypeError(f"Expected JSON object, got {type(data).__name__}")
    return data
