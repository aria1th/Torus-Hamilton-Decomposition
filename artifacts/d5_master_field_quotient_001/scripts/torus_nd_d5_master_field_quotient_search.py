#!/usr/bin/env python3
"""Search cyclic-equivariant permutation-valued quotient fields for d=5."""

from __future__ import annotations

import argparse
import json
import platform
import time
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, List, Sequence

from ortools.sat.python import cp_model

from torus_nd_d5_master_field_quotient_family import (
    PILOT_M_VALUES,
    STABILITY_M_VALUES,
    DIM,
    SCHEMA_BY_NAME,
    TASK_ID,
    State,
    anchor_defect_summary,
    analyze_latin,
    color_cycle_summary,
    first_return_qwu_for_color0,
    permutation_table_payload,
    predecessor_patterns,
    required_color0_output,
    rotate_state,
    schema_state_space,
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


def _solve_schema(
    schema_name: str,
    pilot_m_values: Sequence[int],
    stability_m_values: Sequence[int],
    *,
    max_time_sec: float,
    workers: int,
    random_seed: int,
) -> Dict[str, object]:
    schema = SCHEMA_BY_NAME[schema_name]
    start = time.perf_counter()
    state_space_key = tuple(sorted(set(pilot_m_values) | set(stability_m_values)))
    states = schema_state_space(schema_name, state_space_key)
    state_to_id = {state: idx for idx, state in enumerate(states)}
    model = cp_model.CpModel()

    assign = {}
    for state_id in range(len(states)):
        for color in range(DIM):
            for direction in range(DIM):
                assign[(state_id, color, direction)] = model.NewBoolVar(f"s{state_id}_c{color}_d{direction}")

    for state_id in range(len(states)):
        for color in range(DIM):
            model.Add(sum(assign[(state_id, color, direction)] for direction in range(DIM)) == 1)
        for direction in range(DIM):
            model.Add(sum(assign[(state_id, color, direction)] for color in range(DIM)) == 1)

    for state_id, state in enumerate(states):
        rotated_id = state_to_id[rotate_state(state, 1)]
        for color in range(DIM):
            for direction in range(DIM):
                model.Add(assign[(rotated_id, (color + 1) % DIM, (direction + 1) % DIM)] == assign[(state_id, color, direction)])

    for state_id, state in enumerate(states):
        model.Add(assign[(state_id, 0, required_color0_output(state, schema))] == 1)

    pattern_counts = {}
    for m in pilot_m_values:
        patterns = predecessor_patterns(schema_name, m, state_space_key)
        pattern_counts[str(m)] = len(patterns)
        for pattern in patterns:
            for color in range(DIM):
                model.Add(sum(assign[(pattern[direction], color, direction)] for direction in range(DIM)) == 1)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time_sec
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    solver.parameters.cp_model_presolve = True
    solver.parameters.log_search_progress = False
    status = solver.Solve(model)

    status_name = solver.StatusName(status)
    payload = {
        "schema": schema_name,
        "schema_description": schema.description,
        "state_count": len(states),
        "pilot_m_values": list(pilot_m_values),
        "stability_m_values": list(stability_m_values),
        "pattern_counts": pattern_counts,
        "solver_status": status_name,
        "runtime_sec": time.perf_counter() - start,
        "objective_value": solver.ObjectiveValue() if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
        "anchor_baseline": {str(m): anchor_defect_summary(schema, m, state_space_key) for m in pilot_m_values},
    }

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return payload

    table = {}
    for state_id in range(len(states)):
        perm = []
        for color in range(DIM):
            direction = next(direction for direction in range(DIM) if solver.Value(assign[(state_id, color, direction)]))
            perm.append(direction)
        table[state_id] = tuple(perm)

    payload["permutation_table"] = permutation_table_payload(schema, states, table)
    payload["pilot_validation"] = {
        str(m): {
            "latin": analyze_latin(table, schema, m, state_space_key),
            "color_cycles": color_cycle_summary(table, schema, m, state_space_key),
            "color0_return": first_return_qwu_for_color0(table, schema, m, state_space_key),
        }
        for m in pilot_m_values
    }
    payload["stability_validation"] = {
        str(m): {
            "latin": analyze_latin(table, schema, m, state_space_key),
            "color_cycles": color_cycle_summary(table, schema, m, state_space_key),
            "color0_return": first_return_qwu_for_color0(table, schema, m, state_space_key),
        }
        for m in stability_m_values
    }
    return payload


def run_search(
    *,
    schema_names: Sequence[str],
    pilot_m_values: Sequence[int],
    stability_m_values: Sequence[int],
    max_time_sec: float,
    workers: int,
    random_seed: int,
) -> Dict[str, object]:
    start = time.perf_counter()
    schema_results = []
    for schema_name in schema_names:
        schema_results.append(
            _solve_schema(
                schema_name,
                pilot_m_values,
                stability_m_values,
                max_time_sec=max_time_sec,
                workers=workers,
                random_seed=random_seed,
            )
        )
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "search_parameters": {
            "schemas": list(schema_names),
            "pilot_m_values": list(pilot_m_values),
            "stability_m_values": list(stability_m_values),
            "max_time_sec": max_time_sec,
            "workers": workers,
            "random_seed": random_seed,
        },
        "environment": {
            "python_version": platform.python_version(),
            "rich_version": _rich_version(),
            "ortools_version": version("ortools"),
        },
        "schema_results": schema_results,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [f"task_id: {summary['task_id']}", f"runtime_sec: {summary['runtime_sec']:.3f}"]
    for item in summary["schema_results"]:
        line = (
            f"{item['schema']}: status={item['solver_status']} "
            f"states={item['state_count']} patterns={item['pattern_counts']} runtime={item['runtime_sec']:.3f}"
        )
        if item.get("pilot_validation"):
            best = item["pilot_validation"][str(summary["search_parameters"]["pilot_m_values"][0])]
            line += (
                f" | latin={best['latin']['incoming_latin']} "
                f"color0_U={best['color0_return']['U_cycle_lengths']} "
                f"mono={best['color0_return']['monodromies']}"
            )
        lines.append(line)
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search d=5 master-field quotient schemas.")
    parser.add_argument(
        "--schemas",
        default="stable_anchor_two_atom,unit_anchor_three_atom",
        help="comma-separated schema names",
    )
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--stability-m-list", default="11,13", help="comma-separated stability moduli")
    parser.add_argument("--max-time-sec", type=float, default=120.0, help="per-schema solver time limit")
    parser.add_argument("--workers", type=int, default=8, help="CP-SAT worker count")
    parser.add_argument("--random-seed", type=int, default=20260310, help="CP-SAT random seed")
    parser.add_argument("--out", type=Path, help="write JSON summary to this path")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    schema_names = [part.strip() for part in args.schemas.split(",") if part.strip()]
    summary = run_search(
        schema_names=schema_names,
        pilot_m_values=_parse_m_list(args.pilot_m_list),
        stability_m_values=_parse_m_list(args.stability_m_list),
        max_time_sec=args.max_time_sec,
        workers=args.workers,
        random_seed=args.random_seed,
    )

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2))

    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
