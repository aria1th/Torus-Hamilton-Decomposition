#!/usr/bin/env python3
"""Analyze Sessions 26/27 as a geometry-vs-holonomy decomposition."""

from __future__ import annotations

import argparse
import json
import platform
import time
from collections import Counter, defaultdict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

TASK_ID = "D5-TWIST-GEOMETRY-ANALYSIS-010"

try:
    from rich.console import Console
except ImportError:  # pragma: no cover
    Console = None


def rich_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def environment_block() -> Dict[str, object]:
    return {"python_version": platform.python_version(), "rich_version": rich_version()}


def _load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text())


def _ordered_per_m_keys(per_m: Mapping[str, object]) -> List[str]:
    return sorted(per_m.keys(), key=int)


def cycle_signature(per_m: Mapping[str, object]) -> Tuple[Tuple[int, int, Tuple[int, ...]], ...]:
    out = []
    for m in _ordered_per_m_keys(per_m):
        row = per_m[m]["color0_return"]
        out.append((int(m), int(row["U_cycle_count"]), tuple(int(v) for v in row["U_cycle_lengths"])))
    return tuple(out)


def monodromy_signature(per_m: Mapping[str, object]) -> Tuple[Tuple[int, Tuple[int, ...]], ...]:
    out = []
    for m in _ordered_per_m_keys(per_m):
        row = per_m[m]["color0_return"]
        out.append((int(m), tuple(int(v) for v in row["monodromies"])))
    return tuple(out)


def _serialize_cycle_signature(signature: Tuple[Tuple[int, int, Tuple[int, ...]], ...]) -> List[Dict[str, object]]:
    return [
        {"m": m, "U_cycle_count": count, "U_cycle_lengths": list(lengths)}
        for m, count, lengths in signature
    ]


def _serialize_monodromy_signature(signature: Tuple[Tuple[int, Tuple[int, ...]], ...]) -> List[Dict[str, object]]:
    return [
        {"m": m, "monodromies": list(values)}
        for m, values in signature
    ]


def _ordered_pair(rule: Mapping[str, object]) -> Tuple[str, str]:
    return (str(rule["layer3_mode_p0"]["name"]), str(rule["layer3_mode_p1"]["name"]))


def _layer2_seed(rule: Mapping[str, object]) -> Tuple[object, ...]:
    if "layer2_bit_name" in rule:
        return (
            str(rule["layer2_bit_name"]),
            int(rule["layer2_alt"]),
            str(rule["layer2_orientation"]),
        )
    return (
        "representative_q=-1",
        str(rule["layer2_orientation"]),
    )


def _layer3_gadget(rule: Mapping[str, object]) -> Tuple[object, ...]:
    return (
        str(rule.get("layer3_bit_name", rule.get("representative_old_bit_name", ""))),
        str(rule["predecessor_flag_name"]),
        str(rule["layer3_mode_p0"]["name"]),
        str(rule["layer3_mode_p1"]["name"]),
    )


def _session26_rows(data: Dict[str, object]) -> List[Dict[str, object]]:
    return list(data["candidates"])


def _session27_stage_rows(data: Dict[str, object], stage_name: str) -> List[Dict[str, object]]:
    return list(data[stage_name]["rule_rows"])


def _law_by_pair(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped: Dict[Tuple[str, str], List[Dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[_ordered_pair(row["rule"])].append(row)
    out = []
    for pair, items in sorted(grouped.items()):
        monodromy_signatures = sorted({_serialize_monodromy_signature(monodromy_signature(item["per_m"]))[0]["monodromies"][0] if False else monodromy_signature(item["per_m"]) for item in items}, key=str)
        out.append(
            {
                "ordered_pair": list(pair),
                "row_count": len(items),
                "unique_monodromy_signature_count": len(monodromy_signatures),
                "monodromy_signatures": [_serialize_monodromy_signature(sig) for sig in monodromy_signatures],
                "layer2_seeds": sorted({list(_layer2_seed(item["rule"]))[0] if False else _layer2_seed(item["rule"]) for item in items}, key=str),
                "predecessor_flags": sorted({item["rule"]["predecessor_flag_name"] for item in items}),
                "layer3_bits": sorted({item["rule"].get("layer3_bit_name", "") for item in items}),
            }
        )
    return out


def _cycle_signature_rows(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped: Dict[Tuple[Tuple[int, int, Tuple[int, ...]], ...], List[Dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[cycle_signature(row["per_m"])].append(row)
    out = []
    for signature, items in sorted(grouped.items(), key=lambda entry: str(entry[0])):
        out.append(
            {
                "signature": _serialize_cycle_signature(signature),
                "row_count": len(items),
                "overall_kinds": dict(sorted(Counter(item["overall_kind"] for item in items).items())),
                "layer2_seeds": sorted({_layer2_seed(item["rule"]) for item in items}, key=str),
                "layer3_gadgets": sorted({_layer3_gadget(item["rule"]) for item in items}, key=str)[:24],
            }
        )
    return out


def _seed_signature_summary(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped: Dict[Tuple[object, ...], List[Dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[_layer2_seed(row["rule"])].append(row)
    out = []
    for seed, items in sorted(grouped.items(), key=str):
        signatures = {cycle_signature(item["per_m"]) for item in items}
        kinds = Counter(item["overall_kind"] for item in items)
        out.append(
            {
                "layer2_seed": list(seed),
                "row_count": len(items),
                "unique_cycle_signature_count": len(signatures),
                "cycle_signatures": [_serialize_cycle_signature(sig) for sig in sorted(signatures, key=str)],
                "overall_kinds": dict(sorted(kinds.items())),
            }
        )
    return out


def _alt4_rescue_summary(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped: Dict[Tuple[object, ...], List[Dict[str, object]]] = defaultdict(list)
    for row in rows:
        seed = _layer2_seed(row["rule"])
        if (seed[0], seed[1]) not in (("q=-1", 4), ("w+u=2", 4)):
            continue
        grouped[(seed[0], seed[1], seed[2], row["rule"]["layer3_bit_name"])].append(row)

    out = []
    for key, items in sorted(grouped.items(), key=str):
        out.append(
            {
                "layer2_seed": [key[0], key[1], key[2]],
                "layer3_bit_name": key[3],
                "overall_kinds": dict(sorted(Counter(item["overall_kind"] for item in items).items())),
                "cycle_signature": _serialize_cycle_signature(cycle_signature(items[0]["per_m"])),
            }
        )
    return out


def _mixed_rows(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    return [row for row in rows if row["overall_kind"] == "both"]


def _clean_strict_rows(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    return [row for row in rows if row["clean_all"] and row["strict_all"]]


def _session26_summary(validation_json: Path) -> Dict[str, object]:
    data = _load_json(validation_json)
    rows = []
    for row in _session26_rows(data):
        pilot = row["pilot_validation"]
        rows.append({"rule": row["rule"], "per_m": pilot["per_m"], "overall_kind": pilot["overall_kind"], "clean_all": pilot["clean_all"], "strict_all": pilot["strict_all"]})
    mixed = _mixed_rows(rows)
    per_flag = Counter(row["rule"]["predecessor_flag_name"] for row in rows)
    return {
        "source": str(validation_json),
        "candidate_count": len(rows),
        "mixed_count": len(mixed),
        "unique_mixed_cycle_signature_count": len({cycle_signature(row["per_m"]) for row in mixed}),
        "mixed_cycle_signatures": _cycle_signature_rows(mixed),
        "ordered_pair_monodromy_law": _law_by_pair(mixed),
        "flag_counts": dict(sorted(per_flag.items())),
    }


def _session27_stage_summary(stage_rows: Sequence[Dict[str, object]], *, stage_name: str) -> Dict[str, object]:
    clean_strict = _clean_strict_rows(stage_rows)
    mixed = _mixed_rows(clean_strict)
    cycle_only = [row for row in clean_strict if row["overall_kind"] == "cycle_only"]
    return {
        "stage_name": stage_name,
        "clean_strict_count": len(clean_strict),
        "mixed_count": len(mixed),
        "cycle_only_count": len(cycle_only),
        "unique_clean_strict_cycle_signature_count": len({cycle_signature(row["per_m"]) for row in clean_strict}),
        "unique_mixed_cycle_signature_count": len({cycle_signature(row["per_m"]) for row in mixed}),
        "unique_cycle_only_cycle_signature_count": len({cycle_signature(row["per_m"]) for row in cycle_only}),
        "cycle_signatures_clean_strict": _cycle_signature_rows(clean_strict),
        "seed_signature_summary": _seed_signature_summary(clean_strict),
        "ordered_pair_monodromy_law_mixed": _law_by_pair(mixed),
        "alt4_rescue_summary": _alt4_rescue_summary(clean_strict),
    }


def _baseline_summary(cycle_search_json: Path, mixed_validation_json: Path) -> Dict[str, object]:
    cycle_data = _load_json(cycle_search_json)
    mixed_data = _load_json(mixed_validation_json)
    cycle_row = cycle_data["best_cycle_only_rules"][0]
    mixed_row = next(row for row in mixed_data["candidates"] if row["pilot_validation"]["overall_kind"] == "both")
    return {
        "cycle_007": {
            "source": str(cycle_search_json),
            "rule": cycle_row["rule"],
            "cycle_signature": _serialize_cycle_signature(cycle_signature(cycle_row["per_m"])),
        },
        "mixed_008": {
            "source": str(mixed_validation_json),
            "rule": mixed_row["rule"],
            "cycle_signature": _serialize_cycle_signature(cycle_signature(mixed_row["pilot_validation"]["per_m"])),
            "monodromy_signature": _serialize_monodromy_signature(monodromy_signature(mixed_row["pilot_validation"]["per_m"])),
        },
    }


def _stability_summary(validation_json: Path) -> Dict[str, object]:
    data = _load_json(validation_json)
    rows = []
    for row in data["stability_spot_checks"]:
        rows.append({"rule": row["rule"], "per_m": row["stability_validation"]["per_m"], "overall_kind": row["stability_validation"]["overall_kind"]})
    return {
        "source": str(validation_json),
        "spot_check_count": len(rows),
        "unique_cycle_signature_count": len({cycle_signature(row["per_m"]) for row in rows}),
        "unique_monodromy_signature_count": len({monodromy_signature(row["per_m"]) for row in rows}),
        "overall_kinds": dict(sorted(Counter(row["overall_kind"] for row in rows).items())),
        "cycle_signatures": _cycle_signature_rows(rows),
        "ordered_pair_monodromy_law": _law_by_pair(rows),
    }


def run_analysis(
    *,
    session26_validation_json: Path,
    session27_search_json: Path,
    session27_validation_json: Path,
    cycle_baseline_json: Path,
) -> Dict[str, object]:
    start = time.perf_counter()
    session26 = _session26_summary(session26_validation_json)
    session27_search = _load_json(session27_search_json)
    stage1 = _session27_stage_summary(_session27_stage_rows(session27_search, "stage1"), stage_name="stage1")
    stage2 = _session27_stage_summary(_session27_stage_rows(session27_search, "stage2"), stage_name="stage2")
    baselines = _baseline_summary(cycle_baseline_json, session26_validation_json)
    stability = _stability_summary(session27_validation_json)

    universal_geometry_stage1 = stage1["unique_clean_strict_cycle_signature_count"] == 1
    universal_geometry_stage2 = stage2["unique_clean_strict_cycle_signature_count"] == 1
    pair_only_monodromy_stage1 = all(row["unique_monodromy_signature_count"] == 1 for row in stage1["ordered_pair_monodromy_law_mixed"])
    pair_only_monodromy_stage2 = all(row["unique_monodromy_signature_count"] == 1 for row in stage2["ordered_pair_monodromy_law_mixed"])

    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": environment_block(),
        "inputs": {
            "session26_validation_json": str(session26_validation_json),
            "session27_search_json": str(session27_search_json),
            "session27_validation_json": str(session27_validation_json),
            "cycle_baseline_json": str(cycle_baseline_json),
        },
        "baselines": baselines,
        "session26": session26,
        "session27": {
            "stage1": stage1,
            "stage2": stage2,
            "stability_spot_checks": stability,
        },
        "interpretation": {
            "universal_geometry_stage1": universal_geometry_stage1,
            "universal_geometry_stage2": universal_geometry_stage2,
            "pair_only_monodromy_stage1": pair_only_monodromy_stage1,
            "pair_only_monodromy_stage2": pair_only_monodromy_stage2,
            "stage1_mixed_improvement_count": int(session27_search["stage1"]["counts"]["improved_mixed_count"]),
            "stage2_mixed_improvement_count": int(session27_search["stage2"]["counts"]["improved_mixed_count"]),
            "diagnosis": (
                "Within the current graft family, cycle geometry rigidifies to the universal m-cycle profile, "
                "while the ordered layer-3 slice pair controls the nonzero holonomy."
            ),
        },
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        (
            f"stage1 universal_geometry={summary['interpretation']['universal_geometry_stage1']} "
            f"pair_only_monodromy={summary['interpretation']['pair_only_monodromy_stage1']}"
        ),
        (
            f"stage2 universal_geometry={summary['interpretation']['universal_geometry_stage2']} "
            f"pair_only_monodromy={summary['interpretation']['pair_only_monodromy_stage2']}"
        ),
        summary["interpretation"]["diagnosis"],
    ]
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze Sessions 26/27 as geometry-vs-holonomy data.")
    parser.add_argument(
        "--session26-validation-json",
        type=Path,
        default=Path("artifacts/d5_layer3_mode_switch_008/data/validation_summary.json"),
        help="Session 26 validation summary",
    )
    parser.add_argument(
        "--session27-search-json",
        type=Path,
        default=Path("artifacts/d5_strong_cycle_mix_009/data/search_summary.json"),
        help="Session 27 search summary",
    )
    parser.add_argument(
        "--session27-validation-json",
        type=Path,
        default=Path("artifacts/d5_strong_cycle_mix_009/data/validation_summary.json"),
        help="Session 27 validation summary",
    )
    parser.add_argument(
        "--cycle-baseline-json",
        type=Path,
        default=Path("artifacts/d5_layer3_alt2_decoupled_007/data/search_summary.json"),
        help="Session 25/007 cycle-only baseline",
    )
    parser.add_argument("--out", type=Path, required=True, help="write analysis JSON here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    summary = run_analysis(
        session26_validation_json=args.session26_validation_json,
        session27_search_json=args.session27_search_json,
        session27_validation_json=args.session27_validation_json,
        cycle_baseline_json=args.cycle_baseline_json,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
