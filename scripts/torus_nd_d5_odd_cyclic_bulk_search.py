#!/usr/bin/env python3
"""Search a restricted odd-d=5 cyclic-bulk family for Hamiltonian witnesses."""

from __future__ import annotations

import argparse
import os
import heapq
import json
import random
import time
from concurrent.futures import ProcessPoolExecutor
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from torus_nd_d5_odd_cyclic_bulk_family import (
    DIM,
    GATE_CATALOG,
    SIGMA_INV,
    all_five_cycle_permutations,
    all_layer0_permutations,
    config_key,
    config_name,
    config_with_layer_gates,
    gate_pair_name,
    permutation_name,
    random_gate_sequence,
    single_gate_options,
)
from torus_nd_d5_odd_cyclic_bulk_validate import validate_config
from torus_nd_validate import validate_rule

try:
    from rich.console import Console
    from rich.progress import track
except ImportError:  # pragma: no cover - optional dependency
    Console = None
    track = None

ConfigDict = Dict[str, object]


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _iter_progress(values: Iterable, *, description: str, use_rich: bool, total: int | None = None):
    if use_rich and track is not None:
        return track(values, description=description, total=total)
    return values


def _rich_available_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def _score_key(stats: Dict[str, object]) -> Tuple[int, int, int]:
    hamilton_colors = int(stats["hamilton_colors"])
    total_cycles = int(stats["total_cycle_count"])
    sign_product = int(stats["sign_product"])
    return (hamilton_colors, -total_cycles, sign_product)


def _heap_entry(stats: Dict[str, object], config: ConfigDict) -> Tuple[Tuple[int, int, int], str, Dict[str, object]]:
    return (_score_key(stats), config_key(config), {"config": config, "stats": stats})


def _resolve_jobs(jobs: int) -> int:
    if jobs > 0:
        return jobs
    return max(1, min(8, os.cpu_count() or 1))


def _layer0_family_permutations(family_name: str) -> List[Tuple[int, ...]]:
    if family_name == "sigma_inv_only":
        return [SIGMA_INV]
    if family_name == "five_cycle":
        return all_five_cycle_permutations()
    if family_name == "all":
        return all_layer0_permutations()
    raise ValueError(f"Unknown layer0 family {family_name}")


def evaluate_config(config: ConfigDict, m: int) -> Dict[str, object]:
    rule = build_rule_for_m(config, m)
    report = validate_rule(DIM, m, rule)
    color_cycle_counts = [int(stat["cycle_count"]) for stat in report["color_stats"]]
    hamilton_colors = sum(1 for stat in report["color_stats"] if stat["is_hamilton"])
    return {
        "m": m,
        "all_hamilton": bool(report["all_hamilton"]),
        "sign_product": int(report["sign_product"]),
        "color_cycle_counts": color_cycle_counts,
        "hamilton_colors": hamilton_colors,
        "total_cycle_count": sum(color_cycle_counts),
    }


def build_rule_for_m(config: ConfigDict, m: int):
    from torus_nd_d5_odd_cyclic_bulk_family import build_rule

    return build_rule(config, m)


def _evaluate_worker(payload: Tuple[ConfigDict, int]) -> Tuple[ConfigDict, Dict[str, object]]:
    config, m = payload
    return config, evaluate_config(config, m)


def _evaluate_configs(
    configs: Sequence[ConfigDict],
    *,
    m: int,
    jobs: int,
    use_rich: bool,
    description: str,
):
    total = len(configs)
    if jobs <= 1:
        for config in _iter_progress(configs, description=description, use_rich=use_rich, total=total):
            yield config, evaluate_config(config, m)
        return

    with ProcessPoolExecutor(max_workers=jobs) as executor:
        iterator = executor.map(_evaluate_worker, ((config, m) for config in configs), chunksize=64)
        iterator = _iter_progress(iterator, description=description, use_rich=use_rich, total=total)
        for config, stats in iterator:
            yield config, stats


def evaluate_and_record(
    config: ConfigDict,
    *,
    m: int,
    phase_name: str,
    top_heap: List[Tuple[Tuple[int, int, int], str, Dict[str, object]]],
    top_k: int,
    best_records: List[Dict[str, object]],
    best_score_ref: List[Tuple[int, int, int] | None],
) -> Dict[str, object]:
    stats = evaluate_config(config, m)
    payload = {
        "phase": phase_name,
        "config_name": config_name(config),
        "config": config,
        "stats": stats,
    }
    score = _score_key(stats)
    if best_score_ref[0] is None or score > best_score_ref[0]:
        best_score_ref[0] = score
        best_records.append(payload)

    entry = _heap_entry(stats, config)
    if len(top_heap) < top_k:
        heapq.heappush(top_heap, entry)
    elif entry > top_heap[0]:
        heapq.heapreplace(top_heap, entry)
    return payload


def exhaustive_single_gate_phase(
    *,
    m: int,
    top_k: int,
    layer0_family: str,
    jobs: int,
    use_rich: bool,
) -> Dict[str, object]:
    start = time.perf_counter()
    top_heap: List[Tuple[Tuple[int, int, int], str, Dict[str, object]]] = []
    best_records: List[Dict[str, object]] = []
    best_score_ref: List[Tuple[int, int, int] | None] = [None]
    evaluated = 0
    full_witnesses = []
    gate_options = single_gate_options()
    layer0_permutations = _layer0_family_permutations(layer0_family)
    configs = [
        config_with_layer_gates(
            layer0_q0,
            {
                1: gates1,
                2: gates2,
                3: gates3,
            },
        )
        for layer0_q0 in layer0_permutations
        for gates1 in gate_options
        for gates2 in gate_options
        for gates3 in gate_options
    ]

    for config, stats in _evaluate_configs(
        configs,
        m=m,
        jobs=jobs,
        use_rich=use_rich,
        description="Exhaustive single-gate phase",
    ):
        payload = {
            "phase": "exhaustive_single_gate",
            "config_name": config_name(config),
            "config": config,
            "stats": stats,
        }
        score = _score_key(stats)
        if best_score_ref[0] is None or score > best_score_ref[0]:
            best_score_ref[0] = score
            best_records.append(payload)
        entry = _heap_entry(stats, config)
        if len(top_heap) < top_k:
            heapq.heappush(top_heap, entry)
        elif entry > top_heap[0]:
            heapq.heapreplace(top_heap, entry)
        evaluated += 1
        if payload["stats"]["all_hamilton"]:
            full_witnesses.append(payload)

    top_candidates = [entry[2] for entry in sorted(top_heap, reverse=True)]
    return {
        "phase": "exhaustive_single_gate",
        "m": m,
        "layer0_family": layer0_family,
        "layer0_family_size": len(layer0_permutations),
        "evaluated_count": evaluated,
        "runtime_sec": time.perf_counter() - start,
        "full_witness_count": len(full_witnesses),
        "full_witnesses": full_witnesses[: min(20, len(full_witnesses))],
        "best_records": best_records,
        "top_candidates": top_candidates,
    }


def random_double_gate_phase(
    *,
    m: int,
    top_k: int,
    sample_count: int,
    seed: int,
    layer0_family: str,
    jobs: int,
    use_rich: bool,
) -> Dict[str, object]:
    start = time.perf_counter()
    rng = random.Random(seed)
    top_heap: List[Tuple[Tuple[int, int, int], str, Dict[str, object]]] = []
    best_records: List[Dict[str, object]] = []
    best_score_ref: List[Tuple[int, int, int] | None] = [None]
    full_witnesses = []
    layer0_permutations = _layer0_family_permutations(layer0_family)
    configs = []
    seen = set()

    for index in range(sample_count):
        if index == 0:
            layer0_q0 = SIGMA_INV
        else:
            layer0_q0 = rng.choice(layer0_permutations)
        config = config_with_layer_gates(
            layer0_q0,
            {
                1: random_gate_sequence(rng, 2),
                2: random_gate_sequence(rng, 2),
                3: random_gate_sequence(rng, 2),
            },
        )
        key = config_key(config)
        if key in seen:
            continue
        seen.add(key)
        configs.append(config)

    for config, stats in _evaluate_configs(
        configs,
        m=m,
        jobs=jobs,
        use_rich=use_rich,
        description="Random double-gate phase",
    ):
        payload = {
            "phase": "random_double_gate",
            "config_name": config_name(config),
            "config": config,
            "stats": stats,
        }
        score = _score_key(stats)
        if best_score_ref[0] is None or score > best_score_ref[0]:
            best_score_ref[0] = score
            best_records.append(payload)
        entry = _heap_entry(stats, config)
        if len(top_heap) < top_k:
            heapq.heappush(top_heap, entry)
        elif entry > top_heap[0]:
            heapq.heapreplace(top_heap, entry)
        if payload["stats"]["all_hamilton"]:
            full_witnesses.append(payload)

    top_candidates = [entry[2] for entry in sorted(top_heap, reverse=True)]
    return {
        "phase": "random_double_gate",
        "m": m,
        "layer0_family": layer0_family,
        "layer0_family_size": len(layer0_permutations),
        "sample_count": sample_count,
        "seed": seed,
        "evaluated_unique_count": len(seen),
        "runtime_sec": time.perf_counter() - start,
        "full_witness_count": len(full_witnesses),
        "full_witnesses": full_witnesses[: min(20, len(full_witnesses))],
        "best_records": best_records,
        "top_candidates": top_candidates,
    }


def _dedupe_candidates(candidates: Sequence[Dict[str, object]]) -> List[ConfigDict]:
    seen = set()
    out = []
    for item in candidates:
        config = item["config"]
        key = config_key(config)
        if key in seen:
            continue
        seen.add(key)
        out.append(config)
    return out


def multi_m_filter(
    configs: Sequence[ConfigDict],
    *,
    m_values: Sequence[int],
    top_k: int,
    use_rich: bool,
) -> List[Dict[str, object]]:
    survivors = []
    iterable = _iter_progress(configs, description="Multi-m filter", use_rich=use_rich)
    for config in iterable:
        per_m = []
        keep = True
        for m in m_values:
            stats = evaluate_config(config, m)
            per_m.append(stats)
            if stats["hamilton_colors"] == 0:
                keep = False
                break
        if not keep:
            continue
        aggregate_score = tuple(sum(item[key] for item in per_m) for key in ("hamilton_colors",))
        survivors.append(
            {
                "config_name": config_name(config),
                "config": config,
                "per_m": per_m,
                "aggregate_score": aggregate_score,
            }
        )
    survivors.sort(
        key=lambda item: (
            sum(stats["hamilton_colors"] for stats in item["per_m"]),
            -sum(stats["total_cycle_count"] for stats in item["per_m"]),
        ),
        reverse=True,
    )
    return survivors[:top_k]


def run_search(
    *,
    stage1_m: int,
    later_m_values: Sequence[int],
    top_k: int,
    random_samples: int,
    random_seed: int,
    layer0_family: str,
    jobs: int,
    use_rich: bool,
) -> Dict[str, object]:
    start = time.perf_counter()
    jobs = _resolve_jobs(jobs)
    exhaustive = exhaustive_single_gate_phase(
        m=stage1_m,
        top_k=top_k,
        layer0_family=layer0_family,
        jobs=jobs,
        use_rich=use_rich,
    )
    random_phase = random_double_gate_phase(
        m=stage1_m,
        top_k=top_k,
        sample_count=random_samples,
        seed=random_seed,
        layer0_family=layer0_family,
        jobs=jobs,
        use_rich=use_rich,
    )
    candidate_pool = _dedupe_candidates(exhaustive["top_candidates"] + random_phase["top_candidates"])
    filtered = multi_m_filter(candidate_pool, m_values=later_m_values, top_k=top_k, use_rich=use_rich)

    best_config = None
    best_validation = None
    selection_reason = "none"
    if filtered:
        best_config = filtered[0]["config"]
        selection_reason = "filtered_best"
        best_validation = validate_config(best_config, [stage1_m, *later_m_values])
    elif candidate_pool:
        best_config = max(
            candidate_pool,
            key=lambda config: _score_key(evaluate_config(config, stage1_m)),
        )
        selection_reason = "stage1_fallback"
        best_validation = validate_config(best_config, [stage1_m, *later_m_values])

    return {
        "task_id": "D5-ODD-CYCLIC-BULK-001",
        "family": {
            "name": "d5_odd_cyclic_bulk_rotating_zero_swaps_v1",
            "dim": DIM,
            "layer0_default_q_nonzero": [1, 2, 3, 4, 0],
            "layers_1_3_default": [0, 1, 2, 3, 4],
            "layers_ge_4_default": [0, 1, 2, 3, 4],
            "layer0_q0_family": layer0_family,
            "layer0_q0_permutation_count": len(_layer0_family_permutations(layer0_family)),
            "gate_catalog": [gate_pair_name(pair) for pair in GATE_CATALOG],
            "gate_description": "for each zero coordinate x_r=0, apply the selected slot-swap after shifting both slots by r",
        },
        "search_parameters": {
            "stage1_m": stage1_m,
            "later_m_values": list(later_m_values),
            "top_k": top_k,
            "random_samples": random_samples,
            "random_seed": random_seed,
            "jobs": jobs,
        },
        "environment": {
            "rich_version": _rich_available_version(),
        },
        "runtime_sec": time.perf_counter() - start,
        "phases": {
            "exhaustive_single_gate": exhaustive,
            "random_double_gate": random_phase,
        },
        "filtered_candidates": filtered,
        "selected_config": best_config,
        "selection_reason": selection_reason,
        "selected_validation": best_validation,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            "exhaustive_single_gate: "
            f"{summary['phases']['exhaustive_single_gate']['evaluated_count']} configs, "
            f"{summary['phases']['exhaustive_single_gate']['full_witness_count']} witnesses at m="
            f"{summary['search_parameters']['stage1_m']} "
            f"({summary['phases']['exhaustive_single_gate']['layer0_family']} family)"
        ),
        (
            "random_double_gate: "
            f"{summary['phases']['random_double_gate']['evaluated_unique_count']} unique configs, "
            f"{summary['phases']['random_double_gate']['full_witness_count']} witnesses at m="
            f"{summary['search_parameters']['stage1_m']}"
        ),
        f"filtered_candidates: {len(summary['filtered_candidates'])}",
        f"selected_config: {config_name(summary['selected_config']) if summary['selected_config'] else 'none'}",
    ]
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the restricted odd-d=5 cyclic-bulk family.")
    parser.add_argument("--stage1-m", type=int, default=3, help="initial exact-search modulus")
    parser.add_argument("--later-m-list", default="5,7", help="comma-separated later moduli for filtering")
    parser.add_argument("--top-k", type=int, default=25, help="number of leading candidates to keep per phase")
    parser.add_argument(
        "--random-samples",
        type=int,
        default=5000,
        help="number of seeded random double-gate samples to evaluate",
    )
    parser.add_argument("--random-seed", type=int, default=12345, help="seed for random double-gate phase")
    parser.add_argument(
        "--layer0-family",
        choices=("five_cycle", "all", "sigma_inv_only"),
        default="five_cycle",
        help="family for the special layer-0 q=0 permutation",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=0,
        help="worker count for search phases; 0 means auto",
    )
    parser.add_argument("--out", type=Path, help="write machine-readable summary JSON to this path")
    parser.add_argument("--best-config-out", type=Path, help="write selected best config JSON to this path")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich progress output")
    args = parser.parse_args(argv)

    use_rich = not args.no_rich and Console is not None and track is not None
    summary = run_search(
        stage1_m=args.stage1_m,
        later_m_values=_parse_m_list(args.later_m_list),
        top_k=args.top_k,
        random_samples=args.random_samples,
        random_seed=args.random_seed,
        layer0_family=args.layer0_family,
        jobs=args.jobs,
        use_rich=use_rich,
    )

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2))

    if args.best_config_out is not None and summary["selected_config"] is not None:
        args.best_config_out.parent.mkdir(parents=True, exist_ok=True)
        args.best_config_out.write_text(json.dumps(summary["selected_config"], indent=2))

    _print_summary(summary, use_rich=use_rich)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
