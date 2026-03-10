#!/usr/bin/env python3
"""Verify the exact color-0 first-return formula and the even-m obstruction."""
from __future__ import annotations
import itertools, json
from pathlib import Path

DIM = 5
payload = json.loads(Path('/mnt/data/d5_m5_kempe_witness_26.json').read_text())
moves = payload["moves"]


def in_support(x, support, m):
    typ = support[0]
    layer = support[1] % m
    if sum(x) % m != layer:
        return False
    if typ == "plane":
        return True
    if typ == "line1":
        _, _, axis, residue = support
        return x[axis] % m == residue % m
    if typ == "line2":
        _, _, axes, residues = support
        return x[axes[0]] % m == residues[0] % m and x[axes[1]] % m == residues[1] % m
    raise ValueError(f"unknown support type: {typ}")


def rule(x, m):
    dirs = list(range(DIM))
    for mv in moves:
        if in_support(x, mv["support"], m):
            a, b = mv["pair"]
            dirs[a], dirs[b] = dirs[b], dirs[a]
    return tuple(dirs)


def x_from_rel(c, q, w, v, u, m):
    arr = [None] * DIM
    arr[(c + 1) % DIM] = q
    arr[(c + 2) % DIM] = w
    arr[(c + 3) % DIM] = v
    arr[(c + 4) % DIM] = u
    arr[c] = (-q - w - v - u) % m
    return tuple(arr)


def rel_coords(x, c):
    return tuple(x[(c + k) % DIM] for k in range(1, DIM))


def prefix_actual_color0(m, q, w, v, u):
    x = x_from_rel(0, q, w, v, u, m)
    cur = x
    pref = []
    for _ in range(4):
        d = rule(cur, m)[0]
        pref.append(d)
        nxt = list(cur)
        nxt[d] = (nxt[d] + 1) % m
        cur = tuple(nxt)
    return tuple(pref)


def d1_formula(q, w, v, u, m):
    if q == 2 and w == 0 and (q + v + u) % m == 0:
        return 3
    if q == 2:
        return 4
    if u == 1:
        return 2
    return 0


def d2_formula(q, w, v, u, m):
    if q == 0 and u == 4:
        return 2 if (w + v) % m == (m - 4) % m else 3
    if q != 2 and u == 2:
        return 1
    if q != 2 and u == 0 and v == 4:
        return 1
    if q == 2 and w == 0 and (v + u) % m == (m - 2) % m:
        return 1 if u == 2 else 0
    if q == 2 and u == 1:
        return 1
    if q == 2 and u == (m - 1) % m and v == 4:
        return 1
    return 0


def d3_formula(q, w, v, u, m):
    d1 = d1_formula(q, w, v, u, m)
    d2 = d2_formula(q, w, v, u, m)
    s = (q + w + v + u) % m
    x0_before_layer3 = (-s + 1 + (1 if d1 == 0 else 0) + (1 if d2 == 0 else 0)) % m
    x2_before_layer3 = (w + (1 if d1 == 2 else 0) + (1 if d2 == 2 else 0)) % m
    if x0_before_layer3 == 4:
        return 2
    if x2_before_layer3 == 2:
        return 1
    return 3


def R0_formula(q, w, v, u, m):
    d1 = d1_formula(q, w, v, u, m)
    d2 = d2_formula(q, w, v, u, m)
    d3 = d3_formula(q, w, v, u, m)
    dq = (1 if d2 == 1 else 0) + (1 if d3 == 1 else 0)
    dw = (1 if d1 == 2 else 0) + (1 if d2 == 2 else 0) + (1 if d3 == 2 else 0)
    dv = (1 if d1 == 3 else 0) + (1 if d2 == 3 else 0) + (1 if d3 == 3 else 0)
    du = (1 if d1 == 4 else 0)
    return ((q + dq) % m, (w + dw) % m, (v + dv) % m, (u + du) % m)


def cycle_lengths(perm):
    seen = [False] * len(perm)
    out = []
    for i in range(len(perm)):
        if seen[i]:
            continue
        cur = i
        L = 0
        while not seen[cur]:
            seen[cur] = True
            cur = perm[cur]
            L += 1
        out.append(L)
    return sorted(out, reverse=True)


def cycle_stats_formula(m):
    states = list(itertools.product(range(m), repeat=4))
    idx = {s: i for i, s in enumerate(states)}
    perm = [idx[R0_formula(*s, m)] for s in states]
    cyc = cycle_lengths(perm)
    return {
        "m": m,
        "cycles": len(cyc),
        "top_lengths": cyc[:10],
        "min_length": cyc[-1],
        "max_length": cyc[0],
    }


def validate_formula_range(lo=6, hi=16):
    validated = []
    for m in range(lo, hi + 1):
        for q, w, v, u in itertools.product(range(m), repeat=4):
            pref = prefix_actual_color0(m, q, w, v, u)
            target_pref = (0, d1_formula(q, w, v, u, m), d2_formula(q, w, v, u, m), d3_formula(q, w, v, u, m))
            assert pref == target_pref, (m, (q, w, v, u), pref, target_pref)
            x = x_from_rel(0, q, w, v, u, m)
            cur = x
            for _ in range(m):
                d = rule(cur, m)[0]
                nxt = list(cur)
                nxt[d] = (nxt[d] + 1) % m
                cur = tuple(nxt)
            assert rel_coords(cur, 0) == R0_formula(q, w, v, u, m), (m, (q, w, v, u), rel_coords(cur, 0), R0_formula(q, w, v, u, m))
        validated.append(m)
    return validated


def even_invariant_family_check(m):
    families = []
    for w in range(m):
        if w == 2:
            continue
        line = [(0, w, v, 4) for v in range(m) if (v - (w + 1)) % 2 == 0]
        images = [R0_formula(*s, m) for s in line]
        assert set(images) == set(line), (m, w, "not invariant")
        for s in line:
            q, ww, v, u = s
            assert R0_formula(*s, m) == (0, ww, (v + 2) % m, 4), (m, s, R0_formula(*s, m))
        families.append({"w": w, "size": len(line)})
    return {"m": m, "num_cycles_Lw": len(families), "cycle_length_each": m // 2}


def generic_region_check(m):
    count = 0
    for q, w, v, u in itertools.product(range(m), repeat=4):
        if q in {0, 2}:
            continue
        if u in {0, 1, 2, 4, (m - 1) % m}:
            continue
        assert d1_formula(q, w, v, u, m) == 0
        assert d2_formula(q, w, v, u, m) == 0
        d3 = d3_formula(q, w, v, u, m)
        s = (q + w + v + u) % m
        if s == (m - 1) % m:
            assert d3 == 2
        elif w == 2:
            assert d3 == 1
        else:
            assert d3 == 3
        count += 1
    return count


def main():
    out = {
        "formula_validated_m": validate_formula_range(),
        "even_obstruction_checks": [],
        "generic_region_counts": {},
        "odd_cycle_stats": [],
    }
    for m in range(6, 19):
        if m % 2 == 0:
            out["even_obstruction_checks"].append(even_invariant_family_check(m))
        out["generic_region_counts"][str(m)] = generic_region_check(m)
    for m in [7, 9, 11, 13, 15, 17, 19, 21, 23]:
        out["odd_cycle_stats"].append(cycle_stats_formula(m))
    Path('/mnt/data/d5_color0_formula_and_even_obstruction_summary.json').write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
