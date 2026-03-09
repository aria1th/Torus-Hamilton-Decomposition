#!/usr/bin/env python3
"""Verify repaired first-return and second-return formulas for the 4D witness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from candidates.hyperplane_fusion_low_layers_v1 import direction_tuple

Coords = Tuple[int, int, int, int]
SectionPoint = Tuple[int, int, int]
QPoint = Tuple[int, int]


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def phi(a: int, b: int, q: int, m: int) -> Coords:
    return (a % m, b % m, (q - a) % m, (-q - b) % m)


def inv_phi(x: Coords, m: int) -> SectionPoint:
    x0, x1, x2, _ = x
    return (x0 % m, x1 % m, (x0 + x2) % m)


def step_vertex(x: Coords, color: int, m: int) -> Coords:
    direction = direction_tuple(4, m, x)[color]
    out = list(x)
    out[direction] = (out[direction] + 1) % m
    return tuple(out)  # type: ignore[return-value]


def actual_R(color: int, a: int, b: int, q: int, m: int) -> SectionPoint:
    x = phi(a, b, q, m)
    for _ in range(m):
        x = step_vertex(x, color, m)
    return inv_phi(x, m)


def formula_R(color: int, a: int, b: int, q: int, m: int) -> SectionPoint:
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
        if q == (m - 1) % m and a != (m - 1) % m:
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
        if q == (m - 1) % m and a != 0:
            return (a, (b + 1) % m, (q + 1) % m)
        return (a, b, (q + 1) % m)
    raise ValueError(f"Unknown color {color}")


def actual_T(color: int, a: int, b: int, m: int) -> QPoint:
    cur = (a % m, b % m, (m - 1) % m)
    for _ in range(m):
        cur = actual_R(color, *cur, m)
    return cur[0], cur[1]


def formula_T(color: int, a: int, b: int, m: int) -> QPoint:
    a %= m
    b %= m
    if color == 0:
        return ((a - (1 if b == 1 % m else 0)) % m, (b - 1) % m)
    if color == 1:
        return ((a - 1) % m, (b - 1 + (1 if a == (m - 1) % m else 0)) % m)
    if color == 2:
        return ((a + (1 if b == 2 % m else 0)) % m, (b + 1) % m)
    if color == 3:
        return ((a + 1) % m, (b + 1 - (1 if a == 0 else 0)) % m)
    raise ValueError(f"Unknown color {color}")


def psi(color: int, a: int, b: int, m: int) -> QPoint:
    a %= m
    b %= m
    if color == 0:
        return ((1 - b) % m, (-a) % m)
    if color == 1:
        return ((-a - 1) % m, (b - a) % m)
    if color == 2:
        return ((b - 2) % m, a)
    if color == 3:
        return (a, (a - b) % m)
    raise ValueError(f"Unknown color {color}")


def odometer(u: int, v: int, m: int) -> QPoint:
    u %= m
    v %= m
    return ((u + 1) % m, (v + (1 if u == 0 else 0)) % m)


def invert_psi(color: int, u: int, v: int, m: int) -> QPoint:
    u %= m
    v %= m
    if color == 0:
        return ((-v) % m, (1 - u) % m)
    if color == 1:
        a = (-u - 1) % m
        return (a, (v + a) % m)
    if color == 2:
        return (v, (u + 2) % m)
    if color == 3:
        a = u
        return (a, (a - v) % m)
    raise ValueError(f"Unknown color {color}")


def cycle_decomposition(perm: Sequence[int]) -> List[List[int]]:
    seen = bytearray(len(perm))
    cycles: List[List[int]] = []
    for start in range(len(perm)):
        if seen[start]:
            continue
        cur = start
        cycle: List[int] = []
        while not seen[cur]:
            seen[cur] = 1
            cycle.append(cur)
            cur = perm[cur]
        cycles.append(cycle)
    return cycles


def q_cycle_report(color: int, m: int) -> Dict[str, object]:
    points = [(a, b) for a in range(m) for b in range(m)]
    pos = {pt: idx for idx, pt in enumerate(points)}
    perm = [pos[formula_T(color, a, b, m)] for a, b in points]
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
        u, v = psi(color, cur[0], cur[1], m)
        orbit.append({"ab": [cur[0], cur[1]], "uv": [u, v]})
        cur = formula_T(color, cur[0], cur[1], m)
    return {
        "color": color,
        "m": m,
        "orbit_length": len(orbit),
        "orbit": orbit,
    }


def verify_m(m: int) -> Dict[str, object]:
    by_color = []
    for color in range(4):
        r_ok = True
        t_ok = True
        psi_ok = True
        q_shift_values = set()

        for a in range(m):
            for b in range(m):
                for q in range(m):
                    actual = actual_R(color, a, b, q, m)
                    formula = formula_R(color, a, b, q, m)
                    if actual != formula:
                        r_ok = False
                    q_shift_values.add((formula[2] - q) % m)
                actual_q = actual_T(color, a, b, m)
                formula_q = formula_T(color, a, b, m)
                if actual_q != formula_q:
                    t_ok = False
                lhs = psi(color, formula_q[0], formula_q[1], m)
                rhs = odometer(*psi(color, a, b, m), m)
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

    return {"m": m, "by_color": by_color}


def build_summary(m_values: Sequence[int]) -> Dict[str, object]:
    per_m = [verify_m(m) for m in m_values]
    return {
        "task_id": "D4-SECOND-RETURN-ODOMETER-02",
        "candidate_rule": "candidates/hyperplane_fusion_low_layers_v1.py",
        "tested_m_values": list(m_values),
        "first_return_formulas": {
            "R0": "q=0 -> (a-1,b,q-1); q=m-1,b=1 -> (a-2,b+1,q-1); otherwise -> (a-1,b+1,q-1)",
            "R1": "q=0 -> (a,b-1,q+1); q=m-1,a!=m-1 -> (a+1,b-2,q+1); otherwise -> (a+1,b-1,q+1)",
            "R2": "q=0 -> (a,b+1,q-1); q=m-1,b=2 -> (a+1,b,q-1); otherwise -> (a,b,q-1)",
            "R3": "q=0 -> (a+1,b,q+1); q=m-1,a!=0 -> (a,b+1,q+1); otherwise -> (a,b,q+1)",
        },
        "second_return_formulas": {
            "T0": "(a,b) -> (a-1_{b=1}, b-1)",
            "T1": "(a,b) -> (a-1, b-1+1_{a=m-1})",
            "T2": "(a,b) -> (a+1_{b=2}, b+1)",
            "T3": "(a,b) -> (a+1, b+1-1_{a=0})",
        },
        "odometer_conjugacies": {
            "T0": "(u,v)=(1-b,-a)",
            "T1": "(u,v)=(-a-1,b-a)",
            "T2": "(u,v)=(b-2,a)",
            "T3": "(u,v)=(a,a-b)",
        },
        "standard_odometer": "(u,v) -> (u+1, v+1_{u=0})",
        "verification": per_m,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify second-return odometer formulas for the 4D witness.")
    parser.add_argument(
        "--m-list",
        default="3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20",
        help="comma-separated list of m values to verify",
    )
    parser.add_argument(
        "--trace-m-list",
        default="5,7",
        help="comma-separated list of representative m values for saved Q-orbit traces",
    )
    parser.add_argument("--out", type=Path, help="write JSON summary to this path")
    parser.add_argument("--trace-dir", type=Path, help="directory for representative trace JSON files")
    args = parser.parse_args()

    m_values = _parse_m_list(args.m_list)
    if not m_values:
        raise SystemExit("Need at least one m value.")
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
                "candidate_rule": "candidates/hyperplane_fusion_low_layers_v1.py",
                "traces": [representative_trace(color, m) for color in range(4)],
            }
            (args.trace_dir / f"q_traces_m{m}.json").write_text(json.dumps(payload, indent=2))

    compact = {
        "tested_m_values": m_values,
        "all_R_verified": all(
            row["R_formula_verified"]
            for report in summary["verification"]
            for row in report["by_color"]
        ),
        "all_T_verified": all(
            row["T_formula_verified"]
            for report in summary["verification"]
            for row in report["by_color"]
        ),
        "all_conjugacies_verified": all(
            row["odometer_conjugacy_verified"]
            for report in summary["verification"]
            for row in report["by_color"]
        ),
    }
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
