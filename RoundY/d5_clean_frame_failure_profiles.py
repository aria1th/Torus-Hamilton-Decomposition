#!/usr/bin/env python3
"""Clean-frame diagnostics and color-3 U/monodromy summary for the fixed 26-move d=5 witness.

For each tested modulus m and color c in {0,1,3,4}, compute:
- whether a clean frame exists, using the coordinate-free criterion
    R_c(x+k) = R_c(x) + k
  for some nonzero order-m translation vector k on P_0;
- cycle decomposition of the full first return R_c on P_0.

For color 3, also compute:
- the section map U_3 induced by the strict clock coordinate w;
- orbitwise monodromies of the top cocycle over U_3-orbits.
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

def first_return_map(c, m):
    out = {}
    for rel in itertools.product(range(m), repeat=4):
        cur = x_from_rel(c, rel, m)
        for _ in range(m):
            d = rule(cur, m)[c]
            nxt = list(cur)
            nxt[d] = (nxt[d] + 1) % m
            cur = tuple(nxt)
        out[rel] = rel_coords(cur, c)
    return out

def cycle_lengths_from_dict(F):
    states = list(F.keys())
    idx = {s: i for i, s in enumerate(states)}
    perm = [idx[F[s]] for s in states]
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

def clean_frame_directions(R, m):
    states = list(itertools.product(range(m), repeat=4))
    good = []
    for k in states[1:]:
        ok = True
        for x in states:
            y = tuple((x[i] + k[i]) % m for i in range(4))
            Rx = R[x]
            Ry = R[y]
            diff = tuple((Ry[i] - Rx[i]) % m for i in range(4))
            if diff != k:
                ok = False
                break
        if ok:
            good.append(k)
    return good

def color3_B_beta(m):
    c = 3
    B = {}
    beta = {}
    for q, w, u in itertools.product(range(m), repeat=3):
        x = x_from_rel(c, (q, w, 0, u), m)
        cur = x
        for _ in range(m):
            d = rule(cur, m)[c]
            nxt = list(cur)
            nxt[d] = (nxt[d] + 1) % m
            cur = tuple(nxt)
        q2, w2, v2, u2 = rel_coords(cur, c)
        B[(q, w, u)] = (q2, w2, u2)
        beta[(q, w, u)] = v2
    return B, beta

def color3_U_monodromy(m):
    B, beta = color3_B_beta(m)
    U = {}
    for q, u in itertools.product(range(m), repeat=2):
        cur = (q, 0, u)
        for _ in range(m):
            cur = B[cur]
        U[(q, u)] = (cur[0], cur[2])

    states = list(U.keys())
    seen = set()
    orbit_lengths = []
    monodromies = []
    for s in states:
        if s in seen:
            continue
        orbit = []
        cur = s
        while cur not in seen:
            seen.add(cur)
            orbit.append(cur)
            cur = U[cur]
        orbit_lengths.append(len(orbit))
        M = 0
        for q, u in orbit:
            cur3 = (q, 0, u)
            for _ in range(m):
                M = (M + beta[cur3]) % m
                cur3 = B[cur3]
        monodromies.append(M)

    return {
        "U_cycle_lengths": sorted(orbit_lengths, reverse=True),
        "orbit_monodromies_mod_m": monodromies,
    }

def main():
    out = {
        "tested_m": [5, 7, 9, 11],
        "colors": {},
    }
    for c in [0, 1, 3, 4]:
        out["colors"][str(c)] = {}
        for m in out["tested_m"]:
            R = first_return_map(c, m)
            dirs = clean_frame_directions(R, m)
            entry = {
                "clean_frame": bool(dirs),
                "num_commuting_directions": len(dirs),
                "sample_commuting_directions": dirs[:10],
                "R_cycle_lengths": cycle_lengths_from_dict(R),
            }
            if c == 3 and dirs:
                entry.update(color3_U_monodromy(m))
            else:
                entry["U_cycle_lengths"] = None
                entry["orbit_monodromies_mod_m"] = None
            out["colors"][str(c)][str(m)] = entry

    Path('/mnt/data/d5_clean_frame_failure_profiles.json').write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
