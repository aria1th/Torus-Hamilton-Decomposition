#!/usr/bin/env python3
"""Exhaustive support for the D5 exact reduction object and canonical beta clock."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import torus_nd_d5_deep_transition_carry_sheet as carry046
import torus_nd_d5_phase_scheduler_branch_support as branch059b
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-EXACT-REDUCTION-SUPPORT-068B"
DEFAULT_FULL_M_VALUES = (13, 15, 17, 19, 21, 23, 25, 27, 29)
DEFAULT_BRANCH_M_VALUES = (31, 33, 35, 37, 39, 41)
FLAT_DN = (0, 0, 0, 1)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _event_class(dn: Sequence[int]) -> str:
    dn_tuple = tuple(int(value) for value in dn)
    if dn_tuple == FLAT_DN:
        return "flat"
    if dn_tuple == (0, 0, 0, 0):
        return "wrap"
    if dn_tuple == (1, 1, 0, 0):
        return "carry_jump"
    return "other"


def _state_B(row_orbit: Mapping[int, Mapping[str, object]], state_index: int, family: str) -> Tuple[object, ...]:
    return tuple(row_orbit[state_index]["B_base"]) + (family,)


def _beta_from_state(row_orbit: Mapping[int, Mapping[str, object]], state_index: int, m: int) -> int:
    row = row_orbit[state_index]
    s, _u, v, layer = [int(value) for value in row["B_base"]]
    q = int(row["q"])
    return (-((q + s + v + layer) % m)) % m


def _signature_for_state(
    row_orbit: Mapping[int, Mapping[str, object]],
    state_index: int,
    cache: MutableMapping[int, Dict[str, object]],
) -> Dict[str, object]:
    if state_index in cache:
        return cache[state_index]
    run_length = 0
    current = int(state_index)
    while tuple(int(value) for value in row_orbit[current]["dn"]) == FLAT_DN:
        run_length += 1
        current = int(row_orbit[current]["next_state_index"])
    payload = {
        "tau": int(run_length),
        "first_nonflat_dn": tuple(int(value) for value in row_orbit[current]["dn"]),
    }
    cache[state_index] = payload
    return payload


def _bucket_exactness(
    rows: Sequence[Mapping[str, object]],
    key_getter,
    value_getter,
) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], List[object]] = defaultdict(list)
    row_refs: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        key = key_getter(row)
        buckets[key].append(value_getter(row))
        row_refs[key].append(row)

    collision_buckets = []
    for key, values in buckets.items():
        unique = set(values)
        if len(unique) > 1:
            collision_buckets.append((key, unique, row_refs[key]))

    first = None
    if collision_buckets:
        key, unique, refs = collision_buckets[0]
        first = {
            "key": _jsonable(key),
            "values": [_jsonable(v) for v in sorted(unique, key=str)],
            "rows": [_represent_row(refs[i]) for i in range(min(4, len(refs)))],
        }

    return {
        "is_exact": bool(not collision_buckets),
        "collision_bucket_count": int(len(collision_buckets)),
        "first_collision": first,
    }


def _jsonable(value):
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _represent_row(row: Mapping[str, object]) -> Dict[str, object]:
    out = {
        "m": int(row["m"]),
        "source_u": int(row["source_u"]),
        "trace_step": int(row["trace_step"]),
        "family": str(row["family"]),
        "state_index": int(row["state_index"]),
        "B": [_jsonable(v) for v in row["B"]],
        "q": int(row["q"]),
        "w": int(row["w"]),
        "u": int(row["u"]),
        "v": int(row["v"]),
        "layer": int(row["layer"]),
        "c": int(row["c"]),
        "epsilon4": str(row["epsilon4"]),
        "tau": int(row["tau"]),
        "next_tau": int(row["next_tau"]),
        "beta": int(row["beta"]),
    }
    if "next_B" in row:
        out["next_B"] = [_jsonable(v) for v in row["next_B"]]
    return out


def _augment_rows(m: int) -> Dict[str, object]:
    payload = carry046._build_active_data(m)
    row_orbit = payload["row_orbit"]
    signature_cache: Dict[int, Dict[str, object]] = {}
    augmented_rows: List[Dict[str, object]] = []

    for row in payload["active_rows"]:
        state_index = int(row["state_index"])
        next_state = int(row_orbit[state_index]["next_state_index"])
        family = str(row["family"])
        signature = _signature_for_state(row_orbit, state_index, signature_cache)
        next_signature = _signature_for_state(row_orbit, next_state, signature_cache)

        beta = _beta_from_state(row_orbit, state_index, m)
        beta_next = _beta_from_state(row_orbit, next_state, m)
        next_dn = tuple(int(value) for value in row_orbit[next_state]["dn"])
        next_next_state = int(row_orbit[next_state]["next_state_index"])
        next_B = _state_B(row_orbit, next_state, family)
        next_B2 = _state_B(row_orbit, next_next_state, family)

        augmented_rows.append(
            {
                **row,
                "epsilon4": _event_class(row["dn"]),
                "tau": int(signature["tau"]),
                "next_tau": int(next_signature["tau"]),
                "beta": int(beta),
                "beta_next": int(beta_next),
                "next_dn": list(next_dn),
                "next_B": next_B,
                "next_B2": next_B2,
            }
        )

    return {
        "m": int(m),
        "rows": augmented_rows,
    }


def _partition_carry_jump_chains(rows: Sequence[Mapping[str, object]], m: int) -> Dict[str, object]:
    regular = [row for row in rows if str(row["family"]) == "regular" and str(row["epsilon4"]) == "carry_jump"]
    per_source: Dict[int, List[Mapping[str, object]]] = defaultdict(list)
    for row in regular:
        per_source[int(row["source_u"])].append(row)

    source_summaries: Dict[str, object] = {}
    expected_ws = list(range(2, m - 1))
    all_sources_ok = True
    all_splices_ok = True

    for source_u, source_rows in sorted(per_source.items()):
        source_rows = sorted(source_rows, key=lambda row: int(row["trace_step"]))
        by_w: Dict[int, List[Mapping[str, object]]] = defaultdict(list)
        for row in source_rows:
            by_w[int(row["w"])].append(row)

        w_values = sorted(by_w.keys())
        chain_lengths = []
        all_chains_ok = True
        splice_ok = True
        per_w = {}

        for w in w_values:
            chain_rows = sorted(by_w[w], key=lambda row: int(row["trace_step"]))
            q_values = [int(row["q"]) for row in chain_rows]
            c_values = [int(row["c"]) for row in chain_rows]
            chain_ok = q_values == list(range(m)) and c_values == [0] * (m - 1) + [1]
            all_chains_ok = all_chains_ok and chain_ok
            chain_lengths.append(len(chain_rows))
            per_w[str(w)] = {
                "chain_ok": bool(chain_ok),
                "q_values": q_values[: min(6, len(q_values))] + (["..."] if len(q_values) > 6 else []),
                "carry_pattern_ok": bool(c_values == [0] * (m - 1) + [1]),
            }

        for idx in range(len(w_values) - 1):
            cur_w = w_values[idx]
            nxt_w = w_values[idx + 1]
            cur_last = sorted(by_w[cur_w], key=lambda row: int(row["trace_step"]))[-1]
            nxt_first = sorted(by_w[nxt_w], key=lambda row: int(row["trace_step"]))[0]
            local_ok = (
                int(cur_last["q"]) == m - 1
                and int(nxt_first["q"]) == 0
                and nxt_w == cur_w + 1
            )
            splice_ok = splice_ok and local_ok

        all_sources_ok = all_sources_ok and all_chains_ok and (w_values == expected_ws)
        all_splices_ok = all_splices_ok and splice_ok
        source_summaries[str(source_u)] = {
            "w_values": w_values,
            "expected_w_values": expected_ws,
            "chain_lengths": chain_lengths,
            "all_w_slices_marked_q_chains": bool(all_chains_ok),
            "endpoint_splice_to_next_w_slice": bool(splice_ok),
            "per_w": per_w,
        }

    return {
        "regular_source_count": int(len(per_source)),
        "expected_chain_w_values": expected_ws,
        "all_regular_sources_ok": bool(all_sources_ok),
        "all_regular_splices_ok": bool(all_splices_ok),
        "interpretation": (
            "fixed-(source_u,w) regular carry_jump rows form a marked length-m q-chain; "
            "quotienting successive w-slices is the extra step needed to view a cycle"
        ),
        "per_source": source_summaries,
    }


def _observable_key(row: Mapping[str, object], name: str) -> Tuple[object, ...]:
    if name == "next_dn":
        return tuple(int(value) for value in row["next_dn"])
    if name == "dn_plus_next_dn":
        return (
            tuple(int(value) for value in row["dn"]),
            tuple(int(value) for value in row["next_dn"]),
        )
    if name == "B":
        return tuple(row["B"])
    if name == "B_next":
        return (tuple(row["B"]), tuple(row["next_B"]))
    if name == "B_next2":
        return (tuple(row["B"]), tuple(row["next_B"]), tuple(row["next_B2"]))
    raise KeyError(name)


def _quotient_diagnostics(rows: Sequence[Mapping[str, object]], m: int) -> Dict[str, object]:
    regular = [row for row in rows if str(row["family"]) == "regular" and str(row["epsilon4"]) == "carry_jump"]
    per_chain: Dict[Tuple[int, int], List[Mapping[str, object]]] = defaultdict(list)
    for row in regular:
        per_chain[(int(row["source_u"]), int(row["w"]))].append(row)

    observable_names = ("next_dn", "dn_plus_next_dn", "B", "B_next", "B_next2")
    per_observable: Dict[str, object] = {}

    for name in observable_names:
        sizes = []
        carry_exact_all = True
        deterministic_all = True
        first_failure = None

        for chain_key, chain_rows in sorted(per_chain.items()):
            chain_rows = sorted(chain_rows, key=lambda row: int(row["q"]))
            keys = [_observable_key(row, name) for row in chain_rows]
            sizes.append(len(set(keys)))

            carry_buckets: Dict[Tuple[object, ...], set[int]] = defaultdict(set)
            for row, key in zip(chain_rows, keys):
                carry_buckets[key].add(int(row["c"]))
            carry_exact = all(len(values) == 1 for values in carry_buckets.values())
            carry_exact_all = carry_exact_all and carry_exact

            succ_map: Dict[Tuple[object, ...], set[Tuple[object, ...]]] = defaultdict(set)
            for idx in range(len(chain_rows) - 1):
                succ_map[keys[idx]].add(keys[idx + 1])
            deterministic = all(len(values) <= 1 for values in succ_map.values())
            deterministic_all = deterministic_all and deterministic

            if first_failure is None and (not carry_exact or not deterministic):
                first_failure = {
                    "chain": [int(chain_key[0]), int(chain_key[1])],
                    "carry_exact": bool(carry_exact),
                    "deterministic_successor": bool(deterministic),
                    "quotient_size": int(len(set(keys))),
                }

        per_observable[name] = {
            "all_chain_sizes": sorted(set(int(size) for size in sizes)),
            "carry_exact_on_every_chain": bool(carry_exact_all),
            "deterministic_successor_on_every_chain": bool(deterministic_all),
            "first_failure": first_failure,
        }

    return per_observable


def _analyze_full_modulus(m: int) -> Dict[str, object]:
    started = time.perf_counter()
    payload = _augment_rows(m)
    rows = payload["rows"]
    nonterminal_rows = [row for row in rows if not row["exit_dirs"]]

    drift_failures = []
    for row in nonterminal_rows:
        if int(row["beta_next"]) != (int(row["beta"]) - 1) % m:
            drift_failures.append(_represent_row(row))
            if len(drift_failures) >= 4:
                break

    exactness = {
        "q": _bucket_exactness(nonterminal_rows, lambda row: (tuple(row["B"]), int(row["beta"])), lambda row: int(row["q"])),
        "c": _bucket_exactness(nonterminal_rows, lambda row: (tuple(row["B"]), int(row["beta"])), lambda row: int(row["c"])),
        "epsilon4": _bucket_exactness(nonterminal_rows, lambda row: (tuple(row["B"]), int(row["beta"])), lambda row: str(row["epsilon4"])),
        "tau": _bucket_exactness(nonterminal_rows, lambda row: (tuple(row["B"]), int(row["beta"])), lambda row: int(row["tau"])),
        "next_tau": _bucket_exactness(nonterminal_rows, lambda row: (tuple(row["B"]), int(row["beta"])), lambda row: int(row["next_tau"])),
        "next_B": _bucket_exactness(nonterminal_rows, lambda row: (tuple(row["B"]), int(row["beta"])), lambda row: tuple(row["next_B"])),
    }

    chain_validation = _partition_carry_jump_chains(rows, m)
    quotient_diagnostics = _quotient_diagnostics(rows, m)

    return {
        "m": int(m),
        "row_count": int(len(rows)),
        "nonterminal_row_count": int(len(nonterminal_rows)),
        "runtime_seconds": runtime_since(started),
        "chain_validation": chain_validation,
        "beta_exactness": {
            "beta_drift_exact": bool(not drift_failures),
            "first_drift_failure": None if not drift_failures else drift_failures[0],
            "readouts": exactness,
        },
        "quotient_diagnostics": quotient_diagnostics,
    }


def _large_branch_support_for_m(m: int) -> Dict[str, object]:
    failures = []
    checked_sources = 0
    regular_targets_ok = True
    exceptional_targets_ok = True

    for source_u in range(1, m):
        family = "exceptional" if source_u == 3 else "regular"
        rho = int((source_u + 1) % m)
        target_phase, _target_dir, target_step = branch059b._family_target(m, family)
        q, w, theta = (m - 1), 1, 2
        for step in range(target_step + 1):
            s = branch059b._s_from_raw_phase(m, q=q, w=w, theta=theta, rho=rho)
            class_label = branch059b._formula_label(m, theta=theta, q=q, w=w, s=s)
            anchor = branch059b._scheduler_anchor(m, theta=theta, q=q, s=s)
            predicted_next = branch059b._projected_next_from_anchor(m, q=q, w=w, theta=theta, anchor=anchor)
            actual_next = branch059b._raw_odometer_next(m, q=q, w=w, theta=theta)
            beta = (-theta) % m
            beta_next = (-actual_next[2]) % m

            if step < target_step and class_label != "B":
                failures.append(
                    {
                        "source_u": int(source_u),
                        "step": int(step),
                        "reason": "nonterminal left B",
                        "q": int(q),
                        "w": int(w),
                        "theta": int(theta),
                        "s": int(s),
                    }
                )
                break
            if predicted_next != actual_next:
                failures.append(
                    {
                        "source_u": int(source_u),
                        "step": int(step),
                        "reason": "scheduler mismatch",
                        "q": int(q),
                        "w": int(w),
                        "theta": int(theta),
                        "s": int(s),
                    }
                )
                break
            if beta_next != (beta - 1) % m:
                failures.append(
                    {
                        "source_u": int(source_u),
                        "step": int(step),
                        "reason": "beta drift mismatch",
                        "q": int(q),
                        "w": int(w),
                        "theta": int(theta),
                    }
                )
                break
            if step == target_step:
                if family == "regular":
                    regular_targets_ok = regular_targets_ok and ((q, w, theta) == target_phase)
                else:
                    exceptional_targets_ok = exceptional_targets_ok and ((q, w, theta) == target_phase)
                checked_sources += 1
                break
            q, w, theta = actual_next

    return {
        "checked_sources": int(checked_sources),
        "all_branch_checks_exact": bool(not failures),
        "regular_targets_ok": bool(regular_targets_ok),
        "exceptional_targets_ok": bool(exceptional_targets_ok),
        "first_failure": None if not failures else failures[0],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Exhaustive support for the D5 exact reduction object and canonical beta clock.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--full-m-values", type=int, nargs="+", default=list(DEFAULT_FULL_M_VALUES))
    parser.add_argument("--branch-m-values", type=int, nargs="+", default=list(DEFAULT_BRANCH_M_VALUES))
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    full_m_values = [int(m) for m in args.full_m_values]
    branch_m_values = [int(m) for m in args.branch_m_values]

    print(f"[{TASK_ID}] full-row moduli: {full_m_values}", flush=True)
    full_results: List[Dict[str, object]] = []
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs, max_tasks_per_child=1) as pool:
            for result in pool.map(_analyze_full_modulus, full_m_values):
                print(
                    f"[{TASK_ID}] finished full m={result['m']} rows={result['row_count']} runtime={result['runtime_seconds']:.2f}s",
                    flush=True,
                )
                full_results.append(result)
    else:
        for m in full_m_values:
            result = _analyze_full_modulus(m)
            print(
                f"[{TASK_ID}] finished full m={result['m']} rows={result['row_count']} runtime={result['runtime_seconds']:.2f}s",
                flush=True,
            )
            full_results.append(result)

    print(f"[{TASK_ID}] branch-local moduli: {branch_m_values}", flush=True)
    branch_results = {}
    for m in branch_m_values:
        branch_results[str(m)] = _large_branch_support_for_m(m)
        print(f"[{TASK_ID}] finished branch m={m}", flush=True)

    full_results_by_m = {str(item["m"]): item for item in full_results}

    marked_chain_validation = {
        str(m): full_results_by_m[str(m)]["chain_validation"]
        for m in full_m_values
    }
    beta_exactness_extension = {
        str(m): full_results_by_m[str(m)]["beta_exactness"]
        for m in full_m_values
    }
    accessible_quotient_on_chain = {
        str(m): full_results_by_m[str(m)]["quotient_diagnostics"]
        for m in full_m_values
    }

    all_chain_ok = all(
        marked_chain_validation[str(m)]["all_regular_sources_ok"]
        and marked_chain_validation[str(m)]["all_regular_splices_ok"]
        for m in full_m_values
    )
    all_beta_ok = all(
        beta_exactness_extension[str(m)]["beta_drift_exact"]
        and all(entry["is_exact"] for entry in beta_exactness_extension[str(m)]["readouts"].values())
        for m in full_m_values
    )

    analysis_summary = {
        "task_id": TASK_ID,
        "full_row_moduli": full_m_values,
        "branch_only_moduli": branch_m_values,
        "all_full_chain_checks_exact": bool(all_chain_ok),
        "all_full_beta_checks_exact": bool(all_beta_ok),
        "large_branch_support_exact": bool(
            all(entry["all_branch_checks_exact"] for entry in branch_results.values())
        ),
        "main_result": (
            "The safer first exact reduction object is a marked length-m chain extracted from regular carry_jump slices. "
            "On the exhaustive full-row range, the canonical clock beta has exact unit drift and (B,beta) is exact for "
            "q, c, epsilon4, tau, next_tau, and next_B. Small chain quotients can read the carry mark, but deterministic "
            "quotients already force the full m-scale state on the marked chain. Larger-modulus branch-local support keeps "
            "the same raw phase scheduler and beta drift."
        ),
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }

    _write_json(out_dir / "analysis_summary.json", analysis_summary)
    _write_json(out_dir / "marked_chain_validation.json", marked_chain_validation)
    _write_json(out_dir / "beta_exactness_extension.json", beta_exactness_extension)
    _write_json(out_dir / "accessible_quotient_on_chain.json", accessible_quotient_on_chain)
    _write_json(out_dir / "branch_support_extension.json", branch_results)
    _write_json(args.summary_out, analysis_summary)


if __name__ == "__main__":
    main()
