#!/usr/bin/env python3
"""Search exact residual families by only refining promoted-collar support classes.

This is a case-reduced follow-up to the d5_291 campaign plan.

We start from the best exact family recorded by d5_281 and only allow the
local rule to change on classes that lie on a crude promoted-collar support
surrogate:

- top interior:         d = m-1, c != m-2, e != m-1
- double-top interior:  d = m-1, c != m-2, e =  m-1
- top hinge:            c = d = m-2, e != m-1
- double hinge:         c = d = m-2, e =  m-1

All other classes are frozen to the d5_281 control rule.

The search objective is no longer "maximize the number of Hamilton colors".
Instead, we score candidates by the cycle structure of the color-1 P0 return on
resonant moduli.  This is an operational proxy for the current
"change the reduced base permutation" frontier.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from ortools.sat.python import cp_model

from torus_nd_d5_routee_line_bit_search_281 import (
    DEFAULT_DETAIL_DIR as LINEBIT_DETAIL_DIR,
    PERM_INDEX,
    PERMS,
    class_name as base_class_name,
    family_key as base_family_key,
)
from torus_nd_d5_selector_star_common_119 import states_P0, selector_perm_star


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_293_resonant_support_refinement_search_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_293_resonant_support_refinement_search"


def promoted_code(m: int, x: tuple[int, int, int, int, int]) -> int:
    c, d, e = x[2], x[3], x[4]
    if d == m - 1 and c != m - 2 and e != m - 1:
        return 1
    if d == m - 1 and c != m - 2 and e == m - 1:
        return 2
    if c == m - 2 and d == m - 2 and e != m - 1:
        return 3
    if c == m - 2 and d == m - 2 and e == m - 1:
        return 4
    return 0


PROMOTED_LABEL = {
    0: "bulk",
    1: "top",
    2: "double",
    3: "hinge_top",
    4: "hinge_double",
}


def family_key(m: int, x: tuple[int, int, int, int, int]) -> tuple[object, ...]:
    return base_family_key(m, x) + (promoted_code(m, x),)


def class_name(key: tuple[object, ...]) -> str:
    return f"{base_class_name(key[:-1])}|PC:{PROMOTED_LABEL[key[-1]]}"


def build_keys(moduli: list[int]) -> list[tuple[object, ...]]:
    keys: set[tuple[object, ...]] = set()
    for m in moduli:
        for x in itertools.product(range(m), repeat=5):
            keys.add(family_key(m, x))
    return sorted(keys, key=str)


def load_control_rule() -> dict[tuple[object, ...], tuple[int, int, int]]:
    payload = json.loads((LINEBIT_DETAIL_DIR / "search.json").read_text(encoding="utf-8"))
    rule_json = payload["best_solution"]["rule"]
    rule: dict[tuple[object, ...], tuple[int, int, int]] = {}
    key_moduli = payload["key_moduli"]
    # Reconstruct the exact key set used in d5_281.
    base_keys: set[tuple[object, ...]] = set()
    for m in key_moduli:
        for x in itertools.product(range(m), repeat=5):
            base_keys.add(base_family_key(m, x))
    for key in base_keys:
        rule[key] = tuple(rule_json[base_class_name(key)])
    return rule


def baseline_perm_for_key(
    control_rule: dict[tuple[object, ...], tuple[int, int, int]],
    key: tuple[object, ...],
) -> tuple[int, int, int]:
    base_key = key[:-1]
    if base_key in control_rule:
        return control_rule[base_key]
    coarse_prefix = base_key[:2]
    candidates = [perm for other_key, perm in control_rule.items() if other_key[:2] == coarse_prefix]
    if candidates:
        return candidates[0]
    raise KeyError(f"no baseline control permutation for key {base_key}")


def build_patterns(
    moduli: list[int],
    key_to_idx: dict[tuple[object, ...], int],
) -> list[list[tuple[int, tuple[int, ...]]]]:
    patterns: list[list[tuple[int, tuple[int, ...]]]] = []
    seen: set[tuple[tuple[int, tuple[int, ...]], ...]] = set()
    for m in moduli:
        for y in itertools.product(range(m), repeat=5):
            row: list[tuple[int, tuple[int, ...]]] = []
            for j in range(5):
                x = list(y)
                x[j] = (x[j] - 1) % m
                x_t = tuple(x)
                key = family_key(m, x_t)
                p_star = selector_perm_star(m, x_t)
                used = {p_star[3], p_star[4]}
                if j == p_star[3]:
                    table = (3, 3, 3, 3, 3, 3)
                elif j == p_star[4]:
                    table = (4, 4, 4, 4, 4, 4)
                else:
                    rem = sorted(d for d in range(5) if d not in used)
                    slot = rem.index(j)
                    table = tuple(perm.index(slot) for perm in PERMS)
                row.append((key_to_idx[key], table))
            signature = tuple(row)
            if signature not in seen:
                seen.add(signature)
                patterns.append(row)
    return patterns


def build_model(
    keys: list[tuple[object, ...]],
    patterns: list[list[tuple[int, tuple[int, ...]]]],
    control_rule: dict[tuple[object, ...], tuple[int, int, int]],
) -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    model = cp_model.CpModel()
    vars_by_key = [model.NewIntVar(0, 5, f"k{i}") for i in range(len(keys))]
    for idx, key in enumerate(keys):
        baseline = PERM_INDEX[baseline_perm_for_key(control_rule, key)]
        if key[-1] == 0:
            model.Add(vars_by_key[idx] == baseline)
    key_to_idx = {key: idx for idx, key in enumerate(keys)}
    # Keep the canonical S0 bulk class fixed as identity.
    model.Add(vars_by_key[key_to_idx[("S0", 0, 0, 0, 0, 0)]] == PERM_INDEX[(0, 1, 2)])
    for row in patterns:
        colors: list[cp_model.IntVar] = []
        for key_idx, table in row:
            cvar = model.NewIntVar(0, 4, "")
            model.AddElement(vars_by_key[key_idx], list(table), cvar)
            colors.append(cvar)
        model.AddAllDifferent(colors)
    return model, vars_by_key


def selector_from_solution(
    solution: list[int],
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    m: int,
    x: tuple[int, int, int, int, int],
) -> tuple[int, int, int, int, int]:
    p_star = selector_perm_star(m, x)
    used = {p_star[3], p_star[4]}
    rem = sorted(d for d in range(5) if d not in used)
    perm = PERMS[solution[key_to_idx[family_key(m, x)]]]
    out = [None] * 5
    out[3] = p_star[3]
    out[4] = p_star[4]
    for color, rem_index in zip((0, 1, 2), perm):
        out[color] = rem[rem_index]
    return tuple(out)


def color_step(
    solution: list[int],
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    m: int,
    color: int,
    point: tuple[int, int, int, int, int],
) -> tuple[int, int, int, int, int]:
    cur = list(point)
    direction = selector_from_solution(solution, keys, key_to_idx, m, point)[color]
    cur[direction] = (cur[direction] + 1) % m
    return tuple(cur)


def p0_return_histogram(
    solution: list[int],
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    m: int,
    color: int = 1,
) -> dict[str, int]:
    points = list(states_P0(m))
    index_of = {point: idx for idx, point in enumerate(points)}
    perm = [0] * len(points)
    for idx, point in enumerate(points):
        cur = point
        for _ in range(m):
            cur = color_step(solution, keys, key_to_idx, m, color, cur)
        perm[idx] = index_of[cur]
    seen = [False] * len(points)
    hist: dict[int, int] = {}
    for start in range(len(points)):
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


def exact_check(
    solution: list[int],
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
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
                    "source_class": class_name(family_key(m, x_t)),
                    "source_selector": list(selector),
                }
            colors.append(incoming[0])
        if sorted(colors) != [0, 1, 2, 3, 4]:
            return False, {"type": "target_not_latin", "target": list(y), "incoming_colors": colors}
    return True, None


def cycle_summary(hist: dict[str, int]) -> tuple[int, int]:
    return sum(hist.values()), max(int(length) for length in hist)


class SearchCallback(cp_model.CpSolverSolutionCallback):
    def __init__(
        self,
        vars_by_key: list[cp_model.IntVar],
        keys: list[tuple[object, ...]],
        key_to_idx: dict[tuple[object, ...], int],
        evaluation_moduli: list[int],
        solution_limit: int,
    ) -> None:
        super().__init__()
        self.vars_by_key = vars_by_key
        self.keys = keys
        self.key_to_idx = key_to_idx
        self.evaluation_moduli = evaluation_moduli
        self.solution_limit = solution_limit
        self.solution_index = 0
        self.best_score: tuple[int, int, int, int] | None = None
        self.best_payload: dict[str, object] | None = None

    def on_solution_callback(self) -> None:
        self.solution_index += 1
        solution = [self.Value(v) for v in self.vars_by_key]
        by_modulus: dict[str, object] = {}
        score_parts: list[int] = []
        for m in self.evaluation_moduli:
            hist = p0_return_histogram(solution, self.keys, self.key_to_idx, m, color=1)
            cycle_count, largest = cycle_summary(hist)
            by_modulus[str(m)] = {
                "p0_return_histogram_color1": hist,
                "cycle_count": cycle_count,
                "largest_cycle": largest,
            }
            score_parts.extend([-cycle_count, largest])
        score = tuple(score_parts)
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_payload = {
                "solution_index": self.solution_index,
                "score": list(score),
                "by_modulus": by_modulus,
                "rule": {
                    class_name(key): list(PERMS[solution[self.key_to_idx[key]]])
                    for key in self.keys
                    if key[-1] != 0
                },
            }
            print(
                json.dumps(
                    {
                        "solution_index": self.solution_index,
                        "score": list(score),
                        "by_modulus": {
                            modulus: {
                                "cycle_count": payload["cycle_count"],
                                "largest_cycle": payload["largest_cycle"],
                            }
                            for modulus, payload in by_modulus.items()
                        },
                    }
                ),
                flush=True,
            )
        if self.solution_index >= self.solution_limit:
            self.StopSearch()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search promoted-support refinements of the d5_281 control family."
    )
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    parser.add_argument("--search-moduli", nargs="*", type=int, default=[7, 9, 11])
    parser.add_argument("--evaluation-moduli", nargs="*", type=int, default=[15, 9])
    parser.add_argument("--promotion-moduli", nargs="*", type=int, default=[13])
    parser.add_argument("--solution-limit", type=int, default=40)
    parser.add_argument("--max-seconds", type=float, default=60.0)
    args = parser.parse_args()

    control_rule = load_control_rule()
    key_moduli = sorted(set(args.search_moduli) | set(args.evaluation_moduli) | set(args.promotion_moduli))
    keys = build_keys(key_moduli)
    key_to_idx = {key: idx for idx, key in enumerate(keys)}
    patterns = build_patterns(args.search_moduli, key_to_idx)
    model, vars_by_key = build_model(keys, patterns, control_rule)

    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = args.max_seconds

    cb = SearchCallback(
        vars_by_key,
        keys,
        key_to_idx,
        evaluation_moduli=args.evaluation_moduli,
        solution_limit=args.solution_limit,
    )
    solver.SearchForAllSolutions(model, cb)
    if cb.best_payload is None or cb.best_score is None:
        raise RuntimeError("resonant support refinement search produced no solution")

    best_rule_map = cb.best_payload["rule"]
    best_solution = [baseline_perm_for_key(control_rule, key) for key in keys]
    best_solution_idx = [PERM_INDEX[perm] for perm in best_solution]
    for idx, key in enumerate(keys):
        if key[-1] != 0:
            label = class_name(key)
            if label in best_rule_map:
                best_solution_idx[idx] = PERM_INDEX[tuple(best_rule_map[label])]

    control_by_modulus = {
        str(m): p0_return_histogram(
            [PERM_INDEX[baseline_perm_for_key(control_rule, key)] for key in keys],
            keys,
            key_to_idx,
            m,
            color=1,
        )
        for m in args.evaluation_moduli
    }
    promotion_exact = {
        str(m): exact_check(best_solution_idx, keys, key_to_idx, m)
        for m in args.promotion_moduli
    }

    summary = {
        "task": "d5_293_resonant_support_refinement_search",
        "family": (
            "Start from the d5_281 best exact family and only allow changes on "
            "classes lying in a promoted-collar support surrogate "
            "(top, double-top, top hinge, double hinge)."
        ),
        "search_moduli": args.search_moduli,
        "evaluation_moduli": args.evaluation_moduli,
        "promotion_moduli": args.promotion_moduli,
        "key_moduli": key_moduli,
        "key_count": len(keys),
        "pattern_count": len(patterns),
        "support_key_count": sum(1 for key in keys if key[-1] != 0),
        "support_base_key_count": len({key[:-1] for key in keys if key[-1] != 0}),
        "solution_limit": args.solution_limit,
        "max_seconds": args.max_seconds,
        "control_p0_color1": {
            modulus: {
                "histogram": hist,
                "cycle_count": cycle_summary(hist)[0],
                "largest_cycle": cycle_summary(hist)[1],
            }
            for modulus, hist in control_by_modulus.items()
        },
        "best_score": list(cb.best_score),
        "best_solution": cb.best_payload,
        "promotion_exact": {
            modulus: {"exact": ok, "failure_witness": witness}
            for modulus, (ok, witness) in promotion_exact.items()
        },
        "conclusion": (
            "The resonant-support refinement search freezes the bulk rule and only varies "
            "promoted-collar-support classes. It should be read as a case-reduced search "
            "for candidates that improve the color-1 resonant P0 return, not as a final theorem."
        ),
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.detail_dir / "search.json").write_text(
        json.dumps(
            {
                "search_moduli": args.search_moduli,
                "evaluation_moduli": args.evaluation_moduli,
                "promotion_moduli": args.promotion_moduli,
                "key_moduli": key_moduli,
                "key_count": len(keys),
                "pattern_count": len(patterns),
                "support_key_count": sum(1 for key in keys if key[-1] != 0),
                "support_base_key_count": len({key[:-1] for key in keys if key[-1] != 0}),
                "solution_limit": args.solution_limit,
                "max_seconds": args.max_seconds,
                "best_solution": cb.best_payload,
                "control_p0_color1": control_by_modulus,
                "promotion_exact": {
                    modulus: {"exact": ok, "failure_witness": witness}
                    for modulus, (ok, witness) in promotion_exact.items()
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
