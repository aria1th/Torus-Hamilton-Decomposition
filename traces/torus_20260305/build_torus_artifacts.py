#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import random
import statistics
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from torus_swap_search import (
    coords,
    cycle_count,
    objective,
    perm_sign,
    random_factorization,
    solve,
    swap_on_vertices,
    tau_cycles,
    verify_basic,
)


OUT_DIR = Path("artifacts/torus_20260305")
TRACE_DIR = OUT_DIR / "codex_swap_traces"
SOL_DIR = OUT_DIR / "hybrid_solutions"
BENCH_DIR = OUT_DIR / "bench"


def _is_hamilton(nexts: List[List[int]]) -> bool:
    return all(cycle_count(nexts[c]) == 1 for c in range(3))


def _canonical_nexts(m: int) -> List[List[int]]:
    n = m ** 3
    nexts = [[0] * n for _ in range(3)]
    for v in range(n):
        i, j, k = coords(v, m)
        nexts[0][v] = (( (i + 1) % m) * m + j) * m + k
        nexts[1][v] = (i * m + ((j + 1) % m)) * m + k
        nexts[2][v] = (i * m + j) * m + ((k + 1) % m)
    return nexts


def run_codex_swap_trace(m: int, seed: int = 0, max_steps: int = 200_000) -> Dict:
    """
    Reproduce the Codex alternating-cycle swap search from the direction-coloring start.
    Records accepted swaps with exact tau-cycle vertex set.
    """
    rng = random.Random(seed)
    nexts = _canonical_nexts(m)

    cycle_counts = [cycle_count(nexts[c]) for c in range(3)]
    cur_obj = sum(cc - 1 for cc in cycle_counts)
    accepted_swaps: List[Dict] = []

    for step in range(1, max_steps + 1):
        if all(cc == 1 for cc in cycle_counts):
            break

        c1, c2 = rng.sample((0, 1, 2), 2)
        tcycles = tau_cycles(nexts[c1], nexts[c2])
        verts = rng.choice(tcycles)

        old_heads1 = [nexts[c1][v] for v in verts]
        old_heads2 = [nexts[c2][v] for v in verts]

        old_obj = cur_obj
        old_cc = cycle_counts[:]

        swap_on_vertices(nexts, c1, c2, verts)
        new_cc = cycle_counts[:]
        new_cc[c1] = cycle_count(nexts[c1])
        new_cc[c2] = cycle_count(nexts[c2])
        new_obj = sum(cc - 1 for cc in new_cc)

        # Same annealed acceptance used in prior quick odd-case search.
        T = max(0.001, 1.0 - step / max_steps)
        accept = new_obj <= old_obj
        if (not accept) and T > 0:
            if rng.random() < math.exp((old_obj - new_obj) / (2.0 * T)):
                accept = True

        if accept:
            cycle_counts = new_cc
            cur_obj = new_obj
            accepted_swaps.append(
                {
                    "accepted_index": len(accepted_swaps) + 1,
                    "attempt_step": step,
                    "pair": [c1, c2],
                    "tau_cycle_len": len(verts),
                    "tau_cycle_vertices": [list(coords(v, m)) for v in verts],
                    "objective_before": old_obj,
                    "objective_after": new_obj,
                    "cycle_counts_before": old_cc,
                    "cycle_counts_after": new_cc,
                }
            )
        else:
            for idx, v in enumerate(verts):
                nexts[c1][v] = old_heads1[idx]
                nexts[c2][v] = old_heads2[idx]

    ok, msg = verify_basic(m, nexts)
    return {
        "m": m,
        "seed": seed,
        "max_steps": max_steps,
        "basic_verify": {"ok": ok, "msg": msg},
        "final_cycle_counts": [cycle_count(nexts[c]) for c in range(3)],
        "final_signs": [perm_sign(nexts[c]) for c in range(3)],
        "final_sign_product": perm_sign(nexts[0]) * perm_sign(nexts[1]) * perm_sign(nexts[2]),
        "hamilton_success": _is_hamilton(nexts),
        "accepted_swap_count": len(accepted_swaps),
        "accepted_swaps": accepted_swaps,
    }


def save_hybrid_solution(m: int, seed: int, restarts: int, steps: int, temp: float, out_path: Path) -> Dict:
    sol = solve(m, seed, restarts, steps, temp, verbose=False)
    if sol is None:
        raise RuntimeError(f"No solution object produced for m={m}")

    ok, msg = verify_basic(m, sol)
    cyc = [cycle_count(sol[c]) for c in range(3)]
    sgn = [perm_sign(sol[c]) for c in range(3)]
    payload = {
        "m": m,
        "seed": seed,
        "restarts": restarts,
        "steps": steps,
        "temp": temp,
        "basic_verify": {"ok": ok, "msg": msg},
        "cycle_counts": cyc,
        "signs": sgn,
        "sign_product": sgn[0] * sgn[1] * sgn[2],
        "hamilton_success": all(x == 1 for x in cyc),
        "nexts": sol,
    }
    out_path.write_text(json.dumps(payload, indent=2))
    return payload


def solve_hybrid_instrumented(
    m: int,
    seed: int,
    restarts: int,
    steps: int,
    temp: float,
) -> Dict:
    rng = random.Random(seed)
    n = m ** 3
    target_sign_prod = -1 if n % 2 == 0 else None

    t0 = time.perf_counter()
    starts_considered = 0
    starts_sign_rejected = 0
    swap_attempts = 0
    swap_accepted = 0

    best_obj = 10 ** 18
    best_cycles = None

    for restart_idx in range(1, restarts + 1):
        nexts = random_factorization(m, rng)
        if nexts is None:
            continue
        starts_considered += 1

        if target_sign_prod is not None:
            sp = perm_sign(nexts[0]) * perm_sign(nexts[1]) * perm_sign(nexts[2])
            if sp != target_sign_prod:
                starts_sign_rejected += 1
                continue

        cur_obj = objective(nexts)
        cur_cycles = [cycle_count(nexts[c]) for c in range(3)]
        if cur_obj < best_obj:
            best_obj = cur_obj
            best_cycles = cur_cycles[:]

        if _is_hamilton(nexts):
            return {
                "m": m,
                "seed": seed,
                "success": True,
                "restart_of_success": restart_idx,
                "step_of_success": 0,
                "runtime_sec": time.perf_counter() - t0,
                "swap_attempts": swap_attempts,
                "swap_accepted": swap_accepted,
                "starts_considered": starts_considered,
                "starts_sign_rejected": starts_sign_rejected,
                "best_obj": 0,
                "best_cycles": [1, 1, 1],
            }

        for step_idx in range(1, steps + 1):
            swap_attempts += 1

            cyc_counts = [cycle_count(nexts[c]) for c in range(3)]
            worst = max(range(3), key=lambda c: cyc_counts[c])
            other = rng.choice([c for c in range(3) if c != worst])
            c1, c2 = worst, other

            cycles = tau_cycles(nexts[c1], nexts[c2])
            verts = rng.choice(cycles)

            old1 = [nexts[c1][v] for v in verts]
            old2 = [nexts[c2][v] for v in verts]

            swap_on_vertices(nexts, c1, c2, verts)
            ok, _ = verify_basic(m, nexts)
            if not ok:
                for idx, v in enumerate(verts):
                    nexts[c1][v] = old1[idx]
                    nexts[c2][v] = old2[idx]
                continue

            new_obj = objective(nexts)
            old_obj = cur_obj
            accept = new_obj <= old_obj
            if (not accept) and temp > 0:
                if rng.random() < math.exp(-(new_obj - old_obj) / temp):
                    accept = True

            if accept:
                swap_accepted += 1
                cur_obj = new_obj
                cur_cycles = [cycle_count(nexts[c]) for c in range(3)]
                if cur_obj < best_obj:
                    best_obj = cur_obj
                    best_cycles = cur_cycles[:]
                if _is_hamilton(nexts):
                    return {
                        "m": m,
                        "seed": seed,
                        "success": True,
                        "restart_of_success": restart_idx,
                        "step_of_success": step_idx,
                        "runtime_sec": time.perf_counter() - t0,
                        "swap_attempts": swap_attempts,
                        "swap_accepted": swap_accepted,
                        "starts_considered": starts_considered,
                        "starts_sign_rejected": starts_sign_rejected,
                        "best_obj": 0,
                        "best_cycles": [1, 1, 1],
                    }
            else:
                for idx, v in enumerate(verts):
                    nexts[c1][v] = old1[idx]
                    nexts[c2][v] = old2[idx]

    return {
        "m": m,
        "seed": seed,
        "success": False,
        "restart_of_success": None,
        "step_of_success": None,
        "runtime_sec": time.perf_counter() - t0,
        "swap_attempts": swap_attempts,
        "swap_accepted": swap_accepted,
        "starts_considered": starts_considered,
        "starts_sign_rejected": starts_sign_rejected,
        "best_obj": best_obj,
        "best_cycles": best_cycles,
    }


def median_or_none(vals: List[float]) -> Optional[float]:
    return statistics.median(vals) if vals else None


def mean_or_none(vals: List[float]) -> Optional[float]:
    return statistics.mean(vals) if vals else None


def run_bench() -> Tuple[List[Dict], List[Dict]]:
    # Chosen to finish quickly while still giving comparative data.
    m_values = list(range(3, 11))  # 3..10
    seeds = list(range(3))
    restarts = 30
    steps = 3000
    temp = 0.2

    raw_rows: List[Dict] = []
    summary_rows: List[Dict] = []

    for m in m_values:
        per_m = []
        for seed in seeds:
            row = solve_hybrid_instrumented(m=m, seed=seed, restarts=restarts, steps=steps, temp=temp)
            raw_rows.append(row)
            per_m.append(row)

        successes = [r for r in per_m if r["success"]]
        summary = {
            "m": m,
            "trials": len(per_m),
            "successes": len(successes),
            "success_rate": len(successes) / len(per_m),
            "median_runtime_sec": median_or_none([r["runtime_sec"] for r in successes]),
            "mean_runtime_sec": mean_or_none([r["runtime_sec"] for r in successes]),
            "median_step_of_success": median_or_none([r["step_of_success"] for r in successes if r["step_of_success"] is not None]),
            "mean_step_of_success": mean_or_none([r["step_of_success"] for r in successes if r["step_of_success"] is not None]),
            "median_restart_of_success": median_or_none([r["restart_of_success"] for r in successes if r["restart_of_success"] is not None]),
            "mean_restart_of_success": mean_or_none([r["restart_of_success"] for r in successes if r["restart_of_success"] is not None]),
            "median_swaps_accepted": median_or_none([r["swap_accepted"] for r in successes]),
            "mean_swaps_accepted": mean_or_none([r["swap_accepted"] for r in successes]),
        }
        summary_rows.append(summary)

    return raw_rows, summary_rows


def write_bench_outputs(raw_rows: List[Dict], summary_rows: List[Dict]) -> None:
    (BENCH_DIR / "hybrid_bench_raw.json").write_text(json.dumps(raw_rows, indent=2))
    (BENCH_DIR / "hybrid_bench_summary.json").write_text(json.dumps(summary_rows, indent=2))

    with (BENCH_DIR / "hybrid_bench_summary.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    # Human-readable markdown table
    lines = []
    lines.append("# Hybrid Solver Performance Summary")
    lines.append("")
    lines.append("Config: m=3..10, 3 seeds each, restarts=30, steps=3000, temp=0.2")
    lines.append("")
    lines.append("| m | success/trials | median runtime (s) | median accepted swaps | median restart | median step |")
    lines.append("|---:|---:|---:|---:|---:|---:|")
    for row in summary_rows:
        succ = f"{row['successes']}/{row['trials']}"
        lines.append(
            "| {m} | {succ} | {rt} | {sw} | {rr} | {st} |".format(
                m=row["m"],
                succ=succ,
                rt=("-" if row["median_runtime_sec"] is None else f"{row['median_runtime_sec']:.4f}"),
                sw=("-" if row["median_swaps_accepted"] is None else f"{row['median_swaps_accepted']:.1f}"),
                rr=("-" if row["median_restart_of_success"] is None else f"{row['median_restart_of_success']:.1f}"),
                st=("-" if row["median_step_of_success"] is None else f"{row['median_step_of_success']:.1f}"),
            )
        )
    (BENCH_DIR / "hybrid_bench_summary.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    SOL_DIR.mkdir(parents=True, exist_ok=True)
    BENCH_DIR.mkdir(parents=True, exist_ok=True)

    manifest: Dict = {
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "codex_swap_traces": [],
        "hybrid_solutions": [],
        "bench": {},
    }

    # 1) Codex swap traces for odd quick cases.
    for m in (3, 5, 7, 9):
        trace = run_codex_swap_trace(m=m, seed=0, max_steps=200_000)
        out_path = TRACE_DIR / f"codex_swap_trace_m{m}_seed0.json"
        out_path.write_text(json.dumps(trace, indent=2))
        manifest["codex_swap_traces"].append(
            {
                "m": m,
                "path": str(out_path),
                "hamilton_success": trace["hamilton_success"],
                "accepted_swap_count": trace["accepted_swap_count"],
                "final_cycle_counts": trace["final_cycle_counts"],
            }
        )

    # 2) Save requested hybrid solutions.
    params = {
        4: dict(seed=0, restarts=200, steps=20_000, temp=0.2),
        6: dict(seed=0, restarts=300, steps=30_000, temp=0.3),
        9: dict(seed=0, restarts=200, steps=20_000, temp=0.2),
    }
    for m in (4, 6, 9):
        p = params[m]
        out_path = SOL_DIR / f"hybrid_solution_m{m}_seed{p['seed']}.json"
        payload = save_hybrid_solution(m=m, out_path=out_path, **p)
        manifest["hybrid_solutions"].append(
            {
                "m": m,
                "path": str(out_path),
                "hamilton_success": payload["hamilton_success"],
                "cycle_counts": payload["cycle_counts"],
                "sign_product": payload["sign_product"],
            }
        )

    # 3) Benchmark summary.
    raw_rows, summary_rows = run_bench()
    write_bench_outputs(raw_rows, summary_rows)
    manifest["bench"] = {
        "summary_json": str(BENCH_DIR / "hybrid_bench_summary.json"),
        "summary_csv": str(BENCH_DIR / "hybrid_bench_summary.csv"),
        "summary_md": str(BENCH_DIR / "hybrid_bench_summary.md"),
        "raw_json": str(BENCH_DIR / "hybrid_bench_raw.json"),
    }

    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))

    readme = """# Torus Artifact Bundle

Contents:
- `codex_swap_traces/`: accepted swap sequences for Codex-style alternating-cycle search from canonical direction-coloring start for m=3,5,7,9.
- `hybrid_solutions/`: full solution JSON files for m=4,6,9 from `torus_swap_search.py`-style hybrid solver.
- `bench/`: hybrid solver performance summary (m=3..12, 5 seeds each; restarts=80, steps=8000, temp=0.2).
- `manifest.json`: top-level index.

Notes:
- In swap trace files, `pair=[r,s]` are swapped colors.
- `tau_cycle_vertices` is the exact vertex set used for that accepted swap, in coordinate form `[i,j,k]`.
"""
    (OUT_DIR / "README.md").write_text(readme)


if __name__ == "__main__":
    main()
