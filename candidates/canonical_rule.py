#!/usr/bin/env python3
"""Toy candidate: the canonical direction tuple everywhere."""

from __future__ import annotations

from typing import Tuple


def direction_tuple(dim: int, m: int, v: Tuple[int, ...]) -> Tuple[int, ...]:
    del m, v
    return tuple(range(dim))
