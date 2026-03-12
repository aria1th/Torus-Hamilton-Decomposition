#!/usr/bin/env python3
"""Session 40 / artifact 020 symbolic carry-swap u-carry diagnostic for D5."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Dict, List, Mapping, Sequence, Tuple

TASK_ID = "D5-CARRY-SWAP-U-CARRY-020"
M_VALUES = (5, 7, 9, 11, 13, 15, 17, 19)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _is_perm(values: Sequence[int]) -> bool:
    return len(set(values)) == len(values)


def _binary_profile(mask: int, m: int) -> List[int]:
    return [(mask >> u) & 1 for u in range(m)]


def _binary_profile_perm_count(m: int) -> Dict[str, object]:
    valid_masks = []
    for mask in range(1 << m):
        beta = _binary_profile(mask, m)
        image = [(u + beta[u]) % m for u in range(m)]
        if _is_perm(image):
            valid_masks.append(mask)
    rows = []
    for mask in valid_masks:
        beta = _binary_profile(mask, m)
        rows.append({"mask": mask, "beta": beta, "kind": "constant" if len(set(beta)) == 1 else "nonconstant"})
    return {
        "m": m,
        "checked_profile_count": 1 << m,
        "permutation_profile_count": len(valid_masks),
        "profiles": rows,
        "conclusion": "For beta: Z_m -> {0,1}, the map u -> u + beta(u) is a permutation iff beta is constant.",
    }


def _candidate_specs(m: int) -> List[Dict[str, object]]:
    candidates: List[Tuple[str, str, Callable[[int, int], int], str]] = [
        (
            "none",
            "no carry swap",
            lambda s, u: 0,
            "beta(s,u)=0",
        ),
        (
            "all_carry_swapped",
            "swap 2->4 on every carry state; grouped selector from layer2 q=-1 bit",
            lambda s, u: 1,
            "beta(s,u)=1",
        ),
        (
            "w_plus_u_eq_2",
            "grouped selector induced by the layer2 current-state bit w+u=2",
            lambda s, u: 1 if s == 3 % m else 0,
            "beta(s,u)=1_{s=3}",
        ),
        (
            "q_plus_u_eq_1",
            "grouped selector induced by the layer2 current-state bit q+u=1",
            lambda s, u: 1 if u == 3 % m else 0,
            "beta(s,u)=1_{u=3}",
        ),
        (
            "q_plus_u_eq_neg1",
            "grouped selector induced by the layer2 current-state bit q+u=-1",
            lambda s, u: 1 if u == 1 % m else 0,
            "beta(s,u)=1_{u=1}",
        ),
        (
            "u_eq_neg1",
            "grouped selector induced by the layer2 current-state bit u=-1",
            lambda s, u: 1 if u == 0 else 0,
            "beta(s,u)=1_{u=0}",
        ),
    ]

    rows: List[Dict[str, object]] = []
    for name, description, beta_fn, formula in candidates:
        beta_rows = [[int(beta_fn(s, u)) for u in range(m)] for s in range(m)]
        depends_only_on_s = all(len(set(row)) == 1 for row in beta_rows)
        depends_only_on_u = all(
            beta_rows[s0][u] == beta_rows[s1][u]
            for u in range(m)
            for s0 in range(m)
            for s1 in range(m)
        )
        per_s_perm = []
        for s in range(m):
            image = [(u + beta_rows[s][u]) % m for u in range(m)]
            per_s_perm.append(_is_perm(image))
        base_image = [((s + 1) % m, (u + beta_rows[s][u]) % m) for s in range(m) for u in range(m)]
        is_base_perm = len(set(base_image)) == m * m

        row: Dict[str, object] = {
            "name": name,
            "description": description,
            "grouped_beta_formula": formula,
            "depends_only_on_s": depends_only_on_s,
            "depends_only_on_u": depends_only_on_u,
            "per_s_binary_profiles_are_permutations": per_s_perm,
            "base_map_is_permutation": is_base_perm,
        }

        if is_base_perm:
            orbit_summary = _orbit_summary(m, lambda s, u: ((s + 1) % m, (u + beta_rows[s][u]) % m))
            row["base_orbit_summary"] = orbit_summary
            row["d_dynamics_formula"] = "d' = d - 1 + 2*beta(s,u)"
            if depends_only_on_s:
                row["classification"] = "valid_but_still_one_dimensional_over_s"
                row["interpretation"] = (
                    "This selector yields a valid grouped base map, but beta depends only on s, so the result is "
                    "still a skew extension over the same one-dimensional base."
                )
            else:
                row["classification"] = "valid_and_candidate_second_coordinate"
                row["interpretation"] = (
                    "This would be a genuine new grouped base coordinate beyond s."
                )
        else:
            row["classification"] = "invalid_binary_single_swap"
            row["interpretation"] = (
                "This selector makes u -> u + beta_s(u) non-permutative for some s, so a single binary carry-swap "
                "with this grouped selector cannot define a valid grouped base map."
            )
        rows.append(row)
    return rows


def _orbit_summary(m: int, next_fn: Callable[[int, int], Tuple[int, int]]) -> Dict[str, object]:
    states = [(s, u) for s in range(m) for u in range(m)]
    visited = set()
    orbits = []
    for start in states:
        if start in visited:
            continue
        cur = start
        orbit = []
        while cur not in visited:
            visited.add(cur)
            orbit.append(cur)
            cur = next_fn(*cur)
        orbits.append(orbit)
    return {
        "orbit_count": len(orbits),
        "orbit_lengths": sorted(len(orbit) for orbit in orbits),
    }


def _paired_swap_example(m: int) -> Dict[str, object]:
    beta = [0] * m
    beta[0] = 1
    beta[1 % m] = -1
    image = [(u + beta[u]) % m for u in range(m)]
    return {
        "m": m,
        "beta_values": beta,
        "image": image,
        "is_permutation": _is_perm(image),
        "interpretation": (
            "A nonconstant ternary profile in {-1,0,1} can be a permutation. "
            "So a paired mechanism with both +1 and -1 shifts is structurally capable of producing a genuine "
            "second base coordinate, unlike a single binary carry-swap."
        ),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Diagnose carry-swap u-carry mechanisms for the D5 mixed witness.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    binary_rows = [_binary_profile_perm_count(m) for m in M_VALUES]
    candidate_rows = {str(m): _candidate_specs(m) for m in M_VALUES}
    ternary_examples = [_paired_swap_example(m) for m in M_VALUES]

    _write_json(out_dir / "binary_profile_permutation_counts.json", {"rows": binary_rows})
    _write_json(out_dir / "candidate_selector_classification.json", {"by_m": candidate_rows})
    _write_json(out_dir / "paired_swap_examples.json", {"rows": ternary_examples})

    summary = {
        "task_id": TASK_ID,
        "m_values": list(M_VALUES),
        "symbolic_family": {
            "first_return": (
                "R_psi(q,s,u,v)=(q+1, s+1+1_{q=m-2}, u+1+psi_carry*1_{q=m-2}, v+dv(q,s))"
            ),
            "grouped_return": "U_psi(s,u,v)=(s+1, u+Psi(s,u), v+phi(s))",
            "d_dynamics": "For d=u-w=2u-s, grouped return satisfies d' = d - 1 + 2*Psi(s,u).",
        },
        "binary_obstruction": (
            "If Psi(s,u) is binary-valued, then bijectivity of the grouped base map forces each profile "
            "u -> u + Psi(s,u) to be a permutation. Exhaustive checks on 5,7,9,11,13,15,17,19 confirm the exact "
            "lemma that for binary Psi this happens iff Psi is constant in u for each fixed s. Therefore a single "
            "binary carry-swap cannot create a genuine second grouped base coordinate."
        ),
        "candidate_selector_file": str(out_dir / "candidate_selector_classification.json"),
        "binary_profile_file": str(out_dir / "binary_profile_permutation_counts.json"),
        "paired_swap_example_file": str(out_dir / "paired_swap_examples.json"),
        "strongest_supported_conclusion": (
            "Single carry-slice binary 2->4 swaps split into two classes: selectors that depend only on s are valid "
            "but remain one-dimensional over the same base, while selectors that depend on a true second coordinate "
            "such as u make the grouped base map non-permutative. So the smallest viable next family is not a single "
            "binary carry-swap, but a paired or multi-valued mechanism capable of inducing a permutation on the "
            "second coordinate."
        ),
        "recommended_next_family": (
            "A coupled two-event family with both +1 and -1 relative u-shifts, e.g. a paired 2->4 and 4->2 "
            "mechanism, or an equivalent reduced family whose grouped second-coordinate update takes values in "
            "{-1,0,1} rather than only {0,1}."
        ),
    }
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2))

    print(f"task_id: {TASK_ID}")
    print("diagnosed binary carry-swap obstruction and next viable family.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
