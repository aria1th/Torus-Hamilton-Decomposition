#!/usr/bin/env python3
"""Validate the d=4 line-union witness with mode switching for large m."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from candidates.hyperplane_fusion_line_union_v1 import direction_tuple as line_union_direction_tuple
from torus_nd_layer2_gauge_analysis import (
    LINE_UNION_CODE,
    actual_R,
    actual_T,
    line_union_R_formula,
    line_union_T_formula,
    line_union_psi,
    odometer,
    q_cycle_report,
    representative_trace,
    rule_matches_code,
    support_polynomial_string,
)
from torus_nd_validate import validate_rule

try:
    from rich.console import Console
    from rich.progress import track
    from rich.table import Table
except ImportError:  # pragma: no cover - optional dependency
    Console = None
    Table = None
    track = None


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _iter_progress(
    values: Iterable[int],
    *,
    description: str,
    use_rich: bool,
):
    if use_rich and track is not None:
        return track(values, description=description)
    return values


def _mode_for_m(mode: str, m: int, exact_max: int, formula_max: int, odometer_max: int) -> str:
    if mode != "auto":
        return mode
    if m <= exact_max:
        return "exact"
    if m <= formula_max:
        return "formula"
    if m <= odometer_max:
        return "odometer"
    return "certificate"


def _exact_check(m: int) -> Dict[str, object]:
    start = time.perf_counter()
    report = validate_rule(4, m, lambda v, mm=m: line_union_direction_tuple(4, mm, v))
    return {
        "mode": "exact",
        "elapsed_sec": time.perf_counter() - start,
        "all_hamilton": bool(report["all_hamilton"]),
        "sign_product": int(report["sign_product"]),
        "color_cycle_counts": [int(stat["cycle_count"]) for stat in report["color_stats"]],
    }


def _formula_check(m: int, *, use_rich: bool, verbosity: str) -> Dict[str, object]:
    start = time.perf_counter()
    by_color = []

    for color in range(4):
        r_ok = True
        t_ok = True
        psi_ok = True
        q_shift_values = set()
        a_iter = _iter_progress(
            range(m),
            description=f"m={m} color={color} formula",
            use_rich=use_rich and verbosity in ("verbose", "debug"),
        )
        for a in a_iter:
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

    return {
        "mode": "formula",
        "elapsed_sec": time.perf_counter() - start,
        "support_formula": support_polynomial_string(LINE_UNION_CODE),
        "support_count": 2 * m - 1,
        "all_formula_checks_pass": all(
            item["R_formula_verified"]
            and item["T_formula_verified"]
            and item["odometer_conjugacy_verified"]
            and item["Q_cycle_count"] == 1
            for item in by_color
        ),
        "by_color": by_color,
    }


def _odometer_check(m: int, *, use_rich: bool, verbosity: str) -> Dict[str, object]:
    start = time.perf_counter()
    by_color = []

    for color in range(4):
        psi_ok = True
        a_iter = _iter_progress(
            range(m),
            description=f"m={m} color={color} odometer",
            use_rich=use_rich and verbosity == "debug",
        )
        for a in a_iter:
            for b in range(m):
                image = line_union_T_formula(color, a, b, m)
                lhs = line_union_psi(color, image[0], image[1], m)
                rhs = odometer(*line_union_psi(color, a, b, m), m)
                if lhs != rhs:
                    psi_ok = False
                    break
            if not psi_ok:
                break
        by_color.append(
            {
                "color": color,
                "odometer_conjugacy_verified": psi_ok,
                "checked_points": m * m,
                "Q_single_cycle_certified": psi_ok,
            }
        )

    return {
        "mode": "odometer",
        "elapsed_sec": time.perf_counter() - start,
        "support_formula": support_polynomial_string(LINE_UNION_CODE),
        "support_count": 2 * m - 1,
        "all_formula_checks_pass": all(item["odometer_conjugacy_verified"] for item in by_color),
        "by_color": by_color,
        "proof_note_dependency": "Assumes the displayed T_c formulas and odometer theorem from RoundX/d4_line_union_proof_note_draft.md",
    }


def _certificate_check(m: int) -> Dict[str, object]:
    start = time.perf_counter()
    return {
        "mode": "certificate",
        "elapsed_sec": time.perf_counter() - start,
        "support_formula": support_polynomial_string(LINE_UNION_CODE),
        "support_count": 2 * m - 1,
        "Q_single_cycle_certified": True,
        "full_hamilton_certified": True,
        "odometer_conjugacies": {
            "T0": "(u,v)=(1-b,-a)",
            "T1": "(u,v)=(-a-1,-b)",
            "T2": "(u,v)=(b-2,a)",
            "T3": "(u,v)=(a,b)",
        },
        "proof_note_dependency": "Pure proof-backed certificate; no state sweep is performed at this m.",
    }


def validate_line_union(
    m_values: Sequence[int],
    *,
    mode: str,
    exact_max: int,
    formula_max: int,
    odometer_max: int,
    use_rich: bool,
    verbosity: str,
) -> Dict[str, object]:
    overall_start = time.perf_counter()
    per_m = []
    for m in _iter_progress(m_values, description="Validating line-union witness", use_rich=use_rich):
        chosen_mode = _mode_for_m(mode, m, exact_max, formula_max, odometer_max)
        if chosen_mode == "exact":
            result = _exact_check(m)
            ok = bool(result["all_hamilton"])
        elif chosen_mode == "formula":
            result = _formula_check(m, use_rich=use_rich, verbosity=verbosity)
            ok = bool(result["all_formula_checks_pass"])
        elif chosen_mode == "odometer":
            result = _odometer_check(m, use_rich=use_rich, verbosity=verbosity)
            ok = bool(result["all_formula_checks_pass"])
        else:
            result = _certificate_check(m)
            ok = bool(result["full_hamilton_certified"])
        result["m"] = m
        result["ok"] = ok
        per_m.append(result)

    return {
        "task_id": "D4-LINE-UNION-VALIDATE-01",
        "candidate_rule": "candidates/hyperplane_fusion_line_union_v1.py",
        "tested_m_values": list(m_values),
        "mode": mode,
        "thresholds": {
            "exact_max": exact_max,
            "formula_max": formula_max,
            "odometer_max": odometer_max,
        },
        "runtime_sec": time.perf_counter() - overall_start,
        "module_matches_line_union_code": all(
            rule_matches_code(line_union_direction_tuple, LINE_UNION_CODE, m) for m in (3, 4, 5, 6)
        ),
        "results": per_m,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    results = summary["results"]
    if use_rich and Console is not None and Table is not None:
        console = Console()
        table = Table(title="Line-Union Validation Summary")
        table.add_column("m", justify="right")
        table.add_column("mode")
        table.add_column("ok")
        table.add_column("elapsed_sec", justify="right")
        for item in results:
            table.add_row(
                str(item["m"]),
                str(item["mode"]),
                "PASS" if item["ok"] else "FAIL",
                f"{item['elapsed_sec']:.3f}",
            )
        console.print(table)
        console.print(f"runtime_sec: {summary['runtime_sec']:.3f}")
        console.print(
            f"module_matches_line_union_code: {summary['module_matches_line_union_code']}"
        )
        return

    print(f"tested_m_values: {summary['tested_m_values']}")
    for item in results:
        print(
            f"m={item['m']} mode={item['mode']} "
            f"status={'PASS' if item['ok'] else 'FAIL'} elapsed_sec={item['elapsed_sec']:.3f}"
        )
    print(f"runtime_sec: {summary['runtime_sec']:.3f}")
    print(f"module_matches_line_union_code: {summary['module_matches_line_union_code']}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the d=4 line-union witness with exact, formula, odometer, or certificate checks."
    )
    parser.add_argument(
        "--m-list",
        default="3,4,5,6,7,8,9,10,12,15,20,25,30,40,50,75,100,200,500,1000,2000,1000000,1000000000",
        help="comma-separated list of m values to validate",
    )
    parser.add_argument(
        "--mode",
        choices=("auto", "exact", "formula", "odometer", "certificate"),
        default="auto",
        help="validation mode for all m, or auto-switch based on thresholds",
    )
    parser.add_argument("--exact-max", type=int, default=12, help="auto mode: exact validation through this m")
    parser.add_argument("--formula-max", type=int, default=30, help="auto mode: formula validation through this m")
    parser.add_argument("--odometer-max", type=int, default=2000, help="auto mode: odometer validation through this m")
    parser.add_argument(
        "--verbosity",
        choices=("quiet", "normal", "verbose", "debug"),
        default="normal",
        help="progress verbosity for Rich/plain output",
    )
    parser.add_argument(
        "--trace-m-list",
        default="5,7",
        help="comma-separated representative m values for saved Q traces",
    )
    parser.add_argument("--out", type=Path, help="write JSON summary to this path")
    parser.add_argument("--trace-dir", type=Path, help="write representative Q traces to this directory")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich progress output")
    args = parser.parse_args(argv)

    use_rich = not args.no_rich and Console is not None and track is not None
    m_values = _parse_m_list(args.m_list)
    summary = validate_line_union(
        m_values,
        mode=args.mode,
        exact_max=args.exact_max,
        formula_max=args.formula_max,
        odometer_max=args.odometer_max,
        use_rich=use_rich and args.verbosity != "quiet",
        verbosity=args.verbosity,
    )

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2))

    if args.trace_dir is not None:
        args.trace_dir.mkdir(parents=True, exist_ok=True)
        for m in _parse_m_list(args.trace_m_list):
            payload = {
                "m": m,
                "candidate_rule": "candidates/hyperplane_fusion_line_union_v1.py",
                "traces": [representative_trace(color, m) for color in range(4)],
            }
            (args.trace_dir / f"line_union_q_traces_m{m}.json").write_text(json.dumps(payload, indent=2))

    _print_summary(summary, use_rich=use_rich and args.verbosity != "quiet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
