# D5 264 SelStar Color-3 Actual `P0` Return Formula

This note closes the first genuinely actual theorem on the live `Sel*`
color-`3` Route-E line.

Primary artifacts:

- [torus_nd_d5_selstar_color3_actual_identification_264.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selstar_color3_actual_identification_264.py)
- [d5_264_selstar_color3_actual_identification_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_264_selstar_color3_actual_identification_summary.json)
- [per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_264_selstar_color3_actual_identification/per_modulus.json)

## 1. Setup

Let `F_3^*` be the color-`3` torus map induced by `Sel*`.

Inside the zero-sum slice

- `P0 = {x in (Z/mZ)^5 : x_0 + ... + x_4 = 0}`,

write

- `R_3^* = (F_3^*)^m | P0`.

## 2. Exact formula

For `x = (x_0,x_1,x_2,x_3,x_4) in P0`, define `d(x)` by:

1. if `x_2 = m-2`, `x_3 = m-1`, and `x_4 = m-2`, then `d(x) = 0`;
2. else if `x_2 = m-2`, `x_0 = m-1`, and `x_3 != m-1`, then `d(x) = 4`;
3. else if `x_2 = m-2`, then `d(x) = 1`;
4. else if `x_1 = m-1` and `x_4 = m-2`, then `d(x) = 0`;
5. else `d(x) = 3`.

Then

- `R_3^*(x) = x + e_4 + e_2 + e_{d(x)} - 3 e_3`.

All coordinates are mod `m`.

## 3. Proof

Starting from `x in P0`, one `F_3^*` step raises the total sum by `1`, so over
the `m` steps defining `R_3^*`, the slice values

- `Sigma = 0,1,2,3,4,...,m-1`

occur exactly once each.

For color `3`, the contributions are therefore:

- on `Sigma=0`, the selector sends color `3` to direction `4`;
- on `Sigma=1`, it sends color `3` to direction `2`;
- on `Sigma=3`, the `q3_rule_117` table sends color `3` to direction `3`
  identically;
- on `Sigma>=4`, `Sel*` is the identity selector, so color `3` again goes to
  direction `3`.

So the only nontrivial step is the unique `Sigma=2` update.
At that moment the state is `x + e_4 + e_2`, so the active-index test sees:

- index `0` iff `x_1 = m-1`,
- index `1` iff `x_2 = m-2`,
- index `2` iff `x_3 = m-1`,
- index `3` iff `x_4 = m-2`,
- index `4` iff `x_0 = m-1`.

Reading the `q2_star_by_subset` table for color `3` gives exactly two regimes.

If `x_2 = m-2`, then the active subset contains index `1`, and the color-`3`
direction is:

- `0` exactly when indices `2,3` are both active, namely when
  `x_3 = m-1` and `x_4 = m-2`;
- `4` exactly when index `4` is active and index `2` is not, namely when
  `x_0 = m-1` and `x_3 != m-1`;
- otherwise `1`.

If `x_2 != m-2`, then index `1` is absent, and the same table reduces to:

- direction `0` exactly when indices `0,3` are both active, namely when
  `x_1 = m-1` and `x_4 = m-2`;
- otherwise direction `3`.

Combining the fixed `Sigma=0,1,3,>=4` contributions with this `Sigma=2`
description yields

- `R_3^*(x) = x + e_4 + e_2 + e_{d(x)} - 3 e_3`.

## 4. Immediate corollary

The second coordinate-clock statement is now exact:

- `x_2(R_3^*(x)) = x_2 + 1`

for every `x in P0`.

Hence the slice

- `S_m = {x in P0 : x_2 = m-2}`

is an exact `m`-step section for `R_3^*`.

## 5. Checked support

The new checker verifies on every checked modulus `m = 3,4,...,25` that:

- the explicit `P0` formula above matches the actual `R_3^*` image exactly;
- the induced section map on `S_m` matches the explicit five-branch model from
  `261` exactly.

So the remaining live step is no longer discovery of the actual first return.
It is only the manuscript-level extraction of the section law from the formula
proved here.
