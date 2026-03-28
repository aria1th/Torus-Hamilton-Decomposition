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

- `RoundY/README.md`
- `RoundY/current-frontier-and-approach.md`
- `RoundY/theorem/d5_284_current_working_frontier_after_nonresonant_closure.md`
- `RoundY/tex/d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex`
- `RoundY/theorem/d5_285_residual_assembly_companion_memo.md`
- `RoundY/tex/d5_285_residual_assembly_companion_after_nonresonant_closure.tex`
- `RoundY/theorem/d5_286_promoted_collar_complete_local_dynamics.md`

The active top-level split is:

1. **Theorem package**
   The accepted odd-`m` globalization package remains closed.
   The stable background is still `076–099`, with `082/099/106/121/122` the
   shortest theorem-side references.
2. **Promoted manuscript layer**
   The front-end one-corner slice `T0--T4` is closed.
   The graph-side color-`4` and color-`3` branches are closed.
   The current manuscript-order working packet is `284/285/286`.
3. **Current live frontier**
   The branch now treats:
   - small odd residual packets as closed working blocks;
   - the nonresonant residual packet for odd `m >= 11` with `3 ∤ m` as closed
     at working-theorem level;
   - and the remaining burden as a resonant residual program for odd
     `m >= 15` with `3 | m`.
- the current assumption audit is in
  `RoundY/theorem/d5_290_current_assumption_and_gap_audit.md`;
- the current residual compute campaign split is in
  `RoundY/theorem/d5_291_residual_compute_campaign_conclusion.md`;
- the reusable request/manifest template is in
  `RoundY/specs/d5_292_residual_compute_request_template.md`.
- the current tar-alignment / explicit-family narrowing is in
  `RoundY/theorem/d5_294_residual_package_alignment_after_tar.md`;
- the current promoted-collar follow-up probe is in
  `RoundY/theorem/d5_295_promoted_collar_dualA_vs_singleB_probe.md`.
- the current row-3 / visible-grid direction synthesis is in
  `RoundY/theorem/d5_296_resonant_row3_direction_after_visible_grid.md`.
- the current late 2-line zero-return atlas is in
  `RoundY/theorem/d5_297_resonant_late_zero_return_atlas.md`.
- the integrated late routing/campaign note is in
  `RoundY/theorem/d5_298_resonant_late_mod30_routing_note.md`.
- the first executed late exact-promotion note is in
  `RoundY/theorem/d5_299_resonant_late_first_exact_promotions.md`.
- the new master `H_m` hinge-profile theorem is in
  `RoundY/theorem/d5_300_resonant_Hm_master_hinge_profile_theorem.md`.
- the resulting resonant pure color-`1` proof-state synthesis is in
  `RoundY/theorem/d5_301_resonant_pure_color1_proof_state_after_Hm_master_profile.md`.
- the short theorem-order map of that promoted resonant stack is in
  `RoundY/theorem/d5_302_resonant_pure_color1_core_chain.md`.
- the short global D5 status overview is in
  `RoundY/theorem/d5_303_current_d5_proof_status_overview.md`.
- the short whole-branch status note after promoting the parallel existence
  layer is in
  `RoundY/theorem/d5_305_current_d5_status_with_routey_existence.md`.
- the parallel existence/seam-surgery layer extracted from the March 28
  support archive is now in `RouteY-Existence/README.md`; treat it as a
  parallel arithmetic/existence lane, not as a replacement for the canonical
  current RoundY frontier.
4. **Independent work**
   Documentation, internalization, literal definitions, citation cleanup,
   bundle cleanup, and manuscript readability work can proceed without waiting
   for the final resonant theorem phrasing to settle.

The live task is no longer broad five-color search.
It is:

- keep the `284/285/286` layer readable and authoritative;
- isolate the remaining resonant residual input cleanly;
- and keep the independence/documentation queue moving in parallel.

## Read this first for D5 work

1. `RoundY/README.md`
2. `RoundY/current-frontier-and-approach.md`
3. `RoundY/theorem/d5_284_current_working_frontier_after_nonresonant_closure.md`
4. `RoundY/tex/d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex`
5. `RoundY/theorem/d5_285_residual_assembly_companion_memo.md`
6. `RoundY/tex/d5_285_residual_assembly_companion_after_nonresonant_closure.tex`
7. `RoundY/theorem/d5_286_promoted_collar_complete_local_dynamics.md`
8. `RoundY/instruction_for_codex.md`
9. `RoundY/theorem/d5_290_current_assumption_and_gap_audit.md`
10. `RoundY/theorem/d5_291_residual_compute_campaign_conclusion.md`
11. `RoundY/specs/d5_292_residual_compute_request_template.md`
12. `RoundY/theorem/d5_294_residual_package_alignment_after_tar.md`
13. `RoundY/theorem/d5_295_promoted_collar_dualA_vs_singleB_probe.md`
14. `RoundY/theorem/d5_296_resonant_row3_direction_after_visible_grid.md`
15. `RoundY/theorem/d5_297_resonant_late_zero_return_atlas.md`
16. `RoundY/theorem/d5_298_resonant_late_mod30_routing_note.md`
17. `RoundY/theorem/d5_299_resonant_late_first_exact_promotions.md`
18. `RoundY/theorem/d5_300_resonant_Hm_master_hinge_profile_theorem.md`
19. `RoundY/theorem/d5_301_resonant_pure_color1_proof_state_after_Hm_master_profile.md`
20. `RoundY/theorem/d5_302_resonant_pure_color1_core_chain.md`
21. `RoundY/theorem/d5_303_current_d5_proof_status_overview.md`
22. `RoundY/theorem/d5_304_routey_existence_parallel_layer.md`
23. `RoundY/theorem/d5_305_current_d5_status_with_routey_existence.md`
24. `RouteY-Existence/README.md`

Then read the specific theorem or artifact note directly relevant to the task.

## What is in bounds for D5

- theorem-side packaging around the accepted odd-`m` globalization package
- manuscript-order packaging around the current `284/285/286` layer
- resonant residual reasoning in the current width-`1` / width-`3` /
  promoted-collar / double-top / `B`-active-gate language
- documentation, internalization, and promotion work for the current frontier
- compute support for:
  - exact packet replay
  - residual-branch validation
  - reader-facing bundle / memo cleanup

## What is out of bounds unless explicitly requested

- reopening broad witness search
- reopening generic tiny-controller families
- reverting the top-level read back to a generic all-odd five-color assembly
  search without explicit new evidence
- replacing the accepted theorem package with new ad hoc coordinates
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
