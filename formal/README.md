# Torus Lean Formalization

This directory is a standalone Lean 4 + mathlib project.

Its current verified core is the `d=4` Hamilton decomposition proof.

For the current `d=5` frontier and the recommended Lean role after artifact
`D5-RETURN-MAP-MODEL-017`, see:

- `README-D5.md`

## Current scope

The current formalization covers:

- the torus point model `Fin 4 -> ZMod m`,
- the explicit line-union witness as a permutation-valued rule,
- the `P_0` parameterization `phi`,
- the explicit return-map formulas `R0`-`R3` and `T0`-`T3`,
- the odometer model,
- the affine conjugacy lemmas `psi0_conj`-`psi3_conj`.

The next proof targets are:

- the odometer single-cycle theorem,
- the lift from `Q` to `P_0`,
- the lift from `P_0` to the full torus,
- linking the explicit witness to the closed-form `R_c` formulas.

## CLI workflow

Build everything:

```bash
cd formal
source "$HOME/.elan/env"
lake build
```

Check a single file:

```bash
cd formal
source "$HOME/.elan/env"
lake env lean TorusD4/Basic.lean
lake env lean TorusD4/ReturnMaps.lean
```

## File layout

- `TorusD4/Basic.lean`
  core types, witness, bump maps, and `phi`
- `TorusD4/ReturnMaps.lean`
  explicit `R`/`T` formulas, odometer, and conjugacy lemmas
- `TorusD4.lean`
  umbrella import for the library
