#!/usr/bin/env python3
"""Fill exact and candidate M4 invariant packets for the mixed_008 full torus."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, Sequence, Tuple

import torus_nd_d5_layer3_mode_switch_common as mode008
import torus_nd_d5_rich_observable_realization as rich040
from torus_nd_d5_return_map_model_common import environment_block, load_witness_specs, runtime_since
from torus_nd_d5_strict_palette_context_common import DIM, encode, incoming_latin_all, parse_m_list

TASK_ID = "D5-M4-CANDIDATE-INVARIANT-EXTRACTION-111"
DEFAULT_EXACT_M_VALUES = (5, 7, 9)
DEFAULT_SUMMARY_M_VALUES = (5, 7, 9, 11)
PERMUTATION = list(range(DIM))


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _jsonable(value):
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    return value


def _mixed_rule() -> tuple[object, mode008.Rule]:
    spec = next(spec for spec in load_witness_specs() if spec.name == "mixed_008")
    return spec, mode008.Rule.from_payload(spec.rule_payload)


def _infer_dirs_by_color(pre: Mapping[str, object], anchors: Sequence[int]) -> List[List[int]]:
    out = [[0] * int(pre["n"]) for _ in range(DIM)]
    feature_ids_by_color = pre["feature_ids_by_color"]
    for color in range(DIM):
        color_dirs = tuple((int(anchor) + color) % DIM for anchor in anchors)
        row = out[color]
        for idx, feature_id in enumerate(feature_ids_by_color[color]):
            row[idx] = int(color_dirs[int(feature_id)])
    return out


def _pred_by_dir(pre: Mapping[str, object]) -> List[List[int]]:
    coords = pre["coords"]
    m = int(pre["m"])
    out = [[0] * len(coords) for _ in range(DIM)]
    for idx, vertex in enumerate(coords):
        for direction in range(DIM):
            pred = list(vertex)
            pred[direction] = (pred[direction] - 1) % m
            out[direction][idx] = encode(pred, m)
    return out


def _prepare_m(m: int, rule: mode008.Rule) -> Dict[str, object]:
    signature_to_id = mode008.exact_signature_catalog((m,))["signature_to_id"]
    pre = mode008.precompute_m(m, signature_to_id)
    anchors = mode008.anchor_by_feature(pre, rule)
    nexts_all = mode008.nexts_all_for_rule(pre, anchors)
    return {
        "m": int(m),
        "pre": pre,
        "anchors": anchors,
        "nexts_all": nexts_all,
        "latin_all_colors": bool(incoming_latin_all(nexts_all)),
        "dirs_by_color": _infer_dirs_by_color(pre, anchors),
        "pred_by_dir": _pred_by_dir(pre),
    }


def _coords_key(prepared: Mapping[str, object], idx: int):
    return tuple(int(value) for value in prepared["pre"]["coords"][idx])


def _feature0_key(prepared: Mapping[str, object], idx: int):
    return int(prepared["pre"]["feature_ids_by_color"][0][idx])


def _feature_profile_key(prepared: Mapping[str, object], idx: int):
    feature_ids_by_color = prepared["pre"]["feature_ids_by_color"]
    return tuple(int(feature_ids_by_color[color][idx]) for color in range(DIM))


def _full24_profile_key(prepared: Mapping[str, object], idx: int):
    coords = prepared["pre"]["coords"][idx]
    m = int(prepared["m"])
    return tuple(
        tuple(int(value) for value in rich040._simple_full24_row(coords, color, m))
        for color in range(DIM)
    )


def _candidate_key_functions() -> Dict[str, Callable[[Mapping[str, object], int], object]]:
    return {
        "coords": _coords_key,
        "feature0": _feature0_key,
        "feature_profile": _feature_profile_key,
        "full24_profile": _full24_profile_key,
    }


def _raw_packet_for_modulus(prepared: Mapping[str, object]) -> Dict[str, object]:
    m = int(prepared["m"])
    coords = prepared["pre"]["coords"]
    dirs_by_color = prepared["dirs_by_color"]
    pred_by_dir = prepared["pred_by_dir"]
    generator_row_by_state = {
        int(state_id): [int(dirs_by_color[color][state_id]) for color in range(DIM)]
        for state_id in range(len(coords))
    }

    state_catalog = []
    generator_rows = []
    predecessor_rows = []
    inverse_rows = []

    generator_rows_are_permutations = True
    generator_row_permutation_failure_count = 0
    inverse_identity_unique_everywhere = True
    failure_witnesses = []

    for state_id, vertex in enumerate(coords):
        generator_row = list(generator_row_by_state[int(state_id)])
        pred_row = [int(pred_by_dir[direction][state_id]) for direction in range(DIM)]

        state_catalog.append(
            {
                "state_id": int(state_id),
                "coords": [int(value) for value in vertex],
            }
        )
        generator_rows.append(
            {
                "state_id": int(state_id),
                "generators_by_color": generator_row,
            }
        )
        predecessor_rows.append(
            {
                "state_id": int(state_id),
                "pred_state_ids_by_generator": pred_row,
            }
        )

        if sorted(generator_row) != PERMUTATION:
            generator_rows_are_permutations = False
            generator_row_permutation_failure_count += 1
            if len(failure_witnesses) < 8:
                failure_witnesses.append(
                    {
                        "kind": "generator_row_not_permutation",
                        "state_id": int(state_id),
                        "coords": [int(value) for value in vertex],
                        "generator_row": generator_row,
                    }
                )

        incoming = []
        for color in range(DIM):
            candidates = [
                direction
                for direction in range(DIM)
                if generator_row_by_state[pred_row[direction]][color] == direction
            ]
            if len(candidates) != 1:
                inverse_identity_unique_everywhere = False
                if len(failure_witnesses) < 8:
                    failure_witnesses.append(
                        {
                            "kind": "inverse_identity_failure",
                            "state_id": int(state_id),
                            "coords": [int(value) for value in vertex],
                            "color": int(color),
                            "candidate_generators": [int(value) for value in candidates],
                            "pred_state_ids_by_generator": pred_row,
                        }
                    )
                incoming.append(-1)
            else:
                incoming.append(int(candidates[0]))

        inverse_rows.append(
            {
                "state_id": int(state_id),
                "incoming_generator_by_color": incoming,
            }
        )

    return {
        "state_count": int(len(coords)),
        "state_catalog": state_catalog,
        "generator_rows": generator_rows,
        "predecessor_rows": predecessor_rows,
        "inverse_rows": inverse_rows,
        "summary_checks": {
            "latin_all_colors": bool(prepared["latin_all_colors"]),
            "generator_rows_are_permutations": bool(generator_rows_are_permutations),
            "generator_row_permutation_failure_count": int(generator_row_permutation_failure_count),
            "predecessor_targets_realized": True,
            "inverse_identity_unique_everywhere": bool(inverse_identity_unique_everywhere),
        },
        "failure_witnesses": failure_witnesses,
        "formula_candidates": {
            "generator_readouts": [],
            "predecessor_transports": [],
            "inverse_identity": [],
        },
        "formula_fit_summary": {
            "generator_readouts_closed": False,
            "predecessor_transports_closed": False,
            "inverse_identity_closed": False,
        },
        "notes": (
            "This is a fully filled table packet for the raw vertex-coordinate invariant on the mixed_008 full torus. "
            "It closes generator, predecessor, and inverse tables on the witness's own state space, but it is not yet "
            "a valid M4 acceptance packet because the colorwise generator rows do not satisfy outgoing permutation "
            "coverage on checked moduli."
        ),
    }


def _class_size_histogram(group_sizes: Iterable[int]) -> Dict[str, int]:
    counter = Counter(int(size) for size in group_sizes)
    return {str(size): int(count) for size, count in sorted(counter.items())}


def _candidate_summary_for_modulus(
    prepared: Mapping[str, object],
    *,
    candidate_name: str,
    key_fn: Callable[[Mapping[str, object], int], object],
) -> Dict[str, object]:
    coords = prepared["pre"]["coords"]
    dirs_by_color = prepared["dirs_by_color"]
    pred_by_dir = prepared["pred_by_dir"]
    state_to_indices: Dict[object, List[int]] = defaultdict(list)

    for idx in range(len(coords)):
        state_to_indices[key_fn(prepared, idx)].append(idx)

    state_items = list(state_to_indices.items())
    state_id_by_key = {state: state_id for state_id, (state, _idxs) in enumerate(state_items)}

    generator_failure_count = 0
    predecessor_failure_count = 0
    inverse_failure_count = 0
    generator_examples = []
    predecessor_examples = []
    inverse_examples = []

    generator_rows: Dict[int, Tuple[int, ...]] = {}
    predecessor_rows: Dict[int, Tuple[int, ...]] = {}

    for state_id, (state_key, indices) in enumerate(state_items):
        generator_value_set = {
            tuple(int(dirs_by_color[color][idx]) for color in range(DIM))
            for idx in indices
        }
        if len(generator_value_set) != 1:
            generator_failure_count += 1
            if len(generator_examples) < 6:
                generator_examples.append(
                    {
                        "state_id": int(state_id),
                        "state_repr": _jsonable(state_key),
                        "class_size": int(len(indices)),
                        "sample_vertices": [
                            [int(value) for value in coords[idx]]
                            for idx in indices[: min(4, len(indices))]
                        ],
                        "observed_generator_rows": [
                            [int(value) for value in row]
                            for row in list(sorted(generator_value_set))[: min(4, len(generator_value_set))]
                        ],
                    }
                )
        else:
            generator_rows[state_id] = next(iter(generator_value_set))

        pred_targets_by_generator = []
        predecessor_ok = True
        pred_target_sets = []
        for direction in range(DIM):
            target_state_ids = {
                state_id_by_key[key_fn(prepared, pred_by_dir[direction][idx])]
                for idx in indices
            }
            pred_target_sets.append(target_state_ids)
            if len(target_state_ids) != 1:
                predecessor_ok = False
                pred_targets_by_generator.append(sorted(int(value) for value in target_state_ids))
            else:
                pred_targets_by_generator.append(int(next(iter(target_state_ids))))
        if not predecessor_ok:
            predecessor_failure_count += 1
            if len(predecessor_examples) < 6:
                predecessor_examples.append(
                    {
                        "state_id": int(state_id),
                        "state_repr": _jsonable(state_key),
                        "class_size": int(len(indices)),
                        "sample_vertices": [
                            [int(value) for value in coords[idx]]
                            for idx in indices[: min(4, len(indices))]
                        ],
                        "pred_targets_by_generator": _jsonable(pred_targets_by_generator),
                        "sample_pred_vertices_by_generator": [
                            [
                                [int(value) for value in coords[pred_by_dir[direction][idx]]]
                                for idx in indices[: min(3, len(indices))]
                            ]
                            for direction in range(DIM)
                        ],
                    }
                )
        else:
            predecessor_rows[state_id] = tuple(int(value) for value in pred_targets_by_generator)

    if generator_failure_count == 0 and predecessor_failure_count == 0:
        for state_id, generator_row in generator_rows.items():
            for color in range(DIM):
                candidates = [
                    direction
                    for direction in range(DIM)
                    if generator_rows[predecessor_rows[state_id][direction]][color] == direction
                ]
                if len(candidates) != 1:
                    inverse_failure_count += 1
                    if len(inverse_examples) < 6:
                        inverse_examples.append(
                            {
                                "state_id": int(state_id),
                                "state_repr": _jsonable(state_items[state_id][0]),
                                "color": int(color),
                                "candidate_generators": [int(value) for value in candidates],
                                "generator_row": [int(value) for value in generator_row],
                                "pred_state_ids_by_generator": [int(value) for value in predecessor_rows[state_id]],
                            }
                        )

    exact_generator_rows = generator_failure_count == 0
    exact_predecessor_transports = predecessor_failure_count == 0
    exact_inverse_identity = inverse_failure_count == 0 and exact_generator_rows and exact_predecessor_transports

    return {
        "candidate_name": candidate_name,
        "state_count": int(len(state_items)),
        "class_size_histogram": _class_size_histogram(len(indices) for _state, indices in state_items),
        "generator_rows_exact": bool(exact_generator_rows),
        "predecessor_transports_exact": bool(exact_predecessor_transports),
        "inverse_identity_exact": bool(exact_inverse_identity),
        "generator_failure_count": int(generator_failure_count),
        "predecessor_failure_count": int(predecessor_failure_count),
        "inverse_failure_count": int(inverse_failure_count),
        "generator_rows_are_permutations_when_defined": bool(
            all(sorted(generator_rows[state_id]) == PERMUTATION for state_id in generator_rows)
        ),
        "failure_examples": {
            "generator_row_failures": generator_examples,
            "predecessor_transport_failures": predecessor_examples,
            "inverse_identity_failures": inverse_examples,
        },
    }


def _exact_packet_payload(per_modulus: Mapping[str, object]) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "target": "filled raw-coordinate generator/predecessor/inverse table packet for M4 debugging",
        "invariant_name": "raw_vertex_coordinates",
        "normalization": {
            "description": "state_id is the torus vertex index in encode(coords,m) order",
            "state_id_format": "integer vertex index",
        },
        "required_sections": [
            "state_catalog",
            "generator_rows",
            "predecessor_rows",
            "inverse_rows",
            "summary_checks",
            "failure_witnesses",
        ],
        "per_modulus": dict(per_modulus),
        "notes": (
            "This packet is intentionally over-resolved. It proves that the M4 table-extraction pipeline works on the "
            "actual mixed_008 full torus and exposes the next obstruction explicitly: even on raw coordinates, the "
            "current witness rows do not yet satisfy the outgoing-permutation coverage required by the selector criterion."
        ),
    }


def run_extraction(*, exact_m_values: Sequence[int], summary_m_values: Sequence[int]) -> Dict[str, object]:
    started = time.perf_counter()
    witness_spec, rule = _mixed_rule()
    all_m_values = tuple(sorted(set(int(m) for m in list(exact_m_values) + list(summary_m_values))))
    prepared_by_m = {int(m): _prepare_m(int(m), rule) for m in all_m_values}

    exact_packet = _exact_packet_payload(
        {
            str(m): _raw_packet_for_modulus(prepared_by_m[int(m)])
            for m in exact_m_values
        }
    )

    candidate_key_functions = _candidate_key_functions()
    candidate_summary = {
        "task_id": TASK_ID,
        "target": "candidate compression audit for M4 invariant automata",
        "witness_name": witness_spec.name,
        "summary_m_values": [int(m) for m in summary_m_values],
        "candidates": list(candidate_key_functions.keys()),
        "per_modulus": {
            str(m): {
                "latin_all_colors": bool(prepared_by_m[int(m)]["latin_all_colors"]),
                "candidates": {
                    name: _candidate_summary_for_modulus(
                        prepared_by_m[int(m)],
                        candidate_name=name,
                        key_fn=key_fn,
                    )
                    for name, key_fn in candidate_key_functions.items()
                },
            }
            for m in summary_m_values
        },
        "notes": (
            "The raw coordinate invariant closes exactly. The smaller candidate invariants are tested against the "
            "same generator/predecessor/inverse criteria to isolate where compact M4 compression still fails."
        ),
    }

    summary = {
        "task_id": TASK_ID,
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
        "raw_packet_m_values": [int(m) for m in exact_m_values],
        "summary_m_values": [int(m) for m in summary_m_values],
        "witness": {
            "name": witness_spec.name,
            "family": witness_spec.family,
            "role": witness_spec.role,
            "source": witness_spec.source,
        },
        "raw_packet_result": {
            str(m): {
                "state_count": int(exact_packet["per_modulus"][str(m)]["state_count"]),
                "latin_all_colors": bool(exact_packet["per_modulus"][str(m)]["summary_checks"]["latin_all_colors"]),
                "generator_rows_are_permutations": bool(
                    exact_packet["per_modulus"][str(m)]["summary_checks"]["generator_rows_are_permutations"]
                ),
                "generator_row_permutation_failure_count": int(
                    exact_packet["per_modulus"][str(m)]["summary_checks"]["generator_row_permutation_failure_count"]
                ),
                "inverse_identity_unique_everywhere": bool(
                    exact_packet["per_modulus"][str(m)]["summary_checks"]["inverse_identity_unique_everywhere"]
                ),
            }
            for m in exact_m_values
        },
        "candidate_snapshot": {
            str(m): {
                name: {
                    "state_count": int(candidate_summary["per_modulus"][str(m)]["candidates"][name]["state_count"]),
                    "generator_rows_exact": bool(
                        candidate_summary["per_modulus"][str(m)]["candidates"][name]["generator_rows_exact"]
                    ),
                    "generator_rows_are_permutations_when_defined": bool(
                        candidate_summary["per_modulus"][str(m)]["candidates"][name]["generator_rows_are_permutations_when_defined"]
                    ),
                    "predecessor_transports_exact": bool(
                        candidate_summary["per_modulus"][str(m)]["candidates"][name]["predecessor_transports_exact"]
                    ),
                    "inverse_identity_exact": bool(
                        candidate_summary["per_modulus"][str(m)]["candidates"][name]["inverse_identity_exact"]
                    ),
                    "generator_failure_count": int(
                        candidate_summary["per_modulus"][str(m)]["candidates"][name]["generator_failure_count"]
                    ),
                    "predecessor_failure_count": int(
                        candidate_summary["per_modulus"][str(m)]["candidates"][name]["predecessor_failure_count"]
                    ),
                }
                for name in candidate_key_functions
            }
            for m in summary_m_values
        },
        "main_result": (
            "The extraction pipeline can fully populate raw-coordinate generator/predecessor/inverse tables on the "
            "mixed_008 full torus, but even raw coordinates do not satisfy the outgoing-permutation coverage demanded "
            "by M4. Separately, feature_profile and full24_profile keep generator readout exact while still failing "
            "deterministic predecessor transport on checked moduli, and feature0 already fails at the generator stage."
        ),
    }

    return {
        "exact_packet": exact_packet,
        "candidate_summary": candidate_summary,
        "run_summary": summary,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fill exact and candidate M4 invariant packets for the mixed_008 full torus.")
    parser.add_argument(
        "--exact-m-list",
        default=",".join(str(value) for value in DEFAULT_EXACT_M_VALUES),
        help="comma-separated moduli for the exact raw-coordinate packet",
    )
    parser.add_argument(
        "--summary-m-list",
        default=",".join(str(value) for value in DEFAULT_SUMMARY_M_VALUES),
        help="comma-separated moduli for the candidate compression summary",
    )
    parser.add_argument("--exact-packet-out", type=Path, required=True, help="write the exact packet JSON here")
    parser.add_argument("--candidate-summary-out", type=Path, required=True, help="write the candidate summary JSON here")
    parser.add_argument("--run-summary-out", type=Path, required=True, help="write the top-level summary JSON here")
    args = parser.parse_args(argv)

    exact_m_values = parse_m_list(args.exact_m_list)
    summary_m_values = parse_m_list(args.summary_m_list)
    payload = run_extraction(exact_m_values=exact_m_values, summary_m_values=summary_m_values)
    _write_json(args.exact_packet_out, payload["exact_packet"])
    _write_json(args.candidate_summary_out, payload["candidate_summary"])
    _write_json(args.run_summary_out, payload["run_summary"])
    print(json.dumps(payload["run_summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
