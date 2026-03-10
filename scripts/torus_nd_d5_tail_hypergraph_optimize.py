#!/usr/bin/env python3
"""Exact optimization of the residual D5 tail hypergraph."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from torus_nd_d5_tail_hypergraph_common import (
    TASK_ID,
    environment_payload,
    parse_m_list,
    subset_mask_to_deltas,
    support_rows_to_weight_map,
)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover - optional dependency
    Console = None


def _cut_weight(mask: int, hyperedges: Dict[int, int], *, all_mask: int) -> int:
    total = 0
    comp = all_mask ^ mask
    for edge_mask, weight in hyperedges.items():
        if (edge_mask & mask) and (edge_mask & comp):
            total += weight
    return total


def _graph_weights(hyperedges: Dict[int, int], *, vertex_count: int) -> Dict[Tuple[int, int], int]:
    weights: Dict[Tuple[int, int], int] = {}
    for edge_mask, weight in hyperedges.items():
        deltas = subset_mask_to_deltas(edge_mask, vertex_count=vertex_count)
        for left_index in range(len(deltas)):
            for right_index in range(left_index + 1, len(deltas)):
                pair = (deltas[left_index], deltas[right_index])
                weights[pair] = weights.get(pair, 0) + weight
    return weights


def _graph_cut_weight(mask: int, weights: Dict[Tuple[int, int], int]) -> int:
    total = 0
    for (left, right), weight in weights.items():
        left_in = bool(mask & (1 << (left - 1)))
        right_in = bool(mask & (1 << (right - 1)))
        if left_in != right_in:
            total += weight
    return total


def _canonical_masks(vertex_count: int) -> List[int]:
    out = []
    for submask in range(1 << (vertex_count - 1)):
        out.append((submask << 1) | 1)
    return out


def _antisymmetric_masks(m: int) -> List[int]:
    pairs = [(delta, m - delta) for delta in range(1, (m - 1) // 2 + 1)]
    out = []
    for submask in range(1 << max(0, len(pairs) - 1)):
        mask = 1
        for pair_index, (left, right) in enumerate(pairs[1:], start=1):
            choose_left = bool(submask & (1 << (pair_index - 1)))
            chosen = left if choose_left else right
            mask |= 1 << (chosen - 1)
        out.append(mask)
    return out


def _optimize_masks(
    masks: Sequence[int],
    hyperedges: Dict[int, int],
    *,
    vertex_count: int,
    graph_weights: Dict[Tuple[int, int], int],
) -> Dict[str, object]:
    all_mask = (1 << vertex_count) - 1
    baseline_excess = sum((edge_mask.bit_count() - 1) * weight for edge_mask, weight in hyperedges.items())
    rows = []
    for mask in masks:
        cut = _cut_weight(mask, hyperedges, all_mask=all_mask)
        rows.append(
            {
                "mask": mask,
                "delta_subset": subset_mask_to_deltas(mask, vertex_count=vertex_count),
                "hypergraph_cut_weight": cut,
                "residual_total_excess": baseline_excess - cut,
                "pair_graph_cut_weight": _graph_cut_weight(mask, graph_weights),
            }
        )
    rows.sort(key=lambda row: (-row["hypergraph_cut_weight"], row["delta_subset"]))
    best_cut = rows[0]["hypergraph_cut_weight"]
    best_rows = [row for row in rows if row["hypergraph_cut_weight"] == best_cut]
    second_best_cut = next((row["hypergraph_cut_weight"] for row in rows if row["hypergraph_cut_weight"] < best_cut), None)
    return {
        "baseline_total_excess": baseline_excess,
        "best_cut_weight": best_cut,
        "best_residual_total_excess": baseline_excess - best_cut,
        "runner_up_cut_gap": best_cut - second_best_cut if second_best_cut is not None else None,
        "optimal_solution_count": len(best_rows),
        "optimal_rows": best_rows,
        "all_rows_top20": rows[:20],
    }


def run_optimize(extract_summary: Dict[str, object]) -> Dict[str, object]:
    start = time.perf_counter()
    per_m = []
    for item in extract_summary["per_m"]:
        m = int(item["m"])
        vertex_count = m - 1
        hyperedges = support_rows_to_weight_map(item["hyperedges"])
        graph_weights = _graph_weights(hyperedges, vertex_count=vertex_count)
        unrestricted = _optimize_masks(_canonical_masks(vertex_count), hyperedges, vertex_count=vertex_count, graph_weights=graph_weights)
        graph_only = []
        for mask in _canonical_masks(vertex_count):
            graph_only.append(
                {
                    "mask": mask,
                    "delta_subset": subset_mask_to_deltas(mask, vertex_count=vertex_count),
                    "pair_graph_cut_weight": _graph_cut_weight(mask, graph_weights),
                }
            )
        graph_only.sort(key=lambda row: (-row["pair_graph_cut_weight"], row["delta_subset"]))
        graph_best = graph_only[0]
        graph_best_hyper_cut = _cut_weight(
            graph_best["mask"],
            hyperedges,
            all_mask=(1 << vertex_count) - 1,
        )
        antisymmetric = _optimize_masks(
            _antisymmetric_masks(m),
            hyperedges,
            vertex_count=vertex_count,
            graph_weights=graph_weights,
        )
        per_m.append(
            {
                "m": m,
                "vertex_count": vertex_count,
                "support_size_histogram": item["support_size_histogram"],
                "baseline_total_excess": unrestricted["baseline_total_excess"],
                "hypergraph_optimum": {
                    "unique_mod_complement": unrestricted["optimal_solution_count"] == 1,
                    "optimal_delta_subset": unrestricted["optimal_rows"][0]["delta_subset"],
                    "best_cut_weight": unrestricted["best_cut_weight"],
                    "best_residual_total_excess": unrestricted["best_residual_total_excess"],
                    "runner_up_cut_gap": unrestricted["runner_up_cut_gap"],
                    "optimal_rows": unrestricted["optimal_rows"],
                },
                "pair_graph_optimum": {
                    "optimal_delta_subset": graph_best["delta_subset"],
                    "pair_graph_cut_weight": graph_best["pair_graph_cut_weight"],
                    "hypergraph_cut_weight_under_graph_best": graph_best_hyper_cut,
                    "hypergraph_residual_total_excess_under_graph_best": unrestricted["baseline_total_excess"] - graph_best_hyper_cut,
                    "matches_hypergraph_optimum": graph_best["delta_subset"] == unrestricted["optimal_rows"][0]["delta_subset"],
                },
                "antisymmetric_optimum": {
                    "unique_mod_complement": antisymmetric["optimal_solution_count"] == 1,
                    "optimal_delta_subset": antisymmetric["optimal_rows"][0]["delta_subset"],
                    "best_cut_weight": antisymmetric["best_cut_weight"],
                    "best_residual_total_excess": antisymmetric["best_residual_total_excess"],
                    "runner_up_cut_gap": antisymmetric["runner_up_cut_gap"],
                    "matches_hypergraph_optimum": antisymmetric["optimal_rows"][0]["delta_subset"]
                    == unrestricted["optimal_rows"][0]["delta_subset"],
                },
            }
        )
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": environment_payload(),
        "m_values": [item["m"] for item in per_m],
        "per_m": per_m,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
    ]
    for item in summary["per_m"]:
        lines.append(
            f"m={item['m']} best={item['hypergraph_optimum']['optimal_delta_subset']} "
            f"graph={item['pair_graph_optimum']['optimal_delta_subset']} "
            f"antisym={item['antisymmetric_optimum']['optimal_delta_subset']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute exact hypergraph optima for the D5 residual tail supports.")
    parser.add_argument("--extract-json", type=Path, required=True, help="hypergraph extraction JSON")
    parser.add_argument("--out", type=Path, required=True, help="write optimization JSON here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    extract_summary = json.loads(args.extract_json.read_text())
    summary = run_optimize(extract_summary)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
