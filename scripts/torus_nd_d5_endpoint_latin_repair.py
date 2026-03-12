#!/usr/bin/env python3
"""Collision extraction and micro-family Latin repair search for D5 endpoint seeds."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from math import gcd
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, Sequence, Tuple

import torus_nd_d5_layer3_mode_switch_common as mode008
from torus_nd_d5_return_map_model_common import environment_block, load_witness_specs, runtime_since
from torus_nd_d5_strict_palette_context_common import DIM, first_return, incoming_latin_all

TASK_ID = "D5-ENDPOINT-LATIN-REPAIR-032"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M = 11
REPRESENTATIVE_W0 = 0
REPRESENTATIVE_S0 = 0
TOP_SEEDS_FOR_REPAIR = 3
CLASS_LABELS = ("L1", "R1", "L2", "R2", "L3", "R3")


@dataclass
class PreparedSearch:
    m: int
    pre: Dict[str, object]
    baseline_nexts_all: List[List[int]]
    baseline_anchor_rel: List[List[int]]
    baseline_prev_all: List[List[int]]
    layer1_sets: Dict[Tuple[int, int], List[List[int]]]
    omitted_layer3_left_sets: Dict[Tuple[int, int], List[List[int]]]
    omitted_layer3_right_sets: Dict[Tuple[int, int], List[List[int]]]


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _load_json(path: str | Path) -> Mapping[str, object]:
    return json.loads(Path(path).read_text())


def _mixed_rule() -> mode008.Rule:
    mixed = next(spec for spec in load_witness_specs() if spec.name == "mixed_008")
    return mode008.Rule.from_payload(mixed.rule_payload)


def _invert_perm(nexts: Sequence[int]) -> List[int]:
    prev = [-1] * len(nexts)
    for idx, nxt in enumerate(nexts):
        prev[nxt] = idx
    if any(value < 0 for value in prev):
        raise ValueError("permutation inverse requested for non-permutation row")
    return prev


def _prepare_m(m: int, mixed_rule: mode008.Rule) -> PreparedSearch:
    signature_to_id = mode008.exact_signature_catalog((m,))["signature_to_id"]
    pre = mode008.precompute_m(m, signature_to_id)
    baseline_anchors = mode008.anchor_by_feature(pre, mixed_rule)
    baseline_nexts_all = mode008.nexts_all_for_rule(pre, baseline_anchors)
    baseline_prev_all = [_invert_perm(row) for row in baseline_nexts_all]

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
        baseline_prev_all=baseline_prev_all,
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


def _load_seed_pairs() -> List[Dict[str, object]]:
    rows = list(_load_json("artifacts/d5_endpoint_word_catalog_030/data/candidate_pairs.json")["rows"])
    filtered = [row for row in rows if row["distinct_layer2_across_m"] and row["distinct_layer3_across_m"]]
    for idx, row in enumerate(filtered):
        row["seed_id"] = idx
    return filtered


def _class_index_map(labels: Sequence[str]) -> Dict[str, List[int]]:
    out: Dict[str, List[int]] = {}
    for idx, label in enumerate(labels):
        out.setdefault(label, []).append(idx)
    return out


def _build_candidate(
    prepared: PreparedSearch,
    *,
    w0: int,
    s0: int,
    left_word: Tuple[int, int, int],
    right_word: Tuple[int, int, int],
    cocycle_defect: str = "none",
    repair: Mapping[str, object] | None = None,
) -> Tuple[List[List[int]] | None, Dict[str, object]]:
    nexts_all = [row[:] for row in prepared.baseline_nexts_all]
    step_by_dir = prepared.pre["step_by_dir"]
    m = prepared.m
    left_w = (w0 - 1) % m
    right_w = w0 % m
    labels_by_color = [["B"] * prepared.pre["n"] for _ in range(DIM)]
    class_dirs_by_color = [{"B": None} for _ in range(DIM)]

    layer2_overlap_sizes: List[int] = []
    layer3_overlap_sizes: List[int] = []
    layer2_left_targets_all: List[List[int]] = [[] for _ in range(DIM)]
    layer2_right_targets_all: List[List[int]] = [[] for _ in range(DIM)]
    layer3_left_targets_all: List[List[int]] = [[] for _ in range(DIM)]
    layer3_right_targets_all: List[List[int]] = [[] for _ in range(DIM)]

    for color in range(DIM):
        labels = labels_by_color[color]
        class_dirs = class_dirs_by_color[color]

        left_sources = prepared.layer1_sets[(left_w, s0)][color]
        right_sources = prepared.layer1_sets[(right_w, s0)][color]
        left_dir1 = (left_word[0] + color) % DIM
        right_dir1 = (right_word[0] + color) % DIM
        class_dirs["L1"] = left_dir1
        class_dirs["R1"] = right_dir1
        for idx in left_sources:
            nexts_all[color][idx] = step_by_dir[left_dir1][idx]
            labels[idx] = "L1"
        for idx in right_sources:
            nexts_all[color][idx] = step_by_dir[right_dir1][idx]
            labels[idx] = "R1"

        left2 = sorted({step_by_dir[left_dir1][idx] for idx in left_sources})
        right2 = sorted({step_by_dir[right_dir1][idx] for idx in right_sources})
        layer2_left_targets_all[color] = left2
        layer2_right_targets_all[color] = right2
        overlap2 = len(set(left2) & set(right2))
        layer2_overlap_sizes.append(overlap2)
        if overlap2 and left_word[1] != right_word[1]:
            return None, {
                "layer2_conflict": True,
                "layer3_conflict": False,
                "layer2_overlap_sizes": layer2_overlap_sizes,
                "layer3_overlap_sizes": layer3_overlap_sizes,
            }

        left_dir2 = (left_word[1] + color) % DIM
        right_dir2 = (right_word[1] + color) % DIM
        class_dirs["L2"] = left_dir2
        class_dirs["R2"] = right_dir2
        for idx in left2:
            nexts_all[color][idx] = step_by_dir[left_dir2][idx]
            labels[idx] = "L2"
        for idx in right2:
            nexts_all[color][idx] = step_by_dir[right_dir2][idx]
            labels[idx] = "R2"

        left3 = sorted({step_by_dir[left_dir2][idx] for idx in left2})
        right3 = sorted({step_by_dir[right_dir2][idx] for idx in right2})
        layer3_left_targets_all[color] = left3
        layer3_right_targets_all[color] = right3
        overlap3 = len(set(left3) & set(right3))
        layer3_overlap_sizes.append(overlap3)
        if overlap3 and left_word[2] != right_word[2]:
            return None, {
                "layer2_conflict": False,
                "layer3_conflict": True,
                "layer2_overlap_sizes": layer2_overlap_sizes,
                "layer3_overlap_sizes": layer3_overlap_sizes,
            }

        left_dir3 = (left_word[2] + color) % DIM
        right_dir3 = (right_word[2] + color) % DIM
        class_dirs["L3"] = left_dir3
        class_dirs["R3"] = right_dir3
        for idx in left3:
            nexts_all[color][idx] = step_by_dir[left_dir3][idx]
            labels[idx] = "L3"
        for idx in right3:
            nexts_all[color][idx] = step_by_dir[right_dir3][idx]
            labels[idx] = "R3"

    if repair is not None:
        bit_name = str(repair.get("bit_name", ""))
        label_name = str(repair["label"])
        alt_dir_rel = int(repair["alt_dir"])
        target_bit = int(repair.get("bit_value", 1))
        for color in range(DIM):
            labels = labels_by_color[color]
            prev_row = prepared.baseline_prev_all[color]
            succ_row = prepared.baseline_nexts_all[color]
            class_dirs = class_dirs_by_color[color]
            rel_to_abs = lambda rel_dir: (rel_dir + color) % DIM

            def bit_value(idx: int) -> int:
                current = labels[idx]
                pred = labels[prev_row[idx]]
                succ = labels[succ_row[idx]]
                if bit_name == "pred_changed":
                    return int(pred != "B")
                if bit_name == "pred_left":
                    return int(pred.startswith("L"))
                if bit_name == "pred_right":
                    return int(pred.startswith("R"))
                if bit_name == "pred_deep":
                    return int(pred in {"L2", "R2", "L3", "R3"})
                if bit_name == "succ_changed":
                    return int(succ != "B")
                if bit_name == "succ_left":
                    return int(succ.startswith("L"))
                if bit_name == "succ_right":
                    return int(succ.startswith("R"))
                if bit_name == "succ_deep":
                    return int(succ in {"L2", "R2", "L3", "R3"})
                if bit_name == "self_deep":
                    return int(current in {"L2", "R2", "L3", "R3"})
                if bit_name == "self_stage3":
                    return int(current in {"L3", "R3"})
                raise ValueError(f"unknown bit {bit_name!r}")

            rel_dir = alt_dir_rel
            abs_dir = rel_to_abs(rel_dir)
            for idx, current in enumerate(labels):
                if current != label_name:
                    continue
                if bit_name:
                    if bit_value(idx) != target_bit:
                        continue
                nexts_all[color][idx] = step_by_dir[abs_dir][idx]
                class_dirs[f"repair:{label_name}:{bit_name}:{target_bit}"] = abs_dir

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
        "labels_by_color": labels_by_color,
        "class_dirs_by_color": class_dirs_by_color,
        "class_index_maps": [_class_index_map(labels) for labels in labels_by_color],
    }


def _coords_payload(prepared: PreparedSearch, idx: int) -> Dict[str, int]:
    coords = prepared.pre["coords"][idx]
    return {
        "x0": int(coords[0]),
        "q": int(coords[1]),
        "w": int(coords[2]),
        "v": int(coords[3]),
        "u": int(coords[4]),
        "s": int((coords[2] + coords[4]) % prepared.m),
        "layer": int(sum(coords) % prepared.m),
    }


def _collision_profile_for_m(
    prepared: PreparedSearch,
    *,
    left_word: Tuple[int, int, int],
    right_word: Tuple[int, int, int],
) -> Dict[str, object]:
    nexts_all, meta = _build_candidate(
        prepared,
        w0=REPRESENTATIVE_W0,
        s0=REPRESENTATIVE_S0,
        left_word=left_word,
        right_word=right_word,
        cocycle_defect="none",
        repair=None,
    )
    if nexts_all is None:
        return {
            "m": prepared.m,
            "layer2_conflict": bool(meta["layer2_conflict"]),
            "layer3_conflict": bool(meta["layer3_conflict"]),
            "layer2_overlap_sizes": list(meta["layer2_overlap_sizes"]),
            "layer3_overlap_sizes": list(meta["layer3_overlap_sizes"]),
        }

    labels_by_color = meta["labels_by_color"]
    overfull_examples = []
    changed_label_counts: Dict[str, int] = {}
    pred_cur_signature_counts: Dict[str, int] = {}
    cur_succ_signature_counts: Dict[str, int] = {}
    bit_names = (
        "pred_changed",
        "pred_left",
        "pred_right",
        "pred_deep",
        "succ_changed",
        "succ_left",
        "succ_right",
        "succ_deep",
        "self_deep",
        "self_stage3",
    )
    separated_targets_by_bit = {name: 0 for name in bit_names}
    separated_targets_pred_cur = 0
    separated_targets_cur_succ = 0
    overfull_target_count = 0
    hole_target_count = 0
    excess_incoming_total = 0

    for color in range(DIM):
        row = nexts_all[color]
        indegree = [0] * prepared.pre["n"]
        incoming: List[List[int]] = [[] for _ in range(prepared.pre["n"])]
        for idx, nxt in enumerate(row):
            indegree[nxt] += 1
            incoming[nxt].append(idx)
        hole_target_count += sum(1 for value in indegree if value == 0)

        labels = labels_by_color[color]
        prev_row = prepared.baseline_prev_all[color]
        succ_row = prepared.baseline_nexts_all[color]

        def bit_value(name: str, idx: int) -> int:
            current = labels[idx]
            pred = labels[prev_row[idx]]
            succ = labels[succ_row[idx]]
            if name == "pred_changed":
                return int(pred != "B")
            if name == "pred_left":
                return int(pred.startswith("L"))
            if name == "pred_right":
                return int(pred.startswith("R"))
            if name == "pred_deep":
                return int(pred in {"L2", "R2", "L3", "R3"})
            if name == "succ_changed":
                return int(succ != "B")
            if name == "succ_left":
                return int(succ.startswith("L"))
            if name == "succ_right":
                return int(succ.startswith("R"))
            if name == "succ_deep":
                return int(succ in {"L2", "R2", "L3", "R3"})
            if name == "self_deep":
                return int(current in {"L2", "R2", "L3", "R3"})
            if name == "self_stage3":
                return int(current in {"L3", "R3"})
            raise ValueError(name)

        for target, sources in enumerate(incoming):
            if indegree[target] <= 1:
                continue
            overfull_target_count += 1
            excess_incoming_total += indegree[target] - 1
            label_bit_pairs = {name: set() for name in bit_names}
            pred_cur_pairs = set()
            cur_succ_pairs = set()
            source_rows = []
            for idx in sources:
                label = labels[idx]
                pred_label = labels[prev_row[idx]]
                succ_label = labels[succ_row[idx]]
                if label != "B":
                    changed_label_counts[label] = changed_label_counts.get(label, 0) + 1
                pred_cur_key = f"{pred_label}->{label}"
                cur_succ_key = f"{label}->{succ_label}"
                pred_cur_signature_counts[pred_cur_key] = pred_cur_signature_counts.get(pred_cur_key, 0) + 1
                cur_succ_signature_counts[cur_succ_key] = cur_succ_signature_counts.get(cur_succ_key, 0) + 1
                pred_cur_pairs.add((pred_label, label))
                cur_succ_pairs.add((label, succ_label))
                for name in bit_names:
                    label_bit_pairs[name].add((label, bit_value(name, idx)))
                if len(overfull_examples) < 25:
                    source_rows.append(
                        {
                            "source_index": int(idx),
                            "source_label": label,
                            "pred_label": pred_label,
                            "succ_label": succ_label,
                            "source_coords": _coords_payload(prepared, idx),
                        }
                    )
            if len(pred_cur_pairs) == len(sources):
                separated_targets_pred_cur += 1
            if len(cur_succ_pairs) == len(sources):
                separated_targets_cur_succ += 1
            for name in bit_names:
                if len(label_bit_pairs[name]) == len(sources):
                    separated_targets_by_bit[name] += 1
            if len(overfull_examples) < 25:
                overfull_examples.append(
                    {
                        "color": color,
                        "target_index": int(target),
                        "target_coords": _coords_payload(prepared, target),
                        "indegree": int(indegree[target]),
                        "sources": source_rows,
                    }
                )

    colliding_changed_labels = sorted(label for label in changed_label_counts if label != "B")
    return {
        "m": prepared.m,
        "layer2_conflict": False,
        "layer3_conflict": False,
        "layer2_overlap_sizes": list(meta["layer2_overlap_sizes"]),
        "layer3_overlap_sizes": list(meta["layer3_overlap_sizes"]),
        "overfull_target_count": int(overfull_target_count),
        "hole_target_count": int(hole_target_count),
        "excess_incoming_total": int(excess_incoming_total),
        "colliding_changed_labels": colliding_changed_labels,
        "changed_label_counts": changed_label_counts,
        "pred_cur_signature_counts": pred_cur_signature_counts,
        "cur_succ_signature_counts": cur_succ_signature_counts,
        "separated_targets_pred_cur": int(separated_targets_pred_cur),
        "separated_targets_cur_succ": int(separated_targets_cur_succ),
        "separated_targets_by_bit": separated_targets_by_bit,
        "overfull_examples": overfull_examples,
    }


def _seed_profiles(prepared_by_m: Mapping[int, PreparedSearch], seeds: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    rows = []
    for seed in seeds:
        left_word = tuple(int(value) for value in seed["left_word"])
        right_word = tuple(int(value) for value in seed["right_word"])
        per_m = {str(m): _collision_profile_for_m(prepared_by_m[m], left_word=left_word, right_word=right_word) for m in PRIMARY_M_VALUES}
        total_excess = sum(int(per_m[str(m)].get("excess_incoming_total", 10**9)) for m in PRIMARY_M_VALUES)
        total_overfull = sum(int(per_m[str(m)].get("overfull_target_count", 10**9)) for m in PRIMARY_M_VALUES)
        changed_label_union = sorted({label for m in PRIMARY_M_VALUES for label in per_m[str(m)].get("colliding_changed_labels", [])})
        bit_scores = {}
        for name in (
            "pred_changed",
            "pred_left",
            "pred_right",
            "pred_deep",
            "succ_changed",
            "succ_left",
            "succ_right",
            "succ_deep",
            "self_deep",
            "self_stage3",
        ):
            bit_scores[name] = sum(int(per_m[str(m)].get("separated_targets_by_bit", {}).get(name, 0)) for m in PRIMARY_M_VALUES)
        pred_cur_score = sum(int(per_m[str(m)].get("separated_targets_pred_cur", 0)) for m in PRIMARY_M_VALUES)
        cur_succ_score = sum(int(per_m[str(m)].get("separated_targets_cur_succ", 0)) for m in PRIMARY_M_VALUES)
        best_bit_name = max(bit_scores, key=bit_scores.get)
        rows.append(
            {
                "seed_id": int(seed["seed_id"]),
                "left_word": list(left_word),
                "right_word": list(right_word),
                "orientation": str(seed["orientation"]),
                "per_m": per_m,
                "total_excess_incoming": int(total_excess),
                "total_overfull_targets": int(total_overfull),
                "colliding_changed_label_count": len(changed_label_union),
                "colliding_changed_labels": changed_label_union,
                "best_bit_name": best_bit_name,
                "best_bit_score": int(bit_scores[best_bit_name]),
                "pred_cur_score": int(pred_cur_score),
                "cur_succ_score": int(cur_succ_score),
            }
        )
    rows.sort(
        key=lambda row: (
            row["total_excess_incoming"],
            row["total_overfull_targets"],
            row["colliding_changed_label_count"],
            -row["best_bit_score"],
            -row["pred_cur_score"],
            -row["cur_succ_score"],
            row["seed_id"],
        )
    )
    return rows


def _evaluate_candidate_across_m(
    prepared_by_m: Mapping[int, PreparedSearch],
    *,
    left_word: Tuple[int, int, int],
    right_word: Tuple[int, int, int],
    cocycle_defect: str,
    repair: Mapping[str, object] | None,
    m_values: Sequence[int],
) -> Dict[str, object]:
    per_m = {}
    latin_all = True
    clean_all = True
    strict_all = True
    full_single_all = True
    total_cycle_count = 0
    total_nonzero_monodromy = 0
    for m in m_values:
        prepared = prepared_by_m[m]
        nexts_all, meta = _build_candidate(
            prepared,
            w0=REPRESENTATIVE_W0,
            s0=REPRESENTATIVE_S0,
            left_word=left_word,
            right_word=right_word,
            cocycle_defect=cocycle_defect,
            repair=repair,
        )
        if nexts_all is None:
            per_m[str(m)] = {
                "latin_all_colors": False,
                "clean_frame": False,
                "strict_clock": False,
                "layer2_conflict": bool(meta["layer2_conflict"]),
                "layer3_conflict": bool(meta["layer3_conflict"]),
            }
            latin_all = False
            clean_all = False
            strict_all = False
            full_single_all = False
            break
        latin = incoming_latin_all(nexts_all)
        if not latin:
            per_m[str(m)] = {
                "latin_all_colors": False,
                "clean_frame": False,
                "strict_clock": False,
                "layer2_conflict": False,
                "layer3_conflict": False,
            }
            latin_all = False
            clean_all = False
            strict_all = False
            full_single_all = False
            break
        ret = first_return(prepared.pre, nexts_all[0])
        monodromies = [int(value) for value in ret["monodromies"]]
        full_single = (
            ret["clean_frame"]
            and ret["strict_clock"]
            and ret["U_cycle_count"] == 1
            and ret["U_cycle_lengths"] == [m * m]
            and len(monodromies) == 1
            and gcd(monodromies[0], m) == 1
        )
        per_m[str(m)] = {
            "latin_all_colors": True,
            "clean_frame": bool(ret["clean_frame"]),
            "strict_clock": bool(ret["strict_clock"]),
            "u_cycle_count": int(ret["U_cycle_count"]),
            "u_cycle_lengths": list(ret["U_cycle_lengths"]),
            "monodromies": monodromies,
            "full_single_grouped_orbit": full_single,
        }
        clean_all &= bool(ret["clean_frame"])
        strict_all &= bool(ret["strict_clock"])
        full_single_all &= bool(full_single)
        total_cycle_count += int(ret["U_cycle_count"])
        total_nonzero_monodromy += sum(1 for value in monodromies if value != 0)

    return {
        "left_word": list(left_word),
        "right_word": list(right_word),
        "cocycle_defect": cocycle_defect,
        "repair": dict(repair) if repair is not None else None,
        "per_m": per_m,
        "latin_all": latin_all,
        "clean_all": clean_all,
        "strict_all": strict_all,
        "full_single_all": full_single_all,
        "total_cycle_count": total_cycle_count,
        "total_nonzero_monodromy": total_nonzero_monodromy,
    }


def _repair_rank(row: Mapping[str, object]) -> Tuple[object, ...]:
    return (
        not row["latin_all"],
        not row["clean_all"],
        not row["strict_all"],
        not row["full_single_all"],
        row["total_cycle_count"] if row["latin_all"] else 10**9,
        -row["total_nonzero_monodromy"],
        row["cocycle_defect"],
        json.dumps(row["repair"], sort_keys=True),
    )


def _search_repairs(
    prepared_by_m: Mapping[int, PreparedSearch],
    ranked_seeds: Sequence[Mapping[str, object]],
) -> Dict[str, object]:
    bit_names = (
        "pred_changed",
        "pred_left",
        "pred_right",
        "pred_deep",
        "succ_changed",
        "succ_left",
        "succ_right",
        "succ_deep",
        "self_deep",
        "self_stage3",
    )
    selected = list(ranked_seeds[:TOP_SEEDS_FOR_REPAIR])
    one_gate_rows = []
    one_bit_rows = []
    for seed in selected:
        left_word = tuple(int(value) for value in seed["left_word"])
        right_word = tuple(int(value) for value in seed["right_word"])
        labels = list(seed["colliding_changed_labels"]) or list(CLASS_LABELS)

        for label in labels:
            base_dir = (left_word if label.startswith("L") else right_word)[int(label[1]) - 1]
            for alt_dir in range(DIM):
                if alt_dir == base_dir:
                    continue
                repair = {"label": label, "alt_dir": alt_dir}
                for cocycle_defect in ("none", "left", "right", "both"):
                    row = _evaluate_candidate_across_m(
                        prepared_by_m,
                        left_word=left_word,
                        right_word=right_word,
                        cocycle_defect=cocycle_defect,
                        repair=repair,
                        m_values=PRIMARY_M_VALUES,
                    )
                    row["seed_id"] = int(seed["seed_id"])
                    one_gate_rows.append(row)

        for label in labels:
            base_dir = (left_word if label.startswith("L") else right_word)[int(label[1]) - 1]
            for bit_name in bit_names:
                for bit_value in (0, 1):
                    for alt_dir in range(DIM):
                        if alt_dir == base_dir:
                            continue
                        repair = {
                            "label": label,
                            "bit_name": bit_name,
                            "bit_value": bit_value,
                            "alt_dir": alt_dir,
                        }
                        for cocycle_defect in ("none", "left", "right", "both"):
                            row = _evaluate_candidate_across_m(
                                prepared_by_m,
                                left_word=left_word,
                                right_word=right_word,
                                cocycle_defect=cocycle_defect,
                                repair=repair,
                                m_values=PRIMARY_M_VALUES,
                            )
                            row["seed_id"] = int(seed["seed_id"])
                            one_bit_rows.append(row)

    one_gate_rows.sort(key=_repair_rank)
    one_bit_rows.sort(key=_repair_rank)

    def summarize(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
        latin_rows = [row for row in rows if row["latin_all"]]
        clean_rows = [row for row in latin_rows if row["clean_all"]]
        strict_rows = [row for row in clean_rows if row["strict_all"]]
        target_rows = [row for row in strict_rows if row["full_single_all"]]
        return {
            "candidate_count": len(rows),
            "latin_count": len(latin_rows),
            "clean_count": len(clean_rows),
            "strict_count": len(strict_rows),
            "target_count": len(target_rows),
            "best_rows": list(rows[:20]),
            "target_rows": list(target_rows[:20]),
        }

    summary = {
        "selected_seed_ids": [int(seed["seed_id"]) for seed in selected],
        "one_gate": summarize(one_gate_rows),
        "one_bit": summarize(one_bit_rows),
    }

    control_rows = []
    for family_name, family in (("one_gate", one_gate_rows), ("one_bit", one_bit_rows)):
        candidate = next((row for row in family if row["strict_all"]), None)
        if candidate is None:
            continue
        control = _evaluate_candidate_across_m(
            {CONTROL_M: prepared_by_m[CONTROL_M]},
            left_word=tuple(int(value) for value in candidate["left_word"]),
            right_word=tuple(int(value) for value in candidate["right_word"]),
            cocycle_defect=str(candidate["cocycle_defect"]),
            repair=candidate["repair"],
            m_values=(CONTROL_M,),
        )
        control["family"] = family_name
        control["seed_id"] = int(candidate["seed_id"])
        control_rows.append(control)

    return {
        "summary": summary,
        "one_gate_rows": one_gate_rows,
        "one_bit_rows": one_bit_rows,
        "control_rows": control_rows,
    }


def _probe_two_gate_best_seed(
    prepared_by_m: Mapping[int, PreparedSearch],
    best_seed: Mapping[str, object],
) -> Dict[str, object]:
    left_word = tuple(int(value) for value in best_seed["left_word"])
    right_word = tuple(int(value) for value in best_seed["right_word"])
    labels = list(best_seed["colliding_changed_labels"])
    rows = []
    for idx1 in range(len(labels)):
        for idx2 in range(idx1 + 1, len(labels)):
            label1 = labels[idx1]
            label2 = labels[idx2]
            base1 = (left_word if label1.startswith("L") else right_word)[int(label1[1]) - 1]
            base2 = (left_word if label2.startswith("L") else right_word)[int(label2[1]) - 1]
            for alt1 in range(DIM):
                if alt1 == base1:
                    continue
                for alt2 in range(DIM):
                    if alt2 == base2:
                        continue
                    for cocycle_defect in ("none", "left", "right", "both"):
                        repair1 = {"label": label1, "alt_dir": alt1}
                        repair2 = {"label": label2, "alt_dir": alt2}
                        per_m = {}
                        latin_all = True
                        clean_all = True
                        strict_all = True
                        target_all = True
                        total_cycle_count = 0
                        for m in PRIMARY_M_VALUES:
                            prepared = prepared_by_m[m]
                            nexts_all, meta = _build_candidate(
                                prepared,
                                w0=REPRESENTATIVE_W0,
                                s0=REPRESENTATIVE_S0,
                                left_word=left_word,
                                right_word=right_word,
                                cocycle_defect=cocycle_defect,
                                repair=None,
                            )
                            if nexts_all is None:
                                latin_all = False
                                clean_all = False
                                strict_all = False
                                target_all = False
                                per_m[str(m)] = {"latin_all_colors": False}
                                break
                            step_by_dir = prepared.pre["step_by_dir"]
                            labels_by_color = meta["labels_by_color"]
                            for color in range(DIM):
                                for repair in (repair1, repair2):
                                    abs_dir = (int(repair["alt_dir"]) + color) % DIM
                                    for source_idx, current in enumerate(labels_by_color[color]):
                                        if current == repair["label"]:
                                            nexts_all[color][source_idx] = step_by_dir[abs_dir][source_idx]
                            latin = incoming_latin_all(nexts_all)
                            if not latin:
                                latin_all = False
                                clean_all = False
                                strict_all = False
                                target_all = False
                                per_m[str(m)] = {"latin_all_colors": False}
                                break
                            ret = first_return(prepared.pre, nexts_all[0])
                            monodromies = [int(value) for value in ret["monodromies"]]
                            full_single = (
                                ret["clean_frame"]
                                and ret["strict_clock"]
                                and ret["U_cycle_count"] == 1
                                and ret["U_cycle_lengths"] == [m * m]
                                and len(monodromies) == 1
                                and gcd(monodromies[0], m) == 1
                            )
                            per_m[str(m)] = {
                                "latin_all_colors": True,
                                "clean_frame": bool(ret["clean_frame"]),
                                "strict_clock": bool(ret["strict_clock"]),
                                "u_cycle_count": int(ret["U_cycle_count"]),
                                "u_cycle_lengths": list(ret["U_cycle_lengths"]),
                                "monodromies": monodromies,
                                "full_single_grouped_orbit": full_single,
                            }
                            clean_all &= bool(ret["clean_frame"])
                            strict_all &= bool(ret["strict_clock"])
                            target_all &= bool(full_single)
                            total_cycle_count += int(ret["U_cycle_count"])
                        rows.append(
                            {
                                "seed_id": int(best_seed["seed_id"]),
                                "left_word": list(left_word),
                                "right_word": list(right_word),
                                "cocycle_defect": cocycle_defect,
                                "repair_pair": [repair1, repair2],
                                "per_m": per_m,
                                "latin_all": latin_all,
                                "clean_all": clean_all,
                                "strict_all": strict_all,
                                "target_all": target_all,
                                "total_cycle_count": total_cycle_count,
                            }
                        )
    rows.sort(
        key=lambda row: (
            not row["latin_all"],
            not row["clean_all"],
            not row["strict_all"],
            not row["target_all"],
            row["total_cycle_count"] if row["latin_all"] else 10**9,
            row["cocycle_defect"],
        )
    )
    latin_rows = [row for row in rows if row["latin_all"]]
    strict_rows = [row for row in latin_rows if row["strict_all"]]
    target_rows = [row for row in strict_rows if row["target_all"]]
    return {
        "seed_id": int(best_seed["seed_id"]),
        "candidate_count": len(rows),
        "latin_count": len(latin_rows),
        "strict_count": len(strict_rows),
        "target_count": len(target_rows),
        "best_rows": rows[:20],
        "target_rows": target_rows[:20],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract Latin collision profiles and search micro-repair families for D5 endpoint seeds.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    start = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    mixed_rule = _mixed_rule()
    prepared_by_m = {m: _prepare_m(m, mixed_rule) for m in PRIMARY_M_VALUES + (CONTROL_M,)}
    seeds = _load_seed_pairs()
    seed_profiles = _seed_profiles(prepared_by_m, seeds)
    repair_results = _search_repairs(prepared_by_m, seed_profiles)
    two_gate_probe = _probe_two_gate_best_seed(prepared_by_m, seed_profiles[0])

    _write_json(out_dir / "seed_pair_collision_profiles.json", {"rows": seed_profiles})
    _write_json(out_dir / "seed_pair_rankings.json", {"rows": seed_profiles})
    _write_json(out_dir / "repair_microfamily_summary.json", repair_results["summary"])
    _write_json(out_dir / "repair_one_gate_rows.json", {"rows": repair_results["one_gate_rows"][:200]})
    _write_json(out_dir / "repair_one_bit_rows.json", {"rows": repair_results["one_bit_rows"][:200]})
    _write_json(out_dir / "control_m11_check.json", {"rows": repair_results["control_rows"]})
    _write_json(out_dir / "two_gate_best_seed_probe.json", two_gate_probe)

    best_seed = seed_profiles[0]
    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "primary_m_values": list(PRIMARY_M_VALUES),
        "control_m": CONTROL_M,
        "seed_count": len(seed_profiles),
        "selected_seed_ids_for_repair": repair_results["summary"]["selected_seed_ids"],
        "best_ranked_seed": {
            "seed_id": int(best_seed["seed_id"]),
            "left_word": list(best_seed["left_word"]),
            "right_word": list(best_seed["right_word"]),
            "total_excess_incoming": int(best_seed["total_excess_incoming"]),
            "total_overfull_targets": int(best_seed["total_overfull_targets"]),
            "best_bit_name": str(best_seed["best_bit_name"]),
            "best_bit_score": int(best_seed["best_bit_score"]),
            "pred_cur_score": int(best_seed["pred_cur_score"]),
            "cur_succ_score": int(best_seed["cur_succ_score"]),
        },
        "two_gate_best_seed_probe": {
            "candidate_count": int(two_gate_probe["candidate_count"]),
            "latin_count": int(two_gate_probe["latin_count"]),
            "strict_count": int(two_gate_probe["strict_count"]),
            "target_count": int(two_gate_probe["target_count"]),
        },
        "repair_summary_file": str(out_dir / "repair_microfamily_summary.json"),
        "collision_profiles_file": str(out_dir / "seed_pair_collision_profiles.json"),
        "strongest_supported_conclusion": (
            "This artifact implements the s45 branch exactly: collision certificates for the 030 seed pairs, ranking by "
            "collision support and separability, and one-gate / one-bit repair searches on the best seeds only. The "
            "goal is to decide whether one extra bit or one localized repair class is enough before widening again."
        ),
    }
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    print(
        f"seed_count={len(seed_profiles)} best_seed={best_seed['seed_id']} "
        f"one_gate_latin={repair_results['summary']['one_gate']['latin_count']} "
        f"one_gate_target={repair_results['summary']['one_gate']['target_count']} "
        f"one_bit_latin={repair_results['summary']['one_bit']['latin_count']} "
        f"one_bit_target={repair_results['summary']['one_bit']['target_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
