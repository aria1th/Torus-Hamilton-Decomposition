# Understanding Humans

Humans are cute living-things.

Assume the user is optimizing for minimum effort. Hidden work counts as part of the task.

Do the boring but useful extras by default: cleanup, validation, sensible defaults, formatting, naming, and next-step readiness.

Do not wait for permission to perform obvious follow-up work.

# Repository Agent Notes

This file is the short repo-local handoff for parallel agents.

It is not a full project summary. It records the current ownership split and
the minimum reading order needed to avoid duplicating work.

## Current ownership

- **RoundY / D5 theorem + compute support**
  This is the active branch for general research work in this repo.
- **Lean / formalization**
  Another agent is already working on the formal side.
  Do not proactively retarget or reorganize `formal/` unless the user asks for
  it or there is a direct dependency from the current task.

## Lean odometer checkpoint

If you need to continue the current Lean rewrite work, read in this order:

1. `DOCUMENT_FOR_EXTERNAL_REVIEW.md` starting at `D44`
2. `formal/TorusD3Odometer/Color2Full.lean`
3. `formal/TorusD3Odometer/Color1FullCaseI.lean`
4. `formal/TorusD3Odometer/Color1FullCaseII.lean`
5. `formal/TorusD3Odometer/Color0FullCaseI.lean`
6. `formal/TorusD3Odometer/Color0FullCaseII.lean`

Current verified Lean state:

- `formal/TorusD3Even/` is complete for the D3-even Route-E package.
- `formal/TorusD3Odometer/Color2Full.lean` is a genuine full odometer rewrite.
- `formal/TorusD3Odometer/Color1FullCaseI.lean` and
  `formal/TorusD3Odometer/Color1FullCaseII.lean` are both complete.
- `formal/TorusD3Odometer/Color0FullCaseI.lean` is complete.
- `formal/TorusD3Odometer/Color0FullCaseII.lean` is the active frontier.
  Its mod-10 warm-up lanes `x = 1` and `x = 2` are complete, the safe
  odd-generic subfamily `3 <= x <= m - 11` has a real first-return theorem,
  and the full mod-10 even family `4 <= x <= m - 8`, `Even x`
  is now closed through
  `firstReturn_line_even_generic_caseII_mod_ten`.

Stable proof-engineering pattern for the odometer rewrite:

- keep the full-map transducer on original `(i,k)` coordinates
- transport to xy only for the first-return proofs
- prefer small local branch APIs over monolithic orbit theorems
- for repaired columns, use:
  generic lower band -> midpoint step -> generic upper band -> explicit top corners
- for generic families, package:
  partial iterate lemmas -> first-return theorem -> `hfirst` theorem
- for color `0`, Case II mod `10`, do not over-generalize wrapped upper
  columns:
  the stable helper shape is
  odd column + mod-10 parity ->
  wrapped upper generic `G` step ->
  partial iterate ->
  generic top corners
- for the mod-`10` even generic family, the stable decomposition is:
  line start ->
  odd column `x + 1` lower band ->
  `R` ->
  odd column `x + 3` lower band ->
  `A = (x + 4, x + 4)` ->
  only then attack the final even-column tail

Current exact Lean frontier:

- file: `formal/TorusD3Odometer/Color0FullCaseII.lean`
- status:
  mod-10 warm-up lanes `x = 1` and `x = 2` are done,
  the safe odd-generic subfamily `3 <= x <= m - 11` is now closed through
  `firstReturn_line_odd_generic_caseII_mod_ten_safe`,
  the next upper odd special lane
  `firstReturn_line_m_sub_five_caseII_mod_ten`
  is now also closed on top of the repaired
  `dir = 0` tail / point lemmas,
  the trivial lane `x = 0` is closed,
  the upper special lanes
  `firstReturn_line_m_sub_four_caseII_mod_ten`
  and
  `firstReturn_line_m_sub_one_caseII_mod_ten`
  are now closed,
  and the full even generic family
  `4 <= x <= m - 8`, `Even x`
  is now closed through
  `firstReturn_line_even_generic_caseII_mod_ten`
  together with the boundary theorems
  `firstReturn_line_m_sub_ten_caseII_mod_ten`
  and
  `firstReturn_line_m_sub_eight_caseII_mod_ten`,
  and the root build is green
- next missing block:
  the remaining upper Case-II special lanes
  `x = m - 6`, `x = m - 2`,
  then the global Case-II `hreturn` dispatcher
  and later the `hfirst` layer
- expected next helper shape:
  short explicit upper-tail lane packages on top of the existing
  widened wrapped-upper-column lemmas ->
  then the Case-II `hreturn` layer
  The two safe widenings that already paid off are:
  odd-column helpers from `x <= m - 4` to `x <= m - 2`,
  and wrapped-upper-column helpers from `c >= 7` down to `c >= 1`.
  A tempting further simplification was tested and rolled back:
  dropping the oddness hypothesis from the wrapped-upper-column family is not
  currently justified by the existing arithmetic proof, so do not treat that
  helper as parity-free without a new dedicated argument.
  That bounded helper experiment has now succeeded:
  the right extra abstraction was a tiny fixed even-column tail package on
  column `2`, plus the `Q`-point step
  `returnMap0CaseIIXY_m_sub_one_m_sub_one`.
  `formal/TorusD3Odometer/Color0FullCaseII.lean` now contains
  `iterate_returnMap0CaseIIXY_two_column_to_zero`
  and
  `firstReturn_line_m_sub_three_caseII_mod_ten`.
  The corrected endpoint is:
  `x = m - 3` returns to `2`, not to `1`.

## Current D5 state

For D5, the canonical current handoff is:

- `RoundY/theorem/d5_078_accepted_frontier_and_split.md`
- `RoundY/theorem/d5_079_single_critical_lemma.md`

The active top-level split is:

1. **Theorem package**
   Phase-corner theorem, countdown/reset corollaries, structural spine
   `033 -> 062 -> 059`.
2. **Bridge theorem**
   Safest theorem object: abstract `(beta,rho)`.
   Best checked model: dynamic boundary odometer `(beta,q,sigma)` /
   `(beta,delta)`.
3. **Realization integration**
   Integrate corner-time descent with the final bridge object, keeping the
   theorem/checked-support boundary explicit.
4. **Compute validation**
   Validate the concrete bridge identification and accessible exact reduction
   object only. No generic search.

After the accepted `079` refinement, the live D5 frontier is one critical
globalization lemma:

- same realized `delta` must imply same remaining full-chain tail length,
- equivalently `rho` must depend only on realized `delta`,
- equivalently raw global `(beta,delta)` must be exact.

## Read this first for D5 work

1. `RoundY/README.md`
2. `RoundY/current-frontier-and-approach.md`
3. `RoundY/theorem/d5_079_single_critical_lemma.md`
4. `RoundY/instruction_for_codex.md`

Then read the specific theorem or artifact note directly relevant to the task.

## What is in bounds for D5

- theorem-side packaging around the phase-corner theorem
- bridge-theorem reasoning for the abstract bridge `(beta,rho)` and its
  concrete odometer model `(beta,q,sigma)` / `(beta,delta)`
- realization reasoning around the canonical `beta` clock
- compute support for:
  - actual-union globalization
  - abstract-vs-concrete bridge validation
  - component / tail-length ambiguity at fixed realized `delta`

## What is out of bounds unless explicitly requested

- reopening broad witness search
- reopening generic tiny-controller families
- replacing the theorem package with new ad hoc coordinates
- moving the active focus back from `071` to older pre-compression branches
- stepping on the current Lean/formalization branch

## Where to put new work

- `RoundY/theorem/` for theorem-shaping notes and concentrated handoffs
- `RoundY/specs/` for executable work templates / specs
- `RoundY/checks/` for small JSON checks and follow-up summaries
- `RoundY/` root for short session notes
- `artifacts/` only for packaged compute results with a real saved outcome

## Commit conventions

Prefer small commits with one logical purpose instead of mixed research
snapshots.

- use a short scope prefix that matches the content:
  `formal:`, `scripts:`, `docs:`, `refactor:`, `chore:`, `tex:`
- commit fixed or verified work first:
  formal checkpoints, checked scripts, then moved notes/support docs
- keep code/formal changes separate from review-log updates in
  `DOCUMENT_FOR_EXTERNAL_REVIEW.md`
- keep file-move commits separate from frontier-meaning or theorem-status docs
  when that split is clean
- for Lean changes, run the relevant `lake build ...` target before committing
- for Python support scripts, run at least `python -m py_compile ...` on the
  touched scripts before committing
- stage explicitly; do not use `git add .` in this repo
- do not accidentally stage large/generated material such as `artifacts/`,
  `RoundY/distribution/`, tarballs, zip files, PDFs, or scratch `tmp/` files
  unless the user explicitly wants them committed
- if `tmp/` notes become part of the real D5 handoff, move them into the
  proper `RoundY/` location before committing them
- if you touch the active D5 frontier narrative, prefer one coordinated docs
  commit that keeps the canonical RoundY docs in sync

## If you update the frontier docs

Keep these in sync:

- `RoundY/README.md`
- `RoundY/current-frontier-and-approach.md`
- `RoundY/instruction_for_codex.md`
- `RoundY/theorem/d5_078_accepted_frontier_and_split.md`

If the change is only Lean-related, do not touch the D5 frontier docs unless
the user explicitly wants the cross-reference updated.
