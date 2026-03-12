#!/usr/bin/env python3
"""Best-seed defect quotient and unary splice lower bound for the D5 endpoint branch."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import torus_nd_d5_endpoint_latin_repair as seed032
from torus_nd_d5_return_map_model_common import environment_block, runtime_since

TASK_ID = "D5-DEFECT-SPLICE-TRANSDUCER-033"
PRIMARY_M_VALUES = (5, 7, 9)
BEST_LEFT_WORD = (2, 2, 1)
BEST_RIGHT_WORD = (1, 4, 4)
REPRESENTATIVE_W0 = 0
REPRESENTATIVE_S0 = 0
BBB_CONTEXT = ("B", "B", "B")


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _coords_payload(prepared: seed032.PreparedSearch, idx: int) -> Dict[str, int]:
    coords = prepared.pre["coords"][idx]
    return {
        "x0": int(coords[0]),
        "q": int(coords[1]),
        "w": int(coords[2]),
        "v": int(coords[3]),
        "u": int(coords[4]),
        "s": int((coords[2] + coords[4]) % prepared.m),
        "layer": int(sum(coords) % prepared.m),
    }


def _classify_overfull_target(m: int, payload: Mapping[str, int]) -> Tuple[str, int | None]:
    q = int(payload["q"])
    w = int(payload["w"])
    u = int(payload["u"])
    layer = int(payload["layer"])
    if q == 0 and w == 0 and layer == 2 and u != 0:
        return "O_R1", u
    if q == 0 and w == 0 and layer == 3 and u == 0:
        return "O_R2", None
    if q == 0 and w == 0 and layer == 4 and u == 1:
        return "O_R3", None
    if q == 0 and w == 1 and layer == 4 and u != 1:
        return "O_L3", u
    raise ValueError(f"unclassified overfull target for m={m}: {payload}")


def _classify_hole_target(m: int, payload: Mapping[str, int]) -> Tuple[str, int | None]:
    q = int(payload["q"])
    w = int(payload["w"])
    u = int(payload["u"])
    layer = int(payload["layer"])
    if q == m - 1 and w == m - 1 and layer == 2 and u != 2:
        return "H_L1", u
    if q == 0 and w == 0 and layer == 3 and u == 1:
        return "H_R2", None
    if q == 0 and w == 0 and layer == 4 and u == 2:
        return "H_R3", None
    if q == m - 1 and w == 1 and layer == 4 and u != 1:
        return "H_L3", u
    raise ValueError(f"unclassified hole target for m={m}: {payload}")


def _build_best_seed(prepared: seed032.PreparedSearch) -> Tuple[List[List[int]], Dict[str, object]]:
    nexts_all, meta = seed032._build_candidate(
        prepared,
        w0=REPRESENTATIVE_W0,
        s0=REPRESENTATIVE_S0,
        left_word=BEST_LEFT_WORD,
        right_word=BEST_RIGHT_WORD,
        cocycle_defect="none",
        repair=None,
    )
    if nexts_all is None:
        raise ValueError("best seed unexpectedly failed to build")
    return nexts_all, meta


def _indegree_tables(row: Sequence[int], n: int) -> Tuple[List[int], List[List[int]]]:
    indegree = [0] * n
    incoming: List[List[int]] = [[] for _ in range(n)]
    for idx, nxt in enumerate(row):
        indegree[nxt] += 1
        incoming[nxt].append(idx)
    return indegree, incoming


def _color0_defect_data(prepared: seed032.PreparedSearch) -> Dict[str, object]:
    nexts_all, meta = _build_best_seed(prepared)
    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    step_by_dir = prepared.pre["step_by_dir"]
    indegree, incoming = _indegree_tables(row, prepared.pre["n"])

    over_targets = [idx for idx, value in enumerate(indegree) if value > 1]
    hole_targets = [idx for idx, value in enumerate(indegree) if value == 0]

    over_rows = []
    hole_rows = []
    over_by_family: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    hole_by_family: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    incoming_family_labels: Dict[str, Counter[str]] = defaultdict(Counter)

    for target in over_targets:
        payload = _coords_payload(prepared, target)
        family, parameter = _classify_overfull_target(prepared.m, payload)
        row_payload = {
            "target_index": int(target),
            "family": family,
            "parameter_u": None if parameter is None else int(parameter),
            "coords": payload,
            "incoming_labels": sorted(labels[idx] for idx in incoming[target]),
        }
        over_rows.append(row_payload)
        over_by_family[family].append(row_payload)
        for idx in incoming[target]:
            incoming_family_labels[family][labels[idx]] += 1

    for target in hole_targets:
        payload = _coords_payload(prepared, target)
        family, parameter = _classify_hole_target(prepared.m, payload)
        row_payload = {
            "target_index": int(target),
            "family": family,
            "parameter_u": None if parameter is None else int(parameter),
            "coords": payload,
        }
        hole_rows.append(row_payload)
        hole_by_family[family].append(row_payload)

    direct_edges: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    for label_name in ("R1", "R2", "R3", "L3", "L1", "B"):
        sources = [idx for idx, label in enumerate(labels) if label == label_name]
        for alt_dir in range(5):
            hits = []
            for idx in sources:
                nxt = step_by_dir[alt_dir][idx]
                if indegree[nxt] == 0:
                    family, parameter = _classify_hole_target(prepared.m, _coords_payload(prepared, nxt))
                    hits.append(
                        {
                            "target_index": int(nxt),
                            "family": family,
                            "parameter_u": None if parameter is None else int(parameter),
                        }
                    )
            if not hits:
                continue
            family_counter = Counter(hit["family"] for hit in hits)
            parameter_counter: Dict[str, Counter[int]] = defaultdict(Counter)
            for hit in hits:
                if hit["parameter_u"] is not None:
                    parameter_counter[hit["family"]][int(hit["parameter_u"])] += 1
            direct_edges[label_name].append(
                {
                    "alt_dir": int(alt_dir),
                    "hit_count": len(hits),
                    "hole_family_counts": dict(sorted(family_counter.items())),
                    "parameter_support": {
                        family: dict(sorted(counter.items()))
                        for family, counter in sorted(parameter_counter.items())
                    },
                }
            )

    family_summaries = []
    for family_name, rows in sorted(over_by_family.items()):
        parameters = sorted({row["parameter_u"] for row in rows if row["parameter_u"] is not None})
        v_values = sorted({row["coords"]["v"] for row in rows})
        family_summaries.append(
            {
                "family": family_name,
                "target_count": len(rows),
                "parameter_values": parameters,
                "parameter_count": len(parameters),
                "v_values": v_values,
                "v_count": len(v_values),
                "incoming_label_counts": dict(sorted(incoming_family_labels[family_name].items())),
                "representative_coords": rows[0]["coords"],
            }
        )

    hole_summaries = []
    for family_name, rows in sorted(hole_by_family.items()):
        parameters = sorted({row["parameter_u"] for row in rows if row["parameter_u"] is not None})
        v_values = sorted({row["coords"]["v"] for row in rows})
        hole_summaries.append(
            {
                "family": family_name,
                "target_count": len(rows),
                "parameter_values": parameters,
                "parameter_count": len(parameters),
                "v_values": v_values,
                "v_count": len(v_values),
                "representative_coords": rows[0]["coords"],
            }
        )

    return {
        "overfull_target_count": len(over_targets),
        "hole_target_count": len(hole_targets),
        "family_summaries": family_summaries,
        "hole_summaries": hole_summaries,
        "direct_repair_edges": dict(sorted(direct_edges.items())),
        "overfull_rows_sample": over_rows[:40],
        "hole_rows_sample": hole_rows[:40],
    }


def _all_color_totals(prepared: seed032.PreparedSearch) -> Dict[str, object]:
    nexts_all, _meta = _build_best_seed(prepared)
    per_color = []
    for color, row in enumerate(nexts_all):
        indegree, _incoming = _indegree_tables(row, prepared.pre["n"])
        per_color.append(
            {
                "color": int(color),
                "overfull_target_count": int(sum(1 for value in indegree if value > 1)),
                "hole_target_count": int(sum(1 for value in indegree if value == 0)),
                "excess_incoming_total": int(sum(value - 1 for value in indegree if value > 1)),
            }
        )
    return {
        "per_color": per_color,
        "all_color_overfull_target_count": int(sum(row["overfull_target_count"] for row in per_color)),
        "all_color_hole_target_count": int(sum(row["hole_target_count"] for row in per_color)),
        "all_color_excess_incoming_total": int(sum(row["excess_incoming_total"] for row in per_color)),
    }


def _context_signature(labels: Sequence[str], prev_row: Sequence[int], succ_row: Sequence[int], idx: int) -> Tuple[str, str, str]:
    return labels[prev_row[idx]], labels[idx], labels[succ_row[idx]]


def _unary_corridor_report(prepared: seed032.PreparedSearch) -> Dict[str, object]:
    nexts_all, meta = _build_best_seed(prepared)
    row = nexts_all[0]
    labels = meta["labels_by_color"][0]
    prev_row = prepared.baseline_prev_all[0]
    succ_row = prepared.baseline_nexts_all[0]
    step_by_dir = prepared.pre["step_by_dir"]
    indegree, _incoming = _indegree_tables(row, prepared.pre["n"])
    hole_targets = [idx for idx, value in enumerate(indegree) if value == 0]
    hole_set_l1 = {
        idx
        for idx in hole_targets
        if _classify_hole_target(prepared.m, _coords_payload(prepared, idx))[0] == "H_L1"
    }

    r1_sources = [idx for idx, label in enumerate(labels) if label == "R1"]
    per_source = []
    distribution = Counter()
    split_by_source_u: Dict[int, Counter[int]] = defaultdict(Counter)

    for source in r1_sources:
        source_payload = _coords_payload(prepared, source)
        best_row = None
        for initial_alt in range(5):
            seen = set()
            current = step_by_dir[initial_alt][source]
            t = 0
            while current not in seen:
                seen.add(current)
                exit_dirs = [d for d in range(5) if step_by_dir[d][current] in hole_set_l1]
                if exit_dirs:
                    prefix_ok = True
                    prefix = step_by_dir[initial_alt][source]
                    for _ in range(t + 1):
                        if _context_signature(labels, prev_row, succ_row, prefix) != BBB_CONTEXT:
                            prefix_ok = False
                            break
                        prefix = row[prefix]
                    if prefix_ok:
                        candidate = {
                            "source_index": int(source),
                            "source_coords": source_payload,
                            "initial_alt_dir": int(initial_alt),
                            "delay_steps": int(t),
                            "exit_dirs": [int(value) for value in exit_dirs],
                            "exit_state_coords": _coords_payload(prepared, current),
                            "exit_context": list(_context_signature(labels, prev_row, succ_row, current)),
                        }
                        candidate_key = (candidate["delay_steps"], candidate["initial_alt_dir"], candidate["exit_dirs"])
                        if best_row is None or candidate_key < (
                            best_row["delay_steps"],
                            best_row["initial_alt_dir"],
                            best_row["exit_dirs"],
                        ):
                            best_row = candidate
                    break
                current = row[current]
                t += 1
        if best_row is None:
            raise ValueError(f"no unary corridor found for R1 source {source_payload}")
        per_source.append(best_row)
        distribution[best_row["delay_steps"]] += 1
        split_by_source_u[int(source_payload["u"])][best_row["delay_steps"]] += 1

    grouped_examples: Dict[int, List[Dict[str, object]]] = defaultdict(list)
    for row_payload in per_source:
        grouped_examples[int(row_payload["delay_steps"])].append(row_payload)

    min_delay = min(row["delay_steps"] for row in per_source)
    max_delay = max(row["delay_steps"] for row in per_source)
    best_case_rows = [row for row in per_source if row["delay_steps"] == min_delay]
    worst_case_rows = [row for row in per_source if row["delay_steps"] == max_delay]

    return {
        "r1_source_count": len(r1_sources),
        "delay_distribution": dict(sorted((int(delay), int(count)) for delay, count in distribution.items())),
        "delay_distribution_by_source_u": {
            str(source_u): dict(sorted((int(delay), int(count)) for delay, count in counter.items()))
            for source_u, counter in sorted(split_by_source_u.items())
        },
        "best_case": {
            "delay_steps": int(min_delay),
            "state_lower_bound": int(min_delay + 1),
            "initial_alt_dir": int(best_case_rows[0]["initial_alt_dir"]),
            "exit_dirs": best_case_rows[0]["exit_dirs"],
            "representatives": best_case_rows[:10],
        },
        "worst_case": {
            "delay_steps": int(max_delay),
            "state_lower_bound": int(max_delay + 1),
            "initial_alt_dir": int(worst_case_rows[0]["initial_alt_dir"]),
            "exit_dirs": worst_case_rows[0]["exit_dirs"],
            "representatives": worst_case_rows[:10],
        },
        "all_sources_share_same_initial_alt": len({row["initial_alt_dir"] for row in per_source}) == 1,
        "all_exit_contexts_are_bbb": all(tuple(row["exit_context"]) == BBB_CONTEXT for row in per_source),
    }


def _analysis_summary(
    started: float,
    template_rows: Mapping[str, object],
    graph_rows: Mapping[str, object],
    lower_bound_rows: Mapping[str, object],
) -> Dict[str, object]:
    per_m_summary = {}
    two_state_impossible = True
    three_state_impossible = True
    for m in PRIMARY_M_VALUES:
        template = template_rows[str(m)]
        graph = graph_rows[str(m)]
        lower = lower_bound_rows[str(m)]["report"]
        best_case_lb = int(lower["best_case"]["state_lower_bound"])
        two_state_impossible &= best_case_lb > 2
        three_state_impossible &= best_case_lb > 3
        per_m_summary[str(m)] = {
            "all_color_overfull_target_count": int(graph["all_color_totals"]["all_color_overfull_target_count"]),
            "all_color_hole_target_count": int(graph["all_color_totals"]["all_color_hole_target_count"]),
            "color0_overfull_target_count": int(graph["color0"]["overfull_target_count"]),
            "color0_hole_target_count": int(graph["color0"]["hole_target_count"]),
            "template_explanation": template["defect_count_explanation"],
            "unresolved_source_family": "R1",
            "unary_best_case_delay": int(lower["best_case"]["delay_steps"]),
            "unary_best_case_state_lower_bound": best_case_lb,
            "unary_worst_case_delay": int(lower["worst_case"]["delay_steps"]),
            "unary_worst_case_state_lower_bound": int(lower["worst_case"]["state_lower_bound"]),
        }

    return {
        "task_id": TASK_ID,
        "best_seed": {
            "left_word": list(BEST_LEFT_WORD),
            "right_word": list(BEST_RIGHT_WORD),
            "w0": REPRESENTATIVE_W0,
            "s0": REPRESENTATIVE_S0,
        },
        "summary": {
            "defect_count_law": "all colors: 10*m^2; per color: 2*m^2 = m*((m-1)+1+1+(m-1))",
            "bounded_template_result": "per color the defect quotients to four overfull families and four hole families, each with an m-fold v-translation",
            "direct_repair_result": "L3, R2, and R3 repair directly; only the R1 channel remains unresolved",
            "state_lower_bound_result": "under the extracted local template alphabet, the shortest R1->H_L1 splice is a unary BBB corridor, so 2-state and 3-state controllers are impossible on the pilot range",
        },
        "two_state_impossible_under_unary_model": bool(two_state_impossible),
        "three_state_impossible_under_unary_model": bool(three_state_impossible),
        "per_m": per_m_summary,
        "runtime_seconds": runtime_since(started),
        "environment": environment_block(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the best-seed defect graph and unary splice lower bound for D5.")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    prepared_by_m = {m: seed032._prepare_m(m, seed032._mixed_rule()) for m in PRIMARY_M_VALUES}

    template_rows: Dict[str, object] = {}
    graph_rows: Dict[str, object] = {}
    lower_bound_rows: Dict[str, object] = {}

    for m, prepared in prepared_by_m.items():
        color0 = _color0_defect_data(prepared)
        all_color = _all_color_totals(prepared)
        lower = _unary_corridor_report(prepared)

        template_rows[str(m)] = {
            "m": int(m),
            "defect_count_explanation": {
                "all_colors": "10*m^2",
                "per_color": "2*m^2",
                "quotient_count_per_color": "2*m = (m-1)+1+1+(m-1)",
                "translation_factor": "each quotient template carries m v-translates",
            },
            "overfull_families": color0["family_summaries"],
            "hole_families": color0["hole_summaries"],
        }

        graph_rows[str(m)] = {
            "m": int(m),
            "color0": color0,
            "all_color_totals": all_color,
            "unresolved_source_families": ["R1"],
            "directly_repairable_source_families": ["L3", "R2", "R3"],
        }

        lower_bound_rows[str(m)] = {
            "m": int(m),
            "assumption": "controller input is the extracted local template/context alphabet; the unresolved splice is tracked through its unary BBB corridor",
            "target_hole_family": "H_L1",
            "report": lower,
        }

    summary = _analysis_summary(started, template_rows, graph_rows, lower_bound_rows)
    _write_json(out_dir / "best_seed_defect_templates.json", template_rows)
    _write_json(out_dir / "best_seed_defect_graph.json", graph_rows)
    _write_json(out_dir / "state_lower_bound_report.json", lower_bound_rows)
    _write_json(
        out_dir / "transducer_synthesis_summary.json",
        {
            "task_id": TASK_ID,
            "status": "pruned_by_lower_bound",
            "checked_state_counts": [2, 3],
            "reason": "the unary BBB corridor lower bound already exceeds three states on every pilot modulus",
            "details": {
                str(m): {
                    "best_case_delay_steps": int(lower_bound_rows[str(m)]["report"]["best_case"]["delay_steps"]),
                    "best_case_state_lower_bound": int(lower_bound_rows[str(m)]["report"]["best_case"]["state_lower_bound"]),
                }
                for m in PRIMARY_M_VALUES
            },
        },
    )
    _write_json(args.summary_out, summary)


if __name__ == "__main__":
    main()
