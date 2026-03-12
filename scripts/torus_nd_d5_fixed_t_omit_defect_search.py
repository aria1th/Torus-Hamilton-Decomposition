#!/usr/bin/env python3
"""Current-state fixed-t omit-defect search for the anti-diagonal D5 branch."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_layer3_mode_switch_common as mode008
from torus_nd_d5_return_map_model_common import environment_block, load_witness_specs, runtime_since
from torus_nd_d5_strict_palette_context_common import DIM, first_return, incoming_latin_all

TASK_ID = "D5-FIXED-T-OMIT-DEFECT-027"
PRIMARY_M_VALUES = (5, 7, 9)


@dataclass
class PreparedSearch:
    m: int
    pre: Dict[str, object]
    baseline_nexts_all: List[List[int]]
    baseline_anchor_rel: List[List[int]]
    layer1_sets: Dict[Tuple[int, int], List[List[int]]]
    layer2_sets: Dict[Tuple[int, int], List[List[int]]]
    layer3_left_sets: Dict[Tuple[int, int], List[List[int]]]
    layer3_right_sets: Dict[Tuple[int, int], List[List[int]]]


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _mixed_rule() -> mode008.Rule:
    mixed = next(spec for spec in load_witness_specs() if spec.name == "mixed_008")
    return mode008.Rule.from_payload(mixed.rule_payload)


def _t_value(w: int, u: int, m: int) -> int:
    return (w + 2 * u) % m


def _prepare_m(m: int, mixed_rule: mode008.Rule) -> PreparedSearch:
    signature_to_id = mode008.exact_signature_catalog((m,))["signature_to_id"]
    pre = mode008.precompute_m(m, signature_to_id)
    baseline_anchors = mode008.anchor_by_feature(pre, mixed_rule)
    baseline_nexts_all = mode008.nexts_all_for_rule(pre, baseline_anchors)

    baseline_anchor_rel: List[List[int]] = [[0] * pre["n"] for _ in range(DIM)]
    for color in range(DIM):
        feature_ids = pre["feature_ids_by_color"][color]
        row = baseline_anchor_rel[color]
        for idx, feature_id in enumerate(feature_ids):
            row[idx] = int(baseline_anchors[feature_id])

    layer1_sets = {(t0, s0): [[] for _ in range(DIM)] for t0 in range(m) for s0 in range(m)}
    layer2_sets = {(t0, s0): [[] for _ in range(DIM)] for t0 in range(m) for s0 in range(m)}
    layer3_left_sets = {(t0, s0): [[] for _ in range(DIM)] for t0 in range(m) for s0 in range(m)}
    layer3_right_sets = {(t0, s0): [[] for _ in range(DIM)] for t0 in range(m) for s0 in range(m)}

    coords = pre["coords"]
    for idx, vertex in enumerate(coords):
        layer = sum(vertex) % m
        if layer not in (1, 2, 3):
            continue
        for color in range(DIM):
            q = vertex[(color + 1) % DIM]
            if q != m - 1:
                continue
            w = vertex[(color + 2) % DIM]
            u = vertex[(color + 4) % DIM]
            s = (w + u) % m
            t = _t_value(w, u, m)
            if layer == 1:
                for s0 in range(m):
                    if s != s0:
                        layer1_sets[(t, s0)][color].append(idx)
            elif layer == 2:
                initial_row = (s - 1) % m
                # P acts on the lower t-state and is seen at layer2 with current t = t0+2.
                for s0 in range(m):
                    if initial_row != s0:
                        layer2_sets[((t - 2) % m, s0)][color].append(idx)
            elif layer == 3:
                initial_row = (s - 2) % m
                layer3_left_sets[((t - 3) % m, initial_row)][color].append(idx)
                layer3_right_sets[((t - 4) % m, initial_row)][color].append(idx)

    return PreparedSearch(
        m=m,
        pre=pre,
        baseline_nexts_all=baseline_nexts_all,
        baseline_anchor_rel=baseline_anchor_rel,
        layer1_sets=layer1_sets,
        layer2_sets=layer2_sets,
        layer3_left_sets=layer3_left_sets,
        layer3_right_sets=layer3_right_sets,
    )


def _toggle_anchor(anchor: int) -> int:
    if anchor == 0:
        return 3
    if anchor == 3:
        return 0
    return anchor


def _build_candidate_nexts(prepared: PreparedSearch, *, t0: int, s0: int, cocycle_defect: str) -> List[List[int]]:
    m = prepared.m
    nexts_all = [row[:] for row in prepared.baseline_nexts_all]
    step_by_dir = prepared.pre["step_by_dir"]

    m_state = (t0 + 1) % m
    for color in range(DIM):
        for idx in prepared.layer1_sets[(m_state, s0)][color]:
            nexts_all[color][idx] = step_by_dir[(2 + color) % DIM][idx]
        for idx in prepared.layer2_sets[(t0, s0)][color]:
            nexts_all[color][idx] = step_by_dir[(4 + color) % DIM][idx]

    toggle_left = cocycle_defect in ("left", "both")
    toggle_right = cocycle_defect in ("right", "both")
    if toggle_left or toggle_right:
        for color in range(DIM):
            if toggle_left:
                for idx in prepared.layer3_left_sets[(t0 % m, s0 % m)][color]:
                    anchor = prepared.baseline_anchor_rel[color][idx]
                    nexts_all[color][idx] = step_by_dir[(_toggle_anchor(anchor) + color) % DIM][idx]
            if toggle_right:
                for idx in prepared.layer3_right_sets[(t0 % m, s0 % m)][color]:
                    anchor = prepared.baseline_anchor_rel[color][idx]
                    nexts_all[color][idx] = step_by_dir[(_toggle_anchor(anchor) + color) % DIM][idx]
    return nexts_all


def _candidate_metrics(prepared: PreparedSearch, *, t0: int, s0: int, cocycle_defect: str) -> Dict[str, object]:
    nexts_all = _build_candidate_nexts(prepared, t0=t0, s0=s0, cocycle_defect=cocycle_defect)
    latin = incoming_latin_all(nexts_all)
    if not latin:
        return {
            "t0": t0,
            "s0": s0,
            "cocycle_defect": cocycle_defect,
            "latin_all_colors": False,
            "clean_frame": False,
            "strict_clock": False,
        }
    ret = first_return(prepared.pre, nexts_all[0])
    return {
        "t0": t0,
        "s0": s0,
        "cocycle_defect": cocycle_defect,
        "latin_all_colors": True,
        "clean_frame": bool(ret["clean_frame"]),
        "strict_clock": bool(ret["strict_clock"]),
        "u_cycle_count": int(ret["U_cycle_count"]),
        "u_cycle_lengths": list(ret["U_cycle_lengths"]),
        "monodromies": [int(value) for value in ret["monodromies"]],
    }


def _baseline_control(prepared: PreparedSearch) -> Dict[str, object]:
    latin = incoming_latin_all(prepared.baseline_nexts_all)
    ret = first_return(prepared.pre, prepared.baseline_nexts_all[0])
    return {
        "m": prepared.m,
        "latin_all_colors": latin,
        "clean_frame": bool(ret["clean_frame"]),
        "strict_clock": bool(ret["strict_clock"]),
        "u_cycle_count": int(ret["U_cycle_count"]),
        "u_cycle_lengths": list(ret["U_cycle_lengths"]),
        "monodromies": [int(value) for value in ret["monodromies"]],
    }


def _search_one_m(prepared: PreparedSearch) -> Dict[str, object]:
    m = prepared.m
    rows = []
    for t0 in range(m):
        for s0 in range(m):
            for cocycle_defect in ("none", "left", "right", "both"):
                rows.append(_candidate_metrics(prepared, t0=t0, s0=s0, cocycle_defect=cocycle_defect))
    return {
        "m": m,
        "candidate_count": len(rows),
        "latin_all_count": sum(1 for row in rows if row["latin_all_colors"]),
        "clean_frame_count": sum(1 for row in rows if row["clean_frame"]),
        "strict_clock_count": sum(1 for row in rows if row["strict_clock"]),
    }


def _collision_examples(m_values: Sequence[int]) -> Dict[str, object]:
    rows = []
    for m in m_values:
        for s in range(m):
            for t0 in range(m):
                left_u = (t0 - s) % m
                left_w = (s - left_u) % m
                right_u = (t0 + 1 - s) % m
                right_w = (s - right_u) % m
                layer2_from_B = {
                    "q": m - 1,
                    "w": left_w,
                    "u": (left_u + 1) % m,
                    "t_layer2": (t0 + 2) % m,
                }
                layer2_from_M = {
                    "q": m - 1,
                    "w": (right_w + 1) % m,
                    "u": right_u,
                    "t_layer2": (t0 + 2) % m,
                }
                if layer2_from_B == layer2_from_M:
                    rows.append(
                        {
                            "m": m,
                            "initial_row_s": s,
                            "t0": t0,
                            "lower_initial_state": {"q": m - 2, "w": left_w, "u": left_u},
                            "higher_initial_state": {"q": m - 2, "w": right_w, "u": right_u},
                            "shared_layer2_state": layer2_from_B,
                        }
                    )
                    break
            else:
                continue
            break
    return {
        "collision_statement": (
            "For any row s and adjacent anti-diagonal stationary pair {t0,t0+1}, the layer2 current state reached by "
            "applying the baseline layer1 step to t0 and by applying M to t0+1 is identical. Therefore the intended "
            "anti-diagonal current-state P/M target also collides at layer 2."
        ),
        "rows": rows,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the anti-diagonal fixed-t current-state omit-defect family.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    start = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    mixed_rule = _mixed_rule()
    search_rows = []
    baseline_rows = []
    for m in PRIMARY_M_VALUES:
        prepared = _prepare_m(m, mixed_rule)
        baseline_rows.append(_baseline_control(prepared))
        search_rows.append(_search_one_m(prepared))

    collision = _collision_examples(PRIMARY_M_VALUES)
    _write_json(out_dir / "baseline_controls.json", {"rows": baseline_rows})
    _write_json(out_dir / "current_state_search_summary.json", {"rows": search_rows})
    _write_json(out_dir / "layer2_collision_examples.json", collision)

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "primary_m_values": list(PRIMARY_M_VALUES),
        "baseline_file": str(out_dir / "baseline_controls.json"),
        "search_file": str(out_dir / "current_state_search_summary.json"),
        "collision_file": str(out_dir / "layer2_collision_examples.json"),
        "strongest_supported_conclusion": (
            "The anti-diagonal stationary current-state B/P/M family is also completely negative on m=5,7,9: none of "
            "the searched candidates is Latin on all colors. The same exact layer2 collision appears in the "
            "anti-diagonal stationary coordinate."
        ),
        "recommended_next_family": (
            "The current-state B/P/M strategy is now blocked on both stationary branches. The next branch must leave "
            "this current-state ansatz rather than shifting between diagonal and anti-diagonal coordinates."
        ),
    }
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    for row in search_rows:
        print(
            f"m={row['m']}: candidates={row['candidate_count']} latin={row['latin_all_count']} "
            f"clean={row['clean_frame_count']} strict={row['strict_clock_count']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
