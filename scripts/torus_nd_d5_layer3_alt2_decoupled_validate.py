#!/usr/bin/env python3
"""Validate surviving rules from the decoupled two-old-bit family with layer-3 alt {0,2}."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Sequence

from torus_nd_d5_layer3_alt2_decoupled_common import (
    TASK_ID,
    Rule,
    environment_block,
    evaluate_rule,
    parse_args_m_list,
    precompute_m,
)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover
    Console = None


def run_validation(*, candidates_json: Path, m_values: Sequence[int]) -> Dict[str, object]:
    start = time.perf_counter()
    payload = json.loads(candidates_json.read_text())
    candidate_rows = payload["candidates"]
    pre_by_pair: Dict[tuple, Dict[int, Dict[str, object]]] = {}
    rows = []
    for row in candidate_rows:
        rule = Rule.from_payload(row["rule"])
        pair = (rule.layer2_bit_name, rule.layer3_bit_name)
        if pair not in pre_by_pair:
            pre_by_pair[pair] = {m: precompute_m(m, *pair) for m in m_values}
        eval_row = evaluate_rule(pre_by_pair[pair], rule, m_values=m_values)
        matches_search = (
            eval_row["clean_all"] == row["search_metrics"]["clean_all"]
            and eval_row["strict_all"] == row["search_metrics"]["strict_all"]
            and eval_row["overall_kind"] == row["search_metrics"]["overall_kind"]
            and eval_row["total_nonzero_monodromies"] == row["search_metrics"]["total_nonzero_monodromies"]
            and eval_row["max_cycle_length"] == row["search_metrics"]["max_cycle_length"]
        )
        rows.append(
            {
                "label": row["label"],
                "rule": row["rule"],
                "search_metrics": row["search_metrics"],
                "pilot_validation": eval_row,
                "pilot_matches_search_summary": matches_search,
            }
        )
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": environment_block(),
        "pilot_m_values": list(m_values),
        "candidate_count": len(rows),
        "all_candidates_match_search_summary": all(row["pilot_matches_search_summary"] for row in rows),
        "all_pilot_candidates_full_color_latin": all(row["pilot_validation"]["latin_all"] for row in rows),
        "candidates": rows,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            f"candidates={summary['candidate_count']} "
            f"pilot_full_color_latin={summary['all_pilot_candidates_full_color_latin']} "
            f"matches_search={summary['all_candidates_match_search_summary']}"
        ),
    ]
    for row in summary["candidates"][:5]:
        lines.append(
            f"{row['label']} s2={row['rule']['layer2_bit_name']} s3={row['rule']['layer3_bit_name']} "
            f"l3_alt={row['rule']['layer3_alt']} kind={row['pilot_validation']['overall_kind']} strict={row['pilot_validation']['strict_all']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the decoupled two-old-bit d=5 family with layer-3 alt {0,2}.")
    parser.add_argument("--candidates-json", type=Path, required=True, help="candidate JSON from the search step")
    parser.add_argument("--m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--out", type=Path, required=True, help="write validation summary here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    summary = run_validation(candidates_json=args.candidates_json, m_values=parse_args_m_list(args.m_list))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
