#!/usr/bin/env python3
"""Coarse-class reduction for the remaining G1 splice search.

What this script does:
1. Surface the mixed_008 coarse feature classes from the 2026-03-21 bundle.
2. Define the explicit layer-baseline package
      sum=0 -> anchor 1,
      sum=1 -> anchor 4,
      sum>=2 -> anchor 0,
   and verify that it is outgoing-exhaustive and incoming-Latin on checked moduli.
3. Compare mixed_008 against this baseline at the coarse-class level.
4. Search, on the finite coarse-class state carrier, whether a support-restricted
   modification on a given color subset S can make all observed coarse class tuples
   outgoing-exhaustive.

Outputs:
- /mnt/data/d5_244_G1_coarse_class_baseline_summary.json
- /mnt/data/d5_244_G1_coarse_class_baseline_table.csv
"""
from __future__ import annotations

import csv
import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Set, Tuple

BUNDLE = Path(
    "/mnt/data/bundle197/roundy_d5_endpoint_return_model_bundle_20260321_update_197"
)
CODE_DIR = BUNDLE / "artifacts" / "d5_mixed_skew_odometer_normal_form_018" / "code"
WITNESS_REGISTRY = BUNDLE / "artifacts" / "d5_mixed_skew_odometer_normal_form_018" / "data" / "witness_registry.json"

sys.path.insert(0, str(CODE_DIR))
import torus_nd_d5_layer3_mode_switch_common as ms  # type: ignore  # noqa: E402
from torus_nd_d5_strict_palette_context_common import incoming_latin_all  # type: ignore  # noqa: E402

CHECKED_M_VALUES = [3, 5, 7, 9, 11, 13]
SEARCH_M_VALUES = [5, 7, 9, 11, 13]
MUTABLE_CLASSES = ["L2s0", "L2s1", "L3s30p0", "L3s30p1", "L3s31p0", "L3s31p1"]


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


def current_class_anchor() -> Dict[str, int]:
    pre = ms.precompute_m(11, SIGNATURE_TO_ID)
    anchors = ms.anchor_by_feature(pre, RULE)
    out: Dict[str, Set[int]] = defaultdict(set)
    for fid, row in enumerate(pre["feature_rows"]):
        out[coarse_class_of_feature(row)].add(int(anchors[fid]))
    return {cls: next(iter(vals)) for cls, vals in out.items()}


CURRENT_CLASS_ANCHOR = current_class_anchor()


def feature_class_tuples_for_modulus(m: int) -> List[Tuple[str, str, str, str, str]]:
    pre = ms.precompute_m(m, SIGNATURE_TO_ID)
    out: List[Tuple[str, str, str, str, str]] = []
    for idx in range(pre["n"]):
        classes = []
        for color in range(ms.DIM):
            fid = pre["feature_ids_by_color"][color][idx]
            classes.append(coarse_class_of_feature(pre["feature_rows"][fid]))
        out.append(tuple(classes))
    return out


ALL_CLASS_TUPLES = sorted(set().union(*(feature_class_tuples_for_modulus(m) for m in SEARCH_M_VALUES)))


def direction_tuple_from_class_tuple(
    class_tuple: Sequence[str], *, support_assign: Mapping[int, Mapping[str, int]] | None = None
) -> Tuple[int, int, int, int, int]:
    dirs = []
    for color, cls in enumerate(class_tuple):
        if support_assign is not None and color in support_assign and cls in support_assign[color]:
            anchor = int(support_assign[color][cls])
        else:
            anchor = int(CURRENT_CLASS_ANCHOR[cls])
        dirs.append((anchor + color) % ms.DIM)
    return tuple(dirs)


# 60 stable bad direction patterns under the naive mixed_008 cyclic package.
BAD_DIR_PATTERNS = sorted(
    {
        direction_tuple_from_class_tuple(class_tuple)
        for class_tuple in ALL_CLASS_TUPLES
        if len(set(direction_tuple_from_class_tuple(class_tuple))) != ms.DIM
    }
)


def necessary_support_subsets_from_bad_patterns() -> List[Tuple[int, ...]]:
    feasible: List[Tuple[int, ...]] = []
    for r in range(ms.DIM + 1):
        for subset in itertools.combinations(range(ms.DIM), r):
            fixed = [c for c in range(ms.DIM) if c not in subset]
            ok = True
            for dirs in BAD_DIR_PATTERNS:
                fixed_dirs = [dirs[c] for c in fixed]
                if len(set(fixed_dirs)) != len(fixed_dirs):
                    ok = False
                    break
            if ok:
                feasible.append(subset)
        if feasible:
            return feasible
    return feasible


NECESSARY_MIN_SUPPORTS = necessary_support_subsets_from_bad_patterns()


def baseline_nexts(pre: Mapping[str, object]) -> List[List[int]]:
    nexts = [[0] * int(pre["n"]) for _ in range(ms.DIM)]
    for color in range(ms.DIM):
        row = nexts[color]
        for idx, fid in enumerate(pre["feature_ids_by_color"][color]):
            cls = coarse_class_of_feature(pre["feature_rows"][fid])
            anchor = BASELINE_CLASS_ANCHOR[cls]
            direction = (anchor + color) % ms.DIM
            row[idx] = pre["step_by_dir"][direction][idx]
    return nexts


def baseline_row_for_modulus(m: int) -> Dict[str, object]:
    pre = ms.precompute_m(m, SIGNATURE_TO_ID)
    nexts = baseline_nexts(pre)
    outgoing_ok = True
    for idx in range(pre["n"]):
        dirs = []
        for color in range(ms.DIM):
            fid = pre["feature_ids_by_color"][color][idx]
            cls = coarse_class_of_feature(pre["feature_rows"][fid])
            dirs.append((BASELINE_CLASS_ANCHOR[cls] + color) % ms.DIM)
        if len(set(dirs)) != ms.DIM:
            outgoing_ok = False
            break
    return {
        "m": m,
        "outgoing_exhaustive": outgoing_ok,
        "incoming_latin": bool(incoming_latin_all(nexts)),
    }


BASELINE_PER_M = {str(m): baseline_row_for_modulus(m) for m in CHECKED_M_VALUES}


def allowed_assignments_for_support(support: Tuple[int, ...], class_tuple: Sequence[str]) -> Tuple[Tuple[int, ...], ...]:
    allowed: List[Tuple[int, ...]] = []
    for values in itertools.product(range(ms.DIM), repeat=len(support)):
        support_assign = {color: {class_tuple[color]: value} for color, value in zip(support, values)}
        dirs = direction_tuple_from_class_tuple(class_tuple, support_assign=support_assign)
        if len(set(dirs)) == ms.DIM:
            allowed.append(tuple(int(v) for v in values))
    return tuple(allowed)


def coarse_support_has_solution(support: Tuple[int, ...]) -> bool:
    vars_ = [(color, cls) for color in support for cls in MUTABLE_CLASSES]
    constraints: List[Tuple[Tuple[str, str, str, str, str], Tuple[Tuple[int, ...], ...]]] = []
    for class_tuple in ALL_CLASS_TUPLES:
        allowed = allowed_assignments_for_support(support, class_tuple)
        if not allowed:
            return False
        constraints.append((class_tuple, allowed))

    domains: Dict[Tuple[int, str], Set[int]] = {var: set(range(ms.DIM)) for var in vars_}
    for class_tuple, allowed in constraints:
        for color, cls in vars_:
            if class_tuple[color] != cls:
                continue
            pos = support.index(color)
            domains[(color, cls)] &= {sol[pos] for sol in allowed}
    if any(len(dom) == 0 for dom in domains.values()):
        return False

    by_var: Dict[Tuple[int, str], List[int]] = defaultdict(list)
    for idx, (class_tuple, _allowed) in enumerate(constraints):
        for color, cls in vars_:
            if class_tuple[color] == cls:
                by_var[(color, cls)].append(idx)

    def constraint_ok(item: Tuple[Tuple[str, str, str, str, str], Tuple[Tuple[int, ...], ...]], assign: Mapping[Tuple[int, str], int]) -> bool:
        class_tuple, allowed = item
        for sol in allowed:
            ok = True
            for pos, color in enumerate(support):
                key = (color, class_tuple[color])
                if class_tuple[color] in MUTABLE_CLASSES and key in assign and int(sol[pos]) != int(assign[key]):
                    ok = False
                    break
            if ok:
                return True
        return False

    order = sorted(vars_, key=lambda var: (len(domains[var]), -len(by_var[var])))

    def backtrack(assign: MutableMapping[Tuple[int, str], int]) -> bool:
        if len(assign) == len(vars_):
            return True
        unassigned = [var for var in order if var not in assign]
        var = unassigned[0]
        # Prefer baseline value when available.
        baseline_pref = BASELINE_CLASS_ANCHOR[var[1]]
        values = sorted(domains[var], key=lambda v: (v != baseline_pref, v))
        for value in values:
            assign[var] = int(value)
            ok = True
            for idx in by_var[var]:
                if not constraint_ok(constraints[idx], assign):
                    ok = False
                    break
            if ok and backtrack(assign):
                return True
            assign.pop(var, None)
        return False

    return backtrack({})


SUPPORT_RESULTS: Dict[str, object] = {
    "size3": {},
    "size4": {},
}
for r in (3, 4):
    for support in itertools.combinations(range(ms.DIM), r):
        SUPPORT_RESULTS[f"size{r}"][str(list(support))] = coarse_support_has_solution(support)

FULL_SUPPORT_BASELINE_OK = all(row["outgoing_exhaustive"] and row["incoming_latin"] for row in BASELINE_PER_M.values())
DIFFERENCE_CLASSES = sorted(
    cls for cls in BASELINE_CLASS_ANCHOR if BASELINE_CLASS_ANCHOR[cls] != CURRENT_CLASS_ANCHOR[cls]
)


def main() -> None:
    summary = {
        "task": "d5_244_G1_coarse_class_baseline_search",
        "witness": "mixed_008",
        "checked_m_values": CHECKED_M_VALUES,
        "search_m_values": SEARCH_M_VALUES,
        "current_class_anchor": CURRENT_CLASS_ANCHOR,
        "baseline_class_anchor": BASELINE_CLASS_ANCHOR,
        "difference_classes": DIFFERENCE_CLASSES,
        "difference_class_count": len(DIFFERENCE_CLASSES),
        "bad_dir_pattern_count": len(BAD_DIR_PATTERNS),
        "bad_dir_patterns": [list(row) for row in BAD_DIR_PATTERNS],
        "necessary_min_support_size": len(NECESSARY_MIN_SUPPORTS[0]) if NECESSARY_MIN_SUPPORTS else None,
        "necessary_min_support_subsets": [list(s) for s in NECESSARY_MIN_SUPPORTS],
        "coarse_support_results": SUPPORT_RESULTS,
        "baseline_per_m": BASELINE_PER_M,
        "baseline_valid_all_checked": FULL_SUPPORT_BASELINE_OK,
        "conclusion": (
            "There is an explicit valid baseline package at the coarse-class level, given by anchors 1 on L0, 4 on L1, and 0 elsewhere. "
            "The mixed_008 rule differs from this baseline on exactly three coarse classes: L2s1, L3s30p1, and L3s31p0. "
            "Necessary support analysis on the 60 stable bad direction patterns shows that any repair support must have size at least 3, and the exact coarse-class CSP shows that no support of size 3 or 4 can restore outgoing exhaustiveness on all observed class tuples. "
            "Thus the remaining G1 task is best read as a three-class splice of the closed color-4 branch into an already valid baseline, not as a broad selector-family search."
        ),
    }

    summary_path = Path("/mnt/data/d5_244_G1_coarse_class_baseline_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True))

    table_rows: List[Dict[str, object]] = []
    for m_key, row in BASELINE_PER_M.items():
        table_rows.append(
            {
                "kind": "baseline_per_m",
                "m": int(m_key),
                "outgoing_exhaustive": int(bool(row["outgoing_exhaustive"])),
                "incoming_latin": int(bool(row["incoming_latin"])),
                "support": "",
                "has_solution": "",
            }
        )
    for size_key in ("size3", "size4"):
        for support_key, value in SUPPORT_RESULTS[size_key].items():
            table_rows.append(
                {
                    "kind": size_key,
                    "m": "",
                    "outgoing_exhaustive": "",
                    "incoming_latin": "",
                    "support": support_key,
                    "has_solution": int(bool(value)),
                }
            )
    table_path = Path("/mnt/data/d5_244_G1_coarse_class_baseline_table.csv")
    with table_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["kind", "m", "outgoing_exhaustive", "incoming_latin", "support", "has_solution"],
        )
        writer.writeheader()
        writer.writerows(table_rows)

    print(summary_path)
    print(table_path)


if __name__ == "__main__":
    main()
