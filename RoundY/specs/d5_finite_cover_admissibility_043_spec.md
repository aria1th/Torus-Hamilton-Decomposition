# D5-FINITE-COVER-ADMISSIBILITY-043

## Question
For the unresolved best-seed active corridor in the seed pair
- left = `[2,2,1]`
- right = `[1,4,4]`

after `042`, is the next missing admissible state best modeled as:
1. the **carry-slice trigger bit**
   \[
   c = \mathbf 1_{\{q=m-1\}},
   \]
   which is enough for regular triggering, or
2. a **tiny finite-sheet lift** over the grouped base
   \[
   B = (s,u,v,\lambda,f),
   \]
   with \(\lambda=\text{layer}\) and \(f\in\{\mathrm{regular},\mathrm{exceptional}\}\),
   which is the true structural object behind the D5 corridor dynamics?

The next job is to determine the smallest admissible lifted coordinate needed for:
- trigger realization, and
- theorem-level structural closure.

## Purpose
`037–040` solved the raw reduced control logic.
`041` showed the first grouped-state-descending admissible families are too small.
`042` sharpened that wall:
- `w` already descends exactly as \(w = s-u\),
- exceptional fire already descends to \(B\),
- regular fire descends to \(B+c\),
- \(c\) is not a function of \(B\),
- but \(B+c\) is still not dynamically closed,
- and the checked active-union lift over \(B\) has fiber size at most `3`.

So the next honest target is **not** full raw `q`, and not another controller search.
It is:
- trigger-level admissible realization of the carry slice, and
- theorem-level extraction of the tiny finite cover over the grouped odometer / skew-odometer base.

## Fixed inputs
- reduced target from `025`:
  - omit-base plus edge-tied point cocycle defect,
  - grouped base orbit size `m^2`,
  - full grouped orbit size `m^3`
- unresolved best seed from `033`:
  - left = `[2,2,1]`
  - right = `[1,4,4]`
- raw odometer / carrier extraction from `037`, `039`, `040`
- grouped admissibility obstruction from `041`
- carry-slice / finite-cover split from `042`
- checked moduli:
  - `m in {5,7,9,11}`

## Known checked facts to treat as input
### Raw control logic
- birth classes are exact on raw current coordinates:
  - source: `layer=1, q=m-1, w=0, u!=0`
  - exceptional source: `u=3`
  - entry: `layer=2, q=m-1, w=1, u!=0`
  - exceptional entry: `u=3`
- raw current `u` drifts later, so family must be initialized at birth
- active carrier model is:
  - `off`
  - `active_reg`
  - `active_exc`
- regular fire:
  - `(q,w,layer)=(m-1,m-2,1)` via direction `[2]`
- exceptional fire:
  - `(q,w,layer)=(m-2,m-1,1)` via direction `[1]`

### Grouped / lifted facts
- \(w=s-u\) exactly on the checked active union
- let
  \[
  B=(s,u,v,\lambda,f)
  \]
- exceptional fire is already a function of `B`
- regular fire is not a function of `B`
- regular fire becomes a function of `B+c`, where
  \[
  c=\mathbf 1_{\{q=m-1\}}
  \]
- `c` is not a function of `B`
- `B+c` is not dynamically closed
- the checked future-signature lift over `B` has fiber size at most `3`
- after adding `c`, the residual ambiguity is at most `2`-sheet

## Main conjectural picture to test
The active D5 branch should be formulated as:
\[
\text{grouped odometer / skew-odometer base } B
\quad + \quad
\text{tiny finite-sheet lift } \widetilde B \to B,
\]
with two different uses of the lift:
- **trigger level:** only the carry-slice bit may be needed;
- **structural level:** a genuine `<=3`-sheet cover may be the correct theorem object.

So the missing ingredient is likely:
- not full raw `q`,
- not more controller state,
- but one tiny lifted sheet over the grouped base.

## Allowed methods
- exact checked-modulus analysis on the active union for `m=5,7,9,11`
- extraction of minimal finite covers over `B` and over `B+c`
- future-signature or return-signature refinement, provided it is saved explicitly
- search for admissible observables only in families that could realize:
  - the carry slice `c`, or
  - the residual `2`-sheet refinement over `B+c`
- theorem-first reformulation of the active corridor as a finite cover of a grouped odometer / skew-odometer base
- no reopening of generic transducer search
- no reopening of grouped-state-descending point-cocycle families already killed by `041`
- no default escalation to full raw `q`

## Success criteria
### Trigger-level success
1. Identify the smallest admissible observable family that realizes the carry-slice bit
   \[
   c=\mathbf 1_{\{q=m-1\}}.
   \]
2. Verify that this yields exact regular triggering over `B+c` on `m=5,7,9,11`.
3. Keep exceptional fire descending directly to `B`.

### Structural success
4. Extract the minimal deterministic finite cover over `B` on the checked active union.
5. Decide whether the cover is best viewed as:
   - a 3-sheet cover over `B`, or
   - a carry bit plus a residual 2-sheet refinement over `B+c`.
6. Save an explicit transition law on the cover.
7. State the clean manuscript formulation:
   - grouped odometer / skew-odometer base,
   - plus finite-sheet lift.

## Failure criteria
- no admissible realization of the carry slice is found in the next plausible lifted family, and
- the finite-cover extraction still does not suggest a compact theorem-shaped lift.

If failure occurs, report the exact next missing datum:
- a larger lifted coordinate than carry slice,
- a residual 2-sheet noncarry refinement,
- or a stronger admissibility obstruction beyond the present `025`-style class.

## Candidate lemmas
- [C] On the checked active union, \(w=s-u\) exactly.
- [C] Exceptional fire descends to \(B=(s,u,v,\lambda,f)\).
- [C] Regular fire descends to \(B+c\) with \(c=\mathbf 1_{\{q=m-1\}}\).
- [C] The carry slice `c` is not a function of `B`.
- [C] `B+c` is not dynamically closed.
- [C] The active lift over `B` has checked fiber size at most `3`.
- [H] The right D5 manuscript language is grouped odometer / skew-odometer base plus tiny finite-sheet lift.
- [H] Full raw `q` is too coarse as the next default lifted object.
- [F] Another grouped-state-descending observable search on the same current quotient is the right next move.
- [O] Full D5 Hamilton decomposition remains open.

## Most useful next subbranches
### 043A. Carry-slice realization branch
Search only for admissible realization of
\[
c=\mathbf 1_{\{q=m-1\}}
\]
in the smallest plausible lifted local / cocycle family.

This is the best next branch if the goal is the next concrete local positive result.

### 043B. Finite-cover theorem branch
Extract and coordinatize the minimal finite cover over `B`, preferably as:
- one carry sheet, plus
- one residual binary sheet on the noncarry branch.

This is the best next branch if the goal is the manuscript-level D3/D4/D5 odometer story.

## Recommendation
Treat the two branches as coupled but not identical:
- **local realization priority:** 043A first
- **theorem / narrative priority:** 043B in parallel or immediately after

The strongest current unifying language is:
- `d=3`: odometer-style return map
- `d=4`: affine / second-return odometer
- `d=5`: grouped odometer / skew-odometer base plus tiny finite cover

## Artifacts to save
- code
- raw logs
- summary report
- `carry_slice_realization_summary_043.json`
- `finite_cover_transition_summary_043.json`
- `residual_two_sheet_summary_043.json`
- `manuscript_language_note_043.md`
- proof-supporting computations

## Return format
- smallest verified lifted trigger coordinate
- whether it is exactly the carry slice
- smallest verified structural cover over `B`
- whether the cover is 3-sheet over `B` or 2-sheet over `B+c`
- clean theorem-level D5 language
- explicit recommendation for the next local branch
