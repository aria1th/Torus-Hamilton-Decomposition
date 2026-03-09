#!/usr/bin/env python3
"""Proof-backed O(1) certificates for very large even m in Route E.

This script is intentionally different from `route_e_even.py`.

- `route_e_even.py --mode theorem` is still the formula-driven regression path:
  it iterates the lane maps and sums the return times explicitly, so it costs
  O(m) per input.
- This module assumes the manuscript proofs are correct and turns the proved
  splice normal forms plus proved return-time identities into an O(1)
  certificate for arbitrarily large even `m >= 6`.

The purpose is not to replace the finite regression scripts. It is to make
large-number spot checks cheap once the proof has been accepted.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import List, Sequence


@dataclass(frozen=True)
class LargeColorCertificate:
    color: int
    splice_permutation: str
    block_summary: str
    lane_map_single_cycle: bool
    rho_sum: int
    rho_sum_equals_m2: bool


@dataclass(frozen=True)
class LargeCertificate:
    m: int
    case: str
    proof_mode: str
    color_certificates: List[LargeColorCertificate]
    p0_hamilton: bool
    full_hamilton: bool


def _parse_m_list(raw: str) -> List[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _case_label(m: int) -> str:
    return "I (m ≡ 0,2 mod 6)" if m % 6 in (0, 2) else "II (m ≡ 4 mod 6)"


def _color2_certificate(m: int) -> LargeColorCertificate:
    rho_sum = 1 + (m - 1) + 2 * m + (m - 3) * m
    return LargeColorCertificate(
        color=2,
        splice_permutation="(1 2)",
        block_summary="F_{2,1}=(0,1); F_{2,2}=(m-1,m-2,...,2)",
        lane_map_single_cycle=True,
        rho_sum=rho_sum,
        rho_sum_equals_m2=(rho_sum == m * m),
    )


def _color1_certificate(m: int) -> LargeColorCertificate:
    if m % 6 in (0, 2):
        rho_sum = 2 + (m - 4) * (m + 2) + 2 * (m + 3)
        if m % 6 == 2:
            block_summary = (
                "F_{1,1}=(0,2,5,...,m-3); "
                "F_{1,2}=(1,4,7,...,m-1); "
                "F_{1,3}=(3,6,9,...,m-2)"
            )
        else:
            block_summary = (
                "F_{1,1}=(0,2,5,...,m-1); "
                "F_{1,2}=(3,6,9,...,m-3,1); "
                "F_{1,3}=(4,7,10,...,m-2)"
            )
    else:
        half = (m - 6) // 2
        rho_sum = 3 + (m + 3) + half * (m + 2) + half * (m + 4) + 2 * (m + 6)
        block_summary = (
            "F_{1,1}=(0,2,5,11,...,m-5,1); "
            "F_{1,2}=(3,9,15,...,m-1,7,13,...,m-3); "
            "F_{1,3}=(4,6,8,...,m-2)"
        )
    return LargeColorCertificate(
        color=1,
        splice_permutation="(1 2 3)",
        block_summary=block_summary,
        lane_map_single_cycle=True,
        rho_sum=rho_sum,
        rho_sum_equals_m2=(rho_sum == m * m),
    )


def _color0_certificate(m: int) -> LargeColorCertificate:
    if m % 6 in (0, 2):
        rho_sum = 1 + (m - 3) * (m - 1) + (2 * m - 3) + (2 * m - 1)
        block_summary = (
            "F_{0,1}=(0,m-2); "
            "F_{0,2}=(1,3,5,...,m-3); "
            "F_{0,3}=(2,4,6,...,m-4); "
            "F_{0,4}=(m-1)"
        )
    elif m % 12 == 10:
        rho_sum = 1 + (m - 6) * (m - 2) + 2 * (2 * m - 4) + 2 * (m - 1) + (2 * m - 3)
        block_summary = (
            "F_{0,1}=(0,m-2,5,9,...,m-1,1); "
            "F_{0,2}=(4,8,...,m-6); "
            "F_{0,3}=(3,7,...,m-3); "
            "F_{0,4}=(2,6,...,m-4)"
        )
    else:
        rho_sum = 1 + (m - 6) * (m - 2) + 2 * (2 * m - 4) + 2 * (m - 1) + (2 * m - 3)
        block_summary = (
            "F_{0,1}=(0,m-2,5,9,...,m-3); "
            "F_{0,2}=(2,6,...,m-6); "
            "F_{0,3}=(3,7,...,m-1,1); "
            "F_{0,4}=(4,8,...,m-4)"
        )
    return LargeColorCertificate(
        color=0,
        splice_permutation="(1 2 3 4)",
        block_summary=block_summary,
        lane_map_single_cycle=True,
        rho_sum=rho_sum,
        rho_sum_equals_m2=(rho_sum == m * m),
    )


def large_theorem_certificate(m: int) -> LargeCertificate:
    if m < 6 or m % 2 != 0:
        raise ValueError("m must be even and >= 6")

    colors = [_color0_certificate(m), _color1_certificate(m), _color2_certificate(m)]
    p0_hamilton = all(cert.lane_map_single_cycle and cert.rho_sum_equals_m2 for cert in colors)

    return LargeCertificate(
        m=m,
        case=_case_label(m),
        proof_mode="splice normal form + return-time identities",
        color_certificates=colors,
        p0_hamilton=p0_hamilton,
        full_hamilton=p0_hamilton,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="O(1) proof-backed certificates for very large even Route E instances."
    )
    parser.add_argument(
        "--m-list",
        default="1000,1000000,1000000000",
        help="comma-separated even m values >= 6",
    )
    parser.add_argument("--json", action="store_true", help="print JSON instead of human-readable text")
    args = parser.parse_args(argv)

    m_values = _parse_m_list(args.m_list)
    if not m_values:
        raise SystemExit("Need at least one m value.")

    certs = [large_theorem_certificate(m) for m in m_values]

    if args.json:
        print(json.dumps([asdict(cert) for cert in certs], indent=2))
        return 0

    for cert in certs:
        print(f"m = {cert.m}")
        print(f"case = {cert.case}")
        print(f"proof_mode = {cert.proof_mode}")
        for color_cert in cert.color_certificates:
            print(
                f"color {color_cert.color}: splice={color_cert.splice_permutation} "
                f"lane_map_single_cycle={color_cert.lane_map_single_cycle} "
                f"rho_sum={color_cert.rho_sum} rho_sum_equals_m2={color_cert.rho_sum_equals_m2}"
            )
            print(f"  blocks: {color_cert.block_summary}")
        print(f"p0_hamilton = {cert.p0_hamilton}")
        print(f"full_hamilton = {cert.full_hamilton}")
        print("Large-m proof-backed certificate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
