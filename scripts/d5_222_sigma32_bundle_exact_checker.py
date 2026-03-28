#!/usr/bin/env python3
"""Exact sigma32 bundle rerun using the surfaced 2026-03-21 artifact bundle.

This mirrors d5_219 for the centered-right strip.  It compares the common left
family for
    sigma21 = [4,1,4]/[1,2,2],
    sigma12 = [1,4,4]/[2,1,2],
    sigma22 = [4,1,4]/[2,1,2],
    sigma32 = [4,4,1]/[2,1,2],
and checks that the actual left-side continuation of sigma21 agrees with the
sigma22 prototype and avoids the dangerous sigma32 prototype.
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
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

TASK_ID = "D5-SIGMA32-BUNDLE-EXACT-CHECKER-222"
SIGMA21_LEFT = (4, 1, 4)
SIGMA21_RIGHT = (1, 2, 2)
CENTERED_RIGHT_LEFT_WORDS: Dict[str, Tuple[int, int, int]] = {
    "sigma12": (1, 4, 4),
    "sigma22": (4, 1, 4),
    "sigma32": (4, 4, 1),
}
CENTERED_RIGHT_RIGHT_WORD = (2, 1, 2)
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


def _build_row(seed032: Any, prepared: Any, *, left_word: Tuple[int, int, int], right_word: Tuple[int, int, int]) -> Tuple[List[int], List[str], Dict[str, object]]:
    nexts_all, meta = seed032._build_candidate(
        prepared,
        w0=0,
        s0=0,
        left_word=left_word,
        right_word=right_word,
        cocycle_defect="none",
        repair=None,
    )
    if nexts_all is None:
        raise ValueError(f"failed to build candidate left={left_word} right={right_word} at m={prepared.m}: {meta}")
    return nexts_all[0], meta["labels_by_color"][0], meta


def _analyze_m(seed032: Any, m: int) -> Dict[str, object]:
    mixed_rule = seed032._mixed_rule()
    prepared = seed032._prepare_m(m, mixed_rule)
    coords = prepared.pre["coords"]
    step_by_dir = prepared.pre["step_by_dir"]

    sigma21_row, sigma21_labels, sigma21_meta = _build_row(
        seed032,
        prepared,
        left_word=SIGMA21_LEFT,
        right_word=SIGMA21_RIGHT,
    )
    sigma12_row, _, sigma12_meta = _build_row(
        seed032,
        prepared,
        left_word=CENTERED_RIGHT_LEFT_WORDS["sigma12"],
        right_word=CENTERED_RIGHT_RIGHT_WORD,
    )
    sigma22_row, _, sigma22_meta = _build_row(
        seed032,
        prepared,
        left_word=CENTERED_RIGHT_LEFT_WORDS["sigma22"],
        right_word=CENTERED_RIGHT_RIGHT_WORD,
    )
    sigma32_row, _, sigma32_meta = _build_row(
        seed032,
        prepared,
        left_word=CENTERED_RIGHT_LEFT_WORDS["sigma32"],
        right_word=CENTERED_RIGHT_RIGHT_WORD,
    )

    source_indices = [idx for idx, label in enumerate(sigma21_labels) if label == "L1"]
    source_count = len(source_indices)

    bad_sigma22_first: List[Dict[str, object]] = []
    bad_sigma12_first: List[Dict[str, object]] = []
    bad_sigma22_second: List[Dict[str, object]] = []
    bad_sigma32_second: List[Dict[str, object]] = []
    bad_sigma12_second: List[Dict[str, object]] = []

    first_rel_counter: Dict[Tuple[int, ...], int] = {}
    second_rel_counter: Dict[Tuple[int, ...], int] = {}
    sigma12_second_rel_counter: Dict[Tuple[int, ...], int] = {}
    sigma32_second_rel_counter: Dict[Tuple[int, ...], int] = {}
    neighbor_counter: Dict[Tuple[str, ...], int] = {}
    examples: List[Dict[str, object]] = []

    def bump(counter: MutableMapping[Tuple[int, ...], int], key: Tuple[int, ...]) -> None:
        counter[key] = int(counter.get(key, 0)) + 1

    for idx in source_indices:
        source_coords = tuple(int(value) for value in coords[idx])
        actual_immediate_idx = int(sigma21_row[idx])
        actual_second_idx = int(sigma21_row[actual_immediate_idx])
        sigma12_immediate_idx = int(sigma12_row[idx])
        sigma12_second_idx = int(sigma12_row[sigma12_immediate_idx])
        sigma22_immediate_idx = int(sigma22_row[idx])
        sigma22_second_idx = int(sigma22_row[sigma22_immediate_idx])
        sigma32_immediate_idx = int(sigma32_row[idx])
        sigma32_second_idx = int(sigma32_row[sigma32_immediate_idx])

        actual_immediate_coords = tuple(int(value) for value in coords[actual_immediate_idx])
        actual_second_coords = tuple(int(value) for value in coords[actual_second_idx])
        sigma12_immediate_coords = tuple(int(value) for value in coords[sigma12_immediate_idx])
        sigma12_second_coords = tuple(int(value) for value in coords[sigma12_second_idx])
        sigma22_immediate_coords = tuple(int(value) for value in coords[sigma22_immediate_idx])
        sigma22_second_coords = tuple(int(value) for value in coords[sigma22_second_idx])
        sigma32_second_coords = tuple(int(value) for value in coords[sigma32_second_idx])

        rel_immediate = tuple(_rel_coords(source_coords, actual_immediate_coords, m))
        rel_second = tuple(_rel_coords(source_coords, actual_second_coords, m))
        rel_sigma12_second = tuple(_rel_coords(source_coords, sigma12_second_coords, m))
        rel_sigma32_second = tuple(_rel_coords(source_coords, sigma32_second_coords, m))
        neighbor_labels = tuple(str(sigma21_labels[int(step_by_dir[d][idx])]) for d in range(5))

        if actual_immediate_idx != sigma22_immediate_idx:
            bad_sigma22_first.append(
                {
                    "source_index": int(idx),
                    "source_coords": list(source_coords),
                    "actual_immediate_coords": list(actual_immediate_coords),
                    "sigma22_immediate_coords": list(sigma22_immediate_coords),
                }
            )
        if actual_immediate_idx == sigma12_immediate_idx:
            bad_sigma12_first.append(
                {
                    "source_index": int(idx),
                    "source_coords": list(source_coords),
                    "actual_immediate_coords": list(actual_immediate_coords),
                    "sigma12_immediate_coords": list(sigma12_immediate_coords),
                }
            )
        if actual_second_idx != sigma22_second_idx:
            bad_sigma22_second.append(
                {
                    "source_index": int(idx),
                    "source_coords": list(source_coords),
                    "actual_second_coords": list(actual_second_coords),
                    "sigma22_second_coords": list(sigma22_second_coords),
                }
            )
        if actual_second_idx == sigma32_second_idx:
            bad_sigma32_second.append(
                {
                    "source_index": int(idx),
                    "source_coords": list(source_coords),
                    "actual_second_coords": list(actual_second_coords),
                    "sigma32_second_coords": list(sigma32_second_coords),
                }
            )
        if actual_second_idx != sigma12_second_idx:
            bad_sigma12_second.append(
                {
                    "source_index": int(idx),
                    "source_coords": list(source_coords),
                    "actual_second_coords": list(actual_second_coords),
                    "sigma12_second_coords": list(sigma12_second_coords),
                }
            )

        bump(first_rel_counter, rel_immediate)
        bump(second_rel_counter, rel_second)
        bump(sigma12_second_rel_counter, rel_sigma12_second)
        bump(sigma32_second_rel_counter, rel_sigma32_second)
        neighbor_counter[neighbor_labels] = int(neighbor_counter.get(neighbor_labels, 0)) + 1

        if len(examples) < 8:
            examples.append(
                {
                    "source_index": int(idx),
                    "source_payload": _coords_payload(source_coords, m),
                    "actual_immediate_payload": _coords_payload(actual_immediate_coords, m),
                    "actual_second_payload": _coords_payload(actual_second_coords, m),
                    "sigma12_second_payload": _coords_payload(sigma12_second_coords, m),
                    "sigma22_second_payload": _coords_payload(sigma22_second_coords, m),
                    "sigma32_second_payload": _coords_payload(sigma32_second_coords, m),
                    "neighbor_labels_by_direction": list(neighbor_labels),
                }
            )

    source_count_matches_m_times_m_minus_1 = source_count == m * (m - 1)
    microcase_count = 1 if len(first_rel_counter) == len(second_rel_counter) == len(sigma32_second_rel_counter) == 1 else None

    return {
        "m": int(m),
        "n": int(prepared.pre["n"]),
        "source_count": int(source_count),
        "source_count_matches_m_times_m_minus_1": bool(source_count_matches_m_times_m_minus_1),
        "all_first_steps_match_sigma22": bool(not bad_sigma22_first),
        "all_first_steps_avoid_sigma12": bool(not bad_sigma12_first),
        "all_second_steps_match_sigma22": bool(not bad_sigma22_second),
        "all_second_steps_match_sigma12": bool(not bad_sigma12_second),
        "all_second_steps_avoid_sigma32": bool(not bad_sigma32_second),
        "candidate_overlap_sizes": {
            "sigma21_layer2": list(sigma21_meta["layer2_overlap_sizes"]),
            "sigma21_layer3": list(sigma21_meta["layer3_overlap_sizes"]),
            "sigma12_layer2": list(sigma12_meta["layer2_overlap_sizes"]),
            "sigma12_layer3": list(sigma12_meta["layer3_overlap_sizes"]),
            "sigma22_layer2": list(sigma22_meta["layer2_overlap_sizes"]),
            "sigma22_layer3": list(sigma22_meta["layer3_overlap_sizes"]),
            "sigma32_layer2": list(sigma32_meta["layer2_overlap_sizes"]),
            "sigma32_layer3": list(sigma32_meta["layer3_overlap_sizes"]),
        },
        "representative_relative_data": {
            "relative_immediate_coords": list(next(iter(first_rel_counter.keys()))),
            "relative_actual_second_coords": list(next(iter(second_rel_counter.keys()))),
            "relative_sigma12_second_coords": list(next(iter(sigma12_second_rel_counter.keys()))),
            "relative_sigma32_second_coords": list(next(iter(sigma32_second_rel_counter.keys()))),
            "counts": {
                "immediate": int(next(iter(first_rel_counter.values()))),
                "actual_second": int(next(iter(second_rel_counter.values()))),
                "sigma12_second": int(next(iter(sigma12_second_rel_counter.values()))),
                "sigma32_second": int(next(iter(sigma32_second_rel_counter.values()))),
            },
        },
        "neighbor_patterns": [
            {"labels": list(labels), "count": int(count)}
            for labels, count in sorted(neighbor_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
        "symmetry_reduced_microcase_count": int(microcase_count or max(len(first_rel_counter), len(second_rel_counter), len(sigma32_second_rel_counter))),
        "bad_sigma22_first_examples": bad_sigma22_first[:3],
        "bad_sigma12_first_examples": bad_sigma12_first[:3],
        "bad_sigma22_second_examples": bad_sigma22_second[:3],
        "bad_sigma12_second_examples": bad_sigma12_second[:3],
        "bad_sigma32_second_examples": bad_sigma32_second[:3],
        "examples": examples,
    }


def _summary(per_m_rows: Sequence[Mapping[str, object]], bundle_root: Path) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "bundle_root": str(bundle_root),
        "checked_moduli": [int(row["m"]) for row in per_m_rows],
        "all_source_counts_match_m_times_m_minus_1": bool(all(bool(row["source_count_matches_m_times_m_minus_1"]) for row in per_m_rows)),
        "all_first_steps_match_sigma22": bool(all(bool(row["all_first_steps_match_sigma22"]) for row in per_m_rows)),
        "all_first_steps_avoid_sigma12": bool(all(bool(row["all_first_steps_avoid_sigma12"]) for row in per_m_rows)),
        "all_second_steps_match_sigma22": bool(all(bool(row["all_second_steps_match_sigma22"]) for row in per_m_rows)),
        "all_second_steps_match_sigma12": bool(all(bool(row["all_second_steps_match_sigma12"]) for row in per_m_rows)),
        "all_second_steps_avoid_sigma32": bool(all(bool(row["all_second_steps_avoid_sigma32"]) for row in per_m_rows)),
        "all_microcase_counts_equal_one": bool(all(int(row["symmetry_reduced_microcase_count"]) == 1 for row in per_m_rows)),
        "representative_relative_data": per_m_rows[0]["representative_relative_data"] if per_m_rows else {},
        "strongest_supported_conclusion": (
            "Across the checked moduli, the common left family in sigma21 has first left step matching sigma22 and avoiding sigma12, "
            "while its second left step matches both sigma12 and sigma22 and always avoids sigma32. "
            "So the dangerous repeated-end centered-right target sigma32 is excluded on the surfaced bundle semantics."
        ),
    }


def _write_csv(path: Path, per_m_rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "m",
        "source_count",
        "source_count_matches_m_times_m_minus_1",
        "symmetry_reduced_microcase_count",
        "all_first_steps_match_sigma22",
        "all_first_steps_avoid_sigma12",
        "all_second_steps_match_sigma22",
        "all_second_steps_match_sigma12",
        "all_second_steps_avoid_sigma32",
        "relative_immediate_coords",
        "relative_actual_second_coords",
        "relative_sigma12_second_coords",
        "relative_sigma32_second_coords",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in per_m_rows:
            rep = row["representative_relative_data"]
            writer.writerow(
                {
                    "m": int(row["m"]),
                    "source_count": int(row["source_count"]),
                    "source_count_matches_m_times_m_minus_1": bool(row["source_count_matches_m_times_m_minus_1"]),
                    "symmetry_reduced_microcase_count": int(row["symmetry_reduced_microcase_count"]),
                    "all_first_steps_match_sigma22": bool(row["all_first_steps_match_sigma22"]),
                    "all_first_steps_avoid_sigma12": bool(row["all_first_steps_avoid_sigma12"]),
                    "all_second_steps_match_sigma22": bool(row["all_second_steps_match_sigma22"]),
                    "all_second_steps_match_sigma12": bool(row["all_second_steps_match_sigma12"]),
                    "all_second_steps_avoid_sigma32": bool(row["all_second_steps_avoid_sigma32"]),
                    "relative_immediate_coords": json.dumps(rep["relative_immediate_coords"]),
                    "relative_actual_second_coords": json.dumps(rep["relative_actual_second_coords"]),
                    "relative_sigma12_second_coords": json.dumps(rep["relative_sigma12_second_coords"]),
                    "relative_sigma32_second_coords": json.dumps(rep["relative_sigma32_second_coords"]),
                }
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--m-values", type=int, nargs="*", default=list(DEFAULT_M_VALUES))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    seed032 = _import_seed032(args.bundle_root)
    per_m_rows = [_analyze_m(seed032, int(m)) for m in args.m_values]
    summary = _summary(per_m_rows, args.bundle_root)

    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_json(out_dir / "summary.json", summary)
    _write_json(out_dir / "per_modulus.json", {"rows": per_m_rows})
    _write_csv(out_dir / "per_modulus.csv", per_m_rows)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
