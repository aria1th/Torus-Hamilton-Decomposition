# D5 272 Route-E Assembly Bundle Requirements

This short spec records what should go into the next external researcher bundle
if the goal is:

- explain the current odd-`m`, `d=5` proof flow,
- isolate the one remaining graph-side issue,
- and hand off the live Route-E-style assembly problem with the sharpest known
  no-go results.

## 1. Core narrative documents

- [d5_267_full_d5_working_manuscript_routee_honest.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/tex/d5_267_full_d5_working_manuscript_routee_honest.tex)
- [d5_268_five_color_assembly_boundary.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_268_five_color_assembly_boundary.md)
- [d5_255_transport_honesty_boundary.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_255_transport_honesty_boundary.md)

## 2. Closed graph-side branches that must be treated as inputs

- [d5_121_M5_corrected_row_stitching.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_121_M5_corrected_row_stitching.md)
- [d5_122_M5_all_odd_identification.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_122_M5_all_odd_identification.md)
- [d5_257_selstar_color3_routee_probe.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_257_selstar_color3_routee_probe.md)
- [d5_258_selstar_color3_section_stitch.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_258_selstar_color3_section_stitch.md)
- [d5_260_selstar_color3_row_model_all_m.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_260_selstar_color3_row_model_all_m.md)
- [d5_261_selstar_color3_section_model_all_m.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_261_selstar_color3_section_model_all_m.md)
- [d5_262_selstar_color3_B0_return_formula.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_262_selstar_color3_B0_return_formula.md)
- [d5_263_selstar_color3_section_model_stitching.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_263_selstar_color3_section_model_stitching.md)
- [d5_264_selstar_color3_actual_P0_return_formula.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_264_selstar_color3_actual_P0_return_formula.md)
- [d5_265_selstar_color3_actual_section_identification.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_265_selstar_color3_actual_section_identification.md)
- [d5_266_selstar_color3_hamilton_theorem.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_266_selstar_color3_hamilton_theorem.md)

## 3. Live no-go / narrowing results for the remaining theorem

- [d5_269_selstar_color12_return_invariant_obstruction.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_269_selstar_color12_return_invariant_obstruction.md)
- [d5_270_five_color_slice_ordering_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_270_five_color_slice_ordering_no_go.md)
- [d5_271_five_color_coarse_defect_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_271_five_color_coarse_defect_no_go.md)

## 4. Historical crosswalk needed to explain why old G1/G2 is not the answer

- [d5_234_graph_side_split_G2_closed_G1_remaining_note.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_234_graph_side_split_G2_closed_G1_remaining_note.tex)
- [d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex)
- [d5_247_G1_explicit_two_swap_splice_note.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_247_G1_explicit_two_swap_splice_note.tex)

## 5. Scripts and checks that should accompany the note chain

- [torus_nd_d5_selector_star_common_119.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selector_star_common_119.py)
- [torus_nd_d5_selstar_color12_return_invariants_269.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selstar_color12_return_invariants_269.py)
- [torus_nd_d5_five_color_slice_ordering_search_270.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_five_color_slice_ordering_search_270.py)
- [torus_nd_d5_five_color_coarse_defect_no_go_271.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_five_color_coarse_defect_no_go_271.py)
- [torus_nd_d5_selstar_color3_actual_identification_264.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selstar_color3_actual_identification_264.py)
- [torus_nd_d5_selstar_color3_section_model_261.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selstar_color3_section_model_261.py)
- [torus_nd_d5_selstar_color3_row_model_260.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selstar_color3_row_model_260.py)

## 6. Optional but useful comparative context

- [d5_119_next_compute_request_selector_star.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/tmp/d5_119_next_compute_request_selector_star.md)
- D3 Route-E formal references already used in the prior researcher bundle

## 7. Bottom line

If the next bundle is meant for a fresh researcher, it should explain three
things in order:

1. the main odd-`m`, `d=5` proof is now paper-readable and only one graph-side
   theorem remains;
2. the closed color-`3` and color-`4` branches should be treated as fixed
   inputs, not as open work;
3. the remaining theorem is already known to lie outside the raw Sel* package,
   outside slice-only completions, and outside the historical defect-bit coarse
   family.
