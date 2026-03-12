Problem:
Determine the smallest lifted coordinate beyond grouped state after `041`, and
decide which object looks mathematically plausible if the goal is a
`d=3,4,5`-style odometer language rather than another ad hoc controller branch.

Current target:
Work the `042` branch on the fixed best-seed active corridor and separate:
- trigger-level lift,
- from closed structural lift.

Known assumptions:
- `037` gives the raw odometer on `(q,w,layer)`.
- `039` makes birth and family transport exact at raw level.
- `040` closes the raw current control logic.
- `041` kills the first grouped-state-descending admissible families.

Attempt A:
  Idea:
  Test the smallest plausible trigger lift over
  `B = (s,u,v,layer,family)`,
  namely
  `c = 1_{q = m-1}`.
  What works:
  `042` verifies on `m = 5,7,9,11` that:
  - `w = s-u`
  - exceptional fire already descends to `B`
  - regular fire descends to `(B,c)`
  - `c` is not a function of `B`
  So the trigger-level lift is smaller than full raw `q`.
  Where it fails:
  `(B,c)` still does not close the active transition law, so the carry bit is
  not the whole reduced dynamics.

Attempt B:
  Idea:
  Extract the structural lifted object directly from future behavior over the
  active grouped base.
  What works:
  The future-signature refinement over the active union has fiber size at most
  `3` over `B` on every checked modulus, and exactly `3` for `m = 7,9,11`.
  That is the right scale for a D5 odometer-style object:
  not full raw `q`, but a tiny finite cover over the grouped base.
  Where it fails:
  The admissible realization of that cover is still open.

Candidate lemmas:
- [C] `w = s-u mod m`.
- [C] Exceptional fire is a function of `B`.
- [C] Regular fire is a function of `(B,c)`.
- [C] `c` is not a function of `B`.
- [C] `(B,c)` is not dynamically closed.
- [C] The structural lift over `B` has fiber size at most `3`.
- [H] The most plausible D5 odometer-style statement is:
  grouped odometer/skew base plus a tiny finite-sheet lift.
- [H] This is better aligned with the D3/D4 language than a branch centered on
  full raw `q`.
- [O] The smallest admissible realization of the carry bit or the finite cover.

Needed computations/search:
- keep trigger and dynamics separated
- prioritize admissible exposure of the carry bit
- in parallel, formulate the finite-cover theorem cleanly
- do not reopen grouped-state-descending observable search

Next branching options:
1. Main branch:
   admissible carry-slice realization
2. Structural branch:
   finite-sheet cover theorem / no-go for smaller lifts
3. Only then:
   broader lifted-coordinate search

Claim status labels:
  [P] `025`
  [C] `037`, `039`, `040`, `041`, `042`
  [H] D5 should be organized as a finite-sheet lift over an odometer-style
      grouped base
  [F] grouped-state descent as the main admissibility branch
  [O] admissible lift
  [O] full D5 decomposition
