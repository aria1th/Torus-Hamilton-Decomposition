# D5 115 Tiered Selector Execution Summary

This note records the executable part of the shrunk `115` compute request and
its checked outcome.

Primary artifacts:

- [../checks/d5_115_tiered_selector_summary.json](../checks/d5_115_tiered_selector_summary.json)
- [../checks/d5_115_slice4_transport_search.json](../checks/d5_115_slice4_transport_search.json)
- [../../scripts/torus_nd_d5_tiered_selector_checks_115.py](../../scripts/torus_nd_d5_tiered_selector_checks_115.py)
- [../../scripts/torus_nd_d5_slice4_transport_search_115.py](../../scripts/torus_nd_d5_slice4_transport_search_115.py)

The old broad defect-slice weighted search was not rerun. Instead, the
executable `115` program was interpreted literally:

1. freeze the pattern-only selector quotient;
2. rerun the small-tier MILP checks and transfer checks;
3. rerun the transport statistics that isolate the slice-4 bottleneck;
4. test a concrete intermediate family for slice-4 compression.

## 1. Reproduced small-tier selector data

The pattern-only MILP on slices `Sigma = 2,3` was rerun for
`m = 5,7,9,11`.

The reproduced values match the existing tmp summary exactly.

Highlights:

- slice `2`, `m = 11`:
  clean `66550`, free optimum `67123`, cyclic optimum `67100`;
- slice `3`, `m = 11`:
  clean `61105`, free optimum `61905`, cyclic optimum `61105`.

The `m = 9` free-opt pattern assignment was then reused without change on
larger moduli and remained exact on both checked targets:

- `m = 11` exact on slices `2` and `3`;
- `m = 13` exact on slices `2` and `3`.

So the small-tier message from `115` survives direct rerun:
the selector-row side is already stable at the 31-pattern level, and larger
full-torus weighted searches are not the right next compute target.

## 2. Reproduced transport bottleneck

The transport statistics from the shrunk request were also rerun.

On slice `3`:

- `F_3^- = (Z,M)` exactly determines the predecessor raw row on `m = 9,11`;
- `F_3 = (B_2,B_3,Z,M)` exactly determines both the outgoing slice-3 raw row
  and the predecessor slice-2 raw row on `m = 9,11`.

On slice `4`:

- `F_4^- = (B_2,B_3,Z,M)` exactly determines the predecessor slice-3 raw row;
- but `F_4^-` does not determine the predecessor `F_3`-state:
  on `m = 9` there are `2470` nondeterministic `(state,j)` pairs, and the same
  count persists on `m = 11`;
- `F_4^{full} = (fullpairs, Z, M)` does determine the predecessor
  `F_3`-state exactly, with state counts `6561` on `m = 9` and `14641` on
  `m = 11`.

So the real compute bottleneck remains exactly the one named in `115`:
compress slice-4 transport strictly below `F_4^{full}` while keeping exact
transport to `F_3`.

## 3. Executed slice-4 candidate search

One concrete search family from the `115` request was run explicitly.

Candidate family:

- target slice `4`;
- base memory `(Z,M)`;
- add pair-sum indicator sets `B_k`;
- test all nonempty subsets of `k in {0,1,2,3,4,5}`;
- require exact transport to predecessor `F_3 = (B_2,B_3,Z,M)` on both
  `m = 9` and `m = 11`.

Outcome:

- total subsets tested: `63`;
- exact subsets found: `0`.

The best candidate in that family was
`(B_0,B_1,B_2,B_3,B_4,Z,M)`, but it still leaves

- `575` nondeterministic `(state,j)` pairs on `m = 9`,
- `840` nondeterministic `(state,j)` pairs on `m = 11`.

The natural extension `(B_0,...,B_5,Z,M)` also fails:

- `400` nondeterministic pairs on `m = 9`,
- `1385` nondeterministic pairs on `m = 11`.

The original lower field `(B_2,B_3,Z,M)` remains much smaller, but still has
`2470` nondeterministic pairs on both `m = 9` and `m = 11`.

So the tested `B_k`-subset family does not yet close slice-4 transport.

## 4. Orbit-quotient check

The other natural `115` suggestion, the cyclic orbit quotient of
`(fullpairs, Z, M)`, was also checked.

It fails badly as a transport field:

- on `m = 9`, state count `1313`, nondeterministic pairs `6350`;
- on `m = 11`, state count `2929`, nondeterministic pairs `13835`.

So the straightforward cyclic quotient of the exact full field destroys too
much absolute information for deterministic predecessor transport.

## 5. Updated status

The executable part of `115` now supports the following sharper status claim.

- The small-tier selector completion is reproducibly closed.
- Slice `3` transport is already controlled by a finite field of size about
  `1.6e3`.
- Slice `4` transport is still the bottleneck.
- Within the first natural intermediate family
  `(B_k for k in subset, Z, M)` for `subset ⊆ {0,1,2,3,4,5}`, there is no
  exact field on both `m = 9` and `m = 11`.
- The straightforward cyclic orbit quotient of the exact full field is also a
  no-go.

So the next search should move beyond this first `B_k`-subset family, rather
than back to the old broad weighted 1-factorization request.
