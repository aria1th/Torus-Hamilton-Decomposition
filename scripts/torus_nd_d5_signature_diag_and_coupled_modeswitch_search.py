#!/usr/bin/env python3
"""Run the d=5 exact-signature diagnostic and coupled mode-switch search."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

from torus_nd_d5_signature_diag_and_coupled_modeswitch_common import (
    CYCLE_BASELINE_TOTAL_U_CYCLES,
    KNOWN_ANTI_COMPRESSIVE_TOTALS,
    MIXED_BASELINE_TOTAL_U_CYCLES,
    StageARule,
    StageBRule,
    environment_block,
    evaluate_stage_a_rule,
    evaluate_stage_b_rule,
    extract_sigma2_summary,
    load_cycle_baseline,
    load_mixed_baseline,
    local_word_diagnostic,
    overall_rank_key,
    parse_args_m_list,
    precompute_m,
    runtime_since,
    stage_a_rules,
    stage_b_rules,
)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover
    Console = None


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


def _serialize_rule_row(result: Mapping[str, object]) -> Dict[str, object]:
    return {
        "rule": result["rule"],
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


def _stage_summary(rows: Sequence[Dict[str, object]]) -> Dict[str, object]:
    return {
        "counts": _counts(rows),
        "regime_histogram": _regime_histogram(rows),
        "best_mixed_rules": [_serialize_rule_row(row) for row in _best_rows(rows, "both")],
        "best_cycle_only_rules": [_serialize_rule_row(row) for row in _best_rows(rows, "cycle_only")],
        "best_monodromy_only_rules": [_serialize_rule_row(row) for row in _best_rows(rows, "monodromy_only")],
    }


def _new_regimes(rows: Sequence[Dict[str, object]]) -> List[int]:
    known = {MIXED_BASELINE_TOTAL_U_CYCLES, *KNOWN_ANTI_COMPRESSIVE_TOTALS}
    found = {
        int(row["total_u_cycle_count"])
        for row in rows
        if row["clean_all"] and row["strict_all"]
    }
    return sorted(found - known)


def _stage_a_candidates(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    return [
        {
            "label": f"stage_a:{index}",
            "kind": "stage_a",
            "rule": row["rule"],
            "search_metrics": _serialize_rule_row(row),
        }
        for index, row in enumerate(rows)
    ]


def _stage_b_candidates(rows: Sequence[Dict[str, object]], stage_name: str) -> List[Dict[str, object]]:
    return [
        {
            "label": f"{stage_name}:{index}",
            "kind": "stage_b",
            "rule": row["rule"],
            "search_metrics": _serialize_rule_row(row),
        }
        for index, row in enumerate(rows)
        if row["clean_all"]
    ]


def _run_stage_a(pre_by_m: Mapping[int, Mapping[str, object]], m_values: Sequence[int]) -> List[Dict[str, object]]:
    rows = []
    for rule in stage_a_rules():
        rows.append(evaluate_stage_a_rule(pre_by_m, rule, m_values=m_values))
    return rows


def _run_stage_b(stage_name: str, pre_by_m: Mapping[int, Mapping[str, object]], m_values: Sequence[int]) -> List[Dict[str, object]]:
    rows = []
    for rule in stage_b_rules(stage_name):
        rows.append(evaluate_stage_b_rule(pre_by_m, rule, m_values=m_values))
    return rows


def run_search(
    *,
    m_values: Sequence[int],
    mixed_baseline_json: Path | None,
    cycle_baseline_json: Path | None,
) -> Dict[str, object]:
    start = time.perf_counter()
    pre_by_m = {m: precompute_m(m) for m in m_values}

    sigma2_summary = extract_sigma2_summary(m_values)
    sterility_local = local_word_diagnostic(m_values=m_values)
    stage_a_rows = _run_stage_a(pre_by_m, m_values)
    stage_a_summary = _stage_summary(stage_a_rows)
    stage_a_new_regimes = _new_regimes(stage_a_rows)

    stage_b1_rows = _run_stage_b("stage_b1", pre_by_m, m_values)
    stage_b1_summary = _stage_summary(stage_b1_rows)

    stage_b2_rows = []
    stage_b2_summary = None
    if stage_b1_summary["counts"]["improved_mixed_count"] == 0:
        stage_b2_rows = _run_stage_b("stage_b2", pre_by_m, m_values)
        stage_b2_summary = _stage_summary(stage_b2_rows)

    stage_b3_rows = []
    stage_b3_summary = None
    if stage_b2_summary is not None and stage_b2_summary["counts"]["improved_mixed_count"] == 0:
        stage_b3_rows = _run_stage_b("stage_b3", pre_by_m, m_values)
        stage_b3_summary = _stage_summary(stage_b3_rows)

    stage_a_sterile = (
        stage_a_summary["counts"]["improved_mixed_count"] == 0
        and not stage_a_new_regimes
    )

    candidates = _stage_a_candidates(stage_a_rows)
    candidates.extend(_stage_b_candidates(stage_b1_rows, "stage_b1"))
    candidates.extend(_stage_b_candidates(stage_b2_rows, "stage_b2"))
    candidates.extend(_stage_b_candidates(stage_b3_rows, "stage_b3"))

    summary = {
        "task_id": "D5-SIGNATURE-DIAG-AND-COUPLED-MODESWITCH-014",
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "pilot_m_values": list(m_values),
        "exact_bit_name": sigma2_summary["exact_bit_name"],
        "exact_bit_description": sigma2_summary["exact_bit_description"],
        "baseline_comparison": {
            "mixed_013": load_mixed_baseline(mixed_baseline_json),
            "cycle_007": load_cycle_baseline(cycle_baseline_json),
            "mixed_baseline_total_u_cycle_count": MIXED_BASELINE_TOTAL_U_CYCLES,
            "cycle_baseline_total_u_cycle_count": CYCLE_BASELINE_TOTAL_U_CYCLES,
            "known_anti_compressive_totals": list(KNOWN_ANTI_COMPRESSIVE_TOTALS),
        },
        "sigma2_summary": sigma2_summary,
        "sterility_local_diagnostic": sterility_local,
        "stage_a_summary": stage_a_summary,
        "stage_a_new_regimes": stage_a_new_regimes,
        "stage_a_sterility_verdict": {
            "pilot_return_sterile": stage_a_sterile,
            "statement": (
                "The exact predecessor-tail refinement adds no new pilot regime and no improved mixed witness in the fixed-twist layer-2-only branch."
                if stage_a_sterile
                else "The exact predecessor-tail refinement changes the pilot regime landscape or improves the mixed baseline."
            ),
        },
        "chosen_exact_bit_for_stage_b": "pred_sig1_phase_align",
        "stage_b1_summary": stage_b1_summary,
        "stage_b2_summary": stage_b2_summary,
        "stage_b3_summary": stage_b3_summary,
        "validation_candidate_count": len(candidates),
    }
    return {
        "summary": summary,
        "sigma2_summary": sigma2_summary,
        "sterility_local_diagnostic": sterility_local,
        "stage_a_rows": [_serialize_rule_row(row) for row in stage_a_rows],
        "stage_b_rows": {
            "stage_b1": [_serialize_rule_row(row) for row in stage_b1_rows],
            "stage_b2": [_serialize_rule_row(row) for row in stage_b2_rows],
            "stage_b3": [_serialize_rule_row(row) for row in stage_b3_rows],
        },
        "validation_candidates": candidates,
    }


def _print_summary(summary: Mapping[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            f"stage_a clean={summary['stage_a_summary']['counts']['clean_survivor_count']} "
            f"strict={summary['stage_a_summary']['counts']['strict_survivor_count']} "
            f"both={summary['stage_a_summary']['counts']['both_count']} "
            f"improved={summary['stage_a_summary']['counts']['improved_mixed_count']}"
        ),
        (
            f"stage_b1 clean={summary['stage_b1_summary']['counts']['clean_survivor_count']} "
            f"strict={summary['stage_b1_summary']['counts']['strict_survivor_count']} "
            f"both={summary['stage_b1_summary']['counts']['both_count']} "
            f"improved={summary['stage_b1_summary']['counts']['improved_mixed_count']}"
        ),
    ]
    if summary["stage_b2_summary"] is not None:
        lines.append(
            (
                f"stage_b2 clean={summary['stage_b2_summary']['counts']['clean_survivor_count']} "
                f"strict={summary['stage_b2_summary']['counts']['strict_survivor_count']} "
                f"both={summary['stage_b2_summary']['counts']['both_count']} "
                f"improved={summary['stage_b2_summary']['counts']['improved_mixed_count']}"
            )
        )
    if summary["stage_b3_summary"] is not None:
        lines.append(
            (
                f"stage_b3 clean={summary['stage_b3_summary']['counts']['clean_survivor_count']} "
                f"strict={summary['stage_b3_summary']['counts']['strict_survivor_count']} "
                f"both={summary['stage_b3_summary']['counts']['both_count']} "
                f"improved={summary['stage_b3_summary']['counts']['improved_mixed_count']}"
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
    parser = argparse.ArgumentParser(description="Run the d=5 exact-signature diagnostic and coupled mode-switch search.")
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--mixed-baseline-json", type=Path, help="override the mixed baseline validation summary")
    parser.add_argument("--cycle-baseline-json", type=Path, help="override the cycle baseline search summary")
    parser.add_argument("--out", type=Path, required=True, help="write main summary here")
    parser.add_argument("--sigma-out", type=Path, required=True, help="write exact sigma summary here")
    parser.add_argument("--diagnostic-out", type=Path, required=True, help="write local sterility diagnostic here")
    parser.add_argument("--stage-a-out", type=Path, required=True, help="write Stage A rule rows here")
    parser.add_argument("--stage-b-out", type=Path, required=True, help="write Stage B rule rows here")
    parser.add_argument("--candidates-out", type=Path, required=True, help="write validation candidates here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    result = run_search(
        m_values=parse_args_m_list(args.pilot_m_list),
        mixed_baseline_json=args.mixed_baseline_json,
        cycle_baseline_json=args.cycle_baseline_json,
    )

    for path in (args.out, args.sigma_out, args.diagnostic_out, args.stage_a_out, args.stage_b_out, args.candidates_out):
        path.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result["summary"], indent=2))
    args.sigma_out.write_text(json.dumps(result["sigma2_summary"], indent=2))
    args.diagnostic_out.write_text(json.dumps(result["sterility_local_diagnostic"], indent=2))
    args.stage_a_out.write_text(json.dumps({"rows": result["stage_a_rows"]}, indent=2))
    args.stage_b_out.write_text(json.dumps(result["stage_b_rows"], indent=2))
    args.candidates_out.write_text(json.dumps({"candidates": result["validation_candidates"]}, indent=2))
    _print_summary(result["summary"], use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
