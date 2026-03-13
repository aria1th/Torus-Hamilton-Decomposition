#!/usr/bin/env python3
"""Validate the explicit constructive rho-route formulas from 063."""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

import torus_nd_d5_source_residue_refinement as rho049
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-CONSTRUCTIVE-SOURCE-RESIDUE-SUPPORT-063A"
DEFAULT_M_VALUES = (13, 15, 17, 19)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _formula_delta(row: Mapping[str, object]) -> int:
    m = int(row["m"])
    return (int(row["rho"]) - (int(row["s"]) + int(row["u"]) + int(row["v"]) + int(row["layer"]))) % m


def _formula_a(row: Mapping[str, object]) -> int:
    m = int(row["m"])
    return 1 if (int(row["rho"]) - int(row["u"])) % m == 1 else 0


def _predict_c(row: Mapping[str, object]) -> int:
    m = int(row["m"])
    rhs = (int(row["u"]) + 1 + (1 if str(row["epsilon4"]) == "carry_jump" else 0)) % m
    return 1 if int(row["rho"]) == rhs else 0


def _predict_tau(row: Mapping[str, object]) -> int:
    m = int(row["m"])
    delta = _formula_delta(row)
    a = _formula_a(row)
    s = int(row["s"])
    if delta == 0:
        return 0
    if 1 <= delta <= m - 4:
        return delta
    if delta == m - 3:
        cond = (a == 0 and s == 2) or (a == 1 and s != 2)
        return 0 if cond else m - 3
    if delta == m - 2:
        if a == 1:
            return 0
        if s == 2:
            return 1
        return m - 2
    raise AssertionError(f"unexpected delta={delta} for m={m}")


def _predict_next_tau(row: Mapping[str, object]) -> int:
    m = int(row["m"])
    epsilon4 = str(row["epsilon4"])
    if epsilon4 == "flat":
        return int(row["tau"]) - 1
    if epsilon4 == "wrap":
        return 0
    if epsilon4 == "carry_jump":
        if (int(row["rho"]) - int(row["u"])) % m == 2:
            return 0
        return 1 if int(row["s"]) == 1 else m - 2
    if epsilon4 == "other":
        delta = _formula_delta(row)
        s = int(row["s"])
        if delta == m - 2:
            return m - 3 if s == 1 else 0
        if delta == m - 3:
            return m - 4
        raise AssertionError(
            f"unexpected other-branch delta={delta} for m={m}, "
            f"row={rho049._represent_row(row)}"
        )
    raise AssertionError(f"unexpected epsilon4={epsilon4}")


def _predict_q(row: Mapping[str, object]) -> int:
    m = int(row["m"])
    return (int(row["u"]) - int(row["rho"]) + (1 if str(row["epsilon4"]) == "carry_jump" else 0)) % m


def _check_modulus(m: int) -> Dict[str, object]:
    rows = rho049._build_rows_for_m(int(m))
    tau_failures: List[Dict[str, object]] = []
    next_tau_failures: List[Dict[str, object]] = []
    c_failures: List[Dict[str, object]] = []
    q_failures: List[Dict[str, object]] = []
    unexpected_rows: List[Dict[str, object]] = []

    for row in rows:
        try:
            predicted_tau = _predict_tau(row)
            predicted_next_tau = _predict_next_tau(row)
            predicted_c = _predict_c(row)
            predicted_q = _predict_q(row)
        except Exception as exc:  # noqa: BLE001
            unexpected_rows.append(
                {
                    "error": str(exc),
                    "row": rho049._represent_row(row),
                    "delta": _formula_delta(row),
                    "a": _formula_a(row),
                }
            )
            continue

        if predicted_tau != int(row["tau"]):
            tau_failures.append(
                {
                    "predicted_tau": int(predicted_tau),
                    "delta": _formula_delta(row),
                    "a": _formula_a(row),
                    "row": rho049._represent_row(row),
                }
            )
        if predicted_next_tau != int(row["next_tau"]):
            next_tau_failures.append(
                {
                    "predicted_next_tau": int(predicted_next_tau),
                    "delta": _formula_delta(row),
                    "a": _formula_a(row),
                    "row": rho049._represent_row(row),
                }
            )
        if predicted_c != int(row["c"]):
            c_failures.append(
                {
                    "predicted_c": int(predicted_c),
                    "row": rho049._represent_row(row),
                }
            )
        if predicted_q != int(row["q"]):
            q_failures.append(
                {
                    "predicted_q": int(predicted_q),
                    "row": rho049._represent_row(row),
                }
            )

    return {
        "m": int(m),
        "row_count": int(len(rows)),
        "tau_formula_exact": bool(not tau_failures and not unexpected_rows),
        "next_tau_formula_exact": bool(not next_tau_failures and not unexpected_rows),
        "c_formula_exact": bool(not c_failures and not unexpected_rows),
        "q_formula_exact": bool(not q_failures and not unexpected_rows),
        "tau_formula_collisions": int(len(tau_failures)),
        "next_tau_formula_collisions": int(len(next_tau_failures)),
        "c_formula_collisions": int(len(c_failures)),
        "q_formula_collisions": int(len(q_failures)),
        "unexpected_row_count": int(len(unexpected_rows)),
        "first_tau_failure": tau_failures[:1],
        "first_next_tau_failure": next_tau_failures[:1],
        "first_c_failure": c_failures[:1],
        "first_q_failure": q_failures[:1],
        "first_unexpected_row": unexpected_rows[:1],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the explicit constructive rho-route formulas from 063.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument(
        "--m-values",
        type=int,
        nargs="+",
        default=list(DEFAULT_M_VALUES),
        help="Odd moduli to analyze.",
    )
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    m_values = [int(m) for m in args.m_values]
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(_check_modulus, m_values))
    else:
        results = [_check_modulus(m) for m in m_values]
    results_by_m = {str(item["m"]): item for item in sorted(results, key=lambda item: item["m"])}

    all_exact = all(
        item["tau_formula_exact"]
        and item["next_tau_formula_exact"]
        and item["c_formula_exact"]
        and item["q_formula_exact"]
        for item in results
    )

    first_collision_witnesses = {
        "tau_formula": next(
            (item["first_tau_failure"][0] for item in results if item["first_tau_failure"]),
            None,
        ),
        "next_tau_formula": next(
            (item["first_next_tau_failure"][0] for item in results if item["first_next_tau_failure"]),
            None,
        ),
        "c_formula": next(
            (item["first_c_failure"][0] for item in results if item["first_c_failure"]),
            None,
        ),
        "q_formula": next(
            (item["first_q_failure"][0] for item in results if item["first_q_failure"]),
            None,
        ),
        "unexpected_row": next(
            (item["first_unexpected_row"][0] for item in results if item["first_unexpected_row"]),
            None,
        ),
    }

    constructive_route_compression = {
        "current_rho_transport_required": True,
        "current_delta_computation": "delta = rho - (s + u + v + layer) (mod m)",
        "piecewise_current_formulas": {
            "c": "1_{rho = u + 1 + 1_{epsilon4=carry_jump}}",
            "tau": "explicit piecewise delta-formula from 063",
            "next_tau": "explicit branchwise piecewise formula on (s,u,layer,rho,epsilon4)",
        },
        "stable_through_m_19": bool(all_exact),
    }

    analysis_summary = {
        "task_id": TASK_ID,
        "checked_moduli": m_values,
        "all_requested_checks_exact": bool(all_exact),
        "constructive_route_stable_through_m_19": bool(all_exact),
        "per_modulus": results_by_m,
        "first_collision_witnesses": first_collision_witnesses,
        "constructive_route_compression": constructive_route_compression,
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "constructive_source_residue_extension_checks_063a.json", results_by_m)
    _write_json(out_dir / "constructive_route_compression_063a.json", constructive_route_compression)
    _write_json(out_dir / "first_collision_witnesses_063a.json", first_collision_witnesses)
    _write_json(args.summary_out, analysis_summary)


if __name__ == "__main__":
    main()
