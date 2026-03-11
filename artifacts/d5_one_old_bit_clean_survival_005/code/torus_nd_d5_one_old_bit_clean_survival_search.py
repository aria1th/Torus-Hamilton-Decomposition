#!/usr/bin/env python3
"""Exact one-old-bit clean-survival search for d=5 active layer-2/3 grammars."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Sequence

from torus_nd_d5_one_old_bit_clean_common import (
    CONTEXT_NAMES,
    OLD_BIT_NAMES,
    STRICT_ALTERNATES,
    TASK_ID,
    Rule,
    environment_block,
    evaluate_rule_from_known_latin,
    latin_surviving_layer_tables,
    parse_args_m_list,
    precompute_m,
    result_rank_key,
    runtime_since,
    strict_rank_key,
)

try:
    from rich.console import Console
    from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeElapsedColumn
except ImportError:  # pragma: no cover - optional dependency
    Console = None
    Progress = None


def _rule_key(item: Dict[str, object]) -> tuple:
    return (
        item["rule"]["old_bit_name"],
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
    rank = strict_rank_key if strict else result_rank_key
    best_by_key: Dict[tuple, Dict[str, object]] = {}
    for item in items:
        key = _rule_key(item)
        incumbent = best_by_key.get(key)
        if incumbent is None or rank(item) < rank(incumbent):
            best_by_key[key] = item
    out = list(best_by_key.values())
    out.sort(key=rank)
    return out


def _bit_redundancy_summary(old_bit_name: str, pre_by_m: Dict[int, Dict[str, object]]) -> Dict[str, object]:
    per_m = {}
    for m, pre in pre_by_m.items():
        layer2 = pre["layer2_patterns"]
        layer3 = pre["layer3_patterns"]
        per_m[str(m)] = {
            "layer2_context_count": len({int(value) for value in layer2.reshape(-1).tolist()}),
            "layer3_context_count": len({int(value) for value in layer3.reshape(-1).tolist()}),
        }
    return {"old_bit_name": old_bit_name, "contexts": list(CONTEXT_NAMES), "per_m": per_m}


def run_search(*, m_values: Sequence[int], use_rich: bool) -> Dict[str, object]:
    start = time.perf_counter()
    pre_by_bit = {old_bit: {m: precompute_m(m, old_bit) for m in m_values} for old_bit in OLD_BIT_NAMES}
    bit_summaries = [_bit_redundancy_summary(old_bit, pre_by_bit[old_bit]) for old_bit in OLD_BIT_NAMES]

    layer_latin_cache: Dict[str, Dict[int, Dict[int, List[Dict[str, object]]]]] = {
        old_bit: {2: {}, 3: {}} for old_bit in OLD_BIT_NAMES
    }
    one_layer_rows = []
    full_family_rows = []
    global_clean = []
    global_strict = []
    validation_candidates: List[Dict[str, object]] = []
    candidate_seen: set[tuple] = set()

    progress = None
    tasks = {}
    if use_rich and Progress is not None and Console is not None:
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
        )
        progress.start()
        tasks["one"] = progress.add_task("one-layer families", total=len(OLD_BIT_NAMES) * len(STRICT_ALTERNATES) * 2)
        tasks["full"] = progress.add_task("full families", total=len(OLD_BIT_NAMES) * len(STRICT_ALTERNATES) ** 2)

    for old_bit in OLD_BIT_NAMES:
        pre_by_m = pre_by_bit[old_bit]
        for active_layer in (2, 3):
            for alt_anchor in STRICT_ALTERNATES:
                family_start = time.perf_counter()
                latin_tables = latin_surviving_layer_tables(
                    pre_by_m,
                    active_layer=active_layer,
                    alt_anchor=alt_anchor,
                    m_values=m_values,
                )
                layer_latin_cache[old_bit][active_layer][alt_anchor] = latin_tables
                family_results = []
                for table in latin_tables:
                    rule = Rule.from_anchor_tables(
                        old_bit_name=old_bit,
                        layer2_alt=alt_anchor if active_layer == 2 else 2,
                        layer3_alt=alt_anchor if active_layer == 3 else 3,
                        layer2_table=table["anchors"] if active_layer == 2 else (2,) * len(CONTEXT_NAMES),
                        layer3_table=table["anchors"] if active_layer == 3 else (3,) * len(CONTEXT_NAMES),
                    )
                    result = evaluate_rule_from_known_latin(pre_by_m, rule, m_values=m_values)
                    result["raw_multiplicity"] = table["raw_multiplicity"]
                    family_results.append(result)

                clean_results = [item for item in family_results if item["clean_all"]]
                strict_results = [item for item in clean_results if item["strict_all"]]
                clean_results.sort(key=result_rank_key)
                strict_results.sort(key=strict_rank_key)
                global_clean.extend(clean_results)
                global_strict.extend(strict_results)
                row = {
                    "old_bit_name": old_bit,
                    "active_layer": active_layer,
                    "alt_anchor": alt_anchor,
                    "latin_table_count": len(latin_tables),
                    "clean_count": len(clean_results),
                    "strict_count": len(strict_results),
                    "context_dependent_clean": sum(1 for item in clean_results if item["rule"]["context_dependent"]),
                    "context_dependent_strict": sum(1 for item in strict_results if item["rule"]["context_dependent"]),
                    "strict_with_nontrivial_u": sum(1 for item in strict_results if item["any_nontrivial_u"]),
                    "runtime_sec": runtime_since(family_start),
                    "best_clean_rules": clean_results[:5],
                    "best_strict_rules": strict_results[:5],
                }
                one_layer_rows.append(row)
                if clean_results:
                    _append_candidate(
                        validation_candidates,
                        candidate_seen,
                        clean_results[0],
                        f"one_layer_{old_bit}_L{active_layer}_a{alt_anchor}",
                    )
                if progress is not None:
                    progress.advance(tasks["one"])

    for old_bit in OLD_BIT_NAMES:
        pre_by_m = pre_by_bit[old_bit]
        for layer2_alt in STRICT_ALTERNATES:
            layer2_tables = layer_latin_cache[old_bit][2][layer2_alt]
            for layer3_alt in STRICT_ALTERNATES:
                family_start = time.perf_counter()
                layer3_tables = layer_latin_cache[old_bit][3][layer3_alt]
                family_results = []
                for layer2_table in layer2_tables:
                    for layer3_table in layer3_tables:
                        rule = Rule.from_anchor_tables(
                            old_bit_name=old_bit,
                            layer2_alt=layer2_alt,
                            layer3_alt=layer3_alt,
                            layer2_table=layer2_table["anchors"],
                            layer3_table=layer3_table["anchors"],
                        )
                        result = evaluate_rule_from_known_latin(pre_by_m, rule, m_values=m_values)
                        result["raw_multiplicity"] = layer2_table["raw_multiplicity"] * layer3_table["raw_multiplicity"]
                        family_results.append(result)
                clean_results = [item for item in family_results if item["clean_all"]]
                strict_results = [item for item in clean_results if item["strict_all"]]
                clean_results.sort(key=result_rank_key)
                strict_results.sort(key=strict_rank_key)
                global_clean.extend(clean_results)
                global_strict.extend(strict_results)
                row = {
                    "old_bit_name": old_bit,
                    "layer2_alt": layer2_alt,
                    "layer3_alt": layer3_alt,
                    "layer2_latin_table_count": len(layer2_tables),
                    "layer3_latin_table_count": len(layer3_tables),
                    "full_candidate_count": len(layer2_tables) * len(layer3_tables),
                    "clean_count": len(clean_results),
                    "strict_count": len(strict_results),
                    "context_dependent_clean": sum(1 for item in clean_results if item["rule"]["context_dependent"]),
                    "context_dependent_strict": sum(1 for item in strict_results if item["rule"]["context_dependent"]),
                    "strict_with_nontrivial_u": sum(1 for item in strict_results if item["any_nontrivial_u"]),
                    "runtime_sec": runtime_since(family_start),
                    "best_clean_rules": clean_results[:5],
                    "best_strict_rules": strict_results[:5],
                }
                full_family_rows.append(row)
                if clean_results:
                    _append_candidate(
                        validation_candidates,
                        candidate_seen,
                        clean_results[0],
                        f"full_{old_bit}_a{layer2_alt}_b{layer3_alt}",
                    )
                if progress is not None:
                    progress.advance(tasks["full"])

    if progress is not None:
        progress.stop()

    unique_clean = _dedupe_results(global_clean, strict=False)
    unique_strict = _dedupe_results(global_strict, strict=True)
    for index, item in enumerate(unique_clean):
        _append_candidate(validation_candidates, candidate_seen, item, f"unique_clean_{index}")
    for index, item in enumerate(unique_strict):
        _append_candidate(validation_candidates, candidate_seen, item, f"unique_strict_{index}")

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "pilot_m_values": list(m_values),
        "old_bit_candidates_tested": list(OLD_BIT_NAMES),
        "bit_summaries": bit_summaries,
        "one_layer_summaries": one_layer_rows,
        "full_family_summaries": full_family_rows,
        "global_counts": {
            "one_layer_context_dependent_clean_families": sum(1 for row in one_layer_rows if row["context_dependent_clean"] > 0),
            "one_layer_context_dependent_strict_families": sum(1 for row in one_layer_rows if row["context_dependent_strict"] > 0),
            "full_context_dependent_clean_families": sum(1 for row in full_family_rows if row["context_dependent_clean"] > 0),
            "full_context_dependent_strict_families": sum(1 for row in full_family_rows if row["context_dependent_strict"] > 0),
            "family_aggregated_clean_survivor_count": len(global_clean),
            "family_aggregated_strict_survivor_count": len(global_strict),
            "unique_clean_survivor_count": len(unique_clean),
            "unique_strict_survivor_count": len(unique_strict),
            "unique_context_dependent_clean": sum(1 for item in unique_clean if item["rule"]["context_dependent"]),
            "unique_context_dependent_strict": sum(1 for item in unique_strict if item["rule"]["context_dependent"]),
            "unique_strict_with_nontrivial_u": sum(1 for item in unique_strict if item["any_nontrivial_u"]),
        },
        "best_clean_rules": unique_clean[:20],
        "best_strict_rules": unique_strict[:20],
        "recommended_next_step": (
            "If all one-old-bit families still collapse to constant clean survivors, move to predecessor-tail + old-bit hybrid contexts."
        ),
    }
    return {"summary": summary, "validation_candidates": validation_candidates}


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            f"one_layer_context_clean={summary['global_counts']['one_layer_context_dependent_clean_families']} "
            f"full_context_clean={summary['global_counts']['full_context_dependent_clean_families']} "
            f"unique_clean={summary['global_counts']['unique_clean_survivor_count']} "
            f"unique_context_clean={summary['global_counts']['unique_context_dependent_clean']} "
            f"unique_strict_nontrivial_u={summary['global_counts']['unique_strict_with_nontrivial_u']}"
        ),
    ]
    for item in summary["best_strict_rules"][:5]:
        lines.append(
            f"strict bit={item['rule']['old_bit_name']} a={item['rule']['layer2_alt']} b={item['rule']['layer3_alt']} "
            f"context={item['rule']['context_dependent']} U={item['total_u_cycle_count']} nontrivial={item['any_nontrivial_u']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search one-old-bit d=5 active layer-2/3 grammars for clean survivors.")
    parser.add_argument("--m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--out", type=Path, required=True, help="write search summary JSON here")
    parser.add_argument("--candidates-out", type=Path, required=True, help="write validation candidate JSON here")
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
