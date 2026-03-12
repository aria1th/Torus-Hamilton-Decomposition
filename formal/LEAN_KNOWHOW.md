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

## D3 odd status

- `TorusD3Odd/*` now covers the full odd-case chain, not just the return maps.
  `Cycles.lean` proves the three affine conjugacies and the exact `m^2` cycles
  for `F0`, `F1`, and `F2`.
- `FullCycles.lean` adds the full-coordinate model for `d=3` odd:
  `KMap`, `pairColorMap`, the explicit two-step formulas on the low layers,
  the canonical-tail lemma from layer `S = 2`, the first-return theorem
  `((colorMap c)^[m]) (phiLayer u 0) = phiLayer (FMap c u) 0`, and the final
  lift to exact `m^3` cycles on the full torus.
- The practical proof pattern for `d=3` odd is simpler than `d=4`:
  do the low-layer work explicitly for the first two steps, then switch to a
  uniform canonical map `KMap` for the remaining `m - 2` steps.
- One recurring Lean issue in this file was that the final theorem
  `point_eq_phiLayer_of_splitPointEquiv_eq` wants the coordinate value
  `(u, s)` directly. Do not convert that back into
  `splitPointEquiv (phiLayer u s)` unless you really need the conjugacy form;
  ending the calc chain at `slicePoint s u` is usually the cleaner target.

## D3 even color-2 status

- `TorusD3Even/Counting.lean` now contains a reusable first-return counting
  theorem on finite types. The useful proof pattern is:
  define recursive block times, prove the block-time iterate theorem, prove a
  minimal-return contradiction by locating any putative early return inside one
  block interval, then package the final cycle with `cycleOn_of_period_card`.
- `TorusD3Even/Color2.lean` now has the verified one-dimensional lane map
  `T2`, its conjugacy `psiT2` to `x ↦ x + 1`, the exact `m`-cycle theorem for
  `T2`, the closed-form two-dimensional map `R2xy`, the return-time function
  `rho2`, and the easy `x = 0` first-return lemma.
- Important boundary lesson: the closed-form `R2xy` branch proofs must be
  stated under the real even-theorem regime `m ≥ 6` (or at least with explicit
  lower bounds strong enough to keep `-1`, `-2`, `2`, `3`, ... distinct in
  `ZMod m`). Several naive “obvious” step lemmas become false or change branch
  behavior at small moduli like `m = 3` or `m = 4`.
- Practical consequence: do not prove the `x = 1` / `x = 2` boundary traces by
  ad hoc `simp` under a weak assumption like `2 < m`. First set the correct
  lower-bound hypotheses, then build a small helper layer for nat-cast
  nonvanishing (`3 ≠ 0`, `4 ≠ 0`, casted `m - 1`, casted `m - 2`, etc.) and
  only after that prove the long generic `G`-segment lemmas.
