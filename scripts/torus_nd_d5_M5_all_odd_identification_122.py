#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from torus_nd_d5_selector_star_common_119 import selector_perm_star

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = REPO_ROOT / 'RoundY' / 'checks' / 'd5_122_M5_all_odd_identification_summary.json'

EXACT_T_MODULI = [11, 13, 15, 17, 19, 21]
EXACT_U_MODULI = [11, 13, 15, 17, 19, 21]
SMALL_FULL_TORUS_MODULI = [5, 7, 9]


def apply_F_color4(m: int, x: Tuple[int, int, int, int, int]) -> Tuple[int, int, int, int, int]:
    p = selector_perm_star(m, x)
    j = p[4]
    y = list(x)
    y[j] = (y[j] + 1) % m
    return tuple(y)


def state_to_id(x: Tuple[int, int, int, int, int], m: int) -> int:
    return x[0] + m * (x[1] + m * (x[2] + m * (x[3] + m * x[4])))


def id_to_state(idx: int, m: int) -> Tuple[int, int, int, int, int]:
    x0 = idx % m
    idx //= m
    x1 = idx % m
    idx //= m
    x2 = idx % m
    idx //= m
    x3 = idx % m
    idx //= m
    x4 = idx % m
    return (x0, x1, x2, x3, x4)


def iterate_F(m: int, x: Tuple[int, int, int, int, int], steps: int) -> Tuple[int, int, int, int, int]:
    y = x
    for _ in range(steps):
        y = apply_F_color4(m, y)
    return y


def B_formula(m: int, a: int, b: int, u: int) -> int:
    if a != (u + 1) % m:
        eta = 1 if a in {0, 2, 4, m - 1} else 2
    else:
        if a in {2, 4}:
            eta = -1
        elif a in {0, m - 1}:
            eta = -3
        else:
            eta = -2
    return (b + eta) % m


def T_formula(m: int, a: int, b: int, u: int) -> Tuple[int, int, int]:
    B = B_formula(m, a, b, u)
    S = int((u != 6 % m) and (B == (m - 1) % m))
    if S == 1:
        eps1 = int(a == 3) ^ int(a == (u + 1) % m)
        eps2 = int(a == (m - 2) % m)
        eps3 = int(a == 1) ^ int(a == (u + 1) % m)
    else:
        eps1 = int(a == 4) ^ int(a == (u + 2) % m)
        eps2 = int(a == (m - 1) % m)
        eps3 = int(a == 2) ^ int(a == (u + 2) % m)
    return ((a + S) % m, (B + eps1 + eps2 + eps3) % m, (u + 1) % m)


def T_actual(m: int, a: int, b: int, u: int) -> Tuple[int, int, int]:
    x = (a, b, (u - a) % m, 0, (-u - b) % m)
    y = iterate_F(m, x, m * m)
    assert y[3] % m == 0
    return (y[0], y[1], (y[0] + y[2]) % m)


def U_via_T_formula(m: int, a: int, b: int) -> Tuple[int, int]:
    aa, bb, uu = a, b, 0
    for _ in range(m):
        aa, bb, uu = T_formula(m, aa, bb, uu)
    assert uu == 0
    return aa, bb


def U_actual(m: int, a: int, b: int) -> Tuple[int, int]:
    x = (a, b, (-a) % m, 0, (-b) % m)
    y = iterate_F(m, x, m ** 3)
    assert sum(y) % m == 0
    assert y[3] % m == 0
    assert (y[2] + y[0]) % m == 0
    assert (y[4] + y[1]) % m == 0
    return (y[0], y[1])


def U_natural_formula(m: int, a: int, b: int) -> Tuple[int, int]:
    if a == 0:
        if b in {(m - 8) % m, (m - 1) % m}:
            return (0, (b - 2) % m)
        return (1, (2 * b + 3) % m)
    if a == 1:
        if b == 1:
            return (7 % m, (m - 15) % m)
        if b == (m - 11) % m:
            return (1, (m - 13) % m)
        return (2, (b - 3) % m)
    if a == 2:
        if b == 0:
            return (2, (m - 2) % m)
        if b == (m - 12) % m:
            return (2, (m - 14) % m)
        return (3, (b - 3) % m)
    if a == 3:
        if b == (m - 1) % m:
            return (3, (m - 3) % m)
        if b == (m - 13) % m:
            return (3, (m - 15) % m)
        return (4, (b - 1) % m)
    if a == 4:
        if b == 0:
            return (4, (m - 2) % m)
        if b == (m - 12) % m:
            return (4, (m - 14) % m)
        return (5, (b - 3) % m)
    if a == 5:
        if b in {(m - 1) % m, (m - 13) % m}:
            return (5, (b - 2) % m)
        return (6, (b - 2) % m)
    if a == 6:
        if b in {(m - 1) % m, (m - 13) % m}:
            return (6, (b - 2) % m)
        return (7, (b - 2) % m)
    if a == 7:
        if b == (m - 1) % m:
            return (7, (b - 2) % m)
        return (8, (b - 2) % m)
    if a == 8:
        if b == (m - 15) % m:
            return (0, (m - 2) % m)
        if b == (m - 1) % m:
            return (8, (b - 2) % m)
        return (9 % m, (b - 2) % m)
    if 9 <= a <= m - 3:
        if b in {(m - 1) % m, (m - 15) % m}:
            return (a, (b - 2) % m)
        return ((a + 1) % m, (b - 2) % m)
    if a == m - 2:
        if b in {(m - 1) % m, (m - 15) % m}:
            return (a, (b - 2) % m)
        return (m - 1, (b - 1) % m)
    if a == m - 1:
        if b in {0, (m - 14) % m}:
            return (m - 1, (b - 2) % m)
        if b == 4:
            return (1, 1)
        if b == 2:
            return (0, (m - 1) % m)
        if b % 2 == 1:
            return (0, ((b + m - 6) // 2) % m)
        return (0, (b // 2 - 3) % m)
    raise AssertionError(f'unreachable row a={a}')


def correction_c(m: int) -> List[int]:
    c = [0] * m
    c[0] = 0
    c[1] = 3 % m
    c[2] = 6 % m
    c[3] = 9 % m
    c[4] = 10 % m
    for a in range(5, m - 1):
        c[a] = (2 * a + 3) % m
    c[m - 1] = 0
    return c


def model_rule(m: int, a: int, v: int) -> Tuple[str, Tuple[int, int]]:
    if a == 0:
        if v == (m - 8) % m:
            return ('row0_same_m_minus_8', (0, (v - 2) % m))
        if v == (m - 1) % m:
            return ('row0_same_m_minus_1', (0, (v - 2) % m))
        return ('row0_to_row1_affine', (1, (2 * v + 6) % m))
    if 1 <= a <= 6:
        if a == 1 and v == 4 % m:
            return ('row1_special_to_row7', (7 % m, 2 % m))
        if v == (2 * a + 2) % m:
            return ('line_A_same', (a, (v - 2) % m))
        if v == (2 * a - 10) % m:
            return ('line_B_early_same', (a, (v - 2) % m))
        return ('bulk', ((a + 1) % m, v))
    if a == 7:
        if v == (2 * a + 2) % m:
            return ('line_A_same', (a, (v - 2) % m))
        return ('bulk', ((a + 1) % m, v))
    if a == 8:
        if v == (2 * a - 12) % m:
            return ('row8_special_to_row0', (0, (m - 2) % m))
        if v == (2 * a + 2) % m:
            return ('line_A_same', (a, (v - 2) % m))
        return ('bulk', ((a + 1) % m, v))
    if 9 <= a <= m - 2:
        if v == (2 * a + 2) % m:
            return ('line_A_same', (a, (v - 2) % m))
        if v == (2 * a - 12) % m:
            return ('line_B_late_same', (a, (v - 2) % m))
        return ('bulk', ((a + 1) % m, v))
    if v == 0:
        return ('row_last_same_zero', (a, (v - 2) % m))
    if v == (m - 14) % m:
        return ('row_last_same_m_minus_14', (a, (v - 2) % m))
    if v == 4 % m:
        return ('row_last_special_to_row1', (1, 4 % m))
    if v == 2 % m:
        return ('row_last_special_to_row0_m_minus_1', (0, (m - 1) % m))
    if v % 2 == 1:
        return ('row_last_odd_half_to_row0', (0, ((v + m - 6) // 2) % m))
    return ('row_last_even_half_to_row0', (0, (v // 2 - 3) % m))


def check_T_exact(m: int) -> Dict[str, object]:
    mismatches = []
    checked = 0
    for a, b, u in itertools.product(range(m), repeat=3):
        actual = T_actual(m, a, b, u)
        formula = T_formula(m, a, b, u)
        checked += 1
        if actual != formula:
            mismatches.append({'state': [a, b, u], 'actual': list(actual), 'formula': list(formula)})
            if len(mismatches) >= 10:
                break
    return {
        'exact': not mismatches,
        'states_checked': checked,
        'sample_mismatches': mismatches,
    }


def check_U_formula_and_model(m: int) -> Dict[str, object]:
    mismatches_actual_vs_T = []
    mismatches_actual_vs_nat = []
    mismatches_nat_vs_model = []
    type_counts = Counter()
    corrected_map: Dict[Tuple[int, int], Tuple[int, int]] = {}
    c = correction_c(m)
    checked = 0
    for a, b in itertools.product(range(m), repeat=2):
        actual = U_actual(m, a, b)
        via_T = U_via_T_formula(m, a, b)
        natural = U_natural_formula(m, a, b)
        checked += 1
        if actual != via_T and len(mismatches_actual_vs_T) < 10:
            mismatches_actual_vs_T.append({'state': [a, b], 'actual': list(actual), 'via_T': list(via_T)})
        if actual != natural and len(mismatches_actual_vs_nat) < 10:
            mismatches_actual_vs_nat.append({'state': [a, b], 'actual': list(actual), 'natural': list(natural)})
        ap, bp = natural
        v = (b + c[a]) % m
        vp = (bp + c[ap]) % m
        kind, model_image = model_rule(m, a, v)
        corrected_map[(a, v)] = model_image
        if (ap, vp) != model_image and len(mismatches_nat_vs_model) < 10:
            mismatches_nat_vs_model.append({
                'natural_state': [a, b],
                'corrected_state': [a, v],
                'natural_image': [ap, vp],
                'model_image': [model_image[0], model_image[1]],
                'type': kind,
            })
        type_counts[kind] += 1
    cycle = cycle_summary_map(corrected_map, m)
    return {
        'actual_equals_T_formula': not mismatches_actual_vs_T,
        'actual_equals_natural_formula': not mismatches_actual_vs_nat,
        'natural_formula_equals_corrected_model': not mismatches_nat_vs_model,
        'states_checked': checked,
        'sample_mismatches_actual_vs_T': mismatches_actual_vs_T,
        'sample_mismatches_actual_vs_natural': mismatches_actual_vs_nat,
        'sample_mismatches_natural_vs_model': mismatches_nat_vs_model,
        'corrected_model_cycle_summary': cycle,
        'corrected_rule_type_counts': dict(sorted(type_counts.items())),
    }


def cycle_summary_map(mapping: Dict[Tuple[int, int], Tuple[int, int]], m: int) -> Dict[str, object]:
    states = [(a, b) for a in range(m) for b in range(m)]
    idx = {state: i for i, state in enumerate(states)}
    perm = [idx[mapping[state]] for state in states]
    visited = [False] * len(states)
    lengths: List[int] = []
    for i in range(len(states)):
        if visited[i]:
            continue
        cur = i
        length = 0
        while not visited[cur]:
            visited[cur] = True
            cur = perm[cur]
            length += 1
        lengths.append(length)
    lengths.sort(reverse=True)
    distribution = Counter(lengths)
    return {
        'cycle_count': len(lengths),
        'largest_cycle': lengths[0],
        'distribution': {str(k): v for k, v in sorted(distribution.items(), reverse=True)},
        'one_cycle': len(lengths) == 1,
    }


def check_full_torus_hamilton(m: int) -> Dict[str, object]:
    N = m ** 5
    perm = [0] * N
    for idx in range(N):
        x = id_to_state(idx, m)
        y = apply_F_color4(m, x)
        perm[idx] = state_to_id(y, m)
    visited = [False] * N
    lengths: List[int] = []
    for i in range(N):
        if visited[i]:
            continue
        cur = i
        length = 0
        while not visited[cur]:
            visited[cur] = True
            cur = perm[cur]
            length += 1
        lengths.append(length)
    lengths.sort(reverse=True)
    distribution = Counter(lengths)
    return {
        'state_count': N,
        'cycle_count': len(lengths),
        'largest_cycle': lengths[0],
        'distribution': {str(k): v for k, v in sorted(distribution.items(), reverse=True)},
        'hamilton': len(lengths) == 1,
    }


def main() -> None:
    summary = {
        'scope': {
            'note': 'RoundY/theorem/d5_122_M5_all_odd_identification.tex',
            'selector': 'Sel* color 4 from scripts/torus_nd_d5_selector_star_common_119.py',
            'exact_T_moduli': EXACT_T_MODULI,
            'exact_U_moduli': EXACT_U_MODULI,
            'small_full_torus_moduli': SMALL_FULL_TORUS_MODULI,
        },
        'T_formula_checks': {str(m): check_T_exact(m) for m in EXACT_T_MODULI},
        'U_formula_checks': {str(m): check_U_formula_and_model(m) for m in EXACT_U_MODULI},
        'small_full_torus_hamilton_checks': {str(m): check_full_torus_hamilton(m) for m in SMALL_FULL_TORUS_MODULI},
    }
    summary['all_T_exact'] = all(block['exact'] for block in summary['T_formula_checks'].values())
    summary['all_U_actual_equals_T_formula'] = all(block['actual_equals_T_formula'] for block in summary['U_formula_checks'].values())
    summary['all_U_actual_equals_natural_formula'] = all(block['actual_equals_natural_formula'] for block in summary['U_formula_checks'].values())
    summary['all_natural_equals_corrected_model'] = all(block['natural_formula_equals_corrected_model'] for block in summary['U_formula_checks'].values())
    summary['all_corrected_models_one_cycle'] = all(block['corrected_model_cycle_summary']['one_cycle'] for block in summary['U_formula_checks'].values())
    summary['all_small_full_torus_hamilton'] = all(block['hamilton'] for block in summary['small_full_torus_hamilton_checks'].values())
    OUT_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps({
        'all_T_exact': summary['all_T_exact'],
        'all_U_actual_equals_T_formula': summary['all_U_actual_equals_T_formula'],
        'all_U_actual_equals_natural_formula': summary['all_U_actual_equals_natural_formula'],
        'all_natural_equals_corrected_model': summary['all_natural_equals_corrected_model'],
        'all_corrected_models_one_cycle': summary['all_corrected_models_one_cycle'],
        'all_small_full_torus_hamilton': summary['all_small_full_torus_hamilton'],
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
