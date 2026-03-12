Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch after `039`, where the raw birth
predicates and raw target predicates were already explicit.

Current target:
Decide whether the fixed raw carrier logic is itself still the live problem, or
whether the only remaining gap is exposure / admissibility of the right
coordinate-level observables.

Known assumptions:
- `037` extracts the raw corridor odometer and the family-specific targets.
- `038` kills the simple small projection search in the point neighborhood bit
  alphabet.
- `039` makes the source and entry birth predicates exact on raw current
  coordinates and packages the raw tagged carrier model.

Attempt A:
  Idea:
  Test the first richer families still generated from the same simple `038`
  alphabet: full current row, source-edge full-row pair, lag-1 full-row pair,
  lag-2 full-row pair.
  What works:
  `040` shows these families still do not solve the realization problem.
  - full simple row still does not isolate source or entry
  - source-edge full-row pair still does not isolate the source class
  - lag-1 and lag-2 full-row pairs still fail on the exceptional trigger for
    every checked `m`
  - regular trigger uniqueness in those simple lag families also degrades by
    `m=9,11`
  Where it fails:
  So the next family is not “the same simple alphabet, but with one more lift”.

Attempt B:
  Idea:
  Test whether the fixed raw carrier logic is already exact on coordinate-level
  current observables.
  What works:
  Yes.
  On checked moduli `m = 5,7,9,11`:
  - birth on raw current coordinates is exact
  - current `(q,w,u,layer)` already separates the active source families on the
    traced active union
  - active-conditioned target firing by current `(q,w,layer)` has zero prehits
    on both regular and exceptional branches
  So the control logic itself is already closed at the reduced raw-coordinate
  level.
  Where it fails:
  This is still a realization boundary result, not a final local mechanism,
  because admissibility / exposure of those coordinate-level observables
  remains open.

Candidate lemmas:
- [C] The fixed raw carrier logic from `037/039` is machine-readable and exact
  on checked moduli.
- [C] Full simple-row current / source-edge / lag-1 / lag-2 families still do
  not realize the branch.
- [C] On traced active states, current `(q,w,u,layer)` already determines the
  active source family.
- [C] Active-conditioned current `(q,w,layer)` triggers exactly at the regular
  and exceptional targets with zero prehits on checked moduli.
- [H] The remaining gap is exposure / admissibility of coordinate-level
  observables, not controller-logic discovery.
- [F] “Try a slightly richer lift of the same simple 038 row” is the right next
  branch.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- stop treating transport logic itself as unknown
- separate:
  - reduced control logic,
  - and local exposure / admissibility of the needed coordinates
- only after that, choose between:
  - a coordinate-exposure mechanism branch,
  - or an admissibility / no-go theorem branch

Next branching options:
1. Main branch:
   coordinate-exposure / admissibility for the raw current observables that
   already realize the reduced control logic.
2. Secondary branch:
   a theorem/no-go statement for all simple-row-derived source-edge and short
   temporal lifts.
3. Only then:
   reopen genuinely new observable families.

Claim status labels:
  [P] `019`, `025`
  [C] `032`, `033`, `035`, `036`, `037`, `038`, `039`, `040`
  [H] controller logic is no longer the live issue; exposure / admissibility is
      the live issue
  [F] reusing the same simple row with slightly richer lifts as the main branch
  [O] local admissibility of the coordinate-level raw observables
  [O] full D5 decomposition
