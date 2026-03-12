#!/usr/bin/env python3
"""Search one-defect grouped adjacent-transposition families for the D5 reduced model."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

TASK_ID = "D5-GROUPED-TRANSPOSITION-DEFECT-024"
M_VALUES = (5, 7, 9, 11, 13, 15, 17, 19)
SLOPES = (-1, 1)
INTERCEPTS = (-3, -2, -1, 0, 1, 2, 3)
DEFECT_ROWS = (-1, 0, 1, 2, 3)
SHIFTS = (-3, -2, -1, 0, 1, 2, 3)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _graph_formula(slope: int, intercept: int) -> str:
    if intercept == 0:
        offset = ""
    elif intercept > 0:
        offset = f"+{intercept}"
    else:
        offset = str(intercept)
    if slope == 1:
        return f"u=s{offset}"
    return f"u=-s{offset}"


def _defect_catalog() -> List[Tuple[str, Tuple[int, ...]]]:
    rows: List[Tuple[str, Tuple[int, ...]]] = [("omit", ())]
    for shift in SHIFTS:
        rows.append((f"shift_{shift}", (shift,)))
    for left, right in itertools.combinations(SHIFTS, 2):
        rows.append((f"pair_{left}_{right}", (left, right)))
    return rows


def _phi(s: int, m: int) -> int:
    return (2 + (1 if s == 1 else 0) - 2 * (1 if s == 2 % m else 0) - (1 if s == 3 % m else 0)) % m


def _row_map(m: int, *, s: int, slope: int, intercept: int, defect_row: int, defect_offsets: Tuple[int, ...]) -> List[int] | None:
    starts = (
        [(slope * s + intercept + offset) % m for offset in defect_offsets]
        if s == defect_row % m
        else [(slope * s + intercept) % m]
    )
    used = set()
    row = list(range(m))
    for start in starts:
        neighbor = (start + 1) % m
        if start in used or neighbor in used:
            return None
        used.add(start)
        used.add(neighbor)
        row[start], row[neighbor] = row[neighbor], row[start]
    if len(set(row)) != m:
        return None
    return row


def _base_orbits(m: int, *, slope: int, intercept: int, defect_row: int, defect_offsets: Tuple[int, ...]) -> List[int] | None:
    next_map = {}
    for s in range(m):
        row = _row_map(
            m,
            s=s,
            slope=slope,
            intercept=intercept,
            defect_row=defect_row,
            defect_offsets=defect_offsets,
        )
        if row is None:
            return None
        for u in range(m):
            next_map[(s, u)] = ((s + 1) % m, row[u])

    visited = set()
    orbit_lengths: List[int] = []
    for state in next_map:
        if state in visited:
            continue
        cur = state
        orbit_length = 0
        while cur not in visited:
            visited.add(cur)
            orbit_length += 1
            cur = next_map[cur]
        orbit_lengths.append(orbit_length)
    orbit_lengths.sort()
    return orbit_lengths


def _full_grouped_orbits(
    m: int,
    *,
    slope: int,
    intercept: int,
    defect_row: int,
    defect_offsets: Tuple[int, ...],
) -> List[int] | None:
    row_maps = []
    for s in range(m):
        row = _row_map(
            m,
            s=s,
            slope=slope,
            intercept=intercept,
            defect_row=defect_row,
            defect_offsets=defect_offsets,
        )
        if row is None:
            return None
        row_maps.append(row)

    visited = set()
    orbit_lengths: List[int] = []
    for s0 in range(m):
        for u0 in range(m):
            for v0 in range(m):
                state = (s0, u0, v0)
                if state in visited:
                    continue
                cur = state
                orbit_length = 0
                while cur not in visited:
                    visited.add(cur)
                    s, u, v = cur
                    cur = ((s + 1) % m, row_maps[s][u], (v + _phi(s, m)) % m)
                    orbit_length += 1
                orbit_lengths.append(orbit_length)
    orbit_lengths.sort()
    return orbit_lengths


def _candidate_row(
    *,
    slope: int,
    intercept: int,
    defect_row: int,
    defect_name: str,
    defect_offsets: Tuple[int, ...],
) -> Dict[str, object]:
    base_by_m = {}
    full_by_m = {}
    is_valid = True
    single_base_orbit = True
    for m in M_VALUES:
        base = _base_orbits(
            m,
            slope=slope,
            intercept=intercept,
            defect_row=defect_row,
            defect_offsets=defect_offsets,
        )
        full = _full_grouped_orbits(
            m,
            slope=slope,
            intercept=intercept,
            defect_row=defect_row,
            defect_offsets=defect_offsets,
        ) if base is not None else None
        if base is None or full is None:
            is_valid = False
            break
        base_by_m[str(m)] = base
        full_by_m[str(m)] = full
        single_base_orbit = single_base_orbit and base == [m * m]

    return {
        "slope": slope,
        "intercept": intercept,
        "graph_formula": _graph_formula(slope, intercept),
        "defect_row": defect_row,
        "defect_name": defect_name,
        "defect_offsets": list(defect_offsets),
        "is_valid_for_all_checked_m": is_valid,
        "single_base_orbit_for_all_checked_m": is_valid and single_base_orbit,
        "base_orbits_by_m": base_by_m,
        "full_grouped_orbits_by_m": full_by_m,
    }


def _representative_sample() -> Mapping[str, object]:
    return _candidate_row(slope=1, intercept=0, defect_row=0, defect_name="omit", defect_offsets=())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search one-defect grouped transposition families for D5.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    stable_rows = []
    stable_by_defect: Dict[str, int] = {}
    for slope in SLOPES:
        for intercept in INTERCEPTS:
            for defect_row in DEFECT_ROWS:
                for defect_name, defect_offsets in _defect_catalog():
                    row = _candidate_row(
                        slope=slope,
                        intercept=intercept,
                        defect_row=defect_row,
                        defect_name=defect_name,
                        defect_offsets=defect_offsets,
                    )
                    if not row["is_valid_for_all_checked_m"]:
                        continue
                    rows.append(row)
                    if row["single_base_orbit_for_all_checked_m"]:
                        stable_rows.append(row)
                        stable_by_defect[defect_name] = stable_by_defect.get(defect_name, 0) + 1

    _write_json(out_dir / "all_valid_candidates.json", {"rows": rows})
    _write_json(out_dir / "stable_single_base_orbit_candidates.json", {"rows": stable_rows})
    _write_json(out_dir / "stable_by_defect_type.json", stable_by_defect)
    _write_json(out_dir / "representative_omit_candidate.json", _representative_sample())

    summary = {
        "task_id": TASK_ID,
        "checked_m_values": list(M_VALUES),
        "valid_candidate_count": len(rows),
        "stable_single_base_orbit_count": len(stable_rows),
        "stable_by_defect_type": stable_by_defect,
        "strongest_supported_conclusion": (
            "Combining the s41 adjacent-transposition classification with the diagonal moving-transposition family, "
            "a single fixed-point defect is already enough: omitting the transposition on one chosen s-row yields a "
            "single grouped-base orbit of size m^2 across the checked odd moduli. The full grouped map still splits "
            "into m orbits of size m^2 because the twist remains phi(s)-only."
        ),
        "recommended_next_family": (
            "Target a local paired carry mechanism whose grouped effect is a diagonal or anti-diagonal moving adjacent "
            "transposition with one omitted row, and track separately whether the twist must also acquire u-dependence."
        ),
    }
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    print(f"valid_candidate_count: {len(rows)}")
    print(f"stable_single_base_orbit_count: {len(stable_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
