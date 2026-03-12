#!/usr/bin/env python3
"""Evaluate the first richer observable families for the fixed D5 raw carrier."""

from __future__ import annotations

import argparse
import json
import time
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_corridor_phase_clarification as clar036
import torus_nd_d5_corridor_phase_extraction as phase034
import torus_nd_d5_endpoint_latin_repair as seed032
import torus_nd_d5_layer3_mode_switch_common as mode008
from torus_nd_d5_return_map_model_common import environment_block, runtime_since
from torus_nd_d5_strict_palette_context_common import DIM

TASK_ID = "D5-RICH-OBSERVABLE-RAW-CARRIER-REALIZATION-040"
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


def _successor_coords(coords: Sequence[int], color: int, rel_direction: int, m: int) -> Tuple[int, ...]:
    out = list(coords)
    out[(color + rel_direction) % DIM] = (out[(color + rel_direction) % DIM] + 1) % m
    return tuple(out)


def _simple_full24_row(coords: Sequence[int], color: int, m: int) -> Tuple[int, ...]:
    row: List[int] = [
        int(sum(coords) % m),
        int(mode008.old_bit_q_eq_neg1(coords, color, m)),
        int(mode008.phase_align_value(coords, color, m)),
        int(mode008.wu2_value(coords, color, m)),
    ]
    for rel_direction in range(DIM):
        pred = mode008.predecessor_coords(coords, color, rel_direction, m)
        row.append(int(mode008.phase_align_value(pred, color, m)))
        row.append(int(mode008.wu2_value(pred, color, m)))
    for rel_direction in range(DIM):
        succ = _successor_coords(coords, color, rel_direction, m)
        row.append(int(mode008.phase_align_value(succ, color, m)))
        row.append(int(mode008.wu2_value(succ, color, m)))
    return tuple(row)


def _current_projection_rows(row24: Sequence[int]) -> Tuple[int, ...]:
    return tuple(row24)


def _curpred_projection_rows(row24: Sequence[int]) -> Tuple[int, ...]:
    return tuple(row24[:14])


def _pred_projection_rows(row24: Sequence[int]) -> Tuple[int, ...]:
    return tuple(row24[4:14])


def _matches_source_formula(payload: Mapping[str, int], m: int) -> bool:
    return (
        int(payload["layer"]) == 1
        and int(payload["q"]) == m - 1
        and int(payload["w"]) == 0
        and int(payload["u"]) != 0
    )


def _matches_entry_formula(payload: Mapping[str, int], m: int) -> bool:
    return (
        int(payload["layer"]) == 2
        and int(payload["q"]) == m - 1
        and int(payload["w"]) == 1
        and int(payload["u"]) != 0
    )


def _isolate_count(
    values: Sequence[Tuple[int, ...]],
    target: set[int],
    subset: set[int] | None = None,
) -> Dict[str, object]:
    if subset is None:
        positive = target
        comparison = set(range(len(values))) - target
    else:
        positive = subset
        comparison = target - subset
    positive_values = {values[idx] for idx in positive}
    collision = sum(1 for idx in comparison if values[idx] in positive_values)
    return {"isolates": bool(collision == 0), "collision_count": int(collision)}


def _pairwise_overlap_matrix(family_rows: Mapping[int, set[Tuple[int, int, int, int]]]) -> Dict[str, object]:
    max_overlap = 0
    rows = []
    for left, right in combinations(sorted(family_rows), 2):
        overlap = len(family_rows[left] & family_rows[right])
        max_overlap = max(max_overlap, overlap)
        if overlap > 0 or len(rows) < 10:
            rows.append(
                {
                    "left_source_u": int(left),
                    "right_source_u": int(right),
                    "overlap_count": int(overlap),
                }
            )
    return {
        "max_pairwise_overlap": int(max_overlap),
        "rows": rows[: min(40, len(rows))],
    }


def _per_m_analysis(m: int) -> Dict[str, object]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    nexts_all, meta = phase034._build_best_seed(prepared)
    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    coords = prepared.pre["coords"]
    step_by_dir = prepared.pre["step_by_dir"]
    hole_l1 = phase034._hole_l1_set(prepared, row)

    simple_rows = [_simple_full24_row(vertex, 0, m) for vertex in coords]
    current_full24 = [_current_projection_rows(row24) for row24 in simple_rows]
    current_curpred14 = [_curpred_projection_rows(row24) for row24 in simple_rows]
    current_pred10 = [_pred_projection_rows(row24) for row24 in simple_rows]

    source = {idx for idx, label in enumerate(labels) if label == "R1"}
    exceptional_source = {idx for idx in source if int(coords[idx][4]) == REPRESENTATIVE_EXCEPTIONAL_U}
    entry = {int(step_by_dir[2][idx]) for idx in source}
    exceptional_entry = {int(step_by_dir[2][idx]) for idx in exceptional_source}

    full_row_nogo = {
        "full24": {
            "source": _isolate_count(current_full24, source),
            "entry": _isolate_count(current_full24, entry),
            "source_exc": _isolate_count(current_full24, source, exceptional_source),
            "entry_exc": _isolate_count(current_full24, entry, exceptional_entry),
        },
        "curpred14": {
            "source": _isolate_count(current_curpred14, source),
            "entry": _isolate_count(current_curpred14, entry),
            "source_exc": _isolate_count(current_curpred14, source, exceptional_source),
            "entry_exc": _isolate_count(current_curpred14, entry, exceptional_entry),
        },
        "pred10": {
            "source": _isolate_count(current_pred10, source),
            "entry": _isolate_count(current_pred10, entry),
            "source_exc": _isolate_count(current_pred10, source, exceptional_source),
            "entry_exc": _isolate_count(current_pred10, entry, exceptional_entry),
        },
    }

    source_edge_pairs = [(current_full24[idx], current_full24[step_by_dir[2][idx]]) for idx in range(len(coords))]
    source_edge_birth = {
        "source": _isolate_count(source_edge_pairs, source),
        "source_exc": _isolate_count(source_edge_pairs, source, exceptional_source),
    }

    representative_traces = {}
    lag_rows = {1: {}, 2: {}}
    active_family_sets: Dict[int, set[Tuple[int, int, int, int]]] = {}
    regular_trigger_hits = 0
    regular_trigger_prehits = 0
    exceptional_trigger_hits = 0
    exceptional_trigger_prehits = 0
    trigger_formula_regular = (m - 1, m - 2, 1)
    trigger_formula_exceptional = (m - 2, m - 1, 1)

    for source_u in range(1, m):
        source_index = next(idx for idx in source if int(coords[idx][4]) == source_u)
        trace = clar036._trace_source(prepared, row, source_index, hole_l1)["trace"]
        representative_traces[str(source_u)] = trace
        qwu_layer_set = {
            (
                int(row_data["coords"]["q"]),
                int(row_data["coords"]["w"]),
                int(row_data["coords"]["u"]),
                int(row_data["coords"]["layer"]),
            )
            for row_data in trace
        }
        active_family_sets[source_u] = qwu_layer_set
        trigger_hits = sum(
            1
            for row_data in trace
            if (
                int(row_data["coords"]["q"]),
                int(row_data["coords"]["w"]),
                int(row_data["coords"]["layer"]),
            )
            == (trigger_formula_exceptional if source_u == REPRESENTATIVE_EXCEPTIONAL_U else trigger_formula_regular)
        )
        trigger_prehits = sum(
            1
            for row_data in trace[:-1]
            if (
                int(row_data["coords"]["q"]),
                int(row_data["coords"]["w"]),
                int(row_data["coords"]["layer"]),
            )
            == (trigger_formula_exceptional if source_u == REPRESENTATIVE_EXCEPTIONAL_U else trigger_formula_regular)
        )
        if source_u == REPRESENTATIVE_EXCEPTIONAL_U:
            exceptional_trigger_hits = trigger_hits
            exceptional_trigger_prehits = trigger_prehits
        else:
            regular_trigger_hits += trigger_hits
            regular_trigger_prehits += trigger_prehits

        for lag in (1, 2):
            rows_lag = []
            for idx in range(lag, len(trace)):
                prev_payload = trace[idx - lag]["coords"]
                cur_payload = trace[idx]["coords"]
                prev_coords = (
                    int(prev_payload["x0"]),
                    int(prev_payload["q"]),
                    int(prev_payload["w"]),
                    int(prev_payload["v"]),
                    int(prev_payload["u"]),
                )
                cur_coords = (
                    int(cur_payload["x0"]),
                    int(cur_payload["q"]),
                    int(cur_payload["w"]),
                    int(cur_payload["v"]),
                    int(cur_payload["u"]),
                )
                rows_lag.append((_simple_full24_row(prev_coords, 0, m), _simple_full24_row(cur_coords, 0, m)))
            lag_rows[lag][source_u] = rows_lag

    lag_target_visibility = {}
    for lag in (1, 2):
        regular_multiplicities = [rows[-1:] and rows.count(rows[-1]) or 0 for source_u, rows in lag_rows[lag].items() if source_u != REPRESENTATIVE_EXCEPTIONAL_U]
        exceptional_rows = lag_rows[lag][REPRESENTATIVE_EXCEPTIONAL_U]
        lag_target_visibility[f"lag{lag}"] = {
            "regular_target_max_final_multiplicity": int(max(regular_multiplicities)),
            "regular_target_all_unique": bool(all(value == 1 for value in regular_multiplicities)),
            "exceptional_target_final_multiplicity": int(exceptional_rows.count(exceptional_rows[-1])),
            "exceptional_target_unique": bool(exceptional_rows.count(exceptional_rows[-1]) == 1),
        }

    active_disjointness = _pairwise_overlap_matrix(active_family_sets)

    return {
        "m": int(m),
        "raw_carrier_spec": {
            "states": ["off", "active_reg", "active_exc"],
            "birth": {
                "source_formula": "layer=1, q=m-1, w=0, u!=0",
                "regular_birth": "layer=1, q=m-1, w=0, u!=0,3 -> take alt-2 -> active_reg",
                "exceptional_birth": "layer=1, q=m-1, w=0, u=3 -> take alt-2 -> active_exc",
            },
            "fire": {
                "regular_target_qwl": [m - 1, m - 2, 1],
                "regular_exit_dir": [2],
                "exceptional_target_qwl": [m - 2, m - 1, 1],
                "exceptional_exit_dir": [1],
            },
            "reduced_observation": "on traced active states, current (q,w,u,layer) already determines source family exactly",
        },
        "simple_full_row_nogo": full_row_nogo,
        "simple_richer_family_results": {
            "source_edge_alt2_pair_full24": source_edge_birth,
            "temporal_lag_target_visibility": lag_target_visibility,
        },
        "raw_current_coordinate_results": {
            "source_formula_exact": bool(all(_matches_source_formula(_coords_payload(prepared, idx), m) == (idx in source) for idx in range(len(coords)))),
            "entry_formula_exact": bool(all(_matches_entry_formula(_coords_payload(prepared, idx), m) == (idx in entry) for idx in range(len(coords)))),
            "active_family_qwu_layer_pairwise_disjoint": bool(active_disjointness["max_pairwise_overlap"] == 0),
            "active_family_pairwise_overlap": active_disjointness,
            "regular_target_qwl_hits_across_all_regular_traces": int(regular_trigger_hits),
            "regular_target_qwl_prehits_across_all_regular_traces": int(regular_trigger_prehits),
            "exceptional_target_qwl_hits": int(exceptional_trigger_hits),
            "exceptional_target_qwl_prehits": int(exceptional_trigger_prehits),
        },
    }


def _analysis_summary(started: float, per_m: Mapping[str, object]) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "main_result": (
            "The simple 038 neighborhood alphabet remains the wrong realization family even "
            "after richer point-derived source-edge and lag-1/lag-2 lifts. The fixed raw "
            "carrier logic from 037/039 is already exact on current coordinates, and on "
            "traced active states current (q,w,u,layer) already separates the source families. "
            "So the remaining gap is not controller logic discovery. It is exposure / "
            "admissibility of coordinate-level observables."
        ),
        "per_m": {
            m: {
                "source_full24_isolates": payload["simple_full_row_nogo"]["full24"]["source"]["isolates"],
                "entry_full24_isolates": payload["simple_full_row_nogo"]["full24"]["entry"]["isolates"],
                "source_edge_pair_isolates_source": payload["simple_richer_family_results"]["source_edge_alt2_pair_full24"]["source"]["isolates"],
                "lag1_regular_target_all_unique": payload["simple_richer_family_results"]["temporal_lag_target_visibility"]["lag1"]["regular_target_all_unique"],
                "lag1_exceptional_target_unique": payload["simple_richer_family_results"]["temporal_lag_target_visibility"]["lag1"]["exceptional_target_unique"],
                "lag2_regular_target_all_unique": payload["simple_richer_family_results"]["temporal_lag_target_visibility"]["lag2"]["regular_target_all_unique"],
                "lag2_exceptional_target_unique": payload["simple_richer_family_results"]["temporal_lag_target_visibility"]["lag2"]["exceptional_target_unique"],
                "active_family_qwu_layer_pairwise_disjoint": payload["raw_current_coordinate_results"]["active_family_qwu_layer_pairwise_disjoint"],
                "regular_target_qwl_prehits": payload["raw_current_coordinate_results"]["regular_target_qwl_prehits_across_all_regular_traces"],
                "exceptional_target_qwl_prehits": payload["raw_current_coordinate_results"]["exceptional_target_qwl_prehits"],
            }
            for m, payload in per_m.items()
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the first richer observable families for the fixed D5 raw carrier.")
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
        out_dir / "raw_carrier_transducer_spec.json",
        {m: payload["raw_carrier_spec"] for m, payload in per_m.items()},
    )
    _write_json(
        out_dir / "simple_alphabet_full_row_nogo_040.json",
        {m: payload["simple_full_row_nogo"] for m, payload in per_m.items()},
    )
    _write_json(
        out_dir / "active_target_visibility_simple_alphabet_040.json",
        {
            m: payload["simple_richer_family_results"]["temporal_lag_target_visibility"]
            for m, payload in per_m.items()
        },
    )
    _write_json(
        out_dir / "richer_observable_catalog_040.json",
        {
            "families": [
                {
                    "name": "simple_current_full24",
                    "description": "Current 24-bit simple row from the 038 alphabet.",
                },
                {
                    "name": "simple_source_edge_alt2_pair_full24",
                    "description": "Ordered pair of current 24-bit row and alt-2 successor 24-bit row.",
                },
                {
                    "name": "simple_temporal_lag1_pair_full24",
                    "description": "Ordered pair of previous and current 24-bit rows along the active corridor.",
                },
                {
                    "name": "simple_temporal_lag2_pair_full24",
                    "description": "Ordered pair of lag-2 previous and current 24-bit rows along the active corridor.",
                },
                {
                    "name": "raw_current_qwu_layer",
                    "description": "Coordinate-level current observable (q,w,u,layer) on traced active states.",
                },
                {
                    "name": "active_plus_raw_qwl",
                    "description": "Active-conditioned target trigger on current (q,w,layer).",
                },
            ],
            "per_m": {
                m: {
                    "simple_source_edge_alt2_pair_full24": payload["simple_richer_family_results"]["source_edge_alt2_pair_full24"],
                    "simple_temporal_lag_visibility": payload["simple_richer_family_results"]["temporal_lag_target_visibility"],
                    "raw_current_coordinate_results": payload["raw_current_coordinate_results"],
                }
                for m, payload in per_m.items()
            },
        },
    )
    _write_json(
        out_dir / "realization_search_summary.json",
        {
            "verdict": (
                "No family built only from the simple 038 row survives as the next realization alphabet, "
                "even after source-edge and lag-1/lag-2 lifts. The first surviving realization is the "
                "coordinate-level raw current family, which already makes birth, family separation on active "
                "traces, and active-conditioned target firing exact on checked moduli. The remaining gap is "
                "admissibility / exposure of those coordinate-level observables."
            ),
            "per_m": {
                m: {
                    "simple_source_edge_pair_source_isolates": payload["simple_richer_family_results"]["source_edge_alt2_pair_full24"]["source"]["isolates"],
                    "simple_source_edge_pair_source_exc_isolates": payload["simple_richer_family_results"]["source_edge_alt2_pair_full24"]["source_exc"]["isolates"],
                    "simple_lag1_exc_target_unique": payload["simple_richer_family_results"]["temporal_lag_target_visibility"]["lag1"]["exceptional_target_unique"],
                    "simple_lag2_exc_target_unique": payload["simple_richer_family_results"]["temporal_lag_target_visibility"]["lag2"]["exceptional_target_unique"],
                    "raw_current_birth_exact": payload["raw_current_coordinate_results"]["source_formula_exact"],
                    "raw_current_family_disjoint": payload["raw_current_coordinate_results"]["active_family_qwu_layer_pairwise_disjoint"],
                    "raw_current_regular_target_prehits": payload["raw_current_coordinate_results"]["regular_target_qwl_prehits_across_all_regular_traces"],
                    "raw_current_exceptional_target_prehits": payload["raw_current_coordinate_results"]["exceptional_target_qwl_prehits"],
                }
                for m, payload in per_m.items()
            },
            "next_gap": "coordinate exposure / admissibility, not controller logic",
        },
    )
    _write_json(args.summary_out, summary)


if __name__ == "__main__":
    main()
