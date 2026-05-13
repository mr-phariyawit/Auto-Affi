"""Product + run registry — Sheets-backed source of truth for orders.

The registry replaces hard-coded niche briefs and per-product knowledge that
previously lived in `auto_affi.ops.run_once._NICHE_BRIEFS` and the writers'-room
fallback templates. Briefs and per-product storyboard overrides live in a
Google Sheet; runs are logged back to a runs tab for ops visibility.

Two backends, same `Registry` protocol:

* `LocalJsonlRegistry` — bootstrap mode. Reads + writes
  `data/registry/{products,runs,storyboards}.jsonl`. Active when no service
  account / sheet id is configured. Useful in CI + dev.
* `SheetsRegistry` — production mode. Talks to a Google Sheet via a service
  account. Active when `AUTO_AFFI__SHEETS_ID` + service-account JSON are set.

Order numbering is monotonically increasing per registry. Run numbering is
monotonically increasing per order. GCS paths embed both
(`gs://<bucket>/orders/<order_no:04d>/runs/<run_no:04d>/...`) so every artifact
is locatable by (order, run) coordinates without grep-ing the Sheet.
"""

from auto_affi.registry.gcs_paths import (
    build_gs_uri,
    build_order_prefix,
    build_run_prefix,
    build_stage_prefix,
)
from auto_affi.registry.local_jsonl import LocalJsonlRegistry
from auto_affi.registry.models import ProductEntry, RunEntry, StoryboardSceneOverride
from auto_affi.registry.protocol import Registry, registry_from_env

__all__ = [
    "LocalJsonlRegistry",
    "ProductEntry",
    "Registry",
    "RunEntry",
    "StoryboardSceneOverride",
    "build_gs_uri",
    "build_order_prefix",
    "build_run_prefix",
    "build_stage_prefix",
    "registry_from_env",
]
