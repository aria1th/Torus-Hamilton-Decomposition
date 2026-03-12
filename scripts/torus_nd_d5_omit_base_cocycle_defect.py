#!/usr/bin/env python3
"""Analyze small cocycle defects over the D5 omit-base reduced target."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

TASK_ID = "D5-OMIT-BASE-COCYCLE-DEFECT-025"
M_VALUES = (5, 7, 9, 11, 13, 15, 17, 19)
BASES = (
    {"name": "diag_omit", "slope": 1, "intercept": 0, "defect_row": 0},
    {"name": "antidiag_omit", "slope": -1, "intercept": 0, "defect_row": 0},
)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _graph_value(slope: int, intercept: int, s: int, m: int) -> int:
    return (slope * s + intercept) % m


def _base_next(s: int, u: int, *, m: int, slope: int, intercept: int, defect_row: int) -> Tuple[int, int]:
    if s == defect_row % m:
        return (s + 1) % m, u
    left = _graph_value(slope, intercept, s, m)
    right = (left + 1) % m
    if u == left:
        return (s + 1) % m, right
    if u == right:
        return (s + 1) % m, left
    return (s + 1) % m, u


def _phi0(s: int, m: int) -> int:
    return (2 + (1 if s == 1 else 0) - 2 * (1 if s == 2 % m else 0) - (1 if s == 3 % m else 0)) % m


def _defect_catalog() -> Dict[str, str]:
    return {
        "none": "No extra cocycle defect.",
        "point_left": "One-point defect at the omitted left endpoint (defect row, g(defect row)).",
        "point_right": "One-point defect at the omitted right endpoint (defect row, g(defect row)+1).",
        "edge_pair": "Two-point defect on both omitted edge endpoints.",
        "defect_row": "Whole omitted row.",
        "graph": "Whole diagonal / anti-diagonal graph matching the base.",
    }


def _in_defect(name: str, *, s: int, u: int, m: int, slope: int, intercept: int, defect_row: int) -> bool:
    left = _graph_value(slope, intercept, defect_row, m)
    right = (left + 1) % m
    if name == "none":
        return False
    if name == "point_left":
        return s == defect_row % m and u == left
    if name == "point_right":
        return s == defect_row % m and u == right
    if name == "edge_pair":
        return s == defect_row % m and u in {left, right}
    if name == "defect_row":
        return s == defect_row % m
    if name == "graph":
        return u == _graph_value(slope, intercept, s, m)
    raise ValueError(name)


def _full_grouped_orbits(
    *,
    m: int,
    slope: int,
    intercept: int,
    defect_row: int,
    defect_name: str,
) -> List[int]:
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
                    s1, u1 = _base_next(s, u, m=m, slope=slope, intercept=intercept, defect_row=defect_row)
                    twist = (_phi0(s, m) + (1 if _in_defect(
                        defect_name,
                        s=s,
                        u=u,
                        m=m,
                        slope=slope,
                        intercept=intercept,
                        defect_row=defect_row,
                    ) else 0)) % m
                    cur = (s1, u1, (v + twist) % m)
                    orbit_length += 1
                orbit_lengths.append(orbit_length)
    orbit_lengths.sort()
    return orbit_lengths


def _base_cycle_point_count(*, m: int, slope: int, intercept: int, defect_row: int, defect_name: str) -> int:
    count = 0
    for s in range(m):
        for u in range(m):
            if _in_defect(
                defect_name,
                s=s,
                u=u,
                m=m,
                slope=slope,
                intercept=intercept,
                defect_row=defect_row,
            ):
                count += 1
    return count


def _analyze_base(base: Mapping[str, int | str]) -> Mapping[str, object]:
    slope = int(base["slope"])
    intercept = int(base["intercept"])
    defect_row = int(base["defect_row"])
    rows = []
    for defect_name, description in _defect_catalog().items():
        by_m = {}
        for m in M_VALUES:
            point_count = _base_cycle_point_count(
                m=m,
                slope=slope,
                intercept=intercept,
                defect_row=defect_row,
                defect_name=defect_name,
            )
            orbit_lengths = _full_grouped_orbits(
                m=m,
                slope=slope,
                intercept=intercept,
                defect_row=defect_row,
                defect_name=defect_name,
            )
            by_m[str(m)] = {
                "defect_point_count": point_count,
                "predicted_total_cocycle_shift_mod_m": point_count % m,
                "full_grouped_orbit_lengths": orbit_lengths,
            }
        rows.append(
            {
                "defect_name": defect_name,
                "description": description,
                "by_m": by_m,
            }
        )
    return {
        "base": base,
        "rows": rows,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze cocycle defects over the D5 omit-base target.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    base_rows = [_analyze_base(base) for base in BASES]
    _write_json(out_dir / "cocycle_defect_catalog.json", {"rows": base_rows})

    summary_rows = []
    for row in base_rows:
        base = row["base"]
        defects = {}
        for defect in row["rows"]:
            defects[defect["defect_name"]] = {
                "m11_orbits": defect["by_m"]["11"]["full_grouped_orbit_lengths"],
                "all_single_orbit": all(
                    defect["by_m"][str(m)]["full_grouped_orbit_lengths"] == [m ** 3] for m in M_VALUES
                ),
            }
        summary_rows.append({"base": base, "defects": defects})

    summary = {
        "task_id": TASK_ID,
        "checked_m_values": list(M_VALUES),
        "strongest_supported_conclusion": (
            "On top of the 024 omit-base candidate, a single-point cocycle defect at either omitted edge endpoint is "
            "already enough to produce a single full grouped orbit of size m^3 across the checked odd moduli. The "
            "two-point omitted-edge defect also works. By contrast, row-sized and graph-sized defects still collapse "
            "because their total contribution over the unique base orbit is 0 mod m."
        ),
        "recommended_next_family": (
            "Target a local mechanism that simultaneously realizes the omit-base defect and a pointwise or two-point "
            "cocycle defect attached to the omitted edge endpoints."
        ),
        "rows": summary_rows,
    }
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    print("analyzed cocycle defects over omit-base targets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
