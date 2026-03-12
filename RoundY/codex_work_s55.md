Problem:
After `041`, grouped-state-descending observables are exhausted. Determine
whether the next honest lift is full raw `q`, a smaller carry-slice bit, or a
small finite cover over the grouped active base.

Current target:
Work the first lifted branch over
`B = (s,u,v,layer,family)`
on the fixed best-seed active corridor and determine the smallest verified lift
that:
- makes the trigger logic exact,
- and clarifies the right odometer-style structural object.

Known assumptions:
- `037` extracts the raw odometer on `(q,w,layer)`.
- `039` fixes exact raw birth and family transport requirements.
- `040` makes the raw current control logic exact.
- `041` proves the first `025`-style grouped-state-descending families are too
  small.

Attempt A:
  Idea:
  Test the carry-slice bit
  `c = 1_{q = m-1}`
  as the smallest lift over
  `B = (s,u,v,layer,family)`.
  What works:
  On checked moduli:
  - `w = s-u`
  - exceptional fire is already a function of `B`
  - regular fire becomes a function of `(B,c)`
  - `c` is not a function of `B`
  Where it fails:
  `(B,c)` still does not make the active transition law deterministic.

Attempt B:
  Idea:
  Extract the structural lifted object as a finite cover over `B`, rather than
  only as a pointwise trigger bit.
  What works:
  The future-signature refinement over the checked active union has fiber size
  at most `3` over every checked modulus, and exactly `3` for `m=7,9,11`.
  That gives a small-cover interpretation compatible with an odometer-style
  viewpoint.
  Where it fails:
  This does not yet expose an admissible local observable for that cover.

Candidate lemmas:
- [C] `w = s-u mod m` on the checked active union.
- [C] Exceptional fire descends to `B = (s,u,v,layer,family)`.
- [C] Regular fire descends to `(B,c)` with `c = 1_{q=m-1}`.
- [C] `c` is not a function of `B`.
- [C] `(B,c)` is still not dynamically closed.
- [C] The extracted future-signature lift has fiber size at most `3` over `B`.
- [H] The right odometer-style object for D5 is a tiny finite-sheet lift over
  the grouped base, not full raw `q`.
- [O] The smallest admissible observable realizing that lift.

Needed computations/search:
- keep trigger logic separate from dynamic closure
- target admissible realization of the carry bit first
- in parallel, treat the finite-sheet cover as the structural theorem target
- avoid reopening grouped-state-descending search

Next branching options:
1. Main branch:
   admissible realization of the carry-slice bit
2. Structural branch:
   theorem/no-go for the minimal finite-sheet cover over `B`
3. Only then:
   reopen broader lifted observables if both fail

Claim status labels:
  [P] `025`
  [C] `037`, `039`, `040`, `041`, `042`
  [H] D5 should be read as a tiny-sheet lift over an odometer-style grouped
      base
  [F] grouped-state-descending observables as the main next search
  [O] admissible carry-bit / finite-cover realization
  [O] full D5 decomposition
