#!/usr/bin/env python3
"""Schema helpers for d=5 master-field quotient searches."""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Iterable, List, Sequence, Tuple

DIM = 5
TASK_ID = "D5-MASTER-FIELD-QUOTIENT-001"
PILOT_M_VALUES = (5, 7, 9)
STABILITY_M_VALUES = (11, 13)
LAYER_BUCKETS = (0, 1, 2, 3, "4+")

State = Tuple[object, Tuple[int, int, int, int, int]]


@dataclass(frozen=True)
class SchemaSpec:
    name: str
    description: str
    atom_names: Tuple[str, ...]
    include_phase_align: bool = False


SCHEMA_A = SchemaSpec(
    name="stable_anchor_two_atom",
    description="Single-cycle / zero-monodromy anchor from the fresh q-clock search",
    atom_names=("q=-1", "q+u=1"),
)

SCHEMA_B = SchemaSpec(
    name="unit_anchor_three_atom",
    description="Unit-monodromy / fractured-U anchor from the fresh q-clock search",
    atom_names=("w+u=2", "q+u=-1", "u=-1"),
)

SCHEMA_JOIN = SchemaSpec(
    name="joined_anchor_five_atom",
    description="Joined Theta_AB quotient carrying the informative atoms from Schema A and Schema B",
    atom_names=("q=-1", "q+u=1", "w+u=2", "q+u=-1", "u=-1"),
)

SCHEMA_PHASE_ALIGN = SchemaSpec(
    name="joined_anchor_five_atom_phase_align",
    description="Refined Theta_AB quotient with the extra phase_align bit phase_align_c=1_{x_{c+3}-x_{c+1}=0}",
    atom_names=("q=-1", "q+u=1", "w+u=2", "q+u=-1", "u=-1"),
    include_phase_align=True,
)

SCHEMA_BY_NAME = {schema.name: schema for schema in (SCHEMA_A, SCHEMA_B, SCHEMA_JOIN, SCHEMA_PHASE_ALIGN)}

ATOM_INDEX = {
    "q=-1": 0,
    "q+u=1": 1,
    "w+u=2": 2,
    "q+u=-1": 3,
    "u=-1": 4,
}


def layer_bucket(layer: int) -> object:
    return "4+" if layer >= 4 else layer


def rotate_tuple(values: Sequence[int], shift: int) -> Tuple[int, ...]:
    shift %= DIM
    if shift == 0:
        return tuple(values)
    return tuple(values[shift:] + values[:shift])


def rotate_state(state: State, shift: int) -> State:
    return (state[0], rotate_tuple(list(state[1]), shift))


def state_to_id_map(states: Sequence[State]) -> Dict[State, int]:
    return {state: idx for idx, state in enumerate(states)}


def color_relative_coordinates(coords: Sequence[int], color: int) -> Tuple[int, int, int]:
    q = coords[(color + 1) % DIM]
    w = coords[(color + 2) % DIM]
    u = coords[(color + 4) % DIM]
    return (q, w, u)


def atom_truths(q: int, w: int, u: int, m: int) -> Tuple[bool, bool, bool, bool, bool]:
    return (
        q == (m - 1),
        (q + u) % m == 1,
        (w + u) % m == 2,
        (q + u) % m == (m - 1),
        u == (m - 1),
    )


def phase_align_value(coords: Sequence[int], color: int, m: int) -> int:
    q = coords[(color + 1) % DIM]
    v = coords[(color + 3) % DIM]
    return int((v - q) % m == 0)


def signature_value(schema: SchemaSpec, q: int, w: int, u: int, m: int, *, phase_align: int = 0) -> int:
    truths = atom_truths(q, w, u, m)
    value = 0
    for bit, atom_name in enumerate(schema.atom_names):
        if truths[ATOM_INDEX[atom_name]]:
            value |= 1 << bit
    if schema.include_phase_align and phase_align:
        value |= 1 << len(schema.atom_names)
    return value


def state_for_vertex(coords: Sequence[int], m: int, schema: SchemaSpec) -> State:
    layer = layer_bucket(sum(coords) % m)
    signature = tuple(
        signature_value(
            schema,
            *color_relative_coordinates(coords, color),
            m,
            phase_align=phase_align_value(coords, color, m),
        )
        for color in range(DIM)
    )
    return (layer, signature)


def required_color0_output(state: State, schema: SchemaSpec) -> int:
    layer, signature = state
    sig0 = signature[0]
    return required_output_for_signature(layer, sig0, schema)


def required_output_for_signature(layer_bucket_value: object, signature_value_code: int, schema: SchemaSpec) -> int:
    layer = layer_bucket_value
    sig0 = signature_value_code
    if layer == 0:
        return 1
    if layer == 1:
        return 3 if schema.name == SCHEMA_A.name else 4
    if layer == 2:
        if schema.name == SCHEMA_A.name:
            if sig0 & 1:
                return 4
            if sig0 & 2:
                return 0
            return 2
        if sig0 & 1:
            return 4
        if sig0 & 2:
            return 3
        return 2
    if layer == 3:
        if schema.name == SCHEMA_A.name:
            return 4
        if sig0 & 4:
            return 3
        return 0
    return 0


def serialize_state(state: State) -> Dict[str, object]:
    return {"layer_bucket": state[0], "signature": list(state[1])}


def state_name(state: State) -> str:
    return f"L={state[0]}|sig={''.join(str(v) for v in state[1])}"


def permutation_name(perm: Sequence[int]) -> str:
    return "".join(str(value) for value in perm)


def preferred_anchor_value(state: State) -> int | None:
    if state[0] == 0:
        return 1
    if state[0] == "4+":
        return 0
    return None


def rotation_orbits(states: Sequence[State]) -> Tuple[Tuple[int, ...], ...]:
    state_map = state_to_id_map(states)
    visited = set()
    orbits = []
    for state_id, state in enumerate(states):
        if state_id in visited:
            continue
        orbit = tuple(sorted({state_map[rotate_state(state, shift)] for shift in range(DIM)}))
        visited.update(orbit)
        orbits.append(orbit)
    return tuple(sorted(orbits, key=lambda orbit: orbit[0]))


def rotation_orbit_histogram(states: Sequence[State]) -> Dict[str, int]:
    histogram = Counter(len(orbit) for orbit in rotation_orbits(states))
    return {str(size): count for size, count in sorted(histogram.items())}


def state_table_payload(schema: SchemaSpec, states: Sequence[State]) -> Dict[str, object]:
    orbits = rotation_orbits(states)
    orbit_index = {}
    for orbit_id, orbit in enumerate(orbits):
        for state_id in orbit:
            orbit_index[state_id] = orbit_id
    rows = []
    for state_id, state in enumerate(states):
        orbit = orbits[orbit_index[state_id]]
        rows.append(
            {
                "state_id": state_id,
                "state": serialize_state(state),
                "state_name": state_name(state),
                "preferred_anchor_value": preferred_anchor_value(state),
                "orbit_id": orbit_index[state_id],
                "orbit_size": len(orbit),
                "orbit_member_state_ids": list(orbit),
                "is_orbit_representative": state_id == orbit[0],
            }
        )
    return {
        "task_id": TASK_ID,
        "schema": schema.name,
        "schema_description": schema.description,
        "state_count": len(states),
        "rotation_orbit_count": len(orbits),
        "rotation_orbit_size_histogram": rotation_orbit_histogram(states),
        "rows": rows,
    }


def orbit_table_payload(schema: SchemaSpec, states: Sequence[State]) -> Dict[str, object]:
    orbits = rotation_orbits(states)
    return {
        "task_id": TASK_ID,
        "schema": schema.name,
        "schema_description": schema.description,
        "state_count": len(states),
        "rotation_orbit_count": len(orbits),
        "rotation_orbit_size_histogram": rotation_orbit_histogram(states),
        "orbits": [
            {
                "orbit_id": orbit_id,
                "size": len(orbit),
                "state_ids": list(orbit),
                "representative_state_id": orbit[0],
                "representative_state": serialize_state(states[orbit[0]]),
                "representative_state_name": state_name(states[orbit[0]]),
            }
            for orbit_id, orbit in enumerate(orbits)
        ],
    }


@lru_cache(maxsize=None)
def schema_state_space(schema_name: str, m_values: Tuple[int, ...]) -> Tuple[State, ...]:
    schema = SCHEMA_BY_NAME[schema_name]
    states = set()
    for m in m_values:
        for x0 in range(m):
            for x1 in range(m):
                for x2 in range(m):
                    for x3 in range(m):
                        for x4 in range(m):
                            states.add(state_for_vertex((x0, x1, x2, x3, x4), m, schema))
    return tuple(sorted(states, key=lambda item: (str(item[0]), item[1])))


@lru_cache(maxsize=None)
def schema_state_counts_by_m(schema_name: str, m_values: Tuple[int, ...]) -> Tuple[Tuple[int, int], ...]:
    schema = SCHEMA_BY_NAME[schema_name]
    counts = []
    for m in m_values:
        states = set()
        for x0 in range(m):
            for x1 in range(m):
                for x2 in range(m):
                    for x3 in range(m):
                        for x4 in range(m):
                            states.add(state_for_vertex((x0, x1, x2, x3, x4), m, schema))
        counts.append((m, len(states)))
    return tuple(counts)


@lru_cache(maxsize=None)
def vertex_state_ids(schema_name: str, m: int, m_values: Tuple[int, ...]) -> Tuple[int, ...]:
    schema = SCHEMA_BY_NAME[schema_name]
    states = schema_state_space(schema_name, m_values)
    state_to_id = {state: idx for idx, state in enumerate(states)}
    out = []
    for x0 in range(m):
        for x1 in range(m):
            for x2 in range(m):
                for x3 in range(m):
                    for x4 in range(m):
                        out.append(state_to_id[state_for_vertex((x0, x1, x2, x3, x4), m, schema)])
    return tuple(out)


def encode_vertex(coords: Sequence[int], m: int) -> int:
    idx = 0
    for value in coords:
        idx = idx * m + value
    return idx


def decode_vertex(idx: int, m: int) -> Tuple[int, ...]:
    coords = [0] * DIM
    for pos in range(DIM - 1, -1, -1):
        idx, coords[pos] = divmod(idx, m)
    return tuple(coords)


@lru_cache(maxsize=None)
def predecessor_patterns(schema_name: str, m: int, m_values: Tuple[int, ...]) -> Tuple[Tuple[int, ...], ...]:
    state_ids = vertex_state_ids(schema_name, m, m_values)
    patterns = set()
    for vertex_idx in range(m**DIM):
        coords = decode_vertex(vertex_idx, m)
        pred = []
        for direction in range(DIM):
            source = list(coords)
            source[direction] = (source[direction] - 1) % m
            pred.append(state_ids[encode_vertex(source, m)])
        patterns.add(tuple(pred))
    return tuple(sorted(patterns))


def rotation_equalities(states: Sequence[State]) -> List[Tuple[int, int, int]]:
    state_to_id = {state: idx for idx, state in enumerate(states)}
    out = []
    for idx, state in enumerate(states):
        rotated = rotate_state(state, 1)
        out.append((idx, state_to_id[rotated], 1))
    return out


def expand_permutations(states: Sequence[State], base_table: Dict[int, Sequence[int]]) -> Dict[str, object]:
    return {
        "states": [
            {
                "state_id": idx,
                "state_name": state_name(state),
                "state": serialize_state(state),
                "permutation": list(base_table[idx]),
                "permutation_name": permutation_name(base_table[idx]),
                "required_color0_output": required_color0_output(state, SCHEMA_A if len(state[1]) <= 4 else SCHEMA_B),
            }
            for idx, state in enumerate(states)
        ]
    }


def color_map_from_table(
    table: Dict[int, Sequence[int]],
    schema: SchemaSpec,
    m: int,
    coords: Sequence[int],
    color: int,
    m_values: Tuple[int, ...],
) -> Tuple[int, ...]:
    state_ids = vertex_state_ids(schema.name, m, m_values)
    state = state_ids[encode_vertex(coords, m)]
    direction = table[state][color]
    out = list(coords)
    out[direction] = (out[direction] + 1) % m
    return tuple(out)


def indegree_histogram(nexts: Sequence[int]) -> Dict[int, int]:
    indegrees = [0] * len(nexts)
    for nxt in nexts:
        indegrees[nxt] += 1
    histogram = Counter(indegrees)
    return dict(sorted(histogram.items()))


def cycle_decomposition(nexts: Sequence[int]) -> List[List[int]]:
    n = len(nexts)
    visited = [0] * n
    cycles = []
    for start in range(n):
        if visited[start]:
            continue
        seen = {}
        path = []
        cur = start
        while not visited[cur] and cur not in seen:
            seen[cur] = len(path)
            path.append(cur)
            cur = nexts[cur]
        if not visited[cur] and cur in seen:
            cycles.append(path[seen[cur] :])
        for node in path:
            visited[node] = 1
    return cycles


def analyze_latin(table: Dict[int, Sequence[int]], schema: SchemaSpec, m: int, m_values: Tuple[int, ...]) -> Dict[str, object]:
    state_ids = vertex_state_ids(schema.name, m, m_values)
    outgoing_ok = True
    for perm in table.values():
        if sorted(perm) != list(range(DIM)):
            outgoing_ok = False
            break

    incoming_failures = []
    for vertex_idx in range(m**DIM):
        coords = decode_vertex(vertex_idx, m)
        for color in range(DIM):
            count = 0
            witness = []
            for direction in range(DIM):
                source = list(coords)
                source[direction] = (source[direction] - 1) % m
                state = state_ids[encode_vertex(source, m)]
                if table[state][color] == direction:
                    count += 1
                    witness.append(direction)
            if count != 1:
                incoming_failures.append({"vertex": list(coords), "color": color, "matching_directions": witness})
                if len(incoming_failures) >= 20:
                    break
        if len(incoming_failures) >= 20:
            break
    return {
        "m": m,
        "outgoing_latin": outgoing_ok,
        "incoming_latin": len(incoming_failures) == 0,
        "incoming_failure_examples": incoming_failures,
    }


def color_cycle_summary(table: Dict[int, Sequence[int]], schema: SchemaSpec, m: int, m_values: Tuple[int, ...]) -> List[Dict[str, object]]:
    summaries = []
    for color in range(DIM):
        nexts = []
        for vertex_idx in range(m**DIM):
            coords = decode_vertex(vertex_idx, m)
            image = color_map_from_table(table, schema, m, coords, color, m_values)
            nexts.append(encode_vertex(image, m))
        cycles = cycle_decomposition(nexts)
        summaries.append(
            {
                "color": color,
                "cycle_count": len(cycles),
                "cycle_lengths": sorted(len(cycle) for cycle in cycles),
                "is_hamilton": len(cycles) == 1 and len(cycles[0]) == m**DIM,
                "indegree_histogram": indegree_histogram(nexts),
            }
        )
    return summaries


def first_return_qwu_for_color0(table: Dict[int, Sequence[int]], schema: SchemaSpec, m: int, m_values: Tuple[int, ...]) -> Dict[str, object]:
    def step(coords):
        return color_map_from_table(table, schema, m, coords, 0, m_values)

    groups: Dict[Tuple[int, int, int], List[Tuple[Tuple[int, int, int], int]]] = {}
    for q in range(m):
        for w in range(m):
            for u in range(m):
                for v in range(m):
                    coords = ((-q - w - v - u) % m, q, w, v, u)
                    cur = coords
                    for _ in range(m):
                        cur = step(cur)
                    q2, w2, v2, u2 = cur[1], cur[2], cur[3], cur[4]
                    groups.setdefault((q, w, u), []).append(((q2, w2, u2), (v2 - v) % m))

    clean_frame = True
    examples = []
    r_next = {}
    r_dv = {}
    for key, images in groups.items():
        image_set = {item[0] for item in images}
        dv_set = {item[1] for item in images}
        if len(image_set) != 1 or len(dv_set) != 1:
            clean_frame = False
            examples.append({"qwu": list(key), "image_set": [list(item) for item in sorted(image_set)], "dv_set": sorted(dv_set)})
            if len(examples) >= 10:
                break
        else:
            r_next[key] = next(iter(image_set))
            r_dv[key] = next(iter(dv_set))

    strict_clock = clean_frame and all(((image[0] - key[0]) % m) == 1 for key, image in r_next.items())

    u_map = {}
    u_dv = {}
    if clean_frame and strict_clock:
        for w in range(m):
            for u in range(m):
                cur = (0, w, u)
                total = 0
                for _ in range(m):
                    total = (total + r_dv[cur]) % m
                    cur = r_next[cur]
                u_map[(w, u)] = (cur[1], cur[2])
                u_dv[(w, u)] = total

    cycles = []
    monodromies = []
    if u_map:
        idx_map = {(w, u): w * m + u for w in range(m) for u in range(m)}
        nexts = [idx_map[u_map[(w, u)]] for w in range(m) for u in range(m)]
        cycles = cycle_decomposition(nexts)
        monodromies = []
        for cycle in cycles:
            total = 0
            for idx in cycle:
                w, u = divmod(idx, m)
                total = (total + u_dv[(w, u)]) % m
            monodromies.append(total)

    return {
        "m": m,
        "clean_frame": clean_frame,
        "strict_clock": strict_clock,
        "frame_failure_examples": examples,
        "U_cycle_count": len(cycles),
        "U_cycle_lengths": sorted(len(cycle) for cycle in cycles),
        "U_is_single_cycle": len(cycles) == 1 and len(cycles[0]) == m * m,
        "monodromies": monodromies,
        "all_monodromies_unit": all(math.gcd(value, m) == 1 for value in monodromies) if monodromies else False,
    }


def old_collapse_law_for_color0(table: Dict[int, Sequence[int]], schema: SchemaSpec, m: int, m_values: Tuple[int, ...]) -> Dict[str, object]:
    bad_examples = []
    for q in range(m):
        for w in range(m):
            for v in range(m):
                for u in range(m):
                    coords = ((-q - w - v - u) % m, q, w, v, u)
                    cur = coords
                    for _ in range(m):
                        cur = color_map_from_table(table, schema, m, cur, 0, m_values)
                    got = (cur[1], cur[2], cur[3], cur[4])
                    target = ((q + 1) % m, w, (v + 1) % m, u)
                    if got != target:
                        bad_examples.append({"qwvu": [q, w, v, u], "got": list(got), "target": list(target)})
                        if len(bad_examples) >= 20:
                            return {"m": m, "matches_old_collapse_law": False, "bad_examples": bad_examples}
    return {"m": m, "matches_old_collapse_law": True, "bad_examples": bad_examples}


def permutation_table_payload(schema: SchemaSpec, states: Sequence[State], table: Dict[int, Sequence[int]]) -> Dict[str, object]:
    rows = []
    for idx, state in enumerate(states):
        rows.append(
            {
                "state_id": idx,
                "state": serialize_state(state),
                "state_name": state_name(state),
                "permutation": list(table[idx]),
                "permutation_name": permutation_name(table[idx]),
                "required_color0_output": required_color0_output(state, schema),
            }
        )
    return {
        "task_id": TASK_ID,
        "schema": schema.name,
        "schema_description": schema.description,
        "rows": rows,
    }


def anchored_tuple(state: State, schema: SchemaSpec) -> Tuple[int, ...]:
    layer, signature = state
    return tuple(required_output_for_signature(layer, signature[color], schema) for color in range(DIM))


def anchor_defect_summary(schema: SchemaSpec, m: int, m_values: Tuple[int, ...]) -> Dict[str, object]:
    state_ids = vertex_state_ids(schema.name, m, m_values)
    states = schema_state_space(schema.name, m_values)
    outgoing_perm_count = 0
    tuple_hist = Counter()
    tuple_examples = []
    incoming_failures = 0
    incoming_examples = []

    anchor_table = {state_id: anchored_tuple(states[state_id], schema) for state_id in range(len(states))}

    for state_id, perm in anchor_table.items():
        histogram = tuple(sorted(Counter(perm).values(), reverse=True))
        tuple_hist[histogram] += 1
        if sorted(perm) == list(range(DIM)):
            outgoing_perm_count += 1
        elif len(tuple_examples) < 10:
            tuple_examples.append({"state_id": state_id, "state": serialize_state(states[state_id]), "tuple": list(perm), "multiplicity_pattern": list(histogram)})

    for vertex_idx in range(m**DIM):
        coords = decode_vertex(vertex_idx, m)
        for color in range(DIM):
            count = 0
            witness = []
            for direction in range(DIM):
                source = list(coords)
                source[direction] = (source[direction] - 1) % m
                state = state_ids[encode_vertex(source, m)]
                if anchor_table[state][color] == direction:
                    count += 1
                    witness.append(direction)
            if count != 1:
                incoming_failures += 1
                if len(incoming_examples) < 10:
                    incoming_examples.append({"vertex": list(coords), "color": color, "matching_directions": witness})

    return {
        "m": m,
        "state_count": len(states),
        "outgoing_permutation_state_count": outgoing_perm_count,
        "outgoing_nonpermutation_state_count": len(states) - outgoing_perm_count,
        "outgoing_multiplicity_histogram": {",".join(str(v) for v in key): value for key, value in sorted(tuple_hist.items())},
        "outgoing_examples": tuple_examples,
        "incoming_failure_count": incoming_failures,
        "incoming_failure_examples": incoming_examples,
    }


def anchor_values_to_permutation_table(states: Sequence[State], anchor_values: Dict[int, int]) -> Dict[int, Tuple[int, ...]]:
    state_map = state_to_id_map(states)
    out = {}
    for state_id, state in enumerate(states):
        perm = []
        for color in range(DIM):
            rotated = rotate_state(state, (-color) % DIM)
            anchor = anchor_values[state_map[rotated]]
            perm.append((anchor + color) % DIM)
        out[state_id] = tuple(perm)
    return out


def anchor_table_payload(schema: SchemaSpec, states: Sequence[State], anchor_values: Dict[int, int]) -> Dict[str, object]:
    rows = []
    perm_table = anchor_values_to_permutation_table(states, anchor_values)
    for idx, state in enumerate(states):
        rows.append(
            {
                "state_id": idx,
                "state": serialize_state(state),
                "state_name": state_name(state),
                "anchor_value": int(anchor_values[idx]),
                "preferred_anchor_value": preferred_anchor_value(state),
                "permutation": list(perm_table[idx]),
                "permutation_name": permutation_name(perm_table[idx]),
            }
        )
    return {
        "task_id": TASK_ID,
        "rows": rows,
    }
