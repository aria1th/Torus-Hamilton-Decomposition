#!/usr/bin/env python3
"""Validate saved d=5 fresh cyclic q-clock / v-fiber candidates."""

from __future__ import annotations

import argparse
import json
import platform
import time
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from torus_nd_d5_fresh_cyclic_qclock_family import (
    TASK_ID,
    analyze_candidate_for_modulus,
    candidate_name,
    compose_first_return,
    deserialize_candidate,
    full_first_return_check,
    section_return,
)

try:
    from rich.console import Console
    from rich.progress import track
except ImportError:  # pragma: no cover - optional dependency
    Console = None
    track = None


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _iter_progress(values: Iterable, *, description: str, use_rich: bool, total: int | None = None):
    if use_rich and track is not None:
        return track(values, description=description, total=total)
    return values


def _rich_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def _extract_candidate_payloads(payload) -> List[Dict[str, object]]:
    if isinstance(payload, list):
        out = []
        for item in payload:
            if isinstance(item, dict) and "candidate" in item:
                out.append(item["candidate"])
            else:
                out.append(item)
        return out
    if isinstance(payload, dict) and "selected_candidate" in payload:
        selected = payload["selected_candidate"]
        if selected is None:
            return []
        return [selected["candidate"]]
    if isinstance(payload, dict) and "candidate" in payload:
        return [payload["candidate"]]
    if isinstance(payload, dict) and "layers" in payload:
        return [payload]
    raise ValueError("Unsupported candidate JSON format")


def _u_cycle_traces(spec, m: int, limit: int) -> Dict[str, object]:
    u_next, u_dv = section_return(*compose_first_return(spec, m), m)
    visited = set()
    traces = []
    for start in range(len(u_next)):
        if start in visited:
            continue
        orbit = []
        cur = start
        seen_local = {}
        while cur not in seen_local:
            seen_local[cur] = len(orbit)
            visited.add(cur)
            w, u = divmod(cur, m)
            orbit.append({"wu": [w, u], "fiber_shift": u_dv[cur], "next": list(divmod(u_next[cur], m))})
            cur = u_next[cur]
        traces.append({"start": list(divmod(start, m)), "orbit_prefix": orbit[:limit], "cycle_entry_index": seen_local[cur]})
        if len(traces) >= limit:
            break
    return {"m": m, "traces": traces}


def validate_candidates(
    candidate_payloads: Sequence[Dict[str, object]],
    *,
    m_values: Sequence[int],
    full_check_m_values: Sequence[int],
    full_check_colors: Sequence[int],
    limit: int | None,
    trace_limit: int,
    use_rich: bool,
) -> Dict[str, object]:
    start = time.perf_counter()
    if limit is not None:
        candidate_payloads = list(candidate_payloads)[:limit]
    candidates = [deserialize_candidate(payload) for payload in candidate_payloads]
    results = []
    iterable = zip(candidate_payloads, candidates)
    iterable = _iter_progress(iterable, description="Validate candidates", use_rich=use_rich, total=len(candidates))
    for candidate_payload, spec in iterable:
        per_m = [analyze_candidate_for_modulus(spec, m) for m in m_values]
        full_checks = []
        for m in full_check_m_values:
            full_checks.append({"m": m, **full_first_return_check(spec, m, colors=full_check_colors)})
        traces = [_u_cycle_traces(spec, m, trace_limit) for m in m_values[: min(3, len(m_values))]]
        results.append(
            {
                "candidate_name": candidate_name(spec),
                "candidate": candidate_payload,
                "per_m": per_m,
                "full_checks": full_checks,
                "u_cycle_traces": traces,
            }
        )
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": {
            "python_version": platform.python_version(),
            "rich_version": _rich_version(),
        },
        "m_values": list(m_values),
        "full_check_m_values": list(full_check_m_values),
        "full_check_colors": list(full_check_colors),
        "results": results,
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        f"validated_candidates: {len(summary['results'])}",
    ]
    for item in summary["results"][:5]:
        best = item["per_m"][0]
        lines.append(
            f"{item['candidate_name']} | m={best['m']} U_cycles={best['U_cycle_lengths']} "
            f"monodromies={best['monodromies']} indegree={best['R_indegree_histogram']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate saved fresh cyclic q-clock / v-fiber candidates.")
    parser.add_argument("--candidates-json", type=Path, required=True, help="candidate JSON or search summary JSON")
    parser.add_argument("--m-list", default="5,7,9,11,13", help="comma-separated moduli to validate")
    parser.add_argument("--full-check-m-list", default="5,7,9,11,13", help="moduli for full reduced-vs-full checks")
    parser.add_argument("--full-check-colors", default="0", help="comma-separated colors for full checks")
    parser.add_argument("--limit", type=int, help="only validate the first N candidates from the input JSON")
    parser.add_argument("--trace-limit", type=int, default=5, help="number of U-orbit traces to keep per modulus")
    parser.add_argument("--out", type=Path, help="write validation JSON to this path")
    parser.add_argument("--trace-dir", type=Path, help="write per-candidate trace files to this directory")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich progress")
    args = parser.parse_args(argv)

    use_rich = not args.no_rich and Console is not None and track is not None
    payload = json.loads(args.candidates_json.read_text())
    candidate_payloads = _extract_candidate_payloads(payload)
    summary = validate_candidates(
        candidate_payloads,
        m_values=_parse_m_list(args.m_list),
        full_check_m_values=_parse_m_list(args.full_check_m_list),
        full_check_colors=_parse_m_list(args.full_check_colors),
        limit=args.limit,
        trace_limit=args.trace_limit,
        use_rich=use_rich,
    )

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2))
    if args.trace_dir is not None:
        args.trace_dir.mkdir(parents=True, exist_ok=True)
        for index, item in enumerate(summary["results"]):
            path = args.trace_dir / f"candidate_{index:02d}_u_traces.json"
            path.write_text(json.dumps(item["u_cycle_traces"], indent=2))

    _print_summary(summary, use_rich=use_rich)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
