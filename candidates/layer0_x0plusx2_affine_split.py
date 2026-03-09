#!/usr/bin/env python3
"""Affine low-layer scouting candidate in dimension 4.

Rule:

- outside residue layer sum(coords) == 0 mod m: use the canonical tuple;
- on that layer: use (1, 0, 3, 2);
- on the sub-slice x0 + x2 == 0 mod m inside that layer: use (3, 2, 1, 0).
"""

from __future__ import annotations

from typing import Tuple


def direction_tuple(dim: int, m: int, v: Tuple[int, ...]) -> Tuple[int, ...]:
    if dim != 4:
        raise ValueError("layer0_x0plusx2_affine_split is intended for dim=4 scouting only")
    if sum(v) % m != 0:
        return (0, 1, 2, 3)
    if (v[0] + v[2]) % m == 0:
        return (3, 2, 1, 0)
    return (1, 0, 3, 2)
