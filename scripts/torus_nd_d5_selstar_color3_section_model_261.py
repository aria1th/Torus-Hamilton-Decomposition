#!/usr/bin/env python3
"""Explicit section-model support for the Sel* color-3 route.

This script studies the pure three-dimensional model obtained from the
five-branch section law of d5_258, independent of the original torus map.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from torus_nd_d5_selstar_color3_row_model_260 import explicit_row_model


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_261_selstar_color3_section_model_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_261_selstar_color3_section_model"

Point3 = tuple[int, int, int]


def section_model_step(m: int, point: Point3) -> Point3:
    a, b, e = point
    c = (2 - a - b - e) % m
    if a == m - 1 and c != m - 1 and (b != m - 1 or e == (m - 3) % m):
        return (a, b, (e + 1) % m)
    if b == (m - 2) % m and e != (m - 2) % m and (a != m - 1 or e == 6 % m):
        return ((a + 1) % m, (b + 1) % m, e)
    if e == (m - 2) % m and c == m - 1:
        return ((a + 1) % m, b, e)
    if a == m - 1 and b == m - 1 and e not in {5 % m, (m - 3) % m}:
        return ((a + 1) % m, b, (e + 1) % m)
    return (a, (b + 1) % m, e)


def cycle_counts_from_map(points: list[Point3], mapping: dict[Point3, Point3]) -> Counter[int]:
    seen: set[Point3] = set()
    counts: Counter[int] = Counter()
    for point in points:
        if point in seen:
            continue
        cur = point
        length = 0
        while cur not in seen:
            seen.add(cur)
            cur = mapping[cur]
            length += 1
        counts[length] += 1
    return counts


def build_model_map(m: int) -> dict[Point3, Point3]:
    return {(a, b, e): section_model_step(m, (a, b, e)) for a in range(m) for b in range(m) for e in range(m)}


def first_return_to_B0(m: int, mapping: dict[Point3, Point3]) -> tuple[dict[tuple[int, int], tuple[int, int]], Counter[int], bool, int]:
    B0 = [(a, 0, e) for a in range(m) for e in range(m)]
    return_map: dict[tuple[int, int], tuple[int, int]] = {}
    return_times: Counter[int] = Counter()

    owner: dict[Point3, tuple[int, int]] = {}
    disjoint = True

    for start in B0:
        base = (start[0], start[2])
        cur = start
        owner[cur] = base
        t = 0
        while True:
            cur = mapping[cur]
            t += 1
            if cur[1] == 0:
                return_map[base] = (cur[0], cur[2])
                return_times[t] += 1
                break
            if cur in owner and owner[cur] != base:
                disjoint = False
            owner[cur] = base
            if t > 20 * m * m:
                raise RuntimeError(f"B0 return exceeded 20m^2 at m={m} for start={start}")

    return return_map, return_times, disjoint, len(owner)


def analyse_modulus(m: int) -> dict[str, object]:
    mapping = build_model_map(m)
    points = sorted(mapping)
    cycle_counts = cycle_counts_from_map(points, mapping)

    b0_return_map, b0_return_times, b0_disjoint, half_open_coverage = first_return_to_B0(m, mapping)
    b0_points = sorted(b0_return_map)
    b0_cycle_counts = cycle_counts_from_map(b0_points, b0_return_map)

    payload: dict[str, object] = {
        "m": m,
        "section_model_cycle_counts": {str(k): v for k, v in sorted(cycle_counts.items())},
        "section_model_is_single_cycle": cycle_counts == Counter({m**3: 1}),
        "B0_return_cycle_counts": {str(k): v for k, v in sorted(b0_cycle_counts.items())},
        "B0_return_is_single_cycle": b0_cycle_counts == Counter({m**2: 1}),
        "B0_return_time_counts": {str(k): v for k, v in sorted(b0_return_times.items())},
        "B0_half_open_segments_disjoint": b0_disjoint,
        "B0_half_open_segment_coverage": half_open_coverage,
        "B0_half_open_segments_cover_all_states": half_open_coverage == m**3,
    }

    if m >= 9:
        row_model = explicit_row_model(m)
        mismatches = []
        for point in b0_points:
            if b0_return_map[point] != row_model[point]:
                mismatches.append(
                    {
                        "point": list(point),
                        "actual_image": list(b0_return_map[point]),
                        "row_model_image": list(row_model[point]),
                    }
                )
                if len(mismatches) >= 25:
                    break
        payload["B0_return_matches_row_model"] = not mismatches
        payload["B0_return_row_model_mismatches"] = mismatches

    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Explicit section-model support for Sel* color-3.")
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=DEFAULT_SUMMARY,
        help=f"summary JSON path (default: {DEFAULT_SUMMARY})",
    )
    parser.add_argument(
        "--detail-dir",
        type=Path,
        default=DEFAULT_DETAIL_DIR,
        help=f"detail output directory (default: {DEFAULT_DETAIL_DIR})",
    )
    parser.add_argument(
        "--moduli",
        type=int,
        nargs="*",
        default=list(range(3, 102)),
        help="moduli to check",
    )
    args = parser.parse_args()

    per_modulus = {str(m): analyse_modulus(m) for m in args.moduli}
    summary = {
        "task": "d5_261_selstar_color3_section_model",
        "selector": "Sel*",
        "color": 3,
        "candidate_theorem": (
            "For every m > 2, the explicit five-branch section model from d5_258 "
            "is one m^3-cycle."
        ),
        "checked_moduli": args.moduli,
        "all_section_models_single_cycle": all(
            payload["section_model_is_single_cycle"] for payload in per_modulus.values()
        ),
        "all_B0_returns_single_cycle": all(
            payload["B0_return_is_single_cycle"] for payload in per_modulus.values()
        ),
        "all_B0_half_open_segments_disjoint": all(
            payload["B0_half_open_segments_disjoint"] for payload in per_modulus.values()
        ),
        "all_B0_half_open_segments_cover_all_states": all(
            payload["B0_half_open_segments_cover_all_states"] for payload in per_modulus.values()
        ),
        "all_B0_returns_match_row_model_for_m_ge_9": all(
            (int(m) < 9) or payload.get("B0_return_matches_row_model", False)
            for m, payload in per_modulus.items()
        ),
    }

    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)

    with args.summary_output.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
        fh.write("\n")

    with (args.detail_dir / "per_modulus.json").open("w", encoding="utf-8") as fh:
        json.dump(per_modulus, fh, indent=2, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
