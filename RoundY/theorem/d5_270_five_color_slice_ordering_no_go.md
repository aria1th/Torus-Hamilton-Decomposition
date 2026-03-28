# D5 270 Five-Color Slice-Ordering No-Go

This note records the smallest local completion family that one would try after
fixing the closed Sel* colors `3` and `4`.

Primary files:

- [torus_nd_d5_five_color_slice_ordering_search_270.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_five_color_slice_ordering_search_270.py)
- [d5_270_five_color_slice_ordering_search_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_270_five_color_slice_ordering_search_summary.json)
- [d5_268_five_color_assembly_boundary.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_268_five_color_assembly_boundary.md)
- [d5_269_selstar_color12_return_invariant_obstruction.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_269_selstar_color12_return_invariant_obstruction.md)

## 1. Family tested

Fix the closed Sel* colors:

- `h_3 = F_3^*`,
- `h_4 = F_4^*`.

At each vertex, these two colors occupy two directions, leaving exactly three
unused outgoing directions.

The smallest imaginable completion family is:

- for each slice class `Sigma = 0,1,2,3,4+`,
- sort those three remaining directions increasingly,
- then assign colors `0,1,2` to that ordered triple by one fixed permutation
  depending only on the slice class.

So the whole family has exactly

- `6^5 = 7776`

rules.

## 2. Result

The checker exhausts all `7776` such rules at `m=5` and finds:

- `0` exact completions.

So even before asking for Hamiltonicity, this smallest slice-class-only family
already fails the basic colorwise exactness requirement.

## 3. Consequence

Combined with `269`, this means the remaining five-color assembly theorem is
already narrower than a naive local completion problem:

- the current Sel* colors `1,2` are obstructed;
- and the most naive “just fill the remaining three directions by a fixed
  slice-class ordering” family does not even give a valid package.

Therefore any successful assembly theorem must use a more structured local
mechanism than:

- the raw current Sel* package, or
- a slice-class-only reordering of the three leftover directions.
