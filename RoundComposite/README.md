# RoundComposite — Composite-Dimension Reduction

This directory contains the theorem-level composite-dimension reduction for
directed torus Hamilton decompositions.

Current result:

- `d_composite_product_reduction.tex`
  proves a square lemma for `D_2(m)`,
  a multiplicative-closure theorem
  `D_a + D_b => D_{ab}`,
  and the prime-reduction corollary
  `all prime dimensions solved => all composite dimensions solved`.

What is unconditional now:

- `d=2` is closed by the square lemma in this directory.
- `d=3` and `d=4` are already closed elsewhere in the repo.
- Therefore every dimension of the form `2^alpha 3^beta` with
  `alpha + beta >= 1` is now closed by repeated product reduction.
  This includes `d=6,8,9,12,16,18,...`.

What is still conditional:

- the full statement for every composite dimension still depends on the
  unresolved prime dimensions such as `d=5`, `d=7`, and beyond;
- the current note is an existence theorem, not a tiny local witness-table
  construction.

Suggested reading order:

1. `d_composite_product_reduction.tex`
2. `Result.md`
3. `../README.md`
4. `../formal/README.md`
