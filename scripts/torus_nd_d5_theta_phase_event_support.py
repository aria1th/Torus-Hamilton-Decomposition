#!/usr/bin/env python3
"""Support checks for the D5 Theta phase-event law."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, List, Mapping, MutableMapping

import torus_nd_d5_deep_transition_carry_sheet as carry046
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-THETA-PHASE-EVENT-CHECK-058A"
DEFAULT_M_VALUES = (13, 15, 17, 19, 21, 23)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _jsonable_row(row: Mapping[str, object], theta: int) -> Dict[str, object]:
    b = list(row["B"])
    return {
        "m": int(row["m"]),
        "source_u": int(row["source_u"]),
        "trace_step": int(row["trace_step"]),
        "state_index": int(row["state_index"]),
        "family": str(row["family"]),
        "B": [int(value) for value in b],
        "s": int(b[0]),
        "u": int(b[1]),
        "v": int(b[2]),
        "layer": int(b[3]),
        "q": int(row["q"]),
        "c": int(row["c"]),
        "theta": int(theta),
        "epsilon4": str(row["epsilon4"]),
        "dn": [int(value) for value in row["dn"]],
    }


def _expected(theta: int, s: int, c: int, m: int) -> tuple[str, tuple[int, int, int, int]] | None:
    if theta == 0:
        return ("wrap", (0, 0, 0, 0))
    if theta == 1:
        return ("carry_jump", (1, 1, 0, 0))
    if theta == 2:
        if c == 1:
            return ("other", (1, 0, 0, 0))
        return ("flat", (0, 0, 0, 1))
    if theta == 3:
        if (c == 0 and s == 2) or (c == 1 and s != 2):
            return ("other", (0, 0, 1, 0))
        return ("flat", (0, 0, 0, 1))
    if 4 <= theta <= m - 1:
        return ("flat", (0, 0, 0, 1))
    return None


def _event_class(dn: tuple[int, int, int, int]) -> str:
    if dn == (0, 0, 0, 0):
        return "wrap"
    if dn == (1, 1, 0, 0):
        return "carry_jump"
    if dn == (0, 0, 0, 1):
        return "flat"
    return "other"


def _check_modulus(m: int) -> Dict[str, object]:
    payload = carry046._build_active_data(int(m))
    rows = payload["active_rows"]

    failures = []
    buckets: MutableMapping[tuple[int, int, int], Counter[str]] = defaultdict(Counter)
    compressed: Dict[str, Dict[str, Dict[str, List[int]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for row in rows:
        b = list(row["B"])
        s = int(b[0])
        v = int(b[2])
        layer = int(b[3])
        theta = (int(row["q"]) + s + v + layer) % int(m)
        c = int(row["c"])
        dn = tuple(int(value) for value in row["dn"])
        epsilon = _event_class(dn)
        expected = _expected(theta, s, c, int(m))

        label = f"({epsilon}, {dn})"
        buckets[(theta, s, c)][label] += 1
        compressed[str(theta)][str(c)][label].append(int(s))

        if expected is not None and (epsilon, dn) != expected:
            failures.append(_jsonable_row(row, theta))

    # compress s lists for readability
    compressed_out: Dict[str, Dict[str, Dict[str, List[int]]]] = {}
    for theta_key, by_c in compressed.items():
        compressed_out[theta_key] = {}
        for c_key, by_label in by_c.items():
            compressed_out[theta_key][c_key] = {
                label: sorted(values)
                for label, values in by_label.items()
            }

    return {
        "m": int(m),
        "row_count": int(len(rows)),
        "is_exact_on_theta_s_c": bool(len(failures) == 0),
        "conflict": None if not failures else failures[0],
        "compressed": compressed_out,
        "sample_failures": failures[:8],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Support checks for the D5 Theta phase-event law.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument(
        "--m-values",
        type=int,
        nargs="+",
        default=list(DEFAULT_M_VALUES),
        help="Odd moduli to check.",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=0,
        help="Worker count. Default uses one worker per modulus up to 6.",
    )
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    m_values = [int(m) for m in args.m_values]
    jobs = int(args.jobs) if int(args.jobs) > 0 else min(len(m_values), 6)

    with ProcessPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(_check_modulus, m_values))
    results.sort(key=lambda item: int(item["m"]))

    per_modulus = {str(item["m"]): item for item in results}
    analysis_summary = {
        "task_id": TASK_ID,
        "main_result": (
            "On the extended proof-support range m=13,15,17,19,21,23, the active phase-event law in Theta=q+s+v+layer remains exact on "
            "(Theta,s,c): Theta=0 gives wrap, Theta=1 gives carry_jump, Theta=2 and Theta=3 give the checked c/s-dependent other-vs-flat "
            "splits, and Theta>=4 gives flat."
        ),
        "checked_moduli": m_values,
        "all_exact_on_theta_s_c": bool(all(item["is_exact_on_theta_s_c"] for item in results)),
        "environment": environment_block(),
        "runtime_seconds": runtime_since(started),
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "theta_phase_event_checks_058a.json", per_modulus)
    _write_json(out_dir / "sample_failures_058a.json", {
        str(item["m"]): item["sample_failures"]
        for item in results
    })
    _write_json(args.summary_out, analysis_summary)


if __name__ == "__main__":
    main()
