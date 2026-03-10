#!/usr/bin/env python3
"""Search fresh cyclic q-clock / v-fiber families for d=5 on the reduced state space."""

from __future__ import annotations

import argparse
import heapq
import json
import os
import platform
import random
import time
from concurrent.futures import ProcessPoolExecutor
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from torus_nd_d5_fresh_cyclic_qclock_family import (
    PILOT_M_VALUES,
    STABILITY_M_VALUES,
    OUTPUT_OFFSETS,
    TASK_ID,
    CandidateSpec,
    Clause,
    LayerSpec,
    action_catalog_one_clause_default0,
    all_clauses,
    analyze_candidate_for_modulus,
    candidate_key,
    candidate_name,
    default_candidate,
    dominates,
    make_candidate_spec,
    make_layer_spec,
    objective_vector,
    serialize_candidate,
    total_clause_count,
)

try:
    from rich.console import Console
    from rich.progress import track
except ImportError:  # pragma: no cover - optional dependency
    Console = None
    track = None

SummaryDict = Dict[str, object]


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _rich_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def _iter_progress(values: Iterable, *, description: str, use_rich: bool, total: int | None = None):
    if use_rich and track is not None:
        return track(values, description=description, total=total)
    return values


def _resolve_jobs(jobs: int) -> int:
    if jobs > 0:
        return jobs
    return max(1, min(8, os.cpu_count() or 1))


def _score_tuple(summary: SummaryDict) -> Tuple[int, ...]:
    return tuple(int(value) for value in summary["objective"])


def _summary_from_per_m(spec: CandidateSpec, per_m: Sequence[Dict[str, object]], phase: str) -> SummaryDict:
    return {
        "phase": phase,
        "candidate_name": candidate_name(spec),
        "candidate": serialize_candidate(spec),
        "objective": list(objective_vector(per_m, spec)),
        "per_m": list(per_m),
        "total_clauses": total_clause_count(spec),
    }


def _evaluate_candidate(spec: CandidateSpec, m_values: Sequence[int], phase: str) -> SummaryDict:
    per_m = [analyze_candidate_for_modulus(spec, m) for m in m_values]
    return _summary_from_per_m(spec, per_m, phase)


def _heap_entry(summary: SummaryDict) -> Tuple[Tuple[int, ...], str, SummaryDict]:
    spec = summary["candidate"]
    return (_score_tuple(summary), json.dumps(spec, sort_keys=True), summary)


def _trim_top_heap(top_heap: List[Tuple[Tuple[int, ...], str, SummaryDict]], summary: SummaryDict, top_k: int) -> None:
    entry = _heap_entry(summary)
    if len(top_heap) < top_k:
        heapq.heappush(top_heap, entry)
    elif entry > top_heap[0]:
        heapq.heapreplace(top_heap, entry)


def _merge_frontier(frontier: Dict[str, SummaryDict], summary: SummaryDict) -> bool:
    key = json.dumps(summary["candidate"], sort_keys=True)
    score = _score_tuple(summary)
    for other_key, other in list(frontier.items()):
        other_score = _score_tuple(other)
        if dominates(other_score, score):
            return False
        if dominates(score, other_score):
            frontier.pop(other_key)
    frontier[key] = summary
    return True


def _phase1_worker(
    layer1_spec: LayerSpec,
    layer_action_catalog: Sequence[LayerSpec],
    m_value: int,
    top_k: int,
) -> Dict[str, object]:
    local_top: List[Tuple[Tuple[int, ...], str, SummaryDict]] = []
    improving_history: List[SummaryDict] = []
    best_score: Tuple[int, ...] | None = None
    evaluated = 0
    for layer2_spec in layer_action_catalog:
        for layer3_spec in layer_action_catalog:
            spec = make_candidate_spec((layer1_spec, layer2_spec, layer3_spec))
            summary = _evaluate_candidate(spec, [m_value], "phase1_one_clause_default0")
            _trim_top_heap(local_top, summary, top_k)
            score = _score_tuple(summary)
            if best_score is None or score > best_score:
                best_score = score
                improving_history.append(summary)
            evaluated += 1
    return {
        "evaluated": evaluated,
        "top": [entry[2] for entry in sorted(local_top, reverse=True)],
        "improving_history": improving_history,
    }


def run_phase1(
    *,
    m_value: int,
    top_k: int,
    jobs: int,
    use_rich: bool,
) -> Dict[str, object]:
    start = time.perf_counter()
    layer_action_catalog = action_catalog_one_clause_default0()
    local_results = []
    iterator = layer_action_catalog
    if jobs <= 1:
        iterable = _iter_progress(iterator, description="Phase 1 exhaustive", use_rich=use_rich, total=len(layer_action_catalog))
        for layer1_spec in iterable:
            local_results.append(_phase1_worker(layer1_spec, layer_action_catalog, m_value, top_k))
    else:
        with ProcessPoolExecutor(max_workers=jobs) as executor:
            mapped = executor.map(
                _phase1_worker,
                layer_action_catalog,
                [layer_action_catalog] * len(layer_action_catalog),
                [m_value] * len(layer_action_catalog),
                [top_k] * len(layer_action_catalog),
                chunksize=1,
            )
            mapped = _iter_progress(mapped, description="Phase 1 exhaustive", use_rich=use_rich, total=len(layer_action_catalog))
            local_results.extend(mapped)

    merged_top: List[Tuple[Tuple[int, ...], str, SummaryDict]] = []
    merged_improving: List[SummaryDict] = []
    evaluated = 0
    for item in local_results:
        evaluated += int(item["evaluated"])
        for summary in item["top"]:
            _trim_top_heap(merged_top, summary, top_k)
        merged_improving.extend(item["improving_history"])
    merged_improving.sort(key=_score_tuple, reverse=True)
    return {
        "phase": "phase1_one_clause_default0",
        "m": m_value,
        "evaluated_count": evaluated,
        "action_catalog_size": len(layer_action_catalog),
        "runtime_sec": time.perf_counter() - start,
        "top_candidates": [entry[2] for entry in sorted(merged_top, reverse=True)],
        "improving_history": merged_improving[:top_k],
    }


def _random_clause(rng: random.Random, default_offset: int) -> Clause:
    while True:
        clause = rng.choice(all_clauses())
        if clause[2] != default_offset:
            return clause


def _normalize_layer_spec(default_offset: int, clauses: Sequence[Clause], max_clauses: int) -> LayerSpec:
    deduped: List[Clause] = []
    seen = set()
    for clause in clauses:
        if clause[2] == default_offset:
            continue
        if clause in seen:
            continue
        seen.add(clause)
        deduped.append(clause)
    return make_layer_spec(default_offset, tuple(deduped[:max_clauses]))


def mutate_candidate(spec: CandidateSpec, rng: random.Random, max_clauses: int) -> CandidateSpec:
    layers = [[layer_spec[0], list(layer_spec[1])] for layer_spec in spec]
    layer_index = rng.randrange(3)
    default_offset, clauses = layers[layer_index]
    operation = rng.choice(("change_default", "add_clause", "replace_clause", "remove_clause", "swap_clauses"))

    if operation == "change_default":
        default_offset = rng.choice(OUTPUT_OFFSETS)
    elif operation == "add_clause" and len(clauses) < max_clauses:
        insert_at = rng.randint(0, len(clauses))
        clauses.insert(insert_at, _random_clause(rng, default_offset))
    elif operation == "replace_clause" and clauses:
        clauses[rng.randrange(len(clauses))] = _random_clause(rng, default_offset)
    elif operation == "remove_clause" and clauses:
        clauses.pop(rng.randrange(len(clauses)))
    elif operation == "swap_clauses" and len(clauses) >= 2:
        idx_a, idx_b = rng.sample(range(len(clauses)), 2)
        clauses[idx_a], clauses[idx_b] = clauses[idx_b], clauses[idx_a]
    else:
        if len(clauses) < max_clauses:
            clauses.append(_random_clause(rng, default_offset))
        else:
            default_offset = rng.choice(OUTPUT_OFFSETS)

    layers[layer_index] = list(_normalize_layer_spec(default_offset, clauses, max_clauses))
    return make_candidate_spec(
        [
            _normalize_layer_spec(layer_default, layer_clauses, max_clauses)
            for layer_default, layer_clauses in layers
        ]
    )


def random_candidate(rng: random.Random, max_clauses: int) -> CandidateSpec:
    layer_specs = []
    for _ in range(3):
        default_offset = rng.choice(OUTPUT_OFFSETS)
        clause_count = rng.randint(0, max_clauses)
        clauses = [_random_clause(rng, default_offset) for _ in range(clause_count)]
        layer_specs.append(_normalize_layer_spec(default_offset, clauses, max_clauses))
    return make_candidate_spec(layer_specs)


def run_phase2(
    *,
    seeds: Sequence[CandidateSpec],
    m_values: Sequence[int],
    sample_count: int,
    mutation_seed: int,
    max_clauses: int,
    top_k: int,
    use_rich: bool,
) -> Dict[str, object]:
    start = time.perf_counter()
    rng = random.Random(mutation_seed)
    seen = set()
    top_heap: List[Tuple[Tuple[int, ...], str, SummaryDict]] = []
    frontier: Dict[str, SummaryDict] = {}
    improving_history: List[SummaryDict] = []
    best_score: Tuple[int, ...] | None = None

    seed_specs = list(seeds) or [default_candidate()]
    iterable = _iter_progress(range(sample_count), description="Phase 2 beam/random", use_rich=use_rich, total=sample_count)
    for index in iterable:
        if index < len(seed_specs):
            spec = seed_specs[index]
        elif rng.random() < 0.75:
            spec = mutate_candidate(rng.choice(seed_specs), rng, max_clauses)
        else:
            spec = random_candidate(rng, max_clauses)
        key = candidate_key(spec)
        if key in seen:
            continue
        seen.add(key)
        summary = _evaluate_candidate(spec, m_values, "phase2_mutation")
        score = _score_tuple(summary)
        _trim_top_heap(top_heap, summary, top_k)
        _merge_frontier(frontier, summary)
        if best_score is None or score > best_score:
            best_score = score
            improving_history.append(summary)

    return {
        "phase": "phase2_mutation",
        "pilot_m_values": list(m_values),
        "sample_count": sample_count,
        "unique_evaluated_count": len(seen),
        "mutation_seed": mutation_seed,
        "max_clauses": max_clauses,
        "runtime_sec": time.perf_counter() - start,
        "top_candidates": [entry[2] for entry in sorted(top_heap, reverse=True)],
        "frontier": sorted(frontier.values(), key=_score_tuple, reverse=True),
        "improving_history": improving_history,
    }


def validate_frontier(frontier: Sequence[SummaryDict], m_values: Sequence[int], top_k: int) -> List[SummaryDict]:
    out = []
    for item in frontier[:top_k]:
        spec = item["candidate"]
        serialized = item["candidate"]
        if isinstance(spec, dict):
            from torus_nd_d5_fresh_cyclic_qclock_family import deserialize_candidate

            spec_tuple = deserialize_candidate(serialized)
        else:
            spec_tuple = spec
        out.append(_evaluate_candidate(spec_tuple, m_values, "stability_validation"))
    return out


def best_candidate(frontier: Sequence[SummaryDict], top_candidates: Sequence[SummaryDict]) -> SummaryDict | None:
    combined = list(frontier) + list(top_candidates)
    if not combined:
        return None
    combined.sort(key=_score_tuple, reverse=True)
    return combined[0]


def run_search(
    *,
    phase1_m: int,
    pilot_m_values: Sequence[int],
    stability_m_values: Sequence[int],
    top_k: int,
    sample_count: int,
    mutation_seed: int,
    max_clauses: int,
    jobs: int,
    use_rich: bool,
) -> Dict[str, object]:
    start = time.perf_counter()
    jobs = _resolve_jobs(jobs)

    phase1 = run_phase1(m_value=phase1_m, top_k=top_k, jobs=jobs, use_rich=use_rich)
    seed_candidates = []
    for item in phase1["top_candidates"][:top_k]:
        from torus_nd_d5_fresh_cyclic_qclock_family import deserialize_candidate

        seed_candidates.append(deserialize_candidate(item["candidate"]))
    for item in phase1["improving_history"][:top_k]:
        from torus_nd_d5_fresh_cyclic_qclock_family import deserialize_candidate

        seed_candidates.append(deserialize_candidate(item["candidate"]))

    phase2 = run_phase2(
        seeds=seed_candidates,
        m_values=pilot_m_values,
        sample_count=sample_count,
        mutation_seed=mutation_seed,
        max_clauses=max_clauses,
        top_k=top_k,
        use_rich=use_rich,
    )
    stability = validate_frontier(phase2["frontier"], stability_m_values, top_k=min(10, top_k))
    selected = best_candidate(phase2["frontier"], phase2["top_candidates"])
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "search_parameters": {
            "phase1_m": phase1_m,
            "pilot_m_values": list(pilot_m_values),
            "stability_m_values": list(stability_m_values),
            "top_k": top_k,
            "sample_count": sample_count,
            "mutation_seed": mutation_seed,
            "max_clauses": max_clauses,
            "jobs": jobs,
        },
        "environment": {
            "python_version": platform.python_version(),
            "rich_version": _rich_version(),
        },
        "phases": {
            "phase1": phase1,
            "phase2": phase2,
        },
        "stability_validation": stability,
        "selected_candidate": selected,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    selected = summary["selected_candidate"]
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            "phase1: "
            f"{summary['phases']['phase1']['evaluated_count']} exhaustive candidates at m="
            f"{summary['search_parameters']['phase1_m']}"
        ),
        (
            "phase2: "
            f"{summary['phases']['phase2']['unique_evaluated_count']} unique candidates on "
            f"{summary['search_parameters']['pilot_m_values']}"
        ),
        f"phase2_frontier_size: {len(summary['phases']['phase2']['frontier'])}",
        f"selected_candidate: {selected['candidate_name'] if selected else 'none'}",
    ]
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search fresh cyclic q-clock / v-fiber families for d=5.")
    parser.add_argument("--phase1-m", type=int, default=5, help="modulus for exhaustive phase-1 screening")
    parser.add_argument("--pilot-m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--stability-m-list", default="11,13", help="comma-separated later validation moduli")
    parser.add_argument("--top-k", type=int, default=50, help="number of top candidates to keep")
    parser.add_argument("--sample-count", type=int, default=50000, help="phase-2 random/mutation sample count")
    parser.add_argument("--mutation-seed", type=int, default=20260310, help="fixed seed for phase 2")
    parser.add_argument("--max-clauses", type=int, default=2, help="maximum clauses per layer in phase 2")
    parser.add_argument("--jobs", type=int, default=0, help="worker count for phase 1; 0 means auto")
    parser.add_argument("--out", type=Path, help="write machine-readable summary JSON to this path")
    parser.add_argument("--frontier-out", type=Path, help="write the phase-2 frontier to this JSON path")
    parser.add_argument("--selected-out", type=Path, help="write the selected candidate JSON to this path")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich progress")
    args = parser.parse_args(argv)

    use_rich = not args.no_rich and Console is not None and track is not None
    summary = run_search(
        phase1_m=args.phase1_m,
        pilot_m_values=_parse_m_list(args.pilot_m_list),
        stability_m_values=_parse_m_list(args.stability_m_list),
        top_k=args.top_k,
        sample_count=args.sample_count,
        mutation_seed=args.mutation_seed,
        max_clauses=args.max_clauses,
        jobs=args.jobs,
        use_rich=use_rich,
    )

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2))
    if args.frontier_out is not None:
        args.frontier_out.parent.mkdir(parents=True, exist_ok=True)
        args.frontier_out.write_text(json.dumps(summary["phases"]["phase2"]["frontier"], indent=2))
    if args.selected_out is not None and summary["selected_candidate"] is not None:
        args.selected_out.parent.mkdir(parents=True, exist_ok=True)
        args.selected_out.write_text(json.dumps(summary["selected_candidate"], indent=2))

    _print_summary(summary, use_rich=use_rich)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
