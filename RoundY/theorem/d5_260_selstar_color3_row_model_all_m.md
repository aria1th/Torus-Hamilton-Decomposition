# D5 260 SelStar Color-3 All-m Row Model

This note isolates the first all-`m` theorem currently available on the live
`Sel*` color-`3` route.

Primary artifacts:

- [d5_258_selstar_color3_section_stitch.md](./d5_258_selstar_color3_section_stitch.md)
- [d5_259_selstar_color3_all_m_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_259_selstar_color3_all_m_summary.json)
- [torus_nd_d5_selstar_color3_row_model_260.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selstar_color3_row_model_260.py)
- [d5_260_selstar_color3_row_model_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_260_selstar_color3_row_model_summary.json)
- [actual_per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_260_selstar_color3_row_model/actual_per_modulus.json)
- [model_per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_260_selstar_color3_row_model/model_per_modulus.json)

## 1. Purpose

`258` identified an exact checked five-branch section law for the color-`3`
section map

- `T_m` on section coordinates `(a,b,e)`.

The remaining symbolic issue in that route is not the cycle structure of the
resulting row model. That part can already be proved for all large `m`.

This note records that row-model theorem.

## 2. The row-return model

Inside the five-branch section model from `258`, take the row section

- `B0 = {b = 0}`.

For `m >= 9`, define the explicit row-return model

- `W_m : (Z/mZ)^2 -> (Z/mZ)^2`

on coordinates `(a,e)` by:

- if `a <= m-3`, then `W_m(a,e) = (a+1,e)`;
- if `a = m-2` and `e = 5`, then `W_m(a,e) = (m-1,5)`;
- if `a = m-2` and `e = m-3`, then `W_m(a,e) = (0,m-1)`;
- if `a = m-2` and `e = m-2`, then `W_m(a,e) = (0,6)`;
- if `a = m-2` and `e` is different from `5,m-3,m-2`, then
  `W_m(a,e) = (0,e+1)`;
- if `a = m-1` and `e = 4`, then `W_m(a,e) = (0,m-2)`;
- if `a = m-1` and `e != 4`, then `W_m(a,e) = (m-1,e+1)`.

All coordinates are taken mod `m`.

## 3. Theorem

For every `m >= 9`, the explicit row-return model `W_m` is one `m^2`-cycle.

## 4. Proof

Write

- `C_e = {(a,e) : 0 <= a <= m-2}` for the non-top column at fixed `e`,
- `H = {(m-1,e) : e in Z/mZ}` for the top row.

From the definition of `W_m`:

- on every `C_e` with `e notin {5,m-3,m-2}`, the map runs straight upward
  through `a = 0,1,...,m-2` and exits to the bottom of `C_{e+1}`;
- on `C_5`, the map runs upward through `a = 0,1,...,m-2` and then exits to
  `(m-1,5)`, the entry point of the top row `H`;
- on `H`, the map runs horizontally
  `5 -> 6 -> ... -> m-1 -> 0 -> 1 -> 2 -> 3 -> 4`
  and then exits from `(m-1,4)` to the bottom of `C_{m-2}`;
- on `C_{m-2}`, the map runs upward and exits from `(m-2,m-2)` to the bottom
  of `C_6`;
- on `C_{m-3}`, the map runs upward and exits from `(m-2,m-3)` to the bottom
  of `C_{m-1}`;
- on `C_{m-1}`, the map runs upward and exits from `(m-2,m-1)` to `(0,0)`.

So the orbit of `(0,0)` is forced to pass through the disjoint blocks in the
following order:

1. `C_0`
2. `C_1`
3. `C_2`
4. `C_3`
5. `C_4`
6. `C_5`
7. `H`
8. `C_{m-2}`
9. `C_6`
10. `C_7`
11. ...
12. `C_{m-4}`
13. `C_{m-3}`
14. `C_{m-1}`
15. back to `(0,0)`

These blocks are pairwise disjoint and their total size is

- `6(m-1) + m + (m-9)(m-1) + (m-1) + (m-1) = m^2`.

Therefore the orbit of `(0,0)` has length exactly `m^2`, so it contains every
state of `(Z/mZ)^2`. Hence `W_m` is one `m^2`-cycle.

## 5. Checked support against the actual D5 route

The new row-model checker establishes:

- the actual first return of the checked `258` section map to `B0` is itself a
  single `m^2`-cycle for every checked `m = 3,4,...,25`;
- for every checked `m = 9,10,...,25`, that actual row return agrees exactly
  with the explicit row model `W_m`;
- the explicit row model `W_m` is a single `m^2`-cycle for every checked
  `m = 9,10,...,401`.

So the cycle theorem is no longer the live uncertainty. The live uncertainty is
the symbolic identification step:

- prove that the actual `Sel*` color-`3` section return really equals the
  five-branch law from `258`, so that its induced `b = 0` first return equals
  the row model treated here.

## 6. Consequence

This gives the correct all-`m` theorem target for the live color-`3` route:

- not a cyclic transport theorem from the old `G1/G2` package,
- but a direct section-identification theorem whose row model is already
  globally understood.

In particular, once the actual section map is identified with the `258`
five-branch law, the remaining row-model cycle argument is already closed for all
`m >= 9`, with `m = 3,4,5,6,7,8` already closed by direct checked row-return
computation.
