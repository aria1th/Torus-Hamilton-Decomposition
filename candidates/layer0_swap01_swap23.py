#!/usr/bin/env python3
"""Simple 4D scouting candidate.

Use the permutation (1, 0, 3, 2) on the residue layer sum(coords) == 0 mod m,
and the canonical tuple elsewhere.
"""

from __future__ import annotations

from typing import Tuple


def direction_tuple(dim: int, m: int, v: Tuple[int, ...]) -> Tuple[int, ...]:
    if dim != 4:
        raise ValueError("layer0_swap01_swap23 is intended for dim=4 scouting only")
    if sum(v) % m == 0:
        return (1, 0, 3, 2)
    return (0, 1, 2, 3)
