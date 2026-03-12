Problem:
Determine whether the raw current-coordinate control logic isolated in `040`
can be exposed inside the first admissible reduced families suggested by `025`,
or whether those families still fail by an exact grouped-state obstruction.

Current target:
Test the first `025`-style grouped-state-descending coordinate-surrogate
families on the fixed best-seed channel `R1 -> H_L1` and return either:
- a surviving smaller coordinate package, or
- the first exact admissibility no-go.

Known assumptions:
- `025` gives the reduced target `omit-base + edge-tied point cocycle defect`.
- `037` makes the lifted raw odometer visible on `(q,w,layer)`.
- `039` makes raw birth explicit and shows the family tag must be transported.
- `040` shows raw current coordinates already close the reduced control logic
  on the checked active union.

Attempt A:
  Idea:
  Treat the first admissible families as observables that descend to the
  current grouped state `(s,u,v)`, including canonical omit-base gauges and
  edge-tied cocycle coordinates anchored by `025`.
  What works:
  These are the right first admissible families to test because they preserve
  the reduced model and avoid reopening raw neighborhood search.
  Where it fails:
  The regular and exceptional fire predicates still collide on identical
  current grouped states, so any grouped-state-descending family fails.

Attempt B:
  Idea:
  Separate what already descends from what still needs a lift.
  What works:
  `w` already descends exactly as `w = s-u mod m`.
  Where it fails:
  The fire predicates do not descend, even after conditioning on the carried
  family bit, so one more lifted coordinate is still missing.

Candidate lemmas:
- [C] On the checked active union, `w = s-u mod m`.
- [C] The regular and exceptional fire predicates are not functions of the
  current grouped state `(s,u,v)`, even after conditioning on family.
- [C] Gauge-fixed omit-base base coordinates and edge-tied point cocycles from
  `025` do not improve those collision counts.
- [H] The exact missing admissibility ingredient is one lifted coordinate not
  determined by the current grouped state.
- [F] Another grouped-state-descending observable family is the right next main
  branch.
- [O] The smallest admissible lifted coordinate beyond current grouped state.

Needed computations/search:
- extract the exact reduced predicate package from `039/040`
- enumerate the first `025`-style grouped-state-descending coordinate
  surrogates
- save collision certificates for regular and exceptional fire
- state the precise next missing ingredient

Next branching options:
1. Main branch:
   admissible realization of one lifted coordinate beyond current grouped state
2. Secondary branch:
   theorem/no-go statement for all grouped-state-descending observables in the
   first `025` family
3. Only then:
   reopen broader realization classes if the lift target is still ambiguous

Claim status labels:
  [P] `025`
  [C] `037`, `039`, `040`, `041`
  [H] the next honest target is a lifted coordinate beyond current grouped
      state
  [F] grouped-state-descending coordinate-surrogate families as the main next
      branch
  [O] smallest admissible lift
  [O] full D5 decomposition
