#!/usr/bin/env python3
"""Support checks for the D5 active phase scheduler theorem of 059."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, List, Mapping, MutableMapping

import torus_nd_d5_corridor_phase_extraction as phase034
import torus_nd_d5_deep_transition_carry_sheet as carry046
import torus_nd_d5_endpoint_latin_repair as seed032
import torus_nd_d5_layer3_mode_switch_common as mode008
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-PHASE-SCHEDULER-SUPPORT-059A"
DEFAULT_M_VALUES = (25, 27, 29)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _event_class(dn: tuple[int, int, int, int]) -> str:
    if dn == (0, 0, 0, 0):
        return "wrap"
    if dn == (1, 1, 0, 0):
        return "carry_jump"
    if dn == (0, 0, 0, 1):
        return "flat"
    return "other"


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


def _jsonable_row(row: Mapping[str, object], theta: int, pred_sig1_wu2: int) -> Dict[str, object]:
    b = list(row["B"])
    return {
        "m": int(row["m"]),
        "source_u": int(row["source_u"]),
        "trace_step": int(row["trace_step"]),
        "state_index": int(row["state_index"]),
        "family": str(row["family"]),
        "label": str(row["label"]),
        "B": [int(value) if isinstance(value, int) else value for value in b],
        "s": int(b[0]),
        "u": int(b[1]),
        "v": int(b[2]),
        "layer": int(b[3]),
        "q": int(row["q"]),
        "w": int(row["w"]),
        "c": int(row["c"]),
        "theta": int(theta),
        "pred_sig1_wu2": int(pred_sig1_wu2),
        "dn": [int(value) for value in row["dn"]],
        "exit_dirs": [int(value) for value in row["exit_dirs"]],
    }


def _build_support_rows(m: int) -> List[Dict[str, object]]:
    payload = carry046._build_active_data(int(m))
    return payload["active_rows"]


def _pred_sig1_wu2_from_row(row: Mapping[str, object], m: int) -> int:
    coords = (
        int(row["layer"]),
        int(row["q"]),
        int(row["w"]),
        int(row["v"]),
        int(row["u"]),
    )
    pred1 = mode008.predecessor_coords(coords, 0, 1, int(m))
    return int(mode008.wu2_value(pred1, 0, int(m)))


def _representative_table(rows: List[Mapping[str, object]], m: int) -> Dict[str, object]:
    table: MutableMapping[str, MutableMapping[str, MutableMapping[str, Dict[str, object]]]] = defaultdict(
        lambda: defaultdict(dict)
    )
    for row in rows:
        b = list(row["B"])
        s = int(b[0])
        theta = (int(row["q"]) + s + int(row["v"]) + int(row["layer"])) % int(m)
        c = int(row["c"])
        dn = tuple(int(value) for value in row["dn"])
        epsilon = _event_class(dn)
        theta_key = str(theta)
        c_key = str(c)
        s_key = str(s)
        if s_key in table[theta_key][c_key]:
            continue
        table[theta_key][c_key][s_key] = {
            "epsilon4": epsilon,
            "dn": [int(value) for value in dn],
            "state_index": int(row["state_index"]),
            "trace_step": int(row["trace_step"]),
            "source_u": int(row["source_u"]),
        }
    out: Dict[str, object] = {}
    for theta_key, by_c in sorted(table.items(), key=lambda item: int(item[0])):
        out[theta_key] = {}
        for c_key, by_s in sorted(by_c.items(), key=lambda item: int(item[0])):
            out[theta_key][c_key] = {
                s_key: payload
                for s_key, payload in sorted(by_s.items(), key=lambda item: int(item[0]))
            }
    return out


def _check_modulus(m: int) -> Dict[str, object]:
    rows = _build_support_rows(int(m))
    nonterminal_rows = [row for row in rows if not row["exit_dirs"]]

    scheduler_failures = []
    label_failures = []
    pred_failures = []

    for row in nonterminal_rows:
        b = list(row["B"])
        s = int(b[0])
        theta = (int(row["q"]) + s + int(row["v"]) + int(row["layer"])) % int(m)
        c = int(row["c"])
        dn = tuple(int(value) for value in row["dn"])
        epsilon = _event_class(dn)
        expected = _expected(theta, s, c, int(m))
        pred_sig1_wu2 = _pred_sig1_wu2_from_row(row, int(m))

        if str(row["label"]) != "B":
            label_failures.append(_jsonable_row(row, theta, pred_sig1_wu2))
        if pred_sig1_wu2 != int(s == 2):
            pred_failures.append(_jsonable_row(row, theta, pred_sig1_wu2))
        if expected is not None and (epsilon, dn) != expected:
            scheduler_failures.append(_jsonable_row(row, theta, pred_sig1_wu2))

    label_hist = Counter(str(row["label"]) for row in nonterminal_rows)

    return {
        "m": int(m),
        "active_row_count": int(len(rows)),
        "active_nonterminal_row_count": int(len(nonterminal_rows)),
        "scheduler_exact": bool(not scheduler_failures),
        "all_nonterminal_labels_are_B": bool(not label_failures),
        "pred_sig1_wu2_equiv_s_eq_2": bool(not pred_failures),
        "label_histogram_nonterminal": dict(sorted(label_hist.items())),
        "first_scheduler_failure": None if not scheduler_failures else scheduler_failures[0],
        "first_label_failure": None if not label_failures else label_failures[0],
        "first_pred_failure": None if not pred_failures else pred_failures[0],
        "representative_table": _representative_table(nonterminal_rows, int(m)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Support checks for the D5 active phase scheduler theorem of 059.")
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
    m_values = [int(value) for value in args.m_values]
    jobs = int(args.jobs) if int(args.jobs) > 0 else min(len(m_values), 6)

    with ProcessPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(_check_modulus, m_values))
    results.sort(key=lambda item: int(item["m"]))

    per_modulus = {str(item["m"]): item for item in results}
    analysis_summary = {
        "task_id": TASK_ID,
        "main_result": (
            "On m=25,27,29, the 059 active phase scheduler support checks whether the nonterminal active best-seed branch remains B-labeled, "
            "whether pred_sig1_wu2 reduces to s=2, and whether the exact scheduler table on (Theta,s,c) still governs the grouped event."
        ),
        "checked_moduli": m_values,
        "all_scheduler_exact": bool(all(item["scheduler_exact"] for item in results)),
        "all_nonterminal_labels_are_B": bool(all(item["all_nonterminal_labels_are_B"] for item in results)),
        "all_pred_sig1_wu2_equiv_s_eq_2": bool(all(item["pred_sig1_wu2_equiv_s_eq_2"] for item in results)),
        "environment": environment_block(),
        "runtime_seconds": runtime_since(started),
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "phase_scheduler_support_059a.json", per_modulus)
    _write_json(
        out_dir / "representative_witness_tables_059a.json",
        {str(item["m"]): item["representative_table"] for item in results},
    )
    _write_json(args.summary_out, analysis_summary)


if __name__ == "__main__":
    main()
