# D5 197: sigma23 immediate-`R1` microstate check

## Purpose

This note executes the focused local compute request isolated in `196`.
The source row is the centered-left case

- `sigma21 = [4,1,4] / [1,2,2]`,

and the target question is whether the surviving immediate `R1` local move can
land in the terminal-right-skip case

- `sigma23 = [4,1,4] / [2,2,1]`.

## Implementation used

The computation uses the exact family-labelled local transition builder already
present in the recovered `032` code:

- `scripts/torus_nd_d5_endpoint_latin_repair.py`

The dedicated checker added here is:

- `scripts/torus_nd_d5_sigma23_r1_microstate_check_197.py`

Outputs:

- `RoundY/checks/d5_197_sigma23_r1_microstate_summary.json`
- `RoundY/checks/d5_197_sigma23_r1_microstate_check/per_modulus.json`
- `RoundY/checks/d5_197_sigma23_r1_microstate_check/symmetry_reduced_microcases.json`

## What was checked

For each odd modulus

- `m = 5,7,9,11,13,15,17`,

the script builds the three centered-left prototypes

- `sigma21 = [4,1,4] / [1,2,2]`,
- `sigma22 = [4,1,4] / [2,1,2]`,
- `sigma23 = [4,1,4] / [2,2,1]`,

then enumerates every `R1` source in `sigma21`, records its immediate image and
its second-step image, and compares that actual two-step continuation with the
`sigma22` and `sigma23` prototypes from the same rooted source.

The symmetry reduction used in the output is rooted torus translation on the
local source microstate.

## Main compute result

The checked result is uniform across the whole range.

1. For every checked modulus, the entire `sigma21` immediate `R1` source family
   collapses to exactly one rooted translation class.
2. In that class, the source neighborhood is always
   `neighbor_labels_by_direction = [B, R2, B, B, B]`.
3. The actual immediate image is always the relative state
   `(+q, +w) = (1, 0)`.
4. The actual second-step image is always the relative state
   `(+q, +w) = (1, 1)`.
5. That second-step image agrees exactly with the `sigma22` prototype and
   disagrees exactly with the `sigma23` prototype.

So, on the checked range, every surviving immediate microcase has

- image right word `[2,1,2]`,
- `Delta_R = {1,2}`,
- unchanged slot `3`,
- compatibility `sigma22 = true`, `sigma23 = false`.

## Representative microcase

The normalized representative is already visible at every checked modulus:

- source payload `(q,w,v,u,layer,s) = (m-1, 0, 0, 2, 1, 2)`,
- immediate image `(0, 0, 0, 2, 2, 2)`,
- actual second image `(0, 1, 0, 2, 3, 3)`,
- `sigma22` second image `(0, 1, 0, 2, 3, 3)`,
- `sigma23` second image `(m-1, 2, 0, 2, 3, 4)`.

In other words, the actual `R1` continuation lands on the middle-slot witness
branch and not on the terminal-right-skip branch.

## Status consequence

This compute does not by itself give a manuscript proof for all odd `m`.
But it does remove the old ambiguity in the checked range:

> no checked immediate `R1` microstate out of `sigma21` realizes the
> `sigma23` pattern.

So the remaining theorem-side burden is now to promote this local behavior from
the checked exact family-labelled implementation to an all-odd local theorem.
