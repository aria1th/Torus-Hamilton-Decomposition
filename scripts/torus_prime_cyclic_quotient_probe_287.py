#!/usr/bin/env python3
"""Probe naive cyclic-quotient ideas against closed D3 and frontier D5 data.

This script is meant to test one specific methodological question:

    if one starts from the full torus and quotients by cyclic coordinate
    rotation, does the fixed-color dynamics descend to a clean quotient map?

The current D3 and D5 work strongly suggests the answer is "no" at the full
map level. The simple structure only appears after the existing return-ladder
compression.

Outputs:
- RoundY/checks/d5_287_prime_cyclic_quotient_probe_summary.json
- RoundY/checks/d5_287_prime_cyclic_quotient_probe/per_case.json
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import sys
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = REPO_ROOT / "RoundY" / "checks" / "d5_287_prime_cyclic_quotient_probe_summary.json"
DEFAULT_DETAIL_DIR = REPO_ROOT / "RoundY" / "checks" / "d5_287_prime_cyclic_quotient_probe"

sys.path.insert(0, str(REPO_ROOT / "scripts"))

from torus_nd_d5_selector_star_common_119 import build_R_data, selector_perm_star
from torus_nd_d5_selstar_color3_actual_identification_264 import analyse_modulus as analyse_d5_actual_identification
from torus_nd_d5_selstar_color3_row_model_260 import (
    analyse_actual_modulus as analyse_d5_row_actual,
    analyse_model_modulus as analyse_d5_row_model,
)
from torus_nd_d5_selstar_color3_section_model_261 import analyse_modulus as analyse_d5_section_model


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load module {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ROUTE_E_PATH = (
    REPO_ROOT
    / "arxiv_uploads"
    / "2026-03-25_cases"
    / "d3_review_candidates"
    / "v8_d3_only"
    / "anc"
    / "route_e_even.py"
)
route_e_even = load_module("route_e_even_probe_287", ROUTE_E_PATH)


def cyclic_shift(x: tuple[int, ...], shift: int = 1) -> tuple[int, ...]:
    n = len(x)
    shift %= n
    return x[shift:] + x[:shift]


def orbit_rep_cyclic(x: tuple[int, ...]) -> tuple[int, ...]:
    return min(cyclic_shift(x, shift) for shift in range(len(x)))


def free_orbit_representatives(dim: int, m: int) -> dict[tuple[int, ...], set[tuple[int, ...]]]:
    reps: dict[tuple[int, ...], set[tuple[int, ...]]] = {}
    for x in itertools.product(range(m), repeat=dim):
        orbit = {cyclic_shift(x, shift) for shift in range(dim)}
        if len(orbit) != dim:
            continue
        reps.setdefault(orbit_rep_cyclic(x), orbit)
    return reps


def family_covariance_probe(
    *,
    dim: int,
    m: int,
    num_colors: int,
    apply_color_map,
) -> list[dict[str, object]]:
    states = list(itertools.product(range(m), repeat=dim))
    payload: list[dict[str, object]] = []
    for color_shift in range(num_colors):
        witness = None
        for color in range(num_colors):
            for x in states:
                lhs = cyclic_shift(apply_color_map(m, color, x), 1)
                rhs = apply_color_map(m, (color + color_shift) % num_colors, cyclic_shift(x, 1))
                if lhs != rhs:
                    witness = {
                        "color_shift": color_shift,
                        "color": color,
                        "state": list(x),
                        "shifted_image": list(lhs),
                        "shift_then_color_image": list(rhs),
                    }
                    break
            if witness is not None:
                break
        payload.append(
            {
                "color_shift": color_shift,
                "covariance_holds": witness is None,
                "first_witness": witness,
            }
        )
    return payload


def quotient_determinism_probe(
    *,
    dim: int,
    m: int,
    num_colors: int,
    apply_color_map,
) -> dict[str, object]:
    orbit_reps = free_orbit_representatives(dim, m)
    per_color: dict[str, object] = {}
    for color in range(num_colors):
        deterministic = 0
        nondeterministic = 0
        first_witness = None
        for rep, orbit in orbit_reps.items():
            image_reps = {orbit_rep_cyclic(apply_color_map(m, color, x)) for x in orbit}
            if len(image_reps) == 1:
                deterministic += 1
            else:
                nondeterministic += 1
                if first_witness is None:
                    first_witness = {
                        "orbit_representative": list(rep),
                        "image_orbit_representatives": [list(y) for y in sorted(image_reps)],
                    }
        per_color[str(color)] = {
            "deterministic_free_orbits": deterministic,
            "nondeterministic_free_orbits": nondeterministic,
            "first_witness": first_witness,
        }
    return per_color


def d3_apply_color_map(m: int, color: int, x: tuple[int, int, int]) -> tuple[int, int, int]:
    return route_e_even.color_map_from_definition(m, color, x)


def d5_apply_full_color_map(
    m: int,
    color: int,
    x: tuple[int, int, int, int, int],
) -> tuple[int, int, int, int, int]:
    perm = selector_perm_star(m, x)
    direction = perm[color]
    y = list(x)
    y[direction] = (y[direction] + 1) % m
    return tuple(y)


def d5_make_p0_state(x4: tuple[int, int, int, int], m: int) -> tuple[int, int, int, int, int]:
    return x4 + ((-sum(x4)) % m,)


def d5_color3_p0_return_probe(m: int) -> dict[str, object]:
    points, _perm, images4 = build_R_data(m, 3, selector_perm_star)
    xs = [d5_make_p0_state(point[:4], m) for point in points]
    ys = [d5_make_p0_state(tuple(int(v) for v in images4[idx]), m) for idx in range(len(points))]

    orbit_bundles: dict[tuple[int, ...], list[tuple[tuple[int, ...], tuple[int, ...]]]] = {}
    for x, y in zip(xs, ys):
        orbit = {cyclic_shift(x, shift) for shift in range(5)}
        if len(orbit) != 5:
            continue
        orbit_bundles.setdefault(orbit_rep_cyclic(x), []).append((x, y))

    deterministic = 0
    nondeterministic = 0
    first_witness = None
    for rep, pairs in orbit_bundles.items():
        image_reps = {orbit_rep_cyclic(y) for _x, y in pairs}
        if len(image_reps) == 1:
            deterministic += 1
        else:
            nondeterministic += 1
            if first_witness is None:
                first_witness = {
                    "orbit_representative": list(rep),
                    "image_orbit_representatives": [list(y) for y in sorted(image_reps)],
                }

    return {
        "deterministic_free_orbits": deterministic,
        "nondeterministic_free_orbits": nondeterministic,
        "first_witness": first_witness,
    }


def analyse_d3_modulus(m: int) -> dict[str, object]:
    certificate = route_e_even.theorem_certificate(m)
    return {
        "m": m,
        "full_family_covariance": family_covariance_probe(
            dim=3,
            m=m,
            num_colors=3,
            apply_color_map=d3_apply_color_map,
        ),
        "full_free_orbit_quotient": quotient_determinism_probe(
            dim=3,
            m=m,
            num_colors=3,
            apply_color_map=d3_apply_color_map,
        ),
        "P0_return_cycle_lengths": {
            str(color): route_e_even.cycle_lengths_on_p0(m, color) for color in range(3)
        },
        "transversal_first_return_cycle_lengths": {
            "0": [len(certificate.T0_cycle_order)],
            "1": [len(certificate.T1_cycle_order)],
            "2": [len(certificate.T2_cycle_order)],
        },
        "transversal_return_time_sums": {
            "0": certificate.rho0_sum,
            "1": certificate.rho1_sum,
            "2": certificate.rho2_sum,
        },
    }


def analyse_d5_modulus(m: int) -> dict[str, object]:
    payload: dict[str, object] = {
        "m": m,
        "full_family_covariance": family_covariance_probe(
            dim=5,
            m=m,
            num_colors=5,
            apply_color_map=d5_apply_full_color_map,
        ),
        "full_free_orbit_quotient": quotient_determinism_probe(
            dim=5,
            m=m,
            num_colors=5,
            apply_color_map=d5_apply_full_color_map,
        ),
        "color3_P0_return_free_orbit_quotient": d5_color3_p0_return_probe(m),
        "color3_actual_identification": analyse_d5_actual_identification(m),
    }
    if m >= 9:
        payload["color3_section_model"] = analyse_d5_section_model(m)
        payload["color3_row_actual"] = analyse_d5_row_actual(m)
        payload["color3_row_model"] = analyse_d5_row_model(m)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe naive cyclic-quotient ideas on D3 and D5.")
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=DEFAULT_SUMMARY,
        help=f"summary JSON path (default: {DEFAULT_SUMMARY})",
    )
    parser.add_argument(
        "--detail-dir",
        type=Path,
        default=DEFAULT_DETAIL_DIR,
        help=f"detail output directory (default: {DEFAULT_DETAIL_DIR})",
    )
    parser.add_argument(
        "--d3-moduli",
        type=int,
        nargs="*",
        default=[6, 8, 10],
        help="even D3 moduli to probe",
    )
    parser.add_argument(
        "--d5-moduli",
        type=int,
        nargs="*",
        default=[5, 7, 9, 11],
        help="odd D5 moduli to probe",
    )
    args = parser.parse_args()

    d3 = {str(m): analyse_d3_modulus(m) for m in args.d3_moduli}
    d5 = {str(m): analyse_d5_modulus(m) for m in args.d5_moduli}

    summary = {
        "task": "d5_287_prime_cyclic_quotient_probe",
        "question": (
            "Can one start from the full torus, quotient by cyclic coordinate rotation, "
            "and expect the fixed-color dynamics to descend cleanly in the already closed "
            "D3 and current D5 branches?"
        ),
        "d3_moduli": args.d3_moduli,
        "d5_moduli": args.d5_moduli,
        "all_d3_full_covariance_shifts_fail": all(
            not item["covariance_holds"]
            for payload in d3.values()
            for item in payload["full_family_covariance"]
        ),
        "all_d3_full_free_orbit_quotients_have_nondeterministic_colors": all(
            any(color_payload["nondeterministic_free_orbits"] > 0 for color_payload in payload["full_free_orbit_quotient"].values())
            for payload in d3.values()
        ),
        "all_d3_P0_returns_are_single_cycles": all(
            payload["P0_return_cycle_lengths"] == {str(c): [int(m) ** 2] for c in range(3)}
            for m, payload in d3.items()
        ),
        "all_d3_transversal_first_returns_are_m_cycles": all(
            payload["transversal_first_return_cycle_lengths"] == {str(c): [int(m)] for c in range(3)}
            for m, payload in d3.items()
        ),
        "all_d5_full_covariance_shifts_fail": all(
            not item["covariance_holds"]
            for payload in d5.values()
            for item in payload["full_family_covariance"]
        ),
        "all_d5_full_free_orbit_quotients_have_nondeterministic_colors": all(
            all(color_payload["nondeterministic_free_orbits"] > 0 for color_payload in payload["full_free_orbit_quotient"].values())
            for payload in d5.values()
        ),
        "all_d5_color3_P0_free_orbit_quotients_fail": all(
            payload["color3_P0_return_free_orbit_quotient"]["nondeterministic_free_orbits"] > 0
            for payload in d5.values()
        ),
        "all_d5_color3_actual_identifications_verified": all(
            payload["color3_actual_identification"]["R_formula_verified"]
            and payload["color3_actual_identification"]["section_formula_verified"]
            for payload in d5.values()
        ),
        "all_checked_large_d5_section_models_single_cycle": all(
            ("color3_section_model" not in payload)
            or payload["color3_section_model"]["section_model_is_single_cycle"]
            for payload in d5.values()
        ),
        "all_checked_large_d5_row_models_single_cycle": all(
            ("color3_row_model" not in payload)
            or payload["color3_row_model"]["row_model_is_single_cycle"]
            for payload in d5.values()
        ),
        "conclusion": (
            "The naive full-torus cyclic quotient is not the right primary theorem object: "
            "it already fails in the closed D3 Route-E package and in the current D5 Sel* "
            "package. The useful cyclic/clock structure appears only after the existing "
            "return-ladder compression, on the proved transversal/section/row models."
        ),
        "revised_direction": (
            "For prime-p generalization, treat cyclic-quotient or voltage language as a "
            "late-stage description of an already extracted reduced return model. Do not "
            "start from a full-torus quotient-first program; keep the backbone-first, "
            "return-ladder, resonance-split, defect-localization strategy."
        ),
    }

    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.detail_dir.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.detail_dir / "per_case.json").write_text(
        json.dumps({"d3": d3, "d5": d5}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
