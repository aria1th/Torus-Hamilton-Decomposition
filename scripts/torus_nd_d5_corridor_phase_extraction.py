#!/usr/bin/env python3
"""Extract the reduced corridor-phase model for the best-seed unresolved channel."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_endpoint_latin_repair as seed032
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-CORRIDOR-PHASE-EXTRACTION-034"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M_VALUES = (11,)
ALL_M_VALUES = PRIMARY_M_VALUES + CONTROL_M_VALUES
BEST_LEFT_WORD = (2, 2, 1)
BEST_RIGHT_WORD = (1, 4, 4)
REPRESENTATIVE_W0 = 0
REPRESENTATIVE_S0 = 0


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _coords_payload(prepared: seed032.PreparedSearch, idx: int) -> Dict[str, int]:
    coords = prepared.pre["coords"][idx]
    w = int(coords[2])
    u = int(coords[4])
    return {
        "x0": int(coords[0]),
        "q": int(coords[1]),
        "w": w,
        "v": int(coords[3]),
        "u": u,
        "s": int((w + u) % prepared.m),
        "layer": int(sum(coords) % prepared.m),
    }


def _phase_pair(prepared: seed032.PreparedSearch, idx: int) -> Tuple[int, int]:
    payload = _coords_payload(prepared, idx)
    return int(payload["s"]), int(payload["layer"])


def _build_best_seed(prepared: seed032.PreparedSearch) -> Tuple[List[List[int]], Dict[str, object]]:
    nexts_all, meta = seed032._build_candidate(
        prepared,
        w0=REPRESENTATIVE_W0,
        s0=REPRESENTATIVE_S0,
        left_word=BEST_LEFT_WORD,
        right_word=BEST_RIGHT_WORD,
        cocycle_defect="none",
        repair=None,
    )
    if nexts_all is None:
        raise ValueError("best seed unexpectedly failed to build")
    return nexts_all, meta


def _hole_l1_set(prepared: seed032.PreparedSearch, row: Sequence[int]) -> set[int]:
    indegree = [0] * prepared.pre["n"]
    for idx, nxt in enumerate(row):
        indegree[nxt] += 1
    out = set()
    for idx, value in enumerate(indegree):
        if value != 0:
            continue
        payload = _coords_payload(prepared, idx)
        if payload["q"] == prepared.m - 1 and payload["w"] == prepared.m - 1 and payload["layer"] == 2:
            out.add(idx)
    return out


def _phase_rule(m: int, rho: int, phase: Tuple[int, int]) -> Tuple[int, int]:
    s_value, layer = phase
    if layer == 1:
        return ((s_value + 1) % m, 2)
    if layer == 2 and s_value == rho:
        return ((s_value + 1) % m, 3)
    return (s_value, (layer + 1) % m)


def _small_orbit_formula(m: int, rho: int) -> List[Tuple[int, int]]:
    return sorted(
        [(rho, layer) for layer in range(m) if layer != 2] + [((rho + 1) % m, 2)]
    )


def _extract_one_source(
    prepared: seed032.PreparedSearch,
    row: Sequence[int],
    labels: Sequence[str],
    source_index: int,
    hole_l1: set[int],
) -> Dict[str, object]:
    step_by_dir = prepared.pre["step_by_dir"]
    current = step_by_dir[2][source_index]
    phase_seen: Dict[Tuple[int, int], int] = {}
    phase_sequence: List[Tuple[int, int]] = []
    state_sequence: List[Dict[str, int]] = []
    while True:
        phase = _phase_pair(prepared, current)
        if phase in phase_seen:
            repeat_from = phase_seen[phase]
            break
        phase_seen[phase] = len(phase_sequence)
        phase_sequence.append(phase)
        state_sequence.append(_coords_payload(prepared, current))
        current = row[current]

    current = step_by_dir[2][source_index]
    delay = 0
    seen_states = set()
    exit_payload = None
    exit_dirs: List[int] = []
    while current not in seen_states:
        seen_states.add(current)
        exit_dirs = [direction for direction in range(5) if step_by_dir[direction][current] in hole_l1]
        if exit_dirs:
            exit_payload = _coords_payload(prepared, current)
            break
        current = row[current]
        delay += 1
    if exit_payload is None:
        raise ValueError("failed to locate first H_L1 exit")

    source_payload = _coords_payload(prepared, source_index)
    rho = int((source_payload["u"] + 1) % prepared.m)
    missing = sorted(set((s_value, layer) for s_value in range(prepared.m) for layer in range(prepared.m)) - set(phase_sequence))
    extracted_transition_ok = all(
        _phase_rule(prepared.m, rho, phase_sequence[idx]) == phase_sequence[(idx + 1) % len(phase_sequence)]
        for idx in range(len(phase_sequence))
    )
    return {
        "source_index": int(source_index),
        "source_coords": source_payload,
        "rho": rho,
        "entry_phase": list(phase_sequence[0]),
        "phase_period": len(phase_sequence) - repeat_from,
        "phase_sequence_sample": [list(phase) for phase in phase_sequence[: min(20, len(phase_sequence))]],
        "missing_small_orbit": [list(phase) for phase in missing],
        "missing_formula": [list(phase) for phase in _small_orbit_formula(prepared.m, rho)],
        "phase_rule_matches_extraction": bool(extracted_transition_ok),
        "first_exit_delay": int(delay),
        "first_exit_phase": [int(exit_payload["s"]), int(exit_payload["layer"])],
        "first_exit_dirs": [int(value) for value in exit_dirs],
        "phase_residue_mod_period": int(delay % len(phase_sequence)),
    }


def _per_m_rows(m: int) -> Dict[str, object]:
    prepared = seed032._prepare_m(m, seed032._mixed_rule())
    nexts_all, meta = _build_best_seed(prepared)
    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    coords = prepared.pre["coords"]
    hole_l1 = _hole_l1_set(prepared, row)

    source_rows = []
    for u_value in range(1, m):
        source_index = next(idx for idx, label in enumerate(labels) if label == "R1" and int(coords[idx][4]) == u_value)
        source_rows.append(_extract_one_source(prepared, row, labels, source_index, hole_l1))

    phase_periods = Counter(row["phase_period"] for row in source_rows)
    delay_by_u = {str(row["source_coords"]["u"]): int(row["first_exit_delay"]) for row in source_rows}
    residues = Counter(row["phase_residue_mod_period"] for row in source_rows)
    exit_dirs = Counter(tuple(row["first_exit_dirs"]) for row in source_rows)
    exceptional_rows = [row for row in source_rows if row["source_coords"]["u"] == 3]
    regular_rows = [row for row in source_rows if row["source_coords"]["u"] != 3]

    period = m * (m - 1)
    short_delay = regular_rows[0]["first_exit_delay"]
    long_delay = exceptional_rows[0]["first_exit_delay"]
    phase_residue = regular_rows[0]["phase_residue_mod_period"]
    return {
        "m": int(m),
        "phase_model": {
            "projection": "(s, layer)",
            "rule": "F_rho(s,layer) = (s+1,2) if layer=1; (s+1,3) if (s,layer)=(rho,2); else (s,layer+1)",
            "rho_definition": "rho = u_source + 1 mod m",
            "large_orbit_size": int(period),
            "small_orbit_size": int(m),
            "large_orbit_formula": "Z_m^2 minus the small orbit M_rho",
            "small_orbit_formula": "M_rho = {(rho,layer): layer != 2} union {(rho+1,2)}",
        },
        "verifications": {
            "all_phase_periods_equal_m_m_minus_1": bool(phase_periods == Counter({period: m - 1})),
            "all_phase_rules_match": bool(all(row["phase_rule_matches_extraction"] for row in source_rows)),
            "all_missing_sets_match_formula": bool(
                all(
                    sorted(tuple(pair) for pair in row["missing_small_orbit"])
                    == sorted(tuple(pair) for pair in row["missing_formula"])
                    for row in source_rows
                )
            ),
            "short_formula_matches": bool(short_delay == (m - 3) * (m**2) - 1),
            "long_formula_matches": bool(long_delay == (m - 3) * (m**2) - 1 + m * (m - 1)),
            "residue_formula_matches": bool(phase_residue == m**2 - 3 * m - 1),
            "long_minus_short_equals_period": bool(long_delay - short_delay == period),
        },
        "delay_summary": {
            "period": int(period),
            "delay_by_source_u": delay_by_u,
            "short_family_delay": int(short_delay),
            "long_family_delay": int(long_delay),
            "long_minus_short": int(long_delay - short_delay),
            "phase_residue": int(phase_residue),
            "short_formula": int((m - 3) * (m**2) - 1),
            "long_formula": int((m - 3) * (m**2) - 1 + m * (m - 1)),
            "residue_formula": int(m**2 - 3 * m - 1),
            "regular_source_condition": "u_source != 3",
            "exceptional_source_condition": "u_source = 3",
        },
        "exit_summary": {
            "exit_dirs": {str(key): int(value) for key, value in sorted(exit_dirs.items())},
            "regular_exit_phase_formula": "(u_source - 3 mod m, 1)",
            "regular_exit_dir": [2],
            "exceptional_exit_phase_formula": "(0, 1)",
            "exceptional_exit_dir": [1],
        },
        "source_rows": source_rows,
        "residue_histogram": {str(key): int(value) for key, value in sorted(residues.items())},
    }


def _analysis_summary(started: float, per_m_rows: Mapping[str, object]) -> Dict[str, object]:
    primary_rows = [per_m_rows[str(m)] for m in PRIMARY_M_VALUES]
    return {
        "task_id": TASK_ID,
        "best_seed": {
            "left_word": list(BEST_LEFT_WORD),
            "right_word": list(BEST_RIGHT_WORD),
            "w0": REPRESENTATIVE_W0,
            "s0": REPRESENTATIVE_S0,
        },
        "summary": {
            "main_result": "the unresolved R1->H_L1 channel already factors through a reduced corridor-phase model on (s, layer)",
            "phase_rule": "after the initial R1 alt-2 entry, the BBB corridor follows the exact source-parameterized map F_rho on (s, layer)",
            "orbit_split": "for every source slice, the projected phase space splits into one small orbit of size m and one large orbit of size m(m-1)",
            "phase_verdict": "the short and long delay families differ by exactly one full large-orbit lap m(m-1), so the missing state is orbit phase rather than a tiny generic transducer state",
        },
        "per_m": {
            str(m): {
                "large_orbit_size": int(per_m_rows[str(m)]["phase_model"]["large_orbit_size"]),
                "small_orbit_size": int(per_m_rows[str(m)]["phase_model"]["small_orbit_size"]),
                "short_family_delay": int(per_m_rows[str(m)]["delay_summary"]["short_family_delay"]),
                "long_family_delay": int(per_m_rows[str(m)]["delay_summary"]["long_family_delay"]),
                "period_difference": int(per_m_rows[str(m)]["delay_summary"]["long_minus_short"]),
                "phase_residue": int(per_m_rows[str(m)]["delay_summary"]["phase_residue"]),
            }
            for m in ALL_M_VALUES
        },
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the reduced corridor-phase model for the best-seed unresolved channel.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    per_m_rows = {str(m): _per_m_rows(m) for m in ALL_M_VALUES}
    analysis_summary = _analysis_summary(started, per_m_rows)

    _write_json(out_dir / "corridor_phase_summary.json", analysis_summary)
    _write_json(out_dir / "corridor_phase_models.json", {str(m): per_m_rows[str(m)]["phase_model"] for m in ALL_M_VALUES})
    _write_json(
        out_dir / "delay_formula_verification.json",
        {
            str(m): {
                "delay_summary": per_m_rows[str(m)]["delay_summary"],
                "exit_summary": per_m_rows[str(m)]["exit_summary"],
                "residue_histogram": per_m_rows[str(m)]["residue_histogram"],
            }
            for m in ALL_M_VALUES
        },
    )
    _write_json(out_dir / "source_family_phase_rows.json", {str(m): per_m_rows[str(m)]["source_rows"] for m in ALL_M_VALUES})
    _write_json(args.summary_out, analysis_summary)


if __name__ == "__main__":
    main()
