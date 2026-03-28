#!/usr/bin/env python3
"""Record the short-cycle structure of the d5_274 combined-best color-2 return.

We study the first return

    R_2 = (H_2)^m | P0

for the combined-best exact family from d5_274.

The goal is not to prove the final graph-side theorem. It is to isolate the
remaining non-Hamiltonicity into explicit short-cycle families.

Outputs:
- RoundY/checks/d5_276_routee_color2_short_cycle_structure_summary.json
- RoundY/checks/d5_276_routee_color2_short_cycle_structure/per_modulus.json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from torus_nd_d5_routee_color2_residual_probe_275 import (
    DEFAULT_RULE_JSON,
    State,
    branch_name,
    load_best_rule,
    p0_first_return,
    states_P0,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = (
    REPO_ROOT / "RoundY" / "checks" / "d5_276_routee_color2_short_cycle_structure_summary.json"
)
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_276_routee_color2_short_cycle_structure"


def cycle_decomposition(m: int) -> tuple[list[list[State]], dict[State, str]]:
    rule = load_best_rule(DEFAULT_RULE_JSON)
    states = list(states_P0(m))
    index_of = {state: idx for idx, state in enumerate(states)}
    perm = [0] * len(states)
    branch_of: dict[State, str] = {}
    for idx, state in enumerate(states):
        image = p0_first_return(rule, m, 2, state)
        perm[idx] = index_of[image]
        disp = tuple((image[i] - state[i]) % m for i in range(4))
        branch_of[state] = branch_name(m, disp)

    cycles: list[list[State]] = []
    seen = [False] * len(states)
    for start in range(len(states)):
        if seen[start]:
            continue
        cur = start
        cycle: list[State] = []
        while not seen[cur]:
            seen[cur] = True
            cycle.append(states[cur])
            cur = perm[cur]
        cycles.append(cycle)
    return cycles, branch_of


def pattern_name(pattern: tuple[tuple[str, int], ...]) -> str:
    if pattern and len(pattern) == 1 and pattern[0][0] in {"G", "M"}:
        return f"{pattern[0][0]}-only"
    return "mixed"


def analyse_modulus(m: int) -> dict[str, object]:
    cycles, branch_of = cycle_decomposition(m)
    short_cycles = [cycle for cycle in cycles if len(cycle) == m]
    long_cycles = [cycle for cycle in cycles if len(cycle) != m]

    short_pattern_counter: Counter[tuple[tuple[str, int], ...]] = Counter()
    g_by_x4: dict[int, set[int]] = defaultdict(set)
    g_bad_examples: list[dict[str, object]] = []
    m_by_x2: dict[int, set[int]] = defaultdict(set)
    m_bad_examples: list[dict[str, object]] = []

    for cycle in short_cycles:
        pattern = tuple(sorted(Counter(branch_of[state] for state in cycle).items()))
        short_pattern_counter[pattern] += 1

        if pattern == (("G", m),):
            x2_values = {state[2] for state in cycle}
            x4_values = {state[4] for state in cycle}
            if len(x2_values) != 1 or len(x4_values) != 1:
                g_bad_examples.append({"type": "nonconstant_slice", "cycle_head": list(cycle[0])})
                continue
            x2 = next(iter(x2_values))
            x4 = next(iter(x4_values))
            inv = (cycle[0][0] + 2 * cycle[0][1]) % m
            g_by_x4[x4].add(inv)
            if x2 != m - 1 or x4 == m - 1:
                g_bad_examples.append(
                    {
                        "type": "unexpected_G_location",
                        "cycle_head": list(cycle[0]),
                        "x2": x2,
                        "x4": x4,
                    }
                )

        if pattern == (("M", m),):
            x2_values = {state[2] for state in cycle}
            x4_values = {state[4] for state in cycle}
            if len(x2_values) != 1 or len(x4_values) != 1:
                m_bad_examples.append({"type": "nonconstant_slice", "cycle_head": list(cycle[0])})
                continue
            x2 = next(iter(x2_values))
            x4 = next(iter(x4_values))
            inv = (2 * cycle[0][0] + 3 * cycle[0][1]) % m
            m_by_x2[x2].add(inv)
            if x4 != m - 1 or x2 == m - 1:
                m_bad_examples.append(
                    {
                        "type": "unexpected_M_location",
                        "cycle_head": list(cycle[0]),
                        "x2": x2,
                        "x4": x4,
                    }
                )

    pattern_counts = {
        pattern_name(pattern): count for pattern, count in sorted(short_pattern_counter.items(), key=str)
    }

    g_expected = {
        x4: sorted(value for value in range(m) if value != (1 - x4) % m) for x4 in range(m - 1)
    }
    g_observed = {x4: sorted(values) for x4, values in sorted(g_by_x4.items())}
    g_parameterization_ok = g_observed == g_expected

    m_expected: dict[int, list[int]] = {}
    if m % 3 == 0:
        m_expected = {
            x2: [value for value in range(m) if value % 3 != 1] for x2 in range(m - 1)
        }
    m_observed = {x2: sorted(values) for x2, values in sorted(m_by_x2.items())}
    m_parameterization_ok = (not m_expected and not m_observed) or (m_observed == m_expected)

    return {
        "m": m,
        "cycle_length_histogram": {str(length): count for length, count in sorted(Counter(len(c) for c in cycles).items())},
        "short_cycle_count": len(short_cycles),
        "long_cycle_lengths": sorted(len(cycle) for cycle in long_cycles),
        "short_cycle_pattern_counts": pattern_counts,
        "G_only_expected_count": (m - 1) ** 2,
        "G_only_actual_count": pattern_counts.get("G-only", 0),
        "G_only_parameterization_verified": g_parameterization_ok and not g_bad_examples,
        "G_only_by_x4_invariant_values": g_observed,
        "M_only_expected_count": (m - 1) * (2 * m // 3) if m % 3 == 0 else 0,
        "M_only_actual_count": pattern_counts.get("M-only", 0),
        "M_only_parameterization_verified": m_parameterization_ok and not m_bad_examples,
        "M_only_by_x2_invariant_values": m_observed,
        "G_bad_examples": g_bad_examples[:10],
        "M_bad_examples": m_bad_examples[:10],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Record the short-cycle structure of the combined-best color-2 P0 return.")
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    parser.add_argument("--moduli", nargs="*", type=int, default=[5, 7, 9, 11, 13, 15, 17, 19, 21])
    args = parser.parse_args()

    per_modulus = {str(m): analyse_modulus(m) for m in args.moduli}
    summary = {
        "task": "d5_276_routee_color2_short_cycle_structure",
        "source_rule": "combined best exact rule from d5_274",
        "checked_moduli": args.moduli,
        "all_G_only_short_counts_match": all(
            per_modulus[str(m)]["G_only_actual_count"] == (m - 1) ** 2 for m in args.moduli
        ),
        "all_G_only_parameterizations_verified": all(
            per_modulus[str(m)]["G_only_parameterization_verified"] for m in args.moduli
        ),
        "all_M_only_counts_match": all(
            per_modulus[str(m)]["M_only_actual_count"]
            == ((m - 1) * (2 * m // 3) if m % 3 == 0 else 0)
            for m in args.moduli
        ),
        "all_M_only_parameterizations_verified": all(
            per_modulus[str(m)]["M_only_parameterization_verified"] for m in args.moduli
        ),
        "conclusion": (
            "For the combined-best d5_274 family, the non-Hamilton part of the color-2 P0 return "
            "is concentrated in explicit short-cycle families. A universal G-only family contributes "
            "(m-1)^2 short m-cycles and is parameterized by x2=m-1, x4!=m-1, and the invariant "
            "x0+2x1 != 1-x4. On checked moduli divisible by 3, there is an extra M-only family of "
            "(m-1)*(2m/3) short m-cycles on x4=m-1, x2!=m-1, parameterized by the invariant "
            "2x0+3x1 avoiding the residue class 1 mod 3."
        ),
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.detail_dir / "per_modulus.json").write_text(
        json.dumps(per_modulus, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
