#!/usr/bin/env python3
"""Search a normalized hyperplane-fusion low-layer family for the directed 4-torus.

Family:

- dimension fixed at `d = 4`;
- outside low layers `S in {0, 1, 2}`, keep the affine-split baseline;
- inside low layers, the local direction tuple depends only on the pattern
  `(S, x0=0, x1=0, x2=0, x3=0, q=0)` with `q = x0 + x2 mod m`;
- one shared permutation table is searched across all requested `m`.

This is the finite compatibility formulation requested in
`RoundX/codex_job_request.md`.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from ortools.sat.python import cp_model

from torus_nd_validate import (
    coord_hyperplane_indices,
    cycle_decomposition,
    induced_first_return_maps,
    induced_p0_maps,
    index_to_coords,
    neighbor_index,
    predecessor_index,
    strides,
    validate_direction_tuples,
)

DIM = 4
LOW_LAYERS = (0, 1, 2)

Coords = Tuple[int, ...]
DirectionTuple = Tuple[int, ...]
PatternKey = Tuple[int, int, int, int, int, int]


@dataclass(frozen=True)
class InstanceCache:
    m: int
    vertex_count: int
    axis_strides: Tuple[int, ...]
    coords: Tuple[Coords, ...]
    row_of_vertex: Tuple[int, ...]
    baseline_tuples: Tuple[DirectionTuple, ...]


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _affine_split_direction_tuple(m: int, coords: Coords) -> DirectionTuple:
    layer = sum(coords) % m
    if layer != 0:
        return (0, 1, 2, 3)
    if (coords[0] + coords[2]) % m == 0:
        return (3, 2, 1, 0)
    return (1, 0, 3, 2)


def _pattern_key(m: int, coords: Coords) -> PatternKey | None:
    layer = sum(coords) % m
    if layer not in LOW_LAYERS:
        return None
    return (
        layer,
        int(coords[0] == 0),
        int(coords[1] == 0),
        int(coords[2] == 0),
        int(coords[3] == 0),
        int((coords[0] + coords[2]) % m == 0),
    )


def _pattern_key_to_dict(key: PatternKey) -> Dict[str, int]:
    return {
        "layer": key[0],
        "x0_eq_0": key[1],
        "x1_eq_0": key[2],
        "x2_eq_0": key[3],
        "x3_eq_0": key[4],
        "q_eq_0": key[5],
    }


def _build_row_catalog(m_values: Sequence[int]) -> List[PatternKey]:
    rows = set()
    for m in m_values:
        for index in range(m ** DIM):
            coords = index_to_coords(index, DIM, m)
            key = _pattern_key(m, coords)
            if key is not None:
                rows.add(key)
    return sorted(rows)


def _build_instance_cache(m: int, row_index_by_key: Dict[PatternKey, int]) -> InstanceCache:
    vertex_count = m ** DIM
    axis_strides = tuple(strides(DIM, m))
    coords: List[Coords] = []
    row_of_vertex: List[int] = []
    baseline_tuples: List[DirectionTuple] = []
    for index in range(vertex_count):
        coord = index_to_coords(index, DIM, m)
        coords.append(coord)
        key = _pattern_key(m, coord)
        row_of_vertex.append(-1 if key is None else row_index_by_key[key])
        baseline_tuples.append(_affine_split_direction_tuple(m, coord))
    return InstanceCache(
        m=m,
        vertex_count=vertex_count,
        axis_strides=axis_strides,
        coords=tuple(coords),
        row_of_vertex=tuple(row_of_vertex),
        baseline_tuples=tuple(baseline_tuples),
    )


def _affine_split_hint_perm(pattern: PatternKey) -> DirectionTuple:
    layer, _, _, _, _, q_zero = pattern
    if layer == 0:
        return (3, 2, 1, 0) if q_zero else (1, 0, 3, 2)
    return (0, 1, 2, 3)


def _matching_perm_indices(perms: Sequence[DirectionTuple]) -> Dict[Tuple[int, int], List[int]]:
    out: Dict[Tuple[int, int], List[int]] = {}
    for color in range(DIM):
        for direction in range(DIM):
            out[(color, direction)] = [
                perm_idx for perm_idx, perm in enumerate(perms) if perm[color] == direction
            ]
    return out


def _add_row_one_hot_constraints(
    model: cp_model.CpModel,
    row_keys: Sequence[PatternKey],
    perms: Sequence[DirectionTuple],
) -> Dict[Tuple[int, int], cp_model.IntVar]:
    perm_index_by_tuple = {perm: idx for idx, perm in enumerate(perms)}
    variables: Dict[Tuple[int, int], cp_model.IntVar] = {}
    for row_idx, key in enumerate(row_keys):
        vars_for_row = []
        hint_idx = perm_index_by_tuple[_affine_split_hint_perm(key)]
        for perm_idx in range(len(perms)):
            var = model.NewBoolVar(f"row_{row_idx}_perm_{perm_idx}")
            variables[(row_idx, perm_idx)] = var
            vars_for_row.append(var)
            model.AddHint(var, 1 if perm_idx == hint_idx else 0)
        model.Add(sum(vars_for_row) == 1)
    return variables


def _build_indegree_constraints(
    model: cp_model.CpModel,
    variables: Dict[Tuple[int, int], cp_model.IntVar],
    instances: Sequence[InstanceCache],
    perms: Sequence[DirectionTuple],
) -> None:
    matching = _matching_perm_indices(perms)
    for instance in instances:
        m = instance.m
        for head in range(instance.vertex_count):
            head_coords = instance.coords[head]
            for color in range(DIM):
                coeffs: Dict[Tuple[int, int], int] = defaultdict(int)
                const = 0
                for direction in range(DIM):
                    pred = predecessor_index(head, head_coords, direction, m, instance.axis_strides)
                    row_idx = instance.row_of_vertex[pred]
                    if row_idx < 0:
                        if instance.baseline_tuples[pred][color] == direction:
                            const += 1
                        continue
                    for perm_idx in matching[(color, direction)]:
                        coeffs[(row_idx, perm_idx)] += 1
                model.Add(
                    sum(coeff * variables[key] for key, coeff in coeffs.items()) + const == 1
                )


def _extract_assignment(
    solver: cp_model.CpSolver,
    variables: Dict[Tuple[int, int], cp_model.IntVar],
    row_count: int,
    perm_count: int,
) -> List[int]:
    out = [0] * row_count
    for row_idx in range(row_count):
        selected = None
        for perm_idx in range(perm_count):
            if solver.Value(variables[(row_idx, perm_idx)]):
                selected = perm_idx
                break
        if selected is None:
            raise RuntimeError(f"No permutation selected for row {row_idx}")
        out[row_idx] = selected
    return out


def _direction_tuples_for_instance(
    instance: InstanceCache,
    row_perm_indices: Sequence[int],
    perms: Sequence[DirectionTuple],
) -> List[DirectionTuple]:
    out: List[DirectionTuple] = []
    for vertex in range(instance.vertex_count):
        row_idx = instance.row_of_vertex[vertex]
        if row_idx < 0:
            out.append(instance.baseline_tuples[vertex])
        else:
            out.append(perms[row_perm_indices[row_idx]])
    return out


def _canonical_table_json(
    row_keys: Sequence[PatternKey],
    row_perm_indices: Sequence[int],
    perms: Sequence[DirectionTuple],
    m_values: Sequence[int],
) -> Dict[str, object]:
    return {
        "family": "d4_hyperplane_fusion_low_layer_table_v1",
        "dim": DIM,
        "low_layers": list(LOW_LAYERS),
        "m_values": list(m_values),
        "pattern_schema": ["layer", "x0_eq_0", "x1_eq_0", "x2_eq_0", "x3_eq_0", "q_eq_0"],
        "rows": [
            {
                "row_id": row_idx,
                "pattern": _pattern_key_to_dict(key),
                "direction_tuple": list(perms[row_perm_indices[row_idx]]),
            }
            for row_idx, key in enumerate(row_keys)
        ],
        "outside_low_layers_rule": "affine_split_baseline",
    }


def _evaluate_assignment(
    row_keys: Sequence[PatternKey],
    row_perm_indices: Sequence[int],
    perms: Sequence[DirectionTuple],
    instances: Sequence[InstanceCache],
) -> Dict[str, object]:
    reports: List[Dict[str, object]] = []
    score_total = 0
    score_max = 0
    all_hamilton = True

    for instance in instances:
        direction_tuples = _direction_tuples_for_instance(instance, row_perm_indices, perms)
        validation = validate_direction_tuples(DIM, instance.m, direction_tuples)
        nexts = validation.pop("nexts")
        p0_report = induced_p0_maps(nexts, DIM, instance.m)

        hyperplane_reports = []
        for axis in range(DIM):
            section = coord_hyperplane_indices(DIM, instance.m, axis, 0)
            section_report = induced_first_return_maps(nexts, DIM, instance.m, section)
            hyperplane_reports.append(
                {
                    "axis": axis,
                    "matched_color": axis,
                    "matched_color_report": section_report["color_maps"][axis],
                }
            )

        cycle_counts = [int(stat["cycle_count"]) for stat in validation["color_stats"]]
        score_total += sum(cycle_counts)
        score_max = max(score_max, max(cycle_counts))
        all_hamilton = all_hamilton and bool(validation["all_hamilton"])
        reports.append(
            {
                "m": instance.m,
                "vertex_count": instance.vertex_count,
                "all_hamilton": validation["all_hamilton"],
                "sign_product": validation["sign_product"],
                "color_stats": validation["color_stats"],
                "p0_report": p0_report,
                "matched_hyperplane_returns": hyperplane_reports,
                "_nexts": nexts,
            }
        )

    return {
        "row_table": _canonical_table_json(row_keys, row_perm_indices, perms, [instance.m for instance in instances]),
        "all_hamilton": all_hamilton,
        "score_total_cycles": score_total,
        "score_max_cycles": score_max,
        "instance_reports": reports,
    }


def _add_cycle_cuts(
    model: cp_model.CpModel,
    variables: Dict[Tuple[int, int], cp_model.IntVar],
    perms: Sequence[DirectionTuple],
    instances: Sequence[InstanceCache],
    evaluation: Dict[str, object],
    cut_signatures: set[Tuple[int, int, Tuple[int, ...]]],
) -> Tuple[int, Dict[str, object] | None]:
    matching = _matching_perm_indices(perms)
    instance_by_m = {instance.m: instance for instance in instances}
    added = 0

    for report in evaluation["instance_reports"]:
        m = int(report["m"])
        instance = instance_by_m[m]
        nexts = report["_nexts"]
        for color, perm in enumerate(nexts):
            cycles = cycle_decomposition(perm)
            for cycle in cycles:
                if len(cycle) == instance.vertex_count:
                    continue
                signature = (m, color, tuple(sorted(cycle)))
                if signature in cut_signatures:
                    continue
                cycle_set = set(cycle)
                coeffs: Dict[Tuple[int, int], int] = defaultdict(int)
                const = 0
                for vertex in cycle:
                    coords = instance.coords[vertex]
                    row_idx = instance.row_of_vertex[vertex]
                    for direction in range(DIM):
                        head = neighbor_index(vertex, coords, direction, m, instance.axis_strides)
                        if head in cycle_set:
                            continue
                        if row_idx < 0:
                            if instance.baseline_tuples[vertex][color] == direction:
                                const += 1
                            continue
                        for perm_idx in matching[(color, direction)]:
                            coeffs[(row_idx, perm_idx)] += 1

                if const > 0:
                    cut_signatures.add(signature)
                    continue
                if not coeffs:
                    return added, {
                        "status": "blocked_cycle",
                        "m": m,
                        "color": color,
                        "cycle_size": len(cycle),
                        "cycle_vertices": cycle,
                    }

                model.Add(sum(coeff * variables[key] for key, coeff in coeffs.items()) >= 1)
                cut_signatures.add(signature)
                added += 1

    return added, None


def search_hyperplane_fusion(
    m_values: Sequence[int],
    time_limit_sec: float,
    workers: int,
    random_seed: int,
) -> Dict[str, object]:
    start = time.perf_counter()
    row_keys = _build_row_catalog(m_values)
    row_index_by_key = {key: idx for idx, key in enumerate(row_keys)}
    instances = [_build_instance_cache(m, row_index_by_key) for m in m_values]
    perms = list(itertools.permutations(range(DIM)))

    model = cp_model.CpModel()
    variables = _add_row_one_hot_constraints(model, row_keys, perms)
    _build_indegree_constraints(model, variables, instances, perms)

    iteration_count = 0
    total_cut_count = 0
    cut_signatures: set[Tuple[int, int, Tuple[int, ...]]] = set()
    solver_status_name = "UNKNOWN"
    last_evaluation: Dict[str, object] | None = None
    last_assignment: List[int] | None = None

    while True:
        elapsed = time.perf_counter() - start
        remaining = max(0.0, time_limit_sec - elapsed)
        if remaining <= 0:
            break

        iteration_count += 1
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = remaining
        solver.parameters.num_search_workers = workers
        solver.parameters.random_seed = random_seed
        status = solver.Solve(model)
        solver_status_name = solver.StatusName(status)

        print(
            json.dumps(
                {
                    "iteration": iteration_count,
                    "solver_status": solver_status_name,
                    "elapsed_sec": round(time.perf_counter() - start, 3),
                    "cuts_so_far": total_cut_count,
                }
            ),
            flush=True,
        )

        if status == cp_model.INFEASIBLE:
            payload = {
                "family": "d4_hyperplane_fusion_low_layer_table_v1",
                "dim": DIM,
                "m_values": list(m_values),
                "row_count": len(row_keys),
                "perm_count": len(perms),
                "status": "unsat_exact",
                "solver_status": solver_status_name,
                "runtime_sec": time.perf_counter() - start,
                "time_limit_sec": time_limit_sec,
                "iteration_count": iteration_count,
                "cut_count": total_cut_count,
                "row_schema": [_pattern_key_to_dict(key) for key in row_keys],
            }
            if last_evaluation is not None:
                payload["last_incumbent"] = _serialize_evaluation(last_evaluation)
            return payload

        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            break

        last_assignment = _extract_assignment(solver, variables, len(row_keys), len(perms))
        last_evaluation = _evaluate_assignment(row_keys, last_assignment, perms, instances)

        compact = {
            "iteration": iteration_count,
            "score_total_cycles": last_evaluation["score_total_cycles"],
            "score_max_cycles": last_evaluation["score_max_cycles"],
            "all_hamilton": last_evaluation["all_hamilton"],
            "cycle_counts_by_m": {
                str(report["m"]): [stat["cycle_count"] for stat in report["color_stats"]]
                for report in last_evaluation["instance_reports"]
            },
        }
        print(json.dumps(compact), flush=True)

        if last_evaluation["all_hamilton"]:
            return {
                "family": "d4_hyperplane_fusion_low_layer_table_v1",
                "dim": DIM,
                "m_values": list(m_values),
                "row_count": len(row_keys),
                "perm_count": len(perms),
                "status": "hamilton_witness",
                "solver_status": solver_status_name,
                "runtime_sec": time.perf_counter() - start,
                "time_limit_sec": time_limit_sec,
                "iteration_count": iteration_count,
                "cut_count": total_cut_count,
                "result": _serialize_evaluation(last_evaluation),
            }

        new_cuts, blocked = _add_cycle_cuts(model, variables, perms, instances, last_evaluation, cut_signatures)
        total_cut_count += new_cuts
        if blocked is not None:
            return {
                "family": "d4_hyperplane_fusion_low_layer_table_v1",
                "dim": DIM,
                "m_values": list(m_values),
                "row_count": len(row_keys),
                "perm_count": len(perms),
                "status": "blocked_cycle",
                "solver_status": solver_status_name,
                "runtime_sec": time.perf_counter() - start,
                "time_limit_sec": time_limit_sec,
                "iteration_count": iteration_count,
                "cut_count": total_cut_count,
                "blocked_cycle": blocked,
                "last_incumbent": _serialize_evaluation(last_evaluation),
            }
        if new_cuts == 0:
            break

    payload = {
        "family": "d4_hyperplane_fusion_low_layer_table_v1",
        "dim": DIM,
        "m_values": list(m_values),
        "row_count": len(row_keys),
        "perm_count": len(perms),
        "status": "timeout",
        "solver_status": solver_status_name,
        "runtime_sec": time.perf_counter() - start,
        "time_limit_sec": time_limit_sec,
        "iteration_count": iteration_count,
        "cut_count": total_cut_count,
        "row_schema": [_pattern_key_to_dict(key) for key in row_keys],
    }
    if last_evaluation is not None:
        payload["last_incumbent"] = _serialize_evaluation(last_evaluation)
    if last_assignment is not None:
        payload["last_row_assignment"] = _canonical_table_json(row_keys, last_assignment, perms, m_values)
    return payload


def _serialize_evaluation(evaluation: Dict[str, object]) -> Dict[str, object]:
    instance_reports = []
    for report in evaluation["instance_reports"]:
        clean = dict(report)
        clean.pop("_nexts", None)
        instance_reports.append(clean)
    return {
        "row_table": evaluation["row_table"],
        "all_hamilton": evaluation["all_hamilton"],
        "score_total_cycles": evaluation["score_total_cycles"],
        "score_max_cycles": evaluation["score_max_cycles"],
        "instance_reports": instance_reports,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search a shared low-layer hyperplane-fusion table on the directed 4-torus."
    )
    parser.add_argument(
        "--m-list",
        default="3,4,5,6",
        help="comma-separated list of m values to constrain simultaneously",
    )
    parser.add_argument("--time-limit-sec", type=float, default=600.0, help="global wall-clock limit")
    parser.add_argument("--workers", type=int, default=8, help="CP-SAT worker count")
    parser.add_argument("--random-seed", type=int, default=0, help="fixed random seed for reproducibility")
    parser.add_argument("--out", type=Path, help="write JSON result to this path")
    args = parser.parse_args()

    m_values = _parse_m_list(args.m_list)
    if not m_values:
        raise SystemExit("Need at least one m value.")
    if any(m < 3 for m in m_values):
        raise SystemExit("This search assumes m >= 3.")
    if any(m_values[idx] >= m_values[idx + 1] for idx in range(len(m_values) - 1)):
        raise SystemExit("Please supply m values in strictly increasing order.")

    result = search_hyperplane_fusion(
        m_values=m_values,
        time_limit_sec=args.time_limit_sec,
        workers=args.workers,
        random_seed=args.random_seed,
    )

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2))
    print(json.dumps({"status": result["status"], "runtime_sec": result["runtime_sec"]}, indent=2))


if __name__ == "__main__":
    main()
