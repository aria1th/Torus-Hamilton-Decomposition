#!/usr/bin/env python3
"""Search for nonlifted witnesses on the passive tail_cut refined quotient."""

from __future__ import annotations

import argparse
import json
import platform
import time
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, List, Sequence

from ortools.sat.python import cp_model

from torus_nd_d5_tail_cut_lookup_rerun import (
    SCHEMA_PHASE_ALIGN_TAIL_CUT,
    _build_model,
    _extend_anchor_values_to_full_union,
    _field_payload,
    _load_base_anchor_map,
    _parse_m_list,
    _projection_anchor_values,
    _rich_version,
)
from torus_nd_d5_master_field_quotient_family import DIM, preferred_anchor_value, schema_state_space

TASK_ID = "D5-ACTIVE-TAIL-GRAMMAR-002"

try:
    from rich.console import Console
except ImportError:  # pragma: no cover - optional dependency
    Console = None


def _extract_anchor_values(anchor_vars, solver: cp_model.CpSolver, *, state_count: int) -> Dict[int, int]:
    return {
        state_id: next(value for value in range(DIM) if solver.Value(anchor_vars[(state_id, value)]))
        for state_id in range(state_count)
    }


def _diff_expr(anchor_vars, lifted_anchor_values: Dict[int, int], *, state_count: int):
    same_terms = [anchor_vars[(state_id, lifted_anchor_values[state_id])] for state_id in range(state_count)]
    return state_count - sum(same_terms)


def _solve_variant(
    *,
    base_field_json: Path,
    pilot_m_values: Sequence[int],
    stability_m_values: Sequence[int],
    max_time_sec: float,
    workers: int,
    random_seed: int,
    mode: str,
) -> Dict[str, object]:
    schema_name = SCHEMA_PHASE_ALIGN_TAIL_CUT.name
    base_anchor_map = _load_base_anchor_map(base_field_json)
    model, states, pilot_state_space_key, anchor_vars, preference_expr, pattern_counts = _build_model(schema_name, pilot_m_values)
    lifted_anchor_values = _projection_anchor_values(states, base_anchor_map)
    for state_id, value in lifted_anchor_values.items():
        model.AddHint(anchor_vars[(state_id, value)], 1)

    full_state_space_key = tuple(sorted(set(pilot_m_values) | set(stability_m_values)))
    full_states = schema_state_space(schema_name, full_state_space_key)
    diff_expr = _diff_expr(anchor_vars, lifted_anchor_values, state_count=len(states))
    lifted_score = sum(
        1
        for state_id, state in enumerate(states)
        if preferred_anchor_value(state) is not None and lifted_anchor_values[state_id] == preferred_anchor_value(state)
    )

    if mode == "same_preference":
        model.Add(preference_expr == lifted_score)
        model.Add(diff_expr >= 1)
        model.Maximize(diff_expr)
    elif mode == "best_divergent":
        model.Add(diff_expr >= 1)
        model.Maximize(preference_expr * (len(states) + 1) + diff_expr)
    else:
        raise ValueError(mode)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time_sec
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    status = solver.Solve(model)

    payload = {
        "mode": mode,
        "solver_status": solver.StatusName(status),
        "lifted_preference_score": lifted_score,
        "state_count": len(states),
        "pattern_counts": pattern_counts,
    }
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return payload

    anchor_values = _extract_anchor_values(anchor_vars, solver, state_count=len(states))
    changed_state_count = sum(1 for state_id in range(len(states)) if anchor_values[state_id] != lifted_anchor_values[state_id])
    preference_score = sum(
        1
        for state_id, state in enumerate(states)
        if preferred_anchor_value(state) is not None and anchor_values[state_id] == preferred_anchor_value(state)
    )
    full_anchor_values = _extend_anchor_values_to_full_union(states, anchor_values, full_states, base_anchor_map)
    payload["field"] = _field_payload(
        mode,
        anchor_values,
        states,
        schema_name,
        pilot_m_values,
        pilot_state_space_key,
        full_states,
        full_anchor_values,
        full_state_space_key,
        stability_m_values,
        preference_score,
        changed_state_count=changed_state_count,
    )
    payload["objective_value"] = int(solver.ObjectiveValue())
    payload["changed_state_count"] = changed_state_count
    return payload


def run_search(
    *,
    base_field_json: Path,
    pilot_m_values: Sequence[int],
    stability_m_values: Sequence[int],
    max_time_sec: float,
    workers: int,
    random_seed: int,
) -> Dict[str, object]:
    start = time.perf_counter()
    same_pref = _solve_variant(
        base_field_json=base_field_json,
        pilot_m_values=pilot_m_values,
        stability_m_values=stability_m_values,
        max_time_sec=max_time_sec,
        workers=workers,
        random_seed=random_seed,
        mode="same_preference",
    )
    best_div = _solve_variant(
        base_field_json=base_field_json,
        pilot_m_values=pilot_m_values,
        stability_m_values=stability_m_values,
        max_time_sec=max_time_sec,
        workers=workers,
        random_seed=random_seed + 1,
        mode="best_divergent",
    )
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": {
            "python_version": platform.python_version(),
            "rich_version": _rich_version(),
            "ortools_version": version("ortools"),
        },
        "search_parameters": {
            "base_field_json": str(base_field_json),
            "pilot_m_values": list(pilot_m_values),
            "stability_m_values": list(stability_m_values),
            "max_time_sec_per_variant": max_time_sec,
            "workers": workers,
            "random_seed": random_seed,
        },
        "same_preference_divergence": same_pref,
        "best_divergent_field": best_div,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [f"task_id: {summary['task_id']}", f"runtime_sec: {summary['runtime_sec']:.3f}"]
    for key in ("same_preference_divergence", "best_divergent_field"):
        item = summary[key]
        line = f"{item['mode']}: status={item['solver_status']}"
        if "field" in item:
            first = item["field"]["pilot_validation"]["5"]["color0_return"]
            line += (
                f" changed={item['changed_state_count']} pref={item['field']['preference_score']} "
                f"strict={first['strict_clock']} U={first['U_cycle_lengths']} mono={first['monodromies']}"
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
    parser = argparse.ArgumentParser(description="Search for nonlifted witnesses on the passive tail_cut quotient.")
    parser.add_argument(
        "--base-field-json",
        type=Path,
        default=Path("artifacts/d5_theta_ab_phase_align_001/data/best_strict_collapse_field.json"),
        help="strict-collapse representative to compare against",
    )
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--stability-m-list", default="11,13", help="comma-separated post hoc stability moduli")
    parser.add_argument("--max-time-sec", type=float, default=60.0, help="per-variant CP-SAT time budget")
    parser.add_argument("--workers", type=int, default=8, help="CP-SAT worker count")
    parser.add_argument("--random-seed", type=int, default=20260310, help="fixed CP-SAT random seed")
    parser.add_argument("--out", type=Path, required=True, help="write JSON summary here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    summary = run_search(
        base_field_json=args.base_field_json,
        pilot_m_values=_parse_m_list(args.pilot_m_list),
        stability_m_values=_parse_m_list(args.stability_m_list),
        max_time_sec=args.max_time_sec,
        workers=args.workers,
        random_seed=args.random_seed,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
