#!/usr/bin/env python3
"""Common helpers for the d=5 exact-signature diagnostic and coupled mode-switch search."""

from __future__ import annotations

import json
import platform
import time
from collections import OrderedDict
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from torus_nd_d5_layer3_mode_switch_common import exact_predecessor_signature, simple_flag_mask
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

TASK_ID = "D5-SIGNATURE-DIAG-AND-COUPLED-MODESWITCH-014"
PILOT_M_VALUES = (5, 7, 9)
STABILITY_M_VALUES = (11, 13)
OLD_BIT_NAMES = ("q=-1", "q+u=1", "w+u=2", "q+u=-1", "u=-1")
NAMED_FLAG_NAMES = (
    "pred_any_phase_align",
    "pred_sig0_phase_align",
    "pred_sig1_wu2",
    "pred_sig4_wu2",
)
EXACT_BIT_NAME = "pred_sig1_phase_align"
EXACT_BIT_DESCRIPTION = "phase_align on the predecessor in color-relative direction 1; exact signature coordinate 2"
ALT4_MODE_TABLES = OrderedDict(
    [
        ("q=-1:2/4", {"bit_name": "q=-1", "orientation": "2/4", "s0": 2, "s1": 4}),
        ("q=-1:4/2", {"bit_name": "q=-1", "orientation": "4/2", "s0": 4, "s1": 2}),
        ("w+u=2:2/4", {"bit_name": "w+u=2", "orientation": "2/4", "s0": 2, "s1": 4}),
        ("w+u=2:4/2", {"bit_name": "w+u=2", "orientation": "4/2", "s0": 4, "s1": 2}),
    ]
)
LAYER2_MODE_TABLES = OrderedDict(
    [
        (
            "const_2/4",
            {"kind": "constant", "p0_mode_name": "w+u=2:2/4", "p1_mode_name": "w+u=2:2/4"},
        ),
        (
            "const_4/2",
            {"kind": "constant", "p0_mode_name": "w+u=2:4/2", "p1_mode_name": "w+u=2:4/2"},
        ),
        (
            "flip_p0",
            {"kind": "switch", "p0_mode_name": "w+u=2:4/2", "p1_mode_name": "w+u=2:2/4"},
        ),
        (
            "flip_p1",
            {"kind": "switch", "p0_mode_name": "w+u=2:2/4", "p1_mode_name": "w+u=2:4/2"},
        ),
    ]
)
LAYER3_SLICE_MODES = OrderedDict(
    [
        ("0/3", (0, 3)),
        ("3/0", (3, 0)),
        ("3/3", (3, 3)),
    ]
)
CANONICAL_LAYER3_OLD_BIT = "q+u=-1"
CANONICAL_LAYER3_FLAG = "pred_sig1_wu2"
COUPLED_LAYER3_OLD_BITS_STAGE1 = ("q+u=-1",)
COUPLED_LAYER3_OLD_BITS_STAGE2 = ("q+u=1", "u=-1")
COUPLED_LAYER3_OLD_BITS_STAGE3 = ("q+u=1", "q+u=-1", "u=-1")
MIXED_BASELINE_TOTAL_U_CYCLES = 21
CYCLE_BASELINE_TOTAL_U_CYCLES = 15
KNOWN_ANTI_COMPRESSIVE_TOTALS = (35, 39, 57, 119, 137, 155)


@dataclass(frozen=True)
class StageARule:
    mode_p0_name: str
    mode_p1_name: str

    def payload(self) -> Dict[str, object]:
        return {
            "kind": "stage_a",
            "exact_bit_name": EXACT_BIT_NAME,
            "mode_p0": _mode_payload(self.mode_p0_name),
            "mode_p1": _mode_payload(self.mode_p1_name),
            "effective_key": list(self.effective_key()),
        }

    def effective_key(self) -> Tuple[object, ...]:
        return ("stage_a", self.mode_p0_name, self.mode_p1_name)

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> "StageARule":
        return cls(
            mode_p0_name=str(payload["mode_p0"]["name"]),
            mode_p1_name=str(payload["mode_p1"]["name"]),
        )


@dataclass(frozen=True)
class StageBRule:
    stage: str
    layer2_mode_name: str
    layer3_old_bit_name: str
    mode_p0_name: str
    mode_p1_name: str

    def payload(self) -> Dict[str, object]:
        return {
            "kind": "stage_b",
            "stage": self.stage,
            "exact_bit_name": EXACT_BIT_NAME,
            "layer2_mode": _layer2_mode_payload(self.layer2_mode_name),
            "layer3_old_bit_name": self.layer3_old_bit_name,
            "mode_p0": _slice_payload(self.mode_p0_name),
            "mode_p1": _slice_payload(self.mode_p1_name),
            "effective_key": list(self.effective_key()),
        }

    def effective_key(self) -> Tuple[object, ...]:
        return (
            "stage_b",
            self.stage,
            self.layer2_mode_name,
            self.layer3_old_bit_name,
            self.mode_p0_name,
            self.mode_p1_name,
        )

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> "StageBRule":
        return cls(
            stage=str(payload["stage"]),
            layer2_mode_name=str(payload["layer2_mode"]["name"]),
            layer3_old_bit_name=str(payload["layer3_old_bit_name"]),
            mode_p0_name=str(payload["mode_p0"]["name"]),
            mode_p1_name=str(payload["mode_p1"]["name"]),
        )

    def uses_two_slice_modes(self) -> bool:
        return self.mode_p0_name != self.mode_p1_name


def control_rule_from(rule: StageBRule) -> StageBRule:
    swap = {"0/3": "3/0", "3/0": "0/3", "3/3": "3/3"}
    return StageBRule(
        stage="control",
        layer2_mode_name=rule.layer2_mode_name,
        layer3_old_bit_name=rule.layer3_old_bit_name,
        mode_p0_name=swap[rule.mode_p0_name],
        mode_p1_name=swap[rule.mode_p1_name],
    )


def _mode_payload(mode_name: str) -> Dict[str, object]:
    mode = ALT4_MODE_TABLES[mode_name]
    return {
        "name": mode_name,
        "bit_name": mode["bit_name"],
        "orientation": mode["orientation"],
        "table": {"s0": mode["s0"], "s1": mode["s1"]},
    }


def _layer2_mode_payload(mode_name: str) -> Dict[str, object]:
    row = LAYER2_MODE_TABLES[mode_name]
    return {
        "name": mode_name,
        "kind": row["kind"],
        "p0_mode": _mode_payload(row["p0_mode_name"]),
        "p1_mode": _mode_payload(row["p1_mode_name"]),
    }


def _slice_payload(mode_name: str) -> Dict[str, object]:
    s0, s1 = LAYER3_SLICE_MODES[mode_name]
    return {"name": mode_name, "table": {"s0": s0, "s1": s1}}


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
    return int(exact_predecessor_signature(coords, color, m)[2])


def _feature_tuple(coords: Sequence[int], color: int, m: int) -> Tuple[int, int, int, int, int, int, int]:
    layer = layer_bucket(sum(coords) % m)
    layer_code = 4 if layer == "4+" else int(layer)
    q = coords[(color + 1) % DIM]
    w = coords[(color + 2) % DIM]
    u = coords[(color + 4) % DIM]
    flag_mask = simple_flag_mask(coords, color, m)
    return (
        layer_code,
        old_bit_value("q=-1", q, w, u, m),
        old_bit_value("w+u=2", q, w, u, m),
        old_bit_value("q+u=1", q, w, u, m),
        old_bit_value("q+u=-1", q, w, u, m),
        old_bit_value("u=-1", q, w, u, m),
        (flag_mask >> 2) & 1,
        exact_bit_value(coords, color, m),
    )


def precompute_m(m: int) -> Dict[str, object]:
    n = m**DIM
    coords = [decode(idx, m) for idx in range(n)]
    step_by_dir = [[0] * n for _ in range(DIM)]
    feature_rows: List[Tuple[int, int, int, int, int, int, int, int]] = []
    feature_to_id: Dict[Tuple[int, int, int, int, int, int, int, int], int] = {}
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


def _stage_a_anchor_by_feature(pre: Mapping[str, object], rule: StageARule) -> List[int]:
    anchors = [0] * len(pre["feature_rows"])
    for feature_id, feature in enumerate(pre["feature_rows"]):
        layer_code, q_neg_one, wu2, qpu1, qpun1, un1, pred_sig1_wu2, exact_p = feature
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
            mode_name = rule.mode_p1_name if exact_p else rule.mode_p0_name
            mode = ALT4_MODE_TABLES[mode_name]
            s_value = q_neg_one if mode["bit_name"] == "q=-1" else wu2
            anchors[feature_id] = mode["s1"] if s_value else mode["s0"]
            continue
        layer3_mode_name = "3/0" if pred_sig1_wu2 else "0/3"
        s0, s1 = LAYER3_SLICE_MODES[layer3_mode_name]
        anchors[feature_id] = s1 if qpun1 else s0
    return anchors


def _stage_b_anchor_by_feature(pre: Mapping[str, object], rule: StageBRule) -> List[int]:
    anchors = [0] * len(pre["feature_rows"])
    layer2_mode = LAYER2_MODE_TABLES[rule.layer2_mode_name]
    for feature_id, feature in enumerate(pre["feature_rows"]):
        layer_code, q_neg_one, wu2, qpu1, qpun1, un1, pred_sig1_wu2, exact_p = feature
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
            mode_name = layer2_mode["p1_mode_name"] if exact_p else layer2_mode["p0_mode_name"]
            mode = ALT4_MODE_TABLES[mode_name]
            anchors[feature_id] = mode["s1"] if wu2 else mode["s0"]
            continue
        s_value = {"q+u=1": qpu1, "q+u=-1": qpun1, "u=-1": un1}[rule.layer3_old_bit_name]
        layer3_mode_name = rule.mode_p1_name if exact_p else rule.mode_p0_name
        s0, s1 = LAYER3_SLICE_MODES[layer3_mode_name]
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


def _evaluate_with_anchors(
    pre_by_m: Mapping[int, Mapping[str, object]],
    *,
    anchors_fn,
    rule,
    m_values: Sequence[int],
) -> Dict[str, object]:
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
        anchors = anchors_fn(pre, rule)
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


def evaluate_stage_a_rule(pre_by_m: Mapping[int, Mapping[str, object]], rule: StageARule, *, m_values: Sequence[int]) -> Dict[str, object]:
    return _evaluate_with_anchors(pre_by_m, anchors_fn=_stage_a_anchor_by_feature, rule=rule, m_values=m_values)


def evaluate_stage_b_rule(pre_by_m: Mapping[int, Mapping[str, object]], rule: StageBRule, *, m_values: Sequence[int]) -> Dict[str, object]:
    return _evaluate_with_anchors(pre_by_m, anchors_fn=_stage_b_anchor_by_feature, rule=rule, m_values=m_values)


def stage_a_rules() -> Iterable[StageARule]:
    mode_names = tuple(ALT4_MODE_TABLES.keys())
    for mode_p0_name in mode_names:
        for mode_p1_name in mode_names:
            yield StageARule(mode_p0_name=mode_p0_name, mode_p1_name=mode_p1_name)


def stage_b_rules(stage: str) -> Iterable[StageBRule]:
    if stage == "stage_b1":
        layer2_mode_names = ("const_2/4", "const_4/2")
        old_bit_names = COUPLED_LAYER3_OLD_BITS_STAGE1
    elif stage == "stage_b2":
        layer2_mode_names = ("const_2/4", "const_4/2")
        old_bit_names = COUPLED_LAYER3_OLD_BITS_STAGE2
    elif stage == "stage_b3":
        layer2_mode_names = ("flip_p0", "flip_p1")
        old_bit_names = COUPLED_LAYER3_OLD_BITS_STAGE3
    else:
        raise ValueError(f"unknown stage {stage}")
    mode_names = tuple(LAYER3_SLICE_MODES.keys())
    for layer2_mode_name in layer2_mode_names:
        for layer3_old_bit_name in old_bit_names:
            for mode_p0_name in mode_names:
                for mode_p1_name in mode_names:
                    yield StageBRule(
                        stage=stage,
                        layer2_mode_name=layer2_mode_name,
                        layer3_old_bit_name=layer3_old_bit_name,
                        mode_p0_name=mode_p0_name,
                        mode_p1_name=mode_p1_name,
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
    path = validation_summary_json or Path("artifacts/d5_alt4_three_flag_geometry_013/data/validation_summary.json")
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


def extract_sigma2_summary(m_values: Sequence[int]) -> Dict[str, object]:
    layer_rows: Dict[str, object] = {}
    for layer in (2, 3):
        class_map: Dict[Tuple[int, ...], Dict[str, object]] = {}
        for m in m_values:
            for idx in range(m**DIM):
                coords = decode(idx, m)
                if sum(coords) % m != layer:
                    continue
                sig = exact_predecessor_signature(coords, 0, m)
                named_mask = simple_flag_mask(coords, 0, m)
                exact_p = int(sig[2])
                row = class_map.setdefault(
                    sig,
                    {
                        "signature": list(sig),
                        "named_mask": named_mask,
                        "named_active_flags": [name for bit, name in enumerate(NAMED_FLAG_NAMES) if (named_mask >> bit) & 1],
                        "exact_bit_value": exact_p,
                        "representatives": {},
                    },
                )
                row["representatives"].setdefault(str(m), list(coords))
        rows = sorted(class_map.values(), key=lambda row: (row["named_mask"], row["exact_bit_value"], tuple(row["signature"])))
        by_named_and_p: Dict[Tuple[int, int], Tuple[int, ...]] = {}
        exact_generated = True
        for row in rows:
            key = (int(row["named_mask"]), int(row["exact_bit_value"]))
            sig = tuple(int(v) for v in row["signature"])
            prev = by_named_and_p.get(key)
            if prev is None:
                by_named_and_p[key] = sig
            elif prev != sig:
                exact_generated = False
        split_rows = []
        grouped: Dict[int, List[Dict[str, object]]] = {}
        for row in rows:
            grouped.setdefault(int(row["named_mask"]), []).append(row)
        for named_mask, group in sorted(grouped.items()):
            if len(group) == 2:
                a = tuple(group[0]["signature"])
                b = tuple(group[1]["signature"])
                diff_positions = [index for index, (x, y) in enumerate(zip(a, b)) if x != y]
                split_rows.append(
                    {
                        "named_mask": named_mask,
                        "named_active_flags": group[0]["named_active_flags"],
                        "split_exact_bit_values": [int(group[0]["exact_bit_value"]), int(group[1]["exact_bit_value"])],
                        "diff_positions": diff_positions,
                        "class_rows": group,
                    }
                )
        layer_rows[str(layer)] = {
            "exact_class_count": len(rows),
            "named_cell_count": len(grouped),
            "exact_generated_by_named_plus_exact_bit": exact_generated,
            "class_rows": rows,
            "split_named_cells": split_rows,
        }
    return {
        "exact_bit_name": EXACT_BIT_NAME,
        "exact_bit_description": EXACT_BIT_DESCRIPTION,
        "pilot_m_values": list(m_values),
        "layers": layer_rows,
    }


def local_word_diagnostic(*, m_values: Sequence[int]) -> Dict[str, object]:
    def step(vertex: Tuple[int, ...], direction: int, m: int) -> Tuple[int, ...]:
        out = list(vertex)
        out[direction] = (out[direction] + 1) % m
        return tuple(out)

    def start_rows(m: int) -> Dict[Tuple[int, int], Tuple[int, ...]]:
        reps = {}
        for idx in range(m**DIM):
            coords = decode(idx, m)
            if sum(coords) % m != 2:
                continue
            sig = exact_predecessor_signature(coords, 0, m)
            reps.setdefault((simple_flag_mask(coords, 0, m), int(sig[2])), tuple(coords))
        return reps

    pre_by_m = {m: precompute_m(m) for m in m_values}
    out = {}
    for base_name in ("const_2/4", "const_4/2"):
        base_mode_name = LAYER2_MODE_TABLES[base_name]["p0_mode_name"]
        rule = StageARule(mode_p0_name=base_mode_name, mode_p1_name=base_mode_name)
        base_rows = {}
        for m in m_values:
            pre = pre_by_m[m]
            anchors = _stage_a_anchor_by_feature(pre, rule)
            reps = start_rows(m)
            split_rows = []
            for named_mask in (1, 5, 9):
                cell_rows = []
                for exact_p in (0, 1):
                    vertex = reps[(named_mask, exact_p)]
                    idx = encode(vertex, m)
                    word = []
                    cur = idx
                    for _ in range(3):
                        feature_id = pre["feature_ids_by_color"][0][cur]
                        direction = anchors[feature_id]
                        word.append(int(direction))
                        cur = pre["step_by_dir"][direction][cur]
                    end_vertex = decode(cur, m)
                    split_rows_value = {
                        "named_mask": named_mask,
                        "exact_bit_value": exact_p,
                        "representative": list(vertex),
                        "three_step_word": word,
                        "three_step_increment": [
                            (end_vertex[pos] - vertex[pos]) % m
                            for pos in range(DIM)
                        ],
                    }
                    cell_rows.append(split_rows_value)
                split_rows.append(
                    {
                        "named_mask": named_mask,
                        "exact_bit_changes_word": cell_rows[0]["three_step_word"] != cell_rows[1]["three_step_word"],
                        "exact_bit_changes_increment": cell_rows[0]["three_step_increment"] != cell_rows[1]["three_step_increment"],
                        "rows": cell_rows,
                    }
                )
            base_rows[str(m)] = {"split_rows": split_rows}
        out[base_name] = base_rows
    return out


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
