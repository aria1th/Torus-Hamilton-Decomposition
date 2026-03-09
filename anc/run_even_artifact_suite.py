#!/usr/bin/env python3
"""Convenience runner for the even-case artifact suite.

Default behaviour:
  * m=4 finite-witness check;
  * low-layer table / partition checks on all even m in [6, 60];
  * first-return checks on all even m in [6, 120];
  * route_e_even theorem certificates on all even m in [6, 500];
  * proof-backed large-m certificates on a short large-number list;
  * route_e_even p0-check on all even m in [6, 60];
  * route_e_even full-check on all even m in [6, 30].
"""

from __future__ import annotations

import argparse
from typing import Sequence

import route_e_even as ree
import routee_large_m_certificate as large_cert
import routee_first_return_check as first_return_check
import routee_return_formula_tables_check as tables_check
import verify_m4_witness as m4_check


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the even-case artifact suite.")
    parser.add_argument("--tables-max", type=int, default=60, help="upper bound for low-layer table checks")
    parser.add_argument("--first-return-max", type=int, default=120, help="upper bound for first-return checks")
    parser.add_argument("--theorem-max", type=int, default=500, help="upper bound for theorem certificates")
    parser.add_argument(
        "--large-m-list",
        default="1000,1000000,1000000000",
        help="comma-separated large even m values for the O(1) proof-backed certificates",
    )
    parser.add_argument("--p0-max", type=int, default=60, help="upper bound for exact P0 checks")
    parser.add_argument("--full-max", type=int, default=30, help="upper bound for exact full V checks")
    args = parser.parse_args(argv)

    print("[1/7] m=4 finite witness ...")
    m4_check.main()

    print("[2/7] Low-layer table / partition checks ...")
    tables_check.main(["--m-min", "6", "--m-max", str(args.tables_max)])

    print("[3/7] First-return checks ...")
    first_return_check.main(["--m-min", "6", "--m-max", str(args.first_return_max)])

    print("[4/7] Theorem certificates from closed-form first-return maps ...")
    for m in range(6, args.theorem_max + 1, 2):
        ree.theorem_certificate(m)
    print(f"route_e_even theorem mode: PASS for even m = 6..{args.theorem_max} (step 2)")

    print("[5/7] Proof-backed large-m certificates ...")
    large_cert.main(["--m-list", args.large_m_list])

    print("[6/7] Exact P0 checks (Route E definition -> return maps -> cycle structure) ...")
    for m in range(6, args.p0_max + 1, 2):
        ree.validate_return_maps_against_definition(m)
        ree.validate_return_map_cycle_structure(m)
    print(f"route_e_even p0-check logic: PASS for even m = 6..{args.p0_max} (step 2)")

    print("[7/7] Exact full checks on V ...")
    for m in range(6, args.full_max + 1, 2):
        ree.validate_full_color_cycles(m)
    print(f"route_e_even full-check logic: PASS for even m = 6..{args.full_max} (step 2)")

    print("All attachment-bundle artifact checks: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
