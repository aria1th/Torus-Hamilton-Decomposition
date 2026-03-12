#!/usr/bin/env python3
"""Clarify the 034 corridor-phase convention and extract the lifted long-run model."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_corridor_phase_extraction as phase034
import torus_nd_d5_endpoint_latin_repair as seed032
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-CORRIDOR-PHASE-CLARIFICATION-036"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M_VALUES = (11,)
ALL_M_VALUES = PRIMARY_M_VALUES + CONTROL_M_VALUES
REPRESENTATIVE_REGULAR_U = 1
REPRESENTATIVE_EXCEPTIONAL_U = 3


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _normalized_a(payload: Mapping[str, int], rho: int, m: int) -> int:
    return int((payload["s"] - rho) % m)


def _first_pass_next(a_value: int, layer: int, m: int) -> Tuple[int, int]:
    if layer == 1:
        return ((a_value + 1) % m, 2)
    if layer == 2 and a_value == 0:
        return ((a_value + 1) % m, 3)
    return (a_value, (layer + 1) % m)


def _lifted_next(q_value: int, a_value: int, layer: int, m: int) -> Tuple[int, int, int]:
    if layer == 0:
        return ((q_value + 1) % m, a_value, 1)
    if layer == 1:
        return (q_value, (a_value + 1) % m, 2)
    if layer == 2:
        return (q_value, (a_value + (1 if q_value == m - 1 else 0)) % m, 3)
    return (q_value, a_value, (layer + 1) % m)


def _trace_source(
    prepared: seed032.PreparedSearch,
    row: Sequence[int],
    source_index: int,
    hole_l1: set[int],
) -> Dict[str, object]:
    source_payload = phase034._coords_payload(prepared, source_index)
    rho = int((source_payload["u"] + 1) % prepared.m)
    step_by_dir = prepared.pre["step_by_dir"]
    current = step_by_dir[2][source_index]
    seen = set()
    trace_rows: List[Dict[str, object]] = []
    while current not in seen:
        seen.add(current)
        payload = phase034._coords_payload(prepared, current)
        exit_dirs = [direction for direction in range(5) if step_by_dir[direction][current] in hole_l1]
        a_value = _normalized_a(payload, rho, prepared.m)
        row_data: Dict[str, object] = {
            "step": len(trace_rows),
            "coords": payload,
            "phase": [int(payload["s"]), int(payload["layer"])],
            "normalized_phase": [a_value, int(payload["layer"])],
            "lifted_phase": [int(payload["q"]), a_value, int(payload["layer"])],
            "exit_dirs": [int(value) for value in exit_dirs],
        }
        if not exit_dirs:
            next_payload = phase034._coords_payload(prepared, row[current])
            next_a = _normalized_a(next_payload, rho, prepared.m)
            row_data["actual_next_phase"] = [int(next_payload["s"]), int(next_payload["layer"])]
            row_data["actual_next_normalized_phase"] = [next_a, int(next_payload["layer"])]
            row_data["actual_next_lifted_phase"] = [int(next_payload["q"]), next_a, int(next_payload["layer"])]
            row_data["predicted_first_pass_next"] = list(_first_pass_next(a_value, int(payload["layer"]), prepared.m))
            row_data["predicted_lifted_next"] = list(_lifted_next(int(payload["q"]), a_value, int(payload["layer"]), prepared.m))
        trace_rows.append(row_data)
        if exit_dirs:
            break
        current = row[current]

    first_phase_repeat = None
    first_pass_mismatch = None
    first_lift_repeat = None
    by_phase: Dict[Tuple[int, int], int] = {}
    by_lift: Dict[Tuple[int, int, int], int] = {}
    for idx, row_data in enumerate(trace_rows[:-1]):
        phase = tuple(int(value) for value in row_data["phase"])
        lift = tuple(int(value) for value in row_data["lifted_phase"])
        next_phase = tuple(int(value) for value in row_data["actual_next_phase"])
        next_lift = tuple(int(value) for value in row_data["actual_next_lifted_phase"])
        prev_idx = by_phase.get(phase)
        if prev_idx is None:
            by_phase[phase] = idx
        elif first_phase_repeat is None:
            first_phase_repeat = {
                "first_index": int(prev_idx),
                "repeat_index": int(idx),
                "phase": list(phase),
                "first_next_phase": list(tuple(int(value) for value in trace_rows[prev_idx]["actual_next_phase"])),
                "repeat_next_phase": list(next_phase),
            }
            if tuple(int(value) for value in trace_rows[prev_idx]["actual_next_phase"]) != next_phase:
                first_pass_mismatch = {
                    "first_index": int(prev_idx),
                    "repeat_index": int(idx),
                    "phase": list(phase),
                    "first_next_phase": list(tuple(int(value) for value in trace_rows[prev_idx]["actual_next_phase"])),
                    "repeat_next_phase": list(next_phase),
                }
        prev_lift_idx = by_lift.get(lift)
        if prev_lift_idx is None:
            by_lift[lift] = idx
        elif first_lift_repeat is None:
            first_lift_repeat = {
                "first_index": int(prev_lift_idx),
                "repeat_index": int(idx),
                "lifted_phase": list(lift),
                "first_next_lifted_phase": list(tuple(int(value) for value in trace_rows[prev_lift_idx]["actual_next_lifted_phase"])),
                "repeat_next_lifted_phase": list(next_lift),
            }

    first_exit_row = trace_rows[-1]
    return {
        "source_u": int(source_payload["u"]),
        "source_coords": source_payload,
        "rho": rho,
        "entry_phase": trace_rows[0]["phase"],
        "entry_normalized_phase": trace_rows[0]["normalized_phase"],
        "entry_lifted_phase": trace_rows[0]["lifted_phase"],
        "first_exit_step": int(first_exit_row["step"]),
        "first_exit_phase": first_exit_row["phase"],
        "first_exit_normalized_phase": first_exit_row["normalized_phase"],
        "first_exit_lifted_phase": first_exit_row["lifted_phase"],
        "first_exit_dirs": first_exit_row["exit_dirs"],
        "first_phase_repeat": first_phase_repeat,
        "first_pass_mismatch": first_pass_mismatch,
        "first_lift_repeat": first_lift_repeat,
        "trace": trace_rows,
    }


def _per_m_analysis(m: int) -> Dict[str, object]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    nexts_all, meta = phase034._build_best_seed(prepared)
    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    coords = prepared.pre["coords"]
    hole_l1 = phase034._hole_l1_set(prepared, row)

    traces = []
    first_pass_rule_ok = True
    lifted_rule_ok = True
    regular_exit_lift = None
    exceptional_exit_lift = None
    regular_exit_dir = None
    exceptional_exit_dir = None
    representative_rows = {}

    for u_value in range(1, m):
        source_index = next(idx for idx, label in enumerate(labels) if label == "R1" and int(coords[idx][4]) == u_value)
        trace_row = _trace_source(prepared, row, source_index, hole_l1)
        traces.append(trace_row)

        trace = trace_row["trace"]
        first_repeat_idx = trace_row["first_phase_repeat"]["repeat_index"] if trace_row["first_phase_repeat"] else len(trace)
        for row_data in trace[: max(first_repeat_idx, 0)]:
            if "actual_next_normalized_phase" not in row_data:
                continue
            actual = tuple(int(value) for value in row_data["actual_next_normalized_phase"])
            predicted = tuple(int(value) for value in row_data["predicted_first_pass_next"])
            first_pass_rule_ok &= actual == predicted
        for row_data in trace:
            if "actual_next_lifted_phase" not in row_data:
                continue
            actual = tuple(int(value) for value in row_data["actual_next_lifted_phase"])
            predicted = tuple(int(value) for value in row_data["predicted_lifted_next"])
            lifted_rule_ok &= actual == predicted

        if u_value == REPRESENTATIVE_REGULAR_U:
            representative_rows["regular"] = trace_row
        if u_value == REPRESENTATIVE_EXCEPTIONAL_U:
            representative_rows["exceptional"] = trace_row

        if u_value != REPRESENTATIVE_EXCEPTIONAL_U:
            regular_exit_lift = trace_row["first_exit_lifted_phase"]
            regular_exit_dir = trace_row["first_exit_dirs"]
        else:
            exceptional_exit_lift = trace_row["first_exit_lifted_phase"]
            exceptional_exit_dir = trace_row["first_exit_dirs"]

    return {
        "m": int(m),
        "summary": {
            "first_pass_phase_is_not_full_factor": bool(any(row["first_pass_mismatch"] is not None for row in traces)),
            "first_pass_rule_matches_until_first_phase_repeat": bool(first_pass_rule_ok),
            "lifted_rule_matches_until_first_exit": bool(lifted_rule_ok),
            "entry_lift_formula": [int(m - 1), 0, 2],
            "regular_exit_lift_formula": regular_exit_lift,
            "regular_exit_dir": regular_exit_dir,
            "exceptional_exit_lift_formula": exceptional_exit_lift,
            "exceptional_exit_dir": exceptional_exit_dir,
        },
        "first_pass_rule": {
            "coordinates": "(a, layer) with a = s - rho mod m and rho = u_source + 1 mod m",
            "rule": "(0,2)->(1,3); (a,1)->(a+1,2); otherwise (a,layer)->(a,layer+1 mod m)",
            "scope": "matches the extracted first phase lap until the first repeated normalized phase",
        },
        "lifted_rule": {
            "coordinates": "(q, a, layer) with a = s - rho mod m and rho = u_source + 1 mod m",
            "rule": "(q,a,0)->(q+1,a,1); (q,a,1)->(q,a+1,2); (q,a,2)->(q,a+1,3) if q=m-1 else (q,a,3); otherwise (q,a,layer)->(q,a,layer+1 mod m)",
            "scope": "matches every traced corridor step up to the first H_L1-legal exit for all source families",
        },
        "representative_traces": representative_rows,
        "all_source_rows": [
            {
                "source_u": int(row["source_u"]),
                "rho": int(row["rho"]),
                "entry_lifted_phase": row["entry_lifted_phase"],
                "first_exit_step": int(row["first_exit_step"]),
                "first_exit_lifted_phase": row["first_exit_lifted_phase"],
                "first_exit_dirs": row["first_exit_dirs"],
                "first_phase_repeat": row["first_phase_repeat"],
                "first_pass_mismatch": row["first_pass_mismatch"],
            }
            for row in traces
        ],
    }


def _analysis_summary(started: float, per_m: Mapping[str, object]) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "main_result": (
            "The saved 034 (s,layer) phase rule is only a first-pass projected phase lap. "
            "It does not remain a deterministic factor of the full long corridor. The long "
            "corridor does admit an exact lifted deterministic model on (q,a,layer), where "
            "a = s - rho mod m and rho = u_source + 1."
        ),
        "per_m": {
            str(m): per_m[str(m)]["summary"]
            for m in ALL_M_VALUES
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Clarify the 034 corridor-phase convention and extract the lifted long-run model.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    per_m = {str(m): _per_m_analysis(m) for m in ALL_M_VALUES}
    summary = _analysis_summary(started, per_m)

    _write_json(out_dir / "analysis_summary.json", summary)
    _write_json(
        out_dir / "phase_clarification_summary.json",
        {
            str(m): {
                "summary": per_m[str(m)]["summary"],
                "first_pass_rule": per_m[str(m)]["first_pass_rule"],
                "lifted_rule": per_m[str(m)]["lifted_rule"],
                "all_source_rows": per_m[str(m)]["all_source_rows"],
            }
            for m in ALL_M_VALUES
        },
    )
    _write_json(
        out_dir / "representative_corridor_traces.json",
        {
            str(m): per_m[str(m)]["representative_traces"]
            for m in ALL_M_VALUES
        },
    )
    _write_json(
        out_dir / "phase_mismatch_examples.json",
        {
            str(m): {
                "regular": per_m[str(m)]["representative_traces"]["regular"]["first_pass_mismatch"],
                "exceptional": per_m[str(m)]["representative_traces"]["exceptional"]["first_pass_mismatch"],
            }
            for m in ALL_M_VALUES
        },
    )
    _write_json(args.summary_out, summary)


if __name__ == "__main__":
    main()
