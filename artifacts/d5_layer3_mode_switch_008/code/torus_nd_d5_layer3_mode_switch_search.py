#!/usr/bin/env python3
"""Exact search for the d=5 layer-3 one-flag mode-switch family."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from torus_nd_d5_layer3_mode_switch_common import (
    PILOT_M_VALUES,
    SIMPLE_FLAG_DESCRIPTIONS,
    SIMPLE_FLAG_NAMES,
    TASK_ID,
    Rule,
    environment_block,
    evaluate_rule,
    exact_signature_catalog,
    exact_signature_rows,
    overall_rank_key,
    parse_args_m_list,
    precompute_m,
    runtime_since,
    simple_flag_rows,
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
    }


def _best_rows(rows: Sequence[Dict[str, object]], kind: str, limit: int = 20) -> List[Dict[str, object]]:
    picked = [item for item in rows if item["clean_all"] and item["strict_all"] and item["overall_kind"] == kind]
    picked.sort(key=overall_rank_key)
    return picked[:limit]


def _family_summary_simple(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    out = []
    for flag_name in SIMPLE_FLAG_NAMES:
        group = [item for item in rows if item["rule"]["predecessor_flag_name"] == flag_name]
        counts = _regime_counts(group)
        out.append(
            {
                "predecessor_flag_name": flag_name,
                "predecessor_flag_description": SIMPLE_FLAG_DESCRIPTIONS[flag_name],
                "raw_rule_count": len(group),
                "counts": counts,
                "best_both_rules": _best_rows(group, "both", limit=8),
                "best_cycle_only_rules": _best_rows(group, "cycle_only", limit=8),
                "best_monodromy_only_rules": _best_rows(group, "monodromy_only", limit=8),
                "best_trivial_rules": _best_rows(group, "trivial", limit=8),
            }
        )
    return out


def _family_summary_exact(rows: Sequence[Dict[str, object]]) -> Dict[str, object]:
    return {
        "raw_rule_count": len(rows),
        "counts": _regime_counts(rows),
        "best_both_rules": _best_rows(rows, "both", limit=12),
        "best_cycle_only_rules": _best_rows(rows, "cycle_only", limit=12),
        "best_monodromy_only_rules": _best_rows(rows, "monodromy_only", limit=12),
        "best_trivial_rules": _best_rows(rows, "trivial", limit=12),
    }


def _select_validation_candidates(simple_rows: Sequence[Dict[str, object]], exact_rows: Sequence[Dict[str, object]] | None) -> List[Dict[str, object]]:
    selected: List[Dict[str, object]] = []
    seen: set[Tuple[object, ...]] = set()

    def add_rows(rows: Iterable[Dict[str, object]], prefix: str) -> None:
        for index, item in enumerate(rows):
            _append_candidate(selected, seen, item, f"{prefix}_{index}")

    clean_unique: Dict[Tuple[object, ...], Dict[str, object]] = {}
    for item in list(simple_rows) + list(exact_rows or []):
        if not item["clean_all"]:
            continue
        clean_unique.setdefault(tuple(item["rule"]["effective_key"]), item)

    clean_unique_rows = sorted(clean_unique.values(), key=overall_rank_key)
    if len(clean_unique_rows) <= 1000:
        add_rows(clean_unique_rows, "clean_survivor")
        return selected

    for family_name, rows in (("simple", simple_rows), ("exact_signature", exact_rows or [])):
        for kind in ("both", "monodromy_only", "cycle_only", "trivial"):
            add_rows(_best_rows(rows, kind, limit=50 if kind == "cycle_only" else 20), f"{family_name}_{kind}")
    return selected


def _evaluate_rows(
    rows: Sequence[Rule],
    *,
    pre_by_m: Dict[int, Dict[str, object]],
    m_values: Sequence[int],
    use_rich: bool,
    description: str,
) -> List[Dict[str, object]]:
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
        task = progress.add_task(description, total=len(rows))
    for rule in rows:
        out.append(evaluate_rule(pre_by_m, rule, m_values=m_values))
        if progress is not None and task is not None:
            progress.advance(task)
    if progress is not None:
        progress.stop()
    return out


def run_search(*, m_values: Sequence[int], use_rich: bool) -> Dict[str, object]:
    start = __import__("time").perf_counter()
    signature_catalog = exact_signature_catalog(m_values)
    signature_to_id = signature_catalog["signature_to_id"]
    signature_rows = signature_catalog["rows"]
    pre_by_m = {m: precompute_m(m, signature_to_id) for m in m_values}

    simple_rules = simple_flag_rows()
    simple_rows = _evaluate_rows(simple_rules, pre_by_m=pre_by_m, m_values=m_values, use_rich=use_rich, description="simple flags")
    simple_summary = {
        "raw_rule_count": len(simple_rules),
        "counts": _regime_counts(simple_rows),
        "flag_families": _family_summary_simple(simple_rows),
        "best_both_rules": _best_rows(simple_rows, "both"),
        "best_cycle_only_rules": _best_rows(simple_rows, "cycle_only"),
        "best_monodromy_only_rules": _best_rows(simple_rows, "monodromy_only"),
        "best_trivial_rules": _best_rows(simple_rows, "trivial"),
    }

    exact_rows = None
    exact_summary = None
    if simple_summary["counts"]["both_count"] == 0:
        exact_rules = exact_signature_rows(len(signature_rows))
        exact_rows = _evaluate_rows(
            exact_rules,
            pre_by_m=pre_by_m,
            m_values=m_values,
            use_rich=use_rich,
            description="exact signature fallback",
        )
        exact_summary = _family_summary_exact(exact_rows)
        exact_summary["signature_class_count"] = len(signature_rows)
        exact_summary["signature_classes"] = signature_rows

    validation_candidates = _select_validation_candidates(simple_rows, exact_rows)
    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "pilot_m_values": list(m_values),
        "search_shape": {
            "representative_old_bit_name": "q=-1",
            "layer2_orientations": ["0/2", "2/0"],
            "layer3_modes_per_p_slice": ["0/3", "3/0", "2/3", "3/2", "3/3"],
            "simple_predecessor_flags": list(SIMPLE_FLAG_NAMES),
            "simple_raw_rule_count": len(simple_rules),
            "fallback_trigger": "run exact predecessor-local signature family iff simple both_count = 0",
            "exact_signature_class_count": len(signature_rows),
        },
        "simple_predecessor_flags": simple_summary,
        "exact_signature_fallback": exact_summary,
        "validation_candidate_count": len(validation_candidates),
        "recommended_next_step": (
            "If no one-flag family produces both moving U_0 cycles and nonzero monodromy, move to a two-bit layer-3 local grammar."
        ),
    }
    return {"summary": summary, "validation_candidates": validation_candidates}


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            f"simple clean={summary['simple_predecessor_flags']['counts']['clean_survivor_count']} "
            f"strict={summary['simple_predecessor_flags']['counts']['strict_survivor_count']} "
            f"both={summary['simple_predecessor_flags']['counts']['both_count']} "
            f"cycle={summary['simple_predecessor_flags']['counts']['cycle_only_count']} "
            f"mono={summary['simple_predecessor_flags']['counts']['monodromy_only_count']} "
            f"trivial={summary['simple_predecessor_flags']['counts']['trivial_count']}"
        ),
    ]
    if summary["exact_signature_fallback"] is not None:
        exact = summary["exact_signature_fallback"]
        lines.append(
            (
                f"exact clean={exact['counts']['clean_survivor_count']} "
                f"strict={exact['counts']['strict_survivor_count']} "
                f"both={exact['counts']['both_count']} "
                f"cycle={exact['counts']['cycle_only_count']} "
                f"mono={exact['counts']['monodromy_only_count']} "
                f"trivial={exact['counts']['trivial_count']}"
            )
        )
    for row in summary["simple_predecessor_flags"]["best_both_rules"][:3]:
        rule = row["rule"]
        lines.append(
            f"simple-both flag={rule['predecessor_flag_name']} l2={rule['layer2_orientation']} "
            f"p0={rule['layer3_mode_p0']['name']} p1={rule['layer3_mode_p1']['name']}"
        )
    if summary["exact_signature_fallback"] is not None:
        for row in summary["exact_signature_fallback"]["best_both_rules"][:3]:
            rule = row["rule"]
            lines.append(
                f"exact-both l2={rule['layer2_orientation']} p0={rule['layer3_mode_p0']['name']} "
                f"p1={rule['layer3_mode_p1']['name']} mask={rule['exact_signature_mask']}"
            )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the d=5 layer-3 one-flag mode-switch family.")
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
