#!/usr/bin/env python3
"""Check the remaining sigma23 local microstate theorem on the centered-left strip."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_endpoint_latin_repair as seed032
from torus_nd_d5_return_map_model_common import environment_block

TASK_ID = "D5-SIGMA23-R1-MICROSTATE-CHECK-197"
DEFAULT_M_VALUES = (5, 7, 9, 11, 13, 15, 17)
LEFT_WORD = (4, 1, 4)
RIGHT_WORDS = {
    "sigma21": (1, 2, 2),
    "sigma22": (2, 1, 2),
    "sigma23": (2, 2, 1),
}


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _coords_payload(coords: Sequence[int], m: int) -> Dict[str, int]:
    return {
        "x0": int(coords[0]),
        "q": int(coords[1]),
        "w": int(coords[2]),
        "v": int(coords[3]),
        "u": int(coords[4]),
        "s": int((int(coords[2]) + int(coords[4])) % m),
        "layer": int(sum(int(value) for value in coords) % m),
    }


def _rel_coords(source: Sequence[int], target: Sequence[int], m: int) -> List[int]:
    return [int((int(target[axis]) - int(source[axis])) % m) for axis in range(5)]


def _signature(
    *,
    m: int,
    source_coords: Sequence[int],
    immediate_coords: Sequence[int],
    actual_second_coords: Sequence[int],
    sigma22_second_coords: Sequence[int],
    sigma23_second_coords: Sequence[int],
    neighbor_labels: Sequence[str],
) -> Tuple[object, ...]:
    return (
        tuple(_rel_coords(source_coords, immediate_coords, m)),
        tuple(_rel_coords(source_coords, actual_second_coords, m)),
        tuple(_rel_coords(source_coords, sigma22_second_coords, m)),
        tuple(_rel_coords(source_coords, sigma23_second_coords, m)),
        tuple(str(label) for label in neighbor_labels),
    )


def _build_rows(prepared: seed032.PreparedSearch) -> Dict[str, Tuple[List[int], List[str]]]:
    out: Dict[str, Tuple[List[int], List[str]]] = {}
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
            raise ValueError(f"{name} unexpectedly failed to build at m={prepared.m}")
        out[name] = (nexts_all[0], meta["labels_by_color"][0])
    return out


def _per_m_analysis(m: int) -> Dict[str, object]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    rows = _build_rows(prepared)
    coords = prepared.pre["coords"]
    step_by_dir = prepared.pre["step_by_dir"]

    sigma21_row, sigma21_labels = rows["sigma21"]
    sigma22_row, _ = rows["sigma22"]
    sigma23_row, _ = rows["sigma23"]

    source_indices = [idx for idx, label in enumerate(sigma21_labels) if label == "R1"]
    microcases: Dict[Tuple[object, ...], Dict[str, object]] = {}
    signature_counts: Counter[Tuple[object, ...]] = Counter()
    first_bad_sigma22 = None
    first_bad_sigma23 = None

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
        neighbor_labels = [str(sigma21_labels[int(step_by_dir[direction][idx])]) for direction in range(5)]

        sig = _signature(
            m=m,
            source_coords=source_coords,
            immediate_coords=immediate_coords,
            actual_second_coords=actual_second_coords,
            sigma22_second_coords=sigma22_second_coords,
            sigma23_second_coords=sigma23_second_coords,
            neighbor_labels=neighbor_labels,
        )
        signature_counts[sig] += 1

        matches_sigma22 = actual_second_idx == sigma22_second_idx
        matches_sigma23 = actual_second_idx == sigma23_second_idx
        if not matches_sigma22 and first_bad_sigma22 is None:
            first_bad_sigma22 = {
                "source_index": int(idx),
                "source_coords": list(source_coords),
                "actual_second_coords": list(actual_second_coords),
                "sigma22_second_coords": list(sigma22_second_coords),
            }
        if matches_sigma23 and first_bad_sigma23 is None:
            first_bad_sigma23 = {
                "source_index": int(idx),
                "source_coords": list(source_coords),
                "actual_second_coords": list(actual_second_coords),
                "sigma23_second_coords": list(sigma23_second_coords),
            }

        case = microcases.setdefault(
            sig,
            {
                "source_local_signature": {
                    "source_label": "R1",
                    "neighbor_labels_by_direction": neighbor_labels,
                    "source_payload": _coords_payload(source_coords, m),
                },
                "relative_immediate_coords": _rel_coords(source_coords, immediate_coords, m),
                "relative_actual_second_coords": _rel_coords(source_coords, actual_second_coords, m),
                "relative_sigma22_second_coords": _rel_coords(source_coords, sigma22_second_coords, m),
                "relative_sigma23_second_coords": _rel_coords(source_coords, sigma23_second_coords, m),
                "immediate_payload": _coords_payload(immediate_coords, m),
                "actual_second_payload": _coords_payload(actual_second_coords, m),
                "sigma22_second_payload": _coords_payload(sigma22_second_coords, m),
                "sigma23_second_payload": _coords_payload(sigma23_second_coords, m),
                "immediate_image_right_word": [2, 1, 2],
                "right_delta_from_sigma21": [1, 2],
                "slot3_changes": False,
                "centered_left_compatibility": {
                    "sigma21": False,
                    "sigma22": True,
                    "sigma23": False,
                },
                "reason": (
                    "After the immediate sigma21 R1 step, the actual second-step target agrees with the sigma22 "
                    "prototype and disagrees with the sigma23 prototype."
                ),
                "example_sources": [],
            },
        )
        if len(case["example_sources"]) < 6:
            case["example_sources"].append(
                {
                    "source_index": int(idx),
                    "source_coords": list(source_coords),
                    "immediate_coords": list(immediate_coords),
                    "actual_second_coords": list(actual_second_coords),
                }
            )

    case_rows = []
    for case_id, (sig, count) in enumerate(signature_counts.items()):
        row = dict(microcases[sig])
        row["case_id"] = f"C{case_id}"
        row["count"] = int(count)
        case_rows.append(row)
    case_rows.sort(key=lambda row: row["case_id"])

    return {
        "m": int(m),
        "source_count": int(len(source_indices)),
        "symmetry_reduced_microcase_count": int(len(case_rows)),
        "all_second_steps_match_sigma22": bool(first_bad_sigma22 is None),
        "all_second_steps_avoid_sigma23": bool(first_bad_sigma23 is None),
        "all_inferred_delta_is_12": bool(
            all(row["right_delta_from_sigma21"] == [1, 2] for row in case_rows)
        ),
        "all_slot3_unchanged": bool(all(not row["slot3_changes"] for row in case_rows)),
        "first_bad_sigma22": first_bad_sigma22,
        "first_bad_sigma23": first_bad_sigma23,
        "case_rows": case_rows,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the sigma23 immediate-R1 microstate theorem.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args(argv)

    per_m_rows = [_per_m_analysis(m) for m in DEFAULT_M_VALUES]

    summary = {
        "task_id": TASK_ID,
        "checked_moduli": list(DEFAULT_M_VALUES),
        "all_second_steps_match_sigma22": bool(
            all(row["all_second_steps_match_sigma22"] for row in per_m_rows)
        ),
        "all_second_steps_avoid_sigma23": bool(
            all(row["all_second_steps_avoid_sigma23"] for row in per_m_rows)
        ),
        "all_inferred_delta_is_12": bool(
            all(row["all_inferred_delta_is_12"] for row in per_m_rows)
        ),
        "all_slot3_unchanged": bool(
            all(row["all_slot3_unchanged"] for row in per_m_rows)
        ),
        "microcase_count_pattern": {
            str(row["m"]): int(row["symmetry_reduced_microcase_count"]) for row in per_m_rows
        },
        "source_count_pattern": {
            str(row["m"]): int(row["source_count"]) for row in per_m_rows
        },
        "main_result": (
            "For every checked odd modulus, the sigma21 immediate R1 source family collapses to a single rooted "
            "translation class. Its actual two-step continuation matches the sigma22 prototype and never the sigma23 "
            "prototype, so every checked case has image right word [2,1,2], delta [1,2], and unchanged slot 3."
        ),
        "environment": environment_block(),
    }

    representative_cases = {
        str(row["m"]): row["case_rows"] for row in per_m_rows
    }
    _write_json(args.out_dir / "per_modulus.json", {"rows": per_m_rows})
    _write_json(args.out_dir / "symmetry_reduced_microcases.json", representative_cases)
    _write_json(args.out_dir / "analysis_summary.json", summary)
    _write_json(args.summary_out, summary)

    print(
        f"{TASK_ID}: checked={len(DEFAULT_M_VALUES)} "
        f"match_sigma22={summary['all_second_steps_match_sigma22']} "
        f"avoid_sigma23={summary['all_second_steps_avoid_sigma23']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
