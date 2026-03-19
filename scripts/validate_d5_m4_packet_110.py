#!/usr/bin/env python3
"""Validate the shape and local consistency of a D5 M4 invariant packet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_TOP_LEVEL = {
    "task_id",
    "target",
    "invariant_name",
    "normalization",
    "required_sections",
    "per_modulus",
}

REQUIRED_MODULUS_KEYS = {
    "state_count",
    "state_catalog",
    "generator_rows",
    "predecessor_rows",
    "inverse_rows",
    "summary_checks",
    "failure_witnesses",
}


def _fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def _expect_keys(mapping: Mapping[str, object], keys: set[str], label: str) -> None:
    missing = sorted(key for key in keys if key not in mapping)
    if missing:
        _fail(f"{label} missing keys: {', '.join(missing)}")


def _expect_int_range(value: object, low: int, high: int, label: str) -> None:
    if not isinstance(value, int) or value < low or value > high:
        _fail(f"{label} must be an int in [{low}, {high}]")


def _validate_modulus(m_text: str, payload: Mapping[str, object]) -> None:
    _expect_keys(payload, REQUIRED_MODULUS_KEYS, f"per_modulus[{m_text}]")

    state_catalog = payload["state_catalog"]
    generator_rows = payload["generator_rows"]
    predecessor_rows = payload["predecessor_rows"]
    inverse_rows = payload["inverse_rows"]

    if not isinstance(state_catalog, list):
        _fail(f"per_modulus[{m_text}].state_catalog must be a list")
    if not isinstance(generator_rows, list):
        _fail(f"per_modulus[{m_text}].generator_rows must be a list")
    if not isinstance(predecessor_rows, list):
        _fail(f"per_modulus[{m_text}].predecessor_rows must be a list")
    if not isinstance(inverse_rows, list):
        _fail(f"per_modulus[{m_text}].inverse_rows must be a list")

    state_ids = []
    for idx, row in enumerate(state_catalog):
        if not isinstance(row, dict):
            _fail(f"state_catalog[{idx}] must be an object")
        if "state_id" not in row:
            _fail(f"state_catalog[{idx}] missing state_id")
        state_ids.append(row["state_id"])

    if len(set(state_ids)) != len(state_ids):
        _fail(f"per_modulus[{m_text}] state_id values must be unique")

    state_id_set = set(state_ids)
    if int(payload["state_count"]) != len(state_ids):
        _fail(f"per_modulus[{m_text}].state_count does not match state_catalog length")

    generator_map: Dict[str, List[int]] = {}
    for idx, row in enumerate(generator_rows):
        if not isinstance(row, dict):
            _fail(f"generator_rows[{idx}] must be an object")
        state_id = row.get("state_id")
        generators = row.get("generators_by_color")
        if state_id not in state_id_set:
            _fail(f"generator_rows[{idx}] references unknown state_id")
        if not isinstance(generators, list) or len(generators) != 5:
            _fail(f"generator_rows[{idx}].generators_by_color must be a length-5 list")
        for j, value in enumerate(generators):
            _expect_int_range(value, 0, 4, f"generator_rows[{idx}].generators_by_color[{j}]")
        if sorted(generators) != [0, 1, 2, 3, 4]:
            _fail(f"generator_rows[{idx}] is not a permutation of 0..4")
        generator_map[state_id] = generators

    predecessor_map: Dict[str, List[str]] = {}
    for idx, row in enumerate(predecessor_rows):
        if not isinstance(row, dict):
            _fail(f"predecessor_rows[{idx}] must be an object")
        state_id = row.get("state_id")
        preds = row.get("pred_state_ids_by_generator")
        if state_id not in state_id_set:
            _fail(f"predecessor_rows[{idx}] references unknown state_id")
        if not isinstance(preds, list) or len(preds) != 5:
            _fail(f"predecessor_rows[{idx}].pred_state_ids_by_generator must be a length-5 list")
        for j, target in enumerate(preds):
            if target not in state_id_set:
                _fail(f"predecessor_rows[{idx}].pred_state_ids_by_generator[{j}] references unknown state_id")
        predecessor_map[state_id] = preds

    inverse_map: Dict[str, List[int]] = {}
    for idx, row in enumerate(inverse_rows):
        if not isinstance(row, dict):
            _fail(f"inverse_rows[{idx}] must be an object")
        state_id = row.get("state_id")
        incoming = row.get("incoming_generator_by_color")
        if state_id not in state_id_set:
            _fail(f"inverse_rows[{idx}] references unknown state_id")
        if not isinstance(incoming, list) or len(incoming) != 5:
            _fail(f"inverse_rows[{idx}].incoming_generator_by_color must be a length-5 list")
        for c, value in enumerate(incoming):
            _expect_int_range(value, 0, 4, f"inverse_rows[{idx}].incoming_generator_by_color[{c}]")
        inverse_map[state_id] = incoming

    # Internal local inverse-identity check.
    for state_id in state_id_set:
        if state_id not in generator_map:
            _fail(f"missing generator row for state_id {state_id}")
        if state_id not in predecessor_map:
            _fail(f"missing predecessor row for state_id {state_id}")
        if state_id not in inverse_map:
            _fail(f"missing inverse row for state_id {state_id}")
        for color in range(5):
            candidates = []
            for generator in range(5):
                pred_state = predecessor_map[state_id][generator]
                if generator_map[pred_state][color] == generator:
                    candidates.append(generator)
            if len(candidates) != 1:
                _fail(
                    f"local inverse identity fails at state_id {state_id}, color {color}: candidates={candidates}"
                )
            if inverse_map[state_id][color] != candidates[0]:
                _fail(
                    f"inverse_rows disagrees at state_id {state_id}, color {color}: "
                    f"recorded={inverse_map[state_id][color]} actual={candidates[0]}"
                )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the shape and local consistency of a D5 M4 invariant packet.")
    parser.add_argument("packet", type=Path, help="Path to the packet JSON file.")
    args = parser.parse_args()

    payload = json.loads(args.packet.read_text())
    if not isinstance(payload, dict):
        _fail("top-level JSON value must be an object")
    _expect_keys(payload, REQUIRED_TOP_LEVEL, "top-level packet")

    per_modulus = payload["per_modulus"]
    if not isinstance(per_modulus, dict):
        _fail("per_modulus must be an object")

    for m_text, modulus_payload in per_modulus.items():
        if not isinstance(modulus_payload, dict):
            _fail(f"per_modulus[{m_text}] must be an object")
        _validate_modulus(m_text, modulus_payload)

    print(f"VALID: {args.packet}")


if __name__ == "__main__":
    main()
