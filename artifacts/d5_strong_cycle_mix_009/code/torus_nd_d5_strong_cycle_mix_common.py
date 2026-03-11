#!/usr/bin/env python3
"""Common evaluator for the d=5 strong cycle + twist graft search."""

from __future__ import annotations

import json
import platform
import time
from collections import OrderedDict
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from torus_nd_d5_layer3_mode_switch_common import SIMPLE_FLAG_NAMES, simple_flag_mask
from torus_nd_d5_master_field_quotient_family import atom_truths
from torus_nd_d5_strict_palette_context_common import (
    DIM,
    decode,
    encode,
    first_return,
    incoming_latin_all,
    layer_bucket,
    parse_m_list,
)

TASK_ID = "D5-STRONG-CYCLE-MIX-009"
PILOT_M_VALUES = (5, 7, 9)
STABILITY_M_VALUES = (11, 13)
OLD_BIT_NAMES = ("q=-1", "q+u=1", "w+u=2", "q+u=-1", "u=-1")
LAYER2_ALTERNATES = OrderedDict(
    [
        ("q=-1", (0, 3, 4)),
        ("q+u=1", (0, 3)),
        ("q+u=-1", (0, 3)),
        ("u=-1", (0, 3)),
        ("w+u=2", (4,)),
    ]
)
STAGE1_LAYER3_BITS = ("q=-1",)
STAGE2_LAYER3_BITS = ("q=-1", "q+u=1", "q+u=-1", "u=-1")
TWIST_FLAG_NAMES = ("pred_sig1_wu2", "pred_sig4_wu2")
TWIST_MODE_TABLES = OrderedDict(
    [
        ("0/3", (0, 3)),
        ("3/0", (3, 0)),
        ("3/3", (3, 3)),
    ]
)
MIXED_BASELINE_TOTAL_U_CYCLES = 21
MIXED_BASELINE_MAX_CYCLE_LENGTH = 9
CYCLE_BASELINE_TOTAL_U_CYCLES = 15
LAYER3_FLAG_BIT_INDEX = {
    "pred_sig1_wu2": SIMPLE_FLAG_NAMES.index("pred_sig1_wu2"),
    "pred_sig4_wu2": SIMPLE_FLAG_NAMES.index("pred_sig4_wu2"),
}


@dataclass(frozen=True)
class Rule:
    stage: str
    layer2_bit_name: str
    layer2_alt: int
    layer2_orientation_name: str
    layer2_s0_anchor: int
    layer2_s1_anchor: int
    layer3_bit_name: str
    predecessor_flag_name: str
    mode_p0_name: str
    mode_p1_name: str

    def payload(self) -> Dict[str, object]:
        return {
            "stage": self.stage,
            "layer2_bit_name": self.layer2_bit_name,
            "layer2_alt": self.layer2_alt,
            "layer2_orientation": self.layer2_orientation_name,
            "layer2_table": {"s0": self.layer2_s0_anchor, "s1": self.layer2_s1_anchor},
            "layer3_bit_name": self.layer3_bit_name,
            "predecessor_flag_name": self.predecessor_flag_name,
            "layer3_mode_p0": {"name": self.mode_p0_name, "table": {"s0": TWIST_MODE_TABLES[self.mode_p0_name][0], "s1": TWIST_MODE_TABLES[self.mode_p0_name][1]}},
            "layer3_mode_p1": {"name": self.mode_p1_name, "table": {"s0": TWIST_MODE_TABLES[self.mode_p1_name][0], "s1": TWIST_MODE_TABLES[self.mode_p1_name][1]}},
            "effective_key": list(self.effective_key()),
        }

    def effective_key(self) -> Tuple[object, ...]:
        return (
            self.layer2_bit_name,
            self.layer2_alt,
            self.layer2_orientation_name,
            self.layer3_bit_name,
            self.predecessor_flag_name,
            self.mode_p0_name,
            self.mode_p1_name,
        )

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> "Rule":
        return cls(
            stage=str(payload["stage"]),
            layer2_bit_name=str(payload["layer2_bit_name"]),
            layer2_alt=int(payload["layer2_alt"]),
            layer2_orientation_name=str(payload["layer2_orientation"]),
            layer2_s0_anchor=int(payload["layer2_table"]["s0"]),
            layer2_s1_anchor=int(payload["layer2_table"]["s1"]),
            layer3_bit_name=str(payload["layer3_bit_name"]),
            predecessor_flag_name=str(payload["predecessor_flag_name"]),
            mode_p0_name=str(payload["layer3_mode_p0"]["name"]),
            mode_p1_name=str(payload["layer3_mode_p1"]["name"]),
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


def old_bit_value(old_bit_name: str, q: int, w: int, u: int, m: int) -> int:
    truths = atom_truths(q, w, u, m)
    index = OLD_BIT_NAMES.index(old_bit_name)
    return int(truths[index])


def _feature_tuple(coords: Sequence[int], color: int, m: int, layer2_bit_name: str, layer3_bit_name: str) -> Tuple[int, int, int, int]:
    layer = layer_bucket(sum(coords) % m)
    layer_code = 4 if layer == "4+" else int(layer)
    if layer_code == 2:
        q = coords[(color + 1) % DIM]
        w = coords[(color + 2) % DIM]
        u = coords[(color + 4) % DIM]
        return (layer_code, old_bit_value(layer2_bit_name, q, w, u, m), 0, 0)
    if layer_code == 3:
        q = coords[(color + 1) % DIM]
        w = coords[(color + 2) % DIM]
        u = coords[(color + 4) % DIM]
        return (layer_code, 0, old_bit_value(layer3_bit_name, q, w, u, m), simple_flag_mask(coords, color, m))
    return (layer_code, 0, 0, 0)


def precompute_m(m: int, layer2_bit_name: str, layer3_bit_name: str) -> Dict[str, object]:
    n = m**DIM
    coords = [decode(idx, m) for idx in range(n)]
    step_by_dir = [[0] * n for _ in range(DIM)]
    feature_rows: List[Tuple[int, int, int, int]] = []
    feature_to_id: Dict[Tuple[int, int, int, int], int] = {}
    feature_ids_by_color = [[0] * n for _ in range(DIM)]

    for idx, vertex in enumerate(coords):
        for direction in range(DIM):
            nxt = list(vertex)
            nxt[direction] = (nxt[direction] + 1) % m
            step_by_dir[direction][idx] = encode(nxt, m)
        for color in range(DIM):
            feature = _feature_tuple(vertex, color, m, layer2_bit_name, layer3_bit_name)
            feature_id = feature_to_id.get(feature)
            if feature_id is None:
                feature_id = len(feature_rows)
                feature_to_id[feature] = feature_id
                feature_rows.append(feature)
            feature_ids_by_color[color][idx] = feature_id

    color0_patterns = set()
    for vertex in coords:
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
    mode_p0 = TWIST_MODE_TABLES[rule.mode_p0_name]
    mode_p1 = TWIST_MODE_TABLES[rule.mode_p1_name]
    flag_bit_index = LAYER3_FLAG_BIT_INDEX[rule.predecessor_flag_name]
    anchors = [0] * len(pre["feature_rows"])
    for feature_id, (layer_code, s2, s3, flag_mask) in enumerate(pre["feature_rows"]):
        if layer_code == 0:
            anchors[feature_id] = 1
        elif layer_code == 1:
            anchors[feature_id] = 4
        elif layer_code == 2:
            anchors[feature_id] = rule.layer2_s0_anchor if s2 == 0 else rule.layer2_s1_anchor
        elif layer_code == 3:
            p_bit = (flag_mask >> flag_bit_index) & 1
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
        feature_ids = pre["feature_ids_by_color"][color]
        row = nexts[color]
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


def improved_over_mixed_baseline(result: Dict[str, object], *, mixed_baseline_total_u_cycles: int = MIXED_BASELINE_TOTAL_U_CYCLES) -> bool:
    if not (result["clean_all"] and result["strict_all"] and result["overall_kind"] == "both"):
        return False
    if result["total_u_cycle_count"] < mixed_baseline_total_u_cycles:
        return True
    for m_key, row in result["per_m"].items():
        m = int(m_key)
        if row["color0_return"]["U_cycle_count"] < m:
            return True
    return False


def evaluate_rule(pre_by_m: Dict[int, Dict[str, object]], rule: Rule, *, m_values: Sequence[int]) -> Dict[str, object]:
    per_m: Dict[str, object] = {}
    latin_color0_all = True
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
            latin_color0_all = False
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
        latin_color0_all &= latin0
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

    result = {
        "rule": rule.payload(),
        "per_m": per_m,
        "latin_color0_all": latin_color0_all,
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
    result["improves_mixed_baseline"] = improved_over_mixed_baseline(result)
    return result


def overall_rank_key(result: Dict[str, object]) -> Tuple[object, ...]:
    kind_order = {"both": 0, "cycle_only": 1, "monodromy_only": 2, "trivial": 3}
    rule = result["rule"]
    return (
        not result["clean_all"],
        not result["strict_all"],
        not result["improves_mixed_baseline"],
        kind_order[result["overall_kind"]],
        result["total_u_cycle_count"],
        -result["max_cycle_length"],
        -result["total_nonzero_monodromies"],
        rule["stage"],
        rule["layer2_bit_name"],
        rule["layer2_alt"],
        rule["layer2_orientation"],
        rule["layer3_bit_name"],
        rule["predecessor_flag_name"],
        rule["layer3_mode_p0"]["name"],
        rule["layer3_mode_p1"]["name"],
    )


def layer2_seed_rows() -> List[Tuple[str, int, str, int, int]]:
    rows = []
    for bit_name, alternates in LAYER2_ALTERNATES.items():
        for alt in alternates:
            rows.append((bit_name, alt, f"2/{alt}", 2, alt))
            rows.append((bit_name, alt, f"{alt}/2", alt, 2))
    return rows


def twist_mode_pairs() -> List[Tuple[str, str]]:
    names = list(TWIST_MODE_TABLES)
    return [(left, right) for left in names for right in names if left != right]


def stage_rows(stage: str) -> List[Rule]:
    layer3_bits = STAGE1_LAYER3_BITS if stage == "stage1" else STAGE2_LAYER3_BITS
    rows = []
    for layer2_bit_name, layer2_alt, orientation_name, s0_anchor, s1_anchor in layer2_seed_rows():
        for layer3_bit_name in layer3_bits:
            for predecessor_flag_name in TWIST_FLAG_NAMES:
                for mode_p0_name, mode_p1_name in twist_mode_pairs():
                    rows.append(
                        Rule(
                            stage=stage,
                            layer2_bit_name=layer2_bit_name,
                            layer2_alt=layer2_alt,
                            layer2_orientation_name=orientation_name,
                            layer2_s0_anchor=s0_anchor,
                            layer2_s1_anchor=s1_anchor,
                            layer3_bit_name=layer3_bit_name,
                            predecessor_flag_name=predecessor_flag_name,
                            mode_p0_name=mode_p0_name,
                            mode_p1_name=mode_p1_name,
                        )
                    )
    return rows


def load_cycle_baseline(search_summary_json: Path | None = None) -> Dict[str, object]:
    path = search_summary_json or Path("artifacts/d5_layer3_alt2_decoupled_007/data/search_summary.json")
    data = json.loads(path.read_text())
    row = data["best_cycle_only_rules"][0]
    return {
        "source": str(path),
        "rule": row["rule"],
        "total_u_cycle_count": row["total_u_cycle_count"],
        "max_cycle_length": row["max_cycle_length"],
        "total_nonzero_monodromies": row["total_nonzero_monodromies"],
    }


def load_mixed_baseline(validation_summary_json: Path | None = None) -> Dict[str, object]:
    path = validation_summary_json or Path("artifacts/d5_layer3_mode_switch_008/data/validation_summary.json")
    data = json.loads(path.read_text())
    row = next(item for item in data["candidates"] if item["pilot_validation"]["overall_kind"] == "both")
    pilot = row["pilot_validation"]
    return {
        "source": str(path),
        "rule": row["rule"],
        "total_u_cycle_count": pilot["total_u_cycle_count"],
        "max_cycle_length": pilot["max_cycle_length"],
        "total_nonzero_monodromies": pilot["total_nonzero_monodromies"],
        "per_m": pilot["per_m"],
    }
