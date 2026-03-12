#!/usr/bin/env python3
"""Session 37 / artifact 018 reduced skew-odometer extraction for the D5 mixed witness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from torus_nd_d5_return_map_model_common import (
    environment_block,
    extract_first_return_table,
    extract_grouped_return,
    load_witness_specs,
    prepare_witness,
    runtime_since,
    deterministic_quotient_R,
    deterministic_quotient_U,
)

TASK_ID = "D5-MIXED-SKEW-ODOMETER-NORMAL-FORM-018"
INSPECTED_M_VALUES = (5, 7, 9, 11, 13)
EXTENDED_M_VALUES = (15, 17, 19)


def _load_json(path: str | Path) -> Dict[str, object]:
    return json.loads(Path(path).read_text())


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _sorted_unique(values: Iterable[Tuple[int, ...]]) -> List[Tuple[int, ...]]:
    return sorted(set(values))


def _indicator(flag: bool) -> int:
    return 1 if flag else 0


def _phi_formula(s: int, m: int) -> int:
    return (2 + _indicator(s == 1) - 2 * _indicator(s == 2) - _indicator(s == 3)) % m


def _phi_local_formula(s: int, m: int) -> int:
    return (2 - 2 * _indicator(s == 2)) % m


def _phi_pure_formula(s: int, m: int) -> int:
    return (-2 * _indicator(s == 2)) % m


def _local_gauge(s: int) -> int:
    return _indicator(s in (2, 3))


def _linear_gauge(s: int, m: int) -> int:
    return (2 * s) % m


def _state_classes(raw_classes: Mapping[str, Sequence[Sequence[int]]]) -> Dict[int, List[Tuple[int, ...]]]:
    return {int(k): [tuple(int(v) for v in state) for state in members] for k, members in raw_classes.items()}


def _verify_first_return_reduction(
    first_return: Mapping[str, object], quotient_r: Mapping[str, object], *, m: int
) -> Dict[str, object]:
    classes = _state_classes(quotient_r["classes"])
    transitions = {int(k): int(v) for k, v in quotient_r["transitions"].items()}
    class_to_qs: Dict[int, Tuple[int, int]] = {}
    for class_id, members in classes.items():
        qs_set = {(q, (w + u) % m) for (q, w, u) in members}
        if len(qs_set) != 1:
            raise AssertionError(f"quotient_R class {class_id} is not constant on (q,s) at m={m}: {qs_set}")
        class_to_qs[class_id] = next(iter(qs_set))

    qs_to_class: Dict[Tuple[int, int], int] = {}
    for class_id, qs in class_to_qs.items():
        if qs in qs_to_class:
            raise AssertionError(f"duplicate class for (q,s)={qs} at m={m}")
        qs_to_class[qs] = class_id
    if len(qs_to_class) != m * m:
        raise AssertionError(f"expected m^2 quotient_R classes at m={m}, got {len(qs_to_class)}")

    reduced_rows = []
    output_rows = []
    state_rows = first_return["states"]
    reduced_output: Dict[Tuple[int, int], Tuple[int, Tuple[int, ...]]] = {}
    for row in state_rows.values():
        q = int(row["q"])
        w = int(row["w"])
        u = int(row["u"])
        s = (w + u) % m
        dv = int(row["dv"])
        low_word = tuple(int(v) for v in row["representative_low_layer_word"])
        key = (q, s)
        if key in reduced_output and reduced_output[key] != (dv, low_word):
            raise AssertionError(f"first-return output depends on more than (q,s) at m={m}, key={key}")
        reduced_output[key] = (dv, low_word)

    for q in range(m):
        for s in range(m):
            class_id = qs_to_class[(q, s)]
            next_class = transitions[class_id]
            next_q, next_s = class_to_qs[next_class]
            expected_next = ((q + 1) % m, (s + 1 + _indicator(q == m - 2)) % m)
            if (next_q, next_s) != expected_next:
                raise AssertionError(
                    f"reduced first-return transition mismatch at m={m}, (q,s)={(q,s)}: "
                    f"actual={(next_q,next_s)} expected={expected_next}"
                )
            dv, low_word = reduced_output[(q, s)]
            expected_dv = _indicator((q != m - 2 and s == 1) or (q == m - 2 and s != 0))
            if dv != expected_dv:
                raise AssertionError(
                    f"reduced first-return dv mismatch at m={m}, (q,s)={(q,s)}: actual={dv} expected={expected_dv}"
                )
            expected_low_word = [1, 4, 2 if q == m - 2 else 0, 3 if dv == 1 else 0]
            if list(low_word) != expected_low_word:
                raise AssertionError(
                    f"reduced first-return low word mismatch at m={m}, (q,s)={(q,s)}: "
                    f"actual={list(low_word)} expected={expected_low_word}"
                )
            reduced_rows.append(
                {
                    "q": q,
                    "s": s,
                    "next_q": next_q,
                    "next_s": next_s,
                    "dw_carry": _indicator(q == m - 2),
                    "dv": dv,
                    "low_layer_word": list(low_word),
                }
            )
            output_rows.append({"q": q, "s": s, "dv": dv, "low_layer_word": list(low_word)})

    return {
        "m": m,
        "class_count": len(classes),
        "quotient_coordinate": "(q,s) with s=w+u mod m",
        "transition_formula": "R_red(q,s)=(q+1, s+1+1_{q=m-2})",
        "dv_formula": "dv(q,s)=1 iff ((q!=m-2 and s=1) or (q=m-2 and s!=0))",
        "low_layer_word_formula": "(1,4,2*1_{q=m-2},3*dv)",
        "rows": reduced_rows,
        "distinct_low_layer_words": [list(word) for word in _sorted_unique(tuple(row["low_layer_word"]) for row in reduced_rows)],
    }


def _verify_grouped_reduction(
    grouped_return: Mapping[str, object], quotient_u: Mapping[str, object], *, m: int
) -> Dict[str, object]:
    classes = _state_classes(quotient_u["classes"])
    transitions = {int(k): int(v) for k, v in quotient_u["transitions"].items()}
    class_to_s: Dict[int, int] = {}
    for class_id, members in classes.items():
        s_set = {(w + u) % m for (w, u) in members}
        if len(s_set) != 1:
            raise AssertionError(f"quotient_U class {class_id} is not constant on s at m={m}: {s_set}")
        class_to_s[class_id] = next(iter(s_set))

    s_to_class: Dict[int, int] = {}
    for class_id, s in class_to_s.items():
        if s in s_to_class:
            raise AssertionError(f"duplicate class for s={s} at m={m}")
        s_to_class[s] = class_id
    if len(s_to_class) != m:
        raise AssertionError(f"expected m quotient_U classes at m={m}, got {len(s_to_class)}")

    grouped_rows = grouped_return["states"]
    reduced_output: Dict[int, Tuple[int, Tuple[Tuple[int, ...], ...]]] = {}
    for row in grouped_rows.values():
        s = (int(row["w"]) + int(row["u"])) % m
        sig = (
            int(row["phi"]),
            tuple(tuple(int(v) for v in word) for word in row["grouped_low_layer_trace"]),
        )
        if s in reduced_output and reduced_output[s] != sig:
            raise AssertionError(f"grouped output depends on more than s at m={m}, s={s}")
        reduced_output[s] = sig

    reduced_rows = []
    gauge_rows = []
    phi_values = []
    for s in range(m):
        class_id = s_to_class[s]
        next_s = class_to_s[transitions[class_id]]
        expected_next_s = (s + 1) % m
        if next_s != expected_next_s:
            raise AssertionError(
                f"grouped reduced transition mismatch at m={m}, s={s}: actual={next_s} expected={expected_next_s}"
            )
        phi, trace = reduced_output[s]
        expected_phi = _phi_formula(s, m)
        if phi != expected_phi:
            raise AssertionError(f"grouped phi mismatch at m={m}, s={s}: actual={phi} expected={expected_phi}")
        g = _local_gauge(s)
        g_next = _local_gauge((s + 1) % m)
        phi_local = (phi + g - g_next) % m
        if phi_local != _phi_local_formula(s, m):
            raise AssertionError(
                f"local gauge mismatch at m={m}, s={s}: actual={phi_local} expected={_phi_local_formula(s,m)}"
            )
        h = _linear_gauge(s, m)
        h_next = _linear_gauge((s + 1) % m, m)
        phi_pure = (phi_local + h - h_next) % m
        if phi_pure != _phi_pure_formula(s, m):
            raise AssertionError(
                f"linear gauge mismatch at m={m}, s={s}: actual={phi_pure} expected={_phi_pure_formula(s,m)}"
            )
        phi_values.append(phi)
        reduced_rows.append(
            {
                "s": s,
                "next_s": next_s,
                "phi": phi,
                "grouped_low_layer_trace": [list(word) for word in trace],
            }
        )
        gauge_rows.append(
            {
                "s": s,
                "phi": phi,
                "g_local": g,
                "phi_after_local_gauge": phi_local,
                "h_linear": h,
                "phi_pure_one_defect": phi_pure,
            }
        )

    cycle_sum = sum(phi_values) % m
    expected_cycle_sum = (m - 2) % m
    if cycle_sum != expected_cycle_sum:
        raise AssertionError(f"grouped phi orbit sum mismatch at m={m}: actual={cycle_sum} expected={expected_cycle_sum}")

    return {
        "m": m,
        "class_count": len(classes),
        "quotient_coordinate": "s=w+u mod m",
        "transition_formula": "U_red(s)=s+1",
        "phi_formula": "phi(s)=2+1_{s=1}-2*1_{s=2}-1_{s=3} (mod m)",
        "cycle_sum_formula": "sum_s phi(s) = m-2 (mod m)",
        "rows": reduced_rows,
        "gauge_rows": gauge_rows,
        "phi_values": phi_values,
    }


def _saved_table_paths(witness: str, m: int) -> Dict[str, Path]:
    base = Path("artifacts/d5_return_map_model_017/data/tables")
    return {
        "first_return": base / f"{witness}_m{m}_first_return.json",
        "grouped_return": base / f"{witness}_m{m}_grouped_return.json",
        "quotient_R": base / f"{witness}_m{m}_quotient_R.json",
        "quotient_U": base / f"{witness}_m{m}_quotient_U.json",
    }


def analyse_saved_mixed_tables(m_values: Sequence[int], *, out_dir: Path) -> Dict[str, object]:
    reports = []
    for m in m_values:
        paths = _saved_table_paths("mixed_008", m)
        first_return = _load_json(paths["first_return"])
        grouped_return = _load_json(paths["grouped_return"])
        quotient_r = _load_json(paths["quotient_R"])
        quotient_u = _load_json(paths["quotient_U"])
        reduced_r = _verify_first_return_reduction(first_return, quotient_r, m=m)
        reduced_u = _verify_grouped_reduction(grouped_return, quotient_u, m=m)
        reduced_r_path = out_dir / "saved_table_reductions" / f"mixed_008_m{m}_reduced_first_return.json"
        reduced_u_path = out_dir / "saved_table_reductions" / f"mixed_008_m{m}_reduced_grouped_return.json"
        _write_json(reduced_r_path, reduced_r)
        _write_json(reduced_u_path, reduced_u)
        reports.append(
            {
                "m": m,
                "evidence_type": "saved_017_tables",
                "reduced_first_return_file": str(reduced_r_path),
                "reduced_grouped_return_file": str(reduced_u_path),
                "first_return_class_count": reduced_r["class_count"],
                "grouped_return_class_count": reduced_u["class_count"],
                "phi_values": reduced_u["phi_values"],
            }
        )
    return {"m_values": list(m_values), "reports": reports}


def analyse_direct_mixed_replay(m_values: Sequence[int], *, out_dir: Path) -> Dict[str, object]:
    specs = {spec.name: spec for spec in load_witness_specs()}
    prepared = prepare_witness(specs["mixed_008"], m_values)
    reports = []
    for m in m_values:
        pre = prepared.pre_by_m[m]
        nexts0 = prepared.nexts0_by_m[m]
        dir_row = prepared.dir_by_m[m]
        first_return = extract_first_return_table(pre, nexts0, dir_row)
        grouped_return = extract_grouped_return(first_return)
        quotient_r = deterministic_quotient_R(first_return)
        quotient_u = deterministic_quotient_U(grouped_return)
        reduced_r = _verify_first_return_reduction(first_return, quotient_r, m=m)
        reduced_u = _verify_grouped_reduction(grouped_return, quotient_u, m=m)
        reduced_r_path = out_dir / "direct_replay_reductions" / f"mixed_008_m{m}_reduced_first_return.json"
        reduced_u_path = out_dir / "direct_replay_reductions" / f"mixed_008_m{m}_reduced_grouped_return.json"
        quotient_r_path = out_dir / "direct_replay_reductions" / f"mixed_008_m{m}_quotient_R.json"
        quotient_u_path = out_dir / "direct_replay_reductions" / f"mixed_008_m{m}_quotient_U.json"
        _write_json(reduced_r_path, reduced_r)
        _write_json(reduced_u_path, reduced_u)
        _write_json(quotient_r_path, quotient_r)
        _write_json(quotient_u_path, quotient_u)
        reports.append(
            {
                "m": m,
                "evidence_type": "direct_replay_from_mixed_008_rule",
                "reduced_first_return_file": str(reduced_r_path),
                "reduced_grouped_return_file": str(reduced_u_path),
                "quotient_R_file": str(quotient_r_path),
                "quotient_U_file": str(quotient_u_path),
                "first_return_class_count": reduced_r["class_count"],
                "grouped_return_class_count": reduced_u["class_count"],
                "phi_values": reduced_u["phi_values"],
            }
        )
    return {"m_values": list(m_values), "reports": reports}


def analyse_controls_from_017(m_values: Sequence[int], *, out_dir: Path) -> Dict[str, object]:
    summary_017 = _load_json("artifacts/d5_return_map_model_017/data/analysis_summary.json")
    by_name = {block["witness"]["name"]: block for block in summary_017["witnesses"]}
    rows = []
    for witness_name in ["monodromy_008", "cycle_007", "anti_mixed_010"]:
        block = by_name[witness_name]
        for report in block["reports_by_m"]:
            if report["m"] not in m_values:
                continue
            quotient_u = _load_json(_saved_table_paths(witness_name, report["m"])["quotient_U"])
            grouped_return = _load_json(_saved_table_paths(witness_name, report["m"])["grouped_return"])
            s_only_output = True
            grouped_output_by_s: Dict[int, Tuple[int, Tuple[Tuple[int, ...], ...]]] = {}
            m = int(report["m"])
            for row in grouped_return["states"].values():
                s = (int(row["w"]) + int(row["u"])) % m
                sig = (
                    int(row["phi"]),
                    tuple(tuple(int(v) for v in word) for word in row["grouped_low_layer_trace"]),
                )
                if s in grouped_output_by_s and grouped_output_by_s[s] != sig:
                    s_only_output = False
                    break
                grouped_output_by_s[s] = sig
            rows.append(
                {
                    "witness": witness_name,
                    "m": m,
                    "grouped_model_kind": report["U_models"]["grouped_model_classification"]["kind"],
                    "quotient_R_class_count": int(report["quotient_R"]["class_count"]),
                    "quotient_U_class_count": int(quotient_u["class_count"]),
                    "grouped_output_depends_only_on_s": s_only_output,
                    "cycle_count": report["grouped_return_summary"]["cycle_count"],
                    "cycle_monodromies": report["grouped_return_summary"]["cycle_monodromies"],
                }
            )
    out = {"m_values": list(m_values), "rows": rows}
    _write_json(out_dir / "control_comparison.json", out)
    return out


def compare_saved_vs_direct(saved_block: Mapping[str, object], direct_block: Mapping[str, object]) -> Dict[str, object]:
    saved_by_m = {int(row["m"]): row for row in saved_block["reports"]}
    direct_by_m = {int(row["m"]): row for row in direct_block["reports"]}
    rows = []
    for m in sorted(saved_by_m):
        row = {
            "m": m,
            "same_first_return_class_count": saved_by_m[m]["first_return_class_count"] == direct_by_m[m]["first_return_class_count"],
            "same_grouped_return_class_count": saved_by_m[m]["grouped_return_class_count"] == direct_by_m[m]["grouped_return_class_count"],
            "same_phi_values": saved_by_m[m]["phi_values"] == direct_by_m[m]["phi_values"],
        }
        rows.append(row)
    return {"rows": rows}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract the reduced skew-odometer normal form for the D5 mixed witness.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    parser.add_argument(
        "--extended-m-list",
        default="15,17,19",
        help="comma-separated larger odd moduli for direct replay stability checks",
    )
    args = parser.parse_args(argv)

    start = __import__("time").perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    extended_m_values = [int(piece) for piece in args.extended_m_list.split(",") if piece.strip()]
    saved_tables = analyse_saved_mixed_tables(INSPECTED_M_VALUES, out_dir=out_dir)
    direct_replay = analyse_direct_mixed_replay(tuple(list(INSPECTED_M_VALUES) + extended_m_values), out_dir=out_dir)
    controls = analyse_controls_from_017(INSPECTED_M_VALUES, out_dir=out_dir)
    comparison = compare_saved_vs_direct(saved_tables, {"reports": [row for row in direct_replay["reports"] if row["m"] in INSPECTED_M_VALUES]})

    witness_registry = [spec.__dict__ for spec in load_witness_specs()]
    witness_registry_path = out_dir / "witness_registry.json"
    _write_json(witness_registry_path, {"witnesses": witness_registry})
    comparison_path = out_dir / "saved_vs_direct_comparison.json"
    _write_json(comparison_path, comparison)

    summary = {
        "task_id": TASK_ID,
        "runtime_sec": runtime_since(start),
        "environment": environment_block(),
        "inspected_m_values": list(INSPECTED_M_VALUES),
        "extended_m_values": list(extended_m_values),
        "exact_reduced_coordinates": {
            "first_return": "(q,s) with s=w+u mod m",
            "grouped_return": "s=w+u mod m",
        },
        "exact_formulas": {
            "R_red": "R_red(q,s)=(q+1, s+1+1_{q=m-2})",
            "dv": "dv(q,s)=1 iff ((q!=m-2 and s=1) or (q=m-2 and s!=0))",
            "low_layer_word": "(1,4,2*1_{q=m-2},3*dv)",
            "U_red": "U_red(s)=s+1",
            "phi": "phi(s)=2+1_{s=1}-2*1_{s=2}-1_{s=3} (mod m)",
            "phi_after_local_gauge": "2-2*1_{s=2} (mod m)",
            "phi_pure_one_defect": "-2*1_{s=2} (mod m)",
        },
        "saved_table_analysis": saved_tables,
        "direct_replay_analysis": direct_replay,
        "saved_vs_direct_comparison": comparison,
        "control_comparison_file": str(out_dir / "control_comparison.json"),
        "witness_registry_file": str(witness_registry_path),
        "strongest_supported_conclusion": (
            "For mixed_008, the reduced first return is exactly a finite-state carry system on (q,s), "
            "the reduced grouped return is exactly the one-dimensional odometer s->s+1, and the grouped "
            "cocycle is exactly phi(s)=2+1_{s=1}-2*1_{s=2}-1_{s=3}, cohomologous to the one-defect "
            "cocycle -2*1_{s=2}, on inspected moduli 5,7,9,11,13 and direct replay stability checks 15,17,19."
        ),
        "remaining_gap": (
            "The current artifact is exact computational extraction and direct witness replay, not yet a symbolic theorem "
            "derived from the mixed_008 witness definition in manuscript form."
        ),
    }
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2))
    print(f"task_id: {TASK_ID}")
    print(f"runtime_sec: {summary['runtime_sec']:.3f}")
    print("inspected m:", ",".join(str(m) for m in summary["inspected_m_values"]))
    print("extended m:", ",".join(str(m) for m in summary["extended_m_values"]))
    print("reduced first-return and grouped cocycle formulas verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
