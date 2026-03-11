#!/usr/bin/env python3
"""Common evaluator for the d=5 strict-palette context search."""

from __future__ import annotations

import platform
import time
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from typing import Dict, Iterable, List, Sequence, Tuple

TASK_ID = "D5-STRICT-PALETTE-CONTEXT-004"
DIM = 5
STRICT_ALTERNATES = (0, 2, 3, 4)
CONTEXT_NAMES = ("phase_align", "00", "01", "10", "11")
B1_LOOKUP = {
    5: frozenset((1, 2)),
    7: frozenset((1, 3, 5)),
    9: frozenset((1, 2, 5, 6)),
}
B2_LOOKUP = {
    5: frozenset((1, 3)),
    7: frozenset((1, 2, 4)),
    9: frozenset((1, 3, 5, 7)),
}


@dataclass(frozen=True)
class Rule:
    layer2_alt: int
    layer3_alt: int
    layer2_bits: Tuple[int, int, int, int, int]
    layer3_bits: Tuple[int, int, int, int, int]

    def layer2_anchors(self) -> Tuple[int, int, int, int, int]:
        return tuple(self.layer2_alt if bit else 2 for bit in self.layer2_bits)

    def layer3_anchors(self) -> Tuple[int, int, int, int, int]:
        return tuple(self.layer3_alt if bit else 3 for bit in self.layer3_bits)

    def selected_anchors_by_token(self) -> Tuple[int, ...]:
        return (1, 4) + self.layer2_anchors() + self.layer3_anchors() + (0,)

    def effective_key(self) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        return (self.layer2_anchors(), self.layer3_anchors())

    def is_context_dependent(self) -> bool:
        layer2 = self.layer2_anchors()
        layer3 = self.layer3_anchors()
        return len(set(layer2)) > 1 or len(set(layer3)) > 1

    def payload(self) -> Dict[str, object]:
        layer2_anchors = self.layer2_anchors()
        layer3_anchors = self.layer3_anchors()
        return {
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
            layer2_alt=int(payload["layer2_alt"]),
            layer3_alt=int(payload["layer3_alt"]),
            layer2_bits=tuple(int(value) for value in payload["layer2_bits"]),
            layer3_bits=tuple(int(value) for value in payload["layer3_bits"]),
        )


def rich_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def encode(coords: Sequence[int], m: int) -> int:
    out = 0
    for value in coords:
        out = out * m + value
    return out


def decode(idx: int, m: int) -> Tuple[int, ...]:
    coords = [0] * DIM
    for pos in range(DIM - 1, -1, -1):
        idx, coords[pos] = divmod(idx, m)
    return tuple(coords)


def layer_bucket(layer: int) -> object:
    return "4+" if layer >= 4 else layer


def ctx_index(delta: int, m: int) -> int:
    if m not in B1_LOOKUP or m not in B2_LOOKUP:
        raise ValueError(f"tail-bit lookups are only defined for m in {sorted(B1_LOOKUP)}; received m={m}")
    b1 = int(delta in B1_LOOKUP[m])
    b2 = int(delta in B2_LOOKUP[m])
    return b1 * 2 + b2


def context_index(delta: int, m: int) -> int:
    return 0 if delta == 0 else 1 + ctx_index(delta, m)


def token_for(layer: object, ctx: int) -> int:
    if layer == 0:
        return 0
    if layer == 1:
        return 1
    if layer == 2:
        return 2 + ctx
    if layer == 3:
        return 7 + ctx
    return 12


def iter_raw_rules_for_family(layer2_alt: int, layer3_alt: int) -> Iterable[Rule]:
    for mask2 in range(32):
        layer2_bits = tuple((mask2 >> idx) & 1 for idx in range(5))
        for mask3 in range(32):
            layer3_bits = tuple((mask3 >> idx) & 1 for idx in range(5))
            yield Rule(
                layer2_alt=layer2_alt,
                layer3_alt=layer3_alt,
                layer2_bits=layer2_bits,
                layer3_bits=layer3_bits,
            )


def unique_rules_for_family(layer2_alt: int, layer3_alt: int) -> Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], Dict[str, object]]:
    unique: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], Dict[str, object]] = {}
    for rule in iter_raw_rules_for_family(layer2_alt, layer3_alt):
        key = rule.effective_key()
        entry = unique.get(key)
        if entry is None:
            unique[key] = {"rule": rule, "raw_multiplicity": 1}
        else:
            entry["raw_multiplicity"] += 1
    return unique


def precompute_m(m: int) -> Dict[str, object]:
    n = m**DIM
    coords = [decode(idx, m) for idx in range(n)]
    step_by_dir = [[0] * n for _ in range(DIM)]
    vertex_tokens_by_color = [[0] * n for _ in range(DIM)]
    vertex_tokens0 = [0] * n
    for idx, vertex in enumerate(coords):
        total = sum(vertex) % m
        layer = layer_bucket(total)
        for direction in range(DIM):
            nxt = list(vertex)
            nxt[direction] = (nxt[direction] + 1) % m
            step_by_dir[direction][idx] = encode(nxt, m)
        for color in range(DIM):
            q = vertex[(color + 1) % DIM]
            v = vertex[(color + 3) % DIM]
            delta = (v - q) % m
            token = token_for(layer, context_index(delta, m))
            vertex_tokens_by_color[color][idx] = token
            if color == 0:
                vertex_tokens0[idx] = token

    latin_patterns: List[Tuple[int, int, int, int, int]] = []
    for total in range(m):
        prev_total = (total - 1) % m
        prev_layer = layer_bucket(prev_total)
        for delta in range(m):
            tokens = []
            for direction in range(DIM):
                if direction == 1:
                    prev_delta = (delta + 1) % m
                elif direction == 3:
                    prev_delta = (delta - 1) % m
                else:
                    prev_delta = delta
                tokens.append(token_for(prev_layer, context_index(prev_delta, m)))
            latin_patterns.append(tuple(tokens))  # type: ignore[arg-type]

    return {
        "m": m,
        "n": n,
        "coords": coords,
        "step_by_dir": step_by_dir,
        "vertex_tokens0": vertex_tokens0,
        "vertex_tokens_by_color": vertex_tokens_by_color,
        "latin_patterns": latin_patterns,
    }


def color0_is_latin(pre: Dict[str, object], rule: Rule) -> bool:
    anchors = rule.selected_anchors_by_token()
    for token0, token1, token2, token3, token4 in pre["latin_patterns"]:
        indegree = int(anchors[token0] == 0)
        indegree += int(anchors[token1] == 1)
        indegree += int(anchors[token2] == 2)
        indegree += int(anchors[token3] == 3)
        indegree += int(anchors[token4] == 4)
        if indegree != 1:
            return False
    return True


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


def incoming_latin_all(nexts: List[List[int]]) -> bool:
    n = len(nexts[0])
    for color in range(DIM):
        indegree = [0] * n
        for nxt in nexts[color]:
            indegree[nxt] += 1
        if any(value != 1 for value in indegree):
            return False
    return True


def first_return(pre: Dict[str, object], nexts0: List[int]) -> Dict[str, object]:
    m = pre["m"]
    coords = pre["coords"]

    groups = {}
    for q in range(m):
        for w in range(m):
            for u in range(m):
                images = []
                for v in range(m):
                    idx = encode(((-q - w - v - u) % m, q, w, v, u), m)
                    cur = idx
                    for _ in range(m):
                        cur = nexts0[cur]
                    c = coords[cur]
                    q2, w2, v2, u2 = c[1], c[2], c[3], c[4]
                    images.append(((q2, w2, u2), (v2 - v) % m))
                groups[(q, w, u)] = images

    clean_frame = True
    r_next = {}
    r_dv = {}
    for key, images in groups.items():
        image_set = {item[0] for item in images}
        dv_set = {item[1] for item in images}
        if len(image_set) != 1 or len(dv_set) != 1:
            clean_frame = False
            break
        r_next[key] = next(iter(image_set))
        r_dv[key] = next(iter(dv_set))

    strict_clock = clean_frame and all(((image[0] - key[0]) % m) == 1 for key, image in r_next.items())
    if not clean_frame:
        return {
            "clean_frame": False,
            "strict_clock": False,
            "U_cycle_count": 0,
            "U_cycle_lengths": [],
            "monodromies": [],
            "nontrivial_u": False,
        }

    u_map = {}
    u_dv = {}
    for w in range(m):
        for u in range(m):
            cur = (0, w, u)
            total = 0
            for _ in range(m):
                total = (total + r_dv[cur]) % m
                cur = r_next[cur]
            u_map[(w, u)] = (cur[1], cur[2])
            u_dv[(w, u)] = total

    idx_map = {(w, u): w * m + u for w in range(m) for u in range(m)}
    u_nexts = [idx_map[u_map[(w, u)]] for w in range(m) for u in range(m)]
    visited = [0] * len(u_nexts)
    cycles = []
    for start in range(len(u_nexts)):
        if visited[start]:
            continue
        seen = {}
        path = []
        cur = start
        while not visited[cur] and cur not in seen:
            seen[cur] = len(path)
            path.append(cur)
            cur = u_nexts[cur]
        if not visited[cur] and cur in seen:
            cycles.append(path[seen[cur] :])
        for node in path:
            visited[node] = 1

    monodromies = []
    for cycle in cycles:
        total = 0
        for idx in cycle:
            w, u = divmod(idx, m)
            total = (total + u_dv[(w, u)]) % m
        monodromies.append(total)

    cycle_lengths = sorted(len(cycle) for cycle in cycles)
    nontrivial_u = len(cycles) < m * m or any(length > 1 for length in cycle_lengths) or any(value != 0 for value in monodromies)
    return {
        "clean_frame": True,
        "strict_clock": strict_clock,
        "U_cycle_count": len(cycles),
        "U_cycle_lengths": cycle_lengths,
        "monodromies": monodromies,
        "nontrivial_u": nontrivial_u,
    }


def search_rank_key(result: Dict[str, object]) -> Tuple[object, ...]:
    return (
        not result["any_nontrivial_u"],
        not result["strict_all"],
        not result["rule"]["context_dependent"],
        result["total_u_cycle_count"],
        -result["total_nonzero_monodromies"],
        result["rule"]["layer2_table"]["phase_align"],
        result["rule"]["layer3_table"]["phase_align"],
        tuple(result["rule"]["layer2_bits"]),
        tuple(result["rule"]["layer3_bits"]),
    )


def strict_rank_key(result: Dict[str, object]) -> Tuple[object, ...]:
    return (
        not result["any_nontrivial_u"],
        not result["rule"]["context_dependent"],
        result["total_u_cycle_count"],
        -result["total_nonzero_monodromies"],
        result["rule"]["layer2_table"]["phase_align"],
        result["rule"]["layer3_table"]["phase_align"],
        tuple(result["rule"]["layer2_bits"]),
        tuple(result["rule"]["layer3_bits"]),
    )


def evaluate_rule_search(pre_by_m: Dict[int, Dict[str, object]], rule: Rule, *, m_values: Sequence[int]) -> Dict[str, object]:
    per_m: Dict[str, object] = {}
    latin_all = True
    clean_all = True
    strict_all = True
    total_u_cycles = 0
    total_nonzero_monodromies = 0
    any_nontrivial_u = False
    compute_returns = True
    for m in m_values:
        pre = pre_by_m[m]
        latin = color0_is_latin(pre, rule)
        if not latin:
            per_m[str(m)] = {"latin_color0": False}
            latin_all = False
            clean_all = False
            strict_all = False
            break
        if compute_returns:
            nexts0 = nexts0_for_rule(pre, rule)
            ret = first_return(pre, nexts0)
            per_m[str(m)] = {"latin_color0": True, "color0_return": ret}
            clean_all &= ret["clean_frame"]
            strict_all &= ret["strict_clock"]
            total_u_cycles += ret["U_cycle_count"]
            total_nonzero_monodromies += sum(1 for value in ret["monodromies"] if value != 0)
            any_nontrivial_u |= ret["nontrivial_u"]
            if not ret["clean_frame"]:
                compute_returns = False
        else:
            per_m[str(m)] = {"latin_color0": True}
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


def environment_block() -> Dict[str, object]:
    return {"python_version": platform.python_version(), "rich_version": rich_version()}


def runtime_since(start: float) -> float:
    return time.perf_counter() - start
