"""Shopee product source — DRY-RUN mode (Phase 1, offline-only).

This module provides a dry-run product source that returns hardcoded fixture
products. No network calls are made. Network integration (Shopee Affiliate Open
API via SHA256-HMAC) is available at git ``5602e53`` and will be re-introduced
in Phase 2 once Affiliate Program approval is obtained.

Phase 1 scope:
- ``ShopeeProduct`` — pydantic model matching the Shopee product shape from 5602e53
- ``DryRunShopeeSource`` — returns fixture products with ``dry_run=True`` default
- ``get_fixture_products`` — convenience function returning the built-in fixtures

Fixtures represent real Thai Shopee category examples:
  - A rain-season umbrella (beauty_skincare adjacent: ``mom_baby`` category)
  - A phone/accessory pouch (``gadgets_accessories``)
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ShopeeProduct(BaseModel):
    """A trimmed Shopee product offer used by the Scout agent.

    Field names and types are identical to the 5602e53 implementation so that
    scoring and registry adapters can switch to live data without model changes.
    """

    item_id: int
    shop_id: int
    name: str
    price_min: float = Field(ge=0)
    price_max: float = Field(ge=0)
    commission_rate: float = Field(ge=0, le=1, description="0.0-1.0 fraction")
    rating_star: float = Field(ge=0, le=5)
    sales: int = Field(ge=0)
    image_url: str | None = None
    shopee_url: str | None = None


# ---------------------------------------------------------------------------
# Built-in fixture products
# ---------------------------------------------------------------------------

_FIXTURES: list[ShopeeProduct] = [
    ShopeeProduct(
        item_id=10000001,
        shop_id=500001,
        name="ร่มกันฝน UV พับได้ 3 ตอน กันแดด กันฝน",  # Foldable UV rain umbrella
        price_min=129.0,
        price_max=199.0,
        commission_rate=0.07,
        rating_star=4.8,
        sales=3200,
        image_url=None,
        shopee_url="https://shopee.co.th/ร่มกันฝน-UV-i.500001.10000001",
    ),
    ShopeeProduct(
        item_id=10000002,
        shop_id=500002,
        name="ซองใส่โทรศัพท์กันน้ำ กระเป๋าคาดเอว 2-in-1",  # Waterproof phone pouch belt bag
        price_min=89.0,
        price_max=149.0,
        commission_rate=0.08,
        rating_star=4.7,
        sales=1850,
        image_url=None,
        shopee_url="https://shopee.co.th/ซองใส่โทรศัพท์กันน้ำ-i.500002.10000002",
    ),
    ShopeeProduct(
        item_id=10000003,
        shop_id=500003,
        name="ครีมกันแดด SPF50+ PA++++ ไม่มัน บางเบา",  # Lightweight SPF50+ sunscreen
        price_min=185.0,
        price_max=285.0,
        commission_rate=0.09,
        rating_star=4.9,
        sales=8100,
        image_url=None,
        shopee_url="https://shopee.co.th/ครีมกันแดด-SPF50-i.500003.10000003",
    ),
]


def get_fixture_products() -> list[ShopeeProduct]:
    """Return the built-in offline fixture products (immutable copy)."""
    return list(_FIXTURES)


class DryRunShopeeSource:
    """Offline product source that returns fixture Shopee products.

    ``dry_run=True`` by default; when ``False`` this class would delegate to
    the live API client (not implemented in Phase 1 — raises NotImplementedError
    to make the boundary explicit).
    """

    def __init__(self, *, dry_run: bool = True) -> None:
        self.dry_run = dry_run

    def fetch_products(
        self,
        keyword: str = "",
        *,
        min_commission_pct: float = 3.0,
    ) -> list[ShopeeProduct]:
        """Return products matching optional keyword/commission filters.

        In dry-run mode: filters the fixture list. In live mode: raises
        ``NotImplementedError`` (Phase 2).
        """
        if not self.dry_run:
            raise NotImplementedError(
                "Live Shopee API not available in Phase 1. "
                "See git 5602e53:src/auto_affi/adapters/shopee.py for the async client."
            )

        threshold = min_commission_pct / 100.0
        results = [p for p in _FIXTURES if p.commission_rate >= threshold]
        if keyword:
            kw = keyword.lower()
            results = [p for p in results if kw in p.name.lower()]
        return results
