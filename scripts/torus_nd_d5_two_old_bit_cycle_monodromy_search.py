#!/usr/bin/env python3
"""Exact search for the minimal decoupled two-old-bit d=5 family."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Sequence

from torus_nd_d5_two_old_bit_cycle_monodromy_common import (
    LAYER2_ALTERNATES,
    LAYER3_ALTERNATE,
    OLD_BIT_NAMES,
    TASK_ID,
    Rule,
    environment_block,
    evaluate_rule,
    overall_rank_key,
    parse_args_m_list,
    precompute_m,
    runtime_since,
)

try:
    from rich.console import Console
    from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeElapsedColumn
except ImportError:  # pragma: no cover
    Console = None
    Progress = None


def _append_candidate(target: List[Dict[str, object]], seen: set[tuple], item: Dict[str, object], label: str) -> None:
    key = (
        item["rule"]["layer2_bit_name"],
        item["rule"]["layer3_bit_name"],
        item["rule"]["layer2_alt"],
        item["rule"]["layer2_orientation"],
        item["rule"]["layer3_orientation"],
    )
    if key in seen:
        return
    seen.add(key)
    target.append(
        {
            "label": label,
            "rule": item["rule"],
            "search_metrics": {
                "latin_all": item["latin_all"],
                "clean_all": item["clean_all"],
                "strict_all": item["strict_all"],
                "overall_kind": item["overall_kind"],
                "has_cycle": item["has_cycle"],
                "has_monodromy": item["has_monodromy"],
                "total_u_cycle_count": item["total_u_cycle_count"],
                "max_cycle_length": item["max_cycle_length"],
                "total_nonzero_monodromies": item["total_nonzero_monodromies"],
            },
        }
    )


def _rule_rows() -> List[Rule]:
    rows = []
    for layer2_bit_name in OLD_BIT_NAMES:
        for layer3_bit_name in OLD_BIT_NAMES:
            for layer2_alt in LAYER2_ALTERNATES:
                for layer2_table in ((2, layer2_alt), (layer2_alt, 2)):
                    for layer3_table in ((3, LAYER3_ALTERNATE), (LAYER3_ALTERNATE, 3)):
                        rows.append(
                            Rule(
                                layer2_bit_name=layer2_bit_name,
                                layer3_bit_name=layer3_bit_name,
                                layer2_alt=layer2_alt,
                                layer2_s0_anchor=layer2_table[0],
                                layer2_s1_anchor=layer2_table[1],
                                layer3_s0_anchor=layer3_table[0],
                                layer3_s1_anchor=layer3_table[1],
                            )
                        )
    return rows


def run_search(*, m_values: Sequence[int], use_rich: bool) -> Dict[str, object]:
    start = time.perf_counter()
    rules = _rule_rows()
    pre_by_pair = {
        (layer2_bit_name, layer3_bit_name): {m: precompute_m(m, layer2_bit_name, layer3_bit_name) for m in m_values}
        for layer2_bit_name in OLD_BIT_NAMES
        for layer3_bit_name in OLD_BIT_NAMES
    }
    rows = []
    by_pair = []
    validation_candidates: List[Dict[str, object]] = []
    candidate_seen: set[tuple] = set()

    progress = None
    task = None
    if use_rich and Progress is not None and Console is not None:
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
        )
        progress.start()
        task = progress.add_task("rules", total=len(rules))

    grouped: Dict[tuple, List[Dict[str, object]]] = {}
    for rule in rules:
        result = evaluate_rule(pre_by_pair[(rule.layer2_bit_name, rule.layer3_bit_name)], rule, m_values=m_values)
        rows.append(result)
        grouped.setdefault((rule.layer2_bit_name, rule.layer3_bit_name), []).append(result)
        if progress is not None and task is not None:
            progress.advance(task)

    if progress is not None:
        progress.stop()

    clean_survivors = [item for item in rows if item["clean_all"]]
    strict_survivors = [item for item in clean_survivors if item["strict_all"]]
    both_survivors = [item for item in strict_survivors if item["overall_kind"] == "both"]
    cycle_only_survivors = [item for item in strict_survivors if item["overall_kind"] == "cycle_only"]
    monodromy_only_survivors = [item for item in strict_survivors if item["overall_kind"] == "monodromy_only"]
    trivial_survivors = [item for item in strict_survivors if item["overall_kind"] == "trivial"]

    clean_survivors.sort(key=overall_rank_key)
    strict_survivors.sort(key=overall_rank_key)
    both_survivors.sort(key=overall_rank_key)
    cycle_only_survivors.sort(key=overall_rank_key)
    monodromy_only_survivors.sort(key=overall_rank_key)
    trivial_survivors.sort(key=overall_rank_key)

    for pair, items in sorted(grouped.items()):
        pair_clean = [item for item in items if item["clean_all"]]
        pair_strict = [item for item in pair_clean if item["strict_all"]]
        pair_clean.sort(key=overall_rank_key)
        pair_strict.sort(key=overall_rank_key)
        row = {
            "layer2_bit_name": pair[0],
            "layer3_bit_name": pair[1],
            "rule_count": len(items),
            "clean_count": len(pair_clean),
            "strict_count": len(pair_strict),
            "both_count": sum(1 for item in pair_strict if item["overall_kind"] == "both"),
            "cycle_only_count": sum(1 for item in pair_strict if item["overall_kind"] == "cycle_only"),
            "monodromy_only_count": sum(1 for item in pair_strict if item["overall_kind"] == "monodromy_only"),
            "trivial_count": sum(1 for item in pair_strict if item["overall_kind"] == "trivial"),
            "best_rule": pair_strict[0] if pair_strict else None,
        }
        by_pair.append(row)
        if pair_strict:
            _append_candidate(validation_candidates, candidate_seen, pair_strict[0], f"pair_{pair[0]}__{pair[1]}_best")

    for idx, item in enumerate(clean_survivors):
        _append_candidate(validation_candidates, candidate_seen, item, f"clean_survivor_{idx}")

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "pilot_m_values": list(m_values),
        "search_space": {
            "ordered_bit_pairs": len(OLD_BIT_NAMES) ** 2,
            "layer2_alternates": list(LAYER2_ALTERNATES),
            "layer2_orientations": ["2/a", "a/2"],
            "layer3_orientations": ["3/0", "0/3"],
            "rule_count": len(rules),
        },
        "pair_summaries": by_pair,
        "global_counts": {
            "clean_survivor_count": len(clean_survivors),
            "strict_survivor_count": len(strict_survivors),
            "both_count": len(both_survivors),
            "cycle_only_count": len(cycle_only_survivors),
            "monodromy_only_count": len(monodromy_only_survivors),
            "trivial_count": len(trivial_survivors),
        },
        "best_both_rules": both_survivors[:20],
        "best_cycle_only_rules": cycle_only_survivors[:20],
        "best_monodromy_only_rules": monodromy_only_survivors[:20],
        "best_trivial_rules": trivial_survivors[:20],
        "recommended_next_step": (
            "If no combined witness exists, add predecessor-tail information to one layer only."
        ),
    }
    return {"summary": summary, "validation_candidates": validation_candidates}


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            f"clean={summary['global_counts']['clean_survivor_count']} "
            f"strict={summary['global_counts']['strict_survivor_count']} "
            f"both={summary['global_counts']['both_count']} "
            f"cycle_only={summary['global_counts']['cycle_only_count']} "
            f"monodromy_only={summary['global_counts']['monodromy_only_count']} "
            f"trivial={summary['global_counts']['trivial_count']}"
        ),
    ]
    for item in summary["best_both_rules"][:3]:
        lines.append(
            f"both s2={item['rule']['layer2_bit_name']} s3={item['rule']['layer3_bit_name']} "
            f"l2={item['rule']['layer2_orientation']} l3={item['rule']['layer3_orientation']} "
            f"U={item['total_u_cycle_count']} mono={item['total_nonzero_monodromies']}"
        )
    for item in summary["best_cycle_only_rules"][:2]:
        lines.append(
            f"cycle s2={item['rule']['layer2_bit_name']} s3={item['rule']['layer3_bit_name']} "
            f"l2={item['rule']['layer2_orientation']} l3={item['rule']['layer3_orientation']} "
            f"U={item['total_u_cycle_count']}"
        )
    for item in summary["best_monodromy_only_rules"][:2]:
        lines.append(
            f"mono s2={item['rule']['layer2_bit_name']} s3={item['rule']['layer3_bit_name']} "
            f"l2={item['rule']['layer2_orientation']} l3={item['rule']['layer3_orientation']} "
            f"mono={item['total_nonzero_monodromies']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the minimal decoupled two-old-bit d=5 family.")
    parser.add_argument("--m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--out", type=Path, required=True, help="write search summary JSON here")
    parser.add_argument("--candidates-out", type=Path, required=True, help="write validation candidates JSON here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    payload = run_search(m_values=parse_args_m_list(args.m_list), use_rich=not args.no_rich)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload["summary"], indent=2))
    args.candidates_out.parent.mkdir(parents=True, exist_ok=True)
    args.candidates_out.write_text(
        json.dumps({"task_id": TASK_ID, "pilot_m_values": parse_args_m_list(args.m_list), "candidates": payload["validation_candidates"]}, indent=2)
    )
    _print_summary(payload["summary"], use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
