#!/usr/bin/env python3
"""Search the d=5 wu2-secondary exact-twist family."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

from torus_nd_d5_wu2_secondary_exact_twist_common import (
    CYCLE_BASELINE_TOTAL_U_CYCLES,
    KNOWN_ANTI_COMPRESSIVE_TOTALS,
    MIXED_BASELINE_TOTAL_U_CYCLES,
    Rule,
    dependency_class,
    environment_block,
    evaluate_rule,
    load_cycle_baseline,
    load_mixed_baseline,
    overall_rank_key,
    parse_args_m_list,
    precompute_m,
    rule_rows,
    runtime_since,
)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover
    Console = None


def _serialize_row(result: Mapping[str, object]) -> Dict[str, object]:
    return {
        "rule": result["rule"],
        "dependency_class": dependency_class(Rule.from_payload(result["rule"])),
        "latin_color0_all": result["latin_color0_all"],
        "latin_all": result["latin_all"],
        "clean_all": result["clean_all"],
        "strict_all": result["strict_all"],
        "profile_kind": result["profile_kind"],
        "total_u_cycle_count": result["total_u_cycle_count"],
        "max_cycle_length": result["max_cycle_length"],
        "total_nonzero_monodromies": result["total_nonzero_monodromies"],
        "improves_mixed_baseline": result["improves_mixed_baseline"],
        "per_m": result["per_m"],
    }


def _counts(rows: Sequence[Dict[str, object]]) -> Dict[str, int]:
    clean_rows = [row for row in rows if row["clean_all"]]
    clean_strict = [row for row in clean_rows if row["strict_all"]]
    return {
        "row_count": len(rows),
        "clean_survivor_count": len(clean_rows),
        "strict_survivor_count": len(clean_strict),
        "both_count": sum(1 for row in clean_strict if row["profile_kind"] == "both"),
        "cycle_only_count": sum(1 for row in clean_strict if row["profile_kind"] == "cycle_only"),
        "monodromy_only_count": sum(1 for row in clean_strict if row["profile_kind"] == "monodromy_only"),
        "mixed_profile_count": sum(1 for row in clean_strict if row["profile_kind"] == "mixed_profile"),
        "trivial_count": sum(1 for row in clean_strict if row["profile_kind"] == "trivial"),
        "improved_mixed_count": sum(1 for row in clean_strict if row["improves_mixed_baseline"]),
    }


def _best_rows(rows: Sequence[Dict[str, object]], kind: str, limit: int = 12) -> List[Dict[str, object]]:
    picked = [row for row in rows if row["clean_all"] and row["strict_all"] and row["profile_kind"] == kind]
    picked.sort(key=overall_rank_key)
    return picked[:limit]


def _regime_histogram(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    counter = Counter()
    for row in rows:
        if row["clean_all"] and row["strict_all"]:
            counter[(row["profile_kind"], int(row["total_u_cycle_count"]))] += 1
    return [
        {"profile_kind": kind, "total_u_cycle_count": total_u_cycle_count, "count": count}
        for (kind, total_u_cycle_count), count in sorted(counter.items(), key=lambda item: (item[0][1], item[0][0]))
    ]


def _dependency_counts(rows: Sequence[Dict[str, object]]) -> Dict[str, int]:
    counter = Counter()
    for row in rows:
        if row["clean_all"] and row["strict_all"]:
            counter[row["dependency_class"]] += 1
    return dict(sorted(counter.items()))


def _group_counts(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped: Dict[tuple, List[Dict[str, object]]] = defaultdict(list)
    for row in rows:
        rule = row["rule"]
        key = (
            rule["layer2_base_name"],
            rule["controller_flag_name"],
            rule["layer3_old_bit_name"],
        )
        grouped[key].append(row)
    out = []
    for key, items in sorted(grouped.items()):
        out.append(
            {
                "group": {
                    "layer2_base_name": key[0],
                    "controller_flag_name": key[1],
                    "layer3_old_bit_name": key[2],
                },
                "counts": _counts(items),
                "dependency_class_counts": _dependency_counts(items),
                "best_mixed_rules": _best_rows(items, "both", 4),
            }
        )
    return out


def _candidate_rows(rows: Sequence[Dict[str, object]], label_prefix: str) -> List[Dict[str, object]]:
    selected = []
    seen = set()
    ordered = [row for row in rows if row["clean_all"]]
    ordered.sort(key=overall_rank_key)
    for index, row in enumerate(ordered):
        key = tuple(row["rule"]["effective_key"])
        if key in seen:
            continue
        seen.add(key)
        selected.append(
            {
                "label": f"{label_prefix}:{index}",
                "rule": row["rule"],
                "search_metrics": row,
            }
        )
    return selected


def _evaluate_stage(stage: str, pre_by_m, m_values) -> List[Dict[str, object]]:
    return [_serialize_row(evaluate_rule(pre_by_m, rule, m_values=m_values)) for rule in rule_rows(stage)]


def run_search(*, m_values: Sequence[int], mixed_baseline_json: Path | None, cycle_baseline_json: Path | None) -> Dict[str, object]:
    start = __import__("time").perf_counter()
    pre_by_m = {m: precompute_m(m) for m in m_values}
    stage1_rows = _evaluate_stage("stage1", pre_by_m, m_values)
    stage2_rows = []
    if _counts(stage1_rows)["improved_mixed_count"] == 0:
        stage2_rows = _evaluate_stage("stage2", pre_by_m, m_values)

    summary = {
        "task_id": "D5-WU2-SECONDARY-EXACT-TWIST-015",
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "pilot_m_values": list(m_values),
        "baseline_comparison": {
            "mixed_008": load_mixed_baseline(mixed_baseline_json),
            "cycle_007": load_cycle_baseline(cycle_baseline_json),
            "mixed_baseline_total_u_cycle_count": MIXED_BASELINE_TOTAL_U_CYCLES,
            "cycle_baseline_total_u_cycle_count": CYCLE_BASELINE_TOTAL_U_CYCLES,
            "known_anti_compressive_totals": list(KNOWN_ANTI_COMPRESSIVE_TOTALS),
        },
        "stage1": {
            "counts": _counts(stage1_rows),
            "regime_histogram": _regime_histogram(stage1_rows),
            "dependency_class_counts": _dependency_counts(stage1_rows),
            "group_summaries": _group_counts(stage1_rows),
            "best_mixed_rules": _best_rows(stage1_rows, "both"),
            "best_cycle_only_rules": _best_rows(stage1_rows, "cycle_only"),
            "best_monodromy_only_rules": _best_rows(stage1_rows, "monodromy_only"),
            "rule_rows": stage1_rows,
        },
        "stage2": None,
        "stage2_triggered": _counts(stage1_rows)["improved_mixed_count"] == 0,
    }
    if stage2_rows:
        summary["stage2"] = {
            "counts": _counts(stage2_rows),
            "regime_histogram": _regime_histogram(stage2_rows),
            "dependency_class_counts": _dependency_counts(stage2_rows),
            "group_summaries": _group_counts(stage2_rows),
            "best_mixed_rules": _best_rows(stage2_rows, "both"),
            "best_cycle_only_rules": _best_rows(stage2_rows, "cycle_only"),
            "best_monodromy_only_rules": _best_rows(stage2_rows, "monodromy_only"),
            "rule_rows": stage2_rows,
        }
    candidates = _candidate_rows(stage1_rows, "stage1")
    if stage2_rows:
        candidates.extend(_candidate_rows(stage2_rows, "stage2"))
    return {"summary": summary, "validation_candidates": candidates}


def _print_summary(summary: Mapping[str, object], *, use_rich: bool) -> None:
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
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the d=5 wu2-secondary exact-twist family.")
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--mixed-baseline-json", type=Path, help="override the mixed baseline validation summary")
    parser.add_argument("--cycle-baseline-json", type=Path, help="override the cycle baseline search summary")
    parser.add_argument("--out", type=Path, required=True, help="write search summary here")
    parser.add_argument("--candidates-out", type=Path, required=True, help="write validation candidates here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    result = run_search(
        m_values=parse_args_m_list(args.pilot_m_list),
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
