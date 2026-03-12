Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch, now that the grouped base problem
and the grouped twist problem have begun to separate.

Current target:
Use the `s41` adjacent-transposition observation to replace “find some richer
grouped `u` motion” by the sharper target:

find the smallest adjacent-transposition-based grouped base mechanism that
breaks the old diagonal obstruction, then isolate the remaining twist problem.

Known assumptions:
- `019` gives the extracted mixed grouped model with passive `u`.
- `020`, `021`, `022` prune binary, standard one-bit, and one-surface affine
  local families.
- `s41` says ternary same-`s` grouped permutations are built from fixed points
  and adjacent transpositions.
- `023` identifies the first genuine 2D reduced family:
  diagonal / anti-diagonal moving adjacent transpositions.

Attempt A:
  Idea:
  Use the `s41` classification literally and search one-row defects of the
  diagonal moving adjacent-transposition family.
  What works:
  This is the right reduced language. It searches fixed-point defects and
  adjacent-transposition defects, not arbitrary ternary noise.
  The result is strong: among `1190` valid one-row defect candidates, exactly
  `70` stable single grouped-base-orbit families appear, and every one of them
  is the same mechanism:
  omit the adjacent transposition on one chosen `s`-row.
  Representative example:
  baseline graph `u=s`, defect row `s=0`, no transposition on that row.
  This gives grouped base orbit size `[m^2]` on
  `m=5,7,9,11,13,15,17,19`.
  Where it fails:
  With the old twist `phi(s)` unchanged, the full grouped map on `(s,u,v)`
  still splits into `m` orbits of size `m^2`.
  So the grouped base obstruction is gone, but the twist is still one-dimensional.

Attempt B:
  Idea:
  Reinterpret the project as two separated subproblems:
  build the right grouped base first, then fix the twist.
  What works:
  This is now justified by evidence, not taste.
  `024` gives a single grouped-base orbit with a very small defect.
  So the remaining gap is no longer “find a second base coordinate.”
  It is:
  make the grouped twist depend on more than `s`, or otherwise couple it to the
  new base orbit.
  Where it fails:
  There is still no local realization of the omission defect.
  There is also still no reduced model for the needed `u`-dependent twist.

Candidate lemmas:
- [C] In the searched adjacent-transposition defect range, only omission
  defects produce a stable single grouped-base orbit.
- [H] The next local target should be:
  diagonal / anti-diagonal moving adjacent transposition with one omitted row.
- [C] After `024`, the grouped base obstruction is essentially solved at the
  reduced-model level.
- [H] The next remaining obstruction is the `phi(s)`-only twist.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- Search for a local paired carry mechanism that realizes the omission defect.
- In parallel, search the smallest twist perturbation that depends on the new
  grouped base coordinate rather than only on `s`.
- Compare local candidates against both signatures:
  single grouped-base orbit on `(s,u)` and nontrivial coupling in `v`.

Next branching options:
1. Main branch:
   local realization of the omission-defect grouped base.
2. Secondary branch:
   reduced search for the smallest `u`-dependent twist over that base.
3. Only after those:
   re-couple base and twist in the local rule space.

Claim status labels:
  [P] `019`
  [C] `020`, `021`, `022`, `024`
  [H] omission defect as the right next grouped-base target
  [O] full D5 decomposition
