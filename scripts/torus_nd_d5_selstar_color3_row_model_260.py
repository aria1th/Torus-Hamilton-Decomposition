#!/usr/bin/env python3
"""All-m row-model support for the Sel* color-3 section-stitch route.

This script studies the first return to the row section

    B0 = {b = 0}

inside the explicit five-branch section model from d5_258.

For m >= 9, the induced row-return map is conjecturally and checked to equal
the explicit two-dimensional row model

    W_m : (a,e) -> (a',e')

defined by the formulas in `row_model_image`.

The script records three kinds of evidence:

1. exact agreement between the actual row return and the explicit row model
   on a checked range;
2. direct cycle counts for the actual row return on a broader checked range;
3. cycle counts for the explicit row model on a much broader checked range.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from torus_nd_d5_selstar_color3_section_stitch_probe_258 import build_section_map


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_260_selstar_color3_row_model_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_260_selstar_color3_row_model"


def cycle_counts_from_map(points: list[tuple[int, int]], mapping: dict[tuple[int, int], tuple[int, int]]) -> Counter[int]:
    seen: set[tuple[int, int]] = set()
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


def actual_row_return(m: int) -> dict[tuple[int, int], tuple[int, int]]:
    section, section_map, _return_times = build_section_map(m)
    row_section = [x for x in section if x[1] == 0]

    mapping: dict[tuple[int, int], tuple[int, int]] = {}
    for x in row_section:
        cur = x
        while True:
            cur = section_map[cur]
            if cur[1] == 0:
                mapping[(x[0], x[4])] = (cur[0], cur[4])
                break
    return mapping


def row_model_image(m: int, a: int, e: int) -> tuple[int, int]:
    if m < 9:
        raise ValueError("row_model_image is intended only for m >= 9")
    if a == m - 1:
        if e == 4:
            return (0, m - 2)
        return (m - 1, (e + 1) % m)
    if a == m - 2:
        if e == 5:
            return (m - 1, 5)
        if e == m - 3:
            return (0, m - 1)
        if e == m - 2:
            return (0, 6)
        return (0, (e + 1) % m)
    return ((a + 1) % m, e)


def explicit_row_model(m: int) -> dict[tuple[int, int], tuple[int, int]]:
    if m < 9:
        raise ValueError("explicit_row_model is intended only for m >= 9")
    return {(a, e): row_model_image(m, a, e) for a in range(m) for e in range(m)}


def analyse_actual_modulus(m: int) -> dict[str, object]:
    mapping = actual_row_return(m)
    points = sorted(mapping)
    cycle_counts = cycle_counts_from_map(points, mapping)
    payload: dict[str, object] = {
        "m": m,
        "row_return_cycle_counts": {str(k): v for k, v in sorted(cycle_counts.items())},
        "row_return_is_single_cycle": cycle_counts == Counter({m * m: 1}),
    }

    if m >= 9:
        model = explicit_row_model(m)
        mismatches = []
        for point in points:
            if mapping[point] != model[point]:
                mismatches.append(
                    {
                        "point": list(point),
                        "actual_image": list(mapping[point]),
                        "model_image": list(model[point]),
                    }
                )
                if len(mismatches) >= 25:
                    break
        payload["row_model_formula_verified"] = not mismatches
        payload["row_model_formula_mismatches"] = mismatches

    return payload


def analyse_model_modulus(m: int) -> dict[str, object]:
    mapping = explicit_row_model(m)
    points = sorted(mapping)
    cycle_counts = cycle_counts_from_map(points, mapping)
    return {
        "m": m,
        "row_model_cycle_counts": {str(k): v for k, v in sorted(cycle_counts.items())},
        "row_model_is_single_cycle": cycle_counts == Counter({m * m: 1}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Sel* color-3 row-model support.")
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
        "--actual-moduli",
        type=int,
        nargs="*",
        default=list(range(3, 26)),
        help="moduli for direct actual row-return checks",
    )
    parser.add_argument(
        "--model-moduli",
        type=int,
        nargs="*",
        default=list(range(9, 402)),
        help="moduli for the explicit row-model cycle checks",
    )
    args = parser.parse_args()

    actual_results = {str(m): analyse_actual_modulus(m) for m in args.actual_moduli}
    model_results = {str(m): analyse_model_modulus(m) for m in args.model_moduli}

    summary = {
        "task": "d5_260_selstar_color3_row_model",
        "selector": "Sel*",
        "color": 3,
        "candidate_theorem": (
            "For m >= 9, the explicit b=0 row-return model extracted from the "
            "five-branch section law is one m^2-cycle."
        ),
        "actual_moduli": args.actual_moduli,
        "model_moduli": args.model_moduli,
        "all_actual_row_returns_single_cycle_for_m_gt_2_in_checked_range": all(
            payload["row_return_is_single_cycle"] for payload in actual_results.values()
        ),
        "all_actual_row_returns_match_model_for_m_ge_9_in_checked_range": all(
            (int(m) < 9) or payload.get("row_model_formula_verified", False)
            for m, payload in actual_results.items()
        ),
        "all_explicit_row_models_single_cycle_in_checked_range": all(
            payload["row_model_is_single_cycle"] for payload in model_results.values()
        ),
        "small_moduli_closed_by_direct_actual_check": [m for m in args.actual_moduli if 3 <= m <= 8],
    }

    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)

    with args.summary_output.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
        fh.write("\n")

    with (args.detail_dir / "actual_per_modulus.json").open("w", encoding="utf-8") as fh:
        json.dump(actual_results, fh, indent=2, sort_keys=True)
        fh.write("\n")

    with (args.detail_dir / "model_per_modulus.json").open("w", encoding="utf-8") as fh:
        json.dump(model_results, fh, indent=2, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
