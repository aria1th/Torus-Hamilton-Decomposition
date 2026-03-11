# Lean Review Request: `d = 4`

## Scope

Please review the Lean 4 formalization in `formal/TorusD4/*` for the `d = 4`
line-union proof.

The intended verified chain is:

1. explicit witness and color maps on the torus,
2. explicit first-return maps `R_c` on `P_0`,
3. second-return maps `T_c` on `Q`,
4. conjugacy of `T_c` to an odometer,
5. lift from `Q` to `P_0`,
6. lift from `P_0` to the full torus.

## Main theorem targets

- `formal/TorusD4/FullCycles.lean`
  - `hasCycle_colorMap`
  - `all_colors_haveCycle`
- `formal/TorusD4/FirstReturn.lean`
  - `firstReturn_eq_RMap`
- `formal/TorusD4/P0Cycles.lean`
  - `hasCycle_RMap_cube`
- `formal/TorusD4/SecondReturn.lean`
  - `secondReturnOfRMap_eq_TMap`

## Build

```bash
cd formal
source "$HOME/.elan/env"
lake build
```

## Review focus

- correctness of the return-map reductions,
- correctness of the cycle-lifting arguments,
- any hidden assumptions around `ZMod m`, especially for the `m >= 3` regime,
- theorem packaging and whether the current statement boundaries are clean.

Cleanup is intentionally deferred. There are linter warnings in
`FirstReturn.lean` and `FullCycles.lean`, but the project builds successfully.
