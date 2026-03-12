#!/usr/bin/env python3
"""Package the D5 finite-cover picture beyond the carry slice on the best-seed active union."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import torus_nd_d5_carry_slice_cover as carry042
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-FINITE-COVER-ADMISSIBILITY-043"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M_VALUES = (11,)
ALL_M_VALUES = PRIMARY_M_VALUES + CONTROL_M_VALUES
SHORT_FUTURE_WINDOW_LIMIT = 7

State = Tuple[int, int, int, int, int, str]
BKey = Tuple[int, int, int, int, str]
BcKey = Tuple[int, int, int, int, str, int]


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _b_key(info: Mapping[str, object]) -> BKey:
    s_value, u_value, v_value, layer, family = info["B"]
    return (int(s_value), int(u_value), int(v_value), int(layer), str(family))


def _bc_key(m: int, state: State, info: Mapping[str, object]) -> BcKey:
    return _b_key(info) + (int(state[0] == m - 1),)


def _state_payload(state: State, info: Mapping[str, object], *, cover_class: int | None = None) -> Dict[str, object]:
    payload: Dict[str, object] = {
        "q": int(state[0]),
        "w": int(state[1]),
        "u": int(state[2]),
        "v": int(state[3]),
        "layer": int(state[4]),
        "family": str(state[5]),
        "B": list(_b_key(info)),
    }
    if cover_class is not None:
        payload["cover_class"] = int(cover_class)
    return payload


def _active_model(m: int) -> Tuple[List[Dict[str, object]], Dict[State, Dict[str, object]], Dict[State, State]]:
    rows, state_info, next_map = carry042._active_union(m)
    rows_by_state = {
        (int(row["q"]), int(row["w"]), int(row["u"]), int(row["v"]), int(row["layer"]), str(row["family"])): row
        for row in rows
    }
    for state, nxt in next_map.items():
        rows_by_state[state]["next_B"] = rows_by_state[nxt]["B"]
        rows_by_state[state]["next_Bc"] = rows_by_state[nxt]["Bc"]
    return rows, state_info, next_map


def _minimal_cover_classes(
    state_info: Mapping[State, Mapping[str, object]],
    next_map: Mapping[State, State],
) -> Tuple[int, Dict[State, int]]:
    classes: Dict[State, object] = {state: info["status"] for state, info in state_info.items()}
    rounds = 0
    changed = True
    while changed and rounds < 5000:
        rounds += 1
        signature_to_id: Dict[Tuple[object, object], int] = {}
        new_classes: Dict[State, int] = {}
        for state in sorted(state_info, key=repr):
            signature = (state_info[state]["status"], classes.get(next_map.get(state), None))
            if signature not in signature_to_id:
                signature_to_id[signature] = len(signature_to_id)
            new_classes[state] = signature_to_id[signature]
        changed = new_classes != classes
        classes = new_classes
    return rounds, {state: int(label) for state, label in classes.items()}


def _fiber_buckets(
    m: int,
    state_info: Mapping[State, Mapping[str, object]],
    *,
    key_name: str,
) -> Dict[Tuple[object, ...], List[State]]:
    out: Dict[Tuple[object, ...], List[State]] = defaultdict(list)
    for state, info in state_info.items():
        if key_name == "B":
            out[_b_key(info)].append(state)
        elif key_name == "Bc":
            out[_bc_key(m, state, info)].append(state)
        else:
            raise ValueError(f"unknown key_name: {key_name}")
    return out


def _cover_summary_over_key(
    m: int,
    state_info: Mapping[State, Mapping[str, object]],
    next_map: Mapping[State, State],
    classes: Mapping[State, int],
    *,
    key_name: str,
) -> Dict[str, object]:
    buckets = _fiber_buckets(m, state_info, key_name=key_name)
    class_buckets = {key: sorted({int(classes[state]) for state in states}) for key, states in buckets.items()}
    fiber_sizes = sorted({len(values) for values in class_buckets.values()})
    max_fiber = max((len(values) for values in class_buckets.values()), default=0)
    ambiguous_keys = [key for key, values in class_buckets.items() if len(values) > 1]

    if key_name == "Bc":
        local_sheet_index: Dict[State, int] = {}
        for key, states in buckets.items():
            ordered = sorted({int(classes[state]) for state in states})
            class_to_sheet = {cover_class: idx for idx, cover_class in enumerate(ordered)}
            for state in states:
                local_sheet_index[state] = int(class_to_sheet[int(classes[state])])
        transition_buckets: Dict[Tuple[object, ...], set[Tuple[object, ...]]] = defaultdict(set)
        for state, nxt in next_map.items():
            transition_buckets[
                (_bc_key(m, state, state_info[state]), int(local_sheet_index[state]))
            ].add(
                (_bc_key(m, nxt, state_info[nxt]), int(local_sheet_index[nxt]))
            )
        nondeterministic = [key for key, values in transition_buckets.items() if len(values) > 1]
    else:
        local_sheet_index = {}
        nondeterministic = []

    sample_max_fiber = None
    for key in ambiguous_keys:
        if len(class_buckets[key]) != max_fiber:
            continue
        rows = [
            _state_payload(state, state_info[state], cover_class=int(classes[state]))
            for state in buckets[key]
        ]
        if key_name == "Bc":
            for row, state in zip(rows, buckets[key]):
                row["local_sheet"] = int(local_sheet_index[state])
        sample_max_fiber = {
            key_name: list(key),
            "rows": rows,
        }
        break

    out: Dict[str, object] = {
        "fiber_sizes_seen": [int(value) for value in fiber_sizes],
        "max_cover_fiber_size": int(max_fiber),
        "ambiguous_key_count": int(len(ambiguous_keys)),
        "sample_max_fiber": sample_max_fiber,
    }
    if key_name == "Bc":
        out["transition_on_cover"] = {
            "is_deterministic": bool(not nondeterministic),
            "nondeterministic_key_count": int(len(nondeterministic)),
            "sample_nondeterministic_key": None if not nondeterministic else list(nondeterministic[0]),
        }
    return out


def _feature_refines_cover_summary(
    m: int,
    state_info: Mapping[State, Mapping[str, object]],
    classes: Mapping[State, int],
    feature_name: str,
    feature_fn: Callable[[State], object],
) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], set[int]] = defaultdict(set)
    sample_collision = None
    for state, info in state_info.items():
        key = _bc_key(m, state, info) + (feature_fn(state),)
        buckets[key].add(int(classes[state]))
    collisions = [key for key, values in buckets.items() if len(values) > 1]
    if collisions:
        key = collisions[0]
        witness_states = [
            state
            for state, info in state_info.items()
            if _bc_key(m, state, info) + (feature_fn(state),) == key
        ]
        sample_collision = {
            "shared_key": list(key[:-1]),
            "feature_value": key[-1] if not isinstance(key[-1], tuple) else list(key[-1]),
            "rows": [
                _state_payload(state, state_info[state], cover_class=int(classes[state]))
                for state in witness_states
            ],
        }
    return {
        "feature_name": feature_name,
        "cover_class_is_function_of_Bc_plus_feature": bool(not collisions),
        "collision_key_count": int(len(collisions)),
        "sample_collision": sample_collision,
    }


def _future_carry_signature_fn(
    m: int,
    next_map: Mapping[State, State],
    *,
    length: int,
) -> Callable[[State], Tuple[int, ...]]:
    @lru_cache(maxsize=None)
    def _signature(state: State) -> Tuple[int, ...]:
        out: List[int] = []
        cur: State | None = state
        for _ in range(length):
            if cur is None:
                out.append(-1)
            else:
                out.append(int(cur[0] == m - 1))
                cur = next_map.get(cur)
        return tuple(out)

    return _signature


def _time_to_next_carry_fn(m: int, next_map: Mapping[State, State]) -> Callable[[State], int | None]:
    @lru_cache(maxsize=None)
    def _ttnc(state: State | None) -> int | None:
        if state is None:
            return None
        if state[0] == m - 1:
            return 0
        nxt = next_map.get(state)
        value = _ttnc(nxt)
        return None if value is None else int(value + 1)

    return _ttnc


def _residual_two_sheet_summary(
    m: int,
    state_info: Mapping[State, Mapping[str, object]],
    next_map: Mapping[State, State],
    classes: Mapping[State, int],
) -> Dict[str, object]:
    buckets = _fiber_buckets(m, state_info, key_name="Bc")
    ambiguous = {
        key: states
        for key, states in buckets.items()
        if len({int(classes[state]) for state in states}) > 1
    }
    q_pair_counter: Counter[Tuple[int, ...]] = Counter(
        tuple(sorted({int(state[0]) for state in states}))
        for states in ambiguous.values()
    )

    q_eq_m_minus_2 = _feature_refines_cover_summary(
        m,
        state_info,
        classes,
        "1_{q=m-2}",
        lambda state: int(state[0] == m - 2),
    )
    future_window_summaries = {}
    minimal_future_window = None
    for length in range(1, SHORT_FUTURE_WINDOW_LIMIT + 1):
        summary = _feature_refines_cover_summary(
            m,
            state_info,
            classes,
            f"future_carry_window_{length}",
            _future_carry_signature_fn(m, next_map, length=length),
        )
        future_window_summaries[str(length)] = summary
    for length in range(1, 256):
        summary = _feature_refines_cover_summary(
            m,
            state_info,
            classes,
            f"future_carry_window_{length}",
            _future_carry_signature_fn(m, next_map, length=length),
        )
        if summary["cover_class_is_function_of_Bc_plus_feature"]:
            minimal_future_window = int(length)
            break
    time_to_next_carry = _time_to_next_carry_fn(m, next_map)
    time_to_next_carry_summary = _feature_refines_cover_summary(
        m,
        state_info,
        classes,
        "time_to_next_carry",
        time_to_next_carry,
    )

    def _normalized_subset(subset: Iterable[int]) -> List[int]:
        return [int(value) for value in subset]

    good_q_partitions: List[List[int]] = []
    for bits in product((0, 1), repeat=m - 1):
        bit_map = {0: 0}
        for q_value, bit in zip(range(1, m), bits):
            bit_map[int(q_value)] = int(bit)
        summary = _feature_refines_cover_summary(
            m,
            state_info,
            classes,
            "q_partition_bit",
            lambda state, bit_map=bit_map: int(bit_map[int(state[0])]),
        )
        if summary["cover_class_is_function_of_Bc_plus_feature"]:
            good_q_partitions.append(_normalized_subset(q for q, bit in bit_map.items() if bit))

    time_values = sorted(
        {
            int(time_to_next_carry(state))
            for states in ambiguous.values()
            for state in states
            if time_to_next_carry(state) is not None
        }
    )

    return {
        "ambiguous_key_count": int(len(ambiguous)),
        "support_is_regular_noncarry_only": bool(
            all(key[4] == "regular" and key[5] == 0 for key in ambiguous)
        ),
        "support_families": sorted({str(key[4]) for key in ambiguous}),
        "support_carry_values": sorted({int(key[5]) for key in ambiguous}),
        "support_layers_seen": sorted({int(key[3]) for key in ambiguous}),
        "q_value_pairs": [
            {"q_values": list(pair), "count": int(count)}
            for pair, count in q_pair_counter.most_common()
        ],
        "sample_ambiguous_keys": [
            {
                "Bc": list(key),
                "rows": [
                    _state_payload(state, state_info[state], cover_class=int(classes[state]))
                    for state in states
                ],
                "time_to_next_carry_values": [time_to_next_carry(state) for state in states],
            }
            for key, states in list(sorted(ambiguous.items(), key=lambda item: repr(item[0])))[:8]
        ],
        "candidate_feature_checks": {
            "q_eq_m_minus_2": q_eq_m_minus_2,
            "future_carry_windows": future_window_summaries,
            "minimal_future_carry_window_length": minimal_future_window,
            "time_to_next_carry": {
                **time_to_next_carry_summary,
                "value_range_on_ambiguous_support": [time_values[0], time_values[-1]] if time_values else [],
            },
            "q_only_binary_partition_search": {
                "solution_count": int(len(good_q_partitions)),
                "representative_solutions": good_q_partitions[:12],
            },
        },
    }


def _trigger_summary(
    m: int,
    rows: Sequence[Mapping[str, object]],
) -> Dict[str, object]:
    return {
        "w_formula_exact": bool(
            all(int(row["w"]) == (int(row["s"]) - int(row["u"])) % m for row in rows)
        ),
        "exceptional_fire_on_B": bool(
            carry042._collision_summary(rows, "B", "is_exceptional_target")["is_function_of_key"]
        ),
        "regular_fire_on_B": bool(
            carry042._collision_summary(rows, "B", "is_regular_target")["is_function_of_key"]
        ),
        "regular_fire_on_Bc": bool(
            carry042._collision_summary(rows, "Bc", "is_regular_target")["is_function_of_key"]
        ),
        "carry_is_function_of_B": bool(carry042._carry_summary(rows)["carry_is_function_of_B"]),
        "smallest_verified_trigger_coordinate": "B + 1_{q=m-1}",
        "admissible_realization_status": "open",
    }


def _per_m_analysis(m: int) -> Dict[str, object]:
    rows, state_info, next_map = _active_model(m)
    refinement_rounds, classes = _minimal_cover_classes(state_info, next_map)
    cover_over_B = _cover_summary_over_key(m, state_info, next_map, classes, key_name="B")
    cover_over_Bc = _cover_summary_over_key(m, state_info, next_map, classes, key_name="Bc")
    residual = _residual_two_sheet_summary(m, state_info, next_map, classes)
    return {
        "m": int(m),
        "trigger_level": _trigger_summary(m, rows),
        "minimal_cover_over_B": {
            "refinement_rounds": int(refinement_rounds),
            **cover_over_B,
        },
        "minimal_cover_over_Bc": {
            "refinement_rounds": int(refinement_rounds),
            **cover_over_Bc,
        },
        "residual_two_sheet": residual,
    }


def _analysis_summary(started: float, per_m: Mapping[str, object]) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "main_result": (
            "After the carry-slice split from 042, the checked active branch is best read as "
            "B = (s,u,v,layer,family), then B plus the carry bit c = 1_{q=m-1}, then a residual "
            "binary sheet over B plus c. On m = 5,7,9,11 the minimal deterministic cover over "
            "B plus c has fiber size exactly 2 at worst, and its support lies entirely on the "
            "regular noncarry branch. The residual sheet is not the obvious bit 1_{q=m-2} except "
            "in the m=5 pilot, and short future-carry windows do not coordinatize it on larger "
            "m. A theorem-friendly but nonlocal coordinatization does exist via time to next carry. "
            "So the clean D5 language is grouped base + carry sheet + residual binary noncarry sheet, "
            "while the clean next local branch is still admissible realization of the carry slice first."
        ),
        "per_m": {
            str(m): {
                "regular_fire_on_Bc": payload["trigger_level"]["regular_fire_on_Bc"],
                "max_cover_fiber_over_B": payload["minimal_cover_over_B"]["max_cover_fiber_size"],
                "max_cover_fiber_over_Bc": payload["minimal_cover_over_Bc"]["max_cover_fiber_size"],
                "residual_support_regular_noncarry_only": payload["residual_two_sheet"]["support_is_regular_noncarry_only"],
                "q_eq_m_minus_2_refines_cover": payload["residual_two_sheet"]["candidate_feature_checks"]["q_eq_m_minus_2"]["cover_class_is_function_of_Bc_plus_feature"],
                "minimal_future_carry_window_length": payload["residual_two_sheet"]["candidate_feature_checks"]["minimal_future_carry_window_length"],
                "time_to_next_carry_refines_cover": payload["residual_two_sheet"]["candidate_feature_checks"]["time_to_next_carry"]["cover_class_is_function_of_Bc_plus_feature"],
                "q_only_binary_partition_solution_count": payload["residual_two_sheet"]["candidate_feature_checks"]["q_only_binary_partition_search"]["solution_count"],
            }
            for m, payload in per_m.items()
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the D5 finite-cover picture beyond the carry slice.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    per_m = {str(m): _per_m_analysis(m) for m in ALL_M_VALUES}
    summary = _analysis_summary(started, per_m)

    _write_json(out_dir / "analysis_summary.json", summary)
    _write_json(
        out_dir / "carry_slice_realization_summary_043.json",
        {m: payload["trigger_level"] for m, payload in per_m.items()},
    )
    _write_json(
        out_dir / "finite_cover_transition_summary_043.json",
        {
            m: {
                "minimal_cover_over_B": payload["minimal_cover_over_B"],
                "minimal_cover_over_Bc": payload["minimal_cover_over_Bc"],
            }
            for m, payload in per_m.items()
        },
    )
    _write_json(
        out_dir / "residual_two_sheet_summary_043.json",
        {m: payload["residual_two_sheet"] for m, payload in per_m.items()},
    )
    _write_json(args.summary_out, summary)
    print(f"task_id: {TASK_ID}")
    print("extracted the residual finite-sheet structure beyond the carry slice on the D5 active branch.")


if __name__ == "__main__":
    main()
