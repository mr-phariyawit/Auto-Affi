"""Shared unit-test fixtures.

Product fixtures used by more than one test module live here so they are defined
once (previously duplicated in test_strategist.py and test_writers_room.py).
"""

from __future__ import annotations

import pytest

from auto_affi.adapters.shopee import ShopeeProduct


@pytest.fixture()
def umbrella_product() -> ShopeeProduct:
    """Rainy-season umbrella — triggers rainy-season-must-have template."""
    return ShopeeProduct(
        item_id=10000001,
        shop_id=500001,
        name="ร่มกันฝน UV พับได้ 3 ตอน กันแดด กันฝน",
        price_min=129.0,
        price_max=199.0,
        commission_rate=0.07,
        rating_star=4.8,
        sales=3200,
    )


@pytest.fixture()
def sunscreen_product() -> ShopeeProduct:
    """Skincare / beauty product — triggers beauty-result-reveal template."""
    return ShopeeProduct(
        item_id=10000003,
        shop_id=500003,
        name="ครีมกันแดด SPF50+ PA++++ ไม่มัน บางเบา",
        price_min=185.0,
        price_max=285.0,
        commission_rate=0.09,
        rating_star=4.9,
        sales=8100,
    )
