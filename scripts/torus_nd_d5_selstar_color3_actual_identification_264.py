#!/usr/bin/env python3
"""Replay support for the Sel* color-3 actual/model identification theorem.

This script verifies two exact claims on checked moduli:

1. the first return

       R_3^* = (F_3^*)^m | P0

   on `P0 = {Sigma = 0}` is given by one explicit piecewise-affine formula;

2. on the section

       S_m = {x in P0 : x_2 = m - 2},

   the actual section return

       T_m = (R_3^*)^m | S_m

   agrees exactly with the explicit five-branch model from `d5_261`.

Outputs:
- RoundY/checks/d5_264_selstar_color3_actual_identification_summary.json
- RoundY/checks/d5_264_selstar_color3_actual_identification/per_modulus.json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from torus_nd_d5_selector_star_common_119 import build_R_data, selector_perm_star
from torus_nd_d5_selstar_color3_section_stitch_probe_258 import build_section_map
from torus_nd_d5_selstar_color3_section_model_261 import section_model_step


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = (
    REPO_ROOT / "RoundY" / "checks" / "d5_264_selstar_color3_actual_identification_summary.json"
)
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_264_selstar_color3_actual_identification"

State = tuple[int, int, int, int, int]
SectionPoint = tuple[int, int, int]


def make_p0_state(x4: tuple[int, int, int, int], m: int) -> State:
    return x4 + ((-sum(x4)) % m,)


def actual_r3_case(m: int, x: State) -> tuple[str, int]:
    x0, x1, x2, x3, x4 = x
    if x2 == m - 2:
        if x3 == m - 1 and x4 == m - 2:
            return ("section_C_start", 0)
        if x0 == m - 1 and x3 != m - 1:
            return ("section_A_start", 4)
        return ("section_G_start", 1)
    if x1 == m - 1 and x4 == m - 2:
        return ("later_special", 0)
    return ("later_generic", 3)


def actual_r3_formula(m: int, x: State) -> tuple[State, str]:
    case_name, d2 = actual_r3_case(m, x)
    y = list(x)
    y[4] = (y[4] + 1) % m
    y[2] = (y[2] + 1) % m
    y[d2] = (y[d2] + 1) % m
    y[3] = (y[3] - 3) % m
    return (tuple(y), case_name)


def analyse_modulus(m: int) -> dict[str, object]:
    pts, _perm, images4 = build_R_data(m, 3, selector_perm_star)
    xs = [make_p0_state(point[:4], m) for point in pts]
    ys = [make_p0_state(tuple(int(v) for v in images4[idx]), m) for idx in range(len(pts))]

    formula_failures: list[dict[str, object]] = []
    case_counts: Counter[str] = Counter()

    for x, y in zip(xs, ys):
        predicted, case_name = actual_r3_formula(m, x)
        case_counts[case_name] += 1
        if y != predicted and len(formula_failures) < 25:
            formula_failures.append(
                {
                    "state": list(x),
                    "actual_image": list(y),
                    "predicted_image": list(predicted),
                    "predicted_case": case_name,
                }
            )

    section, section_map, return_times = build_section_map(m)
    section_formula_failures: list[dict[str, object]] = []
    section_class_counts: Counter[str] = Counter()
    initial_class_counts: Counter[str] = Counter()
    later_special_counts: Counter[str] = Counter()

    for x in section:
        y = section_map[x]
        point: SectionPoint = (x[0], x[1], x[4])
        predicted = section_model_step(m, point)
        c = (2 - point[0] - point[1] - point[2]) % m
        a, b, e = point
        if e == m - 2 and c == m - 1:
            initial_class = "C_start"
        elif a == m - 1 and c != m - 1:
            initial_class = "A_start"
        else:
            initial_class = "G_start"
        initial_class_counts[initial_class] += 1

        pred_section_point = (y[0], y[1], y[4])
        if pred_section_point != predicted and len(section_formula_failures) < 25:
            section_formula_failures.append(
                {
                    "state": list(x),
                    "actual_image": list(y),
                    "predicted_section_coords": list(predicted),
                    "initial_class": initial_class,
                }
            )

        diff = (
            (pred_section_point[0] - a) % m,
            (pred_section_point[1] - b) % m,
            (pred_section_point[2] - e) % m,
        )
        class_name = {
            (0, 1, 0): "G",
            (0, 0, 1): "A",
            (1, 1, 0): "B",
            (1, 0, 0): "C",
            (1, 0, 1): "D",
        }.get(diff, "UNKNOWN")
        section_class_counts[class_name] += 1
        later_special_counts["with_later_special" if diff[0] == 1 and class_name != "C" else "without_later_special"] += 1

    return {
        "m": m,
        "P0_size": len(xs),
        "S_size": len(section),
        "R_formula_verified": not formula_failures,
        "R_formula_failures": formula_failures,
        "R_case_counts": dict(sorted(case_counts.items())),
        "section_return_times": {str(k): v for k, v in sorted(return_times.items())},
        "section_formula_verified": not section_formula_failures,
        "section_formula_failures": section_formula_failures,
        "section_class_counts": dict(sorted(section_class_counts.items())),
        "section_initial_class_counts": dict(sorted(initial_class_counts.items())),
        "section_later_special_counts": dict(sorted(later_special_counts.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Sel* color-3 actual/model identification replay.")
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
        default=list(range(3, 26)),
        help="moduli to check",
    )
    args = parser.parse_args()

    per_modulus = {str(m): analyse_modulus(m) for m in args.moduli}
    summary = {
        "task": "d5_264_selstar_color3_actual_identification",
        "selector": "Sel*",
        "color": 3,
        "checked_moduli": args.moduli,
        "all_P0_return_formulas_verified": all(
            payload["R_formula_verified"] for payload in per_modulus.values()
        ),
        "all_section_formulas_verified": all(
            payload["section_formula_verified"] for payload in per_modulus.values()
        ),
        "conclusion": (
            "The actual Sel* color-3 first return R_3^* on P0 is given by one explicit "
            "piecewise-affine formula, and the actual m-step section return on "
            "S_m={x_2=m-2} agrees exactly with the explicit five-branch model from d5_261 "
            "throughout the checked range."
        ),
    }

    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.detail_dir / "per_modulus.json").write_text(
        json.dumps(per_modulus, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
