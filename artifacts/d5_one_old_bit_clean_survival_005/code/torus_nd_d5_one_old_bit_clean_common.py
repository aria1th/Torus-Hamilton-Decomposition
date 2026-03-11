#!/usr/bin/env python3
"""Common evaluator for the d=5 one-old-bit clean-survival search."""

from __future__ import annotations

import platform
import time
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

from torus_nd_d5_master_field_quotient_family import atom_truths
from torus_nd_d5_strict_palette_context_common import (
    B1_LOOKUP,
    B2_LOOKUP,
    DIM,
    STRICT_ALTERNATES,
    encode,
    decode,
    first_return,
    incoming_latin_all,
    layer_bucket,
    parse_m_list,
)

TASK_ID = "D5-ONE-OLD-BIT-CLEAN-SURVIVAL-005"
OLD_BIT_NAMES = ("q=-1", "q+u=1", "w+u=2", "q+u=-1", "u=-1")
OLD_BIT_SAFE_NAMES = {
    "q=-1": "q_eq_neg1",
    "q+u=1": "q_plus_u_eq_1",
    "w+u=2": "w_plus_u_eq_2",
    "q+u=-1": "q_plus_u_eq_neg1",
    "u=-1": "u_eq_neg1",
}
CONTEXT_NAMES = (
    "align_s0",
    "align_s1",
    "00_s0",
    "00_s1",
    "01_s0",
    "01_s1",
    "10_s0",
    "10_s1",
    "11_s0",
    "11_s1",
)


@dataclass(frozen=True)
class Rule:
    old_bit_name: str
    layer2_alt: int
    layer3_alt: int
    layer2_bits: Tuple[int, ...]
    layer3_bits: Tuple[int, ...]

    def layer2_anchors(self) -> Tuple[int, ...]:
        return tuple(self.layer2_alt if bit else 2 for bit in self.layer2_bits)

    def layer3_anchors(self) -> Tuple[int, ...]:
        return tuple(self.layer3_alt if bit else 3 for bit in self.layer3_bits)

    def selected_anchors_by_token(self) -> Tuple[int, ...]:
        return (1, 4) + self.layer2_anchors() + self.layer3_anchors() + (0,)

    def effective_key(self) -> Tuple[str, Tuple[int, ...], Tuple[int, ...]]:
        return (self.old_bit_name, self.layer2_anchors(), self.layer3_anchors())

    def is_context_dependent(self) -> bool:
        return len(set(self.layer2_anchors())) > 1 or len(set(self.layer3_anchors())) > 1

    def payload(self) -> Dict[str, object]:
        layer2_anchors = self.layer2_anchors()
        layer3_anchors = self.layer3_anchors()
        return {
            "old_bit_name": self.old_bit_name,
            "old_bit_safe_name": OLD_BIT_SAFE_NAMES[self.old_bit_name],
            "layer2_alt": self.layer2_alt,
            "layer3_alt": self.layer3_alt,
            "layer2_bits": list(self.layer2_bits),
            "layer3_bits": list(self.layer3_bits),
            "layer2_table": {name: layer2_anchors[idx] for idx, name in enumerate(CONTEXT_NAMES)},
            "layer3_table": {name: layer3_anchors[idx] for idx, name in enumerate(CONTEXT_NAMES)},
            "context_dependent": self.is_context_dependent(),
            "effective_key": {
                "layer2_anchors": list(layer2_anchors),
                "layer3_anchors": list(layer3_anchors),
            },
        }

    @classmethod
    def from_payload(cls, payload: Dict[str, object]) -> "Rule":
        return cls(
            old_bit_name=str(payload["old_bit_name"]),
            layer2_alt=int(payload["layer2_alt"]),
            layer3_alt=int(payload["layer3_alt"]),
            layer2_bits=tuple(int(value) for value in payload["layer2_bits"]),
            layer3_bits=tuple(int(value) for value in payload["layer3_bits"]),
        )

    @classmethod
    def from_anchor_tables(
        cls,
        *,
        old_bit_name: str,
        layer2_alt: int,
        layer3_alt: int,
        layer2_table: Sequence[int],
        layer3_table: Sequence[int],
    ) -> "Rule":
        return cls(
            old_bit_name=old_bit_name,
            layer2_alt=layer2_alt,
            layer3_alt=layer3_alt,
            layer2_bits=tuple(int(value == layer2_alt and layer2_alt != 2) for value in layer2_table),
            layer3_bits=tuple(int(value == layer3_alt and layer3_alt != 3) for value in layer3_table),
        )


def rich_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def environment_block() -> Dict[str, object]:
    return {"python_version": platform.python_version(), "rich_version": rich_version(), "numpy_version": np.__version__}


def runtime_since(start: float) -> float:
    return time.perf_counter() - start


def ctx_index(delta: int, m: int) -> int:
    if m not in B1_LOOKUP or m not in B2_LOOKUP:
        raise ValueError(f"pilot tail-bit lookups are only defined for m in {sorted(B1_LOOKUP)}; received m={m}")
    b1 = int(delta in B1_LOOKUP[m])
    b2 = int(delta in B2_LOOKUP[m])
    return b1 * 2 + b2


def old_bit_value(old_bit_name: str, q: int, w: int, u: int, m: int) -> int:
    truths = atom_truths(q, w, u, m)
    index = OLD_BIT_NAMES.index(old_bit_name)
    return int(truths[index])


def context_index(delta: int, s_bit: int, m: int) -> int:
    if delta == 0:
        return s_bit
    return 2 + 2 * ctx_index(delta, m) + s_bit


def token_for(layer: object, ctx: int) -> int:
    if layer == 0:
        return 0
    if layer == 1:
        return 1
    if layer == 2:
        return 2 + ctx
    if layer == 3:
        return 12 + ctx
    return 22


def unique_layer_tables(seed_anchor: int, alt_anchor: int) -> List[Dict[str, object]]:
    if alt_anchor == seed_anchor:
        return [
            {
                "bits": tuple(0 for _ in CONTEXT_NAMES),
                "anchors": tuple(seed_anchor for _ in CONTEXT_NAMES),
                "raw_multiplicity": 1 << len(CONTEXT_NAMES),
            }
        ]
    rows = []
    for mask in range(1 << len(CONTEXT_NAMES)):
        bits = tuple((mask >> idx) & 1 for idx in range(len(CONTEXT_NAMES)))
        rows.append(
            {
                "bits": bits,
                "anchors": tuple(alt_anchor if bit else seed_anchor for bit in bits),
                "raw_multiplicity": 1,
            }
        )
    return rows


def _pattern_array(patterns: List[Tuple[int, ...]]) -> np.ndarray:
    return np.array(patterns, dtype=np.uint8)


def precompute_m(m: int, old_bit_name: str) -> Dict[str, object]:
    n = m**DIM
    coords = [decode(idx, m) for idx in range(n)]
    step_by_dir = [[0] * n for _ in range(DIM)]
    vertex_tokens_by_color = [[0] * n for _ in range(DIM)]
    vertex_tokens0 = [0] * n
    layer2_patterns: List[Tuple[int, int, int, int, int]] = []
    layer3_patterns: List[Tuple[int, int, int, int, int]] = []

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
            v = vertex[(color + 3) % DIM]
            u = vertex[(color + 4) % DIM]
            delta = (v - q) % m
            s_bit = old_bit_value(old_bit_name, q, w, u, m)
            token = token_for(layer, context_index(delta, s_bit, m))
            vertex_tokens_by_color[color][idx] = token
            if color == 0:
                vertex_tokens0[idx] = token

        if total in (3, 4):
            patterns = []
            for direction in range(DIM):
                pred = list(vertex)
                pred[direction] = (pred[direction] - 1) % m
                q = pred[1]
                w = pred[2]
                v = pred[3]
                u = pred[4]
                delta = (v - q) % m
                s_bit = old_bit_value(old_bit_name, q, w, u, m)
                patterns.append(context_index(delta, s_bit, m))
            if total == 3:
                layer2_patterns.append(tuple(patterns))
            else:
                layer3_patterns.append(tuple(patterns))

    return {
        "m": m,
        "n": n,
        "coords": coords,
        "step_by_dir": step_by_dir,
        "vertex_tokens0": vertex_tokens0,
        "vertex_tokens_by_color": vertex_tokens_by_color,
        "layer2_patterns": _pattern_array(layer2_patterns),
        "layer3_patterns": _pattern_array(layer3_patterns),
    }


def layer_table_is_latin(patterns: np.ndarray, anchors: Sequence[int]) -> bool:
    if patterns.size == 0:
        return True
    indegree = np.zeros(patterns.shape[0], dtype=np.int8)
    anchor_array = np.fromiter(anchors, dtype=np.uint8, count=len(CONTEXT_NAMES))
    for direction in range(DIM):
        indegree += (anchor_array[patterns[:, direction]] == direction)
    return bool(np.all(indegree == 1))


def latin_surviving_layer_tables(
    pre_by_m: Dict[int, Dict[str, object]],
    *,
    active_layer: int,
    alt_anchor: int,
    m_values: Sequence[int],
) -> List[Dict[str, object]]:
    seed_anchor = 2 if active_layer == 2 else 3
    rows = unique_layer_tables(seed_anchor, alt_anchor)
    if alt_anchor == seed_anchor:
        return rows
    tables = np.array([row["anchors"] for row in rows], dtype=np.uint8)
    alive = np.ones(len(rows), dtype=bool)
    for m in m_values:
        patterns = pre_by_m[m][f"layer{active_layer}_patterns"]
        if patterns.size == 0:
            continue
        indegree = np.zeros((tables.shape[0], patterns.shape[0]), dtype=np.int8)
        for direction in range(DIM):
            indegree += (tables[:, patterns[:, direction]] == direction)
        alive &= np.all(indegree == 1, axis=1)
        if not np.any(alive):
            break
        tables = tables[alive]
        rows = [row for keep, row in zip(alive.tolist(), rows) if keep]
        alive = np.ones(len(rows), dtype=bool)
    return rows


def nexts0_for_rule(pre: Dict[str, object], rule: Rule) -> List[int]:
    anchors = rule.selected_anchors_by_token()
    step_by_dir = pre["step_by_dir"]
    nexts = [0] * pre["n"]
    for idx, token in enumerate(pre["vertex_tokens0"]):
        nexts[idx] = step_by_dir[anchors[token]][idx]
    return nexts


def nexts_all_for_rule(pre: Dict[str, object], rule: Rule) -> List[List[int]]:
    anchors = rule.selected_anchors_by_token()
    step_by_dir = pre["step_by_dir"]
    nexts = [[0] * pre["n"] for _ in range(DIM)]
    for color in range(DIM):
        color_dirs = tuple((anchor + color) % DIM for anchor in anchors)
        row = nexts[color]
        tokens = pre["vertex_tokens_by_color"][color]
        for idx, token in enumerate(tokens):
            row[idx] = step_by_dir[color_dirs[token]][idx]
    return nexts


def evaluate_rule_from_known_latin(
    pre_by_m: Dict[int, Dict[str, object]],
    rule: Rule,
    *,
    m_values: Sequence[int],
) -> Dict[str, object]:
    per_m: Dict[str, object] = {}
    clean_all = True
    strict_all = True
    total_u_cycles = 0
    total_nonzero_monodromies = 0
    any_nontrivial_u = False
    for m in m_values:
        pre = pre_by_m[m]
        ret = first_return(pre, nexts0_for_rule(pre, rule))
        per_m[str(m)] = {"color0_return": ret}
        clean_all &= ret["clean_frame"]
        strict_all &= ret["strict_clock"]
        total_u_cycles += ret["U_cycle_count"]
        total_nonzero_monodromies += sum(1 for value in ret["monodromies"] if value != 0)
        any_nontrivial_u |= ret["nontrivial_u"]
        if not ret["clean_frame"]:
            break
    return {
        "rule": rule.payload(),
        "per_m": per_m,
        "latin_all": True,
        "clean_all": clean_all,
        "strict_all": strict_all,
        "total_u_cycle_count": total_u_cycles,
        "total_nonzero_monodromies": total_nonzero_monodromies,
        "any_nontrivial_u": any_nontrivial_u,
    }


def evaluate_rule_validation(
    pre_by_m: Dict[int, Dict[str, object]],
    rule: Rule,
    *,
    m_values: Sequence[int],
) -> Dict[str, object]:
    per_m: Dict[str, object] = {}
    latin_all = True
    clean_all = True
    strict_all = True
    total_u_cycles = 0
    total_nonzero_monodromies = 0
    any_nontrivial_u = False
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
        per_m[str(m)] = {"latin_all_colors": latin, "color0_return": ret}
        latin_all &= latin
        clean_all &= ret["clean_frame"]
        strict_all &= ret["strict_clock"]
        total_u_cycles += ret["U_cycle_count"]
        total_nonzero_monodromies += sum(1 for value in ret["monodromies"] if value != 0)
        any_nontrivial_u |= ret["nontrivial_u"]
    return {
        "rule": rule.payload(),
        "per_m": per_m,
        "latin_all": latin_all,
        "clean_all": clean_all,
        "strict_all": strict_all,
        "total_u_cycle_count": total_u_cycles,
        "total_nonzero_monodromies": total_nonzero_monodromies,
        "any_nontrivial_u": any_nontrivial_u,
    }


def result_rank_key(result: Dict[str, object]) -> Tuple[object, ...]:
    return (
        not result["any_nontrivial_u"],
        not result["strict_all"],
        not result["rule"]["context_dependent"],
        result["total_u_cycle_count"],
        -result["total_nonzero_monodromies"],
        result["rule"]["old_bit_name"],
        result["rule"]["layer2_alt"],
        result["rule"]["layer3_alt"],
        tuple(result["rule"]["layer2_bits"]),
        tuple(result["rule"]["layer3_bits"]),
    )


def strict_rank_key(result: Dict[str, object]) -> Tuple[object, ...]:
    return (
        not result["any_nontrivial_u"],
        not result["rule"]["context_dependent"],
        result["total_u_cycle_count"],
        -result["total_nonzero_monodromies"],
        result["rule"]["old_bit_name"],
        result["rule"]["layer2_alt"],
        result["rule"]["layer3_alt"],
        tuple(result["rule"]["layer2_bits"]),
        tuple(result["rule"]["layer3_bits"]),
    )


def parse_args_m_list(raw: str) -> List[int]:
    return parse_m_list(raw)
