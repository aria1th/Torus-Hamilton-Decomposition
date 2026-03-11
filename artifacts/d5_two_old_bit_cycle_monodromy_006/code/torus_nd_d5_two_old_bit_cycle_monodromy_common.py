#!/usr/bin/env python3
"""Common evaluator for the d=5 two-old-bit cycle/monodromy search."""

from __future__ import annotations

import platform
import time
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from typing import Dict, List, Sequence, Tuple

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

TASK_ID = "D5-TWO-OLD-BIT-CYCLE-MONODROMY-006"
OLD_BIT_NAMES = ("q=-1", "q+u=1", "w+u=2", "q+u=-1", "u=-1")
OLD_BIT_SAFE_NAMES = {
    "q=-1": "q_eq_neg1",
    "q+u=1": "q_plus_u_eq_1",
    "w+u=2": "w_plus_u_eq_2",
    "q+u=-1": "q_plus_u_eq_neg1",
    "u=-1": "u_eq_neg1",
}
LAYER2_ALTERNATES = (0, 3, 4)
LAYER3_ALTERNATE = 0


@dataclass(frozen=True)
class Rule:
    layer2_bit_name: str
    layer3_bit_name: str
    layer2_alt: int
    layer2_s0_anchor: int
    layer2_s1_anchor: int
    layer3_s0_anchor: int
    layer3_s1_anchor: int

    def layer2_orientation(self) -> str:
        return f"{self.layer2_s0_anchor}/{self.layer2_s1_anchor}"

    def layer3_orientation(self) -> str:
        return f"{self.layer3_s0_anchor}/{self.layer3_s1_anchor}"

    def context_dependent(self) -> bool:
        return self.layer2_s0_anchor != self.layer2_s1_anchor or self.layer3_s0_anchor != self.layer3_s1_anchor

    def payload(self) -> Dict[str, object]:
        return {
            "layer2_bit_name": self.layer2_bit_name,
            "layer2_bit_safe_name": OLD_BIT_SAFE_NAMES[self.layer2_bit_name],
            "layer3_bit_name": self.layer3_bit_name,
            "layer3_bit_safe_name": OLD_BIT_SAFE_NAMES[self.layer3_bit_name],
            "layer2_alt": self.layer2_alt,
            "layer2_table": {"s0": self.layer2_s0_anchor, "s1": self.layer2_s1_anchor},
            "layer3_table": {"s0": self.layer3_s0_anchor, "s1": self.layer3_s1_anchor},
            "layer2_orientation": self.layer2_orientation(),
            "layer3_orientation": self.layer3_orientation(),
            "context_dependent": self.context_dependent(),
        }

    @classmethod
    def from_payload(cls, payload: Dict[str, object]) -> "Rule":
        return cls(
            layer2_bit_name=str(payload["layer2_bit_name"]),
            layer3_bit_name=str(payload["layer3_bit_name"]),
            layer2_alt=int(payload["layer2_alt"]),
            layer2_s0_anchor=int(payload["layer2_table"]["s0"]),
            layer2_s1_anchor=int(payload["layer2_table"]["s1"]),
            layer3_s0_anchor=int(payload["layer3_table"]["s0"]),
            layer3_s1_anchor=int(payload["layer3_table"]["s1"]),
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


def old_bit_value(old_bit_name: str, q: int, w: int, u: int, m: int) -> int:
    truths = atom_truths(q, w, u, m)
    index = OLD_BIT_NAMES.index(old_bit_name)
    return int(truths[index])


def _token_for(layer: object, s_bit: int) -> int:
    if layer == 0:
        return 0
    if layer == 1:
        return 1
    if layer == 2:
        return 2 + s_bit
    if layer == 3:
        return 4 + s_bit
    return 6


def precompute_m(m: int, layer2_bit_name: str, layer3_bit_name: str) -> Dict[str, object]:
    n = m**DIM
    coords = [decode(idx, m) for idx in range(n)]
    step_by_dir = [[0] * n for _ in range(DIM)]
    vertex_tokens_by_color = [[0] * n for _ in range(DIM)]
    for idx, vertex in enumerate(coords):
        total = sum(vertex) % m
        layer = layer_bucket(total)
        for direction in range(DIM):
            nxt = list(vertex)
            nxt[direction] = (nxt[direction] + 1) % m
            step_by_dir[direction][idx] = encode(nxt, m)
        for color in range(DIM):
            q = vertex[(color + 1) % DIM]
            w = vertex[(color + 2) % DIM]
            u = vertex[(color + 4) % DIM]
            if layer == 2:
                s_bit = old_bit_value(layer2_bit_name, q, w, u, m)
            elif layer == 3:
                s_bit = old_bit_value(layer3_bit_name, q, w, u, m)
            else:
                s_bit = 0
            vertex_tokens_by_color[color][idx] = _token_for(layer, s_bit)
    return {"m": m, "n": n, "coords": coords, "step_by_dir": step_by_dir, "vertex_tokens_by_color": vertex_tokens_by_color}


def nexts_all_for_rule(pre: Dict[str, object], rule: Rule) -> List[List[int]]:
    anchors = (
        1,
        4,
        rule.layer2_s0_anchor,
        rule.layer2_s1_anchor,
        rule.layer3_s0_anchor,
        rule.layer3_s1_anchor,
        0,
    )
    step_by_dir = pre["step_by_dir"]
    nexts = [[0] * pre["n"] for _ in range(DIM)]
    for color in range(DIM):
        color_dirs = tuple((anchor + color) % DIM for anchor in anchors)
        row = nexts[color]
        tokens = pre["vertex_tokens_by_color"][color]
        for idx, token in enumerate(tokens):
            row[idx] = step_by_dir[color_dirs[token]][idx]
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
        nexts_all = nexts_all_for_rule(pre, rule)
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
            "latin_all_colors": latin,
            "color0_return": ret,
            "classification": classification,
        }
        latin_all &= latin
        clean_all &= ret["clean_frame"]
        strict_all &= ret["strict_clock"]
        total_u_cycle_count += ret["U_cycle_count"]
        total_nonzero_monodromies += sum(1 for value in ret["monodromies"] if value != 0)
        if ret["U_cycle_lengths"]:
            max_cycle_length = max(max_cycle_length, max(ret["U_cycle_lengths"]))
        has_cycle |= classification["has_cycle"]
        has_monodromy |= classification["has_monodromy"]
    overall_kind = classify_return(
        {
            "U_cycle_lengths": [max_cycle_length] if has_cycle else [1],
            "monodromies": [1] if has_monodromy else [0],
        }
    )["kind"]
    return {
        "rule": rule.payload(),
        "per_m": per_m,
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
    return (
        not result["clean_all"],
        not result["strict_all"],
        kind_order[result["overall_kind"]],
        result["total_u_cycle_count"],
        -result["max_cycle_length"],
        -result["total_nonzero_monodromies"],
        result["rule"]["layer2_bit_name"],
        result["rule"]["layer3_bit_name"],
        result["rule"]["layer2_alt"],
        result["rule"]["layer2_orientation"],
        result["rule"]["layer3_orientation"],
    )


def parse_args_m_list(raw: str) -> List[int]:
    return parse_m_list(raw)
