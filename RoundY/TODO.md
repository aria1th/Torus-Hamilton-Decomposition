# RoundY TODO

This file tracks the post-closure D5 odd-`m` follow-up work in one place.

## Priority 1

- Demonstrate that the theorem-guided search/screen method remains effective
  beyond `d=5` on a small but meaningful pilot range, starting with
  `d = 7, 9, ...` and only at sufficiently manageable sizes.
- Treat this as a method-validation task, not as a full theorem search.
- Preferred output:
  a compact report showing which finite-family / state-machine screening tests
  still run in practical time and which invariants remain informative.

## Priority 2

- Repackage the current D5 odd-`m` solution as a reusable screening template:
  clean frame, strict clock, exact bridge, and small local implementation
  checks.
- Record which parts are D5-specific and which parts look reusable for higher
  odd dimensions.

## Priority 3

- Only after the pilot `d = 7, 9, ...` validation, decide whether to launch a
  broader odd-prime search or a Lean-facing abstraction pass.
- Do not reopen broad brute-force witness search before the pilot
  theorem-guided method is validated.
- After the odd-dimension pilot, evaluate the `d=5`, even-`m` critical-row
  program on small moduli `m = 6, 8, 10, 12`: bulk odometer, regular
  source-window splice, and exceptional interface.
