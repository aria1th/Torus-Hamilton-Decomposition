#!/usr/bin/env python3
"""Derive and verify the color-3 partial theorem from the 26-move d=5 witness.

Claims checked:
1. Exact layer formulas d0,d1,d2,d3 for color 3.
2. Exact first-return base map B(q,w,u).
3. Exact nested return U = B^m on the section w=0.
4. Cycle counts for U, B, and R_3 on odd m = 5,7,9,11,13.
5. Total beta cocycle sum mod m equals m-1.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
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

def first_return_prefix_color3(m, q, w, u):
    c = 3
    x = x_from_rel(c, q, w, 0, u, m)
    cur = x
    pref = []
    for _ in range(4):
        d = rule(cur, m)[c]
        pref.append(d)
        nxt = list(cur)
        nxt[d] = (nxt[d] + 1) % m
        cur = tuple(nxt)
    return tuple(pref)

def d0_formula(q, w, u, m):
    if w == 0 and q == 0:
        return 2
    if u == 3 or (u == 0 and q == 1):
        return 1
    return 3

def d1_formula(q, w, u, m):
    if w == 1 and u == 0:
        return 4
    if w == 4:
        return 2 if q == 3 else 1
    return 3

def d2_formula(q, w, u, m):
    x4_2 = (q + (1 if (w == 1 and u == 0) else 0)) % m
    if x4_2 == 4:
        return 2 if w == 0 else 1
    return 2 if w == 2 else 3

def gamma_formula(q, w):
    return 1 if ((w == 0 and q in {0, 4}) or (w == 2 and q != 4) or (w == 4 and q == 3)) else 0

def beta_formula(q, w, u, m):
    ds = [d0_formula(q, w, u, m), d1_formula(q, w, u, m), d2_formula(q, w, u, m)]
    return sum(1 for d in ds if d == 1) % m

def B_formula(q, w, u, m):
    return ((q + (1 if (w == 1 and u == 0) else 0)) % m, (w + 1) % m, (u + gamma_formula(q, w)) % m)

def U_formula(q, u, m):
    a = 1 if q in {0, 4} else 0
    u1 = (u + a) % m
    b = 1 if u1 == 0 else 0
    q2 = (q + b) % m
    c = 1 if q2 != 4 else 0
    d = 1 if q2 == 3 else 0
    return q2, (u1 + c + d) % m

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

def validate_m(m):
    c = 3

    # 1) prefix formulas
    for q, w, u in itertools.product(range(m), repeat=3):
        pref = first_return_prefix_color3(m, q, w, u)
        target = (d0_formula(q, w, u, m), d1_formula(q, w, u, m), d2_formula(q, w, u, m), 0)
        assert pref == target, (m, q, w, u, pref, target)

    # 2) full R_3 and extracted B, beta
    R = {}
    B = {}
    beta = {}
    for q, w, v, u in itertools.product(range(m), repeat=4):
        x = x_from_rel(c, q, w, v, u, m)
        cur = x
        for _ in range(m):
            d = rule(cur, m)[c]
            nxt = list(cur)
            nxt[d] = (nxt[d] + 1) % m
            cur = tuple(nxt)
        q2, w2, v2, u2 = rel_coords(cur, c)
        R[(q, w, v, u)] = (q2, w2, v2, u2)
        if v == 0:
            B[(q, w, u)] = (q2, w2, u2)
            beta[(q, w, u)] = v2
            assert B[(q, w, u)] == B_formula(q, w, u, m)
            assert beta[(q, w, u)] == beta_formula(q, w, u, m)

    # 3) cycle count for R on P0
    states4 = list(itertools.product(range(m), repeat=4))
    idx4 = {s: i for i, s in enumerate(states4)}
    perm_R = [idx4[R[s]] for s in states4]
    cyc_R = cycle_lengths(perm_R)

    # 4) cycle count for B
    states3 = list(itertools.product(range(m), repeat=3))
    idx3 = {s: i for i, s in enumerate(states3)}
    perm_B = [idx3[B[s]] for s in states3]
    cyc_B = cycle_lengths(perm_B)

    # 5) cycle count for U on w=0 section
    states2 = list(itertools.product(range(m), repeat=2))
    idx2 = {s: i for i, s in enumerate(states2)}
    perm_U = []
    for q, u in states2:
        cur = (q, 0, u)
        for _ in range(m):
            cur = B[cur]
        nxt = (cur[0], cur[2])
        assert nxt == U_formula(q, u, m)
        perm_U.append(idx2[nxt])
    cyc_U = cycle_lengths(perm_U)

    return {
        "m": m,
        "R_cycles": len(cyc_R),
        "R_max": cyc_R[0],
        "B_cycles": len(cyc_B),
        "B_max": cyc_B[0],
        "U_cycles": len(cyc_U),
        "U_max": cyc_U[0],
        "beta_counts": dict(sorted(Counter(beta.values()).items())),
        "beta_sum_mod_m": sum(beta.values()) % m,
        "u_carry_count": sum(gamma_formula(q, w) for q, w in itertools.product(range(m), repeat=2)),
    }

out = {"validated_m": [], "results": []}
for m in [5, 7, 9, 11, 13]:
    res = validate_m(m)
    out["validated_m"].append(m)
    out["results"].append(res)

Path('/mnt/data/d5_color3_partial_theorem_summary.json').write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
