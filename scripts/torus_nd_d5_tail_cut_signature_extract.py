#!/usr/bin/env python3
"""Extract incidence-signature classes and exact pilot tail_cut tables."""

from __future__ import annotations

import argparse
import json
import platform
import time
from collections import Counter, defaultdict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, List, Sequence

TASK_ID = "D5-TAIL-CUT-QUOTIENT-RERUN-001"

try:
    from rich.console import Console
except ImportError:  # pragma: no cover - optional dependency
    Console = None


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _rich_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def _signature_rows(state_rows: Sequence[Dict[str, object]], *, m: int) -> List[Dict[str, object]]:
    signatures = {delta: [] for delta in range(1, m)}
    support_sizes = {delta: 0 for delta in range(1, m)}
    for row in state_rows:
        delta_values = set(int(delta) for delta in row["delta_values"])
        for delta in range(1, m):
            bit = int(delta in delta_values)
            signatures[delta].append(bit)
            support_sizes[delta] += bit

    classes = defaultdict(list)
    for delta, signature in signatures.items():
        classes[tuple(signature)].append(delta)

    class_rows = []
    for class_id, members in enumerate(sorted(classes.values(), key=lambda item: (len(item), item))):
        representative = members[0]
        class_rows.append(
            {
                "class_id": class_id,
                "deltas": list(members),
                "size": len(members),
                "representative_delta": representative,
                "signature_hamming_weight": support_sizes[representative],
            }
        )

    delta_rows = [
        {
            "delta": delta,
            "support_count": support_sizes[delta],
            "class_id": next(row["class_id"] for row in class_rows if delta in row["deltas"]),
        }
        for delta in range(1, m)
    ]
    return {"class_rows": class_rows, "delta_rows": delta_rows}


def _post_cut_summary(state_rows: Sequence[Dict[str, object]], cut_set: set[int]) -> Dict[str, object]:
    fragment_hist = Counter()
    residual_fragment_hist = Counter()
    cut_state_count = 0
    post_split_excess = 0

    for row in state_rows:
        deltas = set(int(delta) for delta in row["delta_values"])
        left = deltas & cut_set
        right = deltas - cut_set
        if left and right:
            cut_state_count += 1
        for part in (left, right):
            if not part:
                continue
            fragment_hist[len(part)] += 1
            if len(part) > 1:
                residual_fragment_hist[len(part)] += 1
                post_split_excess += len(part) - 1

    return {
        "cut_state_count": cut_state_count,
        "post_split_total_excess": post_split_excess,
        "fragment_histogram": {str(size): count for size, count in sorted(fragment_hist.items())},
        "residual_fragment_histogram": {str(size): count for size, count in sorted(residual_fragment_hist.items())},
        "largest_first_residual_histogram": [
            {"support_size": size, "count": residual_fragment_hist[size]}
            for size in sorted(residual_fragment_hist, reverse=True)
        ],
    }


def run_extract(
    hypergraph_extract: Dict[str, object],
    hypergraph_optimize: Dict[str, object],
    *,
    m_values: Sequence[int],
) -> Dict[str, object]:
    start = time.perf_counter()
    optimize_by_m = {int(item["m"]): item for item in hypergraph_optimize["per_m"]}
    per_m = []

    for item in hypergraph_extract["per_m"]:
        m = int(item["m"])
        if m not in m_values:
            continue
        state_rows = item["state_rows"]
        signatures = _signature_rows(state_rows, m=m)
        cut_set = set(int(delta) for delta in optimize_by_m[m]["hypergraph_optimum"]["optimal_delta_subset"])
        post_cut = _post_cut_summary(state_rows, cut_set)
        per_m.append(
            {
                "m": m,
                "residual_state_count": item["residual_state_count"],
                "unique_support_count": item["unique_support_count"],
                "incidence_signature_class_count": len(signatures["class_rows"]),
                "all_classes_singleton": all(row["size"] == 1 for row in signatures["class_rows"]),
                "incidence_signature_classes": signatures["class_rows"],
                "delta_rows": signatures["delta_rows"],
                "tail_cut_lookup": {
                    str(delta): int(delta in cut_set)
                    for delta in range(1, m)
                },
                "tail_cut_subset": sorted(cut_set),
                "post_cut": post_cut,
            }
        )

    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": {"python_version": platform.python_version(), "rich_version": _rich_version()},
        "m_values": [item["m"] for item in per_m],
        "per_m": per_m,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [f"task_id: {summary['task_id']}", f"runtime_sec: {summary['runtime_sec']:.3f}"]
    for item in summary["per_m"]:
        lines.append(
            f"m={item['m']} classes={item['incidence_signature_class_count']} "
            f"singleton={item['all_classes_singleton']} tail_cut={item['tail_cut_subset']} "
            f"post_excess={item['post_cut']['post_split_total_excess']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract incidence-signature classes and exact pilot tail_cut tables.")
    parser.add_argument(
        "--hypergraph-extract-json",
        type=Path,
        default=Path("artifacts/d5_tail_automaton_bit_extraction_001/data/hypergraph_extract.json"),
        help="exact residual support extraction JSON",
    )
    parser.add_argument(
        "--hypergraph-optimize-json",
        type=Path,
        default=Path("artifacts/d5_tail_automaton_bit_extraction_001/data/hypergraph_optimize.json"),
        help="exact hypergraph optimization JSON",
    )
    parser.add_argument("--m-list", default="5,7,9", help="comma-separated moduli")
    parser.add_argument("--out", type=Path, required=True, help="write JSON summary here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    hypergraph_extract = json.loads(args.hypergraph_extract_json.read_text())
    hypergraph_optimize = json.loads(args.hypergraph_optimize_json.read_text())
    summary = run_extract(hypergraph_extract, hypergraph_optimize, m_values=_parse_m_list(args.m_list))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
