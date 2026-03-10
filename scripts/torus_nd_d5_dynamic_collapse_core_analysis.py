#!/usr/bin/env python3
"""Analyze the dynamic-collapse core of the stable joined-quotient d=5 field."""

from __future__ import annotations

import argparse
import json
import platform
import time
from collections import Counter, defaultdict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from torus_nd_d5_master_field_quotient_family import (
    SCHEMA_JOIN,
    color_map_from_table,
    rotation_orbits,
    schema_state_space,
    state_for_vertex,
    state_name,
    state_to_id_map,
)

TASK_ID = "D5-DYNAMIC-COLLAPSE-CORE-001"
STATE_SPACE_KEY = (5, 7, 9, 11, 13)

try:
    from rich.console import Console
except ImportError:  # pragma: no cover - optional dependency
    Console = None


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _rich_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def _load_table(field_json: Path) -> Tuple[dict, Dict[int, Tuple[int, ...]]]:
    field = json.loads(field_json.read_text())
    table = {int(row["state_id"]): tuple(row["permutation"]) for row in field["anchor_table"]["rows"]}
    return field, table


def _layer_sort_key(layer_bucket: object) -> Tuple[int, str]:
    if layer_bucket == "4+":
        return (4, "4+")
    return (int(layer_bucket), str(layer_bucket))


def _phase_delta(coords: Sequence[int], m: int) -> int:
    return (coords[3] - coords[1]) % m


def _phase_align_bit(coords: Sequence[int], m: int) -> int:
    return int(_phase_delta(coords, m) == 0)


def _palette_by_layer(field: dict) -> Dict[str, object]:
    palette = defaultdict(lambda: {"permutations": Counter(), "color0_outputs": Counter()})
    for row in field["anchor_table"]["rows"]:
        layer = str(row["state"]["layer_bucket"])
        palette[layer]["permutations"][row["permutation_name"]] += 1
        palette[layer]["color0_outputs"][str(row["permutation"][0])] += 1
    ordered = {}
    for layer in sorted(palette, key=lambda item: _layer_sort_key(item if item != "4+" else "4+")):
        ordered[layer] = {
            "permutation_histogram": dict(sorted(palette[layer]["permutations"].items())),
            "color0_output_histogram": dict(sorted(palette[layer]["color0_outputs"].items())),
            "is_constant_permutation": len(palette[layer]["permutations"]) == 1,
            "is_constant_color0_output": len(palette[layer]["color0_outputs"]) == 1,
            "constant_permutation": next(iter(palette[layer]["permutations"])) if len(palette[layer]["permutations"]) == 1 else None,
            "constant_color0_output": int(next(iter(palette[layer]["color0_outputs"]))) if len(palette[layer]["color0_outputs"]) == 1 else None,
        }
    return ordered


def _return_formula_summary(table: Dict[int, Tuple[int, ...]], *, m_values: Sequence[int]) -> Dict[str, object]:
    results = []
    for m in m_values:
        matches = True
        bad_examples = []
        for q in range(m):
            for w in range(m):
                for v in range(m):
                    for u in range(m):
                        coords = ((-q - w - v - u) % m, q, w, v, u)
                        cur = coords
                        for _ in range(m):
                            cur = color_map_from_table(table, SCHEMA_JOIN, m, cur, 0, STATE_SPACE_KEY)
                        got = (cur[1], cur[2], cur[3], cur[4])
                        target = ((q + 1) % m, w, (v + 1) % m, u)
                        if got != target:
                            matches = False
                            if len(bad_examples) < 10:
                                bad_examples.append({"qwvu": [q, w, v, u], "got": list(got), "target": list(target)})
        results.append({"m": m, "matches_formula": matches, "bad_examples": bad_examples})
    return {
        "formula_checked": "R_0(q,w,v,u) = (q+1, w, v+1, u)",
        "implied_section_return": "U_0 = id on (w,u)",
        "implied_monodromy": 0,
        "m_results": results,
    }


def _canonical_background_path(table: Dict[int, Tuple[int, ...]], *, m: int) -> List[Dict[str, object]]:
    union_states = schema_state_space(SCHEMA_JOIN.name, STATE_SPACE_KEY)
    state_ids = state_to_id_map(union_states)
    coords = (0, 0, 0, 0, 0)
    path = []
    for step in range(m):
        state = state_for_vertex(coords, m, SCHEMA_JOIN)
        state_id = state_ids[state]
        path.append(
            {
                "step": step,
                "coords": list(coords),
                "state_id": state_id,
                "state_name": state_name(state),
                "state": {"layer_bucket": state[0], "signature": list(state[1])},
                "permutation": list(table[state_id]),
                "color0_output": table[state_id][0],
                "delta": _phase_delta(coords, m),
                "phase_align": _phase_align_bit(coords, m),
            }
        )
        coords = color_map_from_table(table, SCHEMA_JOIN, m, coords, 0, STATE_SPACE_KEY)
    return path


def _phase_collision_data(table: Dict[int, Tuple[int, ...]], *, m_values: Sequence[int]) -> Dict[str, object]:
    union_states = schema_state_space(SCHEMA_JOIN.name, STATE_SPACE_KEY)
    state_ids = state_to_id_map(union_states)
    orbit_index = {}
    for orbit_id, orbit in enumerate(rotation_orbits(union_states)):
        for state_id in orbit:
            orbit_index[state_id] = orbit_id

    per_m = []
    canonical_tail_core = None
    collision_lookup_all = {}
    for m in m_values:
        visited_delta = defaultdict(set)
        visited_examples = defaultdict(dict)
        for q in range(m):
            for w in range(m):
                for v in range(m):
                    for u in range(m):
                        cur = ((-q - w - v - u) % m, q, w, v, u)
                        for _ in range(m):
                            state = state_for_vertex(cur, m, SCHEMA_JOIN)
                            delta = _phase_delta(cur, m)
                            bit = _phase_align_bit(cur, m)
                            visited_delta[state].add(delta)
                            visited_examples[(state, delta)] = tuple(cur)
                            visited_examples[(state, ("bit", bit))] = tuple(cur)
                            cur = color_map_from_table(table, SCHEMA_JOIN, m, cur, 0, STATE_SPACE_KEY)

        support_histogram = Counter(len(values) for values in visited_delta.values())
        layer_split = Counter()
        collision_rows = []
        for state, delta_values in visited_delta.items():
            if len(delta_values) <= 1:
                continue
            state_id = state_ids[state]
            bit_zero_example = visited_examples.get((state, ("bit", 0)))
            bit_one_example = visited_examples.get((state, ("bit", 1)))
            bit_split = bit_zero_example is not None and bit_one_example is not None
            if bit_split:
                layer_split[str(state[0])] += 1
            collision_rows.append(
                {
                    "state_id": state_id,
                    "orbit_id": orbit_index[state_id],
                    "state_name": state_name(state),
                    "state": {"layer_bucket": state[0], "signature": list(state[1])},
                    "delta_values": sorted(delta_values),
                    "delta_support_size": len(delta_values),
                    "phase_align_bit_split": bit_split,
                    "phase_align_example": list(bit_one_example) if bit_one_example is not None else None,
                    "phase_misaligned_example": list(bit_zero_example) if bit_zero_example is not None else None,
                }
            )
            collision_lookup_all[(m, state_id)] = collision_rows[-1]
        collision_rows.sort(
            key=lambda row: (
                0 if row["state"]["layer_bucket"] not in (2, 3, "4+") else -1,
                -row["delta_support_size"],
                str(row["state"]["layer_bucket"]),
                row["state_name"],
            )
        )
        per_m.append(
            {
                "m": m,
                "visited_state_count": len(visited_delta),
                "delta_support_histogram": {str(size): count for size, count in sorted(support_histogram.items())},
                "multi_delta_state_count": len(collision_rows),
                "phase_align_split_state_count": sum(1 for row in collision_rows if row["phase_align_bit_split"]),
                "phase_align_split_by_layer": dict(sorted(layer_split.items())),
                "collision_rows": collision_rows[:40],
            }
        )

    preferred_path = None
    for preferred_m in (7, 9, 5, 11, 13):
        if preferred_m in m_values:
            preferred_path = _canonical_background_path(table, m=preferred_m)
            break
    if preferred_path is not None:
        for row in preferred_path:
            if row["state"]["layer_bucket"] in (2, 3, "4+"):
                key = (preferred_m, row["state_id"])
                if key in collision_lookup_all and collision_lookup_all[key]["phase_align_bit_split"]:
                    canonical_tail_core = {"m": preferred_m, **collision_lookup_all[key]}
                    break
    if canonical_tail_core is None:
        for item in per_m:
            tail_candidates = [
                row
                for row in item["collision_rows"]
                if row["phase_align_bit_split"] and row["state"]["layer_bucket"] in (2, 3, "4+")
            ]
            if tail_candidates:
                tail_candidates.sort(
                    key=lambda row: (
                        _layer_sort_key(row["state"]["layer_bucket"]),
                        -row["delta_support_size"],
                        row["state_name"],
                    )
                )
                canonical_tail_core = {"m": item["m"], **tail_candidates[0]}
                break

    return {
        "candidate_bit": "phase_align := 1_{(v-q) mod m = 0}",
        "per_m": per_m,
        "canonical_tail_core": canonical_tail_core,
        "canonical_background_path": preferred_path,
    }


def _core_automaton(palette_by_layer: Dict[str, object], canonical_tail_core: Dict[str, object] | None) -> Dict[str, object]:
    return {
        "core_name": "kick-kick-freeze",
        "motifs": [
            {
                "motif_id": "M0_q_kick",
                "layer_buckets": [0],
                "constant_permutation": palette_by_layer["0"]["constant_permutation"],
                "color0_output": palette_by_layer["0"]["constant_color0_output"],
                "effect_on_qwvu": [1, 0, 0, 0],
                "effect_on_delta_v_minus_q": -1,
                "role": "first exceptional step; increments q",
            },
            {
                "motif_id": "M1_v_kick",
                "layer_buckets": [1],
                "constant_permutation": palette_by_layer["1"]["constant_permutation"],
                "color0_output": palette_by_layer["1"]["constant_color0_output"],
                "effect_on_qwvu": [0, 0, 1, 0],
                "effect_on_delta_v_minus_q": 1,
                "role": "second exceptional step; increments v and restores delta",
            },
            {
                "motif_id": "M2_freeze_tail",
                "layer_buckets": [2, 3, "4+"],
                "constant_permutation": palette_by_layer["2"]["constant_permutation"],
                "color0_output": palette_by_layer["2"]["constant_color0_output"],
                "effect_on_qwvu": [0, 0, 0, 0],
                "effect_on_delta_v_minus_q": 0,
                "role": "identity tail; preserves q,w,v,u during the remaining steps",
                "canonical_conflict_state": canonical_tail_core,
            },
        ],
        "transition_sequence": [
            {"from": "M0_q_kick", "to": "M1_v_kick"},
            {"from": "M1_v_kick", "to": "M2_freeze_tail"},
            {"from": "M2_freeze_tail", "to": "M2_freeze_tail"},
        ],
        "forced_return_law": "R_0(q,w,v,u) = (q+1, w, v+1, u)",
        "forced_hidden_invariant": "delta := v-q is preserved by one full return",
        "forced_section_return": "U_0 = id on (w,u)",
        "forced_monodromy": 0,
    }


def _candidate_refinement(collision_data: Dict[str, object]) -> Dict[str, object]:
    split_stats = []
    for item in collision_data["per_m"]:
        split_stats.append(
            {
                "m": item["m"],
                "multi_delta_state_count": item["multi_delta_state_count"],
                "phase_align_split_state_count": item["phase_align_split_state_count"],
                "phase_align_split_fraction": (
                    item["phase_align_split_state_count"] / item["multi_delta_state_count"]
                    if item["multi_delta_state_count"]
                    else 0.0
                ),
                "phase_align_split_by_layer": item["phase_align_split_by_layer"],
            }
        )

    canonical = collision_data["canonical_tail_core"]
    return {
        "bit_name": "phase_align",
        "relative_formula": "phase_align_c(x) = 1_{(v_c-q_c) mod m = 0}",
        "coordinate_formula": "phase_align_c(x) = 1_{(x_{c+3}-x_{c+1}) mod m = 0}",
        "why_this_bit": [
            "The stable return law preserves delta_c := v_c-q_c, so delta_c is the hidden phase that survives one full first return.",
            "Theta_AB merges many states with different delta_c values, including aligned and non-aligned phase fibers.",
            "Splitting phase_align_c is the smallest cyclic-equivariant refinement that separates those conflicting fibers without changing the rest of the grammar.",
        ],
        "split_statistics": split_stats,
        "canonical_conflict_state": canonical,
        "ready_for_next_search_rule": {
            "refined_quotient_name": "Theta_AB_plus_phase_align",
            "state_definition": "theta_plus(x) = (L(x), (s_c(x), phase_align_c(x))_{c in Z/5Z})",
            "existing_atoms": [
                "q_c = -1",
                "q_c + u_c = 1",
                "w_c + u_c = 2",
                "q_c + u_c = -1",
                "u_c = -1",
            ],
            "new_atom": "phase_align_c(x) = 1_{(x_{c+3}-x_{c+1}) mod m = 0}",
        },
    }


def run_analysis(field_json: Path, *, m_values: Sequence[int]) -> Dict[str, object]:
    start = time.perf_counter()
    field, table = _load_table(field_json)
    palette_by_layer = _palette_by_layer(field)
    return_law = _return_formula_summary(table, m_values=m_values)
    collision_data = _phase_collision_data(table, m_values=m_values)
    automaton = _core_automaton(palette_by_layer, collision_data["canonical_tail_core"])
    refinement = _candidate_refinement(collision_data)
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": {"python_version": platform.python_version(), "rich_version": _rich_version()},
        "field_json": str(field_json),
        "palette_by_layer": palette_by_layer,
        "return_law": return_law,
        "collapse_automaton": automaton,
        "phase_collision_data": collision_data,
        "candidate_refinement": refinement,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    canonical = summary["phase_collision_data"]["canonical_tail_core"]
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        f"return_law: {summary['return_law']['formula_checked']}",
        f"candidate_bit: {summary['candidate_refinement']['relative_formula']}",
    ]
    if canonical is not None:
        lines.append(
            f"tail_core: m={canonical['m']} state={canonical['state_name']} "
            f"delta={canonical['delta_values']} bit_split={canonical['phase_align_bit_split']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze the dynamic collapse core of the stable joined-quotient field.")
    parser.add_argument(
        "--field-json",
        type=Path,
        default=Path("artifacts/d5_join_quotient_001/data/best_stable_field.json"),
        help="stable joined-quotient field JSON",
    )
    parser.add_argument("--m-list", default="5,7,9,11,13", help="comma-separated moduli for deterministic checks")
    parser.add_argument("--out-dir", type=Path, required=True, help="write analysis artifacts into this directory")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    summary = run_analysis(args.field_json, m_values=_parse_m_list(args.m_list))

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "analysis_summary.json").write_text(json.dumps(summary, indent=2))
    (args.out_dir / "return_law_summary.json").write_text(json.dumps(summary["return_law"], indent=2))
    (args.out_dir / "return_automaton.json").write_text(json.dumps(summary["collapse_automaton"], indent=2))
    (args.out_dir / "minimal_collapse_core.json").write_text(
        json.dumps(
            {
                "task_id": TASK_ID,
                "palette_by_layer": summary["palette_by_layer"],
                "canonical_tail_core": summary["phase_collision_data"]["canonical_tail_core"],
                "forced_return_law": summary["return_law"]["formula_checked"],
            },
            indent=2,
        )
    )
    (args.out_dir / "phase_collision_table.json").write_text(json.dumps(summary["phase_collision_data"], indent=2))
    (args.out_dir / "candidate_refinement.json").write_text(json.dumps(summary["candidate_refinement"], indent=2))
    (args.out_dir / "canonical_background_path.json").write_text(
        json.dumps(summary["phase_collision_data"]["canonical_background_path"], indent=2)
    )

    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
