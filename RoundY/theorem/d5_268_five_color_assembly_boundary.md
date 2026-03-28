# D5 268 Five-Color Assembly Boundary

This note records the honest proof boundary after the `257–266` Route-E closure
line and the manuscript rewrite in
[d5_267_full_d5_working_manuscript_routee_honest.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/tex/d5_267_full_d5_working_manuscript_routee_honest.tex).

Historical update:
the later `0326` working memo promotion
[d5_284_current_working_frontier_after_nonresonant_closure.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_284_current_working_frontier_after_nonresonant_closure.md)
now supersedes this note as the canonical top-level frontier description.
The present note remains the right stable record of the earlier,
broader “five-color assembly boundary” stage and of the `267–281` narrowing
ladder that led to the later resonant-residual split.

## Executive status

The current odd-`m`, `d=5` manuscript is now independently readable in the
following precise sense:

- the front-end theorem block `T0--T4` is stated and closed in one place;
- the post-entry odometer spine is stated explicitly;
- the theorem-side anchor/globalization packets `M23` and `M6` are stated
  explicitly;
- the corrected selector `SelCorr`, the surgery selector `SelStar`, and the
  theorem-side quotient `Q_th` are now written literally inside the manuscript
  appendix;
- the color-`4` Sel* branch is closed;
- the color-`3` Sel* Route-E branch is closed.

What is **not** yet closed is one remaining graph-side theorem:

> a five-color assembly theorem that inserts the closed color-`3` and
> color-`4` branches into a full five-color Hamilton selector package.

So the `267`-stage main theorem is honest and conditional on that single
remaining input. For the later narrower current frontier after small odd and
nonresonant closure, use `284/285/286` instead.

## What exactly is already closed

Closed theorem blocks:

- `T0`: actual-needed tiny-repair core
- `T1`: strip closure via the surfaced `sigma23` / `sigma32` arguments
- `T2`: centered-core obstruction
- `T3`: repeated-end obstruction
- `T4`: canonical entry / one-corner reduction
- post-entry exact odometer spine
- `M23`: theorem-side anchor package
- `M4`: corrected-selector baseline theorem
- `M5-color4`: Sel* color-`4` Hamilton theorem
- `M5-color3`: Sel* color-`3` Route-E Hamilton theorem
- `M6`: odd-`m` globalization theorem

Sharp obstruction already known inside the current Sel* package:

- [d5_269_selstar_color12_return_invariant_obstruction.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_269_selstar_color12_return_invariant_obstruction.md)
  shows that the current Sel* colors `1` and `2` preserve simple first-return
  invariants on `P0`, so they cannot themselves be the missing Hamilton colors.
- [d5_270_five_color_slice_ordering_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_270_five_color_slice_ordering_no_go.md)
  rules out the smallest slice-class-only completion family.
- [d5_271_five_color_coarse_defect_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_271_five_color_coarse_defect_no_go.md)
  then rules out the next historical coarse family that still uses the old
  slice-`2` old bit and slice-`3` predecessor flag from the `245/247` splice
  picture.

Historical but no longer active as the final route:

- `G1`: explicit two-swap splice package
- `G2`: abstract cyclic transport theorem

The reason these are only historical is the `256` no-go result: the explicit
`G1` package is not the right concrete package on which to apply the old cyclic
transport story.

## What the remaining theorem must say

The remaining graph-side theorem should be formulated as a package-level
statement on the full torus.

The clean honest form is:

1. There exist five torus permutations `h_0,...,h_4`.
2. Their arc sets are pairwise disjoint and cover the full directed arc set.
3. `h_3` is the already closed Sel* color-`3` map.
4. `h_4` is the already closed Sel* color-`4` map.
5. The remaining maps `h_0,h_1,h_2` are Hamilton.

This is exactly the manuscript background input
`five-color assembly`.

By the obstruction note `269`, this remaining theorem should not be read as
“prove the other Sel* colors Hamilton.” It must genuinely replace at least the
current Sel* colors `1` and `2`.
By `270` and `271`, it must also use finer local data than either:

- a slice-class-only completion rule, or
- the historical defect-bit coarse class family from the old `245/247` route.

The next simplification is now explicit in
[d5_274_routee_assembly_pattern_search.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_274_routee_assembly_pattern_search.md):
the simple family `S2(A2) + S3(1 in A3)` already compresses local exactness to
a finite pattern CSP and produces near-assembly solutions with three or four
Hamilton colors on the checked range. The follow-up probe
[d5_275_routee_color2_residual_probe.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_275_routee_color2_residual_probe.md)
then shows that, inside the combined best `274` family, color `2` is the
cleanest residual Route-E target. The next note
[d5_276_routee_color2_short_cycle_structure.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_276_routee_color2_short_cycle_structure.md)
then isolates its explicit affine short-cycle families, and
[d5_277_routee_refined_family_search.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_277_routee_refined_family_search.md)
shows that feeding those markers back into the finite exactness CSP already
repairs checked color `2` on `m=7,9`. The gate note
[d5_278_routee_refined_family_large_odd_gate.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_278_routee_refined_family_large_odd_gate.md)
then shows that one further local exactness distinction is still missing.
So the live theorem should now be read as:

- finite exactness in that compressed family,
- then one or two defect-marker refinements of it,
- then the `279` one-point repair that closes checked color `2`,
- and then a residual color-`1/0` refinement beyond the raw `280` line
  relation, since `281` shows that the line bit alone is still not enough to
  close the full five-color package.

## Why this is a real remaining theorem

The remaining issue is not just exposition.

The current concrete historical package `g_0,...,g_4` from `247` is a valid
colorwise selector package, but that by itself does **not** imply that the
non-color-`4` maps are Hamilton.
The old `G1 -> G2` transport route was supposed to provide that implication,
and `256` shows that route is not available for the present concrete package.

So after `266`, the proof boundary is sharper, not vacuous:

- one transport theorem disappeared;
- one actual color-`3` Hamilton theorem was added;
- one checked color-`2` repaired-family closure was added;
- one explicit residual color-`1` affine line obstruction was added;
- but one five-color assembly theorem still remains.

## What can proceed independently

The following independence/internalization tasks can proceed without waiting for
the remaining five-color assembly theorem:

- line-level cleanup of the top-level manuscript
- literal object definitions and notation cleanup
- packet-proof appendix cleanup
- stable citation cleanup away from `tmp/`
- certificate appendix planning
- reader-facing documentation and bundle cleanup

These are the tasks queued in
[d5_256_independence_internalization_queue.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_256_independence_internalization_queue.md),
but they should now be read with the present honesty boundary in mind.

## Bottom line

The odd-`m`, `d=5` proof chain is now in the following state:

- almost all theorem packets that the manuscript needs are explicit and closed;
- the manuscript itself is readable as a paper-form theorem-order document;
- the final unproved content is concentrated in one explicit graph-side input,
  namely the five-color assembly theorem;
- and the current best concrete handoff into that theorem is the
  `274–281` chain: compressed exactness family, explicit color-`2`
  short-cycle structure, a first defect-marker refinement, the `279`
  one-point repair that closes checked color `2`, and then the `280–281`
  evidence that the remaining color-`1` obstruction is an explicit affine line
  family but that the raw line bit alone still does not finish the assembly.
