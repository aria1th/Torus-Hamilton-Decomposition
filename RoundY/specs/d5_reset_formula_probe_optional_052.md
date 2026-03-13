# Optional narrow compute request after 052

This is optional proof support, not a new branch.

## Goal
Test whether the tested reset maps
\[
R_{\mathrm{cj}}(s,v,\lambda),
\qquad
R_{\mathrm{oth}}(s,u,\lambda)
\]
admit a simple symbolic description on larger odd moduli.

## Why this matters
The theorem-side proof no longer needs more witness families. The only missing
symbolic ingredient that could noticeably strengthen the manuscript is an
explicit formula, or a sharply constrained piecewise formula, for the boundary
reset values.

## What to test
On the active best-seed boundary `tau=0`, through as many odd moduli as are
cheap:
- build the full exact tables for
  - `carry_jump -> next_tau` keyed by `(s,v,layer)`
  - `other -> next_tau` keyed by `(s,u,layer)`
- test candidate affine / piecewise-affine laws over `Z_m`
- separately test whether the image fibers for the known value sets
  - `{0,1,m-2}` on `carry_jump`
  - `{0,m-4,m-3}` on `other`
  are each cut out by one or two simple congruence conditions.

## Useful outputs
- `reset_formula_candidates.json`
- `reset_formula_failures.json`
- `reset_value_partition_tables.json`
- one short README saying whether there is:
  - a uniform simple formula,
  - only a piecewise formula,
  - or no short symbolic law in the tested candidate family.

## Non-goals
- do not reopen carry coding
- do not search for rho again
- do not widen to generic transducers
