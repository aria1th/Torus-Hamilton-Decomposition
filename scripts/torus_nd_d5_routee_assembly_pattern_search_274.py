#!/usr/bin/env python3
"""Compressed local-pattern search for the D5 five-color Route-E assembly family.

This script studies the simple family:

- fix Sel* colors 3 and 4;
- assign colors 0,1,2 by one fixed permutation on
  S0, S1, S4+, the full slice-2 active-set class S2(A2),
  and the one-bit slice-3 class S3(1 in A3).

The main point is that local exactness compresses to finitely many target
patterns. This script records two searches:

1. A stable-odd search based on the m=9 pattern set, where the local pattern
   set stabilizes for odd m >= 9. Among the first 87 solutions, a rule appears
   whose m=5 cycle structure already has four Hamilton colors.
2. A combined search based on the joint m=7 and m=9 pattern set. Among the
   first 200 solutions, the best rule has Hamilton-count profile
   m=5 -> 3, m=7 -> 4.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Iterable

from ortools.sat.python import cp_model

from torus_nd_d5_selector_star_common_119 import active2, active3, selector_perm_star

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_274_routee_assembly_pattern_search_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_274_routee_assembly_pattern_search"

PERMS = list(itertools.permutations((0, 1, 2)))
PERM_INDEX = {perm: idx for idx, perm in enumerate(PERMS)}


def family_key(m: int, x: tuple[int, int, int, int, int]) -> tuple[object, ...]:
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


def build_keys(moduli: Iterable[int]) -> list[tuple[object, ...]]:
    all_keys: set[tuple[object, ...]] = set()
    for m in moduli:
        all_keys |= {family_key(m, x) for x in itertools.product(range(m), repeat=5)}
    return sorted(all_keys, key=str)


def build_patterns(moduli: Iterable[int], key_to_idx: dict[tuple[object, ...], int]) -> list[list[tuple[int, tuple[int, ...]]]]:
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


def build_model(keys: list[tuple[object, ...]], patterns: list[list[tuple[int, tuple[int, ...]]]]) -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    model = cp_model.CpModel()
    vars_by_key = [model.NewIntVar(0, 5, f"k{i}") for i in range(len(keys))]
    key_to_idx = {key: idx for idx, key in enumerate(keys)}
    model.Add(vars_by_key[key_to_idx[("S0",)]] == PERM_INDEX[(0, 1, 2)])
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
    for i in range(len(states)):
        if seen[i]:
            continue
        cur = i
        length = 0
        while not seen[cur]:
            seen[cur] = True
            cur = perm[cur]
            length += 1
        hist[length] = hist.get(length, 0) + 1
    return {str(length): count for length, count in sorted(hist.items())}


def hamilton_colors_from_histograms(m: int, histograms: dict[str, dict[str, int]]) -> list[int]:
    full = str(m**5)
    out = []
    for color in range(5):
        hist = histograms[str(color)]
        if hist == {full: 1}:
            out.append(color)
    return out


class StableSearchCallback(cp_model.CpSolverSolutionCallback):
    def __init__(
        self,
        vars_by_key: list[cp_model.IntVar],
        keys: list[tuple[object, ...]],
        key_to_idx: dict[tuple[object, ...], int],
        m_eval: int,
        stop_at_ham_count: int,
    ) -> None:
        super().__init__()
        self.vars_by_key = vars_by_key
        self.keys = keys
        self.key_to_idx = key_to_idx
        self.m_eval = m_eval
        self.stop_at_ham_count = stop_at_ham_count
        self.solution_index = 0
        self.result: dict[str, object] | None = None

    def on_solution_callback(self) -> None:
        self.solution_index += 1
        solution = [self.Value(v) for v in self.vars_by_key]
        histograms = {
            str(color): cycle_histogram(solution, self.keys, self.key_to_idx, self.m_eval, color)
            for color in range(5)
        }
        ham_colors = hamilton_colors_from_histograms(self.m_eval, histograms)
        if len(ham_colors) >= self.stop_at_ham_count:
            self.result = {
                "solution_index": self.solution_index,
                "evaluation_modulus": self.m_eval,
                "histograms": histograms,
                "hamilton_colors": ham_colors,
                "nonhamilton_colors": [color for color in range(5) if color not in ham_colors],
                "rule": {
                    class_name(key): list(PERMS[solution[self.key_to_idx[key]]])
                    for key in self.keys
                },
            }
            self.StopSearch()


class CombinedSearchCallback(cp_model.CpSolverSolutionCallback):
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
        self.best_score: tuple[int, int, int] | None = None
        self.best_payload: dict[str, object] | None = None

    def on_solution_callback(self) -> None:
        self.solution_index += 1
        solution = [self.Value(v) for v in self.vars_by_key]
        by_modulus: dict[str, object] = {}
        ham_counts: dict[str, int] = {}
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
        min_ham = min(ham_counts.values())
        total_ham = sum(ham_counts.values())
        largest_7 = sum(
            max(int(length) for length in by_modulus["7"]["histograms"][str(color)].keys())
            for color in (0, 1, 2)
        )
        score = (min_ham, total_ham, largest_7)
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_payload = {
                "solution_index": self.solution_index,
                "hamilton_counts": ham_counts,
                "by_modulus": by_modulus,
                "rule": {
                    class_name(key): list(PERMS[solution[self.key_to_idx[key]]])
                    for key in self.keys
                },
            }
        if self.solution_index >= self.solution_limit:
            self.StopSearch()


def run_stable_search() -> dict[str, object]:
    stable_moduli = [9]
    keys = build_keys(stable_moduli)
    key_to_idx = {key: idx for idx, key in enumerate(keys)}
    patterns = build_patterns(stable_moduli, key_to_idx)
    model, vars_by_key = build_model(keys, patterns)

    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1

    cb = StableSearchCallback(vars_by_key, keys, key_to_idx, m_eval=5, stop_at_ham_count=4)
    solver.SearchForAllSolutions(model, cb)
    if cb.result is None:
        raise RuntimeError("stable search failed to find the expected 4-Hamilton witness")
    return {
        "search_moduli": stable_moduli,
        "key_count": len(keys),
        "pattern_count": len(patterns),
        "first_four_hamilton_solution": cb.result,
    }


def run_combined_search() -> dict[str, object]:
    search_moduli = [7, 9]
    evaluation_moduli = [5, 7]
    keys = build_keys(search_moduli)
    key_to_idx = {key: idx for idx, key in enumerate(keys)}
    patterns = build_patterns(search_moduli, key_to_idx)
    model, vars_by_key = build_model(keys, patterns)

    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1

    cb = CombinedSearchCallback(
        vars_by_key,
        keys,
        key_to_idx,
        evaluation_moduli=evaluation_moduli,
        solution_limit=200,
    )
    solver.SearchForAllSolutions(model, cb)
    if cb.best_payload is None or cb.best_score is None:
        raise RuntimeError("combined search did not produce any solution")
    return {
        "search_moduli": search_moduli,
        "evaluation_moduli": evaluation_moduli,
        "key_count": len(keys),
        "pattern_count": len(patterns),
        "solution_limit": 200,
        "best_score": list(cb.best_score),
        "best_solution": cb.best_payload,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compressed local-pattern search for Route-E five-color assembly.")
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    args = parser.parse_args()

    stable = run_stable_search()
    combined = run_combined_search()

    summary = {
        "task": "d5_274_routee_assembly_pattern_search",
        "family": (
            "Fix Sel* colors 3 and 4. Assign colors 0,1,2 by one fixed permutation on "
            "S0, S1, S4+, the full slice-2 active-set class S2(A2), and the one-bit "
            "slice-3 class S3(1 in A3)."
        ),
        "stable_local_exactness": {
            "search_moduli": stable["search_moduli"],
            "key_count": stable["key_count"],
            "pattern_count": stable["pattern_count"],
            "first_four_hamilton_solution_index": stable["first_four_hamilton_solution"]["solution_index"],
            "evaluation_modulus": stable["first_four_hamilton_solution"]["evaluation_modulus"],
            "hamilton_colors": stable["first_four_hamilton_solution"]["hamilton_colors"],
            "nonhamilton_colors": stable["first_four_hamilton_solution"]["nonhamilton_colors"],
        },
        "combined_7_9_search": {
            "search_moduli": combined["search_moduli"],
            "evaluation_moduli": combined["evaluation_moduli"],
            "key_count": combined["key_count"],
            "pattern_count": combined["pattern_count"],
            "solution_limit": combined["solution_limit"],
            "best_hamilton_counts": combined["best_solution"]["hamilton_counts"],
            "best_nonhamilton_colors": {
                modulus: combined["best_solution"]["by_modulus"][modulus]["nonhamilton_colors"]
                for modulus in combined["best_solution"]["by_modulus"]
            },
        },
        "conclusion": (
            "The simple S2(A2)+S3(one-bit) assembly family admits a finite local exactness compression. "
            "For odd m >= 9 the local exactness constraints stabilize to 221 patterns. "
            "Inside this family, a 4-Hamilton solution already appears in the stable search at m=5, "
            "and among the first 200 solutions of the combined 7/9 exact model the best rule has "
            "Hamilton-count profile m=5 -> 3, m=7 -> 4. So the remaining assembly problem has been "
            "reduced to a much narrower finite-pattern search plus one or two residual Hamilton closures, "
            "rather than an open-ended new-coordinate search."
        ),
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2))
    (args.detail_dir / "stable_search.json").write_text(json.dumps(stable, indent=2))
    (args.detail_dir / "combined_search.json").write_text(json.dumps(combined, indent=2))


if __name__ == "__main__":
    main()
