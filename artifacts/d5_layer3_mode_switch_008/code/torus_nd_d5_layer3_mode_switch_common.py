#!/usr/bin/env python3
"""Common evaluator for the d=5 layer-3 one-flag mode-switch search."""

from __future__ import annotations

import platform
import time
from collections import OrderedDict
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from typing import Dict, List, Mapping, Sequence, Tuple

from torus_nd_d5_strict_palette_context_common import (
    DIM,
    decode,
    encode,
    first_return,
    incoming_latin_all,
    layer_bucket,
    parse_m_list,
)

TASK_ID = "D5-LAYER3-MODE-SWITCH-008"
PILOT_M_VALUES = (5, 7, 9)
REPRESENTATIVE_OLD_BIT = "q=-1"
LAYER2_ORIENTATIONS = OrderedDict(
    [
        ("0/2", (0, 2)),
        ("2/0", (2, 0)),
    ]
)
LAYER3_MODES = OrderedDict(
    [
        ("0/3", (0, 3)),
        ("3/0", (3, 0)),
        ("2/3", (2, 3)),
        ("3/2", (3, 2)),
        ("3/3", (3, 3)),
    ]
)
SIMPLE_FLAG_NAMES = (
    "pred_any_phase_align",
    "pred_sig0_phase_align",
    "pred_sig1_wu2",
    "pred_sig4_wu2",
)
SIMPLE_FLAG_DESCRIPTIONS = {
    "pred_any_phase_align": "1 iff at least one of the five color-relative predecessors has phase_align=1.",
    "pred_sig0_phase_align": "1 iff the color-relative predecessor in direction 0 has phase_align=1.",
    "pred_sig1_wu2": "1 iff the color-relative predecessor in direction 1 satisfies w+u=2.",
    "pred_sig4_wu2": "1 iff the color-relative predecessor in direction 4 satisfies w+u=2.",
}
EXACT_SIGNATURE_DESCRIPTION = (
    "One-bit partition on the exact 10-bit predecessor-local signature "
    "((phase_align, wu2) on each color-relative predecessor direction 0..4)."
)


@dataclass(frozen=True)
class Rule:
    family: str
    layer2_orientation_name: str
    mode_p0_name: str
    mode_p1_name: str
    predecessor_flag_name: str | None = None
    exact_signature_mask: int | None = None
    exact_signature_subset: Tuple[int, ...] = ()

    def layer2_table(self) -> Tuple[int, int]:
        return LAYER2_ORIENTATIONS[self.layer2_orientation_name]

    def mode_p0_table(self) -> Tuple[int, int]:
        return LAYER3_MODES[self.mode_p0_name]

    def mode_p1_table(self) -> Tuple[int, int]:
        return LAYER3_MODES[self.mode_p1_name]

    def effective_key(self) -> Tuple[object, ...]:
        if self.mode_p0_name == self.mode_p1_name:
            return ("constant", self.layer2_orientation_name, self.mode_p0_name)
        if self.family == "simple":
            return ("simple", self.layer2_orientation_name, self.predecessor_flag_name, self.mode_p0_name, self.mode_p1_name)
        return (
            "exact_signature",
            self.layer2_orientation_name,
            int(self.exact_signature_mask or 0),
            self.mode_p0_name,
            self.mode_p1_name,
        )

    def payload(self) -> Dict[str, object]:
        layer2_s0, layer2_s1 = self.layer2_table()
        mode_p0 = self.mode_p0_table()
        mode_p1 = self.mode_p1_table()
        payload: Dict[str, object] = {
            "family": self.family,
            "representative_old_bit_name": REPRESENTATIVE_OLD_BIT,
            "layer2_orientation": self.layer2_orientation_name,
            "layer2_table": {"s0": layer2_s0, "s1": layer2_s1},
            "layer3_mode_p0": {
                "name": self.mode_p0_name,
                "table": {"s0": mode_p0[0], "s1": mode_p0[1]},
            },
            "layer3_mode_p1": {
                "name": self.mode_p1_name,
                "table": {"s0": mode_p1[0], "s1": mode_p1[1]},
            },
            "effective_key": list(self.effective_key()),
        }
        if self.family == "simple":
            payload["predecessor_flag_name"] = self.predecessor_flag_name
            payload["predecessor_flag_description"] = SIMPLE_FLAG_DESCRIPTIONS[str(self.predecessor_flag_name)]
        else:
            payload["exact_signature_mask"] = int(self.exact_signature_mask or 0)
            payload["exact_signature_subset"] = list(self.exact_signature_subset)
            payload["exact_signature_description"] = EXACT_SIGNATURE_DESCRIPTION
        return payload

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> "Rule":
        family = str(payload["family"])
        if family == "simple":
            return cls(
                family=family,
                layer2_orientation_name=str(payload["layer2_orientation"]),
                predecessor_flag_name=str(payload["predecessor_flag_name"]),
                mode_p0_name=str(payload["layer3_mode_p0"]["name"]),
                mode_p1_name=str(payload["layer3_mode_p1"]["name"]),
            )
        return cls(
            family=family,
            layer2_orientation_name=str(payload["layer2_orientation"]),
            mode_p0_name=str(payload["layer3_mode_p0"]["name"]),
            mode_p1_name=str(payload["layer3_mode_p1"]["name"]),
            exact_signature_mask=int(payload["exact_signature_mask"]),
            exact_signature_subset=tuple(int(value) for value in payload.get("exact_signature_subset", [])),
        )


def rich_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def environment_block() -> Dict[str, object]:
    return {"python_version": platform.python_version(), "rich_version": rich_version()}


def runtime_since(start: float) -> float:
    return time.perf_counter() - start


def parse_args_m_list(raw: str) -> List[int]:
    return parse_m_list(raw)


def old_bit_q_eq_neg1(coords: Sequence[int], color: int, m: int) -> int:
    return int(coords[(color + 1) % DIM] == (m - 1))


def phase_align_value(coords: Sequence[int], color: int, m: int) -> int:
    q = coords[(color + 1) % DIM]
    v = coords[(color + 3) % DIM]
    return int((v - q) % m == 0)


def wu2_value(coords: Sequence[int], color: int, m: int) -> int:
    w = coords[(color + 2) % DIM]
    u = coords[(color + 4) % DIM]
    return int((w + u) % m == 2)


def predecessor_coords(coords: Sequence[int], color: int, rel_direction: int, m: int) -> Tuple[int, ...]:
    out = list(coords)
    out[(color + rel_direction) % DIM] = (out[(color + rel_direction) % DIM] - 1) % m
    return tuple(out)


def exact_predecessor_signature(coords: Sequence[int], color: int, m: int) -> Tuple[int, ...]:
    rows: List[int] = []
    for rel_direction in range(DIM):
        pred = predecessor_coords(coords, color, rel_direction, m)
        rows.append(phase_align_value(pred, color, m))
        rows.append(wu2_value(pred, color, m))
    return tuple(rows)


def simple_flag_mask(coords: Sequence[int], color: int, m: int) -> int:
    preds = [predecessor_coords(coords, color, rel_direction, m) for rel_direction in range(DIM)]
    phase_bits = [phase_align_value(pred, color, m) for pred in preds]
    wu2_bits = [wu2_value(pred, color, m) for pred in preds]
    flags = (
        int(any(phase_bits)),
        int(phase_bits[0]),
        int(wu2_bits[1]),
        int(wu2_bits[4]),
    )
    mask = 0
    for index, value in enumerate(flags):
        if value:
            mask |= 1 << index
    return mask


def exact_signature_catalog(m_values: Sequence[int]) -> Dict[str, object]:
    classes: Dict[Tuple[int, ...], List[object]] = {}
    for m in m_values:
        for idx in range(m**DIM):
            coords = decode(idx, m)
            if sum(coords) % m != 3:
                continue
            raw = exact_predecessor_signature(coords, 0, m)
            if raw not in classes:
                classes[raw] = [m, coords]
    rows = []
    signature_to_id: Dict[Tuple[int, ...], int] = {}
    for class_id, raw in enumerate(sorted(classes)):
        signature_to_id[raw] = class_id
        sample_m, sample_coords = classes[raw]
        rows.append(
            {
                "class_id": class_id,
                "signature_bits": list(raw),
                "sample_m": int(sample_m),
                "sample_coords": list(sample_coords),
            }
        )
    return {"signature_to_id": signature_to_id, "rows": rows}


def _feature_tuple(coords: Sequence[int], color: int, m: int, signature_to_id: Mapping[Tuple[int, ...], int]) -> Tuple[int, int, int, int, int]:
    layer = layer_bucket(sum(coords) % m)
    layer_code = 4 if layer == "4+" else int(layer)
    if layer_code == 2:
        return (layer_code, old_bit_q_eq_neg1(coords, color, m), 0, 0, -1)
    if layer_code == 3:
        raw_signature = exact_predecessor_signature(coords, color, m)
        return (
            layer_code,
            0,
            old_bit_q_eq_neg1(coords, color, m),
            simple_flag_mask(coords, color, m),
            int(signature_to_id[raw_signature]),
        )
    return (layer_code, 0, 0, 0, -1)


def precompute_m(m: int, signature_to_id: Mapping[Tuple[int, ...], int]) -> Dict[str, object]:
    n = m**DIM
    coords = [decode(idx, m) for idx in range(n)]
    step_by_dir = [[0] * n for _ in range(DIM)]
    feature_ids_by_color = [[0] * n for _ in range(DIM)]
    feature_rows: List[Tuple[int, int, int, int, int]] = []
    feature_to_id: Dict[Tuple[int, int, int, int, int], int] = {}

    for idx, vertex in enumerate(coords):
        for direction in range(DIM):
            nxt = list(vertex)
            nxt[direction] = (nxt[direction] + 1) % m
            step_by_dir[direction][idx] = encode(nxt, m)
        for color in range(DIM):
            feature = _feature_tuple(vertex, color, m, signature_to_id)
            feature_id = feature_to_id.get(feature)
            if feature_id is None:
                feature_id = len(feature_rows)
                feature_to_id[feature] = feature_id
                feature_rows.append(feature)
            feature_ids_by_color[color][idx] = feature_id

    color0_patterns = set()
    for idx, vertex in enumerate(coords):
        pattern = []
        for direction in range(DIM):
            pred = list(vertex)
            pred[direction] = (pred[direction] - 1) % m
            pattern.append(feature_ids_by_color[0][encode(pred, m)])
        color0_patterns.add(tuple(pattern))

    return {
        "m": m,
        "n": n,
        "coords": coords,
        "step_by_dir": step_by_dir,
        "feature_rows": feature_rows,
        "feature_ids_by_color": feature_ids_by_color,
        "color0_patterns": tuple(sorted(color0_patterns)),
    }


def anchor_by_feature(pre: Dict[str, object], rule: Rule) -> List[int]:
    layer2_s0, layer2_s1 = rule.layer2_table()
    mode_p0 = rule.mode_p0_table()
    mode_p1 = rule.mode_p1_table()
    simple_flag_index = SIMPLE_FLAG_NAMES.index(rule.predecessor_flag_name) if rule.family == "simple" else None
    exact_mask = int(rule.exact_signature_mask or 0)

    anchors = [0] * len(pre["feature_rows"])
    for feature_id, (layer_code, s2, s3, flag_mask, signature_id) in enumerate(pre["feature_rows"]):
        if layer_code == 0:
            anchors[feature_id] = 1
        elif layer_code == 1:
            anchors[feature_id] = 4
        elif layer_code == 2:
            anchors[feature_id] = layer2_s0 if s2 == 0 else layer2_s1
        elif layer_code == 3:
            if rule.family == "simple":
                p_bit = (flag_mask >> int(simple_flag_index)) & 1
            else:
                p_bit = 0 if signature_id < 0 else ((exact_mask >> int(signature_id)) & 1)
            anchors[feature_id] = (mode_p1 if p_bit else mode_p0)[s3]
        else:
            anchors[feature_id] = 0
    return anchors


def color0_is_latin(pre: Dict[str, object], anchors: Sequence[int]) -> bool:
    for token0, token1, token2, token3, token4 in pre["color0_patterns"]:
        indegree = int(anchors[token0] == 0)
        indegree += int(anchors[token1] == 1)
        indegree += int(anchors[token2] == 2)
        indegree += int(anchors[token3] == 3)
        indegree += int(anchors[token4] == 4)
        if indegree != 1:
            return False
    return True


def nexts_all_for_rule(pre: Dict[str, object], anchors: Sequence[int]) -> List[List[int]]:
    step_by_dir = pre["step_by_dir"]
    nexts = [[0] * pre["n"] for _ in range(DIM)]
    for color in range(DIM):
        color_dirs = tuple((anchor + color) % DIM for anchor in anchors)
        row = nexts[color]
        feature_ids = pre["feature_ids_by_color"][color]
        for idx, feature_id in enumerate(feature_ids):
            row[idx] = step_by_dir[color_dirs[feature_id]][idx]
    return nexts


def classify_return(ret: Dict[str, object]) -> Dict[str, object]:
    has_cycle = any(length > 1 for length in ret["U_cycle_lengths"])
    has_monodromy = any(value != 0 for value in ret["monodromies"])
    if has_cycle and has_monodromy:
        kind = "both"
    elif has_cycle:
        kind = "cycle_only"
    elif has_monodromy:
        kind = "monodromy_only"
    else:
        kind = "trivial"
    return {"kind": kind, "has_cycle": has_cycle, "has_monodromy": has_monodromy}


def evaluate_rule(pre_by_m: Dict[int, Dict[str, object]], rule: Rule, *, m_values: Sequence[int]) -> Dict[str, object]:
    per_m: Dict[str, object] = {}
    latin0_all = True
    latin_all = True
    clean_all = True
    strict_all = True
    total_u_cycle_count = 0
    total_nonzero_monodromies = 0
    max_cycle_length = 0
    has_cycle = False
    has_monodromy = False

    for m in m_values:
        pre = pre_by_m[m]
        anchors = anchor_by_feature(pre, rule)
        latin0 = color0_is_latin(pre, anchors)
        if not latin0:
            per_m[str(m)] = {
                "latin_color0": False,
                "latin_all_colors": False,
                "color0_return": {
                    "clean_frame": False,
                    "strict_clock": False,
                    "U_cycle_count": 0,
                    "U_cycle_lengths": [],
                    "monodromies": [],
                    "nontrivial_u": False,
                },
                "classification": {"kind": "invalid", "has_cycle": False, "has_monodromy": False},
            }
            latin0_all = False
            latin_all = False
            clean_all = False
            strict_all = False
            continue

        nexts_all = nexts_all_for_rule(pre, anchors)
        latin = incoming_latin_all(nexts_all)
        ret = first_return(pre, nexts_all[0]) if latin else {
            "clean_frame": False,
            "strict_clock": False,
            "U_cycle_count": 0,
            "U_cycle_lengths": [],
            "monodromies": [],
            "nontrivial_u": False,
        }
        classification = classify_return(ret) if latin else {"kind": "invalid", "has_cycle": False, "has_monodromy": False}
        per_m[str(m)] = {
            "latin_color0": True,
            "latin_all_colors": latin,
            "color0_return": ret,
            "classification": classification,
        }
        latin0_all &= latin0
        latin_all &= latin
        clean_all &= ret["clean_frame"]
        strict_all &= ret["strict_clock"]
        total_u_cycle_count += ret["U_cycle_count"]
        total_nonzero_monodromies += sum(1 for value in ret["monodromies"] if value != 0)
        if ret["U_cycle_lengths"]:
            max_cycle_length = max(max_cycle_length, max(ret["U_cycle_lengths"]))
        has_cycle |= classification["has_cycle"]
        has_monodromy |= classification["has_monodromy"]

    if has_cycle and has_monodromy:
        overall_kind = "both"
    elif has_cycle:
        overall_kind = "cycle_only"
    elif has_monodromy:
        overall_kind = "monodromy_only"
    else:
        overall_kind = "trivial"

    return {
        "rule": rule.payload(),
        "per_m": per_m,
        "latin_color0_all": latin0_all,
        "latin_all": latin_all,
        "clean_all": clean_all,
        "strict_all": strict_all,
        "total_u_cycle_count": total_u_cycle_count,
        "total_nonzero_monodromies": total_nonzero_monodromies,
        "max_cycle_length": max_cycle_length,
        "has_cycle": has_cycle,
        "has_monodromy": has_monodromy,
        "overall_kind": overall_kind,
    }


def overall_rank_key(result: Dict[str, object]) -> Tuple[object, ...]:
    kind_order = {"both": 0, "cycle_only": 1, "monodromy_only": 2, "trivial": 3}
    rule = result["rule"]
    return (
        not result["clean_all"],
        not result["strict_all"],
        kind_order[result["overall_kind"]],
        result["total_u_cycle_count"],
        -result["max_cycle_length"],
        -result["total_nonzero_monodromies"],
        rule["family"],
        rule["layer2_orientation"],
        rule["layer3_mode_p0"]["name"],
        rule["layer3_mode_p1"]["name"],
        str(rule.get("predecessor_flag_name", "")),
        int(rule.get("exact_signature_mask", 0)),
    )


def simple_flag_rows() -> List[Rule]:
    rows = []
    for orientation_name in LAYER2_ORIENTATIONS:
        for flag_name in SIMPLE_FLAG_NAMES:
            for mode_p0_name in LAYER3_MODES:
                for mode_p1_name in LAYER3_MODES:
                    rows.append(
                        Rule(
                            family="simple",
                            layer2_orientation_name=orientation_name,
                            predecessor_flag_name=flag_name,
                            mode_p0_name=mode_p0_name,
                            mode_p1_name=mode_p1_name,
                        )
                    )
    return rows


def exact_signature_masks(class_count: int) -> List[int]:
    if class_count <= 0:
        return [0]
    return [mask for mask in range(1 << class_count) if (mask & 1) == 0]


def exact_signature_rows(class_count: int) -> List[Rule]:
    rows = []
    masks = exact_signature_masks(class_count)
    for orientation_name in LAYER2_ORIENTATIONS:
        for mode_p0_name in LAYER3_MODES:
            for mode_p1_name in LAYER3_MODES:
                if mode_p0_name == mode_p1_name:
                    mask_iter = (0,)
                else:
                    mask_iter = masks
                for mask in mask_iter:
                    subset = tuple(class_id for class_id in range(class_count) if mask & (1 << class_id))
                    rows.append(
                        Rule(
                            family="exact_signature",
                            layer2_orientation_name=orientation_name,
                            mode_p0_name=mode_p0_name,
                            mode_p1_name=mode_p1_name,
                            exact_signature_mask=mask,
                            exact_signature_subset=subset,
                        )
                    )
    return rows
