#!/usr/bin/env python3
"""Validate saved joined-quotient d=5 master-field candidates."""

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
    anchor_values_to_permutation_table,
    analyze_latin,
    color_cycle_summary,
    first_return_qwu_for_color0,
    schema_state_space,
)

TASK_ID = "D5-MASTER-FIELD-JOIN-QUOTIENT-001"

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


def _anchor_values(field: Dict[str, object]) -> Dict[int, int]:
    return {int(row["state_id"]): int(row["anchor_value"]) for row in field["anchor_table"]["rows"]}


def run_validation(search_summary: Dict[str, object], *, m_values: Sequence[int], field_limit: int) -> Dict[str, object]:
    start = time.perf_counter()
    results = []
    for schema_result in search_summary["schema_results"]:
        if "feasible_fields" not in schema_result:
            continue
        schema = SCHEMA_BY_NAME[schema_result["schema"]]
        state_space_key = tuple(sorted(set(schema_result["pilot_m_values"]) | set(schema_result["stability_m_values"])))
        states = schema_state_space(schema.name, state_space_key)
        for field_index, field in enumerate(schema_result["feasible_fields"][:field_limit]):
            anchor_values = _anchor_values(field)
            perm_table = anchor_values_to_permutation_table(states, anchor_values)
            results.append(
                {
                    "schema": schema.name,
                    "field_index": field_index,
                    "results": [
                        {
                            "m": m,
                            "latin": analyze_latin(perm_table, schema, m, state_space_key),
                            "color_cycles": color_cycle_summary(perm_table, schema, m, state_space_key),
                            "color0_return": first_return_qwu_for_color0(perm_table, schema, m, state_space_key),
                        }
                        for m in m_values
                    ],
                }
            )
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": {"python_version": platform.python_version(), "rich_version": _rich_version()},
        "validated_fields": results,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        f"validated_fields: {len(summary['validated_fields'])}",
    ]
    for item in summary["validated_fields"][:5]:
        first = item["results"][0]
        lines.append(
            f"{item['schema']} field#{item['field_index']}: m={first['m']} "
            f"latin={first['latin']['incoming_latin']} clean_frame={first['color0_return']['clean_frame']} "
            f"strict_clock={first['color0_return']['strict_clock']} U={first['color0_return']['U_cycle_lengths']} "
            f"mono={first['color0_return']['monodromies']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate joined-quotient master-field candidates.")
    parser.add_argument("--search-summary-json", type=Path, required=True, help="joined-quotient search summary JSON")
    parser.add_argument("--m-list", default="5,7,9,11,13", help="comma-separated moduli to validate")
    parser.add_argument("--field-limit", type=int, default=10, help="max fields per schema to validate")
    parser.add_argument("--out", type=Path, help="write JSON summary to this path")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    payload = json.loads(args.search_summary_json.read_text())
    summary = run_validation(payload, m_values=_parse_m_list(args.m_list), field_limit=args.field_limit)

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2))

    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
