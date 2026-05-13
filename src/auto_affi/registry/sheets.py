"""SheetsRegistry — Google Sheets backend via gspread + service account.

Gated behind the optional ``gspread`` dependency. When ``gspread`` isn't
installed (or the service-account JSON isn't valid) the import or constructor
raises and the caller falls back to ``LocalJsonlRegistry``.

Schema convention: tabs named ``products``, ``runs``, ``storyboards``;
row 1 is the header row, columns match ``ProductEntry`` / ``RunEntry`` /
``StoryboardSceneOverride`` field names verbatim. List fields are stored as
``;``-joined strings (newline-free for cell safety) and parsed on read.

The implementation is intentionally thin — gspread does the auth + range
ops; this module just translates between Sheet rows and pydantic models.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from auto_affi.registry.models import ProductEntry, RunEntry, StoryboardSceneOverride


_SCOPES = (
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
)


def _split_list(raw: str) -> list[str]:
    if not raw:
        return []
    return [s.strip() for s in raw.split(";") if s.strip()]


def _join_list(items: list[str]) -> str:
    return ";".join(s.replace(";", ",").strip() for s in items if s.strip())


def _coerce_value(field_name: str, raw: Any, target_type: Any) -> Any:
    """Translate a Sheet cell string into a python value matching the model field."""
    if raw is None or raw == "":
        return None
    if field_name == "persona_pain_points":
        return _split_list(str(raw))
    s = str(raw).strip()
    origin = getattr(target_type, "__origin__", None)
    if target_type is int or origin is int:
        return int(float(s))
    if target_type is float or origin is float:
        return float(s)
    if target_type is bool:
        return s.lower() in ("true", "1", "yes", "y")
    if target_type is datetime or origin is datetime:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    return s


def _row_to_model(row: dict[str, Any], cls: type) -> Any:
    fields = {}
    for name, info in cls.model_fields.items():
        raw = row.get(name, "")
        try:
            val = _coerce_value(name, raw, info.annotation)
        except (ValueError, TypeError):
            val = None
        if val is None:
            if info.is_required():
                # Required + empty → skip this row
                return None
            continue
        fields[name] = val
    return cls(**fields)


def _model_to_row(model: Any) -> dict[str, Any]:
    raw = model.model_dump(mode="json")
    out: dict[str, Any] = {}
    for k, v in raw.items():
        if isinstance(v, list):
            out[k] = _join_list([str(x) for x in v])
        elif v is None:
            out[k] = ""
        else:
            out[k] = v
    return out


class SheetsRegistry:
    """Google-Sheets-backed registry. Requires ``gspread`` + service account."""

    def __init__(self, *, sheet_id: str, service_account_json: str) -> None:
        try:
            import gspread  # type: ignore[import-not-found]
            from google.oauth2.service_account import Credentials  # type: ignore[import-not-found]
        except ImportError as exc:  # pragma: no cover — depends on optional dep
            raise ImportError(
                "SheetsRegistry requires `gspread` + `google-auth`. "
                "Add to pyproject [adapters] group and re-install."
            ) from exc

        sa_payload: dict[str, Any]
        candidate = Path(service_account_json)
        if candidate.exists():
            sa_payload = json.loads(candidate.read_text(encoding="utf-8"))
        else:
            sa_payload = json.loads(service_account_json)

        creds = Credentials.from_service_account_info(sa_payload, scopes=list(_SCOPES))
        self._gc = gspread.authorize(creds)
        self._book = self._gc.open_by_key(sheet_id)

    # ---- internal helpers --------------------------------------------- #

    def _ws(self, name: str):
        try:
            return self._book.worksheet(name)
        except Exception:
            cols = {
                "products": list(ProductEntry.model_fields.keys()),
                "runs": list(RunEntry.model_fields.keys()),
                "storyboards": list(StoryboardSceneOverride.model_fields.keys()),
            }[name]
            ws = self._book.add_worksheet(title=name, rows=1000, cols=max(len(cols), 12))
            ws.append_row(cols, value_input_option="RAW")
            return ws

    def _read_all(self, ws_name: str, cls: type) -> list[Any]:
        ws = self._ws(ws_name)
        rows = ws.get_all_records()
        out = []
        for r in rows:
            m = _row_to_model(r, cls)
            if m is not None:
                out.append(m)
        return out

    # ---- products ----------------------------------------------------- #

    def find_product_by_item_id(self, item_id: int) -> ProductEntry | None:
        for p in self._read_all("products", ProductEntry):
            if p.item_id == item_id:
                return p
        return None

    def find_product_by_url(self, url: str) -> ProductEntry | None:
        for p in self._read_all("products", ProductEntry):
            if p.url == url:
                return p
        return None

    def list_products(self, *, status: str | None = "ACTIVE") -> list[ProductEntry]:
        rows = self._read_all("products", ProductEntry)
        if status is None:
            return rows
        return [p for p in rows if p.status == status]

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
        rows = self._read_all("products", ProductEntry)
        next_no = 1 + max((p.order_no for p in rows), default=0)
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
        ws = self._ws("products")
        header = ws.row_values(1)
        row_dict = _model_to_row(entry)
        ws.append_row(
            [row_dict.get(h, "") for h in header],
            value_input_option="USER_ENTERED",
        )
        return entry

    # ---- runs --------------------------------------------------------- #

    def start_run(
        self, *, order_no: int, run_id: str, publish_mode: str = "dry_run"
    ) -> RunEntry:
        existing = [
            r for r in self._read_all("runs", RunEntry) if r.order_no == order_no
        ]
        next_no = 1 + max((r.run_no for r in existing), default=0)
        entry = RunEntry(
            run_no=next_no,
            order_no=order_no,
            run_id=run_id,
            publish_mode=publish_mode,  # type: ignore[arg-type]
        )
        ws = self._ws("runs")
        header = ws.row_values(1)
        ws.append_row(
            [_model_to_row(entry).get(h, "") for h in header],
            value_input_option="USER_ENTERED",
        )
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
        ws = self._ws("runs")
        rows = ws.get_all_records()
        header = ws.row_values(1)
        target_row_idx = None
        for i, r in enumerate(rows, start=2):  # row 1 = header
            try:
                if int(r.get("order_no", 0)) == order_no and int(r.get("run_no", 0)) == run_no:
                    target_row_idx = i
                    break
            except (ValueError, TypeError):
                continue
        if target_row_idx is None:
            raise KeyError(f"run order_no={order_no} run_no={run_no} not in sheet")
        updates: dict[str, Any] = {
            "status": status,
            "ended_at": datetime.utcnow().isoformat() + "Z",
            "total_cost_thb": total_cost_thb,
            "gcs_prefix": gcs_prefix,
            "final_mp4_gs_uri": final_mp4_gs_uri,
            "scene_count": scene_count,
            "last_decision": last_decision,
            "error": error,
        }
        for col_name, value in updates.items():
            if col_name not in header:
                continue
            col_idx = header.index(col_name) + 1
            ws.update_cell(target_row_idx, col_idx, value)
        # Re-read the row for the caller
        for r in self._read_all("runs", RunEntry):
            if r.order_no == order_no and r.run_no == run_no:
                return r
        raise KeyError(f"run order_no={order_no} run_no={run_no} re-read failed")

    def list_runs(self, *, order_no: int | None = None) -> list[RunEntry]:
        rows = self._read_all("runs", RunEntry)
        if order_no is None:
            return rows
        return [r for r in rows if r.order_no == order_no]

    # ---- storyboard overrides ----------------------------------------- #

    def get_storyboard_overrides(self, order_no: int) -> list[StoryboardSceneOverride]:
        rows = self._read_all("storyboards", StoryboardSceneOverride)
        rows = [r for r in rows if r.order_no == order_no]
        rows.sort(key=lambda r: r.scene_idx)
        return rows
