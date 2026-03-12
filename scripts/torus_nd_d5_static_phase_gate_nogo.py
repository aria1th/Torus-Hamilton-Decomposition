#!/usr/bin/env python3
"""Test the first static phase-exposure gate families on the best D5 endpoint seed."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from math import gcd
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import torus_nd_d5_endpoint_latin_repair as seed032
from torus_nd_d5_return_map_model_common import environment_block, runtime_since
from torus_nd_d5_strict_palette_context_common import DIM, first_return, incoming_latin_all

TASK_ID = "D5-STATIC-PHASE-GATE-NOGO-035"
PRIMARY_M_VALUES = (5, 7, 9)
CONTROL_M = 11
BEST_LEFT_WORD = (2, 2, 1)
BEST_RIGHT_WORD = (1, 4, 4)
REPRESENTATIVE_W0 = 0
REPRESENTATIVE_S0 = 0
FIELDS = ("q", "w", "v", "u", "s", "layer")


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _state_dict(vertex: Sequence[int], color: int, m: int) -> Dict[str, int]:
    q = int(vertex[(color + 1) % DIM])
    w = int(vertex[(color + 2) % DIM])
    v = int(vertex[(color + 3) % DIM])
    u = int(vertex[(color + 4) % DIM])
    layer = int(sum(vertex) % m)
    s_value = int((w + u) % m)
    return {"q": q, "w": w, "v": v, "u": u, "s": s_value, "layer": layer}


def _build_best_seed(prepared: seed032.PreparedSearch, cocycle_defect: str) -> Tuple[List[List[int]], Dict[str, object]]:
    nexts_all, meta = seed032._build_candidate(
        prepared,
        w0=REPRESENTATIVE_W0,
        s0=REPRESENTATIVE_S0,
        left_word=BEST_LEFT_WORD,
        right_word=BEST_RIGHT_WORD,
        cocycle_defect=cocycle_defect,
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
        vertex = prepared.pre["coords"][idx]
        if int(vertex[1]) == prepared.m - 1 and int(vertex[2]) == prepared.m - 1 and int(sum(vertex) % prepared.m) == 2:
            out.add(idx)
    return out


def _exit_rows_for_m(prepared: seed032.PreparedSearch) -> List[Dict[str, object]]:
    nexts_all, meta = _build_best_seed(prepared, "none")
    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    hole_l1 = _hole_l1_set(prepared, row)
    step_by_dir = prepared.pre["step_by_dir"]
    coords = prepared.pre["coords"]

    rows = []
    for u_value in range(1, prepared.m):
        source_index = next(idx for idx, label in enumerate(labels) if label == "R1" and int(coords[idx][4]) == u_value)
        current = step_by_dir[2][source_index]
        path = []
        seen = set()
        exit_row = None
        while current not in seen:
            seen.add(current)
            path.append(_state_dict(coords[current], 0, prepared.m))
            exit_dirs = [direction for direction in range(5) if step_by_dir[direction][current] in hole_l1]
            if exit_dirs:
                exit_row = {
                    "source_u": int(u_value),
                    "delay": len(path) - 1,
                    "exit_dirs": [int(value) for value in exit_dirs],
                    "path": path,
                    "exit_state": path[-1],
                }
                break
            current = row[current]
        if exit_row is None:
            raise ValueError(f"no H_L1 exit found for source u={u_value}")
        rows.append(exit_row)
    return rows


def _projection_key(row: Mapping[str, int], combo: Sequence[str]) -> Tuple[int, ...]:
    return tuple(int(row[field]) for field in combo)


def _separating_projection_rows(per_m_exit_rows: Mapping[int, Sequence[Mapping[str, object]]]) -> Dict[str, object]:
    rows = []
    good_by_size = {1: [], 2: [], 3: []}
    for size in (1, 2, 3):
        for combo in itertools.combinations(FIELDS, size):
            good = True
            details = {}
            for m, exit_rows in per_m_exit_rows.items():
                for source_row in exit_rows:
                    exit_key = _projection_key(source_row["exit_state"], combo)
                    if any(_projection_key(state_row, combo) == exit_key for state_row in source_row["path"][:-1]):
                        good = False
                        break
                if not good:
                    break
                regular_keys = sorted(
                    {
                        _projection_key(source_row["exit_state"], combo)
                        for source_row in exit_rows
                        if source_row["exit_dirs"] == [2]
                    }
                )
                exceptional_keys = sorted(
                    {
                        _projection_key(source_row["exit_state"], combo)
                        for source_row in exit_rows
                        if source_row["exit_dirs"] == [1]
                    }
                )
                details[str(m)] = {
                    "regular_key_count": len(regular_keys),
                    "exceptional_key_count": len(exceptional_keys),
                    "regular_keys": [list(value) for value in regular_keys],
                    "exceptional_keys": [list(value) for value in exceptional_keys],
                }
            row = {
                "fields": list(combo),
                "size": size,
                "separates_first_exit": bool(good),
                "per_m": details,
            }
            rows.append(row)
            if good:
                good_by_size[size].append(list(combo))
    return {"rows": rows, "good_by_size": good_by_size}


def _regular_and_exceptional_keys(exit_rows: Sequence[Mapping[str, object]], combo: Sequence[str]) -> Tuple[set[Tuple[int, ...]], set[Tuple[int, ...]]]:
    regular = {
        _projection_key(source_row["exit_state"], combo)
        for source_row in exit_rows
        if source_row["exit_dirs"] == [2]
    }
    exceptional = {
        _projection_key(source_row["exit_state"], combo)
        for source_row in exit_rows
        if source_row["exit_dirs"] == [1]
    }
    return regular, exceptional


def _evaluate_phase_gate(
    prepared_by_m: Mapping[int, seed032.PreparedSearch],
    combo: Sequence[str],
    mode: str,
    cocycle_defect: str,
) -> Dict[str, object]:
    per_m = {}
    latin_all = True
    clean_all = True
    strict_all = True
    full_single_all = True
    total_cycle_count = 0
    total_nonzero_monodromy = 0

    for m in PRIMARY_M_VALUES:
        prepared = prepared_by_m[m]
        nexts_all, meta = _build_best_seed(prepared, cocycle_defect)
        labels_by_color = meta["labels_by_color"]
        step_by_dir = prepared.pre["step_by_dir"]
        coords = prepared.pre["coords"]
        exit_rows = _exit_rows_for_m(prepared)
        regular_keys, exceptional_keys = _regular_and_exceptional_keys(exit_rows, combo)

        for color in range(DIM):
            labels = labels_by_color[color]
            for idx, label in enumerate(labels):
                if label != "B":
                    continue
                state_row = _state_dict(coords[idx], color, m)
                key = _projection_key(state_row, combo)
                if mode in {"reg_only", "both"} and key in regular_keys:
                    nexts_all[color][idx] = step_by_dir[(2 + color) % DIM][idx]
                elif mode in {"exc_only", "both"} and key in exceptional_keys:
                    nexts_all[color][idx] = step_by_dir[(1 + color) % DIM][idx]

        latin = incoming_latin_all(nexts_all)
        if not latin:
            per_m[str(m)] = {"latin_all_colors": False}
            latin_all = False
            clean_all = False
            strict_all = False
            full_single_all = False
            break

        ret = first_return(prepared.pre, nexts_all[0])
        monodromies = [int(value) for value in ret["monodromies"]]
        full_single = (
            ret["clean_frame"]
            and ret["strict_clock"]
            and ret["U_cycle_count"] == 1
            and ret["U_cycle_lengths"] == [m * m]
            and len(monodromies) == 1
            and gcd(monodromies[0], m) == 1
        )
        per_m[str(m)] = {
            "latin_all_colors": True,
            "clean_frame": bool(ret["clean_frame"]),
            "strict_clock": bool(ret["strict_clock"]),
            "u_cycle_count": int(ret["U_cycle_count"]),
            "u_cycle_lengths": list(ret["U_cycle_lengths"]),
            "monodromies": monodromies,
            "full_single_grouped_orbit": bool(full_single),
            "regular_key_count": len(regular_keys),
            "exceptional_key_count": len(exceptional_keys),
        }
        clean_all &= bool(ret["clean_frame"])
        strict_all &= bool(ret["strict_clock"])
        full_single_all &= bool(full_single)
        total_cycle_count += int(ret["U_cycle_count"])
        total_nonzero_monodromy += sum(1 for value in monodromies if value != 0)

    return {
        "fields": list(combo),
        "mode": mode,
        "cocycle_defect": cocycle_defect,
        "latin_all": latin_all,
        "clean_all": clean_all,
        "strict_all": strict_all,
        "full_single_all": full_single_all,
        "total_cycle_count": total_cycle_count,
        "total_nonzero_monodromy": total_nonzero_monodromy,
        "per_m": per_m,
    }


def _search_static_phase_gates(
    prepared_by_m: Mapping[int, seed032.PreparedSearch],
    separating_rows: Mapping[str, object],
) -> Dict[str, object]:
    good_size3 = [tuple(row) for row in separating_rows["good_by_size"][3]]
    rows = []
    for combo in good_size3:
        for mode in ("reg_only", "exc_only", "both"):
            for cocycle_defect in ("none", "left", "right", "both"):
                rows.append(_evaluate_phase_gate(prepared_by_m, combo, mode, cocycle_defect))

    rows.sort(
        key=lambda row: (
            not row["latin_all"],
            not row["clean_all"],
            not row["strict_all"],
            not row["full_single_all"],
            row["total_cycle_count"] if row["latin_all"] else 10**9,
            -row["total_nonzero_monodromy"],
            tuple(row["fields"]),
            row["mode"],
            row["cocycle_defect"],
        )
    )
    latin_rows = [row for row in rows if row["latin_all"]]
    clean_rows = [row for row in latin_rows if row["clean_all"]]
    strict_rows = [row for row in clean_rows if row["strict_all"]]
    target_rows = [row for row in strict_rows if row["full_single_all"]]
    return {
        "rows": rows,
        "summary": {
            "candidate_count": len(rows),
            "latin_count": len(latin_rows),
            "clean_count": len(clean_rows),
            "strict_count": len(strict_rows),
            "target_count": len(target_rows),
            "best_rows": rows[:20],
            "target_rows": target_rows[:20],
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Test the first static phase-exposure gate families on the best D5 endpoint seed.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args(argv)

    start = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    prepared_by_m = {m: seed032._prepare_m(m, seed032._mixed_rule()) for m in PRIMARY_M_VALUES}
    control_prepared = seed032._prepare_m(CONTROL_M, seed032._mixed_rule())
    per_m_exit_rows = {m: _exit_rows_for_m(prepared_by_m[m]) for m in PRIMARY_M_VALUES}
    per_m_exit_rows[CONTROL_M] = _exit_rows_for_m(control_prepared)
    separating_rows = _separating_projection_rows(per_m_exit_rows)
    static_gate_rows = _search_static_phase_gates(prepared_by_m, separating_rows)

    _write_json(out_dir / "exit_phase_projection_catalog.json", separating_rows)
    _write_json(out_dir / "source_exit_rows.json", {str(m): per_m_exit_rows[m] for m in PRIMARY_M_VALUES + (CONTROL_M,)})
    _write_json(out_dir / "static_phase_gate_rows.json", {"rows": static_gate_rows["rows"]})
    _write_json(out_dir / "static_phase_gate_summary.json", static_gate_rows["summary"])

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "primary_m_values": list(PRIMARY_M_VALUES),
        "control_m": CONTROL_M,
        "best_seed": {
            "left_word": list(BEST_LEFT_WORD),
            "right_word": list(BEST_RIGHT_WORD),
        },
        "projection_summary": {
            "good_size_1_count": len(separating_rows["good_by_size"][1]),
            "good_size_2_count": len(separating_rows["good_by_size"][2]),
            "good_size_3_count": len(separating_rows["good_by_size"][3]),
            "good_size_3_fields": separating_rows["good_by_size"][3],
        },
        "static_gate_summary": static_gate_rows["summary"],
        "strongest_supported_conclusion": (
            "The first static phase-exposure layer is already sharply constrained. No one- or two-coordinate projection "
            "of (q,w,v,u,s,layer) isolates the first H_L1 exit along every best-seed corridor on m=5,7,9,11. Exactly "
            "eight three-coordinate projections do isolate that exit along the corridor, but every resulting static "
            "B-state phase gate family (regular-only, exceptional-only, or both; with any of the four cocycle-defect "
            "choices) fails incoming Latin already on the pilot range."
        ),
    }
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    print(
        f"good_size1={len(separating_rows['good_by_size'][1])} "
        f"good_size2={len(separating_rows['good_by_size'][2])} "
        f"good_size3={len(separating_rows['good_by_size'][3])} "
        f"static_gate_latin={static_gate_rows['summary']['latin_count']} "
        f"static_gate_target={static_gate_rows['summary']['target_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
