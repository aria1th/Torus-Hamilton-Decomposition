Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch, now that the reduced grouped base
and reduced grouped twist can be analyzed separately.

Current target:
Turn the `024` omit-base candidate into a full reduced normal form by finding
the smallest cocycle defect that yields a single grouped orbit on `(s,u,v)`.

Known assumptions:
- `019` gives the baseline mixed grouped model.
- `021` and `022` prune the obvious local selector families.
- `023` identifies the diagonal / anti-diagonal moving adjacent transposition
  as the first genuine 2D reduced base family.
- `024` shows that omitting the transposition on one row already gives a single
  grouped-base orbit of size `m^2`.
- `s42` points out the remaining issue: if the twist stays `s`-only, base
  merging alone cannot finish the full grouped orbit.

Attempt A:
  Idea:
  Add the smallest cocycle defects tied to the omitted edge of the `024`
  representative and test which ones produce a single full grouped orbit.
  What works:
  This is enough. A single-point cocycle defect at either omitted edge endpoint
  already yields a single grouped orbit of size `m^3` on
  `m=5,7,9,11,13,15,17,19`.
  The two-point omitted-edge defect also works.
  Where it fails:
  Row-sized and graph-sized defects still collapse. So the twist correction has
  to stay genuinely local; it cannot be another `s`-only or graph-wide defect.

Attempt B:
  Idea:
  Reframe the next local search around the full reduced target, not around the
  old separated subproblems.
  What works:
  The reduced target is now explicit:
  diagonal / anti-diagonal omit-base plus a pointwise edge-tied cocycle defect.
  This is the first reduced D5 model on this branch that gives a single orbit
  of size `m^3`.
  Where it fails:
  There is still no local realization of that reduced model.

Candidate lemmas:
- [C] The omit-base candidate from `024` gives a single grouped-base orbit of
  size `m^2`.
- [C] One-point and two-point omitted-edge cocycle defects upgrade that reduced
  model to a single grouped orbit of size `m^3`.
- [C] Row-sized and graph-sized cocycle defects do not.
- [H] The next local target should match this full reduced signature, not just
  the base part.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- Search for a local paired carry mechanism that realizes both:
  the omitted-row base defect and the pointwise edge cocycle defect.
- Use the reduced orbit signature `m^3` on `(s,u,v)` as the acceptance test.
- Avoid broader selector sweeps until that exact target is either realized or
  sharply ruled out.

Next branching options:
1. Main branch:
   tiny local search aimed at the full reduced `025` signature.
2. Secondary branch:
   look for gauge-equivalent local twist defects if the exact point defect is
   not realizable.
3. Only after that:
   widen the local state space.

Claim status labels:
  [P] `019`
  [C] `021`, `022`, `024`, `025`
  [H] full reduced normal form candidate identified
  [O] full D5 decomposition
