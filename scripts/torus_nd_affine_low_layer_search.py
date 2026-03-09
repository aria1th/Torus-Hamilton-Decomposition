#!/usr/bin/env python3
"""Search a small affine-slice family inside one low residue layer.

Family:

- canonical bulk outside one selected residue layer S = s;
- on the active layer, use a default permutation p_default;
- on one affine slice L(v) = r (mod m) inside that layer, override with
  p_special.

This is the next-smallest family after the uniform layer-template search.
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


def _form_catalog(dim: int) -> List[Tuple[str, Tuple[int, ...]]]:
    forms: List[Tuple[str, Tuple[int, ...]]] = []
    for idx in range(dim):
        coeffs = [0] * dim
        coeffs[idx] = 1
        forms.append((f"x{idx}", tuple(coeffs)))
    for i in range(dim):
        for j in range(i + 1, dim):
            plus = [0] * dim
            plus[i] = 1
            plus[j] = 1
            forms.append((f"x{i}+x{j}", tuple(plus)))
            minus = [0] * dim
            minus[i] = 1
            minus[j] = -1
            forms.append((f"x{i}-x{j}", tuple(minus)))
    return forms


def _decode_template_id(
    template_id: int,
    layer_count: int,
    perm_count: int,
    form_count: int,
    m: int,
) -> Tuple[int, int, int, int, int]:
    template_id, special_perm = divmod(template_id, perm_count)
    template_id, residue = divmod(template_id, m)
    template_id, form_idx = divmod(template_id, form_count)
    template_id, default_perm = divmod(template_id, perm_count)
    template_id, layer_idx = divmod(template_id, layer_count)
    return layer_idx, default_perm, form_idx, residue, special_perm


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


def _score_template(decoded: Tuple[int, int, int, int, int]) -> Tuple[int, int, Tuple[int, ...]]:
    dim = int(_STATE["dim"])
    vertex_count = int(_STATE["vertex_count"])
    active_layers = _STATE["active_layers"]
    layer_of_vertex = _STATE["layer_of_vertex"]
    form_residues = _STATE["form_residues"]
    neighbor_by_direction = _STATE["neighbor_by_direction"]
    perms = _STATE["perms"]
    canonical_idx = int(_STATE["canonical_idx"])

    layer_idx, default_perm_idx, form_idx, residue, special_perm_idx = decoded
    active_layer = active_layers[layer_idx]

    cycle_counts: List[int] = []
    for color in range(dim):
        perm = [0] * vertex_count
        for vertex in range(vertex_count):
            if layer_of_vertex[vertex] != active_layer:
                perm_idx = canonical_idx
            elif form_residues[form_idx][vertex] == residue:
                perm_idx = special_perm_idx
            else:
                perm_idx = default_perm_idx
            direction = perms[perm_idx][color]
            perm[vertex] = neighbor_by_direction[direction][vertex]
        cycle_counts.append(_count_cycles(perm))
    return sum(cycle_counts), max(cycle_counts), tuple(cycle_counts)


def _evaluate_batch(start: int, end: int, top_k: int) -> Dict[str, object]:
    layer_count = int(_STATE["layer_count"])
    perm_count = int(_STATE["perm_count"])
    form_count = int(_STATE["form_count"])
    m = int(_STATE["m"])

    best: List[Dict[str, object]] = []
    hits: List[Dict[str, object]] = []

    for template_id in range(start, end):
        decoded = _decode_template_id(template_id, layer_count, perm_count, form_count, m)
        score_total, score_max, cycle_counts = _score_template(decoded)
        layer_idx, default_perm, form_idx, residue, special_perm = decoded
        record = {
            "template_id": template_id,
            "layer_idx": layer_idx,
            "default_perm_idx": default_perm,
            "form_idx": form_idx,
            "residue": residue,
            "special_perm_idx": special_perm,
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
    canonical_idx: int,
    layer_of_vertex: Sequence[int],
    form_residues: Sequence[Sequence[int]],
    neighbor_by_direction: Sequence[Sequence[int]],
) -> None:
    _STATE.clear()
    _STATE.update(
        {
            "dim": dim,
            "m": m,
            "active_layers": tuple(active_layers),
            "layer_count": len(active_layers),
            "perm_count": len(perms),
            "form_count": len(form_residues),
            "perms": tuple(tuple(p) for p in perms),
            "canonical_idx": canonical_idx,
            "vertex_count": m ** dim,
            "layer_of_vertex": tuple(layer_of_vertex),
            "form_residues": tuple(tuple(row) for row in form_residues),
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
    forms: Sequence[Tuple[str, Tuple[int, ...]]],
    perms: Sequence[DirectionTuple],
    decoded: Tuple[int, int, int, int, int],
) -> List[DirectionTuple]:
    layer_idx, default_perm_idx, form_idx, residue, special_perm_idx = decoded
    active_layer = active_layers[layer_idx]
    _, coeffs = forms[form_idx]
    canonical = canonical_direction_tuple(dim)
    out: List[DirectionTuple] = []
    for vertex in range(m ** dim):
        coords = index_to_coords(vertex, dim, m)
        if sum(coords) % m != active_layer:
            out.append(canonical)
            continue
        value = sum(coeffs[idx] * coords[idx] for idx in range(dim)) % m
        if value == residue:
            out.append(perms[special_perm_idx])
        else:
            out.append(perms[default_perm_idx])
    return out


def search_affine_low_layer(
    dim: int,
    m: int,
    low_layers: Sequence[int],
    top_k: int,
    workers: int,
    chunk_size: int,
) -> Dict[str, object]:
    forms = _form_catalog(dim)
    perms = list(itertools.permutations(range(dim)))
    canonical_idx = perms.index(canonical_direction_tuple(dim))
    active_layers = sorted({layer % m for layer in low_layers})
    vertex_count = m ** dim

    layer_of_vertex = [0] * vertex_count
    neighbor_by_direction = [[0] * vertex_count for _ in range(dim)]
    form_residues = [[0] * vertex_count for _ in forms]
    for vertex in range(vertex_count):
        coords = index_to_coords(vertex, dim, m)
        layer_of_vertex[vertex] = sum(coords) % m
        for form_idx, (_, coeffs) in enumerate(forms):
            form_residues[form_idx][vertex] = sum(coeffs[idx] * coords[idx] for idx in range(dim)) % m
        for direction in range(dim):
            nxt = list(coords)
            nxt[direction] = (nxt[direction] + 1) % m
            neighbor_by_direction[direction][vertex] = sum(nxt[idx] * (m ** (dim - 1 - idx)) for idx in range(dim))

    template_count = len(active_layers) * len(perms) * len(forms) * m * len(perms)
    start = time.perf_counter()
    best: List[Dict[str, object]] = []
    hits: List[Dict[str, object]] = []
    checked = 0

    batch_ranges = [(idx, min(idx + chunk_size, template_count)) for idx in range(0, template_count, chunk_size)]
    with ProcessPoolExecutor(
        max_workers=workers,
        initializer=_init_worker,
        initargs=(dim, m, active_layers, perms, canonical_idx, layer_of_vertex, form_residues, neighbor_by_direction),
    ) as pool:
        futures = [pool.submit(_evaluate_batch, begin, end, top_k) for begin, end in batch_ranges]
        for future in as_completed(futures):
            payload = future.result()
            checked += int(payload["checked"])
            best = _merge_top(best, payload["best"], top_k)
            hits.extend(payload["hits"])

    enriched_best = []
    for row in best:
        decoded = (
            int(row["layer_idx"]),
            int(row["default_perm_idx"]),
            int(row["form_idx"]),
            int(row["residue"]),
            int(row["special_perm_idx"]),
        )
        direction_tuples = _direction_tuples_for_template(dim, m, active_layers, forms, perms, decoded)
        validation = validate_direction_tuples(dim, m, direction_tuples)
        nexts = validation.pop("nexts")
        defect = defect_support_summary(dim, m, direction_tuples, canonical_direction_tuple(dim))
        p0_report = induced_p0_maps(nexts, dim, m)
        layer_idx, default_perm_idx, form_idx, residue, special_perm_idx = decoded
        enriched_best.append(
            {
                **row,
                "active_layer": active_layers[layer_idx],
                "default_perm": list(perms[default_perm_idx]),
                "form_name": forms[form_idx][0],
                "form_coeffs": list(forms[form_idx][1]),
                "special_residue": residue,
                "special_perm": list(perms[special_perm_idx]),
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
        "form_names": [name for name, _ in forms],
        "template_count": template_count,
        "top_k": top_k,
        "checked": checked,
        "runtime_sec": runtime_sec,
        "hamilton_hit_count": len(hits),
        "hits": hits[: min(20, len(hits))],
        "best_templates": enriched_best,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Search one-layer affine-slice templates on the directed d-torus.")
    parser.add_argument("--dim", type=int, default=4, help="torus dimension d")
    parser.add_argument("--m", type=int, required=True, help="cycle length m")
    parser.add_argument(
        "--low-layers",
        default="0,1,2,3",
        help="comma-separated active residue layers to consider",
    )
    parser.add_argument("--top-k", type=int, default=10, help="retain the best K templates")
    parser.add_argument("--workers", type=int, default=8, help="worker process count")
    parser.add_argument("--chunk-size", type=int, default=4096, help="templates per worker batch")
    parser.add_argument("--out", type=Path, help="write JSON output to this path")
    args = parser.parse_args()

    if args.dim < 1 or args.m < 2:
        raise SystemExit("Need dim >= 1 and m >= 2.")
    low_layers = [int(part.strip()) for part in args.low_layers.split(",") if part.strip()]
    if not low_layers:
        raise SystemExit("Need at least one low layer residue.")

    payload = search_affine_low_layer(args.dim, args.m, low_layers, args.top_k, args.workers, args.chunk_size)
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
