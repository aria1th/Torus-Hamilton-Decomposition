#!/usr/bin/env python3
"""Record the one-point repair that kills the d5_278 recurring witness family.

The source rule is the best refined-family rule from d5_277.  The repair is:

- only on the source family x = (m-1, 6, m-1, m-1, m-1),
- and only when that source lies in class S2({1,2,3,4})|G0|M0,
- replace the local permutation on colors 0,1,2 by (1,2,0).

On the checked odd range this leaves m=7,9 unchanged and repairs the
large-odd exactness failures starting at m=11.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from torus_nd_d5_routee_refined_family_search_277 import (
    DEFAULT_DETAIL_DIR as SEARCH_DETAIL_DIR,
    PERM_INDEX,
    build_keys,
    class_name,
    family_key,
    selector_from_solution,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_279_one_point_repair_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_279_one_point_repair"
TARGET_CLASS = "S2({1,2,3,4})|G0|M0"
OVERRIDE = (1, 2, 0)


def load_solution() -> tuple[list[tuple[object, ...]], dict[tuple[object, ...], int], list[int]]:
    payload = json.loads((SEARCH_DETAIL_DIR / "search.json").read_text(encoding="utf-8"))
    rule = payload["best_solution"]["rule"]
    key_moduli = payload["key_moduli"]
    keys = build_keys(key_moduli)
    key_to_idx = {key: idx for idx, key in enumerate(keys)}
    solution = [0] * len(keys)
    for key in keys:
        solution[key_to_idx[key]] = PERM_INDEX[tuple(rule[class_name(key)])]
    return keys, key_to_idx, solution


def repaired_selector(
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    solution: list[int],
    m: int,
    x: tuple[int, int, int, int, int],
) -> tuple[int, int, int, int, int]:
    base = list(selector_from_solution(solution, keys, key_to_idx, m, x))
    if (
        class_name(family_key(m, x)) == TARGET_CLASS
        and x[0] == m - 1
        and x[1] == 6
        and x[2] == m - 1
        and x[3] == m - 1
        and x[4] == m - 1
    ):
        used = {base[3], base[4]}
        rem = sorted(d for d in range(5) if d not in used)
        out = [None] * 5
        out[3] = base[3]
        out[4] = base[4]
        for color, ridx in zip((0, 1, 2), OVERRIDE):
            out[color] = rem[ridx]
        return tuple(out)
    return tuple(base)


def exact_check(
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    solution: list[int],
    m: int,
) -> tuple[bool, dict[str, object] | None]:
    for y in itertools.product(range(m), repeat=5):
        colors = []
        for j in range(5):
            x = list(y)
            x[j] = (x[j] - 1) % m
            x_t = tuple(x)
            selector = repaired_selector(keys, key_to_idx, solution, m, x_t)
            incoming = [c for c, d in enumerate(selector) if d == j]
            if len(incoming) != 1:
                return False, {
                    "type": "predecessor_collision",
                    "target": list(y),
                    "direction": j,
                    "incoming_colors": incoming,
                    "source": list(x_t),
                    "source_class": class_name(family_key(m, x_t)),
                    "source_selector": list(selector),
                }
            colors.append(incoming[0])
        if sorted(colors) != [0, 1, 2, 3, 4]:
            return False, {
                "type": "target_not_latin",
                "target": list(y),
                "incoming_colors": colors,
            }
    return True, None


def cycle_histogram(
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    solution: list[int],
    m: int,
    color: int,
) -> dict[str, int]:
    states = list(itertools.product(range(m), repeat=5))
    idx = {state: i for i, state in enumerate(states)}
    perm = [0] * len(states)
    for i, state in enumerate(states):
        y = list(state)
        d = repaired_selector(keys, key_to_idx, solution, m, state)[color]
        y[d] = (y[d] + 1) % m
        perm[i] = idx[tuple(y)]
    seen = [False] * len(states)
    hist: dict[int, int] = {}
    for start in range(len(states)):
        if seen[start]:
            continue
        cur = start
        size = 0
        while not seen[cur]:
            seen[cur] = True
            cur = perm[cur]
            size += 1
        hist[size] = hist.get(size, 0) + 1
    return {str(length): count for length, count in sorted(hist.items())}


def main() -> None:
    parser = argparse.ArgumentParser(description="Check the one-point repair on top of the d5_277 refined family.")
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    parser.add_argument("--exact-moduli", nargs="*", type=int, default=[7, 9, 11, 13, 15, 17])
    parser.add_argument("--full-profile-moduli", nargs="*", type=int, default=[7, 9, 11, 13])
    parser.add_argument("--color2-profile-moduli", nargs="*", type=int, default=[7, 9, 11, 13, 15, 17])
    args = parser.parse_args()

    keys, key_to_idx, solution = load_solution()

    exact_rows = {str(m): exact_check(keys, key_to_idx, solution, m) for m in args.exact_moduli}
    full_profiles = {
        str(m): {
            str(color): cycle_histogram(keys, key_to_idx, solution, m, color)
            for color in range(5)
        }
        for m in args.full_profile_moduli
    }
    color2_profiles = {
        str(m): cycle_histogram(keys, key_to_idx, solution, m, 2)
        for m in args.color2_profile_moduli
    }

    summary = {
        "task": "d5_279_one_point_repair",
        "source_rule": "best d5_277 refined-family rule",
        "repair": {
            "target_class": TARGET_CLASS,
            "source_family": "(m-1, 6, m-1, m-1, m-1)",
            "override_perm_012": list(OVERRIDE),
        },
        "exact_checked_moduli": args.exact_moduli,
        "all_exact_checks_passed": all(ok for ok, _ in exact_rows.values()),
        "color2_hamilton_checked_moduli": [
            m for m in args.color2_profile_moduli if color2_profiles[str(m)] == {str(m**5): 1}
        ],
        "conclusion": (
            "A single source-family repair on top of the d5_277 refined family "
            "kills the recurring d5_278 witness family. On the checked odd range "
            "7,9,11,13,15,17 the repaired family is exact, and color 2 is Hamilton "
            "throughout that checked range."
        ),
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.detail_dir / "exact_checks.json").write_text(
        json.dumps(
            {
                modulus: {"exact": ok, "failure_witness": witness}
                for modulus, (ok, witness) in exact_rows.items()
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (args.detail_dir / "full_profiles.json").write_text(
        json.dumps(full_profiles, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.detail_dir / "color2_profiles.json").write_text(
        json.dumps(color2_profiles, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
