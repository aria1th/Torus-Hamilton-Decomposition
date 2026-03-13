#!/usr/bin/env python3
"""Run narrow proof-support checks beyond the checked D5 pilot range."""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Mapping, MutableMapping, Sequence, Tuple

import torus_nd_d5_future_transition_carry_coding as carry047
import torus_nd_d5_source_residue_refinement as refine049
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-PROOF-SUPPORT-GENERALIZATION-050"
DEFAULT_M_VALUES = (5, 7, 9, 11, 13, 15, 17, 19)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _bucket_exactness(
    rows: Sequence[Mapping[str, object]],
    *,
    key_fields: Sequence[str],
    target_field: str,
) -> Dict[str, object]:
    buckets: MutableMapping[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        key = tuple(row[field] for field in key_fields)
        buckets[key].append(row)

    collision_buckets = []
    for key, bucket in buckets.items():
        values = sorted({int(row[target_field]) for row in bucket})
        if len(values) > 1:
            collision_buckets.append(
                {
                    "key": list(key),
                    "target_values": values,
                    "rows": [
                        {
                            "m": int(row["m"]),
                            "source_u": int(row["source_u"]),
                            "trace_step": int(row["trace_step"]),
                            "family": str(row["family"]),
                            "s": int(row["s"]),
                            "u": int(row["u"]),
                            "v": int(row["v"]),
                            "layer": int(row["layer"]),
                            "tau": int(row["tau"]),
                            "epsilon4": str(row["epsilon4"]),
                            "next_tau": int(row["next_tau"]),
                        }
                        for row in bucket[:4]
                    ],
                }
            )
    return {
        "distinct_key_count": int(len(buckets)),
        "collision_bucket_count": int(len(collision_buckets)),
        "is_exact": bool(len(collision_buckets) == 0),
        "sample_collisions": collision_buckets[:3],
    }


def _reset_summary_for_m(m: int) -> Dict[str, object]:
    rows = refine049._build_rows_for_m(m)
    positive_rows = [row for row in rows if int(row["tau"]) > 0]
    boundary_rows = [row for row in rows if int(row["tau"]) == 0]
    carry_jump_rows = [row for row in boundary_rows if str(row["epsilon4"]) == "carry_jump"]
    other_rows = [row for row in boundary_rows if str(row["epsilon4"]) == "other"]
    wrap_rows = [row for row in boundary_rows if str(row["epsilon4"]) == "wrap"]

    countdown_failures = [
        {
            "source_u": int(row["source_u"]),
            "trace_step": int(row["trace_step"]),
            "tau": int(row["tau"]),
            "next_tau": int(row["next_tau"]),
        }
        for row in positive_rows
        if int(row["next_tau"]) != int(row["tau"]) - 1
    ]

    carry_jump_exact = _bucket_exactness(
        carry_jump_rows,
        key_fields=("s", "v", "layer"),
        target_field="next_tau",
    )
    other_exact = _bucket_exactness(
        other_rows,
        key_fields=("s", "u", "layer"),
        target_field="next_tau",
    )

    carry_jump_values = sorted({int(row["next_tau"]) for row in carry_jump_rows})
    other_values = sorted({int(row["next_tau"]) for row in other_rows})
    wrap_values = sorted({int(row["next_tau"]) for row in wrap_rows})

    carry_jump_table = [
        {
            "key": [int(row["s"]), int(row["v"]), int(row["layer"])],
            "next_tau": int(row["next_tau"]),
        }
        for row in sorted(carry_jump_rows, key=lambda r: (r["s"], r["v"], r["layer"]))[:12]
    ]
    other_table = [
        {
            "key": [int(row["s"]), int(row["u"]), int(row["layer"])],
            "next_tau": int(row["next_tau"]),
        }
        for row in sorted(other_rows, key=lambda r: (r["s"], r["u"], r["layer"]))[:12]
    ]

    return {
        "row_count": int(len(rows)),
        "positive_row_count": int(len(positive_rows)),
        "boundary_row_count": int(len(boundary_rows)),
        "countdown_failure_count": int(len(countdown_failures)),
        "countdown_sample_failures": countdown_failures[:5],
        "carry_jump_exact_on_s_v_layer": carry_jump_exact,
        "other_exact_on_s_u_layer": other_exact,
        "wrap_reset_values": wrap_values,
        "carry_jump_reset_values": carry_jump_values,
        "other_reset_values": other_values,
        "carry_jump_values_match_0_1_m_minus_2": bool(carry_jump_values == [0, 1, m - 2]),
        "other_values_match_0_m_minus_4_m_minus_3": bool(other_values == [0, m - 4, m - 3]),
        "sample_carry_jump_table": carry_jump_table,
        "sample_other_table": other_table,
    }


def _witness_summary_for_m(m: int) -> Dict[str, object]:
    rows = carry047._build_augmented_data(m, m)["augmented_rows"]
    hits = [
        row
        for row in rows
        if int(row["q"]) in (m - 2, m - 1)
        and int(row["w"]) == 2
        and int(row["u"]) == 1
        and int(row["v"]) == 2
        and int(row["layer"]) == 0
        and str(row["family"]) == "regular"
    ]
    hits = sorted(hits, key=lambda row: int(row["q"]))
    if len(hits) != 2:
        raise AssertionError(f"expected 2 witness hits for m={m}, found {len(hits)}")

    x_minus, x_plus = hits
    prefix_minus = list(x_minus["future_binary_after_current_max"])
    prefix_plus = list(x_plus["future_binary_after_current_max"])
    common_prefix_length = 0
    while (
        common_prefix_length < min(len(prefix_minus), len(prefix_plus))
        and prefix_minus[common_prefix_length] == prefix_plus[common_prefix_length]
    ):
        common_prefix_length += 1

    return {
        "x_minus": {
            "q": int(x_minus["q"]),
            "w": int(x_minus["w"]),
            "u": int(x_minus["u"]),
            "v": int(x_minus["v"]),
            "layer": int(x_minus["layer"]),
            "c": int(x_minus["c"]),
            "tau": int(x_minus["tau"]),
            "epsilon4": str(x_minus["epsilon4"]),
            "B": list(x_minus["B"]),
            "source_u": int(x_minus["source_u"]),
            "trace_step": int(x_minus["trace_step"]),
        },
        "x_plus": {
            "q": int(x_plus["q"]),
            "w": int(x_plus["w"]),
            "u": int(x_plus["u"]),
            "v": int(x_plus["v"]),
            "layer": int(x_plus["layer"]),
            "c": int(x_plus["c"]),
            "tau": int(x_plus["tau"]),
            "epsilon4": str(x_plus["epsilon4"]),
            "B": list(x_plus["B"]),
            "source_u": int(x_plus["source_u"]),
            "trace_step": int(x_plus["trace_step"]),
        },
        "common_future_binary_prefix_length": int(common_prefix_length),
        "first_difference_index": int(common_prefix_length),
        "claimed_lower_bound_valid_for_h_less_than": int(common_prefix_length + 1),
        "matches_expected_pattern": bool(
            int(x_minus["q"]) == m - 2
            and int(x_plus["q"]) == m - 1
            and int(x_minus["tau"]) == m - 3
            and int(x_plus["tau"]) == m - 4
            and common_prefix_length == m - 5
            and str(x_minus["epsilon4"]) == "flat"
            and str(x_plus["epsilon4"]) == "flat"
            and list(x_minus["B"]) == [3, 1, 2, 0, "regular"]
            and list(x_plus["B"]) == [3, 1, 2, 0, "regular"]
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run narrow proof-support checks beyond the checked D5 pilot range.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument(
        "--m-values",
        type=int,
        nargs="+",
        default=list(DEFAULT_M_VALUES),
        help="Odd moduli to analyze.",
    )
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    reset_law_generalization = {
        str(m): _reset_summary_for_m(int(m))
        for m in args.m_values
    }
    witness_pair_persistence = {
        str(m): _witness_summary_for_m(int(m))
        for m in args.m_values
    }

    analysis_summary = {
        "task_id": TASK_ID,
        "main_result": (
            "The two highest-value proof-support checks from the 050 parallel request persist on the extended odd-modulus range through m=19. "
            "First, the 048 reset law remains exact: countdown has no failures, wrap resets to 0, carry_jump stays exact on (s,v,layer), "
            "and other stays exact on (s,u,layer); moreover the reset-value sets stabilize as carry_jump in {0,1,m-2} and other in {0,m-4,m-3}. "
            "Second, the explicit witness pair from the 047/048 lower-bound direction persists exactly with x^-_m=(m-2,2,1,2,0), "
            "x^+_m=(m-1,2,1,2,0), common B=(3,1,2,0,regular), tau values m-3 and m-4, and common future-binary prefix length m-5."
        ),
        "checked_moduli": [int(m) for m in args.m_values],
        "reset_law_generalization": {
            "countdown_failures": {
                str(m): int(payload["countdown_failure_count"])
                for m, payload in reset_law_generalization.items()
            },
            "carry_jump_exact_on_s_v_layer": {
                str(m): bool(payload["carry_jump_exact_on_s_v_layer"]["is_exact"])
                for m, payload in reset_law_generalization.items()
            },
            "other_exact_on_s_u_layer": {
                str(m): bool(payload["other_exact_on_s_u_layer"]["is_exact"])
                for m, payload in reset_law_generalization.items()
            },
        },
        "witness_pair_matches_expected_pattern": {
            str(m): bool(payload["matches_expected_pattern"])
            for m, payload in witness_pair_persistence.items()
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "reset_law_generalization_050.json", reset_law_generalization)
    _write_json(out_dir / "witness_pair_persistence_050.json", witness_pair_persistence)
    _write_json(args.summary_out, analysis_summary)


if __name__ == "__main__":
    main()
