#!/usr/bin/env python3
"""Catalog short endpoint words around mixed_008 for the diagonal representative branch."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_layer3_mode_switch_common as mode008
from torus_nd_d5_return_map_model_common import environment_block, load_witness_specs, runtime_since
from torus_nd_d5_strict_palette_context_common import DIM, encode

TASK_ID = "D5-ENDPOINT-WORD-CATALOG-030"
M_VALUES = (5, 7, 9)
WORD_LENGTH = 3
REPRESENTATIVE_W0 = 0
REPRESENTATIVE_S0 = 0


@dataclass
class PreparedSearch:
    m: int
    pre: Dict[str, object]
    baseline_nexts0: List[int]
    baseline_dir0: List[int]


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _mixed_rule() -> mode008.Rule:
    mixed = next(spec for spec in load_witness_specs() if spec.name == "mixed_008")
    return mode008.Rule.from_payload(mixed.rule_payload)


def _prepare_m(m: int, mixed_rule: mode008.Rule) -> PreparedSearch:
    signature_to_id = mode008.exact_signature_catalog((m,))["signature_to_id"]
    pre = mode008.precompute_m(m, signature_to_id)
    baseline_anchors = mode008.anchor_by_feature(pre, mixed_rule)
    baseline_nexts0 = mode008.nexts_all_for_rule(pre, baseline_anchors)[0]
    baseline_dir0 = [baseline_anchors[feature_id] for feature_id in pre["feature_ids_by_color"][0]]
    return PreparedSearch(
        m=m,
        pre=pre,
        baseline_nexts0=baseline_nexts0,
        baseline_dir0=baseline_dir0,
    )


def _initial_index(prepared: PreparedSearch, *, side: str) -> int:
    m = prepared.m
    q = m - 2
    if side == "left":
        w = (REPRESENTATIVE_W0 - 1) % m
        u = (REPRESENTATIVE_S0 - w) % m
    elif side == "right":
        w = REPRESENTATIVE_W0 % m
        u = (REPRESENTATIVE_S0 - w) % m
    else:
        raise ValueError(f"unknown side {side}")
    v = 0
    return encode(((-q - w - v - u) % m, q, w, v, u), m)


def _simulate_word(prepared: PreparedSearch, *, side: str, word: Tuple[int, ...]) -> Dict[str, object]:
    m = prepared.m
    pre = prepared.pre
    coords = pre["coords"]
    step_by_dir = pre["step_by_dir"]
    baseline_nexts0 = prepared.baseline_nexts0

    cur = _initial_index(prepared, side=side)
    start_coords = coords[cur]
    overrides: Dict[int, int] = {}
    states = [tuple(int(value) for value in start_coords)]
    dirs: List[int] = []
    for step in range(m):
        if step < len(word):
            direction = int(word[step])
            overrides[cur] = step_by_dir[direction][cur]
            nxt = overrides[cur]
        else:
            nxt = overrides.get(cur, baseline_nexts0[cur])
            cur_coords = coords[cur]
            nxt_coords = coords[nxt]
            direction = next(
                direction
                for direction in range(DIM)
                if all(
                    (int(nxt_coords[axis]) - int(cur_coords[axis])) % m == (1 if axis == direction else 0)
                    for axis in range(DIM)
                )
            )
        dirs.append(direction)
        cur = nxt
        states.append(tuple(int(value) for value in coords[cur]))

    end = coords[cur]
    return {
        "start_state": tuple(int(value) for value in start_coords),
        "end_state": tuple(int(value) for value in end),
        "next_qwu": (int(end[1]), int(end[2]), int(end[4])),
        "dv": int((int(end[3]) - int(start_coords[3])) % m),
        "dirs": tuple(dirs),
        "first_states": tuple(states[: WORD_LENGTH + 1]),
        "layer2_state": tuple(states[1]) if len(states) > 1 else None,
        "layer3_state": tuple(states[2]) if len(states) > 2 else None,
    }


def _baseline_trace(prepared: PreparedSearch, *, side: str) -> Dict[str, object]:
    return _simulate_word(prepared, side=side, word=())


def _delta_class(m: int, baseline: Mapping[str, object], trial: Mapping[str, object]) -> Tuple[int, int]:
    base_q, base_w, base_u = baseline["next_qwu"]
    trial_q, trial_w, trial_u = trial["next_qwu"]
    if base_q != trial_q:
        return (999, 999)
    return ((trial_w - base_w) % m, (trial_u - base_u) % m)


def _catalog_side(prepared_by_m: Mapping[int, PreparedSearch], *, side: str) -> Dict[str, object]:
    baselines = {m: _baseline_trace(prepared_by_m[m], side=side) for m in M_VALUES}
    rows = []
    desired_rows = []
    for word in itertools.product(range(DIM), repeat=WORD_LENGTH):
        per_m = {}
        delta_signature = []
        same_s_signature = True
        for m in M_VALUES:
            prepared = prepared_by_m[m]
            trial = _simulate_word(prepared, side=side, word=tuple(int(value) for value in word))
            delta = _delta_class(m, baselines[m], trial)
            per_m[str(m)] = {
                "next_qwu": list(trial["next_qwu"]),
                "dv": int(trial["dv"]),
                "delta_wu_relative_to_baseline": list(delta),
                "layer2_state": list(trial["layer2_state"]),
                "layer3_state": list(trial["layer3_state"]),
            }
            delta_signature.append(delta)
            same_s_signature &= (delta[0] + delta[1]) % m == 0
        row = {
            "word": list(word),
            "per_m": per_m,
            "delta_signature": [list(item) for item in delta_signature],
            "same_s_signature": same_s_signature,
        }
        rows.append(row)
        plus_class = all(delta == (1, prepared_by_m[m].m - 1) for delta, m in zip(delta_signature, M_VALUES))
        minus_class = all(delta == (prepared_by_m[m].m - 1, 1) for delta, m in zip(delta_signature, M_VALUES))
        if same_s_signature and (plus_class or minus_class):
            row["delta_type"] = "plus_w" if plus_class else "minus_w"
            desired_rows.append(row)

    desired_rows.sort(key=lambda row: row["word"])
    return {
        "side": side,
        "baseline": {
            str(m): {
                "next_qwu": list(baselines[m]["next_qwu"]),
                "dv": int(baselines[m]["dv"]),
                "layer2_state": list(baselines[m]["layer2_state"]),
                "layer3_state": list(baselines[m]["layer3_state"]),
            }
            for m in M_VALUES
        },
        "total_word_count": len(rows),
        "desired_word_count": len(desired_rows),
        "desired_words": desired_rows[:40],
    }


def _pair_candidates(left_rows: Sequence[Mapping[str, object]], right_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    out = []
    for left in left_rows:
        for right in right_rows:
            left_type = str(left["delta_type"])
            right_type = str(right["delta_type"])
            if left_type == right_type:
                continue
            distinct_layer2 = all(
                left["per_m"][str(m)]["layer2_state"] != right["per_m"][str(m)]["layer2_state"] for m in M_VALUES
            )
            distinct_layer3 = all(
                left["per_m"][str(m)]["layer3_state"] != right["per_m"][str(m)]["layer3_state"] for m in M_VALUES
            )
            out.append(
                {
                    "left_word": list(left["word"]),
                    "right_word": list(right["word"]),
                    "orientation": f"left_{left_type}__right_{right_type}",
                    "distinct_layer2_across_m": distinct_layer2,
                    "distinct_layer3_across_m": distinct_layer3,
                    "left_delta_signature": left["delta_signature"],
                    "right_delta_signature": right["delta_signature"],
                }
            )
    out.sort(
        key=lambda row: (
            not row["distinct_layer2_across_m"],
            not row["distinct_layer3_across_m"],
            row["left_word"],
            row["right_word"],
        )
    )
    return out


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Catalog short endpoint words around mixed_008.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    start = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    mixed_rule = _mixed_rule()
    prepared_by_m = {m: _prepare_m(m, mixed_rule) for m in M_VALUES}

    left_catalog = _catalog_side(prepared_by_m, side="left")
    right_catalog = _catalog_side(prepared_by_m, side="right")
    pair_rows = _pair_candidates(left_catalog["desired_words"], right_catalog["desired_words"])

    _write_json(out_dir / "left_word_catalog.json", left_catalog)
    _write_json(out_dir / "right_word_catalog.json", right_catalog)
    _write_json(out_dir / "candidate_pairs.json", {"rows": pair_rows[:80]})

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "m_values": list(M_VALUES),
        "word_length": WORD_LENGTH,
        "representative_branch": {"w0": REPRESENTATIVE_W0, "s0": REPRESENTATIVE_S0},
        "left_desired_word_count": int(left_catalog["desired_word_count"]),
        "right_desired_word_count": int(right_catalog["desired_word_count"]),
        "candidate_pair_count": len(pair_rows),
        "distinct_layer2_pair_count": sum(1 for row in pair_rows if row["distinct_layer2_across_m"]),
        "distinct_layer3_pair_count": sum(1 for row in pair_rows if row["distinct_layer3_across_m"]),
        "strongest_supported_conclusion": (
            "This artifact catalogs short endpoint words before any global Latin check. It asks whether the first "
            "honest richer branch after 029 could come from nonbaseline 3-step endpoint words that already realize "
            "the required relative ±1 change in w while keeping the same s increment and changing the intermediate "
            "state class."
        ),
    }
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    print(
        f"left_desired={left_catalog['desired_word_count']} right_desired={right_catalog['desired_word_count']} "
        f"pairs={len(pair_rows)} distinct_layer2={summary['distinct_layer2_pair_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
