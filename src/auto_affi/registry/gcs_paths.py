"""GCS path conventions for orders + runs.

All artifacts produced by a production run live under
``gs://<bucket>/orders/<order_no:04d>/runs/<run_no:04d>/...``.

Stage-level prefixes follow the 10-stage ADR-007 vocabulary so any operator
can `gsutil ls` a run and find brief / script / storyboard / visuals /
animatics / vo / music / final / compliance / publish without consulting code.

Note: This module builds path strings only. No GCS SDK imported.
"""

from __future__ import annotations


def build_order_prefix(order_no: int) -> str:
    """``orders/0001`` — used for the product snapshot + per-order metadata."""
    return f"orders/{order_no:04d}"


def build_run_prefix(order_no: int, run_no: int) -> str:
    """``orders/0001/runs/0001`` — root for everything a single run produces."""
    return f"{build_order_prefix(order_no)}/runs/{run_no:04d}"


STAGE_DIR: dict[int, str] = {
    1: "stage1-brief",
    2: "stage2-script",
    3: "stage3-storyboard",
    4: "stage4-visuals",
    5: "stage5-animatics",
    6: "stage6-vo",
    7: "stage7-music",
    8: "stage8-final",
    9: "stage9-compliance",
    10: "stage10-publish",
}


def build_stage_prefix(order_no: int, run_no: int, stage_id: int) -> str:
    """``orders/0001/runs/0001/stage4-visuals``."""
    if stage_id not in STAGE_DIR:
        raise ValueError(f"Unknown stage_id {stage_id}; expected 1..10")
    return f"{build_run_prefix(order_no, run_no)}/{STAGE_DIR[stage_id]}"


def build_gs_uri(bucket: str, *parts: str) -> str:
    """Build a `gs://bucket/parts/...` URI from parts."""
    tail = "/".join(p.strip("/") for p in parts if p)
    return f"gs://{bucket}/{tail}" if tail else f"gs://{bucket}"
