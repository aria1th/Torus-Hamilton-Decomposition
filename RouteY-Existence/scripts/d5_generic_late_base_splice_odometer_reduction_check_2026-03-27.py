from __future__ import annotations

"""Checks for the generic-late base-splice odometer reduction note."""

import json
import os
import sys
import tarfile
import time
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
if SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

import visibility_t1_generic_arithmetic_audit as audit  # type: ignore


def decompose(mp: np.ndarray) -> List[List[int]]:
    n = len(mp)
    seen = np.zeros(n, dtype=np.uint8)
    out: List[List[int]] = []
    for s in range(n):
        if seen[s]:
            continue
        cyc: List[int] = []
        cur = s
        while not seen[cur]:
            seen[cur] = 1
            cyc.append(int(cur))
            cur = int(mp[cur])
        out.append(cyc)
    return out


@lru_cache(maxsize=None)
def source_data(m: int, t: int = 4):
    return audit.ordinary_source_data(m, t)


@lru_cache(maxsize=None)
def p_gen_arr(m: int, t: int = 4) -> np.ndarray:
    f, rho, spec = source_data(m, t)
    M = m // 3
    out = np.empty(M, dtype=np.int64)
    for u in range(M):
        A = 3 * u + 1
        out[u] = (f[A] - 1) // 3
    return out


@lru_cache(maxsize=None)
def special_hit_map_and_steps(m: int, t: int = 4) -> Tuple[np.ndarray, np.ndarray]:
    f, rho, spec = source_data(m, t)
    M = m // 3
    hit = np.empty(M, dtype=np.int64)
    steps = np.empty(M, dtype=np.int64)
    for u in range(M):
        A = 3 * u + 1
        Acur, ecur = audit.symbolic_next_return_compact(m, t, A, 0)
        n = 1
        while ecur != audit.special_row(m, Acur):
            Acur, ecur = audit.candidate_next_return(m, f, rho, spec, Acur, ecur)
            n += 1
            if n > 1_000_000:
                raise RuntimeError(("too many source steps", m, u))
        hit[u] = (Acur - 1) // 3
        steps[u] = n
    return hit, steps


@lru_cache(maxsize=None)
def symbolic_P_base(m: int, t: int = 4) -> np.ndarray:
    f, rho, spec = source_data(m, t)
    out = np.empty(m, dtype=np.int64)
    for A0 in range(m):
        A, e = audit.symbolic_next_return_compact(m, t, A0, 0)
        n = 0
        while e != 0:
            A, e = audit.candidate_next_return(m, f, rho, spec, A, e)
            n += 1
            if n > 1_000_000:
                raise RuntimeError(("too many base steps", m, A0))
        out[A0] = A
    return out


def reduced_g_from_P(m: int) -> np.ndarray:
    P = symbolic_P_base(m)
    M = m // 3
    P3 = P[P[P]]
    out = np.empty(M, dtype=np.int64)
    for u in range(M):
        a = 3 * u + 1
        b = int(P3[a])
        if b % 3 != 1:
            raise RuntimeError(("P^3 left the active residue class", m, u, b))
        out[u] = (b - 1) // 3
    return out


def delta_M(m: int) -> int:
    M = m // 3
    return (7 * pow(5, -1, m)) % m % M


def power_map(mp: np.ndarray, r: int) -> np.ndarray:
    n = len(mp)
    out = np.arange(n, dtype=np.int64)
    for _ in range(r):
        out = mp[out]
    return out


def defect_formula(m: int, L: int, r: int) -> Tuple[int, int, int]:
    """Returns (offset b, first special time n, chosen q)."""
    eta = (2 - 5 * L) % m
    d = (L - r) % L
    best: Tuple[int, int, int] | None = None
    g = int(np.gcd(int(eta), int(m)))
    mod = int(m // g)
    inv = pow(int(eta // g), -1, int(mod))

    for b in range(L):
        rhs = (5 * (b + 1) - (2 if b >= d else 0)) % m
        if rhs % g != 0:
            continue
        q = (inv * (rhs // g)) % mod
        n = q * L + b
        if n == 0:
            n += mod * L
        row = (b, n, q)
        if best is None or row[1] < best[1]:
            best = row
    if best is None:
        raise RuntimeError(("no defect candidate", m, L, r))
    return best


def main() -> None:
    start = time.time()
    good_ms = [m for m in range(27, 302, 6) if m % 5 != 0 and m % 7 != 0]

    factor_failures: List[Dict[str, object]] = []
    nondef_failures: List[Dict[str, object]] = []
    defect_failures: List[Dict[str, object]] = []

    total_moduli = 0
    total_active_states = 0
    total_nondef_cycles = 0
    total_nondef_states = 0
    total_def_cycles = 0
    total_def_states = 0

    selected_examples: Dict[str, object] = {}

    for m in good_ms:
        total_moduli += 1
        M = m // 3
        total_active_states += M

        p = p_gen_arr(m)
        N, steps = special_hit_map_and_steps(m)
        g_exact = reduced_g_from_P(m)
        g_fact = (N + delta_M(m)) % M

        if not np.array_equal(g_exact, g_fact):
            factor_failures.append({
                "m": m,
                "M": M,
                "exact_g_head": g_exact[:12].tolist(),
                "factored_g_head": g_fact[:12].tolist(),
            })

        cycles = decompose(p)
        for cyc in cycles:
            L = len(cyc)
            if 1 not in cyc:
                total_nondef_cycles += 1
                total_nondef_states += L
                rC = (m - 1) % L
                pr = power_map(p, rC)
                for u in cyc:
                    if int(N[u]) != int(pr[u]):
                        nondef_failures.append({
                            "m": m,
                            "cycle_length": L,
                            "u": int(u),
                            "N_u": int(N[u]),
                            "expected": int(pr[u]),
                            "rC": int(rC),
                        })
                        break
            else:
                total_def_cycles += 1
                total_def_states += L
                h = cyc.index(1)
                cyc_rot = cyc[h:] + cyc[:h]
                idx = {u: i for i, u in enumerate(cyc_rot)}
                residuals: List[int] = []
                for r, u in enumerate(cyc_rot):
                    target_idx = idx[int(N[u])]
                    b_actual = (target_idx - r) % L
                    b, n, q = defect_formula(m, L, r)
                    residuals.append(int(b_actual))
                    if b_actual != b or int(steps[u]) != n:
                        defect_failures.append({
                            "m": m,
                            "cycle_length": L,
                            "r": int(r),
                            "b_actual": int(b_actual),
                            "b_formula": int(b),
                            "steps_actual": int(steps[u]),
                            "steps_formula": int(n),
                            "q_formula": int(q),
                        })
                        break
                if m in (39, 81):
                    selected_examples[str(m)] = {
                        "defect_cycle_length": L,
                        "residual_offsets": residuals,
                    }

    report = {
        "title": "d=5 generic-late base-splice odometer reduction check report",
        "scope": [
            "Good generic-late branch only: 27<=m<=301, 3|m, 5∤m, 7∤m.",
            "Verifies the factorization g_t = N_t + delta_M.",
            "Verifies the constant-power formula on every nondefect active cycle.",
            "Verifies the explicit defect-cycle odometer equation.",
        ],
        "summary": {
            "total_moduli": total_moduli,
            "total_active_states": total_active_states,
            "total_nondef_cycles": total_nondef_cycles,
            "total_nondef_states": total_nondef_states,
            "total_def_cycles": total_def_cycles,
            "total_def_states": total_def_states,
            "factor_failures": len(factor_failures),
            "nondef_failures": len(nondef_failures),
            "defect_failures": len(defect_failures),
            "seconds": time.time() - start,
        },
        "selected_examples": selected_examples,
        "factor_failure_samples": factor_failures[:8],
        "nondef_failure_samples": nondef_failures[:8],
        "defect_failure_samples": defect_failures[:8],
    }

    json_path = "/mnt/data/d5_generic_late_base_splice_odometer_reduction_check_report_2026-03-27.json"
    txt_path = "/mnt/data/d5_generic_late_base_splice_odometer_reduction_check_report_2026-03-27.txt"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("d=5 generic-late base-splice odometer reduction check report\n")
        f.write("=========================================================\n\n")
        f.write(json.dumps(report["summary"], indent=2, sort_keys=True))
        f.write("\n\nSelected examples\n")
        for m, row in report["selected_examples"].items():
            f.write(f"  m={m}: defect_cycle_length={row['defect_cycle_length']}, residual_offsets={row['residual_offsets']}\n")
        if factor_failures or nondef_failures or defect_failures:
            f.write("\n\nFailure samples\n")
            f.write(json.dumps({
                "factor": factor_failures[:8],
                "nondef": nondef_failures[:8],
                "defect": defect_failures[:8],
            }, indent=2, sort_keys=True))
    print(txt_path)


if __name__ == "__main__":
    main()
