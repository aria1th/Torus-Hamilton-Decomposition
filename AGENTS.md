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

Stable proof-engineering pattern for the odometer rewrite:

- keep the full-map transducer on original `(i,k)` coordinates
- transport to xy only for the first-return proofs
- prefer small local branch APIs over monolithic orbit theorems
- for repaired columns, use:
  generic lower band -> midpoint step -> generic upper band -> explicit top corners
- for generic families, package:
  partial iterate lemmas -> first-return theorem -> `hfirst` theorem

Current exact Lean frontier:

- file: `formal/TorusD3Odometer/Color0FullCaseII.lean`
- status:
  mod-10 warm-up lanes `x = 1` and `x = 2` are done,
  the odd generic band now has a clean prefix/middle layer through the `R` step,
  and the root build is green
- next missing block:
  the post-`R` wrapped upper-column tail on column `x + 4`
- expected next helper shape:
  wrapped upper-column generic `G` step ->
  wrapped upper-column partial iterate package ->
  explicit top-corner lemmas only if the boundary lane forces them

## Current D5 state

For D5, the canonical current handoff is:

- `RoundY/theorem/d5_067_concentrated_handoff.md`

The active top-level split is:

1. **Theorem package**
   Phase-corner theorem, countdown/reset corollaries, structural spine
   `033 -> 062 -> 059`.
2. **Clock route**
   The canonical `beta` clock, viewed as:
   - lifted-clock descent / realization
   - exact-clock rigidity / necessity
3. **Compute support**
   Validate the exact reduction object and exact reduction data only.
   No generic search.

## Read this first for D5 work

1. `RoundY/README.md`
2. `RoundY/current-frontier-and-approach.md`
3. `RoundY/theorem/d5_067_concentrated_handoff.md`
4. `RoundY/instruction_for_codex.md`

Then read the specific theorem or artifact note directly relevant to the task.

## What is in bounds for D5

- theorem-side packaging around the phase-corner theorem
- clock-route reasoning around the canonical `beta` clock
- compute support for:
  - cycle vs chain
  - accessible quotient
  - `(B,beta)` exactness / drift on larger moduli

## What is out of bounds unless explicitly requested

- reopening broad witness search
- reopening generic tiny-controller families
- replacing the theorem package with new ad hoc coordinates
- moving the active focus back from `067` to older pre-compression branches
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
- `RoundY/theorem/d5_067_concentrated_handoff.md`

If the change is only Lean-related, do not touch the D5 frontier docs unless
the user explicitly wants the cross-reference updated.
