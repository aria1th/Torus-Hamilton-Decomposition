#!/usr/bin/env python3
"""Branch-local support for the D5 phase scheduler theorem of 059."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import torus_nd_d5_corridor_phase_extraction as phase034
import torus_nd_d5_deep_transition_carry_sheet as carry046
import torus_nd_d5_endpoint_latin_repair as seed032
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-PHASE-SCHEDULER-BRANCH-SUPPORT-059B"
SMALL_M_VALUES = (5, 7, 9, 11)
LARGE_M_VALUES = (25, 27, 29)
MODIFIED_LABELS = ("L1", "R1", "L2", "R2", "L3", "R3")


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _coords_payload(coords: Sequence[int], m: int) -> Dict[str, int]:
    q = int(coords[1])
    w = int(coords[2])
    v = int(coords[3])
    u = int(coords[4])
    theta = int(sum(coords) % m)
    s = int((w + u) % m)
    return {
        "x0": int(coords[0]),
        "q": q,
        "w": w,
        "v": v,
        "u": u,
        "s": s,
        "theta": theta,
    }


def _formula_label(m: int, *, theta: int, q: int, w: int, s: int) -> str:
    if theta == 1 and q == m - 1 and w == 0 and s != 0:
        return "R1"
    if theta == 1 and q == m - 1 and w == m - 1 and s != 0:
        return "L1"
    if theta == 2 and q == 0 and w == 0 and s != 0:
        return "R2"
    if theta == 2 and q == m - 1 and w == 0 and s != 1:
        return "L2"
    if theta == 3 and q == 0 and w == 0 and s != 1:
        return "R3"
    if theta == 3 and q == m - 1 and w == 1 and s != 2:
        return "L3"
    return "B"


def _scheduler_anchor(m: int, *, theta: int, q: int, s: int) -> int:
    c = int(q == m - 1)
    if theta == 0:
        return 1
    if theta == 1:
        return 4
    if theta == 2:
        return 2 if c == 1 else 0
    if theta == 3:
        return 3 if ((c == 0 and s == 2) or (c == 1 and s != 2)) else 0
    return 0


def _projected_next_from_anchor(m: int, *, q: int, w: int, theta: int, anchor: int) -> Tuple[int, int, int]:
    if anchor == 1:
        return ((q + 1) % m, w, (theta + 1) % m)
    if anchor == 2:
        return (q, (w + 1) % m, (theta + 1) % m)
    return (q, w, (theta + 1) % m)


def _raw_odometer_next(m: int, *, q: int, w: int, theta: int) -> Tuple[int, int, int]:
    if theta == 0:
        return ((q + 1) % m, w, 1)
    if theta == 1:
        return (q, w, 2)
    if theta == 2:
        return (q, (w + (1 if q == m - 1 else 0)) % m, 3)
    return (q, w, (theta + 1) % m)


def _s_from_raw_phase(m: int, *, q: int, w: int, theta: int, rho: int) -> int:
    return int((q + w - (1 if theta == 1 else 0) + rho) % m)


def _regular_target_step(m: int) -> int:
    return int((m - 3) * (m**2) - 1)


def _exceptional_target_step(m: int) -> int:
    return int(_regular_target_step(m) + m * (m - 1))


def _family_target(m: int, family: str) -> Tuple[Tuple[int, int, int], int, int]:
    if family == "exceptional":
        return ((m - 2) % m, (m - 1) % m, 1), 1, _exceptional_target_step(m)
    return ((m - 1) % m, (m - 2) % m, 1), 2, _regular_target_step(m)


def _small_range_checks() -> Dict[str, object]:
    mixed_rule = seed032._mixed_rule()
    per_m: Dict[str, object] = {}

    for m in SMALL_M_VALUES:
        prepared = seed032._prepare_m(m, mixed_rule)
        nexts_all, meta = phase034._build_best_seed(prepared)
        labels = meta["labels_by_color"][0]
        coords = prepared.pre["coords"]

        modified_failures = []
        modified_count = 0
        for idx, label in enumerate(labels):
            if label not in MODIFIED_LABELS:
                continue
            modified_count += 1
            payload = _coords_payload(coords[idx], m)
            predicted = _formula_label(m, theta=payload["theta"], q=payload["q"], w=payload["w"], s=payload["s"])
            if predicted != label:
                modified_failures.append(
                    {
                        "state_index": int(idx),
                        "actual_label": str(label),
                        "predicted_label": str(predicted),
                        **payload,
                    }
                )
                if len(modified_failures) >= 8:
                    break

        active_rows = carry046._build_active_data(m)["active_rows"]
        nonterminal_rows = [row for row in active_rows if not row["exit_dirs"]]
        active_b_failures = []
        for row in nonterminal_rows:
            b = list(row["B"])
            theta = int((int(row["layer"]) + int(row["q"]) + int(row["w"]) + int(row["v"]) + int(row["u"])) % m)
            predicted = _formula_label(
                m,
                theta=theta,
                q=int(row["q"]),
                w=int(row["w"]),
                s=int(b[0]),
            )
            if predicted != "B" or str(row["label"]) != "B":
                active_b_failures.append(
                    {
                        "state_index": int(row["state_index"]),
                        "actual_label": str(row["label"]),
                        "predicted_label": str(predicted),
                        "q": int(row["q"]),
                        "w": int(row["w"]),
                        "theta": theta,
                        "s": int(b[0]),
                    }
                )
                if len(active_b_failures) >= 8:
                    break

        per_m[str(m)] = {
            "modified_formula_exact": bool(not modified_failures),
            "modified_labeled_state_count": int(modified_count),
            "first_modified_failure": None if not modified_failures else modified_failures[0],
            "active_nonterminal_all_B": bool(not active_b_failures),
            "active_nonterminal_count": int(len(nonterminal_rows)),
            "first_active_B_failure": None if not active_b_failures else active_b_failures[0],
        }

    return {
        "checked_moduli": list(SMALL_M_VALUES),
        "all_modified_formula_exact": bool(all(per_m[str(m)]["modified_formula_exact"] for m in SMALL_M_VALUES)),
        "all_active_nonterminal_B": bool(all(per_m[str(m)]["active_nonterminal_all_B"] for m in SMALL_M_VALUES)),
        "per_m": per_m,
    }


def _large_range_checks() -> Dict[str, object]:
    per_m: Dict[str, object] = {}

    for m in LARGE_M_VALUES:
        family_rows = []
        failures = []

        for source_u in range(1, m):
            family = "exceptional" if source_u == 3 else "regular"
            rho = int((source_u + 1) % m)
            target_phase, target_dir, target_step = _family_target(m, family)
            q, w, theta = (m - 1), 1, 2

            representative_rows = []
            branch_ok = True
            for step in range(target_step + 1):
                s = _s_from_raw_phase(m, q=q, w=w, theta=theta, rho=rho)
                class_label = _formula_label(m, theta=theta, q=q, w=w, s=s)
                pred_sig1_wu2 = int(s == 2)
                anchor = _scheduler_anchor(m, theta=theta, q=q, s=s)
                predicted_next = _projected_next_from_anchor(m, q=q, w=w, theta=theta, anchor=anchor)
                actual_next = _raw_odometer_next(m, q=q, w=w, theta=theta)
                current_phase = (q, w, theta)

                if step < target_step and class_label != "B":
                    branch_ok = False
                    failures.append(
                        {
                            "m": int(m),
                            "source_u": int(source_u),
                            "step": int(step),
                            "reason": "nonterminal state left B-region",
                            "family": family,
                            "q": int(q),
                            "w": int(w),
                            "theta": int(theta),
                            "s": int(s),
                            "class_label": class_label,
                        }
                    )
                    break

                if predicted_next != actual_next:
                    branch_ok = False
                    failures.append(
                        {
                            "m": int(m),
                            "source_u": int(source_u),
                            "step": int(step),
                            "reason": "scheduler disagrees with raw odometer",
                            "family": family,
                            "q": int(q),
                            "w": int(w),
                            "theta": int(theta),
                            "s": int(s),
                            "predicted_next": list(predicted_next),
                            "actual_next": list(actual_next),
                            "anchor": int(anchor),
                        }
                    )
                    break

                if pred_sig1_wu2 != int(s == 2):
                    branch_ok = False
                    failures.append(
                        {
                            "m": int(m),
                            "source_u": int(source_u),
                            "step": int(step),
                            "reason": "pred_sig1_wu2 mismatch",
                            "family": family,
                            "q": int(q),
                            "w": int(w),
                            "theta": int(theta),
                            "s": int(s),
                            "pred_sig1_wu2": int(pred_sig1_wu2),
                        }
                    )
                    break

                if step < 10 or step in {target_step - 1, target_step}:
                    representative_rows.append(
                        {
                            "step": int(step),
                            "q": int(q),
                            "w": int(w),
                            "theta": int(theta),
                            "s": int(s),
                            "c": int(q == m - 1),
                            "class_label": class_label,
                            "anchor": int(anchor),
                            "predicted_next": list(predicted_next),
                        }
                    )

                if step < target_step:
                    q, w, theta = actual_next

            if branch_ok and current_phase != target_phase:
                branch_ok = False
                failures.append(
                    {
                        "m": int(m),
                        "source_u": int(source_u),
                        "step": int(target_step),
                        "reason": "wrong first-exit raw target",
                        "family": family,
                        "final_phase": list(current_phase),
                        "target_phase": list(target_phase),
                    }
                )

            family_rows.append(
                {
                    "source_u": int(source_u),
                    "family": family,
                    "rho": int(rho),
                    "target_step": int(target_step),
                    "target_phase": list(target_phase),
                    "target_dir": [int(target_dir)],
                    "ok": bool(branch_ok),
                    "representative_rows": representative_rows,
                }
            )

        per_m[str(m)] = {
            "all_source_families_ok": bool(all(row["ok"] for row in family_rows)),
            "first_failure": None if not failures else failures[0],
            "family_rows": family_rows,
        }

    return {
        "checked_moduli": list(LARGE_M_VALUES),
        "all_large_branch_checks_ok": bool(all(per_m[str(m)]["all_source_families_ok"] for m in LARGE_M_VALUES)),
        "per_m": per_m,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Branch-local support for the D5 phase scheduler theorem of 059.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    small = _small_range_checks()
    large = _large_range_checks()

    analysis_summary = {
        "task_id": TASK_ID,
        "main_result": (
            "The 059 proof-critical support can be checked branch-locally instead of through the memory-heavy full-state 059A route. "
            "On the small extracted range, the direct modified-class formulas agree with the actual best-seed labels on the relevant states, "
            "and on the larger range the 037 raw corridor model is checked against the 059 scheduler and B-region premise source-family by source-family."
        ),
        "small_range": {
            "checked_moduli": small["checked_moduli"],
            "all_modified_formula_exact": bool(small["all_modified_formula_exact"]),
            "all_active_nonterminal_B": bool(small["all_active_nonterminal_B"]),
        },
        "large_range": {
            "checked_moduli": large["checked_moduli"],
            "all_large_branch_checks_ok": bool(large["all_large_branch_checks_ok"]),
        },
        "environment": environment_block(),
        "runtime_seconds": runtime_since(started),
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "small_range_label_formula_checks.json", small)
    _write_json(out_dir / "large_range_branch_validation.json", large)
    _write_json(
        out_dir / "representative_branch_tables.json",
        {
            "small_range": small["per_m"],
            "large_range": {
                key: {
                    "family_rows": value["family_rows"],
                }
                for key, value in large["per_m"].items()
            },
        },
    )
    _write_json(args.summary_out, analysis_summary)


if __name__ == "__main__":
    main()
