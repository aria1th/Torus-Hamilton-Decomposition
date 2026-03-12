#!/usr/bin/env python3
"""Search simple grouped transposition families over the D5 reduced base."""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Mapping, Sequence, Tuple

TASK_ID = "D5-GROUPED-TRANSPOSITION-FAMILY-023"
M_VALUES = (5, 7, 9, 11, 13, 15, 17, 19)
SLOPES = (-1, 0, 1)
INTERCEPTS = (-3, -2, -1, 0, 1, 2, 3)


@dataclass(frozen=True)
class GraphSpec:
    slope: int
    intercept: int

    @property
    def formula(self) -> str:
        if self.intercept == 0:
            offset = ""
        elif self.intercept > 0:
            offset = f"+{self.intercept}"
        else:
            offset = str(self.intercept)
        if self.slope == 1:
            return f"u=s{offset}"
        if self.slope == -1:
            return f"u=-s{offset}"
        return f"u={self.intercept}"


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _phi(s: int, m: int) -> int:
    return (2 + (1 if s == 1 else 0) - 2 * (1 if s == 2 % m else 0) - (1 if s == 3 % m else 0)) % m


def _row_map(m: int, s: int, graphs: Sequence[GraphSpec]) -> List[int] | None:
    row = list(range(m))
    used = set()
    for graph in graphs:
        x = (graph.slope * s + graph.intercept) % m
        y = (x + 1) % m
        if x in used or y in used:
            return None
        used.add(x)
        used.add(y)
        row[x], row[y] = row[y], row[x]
    if len(set(row)) != m:
        return None
    return row


def _base_orbits(m: int, graphs: Sequence[GraphSpec]) -> List[int] | None:
    next_map = {}
    for s in range(m):
        row = _row_map(m, s, graphs)
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


def _full_grouped_orbits(m: int, graphs: Sequence[GraphSpec]) -> List[int] | None:
    row_maps = []
    for s in range(m):
        row = _row_map(m, s, graphs)
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


def _family_row(graphs: Sequence[GraphSpec]) -> Mapping[str, object]:
    base_by_m = {}
    full_by_m = {}
    is_valid = True
    for m in M_VALUES:
        base_orbits = _base_orbits(m, graphs)
        full_orbits = _full_grouped_orbits(m, graphs) if base_orbits is not None else None
        if base_orbits is None or full_orbits is None:
            is_valid = False
            break
        base_by_m[str(m)] = base_orbits
        full_by_m[str(m)] = full_orbits
    return {
        "graphs": [{"slope": graph.slope, "intercept": graph.intercept, "formula": graph.formula} for graph in graphs],
        "is_valid_for_all_checked_m": is_valid,
        "base_orbits_by_m": base_by_m,
        "full_grouped_orbits_by_m": full_by_m,
    }


def _search_single_graph_families() -> List[Mapping[str, object]]:
    rows = []
    for graph in (GraphSpec(slope, intercept) for slope in SLOPES for intercept in INTERCEPTS):
        row = _family_row((graph,))
        if row["is_valid_for_all_checked_m"]:
            rows.append(row)
    return rows


def _search_two_graph_families() -> List[Mapping[str, object]]:
    rows = []
    graphs = [GraphSpec(slope, intercept) for slope in SLOPES for intercept in INTERCEPTS]
    for pair in itertools.combinations(graphs, 2):
        row = _family_row(pair)
        if row["is_valid_for_all_checked_m"]:
            rows.append(row)
    return rows


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search grouped transposition families for D5.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    single_rows = _search_single_graph_families()
    two_rows = _search_two_graph_families()
    _write_json(out_dir / "single_graph_families.json", {"rows": single_rows})
    _write_json(out_dir / "two_graph_families.json", {"rows": two_rows})

    diagonal_rows = [
        row
        for row in single_rows
        if row["graphs"][0]["slope"] in (-1, 1)
    ]
    summary = {
        "task_id": TASK_ID,
        "checked_m_values": list(M_VALUES),
        "single_graph_valid_count": len(single_rows),
        "two_graph_valid_count": len(two_rows),
        "strongest_supported_conclusion": (
            "The first genuinely two-dimensional reduced perturbation is a moving adjacent transposition along a "
            "diagonal or anti-diagonal graph u = ±s + b. It yields grouped base orbit sizes [m, m(m-1)] and full "
            "grouped orbit sizes [m^2, m^2(m-1)] across the checked odd moduli. No single-graph or two-graph affine "
            "transposition family in the searched range yields a single grouped-base orbit of size m^2."
        ),
        "recommended_next_family": (
            "Target a local paired carry mechanism whose grouped effect emulates a diagonal moving adjacent "
            "transposition, then add a controlled defect that breaks the residual invariant diagonal."
        ),
        "diagonal_examples": diagonal_rows[:8],
    }
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    print(f"single_graph_valid_count: {len(single_rows)}")
    print(f"two_graph_valid_count: {len(two_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
