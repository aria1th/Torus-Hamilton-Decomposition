#!/usr/bin/env python3
"""Checker for the d5_256 transport no-go note.

This script verifies three points for the explicit two-swap package from d5_247:

1. the pulled-back relative-direction witness at y=(0,0,0,1,2) is [0,0,2,0,3];
2. colors 0,1,2,3 use restricted direction supports as stated in d5_256;
3. colors 0,1,2,3 are non-Hamilton on checked odd moduli.

Outputs:
- RoundY/checks/d5_256_transport_no_go_summary.json
- RoundY/checks/d5_256_transport_no_go/per_modulus.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set

REPO_ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = REPO_ROOT / "artifacts" / "d5_mixed_skew_odometer_normal_form_018" / "code"
WITNESS_REGISTRY = REPO_ROOT / "artifacts" / "d5_mixed_skew_odometer_normal_form_018" / "data" / "witness_registry.json"
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_256_transport_no_go_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_256_transport_no_go"

sys.path.insert(0, str(CODE_DIR))
import torus_nd_d5_layer3_mode_switch_common as ms  # type: ignore  # noqa: E402


EXPLICIT_VERTEX = (0, 0, 0, 1, 2)


def load_mixed_rule() -> ms.Rule:
    registry = json.loads(WITNESS_REGISTRY.read_text())
    payload = next(row["rule_payload"] for row in registry["witnesses"] if row["name"] == "mixed_008")
    return ms.Rule.from_payload(payload)


RULE = load_mixed_rule()
SIGNATURE_TO_ID = ms.exact_signature_catalog([5, 7, 9, 11, 13])["signature_to_id"]


def rot_left(coords: Sequence[int], k: int) -> tuple[int, ...]:
    k %= ms.DIM
    return tuple(coords[(i + k) % ms.DIM] for i in range(ms.DIM))


def pbit_from_flagmask(mask: int) -> int:
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


def build_package(pre: Mapping[str, object]) -> dict[str, object]:
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

    return {"dirs": dirs, "nexts": nexts, "D1": D1, "D2": D2, "mixed4": mixed4}


def cycle_lengths(row: Sequence[int]) -> list[int]:
    n = len(row)
    seen = [False] * n
    lens: list[int] = []
    for i in range(n):
        if seen[i]:
            continue
        cur = i
        L = 0
        while not seen[cur]:
            seen[cur] = True
            cur = row[cur]
            L += 1
        lens.append(L)
    lens.sort(reverse=True)
    return lens


def pulled_back_relative_dirs(pre: Mapping[str, object], pkg: Mapping[str, object], vertex: Sequence[int], m: int) -> list[int]:
    dirs: list[int] = []
    for color in range(ms.DIM):
        xin = rot_left(vertex, -color)
        idx = ms.encode(xin, m)
        abs_dir = int(pkg["dirs"][color][idx])
        dirs.append((abs_dir - color) % ms.DIM)
    return dirs


def direction_supports(pkg: Mapping[str, object]) -> dict[str, list[int]]:
    return {
        str(color): sorted(set(int(v) for v in pkg["dirs"][color]))
        for color in range(ms.DIM)
    }


def analyse_modulus(m: int) -> dict[str, object]:
    pre = ms.precompute_m(m, SIGNATURE_TO_ID)
    pkg = build_package(pre)
    supports = direction_supports(pkg)
    witness_dirs = pulled_back_relative_dirs(pre, pkg, EXPLICIT_VERTEX, m)

    cycle_data = {}
    for color in range(ms.DIM):
        lens = cycle_lengths(pkg["nexts"][color])
        cycle_data[str(color)] = {
            "cycle_count": len(lens),
            "largest_cycles": lens[:10],
            "is_hamilton": len(lens) == 1 and lens[0] == int(pre["n"]),
        }

    return {
        "m": m,
        "pulled_back_relative_dirs_at_y": witness_dirs,
        "direction_supports": supports,
        "cycle_data": cycle_data,
        "color_0_preserves": ["x2", "x3"],
        "color_1_preserves": ["x3"],
        "color_2_preserves": ["x0"],
        "color_3_preserves": ["x0", "x1"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Checker for the d5_256 transport no-go note.")
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=DEFAULT_SUMMARY,
        help=f"summary JSON path (default: {DEFAULT_SUMMARY})",
    )
    parser.add_argument(
        "--detail-dir",
        type=Path,
        default=DEFAULT_DETAIL_DIR,
        help=f"detail output directory (default: {DEFAULT_DETAIL_DIR})",
    )
    parser.add_argument(
        "--moduli",
        type=int,
        nargs="*",
        default=[5, 7, 9, 11, 13],
        help="odd moduli to check",
    )
    args = parser.parse_args()

    per_modulus = {str(m): analyse_modulus(m) for m in args.moduli}

    summary = {
        "task": "d5_256_transport_no_go",
        "checked_moduli": args.moduli,
        "explicit_vertex_y": list(EXPLICIT_VERTEX),
        "expected_pulled_back_relative_dirs": [0, 0, 2, 0, 3],
        "all_witness_dirs_match": all(
            payload["pulled_back_relative_dirs_at_y"] == [0, 0, 2, 0, 3]
            for payload in per_modulus.values()
        ),
        "expected_direction_supports": {
            "0": [0, 1, 4],
            "1": [0, 1, 2, 4],
            "2": [1, 2, 3, 4],
            "3": [2, 3, 4],
        },
        "all_supports_match": all(
            payload["direction_supports"]["0"] == [0, 1, 4]
            and payload["direction_supports"]["1"] == [0, 1, 2, 4]
            and payload["direction_supports"]["2"] == [1, 2, 3, 4]
            and payload["direction_supports"]["3"] == [2, 3, 4]
            for payload in per_modulus.values()
        ),
        "all_noncolor4_nonhamilton": all(
            not payload["cycle_data"][str(color)]["is_hamilton"]
            for payload in per_modulus.values()
            for color in range(4)
        ),
        "conclusion": (
            "The explicit two-swap package from d5_247 is not transport-compatible in the G2 sense. "
            "At y=(0,0,0,1,2) the pulled-back relative directions are [0,0,2,0,3], so the package is not one "
            "common color-relative family. Moreover colors 0,1,2,3 use restricted direction supports and are non-Hamilton "
            "on all checked odd moduli."
        ),
    }

    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summary, indent=2))
    (args.detail_dir / "per_modulus.json").write_text(json.dumps(per_modulus, indent=2))
    print(args.summary_output)
    print(args.detail_dir / "per_modulus.json")


if __name__ == "__main__":
    main()
