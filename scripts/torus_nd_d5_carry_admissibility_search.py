#!/usr/bin/env python3
"""Search the first admissible lifted families for exact realization of the D5 carry slice."""

from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import time
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import torus_nd_d5_corridor_phase_extraction as phase034
import torus_nd_d5_endpoint_latin_repair as seed032
import torus_nd_d5_coordinate_exposure_admissibility as coord041
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-CARRY-ADMISSIBILITY-SEARCH-045"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M_VALUES = (11,)
ALL_M_VALUES = PRIMARY_M_VALUES + CONTROL_M_VALUES
REPRESENTATIVE_EXCEPTIONAL_U = 3

CATALOG_DEFS = (
    {
        "name": "core_transition",
        "description": "current-edge / 1-step / 2-step transition features built from labels, layers, and grouped deltas",
        "feature_names": (
            "label",
            "pred_label",
            "succ_label",
            "layer",
            "next_layer",
            "dn",
            "next_dn",
        ),
        "max_size": 5,
    },
    {
        "name": "gauge_transition_basis",
        "description": "core transition features plus a low-cardinality 025-style tau/edge anchored gauge basis on current and next grouped states",
        "feature_names": (
            "label",
            "pred_label",
            "succ_label",
            "layer",
            "next_layer",
            "dn",
            "next_dn",
            "cur:diag_omit.tau_lo",
            "nxt:diag_omit.tau_lo",
            "dlt:diag_omit.tau_lo",
            "cur:diag_omit.tau_hi",
            "nxt:diag_omit.tau_hi",
            "dlt:diag_omit.tau_hi",
            "cur:diag_omit.edge_pair",
            "nxt:diag_omit.edge_pair",
            "dlt:diag_omit.edge_pair",
            "cur:antidiag_omit.tau_lo",
            "nxt:antidiag_omit.tau_lo",
            "dlt:antidiag_omit.tau_lo",
            "cur:antidiag_omit.tau_hi",
            "nxt:antidiag_omit.tau_hi",
            "dlt:antidiag_omit.tau_hi",
            "cur:antidiag_omit.edge_pair",
            "nxt:antidiag_omit.edge_pair",
            "dlt:antidiag_omit.edge_pair",
        ),
        "max_size": 5,
    },
    {
        "name": "point_defect_basis",
        "description": "targeted binary defect bits from the 025 representatives, combined with the smallest transition data",
        "feature_names": (
            "layer",
            "dn",
            "cur:diag_omit.point_left",
            "nxt:diag_omit.point_left",
            "dlt:diag_omit.point_left",
            "cur:diag_omit.point_right",
            "nxt:diag_omit.point_right",
            "dlt:diag_omit.point_right",
            "cur:antidiag_omit.point_left",
            "nxt:antidiag_omit.point_left",
            "dlt:antidiag_omit.point_left",
            "cur:antidiag_omit.point_right",
            "nxt:antidiag_omit.point_right",
            "dlt:antidiag_omit.point_right",
        ),
        "max_size": 4,
    },
)

EncodedRow = Tuple[Tuple[int, ...], int, Tuple[int, ...]]
_WORKER_CATALOG_ROWS: Mapping[int, Sequence[EncodedRow]] | None = None


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _frozen_rows_for_m(m: int) -> List[Dict[str, object]]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    nexts_all, meta = phase034._build_best_seed(prepared)
    row = nexts_all[0]
    inv_row = [0] * len(row)
    for idx, nxt in enumerate(row):
        inv_row[nxt] = idx

    labels = meta["labels_by_color"][0]
    coords = prepared.pre["coords"]
    step_by_dir = prepared.pre["step_by_dir"]
    hole_l1 = phase034._hole_l1_set(prepared, row)
    feature_maps = coord041._base_feature_catalog(m)

    rows: List[Dict[str, object]] = []
    seen_states = set()
    for source_u in range(1, m):
        source_index = next(
            idx
            for idx, label in enumerate(labels)
            if label == "R1" and int(coords[idx][4]) == source_u
        )
        family = "exceptional" if source_u == REPRESENTATIVE_EXCEPTIONAL_U else "regular"
        current = step_by_dir[2][source_index]
        trace_step = 0
        while current not in seen_states:
            seen_states.add(current)
            q_value, w_value, v_value, u_value = [int(value) for value in coords[current][1:5]]
            layer = int(coords[current][0])
            s_value = (w_value + u_value) % m

            nxt = row[current]
            q_next, w_next, v_next, u_next = [int(value) for value in coords[nxt][1:5]]
            layer_next = int(coords[nxt][0])
            s_next = (w_next + u_next) % m

            nxt2 = row[nxt]
            q_next2, w_next2, v_next2, u_next2 = [int(value) for value in coords[nxt2][1:5]]
            layer_next2 = int(coords[nxt2][0])
            s_next2 = (w_next2 + u_next2) % m

            dn = (
                (s_next - s_value) % m,
                (u_next - u_value) % m,
                (v_next - v_value) % m,
                (layer_next - layer) % m,
            )
            next_dn = (
                (s_next2 - s_next) % m,
                (u_next2 - u_next) % m,
                (v_next2 - v_next) % m,
                (layer_next2 - layer_next) % m,
            )

            first_carry_index = current
            while int(coords[first_carry_index][1]) != m - 1:
                first_carry_index = row[first_carry_index]
            next_carry_u = int(coords[first_carry_index][4])
            d_value = int(next_carry_u >= m - 3)

            current_grouped = (s_value, u_value)
            next_grouped = (s_next, u_next)

            feature_values: Dict[str, object] = {
                "label": labels[current],
                "pred_label": labels[inv_row[current]],
                "succ_label": labels[nxt],
                "layer": int(layer),
                "next_layer": int(layer_next),
                "dn": [int(value) for value in dn],
                "next_dn": [int(value) for value in next_dn],
            }
            for name, mapping in feature_maps.items():
                cur_value = mapping[current_grouped]
                next_value = mapping[next_grouped]
                if isinstance(cur_value, int):
                    delta_value = int((next_value - cur_value) % m)
                else:
                    delta_value = int(next_value != cur_value)
                feature_values[f"cur:{name}"] = int(cur_value)
                feature_values[f"nxt:{name}"] = int(next_value)
                feature_values[f"dlt:{name}"] = int(delta_value)

            exit_dirs = [
                int(direction)
                for direction in range(5)
                if step_by_dir[direction][current] in hole_l1
            ]
            rows.append(
                {
                    "m": int(m),
                    "source_u": int(source_u),
                    "trace_step": int(trace_step),
                    "family": family,
                    "state_index": int(current),
                    "q": int(q_value),
                    "w": int(w_value),
                    "u": int(u_value),
                    "v": int(v_value),
                    "s": int(s_value),
                    "layer": int(layer),
                    "B": [int(s_value), int(u_value), int(v_value), int(layer), family],
                    "B_next": [int(s_next), int(u_next), int(v_next), int(layer_next), family],
                    "B_next2": [int(s_next2), int(u_next2), int(v_next2), int(layer_next2), family],
                    "dn": [int(value) for value in dn],
                    "next_dn": [int(value) for value in next_dn],
                    "c": int(q_value == m - 1),
                    "d": int(d_value),
                    "next_carry_u": int(next_carry_u),
                    "is_regular_target": bool((q_value, w_value, layer) == (m - 1, m - 2, 1)),
                    "is_exceptional_target": bool((q_value, w_value, layer) == (m - 2, m - 1, 1)),
                    "label": str(labels[current]),
                    "pred_label": str(labels[inv_row[current]]),
                    "succ_label": str(labels[nxt]),
                    "exit_dirs": exit_dirs,
                    "feature_values": feature_values,
                }
            )
            trace_step += 1
            if exit_dirs:
                break
            current = row[current]
    return rows


def _bucket_error_profile(rows: Sequence[Mapping[str, object]], key_getter) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        buckets[key_getter(row)].append(row)

    collision_key_count = 0
    false_pos = 0
    false_neg = 0
    error_rows: List[Mapping[str, object]] = []
    distinguishing_B_fiber_count = 0

    by_B_feature_values: Dict[Tuple[object, ...], set[Tuple[object, ...]]] = defaultdict(set)
    for key, bucket in buckets.items():
        b_key = tuple(row_key for row_key in bucket[0]["B"])
        by_B_feature_values[b_key].add(tuple(key[1:]))
        counts = Counter(int(row["c"]) for row in bucket)
        if len(counts) > 1:
            collision_key_count += 1
        predicted = 1 if counts[1] > counts[0] else 0
        for row in bucket:
            actual = int(row["c"])
            if actual != predicted:
                error_rows.append(row)
                if predicted == 1:
                    false_pos += 1
                else:
                    false_neg += 1
    distinguishing_B_fiber_count = sum(1 for values in by_B_feature_values.values() if len(values) > 1)

    return {
        "distinct_key_count": int(len(buckets)),
        "collision_key_count": int(collision_key_count),
        "false_pos": int(false_pos),
        "false_neg": int(false_neg),
        "total_errors": int(false_pos + false_neg),
        "is_exact": bool(collision_key_count == 0),
        "distinguishes_B_fibers": bool(distinguishing_B_fiber_count > 0),
        "distinguishing_B_fiber_count": int(distinguishing_B_fiber_count),
        "error_rows": error_rows,
    }


def _freeze_key_part(value: object) -> object:
    if isinstance(value, list):
        return tuple(_freeze_key_part(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_key_part(item) for item in value)
    if isinstance(value, dict):
        return tuple(sorted((str(key), _freeze_key_part(item)) for key, item in value.items()))
    return value


def _family_code(family: object) -> int:
    return 1 if str(family) == "exceptional" else 0


def _encode_B_key(values: Sequence[object]) -> Tuple[int, ...]:
    return (
        int(values[0]),
        int(values[1]),
        int(values[2]),
        int(values[3]),
        _family_code(values[4]),
    )


def _encode_catalog_rows(
    rows_by_m: Mapping[int, Sequence[Mapping[str, object]]],
    feature_names: Sequence[str],
) -> Dict[int, List[EncodedRow]]:
    encoders = {name: {} for name in feature_names}
    out: Dict[int, List[EncodedRow]] = {}
    for m in ALL_M_VALUES:
        encoded_rows: List[EncodedRow] = []
        for row in rows_by_m[m]:
            encoded_feature_values = []
            for name in feature_names:
                frozen = _freeze_key_part(row["feature_values"][name])
                mapping = encoders[name]
                code = mapping.get(frozen)
                if code is None:
                    code = len(mapping)
                    mapping[frozen] = code
                encoded_feature_values.append(int(code))
            encoded_rows.append(
                (
                    _encode_B_key(row["B"]),
                    int(row["c"]),
                    tuple(encoded_feature_values),
                )
            )
        out[m] = encoded_rows
    return out


def _fast_bucket_error_profile(
    rows: Sequence[EncodedRow],
    combo_indices: Sequence[int],
) -> Dict[str, object]:
    buckets: Dict[Tuple[int, ...], List[int]] = {}
    by_B_feature_values: Dict[Tuple[int, ...], set[Tuple[int, ...]]] = defaultdict(set)

    for base_key, carry, feature_values in rows:
        feature_slice = tuple(feature_values[index] for index in combo_indices)
        key = base_key + feature_slice
        counts = buckets.get(key)
        if counts is None:
            counts = [0, 0]
            buckets[key] = counts
        counts[carry] += 1
        by_B_feature_values[base_key].add(feature_slice)

    collision_key_count = 0
    false_pos = 0
    false_neg = 0
    for counts in buckets.values():
        count0, count1 = int(counts[0]), int(counts[1])
        if count0 and count1:
            collision_key_count += 1
        if count1 > count0:
            false_pos += count0
        else:
            false_neg += count1

    distinguishing_B_fiber_count = sum(1 for values in by_B_feature_values.values() if len(values) > 1)
    return {
        "distinct_key_count": int(len(buckets)),
        "collision_key_count": int(collision_key_count),
        "false_pos": int(false_pos),
        "false_neg": int(false_neg),
        "total_errors": int(false_pos + false_neg),
        "is_exact": bool(collision_key_count == 0),
        "distinguishes_B_fibers": bool(distinguishing_B_fiber_count > 0),
        "distinguishing_B_fiber_count": int(distinguishing_B_fiber_count),
    }


def _init_catalog_worker(catalog_rows: Mapping[int, Sequence[EncodedRow]]) -> None:
    global _WORKER_CATALOG_ROWS
    _WORKER_CATALOG_ROWS = catalog_rows


def _evaluate_combo_chunk(combo_chunk: Sequence[Tuple[int, ...]]) -> List[Dict[str, object]]:
    assert _WORKER_CATALOG_ROWS is not None
    out: List[Dict[str, object]] = []
    for combo_indices in combo_chunk:
        per_m = {}
        exact_all = True
        total_errors = 0
        collision_count = 0
        for m in ALL_M_VALUES:
            summary = _fast_bucket_error_profile(_WORKER_CATALOG_ROWS[m], combo_indices)
            per_m[str(m)] = summary
            total_errors += int(summary["total_errors"])
            collision_count += int(summary["collision_key_count"])
            if not summary["is_exact"]:
                exact_all = False
        out.append(
            {
                "combo_indices": [int(index) for index in combo_indices],
                "per_m": per_m,
                "exact_all_m": bool(exact_all),
                "score": {
                    "total_errors": int(total_errors),
                    "collision_key_count": int(collision_count),
                },
            }
        )
    return out


def _chunked(values: Sequence[Tuple[int, ...]], chunk_size: int) -> Iterable[List[Tuple[int, ...]]]:
    for index in range(0, len(values), chunk_size):
        yield list(values[index : index + chunk_size])


def _error_support_profile(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    family_counts = Counter(str(row["family"]) for row in rows)
    layer_counts = Counter(int(row["layer"]) for row in rows)
    carry_counts = Counter(int(row["c"]) for row in rows)
    label_counts = Counter(str(row["label"]) for row in rows)
    return {
        "error_row_count": int(len(rows)),
        "family_counts": {str(key): int(value) for key, value in sorted(family_counts.items())},
        "carry_counts": {str(key): int(value) for key, value in sorted(carry_counts.items())},
        "layer_counts": {str(key): int(value) for key, value in sorted(layer_counts.items())},
        "label_counts_top10": [
            {"label": str(label), "count": int(count)}
            for label, count in label_counts.most_common(10)
        ],
    }


def _search_catalog(
    rows_by_m: Mapping[int, Sequence[Mapping[str, object]]],
    *,
    catalog_name: str,
    feature_names: Sequence[str],
    max_size: int,
    workers: int,
    chunk_size: int,
) -> Dict[str, object]:
    tested = 0
    positives: List[Dict[str, object]] = []
    best_by_size: Dict[int, Dict[str, object]] = {}

    feature_name_list = list(feature_names)
    combo_records: List[Tuple[int, ...]] = []
    for size in range(1, max_size + 1):
        combo_records.extend(combinations(range(len(feature_name_list)), size))
    tested = len(combo_records)
    encoded_rows = _encode_catalog_rows(rows_by_m, feature_name_list)

    def _consume_result(result: Mapping[str, object]) -> None:
        combo_indices = tuple(int(index) for index in result["combo_indices"])
        combo = tuple(feature_name_list[index] for index in combo_indices)
        candidate = {
            "catalog": catalog_name,
            "feature_names": list(combo),
            "size": int(len(combo)),
            "exact_all_m": bool(result["exact_all_m"]),
            "per_m": result["per_m"],
            "score": result["score"],
        }
        if candidate["exact_all_m"]:
            positives.append(candidate)
        best = best_by_size.get(len(combo))
        candidate_rank = (
            int(candidate["score"]["total_errors"]),
            int(candidate["score"]["collision_key_count"]),
            int(candidate["size"]),
            tuple(candidate["feature_names"]),
        )
        if best is None:
            best_by_size[len(combo)] = candidate
            return
        best_rank = (
            int(best["score"]["total_errors"]),
            int(best["score"]["collision_key_count"]),
            int(best["size"]),
            tuple(best["feature_names"]),
        )
        if candidate_rank < best_rank:
            best_by_size[len(combo)] = candidate

    if workers <= 1:
        _init_catalog_worker(encoded_rows)
        for chunk in _chunked(combo_records, chunk_size):
            for result in _evaluate_combo_chunk(chunk):
                _consume_result(result)
    else:
        with mp.Pool(processes=workers, initializer=_init_catalog_worker, initargs=(encoded_rows,)) as pool:
            for chunk_result in pool.imap_unordered(
                _evaluate_combo_chunk,
                _chunked(combo_records, chunk_size),
                chunksize=1,
            ):
                for result in chunk_result:
                    _consume_result(result)

    best_candidates = [best_by_size[size] for size in sorted(best_by_size)]
    return {
        "catalog_name": catalog_name,
        "feature_names": list(feature_names),
        "max_size": int(max_size),
        "tested_candidate_count": int(tested),
        "positive_candidate_count": int(len(positives)),
        "positive_candidates": positives[:20],
        "best_candidates_by_size": best_candidates,
    }


def _named_family_checks(rows_by_m: Mapping[int, Sequence[Mapping[str, object]]]) -> Dict[str, object]:
    named_defs = {
        "B_only": lambda row: tuple(row["B"]),
        "B_next": lambda row: tuple(row["B"]) + tuple(row["B_next"]),
        "B_next_next2": lambda row: tuple(row["B"]) + tuple(row["B_next"]) + tuple(row["B_next2"]),
        "B_plus_dn": lambda row: tuple(row["B"]) + tuple(row["dn"]),
        "B_plus_next_dn": lambda row: tuple(row["B"]) + tuple(row["next_dn"]),
        "B_plus_dn_next_dn": lambda row: tuple(row["B"]) + tuple(row["dn"]) + tuple(row["next_dn"]),
        "B_plus_pure_carry_delta_indicator": lambda row: tuple(row["B"]) + (int(tuple(row["dn"]) == (1, 0, 0, 1)),),
    }
    out = {}
    for name, key_getter in named_defs.items():
        per_m = {}
        for m in ALL_M_VALUES:
            summary = _bucket_error_profile(rows_by_m[m], key_getter)
            per_m[str(m)] = {
                key: value
                for key, value in summary.items()
                if key != "error_rows"
            }
        out[name] = {
            "per_m": per_m,
            "exact_all_m": bool(all(per_m[str(m)]["is_exact"] for m in ALL_M_VALUES)),
        }
    return out


def _analysis_summary(started: float, per_catalog: Mapping[str, object], named_checks: Mapping[str, object]) -> Dict[str, object]:
    core = per_catalog["core_transition"]
    gauge = per_catalog["gauge_transition_basis"]
    point = per_catalog["point_defect_basis"]
    return {
        "task_id": TASK_ID,
        "main_result": (
            "No exact admissible carry family was found in the first carry-only search catalogs on the checked active branch. "
            "In particular, no candidate survives in the core edge/transition catalog up to size 5, none survives in the low-cardinality "
            "tau/edge anchored gauge-transition catalog up to size 5, and none survives in the targeted point-defect catalog up to size 4. "
            "Full B->B_next and B->B_next->B_next2 grouped transition classes also fail. So after 044, the next missing admissibility datum "
            "is sharper than current edge, 1-step transition, 2-step transition, or low-cardinality anchored cocycle bits; the branch is pruned "
            "through those families and points to a broader lifted gauge or deeper transition sheet."
        ),
        "catalog_summary": {
            name: {
                "tested_candidate_count": payload["tested_candidate_count"],
                "positive_candidate_count": payload["positive_candidate_count"],
            }
            for name, payload in per_catalog.items()
        },
        "named_family_status": {
            name: payload["exact_all_m"]
            for name, payload in named_checks.items()
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Search the first admissible lifted families for exact realization of the D5 carry slice.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=min(32, mp.cpu_count()))
    parser.add_argument("--chunk-size", type=int, default=256)
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    rows_by_m = {m: _frozen_rows_for_m(m) for m in ALL_M_VALUES}
    frozen_dataset = {str(m): rows_by_m[m] for m in ALL_M_VALUES}

    per_catalog = {}
    for catalog in CATALOG_DEFS:
        per_catalog[catalog["name"]] = _search_catalog(
            rows_by_m,
            catalog_name=str(catalog["name"]),
            feature_names=tuple(str(name) for name in catalog["feature_names"]),
            max_size=int(catalog["max_size"]),
            workers=max(1, int(args.workers)),
            chunk_size=max(1, int(args.chunk_size)),
        )

    named_checks = _named_family_checks(rows_by_m)
    summary = _analysis_summary(started, per_catalog, named_checks)

    collision_profiles = {}
    support_profiles = {}
    for catalog_name, payload in per_catalog.items():
        collision_profiles[catalog_name] = []
        support_profiles[catalog_name] = []
        for candidate in payload["best_candidates_by_size"]:
            feature_names = tuple(candidate["feature_names"])
            per_m_profiles = {}
            per_m_support = {}
            for m in ALL_M_VALUES:
                profile = _bucket_error_profile(
                    rows_by_m[m],
                    lambda row, feature_names=feature_names: tuple(row["B"]) + tuple(
                        _freeze_key_part(row["feature_values"][name]) for name in feature_names
                    ),
                )
                per_m_profiles[str(m)] = {
                    key: value
                    for key, value in profile.items()
                    if key != "error_rows"
                }
                per_m_support[str(m)] = _error_support_profile(profile["error_rows"])
            collision_profiles[catalog_name].append(
                {
                    "feature_names": list(feature_names),
                    "size": int(candidate["size"]),
                    "per_m": per_m_profiles,
                }
            )
            support_profiles[catalog_name].append(
                {
                    "feature_names": list(feature_names),
                    "size": int(candidate["size"]),
                    "per_m": per_m_support,
                }
            )

    exact_positive = []
    for payload in per_catalog.values():
        exact_positive.extend(payload["positive_candidates"])

    obstruction = {
        "next_missing_admissibility_datum": "broader lifted gauge or deeper-than-2-step transition sheet",
        "killed_families": [
            "current-edge / label / delta core catalog up to size 5",
            "1-step and 2-step grouped transition signatures in the core catalog up to size 5",
            "low-cardinality tau/edge anchored gauge-transition catalog up to size 5",
            "targeted point-defect anchored catalog up to size 4",
            "full B->B_next and B->B_next->B_next2 grouped transition classes",
        ],
        "reason": (
            "No exact carry family appears in the first admissible edge / transition / anchored-gauge catalogs, "
            "so the carry slice is not exposed by current B, current edge labels, 1-step grouped transition, "
            "2-step grouped transition, or the first low-cardinality 025-style cocycle bits."
        ),
    }

    _write_json(out_dir / "analysis_summary.json", summary)
    _write_json(out_dir / "frozen_active_carry_dataset_045.json", frozen_dataset)
    _write_json(
        out_dir / "candidate_family_catalog_045.json",
        {
            "catalogs": list(CATALOG_DEFS),
            "named_family_checks": named_checks,
        },
    )
    _write_json(out_dir / "carry_realization_search_summary_045.json", per_catalog)
    _write_json(
        out_dir / "carry_exactness_tables_045.json",
        {
            "named_family_checks": named_checks,
            "best_candidates_by_catalog": {
                name: payload["best_candidates_by_size"]
                for name, payload in per_catalog.items()
            },
        },
    )
    _write_json(out_dir / "carry_collision_profiles_045.json", collision_profiles)
    _write_json(out_dir / "carry_support_profiles_045.json", support_profiles)
    _write_json(
        out_dir / "minimal_positive_carry_family_045.json",
        {"positive_candidates": exact_positive[:20], "positive_candidate_count": int(len(exact_positive))},
    )
    _write_json(out_dir / "exact_obstruction_summary_045.json", obstruction)
    _write_json(args.summary_out, summary)
    print(f"task_id: {TASK_ID}")
    print("searched the first admissible carry-only families on the checked D5 active branch.")


if __name__ == "__main__":
    main()
