#!/usr/bin/env python3
"""Session 38 / artifact 019 symbolic normal-form and u-obstruction analysis for the D5 mixed witness."""

from __future__ import annotations

import argparse
import json
from math import gcd
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

from torus_nd_d5_return_map_model_common import (
    environment_block,
    extract_first_return_table,
    extract_grouped_return,
    load_witness_specs,
    prepare_witness,
    runtime_since,
)

TASK_ID = "D5-MIXED-NORMAL-FORM-AND-U-OBSTRUCTION-019"
M_VALUES = (5, 7, 9, 11, 13, 15, 17, 19)


def _indicator(flag: bool) -> int:
    return 1 if flag else 0


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _phi_formula(s: int, m: int) -> int:
    return (2 + _indicator(s == 1) - 2 * _indicator(s == 2) - _indicator(s == 3)) % m


def _phi_local_formula(s: int, m: int) -> int:
    return (2 - 2 * _indicator(s == 2)) % m


def _phi_pure_formula(s: int, m: int) -> int:
    return (-2 * _indicator(s == 2)) % m


def _carry(q: int, m: int) -> int:
    return _indicator(q == m - 2)


def _dv_formula(q: int, s: int, m: int) -> int:
    return _indicator((q != m - 2 and s == 1) or (q == m - 2 and s != 0))


def _first_return_formula(q: int, s: int, u: int, v: int, m: int) -> Tuple[int, int, int, int]:
    carry = _carry(q, m)
    dv = _dv_formula(q, s, m)
    return ((q + 1) % m, (s + 1 + carry) % m, (u + 1) % m, (v + dv) % m)


def _grouped_return_formula(s: int, u: int, v: int, m: int) -> Tuple[int, int, int]:
    return ((s + 1) % m, u, (v + _phi_formula(s, m)) % m)


def _rule_derivation(spec_payload: Mapping[str, object]) -> Dict[str, object]:
    return {
        "witness_rule": spec_payload,
        "derived_coordinates": {
            "section_state": "(q,w,v,u) with x0=-q-w-v-u",
            "reduced_first_return_state": "(q,s,u,v) with s=w+u",
            "grouped_state": "(s,u,v)",
        },
        "derivation_steps": [
            "At layer 0 the rule always moves in direction 1, so q increases by 1.",
            "At layer 1 the rule always moves in direction 4, so u increases by 1.",
            "At layer 2 the rule uses old bit q=-1 after layer 0, hence w gains the carry 1_{q=m-2}.",
            "For color 0, pred_sig1_wu2 checks the predecessor in direction 1, which leaves w and u unchanged.",
            "Therefore the layer-3 predecessor flag is exactly p=1 iff current w+u equals 2.",
            "After layers 0 and 1 and the layer-2 carry, current w+u is s+1+1_{q=m-2}.",
            "The layer-3 tables are 0/3 and 3/0, so direction 3 is chosen exactly when q_oldbit XOR p equals 1.",
            "Hence dv(q,s)=1 iff ((q!=m-2 and s=1) or (q=m-2 and s!=0)).",
            "Summing dv around one grouped cycle starting at q=0 yields phi(s)=2+1_{s=1}-2*1_{s=2}-1_{s=3}.",
            "Grouped return therefore preserves u and acts as a skew-odometer on (s,v).",
        ],
        "exact_formulas": {
            "carry": "carry(q)=1_{q=m-2}",
            "predecessor_flag": "p(q,s)=1 iff s+1+1_{q=m-2}=2 (mod m)",
            "dv": "dv(q,s)=1 iff ((q!=m-2 and s=1) or (q=m-2 and s!=0))",
            "R": "R(q,s,u,v)=(q+1, s+1+1_{q=m-2}, u+1, v+dv(q,s))",
            "phi": "phi(s)=2+1_{s=1}-2*1_{s=2}-1_{s=3} (mod m)",
            "U": "U(s,u,v)=(s+1, u, v+phi(s))",
            "phi_after_local_gauge": "2-2*1_{s=2} (mod m)",
            "phi_pure_one_defect": "-2*1_{s=2} (mod m)",
        },
    }


def _verify_direct_replay_for_m(first_return: Mapping[str, object], grouped_return: Mapping[str, object], *, m: int) -> Dict[str, object]:
    first_rows = first_return["states"]
    grouped_rows = grouped_return["states"]

    for row in first_rows.values():
        q = int(row["q"])
        w = int(row["w"])
        u = int(row["u"])
        s = (w + u) % m
        carry = _carry(q, m)
        expected_next = [(q + 1) % m, (w + carry) % m, (u + 1) % m]
        expected_dv = _dv_formula(q, s, m)
        expected_low_word = [1, 4, 2 if carry else 0, 3 if expected_dv else 0]
        if list(row["next_state"]) != expected_next:
            raise AssertionError(
                f"first-return next_state mismatch at m={m}, state={(q,w,u)}: "
                f"actual={row['next_state']} expected={expected_next}"
            )
        if int(row["dv"]) != expected_dv:
            raise AssertionError(
                f"first-return dv mismatch at m={m}, state={(q,w,u)}: "
                f"actual={row['dv']} expected={expected_dv}"
            )
        if list(row["representative_low_layer_word"]) != expected_low_word:
            raise AssertionError(
                f"first-return low word mismatch at m={m}, state={(q,w,u)}: "
                f"actual={row['representative_low_layer_word']} expected={expected_low_word}"
            )

    for row in grouped_rows.values():
        w = int(row["w"])
        u = int(row["u"])
        s = (w + u) % m
        expected_next = [(w + 1) % m, u]
        expected_phi = _phi_formula(s, m)
        if list(row["next_state"]) != expected_next:
            raise AssertionError(
                f"grouped next_state mismatch at m={m}, state={(w,u)}: "
                f"actual={row['next_state']} expected={expected_next}"
            )
        if int(row["phi"]) != expected_phi:
            raise AssertionError(
                f"grouped phi mismatch at m={m}, state={(w,u)}: actual={row['phi']} expected={expected_phi}"
            )

    phi_values = [_phi_formula(s, m) for s in range(m)]
    local_values = [_phi_local_formula(s, m) for s in range(m)]
    pure_values = [_phi_pure_formula(s, m) for s in range(m)]
    return {
        "m": m,
        "first_return_state_count": int(first_return["state_count"]),
        "grouped_state_count": int(grouped_return["state_count"]),
        "phi_values": phi_values,
        "phi_after_local_gauge": local_values,
        "phi_pure_one_defect": pure_values,
        "cycle_sum": sum(phi_values) % m,
        "expected_cycle_sum": (m - 2) % m,
    }


def _grouped_orbit_summary(m: int) -> Dict[str, object]:
    next_map = {
        (s, v): ((s + 1) % m, (v + _phi_formula(s, m)) % m)
        for s in range(m)
        for v in range(m)
    }
    visited = set()
    orbits: List[List[Tuple[int, int]]] = []
    for start in sorted(next_map):
        if start in visited:
            continue
        cur = start
        orbit = []
        while cur not in visited:
            visited.add(cur)
            orbit.append(cur)
            cur = next_map[cur]
        orbits.append(orbit)

    translation_after_cycle = sum(_phi_formula(s, m) for s in range(m)) % m
    return {
        "m": m,
        "orbit_count_per_fixed_u": len(orbits),
        "orbit_lengths_per_fixed_u": sorted(len(orbit) for orbit in orbits),
        "translation_after_m_steps": translation_after_cycle,
        "gcd_of_translation_and_m": gcd(translation_after_cycle, m),
        "single_orbit_on_fixed_u": len(orbits) == 1 and len(orbits[0]) == m * m,
        "proof_summary": (
            "U^m acts by v -> v + (sum_s phi(s)) = v - 2. "
            "For odd m, gcd(m,2)=1, so this translation is cyclic on v and combines with s -> s+1 "
            "to give one orbit of length m^2 on each fixed-u fiber."
        ),
    }


def _control_interpretation() -> Dict[str, object]:
    rows = json.loads(
        Path("artifacts/d5_mixed_skew_odometer_normal_form_018/data/control_comparison.json").read_text()
    )["rows"]
    out_rows = []
    for row in rows:
        witness = row["witness"]
        if witness == "monodromy_008":
            interpretation = "degenerate affine case: grouped quotient collapses to one state, so there is no active odometer base"
        else:
            interpretation = "does not collapse to the s-only grouped model, so it does not realize the mixed skew-odometer normal form"
        out_rows.append(
            {
                "witness": witness,
                "m": int(row["m"]),
                "quotient_R_class_count": int(row["quotient_R_class_count"]),
                "quotient_U_class_count": int(row["quotient_U_class_count"]),
                "grouped_output_depends_only_on_s": bool(row["grouped_output_depends_only_on_s"]),
                "grouped_model_kind": row["grouped_model_kind"],
                "interpretation": interpretation,
            }
        )
    return {"rows": out_rows}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Derive and verify the D5 mixed normal form and grouped u-obstruction.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    start = __import__("time").perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    specs = {spec.name: spec for spec in load_witness_specs()}
    mixed = specs["mixed_008"]
    prepared = prepare_witness(mixed, M_VALUES)

    derivation = _rule_derivation(mixed.rule_payload)
    _write_json(out_dir / "symbolic_derivation.json", derivation)

    verification_rows = []
    for m in M_VALUES:
        pre = prepared.pre_by_m[m]
        nexts0 = prepared.nexts0_by_m[m]
        dir_row = prepared.dir_by_m[m]
        first_return = extract_first_return_table(pre, nexts0, dir_row)
        grouped_return = extract_grouped_return(first_return)
        verification = _verify_direct_replay_for_m(first_return, grouped_return, m=m)
        verification_rows.append(verification)

    grouped_orbits = {"rows": [_grouped_orbit_summary(m) for m in M_VALUES]}
    controls = _control_interpretation()
    _write_json(out_dir / "direct_replay_verification.json", {"rows": verification_rows})
    _write_json(out_dir / "grouped_orbit_summary.json", grouped_orbits)
    _write_json(out_dir / "control_interpretation.json", controls)

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "m_values": list(M_VALUES),
        "rule_derived_facts_file": str(out_dir / "symbolic_derivation.json"),
        "replay_verified_facts_file": str(out_dir / "direct_replay_verification.json"),
        "grouped_orbit_summary_file": str(out_dir / "grouped_orbit_summary.json"),
        "control_interpretation_file": str(out_dir / "control_interpretation.json"),
        "exact_reduced_coordinates": {
            "first_return": "(q,s,u,v) with s=w+u mod m",
            "grouped_return": "(s,u,v)",
        },
        "exact_formulas": derivation["exact_formulas"],
        "obstruction_statement": (
            "Grouped return already factors as identity on u times a one-defect skew-odometer on (s,v); "
            "the remaining obstruction is the absence of grouped u-carry."
        ),
        "strongest_supported_conclusion": (
            "For mixed_008, the witness rule itself explains the reduced normal form: "
            "R(q,s,u,v)=(q+1, s+1+1_{q=m-2}, u+1, v+dv(q,s)) and "
            "U(s,u,v)=(s+1, u, v+phi(s)) with phi(s) cohomologous to -2*1_{s=2}. "
            "For each odd checked m, every fixed-u grouped fiber is a single orbit on (s,v), "
            "so the exact remaining obstruction is grouped u-invariance."
        ),
        "remaining_gap": (
            "The derivation is explicit and replay-verified but still written as proof-supporting computation; "
            "it has not yet been formalized as a manuscript theorem or Lean proof."
        ),
    }
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2))

    print(f"task_id: {TASK_ID}")
    print(f"runtime_sec: {summary['runtime_sec']:.3f}")
    print("derived mixed_008 normal form and grouped u-obstruction.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
