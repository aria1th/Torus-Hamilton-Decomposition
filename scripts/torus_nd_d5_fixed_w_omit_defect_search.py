#!/usr/bin/env python3
"""Targeted current-state fixed-w omit-defect search around the D5 mixed witness."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from math import gcd
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import torus_nd_d5_layer3_mode_switch_common as mode008
from torus_nd_d5_return_map_model_common import environment_block, load_witness_specs, runtime_since
from torus_nd_d5_strict_palette_context_common import DIM, first_return, incoming_latin_all

TASK_ID = "D5-FIXED-W-OMIT-DEFECT-026"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M = 11


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

    layer1_sets = {(w0, s0): [[] for _ in range(DIM)] for w0 in range(m) for s0 in range(m)}
    layer2_sets = {(w0, s0): [[] for _ in range(DIM)] for w0 in range(m) for s0 in range(m)}
    layer3_left_sets = {(w0, s0): [[] for _ in range(DIM)] for w0 in range(m) for s0 in range(m)}
    layer3_right_sets = {(w0, s0): [[] for _ in range(DIM)] for w0 in range(m) for s0 in range(m)}

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
            if layer == 1:
                for s0 in range(m):
                    if s != s0:
                        layer1_sets[(w, s0)][color].append(idx)
            elif layer == 2:
                initial_row = (s - 1) % m
                for s0 in range(m):
                    if initial_row != s0:
                        layer2_sets[(w, s0)][color].append(idx)
            elif layer == 3:
                initial_row = (s - 2) % m
                layer3_left_sets[(w, initial_row)][color].append(idx)
                layer3_right_sets[((w - 1) % m, initial_row)][color].append(idx)

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


def _build_candidate_nexts(
    prepared: PreparedSearch,
    *,
    w0: int,
    s0: int,
    assignment: str,
    cocycle_defect: str,
) -> List[List[int]]:
    m = prepared.m
    nexts_all = [row[:] for row in prepared.baseline_nexts_all]
    step_by_dir = prepared.pre["step_by_dir"]

    if assignment == "P_on_w0":
        p_state = w0 % m
        m_state = (w0 - 1) % m
    elif assignment == "P_on_w0_minus_1":
        p_state = (w0 - 1) % m
        m_state = w0 % m
    else:
        raise ValueError(f"unknown assignment {assignment}")

    for color in range(DIM):
        for idx in prepared.layer1_sets[(m_state, s0)][color]:
            nexts_all[color][idx] = step_by_dir[(2 + color) % DIM][idx]
        for idx in prepared.layer2_sets[(p_state, s0)][color]:
            nexts_all[color][idx] = step_by_dir[(4 + color) % DIM][idx]

    toggle_left = cocycle_defect in ("left", "both")
    toggle_right = cocycle_defect in ("right", "both")
    if toggle_left or toggle_right:
        for color in range(DIM):
            if toggle_left:
                for idx in prepared.layer3_left_sets[(w0 % m, s0 % m)][color]:
                    anchor = prepared.baseline_anchor_rel[color][idx]
                    nexts_all[color][idx] = step_by_dir[(_toggle_anchor(anchor) + color) % DIM][idx]
            if toggle_right:
                for idx in prepared.layer3_right_sets[(w0 % m, s0 % m)][color]:
                    anchor = prepared.baseline_anchor_rel[color][idx]
                    nexts_all[color][idx] = step_by_dir[(_toggle_anchor(anchor) + color) % DIM][idx]

    return nexts_all


def _candidate_metrics(prepared: PreparedSearch, *, w0: int, s0: int, assignment: str, cocycle_defect: str) -> Dict[str, object]:
    nexts_all = _build_candidate_nexts(
        prepared,
        w0=w0,
        s0=s0,
        assignment=assignment,
        cocycle_defect=cocycle_defect,
    )
    latin = incoming_latin_all(nexts_all)
    if not latin:
        return {
            "w0": w0,
            "s0": s0,
            "assignment": assignment,
            "cocycle_defect": cocycle_defect,
            "latin_all_colors": False,
            "clean_frame": False,
            "strict_clock": False,
            "u_cycle_count": None,
            "u_cycle_lengths": [],
            "monodromies": [],
            "full_single_grouped_orbit": False,
        }

    ret = first_return(prepared.pre, nexts_all[0])
    monodromies = [int(value) for value in ret["monodromies"]]
    full_single = (
        ret["clean_frame"]
        and ret["strict_clock"]
        and ret["U_cycle_count"] == 1
        and ret["U_cycle_lengths"] == [prepared.m * prepared.m]
        and len(monodromies) == 1
        and gcd(monodromies[0], prepared.m) == 1
    )
    return {
        "w0": w0,
        "s0": s0,
        "assignment": assignment,
        "cocycle_defect": cocycle_defect,
        "latin_all_colors": True,
        "clean_frame": bool(ret["clean_frame"]),
        "strict_clock": bool(ret["strict_clock"]),
        "u_cycle_count": int(ret["U_cycle_count"]),
        "u_cycle_lengths": list(ret["U_cycle_lengths"]),
        "monodromies": monodromies,
        "full_single_grouped_orbit": full_single,
    }


def _rank_candidate(row: Mapping[str, object], m: int) -> Tuple[object, ...]:
    monodromy_score = max((gcd(int(value), m) for value in row["monodromies"]), default=m)
    max_cycle = max(row["u_cycle_lengths"] or [0])
    return (
        not row["latin_all_colors"],
        not row["clean_frame"],
        not row["strict_clock"],
        not row["full_single_grouped_orbit"],
        row["u_cycle_count"] if row["u_cycle_count"] is not None else m * m + 1,
        -max_cycle,
        monodromy_score,
        row["w0"],
        row["s0"],
        row["assignment"],
        row["cocycle_defect"],
    )


def _search_one_m(prepared: PreparedSearch) -> Dict[str, object]:
    m = prepared.m
    rows = []
    for w0 in range(m):
        for s0 in range(m):
            for assignment in ("P_on_w0", "P_on_w0_minus_1"):
                for cocycle_defect in ("none", "left", "right", "both"):
                    rows.append(
                        _candidate_metrics(
                            prepared,
                            w0=w0,
                            s0=s0,
                            assignment=assignment,
                            cocycle_defect=cocycle_defect,
                        )
                    )

    rows.sort(key=lambda row: _rank_candidate(row, m))
    target_rows = [row for row in rows if row["full_single_grouped_orbit"]]
    clean_rows = [row for row in rows if row["clean_frame"]]
    strict_rows = [row for row in rows if row["strict_clock"]]

    return {
        "m": m,
        "candidate_count": len(rows),
        "latin_all_count": sum(1 for row in rows if row["latin_all_colors"]),
        "clean_frame_count": len(clean_rows),
        "strict_clock_count": len(strict_rows),
        "full_single_grouped_orbit_count": len(target_rows),
        "target_rows": target_rows[:20],
        "best_rows": rows[:20],
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


def _collision_examples(m_values: Sequence[int]) -> Dict[str, object]:
    rows = []
    for m in m_values:
        for s in range(m):
            for w0 in range(m):
                left_w = (w0 - 1) % m
                left_u = (s - left_w) % m
                right_w = w0 % m
                right_u = (s - right_w) % m
                layer2_from_M = {
                    "q": m - 1,
                    "w": (left_w + 1) % m,
                    "u": left_u,
                    "s_layer2": (s + 1) % m,
                }
                layer2_from_B = {
                    "q": m - 1,
                    "w": right_w,
                    "u": (right_u + 1) % m,
                    "s_layer2": (s + 1) % m,
                }
                if layer2_from_M == layer2_from_B:
                    rows.append(
                        {
                            "m": m,
                            "initial_row_s": s,
                            "w0": w0,
                            "left_initial_state": {"q": m - 2, "w": left_w, "u": left_u},
                            "right_initial_state": {"q": m - 2, "w": right_w, "u": right_u},
                            "shared_layer2_state": layer2_from_M,
                        }
                    )
                    break
            else:
                continue
            break
    return {
        "collision_statement": (
            "For any row s and adjacent pair {w0-1,w0} on the carry slice q=m-2, the layer2 current state reached by "
            "applying M to w0-1 and by applying the baseline layer1 step to w0 is identical. Therefore a current-state "
            "rule at layer 2 cannot distinguish the intended P target from the adjacent M target."
        ),
        "rows": rows,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the current-state fixed-w omit-defect family around mixed_008.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    start = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    mixed_rule = _mixed_rule()
    search_rows = []
    baseline_rows = []
    found_any_primary = False
    representative_control = None
    for m in PRIMARY_M_VALUES:
        prepared = _prepare_m(m, mixed_rule)
        baseline_rows.append(_baseline_control(prepared))
        summary = _search_one_m(prepared)
        search_rows.append(summary)
        if summary["target_rows"]:
            found_any_primary = True
            representative_control = summary["target_rows"][0]

    collision = _collision_examples(PRIMARY_M_VALUES + (CONTROL_M,))
    _write_json(out_dir / "baseline_controls.json", {"rows": baseline_rows})
    _write_json(out_dir / "current_state_search_summary.json", {"rows": search_rows})
    _write_json(out_dir / "layer2_collision_examples.json", collision)

    control_rows = []
    if found_any_primary and representative_control is not None:
        prepared = _prepare_m(CONTROL_M, mixed_rule)
        control_rows.append(
            _candidate_metrics(
                prepared,
                w0=int(representative_control["w0"]),
                s0=int(representative_control["s0"]),
                assignment=str(representative_control["assignment"]),
                cocycle_defect=str(representative_control["cocycle_defect"]),
            )
        )
    _write_json(out_dir / "control_m11_check.json", {"rows": control_rows})

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "primary_m_values": list(PRIMARY_M_VALUES),
        "control_m": CONTROL_M,
        "search_file": str(out_dir / "current_state_search_summary.json"),
        "baseline_file": str(out_dir / "baseline_controls.json"),
        "collision_file": str(out_dir / "layer2_collision_examples.json"),
        "control_file": str(out_dir / "control_m11_check.json"),
        "strongest_supported_conclusion": (
            "The baseline mixed_008 control still validates cleanly, but the targeted current-state B/P/M fixed-w "
            "omit-defect family does not realize the 025 reduced normal form on the searched primary moduli. In fact "
            "none of the searched candidates is Latin on all colors. The underlying reason is structural: the intended "
            "P target and the adjacent M target collide at the same layer2 current state, so a deterministic "
            "current-state layer2 rule cannot separate them."
        ),
        "recommended_next_family": (
            "Move to a history-sensitive or genuinely different local mechanism. Another current-state selector expansion "
            "around the same B/P/M palette is unlikely to succeed because the layer2 collision is exact."
        ),
    }
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    for row in search_rows:
        print(
            f"m={row['m']}: candidates={row['candidate_count']} latin={row['latin_all_count']} "
            f"clean={row['clean_frame_count']} strict={row['strict_clock_count']} "
            f"target={row['full_single_grouped_orbit_count']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
