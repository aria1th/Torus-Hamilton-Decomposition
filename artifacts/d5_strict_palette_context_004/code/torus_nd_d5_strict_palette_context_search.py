#!/usr/bin/env python3
"""Exhaustive strict-friendly context search for d=5 active layer-2/3 grammars."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Sequence

from torus_nd_d5_strict_palette_context_common import (
    STRICT_ALTERNATES,
    TASK_ID,
    environment_block,
    evaluate_rule_search,
    parse_m_list,
    precompute_m,
    search_rank_key,
    strict_rank_key,
    unique_rules_for_family,
)

try:
    from rich.console import Console
    from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeElapsedColumn
except ImportError:  # pragma: no cover - optional dependency
    Console = None
    Progress = None


def _rule_key(item: Dict[str, object]) -> tuple:
    return (
        tuple(item["rule"]["effective_key"]["layer2_anchors"]),
        tuple(item["rule"]["effective_key"]["layer3_anchors"]),
    )


def _append_candidate(target: List[Dict[str, object]], seen: set[tuple], item: Dict[str, object], label: str) -> None:
    key = _rule_key(item)
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
                "any_nontrivial_u": item["any_nontrivial_u"],
                "total_u_cycle_count": item["total_u_cycle_count"],
                "total_nonzero_monodromies": item["total_nonzero_monodromies"],
            },
        }
        )


def _dedupe_results(items: List[Dict[str, object]], *, strict: bool) -> List[Dict[str, object]]:
    best_by_key: Dict[tuple, Dict[str, object]] = {}
    for item in items:
        key = _rule_key(item)
        incumbent = best_by_key.get(key)
        if incumbent is None:
            best_by_key[key] = item
            continue
        rank = strict_rank_key if strict else search_rank_key
        if rank(item) < rank(incumbent):
            best_by_key[key] = item
    out = list(best_by_key.values())
    out.sort(key=strict_rank_key if strict else search_rank_key)
    return out


def run_search(*, m_values: Sequence[int], use_rich: bool) -> Dict[str, object]:
    start = time.perf_counter()
    pre_by_m = {m: precompute_m(m) for m in m_values}
    family_rows = []
    global_clean = []
    global_strict = []
    validation_candidates: List[Dict[str, object]] = []
    candidate_seen: set[tuple] = set()

    family_pairs = [(layer2_alt, layer3_alt) for layer2_alt in STRICT_ALTERNATES for layer3_alt in STRICT_ALTERNATES]
    progress = None
    task_id = None
    if use_rich and Progress is not None and Console is not None:
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
        )
        progress.start()
        task_id = progress.add_task("families", total=len(family_pairs))

    for layer2_alt, layer3_alt in family_pairs:
        family_start = time.perf_counter()
        unique_entries = unique_rules_for_family(layer2_alt, layer3_alt)
        family_results = []
        raw_counts = {
            "total_tables": 32 * 32,
            "latin_all": 0,
            "clean_all": 0,
            "strict_all": 0,
            "strict_with_nontrivial_u": 0,
        }
        for entry in unique_entries.values():
            result = evaluate_rule_search(pre_by_m, entry["rule"], m_values=m_values)
            result["raw_multiplicity"] = entry["raw_multiplicity"]
            family_results.append(result)
            if result["latin_all"]:
                raw_counts["latin_all"] += entry["raw_multiplicity"]
            if result["clean_all"]:
                raw_counts["clean_all"] += entry["raw_multiplicity"]
            if result["strict_all"]:
                raw_counts["strict_all"] += entry["raw_multiplicity"]
            if result["strict_all"] and result["any_nontrivial_u"]:
                raw_counts["strict_with_nontrivial_u"] += entry["raw_multiplicity"]

        clean_results = [item for item in family_results if item["clean_all"]]
        strict_results = [item for item in clean_results if item["strict_all"]]
        clean_results.sort(key=search_rank_key)
        strict_results.sort(key=strict_rank_key)
        global_clean.extend(clean_results)
        global_strict.extend(strict_results)

        family_row = {
            "family": {"layer2_alt": layer2_alt, "layer3_alt": layer3_alt},
            "effective_rule_count": len(family_results),
            "runtime_sec": time.perf_counter() - family_start,
            "raw_counts": raw_counts,
            "effective_counts": {
                "latin_all": sum(1 for item in family_results if item["latin_all"]),
                "clean_all": len(clean_results),
                "strict_all": len(strict_results),
                "clean_context_dependent": sum(1 for item in clean_results if item["rule"]["context_dependent"]),
                "strict_context_dependent": sum(1 for item in strict_results if item["rule"]["context_dependent"]),
                "strict_with_nontrivial_u": sum(1 for item in strict_results if item["any_nontrivial_u"]),
            },
            "best_clean_rules": clean_results[:5],
            "best_strict_rules": strict_results[:5],
            "best_context_dependent_clean": next(
                (item for item in clean_results if item["rule"]["context_dependent"]),
                None,
            ),
            "best_context_dependent_strict": next(
                (item for item in strict_results if item["rule"]["context_dependent"]),
                None,
            ),
        }
        family_rows.append(family_row)

        if clean_results:
            _append_candidate(
                validation_candidates,
                candidate_seen,
                clean_results[0],
                f"family_best_clean_a{layer2_alt}_b{layer3_alt}",
            )
        if strict_results:
            _append_candidate(
                validation_candidates,
                candidate_seen,
                strict_results[0],
                f"family_best_strict_a{layer2_alt}_b{layer3_alt}",
            )
        context_clean = family_row["best_context_dependent_clean"]
        if context_clean is not None:
            _append_candidate(
                validation_candidates,
                candidate_seen,
                context_clean,
                f"family_best_context_clean_a{layer2_alt}_b{layer3_alt}",
            )
        context_strict = family_row["best_context_dependent_strict"]
        if context_strict is not None:
            _append_candidate(
                validation_candidates,
                candidate_seen,
                context_strict,
                f"family_best_context_strict_a{layer2_alt}_b{layer3_alt}",
            )

        if progress is not None and task_id is not None:
            progress.advance(task_id)

    if progress is not None:
        progress.stop()

    global_clean.sort(key=search_rank_key)
    global_strict.sort(key=strict_rank_key)
    unique_global_clean = _dedupe_results(global_clean, strict=False)
    unique_global_strict = _dedupe_results(global_strict, strict=True)
    for index, item in enumerate(unique_global_clean):
        _append_candidate(validation_candidates, candidate_seen, item, f"unique_clean_{index}")
    for index, item in enumerate(unique_global_strict):
        _append_candidate(validation_candidates, candidate_seen, item, f"unique_strict_{index}")

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": environment_block(),
        "pilot_m_values": list(m_values),
        "search_space": {
            "families": len(family_pairs),
            "strict_alternates": list(STRICT_ALTERNATES),
            "raw_rules_per_family": 32 * 32,
            "raw_total_rules": len(family_pairs) * 32 * 32,
            "contexts": ["phase_align", "00", "01", "10", "11"],
        },
        "family_summaries": family_rows,
        "global_counts": {
            "families_with_clean_survivors": sum(1 for row in family_rows if row["effective_counts"]["clean_all"] > 0),
            "families_with_strict_survivors": sum(1 for row in family_rows if row["effective_counts"]["strict_all"] > 0),
            "families_with_context_dependent_clean": sum(
                1 for row in family_rows if row["effective_counts"]["clean_context_dependent"] > 0
            ),
            "families_with_context_dependent_strict": sum(
                1 for row in family_rows if row["effective_counts"]["strict_context_dependent"] > 0
            ),
            "families_with_nontrivial_u": sum(
                1 for row in family_rows if row["effective_counts"]["strict_with_nontrivial_u"] > 0
            ),
            "family_aggregated_clean_survivor_count": len(global_clean),
            "family_aggregated_strict_survivor_count": len(global_strict),
            "unique_clean_survivor_count": len(unique_global_clean),
            "unique_strict_survivor_count": len(unique_global_strict),
            "unique_strict_with_nontrivial_u": sum(1 for item in unique_global_strict if item["any_nontrivial_u"]),
            "unique_context_dependent_clean": sum(1 for item in unique_global_clean if item["rule"]["context_dependent"]),
            "unique_context_dependent_strict": sum(1 for item in unique_global_strict if item["rule"]["context_dependent"]),
        },
        "best_clean_rules": unique_global_clean[:15],
        "best_strict_rules": unique_global_strict[:15],
        "recommended_next_step": (
            "If strict survivors remain U0-trivial, move to one-old-atom output grammars on top of the strict-friendly palette."
        ),
    }
    return {"summary": summary, "validation_candidates": validation_candidates}


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            "families_with_clean="
            f"{summary['global_counts']['families_with_clean_survivors']} "
            "families_with_strict="
            f"{summary['global_counts']['families_with_strict_survivors']} "
            "context_clean="
            f"{summary['global_counts']['unique_context_dependent_clean']} "
            "context_strict="
            f"{summary['global_counts']['unique_context_dependent_strict']} "
            "strict_nontrivial_u="
            f"{summary['global_counts']['unique_strict_with_nontrivial_u']}"
        ),
    ]
    for item in summary["best_strict_rules"][:5]:
        lines.append(
            "strict "
            f"a={item['rule']['layer2_alt']} b={item['rule']['layer3_alt']} "
            f"l2={item['rule']['layer2_table']} l3={item['rule']['layer3_table']} "
            f"context={item['rule']['context_dependent']} U={item['total_u_cycle_count']} "
            f"nontrivial={item['any_nontrivial_u']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search strict-friendly 5-context active layer-2/3 grammars.")
    parser.add_argument("--m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--out", type=Path, required=True, help="write search summary JSON here")
    parser.add_argument(
        "--candidates-out",
        type=Path,
        required=True,
        help="write validation-candidate JSON here",
    )
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    payload = run_search(m_values=parse_m_list(args.m_list), use_rich=not args.no_rich)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload["summary"], indent=2))
    args.candidates_out.parent.mkdir(parents=True, exist_ok=True)
    args.candidates_out.write_text(
        json.dumps(
            {
                "task_id": TASK_ID,
                "pilot_m_values": parse_m_list(args.m_list),
                "candidates": payload["validation_candidates"],
            },
            indent=2,
        )
    )
    _print_summary(payload["summary"], use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
