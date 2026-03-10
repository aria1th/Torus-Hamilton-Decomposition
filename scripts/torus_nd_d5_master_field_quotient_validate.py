#!/usr/bin/env python3
"""Validate solved d=5 master-field quotient candidates."""

from __future__ import annotations

import argparse
import json
import platform
import time
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, List, Sequence

from torus_nd_d5_master_field_quotient_family import (
    SCHEMA_BY_NAME,
    TASK_ID,
    analyze_latin,
    color_cycle_summary,
    first_return_qwu_for_color0,
)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover - optional dependency
    Console = None


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _rich_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def _load_tables(search_summary: Dict[str, object], schema_names: Sequence[str] | None) -> List[Dict[str, object]]:
    out = []
    wanted = set(schema_names or [])
    for item in search_summary["schema_results"]:
        if wanted and item["schema"] not in wanted:
            continue
        if "permutation_table" not in item:
            continue
        out.append(item)
    return out


def _table_dict(schema_result: Dict[str, object]) -> Dict[int, Sequence[int]]:
    return {int(row["state_id"]): tuple(int(value) for value in row["permutation"]) for row in schema_result["permutation_table"]["rows"]}


def validate_schema_result(schema_result: Dict[str, object], m_values: Sequence[int]) -> Dict[str, object]:
    schema = SCHEMA_BY_NAME[schema_result["schema"]]
    state_space_key = tuple(sorted(set(schema_result["pilot_m_values"]) | set(schema_result["stability_m_values"])))
    table = _table_dict(schema_result)
    return {
        "schema": schema_result["schema"],
        "schema_description": schema.description,
        "m_values": list(m_values),
        "results": [
            {
                "m": m,
                "latin": analyze_latin(table, schema, m, state_space_key),
                "color_cycles": color_cycle_summary(table, schema, m, state_space_key),
                "color0_return": first_return_qwu_for_color0(table, schema, m, state_space_key),
            }
            for m in m_values
        ],
    }


def run_validation(search_summary: Dict[str, object], *, m_values: Sequence[int], schema_names: Sequence[str] | None) -> Dict[str, object]:
    start = time.perf_counter()
    solved = _load_tables(search_summary, schema_names)
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": {"python_version": platform.python_version(), "rich_version": _rich_version()},
        "validated_schemas": [validate_schema_result(item, m_values) for item in solved],
        "skipped_schemas": [
            {"schema": item["schema"], "solver_status": item["solver_status"]}
            for item in search_summary["schema_results"]
            if "permutation_table" not in item and (not schema_names or item["schema"] in schema_names)
        ],
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        f"validated_schemas: {len(summary['validated_schemas'])}",
        f"skipped_schemas: {len(summary['skipped_schemas'])}",
    ]
    for item in summary["validated_schemas"]:
        first = item["results"][0]
        lines.append(
            f"{item['schema']}: m={first['m']} latin={first['latin']['incoming_latin']} "
            f"U={first['color0_return']['U_cycle_lengths']} mono={first['color0_return']['monodromies']}"
        )
    for item in summary["skipped_schemas"]:
        lines.append(f"{item['schema']}: skipped ({item['solver_status']})")
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate solved d=5 master-field quotient candidates.")
    parser.add_argument("--search-summary-json", type=Path, required=True, help="search summary JSON")
    parser.add_argument("--m-list", default="5,7,9,11,13", help="comma-separated moduli to validate")
    parser.add_argument("--schemas", help="optional comma-separated schema filter")
    parser.add_argument("--out", type=Path, help="write JSON summary to this path")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    payload = json.loads(args.search_summary_json.read_text())
    schema_names = [part.strip() for part in args.schemas.split(",") if part.strip()] if args.schemas else None
    summary = run_validation(payload, m_values=_parse_m_list(args.m_list), schema_names=schema_names)

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2))

    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
