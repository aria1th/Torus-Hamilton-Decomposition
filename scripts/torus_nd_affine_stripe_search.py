#!/usr/bin/env python3
"""Search a fixed affine-stripe family inside one residue layer.

Family:

- canonical bulk outside one selected residue layer S = s;
- on the active layer, the direction tuple depends only on the residue of one
  affine form L(v) mod m;
- each residue class of L gets its own permutation.

This is the next refinement after the one-slice affine search.
"""

from __future__ import annotations

import argparse
import itertools
import json
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


def _form_catalog(dim: int) -> Dict[str, Tuple[int, ...]]:
    forms: Dict[str, Tuple[int, ...]] = {}
    for idx in range(dim):
        coeffs = [0] * dim
        coeffs[idx] = 1
        forms[f"x{idx}"] = tuple(coeffs)
    for i in range(dim):
        for j in range(i + 1, dim):
            plus = [0] * dim
            plus[i] = 1
            plus[j] = 1
            forms[f"x{i}+x{j}"] = tuple(plus)
            minus = [0] * dim
            minus[i] = 1
            minus[j] = -1
            forms[f"x{i}-x{j}"] = tuple(minus)
    return forms


def _decode_template_id(template_id: int, perm_count: int, stripe_count: int) -> List[int]:
    digits = [0] * stripe_count
    for idx in range(stripe_count):
        template_id, digits[idx] = divmod(template_id, perm_count)
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


def _score_template(perm_indices: Sequence[int]) -> Tuple[int, int, Tuple[int, ...]]:
    dim = int(_STATE["dim"])
    vertex_count = int(_STATE["vertex_count"])
    canonical_idx = int(_STATE["canonical_idx"])
    active_layer = int(_STATE["active_layer"])
    layer_of_vertex = _STATE["layer_of_vertex"]
    stripe_of_vertex = _STATE["stripe_of_vertex"]
    neighbor_by_direction = _STATE["neighbor_by_direction"]
    perms = _STATE["perms"]

    cycle_counts: List[int] = []
    for color in range(dim):
        perm = [0] * vertex_count
        for vertex in range(vertex_count):
            if layer_of_vertex[vertex] != active_layer:
                perm_idx = canonical_idx
            else:
                perm_idx = perm_indices[stripe_of_vertex[vertex]]
            direction = perms[perm_idx][color]
            perm[vertex] = neighbor_by_direction[direction][vertex]
        cycle_counts.append(_count_cycles(perm))
    return sum(cycle_counts), max(cycle_counts), tuple(cycle_counts)


def _evaluate_batch(start: int, end: int, top_k: int) -> Dict[str, object]:
    perm_count = int(_STATE["perm_count"])
    stripe_count = int(_STATE["stripe_count"])
    best: List[Dict[str, object]] = []
    hits: List[Dict[str, object]] = []

    for template_id in range(start, end):
        perm_indices = _decode_template_id(template_id, perm_count, stripe_count)
        score_total, score_max, cycle_counts = _score_template(perm_indices)
        record = {
            "template_id": template_id,
            "perm_indices": perm_indices,
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
    active_layer: int,
    perms: Sequence[DirectionTuple],
    canonical_idx: int,
    layer_of_vertex: Sequence[int],
    stripe_of_vertex: Sequence[int],
    neighbor_by_direction: Sequence[Sequence[int]],
) -> None:
    _STATE.clear()
    _STATE.update(
        {
            "dim": dim,
            "m": m,
            "active_layer": active_layer,
            "perm_count": len(perms),
            "stripe_count": m,
            "perms": tuple(tuple(p) for p in perms),
            "canonical_idx": canonical_idx,
            "vertex_count": m ** dim,
            "layer_of_vertex": tuple(layer_of_vertex),
            "stripe_of_vertex": tuple(stripe_of_vertex),
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
    active_layer: int,
    coeffs: Sequence[int],
    perms: Sequence[DirectionTuple],
    perm_indices: Sequence[int],
) -> List[DirectionTuple]:
    canonical = canonical_direction_tuple(dim)
    out: List[DirectionTuple] = []
    for vertex in range(m ** dim):
        coords = index_to_coords(vertex, dim, m)
        if sum(coords) % m != active_layer:
            out.append(canonical)
            continue
        stripe = sum(coeffs[idx] * coords[idx] for idx in range(dim)) % m
        out.append(perms[perm_indices[stripe]])
    return out


def search_affine_stripes(
    dim: int,
    m: int,
    active_layer: int,
    form_name: str,
    top_k: int,
    workers: int,
    chunk_size: int,
) -> Dict[str, object]:
    forms = _form_catalog(dim)
    if form_name not in forms:
        raise ValueError(f"Unknown form {form_name!r}; choose from {sorted(forms)}")
    coeffs = forms[form_name]
    perms = list(itertools.permutations(range(dim)))
    canonical_idx = perms.index(canonical_direction_tuple(dim))
    vertex_count = m ** dim

    layer_of_vertex = [0] * vertex_count
    stripe_of_vertex = [0] * vertex_count
    neighbor_by_direction = [[0] * vertex_count for _ in range(dim)]
    for vertex in range(vertex_count):
        coords = index_to_coords(vertex, dim, m)
        layer_of_vertex[vertex] = sum(coords) % m
        stripe_of_vertex[vertex] = sum(coeffs[idx] * coords[idx] for idx in range(dim)) % m
        for direction in range(dim):
            nxt = list(coords)
            nxt[direction] = (nxt[direction] + 1) % m
            neighbor_by_direction[direction][vertex] = sum(nxt[idx] * (m ** (dim - 1 - idx)) for idx in range(dim))

    template_count = len(perms) ** m
    start = time.perf_counter()
    best: List[Dict[str, object]] = []
    hits: List[Dict[str, object]] = []
    checked = 0

    batch_ranges = [(idx, min(idx + chunk_size, template_count)) for idx in range(0, template_count, chunk_size)]
    with ProcessPoolExecutor(
        max_workers=workers,
        initializer=_init_worker,
        initargs=(dim, m, active_layer, perms, canonical_idx, layer_of_vertex, stripe_of_vertex, neighbor_by_direction),
    ) as pool:
        futures = [pool.submit(_evaluate_batch, begin, end, top_k) for begin, end in batch_ranges]
        for future in as_completed(futures):
            payload = future.result()
            checked += int(payload["checked"])
            best = _merge_top(best, payload["best"], top_k)
            hits.extend(payload["hits"])

    enriched_best = []
    for row in best:
        perm_indices = [int(idx) for idx in row["perm_indices"]]
        direction_tuples = _direction_tuples_for_template(dim, m, active_layer, coeffs, perms, perm_indices)
        validation = validate_direction_tuples(dim, m, direction_tuples)
        nexts = validation.pop("nexts")
        defect = defect_support_summary(dim, m, direction_tuples, canonical_direction_tuple(dim))
        p0_report = induced_p0_maps(nexts, dim, m)
        enriched_best.append(
            {
                **row,
                "active_layer": active_layer,
                "form_name": form_name,
                "form_coeffs": list(coeffs),
                "stripe_assignments": {
                    str(residue): list(perms[perm_indices[residue]]) for residue in range(m)
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
        "active_layer": active_layer,
        "form_name": form_name,
        "form_coeffs": list(coeffs),
        "template_count": template_count,
        "top_k": top_k,
        "checked": checked,
        "runtime_sec": runtime_sec,
        "hamilton_hit_count": len(hits),
        "hits": hits[: min(20, len(hits))],
        "best_templates": enriched_best,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Search a fixed affine-stripe family inside one residue layer.")
    parser.add_argument("--dim", type=int, default=4, help="torus dimension d")
    parser.add_argument("--m", type=int, required=True, help="cycle length m")
    parser.add_argument("--active-layer", type=int, default=0, help="active residue layer S")
    parser.add_argument("--form", default="x0+x2", help="affine form name, e.g. x0+x2")
    parser.add_argument("--top-k", type=int, default=10, help="retain the best K templates")
    parser.add_argument("--workers", type=int, default=8, help="worker process count")
    parser.add_argument("--chunk-size", type=int, default=4096, help="templates per worker batch")
    parser.add_argument("--out", type=Path, help="write JSON output to this path")
    args = parser.parse_args()

    if args.dim < 1 or args.m < 2:
        raise SystemExit("Need dim >= 1 and m >= 2.")

    payload = search_affine_stripes(
        args.dim,
        args.m,
        args.active_layer % args.m,
        args.form,
        args.top_k,
        args.workers,
        args.chunk_size,
    )
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
