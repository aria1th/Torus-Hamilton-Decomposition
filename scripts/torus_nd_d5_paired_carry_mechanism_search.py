#!/usr/bin/env python3
"""Reduced paired 4<->2 carry mechanism search for the D5 mixed witness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Dict, List, Mapping, Sequence, Tuple

TASK_ID = "D5-PAIRED-CARRY-MECHANISM-021"
M_VALUES = (5, 7, 9, 11, 13, 15, 17, 19)

SelectorFn = Callable[[int, int, int, int], int]


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _indicator(flag: bool) -> int:
    return 1 if flag else 0


def _selector_catalog() -> Dict[str, Tuple[str, SelectorFn]]:
    return {
        "none": ("0", lambda m, q, s, u: 0),
        "const1": ("1", lambda m, q, s, u: 1),
        "q_eq_neg1": ("1_{q=-1}", lambda m, q, s, u: _indicator(q == m - 1)),
        "w_plus_u_eq_2": ("1_{s=2}", lambda m, q, s, u: _indicator(s == 2 % m)),
        "q_plus_u_eq_1": ("1_{q+u=1}", lambda m, q, s, u: _indicator((q + u) % m == 1)),
        "q_plus_u_eq_neg1": ("1_{q+u=-1}", lambda m, q, s, u: _indicator((q + u) % m == m - 1)),
        "u_eq_neg1": ("1_{u=-1}", lambda m, q, s, u: _indicator(u == m - 1)),
    }


def _carry(q: int, m: int) -> int:
    return _indicator(q == m - 2)


def _dv_formula(q: int, s: int, m: int) -> int:
    return _indicator((q != m - 2 and s == 1) or (q == m - 2 and s != 0))


def _first_return(alpha_fn: SelectorFn, beta_fn: SelectorFn, *, q: int, s: int, u: int, m: int) -> Dict[str, int]:
    q1 = (q + 1) % m
    alpha = alpha_fn(m, q1, s, u)
    carry = _carry(q, m)

    # After layer 1, s increases by 1 regardless of whether the fixed 4 is swapped to 2.
    s2 = (s + 1) % m
    u2 = (u + 1 - alpha) % m

    beta = beta_fn(m, q1, s2, u2)

    s_next = (s + 1 + carry) % m
    u_next = (u + 1 - alpha + carry * beta) % m
    return {
        "q_next": q1,
        "s_next": s_next,
        "u_next": u_next,
        "alpha": alpha,
        "beta": beta,
        "carry": carry,
        "dv": _dv_formula(q, s, m),
    }


def _grouped_base(alpha_fn: SelectorFn, beta_fn: SelectorFn, m: int) -> Dict[str, object]:
    next_map: Dict[Tuple[int, int], Tuple[int, int]] = {}
    psi_values: Dict[Tuple[int, int], int] = {}

    for s0 in range(m):
        for u0 in range(m):
            q = 0
            s = s0
            u = u0
            for _ in range(m):
                step = _first_return(alpha_fn, beta_fn, q=q, s=s, u=u, m=m)
                q = step["q_next"]
                s = step["s_next"]
                u = step["u_next"]
            next_map[(s0, u0)] = (s, u)
            psi_values[(s0, u0)] = (u - u0) % m

    states = [(s, u) for s in range(m) for u in range(m)]
    is_perm = len(set(next_map.values())) == len(states)
    psi_depends_only_on_s = True
    for s in range(m):
        vals = {psi_values[(s, u)] for u in range(m)}
        if len(vals) != 1:
            psi_depends_only_on_s = False
            break

    orbit_lengths: List[int] = []
    if is_perm:
        visited = set()
        for start in states:
            if start in visited:
                continue
            cur = start
            orbit = []
            while cur not in visited:
                visited.add(cur)
                orbit.append(cur)
                cur = next_map[cur]
            orbit_lengths.append(len(orbit))
        orbit_lengths.sort()

    sample_rows = []
    for s in range(min(m, 5)):
        for u in range(min(m, 5)):
            nxt = next_map[(s, u)]
            sample_rows.append(
                {"s": s, "u": u, "next_s": nxt[0], "next_u": nxt[1], "Psi": psi_values[(s, u)]}
            )

    return {
        "is_permutation": is_perm,
        "psi_depends_only_on_s": psi_depends_only_on_s,
        "orbit_lengths": orbit_lengths,
        "orbit_count": len(orbit_lengths),
        "sample_rows": sample_rows,
    }


def _search_for_m(m: int) -> Dict[str, object]:
    catalog = _selector_catalog()
    good_rows = []
    all_rows = []
    for alpha_name, (alpha_formula, alpha_fn) in catalog.items():
        for beta_name, (beta_formula, beta_fn) in catalog.items():
            base = _grouped_base(alpha_fn, beta_fn, m)
            row = {
                "alpha_name": alpha_name,
                "alpha_formula": alpha_formula,
                "beta_name": beta_name,
                "beta_formula": beta_formula,
                **base,
            }
            if row["is_permutation"]:
                if row["psi_depends_only_on_s"]:
                    row["classification"] = "valid_but_s_only"
                else:
                    row["classification"] = "valid_genuine_2d_candidate"
                    good_rows.append(row)
            else:
                row["classification"] = "invalid"
            all_rows.append(row)

    return {
        "m": m,
        "total_pairs": len(all_rows),
        "valid_pair_count": sum(1 for row in all_rows if row["is_permutation"]),
        "valid_genuine_2d_count": len(good_rows),
        "best_rows": sorted(
            [row for row in all_rows if row["is_permutation"]],
            key=lambda row: (
                row["psi_depends_only_on_s"],
                row["orbit_count"],
                -max(row["orbit_lengths"] or [0]),
                row["alpha_name"],
                row["beta_name"],
            ),
        )[:20],
        "genuine_2d_rows": good_rows[:20],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the reduced paired carry mechanism family for D5.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [_search_for_m(m) for m in M_VALUES]
    _write_json(out_dir / "paired_selector_search.json", {"rows": rows})

    any_2d = any(row["valid_genuine_2d_count"] > 0 for row in rows)
    summary = {
        "task_id": TASK_ID,
        "m_values": list(M_VALUES),
        "search_file": str(out_dir / "paired_selector_search.json"),
        "strongest_supported_conclusion": (
            "In the reduced paired family with a layer-1 4->2 selector alpha and a carry-slice 2->4 selector beta, "
            "there are valid permutation maps that genuinely depend on a second coordinate beyond s."
            if any_2d
            else
            "In the searched reduced paired family built from the standard one-bit atoms, no genuine second-coordinate "
            "grouped base map appears; all valid pairs still collapse to s-only grouped u-cocycles."
        ),
        "any_genuine_2d_candidate": any_2d,
    }
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2))

    print(f"task_id: {TASK_ID}")
    print("searched reduced paired carry mechanism family.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
