#!/usr/bin/env python3
"""Prune and code the exact future-transition carry target on the checked D5 active branch."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Mapping, MutableMapping, Sequence, Tuple

import torus_nd_d5_deep_transition_carry_sheet as carry046
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-FUTURE-TRANSITION-CARRY-CODING-047"
FLAT_DN = tuple(carry046.FLAT_DN)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _event_class(dn: Sequence[int]) -> str:
    dn_tuple = tuple(int(value) for value in dn)
    if dn_tuple == FLAT_DN:
        return "flat"
    if dn_tuple == (0, 0, 0, 0):
        return "wrap"
    if dn_tuple == (1, 1, 0, 0):
        return "carry_jump"
    return "other"


def _build_augmented_data(m: int, horizon: int) -> Dict[str, object]:
    payload = carry046._build_active_data(m)
    row_orbit = payload["row_orbit"]
    augmented_rows: List[Dict[str, object]] = []

    for row in payload["active_rows"]:
        signature = carry046._initial_flat_signature(row, row_orbit)
        state_index = int(row["state_index"])
        state = state_index

        event_window: List[str] = []
        binary_window: List[int] = []
        for _ in range(horizon):
            dn = tuple(int(value) for value in row_orbit[state]["dn"])
            event_window.append(_event_class(dn))
            binary_window.append(int(dn == FLAT_DN))
            state = int(row_orbit[state]["next_state_index"])

        future_binary_after_current: List[int] = []
        state = int(row_orbit[state_index]["next_state_index"])
        for _ in range(horizon):
            dn = tuple(int(value) for value in row_orbit[state]["dn"])
            future_binary_after_current.append(int(dn == FLAT_DN))
            state = int(row_orbit[state]["next_state_index"])

        augmented_rows.append(
            {
                **row,
                "tau": int(signature["flat_run_length"]),
                "first_nonflat_dn": [int(value) for value in signature["first_nonflat_dn"]],
                "epsilon4": _event_class(row["dn"]),
                "event_window_max": event_window,
                "binary_window_max": binary_window,
                "future_binary_after_current_max": future_binary_after_current,
            }
        )

    return {
        "m": int(m),
        "augmented_rows": augmented_rows,
    }


def _represent_row(row: Mapping[str, object]) -> Dict[str, object]:
    return {
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
        "tau": int(row["tau"]),
        "epsilon4": str(row["epsilon4"]),
        "first_nonflat_dn": list(row["first_nonflat_dn"]),
    }


def _collision_summary(rows: Sequence[Mapping[str, object]], key_getter) -> Dict[str, object]:
    buckets: MutableMapping[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        buckets[key_getter(row)].append(row)

    collision_buckets = []
    ambiguous_row_count = 0
    for key, bucket in buckets.items():
        counts = Counter(int(row["c"]) for row in bucket)
        if len(counts) > 1:
            ambiguous_row_count += len(bucket)
            collision_buckets.append((key, bucket))

    return {
        "distinct_key_count": int(len(buckets)),
        "collision_bucket_count": int(len(collision_buckets)),
        "ambiguous_row_count": int(ambiguous_row_count),
        "is_exact": bool(len(collision_buckets) == 0),
        "collision_buckets": collision_buckets,
    }


def _summary_without_buckets(payload: Mapping[str, object]) -> Dict[str, object]:
    return {
        key: value
        for key, value in payload.items()
        if key != "collision_buckets"
    }


def _sample_collision_rows(
    summary: Mapping[str, object],
    limit_buckets: int = 3,
    limit_rows: int = 4,
) -> List[Dict[str, object]]:
    out = []
    for key, bucket in summary["collision_buckets"][:limit_buckets]:
        out.append(
            {
                "key": _jsonable_key(key),
                "rows": [_represent_row(row) for row in bucket[:limit_rows]],
            }
        )
    return out


def _jsonable_key(key: Tuple[object, ...]) -> List[object]:
    out: List[object] = []
    for value in key:
        if isinstance(value, tuple):
            out.append(_jsonable_key(value))
        else:
            out.append(value)
    return out


def _event_partition_label(row: Mapping[str, object], partition: Mapping[str, str]) -> str:
    epsilon = str(row["epsilon4"])
    if epsilon == "flat":
        return "flat"
    return str(partition[epsilon])


def _partition_catalog() -> List[Dict[str, object]]:
    return [
        {
            "name": "flat+wrap/carry_jump/other",
            "partition": {
                "wrap": "wrap",
                "carry_jump": "carry_jump",
                "other": "other",
            },
        },
        {
            "name": "flat+(wrap,carry_jump)/other",
            "partition": {
                "wrap": "nonflat_a",
                "carry_jump": "nonflat_a",
                "other": "nonflat_b",
            },
        },
        {
            "name": "flat+(wrap,other)/carry_jump",
            "partition": {
                "wrap": "nonflat_a",
                "carry_jump": "nonflat_b",
                "other": "nonflat_a",
            },
        },
        {
            "name": "flat+wrap/(carry_jump,other)",
            "partition": {
                "wrap": "nonflat_a",
                "carry_jump": "nonflat_b",
                "other": "nonflat_b",
            },
        },
        {
            "name": "flat+all_nonflat_merged",
            "partition": {
                "wrap": "nonflat",
                "carry_jump": "nonflat",
                "other": "nonflat",
            },
        },
    ]


def _interval_partition_from_mask(max_tau: int, mask: int) -> Dict[int, int]:
    block = 0
    out = {0: 0}
    for tau in range(1, max_tau + 1):
        if mask & (1 << (tau - 1)):
            block += 1
        out[tau] = block
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Prune and code the exact future-transition carry target on the checked D5 active branch.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    max_horizon = 10
    data_by_m = {
        int(m): _build_augmented_data(int(m), max_horizon)
        for m in carry046.ALL_M_VALUES
    }
    rows_by_m = {
        int(m): payload["augmented_rows"]
        for m, payload in data_by_m.items()
    }
    max_tau = max(int(row["tau"]) for rows in rows_by_m.values() for row in rows)

    frozen_dataset = {
        str(m): rows
        for m, rows in rows_by_m.items()
    }

    quotient_exactness_summary: Dict[str, object] = {}
    representative_ambiguous_rows: Dict[str, object] = {}
    representative_exact_rows: Dict[str, object] = {}

    b_tau_boundary = {}
    for m, rows in rows_by_m.items():
        b_tau = _collision_summary(rows, lambda row: (tuple(row["B"]), int(row["tau"])))
        b_tau_tau_gt_0 = _collision_summary(
            [row for row in rows if int(row["tau"]) > 0],
            lambda row: (tuple(row["B"]), int(row["tau"])),
        )
        b_tau_epsilon = _collision_summary(
            rows,
            lambda row: (tuple(row["B"]), int(row["tau"]), str(row["epsilon4"])),
        )
        tau_zero_collision_buckets = 0
        tau_positive_collision_buckets = 0
        for key, _bucket in b_tau["collision_buckets"]:
            if int(key[1]) == 0:
                tau_zero_collision_buckets += 1
            else:
                tau_positive_collision_buckets += 1
        b_tau_boundary[str(m)] = {
            "B_plus_tau": _summary_without_buckets(b_tau),
            "B_plus_tau_tau_gt_0": _summary_without_buckets(b_tau_tau_gt_0),
            "B_plus_tau_plus_epsilon4": _summary_without_buckets(b_tau_epsilon),
            "B_plus_tau_collision_buckets_tau_eq_0": int(tau_zero_collision_buckets),
            "B_plus_tau_collision_buckets_tau_gt_0": int(tau_positive_collision_buckets),
        }
    quotient_exactness_summary["B_tau_boundary"] = b_tau_boundary

    boundary_partition_rows = []
    for entry in _partition_catalog():
        partition = entry["partition"]
        exact_all = True
        per_m = {}
        for m, rows in rows_by_m.items():
            summary = _collision_summary(
                rows,
                lambda row, partition=partition: (
                    tuple(row["B"]),
                    int(row["tau"]),
                    _event_partition_label(row, partition),
                ),
            )
            per_m[str(m)] = _summary_without_buckets(summary)
            exact_all = exact_all and bool(summary["is_exact"])
        boundary_partition_rows.append(
            {
                "name": entry["name"],
                "partition": entry["partition"],
                "exact_on_checked_moduli": bool(exact_all),
                "per_m": per_m,
            }
        )
    exact_boundary_partitions = [
        row
        for row in boundary_partition_rows
        if row["exact_on_checked_moduli"]
    ]
    quotient_exactness_summary["boundary_partition_search"] = {
        "rows": boundary_partition_rows,
        "exact_partition_count": int(len(exact_boundary_partitions)),
        "minimal_nonflat_class_count": int(
            min(
                len(set(row["partition"].values()))
                for row in exact_boundary_partitions
            )
        ),
        "exact_partition_names": [row["name"] for row in exact_boundary_partitions],
    }

    truncation_rows = []
    for horizon in range(0, max_tau + 1):
        exact_all = True
        per_m = {}
        for m, rows in rows_by_m.items():
            summary = _collision_summary(
                rows,
                lambda row, horizon=horizon: (
                    tuple(row["B"]),
                    int(min(int(row["tau"]), horizon)),
                    str(row["epsilon4"]),
                ),
            )
            per_m[str(m)] = _summary_without_buckets(summary)
            exact_all = exact_all and bool(summary["is_exact"])
        truncation_rows.append(
            {
                "horizon": int(horizon),
                "exact_on_checked_moduli": bool(exact_all),
                "per_m": per_m,
            }
        )
    minimal_exact_truncation = next(
        row["horizon"]
        for row in truncation_rows
        if row["exact_on_checked_moduli"]
    )
    quotient_exactness_summary["tau_truncation_search"] = {
        "rows": truncation_rows,
        "minimal_exact_horizon": int(minimal_exact_truncation),
    }

    threshold_rows = []
    for horizon in range(0, max_tau + 1):
        exact_all = True
        per_m = {}
        for m, rows in rows_by_m.items():
            summary = _collision_summary(
                rows,
                lambda row, horizon=horizon: (
                    tuple(row["B"]),
                    tuple(int(int(row["tau"]) >= level) for level in range(1, horizon + 1)),
                    str(row["epsilon4"]),
                ),
            )
            per_m[str(m)] = _summary_without_buckets(summary)
            exact_all = exact_all and bool(summary["is_exact"])
        threshold_rows.append(
            {
                "horizon": int(horizon),
                "exact_on_checked_moduli": bool(exact_all),
                "per_m": per_m,
            }
        )
    minimal_exact_threshold = next(
        row["horizon"]
        for row in threshold_rows
        if row["exact_on_checked_moduli"]
    )
    quotient_exactness_summary["tau_threshold_bit_search"] = {
        "rows": threshold_rows,
        "minimal_exact_horizon": int(minimal_exact_threshold),
    }

    interval_exact_rows = []
    best_interval_block_count = None
    for mask in range(1 << max_tau):
        partition = _interval_partition_from_mask(max_tau, mask)
        exact_all = True
        for m, rows in rows_by_m.items():
            summary = _collision_summary(
                rows,
                lambda row, partition=partition: (
                    tuple(row["B"]),
                    int(partition[int(row["tau"])]),
                    str(row["epsilon4"]),
                ),
            )
            if not summary["is_exact"]:
                exact_all = False
                break
        if exact_all:
            block_count = max(partition.values()) + 1
            record = {
                "mask": int(mask),
                "block_count": int(block_count),
                "partition": {
                    str(key): int(value)
                    for key, value in partition.items()
                },
            }
            interval_exact_rows.append(record)
            if best_interval_block_count is None or block_count < best_interval_block_count:
                best_interval_block_count = int(block_count)
    minimal_interval_partitions = [
        row
        for row in interval_exact_rows
        if row["block_count"] == best_interval_block_count
    ]
    quotient_exactness_summary["tau_interval_partition_search"] = {
        "max_tau": int(max_tau),
        "exact_partition_count": int(len(interval_exact_rows)),
        "minimal_exact_block_count": int(best_interval_block_count),
        "minimal_exact_partitions": minimal_interval_partitions,
    }

    transition_rows_eps4_window = []
    transition_rows_binary_window = []
    transition_rows_current_eps_future_binary = []
    for horizon in range(1, max_horizon + 1):
        exact_eps4_all = True
        exact_binary_all = True
        exact_current_eps_all = True
        per_m_eps4 = {}
        per_m_binary = {}
        per_m_current_eps = {}
        for m, rows in rows_by_m.items():
            eps4_summary = _collision_summary(
                rows,
                lambda row, horizon=horizon: (
                    tuple(row["B"]),
                    tuple(row["event_window_max"][:horizon]),
                ),
            )
            binary_summary = _collision_summary(
                rows,
                lambda row, horizon=horizon: (
                    tuple(row["B"]),
                    tuple(int(value) for value in row["binary_window_max"][:horizon]),
                ),
            )
            current_eps_future_binary_summary = _collision_summary(
                rows,
                lambda row, horizon=horizon: (
                    tuple(row["B"]),
                    str(row["epsilon4"]),
                    tuple(int(value) for value in row["future_binary_after_current_max"][:horizon]),
                ),
            )
            per_m_eps4[str(m)] = _summary_without_buckets(eps4_summary)
            per_m_binary[str(m)] = _summary_without_buckets(binary_summary)
            per_m_current_eps[str(m)] = _summary_without_buckets(current_eps_future_binary_summary)
            exact_eps4_all = exact_eps4_all and bool(eps4_summary["is_exact"])
            exact_binary_all = exact_binary_all and bool(binary_summary["is_exact"])
            exact_current_eps_all = exact_current_eps_all and bool(current_eps_future_binary_summary["is_exact"])

        transition_rows_eps4_window.append(
            {
                "horizon": int(horizon),
                "exact_on_checked_moduli": bool(exact_eps4_all),
                "per_m": per_m_eps4,
            }
        )
        transition_rows_binary_window.append(
            {
                "horizon": int(horizon),
                "exact_on_checked_moduli": bool(exact_binary_all),
                "per_m": per_m_binary,
            }
        )
        transition_rows_current_eps_future_binary.append(
            {
                "horizon": int(horizon),
                "exact_on_checked_moduli": bool(exact_current_eps_all),
                "per_m": per_m_current_eps,
            }
        )

    minimal_eps4_window_horizon = next(
        row["horizon"]
        for row in transition_rows_eps4_window
        if row["exact_on_checked_moduli"]
    )
    minimal_binary_window_horizon = next(
        row["horizon"]
        for row in transition_rows_binary_window
        if row["exact_on_checked_moduli"]
    )
    minimal_current_eps_future_binary_horizon = next(
        row["horizon"]
        for row in transition_rows_current_eps_future_binary
        if row["exact_on_checked_moduli"]
    )

    transition_sheet_search = {
        "eps4_window": {
            "rows": transition_rows_eps4_window,
            "minimal_exact_horizon": int(minimal_eps4_window_horizon),
        },
        "binary_window": {
            "rows": transition_rows_binary_window,
            "minimal_exact_horizon": int(minimal_binary_window_horizon),
        },
        "current_eps4_plus_future_binary_after_current": {
            "rows": transition_rows_current_eps_future_binary,
            "minimal_exact_horizon": int(minimal_current_eps_future_binary_horizon),
        },
    }

    ambiguous_truncation = _collision_summary(
        rows_by_m[11],
        lambda row: (
            tuple(row["B"]),
            int(min(int(row["tau"]), minimal_exact_truncation - 1)),
            str(row["epsilon4"]),
        ),
    )
    ambiguous_current_eps_future_binary = _collision_summary(
        rows_by_m[11],
        lambda row: (
            tuple(row["B"]),
            str(row["epsilon4"]),
            tuple(int(value) for value in row["future_binary_after_current_max"][: minimal_current_eps_future_binary_horizon - 1]),
        ),
    )
    ambiguous_eps4_window = _collision_summary(
        rows_by_m[11],
        lambda row: (
            tuple(row["B"]),
            tuple(row["event_window_max"][: minimal_eps4_window_horizon - 1]),
        ),
    )
    ambiguous_binary_window = _collision_summary(
        rows_by_m[11],
        lambda row: (
            tuple(row["B"]),
            tuple(int(value) for value in row["binary_window_max"][: minimal_binary_window_horizon - 1]),
        ),
    )
    representative_ambiguous_rows["m11"] = {
        "tau_truncation_H_minus_1": _sample_collision_rows(ambiguous_truncation),
        "current_eps4_plus_future_binary_after_current_H_minus_1": _sample_collision_rows(ambiguous_current_eps_future_binary),
        "eps4_window_H_minus_1": _sample_collision_rows(ambiguous_eps4_window),
        "binary_window_H_minus_1": _sample_collision_rows(ambiguous_binary_window),
    }

    representative_exact_rows["m11"] = {
        "tau_truncation_H": [
            _represent_row(row)
            for row in rows_by_m[11][:6]
        ],
        "current_eps4_plus_future_binary_after_current_H": [
            {
                **_represent_row(row),
                "future_binary_after_current_window": list(
                    row["future_binary_after_current_max"][:minimal_current_eps_future_binary_horizon]
                ),
            }
            for row in rows_by_m[11][:6]
        ],
        "eps4_window_H": [
            {
                **_represent_row(row),
                "eps4_window": list(row["event_window_max"][:minimal_eps4_window_horizon]),
            }
            for row in rows_by_m[11][:6]
        ],
    }

    quotient_exactness_summary["transition_sheet_search"] = transition_sheet_search

    analysis_summary = {
        "task_id": TASK_ID,
        "main_result": (
            "The 046 carry target sharpens further on the checked active branch. "
            "The boundary event class is genuinely 3-class minimal at tau=0, and the first exact checked-range quotient is "
            "current B together with min(tau,8) and the current grouped-delta event class. "
            "Equivalently, the first exact transition-sheet coding found here is current B plus the current 4-class grouped-delta event "
            "and the next 7 future flat/nonflat indicators after the current step. "
            "No smaller tau truncation or threshold-bit quotient survives on m=5,7,9,11, while pure future binary windows need to be longer. "
            "So the live hidden datum is tau itself up to the checked-range top cap, with epsilon as a secondary boundary correction."
        ),
        "checked_moduli": [int(m) for m in carry046.ALL_M_VALUES],
        "exact_target": {
            "B": ["s", "u", "v", "layer", "family"],
            "tau": "initial flat-run length for future grouped delta dn=(0,0,0,1)",
            "epsilon4": ["flat", "wrap", "carry_jump", "other"],
            "checked_range_exact_quotient": "B + min(tau,8) + epsilon4",
            "checked_range_transition_sheet": "B + epsilon4(current) + future_binary_after_current_window_length_7",
        },
        "quotient_pruning": {
            "boundary_partition_minimal_nonflat_class_count": int(
                quotient_exactness_summary["boundary_partition_search"]["minimal_nonflat_class_count"]
            ),
            "minimal_exact_tau_truncation_horizon": int(minimal_exact_truncation),
            "minimal_exact_tau_threshold_horizon": int(minimal_exact_threshold),
            "minimal_exact_interval_block_count": int(best_interval_block_count),
            "minimal_exact_interval_partitions": minimal_interval_partitions,
        },
        "transition_sheet_minimal_horizons": {
            "current_eps4_plus_future_binary_after_current": int(minimal_current_eps_future_binary_horizon),
            "eps4_window": int(minimal_eps4_window_horizon),
            "binary_window": int(minimal_binary_window_horizon),
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "frozen_B_c_tau_epsilon_dataset_047.json", frozen_dataset)
    _write_json(out_dir / "quotient_exactness_summary.json", quotient_exactness_summary)
    _write_json(out_dir / "representative_ambiguous_rows.json", representative_ambiguous_rows)
    _write_json(out_dir / "representative_exact_rows.json", representative_exact_rows)
    _write_json(args.summary_out, analysis_summary)

    print(f"task_id: {TASK_ID}")
    print("pruned the exact future-transition carry target and extracted the first exact checked-range transition-sheet coding.")


if __name__ == "__main__":
    main()
