#!/usr/bin/env python3
"""Exact fixed-twist layer-2 geometry search for d=5 witnesses."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from torus_nd_d5_layer2_geometry_under_fixed_twist_common import (
    CANONICAL_TWIST,
    CONTROL_TWIST,
    CYCLE_BASELINE_TOTAL_U_CYCLES,
    MIXED_BASELINE_TOTAL_U_CYCLES,
    TASK_ID,
    Rule,
    control_rows,
    environment_block,
    evaluate_rule,
    load_cycle_baseline,
    load_mixed_baseline,
    overall_rank_key,
    parse_args_m_list,
    precompute_m,
    runtime_since,
    stage1_rows,
    stage2_rows,
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
                "profile_kind": item["profile_kind"],
                "total_u_cycle_count": item["total_u_cycle_count"],
                "max_cycle_length": item["max_cycle_length"],
                "total_nonzero_monodromies": item["total_nonzero_monodromies"],
                "improves_mixed_baseline": item["improves_mixed_baseline"],
            },
        }
    )


def _counts(rows: Sequence[Dict[str, object]]) -> Dict[str, int]:
    clean_strict = [item for item in rows if item["clean_all"] and item["strict_all"]]
    return {
        "clean_survivor_count": sum(1 for item in rows if item["clean_all"]),
        "strict_survivor_count": len(clean_strict),
        "both_count": sum(1 for item in clean_strict if item["profile_kind"] == "both"),
        "cycle_only_count": sum(1 for item in clean_strict if item["profile_kind"] == "cycle_only"),
        "monodromy_only_count": sum(1 for item in clean_strict if item["profile_kind"] == "monodromy_only"),
        "mixed_profile_count": sum(1 for item in clean_strict if item["profile_kind"] == "mixed_profile"),
        "trivial_count": sum(1 for item in clean_strict if item["profile_kind"] == "trivial"),
        "improved_mixed_count": sum(1 for item in clean_strict if item["improves_mixed_baseline"]),
    }


def _best_rows(rows: Sequence[Dict[str, object]], kind: str, limit: int = 20) -> List[Dict[str, object]]:
    picked = [item for item in rows if item["clean_all"] and item["strict_all"] and item["profile_kind"] == kind]
    picked.sort(key=overall_rank_key)
    return picked[:limit]


def _serialize_row(item: Dict[str, object]) -> Dict[str, object]:
    return {
        "rule": item["rule"],
        "latin_color0_all": item["latin_color0_all"],
        "latin_all": item["latin_all"],
        "clean_all": item["clean_all"],
        "strict_all": item["strict_all"],
        "profile_kind": item["profile_kind"],
        "total_u_cycle_count": item["total_u_cycle_count"],
        "max_cycle_length": item["max_cycle_length"],
        "total_nonzero_monodromies": item["total_nonzero_monodromies"],
        "improves_mixed_baseline": item["improves_mixed_baseline"],
        "per_m": item["per_m"],
    }


def _serialize_rows(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    return [_serialize_row(item) for item in rows]


def _layer2_key(rule_payload: Dict[str, object]) -> Tuple[object, ...]:
    return (
        rule_payload["layer2_flag_name"],
        rule_payload["layer2_mode_p0"]["name"],
        rule_payload["layer2_mode_p1"]["name"],
    )


def _flag_key(rule_payload: Dict[str, object]) -> Tuple[object, ...]:
    return (rule_payload["layer2_flag_name"],)


def _group_counts(rows: Sequence[Dict[str, object]], key_fn) -> List[Dict[str, object]]:
    grouped: Dict[Tuple[object, ...], List[Dict[str, object]]] = defaultdict(list)
    for item in rows:
        grouped[key_fn(item["rule"])].append(item)
    out = []
    for key, items in sorted(grouped.items()):
        out.append(
            {
                "key": list(key),
                "rule_count": len(items),
                "counts": _counts(items),
                "best_mixed_rule": _serialize_row(_best_rows(items, "both", limit=1)[0]) if any(
                    item["clean_all"] and item["strict_all"] and item["profile_kind"] == "both"
                    for item in items
                ) else None,
            }
        )
    return out


def _evaluate_rows(
    rules: Sequence[Rule],
    *,
    m_values: Sequence[int],
    use_rich: bool,
    description: str,
) -> List[Dict[str, object]]:
    bit_set = sorted({rule.layer3_bit_name for rule in rules})
    pre_by_bit = {bit_name: {m: precompute_m(m, bit_name) for m in m_values} for bit_name in bit_set}
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
        out.append(evaluate_rule(pre_by_bit[rule.layer3_bit_name], rule, m_values=m_values))
        if progress is not None and task is not None:
            progress.advance(task)
    if progress is not None:
        progress.stop()
    return out


def _candidate_rows(stage1_rows_: Sequence[Dict[str, object]], stage2_rows_: Sequence[Dict[str, object]] | None) -> List[Dict[str, object]]:
    selected: List[Dict[str, object]] = []
    seen: set[Tuple[object, ...]] = set()
    clean_rows = sorted(
        [item for item in list(stage1_rows_) + list(stage2_rows_ or []) if item["clean_all"]],
        key=overall_rank_key,
    )
    for index, item in enumerate(clean_rows):
        _append_candidate(selected, seen, item, f"clean_survivor_{index}")
    return selected


def _control_comparison(stage1_results: Sequence[Dict[str, object]], control_results: Sequence[Dict[str, object]]) -> Dict[str, object]:
    canonical = {_layer2_key(item["rule"]): item for item in stage1_results}
    control = {_layer2_key(item["rule"]): item for item in control_results}
    shared_keys = sorted(set(canonical) & set(control))
    same_cycle_signature = 0
    same_total_u_cycle_count = 0
    same_profile_kind = 0
    differing_examples = []
    for key in shared_keys:
        left = canonical[key]
        right = control[key]
        if left["cycle_signature"] == right["cycle_signature"]:
            same_cycle_signature += 1
        else:
            if len(differing_examples) < 8:
                differing_examples.append(
                    {
                        "layer2_key": list(key),
                        "canonical": _serialize_row(left),
                        "control": _serialize_row(right),
                    }
                )
        if left["total_u_cycle_count"] == right["total_u_cycle_count"]:
            same_total_u_cycle_count += 1
        if left["profile_kind"] == right["profile_kind"]:
            same_profile_kind += 1
    return {
        "rule_count": len(shared_keys),
        "same_cycle_signature_count": same_cycle_signature,
        "same_total_u_cycle_count_count": same_total_u_cycle_count,
        "same_profile_kind_count": same_profile_kind,
        "differing_examples": differing_examples,
    }


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

    stage1_rule_rows = stage1_rows()
    stage1_results = _evaluate_rows(stage1_rule_rows, m_values=m_values, use_rich=use_rich, description="stage1")
    stage1_counts = _counts(stage1_results)

    control_rule_rows = control_rows()
    control_results = _evaluate_rows(control_rule_rows, m_values=m_values, use_rich=use_rich, description="control")
    control_counts = _counts(control_results)
    control_summary = _control_comparison(stage1_results, control_results)

    improved_stage1_rules = [
        Rule.from_payload(item["rule"])
        for item in stage1_results
        if item["clean_all"] and item["strict_all"] and item["improves_mixed_baseline"]
    ]

    stage2_results = None
    stage2_counts = None
    stage2_rule_rows = []
    if improved_stage1_rules:
        stage2_rule_rows = stage2_rows(improved_stage1_rules)
        stage2_results = _evaluate_rows(stage2_rule_rows, m_values=m_values, use_rich=use_rich, description="stage2")
        stage2_counts = _counts(stage2_results)

    validation_candidates = _candidate_rows(stage1_results, stage2_results)
    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "pilot_m_values": list(m_values),
        "baseline_comparison": {
            "mixed_010": mixed_baseline,
            "cycle_007": cycle_baseline,
            "mixed_baseline_total_u_cycle_count": MIXED_BASELINE_TOTAL_U_CYCLES,
            "cycle_baseline_total_u_cycle_count": CYCLE_BASELINE_TOTAL_U_CYCLES,
        },
        "canonical_twist": CANONICAL_TWIST,
        "control_twist": CONTROL_TWIST,
        "stage1": {
            "raw_rule_count": len(stage1_rule_rows),
            "counts": stage1_counts,
            "flag_summaries": _group_counts(stage1_results, _flag_key),
            "layer2_pair_summaries": _group_counts(stage1_results, _layer2_key),
            "best_mixed_rules": _best_rows(stage1_results, "both"),
            "best_cycle_only_rules": _best_rows(stage1_results, "cycle_only"),
            "best_monodromy_only_rules": _best_rows(stage1_results, "monodromy_only"),
            "rule_rows": _serialize_rows(stage1_results),
        },
        "control": {
            "raw_rule_count": len(control_rule_rows),
            "counts": control_counts,
            "comparison_with_canonical": control_summary,
            "best_mixed_rules": _best_rows(control_results, "both"),
            "rule_rows": _serialize_rows(control_results),
        },
        "stage2": None,
        "stage2_triggered": bool(improved_stage1_rules),
        "validation_candidate_count": len(validation_candidates),
        "recommended_next_step": (
            "If no fixed-twist layer-2 rule beats the mixed baseline, widen layer-2 local state rather than layer 3."
        ),
    }
    if stage2_results is not None:
        summary["stage2"] = {
            "raw_rule_count": len(stage2_rule_rows),
            "geometry_rule_count": len({tuple(rule.effective_key()[:3]) for rule in improved_stage1_rules}),
            "counts": stage2_counts,
            "flag_summaries": _group_counts(stage2_results, _flag_key),
            "layer2_pair_summaries": _group_counts(stage2_results, _layer2_key),
            "best_mixed_rules": _best_rows(stage2_results, "both"),
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
        (
            f"control same_cycle_signature={summary['control']['comparison_with_canonical']['same_cycle_signature_count']}/"
            f"{summary['control']['comparison_with_canonical']['rule_count']}"
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
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the d=5 fixed-twist layer-2 geometry family.")
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--mixed-baseline-json", type=Path, help="override the mixed baseline validation summary")
    parser.add_argument("--cycle-baseline-json", type=Path, help="override the cycle baseline search summary")
    parser.add_argument("--out", type=Path, required=True, help="write search summary here")
    parser.add_argument("--candidates-out", type=Path, required=True, help="write validation candidate JSON here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    result = run_search(
        m_values=parse_args_m_list(args.pilot_m_list),
        use_rich=not args.no_rich and Progress is not None and Console is not None,
        mixed_baseline_json=args.mixed_baseline_json,
        cycle_baseline_json=args.cycle_baseline_json,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result["summary"], indent=2))
    args.candidates_out.parent.mkdir(parents=True, exist_ok=True)
    args.candidates_out.write_text(json.dumps({"candidates": result["validation_candidates"]}, indent=2))
    _print_summary(result["summary"], use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
