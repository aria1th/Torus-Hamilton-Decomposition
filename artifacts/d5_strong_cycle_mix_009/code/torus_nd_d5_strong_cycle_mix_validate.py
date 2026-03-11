#!/usr/bin/env python3
"""Validate reported survivors from the strong mixed d=5 graft search."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Sequence

from torus_nd_d5_strong_cycle_mix_common import (
    TASK_ID,
    Rule,
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


def _pair_cache(rows, m_values):
    pair_set = set()
    for row in rows:
        rule = Rule.from_payload(row["rule"])
        pair_set.add((rule.layer2_bit_name, rule.layer3_bit_name))
    return {pair: {m: precompute_m(m, pair[0], pair[1]) for m in m_values} for pair in pair_set}


def run_validation(
    *,
    candidates_json: Path,
    pilot_m_values: Sequence[int],
    stability_m_values: Sequence[int],
    stability_limit: int,
) -> Dict[str, object]:
    start = time.perf_counter()
    payload = json.loads(candidates_json.read_text())
    candidate_rows = payload["candidates"]
    pilot_pre = _pair_cache(candidate_rows, pilot_m_values)

    rows = []
    for row in candidate_rows:
        rule = Rule.from_payload(row["rule"])
        pair = (rule.layer2_bit_name, rule.layer3_bit_name)
        pilot_eval = evaluate_rule(pilot_pre[pair], rule, m_values=pilot_m_values)
        matches_search = (
            pilot_eval["latin_all"] == row["search_metrics"]["latin_all"]
            and pilot_eval["clean_all"] == row["search_metrics"]["clean_all"]
            and pilot_eval["strict_all"] == row["search_metrics"]["strict_all"]
            and pilot_eval["overall_kind"] == row["search_metrics"]["overall_kind"]
            and pilot_eval["max_cycle_length"] == row["search_metrics"]["max_cycle_length"]
            and pilot_eval["total_nonzero_monodromies"] == row["search_metrics"]["total_nonzero_monodromies"]
            and pilot_eval["improves_mixed_baseline"] == row["search_metrics"]["improves_mixed_baseline"]
        )
        rows.append(
            {
                "label": row["label"],
                "rule": row["rule"],
                "search_metrics": row["search_metrics"],
                "pilot_validation": pilot_eval,
                "pilot_matches_search_summary": matches_search,
            }
        )

    stability_rows = []
    if stability_m_values:
        sorted_rows = sorted(rows, key=lambda item: overall_rank_key(item["pilot_validation"]))
        stability_targets = sorted_rows[:stability_limit]
        stability_pre = _pair_cache(stability_targets, stability_m_values)
        for row in stability_targets:
            rule = Rule.from_payload(row["rule"])
            pair = (rule.layer2_bit_name, rule.layer3_bit_name)
            stability_eval = evaluate_rule(stability_pre[pair], rule, m_values=stability_m_values)
            stability_rows.append(
                {
                    "label": row["label"],
                    "rule": row["rule"],
                    "stability_validation": stability_eval,
                }
            )

    return {
        "task_id": TASK_ID,
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
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            f"candidates={summary['candidate_count']} "
            f"pilot_full_color_latin={summary['all_candidates_full_color_latin']} "
            f"matches_search={summary['all_candidates_match_search_summary']} "
            f"stability_checks={len(summary['stability_spot_checks'])}"
        ),
    ]
    for row in summary["candidates"][:8]:
        r = row["rule"]
        v = row["pilot_validation"]
        lines.append(
            f"{row['label']} stage={r['stage']} seed={r['layer2_bit_name']}:{r['layer2_orientation']} "
            f"l3={r['layer3_bit_name']} {r['predecessor_flag_name']} "
            f"({r['layer3_mode_p0']['name']},{r['layer3_mode_p1']['name']}) "
            f"kind={v['overall_kind']} improve={v['improves_mixed_baseline']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the d=5 strong mixed graft family.")
    parser.add_argument("--candidates-json", type=Path, required=True, help="candidate JSON from the search step")
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--stability-m-list", default="11,13", help="comma-separated stability spot-check moduli")
    parser.add_argument("--stability-limit", type=int, default=12, help="how many top candidates to stability-check")
    parser.add_argument("--out", type=Path, required=True, help="write validation summary here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    summary = run_validation(
        candidates_json=args.candidates_json,
        pilot_m_values=parse_args_m_list(args.pilot_m_list),
        stability_m_values=parse_args_m_list(args.stability_m_list),
        stability_limit=args.stability_limit,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
