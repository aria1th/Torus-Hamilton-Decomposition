#!/usr/bin/env python3
"""Search a richer affine paired carry mechanism family for the D5 mixed witness."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

TASK_ID = "D5-AFFINE-PAIRED-CARRY-SEARCH-022"
M_VALUES = (5, 7, 9, 11, 13, 15, 17, 19)
PILOT_M = 11
T_VALUES = (-3, -2, -1, 0, 1, 2, 3)
COEFF_VALUES = (-1, 0, 1)


@dataclass(frozen=True)
class SelectorSpec:
    name: str
    formula: str
    kind: str
    coeffs: Tuple[int, int, int] | None = None
    target: int | None = None


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _indicator(flag: bool) -> int:
    return 1 if flag else 0


def _normalize_affine(coeffs: Tuple[int, int, int], target: int) -> Tuple[Tuple[int, int, int], int]:
    a, b, c = coeffs
    for entry in coeffs:
        if entry == 0:
            continue
        if entry < 0:
            return (-a, -b, -c), -target
        break
    return coeffs, target


def _var_term(name: str, coeff: int) -> str | None:
    if coeff == 0:
        return None
    if coeff == 1:
        return name
    if coeff == -1:
        return f"-{name}"
    return f"{coeff}*{name}"


def _affine_formula(coeffs: Tuple[int, int, int], target: int) -> str:
    terms = [term for term in (_var_term("q", coeffs[0]), _var_term("s", coeffs[1]), _var_term("u", coeffs[2])) if term]
    expr = " + ".join(terms).replace("+ -", "- ")
    return f"1_{{{expr}={target}}}"


def _affine_name(coeffs: Tuple[int, int, int], target: int) -> str:
    coeff_tag = "_".join(f"{entry:+d}".replace("+", "p").replace("-", "n") for entry in coeffs)
    target_tag = f"{target:+d}".replace("+", "p").replace("-", "n")
    return f"aff_{coeff_tag}_eq_{target_tag}"


def _selector_catalog() -> List[SelectorSpec]:
    catalog: List[SelectorSpec] = [
        SelectorSpec(name="none", formula="0", kind="const"),
        SelectorSpec(name="const1", formula="1", kind="const"),
    ]
    seen = set()
    for a in COEFF_VALUES:
        for b in COEFF_VALUES:
            for c in COEFF_VALUES:
                if (a, b, c) == (0, 0, 0):
                    continue
                for target in T_VALUES:
                    coeffs, normalized_target = _normalize_affine((a, b, c), target)
                    key = (coeffs, normalized_target)
                    if key in seen:
                        continue
                    seen.add(key)
                    catalog.append(
                        SelectorSpec(
                            name=_affine_name(coeffs, normalized_target),
                            formula=_affine_formula(coeffs, normalized_target),
                            kind="affine",
                            coeffs=coeffs,
                            target=normalized_target,
                        )
                    )
    return catalog


def _selector_value(spec: SelectorSpec, *, q: int, s: int, u: int, m: int) -> int:
    if spec.kind == "const":
        return 0 if spec.name == "none" else 1
    assert spec.coeffs is not None
    assert spec.target is not None
    a, b, c = spec.coeffs
    return _indicator((a * q + b * s + c * u - spec.target) % m == 0)


def _table_index(m: int, q: int, s: int, u: int) -> int:
    return (q * m + s) * m + u


def _precompute_tables(m: int, specs: Sequence[SelectorSpec]) -> Dict[str, bytearray]:
    size = m * m * m
    tables: Dict[str, bytearray] = {}
    for spec in specs:
        table = bytearray(size)
        for q in range(m):
            for s in range(m):
                base = _table_index(m, q, s, 0)
                for u in range(m):
                    table[base + u] = _selector_value(spec, q=q, s=s, u=u, m=m)
        tables[spec.name] = table
    return tables


def _phi(s: int, m: int) -> int:
    return (2 + _indicator(s == 1) - 2 * _indicator(s == 2 % m) - _indicator(s == 3 % m)) % m


def _grouped_map(m: int, alpha_table: bytearray, beta_table: bytearray) -> Dict[str, object]:
    states = [(s, u) for s in range(m) for u in range(m)]
    next_map: Dict[Tuple[int, int], Tuple[int, int]] = {}
    psi_values: Dict[Tuple[int, int], int] = {}
    image_seen = set()
    psi_depends_only_on_s = True
    orbit_lengths: List[int] = []

    for s0 in range(m):
        row_values = set()
        for u0 in range(m):
            q = 0
            s = s0
            u = u0
            for _ in range(m):
                q1 = (q + 1) % m
                alpha = alpha_table[_table_index(m, q1, s, u)]
                s2 = (s + 1) % m
                u2 = (u + 1 - alpha) % m
                beta = beta_table[_table_index(m, q1, s2, u2)]
                carry = 1 if q == m - 2 else 0
                s = (s + 1 + carry) % m
                u = (u + 1 - alpha + carry * beta) % m
                q = q1
            next_state = (s, u)
            next_map[(s0, u0)] = next_state
            psi = (u - u0) % m
            psi_values[(s0, u0)] = psi
            row_values.add(psi)
            image_seen.add(next_state)
        if len(row_values) != 1:
            psi_depends_only_on_s = False

    is_permutation = len(image_seen) == len(states)

    if is_permutation:
        visited = set()
        for start in states:
            if start in visited:
                continue
            cur = start
            orbit_length = 0
            while cur not in visited:
                visited.add(cur)
                orbit_length += 1
                cur = next_map[cur]
            orbit_lengths.append(orbit_length)
        orbit_lengths.sort()

    sample_rows = []
    for s in range(min(m, 4)):
        for u in range(min(m, 4)):
            nxt = next_map[(s, u)]
            sample_rows.append(
                {
                    "s": s,
                    "u": u,
                    "next_s": nxt[0],
                    "next_u": nxt[1],
                    "Psi": psi_values[(s, u)],
                }
            )

    return {
        "is_permutation": is_permutation,
        "psi_depends_only_on_s": psi_depends_only_on_s,
        "orbit_count": len(orbit_lengths),
        "orbit_lengths": orbit_lengths,
        "sample_rows": sample_rows,
        "psi_by_s": [
            {
                "s": s,
                "values": sorted({psi_values[(s, u)] for u in range(m)}),
            }
            for s in range(m)
        ],
    }


def _grouped_full_orbit_summary(
    m: int,
    alpha_table: bytearray,
    beta_table: bytearray,
) -> Dict[str, object]:
    visited = set()
    orbit_lengths: List[int] = []
    for s0 in range(m):
        for u0 in range(m):
            for v0 in range(m):
                start = (s0, u0, v0)
                if start in visited:
                    continue
                cur = start
                orbit_length = 0
                while cur not in visited:
                    visited.add(cur)
                    s, u, v = cur
                    base = _grouped_map_single_step(m, alpha_table, beta_table, s, u)
                    cur = (base[0], base[1], (v + _phi(s, m)) % m)
                    orbit_length += 1
                orbit_lengths.append(orbit_length)
    orbit_lengths.sort()
    return {
        "orbit_count": len(orbit_lengths),
        "orbit_lengths": orbit_lengths,
    }


def _grouped_map_single_step(
    m: int,
    alpha_table: bytearray,
    beta_table: bytearray,
    s0: int,
    u0: int,
) -> Tuple[int, int]:
    q = 0
    s = s0
    u = u0
    for _ in range(m):
        q1 = (q + 1) % m
        alpha = alpha_table[_table_index(m, q1, s, u)]
        s2 = (s + 1) % m
        u2 = (u + 1 - alpha) % m
        beta = beta_table[_table_index(m, q1, s2, u2)]
        carry = 1 if q == m - 2 else 0
        s = (s + 1 + carry) % m
        u = (u + 1 - alpha + carry * beta) % m
        q = q1
    return s, u


def _evaluate_pair(
    alpha_spec: SelectorSpec,
    beta_spec: SelectorSpec,
    *,
    m: int,
    tables: Mapping[str, bytearray],
    include_full_orbits: bool,
) -> Dict[str, object]:
    alpha_table = tables[alpha_spec.name]
    beta_table = tables[beta_spec.name]
    grouped = _grouped_map(m, alpha_table, beta_table)
    row: Dict[str, object] = {
        "alpha_name": alpha_spec.name,
        "alpha_formula": alpha_spec.formula,
        "beta_name": beta_spec.name,
        "beta_formula": beta_spec.formula,
        **grouped,
    }
    if not grouped["is_permutation"]:
        row["classification"] = "invalid"
        if include_full_orbits:
            row["full_grouped_orbits"] = None
        return row
    if grouped["psi_depends_only_on_s"]:
        row["classification"] = "valid_but_s_only"
    else:
        row["classification"] = "valid_genuine_2d_candidate"
    if include_full_orbits:
        row["full_grouped_orbits"] = _grouped_full_orbit_summary(m, alpha_table, beta_table)
    return row


def _pilot_search(specs: Sequence[SelectorSpec]) -> Dict[str, object]:
    tables = _precompute_tables(PILOT_M, specs)
    rows: List[Dict[str, object]] = []
    genuine_rows: List[Dict[str, object]] = []
    valid_rows: List[Dict[str, object]] = []

    for alpha_spec in specs:
        for beta_spec in specs:
            row = _evaluate_pair(alpha_spec, beta_spec, m=PILOT_M, tables=tables, include_full_orbits=False)
            rows.append(row)
            if row["is_permutation"]:
                valid_rows.append(row)
                if row["classification"] == "valid_genuine_2d_candidate":
                    genuine_rows.append(row)

    valid_rows.sort(
        key=lambda row: (
            row["classification"] != "valid_genuine_2d_candidate",
            row["orbit_count"],
            -max(row["orbit_lengths"] or [0]),
            row["alpha_name"],
            row["beta_name"],
        )
    )

    return {
        "pilot_m": PILOT_M,
        "total_pairs": len(rows),
        "valid_pair_count": len(valid_rows),
        "valid_genuine_2d_count": len(genuine_rows),
        "genuine_rows": genuine_rows[:40],
        "best_valid_rows": valid_rows[:60],
    }


def _crosscheck_candidates(specs: Sequence[SelectorSpec], pilot_rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    spec_by_name = {spec.name: spec for spec in specs}
    candidate_keys = [(row["alpha_name"], row["beta_name"]) for row in pilot_rows]
    per_pair_rows = []

    for alpha_name, beta_name in candidate_keys:
        alpha_spec = spec_by_name[alpha_name]
        beta_spec = spec_by_name[beta_name]
        per_m = []
        stable_genuine = True
        for m in M_VALUES:
            tables = _precompute_tables(m, (alpha_spec, beta_spec))
            row = _evaluate_pair(alpha_spec, beta_spec, m=m, tables=tables, include_full_orbits=True)
            per_m.append(
                {
                    "m": m,
                    "classification": row["classification"],
                    "orbit_count": row["orbit_count"],
                    "orbit_lengths": row["orbit_lengths"],
                    "psi_by_s": row["psi_by_s"],
                    "full_grouped_orbits": row["full_grouped_orbits"],
                }
            )
            stable_genuine = stable_genuine and row["classification"] == "valid_genuine_2d_candidate"
        per_pair_rows.append(
            {
                "alpha_name": alpha_name,
                "alpha_formula": alpha_spec.formula,
                "beta_name": beta_name,
                "beta_formula": beta_spec.formula,
                "stable_genuine_candidate": stable_genuine,
                "per_m": per_m,
            }
        )

    return {
        "candidate_pair_count": len(per_pair_rows),
        "stable_genuine_candidate_count": sum(1 for row in per_pair_rows if row["stable_genuine_candidate"]),
        "rows": per_pair_rows,
    }


def _summary_from_results(pilot: Mapping[str, object], crosscheck: Mapping[str, object]) -> Dict[str, object]:
    stable_count = crosscheck["stable_genuine_candidate_count"]
    if stable_count > 0:
        conclusion = (
            "The first richer affine selector family already contains stable genuine two-coordinate grouped base "
            "candidates beyond the old s-only collapse."
        )
        recommendation = (
            "Focus next on the stable affine candidate pairs, derive their grouped base law symbolically, and then "
            "look for realizable local bits matching those selector surfaces."
        )
    elif pilot["valid_genuine_2d_count"] > 0:
        conclusion = (
            "Some affine selector pairs produce genuine two-coordinate grouped base maps at the pilot modulus, but "
            "none stay stable across the checked odd moduli."
        )
        recommendation = (
            "Treat affine selector surfaces as a pilot-only phenomenon and move next to stronger non-affine or "
            "predecessor-style selectors."
        )
    else:
        conclusion = (
            "Even the first affine one-surface paired family fails to produce a genuine two-coordinate grouped base "
            "map at the pilot modulus; all valid pairs still collapse to s-only grouped u-cocycles."
        )
        recommendation = (
            "Stop expecting single affine selector surfaces to be enough. The next viable perturbation should use a "
            "richer non-affine controller, an exact predecessor / tail bit, or a genuinely multi-surface rule."
        )
    return {
        "task_id": TASK_ID,
        "pilot_m": PILOT_M,
        "checked_m_values": list(M_VALUES),
        "pilot_valid_genuine_2d_count": pilot["valid_genuine_2d_count"],
        "stable_genuine_candidate_count": stable_count,
        "strongest_supported_conclusion": conclusion,
        "recommended_next_family": recommendation,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search affine paired carry selectors for the D5 mixed witness.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    specs = _selector_catalog()
    _write_json(
        out_dir / "selector_catalog.json",
        {
            "selector_count": len(specs),
            "rows": [
                {
                    "name": spec.name,
                    "formula": spec.formula,
                    "kind": spec.kind,
                    "coeffs": list(spec.coeffs) if spec.coeffs is not None else None,
                    "target": spec.target,
                }
                for spec in specs
            ],
        },
    )

    pilot = _pilot_search(specs)
    _write_json(out_dir / "pilot_search_summary.json", pilot)

    pilot_candidates = pilot["genuine_rows"] if pilot["genuine_rows"] else pilot["best_valid_rows"][:12]
    crosscheck = _crosscheck_candidates(specs, pilot_candidates)
    _write_json(out_dir / "crosscheck_candidates.json", crosscheck)

    summary = _summary_from_results(pilot, crosscheck)
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    print(f"selector_count: {len(specs)}")
    print(f"pilot_valid_genuine_2d_count: {pilot['valid_genuine_2d_count']}")
    print(f"stable_genuine_candidate_count: {crosscheck['stable_genuine_candidate_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
