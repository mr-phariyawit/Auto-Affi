"""Product + run registry — JSONL-backed source of truth for orders.

The registry replaces hard-coded niche briefs and per-product knowledge.
Briefs and per-product storyboard overrides live in JSONL files under
``data/registry/``; runs are logged back for ops visibility.

Phase-1 offline backend: ``LocalJsonlRegistry`` only.
Sheets backend (``SheetsRegistry``) is deferred to Phase 2 — gspread is not
a runtime dependency in the offline slice.

Two backends share the same ``Registry`` protocol:

* ``LocalJsonlRegistry`` — bootstrap / offline mode. Reads + writes
  ``data/registry/{products,runs,storyboards}.jsonl``. Active in CI + dev.
* ``SheetsRegistry`` — production mode (Phase 2). Talks to a Google Sheet via
  a service account. Active when ``AUTO_AFFI__SHEETS_ID`` + service-account
  JSON are set AND gspread is installed.

Order numbering is monotonically increasing per registry. Run numbering is
monotonically increasing per order. GCS path helpers embed both coordinates
(``orders/<order_no:04d>/runs/<run_no:04d>/...``) so every artifact is
locatable by (order, run) without grep-ing the Sheet.
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
