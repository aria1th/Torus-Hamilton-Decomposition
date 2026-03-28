from __future__ import annotations

"""Checks for the generic-late base-splice 7-split theorem."""

import os
import sys
import time
import tarfile
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Tuple

import numpy as np

ARCHIVE = "/mnt/data/d5_consolidated_support_archive_2026-03-27.tar"
EXTRACT_ROOT = "/mnt/data/extract"
EXTRACT_DIR = os.path.join(EXTRACT_ROOT, "d5_consolidated_support_archive_2026-03-27")
SCRIPTS_DIR = os.path.join(EXTRACT_DIR, "02_scripts_and_reports")


def ensure_extract() -> None:
    if os.path.exists(SCRIPTS_DIR):
        return
    os.makedirs(EXTRACT_ROOT, exist_ok=True)
    with tarfile.open(ARCHIVE, "r") as tf:
        tf.extractall(EXTRACT_ROOT)


ensure_extract()
sys.path.append(SCRIPTS_DIR)

import scan_promoted_plus_t as scan  # type: ignore
import visibility_t1_generic_arithmetic_audit as audit  # type: ignore


@dataclass
class RawExactStateCheck:
    a: int
    symbolic_image: int
    exact_image: int
    exact_steps: int


def cycle_type_arr(mp: np.ndarray) -> Tuple[int, ...]:
    n = len(mp)
    seen = np.zeros(n, dtype=np.uint8)
    out: List[int] = []
    for s in range(n):
        if seen[s]:
            continue
        cur = s
        c = 0
        while not seen[cur]:
            seen[cur] = 1
            c += 1
            cur = int(mp[cur])
        out.append(c)
    return tuple(sorted(out, reverse=True))


@lru_cache(maxsize=None)
def source_data(m: int):
    return audit.ordinary_source_data(m, 4)


def candidate_next(m: int, A: int, e: int) -> Tuple[int, int]:
    f, rho, spec = source_data(m)
    return audit.candidate_next_return(m, f, rho, spec, A, e)


def eventual_base_from_special(m: int, A: int) -> int:
    f, rho, spec = source_data(m)
    e = audit.special_row(m, A)
    Acur, ecur = audit.symbolic_next_return_compact(m, 4, A, e)
    steps = 0
    while ecur != 0:
        Acur, ecur = audit.candidate_next_return(m, f, rho, spec, Acur, ecur)
        steps += 1
        if steps > 20 * m * m:
            raise RuntimeError(("special source did not return to base", m, A))
    return Acur


def symbolic_P_base(m: int) -> np.ndarray:
    f, rho, spec = source_data(m)
    out = np.empty(m, dtype=np.int64)
    for A0 in range(m):
        A, e = audit.symbolic_next_return_compact(m, 4, A0, 0)
        steps = 0
        while e != 0:
            A, e = audit.candidate_next_return(m, f, rho, spec, A, e)
            steps += 1
            if steps > 20 * m * m:
                raise RuntimeError(("base orbit did not return", m, A0))
        out[A0] = A
    return out


def exact_B_map(m: int, max_blocks: int = 4_000_000) -> np.ndarray:
    ops = scan.ops_for_t(m, 4)
    mp, ok, steps = scan.build_B_map(m, ops, scan.Q2, max_blocks)
    if not np.all(ok == 1):
        raise RuntimeError((m, int(np.sum(ok == 0))))
    return np.array(mp, dtype=np.int64)


def exact_one_state(m: int, a: int, max_blocks: int = 20_000_000) -> Tuple[int, int]:
    ops = scan.ops_for_t(m, 4)
    img, steps, flag = scan.next_return_B(a, m, ops, scan.Q2, max_blocks)
    if flag != 1:
        raise RuntimeError((m, a, "no exact base return within bound"))
    return int(img), int(steps)


def inv_mod(a: int, m: int) -> int:
    return pow(a, -1, m)


def r_good(m: int) -> int:
    return (-4 * inv_mod(5, m)) % m


def delta_good(m: int) -> int:
    return (7 * (r_good(m) + 1)) % m


def scan_symbolic(limit_m: int = 301) -> Dict[str, object]:
    safe_ms = [m for m in range(27, limit_m + 1, 6) if m % 5 != 0]
    good_ms = [m for m in safe_ms if m % 7 != 0]
    bad_ms = [m for m in safe_ms if m % 7 == 0]

    good_failures: List[Tuple[int, int, int, int]] = []
    drift_failures: List[int] = []
    bad_failures: List[Tuple[int, int, int]] = []
    obstruction_failures: List[int] = []
    bad_examples: List[Dict[str, object]] = []

    for m in good_ms:
        D = delta_good(m)
        for A in range(m):
            got = eventual_base_from_special(m, A)
            want = (A + D) % m
            if got != want and len(good_failures) < 20:
                good_failures.append((m, A, got, want))
        P = symbolic_P_base(m)
        diffs = (P - np.arange(m, dtype=np.int64)) % m
        if not np.all((diffs % 3) == 2):
            drift_failures.append(m)

    for m in bad_ms:
        P = symbolic_P_base(m)
        target = [A for A in range(m) if (A % 3 != 1) and (A % 7 != 4)]
        bad_here = [A for A in target if int(P[A]) != A]
        if bad_here:
            obstruction_failures.append(m)
            for A in bad_here[:4]:
                if len(bad_failures) < 20:
                    bad_failures.append((m, A, int(P[A])))
        bad_examples.append({
            "m": m,
            "M": m // 3,
            "fixed_points": int(np.sum(P == np.arange(m, dtype=np.int64))),
            "target_fixed_count": len(target),
            "cycle_type_prefix": list(cycle_type_arr(P)[:8]),
        })

    return {
        "safe_ms": safe_ms,
        "good_ms": good_ms,
        "bad_ms": bad_ms,
        "num_safe_ms": len(safe_ms),
        "num_good_ms": len(good_ms),
        "num_bad_ms": len(bad_ms),
        "good_special_formula_failures": good_failures,
        "good_drift_failures": drift_failures,
        "bad_fixed_point_failures": bad_failures,
        "bad_obstruction_failures": obstruction_failures,
        "bad_examples": bad_examples,
    }


def raw_exact_checks() -> Dict[str, object]:
    full_cases = [33, 39, 51, 63]
    full_results: List[Dict[str, object]] = []
    for m in full_cases:
        t0 = time.time()
        sym = symbolic_P_base(m)
        raw = exact_B_map(m)
        full_results.append({
            "m": m,
            "same": bool(np.array_equal(sym, raw)),
            "cycle_type": list(cycle_type_arr(raw)),
            "fixed_points": int(np.sum(raw == np.arange(m, dtype=np.int64))),
            "seconds": time.time() - t0,
        })

    sel_states = [0, 1, 4, 7]
    sel_results: List[RawExactStateCheck] = []
    P147 = symbolic_P_base(147)
    for a in sel_states:
        img, steps = exact_one_state(147, a)
        sel_results.append(RawExactStateCheck(
            a=a,
            symbolic_image=int(P147[a]),
            exact_image=img,
            exact_steps=steps,
        ))

    return {
        "full_map_cases": full_results,
        "selected_state_case_m147": [
            {
                "a": row.a,
                "symbolic_image": row.symbolic_image,
                "exact_image": row.exact_image,
                "exact_steps": row.exact_steps,
            }
            for row in sel_results
        ],
    }


def main() -> None:
    start = time.time()
    symbolic = scan_symbolic(limit_m=301)
    raw = raw_exact_checks()
    total_seconds = time.time() - start

    report = {
        "title": "d=5 generic-late base-splice 7-split check report",
        "scope": [
            "Symbolic scan on all safe moduli 27<=m<=301, 3|m, 5∤m, for generic-late row t=4.",
            "Checks the special-source induced base formula when 7∤m.",
            "Checks the fixed-point obstruction when 7|m.",
            "Performs selected raw exact comparisons on the actual B_m next-return map.",
        ],
        "symbolic": symbolic,
        "raw": raw,
        "summary": {
            "num_safe_ms": symbolic["num_safe_ms"],
            "num_good_ms": symbolic["num_good_ms"],
            "num_bad_ms": symbolic["num_bad_ms"],
            "good_special_formula_failures": len(symbolic["good_special_formula_failures"]),
            "good_drift_failures": len(symbolic["good_drift_failures"]),
            "bad_fixed_point_failures": len(symbolic["bad_fixed_point_failures"]),
            "bad_obstruction_failures": len(symbolic["bad_obstruction_failures"]),
            "raw_full_cases_all_match": all(row["same"] for row in raw["full_map_cases"]),
            "raw_m147_selected_all_match": all(row["symbolic_image"] == row["exact_image"] for row in raw["selected_state_case_m147"]),
            "seconds": total_seconds,
        },
    }

    import json
    json_path = "/mnt/data/d5_generic_late_base_splice_7split_check_report_2026-03-27.json"
    txt_path = "/mnt/data/d5_generic_late_base_splice_7split_check_report_2026-03-27.txt"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("d=5 generic-late base-splice 7-split check report\n")
        f.write("================================================\n\n")
        f.write(json.dumps(report["summary"], indent=2, sort_keys=True))
        f.write("\n\nBad-case examples\n")
        for row in symbolic["bad_examples"]:
            f.write(f"  m={row['m']}, M={row['M']}, fixed_points={row['fixed_points']}, target_fixed_count={row['target_fixed_count']}, cycle_type_prefix={row['cycle_type_prefix']}\n")
        f.write("\nSelected raw exact full-map comparisons\n")
        for row in raw["full_map_cases"]:
            f.write(f"  m={row['m']}: same={row['same']}, cycle_type={row['cycle_type']}, fixed_points={row['fixed_points']}, seconds={row['seconds']:.2f}\n")
        f.write("\nSelected raw exact state checks at m=147\n")
        for row in raw["selected_state_case_m147"]:
            f.write(f"  a={row['a']}: symbolic={row['symbolic_image']}, exact={row['exact_image']}, exact_steps={row['exact_steps']}\n")
    print(txt_path)


if __name__ == "__main__":
    main()
