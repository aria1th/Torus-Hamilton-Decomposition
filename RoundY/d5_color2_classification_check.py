#!/usr/bin/env python3
"""Verify the color-2 classification for the fixed 26-move d=5 witness.

Claims:
1. Exact layer-by-layer first-return prefix formulas for color 2.
2. Exact first-return formula R_2 on P0 in relative coordinates.
3. Exact nested section maps T and U.
4. U(q,u) = (q, u+3) except on the diagonal q+u=m-3, where U(q,u)=(q-1,u+4).
5. Therefore color 2 is Hamilton iff gcd(m,3)=1.
"""
from __future__ import annotations
import itertools, json, math
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

def first_return_prefix(c, m, q, w, v, u):
    x = x_from_rel(c, q, w, v, u, m)
    cur = x
    pref = []
    for _ in range(4):
        d = rule(cur, m)[c]
        pref.append(d)
        nxt = list(cur)
        nxt[d] = (nxt[d] + 1) % m
        cur = tuple(nxt)
    return tuple(pref)

def prefix_formula_color2(q, w, v, u, m):
    if w == 0 and v == 0:
        d0 = 1 if (q + u) % m == (m - 3) % m else 3
    else:
        d0 = 2

    if w == 1:
        d1 = 0
    elif w == 3 or (w == 4 and v == 2):
        d1 = 1
    else:
        d1 = 2

    if w == 1 or (w == 3 and v == 4) or (w == 4 and v == 0):
        d2 = 1
    elif w != 1 and v == 2:
        d2 = 3
    else:
        d2 = 2

    d3 = 4
    return (d0, d1, d2, d3)

def R_formula_color2(q, w, v, u, m):
    s = (q + u) % m
    q_inc = (1 if (w == 0 and v == 0 and s != (m - 3) % m) else 0) + (1 if (w != 1 and v == 2) else 0)
    v_inc = 1 if w == 1 else 0
    u_inc = (
        (1 if (w == 0 and v == 0 and s == (m - 3) % m) else 0)
        + (1 if (w == 3 or (w == 4 and v == 2)) else 0)
        + (1 if (w == 1 or (w == 3 and v == 4) or (w == 4 and v == 0)) else 0)
    )
    return ((q + q_inc) % m, (w + 1) % m, (v + v_inc) % m, (u + u_inc) % m)

def T_formula_color2(q, v, u, m):
    s = (q + u) % m
    if v == 0:
        q_inc = 0 if s == (m - 3) % m else 1
    elif v == 1:
        q_inc = (m - 2) % m
    elif v == 2:
        q_inc = 1
    else:
        q_inc = 0

    u_inc = 2 + (1 if (v == 0 and s == (m - 3) % m) else 0) + (1 if v == 1 else 0) + (1 if v == 3 else 0) + (1 if v == (m - 1) % m else 0)
    return ((q + q_inc) % m, (v + 1) % m, (u + u_inc) % m)

def U_formula_color2(q, u, m):
    if (q + u) % m == (m - 3) % m:
        return ((q - 1) % m, (u + 4) % m)
    return (q, (u + 3) % m)

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

def verify_m(m):
    c = 2
    R = {}
    for q, w, v, u in itertools.product(range(m), repeat=4):
        pref_actual = first_return_prefix(c, m, q, w, v, u)
        pref_formula = prefix_formula_color2(q, w, v, u, m)
        assert pref_actual == pref_formula, (m, (q, w, v, u), pref_actual, pref_formula)

        x = x_from_rel(c, q, w, v, u, m)
        cur = x
        for _ in range(m):
            d = rule(cur, m)[c]
            nxt = list(cur)
            nxt[d] = (nxt[d] + 1) % m
            cur = tuple(nxt)
        R[(q, w, v, u)] = rel_coords(cur, c)
        assert R[(q, w, v, u)] == R_formula_color2(q, w, v, u, m)

    states4 = list(R.keys())
    idx4 = {s: i for i, s in enumerate(states4)}
    perm_R = [idx4[R[s]] for s in states4]
    cyc_R = cycle_lengths(perm_R)

    T = {}
    for q, v, u in itertools.product(range(m), repeat=3):
        cur = (q, 0, v, u)
        for _ in range(m):
            cur = R[cur]
        T[(q, v, u)] = (cur[0], cur[2], cur[3])
        assert T[(q, v, u)] == T_formula_color2(q, v, u, m)

    states3 = list(T.keys())
    idx3 = {s: i for i, s in enumerate(states3)}
    perm_T = [idx3[T[s]] for s in states3]
    cyc_T = cycle_lengths(perm_T)

    U = {}
    for q, u in itertools.product(range(m), repeat=2):
        cur = (q, 0, u)
        for _ in range(m):
            cur = T[cur]
        U[(q, u)] = (cur[0], cur[2])
        assert U[(q, u)] == U_formula_color2(q, u, m)

    states2 = list(U.keys())
    idx2 = {s: i for i, s in enumerate(states2)}
    perm_U = [idx2[U[s]] for s in states2]
    cyc_U = cycle_lengths(perm_U)

    return {
        "m": m,
        "gcd_m_3": math.gcd(m, 3),
        "R_cycles": len(cyc_R),
        "R_max": cyc_R[0],
        "T_cycles": len(cyc_T),
        "T_max": cyc_T[0],
        "U_cycles": len(cyc_U),
        "U_max": cyc_U[0],
        "hamilton_color2": len(cyc_R) == 1,
    }

out = {"validated_m": [], "results": []}
for m in range(5, 17):
    res = verify_m(m)
    out["validated_m"].append(m)
    out["results"].append(res)

Path('/mnt/data/d5_color2_classification_summary.json').write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
