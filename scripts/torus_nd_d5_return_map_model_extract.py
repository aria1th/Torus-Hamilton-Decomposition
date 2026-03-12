#!/usr/bin/env python3
"""Extract return-map models for the current d=5 witness set."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

from torus_nd_d5_return_map_model_common import (
    DEFAULT_M_VALUES,
    PILOT_M_VALUES,
    STABILITY_M_VALUES,
    TASK_ID,
    PreparedWitness,
    classify_grouped_model,
    deterministic_quotient_R,
    deterministic_quotient_U,
    environment_block,
    extract_first_return_table,
    extract_grouped_return,
    fit_affine_map,
    fit_affine_scalar,
    fit_single_slice,
    load_witness_specs,
    parse_args_m_list,
    prepare_witness,
    runtime_since,
    search_linear_forms,
)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover
    Console = None


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _r_state_list(table: Mapping[str, object]) -> List[Tuple[int, int, int]]:
    return [(row["q"], row["w"], row["u"]) for row in table["states"].values() if row["clean_state"]]


def _u_state_list(table: Mapping[str, object]) -> List[Tuple[int, int]]:
    return [(row["w"], row["u"]) for row in table["states"].values()]


def _analyse_one(prepared: PreparedWitness, m: int, *, out_dir: Path) -> Dict[str, object]:
    pre = prepared.pre_by_m[m]
    nexts0 = prepared.nexts0_by_m[m]
    dir_row = prepared.dir_by_m[m]

    first_return = extract_first_return_table(pre, nexts0, dir_row)
    grouped_return = extract_grouped_return(first_return)
    quotient_r = deterministic_quotient_R(first_return)
    quotient_u = deterministic_quotient_U(grouped_return)

    first_path = out_dir / f"{prepared.spec.name}_m{m}_first_return.json"
    grouped_path = out_dir / f"{prepared.spec.name}_m{m}_grouped_return.json"
    quotient_r_path = out_dir / f"{prepared.spec.name}_m{m}_quotient_R.json"
    quotient_u_path = out_dir / f"{prepared.spec.name}_m{m}_quotient_U.json"
    _write_json(first_path, first_return)
    _write_json(grouped_path, grouped_return)
    _write_json(quotient_r_path, quotient_r)
    _write_json(quotient_u_path, quotient_u)

    r_increment_models = {}
    r_affine = {}
    if first_return["clean_frame"] and first_return["strict_clock"]:
        states_r = _r_state_list(first_return)
        next_r = {
            (row["q"], row["w"], row["u"]): tuple(int(value) for value in row["next_state"])
            for row in first_return["states"].values()
            if row["clean_state"]
        }
        dv_r = {
            (row["q"], row["w"], row["u"]): int(row["dv"])
            for row in first_return["states"].values()
            if row["clean_state"]
        }
        increments = {
            state: (
                (next_r[state][0] - state[0]) % m,
                (next_r[state][1] - state[1]) % m,
                (next_r[state][2] - state[2]) % m,
            )
            for state in states_r
        }
        r_increment_models = {
            "dq": fit_single_slice(states_r, {state: increments[state][0] for state in states_r}, m),
            "dw": fit_single_slice(states_r, {state: increments[state][1] for state in states_r}, m),
            "du": fit_single_slice(states_r, {state: increments[state][2] for state in states_r}, m),
            "dv": fit_single_slice(states_r, dv_r, m),
        }
        r_affine = {
            "next_state": fit_affine_map(states_r, next_r, m),
            "dv": fit_affine_scalar(states_r, dv_r, m),
        }

    u_affine = {}
    linear_forms = {}
    grouped_model = {}
    if grouped_return.get("available", False):
        states_u = _u_state_list(grouped_return)
        next_u = {
            (row["w"], row["u"]): tuple(int(value) for value in row["next_state"])
            for row in grouped_return["states"].values()
        }
        phi_u = {
            (row["w"], row["u"]): int(row["phi"])
            for row in grouped_return["states"].values()
        }
        u_affine = {
            "next_state": fit_affine_map(states_u, next_u, m),
            "phi": fit_affine_scalar(states_u, phi_u, m),
        }
        linear_forms = search_linear_forms(states_u, next_u, m)
        grouped_model = classify_grouped_model(grouped_return, u_affine["next_state"], linear_forms, m)
    else:
        states_u = []
        next_u = {}
        phi_u = {}

    return {
        "witness": {
            "name": prepared.spec.name,
            "role": prepared.spec.role,
            "family": prepared.spec.family,
            "source": prepared.spec.source,
            "rule": prepared.spec.rule_payload,
        },
        "m": m,
        "first_return_summary": {
            "clean_frame": first_return["clean_frame"],
            "strict_clock": first_return["strict_clock"],
            "state_count": first_return["state_count"],
            "low_layer_word_histogram": first_return["low_layer_word_histogram"][:12],
            "full_word_histogram": first_return["full_word_histogram"][:12],
            "file": str(first_path),
        },
        "grouped_return_summary": {
            "available": grouped_return.get("available", False),
            "state_count": grouped_return.get("state_count", 0),
            "cycle_count": grouped_return.get("cycle_count"),
            "cycle_lengths": grouped_return.get("cycle_lengths"),
            "cycle_monodromies": grouped_return.get("cycle_monodromies"),
            "file": str(grouped_path),
        },
        "quotient_R": {**quotient_r, "file": str(quotient_r_path)},
        "quotient_U": {**quotient_u, "file": str(quotient_u_path)},
        "R_models": {
            "increment_models": r_increment_models,
            "affine_models": r_affine,
        },
        "U_models": {
            "affine_models": u_affine,
            "linear_forms": linear_forms,
            "grouped_model_classification": grouped_model,
        },
    }


def run_extraction(*, m_values: Sequence[int], out_dir: Path) -> Dict[str, object]:
    start = __import__("time").perf_counter()
    specs = load_witness_specs()
    prepared = [prepare_witness(spec, m_values) for spec in specs]

    by_witness = []
    for item in prepared:
        witness_reports = []
        for m in m_values:
            witness_reports.append(_analyse_one(item, m, out_dir=out_dir / "tables"))
        by_witness.append(
            {
                "witness": {
                    "name": item.spec.name,
                    "role": item.spec.role,
                    "family": item.spec.family,
                    "source": item.spec.source,
                    "rule": item.spec.rule_payload,
                },
                "reports_by_m": witness_reports,
            }
        )

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "pilot_m_values": list(PILOT_M_VALUES),
        "stability_m_values": list(STABILITY_M_VALUES),
        "analysed_m_values": list(m_values),
        "witnesses": by_witness,
    }
    return summary


def _print_summary(summary: Mapping[str, object], *, use_rich: bool) -> None:
    lines = [f"task_id: {summary['task_id']}", f"runtime_sec: {summary['runtime_sec']:.3f}"]
    for witness_block in summary["witnesses"]:
        witness_name = witness_block["witness"]["name"]
        short = []
        for report in witness_block["reports_by_m"]:
            grouped = report["U_models"]["grouped_model_classification"]["kind"]
            short.append(
                f"m={report['m']}:Rclean={report['first_return_summary']['clean_frame']} "
                f"Ucycles={report['grouped_return_summary'].get('cycle_count')} "
                f"model={grouped}"
            )
        lines.append(f"{witness_name}: " + " | ".join(short))
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract return-map models for the current d=5 witness set.")
    parser.add_argument("--m-list", default="5,7,9,11,13", help="comma-separated moduli to analyze")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="write main summary JSON here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    summary = run_extraction(m_values=parse_args_m_list(args.m_list), out_dir=args.out_dir)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
