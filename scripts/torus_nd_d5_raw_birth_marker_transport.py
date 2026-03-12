#!/usr/bin/env python3
"""Extract the raw birth formulas and tagged transport target for the best-seed corridor."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

import torus_nd_d5_corridor_phase_clarification as clar036
import torus_nd_d5_corridor_phase_extraction as phase034
import torus_nd_d5_endpoint_latin_repair as seed032
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-RAW-BIRTH-MARKER-TRANSPORT-039"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M_VALUES = (11,)
ALL_M_VALUES = PRIMARY_M_VALUES + CONTROL_M_VALUES
REPRESENTATIVE_REGULAR_U = 1
REPRESENTATIVE_EXCEPTIONAL_U = 3


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _coords_payload(prepared: seed032.PreparedSearch, idx: int) -> Dict[str, int]:
    coords = prepared.pre["coords"][idx]
    w_value = int(coords[2])
    u_value = int(coords[4])
    return {
        "x0": int(coords[0]),
        "q": int(coords[1]),
        "w": w_value,
        "v": int(coords[3]),
        "u": u_value,
        "s": int((w_value + u_value) % prepared.m),
        "layer": int(sum(coords) % prepared.m),
    }


def _matches_source_formula(payload: Mapping[str, int], m: int) -> bool:
    return (
        int(payload["layer"]) == 1
        and int(payload["q"]) == m - 1
        and int(payload["w"]) == 0
        and int(payload["u"]) != 0
    )


def _matches_exceptional_source_formula(payload: Mapping[str, int], m: int) -> bool:
    return (
        int(payload["layer"]) == 1
        and int(payload["q"]) == m - 1
        and int(payload["w"]) == 0
        and int(payload["u"]) == REPRESENTATIVE_EXCEPTIONAL_U
    )


def _matches_entry_formula(payload: Mapping[str, int], m: int) -> bool:
    return (
        int(payload["layer"]) == 2
        and int(payload["q"]) == m - 1
        and int(payload["w"]) == 1
        and int(payload["u"]) != 0
    )


def _matches_exceptional_entry_formula(payload: Mapping[str, int], m: int) -> bool:
    return (
        int(payload["layer"]) == 2
        and int(payload["q"]) == m - 1
        and int(payload["w"]) == 1
        and int(payload["u"]) == REPRESENTATIVE_EXCEPTIONAL_U
    )


def _per_m_analysis(m: int) -> Dict[str, object]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    nexts_all, meta = phase034._build_best_seed(prepared)
    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    coords = prepared.pre["coords"]
    step_by_dir = prepared.pre["step_by_dir"]
    hole_l1 = phase034._hole_l1_set(prepared, row)

    source = {idx for idx, label in enumerate(labels) if label == "R1"}
    exceptional_source = {idx for idx in source if int(coords[idx][4]) == REPRESENTATIVE_EXCEPTIONAL_U}
    entry = {int(step_by_dir[2][idx]) for idx in source}
    exceptional_entry = {int(step_by_dir[2][idx]) for idx in exceptional_source}

    formula_source = {idx for idx in range(len(coords)) if _matches_source_formula(_coords_payload(prepared, idx), m)}
    formula_exceptional_source = {
        idx for idx in range(len(coords)) if _matches_exceptional_source_formula(_coords_payload(prepared, idx), m)
    }
    formula_entry = {idx for idx in range(len(coords)) if _matches_entry_formula(_coords_payload(prepared, idx), m)}
    formula_exceptional_entry = {
        idx for idx in range(len(coords)) if _matches_exceptional_entry_formula(_coords_payload(prepared, idx), m)
    }

    regular_source_index = next(idx for idx in source if int(coords[idx][4]) == REPRESENTATIVE_REGULAR_U)
    exceptional_source_index = next(iter(exceptional_source))
    regular_trace = clar036._trace_source(prepared, row, regular_source_index, hole_l1)
    exceptional_trace = clar036._trace_source(prepared, row, exceptional_source_index, hole_l1)

    regular_u_values = sorted({int(row_data["coords"]["u"]) for row_data in regular_trace["trace"]})
    exceptional_u_values = sorted({int(row_data["coords"]["u"]) for row_data in exceptional_trace["trace"]})

    regular_entry_index = int(step_by_dir[2][regular_source_index])
    exceptional_entry_index = int(step_by_dir[2][exceptional_source_index])
    regular_exit = regular_trace["trace"][-1]
    exceptional_exit = exceptional_trace["trace"][-1]

    return {
        "m": int(m),
        "formulae": {
            "source": "layer=1, q=m-1, w=0, u!=0",
            "exceptional_source": "layer=1, q=m-1, w=0, u=3",
            "entry": "layer=2, q=m-1, w=1, u!=0",
            "exceptional_entry": "layer=2, q=m-1, w=1, u=3",
        },
        "summary": {
            "source_count": int(len(source)),
            "source_formula_count": int(len(formula_source)),
            "source_formula_exact": bool(source == formula_source),
            "exceptional_source_count": int(len(exceptional_source)),
            "exceptional_source_formula_count": int(len(formula_exceptional_source)),
            "exceptional_source_formula_exact": bool(exceptional_source == formula_exceptional_source),
            "entry_count": int(len(entry)),
            "entry_formula_count": int(len(formula_entry)),
            "entry_formula_exact": bool(entry == formula_entry),
            "exceptional_entry_count": int(len(exceptional_entry)),
            "exceptional_entry_formula_count": int(len(formula_exceptional_entry)),
            "exceptional_entry_formula_exact": bool(exceptional_entry == formula_exceptional_entry),
            "regular_u_drift_all_residues": bool(len(regular_u_values) == m),
            "exceptional_u_drift_all_residues": bool(len(exceptional_u_values) == m),
        },
        "representatives": {
            "regular_source": {
                "source_u": int(REPRESENTATIVE_REGULAR_U),
                "source_coords": _coords_payload(prepared, regular_source_index),
                "entry_coords": _coords_payload(prepared, regular_entry_index),
                "entry_u_preserved": bool(int(coords[regular_source_index][4]) == int(coords[regular_entry_index][4])),
                "first_exit_coords": regular_exit["coords"],
                "first_exit_dirs": [int(value) for value in regular_exit["exit_dirs"]],
                "u_values_seen": regular_u_values,
                "trace_length": int(len(regular_trace["trace"])),
            },
            "exceptional_source": {
                "source_u": int(REPRESENTATIVE_EXCEPTIONAL_U),
                "source_coords": _coords_payload(prepared, exceptional_source_index),
                "entry_coords": _coords_payload(prepared, exceptional_entry_index),
                "entry_u_preserved": bool(int(coords[exceptional_source_index][4]) == int(coords[exceptional_entry_index][4])),
                "first_exit_coords": exceptional_exit["coords"],
                "first_exit_dirs": [int(value) for value in exceptional_exit["exit_dirs"]],
                "u_values_seen": exceptional_u_values,
                "trace_length": int(len(exceptional_trace["trace"])),
            },
        },
        "carrier_model": {
            "states": ["off", "active_reg", "active_exc"],
            "birth": {
                "active_reg": "if layer=1, q=m-1, w=0, u!=0 and u!=3, then take alt-2 and initialize active_reg",
                "active_exc": "if layer=1, q=m-1, w=0, u=3, then take alt-2 and initialize active_exc",
            },
            "entry": {
                "regular_entry_formula": [m - 1, 1, REPRESENTATIVE_REGULAR_U, 2],
                "exceptional_entry_formula": [m - 1, 1, REPRESENTATIVE_EXCEPTIONAL_U, 2],
                "note": "raw current u is preserved at birth, but not later along the corridor",
            },
            "transport_targets": {
                "regular": {
                    "raw_phase": [m - 1, m - 2, 1],
                    "exit_dirs": [2],
                },
                "exceptional": {
                    "raw_phase": [m - 2, m - 1, 1],
                    "exit_dirs": [1],
                },
            },
        },
    }


def _analysis_summary(started: float, per_m: Mapping[str, object]) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "main_result": (
            "The best-seed raw birth classes are exact on current coordinates: "
            "source = {layer=1, q=m-1, w=0, u!=0}, exceptional source = {u=3}, "
            "entry = {layer=2, q=m-1, w=1, u!=0}, exceptional entry = {u=3}. "
            "So birth is already explicit at the reduced raw-coordinate level. "
            "The remaining reduced obstruction is tagged transport, because the "
            "current raw u-value drifts through all residues along both regular "
            "and exceptional corridor traces."
        ),
        "per_m": {
            m: payload["summary"]
            for m, payload in per_m.items()
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the raw birth formulas and tagged transport target for the best-seed corridor.")
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
        out_dir / "source_entry_formula_summary.json",
        {
            m: {
                "formulae": payload["formulae"],
                "summary": payload["summary"],
            }
            for m, payload in per_m.items()
        },
    )
    _write_json(
        out_dir / "family_bit_drift_summary.json",
        {
            m: {
                "regular_source": {
                    "source_u": payload["representatives"]["regular_source"]["source_u"],
                    "trace_length": payload["representatives"]["regular_source"]["trace_length"],
                    "u_values_seen": payload["representatives"]["regular_source"]["u_values_seen"],
                    "all_residues_seen": payload["summary"]["regular_u_drift_all_residues"],
                },
                "exceptional_source": {
                    "source_u": payload["representatives"]["exceptional_source"]["source_u"],
                    "trace_length": payload["representatives"]["exceptional_source"]["trace_length"],
                    "u_values_seen": payload["representatives"]["exceptional_source"]["u_values_seen"],
                    "all_residues_seen": payload["summary"]["exceptional_u_drift_all_residues"],
                },
            }
            for m, payload in per_m.items()
        },
    )
    _write_json(
        out_dir / "carrier_model_summary.json",
        {
            m: {
                "carrier_model": payload["carrier_model"],
                "representatives": payload["representatives"],
            }
            for m, payload in per_m.items()
        },
    )
    _write_json(args.summary_out, summary)


if __name__ == "__main__":
    main()
