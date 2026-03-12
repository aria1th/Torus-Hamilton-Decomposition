Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch after the unresolved best-seed
channel has been extracted as a corridor-phase problem, but with one open
question about whether the saved `034` phase coordinates are already the true
long-run normal form.

Current target:
Clarify the `034` phase convention and decide whether:
- `(s, layer)` is a true deterministic factor of the full long corridor, or
- one more reduced coordinate is already forced by the data.

Known assumptions:
- `032` fixes the best endpoint seed `[2,2,1] / [1,4,4]`.
- `033` reduces the best-seed obstruction to the unresolved `R1 -> H_L1`
  corridor.
- `034` extracts a source-normalized first-pass projected rule on `(a, layer)`,
  where `a = s - rho` and `rho = u_source + 1`.
- `035` prunes the first raw static phase-gate layer built on top of that
  projected phase picture.

Attempt A:
  Idea:
  Compare the saved `034` first-pass phase data against the actual long corridor
  traces, and check whether the first repeated projected phase still has the
  same successor.
  What works:
  The reader’s flagged mismatch is real.
  For every checked `m = 5,7,9,11`, the `034` first-pass rule is correct until
  the first repeated projected phase.
  But after one projected lap:
  - the same `(s, layer)` reappears,
  - and its next projected phase changes.
  So `(s, layer)` is not a deterministic factor of the full long corridor.
  That is exactly why `first_exit_phase` and `phase_residue_mod_period` do not
  name the same state.
  Where it fails:
  This kills the naive interpretation of `034` as the final long-run normal
  form. It does not yet say what the correct lifted model is.

Attempt B:
  Idea:
  Search for the smallest exact lifted corridor state visible in the traced data.
  What works:
  One more reduced coordinate is enough in the traced range.
  After normalizing by
  - `rho = u_source + 1`
  - `a = s - rho mod m`
  the long corridor follows an exact deterministic rule on `(q, a, layer)` up
  to the first `H_L1`-legal exit for every checked source family and every
  checked `m = 5,7,9,11`.
  The verified lifted rule is:
  - `(q,a,0) -> (q+1, a, 1)`
  - `(q,a,1) -> (q, a+1, 2)`
  - `(q,a,2) -> (q, a+1, 3)` if `q = m-1`
  - `(q,a,2) -> (q, a, 3)` if `q != m-1`
  - otherwise `(q,a,layer) -> (q, a, layer+1 mod m)`
  The entry and first exits also become clean:
  - entry lift: `(m-1, 0, 2)`
  - regular first exit: `(m-1, m-4, 1)` via direction `[2]`
  - exceptional first exit: `(m-2, m-4, 1)` via direction `[1]`
  Where it fails:
  This is a traced-lift model up to first exit, not yet a full theorem for the
  entire infinite branch or a local realization.

Candidate lemmas:
- [C] The saved `034` phase rule is only a first-pass projected phase lap.
- [C] `(s, layer)` is not a deterministic factor of the full long corridor.
- [C] The first repeated projected phase already has a different projected
  successor.
- [C] The traced long corridor admits an exact deterministic lift on
  `(q, a, layer)` up to first exit.
- [C] The lifted entry and first-exit formulas are uniform across
  `m = 5,7,9,11`.
- [H] The next local branch should be designed against the lifted model, not
  against `(s, layer)` alone.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- stop treating `(s, layer)` as the final long-run phase state
- use the lifted `(q, a, layer)` model in the next local-mechanism branch
- pack runnable scripts and raw traces for external readers so they can audit
  and extend `032–036` directly

Next branching options:
1. Main branch:
   a local mechanism that can read or carry the lifted corridor state,
   especially the `q`-controlled layer-2 event.
2. Secondary branch:
   a theorem/no-go pass showing why `(s, layer)`-only mechanisms cannot resolve
   the corridor.
3. Only then:
   reopen local synthesis on a lift-aware alphabet.

Claim status labels:
  [P] `019`, `025`
  [C] `032`, `033`, `034`, `035`, `036`
  [H] the next live target is the lifted corridor state, not `(s, layer)` alone
  [F] interpreting `034` as the final long-run phase normal form
  [O] full D5 decomposition
