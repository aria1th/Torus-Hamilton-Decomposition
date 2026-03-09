#!/usr/bin/env python3
"""Validate candidate decompositions of the directed d-torus C_m^d.

A rule assigns, at each vertex, a permutation of the coordinate directions
`0..d-1`. Color `c` then follows the `c`-th direction in that permutation.

This module provides reusable helpers for:

- loading candidate rules from Python modules or witness JSON files;
- validating full color permutations and Hamiltonicity;
- extracting cycle decompositions and P0 return maps.

Examples:

```bash
python torus_nd_validate.py 3 3 --rule canonical
python torus_nd_validate.py 3 6 --module anc/route_e_even.py --function route_e_direction_triple
python torus_nd_validate.py 3 3 --witness-json witness.json
```
"""

from __future__ import annotations

import argparse
import importlib.util
import inspect
import json
import sys
from array import array
from pathlib import Path
from typing import Callable, Dict, List, Sequence, Tuple

Coords = Tuple[int, ...]
DirectionTuple = Tuple[int, ...]
RuleFn = Callable[[Coords], Sequence[int]]


def strides(dim: int, m: int) -> List[int]:
    out = [1] * dim
    for idx in range(dim - 2, -1, -1):
        out[idx] = out[idx + 1] * m
    return out


def index_to_coords(index: int, dim: int, m: int) -> Coords:
    coords = [0] * dim
    for idx in range(dim - 1, -1, -1):
        index, coords[idx] = divmod(index, m)
    return tuple(coords)


def coords_to_index(coords: Sequence[int], m: int, axis_strides: Sequence[int] | None = None) -> int:
    if axis_strides is None:
        axis_strides = strides(len(coords), m)
    return sum((coord % m) * axis_strides[idx] for idx, coord in enumerate(coords))


def neighbor_index(index: int, coords: Coords, direction: int, m: int, axis_strides: Sequence[int]) -> int:
    step = axis_strides[direction]
    if coords[direction] + 1 < m:
        return index + step
    return index - (m - 1) * step


def predecessor_index(head_index: int, head_coords: Coords, direction: int, m: int, axis_strides: Sequence[int]) -> int:
    step = axis_strides[direction]
    if head_coords[direction] > 0:
        return head_index - step
    return head_index + (m - 1) * step


def canonical_direction_tuple(dim: int) -> DirectionTuple:
    return tuple(range(dim))


def _validate_signature(fn: Callable[..., object], function_name: str) -> int:
    sig = inspect.signature(fn)
    positional = [
        p for p in sig.parameters.values()
        if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]
    has_varargs = any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in sig.parameters.values())
    arity = 3 if has_varargs else len(positional)
    if arity not in (1, 2, 3):
        raise TypeError(
            f"Unsupported signature for {function_name}: expected 1, 2, or 3 positional arguments"
        )
    return arity


def load_rule_factory(module_path: Path, function_name: str) -> Callable[[int, int], RuleFn]:
    resolved = module_path.resolve()
    module_name = f"torus_nd_rule_{resolved.stem}"
    spec = importlib.util.spec_from_file_location(module_name, resolved)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {resolved}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    fn = getattr(module, function_name, None)
    if fn is None:
        raise AttributeError(f"{resolved} does not define {function_name}")

    arity = _validate_signature(fn, function_name)

    def wrapper_factory(dim: int, m: int) -> RuleFn:
        if arity == 1:
            return lambda v: fn(v)
        if arity == 2:
            return lambda v: fn(m, v)
        return lambda v: fn(dim, m, v)

    return wrapper_factory


def load_witness_rule(witness_json: Path, dim: int, m: int) -> RuleFn:
    payload = json.loads(witness_json.read_text())
    payload_dim = int(payload["dim"])
    payload_m = int(payload["m"])
    if payload_dim != dim or payload_m != m:
        raise ValueError(
            f"Witness {witness_json} is for dim={payload_dim}, m={payload_m}; requested dim={dim}, m={m}"
        )
    tuples_raw = payload.get("witness_direction_tuples")
    if tuples_raw is None:
        tuples_raw = payload.get("incumbent_direction_tuples")
    if tuples_raw is None:
        raise KeyError(f"{witness_json} does not contain witness_direction_tuples or incumbent_direction_tuples")
    direction_tuples = [tuple(int(x) for x in dirs) for dirs in tuples_raw]
    expected = m ** dim
    if len(direction_tuples) != expected:
        raise ValueError(f"Witness contains {len(direction_tuples)} vertices; expected {expected}")

    def rule(coords: Coords) -> DirectionTuple:
        idx = coords_to_index(coords, m)
        return direction_tuples[idx]

    return rule


def evaluate_rule_tuples(dim: int, m: int, rule: RuleFn) -> Dict[str, object]:
    vertex_count = m ** dim
    direction_tuples: List[DirectionTuple] = []
    first_bad_vertex = None
    first_bad_dirs = None
    first_bad_reason = None
    expected_dirs = list(range(dim))

    for index in range(vertex_count):
        coords = index_to_coords(index, dim, m)
        try:
            dirs = tuple(int(x) for x in rule(coords))
        except Exception as exc:  # pragma: no cover - defensive reporting path
            first_bad_vertex = coords
            first_bad_reason = f"rule evaluation failed: {exc}"
            break

        if len(dirs) != dim:
            first_bad_vertex = coords
            first_bad_dirs = dirs
            first_bad_reason = f"expected {dim} directions, got {len(dirs)}"
            break

        if sorted(dirs) != expected_dirs:
            first_bad_vertex = coords
            first_bad_dirs = dirs
            first_bad_reason = f"rule output is not a permutation of 0..{dim - 1}"
            break

        direction_tuples.append(dirs)

    report: Dict[str, object] = {
        "dim": dim,
        "m": m,
        "vertex_count": vertex_count,
        "rule_valid": first_bad_reason is None,
    }
    if first_bad_reason is None:
        report["direction_tuples"] = direction_tuples
    else:
        report["first_bad_vertex"] = list(first_bad_vertex) if first_bad_vertex is not None else None
        report["first_bad_dirs"] = list(first_bad_dirs) if first_bad_dirs is not None else None
        report["first_bad_reason"] = first_bad_reason
    return report


def build_nexts_from_direction_tuples(
    dim: int,
    m: int,
    direction_tuples: Sequence[DirectionTuple],
) -> List[array]:
    vertex_count = m ** dim
    if len(direction_tuples) != vertex_count:
        raise ValueError(f"Need {vertex_count} direction tuples, got {len(direction_tuples)}")
    axis_strides = strides(dim, m)
    nexts = [array("I", [0]) * vertex_count for _ in range(dim)]
    for index, dirs in enumerate(direction_tuples):
        coords = index_to_coords(index, dim, m)
        for color, direction in enumerate(dirs):
            nexts[color][index] = neighbor_index(index, coords, direction, m, axis_strides)
    return nexts


def cycle_decomposition(perm: Sequence[int]) -> List[List[int]]:
    n = len(perm)
    seen = bytearray(n)
    cycles: List[List[int]] = []
    for start in range(n):
        if seen[start]:
            continue
        cur = start
        cycle: List[int] = []
        while not seen[cur]:
            seen[cur] = 1
            cycle.append(cur)
            cur = perm[cur]
        cycles.append(cycle)
    return cycles


def cycle_stats(perm: Sequence[int]) -> Tuple[int, int]:
    cycles = cycle_decomposition(perm)
    sign = 1
    for cycle in cycles:
        if (len(cycle) - 1) % 2 == 1:
            sign *= -1
    return len(cycles), sign


def validate_direction_tuples(dim: int, m: int, direction_tuples: Sequence[DirectionTuple]) -> Dict[str, object]:
    vertex_count = m ** dim
    nexts = build_nexts_from_direction_tuples(dim, m, direction_tuples)
    report: Dict[str, object] = {
        "dim": dim,
        "m": m,
        "vertex_count": vertex_count,
        "next_arrays_bytes_estimate": dim * vertex_count * 4,
        "rule_valid": True,
    }

    color_stats = []
    sign_product = 1
    all_hamilton = True
    all_permutations = True

    for color, perm in enumerate(nexts):
        indeg = array("I", [0]) * vertex_count
        bad_head = None
        for head in perm:
            indeg[head] += 1
        for vertex, count in enumerate(indeg):
            if count != 1:
                bad_head = vertex
                all_permutations = False
                break

        cycles = cycle_decomposition(perm)
        sign = 1
        for cycle in cycles:
            if (len(cycle) - 1) % 2 == 1:
                sign *= -1
        sign_product *= sign
        cycle_count = len(cycles)
        is_hamilton = bad_head is None and cycle_count == 1
        all_hamilton = all_hamilton and is_hamilton

        color_stats.append(
            {
                "color": color,
                "indegree_ok": bad_head is None,
                "bad_head": bad_head,
                "cycle_count": cycle_count,
                "sign": sign,
                "is_hamilton": is_hamilton,
            }
        )

    report["all_permutations"] = all_permutations
    report["all_hamilton"] = all_hamilton
    report["sign_product"] = sign_product
    report["color_stats"] = color_stats
    report["nexts"] = nexts
    return report


def validate_rule(dim: int, m: int, rule: RuleFn) -> Dict[str, object]:
    tuple_report = evaluate_rule_tuples(dim, m, rule)
    if not tuple_report["rule_valid"]:
        tuple_report["next_arrays_bytes_estimate"] = dim * (m ** dim) * 4
        return tuple_report

    direction_tuples = tuple_report["direction_tuples"]
    report = validate_direction_tuples(dim, m, direction_tuples)
    report["direction_tuples"] = direction_tuples
    return report


def p0_indices(dim: int, m: int) -> List[int]:
    return [idx for idx in range(m ** dim) if sum(index_to_coords(idx, dim, m)) % m == 0]


def section_indices(dim: int, m: int, predicate: Callable[[Coords], bool]) -> List[int]:
    return [idx for idx in range(m ** dim) if predicate(index_to_coords(idx, dim, m))]


def coord_hyperplane_indices(dim: int, m: int, axis: int, residue: int = 0) -> List[int]:
    residue %= m
    return section_indices(dim, m, lambda coords: coords[axis] % m == residue)


def induced_first_return_maps(
    nexts: Sequence[Sequence[int]],
    dim: int,
    m: int,
    section_vertices: Sequence[int],
) -> Dict[str, object]:
    section = list(section_vertices)
    pos = {vertex: idx for idx, vertex in enumerate(section)}
    section_coords = [list(index_to_coords(vertex, dim, m)) for vertex in section]
    maps = []
    vertex_count = m ** dim

    for color, perm in enumerate(nexts):
        image_positions: List[int] = []
        return_lengths: List[int] = []
        for vertex in section:
            cur = perm[vertex]
            steps = 1
            while cur not in pos and steps <= vertex_count:
                cur = perm[cur]
                steps += 1
            if cur not in pos:
                raise RuntimeError(
                    f"First return to section failed for color={color}, start={vertex}, "
                    f"dim={dim}, m={m}"
                )
            image_positions.append(pos[cur])
            return_lengths.append(steps)
        cycles = cycle_decomposition(image_positions)
        maps.append(
            {
                "color": color,
                "cycle_count": len(cycles),
                "is_hamilton": len(cycles) == 1,
                "map": image_positions,
                "return_lengths": return_lengths,
                "uniform_return_length": len(set(return_lengths)) == 1,
            }
        )
    return {
        "section_size": len(section),
        "section_vertices": section_coords,
        "color_maps": maps,
    }


def induced_p0_maps(nexts: Sequence[Sequence[int]], dim: int, m: int) -> Dict[str, object]:
    p0 = p0_indices(dim, m)
    pos = {vertex: idx for idx, vertex in enumerate(p0)}
    p0_coords = [list(index_to_coords(vertex, dim, m)) for vertex in p0]
    maps = []
    for color, perm in enumerate(nexts):
        image_positions: List[int] = []
        for vertex in p0:
            cur = vertex
            for _ in range(m):
                cur = perm[cur]
            image_positions.append(pos[cur])
        cycles = cycle_decomposition(image_positions)
        maps.append(
            {
                "color": color,
                "cycle_count": len(cycles),
                "is_hamilton": len(cycles) == 1,
                "map": image_positions,
            }
        )
    return {
        "p0_size": len(p0),
        "p0_vertices": p0_coords,
        "color_maps": maps,
    }


def defect_support_summary(
    dim: int,
    m: int,
    direction_tuples: Sequence[DirectionTuple],
    bulk_direction_tuple: DirectionTuple | None = None,
) -> Dict[str, object]:
    if bulk_direction_tuple is None:
        bulk_direction_tuple = canonical_direction_tuple(dim)
    defect_vertices: List[List[int]] = []
    layer_counts: Dict[str, int] = {}
    low_layers = {0, 1, 2, 3}
    low_layer_only = True

    for index, dirs in enumerate(direction_tuples):
        if tuple(dirs) == tuple(bulk_direction_tuple):
            continue
        coords = list(index_to_coords(index, dim, m))
        defect_vertices.append(coords)
        layer = sum(coords) % m
        layer_counts[str(layer)] = layer_counts.get(str(layer), 0) + 1
        if layer not in low_layers:
            low_layer_only = False

    return {
        "bulk_direction_tuple": list(bulk_direction_tuple),
        "defect_vertex_count": len(defect_vertices),
        "defect_vertices": defect_vertices,
        "defect_layer_counts": layer_counts,
        "defect_layers": sorted(int(layer) for layer in layer_counts),
        "low_layer_only": low_layer_only,
    }


def _human_bytes(num_bytes: int) -> str:
    value = float(num_bytes)
    for suffix in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024.0 or suffix == "TiB":
            return f"{value:.2f} {suffix}"
        value /= 1024.0
    return f"{num_bytes} B"


def _parse_rule_source(args: argparse.Namespace) -> Tuple[RuleFn, str]:
    if args.witness_json is not None:
        return load_witness_rule(args.witness_json, args.dim, args.m), f"witness:{args.witness_json}"
    if args.module is not None:
        factory = load_rule_factory(args.module, args.function)
        return factory(args.dim, args.m), f"{args.module}:{args.function}"
    return (lambda v: canonical_direction_tuple(args.dim)), args.rule


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate candidate decompositions of the directed d-torus.")
    parser.add_argument("dim", type=int, help="torus dimension d")
    parser.add_argument("m", type=int, help="cycle length m in each coordinate")
    parser.add_argument(
        "--rule",
        choices=("canonical",),
        default="canonical",
        help="built-in rule to validate (ignored if --module or --witness-json is supplied)",
    )
    parser.add_argument("--module", type=Path, help="Python module defining an external rule function")
    parser.add_argument("--function", default="direction_tuple", help="external rule function name")
    parser.add_argument("--witness-json", type=Path, help="JSON witness emitted by torus_nd_exact_search.py")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()

    if args.dim < 1 or args.m < 2:
        raise SystemExit("Need dim >= 1 and m >= 2.")

    rule, rule_label = _parse_rule_source(args)
    report = validate_rule(args.dim, args.m, rule)
    report["rule_source"] = rule_label

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True, default=list))
        return

    print(f"dim={args.dim} m={args.m} vertices={report['vertex_count']}")
    print(f"rule={rule_label}")
    print(f"estimated next-array memory={_human_bytes(int(report['next_arrays_bytes_estimate']))}")
    if not report["rule_valid"]:
        print("rule_valid=False")
        print(f"first_bad_vertex={report.get('first_bad_vertex')}")
        print(f"first_bad_dirs={report.get('first_bad_dirs')}")
        print(f"reason={report.get('first_bad_reason')}")
        return

    print(f"all_permutations={report['all_permutations']}")
    print(f"all_hamilton={report['all_hamilton']}")
    print(f"sign_product={report['sign_product']}")
    for stat in report["color_stats"]:
        print(
            f"color {stat['color']}: indegree_ok={stat['indegree_ok']} "
            f"cycles={stat['cycle_count']} sign={stat['sign']} hamilton={stat['is_hamilton']}"
        )


if __name__ == "__main__":
    main()
