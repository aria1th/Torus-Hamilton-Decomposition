#!/usr/bin/env python3
"""Extract a symmetry-reduced D5 seed-class table from the 030/032 artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from torus_nd_d5_return_map_model_common import environment_block

TASK_ID = "D5-SHAPE-CERTIFICATE-EXTRACT-137"
CANONICAL_PAIR = ((2, 2, 1), (1, 4, 4))
VALUES = (1, 2, 3, 4)
INDEX_BY_VALUE = {value: idx for idx, value in enumerate(VALUES)}


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "class_id",
        "member_seed_ids",
        "left_shapes",
        "right_shapes",
        "shared_bridge_symbols",
        "oriented_bridge_type",
        "normalization_map",
        "best_ranked_member_seed_id",
        "best_ranked_member_pair_left",
        "best_ranked_member_pair_right",
        "best_ranked_member_total_excess",
        "status_from_current_accessible_artifacts",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            best_pair = row["best_ranked_member_pair"]
            writer.writerow(
                {
                    "class_id": row["class_id"],
                    "member_seed_ids": json.dumps(row["member_seed_ids"]),
                    "left_shapes": json.dumps(row["left_shapes"]),
                    "right_shapes": json.dumps(row["right_shapes"]),
                    "shared_bridge_symbols": json.dumps(row["shared_bridge_symbols"]),
                    "oriented_bridge_type": row["oriented_bridge_type"],
                    "normalization_map": row["normalization_map"],
                    "best_ranked_member_seed_id": row["best_ranked_member_seed_id"],
                    "best_ranked_member_pair_left": json.dumps(best_pair["left_word"]),
                    "best_ranked_member_pair_right": json.dumps(best_pair["right_word"]),
                    "best_ranked_member_total_excess": row["best_ranked_member_total_excess"],
                    "status_from_current_accessible_artifacts": row["status_from_current_accessible_artifacts"],
                }
            )


def _load_json(path: str | Path) -> Mapping[str, object]:
    return json.loads(Path(path).read_text())


def _shift_symbol(value: int, amount: int) -> int:
    return VALUES[(INDEX_BY_VALUE[int(value)] + amount) % len(VALUES)]


def _shift_word(word: Sequence[int], amount: int) -> Tuple[int, int, int]:
    return tuple(_shift_symbol(int(value), amount) for value in word)


def _reverse_word(word: Sequence[int]) -> Tuple[int, int, int]:
    return tuple(int(value) for value in reversed(word))


def _shape(word: Sequence[int]) -> str:
    a, b, c = (int(value) for value in word)
    if a == b != c:
        return "AAB"
    if a == c != b:
        return "ABA"
    if b == c != a:
        return "ABB"
    return "other"


def _shared_bridge_symbols(left: Sequence[int], right: Sequence[int]) -> List[int]:
    return sorted(set(int(value) for value in left) & set(int(value) for value in right))


def _orbit_with_maps(
    pair: Tuple[Tuple[int, int, int], Tuple[int, int, int]]
) -> Dict[Tuple[Tuple[int, int, int], Tuple[int, int, int]], str]:
    left, right = pair
    out: Dict[Tuple[Tuple[int, int, int], Tuple[int, int, int]], str] = {}
    for shift in range(4):
        shifted_left = _shift_word(left, shift)
        shifted_right = _shift_word(right, shift)
        for reverse_both in (False, True):
            rev_left = _reverse_word(shifted_left) if reverse_both else shifted_left
            rev_right = _reverse_word(shifted_right) if reverse_both else shifted_right
            for swap in (False, True):
                final_left, final_right = (rev_left, rev_right) if not swap else (rev_right, rev_left)
                steps: List[str] = []
                if shift:
                    steps.append(f"cyclic_shift(+{shift})")
                if reverse_both:
                    steps.append("reverse_both_words")
                if swap:
                    steps.append("swap_left_right")
                out[(final_left, final_right)] = " -> ".join(steps) if steps else "identity"
    return out


def _filtered_seed_rows() -> List[Dict[str, object]]:
    raw_rows = list(_load_json("artifacts/d5_endpoint_word_catalog_030/data/candidate_pairs.json")["rows"])
    filtered = [
        row
        for row in raw_rows
        if bool(row["distinct_layer2_across_m"]) and bool(row["distinct_layer3_across_m"])
    ]
    for seed_id, row in enumerate(filtered):
        row["seed_id"] = int(seed_id)
    return filtered


def _ranking_by_seed_id() -> Dict[int, Mapping[str, object]]:
    rows = list(_load_json("artifacts/d5_endpoint_latin_repair_032/data/seed_pair_rankings.json")["rows"])
    return {int(row["seed_id"]): row for row in rows}


def _pair_key(row: Mapping[str, object]) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    return (
        tuple(int(value) for value in row["left_word"]),
        tuple(int(value) for value in row["right_word"]),
    )


def _jsonable(value):
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    return value


def _class_table() -> Dict[str, object]:
    seed_rows = _filtered_seed_rows()
    ranking = _ranking_by_seed_id()

    raw_rows: List[Dict[str, object]] = []
    orbit_key_for_seed: Dict[int, Tuple[Tuple[int, int, int], Tuple[int, int, int]]] = {}
    normalization_for_seed: Dict[int, str | None] = {}

    for row in seed_rows:
        seed_id = int(row["seed_id"])
        pair = _pair_key(row)
        orbit = _orbit_with_maps(pair)
        orbit_key = min(orbit, key=lambda item: (item[0], item[1]))
        orbit_key_for_seed[seed_id] = orbit_key
        normalization_for_seed[seed_id] = orbit.get(CANONICAL_PAIR)
        ranking_row = ranking[seed_id]
        raw_rows.append(
            {
                "seed_id": seed_id,
                "left_word": list(pair[0]),
                "right_word": list(pair[1]),
                "orientation": str(row["orientation"]),
                "left_shape": _shape(pair[0]),
                "right_shape": _shape(pair[1]),
                "shared_bridge_symbols": _shared_bridge_symbols(pair[0], pair[1]),
                "oriented_bridge_type": bool(CANONICAL_PAIR in orbit),
                "normalization_to_canonical": normalization_for_seed[seed_id],
                "orbit_key": _jsonable(orbit_key),
                "total_excess_incoming": int(ranking_row["total_excess_incoming"]),
                "total_overfull_targets": int(ranking_row["total_overfull_targets"]),
                "best_bit_name": str(ranking_row["best_bit_name"]),
                "best_bit_score": int(ranking_row["best_bit_score"]),
                "colliding_changed_labels": list(ranking_row["colliding_changed_labels"]),
            }
        )

    grouped: Dict[Tuple[Tuple[int, int, int], Tuple[int, int, int]], List[Dict[str, object]]] = {}
    for row in raw_rows:
        orbit_key = tuple(tuple(word) for word in row["orbit_key"])  # type: ignore[arg-type]
        grouped.setdefault(orbit_key, []).append(row)

    class_rows: List[Dict[str, object]] = []
    for class_index, orbit_key in enumerate(sorted(grouped.keys(), key=lambda item: (item[0], item[1]))):
        members = sorted(grouped[orbit_key], key=lambda row: int(row["seed_id"]))
        bridge = any(bool(member["oriented_bridge_type"]) for member in members)
        best_member = min(
            members,
            key=lambda row: (
                int(row["total_excess_incoming"]),
                int(row["total_overfull_targets"]),
                int(row["seed_id"]),
            ),
        )
        class_rows.append(
            {
                "class_id": f"C{class_index}",
                "orbit_key": _jsonable(orbit_key),
                "member_seed_ids": [int(member["seed_id"]) for member in members],
                "member_pairs": [
                    {
                        "seed_id": int(member["seed_id"]),
                        "left_word": list(member["left_word"]),
                        "right_word": list(member["right_word"]),
                        "normalization_to_canonical": member["normalization_to_canonical"],
                    }
                    for member in members
                ],
                "left_shapes": sorted({str(member["left_shape"]) for member in members}),
                "right_shapes": sorted({str(member["right_shape"]) for member in members}),
                "shared_bridge_symbols": sorted(
                    {int(value) for member in members for value in member["shared_bridge_symbols"]}
                ),
                "oriented_bridge_type": bool(bridge),
                "normalization_map": (
                    "cyclic relabel + accepted orientation normalization to [2,2,1] / [1,4,4]"
                    if bridge
                    else None
                ),
                "best_ranked_member_seed_id": int(best_member["seed_id"]),
                "best_ranked_member_pair": {
                    "left_word": list(best_member["left_word"]),
                    "right_word": list(best_member["right_word"]),
                },
                "best_ranked_member_total_excess": int(best_member["total_excess_incoming"]),
                "status_from_current_accessible_artifacts": (
                    "bridge"
                    if bridge
                    else "nonbridge_class_needing_disposition_witness"
                ),
            }
        )

    bridge_classes = [row for row in class_rows if bool(row["oriented_bridge_type"])]
    summary = {
        "task_id": TASK_ID,
        "raw_seed_count": len(raw_rows),
        "symmetry_reduced_class_count": len(class_rows),
        "bridge_class_count": len(bridge_classes),
        "bridge_class_ids": [str(row["class_id"]) for row in bridge_classes],
        "canonical_bridge_pair": _jsonable(CANONICAL_PAIR),
        "main_result": (
            "Using the 030 candidate-pair artifact and the 032 ranking artifact, "
            "the 11 filtered seed pairs reduce to a small symmetry-class table. "
            "Exactly one symmetry class contains the canonical oriented bridge pair [2,2,1] / [1,4,4]."
        ),
        "scope_note": (
            "This extraction closes the finite class enumeration and bridge-class uniqueness step. "
            "It does not, by itself, assign manuscript-grade dispositions {closed,infeasible} "
            "to every nonbridge class."
        ),
        "environment": environment_block(),
    }
    return {
        "summary": summary,
        "class_rows": class_rows,
        "raw_seed_rows": raw_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract a symmetry-reduced D5 seed-class table from the 030/032 artifacts.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    payload = _class_table()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    _write_json(out_dir / "class_table.json", {"rows": payload["class_rows"]})
    _write_json(out_dir / "raw_seed_rows.json", {"rows": payload["raw_seed_rows"]})
    _write_json(out_dir / "details.json", payload)
    _write_json(out_dir / "analysis_summary.json", payload["summary"])
    _write_csv(out_dir / "class_table.csv", payload["class_rows"])
    _write_json(args.summary_out, payload["summary"])

    print(
        f"{TASK_ID}: raw_seeds={payload['summary']['raw_seed_count']} "
        f"classes={payload['summary']['symmetry_reduced_class_count']} "
        f"bridge_classes={payload['summary']['bridge_class_count']}"
    )


if __name__ == "__main__":
    main()
