#!/usr/bin/env python3
"""Extract the exact tau countdown/reset dynamics on the frozen D5 carry dataset."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-TAU-COUNTDOWN-CARRIER-048"
DEFAULT_DATASET = Path(
    "artifacts/d5_future_transition_carry_coding_047/data/frozen_B_c_tau_epsilon_dataset_047.json"
)
B_FIELDS = ("s", "u", "v", "layer", "family")


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _load_dataset(path: Path) -> Dict[int, List[Dict[str, object]]]:
    raw = json.loads(path.read_text())
    return {int(m): list(rows) for m, rows in raw.items()}


def _augment_row(row: Mapping[str, object], next_row: Mapping[str, object] | None) -> Dict[str, object]:
    b = list(row["B"])
    out = {
        "m": int(row["m"]),
        "source_u": int(row["source_u"]),
        "trace_step": int(row["trace_step"]),
        "family": str(row["family"]),
        "state_index": int(row["state_index"]),
        "s": int(b[0]),
        "u": int(b[1]),
        "v": int(b[2]),
        "layer": int(b[3]),
        "dn": [int(value) for value in row["dn"]],
        "c": int(row["c"]),
        "q": int(row["q"]),
        "w": int(row["w"]),
        "label": str(row["label"]),
        "tau": int(row["tau"]),
        "epsilon4": str(row["epsilon4"]),
        "has_next": bool(next_row is not None),
    }
    if next_row is not None:
        out["next_tau"] = int(next_row["tau"])
        out["next_epsilon4"] = str(next_row["epsilon4"])
        out["next_state_index"] = int(next_row["state_index"])
    return out


def _augment_dataset(rows_by_m: Mapping[int, Sequence[Mapping[str, object]]]) -> Dict[int, Dict[str, object]]:
    out: Dict[int, Dict[str, object]] = {}
    for m, rows in rows_by_m.items():
        row_index = {
            (str(row["family"]), int(row["source_u"]), int(row["trace_step"])): row
            for row in rows
        }
        nonterminal_rows: List[Dict[str, object]] = []
        terminal_rows: List[Dict[str, object]] = []
        for row in rows:
            next_row = row_index.get(
                (str(row["family"]), int(row["source_u"]), int(row["trace_step"]) + 1)
            )
            augmented = _augment_row(row, next_row)
            if next_row is None:
                terminal_rows.append(augmented)
            else:
                nonterminal_rows.append(augmented)
        out[int(m)] = {
            "nonterminal_rows": nonterminal_rows,
            "terminal_rows": terminal_rows,
        }
    return out


def _bucket_summary(rows: Sequence[Mapping[str, object]], key_fn) -> Dict[str, object]:
    buckets: MutableMapping[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        buckets[key_fn(row)].append(row)
    collisions = []
    for key, bucket in buckets.items():
        values = {int(row["next_tau"]) for row in bucket}
        if len(values) > 1:
            collisions.append((key, bucket))
    return {
        "distinct_key_count": int(len(buckets)),
        "collision_bucket_count": int(len(collisions)),
        "is_exact": bool(len(collisions) == 0),
        "collision_buckets": collisions,
    }


def _jsonable_key(key: Tuple[object, ...]) -> List[object]:
    out = []
    for value in key:
        if isinstance(value, tuple):
            out.append(_jsonable_key(value))
        else:
            out.append(value)
    return out


def _represent_row(row: Mapping[str, object]) -> Dict[str, object]:
    return {
        "m": int(row["m"]),
        "source_u": int(row["source_u"]),
        "trace_step": int(row["trace_step"]),
        "family": str(row["family"]),
        "state_index": int(row["state_index"]),
        "q": int(row["q"]),
        "w": int(row["w"]),
        "s": int(row["s"]),
        "u": int(row["u"]),
        "v": int(row["v"]),
        "layer": int(row["layer"]),
        "label": str(row["label"]),
        "tau": int(row["tau"]),
        "epsilon4": str(row["epsilon4"]),
        "c": int(row["c"]),
        "next_tau": int(row["next_tau"]),
        "next_epsilon4": str(row["next_epsilon4"]),
    }


def _sample_collision_rows(
    summary: Mapping[str, object],
    limit_buckets: int = 3,
    limit_rows: int = 4,
) -> List[Dict[str, object]]:
    out = []
    for key, bucket in summary["collision_buckets"][:limit_buckets]:
        out.append(
            {
                "key": _jsonable_key(key),
                "rows": [_represent_row(row) for row in bucket[:limit_rows]],
            }
        )
    return out


def _countdown_validation(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    positive_rows = [row for row in rows if int(row["tau"]) > 0]
    exact = all(int(row["next_tau"]) == int(row["tau"]) - 1 for row in positive_rows)
    by_tau = Counter(int(row["tau"]) for row in positive_rows)
    failures = [
        _represent_row(row)
        for row in positive_rows
        if int(row["next_tau"]) != int(row["tau"]) - 1
    ]
    return {
        "positive_row_count": int(len(positive_rows)),
        "positive_tau_counts": {str(key): int(value) for key, value in sorted(by_tau.items())},
        "countdown_is_exact": bool(exact),
        "failure_count": int(len(failures)),
        "sample_failures": failures[:6],
    }


def _boundary_value_summary(rows: Sequence[Mapping[str, object]], terminal_rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    out: Dict[str, object] = {}
    boundary_rows = [row for row in rows if int(row["tau"]) == 0]
    boundary_terminals = [row for row in terminal_rows if int(row["tau"]) == 0]
    epsilon_counts: MutableMapping[str, Counter[int]] = defaultdict(Counter)
    for row in boundary_rows:
        epsilon_counts[str(row["epsilon4"])][int(row["next_tau"])] += 1
    terminal_counts = Counter(str(row["epsilon4"]) for row in boundary_terminals)
    reset_values = {
        epsilon: sorted(int(value) for value in counter.keys())
        for epsilon, counter in sorted(epsilon_counts.items())
    }
    out["boundary_nonterminal_row_count"] = int(len(boundary_rows))
    out["boundary_terminal_row_count"] = int(len(boundary_terminals))
    out["next_tau_counts_by_epsilon"] = {
        epsilon: {str(key): int(value) for key, value in sorted(counter.items())}
        for epsilon, counter in sorted(epsilon_counts.items())
    }
    out["reset_values_by_epsilon"] = reset_values
    out["terminal_boundary_counts_by_epsilon"] = {
        str(key): int(value) for key, value in sorted(terminal_counts.items())
    }
    return out


def _find_exact_subsets(
    rows_by_m: Mapping[int, Sequence[Mapping[str, object]]],
    *,
    prefix_fields: Sequence[str],
    candidate_fields: Sequence[str],
) -> Dict[str, object]:
    for size in range(len(candidate_fields) + 1):
        exact_subsets = []
        examples = []
        for subset in combinations(candidate_fields, size):
            collision_examples = []
            exact = True
            for m, rows in rows_by_m.items():
                summary = _bucket_summary(
                    rows,
                    lambda row, subset=subset: tuple(row[field] for field in prefix_fields)
                    + tuple(row[field] for field in subset),
                )
                if not summary["is_exact"]:
                    exact = False
                    collision_examples = _sample_collision_rows(summary)
                    break
            if exact:
                exact_subsets.append(list(subset))
            elif not examples and collision_examples:
                examples = collision_examples
        if exact_subsets:
            return {
                "minimal_size": int(size),
                "exact_subsets": exact_subsets,
                "collision_examples_at_size_minus_one": examples,
            }
    raise AssertionError("no exact subset found")


def _piecewise_key(row: Mapping[str, object]) -> Tuple[object, ...]:
    tau = int(row["tau"])
    if tau > 0:
        return ("countdown", tau)
    epsilon = str(row["epsilon4"])
    if epsilon == "wrap":
        return ("wrap",)
    if epsilon == "carry_jump":
        return ("carry_jump", int(row["s"]), int(row["v"]), int(row["layer"]))
    return ("other", int(row["s"]), int(row["u"]), int(row["layer"]))


def _representative_rows(
    rows_by_m: Mapping[int, Sequence[Mapping[str, object]]],
) -> Dict[str, object]:
    countdown_rows = {}
    boundary_rows = {}
    for m, rows in rows_by_m.items():
        by_tau: Dict[int, Dict[str, object]] = {}
        for row in rows:
            tau = int(row["tau"])
            if tau > 0 and tau not in by_tau:
                by_tau[tau] = _represent_row(row)
            if len(by_tau) >= 4:
                break
        countdown_rows[str(m)] = [by_tau[tau] for tau in sorted(by_tau)[:4]]

        by_boundary: MutableMapping[str, Dict[int, Dict[str, object]]] = defaultdict(dict)
        for row in rows:
            if int(row["tau"]) != 0:
                continue
            epsilon = str(row["epsilon4"])
            next_tau = int(row["next_tau"])
            by_boundary[epsilon].setdefault(next_tau, _represent_row(row))
        boundary_rows[str(m)] = {
            epsilon: [row for _, row in sorted(bucket.items())]
            for epsilon, bucket in sorted(by_boundary.items())
        }

    return {
        "countdown_rows": countdown_rows,
        "boundary_rows": boundary_rows,
    }


def _analysis_summary(
    *,
    started: float,
    countdown_by_m: Mapping[int, Mapping[str, object]],
    boundary_by_m: Mapping[int, Mapping[str, object]],
    global_boundary_minimal: Mapping[str, object],
    carry_jump_minimal: Mapping[str, object],
    other_minimal: Mapping[str, object],
    piecewise_exact: bool,
) -> Dict[str, object]:
    return {
        "task_id": TASK_ID,
        "main_result": (
            "The 047 carry target sharpens internally as well. On the checked active nonterminal branch "
            "for m=5,7,9,11, tau is already an exact countdown carrier: whenever tau>0, the next value is "
            "tau-1. All nontrivial dynamics are confined to the tau=0 boundary, where the reset law is tiny: "
            "wrap resets to 0, carry_jump resets exactly as a function of (s,v,layer), and other resets "
            "exactly as a function of (s,u,layer). Equivalently, the full next-tau map is exact on "
            "(tau,epsilon4,s,u,v,layer), and no smaller B-subset with epsilon4 is exact on the boundary. "
            "So 047A is not a vague future window anymore: it is a countdown carrier with a small current-state reset law."
        ),
        "checked_moduli": sorted(int(m) for m in countdown_by_m),
        "countdown_summary": {
            str(m): {
                "positive_row_count": int(payload["positive_row_count"]),
                "countdown_is_exact": bool(payload["countdown_is_exact"]),
            }
            for m, payload in sorted(countdown_by_m.items())
        },
        "boundary_reset_values": {
            str(m): payload["reset_values_by_epsilon"]
            for m, payload in sorted(boundary_by_m.items())
        },
        "boundary_minimal_exact_quotient": global_boundary_minimal,
        "carry_jump_boundary_minimal_exact_quotient": carry_jump_minimal,
        "other_boundary_minimal_exact_quotient": other_minimal,
        "piecewise_carrier_law_is_exact": bool(piecewise_exact),
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the exact tau countdown/reset dynamics on the frozen D5 carry dataset.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_rows_by_m = _load_dataset(args.dataset)
    augmented = _augment_dataset(raw_rows_by_m)
    nonterminal_by_m = {
        int(m): payload["nonterminal_rows"]
        for m, payload in augmented.items()
    }
    terminal_by_m = {
        int(m): payload["terminal_rows"]
        for m, payload in augmented.items()
    }

    countdown_by_m = {
        int(m): _countdown_validation(rows)
        for m, rows in nonterminal_by_m.items()
    }
    boundary_by_m = {
        int(m): _boundary_value_summary(nonterminal_by_m[m], terminal_by_m[m])
        for m in sorted(nonterminal_by_m)
    }

    global_boundary_minimal = _find_exact_subsets(
        {
            int(m): [row for row in rows if int(row["tau"]) == 0]
            for m, rows in nonterminal_by_m.items()
        },
        prefix_fields=("epsilon4",),
        candidate_fields=B_FIELDS,
    )
    carry_jump_minimal = _find_exact_subsets(
        {
            int(m): [row for row in rows if int(row["tau"]) == 0 and str(row["epsilon4"]) == "carry_jump"]
            for m, rows in nonterminal_by_m.items()
        },
        prefix_fields=(),
        candidate_fields=B_FIELDS,
    )
    other_minimal = _find_exact_subsets(
        {
            int(m): [row for row in rows if int(row["tau"]) == 0 and str(row["epsilon4"]) == "other"]
            for m, rows in nonterminal_by_m.items()
        },
        prefix_fields=(),
        candidate_fields=B_FIELDS,
    )

    piecewise_summary_by_m = {
        str(m): {
            key: value
            for key, value in _bucket_summary(rows, _piecewise_key).items()
            if key != "collision_buckets"
        }
        for m, rows in sorted(nonterminal_by_m.items())
    }
    piecewise_exact = all(payload["is_exact"] for payload in piecewise_summary_by_m.values())
    piecewise_collision_examples = {
        str(m): _sample_collision_rows(_bucket_summary(rows, _piecewise_key))
        for m, rows in sorted(nonterminal_by_m.items())
        if not _bucket_summary(rows, _piecewise_key)["is_exact"]
    }

    representatives = _representative_rows(nonterminal_by_m)

    analysis_summary = _analysis_summary(
        started=started,
        countdown_by_m=countdown_by_m,
        boundary_by_m=boundary_by_m,
        global_boundary_minimal=global_boundary_minimal,
        carry_jump_minimal=carry_jump_minimal,
        other_minimal=other_minimal,
        piecewise_exact=piecewise_exact,
    )

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(
        out_dir / "tau_countdown_validation_048.json",
        {str(m): payload for m, payload in sorted(countdown_by_m.items())},
    )
    _write_json(
        out_dir / "boundary_reset_value_summary_048.json",
        {str(m): payload for m, payload in sorted(boundary_by_m.items())},
    )
    _write_json(
        out_dir / "boundary_reset_minimal_subquotients_048.json",
        {
            "global_boundary_with_epsilon4": global_boundary_minimal,
            "carry_jump_boundary": carry_jump_minimal,
            "other_boundary": other_minimal,
        },
    )
    _write_json(
        out_dir / "tau_piecewise_carrier_validation_048.json",
        {
            "piecewise_rule": {
                "tau_gt_zero": "next_tau = tau - 1",
                "tau_eq_zero_wrap": "next_tau = 0",
                "tau_eq_zero_carry_jump": "next_tau is exact on (s,v,layer)",
                "tau_eq_zero_other": "next_tau is exact on (s,u,layer)",
            },
            "summary_by_modulus": piecewise_summary_by_m,
            "collision_examples": piecewise_collision_examples,
        },
    )
    _write_json(
        out_dir / "representative_tau_rows_048.json",
        representatives,
    )
    args.summary_out.write_text(
        json.dumps(
            {
                "task_id": TASK_ID,
                "analysis_summary": analysis_summary,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
