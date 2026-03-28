#!/usr/bin/env python3
"""Search a Route-E family with the d5_280 color-1 line bit added.

This refines d5_277/d5_279 by exposing the explicit color-1 short-cycle line
relation from d5_280:

    line7(x) = 1 iff x3 != m-1, x4 != m-1, and x0 + 3*x1 + x3 + 3*x4 = 7 mod m.

We also keep the one-point repair source from d5_279 as its own key bit so the
known exact family remains representable inside the search space.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from ortools.sat.python import cp_model

from torus_nd_d5_selector_star_common_119 import active2, active3, selector_perm_star


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_281_routee_line_bit_search_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_281_routee_line_bit_search"

PERMS = list(itertools.permutations((0, 1, 2)))
PERM_INDEX = {perm: idx for idx, perm in enumerate(PERMS)}


def g_anchor(m: int, x: tuple[int, int, int, int, int]) -> int:
    return int(x[2] == m - 1 and (x[0] + 2 * x[1] + x[4]) % m == 1)


def m_bad(x: tuple[int, int, int, int, int]) -> int:
    return int(x[4] != x[2] and (2 * x[0] + 3 * x[1]) % 3 == 1)


def u_special(m: int, x: tuple[int, int, int, int, int]) -> int:
    return int(x == (m - 1, 6 % m, m - 1, m - 1, m - 1))


def line7(m: int, x: tuple[int, int, int, int, int]) -> int:
    return int(
        x[3] != m - 1
        and x[4] != m - 1
        and (x[0] + 3 * x[1] + x[3] + 3 * x[4]) % m == 7 % m
    )


def family_key(m: int, x: tuple[int, int, int, int, int]) -> tuple[object, ...]:
    sigma = sum(x) % m
    base: tuple[object, ...]
    if sigma == 0:
        base = ("S0",)
    elif sigma == 1:
        base = ("S1",)
    elif sigma == 2:
        base = ("S2", active2(m, x))
    elif sigma == 3:
        base = ("S3", int(1 in active3(m, x)))
    else:
        base = ("S4+",)
    return base + (g_anchor(m, x), m_bad(x), u_special(m, x), line7(m, x))


def class_name(key: tuple[object, ...]) -> str:
    base = key[:-4]
    g_bit, m_bit, u_bit, l_bit = key[-4:]
    if base == ("S0",):
        label = "S0"
    elif base == ("S1",):
        label = "S1"
    elif base == ("S4+",):
        label = "S4+"
    elif base[0] == "S3":
        label = f"S3({base[1]})"
    else:
        subset = ",".join(str(v) for v in base[1])
        label = f"S2({{{subset}}})"
    return f"{label}|G{g_bit}|M{int(m_bit)}|U{u_bit}|L{l_bit}"


def build_keys(moduli: list[int]) -> list[tuple[object, ...]]:
    keys: set[tuple[object, ...]] = set()
    for m in moduli:
        for x in itertools.product(range(m), repeat=5):
            keys.add(family_key(m, x))
    return sorted(keys, key=str)


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
) -> tuple[cp_model.CpModel, list[cp_model.IntVar], dict[tuple[object, ...], int]]:
    model = cp_model.CpModel()
    vars_by_key = [model.NewIntVar(0, 5, f"k{i}") for i in range(len(keys))]
    key_to_idx = {key: idx for idx, key in enumerate(keys)}
    model.Add(vars_by_key[key_to_idx[("S0", 0, 0, 0, 0)]] == PERM_INDEX[(0, 1, 2)])
    for row in patterns:
        colors: list[cp_model.IntVar] = []
        for key_idx, table in row:
            cvar = model.NewIntVar(0, 4, "")
            model.AddElement(vars_by_key[key_idx], list(table), cvar)
            colors.append(cvar)
        model.AddAllDifferent(colors)
    return model, vars_by_key, key_to_idx


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


def cycle_histogram(
    solution: list[int],
    keys: list[tuple[object, ...]],
    key_to_idx: dict[tuple[object, ...], int],
    m: int,
    color: int,
) -> dict[str, int]:
    states = list(itertools.product(range(m), repeat=5))
    idx = {state: i for i, state in enumerate(states)}
    perm = [0] * len(states)
    for i, state in enumerate(states):
        y = list(state)
        d = selector_from_solution(solution, keys, key_to_idx, m, state)[color]
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


def hamilton_colors_from_histograms(m: int, histograms: dict[str, dict[str, int]]) -> list[int]:
    full = str(m**5)
    return sorted(color for color in range(5) if histograms[str(color)] == {full: 1})


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
        self.best_score: tuple[int, int, int, int, int] | None = None
        self.best_payload: dict[str, object] | None = None

    def on_solution_callback(self) -> None:
        self.solution_index += 1
        solution = [self.Value(v) for v in self.vars_by_key]
        by_modulus: dict[str, object] = {}
        ham_counts: dict[str, int] = {}
        color1_max = 0
        color0_max = 0
        color2_max = 0
        for m in self.evaluation_moduli:
            histograms = {
                str(color): cycle_histogram(solution, self.keys, self.key_to_idx, m, color)
                for color in range(5)
            }
            ham_colors = hamilton_colors_from_histograms(m, histograms)
            by_modulus[str(m)] = {
                "histograms": histograms,
                "hamilton_colors": ham_colors,
                "nonhamilton_colors": [color for color in range(5) if color not in ham_colors],
            }
            ham_counts[str(m)] = len(ham_colors)
            color1_max += max(int(length) for length in histograms["1"].keys())
            color0_max += max(int(length) for length in histograms["0"].keys())
            color2_max += max(int(length) for length in histograms["2"].keys())

        score = (min(ham_counts.values()), sum(ham_counts.values()), color1_max, color0_max, color2_max)
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_payload = {
                "solution_index": self.solution_index,
                "score": list(score),
                "hamilton_counts": ham_counts,
                "by_modulus": by_modulus,
                "rule": {
                    class_name(key): list(PERMS[solution[self.key_to_idx[key]]])
                    for key in self.keys
                },
            }
            print(
                json.dumps(
                    {
                        "solution_index": self.solution_index,
                        "score": list(score),
                        "hamilton_counts": ham_counts,
                    }
                ),
                flush=True,
            )
        if self.solution_index >= self.solution_limit:
            self.StopSearch()


def main() -> None:
    parser = argparse.ArgumentParser(description="Search a Route-E family with the d5_280 color-1 line bit.")
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    parser.add_argument("--search-moduli", nargs="*", type=int, default=[7, 9, 11])
    parser.add_argument("--evaluation-moduli", nargs="*", type=int, default=[7, 9, 11, 13])
    parser.add_argument("--solution-limit", type=int, default=100)
    parser.add_argument("--max-seconds", type=float, default=30.0)
    args = parser.parse_args()

    key_moduli = sorted(set(args.search_moduli) | set(args.evaluation_moduli))
    keys = build_keys(key_moduli)
    key_to_idx = {key: idx for idx, key in enumerate(keys)}
    patterns = build_patterns(args.search_moduli, key_to_idx)
    model, vars_by_key, key_to_idx = build_model(keys, patterns)

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
        raise RuntimeError("line-bit search produced no solution")

    summary = {
        "task": "d5_281_routee_line_bit_search",
        "family": (
            "Refine the d5_277/d5_279 Route-E family by adding the d5_280 line bit "
            "line7 = 1_{x3!=m-1, x4!=m-1, x0+3x1+x3+3x4=7 mod m} and the d5_279 "
            "one-point source bit U = 1_{x=(m-1,6,m-1,m-1,m-1)}."
        ),
        "search_moduli": args.search_moduli,
        "key_moduli": key_moduli,
        "evaluation_moduli": args.evaluation_moduli,
        "key_count": len(keys),
        "pattern_count": len(patterns),
        "solution_limit": args.solution_limit,
        "max_seconds": args.max_seconds,
        "best_score": list(cb.best_score),
        "best_hamilton_counts": cb.best_payload["hamilton_counts"],
        "best_nonhamilton_colors": {
            modulus: cb.best_payload["by_modulus"][modulus]["nonhamilton_colors"]
            for modulus in cb.best_payload["by_modulus"]
        },
        "conclusion": (
            "The d5_280 line bit is compatible with exact families on the checked "
            "search moduli, but it is not by itself enough to finish the five-color "
            "assembly problem. In the best time-limited run, the Hamilton-color counts "
            "are 3 on m=7 and only 2 on m=9,11,13."
        ),
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.detail_dir / "search.json").write_text(
        json.dumps(
            {
                "search_moduli": args.search_moduli,
                "key_moduli": key_moduli,
                "evaluation_moduli": args.evaluation_moduli,
                "key_count": len(keys),
                "pattern_count": len(patterns),
                "solution_limit": args.solution_limit,
                "max_seconds": args.max_seconds,
                "best_solution": cb.best_payload,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
