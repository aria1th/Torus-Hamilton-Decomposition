# D5 094 Remaining tmp Priority Map

This note records which `tmp/` files still matter after the `251` bundle
promotion.

The point is to separate:

- material that has now been promoted;
- material that still matters as live provenance or auxiliary support;
- and material that should stay outside the stable RoundY theorem chain.

## 0. Current active tmp frontier

There is no longer a live theorem frontier inside the promoted
`T0--T4, G1, G2` slice.

The `251` bundle has now been promoted into stable RoundY locations, so the old
“current tmp frontier” language for `116–118` is no longer the right top-level
description.

The actual remaining non-stable work is not a single tmp theorem note. It is
the manuscript-side treatment of:

- the post-entry odometer packet;
- the final graph-side/globalization packet;
- and, after the later `255` honesty review, the explicit graph-side transport
  compatibility step linking the concrete `G1` package to abstract `G2`.

So the current tmp role is mostly auxiliary/provenance, not primary theorem
status.

Historical update:
the later `0326` memo layer is no longer `tmp`-only. Its current stable
promotions are:

- `tex/d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex`
- `theorem/d5_284_current_working_frontier_after_nonresonant_closure.md`
- `tex/d5_285_residual_assembly_companion_after_nonresonant_closure.tex`
- `theorem/d5_285_residual_assembly_companion_memo.md`
- `theorem/d5_286_promoted_collar_complete_local_dynamics.md`
- `tex/d5_286_promoted_collar_complete_local_dynamics.tex`

These should now be cited first when discussing the current residual frontier.

## 1. Newly promoted from tmp/bundled material

The following late tmp/bundled material is now promoted and should be cited in
its stable RoundY location instead:

- the `251` bundle front-end notes `220`, `223`, `225`, `228`, `229`, `230`,
  `233`
- the `251` bundle graph-side notes `234`, `236`, `240`, `243`, `245`, `247`
- the bundle status/overview notes `249`, `251`
- the refined manuscript and refined overview under `RoundY/tex/`
- the matching scripts and saved checks now under `scripts/` and
  `RoundY/checks/`
- the earlier `121/122` M5 notes, already promoted in the previous pass

## 2. Still useful tmp provenance / auxiliary support

These files are still useful, but they are no longer the main canonical entry
point.

- `tmp/d5_123_odd_m_d5_consolidated_manuscript.tex`
  Importance: `high`
  Role:
  Earlier large conditional manuscript integrating the `M1--M6` language.
  Useful for provenance and for understanding the imported-block boundary, but
  superseded as the main stable manuscript by the promoted `251` TeX files.

- `tmp/d5_124_M1_M6_proof_closure_draft.tex`
  Importance: `medium`
  Role:
  Bookkeeping draft for what was open versus closed in the `M1--M6` split.

- `tmp/d5_125_corrected_M2_M3_anchor_package_note.tex`
  Importance: `medium`
  Role:
  Odometer-side anchor package support for the front-end / quotient story.

- `tmp/d5_126_intended_quotient_verification_note.tex`
  Importance: `medium`
  Role:
  Theorem-side verification note for the intended quotient and local
  provenance questions.

- `tmp/d5_255_from_d5_254_transport_honesty.patch.diff`
  Importance: `low`
  Role:
  Review provenance for the final honesty tightening from the `254`
  packet-closure manuscript to the transport-conditional `255` copy.

- `tmp/d5_133_one_corner_front_end_reduction_note (2).tex`
  Importance: `medium`
  Role:
  One-corner/front-end reduction support relevant to the odometer-side import.

- `tmp/d5_134_shape_theorem_and_odometer_roadmap (1).md`
- `tmp/d5_134_shape_theorem_and_odometer_roadmap (2).md`
- `tmp/d5_135_seed_certificate_table (1).md`
- `tmp/d5_136_shape_theorem_compute_attempt_and_job_request.md`
  Importance: `medium`
  Role:
  Shape-theorem / certificate / odometer-roadmap support that may still matter
  when internalizing the imported odometer packet.

- `tmp/d5_195_sigma23_case_report.md`
- `tmp/d5_196_sigma23_R1_microstate_compute_request.md`
  Importance: `medium`
  Role:
  Late local microstate provenance support behind the surfaced front-end notes.

These should be used as support or provenance, not as the first citation when a
stable RoundY note now exists.

## 3. Stable note already exists; tmp should not be cited first

For the following material, cite the stable RoundY note first:

- all promoted `076–083` notes
- the compact cleanup/reproof line `091–099`
- the quotient/manuscript bridge line `106`, `121`, `122`
- the honesty-boundary / independence line `255`, `256`
- the promoted `251` slice `220`, `223`, `225`, `228`, `229`, `230`, `233`,
  `234`, `236`, `240`, `243`, `245`, `247`, `249`, `251`

## 4. Outside the RoundY D5 theorem chain

These should stay outside the stable RoundY D5 theorem chain unless the user
explicitly requests a separate promotion:

- scratch Lean/test files in `tmp/scratches/`
- unrelated general Hamilton-lift notes such as
  `tmp/scratches/square_product_hamilton_lift.tex`
- old bundle patch diffs kept only as provenance of manuscript editing

## 5. Recommended citation rule

Use this rule:

1. cite the stable RoundY theorem/check/tex copy first;
2. cite a `tmp/` file only if provenance or an unpromoted auxiliary argument
   matters;
3. do not mix a stable promoted theorem chain with stale tmp citations unless
   the stable note explicitly says the argument still lives only in tmp.
