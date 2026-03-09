#!/usr/bin/env python3
"""
torus_swap_search.py

Hybrid solver for Hamilton decomposition of the directed 3D torus D(m):

Vertices: (i,j,k) in Z_m^3.
Arcs: +i, +j, +k.

Goal: decompose all arcs into 3 directed Hamilton cycles (each length m^3).

Strategy:
  1) Build ONE random 1-factorization (three perfect matchings) via:
       - pick a random perfect matching M0 (Hopcroft–Karp),
       - split the remaining 2-regular bipartite graph into M1,M2.
  2) If already Hamilton, done.
  3) Otherwise, repeatedly apply Codex-style alternating-cycle swaps:
       - pick colors r,s,
       - tau = f_s^{-1} o f_r,
       - pick a tau-cycle,
       - swap colors on vertices in that cycle.

Notes:
  - The swap move preserves sign(f_r)*sign(f_s), hence preserves global product sign.
    For even m (n even), a triple of Hamilton n-cycles must have product sign = -1.
    So for even m we *reject* random starts with product sign +1 (or just restart).

No external dependencies (stdlib only).
"""

from __future__ import annotations
import argparse
import math
import random
from collections import deque
from typing import List, Optional, Tuple


# ---------- basic torus helpers ----------
DIRS = (0, 1, 2)  # 0:+i, 1:+j, 2:+k


def coords(v: int, m: int) -> Tuple[int, int, int]:
    k = v % m
    j = (v // m) % m
    i = v // (m * m)
    return i, j, k


def vid(i: int, j: int, k: int, m: int) -> int:
    return (i * m + j) * m + k


def neighbor(v: int, d: int, m: int) -> int:
    i, j, k = coords(v, m)
    if d == 0:
        i = (i + 1) % m
    elif d == 1:
        j = (j + 1) % m
    else:
        k = (k + 1) % m
    return vid(i, j, k, m)


# ---------- permutation / cycle utilities ----------
def cycle_count(perm: List[int]) -> int:
    n = len(perm)
    seen = [False] * n
    cnt = 0
    for s in range(n):
        if not seen[s]:
            cnt += 1
            cur = s
            while not seen[cur]:
                seen[cur] = True
                cur = perm[cur]
    return cnt


def perm_sign(perm: List[int]) -> int:
    """Return +1 or -1."""
    n = len(perm)
    seen = [False] * n
    sgn = 1
    for i in range(n):
        if not seen[i]:
            cur = i
            L = 0
            while not seen[cur]:
                seen[cur] = True
                cur = perm[cur]
                L += 1
            if (L - 1) % 2 == 1:
                sgn *= -1
    return sgn


def verify_basic(m: int, nexts: List[List[int]]) -> Tuple[bool, str]:
    """Verify outgoing partition + each color is a permutation."""
    n = m ** 3
    if len(nexts) != 3 or any(len(nexts[c]) != n for c in range(3)):
        return False, "wrong shape"

    # outgoing distinct
    for v in range(n):
        outs = [nexts[c][v] for c in range(3)]
        if len(set(outs)) != 3:
            return False, f"vertex {v} repeats an outgoing edge"

    # each color indegree 1 and legal edges
    for c in range(3):
        indeg = [0] * n
        for v in range(n):
            w = nexts[c][v]
            if w not in (neighbor(v, 0, m), neighbor(v, 1, m), neighbor(v, 2, m)):
                return False, f"illegal arc at v={v} color={c}"
            indeg[w] += 1
        if any(x != 1 for x in indeg):
            return False, f"color {c} not a permutation"
    return True, "ok"


# ---------- Hopcroft–Karp for one perfect matching ----------
def hopcroft_karp(adj: List[List[int]], rng: random.Random) -> Optional[List[int]]:
    """
    Bipartite graph: U = tails 0..n-1, V = heads 0..n-1
    adj[u] lists heads.

    Return pairU[u]=matched head, or None if not perfect.
    """
    n = len(adj)
    for u in range(n):
        rng.shuffle(adj[u])

    INF = 10 ** 9
    pairU = [-1] * n
    pairV = [-1] * n
    dist = [INF] * n

    def bfs() -> bool:
        q = deque()
        for u in range(n):
            if pairU[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF
        found = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                u2 = pairV[v]
                if u2 == -1:
                    found = True
                elif dist[u2] == INF:
                    dist[u2] = dist[u] + 1
                    q.append(u2)
        return found

    def dfs(u: int) -> bool:
        for v in adj[u]:
            u2 = pairV[v]
            if u2 == -1 or (dist[u2] == dist[u] + 1 and dfs(u2)):
                pairU[u] = v
                pairV[v] = u
                return True
        dist[u] = INF
        return False

    matching = 0
    while bfs():
        free = [u for u in range(n) if pairU[u] == -1]
        rng.shuffle(free)
        for u in free:
            if pairU[u] == -1 and dfs(u):
                matching += 1
    if matching != n:
        return None
    return pairU


def random_factorization(m: int, rng: random.Random) -> Optional[List[List[int]]]:
    """
    Build 3 perfect matchings:
      - M0 via Hopcroft–Karp,
      - split remaining 2-regular graph into M1,M2 by alternating cycles.
    Return nexts[color][tail]=head.
    """
    n = m ** 3
    adj = [[] for _ in range(n)]
    for u in range(n):
        adj[u] = [neighbor(u, d, m) for d in DIRS]

    M0 = hopcroft_karp(adj, rng)
    if M0 is None:
        return None

    rem_tail = [[] for _ in range(n)]
    rem_head = [[] for _ in range(n)]
    for u in range(n):
        mh = M0[u]
        for h in adj[u]:
            if h == mh:
                continue
            rem_tail[u].append(h)
            rem_head[h].append(u)

    for u in range(n):
        if len(rem_tail[u]) != 2:
            return None
    for h in range(n):
        if len(rem_head[h]) != 2:
            return None

    M1 = [-1] * n
    M2 = [-1] * n
    used = set()

    for u0 in range(n):
        for h0 in rem_tail[u0]:
            if (u0, h0) in used:
                continue

            # traverse even cycle in union of remaining edges
            edges = []
            u, h = u0, h0
            while True:
                edges.append((u, h))
                used.add((u, h))

                u2 = rem_head[h][0] if rem_head[h][0] != u else rem_head[h][1]
                edges.append((u2, h))
                used.add((u2, h))

                h2 = rem_tail[u2][0] if rem_tail[u2][0] != h else rem_tail[u2][1]
                u, h = u2, h2
                if u == u0 and h == h0:
                    break

            flip = rng.randrange(2)
            for idx, (t, hh) in enumerate(edges):
                if (idx + flip) % 2 == 0:
                    M1[t] = hh
                else:
                    M2[t] = hh

    if any(x == -1 for x in M1) or any(x == -1 for x in M2):
        return None
    nexts = [M0, M1, M2]
    ok, _ = verify_basic(m, nexts)
    return nexts if ok else None


# ---------- Codex swap move ----------
def tau_cycles(f: List[int], g: List[int]) -> List[List[int]]:
    """
    tau = g^{-1} o f.
    Return tau cycles as lists of vertices.
    """
    n = len(f)
    invg = [0] * n
    for u, h in enumerate(g):
        invg[h] = u
    tau = [0] * n
    for u in range(n):
        tau[u] = invg[f[u]]

    seen = [False] * n
    cycles: List[List[int]] = []
    for s in range(n):
        if not seen[s]:
            cur = s
            cyc = []
            while not seen[cur]:
                seen[cur] = True
                cyc.append(cur)
                cur = tau[cur]
            cycles.append(cyc)
    return cycles


def swap_on_vertices(nexts: List[List[int]], c1: int, c2: int, verts: List[int]) -> None:
    """In-place swap of outgoing heads for colors c1,c2 on given tails."""
    f1 = nexts[c1]
    f2 = nexts[c2]
    for v in verts:
        f1[v], f2[v] = f2[v], f1[v]


def objective(nexts: List[List[int]]) -> int:
    """Sum over colors of (cycle_count - 1)."""
    return sum(cycle_count(nexts[c]) - 1 for c in range(3))


def is_hamilton_decomp(nexts: List[List[int]]) -> bool:
    return all(cycle_count(nexts[c]) == 1 for c in range(3))


def solve(
    m: int,
    seed: int,
    restarts: int,
    steps: int,
    temp: float,
    verbose: bool,
) -> Optional[List[List[int]]]:
    rng = random.Random(seed)
    n = m ** 3

    target_sign_prod = None
    if n % 2 == 0:
        # each Hamilton n-cycle has sign -1, so product must be -1
        target_sign_prod = -1

    best = None
    best_obj = 10 ** 18

    for r in range(1, restarts + 1):
        nexts = random_factorization(m, rng)
        if nexts is None:
            continue

        if target_sign_prod is not None:
            sp = perm_sign(nexts[0]) * perm_sign(nexts[1]) * perm_sign(nexts[2])
            if sp != target_sign_prod:
                continue

        cur_obj = objective(nexts)
        if cur_obj < best_obj:
            best_obj = cur_obj
            best = [arr[:] for arr in nexts]
        if verbose:
            print(f"[restart {r}] start objective={cur_obj}")

        if is_hamilton_decomp(nexts):
            return nexts

        for step in range(1, steps + 1):
            if is_hamilton_decomp(nexts):
                return nexts

            # pick a pair of colors; heuristic: include the worst color often
            cyc_counts = [cycle_count(nexts[c]) for c in range(3)]
            worst = max(range(3), key=lambda c: cyc_counts[c])
            other = rng.choice([c for c in range(3) if c != worst])
            c1, c2 = worst, other

            cycles = tau_cycles(nexts[c1], nexts[c2])
            verts = rng.choice(cycles)

            # try swap; accept if improves or with annealing probability
            old_heads1 = [nexts[c1][v] for v in verts]
            old_heads2 = [nexts[c2][v] for v in verts]

            swap_on_vertices(nexts, c1, c2, verts)
            ok, _ = verify_basic(m, nexts)
            if not ok:
                # revert
                for idx, v in enumerate(verts):
                    nexts[c1][v] = old_heads1[idx]
                    nexts[c2][v] = old_heads2[idx]
                continue

            new_obj = objective(nexts)
            accept = (new_obj <= cur_obj)
            if not accept and temp > 0:
                # simple Metropolis
                import math as _math
                if rng.random() < _math.exp(-(new_obj - cur_obj) / temp):
                    accept = True
            if accept:
                cur_obj = new_obj
                if cur_obj < best_obj:
                    best_obj = cur_obj
                    best = [arr[:] for arr in nexts]
                if verbose and step % 200 == 0:
                    print(f"  step {step}: objective={cur_obj}, cycles={ [cycle_count(nexts[c]) for c in range(3)] }")
            else:
                # revert
                for idx, v in enumerate(verts):
                    nexts[c1][v] = old_heads1[idx]
                    nexts[c2][v] = old_heads2[idx]

    return best if best is not None and is_hamilton_decomp(best) else best


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--restarts", type=int, default=50)
    ap.add_argument("--steps", type=int, default=5000)
    ap.add_argument("--temp", type=float, default=0.0, help="annealing temperature (0=greedy)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    sol = solve(args.m, args.seed, args.restarts, args.steps, args.temp, args.verbose)
    if sol is None:
        print("no solution produced")
        return

    ok, msg = verify_basic(args.m, sol)
    print("basic verify:", ok, msg)
    print("cycle counts:", [cycle_count(sol[c]) for c in range(3)])
    n = args.m ** 3
    print("signs:", [perm_sign(sol[c]) for c in range(3)], "product", perm_sign(sol[0]) * perm_sign(sol[1]) * perm_sign(sol[2]))
    if all(cycle_count(sol[c]) == 1 for c in range(3)):
        print("SUCCESS: Hamilton decomposition found.")
    else:
        print("Not Hamilton yet (best attempt). Increase restarts/steps or use temp>0.")


if __name__ == "__main__":
    main()
