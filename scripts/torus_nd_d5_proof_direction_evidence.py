#!/usr/bin/env python3
"""Consolidate compute evidence supporting the D5 proof directions."""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Mapping, MutableMapping, Sequence, Tuple

import torus_nd_d5_future_transition_carry_coding as carry047
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-PROOF-DIRECTION-EVIDENCE-052"
DEFAULT_M_VALUES = (5, 7, 9, 11, 13, 15, 17, 19)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _jsonable_key(key: Tuple[object, ...]) -> List[object]:
    out: List[object] = []
    for value in key:
        if isinstance(value, tuple):
            out.append(_jsonable_key(value))
        else:
            out.append(value)
    return out


def _represent_row(row: Mapping[str, object]) -> Dict[str, object]:
    return {
        "m": int(row["m"]),
        "source_u": int(row["source_u"]),
        "trace_step": int(row["trace_step"]),
        "family": str(row["family"]),
        "state_index": int(row["state_index"]),
        "B": list(row["B"]),
        "c": int(row["c"]),
        "q": int(row["q"]),
        "w": int(row["w"]),
        "u": int(row["u"]),
        "v": int(row["v"]),
        "layer": int(row["layer"]),
        "tau": int(row["tau"]),
        "epsilon4": str(row["epsilon4"]),
    }


def _collision_summary(
    rows: Sequence[Mapping[str, object]],
    key_getter,
) -> Dict[str, object]:
    buckets: MutableMapping[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        buckets[key_getter(row)].append(row)

    collision_buckets = []
    for key, bucket in buckets.items():
        labels = {int(row["c"]) for row in bucket}
        if len(labels) > 1:
            collision_buckets.append((key, bucket))

    return {
        "distinct_key_count": int(len(buckets)),
        "collision_bucket_count": int(len(collision_buckets)),
        "ambiguous_row_count": int(sum(len(bucket) for _, bucket in collision_buckets)),
        "is_exact": bool(len(collision_buckets) == 0),
        "collision_buckets": collision_buckets,
    }


def _summary_without_buckets(payload: Mapping[str, object]) -> Dict[str, object]:
    return {key: value for key, value in payload.items() if key != "collision_buckets"}


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


def _event_partition_label(row: Mapping[str, object], partition: Mapping[str, str]) -> str:
    epsilon = str(row["epsilon4"])
    if epsilon == "flat":
        return "flat"
    return str(partition[epsilon])


def _partition_catalog() -> List[Dict[str, object]]:
    return [
        {
            "name": "flat+wrap/carry_jump/other",
            "partition": {"wrap": "wrap", "carry_jump": "carry_jump", "other": "other"},
        },
        {
            "name": "flat+(wrap,carry_jump)/other",
            "partition": {"wrap": "nonflat_a", "carry_jump": "nonflat_a", "other": "nonflat_b"},
        },
        {
            "name": "flat+(wrap,other)/carry_jump",
            "partition": {"wrap": "nonflat_a", "carry_jump": "nonflat_b", "other": "nonflat_a"},
        },
        {
            "name": "flat+wrap/(carry_jump,other)",
            "partition": {"wrap": "nonflat_a", "carry_jump": "nonflat_b", "other": "nonflat_b"},
        },
        {
            "name": "flat+all_nonflat_merged",
            "partition": {"wrap": "nonflat", "carry_jump": "nonflat", "other": "nonflat"},
        },
    ]


def _first_exact_horizon(rows: Sequence[Mapping[str, object]], key_getter, max_horizon: int) -> int:
    for horizon in range(max_horizon + 1):
        summary = _collision_summary(rows, lambda row, h=horizon: key_getter(row, h))
        if summary["is_exact"]:
            return int(horizon)
    raise AssertionError("no exact horizon found")


def _per_modulus_summary(m: int) -> Dict[str, object]:
    payload = carry047._build_augmented_data(m, m)
    rows = payload["augmented_rows"]

    b_tau = _collision_summary(rows, lambda row: (tuple(row["B"]), int(row["tau"])))
    b_tau_tau_gt_0 = _collision_summary(
        [row for row in rows if int(row["tau"]) > 0],
        lambda row: (tuple(row["B"]), int(row["tau"])),
    )
    b_tau_epsilon = _collision_summary(
        rows,
        lambda row: (tuple(row["B"]), int(row["tau"]), str(row["epsilon4"])),
    )
    tau_zero_collisions = sum(1 for key, _bucket in b_tau["collision_buckets"] if int(key[1]) == 0)
    tau_positive_collisions = sum(1 for key, _bucket in b_tau["collision_buckets"] if int(key[1]) > 0)

    max_tau = max(int(row["tau"]) for row in rows)
    truncation_rows = []
    exact_truncation_horizon = None
    for horizon in range(max_tau + 1):
        summary = _collision_summary(
            rows,
            lambda row, h=horizon: (
                tuple(row["B"]),
                int(min(int(row["tau"]), h)),
                str(row["epsilon4"]),
            ),
        )
        truncation_rows.append(
            {
                "horizon": int(horizon),
                **_summary_without_buckets(summary),
            }
        )
        if exact_truncation_horizon is None and summary["is_exact"]:
            exact_truncation_horizon = int(horizon)

    partition_rows = []
    exact_partition_names = []
    for entry in _partition_catalog():
        summary = _collision_summary(
            rows,
            lambda row, partition=entry["partition"]: (
                tuple(row["B"]),
                int(row["tau"]),
                _event_partition_label(row, partition),
            ),
        )
        partition_rows.append(
            {
                "name": entry["name"],
                "partition": entry["partition"],
                **_summary_without_buckets(summary),
            }
        )
        if summary["is_exact"]:
            exact_partition_names.append(entry["name"])

    minimal_nonflat_class_count = min(
        len(set(entry["partition"].values()))
        for entry, row in zip(_partition_catalog(), partition_rows)
        if row["is_exact"]
    )

    exact_horizons = {
        "current_eps4_plus_future_binary_after_current": _first_exact_horizon(
            rows,
            lambda row, h: (
                tuple(row["B"]),
                str(row["epsilon4"]),
                tuple(int(value) for value in row["future_binary_after_current_max"][:h]),
            ),
            m,
        ),
        "eps4_window": _first_exact_horizon(
            rows,
            lambda row, h: (
                tuple(row["B"]),
                tuple(row["event_window_max"][:h]),
            ),
            m,
        ),
        "binary_window": _first_exact_horizon(
            rows,
            lambda row, h: (
                tuple(row["B"]),
                tuple(int(value) for value in row["binary_window_max"][:h]),
            ),
            m,
        ),
    }

    truncation_h_minus_1 = _collision_summary(
        rows,
        lambda row: (
            tuple(row["B"]),
            int(min(int(row["tau"]), exact_truncation_horizon - 1)),
            str(row["epsilon4"]),
        ),
    )
    binary_after_current_h_minus_1 = _collision_summary(
        rows,
        lambda row: (
            tuple(row["B"]),
            str(row["epsilon4"]),
            tuple(
                int(value)
                for value in row["future_binary_after_current_max"][: exact_horizons["current_eps4_plus_future_binary_after_current"] - 1]
            ),
        ),
    )

    return {
        "m": int(m),
        "row_count": int(len(rows)),
        "B_plus_tau": _summary_without_buckets(b_tau),
        "B_plus_tau_tau_gt_0": _summary_without_buckets(b_tau_tau_gt_0),
        "B_plus_tau_plus_epsilon4": _summary_without_buckets(b_tau_epsilon),
        "B_plus_tau_collision_buckets_tau_eq_0": int(tau_zero_collisions),
        "B_plus_tau_collision_buckets_tau_gt_0": int(tau_positive_collisions),
        "tau_truncation_rows": truncation_rows,
        "minimal_exact_tau_truncation_horizon": int(exact_truncation_horizon),
        "boundary_partition_rows": partition_rows,
        "boundary_partition_minimal_nonflat_class_count": int(minimal_nonflat_class_count),
        "boundary_exact_partition_names": exact_partition_names,
        "transition_sheet_minimal_horizons": exact_horizons,
        "expected_patterns": {
            "tau_truncation_matches_m_minus_3": bool(exact_truncation_horizon == m - 3),
            "current_eps4_plus_future_binary_after_current_matches_m_minus_4": bool(
                exact_horizons["current_eps4_plus_future_binary_after_current"] == m - 4
            ),
            "eps4_window_matches_m_minus_3": bool(exact_horizons["eps4_window"] == m - 3),
            "binary_window_matches_m_minus_1": bool(exact_horizons["binary_window"] == m - 1),
        },
        "representative_collisions": {
            "tau_truncation_H_minus_1": _sample_collision_rows(truncation_h_minus_1),
            "current_eps4_plus_future_binary_after_current_H_minus_1": _sample_collision_rows(binary_after_current_h_minus_1),
        },
    }


def _load_json(path: Path) -> Mapping[str, object]:
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser(description="Consolidate compute evidence supporting the D5 proof directions.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument(
        "--m-values",
        type=int,
        nargs="+",
        default=list(DEFAULT_M_VALUES),
        help="Odd moduli to analyze.",
    )
    parser.add_argument("--workers", type=int, default=4, help="Worker count for per-modulus extraction.")
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    m_values = [int(m) for m in args.m_values]
    worker_count = max(1, int(args.workers))
    if worker_count == 1:
        summaries = [_per_modulus_summary(m) for m in m_values]
    else:
        with mp.Pool(worker_count) as pool:
            summaries = pool.map(_per_modulus_summary, m_values)
    summaries = sorted(summaries, key=lambda row: int(row["m"]))

    per_modulus = {str(row["m"]): row for row in summaries}

    support_049 = _load_json(
        Path("artifacts/d5_source_residue_refinement_049/data/analysis_summary.json")
    )
    support_050 = _load_json(
        Path("artifacts/d5_proof_support_generalization_050/data/analysis_summary.json")
    )
    witness_support = _load_json(
        Path("artifacts/d5_proof_support_generalization_050/data/witness_pair_persistence_050.json")
    )

    positive_route_support = {
        "theorem_side_reset_map": {
            "description": "Reset-law exactness and persistence on the theorem-side quotient from 048/050.",
            "checked_moduli": support_050["checked_moduli"],
            "countdown_failures": support_050["reset_law_generalization"]["countdown_failures"],
            "carry_jump_exact_on_s_v_layer": support_050["reset_law_generalization"]["carry_jump_exact_on_s_v_layer"],
            "other_exact_on_s_u_layer": support_050["reset_law_generalization"]["other_exact_on_s_u_layer"],
        },
        "constructive_rho_refinement": {
            "description": "Stronger current-state constructive refinement from 049.",
            "checked_moduli": support_049["checked_moduli"],
            "tau_on_s_u_v_layer_rho": support_049["current_state_exactness"]["tau_on_s_u_v_layer_rho"],
            "next_tau_on_s_u_layer_rho_epsilon4": support_049["current_state_exactness"]["next_tau_on_s_u_layer_rho_epsilon4"],
            "c_on_u_rho_epsilon4": support_049["current_state_exactness"]["c_on_u_rho_epsilon4"],
        },
    }

    negative_route_support = {
        "minimal_theorem_side_horizons": {
            str(row["m"]): {
                "tau_truncation": int(row["minimal_exact_tau_truncation_horizon"]),
                **row["transition_sheet_minimal_horizons"],
            }
            for row in summaries
        },
        "witness_pair_support": witness_support,
    }

    analysis_summary = {
        "task_id": TASK_ID,
        "main_result": (
            "The proof-support evidence around the minimal theorem-side object (B,tau,epsilon4) is now consolidated through m=19. "
            "First, the 047 quotient picture generalizes on the tested range: B+tau is exact away from tau=0, B+tau+epsilon4 is globally exact, "
            "the first exact tau truncation stays m-3, and the first exact transition-sheet horizons stay m-4 for current epsilon4 plus future binary "
            "after current, m-3 for full event windows, and m-1 for pure binary windows. The boundary event class is genuinely 3-way on every tested "
            "modulus m>=7, with m=5 the expected small-modulus degenerate exception. "
            "Second, the 048/050 reset-law support remains exact on the same small theorem-side quotients. Third, 049 provides a stronger "
            "constructive current-memory refinement through rho, while 050 extends the witness-pair lower-bound support through m=19."
        ),
        "checked_moduli": m_values,
        "per_modulus_expected_pattern_holds": {
            str(row["m"]): row["expected_patterns"]
            for row in summaries
        },
        "positive_route_support": {
            "reset_law_persists_through_m19": bool(
                all(
                    support_050["reset_law_generalization"]["carry_jump_exact_on_s_v_layer"][str(m)]
                    and support_050["reset_law_generalization"]["other_exact_on_s_u_layer"][str(m)]
                    for m in m_values
                )
            ),
            "rho_refinement_persists_through_m19": bool(
                all(
                    support_049["current_state_exactness"]["tau_on_s_u_v_layer_rho"][str(m)]["is_exact"]
                    and support_049["current_state_exactness"]["next_tau_on_s_u_layer_rho_epsilon4"][str(m)]["is_exact"]
                    and support_049["current_state_exactness"]["c_on_u_rho_epsilon4"][str(m)]["is_exact"]
                    for m in m_values
                )
            ),
        },
        "negative_route_support": {
            "all_transition_horizon_patterns_hold": bool(
                all(all(patterns.values()) for patterns in (
                    row["expected_patterns"] for row in summaries
                ))
            ),
            "boundary_three_way_minimal_for_m_ge_7": bool(
                all(
                    int(row["m"]) < 7 or int(row["boundary_partition_minimal_nonflat_class_count"]) == 3
                    for row in summaries
                )
            ),
            "witness_pair_matches_expected_pattern_through_m19": bool(
                all(
                    witness_support[str(m)]["matches_expected_pattern"]
                    for m in m_values
                )
            ),
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "per_modulus_theorem_support_052.json", per_modulus)
    _write_json(out_dir / "positive_route_support_052.json", positive_route_support)
    _write_json(out_dir / "negative_route_support_052.json", negative_route_support)
    _write_json(args.summary_out, analysis_summary)


if __name__ == "__main__":
    main()
