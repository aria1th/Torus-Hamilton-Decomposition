#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO_ROOT / "RoundY" / "checks" / "d5_115_slice4_transport_search.json"


def pred_b23zm(x: tuple[int, int, int, int, int], m: int):
    z = tuple(i for i, v in enumerate(x) if v == 0)
    mset = tuple(i for i, v in enumerate(x) if v == m - 1)
    b2 = tuple(i for i in range(5) if (x[(i - 1) % 5] + x[(i + 2) % 5]) % m == 2)
    b3 = tuple(i for i in range(5) if (x[(i - 1) % 5] + x[(i + 2) % 5]) % m == 3)
    return (b2, b3, z, mset)


def subset_field(x: tuple[int, int, int, int, int], m: int, subset: tuple[int, ...]):
    z = tuple(i for i, v in enumerate(x) if v == 0)
    mset = tuple(i for i, v in enumerate(x) if v == m - 1)
    blocks = tuple(
        tuple(i for i in range(5) if (x[(i - 1) % 5] + x[(i + 2) % 5]) % m == k)
        for k in subset
    )
    return blocks + (z, mset)


def fullpairszm(x: tuple[int, int, int, int, int], m: int):
    z = tuple(i for i, v in enumerate(x) if v == 0)
    mset = tuple(i for i, v in enumerate(x) if v == m - 1)
    fullpairs = tuple((x[(i - 1) % 5] + x[(i + 2) % 5]) % m for i in range(5))
    return (fullpairs, z, mset)


def rotate_fullpairs_state(state, k: int):
    fullpairs, z, mset = state
    fp = tuple(fullpairs[(i - k) % 5] for i in range(5))
    z2 = tuple(sorted((i + k) % 5 for i in z))
    m2 = tuple(sorted((i + k) % 5 for i in mset))
    return (fp, z2, m2)


def cyclic_orbit_field(x: tuple[int, int, int, int, int], m: int):
    state = fullpairszm(x, m)
    return min(rotate_fullpairs_state(state, k) for k in range(5))


def transport_stats_subset(m: int, subset: tuple[int, ...]) -> dict[str, int]:
    predmap: defaultdict[tuple[object, int], set[object]] = defaultdict(set)
    states = set()
    for y in itertools.product(range(m), repeat=5):
        if sum(y) % m != 4:
            continue
        fy = subset_field(y, m, subset)
        states.add(fy)
        for j in range(5):
            x = list(y)
            x[j] = (x[j] - 1) % m
            predmap[(fy, j)].add(pred_b23zm(tuple(x), m))
    nondet = sum(1 for v in predmap.values() if len(v) > 1)
    max_mult = max((len(v) for v in predmap.values()), default=0)
    return {"state_count": len(states), "nondet_pairs": nondet, "max_multiplicity": max_mult}


def transport_stats_field(m: int, field_kind: str) -> dict[str, int]:
    predmap: defaultdict[tuple[object, int], set[object]] = defaultdict(set)
    states = set()
    for y in itertools.product(range(m), repeat=5):
        if sum(y) % m != 4:
            continue
        if field_kind == "B23ZM":
            fy = pred_b23zm(y, m)
        elif field_kind == "fullpairsZM":
            fy = fullpairszm(y, m)
        elif field_kind == "cyclic_fullpairsZM":
            fy = cyclic_orbit_field(y, m)
        else:
            raise ValueError(field_kind)
        states.add(fy)
        for j in range(5):
            x = list(y)
            x[j] = (x[j] - 1) % m
            predmap[(fy, j)].add(pred_b23zm(tuple(x), m))
    nondet = sum(1 for v in predmap.values() if len(v) > 1)
    max_mult = max((len(v) for v in predmap.values()), default=0)
    return {"state_count": len(states), "nondet_pairs": nondet, "max_multiplicity": max_mult}


def compute_summary() -> dict[str, object]:
    k_pool = (0, 1, 2, 3, 4, 5)
    subset_results = []
    exact_subsets = []
    for r in range(1, len(k_pool) + 1):
        for subset in itertools.combinations(k_pool, r):
            m9 = transport_stats_subset(9, subset)
            m11 = transport_stats_subset(11, subset)
            entry = {
                "subset": list(subset),
                "m9": m9,
                "m11": m11,
                "total_nondet_pairs": m9["nondet_pairs"] + m11["nondet_pairs"],
                "total_state_count": m9["state_count"] + m11["state_count"],
            }
            subset_results.append(entry)
            if m9["nondet_pairs"] == 0 and m11["nondet_pairs"] == 0:
                exact_subsets.append(list(subset))

    subset_results.sort(
        key=lambda item: (
            item["total_nondet_pairs"],
            item["total_state_count"],
            len(item["subset"]),
            item["subset"],
        )
    )

    baselines = {
        "B23ZM": {
            "m9": transport_stats_field(9, "B23ZM"),
            "m11": transport_stats_field(11, "B23ZM"),
        },
        "fullpairsZM": {
            "m9": transport_stats_field(9, "fullpairsZM"),
            "m11": transport_stats_field(11, "fullpairsZM"),
        },
        "cyclic_fullpairsZM": {
            "m9": transport_stats_field(9, "cyclic_fullpairsZM"),
            "m11": transport_stats_field(11, "cyclic_fullpairsZM"),
        },
    }

    distinguished = {}
    for subset in ([2, 3], [2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5]):
        key = ",".join(map(str, subset))
        distinguished[key] = next(item for item in subset_results if item["subset"] == subset)

    return {
        "candidate_family": {
            "target_slice": 4,
            "pred_field": "B23ZM",
            "field_shape": "(B_k for k in subset, Z, M)",
            "k_pool": list(k_pool),
            "moduli_checked": [9, 11],
        },
        "exact_subsets": exact_subsets,
        "best_candidates": subset_results[:20],
        "distinguished_candidates": distinguished,
        "baselines": baselines,
        "counts": {
            "subset_count": len(subset_results),
            "exact_subset_count": len(exact_subsets),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search slice-4 transport candidates for D5 note 115.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help=f"JSON output path (default: {DEFAULT_OUT})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = compute_summary()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2))
    print(args.output)


if __name__ == "__main__":
    main()
