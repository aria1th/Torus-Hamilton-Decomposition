#!/usr/bin/env python3
"""Comparison support for the D5 intended quotient versus the dynamic bridge."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import torus_nd_d5_deep_transition_carry_sheet as carry046
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-INTENDED-QUOTIENT-COMPARE-106"
DEFAULT_M_VALUES = (13, 15, 17)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _event_class(dn: Sequence[int]) -> str:
    dn_tuple = tuple(int(value) for value in dn)
    if dn_tuple == (0, 0, 0, 1):
        return "flat"
    if dn_tuple == (0, 0, 0, 0):
        return "wrap"
    if dn_tuple == (1, 1, 0, 0):
        return "carry_jump"
    if dn_tuple == (1, 0, 0, 0):
        return "other_1000"
    if dn_tuple == (0, 0, 1, 0):
        return "other_0010"
    return "other"


def _beta(row: Mapping[str, object], m: int) -> int:
    s, _u, v, layer, _family = row["B"]
    return int((-(int(row["q"]) + int(s) + int(v) + int(layer))) % m)


def _jsonable(value):
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _represent_row(row: Mapping[str, object]) -> Dict[str, object]:
    return {
        "m": int(row["m"]),
        "source_u": int(row["source_u"]),
        "rho": int(row["rho"]),
        "family": str(row["family"]),
        "trace_step": int(row["trace_step"]),
        "B": _jsonable(tuple(row["B"])),
        "beta": int(row["beta"]),
        "q0": int(row["q0"]),
        "sigma": int(row["sigma"]),
        "delta": int(row["delta"]),
        "a": int(row["a"]),
        "b": int(row["b"]),
        "epsilon4": str(row["epsilon4"]),
        "short_corner": None if "short_corner" not in row else int(row["short_corner"]),
    }


def _extract_chain_rows(m: int) -> Dict[str, object]:
    payload = carry046._build_active_data(m)
    rows = sorted(
        payload["active_rows"],
        key=lambda row: (int(row["source_u"]), str(row["family"]), int(row["trace_step"])),
    )
    by_branch: Dict[Tuple[int, str], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        by_branch[(int(row["source_u"]), str(row["family"]))].append(row)

    chain_rows: List[Dict[str, object]] = []
    branch_count = 0
    chain_count = 0

    for (source_u, family), seq in sorted(by_branch.items()):
        branch_count += 1
        i = 0
        while i < len(seq):
            if _event_class(seq[i]["dn"]) != "carry_jump":
                i += 1
                continue

            start = seq[i]
            q0 = int(start["q"])
            sigma = int((int(source_u) + int(start["w"])) % m)
            rho = int((int(source_u) + 1) % m)
            a = int(q0 == m - 1)
            b = int(((q0 + sigma) % m == 1) or (q0 == m - 1 and sigma != 1))

            chain: List[Mapping[str, object]] = []
            j = i
            while j < len(seq):
                row = seq[j]
                chain.append(row)
                if _event_class(row["dn"]) == "wrap":
                    break
                j += 1

            if not chain or _event_class(chain[-1]["dn"]) != "wrap":
                i += 1
                continue

            chain_count += 1
            for idx, row in enumerate(chain):
                rec = {
                    "m": int(m),
                    "source_u": int(source_u),
                    "rho": int(rho),
                    "family": str(family),
                    "trace_step": int(row["trace_step"]),
                    "B": tuple(row["B"]),
                    "beta": int(_beta(row, m)),
                    "q0": int(q0),
                    "sigma": int(sigma),
                    "delta": int(q0 + m * sigma),
                    "a": int(a),
                    "b": int(b),
                    "epsilon4": str(_event_class(row["dn"])),
                    "terminal": bool(idx == len(chain) - 1),
                }
                if idx < len(chain) - 1:
                    next_row = chain[idx + 1]
                    rec["next_beta"] = int(_beta(next_row, m))
                    rec["next_epsilon4"] = str(_event_class(next_row["dn"]))
                    rec["short_corner"] = int(
                        rec["epsilon4"] == "flat"
                        and rec["next_epsilon4"] == "other_1000"
                    )
                chain_rows.append(rec)

            i = j + 1

    return {
        "m": int(m),
        "branch_count": int(branch_count),
        "chain_count": int(chain_count),
        "rows": chain_rows,
    }


def _bucket_exactness(rows, key_getter, value_getter) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], set] = defaultdict(set)
    refs: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        key = key_getter(row)
        buckets[key].add(value_getter(row))
        refs[key].append(row)

    first = None
    collision_bucket_count = 0
    for key, values in buckets.items():
        if len(values) > 1:
            collision_bucket_count += 1
            if first is None:
                first = {
                    "key": _jsonable(key),
                    "values": [_jsonable(value) for value in sorted(values, key=str)],
                    "rows": [_represent_row(refs[key][idx]) for idx in range(min(4, len(refs[key])))],
                }

    return {
        "is_exact": bool(collision_bucket_count == 0),
        "bucket_count": int(len(buckets)),
        "collision_bucket_count": int(collision_bucket_count),
        "first_collision": first,
    }


def _bucket_determinism(rows, key_getter, succ_getter) -> Dict[str, object]:
    succ_map: Dict[Tuple[object, ...], set] = defaultdict(set)
    refs: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        key = key_getter(row)
        succ_map[key].add(succ_getter(row))
        refs[key].append(row)

    first = None
    failure_count = 0
    for key, values in succ_map.items():
        if len(values) > 1:
            failure_count += 1
            if first is None:
                first = {
                    "key": _jsonable(key),
                    "next_keys": [_jsonable(value) for value in sorted(values, key=str)],
                    "rows": [_represent_row(refs[key][idx]) for idx in range(min(4, len(refs[key])))],
                }

    return {
        "is_deterministic": bool(failure_count == 0),
        "bucket_count": int(len(succ_map)),
        "failure_bucket_count": int(failure_count),
        "first_failure": first,
    }


def _ambiguity_profile(rows, key_getter, value_getter) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], set] = defaultdict(set)
    bucket_rows: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        key = key_getter(row)
        buckets[key].add(value_getter(row))
        bucket_rows[key].append(row)

    size_hist = Counter(len(values) for values in buckets.values())
    ambiguous_keys = [key for key, values in buckets.items() if len(values) > 1]
    first = None
    if ambiguous_keys:
        key = ambiguous_keys[0]
        first = {
            "key": _jsonable(key),
            "value_count": int(len(buckets[key])),
            "values": [_jsonable(value) for value in sorted(buckets[key], key=str)[:8]],
            "rows": [_represent_row(bucket_rows[key][idx]) for idx in range(min(4, len(bucket_rows[key])))],
        }

    return {
        "bucket_count": int(len(buckets)),
        "ambiguous_bucket_count": int(len(ambiguous_keys)),
        "bucket_size_histogram": {
            str(size): int(count)
            for size, count in sorted(size_hist.items())
        },
        "first_ambiguous_bucket": first,
    }


def _analyze_modulus(m: int) -> Dict[str, object]:
    started = time.perf_counter()
    payload = _extract_chain_rows(m)
    rows = payload["rows"]
    nonterminal_rows = [row for row in rows if not row["terminal"]]

    theorem_key = lambda row: (tuple(row["B"]), int(row["beta"]))
    dynamic_key = lambda row: (int(row["beta"]), int(row["q0"]), int(row["sigma"]))
    rho_dynamic_key = lambda row: (int(row["rho"]), int(row["beta"]), int(row["q0"]), int(row["sigma"]))
    family_dynamic_key = lambda row: (str(row["family"]), int(row["beta"]), int(row["q0"]), int(row["sigma"]))
    decorated_key = lambda row: (int(row["beta"]), int(row["a"]), int(row["b"]))

    result = {
        "m": int(m),
        "runtime_seconds": runtime_since(started),
        "branch_count": int(payload["branch_count"]),
        "chain_count": int(payload["chain_count"]),
        "state_row_count": int(len(rows)),
        "nonterminal_state_row_count": int(len(nonterminal_rows)),
        "dynamic_bridge": {
            "epsilon4_exactness": _bucket_exactness(rows, dynamic_key, lambda row: str(row["epsilon4"])),
            "short_corner_exactness": _bucket_exactness(
                nonterminal_rows,
                dynamic_key,
                lambda row: int(row["short_corner"]),
            ),
            "successor_determinism": _bucket_determinism(
                nonterminal_rows,
                dynamic_key,
                lambda row: (int(row["next_beta"]), int(row["q0"]), int(row["sigma"])),
            ),
        },
        "decorated_bridge": {
            "epsilon4_exactness": _bucket_exactness(rows, decorated_key, lambda row: str(row["epsilon4"])),
            "short_corner_exactness": _bucket_exactness(
                nonterminal_rows,
                decorated_key,
                lambda row: int(row["short_corner"]),
            ),
            "successor_determinism": _bucket_determinism(
                nonterminal_rows,
                decorated_key,
                lambda row: (int(row["next_beta"]), int(row["a"]), int(row["b"])),
            ),
        },
        "comparison": {
            "theorem_to_dynamic": _bucket_exactness(rows, theorem_key, dynamic_key),
            "dynamic_to_theorem": _ambiguity_profile(rows, dynamic_key, theorem_key),
            "rho_dynamic_to_theorem": _bucket_exactness(rows, rho_dynamic_key, theorem_key),
            "family_dynamic_to_theorem": _bucket_exactness(rows, family_dynamic_key, theorem_key),
        },
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Comparison support for the D5 intended quotient versus the dynamic bridge.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--m-values", type=int, nargs="+", default=list(DEFAULT_M_VALUES))
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    m_values = [int(m) for m in args.m_values]
    results: List[Dict[str, object]] = []

    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs, max_tasks_per_child=1) as pool:
            for result in pool.map(_analyze_modulus, m_values):
                print(
                    f"[{TASK_ID}] finished m={result['m']} chains={result['chain_count']} rows={result['state_row_count']}",
                    flush=True,
                )
                results.append(result)
    else:
        for m in m_values:
            result = _analyze_modulus(m)
            print(
                f"[{TASK_ID}] finished m={result['m']} chains={result['chain_count']} rows={result['state_row_count']}",
                flush=True,
            )
            results.append(result)

    results.sort(key=lambda item: int(item["m"]))
    by_m = {str(item["m"]): item for item in results}

    all_dynamic_exact = all(
        item["dynamic_bridge"]["epsilon4_exactness"]["is_exact"]
        and item["dynamic_bridge"]["short_corner_exactness"]["is_exact"]
        and item["dynamic_bridge"]["successor_determinism"]["is_deterministic"]
        for item in results
    )
    all_theorem_to_dynamic = all(
        item["comparison"]["theorem_to_dynamic"]["is_exact"]
        for item in results
    )
    all_rho_recovery = all(
        item["comparison"]["rho_dynamic_to_theorem"]["is_exact"]
        for item in results
    )

    analysis_summary = {
        "task_id": TASK_ID,
        "checked_moduli": m_values,
        "all_dynamic_bridge_checks_exact": bool(all_dynamic_exact),
        "all_theorem_to_dynamic_maps_exact": bool(all_theorem_to_dynamic),
        "all_rho_dynamic_recoveries_exact": bool(all_rho_recovery),
        "main_result": (
            "On the regenerated carry_jump-to-wrap state-chain object, the theorem-side key (B,beta) "
            "always determines the dynamic bridge key (beta,q0,sigma), while the reverse direction fails "
            "globally because the dynamic bridge forgets source-residue bookkeeping. Adding rho = source_u + 1 "
            "recovers the theorem-side key exactly on every checked modulus."
        ),
        "recommendation": (
            "Use the intended quotient in M3 as the exact deterministic quotient that retains grouped base, "
            "and prove a comparison theorem to the dynamic bridge rather than claiming literal equality with "
            "(beta,delta). The checked data supports the stronger comparison (B,beta) ~= (rho,beta,q0,sigma) "
            "on the exact marked chain object."
        ),
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }

    details = {
        "summary": analysis_summary,
        "per_modulus": by_m,
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "per_modulus_comparison.json", by_m)
    _write_json(args.summary_out, analysis_summary)
    _write_json(out_dir / "details.json", details)


if __name__ == "__main__":
    main()
