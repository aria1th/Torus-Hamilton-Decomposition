#!/usr/bin/env python3
"""Checks the manuscript's first-return formulas for Route E.

This script complements route_e_even.py.
The main verifier checks

    Route E definition  ->  displayed return maps  ->  cycle structure on P0 / V.

This script verifies the next bridge in the manuscript:

    displayed return maps  ->  first-return maps T_c and times rho_c.

For each even m in a chosen range it compares the closed-form first-return data
(T0,T1,T2,rho0,rho1,rho2) with the actual first-return dynamics of the displayed
return maps R0,R1,R2 on the transversals used in the paper.
"""

from __future__ import annotations

import argparse
from typing import Callable, List, Sequence, Tuple

import route_e_even as ree


Pair = Tuple[int, int]


def first_return_color1(m: int, x: int) -> Pair:
    i, k = x % m, 0
    t = 0
    while True:
        i, k = ree.R1_formula(m, i, k)
        t += 1
        if k % m == 0:
            return i % m, t



def first_return_color0(m: int, x: int) -> Pair:
    i, k = x % m, 0
    t = 0
    while True:
        i, k = ree.R0_formula(m, i, k)
        t += 1
        if k % m == 0:
            return i % m, t



def first_return_color2(m: int, x: int) -> Pair:
    # The manuscript uses working coordinates (x,y)=(i, i+k), with transversal y=0.
    # So the starting point on P0 is (i,k)=(x,-x).
    i, k = x % m, (-x) % m
    t = 0
    while True:
        i, k = ree.R2_formula(m, i, k)
        t += 1
        if (i + k) % m == 0:
            return i % m, t



def orbit(T: Callable[[int, int], int], m: int, start: int = 0) -> List[int]:
    out: List[int] = []
    x = start % m
    seen = set()
    while x not in seen:
        seen.add(x)
        out.append(x)
        x = T(m, x) % m
    if x != start % m:
        raise AssertionError("first-return map did not close at the chosen start")
    return out



def verify_m(m: int) -> None:
    # Pointwise comparison with the formulas recorded in route_e_even.py.
    for x in range(m):
        t0, r0 = first_return_color0(m, x)
        if (t0, r0) != (ree.T0_formula(m, x) % m, ree.rho0_formula(m, x)):
            raise AssertionError(
                f"m={m}, color=0, x={x}: actual {(t0,r0)} != formula {(ree.T0_formula(m,x)%m, ree.rho0_formula(m,x))}"
            )
        t1, r1 = first_return_color1(m, x)
        if (t1, r1) != (ree.T1_formula(m, x) % m, ree.rho1_formula(m, x)):
            raise AssertionError(
                f"m={m}, color=1, x={x}: actual {(t1,r1)} != formula {(ree.T1_formula(m,x)%m, ree.rho1_formula(m,x))}"
            )
        t2, r2 = first_return_color2(m, x)
        if (t2, r2) != (ree.T2_formula(m, x) % m, ree.rho2_formula(m, x)):
            raise AssertionError(
                f"m={m}, color=2, x={x}: actual {(t2,r2)} != formula {(ree.T2_formula(m,x)%m, ree.rho2_formula(m,x))}"
            )

    # Global cycle-structure consequences used in the main proof.
    if len(orbit(ree.T0_formula, m)) != m:
        raise AssertionError(f"m={m}: T0 is not an m-cycle")
    if len(orbit(ree.T1_formula, m)) != m:
        raise AssertionError(f"m={m}: T1 is not an m-cycle")
    if len(orbit(ree.T2_formula, m)) != m:
        raise AssertionError(f"m={m}: T2 is not an m-cycle")

    if sum(ree.rho0_formula(m, x) for x in range(m)) != m * m:
        raise AssertionError(f"m={m}: sum rho0 != m^2")
    if sum(ree.rho1_formula(m, x) for x in range(m)) != m * m:
        raise AssertionError(f"m={m}: sum rho1 != m^2")
    if sum(ree.rho2_formula(m, x) for x in range(m)) != m * m:
        raise AssertionError(f"m={m}: sum rho2 != m^2")



def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the manuscript's first-return formulas for Route E.")
    parser.add_argument("--m-min", type=int, default=6, help="smallest even m to test (default: 6)")
    parser.add_argument("--m-max", type=int, default=120, help="largest even m to test (default: 120)")
    args = parser.parse_args(argv)

    if args.m_min > args.m_max:
        raise SystemExit("--m-min must be <= --m-max")

    tested: List[int] = []
    for m in range(args.m_min, args.m_max + 1):
        if m % 2 == 0 and m >= 6:
            verify_m(m)
            tested.append(m)

    if not tested:
        raise SystemExit("no even m >= 6 in the requested range")

    print("Route E first-return checks: PASS")
    print(f"tested even m = {tested[0]}..{tested[-1]} (step 2), count = {len(tested)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
