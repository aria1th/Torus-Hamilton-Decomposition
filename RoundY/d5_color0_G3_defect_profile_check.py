#!/usr/bin/env python3
from __future__ import annotations
import itertools, collections, math, json
from pathlib import Path

DIM = 5
G3 = [
    {'layer':3,'pair':(0,3),'type':'line1','axes':(1,), 'residues':(0,)},
    {'layer':1,'pair':(0,3),'type':'line1','axes':(1,), 'residues':(2,)},
    {'layer':2,'pair':(2,4),'type':'line1','axes':(3,), 'residues':(4,)},
]
SIGMA = (1,2,3,4,0)
ID = (0,1,2,3,4)
PAIRS = list(itertools.combinations(range(DIM), 2))

def make_orbit_rule(gates, m):
    def rule(x):
        layer = sum(x) % m
        dirs = list(SIGMA if layer == 0 else ID)
        if 1 <= layer <= 3:
            for gate in gates:
                if gate['layer'] != layer:
                    continue
                typ = gate['type']; pair = tuple(gate['pair'])
                for t in range(DIM):
                    if typ == 'plane':
                        ok = True
                    elif typ == 'line1':
                        ok = (x[(gate['axes'][0] + t) % DIM] == gate['residues'][0] % m)
                    elif typ == 'line2':
                        ok = (
                            x[(gate['axes'][0] + t) % DIM] == gate['residues'][0] % m and
                            x[(gate['axes'][1] + t) % DIM] == gate['residues'][1] % m
                        )
                    else:
                        raise ValueError(typ)
                    if ok:
                        a = (pair[0] + t) % DIM
                        b = (pair[1] + t) % DIM
                        dirs[a], dirs[b] = dirs[b], dirs[a]
        return tuple(dirs)
    return rule

def x_from_rel(c, rel, m):
    q, w, v, u = rel
    arr = [None] * DIM
    arr[(c + 1) % DIM] = q
    arr[(c + 2) % DIM] = w
    arr[(c + 3) % DIM] = v
    arr[(c + 4) % DIM] = u
    arr[c] = (-q - w - v - u) % m
    return tuple(arr)

def rel_coords(x, c):
    return tuple(x[(c + k) % DIM] for k in range(1, DIM))

def first_return(rule, c, m):
    out = {}
    for rel in itertools.product(range(m), repeat=4):
        cur = x_from_rel(c, rel, m)
        for _ in range(m):
            d = rule(cur)[c]
            nxt = list(cur); nxt[d] = (nxt[d] + 1) % m
            cur = tuple(nxt)
        out[rel] = rel_coords(cur, c)
    return out

def true_cycles(F):
    states = list(F.keys())
    idx = {s:i for i,s in enumerate(states)}
    nxt = [idx[F[s]] for s in states]
    color = [0] * len(states)
    cycles = []
    for i in range(len(states)):
        if color[i]:
            continue
        cur = i; stack = []; pos = {}
        while color[cur] == 0:
            color[cur] = 1
            pos[cur] = len(stack)
            stack.append(cur)
            cur = nxt[cur]
        if color[cur] == 1:
            cycles.append([states[j] for j in stack[pos[cur]:]])
        for v in stack:
            color[v] = 2
    return cycles

def clean_axes(R, m):
    goods = []
    for axis in range(4):
        k = [0] * 4; k[axis] = 1; k = tuple(k)
        ok = True
        for x, Rx in R.items():
            y = tuple((x[i] + k[i]) % m for i in range(4))
            Ry = R[y]
            if tuple((Ry[i] - Rx[i]) % m for i in range(4)) != k:
                ok = False
                break
        if ok:
            goods.append(axis)
    return goods

def quotient_map(R, fiber_axis, m):
    base_axes = [i for i in range(4) if i != fiber_axis]
    B = {}; beta = {}
    for base in itertools.product(range(m), repeat=3):
        rel = [0] * 4; bi = 0
        for i in range(4):
            if i == fiber_axis:
                rel[i] = 0
            else:
                rel[i] = base[bi]; bi += 1
        rel = tuple(rel)
        out = R[rel]
        B[base] = tuple(out[i] for i in base_axes)
        beta[base] = out[fiber_axis] % m
    return B, beta, base_axes

def strict_clocks(B, m):
    return [ax for ax in range(3) if all((B[x][ax] - x[ax]) % m == 1 for x in B)]

def section_return(B, beta, clock_axis, m):
    rem = [i for i in range(3) if i != clock_axis]
    U = {}; mon = {}
    for a in itertools.product(range(m), repeat=2):
        base = [0] * 3; ai = 0
        for j in range(3):
            if j == clock_axis:
                base[j] = 0
            else:
                base[j] = a[ai]; ai += 1
        base = tuple(base)
        cur = base; M = 0
        for _ in range(m):
            M = (M + beta[cur]) % m
            cur = B[cur]
        U[a] = tuple(cur[j] for j in rem)
        mon[a] = M
    return U, mon

def indegree_hist(F):
    ctr = collections.Counter(F.values())
    hist = collections.Counter(ctr.values())
    zeros = len(F) - len(ctr)
    if zeros:
        hist[0] = zeros
    return {str(k): hist[k] for k in sorted(hist)}

def bad_count(hist):
    return sum(v for k, v in hist.items() if int(k) != 1)

def R0_formula_G3(rel, m):
    q, w, v, u = rel
    d1 = 2 if v == 2 else 3 if q == 1 else 0
    d2 = 4 if (q == 3 and v == 4) else 2 if q == 3 else 3 if u == 4 else 0
    x3 = (v + (1 if d1 == 3 else 0) + (1 if d2 == 3 else 0)) % m
    d3 = 2 if x3 == 0 else 3 if q == m - 1 else 0
    return (
        (q + 1) % m,
        (w + (d1 == 2) + (d2 == 2) + (d3 == 2)) % m,
        (v + (d1 == 3) + (d2 == 3) + (d3 == 3)) % m,
        (u + (d2 == 4)) % m,
    ), {'d1': d1, 'd2': d2, 'd3': d3, 'x3': x3}

def defect_packets_formula(m):
    zero = []; two = []
    for q, w, v, u in itertools.product(range(m), repeat=4):
        if q == 0 and v == 1:
            zero.append((q, w, v, u))
        if q == 0 and v == 0:
            two.append((q, w, v, u))
        if q == 2 and ((u != 4 and v == 3) or (u == 4 and v == 4)):
            zero.append((q, w, v, u))
        if q == 2 and ((u != 4 and v == 2) or (u == 4 and v == 3)):
            two.append((q, w, v, u))
    return set(zero), set(two)

def verify_formula_and_packets(m):
    rule = make_orbit_rule(G3, m)
    R = first_return(rule, 0, m)
    zero_formula, two_formula = defect_packets_formula(m)
    pre = collections.defaultdict(list)
    mismatch = None
    for rel, out in R.items():
        calc, _ = R0_formula_G3(rel, m)
        if calc != out and mismatch is None:
            mismatch = (rel, out, calc)
        pre[out].append(rel)
    zero_actual = {s for s in R if s not in pre}
    two_actual = {y for y, arr in pre.items() if len(arr) == 2}
    return {
        'formula_match': mismatch is None,
        'formula_mismatch_example': mismatch,
        'zero_count': len(zero_actual),
        'two_count': len(two_actual),
        'zero_formula_match': zero_actual == zero_formula,
        'two_formula_match': two_actual == two_formula,
    }

def eval_color0(gates, m):
    rule = make_orbit_rule(gates, m)
    R = first_return(rule, 0, m)
    entry = {
        'R_num_cycles': len(true_cycles(R)),
        'R_indegree_hist': indegree_hist(R),
        'clean_axes': clean_axes(R, m),
        'frames': [],
    }
    for fa in entry['clean_axes']:
        B, beta, base_axes = quotient_map(R, fa, m)
        frame = {
            'fiber_axis': fa,
            'base_axes': list(base_axes),
            'B_num_cycles': len(true_cycles(B)),
            'B_indegree_hist': indegree_hist(B),
            'clock_axes': strict_clocks(B, m),
            'sections': [],
        }
        for ca in frame['clock_axes']:
            U, mon = section_return(B, beta, ca, m)
            Ucycles = true_cycles(U)
            mons = []
            for cyc in Ucycles:
                M = 0
                for s in cyc:
                    M = (M + mon[s]) % m
                mons.append(M)
            frame['sections'].append({
                'clock_axis': ca,
                'U_num_cycles': len(Ucycles),
                'U_indegree_hist': indegree_hist(U),
                'cycle_monodromies': mons,
            })
        entry['frames'].append(frame)
    return entry

def main():
    verification = {str(m): verify_formula_and_packets(m) for m in [5,7,9,11,13]}
    base_eval = eval_color0(G3, 7)
    base_bad = bad_count(base_eval['R_indegree_hist'])

    line1_catalog = []
    for layer in [1,2,3]:
        for pair in PAIRS:
            for ax in range(DIM):
                for r in range(7):
                    g = {'layer':layer,'pair':pair,'type':'line1','axes':(ax,), 'residues':(r,)}
                    if g not in G3:
                        line1_catalog.append(g)

    line1_samecore = 0
    line1_improve = 0
    for g in line1_catalog:
        res = eval_color0(G3 + [g], 7)
        good = False
        for fr in res['frames']:
            for sec in fr['sections']:
                if (
                    res['R_num_cycles'] == 1 and
                    fr['B_num_cycles'] == 1 and
                    sec['U_num_cycles'] == 1 and
                    sum(math.gcd(M, 7) == 1 for M in sec['cycle_monodromies']) == 1
                ):
                    good = True
                    break
            if good:
                break
        if good:
            line1_samecore += 1
            if bad_count(res['R_indegree_hist']) < base_bad:
                line1_improve += 1

    targeted = []
    for pair in PAIRS:
        for r in range(7):
            targeted.append({'layer':1,'pair':pair,'type':'line2','axes':(1,3),'residues':(2,r)})
            targeted.append({'layer':3,'pair':pair,'type':'line2','axes':(1,3),'residues':(0,r)})

    targeted_samecore = 0
    targeted_improve = 0
    for g in targeted:
        res = eval_color0(G3 + [g], 7)
        good = False
        for fr in res['frames']:
            for sec in fr['sections']:
                if (
                    res['R_num_cycles'] == 1 and
                    fr['B_num_cycles'] == 1 and
                    sec['U_num_cycles'] == 1 and
                    sum(math.gcd(M, 7) == 1 for M in sec['cycle_monodromies']) == 1
                ):
                    good = True
                    break
            if good:
                break
        if good:
            targeted_samecore += 1
            if bad_count(res['R_indegree_hist']) < base_bad:
                targeted_improve += 1

    summary = {
        'candidate_G3': G3,
        'verification': verification,
        'base_m7_eval': base_eval,
        'base_bad_m7': base_bad,
        'single_line1_exhaustive_m7': {
            'num_candidates': len(line1_catalog),
            'num_same_single_core_unit_monodromy': line1_samecore,
            'num_strict_R_bad_improvements': line1_improve,
        },
        'single_targeted_line2_m7': {
            'num_candidates': len(targeted),
            'num_same_single_core_unit_monodromy': targeted_samecore,
            'num_strict_R_bad_improvements': targeted_improve,
        }
    }
    out_path = Path('/mnt/data/d5_color0_G3_defect_profile_summary.json')
    out_path.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
