#!/usr/bin/env python3
"""Verify the UNSAT obstruction for the rotational Boolean-layer d=5 model at m=5.

Model:
- layer 0 fixed to +e_{c+1}
- layers 1,2,3 depend only on the Boolean zero-pattern B in {0,1}^5
- rotational covariance across colors
- target first-return displacement is the 3-carry odometer target

Main conclusion:
The layer-1 rule is forced to be the default output 0 on every encountered state,
so the triple-carry start x=(3,4,4,4,0) cannot be realized.
"""
from itertools import product, permutations
import json
from pathlib import Path

m = 5
patterns = [tuple(bits) for bits in product([0, 1], repeat=5)]


def shift(B, s):
    return tuple(B[(i + s) % 5] for i in range(5))


def step(x, d):
    y = list(x)
    y[d] = (y[d] + 1) % m
    return tuple(y)


def target_multiset(x):
    q, w, v = x[1], x[2], x[3]
    if q != 4:
        return []
    if w != 4:
        return [2]
    if v != 4:
        return [2, 3]
    return [2, 3, 4]


# Orbit decomposition under cyclic shift.
seen = set()
orbits = []
for B in patterns:
    if B in seen:
        continue
    orb = []
    cur = B
    while cur not in orb:
        orb.append(cur)
        cur = shift(cur, 1)
    for C in orb:
        seen.add(C)
    orbits.append(orb)
orbits = sorted(orbits, key=lambda o: (len(o), o[0]))

# All orbit assignments induced by a local permutation.
orbit_assignments = []
for orb in orbits:
    if len(orb) == 1:
        orbit_assignments.append([[v] for v in range(5)])
        continue
    assigns = []
    for pi in permutations(range(5)):
        g = [None] * 5
        for s in range(5):
            c = (-s) % 5
            g[s] = (pi[c] - c) % 5
        if g not in assigns:
            assigns.append(g)
    orbit_assignments.append(assigns)

# Starts x in P0 for color 0.
starts = []
for x1, x2, x3, x4 in product(range(m), repeat=4):
    x0 = (-x1 - x2 - x3 - x4) % m
    x = (x0, x1, x2, x3, x4)
    y1 = step(x, 1)
    starts.append(
        {
            "start": x,
            "after0": y1,
            "B1": tuple(1 if t == 0 else 0 for t in y1),
            "target": tuple(target_multiset(x)),
        }
    )

encountered = {}
for item in starts:
    encountered.setdefault(item["B1"], []).append(item)

# Check admissible layer-1 assignments on each orbit:
# - if B1[1] = 0, that state is non-carry and must output 0;
# - if B1[1] = 1, the target only ever allows 0 or 2 on layer 1.
orbit_summary = []
for oi, orb in enumerate(orbits):
    admissible = []
    for g in orbit_assignments[oi]:
        ok = True
        for s, B in enumerate(orb):
            items = encountered.get(B, [])
            if not items:
                continue
            if B[1] == 0:
                if g[s] != 0:
                    ok = False
                    break
            else:
                if g[s] not in (0, 2):
                    ok = False
                    break
        if ok:
            admissible.append(g)
    orbit_summary.append(
        {
            "orbit_index": oi,
            "orbit_size": len(orb),
            "patterns": [list(B) for B in orb],
            "encountered": any(B in encountered for B in orb),
            "admissible_assignments": admissible,
        }
    )

forced_zero = True
for row in orbit_summary:
    if not row["encountered"]:
        continue
    adm = row["admissible_assignments"]
    if len(adm) != 1:
        forced_zero = False
        break
    if any(value != 0 for value in adm[0]):
        forced_zero = False
        break

triple_carry_start = (3, 4, 4, 4, 0)
payload = {
    "forced_zero_on_encountered_orbits": forced_zero,
    "orbit_summary": orbit_summary,
    "triple_carry_start": {
        "start": triple_carry_start,
        "after_layer0": step(triple_carry_start, 1),
        "target_extra_directions": [2, 3, 4],
        "reason_unsat": "layer 1 is forced to default, leaving only layers 2 and 3 for three carries",
    },
}
print(json.dumps(payload, indent=2))
Path("/mnt/data/d5_boolean_model_unsat_check_output.json").write_text(json.dumps(payload, indent=2))
