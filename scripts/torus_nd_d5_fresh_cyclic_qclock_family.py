#!/usr/bin/env python3
"""Reduced-state helpers for the d=5 fresh cyclic q-clock / v-fiber family."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Iterable, List, Sequence, Tuple

TASK_ID = "D5-FRESH-CYCLIC-QCLOCK-VFIBER-001"
DIM = 5
PILOT_M_VALUES = (5, 7, 9)
STABILITY_M_VALUES = (11, 13)
LAYER_IDS = (1, 2, 3)
RESIDUE_LABELS = (0, 1, -1, 2, -2)
ATOM_TYPES = ("q", "w", "u", "q+w", "q+u", "w+u", "q+w+u")
OUTPUT_OFFSETS = (0, 2, 3, 4)
STRICT_CLOCK_SHIFT = 1

Clause = Tuple[str, int, int]
LayerSpec = Tuple[int, Tuple[Clause, ...]]
CandidateSpec = Tuple[LayerSpec, LayerSpec, LayerSpec]


@dataclass(frozen=True)
class ModulusContext:
    m: int
    state_q: Tuple[int, ...]
    state_w: Tuple[int, ...]
    state_u: Tuple[int, ...]
    q_plus: Tuple[int, ...]
    section_to_state: Tuple[int, ...]


def make_layer_spec(default_offset: int, clauses: Sequence[Clause]) -> LayerSpec:
    normalized = tuple((str(atom), int(label), int(offset)) for atom, label, offset in clauses)
    return (int(default_offset), normalized)


def make_candidate_spec(layer_specs: Sequence[LayerSpec]) -> CandidateSpec:
    if len(layer_specs) != 3:
        raise ValueError("Expected exactly three layer specifications")
    return tuple(layer_specs)  # type: ignore[return-value]


def default_candidate() -> CandidateSpec:
    return make_candidate_spec([make_layer_spec(0, ()) for _ in LAYER_IDS])


def resolve_residue(label: int, m: int) -> int:
    return label % m


def atom_value(atom_name: str, q: int, w: int, u: int, m: int) -> int:
    if atom_name == "q":
        return q
    if atom_name == "w":
        return w
    if atom_name == "u":
        return u
    if atom_name == "q+w":
        return (q + w) % m
    if atom_name == "q+u":
        return (q + u) % m
    if atom_name == "w+u":
        return (w + u) % m
    if atom_name == "q+w+u":
        return (q + w + u) % m
    raise ValueError(f"Unknown atom {atom_name}")


def clause_matches(clause: Clause, q: int, w: int, u: int, m: int) -> bool:
    atom_name, residue_label, _ = clause
    return atom_value(atom_name, q, w, u, m) == resolve_residue(residue_label, m)


def layer_output(layer_spec: LayerSpec, q: int, w: int, u: int, m: int) -> int:
    default_offset, clauses = layer_spec
    for clause in clauses:
        if clause_matches(clause, q, w, u, m):
            return clause[2]
    return default_offset


def encode_state(m: int, q: int, w: int, u: int) -> int:
    return (q * m + w) * m + u


def decode_state(m: int, idx: int) -> Tuple[int, int, int]:
    q, rem = divmod(idx, m * m)
    w, u = divmod(rem, m)
    return (q, w, u)


@lru_cache(maxsize=None)
def get_modulus_context(m: int) -> ModulusContext:
    state_q: List[int] = []
    state_w: List[int] = []
    state_u: List[int] = []
    q_plus: List[int] = []
    section_to_state: List[int] = []
    for q in range(m):
        for w in range(m):
            for u in range(m):
                state_q.append(q)
                state_w.append(w)
                state_u.append(u)
                q_plus.append(encode_state(m, (q + STRICT_CLOCK_SHIFT) % m, w, u))
    for w in range(m):
        for u in range(m):
            section_to_state.append(encode_state(m, 0, w, u))
    return ModulusContext(
        m=m,
        state_q=tuple(state_q),
        state_w=tuple(state_w),
        state_u=tuple(state_u),
        q_plus=tuple(q_plus),
        section_to_state=tuple(section_to_state),
    )


@lru_cache(maxsize=None)
def compile_layer_spec(layer_spec: LayerSpec, m: int) -> Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]]:
    ctx = get_modulus_context(m)
    next_idx: List[int] = []
    delta_v: List[int] = []
    outputs: List[int] = []
    for idx in range(m * m * m):
        q = ctx.state_q[idx]
        w = ctx.state_w[idx]
        u = ctx.state_u[idx]
        offset = layer_output(layer_spec, q, w, u, m)
        outputs.append(offset)
        if offset == 2:
            next_idx.append(encode_state(m, q, (w + 1) % m, u))
            delta_v.append(0)
        elif offset == 4:
            next_idx.append(encode_state(m, q, w, (u + 1) % m))
            delta_v.append(0)
        elif offset == 3:
            next_idx.append(idx)
            delta_v.append(1)
        else:
            next_idx.append(idx)
            delta_v.append(0)
    return (tuple(next_idx), tuple(delta_v), tuple(outputs))


def action_catalog_one_clause_default0() -> List[LayerSpec]:
    out = [make_layer_spec(0, ())]
    for atom_name in ATOM_TYPES:
        for residue_label in RESIDUE_LABELS:
            for output_offset in (2, 3, 4):
                out.append(make_layer_spec(0, ((atom_name, residue_label, output_offset),)))
    return out


def all_clauses() -> List[Clause]:
    out = []
    for atom_name in ATOM_TYPES:
        for residue_label in RESIDUE_LABELS:
            for output_offset in OUTPUT_OFFSETS:
                out.append((atom_name, residue_label, output_offset))
    return out


def serialize_candidate(spec: CandidateSpec) -> Dict[str, object]:
    layers = {}
    for layer, layer_spec in zip(LAYER_IDS, spec):
        layers[str(layer)] = {
            "default_offset": layer_spec[0],
            "clauses": [
                {"atom": atom_name, "residue_label": residue_label, "output_offset": output_offset}
                for atom_name, residue_label, output_offset in layer_spec[1]
            ],
        }
    return {
        "task_id": TASK_ID,
        "family": "d5_fresh_cyclic_qclock_vfiber_affine_atoms_v1",
        "layer0_offset": STRICT_CLOCK_SHIFT,
        "layers_ge_4_default_offset": 0,
        "layers": layers,
    }


def deserialize_candidate(payload: Dict[str, object]) -> CandidateSpec:
    layer_specs = []
    for layer in LAYER_IDS:
        layer_payload = payload["layers"][str(layer)]
        clauses = []
        for clause in layer_payload["clauses"]:
            clauses.append((clause["atom"], int(clause["residue_label"]), int(clause["output_offset"])))
        layer_specs.append(make_layer_spec(int(layer_payload["default_offset"]), clauses))
    return make_candidate_spec(layer_specs)


def clause_name(clause: Clause) -> str:
    atom_name, residue_label, output_offset = clause
    return f"{atom_name}={residue_label}->{output_offset}"


def layer_name(layer_spec: LayerSpec) -> str:
    default_offset, clauses = layer_spec
    if not clauses:
        return f"d{default_offset}"
    return f"d{default_offset}[" + ";".join(clause_name(clause) for clause in clauses) + "]"


def candidate_name(spec: CandidateSpec) -> str:
    return "|".join(f"L{layer}:{layer_name(layer_spec)}" for layer, layer_spec in zip(LAYER_IDS, spec))


def candidate_key(spec: CandidateSpec) -> str:
    return json.dumps(serialize_candidate(spec), sort_keys=True)


def total_clause_count(spec: CandidateSpec) -> int:
    return sum(len(layer_spec[1]) for layer_spec in spec)


def compose_first_return(spec: CandidateSpec, m: int) -> Tuple[List[int], List[int]]:
    ctx = get_modulus_context(m)
    compiled_layers = [compile_layer_spec(layer_spec, m) for layer_spec in spec]
    state_count = m * m * m
    r_next = [0] * state_count
    r_delta_v = [0] * state_count
    for idx in range(state_count):
        cur = ctx.q_plus[idx]
        dv = 0
        for next_idx, delta_v, _ in compiled_layers:
            dv = (dv + delta_v[cur]) % m
            cur = next_idx[cur]
        r_next[idx] = cur
        r_delta_v[idx] = dv
    return (r_next, r_delta_v)


def indegree_histogram(nexts: Sequence[int]) -> Dict[int, int]:
    indegrees = [0] * len(nexts)
    for nxt in nexts:
        indegrees[nxt] += 1
    histogram: Dict[int, int] = {}
    for indegree in indegrees:
        histogram[indegree] = histogram.get(indegree, 0) + 1
    return dict(sorted(histogram.items()))


def functional_graph_cycles(nexts: Sequence[int]) -> List[List[int]]:
    n = len(nexts)
    state = [0] * n
    cycles: List[List[int]] = []
    for start in range(n):
        if state[start] != 0:
            continue
        seen: Dict[int, int] = {}
        path: List[int] = []
        cur = start
        while state[cur] == 0 and cur not in seen:
            seen[cur] = len(path)
            path.append(cur)
            cur = nexts[cur]
        if state[cur] == 0 and cur in seen:
            cycle = path[seen[cur] :]
            cycles.append(cycle)
        for node in path:
            state[node] = 1
    return cycles


def section_return(r_next: Sequence[int], r_delta_v: Sequence[int], m: int) -> Tuple[List[int], List[int]]:
    ctx = get_modulus_context(m)
    u_next = [0] * (m * m)
    u_delta_v = [0] * (m * m)
    for section_idx, state_idx in enumerate(ctx.section_to_state):
        cur = state_idx
        total_dv = 0
        for _ in range(m):
            total_dv = (total_dv + r_delta_v[cur]) % m
            cur = r_next[cur]
        q, w, u = decode_state(m, cur)
        if q != 0:
            raise RuntimeError(f"Section return failed to land on q=0 for m={m}")
        u_next[section_idx] = w * m + u
        u_delta_v[section_idx] = total_dv
    return (u_next, u_delta_v)


def cycle_monodromies(cycles: Sequence[Sequence[int]], fiber_shift: Sequence[int], m: int) -> List[int]:
    out = []
    for cycle in cycles:
        total = 0
        for idx in cycle:
            total = (total + fiber_shift[idx]) % m
        out.append(total)
    return out


def is_unit(value: int, m: int) -> bool:
    return math.gcd(value, m) == 1


def first_failure_example(nexts: Sequence[int], histogram: Dict[int, int]) -> Dict[str, object] | None:
    if histogram == {1: len(nexts)}:
        return None
    indegrees = [0] * len(nexts)
    for nxt in nexts:
        indegrees[nxt] += 1
    for idx, indegree in enumerate(indegrees):
        if indegree != 1:
            return {"state_index": idx, "indegree": indegree, "next_state_index": nexts[idx]}
    return None


def analyze_candidate_for_modulus(spec: CandidateSpec, m: int) -> Dict[str, object]:
    r_next, r_delta_v = compose_first_return(spec, m)
    u_next, u_delta_v = section_return(r_next, r_delta_v, m)
    u_cycles = functional_graph_cycles(u_next)
    monodromies = cycle_monodromies(u_cycles, u_delta_v, m)
    indegree_hist = indegree_histogram(r_next)
    indegree_defect_states = sum(count for indegree, count in indegree_hist.items() if indegree != 1)
    indegree_l1 = sum(abs(indegree - 1) * count for indegree, count in indegree_hist.items())
    cycle_lengths = sorted(len(cycle) for cycle in u_cycles)
    return {
        "m": m,
        "clean_frame": True,
        "strict_clock": True,
        "clock_shift": STRICT_CLOCK_SHIFT,
        "v_fiber_clean": True,
        "U_cycle_count": len(u_cycles),
        "U_cycle_lengths": cycle_lengths,
        "U_is_single_cycle": len(u_cycles) == 1 and cycle_lengths == [m * m],
        "U_cycle_representatives": [cycle[0] for cycle in u_cycles[: min(12, len(u_cycles))]],
        "monodromies": monodromies,
        "all_monodromies_unit": all(is_unit(value, m) for value in monodromies),
        "unit_monodromy_cycle_count": sum(1 for value in monodromies if is_unit(value, m)),
        "R_indegree_histogram": indegree_hist,
        "R_is_permutation": indegree_hist == {1: m * m * m},
        "R_indegree_defect_states": indegree_defect_states,
        "R_indegree_l1": indegree_l1,
        "R_first_failure_example": first_failure_example(r_next, indegree_hist),
        "U_first_failure_example": None if len(u_cycles) == 1 and cycle_lengths == [m * m] else {"cycle_lengths": cycle_lengths[:12]},
    }


def objective_vector(per_m: Sequence[Dict[str, object]], spec: CandidateSpec) -> Tuple[int, int, int, int, int, int]:
    return (
        sum(1 for item in per_m if item["clean_frame"]),
        sum(1 for item in per_m if item["U_is_single_cycle"]),
        sum(1 for item in per_m if item["all_monodromies_unit"]),
        -sum(int(item["U_cycle_count"]) for item in per_m),
        -sum(int(item["R_indegree_defect_states"]) for item in per_m),
        -total_clause_count(spec),
    )


def dominates(lhs: Sequence[int], rhs: Sequence[int]) -> bool:
    return all(left >= right for left, right in zip(lhs, rhs)) and any(left > right for left, right in zip(lhs, rhs))


def pilot_summary(spec: CandidateSpec, m_values: Sequence[int]) -> Dict[str, object]:
    per_m = [analyze_candidate_for_modulus(spec, m) for m in m_values]
    return {
        "candidate_name": candidate_name(spec),
        "candidate": serialize_candidate(spec),
        "per_m": per_m,
        "objective": list(objective_vector(per_m, spec)),
    }


def relative_output_for_color(spec: CandidateSpec, layer: int, q: int, w: int, u: int, m: int) -> int:
    if layer == 0:
        return STRICT_CLOCK_SHIFT
    if layer >= 4:
        return 0
    return layer_output(spec[layer - 1], q, w, u, m)


def full_step_color(spec: CandidateSpec, color: int, coords: Sequence[int], m: int) -> Tuple[int, ...]:
    layer = sum(coords) % m
    q = coords[(color + 1) % DIM]
    w = coords[(color + 2) % DIM]
    u = coords[(color + 4) % DIM]
    offset = relative_output_for_color(spec, layer, q, w, u, m)
    direction = (color + offset) % DIM
    out = list(coords)
    out[direction] = (out[direction] + 1) % m
    return tuple(out)


def full_first_return_check(spec: CandidateSpec, m: int, colors: Iterable[int] = (0,)) -> Dict[str, object]:
    ctx = get_modulus_context(m)
    reduced_r_next, reduced_r_delta_v = compose_first_return(spec, m)
    for color in colors:
        for q in range(m):
            for w in range(m):
                for u in range(m):
                    reduced_state = encode_state(m, q, w, u)
                    for v in range(m):
                        coords = [0] * DIM
                        coords[color] = (-q - w - v - u) % m
                        coords[(color + 1) % DIM] = q
                        coords[(color + 2) % DIM] = w
                        coords[(color + 3) % DIM] = v
                        coords[(color + 4) % DIM] = u
                        cur = tuple(coords)
                        for _ in range(m):
                            cur = full_step_color(spec, color, cur, m)
                        q2 = cur[(color + 1) % DIM]
                        w2 = cur[(color + 2) % DIM]
                        v2 = cur[(color + 3) % DIM]
                        u2 = cur[(color + 4) % DIM]
                        target_idx = encode_state(m, q2, w2, u2)
                        if target_idx != reduced_r_next[reduced_state]:
                            return {
                                "ok": False,
                                "color": color,
                                "state": {"q": q, "w": w, "v": v, "u": u},
                                "expected_idx": reduced_r_next[reduced_state],
                                "actual_idx": target_idx,
                            }
                        if (v2 - v) % m != reduced_r_delta_v[reduced_state]:
                            return {
                                "ok": False,
                                "color": color,
                                "state": {"q": q, "w": w, "v": v, "u": u},
                                "expected_dv": reduced_r_delta_v[reduced_state],
                                "actual_dv": (v2 - v) % m,
                            }
    return {"ok": True, "checked_colors": list(colors)}
