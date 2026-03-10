#!/usr/bin/env python3
"""Free-anchor search for d=5 cyclic-equivariant master fields on quotient schemas."""

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
    DIM,
    SCHEMA_BY_NAME,
    TASK_ID,
    State,
    anchor_table_payload,
    anchor_values_to_permutation_table,
    analyze_latin,
    color_cycle_summary,
    first_return_qwu_for_color0,
    preferred_anchor_value,
    predecessor_patterns,
    rotate_state,
    schema_state_space,
    state_to_id_map,
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


class _SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, states, schema, anchor_vars, solution_limit, pilot_m_values, stability_m_values, state_space_key):
        super().__init__()
        self.states = states
        self.schema = schema
        self.anchor_vars = anchor_vars
        self.solution_limit = solution_limit
        self.pilot_m_values = pilot_m_values
        self.stability_m_values = stability_m_values
        self.state_space_key = state_space_key
        self.solutions: List[Dict[str, object]] = []
        self.solution_limit_reached = False

    def on_solution_callback(self) -> None:
        anchor_values = {state_id: next(value for value in range(DIM) if self.Value(self.anchor_vars[(state_id, value)])) for state_id in range(len(self.states))}
        perm_table = anchor_values_to_permutation_table(self.states, anchor_values)
        pilot_validation = {
            str(m): {
                "latin": analyze_latin(perm_table, self.schema, m, self.state_space_key),
                "color0_return": first_return_qwu_for_color0(perm_table, self.schema, m, self.state_space_key),
            }
            for m in self.pilot_m_values
        }
        stability_validation = {
            str(m): {
                "latin": analyze_latin(perm_table, self.schema, m, self.state_space_key),
                "color0_return": first_return_qwu_for_color0(perm_table, self.schema, m, self.state_space_key),
            }
            for m in self.stability_m_values
        }
        self.solutions.append(
            {
                "anchor_table": anchor_table_payload(self.schema, self.states, anchor_values),
                "pilot_validation": pilot_validation,
                "stability_validation": stability_validation,
            }
        )
        if len(self.solutions) >= self.solution_limit:
            self.solution_limit_reached = True
            self.StopSearch()


def _enumerate_fields(
    schema_name: str,
    pilot_m_values: Sequence[int],
    stability_m_values: Sequence[int],
    *,
    target_score: int | None,
    max_time_sec: float,
    random_seed: int,
    solution_limit: int,
) -> tuple[list[dict[str, object]], bool]:
    enum_model, schema, enum_states, enum_state_space_key, enum_anchor_vars, enum_preference_expr, _ = _build_anchor_model(
        schema_name, pilot_m_values, stability_m_values
    )
    if target_score is not None:
        enum_model.Add(enum_preference_expr == target_score)
    collector = _SolutionCollector(
        enum_states,
        schema,
        enum_anchor_vars,
        solution_limit,
        pilot_m_values,
        stability_m_values,
        enum_state_space_key,
    )
    enum_solver = cp_model.CpSolver()
    enum_solver.parameters.max_time_in_seconds = max_time_sec
    enum_solver.parameters.num_search_workers = 1
    enum_solver.parameters.random_seed = random_seed
    enum_solver.SearchForAllSolutions(enum_model, collector)
    return collector.solutions, collector.solution_limit_reached


def _build_anchor_model(schema_name: str, pilot_m_values: Sequence[int], stability_m_values: Sequence[int]):
    schema = SCHEMA_BY_NAME[schema_name]
    state_space_key = tuple(sorted(set(pilot_m_values) | set(stability_m_values)))
    states = schema_state_space(schema_name, state_space_key)
    state_map = state_to_id_map(states)
    rotated_ids = {
        (state_id, shift): state_map[rotate_state(state, shift)]
        for state_id, state in enumerate(states)
        for shift in range(DIM)
    }

    model = cp_model.CpModel()
    anchor_vars = {}
    for state_id in range(len(states)):
        for value in range(DIM):
            anchor_vars[(state_id, value)] = model.NewBoolVar(f"a_s{state_id}_v{value}")
        model.Add(sum(anchor_vars[(state_id, value)] for value in range(DIM)) == 1)

    for state_id in range(len(states)):
        for direction in range(DIM):
            model.Add(
                sum(
                    anchor_vars[(rotated_ids[(state_id, (-color) % DIM)], (direction - color) % DIM)]
                    for color in range(DIM)
                )
                == 1
            )

    pattern_counts = {}
    for m in pilot_m_values:
        patterns = predecessor_patterns(schema_name, m, state_space_key)
        pattern_counts[str(m)] = len(patterns)
        for pattern in patterns:
            for color in range(DIM):
                model.Add(sum(anchor_vars[(rotated_ids[(pattern[direction], (-color) % DIM)], (direction - color) % DIM)] for direction in range(DIM)) == 1)

    preference_terms = []
    for state_id, state in enumerate(states):
        preferred = preferred_anchor_value(state)
        if preferred is not None:
            preference_terms.append(anchor_vars[(state_id, preferred)])
    preference_expr = sum(preference_terms)
    return model, schema, states, state_space_key, anchor_vars, preference_expr, pattern_counts


def _solve_schema(
    schema_name: str,
    pilot_m_values: Sequence[int],
    stability_m_values: Sequence[int],
    *,
    max_time_sec: float,
    workers: int,
    random_seed: int,
    solution_limit: int,
) -> Dict[str, object]:
    start = time.perf_counter()
    model, schema, states, state_space_key, anchor_vars, preference_expr, pattern_counts = _build_anchor_model(
        schema_name, pilot_m_values, stability_m_values
    )
    model.Maximize(preference_expr)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time_sec
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
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
        "optimal_preference_score": int(solver.ObjectiveValue()) if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
    }

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return payload

    target_score = int(solver.ObjectiveValue())
    optimal_fields, optimal_limit_reached = _enumerate_fields(
        schema_name,
        pilot_m_values,
        stability_m_values,
        target_score=target_score,
        max_time_sec=max_time_sec,
        random_seed=random_seed,
        solution_limit=solution_limit,
    )
    sample_fields, sample_limit_reached = _enumerate_fields(
        schema_name,
        pilot_m_values,
        stability_m_values,
        target_score=None,
        max_time_sec=max_time_sec,
        random_seed=random_seed + 1,
        solution_limit=solution_limit,
    )

    combined = []
    seen = set()
    for field in optimal_fields + sample_fields:
        key = json.dumps(field["anchor_table"], sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        combined.append(field)

    payload["optimal_field_count"] = len(optimal_fields)
    payload["optimal_solution_limit_reached"] = optimal_limit_reached
    payload["sample_field_count"] = len(sample_fields)
    payload["sample_solution_limit_reached"] = sample_limit_reached
    payload["feasible_field_count"] = len(combined)
    payload["feasible_fields"] = combined
    return payload


def run_search(
    *,
    schema_names: Sequence[str],
    pilot_m_values: Sequence[int],
    stability_m_values: Sequence[int],
    max_time_sec: float,
    workers: int,
    random_seed: int,
    solution_limit: int,
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
                solution_limit=solution_limit,
            )
        )
    return {
        "task_id": TASK_ID.replace("QUOTIENT", "FREE-ANCHOR"),
        "runtime_sec": time.perf_counter() - start,
        "search_parameters": {
            "schemas": list(schema_names),
            "pilot_m_values": list(pilot_m_values),
            "stability_m_values": list(stability_m_values),
            "max_time_sec": max_time_sec,
            "workers": workers,
            "random_seed": random_seed,
            "solution_limit": solution_limit,
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
            f"{item['schema']}: status={item['solver_status']} states={item['state_count']} "
            f"patterns={item['pattern_counts']} pref={item['optimal_preference_score']} runtime={item['runtime_sec']:.3f}"
        )
        if item.get("feasible_fields"):
            first = item["feasible_fields"][0]["pilot_validation"][str(summary["search_parameters"]["pilot_m_values"][0])]
            line += (
                f" | feasible={item['feasible_field_count']} "
                f"latin={first['latin']['incoming_latin']} U={first['color0_return']['U_cycle_lengths']} "
                f"mono={first['color0_return']['monodromies']}"
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
    parser = argparse.ArgumentParser(description="Search free-anchor d=5 master fields on quotient schemas.")
    parser.add_argument("--schemas", default="stable_anchor_two_atom,unit_anchor_three_atom", help="comma-separated schema names")
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--stability-m-list", default="11,13", help="comma-separated stability moduli")
    parser.add_argument("--max-time-sec", type=float, default=120.0, help="per-schema time budget")
    parser.add_argument("--workers", type=int, default=8, help="CP-SAT worker count")
    parser.add_argument("--random-seed", type=int, default=20260310, help="fixed CP-SAT random seed")
    parser.add_argument("--solution-limit", type=int, default=20, help="max optimal solutions to enumerate per schema")
    parser.add_argument("--out", type=Path, help="write JSON summary to this path")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    summary = run_search(
        schema_names=[part.strip() for part in args.schemas.split(",") if part.strip()],
        pilot_m_values=_parse_m_list(args.pilot_m_list),
        stability_m_values=_parse_m_list(args.stability_m_list),
        max_time_sec=args.max_time_sec,
        workers=args.workers,
        random_seed=args.random_seed,
        solution_limit=args.solution_limit,
    )

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2))

    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
