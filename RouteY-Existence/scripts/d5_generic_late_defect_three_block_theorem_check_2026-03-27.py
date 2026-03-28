from __future__ import annotations

import json
import os
import sys
import tarfile
from functools import lru_cache
from typing import Dict, List, Tuple

import numpy as np

ARCHIVE = "/mnt/data/d5_consolidated_support_archive_2026-03-27.tar"
EXTRACT_ROOT = "/mnt/data/extract"
EXTRACT_DIR = os.path.join(EXTRACT_ROOT, "d5_consolidated_support_archive_2026-03-27")
SCRIPTS_DIR = os.path.join(EXTRACT_DIR, "02_scripts_and_reports")

REPORT_TXT = "/mnt/data/d5_generic_late_defect_three_block_theorem_check_report_2026-03-27.txt"
REPORT_JSON = "/mnt/data/d5_generic_late_defect_three_block_theorem_check_report_2026-03-27.json"


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
def special_hit_map(m: int, t: int = 4) -> np.ndarray:
    f, rho, spec = source_data(m, t)
    M = m // 3
    out = np.empty(M, dtype=np.int64)
    for u in range(M):
        A = 3 * u + 1
        Acur, ecur = audit.symbolic_next_return_compact(m, t, A, 0)
        n = 1
        while ecur != audit.special_row(m, Acur):
            Acur, ecur = audit.candidate_next_return(m, f, rho, spec, Acur, ecur)
            n += 1
            if n > 1_000_000:
                raise RuntimeError(("too many source steps", m, u))
        out[u] = (Acur - 1) // 3
    return out


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


def exact_offsets(m: int) -> List[int]:
    p = p_gen_arr(m)
    N = special_hit_map(m)
    defect_cycle = next(c for c in decompose(p) if 1 in c)
    h = defect_cycle.index(1)
    defect_cycle = defect_cycle[h:] + defect_cycle[:h]
    idx = {u: i for i, u in enumerate(defect_cycle)}
    return [(idx[int(N[u])] - r) % len(defect_cycle) for r, u in enumerate(defect_cycle)]


def cyclic_runs(values: List[int]) -> List[Tuple[int, int]]:
    if not values:
        return []
    runs: List[Tuple[int, int]] = []
    cur = values[0]
    cnt = 1
    for x in values[1:]:
        if x == cur:
            cnt += 1
        else:
            runs.append((int(cur), int(cnt)))
            cur = x
            cnt = 1
    runs.append((int(cur), int(cnt)))
    if len(runs) > 1 and runs[0][0] == runs[-1][0]:
        runs = [(runs[-1][0], runs[-1][1] + runs[0][1])] + runs[1:-1]
    return runs


def theorem_offsets(m: int) -> List[int]:
    if m % 15 not in (3, 9):
        raise ValueError(("wrong residue class", m))
    if m % 15 == 3:
        r = (m - 3) // 15
        if r % 3 == 2:
            L = (5 * r + 2) // 3
            out = [None] * L
            out[0] = 0
            v1 = (4 * r - 2) // 3
            for j in range(1, (r + 1) // 3 + 1):
                out[j] = v1
            v2 = (4 * r + 1) // 3
            for j in range((r + 4) // 3, L):
                out[j] = v2
        else:
            L = 5 * r + 1
            out = [None] * L
            out[0] = 3 * r
            for j in range(1, 2 * r - 1):
                out[j] = 3 * r + 2
            for j in range(2 * r - 1, 2 * r + 1):
                out[j] = r + 2
            for j in range(2 * r + 1, L):
                out[j] = 3 * r
    else:
        r = (m - 9) // 15
        if r % 3 == 1:
            L = (5 * r + 4) // 3
            out = [None] * L
            out[0] = 0
            v1 = (r - 1) // 3
            for j in range(1, (4 * r + 2) // 3 + 1):
                out[j] = v1
            v2 = (r + 2) // 3
            for j in range((4 * r + 5) // 3, L):
                out[j] = v2
        else:
            if r == 2:
                L = 13
                out = [None] * L
                out[0] = 0
                for j in range(1, 11):
                    out[j] = 2
                for j in range(11, 13):
                    out[j] = 3
            else:
                L = 5 * r + 3
                out = [None] * L
                out[0] = 3
                for j in range(1, 4 * r + 3):
                    out[j] = r
                for j in range(4 * r + 3, 5 * r):
                    out[j] = r + 4
                for j in range(5 * r, 5 * r + 3):
                    out[j] = 3
    assert all(v is not None for v in out)
    return [int(v) for v in out]


def case_label(m: int) -> str:
    if m % 15 == 3:
        r = (m - 3) // 15
        return f"15r+3/{'split' if r % 3 == 2 else 'unsplit'}"
    r = (m - 9) // 15
    if r == 2:
        return "15r+9/unsplit-edge"
    return f"15r+9/{'split' if r % 3 == 1 else 'unsplit'}"


def main() -> None:
    max_m = 1501
    moduli = [m for m in range(27, max_m + 1, 6) if m % 5 != 0 and m % 7 != 0 and m % 15 in (3, 9)]

    rows: List[Dict[str, object]] = []
    bad: List[Dict[str, object]] = []
    total_states = 0

    for m in moduli:
        ex = exact_offsets(m)
        th = theorem_offsets(m)
        total_states += len(ex)
        row = {
            "m": m,
            "M": m // 3,
            "case": case_label(m),
            "L": len(ex),
            "exact_runs": cyclic_runs(ex),
            "theorem_runs": cyclic_runs(th),
            "match": ex == th,
        }
        rows.append(row)
        if ex != th:
            row["exact_offsets"] = ex
            row["theorem_offsets"] = th
            bad.append(row)

    summary = {
        "scope": {
            "max_m": max_m,
            "conditions": ["m >= 27", "3|m", "5∤m", "7∤m", "m ≡ 3 or 9 (mod 15)"],
            "num_moduli": len(moduli),
            "total_defect_cycle_states": total_states,
        },
        "all_pass": len(bad) == 0,
        "num_bad": len(bad),
        "bad_rows": bad,
        "rows": rows,
    }

    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    lines: List[str] = []
    lines.append("Generic-late defect-cycle three-block theorem check")
    lines.append("")
    lines.append(f"Scope: 27 <= m <= {max_m}, 3|m, 5∤m, 7∤m, m ≡ 3 or 9 (mod 15)")
    lines.append(f"Moduli checked: {len(moduli)}")
    lines.append(f"Total defect-cycle states checked: {total_states}")
    lines.append(f"all_pass: {summary['all_pass']}")
    lines.append(f"num_bad: {len(bad)}")
    lines.append("")
    lines.append("Per modulus:")
    for row in rows:
        lines.append(
            f"m={row['m']}, M={row['M']}, case={row['case']}, L={row['L']}, "
            f"runs={row['exact_runs']}, match={row['match']}"
        )
    if bad:
        lines.append("")
        lines.append("Bad rows:")
        for row in bad:
            lines.append(json.dumps(row, ensure_ascii=False))

    with open(REPORT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
