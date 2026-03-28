#!/usr/bin/env python3
"""Verify the explicit T3 four-family collision formulas against the surfaced bundle.

This script checks the symbolic formulas from d5_225 on a modest range of moduli.
It is deliberately narrow: it only inspects the repeated-end row
    sigma33 = [4,4,1]/[2,2,1]
at the representative seed (w0,s0)=(0,0).
"""
from __future__ import annotations

import csv
import importlib
import json
import platform
import sys
import time
import types
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

TASK_ID = "D5-T3-FOUR-COLLISION-FAMILY-CHECK-225"
M_VALUES: Tuple[int, ...] = (3, 5, 7, 9, 11)
LEFT_WORD = (4, 4, 1)
RIGHT_WORD = (2, 2, 1)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _load_registry_rows(bundle_root: Path) -> List[Mapping[str, object]]:
    registry_path = bundle_root / "artifacts" / "d5_return_map_model_017" / "data" / "witness_registry.json"
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise TypeError(f"Unexpected witness registry structure at {registry_path}")
    return data


def _inject_common_stub(bundle_root: Path) -> None:
    rows = _load_registry_rows(bundle_root)
    stub = types.ModuleType("torus_nd_d5_return_map_model_common")

    def environment_block() -> Dict[str, object]:
        return {
            "python_version": platform.python_version(),
            "runtime": "bundle_stubbed_loader",
            "bundle_root": str(bundle_root),
        }

    def runtime_since(start: float) -> float:
        return time.perf_counter() - start

    def load_witness_specs() -> List[SimpleNamespace]:
        out: List[SimpleNamespace] = []
        for row in rows:
            out.append(
                SimpleNamespace(
                    name=str(row["name"]),
                    role=row.get("role"),
                    family=row.get("family"),
                    source=row.get("source"),
                    rule_payload=row["rule"],
                )
            )
        return out

    stub.environment_block = environment_block  # type: ignore[attr-defined]
    stub.runtime_since = runtime_since  # type: ignore[attr-defined]
    stub.load_witness_specs = load_witness_specs  # type: ignore[attr-defined]
    sys.modules[stub.__name__] = stub


def _import_modules(bundle_root: Path) -> Tuple[Any, Any]:
    script_dir = bundle_root / "artifacts" / "d5_endpoint_latin_repair_032" / "code"
    common_code_dir = bundle_root / "artifacts" / "d5_mixed_skew_odometer_normal_form_018" / "code"
    for directory in (script_dir, common_code_dir):
        directory_str = str(directory)
        if directory_str not in sys.path:
            sys.path.insert(0, directory_str)
    _inject_common_stub(bundle_root)
    seed032 = importlib.import_module("torus_nd_d5_endpoint_latin_repair")
    mode008 = importlib.import_module("torus_nd_d5_layer3_mode_switch_common")
    return seed032, mode008


def _coords_payload(coords: Sequence[int], m: int) -> Dict[str, int]:
    x0, q, w, v, u = [int(value) for value in coords]
    return {
        "x0": x0,
        "q": q,
        "w": w,
        "v": v,
        "u": u,
        "s": int((w + u) % m),
        "layer": int((x0 + q + w + v + u) % m),
    }


def _pair_counts_color0(nexts: Sequence[int], labels: Sequence[str]) -> Dict[str, int]:
    incoming: List[List[int]] = [[] for _ in range(len(nexts))]
    for idx, nxt in enumerate(nexts):
        incoming[int(nxt)].append(int(idx))
    out: Dict[str, int] = {}
    for sources in incoming:
        if len(sources) <= 1:
            continue
        key = str(tuple(sorted(str(labels[idx]) for idx in sources)))
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items()))


def _verify_family(
    *,
    m: int,
    coords: Sequence[Sequence[int]],
    labels: Sequence[str],
    baseline_anchor_rel: Sequence[int],
    nexts: Sequence[int],
    encode_fn: Any,
    label_name: str,
) -> Dict[str, object]:
    if label_name == "R1":
        mate_delta = (0, 0, 1, 0, -1)
        target_delta = (0, 0, 1, 0, 0)
        expected_layer = 1
        expected_w = 0
        expected_s_forbidden = 0
        expected_baseline_anchor = 4
        expected_mate_anchor = 4
    elif label_name == "L2":
        mate_delta = (0, 0, -1, 0, 1)
        target_delta = (0, 0, 0, 0, 1)
        expected_layer = 2
        expected_w = m - 1
        expected_s_forbidden = 1
        expected_baseline_anchor = 2
        expected_mate_anchor = 2
    elif label_name == "L3":
        mate_delta = (-1, 1, 0, 0, 0)
        target_delta = (0, 1, 0, 0, 0)
        expected_layer = 3
        expected_w = m - 1
        expected_s_forbidden = 2
        expected_baseline_anchor = 3
        expected_mate_anchor = 0
    elif label_name == "R3":
        mate_delta = (-1, 1, 0, 0, 0)
        target_delta = (0, 1, 0, 0, 0)
        expected_layer = 3
        expected_w = 2
        expected_s_forbidden = 2
        expected_baseline_anchor = 3
        expected_mate_anchor = 0
    else:
        raise ValueError(label_name)

    def add(coords_row: Sequence[int], delta: Sequence[int]) -> Tuple[int, ...]:
        return tuple((int(coords_row[i]) + int(delta[i])) % m for i in range(5))

    indices = [idx for idx, label in enumerate(labels) if label == label_name]
    if not indices:
        return {
            "source_count": 0,
            "verified": False,
            "reason": "missing label class",
        }

    incoming: List[List[int]] = [[] for _ in range(len(nexts))]
    for idx, nxt in enumerate(nexts):
        incoming[int(nxt)].append(int(idx))

    sample: Dict[str, object] | None = None
    for idx in indices:
        c = tuple(int(value) for value in coords[idx])
        s_val = int((c[2] + c[4]) % m)
        if not (
            int(c[1]) == m - 1
            and int(c[2]) == expected_w
            and int(sum(c) % m) == expected_layer
            and s_val != expected_s_forbidden
            and int(baseline_anchor_rel[idx]) == expected_baseline_anchor
        ):
            return {
                "source_count": len(indices),
                "verified": False,
                "reason": f"source predicate failed at index {idx}",
                "source": _coords_payload(c, m),
            }
        mate = add(c, mate_delta)
        target = add(c, target_delta)
        mate_idx = int(encode_fn(mate, m))
        target_idx = int(encode_fn(target, m))
        if labels[mate_idx] != "B":
            return {
                "source_count": len(indices),
                "verified": False,
                "reason": f"mate not background at index {idx}",
                "source": _coords_payload(c, m),
                "mate": _coords_payload(mate, m),
                "mate_label": str(labels[mate_idx]),
            }
        if int(baseline_anchor_rel[mate_idx]) != expected_mate_anchor:
            return {
                "source_count": len(indices),
                "verified": False,
                "reason": f"mate anchor mismatch at index {idx}",
                "source": _coords_payload(c, m),
                "mate": _coords_payload(mate, m),
                "mate_anchor": int(baseline_anchor_rel[mate_idx]),
            }
        if int(nexts[idx]) != target_idx or int(nexts[mate_idx]) != target_idx:
            return {
                "source_count": len(indices),
                "verified": False,
                "reason": f"common-target identity failed at index {idx}",
                "source": _coords_payload(c, m),
                "mate": _coords_payload(mate, m),
                "target": _coords_payload(target, m),
            }
        source_labels = sorted(str(labels[source_idx]) for source_idx in incoming[target_idx])
        if source_labels != ["B", label_name]:
            return {
                "source_count": len(indices),
                "verified": False,
                "reason": f"incoming labels mismatch at index {idx}",
                "source": _coords_payload(c, m),
                "target": _coords_payload(target, m),
                "incoming_labels": source_labels,
            }
        if sample is None:
            sample = {
                "source": _coords_payload(c, m),
                "mate": _coords_payload(mate, m),
                "target": _coords_payload(target, m),
            }

    return {
        "source_count": len(indices),
        "verified": True,
        "sample": sample,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle-root", type=Path, default=Path("/mnt/data/bundle197"))
    parser.add_argument("--out-json", type=Path, default=Path("/mnt/data/d5_225_T3_four_collision_family_summary.json"))
    parser.add_argument("--out-csv", type=Path, default=Path("/mnt/data/d5_225_T3_four_collision_family_table.csv"))
    args = parser.parse_args()

    start = time.perf_counter()
    seed032, mode008 = _import_modules(args.bundle_root)
    mixed_rule = seed032._mixed_rule()

    summary: Dict[str, object] = {
        "task_id": TASK_ID,
        "bundle_root": str(args.bundle_root),
        "m_values": list(M_VALUES),
        "left_word": list(LEFT_WORD),
        "right_word": list(RIGHT_WORD),
        "per_m": {},
        "runtime_sec": None,
    }
    csv_rows: List[Dict[str, object]] = []

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
            raise RuntimeError(f"Unexpected conflict for T3 at m={m}: {meta}")
        labels = meta["labels_by_color"][0]
        baseline_anchor_rel = prepared.baseline_anchor_rel[0]
        coords = prepared.pre["coords"]
        pair_counts = _pair_counts_color0(nexts_all[0], labels)
        colliding_labels = sorted({key.split("'")[3] for key in pair_counts if key != "('B', 'B')" and key.startswith("('B',")})

        per_m_row: Dict[str, object] = {
            "pair_counts_color0": pair_counts,
            "colliding_changed_labels_color0": colliding_labels,
            "label_counts_color0": {label: int(sum(1 for current in labels if current == label)) for label in sorted(set(labels))},
            "formula_status": "m>=5 theorem verified" if m >= 5 else "exceptional m<5 profile recorded",
        }
        if m >= 5:
            family_rows = {}
            all_verified = True
            for label_name in ("R1", "L2", "L3", "R3"):
                result = _verify_family(
                    m=m,
                    coords=coords,
                    labels=labels,
                    baseline_anchor_rel=baseline_anchor_rel,
                    nexts=nexts_all[0],
                    encode_fn=mode008.encode,
                    label_name=label_name,
                )
                family_rows[label_name] = result
                all_verified &= bool(result["verified"])
            per_m_row["four_family_verification"] = {
                "verified": bool(all_verified),
                "families": family_rows,
            }
        summary["per_m"][str(m)] = per_m_row
        csv_rows.append(
            {
                "m": m,
                "formula_status": per_m_row["formula_status"],
                "colliding_changed_labels_color0": ";".join(colliding_labels),
                "pair_counts_color0": json.dumps(pair_counts, ensure_ascii=False, sort_keys=True),
                "four_family_verified": int(bool(per_m_row.get("four_family_verification", {}).get("verified", False))),
                "R1_source_count": int(per_m_row.get("four_family_verification", {}).get("families", {}).get("R1", {}).get("source_count", 0)),
                "L2_source_count": int(per_m_row.get("four_family_verification", {}).get("families", {}).get("L2", {}).get("source_count", 0)),
                "L3_source_count": int(per_m_row.get("four_family_verification", {}).get("families", {}).get("L3", {}).get("source_count", 0)),
                "R3_source_count": int(per_m_row.get("four_family_verification", {}).get("families", {}).get("R3", {}).get("source_count", 0)),
            }
        )

    summary["runtime_sec"] = time.perf_counter() - start
    _write_json(args.out_json, summary)
    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)
    print(json.dumps({
        "task_id": TASK_ID,
        "out_json": str(args.out_json),
        "out_csv": str(args.out_csv),
        "runtime_sec": summary["runtime_sec"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
