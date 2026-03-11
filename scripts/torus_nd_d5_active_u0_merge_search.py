#!/usr/bin/env python3
"""Exhaustive search over a small active (b1,b2)-driven layer-2/3 grammar family."""

from __future__ import annotations

import argparse
import json
import platform
import time
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

TASK_ID = "D5-ACTIVE-U0-MERGE-003"
DIM = 5
B1_LOOKUP = {
    5: frozenset((1, 2)),
    7: frozenset((1, 3, 5)),
    9: frozenset((1, 2, 5, 6)),
}
B2_LOOKUP = {
    5: frozenset((1, 3)),
    7: frozenset((1, 2, 4)),
    9: frozenset((1, 3, 5, 7)),
}

try:
    from rich.console import Console
except ImportError:  # pragma: no cover - optional dependency
    Console = None


@dataclass(frozen=True)
class Rule:
    layer2_bits: Tuple[int, int, int, int]
    layer3_bits: Tuple[int, int, int, int]

    def payload(self) -> Dict[str, object]:
        return {
            "layer2_bits": list(self.layer2_bits),
            "layer3_bits": list(self.layer3_bits),
            "layer2_table": {str(idx): (1 if bit else 2) for idx, bit in enumerate(self.layer2_bits)},
            "layer3_table": {str(idx): (1 if bit else 3) for idx, bit in enumerate(self.layer3_bits)},
        }


def _rich_version() -> str | None:
    try:
        return version("rich")
    except PackageNotFoundError:
        return None


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _encode(coords: Sequence[int], m: int) -> int:
    out = 0
    for value in coords:
        out = out * m + value
    return out


def _decode(idx: int, m: int) -> Tuple[int, ...]:
    coords = [0] * DIM
    for pos in range(DIM - 1, -1, -1):
        idx, coords[pos] = divmod(idx, m)
    return tuple(coords)


def _layer_bucket(layer: int) -> object:
    return "4+" if layer >= 4 else layer


def _ctx_index(delta: int, m: int) -> int:
    b1 = int(delta in B1_LOOKUP[m])
    b2 = int(delta in B2_LOOKUP[m])
    return b1 * 2 + b2


def _iter_rules() -> List[Rule]:
    rules = []
    for mask2 in range(16):
        layer2 = tuple((mask2 >> idx) & 1 for idx in range(4))
        for mask3 in range(16):
            layer3 = tuple((mask3 >> idx) & 1 for idx in range(4))
            rules.append(Rule(layer2_bits=layer2, layer3_bits=layer3))
    return rules


def _precompute_m(m: int) -> Dict[str, object]:
    n = m**DIM
    coords = [_decode(idx, m) for idx in range(n)]
    step = [[0] * DIM for _ in range(n)]
    contexts: List[List[Tuple[object, int | None, bool]]] = [[None] * DIM for _ in range(n)]  # type: ignore[assignment]
    for idx, vertex in enumerate(coords):
        total = sum(vertex) % m
        layer = _layer_bucket(total)
        for direction in range(DIM):
            nxt = list(vertex)
            nxt[direction] = (nxt[direction] + 1) % m
            step[idx][direction] = _encode(nxt, m)
        for color in range(DIM):
            q = vertex[(color + 1) % DIM]
            v = vertex[(color + 3) % DIM]
            delta = (v - q) % m
            phase_align = delta == 0
            ctx = None if phase_align else _ctx_index(delta, m)
            contexts[idx][color] = (layer, ctx, phase_align)
    return {"m": m, "n": n, "coords": coords, "step": step, "contexts": contexts}


def _direction(pre: Dict[str, object], idx: int, color: int, rule: Rule) -> int:
    layer, ctx, phase_align = pre["contexts"][idx][color]
    if layer == 0:
        anchor = 1
    elif layer == 1:
        anchor = 4
    elif layer == 2:
        anchor = 2 if phase_align else (1 if rule.layer2_bits[ctx] else 2)
    elif layer == 3:
        anchor = 3 if phase_align else (1 if rule.layer3_bits[ctx] else 3)
    else:
        anchor = 0
    return (anchor + color) % DIM


def _nexts_for_rule(pre: Dict[str, object], rule: Rule) -> List[List[int]]:
    n = pre["n"]
    nexts = [[0] * n for _ in range(DIM)]
    for idx in range(n):
        for color in range(DIM):
            direction = _direction(pre, idx, color, rule)
            nexts[color][idx] = pre["step"][idx][direction]
    return nexts


def _incoming_latin(nexts: List[List[int]]) -> bool:
    n = len(nexts[0])
    for color in range(DIM):
        indegree = [0] * n
        for nxt in nexts[color]:
            indegree[nxt] += 1
        if any(value != 1 for value in indegree):
            return False
    return True


def _first_return(pre: Dict[str, object], nexts0: List[int]) -> Dict[str, object]:
    m = pre["m"]
    coords = pre["coords"]

    groups = {}
    for q in range(m):
        for w in range(m):
            for u in range(m):
                images = []
                for v in range(m):
                    idx = _encode(((-q - w - v - u) % m, q, w, v, u), m)
                    cur = idx
                    for _ in range(m):
                        cur = nexts0[cur]
                    c = coords[cur]
                    q2, w2, v2, u2 = c[1], c[2], c[3], c[4]
                    images.append(((q2, w2, u2), (v2 - v) % m))
                groups[(q, w, u)] = images

    clean_frame = True
    r_next = {}
    r_dv = {}
    for key, images in groups.items():
        image_set = {item[0] for item in images}
        dv_set = {item[1] for item in images}
        if len(image_set) != 1 or len(dv_set) != 1:
            clean_frame = False
            break
        r_next[key] = next(iter(image_set))
        r_dv[key] = next(iter(dv_set))

    strict_clock = clean_frame and all(((image[0] - key[0]) % m) == 1 for key, image in r_next.items())
    if not clean_frame:
        return {
            "clean_frame": False,
            "strict_clock": False,
            "U_cycle_count": 0,
            "U_cycle_lengths": [],
            "monodromies": [],
            "nontrivial_u": False,
        }

    u_map = {}
    u_dv = {}
    for w in range(m):
        for u in range(m):
            cur = (0, w, u)
            total = 0
            for _ in range(m):
                total = (total + r_dv[cur]) % m
                cur = r_next[cur]
            u_map[(w, u)] = (cur[1], cur[2])
            u_dv[(w, u)] = total

    idx_map = {(w, u): w * m + u for w in range(m) for u in range(m)}
    nexts = [idx_map[u_map[(w, u)]] for w in range(m) for u in range(m)]
    visited = [0] * len(nexts)
    cycles = []
    for start in range(len(nexts)):
        if visited[start]:
            continue
        seen = {}
        path = []
        cur = start
        while not visited[cur] and cur not in seen:
            seen[cur] = len(path)
            path.append(cur)
            cur = nexts[cur]
        if not visited[cur] and cur in seen:
            cycles.append(path[seen[cur] :])
        for node in path:
            visited[node] = 1

    monodromies = []
    for cycle in cycles:
        total = 0
        for idx in cycle:
            w, u = divmod(idx, m)
            total = (total + u_dv[(w, u)]) % m
        monodromies.append(total)

    cycle_lengths = sorted(len(cycle) for cycle in cycles)
    nontrivial_u = len(cycles) < m * m or any(length > 1 for length in cycle_lengths) or any(value != 0 for value in monodromies)
    return {
        "clean_frame": True,
        "strict_clock": strict_clock,
        "U_cycle_count": len(cycles),
        "U_cycle_lengths": cycle_lengths,
        "monodromies": monodromies,
        "nontrivial_u": nontrivial_u,
    }


def _evaluate_rule(pre_by_m: Dict[int, Dict[str, object]], rule: Rule, *, m_values: Sequence[int]) -> Dict[str, object]:
    per_m = {}
    latin_all = True
    clean_all = True
    strict_all = True
    total_u_cycles = 0
    total_nonzero_monodromies = 0
    any_nontrivial_u = False
    for m in m_values:
        pre = pre_by_m[m]
        nexts = _nexts_for_rule(pre, rule)
        latin = _incoming_latin(nexts)
        ret = _first_return(pre, nexts[0]) if latin else {
            "clean_frame": False,
            "strict_clock": False,
            "U_cycle_count": 0,
            "U_cycle_lengths": [],
            "monodromies": [],
            "nontrivial_u": False,
        }
        per_m[str(m)] = {"latin": latin, "color0_return": ret}
        latin_all &= latin
        clean_all &= ret["clean_frame"]
        strict_all &= ret["strict_clock"]
        total_u_cycles += ret["U_cycle_count"]
        total_nonzero_monodromies += sum(1 for value in ret["monodromies"] if value != 0)
        any_nontrivial_u |= ret["nontrivial_u"]
    return {
        "rule": rule.payload(),
        "per_m": per_m,
        "latin_all": latin_all,
        "clean_all": clean_all,
        "strict_all": strict_all,
        "total_u_cycle_count": total_u_cycles,
        "total_nonzero_monodromies": total_nonzero_monodromies,
        "any_nontrivial_u": any_nontrivial_u,
    }


def run_search(*, m_values: Sequence[int]) -> Dict[str, object]:
    start = time.perf_counter()
    pre_by_m = {m: _precompute_m(m) for m in m_values}
    all_rules = _iter_rules()
    evaluated = []
    survivors = []
    for rule in all_rules:
        result = _evaluate_rule(pre_by_m, rule, m_values=m_values)
        evaluated.append(result)
        if result["latin_all"] and result["clean_all"]:
            survivors.append(result)

    strict_survivors = [item for item in survivors if item["strict_all"]]
    strict_survivors.sort(
        key=lambda item: (
            not item["any_nontrivial_u"],
            item["total_u_cycle_count"],
            -item["total_nonzero_monodromies"],
            item["rule"]["layer2_bits"],
            item["rule"]["layer3_bits"],
        )
    )
    survivors.sort(
        key=lambda item: (
            not item["any_nontrivial_u"],
            not item["strict_all"],
            item["total_u_cycle_count"],
            -item["total_nonzero_monodromies"],
            item["rule"]["layer2_bits"],
            item["rule"]["layer3_bits"],
        )
    )
    return {
        "task_id": TASK_ID,
        "runtime_sec": time.perf_counter() - start,
        "environment": {"python_version": platform.python_version(), "rich_version": _rich_version()},
        "m_values": list(m_values),
        "family_description": {
            "layer0_anchor": 1,
            "layer1_anchor": 4,
            "layer2_phase_align1_anchor": 2,
            "layer3_phase_align1_anchor": 3,
            "layer4plus_anchor": 0,
            "layer2_nonzero_choices": [2, 1],
            "layer3_nonzero_choices": [3, 1],
            "context_index": "2*b1 + b2",
            "rule_count": len(all_rules),
        },
        "survivor_counts": {
            "total_rules": len(all_rules),
            "latin_and_clean": len(survivors),
            "latin_clean_and_strict": len(strict_survivors),
            "strict_with_nontrivial_u": sum(1 for item in strict_survivors if item["any_nontrivial_u"]),
        },
        "best_clean_rules": survivors[:10],
        "best_strict_rules": strict_survivors[:10],
    }


def _print_summary(summary: Dict[str, object], *, use_rich: bool) -> None:
    lines = [
        f"task_id: {summary['task_id']}",
        f"runtime_sec: {summary['runtime_sec']:.3f}",
        f"rules={summary['survivor_counts']['total_rules']} clean={summary['survivor_counts']['latin_and_clean']} strict={summary['survivor_counts']['latin_clean_and_strict']} strict_nontrivial_u={summary['survivor_counts']['strict_with_nontrivial_u']}",
    ]
    for item in summary["best_strict_rules"][:5]:
        lines.append(
            f"strict rule l2={item['rule']['layer2_bits']} l3={item['rule']['layer3_bits']} "
            f"U={item['total_u_cycle_count']} nontrivial={item['any_nontrivial_u']}"
        )
    if use_rich and Console is not None:
        console = Console()
        for line in lines:
            console.print(line)
    else:
        for line in lines:
            print(line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search a small active two-bit layer-2/3 grammar family for U0 merging.")
    parser.add_argument("--m-list", default="5,7,9", help="comma-separated pilot moduli")
    parser.add_argument("--out", type=Path, required=True, help="write JSON summary here")
    parser.add_argument("--no-rich", action="store_true", help="disable Rich output")
    args = parser.parse_args(argv)

    summary = run_search(m_values=_parse_m_list(args.m_list))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2))
    _print_summary(summary, use_rich=not args.no_rich and Console is not None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
