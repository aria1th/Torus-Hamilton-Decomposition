#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

State2 = Tuple[int, int]
State3 = Tuple[int, int, int]


@dataclass(frozen=True)
class ReducedFamilySpec:
    m: int
    a: int          # slope: +1 or -1
    b: int          # intercept
    defect_row: int
    defect_h: Optional[int]  # None = omission; otherwise swap defect_h <-> defect_h+1 on defect row


def reduced_base_map(spec: ReducedFamilySpec) -> Callable[[State2], State2]:
    m = spec.m
    a = spec.a
    b = spec.b
    d = spec.defect_row
    h = spec.defect_h

    def step(state: State2) -> State2:
        s, u = state
        g = (a * s + b) % m
        if s == d:
            if h is None:
                u2 = u
            else:
                h0 = h % m
                h1 = (h0 + 1) % m
                if u == h0:
                    u2 = h1
                elif u == h1:
                    u2 = h0
                else:
                    u2 = u
        else:
            g1 = (g + 1) % m
            if u == g:
                u2 = g1
            elif u == g1:
                u2 = g
            else:
                u2 = u
        return ((s + 1) % m, u2)

    return step


def orbit_sizes(states: Sequence, step: Callable) -> List[int]:
    seen = set()
    sizes: List[int] = []
    for x in states:
        if x in seen:
            continue
        cur = x
        orbit = []
        while cur not in seen:
            seen.add(cur)
            orbit.append(cur)
            cur = step(cur)
        sizes.append(len(orbit))
    sizes.sort()
    return sizes


def first_return_on_row_zero(m: int, defect_h: Optional[int]) -> Dict[int, int]:
    spec = ReducedFamilySpec(m=m, a=1, b=0, defect_row=0, defect_h=defect_h)
    step = reduced_base_map(spec)
    out: Dict[int, int] = {}
    for u0 in range(m):
        state = (0, u0)
        for _ in range(m):
            state = step(state)
        out[u0] = state[1]
    return out


def canonical_skew_orbit_sizes(m: int, defect_support: Sequence[State2]) -> List[int]:
    spec = ReducedFamilySpec(m=m, a=1, b=0, defect_row=0, defect_h=None)
    base_step = reduced_base_map(spec)
    support = set(defect_support)

    def skew_step(state: State3) -> State3:
        s, u, v = state
        s2, u2 = base_step((s, u))
        inc = 1 if (s, u) in support else 0
        return (s2, u2, (v + inc) % m)

    states = [(s, u, v) for s in range(m) for u in range(m) for v in range(m)]
    return orbit_sizes(states, skew_step)


def main() -> None:
    moduli = [3, 5, 7, 9, 11, 13, 15, 17, 19]
    out_root = Path('/mnt/data')
    summary_path = out_root / 'd5_239_G1_reduced_omit_target_summary.json'
    table_path = out_root / 'd5_239_G1_reduced_omit_target_table.csv'

    summary = {
        'task': 'd5_239_G1_reduced_omit_target_search',
        'family': 'rowwise moving adjacent transposition on Z_m^2 with one defect row',
        'moduli': moduli,
        'per_modulus': {},
    }

    csv_rows: List[Dict[str, object]] = []

    for m in moduli:
        all_states_2 = [(s, u) for s in range(m) for u in range(m)]
        omit_count = 0
        shifted_count = 0
        omit_examples = []
        shifted_examples = []
        # exact search over slope/intercept/defect-row and defect-row replacement
        for a in (1, -1):
            for b in range(m):
                for defect_row in range(m):
                    omit_spec = ReducedFamilySpec(m, a, b, defect_row, None)
                    omit_sizes = orbit_sizes(all_states_2, reduced_base_map(omit_spec))
                    if omit_sizes == [m * m]:
                        omit_count += 1
                        if len(omit_examples) < 3:
                            omit_examples.append({'a': a, 'b': b, 'defect_row': defect_row})
                    for defect_h in range(m):
                        shift_spec = ReducedFamilySpec(m, a, b, defect_row, defect_h)
                        shift_sizes = orbit_sizes(all_states_2, reduced_base_map(shift_spec))
                        if shift_sizes == [m * m]:
                            shifted_count += 1
                            if len(shifted_examples) < 3:
                                shifted_examples.append({'a': a, 'b': b, 'defect_row': defect_row, 'defect_h': defect_h})

        omit_first_return = first_return_on_row_zero(m, None)
        shift0_first_return = first_return_on_row_zero(m, 0)
        omit_first_return_cycle_sizes = orbit_sizes(list(range(m)), lambda u, p=omit_first_return: p[u])
        shift0_first_return_cycle_sizes = orbit_sizes(list(range(m)), lambda u, p=shift0_first_return: p[u])

        # Canonical omission family + smallest cocycle defects on omitted edge endpoints.
        point0_sizes = canonical_skew_orbit_sizes(m, defect_support=[(0, 0)])
        point1_sizes = canonical_skew_orbit_sizes(m, defect_support=[(0, 1 % m)])
        two_point_sizes = canonical_skew_orbit_sizes(m, defect_support=[(0, 0), (0, 1 % m)])

        rec = {
            'm': m,
            'omit_single_base_orbit_count': omit_count,
            'shifted_single_base_orbit_count': shifted_count,
            'omit_example': omit_examples[0] if omit_examples else None,
            'shifted_example': shifted_examples[0] if shifted_examples else None,
            'canonical_omit_first_return': omit_first_return,
            'canonical_shift0_first_return': shift0_first_return,
            'canonical_omit_first_return_cycle_sizes': omit_first_return_cycle_sizes,
            'canonical_shift0_first_return_cycle_sizes': shift0_first_return_cycle_sizes,
            'canonical_point0_full_orbit_sizes': point0_sizes,
            'canonical_point1_full_orbit_sizes': point1_sizes,
            'canonical_two_point_full_orbit_sizes': two_point_sizes,
        }
        summary['per_modulus'][str(m)] = rec
        csv_rows.append({
            'm': m,
            'omit_single_base_orbit_count': omit_count,
            'shifted_single_base_orbit_count': shifted_count,
            'canonical_omit_first_return_cycle_sizes': str(omit_first_return_cycle_sizes),
            'canonical_shift0_first_return_cycle_sizes': str(shift0_first_return_cycle_sizes),
            'canonical_point0_full_orbit_sizes': str(point0_sizes),
            'canonical_point1_full_orbit_sizes': str(point1_sizes),
            'canonical_two_point_full_orbit_sizes': str(two_point_sizes),
        })

    with summary_path.open('w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)

    with table_path.open('w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)

    print(summary_path)
    print(table_path)


if __name__ == '__main__':
    main()
