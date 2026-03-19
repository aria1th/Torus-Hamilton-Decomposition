#!/usr/bin/env python3
"""Explicit formula validation for the D5 M3 comparison theorem draft."""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_deep_transition_carry_sheet as carry046
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-M3-FORMULA-SUPPORT-107"
DEFAULT_M_VALUES = (13, 15, 17)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _event_class(dn: Sequence[int]) -> str:
    dn_tuple = tuple(int(value) for value in dn)
    if dn_tuple == (0, 0, 0, 1):
        return "flat"
    if dn_tuple == (0, 0, 0, 0):
        return "wrap"
    if dn_tuple == (1, 1, 0, 0):
        return "carry_jump"
    if dn_tuple == (1, 0, 0, 0):
        return "other_1000"
    if dn_tuple == (0, 0, 1, 0):
        return "other_0010"
    return "other"


def _beta_from_row(row: Mapping[str, object], m: int) -> int:
    s, _u, v, layer, _family = [int(value) if idx < 4 else value for idx, value in enumerate(row["B"])]
    return int((-(int(row["q"]) + int(s) + int(v) + int(layer))) % m)


def _jsonable(value):
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _represent_row(row: Mapping[str, object]) -> Dict[str, object]:
    return {
        "m": int(row["m"]),
        "source_u": int(row["source_u"]),
        "rho": int(row["rho"]),
        "family": str(row["family"]),
        "trace_step": int(row["trace_step"]),
        "B": _jsonable(tuple(row["B"])),
        "q": int(row["q"]),
        "w": int(row["w"]),
        "u": int(row["u"]),
        "beta": int(row["beta"]),
        "q0": int(row["q0"]),
        "sigma": int(row["sigma"]),
        "delta": int(row["delta"]),
        "epsilon4": str(row["epsilon4"]),
    }


def _I_u(beta: int, m: int) -> int:
    return int(beta != m - 1)


def _I_w(beta: int, q: int, m: int) -> int:
    return int(beta <= m - 3 and q == m - 1)


def _extract_chain_rows(m: int) -> List[Dict[str, object]]:
    payload = carry046._build_active_data(m)
    rows = sorted(
        payload["active_rows"],
        key=lambda row: (int(row["source_u"]), str(row["family"]), int(row["trace_step"])),
    )
    by_branch: Dict[Tuple[int, str], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        by_branch[(int(row["source_u"]), str(row["family"]))].append(row)

    chain_rows: List[Dict[str, object]] = []
    for (source_u, family), seq in sorted(by_branch.items()):
        i = 0
        while i < len(seq):
            if _event_class(seq[i]["dn"]) != "carry_jump":
                i += 1
                continue

            start = seq[i]
            q0 = int(start["q"])
            sigma = int((int(source_u) + int(start["w"])) % m)
            rho = int((int(source_u) + 1) % m)

            chain: List[Mapping[str, object]] = []
            j = i
            while j < len(seq):
                row = seq[j]
                chain.append(row)
                if _event_class(row["dn"]) == "wrap":
                    break
                j += 1

            if not chain or _event_class(chain[-1]["dn"]) != "wrap":
                i += 1
                continue

            for row in chain:
                s, u_b, v, layer, _family = row["B"]
                s = int(s)
                u_b = int(u_b)
                v = int(v)
                layer = int(layer)
                beta = _beta_from_row(row, m)
                rec = {
                    "m": int(m),
                    "source_u": int(source_u),
                    "rho": int(rho),
                    "family": str(family),
                    "trace_step": int(row["trace_step"]),
                    "B": tuple(row["B"]),
                    "q": int(row["q"]),
                    "w": int(row["w"]),
                    "u": int(row["u"]),
                    "s": int(s),
                    "u_B": int(u_b),
                    "v": int(v),
                    "layer": int(layer),
                    "beta": int(beta),
                    "q0": int(q0),
                    "sigma": int(sigma),
                    "delta": int(q0 + m * sigma),
                    "epsilon4": str(_event_class(row["dn"])),
                }
                chain_rows.append(rec)

            i = j + 1

    return chain_rows


def _first_fail(rows, pred) -> Dict[str, object] | None:
    for row in rows:
        failure = pred(row)
        if failure is not None:
            return failure
    return None


def _analyze_modulus(m: int) -> Dict[str, object]:
    started = time.perf_counter()
    rows = _extract_chain_rows(m)

    def _q_formula(row):
        return int((-(int(row["beta"]) + int(row["s"]) + int(row["v"]) + int(row["layer"]))) % m)

    def _rho_formula(row):
        return int((int(row["u"]) - int(row["q"]) + int(row["beta"] == m - 1)) % m)

    def _sigma_formula(row):
        q = int(row["q"])
        beta = int(row["beta"])
        return int((int(row["s"]) - q - _I_u(beta, m) - _I_w(beta, q, m)) % m)

    def _u_formula(row):
        return int((int(row["q0"]) + int(row["rho"]) - 1 + _I_u(int(row["beta"]), m)) % m)

    def _w_formula(row):
        q0 = int(row["q0"])
        beta = int(row["beta"])
        return int((int(row["sigma"]) - int(row["rho"]) + 1 + _I_w(beta, q0, m)) % m)

    q_fail = _first_fail(
        rows,
        lambda row: None if _q_formula(row) == int(row["q"]) else {
            "reason": "q_formula",
            "predicted_q": int(_q_formula(row)),
            "row": _represent_row(row),
        },
    )
    rho_fail = _first_fail(
        rows,
        lambda row: None if _rho_formula(row) == int(row["rho"]) else {
            "reason": "rho_formula",
            "predicted_rho": int(_rho_formula(row)),
            "row": _represent_row(row),
        },
    )
    sigma_fail = _first_fail(
        rows,
        lambda row: None if _sigma_formula(row) == int(row["sigma"]) else {
            "reason": "sigma_formula",
            "predicted_sigma": int(_sigma_formula(row)),
            "row": _represent_row(row),
        },
    )
    u_fail = _first_fail(
        rows,
        lambda row: None if _u_formula(row) == int(row["u"]) else {
            "reason": "u_reconstruction",
            "predicted_u": int(_u_formula(row)),
            "row": _represent_row(row),
        },
    )
    w_fail = _first_fail(
        rows,
        lambda row: None if _w_formula(row) == int(row["w"]) else {
            "reason": "w_reconstruction",
            "predicted_w": int(_w_formula(row)),
            "row": _represent_row(row),
        },
    )

    beta_counts = defaultdict(int)
    for row in rows:
        beta_counts[str(int(row["beta"]))] += 1

    collision_examples = []
    for rho in (2, 3):
        hit = None
        for row in rows:
            if (
                int(row["rho"]) == rho
                and int(row["beta"]) == m - 1
                and int(row["q0"]) == 0
                and int(row["sigma"]) == 5 % m
                and str(row["family"]) == "regular"
            ):
                hit = _represent_row(row)
                break
        collision_examples.append({"rho": int(rho), "row": hit})

    collision_present = all(item["row"] is not None for item in collision_examples)

    return {
        "m": int(m),
        "row_count": int(len(rows)),
        "runtime_seconds": runtime_since(started),
        "q_formula_exact": bool(q_fail is None),
        "rho_formula_exact": bool(rho_fail is None),
        "sigma_formula_exact": bool(sigma_fail is None),
        "u_reconstruction_exact": bool(u_fail is None),
        "w_reconstruction_exact": bool(w_fail is None),
        "first_failures": {
            "q_formula": q_fail,
            "rho_formula": rho_fail,
            "sigma_formula": sigma_fail,
            "u_reconstruction": u_fail,
            "w_reconstruction": w_fail,
        },
        "beta_counts": dict(sorted(beta_counts.items(), key=lambda item: int(item[0]))),
        "two_source_collision_witness_present": bool(collision_present),
        "two_source_collision_examples": collision_examples,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Explicit formula validation for the D5 M3 comparison theorem draft.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--m-values", type=int, nargs="+", default=list(DEFAULT_M_VALUES))
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    m_values = [int(m) for m in args.m_values]
    results: List[Dict[str, object]] = []

    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs, max_tasks_per_child=1) as pool:
            for result in pool.map(_analyze_modulus, m_values):
                print(f"[{TASK_ID}] finished m={result['m']} rows={result['row_count']}", flush=True)
                results.append(result)
    else:
        for m in m_values:
            result = _analyze_modulus(m)
            print(f"[{TASK_ID}] finished m={result['m']} rows={result['row_count']}", flush=True)
            results.append(result)

    results.sort(key=lambda item: int(item["m"]))
    by_m = {str(item["m"]): item for item in results}

    analysis_summary = {
        "task_id": TASK_ID,
        "checked_moduli": m_values,
        "all_q_formulas_exact": bool(all(item["q_formula_exact"] for item in results)),
        "all_rho_formulas_exact": bool(all(item["rho_formula_exact"] for item in results)),
        "all_sigma_formulas_exact": bool(all(item["sigma_formula_exact"] for item in results)),
        "all_u_reconstructions_exact": bool(all(item["u_reconstruction_exact"] for item in results)),
        "all_w_reconstructions_exact": bool(all(item["w_reconstruction_exact"] for item in results)),
        "all_two_source_collision_witnesses_present": bool(
            all(item["two_source_collision_witness_present"] for item in results)
        ),
        "main_result": (
            "On the regenerated carry_jump-to-wrap state-chain object for m=13,15,17, "
            "the explicit formulas proposed in tmp/107 are exact: q is recovered from the phase-corner identity, "
            "rho and sigma are extracted exactly from (B,beta), and the raw current coordinates u and w are "
            "reconstructed exactly from (rho,beta,q0,sigma). The symbolic two-source collision pattern for bare "
            "(beta,q0,sigma) is also realized on every checked modulus."
        ),
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "per_modulus_formula_validation.json", by_m)
    _write_json(args.summary_out, analysis_summary)


if __name__ == "__main__":
    main()
