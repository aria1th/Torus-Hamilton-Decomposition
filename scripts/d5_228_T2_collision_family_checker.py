#!/usr/bin/env python3
"""Check the explicit T2 obstruction families against the surfaced 2026-03-21 bundle.

The theorem-facing formulas being checked are:
  T2 = sigma22 = [4,1,4]/[2,1,2]
  color-0, w0=s0=0.

Changed labels and claimed collision families:
  R1:  x -> x+eW, mate y=x+eW-eU
  L2:  x -> x+eQ, mate y=x-eX+eQ
  R2:  x -> x+eQ, mate y=x-eX+eQ
  R3:  x -> x+eW, mate y=x-eX+eW
  L3^0 (tail): x in L3 with s(x)=0, x -> x+eU, mate y=x-eX+eU

The script uses the surfaced bundle code for the row itself; it only wraps the witness
registry the same way as d5_224 did.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

M_VALUES: Tuple[int, ...] = (5, 7, 9, 11, 13)
LEFT_WORD = (4, 1, 4)
RIGHT_WORD = (2, 1, 2)
TASK_ID = "D5-T2-COLLISION-FAMILY-CHECK-228"


def load_scan224_module() -> object:
    spec = importlib.util.spec_from_file_location("scan224", "/mnt/data/d5_224_T2_T3_bundle_obstruction_scan.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load d5_224 helper module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module


def add_vec(x: Sequence[int], delta: Sequence[int], m: int) -> Tuple[int, ...]:
    return tuple((int(a) + int(b)) % m for a, b in zip(x, delta))


def coord_payload(coord: Sequence[int], m: int) -> Dict[str, int]:
    x0, q, w, v, u = [int(c) for c in coord]
    return {
        "x0": x0,
        "q": q,
        "w": w,
        "v": v,
        "u": u,
        "s": int((w + u) % m),
        "layer": int((x0 + q + w + v + u) % m),
    }


def s_value(coord: Sequence[int], m: int) -> int:
    return int((int(coord[2]) + int(coord[4])) % m)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bundle-root",
        default="/mnt/data/bundlefull/roundy_d5_endpoint_return_model_bundle_20260321_update_197",
        help="bundle root containing scripts/ and artifacts/",
    )
    parser.add_argument(
        "--summary-json",
        default="/mnt/data/d5_228_T2_collision_family_summary.json",
    )
    parser.add_argument(
        "--table-csv",
        default="/mnt/data/d5_228_T2_collision_family_table.csv",
    )
    args = parser.parse_args()

    helper = load_scan224_module()
    bundle_root = Path(args.bundle_root)
    seed032 = helper._import_seed032(bundle_root)
    mixed_rule = seed032._mixed_rule()

    per_m: Dict[str, object] = {}
    table_rows: List[Dict[str, object]] = []

    for m in M_VALUES:
        prepared = seed032._prepare_m(m, mixed_rule)
        nexts_all, meta = seed032._build_candidate(
            prepared,
            w0=0,
            s0=0,
            left_word=LEFT_WORD,
            right_word=RIGHT_WORD,
            cocycle_defect="none",
            repair=None,
        )
        if nexts_all is None:
            raise RuntimeError(f"base T2 row aborted at m={m}: {meta}")

        row = nexts_all[0]
        baseline = prepared.baseline_nexts_all[0]
        labels = meta["labels_by_color"][0]
        coords = [tuple(int(v) for v in c) for c in prepared.pre["coords"]]
        idx_by_coord = {coord: idx for idx, coord in enumerate(coords)}

        def must_get(label: str) -> List[int]:
            return [idx for idx, current in enumerate(labels) if current == label]

        label_sizes = {label: len(must_get(label)) for label in ["L1", "R1", "L2", "R2", "L3", "R3"]}

        family_specs = [
            ("R1", must_get("R1"), (0, 0, 1, 0, 0), (0, 0, 1, 0, -1)),
            ("L2", must_get("L2"), (0, 1, 0, 0, 0), (-1, 1, 0, 0, 0)),
            ("R2", must_get("R2"), (0, 1, 0, 0, 0), (-1, 1, 0, 0, 0)),
            ("R3", must_get("R3"), (0, 0, 1, 0, 0), (-1, 0, 1, 0, 0)),
        ]
        l3_tail = [idx for idx in must_get("L3") if s_value(coords[idx], m) == 0]
        family_specs.append(("L3_tail", l3_tail, (0, 0, 0, 0, 1), (-1, 0, 0, 0, 1)))

        family_results: Dict[str, object] = {}
        all_ok = True
        for family_name, sources, target_delta, mate_delta in family_specs:
            family_ok = True
            bad_examples: List[Dict[str, object]] = []
            for idx in sources:
                x = coords[idx]
                target_coord = add_vec(x, target_delta, m)
                mate_coord = add_vec(x, mate_delta, m)
                tgt = idx_by_coord[target_coord]
                mate = idx_by_coord[mate_coord]
                target_match = int(row[idx]) == int(tgt)
                mate_background = labels[mate] == "B"
                mate_hits_same_target = int(baseline[mate]) == int(tgt)
                if not (target_match and mate_background and mate_hits_same_target):
                    family_ok = False
                    bad_examples.append(
                        {
                            "source": coord_payload(x, m),
                            "expected_target": coord_payload(target_coord, m),
                            "actual_target": coord_payload(coords[int(row[idx])], m),
                            "mate": coord_payload(mate_coord, m),
                            "mate_label": labels[mate],
                            "mate_actual_target": coord_payload(coords[int(baseline[mate])], m),
                        }
                    )
                    if len(bad_examples) >= 3:
                        break
            all_ok &= family_ok
            family_results[family_name] = {
                "count": len(sources),
                "ok": family_ok,
                "bad_examples": bad_examples,
            }
            table_rows.append(
                {
                    "m": m,
                    "family": family_name,
                    "count": len(sources),
                    "expected_count": m * (m - 1) if family_name != "L3_tail" else m,
                    "ok": family_ok,
                }
            )

        # Pair counts from actual row, for comparison with d5_224.
        incoming: Dict[int, List[int]] = {}
        for idx, tgt in enumerate(row):
            incoming.setdefault(int(tgt), []).append(int(idx))
        pair_counts = Counter()
        for sources in incoming.values():
            if len(sources) <= 1:
                continue
            pair = tuple(sorted(str(labels[idx]) for idx in sources))
            pair_counts[str(pair)] += 1

        per_m[str(m)] = {
            "label_sizes_color0": label_sizes,
            "families": family_results,
            "pair_counts_color0": dict(sorted(pair_counts.items())),
            "all_formula_checks_ok": all_ok,
        }

    summary = {
        "task_id": TASK_ID,
        "bundle_root": str(bundle_root),
        "m_values": list(M_VALUES),
        "per_m": per_m,
        "all_formula_checks_ok": all(bool(per_m[str(m)]["all_formula_checks_ok"]) for m in M_VALUES),
    }

    Path(args.summary_json).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    with Path(args.table_csv).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["m", "family", "count", "expected_count", "ok"])
        writer.writeheader()
        writer.writerows(table_rows)


if __name__ == "__main__":
    main()
