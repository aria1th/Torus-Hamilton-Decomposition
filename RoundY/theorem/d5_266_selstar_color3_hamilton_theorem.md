# D5 266 SelStar Color-3 Hamilton Theorem

This note closes the live `Sel*` color-`3` graph-side Route-E line.

Primary inputs:

- [d5_264_selstar_color3_actual_P0_return_formula.md](./d5_264_selstar_color3_actual_P0_return_formula.md)
- [d5_265_selstar_color3_actual_section_identification.md](./d5_265_selstar_color3_actual_section_identification.md)
- [d5_263_selstar_color3_section_model_stitching.md](./d5_263_selstar_color3_section_model_stitching.md)
- [d5_259_selstar_color3_all_m_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_259_selstar_color3_all_m_summary.json)

## 1. Theorem

For every `m > 2`, the color-`3` torus map induced by `Sel*` is Hamilton on
`D_5(m)`.

In particular, for every odd `m >= 5`, the `Sel*` color-`3` branch is closed.

## 2. Proof for `m >= 9`

Let `F_3^*` be the color-`3` torus map, let

- `P0 = {Sigma = 0}`,
- `R_3^* = (F_3^*)^m | P0`,
- `S_m = {x in P0 : x_2 = m-2}`,
- `T_m = (R_3^*)^m | S_m`.

By `264`, under `R_3^*` the coordinate `x_2` increases by `1` everywhere on
`P0`. Hence every `R_3^*` orbit meets `S_m`, and the first return to `S_m` is
exactly `T_m`.

By `265`, the actual section map `T_m` agrees exactly with the explicit model
`T_m^sharp`. By `263`, that explicit model is one `m^3`-cycle. Therefore

- `T_m` is one `m^3`-cycle on `S_m`.

Since every `R_3^*` orbit meets `S_m` and the global first return on `S_m` is
one cycle, `R_3^*` itself is one `m^4`-cycle on `P0`.

Now pass back to the full torus map `F_3^*`. Every `F_3^*` step raises the
total sum `Sigma` by `1`, so every orbit meets `P0`, and the first return to
`P0` is exactly `R_3^*`. Since `R_3^*` is one `m^4`-cycle, the same stitching
argument implies that `F_3^*` is one `m^5`-cycle on the full torus.

Thus `F_3^*` is Hamilton for every `m >= 9`.

## 3. Small moduli

The direct replay in `259` checks the full torus color-`3` map itself for

- `m = 3,4,5,6,7,8`,

and finds a single `m^5`-cycle in every case.

So the theorem holds for every `m > 2`.

## 4. Consequence for the D5 frontier

The actual `Sel*` color-`3` branch is now closed:

- the old `G1 -> G2` transport route is still a no-go for the present explicit
  package;
- but the replacement Route-E line for the actual `Sel*` color-`3` branch is
  now complete.

This does **not** by itself close the whole graph-side endgame.
The remaining graph-side burden is now sharper:

- the color-`4` branch is closed;
- the color-`3` branch is closed;
- but a five-color assembly theorem still remains.

Later note `269` sharpens that further by showing that the current `Sel*`
colors `1` and `2` already preserve simple `P0` first-return invariants, so
they cannot themselves be the missing Hamilton assembly colors.
