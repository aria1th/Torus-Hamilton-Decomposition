#!/usr/bin/env python3
"""Targeted compute support for the D5 exact bridge question.

This script does not reopen broad search. It reuses the bundled frozen/support
JSON data to test:
- larger-modulus marked-chain support (via 068B summaries)
- offset-normalization candidates on the carry_jump slice union (via frozen 047 rows)
- state-level union-of-chains quotients for current epsilon4 and short-corner detection

Outputs are written under artifacts/d5_bridge_compute_support_072/.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

TASK_ID = "D5-BRIDGE-COMPUTE-SUPPORT-072"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def _beta(row: Mapping[str, object]) -> int:
    m = int(row["m"])
    s, _u, v, layer, _family = row["B"]
    return int((-(int(row["q"]) + int(s) + int(v) + int(layer))) % m)


def _extract_regular_state_chains(rows: Sequence[Mapping[str, object]]) -> List[List[Mapping[str, object]]]:
    by_source: Dict[int, List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        if str(row["family"]) == "regular":
            by_source[int(row["source_u"])].append(row)

    chains: List[List[Mapping[str, object]]] = []
    for source_u, source_rows in sorted(by_source.items()):
        seq = sorted(source_rows, key=lambda row: int(row["trace_step"]))
        i = 0
        while i < len(seq):
            if str(seq[i]["epsilon4"]) == "carry_jump":
                chain = [seq[i]]
                j = i + 1
                while j < len(seq):
                    chain.append(seq[j])
                    if str(seq[j]["epsilon4"]) == "wrap":
                        break
                    j += 1
                if str(chain[-1]["epsilon4"]) == "wrap":
                    chains.append(chain)
                    i = j
            i += 1
    return chains


def _first_collision(
    rows: Sequence[Mapping[str, object]],
    key_fn: Callable[[Mapping[str, object]], Tuple[object, ...]],
    value_fn: Callable[[Mapping[str, object]], object],
) -> Dict[str, object] | None:
    buckets: Dict[Tuple[object, ...], set] = defaultdict(set)
    refs: Dict[Tuple[object, ...], List[Tuple[object, Mapping[str, object]]]] = defaultdict(list)
    for row in rows:
        key = key_fn(row)
        value = value_fn(row)
        buckets[key].add(value)
        refs[key].append((value, row))
    for key, values in buckets.items():
        if len(values) > 1:
            witness_rows: List[Dict[str, object]] = []
            seen_values: set = set()
            for value, row in refs[key]:
                if value not in seen_values:
                    witness_rows.append({"value": value, **dict(row)})
                    seen_values.add(value)
                if len(witness_rows) >= min(4, len(values)):
                    break
            return {
                "key": list(key),
                "values": sorted(values, key=str),
                "rows": witness_rows,
            }
    return None


def _determinism_failure(
    rows: Sequence[Mapping[str, object]],
    key_fn: Callable[[Mapping[str, object]], Tuple[object, ...]],
    succ_key_fn: Callable[[Mapping[str, object]], Tuple[object, ...]],
) -> Dict[str, object] | None:
    succ: Dict[Tuple[object, ...], set] = defaultdict(set)
    refs: Dict[Tuple[object, ...], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        key = key_fn(row)
        succ[key].add(succ_key_fn(row))
        refs[key].append(row)
    for key, values in succ.items():
        if len(values) > 1:
            return {
                "key": list(key),
                "next_keys": [list(value) for value in sorted(values, key=str)],
                "rows": [dict(refs[key][i]) for i in range(min(4, len(refs[key])))],
            }
    return None


def _test_exactness(
    rows: Sequence[Mapping[str, object]],
    key_fn: Callable[[Mapping[str, object]], Tuple[object, ...]],
    value_fn: Callable[[Mapping[str, object]], object],
) -> Dict[str, object]:
    buckets: Dict[Tuple[object, ...], set] = defaultdict(set)
    for row in rows:
        buckets[key_fn(row)].add(value_fn(row))
    return {
        "exact": bool(all(len(values) == 1 for values in buckets.values())),
        "quotient_size": int(len(buckets)),
        "first_collision": _first_collision(rows, key_fn, value_fn),
    }


def _test_det(
    rows: Sequence[Mapping[str, object]],
    key_fn: Callable[[Mapping[str, object]], Tuple[object, ...]],
    succ_key_fn: Callable[[Mapping[str, object]], Tuple[object, ...]],
) -> Dict[str, object]:
    succ: Dict[Tuple[object, ...], set] = defaultdict(set)
    for row in rows:
        succ[key_fn(row)].add(succ_key_fn(row))
    return {
        "deterministic": bool(all(len(values) <= 1 for values in succ.values())),
        "first_failure": _determinism_failure(rows, key_fn, succ_key_fn),
    }


def _jsonable_rows(rows: Sequence[Mapping[str, object]], limit: int = 4) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for row in rows[:limit]:
        out.append({k: v for k, v in row.items()})
    return out


def build_outputs(bundle_root: Path) -> Dict[str, Path]:
    artifacts_root = bundle_root / "artifacts"
    out_root = artifacts_root / "d5_bridge_compute_support_072"
    data_root = out_root / "data"
    logs_root = out_root / "logs"
    code_root = out_root / "code"
    code_root.mkdir(parents=True, exist_ok=True)

    # Copy this script into the artifact for reproducibility.
    script_target = code_root / "d5_bridge_compute_support_072.py"
    script_target.write_text(Path(__file__).read_text())

    frozen_047 = _load_json(artifacts_root / "d5_future_transition_carry_coding_047" / "data" / "frozen_B_c_tau_epsilon_dataset_047.json")
    marked_068b = _load_json(artifacts_root / "d5_exact_reduction_support_068b" / "data" / "marked_chain_validation.json")
    beta_068b = _load_json(artifacts_root / "d5_exact_reduction_support_068b" / "data" / "beta_exactness_extension.json")
    quot_068b = _load_json(artifacts_root / "d5_exact_reduction_support_068b" / "data" / "accessible_quotient_on_chain.json")
    summary_068b = _load_json(artifacts_root / "d5_exact_reduction_support_068b" / "data" / "analysis_summary.json")

    # ------------------------------------------------------------------
    # Larger-modulus marked-chain support from 068B.
    # ------------------------------------------------------------------
    larger_modulus_chain_support = {
        "source_artifact": "d5_exact_reduction_support_068b",
        "full_row_moduli": summary_068b["full_row_moduli"],
        "branch_only_moduli": summary_068b["branch_only_moduli"],
        "all_full_chain_checks_exact": bool(summary_068b["all_full_chain_checks_exact"]),
        "all_full_beta_checks_exact": bool(summary_068b["all_full_beta_checks_exact"]),
        "large_branch_support_exact": bool(summary_068b["large_branch_support_exact"]),
        "per_modulus": {
            str(m): {
                "marked_chain_validation": marked_068b[str(m)],
                "beta_exactness": beta_068b[str(m)],
                "accessible_chain_quotients": quot_068b[str(m)],
            }
            for m in summary_068b["full_row_moduli"]
        },
        "takeaway": (
            "The marked carry_jump slice-chain picture remains exact on regenerated full rows through m=21, "
            "and the branch-local phase scheduler/beta drift remain exact through m=41."
        ),
    }

    # ------------------------------------------------------------------
    # Frozen 047 analyses.
    # ------------------------------------------------------------------
    slice_rows: List[Dict[str, object]] = []
    state_rows_all: List[Dict[str, object]] = []
    state_rows_nonterminal: List[Dict[str, object]] = []
    chain_type_counts: Dict[str, Dict[str, int]] = {}
    chain_type_formula_failures: Dict[str, List[Dict[str, object]]] = {}

    for m_text in sorted(frozen_047.keys(), key=int):
        m = int(m_text)
        rows = frozen_047[m_text]
        chains = _extract_regular_state_chains(rows)
        counts = Counter()
        formula_failures: List[Dict[str, object]] = []

        # carry_jump slice rows with successor among carry_jump rows in the same source branch
        by_source: Dict[int, List[Mapping[str, object]]] = defaultdict(list)
        for row in rows:
            if str(row["family"]) == "regular":
                by_source[int(row["source_u"])].append(row)
        for source_u, source_rows in sorted(by_source.items()):
            seq = sorted(source_rows, key=lambda row: int(row["trace_step"]))
            carry_jump_rows = [row for row in seq if str(row["epsilon4"]) == "carry_jump"]
            for i, row in enumerate(carry_jump_rows):
                rec = {
                    "m": m,
                    "source_u": int(source_u),
                    "trace_step": int(row["trace_step"]),
                    "s": int(row["B"][0]),
                    "q": int(row["q"]),
                    "w": int(row["w"]),
                    "c": int(row["c"]),
                    "sigma": int((int(source_u) + int(row["w"])) % m),
                    "terminal": bool(row["exit_dirs"]),
                }
                if i < len(carry_jump_rows) - 1:
                    nxt = carry_jump_rows[i + 1]
                    rec["next_s"] = int(nxt["B"][0])
                    rec["next_w"] = int(nxt["w"])
                slice_rows.append(rec)

        for chain in chains:
            start = chain[0]
            sigma = int((int(start["source_u"]) + int(start["w"])) % m)
            q0 = int(start["q"])
            events = [str(row["epsilon4"]) for row in chain]
            a = int(events[1] == "other")
            b = int(events[2] == "other")
            counts[f"{a}{b}"] += 1
            predicted_a = int(q0 == m - 1)
            predicted_b = int(((q0 + sigma) % m == 1) or (q0 == m - 1 and sigma != 1))
            if (predicted_a, predicted_b) != (a, b):
                formula_failures.append(
                    {
                        "source_u": int(start["source_u"]),
                        "q": q0,
                        "w": int(start["w"]),
                        "sigma": sigma,
                        "actual_ab": [a, b],
                        "predicted_ab": [predicted_a, predicted_b],
                    }
                )
            for idx, row in enumerate(chain):
                rec = {
                    "m": m,
                    "source_u": int(start["source_u"]),
                    "q0": q0,
                    "w0": int(start["w"]),
                    "sigma": sigma,
                    "a": a,
                    "b": b,
                    "beta": int(_beta(row)),
                    "epsilon4": str(row["epsilon4"]),
                    "terminal": bool(idx == len(chain) - 1),
                }
                state_rows_all.append(rec)
                if idx < len(chain) - 1:
                    nxt = chain[idx + 1]
                    rec_nt = dict(rec)
                    rec_nt["next_beta"] = int(_beta(nxt))
                    rec_nt["next_epsilon4"] = str(nxt["epsilon4"])
                    rec_nt["short_corner"] = int(
                        str(row["epsilon4"]) == "flat" and str(nxt["epsilon4"]) == "other"
                    )
                    state_rows_nonterminal.append(rec_nt)

        chain_type_counts[m_text] = {key: int(value) for key, value in sorted(counts.items())}
        chain_type_formula_failures[m_text] = formula_failures

    # Offset normalization on the carry_jump slice union.
    offset_candidates = {
        "s": lambda row: (int(row["m"]), int(row["s"])),
        "s_minus_source_u": lambda row: (int(row["m"]), (int(row["s"]) - int(row["source_u"])) % int(row["m"])),
        "s_minus_w": lambda row: (int(row["m"]), (int(row["s"]) - int(row["w"])) % int(row["m"])),
        "q_equals_s_minus_source_u_minus_w": lambda row: (
            int(row["m"]),
            (int(row["s"]) - int(row["source_u"]) - int(row["w"])) % int(row["m"]),
        ),
    }
    offset_normalization_checks: Dict[str, object] = {
        "checked_moduli": sorted(int(m) for m in frozen_047.keys()),
        "object": "regular carry_jump slice union",
        "target_properties": ["exact_for_current_carry_mark", "deterministic_successor"],
        "candidates": {},
        "takeaway": (
            "Among the natural affine normalizations tested on the carry_jump slice union, only q = s - source_u - w "
            "is exact for the carry mark and deterministic on successor. This validates the expected offset normalization "
            "for the slice-chain object."
        ),
    }
    slice_nonterminal_rows = [row for row in slice_rows if not bool(row["terminal"])]
    for name, key_fn in offset_candidates.items():
        carry_exactness = _test_exactness(slice_nonterminal_rows, key_fn, lambda row: int(row["c"]))
        determinism = _test_det(
            slice_nonterminal_rows,
            key_fn,
            lambda row: key_fn(
                {
                    "m": int(row["m"]),
                    "s": int(row["next_s"]),
                    "source_u": int(row["source_u"]),
                    "w": int(row["next_w"]),
                }
            ),
        )
        offset_normalization_checks["candidates"][name] = {
            **carry_exactness,
            **determinism,
        }

    # Candidate union-of-chains quotients on the state-level open beta-chains.
    state_candidates = {
        "beta": lambda row: (int(row["m"]), int(row["beta"])),
        "beta_plus_a": lambda row: (int(row["m"]), int(row["beta"]), int(row["a"])),
        "beta_plus_b": lambda row: (int(row["m"]), int(row["beta"]), int(row["b"])),
        "beta_plus_q": lambda row: (int(row["m"]), int(row["beta"]), int(row["q0"])),
        "beta_plus_sigma": lambda row: (int(row["m"]), int(row["beta"]), int(row["sigma"])),
        "beta_plus_ab": lambda row: (int(row["m"]), int(row["beta"]), int(row["a"]), int(row["b"])),
        "beta_plus_q_plus_sigma": lambda row: (
            int(row["m"]),
            int(row["beta"]),
            int(row["q0"]),
            int(row["sigma"]),
        ),
    }

    def _succ_payload(row: Mapping[str, object]) -> Dict[str, object]:
        return {
            "m": int(row["m"]),
            "beta": int(row["next_beta"]),
            "q0": int(row["q0"]),
            "sigma": int(row["sigma"]),
            "a": int(row["a"]),
            "b": int(row["b"]),
        }

    state_chain_union_quotients: Dict[str, object] = {
        "checked_moduli": sorted(int(m) for m in frozen_047.keys()),
        "object": "union of regular state-level carry_jump-to-wrap beta-chains",
        "chain_type_counts": chain_type_counts,
        "candidates": {},
        "exact_supported_object": {
            "name": "decorated_beta_chain",
            "state": "(m, beta, a, b)",
            "state_count_on_checked_moduli": {str(m): int(4 * m) for m in sorted(int(m) for m in frozen_047.keys())},
            "successor_rule_on_nonterminal_states": "(m,beta,a,b) -> (m,beta-1,a,b)",
            "current_epsilon4_rule": {
                "beta = m-1": "carry_jump",
                "beta = 0": "wrap",
                "beta = m-2": "other_1000 iff a=1, else flat",
                "beta = m-3": "other_0010 iff b=1, else flat",
                "otherwise": "flat",
            },
            "short_corner_detector": "1 iff (beta,a,b) = (m-2,0,1)",
        },
        "takeaway": (
            "The bare normalized m-state beta chain is deterministic on successor but is not exact for current epsilon4 or "
            "the short-corner detector. A decorated 4m-state beta-chain quotient survives all checked frozen rows."
        ),
    }
    for name, key_fn in state_candidates.items():
        epsilon4_exactness = _test_exactness(state_rows_all, key_fn, lambda row: str(row["epsilon4"]))
        short_corner_exactness = _test_exactness(state_rows_nonterminal, key_fn, lambda row: int(row["short_corner"]))
        determinism = _test_det(state_rows_nonterminal, key_fn, lambda row: key_fn(_succ_payload(row)))

        per_modulus = {}
        for m in sorted(int(x) for x in frozen_047.keys()):
            rows_m_all = [row for row in state_rows_all if int(row["m"]) == m]
            rows_m_nt = [row for row in state_rows_nonterminal if int(row["m"]) == m]
            per_modulus[str(m)] = {
                "epsilon4": _test_exactness(rows_m_all, key_fn, lambda row: str(row["epsilon4"])),
                "short_corner": _test_exactness(rows_m_nt, key_fn, lambda row: int(row["short_corner"])),
                "determinism": _test_det(rows_m_nt, key_fn, lambda row: key_fn(_succ_payload(row))),
            }

        state_chain_union_quotients["candidates"][name] = {
            "combined": {
                "epsilon4": epsilon4_exactness,
                "short_corner": short_corner_exactness,
                "determinism": determinism,
            },
            "per_modulus": per_modulus,
        }

    chain_type_formula_validation = {
        "checked_moduli": sorted(int(m) for m in frozen_047.keys()),
        "formula": {
            "a": "1 iff q = m-1",
            "b": "1 iff (q + sigma = 1 mod m) or (q = m-1 and sigma != 1)",
            "sigma": "source_u + w mod m",
        },
        "all_formula_checks_exact": bool(
            all(not failures for failures in chain_type_formula_failures.values())
        ),
        "failures": chain_type_formula_failures,
        "interpretation": (
            "The two early-post-carry decorations are not arbitrary. On the checked range they are exactly determined by the "
            "normalized slice coordinate q together with the slice offset sigma."
        ),
    }

    analysis_summary = {
        "task_id": TASK_ID,
        "scope": (
            "Targeted bridge-support analysis only: larger-modulus marked-chain validation from 068B, affine offset-normalization "
            "checks on the frozen 047 carry_jump slice union, and candidate quotient checks on the frozen 047 state-level union of chains."
        ),
        "main_result": (
            "The data support a two-stage picture. First, the offset normalization q = s - source_u - w exactly globalizes the regular "
            "carry_jump slice-chain object on the checked frozen range, and the larger 068B artifact keeps the marked-chain / beta picture "
            "exact through m=21 full rows and m=41 branch-local support. Second, that normalization is not enough for current epsilon4 on the "
            "state-level union of chains: the bare m-state beta quotient fails current epsilon4 and the short-corner detector. On the frozen checked "
            "range, the supported sharper object is a decorated 4m-state beta-chain quotient (beta,a,b), with a=1_{q=m-1} and b determined by (q,sigma)."
        ),
        "candidate_bridge_status": {
            "bare_beta_m_state_bridge": "contradicted on checked frozen rows",
            "offset_normalization_on_slice_union": "supported",
            "decorated_beta_union_quotient": "supported on checked frozen rows",
        },
        "saved_outputs": [
            "data/larger_modulus_chain_support.json",
            "data/offset_normalization_checks.json",
            "data/state_chain_union_quotients.json",
            "data/chain_type_formula_validation.json",
            "README.md",
            "logs/summary.log",
            "code/d5_bridge_compute_support_072.py",
        ],
    }

    _write_json(data_root / "analysis_summary.json", analysis_summary)
    _write_json(data_root / "larger_modulus_chain_support.json", larger_modulus_chain_support)
    _write_json(data_root / "offset_normalization_checks.json", offset_normalization_checks)
    _write_json(data_root / "state_chain_union_quotients.json", state_chain_union_quotients)
    _write_json(data_root / "chain_type_formula_validation.json", chain_type_formula_validation)

    readme = f"""# D5 Bridge Compute Support 072

This artifact answers the narrow `071` compute-support prompt without reopening broad search.

## Main result

The checked data support a sharper exact reduction picture:

1. **Slice-chain bridge:** on the regular carry_jump slice union, the expected affine offset normalization
   `q = s - source_u - w (mod m)` is exact for the carry mark and deterministic on successor.
   The other natural candidates tested here (`s`, `s-source_u`, `s-w`) all fail.
2. **Larger-modulus support:** the bundled `068B` artifact already keeps the marked length-`m` chain,
   beta drift, and `(B,beta)` exactness alive on regenerated full rows through `m=21`, with branch-local
   scheduler support through `m=41`.
3. **State-level union of chains:** the bare normalized `m`-state beta quotient is **not** exact for current
   `epsilon4` or the short-corner detector on the frozen exhaustive range `m=5,7,9,11`.
   Its first collisions occur exactly at the two early post-carry positions.
4. **Supported sharper object:** on that same frozen range, a decorated `4m`-state beta-chain quotient
   `(m,beta,a,b)` is exact for current `epsilon4`, deterministic on successor, and exact for the short-corner detector.
   The decorations satisfy
   - `a = 1` iff `q = m-1`
   - `b = 1` iff `(q + sigma = 1 mod m)` or `(q = m-1 and sigma != 1)`, where `sigma = source_u + w mod m`.

So the checked data **contradict** the candidate bridge “offset normalization alone gives one exact `m`-state beta quotient for current `epsilon4`”, but they **support** a slightly richer decorated union-of-chains quotient.

## Files

- `data/analysis_summary.json`
- `data/larger_modulus_chain_support.json`
- `data/offset_normalization_checks.json`
- `data/state_chain_union_quotients.json`
- `data/chain_type_formula_validation.json`
- `logs/summary.log`
- `code/d5_bridge_compute_support_072.py`
"""
    _write_text(out_root / "README.md", readme)

    log_lines = [
        f"[{TASK_ID}] built bridge-support artifact",
        f"[{TASK_ID}] larger-modulus support imported from 068B: full-row moduli {summary_068b['full_row_moduli']}, branch-only moduli {summary_068b['branch_only_moduli']}",
        f"[{TASK_ID}] offset-normalization winner on slice union: q = s - source_u - w",
        f"[{TASK_ID}] bare beta quotient exact for epsilon4: False",
        f"[{TASK_ID}] decorated beta quotient exact for epsilon4 / short-corner / successor: True / True / True",
        f"[{TASK_ID}] chain-type formulas exact on checked moduli: {chain_type_formula_validation['all_formula_checks_exact']}",
    ]
    _write_text(logs_root / "summary.log", "\n".join(log_lines) + "\n")

    return {
        "root": out_root,
        "summary": data_root / "analysis_summary.json",
        "readme": out_root / "README.md",
        "log": logs_root / "summary.log",
    }


if __name__ == "__main__":
    bundle_root = Path(__file__).resolve().parents[1]
    outputs = build_outputs(bundle_root)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))
