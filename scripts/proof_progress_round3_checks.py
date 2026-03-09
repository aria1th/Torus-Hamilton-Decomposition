#!/usr/bin/env python3
"""Checks supporting proof_progress_suggestion_d_round3.md.

The script verifies two finite-range claims against the actual Definition-4 rule
and the two modified variants discussed in the note:

1. primary geometry on m = 10,16,...,100:
   - T1_primary has exactly three cycles for m ≡ 4 (mod 6);
   - T0_primary is a single cycle.
2. deleted-extra-family geometry on m = 10,16,...,250:
   - T1_deleted(1) = T1_deleted(m-1) = 3;
   - T0_deleted(1) = T0_deleted(2) = 4.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
ROUTE_E_PATH = ROOT / "anc" / "route_e_even.py"

spec = importlib.util.spec_from_file_location("routee", ROUTE_E_PATH)
routee = importlib.util.module_from_spec(spec)
sys.modules["routee"] = routee
spec.loader.exec_module(routee)

Triple = Tuple[int, int, int]
Pair = Tuple[int, int]


def bump(v: Triple, direction: int, m: int) -> Triple:
    return routee.bump(v, direction, m)


def p0_point(m: int, i: int, k: int) -> Triple:
    return routee.p0_point(m, i, k)


# ---------------------------------------------------------------------------
# Variant A: primary geometry = Case I layer-0 rule for all even m
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
    for _ in range(5 * m):
        i, k = return_map_primary(m, 1, i, k)
        u, t = (i - k) % m, k % m
        if t == 0:
            return u
    raise RuntimeError("no first return in T1_primary")


def T0_primary(m: int, x: int) -> int:
    i, k = x, 0
    for _ in range(5 * m):
        i, k = return_map_primary(m, 0, i, k)
        u, t = (i + 2 * k) % m, k % m
        if t == 0:
            return u
    raise RuntimeError("no first return in T0_primary")


# ---------------------------------------------------------------------------
# Variant B: actual Case II rule with only the added family deleted
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

    # Keep the actual Case II rule, but revert only the added family
    # {(1,j,m-1-j): 2 <= j <= m-2} and its endpoints
    # (2,0,m-2), (2,m-1,m-1) to the default triple 120.
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

    # Keep the remaining Case II isolated points.
    if (i, j, k) in {(1, 1, m - 2), (m - 2, 1, 1)}:
        return (0, 1, 2)
    if (i, j, k) in {(1, m - 1, 0), (m - 2, 2, 0)}:
        return (2, 0, 1)

    return (1, 2, 0)


def color_map_deleted(m: int, color: int, v: Triple) -> Triple:
    return bump(v, route_e_direction_triple_deleted_extra(m, v)[color], m)


def return_map_deleted(m: int, color: int, i: int, k: int) -> Pair:
    v = p0_point(m, i, k)
    for _ in range(m):
        v = color_map_deleted(m, color, v)
    i2, _, k2 = v
    return i2 % m, k2 % m


def T1_deleted(m: int, x: int) -> int:
    i, k = x, 0
    for _ in range(5 * m):
        i, k = return_map_deleted(m, 1, i, k)
        u, t = (i - k) % m, k % m
        if t == 0:
            return u
    raise RuntimeError("no first return in T1_deleted")


def T0_deleted(m: int, x: int) -> int:
    i, k = x, 0
    for _ in range(5 * m):
        i, k = return_map_deleted(m, 0, i, k)
        u, t = (i + 2 * k) % m, k % m
        if t == 0:
            return u
    raise RuntimeError("no first return in T0_deleted")


# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------

def cycle_count(vals: List[int]) -> int:
    n = len(vals)
    seen = [False] * n
    out = 0
    for x in range(n):
        if seen[x]:
            continue
        y = x
        while not seen[y]:
            seen[y] = True
            y = vals[y]
        out += 1
    return out


def main() -> None:
    print("Checking primary geometry on m = 10,16,...,100")
    for m in range(10, 101, 6):
        vals1 = [T1_primary(m, x) for x in range(m)]
        assert cycle_count(vals1) == 3

        vals0 = [T0_primary(m, x) for x in range(m)]
        assert cycle_count(vals0) == 1
    print("  OK: primary color-1 obstruction and primary color-0 Hamiltonicity")

    print("Checking deleted-extra-family witnesses on m = 10,16,...,250")
    for m in range(10, 251, 6):
        assert T1_deleted(m, 1) == 3
        assert T1_deleted(m, m - 1) == 3
        assert T0_deleted(m, 1) == 4
        assert T0_deleted(m, 2) == 4
    print("  OK: explicit noninjectivity witnesses for colors 1 and 0")

    print("All round-3 checks passed.")


if __name__ == "__main__":
    main()
