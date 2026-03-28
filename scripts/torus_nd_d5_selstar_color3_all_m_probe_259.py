#!/usr/bin/env python3
"""Strengthen the Sel* color-3 theorem target from odd m to all m > 2.

This script bundles three levels of evidence:

1. section-model evidence on S_m = {x2 = m - 2} for a broad checked range;
2. direct first-return cycle counts on P0 for a medium checked range;
3. direct full-torus cycle counts for small moduli.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from torus_nd_d5_selector_star_common_119 import build_R_data, selector_perm_star
from torus_nd_d5_selstar_color3_section_stitch_probe_258 import analyse_modulus


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_259_selstar_color3_all_m_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_259_selstar_color3_all_m"


def cycle_counts_from_perm(perm) -> Counter[int]:
    n = len(perm)
    seen = [False] * n
    counts: Counter[int] = Counter()
    for i in range(n):
        if seen[i]:
            continue
        cur = i
        length = 0
        while not seen[cur]:
            seen[cur] = True
            cur = int(perm[cur])
            length += 1
        counts[length] += 1
    return counts


def all_states(m: int):
    for x0 in range(m):
        for x1 in range(m):
            for x2 in range(m):
                for x3 in range(m):
                    for x4 in range(m):
                        yield (x0, x1, x2, x3, x4)


def build_full_torus_perm(m: int, color: int):
    pts = list(all_states(m))
    id_map = {point: idx for idx, point in enumerate(pts)}
    perm = [0] * len(pts)
    for idx, point in enumerate(pts):
        selector = selector_perm_star(m, point)
        direction = selector[color]
        image = list(point)
        image[direction] = (image[direction] + 1) % m
        perm[idx] = id_map[tuple(image)]
    return perm


def main() -> None:
    parser = argparse.ArgumentParser(description="All-m probe for Sel* color-3.")
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
        "--section-moduli",
        type=int,
        nargs="*",
        default=list(range(2, 24)),
        help="moduli for section-model checks",
    )
    parser.add_argument(
        "--return-moduli",
        type=int,
        nargs="*",
        default=list(range(2, 15)),
        help="moduli for direct P0 first-return cycle counts",
    )
    parser.add_argument(
        "--full-moduli",
        type=int,
        nargs="*",
        default=list(range(2, 11)),
        help="moduli for direct full-torus cycle counts",
    )
    args = parser.parse_args()

    section_results = {str(m): analyse_modulus(m) for m in args.section_moduli}

    return_results = {}
    for m in args.return_moduli:
        _pts, perm, _images4 = build_R_data(m, 3, selector_perm_star)
        counts = cycle_counts_from_perm(perm)
        return_results[str(m)] = {
            "R_cycle_counts": {str(k): v for k, v in sorted(counts.items())},
            "R_is_single_cycle": counts == Counter({m**4: 1}),
        }

    full_results = {}
    for m in args.full_moduli:
        perm = build_full_torus_perm(m, 3)
        counts = cycle_counts_from_perm(perm)
        full_results[str(m)] = {
            "F_cycle_counts": {str(k): v for k, v in sorted(counts.items())},
            "F_is_single_cycle": counts == Counter({m**5: 1}),
        }

    summary = {
        "task": "d5_259_selstar_color3_all_m_probe",
        "selector": "Sel*",
        "color": 3,
        "candidate_theorem": "For every m > 2, the Sel* color-3 map is Hamilton on the full torus.",
        "section_moduli": args.section_moduli,
        "return_moduli": args.return_moduli,
        "full_moduli": args.full_moduli,
        "all_section_formulas_hold_for_m_gt_2_in_checked_range": all(
            int(m) > 2 and payload["section_formula_verified"] or int(m) == 2
            for m, payload in section_results.items()
        ),
        "all_section_cycles_hold_for_m_gt_2_in_checked_range": all(
            int(m) > 2 and payload["section_is_single_cycle"] or int(m) == 2
            for m, payload in section_results.items()
        ),
        "all_R_cycles_hold_for_m_gt_2_in_checked_range": all(
            int(m) > 2 and payload["R_is_single_cycle"] or int(m) == 2
            for m, payload in return_results.items()
        ),
        "all_F_cycles_hold_for_m_gt_2_in_checked_range": all(
            int(m) > 2 and payload["F_is_single_cycle"] or int(m) == 2
            for m, payload in full_results.items()
        ),
        "m2_exception": {
            "section_single_cycle": section_results.get("2", {}).get("section_is_single_cycle"),
            "R_single_cycle": return_results.get("2", {}).get("R_is_single_cycle"),
            "F_single_cycle": full_results.get("2", {}).get("F_is_single_cycle"),
        },
    }

    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)

    with args.summary_output.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
        fh.write("\n")

    with (args.detail_dir / "section_per_modulus.json").open("w", encoding="utf-8") as fh:
        json.dump(section_results, fh, indent=2, sort_keys=True)
        fh.write("\n")

    with (args.detail_dir / "return_per_modulus.json").open("w", encoding="utf-8") as fh:
        json.dump(return_results, fh, indent=2, sort_keys=True)
        fh.write("\n")

    with (args.detail_dir / "full_per_modulus.json").open("w", encoding="utf-8") as fh:
        json.dump(full_results, fh, indent=2, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
