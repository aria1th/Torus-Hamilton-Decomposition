Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch, now that the canonical witness has
an explicit reduced grouped model and the remaining obstruction is grouped
`u`-invariance.

Current target:
Find the smallest perturbation class that genuinely breaks the old `s`-only
grouped collapse, while staying close enough to the extracted mixed-witness
return law to be a plausible local target.

Known assumptions:
- `019` gives the exact reduced first return and grouped return for `mixed_008`.
- `020` shows a single binary carry-slice swap cannot create a genuine second
  grouped base coordinate.
- `021` shows the first paired `4↔2` family built from the standard one-bit
  atoms is still too weak.
- `022` shows the first richer one-surface affine selector family is still too
  weak.
- The live structural gap is no longer “find a better cocycle,” but “find the
  first honest extra grouped base coordinate beyond `s`.”

Attempt A:
  Idea:
  Search the first richer local paired family using single affine selector
  surfaces
  \[
  1_{a q + b s + c u = t}
  \]
  for both the layer-1 compensation selector and the carry-slice selector.
  What works:
  The search is broad enough to be meaningful: `93` selectors and `8649`
  ordered pairs at pilot modulus `m=11`.
  It preserves the current reduced `q,s,v` dynamics by design and therefore
  tests the right local boundary first.
  Where it fails:
  There are `900` valid pilot pairs but `0` genuine second-coordinate grouped
  base candidates.
  Every valid pilot pair still collapses to an `s`-only grouped `u`-cocycle.
  More sharply: every valid pilot pair avoids `u` entirely, so within this
  one-surface affine family, true `u`-dependence is incompatible with grouped
  base bijectivity.

Attempt B:
  Idea:
  Move up one level and search grouped reduced perturbations directly, asking
  for the smallest genuinely two-dimensional grouped base mechanism.
  What works:
  A moving adjacent transposition along a diagonal or anti-diagonal graph
  \[
  u = \pm s + b
  \]
  is the first clean reduced perturbation that genuinely breaks the old
  `s`-only collapse.
  For all checked odd moduli `m=5,7,9,11,13,15,17,19`, it gives grouped base
  orbit sizes `[m, m(m-1)]` and full grouped orbit sizes on `(s,u,v)` equal to
  `[m^2, m^2(m-1)]`.
  So it is already almost transitive on the full grouped state.
  Where it fails:
  It still leaves one residual invariant diagonal orbit of size `m^2`.
  A search over one-graph and two-graph affine transposition families in the
  same range finds no single grouped-base orbit of size `m^2`.

Candidate lemmas:
- [C] Single binary carry-swaps are too weak to produce a genuine second
  grouped base coordinate.
- [C] The first paired local family built from the standard one-bit atoms is
  still too weak.
- [C] The first one-surface affine paired family is still too weak; every valid
  pilot pair avoids `u`.
- [H] The first honest reduced perturbation beyond the old `s`-only collapse is
  a diagonal or anti-diagonal moving adjacent transposition.
- [H] The residual obstruction in that reduced family is a single invariant
  diagonal orbit.
- [H] The most plausible next local target is therefore a paired carry
  mechanism whose grouped effect emulates the diagonal moving transposition,
  plus one controlled defect that breaks the diagonal.

Needed computations/search:
- Try to realize the diagonal moving transposition as a local paired carry
  mechanism using a non-affine or predecessor/tail selector.
- Search a one-defect version of the diagonal moving transposition at grouped
  level before going back to local rule space.
- Compare any local candidate against the diagonal-transposition signature on
  grouped orbit sizes, not just on raw `u`-carry.

Next branching options:
1. Main branch:
   local search for a paired carry mechanism whose grouped effect matches the
   diagonal moving transposition.
2. Secondary branch:
   grouped one-defect search that breaks the residual invariant diagonal while
   preserving the large `m^2(m-1)` orbit.
3. If both fail:
   move from current-state selectors to exact predecessor / short-memory bits,
   because the one-surface current-state families are now well pruned.

Claim status labels:
  [P] `019` reduced model
  [C] `020`, `021`, `022` obstructions
  [H] diagonal moving transposition as the first genuine 2D reduced
      perturbation
  [O] full D5 decomposition
