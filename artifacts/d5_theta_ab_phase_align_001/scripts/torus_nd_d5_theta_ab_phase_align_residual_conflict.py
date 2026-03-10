#!/usr/bin/env python3
"""Residual-conflict analysis for the Theta_AB_plus_phase_align search results."""

from __future__ import annotations

import argparse
import json
import platform
import time
from collections import Counter, defaultdict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, List, Sequence

from torus_nd_d5_master_field_quotient_family import (
    SCHEMA_PHASE_ALIGN,
    color_map_from_table,
    state_for_vertex,
    state_name,
)

TASK_ID = "D5-THETA-AB-PHASE-ALIGN-001"

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


def _anchor_table(field: Dict[str, object]) -> Dict[int, tuple[int, ...]]:
    return {int(row["state_id"]): tuple(row["permutation"]) for row in field["anchor_table"]["rows"]}


def _field_classes(validation_summary: Dict[str, object]) -> Dict[str, object]:
    classes = {"strict_collapse": [], "clean_nonclock": [], "other": []}
    for item in validation_summary["validated_fields"]:
        pilot = item["results"][:3]
        if all(result["latin"]["incoming_latin"] for result in pilot):
            if all(result["old_collapse_law"]["matches_old_collapse_law"] and result["color0_return"]["strict_clock"] for result in pilot):
                classes["strict_collapse"].append(item["field_index"])
                continue
            if all((not result["old_collapse_law"]["matches_old_collapse_law"]) and result["color0_return"]["clean_frame"] and (not result["color0_return"]["strict_clock"]) for result in pilot):
                classes["clean_nonclock"].append(item["field_index"])
                continue
        classes["other"].append(item["field_index"])
    return classes


def _delta(coords: Sequence[int], m: int) -> int:
    return (coords[3] - coords[1]) % m


def _layer_priority(layer_bucket: object) -> int:
    if layer_bucket in (2, 3, "4+"):
        return 0
    if layer_bucket == 1:
        return 1
    return 2


def _residual_conflict_for_field(
    search_summary: Dict[str, object], validation_summary: Dict[str, object], *, m_values: Sequence[int]
) -> Dict[str, object]:
    classes = _field_classes(validation_summary)
    strict_field_index = classes["strict_collapse"][0]
    field = search_summary["schema_results"][0]["feasible_fields"][strict_field_index]
    table = _anchor_table(field)
    state_space_key = tuple(
        sorted(set(search_summary["schema_results"][0]["pilot_m_values"]) | set(search_summary["schema_results"][0]["stability_m_values"]))
    )

    per_m = []
    canonical = None
    for m in m_values:
        delta_support = defaultdict(set)
        examples = {}
        for q in range(m):
            for w in range(m):
                for v in range(m):
                    for u in range(m):
                        cur = ((-q - w - v - u) % m, q, w, v, u)
                        for _ in range(m):
                            state = state_for_vertex(cur, m, SCHEMA_PHASE_ALIGN)
                            delta = _delta(cur, m)
                            delta_support[state].add(delta)
                            examples.setdefault((state, delta), tuple(cur))
                            cur = color_map_from_table(table, SCHEMA_PHASE_ALIGN, m, cur, 0, state_space_key)

        collision_rows = []
        for state, deltas in delta_support.items():
            if len(deltas) <= 1:
                continue
            sorted_deltas = sorted(deltas)
            row = {
                "state_name": state_name(state),
                "state": {"layer_bucket": state[0], "signature": list(state[1])},
                "delta_values": sorted_deltas,
                "delta_support_size": len(sorted_deltas),
                "all_nonzero": sorted_deltas == list(range(1, m)),
                "example_smallest_delta": list(examples[(state, sorted_deltas[0])]),
                "example_largest_delta": list(examples[(state, sorted_deltas[-1])]),
            }
            collision_rows.append(row)
        collision_rows.sort(
            key=lambda row: (
                0 if row["all_nonzero"] else 1,
                _layer_priority(row["state"]["layer_bucket"]),
                str(row["state"]["layer_bucket"]),
                -row["delta_support_size"],
                row["state_name"],
            )
        )
        full_nonzero_count = sum(1 for row in collision_rows if row["all_nonzero"])
        if canonical is None:
            preferred = [
                row
                for row in collision_rows
                if row["all_nonzero"] and row["state"]["layer_bucket"] in (2, 3, "4+")
            ]
            if preferred:
                canonical = {"m": m, **preferred[0]}
            else:
                for row in collision_rows:
                    if row["all_nonzero"]:
                        canonical = {"m": m, **row}
                        break
        per_m.append(
            {
                "m": m,
                "multi_delta_state_count": len(collision_rows),
                "full_nonzero_support_state_count": full_nonzero_count,
                "support_histogram": {
                    str(size): count
                    for size, count in sorted(Counter(row["delta_support_size"] for row in collision_rows).items())
                },
                "example_rows": collision_rows[:40],
            }
        )

    return {
        "field_classes": classes,
        "strict_collapse_field_index": strict_field_index,
        "candidate_next_bit": "predecessor_tail_nonzero_phase",
        "candidate_next_bit_description": (
            "A second refinement should separate at least one nonzero delta tail class inside phase_align=0, "
            "rather than adding more anchor freedom."
        ),
        "per_m": per_m,
        "canonical_residual_conflict": canonical,
    }


def run_analysis(search_summary: Dict[str, object], validation_summary: Dict[str, object], *, m_values: Sequence[int]) -> Dict[str, object]:
    start = time.perf_counter()
    residual = _residual_conflict_for_field(search_summary, validation_summary, m_values=m_values)
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": {"python_version": platform.python_version(), "rich_version": _rich_version()},
        "residual_conflict": residual,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    residual = summary["residual_conflict"]
    canonical = residual["canonical_residual_conflict"]
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        f"strict_collapse_fields: {residual['field_classes']['strict_collapse']}",
        f"clean_nonclock_fields: {residual['field_classes']['clean_nonclock']}",
    ]
    if canonical is not None:
        lines.append(
            f"canonical_residual_conflict: m={canonical['m']} state={canonical['state_name']} "
            f"delta={canonical['delta_values'][:10]} all_nonzero={canonical['all_nonzero']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze residual conflicts after the phase-align quotient refinement.")
    parser.add_argument("--search-summary-json", type=Path, required=True, help="phase-align search summary JSON")
    parser.add_argument("--validation-summary-json", type=Path, required=True, help="phase-align validation summary JSON")
    parser.add_argument("--m-list", default="5,7,9,11,13", help="comma-separated moduli to analyze")
    parser.add_argument("--out", type=Path, required=True, help="write residual conflict JSON here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    search_summary = json.loads(args.search_summary_json.read_text())
    validation_summary = json.loads(args.validation_summary_json.read_text())
    summary = run_analysis(search_summary, validation_summary, m_values=_parse_m_list(args.m_list))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
