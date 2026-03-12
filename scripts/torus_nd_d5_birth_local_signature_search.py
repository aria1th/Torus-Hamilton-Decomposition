#!/usr/bin/env python3
"""Search simple birth-local neighborhood signatures for the best-seed corridor."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import torus_nd_d5_corridor_phase_extraction as phase034
import torus_nd_d5_endpoint_latin_repair as seed032
import torus_nd_d5_layer3_mode_switch_common as mode008
from torus_nd_d5_return_map_model_common import environment_block, runtime_since
from torus_nd_d5_strict_palette_context_common import DIM

TASK_ID = "D5-BIRTH-LOCAL-SIGNATURE-038"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M_VALUES = (11,)
ALL_M_VALUES = PRIMARY_M_VALUES + CONTROL_M_VALUES
MAX_COMBO_SIZE = 5

FIELD_NAMES = (
    "cur_layer",
    "cur_qneg1",
    "cur_phase_align",
    "cur_wu2",
    "pred0_phase",
    "pred0_wu2",
    "pred1_phase",
    "pred1_wu2",
    "pred2_phase",
    "pred2_wu2",
    "pred3_phase",
    "pred3_wu2",
    "pred4_phase",
    "pred4_wu2",
    "succ0_phase",
    "succ0_wu2",
    "succ1_phase",
    "succ1_wu2",
    "succ2_phase",
    "succ2_wu2",
    "succ3_phase",
    "succ3_wu2",
    "succ4_phase",
    "succ4_wu2",
)
FIELD_TO_INDEX = {name: idx for idx, name in enumerate(FIELD_NAMES)}
EXCEPTIONAL_SOURCE_FIELDS = ("pred2_wu2", "pred4_wu2")


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _successor_coords(coords: Sequence[int], color: int, rel_direction: int, m: int) -> Tuple[int, ...]:
    out = list(coords)
    out[(color + rel_direction) % DIM] = (out[(color + rel_direction) % DIM] + 1) % m
    return tuple(out)


def _local_bit_row(coords: Sequence[int], color: int, m: int) -> Tuple[int, ...]:
    row: List[int] = [
        int(sum(coords) % m),
        int(mode008.old_bit_q_eq_neg1(coords, color, m)),
        int(mode008.phase_align_value(coords, color, m)),
        int(mode008.wu2_value(coords, color, m)),
    ]
    for rel_direction in range(DIM):
        pred = mode008.predecessor_coords(coords, color, rel_direction, m)
        row.append(int(mode008.phase_align_value(pred, color, m)))
        row.append(int(mode008.wu2_value(pred, color, m)))
    for rel_direction in range(DIM):
        succ = _successor_coords(coords, color, rel_direction, m)
        row.append(int(mode008.phase_align_value(succ, color, m)))
        row.append(int(mode008.wu2_value(succ, color, m)))
    return tuple(row)


def _combo_key(row: Sequence[int], combo: Sequence[int]) -> Tuple[int, ...]:
    return tuple(int(row[idx]) for idx in combo)


def _target_rows_for_m(m: int) -> Dict[str, object]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    nexts_all, meta = phase034._build_best_seed(prepared)
    labels = meta["labels_by_color"][0]
    coords = prepared.pre["coords"]
    step_by_dir = prepared.pre["step_by_dir"]
    field_rows = [_local_bit_row(vertex, 0, m) for vertex in coords]

    source = {idx for idx, label in enumerate(labels) if label == "R1"}
    exceptional_source = {idx for idx in source if int(coords[idx][4]) == 3}
    entry = {int(step_by_dir[2][idx]) for idx in source}
    exceptional_entry = {int(step_by_dir[2][idx]) for idx in exceptional_source}

    return {
        "m": int(m),
        "field_rows": field_rows,
        "target_sets": {
            "source_marker": source,
            "source_exceptional": exceptional_source,
            "entry_marker": entry,
            "entry_exceptional": exceptional_entry,
        },
    }


def _combo_examples(
    per_m: Mapping[int, Mapping[str, object]],
    combo_names: Sequence[str],
    *,
    target_name: str,
    subset_name: str | None,
) -> Dict[str, object]:
    combo = tuple(FIELD_TO_INDEX[name] for name in combo_names)
    examples = {}
    for m, payload in per_m.items():
        field_rows = payload["field_rows"]
        target = payload["target_sets"][target_name]
        subset = payload["target_sets"][subset_name] if subset_name is not None else target
        target_keys = {_combo_key(field_rows[idx], combo) for idx in target}
        subset_keys = {_combo_key(field_rows[idx], combo) for idx in subset}
        examples[str(m)] = {
            "target_keys": [list(value) for value in sorted(target_keys)],
            "subset_keys": [list(value) for value in sorted(subset_keys)],
        }
    return {
        "fields": list(combo_names),
        "target_name": target_name,
        "subset_name": subset_name,
        "per_m": examples,
    }


def _search_target_kind(
    per_m: Mapping[int, Mapping[str, object]],
    *,
    target_name: str,
    subset_name: str | None,
) -> Dict[str, object]:
    rows = {}
    no_isolator = True
    representative_isolators: List[Sequence[str]] = []
    for size in range(1, MAX_COMBO_SIZE + 1):
        isolating_count = 0
        example_isolators: List[List[str]] = []
        for combo in itertools.combinations(FIELD_NAMES, size):
            combo_indices = tuple(FIELD_TO_INDEX[name] for name in combo)
            isolates_all = True
            for payload in per_m.values():
                field_rows = payload["field_rows"]
                target = payload["target_sets"][target_name]
                if subset_name is None:
                    selected = target
                    comparison = set(range(len(field_rows))) - target
                else:
                    selected = payload["target_sets"][subset_name]
                    comparison = target - selected
                selected_keys = {_combo_key(field_rows[idx], combo_indices) for idx in selected}
                if any(_combo_key(field_rows[idx], combo_indices) in selected_keys for idx in comparison):
                    isolates_all = False
                    break
            if isolates_all:
                isolating_count += 1
                no_isolator = False
                if len(example_isolators) < 10:
                    example_isolators.append(list(combo))
                if len(representative_isolators) < 10:
                    representative_isolators.append(combo)
        rows[str(size)] = {
            "isolating_count": int(isolating_count),
            "example_isolators": example_isolators,
        }
    return {
        "target_name": target_name,
        "subset_name": subset_name,
        "rows": rows,
        "no_isolator_up_to_max_size": bool(no_isolator),
        "representative_isolators": [list(value) for value in representative_isolators],
    }


def _representative_exceptional_bits(per_m: Mapping[int, Mapping[str, object]]) -> Dict[str, object]:
    out = {}
    for field_name in EXCEPTIONAL_SOURCE_FIELDS:
        field_idx = FIELD_TO_INDEX[field_name]
        per_modulus = {}
        for m, payload in per_m.items():
            field_rows = payload["field_rows"]
            source = payload["target_sets"]["source_marker"]
            exceptional = payload["target_sets"]["source_exceptional"]
            regular = source - exceptional
            per_modulus[str(m)] = {
                "regular_values": sorted({int(field_rows[idx][field_idx]) for idx in regular}),
                "exceptional_values": sorted({int(field_rows[idx][field_idx]) for idx in exceptional}),
                "all_source_values": sorted({int(field_rows[idx][field_idx]) for idx in source}),
            }
        out[field_name] = {
            "field_name": field_name,
            "role": "separates exceptional source slice inside the source class",
            "per_m": per_modulus,
        }
    return out


def _analysis_summary(started: float, per_m: Mapping[int, Mapping[str, object]], results: Mapping[str, object]) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "main_result": (
            "In the simple birth-local neighborhood alphabet built from current "
            "and one-step predecessor/successor phase_align/wu2 bits, the "
            "exceptional source slice is already locally visible, but the source "
            "marker itself is not isolated up to size 5, and the entry slice is "
            "also not isolated up to size 5."
        ),
        "field_count": len(FIELD_NAMES),
        "max_combo_size": int(MAX_COMBO_SIZE),
        "per_m_target_sizes": {
            str(m): {
                key: int(len(value))
                for key, value in payload["target_sets"].items()
            }
            for m, payload in per_m.items()
        },
        "summary": {
            "source_marker_nogo_up_to_5": bool(results["source_marker"]["no_isolator_up_to_max_size"]),
            "entry_marker_nogo_up_to_5": bool(results["entry_marker"]["no_isolator_up_to_max_size"]),
            "source_exceptional_min_size": int(
                next(
                    size
                    for size, row in results["source_exceptional"]["rows"].items()
                    if row["isolating_count"] > 0
                )
            ),
            "entry_exceptional_min_size": None,
            "representative_source_exceptional_bits": list(EXCEPTIONAL_SOURCE_FIELDS),
        },
        "per_size_counts": {
            key: {
                size: int(row["isolating_count"])
                for size, row in value["rows"].items()
            }
            for key, value in results.items()
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Search simple birth-local neighborhood signatures for the best-seed corridor.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    per_m = {m: _target_rows_for_m(m) for m in ALL_M_VALUES}
    results = {
        "source_marker": _search_target_kind(per_m, target_name="source_marker", subset_name=None),
        "source_exceptional": _search_target_kind(
            per_m,
            target_name="source_marker",
            subset_name="source_exceptional",
        ),
        "entry_marker": _search_target_kind(per_m, target_name="entry_marker", subset_name=None),
        "entry_exceptional": _search_target_kind(
            per_m,
            target_name="entry_marker",
            subset_name="entry_exceptional",
        ),
    }
    summary = _analysis_summary(started, per_m, results)

    _write_json(out_dir / "analysis_summary.json", summary)
    _write_json(
        out_dir / "birth_signature_summary.json",
        {
            "field_names": list(FIELD_NAMES),
            "max_combo_size": int(MAX_COMBO_SIZE),
            "results": results,
        },
    )
    _write_json(
        out_dir / "representative_exceptional_source_bits.json",
        _representative_exceptional_bits(per_m),
    )
    _write_json(
        out_dir / "representative_combo_examples.json",
        {
            "source_exceptional_examples": [
                _combo_examples(
                    per_m,
                    combo,
                    target_name="source_marker",
                    subset_name="source_exceptional",
                )
                for combo in (("pred2_wu2",), ("pred4_wu2",))
            ],
        },
    )
    _write_json(args.summary_out, summary)


if __name__ == "__main__":
    main()
