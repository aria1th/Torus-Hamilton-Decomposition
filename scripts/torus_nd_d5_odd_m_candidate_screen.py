#!/usr/bin/env python3
"""Theorem-guided odd-m screening for support-based D5 witness families.

This is an example of how to reuse the current D5 odd-m methodology as a
compressed screening harness rather than a broad brute-force search.

For each support-based witness JSON and each odd modulus m, the script:

1. builds the first-return map R_c on P0={S=0} for every color c;
2. computes exact cycle counts of R_c;
3. checks the clean-frame criterion
      R_c(x+k)=R_c(x)+k
   using a filtered translation search; and
4. records a compact theorem-style summary suitable for screening candidate
   families before any deeper symbolic work.

The key complexity reduction is conceptual:

- Naive vertexwise witness search lives in a space of size roughly
      (5!)^(m^5)
  for D5.
- This script does not search that space. It screens a fixed support family in
  polynomial time in m.
- Candidate clean-frame directions are filtered first using only x=0, reducing
  the symmetry check from a naive O(m^8) scan over (k,x) pairs to
  O(m^4 + r*m^4), where r is the number of surviving candidates.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

DIM = 5
DEFAULT_M_VALUES = (5, 7, 9, 11)
DEFAULT_COLORS = (0, 1, 2, 3, 4)

RelState = Tuple[int, int, int, int]
Coords = Tuple[int, int, int, int, int]


def _load_payload(path: Path) -> Mapping[str, object]:
    payload = json.loads(path.read_text())
    moves = payload.get("moves")
    if not isinstance(moves, list):
        raise ValueError(f"{path} does not contain a support-based 'moves' list")
    return payload


def _in_support(x: Coords, support: Sequence[object], m: int) -> bool:
    typ = str(support[0])
    layer = int(support[1]) % m
    if sum(x) % m != layer:
        return False
    if typ == "plane":
        return True
    if typ == "line1":
        axis = int(support[2])
        residue = int(support[3]) % m
        return x[axis] % m == residue
    if typ == "line2":
        axes = support[2]
        residues = support[3]
        return (
            x[int(axes[0])] % m == int(residues[0]) % m
            and x[int(axes[1])] % m == int(residues[1]) % m
        )
    raise ValueError(f"unknown support type: {support}")


def _rule(x: Coords, moves: Sequence[Mapping[str, object]], m: int) -> Tuple[int, ...]:
    dirs = list(range(DIM))
    for move in moves:
        if _in_support(x, move["support"], m):
            a, b = [int(v) for v in move["pair"]]
            dirs[a], dirs[b] = dirs[b], dirs[a]
    return tuple(dirs)


def _x_from_rel(color: int, rel: RelState, m: int) -> Coords:
    q, w, v, u = rel
    arr = [0] * DIM
    arr[(color + 1) % DIM] = q
    arr[(color + 2) % DIM] = w
    arr[(color + 3) % DIM] = v
    arr[(color + 4) % DIM] = u
    arr[color] = (-q - w - v - u) % m
    return tuple(arr)  # type: ignore[return-value]


def _rel_coords(x: Coords, color: int) -> RelState:
    return tuple(x[(color + k) % DIM] for k in range(1, DIM + 0))  # type: ignore[return-value]


def _increment(x: Coords, direction: int, m: int) -> Coords:
    nxt = list(x)
    nxt[direction] = (nxt[direction] + 1) % m
    return tuple(nxt)  # type: ignore[return-value]


def _cycle_stats_from_perm(perm: Sequence[int]) -> Dict[str, int]:
    seen = [False] * len(perm)
    cycle_count = 0
    max_cycle_length = 0
    min_cycle_length = 0 if not perm else len(perm)
    for start in range(len(perm)):
        if seen[start]:
            continue
        cycle_count += 1
        cur = start
        length = 0
        while not seen[cur]:
            seen[cur] = True
            cur = perm[cur]
            length += 1
        max_cycle_length = max(max_cycle_length, length)
        min_cycle_length = min(min_cycle_length, length)
    return {
        "cycle_count": cycle_count,
        "max_cycle_length": max_cycle_length,
        "min_cycle_length": min_cycle_length,
    }


def _sub_mod(a: RelState, b: RelState, m: int) -> RelState:
    return tuple((a[i] - b[i]) % m for i in range(4))  # type: ignore[return-value]


def _find_clean_frame_directions(
    states: Sequence[RelState],
    state_to_index: Mapping[RelState, int],
    perm: Sequence[int],
    m: int,
) -> Tuple[List[RelState], int]:
    zero_target = states[perm[0]]
    candidate_indices: List[int] = []
    for k_index in range(1, len(states)):
        k = states[k_index]
        if _sub_mod(states[perm[k_index]], zero_target, m) == k:
            candidate_indices.append(k_index)

    verified: List[RelState] = []
    for k_index in candidate_indices:
        k = states[k_index]
        ok = True
        for x_index, x in enumerate(states):
            y = tuple((x[i] + k[i]) % m for i in range(4))
            y_index = state_to_index[y]
            if _sub_mod(states[perm[y_index]], states[perm[x_index]], m) != k:
                ok = False
                break
        if ok:
            verified.append(k)

    return verified, len(candidate_indices)


def _screen_color(
    *,
    color: int,
    m: int,
    moves: Sequence[Mapping[str, object]],
    states: Sequence[RelState],
    state_to_index: Mapping[RelState, int],
) -> Dict[str, object]:
    perm: List[int] = []
    rule_calls = 0
    for rel in states:
        cur = _x_from_rel(color, rel, m)
        for _ in range(m):
            direction = _rule(cur, moves, m)[color]
            rule_calls += 1
            cur = _increment(cur, direction, m)
        perm.append(state_to_index[_rel_coords(cur, color)])

    cycle_stats = _cycle_stats_from_perm(perm)
    clean_dirs, filtered_candidates = _find_clean_frame_directions(states, state_to_index, perm, m)
    return {
        "hamilton_on_P0": bool(cycle_stats["cycle_count"] == 1),
        "cycle_count": int(cycle_stats["cycle_count"]),
        "max_cycle_length": int(cycle_stats["max_cycle_length"]),
        "min_cycle_length": int(cycle_stats["min_cycle_length"]),
        "clean_frame_exists": bool(clean_dirs),
        "clean_frame_direction_count": int(len(clean_dirs)),
        "filtered_clean_frame_candidate_count": int(filtered_candidates),
        "sample_clean_frame_directions": [list(k) for k in clean_dirs[:8]],
        "first_return_rule_calls": int(rule_calls),
    }


def _screen_witness_for_m(
    *,
    witness_path: Path,
    payload: Mapping[str, object],
    m: int,
    colors: Sequence[int],
) -> Dict[str, object]:
    states = list(itertools.product(range(m), repeat=4))
    state_to_index = {state: idx for idx, state in enumerate(states)}
    moves = payload["moves"]

    per_color = {
        str(color): _screen_color(
            color=color,
            m=m,
            moves=moves,
            states=states,
            state_to_index=state_to_index,
        )
        for color in colors
    }

    hamilton_colors = [int(c) for c, data in per_color.items() if data["hamilton_on_P0"]]
    clean_frame_colors = [int(c) for c, data in per_color.items() if data["clean_frame_exists"]]
    rule_calls = sum(int(data["first_return_rule_calls"]) for data in per_color.values())
    support_checks = rule_calls * len(moves)

    return {
        "witness": str(witness_path),
        "m": int(m),
        "p0_state_count": int(m**4),
        "per_color": per_color,
        "hamilton_colors": hamilton_colors,
        "clean_frame_colors": clean_frame_colors,
        "all_colors_hamilton": bool(len(hamilton_colors) == len(colors)),
        "all_colors_have_clean_frame": bool(len(clean_frame_colors) == len(colors)),
        "operation_estimates": {
            "first_return_rule_calls_total": int(rule_calls),
            "support_membership_checks_total": int(support_checks),
            "naive_clean_frame_pair_checks_per_color": int((m**4 - 1) * (m**4)),
            "actual_filtered_candidates_total": int(
                sum(int(data["filtered_clean_frame_candidate_count"]) for data in per_color.values())
            ),
        },
    }


def _complexity_note() -> Mapping[str, object]:
    return {
        "what_is_compressed": [
            "candidate search is lifted from arbitrary vertexwise direction tuples to a support-based family description",
            "Hamiltonicity is checked on the first-return map on P0, not by ad hoc full-orbit reasoning",
            "clean-frame detection uses an x=0 prefilter before full translation verification",
        ],
        "naive_candidate_space": "(5!)^(m^5) for arbitrary D5 vertexwise rules",
        "per_candidate_screen_cost": "O(L * |colors| * m^5) rule applications for a support family of length L",
        "clean_frame_cost_reduction": "from naive O(m^8) pair checks over (k,x) to O(m^4 + r*m^4), where r is the filtered surviving translation count",
        "how_to_use": "screen many candidate support families cheaply, then reserve deeper symbolic work only for candidates that keep clean frames and Hamilton colors across several odd moduli",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Theorem-guided odd-m screening for D5 support-based witnesses.")
    parser.add_argument(
        "--witness-json",
        type=Path,
        nargs="+",
        required=True,
        help="One or more support-based witness JSON files (for example RoundY/d5_m5_kempe_witness_26.json).",
    )
    parser.add_argument(
        "--m-values",
        type=int,
        nargs="+",
        default=list(DEFAULT_M_VALUES),
        help="Odd moduli to screen.",
    )
    parser.add_argument(
        "--colors",
        type=int,
        nargs="+",
        default=list(DEFAULT_COLORS),
        help="Colors to screen (default: all 0..4).",
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        required=True,
        help="Where to write the JSON summary.",
    )
    args = parser.parse_args()

    started = time.perf_counter()
    witness_payloads = {path: _load_payload(path) for path in args.witness_json}

    results: Dict[str, object] = {}
    for witness_path, payload in witness_payloads.items():
        witness_results = {}
        for m in args.m_values:
            if m % 2 == 0:
                raise ValueError(f"expected odd modulus, got m={m}")
            witness_results[str(m)] = _screen_witness_for_m(
                witness_path=witness_path,
                payload=payload,
                m=int(m),
                colors=tuple(args.colors),
            )
        results[str(witness_path)] = witness_results

    summary = {
        "title": "D5 odd-m theorem-guided candidate screen",
        "methodology": "first-return + Hamilton cycle count + clean-frame filtered symmetry detection",
        "complexity": _complexity_note(),
        "screened_witnesses": [str(path) for path in args.witness_json],
        "m_values": [int(m) for m in args.m_values],
        "colors": [int(c) for c in args.colors],
        "results": results,
        "runtime_seconds": time.perf_counter() - started,
    }
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
