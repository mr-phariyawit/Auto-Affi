"""Unit tests for the dry-run Shopee product source.

No network calls are made. All products come from hardcoded fixtures.
"""

from __future__ import annotations

import pytest

from auto_affi.adapters.shopee import DryRunShopeeSource, ShopeeProduct, get_fixture_products


@pytest.mark.unit
def test_get_fixture_products_returns_at_least_two() -> None:
    products = get_fixture_products()
    assert len(products) >= 2


@pytest.mark.unit
def test_fixture_products_are_shopee_product_instances() -> None:
    products = get_fixture_products()
    for p in products:
        assert isinstance(p, ShopeeProduct)


@pytest.mark.unit
def test_fixture_products_valid_shape() -> None:
    """Each fixture must have a valid price range, commission, rating."""
    products = get_fixture_products()
    for p in products:
        assert p.price_min >= 0
        assert p.price_max >= p.price_min
        assert 100.0 <= p.price_max <= 300.0, f"{p.name}: price_max {p.price_max} out of ฿100-300"
        assert 0.0 < p.commission_rate <= 1.0
        assert p.rating_star >= 4.5
        assert p.sales > 0


@pytest.mark.unit
def test_fixture_products_have_shopee_urls() -> None:
    products = get_fixture_products()
    for p in products:
        assert p.shopee_url is not None
        assert p.shopee_url.startswith("https://shopee.co.th/")


@pytest.mark.unit
def test_dry_run_source_default_is_dry_run() -> None:
    source = DryRunShopeeSource()
    assert source.dry_run is True


@pytest.mark.unit
def test_dry_run_source_fetch_returns_at_least_two() -> None:
    source = DryRunShopeeSource(dry_run=True)
    products = source.fetch_products()
    assert len(products) >= 2


@pytest.mark.unit
def test_dry_run_source_respects_commission_filter() -> None:
    source = DryRunShopeeSource(dry_run=True)
    # All fixtures have commission >= 7%; filter at 7.5% should return fewer
    high_threshold = source.fetch_products(min_commission_pct=7.5)
    low_threshold = source.fetch_products(min_commission_pct=1.0)
    assert len(high_threshold) <= len(low_threshold)
    for p in high_threshold:
        assert p.commission_rate >= 0.075


@pytest.mark.unit
def test_dry_run_source_keyword_filter() -> None:
    source = DryRunShopeeSource(dry_run=True)
    # "ร่ม" (umbrella) should match the rainy-season umbrella fixture
    umbrella_results = source.fetch_products(keyword="ร่ม", min_commission_pct=1.0)
    assert len(umbrella_results) >= 1
    assert any("ร่ม" in p.name for p in umbrella_results)


@pytest.mark.unit
def test_dry_run_source_no_network_imports() -> None:
    """Verify at module-import level that httpx/requests are not imported."""
    import importlib
    import sys

    # Remove cached module to force fresh import check
    mod_name = "auto_affi.adapters.shopee"
    if mod_name in sys.modules:
        del sys.modules[mod_name]

    # Also remove any httpx/requests from sys.modules to detect fresh imports
    before_httpx = "httpx" in sys.modules
    before_requests = "requests" in sys.modules

    importlib.import_module(mod_name)

    # The shopee module must NOT have introduced httpx or requests
    # (if they were already present from elsewhere, that's fine — we only
    # care that shopee.py itself doesn't import them)
    import auto_affi.adapters.shopee as shopee_mod

    src = shopee_mod.__file__
    assert src is not None
    with open(src) as f:  # noqa: PTH123
        content = f.read()
    assert "import httpx" not in content
    assert "import requests" not in content
    assert "from httpx" not in content
    assert "from requests" not in content


@pytest.mark.unit
def test_live_mode_raises_not_implemented() -> None:
    source = DryRunShopeeSource(dry_run=False)
    with pytest.raises(NotImplementedError, match="Phase 1"):
        source.fetch_products()
