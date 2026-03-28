#!/usr/bin/env python3
"""Check the P0 first-return invariants for Sel* colors 1 and 2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from torus_nd_d5_selector_star_common_119 import selector_perm_star, states_P0

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = (
    REPO_ROOT / "RoundY" / "checks" / "d5_269_selstar_color12_return_invariants_summary.json"
)
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_269_selstar_color12_return_invariants"


def r_step(m: int, color: int, point: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    cur = list(point)
    for _ in range(m):
        perm = selector_perm_star(m, tuple(cur))
        direction = perm[color]
        cur[direction] = (cur[direction] + 1) % m
    return tuple(cur)


def invariant_value(color: int, point: tuple[int, int, int, int, int], m: int) -> int:
    if color == 1:
        return (point[0] - point[2]) % m
    if color == 2:
        return (point[1] - point[3]) % m
    raise ValueError(color)


def analyze_modulus(m: int) -> dict:
    result: dict[str, object] = {"m": m, "colors": {}}
    for color in (1, 2):
        fiber_sizes = {str(v): 0 for v in range(m)}
        invariant_ok = True
        witness = None
        for point in states_P0(m):
            inv = invariant_value(color, point, m)
            fiber_sizes[str(inv)] += 1
            image = r_step(m, color, point)
            inv_image = invariant_value(color, image, m)
            if inv != inv_image and witness is None:
                invariant_ok = False
                witness = {
                    "point": list(point),
                    "image": list(image),
                    "inv_before": inv,
                    "inv_after": inv_image,
                }
        result["colors"][str(color)] = {
            "invariant_preserved": invariant_ok,
            "fiber_sizes": fiber_sizes,
            "witness": witness,
            "fiber_size_set": sorted({int(v) for v in fiber_sizes.values()}),
            "P0_size": m**4,
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Sel* color-1/2 P0-return invariants.")
    parser.add_argument("--moduli", nargs="*", type=int, default=[5, 7, 9, 11, 13])
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    args = parser.parse_args()

    args.detail_dir.mkdir(parents=True, exist_ok=True)
    per_modulus = {}
    all_ok = True
    for m in args.moduli:
        per_modulus[str(m)] = analyze_modulus(m)
        for color in ("1", "2"):
            all_ok &= per_modulus[str(m)]["colors"][color]["invariant_preserved"]

    summary = {
        "task": "d5_269_selstar_color12_return_invariants",
        "selector": "Sel*",
        "moduli": args.moduli,
        "invariants": {
            "1": "I_1(x) = x_0 - x_2 on P0",
            "2": "I_2(x) = x_1 - x_3 on P0",
        },
        "all_invariants_verified": all_ok,
        "conclusion": (
            "For every checked modulus, the first return R_1^* preserves x_0-x_2 and "
            "the first return R_2^* preserves x_1-x_3 on P0. Therefore the current "
            "Sel* colors 1 and 2 cannot themselves be Hamilton assembly colors."
        ),
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    with args.summary_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
    with (args.detail_dir / "per_modulus.json").open("w", encoding="utf-8") as fh:
        json.dump(per_modulus, fh, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
