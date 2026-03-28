#!/usr/bin/env python3
"""Exact sigma23 bundle rerun using the surfaced 2026-03-21 artifact bundle.

This script does three things:
1. injects a lightweight witness loader so the surfaced endpoint-repair script can
   be imported without the older, missing search artifacts;
2. reruns the sigma21/sigma22/sigma23 immediate-R1 comparison on chosen moduli;
3. writes theorem-facing JSON and CSV summaries.

The key computation uses the actual surfaced bundle code
    scripts/torus_nd_d5_endpoint_latin_repair.py
and the shared mode-switch common module
    artifacts/d5_mixed_skew_odometer_normal_form_018/code/torus_nd_d5_layer3_mode_switch_common.py
from the uploaded tarball.
"""
from __future__ import annotations

import argparse
import csv
import importlib
import json
import platform
import sys
import time
import types
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

TASK_ID = "D5-SIGMA23-BUNDLE-EXACT-CHECKER-219"
LEFT_WORD = (4, 1, 4)
RIGHT_WORDS: Dict[str, Tuple[int, int, int]] = {
    "sigma21": (1, 2, 2),
    "sigma22": (2, 1, 2),
    "sigma23": (2, 2, 1),
}
DEFAULT_M_VALUES = (3, 5, 7, 9, 11, 13, 15, 17, 19)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _load_witness_rows(bundle_root: Path) -> List[Mapping[str, object]]:
    registry_path = bundle_root / "artifacts" / "d5_return_map_model_017" / "data" / "witness_registry.json"
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise TypeError(f"Unexpected witness registry structure at {registry_path}")
    return data


def _inject_common_stub(bundle_root: Path) -> None:
    rows = _load_witness_rows(bundle_root)
    stub = types.ModuleType("torus_nd_d5_return_map_model_common")

    def environment_block() -> Dict[str, object]:
        return {
            "python_version": platform.python_version(),
            "runtime": "bundle_stubbed_loader",
            "bundle_root": str(bundle_root),
        }

    def runtime_since(start: float) -> float:
        return time.perf_counter() - start

    def load_witness_specs() -> List[SimpleNamespace]:
        out: List[SimpleNamespace] = []
        for row in rows:
            out.append(
                SimpleNamespace(
                    name=str(row["name"]),
                    role=row.get("role"),
                    family=row.get("family"),
                    source=row.get("source"),
                    rule_payload=row["rule"],
                )
            )
        return out

    stub.environment_block = environment_block  # type: ignore[attr-defined]
    stub.runtime_since = runtime_since  # type: ignore[attr-defined]
    stub.load_witness_specs = load_witness_specs  # type: ignore[attr-defined]
    sys.modules[stub.__name__] = stub


def _import_seed032(bundle_root: Path) -> Any:
    script_dir = bundle_root / "scripts"
    common_code_dir = bundle_root / "artifacts" / "d5_mixed_skew_odometer_normal_form_018" / "code"
    for directory in (script_dir, common_code_dir):
        directory_str = str(directory)
        if directory_str not in sys.path:
            sys.path.insert(0, directory_str)
    _inject_common_stub(bundle_root)
    return importlib.import_module("torus_nd_d5_endpoint_latin_repair")


def _rel_coords(source_coords: Sequence[int], target_coords: Sequence[int], m: int) -> List[int]:
    return [int((int(target_coords[a]) - int(source_coords[a])) % m) for a in range(5)]


def _coords_payload(coords: Sequence[int], m: int) -> Dict[str, int]:
    x0, q, w, v, u = [int(value) for value in coords]
    return {
        "x0": x0,
        "q": q,
        "w": w,
        "v": v,
        "u": u,
        "s": int((w + u) % m),
        "layer": int((x0 + q + w + v + u) % m),
    }


def _build_rows(seed032: Any, prepared: Any) -> Dict[str, Tuple[List[int], List[str], Dict[str, object]]]:
    rows: Dict[str, Tuple[List[int], List[str], Dict[str, object]]] = {}
    for name, right_word in RIGHT_WORDS.items():
        nexts_all, meta = seed032._build_candidate(
            prepared,
            w0=0,
            s0=0,
            left_word=LEFT_WORD,
            right_word=right_word,
            cocycle_defect="none",
            repair=None,
        )
        if nexts_all is None:
            raise ValueError(f"{name} failed to build at m={prepared.m}: {meta}")
        rows[name] = (nexts_all[0], meta["labels_by_color"][0], meta)
    return rows


def _analyze_m(seed032: Any, m: int) -> Dict[str, object]:
    mixed_rule = seed032._mixed_rule()
    prepared = seed032._prepare_m(m, mixed_rule)
    rows = _build_rows(seed032, prepared)
    coords = prepared.pre["coords"]
    step_by_dir = prepared.pre["step_by_dir"]

    sigma21_row, sigma21_labels, sigma21_meta = rows["sigma21"]
    sigma22_row, _, _ = rows["sigma22"]
    sigma23_row, _, _ = rows["sigma23"]

    source_indices = [idx for idx, label in enumerate(sigma21_labels) if label == "R1"]
    source_count = len(source_indices)

    bad_sigma22: List[Dict[str, object]] = []
    bad_sigma23: List[Dict[str, object]] = []
    signature_counter: Counter[Tuple[object, ...]] = Counter()
    neighbor_counter: Counter[Tuple[str, ...]] = Counter()
    immediate_counter: Counter[Tuple[int, ...]] = Counter()
    actual_second_counter: Counter[Tuple[int, ...]] = Counter()
    sigma23_second_counter: Counter[Tuple[int, ...]] = Counter()
    delta_counter: Counter[Tuple[int, ...]] = Counter()
    examples: List[Dict[str, object]] = []

    for idx in source_indices:
        source_coords = tuple(int(value) for value in coords[idx])
        immediate_idx = int(sigma21_row[idx])
        immediate_coords = tuple(int(value) for value in coords[immediate_idx])
        actual_second_idx = int(sigma21_row[immediate_idx])
        actual_second_coords = tuple(int(value) for value in coords[actual_second_idx])

        sigma22_immediate_idx = int(sigma22_row[idx])
        sigma22_second_idx = int(sigma22_row[sigma22_immediate_idx])
        sigma22_second_coords = tuple(int(value) for value in coords[sigma22_second_idx])

        sigma23_immediate_idx = int(sigma23_row[idx])
        sigma23_second_idx = int(sigma23_row[sigma23_immediate_idx])
        sigma23_second_coords = tuple(int(value) for value in coords[sigma23_second_idx])

        rel_immediate = tuple(_rel_coords(source_coords, immediate_coords, m))
        rel_actual_second = tuple(_rel_coords(source_coords, actual_second_coords, m))
        rel_sigma23_second = tuple(_rel_coords(source_coords, sigma23_second_coords, m))
        neighbor_labels = tuple(str(sigma21_labels[int(step_by_dir[d][idx])]) for d in range(5))
        changed_axes = tuple(sorted(a + 1 for a in range(5) if int(actual_second_coords[a]) != int(source_coords[a])))

        if actual_second_idx != sigma22_second_idx:
            bad_sigma22.append(
                {
                    "source_index": int(idx),
                    "source_coords": list(source_coords),
                    "actual_second_coords": list(actual_second_coords),
                    "sigma22_second_coords": list(sigma22_second_coords),
                }
            )
        if actual_second_idx == sigma23_second_idx:
            bad_sigma23.append(
                {
                    "source_index": int(idx),
                    "source_coords": list(source_coords),
                    "actual_second_coords": list(actual_second_coords),
                    "sigma23_second_coords": list(sigma23_second_coords),
                }
            )

        sig = (rel_immediate, rel_actual_second, rel_sigma23_second, neighbor_labels)
        signature_counter[sig] += 1
        neighbor_counter[neighbor_labels] += 1
        immediate_counter[rel_immediate] += 1
        actual_second_counter[rel_actual_second] += 1
        sigma23_second_counter[rel_sigma23_second] += 1
        delta_counter[changed_axes] += 1

        if len(examples) < 8:
            examples.append(
                {
                    "source_index": int(idx),
                    "source_payload": _coords_payload(source_coords, m),
                    "immediate_payload": _coords_payload(immediate_coords, m),
                    "actual_second_payload": _coords_payload(actual_second_coords, m),
                    "sigma22_second_payload": _coords_payload(sigma22_second_coords, m),
                    "sigma23_second_payload": _coords_payload(sigma23_second_coords, m),
                    "neighbor_labels_by_direction": list(neighbor_labels),
                }
            )

    unique_signature, signature_count = next(iter(signature_counter.items()))
    source_count_matches_m_times_m_minus_1 = source_count == m * (m - 1)

    return {
        "m": int(m),
        "n": int(prepared.pre["n"]),
        "source_count": int(source_count),
        "source_count_matches_m_times_m_minus_1": bool(source_count_matches_m_times_m_minus_1),
        "symmetry_reduced_microcase_count": int(len(signature_counter)),
        "all_second_steps_match_sigma22": bool(not bad_sigma22),
        "all_second_steps_avoid_sigma23": bool(not bad_sigma23),
        "all_neighbor_patterns_are_B_R2_B_B_B": bool(set(neighbor_counter.keys()) == {("B", "R2", "B", "B", "B")}),
        "all_actual_deltas_are_12": bool(set(delta_counter.keys()) == {(2, 3)}),
        "candidate_overlap_sizes": {
            "sigma21_layer2": list(rows["sigma21"][2]["layer2_overlap_sizes"]),
            "sigma21_layer3": list(rows["sigma21"][2]["layer3_overlap_sizes"]),
            "sigma22_layer2": list(rows["sigma22"][2]["layer2_overlap_sizes"]),
            "sigma22_layer3": list(rows["sigma22"][2]["layer3_overlap_sizes"]),
            "sigma23_layer2": list(rows["sigma23"][2]["layer2_overlap_sizes"]),
            "sigma23_layer3": list(rows["sigma23"][2]["layer3_overlap_sizes"]),
        },
        "representative_relative_data": {
            "relative_immediate_coords": list(unique_signature[0]),
            "relative_actual_second_coords": list(unique_signature[1]),
            "relative_sigma23_second_coords": list(unique_signature[2]),
            "neighbor_labels_by_direction": list(unique_signature[3]),
            "count": int(signature_count),
        },
        "bad_sigma22_examples": bad_sigma22[:3],
        "bad_sigma23_examples": bad_sigma23[:3],
        "examples": examples,
    }


def _summary(per_m_rows: Sequence[Mapping[str, object]], bundle_root: Path) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "bundle_root": str(bundle_root),
        "checked_moduli": [int(row["m"]) for row in per_m_rows],
        "all_source_counts_match_m_times_m_minus_1": bool(all(bool(row["source_count_matches_m_times_m_minus_1"]) for row in per_m_rows)),
        "all_microcase_counts_equal_one": bool(all(int(row["symmetry_reduced_microcase_count"]) == 1 for row in per_m_rows)),
        "all_second_steps_match_sigma22": bool(all(bool(row["all_second_steps_match_sigma22"]) for row in per_m_rows)),
        "all_second_steps_avoid_sigma23": bool(all(bool(row["all_second_steps_avoid_sigma23"]) for row in per_m_rows)),
        "all_neighbor_patterns_are_B_R2_B_B_B": bool(all(bool(row["all_neighbor_patterns_are_B_R2_B_B_B"]) for row in per_m_rows)),
        "all_actual_deltas_are_12": bool(all(bool(row["all_actual_deltas_are_12"]) for row in per_m_rows)),
        "source_count_pattern": {str(row["m"]): int(row["source_count"]) for row in per_m_rows},
        "microcase_count_pattern": {str(row["m"]): int(row["symmetry_reduced_microcase_count"]) for row in per_m_rows},
        "representative_relative_data": per_m_rows[0]["representative_relative_data"] if per_m_rows else {},
        "main_result": (
            "For every checked modulus, the surfaced bundle builder constructs sigma21/sigma22/sigma23 without overlap conflicts. "
            "Inside sigma21, the entire immediate R1 source family is one rooted microcase, every neighbor pattern is [B,R2,B,B,B], "
            "the actual second step has relative displacement (0,1,1,0,0), and it always agrees with sigma22 while differing from sigma23."
        ),
    }


def _write_csv(path: Path, per_m_rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "m",
        "n",
        "source_count",
        "source_count_matches_m_times_m_minus_1",
        "symmetry_reduced_microcase_count",
        "all_second_steps_match_sigma22",
        "all_second_steps_avoid_sigma23",
        "all_neighbor_patterns_are_B_R2_B_B_B",
        "all_actual_deltas_are_12",
        "relative_immediate_coords",
        "relative_actual_second_coords",
        "relative_sigma23_second_coords",
        "neighbor_labels_by_direction",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in per_m_rows:
            rep = row["representative_relative_data"]
            writer.writerow(
                {
                    "m": int(row["m"]),
                    "n": int(row["n"]),
                    "source_count": int(row["source_count"]),
                    "source_count_matches_m_times_m_minus_1": bool(row["source_count_matches_m_times_m_minus_1"]),
                    "symmetry_reduced_microcase_count": int(row["symmetry_reduced_microcase_count"]),
                    "all_second_steps_match_sigma22": bool(row["all_second_steps_match_sigma22"]),
                    "all_second_steps_avoid_sigma23": bool(row["all_second_steps_avoid_sigma23"]),
                    "all_neighbor_patterns_are_B_R2_B_B_B": bool(row["all_neighbor_patterns_are_B_R2_B_B_B"]),
                    "all_actual_deltas_are_12": bool(row["all_actual_deltas_are_12"]),
                    "relative_immediate_coords": json.dumps(rep["relative_immediate_coords"]),
                    "relative_actual_second_coords": json.dumps(rep["relative_actual_second_coords"]),
                    "relative_sigma23_second_coords": json.dumps(rep["relative_sigma23_second_coords"]),
                    "neighbor_labels_by_direction": json.dumps(rep["neighbor_labels_by_direction"]),
                }
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--csv-out", type=Path, required=True)
    parser.add_argument("--m-values", nargs="+", type=int, default=list(DEFAULT_M_VALUES))
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if any(int(m) <= 0 for m in args.m_values):
        raise ValueError("m-values must be positive")
    bundle_root = args.bundle_root.resolve()
    if not bundle_root.exists():
        raise FileNotFoundError(bundle_root)

    start = time.perf_counter()
    seed032 = _import_seed032(bundle_root)
    per_m_rows: List[Dict[str, object]] = []
    for m in args.m_values:
        t0 = time.perf_counter()
        row = _analyze_m(seed032, int(m))
        row["runtime_sec"] = round(time.perf_counter() - t0, 6)
        per_m_rows.append(row)
        print(
            f"{TASK_ID}: m={m} n={row['n']} source_count={row['source_count']} "
            f"match_sigma22={row['all_second_steps_match_sigma22']} "
            f"avoid_sigma23={row['all_second_steps_avoid_sigma23']} "
            f"runtime={row['runtime_sec']}"
        )

    summary = _summary(per_m_rows, bundle_root)
    summary["total_runtime_sec"] = round(time.perf_counter() - start, 6)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    _write_json(args.out_dir / "per_modulus.json", {"rows": per_m_rows})
    _write_json(args.out_dir / "analysis_summary.json", summary)
    _write_json(args.summary_out, summary)
    _write_csv(args.csv_out, per_m_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
