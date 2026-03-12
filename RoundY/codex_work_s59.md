Task ID:
`D5-CARRY-ADMISSIBILITY-SEARCH-045`

Result:
- searched the fixed `045` carry-only admissibility catalogs exactly on
  `m = 5,7,9,11`
- parallel cached run completed in about `108s` with `32` workers
- `0` exact carry families survived across:
  - core current-edge / label / delta catalog up to size `5`
  - low-cardinality `025`-style gauge-transition catalog up to size `5`
  - targeted point-defect catalog up to size `4`
- full `B`, `B -> B_next`, and `B -> B_next -> B_next2` grouped transition
  classes also fail

Sharpest negative:
- best core / gauge negative is `next_dn`, then `dn + next_dn`
- these are exact on `m=5`
- on `m=7,9,11`, they miss only regular carry states, always on label `B`
- anchored `025`-style gauge bits do not improve that boundary

Conclusion:
- the first carry-only admissible families are now pruned
- the next missing admissibility datum is beyond current edge, `1`-step,
  `2`-step, and low-cardinality anchored-gauge data
- next branch:
  broader lifted gauge or deeper-than-`2`-step transition sheet, still
  targeting only `c = 1_{q=m-1}`
