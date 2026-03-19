#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import itertools
import json
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from scipy.optimize import Bounds, LinearConstraint, milp


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO_ROOT / "RoundY" / "checks" / "d5_115_tiered_selector_summary.json"


def raw_row(m: int, x: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    s = sum(x) % m
    row: list[int] = []
    for c in range(5):
        if s == 0:
            row.append((c + 1) % 5)
        elif s == 1:
            row.append((c - 1) % 5)
        elif s == 2:
            row.append((c + 2) % 5 if x[(c + 1) % 5] == m - 1 else c)
        elif s == 3:
            eta = (((x[(c - 1) % 5] + x[(c + 2) % 5]) % m == 2) ^ (x[(c + 1) % 5] == m - 1))
            row.append((c - 2) % 5 if eta else c)
        else:
            row.append(c)
    return tuple(row)


def raw_edge_prefset(row: tuple[int, ...]) -> dict[int, set[int]]:
    out = {j: set() for j in range(5)}
    for c, j in enumerate(row):
        out[j].add(c)
    return out


def rotate_row(row: tuple[int, ...], k: int = 1) -> tuple[int, ...]:
    new = [None] * 5
    for c, j in enumerate(row):
        new[(c + k) % 5] = (j + k) % 5
    return tuple(new)


def build_type_data(m: int, s: int) -> dict[str, object]:
    coords = list(itertools.product(range(m), repeat=5))
    coord_to_id = {x: i for i, x in enumerate(coords)}
    rows = [raw_row(m, x) for x in coords]
    source_ids = [i for i, x in enumerate(coords) if sum(x) % m == s]
    target_ids = [i for i, x in enumerate(coords) if sum(x) % m == (s + 1) % m]

    type_ids: dict[tuple[int, ...], int] = {}
    types: list[tuple[int, ...]] = []
    weights: list[list[list[int]]] = []
    prefsets: list[dict[int, set[int]]] = []
    type_of_source: dict[int, int] = {}
    clean_agreement = 0

    for sid in source_ids:
        row = rows[sid]
        if row not in type_ids:
            type_ids[row] = len(types)
            types.append(row)
            weights.append([[0] * 5 for _ in range(5)])
            prefsets.append(raw_edge_prefset(row))
        tid = type_ids[row]
        type_of_source[sid] = tid
        pset = prefsets[tid]
        for j in range(5):
            for c in pset[j]:
                weights[tid][j][c] += 1
            if j in pset[j]:
                clean_agreement += 1

    constraints_counter: collections.Counter[tuple[int, ...]] = collections.Counter()
    for yid in target_ids:
        y = coords[yid]
        pred = []
        for j in range(5):
            x = list(y)
            x[j] = (x[j] - 1) % m
            pred.append(type_of_source[coord_to_id[tuple(x)]])
        constraints_counter[tuple(pred)] += 1

    return {
        "types": types,
        "type_ids": type_ids,
        "weights": np.array(weights),
        "constraints_counter": constraints_counter,
        "source_count": len(source_ids),
        "clean_agreement": clean_agreement,
    }


def solve_type_ilp(td: dict[str, object], maximize: bool = True, cyclic: bool = False):
    types = td["types"]
    type_ids = td["type_ids"]
    weights = td["weights"]
    constraints_counter = td["constraints_counter"]

    T = len(types)
    n = T * 25

    def idx(t: int, j: int, c: int) -> int:
        return t * 25 + j * 5 + c

    rows = []
    cols = []
    vals = []
    lb = []
    ub = []
    r = 0

    cvec = np.zeros(n)
    if maximize:
        for t in range(T):
            for j in range(5):
                for c in range(5):
                    cvec[idx(t, j, c)] = -weights[t, j, c]

    for t in range(T):
        for j in range(5):
            for c in range(5):
                rows.append(r)
                cols.append(idx(t, j, c))
                vals.append(1)
            lb.append(1)
            ub.append(1)
            r += 1
        for c in range(5):
            for j in range(5):
                rows.append(r)
                cols.append(idx(t, j, c))
                vals.append(1)
            lb.append(1)
            ub.append(1)
            r += 1

    for pred in constraints_counter:
        for c in range(5):
            for j, t in enumerate(pred):
                rows.append(r)
                cols.append(idx(t, j, c))
                vals.append(1)
            lb.append(1)
            ub.append(1)
            r += 1

    if cyclic:
        for row, t in type_ids.items():
            for k in range(1, 5):
                row2 = rotate_row(row, k)
                if row2 not in type_ids:
                    continue
                t2 = type_ids[row2]
                for j in range(5):
                    for c in range(5):
                        rows.extend([r, r])
                        cols.extend([idx(t2, (j + k) % 5, (c + k) % 5), idx(t, j, c)])
                        vals.extend([1, -1])
                        lb.append(0)
                        ub.append(0)
                        r += 1

    A = sp.coo_matrix((vals, (rows, cols)), shape=(r, n)).tocsr()
    lc = LinearConstraint(A, np.array(lb), np.array(ub))
    bnds = Bounds(np.zeros(n), np.ones(n))
    return milp(c=cvec, constraints=lc, bounds=bnds, integrality=np.ones(n), options={"disp": False})


def extract_assignment(res, td: dict[str, object]) -> dict[tuple[int, ...], tuple[int, ...]]:
    x = np.rint(res.x).astype(int)
    types = td["types"]
    T = len(types)
    out: dict[tuple[int, ...], tuple[int, ...]] = {}
    for t in range(T):
        q = []
        for j in range(5):
            cs = [c for c in range(5) if x[t * 25 + j * 5 + c]]
            q.append(cs[0])
        p = [None] * 5
        for j, c in enumerate(q):
            p[c] = j
        out[types[t]] = tuple(p)
    return out


def agreement_of_assignment(assign: dict[tuple[int, ...], tuple[int, ...]], td: dict[str, object]) -> int:
    type_ids = td["type_ids"]
    weights = td["weights"]
    total = 0
    for row, p in assign.items():
        t = type_ids[row]
        for c, j in enumerate(p):
            total += int(c in raw_edge_prefset(row)[j]) * weights[t, j, c]
    return int(total)


def check_assignment_on_m(assign: dict[tuple[int, ...], tuple[int, ...]], m: int, s: int) -> dict[str, object]:
    q = {
        row: tuple(next(c for c, jj in enumerate(p) if jj == j) for j in range(5))
        for row, p in assign.items()
    }

    type_of: dict[tuple[int, ...], tuple[int, ...]] = {}
    target_states = []
    clean = 0
    agreement = 0

    for x in itertools.product(range(m), repeat=5):
        row = raw_row(m, x)
        sx = sum(x) % m
        if sx == s:
            if row not in assign:
                return {"exact": False, "reason": "missing_row_type", "row": list(row)}
            type_of[x] = row
            pset = raw_edge_prefset(row)
            for j in range(5):
                if j in pset[j]:
                    clean += 1
        elif sx == (s + 1) % m:
            target_states.append(x)

    for x, row in type_of.items():
        p = assign[row]
        pset = raw_edge_prefset(row)
        for c, j in enumerate(p):
            agreement += int(c in pset[j])

    for y in target_states:
        colors = []
        for j in range(5):
            x = list(y)
            x[j] = (x[j] - 1) % m
            colors.append(q[type_of[tuple(x)]][j])
        if sorted(colors) != [0, 1, 2, 3, 4]:
            return {"exact": False, "reason": "target_constraint_fail", "target": list(y), "colors": colors}

    return {"exact": True, "agreement": agreement, "clean": clean}


def field(x: tuple[int, int, int, int, int], m: int, kind: str):
    row = raw_row(m, x)
    Z = tuple(i for i, v in enumerate(x) if v == 0)
    M = tuple(i for i, v in enumerate(x) if v == m - 1)
    B2 = tuple(i for i in range(5) if (x[(i - 1) % 5] + x[(i + 2) % 5]) % m == 2)
    B3 = tuple(i for i in range(5) if (x[(i - 1) % 5] + x[(i + 2) % 5]) % m == 3)
    fullpairs = tuple((x[(i - 1) % 5] + x[(i + 2) % 5]) % m for i in range(5))
    if kind == "row":
        return row
    if kind == "ZM":
        return (Z, M)
    if kind == "B23ZM":
        return (B2, B3, Z, M)
    if kind == "fullpairsZM":
        return (fullpairs, Z, M)
    raise ValueError(kind)


def transport_stats(m: int, target_slice: int, target_kind: str, pred_kind: str) -> dict[str, int]:
    predmap: collections.defaultdict[tuple[object, int], set[object]] = collections.defaultdict(set)
    states = set()
    for y in itertools.product(range(m), repeat=5):
        if sum(y) % m != target_slice:
            continue
        fy = field(y, m, target_kind)
        states.add(fy)
        for j in range(5):
            x = list(y)
            x[j] = (x[j] - 1) % m
            predmap[(fy, j)].add(field(tuple(x), m, pred_kind))
    nondet = sum(1 for v in predmap.values() if len(v) > 1)
    max_mult = max((len(v) for v in predmap.values()), default=0)
    return {"state_count": len(states), "nondet_pairs": nondet, "max_multiplicity": max_mult}


def compute_summary() -> dict[str, object]:
    out: dict[str, object] = {}

    pattern_only = {}
    assignments = {}
    for m in [5, 7, 9, 11]:
        pattern_only[str(m)] = {}
        assignments[m] = {}
        for s in [2, 3]:
            td = build_type_data(m, s)
            res_free = solve_type_ilp(td, maximize=True, cyclic=False)
            assign_free = extract_assignment(res_free, td)
            res_cyc = solve_type_ilp(td, maximize=True, cyclic=True)
            assign_cyc = extract_assignment(res_cyc, td)
            pattern_only[str(m)][str(s)] = {
                "type_count": len(td["types"]),
                "constraint_type_count": len(td["constraints_counter"]),
                "clean_agreement": int(td["clean_agreement"]),
                "free_opt_agreement": agreement_of_assignment(assign_free, td),
                "cyclic_opt_agreement": agreement_of_assignment(assign_cyc, td),
                "edge_count": 5 * int(td["source_count"]),
            }
            assignments[m][s] = assign_free
    out["pattern_only"] = pattern_only

    transfer = {}
    for test_m in [11, 13]:
        transfer[str(test_m)] = {}
        for s in [2, 3]:
            transfer[str(test_m)][str(s)] = check_assignment_on_m(assignments[9][s], test_m, s)
    out["transfer_from_m9"] = transfer

    out["m9_pattern_assignment"] = {
        "2": {str(k): list(v) for k, v in assignments[9][2].items()},
        "3": {str(k): list(v) for k, v in assignments[9][3].items()},
    }

    out["transport"] = {
        "m9": {
            "slice3_row_to_pred_row": transport_stats(9, 3, "row", "row"),
            "slice3_ZM_to_pred_row": transport_stats(9, 3, "ZM", "row"),
            "slice3_B23ZM_to_pred_row": transport_stats(9, 3, "B23ZM", "row"),
            "slice4_row_to_pred_row": transport_stats(9, 4, "row", "row"),
            "slice4_B23ZM_to_pred_row": transport_stats(9, 4, "B23ZM", "row"),
            "slice4_B23ZM_to_pred_B23ZM": transport_stats(9, 4, "B23ZM", "B23ZM"),
            "slice4_fullpairsZM_to_pred_B23ZM": transport_stats(9, 4, "fullpairsZM", "B23ZM"),
        },
        "m11": {
            "slice3_ZM_to_pred_row": transport_stats(11, 3, "ZM", "row"),
            "slice3_B23ZM_to_pred_row": transport_stats(11, 3, "B23ZM", "row"),
            "slice4_B23ZM_to_pred_row": transport_stats(11, 4, "B23ZM", "row"),
            "slice4_fullpairsZM_to_pred_B23ZM": transport_stats(11, 4, "fullpairsZM", "B23ZM"),
        },
    }
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the D5 115 tiered selector checks.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help=f"JSON output path (default: {DEFAULT_OUT})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out = compute_summary()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2))
    print(args.output)


if __name__ == "__main__":
    main()
