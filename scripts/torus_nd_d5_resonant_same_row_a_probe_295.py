#!/usr/bin/env python3
"""Probe explicit promoted-collar refinements on the resonant base permutation.

This script operationalizes the next-family narrowing suggested by the
2026-03-25 residual proof package:

- start from the promoted-collar control family;
- compare the opposite-collar ``A`` refinement directly;
- test whether a single extra ``B`` row already changes the reduced object.

The reduced score object is the base permutation P_m on B_m = {c = d = e = 0}
for the color-1 m-step section return on Sigma = 0.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import tarfile
import tempfile
from functools import lru_cache
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_TAR = REPO_ROOT / "tmp" / "residual_proof_package_2026-03-25.tar"
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_295_resonant_same_row_a_probe_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_295_resonant_same_row_a_probe"

RW_MEMBER = (
    "residual_proof_package_2026-03-25/"
    "04_resonant_section_theorems_and_reductions/"
    "resonant_width1_section_return_check.py"
)
W3_MEMBER = (
    "residual_proof_package_2026-03-25/"
    "04_resonant_section_theorems_and_reductions/"
    "resonant_width3_topcollar_transducer_check.py"
)


def load_package_helpers(source_tar: Path):
    tempdir = tempfile.TemporaryDirectory()
    with tarfile.open(source_tar) as tf:
        tf.extract(RW_MEMBER, tempdir.name)
        tf.extract(W3_MEMBER, tempdir.name)
    root = (
        Path(tempdir.name)
        / "residual_proof_package_2026-03-25"
        / "04_resonant_section_theorems_and_reductions"
    )
    sys.path.insert(0, str(root))
    rw = importlib.import_module("resonant_width1_section_return_check")
    w3 = importlib.import_module("resonant_width3_topcollar_transducer_check")
    return tempdir, rw, w3


def family_ops(w3, m: int, u: int, kind: str, t: int | None = None, s: int | None = None) -> np.ndarray:
    ops = w3.width3_ops(m).tolist()
    # The promoted-collar control is width-3 plus one collar-row A move.
    ops.append((1, 2, u, 3))
    if kind == "opposite_A":
        ops.append((1, 2, t, 3))
    elif kind == "B":
        ops.append((0, 2, s, 3))
    elif kind != "control":
        raise ValueError(f"unsupported kind: {kind}")
    return np.array(ops, dtype=np.int64)


def cycle_lengths(perm: list[int]) -> list[int]:
    n = len(perm)
    seen = [False] * n
    out: list[int] = []
    for i in range(n):
        if seen[i]:
            continue
        cur = i
        size = 0
        while not seen[cur]:
            seen[cur] = True
            cur = perm[cur]
            size += 1
        out.append(size)
    return sorted(out, reverse=True)


def compute_P_cycle_lengths(rw, m: int, ops: np.ndarray) -> list[int]:
    @lru_cache(maxsize=None)
    def block_map(state: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        a, c, d, e = state
        a, _b, c, d, e = rw.iterate_m_steps_sigma0_exact(a, c, d, e, m, ops)
        return (a, c, d, e)

    memo: dict[tuple[int, int, int, int], int] = {}

    def target_from(start: tuple[int, int, int, int]) -> int:
        path: list[tuple[int, int, int, int]] = []
        seen: set[tuple[int, int, int, int]] = set()
        cur = start
        while True:
            nxt = block_map(cur)
            if nxt[1] == 0 and nxt[2] == 0 and nxt[3] == 0:
                target = nxt[0]
                break
            if nxt in memo:
                target = memo[nxt]
                break
            if nxt in seen:
                raise RuntimeError(f"cycle without B-return from {start}: hit {nxt}")
            seen.add(nxt)
            path.append(nxt)
            cur = nxt
        for st in path:
            memo[st] = target
        memo[start] = target
        return target

    perm = [target_from((a, 0, 0, 0)) for a in range(m)]
    return cycle_lengths(perm)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Probe explicit promoted-collar refinements on the resonant base permutation."
    )
    parser.add_argument("--source-tar", type=Path, default=DEFAULT_SOURCE_TAR)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    parser.add_argument("--moduli", nargs="*", type=int, default=[21, 27, 33])
    parser.add_argument("--dualA-spotcheck-moduli", nargs="*", type=int, default=[39, 51])
    args = parser.parse_args()

    tempdir, rw, w3 = load_package_helpers(args.source_tar)
    del tempdir  # keep reference alive in local scope

    results: dict[str, object] = {
        "task": "d5_295_resonant_same_row_a_probe",
        "source_tar": str(args.source_tar),
        "checked_moduli": args.moduli,
        "families": {},
        "dualA_spotchecks": {},
    }

    for m in args.moduli:
        r = (m - 1) // 2
        by_sign: dict[str, object] = {}
        for sign in (-1, 1):
            u = (r + sign) % m
            control = compute_P_cycle_lengths(rw, m, family_ops(w3, m, u, "control"))
            opposite_row = (r - 1) if sign == 1 else (r + 1)
            opposite_row %= m
            opposite_row_a = compute_P_cycle_lengths(
                rw,
                m,
                family_ops(w3, m, u, "opposite_A", t=opposite_row),
            )
            b_scan: dict[str, list[int]] = {}
            for s in range(m):
                b_scan[str(s)] = compute_P_cycle_lengths(rw, m, family_ops(w3, m, u, "B", s=s))
            unique_b_types = sorted({tuple(v) for v in b_scan.values()}, key=lambda cyc: (len(cyc), cyc))
            by_sign[str(sign)] = {
                "u": u,
                "opposite_row": opposite_row,
                "control": control,
                "opposite_row_A": opposite_row_a,
                "single_B_unique_cycle_types": [list(cyc) for cyc in unique_b_types],
                "single_B_rows_by_cycle_type": {
                    json.dumps(list(cyc)): [int(s) for s, v in ((row, tuple(vals)) for row, vals in b_scan.items()) if v == cyc]
                    for cyc in unique_b_types
                },
            }
        results["families"][str(m)] = by_sign

    for m in args.dualA_spotcheck_moduli:
        r = (m - 1) // 2
        by_sign: dict[str, object] = {}
        for sign in (-1, 1):
            u = (r + sign) % m
            opposite_row = (r - 1) if sign == 1 else (r + 1)
            opposite_row %= m
            control = compute_P_cycle_lengths(rw, m, family_ops(w3, m, u, "control"))
            opposite_row_a = compute_P_cycle_lengths(
                rw,
                m,
                family_ops(w3, m, u, "opposite_A", t=opposite_row),
            )
            by_sign[str(sign)] = {
                "u": u,
                "opposite_row": opposite_row,
                "control": control,
                "opposite_row_A": opposite_row_a,
            }
        results["dualA_spotchecks"][str(m)] = by_sign

    conclusions = []
    all_single_B_inert = True
    opposite_A_changes = False
    opposite_A_solves_some_checked_modulus = False
    for m in args.moduli:
        for sign in ("-1", "1"):
            row = results["families"][str(m)][sign]
            unique_b_types = row["single_B_unique_cycle_types"]
            if len(unique_b_types) != 1 or unique_b_types[0] != row["control"]:
                all_single_B_inert = False
            if row["opposite_row_A"] != row["control"]:
                opposite_A_changes = True
            if len(row["opposite_row_A"]) == 1:
                opposite_A_solves_some_checked_modulus = True
    dualA_changes_on_spotchecks = True
    for m in args.dualA_spotcheck_moduli:
        for sign in ("-1", "1"):
            row = results["dualA_spotchecks"][str(m)][sign]
            if row["opposite_row_A"] == row["control"]:
                dualA_changes_on_spotchecks = False

    if all_single_B_inert:
        conclusions.append(
            "On the checked resonant moduli, adding a single extra B_{s,3} row to the promoted-collar control "
            "is inert at the level of the reduced base permutation P_m for every tested row s."
        )
    if opposite_A_changes:
        conclusions.append(
            "On the checked resonant moduli, adding the opposite collar-row A move changes P_m nontrivially "
            "relative to the promoted-collar control."
        )
    if opposite_A_solves_some_checked_modulus:
        conclusions.append(
            "In the checked range, the dual-collar A family already makes P_m a single cycle at m = 21."
        )
    if dualA_changes_on_spotchecks and args.dualA_spotcheck_moduli:
        spotchecks = ", ".join(str(m) for m in args.dualA_spotcheck_moduli)
        conclusions.append(
            f"Additional exact spot checks at m = {spotchecks} show that dual-collar A continues to change P_m "
            "nontrivially beyond the smallest checked moduli."
        )

    summary = {
        "task": results["task"],
        "source_tar": results["source_tar"],
        "checked_moduli": results["checked_moduli"],
        "dualA_spotcheck_moduli": args.dualA_spotcheck_moduli,
        "all_single_B_rows_inert": all_single_B_inert,
        "opposite_collar_A_changes_P_m": opposite_A_changes,
        "opposite_collar_A_solves_some_checked_modulus": opposite_A_solves_some_checked_modulus,
        "opposite_collar_A_changes_P_m_on_spotchecks": dualA_changes_on_spotchecks,
        "conclusions": conclusions,
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.detail_dir / "per_modulus.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
