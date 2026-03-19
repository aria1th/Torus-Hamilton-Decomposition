# D5 094 Remaining tmp Priority Map

This note records the remaining `tmp/` files that still matter after the main
`076–083` promotion pass. The point is to separate:

- files that should now be promoted,
- files whose mathematical content is already absorbed into stable notes,
- files that should remain provenance only,
- and files that are outside the RoundY D5 theorem chain.

## 0. Current active tmp frontier

The active tmp frontier has moved beyond the old `076–083` promotion backlog.
The main live tmp notes are now:

- `tmp/d5_116_slice4_transport_formula_note.tex`
- `tmp/d5_117_M4_corrected_selector_theorem.tex`
- `tmp/d5_118_M4_G4prime_M6_note.tex`

The later M5 notes `tmp/d5_121_M5_corrected_row_stitching_note.tex` and
`tmp/d5_122_M5_all_odd_identification_note.tex` are no longer part of this
active tmp frontier; they have now been promoted into stable RoundY theorem
notes.

These are not “promote now verbatim” files yet. Their current role is:

- `116`: proposes the explicit exact slice-4 transport field
  `F4sharp = (B2,B3,B4,Z,O,M)`;
- `117`: proposes a direct corrected-selector theorem closing M4 on the full
  torus for odd `m >= 5`;
- `118`: repackages the downstream interpretation, arguing that if `117` is
  accepted then M4 and M6 are no longer the live graph-level burden and M5 is
  the next package.

The earlier `112–115` notes remain important provenance for how the old raw-row
and slice-4 bottlenecks were isolated and then replaced, but `116–118` are the
current live graph-theoretic todo notes, not absorbed historical leftovers.

## 1. Promote now

No urgent promotion remains from this shortlist. The latest high-value cleanup
notes from the previous pass have now been promoted:

- `tmp/d5_092_cleaned_independent_theorem_suite.tex`
  -> [d5_092_cleaned_independent_theorem_suite.tex](./d5_092_cleaned_independent_theorem_suite.tex)
- `tmp/d5_095_compact_reproof_079_chart_interface_landing.md/.tex`
  -> [d5_095_compact_reproof_079_chart_interface_landing.md](./d5_095_compact_reproof_079_chart_interface_landing.md)
     and
     [d5_095_compact_reproof_079_chart_interface_landing.tex](./d5_095_compact_reproof_079_chart_interface_landing.tex)
- `tmp/d5_096_compact_reproof_081_regular_closure.md/.tex`
  -> [d5_096_compact_reproof_081_regular_closure.md](./d5_096_compact_reproof_081_regular_closure.md)
     and
     [d5_096_compact_reproof_081_regular_closure.tex](./d5_096_compact_reproof_081_regular_closure.tex)
- `tmp/d5_097_compact_reproof_077_tail_length_reduction.md/.tex`
  -> [d5_097_compact_reproof_077_tail_length_reduction.md](./d5_097_compact_reproof_077_tail_length_reduction.md)
     and
     [d5_097_compact_reproof_077_tail_length_reduction.tex](./d5_097_compact_reproof_077_tail_length_reduction.tex)
- `tmp/d5_098_compact_cleanup_033_062_structural_block.md/.tex`
  -> [d5_098_compact_cleanup_033_062_structural_block.md](./d5_098_compact_cleanup_033_062_structural_block.md)
     and
     [d5_098_compact_cleanup_033_062_structural_block.tex](./d5_098_compact_cleanup_033_062_structural_block.tex)
- `tmp/d5_121_M5_corrected_row_stitching_note.tex`
  -> [d5_121_M5_corrected_row_stitching.md](./d5_121_M5_corrected_row_stitching.md)
     and
     [d5_121_M5_corrected_row_stitching.tex](./d5_121_M5_corrected_row_stitching.tex)
- `tmp/d5_122_M5_all_odd_identification_note.tex`
  -> [d5_122_M5_all_odd_identification.md](./d5_122_M5_all_odd_identification.md)
     and
     [d5_122_M5_all_odd_identification.tex](./d5_122_M5_all_odd_identification.tex)

## 2. Important historical provenance, but already absorbed

These files are still mathematically meaningful, but their substance is already
represented by later stable notes. They should be documented and cited only as
provenance, not promoted again verbatim.

- `tmp/d5_076_track_c_compute.md`
  Importance: `medium`
  What it adds:
  Early concrete-bridge compute framing, especially the exact nature of
  fixed-`delta` ambiguity on proxy unions.
  Stable replacement:
  [d5_077_tail_length_and_actual_union.md](./d5_077_tail_length_and_actual_union.md),
  [d5_078_large_modulus_regular_union_support.md](./d5_078_large_modulus_regular_union_support.md),
  and
  [d5_082_frontier_and_theorem_map.md](./d5_082_frontier_and_theorem_map.md).

- `tmp/077_d5_trackC_work_20260314.md`
  Importance: `medium`
  What it adds:
  The first clear statement that repeated `delta` ambiguity looked terminal-only
  on the actual frozen anchors and that the real missing object was the splice
  graph / component decomposition.
  Stable replacement:
  [d5_077_tail_length_and_actual_union.md](./d5_077_tail_length_and_actual_union.md)
  and
  [d5_078_endpoint_compatibility_criterion.md](./d5_078_endpoint_compatibility_criterion.md).

- `tmp/d5_091_independent_package_gap_note_rewrite_20260314.md`
  Importance: `medium`
  What it adds:
  The best drafting source for the gap note that separates an accepted package
  from a fully independent theorem package.
  Stable replacement:
  [d5_091_independent_package_gap_note.md](./d5_091_independent_package_gap_note.md).

- `tmp/d5_091_independent_package_gap_note_rewrite_20260314.tex`
  Importance: `medium`
  What it adds:
  TeX source for the same independent-package gap note.
  Stable replacement:
  [d5_091_independent_package_gap_note.tex](./d5_091_independent_package_gap_note.tex).

## 3. Stable note already exists; tmp should not be cited

These files are already fully promoted or intentionally summarized elsewhere.

- `tmp/d5_076_bridge_main.md`
- `tmp/d5_076_realization_trackB.md`
- `tmp/d5_076_concrete_bridge_proof.md`
- `tmp/d5_078_rA.md`
- `tmp/d5_078_rB.md`
- `tmp/d5_078_rC.md`
- `tmp/d5_078_rD.md`
- `tmp/d5_080_a.md`
- `tmp/d5_081_4.2.md`
- `tmp/d5_081_5.0.md`
- `tmp/d5_081_6.0_rC_targeted_compute.md`
- `tmp/d5_081b_082_actual_lift_end_gluing_reduction.md`
- `tmp/d5_083_final_theorem_proof.md`
- `tmp/d5_092_cleaned_independent_theorem_suite.md`

Use the stable RoundY theorem copy instead.

## 4. Duplicates or intermediate proof variants

These are useful for provenance but should not be promoted again.

- `tmp/scratches/d5_083_proof_note.md`
  Importance: `low`
  Status:
  Intermediate reduction note. Final role is absorbed by
  [d5_083_gluing_flow_and_final_theorem.md](./d5_083_gluing_flow_and_final_theorem.md)
  and
  [d5_083_final_theorem_proof.md](./d5_083_final_theorem_proof.md).

- `tmp/scratches/d5_083_final_proof_a.md`
  Importance: `low`
  Status:
  Attractive intermediate variant, but not the canonical final proof.

- `tmp/scratches/d5_083_final_gluing_theorem_proof.md`
  Importance: `low`
  Status:
  Parallel proof variant; final theorem now cited through the promoted `083`
  theorem note.

- `tmp/scratches/d5_073_duplicate_handoff.md`
  Importance: `low`
  Status:
  Duplicate handoff.

- `tmp/scratches/d5_response_061.b.md`
  Importance: `low`
  Status:
  Scratch response, not a theorem note.

## 5. Outside the RoundY D5 theorem chain

These should stay outside the D5 promotion pipeline.

- `tmp/scratches/square_product_hamilton_lift.tex`
  Importance: `medium`
  Status:
  A real theorem note, but it is a general square-product lift for Hamilton
  decompositions, not a RoundY D5 bridge/globalization note. If adopted, it
  should be promoted under a broader top-level theorem area, not folded into
  the D5 odd-`m` chain.

- `tmp/scratches/test_dispatch.lean`
  Importance: `low`
  Status:
  Formal scratch file, not part of the stable RoundY theorem notes.

## 6. Recommended citation rule

For any argument already represented in a stable RoundY theorem note:

- cite the stable note first;
- mention the `tmp/` source only if provenance matters; and
- do not mix `tmp/` and stable references in the same theorem dependency chain
  unless the stable note explicitly says a distinct argument still lives only in
  the original.
