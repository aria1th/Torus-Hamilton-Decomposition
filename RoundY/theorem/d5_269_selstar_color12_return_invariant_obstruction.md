# D5 269 SelStar Color-1/2 Return-Invariant Obstruction

This note records the first clean obstruction after the closure of the Sel*
color-`3` and color-`4` branches.

Primary files:

- [d5_267_full_d5_working_manuscript_routee_honest.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/tex/d5_267_full_d5_working_manuscript_routee_honest.tex)
- [torus_nd_d5_selstar_color12_return_invariants_269.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selstar_color12_return_invariants_269.py)
- [d5_269_selstar_color12_return_invariants_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_269_selstar_color12_return_invariants_summary.json)

## 1. Statement

Let `F_1^*`, `F_2^*` be the color-`1` and color-`2` torus maps of the explicit
selector surgery `Sel*`, and let

- `P0 = {Sigma = 0}`,
- `R_1^* = (F_1^*)^m | P0`,
- `R_2^* = (F_2^*)^m | P0`.

Define

- `I_1(x) = x_0 - x_2 (mod m)` on `P0`,
- `I_2(x) = x_1 - x_3 (mod m)` on `P0`.

Then for every odd `m >= 5`:

- `R_1^*` preserves `I_1`,
- `R_2^*` preserves `I_2`.

Consequently neither `F_1^*` nor `F_2^*` can be Hamilton on the full torus.

## 2. Why the invariants are natural

The `Sel*` row field differs from the clean constant slices only on `Sigma=2,3`.
For color `1`, the only slices that touch coordinates `0` or `2` in one full
`P0` return are:

- `Sigma=0`, where the color-`1` step is direction `2`,
- `Sigma=1`, where the color-`1` step is direction `0`.

Inspection of the explicit slice-`2` surgery table shows that on `Sigma=2`, the
color-`1` step never uses direction `0` or `2`, and the explicit slice-`3` rule
uses only directions `1` or `4` for color `1`. So during one `m`-step return:

- coordinate `x_2` increases once at `Sigma=0`,
- coordinate `x_0` increases once at `Sigma=1`,
- no later step changes either of those coordinates.

Hence `x_0-x_2` is preserved by `R_1^*`.

The color-`2` case is the exact cyclic analogue:

- `Sigma=0` contributes direction `3`,
- `Sigma=1` contributes direction `1`,
- the slice-`2` and slice-`3` rules never use directions `1` or `3` for color
  `2`.

So `x_1-x_3` is preserved by `R_2^*`.

## 3. Consequence for the assembly theorem

This is the first clean negative theorem for the remaining graph-side assembly
problem.

The closed Sel* colors are now split sharply:

- color `3` is Hamilton,
- color `4` is Hamilton,
- colors `1` and `2` are obstructed already by simple first-return invariants.

So the remaining five-color assembly theorem cannot simply say

> “take the current Sel* package and prove the other three colors Hamilton.”

At least colors `1` and `2` must be replaced by different assembly maps.

## 4. Checked support

The checker
[torus_nd_d5_selstar_color12_return_invariants_269.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selstar_color12_return_invariants_269.py)
verifies on checked moduli

- `m = 5,7,9,11,13`

that:

- `R_1^*` preserves `x_0-x_2`,
- `R_2^*` preserves `x_1-x_3`,
- every fiber has size exactly `m^3`.

So on `P0`, each return map already splits into at least `m` invariant fibers.
That is enough to rule out Hamiltonicity of the full torus maps `F_1^*`,
`F_2^*`.

## 5. Bottom line

The remaining graph-side theorem is now even sharper than “find three more
Hamilton colors.”

It is:

- keep the closed Sel* color-`3` and color-`4` maps,
- replace the obstructed Sel* colors `1,2`,
- and then complete a five-color selector package with Hamiltonicity.

That is the honest content of the current five-color assembly boundary.
