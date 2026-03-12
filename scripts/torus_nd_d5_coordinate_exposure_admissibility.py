#!/usr/bin/env python3
"""Test the first admissible coordinate-surrogate families for the D5 best-seed branch."""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, Sequence, Tuple

import torus_nd_d5_corridor_phase_clarification as clar036
import torus_nd_d5_corridor_phase_extraction as phase034
import torus_nd_d5_endpoint_latin_repair as seed032
import torus_nd_d5_omit_base_cocycle_defect as defect025
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-COORDINATE-EXPOSURE-ADMISSIBILITY-041"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M_VALUES = (11,)
ALL_M_VALUES = PRIMARY_M_VALUES + CONTROL_M_VALUES
REPRESENTATIVE_EXCEPTIONAL_U = 3

OMIT_BASES = (
    {"name": "diag_omit", "slope": 1, "intercept": 0, "defect_row": 0},
    {"name": "antidiag_omit", "slope": -1, "intercept": 0, "defect_row": 0},
)
DEFECT_NAMES = ("point_left", "point_right", "edge_pair", "defect_row", "graph")


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _active_rows(m: int) -> List[Dict[str, object]]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    nexts_all, meta = phase034._build_best_seed(prepared)
    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    coords = prepared.pre["coords"]
    hole_l1 = phase034._hole_l1_set(prepared, row)

    out: List[Dict[str, object]] = []
    for source_u in range(1, m):
        source_index = next(
            idx
            for idx, label in enumerate(labels)
            if label == "R1" and int(coords[idx][4]) == source_u
        )
        trace = clar036._trace_source(prepared, row, source_index, hole_l1)["trace"]
        family = "exceptional" if source_u == REPRESENTATIVE_EXCEPTIONAL_U else "regular"
        for trace_step, row_data in enumerate(trace):
            cur = row_data["coords"]
            q_value = int(cur["q"])
            w_value = int(cur["w"])
            v_value = int(cur["v"])
            u_value = int(cur["u"])
            layer = int(cur["layer"])
            s_value = (w_value + u_value) % m
            out.append(
                {
                    "source_u": int(source_u),
                    "family": family,
                    "trace_step": int(trace_step),
                    "q": q_value,
                    "w": w_value,
                    "u": u_value,
                    "v": v_value,
                    "s": int(s_value),
                    "layer": layer,
                    "grouped_state": [int(s_value), int(u_value), int(v_value)],
                    "is_regular_target": bool((q_value, w_value, layer) == (m - 1, m - 2, 1)),
                    "is_exceptional_target": bool((q_value, w_value, layer) == (m - 2, m - 1, 1)),
                }
            )
    return out


def _orbit_gauge(m: int, *, slope: int, intercept: int, defect_row: int) -> Dict[str, Dict[Tuple[int, int], int]]:
    start = (defect_row % m, defect025._graph_value(slope, intercept, defect_row, m))
    orbit: List[Tuple[int, int]] = []
    position: Dict[Tuple[int, int], int] = {}
    cur = start
    while cur not in position:
        position[cur] = len(orbit)
        orbit.append(cur)
        cur = defect025._base_next(
            cur[0],
            cur[1],
            m=m,
            slope=slope,
            intercept=intercept,
            defect_row=defect_row,
        )
    if len(orbit) != m * m or cur != start:
        raise ValueError(f"unexpected omit-base orbit for m={m}")

    tau_lo: Dict[Tuple[int, int], int] = {}
    tau_hi: Dict[Tuple[int, int], int] = {}
    cocycles: Dict[str, Dict[Tuple[int, int], int]] = {name: {} for name in DEFECT_NAMES}
    counts = {name: 0 for name in DEFECT_NAMES}

    for idx, state in enumerate(orbit):
        tau_lo[state] = idx % m
        tau_hi[state] = idx // m
        s_value, u_value = state
        for name in DEFECT_NAMES:
            cocycles[name][state] = counts[name] % m
        for name in DEFECT_NAMES:
            if defect025._in_defect(
                name,
                s=s_value,
                u=u_value,
                m=m,
                slope=slope,
                intercept=intercept,
                defect_row=defect_row,
            ):
                counts[name] += 1

    return {
        "tau_lo": tau_lo,
        "tau_hi": tau_hi,
        **cocycles,
    }


def _base_feature_catalog(m: int) -> Dict[str, Dict[Tuple[int, int], int]]:
    out: Dict[str, Dict[Tuple[int, int], int]] = {}
    for base in OMIT_BASES:
        name = str(base["name"])
        gauge = _orbit_gauge(
            m,
            slope=int(base["slope"]),
            intercept=int(base["intercept"]),
            defect_row=int(base["defect_row"]),
        )
        for feature_name, mapping in gauge.items():
            out[f"{name}.{feature_name}"] = mapping
    return out


def _predicate_summary(
    rows: Sequence[Mapping[str, object]],
    key_fn: Callable[[Mapping[str, object]], Tuple[object, ...]],
    pred_fn: Callable[[Mapping[str, object]], bool],
) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], set[bool]] = defaultdict(set)
    for row in rows:
        buckets[key_fn(row)].add(bool(pred_fn(row)))
    collision_keys = [key for key, values in buckets.items() if values == {False, True}]
    return {
        "is_function_of_key": bool(not collision_keys),
        "collision_key_count": int(len(collision_keys)),
        "distinct_key_count": int(len(buckets)),
        "sample_collision_keys": [list(key) for key in collision_keys[:10]],
    }


def _label_summary(
    rows: Sequence[Mapping[str, object]],
    key_fn: Callable[[Mapping[str, object]], Tuple[object, ...]],
    label_fn: Callable[[Mapping[str, object]], str],
) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], set[str]] = defaultdict(set)
    for row in rows:
        buckets[key_fn(row)].add(label_fn(row))
    collision_keys = [key for key, values in buckets.items() if len(values) > 1]
    return {
        "is_function_of_key": bool(not collision_keys),
        "collision_key_count": int(len(collision_keys)),
        "distinct_key_count": int(len(buckets)),
        "sample_collision_keys": [list(key) for key in collision_keys[:10]],
    }


def _grouped_key(row: Mapping[str, object]) -> Tuple[int, int, int]:
    return (int(row["s"]), int(row["u"]), int(row["v"]))


def _grouped_family_key(row: Mapping[str, object]) -> Tuple[object, ...]:
    return _grouped_key(row) + (str(row["family"]),)


def _feature_key(
    row: Mapping[str, object],
    feature_names: Sequence[str],
    feature_maps: Mapping[str, Dict[Tuple[int, int], int]],
) -> Tuple[object, ...]:
    s_value = int(row["s"])
    u_value = int(row["u"])
    key: List[object] = [int(s_value), int(u_value), int(row["v"])]
    for name in feature_names:
        key.append(int(feature_maps[name][(s_value, u_value)]))
    return tuple(key)


def _feature_family_summary(
    rows: Sequence[Mapping[str, object]],
    feature_names: Sequence[str],
    feature_maps: Mapping[str, Dict[Tuple[int, int], int]],
) -> Dict[str, object]:
    key_fn = lambda row: _feature_key(row, feature_names, feature_maps)
    key_family_fn = lambda row: _feature_key(row, feature_names, feature_maps) + (str(row["family"]),)
    return {
        "feature_names": list(feature_names),
        "family_label": _label_summary(rows, key_fn, lambda row: str(row["family"])),
        "regular_target_given_family": _predicate_summary(
            rows,
            key_family_fn,
            lambda row: bool(row["is_regular_target"]),
        ),
        "exceptional_target_given_family": _predicate_summary(
            rows,
            key_family_fn,
            lambda row: bool(row["is_exceptional_target"]),
        ),
    }


def _collision_examples(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    grouped_family_buckets: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    grouped_buckets: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        grouped_buckets[_grouped_key(row)].append(row)
        grouped_family_buckets[_grouped_family_key(row)].append(row)

    def _first_collision(
        buckets: Mapping[Tuple[object, ...], List[Mapping[str, object]]],
        pred_name: str,
    ) -> Dict[str, object] | None:
        for key, values in buckets.items():
            positives = [row for row in values if bool(row[pred_name])]
            negatives = [row for row in values if not bool(row[pred_name])]
            if positives and negatives:
                pos = positives[0]
                neg = negatives[0]
                return {
                    "shared_key": list(key),
                    "positive_row": {
                        "source_u": int(pos["source_u"]),
                        "trace_step": int(pos["trace_step"]),
                        "q": int(pos["q"]),
                        "w": int(pos["w"]),
                        "u": int(pos["u"]),
                        "v": int(pos["v"]),
                        "s": int(pos["s"]),
                        "layer": int(pos["layer"]),
                        "family": str(pos["family"]),
                    },
                    "negative_row": {
                        "source_u": int(neg["source_u"]),
                        "trace_step": int(neg["trace_step"]),
                        "q": int(neg["q"]),
                        "w": int(neg["w"]),
                        "u": int(neg["u"]),
                        "v": int(neg["v"]),
                        "s": int(neg["s"]),
                        "layer": int(neg["layer"]),
                        "family": str(neg["family"]),
                    },
                }
        return None

    return {
        "family_on_grouped_state": _first_collision(grouped_buckets, "is_exceptional_target"),
        "regular_target_given_family_on_grouped_state": _first_collision(grouped_family_buckets, "is_regular_target"),
        "exceptional_target_given_family_on_grouped_state": _first_collision(grouped_family_buckets, "is_exceptional_target"),
    }


def _per_m_analysis(m: int) -> Dict[str, object]:
    rows = _active_rows(m)
    feature_maps = _base_feature_catalog(m)

    grouped_state_summary = {
        "w_affine_formula_exact": bool(all(int(row["w"]) == (int(row["s"]) - int(row["u"])) % m for row in rows)),
        "family_label": _label_summary(rows, _grouped_key, lambda row: str(row["family"])),
        "regular_target_given_family": _predicate_summary(
            rows,
            _grouped_family_key,
            lambda row: bool(row["is_regular_target"]),
        ),
        "exceptional_target_given_family": _predicate_summary(
            rows,
            _grouped_family_key,
            lambda row: bool(row["is_exceptional_target"]),
        ),
    }

    tested_feature_families = [
        ("diag_base_gauge", ("diag_omit.tau_lo", "diag_omit.tau_hi")),
        ("diag_point_cocycles", ("diag_omit.point_left", "diag_omit.point_right", "diag_omit.edge_pair")),
        ("diag_extended", ("diag_omit.tau_lo", "diag_omit.tau_hi", "diag_omit.point_left", "diag_omit.point_right", "diag_omit.edge_pair")),
        ("antidiag_base_gauge", ("antidiag_omit.tau_lo", "antidiag_omit.tau_hi")),
        ("antidiag_point_cocycles", ("antidiag_omit.point_left", "antidiag_omit.point_right", "antidiag_omit.edge_pair")),
        ("both_extended", (
            "diag_omit.tau_lo",
            "diag_omit.tau_hi",
            "diag_omit.point_left",
            "diag_omit.point_right",
            "diag_omit.edge_pair",
            "antidiag_omit.tau_lo",
            "antidiag_omit.tau_hi",
            "antidiag_omit.point_left",
            "antidiag_omit.point_right",
            "antidiag_omit.edge_pair",
        )),
    ]

    family_rows = {
        name: _feature_family_summary(rows, feature_names, feature_maps)
        for name, feature_names in tested_feature_families
    }

    # These families all descend to the current grouped state, so the collision counts must match.
    grouped_regular_collisions = int(grouped_state_summary["regular_target_given_family"]["collision_key_count"])
    grouped_exceptional_collisions = int(grouped_state_summary["exceptional_target_given_family"]["collision_key_count"])
    grouped_family_collisions = int(grouped_state_summary["family_label"]["collision_key_count"])
    all_match_grouped = all(
        int(payload["regular_target_given_family"]["collision_key_count"]) == grouped_regular_collisions
        and int(payload["exceptional_target_given_family"]["collision_key_count"]) == grouped_exceptional_collisions
        and int(payload["family_label"]["collision_key_count"]) == grouped_family_collisions
        for payload in family_rows.values()
    )

    reduced_coordinate_predicates = {
        "w_formula": "w = s - u mod m",
        "raw_birth_formulas_from_039": {
            "source": "layer=1, q=m-1, w=0, u!=0",
            "exceptional_source": "layer=1, q=m-1, w=0, u=3",
            "entry": "layer=2, q=m-1, w=1, u!=0",
            "exceptional_entry": "layer=2, q=m-1, w=1, u=3",
        },
        "active_fire_targets_from_040": {
            "regular": [m - 1, m - 2, 1],
            "exceptional": [m - 2, m - 1, 1],
        },
    }

    obstruction = {
        "grouped_state_descending_observables_fail": bool(
            grouped_regular_collisions > 0 or grouped_exceptional_collisions > 0
        ),
        "all_tested_025_style_families_match_grouped_collision_counts": bool(all_match_grouped),
        "exact_missing_ingredient": (
            "one lifted coordinate not determined by the current grouped state (s,u,v), "
            "equivalently a pre-grouped phase / q-like coordinate or an explicit transported marker"
        ),
        "collision_examples": _collision_examples(rows),
    }

    return {
        "m": int(m),
        "reduced_coordinate_predicates": reduced_coordinate_predicates,
        "grouped_state_summary": grouped_state_summary,
        "tested_families": family_rows,
        "obstruction": obstruction,
    }


def _analysis_summary(started: float, per_m: Mapping[str, object]) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "main_result": (
            "The first admissible coordinate-surrogate families suggested by the 025 reduced class "
            "still do not realize the needed fire predicates. On the traced active union, w already "
            "collapses exactly to s-u, but the regular and exceptional fire predicates are not "
            "functions of the current grouped state (s,u,v), even after conditioning on the carried "
            "family bit. Gauge-fixed omit-base base coordinates and edge-tied point cocycles do not "
            "change that, because they still descend to the same current grouped state. So the exact "
            "missing admissibility ingredient is one lifted coordinate beyond current grouped state."
        ),
        "per_m": {
            str(m): {
                "w_affine_formula_exact": payload["grouped_state_summary"]["w_affine_formula_exact"],
                "family_on_grouped_state": payload["grouped_state_summary"]["family_label"]["is_function_of_key"],
                "regular_target_given_family_on_grouped_state": payload["grouped_state_summary"]["regular_target_given_family"]["is_function_of_key"],
                "exceptional_target_given_family_on_grouped_state": payload["grouped_state_summary"]["exceptional_target_given_family"]["is_function_of_key"],
                "all_tested_025_style_families_match_grouped_collision_counts": payload["obstruction"]["all_tested_025_style_families_match_grouped_collision_counts"],
            }
            for m, payload in per_m.items()
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze admissibility of grouped-state coordinate surrogates for the D5 best-seed branch.")
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
        out_dir / "reduced_coordinate_predicates_041.json",
        {m: payload["reduced_coordinate_predicates"] for m, payload in per_m.items()},
    )
    _write_json(
        out_dir / "admissible_observable_catalog_041.json",
        {
            m: {
                "grouped_state_summary": payload["grouped_state_summary"],
                "tested_families": payload["tested_families"],
            }
            for m, payload in per_m.items()
        },
    )
    _write_json(
        out_dir / "coordinate_exposure_validation_041.json",
        {
            m: {
                "grouped_state_summary": payload["grouped_state_summary"],
                "tested_families": payload["tested_families"],
            }
            for m, payload in per_m.items()
        },
    )
    _write_json(
        out_dir / "coordinate_admissibility_obstruction_041.json",
        {m: payload["obstruction"] for m, payload in per_m.items()},
    )
    _write_json(args.summary_out, summary)
    print(f"task_id: {TASK_ID}")
    print("analyzed first 025-style grouped-state-descending admissibility families.")


if __name__ == "__main__":
    main()
