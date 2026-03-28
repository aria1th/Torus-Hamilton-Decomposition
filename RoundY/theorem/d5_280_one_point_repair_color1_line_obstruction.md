# D5 280 One-Point Repair Color-1 Line Obstruction

This note records the next clean obstruction after
[d5_279_one_point_repair_color2_closure.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_279_one_point_repair_color2_closure.md).

Primary files:

- [torus_nd_d5_one_point_repair_color1_lines_280.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_one_point_repair_color1_lines_280.py)
- [d5_280_one_point_repair_color1_line_obstruction_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_280_one_point_repair_color1_line_obstruction_summary.json)
- [per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_280_one_point_repair_color1_line_obstruction/per_modulus.json)

## 1. Statement

Let `F_1^#` be the color-`1` torus map of the `279` one-point repaired family,
let

- `P0 = {Sigma = 0}`,
- `R_1^# = (F_1^#)^m | P0`.

For odd moduli `m` with `3 \nmid m`, define for each

- `a,b in {0,...,m-2}`

the affine line

- `L_{a,b}(t) = (7-a-3b-3t, t, -7+2b+2t, a, b)`.

Then the checked data show that

- `R_1^#(L_{a,b}(t)) = L_{a,b}(t+1)`

for all checked odd `m = 7,11,13,17,19`.

So each `L_{a,b}` is an `m`-cycle of `R_1^#`, and the full torus map `F_1^#`
contains at least `(m-1)^2` disjoint cycles of length `m^2`.

## 2. Why this matters

`279` repaired the recurring `278` witness family and closed color `2` on the
checked range. The natural next hope was that color `1` might now admit a
Route-E-style section theorem of the same kind as colors `3` and `4`.

`280` shows that this is still too optimistic for the current repaired family.

At least when `3 \nmid m`, color `1` still has a completely explicit affine
line family of short cycles. So the current repaired family is not merely
“not yet proved Hamilton” for color `1`; it is visibly non-Hamilton.

## 3. Shape of the obstruction

The obstruction is cleaner than the old Sel* first-return invariant from
[d5_269_selstar_color12_return_invariant_obstruction.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_269_selstar_color12_return_invariant_obstruction.md).

It is not a preserved scalar fiber such as `x_0-x_2`.

It is an explicit family of affine lines on `P0`:

- `x_3 = a`,
- `x_4 = b`,
- `x_0 + 3x_1 + x_3 + 3x_4 = 7`,
- and then `x_2` is forced by `Sigma = 0`.

Along each such line the return is simply

- `t -> t+1`.

So the residual color-`1` burden in the repaired family is now very concrete:

- the line family must be broken,
- or the family itself must be refined so that these lines no longer remain
  invariant.

## 4. Checked boundary

The same formula fails on the checked multiples of `3`

- `m = 9,15`.

So `280` is not yet a full all-odd theorem for color `1`.

But it is still strong enough to sharpen the frontier:

- for all checked odd `m` with `3 \nmid m`, the current repaired family cannot
  possibly be the final five-color assembly package.

## 5. Bottom line

After `279`, the live frontier is not “understand residual color `1` somehow.”

It is narrower:

- the current repaired family leaves an explicit affine line family invariant,
- that line family already explains the observed `(m-1)^2` short `m^2`-cycles,
- so the next Route-E refinement must specifically break the relation
  `x_0 + 3x_1 + x_3 + 3x_4 = 7` in the residual color-`1` branch.
