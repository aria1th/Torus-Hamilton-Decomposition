#!/usr/bin/env python3
"""Convenience runner for the even-case artifact suite.

Default behaviour:
  * m=4 finite-witness check;
  * low-layer table / partition checks on all even m in [6, 60];
  * first-return checks on all even m in [6, 120];
  * route_e_even theorem certificates on all even m in [6, 500];
  * route_e_even p0-check on all even m in [6, 60];
  * route_e_even full-check on all even m in [6, 30].
"""

from __future__ import annotations

import argparse
from typing import List, Sequence

import route_e_even as ree
import routee_first_return_check as first_return_check
import routee_return_formula_tables_check as tables_check
import verify_m4_witness as m4_check


def run_range(func, start: int, stop: int) -> None:
    for m in range(start, stop + 1, 2):
        func(m)



def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the even-case artifact suite.")
    parser.add_argument("--tables-max", type=int, default=60, help="upper bound for low-layer table checks")
    parser.add_argument("--first-return-max", type=int, default=120, help="upper bound for first-return checks")
    parser.add_argument("--theorem-max", type=int, default=500, help="upper bound for theorem certificates")
    parser.add_argument("--p0-max", type=int, default=60, help="upper bound for exact P0 checks")
    parser.add_argument("--full-max", type=int, default=30, help="upper bound for exact full V checks")
    args = parser.parse_args(argv)

    print("[1/6] m=4 finite witness ...")
    m4_check.main()

    print("[2/6] Low-layer table / partition checks ...")
    tables_check.main(["--m-min", "6", "--m-max", str(args.tables_max)])

    print("[3/6] First-return checks ...")
    first_return_check.main(["--m-min", "6", "--m-max", str(args.first_return_max)])

    print("[4/6] Theorem certificates from closed-form first-return maps ...")
    for m in range(6, args.theorem_max + 1, 2):
        ree.theorem_certificate(m)
    print(f"route_e_even theorem mode: PASS for even m = 6..{args.theorem_max} (step 2)")

    print("[5/6] Exact P0 checks (Route E definition -> return maps -> cycle structure) ...")
    for m in range(6, args.p0_max + 1, 2):
        ree.validate_return_maps_against_definition(m)
        ree.validate_return_map_cycle_structure(m)
    print(f"route_e_even p0-check logic: PASS for even m = 6..{args.p0_max} (step 2)")

    print("[6/6] Exact full checks on V ...")
    for m in range(6, args.full_max + 1, 2):
        ree.validate_full_color_cycles(m)
    print(f"route_e_even full-check logic: PASS for even m = 6..{args.full_max} (step 2)")

    print("All attachment-bundle artifact checks: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
