"""Registry protocol — the contract both backends honor.

Code that needs the registry should depend on ``Registry``, never on
``LocalJsonlRegistry`` directly. ``registry_from_env()`` is the standard
construction site — it picks the backend based on environment variables.

Sheets backend is out of scope for Phase-1 offline slice. If
``AUTO_AFFI__SHEETS_ID`` + service-account are set but gspread is not installed,
we fall through silently to ``LocalJsonlRegistry``.
"""

from __future__ import annotations

import os
from typing import Protocol, cast, runtime_checkable

from auto_affi.registry.models import ProductEntry, RunEntry, StoryboardSceneOverride


@runtime_checkable
class Registry(Protocol):
    """The minimum surface every backend must provide."""

    def find_product_by_item_id(self, item_id: int) -> ProductEntry | None: ...

    def find_product_by_url(self, url: str) -> ProductEntry | None: ...

    def register_product(
        self,
        *,
        item_id: int,
        shop_id: int,
        url: str,
        name: str,
        niche: str,
        sub_niche: str = "",
        persona_label: str,
        persona_pain_points: list[str] | None = None,
        angle: str,
        hook_template: str = "curiosity_gap",
        cta_text: str = "",
        hypothesis: str = "",
        expected_ctr: float = 0.025,
        **extras: object,
    ) -> ProductEntry:
        """Append a new product row, return the entry (with assigned order_no)."""
        ...

    def list_products(self, *, status: str | None = "ACTIVE") -> list[ProductEntry]: ...

    def start_run(
        self, *, order_no: int, run_id: str, publish_mode: str = "dry_run"
    ) -> RunEntry: ...

    def finalize_run(
        self,
        *,
        run_no: int,
        order_no: int,
        status: str,
        total_cost_thb: float = 0.0,
        gcs_prefix: str = "",
        final_mp4_gs_uri: str = "",
        scene_count: int = 0,
        last_decision: str = "",
        error: str = "",
    ) -> RunEntry: ...

    def list_runs(self, *, order_no: int | None = None) -> list[RunEntry]: ...

    def get_storyboard_overrides(self, order_no: int) -> list[StoryboardSceneOverride]:
        """Return any scene overrides for this product (may be empty)."""
        ...


def registry_from_env() -> Registry:
    """Pick the right backend based on env. Local JSONL is the safe default.

    Switches to ``SheetsRegistry`` when both ``AUTO_AFFI__SHEETS_ID`` and a
    service-account credential are present AND gspread is installed. Until
    then everything stays in ``data/registry/*.jsonl`` so the architecture
    works in dev/CI without cloud credentials.
    """
    sheet_id = os.environ.get("AUTO_AFFI__SHEETS_ID", "").strip()
    sa_json = (
        os.environ.get("AUTO_AFFI__GCP_SERVICE_ACCOUNT_JSON")
        or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        or ""
    ).strip()
    if sheet_id and sa_json:
        try:
            from auto_affi.registry.sheets import SheetsRegistry  # type: ignore[import-not-found]

            return cast(Registry, SheetsRegistry(sheet_id=sheet_id, service_account_json=sa_json))
        except ImportError:
            # gspread not installed — fall through to local
            pass

    from auto_affi.registry.local_jsonl import LocalJsonlRegistry

    return LocalJsonlRegistry()
