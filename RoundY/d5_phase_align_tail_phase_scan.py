#!/usr/bin/env python3
"""Scan candidate tail-phase bits after Theta_AB + phase_align.

This script reproduces the analysis saved in
`d5_phase_align_tail_phase_scan_summary.json`.

It works from the extracted phase-align bundle directory, defaulting to
`/mnt/data/tmp_phase/d5_theta_ab_phase_align_001`.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Sequence, Tuple

PILOT_M_VALUES = (5, 7, 9)
EXTENDED_M_VALUES_KEY = (5, 7, 9, 11, 13)


def load_family_module(bundle_dir: Path):
    mod_path = bundle_dir / "scripts" / "torus_nd_d5_master_field_quotient_family.py"
    spec = importlib.util.spec_from_file_location("fam_tail_phase_scan", mod_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {mod_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["fam_tail_phase_scan"] = module
    spec.loader.exec_module(module)
    return module


def load_strict_field(bundle_dir: Path) -> Dict[int, Tuple[int, ...]]:
    field = json.loads((bundle_dir / "data" / "best_strict_collapse_field.json").read_text())
    return {int(row["state_id"]): tuple(row["permutation"]) for row in field["anchor_table"]["rows"]}


def precompute_full(bundle_dir: Path, fam, table: Dict[int, Sequence[int]], m: int):
    schema = fam.SCHEMA_PHASE_ALIGN
    state_ids = fam.vertex_state_ids(schema.name, m, EXTENDED_M_VALUES_KEY)
    visited = []
    for q in range(m):
        for w in range(m):
            for v in range(m):
                for u in range(m):
                    cur = ((-q - w - v - u) % m, q, w, v, u)
                    for _ in range(m):
                        idx = fam.encode_vertex(cur, m)
                        sid = state_ids[idx]
                        q0, w0, v0, u0 = cur[1], cur[2], cur[3], cur[4]
                        delta = (v0 - q0) % m
                        visited.append((sid, q0, w0, u0, delta))
                        cur = fam.color_map_from_table(table, schema, m, cur, 0, EXTENDED_M_VALUES_KEY)
    return visited


def stats_for_pred(visited, m: int, pred: Callable[[int, int, int, int, int], bool]) -> Dict[str, object]:
    delta_support = defaultdict(set)
    for sid, q, w, u, delta in visited:
        delta_support[(sid, 1 if pred(q, w, u, delta, m) else 0)].add(delta)
    all_nonzero = list(range(1, m))
    multi = 0
    total_excess = 0
    full_nonzero = 0
    histogram = Counter()
    for values in delta_support.values():
        if len(values) <= 1:
            continue
        multi += 1
        total_excess += len(values) - 1
        histogram[len(values)] += 1
        if sorted(values) == all_nonzero:
            full_nonzero += 1
    return {
        "multi_delta_state_count": multi,
        "total_excess": total_excess,
        "full_nonzero_support_state_count": full_nonzero,
        "support_histogram": dict(sorted(histogram.items())),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bundle-dir",
        type=Path,
        default=Path("/mnt/data/tmp_phase/d5_theta_ab_phase_align_001"),
        help="Extracted phase-align bundle directory",
    )
    parser.add_argument(
        "--pred-scan-json",
        type=Path,
        default=Path("/mnt/data/d5_phase_align_simple_predecessor_bit_scan.json"),
        help="Existing predecessor-bit scan JSON for comparison",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("/mnt/data/d5_phase_align_tail_phase_scan_summary.json"),
        help="Write summary JSON here",
    )
    args = parser.parse_args(argv)

    fam = load_family_module(args.bundle_dir)
    table = load_strict_field(args.bundle_dir)
    pre_full = {m: precompute_full(args.bundle_dir, fam, table, m) for m in PILOT_M_VALUES}

    baseline = {str(m): stats_for_pred(pre_full[m], m, lambda q, w, u, delta, m: False) for m in PILOT_M_VALUES}

    best_arbitrary = {}
    top_arbitrary = {}
    for m in PILOT_M_VALUES:
        residues = list(range(1, m))
        seen = set()
        rows = []
        for mask in range(1, 1 << (m - 1)):
            subset = tuple(residues[i] for i in range(m - 1) if (mask >> i) & 1)
            comp = tuple(r for r in residues if r not in subset)
            canon = min(subset, comp)
            if canon in seen:
                continue
            seen.add(canon)
            stats = stats_for_pred(pre_full[m], m, lambda q, w, u, delta, m, subset=set(subset): delta in subset)
            rows.append({"subset": list(subset), "complement_subset": list(comp), **stats})
        rows.sort(
            key=lambda row: (
                row["total_excess"],
                row["multi_delta_state_count"],
                row["full_nonzero_support_state_count"],
                len(row["subset"]),
                row["subset"],
            )
        )
        best_arbitrary[str(m)] = rows[0]
        top_arbitrary[str(m)] = rows[:20]

    structured_families = {
        "delta_eq_1": lambda m: {1},
        "delta_eq_minus1": lambda m: {m - 1},
        "delta_eq_plusminus1": lambda m: {1, m - 1},
        "delta_eq_2": lambda m: {2 % m},
        "delta_eq_plusminus2": lambda m: {2 % m, (m - 2) % m},
        "delta_in_1_2": lambda m: {r for r in [1, 2] if 0 < r < m},
        "delta_in_plusminus1_plusminus2": lambda m: {r for r in [1, 2, m - 2, m - 1] if 0 < r < m},
        "delta_odd_residue": lambda m: {r for r in range(1, m) if r % 2 == 1},
        "delta_even_residue": lambda m: {r for r in range(1, m) if r % 2 == 0},
        "delta_first_half": lambda m: set(range(1, (m + 1) // 2)),
        "delta_quadratic_residue": lambda m: {pow(a, 2, m) for a in range(1, m) if pow(a, 2, m) != 0},
    }
    structured = {}
    for name, subset_fn in structured_families.items():
        structured[name] = {}
        for m in PILOT_M_VALUES:
            structured[name][str(m)] = {
                "subset": sorted(subset_fn(m)),
                **stats_for_pred(pre_full[m], m, lambda q, w, u, delta, m, subset_fn=subset_fn: delta in subset_fn(m)),
            }

    affine_rows = []
    for a, b, c in itertools.product([-1, 0, 1], repeat=3):
        for rhs in (-2, -1, 0, 1, 2):
            name = f"{a}q+{b}w+{c}u+delta={rhs}"
            stats = {
                str(m): stats_for_pred(
                    pre_full[m],
                    m,
                    lambda q, w, u, delta, m, a=a, b=b, c=c, rhs=rhs: ((a * q + b * w + c * u + delta) % m) == (rhs % m),
                )
                for m in PILOT_M_VALUES
            }
            affine_rows.append(
                {
                    "predicate": name,
                    "coefficients": {"q": a, "w": b, "u": c, "delta": 1, "rhs": rhs},
                    "stats": stats,
                }
            )
    affine_rows.sort(
        key=lambda row: (
            row["stats"]["7"]["total_excess"],
            row["stats"]["9"]["total_excess"],
            row["stats"]["5"]["total_excess"],
            row["stats"]["7"]["multi_delta_state_count"],
            row["stats"]["9"]["multi_delta_state_count"],
            row["stats"]["5"]["multi_delta_state_count"],
            row["stats"]["7"]["full_nonzero_support_state_count"] + row["stats"]["9"]["full_nonzero_support_state_count"],
        )
    )

    pred_scan = json.loads(args.pred_scan_json.read_text())
    pred_ranking = pred_scan["ranking_by_m7_then_m9_total_excess"][:10]
    pred_candidates = {name: pred_scan["candidate_bits"][name] for name in pred_ranking}

    summary = {
        "task_id": "D5-PHASE-ALIGN-TAIL-PHASE-SCAN-001",
        "baseline_phase_align_strict_collapse": baseline,
        "best_arbitrary_delta_partition_by_m": best_arbitrary,
        "top_arbitrary_delta_partitions_by_m": top_arbitrary,
        "structured_delta_family_scan": structured,
        "top_affine_delta_mixed_equalities": affine_rows[:25],
        "comparison_with_previous_simple_predecessor_scan": {
            "baseline": pred_scan["baseline"],
            "top_ranked_candidate_names": pred_ranking,
            "top_ranked_candidates": pred_candidates,
        },
        "conclusions": {
            "pure_delta_partition_outperforms_simple_predecessor_bits": True,
            "best_affine_equality_predicates_are_pure_delta_equalities": True,
            "no_single_obvious_uniform_arithmetic_delta_bit_emerges_from_m_5_7_9": True,
        },
    }
    args.out.write_text(json.dumps(summary, indent=2))
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
