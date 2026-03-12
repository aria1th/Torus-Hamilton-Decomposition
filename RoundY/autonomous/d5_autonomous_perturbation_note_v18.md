Problem:
Determine whether the `042` tiny-cover picture is best organized as a
`3`-sheet cover over
`B = (s,u,v,layer,family)`
or as a carry sheet over `B` plus a residual binary sheet over `B+c`, and
decide which description is better for the D5 odometer-style branch.

Current target:
Work the `043` branch on the fixed best-seed active union and sharpen the
finite-cover statement past the first carry-slice split.

Known assumptions:
- `037` gives the raw odometer on `(q,w,layer)`.
- `039` makes birth and family transport exact at raw level.
- `040` closes the raw current control logic.
- `041` kills the first grouped-state-descending admissible families.
- `042` isolates `c = 1_{q=m-1}` as the smallest verified trigger lift and
  bounds the structural lift over `B` by `3`.

Attempt A:
  Idea:
  Extract the minimal deterministic cover over `B+c`.
  What works:
  `043` verifies on `m = 5,7,9,11` that the minimal deterministic cover over
  `B+c` has fiber size at most `2`.
  Its support lies entirely on regular noncarry states and it gives a
  deterministic lifted transition law.
  So the clean structural picture is
  `B <- B+c <- B+c+d`
  with residual binary sheet `d`.
  Where it fails:
  This still does not make the carry slice or residual sheet admissible in the
  intended local class.

Attempt B:
  Idea:
  Test whether the residual binary sheet is one of the obvious simple bits.
  What works:
  On `m=7,9,11`, the residual sheet is not `1_{q=m-2}`.
  Short future-carry windows also fail badly:
  the first exact carry-window lengths are `29,55,89`.
  A theorem-friendly coordinatization exists via time to next carry.
  Where it fails:
  That coordinatization is nonlocal and does not settle admissibility.

Candidate lemmas:
- [C] Exceptional fire descends to `B`.
- [C] Regular fire descends to `B+c`.
- [C] The minimal deterministic cover over `B+c` is `2`-sheet on the checked
  active union.
- [C] The residual `2`-sheet support lies entirely on regular noncarry states.
- [C] The residual `2`-sheet is not the obvious bit `1_{q=m-2}` on
  `m=7,9,11`.
- [C] Time to next carry coordinatizes the residual cover nonlocally.
- [H] The right D5 manuscript language is grouped base + carry sheet +
  residual binary noncarry sheet.
- [O] The smallest admissible realization of the carry sheet.
- [O] The smallest admissible realization of the residual binary sheet.

Needed computations/search:
- keep theorem extraction separate from admissibility
- prioritize admissible carry-slice realization first
- treat the residual `2`-sheet as the next structural theorem object
- do not reopen broad lifted-observable search yet

Next branching options:
1. Main branch:
   admissible realization of the carry slice
2. Parallel theorem branch:
   explicit finite-cover theorem over `B+c`
3. Later:
   admissible realization of the residual binary sheet if the carry branch
   succeeds

Claim status labels:
  [P] `025`
  [C] `037`, `039`, `040`, `041`, `042`, `043`
  [H] D5 should be phrased as grouped base + carry sheet + residual binary
      noncarry sheet
  [F] reopening generic lifted-observable search before fixing the carry lift
  [O] admissible carry / residual realization
  [O] full D5 decomposition
