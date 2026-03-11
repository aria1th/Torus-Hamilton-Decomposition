#!/usr/bin/env python3
"""Validate reported d=5 strict-palette context witnesses with full-color checks."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Sequence

from torus_nd_d5_strict_palette_context_common import (
    TASK_ID,
    environment_block,
    evaluate_rule_validation,
    parse_m_list,
    precompute_m,
    Rule,
)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover - optional dependency
    Console = None


def run_validation(
    *,
    candidates_json: Path,
    pilot_m_values: Sequence[int],
    extra_m_values: Sequence[int],
) -> Dict[str, object]:
    start = time.perf_counter()
    payload = json.loads(candidates_json.read_text())
    candidate_rows = payload["candidates"]
    all_m_values = list(dict.fromkeys([*pilot_m_values, *extra_m_values]))
    pre_by_m = {m: precompute_m(m) for m in all_m_values}

    rows = []
    for row in candidate_rows:
        rule = Rule.from_payload(row["rule"])
        pilot_eval = evaluate_rule_validation(pre_by_m, rule, m_values=pilot_m_values)
        extra_eval = evaluate_rule_validation(pre_by_m, rule, m_values=extra_m_values) if extra_m_values else None
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
                "extra_validation": extra_eval,
                "pilot_matches_search_summary": matches_search,
            }
        )

    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": environment_block(),
        "pilot_m_values": list(pilot_m_values),
        "extra_m_values": list(extra_m_values),
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
            f"{row['label']} clean={row['pilot_validation']['clean_all']} "
            f"strict={row['pilot_validation']['strict_all']} "
            f"context={row['rule']['context_dependent']} nontrivial={row['pilot_validation']['any_nontrivial_u']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate reported strict-palette context witnesses with all-color checks.")
    parser.add_argument("--candidates-json", type=Path, required=True, help="candidate JSON from the search step")
    parser.add_argument("--m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--extra-m-list", default="", help="optional comma-separated extra moduli")
    parser.add_argument("--out", type=Path, required=True, help="write validation summary here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    summary = run_validation(
        candidates_json=args.candidates_json,
        pilot_m_values=parse_m_list(args.m_list),
        extra_m_values=parse_m_list(args.extra_m_list),
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
