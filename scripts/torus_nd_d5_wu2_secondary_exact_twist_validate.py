#!/usr/bin/env python3
"""Validate candidates from the d=5 wu2-secondary exact-twist search."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Mapping, Sequence

from torus_nd_d5_wu2_secondary_exact_twist_common import (
    Rule,
    control_rule_from,
    environment_block,
    evaluate_rule,
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
        rule = Rule.from_payload(row["rule"])
        pilot_eval = evaluate_rule(pilot_pre, rule, m_values=pilot_m_values)
        rows.append(
            {
                "label": row["label"],
                "rule": row["rule"],
                "search_metrics": row["search_metrics"],
                "pilot_validation": pilot_eval,
                "pilot_matches_search_summary": _matches_search(pilot_eval, row["search_metrics"]),
            }
        )

    sorted_rows = sorted(rows, key=lambda row: overall_rank_key(row["pilot_validation"]))

    stability_rows = []
    if stability_m_values:
        stability_pre = _cache(stability_m_values)
        for row in sorted_rows[:stability_limit]:
            rule = Rule.from_payload(row["rule"])
            stability_eval = evaluate_rule(stability_pre, rule, m_values=stability_m_values)
            stability_rows.append(
                {
                    "label": row["label"],
                    "rule": row["rule"],
                    "stability_validation": stability_eval,
                }
            )

    control_rows = []
    for row in sorted_rows[:control_limit]:
        rule = Rule.from_payload(row["rule"])
        control_rule = control_rule_from(rule)
        control_eval = evaluate_rule(pilot_pre, control_rule, m_values=pilot_m_values)
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
        "task_id": "D5-WU2-SECONDARY-EXACT-TWIST-015",
        "runtime_sec": time.perf_counter() - start,
        "environment": environment_block(),
        "pilot_m_values": list(pilot_m_values),
        "stability_m_values": list(stability_m_values),
        "candidate_count": len(rows),
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
            f"pilot_full_color_latin={summary['all_candidates_full_color_latin']} "
            f"matches_search={summary['all_candidates_match_search_summary']} "
            f"stability_checks={len(summary['stability_spot_checks'])} "
            f"control_checks={len(summary['control_twist_checks'])}"
        ),
    ]
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the d=5 wu2-secondary exact-twist search.")
    parser.add_argument("--candidates-json", type=Path, required=True, help="candidate JSON from the search step")
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--stability-m-list", default="11,13", help="comma-separated stability spot-check moduli")
    parser.add_argument("--stability-limit", type=int, default=20, help="how many top candidates to stability-check")
    parser.add_argument("--control-limit", type=int, default=20, help="how many top candidates to control-check")
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
