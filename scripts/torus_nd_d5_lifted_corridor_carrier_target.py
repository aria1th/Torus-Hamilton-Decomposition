#!/usr/bin/env python3
"""Extract the raw-coordinate odometer and reduced carrier target for the best-seed corridor."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Mapping

import torus_nd_d5_corridor_phase_clarification as clar036
import torus_nd_d5_corridor_phase_extraction as phase034
import torus_nd_d5_endpoint_latin_repair as seed032
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-LIFTED-CORRIDOR-CARRIER-TARGET-037"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M_VALUES = (11,)
ALL_M_VALUES = PRIMARY_M_VALUES + CONTROL_M_VALUES
REPRESENTATIVE_REGULAR_U = 1
REPRESENTATIVE_EXCEPTIONAL_U = 3


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _chi(m: int, q_value: int, w_value: int, layer: int) -> int:
    q_hat = (q_value - (1 if layer == 1 else 0)) % m
    w_hat = (w_value - (1 if layer != 2 and q_hat == m - 1 else 0)) % m
    return int(
        (
            m * ((q_hat + m * ((w_hat - 1) % m) - (m - 1)) % (m * m))
            + ((layer - 2) % m)
        )
        % (m**3)
    )


def _per_m_analysis(m: int) -> Dict[str, object]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    nexts_all, meta = phase034._build_best_seed(prepared)
    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    coords = prepared.pre["coords"]
    hole_l1 = phase034._hole_l1_set(prepared, row)

    relation_ok = True
    raw_rule_ok = True
    chi_ok = True
    per_source_rows = []
    representative_traces = {}

    for u_value in range(1, m):
        source_index = next(idx for idx, label in enumerate(labels) if label == "R1" and int(coords[idx][4]) == u_value)
        trace_row = clar036._trace_source(prepared, row, source_index, hole_l1)
        rho = int(trace_row["rho"])
        family = "exceptional" if u_value == REPRESENTATIVE_EXCEPTIONAL_U else "regular"

        reduced_trace: List[Dict[str, object]] = []
        for idx, row_data in enumerate(trace_row["trace"]):
            q_value = int(row_data["coords"]["q"])
            w_value = int(row_data["coords"]["w"])
            layer = int(row_data["coords"]["layer"])
            a_value = int(row_data["normalized_phase"][0])
            relation_ok &= a_value == (q_value + w_value - (1 if layer == 1 else 0)) % m
            entry = {
                "step": int(row_data["step"]),
                "q": q_value,
                "w": w_value,
                "layer": layer,
                "a": a_value,
                "chi": _chi(m, q_value, w_value, layer),
                "exit_dirs": [int(value) for value in row_data["exit_dirs"]],
            }
            if idx + 1 < len(trace_row["trace"]):
                next_row = trace_row["trace"][idx + 1]
                next_q = int(next_row["coords"]["q"])
                next_w = int(next_row["coords"]["w"])
                next_layer = int(next_row["coords"]["layer"])
                pred = None
                if layer == 0:
                    pred = [(q_value + 1) % m, w_value, 1]
                elif layer == 1:
                    pred = [q_value, w_value, 2]
                elif layer == 2:
                    pred = [q_value, (w_value + (1 if q_value == m - 1 else 0)) % m, 3]
                else:
                    pred = [q_value, w_value, (layer + 1) % m]
                actual = [next_q, next_w, next_layer]
                raw_rule_ok &= pred == actual
                chi_ok &= (_chi(m, next_q, next_w, next_layer) == (_chi(m, q_value, w_value, layer) + 1) % (m**3))
                entry["predicted_next_raw_phase"] = pred
                entry["actual_next_raw_phase"] = actual
                entry["actual_next_chi"] = _chi(m, next_q, next_w, next_layer)
            reduced_trace.append(entry)

        exit_row = reduced_trace[-1]
        per_source_rows.append(
            {
                "source_u": int(u_value),
                "family": family,
                "entry_raw_phase": [reduced_trace[0]["q"], reduced_trace[0]["w"], reduced_trace[0]["layer"]],
                "entry_chi": int(reduced_trace[0]["chi"]),
                "first_exit_step": int(exit_row["step"]),
                "first_exit_raw_phase": [exit_row["q"], exit_row["w"], exit_row["layer"]],
                "first_exit_dirs": exit_row["exit_dirs"],
                "first_exit_chi": int(exit_row["chi"]),
            }
        )

        if u_value == REPRESENTATIVE_REGULAR_U:
            representative_traces["regular"] = reduced_trace
        if u_value == REPRESENTATIVE_EXCEPTIONAL_U:
            representative_traces["exceptional"] = reduced_trace

    regular_rows = [row for row in per_source_rows if row["family"] == "regular"]
    exceptional_rows = [row for row in per_source_rows if row["family"] == "exceptional"]
    regular_target = regular_rows[0]
    exceptional_target = exceptional_rows[0]
    chi_gap = int((exceptional_target["first_exit_chi"] - regular_target["first_exit_chi"]) % (m**3))

    return {
        "m": int(m),
        "summary": {
            "raw_relation_matches_all_traced_states": bool(relation_ok),
            "raw_rule_matches_until_first_exit": bool(raw_rule_ok),
            "chi_increments_by_one": bool(chi_ok),
            "regular_target_raw_phase": regular_target["first_exit_raw_phase"],
            "regular_target_dir": regular_target["first_exit_dirs"],
            "regular_target_chi": int(regular_target["first_exit_chi"]),
            "exceptional_target_raw_phase": exceptional_target["first_exit_raw_phase"],
            "exceptional_target_dir": exceptional_target["first_exit_dirs"],
            "exceptional_target_chi": int(exceptional_target["first_exit_chi"]),
            "target_gap": int(chi_gap),
            "target_gap_formula": int(m * (m - 1)),
        },
        "raw_model": {
            "relation": "a = q + w - 1_{layer=1} mod m",
            "rule": "(q,w,0)->(q+1,w,1); (q,w,1)->(q,w,2); (q,w,2)->(q,w+1_{q=m-1},3); otherwise (q,w,layer)->(q,w,layer+1 mod m)",
            "chi": "chi = m*(qHat + m*(wHat-1) - (m-1)) + (layer-2 mod m), with qHat = q - 1_{layer=1}, wHat = w - 1_{layer!=2}1_{qHat=m-1}",
        },
        "carrier_target": {
            "entry_raw_phase": [m - 1, 1, 2],
            "entry_chi": 0,
            "regular_target_raw_phase": regular_target["first_exit_raw_phase"],
            "regular_target_chi": int(regular_target["first_exit_chi"]),
            "regular_target_dir": regular_target["first_exit_dirs"],
            "exceptional_target_raw_phase": exceptional_target["first_exit_raw_phase"],
            "exceptional_target_chi": int(exceptional_target["first_exit_chi"]),
            "exceptional_target_dir": exceptional_target["first_exit_dirs"],
            "carrier_model": "one active corridor-local marker plus one family bit (regular vs exceptional); transport by chi->chi+1; fire at family-specific target chi",
        },
        "per_source_rows": per_source_rows,
        "representative_traces": representative_traces,
    }


def _analysis_summary(started: float, per_m: Mapping[str, object]) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "main_result": (
            "The lifted corridor state from 036 is already visible on raw current coordinates. "
            "Along every traced best-seed corridor state up to first exit, a = q + w - 1_{layer=1} mod m, "
            "the raw triple (q,w,layer) follows an exact odometer rule, and the unresolved channel reduces to "
            "a localized carrier problem rather than a hidden-phase problem."
        ),
        "per_m": {
            str(m): per_m[str(m)]["summary"]
            for m in ALL_M_VALUES
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the raw-coordinate odometer and carrier target for the best-seed corridor.")
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
        out_dir / "raw_visibility_summary.json",
        {
            str(m): {
                "summary": per_m[str(m)]["summary"],
                "raw_model": per_m[str(m)]["raw_model"],
            }
            for m in ALL_M_VALUES
        },
    )
    _write_json(
        out_dir / "carrier_target_summary.json",
        {
            str(m): {
                "carrier_target": per_m[str(m)]["carrier_target"],
                "per_source_rows": per_m[str(m)]["per_source_rows"],
            }
            for m in ALL_M_VALUES
        },
    )
    _write_json(
        out_dir / "representative_raw_traces.json",
        {
            str(m): per_m[str(m)]["representative_traces"]
            for m in ALL_M_VALUES
        },
    )
    _write_json(args.summary_out, summary)


if __name__ == "__main__":
    main()
