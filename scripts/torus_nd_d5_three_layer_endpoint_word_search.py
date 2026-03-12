#!/usr/bin/env python3
"""Search a static three-layer endpoint-word family around mixed_008."""

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

TASK_ID = "D5-THREE-LAYER-ENDPOINT-WORD-031"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M = 11
REPRESENTATIVE_W0 = 0
REPRESENTATIVE_S0 = 0
PLUS_WORDS = ((1, 2, 2), (2, 1, 2), (2, 2, 1))
MINUS_WORDS = ((1, 4, 4), (4, 1, 4), (4, 4, 1))


@dataclass
class PreparedSearch:
    m: int
    pre: Dict[str, object]
    baseline_nexts_all: List[List[int]]
    baseline_anchor_rel: List[List[int]]
    layer1_sets: Dict[Tuple[int, int], List[List[int]]]
    omitted_layer3_left_sets: Dict[Tuple[int, int], List[List[int]]]
    omitted_layer3_right_sets: Dict[Tuple[int, int], List[List[int]]]


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
    omitted_layer3_left_sets = {(w0, s0): [[] for _ in range(DIM)] for w0 in range(m) for s0 in range(m)}
    omitted_layer3_right_sets = {(w0, s0): [[] for _ in range(DIM)] for w0 in range(m) for s0 in range(m)}

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
                omitted_layer3_left_sets[(w % m, initial_row)][color].append(idx)
                omitted_layer3_right_sets[((w - 1) % m, initial_row)][color].append(idx)

    return PreparedSearch(
        m=m,
        pre=pre,
        baseline_nexts_all=baseline_nexts_all,
        baseline_anchor_rel=baseline_anchor_rel,
        layer1_sets=layer1_sets,
        omitted_layer3_left_sets=omitted_layer3_left_sets,
        omitted_layer3_right_sets=omitted_layer3_right_sets,
    )


def _toggle_anchor(anchor: int) -> int:
    if anchor == 0:
        return 3
    if anchor == 3:
        return 0
    return anchor


def _iter_candidate_words() -> Iterable[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]:
    for left_word in PLUS_WORDS + MINUS_WORDS:
        right_pool = MINUS_WORDS if left_word in PLUS_WORDS else PLUS_WORDS
        for right_word in right_pool:
            yield left_word, right_word


def _build_candidate_nexts(
    prepared: PreparedSearch,
    *,
    w0: int,
    s0: int,
    left_word: Tuple[int, int, int],
    right_word: Tuple[int, int, int],
    cocycle_defect: str,
) -> Tuple[List[List[int]] | None, Dict[str, object]]:
    nexts_all = [row[:] for row in prepared.baseline_nexts_all]
    step_by_dir = prepared.pre["step_by_dir"]
    m = prepared.m
    left_w = (w0 - 1) % m
    right_w = w0 % m

    layer2_left_targets: List[List[int]] = [[] for _ in range(DIM)]
    layer2_right_targets: List[List[int]] = [[] for _ in range(DIM)]
    layer3_left_targets: List[List[int]] = [[] for _ in range(DIM)]
    layer3_right_targets: List[List[int]] = [[] for _ in range(DIM)]
    layer2_overlap_sizes: List[int] = []
    layer3_overlap_sizes: List[int] = []

    for color in range(DIM):
        left_dir1 = (left_word[0] + color) % DIM
        right_dir1 = (right_word[0] + color) % DIM
        left_sources = prepared.layer1_sets[(left_w, s0)][color]
        right_sources = prepared.layer1_sets[(right_w, s0)][color]

        for idx in left_sources:
            nexts_all[color][idx] = step_by_dir[left_dir1][idx]
        for idx in right_sources:
            nexts_all[color][idx] = step_by_dir[right_dir1][idx]

        left2 = sorted({step_by_dir[left_dir1][idx] for idx in left_sources})
        right2 = sorted({step_by_dir[right_dir1][idx] for idx in right_sources})
        layer2_left_targets[color] = left2
        layer2_right_targets[color] = right2
        layer2_overlap_sizes.append(len(set(left2) & set(right2)))

    layer2_conflict = any(layer2_overlap_sizes) and left_word[1] != right_word[1]
    if layer2_conflict:
        return None, {
            "layer2_conflict": True,
            "layer3_conflict": False,
            "layer2_overlap_sizes": layer2_overlap_sizes,
            "layer3_overlap_sizes": [],
            "layer2_disjoint_by_color": all(value == 0 for value in layer2_overlap_sizes),
            "layer3_disjoint_by_color": False,
        }

    for color in range(DIM):
        left_dir2 = (left_word[1] + color) % DIM
        right_dir2 = (right_word[1] + color) % DIM
        for idx in layer2_left_targets[color]:
            nexts_all[color][idx] = step_by_dir[left_dir2][idx]
        for idx in layer2_right_targets[color]:
            nexts_all[color][idx] = step_by_dir[right_dir2][idx]

        left3 = sorted({step_by_dir[left_dir2][idx] for idx in layer2_left_targets[color]})
        right3 = sorted({step_by_dir[right_dir2][idx] for idx in layer2_right_targets[color]})
        layer3_left_targets[color] = left3
        layer3_right_targets[color] = right3
        layer3_overlap_sizes.append(len(set(left3) & set(right3)))

    layer3_conflict = any(layer3_overlap_sizes) and left_word[2] != right_word[2]
    if layer3_conflict:
        return None, {
            "layer2_conflict": False,
            "layer3_conflict": True,
            "layer2_overlap_sizes": layer2_overlap_sizes,
            "layer3_overlap_sizes": layer3_overlap_sizes,
            "layer2_disjoint_by_color": all(value == 0 for value in layer2_overlap_sizes),
            "layer3_disjoint_by_color": all(value == 0 for value in layer3_overlap_sizes),
        }

    for color in range(DIM):
        left_dir3 = (left_word[2] + color) % DIM
        right_dir3 = (right_word[2] + color) % DIM
        for idx in layer3_left_targets[color]:
            nexts_all[color][idx] = step_by_dir[left_dir3][idx]
        for idx in layer3_right_targets[color]:
            nexts_all[color][idx] = step_by_dir[right_dir3][idx]

    toggle_left = cocycle_defect in ("left", "both")
    toggle_right = cocycle_defect in ("right", "both")
    if toggle_left or toggle_right:
        for color in range(DIM):
            if toggle_left:
                for idx in prepared.omitted_layer3_left_sets[(w0 % m, s0 % m)][color]:
                    anchor = prepared.baseline_anchor_rel[color][idx]
                    nexts_all[color][idx] = step_by_dir[(_toggle_anchor(anchor) + color) % DIM][idx]
            if toggle_right:
                for idx in prepared.omitted_layer3_right_sets[(w0 % m, s0 % m)][color]:
                    anchor = prepared.baseline_anchor_rel[color][idx]
                    nexts_all[color][idx] = step_by_dir[(_toggle_anchor(anchor) + color) % DIM][idx]

    return nexts_all, {
        "layer2_conflict": False,
        "layer3_conflict": False,
        "layer2_overlap_sizes": layer2_overlap_sizes,
        "layer3_overlap_sizes": layer3_overlap_sizes,
        "layer2_disjoint_by_color": all(value == 0 for value in layer2_overlap_sizes),
        "layer3_disjoint_by_color": all(value == 0 for value in layer3_overlap_sizes),
    }


def _candidate_metrics(
    prepared: PreparedSearch,
    *,
    w0: int,
    s0: int,
    left_word: Tuple[int, int, int],
    right_word: Tuple[int, int, int],
    cocycle_defect: str,
) -> Dict[str, object]:
    nexts_all, meta = _build_candidate_nexts(
        prepared,
        w0=w0,
        s0=s0,
        left_word=left_word,
        right_word=right_word,
        cocycle_defect=cocycle_defect,
    )
    row = {
        "w0": w0,
        "s0": s0,
        "left_word": list(left_word),
        "right_word": list(right_word),
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
        row["layer3_conflict"],
        not row["latin_all_colors"],
        not row["clean_frame"],
        not row["strict_clock"],
        not row["full_single_grouped_orbit"],
        row["u_cycle_count"] if row["u_cycle_count"] is not None else m * m + 1,
        -max_cycle,
        monodromy_score,
        not row["layer2_disjoint_by_color"],
        not row["layer3_disjoint_by_color"],
        row["left_word"],
        row["right_word"],
        row["cocycle_defect"],
    )


def _search_one_m(prepared: PreparedSearch, *, w0: int, s0: int) -> Dict[str, object]:
    rows = []
    for left_word, right_word in _iter_candidate_words():
        for cocycle_defect in ("none", "left", "right", "both"):
            rows.append(
                _candidate_metrics(
                    prepared,
                    w0=w0,
                    s0=s0,
                    left_word=left_word,
                    right_word=right_word,
                    cocycle_defect=cocycle_defect,
                )
            )

    rows.sort(key=lambda row: _rank_candidate(row, prepared.m))
    latin_rows = [row for row in rows if row["latin_all_colors"]]
    clean_rows = [row for row in latin_rows if row["clean_frame"]]
    strict_rows = [row for row in clean_rows if row["strict_clock"]]
    target_rows = [row for row in strict_rows if row["full_single_grouped_orbit"]]
    return {
        "m": prepared.m,
        "candidate_count": len(rows),
        "layer2_conflict_count": sum(1 for row in rows if row["layer2_conflict"]),
        "layer3_conflict_count": sum(1 for row in rows if row["layer3_conflict"]),
        "latin_all_count": len(latin_rows),
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
    parser = argparse.ArgumentParser(description="Search a static three-layer endpoint-word family around mixed_008.")
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
    _write_json(out_dir / "three_layer_search_summary.json", {"rows": search_rows})

    control_rows = []
    if found_any_primary and representative_control is not None:
        prepared = _prepare_m(CONTROL_M, mixed_rule)
        control_rows.append(
            _candidate_metrics(
                prepared,
                w0=REPRESENTATIVE_W0,
                s0=REPRESENTATIVE_S0,
                left_word=tuple(int(value) for value in representative_control["left_word"]),
                right_word=tuple(int(value) for value in representative_control["right_word"]),
                cocycle_defect=str(representative_control["cocycle_defect"]),
            )
        )
    _write_json(out_dir / "control_m11_check.json", {"rows": control_rows})

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "representative_branch": {"w0": REPRESENTATIVE_W0, "s0": REPRESENTATIVE_S0, "branch": "diagonal_fixed_w"},
        "primary_m_values": list(PRIMARY_M_VALUES),
        "control_m": CONTROL_M,
        "search_file": str(out_dir / "three_layer_search_summary.json"),
        "baseline_file": str(out_dir / "baseline_controls.json"),
        "control_file": str(out_dir / "control_m11_check.json"),
        "strongest_supported_conclusion": (
            "This artifact promotes the nonbaseline 3-step endpoint words found in 030 into the smallest static "
            "three-layer local family around mixed_008. It is the first exact family that genuinely leaves the "
            "two-layer endpoint-controller scope pruned by 029 while still staying tightly matched to the reduced "
            "025 target."
        ),
    }
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    for row in search_rows:
        print(
            f"m={row['m']}: candidates={row['candidate_count']} l2_conflicts={row['layer2_conflict_count']} "
            f"l3_conflicts={row['layer3_conflict_count']} latin={row['latin_all_count']} "
            f"clean={row['clean_frame_count']} strict={row['strict_clock_count']} "
            f"target={row['full_single_grouped_orbit_count']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
