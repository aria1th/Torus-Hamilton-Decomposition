#!/usr/bin/env python3
"""Shared selector-star utilities for the D5 119/120/122 compute checks."""

from __future__ import annotations

from typing import Callable

import numpy as np


def p_from_q(q: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    p = [None] * 5
    for generator, color in enumerate(q):
        p[color] = generator
    return tuple(p)


def q_from_p(p: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    q = [None] * 5
    for color, generator in enumerate(p):
        q[generator] = color
    return tuple(q)


def q3_rule_117(active_set: tuple[int, ...] | set[int]) -> tuple[int, int, int, int, int]:
    bit1 = 1 in active_set
    bit2 = 2 in active_set
    return (
        2 if bit2 else 0,
        4 if bit1 else 1,
        0 if bit2 else 2,
        3,
        1 if bit1 else 4,
    )


def active2(m: int, x: tuple[int, int, int, int, int]) -> tuple[int, ...]:
    return tuple(i for i in range(5) if x[(i + 1) % 5] == m - 1)


def active3(m: int, x: tuple[int, int, int, int, int]) -> tuple[int, ...]:
    return tuple(
        i
        for i in range(5)
        if (((x[(i - 1) % 5] + x[(i + 2) % 5]) % m == 2) ^ (x[(i + 1) % 5] == m - 1))
    )


q2_star_by_subset = {
    (): (0, 1, 2, 3, 4),
    (0,): (2, 1, 0, 3, 4),
    (1,): (0, 3, 2, 1, 4),
    (0, 1): (2, 3, 0, 1, 4),
    (2,): (0, 1, 4, 3, 2),
    (0, 2): (4, 1, 0, 3, 2),
    (1, 2): (0, 3, 4, 1, 2),
    (0, 1, 2): (4, 3, 0, 1, 2),
    (3,): (0, 1, 2, 3, 4),
    (0, 3): (3, 1, 2, 0, 4),
    (1, 3): (0, 3, 2, 1, 4),
    (0, 1, 3): (0, 3, 2, 1, 4),
    (2, 3): (0, 1, 4, 3, 2),
    (0, 2, 3): (3, 1, 4, 0, 2),
    (1, 2, 3): (3, 0, 4, 1, 2),
    (0, 1, 2, 3): (3, 0, 4, 1, 2),
    (4,): (0, 4, 2, 3, 1),
    (0, 4): (2, 4, 0, 3, 1),
    (1, 4): (0, 4, 2, 1, 3),
    (0, 1, 4): (2, 4, 0, 1, 3),
    (2, 4): (0, 1, 4, 3, 2),
    (0, 2, 4): (4, 1, 0, 3, 2),
    (1, 2, 4): (0, 3, 4, 1, 2),
    (0, 1, 2, 4): (4, 3, 0, 1, 2),
    (3, 4): (0, 4, 2, 3, 1),
    (0, 3, 4): (3, 4, 2, 0, 1),
    (1, 3, 4): (0, 4, 2, 1, 3),
    (0, 1, 3, 4): (0, 4, 2, 1, 3),
    (2, 3, 4): (0, 1, 4, 3, 2),
    (0, 2, 3, 4): (3, 1, 4, 0, 2),
    (1, 2, 3, 4): (3, 0, 4, 1, 2),
    (0, 1, 2, 3, 4): q_from_p((1, 3, 4, 0, 2)),
}


def selector_perm_star(m: int, x: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    slice_sum = sum(x) % m
    if slice_sum == 0:
        return tuple((color + 1) % 5 for color in range(5))
    if slice_sum == 1:
        return tuple((color - 1) % 5 for color in range(5))
    if slice_sum == 2:
        return p_from_q(q2_star_by_subset[active2(m, x)])
    if slice_sum == 3:
        return p_from_q(q3_rule_117(active3(m, x)))
    return tuple(range(5))


def states_P0(m: int):
    for x0 in range(m):
        for x1 in range(m):
            for x2 in range(m):
                for x3 in range(m):
                    x4 = (-x0 - x1 - x2 - x3) % m
                    yield (x0, x1, x2, x3, x4)


def build_R_data(
    m: int,
    color: int,
    selector_func: Callable[[int, tuple[int, int, int, int, int]], tuple[int, int, int, int, int]],
):
    points = list(states_P0(m))
    id_map = {point[:4]: idx for idx, point in enumerate(points)}
    point_count = len(points)
    perm = np.empty(point_count, dtype=np.int64 if point_count >= 2**31 else np.int32)
    images4 = np.empty((point_count, 4), dtype=np.int16 if m < 2**15 else np.int32)
    for idx, point in enumerate(points):
        image = list(point)
        for _ in range(m):
            perm_row = selector_func(m, tuple(image))
            direction = perm_row[color]
            image[direction] = (image[direction] + 1) % m
        perm[idx] = id_map[tuple(image[:4])]
        images4[idx] = image[:4]
    return points, perm, images4
