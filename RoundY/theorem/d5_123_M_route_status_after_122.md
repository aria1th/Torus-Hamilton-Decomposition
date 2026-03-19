# D5 123 M-Route Status After 122

This note collects the current `M`-route picture after the promotion of
`121/122`.

## 1. Reading order

For the current graph-theoretic `M`-route package, the shortest useful reading
order is:

1. [d5_106_intended_quotient_identification_and_comparison.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_106_intended_quotient_identification_and_comparison.md)
2. [d5_111_m4_filled_tables_and_compression_gap.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_111_m4_filled_tables_and_compression_gap.md)
3. [d5_115_tiered_selector_execution_summary.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_115_tiered_selector_execution_summary.md)
4. [d5_118_corrected_selector_frontier_summary.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_118_corrected_selector_frontier_summary.md)
5. [d5_119_selector_star_first_return_factor_probe.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_119_selector_star_first_return_factor_probe.md)
6. [d5_120_final_section_U_corrected_row_model.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_120_final_section_U_corrected_row_model.md)
7. [d5_121_M5_corrected_row_stitching.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_121_M5_corrected_row_stitching.md)
8. [d5_122_M5_all_odd_identification.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_122_M5_all_odd_identification.md)

## 2. Status by route

`M1` channel classification:
still a separate theorem/compute package. The best evidence and gap map remain
outside the promoted M5 chain.

`M2/M3` marked-chain descent and intended quotient:
the bookkeeping target is now clear after `106`, but the theorem-side object is
still the exact deterministic quotient retaining grouped base, not bare
`(beta,delta)`.

`M4` corrected selector package:
the old raw-row compression route is dead. The live theorem candidate is the
corrected-selector package summarized in `118`, conditional on accepting the
`116/117` replacement.

`M5` return-cycle route:
for the live Sel* color-4 branch, the promoted chain `119 -> 120 -> 121 -> 122`
now closes the final-section return package on all odd moduli. The remaining
M5 burden is therefore no longer the final-section cycle theorem for that
branch.

`M6` globalization input:
still imported from the accepted odd-`m` globalization package. No new gap was
created here by the M-route work.

## 3. Main current message

After `122`, the graph-theoretic M-route picture is no longer “M5 is still a
completely open return-cycle problem.” The sharper statement is:

- the corrected-selector route still needs theorem-side acceptance at the M4
  level;
- but once that selector package is accepted, the color-4 Sel* M5 return route
  is already closed theorem-side through `120/121/122`;
- the remaining graph-theoretic frontier is therefore higher-level packaging:
  adopt the corrected selector package cleanly, integrate the closed color-4
  M5 route into the broader graph proof, and keep the other still-external
  graph packages explicit.
