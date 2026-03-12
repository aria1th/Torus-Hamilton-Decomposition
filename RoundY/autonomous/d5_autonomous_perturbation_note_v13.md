Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch after `037`, where the unresolved
best-seed corridor already has visible raw odometer phase.

Current target:
Decide whether the next reduced target is really “marker plus family bit” as a
coupled problem, or whether one of those is already locally available at
birth.

Known assumptions:
- `033` reduces the best-seed obstruction to the unresolved `R1 -> H_L1`
  corridor.
- `035` prunes the first static phase-gate branch.
- `036` lifts the long corridor to `(q,a,layer)`.
- `037` shows that lift is already visible on raw `(q,w,layer)`, so the live
  issue is corridor localization.

Attempt A:
  Idea:
  Search a small raw birth-local neighborhood alphabet for a direct source or
  entry marker.
  What works:
  `038` searches all projections of size `1..5` in the simple alphabet built
  from:
  - current `layer, q=-1, phase_align, wu2`
  - one-step predecessor `phase_align, wu2` in directions `0..4`
  - one-step successor `phase_align, wu2` in directions `0..4`
  over `m = 5,7,9,11`.
  The result is exact:
  - no source-marker isolator up to size `5`
  - no entry-marker isolator up to size `5`
  - no entry-exceptional isolator up to size `5`
  Where it fails:
  The marker itself is still not birth-local in this small neighborhood
  family.

Attempt B:
  Idea:
  Check whether the exceptional source family `u_source = 3` is already locally
  visible once the source class is known.
  What works:
  Yes.
  The source-exceptional slice is already separated by size-`1`:
  - `pred2_wu2`
  - `pred4_wu2`
  and both bits give:
  - regular source values `{0}`
  - exceptional source values `{1}`
  on every checked `m = 5,7,9,11`.
  So the family bit is locally cheap at the source.
  Where it fails:
  This does not create the source marker itself, and it does not remain visible
  at entry.

Candidate lemmas:
- [C] In the simple birth-local neighborhood alphabet, there is no source
  marker isolator of size `<= 5`.
- [C] In the same alphabet, there is no entry marker isolator of size `<= 5`.
- [C] The exceptional source slice is already visible by the one-bit tests
  `pred2_wu2` and `pred4_wu2`.
- [C] The exceptional entry slice is not visible by any size-`<= 5`
  projection in that alphabet.
- [H] The next live branch should focus on source-local marker creation, not on
  inventing the family bit.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- stop coupling “marker” and “family bit” as the same open subproblem
- search for the smallest richer observable or dynamic mechanism that creates a
  source-local marker
- once that source class is captured, reuse the cheap one-bit exceptional
  source test rather than reopening family-bit search at entry

Next branching options:
1. Main branch:
   source-local marker search in a richer observable or coupled carrier family.
2. Secondary branch:
   a no-go theorem for any size-`<= 5` simple birth-local neighborhood marker.
3. Only then:
   reopen broader carrier synthesis.

Claim status labels:
  [P] `019`, `025`
  [C] `032`, `033`, `035`, `036`, `037`, `038`
  [H] the marker is the live obstruction; the family bit is already easy at
      birth once the source class is localized
  [F] treating the family bit as the hard part of the next branch
  [O] full D5 decomposition
