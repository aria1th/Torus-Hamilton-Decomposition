#!/usr/bin/env python3
"""Common utilities for the d=5 return-map model extraction."""

from __future__ import annotations

import json
import math
import platform
import time
from collections import Counter
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import torus_nd_d5_layer3_alt2_decoupled_common as cycle007
import torus_nd_d5_layer3_mode_switch_common as mode008
import torus_nd_d5_shared_pred_interaction_common as anti010
from torus_nd_d5_strict_palette_context_common import DIM, encode, parse_m_list

TASK_ID = "D5-RETURN-MAP-MODEL-017"
PILOT_M_VALUES = (5, 7, 9)
STABILITY_M_VALUES = (11, 13)
DEFAULT_M_VALUES = PILOT_M_VALUES + STABILITY_M_VALUES


@dataclass(frozen=True)
class WitnessSpec:
    name: str
    role: str
    family: str
    source: str
    rule_payload: Mapping[str, object]


@dataclass
class PreparedWitness:
    spec: WitnessSpec
    pre_by_m: Dict[int, Dict[str, object]]
    nexts0_by_m: Dict[int, List[int]]
    dir_by_m: Dict[int, List[int]]


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


def _load_json(path: str | Path) -> Dict[str, object]:
    return json.loads(Path(path).read_text())


def _load_mixed_008() -> WitnessSpec:
    data = _load_json("artifacts/d5_layer3_mode_switch_008/data/validation_summary.json")
    candidate = next(
        item
        for item in data["candidates"]
        if item["pilot_validation"]["overall_kind"] == "both"
        and item["pilot_validation"]["total_u_cycle_count"] == 21
        and item["rule"].get("predecessor_flag_name") == "pred_sig1_wu2"
        and item["rule"].get("layer2_orientation") == "0/2"
        and item["rule"]["layer3_mode_p0"]["name"] == "0/3"
        and item["rule"]["layer3_mode_p1"]["name"] == "3/0"
    )
    return WitnessSpec(
        name="mixed_008",
        role="canonical_mixed",
        family="mode_switch_008",
        source="artifacts/d5_layer3_mode_switch_008/data/validation_summary.json",
        rule_payload=candidate["rule"],
    )


def _load_monodromy_008() -> WitnessSpec:
    data = _load_json("artifacts/d5_layer3_mode_switch_008/data/validation_summary.json")
    candidate = next(
        item
        for item in data["candidates"]
        if item["pilot_validation"]["overall_kind"] == "monodromy_only"
    )
    return WitnessSpec(
        name="monodromy_008",
        role="monodromy_only_control",
        family="mode_switch_008",
        source="artifacts/d5_layer3_mode_switch_008/data/validation_summary.json",
        rule_payload=candidate["rule"],
    )


def _load_cycle_007() -> WitnessSpec:
    data = _load_json("artifacts/d5_layer3_alt2_decoupled_007/data/search_summary.json")
    candidate = data["best_cycle_only_rules"][0]
    return WitnessSpec(
        name="cycle_007",
        role="cycle_only_control",
        family="cycle_007",
        source="artifacts/d5_layer3_alt2_decoupled_007/data/search_summary.json",
        rule_payload=candidate["rule"],
    )


def _load_anti_010() -> WitnessSpec:
    data = _load_json("artifacts/d5_shared_pred_interaction_010/data/validation_summary.json")
    candidate = next(
        item
        for item in data["candidates"]
        if item["pilot_validation"]["overall_kind"] == "both"
        and item["pilot_validation"]["total_u_cycle_count"] == 39
    )
    return WitnessSpec(
        name="anti_mixed_010",
        role="anti_compressive_mixed_control",
        family="shared_010",
        source="artifacts/d5_shared_pred_interaction_010/data/validation_summary.json",
        rule_payload=candidate["rule"],
    )


def load_witness_specs() -> List[WitnessSpec]:
    return [
        _load_mixed_008(),
        _load_cycle_007(),
        _load_monodromy_008(),
        _load_anti_010(),
    ]


def _infer_direction(coords: Sequence[Tuple[int, ...]], nexts0: Sequence[int], m: int) -> List[int]:
    out = [0] * len(nexts0)
    for idx, nxt in enumerate(nexts0):
        cur_coords = coords[idx]
        nxt_coords = coords[nxt]
        found = None
        for direction in range(DIM):
            ok = True
            for axis in range(DIM):
                want = 1 if axis == direction else 0
                if (nxt_coords[axis] - cur_coords[axis]) % m != want:
                    ok = False
                    break
            if ok:
                found = direction
                break
        if found is None:
            raise ValueError(f"could not infer direction for transition {idx}->{nxt} at m={m}")
        out[idx] = found
    return out


def prepare_witness(spec: WitnessSpec, m_values: Sequence[int]) -> PreparedWitness:
    pre_by_m: Dict[int, Dict[str, object]] = {}
    nexts0_by_m: Dict[int, List[int]] = {}
    dir_by_m: Dict[int, List[int]] = {}

    if spec.family == "mode_switch_008":
        signature_to_id = mode008.exact_signature_catalog(tuple(sorted(set(m_values))))["signature_to_id"]
        rule = mode008.Rule.from_payload(spec.rule_payload)
        for m in m_values:
            pre = mode008.precompute_m(m, signature_to_id)
            anchors = mode008.anchor_by_feature(pre, rule)
            nexts0 = mode008.nexts_all_for_rule(pre, anchors)[0]
            pre_by_m[m] = pre
            nexts0_by_m[m] = nexts0
            dir_by_m[m] = _infer_direction(pre["coords"], nexts0, m)
    elif spec.family == "cycle_007":
        rule = cycle007.Rule.from_payload(dict(spec.rule_payload))
        for m in m_values:
            pre = cycle007.precompute_m(m, rule.layer2_bit_name, rule.layer3_bit_name)
            nexts0 = cycle007.nexts_all_for_rule(pre, rule)[0]
            pre_by_m[m] = pre
            nexts0_by_m[m] = nexts0
            dir_by_m[m] = _infer_direction(pre["coords"], nexts0, m)
    elif spec.family == "shared_010":
        rule = anti010.Rule.from_payload(spec.rule_payload)
        for m in m_values:
            pre = anti010.precompute_m(m, rule.layer3_bit_name)
            anchors = anti010.anchor_by_feature(pre, rule)
            nexts0 = anti010.nexts_all_for_rule(pre, anchors)[0]
            pre_by_m[m] = pre
            nexts0_by_m[m] = nexts0
            dir_by_m[m] = _infer_direction(pre["coords"], nexts0, m)
    else:
        raise ValueError(f"unsupported witness family {spec.family}")

    return PreparedWitness(spec=spec, pre_by_m=pre_by_m, nexts0_by_m=nexts0_by_m, dir_by_m=dir_by_m)


def _state_key(q: int, w: int, u: int) -> str:
    return f"{q},{w},{u}"


def _wu_key(w: int, u: int) -> str:
    return f"{w},{u}"


def simulate_return_trace(pre: Mapping[str, object], nexts0: Sequence[int], dir_row: Sequence[int], *, q: int, w: int, v: int, u: int) -> Dict[str, object]:
    m = int(pre["m"])
    coords = pre["coords"]
    idx = encode(((-q - w - v - u) % m, q, w, v, u), m)
    cur = idx
    word: List[int] = []
    low_layer_word: List[int] = []
    layer_sequence: List[int] = []
    for step in range(m):
        current_coords = coords[cur]
        layer_sequence.append(sum(current_coords) % m)
        direction = int(dir_row[cur])
        word.append(direction)
        if step < 4:
            low_layer_word.append(direction)
        cur = nexts0[cur]
    c = coords[cur]
    next_state = (int(c[1]), int(c[2]), int(c[4]))
    return {
        "next_state": next_state,
        "dv": int((c[3] - v) % m),
        "word": tuple(word),
        "low_layer_word": tuple(low_layer_word),
        "layer_sequence": tuple(layer_sequence),
    }


def extract_first_return_table(pre: Mapping[str, object], nexts0: Sequence[int], dir_row: Sequence[int]) -> Dict[str, object]:
    m = int(pre["m"])
    states: Dict[str, object] = {}
    clean_frame = True
    strict_clock = True
    low_word_counter: Counter[Tuple[int, ...]] = Counter()
    word_counter: Counter[Tuple[int, ...]] = Counter()

    for q in range(m):
        for w in range(m):
            for u in range(m):
                traces = [simulate_return_trace(pre, nexts0, dir_row, q=q, w=w, v=v, u=u) for v in range(m)]
                next_set = {trace["next_state"] for trace in traces}
                dv_set = {trace["dv"] for trace in traces}
                word_set = {trace["word"] for trace in traces}
                low_word_set = {trace["low_layer_word"] for trace in traces}
                representative = traces[0]
                state_clean = len(next_set) == 1 and len(dv_set) == 1
                next_state = list(representative["next_state"]) if state_clean else None
                dv = int(representative["dv"]) if state_clean else None
                if not state_clean:
                    clean_frame = False
                    strict_clock = False
                else:
                    strict_clock &= ((int(next_state[0]) - q) % m) == 1
                    low_word_counter[representative["low_layer_word"]] += 1
                    word_counter[representative["word"]] += 1
                states[_state_key(q, w, u)] = {
                    "q": q,
                    "w": w,
                    "u": u,
                    "clean_state": state_clean,
                    "next_state": next_state,
                    "next_increment": (
                        None
                        if next_state is None
                        else [int((next_state[0] - q) % m), int((next_state[1] - w) % m), int((next_state[2] - u) % m)]
                    ),
                    "dv": dv,
                    "representative_v": 0,
                    "representative_word": list(representative["word"]),
                    "representative_low_layer_word": list(representative["low_layer_word"]),
                    "word_variation_count": len(word_set),
                    "low_layer_word_variation_count": len(low_word_set),
                    "sample_v_images": [
                        {
                            "v": v,
                            "next_state": list(trace["next_state"]),
                            "dv": int(trace["dv"]),
                            "low_layer_word": list(trace["low_layer_word"]),
                        }
                        for v, trace in enumerate(traces[: min(4, m)])
                    ],
                }

    return {
        "m": m,
        "clean_frame": clean_frame,
        "strict_clock": strict_clock,
        "state_count": m**3,
        "states": states,
        "low_layer_word_histogram": [
            {"word": list(word), "count": count}
            for word, count in sorted(low_word_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
        "full_word_histogram": [
            {"word": list(word), "count": count}
            for word, count in sorted(word_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
    }


def extract_grouped_return(first_return_table: Mapping[str, object]) -> Dict[str, object]:
    m = int(first_return_table["m"])
    if not (first_return_table["clean_frame"] and first_return_table["strict_clock"]):
        return {
            "m": m,
            "available": False,
            "reason": "first_return_not_clean_strict",
            "state_count": m**2,
            "states": {},
        }

    rows: Mapping[str, Mapping[str, object]] = first_return_table["states"]
    states: Dict[str, object] = {}
    u_next: Dict[Tuple[int, int], Tuple[int, int]] = {}
    u_phi: Dict[Tuple[int, int], int] = {}

    for w in range(m):
        for u in range(m):
            cur = (0, w, u)
            grouped_trace: List[List[int]] = []
            total_dv = 0
            for _ in range(m):
                row = rows[_state_key(*cur)]
                grouped_trace.append(list(row["representative_low_layer_word"]))
                total_dv = (total_dv + int(row["dv"])) % m
                next_state = row["next_state"]
                cur = (int(next_state[0]), int(next_state[1]), int(next_state[2]))
            next_wu = (cur[1], cur[2])
            u_next[(w, u)] = next_wu
            u_phi[(w, u)] = total_dv
            states[_wu_key(w, u)] = {
                "w": w,
                "u": u,
                "next_state": [int(next_wu[0]), int(next_wu[1])],
                "next_increment": [int((next_wu[0] - w) % m), int((next_wu[1] - u) % m)],
                "phi": int(total_dv),
                "grouped_low_layer_trace": grouped_trace,
            }

    visited = set()
    cycles = []
    monodromies = []
    for start in sorted(u_next):
        if start in visited:
            continue
        cur = start
        cycle = []
        total = 0
        while cur not in visited:
            visited.add(cur)
            cycle.append(cur)
            total = (total + u_phi[cur]) % m
            cur = u_next[cur]
        cycles.append(cycle)
        monodromies.append(total)

    return {
        "m": m,
        "available": True,
        "state_count": m**2,
        "states": states,
        "cycle_count": len(cycles),
        "cycle_lengths": [len(cycle) for cycle in cycles],
        "cycle_monodromies": [int(value) for value in monodromies],
    }


def _refine_partition(
    states: Sequence[Tuple[int, ...]],
    next_map: Mapping[Tuple[int, ...], Tuple[int, ...]],
    outputs: Mapping[Tuple[int, ...], object],
) -> Dict[str, object]:
    block_of: Dict[Tuple[int, ...], int] = {}
    signature_to_block: Dict[object, int] = {}
    for state in states:
        signature = outputs[state]
        if signature not in signature_to_block:
            signature_to_block[signature] = len(signature_to_block)
        block_of[state] = signature_to_block[signature]

    changed = True
    while changed:
        changed = False
        new_block_of: Dict[Tuple[int, ...], int] = {}
        signature_to_block = {}
        for state in states:
            signature = (outputs[state], block_of[next_map[state]])
            if signature not in signature_to_block:
                signature_to_block[signature] = len(signature_to_block)
            new_block_of[state] = signature_to_block[signature]
        if any(new_block_of[state] != block_of[state] for state in states):
            changed = True
            block_of = new_block_of

    classes: Dict[int, List[Tuple[int, ...]]] = {}
    for state, block in block_of.items():
        classes.setdefault(block, []).append(state)
    transitions = {}
    for block, members in classes.items():
        rep = members[0]
        transitions[str(block)] = int(block_of[next_map[rep]])
    return {
        "class_count": len(classes),
        "classes": {str(block): [list(state) for state in sorted(members)] for block, members in sorted(classes.items())},
        "transitions": transitions,
    }


def deterministic_quotient_R(first_return_table: Mapping[str, object]) -> Dict[str, object]:
    if not (first_return_table["clean_frame"] and first_return_table["strict_clock"]):
        return {"available": False, "reason": "first_return_not_clean_strict"}
    rows = first_return_table["states"]
    states = [(row["q"], row["w"], row["u"]) for row in rows.values()]
    next_map = {(row["q"], row["w"], row["u"]): tuple(int(v) for v in row["next_state"]) for row in rows.values()}
    outputs = {
        (row["q"], row["w"], row["u"]): (
            int(row["dv"]),
            tuple(int(v) for v in row["representative_low_layer_word"]),
        )
        for row in rows.values()
    }
    result = _refine_partition(states, next_map, outputs)
    result["available"] = True
    result["output_signature"] = "dv + low_layer_word"
    return result


def deterministic_quotient_U(grouped_return: Mapping[str, object]) -> Dict[str, object]:
    if not grouped_return.get("available", False):
        return {"available": False, "reason": grouped_return.get("reason", "grouped_return_unavailable")}
    rows = grouped_return["states"]
    states = [(row["w"], row["u"]) for row in rows.values()]
    next_map = {(row["w"], row["u"]): tuple(int(v) for v in row["next_state"]) for row in rows.values()}
    outputs = {
        (row["w"], row["u"]): (
            int(row["phi"]),
            tuple(tuple(int(value) for value in word) for word in row["grouped_low_layer_trace"]),
        )
        for row in rows.values()
    }
    result = _refine_partition(states, next_map, outputs)
    result["available"] = True
    result["output_signature"] = "phi + grouped_low_layer_trace"
    return result


def fit_affine_map(states: Sequence[Tuple[int, ...]], images: Mapping[Tuple[int, ...], Tuple[int, ...]], m: int) -> Dict[str, object]:
    dim = len(states[0]) if states else 0
    zero = (0,) * dim
    if zero not in images:
        return {"exact": False, "reason": "zero_state_missing"}
    bias = tuple(int(v) for v in images[zero])
    columns = []
    for axis in range(dim):
        basis = [0] * dim
        basis[axis] = 1 % m
        basis_t = tuple(basis)
        if basis_t not in images:
            return {"exact": False, "reason": f"basis_state_missing:{basis_t}"}
        image = images[basis_t]
        columns.append(tuple((int(image[row]) - bias[row]) % m for row in range(len(bias))))

    def predict(state: Tuple[int, ...]) -> Tuple[int, ...]:
        out = list(bias)
        for axis, coeff in enumerate(state):
            for row in range(len(out)):
                out[row] = (out[row] + coeff * columns[axis][row]) % m
        return tuple(out)

    mismatches = []
    for state in states:
        predicted = predict(state)
        if predicted != tuple(int(v) for v in images[state]):
            mismatches.append({"state": list(state), "predicted": list(predicted), "actual": list(images[state])})
            if len(mismatches) >= 5:
                break
    return {
        "exact": len(mismatches) == 0,
        "bias": list(bias),
        "matrix_columns": [list(column) for column in columns],
        "mismatch_examples": mismatches,
    }


def fit_affine_scalar(states: Sequence[Tuple[int, ...]], values: Mapping[Tuple[int, ...], int], m: int) -> Dict[str, object]:
    wrapped = {state: (int(value),) for state, value in values.items()}
    fitted = fit_affine_map(states, wrapped, m)
    return {
        "exact": fitted["exact"],
        "bias": int(fitted["bias"][0]) if "bias" in fitted else None,
        "coefficients": [int(column[0]) for column in fitted.get("matrix_columns", [])],
        "mismatch_examples": fitted.get("mismatch_examples", []),
    }


def fit_single_slice(states: Sequence[Tuple[int, ...]], values: Mapping[Tuple[int, ...], int], m: int) -> Dict[str, object]:
    unique_values = sorted({int(values[state]) for state in states})
    if len(unique_values) == 1:
        return {"kind": "constant", "value": unique_values[0]}
    if len(unique_values) > 2:
        return {"kind": "none"}
    for alpha in ((a, b, c) for a in range(m) for b in range(m) for c in range(m) if (a, b, c) != (0, 0, 0)):
        for offset in range(m):
            off_values = {
                int(values[state])
                for state in states
                if (alpha[0] * state[0] + alpha[1] * state[1] + alpha[2] * state[2]) % m != offset
            }
            on_values = {
                int(values[state])
                for state in states
                if (alpha[0] * state[0] + alpha[1] * state[1] + alpha[2] * state[2]) % m == offset
            }
            if not off_values or not on_values:
                continue
            if len(off_values) == 1 and len(on_values) == 1:
                base_value = next(iter(off_values))
                on_value = next(iter(on_values))
                delta = (on_value - base_value) % m
                return {
                    "kind": "single_slice",
                    "alpha": list(alpha),
                    "offset": int(offset),
                    "base_value": int(base_value),
                    "delta": int(delta),
                }
    return {"kind": "none"}


def _units(m: int) -> List[int]:
    return [value for value in range(1, m) if math.gcd(value, m) == 1]


def _normalize_form(alpha: Tuple[int, ...], m: int) -> Tuple[int, ...]:
    candidates = [tuple((unit * value) % m for value in alpha) for unit in _units(m)] or [alpha]
    return min(candidates)


def search_linear_forms(states: Sequence[Tuple[int, ...]], next_map: Mapping[Tuple[int, ...], Tuple[int, ...]], m: int) -> Dict[str, object]:
    dim = len(states[0]) if states else 0
    seen = set()
    invariants = []
    translators = []
    for alpha in (tuple(values) for values in _product_range(m, dim)):
        if all(value == 0 for value in alpha):
            continue
        normalized = _normalize_form(alpha, m)
        if normalized in seen:
            continue
        seen.add(normalized)
        deltas = {
            (sum(alpha[i] * next_map[state][i] for i in range(dim)) - sum(alpha[i] * state[i] for i in range(dim))) % m
            for state in states
        }
        if len(deltas) != 1:
            continue
        delta = int(next(iter(deltas)))
        record = {"alpha": list(normalized), "delta": delta}
        if delta == 0:
            invariants.append(record)
        else:
            translators.append(record)
    invariants.sort(key=lambda item: item["alpha"])
    translators.sort(key=lambda item: (item["delta"], item["alpha"]))
    return {"invariants": invariants, "translators": translators}


def _product_range(m: int, dim: int) -> Iterable[Tuple[int, ...]]:
    if dim == 0:
        yield ()
        return
    current = [0] * dim
    while True:
        yield tuple(current)
        pos = dim - 1
        while pos >= 0:
            current[pos] += 1
            if current[pos] < m:
                break
            current[pos] = 0
            pos -= 1
        if pos < 0:
            return


def classify_grouped_model(grouped_return: Mapping[str, object], affine_next: Mapping[str, object], linear_forms: Mapping[str, object], m: int) -> Dict[str, object]:
    if not grouped_return.get("available", False):
        return {"kind": "unavailable"}
    if not affine_next.get("exact", False):
        return {"kind": "non_affine_grouped_return"}
    bias = tuple(int(v) for v in affine_next["bias"])
    columns = [tuple(int(v) for v in col) for col in affine_next["matrix_columns"]]
    identity = tuple(tuple(1 if row == col else 0 for row in range(len(columns))) for col in range(len(columns)))
    if tuple(columns) == identity:
        invariants = linear_forms["invariants"]
        translators = [item for item in linear_forms["translators"] if math.gcd(int(item["delta"]), m) == 1]
        if invariants and translators:
            return {
                "kind": "skew_odometer_candidate",
                "translation_bias": list(bias),
                "invariant_form": invariants[0],
                "advancing_form": translators[0],
            }
        return {"kind": "translation_candidate", "translation_bias": list(bias)}
    return {"kind": "affine_nontranslation_grouped_return", "translation_bias": list(bias), "matrix_columns": [list(col) for col in columns]}
