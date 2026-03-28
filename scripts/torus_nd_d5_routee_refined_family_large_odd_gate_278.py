#!/usr/bin/env python3
"""Check the best d5_277 refined family against the next odd moduli.

This script packages the honest follow-up to d5_277:

- load the best refined-family rule from the default d5_277 search;
- check exactness on m = 11, 13;
- record the first failure witness when exactness breaks;
- record how the refined family key count and local-pattern count grow when
  the search moduli are enlarged from 7/9 to 7/9/11 to 7/9/11/13.
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
    build_patterns,
    class_name,
    family_key,
    selector_from_solution,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = (
    REPO_ROOT / "RoundY" / "checks" / "d5_278_routee_refined_family_large_odd_gate_summary.json"
)
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_278_routee_refined_family_large_odd_gate"


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
            selector = selector_from_solution(solution, keys, key_to_idx, m, x_t)
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Check the best d5_277 refined family at the next odd moduli.")
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    parser.add_argument("--gate-moduli", nargs="*", type=int, default=[11, 13])
    args = parser.parse_args()

    keys, key_to_idx, solution = load_solution()
    gate_rows = {str(m): exact_check(keys, key_to_idx, solution, m) for m in args.gate_moduli}

    key_counts = {
        "5_7_9": len(build_keys([5, 7, 9])),
        "5_7_9_11": len(build_keys([5, 7, 9, 11])),
        "5_7_9_11_13": len(build_keys([5, 7, 9, 11, 13])),
    }
    pattern_counts = {
        "7_9": len(build_patterns([7, 9], {k: i for i, k in enumerate(build_keys([5, 7, 9]))})),
        "7_9_11": len(build_patterns([7, 9, 11], {k: i for i, k in enumerate(build_keys([5, 7, 9, 11]))})),
        "7_9_11_13": len(build_patterns([7, 9, 11, 13], {k: i for i, k in enumerate(build_keys([5, 7, 9, 11, 13]))})),
    }

    detail_rows = {
        modulus: {"exact": ok, "failure_witness": witness}
        for modulus, (ok, witness) in gate_rows.items()
    }
    summary = {
        "task": "d5_278_routee_refined_family_large_odd_gate",
        "source_rule": "best d5_277 refined-family rule",
        "checked_gate_moduli": args.gate_moduli,
        "all_gate_checks_passed": all(ok for ok, _ in gate_rows.values()),
        "key_counts": key_counts,
        "pattern_counts": pattern_counts,
        "conclusion": (
            "The best d5_277 refined-family rule improves the checked 7/9 behavior, "
            "but it does not yet close the large-odd exactness gate. The refined key set "
            "stabilizes by m=11, while the local exactness pattern count still grows from "
            "514 to 552 to 560 across 7/9, 7/9/11, and 7/9/11/13."
        ),
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.detail_dir / "gate_checks.json").write_text(
        json.dumps(detail_rows, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
