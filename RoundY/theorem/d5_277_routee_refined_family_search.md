# D5 277 Route-E Refined Family Search

This note packages the first direct refinement suggested by
[d5_276_routee_color2_short_cycle_structure.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_276_routee_color2_short_cycle_structure.md).

Primary files:

- [torus_nd_d5_routee_refined_family_search_277.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_routee_refined_family_search_277.py)
- [d5_277_routee_refined_family_search_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_277_routee_refined_family_search_summary.json)
- [search.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_277_routee_refined_family_search/search.json)

## 1. Family

Start from the compressed exact family of
[d5_274_routee_assembly_pattern_search.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_274_routee_assembly_pattern_search.md):

- keep the closed `Sel*` colors `3,4`;
- assign colors `0,1,2` by a permutation on the local class.

Now refine the class by the two defect markers suggested by `276`:

- `g_anchor = 1_{x_2 = m-1 and x_0 + 2x_1 + x_4 = 1 (mod m)}`,
- `m_bad = 1_{x_4 = m-1, x_2 != m-1, 2x_0 + 3x_1 = 1 (mod 3)}`.

So this is still a very small Route-E-style family. It is not a new global
coordinate system.

## 2. Search size

For the default `7/9` exactness search with evaluation on `5,7,9`, the refined
family has:

- `67` realized keys,
- `514` local exactness patterns.

So the CSP stays finite and small enough to search directly.

## 3. What improves

Among the first `200` refined exact solutions, the best rule has checked
Hamilton-count profile:

- `m=5`: `2` Hamilton colors,
- `m=7`: `3` Hamilton colors,
- `m=9`: `3` Hamilton colors.

The key new feature is that color `2`, which was the residual Route-E target
after `275–276`, becomes Hamilton on the checked moduli `7,9` for the best
refined rule.

So the `276` defect markers are not cosmetic. They do change the finite exact
family in the right direction.

## 4. What does not improve enough

The same best refined rule is still not the final five-color package.

On the checked range `5,7,9`, the best refined family still leaves:

- all colors `0,1,2` open at `m=5`,
- colors `0,1` open at `m=7`,
- colors `0,1` open at `m=9`.

So the refinement does not yet close the assembly theorem by itself.

## 5. Meaning

This search does show a genuinely new fact:

- the short-cycle data of `276` can be fed back into the exactness CSP,
- and the resulting refined family already repairs the residual color `2` on
  the checked moduli `7,9`.

But it also shows the limit of this first refinement:

- two defect markers are not enough to finish the full five-color assembly.

So the honest next step is not “go back to the old coarse search.”

It is:

1. keep the `276` markers,
2. check large-odd exactness honestly,
3. and then identify the next missing local distinction beyond `g_anchor` and
   `m_bad`.

That is exactly what the next gate note `278` records.
