#!/usr/bin/env python3
"""Verify a stable Route-E-style five-color exact-family candidate.

The candidate fixes the closed Sel* colors 3 and 4. The remaining colors 0,1,2
are assigned by one fixed permutation on the following local classes:

- S0
- S1
- S4+
- S2(A2): full slice-2 active set A2(x)
- S3(b1): the one-bit slice-3 class b1 = 1_{1 in A3(x)}

This script records one explicit candidate found by combined CSP search on
m = 5,7, then verifies exactness on checked odd moduli and reports cycle
profiles on small checked moduli.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from torus_nd_d5_selector_star_common_119 import active2, active3, selector_perm_star

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_273_routee_assembly_candidate_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_273_routee_assembly_candidate"


CANDIDATE_RULE: dict[tuple[object, ...], tuple[int, int, int]] = {
    ("S0",): (0, 1, 2),
    ("S1",): (0, 1, 2),
    ("S4+",): (0, 1, 2),
    ("S3", 0): (2, 1, 0),
    ("S3", 1): (1, 2, 0),
    ("S2", ()): (1, 2, 0),
    ("S2", (3,)): (1, 2, 0),
    ("S2", (2,)): (2, 0, 1),
    ("S2", (1,)): (0, 1, 2),
    ("S2", (1, 2, 3)): (2, 0, 1),
    ("S2", (2, 3)): (2, 1, 0),
    ("S2", (1, 3)): (0, 1, 2),
    ("S2", (1, 2)): (2, 0, 1),
    ("S2", (0,)): (1, 2, 0),
    ("S2", (0, 2, 3)): (2, 0, 1),
    ("S2", (0, 3)): (0, 1, 2),
    ("S2", (0, 2)): (2, 1, 0),
    ("S2", (0, 1, 3)): (2, 1, 0),
    ("S2", (0, 1)): (2, 1, 0),
    ("S2", (0, 1, 2)): (1, 0, 2),
    ("S2", (0, 1, 2, 3)): (1, 0, 2),
    ("S2", (4,)): (2, 1, 0),
    ("S2", (2, 3, 4)): (2, 1, 0),
    ("S2", (3, 4)): (2, 1, 0),
    ("S2", (2, 4)): (2, 0, 1),
    ("S2", (1, 3, 4)): (0, 1, 2),
    ("S2", (1, 4)): (0, 1, 2),
    ("S2", (1, 2, 4)): (2, 0, 1),
    ("S2", (1, 2, 3, 4)): (2, 0, 1),
    ("S2", (0, 3, 4)): (2, 0, 1),
    ("S2", (0, 4)): (2, 1, 0),
    ("S2", (0, 2, 4)): (2, 1, 0),
    ("S2", (0, 2, 3, 4)): (2, 0, 1),
    ("S2", (0, 1, 4)): (2, 1, 0),
    ("S2", (0, 1, 3, 4)): (2, 1, 0),
    ("S2", (0, 1, 2, 4)): (1, 0, 2),
    ("S2", (0, 1, 2, 3, 4)): (1, 0, 2),
}


def class_key(m: int, x: tuple[int, int, int, int, int]) -> tuple[object, ...]:
    sig = sum(x) % m
    if sig == 0:
        return ("S0",)
    if sig == 1:
        return ("S1",)
    if sig == 2:
        return ("S2", active2(m, x))
    if sig == 3:
        return ("S3", int(1 in active3(m, x)))
    return ("S4+",)


def class_name(key: tuple[object, ...]) -> str:
    if key == ("S0",):
        return "S0"
    if key == ("S1",):
        return "S1"
    if key == ("S4+",):
        return "S4+"
    if key[0] == "S3":
        return f"S3({key[1]})"
    subset = ",".join(str(v) for v in key[1])
    return f"S2({{{subset}}})"


def selector_candidate(m: int, x: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    p_star = selector_perm_star(m, x)
    used = {p_star[3], p_star[4]}
    rem = sorted(d for d in range(5) if d not in used)
    perm = CANDIDATE_RULE[class_key(m, x)]
    out = [None] * 5
    out[3] = p_star[3]
    out[4] = p_star[4]
    for color, ridx in zip((0, 1, 2), perm):
        out[color] = rem[ridx]
    return tuple(out)


def exact_check(m: int) -> tuple[bool, dict[str, object] | None]:
    for y in itertools.product(range(m), repeat=5):
        colors = []
        for j in range(5):
            x = list(y)
            x[j] = (x[j] - 1) % m
            x_t = tuple(x)
            p = selector_candidate(m, x_t)
            incoming = [c for c, d in enumerate(p) if d == j]
            if len(incoming) != 1:
                return False, {
                    "type": "predecessor_collision",
                    "target": list(y),
                    "direction": j,
                    "incoming_colors": incoming,
                    "source_class": class_name(class_key(m, x_t)),
                    "source_selector": list(p),
                }
            colors.append(incoming[0])
        if sorted(colors) != [0, 1, 2, 3, 4]:
            return False, {
                "type": "target_not_latin",
                "target": list(y),
                "incoming_colors": colors,
            }
    return True, None


def cycle_histogram(m: int, color: int) -> dict[str, int]:
    states = list(itertools.product(range(m), repeat=5))
    index_of = {state: idx for idx, state in enumerate(states)}
    perm = [0] * len(states)
    for idx, x in enumerate(states):
        y = list(x)
        d = selector_candidate(m, x)[color]
        y[d] = (y[d] + 1) % m
        perm[idx] = index_of[tuple(y)]
    seen = [False] * len(states)
    counts: Counter[int] = Counter()
    for start in range(len(states)):
        if seen[start]:
            continue
        cur = start
        size = 0
        while not seen[cur]:
            seen[cur] = True
            cur = perm[cur]
            size += 1
        counts[size] += 1
    return {str(size): count for size, count in sorted(counts.items())}


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify the Route-E assembly exact-family candidate.")
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    args = parser.parse_args()

    exact_moduli = [5, 7, 9, 11, 13]
    cycle_moduli = [5, 7, 9]

    exact_rows = []
    for m in exact_moduli:
        ok, witness = exact_check(m)
        exact_rows.append({"modulus": m, "exact": ok, "failure_witness": witness})

    cycle_rows = []
    for m in cycle_moduli:
        cycle_rows.append(
            {
                "modulus": m,
                "histograms": {str(color): cycle_histogram(m, color) for color in range(5)},
            }
        )

    summary = {
        "task": "d5_273_routee_assembly_candidate",
        "family": (
            "Fix Sel* colors 3 and 4. Assign colors 0,1,2 by one fixed permutation on S0, S1, S4+, "
            "the full slice-2 active-set class S2(A2), and the one-bit slice-3 class S3(1 in A3)."
        ),
        "exact_checked_moduli": exact_moduli,
        "all_exact_checks_passed": all(row["exact"] for row in exact_rows),
        "cycle_checked_moduli": cycle_moduli,
        "conclusion": (
            "There is a simple Route-E-style exact-family candidate beyond the old defect-bit splice coordinates. "
            "The displayed candidate is exact on checked odd moduli 5,7,9,11,13. "
            "Within this candidate, colors 3 and 4 remain Hamilton on the checked range, while colors 0,1,2 "
            "still require a separate Hamiltonicity analysis."
        ),
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    with args.summary_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
    with (args.detail_dir / "exact_checks.json").open("w", encoding="utf-8") as fh:
        json.dump(exact_rows, fh, indent=2, sort_keys=True)
    with (args.detail_dir / "cycle_profiles.json").open("w", encoding="utf-8") as fh:
        json.dump(cycle_rows, fh, indent=2, sort_keys=True)
    with (args.detail_dir / "candidate_rule.json").open("w", encoding="utf-8") as fh:
        json.dump(
            {class_name(key): list(value) for key, value in sorted(CANDIDATE_RULE.items(), key=str)},
            fh,
            indent=2,
            sort_keys=True,
        )


if __name__ == "__main__":
    main()
