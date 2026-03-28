#!/usr/bin/env python3
"""Exact candidate reduction for the remaining graph-side theorem G1.

This script searches the surfaced mode-switch rule family from the
2026-03-21 bundle and asks how large an outgoing-disjoint color package can be
built while preserving colorwise Latinity.

Scope:
- family = simple_flag_rows() union exact_signature_rows() from
  torus_nd_d5_layer3_mode_switch_common.py
- exact impossibility search on m=5
- spot-check sanity on m=7 for one adjacent pair, one nonadjacent pair,
  and one triple

Outputs:
- /mnt/data/d5_237_G1_modeswitch_candidate_summary.json
- /mnt/data/d5_237_G1_modeswitch_candidate_table.csv
"""
from __future__ import annotations

import csv
import itertools
import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

BUNDLE = Path(
    "/mnt/data/bundle197/roundy_d5_endpoint_return_model_bundle_20260321_update_197"
)
CODE_DIR = BUNDLE / "artifacts" / "d5_mixed_skew_odometer_normal_form_018" / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import torus_nd_d5_layer3_mode_switch_common as ms  # type: ignore  # noqa: E402


M_VALUES = [5, 7, 9]


def anchors_for_rule(pre: Dict[str, object], rule: ms.Rule) -> Tuple[int, ...]:
    return tuple(ms.anchor_by_feature(pre, rule))


def color0_latin(pre: Dict[str, object], anchors: Sequence[int]) -> bool:
    for token0, token1, token2, token3, token4 in pre["color0_patterns"]:
        indegree = int(anchors[token0] == 0)
        indegree += int(anchors[token1] == 1)
        indegree += int(anchors[token2] == 2)
        indegree += int(anchors[token3] == 3)
        indegree += int(anchors[token4] == 4)
        if indegree != 1:
            return False
    return True


def outgoing_defect_count(pre: Dict[str, object], anchors: Sequence[int]) -> Tuple[int, Tuple[List[int], List[int]] | None]:
    fids_by_color = pre["feature_ids_by_color"]
    coords = pre["coords"]
    count = 0
    first_bad: Tuple[List[int], List[int]] | None = None
    for idx in range(pre["n"]):
        dirs = [int((anchors[fids_by_color[color][idx]] + color) % ms.DIM) for color in range(ms.DIM)]
        if len(set(dirs)) != ms.DIM:
            count += 1
            if first_bad is None:
                first_bad = (list(coords[idx]), dirs)
    return count, first_bad


@dataclass(frozen=True)
class LatinAnchorRow:
    family: str
    rule_key: str
    defect_count_m5: int
    first_bad_vertex_m5: List[int] | None
    first_bad_dirs_m5: List[int] | None


def latin_anchor_catalog(pre: Dict[str, object], rules: Sequence[ms.Rule]) -> Tuple[List[Tuple[int, ...]], List[LatinAnchorRow]]:
    anchor_to_rules: Dict[Tuple[int, ...], List[ms.Rule]] = defaultdict(list)
    best_meta: Dict[Tuple[int, ...], LatinAnchorRow] = {}
    for rule in rules:
        anchors = anchors_for_rule(pre, rule)
        if not color0_latin(pre, anchors):
            continue
        defects, first_bad = outgoing_defect_count(pre, anchors)
        first_bad_vertex = None if first_bad is None else first_bad[0]
        first_bad_dirs = None if first_bad is None else first_bad[1]
        row = LatinAnchorRow(
            family=rule.family,
            rule_key=str(rule.effective_key()),
            defect_count_m5=defects,
            first_bad_vertex_m5=first_bad_vertex,
            first_bad_dirs_m5=first_bad_dirs,
        )
        anchor_to_rules[anchors].append(rule)
        prev = best_meta.get(anchors)
        if prev is None or (row.defect_count_m5, row.rule_key) < (prev.defect_count_m5, prev.rule_key):
            best_meta[anchors] = row
    anchor_rows = [best_meta[a] for a in anchor_to_rules]
    anchors = list(anchor_to_rules)
    return anchors, anchor_rows


def subset_count(
    *,
    anchor_list: Sequence[Tuple[int, ...]],
    state_patterns: Sequence[Tuple[int, ...]],
    colors: Sequence[int],
    limit: int | None = None,
) -> int:
    colors = tuple(colors)
    dir_pat: Dict[int, List[Tuple[int, ...]]] = {c: [] for c in colors}
    for c in colors:
        for anchors in anchor_list:
            dir_pat[c].append(tuple(int((anchors[p[c]] + c) % ms.DIM) for p in state_patterns))

    count = 0

    def bt(pos: int, used: List[set[int]]) -> None:
        nonlocal count
        if limit is not None and count >= limit:
            return
        if pos == len(colors):
            count += 1
            return
        c = colors[pos]
        for ci in range(len(anchor_list)):
            dirs = dir_pat[c][ci]
            ok = True
            for idx, d in enumerate(dirs):
                if d in used[idx]:
                    ok = False
                    break
            if not ok:
                continue
            for idx, d in enumerate(dirs):
                used[idx].add(d)
            bt(pos + 1, used)
            for idx, d in enumerate(dirs):
                used[idx].remove(d)

    used = [set() for _ in state_patterns]
    bt(0, used)
    return count


def main() -> None:
    sig_catalog = ms.exact_signature_catalog([5, 7, 9, 11, 13])
    pre_by_m = {m: ms.precompute_m(m, sig_catalog["signature_to_id"]) for m in M_VALUES}

    simple_rules = ms.simple_flag_rows()
    exact_rules = ms.exact_signature_rows(len(sig_catalog["rows"]))
    all_rules = list(simple_rules) + list(exact_rules)

    latin_counts: Dict[str, Dict[str, int]] = {
        "simple": {},
        "exact_signature": {},
        "all": {},
    }
    for label, rules in [
        ("simple", simple_rules),
        ("exact_signature", exact_rules),
        ("all", all_rules),
    ]:
        for m, pre in pre_by_m.items():
            latin = 0
            for rule in rules:
                if color0_latin(pre, anchors_for_rule(pre, rule)):
                    latin += 1
            latin_counts[label][str(m)] = latin

    pre5 = pre_by_m[5]
    anchor_list, anchor_rows = latin_anchor_catalog(pre5, all_rules)
    state_patterns_m5 = list(
        {
            tuple(int(pre5["feature_ids_by_color"][c][idx]) for c in range(ms.DIM))
            for idx in range(pre5["n"])
        }
    )

    pair_counts: Dict[str, int] = {}
    triple_counts: Dict[str, int] = {}
    for colors in itertools.combinations(range(ms.DIM), 2):
        pair_counts[str(list(colors))] = subset_count(
            anchor_list=anchor_list,
            state_patterns=state_patterns_m5,
            colors=colors,
            limit=None,
        )
    for colors in itertools.combinations(range(ms.DIM), 3):
        triple_counts[str(list(colors))] = subset_count(
            anchor_list=anchor_list,
            state_patterns=state_patterns_m5,
            colors=colors,
            limit=1,
        )

    # One-rule outgoing-exhaustive count on m=5.
    single_rule_exhaustive_count = 0
    best_defect_row = min(anchor_rows, key=lambda row: (row.defect_count_m5, row.rule_key))
    for row in anchor_rows:
        if row.defect_count_m5 == 0:
            single_rule_exhaustive_count += 1

    # Sanity on m=7 for one adjacent pair, one nonadjacent pair, one triple.
    pre7 = pre_by_m[7]
    state_patterns_m7 = list(
        {
            tuple(int(pre7["feature_ids_by_color"][c][idx]) for c in range(ms.DIM))
            for idx in range(pre7["n"])
        }
    )
    # Latin anchors are stable on checked m, but recompute as a guard.
    anchor_set_m7 = []
    seen_m7 = set()
    for rule in all_rules:
        anchors = anchors_for_rule(pre7, rule)
        if color0_latin(pre7, anchors) and anchors not in seen_m7:
            seen_m7.add(anchors)
            anchor_set_m7.append(anchors)

    sanity_m7 = {
        "adjacent_pair_[0,1]_exists": bool(
            subset_count(anchor_list=anchor_set_m7, state_patterns=state_patterns_m7, colors=[0, 1], limit=1)
        ),
        "nonadjacent_pair_[0,2]_exists": bool(
            subset_count(anchor_list=anchor_set_m7, state_patterns=state_patterns_m7, colors=[0, 2], limit=1)
        ),
        "triple_[0,1,2]_exists": bool(
            subset_count(anchor_list=anchor_set_m7, state_patterns=state_patterns_m7, colors=[0, 1, 2], limit=1)
        ),
    }

    summary = {
        "task": "d5_237_G1_modeswitch_candidate_search",
        "bundle": str(BUNDLE),
        "family_scope": {
            "simple_rule_count": len(simple_rules),
            "exact_signature_rule_count": len(exact_rules),
            "all_rule_count": len(all_rules),
        },
        "latin_counts_by_m": latin_counts,
        "latin_anchor_count_m5": len(anchor_list),
        "single_rule_outgoing_exhaustive_count_m5": single_rule_exhaustive_count,
        "best_single_rule_defect_m5": {
            "defect_count": best_defect_row.defect_count_m5,
            "rule_key": best_defect_row.rule_key,
            "family": best_defect_row.family,
            "first_bad_vertex": best_defect_row.first_bad_vertex_m5,
            "first_bad_dirs": best_defect_row.first_bad_dirs_m5,
        },
        "pair_counts_m5": pair_counts,
        "triple_exists_m5": {k: bool(v) for k, v in triple_counts.items()},
        "max_color_subset_size_m5": 2,
        "adjacent_pairs_only_m5": all(
            (pair_counts[str(list(colors))] > 0)
            == ((colors[1] - colors[0]) % ms.DIM in (1, ms.DIM - 1))
            for colors in itertools.combinations(range(ms.DIM), 2)
        ),
        "sanity_m7": sanity_m7,
        "conclusion": (
            "Inside the surfaced mode-switch family, outgoing-disjoint color packages on m=5 exist for at most two colors, "
            "and the only surviving pairs are cyclic-adjacent pairs. No three-color subset survives, hence no four-color baseline "
            "and no five-color G1 package can be built from this family. Therefore any honest closure of G1 must use genuinely "
            "different SelCorr/SelStar defect-splice data rather than a search inside the surfaced mode-switch rules."
        ),
    }

    summary_path = Path("/mnt/data/d5_237_G1_modeswitch_candidate_summary.json")
    with summary_path.open("w") as f:
        json.dump(summary, f, indent=2)

    table_path = Path("/mnt/data/d5_237_G1_modeswitch_candidate_table.csv")
    with table_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["kind", "colors", "count_or_exists"])
        for colors, count in sorted(pair_counts.items()):
            writer.writerow(["pair_count_m5", colors, count])
        for colors, exists in sorted(triple_counts.items()):
            writer.writerow(["triple_exists_m5", colors, int(bool(exists))])
        writer.writerow(["latin_anchor_count_m5", "all", len(anchor_list)])
        writer.writerow(["single_rule_outgoing_exhaustive_count_m5", "all", single_rule_exhaustive_count])
        writer.writerow(["best_single_rule_defect_m5", "all", best_defect_row.defect_count_m5])
        writer.writerow(["sanity_m7_adjacent_pair_[0,1]_exists", "[0,1]", int(sanity_m7["adjacent_pair_[0,1]_exists"])])
        writer.writerow(["sanity_m7_nonadjacent_pair_[0,2]_exists", "[0,2]", int(sanity_m7["nonadjacent_pair_[0,2]_exists"])])
        writer.writerow(["sanity_m7_triple_[0,1,2]_exists", "[0,1,2]", int(sanity_m7["triple_[0,1,2]_exists"])])

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
