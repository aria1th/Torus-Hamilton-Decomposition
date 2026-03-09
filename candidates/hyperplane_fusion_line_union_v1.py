#!/usr/bin/env python3
"""Line-union gauge representative for the 4D low-layer hyperplane witness.

Rule summary:

- layer S = 0: use the affine-split pair
  - q = x0 + x2 == 0 mod m -> (3, 2, 1, 0)
  - otherwise              -> (1, 0, 3, 2)
- layer S = 1: canonical (0, 1, 2, 3)
- layer S = 2, q = 0: apply two commuting swaps on the canonical tuple
  - odd swap  (slots 1 <-> 3) if x0 = 0
  - even swap (slots 0 <-> 2) if x3 = 0
- layers S >= 3: canonical
"""

from __future__ import annotations

from typing import Tuple


def _apply_swaps(odd_swap: bool, even_swap: bool) -> Tuple[int, int, int, int]:
    out = [0, 1, 2, 3]
    if odd_swap:
        out[1], out[3] = out[3], out[1]
    if even_swap:
        out[0], out[2] = out[2], out[0]
    return tuple(out)


def direction_tuple(dim: int, m: int, v: Tuple[int, ...]) -> Tuple[int, ...]:
    if dim != 4:
        raise ValueError("hyperplane_fusion_line_union_v1 is intended for dim=4 only")

    layer = sum(v) % m
    q_zero = int((v[0] + v[2]) % m == 0)

    if layer == 0:
        return (3, 2, 1, 0) if q_zero else (1, 0, 3, 2)
    if layer == 1:
        return (0, 1, 2, 3)
    if layer == 2 and q_zero:
        return _apply_swaps(odd_swap=(v[0] % m == 0), even_swap=(v[3] % m == 0))
    return (0, 1, 2, 3)
