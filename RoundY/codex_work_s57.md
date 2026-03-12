Problem:
After `042`, determine whether the D5 active branch should be organized as a
`3`-sheet cover over
`B = (s,u,v,layer,family)`
or more cleanly as the carry slice over `B` plus a residual `2`-sheet over
`B+c`, and test how structured that residual sheet already is on the checked
best-seed active union.

Current target:
Work the `043` branch on the fixed best-seed active corridor and package:
- the smallest verified trigger coordinate,
- the minimal deterministic cover over `B+c`,
- and the sharpest exact obstruction to replacing that residual sheet by an
  obvious simple bit.

Known assumptions:
- `037` gives the raw odometer on `(q,w,layer)`.
- `039` and `040` make the raw current control logic exact.
- `041` kills the first grouped-state-descending admissible families.
- `042` isolates the carry bit
  `c = 1_{q=m-1}`
  as the smallest verified trigger lift and bounds the structural cover over
  `B` by `3`.

Attempt A:
  Idea:
  Extract the minimal deterministic cover over `B+c`.
  What works:
  On `m = 5,7,9,11`, the minimal cover over `B+c` has fiber size at most `2`,
  with deterministic transition law on the lifted state.
  The ambiguous support lies entirely on the regular noncarry branch.
  So the clean structural picture is:
  `B <- B+c <- B+c+d`
  with residual binary sheet `d`.
  Where it fails:
  This still does not make the carry slice admissible locally by itself.

Attempt B:
  Idea:
  Test whether the residual binary sheet is one of the obvious simple
  coordinates.
  What works:
  The residual sheet is exactly the old `q=m-2` bit only on the `m=5` pilot.
  It is not that bit on `m=7,9,11`.
  Short future-carry windows do not recover it on larger moduli.
  A theorem-friendly but nonlocal coordinatization does exist via time to next
  carry.
  Where it fails:
  That coordinatization is not a tiny current observable, so it does not solve
  admissibility.

Candidate lemmas:
- [C] `w = s-u mod m` on the checked active union.
- [C] Exceptional fire descends to `B`.
- [C] Regular fire descends to `B+c`.
- [C] The minimal deterministic cover over `B+c` is at most `2`-sheet.
- [C] Its ambiguous support lies entirely on regular noncarry states.
- [C] The residual sheet is not `1_{q=m-2}` on `m=7,9,11`.
- [C] The residual sheet is not a short future-carry window on `m=7,9,11`.
- [H] The right D5 odometer language is grouped base + carry sheet + residual
  binary noncarry sheet.
- [O] The smallest admissible realization of either the carry sheet or the
  residual sheet.

Needed computations/search:
- package the `B+c` cover explicitly
- classify the residual support
- test obvious candidate residual bits
- keep admissibility and theorem extraction separate

Next branching options:
1. Main local branch:
   admissible realization of the carry slice
2. Structural branch:
   finite-cover theorem extraction over `B+c`
3. Only then:
   admissible realization of the residual binary sheet

Claim status labels:
  [P] `025`
  [C] `037`, `039`, `040`, `041`, `042`, `043`
  [H] D5 should be read as grouped base + carry sheet + residual binary
      noncarry sheet
  [F] jumping straight back to generic lifted-observable search
  [O] admissible carry / residual sheet realization
  [O] full D5 decomposition
