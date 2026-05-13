"""Shopee public-product ingester — pre-Affiliate-API fallback.

The official path to a ``ShopeeProduct`` is :class:`ShopeeClient` against
the affiliate GraphQL endpoint with HMAC-signed requests (``shopee.py``).
That requires Shopee Affiliate Program approval, which is currently
pending (see ``.aegis/brain/human-queue.md``).

Until that lands, we need an ingestion path for real product URLs that
does NOT depend on the affiliate API.

Attempted paths (May 2026):
  - HTTP GET ``/api/v4/item/get`` → **403** (Shopee fingerprints non-browser)
  - HTML scrape ``/i.<shop>.<item>`` → SPA shell, no JSON-LD / __INITIAL_STATE__
  - Playwright + ``fetch()`` from page context → triggers anti-bot, page
    redirects to ``/verify/traffic/error`` CAPTCHA

Conclusion: **no fully-automated zero-credential path is reliable** for
Shopee TH today. Three viable strategies remain:

  1. **Affiliate API** (production path) — pending approval
  2. **Manual fixture** — hand-curated JSON file per product. Useful for
     exploring the pipeline with real product names + ids before
     Affiliate is live. *This module's primary mode.*
  3. **Paid scraping service** (Bright Data / ScraperAPI / Apify) —
     deferred to Phase 2 if Affiliate API is slow to approve.

This module provides:
  - :func:`parse_url_to_ids` — extract ``(shop_id, item_id)`` from the
    canonical ``shopee.co.th/i.<shop_id>.<item_id>`` URL pattern.
  - :func:`load_fixture` — read a curated fixture JSON to ``ShopeeProduct``.
  - :func:`fetch_or_fixture` — try Affiliate API (if creds present),
    fall back to fixture (if found), else raise ``AdapterError``.

The same ``ShopeeProduct`` schema as :class:`ShopeeClient` is the target,
so downstream code (Scout / Strategist / Writers') is fully agnostic to
which ingestion path was used.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Final

from auto_affi.adapters.shopee import ShopeeProduct
from auto_affi.exceptions import AdapterError

_URL_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"shopee\.co\.th/(?:[^/]*-)?i\.(\d+)\.(\d+)"
)


def parse_url_to_ids(url: str) -> tuple[int, int]:
    """Extract ``(shop_id, item_id)`` from a Shopee TH product URL.

    Canonical form: ``https://shopee.co.th/<slug>-i.<shop_id>.<item_id>`` or
    ``https://shopee.co.th/i.<shop_id>.<item_id>``.

    Raises :class:`AdapterError` if the URL doesn't match.
    """
    match = _URL_PATTERN.search(url)
    if not match:
        raise AdapterError(
            f"Shopee URL parse failed: expected '.../i.<shop>.<item>' pattern, got {url!r}"
        )
    shop_id = int(match.group(1))
    item_id = int(match.group(2))
    return shop_id, item_id


def load_fixture(path: Path) -> ShopeeProduct:
    """Load a manually-curated product fixture.

    Fixture format (JSON):

    .. code-block:: json

        {
          "_meta": {...},
          "product": {
            "item_id": 44154734826,
            "shop_id": 992256187,
            "name": "...",
            "price_min": 129.0,
            "price_max": 249.0,
            "commission_rate": 0.06,
            "rating_star": 4.7,
            "sales": 1200,
            "image_url": null
          }
        }
    """
    if not path.exists():
        raise AdapterError(f"Shopee fixture not found: {path}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    product_dict = raw.get("product")
    if not product_dict:
        raise AdapterError(
            f"Shopee fixture {path} missing top-level 'product' key"
        )
    try:
        return ShopeeProduct(**product_dict)
    except Exception as err:
        raise AdapterError(f"Shopee fixture {path} invalid: {err}") from err


def find_fixture_by_item_id(
    item_id: int, fixtures_dir: Path = Path("data/fixtures/shopee")
) -> Path | None:
    """Find a fixture file whose name contains the item_id."""
    if not fixtures_dir.exists():
        return None
    for f in fixtures_dir.glob("*.json"):
        if str(item_id) in f.name:
            return f
    return None


def fetch_or_fixture(
    *,
    url: str | None = None,
    shop_id: int | None = None,
    item_id: int | None = None,
    fixtures_dir: Path = Path("data/fixtures/shopee"),
) -> ShopeeProduct:
    """Resolve a ShopeeProduct from URL or (shop_id, item_id), trying fixture first.

    Order of resolution:
      1. If ``url`` provided → parse to ids.
      2. If a fixture matches ``item_id`` → load it.
      3. Affiliate API call placeholder (raises ``AdapterError`` until wired).

    Production usage will swap step 3 to a real :class:`ShopeeClient` call.
    """
    if url is not None:
        shop_id, item_id = parse_url_to_ids(url)
    if item_id is None:
        raise AdapterError("Shopee fetch needs --url or --item-id")

    fixture_path = find_fixture_by_item_id(item_id, fixtures_dir)
    if fixture_path is not None:
        return load_fixture(fixture_path)

    raise AdapterError(
        f"Shopee item {item_id} not in fixtures and Affiliate API not yet wired. "
        f"Add a fixture at {fixtures_dir}/<slug>-{item_id}.json or wait for "
        f"Affiliate Program approval (see .aegis/brain/human-queue.md)."
    )
