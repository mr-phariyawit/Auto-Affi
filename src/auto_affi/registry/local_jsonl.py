"""LocalJsonlRegistry — append-only JSONL backend.

Three files under ``data/registry/``:

* ``products.jsonl`` — one ``ProductEntry`` per line
* ``runs.jsonl`` — one ``RunEntry`` per line (last write wins on run_no)
* ``storyboards.jsonl`` — one ``StoryboardSceneOverride`` per line

Atomic writes via temp file + rename to survive mid-write crashes. Order/run
numbering is computed from the max(order_no/run_no) already on disk so
sequence holes never appear.

This backend is the bootstrap path until ``AUTO_AFFI__SHEETS_ID`` +
service-account credentials land. Once Sheets is wired the same data shape
ports across: each JSONL row maps 1:1 to a Sheet row.
"""

from __future__ import annotations

import contextlib
import json  # noqa: F401 — kept for future use / clarity
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from auto_affi.registry.models import ProductEntry, RunEntry, StoryboardSceneOverride


def _atomic_write(path: Path, content: str) -> None:
    """Write ``content`` to ``path`` via temp + rename so crash mid-write is safe."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fp:
            fp.write(content)
        os.replace(tmp_name, path)
    except Exception:
        with contextlib.suppress(OSError):
            os.unlink(tmp_name)
        raise


class LocalJsonlRegistry:
    """File-backed registry. Implements the ``Registry`` protocol."""

    def __init__(self, root: Path | str = "data/registry") -> None:
        self.root = Path(root)
        self.products_path = self.root / "products.jsonl"
        self.runs_path = self.root / "runs.jsonl"
        self.storyboards_path = self.root / "storyboards.jsonl"
        self.root.mkdir(parents=True, exist_ok=True)
        for p in (self.products_path, self.runs_path, self.storyboards_path):
            if not p.exists():
                p.write_text("", encoding="utf-8")

    # ---- product reads ------------------------------------------------ #

    def _iter_products(self) -> list[ProductEntry]:
        out: list[ProductEntry] = []
        for line in self.products_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            out.append(ProductEntry.model_validate_json(line))
        return out

    def find_product_by_item_id(self, item_id: int) -> ProductEntry | None:
        for p in self._iter_products():
            if p.item_id == item_id:
                return p
        return None

    def find_product_by_url(self, url: str) -> ProductEntry | None:
        for p in self._iter_products():
            if p.url == url:
                return p
        return None

    def list_products(self, *, status: str | None = "ACTIVE") -> list[ProductEntry]:
        rows = self._iter_products()
        if status is None:
            return rows
        return [p for p in rows if p.status == status]

    # ---- product writes ----------------------------------------------- #

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
        existing = self.find_product_by_item_id(item_id)
        if existing is not None:
            return existing
        next_no = 1 + max((p.order_no for p in self._iter_products()), default=0)
        entry = ProductEntry(
            order_no=next_no,
            item_id=item_id,
            shop_id=shop_id,
            url=url,
            name=name,
            niche=niche,
            sub_niche=sub_niche,
            persona_label=persona_label,
            persona_pain_points=persona_pain_points or [],
            angle=angle,
            hook_template=hook_template,
            cta_text=cta_text,
            hypothesis=hypothesis,
            expected_ctr=expected_ctr,
            **{k: v for k, v in extras.items() if k in ProductEntry.model_fields},
        )
        with self.products_path.open("a", encoding="utf-8") as fp:
            fp.write(entry.model_dump_json() + "\n")
        return entry

    # ---- run lifecycle ------------------------------------------------ #

    def _iter_runs(self) -> list[RunEntry]:
        rows = []
        for line in self.runs_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            rows.append(RunEntry.model_validate_json(line))
        # Last-write-wins on (order_no, run_no)
        latest: dict[tuple[int, int], RunEntry] = {}
        for r in rows:
            latest[(r.order_no, r.run_no)] = r
        return list(latest.values())

    def start_run(
        self, *, order_no: int, run_id: str, publish_mode: str = "dry_run"
    ) -> RunEntry:
        existing = [r for r in self._iter_runs() if r.order_no == order_no]
        next_no = 1 + max((r.run_no for r in existing), default=0)
        entry = RunEntry(
            run_no=next_no,
            order_no=order_no,
            run_id=run_id,
            publish_mode=publish_mode,  # type: ignore[arg-type]
        )
        with self.runs_path.open("a", encoding="utf-8") as fp:
            fp.write(entry.model_dump_json() + "\n")
        return entry

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
    ) -> RunEntry:
        rows = self._iter_runs()
        idx = next(
            (i for i, r in enumerate(rows) if r.order_no == order_no and r.run_no == run_no),
            None,
        )
        if idx is None:
            raise KeyError(f"run order_no={order_no} run_no={run_no} not found")
        rows[idx] = rows[idx].model_copy(
            update={
                "status": status,
                "ended_at": datetime.now(timezone.utc),
                "total_cost_thb": total_cost_thb,
                "gcs_prefix": gcs_prefix,
                "final_mp4_gs_uri": final_mp4_gs_uri,
                "scene_count": scene_count,
                "last_decision": last_decision,
                "error": error,
            }
        )
        body = "\n".join(r.model_dump_json() for r in rows) + ("\n" if rows else "")
        _atomic_write(self.runs_path, body)
        return rows[idx]

    def list_runs(self, *, order_no: int | None = None) -> list[RunEntry]:
        rows = self._iter_runs()
        if order_no is None:
            return rows
        return [r for r in rows if r.order_no == order_no]

    # ---- storyboard overrides ----------------------------------------- #

    def get_storyboard_overrides(self, order_no: int) -> list[StoryboardSceneOverride]:
        out = []
        for line in self.storyboards_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            row = StoryboardSceneOverride.model_validate_json(line)
            if row.order_no == order_no:
                out.append(row)
        out.sort(key=lambda r: r.scene_idx)
        return out
