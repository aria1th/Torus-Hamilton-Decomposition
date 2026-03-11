#!/usr/bin/env python3
"""Common evaluator for the d=5 alt-4 three-flag geometry search."""

from __future__ import annotations

import json
import platform
import time
from collections import OrderedDict
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from itertools import product
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

TASK_ID = "D5-ALT4-THREE-FLAG-GEOMETRY-013"
PILOT_M_VALUES = (5, 7, 9)
STABILITY_M_VALUES = (11, 13)
OLD_BIT_NAMES = ("q=-1", "q+u=1", "w+u=2", "q+u=-1", "u=-1")
BASE_FLAG_NAMES = ("pred_sig1_wu2", "pred_sig4_wu2")
EXTRA_FLAG_NAMES = ("pred_any_phase_align", "pred_sig0_phase_align")
STATE_LABELS = tuple(f"{mask:03b}" for mask in range(8))
ALT4_MODE_TABLES = OrderedDict(
    [
        ("q=-1:2/4", {"bit_name": "q=-1", "orientation": "2/4", "s0": 2, "s1": 4}),
        ("q=-1:4/2", {"bit_name": "q=-1", "orientation": "4/2", "s0": 4, "s1": 2}),
        ("w+u=2:2/4", {"bit_name": "w+u=2", "orientation": "2/4", "s0": 2, "s1": 4}),
        ("w+u=2:4/2", {"bit_name": "w+u=2", "orientation": "4/2", "s0": 4, "s1": 2}),
    ]
)
LAYER3_FLAG_NAME = "pred_sig1_wu2"
CANONICAL_TWIST = {
    "layer3_flag_name": LAYER3_FLAG_NAME,
    "layer3_bit_name": "q+u=-1",
    "layer3_mode_p0_name": "0/3",
    "layer3_mode_p1_name": "3/0",
}
CONTROL_TWIST = {
    "layer3_flag_name": LAYER3_FLAG_NAME,
    "layer3_bit_name": "q+u=-1",
    "layer3_mode_p0_name": "3/0",
    "layer3_mode_p1_name": "0/3",
}
LAYER3_MODE_TABLES = OrderedDict(
    [
        ("0/3", (0, 3)),
        ("3/0", (3, 0)),
    ]
)
MIXED_BASELINE_TOTAL_U_CYCLES = 21
CYCLE_BASELINE_TOTAL_U_CYCLES = 15
KNOWN_ANTI_COMPRESSIVE_TOTALS = (35, 39, 57, 119, 137, 155)
FLAG_BIT_INDEX = {
    name: SIMPLE_FLAG_NAMES.index(name)
    for name in set(BASE_FLAG_NAMES) | set(EXTRA_FLAG_NAMES) | {LAYER3_FLAG_NAME}
}


@dataclass(frozen=True)
class Rule:
    extra_flag_name: str
    state_mode_names: Tuple[str, str, str, str, str, str, str, str]
    layer3_flag_name: str
    layer3_bit_name: str
    layer3_mode_p0_name: str
    layer3_mode_p1_name: str

    def state_mode_map(self) -> Dict[str, str]:
        return {label: self.state_mode_names[index] for index, label in enumerate(STATE_LABELS)}

    def payload(self) -> Dict[str, object]:
        mapping = {}
        for state_label, mode_name in self.state_mode_map().items():
            mode = ALT4_MODE_TABLES[mode_name]
            mapping[state_label] = {
                "name": mode_name,
                "bit_name": mode["bit_name"],
                "orientation": mode["orientation"],
                "table": {"s0": mode["s0"], "s1": mode["s1"]},
            }
        layer3_mode_p0 = LAYER3_MODE_TABLES[self.layer3_mode_p0_name]
        layer3_mode_p1 = LAYER3_MODE_TABLES[self.layer3_mode_p1_name]
        return {
            "extra_flag_name": self.extra_flag_name,
            "layer2_state_modes": mapping,
            "layer3_flag_name": self.layer3_flag_name,
            "layer3_bit_name": self.layer3_bit_name,
            "layer3_mode_p0": {
                "name": self.layer3_mode_p0_name,
                "table": {"s0": layer3_mode_p0[0], "s1": layer3_mode_p0[1]},
            },
            "layer3_mode_p1": {
                "name": self.layer3_mode_p1_name,
                "table": {"s0": layer3_mode_p1[0], "s1": layer3_mode_p1[1]},
            },
            "effective_key": list(self.effective_key()),
        }

    def effective_key(self) -> Tuple[object, ...]:
        return (
            self.extra_flag_name,
            *self.state_mode_names,
            self.layer3_flag_name,
            self.layer3_bit_name,
            self.layer3_mode_p0_name,
            self.layer3_mode_p1_name,
        )

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> "Rule":
        state_modes = payload["layer2_state_modes"]
        return cls(
            extra_flag_name=str(payload["extra_flag_name"]),
            state_mode_names=tuple(str(state_modes[label]["name"]) for label in STATE_LABELS),
            layer3_flag_name=str(payload["layer3_flag_name"]),
            layer3_bit_name=str(payload["layer3_bit_name"]),
            layer3_mode_p0_name=str(payload["layer3_mode_p0"]["name"]),
            layer3_mode_p1_name=str(payload["layer3_mode_p1"]["name"]),
        )


def control_rule_from(rule: Rule) -> Rule:
    return Rule(
        extra_flag_name=rule.extra_flag_name,
        state_mode_names=rule.state_mode_names,
        layer3_flag_name=CONTROL_TWIST["layer3_flag_name"],
        layer3_bit_name=CONTROL_TWIST["layer3_bit_name"],
        layer3_mode_p0_name=CONTROL_TWIST["layer3_mode_p0_name"],
        layer3_mode_p1_name=CONTROL_TWIST["layer3_mode_p1_name"],
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


def _feature_tuple(coords: Sequence[int], color: int, m: int) -> Tuple[int, int, int, int, int]:
    layer = layer_bucket(sum(coords) % m)
    layer_code = 4 if layer == "4+" else int(layer)
    q = coords[(color + 1) % DIM]
    w = coords[(color + 2) % DIM]
    u = coords[(color + 4) % DIM]
    if layer_code == 2:
        return (
            layer_code,
            old_bit_value("q=-1", q, w, u, m),
            old_bit_value("w+u=2", q, w, u, m),
            0,
            simple_flag_mask(coords, color, m),
        )
    if layer_code == 3:
        return (
            layer_code,
            0,
            0,
            old_bit_value(CANONICAL_TWIST["layer3_bit_name"], q, w, u, m),
            simple_flag_mask(coords, color, m),
        )
    return (layer_code, 0, 0, 0, 0)


def precompute_m(m: int) -> Dict[str, object]:
    n = m**DIM
    coords = [decode(idx, m) for idx in range(n)]
    step_by_dir = [[0] * n for _ in range(DIM)]
    feature_rows: List[Tuple[int, int, int, int, int]] = []
    feature_to_id: Dict[Tuple[int, int, int, int, int], int] = {}
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


def anchor_by_feature(pre: Dict[str, object], rule: Rule) -> List[int]:
    sig1_bit = FLAG_BIT_INDEX["pred_sig1_wu2"]
    sig4_bit = FLAG_BIT_INDEX["pred_sig4_wu2"]
    extra_bit = FLAG_BIT_INDEX[rule.extra_flag_name]
    layer3_flag_bit = FLAG_BIT_INDEX[rule.layer3_flag_name]
    state_modes = rule.state_mode_map()
    anchors = [0] * len(pre["feature_rows"])
    for feature_id, (layer_code, q_neg_one, wu2, layer3_s, flag_mask) in enumerate(pre["feature_rows"]):
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
            state_label = (
                f"{(flag_mask >> sig1_bit) & 1}"
                f"{(flag_mask >> sig4_bit) & 1}"
                f"{(flag_mask >> extra_bit) & 1}"
            )
            mode_name = state_modes[state_label]
            mode = ALT4_MODE_TABLES[mode_name]
            s_value = q_neg_one if mode["bit_name"] == "q=-1" else wu2
            anchors[feature_id] = mode["s1"] if s_value else mode["s0"]
            continue
        p3 = (flag_mask >> layer3_flag_bit) & 1
        mode_name = rule.layer3_mode_p1_name if p3 else rule.layer3_mode_p0_name
        mode = LAYER3_MODE_TABLES[mode_name]
        anchors[feature_id] = mode[layer3_s]
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


def nexts0_for_rule(pre: Dict[str, object], anchors: Sequence[int]) -> List[int]:
    step_by_dir = pre["step_by_dir"]
    feature_ids = pre["feature_ids_by_color"][0]
    row = [0] * pre["n"]
    for idx, feature_id in enumerate(feature_ids):
        row[idx] = step_by_dir[anchors[feature_id]][idx]
    return row


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


def cycle_signature(per_m: Mapping[str, object]) -> Tuple[Tuple[int, int, Tuple[int, ...]], ...]:
    out = []
    for m_key in sorted(per_m.keys(), key=int):
        row = per_m[m_key]["color0_return"]
        out.append((int(m_key), int(row["U_cycle_count"]), tuple(int(v) for v in row["U_cycle_lengths"])))
    return tuple(out)


def improved_over_mixed_baseline(
    per_m: Mapping[str, object],
    *,
    mixed_baseline_total_u_cycles: int = MIXED_BASELINE_TOTAL_U_CYCLES,
) -> bool:
    total_u_cycles = 0
    for row in per_m.values():
        if row["classification"]["kind"] != "both":
            return False
        total_u_cycles += int(row["color0_return"]["U_cycle_count"])
    if total_u_cycles < mixed_baseline_total_u_cycles:
        return True
    for m_key, row in per_m.items():
        if int(row["color0_return"]["U_cycle_count"]) < int(m_key):
            return True
    return False


def evaluate_rule_color0(pre_by_m: Dict[int, Dict[str, object]], rule: Rule, *, m_values: Sequence[int]) -> Dict[str, object]:
    per_m: Dict[str, object] = {}
    latin_color0_all = True
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
            clean_all = False
            strict_all = False
            continue

        nexts0 = nexts0_for_rule(pre, anchors)
        ret = first_return(pre, nexts0)
        classification = classify_return(ret)
        per_m[str(m)] = {
            "latin_color0": True,
            "color0_return": ret,
            "classification": classification,
        }
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


def evaluate_rule_full(pre_by_m: Dict[int, Dict[str, object]], rule: Rule, *, m_values: Sequence[int]) -> Dict[str, object]:
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


def rule_rows_for_extra_flag(extra_flag_name: str) -> Iterable[Rule]:
    mode_names = tuple(ALT4_MODE_TABLES.keys())
    for names in product(mode_names, repeat=len(STATE_LABELS)):
        yield Rule(
            extra_flag_name=extra_flag_name,
            state_mode_names=tuple(str(name) for name in names),
            layer3_flag_name=CANONICAL_TWIST["layer3_flag_name"],
            layer3_bit_name=CANONICAL_TWIST["layer3_bit_name"],
            layer3_mode_p0_name=CANONICAL_TWIST["layer3_mode_p0_name"],
            layer3_mode_p1_name=CANONICAL_TWIST["layer3_mode_p1_name"],
        )


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
    path = validation_summary_json or Path("artifacts/d5_alt4_two_flag_geometry_012/data/validation_summary.json")
    data = json.loads(path.read_text())
    row = next(
        item
        for item in data["candidates"]
        if item["pilot_validation"]["profile_kind"] == "both"
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


def active_bit_names_for_rule(rule: Rule) -> List[str]:
    names = list(BASE_FLAG_NAMES) + [rule.extra_flag_name]
    outputs = list(rule.state_mode_names)
    active = []
    for bit_index, bit_name in enumerate(names):
        bit_active = False
        for mask in range(8):
            partner = mask ^ (1 << (2 - bit_index))
            if outputs[mask] != outputs[partner]:
                bit_active = True
                break
        if bit_active:
            active.append(bit_name)
    return active


def dependency_class(rule: Rule) -> str:
    values = list(rule.state_mode_names)
    if len(set(values)) == 1:
        return "constant"

    bit_names = list(BASE_FLAG_NAMES) + [rule.extra_flag_name]
    for bit_index, bit_name in enumerate(bit_names):
        buckets: Dict[int, str] = {}
        valid = True
        for mask, value in enumerate(values):
            key = (mask >> (2 - bit_index)) & 1
            prev = buckets.get(key)
            if prev is None:
                buckets[key] = value
            elif prev != value:
                valid = False
                break
        if valid:
            return f"one_flag:{bit_name}"

    xor_masks = (
        (0b110, f"xor:{bit_names[0]}^{bit_names[1]}"),
        (0b101, f"xor:{bit_names[0]}^{bit_names[2]}"),
        (0b011, f"xor:{bit_names[1]}^{bit_names[2]}"),
        (0b111, f"xor:{bit_names[0]}^{bit_names[1]}^{bit_names[2]}"),
    )
    for mask_bits, label in xor_masks:
        buckets = {}
        valid = True
        for mask, value in enumerate(values):
            parity = ((mask & mask_bits).bit_count()) & 1
            prev = buckets.get(parity)
            if prev is None:
                buckets[parity] = value
            elif prev != value:
                valid = False
                break
        if valid:
            return label

    if len(active_bit_names_for_rule(rule)) == 3:
        return "genuine_eight_state"
    return "genuine_multi_state"


def rule_compact_row(result: Dict[str, object]) -> Dict[str, object]:
    rule = Rule.from_payload(result["rule"])
    return {
        "rule": result["rule"],
        "dependency_class": dependency_class(rule),
        "active_bit_names": active_bit_names_for_rule(rule),
        "distinct_mode_count": len(set(rule.state_mode_names)),
        "latin_color0_all": result["latin_color0_all"],
        "clean_all": result["clean_all"],
        "strict_all": result["strict_all"],
        "profile_kind": result["profile_kind"],
        "total_u_cycle_count": result["total_u_cycle_count"],
        "max_cycle_length": result["max_cycle_length"],
        "total_nonzero_monodromies": result["total_nonzero_monodromies"],
        "improves_mixed_baseline": result["improves_mixed_baseline"],
        "per_m_cycle_counts": {
            m_key: int(row["color0_return"]["U_cycle_count"])
            for m_key, row in result["per_m"].items()
        },
        "per_m_cycle_lengths": {
            m_key: list(int(v) for v in row["color0_return"]["U_cycle_lengths"])
            for m_key, row in result["per_m"].items()
        },
        "per_m_monodromies": {
            m_key: list(int(v) for v in row["color0_return"]["monodromies"])
            for m_key, row in result["per_m"].items()
        },
    }


def overall_rank_key(result: Mapping[str, object]) -> Tuple[object, ...]:
    kind_order = {"both": 0, "cycle_only": 1, "monodromy_only": 2, "mixed_profile": 3, "trivial": 4, "invalid": 5}
    rule = result["rule"]
    modes = rule["layer2_state_modes"]
    return (
        not result["clean_all"],
        not result["strict_all"],
        not result["improves_mixed_baseline"],
        kind_order.get(str(result["profile_kind"]), 9),
        int(result["total_u_cycle_count"]),
        -int(result["total_nonzero_monodromies"]),
        -int(result["max_cycle_length"]),
        tuple(modes[label]["name"] for label in STATE_LABELS),
    )
