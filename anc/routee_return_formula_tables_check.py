#!/usr/bin/env python3
"""Checks the low-layer tables and return-map formulas for Route E.

This script is designed to complement route_e_even.py.
It does not re-check the full even theorem path on V; instead it targets the
most table-driven step in the paper:

    Route E definition  ->  low-layer words  ->  displayed return-map formulas.

For every even m in a chosen range, it checks:
  1. the Appendix-B partition sets A,B,C,D,E,F are pairwise disjoint;
  2. their union is all of P_0 \\cong (Z/mZ)^2;
  3. the layer-0 Route E direction triple on each set is the one claimed;
  4. the low-layer words for colors 0,1,2 match the tables / prose;
  5. the displacement induced by each low-layer word matches the displayed
     return-map branch formulas.

This directly addresses the proof-security concern that the tables must form a
true partition and must match the final piecewise return-map formulas exactly.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import route_e_even as ree

Pair = Tuple[int, int]

LAYER0_TRIPLES = {
    "A": "102",
    "B": "021",
    "C": "210",
    "D": "012",
    "E": "201",
    "F": "120",
}


def all_pairs(m: int) -> Set[Pair]:
    return {(i, k) for i in range(m) for k in range(m)}


def case_sets(m: int) -> Dict[str, Set[Pair]]:
    if m < 6 or m % 2 != 0:
        raise ValueError("m must be even and >= 6")

    if m % 6 in (0, 2):
        A = {(0, 0)} | {(i, (m - 1 - i) % m) for i in range(1, m - 2)} | {(m - 1, m - 1)}
        B = {(0, m - 1)} | {(i, 0) for i in range(1, m - 2)} | {(m - 1, 1)}
        C = {(0, k) for k in range(1, m - 1)} | {(1, m - 1)}
        D = {(m - 2, 1)}
        E = {(m - 2, 0)}
    else:
        A = {(0, 0)} | {(i, (m - 1 - i) % m) for i in range(2, m - 2)} | {(m - 1, m - 1)}
        B = {(0, m - 1)} | {(i, 0) for i in range(2, m - 2)} | {(m - 1, 1)}
        C = (
            {(0, k) for k in range(1, m - 1)}
            | {(1, k) for k in range(1, m - 2)}
            | {(1, m - 1), (2, m - 2), (2, m - 1)}
        )
        D = {(1, m - 2), (m - 2, 1)}
        E = {(1, 0), (m - 2, 0)}

    used = A | B | C | D | E
    F = all_pairs(m) - used
    return {"A": A, "B": B, "C": C, "D": D, "E": E, "F": F}


def verify_partition(m: int, sets: Dict[str, Set[Pair]]) -> None:
    ground = all_pairs(m)
    union = set().union(*sets.values())
    if union != ground:
        missing = sorted(ground - union)
        extra = sorted(union - ground)
        raise AssertionError(f"partition coverage failed at m={m}; missing={missing[:10]}, extra={extra[:10]}")
    for a, b in combinations("ABCDEF", 2):
        overlap = sets[a] & sets[b]
        if overlap:
            raise AssertionError(f"partition overlap at m={m}: {a} ∩ {b} = {sorted(overlap)[:10]}")



def p0_vertex(m: int, i: int, k: int) -> Tuple[int, int, int]:
    return ree.p0_point(m, i, k)



def layer0_triple(m: int, i: int, k: int) -> str:
    return "".join(str(x) for x in ree.route_e_direction_triple(m, p0_vertex(m, i, k)))



def low_layer_word(m: int, color: int, i: int, k: int) -> str:
    v = p0_vertex(m, i, k)
    out: List[str] = []
    for _ in range(3):
        d = ree.route_e_direction_triple(m, v)[color]
        out.append(str(d))
        v = ree.bump(v, d, m)
    return "".join(out)



def displacement_from_word(color: int, word: str, i: int, k: int, m: int) -> Pair:
    n0 = word.count("0")
    n2 = word.count("2")
    if color == 0:
        return ((i + n0 - 3) % m, (k + n2) % m)
    if color == 1:
        return ((i + n0) % m, (k + n2) % m)
    if color == 2:
        return ((i + n0) % m, (k + n2 - 3) % m)
    raise ValueError("color must be 0,1,2")



def expected_color1_word(set_name: str) -> str:
    if set_name in {"A", "E"}:
        return "001"
    if set_name in {"C", "D"}:
        return "101"
    return "201"



def expected_color0_word_case1(i: int, k: int, set_name: str, m: int) -> str:
    if set_name == "A":
        return "110" if (i, k) == (0, 0) else "120"
    if set_name == "B":
        return "010" if (i, k) == (m - 1, 1) else "020"
    if set_name == "C":
        if (i, k) == (0, 1):
            return "212"
        if (i, k) == (1, m - 1):
            return "222"
        return "210"
    if set_name == "D":
        return "020"
    if set_name == "E":
        return "220"
    return "122" if (i + k) % m == 1 else "120"



def expected_color2_word_case1(i: int, k: int, set_name: str, m: int) -> str:
    if set_name == "A":
        return "220" if (i, k) == (0, 0) else "212"
    if set_name == "B":
        if (i, k) == (0, m - 1):
            return "122"
        if (i, k) == (2, 0):
            return "110"
        return "112"
    if set_name == "C":
        return "010" if (i, k) == (0, 1) else "012"
    if set_name == "D":
        return "212"
    if set_name == "E":
        return "112"
    if i == m - 1:
        return "022"
    if (i + k) % m == 1:
        return "010"
    return "012"



def expected_color0_word_case2(i: int, k: int, set_name: str, m: int) -> str:
    if set_name == "A":
        return "110" if (i, k) == (0, 0) else "120"
    if set_name == "B":
        return "010" if (i, k) == (m - 1, 1) else "020"
    if set_name == "C":
        if (i, k) == (0, 1):
            return "212"
        if (i, k) in {(1, m - 1), (2, m - 2)}:
            return "222"
        if (i == 1 and 1 <= k <= m - 3) or (i, k) == (2, m - 1):
            return "220"
        if i == 0 and 2 <= k <= m - 2:
            return "210"
        raise AssertionError(f"unclassified Case II color-0 C-point at m={m}: {(i,k)}")
    if set_name == "D":
        return "020"
    if set_name == "E":
        return "220"
    return "122" if (i + k) % m == 1 else "120"



def expected_color2_word_case2(i: int, k: int, set_name: str, m: int) -> str:
    if set_name == "A":
        return "220" if (i, k) == (0, 0) else "212"
    if set_name == "B":
        if (i, k) == (0, m - 1):
            return "122"
        if (i, k) == (2, 0):
            return "110"
        return "112"
    if set_name == "C":
        if (i, k) in {(0, 1), (2, m - 1)}:
            return "010"
        return "012"
    if set_name == "D":
        return "212"
    if set_name == "E":
        return "112"
    if i == m - 1:
        return "022"
    if (i + k) % m == 1:
        return "010"
    return "012"



def expected_word(m: int, set_name: str, color: int, i: int, k: int) -> str:
    if color == 1:
        return expected_color1_word(set_name)
    if m % 6 in (0, 2):
        return expected_color0_word_case1(i, k, set_name, m) if color == 0 else expected_color2_word_case1(i, k, set_name, m)
    return expected_color0_word_case2(i, k, set_name, m) if color == 0 else expected_color2_word_case2(i, k, set_name, m)



def expected_layer0_triple(set_name: str) -> str:
    return LAYER0_TRIPLES[set_name]



def point_set_name(pt: Pair, sets: Dict[str, Set[Pair]]) -> str:
    for name, s in sets.items():
        if pt in s:
            return name
    raise KeyError(pt)



def verify_m(m: int, cross_check_definition: bool = False) -> None:
    sets = case_sets(m)
    verify_partition(m, sets)
    for i, k in sorted(all_pairs(m)):
        set_name = point_set_name((i, k), sets)
        actual_layer0 = layer0_triple(m, i, k)
        expect_layer0 = expected_layer0_triple(set_name)
        if actual_layer0 != expect_layer0:
            raise AssertionError(
                f"m={m}, point={(i,k)}, set={set_name}: layer-0 triple {actual_layer0} != expected {expect_layer0}"
            )
        for color in (0, 1, 2):
            actual_word = low_layer_word(m, color, i, k)
            expect_word = expected_word(m, set_name, color, i, k)
            if actual_word != expect_word:
                raise AssertionError(
                    f"m={m}, color={color}, point={(i,k)}, set={set_name}: word {actual_word} != expected {expect_word}"
                )
            disp_from_word = displacement_from_word(color, actual_word, i, k, m)
            disp_formula = ree.return_map_formula(m, color, i, k)
            if disp_from_word != disp_formula:
                raise AssertionError(
                    f"m={m}, color={color}, point={(i,k)}: displacement {disp_from_word} != formula {disp_formula}"
                )
            if cross_check_definition:
                disp_def = ree.return_map_from_definition(m, color, i, k)
                if disp_formula != disp_def:
                    raise AssertionError(
                        f"m={m}, color={color}, point={(i,k)}: formula {disp_formula} != definition {disp_def}"
                    )



def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Route E tables, partitions, and return-map formulas.")
    parser.add_argument("--m-min", type=int, default=6, help="smallest even m to test (default: 6)")
    parser.add_argument("--m-max", type=int, default=60, help="largest even m to test (default: 60)")
    parser.add_argument(
        "--cross-check-definition",
        action="store_true",
        help="also compare the table-induced displacements with the direct Definition-3 return maps",
    )
    args = parser.parse_args(argv)

    if args.m_min > args.m_max:
        raise SystemExit("--m-min must be <= --m-max")

    tested: List[int] = []
    for m in range(args.m_min, args.m_max + 1):
        if m % 2 == 0 and m >= 6:
            verify_m(m, cross_check_definition=args.cross_check_definition)
            tested.append(m)

    if not tested:
        raise SystemExit("no even m >= 6 in the requested range")

    print("Route E table / partition checks: PASS")
    print(f"tested even m = {tested[0]}..{tested[-1]} (step 2), count = {len(tested)}")
    if args.cross_check_definition:
        print("cross-check with the Route E definition return maps: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
