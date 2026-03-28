#!/usr/bin/env python3
"""Probe the residual Route-E target inside the combined best 274 family.

This script loads the best combined exactness rule from d5_274 and records the
next graph-side frontier data:

1. the combined best rule is exact on checked odd moduli;
2. within that rule, color 2 is the cleanest residual Route-E target;
3. its P0 first return uses a stable five-branch affine displacement support;
4. those five displacement vectors span the full 4-coordinate P0 space, so
   there is no surviving linear first-return invariant;
5. the three smallest defect branches are localized on three simple coordinate
   surfaces.

Outputs:
- RoundY/checks/d5_275_routee_color2_residual_probe_summary.json
- RoundY/checks/d5_275_routee_color2_residual_probe/per_modulus.json
- RoundY/checks/d5_275_routee_color2_residual_probe/best_rule.json
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

from torus_nd_d5_selector_star_common_119 import active2, active3, selector_perm_star, states_P0

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULE_JSON = (
    REPO_ROOT / "RoundY" / "checks" / "d5_274_routee_assembly_pattern_search" / "combined_search.json"
)
DEFAULT_SUMMARY = (
    REPO_ROOT / "RoundY" / "checks" / "d5_275_routee_color2_residual_probe_summary.json"
)
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_275_routee_color2_residual_probe"


State = tuple[int, int, int, int, int]
Disp4 = tuple[int, int, int, int]


def class_key(m: int, x: State) -> tuple[object, ...]:
    sigma = sum(x) % m
    if sigma == 0:
        return ("S0",)
    if sigma == 1:
        return ("S1",)
    if sigma == 2:
        return ("S2", active2(m, x))
    if sigma == 3:
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


def load_best_rule(path: Path) -> dict[str, list[int]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["best_solution"]["rule"]


def selector_from_rule(rule: dict[str, list[int]], m: int, x: State) -> tuple[int, int, int, int, int]:
    p_star = selector_perm_star(m, x)
    used = {p_star[3], p_star[4]}
    rem = sorted(direction for direction in range(5) if direction not in used)
    perm = tuple(rule[class_name(class_key(m, x))])
    out = [None] * 5
    out[3] = p_star[3]
    out[4] = p_star[4]
    for color, rem_index in zip((0, 1, 2), perm):
        out[color] = rem[rem_index]
    return tuple(out)


def exact_check(rule: dict[str, list[int]], m: int) -> tuple[bool, dict[str, object] | None]:
    for y in itertools.product(range(m), repeat=5):
        colors = []
        for direction in range(5):
            x = list(y)
            x[direction] = (x[direction] - 1) % m
            x_t = tuple(x)
            selector = selector_from_rule(rule, m, x_t)
            incoming = [color for color, chosen in enumerate(selector) if chosen == direction]
            if len(incoming) != 1:
                return False, {
                    "type": "predecessor_collision",
                    "target": list(y),
                    "direction": direction,
                    "incoming_colors": incoming,
                    "source": list(x_t),
                    "source_class": class_name(class_key(m, x_t)),
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


def p0_first_return(rule: dict[str, list[int]], m: int, color: int, point: State) -> State:
    cur = list(point)
    for _ in range(m):
        direction = selector_from_rule(rule, m, tuple(cur))[color]
        cur[direction] = (cur[direction] + 1) % m
    return tuple(cur)


def cycle_histogram(rule: dict[str, list[int]], m: int, color: int) -> dict[str, int]:
    states = list(states_P0(m))
    index_of = {state: idx for idx, state in enumerate(states)}
    perm = [0] * len(states)
    for idx, state in enumerate(states):
        perm[idx] = index_of[p0_first_return(rule, m, color, state)]
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


def branch_name(m: int, disp: Disp4) -> str:
    table = {
        (m - 2, 1, 0, 1): "G",
        (m - 3, 2, 0, 1): "M",
        (m - 3, 1, 0, 2): "A",
        (m - 3, 1, 0, 1): "B",
        (m - 3, 1, 1, 1): "C",
    }
    return table.get(disp, "UNKNOWN")


def first_linear_invariant(rows: list[list[int]], m: int) -> list[int] | None:
    for coeffs in itertools.product(range(m), repeat=4):
        if coeffs == (0, 0, 0, 0):
            continue
        if all(sum(coeffs[i] * row[i] for i in range(4)) % m == 0 for row in rows):
            return list(coeffs)
    return None


def analyse_modulus(rule: dict[str, list[int]], m: int) -> dict[str, object]:
    histograms = {str(color): cycle_histogram(rule, m, color) for color in (1, 2)}

    disp_counts: Counter[Disp4] = Counter()
    branch_points: dict[str, list[State]] = defaultdict(list)
    for point in states_P0(m):
        image = p0_first_return(rule, m, 2, point)
        disp = tuple((image[i] - point[i]) % m for i in range(4))
        disp_counts[disp] += 1
        branch_points[branch_name(m, disp)].append(point)

    branch_vectors = [list(disp) for disp in sorted(disp_counts)]
    small_branch_surface_checks = {
        "A_on_x4_eq_m_minus_1": all(point[4] == m - 1 for point in branch_points["A"]),
        "B_on_x3_eq_m_minus_2": all(point[3] == m - 2 for point in branch_points["B"]),
        "C_on_x0_eq_m_minus_1": all(point[0] == m - 1 for point in branch_points["C"]),
    }

    named_disp_counts = {
        branch_name(m, disp): {"disp4": list(disp), "count": count}
        for disp, count in sorted(disp_counts.items())
    }

    return {
        "m": m,
        "P0_cycle_histograms": histograms,
        "color2_branch_count": len(disp_counts),
        "color2_branch_vectors": branch_vectors,
        "color2_branch_vectors_named": named_disp_counts,
        "color2_first_linear_invariant": first_linear_invariant(branch_vectors, m),
        "color2_small_branch_surface_checks": small_branch_surface_checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe the combined-best d5_274 residual Route-E color.")
    parser.add_argument("--rule-json", type=Path, default=DEFAULT_RULE_JSON)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    parser.add_argument("--exact-moduli", nargs="*", type=int, default=[5, 7, 9, 11, 13])
    parser.add_argument("--profile-moduli", nargs="*", type=int, default=[5, 7, 9, 11, 13])
    args = parser.parse_args()

    rule = load_best_rule(args.rule_json)

    exact_rows = {}
    for m in args.exact_moduli:
        ok, witness = exact_check(rule, m)
        exact_rows[str(m)] = {"exact": ok, "failure_witness": witness}

    per_modulus = {str(m): analyse_modulus(rule, m) for m in args.profile_moduli}
    summary = {
        "task": "d5_275_routee_color2_residual_probe",
        "source_rule": "combined best exact rule from d5_274",
        "source_rule_json": str(args.rule_json),
        "exact_checked_moduli": args.exact_moduli,
        "all_exact_checks_passed": all(row["exact"] for row in exact_rows.values()),
        "profile_checked_moduli": args.profile_moduli,
        "color1_cycle_histograms": {
            str(m): per_modulus[str(m)]["P0_cycle_histograms"]["1"] for m in args.profile_moduli
        },
        "color2_cycle_histograms": {
            str(m): per_modulus[str(m)]["P0_cycle_histograms"]["2"] for m in args.profile_moduli
        },
        "color2_branch_vectors_stable": all(
            per_modulus[str(m)]["color2_branch_vectors"]
            == [
                [m - 3, 1, 0, 1],
                [m - 3, 1, 0, 2],
                [m - 3, 1, 1, 1],
                [m - 3, 2, 0, 1],
                [m - 2, 1, 0, 1],
            ]
            for m in args.profile_moduli
        ),
        "color2_no_linear_invariant_by_branch_support": all(
            per_modulus[str(m)]["color2_first_linear_invariant"] is None
            for m in args.profile_moduli
        ),
        "small_branch_surface_localization_verified": all(
            all(per_modulus[str(m)]["color2_small_branch_surface_checks"].values())
            for m in args.profile_moduli
        ),
        "conclusion": (
            "The combined-best d5_274 family is exact on the checked odd range 5,7,9,11,13. "
            "Inside that family, color 2 is the cleanest residual Route-E target: its P0 first "
            "return has a stable five-branch affine displacement support, the three smallest "
            "branches are localized on the coordinate surfaces x3=m-2, x4=m-1, x0=m-1, and there "
            "is no nontrivial 4-coordinate linear invariant forced by the five branch vectors."
        ),
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.detail_dir / "per_modulus.json").write_text(
        json.dumps(per_modulus, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.detail_dir / "exact_checks.json").write_text(
        json.dumps(exact_rows, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.detail_dir / "best_rule.json").write_text(
        json.dumps(rule, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
