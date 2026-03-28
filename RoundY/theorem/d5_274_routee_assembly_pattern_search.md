# D5 274 Route-E Assembly Pattern Search

This note records the first genuinely simplifying reduction after the no-go
chain
[269](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_269_selstar_color12_return_invariant_obstruction.md),
[270](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_270_five_color_slice_ordering_no_go.md),
[271](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_271_five_color_coarse_defect_no_go.md).

Primary files:

- [torus_nd_d5_routee_assembly_pattern_search_274.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_routee_assembly_pattern_search_274.py)
- [d5_274_routee_assembly_pattern_search_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_274_routee_assembly_pattern_search_summary.json)
- [stable_search.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_274_routee_assembly_pattern_search/stable_search.json)
- [combined_search.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_274_routee_assembly_pattern_search/combined_search.json)

## 1. Family tested

Keep the already closed Sel* colors:

- `h_3 = F_3^*`,
- `h_4 = F_4^*`.

For the remaining colors `0,1,2`, test the simple Route-E-style class family:

- `S0`,
- `S1`,
- `S4+`,
- `S2(A2)`: the full slice-`2` active-set class,
- `S3(b1)`: the one-bit slice-`3` class `b1 = 1_{1 in A3}`.

At each source vertex:

- read its class;
- compute the three directions not used by `F_3^*`, `F_4^*`;
- assign colors `0,1,2` to those three directions by one fixed permutation
  depending only on that class.

So this is still a very small family. It is richer than the old coarse defect
bits, but it is not a new large coordinate system.

## 2. Finite local exactness compression

The main discovery is that local exactness compresses completely.

For the family above:

- the odd-`m >= 9` local exactness constraints stabilize to a finite pattern
  set of size `221`;
- the combined `m = 7,9` local exactness constraints compress to a finite
  pattern set of size `226`.

So the remaining graph-side assembly problem is no longer an open-ended search
over the full torus. Inside this family it becomes a finite CSP on class
permutations.

This is the first point where the assembly frontier starts to look like the
earlier D3 Route-E packages: finite local exactness first, then Hamiltonicity
of the surviving candidate branches.

## 3. Stable odd-pattern search

Using only the stabilized odd-`m >= 9` pattern set, the search enumerates
solutions in the compressed exactness model and evaluates them at `m = 5`.

Among the first `87` solutions, there already appears a rule with four
Hamilton colors:

- Hamilton colors: `0,2,3,4`,
- non-Hamilton color: `1`.

So inside this small class family, the obstruction is already down to a single
remaining color on the first stable search line.

This does **not** by itself prove the all-odd theorem, because the resulting
rule is only certified on the stabilized odd-pattern model and not yet on the
combined small-modulus side.

## 4. Combined `7/9` exact search

The combined exact model for `m = 7,9` is more honest for all-odd work, since
it includes the unique extra slice-`2` full-active-set class that appears at
`m = 7`.

Among the first `200` solutions of that combined exact model, the best rule has
Hamilton-count profile:

- `m = 5`: three Hamilton colors `0,3,4`,
- `m = 7`: four Hamilton colors `0,1,3,4`.

So on this stricter search line:

- color `2` is the only remaining non-Hamilton color at `m = 7`,
- while `m = 5` still leaves colors `1,2` open.

The detailed best rule is saved in
[combined_search.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_274_routee_assembly_pattern_search/combined_search.json).

## 5. Meaning for the proof frontier

This note does not close the final five-color assembly theorem.

But it changes the shape of the remaining problem in a substantial way.

What is no longer plausible:

- an open-ended search for a brand-new coordinate system,
- a repair living only in slice class,
- a repair living only in the old `245/247` defect-bit classes.

What now looks plausible:

- fix a simple compressed exact family first;
- then close one or two residual colors by a genuine Route-E return / stitching
  analysis, rather than by another broad selector search.

In other words, the remaining theorem now looks like:

1. finite local exactness in a small class family,
2. then one or two residual Hamilton closures.

That is a much narrower target than the boundary described in
[d5_268_five_color_assembly_boundary.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_268_five_color_assembly_boundary.md)
before this computation.

## 6. Bottom line

The overlooked simplification was not a direct final proof, but a finite
compression of the assembly search itself.

Inside the simple `S2(A2) + S3(one-bit)` family:

- local exactness becomes a finite pattern problem,
- four Hamilton colors already appear on the stable odd-pattern line,
- and the combined `7/9` exact model reduces the remaining burden to at most
  two colors on the checked range.

So the assembly frontier is now close enough to support a real Route-E-style
theorem program, rather than a new global search program.
