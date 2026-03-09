#!/usr/bin/env python3
"""Classify the reduced layer-2 gate family behind the 4D low-layer witness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Dict, List, Sequence, Tuple

from candidates.hyperplane_fusion_line_union_v1 import direction_tuple as line_union_direction_tuple
from candidates.hyperplane_fusion_low_layers_v1 import direction_tuple as current_direction_tuple
from torus_nd_validate import cycle_decomposition, index_to_coords, validate_rule

Coords = Tuple[int, int, int, int]
SectionPoint = Tuple[int, int, int]
QPoint = Tuple[int, int]
Code = Tuple[int, int, int, int]

PATTERN_ORDER: Tuple[Tuple[int, int], ...] = ((0, 0), (1, 0), (0, 1), (1, 1))
PATTERN_LABELS = {
    (0, 0): "u=0,v=0",
    (1, 0): "u=1,v=0",
    (0, 1): "u=0,v=1",
    (1, 1): "u=1,v=1",
}
STATE_NAMES = {
    0: "none",
    1: "odd_swap",
    2: "even_swap",
    3: "both_swaps",
}
GAUGE_NAMES = {
    0: "identity",
    1: "odd_swap",
    2: "even_swap",
    3: "both_swaps",
}
CURRENT_CODE: Code = (0, 1, 2, 3)
LINE_UNION_CODE: Code = (1, 0, 3, 2)


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _apply_swaps(state: int) -> Tuple[int, int, int, int]:
    out = [0, 1, 2, 3]
    if state & 1:
        out[1], out[3] = out[3], out[1]
    if state & 2:
        out[0], out[2] = out[2], out[0]
    return tuple(out)


def make_gate_rule(code: Code, m: int) -> Callable[[Coords], Tuple[int, int, int, int]]:
    table = {pattern: code[idx] for idx, pattern in enumerate(PATTERN_ORDER)}

    def rule(v: Coords) -> Tuple[int, int, int, int]:
        x0, x1, x2, x3 = v
        layer = (x0 + x1 + x2 + x3) % m
        q = (x0 + x2) % m
        if layer == 0:
            return (3, 2, 1, 0) if q == 0 else (1, 0, 3, 2)
        if layer == 1:
            return (0, 1, 2, 3)
        if layer == 2 and q == 0:
            state = table[(int(x0 != 0), int(x3 == 0))]
            return _apply_swaps(state)
        return (0, 1, 2, 3)

    return rule


def code_to_dict(code: Code) -> Dict[str, str]:
    return {
        PATTERN_LABELS[pattern]: STATE_NAMES[code[idx]]
        for idx, pattern in enumerate(PATTERN_ORDER)
    }


def xor_code(code: Code, gauge: int) -> Code:
    return tuple(state ^ gauge for state in code)


def support_polynomial_coeffs(code: Code) -> Tuple[int, int, int]:
    s00 = int(code[0] != 0)
    s10 = int(code[1] != 0)
    s01 = int(code[2] != 0)
    s11 = int(code[3] != 0)
    a2 = s10
    a1 = s00 - 2 * s10 + s11
    a0 = -s00 + s10 + s01 - s11
    return a2, a1, a0


def _format_coeff(coeff: int, monomial: str) -> str:
    if coeff == 0:
        return ""
    if coeff == 1:
        return monomial
    if coeff == -1:
        return f"-{monomial}"
    return f"{coeff}{monomial}"


def support_polynomial_string(code: Code) -> str:
    a2, a1, a0 = support_polynomial_coeffs(code)
    parts: List[str] = []
    for coeff, monomial in ((a2, "m^2"), (a1, "m")):
        term = _format_coeff(coeff, monomial)
        if term:
            parts.append(term)
    if a0 != 0 or not parts:
        parts.append(str(a0))

    out = parts[0]
    for term in parts[1:]:
        if term.startswith("-"):
            out += f" - {term[1:]}"
        else:
            out += f" + {term}"
    return out


def layer2_support_count(code: Code, m: int) -> int:
    a2, a1, a0 = support_polynomial_coeffs(code)
    return a2 * m * m + a1 * m + a0


def code_name(code: Code) -> str:
    if code == CURRENT_CODE:
        return "current_witness"
    if code == LINE_UNION_CODE:
        return "line_union_gauge"
    if code == xor_code(CURRENT_CODE, 2):
        return "even_global_gauge"
    if code == xor_code(CURRENT_CODE, 3):
        return "both_global_gauge"
    return "unnamed"


def rule_matches_code(module_rule: Callable[[int, int, Tuple[int, ...]], Tuple[int, ...]], code: Code, m: int) -> bool:
    generic_rule = make_gate_rule(code, m)
    for index in range(m ** 4):
        coords = index_to_coords(index, 4, m)
        if tuple(module_rule(4, m, coords)) != tuple(generic_rule(coords)):
            return False
    return True


def classify_family(m_values: Sequence[int]) -> Dict[str, object]:
    family_results = []
    survivors: List[Code] = []

    for raw in range(256):
        code = tuple((raw >> (2 * idx)) & 3 for idx in range(4))
        first_fail_m = None
        for m in m_values:
            report = validate_rule(4, m, make_gate_rule(code, m))
            if not bool(report["all_hamilton"]):
                first_fail_m = m
                break
        if first_fail_m is None:
            survivors.append(code)
        family_results.append(
            {
                "code": list(code),
                "code_name": code_name(code),
                "truth_table": code_to_dict(code),
                "is_hamilton_on_range": first_fail_m is None,
                "first_fail_m": first_fail_m,
                "layer2_support_formula": support_polynomial_string(code),
            }
        )

    orbit = sorted({xor_code(CURRENT_CODE, gauge) for gauge in range(4)})
    detailed_survivors = []
    for code in sorted(survivors):
        per_m = []
        for m in m_values:
            report = validate_rule(4, m, make_gate_rule(code, m))
            per_m.append(
                {
                    "m": m,
                    "all_hamilton": bool(report["all_hamilton"]),
                    "sign_product": int(report["sign_product"]),
                    "color_cycle_counts": [int(stat["cycle_count"]) for stat in report["color_stats"]],
                    "layer2_support_count": layer2_support_count(code, m),
                }
            )
        detailed_survivors.append(
            {
                "code": list(code),
                "code_name": code_name(code),
                "truth_table": code_to_dict(code),
                "layer2_support_formula": support_polynomial_string(code),
                "per_m": per_m,
            }
        )

    return {
        "tested_m_values": list(m_values),
        "family_size": 256,
        "survivor_count": len(survivors),
        "survivor_codes": [list(code) for code in sorted(survivors)],
        "survivor_truth_tables": [code_to_dict(code) for code in sorted(survivors)],
        "survivor_orbits_under_klein_four": [
            {
                "orbit_name": "current_witness_orbit",
                "members": [list(code) for code in orbit],
                "member_names": [code_name(code) for code in orbit],
            }
        ],
        "current_module_matches_reduced_code": all(
            rule_matches_code(current_direction_tuple, CURRENT_CODE, m) for m in (3, 4, 5, 6)
        ),
        "line_union_module_matches_reduced_code": all(
            rule_matches_code(line_union_direction_tuple, LINE_UNION_CODE, m) for m in (3, 4, 5, 6)
        ),
        "family_results": family_results,
        "survivor_details": detailed_survivors,
    }


def phi(a: int, b: int, q: int, m: int) -> Coords:
    return (a % m, b % m, (q - a) % m, (-q - b) % m)


def inv_phi(x: Coords, m: int) -> SectionPoint:
    x0, x1, x2, _ = x
    return (x0 % m, x1 % m, (x0 + x2) % m)


def step_vertex(rule: Callable[[int, int, Tuple[int, ...]], Tuple[int, ...]], color: int, x: Coords, m: int) -> Coords:
    direction = int(rule(4, m, x)[color])
    out = list(x)
    out[direction] = (out[direction] + 1) % m
    return tuple(out)  # type: ignore[return-value]


def actual_R(
    rule: Callable[[int, int, Tuple[int, ...]], Tuple[int, ...]],
    color: int,
    a: int,
    b: int,
    q: int,
    m: int,
) -> SectionPoint:
    x = phi(a, b, q, m)
    for _ in range(m):
        x = step_vertex(rule, color, x, m)
    return inv_phi(x, m)


def actual_T(
    rule: Callable[[int, int, Tuple[int, ...]], Tuple[int, ...]],
    color: int,
    a: int,
    b: int,
    m: int,
) -> QPoint:
    cur = (a % m, b % m, (m - 1) % m)
    for _ in range(m):
        cur = actual_R(rule, color, *cur, m)
    return cur[0], cur[1]


def line_union_R_formula(color: int, a: int, b: int, q: int, m: int) -> SectionPoint:
    a %= m
    b %= m
    q %= m
    if color == 0:
        if q == 0:
            return ((a - 1) % m, b, (q - 1) % m)
        if q == (m - 1) % m and b == 1 % m:
            return ((a - 2) % m, (b + 1) % m, (q - 1) % m)
        return ((a - 1) % m, (b + 1) % m, (q - 1) % m)
    if color == 1:
        if q == 0:
            return (a, (b - 1) % m, (q + 1) % m)
        if q == (m - 1) % m and a == (m - 1) % m:
            return ((a + 1) % m, (b - 2) % m, (q + 1) % m)
        return ((a + 1) % m, (b - 1) % m, (q + 1) % m)
    if color == 2:
        if q == 0:
            return (a, (b + 1) % m, (q - 1) % m)
        if q == (m - 1) % m and b == 2 % m:
            return ((a + 1) % m, b, (q - 1) % m)
        return (a, b, (q - 1) % m)
    if color == 3:
        if q == 0:
            return ((a + 1) % m, b, (q + 1) % m)
        if q == (m - 1) % m and a == 0:
            return (a, (b + 1) % m, (q + 1) % m)
        return (a, b, (q + 1) % m)
    raise ValueError(f"Unknown color {color}")


def line_union_T_formula(color: int, a: int, b: int, m: int) -> QPoint:
    a %= m
    b %= m
    if color == 0:
        return ((a - (1 if b == 1 % m else 0)) % m, (b - 1) % m)
    if color == 1:
        return ((a - 1) % m, (b - (1 if a == (m - 1) % m else 0)) % m)
    if color == 2:
        return ((a + (1 if b == 2 % m else 0)) % m, (b + 1) % m)
    if color == 3:
        return ((a + 1) % m, (b + (1 if a == 0 else 0)) % m)
    raise ValueError(f"Unknown color {color}")


def line_union_psi(color: int, a: int, b: int, m: int) -> QPoint:
    a %= m
    b %= m
    if color == 0:
        return ((1 - b) % m, (-a) % m)
    if color == 1:
        return ((-a - 1) % m, (-b) % m)
    if color == 2:
        return ((b - 2) % m, a)
    if color == 3:
        return (a, b)
    raise ValueError(f"Unknown color {color}")


def odometer(u: int, v: int, m: int) -> QPoint:
    u %= m
    v %= m
    return ((u + 1) % m, (v + (1 if u == 0 else 0)) % m)


def q_cycle_report(color: int, m: int) -> Dict[str, object]:
    points = [(a, b) for a in range(m) for b in range(m)]
    pos = {point: idx for idx, point in enumerate(points)}
    perm = [pos[line_union_T_formula(color, a, b, m)] for a, b in points]
    cycles = cycle_decomposition(perm)
    return {
        "color": color,
        "cycle_count": len(cycles),
        "cycle_lengths": sorted(len(cycle) for cycle in cycles),
    }


def representative_trace(color: int, m: int) -> Dict[str, object]:
    visited = set()
    orbit = []
    cur = (0, 0)
    while cur not in visited:
        visited.add(cur)
        u, v = line_union_psi(color, cur[0], cur[1], m)
        orbit.append({"ab": [cur[0], cur[1]], "uv": [u, v]})
        cur = line_union_T_formula(color, cur[0], cur[1], m)
    return {"color": color, "m": m, "orbit_length": len(orbit), "orbit": orbit}


def verify_line_union(m_values: Sequence[int]) -> Dict[str, object]:
    verification = []
    for m in m_values:
        by_color = []
        for color in range(4):
            r_ok = True
            t_ok = True
            psi_ok = True
            q_shift_values = set()

            for a in range(m):
                for b in range(m):
                    for q in range(m):
                        actual = actual_R(line_union_direction_tuple, color, a, b, q, m)
                        formula = line_union_R_formula(color, a, b, q, m)
                        if actual != formula:
                            r_ok = False
                        q_shift_values.add((formula[2] - q) % m)
                    actual_q = actual_T(line_union_direction_tuple, color, a, b, m)
                    formula_q = line_union_T_formula(color, a, b, m)
                    if actual_q != formula_q:
                        t_ok = False
                    lhs = line_union_psi(color, formula_q[0], formula_q[1], m)
                    rhs = odometer(*line_union_psi(color, a, b, m), m)
                    if lhs != rhs:
                        psi_ok = False

            q_report = q_cycle_report(color, m)
            by_color.append(
                {
                    "color": color,
                    "R_formula_verified": r_ok,
                    "T_formula_verified": t_ok,
                    "odometer_conjugacy_verified": psi_ok,
                    "q_shift_values": sorted(q_shift_values),
                    "Q_cycle_count": q_report["cycle_count"],
                    "Q_cycle_lengths": q_report["cycle_lengths"],
                }
            )
        verification.append({"m": m, "by_color": by_color})

    return {
        "candidate_rule": "candidates/hyperplane_fusion_line_union_v1.py",
        "tested_m_values": list(m_values),
        "first_return_formulas": {
            "R0": "q=0 -> (a-1,b,q-1); q=m-1,b=1 -> (a-2,b+1,q-1); otherwise -> (a-1,b+1,q-1)",
            "R1": "q=0 -> (a,b-1,q+1); q=m-1,a=m-1 -> (a+1,b-2,q+1); otherwise -> (a+1,b-1,q+1)",
            "R2": "q=0 -> (a,b+1,q-1); q=m-1,b=2 -> (a+1,b,q-1); otherwise -> (a,b,q-1)",
            "R3": "q=0 -> (a+1,b,q+1); q=m-1,a=0 -> (a,b+1,q+1); otherwise -> (a,b,q+1)",
        },
        "second_return_formulas": {
            "T0": "(a,b) -> (a-1_{b=1}, b-1)",
            "T1": "(a,b) -> (a-1, b-1_{a=m-1})",
            "T2": "(a,b) -> (a+1_{b=2}, b+1)",
            "T3": "(a,b) -> (a+1, b+1_{a=0})",
        },
        "odometer_conjugacies": {
            "T0": "(u,v)=(1-b,-a)",
            "T1": "(u,v)=(-a-1,-b)",
            "T2": "(u,v)=(b-2,a)",
            "T3": "(u,v)=(a,b)",
        },
        "standard_odometer": "(u,v) -> (u+1, v+1_{u=0})",
        "verification": verification,
    }


def build_summary(m_values: Sequence[int]) -> Dict[str, object]:
    return {
        "task_id": "D4-LAYER2-GAUGE-CLASSIFICATION-01",
        "current_witness_code": list(CURRENT_CODE),
        "line_union_code": list(LINE_UNION_CODE),
        "pattern_bits": {
            "u": "1_{x0!=0}",
            "v": "1_{x3=0}",
        },
        "reduced_family": classify_family(m_values),
        "line_union_second_return_analysis": verify_line_union(m_values),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Classify the reduced layer-2 gate family and verify the line-union gauge."
    )
    parser.add_argument(
        "--m-list",
        default="3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20",
        help="comma-separated list of m values to test",
    )
    parser.add_argument(
        "--trace-m-list",
        default="5,7",
        help="comma-separated list of representative m values for line-union Q traces",
    )
    parser.add_argument("--out", type=Path, help="write JSON summary to this path")
    parser.add_argument("--trace-dir", type=Path, help="write line-union Q traces to this directory")
    args = parser.parse_args(argv)

    m_values = _parse_m_list(args.m_list)
    trace_m_values = _parse_m_list(args.trace_m_list)
    summary = build_summary(m_values)

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2))

    if args.trace_dir is not None:
        args.trace_dir.mkdir(parents=True, exist_ok=True)
        for m in trace_m_values:
            payload = {
                "m": m,
                "candidate_rule": "candidates/hyperplane_fusion_line_union_v1.py",
                "traces": [representative_trace(color, m) for color in range(4)],
            }
            (args.trace_dir / f"line_union_q_traces_m{m}.json").write_text(json.dumps(payload, indent=2))

    print(f"tested m values: {m_values}")
    family = summary["reduced_family"]
    print(f"reduced family survivors: {family['survivor_count']} / {family['family_size']}")
    print(f"survivor codes: {family['survivor_codes']}")
    print(f"current module matches reduced code: {family['current_module_matches_reduced_code']}")
    print(f"line-union module matches reduced code: {family['line_union_module_matches_reduced_code']}")

    line_union = summary["line_union_second_return_analysis"]
    for item in line_union["verification"]:
        all_ok = all(
            color_report["R_formula_verified"]
            and color_report["T_formula_verified"]
            and color_report["odometer_conjugacy_verified"]
            and color_report["Q_cycle_count"] == 1
            for color_report in item["by_color"]
        )
        status = "PASS" if all_ok else "FAIL"
        print(f"line-union m={item['m']}: {status}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
