from __future__ import annotations

import json
import os
import sys
import tarfile
from functools import lru_cache
from pathlib import Path

import numpy as np

ARCHIVE="/mnt/data/d5_consolidated_support_archive_2026-03-27.tar"
EXTRACT_ROOT="/mnt/data/extract"
EXTRACT_DIR=os.path.join(EXTRACT_ROOT, "d5_consolidated_support_archive_2026-03-27")
SCRIPTS_DIR=os.path.join(EXTRACT_DIR, "02_scripts_and_reports")

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


def decompose(mp: np.ndarray):
    n = len(mp)
    seen = np.zeros(n, dtype=np.uint8)
    out = []
    for s in range(n):
        if seen[s]:
            continue
        cyc = []
        cur = s
        while not seen[cur]:
            seen[cur] = 1
            cyc.append(int(cur))
            cur = int(mp[cur])
        out.append(cyc)
    return out


def cycle_type(mp: np.ndarray):
    return sorted([len(c) for c in decompose(mp)], reverse=True)


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


def power_map(mp: np.ndarray, r: int) -> np.ndarray:
    out = np.arange(len(mp), dtype=np.int64)
    for _ in range(r):
        out = mp[out]
    return out


def defect_offsets_formula(m: int, L: int):
    if m % 15 == 3:
        r = (m - 3) // 15
        if r % 3 != 2:
            raise ValueError("split branch only")
        expL = (5 * r + 2) // 3
        if L != expL:
            raise RuntimeError(("bad defect length", m, L, expL))
        return [0] + [(4 * r - 2) // 3] * ((r + 1) // 3) + [(4 * r + 1) // 3] * (L - 1 - (r + 1) // 3)
    if m % 15 == 9:
        r = (m - 9) // 15
        if r % 3 != 1:
            raise ValueError("split branch only")
        expL = (5 * r + 4) // 3
        if L != expL:
            raise RuntimeError(("bad defect length", m, L, expL))
        return [0] + [(r - 1) // 3] * ((4 * r + 2) // 3) + [(r + 2) // 3] * (L - 1 - (4 * r + 2) // 3)
    raise ValueError(("unsupported class", m))


def build_N_formula(m: int) -> np.ndarray:
    p = p_gen_arr(m)
    M = m // 3
    out = np.empty(M, dtype=np.int64)
    cycles = decompose(p)
    defect = [cyc for cyc in cycles if 1 in cyc][0]
    for cyc in cycles:
        if cyc is defect:
            continue
        L = len(cyc)
        rC = (m - 1) % L
        pr = power_map(p, rC)
        for u in cyc:
            out[u] = int(pr[u])
    h = defect.index(1)
    defect_rot = defect[h:] + defect[:h]
    offsets = defect_offsets_formula(m, len(defect_rot))
    for j, u in enumerate(defect_rot):
        out[u] = defect_rot[(j + offsets[j]) % len(defect_rot)]
    return out


def delta_formula(m: int) -> int:
    if m % 15 == 3:
        r = (m - 3) // 15
        return 3 * r + 2
    if m % 15 == 9:
        r = (m - 9) // 15
        return r + 2
    raise ValueError(("unsupported class", m))


def build_g_formula(m: int) -> np.ndarray:
    N = build_N_formula(m)
    M = m // 3
    return (N + delta_formula(m)) % M


def main() -> None:
    rows = []
    for m in range(33, 1502, 6):
        M = m // 3
        if m % 5 != 0 and M % 7 != 0 and m % 15 in (3, 9) and M % 3 == 2:
            g = build_g_formula(m)
            rows.append({
                "m": m,
                "M": M,
                "class": m % 15,
                "cycle_type_g": cycle_type(g),
                "single_cycle": len(decompose(g)) == 1,
            })
    single = [row for row in rows if row["single_cycle"]]
    report = {
        "title": "d=5 split-branch conjugacy attempt report",
        "scope": [
            "33<=m<=1501",
            "5∤m, 7∤M, m≡3 or 9 (mod 15), M≡2 (mod 3)",
            "Uses the March 27 explicit reduced-base theorem and March 28 split first-special-hit theorem.",
        ],
        "summary": {
            "total_moduli": len(rows),
            "single_cycle_count": len(single),
            "non_single_count": len(rows) - len(single),
        },
        "prime_counterexamples": [
            row for row in rows if row["m"] in (69, 123)
        ],
        "single_cycle_moduli": single,
        "head": rows[:12],
    }
    txt = Path("/mnt/data/d5_generic_late_split_componentwise_conjugacy_and_global_nogo_check_report_2026-03-28.txt")
    jsn = Path("/mnt/data/d5_generic_late_split_componentwise_conjugacy_and_global_nogo_check_report_2026-03-28.json")
    txt.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    jsn.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
