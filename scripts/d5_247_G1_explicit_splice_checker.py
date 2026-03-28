#!/usr/bin/env python3
"""Verify the explicit two-swap splice package closing G1.

The construction uses:
- the explicit baseline package B from d5_245,
- the surfaced mixed_008 color-4 branch from the bundle,
- two defect sets D1 and D2 cut out by the color-4 mixed branch.

On D1 we swap colors 1 and 4 relative to the baseline.
On D2 we swap colors 2 and 4 relative to the baseline.
Outside D1 ∪ D2 the package equals the baseline.

Outputs:
- /mnt/data/d5_247_G1_explicit_splice_summary.json
- /mnt/data/d5_247_G1_explicit_splice_table.csv
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set

BUNDLE = Path(
    "/mnt/data/bundle_extract/roundy_d5_endpoint_return_model_bundle_20260321_update_197"
)
CODE_DIR = BUNDLE / "artifacts" / "d5_mixed_skew_odometer_normal_form_018" / "code"
WITNESS_REGISTRY = (
    BUNDLE
    / "artifacts"
    / "d5_mixed_skew_odometer_normal_form_018"
    / "data"
    / "witness_registry.json"
)

sys.path.insert(0, str(CODE_DIR))
import torus_nd_d5_layer3_mode_switch_common as ms  # type: ignore  # noqa: E402
from torus_nd_d5_strict_palette_context_common import incoming_latin_all  # type: ignore  # noqa: E402

CHECKED_M_VALUES = [3, 5, 7, 9, 11, 13]


def load_mixed_rule() -> ms.Rule:
    registry = json.loads(WITNESS_REGISTRY.read_text())
    payload = next(row["rule_payload"] for row in registry["witnesses"] if row["name"] == "mixed_008")
    return ms.Rule.from_payload(payload)


RULE = load_mixed_rule()
SIGNATURE_TO_ID = ms.exact_signature_catalog([5, 7, 9, 11, 13])["signature_to_id"]


def pbit_from_flagmask(mask: int) -> int:
    # pred_sig1_wu2 is the third simple flag (bit index 2)
    return (mask >> 2) & 1


def coarse_class_of_feature(row: Sequence[int]) -> str:
    layer, s2, s3, flag_mask, _sig = row
    if layer == 0:
        return "L0"
    if layer == 1:
        return "L1"
    if layer == 4:
        return "L4+"
    if layer == 2:
        return f"L2s{s2}"
    return f"L3s3{s3}p{pbit_from_flagmask(int(flag_mask))}"


BASELINE_CLASS_ANCHOR: Dict[str, int] = {
    "L0": 1,
    "L1": 4,
    "L4+": 0,
    "L2s0": 0,
    "L2s1": 0,
    "L3s30p0": 0,
    "L3s30p1": 0,
    "L3s31p0": 0,
    "L3s31p1": 0,
}


def baseline_dirs(pre: Mapping[str, object], color: int) -> List[int]:
    out = [0] * int(pre["n"])
    for idx, fid in enumerate(pre["feature_ids_by_color"][color]):
        cls = coarse_class_of_feature(pre["feature_rows"][fid])
        out[idx] = (BASELINE_CLASS_ANCHOR[cls] + color) % ms.DIM
    return out


def mixed_color4_dirs(pre: Mapping[str, object]) -> List[int]:
    anchors = ms.anchor_by_feature(pre, RULE)
    out = [0] * int(pre["n"])
    for idx, fid in enumerate(pre["feature_ids_by_color"][4]):
        out[idx] = (int(anchors[fid]) + 4) % ms.DIM
    return out


def d1_indices(pre: Mapping[str, object]) -> Set[int]:
    out = set()
    for idx, fid in enumerate(pre["feature_ids_by_color"][4]):
        if coarse_class_of_feature(pre["feature_rows"][fid]) == "L2s1":
            out.add(int(idx))
    return out


def d2_indices(pre: Mapping[str, object]) -> Set[int]:
    out = set()
    for idx, fid in enumerate(pre["feature_ids_by_color"][4]):
        if coarse_class_of_feature(pre["feature_rows"][fid]) in ("L3s30p1", "L3s31p0"):
            out.add(int(idx))
    return out


def coordinate_d1_indices(pre: Mapping[str, object]) -> Set[int]:
    m = int(pre["m"])
    out = set()
    for idx, coords in enumerate(pre["coords"]):
        if sum(coords) % m == 2 and coords[0] == m - 1:
            out.add(int(idx))
    return out


def coordinate_d2_indices(pre: Mapping[str, object]) -> Set[int]:
    m = int(pre["m"])
    if m <= 3:
        return set()
    out = set()
    for idx, coords in enumerate(pre["coords"]):
        total = sum(coords) % m
        if total != 3:
            continue
        q = coords[0]
        wu = (coords[1] + coords[3]) % m
        if (q != m - 1 and wu == 2) or (q == m - 1 and wu != 2):
            out.add(int(idx))
    return out


def image_set(pre: Mapping[str, object], indices: Iterable[int], direction: int) -> Set[int]:
    step = pre["step_by_dir"][direction]
    return {int(step[idx]) for idx in indices}


def build_package(pre: Mapping[str, object]) -> Dict[str, object]:
    n = int(pre["n"])
    B = {color: baseline_dirs(pre, color) for color in range(ms.DIM)}
    mixed4 = mixed_color4_dirs(pre)
    D1 = d1_indices(pre)
    D2 = d2_indices(pre)

    dirs = {color: B[color][:] for color in range(ms.DIM)}
    for idx in D1:
        dirs[4][idx] = B[1][idx]
        dirs[1][idx] = B[4][idx]
    for idx in D2:
        dirs[4][idx] = B[2][idx]
        dirs[2][idx] = B[4][idx]

    nexts = []
    for color in range(ms.DIM):
        row = [0] * n
        for idx in range(n):
            row[idx] = int(pre["step_by_dir"][dirs[color][idx]][idx])
        nexts.append(row)

    outgoing_bad = 0
    for idx in range(n):
        if len({dirs[color][idx] for color in range(ms.DIM)}) != ms.DIM:
            outgoing_bad += 1

    return {
        "B_dirs": B,
        "mixed4_dirs": mixed4,
        "dirs": dirs,
        "D1": D1,
        "D2": D2,
        "outgoing_bad_vertex_count": outgoing_bad,
        "incoming_latin_all": bool(incoming_latin_all(nexts)),
        "colorwise_permutation": [len(set(row)) == n for row in nexts],
        "g4_matches_mixed_008": all(dirs[4][idx] == mixed4[idx] for idx in range(n)),
    }


def row_for_m(m: int) -> Dict[str, object]:
    pre = ms.precompute_m(m, SIGNATURE_TO_ID)
    pkg = build_package(pre)
    D1_surface = pkg["D1"]
    D2_surface = pkg["D2"]
    D1_coord = coordinate_d1_indices(pre)
    D2_coord = coordinate_d2_indices(pre)
    B = pkg["B_dirs"]

    return {
        "m": m,
        "n": int(pre["n"]),
        "D1_count": len(D1_surface),
        "D2_count": len(D2_surface),
        "surface_D1_equals_coordinate_D1": D1_surface == D1_coord,
        "surface_D2_equals_coordinate_D2": D2_surface == D2_coord,
        "D1_image_e1_equals_e4": image_set(pre, D1_surface, 1) == image_set(pre, D1_surface, 4),
        "D2_image_e2_equals_e4": image_set(pre, D2_surface, 2) == image_set(pre, D2_surface, 4),
        "outgoing_bad_vertex_count": int(pkg["outgoing_bad_vertex_count"]),
        "incoming_latin_all": bool(pkg["incoming_latin_all"]),
        "colorwise_permutation_all": bool(all(pkg["colorwise_permutation"])),
        "g4_matches_mixed_008": bool(pkg["g4_matches_mixed_008"]),
        "baseline_color4_diff_count": int(sum(B[4][idx] != pkg["mixed4_dirs"][idx] for idx in range(int(pre["n"])))),
    }


def main() -> None:
    per_m = {str(m): row_for_m(m) for m in CHECKED_M_VALUES}
    summary = {
        "task": "d5_247_G1_explicit_splice_checker",
        "checked_m_values": CHECKED_M_VALUES,
        "construction": {
            "baseline": "explicit layer baseline from d5_245",
            "color4": "exact mixed_008 branch",
            "D1": "color-4 class L2s1 = {sum=2, x0=m-1}",
            "D2": "color-4 classes L3s30p1 or L3s31p0; for m>3 this is {sum=3 and ((x0!=m-1 & x1+x3=2) or (x0=m-1 & x1+x3!=2))}; for m=3 it is empty",
            "splice": "swap colors 1 and 4 on D1, swap colors 2 and 4 on D2, leave colors 0 and 3 unchanged",
        },
        "per_m": per_m,
        "all_checked_ok": all(
            row["surface_D1_equals_coordinate_D1"]
            and row["surface_D2_equals_coordinate_D2"]
            and row["D1_image_e1_equals_e4"]
            and row["D2_image_e2_equals_e4"]
            and row["outgoing_bad_vertex_count"] == 0
            and row["incoming_latin_all"]
            and row["colorwise_permutation_all"]
            and row["g4_matches_mixed_008"]
            for row in per_m.values()
        ),
        "conclusion": (
            "For every checked odd modulus m>2, the explicit two-swap splice package is outgoing-exhaustive, "
            "colorwise Latin, and agrees exactly with mixed_008 on color 4. "
            "The color-4 defect sets are the surface classes D1=L2s1 and D2=L3s30p1 ∪ L3s31p0, "
            "and the required image-preserving identities are B1(D1)=B4(D1) and B2(D2)=B4(D2)."
        ),
    }

    summary_path = Path("/mnt/data/d5_247_G1_explicit_splice_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True))

    table_rows: List[Dict[str, object]] = []
    for m_key, row in per_m.items():
        table_rows.append(
            {
                "m": int(m_key),
                "n": int(row["n"]),
                "D1_count": int(row["D1_count"]),
                "D2_count": int(row["D2_count"]),
                "surface_D1_equals_coordinate_D1": int(bool(row["surface_D1_equals_coordinate_D1"])),
                "surface_D2_equals_coordinate_D2": int(bool(row["surface_D2_equals_coordinate_D2"])),
                "D1_image_e1_equals_e4": int(bool(row["D1_image_e1_equals_e4"])),
                "D2_image_e2_equals_e4": int(bool(row["D2_image_e2_equals_e4"])),
                "outgoing_bad_vertex_count": int(row["outgoing_bad_vertex_count"]),
                "incoming_latin_all": int(bool(row["incoming_latin_all"])),
                "colorwise_permutation_all": int(bool(row["colorwise_permutation_all"])),
                "g4_matches_mixed_008": int(bool(row["g4_matches_mixed_008"])),
                "baseline_color4_diff_count": int(row["baseline_color4_diff_count"]),
            }
        )

    table_path = Path("/mnt/data/d5_247_G1_explicit_splice_table.csv")
    with table_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "m",
                "n",
                "D1_count",
                "D2_count",
                "surface_D1_equals_coordinate_D1",
                "surface_D2_equals_coordinate_D2",
                "D1_image_e1_equals_e4",
                "D2_image_e2_equals_e4",
                "outgoing_bad_vertex_count",
                "incoming_latin_all",
                "colorwise_permutation_all",
                "g4_matches_mixed_008",
                "baseline_color4_diff_count",
            ],
        )
        writer.writeheader()
        writer.writerows(table_rows)

    print(summary_path)
    print(table_path)


if __name__ == "__main__":
    main()
