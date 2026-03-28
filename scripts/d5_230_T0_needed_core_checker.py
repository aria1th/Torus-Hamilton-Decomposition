#!/usr/bin/env python3
"""Sanity checker for the actual-needed T0 core on the surfaced 2026-03-21 bundle.

This script verifies, on a checked modulus range, that every one-label repair in the
actual-needed T0 scope leaves the universal R1/background collision family intact for

- the canonical seed [2,2,1]/[1,4,4], targeting labels L3,R2,R3;
- the mixed seed sigma21 = [4,1,4]/[1,2,2], targeting labels L2,L3,R2,R3.

The proof in d5_230 is symbolic and all-modulus.  This script is only a sanity check.
"""
from __future__ import annotations

import argparse
import importlib
import json
import platform
import sys
import time
import types
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

TASK_ID = "D5-T0-NEEDED-CORE-CHECKER-230"
BIT_NAMES = (
    "pred_changed",
    "pred_left",
    "pred_right",
    "pred_deep",
    "succ_changed",
    "succ_left",
    "succ_right",
    "succ_deep",
    "self_deep",
    "self_stage3",
)
CHECKED_M_VALUES = (3, 5)
COCYCLE_DEFECTS = ("none", "left", "right", "both")
REPRESENTATIVE_W0 = 0
REPRESENTATIVE_S0 = 0
CASES = (
    {
        "case_name": "canonical_T4_needed_core",
        "left_word": (2, 2, 1),
        "right_word": (1, 4, 4),
        "target_labels": ("L3", "R2", "R3"),
    },
    {
        "case_name": "sigma21_T1_needed_core",
        "left_word": (4, 1, 4),
        "right_word": (1, 2, 2),
        "target_labels": ("L2", "L3", "R2", "R3"),
    },
)


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


def _encode(coords: Sequence[int], m: int) -> int:
    out = 0
    for value in coords:
        out = out * m + int(value)
    return out


def _repair_rows_for_case(case: Mapping[str, object]) -> Iterable[Tuple[str, Mapping[str, object], str]]:
    left_word = tuple(int(value) for value in case["left_word"])
    right_word = tuple(int(value) for value in case["right_word"])
    for label in case["target_labels"]:
        base_dir = (left_word if label.startswith("L") else right_word)[int(str(label)[1]) - 1]
        for alt_dir in range(5):
            if alt_dir == base_dir:
                continue
            repair = {"label": str(label), "alt_dir": int(alt_dir)}
            for cocycle_defect in COCYCLE_DEFECTS:
                yield ("one_gate", repair, cocycle_defect)
        for bit_name in BIT_NAMES:
            for bit_value in (0, 1):
                for alt_dir in range(5):
                    if alt_dir == base_dir:
                        continue
                    repair = {
                        "label": str(label),
                        "bit_name": str(bit_name),
                        "bit_value": int(bit_value),
                        "alt_dir": int(alt_dir),
                    }
                    for cocycle_defect in COCYCLE_DEFECTS:
                        yield ("one_bit", repair, cocycle_defect)


def _coords_to_payload(coords: Sequence[int], m: int) -> Dict[str, int]:
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


def _check_candidate(seed032: Any, prepared: Any, m: int, case: Mapping[str, object], family_name: str, repair: Mapping[str, object], cocycle_defect: str) -> Dict[str, object]:
    nexts_all, meta = seed032._build_candidate(
        prepared,
        w0=REPRESENTATIVE_W0,
        s0=REPRESENTATIVE_S0,
        left_word=tuple(int(value) for value in case["left_word"]),
        right_word=tuple(int(value) for value in case["right_word"]),
        cocycle_defect=cocycle_defect,
        repair=repair,
    )
    if nexts_all is None:
        return {
            "m": int(m),
            "candidate_builds": False,
            "failure": "build_conflict",
            "layer2_conflict": bool(meta["layer2_conflict"]),
            "layer3_conflict": bool(meta["layer3_conflict"]),
        }

    row = nexts_all[0]
    coords = prepared.pre["coords"]
    labels = meta["labels_by_color"][0]

    source_indices = [idx for idx, label in enumerate(labels) if label == "R1"]
    family_examples: List[Dict[str, object]] = []
    failures: List[Dict[str, object]] = []

    for idx in source_indices:
        x = tuple(int(value) for value in coords[idx])
        target_idx = int(row[idx])
        z = tuple(int(value) for value in coords[target_idx])
        expected_z = (x[0], 0, x[2], x[3], x[4])
        y = (x[0], 0, x[2], x[3], (x[4] - 1) % m)
        y_idx = _encode(y, m)

        if z != expected_z:
            failures.append(
                {
                    "type": "R1_step_mismatch",
                    "source_index": int(idx),
                    "source": list(x),
                    "actual_target": list(z),
                    "expected_target": list(expected_z),
                }
            )
            continue
        if labels[y_idx] != "B":
            failures.append(
                {
                    "type": "background_label_changed",
                    "source_index": int(idx),
                    "background_index": int(y_idx),
                    "background": list(y),
                    "background_label": str(labels[y_idx]),
                }
            )
            continue
        if int(row[y_idx]) != target_idx:
            failures.append(
                {
                    "type": "background_target_mismatch",
                    "source_index": int(idx),
                    "background_index": int(y_idx),
                    "background": list(y),
                    "actual_background_target": list(coords[int(row[y_idx])]),
                    "expected_target": list(z),
                }
            )
            continue
        if len(family_examples) < 6:
            family_examples.append(
                {
                    "R1_source_index": int(idx),
                    "R1_source": _coords_to_payload(x, m),
                    "B_mate_index": int(y_idx),
                    "B_mate": _coords_to_payload(y, m),
                    "common_target_index": int(target_idx),
                    "common_target": _coords_to_payload(z, m),
                }
            )

    preserved_family_size = int(len(source_indices) - len(failures))
    return {
        "m": int(m),
        "candidate_builds": True,
        "case_name": str(case["case_name"]),
        "family_name": str(family_name),
        "repair": dict(repair),
        "cocycle_defect": str(cocycle_defect),
        "R1_source_count": int(len(source_indices)),
        "expected_R1_source_count": int(m * (m - 1)),
        "preserved_R1_collision_family_size": preserved_family_size,
        "all_R1_sources_preserved": bool(not failures),
        "examples": family_examples,
        "failures": failures[:10],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bundle-root",
        type=Path,
        default=Path("/mnt/data/bundle_197/roundy_d5_endpoint_return_model_bundle_20260321_update_197"),
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=Path("/mnt/data/d5_230_T0_needed_core_checker_summary.json"),
    )
    parser.add_argument(
        "--out-csv",
        type=Path,
        default=Path("/mnt/data/d5_230_T0_needed_core_checker_table.csv"),
    )
    args = parser.parse_args()

    seed032 = _import_seed032(args.bundle_root)
    mixed_rule = seed032._mixed_rule()
    prepared_by_m = {m: seed032._prepare_m(m, mixed_rule) for m in CHECKED_M_VALUES}
    summary_rows: List[Dict[str, object]] = []
    failures: List[Dict[str, object]] = []

    for case in CASES:
        for family_name, repair, cocycle_defect in _repair_rows_for_case(case):
            for m in CHECKED_M_VALUES:
                row = _check_candidate(seed032, prepared_by_m[m], m, case, family_name, repair, cocycle_defect)
                summary_rows.append(
                    {
                        "case_name": row.get("case_name", case["case_name"]),
                        "m": int(m),
                        "family_name": str(family_name),
                        "label": str(repair["label"]),
                        "cocycle_defect": str(cocycle_defect),
                        "candidate_builds": bool(row["candidate_builds"]),
                        "R1_source_count": int(row.get("R1_source_count", 0)),
                        "expected_R1_source_count": int(row.get("expected_R1_source_count", 0)),
                        "preserved_R1_collision_family_size": int(row.get("preserved_R1_collision_family_size", 0)),
                        "all_R1_sources_preserved": bool(row.get("all_R1_sources_preserved", False)),
                    }
                )
                if not bool(row.get("candidate_builds", False)) or not bool(row.get("all_R1_sources_preserved", False)):
                    failures.append(row)

    import csv

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case_name",
                "m",
                "family_name",
                "label",
                "cocycle_defect",
                "candidate_builds",
                "R1_source_count",
                "expected_R1_source_count",
                "preserved_R1_collision_family_size",
                "all_R1_sources_preserved",
            ],
        )
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    by_case: Dict[str, Dict[str, object]] = {}
    for case in CASES:
        case_name = str(case["case_name"])
        rows = [row for row in summary_rows if row["case_name"] == case_name]
        by_case[case_name] = {
            "candidate_count": len(rows),
            "all_candidates_build": all(bool(row["candidate_builds"]) for row in rows),
            "all_candidates_preserve_full_R1_family": all(bool(row["all_R1_sources_preserved"]) for row in rows),
            "checked_m_values": list(CHECKED_M_VALUES),
            "target_labels": list(case["target_labels"]),
        }

    payload = {
        "task_id": TASK_ID,
        "bundle_root": str(args.bundle_root),
        "checked_m_values": list(CHECKED_M_VALUES),
        "summary_by_case": by_case,
        "failure_count": len(failures),
        "failures": failures[:20],
    }
    _write_json(args.out_json, payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
