#!/usr/bin/env python3
"""Extract the D5 carry-sheet plus binary-anticipation-cover normal form."""

from __future__ import annotations

import argparse
import json
import time
from functools import lru_cache
from pathlib import Path
from typing import Callable, Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_finite_cover_admissibility as finite043
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-CARRY-AND-FINITE-COVER-044"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M_VALUES = (11,)
ALL_M_VALUES = PRIMARY_M_VALUES + CONTROL_M_VALUES

State = finite043.State


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _feature_summary(
    m: int,
    state_info: Mapping[State, Mapping[str, object]],
    classes: Mapping[State, int],
    feature_name: str,
    feature_fn: Callable[[State], object],
) -> Dict[str, object]:
    summary = finite043._feature_refines_cover_summary(m, state_info, classes, feature_name, feature_fn)
    return {
        "feature_name": summary["feature_name"],
        "cover_class_is_function_of_Bc_plus_feature": summary["cover_class_is_function_of_Bc_plus_feature"],
        "collision_key_count": summary["collision_key_count"],
        "sample_collision": summary["sample_collision"],
    }


def _transition_on_feature(
    m: int,
    state_info: Mapping[State, Mapping[str, object]],
    next_map: Mapping[State, State],
    feature_fn: Callable[[State], object],
) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], set[Tuple[object, ...]]] = {}
    nondeterministic: List[Tuple[object, ...]] = []
    for state, nxt in next_map.items():
        key = finite043._bc_key(m, state, state_info[state]) + (feature_fn(state),)
        next_key = finite043._bc_key(m, nxt, state_info[nxt]) + (feature_fn(nxt),)
        values = buckets.setdefault(key, set())
        values.add(next_key)
    for key, values in buckets.items():
        if len(values) > 1:
            nondeterministic.append(key)
    return {
        "is_deterministic": bool(not nondeterministic),
        "nondeterministic_key_count": int(len(nondeterministic)),
        "sample_nondeterministic_key": None if not nondeterministic else list(nondeterministic[0]),
    }


def _analysis_for_m(m: int) -> Dict[str, object]:
    rows, state_info, next_map = finite043._active_model(m)
    _, classes = finite043._minimal_cover_classes(state_info, next_map)
    buckets = finite043._fiber_buckets(m, state_info, key_name="Bc")
    ambiguous = {
        key: states
        for key, states in buckets.items()
        if len({int(classes[state]) for state in states}) > 1
    }

    @lru_cache(maxsize=None)
    def _first_carry(state: State) -> State | None:
        cur: State | None = state
        while cur is not None and cur[0] != m - 1:
            cur = next_map.get(cur)
        return cur

    def _first_carry_state(state: State) -> object:
        return _first_carry(state)

    def _first_carry_B(state: State) -> object:
        first = _first_carry(state)
        return None if first is None else finite043._b_key(state_info[first])

    def _first_carry_u(state: State) -> object:
        first = _first_carry(state)
        return None if first is None else int(first[2])

    def _first_carry_s(state: State) -> object:
        first = _first_carry(state)
        return None if first is None else int(finite043._b_key(state_info[first])[0])

    def _time_to_next_carry(state: State) -> object:
        first = _first_carry(state)
        if first is None:
            return None
        steps = 0
        cur = state
        while cur != first:
            cur = next_map[cur]
            steps += 1
        return int(steps)

    def _anticipation_bit(state: State) -> int:
        first = _first_carry(state)
        if first is None:
            return 0
        return int(int(first[2]) >= m - 3)

    first_carry_summaries = {
        "first_carry_state": _feature_summary(m, state_info, classes, "first_carry_state", _first_carry_state),
        "first_carry_B": _feature_summary(m, state_info, classes, "first_carry_B", _first_carry_B),
        "first_carry_u": _feature_summary(m, state_info, classes, "first_carry_u", _first_carry_u),
        "first_carry_s": _feature_summary(m, state_info, classes, "first_carry_s", _first_carry_s),
        "time_to_next_carry": _feature_summary(m, state_info, classes, "time_to_next_carry", _time_to_next_carry),
        "anticipation_bit": _feature_summary(
            m,
            state_info,
            classes,
            "1_{next carry u >= m-3}",
            _anticipation_bit,
        ),
    }

    carry_trigger_status = {
        "exceptional_fire_on_B": bool(
            finite043.carry042._collision_summary(rows, "B", "is_exceptional_target")["is_function_of_key"]
        ),
        "regular_fire_on_B": bool(
            finite043.carry042._collision_summary(rows, "B", "is_regular_target")["is_function_of_key"]
        ),
        "regular_fire_on_Bc": bool(
            finite043.carry042._collision_summary(rows, "Bc", "is_regular_target")["is_function_of_key"]
        ),
        "transition_on_Bc_is_deterministic": bool(
            finite043.carry042._transition_summary(rows, "Bc", "Bc")["is_deterministic"]
        ),
        "admissible_carry_realization_status": "open",
        "recommended_local_target": "c = 1_{q=m-1}",
    }

    anticipation_support_rows = []
    next_carry_u_values = set()
    next_carry_s_values = set()
    next_carry_u_pairs: Dict[Tuple[int, ...], int] = {}
    next_carry_s_pairs: Dict[Tuple[int, ...], int] = {}
    for key, states in ambiguous.items():
        pair_u = tuple(sorted(int(_first_carry_u(state)) for state in states))
        pair_s = tuple(sorted(int(_first_carry_s(state)) for state in states))
        next_carry_u_pairs[pair_u] = int(next_carry_u_pairs.get(pair_u, 0) + 1)
        next_carry_s_pairs[pair_s] = int(next_carry_s_pairs.get(pair_s, 0) + 1)
        next_carry_u_values.update(pair_u)
        next_carry_s_values.update(pair_s)
        if len(anticipation_support_rows) < 8:
            anticipation_support_rows.append(
                {
                    "Bc": list(key),
                    "rows": [
                        {
                            **finite043._state_payload(state, state_info[state], cover_class=int(classes[state])),
                            "next_carry_B": list(_first_carry_B(state)),
                            "next_carry_u": int(_first_carry_u(state)),
                            "next_carry_s": int(_first_carry_s(state)),
                            "anticipation_bit": int(_anticipation_bit(state)),
                        }
                        for state in states
                    ],
                }
            )

    anticipation_support = {
        "ambiguous_key_count": int(len(ambiguous)),
        "support_is_regular_noncarry_only": bool(
            all(key[4] == "regular" and key[5] == 0 for key in ambiguous)
        ),
        "carry_states_are_singleton_over_Bc": bool(
            all(len(states) == 1 for key, states in buckets.items() if key[5] == 1)
        ),
        "allowed_next_carry_u_values_on_ambiguous_support": [int(value) for value in sorted(next_carry_u_values)],
        "allowed_next_carry_s_values_on_ambiguous_support": [int(value) for value in sorted(next_carry_s_values)],
        "next_carry_u_pair_counts": [
            {"u_values": list(pair), "count": int(count)}
            for pair, count in sorted(next_carry_u_pairs.items())
        ],
        "next_carry_s_pair_counts": [
            {"s_values": list(pair), "count": int(count)}
            for pair, count in sorted(next_carry_s_pairs.items())
        ],
        "sample_rows": anticipation_support_rows,
    }

    normal_form = {
        "base": "B = (s,u,v,layer,family)",
        "carry_sheet": "c = 1_{q=m-1}",
        "binary_anticipation_sheet": "d = 1_{next carry u >= m-3}",
        "exceptional_fire_on_B": carry_trigger_status["exceptional_fire_on_B"],
        "regular_fire_on_Bc": carry_trigger_status["regular_fire_on_Bc"],
        "transition_on_Bc_plus_d": _transition_on_feature(m, state_info, next_map, _anticipation_bit),
        "support_statement": "d is needed only on regular noncarry states on the checked active union",
    }

    return {
        "m": int(m),
        "carry_trigger_status": carry_trigger_status,
        "finite_cover_normal_form": normal_form,
        "next_carry_coordinatization": first_carry_summaries,
        "binary_anticipation_sheet": anticipation_support,
    }


def _analysis_summary(started: float, per_m: Mapping[str, object]) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "main_result": (
            "The 043 finite-cover picture sharpens to a clean checked normal form: "
            "on m = 5,7,9,11 the best-seed active branch factors as B <- B+c <- B+c+d, "
            "where c = 1_{q=m-1} is the exact trigger lift and d can be chosen as the "
            "binary anticipation bit 1_{next carry u >= m-3}. The residual sheet is needed "
            "only on regular noncarry states, carry states are singleton over B+c, and "
            "the transition law closes deterministically on B+c+d. So the theorem branch is "
            "now a grouped base plus carry sheet plus binary anticipation cover, while the "
            "next local branch should still target admissible realization of the carry sheet first."
        ),
        "per_m": {
            str(m): {
                "regular_fire_on_Bc": payload["carry_trigger_status"]["regular_fire_on_Bc"],
                "transition_on_Bc_is_deterministic": payload["carry_trigger_status"]["transition_on_Bc_is_deterministic"],
                "anticipation_bit_refines_cover": payload["next_carry_coordinatization"]["anticipation_bit"]["cover_class_is_function_of_Bc_plus_feature"],
                "carry_states_are_singleton_over_Bc": payload["binary_anticipation_sheet"]["carry_states_are_singleton_over_Bc"],
                "allowed_next_carry_u_values_on_ambiguous_support": payload["binary_anticipation_sheet"]["allowed_next_carry_u_values_on_ambiguous_support"],
            }
            for m, payload in per_m.items()
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the D5 carry-sheet plus binary-anticipation normal form.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    per_m = {str(m): _analysis_for_m(m) for m in ALL_M_VALUES}
    summary = _analysis_summary(started, per_m)

    _write_json(out_dir / "analysis_summary.json", summary)
    _write_json(
        out_dir / "carry_target_status_044.json",
        {m: payload["carry_trigger_status"] for m, payload in per_m.items()},
    )
    _write_json(
        out_dir / "finite_cover_normal_form_044.json",
        {m: payload["finite_cover_normal_form"] for m, payload in per_m.items()},
    )
    _write_json(
        out_dir / "next_carry_coordinatization_044.json",
        {m: payload["next_carry_coordinatization"] for m, payload in per_m.items()},
    )
    _write_json(
        out_dir / "binary_anticipation_sheet_044.json",
        {m: payload["binary_anticipation_sheet"] for m, payload in per_m.items()},
    )
    _write_json(args.summary_out, summary)
    print(f"task_id: {TASK_ID}")
    print("extracted the D5 carry-sheet plus binary-anticipation finite-cover normal form.")


if __name__ == "__main__":
    main()
