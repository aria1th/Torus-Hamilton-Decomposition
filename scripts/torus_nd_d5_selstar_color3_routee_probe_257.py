#!/usr/bin/env python3
"""Probe a Route-E-style finite-defect factor for the Sel* color-3 first return.

The candidate factor is

    Phi_3(x) = (p0(x), p1(x), p2(x), M0(x))

on P0 = {Sigma = 0}, where

    p_i(x) = x_{i-1} + x_{i+2}  (mod m)
    M0(x) = 1[x_0 = m-1].

This script checks that, for the color-3 first return R_3^*:

1. the only nondeterministic Phi_3-states are two affine defect lines;
2. each bad Phi_3-state has an explicit raw fiber of size m-1;
3. inside that raw fiber, exactly one point follows the exceptional branch.

Outputs:
- RoundY/checks/d5_257_selstar_color3_routee_probe_summary.json
- RoundY/checks/d5_257_selstar_color3_routee_probe/per_modulus.json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import DefaultDict

from torus_nd_d5_selector_star_common_119 import build_R_data, selector_perm_star

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_257_selstar_color3_routee_probe_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_257_selstar_color3_routee_probe"


State = tuple[int, int, int, int, int]
FactorState = tuple[int, int, int, int]


def make_p0_state(x4: tuple[int, int, int, int], m: int) -> State:
    return x4 + ((-sum(x4)) % m,)


def pair_sums(x: State, m: int) -> tuple[int, int, int, int, int]:
    return tuple((x[(i - 1) % 5] + x[(i + 2) % 5]) % m for i in range(5))


def m0_bit(x: State, m: int) -> int:
    return int(x[0] == m - 1)


def factor_state(x: State, m: int) -> FactorState:
    p = pair_sums(x, m)
    return (p[0], p[1], p[2], m0_bit(x, m))


def line_a_state(m: int, t: int) -> FactorState:
    return (m - 4, t % m, (2 - t) % m, 0)


def line_b_state(m: int, s: int) -> FactorState:
    return (s % m, (1 - s) % m, m - 3, 0)


def line_a_successors(m: int, t: int) -> set[FactorState]:
    alt_bit = 1 if t % m == (m - 3) % m else 0
    return {
        (m - 2, (t - 3) % m, (4 - t) % m, 0),
        (m - 2, (t - 2) % m, (3 - t) % m, alt_bit),
    }


def line_b_successors(m: int, s: int) -> set[FactorState]:
    return {
        ((s + 2) % m, (-s - 1) % m, m - 2, 0),
        ((s + 2) % m, (-s - 1) % m, m - 2, 1),
    }


def line_a_raw_point(m: int, t: int, a: int) -> State:
    return (a % m, (4 - t) % m, m - 2, (t - a) % m, m - 2)


def line_b_raw_point(m: int, s: int, a: int) -> State:
    return (a % m, m - 1, (s + 2) % m, (1 - s - a) % m, m - 2)


def dominant_exact_diff(per_key_rows: dict[FactorState, list[tuple[State, FactorState]]], m: int) -> tuple[list[int], int]:
    counts: Counter[tuple[int, int, int, int]] = Counter()
    for key, rows in per_key_rows.items():
        succs = {succ for _, succ in rows}
        if len(succs) != 1:
            continue
        succ = next(iter(succs))
        diff = (
            (succ[0] - key[0]) % m,
            (succ[1] - key[1]) % m,
            (succ[2] - key[2]) % m,
            succ[3] - key[3],
        )
        counts[diff] += 1
    diff, count = counts.most_common(1)[0]
    return list(diff), count


def analyse_modulus(m: int) -> dict[str, object]:
    pts, _perm, images4 = build_R_data(m, 3, selector_perm_star)
    xs = [make_p0_state(x[:4], m) for x in pts]
    ys = [make_p0_state(tuple(int(v) for v in images4[idx]), m) for idx in range(len(pts))]

    per_key_rows: DefaultDict[FactorState, list[tuple[State, FactorState]]] = defaultdict(list)
    for x, y in zip(xs, ys):
        per_key_rows[factor_state(x, m)].append((x, factor_state(y, m)))

    nondet = {key: rows for key, rows in per_key_rows.items() if len({succ for _, succ in rows}) > 1}
    expected_line_a = {line_a_state(m, t) for t in range(m) if t != m - 2}
    expected_line_b = {line_b_state(m, s) for s in range(m) if s != m - 4}
    expected_nondet = expected_line_a | expected_line_b

    line_a_ok = True
    line_b_ok = True
    line_a_examples: list[dict[str, object]] = []
    line_b_examples: list[dict[str, object]] = []
    line_a_total_raw = 0
    line_b_total_raw = 0

    for t in sorted(range(m)):
        if t == m - 2:
            continue
        key = line_a_state(m, t)
        rows = nondet.get(key)
        if rows is None:
            line_a_ok = False
            continue
        succs = {succ for _, succ in rows}
        expected_succs = line_a_successors(m, t)
        if succs != expected_succs:
            line_a_ok = False
        raw_points = {x for x, _ in rows}
        expected_raw = {line_a_raw_point(m, t, a) for a in range(m) if a != m - 1}
        if raw_points != expected_raw:
            line_a_ok = False
        exc = line_a_raw_point(m, t, t + 1)
        exc_hits = [(x, succ) for x, succ in rows if x == exc]
        default_branch = (m - 2, (t - 3) % m, (4 - t) % m, 0)
        exceptional_branch = next(iter(expected_succs - {default_branch}))
        if len(exc_hits) != 1 or exc_hits[0][1] != exceptional_branch:
            line_a_ok = False
        for x, succ in rows:
            if x != exc and succ != default_branch:
                line_a_ok = False
                break
        line_a_total_raw += len(rows)
        if len(line_a_examples) < 3:
            line_a_examples.append(
                {
                    "state": list(key),
                    "default_successor": list(default_branch),
                    "exceptional_successor": list(exceptional_branch),
                    "exceptional_raw_point": list(exc),
                }
            )

    for s in sorted(range(m)):
        if s == m - 4:
            continue
        key = line_b_state(m, s)
        rows = nondet.get(key)
        if rows is None:
            line_b_ok = False
            continue
        succs = {succ for _, succ in rows}
        expected_succs = line_b_successors(m, s)
        if succs != expected_succs:
            line_b_ok = False
        raw_points = {x for x, _ in rows}
        expected_raw = {line_b_raw_point(m, s, a) for a in range(m) if a != m - 1}
        if raw_points != expected_raw:
            line_b_ok = False
        exc = line_b_raw_point(m, s, m - 2)
        exc_hits = [(x, succ) for x, succ in rows if x == exc]
        default_branch = ((s + 2) % m, (-s - 1) % m, m - 2, 0)
        exceptional_branch = ((s + 2) % m, (-s - 1) % m, m - 2, 1)
        if len(exc_hits) != 1 or exc_hits[0][1] != exceptional_branch:
            line_b_ok = False
        for x, succ in rows:
            if x != exc and succ != default_branch:
                line_b_ok = False
                break
        line_b_total_raw += len(rows)
        if len(line_b_examples) < 3:
            line_b_examples.append(
                {
                    "state": list(key),
                    "default_successor": list(default_branch),
                    "exceptional_successor": list(exceptional_branch),
                    "exceptional_raw_point": list(exc),
                }
            )

    dominant_diff, dominant_count = dominant_exact_diff(per_key_rows, m)

    return {
        "m": m,
        "factor": "Phi3=(p0,p1,p2,M0)",
        "nondet_state_count": len(nondet),
        "expected_nondet_state_count": 2 * m - 2,
        "nondet_equals_two_affine_lines": set(nondet) == expected_nondet,
        "line_A_state_count": len(expected_line_a),
        "line_B_state_count": len(expected_line_b),
        "line_A_formula_verified": line_a_ok,
        "line_B_formula_verified": line_b_ok,
        "line_A_total_raw_points": line_a_total_raw,
        "line_B_total_raw_points": line_b_total_raw,
        "raw_defect_total": line_a_total_raw + line_b_total_raw,
        "expected_raw_defect_total": 2 * (m - 1) * (m - 1),
        "dominant_exact_diff": dominant_diff,
        "dominant_exact_diff_count": dominant_count,
        "line_A_examples": line_a_examples,
        "line_B_examples": line_b_examples,
        "nondet_states": [list(key) for key in sorted(nondet)],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Route-E-style probe for Sel* color-3 first return.")
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=DEFAULT_SUMMARY,
        help=f"summary JSON path (default: {DEFAULT_SUMMARY})",
    )
    parser.add_argument(
        "--detail-dir",
        type=Path,
        default=DEFAULT_DETAIL_DIR,
        help=f"detail output directory (default: {DEFAULT_DETAIL_DIR})",
    )
    parser.add_argument(
        "--moduli",
        type=int,
        nargs="*",
        default=[9, 11, 13, 15, 17],
        help="odd moduli to check",
    )
    args = parser.parse_args()

    per_modulus = {str(m): analyse_modulus(m) for m in args.moduli}
    summary = {
        "task": "d5_257_selstar_color3_routee_probe",
        "selector": "Sel*",
        "color": 3,
        "factor": "Phi3=(p0,p1,p2,M0)",
        "checked_moduli": args.moduli,
        "all_nondet_sets_are_two_affine_lines": all(
            payload["nondet_equals_two_affine_lines"] for payload in per_modulus.values()
        ),
        "all_line_A_formulas_verified": all(payload["line_A_formula_verified"] for payload in per_modulus.values()),
        "all_line_B_formulas_verified": all(payload["line_B_formula_verified"] for payload in per_modulus.values()),
        "all_raw_defect_totals_match": all(
            payload["raw_defect_total"] == payload["expected_raw_defect_total"] for payload in per_modulus.values()
        ),
        "dominant_exact_diff_by_modulus": {
            m: payload["dominant_exact_diff"] for m, payload in per_modulus.items()
        },
        "conclusion": (
            "For Sel* color 3, the best m^3-scale near-factor Phi3=(p0,p1,p2,M0) is nondeterministic only on "
            "two affine defect lines in the b=0 slice. Each bad factor state has raw fiber size m-1, and in that "
            "fiber exactly one explicit raw point follows the exceptional branch while the remaining m-2 points follow "
            "the default affine branch. This is strong evidence that the live color-3 route should be treated as a "
            "D3 Route-E-style finite-defect affine-itinerary / splice theorem rather than as a cyclic transport theorem."
        ),
    }

    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summary, indent=2))
    (args.detail_dir / "per_modulus.json").write_text(json.dumps(per_modulus, indent=2))
    print(args.summary_output)
    print(args.detail_dir / "per_modulus.json")


if __name__ == "__main__":
    main()
