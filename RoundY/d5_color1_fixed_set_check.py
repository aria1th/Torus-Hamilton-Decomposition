#!/usr/bin/env python3
"""Verify the color-1 fixed-point obstruction for the fixed 26-move d=5 witness.

Claim:
On P0 with relative coordinates (q,w,v,u)=(x2,x3,x4,x0),
the color-1 first return R_1 has the exact fixed set

F_m = { (q,w,v,u):
        v not in {0,1,2,3,4},
        u != 4,
        q not in {2,3},
        and not (q=1 and w in {0,2}) }.

Hence for every m >= 6,
|Fix(R_1)| = (m^2 - 2m - 2)(m-5)(m-1) > 0,
so color 1 cannot be Hamilton.
"""
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

def first_return_map_color1(m):
    c = 1
    out = {}
    for q, w, v, u in itertools.product(range(m), repeat=4):
        x = x_from_rel(c, q, w, v, u, m)
        cur = x
        for _ in range(m):
            d = rule(cur, m)[c]
            nxt = list(cur)
            nxt[d] = (nxt[d] + 1) % m
            cur = tuple(nxt)
        out[(q, w, v, u)] = rel_coords(cur, c)
    return out

def fixed_condition(q, w, v, u, m):
    return (v not in {0, 1, 2, 3, 4}) and (u != 4) and (q not in {2, 3}) and (not (q == 1 and w in {0, 2}))

out = {"validated_m": [], "results": []}
for m in range(5, 13):
    R = first_return_map_color1(m)
    fixed = [s for s, t in R.items() if s == t]
    for s in itertools.product(range(m), repeat=4):
        assert (R[s] == s) == fixed_condition(*s, m)
    formula_count = (m*m - 2*m - 2) * max(m - 5, 0) * (m - 1)
    out["validated_m"].append(m)
    out["results"].append({
        "m": m,
        "fixed_points_on_P0": len(fixed),
        "formula_count": formula_count,
        "matches_formula": len(fixed) == formula_count,
        "has_hamilton_obstruction": len(fixed) > 0,
    })

Path('/mnt/data/d5_color1_fixed_set_summary.json').write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
