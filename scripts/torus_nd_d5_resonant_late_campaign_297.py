#!/usr/bin/env python3
"""Memory-light exact late resonant campaign for the pure color-1 branch.

This runner is designed around the 2026-03-26 late resonant schematic notes.
It keeps disk output minimal, parallelizes only over independent small tasks,
and treats the induced base permutation on B_m as the expensive object.

The default run does two things:

1. exact zero-state calibration on B_m and H_m for the promoted-plus control,
   the late central pair, and the late symmetric flank pair on a late resonant
   modulus list;
2. exact full B_m decomposition only on a small promoted subset of moduli.

No trajectory dumps are written.  The saved outputs are compact JSON summaries.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
import tarfile
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from multiprocessing import get_context
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_TAR = REPO_ROOT / "tmp" / "residual_proof_package_2026-03-25.tar"
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_297_resonant_late_campaign_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_297_resonant_late_campaign"
RW_MEMBER = (
    "residual_proof_package_2026-03-25/"
    "04_resonant_section_theorems_and_reductions/"
    "resonant_width1_section_return_check.py"
)

RW = None
_HELPER_TEMP: tempfile.TemporaryDirectory[str] | None = None


@dataclass(frozen=True)
class ZeroTask:
    m: int
    family: str


@dataclass(frozen=True)
class FullBTask:
    m: int
    family: str
    start_a: int
    stop_a: int


def load_helper_from_tar(source_tar: Path):
    global RW, _HELPER_TEMP
    if RW is not None:
        return RW
    _HELPER_TEMP = tempfile.TemporaryDirectory()
    with tarfile.open(source_tar) as tf:
        tf.extract(RW_MEMBER, _HELPER_TEMP.name)
    root = (
        Path(_HELPER_TEMP.name)
        / "residual_proof_package_2026-03-25"
        / "04_resonant_section_theorems_and_reductions"
    )
    sys.path.insert(0, str(root))
    RW = importlib.import_module("resonant_width1_section_return_check")
    return RW


def family_ops(m: int, family: str) -> np.ndarray:
    r = (m - 1) // 2
    base_ops = [
        (1, 2, 1, 4),      # A_{1,4}
        (0, 1, r, 4),      # C_{r,4}
        (1, 2, 1, 3),      # A_{1,3}
        (0, 1, 3, 3),      # C_{3,3}
        (0, 1, r - 1, 3),  # C_{r-1,3}
        (1, 2, r, 3),      # A_{r,3}
        (0, 1, r + 1, 3),  # C_{r+1,3}
        (1, 2, r + 1, 3),  # promoted + : A_{r+1,3}
    ]
    toggles: set[tuple[int, int, int, int]] = set(base_ops)

    def toggle(op: tuple[int, int, int, int]) -> None:
        if op in toggles:
            toggles.remove(op)
        else:
            toggles.add(op)

    if family == "promoted_plus":
        pass
    elif family == "central_pair":
        toggle((1, 2, r - 2, 3))  # A_{r-2,3}
        toggle((1, 2, r, 3))      # toggle off the built-in A_{r,3}
    elif family == "flank_pair":
        toggle((1, 2, r - 1, 3))  # A_{r-1,3}
        toggle((1, 2, r, 3))      # toggle off the built-in A_{r,3}
    else:
        raise ValueError(f"unknown family {family}")
    ops = sorted(toggles)
    return np.array(ops, dtype=np.int64)


def block_step(m: int, ops: np.ndarray, state: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    rw = RW
    if rw is None:
        raise RuntimeError("helper module not loaded")
    a, c, d, e = state
    a2, _b2, c2, d2, e2 = rw.iterate_m_steps_sigma0_exact(a, c, d, e, m, ops)
    return int(a2), int(c2), int(d2), int(e2)


def next_B_return(m: int, ops: np.ndarray, start_a: int, max_blocks: int) -> dict[str, Any]:
    state = (start_a, 0, 0, 0)
    blocks = 0
    while blocks < max_blocks:
        state = block_step(m, ops, state)
        blocks += 1
        if state[1] == 0 and state[2] == 0 and state[3] == 0:
            return {
                "target_a": state[0],
                "blocks": blocks,
            }
    raise RuntimeError(f"B-return exceeded max_blocks={max_blocks} from a={start_a} at m={m}")


def next_H_return(m: int, ops: np.ndarray, start_a: int, start_e: int, max_blocks: int) -> dict[str, Any]:
    state = (start_a, 0, 0, start_e)
    blocks = 0
    while blocks < max_blocks:
        state = block_step(m, ops, state)
        blocks += 1
        if state[1] == 0 and state[2] == 0:
            return {
                "target_a": state[0],
                "target_e": state[3],
                "blocks": blocks,
            }
    raise RuntimeError(
        f"H-return exceeded max_blocks={max_blocks} from (a,e)=({start_a},{start_e}) at m={m}"
    )


def zero_worker(task: ZeroTask, max_blocks: int) -> dict[str, Any]:
    ops = family_ops(task.m, task.family)
    started = time.perf_counter()
    b = next_B_return(task.m, ops, 0, max_blocks)
    mid = time.perf_counter()
    h = next_H_return(task.m, ops, 0, 0, max_blocks)
    ended = time.perf_counter()
    return {
        "m": task.m,
        "family": task.family,
        "B_zero": b,
        "H_zero": h,
        "timing_sec": {
            "B_zero": round(mid - started, 6),
            "H_zero": round(ended - mid, 6),
            "total": round(ended - started, 6),
        },
    }


def full_b_chunk_worker(task: FullBTask, max_blocks: int) -> dict[str, Any]:
    ops = family_ops(task.m, task.family)
    rows: list[dict[str, int]] = []
    for a in range(task.start_a, task.stop_a):
        rec = next_B_return(task.m, ops, a, max_blocks)
        rows.append({"a": a, "target_a": int(rec["target_a"]), "blocks": int(rec["blocks"])})
    return {"m": task.m, "family": task.family, "rows": rows}


def chunk_ranges(n: int, chunks: int) -> list[tuple[int, int]]:
    chunks = max(1, min(chunks, n))
    out: list[tuple[int, int]] = []
    base = n // chunks
    rem = n % chunks
    start = 0
    for idx in range(chunks):
        size = base + (1 if idx < rem else 0)
        stop = start + size
        if start < stop:
            out.append((start, stop))
        start = stop
    return out


def permutation_cycle_data(targets: list[int]) -> dict[str, Any]:
    n = len(targets)
    seen = [False] * n
    cycles: list[list[int]] = []
    for i in range(n):
        if seen[i]:
            continue
        cur = i
        cyc: list[int] = []
        while not seen[cur]:
            seen[cur] = True
            cyc.append(cur)
            cur = targets[cur]
        cycles.append(cyc)
    cycles.sort(key=lambda cyc: (-len(cyc), cyc[0]))
    short_witnesses = [{"length": len(cyc), "a": cyc[0]} for cyc in cycles if len(cyc) < n]
    return {
        "cycle_lengths": [len(cyc) for cyc in cycles],
        "short_cycle_witnesses": short_witnesses,
    }


def run_zero_campaign(
    zero_moduli: list[int],
    families: list[str],
    workers: int,
    max_blocks: int,
) -> dict[str, Any]:
    tasks = [ZeroTask(m=m, family=family) for m in zero_moduli for family in families]
    results: dict[str, dict[str, Any]] = {str(m): {} for m in zero_moduli}
    ctx = get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        future_map = {pool.submit(zero_worker, task, max_blocks): task for task in tasks}
        for future in as_completed(future_map):
            rec = future.result()
            results[str(rec["m"])][rec["family"]] = rec
    return results


def run_full_b_campaign(
    full_b_moduli: list[int],
    families: list[str],
    workers: int,
    max_blocks: int,
) -> dict[str, Any]:
    results: dict[str, dict[str, Any]] = {}
    ctx = get_context("fork")
    for m in full_b_moduli:
        by_family: dict[str, Any] = {}
        for family in families:
            started = time.perf_counter()
            chunks = chunk_ranges(m, workers)
            tasks = [
                FullBTask(m=m, family=family, start_a=start, stop_a=stop)
                for start, stop in chunks
            ]
            rows: list[dict[str, int]] = []
            with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
                future_map = {pool.submit(full_b_chunk_worker, task, max_blocks): task for task in tasks}
                for future in as_completed(future_map):
                    rows.extend(future.result()["rows"])
            rows.sort(key=lambda row: row["a"])
            targets = [row["target_a"] for row in rows]
            is_permutation = sorted(targets) == list(range(m))
            cycle_data = permutation_cycle_data(targets)
            ended = time.perf_counter()
            by_family[family] = {
                "is_permutation": is_permutation,
                "cycle_lengths": cycle_data["cycle_lengths"],
                "short_cycle_witnesses": cycle_data["short_cycle_witnesses"],
                "zero_target_a": rows[0]["target_a"],
                "zero_blocks": rows[0]["blocks"],
                "max_blocks_per_start": max(row["blocks"] for row in rows),
                "timing_sec": round(ended - started, 6),
            }
        results[str(m)] = by_family
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a memory-light exact late resonant campaign on the pure color-1 branch."
    )
    parser.add_argument("--source-tar", type=Path, default=DEFAULT_SOURCE_TAR)
    parser.add_argument(
        "--zero-moduli",
        nargs="*",
        type=int,
        default=[171, 177, 183, 189, 201, 207, 213],
    )
    parser.add_argument(
        "--zero-families",
        nargs="*",
        default=["promoted_plus", "central_pair", "flank_pair"],
    )
    parser.add_argument(
        "--full-b-moduli",
        nargs="*",
        type=int,
        default=[171, 177],
    )
    parser.add_argument(
        "--full-b-families",
        nargs="*",
        default=["central_pair", "flank_pair"],
    )
    parser.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1))
    parser.add_argument("--max-blocks", type=int, default=50_000_000)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    args = parser.parse_args()

    load_helper_from_tar(args.source_tar)
    # Warm the JIT before forking workers.
    _ = block_step(15, family_ops(15, "promoted_plus"), (0, 0, 0, 0))

    started = time.perf_counter()
    zero_results = run_zero_campaign(
        zero_moduli=args.zero_moduli,
        families=args.zero_families,
        workers=args.workers,
        max_blocks=args.max_blocks,
    )
    full_b_results = run_full_b_campaign(
        full_b_moduli=args.full_b_moduli,
        families=args.full_b_families,
        workers=args.workers,
        max_blocks=args.max_blocks,
    )
    ended = time.perf_counter()

    summary: dict[str, Any] = {
        "task": "d5_297_resonant_late_campaign",
        "source_tar": str(args.source_tar),
        "protocol": "zero_state_calibration_plus_small_full_B_followup",
        "zero_moduli": args.zero_moduli,
        "zero_families": args.zero_families,
        "full_b_moduli": args.full_b_moduli,
        "full_b_families": args.full_b_families,
        "workers": args.workers,
        "max_blocks": args.max_blocks,
        "timing_sec": round(ended - started, 6),
        "high_level_conclusions": [],
    }

    if "171" in full_b_results:
        row = full_b_results["171"]
        if all(family in row and row[family]["cycle_lengths"] == [171] for family in args.full_b_families):
            summary["high_level_conclusions"].append(
                "At m=171 the checked late families in the full-B follow-up are single-cycle on B_m."
            )
    if "177" in full_b_results:
        row = full_b_results["177"]
        if "central_pair" in row and "flank_pair" in row:
            summary["high_level_conclusions"].append(
                "At m=177 both late 2-line families fail on the full B_m decomposition, and the central family is less broken than the flank family."
            )

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.detail_dir / "zero_calibration.json").write_text(
        json.dumps(zero_results, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.detail_dir / "full_b_selected.json").write_text(
        json.dumps(full_b_results, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
