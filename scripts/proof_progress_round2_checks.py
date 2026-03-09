#!/usr/bin/env python3
"""Checks supporting proof_progress_suggestion_d_round2.md.

This script uses the published Route E definition from anc/route_e_even.py,
and evaluates two modified variants:

1. primary geometry: use the Case I layer-0 rule for all even m;
2. deleted-extra-family geometry: in the actual Case II rule, remove only the
   added affine Y210-family and keep the remaining Case II points untouched.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from typing import Tuple

ROOT = Path(__file__).resolve().parent
ROUTE_E_PATH = ROOT / "anc" / "route_e_even.py"

spec = importlib.util.spec_from_file_location("routee", ROUTE_E_PATH)
routee = importlib.util.module_from_spec(spec)
sys.modules["routee"] = routee
spec.loader.exec_module(routee)

Triple = Tuple[int, int, int]
Pair = Tuple[int, int]


def p0_point(m: int, i: int, k: int) -> Triple:
    return routee.p0_point(m, i, k)


def bump(v: Triple, direction: int, m: int) -> Triple:
    return routee.bump(v, direction, m)


# ---------------------------------------------------------------------------
# Variant A: primary geometry = Case I layer-0 rule extended to all even m
# ---------------------------------------------------------------------------

def route_e_direction_triple_primary(m: int, v: Triple) -> Triple:
    i, j, k = (x % m for x in v)
    s = (i + j + k) % m
    if s not in (0, 1, 2):
        return (0, 1, 2)
    if s == 1:
        return (1, 0, 2) if i == 0 else (2, 0, 1)
    if s == 2:
        return (2, 1, 0) if j == 0 else (0, 1, 2)

    # Use the current Case I layer-0 rule for all even m.
    if (i, j, k) == (m - 2, 1, 1):
        return (0, 1, 2)
    if (i, j, k) == (m - 2, 2, 0):
        return (2, 0, 1)
    if (i, j, k) == (0, 0, 0):
        return (1, 0, 2)
    if 1 <= i <= m - 3 and (j, k) == (1, (m - 1 - i) % m):
        return (1, 0, 2)
    if (i, j, k) == (m - 1, 2, m - 1):
        return (1, 0, 2)
    if (i, j, k) == (0, 1, m - 1):
        return (0, 2, 1)
    if 1 <= i <= m - 3 and (j, k) == ((m - i) % m, 0):
        return (0, 2, 1)
    if (i, j, k) == (m - 1, 0, 1):
        return (0, 2, 1)
    if i == 0 and 2 <= j <= m - 1 and k == (m - j) % m:
        return (2, 1, 0)
    if (i, j, k) == (1, 0, m - 1):
        return (2, 1, 0)
    return (1, 2, 0)


def color_map_primary(m: int, color: int, v: Triple) -> Triple:
    return bump(v, route_e_direction_triple_primary(m, v)[color], m)


def return_map_primary(m: int, color: int, i: int, k: int) -> Pair:
    v = p0_point(m, i, k)
    for _ in range(m):
        v = color_map_primary(m, color, v)
    i2, _, k2 = v
    return i2 % m, k2 % m


def T1_primary(m: int, x: int) -> int:
    i, k = x, 0
    while True:
        i, k = return_map_primary(m, 1, i, k)
        u, t = (i - k) % m, k % m
        if t == 0:
            return u


def T0_primary(m: int, x: int) -> int:
    i, k = x, 0
    while True:
        i, k = return_map_primary(m, 0, i, k)
        u, t = (i + 2 * k) % m, k % m
        if t == 0:
            return u


# ---------------------------------------------------------------------------
# Variant B: actual Case II rule with only the added affine family deleted
# ---------------------------------------------------------------------------

def route_e_direction_triple_deleted_extra(m: int, v: Triple) -> Triple:
    i, j, k = (x % m for x in v)
    s = (i + j + k) % m
    if s not in (0, 1, 2):
        return (0, 1, 2)
    if s == 1:
        return (1, 0, 2) if i == 0 else (2, 0, 1)
    if s == 2:
        return (2, 1, 0) if j == 0 else (0, 1, 2)

    if m % 6 in (0, 2):
        return routee.route_e_direction_triple(m, v)

    # Actual Case II rule, but remove only the added Y210-family
    # { (1,j,m-1-j): 2<=j<=m-2 } and its endpoints (2,0,m-2), (2,m-1,m-1).
    if (i, j, k) == (0, 0, 0):
        return (1, 0, 2)
    if 2 <= i <= m - 3 and (j, k) == (1, (m - 1 - i) % m):
        return (1, 0, 2)
    if (i, j, k) == (m - 1, 2, m - 1):
        return (1, 0, 2)

    if (i, j, k) == (0, 1, m - 1):
        return (0, 2, 1)
    if 2 <= i <= m - 3 and (j, k) == ((m - i) % m, 0):
        return (0, 2, 1)
    if (i, j, k) == (m - 1, 0, 1):
        return (0, 2, 1)

    if i == 0 and 2 <= j <= m - 1 and k == (m - j) % m:
        return (2, 1, 0)
    if (i, j, k) == (1, 0, m - 1):
        return (2, 1, 0)

    # Keep the remaining Case II special points.
    if (i, j, k) in {(1, 1, m - 2), (m - 2, 1, 1)}:
        return (0, 1, 2)
    if (i, j, k) in {(1, m - 1, 0), (m - 2, 2, 0)}:
        return (2, 0, 1)

    return (1, 2, 0)


def color_map_deleted_extra(m: int, color: int, v: Triple) -> Triple:
    return bump(v, route_e_direction_triple_deleted_extra(m, v)[color], m)


def return_map_deleted_extra(m: int, color: int, i: int, k: int) -> Pair:
    v = p0_point(m, i, k)
    for _ in range(m):
        v = color_map_deleted_extra(m, color, v)
    i2, _, k2 = v
    return i2 % m, k2 % m


def T1_deleted_extra(m: int, x: int) -> int:
    i, k = x, 0
    while True:
        i, k = return_map_deleted_extra(m, 1, i, k)
        u, t = (i - k) % m, k % m
        if t == 0:
            return u


def T0_deleted_extra(m: int, x: int) -> int:
    i, k = x, 0
    while True:
        i, k = return_map_deleted_extra(m, 0, i, k)
        u, t = (i + 2 * k) % m, k % m
        if t == 0:
            return u


def single_cycle(vals):
    n = len(vals)
    seen = [False] * n
    x = 0
    count = 0
    while not seen[x]:
        seen[x] = True
        count += 1
        x = vals[x]
        if count > n + 1:
            return False
    return x == 0 and count == n


def cycle_count(vals):
    n = len(vals)
    seen = [False] * n
    cycles = 0
    for x in range(n):
        if seen[x]:
            continue
        y = x
        while not seen[y]:
            seen[y] = True
            y = vals[y]
        cycles += 1
    return cycles


def main() -> None:
    print("Checking primary geometry on m = 10,16,...,100")
    for m in range(10, 101, 6):
        vals1 = [T1_primary(m, x) for x in range(m)]
        expect1 = [2 if x == 0 else (x + 3 if 1 <= x <= m - 4 else (1 if x == m - 3 else (0 if x == m - 2 else 3))) for x in range(m)]
        assert vals1 == expect1
        assert cycle_count(vals1) == 3

        vals0 = [T0_primary(m, x) for x in range(m)]
        assert single_cycle(vals0)
    print("  OK: primary T1 formula and 3-cycle obstruction; primary T0 single cycle")

    print("Checking deleted-extra-family formulas on m = 10,16,...,100")
    for m in range(10, 101, 6):
        vals1 = [T1_deleted_extra(m, x) for x in range(m)]
        expect1 = [
            2 if x == 0 else
            3 if x == 1 else
            4 if x == 2 else
            x + 3 if 3 <= x <= m - 4 else
            1 if x == m - 3 else
            0 if x == m - 2 else
            3
            for x in range(m)
        ]
        assert vals1 == expect1
        assert vals1[1] == vals1[m - 1] == 3

        vals0 = [T0_deleted_extra(m, x) for x in range(m)]
        expect0 = [
            (m - 2) if x == 0 else
            4 if x in (1, 2) else
            x + 2 if 3 <= x <= m - 6 else
            (m - 1) if x in (m - 5, m - 4) else
            2 if x == m - 3 else
            1 if x == m - 2 else
            0
            for x in range(m)
        ]
        assert vals0 == expect0
        assert vals0[1] == vals0[2] == 4
    print("  OK: deleted-extra-family formulas and noninjectivity patterns")


if __name__ == "__main__":
    main()
