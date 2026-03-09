#!/usr/bin/env python3
"""Search simple layer-residue templates for the directed d-torus.

This script explores the smallest proof-oriented ansatz family:

- the bulk rule is canonical;
- on a selected set of layer residues S mod m, each layer receives a single
  permutation of the coordinate directions;
- the same permutation is used for every vertex in that layer.

The family is intentionally narrow. A pass would be a strong structural hint;
an exhaustive failure is evidence that any viable 4D pattern needs finer,
coordinate-conditional defect geometry.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from torus_nd_validate import (
    canonical_direction_tuple,
    defect_support_summary,
    induced_p0_maps,
    index_to_coords,
    validate_direction_tuples,
)

DirectionTuple = Tuple[int, ...]

_STATE: Dict[str, object] = {}


def _decode_template_id(template_id: int, perm_count: int, active_count: int) -> List[int]:
    digits = [0] * active_count
    for idx in range(active_count):
        template_id, digit = divmod(template_id, perm_count)
        digits[idx] = digit
    return digits


def _count_cycles(perm: Sequence[int]) -> int:
    seen = bytearray(len(perm))
    count = 0
    for start in range(len(perm)):
        if seen[start]:
            continue
        count += 1
        cur = start
        while not seen[cur]:
            seen[cur] = 1
            cur = perm[cur]
    return count


def _score_template(template_digits: Sequence[int]) -> Tuple[int, int, Tuple[int, ...]]:
    dim = int(_STATE["dim"])
    vertex_count = int(_STATE["vertex_count"])
    active_layers = _STATE["active_layers"]
    layer_of_vertex = _STATE["layer_of_vertex"]
    neighbor_by_direction = _STATE["neighbor_by_direction"]
    perms = _STATE["perms"]
    canonical = _STATE["canonical"]

    layer_to_perm = {layer: template_digits[idx] for idx, layer in enumerate(active_layers)}
    cycle_counts: List[int] = []

    for color in range(dim):
        perm = [0] * vertex_count
        for vertex in range(vertex_count):
            layer = layer_of_vertex[vertex]
            perm_idx = layer_to_perm.get(layer, canonical)
            direction = perms[perm_idx][color]
            perm[vertex] = neighbor_by_direction[direction][vertex]
        cycle_counts.append(_count_cycles(perm))

    return sum(cycle_counts), max(cycle_counts), tuple(cycle_counts)


def _evaluate_batch(start: int, end: int, top_k: int) -> Dict[str, object]:
    perm_count = int(_STATE["perm_count"])
    active_count = len(_STATE["active_layers"])
    best: List[Dict[str, object]] = []
    hits: List[Dict[str, object]] = []

    for template_id in range(start, end):
        digits = _decode_template_id(template_id, perm_count, active_count)
        score_total, score_max, cycle_counts = _score_template(digits)
        record = {
            "template_id": template_id,
            "perm_indices": digits,
            "cycle_counts": list(cycle_counts),
            "score_total_cycles": score_total,
            "score_max_cycles": score_max,
        }
        if score_max == 1:
            hits.append(record)
        best.append(record)
        best.sort(key=lambda row: (row["score_total_cycles"], row["score_max_cycles"], row["cycle_counts"], row["template_id"]))
        if len(best) > top_k:
            best.pop()

    return {"best": best, "hits": hits, "checked": end - start}


def _init_worker(
    dim: int,
    m: int,
    active_layers: Sequence[int],
    perms: Sequence[DirectionTuple],
    canonical: int,
    layer_of_vertex: Sequence[int],
    neighbor_by_direction: Sequence[Sequence[int]],
) -> None:
    _STATE.clear()
    _STATE.update(
        {
            "dim": dim,
            "m": m,
            "active_layers": tuple(active_layers),
            "perm_count": len(perms),
            "perms": tuple(tuple(p) for p in perms),
            "canonical": canonical,
            "vertex_count": m ** dim,
            "layer_of_vertex": tuple(layer_of_vertex),
            "neighbor_by_direction": tuple(tuple(row) for row in neighbor_by_direction),
        }
    )


def _merge_top(existing: List[Dict[str, object]], incoming: Iterable[Dict[str, object]], top_k: int) -> List[Dict[str, object]]:
    merged = list(existing)
    merged.extend(incoming)
    merged.sort(key=lambda row: (row["score_total_cycles"], row["score_max_cycles"], row["cycle_counts"], row["template_id"]))
    return merged[:top_k]


def _direction_tuples_for_template(
    dim: int,
    m: int,
    active_layers: Sequence[int],
    perms: Sequence[DirectionTuple],
    perm_indices: Sequence[int],
) -> List[DirectionTuple]:
    canonical = canonical_direction_tuple(dim)
    layer_to_perm = {layer: perms[perm_indices[idx]] for idx, layer in enumerate(active_layers)}
    out: List[DirectionTuple] = []
    for vertex in range(m ** dim):
        coords = index_to_coords(vertex, dim, m)
        layer = sum(coords) % m
        out.append(layer_to_perm.get(layer, canonical))
    return out


def search_layer_templates(
    dim: int,
    m: int,
    low_layers: Sequence[int],
    top_k: int,
    workers: int,
    chunk_size: int,
) -> Dict[str, object]:
    perms = list(itertools.permutations(range(dim)))
    canonical = perms.index(canonical_direction_tuple(dim))
    active_layers = sorted({layer % m for layer in low_layers})
    vertex_count = m ** dim

    layer_of_vertex = [0] * vertex_count
    neighbor_by_direction = [[0] * vertex_count for _ in range(dim)]
    for vertex in range(vertex_count):
        coords = index_to_coords(vertex, dim, m)
        layer_of_vertex[vertex] = sum(coords) % m
        for direction in range(dim):
            nxt = list(coords)
            nxt[direction] = (nxt[direction] + 1) % m
            neighbor_by_direction[direction][vertex] = sum(nxt[idx] * (m ** (dim - 1 - idx)) for idx in range(dim))

    template_count = len(perms) ** len(active_layers)
    start = time.perf_counter()
    best: List[Dict[str, object]] = []
    hits: List[Dict[str, object]] = []

    batch_ranges = [(idx, min(idx + chunk_size, template_count)) for idx in range(0, template_count, chunk_size)]
    with ProcessPoolExecutor(
        max_workers=workers,
        initializer=_init_worker,
        initargs=(dim, m, active_layers, perms, canonical, layer_of_vertex, neighbor_by_direction),
    ) as pool:
        futures = [pool.submit(_evaluate_batch, begin, end, top_k) for begin, end in batch_ranges]
        checked = 0
        for future in as_completed(futures):
            payload = future.result()
            checked += int(payload["checked"])
            best = _merge_top(best, payload["best"], top_k)
            hits.extend(payload["hits"])

    enriched_best = []
    for row in best:
        direction_tuples = _direction_tuples_for_template(dim, m, active_layers, perms, row["perm_indices"])
        validation = validate_direction_tuples(dim, m, direction_tuples)
        nexts = validation.pop("nexts")
        defect = defect_support_summary(dim, m, direction_tuples, canonical_direction_tuple(dim))
        p0_report = induced_p0_maps(nexts, dim, m)
        enriched_best.append(
            {
                **row,
                "layer_assignments": {
                    str(layer): list(perms[row["perm_indices"][idx]]) for idx, layer in enumerate(active_layers)
                },
                "sign_product": validation["sign_product"],
                "all_hamilton": validation["all_hamilton"],
                "color_stats": validation["color_stats"],
                "defect_support": defect,
                "p0_report": p0_report,
            }
        )

    runtime_sec = time.perf_counter() - start
    return {
        "dim": dim,
        "m": m,
        "low_layers_requested": list(low_layers),
        "active_layers": active_layers,
        "template_count": template_count,
        "top_k": top_k,
        "checked": checked,
        "runtime_sec": runtime_sec,
        "hamilton_hit_count": len(hits),
        "hits": hits[: min(20, len(hits))],
        "best_templates": enriched_best,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Exhaustive search over simple layer-residue template families.")
    parser.add_argument("--dim", type=int, default=4, help="torus dimension d")
    parser.add_argument("--m", type=int, required=True, help="cycle length m")
    parser.add_argument(
        "--low-layers",
        default="0,1,2,3",
        help="comma-separated layer residues to vary; other layers stay canonical",
    )
    parser.add_argument("--top-k", type=int, default=10, help="retain the best K templates")
    parser.add_argument("--workers", type=int, default=8, help="worker process count")
    parser.add_argument("--chunk-size", type=int, default=2048, help="templates per worker batch")
    parser.add_argument("--out", type=Path, help="write JSON output to this path")
    args = parser.parse_args()

    if args.dim < 1 or args.m < 2:
        raise SystemExit("Need dim >= 1 and m >= 2.")
    low_layers = [int(part.strip()) for part in args.low_layers.split(",") if part.strip()]
    if not low_layers:
        raise SystemExit("Need at least one low layer residue.")

    payload = search_layer_templates(args.dim, args.m, low_layers, args.top_k, args.workers, args.chunk_size)
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
