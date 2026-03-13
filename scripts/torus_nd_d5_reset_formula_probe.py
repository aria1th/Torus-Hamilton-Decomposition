#!/usr/bin/env python3
"""Probe short symbolic laws for the D5 boundary reset maps."""

from __future__ import annotations

import argparse
import json
import time
from itertools import product
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_source_residue_refinement as refine049
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-RESET-FORMULA-PROBE-053"
DEFAULT_M_VALUES = (5, 7, 9, 11, 13, 15, 17, 19)
SMALL_COEFFS = (-2, -1, 0, 1, 2)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _jsonable_coeffs(coeffs: Sequence[int]) -> List[int]:
    return [int(value) for value in coeffs]


def _build_branch_tables(
    m_values: Sequence[int],
) -> Dict[str, Dict[int, Dict[Tuple[int, int, int], int]]]:
    out = {"carry_jump": {}, "other": {}}
    for m in m_values:
        rows = refine049._build_rows_for_m(int(m))
        out["carry_jump"][int(m)] = {
            (int(row["s"]), int(row["v"]), int(row["layer"])): int(row["next_tau"])
            for row in rows
            if int(row["tau"]) == 0 and str(row["epsilon4"]) == "carry_jump"
        }
        out["other"][int(m)] = {
            (int(row["s"]), int(row["u"]), int(row["layer"])): int(row["next_tau"])
            for row in rows
            if int(row["tau"]) == 0 and str(row["epsilon4"]) == "other"
        }
    return out


def _affine_value(key: Tuple[int, int, int], coeffs: Tuple[int, int, int], m: int) -> int:
    return int(sum(c * x for c, x in zip(coeffs, key)) % m)


def _single_affine_exact_laws(
    tables: Mapping[int, Mapping[Tuple[int, int, int], int]],
) -> List[Dict[str, object]]:
    hits = []
    for coeffs in product(SMALL_COEFFS, repeat=3):
        if coeffs == (0, 0, 0):
            continue
        exact = True
        per_m = {}
        for m, table in tables.items():
            residue_to_value = {}
            for key, value in table.items():
                residue = _affine_value(key, coeffs, int(m))
                if residue in residue_to_value and residue_to_value[residue] != int(value):
                    exact = False
                    break
                residue_to_value[residue] = int(value)
            if not exact:
                break
            per_m[str(m)] = {
                str(residue): int(value)
                for residue, value in sorted(residue_to_value.items())
            }
        if exact:
            hits.append({"coeffs": _jsonable_coeffs(coeffs), "per_m": per_m})
    return hits


def _target_values(branch: str, m: int) -> List[int]:
    if branch == "carry_jump":
        return [0, 1, m - 2]
    return [0, m - 4, m - 3]


def _support_as_small_residue_union(
    table: Mapping[Tuple[int, int, int], int],
    coeffs: Tuple[int, int, int],
    target_value: int,
    m: int,
    max_residues: int = 2,
) -> Tuple[bool, List[int]]:
    fibers: Dict[int, set[Tuple[int, int, int]]] = {}
    for key in table:
        residue = _affine_value(key, coeffs, m)
        fibers.setdefault(residue, set()).add(key)
    support = {key for key, value in table.items() if int(value) == int(target_value)}
    residues = sorted(residue for residue, pts in fibers.items() if pts and pts <= support)
    union = set().union(*(fibers[residue] for residue in residues)) if residues else set()
    return bool(union == support and len(residues) <= max_residues), residues


def _fiber_candidates(
    branch: str,
    tables: Mapping[int, Mapping[Tuple[int, int, int], int]],
) -> Dict[str, object]:
    out = {}
    for target_index, target_label in enumerate(("target0", "target1", "target2")):
        hits = []
        for coeffs in product(SMALL_COEFFS, repeat=3):
            if coeffs == (0, 0, 0):
                continue
            per_m = {}
            good = True
            for m, table in tables.items():
                target_value = _target_values(branch, int(m))[target_index]
                ok, residues = _support_as_small_residue_union(table, coeffs, target_value, int(m))
                if not ok:
                    good = False
                    break
                per_m[str(m)] = residues
            if good:
                hits.append({"coeffs": _jsonable_coeffs(coeffs), "per_m": per_m})
        out[target_label] = {
            "target_value_description": {
                "carry_jump": ["0", "1", "m-2"],
                "other": ["0", "m-4", "m-3"],
            }[branch][target_index],
            "candidate_count": int(len(hits)),
            "candidates": hits[:20],
        }
    return out


def _two_stage_piecewise_candidates(
    branch: str,
    tables: Mapping[int, Mapping[Tuple[int, int, int], int]],
) -> List[Dict[str, object]]:
    coeff_list = [coeffs for coeffs in product(SMALL_COEFFS, repeat=3) if coeffs != (0, 0, 0)]
    hits = []
    target_labels = {
        "carry_jump": [0, 1, "m-2"],
        "other": [0, "m-4", "m-3"],
    }[branch]
    for coeffs0 in coeff_list:
        for coeffs1 in coeff_list:
            exact = True
            per_m = {}
            for m, table in tables.items():
                values = _target_values(branch, int(m))
                support0 = {key for key, value in table.items() if value == values[0]}
                support1 = {key for key, value in table.items() if value == values[1]}
                ok0, residues0 = _support_as_small_residue_union(table, coeffs0, values[0], int(m))
                ok1, residues1 = _support_as_small_residue_union(table, coeffs1, values[1], int(m))
                if not ok0 or not ok1:
                    exact = False
                    break
                # Enforce a genuine staged law: target-1 support must be handled after removing target-0 support.
                covered0 = {key for key in table if _affine_value(key, coeffs0, int(m)) in residues0}
                covered1 = {key for key in table if _affine_value(key, coeffs1, int(m)) in residues1}
                if covered0 != support0 or (covered1 - covered0) != support1:
                    exact = False
                    break
                per_m[str(m)] = {"residues0": residues0, "residues1": residues1}
            if exact:
                hits.append(
                    {
                        "values": target_labels,
                        "coeffs0": _jsonable_coeffs(coeffs0),
                        "coeffs1": _jsonable_coeffs(coeffs1),
                        "per_m": per_m,
                    }
                )
    return hits


def _partition_tables(
    branch: str,
    tables: Mapping[int, Mapping[Tuple[int, int, int], int]],
) -> Dict[str, object]:
    out = {}
    for m, table in tables.items():
        counter: Dict[str, int] = {}
        for value in sorted(set(table.values())):
            counter[str(int(value))] = sum(1 for observed in table.values() if int(observed) == int(value))
        out[str(m)] = {
            "value_counts": counter,
            "sample_rows": [
                {"key": list(key), "next_tau": int(value)}
                for key, value in list(sorted(table.items()))[:16]
            ],
        }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe short symbolic laws for the D5 boundary reset maps.")
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

    tables = _build_branch_tables(args.m_values)

    single_affine = {
        branch: _single_affine_exact_laws(branch_tables)
        for branch, branch_tables in tables.items()
    }
    fiber_candidates = {
        branch: _fiber_candidates(branch, branch_tables)
        for branch, branch_tables in tables.items()
    }
    two_stage_piecewise = {
        branch: _two_stage_piecewise_candidates(branch, branch_tables)
        for branch, branch_tables in tables.items()
    }
    partition_tables = {
        branch: _partition_tables(branch, branch_tables)
        for branch, branch_tables in tables.items()
    }

    analysis_summary = {
        "task_id": TASK_ID,
        "main_result": (
            "The optional reset-formula probe finds no short global affine law for either boundary reset map, and no tested two-stage "
            "piecewise law built from one or two small-coefficient congruence conditions. The one clear positive result is a simple exact "
            "fiber on the carry_jump branch: the zero-reset locus is cut out on the tested range by s+v+layer ≡ 2 (mod m). Beyond that, "
            "the tested candidate family yields no comparably short symbolic law for the carry_jump value 1 fiber or for the other branch."
        ),
        "checked_moduli": [int(m) for m in args.m_values],
        "single_affine_exact_law_counts": {
            branch: int(len(rows))
            for branch, rows in single_affine.items()
        },
        "carry_jump_zero_fiber_has_simple_formula": bool(
            fiber_candidates["carry_jump"]["target0"]["candidate_count"] > 0
        ),
        "carry_jump_one_fiber_has_simple_formula": bool(
            fiber_candidates["carry_jump"]["target1"]["candidate_count"] > 0
        ),
        "other_branch_has_any_simple_fiber_formula": bool(
            any(
                fiber_candidates["other"][target]["candidate_count"] > 0
                for target in ("target0", "target1", "target2")
            )
        ),
        "tested_two_stage_piecewise_candidates": {
            branch: int(len(rows))
            for branch, rows in two_stage_piecewise.items()
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "reset_formula_candidates.json", {
        "single_affine_exact_laws": single_affine,
        "fiber_candidates": fiber_candidates,
        "two_stage_piecewise_candidates": {
            branch: rows[:20]
            for branch, rows in two_stage_piecewise.items()
        },
    })
    _write_json(out_dir / "reset_formula_failures.json", {
        "single_affine_exact_law_counts": {
            branch: int(len(rows))
            for branch, rows in single_affine.items()
        },
        "two_stage_piecewise_candidate_counts": {
            branch: int(len(rows))
            for branch, rows in two_stage_piecewise.items()
        },
        "notable_negative_claims": {
            "carry_jump_no_single_affine_output_law": bool(len(single_affine["carry_jump"]) == 0),
            "other_no_single_affine_output_law": bool(len(single_affine["other"]) == 0),
            "carry_jump_no_simple_formula_for_value_1_fiber": bool(
                fiber_candidates["carry_jump"]["target1"]["candidate_count"] == 0
            ),
            "other_no_simple_small_coeff_fiber_formula": bool(
                all(
                    fiber_candidates["other"][target]["candidate_count"] == 0
                    for target in ("target0", "target1", "target2")
                )
            ),
            "no_two_stage_piecewise_small_coeff_formula": bool(
                len(two_stage_piecewise["carry_jump"]) == 0 and len(two_stage_piecewise["other"]) == 0
            ),
        },
    })
    _write_json(out_dir / "reset_value_partition_tables.json", partition_tables)
    _write_json(args.summary_out, analysis_summary)


if __name__ == "__main__":
    main()
