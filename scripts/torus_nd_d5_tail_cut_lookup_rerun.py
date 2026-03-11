#!/usr/bin/env python3
"""Pilot rerun with the exact hypergraph-derived tail_cut lookup bit."""

from __future__ import annotations

import argparse
import json
import platform
import time
from collections import Counter, defaultdict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from ortools.sat.python import cp_model

from torus_nd_d5_master_field_quotient_family import (
    DIM,
    SCHEMA_BY_NAME,
    SCHEMA_PHASE_ALIGN_TAIL_CUT,
    anchor_table_payload,
    anchor_values_to_permutation_table,
    analyze_latin,
    color_cycle_summary,
    first_return_qwu_for_color0,
    old_collapse_law_for_color0,
    orbit_table_payload,
    preferred_anchor_value,
    predecessor_patterns,
    rotate_state,
    rotation_orbit_histogram,
    rotation_orbits,
    schema_state_counts_by_m,
    schema_state_space,
    state_table_payload,
    state_to_id_map,
)

TASK_ID = "D5-TAIL-CUT-QUOTIENT-RERUN-001"
OLD_SIGNATURE_MASK = (1 << 6) - 1

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


def _old_state_key_from_serialized(state: Dict[str, object]) -> Tuple[object, Tuple[int, ...]]:
    return (state["layer_bucket"], tuple(int(value) for value in state["signature"]))


def _project_new_state_to_old(state: Tuple[object, Tuple[int, ...]]) -> Tuple[object, Tuple[int, ...]]:
    return (state[0], tuple(int(value) & OLD_SIGNATURE_MASK for value in state[1]))


def _load_base_anchor_map(base_field_json: Path) -> Dict[Tuple[object, Tuple[int, ...]], int]:
    payload = json.loads(base_field_json.read_text())
    return {
        _old_state_key_from_serialized(row["state"]): int(row["anchor_value"])
        for row in payload["anchor_table"]["rows"]
    }


def _projection_anchor_values(
    states: Sequence[Tuple[object, Tuple[int, ...]]],
    base_anchor_map: Dict[Tuple[object, Tuple[int, ...]], int],
) -> Dict[int, int]:
    out = {}
    for state_id, state in enumerate(states):
        out[state_id] = base_anchor_map[_project_new_state_to_old(state)]
    return out


def _palette_by_layer(anchor_rows: Sequence[Dict[str, object]]) -> Dict[str, object]:
    palette = defaultdict(lambda: {"permutations": Counter(), "color0_outputs": Counter()})
    for row in anchor_rows:
        layer = str(row["state"]["layer_bucket"])
        palette[layer]["permutations"][row["permutation_name"]] += 1
        palette[layer]["color0_outputs"][str(row["permutation"][0])] += 1
    ordered = {}
    for layer in sorted(palette, key=lambda item: (4, item) if item == "4+" else (int(item), item)):
        ordered[layer] = {
            "permutation_histogram": dict(sorted(palette[layer]["permutations"].items())),
            "color0_output_histogram": dict(sorted(palette[layer]["color0_outputs"].items())),
            "is_constant_permutation": len(palette[layer]["permutations"]) == 1,
            "constant_permutation": next(iter(palette[layer]["permutations"])) if len(palette[layer]["permutations"]) == 1 else None,
            "is_constant_color0_output": len(palette[layer]["color0_outputs"]) == 1,
            "constant_color0_output": int(next(iter(palette[layer]["color0_outputs"]))) if len(palette[layer]["color0_outputs"]) == 1 else None,
        }
    return ordered


def _validation_bundle(
    anchor_values: Dict[int, int],
    states: Sequence[Tuple[object, Tuple[int, ...]]],
    schema_name: str,
    m_values: Sequence[int],
    state_space_key: Tuple[int, ...],
) -> Dict[str, object]:
    schema = SCHEMA_BY_NAME[schema_name]
    perm_table = anchor_values_to_permutation_table(states, anchor_values)
    return {
        str(m): {
            "latin": analyze_latin(perm_table, schema, m, state_space_key),
            "old_collapse_law": old_collapse_law_for_color0(perm_table, schema, m, state_space_key),
            "color_cycles": color_cycle_summary(perm_table, schema, m, state_space_key),
            "color0_return": first_return_qwu_for_color0(perm_table, schema, m, state_space_key),
        }
        for m in m_values
    }


def _build_model(schema_name: str, pilot_m_values: Sequence[int]):
    state_space_key = tuple(sorted(set(pilot_m_values)))
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
                model.Add(
                    sum(
                        anchor_vars[(rotated_ids[(pattern[direction], (-color) % DIM)], (direction - color) % DIM)]
                        for direction in range(DIM)
                    )
                    == 1
                )

    preference_terms = []
    for state_id, state in enumerate(states):
        preferred = preferred_anchor_value(state)
        if preferred is not None:
            preference_terms.append(anchor_vars[(state_id, preferred)])
    preference_expr = sum(preference_terms)
    return model, states, state_space_key, anchor_vars, preference_expr, pattern_counts


def _extract_anchor_values(anchor_vars: Dict[Tuple[int, int], cp_model.IntVar], solver: cp_model.CpSolver, *, state_count: int) -> Dict[int, int]:
    return {
        state_id: next(value for value in range(DIM) if solver.Value(anchor_vars[(state_id, value)]))
        for state_id in range(state_count)
    }


def _extend_anchor_values_to_full_union(
    pilot_states: Sequence[Tuple[object, Tuple[int, ...]]],
    pilot_anchor_values: Dict[int, int],
    full_states: Sequence[Tuple[object, Tuple[int, ...]]],
    base_anchor_map: Dict[Tuple[object, Tuple[int, ...]], int],
) -> Dict[int, int]:
    pilot_state_map = {state: pilot_anchor_values[state_id] for state_id, state in enumerate(pilot_states)}
    out = {}
    for state_id, state in enumerate(full_states):
        out[state_id] = pilot_state_map.get(state, base_anchor_map[_project_new_state_to_old(state)])
    return out


def _field_payload(
    field_name: str,
    anchor_values: Dict[int, int],
    states: Sequence[Tuple[object, Tuple[int, ...]]],
    schema_name: str,
    pilot_m_values: Sequence[int],
    pilot_state_space_key: Tuple[int, ...],
    full_states: Sequence[Tuple[object, Tuple[int, ...]]],
    full_anchor_values: Dict[int, int],
    full_state_space_key: Tuple[int, ...],
    stability_m_values: Sequence[int],
    preference_score: int,
    changed_state_count: int | None = None,
) -> Dict[str, object]:
    anchor_table = anchor_table_payload(SCHEMA_BY_NAME[schema_name], states, anchor_values)
    return {
        "field_name": field_name,
        "preference_score": int(preference_score),
        "changed_state_count_vs_lifted": changed_state_count,
        "anchor_table": anchor_table,
        "layer_palette": _palette_by_layer(anchor_table["rows"]),
        "pilot_validation": _validation_bundle(anchor_values, states, schema_name, pilot_m_values, pilot_state_space_key),
        "stability_validation_via_projected_extension": _validation_bundle(
            full_anchor_values,
            full_states,
            schema_name,
            stability_m_values,
            full_state_space_key,
        ),
    }


def run_rerun(
    *,
    base_field_json: Path,
    pilot_m_values: Sequence[int],
    stability_m_values: Sequence[int],
    max_time_sec: float,
    workers: int,
    random_seed: int,
) -> Dict[str, object]:
    start = time.perf_counter()
    schema_name = SCHEMA_PHASE_ALIGN_TAIL_CUT.name
    base_anchor_map = _load_base_anchor_map(base_field_json)

    pilot_model, pilot_states, pilot_state_space_key, anchor_vars, preference_expr, pattern_counts = _build_model(schema_name, pilot_m_values)
    lifted_anchor_values = _projection_anchor_values(pilot_states, base_anchor_map)
    for state_id, value in lifted_anchor_values.items():
        pilot_model.AddHint(anchor_vars[(state_id, value)], 1)
    pilot_model.Maximize(preference_expr)

    full_state_space_key = tuple(sorted(set(pilot_m_values) | set(stability_m_values)))
    full_states = schema_state_space(schema_name, full_state_space_key)
    lifted_full_anchor_values = _projection_anchor_values(full_states, base_anchor_map)
    lifted_preference_score = sum(
        1
        for state_id, state in enumerate(pilot_states)
        if preferred_anchor_value(state) is not None and lifted_anchor_values[state_id] == preferred_anchor_value(state)
    )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time_sec
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    status = solver.Solve(pilot_model)

    payload = {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "search_parameters": {
            "schema": schema_name,
            "pilot_m_values": list(pilot_m_values),
            "stability_m_values": list(stability_m_values),
            "pilot_state_space_key": list(pilot_state_space_key),
            "full_state_space_key": list(full_state_space_key),
            "max_time_sec": max_time_sec,
            "workers": workers,
            "random_seed": random_seed,
        },
        "environment": {
            "python_version": platform.python_version(),
            "rich_version": _rich_version(),
            "ortools_version": version("ortools"),
        },
        "schema_summary": {
            "schema": schema_name,
            "schema_description": SCHEMA_BY_NAME[schema_name].description,
            "pilot_state_count": len(pilot_states),
            "full_state_count": len(full_states),
            "rotation_orbit_count": len(rotation_orbits(pilot_states)),
            "rotation_orbit_size_histogram": rotation_orbit_histogram(pilot_states),
            "state_counts_by_m_pilot": {str(m): count for m, count in schema_state_counts_by_m(schema_name, tuple(sorted(set(pilot_m_values))))},
            "state_counts_by_m_full": {str(m): count for m, count in schema_state_counts_by_m(schema_name, full_state_space_key)},
            "pattern_counts": pattern_counts,
        },
        "lifted_field": _field_payload(
            "lifted_projection",
            lifted_anchor_values,
            pilot_states,
            schema_name,
            pilot_m_values,
            pilot_state_space_key,
            full_states,
            lifted_full_anchor_values,
            full_state_space_key,
            stability_m_values,
            lifted_preference_score,
            changed_state_count=0,
        ),
        "solver_status": solver.StatusName(status),
    }

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        solver_anchor_values = _extract_anchor_values(anchor_vars, solver, state_count=len(pilot_states))
        changed_state_count = sum(
            1 for state_id in range(len(pilot_states)) if solver_anchor_values[state_id] != lifted_anchor_values[state_id]
        )
        solver_full_anchor_values = _extend_anchor_values_to_full_union(
            pilot_states,
            solver_anchor_values,
            full_states,
            base_anchor_map,
        )
        payload["solver_field"] = _field_payload(
            "pilot_search_solution",
            solver_anchor_values,
            pilot_states,
            schema_name,
            pilot_m_values,
            pilot_state_space_key,
            full_states,
            solver_full_anchor_values,
            full_state_space_key,
            stability_m_values,
            int(solver.ObjectiveValue()),
            changed_state_count=changed_state_count,
        )
    return payload


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        f"schema={summary['schema_summary']['schema']} pilot_states={summary['schema_summary']['pilot_state_count']} full_states={summary['schema_summary']['full_state_count']}",
        f"solver_status={summary['solver_status']}",
    ]
    lifted = summary["lifted_field"]
    first_m = str(summary["search_parameters"]["pilot_m_values"][0])
    first = lifted["pilot_validation"][first_m]
    lines.append(
        f"lifted: pref={lifted['preference_score']} clean={first['color0_return']['clean_frame']} strict={first['color0_return']['strict_clock']} "
        f"U={first['color0_return']['U_cycle_lengths']} mono={first['color0_return']['monodromies']}"
    )
    solver_field = summary.get("solver_field")
    if solver_field is not None:
        first = solver_field["pilot_validation"][first_m]
        lines.append(
            f"solver: pref={solver_field['preference_score']} changed={solver_field['changed_state_count_vs_lifted']} "
            f"clean={first['color0_return']['clean_frame']} strict={first['color0_return']['strict_clock']} "
            f"U={first['color0_return']['U_cycle_lengths']} mono={first['color0_return']['monodromies']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rerun the d=5 phase-align search with the exact pilot tail_cut lookup bit.")
    parser.add_argument(
        "--base-field-json",
        type=Path,
        default=Path("artifacts/d5_theta_ab_phase_align_001/data/best_strict_collapse_field.json"),
        help="strict-collapse representative to project as a search hint",
    )
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--stability-m-list", default="11,13", help="comma-separated post hoc stability moduli")
    parser.add_argument("--max-time-sec", type=float, default=120.0, help="CP-SAT time budget")
    parser.add_argument("--workers", type=int, default=8, help="CP-SAT worker count")
    parser.add_argument("--random-seed", type=int, default=20260310, help="fixed CP-SAT random seed")
    parser.add_argument("--out", type=Path, required=True, help="write JSON summary to this path")
    parser.add_argument("--state-table-out", type=Path, help="write pilot state table JSON")
    parser.add_argument("--orbit-table-out", type=Path, help="write pilot orbit table JSON")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    pilot_m_values = _parse_m_list(args.pilot_m_list)
    stability_m_values = _parse_m_list(args.stability_m_list)
    summary = run_rerun(
        base_field_json=args.base_field_json,
        pilot_m_values=pilot_m_values,
        stability_m_values=stability_m_values,
        max_time_sec=args.max_time_sec,
        workers=args.workers,
        random_seed=args.random_seed,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))

    if args.state_table_out is not None or args.orbit_table_out is not None:
        pilot_state_space_key = tuple(sorted(set(pilot_m_values)))
        states = schema_state_space(SCHEMA_PHASE_ALIGN_TAIL_CUT.name, pilot_state_space_key)
        if args.state_table_out is not None:
            payload = state_table_payload(SCHEMA_PHASE_ALIGN_TAIL_CUT, states)
            args.state_table_out.parent.mkdir(parents=True, exist_ok=True)
            args.state_table_out.write_text(json.dumps(payload, indent=2))
        if args.orbit_table_out is not None:
            payload = orbit_table_payload(SCHEMA_PHASE_ALIGN_TAIL_CUT, states)
            args.orbit_table_out.parent.mkdir(parents=True, exist_ok=True)
            args.orbit_table_out.write_text(json.dumps(payload, indent=2))

    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
