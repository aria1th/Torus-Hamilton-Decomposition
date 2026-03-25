#!/usr/bin/env python3
"""Deterministic Route E utilities for even m >= 6.

This module has three layers of functionality.

1. theorem_certificate(m):
   Uses the closed-form first-return formulas proved in the manuscript.
   This is the quick path: O(m) time, O(1) extra space.

2. validate_return_maps_against_definition(m):
   Recomputes the return maps from Definition 4 and compares them with the
   Appendix-A formulas. This is O(m^3) if done naively, but here only O(m^2 * m)
   on P_0 and intended as a regression check.

3. validate_full_color_cycles(m):
   Directly computes the three color maps on V=(Z/mZ)^3 and checks that each is a
   single Hamilton cycle. This is O(m^3) in memory/time and is meant only for
   exact finite verification, not for the theorem path.

The code is entirely deterministic and does not use randomness.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Sequence, Tuple

Pair = Tuple[int, int]
Triple = Tuple[int, int, int]


@dataclass(frozen=True)
class Certificate:
    m: int
    case: str
    T0_cycle_order: List[int]
    T1_cycle_order: List[int]
    T2_cycle_order: List[int]
    rho0_sum: int
    rho1_sum: int
    rho2_sum: int


def mod(x: int, m: int) -> int:
    return x % m


# ---------------------------------------------------------------------------
# Direct Route E rule from the manuscript
# ---------------------------------------------------------------------------

def layer(v: Triple, m: int) -> int:
    i, j, k = v
    return (i + j + k) % m


def route_e_direction_triple(m: int, v: Triple) -> Triple:
    """Return (d0,d1,d2) for Route E at vertex v.

    Coordinates and directions are 0-based: direction r means v -> v + e_r.
    """
    if m < 6 or m % 2 != 0:
        raise ValueError("Route E is only defined here for even m >= 6.")

    i, j, k = (x % m for x in v)
    s = (i + j + k) % m

    if s not in (0, 1, 2):
        return (0, 1, 2)

    if s == 1:
        return (1, 0, 2) if i == 0 else (2, 0, 1)

    if s == 2:
        return (2, 1, 0) if j == 0 else (0, 1, 2)

    # s == 0
    if m % 6 in (0, 2):
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

    # m % 6 == 4
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
    if i == 1 and 2 <= j <= m - 2 and k == (m - 1 - j) % m:
        return (2, 1, 0)
    if (i, j, k) == (2, 0, m - 2):
        return (2, 1, 0)
    if (i, j, k) == (2, m - 1, m - 1):
        return (2, 1, 0)

    if (i, j, k) in {(1, 1, m - 2), (m - 2, 1, 1)}:
        return (0, 1, 2)
    if (i, j, k) in {(1, m - 1, 0), (m - 2, 2, 0)}:
        return (2, 0, 1)

    return (1, 2, 0)


def bump(v: Triple, direction: int, m: int) -> Triple:
    i, j, k = v
    if direction == 0:
        return ((i + 1) % m, j, k)
    if direction == 1:
        return (i, (j + 1) % m, k)
    if direction == 2:
        return (i, j, (k + 1) % m)
    raise ValueError("direction must be 0,1,2")


def color_map_from_definition(m: int, color: int, v: Triple) -> Triple:
    return bump(v, route_e_direction_triple(m, v)[color], m)


# ---------------------------------------------------------------------------
# P_0 parameterization and closed-form Appendix-A return maps
# ---------------------------------------------------------------------------

def p0_point(m: int, i: int, k: int) -> Triple:
    return (i % m, (-i - k) % m, k % m)


def return_map_from_definition(m: int, color: int, i: int, k: int) -> Pair:
    v = p0_point(m, i, k)
    for _ in range(m):
        v = color_map_from_definition(m, color, v)
    i2, _, k2 = v
    return i2 % m, k2 % m


def R0_formula(m: int, i: int, k: int) -> Pair:
    i %= m
    k %= m
    if m % 6 in (0, 2):
        if (i, k) == (0, 0):
            return (i - 2) % m, k
        if (i, k) == (1, m - 1):
            return (i - 3) % m, (k + 3) % m
        if (i, k) == (m - 2, 0):
            return (i - 2) % m, (k + 2) % m
        if (i, k) == (m - 1, 1):
            return (i - 1) % m, k
        if (i + k) % m == 1 and (i, k) != (1, 0):
            return (i - 3) % m, (k + 2) % m
        if (k == 0 and 1 <= i <= m - 3) or (i, k) in {(0, m - 1), (m - 2, 1)}:
            return (i - 1) % m, (k + 1) % m
        return (i - 2) % m, (k + 1) % m

    if (i, k) == (0, 0):
        return (i - 2) % m, k
    if (i, k) == (m - 1, 1):
        return (i - 1) % m, k
    if (i, k) in {(1, m - 1), (2, m - 2)}:
        return (i - 3) % m, (k + 3) % m
    if (i == 1 and 0 <= k <= m - 3) or (i, k) in {(2, m - 1), (m - 2, 0)}:
        return (i - 2) % m, (k + 2) % m
    if (i + k) % m == 1 and (i, k) not in {(1, 0), (2, m - 1)}:
        return (i - 3) % m, (k + 2) % m
    if (k == 0 and 2 <= i <= m - 3) or (i, k) in {(0, m - 1), (1, m - 2), (m - 2, 1)}:
        return (i - 1) % m, (k + 1) % m
    return (i - 2) % m, (k + 1) % m


def R1_formula(m: int, i: int, k: int) -> Pair:
    i %= m
    k %= m
    if m % 6 in (0, 2):
        if (((i + k) % m == m - 1 and 1 <= i <= m - 3)
                or (i, k) in {(0, 0), (m - 2, 0), (m - 1, m - 1)}):
            return (i + 2) % m, k
        if ((i == 0 and 1 <= k <= m - 2) or (i, k) in {(1, m - 1), (m - 2, 1)}):
            return (i + 1) % m, k
        return (i + 1) % m, (k + 1) % m

    if (((i + k) % m == m - 1 and 2 <= i <= m - 3)
            or (i, k) in {(0, 0), (1, 0), (m - 2, 0), (m - 1, m - 1)}):
        return (i + 2) % m, k
    if ((i == 0 and 1 <= k <= m - 2)
            or (i == 1 and 1 <= k <= m - 1)
            or (i, k) in {(2, m - 2), (2, m - 1), (m - 2, 1)}):
        return (i + 1) % m, k
    return (i + 1) % m, (k + 1) % m


def R2_formula(m: int, i: int, k: int) -> Pair:
    i %= m
    k %= m
    if (i, k) == (2, 0):
        return (i + 1) % m, (k - 3) % m
    if (i + k) % m == 1 and (i, k) not in {(1, 0), (m - 1, 2)}:
        return (i + 2) % m, (k - 3) % m
    if (((k % m) == ((m - 1 - i) % m) and i != m - 1) or (i, k) == (m - 1, m - 1)):
        return i, (k - 1) % m
    if ((k == 0 and i not in {0, 2, m - 1}) or (i, k) == (m - 1, 1)):
        return i, (k - 2) % m
    if ((i == m - 1 and k not in {1, m - 1}) or (i, k) == (0, 0)):
        return (i + 1) % m, (k - 1) % m
    return (i + 1) % m, (k - 2) % m


def return_map_formula(m: int, color: int, i: int, k: int) -> Pair:
    if color == 0:
        return R0_formula(m, i, k)
    if color == 1:
        return R1_formula(m, i, k)
    if color == 2:
        return R2_formula(m, i, k)
    raise ValueError("color must be 0,1,2")


# ---------------------------------------------------------------------------
# Closed-form first-return data on the transversals used in the manuscript
# ---------------------------------------------------------------------------

def T0_formula(m: int, x: int) -> int:
    x %= m
    if m % 6 in (0, 2):
        if x == 0:
            return m - 2
        if 1 <= x <= m - 5:
            return x + 2
        if x == m - 4:
            return m - 1
        if x == m - 3:
            return 2
        if x == m - 2:
            return 1
        return 0
    if x == 0:
        return m - 2
    if x == 1:
        return 4 % m
    if x == 2:
        return 6 % m
    if 3 <= x <= m - 7:
        return x + 4
    if x == m - 6:
        return 3
    if x == m - 5:
        return m - 1
    if x == m - 4:
        return 0
    if x == m - 3:
        return 2
    if x == m - 2:
        return 5
    return 1


def rho0_formula(m: int, x: int) -> int:
    x %= m
    if m % 6 in (0, 2):
        if x == 0:
            return 1
        if (1 <= x <= m - 4) or x == m - 1:
            return m - 1
        if x == m - 3:
            return 2 * m - 3
        return 2 * m - 1
    if x == 0:
        return 1
    if (1 <= x <= m - 7) or x == m - 4:
        return m - 2
    if x in {m - 6, m - 2}:
        return 2 * m - 4
    if x in {m - 5, m - 1}:
        return m - 1
    return 2 * m - 3


def T1_formula(m: int, x: int) -> int:
    x %= m
    if m % 6 in (0, 2):
        if x == 0:
            return 2 % m
        if 1 <= x <= m - 4:
            return (x + 3) % m
        if x == m - 3:
            return 1
        if x == m - 2:
            return 0
        return 3 % m
    if x == 0:
        return 2 % m
    if x == 1:
        return 3 % m
    if x == 2:
        return 5 % m
    if x == m - 2:
        return 0
    if x == m - 3:
        return 4 % m
    if x == m - 1:
        return 7 % m
    if x % 2 == 0:
        return (x + 2) % m
    return (x + 6) % m


def rho1_formula(m: int, x: int) -> int:
    x %= m
    if m % 6 in (0, 2):
        if x in {0, m - 2}:
            return 1
        if 1 <= x <= m - 4:
            return m + 2
        return m + 3
    if x in {0, 1, m - 2}:
        return 1
    if x == 2:
        return m + 3
    if x in {m - 3, m - 1}:
        return m + 6
    if x % 2 == 0:
        return m + 2
    return m + 4


def T2_formula(m: int, x: int) -> int:
    x %= m
    if x == 0:
        return 1
    if x == 1:
        return m - 1
    if x == 2:
        return 0
    return x - 1


def rho2_formula(m: int, x: int) -> int:
    x %= m
    if x == 0:
        return 1
    if x == 1:
        return m - 1
    if x == 2:
        return 2 * m
    return m


# ---------------------------------------------------------------------------
# Cycle-order helpers for the theorem certificate
# ---------------------------------------------------------------------------

def orbit_of_map(T: Callable[[int, int], int], m: int, start: int = 0) -> List[int]:
    out: List[int] = []
    x = start % m
    seen = set()
    while x not in seen:
        seen.add(x)
        out.append(x)
        x = T(m, x) % m
    if x != start % m:
        raise RuntimeError("map does not return to the start of the orbit")
    return out


def theorem_certificate(m: int) -> Certificate:
    if m < 6 or m % 2 != 0:
        raise ValueError("m must be even and >= 6")
    case = "I (m ≡ 0,2 mod 6)" if m % 6 in (0, 2) else "II (m ≡ 4 mod 6)"
    T0_orbit = orbit_of_map(T0_formula, m)
    T1_orbit = orbit_of_map(T1_formula, m)
    T2_orbit = orbit_of_map(T2_formula, m)
    if not (len(T0_orbit) == len(T1_orbit) == len(T2_orbit) == m):
        raise RuntimeError("at least one first-return map failed to be an m-cycle")
    rho0_sum = sum(rho0_formula(m, x) for x in range(m))
    rho1_sum = sum(rho1_formula(m, x) for x in range(m))
    rho2_sum = sum(rho2_formula(m, x) for x in range(m))
    if (rho0_sum, rho1_sum, rho2_sum) != (m * m, m * m, m * m):
        raise RuntimeError("a return-time sum is not m^2")
    return Certificate(
        m=m,
        case=case,
        T0_cycle_order=T0_orbit,
        T1_cycle_order=T1_orbit,
        T2_cycle_order=T2_orbit,
        rho0_sum=rho0_sum,
        rho1_sum=rho1_sum,
        rho2_sum=rho2_sum,
    )


# ---------------------------------------------------------------------------
# Exact finite validation utilities
# ---------------------------------------------------------------------------

def _encode3(i: int, j: int, k: int, m: int) -> int:
    return i * m * m + j * m + k


def _decode3(idx: int, m: int) -> Triple:
    k = idx % m
    idx //= m
    j = idx % m
    i = idx // m
    return (i, j, k)


def _make_dir_flat(m: int, color: int):
    """Build a flat direction-lookup array for layers 0, 1, 2.

    dir_flat[s*m*m + i*m + k] = bump direction (0/1/2) for the given color
    at the vertex on layer s with coordinates (i, (s-i-k)%m, k).
    Only valid for s in {0, 1, 2}; all other layers use the canonical
    direction = color.

    Fully vectorised: no Python-level loops.
    """
    import numpy as np
    mm = m * m
    c = color
    # Six direction triples
    T102, T201, T021 = (1, 0, 2), (2, 0, 1), (0, 2, 1)
    T210, T120, T012 = (2, 1, 0), (1, 2, 0), (0, 1, 2)

    dir_flat = np.empty(3 * mm, dtype=np.int8)

    # ---- Layer 0 (s = 0) ----
    d0 = dir_flat[0:mm].reshape(m, m)
    if m % 6 in (0, 2):
        # Case I: apply in reverse priority so highest-priority writes last.
        d0[:, :] = T120[c]                                 # default
        d0[0, 1:m - 1] = T210[c]                           # C-line: i=0
        d0[1, m - 1] = T210[c]                             # (1,0,m-1)
        d0[1:m - 2, 0] = T021[c]                           # B-line: k=0
        d0[0, m - 1] = T021[c]                             # (0,1,m-1)
        d0[m - 1, 1] = T021[c]                             # (m-1,0,1)
        ia = np.arange(1, m - 2, dtype=np.int32)
        d0[ia, (m - 1 - ia) % m] = T102[c]                 # A-line
        d0[0, 0] = T102[c]                                 # (0,0,0)
        d0[m - 1, m - 1] = T102[c]                         # (m-1,2,m-1)
        d0[m - 2, 0] = T201[c]                             # (m-2,2,0) overrides B
        d0[m - 2, 1] = T012[c]                             # (m-2,1,1) overrides A
    else:
        # Case II
        d0[:, :] = T120[c]                                 # default
        d0[1, 0] = T201[c]                                 # E: (1,m-1,0)
        d0[m - 2, 0] = T201[c]                             # E: (m-2,2,0)
        d0[1, m - 2] = T012[c]                             # D: (1,1,m-2)
        d0[m - 2, 1] = T012[c]                             # D: (m-2,1,1)
        d0[2, m - 1] = T210[c]                             # C: (2,m-1,m-1)
        d0[2, m - 2] = T210[c]                             # C: (2,0,m-2)
        d0[1, 1:m - 2] = T210[c]                           # C: i=1, k∈[1,m-3]
        d0[1, m - 1] = T210[c]                             # C: (1,0,m-1)
        d0[0, 1:m - 1] = T210[c]                           # C: i=0, k∈[1,m-2]
        d0[m - 1, 1] = T021[c]                             # B: (m-1,0,1)
        d0[2:m - 2, 0] = T021[c]                           # B: i∈[2,m-3], k=0
        d0[0, m - 1] = T021[c]                             # B: (0,1,m-1)
        d0[m - 1, m - 1] = T102[c]                         # A: (m-1,2,m-1)
        ia = np.arange(2, m - 2, dtype=np.int32)
        d0[ia, (m - 1 - ia) % m] = T102[c]                 # A-line
        d0[0, 0] = T102[c]                                 # A: (0,0,0)

    # ---- Layer 1 (s = 1): (1,0,2) if i==0, else (2,0,1) ----
    d1 = dir_flat[mm:2 * mm].reshape(m, m)
    d1[:, :] = T201[c]
    d1[0, :] = T102[c]

    # ---- Layer 2 (s = 2): (2,1,0) if j==0, else (0,1,2) ----
    d2 = dir_flat[2 * mm:3 * mm].reshape(m, m)
    d2[:, :] = T012[c]
    i2d = np.arange(m, dtype=np.int32).reshape(m, 1)
    k2d = np.arange(m, dtype=np.int32).reshape(1, m)
    d2[((i2d + k2d) % m) == 2] = T210[c]

    return dir_flat


def _build_color_perm(m: int, color: int):
    """Build a flat permutation array for one color on all m^3 vertices.

    Uses the vectorised direction tables for layers 0-2 and the canonical
    direction for all other layers.  No Python-level vertex loop.
    """
    import numpy as np
    n = m * m * m
    mm = m * m

    idx = np.arange(n, dtype=np.int32)
    ii = idx // mm
    jj = (idx % mm) // m
    kk = idx % m

    # Default direction for every vertex: `color` (canonical triple)
    d = np.full(n, color, dtype=np.int8)

    # Override layers 0, 1, 2 using the precomputed flat table
    dir_flat = _make_dir_flat(m, color)
    i2d = np.arange(m, dtype=np.int32).reshape(m, 1)
    k2d = np.arange(m, dtype=np.int32).reshape(1, m)
    for s_val in range(3):
        j_s = (s_val - i2d - k2d) % m
        flat_src = s_val * mm + i2d * m + k2d            # index into dir_flat
        flat_dst = i2d * mm + j_s * m + k2d              # index into d
        d[flat_dst.ravel()] = dir_flat[flat_src.ravel()]

    # Vectorised bump
    m0 = d == 0
    m1 = d == 1
    bi = ii.copy(); bi[m0] = (ii[m0] + 1) % m
    bj = jj.copy(); bj[m1] = (jj[m1] + 1) % m
    bk = kk.copy()
    m2 = ~(m0 | m1)
    bk[m2] = (kk[m2] + 1) % m

    return (bi * mm + bj * m + bk).astype(np.int32)


def _compose_perm_n(perm, n: int):
    """Compute perm^n by repeated squaring."""
    import numpy as np
    result = np.arange(len(perm), dtype=np.int32)
    base = perm.copy()
    while n > 0:
        if n & 1:
            result = base[result]
        base = base[base]
        n >>= 1
    return result


def validate_return_maps_against_definition(m: int) -> None:
    """Compare the displayed return-map formulas with the Route E definition.

    Tracks all m^2 points on P_0 through m colour-map steps using
    precomputed direction tables for layers 0-2.  Memory is O(m^2);
    time is O(m^3) with fully vectorised inner loop.
    """
    import numpy as np
    mm = m * m

    for color in range(3):
        dir_flat = _make_dir_flat(m, color)

        # Initialise the m^2 points of P_0: (i, (-i-k)%m, k)
        pi = np.repeat(np.arange(m, dtype=np.int32), m)
        pk = np.tile(np.arange(m, dtype=np.int32), m)
        pj = (-pi - pk) % m

        # Advance all points through m colour-map steps
        for _ in range(m):
            s = (pi + pj + pk) % m

            # Default direction = color (canonical triple on layers >= 3)
            d = np.full(mm, color, dtype=np.int8)

            # Override the (few) points currently on layers 0, 1, or 2
            special = s < 3
            if np.any(special):
                flat_idx = s[special] * mm + pi[special] * m + pk[special]
                d[special] = dir_flat[flat_idx]

            # Apply bump
            m0 = d == 0; m1 = d == 1; m2 = ~(m0 | m1)
            pi[m0] = (pi[m0] + 1) % m
            pj[m1] = (pj[m1] + 1) % m
            pk[m2] = (pk[m2] + 1) % m

        # Compare result with closed-form formulas
        for idx in range(mm):
            i_s, k_s = idx // m, idx % m
            got = (int(pi[idx]), int(pk[idx]))
            expected = return_map_formula(m, color, i_s, k_s)
            if got != expected:
                raise AssertionError(
                    f"return-map mismatch for color={color}, (i,k)=({i_s},{k_s}), "
                    f"definition={got}, formula={expected}"
                )


def cycle_lengths_on_p0(m: int, color: int) -> List[int]:
    """Compute cycle lengths of return map on P_0 using flat array."""
    import numpy as np
    m2 = m * m
    visited = np.zeros(m2, dtype=np.bool_)
    lengths: List[int] = []
    for idx in range(m2):
        if visited[idx]:
            continue
        x = idx
        count = 0
        while not visited[x]:
            visited[x] = True
            count += 1
            i, k = x // m, x % m
            ni, nk = return_map_formula(m, color, i, k)
            x = ni * m + nk
        lengths.append(count)
    lengths.sort()
    return lengths


def validate_return_map_cycle_structure(m: int) -> None:
    for color in range(3):
        lengths = cycle_lengths_on_p0(m, color)
        if lengths != [m * m]:
            raise AssertionError(f"color {color} return map does not have one m^2-cycle: {lengths}")


def cycle_lengths_on_V(m: int, color: int) -> List[int]:
    """Compute cycle lengths on V using numpy permutation array."""
    import numpy as np
    perm = _build_color_perm(m, color)
    n = len(perm)
    visited = np.zeros(n, dtype=np.bool_)
    lengths: List[int] = []
    for idx in range(n):
        if visited[idx]:
            continue
        x = idx
        count = 0
        while not visited[x]:
            visited[x] = True
            count += 1
            x = int(perm[x])
        lengths.append(count)
    lengths.sort()
    return lengths


def validate_full_color_cycles(m: int) -> None:
    for color in range(3):
        lengths = cycle_lengths_on_V(m, color)
        if lengths != [m ** 3]:
            raise AssertionError(f"color {color} is not a single Hamilton cycle: {lengths}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic Route E utilities for even m >= 6.")
    parser.add_argument("m", type=int, help="even integer m >= 6")
    parser.add_argument(
        "--mode",
        choices=["theorem", "return-check", "p0-check", "full-check"],
        default="theorem",
        help=(
            "theorem: quick theorem certificate from the closed-form first-return maps; "
            "return-check: compare displayed return maps with the Route E definition; "
            "p0-check: return-check plus exact cycle count on P0; "
            "full-check: exact cycle count on the full m^3-vertex digraph"
        ),
    )
    args = parser.parse_args(argv)

    m = args.m
    if m < 6 or m % 2 != 0:
        raise SystemExit("m must be even and >= 6")

    cert = theorem_certificate(m)
    print(f"m = {cert.m}")
    print(f"case = {cert.case}")
    print(f"T0 is an m-cycle: {cert.T0_cycle_order}")
    print(f"T1 is an m-cycle: {cert.T1_cycle_order}")
    print(f"T2 is an m-cycle: {cert.T2_cycle_order}")
    print(f"sum rho0 = {cert.rho0_sum}")
    print(f"sum rho1 = {cert.rho1_sum}")
    print(f"sum rho2 = {cert.rho2_sum}")
    print("Quick theorem certificate: PASS")

    if args.mode in {"return-check", "p0-check", "full-check"}:
        validate_return_maps_against_definition(m)
        print("Route E definition -> displayed return-map formulas: PASS")

    if args.mode in {"p0-check", "full-check"}:
        validate_return_map_cycle_structure(m)
        print("Return-map cycle structure on P0: PASS")

    if args.mode == "full-check":
        validate_full_color_cycles(m)
        print("All three color maps are Hamilton cycles on V: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
