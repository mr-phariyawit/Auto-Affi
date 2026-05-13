"""Unit tests for shopee_public — URL parser + fixture loader."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_affi.adapters.shopee import ShopeeProduct
from auto_affi.adapters.shopee_public import (
    fetch_or_fixture,
    find_fixture_by_item_id,
    load_fixture,
    parse_url_to_ids,
)
from auto_affi.exceptions import AdapterError


@pytest.mark.unit
def test_parse_url_canonical_pattern() -> None:
    url = (
        "https://shopee.co.th/8-14-i.992256187.44154734826"
        "/?smtt=580.256747575.7&stm_medium=referral"
    )
    shop, item = parse_url_to_ids(url)
    assert shop == 992256187
    assert item == 44154734826


@pytest.mark.unit
def test_parse_url_no_slug() -> None:
    url = "https://shopee.co.th/i.992256187.44154734826"
    shop, item = parse_url_to_ids(url)
    assert shop == 992256187
    assert item == 44154734826


@pytest.mark.unit
def test_parse_url_rejects_garbage() -> None:
    with pytest.raises(AdapterError, match="URL parse failed"):
        parse_url_to_ids("https://lazada.co.th/products/abc123")


@pytest.mark.unit
def test_load_fixture_round_trip(tmp_path: Path) -> None:
    fixture = {
        "_meta": {"source": "test"},
        "product": {
            "item_id": 1,
            "shop_id": 2,
            "name": "Test Hardware Set",
            "price_min": 99.0,
            "price_max": 199.0,
            "commission_rate": 0.05,
            "rating_star": 4.5,
            "sales": 500,
            "image_url": None,
        },
    }
    path = tmp_path / "test-1.json"
    path.write_text(json.dumps(fixture))
    prod = load_fixture(path)
    assert isinstance(prod, ShopeeProduct)
    assert prod.item_id == 1
    assert prod.shop_id == 2
    assert prod.name == "Test Hardware Set"
    assert prod.commission_rate == 0.05


@pytest.mark.unit
def test_load_fixture_missing_product_key(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text('{"_meta": {}}')
    with pytest.raises(AdapterError, match="missing top-level 'product'"):
        load_fixture(path)


@pytest.mark.unit
def test_load_fixture_missing_file(tmp_path: Path) -> None:
    with pytest.raises(AdapterError, match="not found"):
        load_fixture(tmp_path / "nope.json")


@pytest.mark.unit
def test_find_fixture_by_item_id(tmp_path: Path) -> None:
    (tmp_path / "abc-44154734826.json").write_text("{}")
    (tmp_path / "other-99.json").write_text("{}")
    found = find_fixture_by_item_id(44154734826, tmp_path)
    assert found is not None
    assert found.name == "abc-44154734826.json"
    assert find_fixture_by_item_id(12345, tmp_path) is None
    assert find_fixture_by_item_id(1, Path("/nonexistent")) is None


@pytest.mark.unit
def test_fetch_or_fixture_loads_real_fixture(tmp_path: Path) -> None:
    fx = {
        "product": {
            "item_id": 44154734826,
            "shop_id": 992256187,
            "name": "Socket Bit Set",
            "price_min": 129.0,
            "price_max": 249.0,
            "commission_rate": 0.06,
            "rating_star": 4.7,
            "sales": 1200,
            "image_url": None,
        }
    }
    (tmp_path / "socket-bit-44154734826.json").write_text(json.dumps(fx))
    url = "https://shopee.co.th/socket-bit-i.992256187.44154734826"
    prod = fetch_or_fixture(url=url, fixtures_dir=tmp_path)
    assert prod.item_id == 44154734826
    assert prod.name == "Socket Bit Set"


@pytest.mark.unit
def test_fetch_or_fixture_missing_raises_with_hint(tmp_path: Path) -> None:
    url = "https://shopee.co.th/i.992256187.44154734826"
    with pytest.raises(AdapterError, match="Affiliate Program approval"):
        fetch_or_fixture(url=url, fixtures_dir=tmp_path)


@pytest.mark.unit
def test_fetch_or_fixture_uses_real_curated_fixture() -> None:
    """Smoke test against the actual committed fixture."""
    url = "https://shopee.co.th/...-i.992256187.44154734826/?smtt=foo"
    prod = fetch_or_fixture(url=url)
    assert prod.item_id == 44154734826
    assert "SOCKET" in prod.name or "เจาะ" in prod.name
    assert prod.commission_rate > 0
