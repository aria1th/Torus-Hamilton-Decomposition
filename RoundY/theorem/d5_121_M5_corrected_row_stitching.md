# D5 121 M5 Corrected-Row Stitching

This note promotes the row-stitching result from the tmp-121 package.

Primary artifacts:

- [d5_121_M5_corrected_row_stitching.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_121_M5_corrected_row_stitching.tex)
- [d5_121_M5_corrected_row_stitching_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_121_M5_corrected_row_stitching_summary.json)
- [torus_nd_d5_M5_corrected_row_stitching_121.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_M5_corrected_row_stitching_121.py)
- [d5_120_final_section_U_corrected_row_model.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_120_final_section_U_corrected_row_model.md)

## Statement

Let `U_m^sharp` be the explicit corrected-row model on

`S_m = (Z/mZ)^2`

introduced in `120`. Then for every odd `m >= 11`:

- the first return on row `a = 0` is exactly `t -> t - 2`;
- the row-0 first-return segments are pairwise disjoint;
- the sum of their lengths is exactly `m^2`;
- therefore `U_m^sharp` is one `m^2`-cycle.

This is the corrected-row stitching theorem for the final M5 section.

## Checked support

The promoted check reruns the model on every odd modulus

`m = 11,13,15,...,101`.

The summary JSON verifies simultaneously:

- the row-0 return law;
- the exact return-time distribution
  `1,1,10,m+2,...,m+2,2m-4`;
- pairwise disjointness of the first-return segments;
- coverage of all `m^2` states by those segments;
- Hamiltonicity of the corrected-row model itself.

So after `121`, the final-section problem is no longer “does the symbolic model
stitch?” It does. The remaining issue is only whether the actual return `U_m`
equals that model.

## Consequence

If the true third return

`U_m = (F_4^*)^(m^3)|P2`

agrees with the corrected-row model from `120`, then `U_m` is one cycle, and
the `120` nested-return reduction gives Hamiltonicity of the color-4 Sel*
torus map.
