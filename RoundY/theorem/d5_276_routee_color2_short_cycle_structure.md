# D5 276 Route-E Color-2 Short-Cycle Structure

This note continues the `275` residual probe for the combined best exact family
from
[d5_274_routee_assembly_pattern_search.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_274_routee_assembly_pattern_search.md).

Primary files:

- [torus_nd_d5_routee_color2_short_cycle_structure_276.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_routee_color2_short_cycle_structure_276.py)
- [d5_276_routee_color2_short_cycle_structure_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_276_routee_color2_short_cycle_structure_summary.json)
- [per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_276_routee_color2_short_cycle_structure/per_modulus.json)

## 1. Setup

Let `H_2` be the color-`2` map inside the combined best exact `274` family, and
let

- `P0 = {Sigma = 0}`,
- `R_2 = (H_2)^m | P0`.

The previous note `275` showed that `R_2` has a stable five-branch affine
support and is the cleanest residual surgery target.

The present note asks a more concrete question:

> where, exactly, does the non-Hamiltonicity of `R_2` live?

## 2. Universal short-cycle picture

On the checked odd moduli

- `m = 5,7,9,11,13,15,17,19,21`,

the cycle decomposition of `R_2` has exactly one long cycle and a controlled
short-cycle part.

The universal checked feature is:

- there is always a `G`-only short-cycle family of size `(m-1)^2`,
- every such short cycle has length exactly `m`.

So the remaining defect is not spread across many branch types. It already
organizes itself into explicit short cycles.

## 3. The universal `G`-only family

For every checked modulus, the `G`-only short cycles satisfy:

- `x_2 = m-1` along the whole cycle,
- `x_4 = s` is constant along the whole cycle, with `s != m-1`,
- the invariant

`I_G = x_0 + 2 x_1 (mod m)`

is constant along the whole cycle.

Moreover, for each fixed `s in {0,...,m-2}`, the checked `G`-only cycles are
parameterized exactly by

- `I_G in Z/mZ`,
- excluding the single value `I_G = 1 - s`.

So for every checked modulus:

- each `x_4 = s` slice contributes exactly `m-1` `G`-only short cycles,
- hence the total `G`-only short-cycle count is exactly `(m-1)^2`.

This is not just a counting observation. It says the main short-cycle family is
already an explicit affine fiber family.

## 4. The extra `M`-only family when `3 | m`

On the checked moduli divisible by `3`,

- `m = 9,15,21`,

there is one additional short-cycle family.

Its checked properties are:

- every short cycle is `M`-only,
- `x_4 = m-1` is constant along the whole cycle,
- `x_2 = t` is constant along the whole cycle, with `t != m-1`,
- the invariant

`I_M = 2 x_0 + 3 x_1 (mod m)`

is constant along the whole cycle.

For each fixed `t in {0,...,m-2}`, the checked `M`-only cycles are
parameterized by

- `I_M in Z/mZ`,
- excluding the residue class `I_M == 1 (mod 3)`.

So on checked moduli divisible by `3`, each `x_2=t` slice contributes exactly
`2m/3` `M`-only short cycles, and the total `M`-only short-cycle count is

`(m-1) * (2m/3)`.

On the checked moduli not divisible by `3`, no `M`-only short cycles appear.

## 5. Meaning for the next theorem

This is the first point where the residual color-`2` problem stops looking like
a generic Hamiltonicity failure and starts looking like a very explicit surgery
problem.

What `276` shows is:

- there is one dominant long cycle;
- the defect part is not amorphous;
- it consists of a universal affine `G`-only short-cycle family;
- and, when `3 | m`, one extra affine `M`-only family.

So the next theorem should no longer be framed as

> “somehow prove `H_2` Hamilton.”

The honest next target is:

1. isolate the long cycle and the explicit short-cycle families,
2. prove a local splice/surgery rule that merges the `G`-only family into the
   long cycle,
3. in the divisible-by-`3` case, do the same for the extra `M`-only family.

That is much sharper than the earlier five-color assembly boundary.

## 6. Bottom line

The combined best `274` family is still not the final five-color package.

But after `275–276`, its failure is now explicit:

- a universal `G`-only short-cycle family parameterized by
  `x_2 = m-1`, `x_4`, and `x_0 + 2x_1`,
- plus, on `3 | m`, an extra `M`-only family parameterized by
  `x_4 = m-1`, `x_2`, and `2x_0 + 3x_1`.

So the graph-side frontier is no longer “search for a better family.”

It is: write the short-cycle surgery theorem that kills these explicit affine
families.
