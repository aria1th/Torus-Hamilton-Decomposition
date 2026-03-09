#!/usr/bin/env python3
"""Shared low-layer hyperplane-fusion candidate found by table search in d=4.

Rule summary:

- layer S = 0: use the affine-split pair
  - q = x0 + x2 == 0 mod m -> (3, 2, 1, 0)
  - otherwise              -> (1, 0, 3, 2)
- layer S = 1: canonical (0, 1, 2, 3)
- layer S = 2: canonical except for four q = 0 pattern rows
- layers S >= 3: canonical
"""

from __future__ import annotations

from typing import Dict, Tuple


_LAYER2_PATCH: Dict[Tuple[int, int, int, int, int], Tuple[int, int, int, int]] = {
    (0, 0, 0, 0, 1): (0, 3, 2, 1),
    (0, 0, 0, 1, 1): (2, 3, 0, 1),
    (0, 1, 0, 0, 1): (0, 3, 2, 1),
    (1, 0, 1, 1, 1): (2, 1, 0, 3),
}


def direction_tuple(dim: int, m: int, v: Tuple[int, ...]) -> Tuple[int, ...]:
    if dim != 4:
        raise ValueError("hyperplane_fusion_low_layers_v1 is intended for dim=4 only")

    layer = sum(v) % m
    q_zero = int((v[0] + v[2]) % m == 0)

    if layer == 0:
        return (3, 2, 1, 0) if q_zero else (1, 0, 3, 2)
    if layer == 1:
        return (0, 1, 2, 3)
    if layer == 2:
        key = (int(v[0] == 0), int(v[1] == 0), int(v[2] == 0), int(v[3] == 0), q_zero)
        return _LAYER2_PATCH.get(key, (0, 1, 2, 3))
    return (0, 1, 2, 3)
