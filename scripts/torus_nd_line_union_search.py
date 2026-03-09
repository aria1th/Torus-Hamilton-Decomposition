#!/usr/bin/env python3
"""Derive the d=4 line-union witness from the reduced layer-2 gate family."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from candidates.hyperplane_fusion_line_union_v1 import direction_tuple as line_union_direction_tuple
from torus_nd_layer2_gauge_analysis import (
    CURRENT_CODE,
    LINE_UNION_CODE,
    code_name,
    code_to_dict,
    layer2_support_count,
    make_gate_rule,
    rule_matches_code,
    support_polynomial_string,
    xor_code,
)
from torus_nd_validate import validate_rule

try:
    from rich.console import Console
    from rich.progress import track
except ImportError:  # pragma: no cover - optional dependency
    Console = None
    track = None

Code = Tuple[int, int, int, int]


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _iter_progress(
    values: Iterable[Code],
    *,
    description: str,
    use_rich: bool,
):
    if use_rich and track is not None:
        return track(values, description=description)
    return values


def affine_family_codes() -> List[Code]:
    return [xor_code(CURRENT_CODE, gauge) for gauge in range(4)]


def all_codes() -> List[Code]:
    return [tuple((raw >> (2 * idx)) & 3 for idx in range(4)) for raw in range(256)]


def _selection_key(code: Code, m_values: Sequence[int]) -> Tuple[int, ...]:
    return tuple(layer2_support_count(code, m) for m in m_values)


def derive_line_union(
    m_values: Sequence[int],
    *,
    family: str,
    use_rich: bool,
) -> Dict[str, object]:
    start = time.perf_counter()
    candidate_codes = affine_family_codes() if family == "affine" else all_codes()
    survivors: List[Code] = []
    per_code: List[Dict[str, object]] = []

    for code in _iter_progress(candidate_codes, description="Searching reduced family", use_rich=use_rich):
        first_fail_m = None
        checked_prefix = []
        for m in m_values:
            report = validate_rule(4, m, make_gate_rule(code, m))
            item = {
                "m": m,
                "all_hamilton": bool(report["all_hamilton"]),
                "sign_product": int(report["sign_product"]),
                "color_cycle_counts": [int(stat["cycle_count"]) for stat in report["color_stats"]],
                "layer2_support_count": layer2_support_count(code, m),
            }
            checked_prefix.append(item)
            if not bool(report["all_hamilton"]):
                first_fail_m = m
                break
        if first_fail_m is None:
            survivors.append(code)
        per_code.append(
            {
                "code": list(code),
                "code_name": code_name(code),
                "truth_table": code_to_dict(code),
                "first_fail_m": first_fail_m,
                "is_hamilton_on_range": first_fail_m is None,
                "layer2_support_formula": support_polynomial_string(code),
                "checked_prefix": checked_prefix,
            }
        )

    survivors_sorted = sorted(survivors)
    affine_sorted = sorted(affine_family_codes())
    selected = min(survivors_sorted, key=lambda code: _selection_key(code, m_values))
    elapsed_sec = time.perf_counter() - start

    return {
        "task_id": "D4-LINE-UNION-SEARCH-01",
        "tested_m_values": list(m_values),
        "searched_family": family,
        "family_size": len(candidate_codes),
        "runtime_sec": elapsed_sec,
        "survivor_count": len(survivors_sorted),
        "survivor_codes": [list(code) for code in survivors_sorted],
        "survivor_names": [code_name(code) for code in survivors_sorted],
        "survivor_truth_tables": [code_to_dict(code) for code in survivors_sorted],
        "affine_family_codes": [list(code) for code in affine_sorted],
        "survivors_equal_affine_family": survivors_sorted == affine_sorted,
        "selected_code": list(selected),
        "selected_name": code_name(selected),
        "selected_truth_table": code_to_dict(selected),
        "selected_support_formula": support_polynomial_string(selected),
        "selected_support_counts": {str(m): layer2_support_count(selected, m) for m in m_values},
        "selected_matches_line_union_module": (
            selected == LINE_UNION_CODE
            and all(rule_matches_code(line_union_direction_tuple, selected, m) for m in (3, 4, 5, 6))
        ),
        "module_reference_checks": {
            "line_union_module_matches_line_union_code": all(
                rule_matches_code(line_union_direction_tuple, LINE_UNION_CODE, m) for m in (3, 4, 5, 6)
            ),
        },
        "per_code": per_code,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Search the reduced layer-2 family and derive the line-union witness."
    )
    parser.add_argument(
        "--m-list",
        default="3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20",
        help="comma-separated list of m values used to filter Hamiltonian survivors",
    )
    parser.add_argument(
        "--family",
        choices=("full", "affine"),
        default="full",
        help="search all 256 reduced rules or only the 4 affine-family rules",
    )
    parser.add_argument("--out", type=Path, help="write JSON summary to this path")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich progress output")
    args = parser.parse_args(argv)

    use_rich = not args.no_rich and Console is not None and track is not None
    console = Console() if use_rich else None
    m_values = _parse_m_list(args.m_list)
    summary = derive_line_union(m_values, family=args.family, use_rich=use_rich)

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2))

    lines = [
        f"tested m values: {summary['tested_m_values']}",
        f"searched family: {summary['searched_family']} ({summary['family_size']} codes)",
        f"survivor count: {summary['survivor_count']}",
        f"survivor codes: {summary['survivor_codes']}",
        f"survivors equal affine family: {summary['survivors_equal_affine_family']}",
        f"selected code: {summary['selected_code']} ({summary['selected_name']})",
        f"selected support formula: {summary['selected_support_formula']}",
        f"selected matches line-union module: {summary['selected_matches_line_union_module']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
    ]
    if console is not None:
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
