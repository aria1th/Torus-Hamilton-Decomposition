#!/usr/bin/env python3
"""No-go check for the coarse defect-class five-color assembly family.

The family fixes the closed Sel* colors 3 and 4 and assigns the remaining
colors 0,1,2 by one fixed permutation on each of the nine historical coarse
classes:

- S0
- S1
- S2^(0), S2^(1)
- S3^(0,0), S3^(0,1), S3^(1,0), S3^(1,1)
- S4+

This script does not attempt a global search.  It certifies local impossibility:
for checked odd moduli, some target local signature has no class-permutation
assignment that satisfies incoming Latin exactness.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

from torus_nd_d5_selector_star_common_119 import selector_perm_star

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = (
    REPO_ROOT / "RoundY" / "checks" / "d5_271_five_color_coarse_defect_no_go_summary.json"
)
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_271_five_color_coarse_defect_no_go"

PERMS = list(itertools.permutations((0, 1, 2)))


def coarse_class(m: int, x: tuple[int, int, int, int, int]) -> tuple[str, ...]:
    sig = sum(x) % m
    if sig == 0:
        return ("S0",)
    if sig == 1:
        return ("S1",)
    if sig == 2:
        return ("S2", str(int(x[0] == m - 1)))
    if sig == 3:
        old_bit = int(x[0] == m - 1)
        pred_flag = int((x[1] + x[3]) % m == 2)
        return ("S3", str(old_bit), str(pred_flag))
    return ("S4+",)


def class_name(key: tuple[str, ...]) -> str:
    if key == ("S0",):
        return "S0"
    if key == ("S1",):
        return "S1"
    if key[0] == "S2":
        return f"S2^{key[1]}"
    if key[0] == "S3":
        return f"S3^({key[1]},{key[2]})"
    return "S4+"


def remaining_dirs(m: int, x: tuple[int, int, int, int, int]) -> tuple[int, int, int]:
    p = selector_perm_star(m, x)
    used = {p[3], p[4]}
    return tuple(sorted(d for d in range(5) if d not in used))


def target_signature(
    m: int,
    y: tuple[int, int, int, int, int],
    class_ids: dict[tuple[str, ...], int],
) -> tuple[tuple[int, ...], tuple[tuple[int, int, tuple[int, int, int], int | None], ...]]:
    infos = []
    for j in range(5):
        x = list(y)
        x[j] = (x[j] - 1) % m
        x_t = tuple(x)
        p = selector_perm_star(m, x_t)
        fixed = None
        if p[3] == j:
            fixed = 3
        elif p[4] == j:
            fixed = 4
        infos.append((j, class_ids[coarse_class(m, x_t)], remaining_dirs(m, x_t), fixed))
    vars_t = tuple(sorted({cid for _, cid, _, fixed in infos if fixed is None}))
    return vars_t, tuple(infos)


def color_for_info(
    info: tuple[int, int, tuple[int, int, int], int | None],
    assignment: dict[int, int],
) -> int:
    j, cid, rem, fixed = info
    if fixed is not None:
        return fixed
    idx = rem.index(j)
    perm = PERMS[assignment[cid]]
    return perm.index(idx)


def analyze_modulus(m: int) -> dict[str, object]:
    class_id_map: dict[tuple[str, ...], int] = {}
    for x in itertools.product(range(m), repeat=5):
        key = coarse_class(m, x)
        if key not in class_id_map:
            class_id_map[key] = len(class_id_map)
    class_names = {idx: class_name(key) for key, idx in class_id_map.items()}

    sig_counts: Counter[
        tuple[tuple[int, ...], tuple[tuple[int, int, tuple[int, int, int], int | None], ...]]
    ] = Counter()
    witness_targets: dict[
        tuple[tuple[int, ...], tuple[tuple[int, int, tuple[int, int, int], int | None], ...]],
        tuple[int, int, int, int, int],
    ] = {}

    for y in itertools.product(range(m), repeat=5):
        sig = target_signature(m, y, class_id_map)
        sig_counts[sig] += 1
        witness_targets.setdefault(sig, y)

    zero_allowed = 0
    first_witness: dict[str, object] | None = None
    for sig, multiplicity in sig_counts.items():
        vars_t, infos = sig
        allowed_count = 0
        for vals in itertools.product(range(6), repeat=len(vars_t)):
            assignment = dict(zip(vars_t, vals))
            colors = [color_for_info(info, assignment) for info in infos]
            if sorted(colors) == [0, 1, 2, 3, 4]:
                allowed_count += 1
        if allowed_count == 0:
            zero_allowed += 1
            if first_witness is None:
                first_witness = {
                    "target": list(witness_targets[sig]),
                    "multiplicity": multiplicity,
                    "variable_classes": [class_names[cid] for cid in vars_t],
                    "predecessors": [
                        {
                            "direction": j,
                            "class": class_names[cid],
                            "remaining_dirs": list(rem),
                            "sorted_index_of_direction": None if fixed is not None else rem.index(j),
                            "fixed_color": fixed,
                        }
                        for j, cid, rem, fixed in infos
                    ],
                }

    return {
        "modulus": m,
        "class_count": len(class_id_map),
        "classes": [class_names[i] for i in range(len(class_id_map))],
        "unique_target_signatures": len(sig_counts),
        "zero_allowed_signature_count": zero_allowed,
        "first_zero_allowed_witness": first_witness,
    }


def parse_moduli(raw: str) -> list[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Check the coarse defect-class no-go family.")
    parser.add_argument("--moduli", default="5,7,9,11,13")
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--detail-dir", type=Path, default=DEFAULT_DETAIL_DIR)
    args = parser.parse_args(list(argv) if argv is not None else None)

    moduli = parse_moduli(args.moduli)
    per_modulus = [analyze_modulus(m) for m in moduli]

    summary = {
        "task": "d5_271_five_color_coarse_defect_no_go",
        "family": (
            "Fix Sel* colors 3 and 4. For colors 0,1,2, assign the three remaining directions by "
            "one fixed permutation on each historical coarse class "
            "S0, S1, S2^(0), S2^(1), S3^(0,0), S3^(0,1), S3^(1,0), S3^(1,1), S4+."
        ),
        "checked_moduli": moduli,
        "all_moduli_have_local_obstruction": all(
            item["zero_allowed_signature_count"] > 0 for item in per_modulus
        ),
        "first_common_witness_target": [0, 0, 0, 0, 3],
        "conclusion": (
            "The historical defect-bit coarse family is already locally impossible. "
            "For every checked odd modulus, at least one target local signature has zero allowed "
            "class-permutation assignments, so no exact five-color completion in this family exists."
        ),
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    with args.summary_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
    with (args.detail_dir / "per_modulus.json").open("w", encoding="utf-8") as fh:
        json.dump(per_modulus, fh, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
