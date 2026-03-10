#!/usr/bin/env python3
"""Validate d=5 odd cyclic-bulk candidates and summarize return-map structure."""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from torus_nd_d5_odd_cyclic_bulk_family import DIM, build_rule, charge, config_name, validate_config_shape
from torus_nd_validate import cycle_decomposition, induced_p0_maps, validate_rule

try:
    from rich.console import Console
    from rich.progress import track
    from rich.table import Table
except ImportError:  # pragma: no cover - optional dependency
    Console = None
    Table = None
    track = None

SectionPoint = Tuple[int, int, int, int]
QPoint = Tuple[int, int, int]


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _iter_progress(values: Iterable[int], *, description: str, use_rich: bool):
    if use_rich and track is not None:
        return track(values, description=description)
    return values


def phi(a: int, b: int, c: int, q: int, m: int) -> Tuple[int, ...]:
    inv4 = pow(4, -1, m)
    x4 = (inv4 * (q - a - 2 * b - 3 * c)) % m
    x0 = (-a - b - c - x4) % m
    return (x0, a % m, b % m, c % m, x4)


def inv_phi(x: Sequence[int], m: int) -> SectionPoint:
    return (x[1] % m, x[2] % m, x[3] % m, charge(x, m))


def step_vertex(rule, color: int, x: Sequence[int], m: int) -> Tuple[int, ...]:
    direction = int(rule(tuple(x))[color])
    out = list(x)
    out[direction] = (out[direction] + 1) % m
    return tuple(out)


def actual_R(rule, color: int, a: int, b: int, c: int, q: int, m: int) -> SectionPoint:
    x = phi(a, b, c, q, m)
    for _ in range(m):
        x = step_vertex(rule, color, x, m)
    return inv_phi(x, m)


def actual_T(rule, color: int, a: int, b: int, c: int, q_residue: int, m: int) -> Tuple[QPoint, int]:
    cur = (a % m, b % m, c % m, q_residue % m)
    for steps in range(1, m * m + 1):
        cur = actual_R(rule, color, *cur, m)
        if cur[3] == q_residue % m:
            return (cur[0], cur[1], cur[2]), steps
    raise RuntimeError(f"Second return to q={q_residue} did not occur within m^2 steps for color {color}")


def max_cycle_lengths(nexts: Sequence[Sequence[int]]) -> List[int]:
    out = []
    for perm in nexts:
        cycles = cycle_decomposition(perm)
        out.append(max(len(cycle) for cycle in cycles))
    return out


def q_section_report(rule, color: int, m: int, q_residue: int = 0) -> Dict[str, object]:
    q_shift_values = set()
    for a in range(m):
        for b in range(m):
            for c in range(m):
                for q in range(m):
                    image = actual_R(rule, color, a, b, c, q, m)
                    q_shift_values.add((image[3] - q) % m)

    uniform_q_shift = len(q_shift_values) == 1
    q_shift = next(iter(q_shift_values)) if uniform_q_shift else None

    section_points = [(a, b, c) for a in range(m) for b in range(m) for c in range(m)]
    pos = {point: idx for idx, point in enumerate(section_points)}
    perm = []
    return_lengths = []
    for a, b, c in section_points:
        image, steps = actual_T(rule, color, a, b, c, q_residue, m)
        perm.append(pos[image])
        return_lengths.append(steps)
    cycles = cycle_decomposition(perm)
    return {
        "color": color,
        "q_residue": q_residue,
        "q_shift_values": sorted(q_shift_values),
        "uniform_q_shift": uniform_q_shift,
        "q_shift_is_unit": (q_shift is not None and math.gcd(q_shift, m) == 1),
        "Q_cycle_count": len(cycles),
        "Q_cycle_lengths": sorted(len(cycle) for cycle in cycles),
        "uniform_second_return_length": len(set(return_lengths)) == 1,
        "second_return_lengths": sorted(set(return_lengths)),
    }


def representative_q_trace(rule, color: int, m: int, q_residue: int = 0) -> Dict[str, object]:
    visited = set()
    orbit = []
    cur = (0, 0, 0)
    while cur not in visited:
        visited.add(cur)
        orbit.append({"abc": [cur[0], cur[1], cur[2]]})
        cur, _ = actual_T(rule, color, cur[0], cur[1], cur[2], q_residue, m)
    return {"color": color, "m": m, "q_residue": q_residue, "orbit_length": len(orbit), "orbit": orbit}


def validate_config(config: Dict[str, object], m_values: Sequence[int]) -> Dict[str, object]:
    validate_config_shape(config)
    overall = []
    start = time.perf_counter()

    for m in m_values:
        rule = build_rule(config, m)
        report = validate_rule(DIM, m, rule)
        p0_report = induced_p0_maps(report["nexts"], DIM, m)
        q_reports = [q_section_report(rule, color, m) for color in range(DIM)]
        overall.append(
            {
                "m": m,
                "all_hamilton": bool(report["all_hamilton"]),
                "sign_product": int(report["sign_product"]),
                "color_cycle_counts": [int(stat["cycle_count"]) for stat in report["color_stats"]],
                "max_cycle_lengths": max_cycle_lengths(report["nexts"]),
                "p0_cycle_counts": [int(item["cycle_count"]) for item in p0_report["color_maps"]],
                "p0_is_hamilton": [bool(item["is_hamilton"]) for item in p0_report["color_maps"]],
                "q_section_reports": q_reports,
            }
        )

    return {
        "task_id": "D5-ODD-CYCLIC-BULK-001",
        "candidate_name": config_name(config),
        "config": config,
        "tested_m_values": list(m_values),
        "runtime_sec": time.perf_counter() - start,
        "results": overall,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    if use_rich and Console is not None and Table is not None:
        console = Console()
        table = Table(title="D5 Odd Cyclic Bulk Validation")
        table.add_column("m", justify="right")
        table.add_column("V cycles")
        table.add_column("max cycle lengths")
        table.add_column("P0 cycles")
        table.add_column("Q cycles")
        for item in summary["results"]:
            table.add_row(
                str(item["m"]),
                str(item["color_cycle_counts"]),
                str(item["max_cycle_lengths"]),
                str(item["p0_cycle_counts"]),
                str([report["Q_cycle_count"] for report in item["q_section_reports"]]),
            )
        console.print(table)
        console.print(f"runtime_sec: {summary['runtime_sec']:.3f}")
        return

    print(f"candidate_name: {summary['candidate_name']}")
    for item in summary["results"]:
        print(
            f"m={item['m']} V_cycles={item['color_cycle_counts']} "
            f"max_lengths={item['max_cycle_lengths']} P0_cycles={item['p0_cycle_counts']} "
            f"Q_cycles={[report['Q_cycle_count'] for report in item['q_section_reports']]}"
        )
    print(f"runtime_sec: {summary['runtime_sec']:.3f}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate d=5 odd cyclic-bulk candidate configurations.")
    parser.add_argument("--config-json", type=Path, required=True, help="candidate config JSON file")
    parser.add_argument("--m-list", default="3,5,7", help="comma-separated odd m values to validate")
    parser.add_argument("--out", type=Path, help="write JSON summary to this path")
    parser.add_argument("--trace-dir", type=Path, help="write representative Q traces to this directory")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    use_rich = not args.no_rich and Console is not None and track is not None
    config = json.loads(args.config_json.read_text())
    summary = validate_config(config, _parse_m_list(args.m_list))

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2))

    if args.trace_dir is not None:
        args.trace_dir.mkdir(parents=True, exist_ok=True)
        for m in _parse_m_list(args.m_list):
            rule = build_rule(config, m)
            payload = {
                "m": m,
                "candidate_name": summary["candidate_name"],
                "traces": [representative_q_trace(rule, color, m) for color in range(DIM)],
            }
            (args.trace_dir / f"q_traces_m{m}.json").write_text(json.dumps(payload, indent=2))

    _print_summary(summary, use_rich=use_rich)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
