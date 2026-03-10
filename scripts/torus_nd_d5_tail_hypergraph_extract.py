#!/usr/bin/env python3
"""Extract the residual tail hypergraph for the saved strict-collapse phase-align field."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence

from torus_nd_d5_tail_hypergraph_common import (
    TASK_ID,
    collect_nonzero_occurrences,
    environment_payload,
    hyperedge_weight_rows,
    load_field_table,
    parse_m_list,
    state_support_rows,
)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover - optional dependency
    Console = None


def run_extract(field_json: Path, *, m_values: Sequence[int]) -> Dict[str, object]:
    start = time.perf_counter()
    _, table = load_field_table(field_json)

    per_m = []
    for m in m_values:
        occurrences = collect_nonzero_occurrences(table, m=m)
        state_rows = state_support_rows(occurrences, m=m)
        hyperedges = hyperedge_weight_rows(occurrences)
        support_hist = Counter(row["delta_support_size"] for row in state_rows if row["delta_support_size"] > 1)
        per_m.append(
            {
                "m": m,
                "delta_vertices": list(range(1, m)),
                "occurrence_count": len(occurrences),
                "residual_state_count": sum(1 for row in state_rows if row["delta_support_size"] > 1),
                "unique_support_count": len(hyperedges),
                "support_size_histogram": {str(size): count for size, count in sorted(support_hist.items())},
                "state_rows": state_rows,
                "hyperedges": hyperedges,
            }
        )

    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": environment_payload(),
        "field_json": str(field_json),
        "m_values": list(m_values),
        "per_m": per_m,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
    ]
    for item in summary["per_m"]:
        lines.append(
            f"m={item['m']} residual_states={item['residual_state_count']} "
            f"unique_supports={item['unique_support_count']} occurrences={item['occurrence_count']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract the residual tail hypergraph after Theta_AB + phase_align.")
    parser.add_argument(
        "--field-json",
        type=Path,
        default=Path("artifacts/d5_theta_ab_phase_align_001/data/best_strict_collapse_field.json"),
        help="saved strict-collapse field JSON",
    )
    parser.add_argument("--m-list", default="5,7,9,11,13", help="comma-separated moduli")
    parser.add_argument("--out", type=Path, required=True, help="write JSON summary here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    summary = run_extract(args.field_json, m_values=parse_m_list(args.m_list))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
