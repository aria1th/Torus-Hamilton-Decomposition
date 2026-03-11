#!/usr/bin/env python3
"""Exact three-flag eight-state layer-2 geometry search for d=5 witnesses."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from torus_nd_d5_alt4_three_flag_geometry_common import (
    ALT4_MODE_TABLES,
    CANONICAL_TWIST,
    CYCLE_BASELINE_TOTAL_U_CYCLES,
    EXTRA_FLAG_NAMES,
    KNOWN_ANTI_COMPRESSIVE_TOTALS,
    MIXED_BASELINE_TOTAL_U_CYCLES,
    Rule,
    dependency_class,
    environment_block,
    evaluate_rule_color0,
    load_cycle_baseline,
    load_mixed_baseline,
    overall_rank_key,
    parse_args_m_list,
    precompute_m,
    rule_compact_row,
    rule_rows_for_extra_flag,
    runtime_since,
)

try:
    from rich.console import Console
    from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeElapsedColumn
except ImportError:  # pragma: no cover
    Console = None
    Progress = None


def _counts(rows: Sequence[Dict[str, object]]) -> Dict[str, int]:
    clean_strict = [row for row in rows if row["clean_all"] and row["strict_all"]]
    return {
        "clean_survivor_count": sum(1 for row in rows if row["clean_all"]),
        "strict_survivor_count": len(clean_strict),
        "both_count": sum(1 for row in clean_strict if row["profile_kind"] == "both"),
        "cycle_only_count": sum(1 for row in clean_strict if row["profile_kind"] == "cycle_only"),
        "monodromy_only_count": sum(1 for row in clean_strict if row["profile_kind"] == "monodromy_only"),
        "mixed_profile_count": sum(1 for row in clean_strict if row["profile_kind"] == "mixed_profile"),
        "trivial_count": sum(1 for row in clean_strict if row["profile_kind"] == "trivial"),
        "improved_mixed_count": sum(1 for row in clean_strict if row["improves_mixed_baseline"]),
    }


def _best_rows(rows: Sequence[Dict[str, object]], kind: str, limit: int = 20) -> List[Dict[str, object]]:
    picked = [row for row in rows if row["clean_all"] and row["strict_all"] and row["profile_kind"] == kind]
    picked.sort(key=overall_rank_key)
    return picked[:limit]


def _dependency_counts(rows: Sequence[Dict[str, object]]) -> Dict[str, int]:
    counter = Counter()
    for row in rows:
        if row["clean_all"] and row["strict_all"]:
            counter[str(row["dependency_class"])] += 1
    return dict(sorted(counter.items()))


def _mode_count_histogram(rows: Sequence[Dict[str, object]]) -> Dict[str, int]:
    counter = Counter()
    for row in rows:
        if row["clean_all"] and row["strict_all"]:
            counter[str(row["distinct_mode_count"])] += 1
    return dict(sorted(counter.items()))


def _regime_histogram(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    counter = Counter()
    for row in rows:
        if row["clean_all"] and row["strict_all"]:
            key = (str(row["profile_kind"]), int(row["total_u_cycle_count"]))
            counter[key] += 1
    out = []
    for (kind, total_cycles), count in sorted(counter.items(), key=lambda item: (item[0][1], item[0][0])):
        out.append({"profile_kind": kind, "total_u_cycle_count": total_cycles, "count": count})
    return out


def _serialize_best(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    return list(rows)


def _candidate_payload(row: Dict[str, object]) -> Dict[str, object]:
    return {
        "rule": row["rule"],
        "search_metrics": {
            "dependency_class": row["dependency_class"],
            "active_bit_names": row["active_bit_names"],
            "distinct_mode_count": row["distinct_mode_count"],
            "latin_color0_all": row["latin_color0_all"],
            "clean_all": row["clean_all"],
            "strict_all": row["strict_all"],
            "profile_kind": row["profile_kind"],
            "total_u_cycle_count": row["total_u_cycle_count"],
            "max_cycle_length": row["max_cycle_length"],
            "total_nonzero_monodromies": row["total_nonzero_monodromies"],
            "improves_mixed_baseline": row["improves_mixed_baseline"],
            "per_m_cycle_counts": row["per_m_cycle_counts"],
            "per_m_cycle_lengths": row["per_m_cycle_lengths"],
            "per_m_monodromies": row["per_m_monodromies"],
        },
    }


def _append_candidate(
    target: List[Dict[str, object]],
    seen: set[Tuple[object, ...]],
    row: Dict[str, object],
    label: str,
) -> None:
    key = tuple(row["rule"]["effective_key"])
    if key in seen:
        return
    seen.add(key)
    payload = _candidate_payload(row)
    payload["label"] = label
    target.append(payload)


def _select_candidates(extra_flag_name: str, rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    clean_rows = [row for row in rows if row["clean_all"] and row["strict_all"]]
    clean_rows.sort(key=overall_rank_key)
    selected: List[Dict[str, object]] = []
    seen: set[Tuple[object, ...]] = set()

    for index, row in enumerate(clean_rows):
        if row["improves_mixed_baseline"]:
            _append_candidate(selected, seen, row, f"{extra_flag_name}:improved:{index}")

    for kind, limit in (("both", 16), ("cycle_only", 4), ("monodromy_only", 4)):
        picked = [row for row in clean_rows if row["profile_kind"] == kind]
        for index, row in enumerate(picked[:limit]):
            _append_candidate(selected, seen, row, f"{extra_flag_name}:{kind}:{index}")

    by_regime: Dict[int, Dict[str, object]] = {}
    for row in clean_rows:
        regime = int(row["total_u_cycle_count"])
        by_regime.setdefault(regime, row)
    for regime, row in sorted(by_regime.items()):
        _append_candidate(selected, seen, row, f"{extra_flag_name}:regime:{regime}")

    by_class: Dict[str, Dict[str, object]] = {}
    for row in clean_rows:
        dep = str(row["dependency_class"])
        by_class.setdefault(dep, row)
    for dep, row in sorted(by_class.items()):
        _append_candidate(selected, seen, row, f"{extra_flag_name}:class:{dep}")

    return selected


def _evaluate_extra_flag(
    *,
    extra_flag_name: str,
    pre_by_m: Dict[int, Dict[str, object]],
    m_values: Sequence[int],
    use_rich: bool,
) -> List[Dict[str, object]]:
    rules: Iterable[Rule] = rule_rows_for_extra_flag(extra_flag_name)
    rows: List[Dict[str, object]] = []
    progress = None
    task = None
    total = len(ALT4_MODE_TABLES) ** 8
    if use_rich and Progress is not None and Console is not None:
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
        )
        progress.start()
        task = progress.add_task(f"{extra_flag_name}", total=total)
    for rule in rules:
        row = rule_compact_row(evaluate_rule_color0(pre_by_m, rule, m_values=m_values))
        rows.append(row)
        if progress is not None and task is not None:
            progress.advance(task)
    if progress is not None:
        progress.stop()
    return rows


def run_search(
    *,
    m_values: Sequence[int],
    use_rich: bool,
    mixed_baseline_json: Path | None,
    cycle_baseline_json: Path | None,
) -> Dict[str, object]:
    start = time.perf_counter()
    pre_by_m = {m: precompute_m(m) for m in m_values}
    mixed_baseline = load_mixed_baseline(mixed_baseline_json)
    cycle_baseline = load_cycle_baseline(cycle_baseline_json)

    rows_by_flag: Dict[str, List[Dict[str, object]]] = {}
    candidates: List[Dict[str, object]] = []
    for extra_flag_name in EXTRA_FLAG_NAMES:
        rows = _evaluate_extra_flag(
            extra_flag_name=extra_flag_name,
            pre_by_m=pre_by_m,
            m_values=m_values,
            use_rich=use_rich,
        )
        rows_by_flag[extra_flag_name] = rows
        candidates.extend(_select_candidates(extra_flag_name, rows))

    summary_flags = {}
    for extra_flag_name, rows in rows_by_flag.items():
        counts = _counts(rows)
        summary_flags[extra_flag_name] = {
            "raw_rule_count": len(rows),
            "counts": counts,
            "dependency_class_counts": _dependency_counts(rows),
            "distinct_mode_count_histogram": _mode_count_histogram(rows),
            "regime_histogram": _regime_histogram(rows),
            "best_mixed_rules": _serialize_best(_best_rows(rows, "both")),
            "best_cycle_only_rules": _serialize_best(_best_rows(rows, "cycle_only")),
            "best_monodromy_only_rules": _serialize_best(_best_rows(rows, "monodromy_only")),
        }

    improved_total = sum(item["counts"]["improved_mixed_count"] for item in summary_flags.values())
    summary = {
        "task_id": "D5-ALT4-THREE-FLAG-GEOMETRY-013",
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "pilot_m_values": list(m_values),
        "search_method": {
            "type": "exact_color0_return_under_cyclic_equivariance",
            "note": (
                "The exhaustive pass computes exact color-0 Latin and first-return dynamics on the full torus. "
                "Full-color Latin is checked later on the reported frontier."
            ),
        },
        "baseline_comparison": {
            "mixed_012": mixed_baseline,
            "cycle_007": cycle_baseline,
            "mixed_baseline_total_u_cycle_count": MIXED_BASELINE_TOTAL_U_CYCLES,
            "cycle_baseline_total_u_cycle_count": CYCLE_BASELINE_TOTAL_U_CYCLES,
            "known_anti_compressive_totals": list(KNOWN_ANTI_COMPRESSIVE_TOTALS),
        },
        "canonical_twist": CANONICAL_TWIST,
        "pure_alt4_mode_pool": list(ALT4_MODE_TABLES.keys()),
        "extra_flag_summaries": summary_flags,
        "validation_candidate_count": len(candidates),
        "overall_improved_mixed_count": improved_total,
        "recommended_next_step": (
            "If neither named extra flag improves the baseline, move to an exact predecessor-tail local-signature bit on layer 2."
            if improved_total == 0
            else "Promote the improved mixed survivors to broader stability and layer-3 sensitivity checks."
        ),
    }
    return {"summary": summary, "rows_by_flag": rows_by_flag, "validation_candidates": candidates}


def _print_summary(summary: Mapping[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
    ]
    for extra_flag_name, block in summary["extra_flag_summaries"].items():
        counts = block["counts"]
        lines.append(
            (
                f"{extra_flag_name} clean={counts['clean_survivor_count']} "
                f"strict={counts['strict_survivor_count']} "
                f"both={counts['both_count']} improved={counts['improved_mixed_count']}"
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
    parser = argparse.ArgumentParser(description="Search the d=5 alt-4 three-flag geometry family.")
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--mixed-baseline-json", type=Path, help="override the mixed baseline validation summary")
    parser.add_argument("--cycle-baseline-json", type=Path, help="override the cycle baseline search summary")
    parser.add_argument("--out", type=Path, required=True, help="write search summary here")
    parser.add_argument("--rows-dir", type=Path, required=True, help="write compact per-flag row JSON files here")
    parser.add_argument("--candidates-out", type=Path, required=True, help="write validation candidate JSON here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    result = run_search(
        m_values=parse_args_m_list(args.pilot_m_list),
        use_rich=not args.no_rich and Progress is not None and Console is not None,
        mixed_baseline_json=args.mixed_baseline_json,
        cycle_baseline_json=args.cycle_baseline_json,
    )

    args.rows_dir.mkdir(parents=True, exist_ok=True)
    for extra_flag_name, rows in result["rows_by_flag"].items():
        rows_path = args.rows_dir / f"rule_rows_{extra_flag_name}.json"
        rows_path.write_text(json.dumps({"extra_flag_name": extra_flag_name, "rows": rows}, indent=2))
        result["summary"]["extra_flag_summaries"][extra_flag_name]["rows_file"] = str(rows_path)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result["summary"], indent=2))
    args.candidates_out.parent.mkdir(parents=True, exist_ok=True)
    args.candidates_out.write_text(json.dumps({"candidates": result["validation_candidates"]}, indent=2))
    _print_summary(result["summary"], use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
