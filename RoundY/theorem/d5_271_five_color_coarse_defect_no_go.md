# D5 271 Five-Color Coarse Defect-Class No-Go

This note closes the next smallest assembly family after
[d5_270_five_color_slice_ordering_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_270_five_color_slice_ordering_no_go.md).

Primary files:

- [torus_nd_d5_five_color_coarse_defect_no_go_271.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_five_color_coarse_defect_no_go_271.py)
- [d5_271_five_color_coarse_defect_no_go_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_271_five_color_coarse_defect_no_go_summary.json)
- [per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_271_five_color_coarse_defect_no_go/per_modulus.json)
- [d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_245_G1_valid_layer_baseline_and_three_class_splice_note.tex)
- [d5_247_G1_explicit_two_swap_splice_note.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_247_G1_explicit_two_swap_splice_note.tex)

## 1. Family tested

Fix the already closed Sel* colors:

- `h_3 = F_3^*`,
- `h_4 = F_4^*`.

For the remaining colors `0,1,2`, test the historical coarse family suggested by
the old `245/247` splice picture:

- `S0`,
- `S1`,
- `S2^(0)`, `S2^(1)`,
- `S3^(0,0)`, `S3^(0,1)`, `S3^(1,0)`, `S3^(1,1)`,
- `S4+`.

The rule is:

- at each source vertex, read its coarse class;
- look at the three directions not used by `F_3^*`, `F_4^*`;
- assign colors `0,1,2` to those three directions by one fixed permutation
  depending only on the coarse class.

So this family is much richer than `270`: it already sees the old slice-`2`
old bit and the old slice-`3` predecessor flag.

## 2. Symbolic obstruction

The family is still impossible.

Take the target

- `y = (0,0,0,0,3)`.

Its predecessors along directions `1` and `2` are

- `x^(1) = y - e_1 = (0,m-1,0,0,3)`,
- `x^(2) = y - e_2 = (0,0,m-1,0,3)`.

For every odd `m >= 5`, both are in the same coarse class `S2^(0)`.
For the fixed Sel* colors `3,4`, the remaining directions at those two sources
are:

- at `x^(1)`: `(0,1,2)`,
- at `x^(2)`: `(0,2,3)`.

In both triples, the incoming target direction occupies the same sorted slot:

- at `x^(1)`, direction `1` is the middle entry;
- at `x^(2)`, direction `2` is the middle entry.

If colors `0,1,2` are assigned by one fixed permutation on the class `S2^(0)`,
then these two predecessors necessarily send the same color into `y`.
So incoming Latin exactness already fails locally.

That is enough to rule out the whole family.

## 3. Checked support

The checker verifies this local impossibility on

- `m = 5,7,9,11,13`.

For every checked modulus it finds at least one target local signature with
zero allowed class-permutation assignments. The first witness is always the same
target:

- `y = (0,0,0,0,3)`.

The counted zero-allowed local signatures are:

- `72` at `m=5`,
- `71` at `m=7`,
- `82` at `m=9`,
- `82` at `m=11`,
- `82` at `m=13`.

So the obstruction is not a one-modulus accident.

## 4. Consequence for the live theorem

After `269`, `270`, and the present note, the remaining five-color assembly
theorem is narrower in a precise way.

It cannot live in any of these families:

- the raw Sel* package itself;
- a slice-class-only reordering of the leftover directions;
- the historical defect-bit coarse family coming from the old `245/247` splice
  coordinates.

Therefore any successful assembly theorem must use finer local information than
the old slice-`2` old bit and slice-`3` predecessor flag. In practice this now
looks like a genuine Route-E-style finite-defect construction for the remaining
three colors, rather than a repair inside the historical coarse splice package.

The first witness already says more than that.
The contradiction happens inside one coarse class `S2^(0)`, because the two
source states

- `(0,m-1,0,0,3)`,
- `(0,0,m-1,0,3)`

must be treated differently, but the old family forces them to share one class
rule.
So any viable next family must at least refine the slice-`2` class `S2^(0)`
enough to distinguish these two source types. In other words, the next
theorem-search step should see more of the actual slice-`2` active-set geometry
than the old bit `x_0 = m-1`.
