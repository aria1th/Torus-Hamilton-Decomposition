# D5 122 M5 All-Odd Identification

This note promotes the all-odd identification step for the live color-4 M5
route.

Primary artifacts:

- [d5_122_M5_all_odd_identification.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_122_M5_all_odd_identification.tex)
- [d5_122_M5_all_odd_identification_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_122_M5_all_odd_identification_summary.json)
- [torus_nd_d5_M5_all_odd_identification_122.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_M5_all_odd_identification_122.py)
- [d5_121_M5_corrected_row_stitching.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_121_M5_corrected_row_stitching.md)

## Statement

For the color-4 map `F_4^*` of the explicit selector surgery `Sel*`, the actual
third return

`U_m = (F_4^*)^(m^3)|P2`

agrees, for every odd `m >= 11`, with the explicit corrected-row model from
`120/121`.

Equivalently:

- the exact second nested return `T_m` on `P1` has the symbolic formula stated
  in the promoted tex note;
- the induced natural row formula on `P2` is exact;
- after the correction `v = b + c_m(a)`, that natural row formula is exactly
  the corrected-row model `U_m^sharp`.

Since `121` proves that `U_m^sharp` is one cycle, the actual `U_m` is one cycle
for every odd `m >= 11`. Together with direct checks on `m = 5,7,9`, this
closes the current color-4 Sel* M5 route for all odd moduli.

## Checked support

The promoted summary JSON verifies:

- exact `T_m` formulas on `m = 11,13,15,17,19,21`;
- exact equality
  `actual U = T-formula U = natural row formula`
  on the same moduli;
- exact equality between the natural row formula and the corrected-row model on
  those moduli;
- one-cycle behavior of the corrected-row model on the same range;
- direct full-torus Hamiltonicity on the remaining small odd moduli
  `m = 5,7,9`.

So `122` is the actual/model identification theorem that `121` still left open.

## Consequence

Within the live Sel* route, the sequence

`120 -> 121 -> 122`

now gives a complete M5 closure for color `4` on odd `m`.
