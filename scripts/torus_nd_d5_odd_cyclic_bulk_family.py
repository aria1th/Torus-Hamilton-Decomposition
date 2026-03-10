#!/usr/bin/env python3
"""Shared family helpers for d=5 odd cyclic-bulk searches."""

from __future__ import annotations

import itertools
import json
from typing import Dict, Iterable, List, Sequence, Tuple

DIM = 5
LOW_LAYERS = (0, 1, 2, 3)
SIGMA: Tuple[int, int, int, int, int] = (1, 2, 3, 4, 0)
SIGMA_INV: Tuple[int, int, int, int, int] = (4, 0, 1, 2, 3)
CANONICAL: Tuple[int, int, int, int, int] = (0, 1, 2, 3, 4)
LAYER_GATE_LAYERS = (1, 2, 3)
GatePair = Tuple[int, int]
ConfigDict = Dict[str, object]

GATE_CATALOG: Tuple[GatePair, ...] = tuple(itertools.combinations(range(DIM), 2))


def charge(coords: Sequence[int], m: int) -> int:
    return sum((idx * coords[idx]) for idx in range(1, DIM)) % m


def rotate_tuple(values: Sequence[int], shift: int) -> Tuple[int, ...]:
    return tuple((value + shift) % DIM for value in values)


def apply_slot_swap(direction_tuple: Sequence[int], slot_a: int, slot_b: int) -> Tuple[int, ...]:
    out = list(direction_tuple)
    out[slot_a], out[slot_b] = out[slot_b], out[slot_a]
    return tuple(out)


def apply_rotating_zero_gate(
    direction_tuple: Sequence[int],
    coords: Sequence[int],
    gate_pair: GatePair,
    m: int,
) -> Tuple[int, ...]:
    out = tuple(direction_tuple)
    for shift in range(DIM):
        if coords[shift] % m != 0:
            continue
        slot_a = (gate_pair[0] + shift) % DIM
        slot_b = (gate_pair[1] + shift) % DIM
        out = apply_slot_swap(out, slot_a, slot_b)
    return out


def gate_pair_name(gate_pair: GatePair) -> str:
    return f"swap_{gate_pair[0]}_{gate_pair[1]}"


def permutation_name(perm: Sequence[int]) -> str:
    return "".join(str(x) for x in perm)


def serialize_config(config: ConfigDict) -> Dict[str, object]:
    return {
        "family": str(config["family"]),
        "layer0_q0_tuple": list(config["layer0_q0_tuple"]),
        "layer_gates": {
            str(layer): [list(gate) for gate in config["layer_gates"][str(layer)]]
            for layer in LAYER_GATE_LAYERS
        },
    }


def config_key(config: ConfigDict) -> str:
    return json.dumps(serialize_config(config), sort_keys=True)


def config_name(config: ConfigDict) -> str:
    layer0 = permutation_name(config["layer0_q0_tuple"])
    layer_bits = []
    for layer in LAYER_GATE_LAYERS:
        gates = config["layer_gates"][str(layer)]
        if not gates:
            layer_bits.append(f"L{layer}:none")
            continue
        names = ",".join(gate_pair_name(tuple(gate)) for gate in gates)
        layer_bits.append(f"L{layer}:{names}")
    return f"q0={layer0}|" + "|".join(layer_bits)


def validate_config_shape(config: ConfigDict) -> None:
    tuple_q0 = tuple(int(x) for x in config["layer0_q0_tuple"])
    if sorted(tuple_q0) != list(range(DIM)):
        raise ValueError("layer0_q0_tuple must be a permutation of 0..4")
    for layer in LAYER_GATE_LAYERS:
        gates = config["layer_gates"][str(layer)]
        seen = set()
        for gate in gates:
            pair = tuple(int(x) for x in gate)
            if pair not in GATE_CATALOG:
                raise ValueError(f"Unknown gate pair {pair} on layer {layer}")
            if pair in seen:
                raise ValueError(f"Duplicate gate pair {pair} on layer {layer}")
            seen.add(pair)


def build_rule(config: ConfigDict, m: int):
    validate_config_shape(config)
    layer0_q0_tuple = tuple(int(x) for x in config["layer0_q0_tuple"])
    layer_gates = {
        int(layer): [tuple(int(x) for x in gate) for gate in gates]
        for layer, gates in config["layer_gates"].items()
    }

    def rule(coords: Sequence[int]) -> Tuple[int, ...]:
        layer = sum(coords) % m
        if layer == 0:
            return layer0_q0_tuple if charge(coords, m) == 0 else SIGMA
        if layer not in LAYER_GATE_LAYERS:
            return CANONICAL
        out = CANONICAL
        for gate_pair in layer_gates[layer]:
            out = apply_rotating_zero_gate(out, coords, gate_pair, m)
        return out

    return rule


def base_config(layer0_q0_tuple: Sequence[int]) -> ConfigDict:
    return {
        "family": "d5_odd_cyclic_bulk_rotating_zero_swaps_v1",
        "layer0_q0_tuple": list(layer0_q0_tuple),
        "layer_gates": {str(layer): [] for layer in LAYER_GATE_LAYERS},
    }


def config_with_layer_gates(
    layer0_q0_tuple: Sequence[int],
    layer_gate_map: Dict[int, Sequence[GatePair]],
) -> ConfigDict:
    config = base_config(layer0_q0_tuple)
    for layer in LAYER_GATE_LAYERS:
        config["layer_gates"][str(layer)] = [list(pair) for pair in layer_gate_map.get(layer, [])]
    return config


def all_layer0_permutations() -> List[Tuple[int, ...]]:
    return [tuple(perm) for perm in itertools.permutations(range(DIM))]


def all_five_cycle_permutations() -> List[Tuple[int, ...]]:
    out = []
    for perm in all_layer0_permutations():
        seen = set()
        cur = 0
        cycle = []
        while cur not in seen:
            seen.add(cur)
            cycle.append(cur)
            cur = perm[cur]
        if cur == 0 and len(cycle) == DIM:
            out.append(perm)
    return out


def single_gate_options() -> List[List[GatePair]]:
    return [[]] + [[pair] for pair in GATE_CATALOG]


def random_gate_sequence(rng, max_gates: int) -> List[GatePair]:
    count = rng.randint(0, max_gates)
    if count == 0:
        return []
    picks = rng.sample(list(GATE_CATALOG), count)
    return [tuple(pair) for pair in picks]
