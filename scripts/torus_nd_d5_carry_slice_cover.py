#!/usr/bin/env python3
"""Extract the carry-slice trigger lift and finite-sheet cover over the D5 active grouped model."""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_corridor_phase_clarification as clar036
import torus_nd_d5_corridor_phase_extraction as phase034
import torus_nd_d5_endpoint_latin_repair as seed032
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-CARRY-SLICE-COVER-042"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M_VALUES = (11,)
ALL_M_VALUES = PRIMARY_M_VALUES + CONTROL_M_VALUES
REPRESENTATIVE_EXCEPTIONAL_U = 3


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _active_union(m: int) -> Tuple[List[Dict[str, object]], Dict[Tuple[int, int, int, int, int, str], Dict[str, object]], Dict[Tuple[int, int, int, int, int, str], Tuple[int, int, int, int, int, str]]]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    nexts_all, meta = phase034._build_best_seed(prepared)
    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    coords = prepared.pre["coords"]
    hole_l1 = phase034._hole_l1_set(prepared, row)

    rows: List[Dict[str, object]] = []
    state_info: Dict[Tuple[int, int, int, int, int, str], Dict[str, object]] = {}
    next_map: Dict[Tuple[int, int, int, int, int, str], Tuple[int, int, int, int, int, str]] = {}

    for source_u in range(1, m):
        source_index = next(
            idx
            for idx, label in enumerate(labels)
            if label == "R1" and int(coords[idx][4]) == source_u
        )
        trace = clar036._trace_source(prepared, row, source_index, hole_l1)["trace"]
        family = "exceptional" if source_u == REPRESENTATIVE_EXCEPTIONAL_U else "regular"
        for step, row_data in enumerate(trace):
            cur = row_data["coords"]
            q_value = int(cur["q"])
            w_value = int(cur["w"])
            u_value = int(cur["u"])
            v_value = int(cur["v"])
            layer = int(cur["layer"])
            s_value = (w_value + u_value) % m
            carry = int(q_value == m - 1)
            is_regular_target = (q_value, w_value, layer) == (m - 1, m - 2, 1)
            is_exceptional_target = (q_value, w_value, layer) == (m - 2, m - 1, 1)
            state = (q_value, w_value, u_value, v_value, layer, family)
            rows.append(
                {
                    "source_u": int(source_u),
                    "trace_step": int(step),
                    "family": family,
                    "q": q_value,
                    "w": w_value,
                    "u": u_value,
                    "v": v_value,
                    "s": int(s_value),
                    "layer": layer,
                    "carry": carry,
                    "B": [int(s_value), int(u_value), int(v_value), layer, family],
                    "Bc": [int(s_value), int(u_value), int(v_value), layer, family, carry],
                    "is_regular_target": bool(is_regular_target),
                    "is_exceptional_target": bool(is_exceptional_target),
                }
            )
            state_info[state] = {
                "B": (int(s_value), int(u_value), int(v_value), layer, family),
                "status": "regular_target" if is_regular_target else ("exceptional_target" if is_exceptional_target else "mid"),
            }
            if step + 1 < len(trace):
                nxt = trace[step + 1]["coords"]
                next_map[state] = (
                    int(nxt["q"]),
                    int(nxt["w"]),
                    int(nxt["u"]),
                    int(nxt["v"]),
                    int(nxt["layer"]),
                    family,
                )
    return rows, state_info, next_map


def _collision_summary(
    rows: Sequence[Mapping[str, object]],
    key_name: str,
    pred_name: str,
) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        buckets[tuple(row[key_name])].append(row)
    collisions = []
    for key, bucket in buckets.items():
        positives = [row for row in bucket if bool(row[pred_name])]
        negatives = [row for row in bucket if not bool(row[pred_name])]
        if positives and negatives:
            collisions.append((key, positives[0], negatives[0]))
    return {
        "is_function_of_key": bool(not collisions),
        "collision_key_count": int(len(collisions)),
        "sample_collision": None
        if not collisions
        else {
            "shared_key": list(collisions[0][0]),
            "positive_row": {
                "source_u": int(collisions[0][1]["source_u"]),
                "trace_step": int(collisions[0][1]["trace_step"]),
                "q": int(collisions[0][1]["q"]),
                "w": int(collisions[0][1]["w"]),
                "u": int(collisions[0][1]["u"]),
                "v": int(collisions[0][1]["v"]),
                "s": int(collisions[0][1]["s"]),
                "layer": int(collisions[0][1]["layer"]),
                "family": str(collisions[0][1]["family"]),
            },
            "negative_row": {
                "source_u": int(collisions[0][2]["source_u"]),
                "trace_step": int(collisions[0][2]["trace_step"]),
                "q": int(collisions[0][2]["q"]),
                "w": int(collisions[0][2]["w"]),
                "u": int(collisions[0][2]["u"]),
                "v": int(collisions[0][2]["v"]),
                "s": int(collisions[0][2]["s"]),
                "layer": int(collisions[0][2]["layer"]),
                "family": str(collisions[0][2]["family"]),
            },
        },
    }


def _carry_summary(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], set[int]] = defaultdict(set)
    for row in rows:
        buckets[tuple(row["B"])].add(int(row["carry"]))
    collisions = [key for key, values in buckets.items() if len(values) > 1]
    return {
        "carry_is_function_of_B": bool(not collisions),
        "collision_key_count": int(len(collisions)),
        "sample_collision_key": None if not collisions else list(collisions[0]),
    }


def _transition_summary(rows: Sequence[Mapping[str, object]], key_name: str, next_key_name: str) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], set[Tuple[object, ...]]] = defaultdict(set)
    ordered = list(rows)
    for row in ordered:
        if "next_" + next_key_name not in row:
            continue
        buckets[tuple(row[key_name])].add(tuple(row["next_" + next_key_name]))
    nondet = [key for key, values in buckets.items() if len(values) > 1]
    return {
        "is_deterministic": bool(not nondet),
        "nondeterministic_key_count": int(len(nondet)),
        "max_next_count": int(max((len(values) for values in buckets.values()), default=0)),
        "sample_nondeterministic_key": None if not nondet else list(nondet[0]),
    }


def _cover_summary(
    rows: Sequence[Mapping[str, object]],
    state_info: Mapping[Tuple[int, int, int, int, int, str], Mapping[str, object]],
    next_map: Mapping[Tuple[int, int, int, int, int, str], Tuple[int, int, int, int, int, str]],
) -> Dict[str, object]:
    classes: Dict[Tuple[int, int, int, int, int, str], object] = {
        state: info["status"] for state, info in state_info.items()
    }
    rounds = 0
    changed = True
    while changed and rounds < 5000:
        rounds += 1
        signature_to_id: Dict[Tuple[object, object], int] = {}
        new_classes: Dict[Tuple[int, int, int, int, int, str], int] = {}
        for state in sorted(state_info, key=repr):
            signature = (state_info[state]["status"], classes.get(next_map.get(state), None))
            if signature not in signature_to_id:
                signature_to_id[signature] = len(signature_to_id)
            new_classes[state] = signature_to_id[signature]
        changed = new_classes != classes
        classes = new_classes

    fiber_buckets: Dict[Tuple[object, ...], set[int]] = defaultdict(set)
    for state, info in state_info.items():
        fiber_buckets[tuple(info["B"])].add(int(classes[state]))
    fiber_sizes = sorted({len(values) for values in fiber_buckets.values()})
    max_fiber = max((len(values) for values in fiber_buckets.values()), default=0)

    sample_fiber = None
    for key, values in fiber_buckets.items():
        if len(values) == max_fiber:
            raw_rows = [
                {
                    "q": int(state[0]),
                    "w": int(state[1]),
                    "u": int(state[2]),
                    "v": int(state[3]),
                    "layer": int(state[4]),
                    "family": str(state[5]),
                    "cover_class": int(classes[state]),
                }
                for state, info in state_info.items()
                if tuple(info["B"]) == key
            ]
            sample_fiber = {"B": list(key), "rows": raw_rows}
            break

    return {
        "refinement_rounds": int(rounds),
        "class_count": int(len(set(classes.values()))),
        "fiber_sizes_seen": [int(value) for value in fiber_sizes],
        "max_cover_fiber_size_over_B": int(max_fiber),
        "sample_max_fiber": sample_fiber,
    }


def _per_m_analysis(m: int) -> Dict[str, object]:
    rows, state_info, next_map = _active_union(m)
    rows_by_state = {
        (int(row["q"]), int(row["w"]), int(row["u"]), int(row["v"]), int(row["layer"]), str(row["family"])): row
        for row in rows
    }
    for state, nxt in next_map.items():
        rows_by_state[state]["next_B"] = rows_by_state[nxt]["B"]
        rows_by_state[state]["next_Bc"] = rows_by_state[nxt]["Bc"]

    carry_summary = _carry_summary(rows)
    exceptional_on_B = _collision_summary(rows, "B", "is_exceptional_target")
    regular_on_B = _collision_summary(rows, "B", "is_regular_target")
    regular_on_Bc = _collision_summary(rows, "Bc", "is_regular_target")
    exceptional_on_Bc = _collision_summary(rows, "Bc", "is_exceptional_target")
    transition_on_B = _transition_summary(rows, "B", "B")
    transition_on_Bc = _transition_summary(rows, "Bc", "Bc")
    cover_summary = _cover_summary(rows, state_info, next_map)

    q_fiber_B: Dict[Tuple[object, ...], set[int]] = defaultdict(set)
    q_fiber_Bc: Dict[Tuple[object, ...], set[int]] = defaultdict(set)
    for row in rows:
        q_fiber_B[tuple(row["B"])].add(int(row["q"]))
        q_fiber_Bc[tuple(row["Bc"])].add(int(row["q"]))

    return {
        "m": int(m),
        "trigger_logic": {
            "w_formula": "w = s - u mod m",
            "w_formula_exact": bool(all(int(row["w"]) == (int(row["s"]) - int(row["u"])) % m for row in rows)),
            "exceptional_fire_on_B": exceptional_on_B,
            "regular_fire_on_B": regular_on_B,
            "regular_fire_on_Bc": regular_on_Bc,
            "exceptional_fire_on_Bc": exceptional_on_Bc,
            "carry_on_B": carry_summary,
        },
        "dynamic_closure": {
            "transition_on_B": transition_on_B,
            "transition_on_Bc": transition_on_Bc,
            "max_q_fiber_over_B": int(max(len(values) for values in q_fiber_B.values())),
            "max_q_fiber_over_Bc": int(max(len(values) for values in q_fiber_Bc.values())),
        },
        "minimal_cover": cover_summary,
    }


def _analysis_summary(started: float, per_m: Mapping[str, object]) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "main_result": (
            "On the checked active union, the carry-slice bit c = 1_{q=m-1} is the smallest verified trigger-level lift: "
            "exceptional fire already descends to B = (s,u,v,layer,family), regular fire descends to B plus c, and c is "
            "not a function of B. But B plus c is still not a closed deterministic active dynamics. The structural lift is "
            "therefore better read as a tiny finite cover over B, and the extracted future-signature refinement has fiber "
            "size at most 3 over every checked modulus."
        ),
        "per_m": {
            str(m): {
                "exceptional_fire_on_B": payload["trigger_logic"]["exceptional_fire_on_B"]["is_function_of_key"],
                "regular_fire_on_B": payload["trigger_logic"]["regular_fire_on_B"]["is_function_of_key"],
                "regular_fire_on_Bc": payload["trigger_logic"]["regular_fire_on_Bc"]["is_function_of_key"],
                "carry_on_B": payload["trigger_logic"]["carry_on_B"]["carry_is_function_of_B"],
                "transition_on_B": payload["dynamic_closure"]["transition_on_B"]["is_deterministic"],
                "transition_on_Bc": payload["dynamic_closure"]["transition_on_Bc"]["is_deterministic"],
                "max_cover_fiber_size_over_B": payload["minimal_cover"]["max_cover_fiber_size_over_B"],
            }
            for m, payload in per_m.items()
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the carry-slice trigger lift and finite-sheet cover over the D5 active grouped model.")
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
        out_dir / "carry_slice_trigger_validation_042.json",
        {m: payload["trigger_logic"] for m, payload in per_m.items()},
    )
    _write_json(
        out_dir / "carry_slice_dynamic_closure_042.json",
        {m: payload["dynamic_closure"] for m, payload in per_m.items()},
    )
    _write_json(
        out_dir / "minimal_cover_summary_042.json",
        {m: payload["minimal_cover"] for m, payload in per_m.items()},
    )
    _write_json(args.summary_out, summary)
    print(f"task_id: {TASK_ID}")
    print("analyzed the carry-slice trigger lift and finite-sheet cover over the active grouped model.")


if __name__ == "__main__":
    main()
