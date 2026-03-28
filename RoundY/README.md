# RoundY — d=5 Hamilton Decomposition

Hamilton decomposition of the directed `5`-torus

`D_5(m) = Cay((Z_m)^5, {e_0, e_1, e_2, e_3, e_4})`.

**Status:** the accepted odd-`m` globalization package remains closed, the
front-end one-corner slice `T0--T4` remains closed, and the graph-side
color-`4` and color-`3` branches remain closed.

**Current frontier:** the current `0326` working memo has now been promoted as
the stable RoundY frontier layer. The best current organizational read is no
longer “one generic five-color assembly theorem remains.” Instead, the branch
now treats the small odd residual packets as closed working blocks, treats the
nonresonant residual packet for odd `m >= 11` with `3 ∤ m` as closed at
working-theorem level, and isolates the remaining live burden as a much
narrower **resonant residual program** for odd `m >= 15` with `3 | m`. The
current top-level manuscript and companion are therefore the new `284/285`
documents, while `267–281` should now be read mainly as the narrowing ladder
that led to this split. The exact final theorem phrasing for the resonant input
is still being settled, so the present documentation is organized to make the
current packet structure and reading order explicit rather than to freeze the
final theorem statement too early.

**Parallel support layer:** the March 28 existence / seam-surgery archive is
now curated separately as
[../RouteY-Existence/README.md](../RouteY-Existence/README.md).
That layer is a parallel reading of the resonant residual problem, not a
replacement for the current RoundY proof frontier.

## Current entry points

Read these first:

1. [current-frontier-and-approach.md](./current-frontier-and-approach.md)
2. [theorem/d5_284_current_working_frontier_after_nonresonant_closure.md](./theorem/d5_284_current_working_frontier_after_nonresonant_closure.md)
3. [tex/d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex](./tex/d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex)
4. [theorem/d5_285_residual_assembly_companion_memo.md](./theorem/d5_285_residual_assembly_companion_memo.md)
5. [tex/d5_285_residual_assembly_companion_after_nonresonant_closure.tex](./tex/d5_285_residual_assembly_companion_after_nonresonant_closure.tex)
6. [theorem/d5_286_promoted_collar_complete_local_dynamics.md](./theorem/d5_286_promoted_collar_complete_local_dynamics.md)
7. [theorem/d5_282_backbone_defect_compression_methodology.md](./theorem/d5_282_backbone_defect_compression_methodology.md)
8. [theorem/d5_287_prime_cyclic_quotient_probe.md](./theorem/d5_287_prime_cyclic_quotient_probe.md)
9. [theorem/d5_288_next_closable_piece_priority.md](./theorem/d5_288_next_closable_piece_priority.md)
10. [theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md](./theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md)
11. [theorem/d5_290_current_assumption_and_gap_audit.md](./theorem/d5_290_current_assumption_and_gap_audit.md)
12. [theorem/d5_291_residual_compute_campaign_conclusion.md](./theorem/d5_291_residual_compute_campaign_conclusion.md)
13. [specs/d5_292_residual_compute_request_template.md](./specs/d5_292_residual_compute_request_template.md)
14. [theorem/d5_294_residual_package_alignment_after_tar.md](./theorem/d5_294_residual_package_alignment_after_tar.md)
15. [theorem/d5_295_promoted_collar_dualA_vs_singleB_probe.md](./theorem/d5_295_promoted_collar_dualA_vs_singleB_probe.md)
16. [theorem/d5_296_resonant_row3_direction_after_visible_grid.md](./theorem/d5_296_resonant_row3_direction_after_visible_grid.md)
17. [theorem/d5_297_resonant_late_zero_return_atlas.md](./theorem/d5_297_resonant_late_zero_return_atlas.md)
18. [theorem/d5_298_resonant_late_mod30_routing_note.md](./theorem/d5_298_resonant_late_mod30_routing_note.md)
19. [theorem/d5_299_resonant_late_first_exact_promotions.md](./theorem/d5_299_resonant_late_first_exact_promotions.md)
20. [theorem/d5_300_resonant_Hm_master_hinge_profile_theorem.md](./theorem/d5_300_resonant_Hm_master_hinge_profile_theorem.md)
21. [theorem/d5_301_resonant_pure_color1_proof_state_after_Hm_master_profile.md](./theorem/d5_301_resonant_pure_color1_proof_state_after_Hm_master_profile.md)
22. [theorem/d5_302_resonant_pure_color1_core_chain.md](./theorem/d5_302_resonant_pure_color1_core_chain.md)
23. [theorem/d5_303_current_d5_proof_status_overview.md](./theorem/d5_303_current_d5_proof_status_overview.md)
24. [theorem/d5_304_routey_existence_parallel_layer.md](./theorem/d5_304_routey_existence_parallel_layer.md)
25. [theorem/d5_305_current_d5_status_with_routey_existence.md](./theorem/d5_305_current_d5_status_with_routey_existence.md)
26. [../RouteY-Existence/README.md](../RouteY-Existence/README.md)
27. [theorem/d5_268_five_color_assembly_boundary.md](./theorem/d5_268_five_color_assembly_boundary.md)
28. [theorem/d5_256_independence_internalization_queue.md](./theorem/d5_256_independence_internalization_queue.md)
29. [theorem/d5_279_one_point_repair_color2_closure.md](./theorem/d5_279_one_point_repair_color2_closure.md)
30. [theorem/d5_280_one_point_repair_color1_line_obstruction.md](./theorem/d5_280_one_point_repair_color1_line_obstruction.md)
31. [theorem/d5_281_routee_line_bit_search.md](./theorem/d5_281_routee_line_bit_search.md)
32. [tex/d5_267_full_d5_working_manuscript_routee_honest.tex](./tex/d5_267_full_d5_working_manuscript_routee_honest.tex)
33. [theorem/d5_255_transport_honesty_boundary.md](./theorem/d5_255_transport_honesty_boundary.md)
34. [theorem/d5_082_frontier_and_theorem_map.md](./theorem/d5_082_frontier_and_theorem_map.md)
35. [theorem/d5_099_one_pass_odd_m_globalization_package.md](./theorem/d5_099_one_pass_odd_m_globalization_package.md)

For the accepted odd-`m` globalization package behind the manuscript-level
imports, the shortest stable references remain:

- [theorem/d5_082_frontier_and_theorem_map.md](./theorem/d5_082_frontier_and_theorem_map.md)
- [theorem/d5_083_gluing_flow_and_final_theorem.md](./theorem/d5_083_gluing_flow_and_final_theorem.md)
- [theorem/d5_083_final_theorem_proof.md](./theorem/d5_083_final_theorem_proof.md)
- [theorem/d5_099_one_pass_odd_m_globalization_package.md](./theorem/d5_099_one_pass_odd_m_globalization_package.md)

## Promoted 251 slice

The `251` bundle is no longer a `tmp`-only source. The following blocks are now
stable RoundY material.

### Front-end theorem block

- `T0` actual-needed core:
  [theorem/d5_230_T0_actual_needed_all_odd_surface_proof_note.tex](./theorem/d5_230_T0_actual_needed_all_odd_surface_proof_note.tex)
- `T1` strip closures:
  [theorem/d5_220_sigma23_source_surface_all_m_gt2_closure_note.tex](./theorem/d5_220_sigma23_source_surface_all_m_gt2_closure_note.tex),
  [theorem/d5_223_sigma32_surface_closure_note.tex](./theorem/d5_223_sigma32_surface_closure_note.tex)
- `T2` centered-core obstruction:
  [theorem/d5_228_T2_centered_core_obstruction_note.tex](./theorem/d5_228_T2_centered_core_obstruction_note.tex)
- `T3` four-collision obstruction:
  [theorem/d5_225_T3_four_collision_families_note.tex](./theorem/d5_225_T3_four_collision_families_note.tex)
- small `m=3` addendum for `T2/T3`:
  [theorem/d5_229_T2_T3_m3_small_case_note.md](./theorem/d5_229_T2_T3_m3_small_case_note.md)
- `T4` canonical entry:
  [theorem/d5_233_T4_canonical_entry_surface_proof_note.tex](./theorem/d5_233_T4_canonical_entry_surface_proof_note.tex)

### Graph-side selector block

- `G1` finite-defect splice principle:
  [theorem/d5_236_G1_finite_defect_splice_principle_note.tex](./theorem/d5_236_G1_finite_defect_splice_principle_note.tex)
- reduction history for the final `G1` target:
  [theorem/d5_240_G1_reverse_search_reduced_target_note.tex](./theorem/d5_240_G1_reverse_search_reduced_target_note.tex),
  [theorem/d5_243_G1_periodic_phase_carrier_candidate_note.tex](./theorem/d5_243_G1_periodic_phase_carrier_candidate_note.tex),
  [theorem/d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex](./theorem/d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex)
- final `G1` closure:
  [theorem/d5_247_G1_explicit_two_swap_splice_note.tex](./theorem/d5_247_G1_explicit_two_swap_splice_note.tex)
- `G2` by cyclic transport:
  [theorem/d5_234_graph_side_split_G2_closed_G1_remaining_note.tex](./theorem/d5_234_graph_side_split_G2_closed_G1_remaining_note.tex)

The short status snapshots for this slice are:

- [theorem/d5_249_master_status_after_G1.md](./theorem/d5_249_master_status_after_G1.md)
- [theorem/d5_251_bundle_review_and_polish_note.md](./theorem/d5_251_bundle_review_and_polish_note.md)
- [theorem/d5_251_manifest_summary.md](./theorem/d5_251_manifest_summary.md)

## Imported packets and honest boundary

The `251` refined manuscript is honest about what is still imported rather than
reproved inside the promoted slice:

- the post-entry odometer packet used after the canonical entry state is fixed;
- the final graph-side/globalization packet used to turn the closed
  selector-compatibility slice into the packaged Hamilton-decomposition proof.

After the later `253–255` cleanup, the packet closures are now written more
explicitly at theorem order. The old graph-side honesty boundary remains
historically important, and `256` shows that the current explicit `G1`
package does not in fact satisfy the transport route. The later `257–266`
Route-E line then closes the replacement graph-side branch itself: explicit
reduced color-`3` model, actual-model identification, and the final
color-`3` Hamilton theorem. The later `284–286` memo layer then sharpens the
current organizational read again: small odd residual packets and the
nonresonant packet are now treated as closed working blocks, and the live
remaining burden is recorded as a resonant residual program rather than a
generic all-odd assembly search.

So the current task is split:

- keep the top-level manuscript and companion aligned with the current
  resonant-residual boundary while the final theorem phrasing is still being
  settled;
- use `284–286` as the current reader-facing handoff, with `267–281` as the
  immediately preceding narrowing ladder;
- while separately continuing independence/internalization work that does not
  depend on that final graph-side assembly step.

For later prime-dimension generalization, the present D3/D5 probe
[d5_287_prime_cyclic_quotient_probe.md](./theorem/d5_287_prime_cyclic_quotient_probe.md)
is now the short methodological warning: the data support backbone-first /
return-ladder compression, not a full-torus cyclic-quotient-first program.

For the immediate next mathematical fragment, the current default priority is
[d5_288_next_closable_piece_priority.md](./theorem/d5_288_next_closable_piece_priority.md),
refined by
[d5_289_promoted_collar_base_section_reduction_and_no_go.md](./theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md):
first close the promoted-collar base-section reduction / no-go theorem, then
state the next positive repair target as a theorem about changing the induced
base permutation on `B_m`, before the separate `B`-active / gate theorem.

The newer operational compute read is now recorded separately in
[d5_291_residual_compute_campaign_conclusion.md](./theorem/d5_291_residual_compute_campaign_conclusion.md)
and the reusable batch template
[d5_292_residual_compute_request_template.md](./specs/d5_292_residual_compute_request_template.md):
the pure color-`1` branch should now be tested by whether a candidate changes
the reduced base permutation `P_m`, while the separate `B`-active branch
should be tested by whether it realizes a genuine wall/gate splice.

The inspection note
[d5_294_residual_package_alignment_after_tar.md](./theorem/d5_294_residual_package_alignment_after_tar.md)
then sharpens that operational read once more: the `2026-03-25` residual proof
package is most useful not as a new finished theorem packet but as a
deterministic narrowing of the next explicit family choice. For the pure
color-`1` branch with `5 ∤ m`, it first narrows attention to promoted-collar /
collar-row refinements. The follow-up probe
[d5_295_promoted_collar_dualA_vs_singleB_probe.md](./theorem/d5_295_promoted_collar_dualA_vs_singleB_probe.md)
then sharpens this once more: on checked resonant moduli, a single extra
`B_{s,3}` row is reducedly inert on `P_m`, while the opposite collar-row `A`
move is the first refinement that actually changes the reduced base
permutation, and already makes it a single cycle at `m=21`. So the current
explicit next-family read is “dual-collar `A` first, then only afterwards look
for further compensation”, while the `B`-active / gate branch remains
separate.

The next direction note
[d5_296_resonant_row3_direction_after_visible_grid.md](./theorem/d5_296_resonant_row3_direction_after_visible_grid.md)
then combines `289–295` with the new `tmp/resonant_row3_*` exact notes. The
current best read is now more specific than either generic `A+B` search or
immediate new-support escalation:

- first treat the resonant pure color-`1` branch as a
  **residue-sensitive visible-row seed problem**;
- only then ask for donor-aware compensation on top of the chosen seed;
- keep “new visible support outside the current 7-row grid” and `k=4`
  migration as second-line options.

The late atlas note
[d5_297_resonant_late_zero_return_atlas.md](./theorem/d5_297_resonant_late_zero_return_atlas.md)
adds the first exact zero-state calibration table on the later resonant
2-line branch. Its operational message is:

- the corrected late family encoding must use toggle semantics;
- the late branch is already residue-sensitive at the cheap exact atlas level;
- `B_m` is the expensive family-sensitive object, while `H_m` remains cheap and
  arithmetically rigid;
- and the next full `B_m` promotions should therefore be chosen selectively
  rather than pushed as a uniform late sweep.

The routing note
[d5_298_resonant_late_mod30_routing_note.md](./theorem/d5_298_resonant_late_mod30_routing_note.md)
then folds that atlas back into the earlier late exact ledger and records the
best current campaign map:

- `3 mod 30`: central-first lane;
- `9 mod 30`: crossover lane;
- `21/27 mod 30`: flank-first lanes, with `27` still the more fragile class;
- next exact promotions: `183` central and `201` flank.

The first exact-promotion note
[d5_299_resonant_late_first_exact_promotions.md](./theorem/d5_299_resonant_late_first_exact_promotions.md)
then executes that pair and sharpens the interpretation once more:

- `183` central is a full exact `B_m` win;
- `201` flank is still non-Hamilton, with cycle lengths `103,57,41`;
- so the mod-`30` atlas should currently be read as a promotion/routing law,
  not yet as a winner law.

The new master hinge theorem
[d5_300_resonant_Hm_master_hinge_profile_theorem.md](./theorem/d5_300_resonant_Hm_master_hinge_profile_theorem.md)
then upgrades the local resonant pure color-`1` picture again: the full first
hinge on all of `H_m` is now classified by one effective-phase formula, and
the initial side-top slice is no longer a missing sector. The follow-up status
note
[d5_301_resonant_pure_color1_proof_state_after_Hm_master_profile.md](./theorem/d5_301_resonant_pure_color1_proof_state_after_Hm_master_profile.md)
records the new frontier more sharply: the lower-to-hinge classification is
closed, and the remaining theorem burden has moved upward to double-top
phase-exit and `H_m -> B_m` stitching.

The new core-chain note
[d5_302_resonant_pure_color1_core_chain.md](./theorem/d5_302_resonant_pure_color1_core_chain.md)
then packages the proof-carrying substance of the `2026-03-26` resonant pure
color-`1` bundle into one theorem-order map, so a reader does not need to
reconstruct that chain from many `tmp/` notes. The global status note
[d5_303_current_d5_proof_status_overview.md](./theorem/d5_303_current_d5_proof_status_overview.md)
finally gives the shortest current split between theorem-level closure,
checked-exact packets, and the genuine remaining live frontier.

## Compute support

The checkers and saved outputs from the `251` bundle are now promoted under:

- `scripts/d5_219_*.py`, `scripts/d5_222_*.py`, `scripts/d5_225_*.py`,
  `scripts/d5_228_*.py`, `scripts/d5_229_*.py`, `scripts/d5_230_*.py`,
  `scripts/d5_232_*.py`, `scripts/d5_234_*.py`, `scripts/d5_237_*.py`,
  `scripts/d5_239_*.py`, `scripts/d5_242_*.py`, `scripts/d5_244_*.py`,
  `scripts/d5_247_*.py`
- matching summaries and tables under `RoundY/checks/`
- the refined TeX manuscript and overview under `RoundY/tex/`

## Historical background still in force

The earlier accepted-package notes are still the right stable background for the
odd-`m` D5 proof spine:

- [theorem/d5_091_independent_package_gap_note.md](./theorem/d5_091_independent_package_gap_note.md)
- [theorem/d5_092_cleaned_independent_theorem_suite.md](./theorem/d5_092_cleaned_independent_theorem_suite.md)
- [theorem/d5_095_compact_reproof_079_chart_interface_landing.md](./theorem/d5_095_compact_reproof_079_chart_interface_landing.md)
- [theorem/d5_096_compact_reproof_081_regular_closure.md](./theorem/d5_096_compact_reproof_081_regular_closure.md)
- [theorem/d5_097_compact_reproof_077_tail_length_reduction.md](./theorem/d5_097_compact_reproof_077_tail_length_reduction.md)
- [theorem/d5_098_compact_cleanup_033_062_structural_block.md](./theorem/d5_098_compact_cleanup_033_062_structural_block.md)
- [theorem/d5_099_one_pass_odd_m_globalization_package.md](./theorem/d5_099_one_pass_odd_m_globalization_package.md)
- [theorem/d5_106_intended_quotient_identification_and_comparison.md](./theorem/d5_106_intended_quotient_identification_and_comparison.md)
- [theorem/d5_121_M5_corrected_row_stitching.md](./theorem/d5_121_M5_corrected_row_stitching.md)
- [theorem/d5_122_M5_all_odd_identification.md](./theorem/d5_122_M5_all_odd_identification.md)

## Larger program status

RoundY is only the live `d=5` branch.

- `d=3` is mathematically solved in the odometer presentation.
- `d=4` is mathematically solved and Lean-formalized.
- the remaining low-dimensional manuscript assembly work is concentrated on
  `d=5`.
