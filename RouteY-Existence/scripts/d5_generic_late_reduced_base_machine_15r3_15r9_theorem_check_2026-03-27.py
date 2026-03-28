from __future__ import annotations

"""Check the packaged reduced-base-machine theorem in the 15r+3 / 15r+9 good branches."""

import json
import os
import sys
import tarfile
import time
from functools import lru_cache
from typing import Dict, List

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


@lru_cache(maxsize=None)
def reduced_g_exact(m: int) -> np.ndarray:
    P = symbolic_P_base(m)
    M = m // 3
    P3 = P[P[P]]
    out = np.empty(M, dtype=np.int64)
    for u in range(M):
        a = 3 * u + 1
        b = int(P3[a])
        if b % 3 != 1:
            raise RuntimeError(("P^3 left active residue", m, u, b))
        out[u] = (b - 1) // 3
    return out


@lru_cache(maxsize=None)
def special_hit_map_exact(m: int, t: int = 4) -> np.ndarray:
    f, rho, spec = source_data(m, t)
    M = m // 3
    hit = np.empty(M, dtype=np.int64)
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
    return hit


def delta_M_formula(m: int) -> int:
    if m % 15 == 3:
        r = (m - 3) // 15
        return 3 * r + 2
    if m % 15 == 9:
        r = (m - 9) // 15
        return r + 2
    raise ValueError(("unsupported class", m))


def power_map(mp: np.ndarray, r: int) -> np.ndarray:
    n = len(mp)
    out = np.arange(n, dtype=np.int64)
    for _ in range(r):
        out = mp[out]
    return out


def defect_offsets_formula(m: int, L: int) -> List[int]:
    if m % 15 == 3:
        r = (m - 3) // 15
        if r % 3 != 2:  # unsplit
            out = []
            for j in range(L):
                if j == 0 or 2 * r + 1 <= j <= 5 * r:
                    out.append(3 * r)
                elif 1 <= j <= 2 * r - 2:
                    out.append(3 * r + 2)
                elif 2 * r - 1 <= j <= 2 * r:
                    out.append(r + 2)
                else:
                    raise RuntimeError(("uncovered 15r+3 unsplit", m, L, j))
            return out
        # split
        expL = (5 * r + 2) // 3
        if L != expL:
            raise RuntimeError(("bad split length 15r+3", m, L, expL))
        out = [0]
        out.extend([(4 * r - 2) // 3] * ((r + 1) // 3))
        out.extend([(4 * r + 1) // 3] * (L - 1 - (r + 1) // 3))
        if len(out) != L:
            raise RuntimeError(("length mismatch 15r+3 split", m, L, len(out)))
        return out

    if m % 15 == 9:
        r = (m - 9) // 15
        if r % 3 != 1:  # unsplit
            if r == 2:
                return [0] + [2] * 10 + [3] * 2
            out = []
            for j in range(L):
                if j == 0 or 5 * r <= j <= 5 * r + 2:
                    out.append(3)
                elif 1 <= j <= 4 * r + 2:
                    out.append(r)
                elif 4 * r + 3 <= j <= 5 * r - 1:
                    out.append(r + 4)
                else:
                    raise RuntimeError(("uncovered 15r+9 unsplit", m, L, j))
            return out
        # split
        expL = (5 * r + 4) // 3
        if L != expL:
            raise RuntimeError(("bad split length 15r+9", m, L, expL))
        out = [0]
        out.extend([(r - 1) // 3] * ((4 * r + 2) // 3))
        out.extend([(r + 2) // 3] * (L - 1 - (4 * r + 2) // 3))
        if len(out) != L:
            raise RuntimeError(("length mismatch 15r+9 split", m, L, len(out)))
        return out

    raise ValueError(("unsupported class", m))


def build_N_formula(m: int) -> np.ndarray:
    p = p_gen_arr(m)
    M = m // 3
    out = np.empty(M, dtype=np.int64)
    cycles = decompose(p)
    defect_cycle = None
    for cyc in cycles:
        if 1 in cyc:
            defect_cycle = cyc
            break
    if defect_cycle is None:
        raise RuntimeError(("no defect cycle", m))
    # nondefect cycles
    for cyc in cycles:
        if cyc is defect_cycle:
            continue
        L = len(cyc)
        rC = (m - 1) % L
        pr = power_map(p, rC)
        for u in cyc:
            out[u] = int(pr[u])
    # defect cycle
    h = defect_cycle.index(1)
    cyc_rot = defect_cycle[h:] + defect_cycle[:h]
    L = len(cyc_rot)
    offsets = defect_offsets_formula(m, L)
    for j, u in enumerate(cyc_rot):
        out[u] = cyc_rot[(j + offsets[j]) % L]
    return out


def build_g_formula(m: int) -> np.ndarray:
    N = build_N_formula(m)
    M = m // 3
    return (N + delta_M_formula(m)) % M


def main() -> None:
    start = time.time()
    ms = [m for m in range(33, 602, 6) if m % 5 != 0 and m % 7 != 0 and m % 15 in (3, 9)]
    n_fail: List[Dict[str, object]] = []
    g_fail: List[Dict[str, object]] = []
    total_moduli = 0
    total_states = 0
    selected: Dict[str, object] = {}
    for m in ms:
        total_moduli += 1
        M = m // 3
        total_states += M
        N_exact = special_hit_map_exact(m)
        N_formula = build_N_formula(m)
        if not np.array_equal(N_exact, N_formula):
            diff = [i for i in range(M) if int(N_exact[i]) != int(N_formula[i])][:10]
            n_fail.append({
                "m": m,
                "M": M,
                "diff_indices": diff,
                "exact": {str(i): int(N_exact[i]) for i in diff},
                "formula": {str(i): int(N_formula[i]) for i in diff},
            })
        g_exact = reduced_g_exact(m)
        g_formula = build_g_formula(m)
        if not np.array_equal(g_exact, g_formula):
            diff = [i for i in range(M) if int(g_exact[i]) != int(g_formula[i])][:10]
            g_fail.append({
                "m": m,
                "M": M,
                "diff_indices": diff,
                "exact": {str(i): int(g_exact[i]) for i in diff},
                "formula": {str(i): int(g_formula[i]) for i in diff},
            })
        if m in (33, 39, 93, 129, 219):
            selected[str(m)] = {
                "delta_M": delta_M_formula(m),
                "cycle_type_g": sorted([len(c) for c in decompose(g_formula)], reverse=True),
            }
    report = {
        "title": "d=5 generic-late reduced base machine 15r+3/15r+9 theorem check report",
        "scope": [
            "33<=m<=601",
            "3|m, 5∤m, 7∤m, m≡3 or 9 (mod 15)",
            "Checks the packaged theorem for N_t and g_t in the 15r+3 / 15r+9 good branches.",
        ],
        "summary": {
            "total_moduli": total_moduli,
            "total_states": total_states,
            "N_failures": len(n_fail),
            "g_failures": len(g_fail),
            "seconds": time.time() - start,
        },
        "selected_examples": selected,
        "N_failure_samples": n_fail[:8],
        "g_failure_samples": g_fail[:8],
    }
    txt = "/mnt/data/d5_generic_late_reduced_base_machine_15r3_15r9_theorem_check_report_2026-03-27.txt"
    jsn = "/mnt/data/d5_generic_late_reduced_base_machine_15r3_15r9_theorem_check_report_2026-03-27.json"
    with open(jsn, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    with open(txt, "w", encoding="utf-8") as f:
        f.write("d=5 generic-late reduced base machine 15r+3/15r+9 theorem check report\n")
        f.write("=================================================================\n\n")
        f.write(json.dumps(report["summary"], indent=2, sort_keys=True))
        f.write("\n\nSelected examples\n")
        for m, row in selected.items():
            f.write(f"  m={m}: delta_M={row['delta_M']}, cycle_type_g={row['cycle_type_g']}\n")
        if n_fail or g_fail:
            f.write("\n\nFailure samples\n")
            f.write(json.dumps({"N": n_fail[:8], "g": g_fail[:8]}, indent=2, sort_keys=True))
    print(txt)


if __name__ == "__main__":
    main()
