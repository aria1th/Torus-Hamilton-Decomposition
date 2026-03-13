# D5 Compute Evidence For Proof Directions 052

## Goal

Prepare compute evidence that directly supports the two current proof
directions:

1. positive route:
   code the countdown carrier `tau` or its boundary reset
2. negative route:
   reduce the intended local class to bounded grouped transition/reset data
   and hit it with the witness family

## What was done

Artifact `052` consolidates theorem-side evidence through `m=19`.

It adds no new theorem object.
It packages the following as one machine summary:

- extended `047` quotient / horizon evidence
- the `049` constructive `rho` refinement
- the `050` reset-law and witness-family persistence

## Main support facts

Through `m = 5,7,9,11,13,15,17,19`:

- `B+tau` is exact away from `tau=0`
- `B+tau+epsilon4` is globally exact
- minimal exact tau truncation stays `m-3`
- minimal exact transition-sheet horizons stay:
  - `m-4` for current `epsilon4` + future binary after current
  - `m-3` for full event windows
  - `m-1` for pure binary windows
- the boundary is genuinely `3`-way for all tested `m>=7`
- the `048` reset law remains exact on the same theorem-side quotients
- the explicit witness family from `050` persists with the same
  `h < m-4` lower-bound shape

## Meaning

This is enough to support proof writing in both directions.

- positive route:
  boundary reset / countdown carrier is stable enough to target directly
- negative route:
  the bounded-horizon and bounded-transition story now has a cleaner
  larger-modulus evidence base

The next branch should be proof work, not broad search.
