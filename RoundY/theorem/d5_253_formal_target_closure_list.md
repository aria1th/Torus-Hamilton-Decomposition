# D5 253 Formal Target Closure List

Historical note:

- this note records the formal-target list relative to the `252` manuscript
  boundary;
- the later `255` pass keeps the packet-closure progress but sharpens the final
  honest boundary by isolating the remaining graph-side
  `G1 -> G2` transport-compatibility step;
- for the current state, read this note together with
  [d5_255_transport_honesty_boundary.md](./d5_255_transport_honesty_boundary.md)
  and
  [d5_256_independence_internalization_queue.md](./d5_256_independence_internalization_queue.md).

This note records the shortest honest answer to:

> what still has to be closed as an explicit formal target before the odd-`m`,
> `d=5` proof can be treated as a self-contained formal proof rather than a
> theorem-order manuscript with named upstream packets?

It is written relative to the closed `252` manuscript bundle:

- [../../tmp/d5_252_main_manuscript_bundle_extract/d5_252_main_manuscript_bundle/manuscript/d5_252_full_d5_working_manuscript_closed.tex](../../tmp/d5_252_main_manuscript_bundle_extract/d5_252_main_manuscript_bundle/manuscript/d5_252_full_d5_working_manuscript_closed.tex)
- [../../tmp/d5_252_main_manuscript_bundle_extract/d5_252_main_manuscript_bundle/overview/d5_252_main_manuscript_closure_note.md](../../tmp/d5_252_main_manuscript_bundle_extract/d5_252_main_manuscript_bundle/overview/d5_252_main_manuscript_closure_note.md)

It should be read together with:

- [d5_252_odd_m_remaining_closure_map.md](./d5_252_odd_m_remaining_closure_map.md)
- [../../formal/TorusD5/THEOREM_TARGETS.md](../../formal/TorusD5/THEOREM_TARGETS.md)

## 1. What `252` already closes

At theorem order, the `252` manuscript is already linear enough to support a
single final proof.

The closed slice inside the manuscript is:

- finite seed certificate and bridge normalization
- `T0` actual-needed tiny-repair core
- `T1`, `T2`, `T3`
- `T4` canonical entry
- `G1` explicit selector splice
- `G2` cyclic transport
- corrected final upgrade theorem

The best short status notes for that closed slice are:

- [d5_249_master_status_after_G1.md](./d5_249_master_status_after_G1.md)
- [d5_251_bundle_review_and_polish_note.md](./d5_251_bundle_review_and_polish_note.md)

So the remaining formal work is not “find another missing local theorem inside
`T0--T4, G1, G2`.” It is: turn the remaining named upstream packets into
explicit formal targets with definitions and proofs.

## 2. Why `252` is not yet self-contained as a formal proof

The `252` manuscript states the final theorem unconditionally, but its proof
still uses named upstream packets.

The key places are:

- `thm:odometer-spine` in the manuscript, proved by citing the one-pass
  globalization package rather than by first-principles proof in the file
- standing theorem packets
  `thm:M23`, `thm:M4-SelCorr`, `thm:M5-color4`, `thm:M6-globalization`
- graph-side objects such as `SelCorr` and `SelStar`, which are used at theorem
  order but not defined in the manuscript itself

So the right formal question is not whether the main theorem statement exists.
It does. The question is which imported theorem objects still have to be made
literal in a definition-and-proof chain.

## 3. Minimal formal-target boundary

A self-contained formal odd-`m`, `d=5` package needs the following objects to
exist as explicit definitions and theorems, not only as manuscript-order names.

### A. Core objects and interfaces

These are the objects that later theorems must quantify over explicitly.

- the directed torus `D_5(m)` and its five color maps
- the canonical seed and canonical entry state
- the one-corner section coordinates and current-event map
- the theorem-side quotient objects
  `(rho, beta, q0, sigma)`, `(B, beta)`, and `(beta, delta)`
- the graph-side selector families `SelCorr` and `SelStar`
- the colorwise selector package `g0, ..., g4`

Formal completion condition:

- later theorems no longer depend on manuscript macros or prose names
- each downstream theorem can be stated in terms of these explicit objects

This layer should land on the abstract D5 interfaces already targeted in:

- [../../formal/TorusD5/THEOREM_TARGETS.md](../../formal/TorusD5/THEOREM_TARGETS.md)

## 4. Dependency-ordered formal targets

The remaining formal targets are best organized in the following order.

### 4.1 Front-end finite block

This block is theorem-order closed already, but it still has to be formalized if
the goal is a fully formal final theorem.

The relevant targets are:

- finite seed certificate
- bridge normalization
- `T0` actual-needed repair core
- `T1`, `T2`, `T3`
- `T4` canonical entry

Useful stabilized sources:

- [../tex/d5_251_full_d5_working_manuscript_refined.tex](../tex/d5_251_full_d5_working_manuscript_refined.tex)
- [d5_249_master_status_after_G1.md](./d5_249_master_status_after_G1.md)

Formal role:

- close the front end through canonical entry without importing the later
  odometer packet

### 4.2 Post-entry odometer spine

This is the first genuinely imported theorem packet in `252`.

The target theorem is the manuscript object:

- `thm:odometer-spine`

Mathematical content to formalize:

- after canonical entry, the actual active branch agrees with the candidate
  one-corner orbit up to first exit
- the trigger family is explicit
- the universal regular and exceptional exits are explicit
- no patched current class appears before exit

Current source chain:

- [d5_133_one_corner_front_end_reduction_note.tex](./d5_133_one_corner_front_end_reduction_note.tex)
- [d5_137_shape_certificate_extraction.md](./d5_137_shape_certificate_extraction.md)
- [d5_197_sigma23_r1_microstate_check.md](./d5_197_sigma23_r1_microstate_check.md)
- [d5_099_one_pass_odd_m_globalization_package.md](./d5_099_one_pass_odd_m_globalization_package.md)

Formal landing points inside the D5 model layer:

- section parameterization
- witness first return
- grouped return
- skew-product projection

Those correspond exactly to the interface plan in:

- [../../formal/TorusD5/THEOREM_TARGETS.md](../../formal/TorusD5/THEOREM_TARGETS.md)

### 4.3 Theorem-side `M2/M3` anchor package

This is the second essential imported packet.

The target theorem is:

- `thm:M23`

Mathematical content to formalize:

- existence of the exact marked carry-jump-to-wrap object
- exact deterministic quotient structure for `(B, beta)`
- grouped-base retention
- canonical factor to `(beta, delta)`

Current source chain:

- [d5_106_intended_quotient_identification_and_comparison.md](./d5_106_intended_quotient_identification_and_comparison.md)
- [d5_130_revised_consolidated_manuscript_after_M1_review.tex](./d5_130_revised_consolidated_manuscript_after_M1_review.tex)
- [../../tmp/d5_105_odd_m_marked_chain_descent_note.tex](../../tmp/d5_105_odd_m_marked_chain_descent_note.tex)
- [../../tmp/d5_107_M3_comparison_theorem.tex](../../tmp/d5_107_M3_comparison_theorem.tex)
- [../../tmp/d5_124_M1_M6_proof_closure_draft.tex](../../tmp/d5_124_M1_M6_proof_closure_draft.tex)
- [../../tmp/d5_125_corrected_M2_M3_anchor_package_note.tex](../../tmp/d5_125_corrected_M2_M3_anchor_package_note.tex)
- [../../tmp/d5_126_intended_quotient_verification_note.tex](../../tmp/d5_126_intended_quotient_verification_note.tex)
- [../../tmp/d5_126_local_provenance_compute_request.md](../../tmp/d5_126_local_provenance_compute_request.md)
- [d5_127_local_provenance_compare.md](./d5_127_local_provenance_compare.md)

Formal completion condition:

- the theorem-side quotient is stated and proved directly against the abstract
  `ExactQuotient`-style interface rather than only compared informally with
  checked dynamic models

### 4.4 Corrected-selector baseline

This is the graph-side baseline theorem that must exist before the splice and
transport block can be treated as purely downstream.

The target theorem is:

- `thm:M4-SelCorr`

Mathematical content to formalize:

- explicit definition of `SelCorr`
- proof that `SelCorr` gives five global torus permutations
- pairwise arc-disjointness
- full outgoing arc coverage

Current source chain:

- [../../tmp/d5_116_slice4_transport_formula_note.tex](../../tmp/d5_116_slice4_transport_formula_note.tex)
- [../../tmp/d5_117_M4_corrected_selector_theorem.tex](../../tmp/d5_117_M4_corrected_selector_theorem.tex)
- [../../tmp/d5_118_M4_G4prime_M6_note.tex](../../tmp/d5_118_M4_G4prime_M6_note.tex)

Formal completion condition:

- `SelCorr` is no longer only a manuscript-side family name; it is a literal
  torus selector object with the expected permutation package theorem

### 4.5 Color-4 `SelStar` Hamilton branch

This is the already-closed branch that the downstream splice package uses as
its Hamilton base case.

The target theorem is:

- `thm:M5-color4`

Mathematical content to formalize:

- explicit definition of the color-4 map induced by `SelStar`
- corrected-row model
- all-odd identification of the actual third return with the corrected-row
  model
- Hamiltonicity of the resulting torus map

Current source chain:

- [../../tmp/d5_119_M5_return_and_selector_surgery_note.tex](../../tmp/d5_119_M5_return_and_selector_surgery_note.tex)
- [d5_121_M5_corrected_row_stitching.md](./d5_121_M5_corrected_row_stitching.md)
- [d5_122_M5_all_odd_identification.md](./d5_122_M5_all_odd_identification.md)
- [d5_123_M_route_status_after_122.md](./d5_123_M_route_status_after_122.md)

Formal completion condition:

- the color-4 Hamilton branch becomes a proved theorem over explicit torus maps
  rather than a named imported branch

### 4.6 Odd-`m` globalization packet

This is the last theorem-side imported packet.

The target theorem is:

- `thm:M6-globalization`

Mathematical content to formalize:

- every actual exceptional cutoff lift continues through `3m-2 -> 3m-1`
- no mixed-status realized `delta`
- fixed realized `delta` determines tail length and endpoint class
- raw global `(beta, delta)` exactness on the true accessible boundary union

Current source chain:

- [d5_082_frontier_and_theorem_map.md](./d5_082_frontier_and_theorem_map.md)
- [d5_083_gluing_flow_and_final_theorem.md](./d5_083_gluing_flow_and_final_theorem.md)
- [d5_083_final_theorem_proof.md](./d5_083_final_theorem_proof.md)
- [d5_099_one_pass_odd_m_globalization_package.md](./d5_099_one_pass_odd_m_globalization_package.md)

Formal completion condition:

- the globalization step becomes a proved theorem over the explicit theorem-side
  quotient objects instead of a cited manuscript package

### 4.7 Graph-side splice and transport block

This block is mathematically closed in the present slice, but for a fully formal
end-to-end theorem it still has to be formalized on top of `M4`, `M5`, and the
explicit selector definitions.

The target theorems are:

- `G1` splice compatibility theorem
- `G2` cyclic transport theorem
- colorwise selector package corollary
- all-five-Hamilton corollary

Current source chain:

- [d5_234_graph_side_split_G2_closed_G1_remaining_note.tex](./d5_234_graph_side_split_G2_closed_G1_remaining_note.tex)
- [d5_236_G1_finite_defect_splice_principle_note.tex](./d5_236_G1_finite_defect_splice_principle_note.tex)
- [d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex](./d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex)
- [d5_247_G1_explicit_two_swap_splice_note.tex](./d5_247_G1_explicit_two_swap_splice_note.tex)
- [d5_249_master_status_after_G1.md](./d5_249_master_status_after_G1.md)

Formal completion condition:

- `G1` and `G2` are proved over explicit torus selectors, with the color-4
  branch identified literally as the formal `SelStar` branch

### 4.8 Final upgrade and main theorem

Once the layers above are formalized, the end of the manuscript should be short.

The remaining formal targets are:

- corrected generic upgrade criterion
- main odd-`m`, `d=5` Hamilton decomposition theorem

These are downstream assembly theorems, not new mathematical frontier objects.

## 5. Short list of the true remaining formal targets

If the goal is only to know which currently externalized objects prevent `252`
from already being a self-contained formal proof, the answer is short:

1. explicit core definitions for the imported quotient and selector objects
2. the post-entry odometer spine
3. `M23`
4. `M4-SelCorr`
5. `M5-color4`
6. `M6-globalization`

Everything else in the `252` main proof is now downstream packaging on top of
those objects together with the already-closed `T0--T4, G1, G2` slice.

## 6. Recommended formalization order

The lowest-risk order is:

1. freeze the formal definitions of the quotient objects and selector objects
2. formalize the post-entry odometer spine against the existing abstract D5
   model layer
3. formalize `M23` as the theorem-side exact-quotient landing theorem
4. formalize `M4-SelCorr`
5. formalize `M5-color4`
6. formalize `M6-globalization`
7. formalize `G1`, `G2`, the all-five-Hamilton corollary, the generic upgrade,
   and the main theorem

Parallelizable split:

- odometer and quotient side:
  post-entry spine, `M23`, `M6`
- graph side:
  `SelCorr`, `SelStar`, `M4`, `M5`, `G1`, `G2`

## 7. Bottom line

The `252` manuscript is already a good theorem-order roadmap for Leanization,
but it is not yet a first-principles formal closure.

The honest formal target is therefore not “formalize the whole manuscript at
once.” It is:

- make the imported objects literal,
- close the six remaining external theorem packets,
- then replay the already short `252` endgame formally.
