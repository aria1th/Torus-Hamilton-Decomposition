#!/usr/bin/env python3
"""Probe the Sel* color-3 Route-E section map on x2 = m-2.

We work with the first return

    R3* = (F3*)^m | P0

and then its section iterate

    Tm = (R3*)^m | Sm

on

    Sm = {x in P0 : x2 = m - 2}.

The script verifies:

1. every point of Sm returns to Sm after exactly m iterates of R3*;
2. Tm is a single m^3-cycle on checked odd moduli;
3. the Tm update on section coordinates (a,b,e) = (x0,x1,x4) has a small
   finite-defect law.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from torus_nd_d5_selector_star_common_119 import build_R_data, selector_perm_star


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_258_selstar_color3_section_stitch_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_258_selstar_color3_section_stitch"

State = tuple[int, int, int, int, int]


def make_p0_state(x4: tuple[int, int, int, int], m: int) -> State:
    return x4 + ((-sum(x4)) % m,)


def section_state(x: State, m: int) -> bool:
    return x[2] == m - 2


def section_coords(x: State) -> tuple[int, int, int, int]:
    return (x[0], x[1], x[3], x[4])


def build_section_map(m: int) -> tuple[list[State], dict[State, State], Counter[int]]:
    pts, perm, _images4 = build_R_data(m, 3, selector_perm_star)
    xs = [make_p0_state(tuple(point[:4]), m) for point in pts]
    id_map = {x: idx for idx, x in enumerate(xs)}

    section = [x for x in xs if section_state(x, m)]
    section_map: dict[State, State] = {}
    return_times: Counter[int] = Counter()

    for x in section:
        idx = id_map[x]
        t = 0
        while True:
            idx = int(perm[idx])
            t += 1
            y = xs[idx]
            if section_state(y, m):
                return_times[t] += 1
                if t == m:
                    section_map[x] = y
                break
            if t > 2 * m:
                raise RuntimeError(f"section return exceeded 2m at m={m} for x={x}")

    return section, section_map, return_times


def cycle_counter(section: list[State], section_map: dict[State, State]) -> Counter[int]:
    seen: set[State] = set()
    counts: Counter[int] = Counter()
    for x in section:
        if x in seen:
            continue
        cur = x
        length = 0
        while cur not in seen:
            seen.add(cur)
            length += 1
            cur = section_map[cur]
        counts[length] += 1
    return counts


def classify_section_step(m: int, x: State) -> tuple[str, tuple[int, int, int]]:
    a, b, _, c, e = x
    if a == m - 1 and c != m - 1 and (b != m - 1 or e == (m - 3) % m):
        return ("A", (a, b, (e + 1) % m))
    if b == (m - 2) % m and e != (m - 2) % m and (a != m - 1 or e == 6 % m):
        return ("B", ((a + 1) % m, (b + 1) % m, e))
    if e == (m - 2) % m and c == m - 1:
        return ("C", ((a + 1) % m, b, e))
    if a == m - 1 and b == m - 1 and e not in {5 % m, (m - 3) % m}:
        return ("D", ((a + 1) % m, b, (e + 1) % m))
    return ("G", (a, (b + 1) % m, e))


def analyse_modulus(m: int) -> dict[str, object]:
    section, section_map, return_times = build_section_map(m)
    cycle_counts = cycle_counter(section, section_map)

    diff_counts: Counter[tuple[int, int, int]] = Counter()
    class_counts: Counter[str] = Counter()
    formula_failures: list[dict[str, object]] = []

    nongeneric_columns: Counter[int] = Counter()
    nongeneric_by_column: dict[tuple[int, int], list[tuple[int, str]]] = defaultdict(list)

    for x in section:
        y = section_map[x]
        a, b, e = x[0], x[1], x[4]
        diff = ((y[0] - x[0]) % m, (y[1] - x[1]) % m, (y[4] - x[4]) % m)
        diff_counts[diff] += 1

        cls, predicted = classify_section_step(m, x)
        class_counts[cls] += 1
        if (y[0], y[1], y[4]) != predicted and len(formula_failures) < 25:
            formula_failures.append(
                {
                    "state": list(x),
                    "image": list(y),
                    "class": cls,
                    "predicted_section_coords": list(predicted),
                }
            )
        if cls != "G":
            nongeneric_by_column[(a, e)].append((b, cls))

    for key, rows in nongeneric_by_column.items():
        nongeneric_columns[len(rows)] += 1

    interesting_columns = {
        f"{a},{e}": [{"b": b, "class": cls} for b, cls in sorted(rows)]
        for (a, e), rows in sorted(nongeneric_by_column.items())
        if a >= m - 2
    }

    return {
        "m": m,
        "section_size": len(section),
        "section_return_times": {str(k): v for k, v in sorted(return_times.items())},
        "all_section_returns_after_exactly_m_R_steps": return_times == Counter({m: len(section)}),
        "section_cycle_counts": {str(k): v for k, v in sorted(cycle_counts.items())},
        "section_is_single_cycle": cycle_counts == Counter({m**3: 1}),
        "section_step_diff_counts": {
            f"{d[0]},{d[1]},{d[2]}": c for d, c in sorted(diff_counts.items())
        },
        "class_counts": dict(sorted(class_counts.items())),
        "section_formula_verified": not formula_failures,
        "formula_failures": formula_failures,
        "nongeneric_column_size_histogram": {str(k): v for k, v in sorted(nongeneric_columns.items())},
        "interesting_columns_last_rows": interesting_columns,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe the Sel* color-3 section-stitch route.")
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
        default=[9, 11, 13, 15, 17, 19, 21],
        help="odd moduli to check",
    )
    args = parser.parse_args()

    per_modulus = {str(m): analyse_modulus(m) for m in args.moduli}
    summary = {
        "task": "d5_258_selstar_color3_section_stitch",
        "selector": "Sel*",
        "color": 3,
        "checked_moduli": args.moduli,
        "all_section_returns_exact": all(
            payload["all_section_returns_after_exactly_m_R_steps"] for payload in per_modulus.values()
        ),
        "all_sections_single_cycle": all(payload["section_is_single_cycle"] for payload in per_modulus.values()),
        "all_candidate_section_formulas_verified": all(
            payload["section_formula_verified"] for payload in per_modulus.values()
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
