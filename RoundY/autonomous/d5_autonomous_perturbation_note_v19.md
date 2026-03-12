Problem:
After `043`, decide whether the theorem branch can be made fully explicit and
whether that changes the local search priority.

Current target:
Work the `044` branch on the fixed best-seed active union and sharpen:
- the finite-cover normal form,
- the intrinsic residual binary coordinate,
- and the exact local target ordering.

Known assumptions:
- `042` gives the carry slice as the smallest verified trigger lift.
- `043` gives the binary cover over `B+c`.
- The local carry realization is still open.

Attempt A:
  Idea:
  Search for a canonical intrinsic binary coordinate for the residual sheet.
  What works:
  `044` verifies on `m = 5,7,9,11` that the residual sheet can be chosen as
  `d = 1_{next carry u >= m-3}`.
  This gives a deterministic lifted transition law on `B+c+d`.
  Where it fails:
  It is still a structural / anticipatory coordinate, not yet an admissible
  current observable.

Attempt B:
  Idea:
  Recast the whole checked active branch as a carry-first finite-cover normal
  form.
  What works:
  The checked active branch now reads cleanly as:
  `B = (s,u,v,layer,family)`,
  `c = 1_{q=m-1}`,
  `d = 1_{next carry u >= m-3}`.
  Exceptional fire closes on `B`, regular fire closes on `B+c`, carry states
  are singleton over `B+c`, and `d` is needed only on regular noncarry
  states.
  Where it fails:
  None on the theorem branch. The remaining open part is local realization of
  `c`.

Candidate lemmas:
- [C] The checked active branch factors as `B <- B+c <- B+c+d`.
- [C] `d = 1_{next carry u >= m-3}` is an exact binary anticipation sheet.
- [C] Carry states are singleton over `B+c`.
- [C] `d` is irrelevant on carry and exceptional states.
- [H] The right D5 manuscript language is grouped base + carry sheet + binary
  anticipation cover.
- [O] Admissible realization of `c`.

Needed computations/search:
- package `044`
- move the local branch to carry realization only
- optionally prepare formal / theorem notes for the new normal form

Next branching options:
1. Main branch:
   admissible realization of the carry sheet
2. Parallel structural branch:
   theorem proof / formalization of the `044` normal form
3. Only after that:
   admissible realization of the residual binary anticipation sheet if needed

Claim status labels:
  [P] `025`
  [C] `042`, `043`, `044`
  [H] D5 is grouped base + carry sheet + binary anticipation cover
  [F] broad residual-sheet search before carry realization
  [O] admissible carry realization
  [O] full D5 decomposition
