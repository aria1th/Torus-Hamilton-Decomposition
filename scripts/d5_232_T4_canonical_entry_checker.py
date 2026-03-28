#!/usr/bin/env python3
"""Exact canonical-entry checker for T4 using the surfaced 2026-03-21 bundle.

This script verifies the canonical seed
    [2,2,1]/[1,4,4]
inside the surfaced endpoint-repair builder.  It checks that on chosen odd
moduli the only live source family after the actual-needed tiny-repair cleanup
is the R1 family, and that every such source has the uniform prefix
    1,4,4
with two-step normalized entry
    E = (m-1, 1, u_source, 2)
in the shifted section coordinates used by the explicit odometer block.

Outputs:
- JSON summary
- per-modulus CSV table
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import platform
import sys
import tarfile
import time
import types
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

TASK_ID = "D5-T4-CANONICAL-ENTRY-CHECKER-232"
LEFT_WORD = (2, 2, 1)
RIGHT_WORD = (1, 4, 4)
DEFAULT_M_VALUES = (3, 5, 7, 9, 11, 13, 15, 17)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name) for name in fieldnames})


def _extract_bundle_from_tar(bundle_tar: Path, extract_root: Path) -> Path:
    extract_root.mkdir(parents=True, exist_ok=True)
    with tarfile.open(bundle_tar, "r") as archive:
        archive.extractall(extract_root)
    candidates = [path for path in extract_root.iterdir() if path.is_dir()]
    if len(candidates) != 1:
        raise RuntimeError(f"Expected a single bundle directory under {extract_root}, found {len(candidates)}")
    return candidates[0]


def _resolve_bundle_root(bundle_root: Optional[Path], bundle_tar: Optional[Path], work_root: Path) -> Path:
    if bundle_root is not None:
        if not bundle_root.exists():
            raise FileNotFoundError(f"Bundle root not found: {bundle_root}")
        return bundle_root
    if bundle_tar is None:
        raise ValueError("Either --bundle-root or --bundle-tar must be supplied.")
    extract_root = work_root / "bundle_extract"
    return _extract_bundle_from_tar(bundle_tar, extract_root)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create module spec for {name} at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _inject_return_map_stub(bundle_root: Path) -> None:
    registry_path = bundle_root / "artifacts" / "d5_return_map_model_017" / "data" / "witness_registry.json"
    rows = _load_json(registry_path)
    if not isinstance(rows, list):
        raise TypeError(f"Unexpected witness registry structure at {registry_path}")
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
        return [
            SimpleNamespace(
                name=str(row["name"]),
                role=row.get("role"),
                family=row.get("family"),
                source=row.get("source"),
                rule_payload=row["rule"],
            )
            for row in rows
        ]

    stub.environment_block = environment_block  # type: ignore[attr-defined]
    stub.runtime_since = runtime_since  # type: ignore[attr-defined]
    stub.load_witness_specs = load_witness_specs  # type: ignore[attr-defined]
    sys.modules[stub.__name__] = stub


def _import_seed032(bundle_root: Path) -> Any:
    code_dir = bundle_root / "artifacts" / "d5_mixed_skew_odometer_normal_form_018" / "code"
    script_path = bundle_root / "scripts" / "torus_nd_d5_endpoint_latin_repair.py"

    _load_module(
        "torus_nd_d5_strict_palette_context_common",
        code_dir / "torus_nd_d5_strict_palette_context_common.py",
    )
    _load_module(
        "torus_nd_d5_layer3_mode_switch_common",
        code_dir / "torus_nd_d5_layer3_mode_switch_common.py",
    )
    _inject_return_map_stub(bundle_root)
    return _load_module("torus_nd_d5_endpoint_latin_repair", script_path)


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


def _direction_delta(source: Sequence[int], target: Sequence[int], m: int) -> Tuple[int, ...]:
    return tuple(int((int(target[a]) - int(source[a])) % m) for a in range(5))


def _shifted_entry_from_two_step(two_step_coords: Sequence[int], m: int) -> Tuple[int, int, int, int]:
    q = int(two_step_coords[1])
    w = int(two_step_coords[2])
    u = int(two_step_coords[4])
    return ((q - 1) % m, (w + 1) % m, (u - 1) % m, 2)


def _analyze_m(seed032: Any, m: int) -> Dict[str, object]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    nexts_all, meta = seed032._build_candidate(
        prepared,
        w0=0,
        s0=0,
        left_word=LEFT_WORD,
        right_word=RIGHT_WORD,
        cocycle_defect="none",
        repair=None,
    )
    if nexts_all is None:
        raise ValueError(f"Canonical seed failed to build at m={m}: {meta}")

    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    coords = prepared.pre["coords"]

    source_indices = [idx for idx, label in enumerate(labels) if label == "R1"]
    source_count = len(source_indices)

    all_source_formula = True
    all_immediate_is_R2 = True
    all_second_is_R3 = True
    all_third_is_B = True
    all_first_step_is_dir1 = True
    all_second_step_is_dir4 = True
    all_third_step_is_dir4 = True
    all_two_step_image_formula = True
    all_shifted_entry_matches_E = True

    examples: List[Dict[str, object]] = []
    normalized_two_step_payloads = set()
    shifted_entry_payloads = set()

    for idx in source_indices:
        source = tuple(int(value) for value in coords[idx])
        x0, q, w, v, u_source = source
        immediate_idx = int(row[idx])
        second_idx = int(row[immediate_idx])
        third_idx = int(row[second_idx])

        immediate = tuple(int(value) for value in coords[immediate_idx])
        second = tuple(int(value) for value in coords[second_idx])
        third = tuple(int(value) for value in coords[third_idx])

        all_source_formula &= (
            q == m - 1
            and w == 0
            and u_source != 0
            and ((x0 + v + u_source) % m) == 2
            and ((x0 + q + w + v + u_source) % m) == 1
        )
        all_immediate_is_R2 &= labels[immediate_idx] == "R2"
        all_second_is_R3 &= labels[second_idx] == "R3"
        all_third_is_B &= labels[third_idx] == "B"

        first_delta = _direction_delta(source, immediate, m)
        second_delta = _direction_delta(immediate, second, m)
        third_delta = _direction_delta(second, third, m)
        all_first_step_is_dir1 &= first_delta == (0, 1, 0, 0, 0)
        all_second_step_is_dir4 &= second_delta == (0, 0, 0, 0, 1)
        all_third_step_is_dir4 &= third_delta == (0, 0, 0, 0, 1)

        all_two_step_image_formula &= (
            second[1] == 0
            and second[2] == 0
            and ((second[4] - u_source) % m) == 1
        )
        shifted_entry = _shifted_entry_from_two_step(second, m)
        expected_entry = (m - 1, 1, u_source, 2)
        all_shifted_entry_matches_E &= shifted_entry == expected_entry

        normalized_two_step_payloads.add((int(second[1]), int(second[2]), int((second[4] - u_source) % m)))
        shifted_entry_payloads.add(shifted_entry)

        if len(examples) < 6:
            examples.append(
                {
                    "source_index": int(idx),
                    "source_payload": _coords_payload(source, m),
                    "immediate_payload": _coords_payload(immediate, m),
                    "two_step_payload": _coords_payload(second, m),
                    "three_step_payload": _coords_payload(third, m),
                    "shifted_entry": {
                        "q": int(shifted_entry[0]),
                        "w": int(shifted_entry[1]),
                        "u": int(shifted_entry[2]),
                        "Theta": int(shifted_entry[3]),
                    },
                }
            )

    return {
        "m": int(m),
        "source_count": int(source_count),
        "source_count_matches_m_times_m_minus_1": bool(source_count == m * (m - 1)),
        "all_source_formula": bool(all_source_formula),
        "all_immediate_is_R2": bool(all_immediate_is_R2),
        "all_second_is_R3": bool(all_second_is_R3),
        "all_third_is_B": bool(all_third_is_B),
        "all_first_step_is_dir1": bool(all_first_step_is_dir1),
        "all_second_step_is_dir4": bool(all_second_step_is_dir4),
        "all_third_step_is_dir4": bool(all_third_step_is_dir4),
        "all_two_step_image_formula": bool(all_two_step_image_formula),
        "all_shifted_entry_matches_E": bool(all_shifted_entry_matches_E),
        "normalized_two_step_payloads": [list(item) for item in sorted(normalized_two_step_payloads)],
        "shifted_entry_payloads": [list(item) for item in sorted(shifted_entry_payloads)],
        "examples": examples,
    }


def _parse_m_values(raw: str) -> Tuple[int, ...]:
    values = []
    for token in raw.split(","):
        token = token.strip()
        if token:
            values.append(int(token))
    if not values:
        raise ValueError("Need at least one modulus.")
    return tuple(values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle-root", type=Path, default=Path("/mnt/data/bundle_work/roundy_d5_endpoint_return_model_bundle_20260321_update_197"), help="Extracted bundle root directory.")
    parser.add_argument("--bundle-tar", type=Path, default=Path("/mnt/data/roundy_d5_endpoint_return_model_bundle_20260321_update_197.tar"), help="Bundle tarball path, used only if --bundle-root is absent.")
    parser.add_argument("--work-root", type=Path, default=Path("/mnt/data/d5_232_T4_checker_work"), help="Working directory for optional extraction.")
    parser.add_argument("--m-values", type=str, default=",".join(str(m) for m in DEFAULT_M_VALUES), help="Comma-separated odd moduli.")
    parser.add_argument("--summary-json", type=Path, default=Path("/mnt/data/d5_232_T4_canonical_entry_checker_summary.json"))
    parser.add_argument("--table-csv", type=Path, default=Path("/mnt/data/d5_232_T4_canonical_entry_checker_table.csv"))
    args = parser.parse_args()

    start = time.perf_counter()
    m_values = _parse_m_values(args.m_values)
    bundle_root = _resolve_bundle_root(args.bundle_root, args.bundle_tar, args.work_root)
    seed032 = _import_seed032(bundle_root)

    per_modulus = [_analyze_m(seed032, m) for m in m_values]
    overall = {
        "task_id": TASK_ID,
        "bundle_root": str(bundle_root),
        "m_values": [int(m) for m in m_values],
        "all_source_count_matches_m_times_m_minus_1": all(row["source_count_matches_m_times_m_minus_1"] for row in per_modulus),
        "all_source_formula": all(row["all_source_formula"] for row in per_modulus),
        "all_immediate_is_R2": all(row["all_immediate_is_R2"] for row in per_modulus),
        "all_second_is_R3": all(row["all_second_is_R3"] for row in per_modulus),
        "all_third_is_B": all(row["all_third_is_B"] for row in per_modulus),
        "all_first_step_is_dir1": all(row["all_first_step_is_dir1"] for row in per_modulus),
        "all_second_step_is_dir4": all(row["all_second_step_is_dir4"] for row in per_modulus),
        "all_third_step_is_dir4": all(row["all_third_step_is_dir4"] for row in per_modulus),
        "all_two_step_image_formula": all(row["all_two_step_image_formula"] for row in per_modulus),
        "all_shifted_entry_matches_E": all(row["all_shifted_entry_matches_E"] for row in per_modulus),
        "runtime_seconds": time.perf_counter() - start,
        "per_modulus": per_modulus,
    }
    _write_json(args.summary_json, overall)

    table_rows: List[Dict[str, object]] = []
    for row in per_modulus:
        table_rows.append(
            {
                "m": row["m"],
                "source_count": row["source_count"],
                "source_count_matches_m_times_m_minus_1": row["source_count_matches_m_times_m_minus_1"],
                "all_source_formula": row["all_source_formula"],
                "all_immediate_is_R2": row["all_immediate_is_R2"],
                "all_second_is_R3": row["all_second_is_R3"],
                "all_third_is_B": row["all_third_is_B"],
                "all_first_step_is_dir1": row["all_first_step_is_dir1"],
                "all_second_step_is_dir4": row["all_second_step_is_dir4"],
                "all_third_step_is_dir4": row["all_third_step_is_dir4"],
                "all_two_step_image_formula": row["all_two_step_image_formula"],
                "all_shifted_entry_matches_E": row["all_shifted_entry_matches_E"],
                "normalized_two_step_payloads": json.dumps(row["normalized_two_step_payloads"], ensure_ascii=False),
                "shifted_entry_payloads": json.dumps(row["shifted_entry_payloads"], ensure_ascii=False),
            }
        )
    _write_csv(
        args.table_csv,
        table_rows,
        fieldnames=[
            "m",
            "source_count",
            "source_count_matches_m_times_m_minus_1",
            "all_source_formula",
            "all_immediate_is_R2",
            "all_second_is_R3",
            "all_third_is_B",
            "all_first_step_is_dir1",
            "all_second_step_is_dir4",
            "all_third_step_is_dir4",
            "all_two_step_image_formula",
            "all_shifted_entry_matches_E",
            "normalized_two_step_payloads",
            "shifted_entry_payloads",
        ],
    )


if __name__ == "__main__":
    main()
