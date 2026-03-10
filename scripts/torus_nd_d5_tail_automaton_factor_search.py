#!/usr/bin/env python3
"""Search for automaton-derived one-bit factors matching the exact D5 tail partitions."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Sequence

from torus_nd_d5_tail_hypergraph_common import (
    TASK_ID,
    candidate_family_tokens,
    collect_nonzero_occurrences,
    environment_payload,
    family_name,
    feature_value_for_tokens,
    load_field_table,
    parse_m_list,
    serialize_feature_value,
)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover - optional dependency
    Console = None


def _optimal_targets(optimize_summary: Dict[str, object]) -> Dict[int, set[int]]:
    return {
        int(item["m"]): set(int(delta) for delta in item["hypergraph_optimum"]["optimal_delta_subset"])
        for item in optimize_summary["per_m"]
    }


def _evaluate_family(
    tokens: Sequence[str],
    occurrences_by_m: Dict[int, List[object]],
    target_by_m: Dict[int, set[int]],
) -> Dict[str, object]:
    global_labels = defaultdict(set)
    global_occurrence_count = Counter()
    global_deltas = defaultdict(set)
    global_examples = {}
    per_m = []

    for m, occurrences in occurrences_by_m.items():
        labels = defaultdict(set)
        occurrence_count = Counter()
        deltas = defaultdict(set)
        examples = {}
        target = target_by_m[m]
        for row in occurrences:
            value = feature_value_for_tokens(row, tokens)
            label = int(row.delta in target)
            labels[value].add(label)
            occurrence_count[value] += 1
            deltas[value].add(row.delta)
            global_labels[value].add(label)
            global_occurrence_count[value] += 1
            global_deltas[value].add((m, row.delta))
            examples.setdefault(
                (value, label),
                {
                    "m": m,
                    "delta": row.delta,
                    "coords": list(row.coords),
                    "step_index": row.step_index,
                    "state_name": row.state_name,
                    "prev_state_name": row.prev_state_name,
                    "next_state_name": row.next_state_name,
                    "entry0_state_name": row.entry0_state_name,
                    "entry1_state_name": row.entry1_state_name,
                    "entry2_state_name": row.entry2_state_name,
                },
            )
            global_examples.setdefault((value, label), examples[(value, label)])

        mixed_values = [value for value, label_set in labels.items() if len(label_set) > 1]
        mixed_rows = []
        for value in mixed_values[:8]:
            mixed_rows.append(
                {
                    "feature_value": serialize_feature_value(value),
                    "delta_values": sorted(deltas[value]),
                    "occurrence_count": occurrence_count[value],
                    "label_examples": {
                        str(label): examples[(value, label)]
                        for label in sorted(labels[value])
                    },
                }
            )
        per_m.append(
            {
                "m": m,
                "exact_fit": len(mixed_values) == 0,
                "distinct_value_count": len(labels),
                "mixed_value_count": len(mixed_values),
                "mixed_occurrence_count": sum(occurrence_count[value] for value in mixed_values),
                "mixed_value_examples": mixed_rows,
            }
        )

    global_mixed_values = [value for value, label_set in global_labels.items() if len(label_set) > 1]
    global_examples_rows = []
    for value in global_mixed_values[:12]:
        label_examples = {
            str(label): global_examples[(value, label)]
            for label in sorted(global_labels[value])
        }
        delta_pairs = sorted(global_deltas[value])
        global_examples_rows.append(
            {
                "feature_value": serialize_feature_value(value),
                "modulus_delta_pairs": [[m_value, delta] for m_value, delta in delta_pairs[:12]],
                "occurrence_count": global_occurrence_count[value],
                "label_examples": label_examples,
            }
        )

    per_m.sort(key=lambda row: row["m"])
    return {
        "family_name": family_name(tokens),
        "tokens": list(tokens),
        "token_count": len(tokens),
        "exact_fit_per_m": {str(row["m"]): row["exact_fit"] for row in per_m},
        "exact_fit_global": len(global_mixed_values) == 0,
        "distinct_value_count_global": len(global_labels),
        "mixed_value_count_global": len(global_mixed_values),
        "mixed_occurrence_count_global": sum(global_occurrence_count[value] for value in global_mixed_values),
        "per_m": per_m,
        "global_mixed_value_examples": global_examples_rows,
    }


def _top_family_rows(families: Sequence[Dict[str, object]], *, predicate) -> List[Dict[str, object]]:
    filtered = [item for item in families if predicate(item)]
    filtered.sort(
        key=lambda item: (
            not item["exact_fit_global"],
            item["mixed_occurrence_count_global"],
            item["mixed_value_count_global"],
            item["distinct_value_count_global"],
            item["token_count"],
            item["family_name"],
        )
    )
    return filtered[:10]


def run_factor_search(
    field_json: Path,
    optimize_summary: Dict[str, object],
    *,
    m_values: Sequence[int],
) -> Dict[str, object]:
    start = time.perf_counter()
    _, table = load_field_table(field_json)
    occurrences_by_m = {m: collect_nonzero_occurrences(table, m=m) for m in m_values}
    target_by_m = _optimal_targets(optimize_summary)

    families = []
    for tokens in candidate_family_tokens():
        families.append(_evaluate_family(tokens, occurrences_by_m, target_by_m))

    families.sort(
        key=lambda item: (
            not item["exact_fit_global"],
            item["mixed_occurrence_count_global"],
            item["mixed_value_count_global"],
            item["distinct_value_count_global"],
            item["token_count"],
            item["family_name"],
        )
    )

    exact_fits = [item for item in families if item["exact_fit_global"]]
    local_tokens = {"state_name", "prev_state_name", "next_state_name"}
    entry_tokens = {"entry0_state_name", "entry1_state_name", "entry2_state_name"}
    best_local = _top_family_rows(families, predicate=lambda item: set(item["tokens"]).issubset(local_tokens))
    best_entry = _top_family_rows(families, predicate=lambda item: bool(set(item["tokens"]) & entry_tokens))

    recommended = {
        "exact_one_bit_factor_found": len(exact_fits) > 0,
        "recommendation": (
            "No tested one-bit automaton factor on current/predecessor/successor/entry windows reproduces the exact optimal "
            "partitions uniformly on m=5,7,9,11,13. The next quotient should carry two tail bits: one oriented entry-class bit "
            "from the early return window and one local tail-context bit on the frozen branch."
            if not exact_fits
            else "Use the exact-fit family listed below as the next quotient-level one-bit factor."
        ),
        "best_local_family": best_local[0] if best_local else None,
        "best_entry_augmented_family": best_entry[0] if best_entry else None,
        "credible_two_bit_tail_grammar": {
            "bit_1_name": "tail_entry_orientation",
            "bit_1_source": "a cyclic-equivariant bit learned from the entry window (entry0, entry1, entry2)",
            "bit_2_name": "local_tail_context",
            "bit_2_source": "a cyclic-equivariant bit learned from predecessor/current/successor tail states",
        },
    }

    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": environment_payload(),
        "field_json": str(field_json),
        "m_values": list(m_values),
        "exact_optimal_targets": {
            str(m): sorted(target_by_m[m])
            for m in sorted(target_by_m)
        },
        "exact_fit_family_count": len(exact_fits),
        "exact_fit_families": exact_fits,
        "best_families_overall": families[:10],
        "best_local_families": best_local,
        "best_entry_augmented_families": best_entry,
        "recommended_next_schema": recommended,
        "tested_families": families,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        f"exact_fit_family_count: {summary['exact_fit_family_count']}",
    ]
    for item in summary["best_families_overall"][:5]:
        lines.append(
            f"{item['family_name']}: exact={item['exact_fit_global']} "
            f"mixed_occ={item['mixed_occurrence_count_global']} mixed_values={item['mixed_value_count_global']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search automaton-derived one-bit factors for the D5 residual tail.")
    parser.add_argument(
        "--field-json",
        type=Path,
        default=Path("artifacts/d5_theta_ab_phase_align_001/data/best_strict_collapse_field.json"),
        help="saved strict-collapse field JSON",
    )
    parser.add_argument("--optimize-json", type=Path, required=True, help="exact hypergraph optimization JSON")
    parser.add_argument("--m-list", default="5,7,9,11,13", help="comma-separated moduli")
    parser.add_argument("--out", type=Path, required=True, help="write factor-search JSON here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    optimize_summary = json.loads(args.optimize_json.read_text())
    summary = run_factor_search(args.field_json, optimize_summary, m_values=parse_m_list(args.m_list))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
