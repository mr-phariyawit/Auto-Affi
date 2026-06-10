"""Smoke + lifecycle tests for LocalJsonlRegistry."""

from __future__ import annotations

import pytest

from auto_affi.registry import LocalJsonlRegistry, build_run_prefix, build_stage_prefix
from auto_affi.registry.gcs_paths import build_order_prefix


@pytest.fixture
def registry(tmp_path) -> LocalJsonlRegistry:
    return LocalJsonlRegistry(root=tmp_path / "registry")


def test_register_product_assigns_sequential_order_no(registry: LocalJsonlRegistry) -> None:
    a = registry.register_product(
        item_id=1, shop_id=10, url="u1", name="n1",
        niche="Electronics", persona_label="p", angle="a",
    )
    b = registry.register_product(
        item_id=2, shop_id=10, url="u2", name="n2",
        niche="Beauty", persona_label="p", angle="a",
    )
    assert a.order_no == 1
    assert b.order_no == 2


def test_register_product_idempotent_by_item_id(registry: LocalJsonlRegistry) -> None:
    a = registry.register_product(
        item_id=42, shop_id=10, url="u", name="n",
        niche="Electronics", persona_label="p", angle="a",
    )
    again = registry.register_product(
        item_id=42, shop_id=999, url="other", name="other-name",
        niche="Beauty", persona_label="p", angle="a",
    )
    assert again.order_no == a.order_no
    assert again.shop_id == 10  # original kept
    assert registry.list_products() == [a]


def test_find_product_by_url(registry: LocalJsonlRegistry) -> None:
    p = registry.register_product(
        item_id=1, shop_id=10, url="https://shopee/x", name="n",
        niche="Electronics", persona_label="p", angle="a",
    )
    assert registry.find_product_by_url("https://shopee/x") == p
    assert registry.find_product_by_url("not-there") is None


def test_run_lifecycle(registry: LocalJsonlRegistry) -> None:
    product = registry.register_product(
        item_id=1, shop_id=1, url="u", name="n",
        niche="Electronics", persona_label="p", angle="a",
    )
    r1 = registry.start_run(order_no=product.order_no, run_id="abc")
    r2 = registry.start_run(order_no=product.order_no, run_id="def")
    assert r1.run_no == 1
    assert r2.run_no == 2
    final = registry.finalize_run(
        run_no=r1.run_no, order_no=product.order_no,
        status="APPROVED", total_cost_thb=12.5,
        gcs_prefix=build_run_prefix(product.order_no, r1.run_no),
        scene_count=5, last_decision="dry-run-ok",
    )
    assert final.status == "APPROVED"
    assert final.total_cost_thb == 12.5
    assert final.scene_count == 5
    runs = registry.list_runs(order_no=product.order_no)
    # Both runs persist; finalized one carries the new status.
    assert {(r.run_no, r.status) for r in runs} == {(1, "APPROVED"), (2, "IN_PROGRESS")}


def test_run_numbering_scoped_per_order(registry: LocalJsonlRegistry) -> None:
    a = registry.register_product(
        item_id=1, shop_id=1, url="ua", name="a",
        niche="Electronics", persona_label="p", angle="a",
    )
    b = registry.register_product(
        item_id=2, shop_id=1, url="ub", name="b",
        niche="Beauty", persona_label="p", angle="a",
    )
    ra1 = registry.start_run(order_no=a.order_no, run_id="a1")
    rb1 = registry.start_run(order_no=b.order_no, run_id="b1")
    ra2 = registry.start_run(order_no=a.order_no, run_id="a2")
    assert (ra1.run_no, rb1.run_no, ra2.run_no) == (1, 1, 2)


def test_gcs_path_helpers() -> None:
    assert build_order_prefix(1) == "orders/0001"
    assert build_run_prefix(1, 1) == "orders/0001/runs/0001"
    assert build_run_prefix(12, 345) == "orders/0012/runs/0345"
    assert build_stage_prefix(1, 1, 4) == "orders/0001/runs/0001/stage4-visuals"
    assert build_stage_prefix(1, 1, 10) == "orders/0001/runs/0001/stage10-publish"
    with pytest.raises(ValueError):
        build_stage_prefix(1, 1, 99)


def test_finalize_run_missing_raises(registry: LocalJsonlRegistry) -> None:
    with pytest.raises(KeyError):
        registry.finalize_run(run_no=1, order_no=1, status="APPROVED")
