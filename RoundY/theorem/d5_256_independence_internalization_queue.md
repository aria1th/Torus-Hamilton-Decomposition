# D5 256 Independence Internalization Queue

This note records the work that can proceed **without waiting** for the final
resonant residual theorem.

The point is to separate:

- the still-live residual graph-side theorem work;
- from the documentation/internalization work that is already ready to move.

The older honesty boundary is summarized in:

- [d5_255_transport_honesty_boundary.md](./d5_255_transport_honesty_boundary.md)

The later current frontier memo is:

- [d5_284_current_working_frontier_after_nonresonant_closure.md](./d5_284_current_working_frontier_after_nonresonant_closure.md)

Historical narrowing ladder:

- [d5_257_selstar_color3_routee_probe.md](./d5_257_selstar_color3_routee_probe.md)
  and
- [d5_258_selstar_color3_section_stitch.md](./d5_258_selstar_color3_section_stitch.md)
- [d5_260_selstar_color3_row_model_all_m.md](./d5_260_selstar_color3_row_model_all_m.md)
- [d5_261_selstar_color3_section_model_all_m.md](./d5_261_selstar_color3_section_model_all_m.md)
- [d5_262_selstar_color3_B0_return_formula.md](./d5_262_selstar_color3_B0_return_formula.md)
- [d5_263_selstar_color3_section_model_stitching.md](./d5_263_selstar_color3_section_model_stitching.md)
- [d5_264_selstar_color3_actual_P0_return_formula.md](./d5_264_selstar_color3_actual_P0_return_formula.md)
- [d5_265_selstar_color3_actual_section_identification.md](./d5_265_selstar_color3_actual_section_identification.md)
- [d5_266_selstar_color3_hamilton_theorem.md](./d5_266_selstar_color3_hamilton_theorem.md)
- [d5_275_routee_color2_residual_probe.md](./d5_275_routee_color2_residual_probe.md)
- [d5_276_routee_color2_short_cycle_structure.md](./d5_276_routee_color2_short_cycle_structure.md)
- [d5_277_routee_refined_family_search.md](./d5_277_routee_refined_family_search.md)
- [d5_278_routee_refined_family_large_odd_gate.md](./d5_278_routee_refined_family_large_odd_gate.md)
- [d5_279_one_point_repair_color2_closure.md](./d5_279_one_point_repair_color2_closure.md)
- [d5_280_one_point_repair_color1_line_obstruction.md](./d5_280_one_point_repair_color1_line_obstruction.md)
- [d5_281_routee_line_bit_search.md](./d5_281_routee_line_bit_search.md)

show how the frontier narrowed from the older five-color assembly language to
the current residual split. The later `284/285/286` memo now treats small odd
and nonresonant residual packets as closed working blocks and leaves a
narrower resonant residual program as the live theorem burden. Everything
below should be read with that current boundary in mind.

## 1. What is still pending

Two things are still pending.

### A. One remaining resonant residual theorem/program

The remaining live graph-side burden is now the resonant residual input:

- complete and package the remaining resonant residual theorem/program for odd
  `m >= 15` with `3 | m`, in the narrower width-`1` / width-`3` /
  promoted-collar / double-top / `B`-active-gate language recorded by the
  current `284/285/286` memo.

### B. Manuscript/internalization rewrite

In parallel, the top-level manuscript and companion still have to be kept
honest about that remaining input:

- keep the now-promoted `284/285/286` packet readable as the current top-level
  entry
- keep the older `267/268` layer clearly marked as historical boundary
- avoid freezing the final resonant theorem phrasing before that statement is
  actually settled

## 2. What is not blocked

The following work can proceed now.

### A. Literal object definitions

Current packet/manuscript language still uses theorem-order names for:

- `Q_th`
- `SelCorr`
- `SelStar`
- the explicit colorwise package `g0,...,g4`

Independent-proof task:

- write these as literal definitions in manuscript order
- isolate where each definition is fully expanded and where it is only cited

Natural sources:

- [d5_106_intended_quotient_identification_and_comparison.md](./d5_106_intended_quotient_identification_and_comparison.md)
- [d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex](./d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex)
- [d5_247_G1_explicit_two_swap_splice_note.tex](./d5_247_G1_explicit_two_swap_splice_note.tex)
- [d5_121_M5_corrected_row_stitching.md](./d5_121_M5_corrected_row_stitching.md)
- [d5_122_M5_all_odd_identification.md](./d5_122_M5_all_odd_identification.md)

### B. Packet-proof internalization

The packet statements are now theorem-order explicit, but the proofs still cite
earlier packet notes compactly.

Independent-proof task:

- decide which packet proofs should stay as short citations
- and which should be pulled directly into the main manuscript or appendix

Priority order:

1. post-entry odometer spine
2. `M23`
3. `M4`
4. `M5`
5. `M6`

### C. Citation-chain cleanup

Independent-proof task:

- make every load-bearing theorem use a stable RoundY citation chain first
- minimize dependence on `tmp/` provenance where a stable note now exists
- keep a separate provenance list only for arguments that still genuinely live
  in `tmp/`

### D. Certificate appendix planning

Several finite or checked facts are already stable enough to be organized as a
companion certificate layer.

Independent-proof task:

- identify which finite tables/checks need to be cited in the manuscript body
- and which should move to a certificate appendix or separate evidence bundle

Typical examples:

- finite seed certificate / shape certificate
- small odd `m=5,7,9` exact checks in the color-4 branch
- front-end row-family exact checkers

### E. Bundle and reader-facing documentation

Independent-proof task:

- keep one clean reader path for the current `284/285/286` manuscript +
  companion layer
- keep one clean reader path for the older narrowing ladder `267–281`
- distinguish “current frontier”, “historical narrowing ladder”, “accepted
  background”, and “proof-support bundle” explicitly

## 3. Recommended order

The best low-risk order is:

1. stabilize the current frontier memo / manuscript / companion layer
2. keep the historical honesty-boundary notes clearly labeled as such
3. literalize the named quotient/selector objects
4. build a compact packet-proof citation appendix
5. separate stable citations from tmp-only provenance
6. package a cleaner independent-proof bundle around that stabilized structure

## 4. Practical promotion targets

The most natural stable promotion targets after `255` are:

- the current frontier memo/manuscript/companion layer in `284/285/286`
- the historical honesty-boundary notes in `255/268`
- this queue note itself
- any later appendix-style note that literally defines `Q_th`, `SelCorr`,
  `SelStar`, and the explicit `g_i`

## 5. Bottom line

The old transport route is out, the replacement color-`3` Route-E line is
closed, and the current frontier has now been narrowed further by the
`0326` memo promotion.

What remains is not broad graph-side search but one resonant residual theorem
program together with the documentation/internalization work around it.
