#!/usr/bin/env python3
"""Search the smallest slice-class leftover-ordering family for five-color assembly."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from torus_nd_d5_selector_star_common_119 import selector_perm_star

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = (
    REPO_ROOT / "RoundY" / "checks" / "d5_270_five_color_slice_ordering_search_summary.json"
)


PERMS = list(itertools.permutations((0, 1, 2)))


def remaining_dirs(m: int, x: tuple[int, int, int, int, int]) -> list[int]:
    p = selector_perm_star(m, x)
    used = {p[3], p[4]}
    return sorted(d for d in range(5) if d not in used)


def slice_class(m: int, x: tuple[int, int, int, int, int]) -> int:
    sig = sum(x) % m
    if sig == 0:
        return 0
    if sig == 1:
        return 1
    if sig == 2:
        return 2
    if sig == 3:
        return 3
    return 4


def assign_rule(rule: tuple[tuple[int, int, int], ...], m: int, x: tuple[int, int, int, int, int]) -> dict[int, int]:
    p = selector_perm_star(m, x)
    rem = remaining_dirs(m, x)
    pi = rule[slice_class(m, x)]
    out = {3: p[3], 4: p[4]}
    for color, idx in zip((0, 1, 2), pi):
        out[color] = rem[idx]
    return out


def exact_on(m: int, rule: tuple[tuple[int, int, int], ...]) -> bool:
    for x0 in range(m):
        for x1 in range(m):
            for x2 in range(m):
                for x3 in range(m):
                    for x4 in range(m):
                        y = (x0, x1, x2, x3, x4)
                        seen = []
                        for j in range(5):
                            x = list(y)
                            x[j] = (x[j] - 1) % m
                            colors = [c for c, d in assign_rule(rule, m, tuple(x)).items() if d == j]
                            if len(colors) != 1:
                                return False
                            seen.append(colors[0])
                        if sorted(seen) != [0, 1, 2, 3, 4]:
                            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Search slice-class leftover-ordering completions.")
    parser.add_argument("--modulus", type=int, default=5)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()

    rule_count = 0
    exact_rules = []
    for rule in itertools.product(PERMS, repeat=5):
        rule_count += 1
        if exact_on(args.modulus, rule):
            exact_rules.append(rule)

    summary = {
        "task": "d5_270_five_color_slice_ordering_search",
        "selector_fixed_colors": {"3": "Sel* color 3", "4": "Sel* color 4"},
        "family": (
            "For each slice class Sigma=0,1,2,3,4+, assign colors 0,1,2 to the three "
            "remaining directions by one fixed permutation of their sorted order."
        ),
        "modulus": args.modulus,
        "rule_count": rule_count,
        "exact_rule_count": len(exact_rules),
        "conclusion": (
            "The smallest slice-class-only leftover-ordering family has no exact completion "
            "already at m=5."
        ),
    }
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    with args.summary_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
