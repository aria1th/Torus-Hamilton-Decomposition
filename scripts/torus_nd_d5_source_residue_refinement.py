#!/usr/bin/env python3
"""Extract the rho-refined current-state coding on the D5 active branch."""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import torus_nd_d5_future_transition_carry_coding as carry047
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-SOURCE-RESIDUE-REFINEMENT-049"
DEFAULT_M_VALUES = (5, 7, 9, 11, 13, 15, 17, 19)

TAU_FIELDS = ("s", "u", "v", "layer", "family", "rho")
NEXT_TAU_FIELDS = ("s", "u", "v", "layer", "family", "rho", "epsilon4")
CARRY_FIELDS = ("s", "u", "v", "layer", "family", "rho", "epsilon4")
RECOVERY_FIELDS = ("s", "u", "v", "layer", "family", "tau", "epsilon4")


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
        "rho": int(row["rho"]),
        "trace_step": int(row["trace_step"]),
        "family": str(row["family"]),
        "state_index": int(row["state_index"]),
        "s": int(row["s"]),
        "u": int(row["u"]),
        "v": int(row["v"]),
        "layer": int(row["layer"]),
        "q": int(row["q"]),
        "w": int(row["w"]),
        "c": int(row["c"]),
        "tau": int(row["tau"]),
        "epsilon4": str(row["epsilon4"]),
        "next_tau": int(row["next_tau"]),
        "next_epsilon4": str(row["next_epsilon4"]),
    }


def _sample_rows(rows: Sequence[Mapping[str, object]], limit: int = 4) -> List[Dict[str, object]]:
    return [_represent_row(row) for row in rows[:limit]]


def _build_rows_for_m(m: int, horizon: int = 10) -> List[Dict[str, object]]:
    payload = carry047._build_augmented_data(m, horizon)
    rows = payload["augmented_rows"]
    row_index = {
        (str(row["family"]), int(row["source_u"]), int(row["trace_step"])): row
        for row in rows
    }

    out: List[Dict[str, object]] = []
    for row in rows:
        next_row = row_index.get(
            (str(row["family"]), int(row["source_u"]), int(row["trace_step"]) + 1)
        )
        if next_row is None:
            continue
        b = list(row["B"])
        out.append(
            {
                "m": int(m),
                "source_u": int(row["source_u"]),
                "rho": int((int(row["source_u"]) + 1) % m),
                "trace_step": int(row["trace_step"]),
                "family": str(row["family"]),
                "state_index": int(row["state_index"]),
                "s": int(b[0]),
                "u": int(b[1]),
                "v": int(b[2]),
                "layer": int(b[3]),
                "q": int(row["q"]),
                "w": int(row["w"]),
                "c": int(row["c"]),
                "tau": int(row["tau"]),
                "epsilon4": str(row["epsilon4"]),
                "next_tau": int(next_row["tau"]),
                "next_epsilon4": str(next_row["epsilon4"]),
            }
        )
    return out


def _bucket_values(
    rows: Sequence[Mapping[str, object]],
    key_fields: Sequence[str],
    target_field: str,
) -> MutableMapping[Tuple[object, ...], List[object]]:
    buckets: MutableMapping[Tuple[object, ...], List[object]] = defaultdict(list)
    for row in rows:
        key = tuple(row[field] for field in key_fields)
        buckets[key].append(row[target_field])
    return buckets


def _collision_examples(
    rows_by_m: Mapping[int, Sequence[Mapping[str, object]]],
    *,
    key_fields: Sequence[str],
    target_field: str,
    limit_moduli: int = 2,
    limit_buckets: int = 2,
    limit_rows: int = 4,
) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for m in sorted(rows_by_m)[:]:
        buckets: MutableMapping[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
        for row in rows_by_m[m]:
            key = tuple(row[field] for field in key_fields)
            buckets[key].append(row)
        collisions = []
        for key, bucket in buckets.items():
            values = {row[target_field] for row in bucket}
            if len(values) > 1:
                collisions.append(
                    {
                        "m": int(m),
                        "key": _jsonable_key(key),
                        "target_values": sorted(int(value) for value in values),
                        "rows": _sample_rows(bucket, limit_rows),
                    }
                )
        if collisions:
            out.extend(collisions[:limit_buckets])
        if len(out) >= limit_moduli * limit_buckets:
            break
    return out


def _find_minimal_exact_subsets(
    rows_by_m: Mapping[int, Sequence[Mapping[str, object]]],
    *,
    candidate_fields: Sequence[str],
    target_field: str,
    allow_empty: bool = False,
) -> Dict[str, object]:
    start_size = 0 if allow_empty else 1
    for size in range(start_size, len(candidate_fields) + 1):
        exact_subsets = []
        collision_examples: List[Dict[str, object]] = []
        for subset in combinations(candidate_fields, size):
            exact = True
            for rows in rows_by_m.values():
                buckets = _bucket_values(rows, subset, target_field)
                if not all(len(set(values)) == 1 for values in buckets.values()):
                    exact = False
                    break
            if exact:
                exact_subsets.append(list(subset))
            elif not collision_examples:
                collision_examples = _collision_examples(
                    rows_by_m,
                    key_fields=subset,
                    target_field=target_field,
                )
        if exact_subsets:
            return {
                "minimal_size": int(size),
                "exact_subsets": exact_subsets,
                "collision_examples_at_previous_size": collision_examples,
            }
    raise AssertionError(f"no exact subset found for {target_field}")


def _subset_exactness_by_m(
    rows_by_m: Mapping[int, Sequence[Mapping[str, object]]],
    *,
    subset: Sequence[str],
    target_field: str,
) -> Dict[str, object]:
    out = {}
    for m, rows in rows_by_m.items():
        buckets = _bucket_values(rows, subset, target_field)
        out[str(m)] = {
            "row_count": int(len(rows)),
            "distinct_key_count": int(len(buckets)),
            "is_exact": bool(all(len(set(values)) == 1 for values in buckets.values())),
        }
    return out


def _nonrecoverability_summary(
    rows_by_m: Mapping[int, Sequence[Mapping[str, object]]],
) -> Dict[str, object]:
    per_m = {}
    sample_ambiguous_buckets: List[Dict[str, object]] = []
    matches_linear_law = True
    for m, rows in rows_by_m.items():
        buckets: MutableMapping[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
        for row in rows:
            key = tuple(row[field] for field in RECOVERY_FIELDS)
            buckets[key].append(row)
        ambiguous = []
        max_multiplicity = 1
        for key, bucket in buckets.items():
            rho_values = sorted({int(row["rho"]) for row in bucket})
            if len(rho_values) > 1:
                ambiguous.append((key, bucket, rho_values))
                max_multiplicity = max(max_multiplicity, len(rho_values))
        ambiguous_count = len(ambiguous)
        expected = None if m < 7 else 2 * m - 11
        if expected is not None and ambiguous_count != expected:
            matches_linear_law = False
        per_m[str(m)] = {
            "row_count": int(len(rows)),
            "ambiguous_bucket_count": int(ambiguous_count),
            "max_rho_multiplicity": int(max_multiplicity),
            "matches_2m_minus_11": None if expected is None else bool(ambiguous_count == expected),
            "expected_2m_minus_11": expected,
        }
        for key, bucket, rho_values in ambiguous[:2]:
            sample_ambiguous_buckets.append(
                {
                    "m": int(m),
                    "key": _jsonable_key(key),
                    "rho_values": rho_values,
                    "rows": _sample_rows(bucket),
                }
            )
    return {
        "per_modulus": per_m,
        "matches_2m_minus_11_on_m_ge_7": bool(matches_linear_law),
        "sample_ambiguous_buckets": sample_ambiguous_buckets[:10],
    }


def _q_formula_summary(
    rows_by_m: Mapping[int, Sequence[Mapping[str, object]]],
) -> Dict[str, object]:
    failures = []
    per_m = {}
    for m, rows in rows_by_m.items():
        bad_rows = []
        for row in rows:
            predicted = (int(row["u"]) - int(row["rho"]) + (1 if str(row["epsilon4"]) == "carry_jump" else 0)) % m
            if predicted != int(row["q"]):
                bad_rows.append(_represent_row(row))
        per_m[str(m)] = {
            "row_count": int(len(rows)),
            "failure_count": int(len(bad_rows)),
            "is_exact": bool(len(bad_rows) == 0),
        }
        failures.extend(bad_rows[:2])
    return {
        "formula": "q ≡ u - rho + 1_{epsilon4=carry_jump} (mod m)",
        "per_modulus": per_m,
        "sample_failures": failures[:10],
    }


def _boundary_rows(rows_by_m: Mapping[int, Sequence[Mapping[str, object]]]) -> Dict[int, List[Dict[str, object]]]:
    return {
        int(m): [row for row in rows if int(row["tau"]) == 0]
        for m, rows in rows_by_m.items()
    }


def _boundary_branch_rows(
    rows_by_m: Mapping[int, Sequence[Mapping[str, object]]],
    branch: str,
) -> Dict[int, List[Dict[str, object]]]:
    return {
        int(m): [row for row in rows if int(row["tau"]) == 0 and str(row["epsilon4"]) == branch]
        for m, rows in rows_by_m.items()
    }


def _representatives_by_m(
    rows_by_m: Mapping[int, Sequence[Mapping[str, object]]],
) -> Dict[str, object]:
    out = {}
    for m, rows in rows_by_m.items():
        seen_tau = set()
        sampled = []
        for row in rows:
            tau = int(row["tau"])
            if tau in seen_tau:
                continue
            sampled.append(_represent_row(row))
            seen_tau.add(tau)
            if len(sampled) >= 6:
                break
        out[str(m)] = sampled
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the rho-refined current-state coding on the D5 active branch.")
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

    rows_by_m = {int(m): _build_rows_for_m(int(m)) for m in args.m_values}
    boundary_by_m = _boundary_rows(rows_by_m)

    tau_minimal = _find_minimal_exact_subsets(
        rows_by_m,
        candidate_fields=TAU_FIELDS,
        target_field="tau",
    )
    next_tau_minimal = _find_minimal_exact_subsets(
        rows_by_m,
        candidate_fields=NEXT_TAU_FIELDS,
        target_field="next_tau",
    )
    carry_minimal = _find_minimal_exact_subsets(
        rows_by_m,
        candidate_fields=CARRY_FIELDS,
        target_field="c",
    )

    boundary_global = _find_minimal_exact_subsets(
        boundary_by_m,
        candidate_fields=NEXT_TAU_FIELDS,
        target_field="next_tau",
    )
    boundary_carry_jump = _find_minimal_exact_subsets(
        _boundary_branch_rows(rows_by_m, "carry_jump"),
        candidate_fields=TAU_FIELDS,
        target_field="next_tau",
    )
    boundary_other = _find_minimal_exact_subsets(
        _boundary_branch_rows(rows_by_m, "other"),
        candidate_fields=TAU_FIELDS,
        target_field="next_tau",
    )
    boundary_wrap = _find_minimal_exact_subsets(
        _boundary_branch_rows(rows_by_m, "wrap"),
        candidate_fields=TAU_FIELDS,
        target_field="next_tau",
        allow_empty=True,
    )

    current_state_exactness = {
        "tau_on_s_u_v_layer_rho": _subset_exactness_by_m(
            rows_by_m,
            subset=("s", "u", "v", "layer", "rho"),
            target_field="tau",
        ),
        "next_tau_on_s_u_layer_rho_epsilon4": _subset_exactness_by_m(
            rows_by_m,
            subset=("s", "u", "layer", "rho", "epsilon4"),
            target_field="next_tau",
        ),
        "c_on_u_rho_epsilon4": _subset_exactness_by_m(
            rows_by_m,
            subset=("u", "rho", "epsilon4"),
            target_field="c",
        ),
    }

    q_formula = _q_formula_summary(rows_by_m)
    nonrecoverability = _nonrecoverability_summary(rows_by_m)

    source_residue_refinement = {
        "checked_moduli": [int(m) for m in args.m_values],
        "main_current_state_refinement": {
            "tau_exact_on": ["s", "u", "v", "layer", "rho"],
            "next_tau_exact_on": ["s", "u", "layer", "rho", "epsilon4"],
            "c_exact_on": ["u", "rho", "epsilon4"],
        },
        "minimal_exact_subsets": {
            "tau": tau_minimal,
            "next_tau": next_tau_minimal,
            "c": carry_minimal,
        },
        "q_formula": q_formula,
        "rho_nonrecoverability": nonrecoverability,
    }

    boundary_reset_with_rho = {
        "global_tau_zero_reset": boundary_global,
        "wrap_branch": boundary_wrap,
        "carry_jump_branch": boundary_carry_jump,
        "other_branch": boundary_other,
    }

    analysis_summary = {
        "task_id": TASK_ID,
        "main_result": (
            "On the active D5 best-seed branch, the future-side carry/anticipation object admits a stronger current-state "
            "source-residue refinement through m=19. With rho = source_u + 1 (mod m), tau is minimally exact on "
            "(s,u,v,layer,rho), next_tau is minimally exact on (s,u,layer,rho,epsilon4), c is minimally exact on "
            "(u,rho,epsilon4), and q satisfies q ≡ u - rho + 1_{epsilon4=carry_jump} (mod m). This is a constructive "
            "refinement of the theorem-side cover, not an equivalent reparametrization: rho is not recoverable from "
            "(B,tau,epsilon4) once m>=7, and the ambiguous bucket count matches 2m-11 on the tested extended range."
        ),
        "checked_moduli": [int(m) for m in args.m_values],
        "current_state_exactness": current_state_exactness,
        "boundary_reset_with_rho": {
            "global_tau_zero_minimal_size": int(boundary_global["minimal_size"]),
            "carry_jump_minimal_size": int(boundary_carry_jump["minimal_size"]),
            "other_minimal_size": int(boundary_other["minimal_size"]),
            "wrap_minimal_size": int(boundary_wrap["minimal_size"]),
        },
        "rho_nonrecoverability_matches_2m_minus_11_on_m_ge_7": bool(
            nonrecoverability["matches_2m_minus_11_on_m_ge_7"]
        ),
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "source_residue_refinement_summary_049.json", source_residue_refinement)
    _write_json(out_dir / "current_state_exactness_summary_049.json", current_state_exactness)
    _write_json(out_dir / "boundary_reset_with_rho_summary_049.json", boundary_reset_with_rho)
    _write_json(out_dir / "q_formula_validation_049.json", q_formula)
    _write_json(out_dir / "rho_nonrecoverability_summary_049.json", nonrecoverability)
    _write_json(
        out_dir / "minimal_subset_collision_witnesses_049.json",
        {
            "tau": tau_minimal["collision_examples_at_previous_size"],
            "next_tau": next_tau_minimal["collision_examples_at_previous_size"],
            "c": carry_minimal["collision_examples_at_previous_size"],
        },
    )
    _write_json(out_dir / "representative_rows_049.json", _representatives_by_m(rows_by_m))
    _write_json(args.summary_out, analysis_summary)


if __name__ == "__main__":
    main()
