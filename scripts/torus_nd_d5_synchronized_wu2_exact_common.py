#!/usr/bin/env python3
"""Common evaluator for the d=5 synchronized wu2 exact-bit search."""

from __future__ import annotations

import json
import platform
import time
from collections import OrderedDict
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from torus_nd_d5_layer3_mode_switch_common import simple_flag_mask
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

TASK_ID = "D5-SYNCHRONIZED-WU2-EXACT-016"
PILOT_M_VALUES = (5, 7, 9)
STABILITY_M_VALUES = (11, 13)
OLD_BIT_NAMES = ("q=-1", "q+u=1", "w+u=2", "q+u=-1", "u=-1")
CONTROLLER_FLAG_NAMES = ("pred_sig1_wu2", "pred_sig4_wu2")
EXACT_BIT_NAME = "pred_sig1_phase_align"
LAYER2_BASES = OrderedDict(
    [
        ("const_2/4", {"mode_name": "w+u=2:2/4", "flip_mode_name": "w+u=2:4/2"}),
        ("const_4/2", {"mode_name": "w+u=2:4/2", "flip_mode_name": "w+u=2:2/4"}),
    ]
)
ALT4_MODE_TABLES = OrderedDict(
    [
        ("w+u=2:2/4", {"bit_name": "w+u=2", "orientation": "2/4", "s0": 2, "s1": 4}),
        ("w+u=2:4/2", {"bit_name": "w+u=2", "orientation": "4/2", "s0": 4, "s1": 2}),
    ]
)
SYNC_FLIP_PATTERNS = OrderedDict(
    [
        ("p0_base_p1_flip", {"p0": "base", "p1": "flip"}),
        ("p0_flip_p1_base", {"p0": "flip", "p1": "base"}),
    ]
)
SLICE_MODES = OrderedDict(
    [
        ("0/3", (0, 3)),
        ("3/0", (3, 0)),
        ("3/3", (3, 3)),
    ]
)
STAGE1_OLD_BITS = ("q+u=-1",)
STAGE2_OLD_BITS = ("q+u=1", "q+u=-1", "u=-1")
MIXED_BASELINE_TOTAL_U_CYCLES = 21
CYCLE_BASELINE_TOTAL_U_CYCLES = 15
KNOWN_ANTI_COMPRESSIVE_TOTALS = (35, 39, 57, 119, 137, 155)


@dataclass(frozen=True)
class Rule:
    stage: str
    layer2_base_name: str
    controller_flag_name: str
    layer3_old_bit_name: str
    sync_flip_pattern_name: str
    mode_00_name: str
    mode_01_name: str
    mode_10_name: str
    mode_11_name: str

    def controller_mode_map(self) -> Dict[str, str]:
        return {
            "00": self.mode_00_name,
            "01": self.mode_01_name,
            "10": self.mode_10_name,
            "11": self.mode_11_name,
        }

    def layer2_state_modes(self) -> Dict[str, str]:
        base_info = LAYER2_BASES[self.layer2_base_name]
        base_mode_name = str(base_info["mode_name"])
        flip_mode_name = str(base_info["flip_mode_name"])
        pattern = SYNC_FLIP_PATTERNS[self.sync_flip_pattern_name]
        return {
            "00": base_mode_name,
            "01": base_mode_name,
            "10": base_mode_name if pattern["p0"] == "base" else flip_mode_name,
            "11": base_mode_name if pattern["p1"] == "base" else flip_mode_name,
        }

    def payload(self) -> Dict[str, object]:
        layer2_modes = {}
        for label, mode_name in self.layer2_state_modes().items():
            table = ALT4_MODE_TABLES[mode_name]
            layer2_modes[label] = {
                "name": mode_name,
                "table": {"bit_name": table["bit_name"], "s0": table["s0"], "s1": table["s1"]},
            }
        layer3_modes = {}
        for label, mode_name in self.controller_mode_map().items():
            s0, s1 = SLICE_MODES[mode_name]
            layer3_modes[label] = {"name": mode_name, "table": {"s0": s0, "s1": s1}}
        return {
            "stage": self.stage,
            "layer2_base_name": self.layer2_base_name,
            "controller_flag_name": self.controller_flag_name,
            "exact_bit_name": EXACT_BIT_NAME,
            "layer3_old_bit_name": self.layer3_old_bit_name,
            "sync_flip_pattern_name": self.sync_flip_pattern_name,
            "layer2_modes": layer2_modes,
            "layer3_modes": layer3_modes,
            "effective_key": list(self.effective_key()),
        }

    def effective_key(self) -> Tuple[object, ...]:
        return (
            self.stage,
            self.layer2_base_name,
            self.controller_flag_name,
            self.layer3_old_bit_name,
            self.sync_flip_pattern_name,
            self.mode_00_name,
            self.mode_01_name,
            self.mode_10_name,
            self.mode_11_name,
        )

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> "Rule":
        modes = payload["layer3_modes"]
        return cls(
            stage=str(payload["stage"]),
            layer2_base_name=str(payload["layer2_base_name"]),
            controller_flag_name=str(payload["controller_flag_name"]),
            layer3_old_bit_name=str(payload["layer3_old_bit_name"]),
            sync_flip_pattern_name=str(payload["sync_flip_pattern_name"]),
            mode_00_name=str(modes["00"]["name"]),
            mode_01_name=str(modes["01"]["name"]),
            mode_10_name=str(modes["10"]["name"]),
            mode_11_name=str(modes["11"]["name"]),
        )


def control_rule_from(rule: Rule) -> Rule:
    swap = {"0/3": "3/0", "3/0": "0/3", "3/3": "3/3"}
    return Rule(
        stage="control",
        layer2_base_name=rule.layer2_base_name,
        controller_flag_name=rule.controller_flag_name,
        layer3_old_bit_name=rule.layer3_old_bit_name,
        sync_flip_pattern_name=rule.sync_flip_pattern_name,
        mode_00_name=swap[rule.mode_00_name],
        mode_01_name=swap[rule.mode_01_name],
        mode_10_name=swap[rule.mode_10_name],
        mode_11_name=swap[rule.mode_11_name],
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
    return int(truths[OLD_BIT_NAMES.index(old_bit_name)])


def exact_bit_value(coords: Sequence[int], color: int, m: int) -> int:
    pred = list(coords)
    pred[(color + 1) % DIM] = (pred[(color + 1) % DIM] - 1) % m
    q = pred[(color + 1) % DIM]
    v = pred[(color + 3) % DIM]
    return int((v - q) % m == 0)


def _feature_tuple(coords: Sequence[int], color: int, m: int) -> Tuple[int, int, int, int, int, int, int]:
    layer = layer_bucket(sum(coords) % m)
    layer_code = 4 if layer == "4+" else int(layer)
    q = coords[(color + 1) % DIM]
    w = coords[(color + 2) % DIM]
    u = coords[(color + 4) % DIM]
    flag_mask = simple_flag_mask(coords, color, m)
    return (
        layer_code,
        old_bit_value("w+u=2", q, w, u, m),
        old_bit_value("q+u=1", q, w, u, m),
        old_bit_value("q+u=-1", q, w, u, m),
        old_bit_value("u=-1", q, w, u, m),
        flag_mask,
        exact_bit_value(coords, color, m),
    )


def precompute_m(m: int) -> Dict[str, object]:
    n = m**DIM
    coords = [decode(idx, m) for idx in range(n)]
    step_by_dir = [[0] * n for _ in range(DIM)]
    feature_rows: List[Tuple[int, int, int, int, int, int, int]] = []
    feature_to_id: Dict[Tuple[int, int, int, int, int, int, int], int] = {}
    feature_ids_by_color = [[0] * n for _ in range(DIM)]
    for idx, vertex in enumerate(coords):
        for direction in range(DIM):
            nxt = list(vertex)
            nxt[direction] = (nxt[direction] + 1) % m
            step_by_dir[direction][idx] = encode(nxt, m)
        for color in range(DIM):
            feature = _feature_tuple(vertex, color, m)
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


def anchor_by_feature(pre: Mapping[str, object], rule: Rule) -> List[int]:
    anchors = [0] * len(pre["feature_rows"])
    base_info = LAYER2_BASES[rule.layer2_base_name]
    base_mode = ALT4_MODE_TABLES[str(base_info["mode_name"])]
    flip_mode = ALT4_MODE_TABLES[str(base_info["flip_mode_name"])]
    controller_bit_index = 2 if rule.controller_flag_name == "pred_sig1_wu2" else 3
    layer3_mapping = rule.controller_mode_map()
    sync_pattern = SYNC_FLIP_PATTERNS[rule.sync_flip_pattern_name]

    for feature_id, feature in enumerate(pre["feature_rows"]):
        layer_code, wu2, qpu1, qpun1, un1, flag_mask, exact_p = feature
        if layer_code == 0:
            anchors[feature_id] = 1
            continue
        if layer_code == 1:
            anchors[feature_id] = 4
            continue
        if layer_code == 4:
            anchors[feature_id] = 0
            continue
        if layer_code == 2:
            r = (flag_mask >> controller_bit_index) & 1
            if r == 0:
                mode = base_mode
            else:
                state = sync_pattern[f"p{exact_p}"]
                mode = base_mode if state == "base" else flip_mode
            anchors[feature_id] = mode["s1"] if wu2 else mode["s0"]
            continue
        r = (flag_mask >> controller_bit_index) & 1
        p = exact_p
        mode_name = layer3_mapping[f"{r}{p}"]
        s0, s1 = SLICE_MODES[mode_name]
        s_value = {"q+u=1": qpu1, "q+u=-1": qpun1, "u=-1": un1}[rule.layer3_old_bit_name]
        anchors[feature_id] = s1 if s_value else s0
    return anchors


def color0_is_latin(pre: Mapping[str, object], anchors: Sequence[int]) -> bool:
    for token0, token1, token2, token3, token4 in pre["color0_patterns"]:
        indegree = int(anchors[token0] == 0)
        indegree += int(anchors[token1] == 1)
        indegree += int(anchors[token2] == 2)
        indegree += int(anchors[token3] == 3)
        indegree += int(anchors[token4] == 4)
        if indegree != 1:
            return False
    return True


def nexts_all_for_rule(pre: Mapping[str, object], anchors: Sequence[int]) -> List[List[int]]:
    step_by_dir = pre["step_by_dir"]
    nexts = [[0] * pre["n"] for _ in range(DIM)]
    for color in range(DIM):
        color_dirs = tuple((anchor + color) % DIM for anchor in anchors)
        feature_ids = pre["feature_ids_by_color"][color]
        row = nexts[color]
        for idx, feature_id in enumerate(feature_ids):
            row[idx] = step_by_dir[color_dirs[feature_id]][idx]
    return nexts


def classify_return(ret: Mapping[str, object]) -> Dict[str, object]:
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


def cycle_signature(per_m: Mapping[str, object]) -> Tuple[Tuple[int, int, Tuple[int, ...]], ...]:
    out = []
    for m_key in sorted(per_m.keys(), key=int):
        row = per_m[m_key]["color0_return"]
        out.append((int(m_key), int(row["U_cycle_count"]), tuple(int(v) for v in row["U_cycle_lengths"])))
    return tuple(out)


def improved_over_mixed_baseline(per_m: Mapping[str, object]) -> bool:
    total_u_cycles = 0
    for row in per_m.values():
        if row["classification"]["kind"] != "both":
            return False
        total_u_cycles += int(row["color0_return"]["U_cycle_count"])
    if total_u_cycles < MIXED_BASELINE_TOTAL_U_CYCLES:
        return True
    for m_key, row in per_m.items():
        if int(row["color0_return"]["U_cycle_count"]) < int(m_key):
            return True
    return False


def evaluate_rule(pre_by_m: Mapping[int, Mapping[str, object]], rule: Rule, *, m_values: Sequence[int]) -> Dict[str, object]:
    per_m: Dict[str, object] = {}
    latin_color0_all = True
    latin_all = True
    clean_all = True
    strict_all = True
    total_u_cycle_count = 0
    total_nonzero_monodromies = 0
    max_cycle_length = 0
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
        total_u_cycle_count += int(ret["U_cycle_count"])
        total_nonzero_monodromies += sum(1 for value in ret["monodromies"] if value != 0)
        if ret["U_cycle_lengths"]:
            max_cycle_length = max(max_cycle_length, max(ret["U_cycle_lengths"]))
    per_m_kinds = tuple(per_m[str(m)]["classification"]["kind"] for m in m_values)
    profile_kind = per_m_kinds[0] if len(set(per_m_kinds)) == 1 else "mixed_profile"
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
        "profile_kind": profile_kind,
        "cycle_signature": cycle_signature(per_m),
    }
    result["improves_mixed_baseline"] = improved_over_mixed_baseline(per_m)
    return result


def rule_rows(stage: str) -> Iterable[Rule]:
    old_bits = STAGE1_OLD_BITS if stage == "stage1" else STAGE2_OLD_BITS
    for base_name in LAYER2_BASES:
        for controller_flag_name in CONTROLLER_FLAG_NAMES:
            for old_bit_name in old_bits:
                for sync_flip_pattern_name in SYNC_FLIP_PATTERNS:
                    for mode_00_name in SLICE_MODES:
                        for mode_01_name in SLICE_MODES:
                            for mode_10_name in SLICE_MODES:
                                for mode_11_name in SLICE_MODES:
                                    yield Rule(
                                        stage=stage,
                                        layer2_base_name=base_name,
                                        controller_flag_name=controller_flag_name,
                                        layer3_old_bit_name=old_bit_name,
                                        sync_flip_pattern_name=sync_flip_pattern_name,
                                        mode_00_name=mode_00_name,
                                        mode_01_name=mode_01_name,
                                        mode_10_name=mode_10_name,
                                        mode_11_name=mode_11_name,
                                    )


def layer3_dependency_class(rule: Rule) -> str:
    rows = rule.controller_mode_map()
    if rows["00"] == rows["01"] and rows["10"] == rows["11"]:
        if rows["00"] == rows["10"]:
            return "constant"
        return "p_trivial_within_r"
    if rows["00"] == rows["10"] and rows["01"] == rows["11"]:
        return "r_trivial_within_p"
    if rows["00"] == rows["11"] and rows["01"] == rows["10"]:
        return "xor_like"
    return "genuine_p_refinement"


def synchronized_dependency_class(rule: Rule) -> str:
    layer3_class = layer3_dependency_class(rule)
    if layer3_class == "constant":
        return "layer2_sync_plus_constant_layer3"
    if layer3_class == "p_trivial_within_r":
        return "layer2_sync_plus_r_only_layer3"
    if layer3_class == "r_trivial_within_p":
        return "layer2_sync_plus_p_only_layer3"
    if layer3_class == "xor_like":
        return "layer2_sync_plus_xor_layer3"
    return "genuine_sync_both_layers"


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
    row = next(
        item
        for item in data["candidates"]
        if item["pilot_validation"]["overall_kind"] == "both"
        and item["pilot_validation"]["total_u_cycle_count"] == MIXED_BASELINE_TOTAL_U_CYCLES
    )
    pilot = row["pilot_validation"]
    return {
        "source": str(path),
        "rule": row["rule"],
        "total_u_cycle_count": pilot["total_u_cycle_count"],
        "max_cycle_length": pilot["max_cycle_length"],
        "total_nonzero_monodromies": pilot["total_nonzero_monodromies"],
        "per_m": pilot["per_m"],
    }


def overall_rank_key(result: Mapping[str, object]) -> Tuple[object, ...]:
    kind_order = {"both": 0, "cycle_only": 1, "monodromy_only": 2, "mixed_profile": 3, "trivial": 4, "invalid": 5}
    return (
        not result["clean_all"],
        not result["strict_all"],
        not result["improves_mixed_baseline"],
        kind_order.get(str(result["profile_kind"]), 9),
        int(result["total_u_cycle_count"]),
        -int(result["total_nonzero_monodromies"]),
        -int(result["max_cycle_length"]),
        tuple(result["rule"]["effective_key"]),
    )
