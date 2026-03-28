#!/usr/bin/env python3
"""Sanity checker for the graph-side split: G2 cyclic transport closes, while
mixed_008 does not solve G1 because pointwise outgoing exhaustiveness fails.

This script loads the surfaced mixed_008 witness from the 2026-03-21 bundle,
verifies exact cyclic conjugacy of the color maps on checked moduli, and records
an explicit outgoing-exhaustiveness counterexample for the naive cyclic family.
"""

from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

BUNDLE = Path(
    "/mnt/data/bundle197/roundy_d5_endpoint_return_model_bundle_20260321_update_197"
)
CODE_DIR = BUNDLE / "artifacts" / "d5_mixed_skew_odometer_normal_form_018" / "code"
WITNESS_REGISTRY = BUNDLE / "artifacts" / "d5_mixed_skew_odometer_normal_form_018" / "data" / "witness_registry.json"

sys.path.insert(0, str(CODE_DIR))
import torus_nd_d5_layer3_mode_switch_common as ms  # type: ignore  # noqa: E402


def rot_left(coords: Sequence[int], k: int) -> Tuple[int, ...]:
    k %= ms.DIM
    return tuple(coords[(i + k) % ms.DIM] for i in range(ms.DIM))


def index_rot_left(idx: int, m: int, k: int) -> int:
    return ms.encode(rot_left(ms.decode(idx, m), k), m)


def direction_of_step(src: Sequence[int], dst: Sequence[int], m: int) -> int:
    diffs = [((dst[i] - src[i]) % m) for i in range(ms.DIM)]
    ones = [i for i, d in enumerate(diffs) if d == 1]
    if len(ones) != 1 or any(d not in (0, 1) for d in diffs):
        raise ValueError(f"not a unit step: src={src}, dst={dst}, diffs={diffs}")
    return ones[0]


@dataclass
class PerModulusRow:
    m: int
    incoming_latin_all: bool
    cyclic_conjugacy_exact: bool
    explicit_vertex: List[int]
    explicit_dirs: List[int]
    explicit_outgoing_exhaustive: bool
    first_counterexample_vertex: List[int]
    first_counterexample_dirs: List[int]



def load_mixed_rule() -> ms.Rule:
    with WITNESS_REGISTRY.open() as f:
        registry = json.load(f)
    for row in registry["witnesses"]:
        if row["name"] == "mixed_008":
            return ms.Rule.from_payload(row["rule_payload"])
    raise KeyError("mixed_008 not found in witness registry")


RULE = load_mixed_rule()
SIGNATURE_TO_ID = ms.exact_signature_catalog([5, 7, 9, 11, 13])[
    "signature_to_id"
]
EXPLICIT_VERTEX = (0, 0, 0, 1, 2)


def verify_cyclic_conjugacy(pre: dict, nexts_all: List[List[int]], m: int) -> bool:
    coords = pre["coords"]
    for color in range(ms.DIM):
        row = nexts_all[color]
        for idx, vertex in enumerate(coords):
            xin = index_rot_left(idx, m, color)
            y0 = nexts_all[0][xin]
            y_expected = index_rot_left(y0, m, -color)
            if row[idx] != y_expected:
                return False
    return True



def directions_at_vertex(pre: dict, nexts_all: List[List[int]], vertex: Sequence[int], m: int) -> List[int]:
    idx = ms.encode(vertex, m)
    src = pre["coords"][idx]
    dirs: List[int] = []
    for color in range(ms.DIM):
        dst = pre["coords"][nexts_all[color][idx]]
        dirs.append(direction_of_step(src, dst, m))
    return dirs



def first_counterexample(pre: dict, nexts_all: List[List[int]], m: int) -> Tuple[List[int], List[int]]:
    for idx, src in enumerate(pre["coords"]):
        dirs = []
        for color in range(ms.DIM):
            dst = pre["coords"][nexts_all[color][idx]]
            dirs.append(direction_of_step(src, dst, m))
        if len(set(dirs)) != ms.DIM:
            return list(src), dirs
    raise RuntimeError("no counterexample found")



def analyse_modulus(m: int) -> PerModulusRow:
    pre = ms.precompute_m(m, SIGNATURE_TO_ID)
    anchors = ms.anchor_by_feature(pre, RULE)
    nexts_all = ms.nexts_all_for_rule(pre, anchors)

    incoming_latin = ms.incoming_latin_all(nexts_all)
    conjugacy = verify_cyclic_conjugacy(pre, nexts_all, m)

    explicit_dirs = directions_at_vertex(pre, nexts_all, EXPLICIT_VERTEX, m)
    explicit_outgoing_exhaustive = len(set(explicit_dirs)) == ms.DIM
    first_bad_vertex, first_bad_dirs = first_counterexample(pre, nexts_all, m)

    return PerModulusRow(
        m=m,
        incoming_latin_all=incoming_latin,
        cyclic_conjugacy_exact=conjugacy,
        explicit_vertex=list(EXPLICIT_VERTEX),
        explicit_dirs=explicit_dirs,
        explicit_outgoing_exhaustive=explicit_outgoing_exhaustive,
        first_counterexample_vertex=first_bad_vertex,
        first_counterexample_dirs=first_bad_dirs,
    )



def main() -> None:
    exact_m_values = [5, 7, 9, 11, 13]
    rows = [analyse_modulus(m) for m in exact_m_values]

    summary = {
        "task": "d5_234_G2_transport_checker",
        "witness": "mixed_008",
        "rule": RULE.payload(),
        "exact_m_values": exact_m_values,
        "all_incoming_latin": all(r.incoming_latin_all for r in rows),
        "all_cyclic_conjugacy_exact": all(r.cyclic_conjugacy_exact for r in rows),
        "explicit_vertex": list(EXPLICIT_VERTEX),
        "explicit_dirs_constant": len({tuple(r.explicit_dirs) for r in rows}) == 1,
        "explicit_dirs_value": rows[0].explicit_dirs if rows else None,
        "explicit_outgoing_exhaustive_all": all(r.explicit_outgoing_exhaustive for r in rows),
        "first_counterexample_constant": len({tuple(r.first_counterexample_vertex) for r in rows}) == 1,
        "first_counterexample_vertex": rows[0].first_counterexample_vertex if rows else None,
        "first_counterexample_dirs_constant": len({tuple(r.first_counterexample_dirs) for r in rows}) == 1,
        "first_counterexample_dirs": rows[0].first_counterexample_dirs if rows else None,
        "conclusion": (
            "The surfaced mixed_008 family is exactly color-conjugate across colors and each color map is Latin/permutative, "
            "but the naive cyclic package fails pointwise outgoing exhaustiveness at the explicit vertex (0,0,0,1,2), "
            "so G2 closes while G1 remains a genuine splice/compatibility problem."
        ),
    }

    summary_path = Path("/mnt/data/d5_234_G2_transport_checker_summary.json")
    with summary_path.open("w") as f:
        json.dump(summary, f, indent=2)

    table_path = Path("/mnt/data/d5_234_G2_transport_checker_table.csv")
    with table_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "m",
                "incoming_latin_all",
                "cyclic_conjugacy_exact",
                "explicit_vertex",
                "explicit_dirs",
                "explicit_outgoing_exhaustive",
                "first_counterexample_vertex",
                "first_counterexample_dirs",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.m,
                    int(row.incoming_latin_all),
                    int(row.cyclic_conjugacy_exact),
                    json.dumps(row.explicit_vertex),
                    json.dumps(row.explicit_dirs),
                    int(row.explicit_outgoing_exhaustive),
                    json.dumps(row.first_counterexample_vertex),
                    json.dumps(row.first_counterexample_dirs),
                ]
            )

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
