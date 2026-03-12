Problem:
Determine whether the raw current-coordinate control logic from `040` can be
compressed into the first admissible `025`-style reduced coordinate-surrogate
families, or whether those families still fail.

Current target:
Work the `041` admissibility branch on the fixed best-seed channel
`R1 -> H_L1` and return either the smallest surviving grouped-state surrogate
or the first exact obstruction.

Known assumptions:
- `025` gives the correct reduced target:
  omit-base plus edge-tied point cocycle defect.
- `037` makes the lifted corridor state visible on raw `(q,w,layer)`.
- `039` makes raw birth exact and shows the family tag must be carried.
- `040` shows the reduced control logic is already exact on raw current
  coordinates.

Attempt A:
  Idea:
  Test the first admissible grouped-state-descending families suggested by
  `025`: current grouped state `(s,u,v)`, canonical omit-base base gauges, and
  edge-tied point-cocycle coordinates on the diagonal / anti-diagonal omit
  bases.
  What works:
  This is the right first admissibility family because it stays inside the
  reduced model instead of reopening raw observable search.
  Where it fails:
  The regular and exceptional fire predicates are not functions of the current
  grouped state `(s,u,v)`, even after conditioning on the carried family bit.
  Every tested `025`-style gauge / cocycle family has exactly the same
  collision counts because it still descends to that same grouped state.

Attempt B:
  Idea:
  Separate the coordinates that already descend from the coordinate that still
  needs a lift.
  What works:
  `041` verifies on `m = 5,7,9,11` that `w` already descends exactly:
  `w = s-u mod m`.
  So part of the raw control package is already admissible at the grouped
  level.
  Where it fails:
  The fire predicates do not descend.
  Representative collision certificates show identical grouped states carrying:
  - non-target layer `>=2`,
  - and target layer `1`,
  with the same grouped coordinates and the same carried family.

Candidate lemmas:
- [C] `w = s-u mod m` on the checked active union.
- [C] Regular fire is not a function of current grouped state plus family.
- [C] Exceptional fire is not a function of current grouped state plus family.
- [C] Canonical omit-base gauges and point cocycles do not improve those
  collisions.
- [H] The exact missing ingredient is one lifted coordinate beyond current
  grouped state, equivalently a `q`-like / pre-grouped phase coordinate or an
  explicit transported marker.
- [F] Another grouped-state-descending observable family is the right main
  search.
- [O] The smallest admissible lifted coordinate.

Needed computations/search:
- keep the `041` obstruction theorem-shaped
- avoid reopening grouped-state-descending observables
- target the smallest admissible lift beyond `(s,u,v)`
- prefer branches that can either expose that lift or prove it impossible in a
  still narrower local class

Next branching options:
1. Main branch:
   search for the smallest admissible lifted coordinate beyond current grouped
   state
2. Secondary branch:
   sharpen `041` into a theorem/no-go for all grouped-state-descending
   observables in the first `025` class
3. Only then:
   open broader realization classes

Claim status labels:
  [P] `025`
  [C] `037`, `039`, `040`, `041`
  [H] the next honest branch is a lifted-coordinate admissibility branch
  [F] grouped-state-descending observables as the main next search
  [O] smallest admissible lift
  [O] full D5 decomposition
