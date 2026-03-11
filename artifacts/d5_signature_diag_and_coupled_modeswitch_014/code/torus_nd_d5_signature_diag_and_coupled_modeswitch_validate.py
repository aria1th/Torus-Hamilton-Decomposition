#!/usr/bin/env python3
"""Validate reported candidates for the d=5 exact-signature diagnostic and coupled mode-switch search."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Mapping, Sequence

from torus_nd_d5_signature_diag_and_coupled_modeswitch_common import (
    StageARule,
    StageBRule,
    control_rule_from,
    environment_block,
    evaluate_stage_a_rule,
    evaluate_stage_b_rule,
    overall_rank_key,
    parse_args_m_list,
    precompute_m,
)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover
    Console = None


def _cache(m_values: Sequence[int]) -> Dict[int, Dict[str, object]]:
    return {m: precompute_m(m) for m in m_values}


def _eval_from_candidate(pre_by_m: Mapping[int, Mapping[str, object]], row: Mapping[str, object], m_values: Sequence[int]) -> Dict[str, object]:
    if row["kind"] == "stage_a":
        rule = StageARule.from_payload(row["rule"])
        return evaluate_stage_a_rule(pre_by_m, rule, m_values=m_values)
    rule = StageBRule.from_payload(row["rule"])
    return evaluate_stage_b_rule(pre_by_m, rule, m_values=m_values)


def _matches_search(pilot_eval: Mapping[str, object], search_metrics: Mapping[str, object]) -> bool:
    return (
        pilot_eval["latin_all"] == search_metrics["latin_all"]
        and pilot_eval["clean_all"] == search_metrics["clean_all"]
        and pilot_eval["strict_all"] == search_metrics["strict_all"]
        and pilot_eval["profile_kind"] == search_metrics["profile_kind"]
        and pilot_eval["total_u_cycle_count"] == search_metrics["total_u_cycle_count"]
        and pilot_eval["max_cycle_length"] == search_metrics["max_cycle_length"]
        and pilot_eval["total_nonzero_monodromies"] == search_metrics["total_nonzero_monodromies"]
        and pilot_eval["improves_mixed_baseline"] == search_metrics["improves_mixed_baseline"]
        and pilot_eval["per_m"] == search_metrics["per_m"]
    )


def run_validation(
    *,
    candidates_json: Path,
    pilot_m_values: Sequence[int],
    stability_m_values: Sequence[int],
    stability_limit: int,
    control_limit: int,
) -> Dict[str, object]:
    start = time.perf_counter()
    payload = json.loads(candidates_json.read_text())
    candidate_rows = payload["candidates"]
    pilot_pre = _cache(pilot_m_values)

    rows = []
    for row in candidate_rows:
        pilot_eval = _eval_from_candidate(pilot_pre, row, pilot_m_values)
        rows.append(
            {
                "label": row["label"],
                "kind": row["kind"],
                "rule": row["rule"],
                "search_metrics": row["search_metrics"],
                "pilot_validation": pilot_eval,
                "pilot_matches_search_summary": _matches_search(pilot_eval, row["search_metrics"]),
            }
        )

    stage_b_rows = [row for row in rows if row["kind"] == "stage_b"]
    stage_b_rows.sort(key=lambda row: overall_rank_key(row["pilot_validation"]))

    stability_rows = []
    if stability_m_values:
        stability_pre = _cache(stability_m_values)
        for row in stage_b_rows[:stability_limit]:
            rule = StageBRule.from_payload(row["rule"])
            stability_eval = evaluate_stage_b_rule(stability_pre, rule, m_values=stability_m_values)
            stability_rows.append(
                {
                    "label": row["label"],
                    "kind": row["kind"],
                    "rule": row["rule"],
                    "stability_validation": stability_eval,
                }
            )

    control_rows = []
    for row in stage_b_rows[:control_limit]:
        rule = StageBRule.from_payload(row["rule"])
        control_rule = control_rule_from(rule)
        control_eval = evaluate_stage_b_rule(pilot_pre, control_rule, m_values=pilot_m_values)
        control_rows.append(
            {
                "label": row["label"],
                "canonical_rule": row["rule"],
                "control_rule": control_rule.payload(),
                "canonical_validation": row["pilot_validation"],
                "control_validation": control_eval,
                "same_cycle_signature": row["pilot_validation"]["cycle_signature"] == control_eval["cycle_signature"],
            }
        )

    return {
        "task_id": "D5-SIGNATURE-DIAG-AND-COUPLED-MODESWITCH-014",
        "runtime_sec": time.perf_counter() - start,
        "environment": environment_block(),
        "pilot_m_values": list(pilot_m_values),
        "stability_m_values": list(stability_m_values),
        "candidate_count": len(rows),
        "stage_b_candidate_count": len(stage_b_rows),
        "all_candidates_match_search_summary": all(row["pilot_matches_search_summary"] for row in rows),
        "all_candidates_full_color_latin": all(row["pilot_validation"]["latin_all"] for row in rows),
        "all_clean_candidates_strict": all(
            (not row["pilot_validation"]["clean_all"]) or row["pilot_validation"]["strict_all"]
            for row in rows
        ),
        "candidates": rows,
        "stability_spot_checks": stability_rows,
        "control_twist_checks": control_rows,
    }


def _print_summary(summary: Mapping[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            f"candidates={summary['candidate_count']} "
            f"stage_b_candidates={summary['stage_b_candidate_count']} "
            f"pilot_full_color_latin={summary['all_candidates_full_color_latin']} "
            f"matches_search={summary['all_candidates_match_search_summary']} "
            f"stability_checks={len(summary['stability_spot_checks'])} "
            f"control_checks={len(summary['control_twist_checks'])}"
        ),
    ]
    for row in summary["candidates"][:8]:
        lines.append(
            f"{row['label']} kind={row['kind']} profile={row['pilot_validation']['profile_kind']} "
            f"improve={row['pilot_validation']['improves_mixed_baseline']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the d=5 exact-signature diagnostic and coupled mode-switch search.")
    parser.add_argument("--candidates-json", type=Path, required=True, help="candidate JSON from the search step")
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--stability-m-list", default="11,13", help="comma-separated stability spot-check moduli")
    parser.add_argument("--stability-limit", type=int, default=20, help="how many top stage-B candidates to stability-check")
    parser.add_argument("--control-limit", type=int, default=20, help="how many top stage-B candidates to check under control twist")
    parser.add_argument("--out", type=Path, required=True, help="write validation summary here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    summary = run_validation(
        candidates_json=args.candidates_json,
        pilot_m_values=parse_args_m_list(args.pilot_m_list),
        stability_m_values=parse_args_m_list(args.stability_m_list),
        stability_limit=args.stability_limit,
        control_limit=args.control_limit,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
