#!/usr/bin/env python3
"""Batch scan structured candidate rules on the directed d-torus."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List

from torus_nd_validate import (
    canonical_direction_tuple,
    defect_support_summary,
    induced_p0_maps,
    load_rule_factory,
    load_witness_rule,
    validate_rule,
)


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _slug_from_source(module: Path | None, function: str, witness_json: Path | None) -> str:
    if witness_json is not None:
        return witness_json.stem
    assert module is not None
    return f"{module.stem}_{function}"


def _classify_instance(report: Dict[str, object]) -> str:
    if not report["rule_valid"]:
        return "candidate_fail"
    if report["all_hamilton"]:
        return "candidate_pass"
    return "candidate_fail"


def _family_status(results: List[Dict[str, object]]) -> str:
    passing = [row for row in results if row["classification"] == "candidate_pass"]
    if not passing:
        return "candidate_fail"
    has_odd = any(int(row["m"]) % 2 == 1 for row in passing)
    has_even = any(int(row["m"]) % 2 == 0 for row in passing)
    low_layer_only = all(row.get("low_layer_only", False) for row in passing)
    if has_odd and has_even and low_layer_only:
        return "promising_pattern"
    return "candidate_pass"


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan a candidate rule across multiple m values.")
    parser.add_argument("--dim", type=int, default=4, help="torus dimension d")
    parser.add_argument(
        "--m-list",
        default="5,6,8,10,12",
        help="comma-separated list of m values to scan",
    )
    parser.add_argument("--module", type=Path, help="Python module defining direction_tuple")
    parser.add_argument("--function", default="direction_tuple", help="rule function name")
    parser.add_argument("--witness-json", type=Path, help="JSON witness emitted by torus_nd_exact_search.py")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("artifacts/4d_generalization"),
        help="artifact output directory",
    )
    args = parser.parse_args()

    if args.module is None and args.witness_json is None:
        raise SystemExit("Provide either --module or --witness-json.")

    m_values = _parse_m_list(args.m_list)
    if any(m < 2 for m in m_values):
        raise SystemExit("All m values must be >= 2.")

    slug = _slug_from_source(args.module, args.function, args.witness_json)
    out_dir = args.out_dir / f"d{args.dim}_{slug}"
    out_dir.mkdir(parents=True, exist_ok=True)

    factory = load_rule_factory(args.module, args.function) if args.module is not None else None
    results: List[Dict[str, object]] = []

    for m in m_values:
        if args.witness_json is not None:
            rule = load_witness_rule(args.witness_json, args.dim, m)
            rule_source = f"witness:{args.witness_json}"
        else:
            assert factory is not None
            rule = factory(args.dim, m)
            rule_source = f"{args.module}:{args.function}"

        report = validate_rule(args.dim, m, rule)
        report["rule_source"] = rule_source
        report["classification"] = _classify_instance(report)
        report["parity"] = "even" if m % 2 == 0 else "odd"
        report["m_mod_6"] = m % 6
        report["m_mod_12"] = m % 12

        if report["rule_valid"]:
            direction_tuples = report["direction_tuples"]
            defect = defect_support_summary(args.dim, m, direction_tuples, canonical_direction_tuple(args.dim))
            p0_report = induced_p0_maps(report["nexts"], args.dim, m)
            report["defect_support"] = defect
            report["low_layer_only"] = defect["low_layer_only"]
            report["p0_report"] = p0_report
        else:
            report["low_layer_only"] = False

        json_path = out_dir / f"m{m}.json"
        json_path.write_text(json.dumps(report, indent=2, default=list))
        results.append(
            {
                "m": m,
                "classification": report["classification"],
                "parity": report["parity"],
                "m_mod_6": report["m_mod_6"],
                "m_mod_12": report["m_mod_12"],
                "rule_valid": report["rule_valid"],
                "all_hamilton": report.get("all_hamilton", False),
                "sign_product": report.get("sign_product"),
                "defect_vertex_count": report.get("defect_support", {}).get("defect_vertex_count"),
                "low_layer_only": report.get("low_layer_only", False),
                "json_path": str(json_path),
            }
        )

    family_status = _family_status(results)
    aggregate = {
        "dim": args.dim,
        "rule_source": f"{args.module}:{args.function}" if args.module is not None else f"witness:{args.witness_json}",
        "family_status": family_status,
        "results": results,
    }

    (out_dir / "summary.json").write_text(json.dumps(aggregate, indent=2))
    with (out_dir / "summary.jsonl").open("w", encoding="ascii") as fh:
        for row in results:
            fh.write(json.dumps(row) + "\n")
    with (out_dir / "summary.csv").open("w", newline="", encoding="ascii") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "m",
                "classification",
                "parity",
                "m_mod_6",
                "m_mod_12",
                "rule_valid",
                "all_hamilton",
                "sign_product",
                "defect_vertex_count",
                "low_layer_only",
                "json_path",
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    print(json.dumps({"out_dir": str(out_dir), "family_status": family_status, "runs": len(results)}, indent=2))


if __name__ == "__main__":
    main()
