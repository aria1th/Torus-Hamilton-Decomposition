#!/usr/bin/env python3
"""Shared helpers for the D5 tail-hypergraph and automaton-factor analysis."""

from __future__ import annotations

import json
import platform
from collections import Counter, defaultdict
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from torus_nd_d5_master_field_quotient_family import (
    SCHEMA_PHASE_ALIGN,
    color_map_from_table,
    state_for_vertex,
)

TASK_ID = "D5-TAIL-AUTOMATON-BIT-EXTRACTION-001"
STATE_SPACE_KEY = (5, 7, 9, 11, 13)
START_TOKEN = "<START>"
END_TOKEN = "<END>"
BASE_FEATURE_TOKENS = (
    "state_name",
    "prev_state_name",
    "next_state_name",
    "entry0_state_name",
    "entry1_state_name",
    "entry2_state_name",
)


@dataclass(frozen=True)
class Occurrence:
    m: int
    delta: int
    step_index: int
    coords: Tuple[int, int, int, int, int]
    state_name: str
    layer_bucket: object
    prev_state_name: str
    next_state_name: str
    entry0_state_name: str
    entry1_state_name: str
    entry2_state_name: str

    def token(self, name: str) -> object:
        return getattr(self, name)


def parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def rich_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def environment_payload() -> Dict[str, object]:
    return {"python_version": platform.python_version(), "rich_version": rich_version()}


def load_field_table(field_json: Path) -> Tuple[dict, Dict[int, Tuple[int, ...]]]:
    field = json.loads(field_json.read_text())
    table = {int(row["state_id"]): tuple(row["permutation"]) for row in field["anchor_table"]["rows"]}
    return field, table


def delta_value(coords: Sequence[int], m: int) -> int:
    return (coords[3] - coords[1]) % m


def unique_state_label(state: Tuple[object, Tuple[int, ...]]) -> str:
    return f"L={state[0]}|sig=[{','.join(str(value) for value in state[1])}]"


def serialize_state_support_rows(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    return [dict(row) for row in rows]


def collect_nonzero_occurrences(
    table: Dict[int, Sequence[int]],
    *,
    m: int,
    state_space_key: Tuple[int, ...] = STATE_SPACE_KEY,
) -> List[Occurrence]:
    occurrences: List[Occurrence] = []
    for q in range(m):
        for w in range(m):
            for v in range(m):
                for u in range(m):
                    cur = ((-q - w - v - u) % m, q, w, v, u)
                    path = []
                    for step_index in range(m):
                        state = state_for_vertex(cur, m, SCHEMA_PHASE_ALIGN)
                        path.append(
                            {
                                "step_index": step_index,
                                "coords": tuple(cur),
                                "state_name": unique_state_label(state),
                                "layer_bucket": state[0],
                                "delta": delta_value(cur, m),
                            }
                        )
                        cur = color_map_from_table(table, SCHEMA_PHASE_ALIGN, m, cur, 0, state_space_key)
                    for step_index, row in enumerate(path):
                        if row["delta"] == 0:
                            continue
                        occurrences.append(
                            Occurrence(
                                m=m,
                                delta=row["delta"],
                                step_index=step_index,
                                coords=row["coords"],
                                state_name=row["state_name"],
                                layer_bucket=row["layer_bucket"],
                                prev_state_name=path[step_index - 1]["state_name"] if step_index > 0 else START_TOKEN,
                                next_state_name=path[step_index + 1]["state_name"] if step_index + 1 < len(path) else END_TOKEN,
                                entry0_state_name=path[0]["state_name"],
                                entry1_state_name=path[1]["state_name"] if len(path) > 1 else END_TOKEN,
                                entry2_state_name=path[2]["state_name"] if len(path) > 2 else END_TOKEN,
                            )
                        )
    return occurrences


def state_support_rows(occurrences: Sequence[Occurrence], *, m: int) -> List[Dict[str, object]]:
    support = defaultdict(set)
    examples = {}
    occurrence_count = Counter()
    layer_bucket = {}
    for row in occurrences:
        support[row.state_name].add(row.delta)
        occurrence_count[row.state_name] += 1
        layer_bucket[row.state_name] = row.layer_bucket
        examples.setdefault((row.state_name, row.delta), list(row.coords))

    rows = []
    for state_key, delta_values in support.items():
        sorted_deltas = sorted(delta_values)
        rows.append(
            {
                "state_name": state_key,
                "layer_bucket": layer_bucket[state_key],
                "delta_values": sorted_deltas,
                "delta_support_size": len(sorted_deltas),
                "occurrence_count": occurrence_count[state_key],
                "all_nonzero": sorted_deltas == list(range(1, m)),
                "example_rows": [
                    {"delta": delta, "coords": examples[(state_key, delta)]}
                    for delta in sorted_deltas[: min(6, len(sorted_deltas))]
                ],
            }
        )
    rows.sort(
        key=lambda row: (
            0 if row["delta_support_size"] > 1 else 1,
            -row["delta_support_size"],
            str(row["layer_bucket"]),
            row["state_name"],
        )
    )
    return rows


def hyperedge_weight_rows(occurrences: Sequence[Occurrence]) -> List[Dict[str, object]]:
    support = defaultdict(set)
    support_examples = {}
    for row in occurrences:
        support[row.state_name].add(row.delta)
        support_examples.setdefault((row.state_name, row.delta), list(row.coords))

    support_weights = Counter(tuple(sorted(delta_values)) for delta_values in support.values() if len(delta_values) > 1)
    example_state = {}
    for state_key, delta_values in support.items():
        support_key = tuple(sorted(delta_values))
        if len(support_key) <= 1 or support_key in example_state:
            continue
        example_state[support_key] = {
            "state_name": state_key,
            "example_rows": [
                {"delta": delta, "coords": support_examples[(state_key, delta)]}
                for delta in support_key[: min(6, len(support_key))]
            ],
        }

    rows = []
    for support_key, weight in sorted(
        support_weights.items(),
        key=lambda item: (-len(item[0]), -item[1], item[0]),
    ):
        rows.append(
            {
                "delta_values": list(support_key),
                "support_size": len(support_key),
                "weight": weight,
                "example_state_name": example_state[support_key]["state_name"],
                "example_rows": example_state[support_key]["example_rows"],
            }
        )
    return rows


def support_rows_to_weight_map(rows: Sequence[Dict[str, object]]) -> Dict[int, int]:
    out = {}
    for row in rows:
        mask = 0
        for delta in row["delta_values"]:
            mask |= 1 << (int(delta) - 1)
        out[mask] = out.get(mask, 0) + int(row["weight"])
    return out


def subset_mask_to_deltas(mask: int, *, vertex_count: int) -> List[int]:
    return [delta for delta in range(1, vertex_count + 1) if mask & (1 << (delta - 1))]


def serialize_feature_value(value: object) -> object:
    if isinstance(value, tuple):
        return list(value)
    return value


def family_name(tokens: Sequence[str]) -> str:
    aliases = {
        ("state_name",): "state",
        ("prev_state_name",): "pred",
        ("next_state_name",): "next",
        ("prev_state_name", "state_name"): "pred_cur",
        ("state_name", "next_state_name"): "cur_next",
        ("prev_state_name", "state_name", "next_state_name"): "pred_cur_next",
        ("entry0_state_name",): "entry0",
        ("entry1_state_name",): "entry1",
        ("entry2_state_name",): "entry2",
        ("entry0_state_name", "entry1_state_name"): "entry01",
        ("entry1_state_name", "entry2_state_name"): "entry12",
        ("entry0_state_name", "entry1_state_name", "state_name"): "entry01_cur",
        ("entry1_state_name", "entry2_state_name", "state_name"): "entry12_cur",
    }
    token_tuple = tuple(tokens)
    if token_tuple in aliases:
        return aliases[token_tuple]
    return "__".join(token.replace("_state_name", "").replace("_name", "") for token in token_tuple)


def candidate_family_tokens() -> List[Tuple[str, ...]]:
    families = []
    base = list(BASE_FEATURE_TOKENS)
    for token in base:
        families.append((token,))
    for left_index in range(len(base)):
        for right_index in range(left_index + 1, len(base)):
            families.append((base[left_index], base[right_index]))
    for first in range(len(base)):
        for second in range(first + 1, len(base)):
            for third in range(second + 1, len(base)):
                families.append((base[first], base[second], base[third]))
    families.extend(
        [
            ("entry0_state_name", "entry1_state_name", "entry2_state_name", "state_name"),
            ("entry0_state_name", "entry1_state_name", "state_name", "next_state_name"),
            ("entry0_state_name", "entry1_state_name", "prev_state_name", "state_name"),
            ("entry0_state_name", "entry1_state_name", "prev_state_name", "state_name", "next_state_name"),
        ]
    )
    return families


def feature_value_for_tokens(row: Occurrence, tokens: Sequence[str]) -> object:
    if len(tokens) == 1:
        return row.token(tokens[0])
    return tuple(row.token(token) for token in tokens)
