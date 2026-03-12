#!/usr/bin/env python3
"""Search the smallest static two-layer edge-controller family around mixed_008."""

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

TASK_ID = "D5-EDGE-TRANSDUCER-TWO-LAYER-029"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M = 11
REPRESENTATIVE_W0 = 0
REPRESENTATIVE_S0 = 0


@dataclass
class PreparedSearch:
    m: int
    pre: Dict[str, object]
    baseline_nexts_all: List[List[int]]
    baseline_anchor_rel: List[List[int]]
    layer1_sets: Dict[Tuple[int, int], List[List[int]]]
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
    layer3_left_sets = {(w0, s0): [[] for _ in range(DIM)] for w0 in range(m) for s0 in range(m)}
    layer3_right_sets = {(w0, s0): [[] for _ in range(DIM)] for w0 in range(m) for s0 in range(m)}

    coords = pre["coords"]
    for idx, vertex in enumerate(coords):
        layer = sum(vertex) % m
        if layer not in (1, 3):
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
            else:
                initial_row = (s - 2) % m
                layer3_left_sets[(w % m, initial_row)][color].append(idx)
                layer3_right_sets[((w - 1) % m, initial_row)][color].append(idx)

    return PreparedSearch(
        m=m,
        pre=pre,
        baseline_nexts_all=baseline_nexts_all,
        baseline_anchor_rel=baseline_anchor_rel,
        layer1_sets=layer1_sets,
        layer3_left_sets=layer3_left_sets,
        layer3_right_sets=layer3_right_sets,
    )


def _toggle_anchor(anchor: int) -> int:
    if anchor == 0:
        return 3
    if anchor == 3:
        return 0
    return anchor


def _candidate_target_sets(
    prepared: PreparedSearch,
    *,
    w0: int,
    s0: int,
    left_dir: int,
    right_dir: int,
) -> Dict[str, object]:
    step_by_dir = prepared.pre["step_by_dir"]
    m = prepared.m
    left_w = (w0 - 1) % m
    right_w = w0 % m

    left_targets: List[List[int]] = [[] for _ in range(DIM)]
    right_targets: List[List[int]] = [[] for _ in range(DIM)]
    overlap_sizes: List[int] = []
    for color in range(DIM):
        left_dir_abs = (left_dir + color) % DIM
        right_dir_abs = (right_dir + color) % DIM
        left_set = sorted({step_by_dir[left_dir_abs][idx] for idx in prepared.layer1_sets[(left_w, s0)][color]})
        right_set = sorted({step_by_dir[right_dir_abs][idx] for idx in prepared.layer1_sets[(right_w, s0)][color]})
        left_targets[color] = left_set
        right_targets[color] = right_set
        overlap_sizes.append(len(set(left_set) & set(right_set)))

    return {
        "left_targets": left_targets,
        "right_targets": right_targets,
        "overlap_sizes": overlap_sizes,
        "total_overlap": sum(overlap_sizes),
        "disjoint_by_color": all(value == 0 for value in overlap_sizes),
    }


def _build_candidate_nexts(
    prepared: PreparedSearch,
    *,
    w0: int,
    s0: int,
    left_dir: int,
    right_dir: int,
    left_layer2_dir: int,
    right_layer2_dir: int,
    cocycle_defect: str,
) -> Tuple[List[List[int]] | None, Dict[str, object]]:
    nexts_all = [row[:] for row in prepared.baseline_nexts_all]
    step_by_dir = prepared.pre["step_by_dir"]
    m = prepared.m
    left_w = (w0 - 1) % m
    right_w = w0 % m

    for color in range(DIM):
        left_dir_abs = (left_dir + color) % DIM
        right_dir_abs = (right_dir + color) % DIM
        for idx in prepared.layer1_sets[(left_w, s0)][color]:
            nexts_all[color][idx] = step_by_dir[left_dir_abs][idx]
        for idx in prepared.layer1_sets[(right_w, s0)][color]:
            nexts_all[color][idx] = step_by_dir[right_dir_abs][idx]

    target_sets = _candidate_target_sets(
        prepared,
        w0=w0,
        s0=s0,
        left_dir=left_dir,
        right_dir=right_dir,
    )
    left_targets = target_sets["left_targets"]
    right_targets = target_sets["right_targets"]

    conflict = False
    for color in range(DIM):
        overlap = set(left_targets[color]) & set(right_targets[color])
        if overlap and left_layer2_dir != right_layer2_dir:
            conflict = True
            break

    if conflict:
        return None, {
            "layer2_conflict": True,
            "layer2_target_total_overlap": int(target_sets["total_overlap"]),
            "layer2_overlap_sizes": list(target_sets["overlap_sizes"]),
            "layer2_disjoint_by_color": bool(target_sets["disjoint_by_color"]),
        }

    for color in range(DIM):
        left_dir_abs = (left_layer2_dir + color) % DIM
        right_dir_abs = (right_layer2_dir + color) % DIM
        for idx in left_targets[color]:
            nexts_all[color][idx] = step_by_dir[left_dir_abs][idx]
        for idx in right_targets[color]:
            nexts_all[color][idx] = step_by_dir[right_dir_abs][idx]

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

    return nexts_all, {
        "layer2_conflict": False,
        "layer2_target_total_overlap": int(target_sets["total_overlap"]),
        "layer2_overlap_sizes": list(target_sets["overlap_sizes"]),
        "layer2_disjoint_by_color": bool(target_sets["disjoint_by_color"]),
        "left_layer2_target_sizes": [len(row) for row in left_targets],
        "right_layer2_target_sizes": [len(row) for row in right_targets],
    }


def _candidate_metrics(
    prepared: PreparedSearch,
    *,
    w0: int,
    s0: int,
    left_dir: int,
    right_dir: int,
    left_layer2_dir: int,
    right_layer2_dir: int,
    cocycle_defect: str,
) -> Dict[str, object]:
    nexts_all, meta = _build_candidate_nexts(
        prepared,
        w0=w0,
        s0=s0,
        left_dir=left_dir,
        right_dir=right_dir,
        left_layer2_dir=left_layer2_dir,
        right_layer2_dir=right_layer2_dir,
        cocycle_defect=cocycle_defect,
    )
    row = {
        "w0": w0,
        "s0": s0,
        "left_dir": left_dir,
        "right_dir": right_dir,
        "left_layer2_dir": left_layer2_dir,
        "right_layer2_dir": right_layer2_dir,
        "cocycle_defect": cocycle_defect,
        **meta,
    }
    if nexts_all is None:
        row.update(
            {
                "latin_all_colors": False,
                "clean_frame": False,
                "strict_clock": False,
                "u_cycle_count": None,
                "u_cycle_lengths": [],
                "monodromies": [],
                "full_single_grouped_orbit": False,
            }
        )
        return row

    latin = incoming_latin_all(nexts_all)
    if not latin:
        row.update(
            {
                "latin_all_colors": False,
                "clean_frame": False,
                "strict_clock": False,
                "u_cycle_count": None,
                "u_cycle_lengths": [],
                "monodromies": [],
                "full_single_grouped_orbit": False,
            }
        )
        return row

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
    row.update(
        {
            "latin_all_colors": True,
            "clean_frame": bool(ret["clean_frame"]),
            "strict_clock": bool(ret["strict_clock"]),
            "u_cycle_count": int(ret["U_cycle_count"]),
            "u_cycle_lengths": list(ret["U_cycle_lengths"]),
            "monodromies": monodromies,
            "full_single_grouped_orbit": full_single,
        }
    )
    return row


def _rank_candidate(row: Mapping[str, object], m: int) -> Tuple[object, ...]:
    monodromy_score = max((gcd(int(value), m) for value in row["monodromies"]), default=m)
    max_cycle = max(row["u_cycle_lengths"] or [0])
    return (
        row["layer2_conflict"],
        not row["latin_all_colors"],
        not row["clean_frame"],
        not row["strict_clock"],
        not row["full_single_grouped_orbit"],
        row["u_cycle_count"] if row["u_cycle_count"] is not None else m * m + 1,
        -max_cycle,
        monodromy_score,
        not row["layer2_disjoint_by_color"],
        row["left_dir"],
        row["right_dir"],
        row["left_layer2_dir"],
        row["right_layer2_dir"],
        row["cocycle_defect"],
    )


def _iter_candidate_params() -> Iterable[Tuple[int, int, int, int, str]]:
    for left_dir in range(DIM):
        for right_dir in range(DIM):
            for left_layer2_dir in range(DIM):
                for right_layer2_dir in range(DIM):
                    for cocycle_defect in ("none", "left", "right", "both"):
                        yield left_dir, right_dir, left_layer2_dir, right_layer2_dir, cocycle_defect


def _search_one_m(prepared: PreparedSearch, *, w0: int, s0: int) -> Dict[str, object]:
    rows = []
    for left_dir, right_dir, left_layer2_dir, right_layer2_dir, cocycle_defect in _iter_candidate_params():
        rows.append(
            _candidate_metrics(
                prepared,
                w0=w0,
                s0=s0,
                left_dir=left_dir,
                right_dir=right_dir,
                left_layer2_dir=left_layer2_dir,
                right_layer2_dir=right_layer2_dir,
                cocycle_defect=cocycle_defect,
            )
        )

    rows.sort(key=lambda row: _rank_candidate(row, prepared.m))
    conflict_rows = [row for row in rows if row["layer2_conflict"]]
    latin_rows = [row for row in rows if row["latin_all_colors"]]
    clean_rows = [row for row in latin_rows if row["clean_frame"]]
    strict_rows = [row for row in clean_rows if row["strict_clock"]]
    target_rows = [row for row in strict_rows if row["full_single_grouped_orbit"]]
    disjoint_latin_rows = [row for row in latin_rows if row["layer2_disjoint_by_color"]]
    baseline_word_rows = [
        row
        for row in latin_rows
        if row["left_dir"] == 4
        and row["right_dir"] == 4
        and row["left_layer2_dir"] == 2
        and row["right_layer2_dir"] == 2
    ]
    endpoint_asymmetric_rows = [
        row
        for row in latin_rows
        if (
            row["left_dir"] != row["right_dir"]
            or row["left_layer2_dir"] != row["right_layer2_dir"]
        )
    ]
    nonbaseline_latin_rows = [row for row in latin_rows if row not in baseline_word_rows]

    return {
        "m": prepared.m,
        "candidate_count": len(rows),
        "layer2_conflict_count": len(conflict_rows),
        "latin_all_count": len(latin_rows),
        "latin_disjoint_count": len(disjoint_latin_rows),
        "baseline_word_latin_count": len(baseline_word_rows),
        "nonbaseline_latin_count": len(nonbaseline_latin_rows),
        "endpoint_asymmetric_latin_count": len(endpoint_asymmetric_rows),
        "clean_frame_count": len(clean_rows),
        "strict_clock_count": len(strict_rows),
        "full_single_grouped_orbit_count": len(target_rows),
        "latin_rows": latin_rows[:20],
        "best_rows": rows[:20],
        "target_rows": target_rows[:20],
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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the smallest static two-layer edge-controller family around mixed_008.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    start = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    mixed_rule = _mixed_rule()
    search_rows = []
    baseline_rows = []
    representative_control = None
    found_any_primary = False
    for m in PRIMARY_M_VALUES:
        prepared = _prepare_m(m, mixed_rule)
        baseline_rows.append(_baseline_control(prepared))
        summary = _search_one_m(prepared, w0=REPRESENTATIVE_W0, s0=REPRESENTATIVE_S0)
        search_rows.append(summary)
        if summary["target_rows"]:
            found_any_primary = True
            representative_control = summary["target_rows"][0]

    _write_json(out_dir / "baseline_controls.json", {"rows": baseline_rows})
    _write_json(out_dir / "two_layer_search_summary.json", {"rows": search_rows})

    control_rows = []
    if found_any_primary and representative_control is not None:
        prepared = _prepare_m(CONTROL_M, mixed_rule)
        control_rows.append(
            _candidate_metrics(
                prepared,
                w0=REPRESENTATIVE_W0,
                s0=REPRESENTATIVE_S0,
                left_dir=int(representative_control["left_dir"]),
                right_dir=int(representative_control["right_dir"]),
                left_layer2_dir=int(representative_control["left_layer2_dir"]),
                right_layer2_dir=int(representative_control["right_layer2_dir"]),
                cocycle_defect=str(representative_control["cocycle_defect"]),
            )
        )
    _write_json(out_dir / "control_m11_check.json", {"rows": control_rows})

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "representative_branch": {
            "w0": REPRESENTATIVE_W0,
            "s0": REPRESENTATIVE_S0,
            "branch": "diagonal_fixed_w",
        },
        "primary_m_values": list(PRIMARY_M_VALUES),
        "control_m": CONTROL_M,
        "search_file": str(out_dir / "two_layer_search_summary.json"),
        "baseline_file": str(out_dir / "baseline_controls.json"),
        "control_file": str(out_dir / "control_m11_check.json"),
        "strongest_supported_conclusion": (
            "This artifact tests the smallest static edge-controller family that upgrades the s44 endpoint signature "
            "from an abstract transducer to an actual two-layer local perturbation around mixed_008. The family "
            "modifies layer1 separately on the two endpoints of one fixed adjacent w-pair, then modifies the resulting "
            "layer2 current vertices separately, with the omitted row and omitted-edge cocycle defect handled exactly "
            "as in the reduced target."
        ),
        "recommended_reading_key": (
            "If the only Latin survivors are the baseline word with optional cocycle defect, then the smallest static "
            "two-layer edge-controller family is already blocked before the grouped-orbit target stage."
        ),
    }
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    for row in search_rows:
        print(
            f"m={row['m']}: candidates={row['candidate_count']} conflicts={row['layer2_conflict_count']} "
            f"latin={row['latin_all_count']} clean={row['clean_frame_count']} "
            f"strict={row['strict_clock_count']} target={row['full_single_grouped_orbit_count']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
