#!/usr/bin/env python3
"""Search and certify small periodic phase-carrier candidates for the remaining G1 route.

Family searched:
  T_{m,r,a,patt}(s,u) = (s+1, tau_s(u))
where patt is a length-r pattern with entries either None (identity row) or beta in Z_m,
row s uses residue t=s mod r, and tau_s swaps g=a*s+beta with g+1.

This is the natural periodic-carrier extension of the reduced omitted-row family from d5_240.

Outputs:
- /mnt/data/d5_242_G1_periodic_phase_carrier_summary.json
- /mnt/data/d5_242_G1_periodic_phase_carrier_table.csv
"""
from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

State2 = Tuple[int, int]
Pattern = Tuple[Optional[int], ...]


def cycle_sizes_from_perm(perm: Sequence[int]) -> List[int]:
    n = len(perm)
    seen = [False] * n
    sizes: List[int] = []
    for i in range(n):
        if seen[i]:
            continue
        cur = i
        size = 0
        while not seen[cur]:
            seen[cur] = True
            cur = int(perm[cur])
            size += 1
        sizes.append(size)
    sizes.sort()
    return sizes


class FirstReturnBuilder:
    def __init__(self, m: int) -> None:
        self.m = m
        self.transpositions: List[Tuple[int, int]] = [(i, (i + 1) % m) for i in range(m)]

    def first_return_perm(self, *, r: int, a: int, pattern: Pattern) -> List[int]:
        """Return the first-return permutation on the row-zero coordinate u after m steps."""
        perm = list(range(self.m))
        for s in range(self.m):
            beta = pattern[s % r]
            if beta is None:
                continue
            i, j = self.transpositions[(a * s + beta) % self.m]
            # left-compose the current permutation by the transposition (i j)
            for idx, value in enumerate(perm):
                if value == i:
                    perm[idx] = j
                elif value == j:
                    perm[idx] = i
        return perm


def base_step_factory(*, m: int, r: int, a: int, pattern: Pattern):
    def step(state: State2) -> State2:
        s, u = state
        beta = pattern[s % r]
        if beta is None:
            u2 = u
        else:
            g = (a * s + beta) % m
            g1 = (g + 1) % m
            if u == g:
                u2 = g1
            elif u == g1:
                u2 = g
            else:
                u2 = u
        return ((s + 1) % m, u2)

    return step


def orbit_sizes(states: Sequence, step) -> List[int]:
    seen = set()
    sizes: List[int] = []
    for x in states:
        if x in seen:
            continue
        cur = x
        size = 0
        while cur not in seen:
            seen.add(cur)
            cur = step(cur)
            size += 1
        sizes.append(size)
    sizes.sort()
    return sizes


def grouped_orbit_sizes_for_point_defect(*, m: int, r: int, a: int, pattern: Pattern, defect: State2) -> List[int]:
    base_step = base_step_factory(m=m, r=r, a=a, pattern=pattern)

    def step(state: Tuple[int, int, int]) -> Tuple[int, int, int]:
        s, u, v = state
        s2, u2 = base_step((s, u))
        inc = 1 if (s, u) == defect else 0
        return (s2, u2, (v + inc) % m)

    states = [(s, u, v) for s in range(m) for u in range(m) for v in range(m)]
    return orbit_sizes(states, step)


def canonical_candidate_pattern(m: int) -> Tuple[int, Pattern]:
    """For m=2k+1, return r=k+1 and pattern (0,...,0,None)."""
    k = (m - 1) // 2
    r = k + 1
    pattern: Pattern = tuple([0] * k + [None])
    return r, pattern


def main() -> None:
    exact_moduli = [3, 5, 7, 9, 11]
    candidate_moduli = [3, 5, 7, 9, 11, 13, 15, 17, 19]

    out_root = Path('/mnt/data')
    summary_path = out_root / 'd5_242_G1_periodic_phase_carrier_summary.json'
    table_path = out_root / 'd5_242_G1_periodic_phase_carrier_table.csv'

    summary: Dict[str, object] = {
        'task': 'd5_242_G1_periodic_phase_carrier_search',
        'family': (
            'period-r phase-carrier extension of the reduced adjacent-transposition family: '
            'row s uses pattern entry t=s mod r, with either identity or swap of (a*s+beta, a*s+beta+1)'
        ),
        'exact_small_period_search': {},
        'minimal_phase_catalog_small': {},
        'explicit_candidate_check': {},
    }
    csv_rows: List[Dict[str, object]] = []

    # Exact search for all patterns on checked small periods.
    for m in exact_moduli:
        builder = FirstReturnBuilder(m)
        per_m: Dict[str, object] = {
            'checked_periods': {},
            'minimal_surviving_period_found': None,
        }
        found_r: Optional[int] = None
        for r in range(1, (m - 1) // 2 + 1):
            choices: List[Optional[int]] = [None] + list(range(m))
            survivor_count = 0
            examples: List[Dict[str, object]] = []
            for a in (1, -1):
                for pattern in itertools.product(choices, repeat=r):
                    perm = builder.first_return_perm(r=r, a=a, pattern=pattern)
                    if cycle_sizes_from_perm(perm) == [m]:
                        survivor_count += 1
                        if len(examples) < 3:
                            examples.append({'a': a, 'pattern': [None if x is None else int(x) for x in pattern]})
                        if found_r is None:
                            found_r = r
            rec = {
                'survivor_count': survivor_count,
                'example_patterns': examples,
            }
            per_m['checked_periods'][str(r)] = rec
            csv_rows.append({
                'kind': 'exact_small_period_search',
                'm': m,
                'r': r,
                'survivor_count': survivor_count,
                'example_pattern': '' if not examples else json.dumps(examples[0], sort_keys=True),
            })
        per_m['minimal_surviving_period_found'] = found_r
        summary['exact_small_period_search'][str(m)] = per_m


    # Exact catalog on the first surviving phase size for small moduli.
    for m in [3, 5, 7, 9]:
        r = (m + 1) // 2
        builder = FirstReturnBuilder(m)
        choices: List[Optional[int]] = [None] + list(range(m))
        survivor_count = 0
        examples: List[Dict[str, object]] = []
        omission_positions = set()
        per_sign_counts = {"+1": 0, "-1": 0}
        for a in (1, -1):
            for pattern in itertools.product(choices, repeat=r):
                perm = builder.first_return_perm(r=r, a=a, pattern=pattern)
                if cycle_sizes_from_perm(perm) == [m]:
                    survivor_count += 1
                    per_sign_counts["+1" if a == 1 else "-1"] += 1
                    omission_positions.add(tuple(i for i, x in enumerate(pattern) if x is None))
                    if len(examples) < 6:
                        examples.append({'a': a, 'pattern': [None if x is None else int(x) for x in pattern]})
        summary['minimal_phase_catalog_small'][str(m)] = {
            'r': r,
            'survivor_count': survivor_count,
            'per_sign_counts': per_sign_counts,
            'omission_positions': [list(pos) for pos in sorted(omission_positions)],
            'examples': examples,
        }
        csv_rows.append({
            'kind': 'minimal_phase_catalog_small',
            'm': m,
            'r': r,
            'survivor_count': survivor_count,
            'example_pattern': '' if not examples else json.dumps(examples[0], sort_keys=True),
        })

    # Explicit candidate family and grouped point-defect sanity.
    for m in candidate_moduli:
        r, pattern = canonical_candidate_pattern(m)
        builder = FirstReturnBuilder(m)
        first_return = builder.first_return_perm(r=r, a=1, pattern=pattern)
        first_return_cycle_sizes = cycle_sizes_from_perm(first_return)
        base_sizes = orbit_sizes([(s, u) for s in range(m) for u in range(m)], base_step_factory(m=m, r=r, a=1, pattern=pattern))
        grouped_sizes = grouped_orbit_sizes_for_point_defect(m=m, r=r, a=1, pattern=pattern, defect=(0, 0))
        rec = {
            'r': r,
            'pattern': [None if x is None else int(x) for x in pattern],
            'first_return_cycle_sizes': first_return_cycle_sizes,
            'base_orbit_sizes': base_sizes,
            'grouped_point_defect_orbit_sizes': grouped_sizes,
            'single_base_orbit': base_sizes == [m * m],
            'single_grouped_orbit': grouped_sizes == [m * m * m],
            'first_return_perm': first_return,
        }
        summary['explicit_candidate_check'][str(m)] = rec
        csv_rows.append({
            'kind': 'explicit_candidate_check',
            'm': m,
            'r': r,
            'survivor_count': int(base_sizes == [m * m]),
            'example_pattern': json.dumps(rec['pattern']),
        })

    with summary_path.open('w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)

    with table_path.open('w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=['kind', 'm', 'r', 'survivor_count', 'example_pattern'])
        writer.writeheader()
        writer.writerows(csv_rows)

    print(summary_path)
    print(table_path)


if __name__ == '__main__':
    main()
