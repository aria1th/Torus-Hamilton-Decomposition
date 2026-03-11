#!/usr/bin/env python3
"""Extract a recursive second bit b2 from post-tail_cut residual fragments."""

from __future__ import annotations

import argparse
import json
import platform
import time
from collections import Counter
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, List, Sequence

TASK_ID = "D5-ACTIVE-TAIL-GRAMMAR-002"

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


def _subset_to_mask(deltas: Sequence[int]) -> int:
    mask = 0
    for delta in deltas:
        mask |= 1 << (int(delta) - 1)
    return mask


def _mask_to_subset(mask: int, *, m: int) -> List[int]:
    return [delta for delta in range(1, m) if mask & (1 << (delta - 1))]


def _canonical_masks(m: int) -> List[int]:
    vertex_count = m - 1
    return [((submask << 1) | 1) for submask in range(1 << (vertex_count - 1))]


def _cut_weight(mask: int, hyperedges: Dict[int, int], *, m: int) -> int:
    all_mask = (1 << (m - 1)) - 1
    comp = all_mask ^ mask
    total = 0
    for edge_mask, weight in hyperedges.items():
        if (edge_mask & mask) and (edge_mask & comp):
            total += weight
    return total


def _optimize(hyperedges: Dict[int, int], *, m: int) -> Dict[str, object]:
    baseline = sum((edge_mask.bit_count() - 1) * weight for edge_mask, weight in hyperedges.items())
    rows = []
    for mask in _canonical_masks(m):
        cut = _cut_weight(mask, hyperedges, m=m)
        rows.append(
            {
                "delta_subset": _mask_to_subset(mask, m=m),
                "cut_weight": cut,
                "post_split_total_excess": baseline - cut,
            }
        )
    rows.sort(key=lambda row: (-row["cut_weight"], row["delta_subset"]))
    best = rows[0]
    second = next((row["cut_weight"] for row in rows if row["cut_weight"] < best["cut_weight"]), None)
    return {
        "baseline_total_excess": baseline,
        "optimal_delta_subset": best["delta_subset"],
        "best_cut_weight": best["cut_weight"],
        "post_split_total_excess": best["post_split_total_excess"],
        "runner_up_cut_gap": best["cut_weight"] - second if second is not None else None,
        "unique_mod_complement": len([row for row in rows if row["cut_weight"] == best["cut_weight"]]) == 1,
    }


def run_extract(
    signature_summary: Dict[str, object],
    hypergraph_extract: Dict[str, object],
    *,
    m_values: Sequence[int],
) -> Dict[str, object]:
    start = time.perf_counter()
    signature_by_m = {int(item["m"]): item for item in signature_summary["per_m"]}
    extract_by_m = {int(item["m"]): item for item in hypergraph_extract["per_m"]}
    per_m = []

    for m in m_values:
        b1_set = {int(delta) for delta in signature_by_m[m]["tail_cut_subset"]}
        state_rows = extract_by_m[m]["state_rows"]
        hyperedges = Counter()
        fragment_hist = Counter()
        for row in state_rows:
            deltas = set(int(delta) for delta in row["delta_values"])
            for fragment in (deltas & b1_set, deltas - b1_set):
                if len(fragment) <= 1:
                    continue
                hyperedges[_subset_to_mask(sorted(fragment))] += 1
                fragment_hist[len(fragment)] += 1
        optimize = _optimize(dict(hyperedges), m=m)
        per_m.append(
            {
                "m": m,
                "b1_subset": sorted(b1_set),
                "residual_fragment_hyperedge_count": sum(hyperedges.values()),
                "residual_fragment_support_histogram": {str(size): count for size, count in sorted(fragment_hist.items())},
                "b2_optimum": optimize,
                "b2_lookup": {
                    str(delta): int(delta in optimize["optimal_delta_subset"])
                    for delta in range(1, m)
                },
            }
        )

    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": {"python_version": platform.python_version(), "rich_version": _rich_version()},
        "m_values": list(m_values),
        "per_m": per_m,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [f"task_id: {summary['task_id']}", f"runtime_sec: {summary['runtime_sec']:.3f}"]
    for item in summary["per_m"]:
        lines.append(
            f"m={item['m']} b1={item['b1_subset']} b2={item['b2_optimum']['optimal_delta_subset']} "
            f"residual={item['b2_optimum']['post_split_total_excess']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract a recursive second bit b2 from residual post-tail_cut fragments.")
    parser.add_argument(
        "--signature-summary-json",
        type=Path,
        default=Path("artifacts/d5_tail_cut_quotient_rerun_001/data/signature_summary.json"),
        help="tail_cut signature summary JSON",
    )
    parser.add_argument(
        "--hypergraph-extract-json",
        type=Path,
        default=Path("artifacts/d5_tail_automaton_bit_extraction_001/data/hypergraph_extract.json"),
        help="exact residual support extraction JSON",
    )
    parser.add_argument("--m-list", default="5,7,9", help="comma-separated moduli")
    parser.add_argument("--out", type=Path, required=True, help="write JSON summary here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    signature_summary = json.loads(args.signature_summary_json.read_text())
    hypergraph_extract = json.loads(args.hypergraph_extract_json.read_text())
    summary = run_extract(signature_summary, hypergraph_extract, m_values=_parse_m_list(args.m_list))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
