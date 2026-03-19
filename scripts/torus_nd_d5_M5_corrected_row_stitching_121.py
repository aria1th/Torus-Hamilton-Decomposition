#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = REPO_ROOT / 'RoundY' / 'checks' / 'd5_121_M5_corrected_row_stitching_summary.json'
CHECKED_MODULI = list(range(11, 102, 2))


def model_rule(m: int, a: int, v: int):
    if a == 0:
        if v == (m - 8) % m:
            return (0, (v - 2) % m), 'row0_same_m_minus_8'
        if v == m - 1:
            return (0, (v - 2) % m), 'row0_same_m_minus_1'
        return (1, (2 * v + 6) % m), 'row0_to_row1_affine'

    if 1 <= a <= 6:
        if a == 1 and v == 4 % m:
            return (7 % m, 2 % m), 'row1_special_to_row7'
        if v == (2 * a + 2) % m:
            return (a, (v - 2) % m), 'line_A_same'
        if v == (2 * a - 10) % m:
            return (a, (v - 2) % m), 'line_B_early_same'
        return ((a + 1) % m, v), 'bulk'

    if a == 7:
        if v == (2 * a + 2) % m:
            return (a, (v - 2) % m), 'line_A_same'
        return ((a + 1) % m, v), 'bulk'

    if a == 8:
        if v == (2 * a - 12) % m:
            return (0, m - 2), 'row8_special_to_row0'
        if v == (2 * a + 2) % m:
            return (a, (v - 2) % m), 'line_A_same'
        return ((a + 1) % m, v), 'bulk'

    if 9 <= a <= m - 2:
        if v == (2 * a + 2) % m:
            return (a, (v - 2) % m), 'line_A_same'
        if v == (2 * a - 12) % m:
            return (a, (v - 2) % m), 'line_B_late_same'
        return ((a + 1) % m, v), 'bulk'

    if v == 0:
        return (a, (v - 2) % m), 'row_last_same_zero'
    if v == (m - 14) % m:
        return (a, (v - 2) % m), 'row_last_same_m_minus_14'
    if v == 4 % m:
        return (1, 4 % m), 'row_last_special_to_row1'
    if v == 2 % m:
        return (0, m - 1), 'row_last_special_to_row0_m_minus_1'
    if v % 2 == 1:
        return (0, ((v + (m - 6)) // 2) % m), 'row_last_odd_half_to_row0'
    return (0, (v // 2 - 3) % m), 'row_last_even_half_to_row0'


def first_return_segment(m: int, t: int):
    cur = (0, t)
    seg = []
    kinds = []
    while True:
        seg.append(cur)
        nxt, kind = model_rule(m, *cur)
        kinds.append(kind)
        cur = nxt
        if cur[0] == 0:
            return {
                'start': [0, t],
                'segment': seg,
                'end': cur,
                'length': len(seg),
                'kinds': kinds,
            }


def expected_length(m: int, t: int) -> int:
    if t in {(m - 8) % m, m - 1}:
        return 1
    if t == 0:
        return 10
    if t == 1:
        return 2 * m - 4
    return m + 2


def expected_end(m: int, t: int):
    return (0, (t - 2) % m)


def cycle_summary(m: int):
    states = [(a, v) for a in range(m) for v in range(m)]
    idx = {state: i for i, state in enumerate(states)}
    perm = [idx[model_rule(m, *s)[0]] for s in states]
    seen = [False] * len(states)
    lengths = []
    for i in range(len(states)):
        if seen[i]:
            continue
        j = i
        L = 0
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            L += 1
        lengths.append(L)
    lengths.sort(reverse=True)
    return {
        'cycle_count': len(lengths),
        'largest_cycle': lengths[0],
        'distribution': {str(k): v for k, v in sorted(Counter(lengths).items(), reverse=True)},
        'hamilton': len(lengths) == 1,
    }


def analyze_modulus(m: int):
    segments = {}
    seen_state_to_t = {}
    overlaps = []
    distribution = Counter()
    row0_map_ok = True
    for t in range(m):
        info = first_return_segment(m, t)
        segments[t] = info
        distribution[info['length']] += 1
        if tuple(info['end']) != expected_end(m, t):
            row0_map_ok = False
        if info['length'] != expected_length(m, t):
            row0_map_ok = False
        for state in info['segment']:
            if state in seen_state_to_t:
                overlaps.append({'state': list(state), 't1': seen_state_to_t[state], 't2': t})
                break
            seen_state_to_t[state] = t
    total_length = sum(info['length'] for info in segments.values())
    return {
        'row0_first_return_matches_formula': row0_map_ok,
        'segment_lengths_distribution': {str(k): v for k, v in sorted(distribution.items())},
        'segments_pairwise_disjoint': not overlaps,
        'sample_overlap': overlaps[:5],
        'total_segment_length': total_length,
        'total_segment_length_equals_m2': total_length == m * m,
        'distinct_states_in_segment_union': len(seen_state_to_t),
        'segment_union_equals_m2': len(seen_state_to_t) == m * m,
        'cycle_summary': cycle_summary(m),
    }


def main():
    per_modulus = {str(m): analyze_modulus(m) for m in CHECKED_MODULI}
    summary = {
        'scope': {
            'object': 'corrected-row model U_m^sharp on S_m=(Z/mZ)^2',
            'checked_moduli': CHECKED_MODULI,
        },
        'expected_row0_first_return': {
            'map': 't -> t-2 mod m',
            'times': {
                '1': 't in {m-8, m-1}',
                '10': 't = 0',
                '2m-4': 't = 1',
                'm+2': 'otherwise',
            },
        },
        'all_moduli_match_row0_formula': all(item['row0_first_return_matches_formula'] for item in per_modulus.values()),
        'all_moduli_segments_disjoint': all(item['segments_pairwise_disjoint'] for item in per_modulus.values()),
        'all_moduli_segment_union_equals_m2': all(item['segment_union_equals_m2'] for item in per_modulus.values()),
        'all_moduli_hamilton': all(item['cycle_summary']['hamilton'] for item in per_modulus.values()),
        'per_modulus': per_modulus,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2))
    print(OUT_JSON)


if __name__ == '__main__':
    main()
