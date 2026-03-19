# Instruction For Codex

This file is the shortest practical briefing for a Codex-style agent entering
the current RoundY `d=5` branch.

It is not a full history. It is the minimum orientation needed to avoid
restarting dead branches and to think in the right coordinates from the start.

## Read this first

Read in this order:

1. [README.md](./README.md)
2. [current-frontier-and-approach.md](./current-frontier-and-approach.md)
3. [theorem/d5_076_unified_handoff.md](./theorem/d5_076_unified_handoff.md)
4. [theorem/d5_076_bridge_main.md](./theorem/d5_076_bridge_main.md)
5. [theorem/d5_076_realization_trackB.md](./theorem/d5_076_realization_trackB.md)
6. [theorem/d5_076_concrete_bridge_proof.md](./theorem/d5_076_concrete_bridge_proof.md)
7. [theorem/d5_077_globalization_handoff.md](./theorem/d5_077_globalization_handoff.md)
8. [theorem/d5_077_live_questions_and_tracks.md](./theorem/d5_077_live_questions_and_tracks.md)
9. [theorem/d5_077_tail_length_and_actual_union.md](./theorem/d5_077_tail_length_and_actual_union.md)
10. [theorem/d5_078_global_component_structure.md](./theorem/d5_078_global_component_structure.md)
11. [theorem/d5_078_endpoint_compatibility_criterion.md](./theorem/d5_078_endpoint_compatibility_criterion.md)
12. [theorem/d5_078_large_modulus_regular_union_support.md](./theorem/d5_078_large_modulus_regular_union_support.md)
13. [theorem/d5_078_safe_theorem_language_review.md](./theorem/d5_078_safe_theorem_language_review.md)
14. [theorem/d5_078_accepted_frontier_and_split.md](./theorem/d5_078_accepted_frontier_and_split.md)
15. [theorem/d5_079_single_critical_lemma.md](./theorem/d5_079_single_critical_lemma.md)
16. [theorem/d5_079_exceptional_interface_support.md](./theorem/d5_079_exceptional_interface_support.md)
17. [theorem/d5_080_next_work_program.md](./theorem/d5_080_next_work_program.md)
18. [theorem/d5_080_no_mixed_delta_reduction.md](./theorem/d5_080_no_mixed_delta_reduction.md)
19. [theorem/d5_081_regular_union_and_gluing_support.md](./theorem/d5_081_regular_union_and_gluing_support.md)
20. [theorem/d5_082_exceptional_row_reduction.md](./theorem/d5_082_exceptional_row_reduction.md)
21. [theorem/d5_082_frontier_and_theorem_map.md](./theorem/d5_082_frontier_and_theorem_map.md)
22. [theorem/d5_083_gluing_flow_and_final_theorem.md](./theorem/d5_083_gluing_flow_and_final_theorem.md)
23. [theorem/d5_083_final_theorem_proof.md](./theorem/d5_083_final_theorem_proof.md)
24. [theorem/d5_085_proof_progress_report.md](./theorem/d5_085_proof_progress_report.md)
25. [theorem/d5_086_dependency_audit_and_generalization_gate.md](./theorem/d5_086_dependency_audit_and_generalization_gate.md)
26. [theorem/d5_086_dependency_flow_diagram.md](./theorem/d5_086_dependency_flow_diagram.md)
27. [theorem/d5_087_dependency_audit_report.md](./theorem/d5_087_dependency_audit_report.md)
28. [theorem/d5_091_independent_package_gap_note.md](./theorem/d5_091_independent_package_gap_note.md)
29. [theorem/d5_092_cleaned_independent_theorem_suite.md](./theorem/d5_092_cleaned_independent_theorem_suite.md)
30. [theorem/d5_093_reproof_targets_after_092.md](./theorem/d5_093_reproof_targets_after_092.md)
31. [theorem/d5_095_compact_reproof_079_chart_interface_landing.md](./theorem/d5_095_compact_reproof_079_chart_interface_landing.md)
32. [theorem/d5_096_compact_reproof_081_regular_closure.md](./theorem/d5_096_compact_reproof_081_regular_closure.md)
33. [theorem/d5_097_compact_reproof_077_tail_length_reduction.md](./theorem/d5_097_compact_reproof_077_tail_length_reduction.md)
34. [theorem/d5_098_compact_cleanup_033_062_structural_block.md](./theorem/d5_098_compact_cleanup_033_062_structural_block.md)
35. [theorem/d5_099_one_pass_odd_m_globalization_package.md](./theorem/d5_099_one_pass_odd_m_globalization_package.md)
36. [theorem/d5_100_graph_theoretic_hamilton_decomposition_proof_draft.md](./theorem/d5_100_graph_theoretic_hamilton_decomposition_proof_draft.md)
37. [theorem/d5_even_case_strategy_from_d3.md](./theorem/d5_even_case_strategy_from_d3.md)
38. [theorem/d5_even_m_parity_and_critical_row_program.md](./theorem/d5_even_m_parity_and_critical_row_program.md)
39. [theorem/d5_033_explicit_trigger_family.md](./theorem/d5_033_explicit_trigger_family.md)
40. [theorem/d5_084_theorem_name_map.md](./theorem/d5_084_theorem_name_map.md)
41. [theorem/d5_090_tmp_promotion_index.md](./theorem/d5_090_tmp_promotion_index.md)
42. [theorem/d5_094_tmp_remaining_priority_map.md](./theorem/d5_094_tmp_remaining_priority_map.md)
43. [checks/d5_084_compute_evidence_index.md](./checks/d5_084_compute_evidence_index.md)
44. [theorem/d5_075_threeway_handoff.md](./theorem/d5_075_threeway_handoff.md)
45. [theorem/d5_075_bridge_theorem_request.md](./theorem/d5_075_bridge_theorem_request.md)
46. [theorem/d5_075_realization_integration_request.md](./theorem/d5_075_realization_integration_request.md)
47. [theorem/d5_075_compute_validation_request.md](./theorem/d5_075_compute_validation_request.md)
48. [theorem/d5_075_reviewer_brief.md](./theorem/d5_075_reviewer_brief.md)
49. [../DOCUMENT_FOR_EXTERNAL_REVIEW.md](../DOCUMENT_FOR_EXTERNAL_REVIEW.md)
   Focus on `D23`, `D24`, `D25`, `D26`, `D27`, `D28`, `D29`, `D30`, `D31`,
   `D32`, `D33`, `D34`, `D35`, `D37`, `D38`, `D40`, `D42`, `D45`, `D46`,
   `D47`, `D48`, `D49`.
50. [autonomous/d5_autonomous_perturbation_note_v25.md](./autonomous/d5_autonomous_perturbation_note_v25.md)
51. [theorem/d5_106_intended_quotient_identification_and_comparison.md](./theorem/d5_106_intended_quotient_identification_and_comparison.md)
52. [theorem/d5_111_m4_filled_tables_and_compression_gap.md](./theorem/d5_111_m4_filled_tables_and_compression_gap.md)
53. [specs/d5_111_m4_external_request.md](./specs/d5_111_m4_external_request.md)
54. [../tmp/d5_112_selector_compression_no_go_note.tex](../tmp/d5_112_selector_compression_no_go_note.tex)
55. [../tmp/d5_113_rewrite_M4_selector_theorem.tex](../tmp/d5_113_rewrite_M4_selector_theorem.tex)
56. [../tmp/d5_114_defect_slice_factorization_note.tex](../tmp/d5_114_defect_slice_factorization_note.tex)

Then read the key artifact READMEs in this order:

1. [../artifacts/d5_return_map_model_017/README.md](../artifacts/d5_return_map_model_017/README.md)
2. [../artifacts/d5_mixed_normal_form_and_u_obstruction_019/README.md](../artifacts/d5_mixed_normal_form_and_u_obstruction_019/README.md)
3. [../artifacts/d5_grouped_transposition_family_023/README.md](../artifacts/d5_grouped_transposition_family_023/README.md)
4. [../artifacts/d5_omit_base_cocycle_defect_025/README.md](../artifacts/d5_omit_base_cocycle_defect_025/README.md)
5. [../artifacts/d5_endpoint_latin_repair_032/README.md](../artifacts/d5_endpoint_latin_repair_032/README.md)
6. [../artifacts/d5_defect_splice_transducer_033/README.md](../artifacts/d5_defect_splice_transducer_033/README.md)
7. [../artifacts/d5_corridor_phase_extraction_034/README.md](../artifacts/d5_corridor_phase_extraction_034/README.md)
8. [../artifacts/d5_static_phase_gate_nogo_035/README.md](../artifacts/d5_static_phase_gate_nogo_035/README.md)
9. [../artifacts/d5_corridor_phase_clarification_036/README.md](../artifacts/d5_corridor_phase_clarification_036/README.md)
10. [../artifacts/d5_lifted_corridor_carrier_target_037/README.md](../artifacts/d5_lifted_corridor_carrier_target_037/README.md)
11. [../artifacts/d5_birth_local_signature_search_038/README.md](../artifacts/d5_birth_local_signature_search_038/README.md)
12. [../artifacts/d5_raw_birth_marker_transport_039/README.md](../artifacts/d5_raw_birth_marker_transport_039/README.md)
13. [../artifacts/d5_rich_observable_realization_040/README.md](../artifacts/d5_rich_observable_realization_040/README.md)
14. [../artifacts/d5_coordinate_exposure_admissibility_041/README.md](../artifacts/d5_coordinate_exposure_admissibility_041/README.md)
15. [../artifacts/d5_carry_slice_cover_042/README.md](../artifacts/d5_carry_slice_cover_042/README.md)
16. [../artifacts/d5_finite_cover_admissibility_043/README.md](../artifacts/d5_finite_cover_admissibility_043/README.md)
17. [../artifacts/d5_carry_and_finite_cover_044/README.md](../artifacts/d5_carry_and_finite_cover_044/README.md)
18. [../artifacts/d5_carry_admissibility_search_045/README.md](../artifacts/d5_carry_admissibility_search_045/README.md)
19. [../artifacts/d5_deep_transition_carry_sheet_046/README.md](../artifacts/d5_deep_transition_carry_sheet_046/README.md)
20. [../artifacts/d5_future_transition_carry_coding_047/README.md](../artifacts/d5_future_transition_carry_coding_047/README.md)
21. [../artifacts/d5_tau_countdown_carrier_048/README.md](../artifacts/d5_tau_countdown_carrier_048/README.md)
22. [../artifacts/d5_source_residue_refinement_049/README.md](../artifacts/d5_source_residue_refinement_049/README.md)
23. [../artifacts/d5_proof_support_generalization_050/README.md](../artifacts/d5_proof_support_generalization_050/README.md)
24. [../artifacts/d5_boundary_reset_proof_support_055/README.md](../artifacts/d5_boundary_reset_proof_support_055/README.md)
25. [../artifacts/d5_phase_scheduler_branch_support_059b/README.md](../artifacts/d5_phase_scheduler_branch_support_059b/README.md)

If working on Lean / formalization, then also read:

1. [../formal/README-D5.md](../formal/README-D5.md)
2. [../formal/D5_LEAN_PROGRESS.md](../formal/D5_LEAN_PROGRESS.md)

If producing a new research note or work spec, use:

1. [../docs/template_to_use.md](../docs/template_to_use.md)
2. [../docs/suggested_workflow.md](../docs/suggested_workflow.md)

For D5 support files inside this repo, use this layout:

- `RoundY/specs/` for executable specs and work templates
- `RoundY/checks/` for small JSON prep checks and follow-up summaries
- `RoundY/theorem/` for theorem-shaping notes and snippets
- root `RoundY/` for short session summaries such as `codex_work_s59.md`

For the current theorem-side packaging around `047–062`, start with:

1. [theorem/d5_proof_program_050.md](./theorem/d5_proof_program_050.md)
2. [theorem/d5_proof_generalization_051.md](./theorem/d5_proof_generalization_051.md)
3. [theorem/d5_boundary_reset_and_tau_proof_052.md](./theorem/d5_boundary_reset_and_tau_proof_052.md)
4. [theorem/d5_positive_theorem_chain_054.md](./theorem/d5_positive_theorem_chain_054.md)
5. [theorem/d5_boundary_reset_uniform_proof_attempt_055.md](./theorem/d5_boundary_reset_uniform_proof_attempt_055.md)
6. [theorem/d5_CJ_branch_proof_reduction_056.md](./theorem/d5_CJ_branch_proof_reduction_056.md)
7. [theorem/d5_phase_machine_hypothesis_057a.md](./theorem/d5_phase_machine_hypothesis_057a.md)
8. [theorem/d5_phase_machine_summary_058.md](./theorem/d5_phase_machine_summary_058.md)
9. [theorem/d5_phase_scheduler_uniform_proof_059.md](./theorem/d5_phase_scheduler_uniform_proof_059.md)
10. [theorem/d5_B_region_invariance_proof_progress_060.md](./theorem/d5_B_region_invariance_proof_progress_060.md)
11. [theorem/d5_B_region_bootstrap_proof_061.md](./theorem/d5_B_region_bootstrap_proof_061.md)
12. [theorem/d5_first_exit_target_proof_062.md](./theorem/d5_first_exit_target_proof_062.md)
13. [theorem/d5_067_concentrated_handoff.md](./theorem/d5_067_concentrated_handoff.md)
14. [theorem/d5_068_theorem_package_organized.md](./theorem/d5_068_theorem_package_organized.md)
15. [theorem/d5_069_concentrated_handoff.md](./theorem/d5_069_concentrated_handoff.md)
16. [theorem/d5_070_minimal_handoff_for_069_readers.md](./theorem/d5_070_minimal_handoff_for_069_readers.md)
17. [theorem/d5_071_unified_bridge_handoff.md](./theorem/d5_071_unified_bridge_handoff.md)
18. [theorem/d5_071_four_researcher_questions.md](./theorem/d5_071_four_researcher_questions.md)
19. [theorem/d5_075_threeway_handoff.md](./theorem/d5_075_threeway_handoff.md)
20. [theorem/d5_076_unified_handoff.md](./theorem/d5_076_unified_handoff.md)
21. [theorem/d5_077_globalization_handoff.md](./theorem/d5_077_globalization_handoff.md)
22. [theorem/d5_077_live_questions_and_tracks.md](./theorem/d5_077_live_questions_and_tracks.md)
23. [theorem/d5_078_accepted_frontier_and_split.md](./theorem/d5_078_accepted_frontier_and_split.md)
24. [theorem/d5_079_single_critical_lemma.md](./theorem/d5_079_single_critical_lemma.md)

These notes now spell out the actual top-level split:

- theorem package:
  phase-corner theorem, countdown/reset corollaries, and the `033 -> 062 -> 059`
  structural spine; after `068`, this side should usually be treated as
  near-stable unless the user is explicitly asking for theorem cleanup
- exact reduction / realization:
  the canonical `beta` clock on the exact marked reduction object; after `069`,
  the right question is no longer “invent the clock” but “identify the exact
  object and prove the quotient is exact enough that the clock descends”
- bridge question:
  after `071`, the first exact per-chain marked-chain rule is mostly settled;
  the live missing link is whether those exact quotients globalize across
  chains, or whether the carry is essentially asymmetric
- dynamic bridge:
  after `074`, the best current exact object is the splice-compatible dynamic
  bridge `(beta,q,sigma)` / `(beta,delta)`; the active work is now bridge
  theorem, realization integration, and compute validation of that object
- theorem/support cleanup:
  after `075`, keep the theorem-level canonical bridge abstract as
  `(beta,rho)` unless the concrete identification with `(q,sigma)` /
  `delta` is actually proved; treat the odometer coordinates as the strongest
  checked model, not automatically as theorem data
- intended quotient comparison:
  after `105/106`, the honest M3 target is still the exact deterministic
  quotient retaining grouped base; the checked comparison is
  `(B,beta) ~= (rho,beta,q0,sigma)` on the exact marked chain object, so do not
  flatten the theorem-side quotient prematurely to bare `(beta,delta)`
- accepted `077` reduction:
  fixed-`delta` ambiguity is now reduced to tail length / terminal geometry;
  the live question is global component structure, not local bridge readout
- compute support:
  only reduction validation, accessible quotient validation, and
  `(B,beta)` exactness / drift stress tests
- separate even-`m` branch:
  do not mix it into the closed odd-`m` bridge chain; the current even target
  is a parity-barrier / formal-extension / critical-row repair theorem package,
  not a reopened odd-style globalization search

## Real current problem

Do not frame the problem as:

- “find any mixed witness”
- “find a better one-bit separator”
- “try a slightly larger tiny transducer”

The strongest current theorem-side draft after `062` is:

**derive the universal first-exit targets directly from the explicit `H_{L1}`
trigger theorem, then recover `B`-region invariance, the global active phase
scheduler, and the reset laws as one structural chain**

The odd-`m` globalization theorem is now closed inside the accepted package.
The honest remaining frontier is therefore downstream and graph-theoretic:

**the theorem-side / globalization line is no longer the bottleneck. After
`100`, `106`, the graph packet `111–118`, and the promoted M5 follow-up
`119–122`, the live graph-theoretic split is now: the old raw-row M4 problem
has been replaced by a corrected-selector package candidate (`116/117`), and
the main downstream question is whether to accept that package and integrate
the now-closed color-4 Sel* M5 route into the broader graph proof.**

More concretely:

- `111` shows the M4 tables can be extracted on the actual `mixed_008` full
  torus, but even raw coordinates fail outgoing permutation coverage;
- `112` shows exact compression of the current raw selector row cannot close
  M4, so the remaining target is a transformed selector lift, not a quotient of
  the same row;
- `113` proves that bare selector existence is already solved by the
  common-transport / sum-selector family, so the meaningful remaining work is
  D5 compatibility rather than generic selector existence;
- `114` identifies that D5 compatibility problem with a weighted pair of
  defect-slice 1-factorizations on `G_2` and `G_3`, together with compression
  of the completed defect rows to a compact exact field.
- `115` executes the shrunk compute request:
  the small-tier selector table is stable, but the first slice-4 intermediate
  families `(B_k for k in subset, Z, M)` with `subset ⊆ {0,1,2,3,4,5}` and the
  cyclic orbit quotient of `(fullpairs, Z, M)` are still no-go.
- `116` proposes the exact symbolic slice-4 transport field
  `F4sharp = (B2,B3,B4,Z,O,M)`.
- `117` proposes a direct corrected-selector theorem for odd `m >= 5`.
- `118` explains that if `117` is accepted then M4 and M6 are effectively
  closed in the needed sense, and M5 becomes the live graph-level package.
- `119` shows that the easiest first-return factor families for `Sel*` do not
  give a genuine `m^3` compression and that the color-4 route should move to
  the final section.
- `120` reduces the color-4 Sel* M5 problem to the final section return `U_m`
  and extracts the corrected-row coordinates.
- `121` proves the corrected-row model is one `m^2`-cycle for every odd
  `m >= 11`.
- `122` proves the actual/model identification and closes the color-4 Sel* M5
  route for all odd moduli.

`R1 -> H_L1`

for the best endpoint seed:

- left `[2,2,1]`
- right `[1,4,4]`

## What is already known

Treat these as current working facts unless you are explicitly revisiting them.

1. `019`
   The canonical mixed witness already has an explicit reduced return-map
   model.

2. `023–025`
   The right reduced perturbation target is known:
   the grouped target is not vague anymore.

3. `032`
   The best local endpoint seed is known.

4. `033`
   The defect graph is bounded and the natural small transducer branch is
   already pruned on the current alphabet.

5. `034`
   The unresolved corridor admits a first-pass projected phase model on
   `(s, layer)`.

6. `035`
   The first raw static phase-exposure layer is already pruned:
   no `1`- or `2`-coordinate projection isolates the first exit, and every
   static `B`-state gate built from the separating `3`-coordinate projections
   fails Latin.

7. `036`
   The saved `034` `(s, layer)` rule is only a first-pass projected lap, while
   the traced long corridor lifts exactly to `(q, a, layer)`.

8. `037`
   That lifted state is already visible on raw `(q,w,layer)`, and the traced
   corridor is an exact raw-coordinate odometer with two universal first-exit
   targets.

9. `038`
   In the simple one-step predecessor/successor neighborhood-bit family, the
   exceptional source slice is already locally visible, but the source marker
   and entry marker are not isolated up to projection size `5`.

10. `039`
   In exact raw current coordinates, the source and entry birth classes are
   already explicit, but current raw `u` drifts through all residues later, so
   the family tag still has to be transported.

11. `040`
   The first richer source-edge / lagged lifts of the simple `038` row still
   fail, but raw current coordinates already realize birth, active family
   separation, and active-conditioned target firing on the checked active
   union.
12. `041`
   The first `025`-style grouped-state-descending admissible families still
   fail exactly. `w` already descends as `s-u`, but the fire predicates do not
   descend to current grouped state `(s,u,v)`, even after conditioning on
   family. So the next honest target is one lifted coordinate beyond current
   grouped state.
13. `042`
   The carry-slice bit `c = 1_{q=m-1}` is the smallest verified trigger lift:
   exceptional fire already descends to
   `B = (s,u,v,layer,family)`, and regular fire descends to `B` plus `c`.
   But `(B,c)` is still not a closed deterministic dynamics. The structural
   lift is therefore better read as a tiny finite cover over `B`, with fiber
   size at most `3` on the checked range.
14. `043`
   That finite-cover statement sharpens:
   the minimal deterministic cover over `B+c` is `2`-sheet on
   `m=5,7,9,11`, supported entirely on the regular noncarry branch.
   The residual sheet is not the obvious bit `1_{q=m-2}` on `m=7,9,11`, while
   `time to next carry` already gives a theorem-friendly nonlocal
   coordinatization.
15. `044`
   The theorem branch becomes explicit:
   the residual sheet can be chosen as
   `d = 1_{next carry u >= m-3}`.
   So the checked active branch factors as
   `B <- B+c <- B+c+d`,
   with `d` a binary anticipation sheet and carry states singleton over `B+c`.

16. `045`
   The first carry-only admissible catalogs are already pruned exactly:
   `0` exact candidates across the checked
   current-edge / label / delta core catalog up to size `5`,
   low-cardinality gauge-transition catalog up to size `5`,
   and targeted point-defect catalog up to size `4`.
   Full `B -> B_next` and `B -> B_next -> B_next2` grouped transition classes
   still fail.

17. `046`
   The carry sheet is already an exact future-transition event on the checked
   active grouped base.
   The minimal exact future `dn` horizon is `m-3`, the minimal exact future
   grouped-state horizon is `m-2`, and the exact future window compresses to
   current `B` plus `flat-run length + first nonflat dn`.
18. `047`
   The exact checked-range carry target sharpens to
   `B + min(tau,8) + epsilon4`.
   The boundary event class at `tau=0` is `3`-class minimal, and the first
   exact transition-sheet coding is current `B` plus current `epsilon4` plus
   the next `7` future flat/nonflat indicators after the current step.
19. `048`
   `tau` itself already has exact internal dynamics on the checked active
   nonterminal branch:
   for `tau>0`, the next value is `tau-1`,
   while the boundary reset at `tau=0` is tiny and current-state driven:
   `wrap -> 0`, `carry_jump` on `(s,v,layer)`, and `other` on `(s,u,layer)`.
20. `049`
   a stronger constructive refinement persists through `m=19`:
   with `rho = source_u + 1 mod m`,
   `tau` is exact on `(s,u,v,layer,rho)`,
   `next_tau` is exact on `(s,u,layer,rho,epsilon4)`,
   and `c` is exact on `(u,rho,epsilon4)`.
   But `rho` is not recoverable from `(B,tau,epsilon4)` once `m>=7`, so this
   is a compute-side refinement, not the main theorem object.
21. `050`
   the two narrow proof-support checks persist through `m=19`:
   the `048` reset law remains exact on the same theorem-side quotients,
   and the explicit `047/048` witness pair persists with the same
   `h < m-4` lower-bound shape.
22. `055`
   the boundary-reset proof-support formulas extend through `m=21,23`:
   `carry_jump`, the raw identity `q = 1-s-v-layer`, the `other` subtype law,
   and `wrap -> 0` remain exact.
23. `056`
   the remaining positive burden is compressed to `CJ`, with the real content
   in the noncarry dichotomy rather than the whole branch law.
24. `057`
   `CJ` is reduced again to a one-step flat-corner lemma.
25. `058/058B`
   the flat-corner lemma itself is compressed to a tiny checked phase/corner
   machine in `Theta = q+s+v+layer`, and on the checked frozen scope that
   machine already yields both `CJ` and `OTH`.
26. `059`
   the active phase scheduler is reinterpreted as the mixed witness rule on
   the active branch, once one knows the branch stays in `B`.
27. `059B`
   the safe branch-local support route validates that scheduler / `B`-region
   picture through `m=25,27,29`.
28. `060`
   `B`-region invariance is reduced to avoidance of the six patched classes.
29. `061`
   that invariance is then bootstrapped from local `B`-state dynamics plus the
   universal first-exit targets via the `Theta=2` cross-section odometer.
30. `062`
   the universal first-exit targets are then derived directly from the exact
   `H_{L1}` trigger theorem from `033`, the candidate active orbit, and the
   phase-`1` source-residue invariant; then `B`-region invariance, the global
   phase scheduler, and the reset laws follow.

So the branch is now:

**projected phase known, raw odometer known, raw control logic explicit, grouped-state descent exhausted, carry lift identified, binary anticipation cover explicit, first carry-only catalogs exhausted, future-transition carry sheet extracted, exact checked-range carry coding extracted, countdown carrier extracted, stronger current-memory refinement available, larger-modulus proof support in place, phase machine isolated, `B`-region bootstrap identified, and first-exit targets internalized**

## Patterns to think in first

These patterns should come before any broad search.

### 1. Reduced model first, local realization second

Always ask:

- what reduced map is already known?
- what exact obstruction remains in that reduced map?
- what is the smallest local mechanism that could realize or expose it?

Do not jump to local-rule widening before answering those.

### 2. One best seed first

Use the best seed from `032` first:

- left `[2,2,1]`
- right `[1,4,4]`

Do not widen to lower-ranked seeds unless the best-seed branch is genuinely
exhausted or the new mechanism clearly cannot act on that seed.

### 3. Preserve the `025` target unless there is evidence to leave it

The current reduced target is not a vague heuristic. It is the best exact
reduced object we have.

Default assumption:

- preserve the `025` grouped target to first order

Only leave it if a branch gives concrete evidence that the true target must be
different.

### 4. Phase machine before branch lemmas

Do not start from separate `CJ` and `OTH` formulas if the active phase
scheduler can be used instead.

The current proof compression is:

- phase scheduler in `Theta = q+s+v+layer`
- then flat-corner / branch laws as corollaries
- then `061` bootstrap for `B`-region invariance
- then `062` derivation of the universal first-exit targets

So the first proof question is now:

- if `062` is not yet accepted, can that strengthened structural chain be
  finalized cleanly?

### 5. Treat failure as obstruction sharpening

Every failed branch must return one of:

- a smaller live search space
- a structural no-go
- a cleaner reduced target
- a sharper theorem-shaped conjecture

“No survivors” by itself is not enough.

### 6. Think in orbit phase, not opaque controller state

After `034–037`, the live obstruction is best thought of as corridor
localization on top of an already-visible raw odometer.

Default question:

- how can a local rule read or carry the extracted phase?

not:

- how can we add more abstract controller states?

### 7. Prefer theorem-shaped outputs

The strongest outputs now are not huge candidate lists.
They are:

- exact reduced formulas
- exact obstruction statements
- exact quotient laws
- exact phase rules
- exact “if this local mechanism exists, then the grouped target follows”
  bridge lemmas

## Anti-patterns to avoid

Do not default to:

1. broad one-bit scans
2. broad generic `2`-state / `3`-state transducer widening on the same local
   alphabet
3. reopening static endpoint-word catalogs without a phase-aware ingredient
4. abandoning the best seed too early
5. abandoning the `025` reduced target without hard evidence
6. treating computational extraction as a proof without isolating the
   theorem-shaped statement behind it

## Standard pilot discipline

Unless there is a reason not to:

- pilot on `m = 5,7,9`
- use `m = 11` as the first control
- keep the best-seed branch fixed
- save exact JSON summaries
- separate:
  - extracted facts
  - heuristic interpretation
  - failed search facts

## Critical theorem targets

If you are trying to make mathematical progress, these are the best theorem
targets to seek.

### Already extracted, worth proving cleanly

1. Mixed return-map theorem from `019`
2. Reduced perturbation target theorem from `025`
3. Best-seed defect quotient theorem from `033`
4. Corridor phase theorem from `034`
5. Static phase-gate no-go theorem from `035`
6. Corridor lift theorem from `036`
7. Raw odometer theorem from `037`

### Next real targets

8. Localized-carrier theorem
9. Visible-phase no-go theorem
10. Local-to-reduced realization theorem
11. Bridge-to-full-D5 theorem

Useful supporting lemmas:

9. exceptional-slice lemma (`u_source = 3`)
10. delay law lemma
11. orbit-residue lemma
12. small-orbit description lemma

## Expected output style

When starting a new branch, the default output should be:

1. a research note in the `template_to_use.md` format
2. a narrow executable work spec if computation is needed
3. an artifact bundle if real search / extraction is performed
4. an explicit branch recommendation at the end

Good outputs answer:

- what was learned?
- what was pruned?
- what is now the honest next branch?

## Short version

If you remember only one line, remember this:

**Do not search generically. Read the branch as a corridor-local carrier problem
on top of an already-visible raw odometer.**
