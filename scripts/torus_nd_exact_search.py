#!/usr/bin/env python3
"""Exact CP-SAT search for Hamilton decompositions of the directed d-torus."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from ortools.sat.python import cp_model

from torus_nd_validate import (
    build_nexts_from_direction_tuples,
    cycle_decomposition,
    index_to_coords,
    neighbor_index,
    predecessor_index,
    strides,
    validate_direction_tuples,
)

DirectionTuple = Tuple[int, ...]


def _extract_direction_tuples(
    solver: cp_model.CpSolver,
    variables: Dict[Tuple[int, int, int], cp_model.IntVar],
    vertex_count: int,
    dim: int,
) -> List[DirectionTuple]:
    out: List[DirectionTuple] = []
    for vertex in range(vertex_count):
        dirs = [0] * dim
        for color in range(dim):
            chosen = None
            for direction in range(dim):
                if solver.Value(variables[(vertex, color, direction)]):
                    chosen = direction
                    break
            if chosen is None:
                raise RuntimeError(f"Solver produced no direction for vertex={vertex}, color={color}")
            dirs[color] = chosen
        out.append(tuple(dirs))
    return out


def _build_model(dim: int, m: int) -> Tuple[cp_model.CpModel, Dict[Tuple[int, int, int], cp_model.IntVar]]:
    vertex_count = m ** dim
    axis_strides = strides(dim, m)
    model = cp_model.CpModel()
    variables: Dict[Tuple[int, int, int], cp_model.IntVar] = {}

    for vertex in range(vertex_count):
        for color in range(dim):
            vars_for_color = []
            for direction in range(dim):
                var = model.NewBoolVar(f"x_v{vertex}_c{color}_d{direction}")
                variables[(vertex, color, direction)] = var
                vars_for_color.append(var)
            model.Add(sum(vars_for_color) == 1)

        for direction in range(dim):
            model.Add(sum(variables[(vertex, color, direction)] for color in range(dim)) == 1)

    for head in range(vertex_count):
        head_coords = index_to_coords(head, dim, m)
        for color in range(dim):
            incoming = [
                variables[(predecessor_index(head, head_coords, direction, m, axis_strides), color, direction)]
                for direction in range(dim)
            ]
            model.Add(sum(incoming) == 1)

    # Symmetry break: pin the origin to the canonical tuple.
    origin = 0
    for color in range(dim):
        model.Add(variables[(origin, color, color)] == 1)

    return model, variables


def _add_subtour_cuts(
    model: cp_model.CpModel,
    variables: Dict[Tuple[int, int, int], cp_model.IntVar],
    direction_tuples: Sequence[DirectionTuple],
    dim: int,
    m: int,
) -> Tuple[int, List[int]]:
    nexts = build_nexts_from_direction_tuples(dim, m, direction_tuples)
    axis_strides = strides(dim, m)
    vertex_count = m ** dim
    cut_count = 0
    cycle_counts: List[int] = []

    for color, perm in enumerate(nexts):
        cycles = cycle_decomposition(perm)
        cycle_counts.append(len(cycles))
        for cycle in cycles:
            if len(cycle) == vertex_count:
                continue
            cycle_set = set(cycle)
            leave_terms = []
            for vertex in cycle:
                coords = index_to_coords(vertex, dim, m)
                for direction in range(dim):
                    if neighbor_index(vertex, coords, direction, m, axis_strides) not in cycle_set:
                        leave_terms.append(variables[(vertex, color, direction)])
            if not leave_terms:
                continue
            model.Add(sum(leave_terms) >= 1)
            cut_count += 1

    return cut_count, cycle_counts


def exact_search(dim: int, m: int, time_limit_sec: float, workers: int) -> Dict[str, object]:
    start = time.perf_counter()
    model, variables = _build_model(dim, m)
    vertex_count = m ** dim
    total_cut_count = 0
    iteration_count = 0
    last_report: Dict[str, object] | None = None
    last_cycle_counts: List[int] | None = None
    last_direction_tuples: List[DirectionTuple] | None = None
    solver_status_name = "UNKNOWN"

    while True:
        elapsed = time.perf_counter() - start
        remaining = max(0.0, time_limit_sec - elapsed)
        if remaining <= 0:
            break

        iteration_count += 1
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = remaining
        solver.parameters.num_search_workers = workers
        status = solver.Solve(model)
        solver_status_name = solver.StatusName(status)

        if status == cp_model.INFEASIBLE:
            return {
                "dim": dim,
                "m": m,
                "status": "unsat_exact",
                "solver_status": solver_status_name,
                "runtime_sec": time.perf_counter() - start,
                "time_limit_sec": time_limit_sec,
                "iteration_count": iteration_count,
                "cut_count": total_cut_count,
                "vertex_count": vertex_count,
            }

        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            break

        direction_tuples = _extract_direction_tuples(solver, variables, vertex_count, dim)
        last_direction_tuples = direction_tuples
        validation = validate_direction_tuples(dim, m, direction_tuples)
        validation.pop("nexts", None)
        last_report = validation
        last_cycle_counts = [stat["cycle_count"] for stat in validation["color_stats"]]

        if validation["all_hamilton"]:
            return {
                "dim": dim,
                "m": m,
                "status": "hamilton_witness",
                "solver_status": solver_status_name,
                "runtime_sec": time.perf_counter() - start,
                "time_limit_sec": time_limit_sec,
                "iteration_count": iteration_count,
                "cut_count": total_cut_count,
                "vertex_count": vertex_count,
                "sign_product": validation["sign_product"],
                "color_stats": validation["color_stats"],
                "witness_direction_tuples": [list(dirs) for dirs in direction_tuples],
                "symmetry_break": "origin fixed to canonical tuple",
            }

        new_cuts, cycle_counts = _add_subtour_cuts(model, variables, direction_tuples, dim, m)
        total_cut_count += new_cuts
        last_cycle_counts = cycle_counts
        if new_cuts == 0:
            break

    payload: Dict[str, object] = {
        "dim": dim,
        "m": m,
        "status": "timeout",
        "solver_status": solver_status_name,
        "runtime_sec": time.perf_counter() - start,
        "time_limit_sec": time_limit_sec,
        "iteration_count": iteration_count,
        "cut_count": total_cut_count,
        "vertex_count": vertex_count,
    }
    if last_report is not None:
        payload["sign_product"] = last_report["sign_product"]
        payload["color_stats"] = last_report["color_stats"]
    if last_cycle_counts is not None:
        payload["last_cycle_counts"] = last_cycle_counts
    if last_direction_tuples is not None:
        payload["incumbent_direction_tuples"] = [list(dirs) for dirs in last_direction_tuples]
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Exact CP-SAT search on the directed d-torus.")
    parser.add_argument("--dim", type=int, default=4, help="torus dimension d")
    parser.add_argument("--m", type=int, required=True, help="cycle length m")
    parser.add_argument("--time-limit-sec", type=float, default=600.0, help="global wall-clock limit")
    parser.add_argument("--workers", type=int, default=8, help="CP-SAT worker count")
    parser.add_argument("--out", type=Path, help="write JSON result to this path")
    args = parser.parse_args()

    if args.dim < 1 or args.m < 2:
        raise SystemExit("Need dim >= 1 and m >= 2.")

    payload = exact_search(args.dim, args.m, args.time_limit_sec, args.workers)

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
