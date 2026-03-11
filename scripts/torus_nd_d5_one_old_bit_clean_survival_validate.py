#!/usr/bin/env python3
"""Validate reported one-old-bit d=5 clean-survival witnesses on the full torus."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Sequence

from torus_nd_d5_one_old_bit_clean_common import (
    TASK_ID,
    Rule,
    environment_block,
    evaluate_rule_validation,
    parse_args_m_list,
    precompute_m,
)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover - optional dependency
    Console = None


def run_validation(*, candidates_json: Path, m_values: Sequence[int]) -> Dict[str, object]:
    start = time.perf_counter()
    payload = json.loads(candidates_json.read_text())
    candidate_rows = payload["candidates"]
    pre_by_bit: Dict[str, Dict[int, Dict[str, object]]] = {}
    rows = []
    for row in candidate_rows:
        rule = Rule.from_payload(row["rule"])
        if rule.old_bit_name not in pre_by_bit:
            pre_by_bit[rule.old_bit_name] = {m: precompute_m(m, rule.old_bit_name) for m in m_values}
        pilot_eval = evaluate_rule_validation(pre_by_bit[rule.old_bit_name], rule, m_values=m_values)
        matches_search = (
            pilot_eval["clean_all"] == row["search_metrics"]["clean_all"]
            and pilot_eval["strict_all"] == row["search_metrics"]["strict_all"]
            and pilot_eval["any_nontrivial_u"] == row["search_metrics"]["any_nontrivial_u"]
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
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": environment_block(),
        "pilot_m_values": list(m_values),
        "candidate_count": len(rows),
        "all_candidates_match_search_summary": all(row["pilot_matches_search_summary"] for row in rows),
        "all_pilot_candidates_full_color_latin": all(row["pilot_validation"]["latin_all"] for row in rows),
        "any_pilot_candidate_nontrivial_u": any(row["pilot_validation"]["any_nontrivial_u"] for row in rows),
        "candidates": rows,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            f"candidates={summary['candidate_count']} "
            f"pilot_full_color_latin={summary['all_pilot_candidates_full_color_latin']} "
            f"matches_search={summary['all_candidates_match_search_summary']} "
            f"any_nontrivial_u={summary['any_pilot_candidate_nontrivial_u']}"
        ),
    ]
    for row in summary["candidates"][:5]:
        lines.append(
            f"{row['label']} bit={row['rule']['old_bit_name']} "
            f"clean={row['pilot_validation']['clean_all']} "
            f"strict={row['pilot_validation']['strict_all']} "
            f"context={row['rule']['context_dependent']} "
            f"nontrivial={row['pilot_validation']['any_nontrivial_u']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate one-old-bit clean-survival witnesses on the full torus.")
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
