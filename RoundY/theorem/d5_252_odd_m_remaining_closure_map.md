# D5 252 Odd-m Remaining Closure Map

Historical note:

- this note records the `251 -> 252` closure boundary;
- the later `255` honesty pass refines the graph-side status by separating the
  remaining `G1 -> G2` transport-compatibility issue from the rest of the
  independence/internalization work;
- for the current state, read this note together with
  [d5_255_transport_honesty_boundary.md](./d5_255_transport_honesty_boundary.md)
  and
  [d5_256_independence_internalization_queue.md](./d5_256_independence_internalization_queue.md).

This note records the current shortest answer to:

> what still has to be closed or internalized before the odd-`m`, `d=5`
> theorem can be treated as a clean finished proof manuscript?

It is written relative to the promoted `251` manuscript slice.

## 1. What is already closed

Inside the promoted `251` slice, the following are now closed:

- `T0` actual-needed tiny-repair core
- `T1`, `T2`, `T3`
- `T4` canonical entry
- `G1` colorwise selector-compatibility
- `G2` cyclic transport

The shortest status reference is:

- [d5_249_master_status_after_G1.md](./d5_249_master_status_after_G1.md)

The refined manuscript and overview are:

- [../tex/d5_251_full_d5_working_manuscript_refined.tex](../tex/d5_251_full_d5_working_manuscript_refined.tex)
- [../tex/d5_251_proof_bundle_overview_refined.tex](../tex/d5_251_proof_bundle_overview_refined.tex)

## 2. What is still imported in the refined manuscript

The refined manuscript still imports two blocks:

1. the post-entry odometer packet;
2. the final graph-side/globalization packet.

These are the only remaining nontrivial proof objects in the current
manuscript-order presentation.

## 3. Remaining theorem objects

### A. Post-entry odometer packet

Current role in the refined manuscript:

- theorem label: `thm:odometer-spine`
- mathematical role:
  once the canonical entry state is reached, the actual active branch agrees
  with the candidate one-corner orbit up to first exit, with the explicit
  trigger family and universal exits.

What is needed to close or package it cleanly:

- a clean front-end one-corner reduction interface:
  [d5_233_T4_canonical_entry_surface_proof_note.tex](./d5_233_T4_canonical_entry_surface_proof_note.tex)
- best-seed normal form / shape-side packaging:
  [d5_131_032_seed_normal_form_note.tex](./d5_131_032_seed_normal_form_note.tex)
- shape certificate extraction and its saved data:
  [d5_137_shape_certificate_extraction.md](./d5_137_shape_certificate_extraction.md)
- late local provenance support on the surfaced `sigma23`/`R1` branch:
  [d5_197_sigma23_r1_microstate_check.md](./d5_197_sigma23_r1_microstate_check.md)
- one-corner rewrite framing:
  [d5_133_one_corner_front_end_reduction_note.tex](./d5_133_one_corner_front_end_reduction_note.tex)

Acceptable end state:

- either internalize this packet directly into the refined manuscript;
- or keep it imported, but with an explicit citation chain and a stable compact
  theorem note that a new reader can verify linearly.

### B. Final graph-side/globalization packet

Current role in the refined manuscript:

- stable graph-side inputs:
  corrected selector baseline, closed color-4 surgery branch, globalization
  input
- final stitching theorem:
  converts the front-end reduction, odometer spine, and colorwise package into
  the final odd-`m`, `d=5` Hamilton structure.

What is needed to close or package it cleanly:

- the promoted `G1/G2` block:
  [d5_234_graph_side_split_G2_closed_G1_remaining_note.tex](./d5_234_graph_side_split_G2_closed_G1_remaining_note.tex),
  [d5_236_G1_finite_defect_splice_principle_note.tex](./d5_236_G1_finite_defect_splice_principle_note.tex),
  [d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex](./d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex),
  [d5_247_G1_explicit_two_swap_splice_note.tex](./d5_247_G1_explicit_two_swap_splice_note.tex)
- the accepted odd-`m` globalization spine:
  [d5_082_frontier_and_theorem_map.md](./d5_082_frontier_and_theorem_map.md),
  [d5_083_gluing_flow_and_final_theorem.md](./d5_083_gluing_flow_and_final_theorem.md),
  [d5_083_final_theorem_proof.md](./d5_083_final_theorem_proof.md),
  [d5_099_one_pass_odd_m_globalization_package.md](./d5_099_one_pass_odd_m_globalization_package.md)
- the graph-side branch/package context:
  [d5_121_M5_corrected_row_stitching.md](./d5_121_M5_corrected_row_stitching.md),
  [d5_122_M5_all_odd_identification.md](./d5_122_M5_all_odd_identification.md),
  [d5_123_M_route_status_after_122.md](./d5_123_M_route_status_after_122.md),
  [d5_130_revised_consolidated_manuscript_after_M1_review.tex](./d5_130_revised_consolidated_manuscript_after_M1_review.tex)

Acceptable end state:

- either internalize a short final stitching theorem into the refined
  manuscript;
- or freeze a stable explicit theorem chain for the imported graph-side and
  globalization packet and cite that chain directly.

## 4. What is not part of this closure target

This closure map is about odd `m`, `d=5`.

It does not close:

- the even-`m` branch;
- a larger standalone full-`T0` theorem over the entire seed list;
- unrelated formal/Lean tasks.

## 5. Suggested reading order for the closure task

1. [d5_249_master_status_after_G1.md](./d5_249_master_status_after_G1.md)
2. [d5_251_bundle_review_and_polish_note.md](./d5_251_bundle_review_and_polish_note.md)
3. [../tex/d5_251_full_d5_working_manuscript_refined.tex](../tex/d5_251_full_d5_working_manuscript_refined.tex)
4. the post-entry packet support notes `233`, `131`, `137`, `197`, `133`
5. the graph/globalization packet notes `234`, `236`, `245`, `247`, `082`,
   `083`, `099`, `121`, `122`, `123`, `130`

## 6. Bottom line

The promoted `251` slice exhausted the live theorem frontier inside
`T0--T4, G1, G2`.

So the remaining odd-`m`, `d=5` proof task is no longer “discover a new local
mechanism.” It is:

- package the post-entry odometer block cleanly;
- package the final graph-side/globalization block cleanly;
- then decide whether those blocks should remain imported or be internalized
  into one final manuscript.
