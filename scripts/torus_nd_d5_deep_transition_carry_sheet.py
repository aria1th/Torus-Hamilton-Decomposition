#!/usr/bin/env python3
"""Extract the minimal future grouped-transition sheet realizing the D5 carry bit."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_corridor_phase_extraction as phase034
import torus_nd_d5_endpoint_latin_repair as seed032
from torus_nd_d5_carry_admissibility_search import (
    ALL_M_VALUES,
    REPRESENTATIVE_EXCEPTIONAL_U,
)
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-DEEP-TRANSITION-CARRY-SHEET-046"
FLAT_DN = (0, 0, 0, 1)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _build_active_data(m: int) -> Dict[str, object]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    nexts_all, meta = phase034._build_best_seed(prepared)
    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    coords = prepared.pre["coords"]
    step_by_dir = prepared.pre["step_by_dir"]
    hole_l1 = phase034._hole_l1_set(prepared, row)

    row_orbit: Dict[int, Dict[str, object]] = {}
    for state_index in range(len(coords)):
        q_value, w_value, v_value, u_value = [int(value) for value in coords[state_index][1:5]]
        layer = int(coords[state_index][0])
        s_value = (w_value + u_value) % m

        next_state_index = int(row[state_index])
        q_next, w_next, v_next, u_next = [int(value) for value in coords[next_state_index][1:5]]
        layer_next = int(coords[next_state_index][0])
        s_next = (w_next + u_next) % m

        row_orbit[state_index] = {
            "state_index": int(state_index),
            "next_state_index": int(next_state_index),
            "B_base": (int(s_value), int(u_value), int(v_value), int(layer)),
            "dn": (
                int((s_next - s_value) % m),
                int((u_next - u_value) % m),
                int((v_next - v_value) % m),
                int((layer_next - layer) % m),
            ),
            "c": int(q_value == m - 1),
            "q": int(q_value),
            "w": int(w_value),
            "u": int(u_value),
            "v": int(v_value),
            "layer": int(layer),
            "label": str(labels[state_index]),
        }

    active_rows: List[Dict[str, object]] = []
    seen_states = set()
    for source_u in range(1, m):
        source_index = next(
            idx
            for idx, label in enumerate(labels)
            if label == "R1" and int(coords[idx][4]) == source_u
        )
        family = "exceptional" if source_u == REPRESENTATIVE_EXCEPTIONAL_U else "regular"
        current = int(step_by_dir[2][source_index])
        trace_step = 0
        while current not in seen_states:
            seen_states.add(current)
            base = row_orbit[current]
            exit_dirs = [
                int(direction)
                for direction in range(5)
                if step_by_dir[direction][current] in hole_l1
            ]
            active_rows.append(
                {
                    "m": int(m),
                    "source_u": int(source_u),
                    "trace_step": int(trace_step),
                    "family": family,
                    "state_index": int(current),
                    "B": tuple(base["B_base"]) + (family,),
                    "dn": tuple(base["dn"]),
                    "c": int(base["c"]),
                    "q": int(base["q"]),
                    "w": int(base["w"]),
                    "u": int(base["u"]),
                    "v": int(base["v"]),
                    "layer": int(base["layer"]),
                    "label": str(base["label"]),
                    "exit_dirs": exit_dirs,
                }
            )
            trace_step += 1
            if exit_dirs:
                break
            current = int(row[current])

    return {
        "m": int(m),
        "active_rows": active_rows,
        "row_orbit": row_orbit,
    }


def _future_dn_window(
    row: Mapping[str, object],
    row_orbit: Mapping[int, Mapping[str, object]],
    horizon: int,
) -> Tuple[Tuple[int, int, int, int], ...]:
    state_index = int(row["state_index"])
    out = []
    for _ in range(horizon):
        out.append(tuple(int(value) for value in row_orbit[state_index]["dn"]))
        state_index = int(row_orbit[state_index]["next_state_index"])
    return tuple(out)


def _future_B_window(
    row: Mapping[str, object],
    row_orbit: Mapping[int, Mapping[str, object]],
    horizon: int,
) -> Tuple[Tuple[object, ...], ...]:
    family = str(row["family"])
    state_index = int(row["state_index"])
    out: List[Tuple[object, ...]] = []
    for _ in range(horizon):
        base = tuple(row_orbit[state_index]["B_base"])
        out.append(base + (family,))
        state_index = int(row_orbit[state_index]["next_state_index"])
    return tuple(out)


def _initial_flat_signature(
    row: Mapping[str, object],
    row_orbit: Mapping[int, Mapping[str, object]],
) -> Dict[str, object]:
    state_index = int(row["state_index"])
    flat_run_length = 0
    while tuple(int(value) for value in row_orbit[state_index]["dn"]) == FLAT_DN:
        flat_run_length += 1
        state_index = int(row_orbit[state_index]["next_state_index"])
    first_nonflat_dn = tuple(int(value) for value in row_orbit[state_index]["dn"])
    return {
        "flat_run_length": int(flat_run_length),
        "first_nonflat_dn": first_nonflat_dn,
    }


def _collision_summary(
    rows: Sequence[Mapping[str, object]],
    key_getter,
) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        buckets[key_getter(row)].append(row)

    collision_buckets = []
    false_pos = 0
    false_neg = 0
    for key, bucket in buckets.items():
        counts = Counter(int(row["c"]) for row in bucket)
        if len(counts) > 1:
            collision_buckets.append((key, bucket))
        predicted = 1 if counts[1] > counts[0] else 0
        for row in bucket:
            actual = int(row["c"])
            if actual != predicted:
                if predicted == 1:
                    false_pos += 1
                else:
                    false_neg += 1

    return {
        "distinct_key_count": int(len(buckets)),
        "collision_bucket_count": int(len(collision_buckets)),
        "ambiguous_row_count": int(sum(len(bucket) for _, bucket in collision_buckets)),
        "false_pos": int(false_pos),
        "false_neg": int(false_neg),
        "total_errors": int(false_pos + false_neg),
        "is_exact": bool(len(collision_buckets) == 0),
        "collision_buckets": collision_buckets,
    }


def _represent_row(row: Mapping[str, object], extra: Mapping[str, object]) -> Dict[str, object]:
    out = {
        "m": int(row["m"]),
        "source_u": int(row["source_u"]),
        "trace_step": int(row["trace_step"]),
        "family": str(row["family"]),
        "state_index": int(row["state_index"]),
        "B": list(row["B"]),
        "dn": list(row["dn"]),
        "c": int(row["c"]),
        "q": int(row["q"]),
        "w": int(row["w"]),
        "u": int(row["u"]),
        "v": int(row["v"]),
        "layer": int(row["layer"]),
        "label": str(row["label"]),
    }
    out.update(extra)
    return out


def _support_profile(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    family_counts = Counter(str(row["family"]) for row in rows)
    carry_counts = Counter(int(row["c"]) for row in rows)
    label_counts = Counter(str(row["label"]) for row in rows)
    layer_counts = Counter(int(row["layer"]) for row in rows)
    return {
        "row_count": int(len(rows)),
        "family_counts": {str(key): int(value) for key, value in sorted(family_counts.items())},
        "carry_counts": {str(key): int(value) for key, value in sorted(carry_counts.items())},
        "layer_counts": {str(key): int(value) for key, value in sorted(layer_counts.items())},
        "label_counts": {str(key): int(value) for key, value in sorted(label_counts.items())},
    }


def _analysis_summary(
    started: float,
    horizon_summary: Mapping[str, object],
    signature_summary: Mapping[str, object],
) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "main_result": (
            "The carry sheet is already an exact future-transition event on the checked active grouped base. "
            "The minimal exact future grouped-delta horizon is m-3 on m=5,7,9,11, while the minimal exact future grouped-state horizon is m-2. "
            "Moreover, the exact future window compresses to the current grouped state B together with the initial flat-run length where dn=(0,0,0,1) "
            "and the first nonflat dn after that run. So after 045, the next admissibility target is not an amorphous broader gauge: it is coding this "
            "first exact future grouped-transition event."
        ),
        "minimal_horizon_pattern": horizon_summary,
        "signature_summary": signature_summary,
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the minimal future grouped-transition sheet realizing the D5 carry bit.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    frozen_dataset = {}
    horizon_exactness_summary = {"dn": {}, "B": {}}
    minimal_future_horizons = {}
    failure_at_H_minus_1 = {"dn": {}, "B": {}}
    success_at_H = {"dn": {}, "B": {}}
    representative_ambiguous_states = {"dn": {}, "B": {}}
    representative_exact_states = {"dn": {}, "B": {}}
    first_nonflat_signature_summary = {}

    dn_horizons = []
    B_horizons = []

    for m in ALL_M_VALUES:
        payload = _build_active_data(m)
        active_rows = payload["active_rows"]
        row_orbit = payload["row_orbit"]
        frozen_dataset[str(m)] = active_rows

        dn_tables = []
        B_tables = []
        minimal_dn_horizon = None
        minimal_B_horizon = None
        exact_dn_rows = []
        exact_B_rows = []

        for horizon in range(1, m + 1):
            dn_summary = _collision_summary(
                active_rows,
                lambda row, horizon=horizon: (row["B"], _future_dn_window(row, row_orbit, horizon)),
            )
            dn_tables.append(
                {
                    "horizon": int(horizon),
                    **{
                        key: value
                        for key, value in dn_summary.items()
                        if key != "collision_buckets"
                    },
                }
            )
            if minimal_dn_horizon is None and dn_summary["is_exact"]:
                minimal_dn_horizon = int(horizon)
                exact_dn_rows = [
                    _represent_row(
                        row,
                        {
                            "future_dn_window": [list(item) for item in _future_dn_window(row, row_orbit, horizon)],
                        },
                    )
                    for row in active_rows[: min(6, len(active_rows))]
                ]

            B_summary = _collision_summary(
                active_rows,
                lambda row, horizon=horizon: (row["B"], _future_B_window(row, row_orbit, horizon)),
            )
            B_tables.append(
                {
                    "horizon": int(horizon),
                    **{
                        key: value
                        for key, value in B_summary.items()
                        if key != "collision_buckets"
                    },
                }
            )
            if minimal_B_horizon is None and B_summary["is_exact"]:
                minimal_B_horizon = int(horizon)
                exact_B_rows = [
                    _represent_row(
                        row,
                        {
                            "future_B_window": [list(item) for item in _future_B_window(row, row_orbit, horizon)],
                        },
                    )
                    for row in active_rows[: min(6, len(active_rows))]
                ]

        assert minimal_dn_horizon is not None
        assert minimal_B_horizon is not None

        dn_horizons.append(int(minimal_dn_horizon))
        B_horizons.append(int(minimal_B_horizon))

        minimal_future_horizons[str(m)] = {
            "minimal_exact_future_dn_horizon": int(minimal_dn_horizon),
            "minimal_exact_future_B_horizon": int(minimal_B_horizon),
            "matches_m_minus_3": bool(minimal_dn_horizon == m - 3),
            "matches_m_minus_2": bool(minimal_B_horizon == m - 2),
        }

        horizon_exactness_summary["dn"][str(m)] = dn_tables
        horizon_exactness_summary["B"][str(m)] = B_tables

        dn_failure = next(item for item in dn_tables if item["horizon"] == minimal_dn_horizon - 1)
        B_failure = next(item for item in B_tables if item["horizon"] == minimal_B_horizon - 1)
        dn_success = next(item for item in dn_tables if item["horizon"] == minimal_dn_horizon)
        B_success = next(item for item in B_tables if item["horizon"] == minimal_B_horizon)

        failure_at_H_minus_1["dn"][str(m)] = dn_failure
        failure_at_H_minus_1["B"][str(m)] = B_failure
        success_at_H["dn"][str(m)] = dn_success
        success_at_H["B"][str(m)] = B_success
        representative_exact_states["dn"][str(m)] = exact_dn_rows
        representative_exact_states["B"][str(m)] = exact_B_rows

        dn_failure_detail = _collision_summary(
            active_rows,
            lambda row, horizon=minimal_dn_horizon - 1: (row["B"], _future_dn_window(row, row_orbit, horizon)),
        )
        B_failure_detail = _collision_summary(
            active_rows,
            lambda row, horizon=minimal_B_horizon - 1: (row["B"], _future_B_window(row, row_orbit, horizon)),
        )

        representative_ambiguous_states["dn"][str(m)] = []
        for _, bucket in dn_failure_detail["collision_buckets"][:3]:
            representative_ambiguous_states["dn"][str(m)].append(
                {
                    "support_profile": _support_profile(bucket),
                    "rows": [
                        _represent_row(
                            row,
                            {
                                "future_dn_window": [
                                    list(item)
                                    for item in _future_dn_window(row, row_orbit, minimal_dn_horizon - 1)
                                ],
                            },
                        )
                        for row in bucket[:4]
                    ],
                }
            )

        representative_ambiguous_states["B"][str(m)] = []
        for _, bucket in B_failure_detail["collision_buckets"][:3]:
            representative_ambiguous_states["B"][str(m)].append(
                {
                    "support_profile": _support_profile(bucket),
                    "rows": [
                        _represent_row(
                            row,
                            {
                                "future_B_window": [
                                    list(item)
                                    for item in _future_B_window(row, row_orbit, minimal_B_horizon - 1)
                                ],
                            },
                        )
                        for row in bucket[:4]
                    ],
                }
            )

        signature_exact = _collision_summary(
            active_rows,
            lambda row: (
                row["B"],
                _initial_flat_signature(row, row_orbit)["flat_run_length"],
                _initial_flat_signature(row, row_orbit)["first_nonflat_dn"],
            ),
        )
        length_only = _collision_summary(
            active_rows,
            lambda row: (row["B"], _initial_flat_signature(row, row_orbit)["flat_run_length"]),
        )

        ambiguous_dn_rows = [
            row
            for collision in representative_ambiguous_states["dn"][str(m)]
            for row in collision["rows"]
        ]
        first_nonflat_signature_summary[str(m)] = {
            "signature_is_exact": bool(signature_exact["is_exact"]),
            "flat_run_length_only_is_exact": bool(length_only["is_exact"]),
            "signature_collision_bucket_count": int(signature_exact["collision_bucket_count"]),
            "flat_run_length_only_collision_bucket_count": int(length_only["collision_bucket_count"]),
            "minimal_dn_horizon": int(minimal_dn_horizon),
            "minimal_B_horizon": int(minimal_B_horizon),
            "H_minus_1_ambiguity_is_regular_carry_B_only": bool(
                all(
                    row["family"] == "regular"
                    and int(row["c"]) in {0, 1}
                    and row["label"] == "B"
                    for row in ambiguous_dn_rows
                )
            ),
            "representative_exact_signature_rows": [
                _represent_row(
                    row,
                    _initial_flat_signature(row, row_orbit),
                )
                for row in active_rows[: min(6, len(active_rows))]
            ],
        }

    minimal_horizon_pattern = {
        "dn_horizons": {str(m): int(h) for m, h in zip(ALL_M_VALUES, dn_horizons)},
        "B_horizons": {str(m): int(h) for m, h in zip(ALL_M_VALUES, B_horizons)},
        "dn_matches_m_minus_3_on_checked_moduli": bool(all(h == m - 3 for m, h in zip(ALL_M_VALUES, dn_horizons))),
        "B_matches_m_minus_2_on_checked_moduli": bool(all(h == m - 2 for m, h in zip(ALL_M_VALUES, B_horizons))),
    }

    analysis_summary = _analysis_summary(started, minimal_horizon_pattern, first_nonflat_signature_summary)

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "frozen_active_carry_dataset_046.json", frozen_dataset)
    _write_json(out_dir / "horizon_exactness_summary.json", horizon_exactness_summary)
    _write_json(out_dir / "minimal_future_horizons.json", minimal_future_horizons)
    _write_json(out_dir / "first_nonflat_signature_summary.json", first_nonflat_signature_summary)
    _write_json(out_dir / "failure_at_H_minus_1_tables.json", failure_at_H_minus_1)
    _write_json(out_dir / "success_at_H_tables.json", success_at_H)
    _write_json(out_dir / "representative_ambiguous_states_H_minus_1.json", representative_ambiguous_states)
    _write_json(out_dir / "representative_exact_states_H.json", representative_exact_states)
    _write_json(args.summary_out, analysis_summary)

    print(f"task_id: {TASK_ID}")
    print("extracted the minimal future grouped-transition carry sheet on the checked D5 active branch.")


if __name__ == "__main__":
    main()
