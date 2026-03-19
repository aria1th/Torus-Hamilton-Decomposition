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
7. `formal/TorusD3Even/Color0.lean` if you need the mod-`4` color-`0`
   Case-II splice source

Current verified Lean state:

- `formal/TorusD3Even/` is complete for the D3-even Route-E package.
- `m = 3` does not need a separate reproof in the current formal split:
  it is already covered by
  `formal/TorusD3Odd/FullCycles.lean`
  through the odd-branch theorems
  `hasCycle_pairColorMap`,
  `hasCycle_colorMap`,
  and
  `all_colors_haveCycle`
  under `[Fact (Odd m)] [Fact (2 < m)]`.
- `formal/TorusD3Odometer/Color2Full.lean` is a genuine full odometer rewrite.
- `formal/TorusD3Odometer/Color1FullCaseI.lean` and
  `formal/TorusD3Odometer/Color1FullCaseII.lean` are both complete.
- `formal/TorusD3Odometer/Color0FullCaseI.lean` is complete.
- `formal/TorusD3Odometer/Color0FullCaseII.lean` closes the full
  color-`0`, Case-II, mod-`10` odometer rewrite through
  `hreturn_line_case0_caseII_mod_ten`,
  `hfirst_line_case0_caseII_mod_ten`,
  `cycleOn_returnMap0CaseII_caseII_mod_ten`,
  and
  `cycleOn_fullMap0CaseII_caseII_mod_ten`.
- `formal/TorusD3Odometer/Color0FullCaseIIModFour.lean` now closes the full
  color-`0`, Case-II, mod-`4` odometer rewrite through
  `hreturn_line_case0_caseII_mod_four`,
  `hfirst_line_case0_caseII_mod_four`,
  `cycleOn_returnMap0CaseII_caseII_mod_four`,
  and
  `cycleOn_fullMap0CaseII_caseII_mod_four`.
- The full current D3 odometer rewrite is therefore complete and the root
  target
  `lake build TorusD3Odometer`
  is green.
- Read that odometer tree as the completed D3-even presentation layer.
  It does not replace the pre-existing odd D3 closure; small odd cases such as
  `m = 3` remain on the odd branch.

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

- The proof content frontier is no longer a missing D3 odometer theorem.
- The current optional work is cleanup / presentation:
  - linter cleanup in `formal/TorusD3Odometer/`
  - possible consolidation of duplicated mod-`10` / mod-`4` helper layers
  - higher-level documentation of the completed odometer rewrite split
    (`Color2Full`, `Color1FullCaseI`, `Color1FullCaseII`,
    `Color0FullCaseI`, `Color0FullCaseII`, `Color0FullCaseIIModFour`)
- If a new proof task is needed, the next natural one is not another missing
  D3-even theorem but either cleanup or a new abstraction/refactor pass.

## Current D5 state

For D5, the canonical current handoff is:

- `RoundY/theorem/d5_082_frontier_and_theorem_map.md`
- `RoundY/theorem/d5_083_gluing_flow_and_final_theorem.md`
- `RoundY/theorem/d5_083_final_theorem_proof.md`
- `RoundY/theorem/d5_086_dependency_audit_and_generalization_gate.md`

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

After the promoted `083` proof, the odd-`m` D5 theorem closes inside the
accepted `076–082` package.

The live task is now a short dependency audit:

- recheck `033 -> 062`,
- recheck the `079` chart/interface usage,
- and only then treat D5 as the base for broader generalization.

## Read this first for D5 work

1. `RoundY/README.md`
2. `RoundY/current-frontier-and-approach.md`
3. `RoundY/theorem/d5_082_frontier_and_theorem_map.md`
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
