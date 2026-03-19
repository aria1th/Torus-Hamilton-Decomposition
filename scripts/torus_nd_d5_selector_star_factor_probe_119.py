#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from pathlib import Path

from torus_nd_d5_selector_star_common_119 import build_R_data, selector_perm_star

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO_ROOT / "RoundY" / "checks" / "d5_119_selector_star_factor_probe_summary.json"


def pair_sums(x: tuple[int, int, int, int, int], m: int) -> tuple[int, int, int, int, int]:
    return tuple((x[(i - 1) % 5] + x[(i + 2) % 5]) % m for i in range(5))


def z_tuple(x: tuple[int, int, int, int, int]) -> tuple[int, ...]:
    return tuple(i for i, v in enumerate(x) if v == 0)


def o_tuple(x: tuple[int, int, int, int, int]) -> tuple[int, ...]:
    return tuple(i for i, v in enumerate(x) if v == 1)


def m_tuple(x: tuple[int, int, int, int, int], m: int) -> tuple[int, ...]:
    return tuple(i for i, v in enumerate(x) if v == m - 1)


def b_tuple(x: tuple[int, int, int, int, int], m: int, k: int) -> tuple[int, ...]:
    p = pair_sums(x, m)
    return tuple(i for i, v in enumerate(p) if v == k)


def rotations(x: tuple[int, ...]) -> list[tuple[int, ...]]:
    n = len(x)
    return [tuple(x[(i - shift) % n] for i in range(n)) for shift in range(n)]


def dihedral_orbit(x: tuple[int, ...]) -> list[tuple[int, ...]]:
    rots = rotations(x)
    rev = tuple(reversed(x))
    return rots + rotations(rev)


def bit_value(name: str, x: tuple[int, int, int, int, int], m: int) -> int:
    idx = int(name[1])
    tag = name[0]
    value = x[idx]
    if tag == "Z":
        return int(value == 0)
    if tag == "O":
        return int(value == 1)
    if tag == "M":
        return int(value == m - 1)
    raise ValueError(name)


def make_p0_state(x4: tuple[int, int, int, int], m: int) -> tuple[int, int, int, int, int]:
    return x4 + ((-sum(x4)) % m,)


def evaluate_field(x_states, y_states, field_builder):
    transitions: defaultdict[object, set[object]] = defaultdict(set)
    states = set()
    for x, y in zip(x_states, y_states):
        fx = field_builder(x)
        fy = field_builder(y)
        states.add(fx)
        transitions[fx].add(fy)
    nondet = sum(1 for vals in transitions.values() if len(vals) > 1)
    max_mult = max((len(vals) for vals in transitions.values()), default=0)
    return {
        "state_count": len(states),
        "nondet_states": nondet,
        "max_multiplicity": max_mult,
        "exact": nondet == 0,
    }


def build_dataset(m: int, color: int):
    pts, _perm, images4 = build_R_data(m, color, selector_perm_star)
    x_states = [make_p0_state(x[:4], m) for x in pts]
    y_states = [make_p0_state(tuple(int(v) for v in images4[idx]), m) for idx in range(len(pts))]
    return x_states, y_states


def candidate_builders(m: int):
    builders: dict[str, object] = {}

    for subset in itertools.combinations(range(4), 3):
        name = "coords:" + "".join(str(i) for i in subset)
        builders[name] = lambda x, subset=subset: tuple(x[i] for i in subset)

    for subset in itertools.combinations(range(5), 3):
        label = "".join(str(i) for i in subset)
        builders["pairs3:" + label] = lambda x, subset=subset: tuple(pair_sums(x, m)[i] for i in subset)
        for bit in [f"{tag}{i}" for tag in "ZOM" for i in range(5)]:
            name = f"pairs3+bit:{label}+{bit}"
            builders[name] = lambda x, subset=subset, bit=bit: (
                tuple(pair_sums(x, m)[i] for i in subset),
                bit_value(bit, x, m),
            )

    for subset in itertools.combinations(range(5), 4):
        label = "".join(str(i) for i in subset)
        builders["pairs4:" + label] = lambda x, subset=subset: tuple(pair_sums(x, m)[i] for i in subset)

    builders["disp4"] = None  # filled later from transition data
    builders["ZM"] = lambda x: (z_tuple(x), m_tuple(x, m))
    builders["B23ZM"] = lambda x: (b_tuple(x, m, 2), b_tuple(x, m, 3), z_tuple(x), m_tuple(x, m))
    builders["B234ZOM"] = lambda x: (
        b_tuple(x, m, 2),
        b_tuple(x, m, 3),
        b_tuple(x, m, 4),
        z_tuple(x),
        o_tuple(x),
        m_tuple(x, m),
    )
    builders["pairs_full"] = lambda x: pair_sums(x, m)
    builders["pairs_cyclic"] = lambda x: min(rotations(pair_sums(x, m)))
    builders["pairs_dihedral"] = lambda x: min(dihedral_orbit(pair_sums(x, m)))
    builders["x5_cyclic"] = lambda x: min(rotations(x))
    builders["x5_dihedral"] = lambda x: min(dihedral_orbit(x))
    return builders


def summarize_color(color: int, moduli: list[int]):
    per_field: dict[str, dict[str, object]] = {}
    for m in moduli:
        x_states, y_states = build_dataset(m, color)
        builders = candidate_builders(m)
        disp_cache = {
            x: tuple((y[i] - x[i]) % m for i in range(4))
            for x, y in zip(x_states, y_states)
        }
        builders["disp4"] = lambda x, disp_cache=disp_cache: disp_cache[x]
        for name, builder in builders.items():
            stats = evaluate_field(x_states, y_states, builder)
            per_field.setdefault(name, {})[str(m)] = stats

    exact_candidates = []
    ranked = []
    for name, per_m in per_field.items():
        total_nondet = sum(payload["nondet_states"] for payload in per_m.values())
        total_states = sum(payload["state_count"] for payload in per_m.values())
        max_mult = max(payload["max_multiplicity"] for payload in per_m.values())
        record = {
            "field": name,
            "per_modulus": per_m,
            "total_nondet": total_nondet,
            "total_states": total_states,
            "max_multiplicity": max_mult,
        }
        if all(payload["exact"] for payload in per_m.values()):
            exact_candidates.append(record)
        ranked.append(record)

    exact_candidates.sort(key=lambda item: (item["total_states"], item["field"]))
    ranked.sort(key=lambda item: (item["total_nondet"], item["total_states"], item["field"]))
    return {
        "exact_candidates": exact_candidates,
        "best_candidates": ranked[:25],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe low-complexity factors for the D5 119 selector-star first return.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT, help=f"JSON output path (default: {DEFAULT_OUT})")
    args = parser.parse_args()

    moduli = [9, 11, 13]
    summary = {
        "scope": {
            "selector": "Sel* from scripts/torus_nd_d5_selector_star_common_119.py",
            "colors": [3, 4],
            "moduli": moduli,
            "object": "first return R_c^* on P0",
            "families": [
                "3-coordinate projections on P0",
                "3 chosen pair sums",
                "3 chosen pair sums plus one Z/O/M bit",
                "4 chosen pair sums",
                "disp4, ZM, B23ZM, B234ZOM, full pair sums",
                "cyclic and dihedral orbit quotients of x5 / pair sums",
            ],
        },
        "results": {
            "3": summarize_color(3, moduli),
            "4": summarize_color(4, moduli),
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2))
    print(args.output)


if __name__ == "__main__":
    main()
