#!/usr/bin/env python3
"""Compare countdown-carrier provenance candidates against the theorem-side key."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, List, Mapping, MutableMapping, Sequence, Tuple

import torus_nd_d5_deep_transition_carry_sheet as carry046
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-LOCAL-PROVENANCE-COMPARE-127"
DEFAULT_M_VALUES = (11, 13, 15, 17, 19, 21, 23, 25)

FLAT = "flat"
WRAP = "wrap"
CJ = "carry_jump"
OTHA = "other_1000"
OTHB = "other_0010"


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _event_class(dn: Sequence[int]) -> str:
    dn_tuple = tuple(int(value) for value in dn)
    if dn_tuple == (0, 0, 0, 1):
        return FLAT
    if dn_tuple == (0, 0, 0, 0):
        return WRAP
    if dn_tuple == (1, 1, 0, 0):
        return CJ
    if dn_tuple == (1, 0, 0, 0):
        return OTHA
    if dn_tuple == (0, 0, 1, 0):
        return OTHB
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
    out = {
        "m": int(row["m"]),
        "source_u": int(row["source_u"]),
        "family": str(row["family"]),
        "trace_step": int(row["trace_step"]),
        "B": _jsonable(tuple(row["B"])),
        "beta": int(row["beta"]),
        "q0": int(row["q0"]),
        "sigma": int(row["sigma"]),
        "epsilon4": str(row["epsilon4"]),
        "tau": int(row["tau"]),
        "future_binary_after_current_7": list(row["future_binary_after_current_7"]),
    }
    if row.get("has_next"):
        out["next_B"] = _jsonable(tuple(row["next_B"]))
        out["next_beta"] = int(row["next_beta"])
        out["next_q0"] = int(row["next_q0"])
        out["next_sigma"] = int(row["next_sigma"])
        out["next_epsilon4"] = str(row["next_epsilon4"])
    return out


def _pair_event(beta: int, q: int, m: int) -> str:
    if beta == m - 1:
        return CJ
    if beta == 0:
        return WRAP
    if beta == m - 2 and q == m - 1:
        return OTHA
    return FLAT


def _pair_successor(beta: int, q: int, m: int) -> Tuple[int, int]:
    if beta > 0:
        return (beta - 1, q)
    return (m - 1, (q + 1) % m)


def _precompute_pair_features(m: int) -> Dict[Tuple[int, int], Dict[str, object]]:
    out: Dict[Tuple[int, int], Dict[str, object]] = {}
    for beta in range(m):
        for q in range(m):
            event = _pair_event(beta, q, m)
            tau = 0
            if event == FLAT:
                cur_beta, cur_q = beta, q
                while _pair_event(cur_beta, cur_q, m) == FLAT:
                    tau += 1
                    cur_beta, cur_q = _pair_successor(cur_beta, cur_q, m)
                    if tau > m + 2:
                        raise AssertionError("flat-run exceeded expected odd-m bound")

            future_bits: List[int] = []
            cur_beta, cur_q = beta, q
            for _ in range(7):
                cur_beta, cur_q = _pair_successor(cur_beta, cur_q, m)
                future_bits.append(1 if _pair_event(cur_beta, cur_q, m) == FLAT else 0)

            out[(beta, q)] = {
                "tau": int(tau),
                "future_binary_after_current_7": tuple(int(bit) for bit in future_bits),
            }
    return out


def _extract_marked_rows(m: int) -> List[Dict[str, object]]:
    payload = carry046._build_active_data(m)
    rows = sorted(
        payload["active_rows"],
        key=lambda row: (int(row["source_u"]), str(row["family"]), int(row["trace_step"])),
    )
    by_branch: Dict[Tuple[int, str], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        by_branch[(int(row["source_u"]), str(row["family"]))].append(row)

    pair_features = _precompute_pair_features(m)
    out: List[Dict[str, object]] = []

    for (source_u, family), seq in sorted(by_branch.items()):
        branch_rows: List[Dict[str, object]] = []
        i = 0
        while i < len(seq):
            if _event_class(seq[i]["dn"]) != CJ:
                i += 1
                continue

            start = seq[i]
            q0 = int(start["q"])
            sigma = int((int(source_u) + int(start["w"])) % m)
            j = i
            while j < len(seq):
                row = seq[j]
                beta = int(_beta(row, m))
                feature = pair_features[(beta, q0)]
                branch_rows.append(
                    {
                        "m": int(m),
                        "source_u": int(source_u),
                        "family": str(family),
                        "trace_step": int(row["trace_step"]),
                        "B": tuple(row["B"]),
                        "beta": int(beta),
                        "q0": int(q0),
                        "sigma": int(sigma),
                        "epsilon4": str(_event_class(row["dn"])),
                        "tau": int(feature["tau"]),
                        "future_binary_after_current_7": tuple(
                            feature["future_binary_after_current_7"]
                        ),
                    }
                )
                if _event_class(row["dn"]) == WRAP:
                    break
                j += 1

            i = j + 1

        for idx, rec in enumerate(branch_rows):
            rec["has_next"] = bool(idx + 1 < len(branch_rows))
            if idx + 1 < len(branch_rows):
                next_row = branch_rows[idx + 1]
                rec["next_B"] = tuple(next_row["B"])
                rec["next_beta"] = int(next_row["beta"])
                rec["next_q0"] = int(next_row["q0"])
                rec["next_sigma"] = int(next_row["sigma"])
                rec["next_epsilon4"] = str(next_row["epsilon4"])
                rec["next_tau"] = int(next_row["tau"])
                rec["next_future_binary_after_current_7"] = tuple(
                    next_row["future_binary_after_current_7"]
                )
            out.append(rec)

    return out


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
                    "values": [_jsonable(value) for value in sorted(values, key=str)[:8]],
                    "rows": [_represent_row(refs[key][idx]) for idx in range(min(4, len(refs[key])))],
                }

    return {
        "is_exact": bool(collision_bucket_count == 0),
        "bucket_count": int(len(buckets)),
        "collision_bucket_count": int(collision_bucket_count),
        "first_collision": first,
    }


def _fiber_profile(rows, key_getter, value_getter) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], set] = defaultdict(set)
    bucket_rows: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        key = key_getter(row)
        buckets[key].add(value_getter(row))
        bucket_rows[key].append(row)

    size_hist = Counter(len(values) for values in buckets.values())
    max_fiber = max(size_hist) if size_hist else 0
    ambiguous = [key for key, values in buckets.items() if len(values) > 1]
    first = None
    if ambiguous:
        key = ambiguous[0]
        first = {
            "key": _jsonable(key),
            "fiber_size": int(len(buckets[key])),
            "values": [_jsonable(value) for value in sorted(buckets[key], key=str)[:8]],
            "rows": [_represent_row(bucket_rows[key][idx]) for idx in range(min(4, len(bucket_rows[key])))],
        }

    return {
        "bucket_count": int(len(buckets)),
        "max_fiber_size": int(max_fiber),
        "fiber_size_histogram": {
            str(size): int(count)
            for size, count in sorted(size_hist.items())
        },
        "ambiguous_bucket_count": int(len(ambiguous)),
        "first_ambiguous_bucket": first,
    }


def _candidate_key_tau(row: Mapping[str, object]) -> Tuple[object, ...]:
    return (
        tuple(row["B"]),
        int(min(int(row["tau"]), 8)),
        str(row["epsilon4"]),
    )


def _candidate_key_fw(row: Mapping[str, object]) -> Tuple[object, ...]:
    return (
        tuple(row["B"]),
        str(row["epsilon4"]),
        *tuple(int(value) for value in row["future_binary_after_current_7"]),
    )


def _first_cj_time_from_bucket(start_key, succ_map, eps_map, m: int) -> int | None:
    cur = start_key
    for t in range(m + 2):
        eps = eps_map.get(cur)
        if eps is None:
            return None
        if eps == CJ:
            return t
        nxt = succ_map.get(cur)
        if nxt is None:
            return None
        cur = nxt
    return None


def _analyze_candidate(rows: Sequence[Mapping[str, object]], key_getter, m: int, name: str) -> Dict[str, object]:
    theorem_key = lambda row: (tuple(row["B"]), int(row["beta"]))
    bucket_to_eps = _bucket_exactness(rows, key_getter, lambda row: str(row["epsilon4"]))
    bucket_to_B = _bucket_exactness(rows, key_getter, lambda row: tuple(row["B"]))
    bucket_to_theorem = _bucket_exactness(rows, key_getter, theorem_key)

    state_count: Counter[Tuple[object, ...]] = Counter()
    beta_values: Dict[Tuple[object, ...], set] = defaultdict(set)
    eps_values: Dict[Tuple[object, ...], set] = defaultdict(set)
    succ_map_sets: Dict[Tuple[object, ...], set] = defaultdict(set)
    refs: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)

    for row in rows:
        key = key_getter(row)
        state_count[key] += 1
        beta_values[key].add(int(row["beta"]))
        eps_values[key].add(str(row["epsilon4"]))

    rows_with_next = [row for row in rows if row.get("has_next")]
    for row in rows_with_next:
        key = key_getter(row)
        next_key = key_getter(
            {
                "B": row["next_B"],
                "epsilon4": row["next_epsilon4"],
                "tau": row["next_tau"],
                "future_binary_after_current_7": row["next_future_binary_after_current_7"],
            }
        )
        succ_map_sets[key].add(next_key)
        refs[key].append(row)

    successor_first = None
    successor_failures = 0
    for key, values in succ_map_sets.items():
        if len(values) > 1:
            successor_failures += 1
            if successor_first is None:
                successor_first = {
                    "key": _jsonable(key),
                    "next_keys": [_jsonable(value) for value in sorted(values, key=str)[:8]],
                    "rows": [_represent_row(refs[key][idx]) for idx in range(min(4, len(refs[key])))],
                }
    successor = {
        "is_deterministic": bool(successor_failures == 0),
        "bucket_count": int(len(succ_map_sets)),
        "failure_bucket_count": int(successor_failures),
        "first_failure": successor_first,
    }

    bucket_eps_map = {}
    bucket_succ_map = {}
    for key, values in eps_values.items():
        if len(values) == 1:
            bucket_eps_map[key] = next(iter(values))
    for key, values in succ_map_sets.items():
        if len(values) == 1:
            bucket_succ_map[key] = next(iter(values))

    realized_beta_map: Dict[Tuple[object, ...], int | None] = {}
    realized_beta_failure = None
    for key in state_count:
        t = _first_cj_time_from_bucket(key, bucket_succ_map, bucket_eps_map, m)
        if t is None:
            realized_beta_map[key] = None
            if realized_beta_failure is None:
                realized_beta_failure = {"key": _jsonable(key), "reason": "no_deterministic_cj_recovery"}
        else:
            realized_beta_map[key] = int(m - 1 if t == 0 else t - 1)

    direct_phase_fiber = _fiber_profile(rows, key_getter, lambda row: int(row["beta"]))
    theorem_fiber = _fiber_profile(rows, key_getter, theorem_key)
    rq_fiber = _fiber_profile(
        rows,
        lambda row: (key_getter(row), realized_beta_map[key_getter(row)]),
        theorem_key,
    )

    bucket_ids: Dict[Tuple[object, ...], int] = {
        key: idx for idx, key in enumerate(sorted(state_count.keys(), key=str))
    }
    sample_buckets = []
    for key in sorted(state_count.keys(), key=str)[: min(12, len(state_count))]:
        next_ids = sorted(bucket_ids[nxt] for nxt in succ_map_sets.get(key, set()) if nxt in bucket_ids)
        sample_buckets.append(
            {
                "bucket_id": int(bucket_ids[key]),
                "key": _jsonable(key),
                "state_count": int(state_count[key]),
                "beta_values": sorted(int(value) for value in beta_values[key]),
                "epsilon4_values": sorted(str(value) for value in eps_values[key]),
                "next_bucket_ids": next_ids,
                "realized_beta_from_quotient": realized_beta_map[key],
            }
        )

    candidate_success = (
        bucket_to_eps["is_exact"]
        and bucket_to_B["is_exact"]
        and successor["is_deterministic"]
        and rq_fiber["max_fiber_size"] == 1
    )

    return {
        "candidate_name": name,
        "epsilon4_exactness": bucket_to_eps,
        "successor_determinism": successor,
        "grouped_base_retention": bucket_to_B,
        "direct_candidate_to_theorem_exactness": bucket_to_theorem,
        "phase_fiber_profile_over_candidate": direct_phase_fiber,
        "theorem_key_fiber_profile_over_candidate": theorem_fiber,
        "realized_clock_recovery": {
            "first_failure": realized_beta_failure,
            "rq_to_theorem_fiber_profile": rq_fiber,
        },
        "acceptance_success_A": bool(candidate_success),
        "sample_bucket_table": sample_buckets,
    }


def _analyze_modulus(m: int) -> Dict[str, object]:
    started = time.perf_counter()
    rows = _extract_marked_rows(m)
    result = {
        "m": int(m),
        "runtime_seconds": runtime_since(started),
        "marked_state_count": int(len(rows)),
        "q_tau": _analyze_candidate(rows, _candidate_key_tau, m, "Q_tau = (B, min(tau,8), epsilon4)"),
        "q_fw": _analyze_candidate(rows, _candidate_key_fw, m, "Q_fw = (B, epsilon4, f1..f7)"),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare countdown-carrier local quotients to the theorem-side D5 key.")
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
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            for result in pool.map(_analyze_modulus, m_values):
                print(
                    f"[{TASK_ID}] finished m={result['m']} states={result['marked_state_count']}",
                    flush=True,
                )
                results.append(result)
    else:
        for m in m_values:
            result = _analyze_modulus(m)
            print(
                f"[{TASK_ID}] finished m={result['m']} states={result['marked_state_count']}",
                flush=True,
            )
            results.append(result)

    results.sort(key=lambda item: int(item["m"]))
    by_m = {str(item["m"]): item for item in results}

    def _all(candidate_field: str, path: Sequence[str]) -> bool:
        ok = True
        for item in results:
            node = item[candidate_field]
            for key in path:
                node = node[key]
            if not bool(node):
                ok = False
        return ok

    def _first_modulus_with_fiber_gt_one(candidate_field: str) -> int | None:
        for item in results:
            if int(item[candidate_field]["phase_fiber_profile_over_candidate"]["max_fiber_size"]) > 1:
                return int(item["m"])
        return None

    summary = {
        "task_id": TASK_ID,
        "checked_moduli": m_values,
        "all_q_tau_success_A": _all("q_tau", ("acceptance_success_A",)),
        "all_q_fw_success_A": _all("q_fw", ("acceptance_success_A",)),
        "all_q_tau_successor_exact": _all("q_tau", ("successor_determinism", "is_deterministic")),
        "all_q_fw_successor_exact": _all("q_fw", ("successor_determinism", "is_deterministic")),
        "all_q_tau_retain_B": _all("q_tau", ("grouped_base_retention", "is_exact")),
        "all_q_fw_retain_B": _all("q_fw", ("grouped_base_retention", "is_exact")),
        "first_q_tau_phase_fiber_gt_one": _first_modulus_with_fiber_gt_one("q_tau"),
        "first_q_fw_phase_fiber_gt_one": _first_modulus_with_fiber_gt_one("q_fw"),
        "main_result": (
            "This run compares the historical countdown-carrier candidates Q_tau=(B,min(tau,8),epsilon4) "
            "and Q_fw=(B,epsilon4,f1,...,f7) directly against the theorem-side key (B,beta) on the regenerated "
            "carry-jump-to-wrap exact marked object."
        ),
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }

    details = {
        "summary": summary,
        "per_modulus": by_m,
    }

    _write_json(out_dir / "analysis_summary.json", summary)
    _write_json(out_dir / "per_modulus.json", by_m)
    _write_json(args.summary_out, summary)
    _write_json(out_dir / "details.json", details)


if __name__ == "__main__":
    main()
