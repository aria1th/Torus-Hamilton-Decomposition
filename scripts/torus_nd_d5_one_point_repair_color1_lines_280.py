#!/usr/bin/env python3
"""Check the explicit color-1 line obstruction inside the d5_279 repaired family.

For odd moduli not divisible by 3, the color-1 P0 first return of the d5_279
repaired family has an explicit invariant line family

    L_{a,b}(t) = (7-a-3b-3t, t, -7+2b+2t, a, b),

with a,b in {0,...,m-2}.  Along each such line the P0 return acts by t -> t+1.
This yields (m-1)^2 disjoint m-cycles on P0, hence (m-1)^2 disjoint m^2-cycles
for the full color-1 torus map.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from torus_nd_d5_one_point_repair_279 import load_solution, repaired_selector


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = (
    REPO_ROOT / "RoundY" / "checks" / "d5_280_one_point_repair_color1_line_obstruction_summary.json"
)
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_280_one_point_repair_color1_line_obstruction"


def color_step(
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    solution: list[int],
    m: int,
    color: int,
    point: tuple[int, int, int, int, int],
) -> tuple[int, int, int, int, int]:
    cur = list(point)
    direction = repaired_selector(keys, key_to_idx, solution, m, point)[color]
    cur[direction] = (cur[direction] + 1) % m
    return tuple(cur)


def p0_return(
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    solution: list[int],
    m: int,
    point: tuple[int, int, int, int, int],
) -> tuple[int, int, int, int, int]:
    cur = point
    for _ in range(m):
        cur = color_step(keys, key_to_idx, solution, m, 1, cur)
    return cur


def line_point(m: int, a: int, b: int, t: int) -> tuple[int, int, int, int, int]:
    return (
        (7 - a - 3 * b - 3 * t) % m,
        t % m,
        (-7 + 2 * b + 2 * t) % m,
        a,
        b,
    )


def cycle_histogram_on_p0(
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    solution: list[int],
    m: int,
) -> dict[str, int]:
    states = [point for point in itertools.product(range(m), repeat=5) if sum(point) % m == 0]
    idx = {state: i for i, state in enumerate(states)}
    perm = [0] * len(states)
    for i, state in enumerate(states):
        perm[i] = idx[p0_return(keys, key_to_idx, solution, m, state)]
    seen = [False] * len(states)
    hist: dict[int, int] = {}
    for start in range(len(states)):
        if seen[start]:
            continue
        cur = start
        size = 0
        while not seen[cur]:
            seen[cur] = True
            cur = perm[cur]
            size += 1
        hist[size] = hist.get(size, 0) + 1
    return {str(length): count for length, count in sorted(hist.items())}


def full_cycle_histogram(
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    solution: list[int],
    m: int,
) -> dict[str, int]:
    states = list(itertools.product(range(m), repeat=5))
    idx = {state: i for i, state in enumerate(states)}
    perm = [0] * len(states)
    for i, state in enumerate(states):
        perm[i] = idx[color_step(keys, key_to_idx, solution, m, 1, state)]
    seen = [False] * len(states)
    hist: dict[int, int] = {}
    for start in range(len(states)):
        if seen[start]:
            continue
        cur = start
        size = 0
        while not seen[cur]:
            seen[cur] = True
            cur = perm[cur]
            size += 1
        hist[size] = hist.get(size, 0) + 1
    return {str(length): count for length, count in sorted(hist.items())}


def verify_line_formula(
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    solution: list[int],
    m: int,
) -> tuple[bool, dict[str, object] | None]:
    for a in range(m - 1):
        for b in range(m - 1):
            for t in range(m):
                point = line_point(m, a, b, t)
                image = p0_return(keys, key_to_idx, solution, m, point)
                expected = line_point(m, a, b, t + 1)
                if image != expected:
                    return False, {
                        "a": a,
                        "b": b,
                        "t": t,
                        "point": list(point),
                        "image": list(image),
                        "expected": list(expected),
                    }
    return True, None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check the explicit color-1 line obstruction in the d5_279 repaired family."
    )
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    parser.add_argument("--line-moduli", nargs="*", type=int, default=[7, 11, 13, 17, 19])
    parser.add_argument("--failure-moduli", nargs="*", type=int, default=[9, 15])
    parser.add_argument("--full-profile-moduli", nargs="*", type=int, default=[7, 11, 13, 17])
    args = parser.parse_args()

    keys, key_to_idx, solution = load_solution()

    line_rows = {
        str(m): verify_line_formula(keys, key_to_idx, solution, m)
        for m in args.line_moduli
    }
    failure_rows = {
        str(m): verify_line_formula(keys, key_to_idx, solution, m)
        for m in args.failure_moduli
    }
    p0_histograms = {
        str(m): cycle_histogram_on_p0(keys, key_to_idx, solution, m)
        for m in args.line_moduli
    }
    full_histograms = {
        str(m): full_cycle_histogram(keys, key_to_idx, solution, m)
        for m in args.full_profile_moduli
    }

    summary = {
        "task": "d5_280_one_point_repair_color1_line_obstruction",
        "family": "d5_279 one-point repaired five-color family",
        "color": 1,
        "line_formula": (
            "L_{a,b}(t) = (7-a-3b-3t, t, -7+2b+2t, a, b) on P0, "
            "with a,b in {0,...,m-2}"
        ),
        "verified_nonmultiple_of_3_moduli": args.line_moduli,
        "verified_formula_on_nonmultiple_of_3_moduli": all(ok for ok, _ in line_rows.values()),
        "checked_multiple_of_3_failures": {
            modulus: witness
            for modulus, (ok, witness) in failure_rows.items()
            if not ok
        },
        "p0_short_m_cycle_count": {
            str(m): p0_histograms[str(m)].get(str(m), 0)
            for m in args.line_moduli
        },
        "full_short_m2_cycle_count": {
            str(m): full_histograms[str(m)].get(str(m**2), 0)
            for m in args.full_profile_moduli
        },
        "conclusion": (
            "For checked odd moduli not divisible by 3, the d5_279 repaired family's "
            "color-1 P0 return preserves an explicit (m-1)^2-family of affine lines "
            "and acts on each line by t -> t+1. Therefore the current repaired family "
            "still contains (m-1)^2 disjoint color-1 cycles of length m^2 on the full torus."
        ),
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.detail_dir / "per_modulus.json").write_text(
        json.dumps(
            {
                "line_moduli": {
                    modulus: {
                        "formula_exact": ok,
                        "witness": witness,
                        "p0_histogram": p0_histograms[modulus],
                        "full_histogram": full_histograms.get(modulus),
                    }
                    for modulus, (ok, witness) in line_rows.items()
                },
                "failure_moduli": {
                    modulus: {"formula_exact": ok, "witness": witness}
                    for modulus, (ok, witness) in failure_rows.items()
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
