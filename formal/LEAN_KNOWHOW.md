# Lean Know-How Notes

Working notes for the `d=4` Lean formalization.

## CLI-first workflow

Use the Lean toolchain entirely from the terminal:

```bash
cd formal
source "$HOME/.elan/env"
lake build
```

Check one file without rebuilding everything:

```bash
cd formal
source "$HOME/.elan/env"
lake env lean TorusD4/Basic.lean
lake env lean TorusD4/ReturnMaps.lean
```

If a later file imports an earlier one and complains that the `.olean` file is
missing, build the earlier module explicitly:

```bash
lake build TorusD4.Basic
```

## Setup notes

- `elan` + `lake` + mathlib are enough; editor integration is optional.
- `lake init ... math` creates a project with mathlib wired in.
- `lake exe cache get` is worth doing immediately; otherwise first builds are
  much slower.
- Keep the Lean project in `formal/` instead of mixing it into the main repo
  root.

## Import discipline

- Do not import all of `Mathlib` unless necessary.
- Narrow imports make the CLI iteration loop much faster.
- Current `Basic.lean` only needs:
  - `Mathlib.Data.ZMod.Basic`
  - `Mathlib.Data.Fin.Tuple.Basic`
  - `Mathlib.Data.Fin.VecNotation`
  - `Mathlib.Tactic.FinCases`
  - `Mathlib.Tactic.Ring`

## Definitions that worked well

- Model the torus as `Fin 4 -> ZMod m`.
- Model direction tuples as `Equiv.Perm (Fin 4)`.
- For explicit small permutations on `Fin 4`, writing the `Equiv` directly is
  better than trying to prove bijectivity with `native_decide` inside the main
  file. It elaborates more predictably.
- Use explicit typed numerals in `ZMod m` equalities:
  - `(1 : ZMod m)`
  - `(2 : ZMod m)`
  - `(-1 : ZMod m)`

## `delta` / indicator trick

The useful pattern is:

```lean
def delta (m : ℕ) (p : Prop) [Decidable p] : ZMod m := if p then 1 else 0
```

Put the proposition argument before the typeclass argument. If the order is
 wrong, Lean gets stuck trying to synthesize `Decidable`.

## Common `ZMod` pitfalls

- Statements that look obvious for general `m` can fail at `m = 1`, since in
  `ZMod 1` every element is equal.
- If a lemma really uses nontrivial modulus arithmetic, add an assumption like
  `[Fact (1 < m)]`.
- When moving from manuscript notation to Lean, watch for places where the paper
  silently assumes `m >= 3`.

## Proof patterns that were useful

- For explicit formulas on pairs/triples, `rcases x with ⟨a, b⟩` or
  `⟨a, b, q⟩` is cleaner than heavy rewriting.
- For equality of tuples, `ext` works well.
- For affine identities, `simp` first, then `ring` if needed.
- When formalizing a "single cycle" statement, make the definition include the
  return equality `f^[N] x = x`, not just injectivity/surjectivity of the first
  `N` iterates. The weaker version is not enough for later lifting lemmas.
- For carry-bit equalities like
  `if b = 1 then 1 else 0 = if 1 = b then 1 else 0`,
  direct `by_cases` on the equality is usually simpler than trying to force a
  one-line `simp`.
- If `simp` leaves a goal like `-b + 1 = 0 -> 1 = 0`, it usually means one
  direction of an iff needs its own `[simp]` lemma, e.g.
  `neg_add_one_eq_zero_iff`.

## Build/debug habits

- Start by compiling single files before running full `lake build`.
- If elaboration seems to hang, suspect one of:
  - an overly broad import,
  - a bad `native_decide`,
  - a typeclass argument that Lean cannot infer.
- `lake build Module.Name` is the fastest reliable way to check imported module
  boundaries.

## Current module split

- `TorusD4/Basic.lean`
  torus model, witness permutations, witness rule, `phi`
- `TorusD4/ReturnMaps.lean`
  explicit `R_c`, `T_c`, odometer, affine conjugacy
- `TorusD4/ReturnDynamics.lean`
  generic color-indexed `R`/`T` wrappers, `q`-drift under `R_c`, iterated
  `q`-drift, and the fact that `m` iterates from the `q = -1` slice land back on
  that slice
- `TorusD4/SecondReturn.lean`
  verified `R^m = T` bridge: explicit generic affine maps `G0`-`G3`, their
  iterate formulas, the first-step slice formulas, the middle-segment iterate
  lemmas for the `q = -2` and `q = 1` regimes, and the final
  `secondReturnOfRMap_eq_TMap`
- `TorusD4/ReturnLifts.lean`
  explicit equivalence `P0Coord ≃ QCoord × ZMod m`, the `m`-block lift from
  `RMap` to `TMap`, and the normal form for slice-started iterates
  `m * t + r`
- `TorusD4/P0Cycles.lean`
  verified `Q -> P_0` lift: exact `m^3` cycle theorem for `RMap` from the
  exact `m^2` cycle theorem for `TMap`
- `TorusD4/Cycles.lean`
  exact-cycle notion, odometer cycle proof, conjugacy transfer to `T_c`
- `TorusD4/Lifts.lean`
  generic helper lemmas for periodicity, iterate injectivity on a cycle,
  equality of iterates modulo the cycle length, and product-slice return maps
- `TorusD4/FullCoordinates.lean`
  full-torus coordinate split `Point m ≃ P0Coord m × ZMod m`, the
  `phiLayer/coordOfPoint` equivalence, and the basic `S (colorMap x) = S x + 1`
  layer-shift lemmas
- `TorusD4/FirstReturn.lean`
  verified full-coordinate scaffolding for the first-return step: the
  canonical full-space dynamics `KMap`, explicit iterate formulas, `layer 0`,
  `layer 1`, and `layer 2 with q ≠ 0` split-coordinate lemmas, plus the
  canonical-tail theorem from layer `3`, the color-by-color first-return
  theorems `firstReturn_eq_R0` through `firstReturn_eq_R3`, and the packaged
  theorem `firstReturn_eq_RMap`
- `TorusD4/FullCycles.lean`
  verified `P_0 -> V` lift: conjugates `colorMap` to a full-coordinate map
  `pairColorMap`, proves the `m`-step return on the `S = 0` slice is `RMap`,
  lifts the exact `m^3` cycle for `RMap` to an exact `m^4` cycle for
  `pairColorMap`, and transfers that cycle back to `colorMap`

`D4LineUnionDraft.lean` currently typechecks as a `sorry`-based skeleton. It is
useful as a theorem inventory, but the verified source of truth is the
`TorusD4/*` module tree.

## Practical note from the last lift

- The bridge between `phiLayer u 0` and `slicePoint 0 u` is not definitional in
  the places where it matters for semiconjugacy proofs. Use
  `coordOfPoint_phiLayer` / `splitPointEquiv` explicitly instead of expecting
  `rfl` or a bare `simp` to close those goals.

## Next formalization steps

1. Package a short final theorem for the manuscript-level statement:
   for every color `c`, `colorMap c` has a single `m^4` cycle for `m ≥ 3`.
2. Decide whether to clean up linter-heavy files (`FirstReturn.lean` and
   `FullCycles.lean`) now or defer that until after a review pass.
3. If the `d=4` result is accepted as stable, extract the reusable slice/return
   pattern into a more abstract lemma before touching `d=3`.
