# D5 290 Current Assumption And Gap Audit

This note answers the practical question:

> in the current proof state, what is actually proved, what is imported as
> theorem-level background, what is only checked evidence, and what is still
> genuinely open?

The point is to prevent two different confusions:

- mistaking a theorem-order imported packet for an unproved gap;
- or mistaking a checked exact packet for a proved all-`m` theorem.

## 1. Short answer

For the current `d=5` manuscript layer, there is still **one genuine
load-bearing unproved input**:

- the resonant residual assembly input for odd `m >= 15` with `3 | m`.

Everything else falls into one of three weaker categories:

- already proved inside the current theorem package,
- imported as explicit theorem-level background from earlier promoted notes,
- or only checked exact packet / current frontier evidence.

## 2. What is already theorem-level closed

At the current theorem-order packaging level, the following are closed.

- the front-end slice `T0--T4`
- the theorem-side anchor/globalization spine
- the graph-side color-`4` branch
- the graph-side color-`3` Route-E branch
- the small odd residual packets `m = 5, 7, 9`
- the nonresonant residual theorem for odd `m >= 11` with `3 ∤ m`

This is the package-level meaning of the current top manuscript:
[d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/tex/d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex).

## 3. What is imported but still theorem-level

Some pieces are not reproved from first principles inside `284`, but they are
not current gaps. They are explicit theorem-level background objects.

The main examples are:

- the theorem-side anchor package `M23`
- the accepted odd-`m` globalization package
- the closed color-`3` and color-`4` graph-side branches

In other words, these are **imported background theorems**, not live frontier
assumptions.

So “not reproved in this exact file” should not be confused with
“not proved in the current project state.”

## 4. The genuine load-bearing remaining assumption

The current top theorem is still conditional.

The main theorem in
[d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/tex/d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex#L170)
explicitly assumes the remaining resonant residual assembly input.

The missing load-bearing object is
[fr:resonant-residual-assembly] in that manuscript, namely:

- for every odd `m >= 15` with `3 | m`, construct a selector package extending
  the frozen color-`3` / color-`4` backbone such that the remaining colors
  `0,1,2` are Hamilton.

This is the one theorem that is still genuinely open in the current D5 proof
line.

So the strongest honest current statement is:

- the D5 manuscript is still **conditional on the resonant residual theorem**.

## 5. What is only checked exact packet, not theorem

Several important pieces are currently exact checked packets rather than
all-`m` theorem-level closures.

From the companion ledger
[d5_285_residual_assembly_companion_after_nonresonant_closure.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/tex/d5_285_residual_assembly_companion_after_nonresonant_closure.tex#L532),
the main ones are:

- `51`-type reduction to the width-`1` pure color-`1` frontier
- `69`-type reduction to the width-`3` pure color-`1` frontier
- the `45` / `75` `B`-active / gate branch picture

These are very useful and often exact on the checked moduli, but they are not
yet theorem-level all-`m` statements.

The new promoted-collar base-section note
[d5_289_promoted_collar_base_section_reduction_and_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md)
also belongs partly in this category:

- the reduction to the induced map on `H_m = {c=0,d=0}` is the intended next
  theorem target;
- but the stronger observation that every checked cycle meets
  `B_m = {c=0,d=0,e=0}` is currently still checked evidence, not yet a uniform
  theorem.

So one should not silently promote `289` into a proved all-odd no-go theorem.
At present it is:

- a stable note with exact checked data and a clear next theorem target.

## 6. What is theorem-level but not yet load-bearing

Some current theorem-level statements are proved, but they are not themselves
the missing final step.

The main examples are:

- width-`1` pure color-`1` obstruction
- width-`3` exact collar correction
- width-`3` double-top obstruction
- promoted-collar local audit / finite active-burst theorem

These are important because they sharply localize the remaining resonant
problem.
But they do **not** by themselves close the main theorem.

So they should be read as:

- genuine proved local theorems,
- but still explanatory/intermediate rather than final.

## 7. D3 comparison

To avoid over-generalizing the D5 status:

- the current D3 upload-ready manuscript is not in the same situation.

For D3, the present upload-ready source is theorem-side complete, and the
ancillary scripts are explicitly verification aids rather than load-bearing
assumptions.

The current upload-ready source is
[d3torus_complete_m_ge_3_odometer_revision_v8_rewrite.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/arxiv_uploads/2026-03-25_cases/d3_review_candidates/v8_d3_only/d3torus_complete_m_ge_3_odometer_revision_v8_rewrite.tex).

So the “remaining assumption” language applies to the current D5 manuscript,
not to the current D3 paper.

## 8. Bottom line

At the present time:

- **D3**: theorem-side complete; remaining work is packaging / exposition /
  ancillary presentation.
- **D5**: one genuine load-bearing theorem still open, namely the resonant
  residual assembly theorem.

Inside D5, the clean current status split is:

- closed theorem package:
  front end, theorem-side anchor/globalization, color `3`, color `4`, small
  odd residual packets, nonresonant residual theorem;
- checked exact packet layer:
  `51`, `69`, `45`, `75`, and the stronger `289` base-subset behavior;
- genuine live frontier:
  the resonant residual theorem itself.

That is the most honest current reading of the project state.
