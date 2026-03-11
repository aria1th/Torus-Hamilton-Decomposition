#!/usr/bin/env python3
"""Exact graft search for strong mixed d=5 witnesses."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from torus_nd_d5_strong_cycle_mix_common import (
    CYCLE_BASELINE_TOTAL_U_CYCLES,
    MIXED_BASELINE_TOTAL_U_CYCLES,
    TASK_ID,
    Rule,
    environment_block,
    evaluate_rule,
    layer2_seed_rows,
    load_cycle_baseline,
    load_mixed_baseline,
    overall_rank_key,
    parse_args_m_list,
    precompute_m,
    runtime_since,
    stage_rows,
)

try:
    from rich.console import Console
    from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeElapsedColumn
except ImportError:  # pragma: no cover
    Console = None
    Progress = None


def _append_candidate(target: List[Dict[str, object]], seen: set[Tuple[object, ...]], item: Dict[str, object], label: str) -> None:
    key = tuple(item["rule"]["effective_key"])
    if key in seen:
        return
    seen.add(key)
    target.append(
        {
            "label": label,
            "rule": item["rule"],
            "search_metrics": {
                "latin_color0_all": item["latin_color0_all"],
                "latin_all": item["latin_all"],
                "clean_all": item["clean_all"],
                "strict_all": item["strict_all"],
                "overall_kind": item["overall_kind"],
                "has_cycle": item["has_cycle"],
                "has_monodromy": item["has_monodromy"],
                "total_u_cycle_count": item["total_u_cycle_count"],
                "max_cycle_length": item["max_cycle_length"],
                "total_nonzero_monodromies": item["total_nonzero_monodromies"],
                "improves_mixed_baseline": item["improves_mixed_baseline"],
            },
        }
    )


def _regime_counts(rows: Sequence[Dict[str, object]]) -> Dict[str, int]:
    return {
        "clean_survivor_count": sum(1 for item in rows if item["clean_all"]),
        "strict_survivor_count": sum(1 for item in rows if item["clean_all"] and item["strict_all"]),
        "both_count": sum(1 for item in rows if item["clean_all"] and item["strict_all"] and item["overall_kind"] == "both"),
        "cycle_only_count": sum(1 for item in rows if item["clean_all"] and item["strict_all"] and item["overall_kind"] == "cycle_only"),
        "monodromy_only_count": sum(1 for item in rows if item["clean_all"] and item["strict_all"] and item["overall_kind"] == "monodromy_only"),
        "trivial_count": sum(1 for item in rows if item["clean_all"] and item["strict_all"] and item["overall_kind"] == "trivial"),
        "improved_mixed_count": sum(1 for item in rows if item["improves_mixed_baseline"]),
    }


def _best_rows(rows: Sequence[Dict[str, object]], kind: str, limit: int = 20) -> List[Dict[str, object]]:
    picked = [item for item in rows if item["clean_all"] and item["strict_all"] and item["overall_kind"] == kind]
    picked.sort(key=overall_rank_key)
    return picked[:limit]


def _serialize_rows(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    return [
        {
            "rule": item["rule"],
            "latin_color0_all": item["latin_color0_all"],
            "latin_all": item["latin_all"],
            "clean_all": item["clean_all"],
            "strict_all": item["strict_all"],
            "overall_kind": item["overall_kind"],
            "total_u_cycle_count": item["total_u_cycle_count"],
            "max_cycle_length": item["max_cycle_length"],
            "total_nonzero_monodromies": item["total_nonzero_monodromies"],
            "improves_mixed_baseline": item["improves_mixed_baseline"],
            "per_m": item["per_m"],
        }
        for item in rows
    ]


def _seed_key(rule_payload: Dict[str, object]) -> Tuple[object, ...]:
    return (
        rule_payload["layer2_bit_name"],
        rule_payload["layer2_alt"],
        rule_payload["layer2_orientation"],
    )


def _gadget_key(rule_payload: Dict[str, object]) -> Tuple[object, ...]:
    return (
        rule_payload["layer3_bit_name"],
        rule_payload["predecessor_flag_name"],
        rule_payload["layer3_mode_p0"]["name"],
        rule_payload["layer3_mode_p1"]["name"],
    )


def _seed_summaries(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped: Dict[Tuple[object, ...], List[Dict[str, object]]] = defaultdict(list)
    for item in rows:
        grouped[_seed_key(item["rule"])].append(item)
    out = []
    for key, items in sorted(grouped.items()):
        counts = _regime_counts(items)
        out.append(
            {
                "layer2_bit_name": key[0],
                "layer2_alt": key[1],
                "layer2_orientation": key[2],
                "rule_count": len(items),
                "counts": counts,
                "best_mixed_rule": _best_rows(items, "both", limit=1)[0] if counts["both_count"] else None,
            }
        )
    return out


def _evaluate_stage(
    rules: Sequence[Rule],
    *,
    m_values: Sequence[int],
    use_rich: bool,
    description: str,
) -> List[Dict[str, object]]:
    pair_set = sorted({(rule.layer2_bit_name, rule.layer3_bit_name) for rule in rules})
    pre_by_pair = {
        pair: {m: precompute_m(m, pair[0], pair[1]) for m in m_values}
        for pair in pair_set
    }
    out = []
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
        task = progress.add_task(description, total=len(rules))
    for rule in rules:
        out.append(evaluate_rule(pre_by_pair[(rule.layer2_bit_name, rule.layer3_bit_name)], rule, m_values=m_values))
        if progress is not None and task is not None:
            progress.advance(task)
    if progress is not None:
        progress.stop()
    return out


def _candidate_rows(stage1_rows: Sequence[Dict[str, object]], stage2_rows: Sequence[Dict[str, object]] | None) -> List[Dict[str, object]]:
    selected: List[Dict[str, object]] = []
    seen: set[Tuple[object, ...]] = set()
    all_rows = list(stage1_rows) + list(stage2_rows or [])
    clean_rows = sorted([item for item in all_rows if item["clean_all"]], key=overall_rank_key)
    for index, item in enumerate(clean_rows):
        _append_candidate(selected, seen, item, f"clean_survivor_{index}")
    return selected


def run_search(
    *,
    m_values: Sequence[int],
    use_rich: bool,
    mixed_baseline_json: Path | None,
    cycle_baseline_json: Path | None,
) -> Dict[str, object]:
    start = __import__("time").perf_counter()
    cycle_baseline = load_cycle_baseline(cycle_baseline_json)
    mixed_baseline = load_mixed_baseline(mixed_baseline_json)

    stage1_rules = stage_rows("stage1")
    stage1_results = _evaluate_stage(stage1_rules, m_values=m_values, use_rich=use_rich, description="stage1")
    stage1_counts = _regime_counts(stage1_results)
    stage1_improves = stage1_counts["improved_mixed_count"] > 0

    stage2_results = None
    stage2_counts = None
    if not stage1_improves:
        stage2_rules = stage_rows("stage2")
        stage2_results = _evaluate_stage(stage2_rules, m_values=m_values, use_rich=use_rich, description="stage2")
        stage2_counts = _regime_counts(stage2_results)

    validation_candidates = _candidate_rows(stage1_results, stage2_results)
    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "pilot_m_values": list(m_values),
        "baseline_comparison": {
            "mixed_008": mixed_baseline,
            "cycle_007": cycle_baseline,
            "mixed_baseline_total_u_cycle_count": MIXED_BASELINE_TOTAL_U_CYCLES,
            "cycle_baseline_total_u_cycle_count": CYCLE_BASELINE_TOTAL_U_CYCLES,
        },
        "layer2_seed_count": len(layer2_seed_rows()),
        "stage1": {
            "raw_rule_count": len(stage1_rules),
            "counts": stage1_counts,
            "seed_summaries": _seed_summaries(stage1_results),
            "best_mixed_rules": _best_rows(stage1_results, "both"),
            "best_cycle_only_rules": _best_rows(stage1_results, "cycle_only"),
            "best_monodromy_only_rules": _best_rows(stage1_results, "monodromy_only"),
            "rule_rows": _serialize_rows(stage1_results),
        },
        "stage2": None,
        "stage2_triggered": not stage1_improves,
        "validation_candidate_count": len(validation_candidates),
        "recommended_next_step": (
            "If no mixed survivor improves the baseline even after Stage 2, move to a wider layer-3 gadget or a theorem-level classification of the current twist graft."
        ),
    }
    if stage2_results is not None:
        summary["stage2"] = {
            "raw_rule_count": len(stage_rows("stage2")),
            "counts": stage2_counts,
            "seed_summaries": _seed_summaries(stage2_results),
            "best_mixed_rules": _best_rows(stage2_results, "both"),
            "best_cycle_only_rules": _best_rows(stage2_results, "cycle_only"),
            "best_monodromy_only_rules": _best_rows(stage2_results, "monodromy_only"),
            "rule_rows": _serialize_rows(stage2_results),
        }
    return {"summary": summary, "validation_candidates": validation_candidates}


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            f"stage1 clean={summary['stage1']['counts']['clean_survivor_count']} "
            f"strict={summary['stage1']['counts']['strict_survivor_count']} "
            f"both={summary['stage1']['counts']['both_count']} "
            f"improved={summary['stage1']['counts']['improved_mixed_count']}"
        ),
    ]
    if summary["stage2"] is not None:
        lines.append(
            (
                f"stage2 clean={summary['stage2']['counts']['clean_survivor_count']} "
                f"strict={summary['stage2']['counts']['strict_survivor_count']} "
                f"both={summary['stage2']['counts']['both_count']} "
                f"improved={summary['stage2']['counts']['improved_mixed_count']}"
            )
        )
    for row in summary["stage1"]["best_mixed_rules"][:3]:
        r = row["rule"]
        lines.append(
            f"stage1-both seed={r['layer2_bit_name']}:{r['layer2_orientation']} "
            f"l3={r['layer3_bit_name']} {r['predecessor_flag_name']} "
            f"({r['layer3_mode_p0']['name']},{r['layer3_mode_p1']['name']}) "
            f"U={row['total_u_cycle_count']} improve={row['improves_mixed_baseline']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the d=5 strong mixed graft family.")
    parser.add_argument("--m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--out", type=Path, required=True, help="write search summary JSON here")
    parser.add_argument("--candidates-out", type=Path, required=True, help="write validation candidates JSON here")
    parser.add_argument(
        "--mixed-baseline-json",
        type=Path,
        default=Path("artifacts/d5_layer3_mode_switch_008/data/validation_summary.json"),
        help="validation summary JSON for the Session 26 mixed baseline",
    )
    parser.add_argument(
        "--cycle-baseline-json",
        type=Path,
        default=Path("artifacts/d5_layer3_alt2_decoupled_007/data/search_summary.json"),
        help="search summary JSON for the strongest earlier cycle-only baseline",
    )
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    payload = run_search(
        m_values=parse_args_m_list(args.m_list),
        use_rich=not args.no_rich,
        mixed_baseline_json=args.mixed_baseline_json,
        cycle_baseline_json=args.cycle_baseline_json,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload["summary"], indent=2))
    args.candidates_out.parent.mkdir(parents=True, exist_ok=True)
    args.candidates_out.write_text(
        json.dumps(
            {
                "task_id": TASK_ID,
                "pilot_m_values": parse_args_m_list(args.m_list),
                "candidates": payload["validation_candidates"],
            },
            indent=2,
        )
    )
    _print_summary(payload["summary"], use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
