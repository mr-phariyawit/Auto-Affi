"""Smoke + lifecycle tests for LocalJsonlRegistry."""

from __future__ import annotations

import pytest

from auto_affi.registry import LocalJsonlRegistry, build_run_prefix, build_stage_prefix
from auto_affi.registry.gcs_paths import build_order_prefix
from auto_affi.registry.models import StoryboardSceneOverride


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


def test_list_products_status_filter(registry: LocalJsonlRegistry) -> None:
    """Default lists ACTIVE only; status=None lists all; explicit status filters."""
    registry.register_product(
        item_id=1, shop_id=1, url="u1", name="active-one",
        niche="Electronics", persona_label="p", angle="a",
    )
    # `status` is a real ProductEntry field, so it flows through **extras.
    registry.register_product(
        item_id=2, shop_id=1, url="u2", name="archived-one",
        niche="Beauty", persona_label="p", angle="a",
        status="ARCHIVED",
    )

    active = registry.list_products()  # default status="ACTIVE"
    assert [p.name for p in active] == ["active-one"]

    everything = registry.list_products(status=None)
    assert {p.name for p in everything} == {"active-one", "archived-one"}

    archived = registry.list_products(status="ARCHIVED")
    assert [p.name for p in archived] == ["archived-one"]


def test_register_product_extras_kept_and_unknown_dropped(registry: LocalJsonlRegistry) -> None:
    """Known extra fields persist; unknown kwargs are filtered out (no extra='forbid' crash)."""
    p = registry.register_product(
        item_id=7, shop_id=1, url="u", name="n",
        niche="Electronics", persona_label="p", angle="a",
        price_min_thb=99.0,            # real ProductEntry field -> kept
        not_a_real_field="ignored",    # unknown -> filtered before construction
    )
    assert p.price_min_thb == 99.0
    assert not hasattr(p, "not_a_real_field")
    # round-trips through disk identically
    assert registry.find_product_by_item_id(7).price_min_thb == 99.0


def test_list_runs_across_all_orders(registry: LocalJsonlRegistry) -> None:
    """list_runs(order_no=None) returns runs from every order."""
    a = registry.register_product(
        item_id=1, shop_id=1, url="ua", name="a",
        niche="Electronics", persona_label="p", angle="a",
    )
    b = registry.register_product(
        item_id=2, shop_id=1, url="ub", name="b",
        niche="Beauty", persona_label="p", angle="a",
    )
    registry.start_run(order_no=a.order_no, run_id="a1")
    registry.start_run(order_no=b.order_no, run_id="b1")

    all_runs = registry.list_runs()  # order_no=None
    assert {r.run_id for r in all_runs} == {"a1", "b1"}
    assert {r.run_id for r in registry.list_runs(order_no=a.order_no)} == {"a1"}


def _append_override(registry: LocalJsonlRegistry, **fields) -> None:
    row = StoryboardSceneOverride(**fields)
    with registry.storyboards_path.open("a", encoding="utf-8") as fp:
        fp.write(row.model_dump_json() + "\n")


def test_get_storyboard_overrides_filters_and_sorts(registry: LocalJsonlRegistry) -> None:
    """Overrides are filtered by order_no and returned sorted by scene_idx."""
    # order 1: written out of scene order on purpose
    for idx in (2, 0, 1):
        _append_override(registry, order_no=1, scene_idx=idx, visual_prompt=f"scene {idx}")
    # order 2: must not leak into order 1's result
    _append_override(registry, order_no=2, scene_idx=0, visual_prompt="other order")

    got = registry.get_storyboard_overrides(1)
    assert [o.scene_idx for o in got] == [0, 1, 2]      # sorted ascending
    assert all(o.order_no == 1 for o in got)            # filtered to order 1

    assert [o.scene_idx for o in registry.get_storyboard_overrides(2)] == [0]
    assert registry.get_storyboard_overrides(999) == []  # no overrides -> empty
