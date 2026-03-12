# TorusD5 Theorem Targets

This note records the intended theorem boundary for the future Lean connection
from the full `mixed_008` witness to the extracted `017` return-map model.

The current preparation branch already proves the abstract model layer:

- `formal/TorusD5/Basic.lean`
- `formal/TorusD5/FullCoordinates.lean`
- `formal/TorusD5/FirstReturn.lean`
- `formal/TorusD5/GroupedReturn.lean`
- `formal/TorusD5/Cocycle.lean`
- `formal/TorusD5/Specs.lean`

The future witness proof should ideally land on the spec predicates in
`Specs.lean`, rather than reproving all model lemmas again downstream.

## Intended proof landing points

For the future full-witness development, the clean targets are:

1. Section parameterization:
   - define the exact D5 section and its coordinates
   - prove the future witness return map is well-defined on that section
   - connect the witness-side section coordinates to the bundle-backed slice
     embedding `(-q-w-v-u, q, w, v, u)` already recorded in
     `FullCoordinates.lean`

2. First-return target:
   - prove the induced witness first return satisfies
     `HasCarryFirstReturn`
   - then derive equality with `firstReturnBase` via
     `eq_firstReturnBase_of_hasCarryFirstReturn`

3. Grouped-return target:
   - prove the grouped witness return satisfies
     `HasGroupedReturnBase`
   - then derive equality with `groupedReturnBase` via
     `eq_groupedReturnBase_of_hasGroupedReturnBase`

4. Skew-product target:
   - once the cocycle is fixed, prove the grouped witness map satisfies
     `ProjectsToGroupedSkew`
   - then derive equality with `groupedSkew phi` via
     `eq_groupedSkew_of_projectsToGroupedSkew`

## Why this boundary is useful

This keeps the witness-side proof focused on:

- section definitions,
- return-map calculation,
- coordinate correctness,
- cocycle identification.

It avoids duplicating:

- grouped-base iterate lemmas,
- skew-product iterate formulas,
- extensional map-equality arguments.

## Current caution

The safe preparation branch intentionally stops before any theorem about the
closed form of the D5 cocycle.

So the witness-side proof should not yet aim at:

- a one-defect cocycle normal form,
- cocycle cohomology normalization,
- uniform `u`-independence,
- or a final full Hamiltonicity theorem.

Those should wait for the mathematical review of the `017` bundle and the
subsequent cocycle branch.
